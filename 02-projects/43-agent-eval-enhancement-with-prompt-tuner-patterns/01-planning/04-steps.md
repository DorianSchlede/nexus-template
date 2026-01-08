# Agent Eval Enhancement - Execution Steps

**Project Type**: Build
**Status**: Planning

---

## Context Requirements

**Project Location**: `02-projects/43-agent-eval-enhancement-with-prompt-tuner-patterns/`

**Files to Load for Execution**:
- `01-planning/02-discovery.md` - Requirements, prompts to extract
- `01-planning/03-plan.md` - Approach and decisions

**Output Locations**:
- Subagents: `.claude/agents/`
- Skills: `03-skills/langfuse/`
- Schemas: `02-resources/schemas/`
- Extracted prompts: `02-resources/extracted-prompts/`

**Update Resume After Each Section**: Update `resume-context.md` with current_section, tasks_completed

---

## Phase 1: Extract and Adapt Prompts

**Goal**: Extract prompts from mutagent-monorepo and adapt for agent context
**Context**: Load 02-discovery.md for source file locations

### 1.1 Extract Failure Analysis Prompt **[REQ-1]**

- [ ] Read `mutagent-monorepo/.../failure-analysis-prompt.ts`
- [ ] Extract system prompt and human prompt sections
- [ ] Create `02-resources/extracted-prompts/failure-analysis.md` with:
  - Original prompt (for reference)
  - Adapted prompt (for agent context)
  - Mapping table showing concept adaptations
- [ ] Adapt terminology:
  - PromptSection → AgentInstruction
  - MissingPromptSection → MissingAgentCapability
  - PromptVariable → ToolUsagePattern
- [ ] **CHECKPOINT**: Failure analysis prompt extracted and adapted

### 1.2 Extract Success Analysis Prompt **[REQ-2]**

- [ ] Read `mutagent-monorepo/.../success-analysis-prompt.ts`
- [ ] Extract system prompt and human prompt sections
- [ ] Create `02-resources/extracted-prompts/success-analysis.md`
- [ ] Adapt terminology for agent context
- [ ] **CHECKPOINT**: Success analysis prompt extracted and adapted

### 1.3 Extract Eval Criteria Derivation Prompt **[REQ-5]**

- [ ] Read `mutagent-monorepo/.../eval-criteria-prompt.ts`
- [ ] Extract system prompt and human prompt sections
- [ ] Create `02-resources/extracted-prompts/eval-criteria.md`
- [ ] Adapt for agent sessions (vs prompt executions)
- [ ] **CHECKPOINT**: Eval criteria prompt extracted and adapted

### 1.4 Create Schemas **[REQ-NF-3]**

- [ ] Create `02-resources/schemas/agent-failure-mode.yaml` from prompt-failure-modes.ts
- [ ] Create `02-resources/schemas/agent-success-mode.yaml` from prompt-success-modes.ts
- [ ] Define agent-specific origin types:
  - AgentInstruction
  - ToolUsagePattern
  - ContextGap
  - WorkflowViolation
- [ ] **CHECKPOINT**: Schemas define structured output format

---

## Phase 2: Create Subagents

**Goal**: Create new subagents with adapted prompts
**Context**: Load extracted prompts from Phase 1

### 2.1 Create Agent Failure Analyzer **[REQ-1, REQ-6]**

- [ ] Create `.claude/agents/agent-failure-analyzer.md`
- [ ] Set trigger phrase: "spawn agent-failure-analyzer"
- [ ] Include adapted failure analysis prompt
- [ ] Define 9 root cause categories in agent context
- [ ] Define 4 origin types for agents
- [ ] Specify JSON output schema
- [ ] Add Langfuse skill access (get-session, get-trace)
- [ ] **CHECKPOINT**: Subagent created with correct trigger

### 2.2 Create Agent Success Analyzer **[REQ-2]**

- [ ] Create `.claude/agents/agent-success-analyzer.md`
- [ ] Set trigger phrase: "spawn agent-success-analyzer"
- [ ] Include adapted success analysis prompt
- [ ] Define preservation priority levels
- [ ] Specify JSON output schema
- [ ] Add Langfuse skill access
- [ ] **CHECKPOINT**: Subagent created with correct trigger

---

## Phase 3: Create Skills

**Goal**: Create skill wrappers for the subagents
**Context**: Load 03-plan.md for skill structure

### 3.1 Analyze Agent Failures Skill **[REQ-3]**

- [ ] Create folder: `03-skills/langfuse/analyze-agent-failures/`
- [ ] Create `SKILL.md` with:
  - Trigger phrases: "analyze failures", "why did session fail"
  - Usage examples with session ID
  - Output format description
- [ ] Create `scripts/analyze_failures.py`:
  - Accept --session-id argument
  - Fetch traces from Langfuse (reuse P36 patterns)
  - Format trace data for subagent
  - Output instructions to spawn subagent
- [ ] **CHECKPOINT**: Skill invocable via trigger phrase

### 3.2 Analyze Agent Successes Skill **[REQ-4]**

- [ ] Create folder: `03-skills/langfuse/analyze-agent-successes/`
- [ ] Create `SKILL.md` with:
  - Trigger phrases: "analyze successes", "what worked in session"
  - Usage examples
