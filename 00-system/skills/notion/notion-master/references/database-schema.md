# Beam Nexus Skills Database Schema

Complete schema documentation for the "Beam Nexus Skills" Notion database.

**Database ID**: `2bc2cadf-bbbc-80be-af8a-d45dfc8dfa2e`

---

## Database Properties

| Property Name | Type | Required | Description | Notes |
|---------------|------|----------|-------------|-------|
| **Skill Name** | title | Yes | Unique identifier for the skill | Primary key, must match skill folder name |
| **Description** | rich_text | Yes | One-line summary of what skill does | From YAML `description:` field |
| **Purpose** | rich_text | No | Detailed explanation of skill purpose | From `## Purpose` section in SKILL.md |
| **Team** | select | Yes | Owning team for the skill | General, Solutions, Engineering, Sales |
| **Integration** | multi_select | No | External tools this skill integrates with | Beam AI, Linear, Notion, Airtable, etc. |
| **Owner** | people | Yes | Person who created/maintains the skill | From `user-config.yaml ’ notion_user_id` |
| **Created** | date | Yes | Date skill was added to Notion | Auto-set to today's date |
| **Skill** | files | Yes | Attached .skill or .txt file | Contains full skill folder structure |

---

## Property Details

### Skill Name (title)

**Format**: `skill-name` (lowercase, hyphen-separated)

**Examples**:
-  `query-notion-db`
-  `beam-list-agents`
-  `create-weekly-report`
- L `Query Notion DB` (no spaces or capitals)
- L `query_notion_db` (no underscores)

**Must match**:
- Folder name in `03-skills/{skill-name}/`
- YAML `name:` field in SKILL.md

---

### Description (rich_text)

**Format**: Concise, specific explanation with triggers

**Good examples**:
- "Query Notion databases with filters. Load when user says 'query notion', 'search skills database', or 'find skills in notion'."
- "List all agents in Beam AI workspace. Load when user mentions 'list agents', 'show agents', or 'beam agents'."

**Bad examples**:
- L "A tool" (too vague)
- L "Helps with Notion" (not specific)
- L "[TODO: Add description]" (incomplete)

**Max length**: 1024 characters (Notion limit)

---

### Purpose (rich_text)

**Format**: 2-3 sentences explaining why the skill exists and what problems it solves

**Example**:
```
This skill enables team members to discover and import skills created by
colleagues. It reduces duplication of effort and promotes knowledge sharing
across teams by providing a searchable, centralized skills library.
```

**Extracted from**: `## Purpose` section in SKILL.md

**Max length**: ~500 words recommended

---

### Team (select)

**Available options**:
- **General** - Utility skills usable across all teams
- **Solutions** - Client-facing implementation work
- **Engineering** - Developer tools and infrastructure
- **Sales** - Sales-specific workflows

**Inference rules**:

| Skill Type | Team | Reasoning |
|------------|------|-----------|
| Query/import/export tools | General | Cross-functional utility |
| Notion/Linear integrations | General | Used by multiple teams |
| Agent building/deployment | Solutions | Client implementation |
| Client onboarding workflows | Solutions | Customer-facing |
| CI/CD, testing, dev tools | Engineering | Development-focused |
| Proposal/contract generation | Sales | Sales process |
| Unknown/ambiguous | Ask user | When unclear |

**Note**: New teams can be created by specifying a name that doesn't exist. Notion auto-creates the select option.

---

### Integration (multi_select)

**Available options**:
- Beam AI
- Linear
- Notion
- Airtable
- Slack
- GitHub
- Google Drive
- (others can be added)

**Inference**: AI scans SKILL.md content for mentions of these tools

**Examples**:
- Skill mentions "Beam AI" ’ Add "Beam AI" integration tag
- Skill uses Linear API ’ Add "Linear" integration tag
- Skill queries Notion ’ Add "Notion" integration tag

**Multiple integrations allowed**: A skill can have 0-5+ integration tags

---

### Owner (people)

**Format**: Notion user ID (not email)

**Source**: `user-config.yaml`:
```yaml
integrations:
  notion:
    user_id: "abc123-user-id-here"
    user_name: "Your Name"
```

**Important**:
- Use `user_id`, NOT API key owner
- Each person has unique user ID
- Enables proper attribution even with shared API keys
- Displayed as person's name in Notion

**Get your user ID**:
```bash
curl "https://api.notion.com/v1/users/me" \
  -H "Authorization: Bearer ${NOTION_API_KEY}" \
  -H "Notion-Version: 2022-06-28"
```

---

### Created (date)

**Format**: ISO 8601 date (`YYYY-MM-DD`)

**Auto-set**: Always use today's date when creating new entry

