---
name: notebooklm
description: "Triggers: notebooklm, create notebook, audio overview, podcast."
---

# NotebookLM Integration

Complete integration for Google NotebookLM Enterprise API.

## Quick Start

Say any of these:
- "create notebook [title]"
- "list my notebooks"
- "add [url] to notebook"
- "upload [file] to notebook"
- "create audio overview"
- "generate podcast"

## Available Operations

### Notebooks
- **Create notebook** - Create a new notebook
- **List notebooks** - List recently viewed notebooks
- **Get notebook** - Get notebook details
- **Delete notebooks** - Delete one or more notebooks
- **Share notebook** - Share with other users

### Sources
- **Add sources** - Add from web URL, YouTube, Google Drive, or text
- **Upload file** - Upload PDF, TXT, MD, DOCX, audio, images
- **Get source** - Get source details
- **Delete sources** - Remove sources from notebook

### Audio Overview
- **Create audio** - Generate podcast-style audio overview
- **Delete audio** - Remove audio overview

## Setup Required

NotebookLM Enterprise requires:
1. Google Cloud project with NotebookLM Enterprise enabled
2. gcloud CLI installed and authenticated
3. Project number in `.env`

Run setup:
```bash
python 00-system/skills/notebooklm/notebooklm-master/scripts/setup_notebooklm.py
```

## Architecture

```
notebooklm/
├── notebooklm-master/      # Shared resources (DO NOT load directly)
├── notebooklm-connect/     # Meta-skill (entry point)
├── notebooklm-create-notebook/
├── notebooklm-list-notebooks/
├── notebooklm-get-notebook/
├── notebooklm-delete-notebooks/
├── notebooklm-share-notebook/
├── notebooklm-add-sources/
├── notebooklm-upload-file/
├── notebooklm-get-source/
├── notebooklm-delete-sources/
├── notebooklm-create-audio/
└── notebooklm-delete-audio/
```

---

**Version**: 1.0
**Created**: 2025-12-27
