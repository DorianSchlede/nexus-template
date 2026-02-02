---
name: langfuse-list-sessions
description: "List Langfuse sessions. Load when user says 'list sessions', 'show sessions', 'get sessions'."
---

# List Sessions

Get list of user sessions from Langfuse.

## Usage

### CLI
```bash
uv run python scripts/list_sessions.py --limit 20
uv run python scripts/list_sessions.py --from 2025-01-01T00:00:00Z
```

### Python
```python
from list_sessions import list_sessions

sessions = list_sessions(limit=20)
```

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| --limit | int | Max results (default 50) |
| --page | int | Page number |
| --from | ISO8601 | Start time |
| --to | ISO8601 | End time |

## API Reference

```
GET /api/public/sessions
```

See: `langfuse-master/references/api-reference.md`
