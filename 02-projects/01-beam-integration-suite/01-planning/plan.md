# Beam Integration Suite - Plan

**Last Updated**: 2025-12-11

---

## Approach

**Phase 1: Import Existing Skills**
- Import 9 Beam skills from Notion to `00-system/skills/beam/`
- Exclude design skills (design-beam-agent, graph-slicer, update-variables-in-notion)

**Phase 2: Create beam-master**
- Create shared resource library with ALL 22 API endpoint scripts
- Create `references/` with setup guide, API docs, error handling
- Create `scripts/` for every API endpoint

**Phase 3: Create beam-connect**
- Build user-facing meta-skill following Notion/Airtable pattern
- Implement workflow routing and natural language matching
- Connect to beam-master scripts and references

**Phase 4: Integration & Testing**
- Ensure skills are detected by Nexus loader
- Test all workflows end-to-end
- Document in system skill registry

---

## Key Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| **Location** | `00-system/skills/beam/` | System-level integration, not user skill |
| **Pattern** | Master/Connect | Consistency with Notion/Airtable, DRY principle |
| **Exclude Design Skills** | Yes | User requested - focus on API operations |
| **Full API Coverage** | All 22 endpoints | Complete integration per user request |
| **Base URL** | `https://api.beamstudio.ai` | From Beam API docs |
| **Auth Method** | Bearer token from API key exchange | Standard Beam auth flow |

---

## Resources Needed

**Tools/Access**:
- Notion API access (for skill import)
- Beam API key and workspace ID
- Existing Beam skills from Notion database

**Reference Materials**:
- `00-system/skills/notion/notion-master/` - Master skill template
- `00-system/skills/airtable/airtable-master/` - Master skill template
- Beam API docs: https://docs.beam.ai/08-reference/api/overview/overview

**Environment Variables**:
- `BEAM_API_KEY` - Beam API key
- `BEAM_WORKSPACE_ID` - Workspace ID

---

## Dependencies & Links

**Files to Create**:
- `00-system/skills/beam/` - New folder
- `00-system/skills/beam/beam-master/SKILL.md`
- `00-system/skills/beam/beam-connect/SKILL.md`
- `00-system/skills/beam/beam-master/scripts/` - 22+ Python scripts
- `00-system/skills/beam/beam-master/references/` - Docs

**External Systems**:
- Notion Skills Database - Source of 9 Beam skills
- Beam AI API (https://api.beamstudio.ai) - Target system

**Related Skills**:
- `notion-master` - Pattern reference
- `airtable-master` - Pattern reference
- `import-skill-to-nexus` - For importing skills

---

## Skills to Import from Notion (9)

**Agent Management Skills**:
1. `beam-list-agents` - List agents in workspace
2. `beam-get-agent-graph` - Fetch agent graph config
3. `beam-get-agent-analytics` - Get agent metrics
4. `beam-create-agent-task` - Create agent tasks
5. `beam-update-graph-node` - Update node config
6. `beam-test-graph-node` - Test graph nodes
7. `beam-get-nodes-by-tool` - Get nodes by tool
8. `beam-debug-issue-tasks` - Debug via Langfuse
9. `evaluate-solutions-case-study` - Evaluate case studies

**Excluded (Design Skills)**:
- ~~design-beam-agent~~
- ~~graph-slicer~~
- ~~update-variables-in-notion~~

---

## Scripts to Create (22 API endpoints)

### Authentication Scripts (2)
- `get_access_token.py` - POST /auth/access-token
- `refresh_token.py` - POST /auth/refresh-token

### User Scripts (1)
- `get_current_user.py` - GET /v2/user/me

### Agent Scripts (1)
- `list_agents.py` - GET /agent

### Context File Scripts (1)
- `download_context_file.py` - GET /agent/{agentId}/context/file/{fileId}/download

### Agent Graph Scripts (4)
- `get_agent_graph.py` - GET /agent-graphs/{agentId}
- `test_graph_node.py` - POST /agent-graphs/test-node
- `update_graph_node.py` - PATCH /agent-graphs/update-node
- `get_nodes_by_tool.py` - GET /agent-graphs/agent-task-nodes/{toolFunctionName}

### Agent Task Scripts (11)
- `list_tasks.py` - GET /agent-tasks
- `create_task.py` - POST /agent-tasks
- `get_task.py` - GET /agent-tasks/{taskId}
- `get_task_updates.py` - GET /agent-tasks/{taskId}/updates (SSE)
- `get_analytics.py` - GET /agent-tasks/analytics
- `get_latest_executions.py` - GET /agent-tasks/latest-executions
- `iterate_tasks.py` - GET /agent-tasks/iterate
- `get_tool_output_schema.py` - GET /agent-tasks/tool-output-schema/{graphNodeId}
- `retry_task.py` - POST /agent-tasks/retry
- `provide_user_input.py` - PATCH /agent-tasks/execution/{taskId}/user-input
- `reject_task.py` - POST /agent-tasks/execution/{taskId}/rejection
- `approve_task.py` - POST /agent-tasks/execution/{taskId}/user-consent
- `rate_task_output.py` - PATCH /agent-tasks/execution/{taskId}/output-rating

### Tool Scripts (2)
- `optimize_tool.py` - POST /tool/optimize/{toolFunctionName}
- `get_optimization_status.py` - POST /tool/optimization-status/thread/{threadId}

### Utility Scripts
- `check_beam_config.py` - Config validation with AI-actionable JSON
- `setup_beam.py` - Interactive setup wizard

---

## Open Questions

- [x] What API endpoints exist? (22 documented)
- [x] Exclude design skills? (Yes - user confirmed)
- [x] Base URL? (`https://api.beamstudio.ai`)
- [ ] Rate limiting details for Beam API?

---

## Mental Models Applied

**Architectural Pattern Matching**:
- Following proven master/connect pattern from existing integrations
- 60% context reduction through shared resources
- Progressive disclosure for efficient AI context usage

**Complete Coverage**:
- All 22 API endpoints will have corresponding scripts
- No gaps in API functionality

**Risk Mitigation**:
- Risk: Skills may have different structures → Normalize during import
- Risk: Missing API documentation → Use Beam Academy MCP for gaps
- Risk: Rate limiting → Add exponential backoff to scripts

---

*Next: Complete steps.md to break down execution*
