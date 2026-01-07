# Integrated Subagent Testing System - Plan

**Project Type**: Build
**Status**: Planning

---

## Context

**Load Before Reading**:
- `01-planning/02-discovery.md` - Requirements and dependencies

---

## Mental Model Analysis

### First Principles: What's Essential?

**Core Problem**: We need to validate that skills/features work correctly via parallel subagent execution.

**Essential Components**:
1. **Test Definition**: YAML file with scenarios, prompts, pass criteria
2. **Isolation**: Each test run in its own worktree (file conflicts solved)
3. **Execution**: Subagents that don't know they're being tested (authentic)
4. **Analysis**: Trace fetching from Langfuse + evaluation against criteria
5. **Reporting**: Structured output with pass/fail per criterion

**What's NOT Essential** (remove complexity):
- Multiple modes (Automated/Manual/Interactive/Worktree) → Always worktree
- Separate `fetch-traces.py` → Integrate into main orchestration
- `REPORT:` in prompts → Analyzer handles all reporting

### Pre-Mortem: Why Would This Fail?

| Failure Mode | Cause | Prevention |
|--------------|-------|------------|
| Tests pass but feature broken | Weak pass criteria | Require specific, measurable criteria |
| Subagent behaves differently | Knows it's being tested | Keep test-orchestrator unaware |
| Langfuse traces missing | Ingestion delay | **Retry logic with exponential backoff** |
| Worktree conflicts | Parallel creation race | Sequential worktree setup before parallel execution |
| Reports unreadable | Too much data | Summarize + link to full traces |
| Test scenarios stale | Not updated with feature | Tests live in project, updated during planning |
| **Can't verify pass criteria** | **Missing observations** | **Call GET /traces/{id} for each trace** |
| **Path resolution fails** | **Relative worktree paths** | **Use Path.resolve() for absolute paths** |

---

## Approach

**Strategy**: Simplify validate-feature to a single flow with automatic worktree isolation.

```
┌─────────────────────────────────────────────────────────────────┐
│                    INTEGRATED TEST WORKFLOW                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. PROJECT PLANNING                                             │
│     └── Generate: 02-resources/tests/scenarios.yaml              │
│                                                                  │
│  2. TEST INITIALIZATION (run-tests.py)                           │
│     ├── Read scenarios.yaml                                      │
│     ├── Create N worktrees (one per test run)                    │
│     └── Return worktree paths                                    │
│                                                                  │
│  3. TEST EXECUTION (parallel)                                    │
│     ├── For each worktree:                                       │
│     │   └── Task(prompt="spawn test-orchestrator\n\n{prompt}")   │
│     └── Collect agent_ids                                        │
│                                                                  │
│  4. TRACE COLLECTION (after 15s wait)                            │
│     ├── For each agent_id:                                       │
│     │   └── Query Langfuse: conversationId = "agent-{agentId}"   │
│     └── Fetch full traces with observations                      │
│                                                                  │
│  5. ANALYSIS                                                     │
│     ├── Task(prompt="spawn test-case-analyzer\n\n{traces}")      │
│     └── Analyzer writes report to 04-outputs/validation-reports/ │
│                                                                  │
│  6. CLEANUP                                                      │
│     └── Remove all test worktrees                                │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Correctness Properties

**Property 1: Test Isolation**
For all test runs, each subagent operates in an isolated worktree with no shared file state.
**Validates**: REQ-2

**Property 2: Authentic Behavior**
For any test execution, the test-orchestrator subagent receives no indication that it is being tested.
**Validates**: REQ-3

**Property 3: Trace Completeness**
For all completed test runs, Langfuse traces are retrievable via agent_id within 15 seconds.
**Validates**: REQ-4, REQ-NF-1

**Property 4: Report Generation**
For any test scenario, the test-case-analyzer produces a report at the specified output location.
**Validates**: REQ-5

---

## Key Decisions

| Decision | Choice | Rationale | Validates |
|----------|--------|-----------|-----------|
| Single flow vs multiple modes | Single (always worktree) | Simplicity, all tests benefit from isolation | REQ-2 |
| Trace fetching approach | Use existing Langfuse skills | Proven patterns from Project 36 | REQ-4 |
| Analyzer naming | `test-case-analyzer` | Clearer purpose than `trace-analyzer` | REQ-5 |
| Test location | `02-resources/tests/` | Co-located with project, survives archive | REQ-1 |
| Trigger phrase | "spawn test-case-analyzer" | Explicit, won't trigger accidentally | REQ-5 |

---

## Dependencies & Links

**Files to Modify**:
| File | Changes | Validates |
|------|---------|-----------|
| `.claude/agents/trace-analyzer.md` | Rename to `test-case-analyzer.md` | REQ-5 |
| `validate-feature/SKILL.md` | Simplify to single worktree flow | REQ-2 |
| `validate-feature/scripts/fetch-traces.py` | Use Langfuse skill patterns | REQ-4 |

**Files to Create**:
| File | Purpose | Validates |
|------|---------|-----------|
| `validate-feature/scripts/run-tests.py` | Main orchestration | REQ-1, REQ-2 |
| `validate-feature/templates/scenarios-template.yaml` | Test scenario template | REQ-6 |
| `.claude/agents/test-case-analyzer.md` | Renamed analyzer | REQ-5 |

**External Systems**:
- Langfuse: Trace storage via REST API (existing skills)
- Git: Worktree management for isolation

---

## Testing Strategy

### Property-Based Tests

| Property | Test Strategy |
|----------|---------------|
| P1: Test Isolation | Verify each worktree has unique path, no shared files modified |
| P2: Authentic Behavior | Inspect test-orchestrator.md has no test-awareness language |
| P3: Trace Completeness | Time from subagent completion to trace availability |
| P4: Report Generation | Verify file exists at expected path after analysis |

### Integration Tests

| Scenario | Test Cases |
|----------|------------|
| Basic execution | 3 parallel test runs, verify all complete |
| Error handling | Invalid scenario, verify graceful failure |
| Worktree cleanup | After test, verify no orphan worktrees |

---

## Success Criteria (from Mental Models)

**Must Pass**:
- [ ] Single YAML file splits into N independent test runs
- [ ] All tests run in isolated worktrees (no file conflicts)
- [ ] Subagents behave authentically (no test awareness)
- [ ] Traces fetched successfully from Langfuse
- [ ] Reports generated at `04-outputs/validation-reports/`
- [ ] Worktrees cleaned up after completion

**Quality Indicators**:
- Test execution time < 5 minutes for 5 parallel runs
- Report includes evidence for each pass/fail criterion

---

## Risks & Mitigations (from Pre-Mortem + Deep Analysis)

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| **Missing observations** | **High** | **Critical** | **GET /traces/{id} for each trace** |
| Langfuse ingestion delay varies | Medium | High | **Retry logic (3x, exponential backoff)** |
| Worktree paths don't resolve | Medium | High | **Path.resolve() for absolute paths** |
| Worktree creation race condition | Low | High | Sequential setup, parallel execution |
| Subagent aware of testing | Low | High | Keep test-orchestrator minimal |
| Windows path issues | Medium | Medium | Use pathlib, test on Windows |
| Pagination missing | Low | Medium | Use list_traces skill with page param |

---

## Open Questions

| Question | Resolution | Validates |
|----------|------------|-----------|
| Should tests auto-run during execute-project? | Pending - ask user | REQ-1 |
| Aggregate results across projects? | Nice-to-have, defer | - |

---

*Execution steps in 04-steps.md*
