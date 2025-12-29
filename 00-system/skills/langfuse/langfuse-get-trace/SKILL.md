---
name: langfuse-get-trace
description: "Get specific Langfuse trace. Load when user says 'get trace', 'trace details', 'show trace {id}'."
---

# Get Trace

Get detailed view of a specific trace.

## Usage

### CLI
```bash
python scripts/get_trace.py --id <trace_id>
```

### Python
```python
from get_trace import get_trace

trace = get_trace("trace-abc123")
```

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| --id | string | Trace ID (required) |

## API Reference

```
GET /api/public/traces/{traceId}
```

See: `langfuse-master/references/api-reference.md`
