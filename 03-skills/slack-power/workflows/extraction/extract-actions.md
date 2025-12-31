---
name: Extract Actions
slug: extract-actions
category: extraction
description: Find commitments, TODOs, action items, and promises from Slack conversations
triggers:
  - "extract actions"
  - "find action items"
  - "what did I promise"
  - "get todos from slack"
  - "commitments from"
  - "what should I do"
inputs:
  required:
    - name: source
      type: string
      description: "@user, #channel, or 'all' for recent activity"
  optional:
    - name: days
      type: number
      default: 7
      description: "How far back to look"
    - name: filter
      type: string
      description: "'mine' for my commitments, 'theirs' for what others promised"
outputs:
  - type: markdown
    destination: workspace
    default_path: "04-workspace/07-insights/slack-extracts/{date}-actions.md"
scripts:
  - dm_history.py
  - channel_history.py
  - search_messages.py
---

# Extract Actions

Surface commitments, promises, and action items from Slack conversations.

## Workflow

### Step 1: Gather Messages

**From specific source:**
```bash
python 00-system/skills/slack/slack-master/scripts/dm_history.py {username} --limit 200
```

**Workspace-wide (recent):**
```bash
python 00-system/skills/slack/slack-master/scripts/search_messages.py --query "will do|I'll|todo|action item|follow up" --count 100
```

### Step 2: Pattern Detection

Identify action language:

**Commitment patterns (I → action):**
- "I will...", "I'll..."
- "Let me...", "I'm going to..."
- "Will get you...", "I can..."
- "I need to...", "I should..."

**Request patterns (You → action):**
- "Can you...", "Could you..."
- "Please...", "Would you mind..."
- "I need you to..."

**Task markers:**
- "TODO:", "ACTION:", "FOLLOW UP:"
- Checkboxes, numbered lists
- Deadlines, dates mentioned

### Step 3: Categorize

| Category | Description |
|----------|-------------|
| **My Commitments** | Things I promised to do |
| **Requests to Me** | Things others asked me to do |
| **Their Commitments** | Things others promised |
| **My Requests** | Things I asked others to do |

### Step 4: Extract with Context

For each action item:
- The commitment/request text
- Who made it, to whom
- When (timestamp)
- Status (if discernible - done, pending, unclear)
- Link to original message

### Step 5: Format Output

```markdown
# Action Items from {source}
Extracted: {date}
Period: Last {days} days

## My Open Commitments

### To @{person}
- [ ] {action} (Dec 30)
  Context: "{surrounding text}"

## Requests to Me

### From @{person}
- [ ] {request} (Dec 29)
  Context: "{surrounding text}"

## Pending from Others

### @{person} owes me
- [ ] {their commitment} (Dec 28)
```

### Step 6: Save Option

Default: `04-workspace/07-insights/slack-extracts/{date}-actions.md`

## Example Usage

- "extract actions from burak" → All commitments between you and Burak
- "what did I promise this week" → Your commitments, last 7 days
- "find action items in #team" → All action items from channel
