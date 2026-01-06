# HeyReach Setup Guide

Complete setup instructions for HeyReach API integration.

---

## Prerequisites

- Active HeyReach account
- API access enabled (check your subscription plan)

---

## Step 1: Get Your API Key

1. Log into HeyReach at https://app.heyreach.io
2. Navigate to **Settings** → **API** (or **Integrations**)
3. Click **Generate API Key** or copy your existing key
4. Save the API key securely - you'll need it for configuration

---

## Step 2: Configure Environment

Add to your `.env` file in the Nexus root directory:

```env
HEYREACH_API_KEY=your-api-key-here
```

---

## Step 3: Verify Configuration

Run the config checker:

```bash
python 00-system/skills/heyreach/heyreach-master/scripts/check_heyreach_config.py --json
```

Expected output:
```json
{
  "configured": true,
  "api_key_found": true,
  "api_key_valid": true,
  "ai_action": "proceed_with_operation"
}
```

---

## API Details

| Property | Value |
|----------|-------|
| Base URL | `https://api.heyreach.io/api/public/` |
| Auth Header | `X-API-KEY` |
| Rate Limit | 300 requests/minute |
| Content Type | `application/json` |

---

## Common Issues

### Invalid API Key
- Verify key is copied correctly (no extra spaces)
- Check if key has expired
- Confirm API access is enabled for your account

### 403 Forbidden
- Your subscription may not include API access
- Contact HeyReach support to verify API availability

### Rate Limiting (429)
- Default: 300 requests/minute
- Client automatically retries with backoff
- For bulk operations, add delays between requests

---

## Security Best Practices

1. Never commit `.env` file to version control
2. Rotate API keys periodically
3. Use environment variables in production
4. Monitor API usage for anomalies

---

**Version**: 1.0
**Updated**: 2025-12-19
