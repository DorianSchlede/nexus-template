---
name: langfuse-connect
description: "langfuse, traces, observations, llm tracing."
---

# Langfuse Connect

User-facing entry point for Langfuse integration. Routes to appropriate operation skills.

## Context Reference

For score config IDs, trace structure, and API patterns, load:
```bash
python 00-system/core/nexus-loader.py --skill langfuse-help
```

---

## Pre-Flight Check (ALWAYS FIRST)

Before any operation, run config check:

```bash
python 00-system/skills/langfuse/langfuse-master/scripts/check_langfuse_config.py --json
```

**If `ai_action` is:**
- `proceed_with_operation` → Continue with requested operation
- `prompt_for_api_key` → Ask user for credentials, guide to setup

---

## Routing Table

### Core Operations (Project 08)

| User Says | Skill to Load | Endpoint |
|-----------|---------------|----------|
| "list traces", "show traces", "get traces" | langfuse-list-traces | GET /traces |
| "get trace {id}", "trace details" | langfuse-get-trace | GET /traces/{id} |
| "list observations", "show spans" | langfuse-list-observations | GET /v2/observations |
| "get observation {id}" | langfuse-get-observation | GET /observations/{id} |
| "list sessions", "show sessions" | langfuse-list-sessions | GET /sessions |
| "get session {id}" | langfuse-get-session | GET /sessions/{id} |
| "list scores", "show evaluations" | langfuse-list-scores | GET /v2/scores |
| "get score {id}" | langfuse-get-score | GET /v2/scores/{id} |
| "list models", "model costs" | langfuse-list-models | GET /models |
| "get model {id}" | langfuse-get-model | GET /models/{id} |
| "get project", "current project" | langfuse-get-project | GET /projects |

### Prompts (Phase 1)

| User Says | Skill to Load | Endpoint |
|-----------|---------------|----------|
| "list prompts", "show prompts" | langfuse-list-prompts | GET /v2/prompts |
| "create prompt", "new prompt" | langfuse-create-prompt | POST /v2/prompts |
| "get prompt {name}", "show prompt" | langfuse-get-prompt | GET /v2/prompts/{name} |
| "delete prompt", "remove prompt" | langfuse-delete-prompt | DELETE /v2/prompts/{name} |
| "update prompt", "set prompt label" | langfuse-update-prompt-version | PATCH /v2/prompts/{name}/versions/{v} |

### Datasets (Phase 1)

| User Says | Skill to Load | Endpoint |
|-----------|---------------|----------|
| "list datasets", "show datasets" | langfuse-list-datasets | GET /v2/datasets |
| "create dataset", "new dataset" | langfuse-create-dataset | POST /v2/datasets |
| "get dataset {name}" | langfuse-get-dataset | GET /v2/datasets/{name} |
| "list dataset runs", "show runs" | langfuse-list-dataset-runs | GET /datasets/{name}/runs |
| "get dataset run" | langfuse-get-dataset-run | GET /datasets/{name}/runs/{run} |
| "delete dataset run" | langfuse-delete-dataset-run | DELETE /datasets/{name}/runs/{run} |

### Dataset Items (Phase 1)

| User Says | Skill to Load | Endpoint |
|-----------|---------------|----------|
| "list dataset items", "show items" | langfuse-list-dataset-items | GET /dataset-items |
| "create dataset item", "add item" | langfuse-create-dataset-item | POST /dataset-items |
| "get dataset item {id}" | langfuse-get-dataset-item | GET /dataset-items/{id} |
| "delete dataset item" | langfuse-delete-dataset-item | DELETE /dataset-items/{id} |

### Dataset Run Items (Phase 1)

| User Says | Skill to Load | Endpoint |
|-----------|---------------|----------|
| "list run items", "show results" | langfuse-list-dataset-run-items | GET /dataset-run-items |
| "create run item", "log evaluation" | langfuse-create-dataset-run-item | POST /dataset-run-items |

### Score Configs (Phase 2)

