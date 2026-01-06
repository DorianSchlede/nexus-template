# Beam Authentication Guide

Detailed authentication flow for Beam AI API.

---

## Overview

Beam uses a **two-step authentication** process:

1. **Exchange** your API key for an access token
2. **Use** the access token in subsequent requests

Access tokens expire after **1 hour**. Use refresh tokens to get new access tokens without re-authenticating.

---

## Step 1: Get Access Token

Exchange your API key for an access token:

```bash
curl -X POST https://api.beamstudio.ai/auth/access-token \
  -H "Content-Type: application/json" \
  -d '{"apiKey": "bm_key_your_api_key"}'
```

**Response:**
```json
{
  "idToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Python:**
```python
import requests

response = requests.post(
    'https://api.beamstudio.ai/auth/access-token',
    json={'apiKey': 'bm_key_your_api_key'}
)

tokens = response.json()
access_token = tokens['idToken']
refresh_token = tokens['refreshToken']
```

---

## Step 2: Use Access Token

Include the access token and workspace ID in all API requests:

```bash
curl https://api.beamstudio.ai/agent \
  -H "Authorization: Bearer {access_token}" \
  -H "current-workspace-id: {workspace_id}"
```

**Required Headers:**

| Header | Value | Description |
|--------|-------|-------------|
| `Authorization` | `Bearer {idToken}` | Access token from auth |
| `current-workspace-id` | `{workspace-uuid}` | Your workspace ID |
| `Content-Type` | `application/json` | For POST/PATCH requests |

**Python:**
```python
headers = {
    'Authorization': f'Bearer {access_token}',
    'current-workspace-id': 'your-workspace-id',
    'Content-Type': 'application/json'
}

response = requests.get(
    'https://api.beamstudio.ai/agent',
    headers=headers
)
```

---

## Step 3: Refresh Token

When access token expires (after 1 hour), use refresh token:

```bash
curl -X POST https://api.beamstudio.ai/auth/refresh-token \
  -H "Content-Type: application/json" \
  -d '{"refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."}'
```

**Response:**
```json
{
  "idToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Python:**
```python
def refresh_access_token(refresh_token):
    response = requests.post(
        'https://api.beamstudio.ai/auth/refresh-token',
        json={'refreshToken': refresh_token}
    )
    return response.json()
```

---

## Token Management Pattern

Recommended pattern for managing tokens:

```python
import os
import time
import requests

class BeamAuth:
    def __init__(self):
        self.api_key = os.getenv('BEAM_API_KEY')
        self.workspace_id = os.getenv('BEAM_WORKSPACE_ID')
        self.access_token = None
        self.refresh_token = None
        self.token_expiry = 0

    def get_access_token(self):
        """Get valid access token, refreshing if needed"""
        # Check if token needs refresh (with 5 min buffer)
        if time.time() > self.token_expiry - 300:
            self._refresh_or_authenticate()
        return self.access_token

    def _refresh_or_authenticate(self):
        """Refresh token or re-authenticate"""
        if self.refresh_token:
            try:
                self._refresh_token()
                return
            except:
                pass  # Fall through to re-authenticate

        self._authenticate()

    def _authenticate(self):
        """Authenticate with API key"""
        response = requests.post(
            'https://api.beamstudio.ai/auth/access-token',
            json={'apiKey': self.api_key}
        )
        response.raise_for_status()
        tokens = response.json()
        self.access_token = tokens['idToken']
        self.refresh_token = tokens['refreshToken']
        self.token_expiry = time.time() + 3600  # 1 hour

    def _refresh_token(self):
        """Refresh access token"""
        response = requests.post(
            'https://api.beamstudio.ai/auth/refresh-token',
            json={'refreshToken': self.refresh_token}
        )
        response.raise_for_status()
        tokens = response.json()
        self.access_token = tokens['idToken']
        self.refresh_token = tokens['refreshToken']
        self.token_expiry = time.time() + 3600

    def get_headers(self):
        """Get headers for API request"""
        return {
            'Authorization': f'Bearer {self.get_access_token()}',
            'current-workspace-id': self.workspace_id,
            'Content-Type': 'application/json'
        }

# Usage
auth = BeamAuth()
headers = auth.get_headers()
response = requests.get('https://api.beamstudio.ai/agent', headers=headers)
```

---

## Security Best Practices

1. **Never expose API keys** in client-side code
2. **Store securely** - Use environment variables, not hardcoded
3. **Rotate keys** periodically
4. **Use minimal permissions** - Create keys with only needed scopes
5. **Monitor usage** - Track API key usage for anomalies

---

## Common Issues

### Invalid Token

**Error:** `401 Unauthorized`

**Causes:**
- Token expired
- Token corrupted
- Wrong token type used

**Solution:** Re-authenticate or refresh token

### Missing Workspace Header

**Error:** `400 Bad Request - Workspace ID required`

**Solution:** Include `current-workspace-id` header

### API Key Revoked

**Error:** `401 Unauthorized - Invalid API key`

**Solution:** Generate new API key in Beam settings
