# Langfuse API Reference

Base URL: `{LANGFUSE_HOST}/api/public`

Authentication: Basic Auth (Public Key as username, Secret Key as password)

---

## Traces

### List Traces
```
GET /traces
```

Query Parameters:
- `page` (int): Page number
- `limit` (int): Items per page (max 100)
- `userId` (string): Filter by user ID
- `name` (string): Filter by trace name
- `sessionId` (string): Filter by session ID
- `fromTimestamp` (ISO8601): Start time filter
- `toTimestamp` (ISO8601): End time filter
- `orderBy` (string): Sort field
- `order` (string): "asc" or "desc"

### Get Trace
```
GET /traces/{traceId}
```

---

## Observations

### List Observations (v2)
```
GET /v2/observations
```

Query Parameters:
- `cursor` (string): Pagination cursor
- `limit` (int): Items per page
- `traceId` (string): Filter by trace
- `type` (string): "SPAN", "GENERATION", or "EVENT"
- `name` (string): Filter by name
- `fromStartTime` (ISO8601): Start time filter
- `toStartTime` (ISO8601): End time filter

### Get Observation
```
GET /observations/{observationId}
```

---

## Sessions

### List Sessions
```
GET /sessions
```

Query Parameters:
- `page` (int): Page number
- `limit` (int): Items per page
- `fromTimestamp` (ISO8601): Start time filter
- `toTimestamp` (ISO8601): End time filter

### Get Session
```
GET /sessions/{sessionId}
```

Returns session with associated traces.

---

## Scores

### List Scores (v2)
```
GET /v2/scores
```

Query Parameters:
- `cursor` (string): Pagination cursor
- `limit` (int): Items per page
- `traceId` (string): Filter by trace
- `observationId` (string): Filter by observation
- `name` (string): Filter by score name
- `source` (string): "API", "EVAL", or "ANNOTATION"

### Get Score
```
GET /v2/scores/{scoreId}
```

---

## Models

### List Models
```
GET /models
```

Query Parameters:
- `page` (int): Page number
- `limit` (int): Items per page

### Get Model
```
GET /models/{id}
```

---

## Projects

### Get Project
```
GET /projects
```

Returns the project associated with the API key.

---

## Common Response Patterns

### Pagination (Page-based)
```json
{
  "data": [...],
  "meta": {
    "page": 1,
    "limit": 50,
    "totalItems": 150,
    "totalPages": 3
  }
}
```

### Pagination (Cursor-based)
```json
{
  "data": [...],
  "meta": {
    "nextCursor": "abc123",
    "hasMore": true
  }
}
```

### Error Response
```json
{
  "error": "Not Found",
  "message": "Trace with ID xyz not found"
}
```

---

## Rate Limits

- Standard: 1000 requests/minute
- Self-hosted: Configurable

---

Full API Reference: https://api.reference.langfuse.com/