| User Says | Skill to Load | Endpoint |
|-----------|---------------|----------|
| "list score configs", "show config" | langfuse-list-score-configs | GET /score-configs |
| "create score config", "new config" | langfuse-create-score-config | POST /score-configs |
| "get score config {id}" | langfuse-get-score-config | GET /score-configs/{id} |
| "update score config" | langfuse-update-score-config | PATCH /score-configs/{id} |

### Scores Write (Phase 2)

| User Says | Skill to Load | Endpoint |
|-----------|---------------|----------|
| "create score", "add score" | langfuse-create-score | POST /scores |
| "delete score", "remove score" | langfuse-delete-score | DELETE /scores/{id} |

### Annotation Queues (Phase 2)

| User Says | Skill to Load | Endpoint |
|-----------|---------------|----------|
| "list queues", "annotation queues" | langfuse-list-annotation-queues | GET /annotation-queues |
| "create queue", "new queue" | langfuse-create-annotation-queue | POST /annotation-queues |
| "get queue {id}" | langfuse-get-annotation-queue | GET /annotation-queues/{id} |
| "list queue items", "queue contents" | langfuse-list-queue-items | GET /annotation-queues/{id}/items |
| "add to queue", "create queue item" | langfuse-create-queue-item | POST /annotation-queues/{id}/items |
| "get queue item" | langfuse-get-queue-item | GET /annotation-queues/{id}/items/{item} |
| "update queue item", "annotate item" | langfuse-update-queue-item | PATCH /annotation-queues/{id}/items/{item} |
| "remove from queue" | langfuse-delete-queue-item | DELETE /annotation-queues/{id}/items/{item} |
| "assign reviewer", "add assignment" | langfuse-create-queue-assignment | POST /annotation-queues/{id}/assignments |
| "unassign reviewer" | langfuse-delete-queue-assignment | DELETE /annotation-queues/{id}/assignments |

### Comments (Phase 2)

| User Says | Skill to Load | Endpoint |
|-----------|---------------|----------|
| "list comments", "show comments" | langfuse-list-comments | GET /comments |
| "create comment", "add comment" | langfuse-create-comment | POST /comments |
| "get comment {id}" | langfuse-get-comment | GET /comments/{id} |

### Ingestion (Phase 3)

| User Says | Skill to Load | Endpoint |
|-----------|---------------|----------|
| "batch ingest", "bulk import" | langfuse-batch-ingest | POST /ingestion |
| "otel ingest", "opentelemetry" | langfuse-otel-ingest | POST /otel/v1/traces |

### Media (Phase 3)

| User Says | Skill to Load | Endpoint |
|-----------|---------------|----------|
| "get media", "download media" | langfuse-get-media | GET /media/{id} |
| "update media" | langfuse-update-media | PATCH /media/{id} |
| "upload url", "media upload" | langfuse-get-upload-url | POST /media |

### Traces Write (Phase 3)

| User Says | Skill to Load | Endpoint |
|-----------|---------------|----------|
| "delete trace" | langfuse-delete-trace | DELETE /traces/{id} |
| "bulk delete traces", "purge" | langfuse-delete-traces | DELETE /traces |

### Models Write (Phase 3)

| User Says | Skill to Load | Endpoint |
|-----------|---------------|----------|
| "create model", "add model" | langfuse-create-model | POST /models |
| "delete model" | langfuse-delete-model | DELETE /models/{id} |

### Projects Admin (Phase 3)

| User Says | Skill to Load | Endpoint |
|-----------|---------------|----------|
| "create project" | langfuse-create-project | POST /v2/projects |
| "update project", "rename project" | langfuse-update-project | PUT /v2/projects/{id} |
| "delete project" | langfuse-delete-project | DELETE /v2/projects/{id} |
| "list api keys", "project keys" | langfuse-list-project-api-keys | GET /v2/projects/{id}/api-keys |
| "create api key", "new key" | langfuse-create-project-api-key | POST /v2/projects/{id}/api-keys |
| "delete api key", "revoke key" | langfuse-delete-project-api-key | DELETE /v2/projects/{id}/api-keys/{key} |

