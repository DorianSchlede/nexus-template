---
id: 01-beam-integration-suite
name: Beam Integration Suite
status: COMPLETE
description: "Load when user mentions 'beam', 'beam agent', 'beam analytics', 'beam task', 'beam graph', or any Beam AI operations"
created: 2025-12-11
completed: 2025-12-11
---

# Beam Integration Suite

## Purpose

Create a comprehensive Beam AI integration for Nexus by:
1. Importing 9 existing Beam skills from Notion (excluding design skills)
2. Building a `beam-master` skill with ALL 22 Beam API endpoints
3. Building a `beam-connect` skill (user-facing meta-skill)

This follows the established master/connect pattern from Notion and Airtable integrations, enabling unified Beam AI agent management through natural language commands.

---

## Success Criteria

**Must achieve**:
- [ ] 9 Beam skills imported to `00-system/skills/beam/`
- [ ] `beam-master` skill created with ALL 22 API endpoint scripts
- [ ] `beam-connect` skill created for user-facing operations
- [ ] Config validation script (`check_beam_config.py`) working
- [ ] All API categories covered: Auth, User, Agents, Context Files, Graphs, Tasks, Tools
- [ ] All skills properly integrated with Nexus routing

**Nice to have**:
- [ ] Beam Academy MCP integration documented
- [ ] Context caching for agent lists (like Notion/Airtable)

---

## Context

**Background**:
- 9 Beam agent management skills exist in the Notion skills database
- 22 API endpoints documented at docs.beam.ai
- No centralized integration exists yet in Nexus

**Stakeholders**:
- Solutions team (primary users)
- Anyone working with Beam AI agents

**Constraints**:
- Must follow existing master/connect pattern for consistency
- Skills should integrate with existing Nexus infrastructure
- Location: `00-system/skills/beam/` (system layer)

---

## Scope

**In Scope**:
- Import 9 Beam skills from Notion (agent management only)
- Create beam-master with ALL 22 API endpoint scripts
- Create beam-connect for orchestration
- Integrate with Nexus skill routing

**Out of Scope**:
- Design skills (design-beam-agent, graph-slicer, update-variables-in-notion)
- Beam Academy content integration (separate project)

---

## API Coverage (22 endpoints)

### Authentication (2)
- POST `/auth/access-token` - Exchange API key for token
- POST `/auth/refresh-token` - Refresh token

### User (1)
- GET `/v2/user/me` - Get user profile

### Agents (1)
- GET `/agent` - List workspace agents

### Agent Context Files (1)
- GET `/agent/{agentId}/context/file/{fileId}/download` - Download file

### Agent Graph (4)
- GET `/agent-graphs/{agentId}` - Get agent graph
- POST `/agent-graphs/test-node` - Test node
- PATCH `/agent-graphs/update-node` - Update node
- GET `/agent-graphs/agent-task-nodes/{toolFunctionName}` - Get nodes by tool

### Agent Tasks (11)
- GET `/agent-tasks` - List tasks
- POST `/agent-tasks` - Create task
- GET `/agent-tasks/{taskId}` - Get task
- GET `/agent-tasks/{taskId}/updates` - SSE updates
- GET `/agent-tasks/analytics` - Get analytics
- GET `/agent-tasks/latest-executions` - Recent executions
- GET `/agent-tasks/iterate` - Iterate tasks
- GET `/agent-tasks/tool-output-schema/{graphNodeId}` - Get schema
- POST `/agent-tasks/retry` - Retry task
- PATCH `/agent-tasks/execution/{taskId}/user-input` - User input
- POST `/agent-tasks/execution/{taskId}/rejection` - Reject task
- POST `/agent-tasks/execution/{taskId}/user-consent` - Approve task
- PATCH `/agent-tasks/execution/{taskId}/output-rating` - Rate output

### Tools (2)
- POST `/tool/optimize/{toolFunctionName}` - Optimize tool
- POST `/tool/optimization-status/thread/{threadId}` - Check status

---

*Next: Complete plan.md to define your approach*
