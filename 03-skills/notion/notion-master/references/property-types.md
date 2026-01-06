# Notion Property Types Reference

> Quick reference for all Notion database property types and how to work with them.

---

## Property Type Overview

| Type | Description | Read Format | Write Format |
|------|-------------|-------------|--------------|
| `title` | Primary name field | Plain text | `"My Title"` |
| `rich_text` | Multi-line text | Plain text | `"Description here"` |
| `number` | Numeric value | Number | `42` or `3.14` |
| `select` | Single choice | Option name | `"Option Name"` |
| `multi_select` | Multiple choices | Comma-separated | `"Tag1, Tag2"` |
| `status` | Workflow state | Status name | `"In Progress"` |
| `date` | Date/datetime | ISO format | `"2025-01-15"` |
| `checkbox` | Boolean | Yes/No | `true` or `"yes"` |
| `url` | Web link | URL string | `"https://..."` |
| `email` | Email address | Email string | `"user@example.com"` |
| `phone_number` | Phone | Phone string | `"+1-555-123-4567"` |
| `people` | User assignment | User names | User ID(s) |
| `relation` | Link to database | Page count | Page ID(s) |
| `files` | Attachments | File count | (read-only via API) |
| `formula` | Calculated | Result value | (read-only) |
| `rollup` | Aggregated | Result value | (read-only) |
| `created_time` | Creation date | ISO datetime | (auto) |
| `last_edited_time` | Edit date | ISO datetime | (auto) |
| `created_by` | Creator | User name | (auto) |
| `last_edited_by` | Editor | User name | (auto) |

---

## Detailed Type Reference

### Title (`title`)

The primary identifier for pages. Every database has exactly one title property.

**Read value**: Plain text string
```json
{"title": [{"plain_text": "My Page Title"}]}
```

**Write value**: String
```python
--properties '{"Name": "My Page Title"}'
```

---

### Rich Text (`rich_text`)

Multi-line text content with optional formatting.

**Read value**: Plain text string (formatting stripped)
```json
{"rich_text": [{"plain_text": "Some description text"}]}
```

**Write value**: String
```python
--properties '{"Description": "Some description text"}'
```

**Note**: API writes plain text only. Formatting requires block operations.

---

### Number (`number`)

Numeric values with optional formatting (percent, currency, etc.).

**Read value**: Number or null
```json
{"number": 42}
```

**Write value**: Number or numeric string
```python
--properties '{"Points": 100}'
--properties '{"Price": "29.99"}'
```

---

### Select (`select`)

Single choice from predefined options.

**Read value**: Option name or null
```json
{"select": {"name": "High"}}
```

**Write value**: Option name (must exist)
```python
--properties '{"Priority": "High"}'
```

**Warning**: Writing non-existent option creates it (if integration has permissions).

---

### Multi-Select (`multi_select`)

Multiple choices from predefined options.

**Read value**: Comma-separated option names
```json
{"multi_select": [{"name": "Design"}, {"name": "Frontend"}]}
```

**Write value**: Comma-separated string or array
```python
--properties '{"Tags": "Design, Frontend"}'
--properties '{"Tags": ["Design", "Frontend"]}'
```

---

### Status (`status`)

Workflow state property (newer Notion feature).

**Read value**: Status name
```json
{"status": {"name": "In Progress"}}
```

**Write value**: Status name (must exist)
```python
--properties '{"Status": "Done"}'
```

**Note**: Status options are defined by Notion's workflow system, not editable via API.

---

### Date (`date`)

Date or date range with optional time.

**Read value**: ISO date string(s)
```json
{"date": {"start": "2025-01-15", "end": null}}
{"date": {"start": "2025-01-15T14:30:00.000Z", "end": "2025-01-16"}}
```

**Write value**: ISO format date
```python
--properties '{"Due Date": "2025-01-15"}'
--properties '{"Meeting": "2025-01-15T14:30:00"}'
```

**Formats**:
- Date only: `YYYY-MM-DD`
- With time: `YYYY-MM-DDTHH:MM:SS`
- With timezone: `YYYY-MM-DDTHH:MM:SS.000Z`

---

### Checkbox (`checkbox`)

Boolean true/false value.

