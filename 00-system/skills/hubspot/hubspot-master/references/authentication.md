# HubSpot Authentication

## Overview

HubSpot offers two authentication methods:
1. **Private App Access Tokens** (recommended for single account)
2. **OAuth 2.0** (for public apps / multi-account)

This integration uses **Private App Access Tokens**.

---

## Private App Setup

### Step 1: Create Private App

1. Go to **HubSpot Settings** → **Integrations** → **Private Apps**
2. Click **Create a private app**
3. Enter app name: `Nexus Integration`
4. Add description (optional)

### Step 2: Configure Scopes

Select these scopes for full integration functionality:

**CRM Scopes:**
- `crm.objects.contacts.read`
- `crm.objects.contacts.write`
- `crm.objects.companies.read`
- `crm.objects.companies.write`
- `crm.objects.deals.read`
- `crm.objects.deals.write`

**Engagement Scopes:**
- `crm.objects.emails.read`
- `crm.objects.emails.write`
- `crm.objects.calls.read`
- `crm.objects.calls.write`
- `crm.objects.notes.read`
- `crm.objects.notes.write`
- `crm.objects.meetings.read`
- `crm.objects.meetings.write`

### Step 3: Get Access Token

1. Click **Create app**
2. Copy the access token (starts with `pat-...`)
3. Store securely - you won't see it again!

---

## Environment Configuration

Add to your `.env` file:
```
HUBSPOT_ACCESS_TOKEN=pat-na1-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

---

## Using the Token

Include in all API requests as Bearer token:

```python
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}
```

---

## Token Management

### Token Properties
- **Expiration**: Never expires (unlike OAuth tokens)
- **Rotation**: Can rotate anytime in HubSpot settings
- **Revocation**: Delete private app to revoke

### Security Best Practices
- Never commit tokens to git
- Use environment variables
- Rotate if compromised
- Use minimum required scopes

---

## Troubleshooting

### 401 Unauthorized
- Token is invalid or revoked
- Check token starts with `pat-`
- Verify token is set in environment

### 403 Forbidden
- Missing required scope
- Add scope in Private App settings
- **Important**: Token needs re-creation after scope changes

---

## References

- [Private Apps Documentation](https://developers.hubspot.com/docs/api/private-apps)
- [Authentication Overview](https://developers.hubspot.com/docs/guides/apps/authentication/intro-to-auth)
