# Langfuse Integration Expansion - Plan

**Last Updated**: 2026-01-04

---

## Approach

Extend the existing Langfuse integration in `03-skills/langfuse/` following the established pattern:

1. **Fix client first** - Add `patch()` and `put()` methods to `langfuse_client.py` (BLOCKER)
2. **Validate with one skill** - Create `langfuse-list-prompts/` to confirm pattern works
3. **Batch-create by category** - Group similar endpoints for efficient creation
4. **Update routing incrementally** - Add to langfuse-connect after each category

**Pattern per endpoint**:
```
03-skills/langfuse/langfuse-{operation}/
├── SKILL.md          # Trigger phrases, workflow
└── scripts/
    └── {operation}.py  # API call implementation
```

---

## Key Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| **Skill location** | `03-skills/langfuse/` | Extend existing structure (confirmed by discovery) |
| **v2 vs v1 API** | v2 where available | Better performance, cursor pagination |
| **Script pattern** | Reuse `langfuse_client.py` | DRY, consistent error handling |
| **Skill granularity** | One skill per endpoint | Matches Project 08 pattern |
| **Batching** | Group by HTTP method | GET-only first, then POST, then PATCH/PUT/DELETE |
| **Validation** | Test after each category | Catch issues early, not at end |

---

## Resources Needed

**Tools/Access**:
- Existing Langfuse credentials (already configured)
- Python 3.x with requests library (already available)
- Live instance at https://tracing.beamstudio.ai

**Information/Data**:
- OpenAPI spec: https://cloud.langfuse.com/generated/api/openapi.yml
- API reference: https://api.reference.langfuse.com/

---

## Dependencies & Links (from Discovery)

**Files to Modify FIRST** (Blockers):
- `03-skills/langfuse/langfuse-master/scripts/langfuse_client.py` - Add `patch()` and `put()` methods

**Files to Extend**:
- `03-skills/langfuse/langfuse-connect/SKILL.md` - Add routing for 59 new operations
- `03-skills/langfuse/langfuse-master/references/api-reference.md` - Document new endpoints

**Existing Infrastructure to Reuse**:
- `03-skills/langfuse/langfuse-master/scripts/langfuse_client.py` - API client (needs PATCH/PUT)
- `03-skills/langfuse/langfuse-master/scripts/check_langfuse_config.py` - Config validator
- `03-skills/langfuse/tests/` - Existing test suite to extend

**Related Projects**:
- Project 08: Langfuse Integration (COMPLETE) - Foundation with 11 endpoints

---

## New Skills to Create (59 total)

### Phase 1: HIGH Priority (17 skills)

**Prompts (5 skills)**:
| Skill | Endpoint | Method |
|-------|----------|--------|
| langfuse-list-prompts | /api/public/v2/prompts | GET |
| langfuse-create-prompt | /api/public/v2/prompts | POST |
| langfuse-get-prompt | /api/public/v2/prompts/{name} | GET |
| langfuse-delete-prompt | /api/public/v2/prompts/{name} | DELETE |
| langfuse-update-prompt-version | /api/public/v2/prompts/{name}/versions/{version} | PATCH |

**Datasets (6 skills)**:
| Skill | Endpoint | Method |
|-------|----------|--------|
| langfuse-list-datasets | /api/public/v2/datasets | GET |
| langfuse-create-dataset | /api/public/v2/datasets | POST |
| langfuse-get-dataset | /api/public/v2/datasets/{name} | GET |
| langfuse-list-dataset-runs | /api/public/datasets/{name}/runs | GET |
| langfuse-get-dataset-run | /api/public/datasets/{name}/runs/{runName} | GET |
| langfuse-delete-dataset-run | /api/public/datasets/{name}/runs/{runName} | DELETE |

**Dataset Items (4 skills)**:
| Skill | Endpoint | Method |
|-------|----------|--------|
| langfuse-list-dataset-items | /api/public/dataset-items | GET |
| langfuse-create-dataset-item | /api/public/dataset-items | POST |
| langfuse-get-dataset-item | /api/public/dataset-items/{id} | GET |
| langfuse-delete-dataset-item | /api/public/dataset-items/{id} | DELETE |

**Dataset Run Items (2 skills)**:
| Skill | Endpoint | Method |
|-------|----------|--------|
| langfuse-list-dataset-run-items | /api/public/dataset-run-items | GET |
| langfuse-create-dataset-run-item | /api/public/dataset-run-items | POST |

### Phase 2: MEDIUM Priority (19 skills)

**Score Configs (4 skills)**:
| Skill | Endpoint | Method |
|-------|----------|--------|
| langfuse-list-score-configs | /api/public/score-configs | GET |
| langfuse-create-score-config | /api/public/score-configs | POST |
| langfuse-get-score-config | /api/public/score-configs/{id} | GET |
| langfuse-update-score-config | /api/public/score-configs/{id} | PATCH |

**Scores - Write Operations (2 skills)**:
| Skill | Endpoint | Method |
|-------|----------|--------|
| langfuse-create-score | /api/public/scores | POST |
| langfuse-delete-score | /api/public/scores/{id} | DELETE |

