---
name: langfuse-create-dataset-item
description: "Create a dataset item. Load when user says 'create dataset item', 'add item', 'new test case'."
---

# Create Dataset Item

Add a new item (test case) to a dataset.

## Usage

### CLI
```bash
# Basic item
python scripts/create_dataset_item.py --dataset "my-dataset" --input '{"query": "Hello"}' --expected '{"response": "Hi"}'

# With metadata
python scripts/create_dataset_item.py --dataset "my-dataset" --input '{"q": "test"}' --metadata '{"source": "prod"}'
```

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| --dataset | string | **Required**. Dataset name |
| --input | JSON | **Required**. Input data for the test case |
| --expected | JSON | Expected output (ground truth) |
| --metadata | JSON | Additional metadata |
| --id | string | Custom item ID |

## API Reference

```
POST /api/public/dataset-items
```
