# Google API Error Handling

Common errors and solutions for Google integration skills.

---

## Authentication Errors

### 401 Unauthorized

**Error:** `HttpError 401: Request had invalid authentication credentials`

**Causes:**
- Token expired
- Token revoked
- Invalid credentials

**Solutions:**
```bash
# Re-authenticate
uv run python 00-system/skills/google/google-master/scripts/google_auth.py --login
```

---

### 403 Forbidden

**Error:** `HttpError 403: The caller does not have permission`

**Causes:**
- Missing required scope
- Resource not shared with user
- API not enabled

**Solutions:**

1. **Missing scope:** Re-authenticate to grant all permissions
   ```bash
   uv run python google_auth.py --login
   ```

2. **Resource not shared:** The document/sheet/calendar isn't shared with you
   - Ask owner to share it
   - Check you're using the correct account

3. **API not enabled:** Enable the API in Google Cloud Console
   - Go to APIs & Services > Library
   - Search for the API (Gmail, Docs, Sheets, Calendar)
   - Click Enable

---

### 403 Access Denied (OAuth)

**Error:** `Error 403: access_denied - The developer hasn't given you access`

**Cause:** You're not listed as a test user

**Solution:**
1. Go to Google Cloud Console
2. APIs & Services > OAuth consent screen
3. Test users > Add Users
4. Add your email
5. Wait 5 minutes, try again

---

## Resource Errors

### 404 Not Found

**Error:** `HttpError 404: Requested entity was not found`

**Causes:**
- Wrong document/spreadsheet/calendar ID
- Resource was deleted
- Typo in ID

**Solutions:**
1. Verify the ID from the URL:
   - Docs: `https://docs.google.com/document/d/[ID]/edit`
   - Sheets: `https://docs.google.com/spreadsheets/d/[ID]/edit`
   - Calendar: Check calendar settings for Calendar ID

2. Make sure the resource exists and is accessible

---

### 400 Bad Request

**Error:** `HttpError 400: Invalid value`

**Causes:**
- Malformed request
- Invalid parameters
- Wrong data format

**Solutions:**
- Check parameter formats (dates, IDs, ranges)
- For Sheets: verify A1 notation (e.g., `Sheet1!A1:B10`)
- For Calendar: use ISO 8601 dates (`2025-12-17T10:00:00Z`)

---

## Rate Limiting

### 429 Too Many Requests

**Error:** `HttpError 429: Rate Limit Exceeded`

**Causes:**
- Too many requests per second
- Daily quota exceeded

**Solutions:**
1. **Short-term:** Wait and retry with exponential backoff
2. **Long-term:**
   - Batch requests where possible
   - Cache responses
   - Increase quota in Google Cloud Console (if available)

**Default quotas:**
| API | Requests/min | Requests/day |
|-----|--------------|--------------|
| Gmail | 250 | 1,000,000 |
| Docs | 300 | 300,000 |
| Sheets | 300 | 300,000 |
| Calendar | 500 | 1,000,000 |

---

## Service-Specific Errors

### Gmail

**"Recipient address required"**
- Missing `to` field in send request

**"Invalid RFC 822 message"**
- Malformed email structure
- Check headers and body encoding

**"Mail service not enabled"**
- Gmail API not enabled for this project

### Google Docs

**"Invalid document ID"**
- Check the ID from the document URL

**"Invalid requests[0].insertText"**
- Index out of bounds
- Use `get_document_info()` to find valid indices

### Google Sheets

**"Unable to parse range"**
- Invalid A1 notation
- Check sheet name exists (case-sensitive)
- Use quotes for sheet names with spaces: `'Sheet Name'!A1:B10`

**"Requested writing within range, but values do not match"**
- Data dimensions don't match the range
- Ensure rows/columns align

### Google Calendar

**"Invalid conference type"**
- Check conferenceDataVersion parameter

**"End time must be after start time"**
- Verify datetime ordering

---

## Network Errors

### Connection Timeout

**Error:** `TimeoutError` or `Connection timed out`

**Solutions:**
- Check internet connection
- Retry the request
- Increase timeout settings

### SSL Certificate Error

**Error:** `SSL: CERTIFICATE_VERIFY_FAILED`

**Solutions:**
- Update certifi: `pip install --upgrade certifi`
- Check system time is correct

---

## Token Issues

### "Token has been expired or revoked"

**Cause:** Token no longer valid

**Solution:**
```bash
uv run python google_auth.py --logout
uv run python google_auth.py --login
```

### "Invalid grant"

**Cause:** Refresh token invalid (often after password change)

**Solution:**
```bash
# Remove old token and re-authenticate
rm 01-memory/integrations/google-token.json
uv run python google_auth.py --login
```

---

## Debugging Tips

### 1. Check Configuration First

```bash
uv run python 00-system/skills/google/google-master/scripts/check_google_config.py --json
```

### 2. Verify Service Access

```python
# Quick test for each service
from google_auth import get_service

# Test Gmail
gmail = get_service('gmail')
gmail.users().labels().list(userId='me').execute()

# Test Docs
docs = get_service('docs')
docs.documents().get(documentId='your-doc-id').execute()

# Test Sheets
sheets = get_service('sheets')
sheets.spreadsheets().get(spreadsheetId='your-sheet-id').execute()

# Test Calendar
calendar = get_service('calendar')
calendar.calendarList().list().execute()
```

### 3. Enable Verbose Logging

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### 4. Check Scopes in Token

```python
import json
with open('01-memory/integrations/google-token.json') as f:
    token = json.load(f)
    print("Scopes:", token.get('scopes', []))
```

---

## Error Code Quick Reference

| Code | Meaning | Common Fix |
|------|---------|------------|
| 400 | Bad Request | Check parameters |
| 401 | Unauthorized | Re-authenticate |
| 403 | Forbidden | Check permissions/scopes |
| 404 | Not Found | Verify resource ID |
| 429 | Rate Limited | Wait and retry |
| 500 | Server Error | Retry later |
| 503 | Service Unavailable | Retry later |

---

**Version**: 1.0
**Updated**: 2025-12-17
