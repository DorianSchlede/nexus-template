# Spawned Project: Score Config Setup

**Parent Research**: Project 27 - Langfuse Annotation and Scoring Integration
**Estimated Effort**: Small (1-2 sessions)
**Priority**: High (prerequisite for other projects)

---

## Purpose

Create all score configurations in Langfuse and validate they work correctly. This is the foundational infrastructure needed for the scoring system.

---

## Scope

### Must Do
1. Create 7 score configs in Langfuse:
   - `context_efficiency` (NUMERIC 0-1)
   - `instruction_following` (CATEGORICAL: poor/partial/good/excellent)
   - `tool_appropriateness` (NUMERIC 0-1)
   - `task_completion` (CATEGORICAL: failed/partial/complete/exceeded)
   - `error_recovery` (CATEGORICAL: poor/slow/adequate/excellent)
   - `cost_efficiency` (NUMERIC 0-1)
   - `overall_quality` (NUMERIC 0-1)

2. Create ground truth dataset: `self-improvement-ground-truth`

3. Test scoring on 5 sample sessions manually

### Out of Scope
- Building the automated scorer (separate project)
- Weekly analysis workflow (separate project)
- Human labeling at scale (separate project)

---

## Dependencies

**Requires**:
- Langfuse running at localhost:3002
- Scoring dimensions defined (from research - DONE)

**Enables**:
- Session Scorer project
- Ground Truth Bootstrap project

---

## Implementation Steps

### Phase 1: Create Score Configs

```python
# Score config definitions
SCORE_CONFIGS = [
    {
        "name": "context_efficiency",
        "dataType": "NUMERIC",
        "minValue": 0,
        "maxValue": 1,
        "description": "How efficiently context was used (0=wasteful, 1=optimal)"
    },
    {
        "name": "instruction_following",
        "dataType": "CATEGORICAL",
        "categories": [
            {"label": "poor", "value": 0},
            {"label": "partial", "value": 1},
            {"label": "good", "value": 2},
            {"label": "excellent", "value": 3}
        ],
        "description": "How well instructions were followed"
    },
    {
        "name": "tool_appropriateness",
        "dataType": "NUMERIC",
        "minValue": 0,
        "maxValue": 1,
        "description": "Appropriateness of tool choices (0=wrong tools, 1=perfect)"
    },
    {
        "name": "task_completion",
        "dataType": "CATEGORICAL",
        "categories": [
            {"label": "failed", "value": 0},
            {"label": "partial", "value": 1},
            {"label": "complete", "value": 2},
            {"label": "exceeded", "value": 3}
        ],
        "description": "Whether the task was completed"
    },
    {
        "name": "error_recovery",
        "dataType": "CATEGORICAL",
        "categories": [
            {"label": "poor", "value": 0},
            {"label": "slow", "value": 1},
            {"label": "adequate", "value": 2},
            {"label": "excellent", "value": 3}
        ],
        "description": "Quality of error handling and recovery"
    },
    {
        "name": "cost_efficiency",
        "dataType": "NUMERIC",
        "minValue": 0,
        "maxValue": 1,
        "description": "Cost relative to task complexity (0=expensive, 1=efficient)"
    },
    {
        "name": "overall_quality",
        "dataType": "NUMERIC",
        "minValue": 0,
        "maxValue": 1,
        "description": "Weighted aggregate of all dimensions"
    }
]
```

### Phase 2: Create Ground Truth Dataset

```bash
python 03-skills/langfuse/langfuse-create-dataset/scripts/create_dataset.py \
  --name "self-improvement-ground-truth" \
  --description "Human-labeled sessions for scorer calibration"
```

### Phase 3: Manual Testing

1. Select 5 diverse sessions:
   - 1 small (<10 traces)
   - 2 medium (10-50 traces)
   - 2 large (50+ traces)

2. For each session:
   - Review traces manually
   - Score all 6 dimensions
   - Calculate overall_quality
   - Attach scores to first trace of session

3. Validate scores appear in Langfuse UI

---

## Success Criteria

- [ ] All 7 score configs created in Langfuse
- [ ] Ground truth dataset exists
- [ ] 5 sessions scored manually
- [ ] Scores visible in Langfuse UI
- [ ] Documented any API quirks discovered

---

## Risks

| Risk | Mitigation |
|------|------------|
| Score config API changes | Test all configs immediately after creation |
| Categorical value mapping | Document exact integer mappings |

---

## Outputs

- 7 score configs in Langfuse
- 1 ground truth dataset
- 5 manually scored sessions
- Updated documentation with any API notes

---

*Ready to execute as Project 28*
