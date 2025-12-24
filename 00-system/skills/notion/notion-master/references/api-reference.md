# Notion API Reference

**Consolidated API documentation for all Notion operations in Nexus**

Reference this file from all Notion-related skills using progressive disclosure.

---

## API Configuration

**Base URL:** `https://api.notion.com/v1`

**Required Headers:**
```bash
Authorization: Bearer ${NOTION_API_KEY}
Notion-Version: 2022-06-28
Content-Type: application/json
```

---

## Query Database

**Endpoint:** `POST /databases/{database_id}/query`

**Purpose:** Search and filter records in a Notion database

### Basic Query (All Records)

```bash
curl -s -X POST "https://api.notion.com/v1/databases/${NOTION_SKILLS_DB_ID}/query" \
  -H "Authorization: Bearer ${NOTION_API_KEY}" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{"page_size": 100}'
```

**Response:**
```json
{
  "object": "list",
  "results": [
    {
      "id": "page-id",
      "properties": {
        "Skill Name": {"title": [{"text": {"content": "skill-name"}}]},
        "Description": {"rich_text": [{"text": {"content": "..."}}]},
        "Team": {"select": {"name": "Solutions"}},
        "Integration": {"multi_select": [{"name": "Beam AI"}]},
        "Owner": {"people": [{"id": "user-id", "name": "Name"}]},
        "Created": {"date": {"start": "2025-12-09"}},
        "Skill": {"files": [{"name": "skill.txt", "file": {"url": "..."}}]}
      }
    }
  ],
  "has_more": false,
  "next_cursor": null
}
```

### Filtered Queries

**Filter by Team (select property):**
```json
{
  "filter": {
    "property": "Team",
    "select": {
      "equals": "Solutions"
    }
  }
}
```

**Filter by Integration (multi_select property):**
```json
{
  "filter": {
    "property": "Integration",
    "multi_select": {
      "contains": "Beam AI"
    }
  }
}
```

**Filter by Skill Name (title property):**
```json
{
  "filter": {
    "property": "Skill Name",
    "title": {
      "contains": "beam"
    }
  }
}
```

**Filter by Owner (people property):**
```json
{
  "filter": {
    "property": "Owner",
    "people": {
      "contains": "user-id-here"
    }
  }
}
```

### Sorted Queries

**Sort by Created (newest first):**
```json
{
  "sorts": [
    {
      "property": "Created",
      "direction": "descending"
    }
  ]
}
```

**Sort by Skill Name (A-Z):**
```json
{
  "sorts": [
    {
      "property": "Skill Name",
      "direction": "ascending"
    }
  ]
}
```

### Pagination

**For databases with >100 records:**
```json
{
  "page_size": 100,
  "start_cursor": "next-cursor-from-previous-response"
}
```

---

## Get Page

**Endpoint:** `GET /pages/{page_id}`

**Purpose:** Retrieve full page details including file URLs

```bash
curl -s "https://api.notion.com/v1/pages/{page_id}" \
  -H "Authorization: Bearer ${NOTION_API_KEY}" \
  -H "Notion-Version: 2022-06-28"
```

**Use case:** Get download URL for skill file attachment

**Extract file URL:**
```python
file_url = page["properties"]["Skill"]["files"][0]["file"]["url"]
```

**Important:** File URLs expire after 1 hour. Download immediately after retrieving.

---

## Create Page

**Endpoint:** `POST /pages`

**Purpose:** Create a new database entry (for exporting skills)

### Without File Attachment

```bash
curl -s -X POST "https://api.notion.com/v1/pages" \
  -H "Authorization: Bearer ${NOTION_API_KEY}" \
  -H "Content-Type: application/json" \
  -H "Notion-Version: 2022-06-28" \
  -d '{
    "parent": {"database_id": "NOTION_SKILLS_DB_ID"},
    "properties": {
      "Skill Name": {"title": [{"text": {"content": "skill-name"}}]},
      "Description": {"rich_text": [{"text": {"content": "description"}}]},
      "Purpose": {"rich_text": [{"text": {"content": "purpose"}}]},
      "Team": {"select": {"name": "General"}},
      "Integration": {"multi_select": [{"name": "Notion"}]},
      "Owner": {"people": [{"id": "notion_user_id"}]},
      "Created": {"date": {"start": "2025-12-09"}}
    }
  }'
```

### With File Attachment (3-step process)

**Step 1: Create file upload object**
```bash
curl -s -X POST "https://api.notion.com/v1/file_uploads" \
  -H "Authorization: Bearer ${NOTION_API_KEY}" \
  -H "Content-Type: application/json" \
  -H "Notion-Version: 2022-06-28" \
  -d '{}'
```

**Response:**
```json
{
  "id": "file-upload-id-abc123",
  "status": "ready"
}
```

**Step 2: Send file content**
```bash
curl -s -X POST "https://api.notion.com/v1/file_uploads/{file_upload_id}/send" \
  -H "Authorization: Bearer ${NOTION_API_KEY}" \
  -H "Notion-Version: 2022-06-28" \
  -F "file=@/path/to/skill-name-SKILL.txt"
```

