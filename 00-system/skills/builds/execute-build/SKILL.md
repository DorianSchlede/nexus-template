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
- 100% done → update status to COMPLETE (see below), suggest archive

### 8. Update Build Status (When Complete)

**CRITICAL**: Use Edit tool to update `status:` in `01-planning/01-overview.md`.

**Valid statuses ONLY**: `PLANNING`, `IN_PROGRESS`, `ACTIVE`, `COMPLETE`, `ARCHIVED`

```yaml
# In 01-overview.md frontmatter, change:
status: IN_PROGRESS
# To:
status: COMPLETE
```

**NEVER use**: `EXECUTION`, `DONE`, `FINISHED`, or any other value. These are invalid and will cause warnings.

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

After completing work, update these in resume-context.md:

1. **continue_at** - Specific pointer for next agent:
   ```yaml
   continue_at: "03-working/api.py:142"  # or "Phase 2, Task 3"
   ```

2. **blockers** - List any blockers:
   ```yaml
   blockers:
     - "Waiting for user decision on auth method"
   ```

3. **files_to_load** - Add working files with reason comments:
   ```yaml
   files_to_load:
     - "01-planning/04-steps.md"         # Execution checklist
     - "02-resources/decisions.md"       # Key decisions made
     - "03-working/current-file.py"      # Active work in progress
   ```

**Pattern**: Create context files → Add to files_to_load:
- Made a decision? → Write to `02-resources/decisions.md` → Add to list
- Found a gotcha? → Write to `03-working/session-notes.md` → Add to list
- Hook AUTO-LOADS these files in COMPACT mode

4. **Context for Next Agent** - Prose that POINTS to files:
   ```markdown
   ### Latest Session (YYYY-MM-DD)

   **Completed this session:**
   - [x] Section N tasks
   - [x] Created working file X

   **Key files:**
   - See `decisions.md` for rationale on API design
   - See `session-notes.md` for gotchas discovered

   **Next steps:**
   1. Continue at `continue_at` location
   2. Check `blockers` if any
   ```

> **Philosophy**: Don't capture context in prose. Write it to FILES, add to `files_to_load`. Prose just POINTS to files.

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
