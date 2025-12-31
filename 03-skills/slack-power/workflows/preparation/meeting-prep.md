---
name: Meeting Prep
slug: meeting-prep
category: preparation
description: Aggregate all context with a person before a meeting
triggers:
  - "meeting prep"
  - "prep for call"
  - "context before meeting"
  - "prepare for meeting with"
  - "get ready for call"
inputs:
  required:
    - name: person
      type: string
      description: "@username or name of person you're meeting"
  optional:
    - name: days
      type: number
      default: 14
      description: "How far back to look"
    - name: topic
      type: string
      description: "Specific topic to focus on"
outputs:
  - type: markdown
    destination: workspace
    default_path: "04-workspace/07-insights/meeting-prep/{date}-{person}.md"
scripts:
  - dm_history.py
  - search_messages.py
---

# Meeting Prep

Get full context with a person before a meeting so you walk in prepared.

## Workflow

### Step 1: Pull DM History

```bash
python 00-system/skills/slack/slack-master/scripts/dm_history.py {username} --limit 100
```

### Step 2: Search Shared Channels

Find mentions of this person or conversations involving them:
```bash
python 00-system/skills/slack/slack-master/scripts/search_messages.py --query "from:@{username}" --count 50
```

### Step 3: Analyze Content

Extract and summarize:

| Section | Content |
|---------|---------|
| **Recent Topics** | Main themes from last {days} days |
| **Open Items** | Unresolved discussions, pending decisions |
| **Their Asks** | Things they requested from you |
| **Your Asks** | Things you requested from them |
| **Shared Decisions** | Agreements, conclusions reached |
| **Technical Context** | Schemas, code, specs discussed |

### Step 4: Format Prep Doc

```markdown
# Meeting Prep: {person}
Generated: {date}
Meeting: [add time/purpose]

## TL;DR
{2-3 sentence summary of current state}

## Recent Discussion Topics
1. {topic} - {status}
2. {topic} - {status}

## Open Items

### They're Waiting On You
- [ ] {item} (mentioned {date})

### You're Waiting On Them
- [ ] {item} (mentioned {date})

## Key Decisions Made
- {decision} ({date})

## Technical Context
{any schemas, code, or specs recently discussed}

## Suggested Talking Points
1. Follow up on {open item}
2. Clarify {unclear topic}
3. Decide on {pending decision}

---
*Source: Slack DMs + shared channels, last {days} days*
```

### Step 5: Save to Workspace

Default: `04-workspace/07-insights/meeting-prep/{date}-{person}.md`

Confirm with user before saving.

## Example Usage

- "meeting prep with burak" → Full context dump
- "prep for call with @lu.danisch about onboarding" → Focused on topic
- "get ready for meeting with Bene tomorrow" → Standard prep
