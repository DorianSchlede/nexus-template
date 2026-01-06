#!/usr/bin/env python3
"""
Test update_resume_context.py helper script.

Validates that resume updates work correctly with backup/rollback.
"""

import sys
import subprocess
from pathlib import Path
import shutil

# Find project root and setup paths
project_root = Path(__file__).resolve().parents[3]
projects_dir = project_root / "02-projects"
script_path = project_root / "00-system" / "skills" / "projects" / "execute-project" / "scripts" / "update_resume_context.py"

def create_test_project():
    """Create test project directory structure."""
    test_project = projects_dir / "test-project"
    test_project.mkdir(exist_ok=True)
    planning_dir = test_project / "01-planning"
    planning_dir.mkdir(exist_ok=True)
    return test_project

def cleanup_test_project():
    """Remove test project."""
    test_project = projects_dir / "test-project"
    if test_project.exists():
        shutil.rmtree(test_project)

def test_update_task():
    """Test updating current_task field."""

    print("Test 1: Update current_task...")

    test_project = create_test_project()
    resume_file = test_project / "01-planning" / "resume-context.md"

    # Write initial resume
    initial_content = """---
resume_schema_version: "1.0"
last_updated: "2026-01-04T12:00:00Z"

# PROJECT
project_id: "test-project"
project_name: "Test Project"
current_phase: "execution"

# LOADING
next_action: "execute-project"
files_to_load:
  - "01-planning/overview.md"
  - "01-planning/plan.md"

# STATE
current_section: 1
current_task: 5
total_tasks: 20
tasks_completed: 4
---

*Auto-updated by execute-project skill on task/section completion*
"""

    resume_file.write_text(initial_content, encoding='utf-8')

    # Run update script
    result = subprocess.run(
        [sys.executable, str(script_path), "--project", "test-project", "--task", "6"],
        cwd=str(project_root),
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print(f"ERROR: Update script failed")
        print(f"stdout: {result.stdout}")
        print(f"stderr: {result.stderr}")
        cleanup_test_project()
        return False

    # Read updated resume
    updated_content = resume_file.read_text(encoding='utf-8')

    # Validate changes
    if "current_task: 6" not in updated_content:
        print("ERROR: current_task not updated")
        cleanup_test_project()
        return False

    if "current_task: 5" in updated_content:
        print("ERROR: old current_task still present")
        cleanup_test_project()
        return False

    # Verify backup created
    backup_file = resume_file.with_suffix('.md.backup')
    if not backup_file.exists():
        print("ERROR: Backup file not created")
        cleanup_test_project()
        return False

    # Verify backup has old value
    backup_content = backup_file.read_text(encoding='utf-8')
    if "current_task: 5" not in backup_content:
        print("ERROR: Backup doesn't contain old value")
        cleanup_test_project()
        return False

    print("  PASS: current_task updated from 5 to 6")
    print("  PASS: Backup created successfully")

    cleanup_test_project()
    return True

def test_update_section():
    """Test updating current_section (should reset current_task to 1)."""

    print("\nTest 2: Update current_section...")

    test_project = create_test_project()
    resume_file = test_project / "01-planning" / "resume-context.md"

    # Write initial resume
    initial_content = """---
resume_schema_version: "1.0"
last_updated: "2026-01-04T12:00:00Z"

# PROJECT
project_id: "test-project"
project_name: "Test Project"
current_phase: "execution"

# LOADING
next_action: "execute-project"
files_to_load:
  - "01-planning/overview.md"

# STATE
current_section: 1
current_task: 15
total_tasks: 20
tasks_completed: 14
---

*Auto-updated*
"""

    resume_file.write_text(initial_content, encoding='utf-8')

    # Run update script
    result = subprocess.run(
        [sys.executable, str(script_path), "--project", "test-project", "--section", "2"],
        cwd=str(project_root),
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print(f"ERROR: Update script failed")
        print(f"stdout: {result.stdout}")
        print(f"stderr: {result.stderr}")
        cleanup_test_project()
        return False

    # Read updated resume
    updated_content = resume_file.read_text(encoding='utf-8')

    # Validate changes
    if "current_section: 2" not in updated_content:
        print("ERROR: current_section not updated")
        cleanup_test_project()
        return False

    if "current_task: 1" not in updated_content:
        print("ERROR: current_task not reset to 1")
        cleanup_test_project()
        return False

    print("  PASS: current_section updated to 2")
    print("  PASS: current_task reset to 1")

    cleanup_test_project()
    return True

def test_update_multiple_fields():
    """Test updating multiple fields at once."""

    print("\nTest 3: Update multiple fields...")

    test_project = create_test_project()
    resume_file = test_project / "01-planning" / "resume-context.md"

    # Write initial resume
    initial_content = """---
resume_schema_version: "1.0"
last_updated: "2026-01-04T12:00:00Z"

# PROJECT
project_id: "test-project"
project_name: "Test Project"
current_phase: "execution"

# LOADING
next_action: "execute-project"
files_to_load:
  - "01-planning/overview.md"

# STATE
current_section: 1
current_task: 5
total_tasks: 20
tasks_completed: 4
---

*Auto-updated*
"""

    resume_file.write_text(initial_content, encoding='utf-8')

    # Run update script with multiple fields
    result = subprocess.run(
        [sys.executable, str(script_path),
         "--project", "test-project",
         "--task", "6",
         "--completed", "5"],
        cwd=str(project_root),
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print(f"ERROR: Update script failed")
        print(f"stdout: {result.stdout}")
        print(f"stderr: {result.stderr}")
        cleanup_test_project()
        return False

    # Read updated resume
    updated_content = resume_file.read_text(encoding='utf-8')

    # Validate changes
    if "current_task: 6" not in updated_content:
        print("ERROR: current_task not updated")
        cleanup_test_project()
        return False

    if "tasks_completed: 5" not in updated_content:
        print("ERROR: tasks_completed not updated")
        cleanup_test_project()
        return False

    print("  PASS: current_task updated to 6")
    print("  PASS: tasks_completed updated to 5")

    cleanup_test_project()
    return True

def test_timestamp_update():
    """Test that timestamp is always updated."""

    print("\nTest 4: Timestamp auto-update...")

    test_project = create_test_project()
    resume_file = test_project / "01-planning" / "resume-context.md"

    # Write initial resume with old timestamp
    initial_content = """---
resume_schema_version: "1.0"
last_updated: "2020-01-01T00:00:00Z"

# PROJECT
project_id: "test-project"
project_name: "Test Project"
current_phase: "execution"

# LOADING
next_action: "execute-project"
files_to_load:
  - "01-planning/overview.md"

# STATE
current_section: 1
current_task: 5
total_tasks: 20
tasks_completed: 4
---

*Auto-updated*
"""

    resume_file.write_text(initial_content, encoding='utf-8')

    # Run update script
    result = subprocess.run(
        [sys.executable, str(script_path), "--project", "test-project", "--task", "6"],
        cwd=str(project_root),
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print(f"ERROR: Update script failed")
        print(f"stdout: {result.stdout}")
        print(f"stderr: {result.stderr}")
        cleanup_test_project()
        return False

    # Read updated resume
    updated_content = resume_file.read_text(encoding='utf-8')

    # Validate timestamp changed
    if "2020-01-01T00:00:00Z" in updated_content:
        print("ERROR: Timestamp not updated")
        cleanup_test_project()
        return False

    if "2026-01-04" not in updated_content:
        print("ERROR: Timestamp not current")
        cleanup_test_project()
        return False

    print("  PASS: Timestamp auto-updated to current time")

    cleanup_test_project()
    return True

if __name__ == "__main__":
    print("Testing update_resume_context.py Helper Script")
    print("=" * 50)

    test1 = test_update_task()
    test2 = test_update_section()
    test3 = test_update_multiple_fields()
    test4 = test_timestamp_update()

    print("\n" + "=" * 50)
    if test1 and test2 and test3 and test4:
        print("ALL TESTS PASSED!")
        sys.exit(0)
    else:
        print("TESTS FAILED")
        sys.exit(1)
