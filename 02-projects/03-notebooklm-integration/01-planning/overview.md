---
id: 03-notebooklm-integration
name: NotebookLM Integration
status: PLANNING
description: "Load when user mentions 'notebooklm', 'notebook lm', 'create notebook', 'audio overview', 'podcast', 'add sources to notebook'"
created: 2025-12-27
---

# NotebookLM Integration

Build complete NotebookLM Enterprise integration following the master/connect/specialized pattern.

## Scope

- **Service**: NotebookLM Enterprise (Google Cloud)
- **Base URL**: `https://{ENDPOINT_LOCATION}-discoveryengine.googleapis.com/v1alpha/`
- **Auth Type**: OAuth 2.0 Bearer Token (via gcloud)
- **Endpoints**: 11 selected

## Architecture

Will create:
- `notebooklm-master/` - Shared resources (client, auth, error handling)
- `notebooklm-connect/` - Meta-skill entry point
- 11 operation skills (one per endpoint)

## API Discovery

- **API Docs**: https://docs.cloud.google.com/gemini/enterprise/notebooklm-enterprise/docs/api-notebooks
- **Sources Docs**: https://docs.cloud.google.com/gemini/enterprise/notebooklm-enterprise/docs/api-notebooks-sources
- **Audio Docs**: https://docs.cloud.google.com/gemini/enterprise/notebooklm-enterprise/docs/api-audio-overview

## Endpoints to Implement

### Notebooks (5)
1. POST /notebooks - Create notebook
2. GET /notebooks/{id} - Get notebook
3. GET /notebooks:listRecentlyViewed - List recently viewed
4. POST /notebooks:batchDelete - Batch delete notebooks
5. POST /notebooks/{id}:share - Share notebook

### Sources (4)
6. POST /notebooks/{id}/sources:batchCreate - Add sources (Drive, text, web, YouTube)
7. POST /notebooks/{id}/sources:uploadFile - Upload file (PDF, TXT, MD, audio, images)
8. GET /notebooks/{id}/sources/{sourceId} - Get source details
9. POST /notebooks/{id}/sources:batchDelete - Delete sources

### Audio Overview (2)
10. POST /notebooks/{id}/audioOverviews - Create audio overview (podcast)
11. DELETE /notebooks/{id}/audioOverviews/default - Delete audio overview

## References

- Pattern: See 00-system/skills/system/add-integration/references/integration-architecture.md
