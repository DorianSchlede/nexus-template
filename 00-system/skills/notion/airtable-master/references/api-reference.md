# Airtable API Reference

**Consolidated Airtable API documentation for Nexus integration.**

---

## Base Configuration

### API Base URL

```
https://api.airtable.com/v0
```

### Required Headers

```bash
Authorization: Bearer {personal_access_token}
Content-Type: application/json
```

### API Version

Current version: v0 (stable)

---

## Authentication

### Method: Personal Access Token (PAT)

PATs replaced API keys (deprecated Feb 2024). They provide granular scope control.

**Header format:**
```
Authorization: Bearer pat.xxxxxxxx...
```

**Example:**
```bash
curl -H "Authorization: Bearer pat.xxx..." https://api.airtable.com/v0/meta/whoami
```

---

## Metadata Endpoints

### Get Current User

```bash
GET https://api.airtable.com/v0/meta/whoami
```

**Response:**
```json
{
  "id": "usrxxxxxxxx",
  "email": "user@example.com",
  "scopes": ["data.records:read", "data.records:write", "schema.bases:read"]
}
```

### List Bases

```bash
GET https://api.airtable.com/v0/meta/bases
```

**Response:**
```json
{
  "bases": [
    {
      "id": "appxxxxxxxx",
      "name": "My Base",
      "permissionLevel": "create"
    }
  ]
}
```

### Get Base Schema

```bash
GET https://api.airtable.com/v0/meta/bases/{baseId}/tables
```

**Response:**
```json
{
  "tables": [
    {
      "id": "tblxxxxxxxx",
      "name": "Tasks",
      "primaryFieldId": "fldxxxxxxxx",
      "fields": [
        {"id": "fldxxxxxxxx", "name": "Name", "type": "singleLineText"},
        {"id": "fldxxxxxxxx", "name": "Status", "type": "singleSelect"}
      ],
      "views": [
        {"id": "viwxxxxxxxx", "name": "Grid view", "type": "grid"}
      ]
    }
  ]
}
```

---

## Record Endpoints

### List Records

```bash
GET https://api.airtable.com/v0/{baseId}/{tableIdOrName}
```

**Query Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `fields[]` | array | Only return specific fields |
| `filterByFormula` | string | Airtable formula filter |
| `maxRecords` | integer | Max records to return |
| `pageSize` | integer | Records per page (max 100) |
| `sort[0][field]` | string | Field to sort by |
| `sort[0][direction]` | string | `asc` or `desc` |
| `view` | string | View ID or name |
| `offset` | string | Pagination cursor |

**Example:**
```bash
curl "https://api.airtable.com/v0/appXXX/Tasks?maxRecords=10&view=Grid%20view" \
  -H "Authorization: Bearer pat.xxx..."
```

**Response:**
```json
{
  "records": [
    {
      "id": "recxxxxxxxx",
      "createdTime": "2025-01-15T10:30:00.000Z",
      "fields": {
        "Name": "Task 1",
        "Status": "In Progress"
      }
    }
  ],
  "offset": "itrxxxxxxxx/recxxxxxxxx"
}
```

### Get Record

```bash
GET https://api.airtable.com/v0/{baseId}/{tableIdOrName}/{recordId}
```

**Response:**
```json
{
  "id": "recxxxxxxxx",
  "createdTime": "2025-01-15T10:30:00.000Z",
  "fields": {
    "Name": "Task 1",
    "Status": "In Progress"
  }
}
```

### Create Records

```bash
POST https://api.airtable.com/v0/{baseId}/{tableIdOrName}
```

**Request body (single):**
```json
{
  "fields": {
    "Name": "New Task",
    "Status": "Todo"
  }
}
```

**Request body (batch - up to 10):**
```json
{
  "records": [
    {"fields": {"Name": "Task 1"}},
    {"fields": {"Name": "Task 2"}}
  ]
}
```

**With typecast (auto-convert values):**
```json
{
  "records": [...],
  "typecast": true
}
```

### Update Records

