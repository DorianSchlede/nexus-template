"""
Tests for project_state.py - Enhanced metadata detection utility.

Tests state detection from:
- overview.md YAML frontmatter
- resume-context.md YAML frontmatter
- steps.md checkbox tracking
"""

import pytest
from pathlib import Path
from utils.project_state import (
    extract_yaml_frontmatter,
    get_project_status_from_overview,
    get_project_metadata_from_resume,
    count_tasks_in_steps,
    detect_project_state,
    find_most_recent_project_enhanced,
    detect_phase_from_metadata,
    ProjectState
)


class TestExtractYAMLFrontmatter:
    """Test YAML frontmatter parsing."""

    def test_simple_fields(self, tmp_path):
        """Extract simple key: value fields."""
        md_file = tmp_path / "test.md"
        md_file.write_text("""---
status: IN_PROGRESS
name: Test Project
created: 2026-01-05
---

# Content
""")
        metadata = extract_yaml_frontmatter(md_file)
        assert metadata['status'] == "IN_PROGRESS"
        assert metadata['name'] == "Test Project"
        assert metadata['created'] == "2026-01-05"

    def test_quoted_values(self, tmp_path):
        """Handle quoted values."""
        md_file = tmp_path / "test.md"
        md_file.write_text("""---
description: "Full test suite for handover"
session_id: "aaa111"
---
""")
        metadata = extract_yaml_frontmatter(md_file)
        assert metadata['description'] == "Full test suite for handover"
        assert metadata['session_id'] == "aaa111"

    def test_session_ids_list_multiline(self, tmp_path):
        """Parse multiline session_ids list."""
        md_file = tmp_path / "test.md"
        md_file.write_text("""---
session_ids:
  - "aaa111"
  - "bbb222"
  - "ccc333"
---
""")
        metadata = extract_yaml_frontmatter(md_file)
        assert 'session_ids' in metadata
        assert metadata['session_ids'] == ["aaa111", "bbb222", "ccc333"]

    def test_session_ids_list_inline(self, tmp_path):
        """Parse inline session_ids list."""
        md_file = tmp_path / "test.md"
        md_file.write_text("""---
session_ids: ["aaa111", "bbb222"]
---
""")
        metadata = extract_yaml_frontmatter(md_file)
        assert metadata['session_ids'] == ["aaa111", "bbb222"]

    def test_no_frontmatter(self, tmp_path):
        """Handle files without frontmatter."""
        md_file = tmp_path / "test.md"
        md_file.write_text("# Just content\nNo YAML here")
        metadata = extract_yaml_frontmatter(md_file)
        assert metadata == {}

    def test_missing_file(self, tmp_path):
        """Handle missing files gracefully."""
        metadata = extract_yaml_frontmatter(tmp_path / "missing.md")
        assert metadata == {}

    def test_comments_and_blank_lines(self, tmp_path):
        """Skip comments and blank lines."""
        md_file = tmp_path / "test.md"
        md_file.write_text("""---
# This is a comment
status: IN_PROGRESS

# Another comment
name: Test
---
""")
        metadata = extract_yaml_frontmatter(md_file)
        assert metadata['status'] == "IN_PROGRESS"
        assert metadata['name'] == "Test"
        assert '#' not in metadata  # No comment keys


class TestGetProjectStatus:
    """Test status extraction from overview.md."""

    def test_status_from_overview(self, create_project):
        """Extract status field from overview.md."""
        project_path = create_project("10-test")
        overview = project_path / "01-planning" / "01-overview.md"
        overview.write_text("""---
id: 10-test
status: IN_PROGRESS
name: Test Project
---

# Test
""")
        status = get_project_status_from_overview(project_path)
        assert status == "IN_PROGRESS"

    def test_status_complete(self, create_project):
        """Detect COMPLETE status."""
        project_path = create_project("11-done")
        overview = project_path / "01-planning" / "01-overview.md"
        overview.write_text("""---
status: COMPLETE
---
""")
        status = get_project_status_from_overview(project_path)
        assert status == "COMPLETE"

    def test_missing_overview(self, create_project):
        """Handle missing overview.md."""
        project_path = create_project("12-no-overview")
        (project_path / "01-planning" / "01-overview.md").unlink()
        status = get_project_status_from_overview(project_path)
        assert status is None


