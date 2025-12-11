# Notion Setup Guide

**Single source of truth for setting up Notion integration with Nexus**

Reference this file from all Notion-related skills using progressive disclosure.

---

## Pre-Flight Check

Before ANY Notion operation, verify setup:

```
🔍 Pre-flight check...

1. API Key:     [.env → NOTION_API_KEY]
2. Database ID: [.env → NOTION_SKILLS_DB_ID]
3. User ID:     [user-config.yaml → notion_user_id] (export only)

❌ Missing config? → Run First-Time Setup below
✅ All configured? → Proceed with operation
```

**To run check programmatically:** Use `00-system/skills/notion-master/scripts/check_notion_config.py`

---

## First-Time Setup Wizard

### Interactive Setup Flow

```
🔧 Notion Setup Required

I'll help you set up Notion integration:

Step 1: Get API Key (choose one option)
   Option A: Use the shared team API key
      → Ask your team admin for the NOTION_API_KEY
      → This is the simplest option for most users
      → Recommended for team collaboration

   Option B: Create your own (admin only)
      → Go to https://www.notion.so/my-integrations
      → Click "New integration" → Name: "Nexus"
      → Copy the "Internal Integration Secret"
      → Note: Only workspace admins can create integrations

Step 2: Add to .env
   → I'll create/update your .env file with:
     NOTION_API_KEY=your-key-here
     NOTION_SKILLS_DB_ID=2bc2cadf-bbbc-80be-af8a-d45dfc8dfa2e

Step 3: Connect Database (if using your own key)
   → Open "Beam Nexus Skills" database in Notion
   → Click "..." → "Connections" → Add your integration
   → Skip this if using the shared team key (already connected)

Step 4: Get Your User ID (export only)
   → I'll query Notion API for your user info
   → Save to user-config.yaml (for Owner tracking)

Ready to start? (yes/no)
```

**Why shared keys work:** Ownership is tracked via `notion_user_id` in user-config.yaml, not the API key. Each user's skills will show their name as Owner even when using a shared API key.

---

## Configuration Files

### .env File

**Location:** Project root (`Nexus-v4/.env`)

**Required variables:**
```bash
NOTION_API_KEY=secret_xxxxxxxxxxxxxxxxxxxxx
NOTION_SKILLS_DB_ID=2bc2cadf-bbbc-80be-af8a-d45dfc8dfa2e
```

**How to set:**
```bash
# If .env doesn't exist, create it
echo "NOTION_API_KEY=your-key-here" > .env
echo "NOTION_SKILLS_DB_ID=2bc2cadf-bbbc-80be-af8a-d45dfc8dfa2e" >> .env

# If .env exists, append or update
```

### user-config.yaml File

**Location:** `01-memory/user-config.yaml`

**Required fields (for export):**
```yaml
notion_user_id: "abc123-user-id"
notion_user_name: "Your Name"
```

**How to get user ID:**
```bash
# Query Notion API
curl -s "https://api.notion.com/v1/users/me" \
  -H "Authorization: Bearer ${NOTION_API_KEY}" \
  -H "Notion-Version: 2022-06-28"

# Extract "id" from response
# Add to user-config.yaml
```

---

## Validation

### Test API Connection

```bash
curl -s "https://api.notion.com/v1/users/me" \
  -H "Authorization: Bearer ${NOTION_API_KEY}" \
  -H "Notion-Version: 2022-06-28"
```

**Expected responses:**
- `401 Unauthorized` → Invalid API key, check NOTION_API_KEY
- `200 Success` → Connection works, save user info

### Test Database Access

```bash
curl -s -X POST "https://api.notion.com/v1/databases/${NOTION_SKILLS_DB_ID}/query" \
  -H "Authorization: Bearer ${NOTION_API_KEY}" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{"page_size": 1}'
```

**Expected responses:**
- `404 Not Found` → Wrong database ID or integration not connected
- `403 Forbidden` → Integration doesn't have access to database
- `200 Success` → Database accessible

---

## Database Connection (for custom keys)

If you created your own Notion integration (Step 1, Option B):

1. Open Notion workspace
2. Navigate to "Beam Nexus Skills" database
3. Click "..." (three dots) → "Connections"
4. Select your integration from the list
5. Click "Confirm"

**Skip this step** if using the shared team API key (already connected).

---

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| `401 Unauthorized` | Invalid API key | Check NOTION_API_KEY in .env |
| `404 Not Found` | Wrong database ID | Verify NOTION_SKILLS_DB_ID |
| `403 Forbidden` | Integration not connected | Connect integration to database |
| `.env not found` | Missing .env file | Create .env in project root |
| `notion_user_id missing` | Not in user-config.yaml | Run Step 4 of setup |

---

## Automated Setup Script

**Script:** `00-system/skills/notion-master/scripts/setup_notion.py`

**What it does:**
1. Checks for existing .env and user-config.yaml
2. Guides user through API key setup (Option A: shared key, Option B: custom integration)
3. Tests API connection and database access
4. Retrieves user ID from Notion API
5. Saves configuration to .env and user-config.yaml
6. Auto-runs database discovery to populate context

**Usage:**
```bash
python 00-system/skills/notion-master/scripts/setup_notion.py
```

---

## Security Notes

- **Never commit** `.env` to git (already in .gitignore)
- **API keys are secrets** - treat like passwords
- **Shared keys are OK** for team collaboration (ownership tracked separately)
- **Rotate keys** if compromised

---

## Reference from Skills

**In SKILL.md files, reference this document:**

```markdown
## Setup

Before using this skill, ensure Notion is configured.

**Quick check:** Run pre-flight validation
**First time?** See [Setup Guide](../notion-master/references/setup-guide.md)
```

This keeps SKILL.md files concise while providing full setup details on-demand.
