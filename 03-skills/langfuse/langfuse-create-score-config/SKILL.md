---
name: langfuse-create-score-config
description: "Create a score configuration. Load when user says 'create score config', 'new metric', 'add scoring'."
---

# Create Score Config

Create a new score configuration for evaluation metrics.

## Usage

```bash
# Numeric score
python scripts/create_score_config.py --name "accuracy" --data-type NUMERIC --min 0 --max 1

# Categorical score
python scripts/create_score_config.py --name "quality" --data-type CATEGORICAL --categories "good,bad,neutral"

# Boolean score
python scripts/create_score_config.py --name "correct" --data-type BOOLEAN
```

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| --name | string | **Required**. Score name |
| --data-type | string | **Required**. NUMERIC, CATEGORICAL, or BOOLEAN |
| --min | float | Min value (for NUMERIC) |
| --max | float | Max value (for NUMERIC) |
| --categories | string | Comma-separated categories |
| --description | string | Description |

## API Reference

```
POST /api/public/score-configs
```
