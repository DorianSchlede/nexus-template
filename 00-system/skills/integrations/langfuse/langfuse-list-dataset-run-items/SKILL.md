---
name: langfuse-list-dataset-run-items
description: "List dataset run items. Load when user says 'list run items', 'show run results', 'evaluation results'."
---

# List Dataset Run Items

Get list of items from a dataset evaluation run.

## Usage

### CLI
```bash
uv run python scripts/list_dataset_run_items.py --dataset "my-dataset" --run "run-2024-01"
uv run python scripts/list_dataset_run_items.py --dataset "my-dataset" --run "run-2024-01" --limit 20
```

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| --dataset | string | Filter by dataset name |
| --run | string | Filter by run name |
| --limit | int | Max results (default 50) |
| --page | int | Page number |

## API Reference

```
GET /api/public/dataset-run-items
```
