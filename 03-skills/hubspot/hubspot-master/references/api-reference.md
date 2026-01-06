# HubSpot API Reference

## Base URL

```
https://api.hubapi.com
```

---

## Authentication

All requests require Bearer token authentication:

```
Authorization: Bearer pat-na1-xxxxx
Content-Type: application/json
```

---

## CRM Objects

All CRM objects follow the same pattern:

```
/crm/v3/objects/{objectType}
```

### Supported Object Types
- `contacts`
- `companies`
- `deals`
- `emails`
- `calls`
- `notes`
- `meetings`

---

## Contacts

### List Contacts
```http
GET /crm/v3/objects/contacts
```

**Query Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `limit` | int | Max results (default 10, max 100) |
| `after` | string | Pagination cursor |
| `properties` | string | Comma-separated property names |

**Example:**
```bash
GET /crm/v3/objects/contacts?limit=50&properties=email,firstname,lastname
```

### Create Contact
```http
POST /crm/v3/objects/contacts
```

**Body:**
```json
{
  "properties": {
    "email": "john@example.com",
    "firstname": "John",
    "lastname": "Doe",
    "phone": "+1234567890"
  }
}
```

### Update Contact
```http
PATCH /crm/v3/objects/contacts/{contactId}
```

**Body:**
```json
{
  "properties": {
    "phone": "+0987654321"
  }
}
```

### Search Contacts
```http
POST /crm/v3/objects/contacts/search
```

**Body:**
```json
{
  "filterGroups": [
    {
      "filters": [
        {
          "propertyName": "email",
          "operator": "EQ",
          "value": "john@example.com"
        }
      ]
    }
  ],
  "properties": ["email", "firstname", "lastname"],
  "limit": 10
}
```

**Operators:** `EQ`, `NEQ`, `LT`, `LTE`, `GT`, `GTE`, `CONTAINS_TOKEN`, `NOT_CONTAINS_TOKEN`

---

## Companies

### List Companies
```http
GET /crm/v3/objects/companies?properties=name,domain,industry
```

### Create Company
```http
POST /crm/v3/objects/companies
```

**Body:**
```json
{
  "properties": {
    "name": "Acme Corp",
    "domain": "acme.com",
    "industry": "Technology"
  }
}
```

### Search Companies
```http
POST /crm/v3/objects/companies/search
```

---

## Deals

### List Deals
```http
GET /crm/v3/objects/deals?properties=dealname,amount,dealstage
```

### Create Deal
```http
POST /crm/v3/objects/deals
```

**Body:**
```json
{
  "properties": {
    "dealname": "New Enterprise Deal",
    "amount": "50000",
    "dealstage": "qualifiedtobuy",
    "pipeline": "default"
  }
}
```

### Update Deal
```http
PATCH /crm/v3/objects/deals/{dealId}
```

**Body:**
```json
{
  "properties": {
    "dealstage": "closedwon",
    "amount": "55000"
  }
}
```

### Search Deals
```http
POST /crm/v3/objects/deals/search
```

---

## Associations (v4)

### Get Associations
```http
GET /crm/v4/objects/{fromObjectType}/{objectId}/associations/{toObjectType}
```

**Example:** Get contacts associated with a deal
```bash
GET /crm/v4/objects/deals/123456/associations/contacts
```

---

## Engagements

### Emails

**List Emails:**
```http
GET /crm/v3/objects/emails?properties=hs_email_subject,hs_email_text,hs_timestamp
```

**Log Email:**
```http
POST /crm/v3/objects/emails
```
```json
{
  "properties": {
    "hs_timestamp": "2025-12-13T10:00:00Z",
    "hs_email_direction": "EMAIL",
    "hs_email_subject": "Follow up",
    "hs_email_text": "Email body content"
  }
}
```

### Calls

**List Calls:**
```http
GET /crm/v3/objects/calls?properties=hs_call_title,hs_call_body,hs_timestamp
```

**Log Call:**
```http
POST /crm/v3/objects/calls
```
```json
{
  "properties": {
    "hs_timestamp": "2025-12-13T10:00:00Z",
    "hs_call_title": "Sales Call",
    "hs_call_body": "Discussed pricing options",
    "hs_call_duration": "1800000"
  }
}
```

### Notes

**List Notes:**
```http
GET /crm/v3/objects/notes?properties=hs_note_body,hs_timestamp
```

**Create Note:**
```http
POST /crm/v3/objects/notes
```
```json
{
  "properties": {
    "hs_timestamp": "2025-12-13T10:00:00Z",
    "hs_note_body": "Important note about this contact"
  }
}
```

### Meetings

**List Meetings:**
```http
GET /crm/v3/objects/meetings?properties=hs_meeting_title,hs_meeting_body,hs_timestamp
```

**Create Meeting:**
```http
POST /crm/v3/objects/meetings
```
```json
{
  "properties": {
    "hs_timestamp": "2025-12-13T10:00:00Z",
    "hs_meeting_title": "Product Demo",
    "hs_meeting_body": "Demo of new features",
    "hs_meeting_start_time": "2025-12-13T14:00:00Z",
    "hs_meeting_end_time": "2025-12-13T15:00:00Z"
  }
}
```

---

## Common Properties

### Contact Properties
- `email`, `firstname`, `lastname`, `phone`
- `company`, `jobtitle`, `lifecyclestage`
- `hs_lead_status`, `hubspot_owner_id`

### Company Properties
- `name`, `domain`, `industry`, `phone`
- `city`, `state`, `country`
- `numberofemployees`, `annualrevenue`

### Deal Properties
- `dealname`, `amount`, `dealstage`, `pipeline`
- `closedate`, `hubspot_owner_id`
- `hs_priority`, `dealtype`

---

## Pagination

All list endpoints return paginated results:

```json
{
  "results": [...],
  "paging": {
    "next": {
      "after": "cursor_value",
      "link": "https://api.hubapi.com/..."
    }
  }
}
```

Use `after` parameter for next page:
```
GET /crm/v3/objects/contacts?after=cursor_value
```

---

## Rate Limits

| Limit Type | Value |
|------------|-------|
| Burst | 100 requests per 10 seconds |
| Daily | 500,000 requests per day |

When rate limited, API returns `429 Too Many Requests` with `Retry-After` header.

---

## References

- [CRM API Overview](https://developers.hubspot.com/docs/api/crm/understanding-the-crm)
- [Contacts API](https://developers.hubspot.com/docs/api/crm/contacts)
- [Deals API](https://developers.hubspot.com/docs/api/crm/deals)
- [Engagements API](https://developers.hubspot.com/docs/api/crm/engagements)
