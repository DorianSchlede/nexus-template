---
name: Query Transcript
slug: query-transcript
category: analysis
description: Ask questions about meeting summaries and transcripts from Slack
triggers:
  - "query transcript"
  - "query meeting"
  - "was haben wir besprochen"
  - "frag das meeting"
  - "strategy weekly frage"
  - "what did we discuss"
  - "meeting question"
inputs:
  required:
    - name: question
      type: string
      description: "The question to ask about meetings"
  optional:
    - name: source
      type: string
      default: "#meeting-summaries"
      description: "Channel to search (default: #meeting-summaries)"
    - name: days
      type: number
      default: 30
      description: "How far back to search"
outputs:
  - type: markdown
    destination: display
    description: "Answer with source references"
scripts:
  - channel_history.py
  - search_messages.py
---

# Query Transcript

Ask questions about meeting summaries and get answers with source references.

## Workflow

### Step 1: Identify Source

Default: `#meeting-summaries`

Can also query:
- Specific channel with meeting notes
- Search term to find relevant meetings

### Step 2: Pull Meeting Content

```bash
python 00-system/skills/slack/slack-master/scripts/channel_history.py --channel meeting-summaries --limit 100 --json
```

Or search for specific meetings:
```bash
python 00-system/skills/slack/slack-master/scripts/search_messages.py --query "strategy weekly" --count 50
```

### Step 3: Filter by Date

Filter messages to the specified date range (default: last 30 days).

### Step 4: Analyze and Answer

Read the meeting content and answer the user's question.

Include:
- Direct answer to the question
- Relevant quotes from meetings
- Date of the meeting(s) referenced
- Who said what (if available)

### Step 5: Format Response

```markdown
## Answer

{Direct answer to the question}

### Sources

**Strategy Weekly - Dec 29:**
> "{relevant quote}"

**Strategy Weekly - Dec 22:**
> "{relevant quote}"

---
*Based on #meeting-summaries, last {days} days*
```

## Example Usage

- "was haben wir bei strategy weekly über MetaTuner besprochen?"
- "what decisions did we make about the architecture?"
- "query meeting: wer ist für onboarding zuständig?"
- "strategy weekly frage: was sind die nächsten priorities?"
