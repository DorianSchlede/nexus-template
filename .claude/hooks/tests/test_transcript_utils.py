"""
Tests for utils/transcript.py - Transcript parsing utilities.
"""

import json
import pytest
from pathlib import Path

from utils.transcript import (
    find_build_by_session_id,
    parse_transcript_for_build,
    check_skill_switch_after_build,
    BUILD_PATTERN,
    SESSION_ID_PATTERN,
)


class TestBuildPattern:
    """Tests for the BUILD_PATTERN regex."""

    def test_matches_standard_build_path(self):
        match = BUILD_PATTERN.search("02-builds/01-test-build/file.md")
        assert match is not None
        assert match.group(1) == "01-test-build"

    def test_matches_windows_path(self):
        match = BUILD_PATTERN.search("02-builds\\01-test-build\\file.md")
        assert match is not None
        assert match.group(1) == "01-test-build"

    def test_matches_with_numbers_and_hyphens(self):
        match = BUILD_PATTERN.search("02-builds/28-handover-test-suite/01-planning/steps.md")
        assert match is not None
        assert match.group(1) == "28-handover-test-suite"

    def test_no_match_for_other_paths(self):
        assert BUILD_PATTERN.search("03-skills/my-skill/SKILL.md") is None
        assert BUILD_PATTERN.search("random/path/file.txt") is None


class TestSessionIdPattern:
    """Tests for the SESSION_ID_PATTERN regex."""

    def test_matches_standard_format(self):
        content = 'session_id: "abc-123-def"'
        match = SESSION_ID_PATTERN.search(content)
        assert match is not None
        assert match.group(1) == "abc-123-def"

    def test_matches_in_yaml_block(self):
        content = """---
session_id: "test-session-uuid"
last_updated: "2024-01-01"
---"""
        match = SESSION_ID_PATTERN.search(content)
        assert match is not None
        assert match.group(1) == "test-session-uuid"


class TestFindBuildBySessionId:
    """Tests for find_build_by_session_id()"""

    def test_finds_matching_build(self, temp_nexus_root, create_build):
        session_id = "test-session-123"
        create_build("01-my-build", session_id=session_id)

        result = find_build_by_session_id(
            str(temp_nexus_root / "02-builds"), session_id
        )

        assert result == "01-my-build"

    def test_returns_none_for_no_match(self, temp_nexus_root, create_build):
        create_build("01-my-build", session_id="different-session")

        result = find_build_by_session_id(
            str(temp_nexus_root / "02-builds"), "non-existent-session"
        )

        assert result is None

    def test_returns_none_for_empty_session_id(self, temp_nexus_root):
        result = find_build_by_session_id(str(temp_nexus_root / "02-builds"), "")
        assert result is None

    def test_returns_none_for_unknown_session_id(self, temp_nexus_root):
        result = find_build_by_session_id(
            str(temp_nexus_root / "02-builds"), "unknown"
        )
        assert result is None

    def test_returns_none_for_missing_directory(self, tmp_path):
        result = find_build_by_session_id(str(tmp_path / "nonexistent"), "test")
        assert result is None

    def test_multiple_builds_finds_correct_one(self, temp_nexus_root, create_build):
        create_build("01-first", session_id="session-1")
        create_build("02-second", session_id="session-2")
        create_build("03-third", session_id="session-3")

        result = find_build_by_session_id(
            str(temp_nexus_root / "02-builds"), "session-2"
        )

        assert result == "02-second"


