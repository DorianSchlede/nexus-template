---
name: langfuse-get-observation
description: "Get specific Langfuse observation. Load when user says 'get observation', 'observation details', 'show span {id}'."
---

# Get Observation

Get detailed view of a specific observation.

## Usage

### CLI
```bash
python scripts/get_observation.py --id <observation_id>
```

### Python
```python
from get_observation import get_observation

obs = get_observation("obs-abc123")
```

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| --id | string | Observation ID (required) |

## API Reference

```
GET /api/public/observations/{observationId}
```

See: `langfuse-master/references/api-reference.md`
