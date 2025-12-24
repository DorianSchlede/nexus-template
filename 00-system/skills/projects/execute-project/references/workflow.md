# Execute-Project: Complete Workflow Reference

**Purpose**: Detailed step-by-step implementation guide for the execute-project skill

**Audience**: AI agents executing this skill

**Version**: 1.0

---

## Overview

This document provides the complete implementation workflow for executing projects systematically with continuous progress tracking.

**Core Pattern**: Load → Identify → Execute → Bulk-Complete → Validate → Repeat

---

## Step 1: Initialize Progress Tracking

### Purpose
Create comprehensive TodoWrite to give user visibility into entire execution workflow.

### Implementation

```python
# Count sections in tasks file
sections = parse_sections(tasks_content)
total_sections = len(sections)

# Build TodoWrite items
todo_items = [
    "Load project context",
    "Identify current phase/section",
]

# Add section execution tasks
for i, section in enumerate(sections, 1):
    todo_items.append(f"Execute Section {i}: {section.name}")
    todo_items.append(f"Bulk-complete Section {i}")

# Add completion tasks
todo_items.extend([
    "Project completion validation",
    "Trigger close-session"
])

# Create TodoWrite
TodoWrite(todos=todo_items)
```

### Success Criteria
- ✅ TodoWrite created with ALL workflow steps
- ✅ User can see complete execution roadmap
- ✅ Each section has two items: execute + bulk-complete

---

## Step 2: Load Project Context

### Purpose
Load all project planning files and display current state.

### Implementation

#### 2A. Run nexus-loader.py
```bash
python 00-system/core/nexus-loader.py --project [project-id]
```

**Expected Output**:
```json
{
  "loaded_at": "2025-01-22T10:30:00",
  "bundle": "project",
  "project_id": "05-lead-qualification",
  "project_path": "/path/to/02-projects/05-lead-qualification",
  "files": {
    "01-planning/overview.md": {
      "path": "/path/to/overview.md",
      "metadata": { ... }
    },
    "01-planning/plan.md": { ... },
    "01-planning/steps.md": { ... }
  }
}
```

#### 2B. Read Planning Files in Parallel
```python
Read: {project_path}/01-planning/overview.md
Read: {project_path}/01-planning/plan.md (or design.md)
Read: {project_path}/01-planning/steps.md (or tasks.md)
```

**Note**: Auto-detect steps.md (new format) vs tasks.md (legacy format)

#### 2C. Extract Project Metadata
```python
# From overview.md YAML frontmatter
project_metadata = {
    "id": "05-lead-qualification",
    "name": "Lead Qualification Workflow",
    "status": "IN_PROGRESS",
    "created": "2025-01-15",
    "last_worked": "2025-01-20"
}
```

#### 2D. Parse Tasks File
```python
# Extract all tasks with checkboxes
tasks = []
for line in steps_content.split('\n'):
    if match := re.match(r'- \[([ x])\] (.+)', line, re.IGNORECASE):
        is_complete = match.group(1).lower() == 'x'
        task_text = match.group(2)
        tasks.append({
            "completed": is_complete,
            "text": task_text
        })

# Calculate progress
total = len(tasks)
completed = sum(1 for t in tasks if t["completed"])
progress_pct = (completed / total * 100) if total > 0 else 0
```

#### 2E. Display Project Summary
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PROJECT: Lead Qualification Workflow
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ID: 05-lead-qualification
Status: IN_PROGRESS
Created: 2025-01-15
Last Worked: 2025-01-20

Progress: 12/40 tasks complete (30%)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Success Criteria
- ✅ All planning files loaded successfully
- ✅ Project metadata extracted
- ✅ Tasks parsed and counted
- ✅ Summary displayed to user

---

## Step 3: Identify Current Phase

### Purpose
Parse tasks file to determine current section and next uncompleted task.

### Implementation

