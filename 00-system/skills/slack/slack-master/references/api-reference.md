# Slack API Reference

Quick reference for Slack Web API methods used by Nexus skills.

---

## Base URL

```
https://slack.com/api/
```

All methods are called as POST requests with JSON body or GET with query params.

---

## Authentication

All requests require Bearer token in header:

```http
Authorization: Bearer xoxp-your-user-token
Content-Type: application/json
```

---

## Rate Limits

Slack uses tiered rate limits:
- **Tier 1**: 1+ requests per minute (rare methods)
- **Tier 2**: 20+ requests per minute (most methods)
- **Tier 3**: 50+ requests per minute (common methods)
- **Tier 4**: 100+ requests per minute (very common)

When rate limited, response includes:
```json
{
  "ok": false,
  "error": "rate_limited",
  "retry_after": 30
}
```

---

## Response Format

All responses are JSON with `ok` boolean:

**Success:**
```json
{
  "ok": true,
  "channel": "C123456",
  "ts": "1234567890.123456"
}
```

**Error:**
```json
{
  "ok": false,
  "error": "channel_not_found"
}
```

---

## Messaging Methods

### chat.postMessage

Send a message to a channel.

**Endpoint**: `POST /chat.postMessage`

**Parameters:**
| Param | Type | Required | Description |
|-------|------|----------|-------------|
| channel | string | Yes | Channel ID or name |
| text | string | Yes* | Message text |
| blocks | array | No | Block Kit blocks |
| thread_ts | string | No | Reply to thread |
| reply_broadcast | bool | No | Also post to channel |
| unfurl_links | bool | No | Unfurl URLs |
| unfurl_media | bool | No | Unfurl media |

**Example:**
```json
{
  "channel": "C1234567890",
  "text": "Hello, world!",
  "thread_ts": "1234567890.123456"
}
```

**Response:**
```json
{
  "ok": true,
  "channel": "C1234567890",
  "ts": "1503435956.000247",
  "message": {
    "text": "Hello, world!",
    "user": "U1234567890",
    "ts": "1503435956.000247"
  }
}
```

---

### chat.update

Update an existing message.

**Endpoint**: `POST /chat.update`

**Parameters:**
| Param | Type | Required | Description |
|-------|------|----------|-------------|
| channel | string | Yes | Channel ID |
| ts | string | Yes | Timestamp of message |
| text | string | Yes* | New text |
| blocks | array | No | New blocks |

---

### chat.delete

Delete a message.

**Endpoint**: `POST /chat.delete`

**Parameters:**
| Param | Type | Required | Description |
|-------|------|----------|-------------|
| channel | string | Yes | Channel ID |
| ts | string | Yes | Timestamp of message |

---

### chat.scheduleMessage

Schedule a message for later.

**Endpoint**: `POST /chat.scheduleMessage`

**Parameters:**
| Param | Type | Required | Description |
|-------|------|----------|-------------|
| channel | string | Yes | Channel ID |
| text | string | Yes | Message text |
| post_at | integer | Yes | Unix timestamp to send |

---

## Conversation Methods

### conversations.list

List all channels user can see.

**Endpoint**: `GET /conversations.list`

**Parameters:**
| Param | Type | Required | Description |
|-------|------|----------|-------------|
| types | string | No | Comma-separated: public_channel, private_channel, mpim, im |
| limit | integer | No | Max results (default 100, max 1000) |
| cursor | string | No | Pagination cursor |
| exclude_archived | bool | No | Exclude archived channels |

**Response:**
```json
{
  "ok": true,
  "channels": [
    {
      "id": "C1234567890",
      "name": "general",
      "is_channel": true,
      "is_private": false,
      "is_member": true,
      "num_members": 42
    }
  ],
  "response_metadata": {
    "next_cursor": "dGVhbTpDMDYxRkE1UEI="
  }
}
```

---

### conversations.info

Get info about a channel.

**Endpoint**: `GET /conversations.info`

**Parameters:**
| Param | Type | Required | Description |
|-------|------|----------|-------------|
| channel | string | Yes | Channel ID |
| include_num_members | bool | No | Include member count |

