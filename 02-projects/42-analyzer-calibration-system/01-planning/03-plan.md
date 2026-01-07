# Analyzer Calibration System - Plan

**Project Type**: Build
**Status**: Planning

---

## Context

**Load Before Reading**:
- `01-planning/02-discovery.md` - Requirements and dependencies

---

## Approach

Apply OptiLoop's variance elimination methodology to calibrate the test-case-analyzer:

1. **Create Ground Truth Dataset** - Use existing Langfuse traces with human-validated labels
2. **Measure Baseline** - Run analyzer 10x per trace, measure consistency
3. **Analyze Variance** - Identify divergence points, root cause analysis
4. **Tune Iteratively** - Fix criteria/prompt, re-measure until target met
5. **Verify** - Confirm Consistency >= 0.95 AND Accuracy >= 0.90

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    CALIBRATION ARCHITECTURE                              │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  LANGFUSE DATASET                                                        │
│  ┌────────────────────────────────────────────────────────────────┐     │
│  │ analyzer-calibration                                            │     │
│  │ ├── item-001: trace + criteria + GROUND_TRUTH                  │     │
│  │ ├── item-002: trace + criteria + GROUND_TRUTH                  │     │
│  │ └── item-00N: trace + criteria + GROUND_TRUTH                  │     │
│  └────────────────────────────────────────────────────────────────┘     │
│                           │                                              │
│                           ▼                                              │
│  CALIBRATION SCRIPT (run-calibration.py)                                 │
│  ┌────────────────────────────────────────────────────────────────┐     │
│  │ For each dataset item:                                          │     │
│  │   For i in 1..N:                                                │     │
│  │     spawn test-case-analyzer with (trace, criteria)             │     │
│  │     collect scores[i]                                           │     │
│  │   calculate consistency(scores)                                 │     │
│  │   compare scores[0] vs GROUND_TRUTH → accuracy                  │     │
│  └────────────────────────────────────────────────────────────────┘     │
│                           │                                              │
│                           ▼                                              │
│  OUTPUT: Calibration Report                                              │
│  ┌────────────────────────────────────────────────────────────────┐     │
│  │ Per-criterion consistency: [0.9, 1.0, 0.8, ...]                │     │
│  │ Overall consistency: 0.85                                       │     │
│  │ Accuracy vs ground truth: 0.92                                  │     │
│  │ Divergence analysis: "Criterion 3 varied at reasoning step X"  │     │
│  └────────────────────────────────────────────────────────────────┘     │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Correctness Properties

**Property 1: Consistency Invariant**
For all valid (trace, criteria) pairs, running test-case-analyzer N times with temperature=0 SHALL produce identical scores in >= 95% of criterion evaluations.
**Validates**: REQ-2, REQ-3

**Property 2: Accuracy Guarantee**
For all dataset items with ground truth labels, analyzer scores SHALL match ground truth in >= 90% of criterion evaluations.
**Validates**: REQ-5

**Property 3: Determinism**
For any single (trace, criterion) input, the analyzer SHALL produce the same PASS/FAIL judgment when evidence is unambiguous.
**Validates**: REQ-NF-1

---

## Key Decisions

| Decision | Choice | Rationale | Validates |
|----------|--------|-----------|-----------|
| Dataset storage | Langfuse Dataset | Native integration, supports runs/items, tracks evaluations | REQ-1 |
| Calibration runs | N=10 | Balance between statistical significance and runtime | REQ-2 |
| Consistency metric | Per-criterion agreement rate | Identifies specific problematic criteria | REQ-3 |
| Divergence detection | Diff analyzer reasoning | OptiLoop methodology - find first divergence point | REQ-4 |
| Ground truth creation | Human review of traces | Most reliable source of truth | REQ-5 |

---

## Dependencies & Links

**Files to Modify**:
| File | Changes | Validates |
|------|---------|-----------|
| `.claude/agents/test-case-analyzer.md` | Add explicit evaluation rules, MECE criteria guidance | REQ-3, REQ-4 |

**Files to Create**:
| File | Purpose | Validates |
|------|---------|-----------|
| `scripts/create-calibration-dataset.py` | Create Langfuse dataset with ground truth | REQ-1 |
| `scripts/run-calibration.py` | Execute N runs, collect scores | REQ-2, REQ-6 |
| `scripts/analyze-consistency.py` | Calculate metrics, detect divergence | REQ-3, REQ-4, REQ-5 |
| `03-working/calibration-results.md` | Document iterations | REQ-6 |

