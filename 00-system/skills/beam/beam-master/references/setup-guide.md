# Beam Setup Guide

Complete setup instructions for Beam AI integration.

## Prerequisites

- Beam AI account with workspace access
- API key generation permissions

## Step 1: Get Your API Key

1. Log into [Beam AI](https://app.beam.ai)
2. Navigate to **Settings** → **API Keys**
3. Click **Create API Key**
4. Copy the key (starts with `bm_key_`)

> **Important**: Store the API key securely - it's only shown once!

## Step 2: Find Your Workspace ID

1. In Beam, go to **Settings** → **Workspace**
2. Copy your **Workspace ID** (UUID format)

Alternatively, check the URL when in your workspace:
```
https://app.beam.ai/workspace/{workspace-id}/...
```

## Step 3: Configure Environment

Add to your `.env` file:

```bash
# Beam AI Configuration
BEAM_API_KEY=bm_key_your_api_key_here
BEAM_WORKSPACE_ID=your-workspace-id-here
```

## Step 4: Verify Setup

Run the config check:

```bash
python 00-system/skills/beam/beam-master/scripts/check_beam_config.py
```

Expected output:
```
✅ ALL CHECKS PASSED
You're ready to use Beam skills
```

## Alternative: Interactive Setup

Run the setup wizard for guided configuration:

```bash
python 00-system/skills/beam/beam-master/scripts/setup_beam.py
```

The wizard will:
1. Prompt for your API key
2. Prompt for your workspace ID
3. Test the connection
4. Save configuration to `.env`
5. Verify setup

---

## Authentication Flow

Beam uses a two-step authentication:

1. **Exchange API Key for Access Token**
   ```
   POST https://api.beamstudio.ai/auth/access-token
   Body: {"apiKey": "bm_key_xxx"}
   Response: {"idToken": "...", "refreshToken": "..."}
   ```

2. **Use Access Token in Requests**
   ```
   Authorization: Bearer {idToken}
   current-workspace-id: {workspace-id}
   ```

Access tokens expire after **1 hour**. Use the refresh token to get a new one:
```
POST https://api.beamstudio.ai/auth/refresh-token
Body: {"refreshToken": "..."}
```

---

## Troubleshooting

### "Invalid API Key"
- Verify key starts with `bm_key_`
- Check key hasn't been revoked
- Generate a new key if needed

### "Workspace Not Found"
- Verify workspace ID format (UUID)
- Ensure you have access to the workspace
- Check you're using the correct workspace

### "Unauthorized"
- Access token may have expired
- Re-run authentication flow
- Check API key permissions

---

## Security Notes

- Never commit `.env` to version control
- Rotate API keys periodically
- Use workspace-specific keys for different environments
- Restrict API key permissions to minimum required
