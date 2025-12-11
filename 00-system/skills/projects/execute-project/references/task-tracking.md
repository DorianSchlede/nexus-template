# Task Tracking: Parsing and Bulk-Complete Logic

**Purpose**: Technical reference for parsing tasks and using bulk-complete-tasks.py

**Audience**: AI agents implementing execute-project skill

**Version**: 1.0

---

## Overview

This document explains:
1. How to parse tasks.md / steps.md files
2. How to use bulk-complete-tasks.py script
3. Task completion validation patterns
4. Error handling and edge cases

---

## Part 1: Task File Parsing

### Auto-Detection: steps.md vs tasks.md

**Priority Order**:
```python
def find_task_file(project_path):
    """
    Auto-detect task tracking file.

    Priority:
    1. steps.md (new format, created by init_project.py)
    2. tasks.md (legacy format, onboarding projects)
    """
    planning_dir = project_path / "01-planning"

    # Try new format first
    steps_file = planning_dir / "steps.md"
    if steps_file.exists():
        return steps_file

    # Fall back to legacy
    tasks_file = planning_dir / "tasks.md"
    if tasks_file.exists():
        return tasks_file

    return None
```

**Usage**:
```python
task_file = find_task_file(project_path)

if not task_file:
    print("[ERROR] No task file found")
    print("[INFO] Expected: steps.md or tasks.md in 01-planning/")
    return False

print(f"[INFO] Using task file: {task_file.name}")
```

---

### Task Extraction

**Checkbox Pattern**:
```python
import re

def extract_tasks(content):
    """
    Extract all tasks with line numbers and completion status.

    Returns:
        List of (task_number, line_idx, task_text, is_completed)
    """
    lines = content.split('\n')
    tasks = []
    task_num = 0

    for line_idx, line in enumerate(lines):
        # Match uncompleted: - [ ]
        uncompleted_match = re.match(r'^(\s*)- \[ \] (.+)$', line)

        # Match completed: - [x] or - [X]
        completed_match = re.match(r'^(\s*)- \[x\] (.+)$', line, re.IGNORECASE)

        if uncompleted_match or completed_match:
            task_num += 1
            task_text = (uncompleted_match or completed_match).group(2)
            is_completed = bool(completed_match)

            tasks.append((task_num, line_idx, task_text, is_completed))

    return tasks
```

**Example Output**:
```python
tasks = extract_tasks(content)
# [
#   (1, 10, "Define project scope", True),
#   (2, 11, "Create requirements doc", True),
#   (3, 15, "Design architecture", False),
#   (4, 16, "Implement core logic", False),
#   ...
# ]
```

---

### Section Extraction

**Section Header Patterns**:
```python
def extract_sections(content):
    """
    Extract sections from task file.

    Supported formats:
    - ## Section 1: Planning
    - ## Phase 2: Implementation
    - ## Step 3: Testing
    """
    sections = []
    current_section = None
    task_num = 0

    for line_idx, line in enumerate(content.split('\n')):
        # Detect section headers
        section_match = re.match(
            r'^##\s+(Section|Phase|Step)\s+(\d+):?\s*(.+)?',
            line,
            re.IGNORECASE
        )

        if section_match:
            # Save previous section
            if current_section:
                sections.append(current_section)

            # Start new section
            section_type = section_match.group(1)
            section_num = int(section_match.group(2))
            section_name = section_match.group(3) or f"{section_type} {section_num}"

            current_section = {
                "number": section_num,
                "name": section_name,
                "type": section_type,
                "start_line": line_idx,
                "tasks": []
            }

        # Add tasks to current section
        elif current_section:
            task_match = re.match(
                r'- \[([ x])\] (.+)',
                line,
                re.IGNORECASE
            )

            if task_match:
                task_num += 1
                is_complete = task_match.group(1).lower() == 'x'
                task_text = task_match.group(2)

                current_section["tasks"].append({
                    "number": task_num,
                    "line_idx": line_idx,
                    "text": task_text,
                    "completed": is_complete
                })

    # Add last section
    if current_section:
        sections.append(current_section)

    return sections
```