**External Systems**:
- **Langfuse (localhost:3002)**: Dataset API for storage, trace retrieval
- **Task tool**: Spawning test-case-analyzer subagent

---

## Testing Strategy

### Property-Based Tests

| Property | Test Strategy |
|----------|---------------|
| P1: Consistency | Run 10x on same trace, verify >= 95% criterion agreement |
| P2: Accuracy | Compare all scores vs ground truth, verify >= 90% match |
| P3: Determinism | Single run produces valid PASS/FAIL for each criterion |

### Validation Tests

| Test Case | Expected Outcome |
|-----------|------------------|
| Known PASS trace | All criteria scored PASS |
| Known FAIL trace | At least one criterion scored FAIL |
| Ambiguous trace | Consistent scoring (even if "wrong") |
| Missing observations | Marked as UNCERTAIN, not random |

---

## Open Questions

| Question | Resolution | Validates |
|----------|------------|-----------|
| How to detect divergence programmatically? | Parse analyzer reasoning, diff at statement level | REQ-4 |
| What if baseline consistency is already 1.00? | Document and move on - good outcome | REQ-3 |
| How to handle truly ambiguous traces? | Accept consistent "wrong" over inconsistent "right" | REQ-3 |

---

## Mental Models Applied

### Pre-Mortem Analysis

*"Imagine it's 2 weeks from now and this calibration project failed. What went wrong?"*

| Failure Mode | Likelihood | Impact | Mitigation |
|--------------|------------|--------|------------|
| Ground truth labels are wrong | Medium | Critical | 2nd person validate; use traces with obvious outcomes |
| Analyzer already 100% consistent | Medium | Low | Good outcome - document as baseline |
| **Tuning consistency breaks accuracy** | **High** | **High** | **Always measure BOTH metrics together** |
| Criteria too vague to ever be consistent | Medium | High | Rewrite to be assertable (yes/no based on evidence) |
| Not enough trace diversity | Medium | Medium | Include PASS, FAIL, and edge cases |
| Langfuse traces missing observations | Low | High | Verify `GET /traces/{id}` returns observations first |

### First Principles

**The fundamental question for each criterion:**
> "Given this trace evidence, is there ONE correct answer?"

- **YES** → Assertable → Should be 100% consistent
- **NO** → Either:
  - Criterion is vague → Rewrite it
  - Evidence is ambiguous → Add "UNCERTAIN" category
  - Criterion is evaluable (quality-based) → Needs G-Eval, not PASS/FAIL

**Key Insight**: Variance comes from **ambiguity** - fix the ambiguity, fix the variance.

### Hypothesis Testing

| Hypothesis | Test | Expected |
|------------|------|----------|
| H1: temp=0 produces consistent output | Run same trace 10x | >= 95% agreement |
| H2: Explicit criteria → higher consistency | Compare before/after rewrite | Improvement |
| H3: Ambiguous evidence causes variance | Compare clear vs unclear traces | Clear → higher |
| H0 (null): Analyzer already consistent | Baseline measurement | >= 95%? |

---

## Success Criteria (from Mental Models)

- [ ] Consistency Score >= 0.95 across all calibration traces
- [ ] Accuracy >= 0.90 vs ground truth labels
- [ ] BOTH metrics measured together (never optimize one alone)
- [ ] Divergence points identified and documented (if any)
- [ ] test-case-analyzer prompt updated with explicit rules
- [ ] Criteria writing guidelines documented for future use

## Risks & Mitigations (from Pre-Mortem)

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Ground truth labels are wrong | Medium | Critical | 2nd person validate; obvious outcome traces |
| Analyzer already consistent | Medium | Low | Treat as good baseline, document |
| **Tuning consistency breaks accuracy** | **High** | **High** | **Measure BOTH metrics together; never optimize one alone** |
| Criteria too vague to be consistent | Medium | High | Rewrite as assertable (yes/no from evidence) |
| Not enough trace diversity | Medium | Medium | Include PASS, FAIL, edge cases in dataset |
| 10 runs per trace too slow | Low | Low | Parallelize or reduce to 5 |

---

*Execution steps in 04-steps.md*
