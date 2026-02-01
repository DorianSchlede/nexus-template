#!/usr/bin/env python3
"""
bulk-complete.py - Bulk complete tasks in a build (all or partial)
VERSION 2.1 - NOW SUPPORTS 04-steps.md, steps.md, AND tasks.md

Usage:
    python bulk-complete.py --build <build-id>                    # Interactive mode
    python bulk-complete.py --build 01 --all                        # Complete all tasks
    python bulk-complete.py --build 01 --tasks 1-5,7,10-15          # Complete specific tasks
    python bulk-complete.py --build 01 --section 3                  # Complete all in Section 3
    python bulk-complete.py --build 01 --section "Section 4"        # Complete all in Section 4

Purpose:
    Quickly mark tasks in a build's task file as complete.
    Much faster than individually checking off 20+ tasks with Edit tool.
    NOW SUPPORTS PARTIAL COMPLETIONS!

Version 2.1 Changes:
    - Auto-detects 04-steps.md (current format), steps.md, or tasks.md (legacy)
    - Prefers numbered format (04-steps.md) created by init_build.py
    - Backward compatible with all existing builds

Use When:
    - Entire build is complete (use --all)
    - Specific sections are complete (use --section)
    - Individual tasks are complete (use --tasks)
    - Interactive selection needed (run without flags)

Performance:
    - Completes 100 tasks in <1 second
    - Single file operation (read -> replace -> write)
"""

import sys
import re
from pathlib import Path
from typing import List, Tuple, Set


def find_task_file(build_path: Path) -> Path:
    """
    Find the task tracking file (04-steps.md, steps.md, or tasks.md).

    Tries numbered format first (04-steps.md), then legacy formats.

    Args:
        build_path: Path to build directory

    Returns:
        Path to the task file, or None if none exists
    """
    planning_dir = build_path / "01-planning"

    # Try numbered format first (04-steps.md) - current standard
    numbered_steps = planning_dir / "04-steps.md"
    if numbered_steps.exists():
        return numbered_steps

    # Try unnumbered format (steps.md) - legacy
    steps_file = planning_dir / "steps.md"
    if steps_file.exists():
        return steps_file

    # Fall back to legacy format (tasks.md)
    tasks_file = planning_dir / "tasks.md"
    if tasks_file.exists():
        return tasks_file

    return None


def extract_tasks(content: str) -> List[Tuple[int, str, bool]]:
    """
    Extract all tasks with their line numbers and completion status.

    Returns:
        List of (task_number, line_idx, task_text, is_completed)
    """
    lines = content.split('\n')
    tasks = []
    task_num = 0

    for line_idx, line in enumerate(lines):
        # Match checkbox patterns
        uncompleted_match = re.match(r'^(\s*)- \[ \] (.+)$', line)
        completed_match = re.match(r'^(\s*)- \[x\] (.+)$', line, re.IGNORECASE)

        if uncompleted_match or completed_match:
            task_num += 1
            task_text = (uncompleted_match or completed_match).group(2)
            is_completed = bool(completed_match)
            tasks.append((task_num, line_idx, task_text, is_completed))

    return tasks


def parse_task_selection(selection: str, max_tasks: int) -> Set[int]:
    """
    Parse task selection string like "1-5,7,10-15" into set of task numbers.

    Args:
        selection: String with ranges and individual numbers
        max_tasks: Maximum task number available

    Returns:
        Set of task numbers to complete
    """
    result = set()

    for part in selection.split(','):
        part = part.strip()

        if '-' in part:
            # Range like "1-5"
            try:
                start, end = part.split('-')
                start_num = int(start.strip())
                end_num = int(end.strip())

                for num in range(start_num, end_num + 1):
                    if 1 <= num <= max_tasks:
                        result.add(num)
            except ValueError:
                print(f"[WARNING] Invalid range format: {part}")
        else:
            # Individual number
            try:
                num = int(part)
                if 1 <= num <= max_tasks:
                    result.add(num)
            except ValueError:
                print(f"[WARNING] Invalid task number: {part}")

    return result


