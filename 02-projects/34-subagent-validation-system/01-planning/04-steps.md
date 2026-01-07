# Subagent Validation System - Execution Steps

**Last Updated**: 2026-01-07

**IMPORTANT**: Mark tasks complete with [x] as you finish them.

---

## Context Requirements

**Project Location**: `02-projects/34-subagent-validation-system/`

**Files to Load for Execution**:
- `01-planning/01-overview.md` - Purpose, success criteria
- `01-planning/02-discovery.md` - Dependencies, patterns, risks
- `01-planning/03-plan.md` - Approach, decisions
- `01-planning/04-steps.md` - This file (execution tasks)
- `01-planning/resume-context.md` - Resume state

**Output Locations**:
- `03-working/` - Work in progress files
- `04-outputs/` - Final deliverables

---

## Phase 1: Planning (COMPLETE)

- [x] Complete 01-overview.md
- [x] Complete 02-discovery.md
- [x] Complete 03-plan.md
- [x] Complete 04-steps.md
- [x] Review with stakeholder

---

## Phase 2: Langfuse Integration Validation

**Goal**: Confirm subagent traces are captured in Langfuse

- [x] Verify Langfuse env vars are set correctly
  - Keys in `04-workspace/langfuse/.env` (pk-lf-226d37cd..., sk set)
  - HOST not in .env, use localhost:3002
  - API responds OK (status 200)
- [x] Run test subagent and capture its agent_id
  - agentId: `a7ac23a` (haiku model)
- [x] Query Langfuse for traces matching that timeframe
  - Started claude-langfuse-monitor (background task bc73554)
  - New traces appearing from 2026-01-07
  - Test subagent `ac75a88` ran successfully
- [x] Document: How agent_id maps to Langfuse session_id
  - **SOLVED**: agentId IS in Langfuse as `metadata.conversationId`
  - Format: `agent-{agentId}` (e.g., `agent-ac75a88`)
  - Each subagent gets unique `sessionId` (different from parent)
  - **Use sessionId as primary key** (agentId may collide over time)
  - Query: `conversationId == f"agent-{agent_id}"` → extract `sessionId`
  - See: `03-working/langfuse-trace-mapping.md` for full details
- [x] Document: Delay between subagent completion and trace availability
  - Monitor processes every few seconds
  - Traces appear within ~5-10 seconds of completion

---

## Phase 3: Core Skill Structure (COMPLETE)

**Goal**: Create validate-feature skill skeleton

- [x] Create `00-system/skills/system/validate-feature/` folder
- [x] Create `SKILL.md` with triggers and workflow
- [x] Create `templates/scenario.yaml` template
- [x] Create `templates/report.md` template

---

## Phase 4: Test Runner Implementation (COMPLETE)

**Goal**: Spawn and manage test subagents

- [x] Design subagent prompt template (with context injection)
  - Created: `templates/subagent-prompt.md`
  - Includes context loading, structured report format, pass criteria checklist
- [x] Implement parallel subagent spawning (Task tool)
  - Created: `scripts/spawn-test-subagents.py` (pattern documentation)
  - Uses `run_in_background: true` for parallel execution
- [x] Implement agent_id collection from responses
  - Agent IDs returned in Task tool response
  - Composite key: `{sessionId}:{agentId}` for Langfuse
- [x] Handle automated vs manual mode branching
  - Automated: spawn subagents, collect traces
  - Manual: user provides session IDs, skip spawning
- [x] Test: Spawn 5 subagents with simple scenario
  - Test run: 5/5 completed, 5/5 context loaded
  - Agent IDs: ad059c8, aa1c33c, aae376a, a4ec733, afdfb64

---

## Phase 5: Trace Collector (COMPLETE)

**Goal**: Fetch traces from Langfuse for analysis

- [x] Implement trace fetching by agent_id/session_id
  - Created: `scripts/fetch-traces.py`
  - Uses existing `langfuse_client.py` for REST API
  - Searches by `metadata.conversationId = "agent-{agentId}"`
- [x] Handle ingestion delay (wait/retry logic)
  - `--wait` parameter (default 10s)
  - Retry logic in `find_session_by_agent_id()`
