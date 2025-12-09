#!/usr/bin/env python3
"""
Bulk Complete Onboarding Projects

Marks all 4 onboarding projects (00, 01, 02, 03) as COMPLETE.
Can be run independently or called from skip-onboarding skill.

Usage:
    python 00-system/core/bulk-complete-onboarding.py

What it does:
    1. Finds all onboarding projects (00-onboarding/*)
    2. Marks all tasks in tasks.md as complete ([ ] → [x])
    3. Updates status in overview.md to COMPLETE
    4. Reports completion status
"""

import os
import re
import sys
from pathlib import Path

# Configure UTF-8 output for cross-platform compatibility
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass  # Python < 3.7

# Onboarding projects (4 total)
ONBOARDING_PROJECTS = [
    "02-projects/00-onboarding/00-define-goals",
    "02-projects/00-onboarding/01-first-project",
    "02-projects/00-onboarding/02-first-skill",
    "02-projects/00-onboarding/03-system-mastery"
]

def get_project_root():
    """Find Nexus-v3 root directory"""
    current = Path(__file__).resolve()
    # Go up from 00-system/core/ to root
    return current.parent.parent.parent

def mark_tasks_complete(tasks_file):
    """Mark all tasks in tasks.md as complete"""
    if not tasks_file.exists():
        return False
    
    try:
        content = tasks_file.read_text(encoding='utf-8')
        
        # Replace all [ ] with [x]
        updated = content.replace('- [ ]', '- [x]')
        
        # Write back
        tasks_file.write_text(updated, encoding='utf-8')
        return True
    except Exception as e:
        print(f"   [WARN] Error updating tasks: {e}")
        return False

def update_overview_status(overview_file, new_status="COMPLETE"):
    """Update status in YAML frontmatter"""
    if not overview_file.exists():
        return False
    
    try:
        content = overview_file.read_text(encoding='utf-8')
        
        # Update status line in YAML frontmatter
        updated = re.sub(
            r'^status:\s*\w+',
            f'status: {new_status}',
            content,
            flags=re.MULTILINE
        )
        
        overview_file.write_text(updated, encoding='utf-8')
        return True
    except Exception as e:
        print(f"   [WARN] Error updating overview: {e}")
        return False

def mark_project_complete(project_path):
    """Mark all tasks and status in project as complete"""
    project_dir = get_project_root() / project_path
    
    if not project_dir.exists():
        print(f"[WARN] Project not found: {project_path}")
        return False

    project_name = project_dir.name
    print(f"[PROC] Processing: {project_name}")
    
    # Update tasks.md
    tasks_file = project_dir / "01-planning" / "tasks.md"
    tasks_updated = mark_tasks_complete(tasks_file)
    
    if tasks_updated:
        print(f"   [OK] All tasks marked complete")
    else:
        print(f"   [WARN] Tasks file not found or error")
    
    # Update overview.md status
    overview_file = project_dir / "01-planning" / "overview.md"
    overview_updated = update_overview_status(overview_file)
    
    if overview_updated:
        print(f"   [OK] Status updated to COMPLETE")
    else:
        print(f"   [WARN] Overview file not found or error")
    
    return tasks_updated and overview_updated

def main():
    """Main execution"""
    print("=" * 70)
    print("BULK COMPLETING ONBOARDING PROJECTS")
    print("=" * 70)
    print()
    
    completed = 0
    failed = []
    
    for project in ONBOARDING_PROJECTS:
        if mark_project_complete(project):
            completed += 1
        else:
            failed.append(project)
        print()
    
    print("=" * 70)
    print(f"[DONE] Completed: {completed}/{len(ONBOARDING_PROJECTS)} projects")

    if failed:
        print(f"[WARN] Failed: {len(failed)} projects")
        for f in failed:
            print(f"   - {f}")
    else:
        print("[OK] All onboarding projects marked complete!")
        print()
        print("You're ready to work with Nexus!")

    print("=" * 70)

if __name__ == "__main__":
    main()
