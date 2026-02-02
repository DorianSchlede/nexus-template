---
name: langfuse-list-score-configs
description: "List score configurations. Load when user says 'list score configs', 'show scoring', 'evaluation configs'."
---

# List Score Configs

Get list of score configurations for evaluation metrics.

## Usage

```bash
uv run python scripts/list_score_configs.py
uv run python scripts/list_score_configs.py --limit 20
```

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| --limit | int | Max results (default 50) |
| --page | int | Page number |

## API Reference

```
GET /api/public/score-configs
```
