---
id: 43-agent-eval-enhancement-with-prompt-tuner-patterns
name: Agent Eval Enhancement with Prompt-Tuner Patterns
status: PLANNING
description: "Enhance agent evaluation subagents with prompt-tuner's analysis patterns and create reusable skills"
created: 2026-01-07
project_path: 02-projects/43-agent-eval-enhancement-with-prompt-tuner-patterns/
type: build
---

# Agent Eval Enhancement with Prompt-Tuner Patterns

## Project Files

| File | Purpose |
|------|---------|
| 01-overview.md | This file - purpose, success criteria |
| 02-discovery.md | Prompts to extract, patterns, dependencies |
| 03-plan.md | Approach, decisions |
| 04-steps.md | Execution tasks |
| 02-resources/ | Extracted prompts and schemas |
| 03-working/ | Work in progress |
| 04-outputs/ | Enhanced subagents and skills |

---

## Purpose

Extract the sophisticated analysis patterns from Mutagent's **prompt-tuner pipeline** and integrate them into Nexus's agent evaluation system. This creates:

1. **Enhanced subagents** with deeper analysis capabilities
2. **Reusable skills** for failure analysis, success analysis, and eval criteria generation

**Key Principle**: No new pipeline - enhance existing scoring prompt (`scorer-prompt.md`) and `test-case-analyzer` subagent with prompt-tuner's intelligence.

---

## Source System Analysis

**Source**: `mutagent-monorepo/mutagent/src/framework/metatuner/pipelines/prompt-tuner/`

### What Prompt-Tuner Has (7 Stages)

| Stage | Purpose | Extract? |
|-------|---------|----------|
| dataset-analysis | Validate inputs, route | No - infrastructure |
| dataset-execution | Run prompts, collect results | No - we have this |
| **failure-analysis** | Root cause identification | **YES - core value** |
| **success-analysis** | Identify winning patterns | **YES - core value** |
| **eval-mutation** | Derive scoring criteria | **YES - core value** |
| prompt-mutation | Apply text improvements | Maybe - for agent improvement |
| phase-mutation | Stagnation handling | No - optimization loop |
| mutation-evaluation | Score mutations | No - optimization loop |
| result-analysis | Termination decision | No - optimization loop |

### Key Extractions

| Component | Source File | Target |
|-----------|-------------|--------|
| Failure Analysis Prompt | `failure-analysis-prompt.ts` | Subagent + Skill |
| Success Analysis Prompt | `success-analysis-prompt.ts` | Subagent + Skill |
| Eval Criteria Derivation | `eval-criteria-prompt.ts` | Skill |
| Failure Taxonomy (9 categories) | `prompt-failure-modes.ts` | Schema |
| Success Mode Schema | `prompt-success-modes.ts` | Schema |

---

## What We'll Build

### 1. Enhanced Subagents

| Subagent | Enhancement | Based On |
|----------|-------------|----------|
| `scorer-prompt.md` | Add failure mode detection | failure-analysis-prompt |
| `test-case-analyzer` | Root cause analysis, not just PASS/FAIL | failure-analysis-prompt |
| `agent-failure-analyzer` (NEW) | Dedicated failure analysis | failure-analysis-prompt |
| `agent-success-analyzer` (NEW) | Dedicated success pattern extraction | success-analysis-prompt |

### 2. New Skills

| Skill | Purpose | Invocation |
|-------|---------|------------|
| `analyze-agent-failures` | Deep failure analysis on traces | "analyze failures in session X" |
| `analyze-agent-successes` | Extract winning patterns | "what worked in session X" |
| `derive-eval-criteria` | Auto-generate scoring criteria | "derive scoring criteria from sessions" |

### 3. Schemas (for structured output)

| Schema | Based On | Purpose |
|--------|----------|---------|
| `AgentFailureMode` | `PromptFailureMode` | Structured failure data |
| `AgentSuccessMode` | `PromptSuccessMode` | Structured success data |
| `AgentEvalCriteria` | `PromptEvaluation` | Derived scoring criteria |

---

## Integration with Existing Projects

### Project 36 (Session Scorer)

**Current**: Static 6-dimension scoring
**Enhanced**:
- Failure mode detection when score is low
- Success pattern identification when score is high
- Dynamic criteria based on learned patterns

### Project 41 (Integrated Testing)

**Current**: Basic PASS/FAIL per criterion
**Enhanced**:
- Root cause analysis for failures
- Actionable fix suggestions
- Pattern detection across test runs

---

## Success Criteria

**Must achieve**:
- [ ] Failure analysis prompt extracted and adapted for agents
- [ ] Success analysis prompt extracted and adapted for agents
- [ ] Eval criteria derivation prompt extracted
- [ ] `agent-failure-analyzer` subagent created with 9-category taxonomy
- [ ] `agent-success-analyzer` subagent created
- [ ] `analyze-agent-failures` skill created and tested
- [ ] `analyze-agent-successes` skill created and tested
- [ ] `derive-eval-criteria` skill created and tested
- [ ] `test-case-analyzer` enhanced with root cause analysis
- [ ] Tested on real session traces

**Nice to have**:
- [ ] `scorer-prompt.md` enhanced with failure mode output
- [ ] Agent improvement suggestions based on failures

---

## Context

**Background**:
- Project 36 (Session Scorer) has static 6-dimension scoring
- Project 41 (Testing System) has basic PASS/FAIL analysis
- Mutagent's prompt-tuner has sophisticated failure/success analysis that we want to reuse

**Stakeholders**:
- Developer (me) - wants deeper insight into agent behavior
- Future agent development - benefits from learned patterns

**Constraints**:
- Must use explicit trigger phrases for subagents
- Skills should be standalone (usable without full pipeline)
- Langfuse integration for trace storage

---

## Estimated Effort

Medium-Large (4-6 sessions)
- Phase 1: Extract prompts and schemas (~1 session)
- Phase 2: Create subagents (~1-2 sessions)
- Phase 3: Create skills (~1-2 sessions)
- Phase 4: Integration and testing (~1 session)

---

## Reference Materials

**Source Codebase**:
- `C:\Users\dsber\infinite\auto-company\mutagent-monorepo\mutagent\src\framework\metatuner\pipelines\prompt-tuner\`

**Key Files to Extract**:
- `stages/failure-analysis/llm/failure-analysis/failure-analysis-prompt.ts`
- `stages/failure-analysis/llm/success-analysis/success-analysis-prompt.ts`
- `stages/eval-mutation/llm/eval-criteria-derivation/eval-criteria-prompt.ts`
- `types/prompt-failure-modes.ts`
- `types/prompt-success-modes.ts`

**Existing Nexus Assets**:
- `00-system/skills/meta/langfuse-score-session/prompts/scorer-prompt.md` (scoring instructions)
- `.claude/agents/test-case-analyzer.md`
- `02-projects/36-session-scorer/`
- `02-projects/41-integrated-subagent-testing-system/`

---

*Next: See 02-discovery.md for detailed prompt extraction*
