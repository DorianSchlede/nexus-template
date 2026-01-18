# Architecture Review v2 - State System Refactor

**Reviewer**: Architecture Agent (Claude Opus 4.5)
**Date**: 2026-01-18
**Build**: State System Refactor
**Document Reviewed**: `01-planning/04-steps.md` (updated with multi-agent feedback)

---

## Executive Summary

The updated plan incorporates feedback from the initial architecture, risk, and implementation reviews. Phase 0 Skill Audit has been completed successfully, confirming all 6 onboarding skills correctly set their learning_tracker keys. The plan is now ready for execution with one remaining gap to address.

---

## Full Consumer Analysis

### Functions Being Removed

| Function | Location | Lines |
|----------|----------|-------|
| `check_workspace_configured()` | `state.py` | 434-445 |
| `check_goals_personalized()` | `state.py` | 447-458 |

### Complete Consumer Inventory

| Consumer | File | Line(s) | Type | Addressed in Plan? |
|----------|------|---------|------|-------------------|
| Import statement | `session_start.py` | 460-461 | Direct import | YES (Phase 2c) |
| Usage: `check_goals_personalized(goals_path)` | `session_start.py` | 550 | Direct call | YES (Phase 1) |
| Usage: `check_workspace_configured(base_path)` | `session_start.py` | 554 | Direct call | YES (Phase 1) |
| Import statement | `loaders.py` | 1173-1174 | Try/except import | YES (Phase 2c) |
| Usage: `check_goals_personalized(goals_path)` | `loaders.py` | 1189-1190 | Conditional call | **PARTIAL** |
| Usage: `check_workspace_configured(base)` | `loaders.py` | 1203-1204 | Conditional call | **PARTIAL** |
| Fallback assignment | `loaders.py` | 1181-1182 | `= None` fallback | Built-in safety |
| Import statement (unused) | `service.py` | 31 | Direct import | YES (Phase 2c) |
| Internal call in `build_stats()` | `state.py` | 493-494 | Internal | YES (Phase 2a) |
| Test mock | `conftest.py` | 163-164 | Mock object | **NOT ADDRESSED** |

---

## STRENGTHS of the Updated Plan

### 1. Phase 0 Skill Audit - Critical Safety Net
The completed Phase 0 audit proves that all onboarding skills correctly set their learning_tracker keys:
- `setup-memory/SKILL.md` sets `setup_memory: true`
- `create-folders/SKILL.md` sets `create_folders: true`
- All 4 other onboarding skills verified

This eliminates Risk R5 (skills not updating learning_tracker) and provides confidence that the new single source of truth will work correctly.

### 2. Correct Phasing
The plan correctly sequences operations:
1. **Phase 1**: Update consumers FIRST (session_start.py)
2. **Phase 2a**: Update internal consumer (build_stats)
3. **Phase 2b**: THEN remove functions
4. **Phase 2c**: Clean up imports

This prevents broken import states during the refactor.

### 3. Comprehensive Edge Case Testing
Phase 3 now includes:
- Fresh install scenario (no user-config.yaml)
- Partial learning_tracker (missing keys default to false)
- Conflict resolution (`create_folders: true` but workspace-map.md is template - learning_tracker wins)

### 4. Rollback Command Provided
```bash
git checkout HEAD~1 -- 00-system/core/nexus/state.py .claude/hooks/session_start.py
```
Clear escape hatch if issues arise.

---

## CONCERNS

### CONCERN 1: loaders.py Handling is Incomplete (MEDIUM)

**Issue**: The plan mentions "Check loaders.py for references and update if needed" but does not specify the action.

**Current loaders.py code** (lines 1171-1206):
```python
try:
    from .state import (
        check_goals_personalized,
        check_workspace_configured,
        build_display_hints,
        build_pending_onboarding,
        extract_learning_completed,
    )
except ImportError:
    # Fallback if state.py not available
    check_goals_personalized = None
    check_workspace_configured = None
    # ...

if check_goals_personalized:
    goals_personalized = check_goals_personalized(goals_path)
else:
    # Fallback: simple check
    # ...

if check_workspace_configured:
    workspace_configured = check_workspace_configured(base)
else:
    workspace_configured = False
```