**Response:**
```json
{
  "id": "file-upload-id-abc123",
  "status": "uploaded"
}
```

**Step 3: Create page with file attachment**
```bash
curl -s -X POST "https://api.notion.com/v1/pages" \
  -H "Authorization: Bearer ${NOTION_API_KEY}" \
  -H "Content-Type: application/json" \
  -H "Notion-Version: 2022-06-28" \
  -d '{
    "parent": {"database_id": "NOTION_SKILLS_DB_ID"},
    "properties": {
      "Skill Name": {"title": [{"text": {"content": "skill-name"}}]},
      "Description": {"rich_text": [{"text": {"content": "description"}}]},
      "Skill": {
        "files": [{
          "type": "file_upload",
          "file_upload": {"id": "file-upload-id-abc123"},
          "name": "skill-name-SKILL.txt"
        }]
      }
    }
  }'
```

---

## File Upload API

**Documentation:** https://developers.notion.com/docs/uploading-small-files

### Supported File Types

**Allowed MIME types:**
- Text: `.txt`, `.json`
- Documents: `.pdf`, `.doc`, `.docx`
- Spreadsheets: `.xls`, `.xlsx`
- Presentations: `.ppt`, `.pptx`
- Images: `.png`, `.jpg`, `.gif`, `.svg`
- Audio: `.mp3`, `.wav`
- Video: `.mp4`, `.mov`

**NOT supported:**
- ❌ `.zip` files (rejected with HTTP 400)
- ❌ `.md` files (not in allowed list)
- ❌ `.skill` files (custom extension, treated as zip)

**Workaround:** Rename `.md` → `.txt` before upload, rename back on download

### File Size Limits

- Maximum file size: 5 MB per file
- For larger files: Use external storage (GitHub) + URL property

### File URL Expiration

- Download URLs expire after **1 hour**
- Always download immediately after retrieving page
- Don't cache URLs for later use

---

## Get User Info

**Endpoint:** `GET /users/me`

**Purpose:** Get user ID for Owner property during setup

```bash
curl -s "https://api.notion.com/v1/users/me" \
  -H "Authorization: Bearer ${NOTION_API_KEY}" \
  -H "Notion-Version: 2022-06-28"
```

**Response:**
```json
{
  "object": "user",
  "id": "abc123-user-id",
  "name": "Your Name",
  "avatar_url": "...",
  "type": "person",
  "person": {
    "email": "you@example.com"
  }
}
```

**Save to user-config.yaml:**
```yaml
notion_user_id: "abc123-user-id"
notion_user_name: "Your Name"
```

---

## Property Types Reference

### Title (Skill Name)

```json
"Skill Name": {
  "title": [{"text": {"content": "skill-name"}}]
}
```

### Rich Text (Description, Purpose)

```json
"Description": {
  "rich_text": [{"text": {"content": "description text"}}]
}
```

### Select (Team)

```json
"Team": {
  "select": {"name": "General"}
}
```

**Auto-create:** If team doesn't exist, Notion creates it automatically

### Multi-Select (Integration)

```json
"Integration": {
  "multi_select": [
    {"name": "Beam AI"},
    {"name": "Notion"}
  ]
}
```

### People (Owner)

```json
"Owner": {
  "people": [{"id": "user-id-abc123"}]
}
```

### Date (Created)

```json
"Created": {
  "date": {"start": "2025-12-09"}
}
```

### Files (Skill attachment)

**With file upload:**
```json
"Skill": {
  "files": [{
    "type": "file_upload",
    "file_upload": {"id": "file-upload-id"},
    "name": "skill-name-SKILL.txt"
  }]
}
```

**With external URL:**
```json
"Skill": {
  "files": [{
    "type": "external",
    "name": "skill-name.skill",
    "external": {"url": "https://github.com/..."}
  }]
}
```

---

## Rate Limits

**Notion API rate limits:**
- **3 requests per second** per integration
- Exceeding limit returns HTTP 429 (Too Many Requests)
- Implement exponential backoff for retries

**Example retry logic:**
```python
import time
import requests

def query_with_retry(url, headers, data, max_retries=3):
    for attempt in range(max_retries):
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 429:
            wait_time = 2 ** attempt  # Exponential backoff
            time.sleep(wait_time)
            continue
        return response
    raise Exception("Max retries exceeded")
```

---

## Error Codes

See [error-handling.md](error-handling.md) for comprehensive error handling guide.

---

## Official Documentation

- [Notion API Docs](https://developers.notion.com/reference/intro)
- [File Upload API](https://developers.notion.com/docs/uploading-small-files)
- [Database Query](https://developers.notion.com/reference/post-database-query)
- [Create Page](https://developers.notion.com/reference/post-page)
- [Get Page](https://developers.notion.com/reference/retrieve-a-page)

---

## Reference from Skills

**In SKILL.md files, reference specific sections:**

```markdown
## API Details

See [API Reference](../_notion-shared/references/api-reference.md#query-database) for full documentation.
```

This keeps SKILL.md files concise while providing complete API details on-demand.
