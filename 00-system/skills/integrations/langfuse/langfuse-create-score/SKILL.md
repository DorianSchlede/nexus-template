---
name: langfuse-create-score
description: "Create a score. Load when user says 'create score', 'add evaluation', 'score trace'."
---

# Create Score

Add a score/evaluation to a trace or observation.

## Usage

```bash
# Score a trace
python scripts/create_score.py --trace "trace-abc" --name "accuracy" --value 0.95

# Score an observation
python scripts/create_score.py --trace "trace-abc" --observation "obs-xyz" --name "quality" --value 1

# With comment
python scripts/create_score.py --trace "trace-abc" --name "correct" --value 1 --comment "Perfect response"
```

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| --trace | string | **Required**. Trace ID |
| --name | string | **Required**. Score name |
| --value | float | Score value |
| --observation | string | Observation ID (optional) |
| --comment | string | Comment |
| --config-id | string | Score config ID |

## API Reference

```
POST /api/public/scores
```
