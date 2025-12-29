---
name: langfuse-connect
description: "Complete Langfuse integration (traces, observations, sessions, scores, models). Load when user mentions 'langfuse', 'traces', 'observations', 'llm tracing', 'observability', 'langfuse scores', 'langfuse sessions', 'list traces', 'get trace'."
---

# Langfuse Connect

User-facing entry point for Langfuse integration. Routes to appropriate operation skills.

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
