# Airtable Setup Guide

**Single source of truth for setting up Airtable integration with Nexus**

---

## Pre-Flight Check

Before ANY Airtable operation, verify setup:

```
🔍 Pre-flight check...

1. API Key:     [.env → AIRTABLE_API_KEY]
2. Base ID:     [optional - discovered automatically]

[ERROR] Missing config? → Run First-Time Setup below
[OK] All configured? → Proceed with operation
```

**To run check programmatically:** Use `00-system/skills/notion/airtable-master/scripts/check_airtable_config.py`

---

## First-Time Setup Wizard

### Interactive Setup Flow

```
[*] Airtable Setup Required

I'll help you set up Airtable integration:

Step 1: Create Personal Access Token (PAT)
   → Go to https://airtable.com/create/tokens
   → Click "Create new token"
   → Name it "Nexus Integration"
   → Add scopes (see below)
   → Select bases to access
   → Click "Create token"
   → Copy the token (starts with "pat.")

Step 2: Add to .env
   → I'll create/update your .env file with:
     AIRTABLE_API_KEY=pat.xxxxx...

Step 3: Validate Connection
   → I'll test the API connection
   → Discover accessible bases

Ready to start? (yes/no)
```

---

## Recommended Scopes

**Minimum for reading:**
- `data.records:read` - Read records
- `schema.bases:read` - Read base/table structure

**Full access:**
- `data.records:read` - Read records
- `data.records:write` - Create/update/delete records
- `schema.bases:read` - Read structure
- `schema.bases:write` - Modify structure (optional)
- `data.recordComments:read` - Read comments (optional)
- `data.recordComments:write` - Create comments (optional)

**For webhooks:**
- `webhook:manage` - Create/manage webhooks

---

## Configuration Files

### .env File

**Location:** Project root (`Nexus-v4/.env`)

**Required variables:**
```bash
AIRTABLE_API_KEY=pat.xxxxxxxxxxxxxxxx.xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

**How to set:**
```bash
# If .env doesn't exist, create it
echo "AIRTABLE_API_KEY=pat.your-token-here" > .env

# If .env exists, append
echo "AIRTABLE_API_KEY=pat.your-token-here" >> .env
```

### user-config.yaml File (Optional)

**Location:** `01-memory/user-config.yaml`

**Optional fields:**
```yaml
airtable_user_id: "usrxxxxxxxx"
airtable_default_base: "appxxxxxxxx"
```

---

## Validation

### Test API Connection

```bash
curl "https://api.airtable.com/v0/meta/whoami" \
  -H "Authorization: Bearer ${AIRTABLE_API_KEY}"
```

**Expected responses:**
- `401 Unauthorized` → Invalid PAT, check AIRTABLE_API_KEY
- `200 Success` → Connection works, shows user info

### Test Base Access

```bash
curl "https://api.airtable.com/v0/meta/bases" \
  -H "Authorization: Bearer ${AIRTABLE_API_KEY}"
```

**Expected responses:**
- `200 Success` → Lists accessible bases
- Empty `bases` array → PAT has no base access (add bases to token)

---

## Token Management

### Finding Your Token
1. Go to https://airtable.com/create/tokens
2. Your existing tokens are listed
3. Click a token to view/edit scopes

### Regenerating a Token
1. Go to https://airtable.com/create/tokens
2. Find your token
3. Click "Regenerate"
4. Update `.env` with new token

### Revoking a Token
1. Go to https://airtable.com/create/tokens
2. Find your token
3. Click "Delete"
4. Remove from `.env`

---

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| `401 Unauthorized` | Invalid PAT | Verify token in .env starts with `pat.` |
| `403 Forbidden` | Missing scope | Add required scope to token |
| `404 Not Found` | Wrong base/table ID | Verify IDs from Airtable URL |
| `.env not found` | Missing .env file | Create .env in project root |
| Empty bases list | No base access | Add bases to PAT in token settings |

---

## API Key vs PAT

**API Keys (DEPRECATED)**
- Deprecated February 1, 2024
- Full access to all bases
- No scope control
- No longer works

**Personal Access Tokens (CURRENT)**
- Started with `pat.`
- Granular scopes
- Per-base access control
- Can have multiple tokens

---

## Security Notes

- **Never commit** `.env` to git (already in .gitignore)
- **PATs are secrets** - treat like passwords
- **Use minimum scopes** - only request what you need
- **Rotate tokens** if compromised
- **One token per integration** - easier to revoke

---

## Reference from Skills

**In SKILL.md files, reference this document:**

```markdown
## Setup

Before using this skill, ensure Airtable is configured.

**Quick check:** Run pre-flight validation
**First time?** See [Setup Guide](../airtable-master/references/setup-guide.md)
```

---

**Last Updated:** 2025-12-11
