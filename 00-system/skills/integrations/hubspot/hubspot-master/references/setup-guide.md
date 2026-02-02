# HubSpot Setup Guide

## Overview

This guide walks you through setting up the HubSpot integration with Nexus using a Private App access token.

---

## Prerequisites

- HubSpot account with admin access
- Access to Settings → Integrations → Private Apps

---

## Step 1: Create a Private App

1. Log into HubSpot
2. Click the **gear icon** (Settings)
3. Navigate to: **Integrations** → **Private Apps**
4. Click **Create a private app**

### App Details

- **Name**: `Nexus Integration`
- **Description**: `Integration for Nexus workspace automation`

---

## Step 2: Configure Scopes

Select the following scopes for full integration functionality:

### CRM Scopes (Required)

| Scope | Description |
|-------|-------------|
| `crm.objects.contacts.read` | Read contact records |
| `crm.objects.contacts.write` | Create/update contacts |
| `crm.objects.companies.read` | Read company records |
| `crm.objects.companies.write` | Create/update companies |
| `crm.objects.deals.read` | Read deal records |
| `crm.objects.deals.write` | Create/update deals |

### Engagement Scopes (Optional)

| Scope | Description |
|-------|-------------|
| `crm.objects.emails.read` | Read email engagements |
| `crm.objects.emails.write` | Log emails |
| `crm.objects.calls.read` | Read call logs |
| `crm.objects.calls.write` | Log calls |
| `crm.objects.notes.read` | Read notes |
| `crm.objects.notes.write` | Create notes |
| `crm.objects.meetings.read` | Read meetings |
| `crm.objects.meetings.write` | Create meetings |

---

## Step 3: Get Your Access Token

1. Click **Create app**
2. Copy the access token displayed
3. **Important**: Save this token securely - you won't see it again!

Token format: `pat-na1-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`

---

## Step 4: Configure Nexus

### Option A: Automated Setup

Run the setup wizard:
```bash
uv run python 00-system/skills/hubspot/hubspot-master/scripts/setup_hubspot.py
```

### Option B: Manual Setup

Add to your `.env` file:
```
HUBSPOT_ACCESS_TOKEN=pat-na1-your-token-here
```

---

## Step 5: Verify Configuration

Run the config checker:
```bash
uv run python 00-system/skills/hubspot/hubspot-master/scripts/check_hubspot_config.py
```

You should see:
```
[OK] ALL CHECKS PASSED
You're ready to use HubSpot skills
```

---

## Troubleshooting

### Invalid Token

**Symptoms**: `401 Unauthorized` errors

**Fix**:
1. Verify token starts with `pat-`
2. Check token hasn't been rotated in HubSpot
3. Re-copy token from Private App settings

### Missing Scopes

**Symptoms**: `403 Forbidden` errors

**Fix**:
1. Go to Private App settings
2. Add the missing scope
3. **Important**: You must create a new token after adding scopes

### Connection Errors

**Symptoms**: Timeout or connection refused

**Fix**:
1. Check internet connection
2. Verify HubSpot service status: https://status.hubspot.com/
3. Check firewall/proxy settings

---

## Security Best Practices

1. **Never commit tokens to git** - Use `.env` files
2. **Use minimum required scopes** - Only enable what you need
3. **Rotate tokens regularly** - Especially if compromised
4. **Monitor usage** - Check Private App logs in HubSpot

---

## References

- [HubSpot Private Apps](https://developers.hubspot.com/docs/api/private-apps)
- [Authentication Overview](https://developers.hubspot.com/docs/guides/apps/authentication/intro-to-auth)
- [Scope Reference](https://developers.hubspot.com/docs/api/working-with-oauth#scopes)