#### 3A. Extract Sections
```python
def extract_sections(content):
    """
    Extract sections from tasks.md or steps.md.

    Sections are identified by headers like:
    - ## Section 1: Planning
    - ## Phase 2: Implementation
    - ## Step 3: Testing
    """
    sections = []
    current_section = None

    for line in content.split('\n'):
        # Detect section headers
        if match := re.match(r'^##\s+(Section|Phase|Step)\s+(\d+):?\s*(.+)?', line, re.IGNORECASE):
            if current_section:
                sections.append(current_section)

            section_type = match.group(1)
            section_num = int(match.group(2))
            section_name = match.group(3) or f"{section_type} {section_num}"

            current_section = {
                "number": section_num,
                "name": section_name,
                "tasks": []
            }

        # Add tasks to current section
        elif current_section and (task_match := re.match(r'- \[([ x])\] (.+)', line, re.IGNORECASE)):
            is_complete = task_match.group(1).lower() == 'x'
            task_text = task_match.group(2)
            current_section["tasks"].append({
                "completed": is_complete,
                "text": task_text
            })

    # Add last section
    if current_section:
        sections.append(current_section)

    return sections
```

#### 3B. Find Current Section
```python
def find_current_section(sections):
    """Find first section with uncompleted tasks."""
    for section in sections:
        uncompleted = [t for t in section["tasks"] if not t["completed"]]
        if uncompleted:
            return {
                "section": section,
                "next_task": uncompleted[0],
                "remaining": len(uncompleted)
            }

    # All sections complete
    return None
```

#### 3C. Calculate Section Progress
```python
def calculate_section_progress(sections):
    """Calculate completion status for each section."""
    progress = []

    for section in sections:
        total = len(section["tasks"])
        completed = sum(1 for t in section["tasks"] if t["completed"])

        if completed == total:
            status = "COMPLETE"
        elif completed > 0:
            status = "IN_PROGRESS"
        else:
            status = "NOT_STARTED"

        progress.append({
            "number": section["number"],
            "name": section["name"],
            "status": status,
            "completed": completed,
            "total": total,
            "percentage": (completed / total * 100) if total > 0 else 0
        })

    return progress
```

#### 3D. Display Current State
```
📍 CURRENT STATE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Overall Progress: 12/40 tasks (30%)

✅ Section 1: Planning (8/8 tasks) - COMPLETE
✅ Section 2: Setup (4/4 tasks) - COMPLETE
🔄 Section 3: Implementation (0/16 tasks) - IN PROGRESS
   ├─ Next: Task 13 - "Implement scoring logic"
   └─ Remaining: 16 tasks in this section
⬜ Section 4: Testing (0/7 tasks) - NOT STARTED
⬜ Section 5: Deployment (0/5 tasks) - NOT STARTED

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

#### 3E. Prompt User
```
Ready to continue Section 3: Implementation?

Options:
1. Continue from Task 13 (recommended)
2. Review completed work first
3. Jump to different section
4. Exit and save progress

Your choice:
```

### Success Criteria
- ✅ Sections extracted from tasks file
- ✅ Current section identified
- ✅ Next uncompleted task found
- ✅ Progress displayed clearly
- ✅ User prompted for next action

---

## Step 4: Execute Work with Continuous Tracking

### Purpose
Execute work systematically with section-by-section bulk-completion.

### Implementation Pattern

**For each section** (repeat until all sections complete):

#### 4A. Show Section Overview
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION 3: IMPLEMENTATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Goal: Build core functionality for lead scoring and qualification

Tasks in this section: 13-28 (16 tasks total)
Estimated time: 3-4 hours

Uncompleted tasks:
  [ ] Task 13: Implement scoring logic
  [ ] Task 14: Create validation rules
  [ ] Task 15: Build API endpoints
  [ ] Task 16: Setup database models
  ... (show all 16 tasks)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Starting execution...
```

#### 4B. Execute Tasks Sequentially
```python
# For each task in section
for task in section["tasks"]:
    if task["completed"]:
        continue  # Skip already completed

    print(f"\n{'='*60}")
    print(f"Task {task_num}: {task['text']}")
    print(f"{'='*60}\n")

    # Execute work for this task
    # (write code, create files, run commands, etc.)

    # Show completion
    print(f"\n✅ Task {task_num} complete!\n")

    # Optional: Checkpoint for large sections
    if (task_num % 5 == 0) and (remaining > 5):
        offer_checkpoint()
```

