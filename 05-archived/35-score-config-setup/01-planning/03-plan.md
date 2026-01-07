# Project 35: Execution Plan

**Date**: 2026-01-07
**Status**: Ready for execution
**Updated**: 2026-01-07 (Enhanced scoring dimensions for subagent-based scoring)

---

## Strategy

Execute in 3 phases:
1. **Validation** - Check current state, verify Langfuse connection
2. **Creation** - Create 7 score configs + 1 dataset
3. **Testing** - Create test scores, verify in UI

**Approach**: Create one config of each type first (NUMERIC + CATEGORICAL), verify it works, then bulk create the rest.

**IMPORTANT**: This uses the **enhanced scoring dimensions** designed for subagent-based scoring. See `03-working/enhanced-scoring-design.md` for full design rationale.

---

## Enhanced Dimensions Overview

| Dimension | Type | Weight | What It Measures |
|-----------|------|--------|------------------|
| goal_achievement | CATEGORICAL | 0.30 | Did session accomplish user's goal? |
| tool_efficiency | NUMERIC | 0.20 | Right tools, minimal retries |
| process_adherence | NUMERIC | 0.20 | Followed workflows (TodoWrite, Read→Edit) |
| context_efficiency | NUMERIC | 0.15 | Efficient file reads, no bloat |
| error_handling | CATEGORICAL | 0.10 | How errors were handled |
| output_quality | NUMERIC | 0.05 | Quality of deliverables |
| overall_quality | NUMERIC | - | Weighted aggregate |

**Why Enhanced?**
- More **measurable** (partial auto-signals from trace data)
- More **actionable** (low scores point to specific fixes)
- **Nexus-aware** (process_adherence checks workflow compliance)
- **Non-overlapping** (each dimension measures distinct aspect)

---

## Phase 1: Environment Validation (5-10 min)

### Goals
- Verify Langfuse is accessible
- List existing score configs
- Identify any cleanup needed

### Tasks
1. **BLOCKER**: Add `LANGFUSE_HOST=http://localhost:3002` to `.env`
2. Test Langfuse connection
3. List current score configs
4. List current datasets
5. Decide: clean up test configs from Project 27 or leave them

---

## Phase 2: Score Config Creation (15-20 min)

### Goals
- Create all 7 production score configs (enhanced dimensions)
- Create ground truth dataset

### Order of Creation

**First (validate pattern works)**:
1. `tool_efficiency` (NUMERIC) - simple case

**Then (CATEGORICAL validation)**:
2. `goal_achievement` (CATEGORICAL)

**Bulk create remaining**:
3. `process_adherence` (NUMERIC)
4. `context_efficiency` (NUMERIC)
5. `error_handling` (CATEGORICAL)
6. `output_quality` (NUMERIC)
7. `overall_quality` (NUMERIC)

**Dataset**:
8. `quality-monitoring-ground-truth` dataset

### Config Specifications

```python
SCORE_CONFIGS = [
    # CATEGORICAL configs
    {
        "name": "goal_achievement",
        "data_type": "CATEGORICAL",
        "categories": ["failed", "partial", "complete", "exceeded"],
        "description": "Did the session accomplish the user's goal?"
    },
    {
        "name": "error_handling",
        "data_type": "CATEGORICAL",
        "categories": ["poor", "struggled", "recovered", "prevented"],
        "description": "How were errors and blockers handled?"
    },

    # NUMERIC configs
    {
        "name": "tool_efficiency",
        "data_type": "NUMERIC",
        "min": 0,
        "max": 1,
        "description": "Right tool selection and usage efficiency"
    },
    {
        "name": "process_adherence",
        "data_type": "NUMERIC",
        "min": 0,
        "max": 1,
        "description": "Following proper workflows (TodoWrite, Read→Edit, skills)"
    },
    {
        "name": "context_efficiency",
        "data_type": "NUMERIC",
        "min": 0,
        "max": 1,
        "description": "Efficient use of context window and file reads"
    },
    {
        "name": "output_quality",
        "data_type": "NUMERIC",
        "min": 0,
        "max": 1,
        "description": "Quality of deliverables (code, docs, formatting)"
    },
    {
        "name": "overall_quality",
        "data_type": "NUMERIC",
        "min": 0,
        "max": 1,
        "description": "Weighted aggregate of all dimensions"
    }
]
```

---

## Phase 3: Validation Testing (10-15 min)

### Goals
- Verify all configs created correctly
- Test scoring on a real trace
- Confirm scores visible in Langfuse UI

### Tasks
1. List all configs - verify 7 production configs exist
2. Get a trace ID from recent session
3. Create one score per config on that trace
4. Check Langfuse UI to see scores

### Test Score Values

| Config | Test Value | Expected Display |
|--------|------------|------------------|
| goal_achievement | 2 | "complete" |
| tool_efficiency | 0.80 | 0.80 |
| process_adherence | 0.75 | 0.75 |
| context_efficiency | 0.70 | 0.70 |
| error_handling | 2 | "recovered" |
| output_quality | 0.85 | 0.85 |
| overall_quality | 0.76 | 0.76 |

---

## Success Criteria

- [ ] 7 score configs exist in Langfuse
- [ ] `quality-monitoring-ground-truth` dataset exists
- [ ] Test scores created on a trace
- [ ] Scores visible in Langfuse UI
- [ ] No API errors during creation

---

## Rollback Plan

If something goes wrong:
1. Configs can be deleted via `langfuse-delete-score-config` (if it exists) or UI
2. Datasets can be recreated - low risk
3. Test scores don't affect anything critical

---

## Output Artifacts

After completion:
- `03-working/config-ids.md` - Record of all created config IDs
- `03-working/enhanced-scoring-design.md` - Full design rationale
- `04-outputs/setup-complete.md` - Summary of what was created

---

*Ready to execute. See 04-steps.md for granular task tracking.*
