---
name: slack
description: "send slack message, search slack, list channels, upload to slack."
version: "1.1"
---

# Slack Integration

Complete Slack integration with 32+ API operations using User OAuth.

## Purpose

Provides full Slack workspace interaction:
- Send, update, delete, and schedule messages
- List and create channels
- Search messages and files
- Manage reactions and pins
- Set reminders
- Upload files
- Direct messages and group DMs

## Quick Setup (30 seconds)

**Credentials are included** - just authorize your account:

1. Add to `.env`:
```bash
SLACK_CLIENT_ID=3499735674373.10122697240033
SLACK_CLIENT_SECRET=dce1a170a489edab7234411850b8aeab
```

2. Run: `python 00-system/skills/slack/slack-master/scripts/setup_slack.py`

3. Click "Allow" in browser - done!

## Package Contents

```
slack/
├── credentials/
│   ├── slack-credentials.json    # Client ID + Secret (copy to .env)
│   └── slack-app-manifest.json   # For creating your own app
├── slack-connect/                # Entry point skill
└── slack-master/                 # Scripts and references
    ├── scripts/                  # 32 API operation scripts
    └── references/               # Setup, API docs, troubleshooting
```

## Available Operations

| Category | Operations |
|----------|------------|
| Messages | send, update, delete, schedule |
| Channels | list, create, info, history, join, leave, invite |
| Users | list, info |
| DMs | list, open, history (direct + group) |
| Files | upload, list, search |
| Reactions | add, remove, get |
| Pins | add, remove, list |
| Reminders | create, list, delete |
| Search | messages, files |
| Team | info |

## Example Usage

```bash
# Send message
uv run python slack-master/scripts/send_message.py --channel "#general" --text "Hello!"

# Search messages
uv run python slack-master/scripts/search_messages.py --query "project update"

# List channels
uv run python slack-master/scripts/list_channels.py --json
```

## Authentication

Uses **User OAuth** - messages appear as you, not a bot. Each team member gets their own token.

---

**Version**: 1.0
**Tested**: 29/29 endpoint tests passing
