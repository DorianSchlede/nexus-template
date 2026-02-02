---
name: langfuse-create-comment
description: "Add comment to trace/observation. Load when user says 'create comment', 'add comment', 'comment on trace'."
---

# Create Comment

Add a comment to a trace or observation.

## Usage

```bash
uv run python scripts/create_comment.py --type "TRACE" --id "trace-abc" --content "This trace shows high latency"
uv run python scripts/create_comment.py --type "OBSERVATION" --id "obs-123" --content "Review needed" --author "reviewer@example.com"
```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--type` | Yes | Object type: TRACE or OBSERVATION |
| `--id` | Yes | Object ID to comment on |
| `--content` | Yes | Comment content |
| `--author` | No | Author user ID |

## API Reference

```
POST /api/public/comments
```
