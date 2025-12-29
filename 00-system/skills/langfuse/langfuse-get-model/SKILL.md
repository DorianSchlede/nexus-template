---
name: langfuse-get-model
description: "Get specific Langfuse model. Load when user says 'get model', 'model details', 'show model {id}'."
---

# Get Model

Get detailed view of a specific model.

## Usage

### CLI
```bash
python scripts/get_model.py --id <model_id>
```

### Python
```python
from get_model import get_model

model = get_model("model-abc123")
```

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| --id | string | Model ID (required) |

## API Reference

```
GET /api/public/models/{id}
```

See: `langfuse-master/references/api-reference.md`
