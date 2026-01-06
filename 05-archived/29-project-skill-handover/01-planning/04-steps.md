# Execution Steps: Project Skill Handover

## Phase 1: Handover Flow (COMPLETE)

- [x] Replace Step 10-11 with handover decision flow
- [x] Update CRITICAL EXECUTION REQUIREMENTS header
- [x] Update CORRECT PATTERN section
- [x] Update Key Features bullet
- [x] Update "Why This Design?" section
- [x] Fix all create-project -> plan-project references

---

## Phase 2: Consolidate execute-project

### Step 2.1: Move bulk-complete into execute-project

- [x] Copy `00-system/skills/projects/bulk-complete/scripts/bulk-complete.py` to `00-system/skills/projects/execute-project/scripts/bulk-complete.py`
- [x] Verify script works from new location:
  ```bash
  python 00-system/skills/projects/execute-project/scripts/bulk-complete.py --help
  ```
- [x] Delete `00-system/skills/projects/bulk-complete/` folder entirely (moved to TRASH/)

### Step 2.2: Rename update script

- [x] Rename `update_resume_context.py` to `update-resume.py`:
  ```bash
  # In execute-project/scripts/
  mv update_resume_context.py update-resume.py
  ```
- [x] Verify renamed script works:
  ```bash
  python 00-system/skills/projects/execute-project/scripts/update-resume.py --help
  ```

### Step 2.3: Delete reference docs

- [x] Delete `references/workflow.md` (987 lines) - moved to TRASH/
- [x] Delete `references/task-tracking.md` (851 lines) - moved to TRASH/
- [x] Delete `references/adaptive-granularity.md` (731 lines) - moved to TRASH/
- [x] Delete `references/resume-update-guide.md` (531 lines) - moved to TRASH/
- [x] Delete `scripts/migrate_resume_to_optimized.py` (309 lines) - moved to TRASH/
- [x] Remove empty `references/` folder - moved to TRASH/

### Step 2.4: Replace SKILL.md with lean version

- [x] Replace `execute-project/SKILL.md` with content from plan.md section "New Lean SKILL.md"
- [x] Verify line count is ~150 lines (down from 745) - actual: 183 lines
- [x] Verify all script paths are correct:
  - `00-system/skills/projects/execute-project/scripts/bulk-complete.py`
  - `00-system/skills/projects/execute-project/scripts/update-resume.py`

### Step 2.5: Validation

- [x] Test bulk-complete from new location:
  ```bash
  python 00-system/skills/projects/execute-project/scripts/bulk-complete.py --help
  ```
- [x] Test update-resume from new location:
  ```bash
  python 00-system/skills/projects/execute-project/scripts/update-resume.py --help
  ```
- [x] Verify skill loads correctly via nexus-loader:
  ```bash
  python 00-system/core/nexus-loader.py --skill execute-project
  ```
- [x] Check no broken references remain (file tree shows only scripts/)

---

## Metrics

| Metric | Before | After | Change |
|--------|--------|-------|--------|
| SKILL.md | 745 | ~150 | -80% |
| Reference docs | 3,100 | 0 | -100% |
| Scripts | 637 | 810 | +27% (merged bulk-complete) |
| Total lines | 5,022 | ~960 | -81% |
| Files | 9 | 3 | -67% |
| Skills | 2 | 1 | Merged |
