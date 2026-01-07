# Project 35: Score Config Setup

**Status**: PLANNING
**Type**: Implementation (Small)
**Parent Research**: Project 27 - Langfuse Annotation and Scoring Integration
**Created**: 2026-01-07

---

## High-Level Goal

Create the foundational scoring infrastructure in Langfuse that enables the entire quality monitoring pipeline.

---

## System Context: Self-Improvement Pipeline

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    CLAUDE CODE QUALITY MONITORING SYSTEM                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  PURPOSE: Systematic visibility into session quality with human-reviewed    │
│           suggestions for improvement. NOT autonomous self-improvement.     │
│                                                                              │
│  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐   ┌──────────────┐ │
│  │  PROJECT 35  │   │  PROJECT 36  │   │  PROJECT 37  │   │  PROJECT 38  │ │
│  │              │   │              │   │              │   │              │ │
│  │    Score     │──►│   Session    │──►│   Weekly     │──►│   Ground     │ │
│  │   Config     │   │   Scorer     │   │  Monitoring  │   │    Truth     │ │
│  │   Setup      │   │              │   │              │   │  Bootstrap   │ │
│  │              │   │              │   │              │   │              │ │
│  │  YOU ARE     │   │  Scores      │   │  Synthesizes │   │  Calibrates  │ │
│  │  HERE        │   │  sessions    │   │  patterns    │   │  AI vs human │ │
│  └──────────────┘   └──────────────┘   └──────────────┘   └──────────────┘ │
│        │                   │                  │                  │          │
│        ▼                   ▼                  ▼                  ▼          │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                         LANGFUSE DATABASE                             │  │
│  │  - Score Configs (defines what we measure)                           │  │
│  │  - Scores (attached to traces/sessions)                              │  │
│  │  - Datasets (ground truth for calibration)                           │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                    │                                        │
│                                    ▼                                        │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                     WEEKLY QUALITY REPORTS                            │  │
│  │  - Dimension statistics and trends                                    │  │
│  │  - Outlier sessions (excellent + poor)                               │  │
│  │  - Suggestions for HUMAN REVIEW                                       │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                    │                                        │
│                                    ▼                                        │
│                        HUMAN DECIDES & IMPLEMENTS                           │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Why This Project First**: Score configs define the "schema" for measuring quality. Without them, no scores can be stored. This is the prerequisite for all downstream projects.

---

## What This Project Does

### Deliverables

1. **7 Score Configs in Langfuse**
   - `task_completion` (CATEGORICAL)
   - `execution_quality` (NUMERIC)
   - `tool_mastery` (NUMERIC)
   - `resource_efficiency` (NUMERIC)
   - `security_compliance` (CATEGORICAL)
   - `user_satisfaction` (CATEGORICAL)
   - `overall_quality` (NUMERIC)

2. **1 Ground Truth Dataset**
   - `self-improvement-ground-truth`
   - For storing human labels for calibration

3. **Validation**
   - Test scoring on 3-5 sample sessions
   - Verify scores appear in Langfuse UI

---

## Scoring Dimensions (from Project 27 Research)

| Dimension | Type | Weight | What It Measures |
|-----------|------|--------|------------------|
| task_completion | CATEGORICAL | 0.30 | Did it achieve the goal? |
| execution_quality | NUMERIC | 0.25 | How well were instructions followed? |
| tool_mastery | NUMERIC | 0.20 | Right tools + error recovery? |
| resource_efficiency | NUMERIC | 0.15 | Context/token efficiency? |
| security_compliance | CATEGORICAL | 0.05 | Avoided security risks? |
| user_satisfaction | CATEGORICAL | 0.05 | User happy with result? |
| overall_quality | NUMERIC | - | Weighted aggregate |

---

## Success Criteria

- [ ] All 7 score configs exist in Langfuse
- [ ] Ground truth dataset created
- [ ] 3-5 sessions manually scored
- [ ] Scores visible in Langfuse UI
- [ ] Any API quirks documented

---

## Reference Materials

All from Project 27 research (in `02-resources/reference/`):
- `scoring-dimensions.md` - Full dimension definitions
- `langfuse-api-validation.md` - What works and doesn't
- `architecture-design.md` - System design context
- `research-summary.md` - Executive summary
- `original-spec.md` - Original spawned project spec

---

## Dependencies

**Requires**:
- Langfuse running at localhost:3002
- Langfuse skills working (verified in Project 27)

**Enables**:
- Project 36: Session Scorer
- Project 38: Ground Truth Bootstrap

---

## Estimated Effort

Small (1-2 sessions)
- Phase 1: Discovery & validation (~30 min)
- Phase 2: Create configs (~30 min)
- Phase 3: Test scoring (~30 min)

---

*Next: Complete 02-discovery.md to investigate Langfuse skills and current state*