#### 4C. Adaptive Checkpointing (for large sections)
```python
def offer_checkpoint(section, current_task, total_tasks):
    """
    Offer bulk-complete checkpoint for large sections.
    Only used when section has >15 tasks.
    """
    print(f"\n{'─'*60}")
    print(f"Checkpoint: {current_task}/{total_tasks} tasks complete in this section")
    print(f"{'─'*60}")
    print(f"\nOptions:")
    print(f"1. Continue to next task (recommended)")
    print(f"2. Bulk-complete tasks 1-{current_task} now")
    print(f"3. Pause and save progress")
    print(f"\nYour choice: ")

    # If user chooses option 2:
    # Run bulk-complete --tasks 1-{current_task}
```

#### 4D. Section Completion Checkpoint
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION 3: IMPLEMENTATION - COMPLETE! 🎉
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

All tasks in this section executed successfully!

Completed:
  ✅ Task 13: Implement scoring logic
  ✅ Task 14: Create validation rules
  ✅ Task 15: Build API endpoints
  ... (all 16 tasks)

Ready to bulk-complete Section 3?

What this does:
  ✅ Marks tasks 13-28 as [x] in steps.md
  ✅ Updates progress from 30% → 70%
  ✅ Validates by re-reading file
  ✅ Shows before/after evidence

Type 'yes' to proceed, or 'review' to check work first.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

#### 4E. Execute Bulk-Complete
```bash
# User confirms → Execute script
python 00-system/skills/bulk-complete/scripts/bulk-complete.py \
  --project 05-lead-qualification \
  --section 3 \
  --no-confirm
```

**Script Output**:
```
Bulk Task Completion Tool V2.0 (steps.md + tasks.md support)
============================================================

[INFO] Using task file: steps.md
Project: 05-lead-qualification
Tasks: 24 uncompleted, 16 completed (Total: 40)

[MODE] Complete 16 uncompleted tasks in Section/Phase 3

[AUTO-CONFIRM] Proceeding without confirmation (--no-confirm flag)

[CONFIRM] Will mark 16 tasks as complete:
  [x] Task 13: Implement scoring logic
  [x] Task 14: Create validation rules
  ... (all 16 tasks)

[SUCCESS] Successfully completed 16 tasks!
Updated: 32/40 tasks now complete (80%)
✅ VALIDATED: Re-read file shows 8 uncompleted, 32 completed
File: 02-projects/05-lead-qualification/01-planning/steps.md
```

#### 4F. Display Updated Progress
```
✅ Section 3 bulk-complete successful!

Updated Progress: [████████░░] 80% (32/40 tasks)

Before: 16/40 (40%)
After:  32/40 (80%)
Change: +16 tasks ✅

Completed sections:
  ✅ Section 1: Planning (8 tasks)
  ✅ Section 2: Setup (4 tasks)
  ✅ Section 3: Implementation (16 tasks) ← JUST COMPLETED

Remaining sections:
  ⬜ Section 4: Testing (7 tasks)
  ⬜ Section 5: Deployment (5 tasks)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Continue to Section 4: Testing, or pause for today?
```

#### 4G. User Decision Point
```python
# Ask user what to do next
user_choice = input("Continue, pause, or review? ")

if user_choice.lower() in ["continue", "next", "yes"]:
    # Move to next section
    current_section += 1
    goto_step_4a()  # Repeat for Section 4

elif user_choice.lower() in ["pause", "done", "stop"]:
    # Trigger pause handling (Step 6)
    handle_partial_completion()

elif user_choice.lower() in ["review", "check"]:
    # Show completed work for review
    display_completed_work(section=3)
    # Then ask again: continue or pause?
```

