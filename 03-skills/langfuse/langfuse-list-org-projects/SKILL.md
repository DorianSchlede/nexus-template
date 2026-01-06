---
name: langfuse-list-org-projects
description: "List projects in org. Load when user says 'list org projects', 'org projects', 'all projects'."
---

# List Organization Projects

List all projects in an organization.

**Note**: This endpoint may be Cloud-only or require admin access.

## Usage

```bash
python scripts/list_org_projects.py --org "org-abc123"
```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--org` | Yes | Organization ID |

## API Reference

```
GET /api/public/v2/organizations/{orgId}/projects
```