class TestGetProjectMetadata:
    """Test metadata extraction from resume-context.md."""

    def test_full_metadata(self, create_project):
        """Extract all resume-context fields."""
        project_path = create_project("13-resume")
        resume = project_path / "01-planning" / "resume-context.md"
        resume.write_text("""---
session_id: "aaa111"
last_updated: "2026-01-06T01:13:09.213621"
current_phase: execution
next_action: execute-project
current_section: 7
tasks_completed: 52
total_tasks: 58
---
""")
        metadata = get_project_metadata_from_resume(project_path)
        assert metadata['session_id'] == "aaa111"
        assert metadata['current_phase'] == "execution"
        assert metadata['next_action'] == "execute-project"
        assert metadata['current_section'] == "7"
        assert metadata['tasks_completed'] == "52"

    def test_session_ids_list(self, create_project):
        """Extract session_ids list from resume-context."""
        project_path = create_project("14-multi-session")
        resume = project_path / "01-planning" / "resume-context.md"
        resume.write_text("""---
session_ids:
  - "aaa111"
  - "bbb222"
  - "ccc333"
current_phase: execution
---
""")
        metadata = get_project_metadata_from_resume(project_path)
        assert 'session_ids' in metadata
        assert len(metadata['session_ids']) == 3
        assert "aaa111" in metadata['session_ids']


class TestCountTasks:
    """Test task counting from steps.md."""

    def test_count_mixed_checkboxes(self, create_project):
        """Count completed and total tasks."""
        project_path = create_project("15-tasks")
        steps = project_path / "01-planning" / "04-steps.md"
        steps.write_text("""# Steps

## Phase 1
- [x] Task 1
- [x] Task 2
- [ ] Task 3

## Phase 2
- [x] Task 4
- [ ] Task 5
- [ ] Task 6
""")
        completed, total = count_tasks_in_steps(project_path)
        assert completed == 3
        assert total == 6

    def test_all_completed(self, create_project):
        """All tasks completed."""
        project_path = create_project("16-done")
        steps = project_path / "01-planning" / "04-steps.md"
        steps.write_text("""
- [x] Task 1
- [x] Task 2
- [x] Task 3
""")
        completed, total = count_tasks_in_steps(project_path)
        assert completed == 3
        assert total == 3

    def test_no_tasks(self, create_project):
        """No tasks in steps.md."""
        project_path = create_project("17-no-tasks")
        steps = project_path / "01-planning" / "04-steps.md"
        steps.write_text("# Just headers\n\nNo checkboxes")
        completed, total = count_tasks_in_steps(project_path)
        assert completed == 0
        assert total == 0

    def test_missing_steps_file(self, create_project):
        """Handle missing steps.md."""
        project_path = create_project("18-no-steps")
        (project_path / "01-planning" / "04-steps.md").unlink()
        completed, total = count_tasks_in_steps(project_path)
        assert completed == 0
        assert total == 0

    def test_case_insensitive(self, create_project):
        """Count [X] and [x] both as completed."""
        project_path = create_project("19-case")
        steps = project_path / "01-planning" / "04-steps.md"
        steps.write_text("""
- [x] lowercase
- [X] uppercase
- [ ] pending
""")
        completed, total = count_tasks_in_steps(project_path)
        assert completed == 2
        assert total == 3


