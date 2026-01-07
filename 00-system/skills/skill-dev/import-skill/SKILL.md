---
name: import-skill
description: "Triggers: import skill, download skill, install skill, get skill."
---

# Import Skill from Marketplace

Download skills from the central Skill Marketplace (Airtable) into your local Nexus.

## Purpose

Pull any skill from our shared 120+ skill database directly into `03-skills/`. Handles:

- Searching available skills
- Downloading complete skill bundles (including large skills via linked files)
- Auto-backup of existing skills before overwriting
- Batch import of multiple skills

---

## Quick Start

```bash
# Import a specific skill
python 00-system/skills/airtable/airtable-master/scripts/download_skill.py \
  --base app1gngDx52VAgjVQ --table tblsQL8n9EfMAFIyD \
  --files-table tblhx8DRvcHN7GWmJ \
  --skill "gmail" --token MUTAGENT --output 03-skills

# List all available skills (dry-run)
python 00-system/skills/airtable/airtable-master/scripts/download_skill.py \
  --base app1gngDx52VAgjVQ --table tblsQL8n9EfMAFIyD \
  --all --token MUTAGENT --dry-run
```

---

## Workflow

### Step 1: Search Available Skills

First, find what you need:

```bash
# Search by name
python 00-system/skills/airtable/airtable-master/scripts/query_records.py \
  --base app1gngDx52VAgjVQ --table tblsQL8n9EfMAFIyD \
  --token MUTAGENT --fields "Name,Description,Team" \
  --filter "{Name} contains 'gmail'"

# List all skills
python 00-system/skills/airtable/airtable-master/scripts/query_records.py \
  --base app1gngDx52VAgjVQ --table tblsQL8n9EfMAFIyD \
  --token MUTAGENT --fields "Name,Team" --limit 200
```

### Step 2: Import the Skill

```bash
python 00-system/skills/airtable/airtable-master/scripts/download_skill.py \
  --base app1gngDx52VAgjVQ --table tblsQL8n9EfMAFIyD \
  --files-table tblhx8DRvcHN7GWmJ \
  --skill "<SKILL_NAME>" --token MUTAGENT --output 03-skills
```

**Output:**
```
Using token: AIRTABLE_API_KEY_MUTAGENT
Using linked files table: tblhx8DRvcHN7GWmJ
OK - Extracted 5 files (complete)
```

### Step 3: Verify Import

```bash
ls 03-skills/<skill-name>/
cat 03-skills/<skill-name>/SKILL.md
```

---

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--skill` | Yes* | Skill name to import |
| `--all` | Yes* | Import all skills (alternative to --skill) |
| `--output` | No | Output directory (default: ./downloaded-skills) |
| `--files-table` | No | SkillFiles table for large skills |
| `--no-backup` | No | Skip backup of existing skills |
| `--dry-run` | No | Show what would be imported |

*Either `--skill` or `--all` is required

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

## Skill Categories

| Category | Examples |
|----------|----------|
| **Integrations** | gmail, slack, notion, airtable, hubspot, langfuse, fathom |
| **Google Suite** | google-calendar, google-sheets, google-docs, google-slides |
| **AI/Agents** | beam-connect, notebooklm, design-beam-agent |
| **Productivity** | mental-models, ultrathink, create-meeting-minutes |
| **System** | create-project, close-session, validate-system |

---

## Backup System

When importing a skill that already exists locally:

1. Existing skill is moved to `<skill-name>.backup.<timestamp>`
2. New skill is extracted
3. Backup remains in same directory

**To restore:**
```bash
rm -rf 03-skills/my-skill
mv 03-skills/my-skill.backup.20251231_120000 03-skills/my-skill
```

**To skip backup:**
```bash
--no-backup
```

---

## Example Session

```
User: "import the gmail skill"

AI: Importing gmail from Skill Marketplace...

    python download_skill.py --base app1gngDx52VAgjVQ \
      --table tblsQL8n9EfMAFIyD --files-table tblhx8DRvcHN7GWmJ \
      --skill "gmail" --token MUTAGENT --output 03-skills

    OK - Extracted 8 files (complete)

    Skill imported to: 03-skills/gmail/

    Files:
    - SKILL.md
    - scripts/send_email.py
    - scripts/read_emails.py
    - scripts/search_emails.py
    - references/setup-guide.md
    ...

    Say "send email" to use this skill.
```

---

## Troubleshooting

| Error | Solution |
|-------|----------|
| Skill not found | Check spelling, run search first |
| No content | Skill has no bundle (metadata only) |
| Permission denied | Check AIRTABLE_API_KEY_MUTAGENT in .env |
| Partial bundle | Add `--files-table` for complete download |

---

## Related Skills

- `search-skill-database` - Search the marketplace
- `share-skill` - Upload your skill to marketplace
- `create-skill` - Create a new skill locally

---

*Skill Marketplace powered by Airtable*