- [x] Handle trace not found scenarios
  - Returns empty formatted trace section
  - Logs warning to console
- [x] Format traces for analyzer consumption
  - Markdown format with truncated input/output
  - Includes trace ID, session ID, timestamp
- [x] Test: Fetch traces for test run from Phase 4
  - Agent `af67a58`: 8 traces found
  - Session ID: `a0be5e553e5b680981fce5a3562ecbee`
  - Composite key: `{sessionId}:{agentId}`

---

## Phase 6: Analyzer Implementation (COMPLETE)

**Goal**: Evaluate traces against pass criteria

- [x] Design analyzer prompt with:
  - Traces to review
  - Pass criteria from scenario
  - Report template to fill
  - Created: `.claude/agents/trace-analyzer.md` subagent
- [x] Implement analyzer subagent spawning
  - Uses Task tool with formatted trace data
  - Sonnet model for reasoning
- [x] Parse analyzer response into structured report
  - Returns markdown report with criteria table
  - Includes evidence from traces
- [x] Test: Analyze traces from Phase 5
  - Agent `a5be3b5` analyzed traces from `af67a58`
  - Result: 8/8 criteria PASSED (100%)

---

## Phase 7: End-to-End Integration (COMPLETE)

**Goal**: Full workflow working

- [x] Create sample scenario for testing
  - Created: `02-resources/validation-scenarios.yaml`
  - Scenarios: skill_structure_check, context_loading_test
- [x] Run full validation: scenario → subagents → traces → analyze → report
  - 3 subagents ran: af7e6ca, ac130b0, a4c2bb6
  - All 3 passed: 6/6 criteria each
- [x] Verify report accuracy
  - Reports match actual folder structure
- [x] Test manual mode with provided session IDs
  - `--session-ids` parameter works
  - Fetched 8 traces for session `a0be5e553e5b680981fce5a3562ecbee`
- [x] Document edge cases discovered
  - See below

**Edge Cases & Learnings**:

### 1. Subagent Resume Pattern (VALIDATED)
- Task tool `resume` parameter works for continuing conversations
- Agent ID `a01d45d` tested: spawned → asked questions → resumed with answers
- Enables interactive validation flows where subagents ask questions
- **Pattern**: Spawn subagent → it reports decision points → orchestrator provides answers → resume

### 2. Natural Orchestrator Behavior
- Subagents can behave like normal orchestrator (not aware they're tests)
- Just give them real user requests, they follow orchestrator rules
- Traces capture full behavior for later analysis

### 3. Windows Encoding
- Unicode characters in trace output cause `cp1252` encoding errors
- Solution: Use `--output file.json` instead of printing to console

---

## Phase 8: Documentation & Deployment

**Goal**: Ready for production use

- [x] Update SKILL.md with complete usage documentation
  - Added Quick Start, Three Modes, Context Injection, Langfuse Mapping
  - Full example flow, key insights, meta skill design
- [x] ~~Add validate-feature to orchestrator triggers~~ **SKIPPED**: Meta skill, manually invoked per-project
- [x] ~~Update system-map.md with new skill~~ **SKIPPED**: Not a routed skill
- [x] Create example scenario for reference
  - Already exists: `02-resources/validation-scenarios.yaml`
  - Template: `templates/scenario.yaml`
- [x] Test with real project validation scenario
  - Created: `02-resources/real-project-validation.yaml`
  - Tested plan-project skill with 4 parallel subagents
  - Agent IDs: aed8b1f, a3a5c37, ab3184f, a1e6da1
  - Updated custom subagent descriptions with "MUST BE USED" triggers
  - Documented intelligent matching pattern in SKILL.md

---

## Notes

**Current blockers**: None (resolved)

**Key unknowns**: All resolved
- Agent_id to Langfuse session_id mapping: `metadata.conversationId = "agent-{agentId}"`
- Trace ingestion delay timing: ~5-10 seconds

**Success criteria**:
- [x] Can validate a feature with 5+ subagent runs
- [x] Report shows pass/fail per criteria
- [x] Works for both automated and manual modes

**All success criteria met!**

---

*Mark tasks complete with [x] as you finish them*