**Example**: `"2025-12-10"`

**Not editable**: Represents when skill was first added to Notion

---

### Skill (files)

**Format**: File attachment (`.skill`, `.zip`, or `.txt`)

**Recommended**: `.skill` file (packaged via `package_skill.py`)

**Upload process**: 3-step Notion File Upload API
1. Create file upload object
2. Send file content
3. Attach to page property

**Supported formats** (per Notion API):
- Text: `.txt`, `.json`, `.md` (upload as `.txt`)
- Documents: `.pdf`, `.doc`, `.docx`
- Spreadsheets: `.xls`, `.xlsx`
- Presentations: `.ppt`, `.pptx`
- Archives: `.zip` (for multi-file skills)
- Images, audio, video (various formats)

**Current approach**: Upload `.skill` file (zip format with .skill extension)

**Fallback**: If .skill upload fails, use `.zip` or `.txt`

**File size limit**: 5 MB per file

---

## Field Mapping

**Local (SKILL.md) ’ Notion Property**

| Local Source | Notion Property | Extraction Method |
|--------------|-----------------|-------------------|
| YAML `name:` | Skill Name | Parse YAML frontmatter |
| YAML `description:` | Description | Parse YAML frontmatter |
| `## Purpose` section | Purpose | Extract markdown section content |
| AI inference + user confirm | Team | Analyze skill content, ask user |
| AI content scan | Integration | Scan for tool mentions |
| `user-config.yaml ’ notion_user_id` | Owner | Load from config file |
| Today's date | Created | Auto-generate |
| `.skill` file or folder | Skill | Package and upload via File API |

---

## Example Database Entry

```json
{
  "parent": {"database_id": "2bc2cadf-bbbc-80be-af8a-d45dfc8dfa2e"},
  "properties": {
    "Skill Name": {
      "title": [{"text": {"content": "query-notion-db"}}]
    },
    "Description": {
      "rich_text": [{"text": {"content": "Query Notion databases with filters. Load when user says 'query notion', 'search skills database'."}}]
    },
    "Purpose": {
      "rich_text": [{"text": {"content": "Enables team members to discover and browse the centralized skills library."}}]
    },
    "Team": {
      "select": {"name": "General"}
    },
    "Integration": {
      "multi_select": [
        {"name": "Notion"},
        {"name": "Beam AI"}
      ]
    },
    "Owner": {
      "people": [{"id": "abc123-user-id-here"}]
    },
    "Created": {
      "date": {"start": "2025-12-10"}
    },
    "Skill": {
      "files": [{
        "type": "file_upload",
        "file_upload": {"id": "file-upload-id-here"},
        "name": "query-notion-db.skill"
      }]
    }
  }
}
```

---

## Database Query Filters

**Common filter patterns for query-notion-db skill:**

### Filter by Team
```json
{
  "filter": {
    "property": "Team",
    "select": {"equals": "General"}
  }
}
```

### Filter by Integration
```json
{
  "filter": {
    "property": "Integration",
    "multi_select": {"contains": "Beam AI"}
  }
}
```

### Filter by Owner
```json
{
  "filter": {
    "property": "Owner",
    "people": {"contains": "user-id-here"}
  }
}
```

### Search by Name (partial match)
```json
{
  "filter": {
    "property": "Skill Name",
    "title": {"contains": "notion"}
  }
}
```

### Combined Filters (AND logic)
```json
{
  "filter": {
    "and": [
      {"property": "Team", "select": {"equals": "Solutions"}},
      {"property": "Integration", "multi_select": {"contains": "Beam AI"}}
    ]
  }
}
```

---

## Database Sorting

**Sort by Created date (newest first)**:
```json
{
  "sorts": [
    {"property": "Created", "direction": "descending"}
  ]
}
```

**Sort by Skill Name (alphabetical)**:
```json
{
  "sorts": [
    {"property": "Skill Name", "direction": "ascending"}
  ]
}
```

---

## Validation Rules

Before creating/updating entries:

1. **Skill Name**:
   -  Lowercase hyphen-case
   -  Unique in database
   -  Matches folder name

2. **Description**:
   -  Non-empty
   -  Specific (not generic)
   -  Under 1024 characters

3. **Team**:
   -  One of: General, Solutions, Engineering, Sales (or new name)

4. **Owner**:
   -  Valid Notion user ID
   -  User has access to workspace

5. **Skill File**:
   -  File attached
   -  Under 5 MB
   -  Valid format (.skill/.zip/.txt)

---

**Last Updated**: 2025-12-10
**Database URL**: [Beam Nexus Skills](https://notion.so/2bc2cadf-bbbc-80be-af8a-d45dfc8dfa2e)
