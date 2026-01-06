# Airtable Field Types Reference

**Complete reference for all Airtable field types and their API formats.**

---

## Field Types Overview

| Category | Types |
|----------|-------|
| **Text** | singleLineText, multilineText, richText, email, url, phoneNumber |
| **Number** | number, currency, percent, duration, rating |
| **Selection** | singleSelect, multipleSelects, checkbox |
| **Date/Time** | date, dateTime, createdTime, lastModifiedTime |
| **Relationship** | multipleRecordLinks, lookup, rollup, count |
| **User** | singleCollaborator, multipleCollaborators, createdBy, lastModifiedBy |
| **Special** | multipleAttachments, autoNumber, barcode, button, formula |

---

## Text Fields

### singleLineText

**Read:**
```json
{"Name": "John Doe"}
```

**Write:**
```json
{"fields": {"Name": "John Doe"}}
```

### multilineText

**Read:**
```json
{"Notes": "Line 1\nLine 2\nLine 3"}
```

**Write:**
```json
{"fields": {"Notes": "Line 1\nLine 2"}}
```

### richText

**Read:** Returns plain text (formatting not preserved via API)
```json
{"Description": "This is **bold** text"}
```

**Write:** Plain text only
```json
{"fields": {"Description": "Plain text here"}}
```

### email

**Read:**
```json
{"Email": "user@example.com"}
```

**Write:**
```json
{"fields": {"Email": "user@example.com"}}
```

### url

**Read:**
```json
{"Website": "https://example.com"}
```

**Write:**
```json
{"fields": {"Website": "https://example.com"}}
```

### phoneNumber

**Read:**
```json
{"Phone": "+1 555-123-4567"}
```

**Write:**
```json
{"fields": {"Phone": "+1 555-123-4567"}}
```

---

## Number Fields

### number

**Read:**
```json
{"Quantity": 42}
{"Price": 19.99}
```

**Write:**
```json
{"fields": {"Quantity": 42}}
{"fields": {"Price": 19.99}}
```

### currency

**Read:** (number, formatting in Airtable UI)
```json
{"Amount": 1234.56}
```

**Write:**
```json
{"fields": {"Amount": 1234.56}}
```

### percent

**Read:** (decimal, e.g., 0.75 = 75%)
```json
{"Completion": 0.75}
```

**Write:**
```json
{"fields": {"Completion": 0.75}}
```

### duration

**Read:** (seconds as number)
```json
{"Duration": 3600}
```

**Write:**
```json
{"fields": {"Duration": 3600}}
```

### rating

**Read:** (1-10 integer)
```json
{"Rating": 5}
```

**Write:**
```json
{"fields": {"Rating": 5}}
```

---

## Selection Fields

### singleSelect

**Read:**
```json
{"Status": "In Progress"}
```

**Write:**
```json
{"fields": {"Status": "In Progress"}}
```

**Note:** Value must match existing option, or use `typecast: true` to create new option (if permitted).

### multipleSelects

**Read:**
```json
{"Tags": ["Urgent", "Backend", "Bug"]}
```

**Write:**
```json
{"fields": {"Tags": ["Urgent", "Backend"]}}
```

### checkbox

**Read:**
```json
{"Completed": true}
{"Archived": false}
```

**Write:**
```json
{"fields": {"Completed": true}}
```

**Note:** `false` values may be omitted from response.

---

## Date/Time Fields

### date

**Read:** (ISO 8601 date string)
```json
{"Due Date": "2025-01-15"}
```

**Write:**
```json
{"fields": {"Due Date": "2025-01-15"}}
```

### dateTime

**Read:** (ISO 8601 with time and timezone)
```json
{"Meeting Time": "2025-01-15T10:30:00.000Z"}
```

**Write:**
```json
{"fields": {"Meeting Time": "2025-01-15T10:30:00.000Z"}}
```

### createdTime (Read-Only)

**Read:**
```json
{"Created": "2025-01-10T08:00:00.000Z"}
```

### lastModifiedTime (Read-Only)

**Read:**
```json
{"Modified": "2025-01-14T15:30:00.000Z"}
```

---

## Relationship Fields

