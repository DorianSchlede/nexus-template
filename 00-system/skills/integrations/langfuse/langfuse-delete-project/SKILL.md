---
name: langfuse-delete-project
description: "Delete a project. Load when user says 'delete project', 'remove project'."
---

# Delete Project

Delete a Langfuse project.

**Warning**: This is a destructive operation and cannot be undone.

**Note**: This endpoint may be Cloud-only or require admin access.

## Usage

```bash
uv run python scripts/delete_project.py --project "proj-abc123"
```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--project` | Yes | Project ID |

## API Reference

```
DELETE /api/public/v2/projects/{projectId}
```
