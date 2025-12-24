# Airtable Error Handling

**Common errors, causes, and solutions for all Airtable integration skills.**

---

## Common HTTP Errors

| Code | Name | Cause | Solution |
|------|------|-------|----------|
| 400 | Bad Request | Invalid request body | Check JSON format, field names |
| 401 | Unauthorized | Invalid/expired PAT | Check AIRTABLE_API_KEY in .env |
| 403 | Forbidden | Missing scope or permission | Add required scope to PAT |
| 404 | Not Found | Base/table/record doesn't exist | Verify IDs from Airtable URL |
| 413 | Payload Too Large | Request body too big | Reduce batch size |
| 422 | Unprocessable | Validation error | Check field types, required fields |
| 429 | Too Many Requests | Rate limited | Wait 30s, implement backoff |
| 500 | Server Error | Airtable issue | Retry after delay |
| 503 | Service Unavailable | Maintenance | Check Retry-After header |

---

## Error Response Format

```json
{
  "error": {
    "type": "INVALID_REQUEST_BODY",
    "message": "Could not parse request body"
  }
}
```

---

## Detailed Error Explanations

### 401 Unauthorized

**Causes:**
- PAT is invalid or malformed
- PAT was regenerated/revoked
- Missing `Bearer ` prefix in header

**Solutions:**
1. Verify token starts with `pat.`
2. Check for extra spaces or characters
3. Regenerate token if needed
4. Ensure header is `Authorization: Bearer pat.xxx...`

### 403 Forbidden

**Causes:**
- PAT doesn't have required scope
- PAT doesn't have access to the base
- Field/table has permission restrictions

**Solutions:**
1. Go to https://airtable.com/create/tokens
2. Edit your token
3. Add missing scope (e.g., `data.records:write`)
4. Add base to token's access list

### 404 Not Found

**Causes:**
- Base ID is incorrect
- Table ID/name is incorrect
- Record was deleted
- Using table name when ID is required (or vice versa)

**Solutions:**
1. Get base ID from Airtable URL: `airtable.com/{baseId}/...`
2. Get table ID from base schema endpoint
3. Use URL-encoded table names with spaces

### 422 Unprocessable Entity

**Causes:**
- Required field missing
- Wrong field type (e.g., string for number field)
- Invalid option for select field
- Formula syntax error in filterByFormula

**Solutions:**
1. Check required fields in table
2. Verify field types match expected format
3. Use `typecast: true` for automatic conversion
4. Validate formula syntax

### 429 Too Many Requests

**Causes:**
- Exceeded 5 requests/second per base
- Exceeded 50 requests/second per token
- Monthly limit exceeded (Free/Team plans)

**Solutions:**
1. Wait 30 seconds before retrying
2. Implement exponential backoff
3. Use batch operations (10 records/request)
4. Check monthly usage if on Free/Team plan

---

## Skill-Specific Errors

### airtable-connect Errors

| Error | Cause | Solution |
|-------|-------|----------|
| No bases found | PAT has no base access | Add bases to PAT |
| Schema fetch failed | Base ID incorrect | Verify base ID |
| Permission denied | Missing `schema.bases:read` | Add scope to PAT |

### airtable-query Errors

| Error | Cause | Solution |
|-------|-------|----------|
| Invalid formula | filterByFormula syntax error | Check formula syntax |
| Field not found | Field name changed/deleted | Verify field name in schema |
| No records found | Filter too restrictive | Check filter criteria |

### airtable-sync Errors

| Error | Cause | Solution |
|-------|-------|----------|
| Create failed | Missing required fields | Check table schema |
| Update failed | Record was deleted | Verify record exists |
| Batch too large | >10 records in batch | Split into smaller batches |

---

## Configuration Errors

| Issue | Cause | Solution |
|-------|-------|----------|
| `.env` not found | Missing .env file | Create .env in Nexus root |
| PAT format error | Wrong token format | Ensure token starts with `pat.` |
| YAML parse error | Invalid user-config.yaml | Fix YAML formatting |
| Missing requests | Python package not installed | Run: `pip install requests` |

---

## Network Errors

| Error | Cause | Solution |
|-------|-------|----------|
| Connection timeout | Network/firewall issue | Check internet, increase timeout |
| SSL error | Proxy/certificate issue | Configure proxy or VPN |
| DNS failed | Internet connectivity | Check network connection |

---

## Troubleshooting Steps

### Step 1: Validate Configuration

```bash
python 00-system/skills/notion/airtable-master/scripts/check_airtable_config.py
```

This validates:
- ✅ `.env` file exists with AIRTABLE_API_KEY
- ✅ PAT format is correct (starts with `pat.`)
- ✅ API connection works
- ✅ At least one base is accessible

### Step 2: Test API Connection

```bash
curl "https://api.airtable.com/v0/meta/whoami" \
  -H "Authorization: Bearer ${AIRTABLE_API_KEY}"
```

**Success response:**
```json
{"id": "usrXXX", "email": "you@example.com", "scopes": [...]}
```

### Step 3: Verify Base Access

```bash
curl "https://api.airtable.com/v0/meta/bases" \
  -H "Authorization: Bearer ${AIRTABLE_API_KEY}"
```

**Success response:**
```json
{"bases": [{"id": "appXXX", "name": "My Base", ...}]}
```

### Step 4: Check Python Dependencies

```bash
python -c "import requests; import yaml; print('✅ Dependencies OK')"
```

---

## Error Recovery Patterns

### Pattern 1: Retry with Exponential Backoff

```python
import time

def request_with_retry(method, url, headers, json=None, max_retries=3):
    for attempt in range(max_retries):
        response = requests.request(method, url, headers=headers, json=json)

        if response.status_code == 200:
            return response.json()

        if response.status_code in [429, 500, 503]:
            wait = min(30, 2 ** attempt)  # 1s, 2s, 4s, max 30s
            time.sleep(wait)
            continue

        # Non-retryable error
        response.raise_for_status()

    raise Exception("Max retries exceeded")
```

### Pattern 2: Graceful Degradation

```python
def get_records_safe(base_id, table_name):
    try:
        return get_all_records(base_id, table_name)
    except requests.exceptions.RequestException as e:
        print(f"⚠️ Could not fetch records: {e}")
        return []  # Return empty list instead of failing
```

### Pattern 3: Batch Error Handling

```python
def create_records_batch(base_id, table_name, records):
    results = {"success": [], "failed": []}

    for i in range(0, len(records), 10):
        batch = records[i:i+10]
        try:
            created = create_batch(base_id, table_name, batch)
            results["success"].extend(created)
        except Exception as e:
            results["failed"].extend([{"record": r, "error": str(e)} for r in batch])

    return results
```

---

## Getting Help

If errors persist:

1. **Check Airtable Status:** https://status.airtable.com
2. **API Documentation:** https://airtable.com/developers/web/api
3. **Community Forum:** https://community.airtable.com
4. **Re-run Setup:** `python airtable-master/scripts/check_airtable_config.py`

---

**Last Updated:** 2025-12-11
