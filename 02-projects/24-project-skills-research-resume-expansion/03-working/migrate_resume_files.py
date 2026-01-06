"""
Migration Script: _resume.md -> resume-context.md

Purpose: Migrate existing _resume.md files to new resume-context.md schema
Version: 1.0
Created: 2026-01-04
Phase: 0.6

This script:
1. Renames _resume.md -> resume-context.md
2. Updates schema field names (resume_version -> resume_schema_version)
3. Adds project_name field (extracted from overview.md)
4. Adds validation gate content if missing
5. Creates backup files (_resume.md.backup)

Usage:
    python migrate_resume_files.py [--dry-run] [--project PROJECT_ID]

    --dry-run: Show what would be changed without modifying files
    --project: Migrate only specific project (default: all projects)
"""

import os
import sys
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, Any, Optional, Tuple
import argparse

# Add project root to path for frontmatter import
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

try:
    import frontmatter
except ImportError:
    print("ERROR: 'frontmatter' library not found. Install with: pip install python-frontmatter")
    sys.exit(1)


def get_project_name(project_path: Path) -> str:
    """
    Extract project name from overview.md with fallback.

    Args:
        project_path: Path to project directory

    Returns:
        Project name (from overview.md or derived from ID)
    """
    overview_path = project_path / "01-planning" / "overview.md"

    try:
        if overview_path.exists():
            post = frontmatter.load(overview_path)
            name = post.metadata.get("name")
            if name:
                return name
    except Exception as e:
        print(f"  ⚠️  Warning: Could not read overview.md: {e}")

    # Fallback: convert project ID to title case
    project_id = project_path.name
    return project_id.replace("-", " ").title()


