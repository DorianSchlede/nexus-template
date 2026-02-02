---
name: langfuse-delete-dataset-item
description: "Delete a dataset item. Load when user says 'delete dataset item', 'remove item'."
---

# Delete Dataset Item

Delete a dataset item by ID.

## Usage

### CLI
```bash
uv run python scripts/delete_dataset_item.py --id "item-abc123"
```

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| --id | string | **Required**. Item ID to delete |

## API Reference

```
DELETE /api/public/dataset-items/{id}
```
