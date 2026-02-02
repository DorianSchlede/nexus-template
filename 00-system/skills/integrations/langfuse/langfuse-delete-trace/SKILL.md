---
name: langfuse-delete-trace
description: "Delete a single trace. Load when user says 'delete trace', 'remove trace'."
---

# Delete Trace

Delete a single trace by ID.

## Usage

```bash
uv run python scripts/delete_trace.py --id "trace-abc123"
```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--id` | Yes | Trace ID to delete |

## API Reference

```
DELETE /api/public/traces/{traceId}
```
