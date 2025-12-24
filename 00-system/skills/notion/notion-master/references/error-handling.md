# Notion API Error Handling

Common errors, causes, and solutions for all Notion integration skills.

---

## Common Errors

| Error Code | Error Message | Cause | Solution |
|------------|---------------|-------|----------|
| 401 | Unauthorized | Invalid or expired API key | Check `NOTION_API_KEY` in `.env`, ensure it starts with `secret_` |
| 403 | Forbidden | Integration not connected to database | Connect integration to database in Notion UI |
| 404 | Not Found | Database ID incorrect or inaccessible | Verify `NOTION_SKILLS_DB_ID` in `.env` |
| 400 | Bad Request | Invalid property format or type | Check field mapping against database schema |
| 400 | Validation error | Required field missing | Ensure all required properties are provided |
| 429 | Rate limited | Too many requests | Wait and retry (Notion allows 3 requests/second) |
| 500 | Internal server error | Notion API issue | Retry after a few seconds |
| 503 | Service unavailable | Notion maintenance | Wait and retry later |

---

## Skill-Specific Errors

### query-notion-db Errors

| Error | Cause | Solution |
|-------|-------|----------|
| No results found | Filter too restrictive or empty database | Check filter criteria, verify database has entries |
| Invalid filter | Filter syntax incorrect | Review Notion API filter documentation |
| Missing database ID | `NOTION_SKILLS_DB_ID` not set | Add to `.env` file |

### import-skill-to-nexus Errors

| Error | Cause | Solution |
|-------|-------|----------|
| No file attached | Skill entry has no file property | Select a different skill with attached file |
| File download failed | Network issue or invalid file URL | Retry or check internet connection |
| Invalid SKILL.md format | Missing YAML frontmatter | Manually fix or skip skill |
| Skill already exists locally | Duplicate in `03-skills/` | Choose: overwrite, backup, or skip |
| Invalid skill structure | Missing required sections | Use fallback: create from Notion properties |

### export-skill-to-notion Errors

| Error | Cause | Solution |
|-------|-------|----------|
| Missing `notion_user_id` | Not set in `user-config.yaml` | Run setup to get user ID from API |
| Duplicate skill name | Skill already exists in Notion | Choose: update existing or cancel |
| File upload failed | File too large or network issue | Check file size (<5MB), retry upload |
| Invalid team name | Team contains special characters | Use alphanumeric names only |
| Missing SKILL.md | Invalid skill path | Verify skill exists in `03-skills/` |

---

## Configuration Errors

| Issue | Cause | Solution |
|-------|-------|----------|
| `.env` file not found | Missing in Nexus root | Create `.env` with `NOTION_API_KEY` and `NOTION_SKILLS_DB_ID` |
| `user-config.yaml` parse error | Invalid YAML syntax | Fix YAML formatting (check indentation) |
| PyYAML not installed | Missing Python dependency | Run: `pip install pyyaml` |
| requests not installed | Missing Python dependency | Run: `pip install requests` |
| API key starts with wrong prefix | Copied wrong value | Ensure key starts with `secret_`, not `ntn_` |

---

## Network & Timeout Errors

| Error | Cause | Solution |
|-------|-------|----------|
| Connection timeout | Network issue or slow connection | Retry with longer timeout |
| SSL certificate error | Corporate proxy or firewall | Configure proxy settings or use VPN |
| DNS resolution failed | Internet connectivity issue | Check internet connection |
| Connection refused | Notion API down (rare) | Check Notion status page |

---

## Troubleshooting Steps

### Step 1: Validate Configuration

Run the configuration checker:
```bash
python 00-system/skills/notion-master/scripts/check_notion_config.py
```

This validates:
-  `.env` file exists and has required variables
-  API key format is correct
-  API connection works
-  Database is accessible
-  User ID is set (for exports)

### Step 2: Test API Connection Manually

Test basic API connectivity:
```bash
curl -s "https://api.notion.com/v1/users/me" \
  -H "Authorization: Bearer ${NOTION_API_KEY}" \
  -H "Notion-Version: 2022-06-28"
```

**Expected response (success):**
```json
{
  "object": "user",
  "id": "abc123...",
  "name": "Your Name",
  "type": "person"
}
```

**Common errors:**
- `{"object": "error", "status": 401}` ’ Invalid API key
- Connection refused ’ Network issue
- Timeout ’ Check firewall/proxy

### Step 3: Verify Database Access

Test database query:
```bash
curl -s "https://api.notion.com/v1/databases/${NOTION_SKILLS_DB_ID}" \
  -H "Authorization: Bearer ${NOTION_API_KEY}" \
  -H "Notion-Version: 2022-06-28"
```

**Expected response (success):**
```json
{
  "object": "database",
  "id": "2bc2cadf...",
  "title": [{"plain_text": "Beam Nexus Skills"}]
}
```

**Common errors:**
- `404` ’ Database ID incorrect or integration not connected
- `403` ’ Integration lacks permission (connect it in Notion UI)

### Step 4: Check Python Dependencies

Ensure required packages are installed:
```bash
python -c "import yaml; import requests; print(' Dependencies OK')"
```

If error occurs:
```bash
pip install pyyaml requests
```

---

## Error Recovery Patterns

### Pattern 1: Retry with Exponential Backoff

For transient errors (429, 500, 503):
```python
import time

max_retries = 3
for attempt in range(max_retries):
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            break
        elif response.status_code in [429, 500, 503]:
            wait = 2 ** attempt  # 1s, 2s, 4s
            time.sleep(wait)
    except requests.exceptions.RequestException:
        if attempt == max_retries - 1:
            raise
```

### Pattern 2: Graceful Degradation

If file download fails during import:
```python
# Fallback: Create skill from Notion properties only
if file_download_failed:
    create_skill_from_metadata(
        name=notion_properties['Skill Name'],
        description=notion_properties['Description'],
        purpose=notion_properties.get('Purpose', '')
    )
```

### Pattern 3: User Confirmation on Conflicts

For duplicate detection:
```python
if skill_exists_locally:
    print("   Skill already exists")
    choice = input("1) Overwrite 2) Backup 3) Skip: ")
    if choice == "1":
        overwrite_skill()
    elif choice == "2":
        backup_then_import()
    else:
        return
```

---

## Logging & Debugging

### Enable Verbose Logging

For detailed API debugging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Common Debug Checks

1. **Print API key prefix**: `echo ${NOTION_API_KEY:0:10}` (should show `secret_xxx`)
2. **Check database ID**: `echo ${NOTION_SKILLS_DB_ID}` (should be 32 hex chars)
3. **Verify file paths**: Use absolute paths to avoid confusion
4. **Check YAML syntax**: Use online YAML validator

---

## Getting Help

If errors persist:

1. **Check Notion Status**: https://status.notion.so
2. **Review API Docs**: https://developers.notion.com
3. **Team Support**: Ask admin for shared API key validation
4. **Re-run Setup**: `python 00-system/skills/notion-master/scripts/setup_notion.py`

---

**Last Updated**: 2025-12-10
