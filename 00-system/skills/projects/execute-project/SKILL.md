---
name: execute-project
description: "The ONLY way to work on existing projects. Load when user mentions ANY project by name, ID, or number. Triggers: continue, resume, work on, check progress, status, execute project. Provides: task tracking, bulk-complete, section-based execution, resume state management."
---

# Execute Project

Execute project work systematically with progress tracking.

## Workflow

### 1. Load Context

```bash
python 00-system/core/nexus-loader.py --project [ID]
```

Read files from `_usage.recommended_reads`.

### 2. Show Status

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PROJECT: [Name]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Progress: [X]/[Y] tasks ([Z]%)
Current: Section [N] - [Name]
Next: [Task description]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 3. Find Current State

Parse steps.md for:
- First uncompleted section (`## Section/Phase N`)
- Next uncompleted task (`- [ ]`)

### 4. Execute Section

Work through tasks in current section. Show after each:

```
✅ Task [N] complete!
```

### 5. Bulk-Complete Section

When section done:

```bash
python 00-system/skills/projects/execute-project/scripts/bulk-complete.py \
  --project [ID] --section [N] --no-confirm
```

### 6. Update Resume State

**CRITICAL**: After bulk-complete succeeds:

```bash
python 00-system/skills/projects/execute-project/scripts/update-resume.py \
  --project [ID] --section [N+1] --completed [total]
```

Key: Set `current_section` to **NEXT** section (not completed one).

### 7. Continue or Complete

- More sections → repeat from step 4
- User says "pause" → offer partial bulk-complete, trigger close-session
- 100% done → update status to COMPLETE, suggest archive

---

## Scripts Reference

### bulk-complete.py

| Flag | Purpose |
|------|---------|
| `--project ID` | Project ID (e.g., "05" or "05-name") |
| `--all` | Complete all tasks |
| `--section N` | Complete section N |
| `--tasks 1-5,7` | Specific tasks |
| `--no-confirm` | Skip prompt (**required for AI**) |

**Examples**:
```bash
# Complete section 3
python .../bulk-complete.py --project 05 --section 3 --no-confirm

# Complete specific tasks
python .../bulk-complete.py --project 05 --tasks 1-10,15 --no-confirm

# Complete all
python .../bulk-complete.py --project 05 --all --no-confirm
```

### update-resume.py

| Flag | Purpose |
|------|---------|
| `--project ID` | Project ID |
| `--section N` | **NEXT** section number |
| `--completed N` | Total completed count |
| `--task N` | Current task (optional) |
| `--phase X` | Phase name (optional) |

**Example**:
```bash
# After completing Section 3 (28 total tasks now done)
python .../update-resume.py --project 05 --section 4 --completed 28
```

---

## Key Rules (CRITICAL)

1. **Section-based execution**: Work section by section, not task by task (unless ≤15 total tasks)

2. **Bulk-complete after sections**: NEVER mark tasks manually with Edit tool

3. **Update resume immediately**: After EVERY bulk-complete, update resume-context.md

4. **Resume points to NEXT**: `current_section` = next section to work on, NOT the one just completed

---

## Integration

### From plan-project

```
plan-project completes → User chooses "Execute now"
→ Status updates: PLANNING → IN_PROGRESS
→ execute-project loads immediately (same session)
```

### To close-session

```
User says "pause" or "done for today"
→ Offer partial bulk-complete
→ Trigger close-session skill
```

---

## Error Handling

| Issue | Solution |
|-------|----------|
| No task file | Run `validate-system` skill |
| All tasks done | Display "100%!", offer COMPLETE status |
| Bad checkbox format | Need `- [ ] Task` format |
| Script fails | Fallback to Edit tool, log error |

---

## Display Patterns

### Section Complete

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECTION [N]: [NAME] - COMPLETE!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Tasks: [X]/[X]
Progress: [████████░░] [Y]%

Continue to Section [N+1], or pause?
```

### Project Complete

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PROJECT COMPLETE!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
All [X] tasks done (100%)
Status → COMPLETE

Use 'archive-project' to archive.
```
