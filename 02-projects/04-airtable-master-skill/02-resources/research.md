# Airtable API Research

**Researched:** 2025-12-11
**Purpose:** Foundation for airtable-master skill

---

## 1. Official Documentation

- **Main Docs:** https://airtable.com/developers/web/api/introduction
- **API Reference:** https://airtable.com/developers/web/api
- **Interactive Docs:** https://airtable.com/api (base-specific)
- **Getting Started:** https://support.airtable.com/docs/getting-started-with-airtables-web-api
- **Enterprise API:** https://support.airtable.com/docs/airtable-enterprise-api

---

## 2. Authentication

### Personal Access Tokens (PATs) - Primary Method
- **API keys deprecated:** February 1, 2024
- **PATs are the new standard** for individual use
- **OAuth** for third-party integrations

### Creating a PAT
1. Open developer hub: https://airtable.com/create/tokens
2. Click "Personal access tokens"
3. Click "Create token"
4. Name your token
5. Add scopes (read, write, etc.)
6. Select access level (single base, workspace, all)

### Token Format
```
pat.xxxxxxxxxxxxxxxx.xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### Scopes Available
- `data.records:read` - Read records
- `data.records:write` - Create/update/delete records
- `data.recordComments:read` - Read comments
- `data.recordComments:write` - Create comments
- `schema.bases:read` - Read base schema
- `schema.bases:write` - Modify base schema
- `webhook:manage` - Manage webhooks

### Header Format
```
Authorization: Bearer pat.xxxxx...
```

---

## 3. API Endpoints

### Base URL
```
https://api.airtable.com/v0
```

### Required Headers
```
Authorization: Bearer {access_token}
Content-Type: application/json
```

### Key Endpoints

| Operation | Method | Endpoint |
|-----------|--------|----------|
| List bases | GET | `/meta/bases` |
| Get base schema | GET | `/meta/bases/{baseId}/tables` |
| List records | GET | `/{baseId}/{tableIdOrName}` |
| Get record | GET | `/{baseId}/{tableIdOrName}/{recordId}` |
| Create records | POST | `/{baseId}/{tableIdOrName}` |
| Update records | PATCH/PUT | `/{baseId}/{tableIdOrName}` |
| Delete records | DELETE | `/{baseId}/{tableIdOrName}` |
| Create table | POST | `/meta/bases/{baseId}/tables` |
| Create field | POST | `/meta/bases/{baseId}/tables/{tableId}/fields` |

### Pagination
- Returns up to 100 records per request
- Use `offset` parameter for pagination
- Response includes `offset` if more records exist

### Bulk Operations
- Create/Update/Delete: Up to 10 records per request
- Formula: `records` array in request body

---

## 4. Data Models (Field Types)

### Text Fields
- `singleLineText` - Single line text
- `multilineText` - Long text (rich text)
- `richText` - Formatted text

### Number Fields
- `number` - Integer or decimal
- `currency` - Money values
- `percent` - Percentage
- `duration` - Time duration
- `rating` - Star rating (1-10)

### Selection Fields
- `singleSelect` - Single choice
- `multipleSelects` - Multiple choices
- `checkbox` - Boolean

### Date/Time Fields
- `date` - Date only
- `dateTime` - Date and time
- `createdTime` - Auto created timestamp
- `lastModifiedTime` - Auto modified timestamp

### Relationship Fields
- `multipleRecordLinks` - Links to other records
- `lookup` - Lookup from linked records
- `rollup` - Aggregation from linked records
- `count` - Count of linked records

### Special Fields
- `multipleAttachments` - File attachments
- `autoNumber` - Auto-incrementing number
- `barcode` - Barcode/QR code
- `button` - Action button
- `formula` - Calculated field
- `createdBy` - Auto creator user
- `lastModifiedBy` - Auto modifier user

### User Fields
- `singleCollaborator` - Single user
- `multipleCollaborators` - Multiple users

### Read-Only via API
- `formula`
- `rollup`
- `lookup`
- `count`
- `createdTime`
- `lastModifiedTime`
- `createdBy`
- `lastModifiedBy`
- `autoNumber`

---

## 5. Error Handling

| Code | Name | Cause | Solution |
|------|------|-------|----------|
| 400 | Bad Request | Invalid request body/params | Check JSON format, field names |
| 401 | Unauthorized | Invalid/expired token | Check PAT, regenerate if needed |
| 403 | Forbidden | No permission | Check scopes, base access |
| 404 | Not Found | Resource doesn't exist | Verify base/table/record ID |
| 413 | Payload Too Large | Request too big | Reduce batch size |
| 422 | Unprocessable | Validation error | Check field types, required fields |
| 429 | Too Many Requests | Rate limited | Wait 30s, implement backoff |
| 500 | Server Error | Airtable issue | Retry after delay |
| 503 | Service Unavailable | Maintenance | Retry after Retry-After header |

### Error Response Format
```json
{
  "error": {
    "type": "INVALID_REQUEST_BODY",
    "message": "Could not parse request body"
  }
}
```

---

## 6. Rate Limits

### Per-Base Limit
- **5 requests per second** per base
- Same across all pricing tiers
- Cannot be increased

### Per-Token Limit
- **50 requests per second** for all traffic using a PAT

### Monthly API Call Limits (per workspace)
| Plan | Monthly Limit | When Exceeded |
|------|---------------|---------------|
| Free | 1,000 | Blocked (since Dec 2024) |
| Team | 100,000 | Throttled to 2 req/s |
| Business | Unlimited | N/A |
| Enterprise | Unlimited | N/A |

### When Rate Limited (429)
- Wait 30 seconds before retry
- Check `Retry-After` header
- Implement exponential backoff

### Batching Strategy
- Up to 10 records per create/update/delete
- Effectively 50 records/second with batching

---

## 7. SDKs & Libraries

### Official JavaScript SDK
```bash
npm install airtable
```

### Python - pyairtable (Recommended)
```bash
pip install pyairtable
```

**Basic Usage:**
```python
from pyairtable import Api

