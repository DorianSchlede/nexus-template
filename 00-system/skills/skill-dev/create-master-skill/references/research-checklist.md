# Master Skill Research Checklist

**Comprehensive research tasks before building any master skill.**

---

## Research Phase Overview

**Goal:** Gather ALL information needed to build a complete master skill.

**Time:** 30-60 minutes of focused research

**Output:** `02-resources/research.md` in the planning build

---

## Research Tasks

### 1. Official Documentation

**Search:** `"{integration} official documentation"`

**Capture:**
- [ ] Documentation URL
- [ ] API reference URL
- [ ] Getting started guide URL
- [ ] Changelog/updates URL

**Example:**
```markdown
## Official Documentation
- Main docs: https://developers.{integration}.com
- API reference: https://developers.{integration}.com/api
- Getting started: https://developers.{integration}.com/quickstart
```

---

### 2. Authentication & Authorization

**Search:** `"{integration} API authentication OAuth API key bearer token"`

**Capture:**
- [ ] Authentication method(s) supported
- [ ] How to obtain credentials
- [ ] Token format (API key, OAuth, JWT)
- [ ] Token refresh process (if OAuth)
- [ ] Required headers
- [ ] Scopes/permissions model

**Example:**
```markdown
## Authentication
- Method: API Key (Bearer token)
- Obtain: Settings → API → Generate key
- Header: `Authorization: Bearer {api_key}`
- Scopes: read, write, admin
```

---

### 3. API Endpoints & Operations

**Search:** `"{integration} API endpoints REST reference"`

**Capture:**
- [ ] Base URL
- [ ] API versioning scheme
- [ ] Key endpoints (list, get, create, update, delete)
- [ ] Request format (JSON, form-data)
- [ ] Response format
- [ ] Pagination pattern

**Example:**
```markdown
## API Endpoints
- Base URL: https://api.{integration}.com/v1
- Versioning: URL path (/v1, /v2)
- Format: JSON request/response

### Key Endpoints
| Operation | Method | Endpoint |
|-----------|--------|----------|
| List | GET | /resources |
| Get | GET | /resources/{id} |
| Create | POST | /resources |
| Update | PATCH | /resources/{id} |
| Delete | DELETE | /resources/{id} |
```

---

### 4. Data Models & Schemas

**Search:** `"{integration} API data model schema properties"`

**Capture:**
- [ ] Core resource types
- [ ] Property/field types
- [ ] Required vs optional fields
- [ ] Nested object structures
- [ ] Relationships between resources

**Example:**
```markdown
## Data Models

### Resource
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| id | string | auto | Unique identifier |
| name | string | yes | Display name |
| status | enum | no | active, archived |
| created_at | datetime | auto | Creation timestamp |
```

---

### 5. Error Handling

**Search:** `"{integration} API error codes error handling troubleshooting"`

**Capture:**
- [ ] HTTP status codes used
- [ ] Error response format
- [ ] Common error codes
- [ ] Error messages
- [ ] Recommended handling

**Example:**
```markdown
## Error Handling

### Error Response Format
```json
{
  "error": {
    "code": "invalid_request",
    "message": "The request was invalid",
    "details": [...]
  }
}
```

### Common Errors
| Code | Status | Meaning | Solution |
|------|--------|---------|----------|
| 401 | Unauthorized | Bad API key | Check credentials |
| 429 | Too Many Requests | Rate limited | Implement backoff |
```

---

### 6. Rate Limits & Quotas

**Search:** `"{integration} API rate limits throttling quotas"`

**Capture:**
- [ ] Requests per second/minute
- [ ] Daily/monthly quotas
- [ ] Rate limit headers
- [ ] Backoff recommendations
- [ ] Tier differences (free vs paid)

**Example:**
```markdown
## Rate Limits
- Limit: 100 requests/minute
- Header: `X-RateLimit-Remaining`
- Backoff: Exponential (1s, 2s, 4s...)
- Tier: Free=100/min, Pro=1000/min
```

---

### 7. SDKs & Libraries

**Search:** `"{integration} Python SDK library pip"`

**Capture:**
- [ ] Official SDK availability
- [ ] Installation command
- [ ] Popular third-party libraries
- [ ] SDK vs REST API trade-offs

**Example:**
```markdown
## SDKs & Libraries

### Official SDK
```bash
pip install {integration}-sdk
```

### Usage
```python
from {integration} import Client
client = Client(api_key="...")
```

### Third-Party
- `{integration}-python` - Community maintained
```

---

### 8. Webhooks & Events (if applicable)

**Search:** `"{integration} webhooks events callbacks"`

**Capture:**
- [ ] Webhook support
- [ ] Event types
- [ ] Payload format
- [ ] Verification method
- [ ] Retry policy

**Example:**
```markdown
## Webhooks
- Supported: Yes
- Events: resource.created, resource.updated, resource.deleted
- Verification: HMAC signature in header
- Retries: 3 attempts with exponential backoff
```

---

### 9. File Handling (if applicable)

**Search:** `"{integration} API file upload download attachments"`

**Capture:**
- [ ] File upload method
- [ ] Supported file types
- [ ] Size limits
- [ ] URL expiration
- [ ] Multi-part upload

**Example:**
```markdown
## File Handling
- Upload: POST /files (multipart/form-data)
- Max size: 5MB
- Types: pdf, png, jpg, doc
- URLs expire: 1 hour
```

---

### 10. Best Practices & Patterns

**Search:** `"{integration} API best practices integration patterns"`

**Capture:**
- [ ] Recommended patterns
- [ ] Common anti-patterns
- [ ] Performance tips
- [ ] Security considerations

**Example:**
```markdown
## Best Practices
- Always use pagination for list endpoints
- Cache frequently accessed resources
- Handle rate limits gracefully
- Never expose API keys in client code
```

---

## Research Output Template

Save all findings to: `02-builds/{ID}-{integration}-master-skill/02-resources/research.md`

```markdown
# {Integration} API Research

**Researched:** {date}
**Purpose:** Foundation for {integration}-master skill

---

## 1. Official Documentation
{findings}

## 2. Authentication
{findings}

## 3. API Endpoints
{findings}

## 4. Data Models
{findings}

## 5. Error Handling
{findings}

## 6. Rate Limits
{findings}

## 7. SDKs & Libraries
{findings}

## 8. Webhooks (if applicable)
{findings}

## 9. File Handling (if applicable)
{findings}

## 10. Best Practices
{findings}

---

## Key Insights for Master Skill

### Recommended References
- setup-guide.md: {what to include}
- api-reference.md: {what to include}
- error-handling.md: {what to include}
- Additional: {domain-specific docs}

### Recommended Scripts
- check_config.py: {what to validate}
- discover_resources.py: {what to discover}
- Additional: {specific operations}

### Potential Child Skills
1. {skill-1}: {purpose}
2. {skill-2}: {purpose}
3. {skill-3}: {purpose}
```

---

## Research Quality Checklist

Before proceeding to architecture phase:

- [ ] All 10 research areas covered (or marked N/A)
- [ ] Official documentation links captured
- [ ] Authentication fully understood
- [ ] Key endpoints documented
- [ ] Error codes cataloged
- [ ] Rate limits known
- [ ] At least 3 potential child skills identified
- [ ] Research saved to build resources

---

**Last Updated:** 2025-12-11