def extract_section_tasks(content: str, section_name: str) -> Set[int]:
    """
    Extract task numbers from a specific section.

    Args:
        content: Full file content
        section_name: Section identifier (e.g., "Section 3" or "3" or "Phase 1")

    Returns:
        Set of task numbers in that section
    """
    lines = content.split('\n')
    tasks = extract_tasks(content)

    # Find section boundaries - handle various formats
    # "## Section 1: Title" or "## Phase 1:" or "## Section 1" or section name "Context Loading"
    section_num = section_name.replace('Section', '').replace('section', '').replace('Phase', '').replace('phase', '').strip()

    # Try multiple patterns
    patterns = [
        re.compile(rf'^##\s+(Section|Phase)\s+{re.escape(section_num)}(?:[:\s]|$)', re.IGNORECASE),  # "## Section 1:" or "## Phase 1:" or "## Section 1"
        re.compile(rf'^##\s+{re.escape(section_name)}\s*$', re.IGNORECASE),  # Exact match "## Context Loading"
    ]

    next_section_pattern = re.compile(r'^##\s+(Section\s+\d+|Phase\s+\d+|[A-Z])', re.IGNORECASE)  # Any section header

    in_section = False
    section_start_line = None
    section_end_line = None

    for line_idx, line in enumerate(lines):
        # Check if this is our target section
        if any(pattern.search(line) for pattern in patterns):
            in_section = True
            section_start_line = line_idx
        # Check if we've hit the next section
        elif in_section and next_section_pattern.search(line):
            section_end_line = line_idx
            break

    if section_start_line is None:
        return set()

    if section_end_line is None:
        section_end_line = len(lines)

    # Get tasks in this range
    result = set()
    for task_num, line_idx, _, _ in tasks:
        if section_start_line <= line_idx < section_end_line:
            result.add(task_num)

    return result


def count_tasks(content: str) -> tuple[int, int]:
    """
    Count uncompleted and completed tasks in content.

    Returns:
        (uncompleted_count, completed_count)
    """
    uncompleted = len(re.findall(r'- \[ \]', content))
    completed = len(re.findall(r'- \[x\]', content, re.IGNORECASE))
    return uncompleted, completed


