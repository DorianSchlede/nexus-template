# Slack Setup Guide

Complete guide for setting up Slack integration with Nexus.

---

## Overview

This integration uses **User OAuth** - each person authenticates individually and messages appear as themselves (not a bot).

**Credentials are included** - You just need to authorize your account.

---

## Quick Setup (30 seconds)

### Step 1: Add Credentials to .env

Copy these lines to your `.env` file (in project root):

```bash
# Slack App Credentials (shared - identifies the app)
SLACK_CLIENT_ID=3499735674373.10122697240033
SLACK_CLIENT_SECRET=dce1a170a489edab7234411850b8aeab
```

Or copy from `credentials/slack-credentials.json` in this skill folder.

### Step 2: Authorize Your Account

Run the setup script from this skill's folder:

```bash
# If skill is in 03-skills/slack/:
python 03-skills/slack/slack-master/scripts/setup_slack.py

# If skill is in 00-system/skills/slack/:
python 00-system/skills/slack/slack-master/scripts/setup_slack.py
```

Your browser opens → Sign in to Slack → Click "Allow" → Done!

Your personal token is saved to `.env` as `SLACK_USER_TOKEN`.

**Note**: The script automatically finds your project's `.env` file by looking for `CLAUDE.md` in parent directories.

### Step 3: Verify

```bash
# If skill is in 03-skills/slack/:
python 03-skills/slack/slack-master/scripts/check_slack_config.py

# If skill is in 00-system/skills/slack/:
python 00-system/skills/slack/slack-master/scripts/check_slack_config.py
```

You should see:
```
[OK] SLACK_USER_TOKEN configured
[OK] API connection successful
    User: your-username
    Team: your-workspace
```

**That's it!** You're ready to use Slack commands.

---

## How It Works

| Component | What It Is | Who Has It |
|-----------|-----------|------------|
| Client ID + Secret | Identifies the Slack App | Shared (included in package) |
| User Token | Your personal authorization | You (created in Step 2) |

- **Client credentials** are safe to share - they just identify which app is making requests
- **User token** is personal - never share it, it grants access to your Slack account

---

## Team Deployment

Since credentials are included, team setup is simple:

### Each Team Member

1. Copy the Client ID/Secret to their `.env` (from credentials folder or above)
2. Run `setup_slack.py` to authorize their account
3. Done - each person has their own token

**Result**: Everyone uses the same app, but messages appear as each individual.

---

## Creating Your Own Slack App (Optional)

If you want to use your own Slack App instead of the shared one:

### Step 1: Create App from Manifest

1. Go to [api.slack.com/apps](https://api.slack.com/apps)
2. Click **Create New App** → **From an app manifest**
3. Choose your workspace
4. Select **JSON** tab
5. Paste contents of `00-system/skills/slack/credentials/slack-app-manifest.json`
6. Click **Next** → **Create**

### Step 2: Get Your Credentials

1. Go to **Basic Information** in your new app
2. Copy **Client ID** and **Client Secret**
3. Replace the values in your `.env`

### Step 3: Authorize

Run `setup_slack.py` as usual.

---

## Verify Setup

Run the check script (use the path matching your skill location):

```bash
python <skill-path>/slack-master/scripts/check_slack_config.py
```

Expected output:
```
[OK] .env file found
[OK] SLACK_USER_TOKEN configured (type: user)
[OK] API connection successful
    User: your-username
    Team: your-workspace
```

---

## Troubleshooting

### "invalid_auth" Error

**Cause**: Token is invalid or expired.

**Fix**: Re-run the OAuth setup:
```bash
python <skill-path>/slack-master/scripts/setup_slack.py
```

### "missing_scope" Error

**Cause**: Token doesn't have required scopes.

**Fix**: If using the shared app, re-authorize. If using your own app:
1. Go to your Slack App → OAuth & Permissions
2. Add the missing scope under User Token Scopes
3. Re-run OAuth setup to get new token

### "channel_not_found" Error

**Cause**: Channel doesn't exist or you're not a member.

**Fix**:
- Verify channel exists
- Join the channel first
- Check if it's a private channel you don't have access to

### "not_in_channel" Error

**Cause**: Trying to post to a channel you haven't joined.

**Fix**: Join the channel first, either in Slack or via API.

### Port 8765 Already in Use

**Cause**: Another process using the callback port.

**Fix**: Wait a moment and try again, or kill the process using that port.

### "access_denied" or "oauth_authorization_url_mismatch"

**Cause**: The Slack app isn't installed in your workspace.

**Fix**:
1. Ask a workspace admin to install the Nexus Integration app
2. Or create your own app using the manifest (see "Creating Your Own Slack App")

---

## Security Notes

### What's Safe to Share

- **Client ID** - Public identifier for the app
- **Client Secret** - Shared among team (identifies app, not users)
- **App Manifest** - Template for creating apps

### What's Personal (Never Share)

- **User Token** (`SLACK_USER_TOKEN`) - Grants access to YOUR Slack account
- Already in `.gitignore`
- Stored only in your local `.env`

### Revoking Access

To revoke Nexus's access to your Slack:
1. Go to your Slack workspace
2. Click your profile → **Settings & administration** → **Manage apps**
3. Find "Nexus Integration" and remove it

---

## Next Steps

After setup, you can:
- `slack connect` - Verify connection
- `send slack message` - Send messages
- `list slack channels` - See available channels
- `search slack` - Search messages

See the full skill list with: `list skills`
