# Risk Analysis Review v2 (Post-Phase 0 Audit)

**Build**: State System Refactor
**Reviewer**: Risk Analyst (Deep Analysis)
**Date**: 2026-01-18
**Context**: Phase 0 Skill Audit PASSED - all onboarding skills correctly set learning_tracker

---

## Executive Summary

The plan has been significantly improved since the initial risk review. Phase 0 (Skill Audit) has been completed successfully, addressing the highest-impact risk (R5). The rollback command has been added, and edge case tests have been expanded. However, several execution-time risks remain that warrant careful attention during implementation.

---

## REMAINING RISKS

### R1: Import Chain Breakage During Partial Execution
| Attribute | Value |
|-----------|-------|
| **Probability** | Medium |
| **Impact** | High |
| **Description** | Removing `check_workspace_configured()` and `check_goals_personalized()` from state.py will break imports in THREE files, not just session_start.py |

**Evidence from codebase grep:**
- `session_start.py` lines 460-461: Direct imports
- `loaders.py` lines 1172-1174: Imports with fallback (has graceful degradation)
- `service.py` line 31: Direct import (will cause ImportError)
- `state.py` lines 493-494: Internal calls in `build_stats()`

**Assessment**: Plan Step 2c now covers loaders.py and service.py, BUT the current plan does not specify the correct UPDATE for loaders.py - it still uses the deprecated functions and would fall back to `None` which returns `False` for all state, potentially different from learning_tracker values.

**Mitigation**: Execute atomically in single commit. Test imports before committing.

---

### R2: loaders.py Has Fallback Logic That Masks Errors
| Attribute | Value |
|-----------|-------|
| **Probability** | High |
| **Impact** | Medium |
| **Description** | loaders.py lines 1179-1185 have `except ImportError` fallback that sets functions to `None`, then lines 1189-1206 use conditional checks |

**Problem**: After refactor, `check_goals_personalized` will be removed. The import will fail silently (caught by except), and the fallback at lines 1191-1198 uses a DIFFERENT detection method (checking for `smart_default: true` in content) which may give inconsistent results.

**Current fallback code:**
```python
if check_goals_personalized:  # This becomes False
    goals_personalized = check_goals_personalized(goals_path)
else:
    # Fallback: simple check - DIFFERENT LOGIC!
    goals_personalized = False
    try:
        if goals_path.exists():
            content = goals_path.read_text(encoding="utf-8")
            if "smart_default: true" not in content.lower():
                goals_personalized = True  # WRONG - doesn't use learning_tracker!
    except Exception:
        pass
```

**Impact**: If loaders.py import fails, it falls back to file-content heuristics - the exact problem we're trying to fix.

**Mitigation**: Plan MUST update loaders.py to use `extract_learning_completed()` instead of the deprecated functions. The fallback path needs to be updated or removed.

---

### R3: build_stats() Output Structure Must Be Preserved
| Attribute | Value |
|-----------|-------|
| **Probability** | Low |
| **Impact** | High |
| **Description** | `build_stats()` is called by `NexusService.startup()` and its return value feeds into display hints and menu rendering |

**Current function signature (lines 461-488):**
```python
def build_stats(
    base_path: Path,
    memory_content: Dict[str, str],
    builds: List[Dict[str, Any]],
    skills: List[Dict[str, Any]],
    files_exist: Dict[str, bool],
    goals_path: Path,
    config_path: Path,  # Already receives this!
    update_info: Dict[str, Any],
    configured_integrations: List[Dict[str, Any]],
) -> Dict[str, Any]:
```

**Good news**: `config_path` is already a parameter. The function can use `extract_learning_completed(config_path)` directly.

**Validation required**: Ensure the returned stats dict has the same keys (`goals_personalized`, `workspace_configured`) so downstream consumers don't break.

---

### R4: Stale Context After Execution
| Attribute | Value |
|-----------|-------|
| **Probability** | Medium |
| **Impact** | Low |
| **Description** | After refactor completes, Claude's current session may have cached old state values |

**Mitigation**: Plan should recommend restarting Claude session after Phase 3 validation. This is acceptable risk - the state hash mechanism should help detect staleness.

---

### R5: User Manual Config Tampering (Accepted Risk)
| Attribute | Value |
|-----------|-------|
| **Probability** | Low |
| **Impact** | Low |
| **Description** | User could manually set `create_folders: true` without running the skill |

**Assessment**: This is by design. The plan explicitly accepts that `learning_tracker` is authoritative and user-controlled. This is correct - explicit flags are more reliable than heuristics.

---

### R6: YAML Parsing Edge Cases
| Attribute | Value |
|-----------|-------|
| **Probability** | Low |
| **Impact** | Low |
| **Description** | `extract_learning_completed()` has silent exception handling |

**Current code (lines 382-396):**
```python
try:
    content = config_path.read_text(encoding="utf-8")
    if content.startswith("---"):
        # ... parsing logic
except Exception:
    pass  # Silent fallback to defaults
```

**Assessment**: Fail-safe design returns all `False` on any error. This is consistent with current behavior and acceptable.

---

## ROLLBACK ADEQUACY ASSESSMENT

### Rollback Command Analysis

**Provided command:**
```bash
git checkout HEAD~1 -- 00-system/core/nexus/state.py .claude/hooks/session_start.py
```

**Assessment**: **INCOMPLETE**

