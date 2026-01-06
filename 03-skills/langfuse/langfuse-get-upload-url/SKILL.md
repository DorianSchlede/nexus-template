---
name: langfuse-get-upload-url
description: "Get presigned upload URL for media. Load when user says 'upload url', 'media upload', 'presigned url'."
---

# Get Upload URL

Get a presigned URL to upload media (images, audio, etc.).

## Usage

```bash
python scripts/get_upload_url.py --trace "trace-abc" --field "input" --type "image/png"
python scripts/get_upload_url.py --trace "trace-abc" --observation "obs-123" --field "output" --type "audio/mp3"
```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--trace` | Yes | Trace ID |
| `--observation` | No | Observation ID (if attaching to observation) |
| `--field` | Yes | Field name: input, output, metadata |
| `--type` | Yes | Content type (e.g., image/png, audio/mp3) |

## API Reference

```
POST /api/public/media
```
