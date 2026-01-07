# Agent Eval Enhancement - Discovery

**Project Type**: Build
**Purpose**: Extract prompt-tuner patterns for agent evaluation enhancement and skill creation

---

## Requirements (EARS Format)

### Functional Requirements

**REQ-1**: THE `agent-failure-analyzer` subagent SHALL analyze agent traces and identify failure modes using the 9-category taxonomy

**REQ-2**: THE `agent-success-analyzer` subagent SHALL analyze agent traces and identify success patterns to preserve

**REQ-3**: THE `analyze-agent-failures` skill SHALL accept a session ID and return structured failure modes with root causes

**REQ-4**: THE `analyze-agent-successes` skill SHALL accept a session ID and return structured success patterns with preservation priority

**REQ-5**: THE `derive-eval-criteria` skill SHALL analyze successful sessions and generate G-Eval compatible scoring criteria

**REQ-6**: WHEN failure modes are identified, THE system SHALL trace each failure to a specific origin (agent instruction, tool usage, or context)

**REQ-7**: THE `test-case-analyzer` subagent SHALL be enhanced with root cause analysis capabilities from the failure analysis prompt

### Non-Functional Requirements

**REQ-NF-1**: THE subagents SHALL use explicit trigger phrases ("spawn agent-failure-analyzer")

**REQ-NF-2**: THE skills SHALL integrate with existing Langfuse trace fetching patterns from Project 36

**REQ-NF-3**: THE failure mode output SHALL follow a structured JSON schema for downstream processing

### Quality Checklist (INCOSE)

- [x] All requirements use EARS patterns (THE/WHEN/WHILE/IF/WHERE)
- [x] No vague terms (quickly, adequate, reasonable, user-friendly)
- [x] No pronouns (it, them, they) - specific names used
- [x] Each requirement independently testable
- [x] Active voice throughout
- [x] No escape clauses (where possible, if feasible)
- [x] Solution-free (what, not how)

---

## Prompts to Extract

### 1. Failure Analysis Prompt

**Source**: `mutagent-monorepo/.../failure-analysis-prompt.ts`

**Key Components**:
- CIA Agent role with Root Cause Analysis expertise
- Recursive WHY analysis methodology
- 9 Root Cause Categories:
  1. `INSTRUCTION_AMBIGUITY` - Unclear or conflicting instructions
  2. `MISSING_CONTEXT` - Required context not provided
  3. `MISSING_SECTION` - Entire section absent
  4. `OUTPUT_FORMAT_MISMATCH` - Output doesn't match expectations
  5. `CONSTRAINT_VIOLATION` - Guardrails not followed
  6. `REASONING_GAP` - Missing reasoning steps
  7. `EDGE_CASE_UNHANDLED` - Scenario not covered
  8. `VARIABLE_MISUSE` - Variable used incorrectly
  9. `SCHEMA_DESCRIPTION_WEAK` - Schema description insufficient

**Adaptation for Agents**:
- Replace "PromptSection" with "AgentInstruction"
- Replace "PromptVariable" with "ToolUsage" or "ContextElement"
- Map failure origins to agent definition components

### 2. Success Analysis Prompt

**Source**: `mutagent-monorepo/.../success-analysis-prompt.ts`

**Key Components**:
- Success Pattern Analyst role
- Pattern recognition across multiple executions
- Preservation priority levels: LOW, MEDIUM, HIGH, CRITICAL
- Granularity rules for one origin = one success mode

**Adaptation for Agents**:
- Focus on agent behaviors that work
- Identify tool usage patterns that succeed
- Extract workflow patterns to preserve

### 3. Eval Criteria Derivation Prompt

**Source**: `mutagent-monorepo/.../eval-criteria-prompt.ts`

**Key Components**:
- G-Eval methodology for LLM evaluation
- Train of Thought reasoning capture
- 3-5 evaluation steps per criterion
- 0-1 scoring scale
- Counter-example integration

**Adaptation for Agents**:
- Derive agent-specific scoring dimensions
- Generate criteria from successful sessions
- Create dynamic scoring rubrics (vs static 6 dimensions)

---

## Dependencies

### Files to Modify

| File | Changes Needed |
|------|----------------|
| `.claude/agents/test-case-analyzer.md` | Add root cause analysis section from failure prompt |
| `.claude/agents/general-session-scorer.md` | Optionally add failure mode output |

### Files to Create

