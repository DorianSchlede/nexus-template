---
name: langfuse-list-observations
description: "List Langfuse observations (spans, generations, events). Load when user says 'list observations', 'show spans', 'get generations'."
---

# List Observations

Get list of observations (spans, generations, events) from Langfuse.

## Usage

### CLI
```bash
uv run python scripts/list_observations.py --limit 20
uv run python scripts/list_observations.py --trace-id trace123
uv run python scripts/list_observations.py --type GENERATION
```

### Python
```python
from list_observations import list_observations

obs = list_observations(limit=20)
obs = list_observations(trace_id="trace123", type="GENERATION")
```

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| --limit | int | Max results (default 50) |
| --cursor | string | Pagination cursor |
| --trace-id | string | Filter by trace |
| --type | string | SPAN, GENERATION, or EVENT |
| --name | string | Filter by name |

## API Reference

```
GET /api/public/v2/observations
```

See: `langfuse-master/references/api-reference.md`
