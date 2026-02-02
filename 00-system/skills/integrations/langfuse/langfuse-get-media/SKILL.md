---
name: langfuse-get-media
description: "Get media content by ID. Load when user says 'get media', 'download media', 'media content'."
---

# Get Media

Retrieve media content (images, audio, etc.) by ID.

## Usage

```bash
uv run python scripts/get_media.py --media "media-abc123"
```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--media` | Yes | Media ID |

## API Reference

```
GET /api/public/media/{mediaId}
```
