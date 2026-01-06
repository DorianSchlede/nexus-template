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

from save_resume_state import update_project_resume_context
from session_start import determine_context_mode, detect_project_phase
from utils.transcript import find_project_by_session_id, parse_transcript_for_project


class TestHandoverCycle:
    """Test complete handover cycles."""

    def test_compact_resume_cycle(
        self, temp_nexus_root, create_project, create_transcript, mock_tool_use_entry
    ):
        """
        Full cycle: User works on project → compact → resume in same session

        PreCompact saves session_id → SessionStart finds by session_id
        """
        project_id = "10-cycle-test"
        session_id = "cycle-session-12345"

        # 1. Create project (simulating initial creation)
        create_project(project_id, phase1_complete=False)

        # 2. Simulate work: user reads/writes project files
        entries = [
            mock_tool_use_entry("Read", f"02-projects/{project_id}/01-planning/01-overview.md"),
            mock_tool_use_entry("Write", f"02-projects/{project_id}/03-working/notes.md"),
        ]
        transcript = create_transcript(entries)

        # 3. PreCompact: Save session_id to resume-context.md
        update_project_resume_context(temp_nexus_root, project_id, session_id)

        # 4. SessionStart (compact): Should detect project via session_id
        result = determine_context_mode(
            source="compact",
            transcript_path=transcript,
            project_dir=str(temp_nexus_root),
            session_id=session_id,
        )

        assert result["mode"] == "compact"
        assert result["project_id"] == project_id
        assert result["action"] == "continue_working"
        assert result["phase"] == "planning"  # Phase 1 incomplete

    def test_cross_session_resume(self, temp_nexus_root, create_project, create_transcript):
        """
        Cross-session resume: User closed Claude, opens next day

        PreCompact saved state → SessionStart (resume) finds by session_id match
        """
        project_id = "11-cross-session"
        session_id = "yesterday-session"

        # 1. Project was worked on yesterday, PreCompact saved session_id
        create_project(project_id, phase1_complete=True, session_id=session_id)

        # 2. New session starts (no transcript content)
        transcript = create_transcript([])

        # 3. SessionStart (resume): Should find project via session_id
        result = determine_context_mode(
            source="resume",
            transcript_path=transcript,
            project_dir=str(temp_nexus_root),
            session_id=session_id,
        )

        assert result["mode"] == "compact"
        assert result["project_id"] == project_id
        assert result["phase"] == "execution"  # Phase 1 complete

    def test_new_session_shows_menu(self, temp_nexus_root, create_project, create_transcript):
        """New session always shows menu, regardless of projects."""
        create_project("12-existing", phase1_complete=True)

        transcript = create_transcript([])

        result = determine_context_mode(
            source="new",
            transcript_path=transcript,
            project_dir=str(temp_nexus_root),
            session_id="fresh-session",
        )

        assert result["mode"] == "startup"
        assert result["action"] == "display_menu"
        assert result["project_id"] is None

    def test_skill_read_keeps_project_context(
        self, temp_nexus_root, create_project, tmp_path
    ):
        """
        User was on project, then read a skill file → STAYS in project context

        This is the new behavior: once in a project, stay in project.
        """
        project_id = "13-switched"
        session_id = "switch-session"

        create_project(project_id, session_id=session_id)

        # Transcript: project work, then skill read - should STAY in project
        transcript = tmp_path / "transcript.jsonl"
        transcript.write_text(
            '{"message": {"role": "assistant", "content": [{"type": "tool_use", "name": "Read", "input": {"file_path": "02-projects/13-switched/file.md"}}]}}\n'
            '{"content": "03-skills/paper-search/SKILL.md"}\n'
        )

        result = determine_context_mode(
            source="compact",
            transcript_path=str(transcript),
            project_dir=str(temp_nexus_root),
            session_id=session_id,
        )

        # Project context is PRESERVED
        assert result["mode"] == "compact"
        assert result["action"] == "continue_working"
        assert result["project_id"] == project_id

    def test_phase_detection_accuracy(self, temp_nexus_root, create_project, create_transcript):
        """Verify phase detection correctly distinguishes planning vs execution."""
        # Planning project (Phase 1 incomplete)
        create_project("14-planning", phase1_complete=False, session_id="plan-session")

        # Execution project (Phase 1 complete)
        create_project("15-executing", phase1_complete=True, session_id="exec-session")

        transcript = create_transcript([])

        # Test planning
        plan_result = determine_context_mode(
            source="resume",
            transcript_path=transcript,
            project_dir=str(temp_nexus_root),
            session_id="plan-session",
        )
        assert plan_result["phase"] == "planning"
        assert plan_result["skill"] == "plan-project"

        # Test execution
        exec_result = determine_context_mode(
            source="resume",
            transcript_path=transcript,
            project_dir=str(temp_nexus_root),
            session_id="exec-session",
        )
        assert exec_result["phase"] == "execution"
        assert exec_result["skill"] == "execute-project"


