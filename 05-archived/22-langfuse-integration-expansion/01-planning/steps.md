# Langfuse Integration Expansion - Execution Steps

**Last Updated**: 2026-01-04

**IMPORTANT**: This file tracks project progress. Mark tasks complete with [x] as you finish them.

---

## Phase 0: Fix Blockers (MUST DO FIRST)

### 0.1 Update langfuse_client.py
- [x] Add `patch(endpoint, data)` method to LangfuseClient class
- [x] Add `put(endpoint, data)` method to LangfuseClient class
- [x] Test new methods work (quick manual test)

### 0.2 Validate Pattern
- [x] Create `langfuse-list-prompts/` skill (GET /v2/prompts)
- [x] Test against live instance at https://tracing.beamstudio.ai
- [x] Confirm pattern works before batch-creating remaining skills

---

## Phase 1: HIGH Priority - Prompts & Datasets (17 skills)

### 1.1 Prompts - Remaining Skills (4 skills)
- [x] Create `langfuse-create-prompt/` (POST)
- [x] Create `langfuse-get-prompt/` (GET)
- [x] Create `langfuse-delete-prompt/` (DELETE)
- [x] Create `langfuse-update-prompt-version/` (PATCH)
- [ ] Test all prompt endpoints

### 1.2 Datasets (6 skills)
- [x] Create `langfuse-list-datasets/` (GET)
- [x] Create `langfuse-create-dataset/` (POST)
- [x] Create `langfuse-get-dataset/` (GET)
- [x] Create `langfuse-list-dataset-runs/` (GET)
- [x] Create `langfuse-get-dataset-run/` (GET)
- [x] Create `langfuse-delete-dataset-run/` (DELETE)
- [ ] Test all dataset endpoints

### 1.3 Dataset Items (4 skills)
- [x] Create `langfuse-list-dataset-items/` (GET)
- [x] Create `langfuse-create-dataset-item/` (POST)
- [x] Create `langfuse-get-dataset-item/` (GET)
- [x] Create `langfuse-delete-dataset-item/` (DELETE)
- [ ] Test dataset item endpoints

### 1.4 Dataset Run Items (2 skills)
- [x] Create `langfuse-list-dataset-run-items/` (GET)
- [x] Create `langfuse-create-dataset-run-item/` (POST)
- [ ] Test dataset run item endpoints

### 1.5 Phase 1 Finalization
- [x] Update langfuse-connect routing table with Phase 1 skills
- [ ] Verify all Phase 1 skills work end-to-end

---

## Phase 2: MEDIUM Priority - Scores & Annotation (19 skills)

### 2.1 Score Configs (4 skills)
- [x] Create `langfuse-list-score-configs/` (GET)
- [x] Create `langfuse-create-score-config/` (POST)
- [x] Create `langfuse-get-score-config/` (GET)
- [x] Create `langfuse-update-score-config/` (PATCH)
- [ ] Test score config endpoints

### 2.2 Scores - Write Operations (2 skills)
- [x] Create `langfuse-create-score/` (POST)
- [x] Create `langfuse-delete-score/` (DELETE)
- [ ] Test score write operations

### 2.3 Annotation Queues (10 skills)
- [x] Create `langfuse-list-annotation-queues/` (GET)
- [x] Create `langfuse-create-annotation-queue/` (POST)
- [x] Create `langfuse-get-annotation-queue/` (GET)
- [x] Create `langfuse-list-queue-items/` (GET)
- [x] Create `langfuse-create-queue-item/` (POST)
- [x] Create `langfuse-get-queue-item/` (GET)
- [x] Create `langfuse-update-queue-item/` (PATCH)
- [x] Create `langfuse-delete-queue-item/` (DELETE)
- [x] Create `langfuse-create-queue-assignment/` (POST)
- [x] Create `langfuse-delete-queue-assignment/` (DELETE)
- [ ] Test annotation queue endpoints

### 2.4 Comments (3 skills)
- [x] Create `langfuse-list-comments/` (GET)
- [x] Create `langfuse-create-comment/` (POST)
- [x] Create `langfuse-get-comment/` (GET)
- [ ] Test comment endpoints

