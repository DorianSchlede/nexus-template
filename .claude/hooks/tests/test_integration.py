"""
Integration tests for the full handover flow.

Tests the complete cycle:
PreCompact saves state → SessionStart detects → builds correct context
"""

import json
import os
import pytest
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch, MagicMock

from save_resume_state import update_build_resume_context
from session_start import determine_context_mode, detect_build_phase
from utils.transcript import find_build_by_session_id, parse_transcript_for_build


class TestHandoverCycle:
    """Test complete handover cycles."""

    def test_compact_resume_cycle(
        self, temp_nexus_root, create_build, create_transcript, mock_tool_use_entry
    ):
        """
        Full cycle: User works on build → compact → resume in same session

        PreCompact saves session_id → SessionStart finds by session_id
        """
        build_id = "10-cycle-test"
        session_id = "cycle-session-12345"

        # 1. Create build (simulating initial creation)
        create_build(build_id, phase1_complete=False)

        # 2. Simulate work: user reads/writes build files
        entries = [
            mock_tool_use_entry("Read", f"02-builds/{build_id}/01-planning/01-overview.md"),
            mock_tool_use_entry("Write", f"02-builds/{build_id}/03-working/notes.md"),
        ]
        transcript = create_transcript(entries)

        # 3. PreCompact: Save session_id to resume-context.md
        update_build_resume_context(temp_nexus_root, build_id, session_id)

        # 4. SessionStart (compact): Should detect build via session_id
        result = determine_context_mode(
            source="compact",
            transcript_path=transcript,
            build_dir=str(temp_nexus_root),
            session_id=session_id,
        )

        assert result["mode"] == "compact"
        assert result["build_id"] == build_id
        assert result["action"] == "continue_working"
        assert result["phase"] == "planning"  # Phase 1 incomplete

    def test_cross_session_resume(self, temp_nexus_root, create_build, create_transcript):
        """
        Cross-session resume: User closed Claude, opens next day

        PreCompact saved state → SessionStart (resume) finds by session_id match
        """
        build_id = "11-cross-session"
        session_id = "yesterday-session"

        # 1. Build was worked on yesterday, PreCompact saved session_id
        create_build(build_id, phase1_complete=True, session_id=session_id)

        # 2. New session starts (no transcript content)
        transcript = create_transcript([])

        # 3. SessionStart (resume): Should find build via session_id
        result = determine_context_mode(
            source="resume",
            transcript_path=transcript,
            build_dir=str(temp_nexus_root),
            session_id=session_id,
        )

        assert result["mode"] == "compact"
        assert result["build_id"] == build_id
        assert result["phase"] == "execution"  # Phase 1 complete

    def test_new_session_shows_menu(self, temp_nexus_root, create_build, create_transcript):
        """New session always shows menu, regardless of builds."""
        create_build("12-existing", phase1_complete=True)

        transcript = create_transcript([])

        result = determine_context_mode(
            source="new",
            transcript_path=transcript,
            build_dir=str(temp_nexus_root),
            session_id="fresh-session",
        )

        assert result["mode"] == "startup"
        assert result["action"] == "display_menu"
        assert result["build_id"] is None

    def test_skill_read_keeps_build_context(
        self, temp_nexus_root, create_build, tmp_path
    ):
        """
        User was on build, then read a skill file → STAYS in build context

        This is the new behavior: once in a build, stay in build.
        """
        build_id = "13-switched"
        session_id = "switch-session"

        create_build(build_id, session_id=session_id)

        # Transcript: build work, then skill read - should STAY in build
        transcript = tmp_path / "transcript.jsonl"
        transcript.write_text(
            '{"message": {"role": "assistant", "content": [{"type": "tool_use", "name": "Read", "input": {"file_path": "02-builds/13-switched/file.md"}}]}}\n'
            '{"content": "03-skills/paper-search/SKILL.md"}\n'
        )

        result = determine_context_mode(
            source="compact",
            transcript_path=str(transcript),
            build_dir=str(temp_nexus_root),
            session_id=session_id,
        )

        # Build context is PRESERVED
        assert result["mode"] == "compact"
        assert result["action"] == "continue_working"
        assert result["build_id"] == build_id

    def test_phase_detection_accuracy(self, temp_nexus_root, create_build, create_transcript):
        """Verify phase detection correctly distinguishes planning vs execution."""
        # Planning build (Phase 1 incomplete)
        create_build("14-planning", phase1_complete=False, session_id="plan-session")

        # Execution build (Phase 1 complete)
        create_build("15-executing", phase1_complete=True, session_id="exec-session")

        transcript = create_transcript([])

        # Test planning
        plan_result = determine_context_mode(
            source="resume",
            transcript_path=transcript,
            build_dir=str(temp_nexus_root),
            session_id="plan-session",
        )
        assert plan_result["phase"] == "planning"
        assert plan_result["skill"] == "plan-build"

        # Test execution
        exec_result = determine_context_mode(
            source="resume",
            transcript_path=transcript,
            build_dir=str(temp_nexus_root),
            session_id="exec-session",
        )
        assert exec_result["phase"] == "execution"
        assert exec_result["skill"] == "execute-build"