**PATCH** - Merge update (keeps unspecified fields)
```bash
PATCH https://api.airtable.com/v0/{baseId}/{tableIdOrName}
```

**PUT** - Replace (clears unspecified fields)
```bash
PUT https://api.airtable.com/v0/{baseId}/{tableIdOrName}
```

**Request body:**
```json
{
  "records": [
    {
      "id": "recxxxxxxxx",
      "fields": {"Status": "Done"}
    }
  ]
}
```

### Delete Records

```bash
DELETE https://api.airtable.com/v0/{baseId}/{tableIdOrName}?records[]=recXXX&records[]=recYYY
```

**Or in body:**
```json
{
  "records": ["recxxxxxxxx", "recyyyyyyyy"]
}
```

---

## Filtering with Formulas

### filterByFormula Parameter

Airtable uses its own formula syntax for filtering.

**Comparison:**
```
{Status} = "Done"
{Priority} > 3
{Name} != ""
```

**Logical:**
```
AND({Status} = "Done", {Priority} > 3)
OR({Status} = "Done", {Status} = "In Progress")
NOT({Archived})
```

**Text:**
```
FIND("search", {Name}) > 0
SEARCH("pattern", LOWER({Name})) > 0
```

**Date:**
```
IS_AFTER({Due Date}, TODAY())
IS_SAME({Created}, "2025-01-01", "day")
```

**URL encode the formula:**
```bash
curl "...?filterByFormula=AND(%7BStatus%7D%3D%22Done%22%2C%7BPriority%7D%3E3)"
```

---

## Pagination

### How It Works

- Max 100 records per request
- Response includes `offset` if more records exist
- Pass `offset` in next request to continue

### Example Pagination Loop

```python
records = []
offset = None

while True:
    params = {"pageSize": 100}
    if offset:
        params["offset"] = offset

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    records.extend(data.get("records", []))

    offset = data.get("offset")
    if not offset:
        break
```

---

## Rate Limits

| Limit Type | Value |
|------------|-------|
| Per-base | 5 requests/second |
| Per-token | 50 requests/second |
| Batch size | 10 records max |

**Rate limit headers:**
```
X-Airtable-Has-Unread-Notifications: true/false
```

**When rate limited (429):**
1. Wait 30 seconds
2. Use exponential backoff
3. Consider batching operations

---

## Batch Operations

### Benefits
- Up to 10 records per request
- Effectively 50 records/second

### Create Batch
```json
{
  "records": [
    {"fields": {"Name": "Record 1"}},
    {"fields": {"Name": "Record 2"}},
    // ... up to 10
  ]
}
```

### Update Batch
```json
{
  "records": [
    {"id": "rec1", "fields": {"Status": "Done"}},
    {"id": "rec2", "fields": {"Status": "Done"}},
    // ... up to 10
  ]
}
```

### Delete Batch
```
DELETE ...?records[]=rec1&records[]=rec2&...
```

---

## Common Patterns

### Pattern 1: Get All Records from Table

```python
def get_all_records(base_id, table_name):
    records = []
    offset = None

    while True:
        url = f"https://api.airtable.com/v0/{base_id}/{table_name}"
        params = {"pageSize": 100}
        if offset:
            params["offset"] = offset

        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        records.extend(data.get("records", []))

        offset = data.get("offset")
        if not offset:
            break

    return records
```

### Pattern 2: Upsert (Create or Update)

```python
def upsert_record(base_id, table_name, key_field, key_value, fields):
    # Find existing
    formula = f'{{{key_field}}} = "{key_value}"'
    existing = query_records(base_id, table_name, formula)

    if existing:
        # Update
        return update_record(base_id, table_name, existing[0]["id"], fields)
    else:
        # Create
        return create_record(base_id, table_name, fields)
```

---

## Official Documentation

- **API Reference:** https://airtable.com/developers/web/api
- **Authentication:** https://airtable.com/developers/web/api/authentication
- **Rate Limits:** https://airtable.com/developers/web/api/rate-limits
- **Field Model:** https://airtable.com/developers/web/api/field-model

---

**Last Updated:** 2025-12-11
