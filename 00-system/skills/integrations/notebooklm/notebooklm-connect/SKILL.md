---
name: notebooklm-connect
description: "notebooklm, create notebook, audio overview, podcast."
---

# NotebookLM Connect

Meta-skill for NotebookLM Enterprise operations. Routes to appropriate skills based on user intent.

---

## Pre-Flight Check (ALWAYS FIRST)

Before any operation, verify configuration:

```bash
uv run python 00-system/skills/notebooklm/notebooklm-master/scripts/check_notebooklm_config.py --json
```

**Parse `ai_action` field:**

| ai_action | What to Do |
|-----------|------------|
| `proceed_with_operation` | Continue with user's request |
| `install_gcloud` | Guide: "Install gcloud from https://cloud.google.com/sdk/docs/install" |
| `run_gcloud_auth` | Run: `gcloud auth login` |
| `configure_project` | Ask for project number, save to .env |
| `run_setup_wizard` | Run: `python .../setup_notebooklm.py` |

---

## Workflow Routing

Match user intent to appropriate workflow:

### Workflow 1: Create Notebook

**Triggers:** "create notebook", "new notebook", "make notebook"

**Action:**
```bash
uv run python 00-system/skills/notebooklm/notebooklm-create-notebook/scripts/create_notebook.py --title "TITLE"
```

---

### Workflow 2: List Notebooks

**Triggers:** "list notebooks", "show notebooks", "my notebooks", "recent notebooks"

**Action:**
```bash
uv run python 00-system/skills/notebooklm/notebooklm-list-notebooks/scripts/list_notebooks.py
```

---

### Workflow 3: Get Notebook Details

**Triggers:** "get notebook", "show notebook", "notebook details"

**Action:**
```bash
uv run python 00-system/skills/notebooklm/notebooklm-get-notebook/scripts/get_notebook.py --notebook-id "ID"
```

---

### Workflow 4: Delete Notebooks

**Triggers:** "delete notebook", "remove notebook"

**Action:**
```bash
uv run python 00-system/skills/notebooklm/notebooklm-delete-notebooks/scripts/delete_notebooks.py --notebook-ids "ID1,ID2"
```

---

### Workflow 5: Share Notebook

**Triggers:** "share notebook", "give access", "add collaborator"

**Action:**
```bash
uv run python 00-system/skills/notebooklm/notebooklm-share-notebook/scripts/share_notebook.py --notebook-id "ID" --email "user@example.com" --role "READER"
```

---

### Workflow 6: Add Sources

**Triggers:** "add sources", "add to notebook", "add url", "add youtube", "add drive file"

**Action:**
```bash
# For web URL
uv run python 00-system/skills/notebooklm/notebooklm-add-sources/scripts/add_sources.py --notebook-id "ID" --type web --url "https://..."

# For YouTube
uv run python 00-system/skills/notebooklm/notebooklm-add-sources/scripts/add_sources.py --notebook-id "ID" --type youtube --url "https://youtube.com/..."

# For text
uv run python 00-system/skills/notebooklm/notebooklm-add-sources/scripts/add_sources.py --notebook-id "ID" --type text --content "Your text..."

# For Google Drive
uv run python 00-system/skills/notebooklm/notebooklm-add-sources/scripts/add_sources.py --notebook-id "ID" --type drive --resource-id "DRIVE_FILE_ID"
```

---

### Workflow 7: Upload File

**Triggers:** "upload file", "upload pdf", "add file", "upload document"

**Action:**
```bash
uv run python 00-system/skills/notebooklm/notebooklm-upload-file/scripts/upload_file.py --notebook-id "ID" --file "/path/to/file.pdf"
```

---

### Workflow 8: Get Source Details

**Triggers:** "get source", "source details", "show source"

**Action:**
```bash
uv run python 00-system/skills/notebooklm/notebooklm-get-source/scripts/get_source.py --notebook-id "ID" --source-id "SOURCE_ID"
```

---

### Workflow 9: Delete Sources

**Triggers:** "delete sources", "remove sources", "clear sources"

**Action:**
```bash
uv run python 00-system/skills/notebooklm/notebooklm-delete-sources/scripts/delete_sources.py --notebook-id "ID" --source-ids "S1,S2"
```

---

### Workflow 10: Create Audio Overview

**Triggers:** "create audio", "generate podcast", "audio overview", "make podcast"

**Action:**
```bash
uv run python 00-system/skills/notebooklm/notebooklm-create-audio/scripts/create_audio.py --notebook-id "ID" [--focus "Topic focus"] [--language "en"]
```

---

### Workflow 11: Delete Audio Overview

**Triggers:** "delete audio", "remove podcast", "delete audio overview"

**Action:**
```bash
uv run python 00-system/skills/notebooklm/notebooklm-delete-audio/scripts/delete_audio.py --notebook-id "ID"
```

---

## Common Patterns

### Create notebook and add sources

```bash
# 1. Create notebook
uv run python .../create_notebook.py --title "Research Project"
# Returns: notebookId: abc123

# 2. Add sources
uv run python .../add_sources.py --notebook-id abc123 --type web --url "https://..."
uv run python .../upload_file.py --notebook-id abc123 --file "/path/to/paper.pdf"

# 3. Generate audio
uv run python .../create_audio.py --notebook-id abc123 --focus "Key findings"
```

### Full research workflow

1. Create notebook with descriptive title
2. Add multiple sources (PDFs, URLs, YouTube)
3. Wait for sources to process
4. Generate audio overview
5. Share with team

---

## Error Handling

On any error, load appropriate reference:

| Error Type | Reference to Load |
|------------|-------------------|
| Authentication | `notebooklm-master/references/authentication.md` |
| Permission denied | `notebooklm-master/references/setup-guide.md` |
| API errors | `notebooklm-master/references/error-handling.md` |
| Unknown | `notebooklm-master/references/api-reference.md` |

---

## Context Caching

After listing notebooks, cache the IDs for quick reference:

```yaml
cached_notebooks:
  - id: abc123
    title: "Research Project"
  - id: def456
    title: "Meeting Notes"
```

When user says "add to Research Project", use cached ID.

---

**Version**: 1.0
**Created**: 2025-12-27