class TestDetectionPriority:
    """Test detection priority: session_id > transcript."""

    def test_session_id_takes_priority(
        self, temp_nexus_root, create_build, create_transcript, mock_tool_use_entry
    ):
        """Session ID match should win over transcript detection."""
        # Create two builds
        create_build("20-session-match", session_id="priority-session")
        create_build("21-transcript-match")

        # Transcript shows work on 21-transcript-match
        entries = [
            mock_tool_use_entry("Read", "02-builds/21-transcript-match/file.md")
        ]
        transcript = create_transcript(entries)

        # But session_id matches 20-session-match
        result = determine_context_mode(
            source="compact",
            transcript_path=transcript,
            build_dir=str(temp_nexus_root),
            session_id="priority-session",
        )

        # Session ID should win
        assert result["build_id"] == "20-session-match"

    def test_transcript_fallback_works(
        self, temp_nexus_root, create_build, create_transcript, mock_tool_use_entry
    ):
        """When no session_id match, transcript detection is used."""
        create_build("22-no-session-match")

        entries = [
            mock_tool_use_entry("Write", "02-builds/22-no-session-match/file.md")
        ]
        transcript = create_transcript(entries)

        result = determine_context_mode(
            source="compact",
            transcript_path=transcript,
            build_dir=str(temp_nexus_root),
            session_id="unknown-session",
        )

        assert result["build_id"] == "22-no-session-match"


class TestEdgeCases:
    """Edge cases and error handling."""

    def test_empty_builds_directory(self, temp_nexus_root, create_transcript):
        """Handle empty 02-builds/ gracefully."""
        transcript = create_transcript([])

        result = determine_context_mode(
            source="resume",
            transcript_path=transcript,
            build_dir=str(temp_nexus_root),
            session_id="orphan",
        )

        assert result["mode"] == "startup"
        assert result["action"] == "display_menu"

    def test_missing_builds_directory(self, tmp_path, create_transcript):
        """Handle missing 02-builds/ gracefully."""
        transcript = create_transcript([])

        result = determine_context_mode(
            source="resume",
            transcript_path=transcript,
            build_dir=str(tmp_path),
            session_id="orphan",
        )

        assert result["mode"] == "startup"

    def test_malformed_resume_context(self, temp_nexus_root, create_transcript):
        """Handle malformed resume-context.md gracefully."""
        build_path = temp_nexus_root / "02-builds" / "30-malformed" / "01-planning"
        build_path.mkdir(parents=True)
        (build_path / "resume-context.md").write_text("not valid yaml at all {{{{")

        transcript = create_transcript([])

        # Should not crash
        result = determine_context_mode(
            source="resume",
            transcript_path=transcript,
            build_dir=str(temp_nexus_root),
            session_id="malformed-session",
        )

        assert result is not None

    def test_missing_transcript(self, temp_nexus_root, create_build):
        """Handle missing transcript file gracefully."""
        create_build("31-no-transcript", session_id="no-transcript-session")

        result = determine_context_mode(
            source="compact",
            transcript_path="/nonexistent/transcript.jsonl",
            build_dir=str(temp_nexus_root),
            session_id="no-transcript-session",
        )

        # Should still work via session_id
        assert result["build_id"] == "31-no-transcript"
