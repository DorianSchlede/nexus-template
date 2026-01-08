# Integrated Subagent Testing System - Discovery

**Project Type**: Build
**Purpose**: Surface requirements and dependencies before planning

---

## Requirements (EARS Format)

### Functional Requirements

**REQ-1**: WHEN a project is planned, THE system SHALL generate test scenarios in `02-resources/tests/scenarios.yaml`

**REQ-2**: WHEN test scenarios are defined, THE system SHALL create one git worktree per test run for isolation

**REQ-3**: THE test-orchestrator subagent SHALL read `00-system/.cache/session_start_context.xml` and execute the test prompt without awareness of being tested

**REQ-4**: WHEN all test runs complete, THE system SHALL fetch traces from Langfuse using `metadata.conversationId = "agent-{agentId}"`

**REQ-5**: THE test-case-analyzer subagent SHALL evaluate traces against pass criteria and write reports to `04-outputs/validation-reports/`

**REQ-6**: THE scenarios.yaml file SHALL support multiple test definitions that are split into individual test runs

### Non-Functional Requirements

**REQ-NF-1**: THE system SHALL complete trace fetching within 15 seconds of subagent completion (Langfuse ingestion delay)

**REQ-NF-2**: THE system SHALL handle Windows cp1252 encoding by writing output to files instead of console

**REQ-NF-3**: THE system SHALL cleanup all worktrees after test completion

### Quality Checklist (INCOSE)

- [x] All requirements use EARS patterns (THE/WHEN/WHILE/IF/WHERE)
- [x] No vague terms (quickly, adequate, reasonable, user-friendly)
- [x] No pronouns (it, them, they) - specific names used
- [x] Each requirement independently testable
- [x] Active voice throughout
- [x] No escape clauses (where possible, if feasible)
- [x] Solution-free (what, not how)

---

## Dependencies

### Files to Modify

| File | Changes Needed |
|------|----------------|
| `.claude/agents/trace-analyzer.md` | Rename to `test-case-analyzer.md`, update trigger phrase |
| `00-system/skills/system/validate-feature/SKILL.md` | Simplify to always use worktree, remove manual modes |
| `00-system/skills/system/validate-feature/scripts/fetch-traces.py` | Refactor to use session-scorer Langfuse patterns |

### Files to Create

| File | Purpose |
|------|---------|
| `00-system/skills/system/validate-feature/scripts/init-tests.py` | Initialize test folder structure in projects |
| `00-system/skills/system/validate-feature/scripts/run-tests.py` | Main test orchestration script |
| `00-system/skills/system/validate-feature/templates/scenarios-template.yaml` | Template for test scenarios per project type |
| `.claude/agents/test-case-analyzer.md` | Renamed analyzer subagent |

### External Systems

- **Langfuse**: Trace storage and retrieval via REST API
- **Git Worktrees**: File isolation for parallel test runs

---

## Existing Patterns

| Pattern | Location | Reuse Strategy |
|---------|----------|----------------|
| Langfuse trace fetching | `03-skills/langfuse/langfuse-get-session/scripts/get_session.py` | Use as reference for API calls |
| Langfuse trace hierarchy | Project 36 `trace-structure-analysis.md` | Session → Trace → Observation pattern |
| Session scorer structure | `00-system/skills/meta/langfuse-score-session/prompts/scorer-prompt.md` | Reuse scoring dimensions where applicable |
| Worktree management | `validate-feature/scripts/worktree-manager.py` | Keep and enhance |
| Test orchestrator | `.claude/agents/test-orchestrator.md` | Keep as-is (authentic behavior) |
| Langfuse client | `03-skills/langfuse/langfuse-master/scripts/langfuse_client.py` | Reuse for API calls |

---

## Architecture from Session Scorer (Project 36)

**Langfuse Data Hierarchy**:
```
Session
  └── Trace (1:N via sessionId)
        └── Observation (1:N via traceId)
```

**API Behavior**:
- `GET /sessions/{id}` returns traces WITHOUT observations
- `GET /traces/{id}` returns trace WITH observations
- Must call get-trace for each trace to get full content

**Key Scripts to Reuse**:
```bash
# Get session info
python 03-skills/langfuse/langfuse-get-session/scripts/get_session.py --session-id {id}

# List traces in session
python 03-skills/langfuse/langfuse-list-traces/scripts/list_traces.py --session-id {id}

# Get trace with observations
python 03-skills/langfuse/langfuse-get-trace/scripts/get_trace.py --trace-id {id}
```

---

## Test Scenario Format (Proposed)

