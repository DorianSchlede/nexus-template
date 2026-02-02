---
name: langfuse-update-media
description: "Update media metadata. Load when user says 'update media', 'patch media'."
---

# Update Media

Update media metadata (e.g., mark as uploaded).

## Usage

```bash
uv run python scripts/update_media.py --media "media-abc123" --uploaded
```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--media` | Yes | Media ID |
| `--uploaded` | No | Mark as uploaded |

## API Reference

```
PATCH /api/public/media/{mediaId}
```
