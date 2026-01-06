---
name: langfuse-list-dataset-items
description: "List dataset items. Load when user says 'list dataset items', 'show items', 'dataset items'."
---

# List Dataset Items

Get list of items in a dataset for evaluation.

## Usage

### CLI
```bash
python scripts/list_dataset_items.py --dataset "my-dataset"
python scripts/list_dataset_items.py --dataset "my-dataset" --limit 20
```

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| --dataset | string | Filter by dataset name |
| --limit | int | Max results (default 50) |
| --page | int | Page number |

## API Reference

```
GET /api/public/dataset-items
```
