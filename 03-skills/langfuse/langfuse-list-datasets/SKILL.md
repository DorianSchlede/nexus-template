---
name: langfuse-list-datasets
description: "List Langfuse datasets. Load when user says 'list datasets', 'show datasets', 'get datasets'."
---

# List Datasets

Get list of datasets from Langfuse for experiment evaluation.

## Usage

### CLI
```bash
python scripts/list_datasets.py
python scripts/list_datasets.py --limit 20
python scripts/list_datasets.py --page 2
```

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| --limit | int | Max results (default 50) |
| --page | int | Page number for pagination |

## API Reference

```
GET /api/public/v2/datasets
```
