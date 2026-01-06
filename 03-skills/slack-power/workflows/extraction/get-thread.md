---
name: Get Thread
slug: get-thread
category: extraction
description: Pull full DM or channel history with a person or from a channel
triggers:
  - "get thread"
  - "get dm with"
  - "get messages from"
  - "pull slack history"
  - "slack history"
  - "dm history"
inputs:
  required:
    - name: target
      type: string
      description: "@username for DM or #channel for channel history"
  optional:
    - name: limit
      type: number
      default: 50
      description: "Number of messages to retrieve"
outputs:
  - type: markdown
    destination: display
    description: "Formatted conversation history"
scripts:
  - dm_history.py
  - channel_history.py
---

# Get Thread

Pull conversation history from DMs or channels.

## Workflow

### Step 1: Identify Target Type

- Starts with `@` → DM with user
- Starts with `#` → Channel history
- Plain name → Try to match user first, then channel

### Step 2: Execute Retrieval

**For DMs:**
```bash
python 00-system/skills/slack/slack-master/scripts/dm_history.py {username} --limit {limit}
```

**For Channels:**
```bash
python 00-system/skills/slack/slack-master/scripts/channel_history.py --channel {channel_id} --limit {limit}
```

### Step 3: Format Output

Display chronologically with timestamps and usernames.

### Step 4: Save Option

If user wants to save, write to:
`04-workspace/07-insights/slack-extracts/{date}-{target}-thread.md`

## Example Usage

- "get dm with burak" → Pulls DM history with @burakozafsar
- "get thread from #engineering" → Pulls channel history
- "slack history with @lu.danisch last 100" → Pulls 100 messages