class TestDetectProjectState:
    """Test complete state detection."""

    def test_full_state_detection(self, create_project):
        """Detect complete project state from all sources."""
        project_path = create_project("20-full-state")

        # Create overview.md
        overview = project_path / "01-planning" / "01-overview.md"
        overview.write_text("""---
id: 20-full-state
name: Full State
status: IN_PROGRESS
created: 2026-01-05
---
""")

        # Create resume-context.md
        resume = project_path / "01-planning" / "resume-context.md"
        resume.write_text("""---
session_ids:
  - "aaa111"
  - "bbb222"
current_phase: execution
next_action: execute-project
current_section: 3
tasks_completed: 15
total_tasks: 30
last_updated: "2026-01-06T12:00:00"
---
""")

        # Create steps.md
        steps = project_path / "01-planning" / "04-steps.md"
        steps.write_text("""
- [x] Task 1
- [x] Task 2
- [ ] Task 3
""")

        state = detect_project_state(project_path)

        assert state is not None
        assert state.project_id == "20"
        assert state.name == "Full State"
        assert state.status == "IN_PROGRESS"
        assert state.current_phase == "execution"
        assert state.next_action == "execute-project"
        assert state.current_section == 3
        assert state.tasks_completed == 15  # From resume (authoritative)
        assert state.tasks_total == 30
        assert state.progress_percent == 50.0
        assert state.last_updated == "2026-01-06T12:00:00"
        assert state.created == "2026-01-05"
        assert len(state.session_ids) == 2
        assert "aaa111" in state.session_ids

    def test_minimal_project(self, create_project):
        """Detect state from minimal project (only folder structure)."""
        project_path = create_project("21-minimal")

        # Remove default files to test minimal state
        resume = project_path / "01-planning" / "resume-context.md"
        if resume.exists():
            resume.unlink()
        steps = project_path / "01-planning" / "04-steps.md"
        if steps.exists():
            steps.unlink()

        # Only basic overview
        overview = project_path / "01-planning" / "01-overview.md"
        overview.write_text("""---
id: 21-minimal
name: Minimal
---
""")

        state = detect_project_state(project_path)

        assert state is not None
        assert state.project_id == "21"
        assert state.status == "IN_PROGRESS"  # Default
        assert state.current_phase == "planning"  # Default
        assert state.tasks_completed == 0
        assert state.tasks_total == 0

    def test_legacy_session_id_migration(self, create_project):
        """Migrate legacy session_id to session_ids list."""
        project_path = create_project("22-legacy")
        resume = project_path / "01-planning" / "resume-context.md"
        resume.write_text("""---
session_id: "legacy-aaa111"
current_phase: execution
---
""")

        state = detect_project_state(project_path)

        assert state is not None
        assert "legacy-aaa111" in state.session_ids
        assert len(state.session_ids) == 1

    def test_invalid_project_structure(self, tmp_path):
        """Handle invalid project structure gracefully."""
        invalid_project = tmp_path / "99-invalid"
        invalid_project.mkdir()
        # No 01-planning/ folder

        state = detect_project_state(invalid_project)
        assert state is None

    def test_progress_calculation(self, create_project):
        """Calculate progress percentage correctly."""
        project_path = create_project("23-progress")
        resume = project_path / "01-planning" / "resume-context.md"
        resume.write_text("""---
tasks_completed: 7
total_tasks: 10
---
""")

        state = detect_project_state(project_path)

        assert state.progress_percent == 70.0

    def test_zero_tasks_progress(self, create_project):
        """Handle zero total tasks without division error."""
        project_path = create_project("24-zero")
        resume = project_path / "01-planning" / "resume-context.md"
        resume.write_text("""---
tasks_completed: 0
total_tasks: 0
---
""")

        state = detect_project_state(project_path)

        assert state.progress_percent == 0.0


class TestFindMostRecentProject:
    """Test enhanced most-recent project detection."""

    def test_find_most_recent(self, temp_nexus_root):
        """Find project with most recent timestamp."""
        projects_dir = temp_nexus_root / "02-projects"

        # Create 3 projects with different timestamps
        p1 = projects_dir / "10-old"
        p1.mkdir()
        (p1 / "01-planning").mkdir()
        (p1 / "01-planning" / "01-overview.md").write_text("---\nstatus: IN_PROGRESS\n---")
        (p1 / "01-planning" / "resume-context.md").write_text(
            '---\nlast_updated: "2026-01-01T10:00:00"\n---'
        )

        p2 = projects_dir / "11-recent"
        p2.mkdir()
        (p2 / "01-planning").mkdir()
        (p2 / "01-planning" / "01-overview.md").write_text("---\nstatus: IN_PROGRESS\n---")
        (p2 / "01-planning" / "resume-context.md").write_text(
            '---\nlast_updated: "2026-01-06T15:00:00"\n---'
        )

        p3 = projects_dir / "12-middle"
        p3.mkdir()
        (p3 / "01-planning").mkdir()
        (p3 / "01-planning" / "01-overview.md").write_text("---\nstatus: IN_PROGRESS\n---")
        (p3 / "01-planning" / "resume-context.md").write_text(
            '---\nlast_updated: "2026-01-03T12:00:00"\n---'
        )

        most_recent = find_most_recent_project_enhanced(projects_dir)

        assert most_recent is not None
        assert most_recent.project_id == "11"

    def test_exclude_complete_projects(self, temp_nexus_root):
        """Skip COMPLETE projects by default."""
        projects_dir = temp_nexus_root / "02-projects"

        # Complete project (most recent)
        p1 = projects_dir / "10-done"
        p1.mkdir()
        (p1 / "01-planning").mkdir()
        (p1 / "01-planning" / "01-overview.md").write_text("---\nstatus: COMPLETE\n---")
        (p1 / "01-planning" / "resume-context.md").write_text(
            '---\nlast_updated: "2026-01-06T15:00:00"\n---'
        )

        # In-progress project (older)
        p2 = projects_dir / "11-active"
        p2.mkdir()
        (p2 / "01-planning").mkdir()
        (p2 / "01-planning" / "01-overview.md").write_text("---\nstatus: IN_PROGRESS\n---")
        (p2 / "01-planning" / "resume-context.md").write_text(
            '---\nlast_updated: "2026-01-05T10:00:00"\n---'
        )

        most_recent = find_most_recent_project_enhanced(projects_dir, exclude_complete=True)

        assert most_recent is not None
        assert most_recent.project_id == "11"  # Skipped COMPLETE project

    def test_include_complete_projects(self, temp_nexus_root):
        """Include COMPLETE projects when explicitly requested."""
        projects_dir = temp_nexus_root / "02-projects"

        p1 = projects_dir / "10-done"
        p1.mkdir()
        (p1 / "01-planning").mkdir()
        (p1 / "01-planning" / "01-overview.md").write_text("---\nstatus: COMPLETE\n---")
        (p1 / "01-planning" / "resume-context.md").write_text(
            '---\nlast_updated: "2026-01-06T15:00:00"\n---'
        )

        most_recent = find_most_recent_project_enhanced(projects_dir, exclude_complete=False)

        assert most_recent is not None
        assert most_recent.project_id == "10"

    def test_exclude_archived_projects(self, temp_nexus_root):
        """Skip archived projects (starting with underscore)."""
        projects_dir = temp_nexus_root / "02-projects"

        # Archived project (most recent)
        p1 = projects_dir / "_10-archived"
        p1.mkdir()
        (p1 / "01-planning").mkdir()
        (p1 / "01-planning" / "01-overview.md").write_text("---\nstatus: IN_PROGRESS\n---")
        (p1 / "01-planning" / "resume-context.md").write_text(
            '---\nlast_updated: "2026-01-06T15:00:00"\n---'
        )

        # Active project (older)
        p2 = projects_dir / "11-active"
        p2.mkdir()
        (p2 / "01-planning").mkdir()
        (p2 / "01-planning" / "01-overview.md").write_text("---\nstatus: IN_PROGRESS\n---")
        (p2 / "01-planning" / "resume-context.md").write_text(
            '---\nlast_updated: "2026-01-05T10:00:00"\n---'
        )

        most_recent = find_most_recent_project_enhanced(projects_dir)

        assert most_recent is not None
        assert most_recent.project_id == "11"

    def test_no_projects_found(self, temp_nexus_root):
        """Return None when no projects found."""
        projects_dir = temp_nexus_root / "02-projects"

        most_recent = find_most_recent_project_enhanced(projects_dir)

        assert most_recent is None