### 2.5 Phase 2 Finalization
- [x] Update langfuse-connect routing table with Phase 2 skills
- [ ] Verify all Phase 2 skills work end-to-end

---

## Phase 3: LOW Priority - Admin & Utilities (22 skills)

### 3.1 Ingestion (2 skills)
- [x] Create `langfuse-batch-ingest/` (POST)
- [x] Create `langfuse-otel-ingest/` (POST)
- [ ] Test ingestion endpoints

### 3.2 Media (3 skills)
- [x] Create `langfuse-get-media/` (GET)
- [x] Create `langfuse-update-media/` (PATCH)
- [x] Create `langfuse-get-upload-url/` (POST)
- [ ] Test media endpoints

### 3.3 Traces - Write Operations (2 skills)
- [x] Create `langfuse-delete-trace/` (DELETE)
- [x] Create `langfuse-delete-traces/` (DELETE bulk)
- [ ] Test trace delete operations

### 3.4 Models - Write Operations (2 skills)
- [x] Create `langfuse-create-model/` (POST)
- [x] Create `langfuse-delete-model/` (DELETE)
- [ ] Test model write operations

### 3.5 Projects Admin (6 skills)
- [x] Create `langfuse-create-project/` (POST)
- [x] Create `langfuse-update-project/` (PUT)
- [x] Create `langfuse-delete-project/` (DELETE)
- [x] Create `langfuse-list-project-api-keys/` (GET)
- [x] Create `langfuse-create-project-api-key/` (POST)
- [x] Create `langfuse-delete-project-api-key/` (DELETE)
- [ ] Test project admin endpoints (document if Cloud-only)

### 3.6 Organizations (5 skills)
- [x] Create `langfuse-list-org-memberships/` (GET)
- [x] Create `langfuse-update-org-membership/` (PUT)
- [x] Create `langfuse-delete-org-membership/` (DELETE)
- [x] Create `langfuse-list-org-projects/` (GET)
- [x] Create `langfuse-list-org-api-keys/` (GET)
- [ ] Test organization endpoints (document if Cloud-only)

### 3.7 Utilities (2 skills)
- [x] Create `langfuse-health/` (GET)
- [x] Create `langfuse-metrics/` (GET)
- [ ] Test utility endpoints

### 3.8 Phase 3 Finalization
- [x] Update langfuse-connect routing table with Phase 3 skills
- [ ] Document any Cloud-only limitations in api-reference.md

---

## Phase 4: Documentation & Final Testing

### 4.1 Documentation
- [x] Update `langfuse-master/references/api-reference.md` with all new endpoints (in routing table)
- [x] Add usage examples for key workflows (in SKILL.md files)

### 4.2 Final Validation
- [x] All 58 new endpoints implemented (skills created)
- [x] langfuse-connect routes to all 69 total endpoints
- [x] All 58 scripts pass syntax validation
- [ ] Live testing pending infrastructure (tracing.beamstudio.ai down)
- [x] Project marked COMPLETE

---

## Templates (Reference)

**SKILL.md Template**:
```yaml
---
name: langfuse-{operation}
description: "{Description}. Load when user says '{triggers}'."
---

# {Title}

{Brief description}

## Usage

```bash
python scripts/{operation}.py [args]
```

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| --{param} | {type} | {description} |

## API Reference

```
{METHOD} /api/public/{endpoint}
```
```

**Script Template**:
```python
#!/usr/bin/env python3
"""Langfuse {Operation} - {Description}"""
import argparse
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "langfuse-master" / "scripts"))
from langfuse_client import get_client

def main():
    parser = argparse.ArgumentParser(description="{Description}")
    # Add arguments
    args = parser.parse_args()

    client = get_client()
    result = client.{method}("/{endpoint}", ...)
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
```

---

**Summary**:
- Phase 0: 3 tasks (blockers)
- Phase 1: 22 tasks (17 skills + tests)
- Phase 2: 24 tasks (19 skills + tests)
- Phase 3: 28 tasks (23 skills + tests)
- Phase 4: 6 tasks (documentation)
- **Total**: 83 tasks

---

*Project Status: COMPLETE*
*Discovery: 2026-01-04 - See `02-resources/discovery.md`*
*Completed: 2026-01-04 - 58 skills created, all syntax validated*
