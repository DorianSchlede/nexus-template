# Adaptive Granularity: Smart Progress Tracking

**Purpose**: Automatically adjust tracking granularity based on project size and structure

**Audience**: AI agents implementing execute-project skill

**Version**: 1.0

---

## Overview

Not all projects should be tracked the same way:
- **Small projects** (≤15 tasks): Task-by-task updates feel natural
- **Large projects** (>30 tasks): Section-based with checkpoints prevents overwhelming
- **Unstructured projects** (no sections): Periodic checkpoints work best

**Adaptive granularity** = Auto-detect project characteristics → Choose optimal tracking pattern

---

## Detection Algorithm

### Step 1: Analyze Project Structure

```python
def analyze_project_structure(project_path):
    """
    Analyze project to determine optimal tracking granularity.

    Returns:
        {
            "mode": str,              # "task-by-task", "section-based", "checkpoint", "section-with-checkpoints"
            "total_tasks": int,
            "has_sections": bool,
            "sections": list,
            "checkpoint_interval": int  # (if applicable)
        }
    """
    # Load task file
    task_file = find_task_file(project_path)
    content = task_file.read_text(encoding='utf-8')

    # Extract structure
    all_tasks = extract_tasks(content)
    sections = extract_sections(content)

    total_tasks = len(all_tasks)
    has_sections = len(sections) > 0

    # Determine mode
    mode, checkpoint_interval = determine_mode(
        total_tasks,
        has_sections,
        sections
    )

    return {
        "mode": mode,
        "total_tasks": total_tasks,
        "has_sections": has_sections,
        "sections": sections,
        "checkpoint_interval": checkpoint_interval
    }
```

---

### Step 2: Determine Tracking Mode

```python
def determine_mode(total_tasks, has_sections, sections):
    """
    Choose optimal tracking mode based on project characteristics.

    Returns:
        (mode, checkpoint_interval)
    """
    # Small projects: Task-by-task
    if total_tasks <= 15:
        return ("task-by-task", None)

    # Medium projects with sections: Section-based
    if 16 <= total_tasks <= 30 and has_sections:
        return ("section-based", None)

    # Large projects with sections: Section + checkpoints
    if total_tasks > 30 and has_sections:
        # Checkpoint interval based on average section size
        avg_section_size = total_tasks / len(sections) if sections else 10

        if avg_section_size > 15:
            # Large sections: checkpoint every 5-7 tasks
            checkpoint_interval = 5 if avg_section_size > 20 else 7
            return ("section-with-checkpoints", checkpoint_interval)
        else:
            # Smaller sections: just section-based
            return ("section-based", None)

    # Unstructured projects (no sections): Periodic checkpoints
    if not has_sections:
        # Checkpoint every 10 tasks for unstructured
        return ("checkpoint", 10)

    # Default: Section-based
    return ("section-based", None)
```

---

## Tracking Modes Explained

### Mode 1: Task-by-Task

**When**: Small projects (≤15 tasks)

**Pattern**: Update progress after EVERY task

**Example Workflow**:
```python
# Project with 12 tasks total

for task_num, task in enumerate(tasks, 1):
    # Execute task
    execute_task(task)

    # Show immediate progress
    print(f"\n✅ Task {task_num} complete!")
    print(f"Progress: {task_num}/12 ({task_num/12*100:.1f}%)\n")

    # Offer bulk-complete every 3-5 tasks (optional)
    if task_num % 5 == 0:
        offer_mini_checkpoint(task_num)

# At end: bulk-complete all
print("All 12 tasks complete! Bulk-completing...")
run_bulk_complete_all()
```

**Benefits**:
- ✅ High visibility (see every step)
- ✅ Fast feedback loop
- ✅ Natural for small scope

**Drawbacks**:
- ❌ Too granular for large projects
- ❌ Would overwhelm user with 100+ updates

**Example Project**:
```
Project: Create Logo Design
- 8 tasks total
- No sections

Mode: Task-by-task
- Execute task → Show progress → Next task
- Bulk-complete all at end
```

---

### Mode 2: Section-Based

**When**: Medium projects (16-30 tasks) with clear sections

**Pattern**: Execute entire section → Bulk-complete section

**Example Workflow**:
```python
# Project with 24 tasks across 4 sections (6 tasks each)

for section in sections:
    # Show section overview
    display_section_overview(section)

    # Execute all tasks in section
    for task in section["tasks"]:
        execute_task(task)
        print(f"✅ Task {task['number']} complete")

    # Bulk-complete entire section
    print(f"\n{'='*60}")
    print(f"Section {section['number']} complete! Bulk-completing...")
    run_bulk_complete_section(section['number'])

    # Show updated progress
    display_overall_progress()

    # Ask: continue or pause?
    next_action = prompt_user("Continue to next section?")
```

