# Discovery

**Time**: 5-15 min max | **Purpose**: Surface dependencies before planning

---

## Context

**Load First**: `01-planning/01-overview.md` - Understand project purpose
**Output To**: `01-planning/03-plan.md` - Dependencies section auto-populated from this file

---

## System Overview

### What We're Building

A **subagent-based validation system** that tests new features before deployment by:

1. **Running N subagents** (5-10) executing the same feature scenario
2. **Storing transcripts in Langfuse** via session ID
3. **Running analyzer subagent** that reviews all traces
4. **Generating validation report** back to main agent

### Validation Targets

- New skills before deployment
- System changes (orchestrator, loaders)
- Hook changes
- Any feature that needs behavioral validation

### Two Modes

| Mode | Interactivity | Approach |
|------|---------------|----------|
| **Automated** | None | Subagents run scenario end-to-end |
| **Manual** | Required | User runs flow, then analyzer reviews traces |

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    MAIN AGENT                               │
│  (runs validate-feature skill)                              │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  │ 1. Load scenario definition
                  │ 2. Spawn N test subagents
                  ▼
┌─────────────────────────────────────────────────────────────┐
│              TEST SUBAGENTS (5-10x)                         │
│  - Load full Nexus context (same as main agent)             │
│  - Execute scenario prompt                                  │
│  - Transcripts stored in Langfuse via session_id            │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  │ 3. All test runs complete
                  │ 4. Collect session IDs
                  ▼
┌─────────────────────────────────────────────────────────────┐
│              ANALYZER SUBAGENT                              │
│  - Fetch traces from Langfuse for each session_id           │
│  - Evaluate against pass/fail criteria                      │
│  - Fill validation report template                          │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  │ 5. Return report to main agent
                  ▼
┌─────────────────────────────────────────────────────────────┐
│                    MAIN AGENT                               │
│  - Review report                                            │
│  - Decide: ship / fix / iterate                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Dependencies

### Files to Modify

- `00-system/.cache/session_start_context.xml` - Already exists, subagents read this

### Files to Create

**Skill:**
- `00-system/skills/system/validate-feature/SKILL.md` - Main validation skill

**Templates:**
- `00-system/skills/system/validate-feature/templates/scenario.md` - Scenario definition template
- `00-system/skills/system/validate-feature/templates/report.md` - Validation report template

**Scripts:**
- `00-system/skills/system/validate-feature/scripts/run_validation.py` - Orchestrates subagent runs
- `00-system/skills/system/validate-feature/scripts/analyze_traces.py` - Fetches Langfuse traces

### External Systems

- **Langfuse** - Trace storage and retrieval (already integrated via `03-skills/langfuse/`)
- **Claude Code Task tool** - Spawns subagents

---

## Existing Patterns

### Related Skills

- `03-skills/langfuse/langfuse-get-trace/SKILL.md` - Fetch individual traces
- `03-skills/langfuse/langfuse-list-traces/SKILL.md` - List traces by session
- `.claude/hooks/session_start.py` - Context injection pattern

### Related Projects

- `02-projects/28-handover-test-suite/` - Test suite patterns (98% complete)
- `02-projects/18-hook-research-upgrade/` - Hook patterns research

### Code Patterns

- **Subagent context loading**: `Read 00-system/.cache/session_start_context.xml` (validated today)
- **Langfuse API**: Already have skills for trace retrieval
- **Task tool parallel execution**: Can spawn multiple subagents in single message

---

## Scenario Definition Format

Each project that needs validation will define scenarios in a standard format:

```yaml
# In project's 02-resources/validation-scenarios.yaml
scenarios:
  - name: "basic_flow"
    description: "Test basic skill execution"
    prompt: |
      You are testing the X feature.
      FIRST: Read 00-system/.cache/session_start_context.xml
      THEN: Execute [specific action]
      REPORT: [what to output]
    pass_criteria:
      - "Output contains X"
      - "No errors in execution"
      - "Completed within 60 seconds"
    runs: 5  # Number of subagents to spawn

  - name: "edge_case_empty_input"
    description: "Test with empty input"
    prompt: |
      ...
    pass_criteria:
      - ...
    runs: 5
```

---

## Report Template Format

```markdown
# Validation Report: {feature_name}

**Date**: {timestamp}
**Scenarios Run**: {count}
**Overall Status**: PASS / FAIL / PARTIAL

## Summary

| Scenario | Runs | Passed | Failed | Pass Rate |
|----------|------|--------|--------|-----------|
| basic_flow | 5 | 5 | 0 | 100% |
| edge_case | 5 | 3 | 2 | 60% |

## Detailed Results

### Scenario: basic_flow

**Pass Criteria:**
- [x] Output contains X (5/5)
- [x] No errors (5/5)
- [x] Completed in time (5/5)

**Session IDs**: [link to Langfuse]

### Scenario: edge_case

**Pass Criteria:**
- [x] Output contains X (5/5)
- [ ] No errors (3/5) - FAILED
- [x] Completed in time (5/5)

**Failures:**
- Run 2: Error "..."
- Run 4: Error "..."

**Session IDs**: [link to Langfuse]

## Recommendation

{AI-generated recommendation based on results}
```

---

## Risks & Unknowns

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Langfuse rate limits | Medium | Batch trace fetches, add delays |
| Subagent context too large | Low | Already validated ~20K tokens works |
| Interactive flows can't be automated | High | Manual mode with post-hoc analysis |
| Flaky tests (non-deterministic) | Medium | Run 5-10x, look for patterns |
| Cost of running many subagents | Medium | Use haiku model for test runs |

**Open Questions:**
- [x] Can subagents read cached context? → YES (validated with 10/10 subagents)
- [x] How to handle scenarios that require user input mid-flow? → Manual mode: user runs, provides session IDs
- [x] Should analyzer subagent use same model as test subagents? → YES, use Sonnet for proper simulation
- [x] How to store/version scenario definitions per project? → In project's `02-resources/validation-scenarios.yaml`

**Dependencies Validated:**
- [x] Langfuse running at localhost:3002 (health check OK, version 3.143.0)
- [x] Project 27 research complete - session scorer spec ready
- [x] Subagent transcripts need validation - agentId returned (e.g., `a4920ea`)
- [ ] Langfuse trace capture for subagents - needs env var setup to verify

---

## EARS Requirements (Build Type)

### Core Requirements

**R1**: THE validate-feature skill SHALL spawn N subagents in parallel to execute a given scenario.

**R2**: WHEN a test subagent completes, THE system SHALL store its session_id for later analysis.

**R3**: WHEN all test subagents complete, THE system SHALL spawn an analyzer subagent to review traces.

**R4**: THE analyzer subagent SHALL fetch traces from Langfuse using stored session_ids.

**R5**: THE analyzer subagent SHALL evaluate each trace against defined pass_criteria.

**R6**: THE analyzer subagent SHALL generate a validation report using the standard template.

**R7**: THE validate-feature skill SHALL return the validation report to the main agent.

### Optional Requirements

**R8**: WHERE runs > 5, THE system SHALL use haiku model to reduce costs.

**R9**: WHERE scenario has `interactive: true`, THE system SHALL skip automated execution and prompt for manual run session_ids.

---

*Auto-populate 03-plan.md Dependencies section from findings above*