```yaml
# 02-resources/tests/scenarios.yaml
version: 1.0
project_id: "41-integrated-subagent-testing-system"

scenarios:
  - name: "skill_execution_basic"
    description: "Test basic skill execution flow"
    runs: 3  # Number of parallel test runs
    prompt: |
      FIRST: Read 00-system/.cache/session_start_context.xml
      THEN: Execute the plan-project skill with name "Test Project"
    pass_criteria:
      - "Created project folder in 02-projects/"
      - "Generated 4 planning files"
      - "No errors in execution"

  - name: "error_handling"
    description: "Test error handling with invalid input"
    runs: 2
    prompt: |
      FIRST: Read 00-system/.cache/session_start_context.xml
      THEN: Execute plan-project with empty name
    pass_criteria:
      - "Error message displayed"
      - "Did not crash or hang"
```

**NOTE**: No `REPORT:` section needed - analyzer handles reporting automatically

---

## ARCHITECTURE GAPS (from Deep Analysis)

### Gap 1: Trace Fetching Timing (CRITICAL)

**Problem**: `fetch-traces.py` has hardcoded 10s wait, but ingestion varies 5-15s.

**Current Code** (line 156):
```python
time.sleep(wait_for_ingestion)  # Single wait, no retry
```

**Risk**: If subagent finishes after wait period, traces won't be fetched.

**Fix**: Implement retry logic with exponential backoff:
```python
max_retries = 3
for attempt in range(max_retries):
    traces = find_traces_by_agent_id(agent_id)
    if traces:
        break
    time.sleep(5 * (attempt + 1))  # 5s, 10s, 15s
```

### Gap 2: Missing Observations in Traces (CRITICAL)

**Problem**: `GET /sessions/{id}` returns traces WITHOUT observations.

**Current**: Counts observations but doesn't retrieve them:
```python
if trace.get('observations'):
    output.append(f"Observations: {count}")  # No content!
```

**Fix**: Must call `GET /traces/{id}` for EACH trace to get observations:
```python
for trace in traces:
    full_trace = get_trace(trace['id'])  # Includes observations
    observations = full_trace.get('observations', [])
```

**Impact**: Without observations, can't verify tool calls = can't verify pass criteria.

### Gap 3: Relative Worktree Paths (MODERATE)

**Problem**: Worktrees created as `../test-validation-0` (relative).

**Risk**: Subagent working directory may differ, breaking path resolution.

**Fix**: Use absolute paths:
```python
worktree_path = Path(relative_path).resolve()
```

### Gap 4: No Pagination in Trace Fetching (MODERATE)

**Problem**: `fetch-traces.py` queries with limit but doesn't paginate.

**Current**:
```python
response = client.get("/traces", params={"limit": limit})
```

**Risk**: May miss traces if session has > 100.

**Fix**: Use list_traces skill with proper pagination loop.

### Gap 5: Test-Awareness Language (LOW but IMPORTANT)

**Problem**: `spawn-test-subagents.py` has old pattern:
```python
"You are a TEST SUBAGENT validating a feature..."
```

**Violates**: Design principle that subagents shouldn't know they're being tested.

**Fix**: Remove all test-awareness language. Use clean prompt:
```
FIRST: Read 00-system/.cache/session_start_context.xml
THEN: {user_request}
```

---

## Risks & Unknowns

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Langfuse trace ingestion delay varies | Medium | High | **Retry logic** (3 attempts, exponential backoff) |
| Missing observations in traces | High | Critical | **Call get_trace for each trace_id** |
| Worktree paths don't resolve | Medium | High | **Use Path.resolve() for absolute paths** |
| Pagination missing | Low | Medium | Use list_traces skill with page param |
| Subagent triggers accidentally | Low | Medium | Explicit trigger phrases only |
| Test scenarios grow too complex | Medium | Low | Keep scenarios focused on single behaviors |

### Open Questions

- [x] How does agent_id map to Langfuse? → `metadata.conversationId = "agent-{agentId}"`
- [x] Trace ingestion delay? → ~5-10 seconds
- [x] How to get observations? → Must call `GET /traces/{id}` per trace
- [ ] Should test results aggregate across multiple projects?
- [ ] Integration with execute-project workflow?

---

## Known Working Patterns (DO NOT CHANGE)

| Pattern | Validation | Location |
|---------|------------|----------|
| Context injection via `session_start_context.xml` | 10/10 subagents successful | P34 testing |
| Test-orchestrator unaware of testing | Authentic behavior verified | `.claude/agents/test-orchestrator.md` |
| Sequential worktree setup, parallel execution | Race conditions prevented | `worktree-manager.py` |
| Agent ID mapping: `conversationId = "agent-{agentId}"` | Reliable | P34 key-insights.md |
| Langfuse client with Basic Auth | Proven | `langfuse_client.py` |

---

*This discovery document is MANDATORY. It preserves intelligence across compaction.*
*Auto-populate 03-plan.md Dependencies section from findings above.*
