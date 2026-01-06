# Hook Pattern Research - Execution Steps

**Last Updated**: 2025-12-31
**Current Phase**: Phase 3 - Wave 2 Synthesis (In Progress)

**IMPORTANT**: This file tracks project progress. Mark tasks complete with [x] as you finish them.

---

## Phase 1: Planning & Setup

- [x] Create project structure (Project 17)
- [x] Define research question and extraction schema
- [x] Create _briefing.md with hook types as fields
- [x] Create corpus table (9 repos as sources)
- [x] Generate orchestrator instructions in plan.md
- [x] Create output directories (patterns/, hook-guides/)
- [x] Verify repository availability (9 repos ready)

---

## Phase 2: Wave 1 - Repository Pattern Extraction

**Strategy**: Spawn 12 parallel agents with splits for large repos.

- [x] W1-01: Extract patterns from claude-code-safety-net → patterns/safety-net.yaml
- [x] W1-02: Extract patterns from claude-code-tools → patterns/cc-tools-py.yaml
- [x] W1-03a: Extract patterns from hooks-mastery (tool hooks) → patterns/hooks-mastery-tool.yaml
- [x] W1-03b: Extract patterns from hooks-mastery (session hooks) → patterns/hooks-mastery-session.yaml
- [x] W1-03c: Extract patterns from hooks-mastery (user hooks) → patterns/hooks-mastery-user.yaml
- [x] W1-04: Extract patterns from claude-code-hooks → patterns/hooks-evanl1.yaml
- [x] W1-05: Extract patterns from claude-codex-settings → patterns/codex-settings.yaml
- [x] W1-06a: Extract patterns from tdd-guard (pre-tool) → patterns/tdd-guard-pre.yaml
- [x] W1-06b: Extract patterns from tdd-guard (other hooks) → patterns/tdd-guard-other.yaml
- [x] W1-07: Extract patterns from cc-tools → patterns/cc-tools-go.yaml
- [x] W1-08: Extract patterns from claude-hooks → patterns/claude-hooks-ts.yaml
- [x] W1-09: Extract patterns from awesome-claude-code → patterns/awesome.yaml

**Status**: COMPLETE - 15 YAML files generated (~400KB total patterns)

---

## Phase 3: Wave 2 - Hook-Type Synthesis

**Strategy**: Spawn 10 parallel agents (8 hook types + 2 cross-cutting topics).

### Per Hook Type (8 agents)
- [ ] W2-A: Synthesize SessionStart patterns → hook-guides/SESSION_START.md
- [ ] W2-B: Synthesize PreToolUse patterns → hook-guides/PRE_TOOL_USE.md
- [ ] W2-C: Synthesize PostToolUse patterns → hook-guides/POST_TOOL_USE.md
- [ ] W2-D: Synthesize PreCompact patterns → hook-guides/PRE_COMPACT.md
- [ ] W2-E: Synthesize Stop patterns → hook-guides/STOP.md
- [x] W2-F: Synthesize SubagentStop patterns → hook-guides/SUBAGENT_STOP.md
- [ ] W2-G: Synthesize UserPromptSubmit patterns → hook-guides/USER_PROMPT.md
- [ ] W2-H: Synthesize Notification patterns → hook-guides/NOTIFICATION.md

### Cross-Cutting Topics (2 agents)
- [ ] W2-I: Synthesize Context Loading patterns → hook-guides/CONTEXT_LOADING.md
- [ ] W2-J: Compile Use Case Catalog → hook-guides/USE_CASE_CATALOG.md

---

## Phase 4: Integration & Delivery

- [ ] Create HOOK_PATTERN_CATALOG.md (master reference)
- [ ] Update Project 14 SYNTHESIS.md with pattern links
- [ ] Generate implementation recommendations for Phase 1
- [ ] Mark project complete

---

## Notes

**Current blockers**: None

**Dependencies**:
- Project 14 will consume the pattern catalog for implementation

**Output Files**:
- `02-resources/patterns/*.yaml` - Raw extracted patterns (Wave 1)
- `02-resources/hook-guides/*.md` - Synthesized guides per hook type (Wave 2)
- `04-outputs/HOOK_PATTERN_CATALOG.md` - Master reference (Phase 4)

---

*Mark tasks complete with [x] as you finish them*