**Example Output**:
```python
sections = extract_sections(content)
# [
#   {
#     "number": 1,
#     "name": "Planning",
#     "type": "Section",
#     "start_line": 10,
#     "tasks": [
#       {"number": 1, "line_idx": 12, "text": "Define scope", "completed": True},
#       {"number": 2, "line_idx": 13, "text": "Create requirements", "completed": True}
#     ]
#   },
#   {
#     "number": 2,
#     "name": "Implementation",
#     "type": "Section",
#     "start_line": 20,
#     "tasks": [
#       {"number": 3, "line_idx": 22, "text": "Build API", "completed": False},
#       ...
#     ]
#   }
# ]
```

---

### Task Counting

**Quick Count**:
```python
def count_tasks(content):
    """
    Count uncompleted and completed tasks.

    Returns:
        (uncompleted_count, completed_count)
    """
    uncompleted = len(re.findall(r'- \[ \]', content))
    completed = len(re.findall(r'- \[x\]', content, re.IGNORECASE))

    return uncompleted, completed
```

**Usage**:
```python
uncompleted, completed = count_tasks(content)
total = uncompleted + completed
progress_pct = (completed / total * 100) if total > 0 else 0

print(f"Progress: {completed}/{total} ({progress_pct:.1f}%)")
# Output: "Progress: 25/40 (62.5%)"
```

---

### Finding Current Section

**Algorithm**:
```python
def find_current_section(sections):
    """
    Find first section with uncompleted tasks.

    Returns:
        {
            "section": section_obj,
            "next_task": first_uncompleted_task,
            "remaining": count_of_uncompleted
        }
        or None if all complete
    """
    for section in sections:
        uncompleted_tasks = [
            task for task in section["tasks"]
            if not task["completed"]
        ]

        if uncompleted_tasks:
            return {
                "section": section,
                "next_task": uncompleted_tasks[0],
                "remaining": len(uncompleted_tasks)
            }

    # All sections complete
    return None
```

**Usage**:
```python
current = find_current_section(sections)

if current:
    section = current["section"]
    next_task = current["next_task"]
    remaining = current["remaining"]

    print(f"Current: Section {section['number']} - {section['name']}")
    print(f"Next task: {next_task['number']} - {next_task['text']}")
    print(f"Remaining: {remaining} tasks in this section")
else:
    print("All sections complete! 🎉")
```

---

## Part 2: Using bulk-complete-tasks.py

### Script Location
```
00-system/skills/bulk-complete/scripts/bulk-complete.py
```

**Why in close-session?**: Originally created for session cleanup, but now shared by execute-project

---

### Modes of Operation

#### Mode 1: Complete All Tasks
```bash
python 00-system/skills/bulk-complete/scripts/bulk-complete.py \
  --project 05-lead-qualification \
  --all \
  --no-confirm
```

**When to use**:
- Project is 100% complete
- All work done, ready to finalize
- Finalizing after manual task completion

**Output**:
```
[INFO] Using task file: steps.md
[MODE] Complete ALL 15 uncompleted tasks
[SUCCESS] Successfully completed 15 tasks!
Updated: 40/40 tasks now complete (100%)
✅ VALIDATED: Re-read file shows 0 uncompleted, 40 completed
```

---

#### Mode 2: Complete Specific Section
```bash
python 00-system/skills/bulk-complete/scripts/bulk-complete.py \
  --project 05-lead-qualification \
  --section 3 \
  --no-confirm
```

**When to use**:
- Section 3 work complete
- Want to bulk-mark all Section 3 tasks
- Primary mode for execute-project workflow

**Supported Formats**:
```bash
--section 3              # Section number
--section "Section 3"    # Full section name
--section "Phase 2"      # Phase naming (new format)
```

