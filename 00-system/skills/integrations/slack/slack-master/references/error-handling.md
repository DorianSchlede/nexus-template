# Slack Error Handling

Guide for handling common Slack API errors in Nexus skills.

---

## Error Response Format

Slack API errors return JSON with `ok: false`:

```json
{
  "ok": false,
  "error": "error_code",
  "response_metadata": {
    "messages": ["Additional error context"]
  }
}
```

---

## Authentication Errors

### `not_authed`

**Cause**: No token provided in request.

**Fix**:
1. Check that `SLACK_USER_TOKEN` is in `.env`
2. Verify token is being loaded correctly
3. Re-run setup if needed: `python setup_slack.py`

---

### `invalid_auth`

**Cause**: Token is malformed or doesn't exist.

**Fix**:
1. Verify token starts with `xoxp-` (user token)
2. Check for typos in `.env`
3. Re-authenticate: `python setup_slack.py`

---

### `token_revoked`

**Cause**: User revoked app access or admin removed it.

**Fix**:
1. Re-authenticate: `python setup_slack.py`
2. User needs to re-authorize the app

---

### `account_inactive`

**Cause**: User account has been deactivated.

**Fix**:
1. Contact workspace admin
2. User needs to re-activate account

---

## Permission Errors

### `missing_scope`

**Cause**: Token doesn't have required OAuth scope.

**Example Response**:
```json
{
  "ok": false,
  "error": "missing_scope",
  "needed": "chat:write",
  "provided": "channels:read,users:read"
}
```

**Fix**:
1. Go to Slack App → OAuth & Permissions
2. Add the missing scope under **User Token Scopes**
3. Re-run OAuth flow to get new token with updated scopes

---

### `no_permission`

**Cause**: User doesn't have permission for this action (workspace-level).

**Fix**:
1. Check workspace permissions
2. May need admin to grant access
3. Some actions restricted by workspace settings

---

### `not_allowed_token_type`

**Cause**: Using wrong token type (e.g., bot token for user-only endpoint).

**Fix**:
1. Ensure using user token (xoxp-)
2. Some methods require specific token types

---

## Channel Errors

### `channel_not_found`

**Cause**: Channel doesn't exist or user can't see it.

**Possible Causes**:
- Channel ID is wrong
- Channel was deleted
- Private channel user isn't member of
- Channel in different workspace

**Fix**:
1. Verify channel ID: use `conversations.list` to get valid IDs
2. Check if user is member of the channel
3. For private channels, user must be invited first

---

### `is_archived`

**Cause**: Trying to post to an archived channel.

**Fix**:
1. Unarchive the channel first
2. Use a different active channel

---

### `not_in_channel`

**Cause**: User must be in channel to perform action.

**Fix**:
1. Join the channel first: `conversations.join`
2. Or get invited to the channel

---

### `channel_is_archived`

**Cause**: Channel is archived, can't modify.

**Fix**:
1. Unarchive channel (admin action)
2. Or use different channel

---

## Message Errors

### `message_not_found`

**Cause**: Message with given timestamp doesn't exist.

**Possible Causes**:
- Wrong timestamp
- Message was deleted
- Wrong channel

**Fix**:
1. Verify message timestamp format (e.g., `1234567890.123456`)
2. Check correct channel ID

---

### `cant_delete_message`

**Cause**: Can't delete the message.

**Possible Causes**:
- Not your message
- Message too old (workspace setting)
- Workspace restricts message deletion

**Fix**:
1. Only message author can delete
2. Check workspace retention settings
3. Admins can delete any message

---

### `edit_window_closed`

**Cause**: Can't edit message, too much time passed.

**Possible Causes**:
- Workspace limits edit window
- Default: messages can't be edited after some time

**Fix**:
1. Post a new message instead
2. Use threads for corrections

---

## User Errors

### `user_not_found`

**Cause**: User ID doesn't exist.

**Fix**:
1. Verify user ID format (starts with `U`)
2. Use `users.list` to get valid user IDs
3. Check if user is in this workspace

