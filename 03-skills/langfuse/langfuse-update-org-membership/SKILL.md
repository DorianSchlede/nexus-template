---
name: langfuse-update-org-membership
description: "Update member role. Load when user says 'update member', 'change role', 'update membership'."
---

# Update Organization Membership

Update a member's role in the organization.

**Note**: This endpoint may be Cloud-only or require admin access.

## Usage

```bash
python scripts/update_org_membership.py --org "org-abc123" --membership "mem-xyz" --role "ADMIN"
```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--org` | Yes | Organization ID |
| `--membership` | Yes | Membership ID |
| `--role` | Yes | New role: OWNER, ADMIN, MEMBER, VIEWER |

## API Reference

```
PUT /api/public/v2/organizations/{orgId}/memberships/{membershipId}
```