---

### conversations.history

Get messages from a channel.

**Endpoint**: `GET /conversations.history`

**Parameters:**
| Param | Type | Required | Description |
|-------|------|----------|-------------|
| channel | string | Yes | Channel ID |
| limit | integer | No | Max messages (default 100) |
| oldest | string | No | Start of time range (ts) |
| latest | string | No | End of time range (ts) |
| cursor | string | No | Pagination cursor |
| inclusive | bool | No | Include oldest/latest messages |

---

### conversations.create

Create a new channel.

**Endpoint**: `POST /conversations.create`

**Parameters:**
| Param | Type | Required | Description |
|-------|------|----------|-------------|
| name | string | Yes | Channel name |
| is_private | bool | No | Create private channel |

---

### conversations.invite

Invite users to a channel.

**Endpoint**: `POST /conversations.invite`

**Parameters:**
| Param | Type | Required | Description |
|-------|------|----------|-------------|
| channel | string | Yes | Channel ID |
| users | string | Yes | Comma-separated user IDs |

---

### conversations.join

Join a public channel.

**Endpoint**: `POST /conversations.join`

**Parameters:**
| Param | Type | Required | Description |
|-------|------|----------|-------------|
| channel | string | Yes | Channel ID |

---

### conversations.leave

Leave a channel.

**Endpoint**: `POST /conversations.leave`

**Parameters:**
| Param | Type | Required | Description |
|-------|------|----------|-------------|
| channel | string | Yes | Channel ID |

---

## User Methods

### users.list

List all users in workspace.

**Endpoint**: `GET /users.list`

**Parameters:**
| Param | Type | Required | Description |
|-------|------|----------|-------------|
| limit | integer | No | Max results |
| cursor | string | No | Pagination cursor |

**Response:**
```json
{
  "ok": true,
  "members": [
    {
      "id": "U1234567890",
      "name": "johndoe",
      "real_name": "John Doe",
      "profile": {
        "email": "john@example.com",
        "display_name": "John"
      },
      "is_admin": false,
      "is_bot": false
    }
  ]
}
```

---

### users.info

Get info about a user.

**Endpoint**: `GET /users.info`

**Parameters:**
| Param | Type | Required | Description |
|-------|------|----------|-------------|
| user | string | Yes | User ID |

---

### users.profile.get

Get a user's profile.

**Endpoint**: `GET /users.profile.get`

**Parameters:**
| Param | Type | Required | Description |
|-------|------|----------|-------------|
| user | string | No | User ID (default: current user) |

---

### users.profile.set

Set your profile fields.

**Endpoint**: `POST /users.profile.set`

**Parameters:**
| Param | Type | Required | Description |
|-------|------|----------|-------------|
| profile | object | Yes | Profile fields to update |

---

## File Methods

### files.upload

Upload a file.

**Endpoint**: `POST /files.upload`

**Note**: Uses multipart/form-data, not JSON.

**Parameters:**
| Param | Type | Required | Description |
|-------|------|----------|-------------|
| file | file | Yes* | File to upload |
| content | string | Yes* | File content (text) |
| channels | string | No | Comma-separated channel IDs |
| filename | string | No | Filename |
| title | string | No | Title |
| initial_comment | string | No | Message with file |

---

### files.list

List files.

**Endpoint**: `GET /files.list`

**Parameters:**
| Param | Type | Required | Description |
|-------|------|----------|-------------|
| channel | string | No | Filter by channel |
| user | string | No | Filter by user |
| types | string | No | Filter by type |
| count | integer | No | Number of results |

---

### files.info

Get file info.

**Endpoint**: `GET /files.info`

**Parameters:**
| Param | Type | Required | Description |
|-------|------|----------|-------------|
| file | string | Yes | File ID |

---

### files.delete

Delete a file.

**Endpoint**: `POST /files.delete`

**Parameters:**
| Param | Type | Required | Description |
|-------|------|----------|-------------|
| file | string | Yes | File ID |

---

## Reaction Methods

### reactions.add

Add a reaction to a message.

**Endpoint**: `POST /reactions.add`

