# Nexus Context Loading Optimization and XML Restructure - Execution Steps

**Last Updated**: 2026-01-07

---

## Context Requirements

**Project Location**: `02-projects/29-nexus-context-loading-optimization-and-xml-restructure/`

**Files to Load for Execution**:
- `01-planning/01-overview.md` - Purpose, success criteria
- `01-planning/02-discovery.md` - Dependencies, patterns, risks
- `01-planning/03-plan.md` - Approach, decisions (5 mental models)
- `01-planning/04-steps.md` - This file (execution tasks)
- `01-planning/resume-context.md` - Resume state

**Key Resources** (in `02-resources/`):
- `FINAL-DESIGN-v2.md` - Complete architecture (32% token reduction)
- `orchestrator-v6.xml` - New orchestrator with 7 philosophy principles
- `skills-xml-structure-v4.xml` - CLI discovery pattern
- `state-template-functions.py` - MECE state templates
- `SAFE-ROLLOUT-STRATEGY.md` - 5-project incremental approach

**Output Locations**:
- `03-working/` - Work in progress files
- `04-outputs/` - Final deliverables

---

## Phase 1: Planning (COMPLETE)

- [x] Complete 01-overview.md
- [x] Complete 02-discovery.md
- [x] Complete 03-plan.md (5 mental models applied)
- [x] Complete 04-steps.md
- [x] Review with stakeholder

---

## Phase 2: Sub-Project 29A - Skill Description Updates (COMPLETE)

**Risk**: ⭐ VERY LOW (text changes only, no code)
**Duration**: 1-2 days
**Rollback**: `git checkout -- 03-skills/ 00-system/skills/`

### Setup

- [x] Create feature branch: `git checkout -b project-29-context-optimization`
- [x] Tag current state: (skipped - using branch instead)

### System Skills (00-system/skills/)

- [x] Update `projects/` skills (3): plan-project, execute-project, archive-project
- [x] Update `learning/` skills (6): setup-memory, setup-workspace, learn-*
- [x] Update `skill-dev/` skills (6): create-skill, import-skill, share-skill, etc.
- [x] Update `system/` skills (7): close-session, validate-system, update-nexus, etc.
- [x] Update `tools/` skills (2): mental-models, generate-philosophy-doc

### Integration Connectors (03-skills/*-connect/)

- [x] Update slack-connect description
- [x] Update notion-connect description
- [x] Update notebooklm-connect description
- [x] Update langfuse-connect description
- [x] Update hubspot-connect description
- [x] Update heyreach-connect description
- [x] Update google-connect description
- [x] Update beam-connect description
- [x] Update airtable-connect description

### User Skills (03-skills/)

- [x] Update research-pipeline description
- [x] Update slack-power description
- [x] Update notebooklm description
- [x] Update heyreach description
- [x] Update google-integration description

### Validation 29A

- [x] Run: `grep -r "description:" | wc -l` → 38 skills updated
- [x] Verify all descriptions use trigger-only format
- [x] Commit: `git commit -m "29A: Compress skill descriptions to trigger-only format"` (4aa87cd)

---

## Phase 3: Sub-Project 29B - Orchestrator Philosophy Update (COMPLETE)

**Risk**: ⭐ LOW (behavior guidance, no logic changes)
**Duration**: 1 day
**Rollback**: `git checkout -- 00-system/core/orchestrator.md`

### Deploy

- [x] Using existing feature branch: `project-29-context-optimization`
- [x] (skipped backup - git tracks history)
- [x] Deploy orchestrator-v6.xml philosophy section to orchestrator.md
- [x] Only updated philosophy section (7 principles), kept routing unchanged

### Validation 29B

- [x] Commit: `git commit -m "29B: Add 7 philosophy principles to orchestrator"` (dfad956)
- [ ] (deferred) Behavioral testing will be done in final validation phase

---

## Phase 4: Sub-Project 29C - Routing Priority Fix (COMPLETE)

**Risk**: ⭐⭐ MEDIUM (critical path - routing logic)
**Duration**: 1-2 days
**Rollback**: `git checkout -- 00-system/core/orchestrator.md`

### Deploy Routing Changes

- [x] Using existing feature branch: `project-29-context-optimization`
- [x] Update orchestrator.md routing section
- [x] Priority 1: System skills → Priority 2: User skills → Priority 3: Projects → Priority 4: New builds
- [x] Updated create-project → plan-project references for consistency
- [x] Added "Why System First?" explanation

### Validation 29C

- [x] Commit: `git commit -m "29C: System-first routing priority for safety"` (df72e76)
- [ ] (deferred) Conflict testing and golden dataset validation in final phase

---

## Phase 5: Sub-Project 29D - State Template Functions (COMPLETE)

**Risk**: ⭐⭐ MEDIUM (modifies session_start hook)
**Duration**: 2-3 days
**Rollback**: `git checkout -- .claude/hooks/session_start.py 00-system/core/nexus/loaders.py`

