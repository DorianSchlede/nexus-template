"""
Shared fixtures for handover test suite.
"""

import json
import os
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional
from unittest.mock import MagicMock, patch

import pytest

# Add hooks directory to path
HOOKS_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(HOOKS_DIR))


@pytest.fixture
def temp_nexus_root(tmp_path):
    """Create a minimal Nexus-like directory structure."""
    # Create core directories
    (tmp_path / "00-system" / "core").mkdir(parents=True)
    (tmp_path / "00-system" / ".cache").mkdir(parents=True)
    (tmp_path / "00-system" / "skills" / "projects" / "plan-project").mkdir(parents=True)
    (tmp_path / "00-system" / "skills" / "projects" / "execute-project").mkdir(parents=True)
    (tmp_path / "01-memory").mkdir(parents=True)
    (tmp_path / "02-projects").mkdir(parents=True)
    (tmp_path / "03-skills").mkdir(parents=True)
    (tmp_path / "04-workspace").mkdir(parents=True)

    # Create minimal orchestrator.md
    (tmp_path / "00-system" / "core" / "orchestrator.md").write_text("# Nexus Orchestrator\nTest stub.")

    # Create minimal goals.md
    (tmp_path / "01-memory" / "goals.md").write_text("# Goals\nTest user goals.")

    # Create skill stubs
    (tmp_path / "00-system" / "skills" / "projects" / "plan-project" / "SKILL.md").write_text(
        "---\nname: plan-project\n---\n# Plan Project"
    )
    (tmp_path / "00-system" / "skills" / "projects" / "execute-project" / "SKILL.md").write_text(
        "---\nname: execute-project\n---\n# Execute Project"
    )

    return tmp_path


@pytest.fixture
def create_project(temp_nexus_root):
    """Factory fixture to create mock projects."""

    def _create_project(
        project_id: str,
        status: str = "IN_PROGRESS",
        phase1_complete: bool = False,
        session_id: Optional[str] = None,
        last_updated: Optional[str] = None,
    ):
        project_path = temp_nexus_root / "02-projects" / project_id / "01-planning"
        project_path.mkdir(parents=True, exist_ok=True)

        # Create 01-overview.md
        overview = f"""---
id: {project_id}
name: {project_id}
status: {status}
---
# {project_id}
Test project.
"""
        (project_path / "01-overview.md").write_text(overview)

        # Create 04-steps.md with optional phase 1 completion
        if phase1_complete:
            steps = """# Steps

## Phase 1: Setup
- [x] Task 1
- [x] Task 2

## Phase 2: Implementation
- [ ] Task 3
"""
        else:
            steps = """# Steps

## Phase 1: Setup
- [x] Task 1
- [ ] Task 2

## Phase 2: Implementation
- [ ] Task 3
"""
        (project_path / "04-steps.md").write_text(steps)

        # Create resume-context.md
        ts = last_updated or datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        sid = session_id or ""
        resume = f"""---
session_id: "{sid}"
last_updated: "{ts}"
files_to_load:
  - 01-planning/01-overview.md
  - 01-planning/04-steps.md
---
# Resume Context
"""
        (project_path / "resume-context.md").write_text(resume)

        return project_path.parent

    return _create_project


@pytest.fixture
def create_transcript(tmp_path):
    """Factory fixture to create mock transcript JSONL files."""

    def _create_transcript(entries: list[dict], filename: str = "transcript.jsonl"):
        transcript_path = tmp_path / filename
        with open(transcript_path, "w", encoding="utf-8") as f:
            for entry in entries:
                f.write(json.dumps(entry) + "\n")
        return str(transcript_path)

    return _create_transcript


@pytest.fixture
def mock_tool_use_entry():
    """Factory to create tool_use transcript entries."""

    def _create(tool_name: str, file_path: str):
        return {
            "message": {
                "role": "assistant",
                "content": [
                    {
                        "type": "tool_use",
                        "name": tool_name,
                        "input": {"file_path": file_path},
                    }
                ],
            }
        }

    return _create


@pytest.fixture
def mock_nexus_imports():
    """Mock nexus.loaders and related imports to avoid dependency on nexus core."""
    mock_loaders = MagicMock()
    mock_loaders.scan_projects.return_value = []
    mock_loaders.build_skills_xml.return_value = "<skills/>"
    mock_loaders.load_full_startup_context.return_value = {}

    mock_state = MagicMock()
    mock_state.check_goals_personalized.return_value = True
    mock_state.check_workspace_configured.return_value = True
    mock_state.build_pending_onboarding.return_value = []
    mock_state.extract_learning_completed.return_value = {}

    with patch.dict(
        sys.modules,
        {
            "nexus": MagicMock(),
            "nexus.loaders": mock_loaders,
            "nexus.state": mock_state,
        },
    ):
        yield {"loaders": mock_loaders, "state": mock_state}
