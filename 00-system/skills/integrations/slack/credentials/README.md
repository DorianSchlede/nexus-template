# Slack Credentials Setup

## Quick Start

### Step 1: Create a Slack App

1. Go to [api.slack.com/apps](https://api.slack.com/apps)
2. Click **Create New App** → **From an app manifest**
3. Select your workspace
4. Paste contents of `slack-app-manifest.json`
5. Click **Create**

### Step 2: Get Your Credentials

1. Go to **Basic Information** in your app settings
2. Copy **Client ID** and **Client Secret**
3. Add to your `.env` file:

```bash
SLACK_CLIENT_ID=your-client-id
SLACK_CLIENT_SECRET=your-client-secret
```

### Step 3: Authorize Your Account

```bash
uv run python 00-system/skills/slack/slack-master/scripts/setup_slack.py
```

Browser opens → Sign in → Click "Allow" → Done!

Your user token is automatically saved to `.env`.

---

## What's in This Folder

| File | Purpose |
|------|---------|
| `slack-app-manifest.json` | Template to create your Slack app |
| `README.md` | This guide |

---

## Security

All credentials live in `.env` (already in `.gitignore`):

| Key | Purpose |
|-----|---------|
| `SLACK_CLIENT_ID` | Identifies your Slack app |
| `SLACK_CLIENT_SECRET` | App authentication |
| `SLACK_USER_TOKEN` | Your personal access (created during setup) |

**Never commit `.env` to git.**