class TestDetectPhase:
    """Test phase detection from metadata."""

    def test_explicit_phase_from_resume(self, create_project):
        """Use explicit phase from resume-context.md."""
        project_path = create_project("25-explicit")
        resume = project_path / "01-planning" / "resume-context.md"
        resume.write_text("""---
current_phase: execution
next_action: execute-project
---
""")

        phase, skill = detect_phase_from_metadata(project_path)

        assert phase == "execution"
        assert skill == "execute-project"

    def test_fallback_to_checkbox_planning(self, create_project):
        """Fallback to checkbox logic when resume missing - planning phase."""
        project_path = create_project("26-checkbox-plan")
        # No resume-context.md

        steps = project_path / "01-planning" / "04-steps.md"
        steps.write_text("""# Steps

## Phase 1: Foundation
- [x] Task 1
- [ ] Task 2  # Incomplete
- [ ] Task 3

## Phase 2: Implementation
- [ ] Task 4
""")

        phase, skill = detect_phase_from_metadata(project_path)

        assert phase == "planning"
        assert skill == "plan-project"

    def test_fallback_to_checkbox_execution(self, create_project):
        """Fallback to checkbox logic - execution phase."""
        project_path = create_project("27-checkbox-exec")

        steps = project_path / "01-planning" / "04-steps.md"
        steps.write_text("""# Steps

## Phase 1: Foundation
- [x] Task 1
- [x] Task 2  # All complete
- [x] Task 3

## Phase 2: Implementation
- [ ] Task 4
""")

        phase, skill = detect_phase_from_metadata(project_path)

        assert phase == "execution"
        assert skill == "execute-project"

    def test_no_steps_defaults_to_planning(self, create_project):
        """Default to planning when no steps.md."""
        project_path = create_project("28-no-steps")
        (project_path / "01-planning" / "04-steps.md").unlink()

        phase, skill = detect_phase_from_metadata(project_path)

        assert phase == "planning"
        assert skill == "plan-project"

    def test_no_phase1_defaults_to_planning(self, create_project):
        """Default to planning when no Phase 1 section."""
        project_path = create_project("29-no-phase1")
        steps = project_path / "01-planning" / "04-steps.md"
        steps.write_text("""# Steps

## Some Other Section
- [x] Task 1
""")

        phase, skill = detect_phase_from_metadata(project_path)

        assert phase == "planning"
        assert skill == "plan-project"
