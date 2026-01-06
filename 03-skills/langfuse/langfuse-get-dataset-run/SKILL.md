---
name: langfuse-get-dataset-run
description: "Get a dataset run by name. Load when user says 'get dataset run', 'show run', 'run details'."
---

# Get Dataset Run

Retrieve a specific evaluation run from a dataset.

## Usage

### CLI
```bash
python scripts/get_dataset_run.py --dataset "my-dataset" --run "run-2024-01"
```

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| --dataset | string | **Required**. Dataset name |
| --run | string | **Required**. Run name |

## API Reference

```
GET /api/public/datasets/{datasetName}/runs/{runName}
```
