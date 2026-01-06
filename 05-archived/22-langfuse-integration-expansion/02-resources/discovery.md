# Discovery: Project 22 - Langfuse Integration Expansion

**Time**: ~10 min discovery
**Date**: 2026-01-04

---

## 1. Dependencies (Files/Systems This Project Will Touch)

### Files to Modify

| File | What Changes |
|------|--------------|
| `03-skills/langfuse/langfuse-connect/SKILL.md` | Add routing for 59 new endpoints in routing table |
| `03-skills/langfuse/langfuse-master/SKILL.md` | Update related skills list |
| `03-skills/langfuse/langfuse-master/references/api-reference.md` | Document all new endpoints |
| `03-skills/langfuse/langfuse-master/scripts/langfuse_client.py` | Add `patch()` and `put()` methods (currently only has GET, POST, DELETE) |

### New Files to Create (59 skills)

| Category | Skills (folders in `03-skills/langfuse/`) |
|----------|-------------------------------------------|
| **Prompts (5)** | `langfuse-list-prompts/`, `langfuse-create-prompt/`, `langfuse-get-prompt/`, `langfuse-delete-prompt/`, `langfuse-update-prompt-version/` |
| **Datasets (6)** | `langfuse-list-datasets/`, `langfuse-create-dataset/`, `langfuse-get-dataset/`, `langfuse-list-dataset-runs/`, `langfuse-get-dataset-run/`, `langfuse-delete-dataset-run/` |
| **Dataset Items (4)** | `langfuse-list-dataset-items/`, `langfuse-create-dataset-item/`, `langfuse-get-dataset-item/`, `langfuse-delete-dataset-item/` |
| **Dataset Run Items (2)** | `langfuse-list-dataset-run-items/`, `langfuse-create-dataset-run-item/` |
| **Score Configs (4)** | `langfuse-list-score-configs/`, `langfuse-create-score-config/`, `langfuse-get-score-config/`, `langfuse-update-score-config/` |
| **Scores Write (2)** | `langfuse-create-score/`, `langfuse-delete-score/` |
| **Annotation Queues (10)** | Queue CRUD + item management + assignments |
| **Comments (3)** | `langfuse-list-comments/`, `langfuse-create-comment/`, `langfuse-get-comment/` |
| **Ingestion (2)** | `langfuse-batch-ingest/`, `langfuse-otel-ingest/` |
| **Media (3)** | `langfuse-get-media/`, `langfuse-update-media/`, `langfuse-get-upload-url/` |
| **Traces Write (2)** | `langfuse-delete-trace/`, `langfuse-delete-traces/` |
| **Models Write (2)** | `langfuse-create-model/`, `langfuse-delete-model/` |
| **Projects Admin (6)** | Project CRUD + API key management |
| **Organizations (5)** | Membership + projects + API keys |
| **Utilities (2)** | `langfuse-health/`, `langfuse-metrics/` |

### External Systems

| System | How We Connect |
|--------|---------------|
| **Langfuse API** | Self-hosted at `https://tracing.beamstudio.ai` |
| **Authentication** | Basic Auth via `LANGFUSE_PUBLIC_KEY` / `LANGFUSE_SECRET_KEY` env vars |

---

## 2. Existing Patterns to Reuse

### Pattern: Skill Folder Structure
From existing skills (e.g., `langfuse-list-traces/`):
```
langfuse-{operation}/
├── SKILL.md          # YAML frontmatter + usage docs
└── scripts/
    └── {operation}.py  # Imports langfuse_client, implements API call
```

### Pattern: Script Template
From `langfuse-list-traces/scripts/list_traces.py`:
```python
#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "langfuse-master" / "scripts"))
from langfuse_client import get_client

def main():
    client = get_client()
    result = client.get("/traces", params={...})
    print(json.dumps(result, indent=2))
```

### Pattern: SKILL.md Template
From existing skills:
```yaml
---
name: langfuse-{operation}
description: "{Description}. Load when user says '{triggers}'."
---
```

### Pattern: Connect Routing Table
From `langfuse-connect/SKILL.md`:
```markdown
| User Says | Skill to Load | Endpoint |
|-----------|---------------|----------|
| "list traces" | langfuse-list-traces | GET /traces |
```

