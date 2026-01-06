---
name: langfuse-create-dataset
description: "Create a new Langfuse dataset. Load when user says 'create dataset', 'new dataset', 'add dataset'."
---

# Create Dataset

Create a new dataset in Langfuse for storing evaluation test cases.

## Usage

### CLI
```bash
python scripts/create_dataset.py --name "my-dataset"
python scripts/create_dataset.py --name "eval-set" --description "Production evaluation cases"
python scripts/create_dataset.py --name "test-set" --metadata '{"version": "1.0"}'
```

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| --name | string | **Required**. Dataset name (unique) |
| --description | string | Dataset description |
| --metadata | JSON | Additional metadata |

## API Reference

```
POST /api/public/v2/datasets
```
