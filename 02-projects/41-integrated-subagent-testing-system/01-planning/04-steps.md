# Integrated Subagent Testing System - Execution Steps

**Project Type**: Build
**Status**: Planning

---

## Context Requirements

**Project Location**: `02-projects/41-integrated-subagent-testing-system/`

**Files to Load for Execution**:
- `01-planning/02-discovery.md` - Requirements and dependencies
- `01-planning/03-plan.md` - Approach and decisions

**Output Location**:
- Scripts: `00-system/skills/system/validate-feature/scripts/`
- Subagents: `.claude/agents/`
- Reports: Project's `04-outputs/validation-reports/`

**Update Resume After Each Section**: Update `resume-context.md` with current_section, tasks_completed

---

## Phase 1: Rename and Restructure (COMPLETE)

**Goal**: Rename trace-analyzer → test-case-analyzer, simplify SKILL.md
**Context**: Load 02-discovery.md

- [x] Rename `.claude/agents/trace-analyzer.md` → `test-case-analyzer.md` **[REQ-5]**
- [x] Update trigger phrase to "spawn test-case-analyzer"
- [x] Update test-case-analyzer to use Langfuse skill patterns from scorer-prompt.md
- [x] Simplify `validate-feature/SKILL.md` to single worktree flow **[REQ-2]**
- [x] Remove manual/interactive modes documentation
- [x] **CHECKPOINT**: Both subagents have correct trigger phrases

---

## Phase 2: Test Scenario Infrastructure (COMPLETE)

**Goal**: Create test scenario template and init script
**Context**: Load 03-plan.md approach section

### 2.1 Scenario Template **[REQ-6]**

- [x] Create `validate-feature/templates/scenarios-template.yaml`
- [x] Define schema: version, project_id, scenarios[]
- [x] Each scenario: name, description, runs, prompt, pass_criteria
- [x] **CHECKPOINT**: Template is valid YAML, follows proposed format

### 2.2 Test Initialization **[REQ-1]**

- [x] Create `validate-feature/scripts/init-tests.py`
- [x] Creates `02-resources/tests/` folder in target project
- [x] Copies scenarios-template.yaml to project
- [x] Also creates `04-outputs/validation-reports/` folder

---

## Phase 3: Main Test Runner (COMPLETE)

**Goal**: Implement run-tests.py orchestration script
**Context**: Load 03-plan.md workflow diagram

### 3.1 Worktree Management **[REQ-2]** (see Discovery Gap 3)

- [x] Enhance `worktree-manager.py` with Path.resolve()
- [x] Sequential worktree creation (prevent race conditions)
- [x] **CRITICAL**: Use `Path.resolve()` for absolute paths in all worktree operations
- [x] Return list of ABSOLUTE worktree paths for execution
- [x] Cleanup function for all test worktrees

### 3.2 Test Execution **[REQ-3]**

- [x] Create `validate-feature/scripts/run-tests.py`
- [x] Read scenarios.yaml, parse into individual test configs
- [x] Generate prompts for test-orchestrator in worktrees
- [x] Save prompts to 03-working/test-prompts/ for Claude execution
- [x] Configurable Langfuse ingestion wait (default 10s)

### 3.3 Trace Collection **[REQ-4]** (CRITICAL - see Discovery Gaps 1, 2, 4)

- [x] Refactor `fetch-traces.py` with enhanced patterns
- [x] **CRITICAL**: Retry logic with exponential backoff (5s, 10s, 15s)
- [x] Query by `metadata.conversationId = "agent-{agentId}"`
- [x] **CRITICAL**: Call `GET /traces/{id}` for EACH trace to get observations
- [x] Format traces with observations (structured + markdown)
- [x] **CHECKPOINT**: Scripts ready - all critical fixes implemented

---

## Phase 4: Analyzer Integration (COMPLETE)

**Goal**: Connect test-case-analyzer to workflow
**Context**: Load test-case-analyzer.md

### 4.1 Input Format **[REQ-5]**

- [x] Update test-case-analyzer to expect standardized input format
- [x] Input: traces, pass_criteria, scenario_context, output_location
- [x] Analyzer writes report to specified path via Write tool

### 4.2 Report Generation **[REQ-5]**

- [x] Verify report template in analyzer produces required format
- [x] Include: summary table, per-run analysis, evidence citations
- [x] Write to `04-outputs/validation-reports/{timestamp}-{scenario}.md`
- [x] **CHECKPOINT**: Analyzer configured with correct templates

---

## Phase 5: End-to-End Integration (IN PROGRESS)

**Goal**: Full workflow working
**Context**: All components implemented

- [x] Test dry-run mode: scenarios loaded, worktrees planned correctly
- [x] Verify worktree cleanup works **[REQ-NF-3]**
- [ ] Test with real subagent execution (requires Langfuse running)
- [ ] **CHECKPOINT**: E2E test passes, all files in expected locations

---

## Phase 6: Validation

**Goal**: Verify against requirements and properties
**Context**: Implementation complete

- [ ] Verify REQ-1: Test scenarios generated during project planning
- [ ] Verify REQ-2: All tests use worktree isolation
- [ ] Verify REQ-3: test-orchestrator unaware of testing
- [ ] Verify REQ-4: Traces fetched from Langfuse correctly
- [ ] Verify REQ-5: Reports written to correct location
- [ ] Verify REQ-NF-1: Traces available within 15s
- [ ] Verify REQ-NF-2: No Windows encoding errors
- [ ] Verify REQ-NF-3: Worktrees cleaned up
- [ ] **CHECKPOINT**: All requirements verified

---

## Phase 7: Documentation & Finalization

**Goal**: Complete project and update state
**Context**: All validation passed

- [ ] Update SKILL.md with simplified workflow documentation
- [ ] Update key-insights.md in Project 34 with learnings
- [ ] Update resume-context.md: current_phase: "complete"
- [ ] Update 01-overview.md success criteria checkboxes
- [ ] Clean up any test artifacts

---

## Summary

| Phase | Tasks | Checkpoints | Critical Items |
|-------|-------|-------------|----------------|
| Phase 1: Rename/Restructure | 6 | 1 | - |
| Phase 2: Scenario Infrastructure | 6 | 2 | - |
| Phase 3: Test Runner | 13 | 1 | **Retry logic, Observations, Abs paths** |
| Phase 4: Analyzer Integration | 5 | 1 | - |
| Phase 5: E2E Integration | 4 | 1 | - |
| Phase 6: Validation | 9 | 1 | - |
| Phase 7: Documentation | 5 | 0 | - |
| **Total** | **48** | **7** | **3 critical fixes** |

---

## Critical Implementation Notes (from Deep Analysis)

1. **Observations are REQUIRED for pass criteria verification**
   - Current `fetch-traces.py` counts but doesn't retrieve observations
   - Must call `GET /traces/{id}` for EACH trace

2. **Retry logic prevents missing traces**
   - Ingestion delay varies 5-15s
   - Use exponential backoff: 5s → 10s → 15s

3. **Absolute paths prevent subagent failures**
   - Relative `../test-validation-0` may not resolve
   - Always use `Path.resolve()`

---

*Mark tasks complete with [x] as you finish them*
