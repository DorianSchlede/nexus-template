---
name: share-skill
description: Upload a local skill to the Skill Marketplace. Load when user mentions "share skill", "upload skill", "push skill", "publish skill", "add skill to marketplace", or after creating a new skill.
---

# Share Skill to Marketplace

Upload your local skill to the central Skill Marketplace (Airtable) for others to use.

## Purpose

Push any skill from `03-skills/` or `00-system/skills/` to the shared marketplace. Handles:

- Validating SKILL.md format
- Creating JSON bundle with all skill files
- Uploading to Airtable Skills table
- Handling large skills via SkillFiles table

**Typically used after `create-skill`** to share new skills with the team.

---

## Quick Start

```bash
# Upload a single skill
python 00-system/skills/airtable/airtable-master/scripts/upload_local_skills.py \
  --base app1gngDx52VAgjVQ --table tblsQL8n9EfMAFIyD \
  --token MUTAGENT --skill-path 03-skills/my-skill

# Upload all local skills (batch)
python 00-system/skills/airtable/airtable-master/scripts/upload_local_skills.py \
  --base app1gngDx52VAgjVQ --table tblsQL8n9EfMAFIyD \
  --token MUTAGENT
```

---

## Workflow

### Step 1: Validate Your Skill

Ensure your skill has a valid SKILL.md:

```yaml
---
name: my-skill
description: Load when user mentions "trigger phrase"...
version: 1.0
---

# My Skill

## Purpose

What this skill does...
```

**Required fields:**
- `name` - Skill identifier (lowercase, hyphenated)
- `description` - Must include trigger phrases

**Optional fields:**
- `version` - Defaults to 1.0
- `team` - Defaults to General

### Step 2: Preview Upload (Dry Run)

```bash
python 00-system/skills/airtable/airtable-master/scripts/upload_local_skills.py \
  --base app1gngDx52VAgjVQ --table tblsQL8n9EfMAFIyD \
  --token MUTAGENT --skill-path 03-skills/my-skill --dry-run
```

**Output:**
```
[DRY-RUN] Would upload: my-skill
  Version: 1.0
  Team: General
  Files: 3 (SKILL.md, scripts/helper.py, references/guide.md)
  Bundle size: 4,521 bytes
```

### Step 3: Upload to Marketplace

```bash
python 00-system/skills/airtable/airtable-master/scripts/upload_local_skills.py \
  --base app1gngDx52VAgjVQ --table tblsQL8n9EfMAFIyD \
  --token MUTAGENT --skill-path 03-skills/my-skill
```

**Output:**
```
my-skill... OK (created recXXX)
```

### Step 4: Handle Large Skills

If skill is too large (>90KB), it becomes a "partial" bundle. Upload files separately:

```bash
python 00-system/skills/airtable/airtable-master/scripts/upload_skill_files.py \
  --base app1gngDx52VAgjVQ --table tblhx8DRvcHN7GWmJ \
  --token MUTAGENT --skill my-skill
```

---

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--skill-path` | No | Path to single skill (default: all skills) |
| `--dry-run` | No | Preview without uploading |
| `--force` | No | Update existing skill |
| `--json` | No | Output as JSON |

---

## Marketplace Details

| Property | Value |
|----------|-------|
| Base ID | `app1gngDx52VAgjVQ` |
| Skills Table | `tblsQL8n9EfMAFIyD` |
| Files Table | `tblhx8DRvcHN7GWmJ` |
| Token | `MUTAGENT` |

---

## Bundle Format

Skills are packaged as JSON bundles:

```json
{
  "skill_name": "my-skill",
  "version": "1.0",
  "bundle_format": "nexus-skill-bundle-v1",
  "created": "2025-12-31T12:00:00",
  "files": {
    "SKILL.md": "<base64-encoded>",
    "scripts/helper.py": "<base64-encoded>",
    "references/guide.md": "<base64-encoded>"
  },
  "partial": false
}
```

**Included files:**
- SKILL.md (required)
- scripts/ folder
- references/ folder
- assets/ folder

**Excluded:**
- .git/
- __pycache__/
- *.pyc
- node_modules/

---

## Team Assignment

Set team in SKILL.md frontmatter:

```yaml
---
name: my-skill
description: ...
team: Solutions
---
```

**Available teams:**
- `General` - Company-wide utilities
- `Solutions` - Client implementation
- `Engineering` - Dev tools
- `Sales` - Sales workflows
- Integration-specific: `google`, `slack`, `hubspot`, `langfuse`, etc.

---

## Version Management

```yaml
---
name: my-skill
version: 1.1
---
```

**Version format:** `MAJOR.MINOR` or `MAJOR.MINOR.PATCH`

| Change | Bump |
|--------|------|
| Bug fix | 1.0 → 1.1 |
| New feature | 1.1 → 1.2 |
| Breaking change | 1.x → 2.0 |

---

## Example Session

```
User: "share my new gmail-helper skill"

AI: Uploading gmail-helper to Skill Marketplace...

    Validating SKILL.md... OK
    Creating bundle... 3 files, 2,845 bytes

    python upload_local_skills.py --base app1gngDx52VAgjVQ \
      --table tblsQL8n9EfMAFIyD --token MUTAGENT \
      --skill-path 03-skills/gmail-helper

    gmail-helper... OK (created recABC123)

    Skill uploaded to marketplace.
    Others can now import it with: "import gmail-helper"
```

---

## Updating Existing Skills

To update a skill that already exists:

```bash
--force  # Overwrite existing record
```

Or delete from Airtable first and re-upload.

---

## Troubleshooting

| Error | Solution |
|-------|----------|
| Skill already exists | Use `--force` to update |
| Bundle too large | Use upload_skill_files.py for linked files |
| Missing SKILL.md | Every skill needs SKILL.md |
| Invalid YAML | Check frontmatter format |
| Permission denied | Check AIRTABLE_API_KEY_MUTAGENT in .env |

---

## Related Skills

- `create-skill` - Create a new skill locally
- `import-skill` - Download from marketplace
- `search-skill-database` - Browse available skills

---

*Skill Marketplace powered by Airtable*
