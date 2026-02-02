---
name: langfuse-list-org-api-keys
description: "List org-level API keys. Load when user says 'org api keys', 'organization keys'."
---

# List Organization API Keys

List all API keys at the organization level.

**Note**: This endpoint may be Cloud-only or require admin access.

## Usage

```bash
uv run python scripts/list_org_api_keys.py --org "org-abc123"
```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--org` | Yes | Organization ID |

## API Reference

```
GET /api/public/v2/organizations/{orgId}/api-keys
```
