"""
Tests for save_resume_state.py - PreCompact hook.
"""

import json
import os
import re
import pytest
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

from save_resume_state import (
    find_nexus_root,
    cleanup_session_cache,
    update_project_resume_context,
)


class TestFindNexusRoot:
    """Tests for find_nexus_root()"""

    def test_uses_env_variable(self, tmp_path):
        with patch.dict(os.environ, {"CLAUDE_PROJECT_DIR": str(tmp_path)}):
            result = find_nexus_root()
            assert result == tmp_path

    def test_fallback_to_cwd(self):
        with patch.dict(os.environ, {}, clear=True):
            os.environ.pop("CLAUDE_PROJECT_DIR", None)
            result = find_nexus_root()
            assert result == Path.cwd()


class TestCleanupSessionCache:
    """Tests for cleanup_session_cache()"""

    def test_deletes_existing_cache(self, tmp_path):
        cache_dir = tmp_path / "00-system" / ".cache"
        cache_dir.mkdir(parents=True)

        # Create cache file with session hash
        import hashlib
        session_id = "test-session-123"
        session_hash = hashlib.md5(session_id.encode()).hexdigest()[:8]
        cache_file = cache_dir / f"context_startup_{session_hash}.json"
        cache_file.write_text('{"test": "data"}')

        result = cleanup_session_cache(tmp_path, session_id)

        assert result is True
        assert not cache_file.exists()

    def test_returns_false_if_no_cache(self, tmp_path):
        result = cleanup_session_cache(tmp_path, "nonexistent-session")
        assert result is False

    def test_handles_unknown_session(self, tmp_path):
        result = cleanup_session_cache(tmp_path, "unknown")
        assert result is False

    def test_handles_empty_session(self, tmp_path):
        result = cleanup_session_cache(tmp_path, "")
        assert result is False


class TestUpdateProjectResumeContext:
    """Tests for update_project_resume_context()"""

    def test_updates_session_id(self, temp_nexus_root, create_project):
        create_project("01-test", session_id="old-session")

        result = update_project_resume_context(
            temp_nexus_root, "01-test", "new-session-id"
        )

        assert result is True

        resume_file = temp_nexus_root / "02-projects" / "01-test" / "01-planning" / "resume-context.md"
        content = resume_file.read_text()

        # Multi-session enhancement: check session_ids list contains new ID
        assert '"new-session-id"' in content
        assert 'session_ids:' in content

        # Legacy session_id field should exist for backward compat
        assert 'session_id:' in content

    def test_updates_last_updated(self, temp_nexus_root, create_project):
        create_project("02-test", last_updated="2020-01-01T00:00:00Z")

        before = datetime.now(timezone.utc)
        result = update_project_resume_context(temp_nexus_root, "02-test", "session")
        after = datetime.now(timezone.utc)

        assert result is True

        resume_file = temp_nexus_root / "02-projects" / "02-test" / "01-planning" / "resume-context.md"
        content = resume_file.read_text()

        # Extract timestamp
        match = re.search(r'last_updated:\s*"([^"]+)"', content)
        assert match is not None

        timestamp = datetime.fromisoformat(match.group(1).replace("Z", "+00:00"))
        assert before <= timestamp <= after

    def test_creates_session_id_if_missing(self, temp_nexus_root):
        # Create project without session_id
        project_path = temp_nexus_root / "02-projects" / "03-no-sid" / "01-planning"
        project_path.mkdir(parents=True)
        (project_path / "resume-context.md").write_text(
            '---\nfiles_to_load: []\n---\n# Resume'
        )

        result = update_project_resume_context(temp_nexus_root, "03-no-sid", "added-session")

        assert result is True
        content = (project_path / "resume-context.md").read_text()
        assert 'session_id: "added-session"' in content

    def test_returns_false_for_missing_file(self, temp_nexus_root):
        result = update_project_resume_context(
            temp_nexus_root, "nonexistent-project", "session"
        )
        assert result is False

    def test_preserves_other_content(self, temp_nexus_root, create_project):
        create_project("04-preserve")

        # Read original content
        resume_file = temp_nexus_root / "02-projects" / "04-preserve" / "01-planning" / "resume-context.md"
        original = resume_file.read_text()
        assert "files_to_load" in original

        # Update
        update_project_resume_context(temp_nexus_root, "04-preserve", "new-session")

        # Verify preserved
        updated = resume_file.read_text()
        assert "files_to_load" in updated
        assert "# Resume Context" in updated


class TestIntegrationFlow:
    """Integration tests for PreCompact hook flow."""

    def test_full_precompact_flow(self, temp_nexus_root, create_project, create_transcript, mock_tool_use_entry):
        """Test the full PreCompact flow: detect project → update resume → cleanup cache"""
        project_id = "05-integration"
        session_id = "integration-session-uuid"

        # Create project with different session_id (simulating first compact)
        create_project(project_id, session_id="previous-session")

        # Create transcript with project activity
        entries = [
            mock_tool_use_entry("Read", f"02-projects/{project_id}/01-planning/overview.md"),
            mock_tool_use_entry("Write", f"02-projects/{project_id}/03-working/draft.md"),
        ]
        transcript = create_transcript(entries)

        # Simulate PreCompact updating resume context
        result = update_project_resume_context(temp_nexus_root, project_id, session_id)
        assert result is True

        # Verify session_id added to session_ids list (multi-session)
        resume_file = temp_nexus_root / "02-projects" / project_id / "01-planning" / "resume-context.md"
        content = resume_file.read_text()

        # Check multi-session tracking
        assert f'"{session_id}"' in content  # In session_ids list
        assert 'session_ids:' in content  # List exists
        assert '"previous-session"' in content  # Old session still tracked
