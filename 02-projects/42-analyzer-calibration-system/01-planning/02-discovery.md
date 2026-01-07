# Analyzer Calibration System - Discovery

**Project Type**: Build
**Purpose**: Surface requirements and dependencies before planning

---

## Requirements (EARS Format)

### Functional Requirements

**REQ-1**: THE calibration system SHALL create a Langfuse Dataset named "analyzer-calibration" containing trace data with ground truth labels.

**REQ-2**: WHEN a calibration run is initiated, THE system SHALL execute the test-case-analyzer N times (configurable, default 10) on each dataset item.

**REQ-3**: THE system SHALL calculate per-criterion consistency scores by comparing PASS/FAIL judgments across all N runs.

**REQ-4**: WHEN consistency score is below threshold (0.95), THE system SHALL identify the first divergence point in analyzer reasoning.

**REQ-5**: THE system SHALL compare analyzer scores against ground truth labels and report accuracy percentage.

**REQ-6**: THE calibration script SHALL output a report showing:
- Per-criterion consistency scores
- Overall consistency score
- Accuracy vs ground truth
- Divergence analysis (if variance found)

### Non-Functional Requirements

**REQ-NF-1**: THE calibration runs SHALL use model=sonnet and temperature=0 for deterministic output.

**REQ-NF-2**: THE system SHALL complete a full calibration run (10 iterations × 5 traces) within 15 minutes.

### Quality Checklist (INCOSE)

- [x] All requirements use EARS patterns (THE/WHEN/WHILE/IF/WHERE)
- [x] No vague terms (quickly, adequate, reasonable, user-friendly)
- [x] No pronouns (it, them, they) - specific names used
- [x] Each requirement independently testable
- [x] Active voice throughout
- [x] No escape clauses (where possible, if feasible)
- [x] Solution-free (what, not how)

---

## Dependencies

### Files to Modify

| File | Changes Needed |
|------|----------------|
| `.claude/agents/test-case-analyzer.md` | Tune evaluation rules based on calibration results |

### Files to Create

| File | Purpose |
|------|---------|
| `scripts/create-calibration-dataset.py` | Create Langfuse dataset with ground truth traces |
| `scripts/run-calibration.py` | Execute N calibration runs, measure consistency |
| `scripts/analyze-consistency.py` | Calculate scores, identify divergence |
| `03-working/calibration-results.md` | Document calibration iterations |
| `.claude/agents/eval-aggregator.md` | (Optional) Automated consistency analysis subagent |

### External Systems

- **Langfuse (localhost:3002)**: Dataset storage, trace retrieval, run tracking
- **Claude Code Task tool**: Spawning test-case-analyzer subagent

---

## Existing Patterns

| Pattern | Location | Reuse Strategy |
|---------|----------|----------------|
| OptiLoop variance loop | `02-resources/optiloop/CORE-PRINCIPLES.md` | Apply methodology directly |
| test-case-analyzer | `02-resources/subagents/test-case-analyzer.md` | Target for calibration |
| Langfuse dataset skills | `02-resources/langfuse-skills/` | Use for dataset operations |
| Trace mapping | `02-resources/project-34-reference/langfuse-trace-mapping.md` | Query pattern for traces |
| validate-feature workflow | `02-resources/validate-feature-SKILL.md` | Integration context |

---

## Existing Traces for Calibration

From Project 34 test runs (known outcomes):

| Agent ID | Scenario | Expected Outcome | Notes |
|----------|----------|------------------|-------|
| `af67a58` | skill_structure_check | PASS (8/8) | Full skill validation |
| `ac130b0` | skill_structure_check | PASS | Parallel run |
| `a4c2bb6` | skill_structure_check | PASS | Parallel run |
| TBD | error_handling | FAIL | Need to create failing case |
| TBD | edge_case | PARTIAL | Need ambiguous case |

**Action**: Fetch traces from Langfuse, manually validate, create dataset items.

---

## Risks & Unknowns

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Analyzer already consistent | Medium | Low | Good outcome - document baseline |
| Langfuse trace data incomplete | Low | Medium | Verify observations in traces |
| Tuning breaks accuracy | Medium | High | Measure both metrics together |
| 10 runs too slow | Low | Low | Parallelize or reduce to 5 |

### Open Questions

- [x] Where to get existing traces? → Project 34 test runs in Langfuse
- [x] How to create ground truth? → Human review of trace evidence
- [ ] How to detect divergence programmatically? → Diff analyzer reasoning fields
- [ ] What criteria format causes most variance? → Discover during calibration

### Gaps Identified (from Mental Models)

- [ ] **Trace diversity**: Need FAIL and edge case traces, not just PASS traces
- [ ] **Criterion assertability**: Must verify each criterion has ONE correct answer given evidence
- [ ] **UNCERTAIN handling**: Analyzer needs explicit guidance for ambiguous evidence
- [ ] **Dual metric tracking**: Must always report Consistency AND Accuracy together

---

## Langfuse Dataset Structure

```yaml
# Dataset: "analyzer-calibration"
# Items contain trace data + ground truth

item:
  input:
    trace_data:
      trace_id: "abc123"
      agent_id: "af67a58"
      observations: [...]
    pass_criteria:
      - "Skill folder exists"
      - "SKILL.md has Workflow section"
    scenario:
      name: "skill_structure_check"
      description: "Verify skill folder structure"

  expected_output:  # GROUND TRUTH
    overall: "PASS"
    criteria_scores:
      "Skill folder exists": "PASS"
      "SKILL.md has Workflow section": "PASS"

  metadata:
    source: "project-34-phase-7"
    labeled_by: "human"
    confidence: "high"
```

---

## Calibration Workflow

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    CALIBRATION PIPELINE                                  │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  PHASE 1: DATASET CREATION                                               │
│  ├── List traces from Project 34 test runs                               │
│  ├── Select 5+ traces (mix of PASS/FAIL outcomes)                        │
│  ├── Human-review each trace, create ground truth labels                 │
│  └── Create Langfuse Dataset with items                                  │
│                                                                          │
│  PHASE 2: BASELINE MEASUREMENT                                           │
│  ├── For each dataset item:                                              │
│  │   └── Run test-case-analyzer 10x                                      │
│  ├── Collect all scores                                                  │
│  └── Calculate baseline consistency + accuracy                           │
│                                                                          │
│  PHASE 3: ANALYSIS                                                       │
│  ├── Compare scores across 10 runs per item                              │
│  ├── Identify criteria with < 1.00 consistency                           │
│  ├── Diff analyzer reasoning at divergence points                        │
│  └── Root cause analysis (ambiguous criteria? vague prompt?)             │
│                                                                          │
│  PHASE 4: TUNING                                                         │
│  ├── Fix ambiguous pass_criteria wording                                 │
│  ├── Add explicit evaluation rules to analyzer prompt                    │
│  └── Re-run calibration                                                  │
│                                                                          │
│  PHASE 5: VERIFICATION                                                   │
│  ├── Consistency Score >= 0.95?                                          │
│  ├── Accuracy >= 0.90?                                                   │
│  └── Document final analyzer prompt version                              │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

*This discovery document is MANDATORY. It preserves intelligence across compaction.*
*Auto-populate 03-plan.md Dependencies section from findings above.*