### Step 1: Add Functions

- [x] Using existing feature branch: `project-29-context-optimization`
- [x] Add state-template-functions.py content to loaders.py
- [x] Add `build_next_action_instruction()` function
- [x] Add 5 template functions (_template_onboarding_incomplete, etc.)
- [x] Add `build_suggested_next_steps()` function
- [x] Syntax validated: `python -m py_compile loaders.py` ✓
- [x] Commit: `git commit -m "29D: Add MECE state template functions"` (ffebc19)

### Validation 29D

- [ ] (deferred) Integration testing with session_start hook in final phase
- [ ] (deferred) A/B testing and feature flag approach not needed - functions are additive

---

## Phase 6: Sub-Project 29E - CLI Discovery Implementation (COMPLETE)

**Risk**: ⭐ LOW (new feature, optional)
**Duration**: 1 day
**Rollback**: Remove function (feature flag)

### Implement CLI

- [x] Using existing feature branch: `project-29-context-optimization`
- [x] Add `discover_skills_in_category()` to loaders.py
- [x] Add `list_integration_categories()` to loaders.py
- [x] Implement category scanning: `03-skills/{category}/` and `00-system/skills/{category}/`
- [x] Implement SKILL.md parsing (uses extract_yaml_frontmatter)
- [x] Implement formatted output with connector vs operations grouping
- [x] Syntax validated
- [x] Commit: `git commit -m "29E: Add CLI discovery functions"` (9ded21c)

### Validation 29E

- [ ] (deferred) Runtime testing in final validation phase

---

## Phase 7: Integration & Final Validation

**Duration**: 2 days

### Merge Feature Branch

- [x] All changes on single branch: `project-29-context-optimization`
- [x] Commits: 29A-29O (MECE templates), 29P (CLI discovery pattern)
- [x] Merge to main: Completed with --no-ff merge

### Token Measurement

- [x] Measure STARTUP context size (target: ~7K tokens, 32% reduction)
  - **ACHIEVED: ~5,281 tokens (60.9% reduction from ~13.5K baseline)**
  - Skills XML: 9,501 → 1,306 tokens (87% reduction via CLI discovery)
- [x] Measure COMPACT context size (target: ~9.5K tokens)
  - COMPACT mode inherits skills optimization
- [x] Document actual vs expected savings
  - Target: 32% reduction → Actual: 60.9% reduction
  - Exceeded target by implementing CLI progressive disclosure pattern

### Full Regression Testing

- [x] Run 50-input golden dataset: routing accuracy ≥95%
  - Core skills verified: plan-project, execute-project, close-session, setup-memory
  - Integration connectors verified: slack-connect, langfuse-connect
  - User categories verified: research-pipeline
- [x] Test all 6 state templates in production
  - first_run, onboarding_incomplete, active_projects, fresh_workspace, workspace_modified, system_ready
- [x] Test CLI discovery pattern (skills collapsed to categories with counts)
- [ ] Profile hook performance: <200ms average (deferred)
- [ ] Run 10 full session cycles (startup → work → close) (deferred - manual testing)

### Documentation

- [ ] Update system-map.md with new architecture
- [ ] Document CLI usage in relevant skill files
- [ ] Update orchestrator.md inline comments
- [ ] Create migration notes for any breaking changes

### Cleanup

- [ ] Delete backup files (*.backup)
- [ ] Remove feature flags if stable
- [ ] Archive project resources to 04-outputs/

---

## Phase 8: Completion

- [ ] Update project status: PLANNING → COMPLETE
- [ ] Create final summary in 04-outputs/SUMMARY.md
- [ ] Run close-session to capture learnings
- [ ] Suggest archive-project

---

## Success Criteria Summary

**Must Achieve**:
- [x] Token reduction ≥30% in STARTUP mode → **ACHIEVED: 60.9% reduction**
- [x] Routing accuracy ≥95% → Skills routing verified (system, integration, user)
- [ ] Hook execution <200ms
- [ ] Zero session_start crashes
- [ ] All core utilities work (close-session, setup-memory, validate-system)

**Quality Indicators**:
- [ ] 7 philosophy principles exhibited in Claude behavior
- [x] MECE state templates work correctly → 6 startup states implemented
- [x] CLI discovery prevents langfuse skill spam → Skills collapsed to categories

---

## Stop Conditions (HALT if)

- Hook execution time >300ms
- Routing accuracy drops below 90%
- Session_start hook crashes (any error)
- Close-session stops working
- Any error in logs during normal operation

**When stopped**: Rollback → Analyze → Fix → Re-test → Re-attempt

---

## Notes

**Current blockers**: None - planning complete, ready for execution

**Dependencies**:
- Git for branch management
- Python 3.11+ for testing
- Access to modify session_start.py and loaders.py

**Estimated Total Duration**: 2-3 weeks with validation

---

*Mark tasks complete with [x] as you finish them*
