---
name: langfuse-master
description: "SHARED RESOURCES - DO NOT LOAD DIRECTLY. Contains Langfuse API client, config checker, and reference documentation. Used by langfuse-connect and all operation skills."
---

# Langfuse Master (Shared Resources)

**DO NOT LOAD THIS SKILL DIRECTLY** - This is a resource library for other Langfuse skills.

## Purpose

Provides shared resources for all Langfuse integration skills:
- API client with Basic Auth
- Configuration validator
- Reference documentation

## Scripts

### langfuse_client.py
API client for Langfuse REST API.

```python
from langfuse_client import get_client

client = get_client()
traces = client.get("/traces")
```

### check_langfuse_config.py
Validates environment variables.

```bash
# Check config
uv run python check_langfuse_config.py --json

# Test connection
uv run python check_langfuse_config.py --test
```

Returns:
```json
{
  "status": "configured" | "not_configured",
  "ai_action": "proceed_with_operation" | "prompt_for_api_key",
  "missing": [...],
  "configured": [...]
}
```

## Environment Variables

Required in `.env`:
```
LANGFUSE_PUBLIC_KEY=pk-lf-...
LANGFUSE_SECRET_KEY=sk-lf-...
LANGFUSE_HOST=https://tracing.beamstudio.ai
```

## References

- [setup-guide.md](references/setup-guide.md) - Initial setup
- [api-reference.md](references/api-reference.md) - Endpoint documentation
- [authentication.md](references/authentication.md) - Auth details
- [error-handling.md](references/error-handling.md) - Common errors

## Related Skills

- `langfuse-connect` - User entry point
- `langfuse-list-traces` - GET /traces
- `langfuse-get-trace` - GET /traces/{id}
- `langfuse-list-observations` - GET /v2/observations
- `langfuse-get-observation` - GET /observations/{id}
- `langfuse-list-sessions` - GET /sessions
- `langfuse-get-session` - GET /sessions/{id}
- `langfuse-list-scores` - GET /v2/scores
- `langfuse-get-score` - GET /v2/scores/{id}
- `langfuse-list-models` - GET /models
- `langfuse-get-model` - GET /models/{id}
- `langfuse-get-project` - GET /projects
