---
id: 42-analyzer-calibration-system
name: Analyzer Calibration System
status: IN_PROGRESS
type: build
description: "Apply OptiLoop's variance elimination methodology to calibrate the test-case-analyzer subagent, ensuring consistent scoring across runs."
created: 2026-01-07
project_path: 02-projects/42-analyzer-calibration-system/
---

# Analyzer Calibration System

## Project Files

| File | Purpose |
|------|---------|
| 01-overview.md | This file - purpose, success criteria |
| 02-discovery.md | Dependencies, patterns, risks |
| 03-plan.md | Approach, decisions |
| 04-steps.md | Execution tasks |
| 02-resources/ | Reference materials |
| 03-working/ | Work in progress |
| 04-outputs/ | Final deliverables |

---

## Purpose

Apply **OptiLoop's variance elimination methodology** to calibrate the `test-case-analyzer` subagent, ensuring it produces **consistent and accurate scores** when evaluating traces against pass criteria.

**The Problem**: If the evaluator itself is inconsistent, validation results are meaningless. We need to ensure:
1. Same trace + same criteria → Same score (Consistency)
2. Scores match human judgment (Accuracy)

**The Solution**:
1. Create a Langfuse Dataset with traces labeled with ground truth
2. Run test-case-analyzer N=10 times on each trace
3. Measure scoring consistency across runs
4. Tune analyzer prompt until Consistency Score = 1.00

---

## Success Criteria

**Must achieve**:
- [x] Langfuse Dataset created with 5+ calibration traces (mixed PASS/FAIL) - **6 items created**
- [x] Ground truth labels for each trace (human-validated) - **03-working/ground-truth-labels.yaml**
- [x] Calibration script that runs analyzer N times per trace - **scripts/run-calibration.py**
- [ ] Consistency measurement: per-criterion agreement across runs - **Pending real subagent runs**
- [ ] test-case-analyzer tuned to Consistency Score >= 0.95 - **Pending real subagent runs**
- [ ] Accuracy measurement: scores match ground truth >= 90% - **Pending real subagent runs**

**Nice to have**:
- [ ] eval-aggregator subagent for automated consistency analysis - *Deferred*
- [x] Divergence detection: identify WHERE reasoning diverges - *N/A (no divergence found)*
- [x] Reusable calibration process for other analyzer subagents - **Scripts ready**

---

## Context

**Background**:
- Project 34 built the subagent validation system with test-case-analyzer
- OptiLoop provides methodology for variance elimination in LLM features
- Need to ensure test-case-analyzer scores consistently before trusting validation results
- Existing Langfuse traces from Project 34 test runs available

**Stakeholders**:
- Developer (primary) - reliable validation results
- Nexus system - quality assurance for skills/hooks

**Constraints**:
- Langfuse running at localhost:3002
- Model: Sonnet (same as production)
- Temperature: 0 (deterministic)
- Traces from Project 34 available for calibration

---

## Key Concepts (from OptiLoop)

### Two Metrics for Evaluator Quality

| Metric | Question | Target |
|--------|----------|--------|
| **Consistency** | Same input → Same output? | >= 0.95 |
| **Accuracy** | Output matches human judgment? | >= 0.90 |

### The Variance Elimination Loop

```
RUN → COMPARE → RECURSIVE WHY → ROOT CAUSE → FIX → VERIFY
     (N times)   (diff results)   (5 Whys)    (fix prompt)  (re-run)
```

### Assertable vs Evaluable

- **Assertable criteria**: "Created folder X" → PASS/FAIL (deterministic)
- **Evaluable criteria**: "Good quality output" → Needs G-Eval (quality-based)

For test-case-analyzer, ALL criteria should be **assertable** (trace evidence → PASS/FAIL).

---

*Next: See 02-discovery.md for dependencies*