def migrate_project_resume(project_path: Path, dry_run: bool = False) -> Tuple[str, str]:
    """
    Migrate _resume.md -> resume-context.md with schema updates.

    Checks both root directory and 01-planning/ for _resume.md.
    If found in root, moves to 01-planning/ during migration.

    Args:
        project_path: Path to project directory
        dry_run: If True, don't modify files (just report)

    Returns:
        Tuple of (status, message)
    """
    # Check both possible locations for _resume.md
    old_file_planning = project_path / "01-planning" / "_resume.md"
    old_file_root = project_path / "_resume.md"
    new_file = project_path / "01-planning" / "resume-context.md"

    # Determine which location has the file
    if old_file_planning.exists():
        old_file = old_file_planning
        backup_file = project_path / "01-planning" / "_resume.md.backup"
        location = "01-planning/"
    elif old_file_root.exists():
        old_file = old_file_root
        backup_file = project_path / "_resume.md.backup"
        location = "root"
    else:
        return ("SKIP", "No _resume.md found")

    # Skip if new file already exists
    if new_file.exists():
        return ("SKIP", "resume-context.md already exists")

    # Read old YAML frontmatter
    try:
        post = frontmatter.load(old_file)
        old_metadata = post.metadata
        old_body = post.content
    except Exception as e:
        return ("ERROR", f"Failed to parse {old_file.name}: {e}")

    # Transform schema
    new_metadata = {
        "resume_schema_version": "1.0",  # NEW field (was resume_version)
        "last_updated": old_metadata.get("last_updated", old_metadata.get("updated",
                                        datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"))),
        "project_id": old_metadata.get("project_id"),
        "project_name": get_project_name(project_path),  # NEW field from overview.md
        "current_phase": old_metadata.get("current_phase", old_metadata.get("phase", "execution")),
        "next_action": old_metadata.get("next_action", old_metadata.get("last_skill", "execute-project")),
        "files_to_load": old_metadata.get("files_to_load", [
            "01-planning/overview.md",
            "01-planning/plan.md",
            "01-planning/steps.md"
        ]),
        "current_section": old_metadata.get("current_section", 1),
        "current_task": old_metadata.get("current_task", 1),
        "progress": old_metadata.get("progress", "In progress")
    }

    # Add validation gate if missing
    validation_gate = """# Validation Gate

Before continuing, you MUST verify you understand:

1. **Project Purpose** (from [overview.md](overview.md)):
   - What problem are we solving?
   - What is the success criterion?

2. **Current Location** (from [steps.md](steps.md)):
   - What phase are we in?
   - What is the next task?

3. **Approach** (from [plan.md](plan.md)):
   - What is the implementation strategy?

**If you cannot answer these questions, STOP and re-read files_to_load.**

---

*This file is auto-updated on every task completion by execute-project skill.*
"""

    if "Validation Gate" not in old_body:
        # APPEND validation gate to preserve existing content
        new_body = old_body.strip() + "\n\n" + validation_gate if old_body.strip() else validation_gate
    else:
        new_body = old_body

    # Dry run - just report
    if dry_run:
        changes = []
        if "resume_version" in old_metadata:
            changes.append(f"resume_version -> resume_schema_version: '1.0'")
        if "project_name" not in old_metadata:
            changes.append(f"Add project_name: '{new_metadata['project_name']}'")
        if "Validation Gate" not in old_body:
            changes.append("Add validation gate content")

        return ("DRY-RUN", f"Would migrate: {', '.join(changes)}")

    # Write new file
    new_post = frontmatter.Post(new_body, **new_metadata)

    try:
        # frontmatter.dumps() returns string, frontmatter.dump() writes directly
        content = frontmatter.dumps(new_post)
        with open(new_file, 'w', encoding='utf-8') as f:
            f.write(content)
    except Exception as e:
        return ("ERROR", f"Failed to write {new_file.name}: {e}")

    # Create backup
    try:
        if backup_file.exists():
            backup_file.unlink()  # Remove old backup
        old_file.rename(backup_file)
    except Exception as e:
        return ("ERROR", f"Failed to create backup: {e}")

    return ("SUCCESS", f"Migrated from {location} -> 01-planning/resume-context.md (backup created)")


def find_projects(base_path: Path) -> list[Path]:
    """
    Find all project directories in 02-projects/.

    Args:
        base_path: Root path (strategy-nexus)

    Returns:
        List of project directory paths
    """
    projects_dir = base_path / "02-projects"

    if not projects_dir.exists():
        print(f"ERROR: Projects directory not found: {projects_dir}")
        return []

    # Find all directories matching NN-* pattern
    projects = []
    for item in projects_dir.iterdir():
        if item.is_dir() and "-" in item.name:
            # Check if starts with digits
            parts = item.name.split("-", 1)
            if len(parts) >= 2 and parts[0].isdigit() and len(parts[0]) == 2:
                projects.append(item)

    return sorted(projects)


def rollback_migration(project_path: Path) -> Tuple[str, str]:
    """
    Rollback migration by restoring from backup.

    Checks both possible backup locations (root and 01-planning/).

    Args:
        project_path: Path to project directory

    Returns:
        Tuple of (status, message)
    """
    new_file = project_path / "01-planning" / "resume-context.md"
    backup_file_planning = project_path / "01-planning" / "_resume.md.backup"
    backup_file_root = project_path / "_resume.md.backup"

    # Determine which backup exists
    if backup_file_planning.exists():
        backup_file = backup_file_planning
        old_file = project_path / "01-planning" / "_resume.md"
        location = "01-planning/"
    elif backup_file_root.exists():
        backup_file = backup_file_root
        old_file = project_path / "_resume.md"
        location = "root"
    else:
        return ("SKIP", "No backup file found")

    try:
        # Remove new file if exists
        if new_file.exists():
            new_file.unlink()

        # Restore from backup to original location
        backup_file.rename(old_file)

        return ("SUCCESS", f"Rolled back to {location}_resume.md")
    except Exception as e:
        return ("ERROR", f"Rollback failed: {e}")


def main():
    """Main migration script."""
    parser = argparse.ArgumentParser(description="Migrate _resume.md files to resume-context.md")
    parser.add_argument("--dry-run", action="store_true", help="Show changes without modifying files")
    parser.add_argument("--project", type=str, help="Migrate only specific project ID (e.g., '24-project-name')")
    parser.add_argument("--rollback", action="store_true", help="Rollback migration (restore from backup)")
    args = parser.parse_args()

    # Determine base path (strategy-nexus root)
    script_path = Path(__file__).resolve()
    base_path = script_path.parent.parent.parent.parent  # Up 4 levels from 03-working

    print("=" * 80)
    if args.rollback:
        print("ROLLBACK: Resume File Migration (_resume.md <- resume-context.md)")
    else:
        print("Migration: _resume.md -> resume-context.md")
    print("=" * 80)
    print(f"Base path: {base_path}")
    print(f"Mode: {'DRY-RUN' if args.dry_run else 'LIVE MIGRATION'}")
    print("-" * 80)

    # Find projects
    if args.project:
        # Single project
        project_path = base_path / "02-projects" / args.project
        if not project_path.exists():
            print(f"ERROR: Project not found: {args.project}")
            return 1
        projects = [project_path]
    else:
        # All projects
        projects = find_projects(base_path)

    if not projects:
        print("No projects found")
        return 0

    print(f"Found {len(projects)} projects\n")

    # Migrate each project
    results = {
        "SUCCESS": [],
        "SKIP": [],
        "ERROR": [],
        "DRY-RUN": []
    }

    for project_path in projects:
        project_id = project_path.name

        if args.rollback:
            status, message = rollback_migration(project_path)
        else:
            status, message = migrate_project_resume(project_path, dry_run=args.dry_run)

        results[status].append((project_id, message))

        # Print result
        icons = {
            "SUCCESS": "[OK]",
            "SKIP": "[SKIP]",
            "ERROR": "[ERR]",
            "DRY-RUN": "[DRY]"
        }
        icon = icons.get(status, "[?]")
        print(f"{icon} {project_id}: {message}")

    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Success: {len(results['SUCCESS'])}")
    print(f"Skipped: {len(results['SKIP'])}")
    print(f"Errors: {len(results['ERROR'])}")
    if args.dry_run:
        print(f"Dry-run: {len(results['DRY-RUN'])}")
    print("=" * 80)

    # Show errors if any
    if results['ERROR']:
        print("\nERRORS:")
        for project_id, message in results['ERROR']:
            print(f"  - {project_id}: {message}")

    return 1 if results['ERROR'] else 0


if __name__ == "__main__":
    sys.exit(main())
