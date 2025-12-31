---
name: Channel Digest
slug: channel-digest
category: analysis
description: Generate a summary digest of a channel's recent activity
triggers:
  - "channel digest"
  - "was lief in"
  - "weekly summary"
  - "channel summary"
  - "zusammenfassung"
  - "what happened in"
inputs:
  required:
    - name: channel
      type: string
      description: "#channel-name to summarize"
  optional:
    - name: period
      type: string
      default: "week"
      description: "'week', 'day', or number of days"
outputs:
  - type: markdown
    destination: workspace
    default_path: "04-workspace/07-insights/slack-extracts/{date}-{channel}-digest.md"
scripts:
  - channel_history.py
---

# Channel Digest

Generate a summary of what happened in a channel over a period.

## Workflow

### Step 1: Determine Period

| Input | Days |
|-------|------|
| "week" | 7 |
| "day" | 1 |
| number | that many days |

### Step 2: Pull Channel History

```bash
python 00-system/skills/slack/slack-master/scripts/channel_history.py --channel {channel_id} --limit 200 --json
```

### Step 3: Analyze Content

Group messages by:
- Topic/thread
- Date
- Participant

Identify:
- Key discussions
- Decisions made
- Action items created
- Links/resources shared
- Questions asked/answered

### Step 4: Format Digest

```markdown
# {Channel} Digest
Period: {start_date} - {end_date}

## TL;DR
{2-3 sentence summary of main activity}

## Key Discussions

### {Topic 1}
{Summary of discussion}
- Participants: @person1, @person2
- Outcome: {decision or status}

### {Topic 2}
...

## Decisions Made
- {decision} (by @person, date)
- {decision} (by @person, date)

## Action Items
- [ ] {action} - @owner
- [ ] {action} - @owner

## Resources Shared
- [{title}]({url}) - shared by @person
- [{title}]({url}) - shared by @person

## Activity Stats
- Messages: {count}
- Active participants: {count}
- Links shared: {count}

---
*Generated from #{channel}, {period}*
```

### Step 5: Save Option

Ask user: "Save digest to workspace? (y/n)"

Default path: `04-workspace/07-insights/slack-extracts/{date}-{channel}-digest.md`

## Example Usage

- "channel digest #research this week"
- "was lief in #tech-sys-design letzte woche?"
- "weekly summary #agent-dump"
- "zusammenfassung #agentic-org last 3 days"