**Read value**: "Yes" or "No"
```json
{"checkbox": true}
```

**Write value**: Boolean or truthy string
```python
--properties '{"Completed": true}'
--properties '{"Completed": "yes"}'
--properties '{"Completed": "1"}'
```

**Truthy values**: `true`, `yes`, `1`, `checked`
**Falsy values**: `false`, `no`, `0`, anything else

---

### URL (`url`)

Web link.

**Read value**: URL string or null
```json
{"url": "https://example.com"}
```

**Write value**: URL string
```python
--properties '{"Website": "https://example.com"}'
```

---

### Email (`email`)

Email address.

**Read value**: Email string or null
```json
{"email": "user@example.com"}
```

**Write value**: Email string
```python
--properties '{"Contact": "user@example.com"}'
```

---

### Phone Number (`phone_number`)

Phone number (any format).

**Read value**: Phone string or null
```json
{"phone_number": "+1-555-123-4567"}
```

**Write value**: Phone string
```python
--properties '{"Phone": "+1-555-123-4567"}'
```

---

### People (`people`)

User assignment(s).

**Read value**: Comma-separated user names
```json
{"people": [{"id": "user-id-1", "name": "John Doe"}]}
```

**Write value**: User ID(s) (NOT names)
```python
--properties '{"Assignee": "user-id-123"}'
--properties '{"Team": "user-id-1, user-id-2"}'
```

**Note**: Get user IDs from `list_users` API or previous queries.

---

### Relation (`relation`)

Links to pages in another database.

**Read value**: Count of linked pages
```json
{"relation": [{"id": "page-id-1"}, {"id": "page-id-2"}]}
```

**Write value**: Page ID(s)
```python
--properties '{"Project": "page-id-123"}'
--properties '{"Related": "page-id-1, page-id-2"}'
```

---

### Files (`files`)

File attachments.

**Read value**: File count
```json
{"files": [{"name": "doc.pdf", "type": "file"}]}
```

**Write value**: Not supported via API (upload separately)

---

### Computed Properties (Read-Only)

These properties are calculated automatically:

| Type | Description |
|------|-------------|
| `formula` | Calculated from other properties |
| `rollup` | Aggregated from relations |
| `created_time` | Page creation timestamp |
| `last_edited_time` | Last modification timestamp |
| `created_by` | User who created page |
| `last_edited_by` | User who last edited |

---

## Creating Properties (Database Schema)

When creating a database, use this format:

```json
[
  {"name": "Name", "type": "title"},
  {"name": "Description", "type": "rich_text"},
  {"name": "Status", "type": "select", "options": ["Todo", "In Progress", "Done"]},
  {"name": "Priority", "type": "select", "options": ["Low", "Medium", "High"]},
  {"name": "Tags", "type": "multi_select", "options": ["Design", "Dev", "Urgent"]},
  {"name": "Due Date", "type": "date"},
  {"name": "Points", "type": "number"},
  {"name": "Completed", "type": "checkbox"},
  {"name": "Website", "type": "url"},
  {"name": "Email", "type": "email"}
]
```

---

## Common Patterns

### Filtering by property type

| Property Type | Common Filters |
|---------------|----------------|
| `title`, `rich_text` | `=`, `!=`, `contains`, `starts_with` |
| `select`, `status` | `=`, `!=`, `is_empty` |
| `multi_select` | `contains`, `does_not_contain` |
| `number` | `=`, `!=`, `>`, `<`, `>=`, `<=` |
| `date` | `=`, `>`, `<`, `>=`, `<=` |
| `checkbox` | `=` (true/false) |
| `people`, `relation` | `contains`, `is_empty` |

### Sorting by property type

All property types support sorting:
```bash
--sort "Due Date" --sort-dir asc
--sort "Priority" --sort-dir desc
--sort "Name" --sort-dir asc
```

---

## Error Handling

**"Invalid property type"**: Check type matches schema
**"Invalid option"**: For select/multi_select, option must exist
**"Property not found"**: Property name must match exactly (case-sensitive)
**"Cannot modify"**: Formula, rollup, and auto-properties are read-only

---

*For full API documentation: [Notion Property Object Reference](https://developers.notion.com/reference/property-object)*
