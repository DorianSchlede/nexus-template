---
name: langfuse-delete-org-membership
description: "Remove member from org. Load when user says 'remove member', 'delete membership', 'revoke access'."
---

# Delete Organization Membership

Remove a member from the organization.

**Note**: This endpoint may be Cloud-only or require admin access.

## Usage

```bash
uv run python scripts/delete_org_membership.py --org "org-abc123" --membership "mem-xyz"
```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--org` | Yes | Organization ID |
| `--membership` | Yes | Membership ID |

## API Reference

```
DELETE /api/public/v2/organizations/{orgId}/memberships/{membershipId}
```
