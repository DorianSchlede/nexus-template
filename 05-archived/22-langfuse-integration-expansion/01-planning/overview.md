---
id: 22-langfuse-integration-expansion
name: Langfuse Integration Expansion
status: COMPLETE
description: "Load when user mentions 'langfuse prompts', 'langfuse datasets', 'langfuse experiments', 'annotation queues', 'langfuse comments', 'langfuse media', 'score configs', 'langfuse admin'"
created: 2026-01-03
completed: 2026-01-04
---

# Langfuse Integration Expansion

## Purpose

Expand the existing Langfuse integration (Project 08) from 11 read-only endpoints to **full API coverage** with 59 additional endpoints. This enables complete programmatic control over Langfuse for prompt management, dataset experiments, annotation workflows, and administrative operations.

**Current State** (Project 08):
- 11 GET endpoints (traces, observations, sessions, scores, models, projects)
- Read-only access
- Basic querying capabilities

**Target State** (This Project):
- 70+ total endpoints across 20 categories
- Full CRUD operations (Create, Read, Update, Delete)
- Prompt versioning, dataset experiments, annotation queues
- Admin/org management capabilities

---

## Success Criteria

**Must achieve**:
- [ ] All 59 new endpoints implemented with working scripts
- [ ] Complete CRUD for: Prompts, Datasets, Scores, Annotation Queues
- [ ] All scripts tested against live Langfuse instance
- [ ] Consistent pattern with existing langfuse-master architecture
- [ ] Updated langfuse-connect routing table

**Nice to have**:
- [ ] Unit tests for new endpoints
- [ ] Example workflows documented
- [ ] v2 API preference where available

---

## Context

**Background**: Project 08 built the foundation with 11 GET endpoints. The Langfuse API has expanded significantly with prompt management, datasets for experiments, annotation queues for human review, and administrative APIs. These are needed for full observability workflows.

**Stakeholders**:
- Dev team using Langfuse for LLM tracing
- Prompt engineers needing version control
- QA team doing evaluation experiments

**Constraints**:
- Must extend existing `00-system/skills/langfuse/` structure
- Follow master/connect/specialized pattern
- Self-hosted instance at https://tracing.beamstudio.ai
- Basic Auth with existing env vars

---

## Scope - New Endpoints (59 total)

| Category | Endpoints | Priority |
|----------|-----------|----------|
| **Prompts** | 5 endpoints (CRUD + versioning) | HIGH |
| **Datasets** | 6 endpoints (create, list, runs) | HIGH |
| **Dataset Items** | 4 endpoints (CRUD) | HIGH |
| **Dataset Run Items** | 2 endpoints (create, list) | HIGH |
| **Score Configs** | 4 endpoints (CRUD) | MEDIUM |
| **Annotation Queues** | 10 endpoints (full workflow) | MEDIUM |
| **Comments** | 3 endpoints (CRUD) | MEDIUM |
| **Ingestion** | 2 endpoints (batch, OTEL) | MEDIUM |
| **Media** | 3 endpoints (upload, get, patch) | LOW |
| **Organizations** | 8 endpoints (admin) | LOW |
| **Projects Admin** | 7 endpoints (keys, CRUD) | LOW |
| **SCIM** | 7 endpoints (user provisioning) | LOW |
| **Blob Storage** | 3 endpoints | LOW |
| **LLM Connections** | 2 endpoints | LOW |
| **Health** | 1 endpoint | LOW |

---

## Timeline

**Target**: Complete in phases over multiple sessions

**Milestones**:
- Phase 1: Prompts + Datasets (HIGH priority)
- Phase 2: Scores + Annotation Queues (MEDIUM priority)
- Phase 3: Admin + Utilities (LOW priority)

---

*Next: Complete plan.md to define approach and dependencies*