**Benefits**:
- ✅ Natural checkpoints (sections)
- ✅ Manageable updates (4-6 times per project, not 30+)
- ✅ Clear progress milestones

**Drawbacks**:
- ❌ If sections are huge (20+ tasks), still overwhelming
- ❌ Requires well-structured task file

**Example Project**:
```
Project: Build API Integration
- 24 tasks total
- 4 sections (Planning, Setup, Implementation, Testing)

Mode: Section-based
- Execute Section 1 → Bulk-complete Section 1
- Execute Section 2 → Bulk-complete Section 2
- etc.
```

---

### Mode 3: Section-with-Checkpoints

**When**: Large projects (>30 tasks) with sections, where sections are >15 tasks each

**Pattern**: Execute section with periodic checkpoints → Final section bulk-complete

**Example Workflow**:
```python
# Project with 80 tasks
# Section 3 has 25 tasks → Use checkpoints

checkpoint_interval = 5  # Every 5 tasks

for task_idx, task in enumerate(section["tasks"], 1):
    # Execute task
    execute_task(task)
    print(f"✅ Task {task['number']} complete")

    # Checkpoint every 5 tasks
    if task_idx % checkpoint_interval == 0 and task_idx < len(section["tasks"]):
        print(f"\n{'─'*60}")
        print(f"Checkpoint: {task_idx}/{len(section['tasks'])} tasks in this section")
        print(f"{'─'*60}")
        print("Options:")
        print("1. Continue to next task")
        print(f"2. Bulk-complete tasks 1-{task_idx} now")
        print("3. Pause and save progress")

        user_choice = input("Your choice: ")

        if user_choice == "2":
            # Bulk-complete up to checkpoint
            first_task_num = section["tasks"][0]["number"]
            last_task_num = section["tasks"][task_idx-1]["number"]
            run_bulk_complete_tasks(f"{first_task_num}-{last_task_num}")

# After all tasks in section
print(f"\nSection {section['number']} complete!")
run_bulk_complete_section(section['number'])
```

**Benefits**:
- ✅ Prevents overwhelming user with 25+ tasks at once
- ✅ Offers pause points mid-section
- ✅ Still maintains section structure

**Drawbacks**:
- ❌ More complex (checkpoints + section complete)
- ❌ User sees more prompts

**Example Project**:
```
Project: Full-Stack Application
- 80 tasks total
- 5 sections
  - Section 3: Backend API (25 tasks) ← Use checkpoints

Mode: Section-with-checkpoints
- Execute tasks 1-5 → Checkpoint offer
- Execute tasks 6-10 → Checkpoint offer
- Execute tasks 11-15 → Checkpoint offer
- Execute tasks 16-20 → Checkpoint offer
- Execute tasks 21-25 → Checkpoint offer
- Bulk-complete Section 3 (all 25 tasks)
```

---

### Mode 4: Checkpoint (Unstructured)

**When**: Projects without sections (no `## Section` headers)

**Pattern**: Execute tasks → Checkpoint every N tasks

**Example Workflow**:
```python
# Project with 40 tasks, no sections
checkpoint_interval = 10

for task_idx, task in enumerate(tasks, 1):
    # Execute task
    execute_task(task)
    print(f"✅ Task {task_idx} complete")

    # Checkpoint every 10 tasks
    if task_idx % checkpoint_interval == 0:
        print(f"\n{'─'*60}")
        print(f"Checkpoint: {task_idx}/40 tasks complete ({task_idx/40*100:.0f}%)")
        print(f"{'─'*60}")
        print("Options:")
        print("1. Continue")
        print(f"2. Bulk-complete tasks 1-{task_idx}")
        print("3. Pause")

        # Handle user choice...

# At end: bulk-complete all
run_bulk_complete_all()
```

**Benefits**:
- ✅ Works for any project (no structure required)
- ✅ Regular pause points
- ✅ Prevents overwhelming with huge task list

**Drawbacks**:
- ❌ Arbitrary checkpoints (no semantic meaning)
- ❌ Encourages better structure for future projects

**Example Project**:
```
Project: Miscellaneous Tasks Collection
- 40 tasks total
- No sections (flat list)

Mode: Checkpoint
- Execute tasks 1-10 → Checkpoint
- Execute tasks 11-20 → Checkpoint
- Execute tasks 21-30 → Checkpoint
- Execute tasks 31-40 → Checkpoint
- Bulk-complete all
```

---

## Decision Tree

