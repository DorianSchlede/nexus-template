---
name: validate-feature
description: "validate feature, test feature, run validation, validate skill, validate before deploy."
---

# Validate Feature

Run parallel subagent tests to validate a feature before deployment.

**This is a META SKILL** - manually invoked per-project, not auto-routed.

---

## Quick Start

```bash
# Initialize test folder in your project
python scripts/init-tests.py --project {PROJECT-ID}

# Edit 02-resources/tests/scenarios.yaml
# Define your test scenarios

# Run tests
python scripts/run-tests.py --project {PROJECT-ID}
```

---

## Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                    INTEGRATED TEST WORKFLOW                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. TEST INITIALIZATION (run-tests.py)                           │
│     ├── Read scenarios.yaml                                      │
│     ├── Create N worktrees (one per test run)                    │
│     └── Return worktree paths                                    │
│                                                                  │
│  2. TEST EXECUTION (parallel)                                    │
│     ├── For each worktree:                                       │
│     │   └── Task(prompt="spawn test-orchestrator\n\n{prompt}")   │
│     └── Collect agent_ids                                        │
│                                                                  │
│  3. TRACE COLLECTION (after 15s wait + retry)                    │
│     ├── For each agent_id:                                       │
│     │   └── Query Langfuse: conversationId = "agent-{agentId}"   │
│     └── Fetch full traces WITH observations                      │
│                                                                  │
│  4. ANALYSIS                                                     │
│     ├── Task(prompt="spawn test-case-analyzer\n\n{traces}")      │
│     └── Analyzer writes report to 04-outputs/validation-reports/ │
│                                                                  │
│  5. CLEANUP                                                      │
│     └── Remove all test worktrees                                │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Context Injection (CRITICAL)

Subagents do NOT receive SessionStart hook context automatically.

**Solution**: Every subagent prompt MUST start with:
```
FIRST: Read 00-system/.cache/session_start_context.xml
```

This gives subagents full Nexus context (orchestrator, skills, projects).

---

## Test Scenario Format

Create `02-resources/tests/scenarios.yaml` in your project:

```yaml
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

**NOTE**: No `REPORT:` section needed - test-case-analyzer handles all reporting.

---

## Worktree Isolation

**ALL tests run in isolated git worktrees** - prevents file conflicts between parallel subagents.

```bash
# Scripts handle worktree management automatically
python scripts/run-tests.py --project {PROJECT-ID}

# Behind the scenes:
# 1. Creates worktrees: ../test-validation-0, ../test-validation-1, etc.
# 2. Runs subagents in parallel
# 3. Cleans up worktrees after completion
```

### Manual Worktree Management

```bash
# Create worktrees
python scripts/worktree-manager.py setup --count 3 --prefix test-validation

# List active worktrees
python scripts/worktree-manager.py list

# Cleanup worktrees
python scripts/worktree-manager.py cleanup --prefix test-validation
```

---

## Langfuse Trace Mapping

| Field | Value | Notes |
|-------|-------|-------|
| `agentId` | From Task tool response | e.g., `af67a58` |
| `conversationId` | `agent-{agentId}` | In Langfuse metadata |
| `sessionId` | Unique per subagent | From Langfuse trace |

**Query pattern**:
```python
for trace in traces:
    if trace.metadata.get('conversationId') == f"agent-{agent_id}":
        session_id = trace.sessionId
        break
```

**CRITICAL - Trace Fetching**:
1. **Retry with exponential backoff** (5s, 10s, 15s) - ingestion delay varies
2. **Call GET /traces/{id} for EACH trace** - to get observations
3. **Use absolute paths** - `Path.resolve()` for worktree paths

---

## Scripts

### init-tests.py

Initialize test folder structure in a project:

```bash
python scripts/init-tests.py --project 41-integrated-subagent-testing-system
# Creates: 02-projects/{PROJECT}/02-resources/tests/scenarios.yaml
```

### run-tests.py

Main test orchestration script:

```bash
python scripts/run-tests.py --project 41-integrated-subagent-testing-system
```

### fetch-traces.py

Fetch traces from Langfuse for analysis:

```bash
# By agent IDs
LANGFUSE_HOST="http://localhost:3002" python scripts/fetch-traces.py \
  --agent-ids "af67a58,ac130b0" --wait 10 --output traces.json

# By session IDs (manual mode)
LANGFUSE_HOST="http://localhost:3002" python scripts/fetch-traces.py \
  --session-ids "sess1,sess2" --output traces.json
```

### worktree-manager.py

Manage git worktrees for isolated testing:

```bash
python scripts/worktree-manager.py setup --count 3 --prefix test-validation
python scripts/worktree-manager.py cleanup --prefix test-validation
```

---

## Subagent Configuration

| Subagent | Trigger Phrase | Purpose |
|----------|----------------|---------|
| `test-orchestrator` | "spawn test-orchestrator" | Normal Nexus orchestrator for validation |
| `test-case-analyzer` | "spawn test-case-analyzer" | Analyze traces, generate reports |

**Explicit invocation only** - these won't trigger accidentally.

**Critical Design**: The `test-orchestrator` doesn't know it's being tested. It reads `session_start_context.xml` and behaves like a normal orchestrator = **authentic behavior**.

---

## test-case-analyzer Input Format

The test-case-analyzer expects these inputs:

```yaml
traces:
  - trace_id: "abc123"
    agent_id: "a1b2c3d"
    session_id: "session-xyz"
    timestamp: "2026-01-07T10:30:00Z"
    observations:
      - name: "Read"
        input: {"file_path": "..."}
        output: "file contents..."
      - name: "Write"
        input: {"file_path": "...", "content": "..."}
        output: "success"

pass_criteria:
  - "Created project folder in 02-projects/"
  - "Generated 4 planning files"

scenario:
  name: "skill_execution_basic"
  description: "Test basic skill execution flow"
  feature_under_test: "plan-project"

output_location: "04-outputs/validation-reports/2026-01-07-skill_execution_basic.md"
```

---

## Report Location

Reports are written to the project being validated:

```
02-projects/{PROJECT-ID}/04-outputs/validation-reports/{timestamp}-{scenario}.md
```

---

## Prerequisites

- `claude-langfuse-monitor` must be running
- Langfuse at localhost:3002
- `LANGFUSE_HOST` env var set when running scripts

---

## Key Insights

1. **Always use worktrees** - All tests run in isolated worktrees
2. **Subagents don't know they're tests** - Give real requests, get authentic behavior
3. **Observations are REQUIRED** - Must call `GET /traces/{id}` for each trace
4. **Retry logic prevents failures** - Exponential backoff handles ingestion delay
5. **Absolute paths only** - Use `Path.resolve()` for all worktree operations

See: `02-projects/34-subagent-validation-system/03-working/key-insights.md`
