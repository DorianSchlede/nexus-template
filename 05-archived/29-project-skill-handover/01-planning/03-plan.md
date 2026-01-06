# Plan: Project Skill Handover

## Phase 1: Handover Flow (COMPLETE)

Replace Step 10-11 in plan-project/SKILL.md with handover decision:
- User chooses "Execute now" -> Load execute-project inline
- User chooses "Defer" -> Trigger close-session

---

## Phase 2: execute-project Consolidation

### Problem Analysis

| Mental Model | Finding |
|--------------|---------|
| **First Principles** | Core need: load -> find task -> do work -> mark done -> save state. Skill is 10x more complex than needed. |
| **Pre-Mortem** | Failure modes: AI never reads references, skill too long to follow, over-engineering |
| **Pareto 80/20** | 20% of content (commands, workflow) delivers 80% of value. References are dead weight. |
| **Force Field** | Driving: context limits, maintenance burden. Restraining: sunk cost, completeness bias. |

### Current State (Before)

```
execute-project/
├── SKILL.md (745 lines)
├── references/
│   ├── workflow.md (987 lines)        <- NEVER LOADED
│   ├── task-tracking.md (851 lines)   <- NEVER LOADED
│   ├── adaptive-granularity.md (731)  <- NEVER LOADED
│   └── resume-update-guide.md (531)   <- NEVER LOADED
└── scripts/
    ├── update_resume_context.py (328)
    └── migrate_resume_to_optimized.py (309)

bulk-complete/
├── SKILL.md (58 lines)
└── scripts/
    └── bulk-complete.py (482 lines)

Total: 5,022 lines across 2 skills
```

### Target State (After)

```
execute-project/
├── SKILL.md (~180 lines)
└── scripts/
    ├── bulk-complete.py (482 lines)  <- MOVED here
    └── update-resume.py (328 lines)  <- RENAMED

Total: ~990 lines in 1 skill
```

### New SKILL.md Structure

1. **Triggers** - When to load (10 lines)
2. **Core Workflow** - 6 steps with commands (60 lines)
3. **Scripts Reference** - bulk-complete + update-resume tables (30 lines)
4. **Key Rules** - 4 critical rules (15 lines)
5. **Integration** - plan-project + close-session (20 lines)
6. **Error Handling** - 4 one-liners (10 lines)
7. **Display Patterns** - 2 key templates (25 lines)

---

## Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Delete references/ | Yes | Never loaded, duplicates SKILL.md |
| Merge bulk-complete | Yes | Only used by execute-project |
| Keep scripts | Yes | Actually executed |
| Rename update script | Yes | Clearer name |
| Delete migrate script | Yes | One-time utility, done |

---

## Files to Delete

1. `execute-project/references/workflow.md`
2. `execute-project/references/task-tracking.md`
3. `execute-project/references/adaptive-granularity.md`
4. `execute-project/references/resume-update-guide.md`
5. `execute-project/scripts/migrate_resume_to_optimized.py`
6. `bulk-complete/SKILL.md`
7. `bulk-complete/scripts/bulk-complete.py` (after move)
8. `bulk-complete/` folder

## Files to Create/Move

1. Move `bulk-complete.py` -> `execute-project/scripts/`
2. Rename `update_resume_context.py` -> `update-resume.py`
3. Rewrite `execute-project/SKILL.md` (745 -> ~150 lines)

---

## New Lean SKILL.md (Complete Content)

```markdown
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
```
