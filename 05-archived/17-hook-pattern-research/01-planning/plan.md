# Hook Pattern Research - Plan

**Last Updated**: 2025-12-31
**Status**: PLANNING

---

## Research Question

> **What concrete implementation patterns exist for each of the 8 Claude Code hook event types, and what can be built with them?**

## Research Purpose

Build a comprehensive pattern catalog for the Nexus Advanced Hook System (Project 14). Enable informed decisions about which patterns to implement first.

---

## Approach

**Multi-Agent Repository Analysis** using the research-pipeline pattern:

1. **Wave 1 (10 parallel agents)**: Each agent deep-dives ONE repository, extracts ALL hook patterns
2. **Wave 2 (8 parallel agents)**: Each agent synthesizes ONE hook type across all repos
3. **Integration**: Create master HOOK_PATTERN_CATALOG.md with recommendations

---

## Current State

| Metric | Value |
|--------|-------|
| Phase | 2-Extraction (Ready) |
| Repositories Indexed | 9 |
| Repos Cloned & Ready | 9 |
| Patterns Extracted | 0 |
| Synthesis Complete | No |

---

## Source Corpus (10 Repositories)

| # | Repo ID | Repository | Language | Primary Focus | Status |
|---|---------|------------|----------|---------------|--------|
| 1 | safety-net | claude-code-safety-net | Python | rm/git safety | ready |
| 2 | cc-tools-py | claude-code-tools | Python | TRASH, git safety | ready |
| 3 | hooks-mastery | claude-code-hooks-mastery | Python | ALL 8 hooks | ready |
| 4 | hooks-evanl1 | claude-code-hooks | Python | git-specific | ready |
| 5 | codex-settings | claude-codex-settings | Python | tool redirection | ready |
| 6 | tdd-guard | tdd-guard | TypeScript | TDD enforcement | ready |
| 7 | cc-tools-go | cc-tools | Go | statusline | ready |
| 8 | claude-hooks-ts | claude-hooks | TypeScript | type definitions | ready |
| 9 | awesome | awesome-claude-code | Markdown | resource index | ready |

**Repo Path**: `04-workspace/00-ai-native-org/hook-repos/{repo-name}/`

**Note**: 9 repos cloned and ready. awesome-claude-code provides pattern index reference.

---

## Extraction Schema

For each pattern found, extract:

```yaml
- pattern_name: "{descriptive-name}"
  hook_event: "{SessionStart|PreToolUse|PostToolUse|PreCompact|Stop|SubagentStop|UserPromptSubmit|Notification}"
  source_repo: "{repo_id}"
  source_file: "{path/to/file}"
  description: "{1-2 sentences}"

  implementation:
    matcher: "{tool pattern or empty}"
    decision_type: "{block|ask|allow|modify|none}"
    exit_code: "{0|2|other}"

  technique:
    summary: "{key technique in 1 sentence}"
    code_snippet: |
      {relevant code, max 30 lines}

  use_case:
    when_to_use: "{scenario}"
    when_not_to_use: "{anti-pattern}"

  quality:
    complexity: "{low|medium|high}"
    performance: "{<10ms|10-50ms|50-100ms|>100ms}"
    dependencies: ["{list}"]
```

---

## Subagent Allocation Plan

### Wave 1: Repository Extraction (10 agents)

| Agent | Repo ID | Est. Files | Subagents | Output |
|-------|---------|------------|-----------|--------|
| W1-01 | safety-net | ~15 | 1 | patterns/safety-net.yaml |
| W1-02 | cc-tools-py | ~20 | 1 | patterns/cc-tools-py.yaml |
| W1-03 | hooks-mastery | ~25 | 1 | patterns/hooks-mastery.yaml |
| W1-04 | hooks-evanl1 | ~15 | 1 | patterns/hooks-evanl1.yaml |
| W1-05 | codex-settings | ~10 | 1 | patterns/codex-settings.yaml |
| W1-06 | tdd-guard | ~30 | 1 | patterns/tdd-guard.yaml |
| W1-07 | cc-tools-go | ~20 | 1 | patterns/cc-tools-go.yaml |
| W1-08 | claude-hooks-ts | ~15 | 1 | patterns/claude-hooks-ts.yaml |
| W1-09 | cchooks | ~10 | 1 | patterns/cchooks.yaml |
| W1-10 | hcom | ~10 | 1 | patterns/hcom.yaml |