**Analysis**: The `try/except ImportError` block with `= None` fallback means loaders.py will NOT crash when the functions are removed. It will gracefully fall back to the inline logic.

**Recommendation**:
- **Option A (Minimal)**: Leave as-is. The fallback handles removal gracefully.
- **Option B (Clean)**: Update loaders.py to use `extract_learning_completed()` like session_start.py. This ensures loaders.py and session_start.py use the same source of truth.

**Verdict**: The plan is safe but inconsistent. loaders.py will silently fall back to its inline template-check logic, which differs from the new learning_tracker approach. Add explicit step to Phase 2c:
> "Update loaders.py to use `learning_completed.get()` pattern instead of check_* functions"

---

### CONCERN 2: Test Mocks Need Update (LOW)

**Issue**: `conftest.py` lines 163-164 mock these functions:
```python
mock_state.check_goals_personalized.return_value = True
mock_state.check_workspace_configured.return_value = True
```

After removal, tests may still pass (mocks return `True`) but are testing phantom functionality.

**Recommendation**: Add to Phase 2c:
> "Update test mocks in conftest.py to remove check_goals_personalized and check_workspace_configured mocks"

---

### CONCERN 3: service.py Import is Unused (LOW - CONFIRMED)

**Analysis**: The grep shows `check_goals_personalized` is imported at line 31 but never used in service.py. The plan correctly identifies this for removal in Phase 2c.

**Status**: Addressed. No action needed.

---

## Dependency Graph

```
                   learning_tracker
                   (user-config.yaml)
                          |
                          v
                 extract_learning_completed()
                          |
              +-----------+-----------+
              |                       |
              v                       v
    session_start.py            build_stats()
    (lines 550-554)            (state.py 493-494)
              |                       |
              v                       v
    goals_personalized          goals_personalized
    workspace_configured        workspace_configured
              |                       |
              v                       v
         <state> XML              stats dict
         (to Claude)              (to JSON cache)
```

**Parallel Path (loaders.py)**:
```
    loaders.py (load_full_startup_context)
              |
              v
    check_goals_personalized (if available)
    check_workspace_configured (if available)
              |
              v
    FALLBACK: inline template check (if not available)
```

**Risk**: After refactor, loaders.py will use fallback (template detection) while session_start.py uses learning_tracker. They may produce different values for the same state.

---

## Recommended Additions to Plan

### Phase 2c - Add These Steps:

```markdown
- [ ] Update loaders.py to use `learning_completed.get("setup_memory", False)` for goals_personalized
- [ ] Update loaders.py to use `learning_completed.get("create_folders", False)` for workspace_configured
- [ ] Remove check_goals_personalized and check_workspace_configured from loaders.py import
- [ ] Update conftest.py to remove mocks for removed functions
```

### Phase 3 - Add Integration Test:

```markdown
- [ ] Verify loaders.py `load_full_startup_context()` returns same state values as session_start.py
```

---

## Final Analysis

| Aspect | Assessment |
|--------|------------|
| Consumer identification | 95% complete (loaders.py action unclear) |
| Dependency graph | Complete |
| Phasing correctness | Correct |
| Edge case coverage | Comprehensive |
| Rollback strategy | Provided |
| Test coverage | Needs mock update |

---

## VERDICT: APPROVE WITH CHANGES

The plan is architecturally sound and ready for execution. The Phase 0 Skill Audit success eliminates the primary risk.

**Required changes before execution**:

1. **Add explicit loaders.py update step** in Phase 2c to use `learning_completed.get()` pattern
2. **Add conftest.py mock cleanup step** in Phase 2c

**Rationale**: Without these changes, the codebase will have inconsistent state detection:
- session_start.py: uses learning_tracker (correct)
- loaders.py: falls back to template detection (inconsistent)
- Tests: mock phantom functions (misleading)

The core refactor logic is correct. These are completeness improvements, not blockers.

---

*Reviewed by Architecture Agent*
*Model: Claude Opus 4.5*