| File | Purpose |
|------|---------|
| `.claude/agents/agent-failure-analyzer.md` | New subagent for failure analysis |
| `.claude/agents/agent-success-analyzer.md` | New subagent for success analysis |
| `03-skills/langfuse/analyze-agent-failures/SKILL.md` | Skill wrapper for failure analysis |
| `03-skills/langfuse/analyze-agent-failures/scripts/analyze_failures.py` | CLI for failure analysis |
| `03-skills/langfuse/analyze-agent-successes/SKILL.md` | Skill wrapper for success analysis |
| `03-skills/langfuse/analyze-agent-successes/scripts/analyze_successes.py` | CLI for success analysis |
| `03-skills/langfuse/derive-eval-criteria/SKILL.md` | Skill for criteria derivation |
| `03-skills/langfuse/derive-eval-criteria/scripts/derive_criteria.py` | CLI for criteria derivation |
| `02-resources/schemas/agent-failure-mode.yaml` | Schema for failure mode output |
| `02-resources/schemas/agent-success-mode.yaml` | Schema for success mode output |

### External Systems

- **Langfuse**: Trace storage and retrieval via existing skills
- **Claude Task Tool**: Subagent invocation

---

## Existing Patterns to Reuse

| Pattern | Location | Reuse Strategy |
|---------|----------|----------------|
| Session fetching | `general-session-scorer.md` | Copy Langfuse skill invocation pattern |
| Trace analysis | `general-session-scorer.md` | Reuse trace examination approach |
| JSON output schema | `general-session-scorer.md` | Follow same structured output pattern |
| Skill structure | `03-skills/langfuse/*` | Copy folder structure and SKILL.md format |
| Root cause categories | `prompt-failure-modes.ts` | Adapt taxonomy for agent context |

---

## Failure Mode Taxonomy (Adapted for Agents)

| Category | Prompt Context | Agent Context |
|----------|----------------|---------------|
| `INSTRUCTION_AMBIGUITY` | Unclear prompt instructions | Unclear agent definition |
| `MISSING_CONTEXT` | Missing runtime context | Missing session context |
| `MISSING_SECTION` | Missing prompt section | Missing agent capability |
| `OUTPUT_FORMAT_MISMATCH` | Wrong output structure | Wrong tool output handling |
| `CONSTRAINT_VIOLATION` | Guardrail not followed | Tool usage policy violated |
| `REASONING_GAP` | Missing reasoning steps | Missing planning/thinking |
| `EDGE_CASE_UNHANDLED` | Scenario not covered | Unusual input not handled |
| `VARIABLE_MISUSE` | Input variable misused | Tool parameter misused |
| `SCHEMA_DESCRIPTION_WEAK` | Schema description weak | Tool description weak |

---

## Agent Failure Origin Types

| Origin Type | Description | Example |
|-------------|-------------|---------|
| `AgentInstruction` | Instruction in agent definition | "Follow the orchestrator.md routing rules" |
| `ToolUsagePattern` | How a tool was used | "Used Bash instead of Read for file" |
| `ContextGap` | Missing context in session | "Did not read Nexus context first" |
| `WorkflowViolation` | Workflow not followed | "Skipped TodoWrite for multi-step task" |

---

## Risks & Unknowns

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Prompt adaptation loses nuance | Medium | High | Careful manual review of adapted prompts |
| Agent traces differ from prompt executions | High | Medium | Design agent-specific origin types |
| Subagent output parsing fails | Low | Medium | Strict JSON schema validation |
| Token limits exceeded for large sessions | Medium | Medium | Sampling strategy from P36 |

### Open Questions

- [x] How to map prompt sections to agent components? → Use AgentInstruction, ToolUsagePattern, ContextGap, WorkflowViolation
- [ ] Should failure analyzer call success analyzer first (like prompt-tuner)? → Recommend yes for consistency
- [ ] Should derived criteria replace or augment static 6 dimensions? → Recommend augment

---

## Source File Locations

```
C:\Users\dsber\infinite\auto-company\mutagent-monorepo\mutagent\src\framework\metatuner\pipelines\prompt-tuner\
├── stages/
│   ├── failure-analysis/
│   │   └── llm/
│   │       ├── failure-analysis/
│   │       │   ├── failure-analysis-prompt.ts      ← EXTRACT
│   │       │   └── failure-analysis-schema.ts      ← EXTRACT
│   │       └── success-analysis/
│   │           ├── success-analysis-prompt.ts      ← EXTRACT
│   │           └── success-analysis-schema.ts      ← EXTRACT
│   └── eval-mutation/
│       └── llm/
│           └── eval-criteria-derivation/
│               ├── eval-criteria-prompt.ts         ← EXTRACT
│               └── eval-criteria-schema.ts         ← EXTRACT
└── types/
    ├── prompt-failure-modes.ts                     ← EXTRACT (taxonomy)
    └── prompt-success-modes.ts                     ← EXTRACT (taxonomy)
```

---

*This discovery document is MANDATORY. It preserves intelligence across compaction.*