class TestParseTranscriptForBuild:
    """Tests for parse_transcript_for_build()"""

    def test_extracts_build_from_read_tool(self, create_transcript, mock_tool_use_entry):
        entries = [
            mock_tool_use_entry("Read", "02-builds/05-my-build/01-planning/overview.md")
        ]
        transcript = create_transcript(entries)

        build_id, method = parse_transcript_for_build(transcript)

        assert build_id == "05-my-build"
        assert method == "transcript"

    def test_extracts_build_from_write_tool(self, create_transcript, mock_tool_use_entry):
        entries = [
            mock_tool_use_entry("Write", "02-builds/10-another/03-working/draft.md")
        ]
        transcript = create_transcript(entries)

        build_id, method = parse_transcript_for_build(transcript)

        assert build_id == "10-another"
        assert method == "transcript"

    def test_extracts_build_from_edit_tool(self, create_transcript, mock_tool_use_entry):
        entries = [
            mock_tool_use_entry("Edit", "02-builds/03-test/file.py")
        ]
        transcript = create_transcript(entries)

        build_id, method = parse_transcript_for_build(transcript)

        assert build_id == "03-test"
        assert method == "transcript"

    def test_returns_most_recent_build_when_two(self, create_transcript, mock_tool_use_entry):
        """With 2 builds, return most recent (not bulk work)."""
        entries = [
            mock_tool_use_entry("Read", "02-builds/01-first/file.md"),
            mock_tool_use_entry("Write", "02-builds/02-second/file.md"),
        ]
        transcript = create_transcript(entries)

        build_id, _ = parse_transcript_for_build(transcript)

        assert build_id == "02-second"

    def test_returns_none_for_multi_build_session(self, create_transcript, mock_tool_use_entry):
        """With 3+ builds touched, this is bulk work - no single active build."""
        entries = [
            mock_tool_use_entry("Read", "02-builds/01-first/file.md"),
            mock_tool_use_entry("Read", "02-builds/02-second/file.md"),
            mock_tool_use_entry("Write", "02-builds/03-third/file.md"),
        ]
        transcript = create_transcript(entries)

        build_id, method = parse_transcript_for_build(transcript)

        assert build_id is None
        assert method == "none"

    def test_returns_none_for_no_build(self, create_transcript, mock_tool_use_entry):
        entries = [
            mock_tool_use_entry("Read", "03-skills/my-skill/SKILL.md"),
            mock_tool_use_entry("Read", "01-memory/goals.md"),
        ]
        transcript = create_transcript(entries)

        build_id, method = parse_transcript_for_build(transcript)

        assert build_id is None
        assert method == "none"

    def test_returns_none_for_missing_file(self):
        build_id, method = parse_transcript_for_build("/nonexistent/path.jsonl")

        assert build_id is None
        assert method == "none"

    def test_handles_malformed_jsonl(self, create_transcript, mock_tool_use_entry):
        # Create transcript with some invalid lines
        entries = [
            mock_tool_use_entry("Read", "02-builds/05-test/file.md"),
        ]
        transcript_path = create_transcript(entries)

        # Append malformed line
        with open(transcript_path, "a") as f:
            f.write("not valid json\n")

        build_id, _ = parse_transcript_for_build(transcript_path)

        assert build_id == "05-test"

    def test_ignores_non_file_tools(self, create_transcript):
        entries = [
            {
                "message": {
                    "role": "assistant",
                    "content": [
                        {
                            "type": "tool_use",
                            "name": "TodoWrite",
                            "input": {"todos": []},
                        }
                    ],
                }
            }
        ]
        transcript = create_transcript(entries)

        build_id, method = parse_transcript_for_build(transcript)

        assert build_id is None
        assert method == "none"

    def test_ignores_user_messages(self, create_transcript):
        entries = [
            {
                "message": {
                    "role": "user",
                    "content": "work on 02-builds/01-test/file.md",
                }
            }
        ]
        transcript = create_transcript(entries)

        build_id, method = parse_transcript_for_build(transcript)

        assert build_id is None
        assert method == "none"


class TestCheckSkillSwitchAfterBuild:
    """Tests for check_skill_switch_after_build()"""

    def test_detects_user_skill_switch(self, tmp_path):
        transcript = tmp_path / "transcript.jsonl"
        transcript.write_text(
            '{"content": "02-builds/05-test/file.md"}\n'
            '{"content": "03-skills/paper-search/SKILL.md"}\n'
        )

        result = check_skill_switch_after_build(str(transcript), "05-test")

        assert result is True

    def test_detects_system_skill_switch(self, tmp_path):
        """
        System skills matching 00-system/skills/[not-builds]/SKILL.md count as switch.

        Note: The current regex pattern matches skills directly under skills/,
        not nested like system/close-session/. This tests actual behavior.
        """
        transcript = tmp_path / "transcript.jsonl"
        # Use a skill path that matches the regex: 00-system/skills/[^/]+/SKILL.md
        transcript.write_text(
            '{"content": "02-builds/05-test/file.md"}\n'
            '{"content": "00-system/skills/learning/SKILL.md"}\n'
        )

        result = check_skill_switch_after_build(str(transcript), "05-test")

        assert result is True

    def test_no_switch_when_only_build(self, tmp_path):
        transcript = tmp_path / "transcript.jsonl"
        transcript.write_text(
            '{"content": "02-builds/05-test/file.md"}\n'
            '{"content": "02-builds/05-test/another.md"}\n'
        )

        result = check_skill_switch_after_build(str(transcript), "05-test")

        assert result is False

    def test_no_switch_for_build_skills(self, tmp_path):
        """execute-build and plan-build should NOT count as switches."""
        transcript = tmp_path / "transcript.jsonl"
        transcript.write_text(
            '{"content": "02-builds/05-test/file.md"}\n'
            '{"content": "00-system/skills/builds/execute-build/SKILL.md"}\n'
        )

        result = check_skill_switch_after_build(str(transcript), "05-test")

        assert result is False

    def test_returns_false_for_no_build(self, tmp_path):
        transcript = tmp_path / "transcript.jsonl"
        transcript.write_text('{"content": "some content"}\n')

        result = check_skill_switch_after_build(str(transcript), None)

        assert result is False

    def test_returns_false_for_missing_file(self):
        result = check_skill_switch_after_build("/nonexistent.jsonl", "05-test")
        assert result is False

    def test_skill_before_build_not_counted(self, tmp_path):
        """Skill BEFORE build should not count as switch."""
        transcript = tmp_path / "transcript.jsonl"
        transcript.write_text(
            '{"content": "03-skills/paper-search/SKILL.md"}\n'
            '{"content": "02-builds/05-test/file.md"}\n'
        )

        result = check_skill_switch_after_build(str(transcript), "05-test")

        assert result is False
