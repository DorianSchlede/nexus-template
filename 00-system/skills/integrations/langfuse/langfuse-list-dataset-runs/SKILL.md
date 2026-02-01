---
name: langfuse-list-dataset-runs
description: "List dataset runs. Load when user says 'list dataset runs', 'show runs', 'dataset experiments'."
---

# List Dataset Runs

Get list of evaluation runs for a dataset.

## Usage

### CLI
```bash
python scripts/list_dataset_runs.py --name "my-dataset"
python scripts/list_dataset_runs.py --name "my-dataset" --limit 10
```

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| --name | string | **Required**. Dataset name |
| --limit | int | Max results (default 50) |
| --page | int | Page number |

## API Reference

```
GET /api/public/datasets/{datasetName}/runs
```
