# Langfuse API Validation

**Phase**: 4 (API Validation)
**Date**: 2026-01-05

---

## Summary

| API Feature | Status | Notes |
|-------------|--------|-------|
| Score Configs | Working | NUMERIC, CATEGORICAL both work |
| Create Score | Working | Trace and observation level |
| List Scores | Working | Returns created scores |
| Annotation Queues | **NOT WORKING** | 400 Bad Request |
| Datasets | Working | Full CRUD operations |
| Dataset Items | Working | Can store ground truth |

---

## Score Configs API

### Create NUMERIC Config
```bash
python langfuse-create-score-config/scripts/create_score_config.py \
  --name "test-efficiency" \
  --data-type "NUMERIC" \
  --min 0 --max 1
```

**Response**:
```json
{
  "id": "44cb8474-9898-4b35-a825-70d1a4ea2c52",
  "name": "test-efficiency",
  "dataType": "NUMERIC",
  "minValue": 0,
  "maxValue": 1
}
```

### Create CATEGORICAL Config
```bash
python langfuse-create-score-config/scripts/create_score_config.py \
  --name "test-quality" \
  --data-type "CATEGORICAL" \
  --categories "poor,acceptable,good,excellent"
```

**Response**:
```json
{
  "id": "ba02dae1-7b6c-4401-b13a-afb6df23c35d",
  "name": "test-quality",
  "dataType": "CATEGORICAL",
  "categories": [
    {"label": "poor", "value": 0},
    {"label": "acceptable", "value": 1},
    {"label": "good", "value": 2},
    {"label": "excellent", "value": 3}
  ]
}
```

---

## Scores API

### Score at Trace Level
```bash
python langfuse-create-score/scripts/create_score.py \
  --trace "954df280-faab-4823-91a8-9a31f4628f8c" \
  --name "test-efficiency" \
  --value 0.85 \
  --config-id "44cb8474-9898-4b35-a825-70d1a4ea2c52"
```

**Result**: Score attached to trace

### Score at Observation Level
```bash
python langfuse-create-score/scripts/create_score.py \
  --trace "954df280-faab-4823-91a8-9a31f4628f8c" \
  --observation "5a7b63e6-df31-479a-b2fb-6632f9804564" \
  --name "test-efficiency" \
  --value 0.9
```

**Result**: Score attached to observation

### Score Categories
For CATEGORICAL scores, pass the value as an integer:
- 0 = "poor"
- 1 = "acceptable"
- 2 = "good"
- 3 = "excellent"

---

## Annotation Queues API

### Create Queue
```bash
python langfuse-create-annotation-queue/scripts/create_annotation_queue.py \
  --name "test-review-queue"
```

**Error**: 400 Bad Request

**Possible causes**:
- Missing required fields (scoreConfigIds?)
- API version mismatch
- Self-hosted Langfuse may not support this feature

**Workaround**: Use Datasets API for ground truth storage instead

---

## Datasets API

### Create Dataset
```bash
python langfuse-create-dataset/scripts/create_dataset.py \
  --name "test-ground-truth" \
  --description "Test dataset for ground truth labels"
```

**Response**:
```json
{
  "id": "cmk1b4o8u0003qg07v556ysoj",
  "name": "test-ground-truth"
}
```

### Create Dataset Item
```bash
python langfuse-create-dataset-item/scripts/create_dataset_item.py \
  --dataset "test-ground-truth" \
  --input '{"session_id":"...", "trace_count":8}' \
  --expected '{"efficiency":0.85, "quality":"good"}'
```

**Response**:
```json
{
  "id": "6cd9a90f-be69-4053-a3a4-df3f788c14cb",
  "input": {"session_id": "...", "trace_count": 8},
  "expectedOutput": {"quality": "good", "efficiency": 0.85}
}
```

---

## Key Findings

1. **Scoring works at both levels**
   - Trace-level: Score entire user turns
   - Observation-level: Score individual LLM responses

2. **Score config types work as expected**
   - NUMERIC: min/max range
   - CATEGORICAL: predefined labels mapped to integers

3. **Datasets are the way to store ground truth**
   - Input: session or trace reference
   - Expected output: human-labeled scores
   - Can run evaluations against datasets later

4. **Annotation queues may require UI setup**
   - API creation fails
   - May need to configure via Langfuse UI
   - Not critical for MVP - datasets work

---

## Architecture Implications

### For Scoring Pipeline
```python
# 1. Get session traces
session = get_session(session_id)

# 2. Score each trace
for trace in session.traces:
    score = evaluate_trace(trace)
    create_score(
        trace_id=trace.id,
        name="context_efficiency",
        value=score,
        config_id=config_id
    )

# 3. Aggregate session score
session_score = aggregate_scores(trace_scores)
```

### For Ground Truth
```python
# Human labels a session
dataset_item = create_dataset_item(
    dataset="ground-truth-sessions",
    input={"session_id": session_id},
    expected_output={
        "context_efficiency": 0.85,
        "instruction_following": "good",
        "overall_quality": "excellent"
    }
)
```

### For Calibration
```python
# Compare AI scores to human labels
ai_scores = get_scores(trace_id)
human_labels = get_dataset_item(item_id)

# Measure disagreement
disagreement = compare_scores(ai_scores, human_labels)
```

---

## Test Artifacts Created

| Type | ID/Name |
|------|---------|
| Score Config (NUMERIC) | test-efficiency |
| Score Config (CATEGORICAL) | test-quality |
| Dataset | test-ground-truth |
| Dataset Item | 6cd9a90f-be69-4053-a3a4-df3f788c14cb |
| Scores | 3 test scores on trace/observation |

---

*Next: Phase 5 - Pattern Identification*
