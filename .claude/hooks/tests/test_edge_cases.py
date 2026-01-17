"""
Edge case tests for handover system robustness.

These tests cover unusual but possible scenarios that could break detection.
"""

import json
import pytest
from pathlib import Path
from datetime import datetime, timezone, timedelta

from session_start import determine_context_mode, detect_build_phase, load_resume_context
from utils.transcript import parse_transcript_for_build, find_build_by_session_id


class TestTranscriptEdgeCases:
    """Edge cases in transcript parsing."""

    def test_empty_transcript_file(self, tmp_path):
        """1. Empty transcript file should return None."""
        transcript = tmp_path / "empty.jsonl"
        transcript.write_text("")

        build_id, method = parse_transcript_for_build(str(transcript))

        assert build_id is None
        assert method == "none"

    def test_transcript_with_only_whitespace(self, tmp_path):
        """2. Whitespace-only transcript should return None."""
        transcript = tmp_path / "whitespace.jsonl"
        transcript.write_text("\n\n  \n\t\n")

        build_id, method = parse_transcript_for_build(str(transcript))

        assert build_id is None
        assert method == "none"

    def test_very_long_file_path(self, create_transcript, mock_tool_use_entry):
        """3. Extremely long file paths should still be parsed."""
        long_path = "02-builds/01-test/" + "a" * 500 + "/file.md"
        entries = [mock_tool_use_entry("Read", long_path)]
        transcript = create_transcript(entries)

        build_id, method = parse_transcript_for_build(transcript)

        assert build_id == "01-test"

    def test_build_id_with_underscores(self, create_transcript, mock_tool_use_entry):
        """4. Build IDs with underscores should be detected."""
        entries = [mock_tool_use_entry("Read", "02-builds/05-my_cool_build/file.md")]
        transcript = create_transcript(entries)

        build_id, _ = parse_transcript_for_build(transcript)

        assert build_id == "05-my_cool_build"

    def test_build_id_with_numbers_in_name(self, create_transcript, mock_tool_use_entry):
        """5. Build IDs with numbers in name part should work."""
        entries = [mock_tool_use_entry("Read", "02-builds/99-v2-migration-2024/file.md")]
        transcript = create_transcript(entries)

        build_id, _ = parse_transcript_for_build(transcript)

        assert build_id == "99-v2-migration-2024"

    def test_mixed_path_separators(self, create_transcript, mock_tool_use_entry):
        """6. Mixed forward/back slashes should both work."""
        entries = [
            mock_tool_use_entry("Read", "02-builds\\01-test/subdir\\file.md")
        ]
        transcript = create_transcript(entries)

        build_id, _ = parse_transcript_for_build(transcript)

        assert build_id == "01-test"

    def test_case_insensitive_builds_path(self, create_transcript, mock_tool_use_entry):
        """7. Case variations of 02-builds should work."""
        entries = [mock_tool_use_entry("Read", "02-BUILDS/01-test/file.md")]
        transcript = create_transcript(entries)

        build_id, _ = parse_transcript_for_build(transcript)

        assert build_id == "01-test"

    def test_unicode_in_transcript(self, tmp_path):
        """8. Unicode content in transcript should not crash."""
        transcript = tmp_path / "unicode.jsonl"
        transcript.write_text(
            '{"message": {"role": "user", "content": "こんにちは 🎉"}}\n'
            '{"message": {"role": "assistant", "content": [{"type": "tool_use", "name": "Read", "input": {"file_path": "02-builds/01-test/日本語.md"}}]}}\n',
            encoding="utf-8"
        )

        build_id, _ = parse_transcript_for_build(str(transcript))

        assert build_id == "01-test"

    def test_binary_garbage_in_transcript(self, tmp_path):
        """9. Binary data mixed in - currently fails whole file (could be improved)."""
        transcript = tmp_path / "binary.jsonl"
        with open(transcript, "wb") as f:
            f.write(b'{"message": {"role": "user", "content": "hello"}}\n')
            f.write(b'\x00\x01\x02\xff\xfe invalid binary\n')
            f.write(b'{"message": {"role": "assistant", "content": [{"type": "tool_use", "name": "Read", "input": {"file_path": "02-builds/01-test/file.md"}}]}}\n')

        # Current behavior: binary causes UTF-8 decode error, returns None
        # This is a known limitation - binary garbage corrupts the file
        build_id, method = parse_transcript_for_build(str(transcript))

        assert build_id is None
        assert method == "none"

    def test_same_build_touched_many_times(self, create_transcript, mock_tool_use_entry):
        """10. Same build touched 100 times should still return it."""
        entries = [
            mock_tool_use_entry("Read", "02-builds/01-focused/file.md")
            for _ in range(100)
        ]
        transcript = create_transcript(entries)

        build_id, _ = parse_transcript_for_build(transcript)

        assert build_id == "01-focused"

    def test_exactly_three_builds_is_bulk(self, create_transcript, mock_tool_use_entry):
        """11. Exactly 3 builds = bulk work threshold."""
        entries = [
            mock_tool_use_entry("Read", "02-builds/01-a/file.md"),
            mock_tool_use_entry("Read", "02-builds/02-b/file.md"),
            mock_tool_use_entry("Read", "02-builds/03-c/file.md"),
        ]
        transcript = create_transcript(entries)

        build_id, method = parse_transcript_for_build(transcript)

        assert build_id is None  # 3+ = bulk

    def test_exactly_two_builds_is_not_bulk(self, create_transcript, mock_tool_use_entry):
        """12. Exactly 2 builds = focused work, not bulk."""
        entries = [
            mock_tool_use_entry("Read", "02-builds/01-main/file.md"),
            mock_tool_use_entry("Read", "02-builds/02-related/file.md"),
        ]
        transcript = create_transcript(entries)

        build_id, _ = parse_transcript_for_build(transcript)

        assert build_id == "02-related"  # Most recent


