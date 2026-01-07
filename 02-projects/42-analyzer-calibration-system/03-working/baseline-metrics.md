# Calibration Analysis Report

**Generated**: 2026-01-07T20:38:23.783079
**Source**: 02-projects/42-analyzer-calibration-system/03-working/baseline-results.json
**Items Analyzed**: 6
**Runs Per Item**: 10

---

## Summary

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| Avg Consistency | 100.00% | >= 95% | PASS |
| Avg Accuracy | 100.00% | >= 90% | PASS |

---

## Per-Criterion Consistency

| Criterion | Avg Consistency |
|-----------|-----------------|
| Agent responded to task | 100.00% |
| No errors in execution | 100.00% |
| Task completed | 100.00% |
| Used appropriate tools | 100.00% |

---

## Per-Item Analysis

### cal-a2251e1 (long_session)

**Consistency**: 100.00%
**Accuracy**: 100.00%

| Criterion | Consistency | Expected | Actual | Match |
|-----------|-------------|----------|--------|-------|
| Agent responded to task | 100.00% | PASS | PASS | Y |
| No errors in execution | 100.00% | PASS | PASS | Y |
| Task completed | 100.00% | UNCERTAIN | PASS | Y |
| Used appropriate tools | 100.00% | PASS | PASS | Y |

### cal-aae376a (short_session)

**Consistency**: 100.00%
**Accuracy**: 100.00%

| Criterion | Consistency | Expected | Actual | Match |
|-----------|-------------|----------|--------|-------|
| Agent responded to task | 100.00% | PASS | PASS | Y |
| No errors in execution | 100.00% | UNCERTAIN | PASS | Y |
| Task completed | 100.00% | UNCERTAIN | PASS | Y |
| Used appropriate tools | 100.00% | UNCERTAIN | PASS | Y |

### cal-ac130b0 (skill_structure_check)

**Consistency**: 100.00%
**Accuracy**: 100.00%

| Criterion | Consistency | Expected | Actual | Match |
|-----------|-------------|----------|--------|-------|
| Agent responded to task | 100.00% | PASS | PASS | Y |
| No errors in execution | 100.00% | PASS | PASS | Y |
| Task completed | 100.00% | PASS | PASS | Y |
| Used appropriate tools | 100.00% | PASS | PASS | Y |

### cal-aa40d86 (documentation_reading)

**Consistency**: 100.00%
**Accuracy**: 100.00%

| Criterion | Consistency | Expected | Actual | Match |
|-----------|-------------|----------|--------|-------|
| Agent responded to task | 100.00% | PASS | PASS | Y |
| No errors in execution | 100.00% | PASS | PASS | Y |
| Task completed | 100.00% | PASS | PASS | Y |
| Used appropriate tools | 100.00% | UNCERTAIN | PASS | Y |

### cal-a9cda74 (research_task)

**Consistency**: 100.00%
**Accuracy**: 100.00%

| Criterion | Consistency | Expected | Actual | Match |
|-----------|-------------|----------|--------|-------|
| Agent responded to task | 100.00% | PASS | PASS | Y |
| No errors in execution | 100.00% | PASS | PASS | Y |
| Task completed | 100.00% | PASS | PASS | Y |
| Used appropriate tools | 100.00% | PASS | PASS | Y |

### cal-a000241 (skill_validation)

**Consistency**: 100.00%
**Accuracy**: 100.00%

| Criterion | Consistency | Expected | Actual | Match |
|-----------|-------------|----------|--------|-------|
| Agent responded to task | 100.00% | PASS | PASS | Y |
| No errors in execution | 100.00% | PASS | PASS | Y |
| Task completed | 100.00% | PASS | PASS | Y |
| Used appropriate tools | 100.00% | PASS | PASS | Y |

---

## Next Steps

**NOTE: SIMULATED DATA ONLY**

These results are from SIMULATED analyzer (Python logic), NOT the real test-case-analyzer subagent.

### Blocking Issue

Trace data has **0 observations**. Cannot run real subagent calibration until traces with observation data are available.

### Investigation Required

1. [ ] Investigate why selected traces have no observations
2. [ ] Re-select traces with actual observation data
3. [ ] Update dataset items to point to valid traces
4. [ ] Run REAL subagent calibration (N=10 × 6 items)
5. [ ] Calculate real metrics and compare to simulated
