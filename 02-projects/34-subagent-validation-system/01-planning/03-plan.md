# Subagent Validation System - Plan

**Last Updated**: 2026-01-07

---

## Context

**Load Before Reading**:
- `01-planning/01-overview.md` - Purpose and success criteria
- `01-planning/02-discovery.md` - Dependencies discovered

---

## Approach

Build a **skill-based validation system** that:

1. **Spawns N test subagents** (5-10) running the same scenario in parallel
2. **Stores transcripts in Langfuse** via subagent session IDs
3. **Spawns analyzer subagent** to review all traces and evaluate pass/fail
4. **Returns validation report** to main agent for decision

**Two execution modes:**
- **Automated**: Non-interactive scenarios run end-to-end by subagents
- **Manual**: User runs interactive flow, provides session IDs, analyzer reviews

---

## Key Decisions

| Decision | Choice | Why |
|----------|--------|-----|
| Skill vs Project | **Skill** (`validate-feature`) | Reusable across projects, can be invoked on-demand |
| Test subagent model | **Sonnet** | Proper simulation - same capabilities as production |
| Analyzer model | **Sonnet** | Needs full reasoning for trace analysis |
| Scenario storage | **Project's `02-resources/`** | Each project owns its validation scenarios |
| Report format | **Markdown template** | Human-readable, can be stored in project outputs |
| Context injection | **Read cached XML** | Validated with 10/10 subagents - simple, works |

---

## Dependencies & Links

**Files to Create**:
- `00-system/skills/system/validate-feature/SKILL.md`
- `00-system/skills/system/validate-feature/templates/scenario.yaml`
- `00-system/skills/system/validate-feature/templates/report.md`

**External Systems**:
- Langfuse (localhost:3002) - Trace storage and retrieval
- Claude Code Task tool - Subagent spawning

**Related Projects**:
- Project 27 (COMPLETE) - Langfuse research, session scorer spec
- Project 28 - Handover test suite (98% complete)

**Related Skills**:
- `03-skills/langfuse/langfuse-get-trace/` - Fetch individual traces
- `03-skills/langfuse/langfuse-list-traces/` - List traces by session

---

## Technical Architecture

**System Components**:

```
┌─────────────────────────────────────────────────────────────┐
│                 validate-feature SKILL                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. SCENARIO LOADER                                          │
│     └─► Read project's validation-scenarios.yaml             │
│                                                              │
│  2. TEST RUNNER                                              │
│     └─► Spawn N subagents in parallel                        │
│     └─► Each reads 00-system/.cache/session_start_context.xml│
│     └─► Each executes scenario prompt                        │
│     └─► Collect agent IDs on completion                      │
│                                                              │
│  3. TRACE COLLECTOR                                          │
│     └─► Wait for Langfuse ingestion (~5s delay)              │
│     └─► Fetch traces for each agent session                  │
│                                                              │
│  4. ANALYZER                                                 │
│     └─► Spawn analyzer subagent                              │
│     └─► Provide: traces, pass_criteria, report template      │
│     └─► Receive: completed validation report                 │
│                                                              │
│  5. REPORT GENERATOR                                         │
│     └─► Format report from analyzer output                   │
│     └─► Return to main agent                                 │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Data Flow**:
```
Project scenarios.yaml → Skill loads scenarios
                      → Spawn test subagents (parallel)
                      → Subagents execute, return agent IDs
                      → Fetch traces from Langfuse
                      → Spawn analyzer with traces + criteria
                      → Analyzer evaluates, generates report
                      → Report returned to main agent
```

**Technology Stack**:
- Python scripts for orchestration (optional)
- Claude Code Task tool for subagent spawning
- Langfuse Python SDK for trace retrieval
- YAML for scenario definitions
- Markdown for reports

---

## Implementation Strategy

**Phase 1: Core Skill Structure**
- Create skill folder and SKILL.md
- Define scenario template format
- Define report template format

**Phase 2: Test Runner**
- Implement parallel subagent spawning
- Collect agent IDs from Task tool responses
- Handle both automated and manual modes

**Phase 3: Trace Integration**
- Connect to Langfuse for trace retrieval
- Map agent IDs to Langfuse session IDs (may need investigation)
- Handle trace not found scenarios

**Phase 4: Analyzer**
- Design analyzer prompt with pass_criteria
- Implement report generation
- Test on sample scenarios

**Phase 5: End-to-End Validation**
- Test with real project scenario
- Validate full flow works
- Document usage patterns

**Testing Approach**:
- Unit test: Each component in isolation
- Integration test: Full flow with mock scenario
- Real test: Validate the validator using itself

**Deployment Plan**:
- Skill goes in `00-system/skills/system/validate-feature/`
- Add to orchestrator routing triggers
- Document in system-map.md

---

## Open Questions

- [x] Can subagents read cached context? → YES
- [x] What model for subagents? → Sonnet (proper simulation)
- [ ] How do Claude Code agent IDs map to Langfuse session IDs?
- [ ] Is there a delay before traces appear in Langfuse?
- [ ] Can we run 10 subagents in parallel without rate limits?

---

*Next: Break down execution in 04-steps.md*