class TestDetectionPriority:
    """Test detection priority: session_id > transcript."""

    def test_session_id_takes_priority(
        self, temp_nexus_root, create_project, create_transcript, mock_tool_use_entry
    ):
        """Session ID match should win over transcript detection."""
        # Create two projects
        create_project("20-session-match", session_id="priority-session")
        create_project("21-transcript-match")

        # Transcript shows work on 21-transcript-match
        entries = [
            mock_tool_use_entry("Read", "02-projects/21-transcript-match/file.md")
        ]
        transcript = create_transcript(entries)

        # But session_id matches 20-session-match
        result = determine_context_mode(
            source="compact",
            transcript_path=transcript,
            project_dir=str(temp_nexus_root),
            session_id="priority-session",
        )

        # Session ID should win
        assert result["project_id"] == "20-session-match"

    def test_transcript_fallback_works(
        self, temp_nexus_root, create_project, create_transcript, mock_tool_use_entry
    ):
        """When no session_id match, transcript detection is used."""
        create_project("22-no-session-match")

        entries = [
            mock_tool_use_entry("Write", "02-projects/22-no-session-match/file.md")
        ]
        transcript = create_transcript(entries)

        result = determine_context_mode(
            source="compact",
            transcript_path=transcript,
            project_dir=str(temp_nexus_root),
            session_id="unknown-session",
        )

        assert result["project_id"] == "22-no-session-match"


class TestEdgeCases:
    """Edge cases and error handling."""

    def test_empty_projects_directory(self, temp_nexus_root, create_transcript):
        """Handle empty 02-projects/ gracefully."""
        transcript = create_transcript([])

        result = determine_context_mode(
            source="resume",
            transcript_path=transcript,
            project_dir=str(temp_nexus_root),
            session_id="orphan",
        )

        assert result["mode"] == "startup"
        assert result["action"] == "display_menu"

    def test_missing_projects_directory(self, tmp_path, create_transcript):
        """Handle missing 02-projects/ gracefully."""
        transcript = create_transcript([])

        result = determine_context_mode(
            source="resume",
            transcript_path=transcript,
            project_dir=str(tmp_path),
            session_id="orphan",
        )

        assert result["mode"] == "startup"

    def test_malformed_resume_context(self, temp_nexus_root, create_transcript):
        """Handle malformed resume-context.md gracefully."""
        project_path = temp_nexus_root / "02-projects" / "30-malformed" / "01-planning"
        project_path.mkdir(parents=True)
        (project_path / "resume-context.md").write_text("not valid yaml at all {{{{")

        transcript = create_transcript([])

        # Should not crash
        result = determine_context_mode(
            source="resume",
            transcript_path=transcript,
            project_dir=str(temp_nexus_root),
            session_id="malformed-session",
        )

        assert result is not None

    def test_missing_transcript(self, temp_nexus_root, create_project):
        """Handle missing transcript file gracefully."""
        create_project("31-no-transcript", session_id="no-transcript-session")

        result = determine_context_mode(
            source="compact",
            transcript_path="/nonexistent/transcript.jsonl",
            project_dir=str(temp_nexus_root),
            session_id="no-transcript-session",
        )

        # Should still work via session_id
        assert result["project_id"] == "31-no-transcript"
