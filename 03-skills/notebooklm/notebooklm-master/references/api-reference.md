# NotebookLM Enterprise API Reference

Complete API documentation for NotebookLM Enterprise.

---

## Base URL

```
https://{ENDPOINT_LOCATION}-discoveryengine.googleapis.com/v1alpha/projects/{PROJECT_NUMBER}/locations/{LOCATION}
```

**Endpoint location prefixes:**
- `global-` (default)
- `us-`
- `eu-`

---

## Authentication

All requests require OAuth 2.0 Bearer token:

```bash
curl -H "Authorization: Bearer $(gcloud auth print-access-token)" \
     -H "Content-Type: application/json" \
     "https://global-discoveryengine.googleapis.com/v1alpha/..."
```

---

## Notebooks API

### Create Notebook

**Endpoint:** `POST /notebooks`

**Request:**
```json
{
  "title": "My Notebook"
}
```

**Response:**
```json
{
  "title": "My Notebook",
  "notebookId": "abc123",
  "name": "projects/123/locations/global/notebooks/abc123",
  "metadata": {
    "userRole": "OWNER",
    "sharingStatus": "PRIVATE"
  }
}
```

---

### Get Notebook

**Endpoint:** `GET /notebooks/{notebookId}`

**Response:** Same as create response

---

### List Recently Viewed

**Endpoint:** `GET /notebooks:listRecentlyViewed`

**Response:**
```json
{
  "notebooks": [
    {
      "title": "Notebook 1",
      "notebookId": "abc123",
      ...
    }
  ]
}
```

---

### Batch Delete Notebooks

**Endpoint:** `POST /notebooks:batchDelete`

**Request:**
```json
{
  "names": [
    "projects/123/locations/global/notebooks/abc123",
    "projects/123/locations/global/notebooks/def456"
  ]
}
```

**Response:** Empty object `{}`

---

### Share Notebook

**Endpoint:** `POST /notebooks/{notebookId}:share`

**Request:**
```json
{
  "shareSettings": [
    {
      "email": "user@example.com",
      "role": "READER"
    }
  ]
}
```

**Roles:** `OWNER`, `WRITER`, `READER`, `NOT_SHARED`

---

## Sources API

### Batch Create Sources

**Endpoint:** `POST /notebooks/{notebookId}/sources:batchCreate`

**Request (Google Drive):**
```json
{
  "requests": [
    {
      "userContent": {
        "googleDriveContent": {
          "resourceId": "drive_file_id"
        }
      }
    }
  ]
}
```

**Request (Web URL):**
```json
{
  "requests": [
    {
      "userContent": {
        "webContent": {
          "url": "https://example.com/article"
        }
      }
    }
  ]
}
```

**Request (YouTube):**
```json
{
  "requests": [
    {
      "userContent": {
        "videoContent": {
          "url": "https://youtube.com/watch?v=xxx"
        }
      }
    }
  ]
}
```

**Request (Raw Text):**
```json
{
  "requests": [
    {
      "userContent": {
        "textContent": {
          "text": "Your text content here..."
        }
      }
    }
  ]
}
```

---

### Upload File

**Endpoint:** `POST /notebooks/{notebookId}/sources:uploadFile`

**Headers:**
```
Authorization: Bearer {token}
Content-Type: application/pdf  # or appropriate MIME type
X-Goog-Upload-File-Name: document.pdf
X-Goog-Upload-Protocol: raw
```

**Body:** Raw file bytes

**Supported formats:**
- Documents: PDF, TXT, MD, DOCX, PPTX, XLSX
- Audio: MP3, WAV, AAC, OGG, FLAC
- Images: PNG, JPG, JPEG

---

### Get Source

**Endpoint:** `GET /notebooks/{notebookId}/sources/{sourceId}`

**Response:**
```json
{
  "sourceId": "source123",
  "title": "Document Title",
  "metadata": {
    "wordCount": 5000,
    "tokenCount": 7500
  },
  "status": "READY"
}
```

---

### Batch Delete Sources

**Endpoint:** `POST /notebooks/{notebookId}/sources:batchDelete`

**Request:**
```json
{
  "names": [
    "projects/123/locations/global/notebooks/abc/sources/source1"
  ]
}
```

---

## Audio Overview API

### Create Audio Overview

**Endpoint:** `POST /notebooks/{notebookId}/audioOverviews`

**Request:**
```json
{
  "sourceIds": [
    {"id": "source1"},
    {"id": "source2"}
  ],
  "episodeFocus": "Focus on the key findings and methodology",
  "languageCode": "en"
}
```

**Notes:**
- `sourceIds` is optional - omit to use all sources
- Only one audio overview per notebook
- Processing takes several minutes

**Response:**
```json
{
  "audioOverview": {
    "status": "AUDIO_OVERVIEW_STATUS_IN_PROGRESS",
    "audioOverviewId": "audio123",
    "name": "projects/123/locations/global/notebooks/abc/audioOverviews/default"
  }
}
```

**Status values:**
- `AUDIO_OVERVIEW_STATUS_IN_PROGRESS`
- `AUDIO_OVERVIEW_STATUS_READY`
- `AUDIO_OVERVIEW_STATUS_FAILED`

---

### Delete Audio Overview

**Endpoint:** `DELETE /notebooks/{notebookId}/audioOverviews/default`

**Response:** Empty object `{}`

---

## Error Codes

| Code | Meaning |
|------|---------|
| 400 | Bad request - check request format |
| 401 | Unauthorized - token expired or invalid |
| 403 | Forbidden - missing permissions or API not enabled |
| 404 | Not found - notebook or source doesn't exist |
| 429 | Rate limited - too many requests |
| 500 | Server error - retry later |

---

## Rate Limits

- **Requests:** 100 per minute per user
- **Audio overviews:** 10 per day per project

---

**Last Updated**: 2025-12-27
**API Version**: v1alpha
