# NotebookLM Enterprise Error Handling

Common errors and solutions for NotebookLM Enterprise API.

---

## HTTP Error Codes

### 400 Bad Request

**Cause:** Invalid request format or missing required fields.

**Solutions:**
1. Check JSON syntax
2. Verify required fields are present
3. Check field types match expected format

**Example:**
```json
{"error": {"message": "Invalid notebook title"}}
```

---

### 401 Unauthorized

**Cause:** Invalid or expired access token.

**Solutions:**
1. Refresh token: `gcloud auth print-access-token`
2. Re-authenticate: `gcloud auth login`
3. Check token hasn't expired

**Example:**
```json
{"error": {"message": "Request had invalid authentication credentials"}}
```

---

### 403 Forbidden

**Cause:** Missing permissions or API not enabled.

**Solutions:**
1. Enable Discovery Engine API in Cloud Console
2. Verify NotebookLM Enterprise is enabled for your Workspace
3. Check IAM roles (need `NotebookLM Enterprise User`)
4. Verify project has NotebookLM Enterprise access

**Example:**
```json
{"error": {"message": "Permission denied on resource"}}
```

---

### 404 Not Found

**Cause:** Resource doesn't exist.

**Solutions:**
1. Verify notebook ID is correct
2. Check source ID exists
3. Confirm resource wasn't deleted

**Example:**
```json
{"error": {"message": "Notebook not found"}}
```

---

### 429 Too Many Requests

**Cause:** Rate limit exceeded.

**Solutions:**
1. Wait and retry (exponential backoff)
2. Reduce request frequency
3. Request quota increase if needed

**Example:**
```json
{"error": {"message": "Quota exceeded for rate limit"}}
```

---

### 500 Internal Server Error

**Cause:** Server-side issue.

**Solutions:**
1. Wait and retry
2. Check Google Cloud Status page
3. Report if persistent

---

## Common Error Scenarios

### "gcloud not found"

**Cause:** Google Cloud SDK not installed.

**Solution:**
```bash
# Install from https://cloud.google.com/sdk/docs/install
```

---

### "Not authenticated"

**Cause:** gcloud session expired.

**Solution:**
```bash
gcloud auth login
gcloud auth application-default login
```

---

### "Project number not found"

**Cause:** Missing or incorrect project configuration.

**Solution:**
```bash
# Get your project number
gcloud projects describe YOUR_PROJECT_ID --format='value(projectNumber)'

# Add to .env
echo "GOOGLE_CLOUD_PROJECT_NUMBER=123456789012" >> .env
```

---

### "API not enabled"

**Cause:** Discovery Engine API not enabled.

**Solution:**
```bash
gcloud services enable discoveryengine.googleapis.com
```

Or via Cloud Console:
1. Go to APIs & Services > Library
2. Search "Discovery Engine API"
3. Click Enable

---

### Audio Overview "IN_PROGRESS" for long time

**Cause:** Audio generation takes 5-15 minutes.

**Solution:**
1. Wait for processing
2. Poll status every 30 seconds
3. Check if source content is processable

---

### "Unsupported file type"

**Cause:** File format not supported.

**Supported formats:**
- Documents: PDF, TXT, MD, DOCX, PPTX, XLSX
- Audio: MP3, WAV, AAC, OGG, FLAC, M4A
- Images: PNG, JPG, JPEG

**Solution:** Convert to supported format before upload.

---

## Retry Strategy

Recommended exponential backoff:

```python
import time

def retry_with_backoff(func, max_retries=3):
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if "429" in str(e) or "500" in str(e):
                wait_time = 2 ** attempt  # 1, 2, 4 seconds
                time.sleep(wait_time)
                continue
            raise
    raise Exception("Max retries exceeded")
```

---

## Getting Help

1. Check [API Reference](api-reference.md)
2. Review [Setup Guide](setup-guide.md)
3. Check Google Cloud Status: https://status.cloud.google.com/
4. Contact Google Cloud Support

---

**Last Updated**: 2025-12-27
