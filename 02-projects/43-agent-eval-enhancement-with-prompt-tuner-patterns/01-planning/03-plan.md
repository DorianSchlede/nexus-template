# Agent Eval Enhancement - Plan

**Project Type**: Build
**Status**: Planning

---

## Context

**Load Before Reading**:
- `01-planning/02-discovery.md` - Requirements, prompts to extract, dependencies

---

## Approach

**Strategy**: Extract prompts from mutagent, adapt for agent context, create subagents and skills.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    AGENT EVAL ENHANCEMENT ARCHITECTURE                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  EXTRACTION LAYER (Phase 1)                                                  │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │  Source: mutagent-monorepo/prompt-tuner/                              │   │
│  │                                                                        │   │
│  │  failure-analysis-prompt.ts  ──┐                                      │   │
│  │  success-analysis-prompt.ts  ──┼──► 02-resources/extracted-prompts/   │   │
│  │  eval-criteria-prompt.ts     ──┘                                      │   │
│  │                                                                        │   │
│  │  prompt-failure-modes.ts     ──┬──► 02-resources/schemas/             │   │
│  │  prompt-success-modes.ts     ──┘                                      │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                     │                                        │
│                                     ▼                                        │
│  SUBAGENT LAYER (Phase 2)                                                   │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │  .claude/agents/                                                      │   │
│  │                                                                        │   │
│  │  ┌─────────────────────────┐   ┌─────────────────────────┐           │   │
│  │  │ agent-failure-analyzer  │   │ agent-success-analyzer  │           │   │
│  │  │ "spawn agent-failure-   │   │ "spawn agent-success-   │           │   │
│  │  │  analyzer"              │   │  analyzer"              │           │   │
│  │  │                         │   │                         │           │   │
│  │  │ - 9 root cause cats     │   │ - Pattern recognition   │           │   │
│  │  │ - WHY analysis          │   │ - Preservation priority │           │   │
│  │  │ - Origin tracing        │   │ - Success evidence      │           │   │
│  │  └─────────────────────────┘   └─────────────────────────┘           │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                     │                                        │
│                                     ▼                                        │
│  SKILL LAYER (Phase 3)                                                      │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │  03-skills/langfuse/                                                  │   │
│  │                                                                        │   │
│  │  ┌─────────────────────┐ ┌─────────────────────┐ ┌─────────────────┐ │   │
│  │  │ analyze-agent-      │ │ analyze-agent-      │ │ derive-eval-    │ │   │
│  │  │ failures/           │ │ successes/          │ │ criteria/       │ │   │
│  │  │                     │ │                     │ │                 │ │   │
│  │  │ SKILL.md            │ │ SKILL.md            │ │ SKILL.md        │ │   │
│  │  │ scripts/            │ │ scripts/            │ │ scripts/        │ │   │
│  │  │  analyze_failures.py│ │  analyze_successes.py│  derive_criteria.py │   │
│  │  └─────────────────────┘ └─────────────────────┘ └─────────────────┘ │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                     │                                        │
│                                     ▼                                        │
│  INTEGRATION LAYER (Phase 4)                                                │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │  Enhanced Existing Subagents                                          │   │
│  │                                                                        │   │
│  │  test-case-analyzer.md  ←── Add root cause analysis section           │   │
│  │  general-session-scorer.md ←── (Optional) Add failure mode output     │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Correctness Properties

**Property 1: Failure Mode Completeness**
For all failed agent traces, the agent-failure-analyzer SHALL identify at least one failure mode with a valid root cause category.
**Validates**: REQ-1, REQ-6

**Property 2: Success Mode Preservation**
For all successful agent traces, the agent-success-analyzer SHALL identify patterns with preservation priority that do not overlap with identified failure origins.
**Validates**: REQ-2

**Property 3: Skill Invocation**
For any session ID provided to the skills, the skill SHALL fetch traces from Langfuse and invoke the appropriate subagent.
**Validates**: REQ-3, REQ-4, REQ-NF-2

**Property 4: Schema Conformance**
For all subagent outputs, the output SHALL conform to the defined JSON schema for failure modes or success modes.
**Validates**: REQ-NF-3

---

## Key Decisions