```
                      ┌─────────────────┐
                      │ Analyze Project │
                      └────────┬────────┘
                               │
                    ┌──────────▼──────────┐
                    │ Count Total Tasks   │
                    └──────────┬──────────┘
                               │
                  ┌────────────▼────────────┐
                  │ Total Tasks ≤ 15?      │
                  └──┬──────────────────┬───┘
                     │ YES              │ NO
                     │                  │
              ┌──────▼──────┐    ┌──────▼──────────┐
              │ Task-by-Task│    │ Has Sections?   │
              └─────────────┘    └──┬──────────┬───┘
                                    │ YES      │ NO
                                    │          │
                          ┌─────────▼─────┐  ┌─▼────────────┐
                          │ Total ≤ 30?   │  │ Checkpoint   │
                          └──┬─────────┬──┘  │ (every 10)   │
                             │ YES     │ NO  └──────────────┘
                             │         │
                  ┌──────────▼───┐  ┌──▼──────────────────┐
                  │ Section-Based│  │ Check Section Size  │
                  └──────────────┘  └──┬──────────────┬───┘
                                       │ Avg ≤ 15     │ Avg > 15
                                       │              │
                            ┌──────────▼───┐  ┌───────▼─────────────┐
                            │ Section-Based│  │ Section + Checkpoint│
                            └──────────────┘  └─────────────────────┘
```

---

## Implementation

### Quick Start Code

```python
def choose_tracking_mode(project_path):
    """
    Auto-detect optimal tracking mode for project.

    Returns:
        str: One of "task-by-task", "section-based", "checkpoint", "section-with-checkpoints"
    """
    # Analyze structure
    analysis = analyze_project_structure(project_path)

    total = analysis["total_tasks"]
    has_sections = analysis["has_sections"]
    sections = analysis["sections"]

    # Small projects
    if total <= 15:
        return "task-by-task"

    # No sections
    if not has_sections:
        return "checkpoint"

    # Medium with sections
    if 16 <= total <= 30:
        return "section-based"

    # Large with sections
    if total > 30:
        # Check average section size
        avg_size = total / len(sections)

        if avg_size > 15:
            return "section-with-checkpoints"
        else:
            return "section-based"

    # Default
    return "section-based"
```

---

### Execute Mode

```python
def execute_with_adaptive_granularity(project_path):
    """Execute project with appropriate tracking mode."""

    # Detect mode
    mode = choose_tracking_mode(project_path)

    # Load structure
    analysis = analyze_project_structure(project_path)

    print(f"[INFO] Project has {analysis['total_tasks']} tasks")
    print(f"[INFO] Using tracking mode: {mode}")
    print()

    # Execute based on mode
    if mode == "task-by-task":
        execute_task_by_task(analysis)

    elif mode == "section-based":
        execute_section_based(analysis)

    elif mode == "section-with-checkpoints":
        execute_section_with_checkpoints(analysis)

    elif mode == "checkpoint":
        execute_checkpoint_based(analysis)
```

---

## User Communication

### Explain Mode to User

**Show mode decision**:
```python
def explain_tracking_mode(mode, total_tasks):
    """Explain to user why this mode was chosen."""

    explanations = {
        "task-by-task": f"This project has {total_tasks} tasks (small). I'll update progress after each task.",

        "section-based": f"This project has {total_tasks} tasks across sections. I'll bulk-complete after each section.",

        "section-with-checkpoints": f"This project has {total_tasks} tasks with large sections. I'll offer checkpoints every 5-7 tasks.",

        "checkpoint": f"This project has {total_tasks} tasks without sections. I'll checkpoint every 10 tasks."
    }

    print(f"[INFO] {explanations[mode]}")
    print()
```

**Example Output**:
```
[INFO] Project has 24 tasks across 4 sections
[INFO] Using tracking mode: section-based
[INFO] I'll bulk-complete after each section.
```

---

## Override Option

**Allow user to override** if they prefer different granularity:

```python
def confirm_tracking_mode(detected_mode, total_tasks):
    """
    Let user confirm or override tracking mode.
    """
    print(f"Detected tracking mode: {detected_mode}")
    print(f"Total tasks: {total_tasks}")
    print()
    print("Is this OK, or would you prefer:")
    print("1. Use detected mode (recommended)")
    print("2. Task-by-task (more granular)")
    print("3. Section-based (coarser)")
    print("4. Just do the work (I'll bulk-complete at end)")

    choice = input("Your choice (1-4): ").strip()

    mode_map = {
        "1": detected_mode,
        "2": "task-by-task",
        "3": "section-based",
        "4": "no-tracking"
    }

    return mode_map.get(choice, detected_mode)
```

---

## Examples by Project Size

### Example 1: Small Project (8 tasks)

