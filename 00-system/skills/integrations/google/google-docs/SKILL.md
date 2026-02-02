---
name: google-docs
description: "Read, write, and manage Google Docs. Load when user mentions 'google docs', 'google document', 'create doc', 'read doc', 'write doc', 'edit document', or references creating/editing text documents in Google Drive."
---

# Google Docs

Read, write, create, and manage Google Docs via OAuth authentication.

## Pre-Flight Check (ALWAYS RUN FIRST)

```bash
uv run python 00-system/skills/google/google-master/scripts/google_auth.py --check --service docs
```

**Exit codes:**
- **0**: Ready to use - proceed with user request
- **1**: Need to login - run `python3 00-system/skills/google/google-master/scripts/google_auth.py --login`
- **2**: Missing credentials or dependencies - see [../google-master/references/setup-guide.md](../google-master/references/setup-guide.md)

---

## Quick Reference

### Read Document
```bash
uv run python 00-system/skills/google/google-docs/scripts/docs_operations.py read <document_id>
```

### Create Document
```bash
uv run python 00-system/skills/google/google-docs/scripts/docs_operations.py create "My Document" --content "Initial content here"
```

### Insert Text
```bash
uv run python 00-system/skills/google/google-docs/scripts/docs_operations.py insert <document_id> "Text to insert" --index 1
```

### Append Text
```bash
uv run python 00-system/skills/google/google-docs/scripts/docs_operations.py append <document_id> "Text to append at end"
```

### Find and Replace
```bash
uv run python 00-system/skills/google/google-docs/scripts/docs_operations.py replace <document_id> "old text" "new text"
```

### Export Document
```bash
uv run python 00-system/skills/google/google-docs/scripts/docs_operations.py export <document_id> --format pdf --output ./report.pdf
```

### List Documents
```bash
uv run python 00-system/skills/google/google-docs/scripts/docs_operations.py list --query "report"
```

### Copy Document
```bash
uv run python 00-system/skills/google/google-docs/scripts/docs_operations.py copy <document_id> "Copy of My Document"
```

### Rename Document
```bash
uv run python 00-system/skills/google/google-docs/scripts/docs_operations.py rename <document_id> "New Title"
```

---

## Document ID

The document ID is in the URL:
```
https://docs.google.com/document/d/[DOCUMENT_ID]/edit
```

---

## Common Workflows

### Generate Report -> Save to Google Docs

```python
from docs_operations import create_document, append_text

doc = create_document("Weekly Report - Jan 2024")
append_text(doc['document_id'], "Key findings from this week...")
print(f"Report created: {doc['url']}")
```

### Create Document from Template

```python
from docs_operations import copy_document, replace_all_text

new_doc = copy_document(template_id, "Invoice #1234")
replace_all_text(new_doc['document_id'], "{{CLIENT}}", "Acme Corp")
replace_all_text(new_doc['document_id'], "{{AMOUNT}}", "$5,000")
```

---

## Available Operations

| Operation | Function | Description |
|-----------|----------|-------------|
| **Read** | `read_document()` | Get document content |
| **Info** | `get_document_info()` | Get title, ID, URL |
| **Create** | `create_document()` | Create new document |
| **Copy** | `copy_document()` | Duplicate document |
| **Rename** | `rename_document()` | Change title |
| **Insert** | `insert_text()` | Insert at position |
| **Append** | `append_text()` | Add to end |
| **Replace** | `replace_all_text()` | Find and replace |
| **Export** | `export_document()` | Export to text/HTML/PDF/DOCX |
| **List** | `list_documents()` | List accessible docs |

---

## Error Handling

See [../google-master/references/error-handling.md](../google-master/references/error-handling.md) for common errors and solutions.

---

## Setup

First-time setup: [../google-master/references/setup-guide.md](../google-master/references/setup-guide.md)

**Quick start:**
1. `pip install google-auth google-auth-oauthlib google-api-python-client`
2. Create OAuth credentials in Google Cloud Console (enable Google Docs API & Drive API, choose "Desktop app")
3. Add to `.env` file at Nexus root:
   ```
   GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
   GOOGLE_CLIENT_SECRET=your-client-secret
   GOOGLE_PROJECT_ID=your-project-id
   ```
4. Run `python3 00-system/skills/google/google-master/scripts/google_auth.py --login`
