# Analyzer Calibration System - Execution Steps

**Project Type**: Build
**Status**: IN_PROGRESS

---

## Context Requirements

**Project Location**: `02-projects/42-analyzer-calibration-system/`

**Files to Load for Execution**:
- `01-planning/02-discovery.md` - Requirements
- `01-planning/03-plan.md` - Approach and decisions
- `02-resources/optiloop/CORE-PRINCIPLES.md` - Variance elimination methodology

**Output Location**: `04-outputs/calibration-reports/`

**Update Resume After Each Section**: Update `resume-context.md` with current_section, tasks_completed

---

## Phase 1: Setup & Trace Selection

**Goal**: Select calibration traces and validate environment
**Context**: Load 02-discovery.md

- [x] Verify Langfuse is running at localhost:3002 **[REQ-1]**
- [x] List available traces from Project 34 test runs
- [x] Select 5+ traces for calibration (mix PASS/FAIL) **[REQ-1]**
- [x] Document selected traces in `03-working/selected-traces.md`
- [x] **CHECKPOINT**: Traces identified (6 sessions selected)

---

## Phase 2: Ground Truth Creation

**Goal**: Human-review traces and create ground truth labels
**Context**: Selected traces from Phase 1

### 2.1 Review Traces **[REQ-1, REQ-5]**

- [x] Fetch full trace data for each selected trace (with observations)
- [x] For each trace:
  - [x] Review observations (tool calls, inputs, outputs)
  - [x] Determine expected PASS/FAIL for each criterion
  - [x] Document evidence supporting judgment
- [x] Create `03-working/ground-truth-labels.yaml`

### 2.2 Create Langfuse Dataset **[REQ-1]**

- [x] Create dataset "analyzer-calibration" via `langfuse-create-dataset`
- [x] For each trace, create dataset item with:
  - Input: trace_data, pass_criteria, scenario
  - Expected output: ground_truth labels
  - Metadata: source, labeled_by
- [x] Verify dataset items created correctly
- [x] **CHECKPOINT**: Dataset ready (6 items: 4 PASS, 1 UNCERTAIN, 1 edge case)

---

## Phase 3: Infrastructure & Simulated Testing

**Goal**: Build calibration scripts and verify with simulated analyzer
**Context**: Dataset created in Phase 2

### 3.1 Create Calibration Script **[REQ-2]**

- [x] Create `scripts/run-calibration.py` that:
  - Loads dataset items from Langfuse
  - For each item, runs analyzer N times
  - Collects scores from each run
  - Outputs results to JSON

### 3.2 Create Analysis Script **[REQ-3, REQ-5]**

- [x] Create `scripts/analyze-consistency.py` that calculates:
  - Per-criterion consistency (agreement rate across N runs)
  - Overall consistency score
  - Accuracy vs ground truth
- [x] Test with simulated analyzer (deterministic Python logic)
- [x] Verify metrics calculation works correctly
- [x] **CHECKPOINT**: Infrastructure verified with simulated data
  - Simulated Consistency: 100%
  - Simulated Accuracy: 100%

**NOTE**: Phase 3 used SIMULATED analyzer, not real subagent. Results only validate the infrastructure.

---

## Phase 4: Real Subagent Calibration

**Goal**: Run ACTUAL test-case-analyzer subagent N times per trace
**Context**: Infrastructure from Phase 3

### 4.1 Modify Calibration Script **[REQ-2]**

- [ ] Update `run-calibration.py` to spawn real test-case-analyzer subagent
- [ ] Add Task tool integration for subagent spawning
- [ ] Handle subagent response parsing
- [ ] Add error handling for failed subagent runs

### 4.2 Run Real Baseline Calibration **[REQ-2, REQ-3]**

- [ ] Execute calibration with N=10 runs per trace using REAL subagent
- [ ] Collect all analyzer reports from subagent responses
- [ ] Store raw results in `03-working/real-baseline-results.json`
- [ ] **CHECKPOINT**: All 60 real runs completed (6 items × 10 runs)