**Annotation Queues (10 skills)**:
| Skill | Endpoint | Method |
|-------|----------|--------|
| langfuse-list-annotation-queues | /api/public/annotation-queues | GET |
| langfuse-create-annotation-queue | /api/public/annotation-queues | POST |
| langfuse-get-annotation-queue | /api/public/annotation-queues/{id} | GET |
| langfuse-list-queue-items | /api/public/annotation-queues/{id}/items | GET |
| langfuse-create-queue-item | /api/public/annotation-queues/{id}/items | POST |
| langfuse-get-queue-item | /api/public/annotation-queues/{id}/items/{itemId} | GET |
| langfuse-update-queue-item | /api/public/annotation-queues/{id}/items/{itemId} | PATCH |
| langfuse-delete-queue-item | /api/public/annotation-queues/{id}/items/{itemId} | DELETE |
| langfuse-create-queue-assignment | /api/public/annotation-queues/{id}/assignments | POST |
| langfuse-delete-queue-assignment | /api/public/annotation-queues/{id}/assignments | DELETE |

**Comments (3 skills)**:
| Skill | Endpoint | Method |
|-------|----------|--------|
| langfuse-list-comments | /api/public/comments | GET |
| langfuse-create-comment | /api/public/comments | POST |
| langfuse-get-comment | /api/public/comments/{id} | GET |

### Phase 3: LOW Priority (23 skills)

**Ingestion (2 skills)**:
| Skill | Endpoint | Method |
|-------|----------|--------|
| langfuse-batch-ingest | /api/public/ingestion | POST |
| langfuse-otel-ingest | /api/public/otel/v1/traces | POST |

**Media (3 skills)**:
| Skill | Endpoint | Method |
|-------|----------|--------|
| langfuse-get-media | /api/public/media/{id} | GET |
| langfuse-update-media | /api/public/media/{id} | PATCH |
| langfuse-get-upload-url | /api/public/media | POST |

**Traces - Write Operations (2 skills)**:
| Skill | Endpoint | Method |
|-------|----------|--------|
| langfuse-delete-trace | /api/public/traces/{id} | DELETE |
| langfuse-delete-traces | /api/public/traces | DELETE |

**Models - Write Operation (1 skill)**:
| Skill | Endpoint | Method |
|-------|----------|--------|
| langfuse-create-model | /api/public/models | POST |
| langfuse-delete-model | /api/public/models/{id} | DELETE |

**Projects Admin (7 skills)**:
| Skill | Endpoint | Method |
|-------|----------|--------|
| langfuse-create-project | /api/public/projects | POST |
| langfuse-update-project | /api/public/projects/{id} | PUT |
| langfuse-delete-project | /api/public/projects/{id} | DELETE |
| langfuse-list-project-api-keys | /api/public/projects/{id}/apiKeys | GET |
| langfuse-create-project-api-key | /api/public/projects/{id}/apiKeys | POST |
| langfuse-delete-project-api-key | /api/public/projects/{id}/apiKeys/{keyId} | DELETE |

**Organizations (6 skills)**:
| Skill | Endpoint | Method |
|-------|----------|--------|
| langfuse-list-org-memberships | /api/public/organizations/memberships | GET |
| langfuse-update-org-membership | /api/public/organizations/memberships | PUT |
| langfuse-delete-org-membership | /api/public/organizations/memberships | DELETE |
| langfuse-list-org-projects | /api/public/organizations/projects | GET |
| langfuse-list-org-api-keys | /api/public/organizations/apiKeys | GET |

**Utilities (2 skills)**:
| Skill | Endpoint | Method |
|-------|----------|--------|
| langfuse-health | /api/public/health | GET |
| langfuse-metrics | /api/public/v2/metrics | GET |

---

## Open Questions

- [x] Where are existing skills? → `03-skills/langfuse/` (confirmed)
- [x] What pattern to follow? → One skill per endpoint with scripts/
- [x] Does client support all HTTP methods? → **NO** - needs PATCH/PUT (BLOCKER)
- [ ] Are all endpoints available on self-hosted? → Test during Phase 3
- [ ] Rate limits for write operations? → Test during implementation

---

## Risks (from Discovery)

| Risk | Severity | Mitigation |
|------|----------|------------|
| Client missing PATCH/PUT | HIGH | Fix in Phase 0 before any skills |
| Self-hosted API limitations | MEDIUM | Test admin endpoints, document Cloud-only |
| 59 skills is tedious | LOW | Batch-create by category, validate pattern first |

---

## Mental Models Applied

**Fix Dependencies First**:
- Resolve `langfuse_client.py` blocker before creating skills
- Validate with one skill before batch-creating 58 more

**Incremental Delivery**:
- Phase by priority ensures usable integration at each milestone
- HIGH priority (prompts, datasets) unlocks core workflows immediately

**DRY Principle**:
- Reuse existing `langfuse_client.py` for all new endpoints
- Consistent error handling across all operations

---

*Discovery completed: 2026-01-04 - See `02-resources/discovery.md`*