def bulk_complete_tasks(
    build_id: str,
    base_path: str = ".",
    complete_all: bool = False,
    task_selection: str = None,
    section: str = None,
    interactive: bool = False,
    no_confirm: bool = False
):
    """
    Mark tasks in a build as complete (all or partial).

    Args:
        build_id: Build identifier (e.g., "01-first-build" or just "01")
        base_path: Base path to Nexus-v3
        complete_all: If True, complete all tasks
        task_selection: String like "1-5,7,10-15" for specific tasks
        section: Section name/number to complete (e.g., "3" or "Section 3" or "Phase 2")
        interactive: If True, show interactive selection
        no_confirm: If True, skip confirmation prompt (for AI automation)

    Returns:
        True if successful, False otherwise
    """
    base = Path(base_path)

    # Find build folder - try multiple patterns
    possible_folders = [
        base / "02-builds" / build_id,  # Full ID provided
        base / "02-builds" / f"{build_id.zfill(2)}-*",  # Just number provided
        base / "02-builds" / "00-onboarding" / build_id,  # Onboarding subfolder
        base / "02-builds" / "00-onboarding" / f"{build_id.zfill(2)}-*",  # Onboarding with number
    ]

    build_path = None
    for pattern in possible_folders:
        matches = list(base.glob(str(pattern.relative_to(base))))
        if matches:
            build_path = matches[0]
            break

    if not build_path or not build_path.exists():
        print(f"[ERROR] Build not found: {build_id}")
        print(f"[INFO] Searched in: 02-builds/")
        return False

    # Find task file (steps.md or tasks.md) - NEW AUTO-DETECTION
    task_file = find_task_file(build_path)

    if not task_file:
        print(f"[ERROR] No task file found in {build_path.name}")
        print(f"[INFO] Expected: 04-steps.md, steps.md, or tasks.md in 01-planning/")
        return False

    print(f"[INFO] Using task file: {task_file.name}")

    # Read current content
    try:
        content = task_file.read_text(encoding='utf-8')
    except Exception as e:
        print(f"[ERROR] Failed to read {task_file.name}: {e}")
        return False

    # Extract all tasks
    all_tasks = extract_tasks(content)
    uncompleted, completed = count_tasks(content)
    total = uncompleted + completed

    if uncompleted == 0:
        print(f"[OK] All tasks already complete in {build_path.name}!")
        print(f"[INFO] {completed}/{total} tasks are checked")
        return True

    print(f"Build: {build_path.name}")
    print(f"Tasks: {uncompleted} uncompleted, {completed} completed (Total: {total})")
    print()

    # Determine which tasks to complete
    tasks_to_complete = set()

    if complete_all:
        # Complete all uncompleted tasks
        tasks_to_complete = {num for num, _, _, is_completed in all_tasks if not is_completed}
        print(f"[MODE] Complete ALL {len(tasks_to_complete)} uncompleted tasks")

    elif section:
        # Complete tasks in specific section
        tasks_to_complete = extract_section_tasks(content, section)
        if not tasks_to_complete:
            print(f"[ERROR] No tasks found in Section/Phase {section}")
            return False
        # Filter to only uncompleted ones
        tasks_to_complete = {
            num for num in tasks_to_complete
            if not all_tasks[num-1][3]  # Check is_completed flag
        }
        print(f"[MODE] Complete {len(tasks_to_complete)} uncompleted tasks in Section/Phase {section}")

    elif task_selection:
        # Complete specific tasks by number
        tasks_to_complete = parse_task_selection(task_selection, total)
        if not tasks_to_complete:
            print(f"[ERROR] No valid tasks in selection: {task_selection}")
            return False
        # Filter to only uncompleted ones
        tasks_to_complete = {
            num for num in tasks_to_complete
            if not all_tasks[num-1][3]  # Check is_completed flag
        }
        print(f"[MODE] Complete {len(tasks_to_complete)} specific tasks: {sorted(tasks_to_complete)}")

    elif interactive:
        # Interactive mode - show tasks and let user select
        print("[MODE] Interactive selection")
        print()
        print("Uncompleted tasks:")
        for num, _, text, is_completed in all_tasks:
            if not is_completed:
                print(f"  {num}. {text[:80]}{'...' if len(text) > 80 else ''}")
        print()
        print("Enter tasks to complete:")
        print("  Examples: '1-5' or '1,3,5' or '1-5,7,10-15'")
        print("  Or 'all' for all tasks")
        selection = input("Selection: ").strip()

        if selection.lower() == 'all':
            tasks_to_complete = {num for num, _, _, is_completed in all_tasks if not is_completed}
        else:
            tasks_to_complete = parse_task_selection(selection, total)
            # Filter to only uncompleted ones
            tasks_to_complete = {
                num for num in tasks_to_complete
                if not all_tasks[num-1][3]
            }

    else:
        print("[ERROR] No mode specified. Use --all, --tasks, --section, or run interactively")
        return False

    if not tasks_to_complete:
        print("[INFO] No uncompleted tasks to mark")
        return True

    # Show what will be done
    print()
    print(f"[CONFIRM] Will mark {len(tasks_to_complete)} tasks as complete:")
    for num in sorted(tasks_to_complete):
        task_num, line_idx, text, _ = all_tasks[num-1]
        # Handle Unicode encoding for Windows console
        try:
            print(f"  [x] Task {num}: {text[:70]}{'...' if len(text) > 70 else ''}")
        except UnicodeEncodeError:
            # Fallback: ASCII-safe representation
            safe_text = text[:70].encode('ascii', 'replace').decode('ascii')
            print(f"  [x] Task {num}: {safe_text}{'...' if len(text) > 70 else ''}")
    print()

    # Skip confirmation if no_confirm flag set (for AI automation)
    if not no_confirm:
        response = input(f"Proceed? (y/n): ").strip().lower()
        if response != 'y':
            print("[CANCELLED] No changes made")
            return False
    else:
        print("[AUTO-CONFIRM] Proceeding without confirmation (--no-confirm flag)")


    # Perform completion
    try:
        lines = content.split('\n')

        # Mark selected tasks as complete
        for num in tasks_to_complete:
            task_num, line_idx, text, is_completed = all_tasks[num-1]
            if not is_completed:
                # Replace [ ] with [x] on this specific line
                lines[line_idx] = re.sub(r'- \[ \]', '- [x]', lines[line_idx])

        updated_content = '\n'.join(lines)

        # Write updated content
        task_file.write_text(updated_content, encoding='utf-8')

        # VALIDATE by re-reading file (CRITICAL for evidence)
        try:
            validation_content = task_file.read_text(encoding='utf-8')
            new_uncompleted, new_completed = count_tasks(validation_content)
        except Exception as e:
            print(f"[WARNING] Validation read failed: {e}")
            new_uncompleted, new_completed = count_tasks(updated_content)

        print()
        print(f"[SUCCESS] Successfully completed {len(tasks_to_complete)} tasks!")
        print(f"Updated: {new_completed}/{total} tasks now complete ({(new_completed/total*100):.1f}%)")
        print(f"[VALIDATED] Re-read file shows {new_uncompleted} uncompleted, {new_completed} completed")
        print(f"File: {task_file.relative_to(base)}")

        return True

    except Exception as e:
        print(f"[ERROR] Failed to update tasks: {e}")
        return False


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Bulk complete tasks in a build (all or partial) - V2.1 with 04-steps.md support",
        epilog="""
Examples:
  python bulk-complete.py --build 01                      # Interactive mode
  python bulk-complete.py --build 01 --all                # Complete all tasks
  python bulk-complete.py --build 01 --tasks 1-5,7,10-15  # Complete specific tasks
  python bulk-complete.py --build 01 --section 3          # Complete Section 3
  python bulk-complete.py --build 01 --section "Phase 2"  # Complete Phase 2 (new format)

Version 2.1 Features:
  - Auto-detects 04-steps.md (current) or steps.md/tasks.md (legacy)
  - Supports both "Section" and "Phase" naming conventions
  - Backward compatible with all existing builds
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        '--build',
        required=True,
        help='Build ID (e.g., 01-first-build or just 01)'
    )
    parser.add_argument(
        '--all',
        action='store_true',
        help='Complete ALL uncompleted tasks'
    )
    parser.add_argument(
        '--tasks',
        type=str,
        help='Complete specific tasks (e.g., "1-5,7,10-15")'
    )
    parser.add_argument(
        '--section',
        type=str,
        help='Complete all tasks in a section (e.g., "3" or "Section 3" or "Phase 2")'
    )
    parser.add_argument(
        '--base-path',
        default='.',
        help='Base path to Nexus-v3 (default: current directory)'
    )
    parser.add_argument(
        '--no-confirm',
        action='store_true',
        help='Skip confirmation prompt (for AI automation)'
    )

    args = parser.parse_args()

    print("Bulk Task Completion Tool V2.1 (04-steps.md, steps.md, tasks.md support)")
    print("=" * 60)
    print()

    # Determine mode
    interactive = not (args.all or args.tasks or args.section)

    success = bulk_complete_tasks(
        build_id=args.build,
        base_path=args.base_path,
        complete_all=args.all,
        task_selection=args.tasks,
        section=args.section,
        interactive=interactive,
        no_confirm=args.no_confirm
    )

    if success:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
