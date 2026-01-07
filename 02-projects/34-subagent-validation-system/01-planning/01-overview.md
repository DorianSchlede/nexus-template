---
id: 34-subagent-validation-system
name: Subagent Validation System
status: PLANNING
type: build
description: "Build a subagent-based validation system to test new features before deployment using parallel test runs and Langfuse trace analysis."
created: 2026-01-07
project_path: 02-projects/34-subagent-validation-system/
---

# Subagent Validation System

## Project Files

| File | Purpose |
|------|---------|
| 01-overview.md | This file - purpose, success criteria |
| 02-discovery.md | Dependencies, patterns, risks |
| 03-plan.md | Approach, decisions |
| 04-steps.md | Execution tasks |
| 02-resources/ | Reference materials |
| 03-working/ | Work in progress |
| 04-outputs/ | Final deliverables |

---

## Purpose

Build a **skill-based validation system** that tests new features (skills, hooks, system changes) before deployment by:

1. Running N subagents (5-10) executing the same scenario in parallel
2. Storing transcripts in Langfuse via session IDs
3. Running an analyzer subagent to review all traces
4. Generating a validation report with pass/fail criteria

This enables **faster feature development** by catching issues before deployment through automated behavioral validation.

---

## Success Criteria

**Must achieve**:
- [ ] `validate-feature` skill created and functional
- [ ] Can spawn 5+ test subagents executing a scenario
- [ ] Can retrieve subagent traces from Langfuse
- [ ] Analyzer subagent evaluates traces against pass criteria
- [ ] Generates structured validation report
- [ ] Both automated and manual modes working

**Nice to have**:
- [ ] Support for interactive scenario validation (manual mode)
- [ ] Scenario templates for common validation patterns
- [ ] Integration with project workflow (auto-validate before merge)

---

## Context

**Background**:
- Validated that subagents can read `00-system/.cache/session_start_context.xml` (10/10 success)
- Langfuse running at localhost:3002 (health OK, version 3.143.0)
- Project 27 research complete - session scorer architecture ready
- Need to validate Langfuse trace capture for subagents before building

**Stakeholders**:
- Developer (primary) - faster feature validation
- Nexus system - quality assurance for skills/hooks

**Constraints**:
- Subagent traces must appear in Langfuse (needs validation)
- Sonnet model for proper simulation (not haiku)
- Non-interactive scenarios only for automated mode

---

*Next: See 02-discovery.md for dependencies*