### 4.3 Calculate Real Metrics **[REQ-3, REQ-5]**

- [ ] Run analysis on real baseline results
- [ ] Generate `03-working/real-baseline-metrics.md`
- [ ] Compare real vs simulated results
- [ ] **CHECKPOINT**: Real baseline metrics documented

---

## Phase 5: Divergence Analysis & Tuning

**Goal**: Identify variance sources and tune until targets met
**Context**: Real baseline from Phase 4

### 5.1 Divergence Detection **[REQ-4]**

- [ ] For criteria with consistency < 1.00:
  - [ ] Extract analyzer reasoning from divergent runs
  - [ ] Diff reasoning to find first divergence point
  - [ ] Document root cause (ambiguous criterion? vague prompt?)
- [ ] Create `03-working/divergence-analysis.md`

### 5.2 Tune Pass Criteria **[REQ-3]**

- [ ] For each ambiguous criterion:
  - [ ] Rewrite to be more explicit (MECE format)
  - [ ] Add specific evidence requirements
- [ ] Document changes in `03-working/criteria-improvements.md`

### 5.3 Tune Analyzer Prompt **[REQ-3, REQ-4]**

- [ ] Update `.claude/agents/test-case-analyzer.md`:
  - [ ] Add explicit evaluation rules for common criteria types
  - [ ] Add priority-ordered decision guidelines
  - [ ] Add handling for ambiguous/missing evidence
- [ ] Document changes in `03-working/prompt-improvements.md`

### 5.4 Re-Run Calibration **[REQ-2, REQ-3]**

- [ ] Run calibration again with updated criteria/prompt
- [ ] Calculate new metrics
- [ ] Compare to baseline
- [ ] **CHECKPOINT**: If Consistency >= 0.95 AND Accuracy >= 0.90, proceed to Phase 6
- [ ] If targets not met, repeat Phase 5 (max 3 iterations)

---

## Phase 6: Verification & Documentation

**Goal**: Verify targets met, document final state
**Context**: Tuning complete

### 6.1 Final Verification **[REQ-3, REQ-5]**

- [ ] Run final calibration (N=10) with real subagent **[Property 1]**
- [ ] Verify Consistency >= 0.95 **[Property 1]**
- [ ] Verify Accuracy >= 0.90 **[Property 2]**
- [ ] Generate final calibration report

### 6.2 Documentation **[REQ-6]**

- [ ] Write `04-outputs/calibration-reports/final-report.md`
- [ ] Document all changes made to analyzer prompt
- [ ] Document criteria writing guidelines discovered
- [ ] Update 01-overview.md success criteria checkboxes

### 6.3 Finalization

- [ ] Update resume-context.md: current_phase: "complete"
- [ ] Archive calibration data for future reference
- [ ]* Create eval-aggregator subagent for automated future calibration (optional)

---

## Summary

| Phase | Tasks | Status |
|-------|-------|--------|
| Phase 1: Setup | 5 | COMPLETE |
| Phase 2: Ground Truth | 8 | COMPLETE |
| Phase 3: Infrastructure | 5 | COMPLETE (simulated) |
| Phase 4: Real Calibration | 7 | **NOT STARTED** |
| Phase 5: Tuning | 10 | NOT STARTED |
| Phase 6: Documentation | 9 | NOT STARTED |
| **Total** | **44** | **18/44 done** |

---

## Iteration Tracking

| Iteration | Type | Consistency | Accuracy | Changes Made |
|-----------|------|-------------|----------|--------------|
| Simulated | Python logic | 100% | 100% | N/A (infrastructure test) |
| Real Baseline | Subagent | TBD | TBD | Pending |
| Real Iteration 1 | Subagent | TBD | TBD | TBD |
| Final | Subagent | >= 0.95 | >= 0.90 | (target) |

---

*Mark tasks complete with [x] as you finish them*
*Optional tasks marked with `*` can be skipped for faster MVP*
