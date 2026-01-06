# Beam Error Handling Guide

Common errors and solutions for Beam AI integration.

---

## HTTP Error Codes

### 401 Unauthorized

**Causes:**
- Access token expired (tokens last 1 hour)
- Invalid API key
- Missing Authorization header

**Solutions:**
1. Refresh the access token:
   ```python
   python scripts/refresh_token.py
   ```
2. Re-authenticate with API key:
   ```python
   python scripts/get_access_token.py
   ```
3. Verify API key is correct in `.env`

### 403 Forbidden

**Causes:**
- No access to workspace
- Insufficient permissions
- API key doesn't have required scopes

**Solutions:**
1. Verify workspace ID is correct
2. Check API key permissions in Beam settings
3. Contact workspace admin for access

### 404 Not Found

**Causes:**
- Invalid agent ID
- Invalid task ID
- Resource was deleted

**Solutions:**
1. Verify resource IDs are correct
2. List available resources first
3. Check resource wasn't deleted

### 429 Rate Limited

**Causes:**
- Too many requests in short period
- Exceeded workspace rate limits

**Solutions:**
1. Implement exponential backoff
2. Cache responses where possible
3. Batch operations when supported

**Retry pattern:**
```python
import time

def make_request_with_retry(func, max_retries=3):
    for attempt in range(max_retries):
        try:
            return func()
        except RateLimitError:
            wait = 2 ** attempt  # 1, 2, 4 seconds
            time.sleep(wait)
    raise Exception("Max retries exceeded")
```

### 500 Server Error

**Causes:**
- Beam platform issue
- Temporary outage

**Solutions:**
1. Wait and retry
2. Check [Beam status page](https://status.beam.ai)
3. Contact Beam support if persistent

---

## Configuration Errors

### Missing API Key

**Error:**
```
BEAM_API_KEY not found in .env
```

**Solution:**
1. Add to `.env`:
   ```
   BEAM_API_KEY=bm_key_your_key_here
   ```
2. Or run setup wizard:
   ```bash
   python scripts/setup_beam.py
   ```

### Missing Workspace ID

**Error:**
```
BEAM_WORKSPACE_ID not found in .env
```

**Solution:**
1. Find workspace ID in Beam Settings → Workspace
2. Add to `.env`:
   ```
   BEAM_WORKSPACE_ID=your-workspace-uuid
   ```

### Invalid API Key Format

**Error:**
```
Invalid API key format
```

**Solution:**
- API keys must start with `bm_key_`
- Verify no extra spaces or characters
- Generate new key if corrupted

---

## Task Errors

### Task Stuck in QUEUED

**Causes:**
- Agent not published
- Trigger not configured
- System backlog

**Solutions:**
1. Verify agent is published
2. Check agent configuration
3. Wait for queue processing

### Task FAILED Status

**Causes:**
- Node execution error
- Integration auth expired
- Invalid input data

**Solutions:**
1. Check task execution logs
2. Review node-level errors
3. Verify integration connections
4. Test with simplified input

### HITL Task Pending

**Causes:**
- Task requires human approval
- User input needed

**Solutions:**
1. Check task status for required action
2. Provide user input via API:
   ```python
   python scripts/provide_user_input.py --task-id xxx --input "response"
   ```
3. Or approve/reject:
   ```python
   python scripts/approve_task.py --task-id xxx
   ```

---

## Agent Graph Errors

### Node Test Failed

**Causes:**
- Invalid node configuration
- Missing required parameters
- Integration connection issue

**Solutions:**
1. Review node objective and criteria
2. Verify all required params provided
3. Check integration credentials
4. Test with minimal input first

### Update Node Failed

**Causes:**
- Invalid node ID
- Graph is locked/published
- Permission issue

**Solutions:**
1. Verify node ID exists
2. Use draft graph for updates
3. Check edit permissions

---

## Integration Errors

### Token Expired During Operation

**Pattern:**
```python
def ensure_valid_token():
    """Check token validity and refresh if needed"""
    # Tokens expire after 1 hour
    # Proactively refresh before expiry
    pass
```

### Connection Timeout

**Causes:**
- Network issues
- Large payload
- Slow response

**Solutions:**
1. Increase timeout:
   ```python
   requests.get(url, timeout=60)
   ```
2. Check network connectivity
3. Try smaller payloads

---

## Debugging Tips

### Enable Verbose Logging

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Check Request/Response

```python
response = requests.get(url, headers=headers)
print(f"Status: {response.status_code}")
print(f"Headers: {response.headers}")
print(f"Body: {response.text}")
```

### Validate JSON Payload

```python
import json
try:
    json.loads(payload)
except json.JSONDecodeError as e:
    print(f"Invalid JSON: {e}")
```

---

## Getting Help

1. **Check logs** - Task execution logs show detailed errors
2. **Use LangFuse** - Deep execution tracing for debugging
3. **Beam documentation** - https://docs.beam.ai
4. **Support** - Contact Beam support for platform issues