**Output**:
```
[INFO] Using task file: steps.md
[MODE] Complete 16 uncompleted tasks in Section/Phase 3
[SUCCESS] Successfully completed 16 tasks!
Updated: 28/40 tasks now complete (70%)
✅ VALIDATED: Re-read file shows 12 uncompleted, 28 completed
```

---

#### Mode 3: Complete Specific Tasks
```bash
python 00-system/skills/bulk-complete/scripts/bulk-complete.py \
  --project 05-lead-qualification \
  --tasks "13-21,25,30-35" \
  --no-confirm
```

**When to use**:
- Partial section completion
- User completed specific tasks, not whole section
- Mid-session checkpoint

**Syntax**:
- Ranges: `1-5` (tasks 1 through 5)
- Individual: `7` (task 7 only)
- Combined: `1-5,7,10-15` (ranges + individual)

**Output**:
```
[INFO] Using task file: steps.md
[MODE] Complete 12 specific tasks: [13, 14, 15, 16, 17, 18, 19, 20, 21, 25, 30, 31, 32, 33, 34, 35]
[SUCCESS] Successfully completed 12 tasks!
Updated: 25/40 tasks now complete (62.5%)
✅ VALIDATED: Re-read file shows 15 uncompleted, 25 completed
```

---

#### Mode 4: Interactive (AI doesn't use this)
```bash
python 00-system/skills/bulk-complete/scripts/bulk-complete.py \
  --project 05-lead-qualification
```

**When to use**:
- User running script manually
- AI should NOT use this mode (requires input)

**AI should use**: Modes 1-3 with `--no-confirm` flag

---

### Critical Flag: --no-confirm

**Why it exists**:
- Script was designed for human users (requires confirmation)
- AI automation needs to skip confirmation prompts
- `--no-confirm` bypasses the "Proceed? (y/n)" prompt

**Always use in AI workflows**:
```bash
# ✅ CORRECT (AI automation)
--no-confirm

# ❌ WRONG (will hang waiting for user input)
# (no flag - script waits for y/n)
```

---

### Project ID Flexibility

**Script accepts multiple formats**:
```bash
# Full project folder name
--project 05-lead-qualification

# Just the ID number
--project 05

# Zero-padded or not
--project 5    # Script converts to "05"
```

**Auto-detection logic**:
```python
# Script tries these patterns:
1. 02-projects/05-lead-qualification/  (exact match)
2. 02-projects/05-*/                   (glob pattern)
3. 02-projects/5-*/                    (unpadded ID)
```

---

### Validation Pattern

**Script ALWAYS validates** after writing:
```python
# 1. Write updated content
task_file.write_text(updated_content, encoding='utf-8')

# 2. Re-read file to validate
validation_content = task_file.read_text(encoding='utf-8')
new_uncompleted, new_completed = count_tasks(validation_content)

# 3. Display evidence
print(f"✅ VALIDATED: Re-read file shows {new_uncompleted} uncompleted, {new_completed} completed")
```

**Why this matters**:
- Proves tasks were actually updated
- Catches file write errors
- Provides evidence for user
- execute-project can trust the output

---

## Part 3: Integration Patterns

### Pattern 1: Section-Based Execution

**Workflow**:
```python
# 1. Execute work in section
execute_section_tasks(section)

# 2. Ask user for confirmation
print(f"Section {section['number']} complete. Bulk-complete?")
user_confirms = input("yes/no: ")

# 3. If confirmed, bulk-complete
if user_confirms.lower() == "yes":
    run_bulk_complete_section(project_id, section['number'])

# 4. Validate and show progress
display_updated_progress()
```

**Example**:
```python
# User working on Section 3
print("Executing Section 3: Implementation...")

# [Work happens: code, files, etc.]

print("\n✅ Section 3 work complete!")
print("Ready to bulk-complete Section 3? (yes/no)")

if input().strip().lower() == "yes":
    subprocess.run([
        "python",
        "00-system/skills/bulk-complete/scripts/bulk-complete.py",
        "--project", "05-lead-qualification",
        "--section", "3",
        "--no-confirm"
    ])

    # Show validation output
    # Progress: 28/40 (70%)
```