**Parameters:**
| Param | Type | Required | Description |
|-------|------|----------|-------------|
| channel | string | Yes | Channel ID |
| timestamp | string | Yes | Message timestamp |
| name | string | Yes | Emoji name (without colons) |

---

### reactions.remove

Remove a reaction.

**Endpoint**: `POST /reactions.remove`

**Parameters:**
| Param | Type | Required | Description |
|-------|------|----------|-------------|
| channel | string | Yes | Channel ID |
| timestamp | string | Yes | Message timestamp |
| name | string | Yes | Emoji name |

---

### reactions.get

Get reactions for a message.

**Endpoint**: `GET /reactions.get`

**Parameters:**
| Param | Type | Required | Description |
|-------|------|----------|-------------|
| channel | string | Yes | Channel ID |
| timestamp | string | Yes | Message timestamp |

---

## Search Methods

### search.messages

Search messages.

**Endpoint**: `GET /search.messages`

**Parameters:**
| Param | Type | Required | Description |
|-------|------|----------|-------------|
| query | string | Yes | Search query |
| count | integer | No | Results per page (default 20) |
| page | integer | No | Page number |
| sort | string | No | Sort: score or timestamp |
| sort_dir | string | No | Sort direction: asc or desc |

**Search Modifiers:**
- `from:@user` - From specific user
- `in:#channel` - In specific channel
- `before:2024-01-01` - Before date
- `after:2024-01-01` - After date
- `has:link` - Contains links
- `has:reaction` - Has reactions

---

### search.files

Search files.

**Endpoint**: `GET /search.files`

**Parameters:**
| Param | Type | Required | Description |
|-------|------|----------|-------------|
| query | string | Yes | Search query |
| count | integer | No | Results per page |
| page | integer | No | Page number |

---

## Pin Methods

### pins.add

Pin a message.

**Endpoint**: `POST /pins.add`

**Parameters:**
| Param | Type | Required | Description |
|-------|------|----------|-------------|
| channel | string | Yes | Channel ID |
| timestamp | string | Yes | Message timestamp |

---

### pins.remove

Remove a pin.

**Endpoint**: `POST /pins.remove`

**Parameters:**
| Param | Type | Required | Description |
|-------|------|----------|-------------|
| channel | string | Yes | Channel ID |
| timestamp | string | Yes | Message timestamp |

---

### pins.list

List pinned items.

**Endpoint**: `GET /pins.list`

**Parameters:**
| Param | Type | Required | Description |
|-------|------|----------|-------------|
| channel | string | Yes | Channel ID |

---

## Reminder Methods

### reminders.add

Create a reminder.

**Endpoint**: `POST /reminders.add`

**Parameters:**
| Param | Type | Required | Description |
|-------|------|----------|-------------|
| text | string | Yes | Reminder text |
| time | string | Yes | When to remind (Unix ts or natural language) |
| user | string | No | User to remind (default: yourself) |

---

### reminders.list

List reminders.

**Endpoint**: `GET /reminders.list`

---

### reminders.delete

Delete a reminder.

**Endpoint**: `POST /reminders.delete`

**Parameters:**
| Param | Type | Required | Description |
|-------|------|----------|-------------|
| reminder | string | Yes | Reminder ID |

---

## Common Error Codes

| Error | Description |
|-------|-------------|
| `not_authed` | No authentication token |
| `invalid_auth` | Invalid token |
| `account_inactive` | Account deactivated |
| `token_revoked` | Token has been revoked |
| `no_permission` | Token lacks required scope |
| `missing_scope` | Specific scope missing |
| `channel_not_found` | Channel doesn't exist or no access |
| `user_not_found` | User doesn't exist |
| `message_not_found` | Message doesn't exist |
| `cant_delete_message` | Can't delete (not yours or too old) |
| `rate_limited` | Too many requests |
| `fatal_error` | Server error |

---

## References

- [Slack API Methods](https://api.slack.com/methods)
- [Block Kit Builder](https://app.slack.com/block-kit-builder)
- [Rate Limits](https://api.slack.com/docs/rate-limits)
