---
name: langfuse-get-score-config
description: "Get a score config by ID. Load when user says 'get score config', 'show metric'."
---

# Get Score Config

Get a specific score configuration by ID.

## Usage

```bash
uv run python scripts/get_score_config.py --id "config-abc123"
```

## API Reference

```
GET /api/public/score-configs/{id}
```
