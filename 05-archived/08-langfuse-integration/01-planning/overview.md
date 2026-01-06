---
id: 08-langfuse-integration
name: Langfuse Integration
status: COMPLETE
description: "Load when user mentions 'langfuse', 'traces', 'observations', 'llm tracing', 'observability', 'langfuse scores', 'langfuse sessions'"
created: 2025-12-28
---

# Langfuse Integration

Build complete Langfuse integration following the master/connect/specialized pattern.

## Discovery

- **Service**: Langfuse (LLM Observability & Tracing)
- **API Docs**: https://api.reference.langfuse.com/
- **Auth Type**: Basic Auth (Public Key as username, Secret Key as password)
- **Base URL**: https://tracing.beamstudio.ai (self-hosted)

## Scope

- **Endpoints**: 11 GET endpoints (read-only)
- **Categories**: Traces, Observations, Sessions, Scores, Models, Projects

## Selected Endpoints

| Category | Endpoint | Path |
|----------|----------|------|
| Traces | List Traces | GET /traces |
| Traces | Get Trace | GET /traces/{traceId} |
| Observations | List Observations | GET /v2/observations |
| Observations | Get Observation | GET /observations/{id} |
| Sessions | List Sessions | GET /sessions |
| Sessions | Get Session | GET /sessions/{id} |
| Scores | List Scores | GET /v2/scores |
| Scores | Get Score | GET /v2/scores/{id} |
| Models | List Models | GET /models |
| Models | Get Model | GET /models/{id} |
| Projects | Get Project | GET /projects |

## Architecture

Will create in `00-system/skills/langfuse/`:
- `langfuse-master/` - Shared resources (client, config check, references)
- `langfuse-connect/` - Meta-skill entry point with routing
- 11 operation skills (one per endpoint)

## References

- Config: [integration-config.json](../02-resources/integration-config.json)
- Pattern: See 00-system/skills/system/add-integration/references/integration-architecture.md
- Env vars already configured in .env

---

*Next: See steps.md for implementation checklist*