---

### `users_list_not_supplied`

**Cause**: Missing required users parameter.

**Fix**: Provide user IDs in the request.

---

## File Errors

### `file_not_found`

**Cause**: File doesn't exist or was deleted.

**Fix**:
1. Verify file ID
2. File may have been deleted

---

### `file_deleted`

**Cause**: File has been deleted.

**Fix**: File no longer available.

---

### `file_uploads_disabled`

**Cause**: File uploads disabled in workspace.

**Fix**: Contact workspace admin.

---

## Rate Limiting

### `rate_limited`

**Cause**: Too many requests.

**Response includes**:
```json
{
  "ok": false,
  "error": "rate_limited",
  "retry_after": 30
}
```

**Also check header**: `Retry-After: 30`

**Fix**:
1. Wait the specified seconds
2. Implement exponential backoff
3. Reduce request frequency
4. Cache responses when possible

**Rate Limit Tiers**:
| Tier | Requests/min | Example Methods |
|------|--------------|-----------------|
| 1 | 1 | admin.* |
| 2 | 20 | Most methods |
| 3 | 50 | Common methods |
| 4 | 100 | High-frequency |

---

## Server Errors

### `internal_error`

**Cause**: Slack server error.

**Fix**:
1. Retry after a moment
2. Check [Slack Status](https://status.slack.com)

---

### `fatal_error`

**Cause**: Unrecoverable server error.

**Fix**:
1. Retry later
2. Check Slack Status

---

### `service_unavailable`

**Cause**: Slack temporarily unavailable.

**Fix**:
1. Retry with exponential backoff
2. Check Slack Status

---

## Handling Errors in Scripts

### Python Pattern

```python
from slack_client import get_client, SlackAPIError, explain_error

try:
    client = get_client()
    result = client.post('chat.postMessage', {
        'channel': 'C123',
        'text': 'Hello'
    })
except SlackAPIError as e:
    if e.error_code == 'channel_not_found':
        print(f"Channel doesn't exist or you don't have access")
    elif e.error_code == 'rate_limited':
        print(f"Rate limited, retry after {e.response_data.get('retry_after', 60)}s")
    elif e.error_code == 'missing_scope':
        print(f"Need scope: {e.response_data.get('needed')}")
    else:
        print(f"Error: {explain_error(e.error_code)}")
```

### JSON Output for AI

When errors occur, format for AI consumption:

```json
{
  "success": false,
  "error": {
    "code": "channel_not_found",
    "message": "Channel does not exist or you lack access",
    "method": "chat.postMessage",
    "ai_action": "verify_channel_id",
    "suggestions": [
      "Use 'list channels' to see available channels",
      "Check if channel is private and you're a member",
      "Verify the channel ID format (should start with C)"
    ]
  }
}
```

---

## Retry Strategy

### Exponential Backoff

```python
import time
import random

def retry_with_backoff(func, max_retries=3):
    for attempt in range(max_retries):
        try:
            return func()
        except SlackAPIError as e:
            if e.error_code == 'rate_limited':
                wait = int(e.response_data.get('retry_after', 30))
            elif e.error_code in ['internal_error', 'service_unavailable']:
                wait = (2 ** attempt) + random.random()
            else:
                raise  # Don't retry other errors

            if attempt < max_retries - 1:
                time.sleep(wait)
            else:
                raise
```

### Which Errors to Retry

**Retry these**:
- `rate_limited`
- `internal_error`
- `service_unavailable`
- Network timeouts

**Don't retry these**:
- `invalid_auth`
- `missing_scope`
- `channel_not_found`
- `user_not_found`
- Most `4xx` type errors

---

## Debugging Checklist

1. **Check config**: `python check_slack_config.py --json`
2. **Verify token type**: Should be `xoxp-` for user operations
3. **Check scopes**: Look at `x-oauth-scopes` response header
4. **Validate IDs**: Channels start with `C`, users with `U`
5. **Check permissions**: User must have access to channel
6. **Review rate limits**: Implement backoff if needed
