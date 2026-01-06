---
name: langfuse-delete-traces
description: "Bulk delete traces. Load when user says 'bulk delete traces', 'delete multiple traces', 'purge traces'."
---

# Bulk Delete Traces

Delete multiple traces matching filter criteria.

## Usage

```bash
python scripts/delete_traces.py --ids "trace-1,trace-2,trace-3"
python scripts/delete_traces.py --filter '{"name": "test-trace"}'
```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--ids` | No | Comma-separated trace IDs |
| `--filter` | No | JSON filter object |

## API Reference

```
DELETE /api/public/traces
```
