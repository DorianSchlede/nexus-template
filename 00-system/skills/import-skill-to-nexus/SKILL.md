---
name: import-skill-to-nexus
description: Import a skill from Notion (or other source) into local Nexus. Load when user mentions "import skill", "download skill", "add skill to nexus", "pull skill from notion", or selects a skill to import after querying.
---

# Import Skill to Nexus

Download skill content from Notion and create it locally in `03-skills/`.

## Purpose

This is an atomic building block that takes skill content (from Notion or other sources) and creates a proper skill folder structure in Nexus. It handles:

- Downloading the skill file from Notion
- Extracting/creating the SKILL.md
- Creating the folder structure
- Checking for existing skills (prompt to overwrite)

**Typically used after `query-notion-db`** when user selects a skill to import.

---

## Safeguards

### Pre-Flight Check (ALWAYS Run First)

Before ANY import operation, verify Notion setup:

```
🔍 Pre-flight check...

1. API Key:     [.env → NOTION_API_KEY]
2. Database ID: [.env → NOTION_SKILLS_DB_ID]

❌ Missing config? → Run "First-Time Setup" (see export-skill-to-notion)
✅ All configured? → Proceed with import
```

### Content Validation

Before importing, validate the skill:

1. **File exists** → Check Skill property has attachment
2. **Valid YAML** → Verify `name:` and `description:` in header
3. **No malicious content** → Basic sanity check on file content

```
Validating skill content...

✅ File attached: {filename}
✅ Valid YAML header
✅ Content looks safe

Ready to import.
```

### Local Conflict Detection

Before overwriting local skill:

```
⚠️ Local skill "{skill-name}" exists

Local version:  Modified {date}
Notion version: Created by {owner} on {date}

Options:
1. Overwrite local with Notion version
2. Keep local version
3. Compare side-by-side
4. Backup local, then import

Choose (1-4):
```

### Prohibited Operations

| Operation | Status | Notes |
|-----------|--------|-------|
| Import single skill | ✅ Allowed | With confirmation if exists |
| Bulk import | ⚠️ Careful | Confirm each skill individually |
| Import without file | ❌ Blocked | Skill must have attachment |
| Import invalid SKILL.md | ⚠️ Recover | Auto-create from Notion properties |

---

## Workflow

### Step 1: Receive Skill Data

From `query-notion-db` or user input, receive:
- **Skill name** (e.g., "beam-list-agents")
- **Notion page ID** (for downloading attached file)
- **Description** (for creating SKILL.md if needed)

### Step 2: Check for Existing Skill

```bash
# Check if skill already exists
ls 03-skills/{skill-name}/SKILL.md
```

**If exists:**
```
⚠️ Skill "{skill-name}" already exists locally.

Options:
1. Overwrite - Replace with version from Notion
2. Skip - Keep local version
3. Compare - Show differences

What would you like to do?
```

### Step 3: Download Skill File

**Get file URL from Notion page:**
```bash
curl -s "https://api.notion.com/v1/pages/{page_id}" \
  -H "Authorization: Bearer ${NOTION_API_KEY}" \
  -H "Notion-Version: 2022-06-28"
```

**Extract file URL from response:**
```python
file_url = page["properties"]["Skill"]["files"][0]["file"]["url"]
```

**Download the file:**
```bash
# Get the filename from the response (usually {skill-name}-SKILL.txt)
curl -L -o /tmp/{filename} "{file_url}"
```

### Step 4: Extract and Create Skill

**If .txt file (current format from Notion File Upload API):**
```bash
mkdir -p 03-skills/{skill-name}
# Rename .txt back to SKILL.md
mv /tmp/{skill-name}-SKILL.txt 03-skills/{skill-name}/SKILL.md
```

**If .zip file (legacy format):**
```bash
unzip /tmp/{skill-name}.zip -d 03-skills/{skill-name}/
```

**If single SKILL.md:**
```bash
mkdir -p 03-skills/{skill-name}
mv /tmp/SKILL.md 03-skills/{skill-name}/
```

### Step 5: Validate Structure

Required structure:
```
03-skills/{skill-name}/
└── SKILL.md          # Required - skill definition
└── references/       # Optional - supporting docs
└── scripts/          # Optional - automation scripts
└── assets/           # Optional - images, templates
```

**Validate SKILL.md has required YAML header:**
```yaml
---
name: skill-name
description: Load when user mentions "trigger phrase"...
---
```

### Step 6: Confirm Success

```
✅ Skill imported successfully!

📁 Location: 03-skills/{skill-name}/
📄 Files:
   - SKILL.md
   - references/ (if present)

💡 Try it: Say "{trigger phrase}" to use this skill
```

---

## Input Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| skill_name | Yes | Name for the skill folder |
| page_id | Yes* | Notion page ID (if importing from Notion) |
| source_url | Yes* | Direct URL to skill file (alternative to page_id) |
| content | Yes* | Raw SKILL.md content (alternative to download) |

*One of page_id, source_url, or content required

---

## Example Usage

### Import from Notion Query Results

```
User: "Show me skills for Linear integration"

AI: [Runs query-notion-db with Integration=Linear filter]

Found 2 skills:
1. setup-linear-onboarding-template - Fill Linear template projects
2. generate-linear-project-update - Create weekly status updates

Which would you like to import? (1, 2, or both)

User: "1"

AI: [Runs import-skill-to-nexus]

✅ Imported: setup-linear-onboarding-template
📁 Location: 03-skills/setup-linear-onboarding-template/
```

### Import with Overwrite Check

```
User: "Import beam-list-agents"

AI: ⚠️ Skill "beam-list-agents" already exists locally.

Options:
1. Overwrite - Replace with Notion version
2. Skip - Keep local version
3. Compare - Show differences

User: "1"

AI: ✅ Overwrote beam-list-agents with version from Notion
```

---

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| No file attached | Notion page has no Skill file | Ask user to attach file in Notion first |
| Invalid SKILL.md | Missing YAML header | Create minimal header from Notion properties |
| Download failed | Expired URL or network issue | Retry with fresh page query |
| Extract failed | Corrupt zip or wrong format | Check file format, try manual download |

### Auto-Recovery: Create SKILL.md from Notion Properties

If downloaded file doesn't contain valid SKILL.md, create one from Notion data:

```yaml
---
name: {skill-name}
description: {description from Notion}
---

# {Skill Name}

{Description from Notion}

## Purpose

{Purpose from Notion, or "Imported from Beam Nexus Skills database"}

---

*Imported from Notion on {date}*
```

---

## Integration with Other Skills

**Typically called after:**
- `query-notion-db` - User selects skill(s) from query results

**Can be followed by:**
- Testing the imported skill
- `export-skill-to-notion` - If user modifies and wants to push changes back

---

## Notes

- Files are downloaded to `/tmp/` first, then moved to `03-skills/`
- Notion file URLs expire after 1 hour - download immediately after query
- **Current format**: `.txt` files (from Notion File Upload API) - rename to SKILL.md
- **Legacy format**: `.zip` files - extract contents
- Always validate SKILL.md format before confirming success