### multipleRecordLinks

**Read:**
```json
{"Projects": ["recXXXXXX", "recYYYYYY"]}
```

**Write:**
```json
{"fields": {"Projects": ["recXXXXXX", "recYYYYYY"]}}
```

**Note:** Values are record IDs from linked table.

### lookup (Read-Only)

**Read:** (depends on looked-up field type)
```json
{"Project Names": ["Project A", "Project B"]}
{"Project Budgets": [10000, 25000]}
```

### rollup (Read-Only)

**Read:** (depends on aggregation)
```json
{"Total Budget": 35000}
{"Task Count": 12}
```

### count (Read-Only)

**Read:**
```json
{"Linked Records": 5}
```

---

## User Fields

### singleCollaborator

**Read:**
```json
{
  "Assignee": {
    "id": "usrXXXXXX",
    "email": "user@example.com",
    "name": "John Doe"
  }
}
```

**Write:** (use user ID)
```json
{"fields": {"Assignee": {"id": "usrXXXXXX"}}}
```

### multipleCollaborators

**Read:**
```json
{
  "Team": [
    {"id": "usrXXX", "email": "a@example.com", "name": "Alice"},
    {"id": "usrYYY", "email": "b@example.com", "name": "Bob"}
  ]
}
```

**Write:**
```json
{"fields": {"Team": [{"id": "usrXXX"}, {"id": "usrYYY"}]}}
```

### createdBy (Read-Only)

**Read:**
```json
{
  "Created By": {
    "id": "usrXXXXXX",
    "email": "user@example.com",
    "name": "Creator Name"
  }
}
```

### lastModifiedBy (Read-Only)

**Read:**
```json
{
  "Modified By": {
    "id": "usrXXXXXX",
    "email": "user@example.com",
    "name": "Editor Name"
  }
}
```

---

## Special Fields

### multipleAttachments

**Read:**
```json
{
  "Files": [
    {
      "id": "attXXXXXX",
      "url": "https://dl.airtable.com/.../file.pdf",
      "filename": "document.pdf",
      "size": 12345,
      "type": "application/pdf",
      "thumbnails": {
        "small": {"url": "...", "width": 36, "height": 36},
        "large": {"url": "...", "width": 512, "height": 512}
      }
    }
  ]
}
```

**Write:** (URL must be publicly accessible)
```json
{
  "fields": {
    "Files": [
      {"url": "https://example.com/file.pdf"}
    ]
  }
}
```

**Note:** Cannot delete individual attachments, only replace entire array.

### autoNumber (Read-Only)

**Read:**
```json
{"ID": 42}
```

### barcode

**Read:**
```json
{
  "Barcode": {
    "text": "1234567890"
  }
}
```

**Write:**
```json
{"fields": {"Barcode": {"text": "1234567890"}}}
```

### button (Read-Only)

Buttons are UI-only and cannot be read/written via API.

### formula (Read-Only)

**Read:** (depends on formula result type)
```json
{"Full Name": "John Doe"}
{"Days Until Due": 5}
{"Is Overdue": true}
```

---

## Type Conversion with typecast

When `typecast: true` is included in the request:

- **singleSelect/multipleSelects:** Creates new options if they don't exist
- **date/dateTime:** Parses common date formats
- **number/currency/percent:** Converts strings to numbers
- **multipleRecordLinks:** Searches by primary field value instead of record ID

**Example:**
```json
{
  "records": [
    {"fields": {"Status": "New Status"}}
  ],
  "typecast": true
}
```

**Note:** `typecast` requires creator/owner permissions for creating new select options.

---

## Field Type Detection

Get field types from the base schema:

```bash
GET https://api.airtable.com/v0/meta/bases/{baseId}/tables
```

Response includes field types:
```json
{
  "tables": [{
    "fields": [
      {"id": "fldXXX", "name": "Name", "type": "singleLineText"},
      {"id": "fldYYY", "name": "Status", "type": "singleSelect", "options": {...}},
      {"id": "fldZZZ", "name": "Due Date", "type": "date", "options": {...}}
    ]
  }]
}
```

---

**Last Updated:** 2025-12-11
