# HubSpot Error Handling

## HTTP Status Codes

| Code | Meaning | Action |
|------|---------|--------|
| `200` | Success | Process response |
| `201` | Created | Record created successfully |
| `204` | No Content | Delete successful |
| `400` | Bad Request | Check request body/params |
| `401` | Unauthorized | Invalid/expired token |
| `403` | Forbidden | Missing scope |
| `404` | Not Found | Record doesn't exist |
| `409` | Conflict | Duplicate record |
| `429` | Rate Limited | Retry after delay |
| `500` | Server Error | Retry later |
| `502` | Bad Gateway | Retry later |
| `503` | Service Unavailable | Retry later |

---

## Error Response Format

```json
{
  "status": "error",
  "message": "Property values were not valid",
  "correlationId": "abc123-def456",
  "category": "VALIDATION_ERROR",
  "errors": [
    {
      "message": "Email is invalid",
      "error": "INVALID_EMAIL",
      "name": "email"
    }
  ]
}
```

---

## Common Errors

### Authentication Errors

**401 - Invalid Token**
```json
{
  "status": "error",
  "message": "Authentication credentials not found",
  "category": "INVALID_AUTHENTICATION"
}
```
**Fix:** Check `HUBSPOT_ACCESS_TOKEN` is set and valid.

**403 - Missing Scope**
```json
{
  "status": "error",
  "message": "This app hasn't been granted all required scopes",
  "category": "MISSING_SCOPES",
  "errors": [
    {"message": "crm.objects.contacts.write"}
  ]
}
```
**Fix:** Add missing scope to Private App settings and regenerate token.

---

### Validation Errors

**400 - Invalid Property**
```json
{
  "status": "error",
  "message": "Property values were not valid",
  "category": "VALIDATION_ERROR",
  "errors": [
    {"message": "Property 'bad_prop' does not exist", "name": "bad_prop"}
  ]
}
```
**Fix:** Use valid property names from schema.

**400 - Invalid Email**
```json
{
  "status": "error",
  "category": "VALIDATION_ERROR",
  "errors": [
    {"message": "Email is invalid", "error": "INVALID_EMAIL", "name": "email"}
  ]
}
```
**Fix:** Validate email format before sending.

---

### Conflict Errors

**409 - Duplicate Contact**
```json
{
  "status": "error",
  "message": "Contact already exists",
  "category": "CONFLICT",
  "errors": [
    {"message": "Contact already exists. Existing ID: 12345"}
  ]
}
```
**Fix:** Use search to find existing record, then update instead of create.

---

### Not Found Errors

**404 - Record Not Found**
```json
{
  "status": "error",
  "message": "resource not found",
  "category": "OBJECT_NOT_FOUND"
}
```
**Fix:** Verify record ID exists before updating/deleting.

---

## AI Action Mapping

When errors occur, map to appropriate AI actions:

| Error Category | AI Action |
|---------------|-----------|
| `INVALID_AUTHENTICATION` | `prompt_for_access_token` |
| `MISSING_SCOPES` | `add_missing_scopes` |
| `VALIDATION_ERROR` | `show_error_details` |
| `CONFLICT` | `search_and_update` |
| `OBJECT_NOT_FOUND` | `verify_record_id` |
| `RATE_LIMITED` | `wait_and_retry` |

---

## Error Handling Pattern

```python
from hubspot_client import HubSpotClient, HubSpotError

client = HubSpotClient()

try:
    result = client.post('/crm/v3/objects/contacts', {
        "properties": {"email": "test@example.com"}
    })
except HubSpotError as e:
    if e.category == 'CONFLICT':
        # Contact exists - search and update instead
        print(f"Contact exists, use update instead")
    elif e.category == 'VALIDATION_ERROR':
        # Show validation errors
        for error in e.errors:
            print(f"Validation: {error['name']} - {error['message']}")
    elif e.category == 'MISSING_SCOPES':
        # Need to add scopes
        print("Missing scopes - update Private App settings")
    else:
        # Unknown error
        print(f"Error: {e.message}")
        print(f"Correlation ID: {e.correlation_id}")
```

---

## Correlation ID

Every error includes a `correlationId`. Save this for debugging:

```python
except HubSpotError as e:
    logging.error(f"HubSpot error: {e.message}")
    logging.error(f"Correlation ID: {e.correlation_id}")
```

Use correlation ID when contacting HubSpot support.

---

## Rate Limiting

When rate limited (429):

1. Check `Retry-After` header for wait time
2. Implement exponential backoff
3. Consider batching requests

```python
# Rate limit handling is built into hubspot_client.py
# It automatically retries with backoff
```

---

## References

- [Error Responses](https://developers.hubspot.com/docs/api/error-handling)
- [Validation Errors](https://developers.hubspot.com/docs/api/crm/understanding-the-crm#validation)
- [Rate Limits](https://developers.hubspot.com/docs/api/usage-details)
