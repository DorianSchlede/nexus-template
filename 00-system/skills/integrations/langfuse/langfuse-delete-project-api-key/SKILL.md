---
name: langfuse-delete-project-api-key
description: "Delete an API key. Load when user says 'delete api key', 'revoke key', 'remove key'."
---

# Delete Project API Key

Delete an API key from a project.

**Warning**: This will immediately invalidate the key.

**Note**: This endpoint may be Cloud-only or require admin access.

## Usage

```bash
uv run python scripts/delete_project_api_key.py --project "proj-abc123" --key "key-xyz789"
```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--project` | Yes | Project ID |
| `--key` | Yes | API Key ID |

## API Reference

```
DELETE /api/public/v2/projects/{projectId}/api-keys/{apiKeyId}
```
