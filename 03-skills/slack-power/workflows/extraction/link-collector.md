---
name: Link Collector
slug: link-collector
category: extraction
description: Collect and organize all links shared in a channel
triggers:
  - "collect links"
  - "alle links aus"
  - "resources from"
  - "link sammlung"
  - "get links from"
  - "shared links"
inputs:
  required:
    - name: channel
      type: string
      description: "#channel-name to collect links from"
  optional:
    - name: days
      type: number
      default: 14
      description: "How far back to search"
    - name: filter
      type: string
      description: "Optional keyword filter (e.g., 'arxiv', 'youtube')"
outputs:
  - type: markdown
    destination: workspace
    default_path: "04-workspace/07-insights/slack-extracts/{date}-{channel}-links.md"
scripts:
  - channel_history.py
---

# Link Collector

Collect and organize all links shared in a channel.

## Workflow

### Step 1: Pull Channel History

```bash
python 00-system/skills/slack/slack-master/scripts/channel_history.py --channel {channel_id} --limit 300 --json
```

### Step 2: Extract URLs

Regex pattern for URLs in messages.

Filter by date range (default: last 14 days).

### Step 3: Categorize by Domain

| Category | Domains |
|----------|---------|
| **Research** | arxiv.org, papers.ssrn.com, scholar.google.com |
| **Video** | youtube.com, youtu.be, vimeo.com |
| **Code** | github.com, gitlab.com, gist.github.com |
| **Docs** | notion.so, docs.google.com, medium.com |
| **Tools** | Various SaaS, product pages |
| **Social** | twitter.com, linkedin.com |
| **Other** | Everything else |

### Step 4: Add Context

For each link:
- Who shared it
- When (date)
- Surrounding message text (context)
- Any reactions/replies (indicates value)

### Step 5: Format Output

```markdown
# Links from #{channel}
Collected: {date}
Period: Last {days} days

## Research Papers ({count})

| Link | Shared By | Date | Context |
|------|-----------|------|---------|
| [arxiv.org/abs/...](url) | @person | Dec 28 | "interesting paper on..." |

## Videos ({count})

| Link | Shared By | Date | Context |
|------|-----------|------|---------|
| [YouTube: Title](url) | @person | Dec 27 | "check this out..." |

## Code & GitHub ({count})

| Link | Shared By | Date | Context |
|------|-----------|------|---------|
| [repo-name](url) | @person | Dec 26 | "useful library for..." |

## Documentation ({count})
...

## Tools & Products ({count})
...

## Other ({count})
...

---
*{total_count} links from #{channel}, last {days} days*
```

### Step 6: Save Option

Ask user: "Save links to workspace? (y/n)"

Default path: `04-workspace/07-insights/slack-extracts/{date}-{channel}-links.md`

## Example Usage

- "collect links from #agent-dump"
- "alle links aus #research letzte 2 wochen"
- "get links from #tech-sys-design filter:github"
- "resources from #agent-dump last 30 days"
