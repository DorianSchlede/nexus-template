---
name: langfuse-list-models
description: "List Langfuse models. Load when user says 'list models', 'show models', 'model costs'."
---

# List Models

Get list of configured models (for cost tracking).

## Usage

### CLI
```bash
python scripts/list_models.py
python scripts/list_models.py --limit 20
```

### Python
```python
from list_models import list_models

models = list_models()
```

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| --limit | int | Max results (default 50) |
| --page | int | Page number |

## API Reference

```
GET /api/public/models
```

See: `langfuse-master/references/api-reference.md`
