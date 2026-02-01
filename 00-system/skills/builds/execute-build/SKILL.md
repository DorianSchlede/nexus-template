---
name: execute-build
description: "continue [build], resume, work on, check progress, execute build, build [ID/name]."
---

# Execute Build

Execute build work systematically with progress tracking.

## Workflow

### 1. Load Context

```bash
nexus-load --build [ID]
```

Read files from `_usage.recommended_reads`.

### 2. Show Status

```
----------------------------------
BUILD: [Name]
----------------------------------
Progress: [X]/[Y] tasks ([Z]%)
Current: Section [N] - [Name]
Next: [Task description]
----------------------------------
```

### 3. Find Current State

Parse steps.md for:
- First uncompleted section (`## Section/Phase N`)
- Next uncompleted task (`- [ ]`)

### 4. Execute Section

Work through tasks in current section. Show after each:

```
[OK] Task [N] complete!
```

### 5. Bulk-Complete Section

When section done:

```bash
nexus-bulk-complete --build [ID] --section [N] --no-confirm
```

### 6. Update Resume State

**CRITICAL**: After bulk-complete succeeds:

```bash
nexus-update-resume --build [ID] --section [N+1] --completed [total]
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
| `--build ID` | Build ID (e.g., "05" or "05-name") |
| `--all` | Complete all tasks |
| `--section N` | Complete section N |
| `--tasks 1-5,7` | Specific tasks |
| `--no-confirm` | Skip prompt (**required for AI**) |

**Examples**:
```bash
# Complete section 3
nexus-bulk-complete --build 05 --section 3 --no-confirm

# Complete specific tasks
nexus-bulk-complete --build 05 --tasks 1-10,15 --no-confirm

# Complete all
nexus-bulk-complete --build 05 --all --no-confirm
```

### update-resume.py

| Flag | Purpose |
|------|---------|
| `--build ID` | Build ID |
| `--section N` | **NEXT** section number |
| `--completed N` | Total completed count |
| `--task N` | Current task (optional) |
| `--phase X` | Phase name (optional) |

**Example**:
```bash
# After completing Section 3 (28 total tasks now done)
nexus-update-resume --build 05 --section 4 --completed 28
```

---

## Resume Context Updates (CRITICAL)

### Auto-Synced by Hooks (don't manually update)

These fields are automatically synced by PreCompact hook:
- `session_ids` - List of all sessions that touched this build
- `last_updated` - Timestamp of last activity
- `total_tasks` - Checkbox count from 04-steps.md
- `tasks_completed` - Completed checkbox count
- `current_section` - First section with unchecked tasks
- `current_task` - Position of first unchecked task
- `current_phase` - "planning" or "execution"
- `next_action` - "plan-build" or "execute-build"

### Claude Must Update

After completing a section, update these in resume-context.md:

1. **files_to_load** - Update to include relevant working files:
   ```yaml
   files_to_load:
     - "01-planning/04-steps.md"
     - "03-working/current-file.py"  # Add working files as created
   ```

2. **Progress Summary** - Update with session accomplishments:
   ```markdown
   ### Latest Session (YYYY-MM-DD)

   **Completed this session:**
   - [x] Section N tasks
   - [x] Created working file X

   **Key decisions:**
   - Decision made and rationale

   **Next steps:**
   1. Next section/task to do
   2. Following task
   ```

---

## Key Rules (CRITICAL)

1. **Section-based execution**: Work section by section, not task by task (unless ≤15 total tasks)

2. **Bulk-complete after sections**: NEVER mark tasks manually with Edit tool

3. **Update resume immediately**: After EVERY bulk-complete, update resume-context.md Progress Summary

4. **Resume points to NEXT**: `current_section` = next section to work on, NOT the one just completed

5. **Update files_to_load**: Add working files created during execution for context on resume

---

## Integration

### From plan-build

```
plan-build completes → User chooses "Execute now"
→ Status updates: PLANNING → IN_PROGRESS
→ execute-build loads immediately (same session)
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
----------------------------------
SECTION [N]: [NAME] - COMPLETE!
----------------------------------
Tasks: [X]/[X]
Progress: [████████░░] [Y]%

Continue to Section [N+1], or pause?
```

### Build Complete

```
----------------------------------
BUILD COMPLETE!
----------------------------------
All [X] tasks done (100%)
Status → COMPLETE

Use 'archive-build' to archive.
```
