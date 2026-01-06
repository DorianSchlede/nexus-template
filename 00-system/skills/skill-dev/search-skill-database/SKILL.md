---
name: search-skill-database
description: Search the Skill Marketplace for available skills. Load when user mentions "search skills", "find skill", "browse skills", "list skills", "what skills are available", or "skill marketplace".
---

# Search Skill Marketplace

Browse and search the central Skill Marketplace (120+ skills) to find what you need.

## Purpose

Discover skills from the shared marketplace. Filter by name, team, or integration to find relevant skills for import.

**Use cases:**
- Discover skills created by teammates
- Find skills for specific integrations (Gmail, Slack, HubSpot, etc.)
- Check if a skill already exists before creating
- Browse skills by team (General, Solutions, Engineering, Sales)

**Time Estimate**: 30 seconds

---

## Quick Start

```bash
# List all skills
python 00-system/skills/airtable/airtable-master/scripts/query_records.py \
  --base app1gngDx52VAgjVQ --table tblsQL8n9EfMAFIyD \
  --token MUTAGENT --fields "Name,Description,Team" --limit 200

# Search by name
python 00-system/skills/airtable/airtable-master/scripts/query_records.py \
  --base app1gngDx52VAgjVQ --table tblsQL8n9EfMAFIyD \
  --token MUTAGENT --fields "Name,Description,Team" \
  --filter "FIND('gmail', LOWER({Name}))"
```

---

## Workflow

### Step 1: Search Skills

**List all available skills:**
```bash
python 00-system/skills/airtable/airtable-master/scripts/query_records.py \
  --base app1gngDx52VAgjVQ --table tblsQL8n9EfMAFIyD \
  --token MUTAGENT --fields "Name,Team" --limit 200
```

**Search by name (contains):**
```bash
--filter "FIND('slack', LOWER({Name}))"
```

**Filter by team:**
```bash
--filter "{Team}='Solutions'"
--filter "{Team}='google'"
--filter "{Team}='hubspot'"
```

**Combined search:**
```bash
--filter "AND({Team}='Solutions', FIND('beam', LOWER({Name})))"
```

### Step 2: View Results

Output shows skill metadata:
```
Found 5 records

1. gmail
   Team: google
   Description: Send, read, and search emails...

2. slack
   Team: slack
   Description: Complete Slack integration...

3. hubspot-create-deal
   Team: hubspot
   Description: Create deals in HubSpot CRM...
```

### Step 3: Import Selected Skill

Once you find what you need:

```bash
python 00-system/skills/airtable/airtable-master/scripts/download_skill.py \
  --base app1gngDx52VAgjVQ --table tblsQL8n9EfMAFIyD \
  --files-table tblhx8DRvcHN7GWmJ \
  --skill "<SKILL_NAME>" --token MUTAGENT --output 03-skills
```

---

## Common Searches

| Looking for... | Filter |
|----------------|--------|
| Gmail/email skills | `--filter "FIND('gmail', LOWER({Name}))"` |
| Slack skills | `--filter "FIND('slack', LOWER({Name}))"` |
| HubSpot CRM | `--filter "{Team}='hubspot'"` |
| Google suite | `--filter "{Team}='google'"` |
| Beam AI agents | `--filter "FIND('beam', LOWER({Name}))"` |
| Solutions team | `--filter "{Team}='Solutions'"` |
| All integrations | `--filter "{Team}='langfuse' OR {Team}='hubspot'"` |

---

## Skill Categories

| Team | Count | Examples |
|------|-------|----------|
| **google** | 8 | gmail, google-calendar, google-sheets, google-docs |
| **slack** | 2 | slack, slack-connect |
| **hubspot** | 15+ | hubspot-create-deal, hubspot-search-contacts |
| **langfuse** | 6 | langfuse-get-trace, langfuse-list-sessions |
| **beam** | 4 | beam-connect, beam-debug-issue-tasks |
| **Solutions** | 20+ | fathom, create-meeting-minutes, design-beam-agent |
| **system** | 10 | close-session, validate-system, update-nexus |
| **skill-dev** | 5 | create-skill, share-skill, import-skill |

---

## Marketplace Details

| Property | Value |
|----------|-------|
| Base ID | `app1gngDx52VAgjVQ` |
| Skills Table | `tblsQL8n9EfMAFIyD` |
| Files Table | `tblhx8DRvcHN7GWmJ` |
| Token | `MUTAGENT` |
| Total Skills | 120+ |

---

## Example Session

```
User: "what slack skills are available?"

AI: Searching Skill Marketplace for Slack skills...

    python query_records.py --base app1gngDx52VAgjVQ \
      --table tblsQL8n9EfMAFIyD --token MUTAGENT \
      --fields "Name,Description" \
      --filter "FIND('slack', LOWER({Name}))"

    Found 2 skills:

    1. slack
       Complete Slack integration - 32 API operations
       (messages, channels, reactions, reminders)

    2. slack-connect
       Meta-skill for Slack workspace connection

    Want to import one? Say "import slack"
```

---

## JSON Output

For programmatic use:

```bash
python query_records.py ... --json
```

Returns:
```json
{
  "records": [
    {"id": "rec...", "fields": {"Name": "gmail", "Team": "google", ...}},
    ...
  ]
}
```

---

## Related Skills

- `import-skill` - Import a skill from marketplace
- `share-skill` - Upload your skill to marketplace
- `create-skill` - Create a new skill locally

---

*Skill Marketplace powered by Airtable*
