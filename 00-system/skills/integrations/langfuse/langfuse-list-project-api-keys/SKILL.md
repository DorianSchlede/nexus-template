---
name: langfuse-list-project-api-keys
description: "List API keys for project. Load when user says 'list api keys', 'show keys', 'project keys'."
---

# List Project API Keys

List all API keys for a project.

**Note**: This endpoint may be Cloud-only or require admin access.

## Usage

```bash
python scripts/list_project_api_keys.py --project "proj-abc123"
```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--project` | Yes | Project ID |

## API Reference

```
GET /api/public/v2/projects/{projectId}/api-keys
```