---

### Pattern 2: Checkpoint-Based (Large Sections)

**Workflow**:
```python
# For sections with >15 tasks
# Checkpoint every 5-7 tasks

tasks_completed = 0
checkpoint_interval = 5

for task in section["tasks"]:
    execute_task(task)
    tasks_completed += 1

    # Checkpoint
    if tasks_completed % checkpoint_interval == 0:
        offer_checkpoint(tasks_completed)

# Final section bulk-complete
bulk_complete_section()
```

**Example**:
```python
# Section 3 has 20 tasks
# Checkpoint at 5, 10, 15, then bulk-complete all 20

# After task 5
print("Checkpoint: 5/20 tasks complete")
print("Options:")
print("1. Continue")
print("2. Bulk-complete 1-5 now")

if user_choice == 2:
    run_bulk_complete_tasks("05", tasks="1-5")

# After task 10
print("Checkpoint: 10/20 tasks complete")
# ... (repeat)

# After task 20
print("Section 3 complete! Bulk-complete all 20?")
run_bulk_complete_section("05", section=3)
```

---

### Pattern 3: Partial Completion (Pause Mid-Section)

**Workflow**:
```python
# User wants to pause mid-section
current_task = 15  # User completed up to task 15
total_in_section = 20

print(f"You're at task {current_task}/{total_in_section} in this section")
print("Options:")
print("1. Bulk-complete tasks 1-15 (what you've done)")
print("2. Leave as-is (resume here next time)")

if user_choice == 1:
    run_bulk_complete_tasks("05", tasks=f"1-{current_task}")
```

**Example**:
```python
# User pauses after task 18 of 20 in Section 3

print("Pausing mid-section...")
print("Completed tasks 1-18, remaining: 19-20")
print("\nBulk-complete 1-18 before pausing?")

if input().strip().lower() == "yes":
    subprocess.run([
        "python",
        "00-system/skills/bulk-complete/scripts/bulk-complete.py",
        "--project", "05-lead-qualification",
        "--tasks", "1-18",
        "--no-confirm"
    ])

    print("✅ Tasks 1-18 marked complete")
    print("Next session will resume at task 19")
```

---

## Part 4: Error Handling

### Error 1: Task File Not Found

**Detection**:
```python
task_file = find_task_file(project_path)

if not task_file:
    # Handle error
```

**Handling**:
```python
print("[ERROR] No task file found in project")
print("[INFO] Expected: steps.md or tasks.md in 01-planning/")
print("\nSolutions:")
print("1. Run 'validate-system' skill to check structure")
print("2. Create steps.md manually with checkbox format")
print("3. If this is an old project, use tasks.md instead")

return False
```

---

### Error 2: No Uncompleted Tasks

**Detection**:
```python
uncompleted, completed = count_tasks(content)

if uncompleted == 0:
    # All tasks already done
```

**Handling**:
```python
print(f"[OK] All tasks already complete in {project_name}!")
print(f"[INFO] {completed}/{completed} tasks are checked")
print("\nThis project is 100% complete! 🎉")
print("\nNext steps:")
print("1. Update project status to COMPLETE")
print("2. Use 'archive-project' skill to move to archive")
print("3. Or keep in active projects for reference")

return True  # Not an error, just complete
```

---

### Error 3: Invalid Section Number

**Detection**:
```python
section_tasks = extract_section_tasks(content, section_num)

if not section_tasks:
    # Section not found or no tasks
```

**Handling**:
```python
print(f"[ERROR] No tasks found in Section {section_num}")
print(f"\nAvailable sections:")

sections = extract_sections(content)
for section in sections:
    task_count = len(section["tasks"])
    print(f"  - Section {section['number']}: {section['name']} ({task_count} tasks)")

print(f"\nPlease specify a valid section number (1-{len(sections)})")

return False
```

---

### Error 4: Bulk-Complete Script Fails

