---
name: query-notion-db
description: Query any Notion database and return results. Load when user mentions "query notion", "search notion database", "what's in notion", "find in notion", or needs to retrieve data from a Notion database.
---

# Query Notion Database

Generic Notion database query skill - returns raw results for AI processing.

## Purpose

Query any Notion database using the API. This is an atomic building block that can be used standalone or composed with other skills (like `import-skill-to-nexus`).

**Use cases:**
- List all skills in the company database
- Filter skills by team, integration, or owner
- Search for skills matching a description
- Check if a skill already exists before creating

---

## Safeguards

### Pre-Flight Check (ALWAYS Run First)

Before ANY query operation, verify Notion setup:

```
🔍 Pre-flight check...

1. API Key:     [.env → NOTION_API_KEY]
2. Database ID: [.env → NOTION_SKILLS_DB_ID]

❌ Missing config? → Run Notion setup wizard
✅ All configured? → Proceed with query
```

### First-Time Setup Detection

If Notion is not configured, guide the user:

```
🔧 Notion Setup Required

I notice you want to browse skills from the company database,
but Notion isn't configured yet. Let me help:

Step 1: Get an API key (choose one)
   Option A: Use the shared team API key
      → Ask your team admin for the NOTION_API_KEY
      → Simplest option - works immediately

   Option B: Create your own (admin only)
      → Go to https://www.notion.so/my-integrations
      → Click "New integration" → Name: "Nexus"
      → Note: Only workspace admins can create integrations

Step 2: Add to .env
   → NOTION_API_KEY=your-key-here
   → NOTION_SKILLS_DB_ID=2bc2cadf-bbbc-80be-af8a-d45dfc8dfa2e

Step 3: Connect database (if using your own key)
   → Open "Beam Nexus Skills" in Notion
   → Click "..." → "Connections" → Add your integration
   → Skip if using shared team key (already connected)

Want me to walk you through this? (yes/no)
```

### Read-Only Guarantee

This skill is **strictly read-only**:

| Operation | Status | Notes |
|-----------|--------|-------|
| Query/list skills | ✅ Allowed | Core functionality |
| Filter by any property | ✅ Allowed | Team, Integration, Owner, etc. |
| Create skills | ❌ Not here | Use `export-skill-to-notion` |
| Update skills | ❌ Not here | Use `export-skill-to-notion` |
| Delete skills | ❌ Never | Must use Notion UI |

---

## How to Use

### Basic Query (All Records)

```
AI: Query the Beam Nexus Skills database
```

**API Call:**
```bash
curl -s -X POST "https://api.notion.com/v1/databases/${NOTION_SKILLS_DB_ID}/query" \
  -H "Authorization: Bearer ${NOTION_API_KEY}" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{"page_size": 100}'
```

### Filtered Query

**Filter by Team:**
```json
{
  "filter": {
    "property": "Team",
    "select": {
      "equals": "Solutions"
    }
  }
}
```

**Filter by Integration:**
```json
{
  "filter": {
    "property": "Integration",
    "multi_select": {
      "contains": "Beam AI"
    }
  }
}
```

**Filter by Skill Name (contains):**
```json
{
  "filter": {
    "property": "Skill Name",
    "title": {
      "contains": "beam"
    }
  }
}
```

### Sorted Query

**Sort by Created (newest first):**
```json
{
  "sorts": [
    {
      "property": "Created",
      "direction": "descending"
    }
  ]
}
```

---

## Configuration

**Required environment variables** (from `.env`):
- `NOTION_API_KEY` - Your Notion integration token
- `NOTION_SKILLS_DB_ID` - Database ID for "Beam Nexus Skills"

**Current values:**
```
NOTION_SKILLS_DB_ID=2bc2cadf-bbbc-80be-af8a-d45dfc8dfa2e
```

---

## Database Schema

The "Beam Nexus Skills" database has these properties:

| Property | Type | Description |
|----------|------|-------------|
| Skill Name | title | Name of the skill |
| Team | select | Team that owns the skill (e.g., Solutions) |
| Skill | files | Attached skill file (.zip) |
| Integration | multi_select | Tools used (Beam AI, Linear, Notion, etc.) |
| Purpose | rich_text | Why this skill exists |
| Description | rich_text | What the skill does |
| Owner | people | Person who created/maintains it |
| Created | date | When the skill was added |

---

## Output Format

The skill returns an array of records. AI should parse and present results clearly:

**Example output format:**
```
Found 3 skills matching "onboarding":

1. setup-linear-onboarding-template
   Team: Solutions | Owner: Jack Li
   Description: Fill Linear template projects interactively via MCP

2. setup-notion-customer-onboarding
   Team: Solutions | Owner: Jack Li
   Description: Populate Notion onboarding templates via MCP

3. update-variables-in-notion
   Team: Solutions | Owner: Jack Li
   Description: Extract prompt variables to Notion DB via MCP
```

---

## Example Workflows

### "What skills are available?"
1. Query database with no filters
2. Present all skills grouped by Team or Integration
3. Ask if user wants to import any

### "Find skills for working with Beam agents"
1. Query with filter: Integration contains "Beam AI"
2. Present matching skills with descriptions
3. Offer to import selected skills

### "Does a skill for X already exist?"
1. Query with filter: Skill Name contains "[search term]"
2. If found: Show existing skill details
3. If not found: Offer to create new skill

---

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Invalid API key | Check NOTION_API_KEY in .env |
| 404 Not Found | Wrong database ID | Verify NOTION_SKILLS_DB_ID |
| Empty results | No matches or wrong filter | Try broader query, check filter syntax |

---

## Notes

- This skill is **read-only** - it only queries data
- For creating/updating records, use `export-skill-to-notion`
- Results are paginated (100 per page) - handle `has_more` for large databases
- API key must have access to the database (connect integration in Notion)