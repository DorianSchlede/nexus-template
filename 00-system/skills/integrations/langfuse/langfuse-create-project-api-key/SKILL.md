---
name: langfuse-create-project-api-key
description: "Create new API key for project. Load when user says 'create api key', 'new key', 'generate key'."
---

# Create Project API Key

Create a new API key for a project.

**Note**: This endpoint may be Cloud-only or require admin access.

## Usage

```bash
uv run python scripts/create_project_api_key.py --project "proj-abc123" --note "Production key"
```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--project` | Yes | Project ID |
| `--note` | No | Description/note for the key |

## API Reference

```
POST /api/public/v2/projects/{projectId}/api-keys
```
