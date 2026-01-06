# Slack Authentication

User OAuth authentication flow for Slack integration.

---

## Overview

This integration uses **User OAuth 2.0** to authenticate individual users:

- Each user authorizes with their own Slack account
- Messages appear as the actual user (not a bot)
- Access limited to what the user can see
- Token type: `xoxp-` (user token)

---

## Token Types

### User Token (xoxp-)

**Used by this integration.**

```
xoxp-XXXXXXXXXX-XXXXXXXXXX-XXXXXXXXXX-XXXXXXXXXXXX
```

**Characteristics**:
- Acts as the user who authorized
- Messages show as from that user
- Only sees channels/DMs user has access to
- Scopes prefixed with nothing (e.g., `channels:read`)

### Bot Token (xoxb-)

**Not used by this integration.**

```
xoxb-XXXXXXXXXX-XXXXXXXXXX-XXXXXXXXXXXX
```

**Characteristics**:
- Acts as the app/bot
- Messages show as from the bot
- Needs to be invited to channels
- Has different scope names

---

## OAuth 2.0 Flow

### 1. Authorization Request

User clicks authorization link:

```
https://slack.com/oauth/v2/authorize?
  client_id=YOUR_CLIENT_ID&
  user_scope=channels:read,chat:write&
  redirect_uri=https://localhost:8765/callback
```

**Key Parameter**: `user_scope` (not `scope`) for user tokens.

### 2. User Authorizes

- User sees permission screen in Slack
- Lists requested scopes
- User clicks "Allow"

### 3. Callback with Code

Slack redirects to your redirect URI:

```
https://localhost:8765/callback?code=TEMP_CODE
```

The code is valid for 10 minutes.

### 4. Exchange Code for Token

POST to token endpoint:

```http
POST https://slack.com/api/oauth.v2.access
Content-Type: application/x-www-form-urlencoded

client_id=YOUR_CLIENT_ID&
client_secret=YOUR_CLIENT_SECRET&
code=TEMP_CODE&
redirect_uri=https://localhost:8765/callback
```

### 5. Receive Token

Response contains user token in `authed_user`:

```json
{
  "ok": true,
  "app_id": "A123456",
  "authed_user": {
    "id": "U1234567",
    "scope": "channels:read,chat:write",
    "access_token": "xoxp-1234567890-...",
    "token_type": "user"
  },
  "team": {
    "id": "T123456",
    "name": "My Workspace"
  }
}
```

---

## Token Characteristics

### Token Lifetime

Slack user tokens **do not expire** automatically.

A token remains valid until:
- User revokes app access
- Admin removes app from workspace
- App is deleted
- Token is explicitly revoked via API

### No Refresh Tokens

Unlike many OAuth implementations:
- Slack doesn't provide refresh tokens for user tokens
- No need to implement token refresh
- Simply re-authorize if token becomes invalid

### Scope Additivity

When user re-authorizes with new scopes:
- New scopes are **added** to existing token
- Old scopes are not removed
- To remove scopes, must revoke and re-authorize

---

## Using the Token

### HTTP Header

All API requests include token in Authorization header:

```http
Authorization: Bearer xoxp-your-token-here
Content-Type: application/json
```

### Python Example

```python
import requests

token = "xoxp-..."
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

response = requests.post(
    "https://slack.com/api/chat.postMessage",
    headers=headers,
    json={"channel": "C123", "text": "Hello!"}
)
```

---

## Required Scopes

### Minimum (Basic Functionality)

```
channels:read     # List public channels
chat:write        # Send messages
users:read        # List users
```

### Recommended (Full Functionality)

```
# Channels
channels:read
channels:write
channels:history

# Private Channels
groups:read
groups:write
groups:history

# Direct Messages
im:read
im:write
im:history

# Group DMs
mpim:read
mpim:write
mpim:history

# Messaging
chat:write

# Users
users:read
users:read.email

# Files
files:read
files:write

# Reactions
reactions:read
reactions:write

# Pins
pins:read
pins:write

# Search
search:read

# Reminders
reminders:read
reminders:write

# Team Info
team:read
```

---

## Token Storage

### .env File

Store token in project's `.env`:

```bash
SLACK_USER_TOKEN=xoxp-1234567890-...
```

### Security Considerations

- Never commit `.env` to version control
- Add `.env` to `.gitignore`
- Each user should have their own token
- Tokens are tied to individual user accounts

---

## Token Validation

### Test Authentication

```http
POST https://slack.com/api/auth.test
Authorization: Bearer xoxp-...
```

**Success Response**:
```json
{
  "ok": true,
  "url": "https://myworkspace.slack.com/",
  "team": "My Workspace",
  "user": "username",
  "team_id": "T123456",
  "user_id": "U123456"
}
```

### Check Scopes

Scopes returned in response header:

```http
x-oauth-scopes: channels:read,chat:write,users:read
```

---

## Token Revocation

### By User

User can revoke via:
1. Slack App → Your Apps → Revoke
2. Or via workspace app management

### Via API

```http
POST https://slack.com/api/auth.revoke
Authorization: Bearer xoxp-...
```

After revocation, token is immediately invalid.

---

## Troubleshooting

### "invalid_auth"

Token is invalid. Causes:
- Token revoked
- Token copied incorrectly
- Token for different workspace

**Fix**: Re-authorize via setup wizard.

### "token_revoked"

User or admin revoked access.

**Fix**: User needs to re-authorize.

### "missing_scope"

Token lacks required scope.

**Fix**:
1. Add scope to app in Slack
2. Re-authorize to get new token with scope

### "not_allowed_token_type"

Using wrong token type for endpoint.

**Fix**: Ensure using user token (xoxp-) not bot token (xoxb-).

---

## Multi-User Setup

For teams where multiple users need Slack access:

### 1. Shared App Configuration

All users share:
- `SLACK_CLIENT_ID`
- `SLACK_CLIENT_SECRET`

### 2. Individual User Tokens

Each user runs setup and gets their own:
- `SLACK_USER_TOKEN`

### 3. Token Isolation

- Each user's token only accesses their data
- No cross-user data exposure
- Messages appear as the individual user

---

## Security Best Practices

1. **Minimal Scopes**: Only request scopes you need
2. **Secure Storage**: Keep tokens in `.env`, never in code
3. **User Education**: Users should understand what access they're granting
4. **Token Rotation**: Periodically re-authorize for security
5. **Audit Access**: Use `auth.test` to verify token validity