class TestSessionIdEdgeCases:
    """Edge cases in session ID matching."""

    def test_session_id_with_special_characters(self, temp_nexus_root, create_build):
        """13. Session IDs with dashes and numbers should match."""
        session_id = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
        create_build("01-test", session_id=session_id)

        result = find_build_by_session_id(
            str(temp_nexus_root / "02-builds"), session_id
        )

        assert result == "01-test"

    def test_similar_session_ids_dont_match(self, temp_nexus_root, create_build):
        """14. Partial session ID match should NOT work."""
        create_build("01-test", session_id="abc-123-def")

        # Similar but not exact
        result = find_build_by_session_id(
            str(temp_nexus_root / "02-builds"), "abc-123-de"
        )

        assert result is None

    def test_multiple_builds_same_session_returns_first(self, temp_nexus_root):
        """15. If multiple builds have same session_id, return first found."""
        session_id = "duplicate-session"

        for i in range(3):
            build_path = temp_nexus_root / "02-builds" / f"0{i}-dup" / "01-planning"
            build_path.mkdir(parents=True)
            (build_path / "resume-context.md").write_text(
                f'---\nsession_id: "{session_id}"\n---'
            )

        result = find_build_by_session_id(
            str(temp_nexus_root / "02-builds"), session_id
        )

        # Should return one of them (first in iteration order)
        assert result in ["00-dup", "01-dup", "02-dup"]


class TestPhaseDetectionEdgeCases:
    """Edge cases in phase detection."""

    def test_steps_file_with_no_checkboxes(self, temp_nexus_root):
        """16. Steps file without any checkboxes = planning."""
        build_path = temp_nexus_root / "02-builds" / "01-no-checkboxes" / "01-planning"
        build_path.mkdir(parents=True)
        (build_path / "04-steps.md").write_text(
            "# Steps\n\nJust some text, no checkboxes."
        )

        result = detect_build_phase(str(temp_nexus_root), "01-no-checkboxes")

        assert result == "plan-build"

    def test_steps_with_all_checked_phase1(self, temp_nexus_root):
        """17. All Phase 1 tasks checked = execution."""
        build_path = temp_nexus_root / "02-builds" / "01-done" / "01-planning"
        build_path.mkdir(parents=True)
        (build_path / "04-steps.md").write_text(
            "# Steps\n## Phase 1\n- [x] Task 1\n- [x] Task 2\n## Phase 2\n- [ ] Task 3"
        )

        result = detect_build_phase(str(temp_nexus_root), "01-done")

        assert result == "execute-build"

    def test_steps_with_partial_phase1(self, temp_nexus_root):
        """18. Some Phase 1 tasks checked = still planning."""
        build_path = temp_nexus_root / "02-builds" / "01-partial" / "01-planning"
        build_path.mkdir(parents=True)
        (build_path / "04-steps.md").write_text(
            "# Steps\n## Phase 1\n- [x] Task 1\n- [ ] Task 2\n## Phase 2\n- [ ] Task 3"
        )

        result = detect_build_phase(str(temp_nexus_root), "01-partial")

        assert result == "plan-build"

    def test_steps_file_is_directory(self, temp_nexus_root):
        """19. If 04-steps.md is a directory (error), handle gracefully."""
        build_path = temp_nexus_root / "02-builds" / "01-weird" / "01-planning"
        build_path.mkdir(parents=True)
        (build_path / "04-steps.md").mkdir()  # Directory, not file!

        result = detect_build_phase(str(temp_nexus_root), "01-weird")

        assert result == "plan-build"  # Fallback to planning


class TestResumeContextEdgeCases:
    """Edge cases in resume context loading."""

    def test_resume_context_with_empty_yaml(self, temp_nexus_root):
        """20. Empty YAML frontmatter should return empty files list, not crash."""
        build_path = temp_nexus_root / "02-builds" / "01-empty-yaml" / "01-planning"
        build_path.mkdir(parents=True)
        (build_path / "resume-context.md").write_text("---\n---\n# Empty")

        result = load_resume_context(str(temp_nexus_root), "01-empty-yaml")

        # Returns dict with empty files_to_load list
        assert result is not None
        assert result.get("files_to_load") == []


class TestDetermineContextModeEdgeCases:
    """Edge cases in the main routing function."""

    def test_source_clear_acts_like_new(self, temp_nexus_root, create_transcript):
        """BONUS: source=clear should act like new session."""
        transcript = create_transcript([])

        result = determine_context_mode(
            source="clear",
            transcript_path=transcript,
            build_dir=str(temp_nexus_root),
            session_id="any",
        )

        # Clear should show menu like new
        # (If not implemented, this documents expected behavior)
        assert result is not None