api = Api(os.environ['AIRTABLE_API_KEY'])
table = api.table('appXXX', 'tblXXX')

# List records
records = table.all()

# Create record
table.create({"Name": "New Record"})

# Update record
table.update('recXXX', {"Name": "Updated"})

# Delete record
table.delete('recXXX')
```

### Alternative Python Libraries
- `airtable-python-wrapper` (now pyairtable)
- `airtable` (older, less maintained)

---

## 8. Webhooks

### Incoming Webhooks (Automation Trigger)
- Create unique URL for external services
- Trigger automations from external events
- No code required

### Webhooks API
- Subscribe to data/metadata changes
- Receive HTTP POST notifications
- Must save secret for payload validation

### Webhook Events
- Record created
- Record updated
- Record deleted
- Field created/updated
- Table created/updated

### Payload Validation
- Secret returned when webhook created
- Must validate payloads with secret
- Persist cursor to avoid duplicate processing

---

## 9. Best Practices

### Performance
- Use batch operations (10 records max)
- Implement caching for read-heavy workloads
- Use views to filter at API level
- Request only needed fields with `fields` param

### Error Handling
- Always check response status codes
- Implement exponential backoff for 429/5xx
- Log errors with request details
- Graceful degradation on failures

### Security
- Never expose tokens in client code
- Use environment variables
- Rotate tokens periodically
- Use minimum required scopes

### Pagination
- Always handle pagination for large tables
- Check for `offset` in response
- Loop until no offset returned

---

## 10. Key Insights for Master Skill

### Recommended References
- **setup-guide.md**: PAT creation, .env setup, scope selection
- **api-reference.md**: Base URL, endpoints, headers, pagination
- **error-handling.md**: Error codes, recovery patterns
- **field-types.md**: All field types with read/write formats (domain-specific)

### Recommended Scripts
- **check_airtable_config.py**: Validate PAT, test connection
- **discover_bases.py**: Find all accessible bases
- **discover_tables.py**: Get schema for a base
- **query_records.py**: List/filter records
- **manage_records.py**: CRUD operations

### Potential Child Skills
1. **airtable-connect** - Connect to any base, discover schema
2. **airtable-query** - Query records with filters
3. **airtable-sync** - Import/export records
4. **airtable-automate** - Webhook-based workflows

---

## Sources

- [Airtable Web API](https://airtable.com/developers/web/api/introduction)
- [Personal Access Tokens](https://airtable.com/developers/web/guides/personal-access-tokens)
- [Rate Limits](https://airtable.com/developers/web/api/rate-limits)
- [Field Types](https://airtable.com/developers/web/api/field-model)
- [Error Handling](https://airtable.com/developers/web/api/errors)
- [Webhooks Overview](https://airtable.com/developers/web/api/webhooks-overview)
- [pyairtable Documentation](https://pyairtable.readthedocs.io/)
