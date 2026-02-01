---
name: langfuse-delete-model
description: "Delete a model definition. Load when user says 'delete model', 'remove model'."
---

# Delete Model

Delete a model definition by ID.

## Usage

```bash
python scripts/delete_model.py --id "model-abc123"
```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--id` | Yes | Model ID |

## API Reference

```
DELETE /api/public/models/{modelId}
```
