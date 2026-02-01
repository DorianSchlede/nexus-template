---
name: langfuse-batch-ingest
description: "Batch ingest traces/spans/events. Load when user says 'batch ingest', 'bulk import', 'ingest data'."
---

# Batch Ingest

Ingest multiple traces, spans, generations, and events in a single request.

## Usage

```bash
python scripts/batch_ingest.py --file events.json
python scripts/batch_ingest.py --batch '[{"type": "trace-create", "body": {...}}]'
```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--file` | No | JSON file with batch array |
| `--batch` | No | JSON string of batch array |

## Batch Format

```json
{
  "batch": [
    {
      "type": "trace-create",
      "body": { "id": "trace-1", "name": "my-trace" }
    },
    {
      "type": "span-create",
      "body": { "traceId": "trace-1", "name": "my-span" }
    }
  ]
}
```

## Supported Types

- `trace-create`
- `span-create`, `span-update`
- `generation-create`, `generation-update`
- `event-create`
- `score-create`

## API Reference

```
POST /api/public/ingestion
```