### Success Criteria
- ✅ Section overview displayed
- ✅ All tasks in section executed
- ✅ bulk-complete-tasks.py executed successfully
- ✅ Validation output shown (before/after)
- ✅ Updated progress displayed
- ✅ User prompted for next action

---

## Step 5: Incremental Progress Updates

### Purpose
Show continuous progress updates after each section/checkpoint.

### Implementation

#### 5A. Progress Bar Visualization
```python
def display_progress_bar(completed, total):
    """Display visual progress bar."""
    percentage = (completed / total * 100) if total > 0 else 0
    bar_length = 40
    filled = int(bar_length * completed / total)
    bar = '█' * filled + '░' * (bar_length - filled)

    print(f"\nProgress: [{bar}] {percentage:.1f}% ({completed}/{total} tasks)\n")
```

**Output**:
```
Progress: [████████████████████░░░░░░░░░░░░] 80% (32/40 tasks)
```

#### 5B. Section Summary
```python
def display_section_summary(sections):
    """Show completion status for all sections."""
    print("Completed:")
    for section in sections:
        if all(t["completed"] for t in section["tasks"]):
            task_count = len(section["tasks"])
            print(f"  ✅ Section {section['number']}: {section['name']} ({task_count} tasks)")

    print("\nRemaining:")
    for section in sections:
        if not all(t["completed"] for t in section["tasks"]):
            uncompleted = sum(1 for t in section["tasks"] if not t["completed"])
            print(f"  ⬜ Section {section['number']}: {section['name']} ({uncompleted} tasks)")
```

**Output**:
```
Completed:
  ✅ Section 1: Planning (8 tasks)
  ✅ Section 2: Setup (4 tasks)
  ✅ Section 3: Implementation (16 tasks)

Remaining:
  ⬜ Section 4: Testing (7 tasks)
  ⬜ Section 5: Deployment (5 tasks)
```

#### 5C. Next Steps Prompt
```
Options:
1. Continue to Section 4: Testing (7 tasks, ~1-2 hours)
2. Pause and save progress (will resume at Section 4 next time)
3. Review completed work (see outputs from Sections 1-3)
4. Jump to different section (advanced)

Your choice:
```

### Success Criteria
- ✅ Progress bar displayed after each section
- ✅ Section summary shows completed vs remaining
- ✅ Clear next steps presented
- ✅ User chooses next action

---

## Step 6: Handle Partial Completion

### Purpose
Gracefully handle pause/resume when user stops mid-project.

### Implementation

#### 6A. Detect Pause Request
```python
# User says: "pause", "done", "stop", "save progress"
if user_wants_to_pause():
    handle_partial_completion()
```

#### 6B. Offer Task Completion Options
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PAUSING SESSION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Current progress: 25/40 tasks (62.5%)

You're in the middle of Section 3 (completed 9/16 tasks).

Do you want to mark any completed tasks before pausing?

Options:
1. Bulk-complete Section 3 fully (if all work done)
2. Bulk-complete specific tasks (e.g., "13-21" for tasks 13-21)
3. Leave as-is (resume exactly here next time)

Your choice:
```

#### 6C. Execute Partial Bulk-Complete (if requested)
```bash
# Example: User completed tasks 13-21 but not full section
python 00-system/skills/bulk-complete/scripts/bulk-complete.py \
  --project 05-lead-qualification \
  --tasks 13-21 \
  --no-confirm
```

**Output**:
```
[INFO] Using task file: steps.md
[MODE] Complete 9 specific tasks: [13, 14, 15, 16, 17, 18, 19, 20, 21]

[SUCCESS] Successfully completed 9 tasks!
Updated: 25/40 tasks now complete (62.5%)
✅ VALIDATED: Re-read file shows 15 uncompleted, 25 completed
```

#### 6D. Save State and Trigger close-session
```
✅ Progress saved!

Updated status:
  Progress: 25/40 tasks (62.5%)
  Current section: Section 3 (9/16 complete)
  Next task: Task 22 - "Build validation UI"

Triggering close-session to save session report...

