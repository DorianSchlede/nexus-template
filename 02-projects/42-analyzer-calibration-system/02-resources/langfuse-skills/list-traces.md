---
name: langfuse-list-traces
description: "List Langfuse traces. Load when user says 'list traces', 'show traces', 'get traces', 'recent traces'."
---

# List Traces

Get list of LLM traces from Langfuse.

## Usage

### CLI
```bash
python scripts/list_traces.py --limit 20
python scripts/list_traces.py --user-id user123
python scripts/list_traces.py --session-id sess123
python scripts/list_traces.py --name "chat-completion"
```

### Python
```python
from list_traces import list_traces

traces = list_traces(limit=20)
traces = list_traces(user_id="user123")
```

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| --limit | int | Max results (default 50) |
| --page | int | Page number |
| --user-id | string | Filter by user |
| --session-id | string | Filter by session |
| --name | string | Filter by trace name |
| --from | ISO8601 | Start time |
| --to | ISO8601 | End time |

## API Reference

```
GET /api/public/traces
```

See: `langfuse-master/references/api-reference.md`
