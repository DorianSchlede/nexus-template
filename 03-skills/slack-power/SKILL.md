---
name: slack-power
description: "slack power, meeting prep, channel digest, collect links, query meeting."
---

# Slack Power

Advanced Slack workflows for knowledge extraction, meeting analysis, and team communication.

## When This Triggers

- "get dm with @user" / "slack history"
- "extract schemas from slack" / "find code blocks"
- "what did I promise" / "action items from slack"
- "meeting prep with @user" / "prep for call"
- "post update to #channel" / "share to slack"
- "channel digest #channel" / "was lief in #channel"
- "collect links from #channel" / "alle links aus"
- "query meeting" / "was haben wir besprochen"

## Prerequisites

Requires Slack integration. If not set up:
```bash
python 00-system/skills/slack/slack-master/scripts/setup_slack.py
```

---

## Workflow

### Step 1: Scan Available Workflows

```bash
python 03-skills/slack-power/scripts/select_workflow.py --format brief
```

### Step 2: Match User Intent

| Category | Workflows | Triggers |
|----------|-----------|----------|
| **extraction** | get-thread, extract-schemas, extract-actions, link-collector | "get", "extract", "find", "pull", "collect links" |
| **preparation** | meeting-prep | "prep", "prepare", "before meeting" |
| **broadcast** | post-update | "post", "share", "send", "update" |
| **analysis** | channel-digest, query-transcript | "digest", "summary", "query", "was lief", "was haben wir" |

### Step 3: Load Specific Workflow

Read the matched workflow file:
```
03-skills/slack-power/workflows/{category}/{workflow-slug}.md
```

### Step 4: Execute Workflow

Follow the workflow instructions. Each workflow specifies:
- Required/optional inputs
- Scripts to run
- Output format
- Save location

### Step 5: Handle Output

**Display**: Show results in conversation

**Save to Workspace** (if configured):
- Check `user-config.yaml` → `slack_power.auto_save`
- If `ask`: Prompt "Save to workspace? (y/n)"
- If `always`: Auto-save and show path
- If `never`: Display only

Default paths:
| Output Type | Location |
|-------------|----------|
| Threads | `04-workspace/07-insights/slack-extracts/` |
| Schemas | `04-workspace/07-insights/technical/` |
| Actions | `04-workspace/07-insights/slack-extracts/` |
| Meeting Prep | `04-workspace/07-insights/meeting-prep/` |

**Post to Slack**: Always confirm before posting.

---

## Quick Reference

### Extraction Workflows

| Workflow | Command | Output |
|----------|---------|--------|
| **get-thread** | `get dm with @burak` | Conversation history |
| **extract-schemas** | `extract schemas from @burak` | Code blocks, interfaces |
| **extract-actions** | `what did I promise to burak` | Action items, commitments |
| **link-collector** | `collect links from #agent-dump` | Organized link collection |

### Analysis Workflows

| Workflow | Command | Output |
|----------|---------|--------|
| **channel-digest** | `channel digest #research this week` | Weekly/daily channel summary |
| **query-transcript** | `was haben wir über X besprochen?` | Answer from meeting summaries |

### Preparation Workflows

| Workflow | Command | Output |
|----------|---------|--------|
| **meeting-prep** | `meeting prep with @burak` | Full context document |

### Broadcast Workflows

| Workflow | Command | Output |
|----------|---------|--------|
| **post-update** | `post update to #team: done with X` | Slack message (confirmed) |

---

## Configuration

In `01-memory/user-config.yaml`:

```yaml
slack_power:
  auto_save: "ask"  # "ask", "always", "never"
  default_days: 7   # How far back to search by default
```

---

## Adding New Workflows

1. Create `workflows/{category}/{workflow-slug}.md`
2. Add YAML frontmatter with: name, slug, category, description, triggers, inputs, outputs
3. Write workflow steps
4. Scanner auto-discovers on next run

---

## Scripts Reference

| Script | Purpose |
|--------|---------|
| `select_workflow.py` | Scan and list all workflows |
| Slack scripts in `00-system/skills/slack/slack-master/scripts/` | API operations |