**Total Wave 1 subagents**: 10
**Max concurrent**: 10 (all parallel)

### Wave 2: Hook-Type Synthesis (8 agents)

| Agent | Hook Type | Input Files | Output |
|-------|-----------|-------------|--------|
| W2-A | SessionStart | all 9 pattern files | hook-guides/SESSION_START.md |
| W2-B | PreToolUse | all 9 pattern files | hook-guides/PRE_TOOL_USE.md |
| W2-C | PostToolUse | all 9 pattern files | hook-guides/POST_TOOL_USE.md |
| W2-D | PreCompact | all 9 pattern files | hook-guides/PRE_COMPACT.md |
| W2-E | Stop | all 9 pattern files | hook-guides/STOP.md |
| W2-F | SubagentStop | all 9 pattern files | hook-guides/SUBAGENT_STOP.md |
| W2-G | UserPromptSubmit | all 9 pattern files | hook-guides/USER_PROMPT.md |
| W2-H | Notification | all 9 pattern files | hook-guides/NOTIFICATION.md |

### Wave 2b: Cross-Cutting Synthesis (2 agents)

| Agent | Topic | Input Files | Output |
|-------|-------|-------------|--------|
| W2-I | Context Loading | all 9 pattern files | hook-guides/CONTEXT_LOADING.md |
| W2-J | Use Case Catalog | all 9 pattern files | hook-guides/USE_CASE_CATALOG.md |

**Total Wave 2 subagents**: 10 (8 hook types + 2 cross-cutting)
**Max concurrent**: 10 (all parallel)

---

## Orchestrator Instructions

### Constants

```
PROJECT_PATH = "02-projects/17-hook-pattern-research"
REPOS_PATH = "04-workspace/00-ai-native-org/hook-repos"  # Cloned repositories
PATTERNS_OUTPUT = "02-projects/17-hook-pattern-research/02-resources/patterns"
GUIDES_OUTPUT = "02-projects/17-hook-pattern-research/02-resources/hook-guides"
BRIEFING = "02-projects/17-hook-pattern-research/02-resources/_briefing.md"
```

### Phase 1: Wave 1 - Repository Extraction

**Spawn 10 agents in parallel:**

```python
for repo in REPOSITORIES:
    Task(
        subagent_type="general-purpose",
        prompt=f"""
## Hook Pattern Extraction: {repo.id}

### INPUT CONTRACT (STRICT)
1. READ the briefing: {BRIEFING}
2. READ the repository at: {REPOS_PATH}/{repo.path}/
3. Find ALL hook implementations:
   - settings.json / .claude/settings.json
   - *.py files with hook logic
   - *.ts files with hook handlers
   - *.go files with hook implementations
4. For EACH hook found, extract using the schema in _briefing.md

### SEARCH STRATEGY
1. First find settings.json to understand hook configuration
2. Then trace each hook command to its implementation file
3. Look for patterns in:
   - Exit code handling (0, 2, other)
   - JSON stdin/stdout parsing
   - Decision logic (block/ask/allow)
   - Input modification (updatedInput)

### FILES TO IGNORE
- node_modules/, vendor/, .git/
- Test files (unless they show usage patterns)
- Documentation (unless it describes patterns)
- Package manager files

### OUTPUT CONTRACT
Write YAML to: {PATTERNS_OUTPUT}/{repo.id}.yaml

Format:
```yaml
repo_id: "{repo.id}"
repo_name: "{repo.name}"
language: "{repo.language}"
extracted_at: "{{timestamp}}"

patterns:
  - pattern_name: "..."
    hook_event: "..."
    # ... full schema from _briefing.md
```

Include ALL hooks found. If repo has 0 patterns for a hook type, note it in a `hooks_not_found` section.
""",
        description=f"Extract {repo.id} patterns"
    )
```

### Phase 2: Wave 2 - Hook-Type Synthesis

**After Wave 1 completes, spawn 8 agents in parallel:**

