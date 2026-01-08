---
id: 41-integrated-subagent-testing-system
name: Integrated Subagent Testing System
status: EXECUTION
description: "10x the validation system: From manual meta-skill to integrated project testing"
created: 2026-01-07
project_path: 02-projects/41-integrated-subagent-testing-system/
---

# Integrated Subagent Testing System

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

Transform the manual `validate-feature` meta-skill (Project 34) into an **integrated testing system** that:

1. **Auto-generates test scenarios** when planning projects
2. **Runs tests via subagents** with automatic worktree isolation
3. **Analyzes results via Langfuse** using established patterns
4. **Stores test assets** in project's `02-resources/tests/` folder

**Key Shift**: From "manually invoke validate-feature" to "testing is part of the project workflow"

---

## Success Criteria

**Must achieve**:
- [x] Test scenarios auto-generated during project planning (in `02-resources/tests/`)
  - `init-tests.py` creates folder structure and copies template
- [x] Single YAML file defines all tests, script splits into individual test runs
  - `scenarios-template.yaml` defines schema, `run-tests.py` processes scenarios
- [x] All subagent tests use worktree isolation automatically
  - Default behavior in `run-tests.py`, uses `worktree-manager.py`
- [x] Test results written to `04-outputs/validation-reports/`
  - `test-case-analyzer` writes to this location
- [x] Langfuse trace fetching uses established patterns (from scorer-prompt.md)
  - `fetch-traces.py` with retry logic (5s, 10s, 15s) and GET /traces/{id}
- [x] Renamed analyzer: `test-case-analyzer` (not trace-analyzer)
  - Created `.claude/agents/test-case-analyzer.md`, removed trace-analyzer

**Nice to have**:
- [ ] Test templates per project type (build, integration, skill)
- [ ] Aggregated test dashboard across projects

---

## Context

**Background**:
- Project 34 built `validate-feature` skill with 4 modes (Automated, Manual, Interactive, Worktree)
- Custom subagents: `test-orchestrator`, `trace-analyzer` (explicit triggers)
- Langfuse integration documented but not using best patterns
- Project 36 (session-scorer) has proven Langfuse fetching patterns

**Stakeholders**:
- Developer (me) - wants automated quality validation
- Future projects - need standardized testing

**Constraints**:
- Must use explicit trigger phrases ("spawn test-orchestrator")
- Subagents must NOT know they're being tested (authentic behavior)
- Windows environment (encoding issues with Unicode)

---

## From Project 34 (What We Keep)

| Component | Status | Notes |
|-----------|--------|-------|
| `test-orchestrator.md` | KEEP | Rename to explicit trigger only |
| `trace-analyzer.md` | RENAME | → `test-case-analyzer.md` |
| `worktree-manager.py` | KEEP | Make automatic for all tests |
| `fetch-traces.py` | REFACTOR | Use session-scorer patterns |
| `SKILL.md` modes | REFACTOR | Simplify - always worktree |

---

*Next: Fill in 02-discovery.md*
