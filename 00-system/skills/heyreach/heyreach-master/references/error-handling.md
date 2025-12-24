# HeyReach Error Handling

Troubleshooting guide for HeyReach API integration.

---

## HTTP Error Codes

### 400 Bad Request
**Cause**: Invalid request parameters or malformed JSON

**Solutions**:
- Check request body format
- Verify required fields are included
- Ensure data types are correct (strings, numbers, arrays)

```json
{
  "error": "Bad Request",
  "message": "Invalid campaign ID format"
}
```

---

### 401 Unauthorized
**Cause**: Invalid or missing API key

**Solutions**:
1. Verify `HEYREACH_API_KEY` is set in `.env`
2. Check API key is valid (not expired)
3. Ensure no extra spaces in the key
4. Regenerate key in HeyReach settings if needed

```json
{
  "error": "Unauthorized",
  "message": "Invalid API key"
}
```

**Fix**:
```bash
# Check current config
python 00-system/skills/heyreach/heyreach-master/scripts/check_heyreach_config.py --json

# If invalid, update .env with new key
HEYREACH_API_KEY=your-new-key
```

---

### 403 Forbidden
**Cause**: API key lacks required permissions or feature not available

**Solutions**:
1. Verify your HeyReach subscription includes API access
2. Check if the specific feature is available in your plan
3. Contact HeyReach support to enable API access

```json
{
  "error": "Forbidden",
  "message": "API access not available for your subscription"
}
```

---

### 404 Not Found
**Cause**: Resource doesn't exist

**Solutions**:
- Verify the campaign/lead/list ID is correct
- Check if the resource was deleted
- Use list endpoints to find valid IDs

```json
{
  "error": "Not Found",
  "message": "Campaign not found"
}
```

---

### 429 Too Many Requests
**Cause**: Rate limit exceeded (300 requests/minute)

**Solutions**:
1. Client automatically retries with backoff
2. For bulk operations, add delays between requests
3. Batch operations when possible

```json
{
  "error": "Too Many Requests",
  "message": "Rate limit exceeded. Retry after 60 seconds."
}
```

**Automatic Handling**:
The `heyreach_client.py` handles rate limits automatically with exponential backoff.

---

### 500 Internal Server Error
**Cause**: HeyReach server issue

**Solutions**:
1. Wait and retry (client does this automatically)
2. Check HeyReach status page
3. If persistent, contact support

---

## Common Issues

### Connection Timeout
**Symptoms**: Request hangs then fails

**Solutions**:
- Check internet connectivity
- Verify HeyReach API is accessible
- Try again later

### Invalid JSON Response
**Symptoms**: Parsing errors

**Solutions**:
- Check for empty responses (204 status)
- Verify Content-Type header
- Log raw response for debugging

### Campaign Not Starting
**Symptoms**: Toggle doesn't work

**Solutions**:
- Verify LinkedIn accounts are connected
- Check campaign has leads
- Ensure no validation errors in campaign settings

---

## Debugging Tips

### Enable Logging
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Check Raw Response
```python
response = requests.get(url, headers=headers)
print(f"Status: {response.status_code}")
print(f"Headers: {response.headers}")
print(f"Body: {response.text}")
```

### Validate API Key
```bash
curl -X GET "https://api.heyreach.io/api/public/v2/linkedin-accounts/All" \
  -H "X-API-KEY: your-api-key"
```

---

## Error Recovery Patterns

### Retry with Backoff
```python
import time

for attempt in range(3):
    try:
        result = client.get(endpoint)
        break
    except HeyReachError as e:
        if e.status_code == 429:
            time.sleep(2 ** attempt)
        else:
            raise
```

### Graceful Degradation
```python
try:
    campaigns = client.list_campaigns()
except HeyReachError as e:
    if e.status_code == 403:
        print("API access not available - check subscription")
    else:
        print(f"Error: {e.message}")
```

---

**Version**: 1.0
**Updated**: 2025-12-19