**Missing files from rollback:**
- `00-system/core/nexus/loaders.py` - Plan Step 2c modifies this
- `00-system/core/nexus/service.py` - Plan Step 2c removes unused import
- `.claude/hooks/tests/conftest.py` - Test mocks need updating

**Corrected rollback command:**
```bash
git checkout HEAD~1 -- \
  00-system/core/nexus/state.py \
  00-system/core/nexus/loaders.py \
  00-system/core/nexus/service.py \
  .claude/hooks/session_start.py \
  .claude/hooks/tests/conftest.py
```

### Rollback Scenarios

| Scenario | Recovery Time | Complexity |
|----------|---------------|------------|
| Import error on startup | < 2 minutes | Low - git revert |
| Wrong state in menu | < 2 minutes | Low - git revert + restart Claude |
| Partial execution failure | 5-10 minutes | Medium - identify affected files |
| Silent wrong behavior | Unknown | High - may not be detected immediately |

### Rollback Trigger Criteria

The plan should clearly define when to rollback:
1. **Immediate**: Any Python ImportError or SyntaxError
2. **Within 5 minutes**: Menu shows wrong state for known config values
3. **Within session**: Hook takes >200ms consistently

---

## TEST COVERAGE ASSESSMENT

### Tests Covered in Phase 3

| Test | Coverage | Assessment |
|------|----------|------------|
| `workspace_configured` with `create_folders: false` | Yes | Core requirement |
| `workspace_configured` with `create_folders: true` | Yes | Core requirement |
| `goals_personalized` with `setup_memory: true` | Yes | Core requirement |
| Fresh install (no user-config.yaml) | Yes | Edge case |
| Partial learning_tracker (missing keys) | Yes | Edge case |
| learning_tracker vs template file conflict | Yes | Edge case - learning_tracker wins |
| `build_stats()` output structure | Yes | Regression check |
| Full hook end-to-end | Yes | Integration |

### Tests NOT Explicitly Covered

| Missing Test | Risk if Untested | Recommendation |
|--------------|------------------|----------------|
| `loaders.py` fallback path behavior | Medium - could silently use wrong logic | Add: Verify loaders.py uses learning_tracker after update |
| `service.py` import removal | Low - will fail fast if broken | Covered by import error detection |
| Test mock updates (conftest.py) | Low - tests fail if wrong | Run test suite after changes |
| Performance benchmark (<50ms) | Low - already logging perf | Add timing check to validation |
| Concurrent session behavior | Very Low - single user | Accept risk |

### Test Gap: loaders.py Fallback

**Critical finding**: The Phase 3 tests don't verify that `loaders.py` correctly uses `extract_learning_completed()` after the deprecated functions are removed.

**Current loaders.py fallback (lines 1191-1198)** will incorrectly use file-content heuristics if the import fails or if the code path isn't updated.

**Recommended additional test:**
```
- [ ] Verify loaders.py load_full_startup_context() returns correct
      state when learning_tracker differs from file template status
```

---

## BLAST RADIUS ANALYSIS

### Direct Impact (Files Modified)

| File | Change Type | Lines Affected |
|------|-------------|----------------|
| `state.py` | Function removal + update | ~30 lines |
| `session_start.py` | Import removal + logic change | ~20 lines |
| `loaders.py` | Import removal + logic update | ~35 lines |
| `service.py` | Import removal | ~1 line |
| `conftest.py` | Mock update | ~2 lines |

### Indirect Impact (Consumers)

| Consumer | Dependency | Impact if Broken |
|----------|------------|------------------|
| Menu display | `workspace_configured` from context | Wrong status shown |
| Onboarding suggestions | `goals_personalized` value | Wrong skill suggestions |
| Template selection | `_template_onboarding_incomplete()` | Wrong template loaded |
| Stats display | `build_stats()` return value | Wrong counts/hints |

### Isolated Components (No Impact)

- Build execution (04-steps.md based)
- Skill loading (path-based discovery)
- Memory file persistence
- Git sync functionality

---

## VERDICT

### APPROVE

The plan is now ready for execution with the following conditions:

**Required Actions (MUST complete during execution):**

1. **Update loaders.py correctly**: The plan lists this file but must ensure it uses `extract_learning_completed()` instead of falling back to file-content heuristics. The fallback code (lines 1191-1206) needs explicit updating, not just import removal.

2. **Update rollback command**: Current command is incomplete. Add all modified files:
   ```bash
   git checkout HEAD~1 -- \
     00-system/core/nexus/state.py \
     00-system/core/nexus/loaders.py \
     00-system/core/nexus/service.py \
     .claude/hooks/session_start.py \
     .claude/hooks/tests/conftest.py
   ```

3. **Add loaders.py verification test**: Phase 3 should verify that `load_full_startup_context()` returns correct state based on learning_tracker, not file content.

**Accepted Risks:**

- Silent YAML parsing fallback (consistent, safe behavior)
- User manual config editing (by design)
- Stale session context (restart documented)
- No concurrency protection (single-user system)

**Confidence Level**: 85%

The remaining 15% uncertainty is:
- 10%: loaders.py fallback path behavior may be more complex
- 5%: Unknown consumers of deprecated functions outside audited files

**Execution Recommendation**: Proceed with execution. Maintain checkpoint discipline. Test each phase before moving to next. Keep git working tree clean for easy rollback.

---

*Review completed: 2026-01-18*
*Reviewer: Risk Analyst (Deep Analysis)*
