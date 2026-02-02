---
name: langfuse-update-project
description: "Update project settings. Load when user says 'update project', 'rename project'."
---

# Update Project

Update project settings.

**Note**: This endpoint may be Cloud-only or require admin access.

## Usage

```bash
uv run python scripts/update_project.py --project "proj-abc" --name "New Name"
```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--project` | Yes | Project ID |
| `--name` | No | New project name |

## API Reference

```
PUT /api/public/v2/projects/{projectId}
```
