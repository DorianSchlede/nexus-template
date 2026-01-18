# Risk Analysis Review

**Build**: State System Refactor
**Reviewer**: Risk Analyst
**Date**: 2026-01-18
**Documents Reviewed**: 02-discovery.md, 03-plan.md, 04-steps.md

---

## Identified Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| **R1: Breaking import chain** - Removing `check_workspace_configured()` and `check_goals_personalized()` from state.py will break session_start.py imports if not updated atomically | M | H | Execute Phase 1 and Phase 2 together in single commit. Never leave codebase in partial state. |
| **R2: Dual source of truth during transition** - Old template detection logic (`is_template_file`) and new learning_tracker logic may conflict during partial rollout | M | M | Plan explicitly keeps `is_template_file()` for validation/logging only. Add comments marking deprecated usage. |
| **R3: Silent state regression** - `extract_learning_completed()` defaults all skills to `false`. If YAML parsing fails silently, users may see regression to "incomplete" status | M | M | Add explicit error logging in `extract_learning_completed()`. Consider returning a tuple `(data, error)` instead of silent fallback. |
| **R4: Stale session context** - Claude's context window may cache old state values after hook updates. Plan doesn't address context invalidation | M | M | Document that users should restart Claude session after refactor. Consider bumping context version hash. |
| **R5: Skills not updating learning_tracker** - Discovery notes this risk but plan doesn't audit existing skills | H | H | **BLOCKER**: Before execution, audit all onboarding skills to verify they set `learning_tracker.completed.{skill}` on completion. Document findings. |
| **R6: Performance regression** - REQ-NF-2 requires <50ms state detection. No baseline measurement in plan | L | L | Add timing instrumentation before/after. Current hook logs performance already. |
| **R7: Naming inconsistency** - REQ-5 defines `create_folders` (underscore) for config keys. Current user-config.yaml uses this correctly, but typos in skill updates could break detection | L | M | Add validation in `extract_learning_completed()` to warn on unknown keys. |
| **R8: Concurrent modification** - No locking mechanism for user-config.yaml. Multiple skills or hooks could race | L | L | Acceptable risk for single-user system. Document as known limitation. |

---

## Critical Risk: Skill Audit Required (R5)

The plan identifies that skills may not be setting `learning_tracker.completed` on completion, but Phase 1-4 execution steps do not include a skill audit task.

**Evidence from Discovery**:
> "Skills not setting learning_tracker on completion | Medium | High | Audit all onboarding skills, add update step"

**Files requiring audit**:
- `00-system/skills/learning/setup-memory/SKILL.md`
- `00-system/skills/learning/create-folders/SKILL.md`
- `00-system/skills/learning/learn-builds/SKILL.md`
- `00-system/skills/learning/learn-skills/SKILL.md`
- `00-system/skills/learning/learn-integrations/SKILL.md`
- `00-system/skills/learning/learn-nexus/SKILL.md`

**Recommendation**: Add "Phase 0: Skill Audit" before Phase 1 execution. Verify each skill:
1. Sets `learning_tracker.completed.{skill_key}: true` on completion
2. Uses correct key name (underscore format)

---

## Rollback Strategy

### Immediate Rollback (< 5 minutes)
1. **Git revert**: All changes are in-place modifications to existing files
   ```bash
   git checkout HEAD~1 -- 00-system/core/nexus/state.py
   git checkout HEAD~1 -- .claude/hooks/session_start.py
   ```
2. **Restart Claude session** to clear cached context

### Staged Rollback (if partial deployment)
1. Keep `check_workspace_configured()` and `check_goals_personalized()` in state.py as deprecated stubs
2. Have them read from `learning_tracker` internally (wrapper pattern)
3. This provides backward compatibility while transitioning

### Rollback Triggers
- Menu shows incorrect state after refactor
- Error logs show YAML parsing failures
- Hook performance exceeds 200ms consistently

---

## Migration Concerns

### Existing User Configs

**Current user-config.yaml analysis:**
```yaml
learning_tracker:
  completed:
    setup_memory: true
    create_folders: false  # Correctly set
    learn_integrations: false
    learn_builds: false
    learn_skills: false
    learn_nexus: false
```

**Assessment**: Current config structure matches expected schema. No migration needed.

### Edge Cases

| Scenario | Current Behavior | Post-Refactor Behavior | Risk |
|----------|------------------|------------------------|------|
| Missing `learning_tracker` key | `extract_learning_completed()` returns defaults | Same - no change | None |
| Missing individual skill key | Returns `False` for that skill | Same - no change | None |
| Old config without YAML frontmatter | `extract_learning_completed()` returns defaults | Same - no change | None |
| Malformed YAML | Silent fallback to defaults | Silent fallback to defaults | Low - consistent |

### Config Version Tracking
**Recommendation**: Add `config_version: 2` to user-config.yaml schema. This allows future migrations to detect config format changes.

---

## Blast Radius Analysis

### Direct Impact (Files Modified)
| File | Impact | Recovery Complexity |
|------|--------|---------------------|
| `state.py` | Function removal | Simple git revert |
| `session_start.py` | Import + logic change | Simple git revert |

### Indirect Impact (Dependent Components)
| Component | Dependency | Impact if Broken |
|-----------|------------|------------------|
| Menu display | Reads `workspace_configured` from context | Shows wrong status |
| Onboarding flow | Uses `goals_personalized` to suggest skills | May suggest already-completed skills |
| Resume detection | Uses state values for build matching | Could fail to resume correctly |
| Orchestrator templates | `_template_onboarding_incomplete()` uses context | May show wrong template |

### Isolated Components (No Impact)
- Build execution (uses 04-steps.md, not state detection)
- Skill loading (path-based, not state-based)
- Memory persistence (independent of state detection)

---

## Testing Gap Analysis

### Covered by Plan
- Unit tests for `extract_learning_completed()`
- Property tests for state consistency
- Checkpoint validation at each phase

### NOT Covered by Plan
1. **End-to-end menu rendering test** - Verify actual menu output matches expected state
2. **Skill completion flow test** - Run `create-folders` skill, verify `learning_tracker` updates
3. **Context cache invalidation test** - Verify fresh session picks up new state
4. **Performance benchmark** - Baseline before, measure after

**Recommendation**: Add integration test task to Phase 3: "Run full hook and verify menu displays correct status for both `create_folders: true` and `create_folders: false` cases"

---

## Verdict

### APPROVE WITH CHANGES

The refactor plan is sound and addresses a real architectural debt. The single-source-of-truth approach is the correct design decision. However, execution should not proceed until:

**Required Changes (MUST DO)**:
1. Add "Phase 0: Skill Audit" to verify all onboarding skills set `learning_tracker.completed` correctly
2. Add end-to-end test to Phase 3 that verifies menu rendering

**Recommended Changes (SHOULD DO)**:
1. Add error logging to `extract_learning_completed()` for YAML parse failures
2. Bump state hash version to force context refresh
3. Document rollback procedure in resume-context.md

**Accepted Risks**:
- Silent YAML fallback behavior (consistent with current behavior)
- No config version tracking (low risk for now)
- No concurrency protection (acceptable for single-user system)

---

*Review completed: 2026-01-18*
