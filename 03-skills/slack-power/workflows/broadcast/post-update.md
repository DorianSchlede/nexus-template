---
name: Post Update
slug: post-update
category: broadcast
description: Share progress or updates to a Slack channel or DM
triggers:
  - "post update"
  - "share to slack"
  - "send update to"
  - "post to channel"
  - "slack update"
inputs:
  required:
    - name: destination
      type: string
      description: "#channel or @user to post to"
    - name: content
      type: string
      description: "The update content or 'generate' to create from context"
  optional:
    - name: format
      type: string
      default: "standard"
      description: "'standard', 'standup', 'summary', 'announcement'"
outputs:
  - type: slack_message
    destination: slack
    requires_confirmation: true
scripts:
  - send_message.py
---

# Post Update

Share updates to Slack channels or DMs. Always confirms before posting.

## Workflow

### Step 1: Determine Content

**Option A - User provides content:**
Use the content directly.

**Option B - Generate from context:**
If content is "generate" or similar, create update from:
- Recent completed todos
- Current project progress
- Session accomplishments

### Step 2: Select Format

| Format | Structure |
|--------|-----------|
| **standard** | Plain message with content |
| **standup** | What I did / What I'm doing / Blockers |
| **summary** | TL;DR + bullet points |
| **announcement** | Header + body + call to action |

### Step 3: Format Message

**Standard:**
```
{content}
```

**Standup:**
```
*Standup Update - {date}*

*Done:*
• {completed items}

*Doing:*
• {current focus}

*Blockers:*
• {any blockers or "None"}
```

**Summary:**
```
*{title}*

TL;DR: {one-liner}

• {point 1}
• {point 2}
• {point 3}
```

**Announcement:**
```
:mega: *{title}*

{body}

{call to action if any}
```

### Step 4: Confirm Before Posting

**ALWAYS show preview and confirm:**

```
Ready to post to {destination}:

---
{formatted message}
---

Post this message? (yes/no)
```

Only proceed if user confirms.

### Step 5: Send Message

```bash
python 00-system/skills/slack/slack-master/scripts/send_message.py --channel "{destination}" --text "{message}"
```

### Step 6: Confirm Success

Display: "Posted to {destination}"

## Example Usage

- "post update to #team: finished the API integration" → Standard message
- "share standup to #daily" → Generates standup format
- "send summary of today's work to @burak" → Summary DM
