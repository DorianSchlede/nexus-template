---
name: langfuse-list-comments
description: "List comments on traces/observations. Load when user says 'list comments', 'get comments', 'show comments'."
---

# List Comments

List comments filtered by object type and ID.

## Usage

```bash
python scripts/list_comments.py --type "TRACE" --id "trace-abc"
python scripts/list_comments.py --type "OBSERVATION" --id "obs-123" --limit 50
```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--type` | Yes | Object type: TRACE or OBSERVATION |
| `--id` | Yes | Object ID to list comments for |
| `--page` | No | Page number (default: 1) |
| `--limit` | No | Results per page (default: 50) |

## API Reference

```
GET /api/public/comments?objectType={type}&objectId={id}
```