### Organizations (Phase 3)

| User Says | Skill to Load | Endpoint |
|-----------|---------------|----------|
| "list members", "org members" | langfuse-list-org-memberships | GET /v2/organizations/{id}/memberships |
| "update member", "change role" | langfuse-update-org-membership | PUT /v2/organizations/{id}/memberships/{m} |
| "remove member" | langfuse-delete-org-membership | DELETE /v2/organizations/{id}/memberships/{m} |
| "list org projects" | langfuse-list-org-projects | GET /v2/organizations/{id}/projects |
| "org api keys" | langfuse-list-org-api-keys | GET /v2/organizations/{id}/api-keys |

### Utilities (Phase 3)

| User Says | Skill to Load | Endpoint |
|-----------|---------------|----------|
| "health check", "is langfuse up" | langfuse-health | GET /health |
| "metrics", "usage stats" | langfuse-metrics | GET /metrics |

---

## Workflows

### Workflow 0: Config Check (Auto - ALWAYS FIRST)

```bash
python 00-system/skills/langfuse/langfuse-master/scripts/check_langfuse_config.py --json
```

### Workflow 1: List Traces

Show recent LLM traces.

```bash
python 00-system/skills/langfuse/langfuse-list-traces/scripts/list_traces.py --limit 20
```

### Workflow 2: Get Trace Details

Get detailed view of specific trace.

```bash
python 00-system/skills/langfuse/langfuse-get-trace/scripts/get_trace.py --id <trace_id>
```

### Workflow 3: List Observations

List spans, generations, and events.

```bash
python 00-system/skills/langfuse/langfuse-list-observations/scripts/list_observations.py --limit 20
```

### Workflow 4: Get Observation

Get specific observation details.

```bash
python 00-system/skills/langfuse/langfuse-get-observation/scripts/get_observation.py --id <obs_id>
```

### Workflow 5: List Sessions

List user sessions.

```bash
python 00-system/skills/langfuse/langfuse-list-sessions/scripts/list_sessions.py --limit 20
```

### Workflow 6: Get Session

Get session with traces.

```bash
python 00-system/skills/langfuse/langfuse-get-session/scripts/get_session.py --id <session_id>
```

### Workflow 7: List Scores

List evaluation scores.

```bash
python 00-system/skills/langfuse/langfuse-list-scores/scripts/list_scores.py --limit 20
```

### Workflow 8: Get Score

Get specific score.

```bash
python 00-system/skills/langfuse/langfuse-get-score/scripts/get_score.py --id <score_id>
```

### Workflow 9: List Models

List configured models (for cost tracking).

```bash
python 00-system/skills/langfuse/langfuse-list-models/scripts/list_models.py
```

### Workflow 10: Get Model

Get model details.

```bash
python 00-system/skills/langfuse/langfuse-get-model/scripts/get_model.py --id <model_id>
```

### Workflow 11: Get Project

Get current project info.

```bash
python 00-system/skills/langfuse/langfuse-get-project/scripts/get_project.py
```

---

## Quick Reference

```bash
# Check config
python 00-system/skills/langfuse/langfuse-master/scripts/check_langfuse_config.py --test

# List recent traces
python 00-system/skills/langfuse/langfuse-list-traces/scripts/list_traces.py --limit 10

# Get specific trace
python 00-system/skills/langfuse/langfuse-get-trace/scripts/get_trace.py --id abc123
```

---

## Error Handling

On error, load: `langfuse-master/references/error-handling.md`

Common issues:
- **401**: Check API keys
- **404**: Resource not found
- **429**: Rate limited, wait and retry

---

## References

- Master skill: `langfuse-master/`
- Setup guide: `langfuse-master/references/setup-guide.md`
- API reference: `langfuse-master/references/api-reference.md`
