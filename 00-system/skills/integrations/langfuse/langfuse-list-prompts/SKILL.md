---
name: langfuse-list-prompts
description: "List Langfuse prompts. Load when user says 'list prompts', 'show prompts', 'get prompts', 'langfuse prompts'."
---

# List Prompts

Get list of prompts from Langfuse with optional filtering.

## Usage

### CLI
```bash
uv run python scripts/list_prompts.py
uv run python scripts/list_prompts.py --limit 20
uv run python scripts/list_prompts.py --name "my-prompt"
uv run python scripts/list_prompts.py --label production
uv run python scripts/list_prompts.py --tag "v1"
```

### Python
```python
from list_prompts import list_prompts

prompts = list_prompts(limit=20)
prompts = list_prompts(name="my-prompt")
```

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| --limit | int | Max results (default 50) |
| --page | int | Page number for pagination |
| --name | string | Filter by prompt name |
| --label | string | Filter by label (e.g., "production", "staging") |
| --tag | string | Filter by tag |
| --from | ISO8601 | Filter prompts created after this time |
| --to | ISO8601 | Filter prompts created before this time |

## API Reference

```
GET /api/public/v2/prompts
```

Query Parameters:
- `page` (int): Page number
- `limit` (int): Items per page (max 100)
- `name` (string): Filter by name
- `label` (string): Filter by label
- `tag` (string): Filter by tag
- `fromUpdatedAt` (ISO8601): Start time filter
- `toUpdatedAt` (ISO8601): End time filter

See: `langfuse-master/references/api-reference.md`
