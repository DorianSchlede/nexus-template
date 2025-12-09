#!/usr/bin/env python3
"""
Uncheck all tasks in onboarding projects
"""
import sys
from pathlib import Path
import re

# Configure UTF-8 output for cross-platform compatibility
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass  # Python < 3.7

def uncheck_all_tasks(file_path):
    """Replace all [x] with [ ] in a file"""
    try:
        content = file_path.read_text(encoding='utf-8')
        # Replace both [x] and [X] with [ ]
        updated = re.sub(r'- \[x\]', '- [ ]', content, flags=re.IGNORECASE)
        file_path.write_text(updated, encoding='utf-8')
        
        # Count changes
        original_checked = len(re.findall(r'- \[x\]', content, re.IGNORECASE))
        new_checked = len(re.findall(r'- \[x\]', updated, re.IGNORECASE))
        unchecked_count = original_checked - new_checked
        
        return unchecked_count
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return 0

# Process all onboarding projects
base_path = Path(__file__).parent.parent.parent
onboarding_projects = [
    "02-projects/00-onboarding/00-define-goals/01-planning/steps.md",
    "02-projects/00-onboarding/01-first-project/01-planning/steps.md",
    "02-projects/00-onboarding/02-first-skill/01-planning/steps.md",
    "02-projects/00-onboarding/03-system-mastery/01-planning/steps.md",
]

total_unchecked = 0
for project_file in onboarding_projects:
    file_path = base_path / project_file
    if file_path.exists():
        count = uncheck_all_tasks(file_path)
        total_unchecked += count
        print(f"[OK] {file_path.name}: Unchecked {count} tasks")
    else:
        print(f"[SKIP] {file_path.name}: File not found")

print(f"\n[DONE] Total: Unchecked {total_unchecked} tasks across all onboarding projects")