### Pattern: langfuse_client.py Methods
**Current methods**:
- `get(endpoint, params)` - For list/get operations
- `post(endpoint, data)` - For create operations
- `delete(endpoint, params)` - For delete operations

**Missing methods (need to add)**:
- `patch(endpoint, data)` - For partial updates (PATCH)
- `put(endpoint, data)` - For full updates (PUT)

---

## 3. Risks & Unknowns

### High Risk: Client Missing PATCH/PUT Methods
**Issue**: `langfuse_client.py` only has GET, POST, DELETE. PATCH is needed for:
- `langfuse-update-prompt-version` (PATCH /v2/prompts/{name}/versions/{version})
- `langfuse-update-score-config` (PATCH /score-configs/{id})
- `langfuse-update-queue-item` (PATCH /annotation-queues/{id}/items/{itemId})
- `langfuse-update-media` (PATCH /media/{id})

PUT is needed for:
- `langfuse-update-project` (PUT /projects/{id})
- `langfuse-update-org-membership` (PUT /organizations/memberships)

**Mitigation**: Add `patch()` and `put()` methods to `langfuse_client.py` BEFORE creating skills that need them.

### Medium Risk: Plan.md Says Wrong Location
**Issue**: plan.md says files are in `03-skills/langfuse/` but references say `00-system/skills/langfuse/`

**Reality Check**: Files are actually in `03-skills/langfuse/` (confirmed by Glob)

**Mitigation**:
- Use `03-skills/langfuse/` as correct path
- langfuse-connect SKILL.md has wrong script paths (uses `00-system/skills/langfuse/`)
- Need to update these paths OR keep using 00-system paths (check which works)

### Medium Risk: Self-Hosted API Availability
**Issue**: Some admin endpoints may be Cloud-only (Organizations, SCIM)

**Mitigation**:
- Test each endpoint against self-hosted instance
- Document Cloud-only limitations in api-reference.md
- Mark skills as "Cloud-only" if needed

### Low Risk: v1 vs v2 API Endpoints
**Issue**: Some endpoints have v2 versions (e.g., `/v2/prompts`, `/v2/observations`)

**Mitigation**:
- Always prefer v2 where available
- Document which version each skill uses

### Unknown: Existing Tests
**Discovery**: Tests exist at `03-skills/langfuse/tests/`:
- `test_langfuse_client.py`
- `test_config_check.py`
- `test_integration.py`
- `test_api_endpoints.py`

**Action**: Review existing test patterns and extend for new endpoints.

---

## 4. Quick Wins & First Steps

### Immediate Actions Before Phase 1

1. **Fix langfuse_client.py** - Add `patch()` and `put()` methods
2. **Verify script paths** - Check if `00-system/skills/langfuse/` or `03-skills/langfuse/` is correct in langfuse-connect routing

### First Skill to Create (Validation)
Start with `langfuse-list-prompts/` because:
- GET request (no client changes needed)
- Simple to verify against live instance
- Validates pattern before creating 58 more skills

---

## Auto-Populate for plan.md Dependencies

Based on this discovery, here's what should go in plan.md Dependencies:

**Files Impacted**:
- `03-skills/langfuse/langfuse-master/scripts/langfuse_client.py` - Add PATCH/PUT methods
- `03-skills/langfuse/langfuse-connect/SKILL.md` - Add 59 new routes
- `03-skills/langfuse/langfuse-master/references/api-reference.md` - Document new endpoints

**External Systems**:
- Langfuse API at https://tracing.beamstudio.ai (self-hosted)

**Related Projects**:
- Project 08: Langfuse Integration (COMPLETE) - Foundation with 11 endpoints

**Existing Infrastructure to Reuse**:
- `langfuse_client.py` - API client (needs PATCH/PUT additions)
- `check_langfuse_config.py` - Config validator
- Test suite in `03-skills/langfuse/tests/`

---

## Next Steps

1. Add `patch()` and `put()` methods to `langfuse_client.py`
2. Create `langfuse-list-prompts/` skill as validation
3. Test against live Langfuse instance
4. If successful, batch-create remaining Phase 1 skills (16 more)