- [ ] Create `scripts/analyze_successes.py`:
  - Accept --session-id argument
  - Fetch traces from Langfuse
  - Format trace data for subagent
- [ ] **CHECKPOINT**: Skill invocable via trigger phrase

### 3.3 Derive Eval Criteria Skill **[REQ-5]**

- [ ] Create folder: `03-skills/langfuse/derive-eval-criteria/`
- [ ] Create `SKILL.md` with:
  - Trigger phrases: "derive criteria", "generate scoring criteria"
  - Usage: accepts multiple session IDs
- [ ] Create `scripts/derive_criteria.py`:
  - Accept --session-ids (comma-separated)
  - Fetch traces for all sessions
  - Identify successful sessions
  - Format for criteria derivation
- [ ] **CHECKPOINT**: Skill generates G-Eval compatible criteria

---

## Phase 4: Enhance Existing Subagents

**Goal**: Add root cause analysis to test-case-analyzer
**Context**: Load existing subagent definitions

### 4.1 Enhance Test Case Analyzer **[REQ-7]**

- [ ] Read `.claude/agents/test-case-analyzer.md`
- [ ] Add root cause analysis section from failure-analysis prompt
- [ ] Update report template to include:
  - Root cause category for each failure
  - Origin tracing (which agent instruction/tool caused it)
  - Actionable fix suggestions
- [ ] Keep existing PASS/FAIL format, add root cause details
- [ ] **CHECKPOINT**: Enhanced analyzer produces root cause analysis

### 4.2 (Optional) Enhance Session Scorer

- [ ]* Read `00-system/skills/meta/langfuse-score-session/prompts/scorer-prompt.md`
- [ ]* Add failure mode detection when score is low
- [ ]* Output failure modes alongside scores
- [ ] **CHECKPOINT**: Session scorer enhanced (optional)

---

## Phase 5: Integration Testing

**Goal**: Verify end-to-end flows work
**Context**: All components implemented

### 5.1 Test Failure Analysis Flow **[Property 1]**

- [ ] Find a session with known failures in Langfuse
- [ ] Run: `analyze failures in session {id}`
- [ ] Verify failure modes identified with:
  - Valid root cause category
  - Traced origin (AgentInstruction, ToolUsagePattern, etc.)
  - Supporting evidence
- [ ] Document session ID and results in `03-working/test-results.md`

### 5.2 Test Success Analysis Flow **[Property 2]**

- [ ] Find a successful session in Langfuse
- [ ] Run: `analyze successes in session {id}`
- [ ] Verify success modes identified with:
  - Preservation priority
  - Pattern description
  - Evidence from traces

### 5.3 Test Criteria Derivation Flow **[REQ-5]**

- [ ] Find 3 successful sessions
- [ ] Run: `derive criteria from sessions {id1},{id2},{id3}`
- [ ] Verify output includes:
  - G-Eval compatible criteria
  - Evaluation steps
  - Evidence grounding

### 5.4 Test Enhanced Test-Case-Analyzer **[REQ-7]**

- [ ] Run P41 validate-feature with test scenario
- [ ] Verify validation report includes root cause analysis
- [ ] Compare with previous report format

### 5.5 Verify Schema Conformance **[Property 4]**

- [ ] Validate failure mode output against schema
- [ ] Validate success mode output against schema
- [ ] **CHECKPOINT**: All outputs conform to schemas

---

## Phase 6: Finalization

**Goal**: Complete project and update state
**Context**: All validation passed

- [ ] Update `01-overview.md` success criteria checkboxes
- [ ] Update `resume-context.md`: current_phase: "complete"
- [ ] Create `04-outputs/test-results.md` with all test results
- [ ] Update `03-skills/langfuse/langfuse-connect/SKILL.md` to reference new skills
- [ ] Clean up any working files

---

## Summary

| Phase | Tasks | Optional | Checkpoints |
|-------|-------|----------|-------------|
| Phase 1: Extract | 16 | 0 | 4 |
| Phase 2: Subagents | 14 | 0 | 2 |
| Phase 3: Skills | 12 | 0 | 3 |
| Phase 4: Enhance | 7 | 3 | 2 |
| Phase 5: Testing | 12 | 0 | 1 |
| Phase 6: Finalize | 5 | 0 | 0 |
| **Total** | **66** | **3** | **12** |

---

## Quick Reference: Source Files

```
mutagent-monorepo/.../prompt-tuner/stages/
├── failure-analysis/llm/failure-analysis/failure-analysis-prompt.ts
├── failure-analysis/llm/success-analysis/success-analysis-prompt.ts
└── eval-mutation/llm/eval-criteria-derivation/eval-criteria-prompt.ts
```

## Quick Reference: Output Locations

```
.claude/agents/
├── agent-failure-analyzer.md    (NEW)
├── agent-success-analyzer.md    (NEW)
└── test-case-analyzer.md        (ENHANCED)

03-skills/langfuse/
├── analyze-agent-failures/      (NEW)
├── analyze-agent-successes/     (NEW)
└── derive-eval-criteria/        (NEW)
```

---

*Mark tasks complete with [x] as you finish them*
*Optional tasks marked with `*` can be skipped for faster MVP*
