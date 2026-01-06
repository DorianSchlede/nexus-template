# NotebookLM Enterprise Authentication

OAuth 2.0 authentication via Google Cloud SDK (gcloud).

---

## Overview

NotebookLM Enterprise uses Google Cloud OAuth 2.0 for authentication. The gcloud CLI handles token management automatically.

---

## Authentication Flow

```
┌─────────────────────────────────────────────────────────┐
│  1. User runs: gcloud auth login                        │
│     ↓                                                   │
│  2. Browser opens for Google sign-in                    │
│     ↓                                                   │
│  3. gcloud stores credentials locally                   │
│     ↓                                                   │
│  4. Scripts call: gcloud auth print-access-token        │
│     ↓                                                   │
│  5. Token used in Authorization header                  │
└─────────────────────────────────────────────────────────┘
```

---

## Initial Setup

### 1. Install gcloud CLI

```bash
# macOS
brew install --cask google-cloud-sdk

# Windows: Download from
# https://cloud.google.com/sdk/docs/install#windows

# Linux
curl https://sdk.cloud.google.com | bash
```

### 2. Authenticate

```bash
# Interactive browser login
gcloud auth login

# For service accounts or CI/CD
gcloud auth application-default login
```

### 3. Set Project

```bash
gcloud config set project YOUR_PROJECT_ID
```

---

## Token Management

### Get Access Token

```bash
gcloud auth print-access-token
```

Returns a token valid for ~1 hour.

### Use in API Requests

```bash
curl -X GET \
  -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  -H "Content-Type: application/json" \
  "https://global-discoveryengine.googleapis.com/v1alpha/..."
```

### Python Integration

```python
import subprocess

def get_access_token():
    result = subprocess.run(
        ['gcloud', 'auth', 'print-access-token'],
        capture_output=True,
        text=True,
        check=True
    )
    return result.stdout.strip()

headers = {
    "Authorization": f"Bearer {get_access_token()}",
    "Content-Type": "application/json"
}
```

---

## Token Refresh

gcloud automatically refreshes tokens when they expire. If you get a 401 error:

1. Token may have just expired - retry the request
2. Re-authenticate: `gcloud auth login`
3. Check credentials: `gcloud auth list`

---

## Required IAM Roles

Users need these roles for NotebookLM operations:

| Role | Permissions |
|------|-------------|
| `roles/discoveryengine.notebooklmUser` | Create, read, update notebooks |
| `roles/discoveryengine.notebooklmAdmin` | Share notebooks, manage access |

### Grant Roles

```bash
gcloud projects add-iam-policy-binding PROJECT_ID \
  --member="user:email@example.com" \
  --role="roles/discoveryengine.notebooklmUser"
```

---

## Service Account Authentication

For automated/CI workflows:

### 1. Create Service Account

```bash
gcloud iam service-accounts create notebooklm-sa \
  --display-name="NotebookLM Service Account"
```

### 2. Grant Roles

```bash
gcloud projects add-iam-policy-binding PROJECT_ID \
  --member="serviceAccount:notebooklm-sa@PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/discoveryengine.notebooklmUser"
```

### 3. Create Key

```bash
gcloud iam service-accounts keys create key.json \
  --iam-account=notebooklm-sa@PROJECT_ID.iam.gserviceaccount.com
```

### 4. Authenticate

```bash
gcloud auth activate-service-account --key-file=key.json
```

---

## Security Best Practices

1. **Never commit tokens** - Always generate at runtime
2. **Use short-lived tokens** - gcloud tokens expire after ~1 hour
3. **Rotate service account keys** - Regularly regenerate keys
4. **Principle of least privilege** - Grant only needed roles
5. **Audit access** - Check Cloud Audit Logs

---

## Troubleshooting

### "Token expired"

```bash
gcloud auth login  # Re-authenticate
```

### "Permission denied"

```bash
# Check current identity
gcloud auth list

# Check roles
gcloud projects get-iam-policy PROJECT_ID
```

### "gcloud not found"

Install Google Cloud SDK from https://cloud.google.com/sdk/docs/install

---

**Last Updated**: 2025-12-27