[Execute close-session skill]
```

#### 6E. close-session Integration
```python
# close-session will:
# 1. Read current task state (already up-to-date from bulk-complete)
# 2. Offer additional manual completion (user can decline)
# 3. Create session report with progress summary
# 4. Save project state to memory
```

**close-session Output**:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SESSION COMPLETE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Project: 05-lead-qualification
Progress: 25/40 tasks (62.5%)

Work completed this session:
  ✅ Section 1: Planning (8 tasks)
  ✅ Section 2: Setup (4 tasks)
  🔄 Section 3: Implementation (9/16 tasks)

Next session will resume at:
  Section 3, Task 22 - "Build validation UI"

Session report saved to:
  01-memory/session-reports/2025-01-22-execute-project.md

See you next time! 👋
```

### Success Criteria
- ✅ Pause request detected
- ✅ Partial task completion offered
- ✅ bulk-complete executed (if requested)
- ✅ Progress validated and saved
- ✅ close-session triggered
- ✅ Next session resumption point clear

---

## Step 7: Project Completion

### Purpose
Finalize project when all sections complete.

### Implementation

#### 7A. Detect Full Completion
```python
def is_project_complete(sections):
    """Check if all sections have all tasks complete."""
    for section in sections:
        if not all(t["completed"] for t in section["tasks"]):
            return False
    return True

# After last section bulk-complete
if is_project_complete(sections):
    handle_project_completion()
```

#### 7B. Display Completion Summary
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎉 PROJECT COMPLETE! 🎉
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Project: Lead Qualification Workflow
ID: 05-lead-qualification

All sections executed successfully:
  ✅ Section 1: Planning (8 tasks)
  ✅ Section 2: Setup (4 tasks)
  ✅ Section 3: Implementation (16 tasks)
  ✅ Section 4: Testing (7 tasks)
  ✅ Section 5: Deployment (5 tasks)

Total: 40/40 tasks (100%) ✅

Created: 2025-01-15
Completed: 2025-01-22
Duration: 7 days

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

#### 7C. Final Bulk-Complete (if needed)
```python
# Check if any tasks still unchecked (edge case)
uncompleted = count_uncompleted_tasks()

if uncompleted > 0:
    print(f"\n{uncompleted} tasks still unchecked. Running final bulk-complete...\n")

    # Complete all remaining
    run_bulk_complete(
        project_id=project_id,
        mode="--all",
        no_confirm=True
    )
```

**Script Output**:
```
[INFO] Using task file: steps.md
[MODE] Complete ALL 2 uncompleted tasks

[SUCCESS] Successfully completed 2 tasks!
Updated: 40/40 tasks now complete (100%)
✅ VALIDATED: Re-read file shows 0 uncompleted, 40 completed
```

#### 7D. Update Project Metadata
```python
# Update overview.md frontmatter
def update_project_status(project_path):
    """Mark project as COMPLETE in overview.md."""
    overview_path = project_path / "01-planning/overview.md"
    content = overview_path.read_text(encoding='utf-8')

    # Update YAML frontmatter
    updated = re.sub(
        r'status:\s*IN_PROGRESS',
        'status: COMPLETE',
        content
    )

    # Update last_worked date
    from datetime import datetime
    today = datetime.now().strftime('%Y-%m-%d')
    updated = re.sub(
        r'last_worked:\s*\d{4}-\d{2}-\d{2}',
        f'last_worked: {today}',
        updated
    )

    overview_path.write_text(updated, encoding='utf-8')

    print(f"✅ Project status updated to COMPLETE")
    print(f"✅ Last worked date: {today}")
```

#### 7E. Suggest Next Steps
```
Ready to finalize project?

Actions:
  ✅ Mark all tasks complete (done)
  ✅ Update project status to COMPLETE (done)
  ⬜ Archive project (recommended)
  ⬜ Save session with close-session

Options:
1. Archive now (use 'archive-project' skill)
2. Keep in active projects for reference
3. Save session and decide later

Your choice:
```

