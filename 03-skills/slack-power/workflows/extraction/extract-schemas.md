---
name: Extract Schemas
slug: extract-schemas
category: extraction
description: Find and extract code blocks, interfaces, types, and technical schemas from Slack
triggers:
  - "extract schemas"
  - "find code"
  - "get interfaces"
  - "find types from"
  - "extract technical"
  - "get schemas from slack"
inputs:
  required:
    - name: source
      type: string
      description: "@user for DMs, #channel, or 'search:query' for workspace-wide"
  optional:
    - name: keywords
      type: string
      description: "Additional search terms (interface, type, schema, export)"
    - name: days
      type: number
      default: 30
      description: "How far back to search"
outputs:
  - type: markdown
    destination: workspace
    default_path: "04-workspace/07-insights/technical/{date}-{source}-schemas.md"
scripts:
  - dm_history.py
  - search_messages.py
---

# Extract Schemas

Find and compile technical schemas, interfaces, and code blocks from Slack.

## Workflow

### Step 1: Search for Code Content

**Option A - From DMs:**
```bash
python 00-system/skills/slack/slack-master/scripts/dm_history.py {username} --limit 500
```
Then filter for messages containing code blocks.

**Option B - Workspace Search:**
```bash
python 00-system/skills/slack/slack-master/scripts/search_messages.py --query "export interface" --count 50
python 00-system/skills/slack/slack-master/scripts/search_messages.py --query "type {keyword}" --count 50
```

### Step 2: Pattern Detection

Look for:
- Triple backtick code blocks (```)
- `interface`, `type`, `export`, `schema` keywords
- JSON/YAML structures
- Function signatures
- API definitions

### Step 3: Extract and Compile

For each found schema:
1. Extract the full code block
2. Note the source (who shared, when, context)
3. Group by type (interfaces, types, schemas, snippets)

### Step 4: Format Output

```markdown
# Technical Schemas from {source}
Extracted: {date}

## Interfaces

### {InterfaceName}
Source: @{user} on {date}
Context: {surrounding message text}

\`\`\`typescript
{code}
\`\`\`

## Types
...
```

### Step 5: Save to Workspace

Default: `04-workspace/07-insights/technical/{date}-{source}-schemas.md`

Ask user: "Save to workspace? (y/n)"

## Example Usage

- "extract schemas from burak" → All code from DMs with Burak
- "find interfaces in #engineering" → Code blocks from channel
- "get types search:MetaTuner" → Search all Slack for MetaTuner types
