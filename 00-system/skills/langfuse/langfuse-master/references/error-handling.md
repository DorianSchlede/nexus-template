# Langfuse Error Handling

## HTTP Status Codes

| Code | Meaning | Action |
|------|---------|--------|
| 200 | Success | Process response |
| 400 | Bad Request | Check request parameters |
| 401 | Unauthorized | Check API keys |
| 403 | Forbidden | Check permissions |
| 404 | Not Found | Resource doesn't exist |
| 429 | Rate Limited | Wait and retry |
| 500 | Server Error | Retry later |

## Common Errors

### Authentication Errors

**401 Unauthorized**
```json
{"error": "Unauthorized", "message": "Invalid API key"}
```
Fix:
1. Verify LANGFUSE_PUBLIC_KEY and LANGFUSE_SECRET_KEY
2. Check keys aren't swapped
3. Ensure keys are for correct project

### Resource Not Found

**404 Not Found**
```json
{"error": "Not Found", "message": "Trace with ID xyz not found"}
```
Fix:
1. Verify ID exists
2. Check correct project
3. Resource may have been deleted

### Validation Errors

**400 Bad Request**
```json
{"error": "Bad Request", "message": "Invalid parameter: limit must be <= 100"}
```
Fix:
1. Check parameter constraints in API docs
2. Validate input before sending

### Rate Limiting

**429 Too Many Requests**
```json
{"error": "Too Many Requests", "message": "Rate limit exceeded"}
```
Fix:
1. Wait for rate limit window to reset
2. Implement exponential backoff
3. Reduce request frequency

## Python Error Handling

```python
import requests
from langfuse_client import get_client

client = get_client()

try:
    result = client.get("/traces/invalid-id")
except requests.exceptions.HTTPError as e:
    if e.response.status_code == 404:
        print("Trace not found")
    elif e.response.status_code == 401:
        print("Authentication failed - check API keys")
    else:
        print(f"API error: {e}")
except requests.exceptions.ConnectionError:
    print("Connection failed - check LANGFUSE_HOST")
```

## AI Action Mapping

When errors occur, the AI should:

| Error | AI Action |
|-------|-----------|
| 401 | Run `check_langfuse_config.py --json`, prompt for keys |
| 404 | Inform user resource not found, suggest alternatives |
| 429 | Wait, then retry |
| 500 | Suggest trying again later |