#### 7F. Trigger close-session
```bash
python 00-system/core/nexus-loader.py --skill close-session
```
Then execute close-session workflow per SKILL.md

**close-session Output**:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SESSION COMPLETE - PROJECT FINISHED! 🎉
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Project: 05-lead-qualification
Status: COMPLETE ✅
Progress: 40/40 tasks (100%)

This project is now complete and ready to archive!

Outputs created:
  📄 Lead scoring algorithm (03-working/scoring.py)
  📄 API endpoints (03-working/api/)
  📄 Documentation (04-outputs/README.md)
  📄 Test suite (03-working/tests/)

Next steps:
  - Use 'archive-project 05' to move to archive
  - Or keep in active projects for reference

Session report saved to:
  01-memory/session-reports/2025-01-22-project-complete.md

Congratulations! 🎉
```

### Success Criteria
- ✅ All sections marked complete
- ✅ Final bulk-complete executed (if needed)
- ✅ Project metadata updated (status: COMPLETE)
- ✅ Completion summary displayed
- ✅ Next steps suggested (archive)
- ✅ close-session triggered
- ✅ User celebrated! 🎉

---

## Error Handling

### Common Errors and Solutions

#### Error: Tasks file not found
```
[ERROR] No task file found in 05-lead-qualification
[INFO] Expected: steps.md or tasks.md in 01-planning/

Solution:
1. Check project structure with 'validate-system'
2. If missing, create manually or use 'create-project' skill
```

#### Error: No uncompleted tasks
```
[OK] All tasks already complete in 05-lead-qualification!
[INFO] 40/40 tasks are checked

Solution:
- Display message: "This project is already complete!"
- Suggest: "Use 'archive-project' to move to archive"
- Offer: Review completed work or outputs
```

#### Error: Invalid task format
```
[ERROR] No tasks found with checkbox format

Expected format:
  - [ ] Task description
  - [x] Completed task

Found:
  * Task description (bullet list, not checkbox)
  1. Task description (numbered list, not checkbox)

Solution:
1. Show format example
2. Offer to fix formatting automatically
3. Or suggest manual fix in steps.md
```

#### Error: bulk-complete-tasks.py fails
```
[ERROR] Failed to update tasks: Permission denied

Solution:
1. Fallback to manual Edit tool
2. Log error for debugging
3. Show user what needs to be marked
4. Offer manual checkbox completion
```

#### Error: Validation mismatch
```
[WARNING] Validation read failed: File locked

Solution:
1. Retry validation read (3 attempts)
2. If still fails, trust write operation
3. Log warning but continue
4. User can verify manually
```

---

## Best Practices

### DO
- ✅ Always validate after bulk-complete (re-read file)
- ✅ Show before/after progress evidence
- ✅ Offer pause points after each section
- ✅ Display clear visual progress (bars, percentages)
- ✅ Auto-detect task file (steps.md vs tasks.md)
- ✅ Use --no-confirm for bulk-complete (AI automation)
- ✅ Trigger close-session at appropriate times
- ✅ Celebrate completion! 🎉

### DON'T
- ❌ Bulk-complete tasks before work is actually done
- ❌ Skip validation step (always verify)
- ❌ Assume task file name (auto-detect steps.md vs tasks.md)
- ❌ Overwhelm user (use adaptive granularity)
- ❌ Continue after errors (handle gracefully)
- ❌ Forget to update project metadata (status: COMPLETE)
- ❌ Skip close-session (always save state)

---

## Performance Notes

### Efficiency
- **Bulk-complete**: Completes 100 tasks in <1 second
- **Single file operation**: Read → Replace → Write
- **Validation**: Re-read adds ~100ms, worth it for evidence

### Scalability
- **Small projects** (≤15 tasks): Task-by-task, real-time
- **Medium projects** (16-30 tasks): Section-based
- **Large projects** (>30 tasks): Section + periodic checkpoints
- **Very large projects** (>100 tasks): Checkpoint every 10 tasks

---

**Version**: 1.0
**Last Updated**: 2025-01-22
**Status**: Production Ready