**Detection**:
```python
result = subprocess.run([...], capture_output=True)

if result.returncode != 0:
    # Script failed
```

**Handling**:
```python
print("[ERROR] Bulk-complete failed!")
print(f"Error: {result.stderr.decode()}")
print("\nFallback: Manual task completion")
print("I'll mark tasks manually using Edit tool...")

# Fallback to manual Edit
for task_num in tasks_to_complete:
    # Use Edit tool to change - [ ] to - [x]
    edit_task_manually(task_file, task_num)

print("✅ Tasks marked manually (fallback method)")
```

---

### Error 5: Validation Mismatch

**Detection**:
```python
# After bulk-complete
expected_completed = old_completed + newly_completed
actual_completed = count_tasks(validate_content)[1]

if actual_completed != expected_completed:
    # Mismatch!
```

**Handling**:
```python
print("[WARNING] Validation mismatch detected!")
print(f"Expected: {expected_completed} completed")
print(f"Actual:   {actual_completed} completed")
print(f"Difference: {abs(expected_completed - actual_completed)} tasks")

print("\nPossible causes:")
print("- File was modified during execution")
print("- Some tasks already completed")
print("- Script bug (rare)")

print("\nRecommendation: Manually verify tasks in steps.md")

# Still show progress, but flag as needing verification
```

---

## Part 5: Best Practices

### DO

✅ **Always auto-detect task file**
```python
task_file = find_task_file(project_path)
print(f"[INFO] Using task file: {task_file.name}")
```

✅ **Always use --no-confirm for AI automation**
```bash
--no-confirm  # Skips confirmation prompt
```

✅ **Always validate after bulk-complete**
```python
# Script does this automatically
# Just parse the output
```

✅ **Always show before/after evidence**
```python
print(f"Before: {old_completed}/{total} ({old_pct}%)")
print(f"After:  {new_completed}/{total} ({new_pct}%)")
print(f"Change: +{newly_completed} tasks ✅")
```

✅ **Always handle errors gracefully**
```python
try:
    run_bulk_complete()
except Exception as e:
    fallback_to_manual_edit()
```

---

### DON'T

❌ **Don't assume file name**
```python
# WRONG
task_file = project_path / "01-planning/tasks.md"

# RIGHT
task_file = find_task_file(project_path)
```

❌ **Don't bulk-complete without work**
```python
# WRONG: Marking tasks before actually doing them
run_bulk_complete_section(3)  # But Section 3 not executed yet!

# RIGHT: Execute work first, THEN bulk-complete
execute_section_3_work()
run_bulk_complete_section(3)
```

❌ **Don't skip validation**
```python
# WRONG: Trust write without verification
run_bulk_complete()
print("Done!")  # Hope it worked

# RIGHT: Parse validation output
result = run_bulk_complete()
if "VALIDATED" in result.stdout:
    print("✅ Confirmed!")
```

❌ **Don't use interactive mode in AI workflows**
```python
# WRONG: Will hang waiting for input
subprocess.run(["python", "bulk-complete-tasks.py", "--project", "05"])

# RIGHT: Use --no-confirm
subprocess.run([
    "python", "bulk-complete-tasks.py",
    "--project", "05",
    "--section", "3",
    "--no-confirm"  # ← Critical!
])
```

---

## Summary

**Key Takeaways**:
1. Auto-detect steps.md vs tasks.md (prefer steps.md)
2. Extract sections and tasks with regex patterns
3. Use bulk-complete-tasks.py with --no-confirm flag
4. Three modes: --all, --section, --tasks
5. Always validate after bulk-complete
6. Handle errors gracefully with fallbacks
7. Show before/after evidence to user

**Script Location**:
```
00-system/skills/bulk-complete/scripts/bulk-complete.py
```

**Common Command**:
```bash
python 00-system/skills/bulk-complete/scripts/bulk-complete.py \
  --project [ID] \
  --section [N] \
  --no-confirm
```

---

**Version**: 1.0
**Last Updated**: 2025-01-22
**Status**: Production Ready
