---
name: langfuse-update-score-config
description: "Update a score config. Load when user says 'update score config', 'modify metric'."
---

# Update Score Config

Update an existing score configuration.

## Usage

```bash
uv run python scripts/update_score_config.py --id "config-abc" --description "Updated desc"
uv run python scripts/update_score_config.py --id "config-abc" --archived
```

## API Reference

```
PATCH /api/public/score-configs/{id}
```