| Decision | Choice | Rationale | Validates |
|----------|--------|-----------|-----------|
| Two-pass analysis | Success first, then failure | Prevents implicating working patterns (prompt-tuner pattern) | REQ-1, REQ-2 |
| Origin type adaptation | 4 agent-specific origin types | Agent traces differ from prompt executions | REQ-6 |
| Subagent invocation | Via Task tool with trigger phrase | Matches existing pattern from P36 | REQ-NF-1 |
| Skill structure | Follow langfuse/* pattern | Consistent with existing skills | REQ-3, REQ-4, REQ-5 |
| JSON output | Structured schema | Enables downstream processing | REQ-NF-3 |
| Session fetching | Reuse P36 Langfuse patterns | Proven, handles observations | REQ-NF-2 |

---

## Dependencies & Links

**Files to Modify**:
| File | Changes | Validates |
|------|---------|-----------|
| `.claude/agents/test-case-analyzer.md` | Add root cause section | REQ-7 |

**Files to Create**:
| File | Purpose | Validates |
|------|---------|-----------|
| `.claude/agents/agent-failure-analyzer.md` | Failure analysis subagent | REQ-1 |
| `.claude/agents/agent-success-analyzer.md` | Success analysis subagent | REQ-2 |
| `03-skills/langfuse/analyze-agent-failures/SKILL.md` | Failure skill definition | REQ-3 |
| `03-skills/langfuse/analyze-agent-failures/scripts/analyze_failures.py` | Failure skill CLI | REQ-3 |
| `03-skills/langfuse/analyze-agent-successes/SKILL.md` | Success skill definition | REQ-4 |
| `03-skills/langfuse/analyze-agent-successes/scripts/analyze_successes.py` | Success skill CLI | REQ-4 |
| `03-skills/langfuse/derive-eval-criteria/SKILL.md` | Criteria skill definition | REQ-5 |
| `03-skills/langfuse/derive-eval-criteria/scripts/derive_criteria.py` | Criteria skill CLI | REQ-5 |
| `02-resources/extracted-prompts/failure-analysis.md` | Extracted prompt | REQ-1 |
| `02-resources/extracted-prompts/success-analysis.md` | Extracted prompt | REQ-2 |
| `02-resources/extracted-prompts/eval-criteria.md` | Extracted prompt | REQ-5 |
| `02-resources/schemas/agent-failure-mode.yaml` | Failure schema | REQ-NF-3 |
| `02-resources/schemas/agent-success-mode.yaml` | Success schema | REQ-NF-3 |

**External Systems**:
- Langfuse: Trace storage and retrieval via existing skills
- Claude Task Tool: Subagent invocation

---

## Prompt Adaptation Strategy

### Failure Analysis Prompt Adaptation

| Original Concept | Agent Adaptation |
|------------------|------------------|
| PromptSection | AgentInstruction (section in agent definition) |
| MissingPromptSection | MissingAgentCapability (gap in agent abilities) |
| PromptVariable | ToolUsagePattern (how tools were used) |
| InputSchema | SessionContext (what context was available) |
| OutputSchema | ExpectedBehavior (what agent should have done) |

### Success Analysis Prompt Adaptation

| Original Concept | Agent Adaptation |
|------------------|------------------|
| Effective prompt sections | Effective agent instructions |
| Clear criteria definitions | Clear tool usage patterns |
| Explicit constraints | Explicit workflow adherence |
| Preservation priority | Keep in agent definition |

---

## Testing Strategy

### Property-Based Tests

| Property | Test Strategy |
|----------|---------------|
| P1: Failure Mode Completeness | Run on known-failed sessions, verify output contains failure modes |
| P2: Success Mode Preservation | Run on known-successful sessions, verify patterns identified |
| P3: Skill Invocation | Verify Langfuse fetch + subagent spawn works |
| P4: Schema Conformance | Validate output against YAML schema |

### Integration Tests

| Scenario | Test Cases |
|----------|------------|
| Failure analysis | Analyze session with tool misuse, verify correct category |
| Success analysis | Analyze clean session, verify preservation priorities |
| Criteria derivation | Generate criteria from 3 successful sessions |
| Enhanced test-case-analyzer | Verify root cause in validation reports |

---

## Success Criteria (from Mental Models)

**Must Pass**:
- [ ] All 3 prompts extracted and adapted
- [ ] 2 new subagents created with explicit triggers
- [ ] 3 new skills created and functional
- [ ] test-case-analyzer enhanced
- [ ] Tested on real session traces
- [ ] JSON output validates against schemas

**Quality Indicators**:
- Failure modes identify actionable root causes (not just "it failed")
- Success patterns have clear preservation rationale
- Derived criteria are specific enough to score

---

## Risks & Mitigations (from Pre-Mortem)

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Prompt adaptation loses nuance | Medium | High | Manual review, iterative testing |
| Agent traces differ from prompt executions | High | Medium | Custom origin types designed |
| Subagent output parsing fails | Low | Medium | Strict JSON schema validation |
| Token limits exceeded | Medium | Medium | Sampling strategy from P36 |

---

## Open Questions

| Question | Resolution | Validates |
|----------|------------|-----------|
| Two-pass analysis order? | Yes, success first then failure | REQ-1, REQ-2 |
| Augment or replace 6 dimensions? | Augment - derived criteria are additional | REQ-5 |
| Store results in Langfuse? | Yes, as annotations on traces | REQ-NF-2 |

---

*Execution steps in 04-steps.md*
