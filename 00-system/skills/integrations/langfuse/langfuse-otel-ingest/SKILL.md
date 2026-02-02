---
name: langfuse-otel-ingest
description: "Ingest OpenTelemetry data. Load when user says 'otel ingest', 'opentelemetry', 'otlp'."
---

# OpenTelemetry Ingest

Ingest OpenTelemetry Protocol (OTLP) data into Langfuse.

## Usage

```bash
uv run python scripts/otel_ingest.py --file otel_spans.json
uv run python scripts/otel_ingest.py --spans '[...]'
```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--file` | No | JSON file with OTLP spans |
| `--spans` | No | JSON string of resource spans |

## OTLP Format

```json
{
  "resourceSpans": [
    {
      "resource": { "attributes": [...] },
      "scopeSpans": [
        {
          "spans": [...]
        }
      ]
    }
  ]
}
```

## API Reference

```
POST /api/public/otel/v1/traces
```