```python
HOOK_TYPES = [
    ("SessionStart", "SESSION_START"),
    ("PreToolUse", "PRE_TOOL_USE"),
    ("PostToolUse", "POST_TOOL_USE"),
    ("PreCompact", "PRE_COMPACT"),
    ("Stop", "STOP"),
    ("SubagentStop", "SUBAGENT_STOP"),
    ("UserPromptSubmit", "USER_PROMPT"),
    ("Notification", "NOTIFICATION"),
]

for hook_event, filename in HOOK_TYPES:
    Task(
        subagent_type="general-purpose",
        prompt=f"""
## Hook Pattern Synthesis: {hook_event}

### INPUT CONTRACT
Read ALL pattern files from: {PATTERNS_OUTPUT}/
- patterns/safety-net.yaml
- patterns/cc-tools-py.yaml
- patterns/hooks-mastery.yaml
- patterns/hooks-evanl1.yaml
- patterns/codex-settings.yaml
- patterns/tdd-guard.yaml
- patterns/cc-tools-go.yaml
- patterns/claude-hooks-ts.yaml
- patterns/cchooks.yaml
- patterns/hcom.yaml

Filter for: hook_event == "{hook_event}"

### SYNTHESIS REQUIREMENTS

Create a comprehensive guide with these sections:

## 1. Overview
- What this hook does
- When it fires (trigger conditions)
- Can it block? (Yes/No)
- JSON input schema (what data the hook receives)
- JSON output schema (valid responses)

## 2. Pattern Catalog
For each unique pattern found:

### Pattern: {{pattern_name}}
**Sources**: {{repos where found}}
**Description**: {{what it does}}
**Decision Type**: {{block/ask/allow/modify}}

**Implementation**:
```{{language}}
{{best code example}}
```

**Pros**:
- {{advantage 1}}
- {{advantage 2}}

**Cons**:
- {{limitation 1}}

**Use When**: {{scenario}}
**Avoid When**: {{anti-pattern}}

## 3. Inspiration Ideas
Based on patterns found, suggest NEW use cases:
- What ELSE could this hook do?
- Combinations with other hooks?
- Advanced applications?
- Patterns from other domains that could apply?

## 4. Implementation Recommendations
- Best patterns to adopt (ranked)
- Patterns to avoid
- Performance considerations
- Testing approach

### OUTPUT CONTRACT
Write to: {GUIDES_OUTPUT}/{filename}.md
""",
        description=f"Synthesize {hook_event} patterns"
    )
```

### Phase 3: Integration

**After Wave 2 completes:**

1. Read all 8 hook guide files
2. Create `HOOK_PATTERN_CATALOG.md` with:
   - Quick reference table (hook type, pattern count, key use cases)
   - Links to detailed guides
   - Overall recommendations for Project 14

---

## Key Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| **YAML vs JSON for patterns** | YAML | More readable, easier to edit |
| **10 parallel then 8 parallel** | Two waves | Dependencies: synthesis needs extraction first |
| **Repo-first vs hook-first** | Repo-first extraction | Better context per repo |

---

## Dependencies & Links

**Related Projects**:
- Project 14: Advanced Hook System - Consumer of this research

**Files Impacted**:
- `02-projects/14-advanced-hook-system/02-research/SYNTHESIS.md` - Will be updated with patterns

**External Repositories** (to clone if missing):
- https://github.com/GowayLee/cchooks
- https://github.com/aannoo/claude-hook-comms

---

## Open Questions

- [x] Which repos to include? → 9 repos available
- [x] Extraction schema fields? → 12 fields defined (8 hooks + 4 cross-cutting)
- [x] Clone missing repos? → Not needed, 9 repos ready at hook-repos/
- [x] Re-use existing findings? → Fresh extraction for comprehensive patterns

---

## Success Criteria

- [ ] All 10 repos analyzed
- [ ] All 8 hook types have synthesis documents
- [ ] Each synthesis has 3+ concrete patterns
- [ ] Each synthesis has "Inspiration Ideas" section
- [ ] Master catalog created with recommendations
- [ ] Patterns actionable for Project 14 Phase 1

---

*Next: Execute Wave 1 extraction*