**Project**: Create logo design
**Tasks**: 8 total, no sections

**Detected Mode**: Task-by-task

**Workflow**:
```
Executing task 1/8: Brainstorm concepts...
✅ Task 1 complete! Progress: 12.5%

Executing task 2/8: Sketch initial designs...
✅ Task 2 complete! Progress: 25%

... (continue task-by-task)

✅ Task 8 complete! Progress: 100%

Bulk-completing all 8 tasks...
✅ VALIDATED: 8/8 tasks complete
```

---

### Example 2: Medium Project (24 tasks, 4 sections)

**Project**: API Integration
**Tasks**: 24 total across 4 sections (6 each)

**Detected Mode**: Section-based

**Workflow**:
```
Section 1: Planning (6 tasks)
Executing tasks 1-6...
✅ Section 1 complete!

Bulk-completing Section 1...
✅ VALIDATED: 6/24 tasks (25%)

Section 2: Setup (6 tasks)
Executing tasks 7-12...
✅ Section 2 complete!

Bulk-completing Section 2...
✅ VALIDATED: 12/24 tasks (50%)

... (continue section-by-section)
```

---

### Example 3: Large Project (80 tasks, 5 sections, some huge)

**Project**: Full-stack application
**Tasks**: 80 total, Section 3 has 25 tasks

**Detected Mode**: Section-with-checkpoints

**Workflow**:
```
Section 3: Backend API (25 tasks)

Executing tasks 1-5...
─────────────────────────────────────
Checkpoint: 5/25 tasks in this section
─────────────────────────────────────
Options: 1. Continue  2. Bulk-complete 1-5  3. Pause
Your choice: 1

Executing tasks 6-10...
─────────────────────────────────────
Checkpoint: 10/25 tasks in this section
─────────────────────────────────────
Options: ...

... (continue with checkpoints)

✅ All 25 tasks in Section 3 complete!
Bulk-completing Section 3...
✅ VALIDATED: 53/80 tasks (66%)
```

---

### Example 4: Unstructured Project (40 tasks, no sections)

**Project**: Miscellaneous tasks
**Tasks**: 40 total, flat list (no sections)

**Detected Mode**: Checkpoint (every 10)

**Workflow**:
```
Executing tasks 1-10...
─────────────────────────────────────
Checkpoint: 10/40 tasks complete (25%)
─────────────────────────────────────
Options: 1. Continue  2. Bulk-complete 1-10  3. Pause
Your choice: 1

Executing tasks 11-20...
Checkpoint: 20/40 (50%)
...

Executing tasks 31-40...
✅ All 40 tasks complete!

Bulk-completing all tasks...
✅ VALIDATED: 40/40 tasks (100%)
```

---

## Best Practices

### DO

✅ **Explain mode to user**
```python
print(f"[INFO] Using {mode} tracking for this {total}-task project")
```

✅ **Respect detected mode (but allow override)**
```python
if user_wants_override:
    mode = ask_user_preference()
```

✅ **Adjust checkpoint interval dynamically**
```python
# Large sections → smaller checkpoints
if avg_section_size > 20:
    checkpoint_interval = 5
elif avg_section_size > 15:
    checkpoint_interval = 7
else:
    checkpoint_interval = 10
```

✅ **Show progress frequently**
```python
# Every task, checkpoint, or section
display_progress_bar(completed, total)
```

---

### DON'T

❌ **Don't use same mode for all projects**
```python
# WRONG
mode = "section-based"  # Always use this

# RIGHT
mode = choose_tracking_mode(project_path)  # Adaptive
```

❌ **Don't overwhelm user with updates**
```python
# WRONG: Task-by-task for 100-task project
for task in 100_tasks:
    execute_task()
    show_progress()  # 100 updates!

# RIGHT: Use checkpoints
for task in 100_tasks:
    execute_task()
    if task_num % 10 == 0:
        show_checkpoint()  # 10 updates
```

❌ **Don't ignore project structure**
```python
# WRONG: Checkpoints when sections exist
mode = "checkpoint"  # But project HAS sections!

# RIGHT: Use sections
if has_sections:
    mode = "section-based"
```

---

## Summary

**Key Points**:
1. **Auto-detect** project size and structure
2. **Choose mode**: task-by-task, section-based, section-with-checkpoints, or checkpoint
3. **Explain** mode to user
4. **Allow override** if user prefers different granularity
5. **Adjust dynamically** (checkpoint intervals based on section size)

**Decision Factors**:
- Total task count
- Presence of sections
- Average section size
- User preference (if overridden)

**Result**: Optimal user experience regardless of project size!

---

**Version**: 1.0
**Last Updated**: 2025-01-22
**Status**: Production Ready
