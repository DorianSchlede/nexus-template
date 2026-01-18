# Architecture Review: State System Refactor

**Reviewer**: Architecture Reviewer
**Date**: 2026-01-18
**Documents Reviewed**:
- 02-discovery.md (Requirements)
- 03-plan.md (Approach)
- 04-steps.md (Execution)
- state.py (Current Implementation)
- session_start.py (Hook Integration)

---

## Strengths

### 1. Sound Architectural Principle
The "single source of truth" approach using `learning_tracker.completed` is fundamentally correct. The current system has **three competing state sources**:
- `is_template_file()` - content-based detection
- `check_workspace_configured()` / `check_goals_personalized()` - file existence + template detection
- `learning_tracker.completed` - explicit completion flags

This creates race conditions and inconsistent state reporting. Consolidating to explicit flags is the right call.

### 2. Clear Requirements Engineering
The EARS-format requirements (REQ-1 through REQ-NF-2) are well-written, testable, and traceable. Each step in 04-steps.md maps back to a requirement.

### 3. Correct Identification of Root Cause
The discovery document correctly identifies that file content heuristics (`is_template_file()`) are unreliable because:
- Users may manually edit files
- Template markers may be removed but skill not "completed"
- Multiple detection methods disagree on state

### 4. Safe Fallback Design
`extract_learning_completed()` already provides sensible defaults (`False` for all skills), so missing or malformed config files won't break the system.

### 5. Non-Breaking Scope
The refactor only changes internal state detection logic. The external API (what values are reported) stays the same - just sourced from a single location.

---

## Concerns

### 1. CRITICAL: Multiple Consumers Not Fully Mapped

The plan identifies changes to:
- `state.py` (remove functions)
- `session_start.py` (change detection)

**But the grep analysis reveals additional consumers:**

| File | Import/Usage | Impact |
|------|--------------|--------|
| `loaders.py` (lines 1173-1204) | Imports and calls both `check_*` functions | Will break on removal |
| `service.py` (line 31) | Imports `check_goals_personalized` | Will break on removal |
| `conftest.py` (lines 163-164) | Mocks both functions in tests | Tests will fail |

**Risk**: Removing functions from `state.py` without updating these files will cause `ImportError` and runtime failures.

### 2. Dual State Detection Still Exists in session_start.py

Lines 549-567 of `session_start.py` currently do:
```python
goals_is_template = is_template_file(str(goals_path))
goals_personalized = check_goals_personalized(goals_path)
# ...validation that forces consistency
```

The plan says "keep is_template_file checks but only for logging" but the current code uses them for **validation overrides** (lines 562-567):
```python
if goals_is_template and goals_personalized:
    goals_personalized = False  # Force correct value
```

If we switch to `learning_tracker` as truth, this validation logic becomes:
- Either redundant (learning_tracker is trusted)
- Or incorrect (overriding learning_tracker based on template detection)

**Decision needed**: Should validation overrides be removed, or should they now warn-only?

### 3. build_stats() Internal Calls

`state.py:build_stats()` (lines 493-494) internally calls both `check_*` functions:
```python
goals_personalized = check_goals_personalized(goals_path)
workspace_configured = check_workspace_configured(base_path)
```

This function is called by `NexusService.startup()`. If we remove the `check_*` functions, `build_stats()` also needs updating to use `learning_tracker` - but this is not mentioned in 04-steps.md.

### 4. Naming Convention Mismatch

REQ-5 specifies `create_folders` (underscore) for config keys. Current code in `session_start.py` line 570:
```python
learning_completed = extract_learning_completed(config_path)
```

The `extract_learning_completed()` function in state.py (lines 370-377) uses:
```python
"setup_memory": False,
"create_folders": False,  # Already correct
```

**Confirmed safe**: The naming is already consistent in the code.

---

## Recommendations

### R1: Update Dependency List (REQUIRED)
Before execution, update 02-discovery.md and 04-steps.md to include:

| File | Change Needed |
|------|---------------|
| `loaders.py` | Replace `check_*` calls with `learning_tracker` lookup |
| `service.py` | Remove unused import `check_goals_personalized` |
| `state.py:build_stats()` | Use `learning_completed` param already passed in, remove internal `check_*` calls |
| `conftest.py` | Update mocks to match new API |

### R2: Clarify Validation Override Behavior
Add explicit decision to 03-plan.md:

> **Decision**: Template validation in session_start.py (lines 562-567) shall be converted to warning-only logging. The `learning_tracker` value is authoritative and shall not be overridden by template detection.

### R3: Add Migration Testing
Phase 3 validation should include:
- [ ] Test with config where `create_folders: true` but workspace-map.md is still a template (verify learning_tracker wins)
- [ ] Test with config missing `learning_tracker` section entirely (verify defaults work)

### R4: Consider Deprecation Over Deletion
Instead of immediately removing `check_workspace_configured()` and `check_goals_personalized()`, consider:

```python
def check_workspace_configured(base_path: Path) -> bool:
    """DEPRECATED: Use extract_learning_completed()['create_folders'] instead."""
    import warnings
    warnings.warn("check_workspace_configured is deprecated", DeprecationWarning)
    # ... existing logic for backward compatibility
```

This gives external consumers (if any exist outside the codebase) time to migrate.

---

## Edge Cases to Consider

### E1: Skill Execution Failure
**Scenario**: User runs `create-folders` skill, but it fails mid-execution. Learning tracker updated?

**Current plan assumption**: Skill sets flag on completion.
**Risk**: If skill sets flag at START, partial completion is marked as done.
**Mitigation**: Audit each onboarding skill to ensure flag is set ONLY on successful completion.

### E2: Manual Config Editing
**Scenario**: User manually sets `create_folders: true` in user-config.yaml without running the skill.

**Impact**: System believes folders are created when they may not be.
**Acceptable**: This is user choice. The plan explicitly accepts explicit flags over heuristics.

### E3: Config File Corruption
**Scenario**: YAML parsing fails due to syntax error.

**Current handling**: `extract_learning_completed()` has try/except returning defaults (all False).
**Acceptable**: Fail-safe behavior. User sees onboarding suggestions again.

### E4: Clock/Timezone Issues in Logging
**Scenario**: Logging timestamps inconsistent.

**Impact**: None on state detection.
**N/A**: Out of scope.

### E5: Concurrent Session Conflict
**Scenario**: Two Claude sessions run simultaneously, one completes onboarding.

**Risk**: Second session has stale cached state.
**Current mitigation**: None in plan.
**Recommendation**: Not critical for v1, but note that `session_start.py` reads config fresh each time.

---

## Verdict

### APPROVE WITH CHANGES

The architectural approach is sound and the "single source of truth" pattern is correct. However, the dependency analysis is incomplete.

**Required before execution:**
1. Add `loaders.py`, `service.py`, and `build_stats()` to the modification list
2. Update `conftest.py` test mocks
3. Clarify validation override behavior in session_start.py

**Recommended but not blocking:**
- Consider deprecation warnings before removal
- Add migration test cases

Once the dependency list is complete, this refactor can proceed safely.

---

*Review completed: 2026-01-18*
