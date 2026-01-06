# HYPERPLAN: Hook Pattern Extraction & Synthesis

**Project:** Advanced Hook System - Pattern Research
**Date:** 2025-12-31
**Objective:** Extract concrete implementation patterns for ALL 8 hook types from 10 repositories

---

## Research Question

> **For each of the 8 Claude Code hook event types, what concrete patterns, use cases, and implementation examples exist in the community?**

---

## The 8 Hook Event Types (Target)

| # | Hook Event | Can Block | Primary Use Cases |
|---|------------|-----------|-------------------|
| 1 | **SessionStart** | No | Initialization, greeting, state setup |
| 2 | **PreToolUse** | **Yes** | Safety gates, validation, input modification |
| 3 | **PostToolUse** | **Yes** | Logging, quality checks, notifications |
| 4 | **PreCompact** | No | State preservation, context save |
| 5 | **Stop** | **Yes** | Session cleanup, reports, notifications |
| 6 | **SubagentStop** | **Yes** | Subagent coordination, handoff |
| 7 | **UserPromptSubmit** | **Yes** | Input filtering, routing, enhancement |
| 8 | **Notification** | No | Alerts, TTS, desktop notifications |

---

## Source Repositories (10 total)

| # | Repository | Primary Hook Focus | Language |
|---|------------|-------------------|----------|
| 1 | claude-code-safety-net | PreToolUse (rm, git) | Python |
| 2 | claude-code-tools | PreToolUse (safety), PostToolUse | Python |
| 3 | claude-code-hooks-mastery | ALL 8 hooks (reference impl) | Python |
| 4 | claude-code-hooks (EvanL1) | PreToolUse (git-specific) | Python |
| 5 | claude-codex-settings | PreToolUse (quality), PostToolUse | Python |
| 6 | tdd-guard | PreToolUse (TDD enforcement) | TypeScript |
| 7 | cc-tools | PostToolUse (statusline) | Go |
| 8 | claude-hooks | ALL hooks (type definitions) | TypeScript |
| 9 | cchooks | SDK abstraction | Python |
| 10 | HCOM | SubagentStop (multi-agent comm) | Python |

---

## Extraction Schema (Per Hook Type)

For each hook event found, extract:

```yaml
hook_event: "PreToolUse"
pattern_name: "rm-rf-blocking"
source_repo: "claude-code-safety-net"
description: "Blocks dangerous rm -rf commands with path-aware allowlist"

# Implementation details
matcher: "Bash"  # What triggers this hook
decision_type: "block|ask|allow|modify"
exit_code_used: 0|2|other

# Code patterns
key_technique: "Regex pattern matching with temp path allowlist"
code_snippet: |
  patterns = [
    r'\brm\s+.*-[a-z]*r[a-z]*f',
    ...
  ]

# Use case
use_case: "Prevent accidental deletion of important files"
when_to_use: "Always for any codebase with destructive operations"
when_not_to_use: "Temp/sandbox environments where deletion is expected"

# Quality
complexity: "low|medium|high"
performance_impact: "<10ms|10-50ms|50-100ms|>100ms"
dependencies: ["none|external packages"]
```

---

## Multi-Agent Extraction Strategy

### Wave 1: Repository Deep-Dive (10 parallel agents)

Each agent extracts ALL hook patterns from ONE repository:

```
Agent 1: claude-code-safety-net → patterns_safety_net.md
Agent 2: claude-code-tools → patterns_tools.md
Agent 3: claude-code-hooks-mastery → patterns_mastery.md
Agent 4: claude-code-hooks (EvanL1) → patterns_evanl1.md
Agent 5: claude-codex-settings → patterns_codex.md
Agent 6: tdd-guard → patterns_tdd_guard.md
Agent 7: cc-tools → patterns_cc_tools.md
Agent 8: claude-hooks → patterns_claude_hooks.md
Agent 9: cchooks → patterns_cchooks.md
Agent 10: HCOM → patterns_hcom.md
```

**Agent Prompt Template:**

```markdown
## Hook Pattern Extraction Task: {repo_name}

### INPUT CONTRACT (STRICT)
1. READ the repository at: 04-workspace/repos/{repo_name}/
2. Find ALL hook implementations (settings.json, *.py, *.ts, *.go)
3. For EACH hook found, extract using the schema below

### EXTRACTION SCHEMA
For each hook implementation found, create an entry:

```yaml
- hook_event: "{SessionStart|PreToolUse|PostToolUse|PreCompact|Stop|SubagentStop|UserPromptSubmit|Notification}"
  pattern_name: "{descriptive-name}"
  source_repo: "{repo_name}"
  source_file: "{relative/path/to/file.py}"
  description: "{1-2 sentence description}"

  implementation:
    matcher: "{tool pattern or empty}"
    decision_type: "{block|ask|allow|modify|none}"
    exit_code: "{0|2|other}"

  technique:
    summary: "{key technique in 1 sentence}"
    code_snippet: |
      {relevant code, max 20 lines}

  use_case:
    when_to_use: "{scenario}"
    when_not_to_use: "{anti-pattern}"

  quality:
    complexity: "{low|medium|high}"
    performance: "{estimate}"
    dependencies: ["{list}"]
```

### OUTPUT CONTRACT
Write to: 02-projects/14-advanced-hook-system/02-research/patterns/{repo_name}.yaml

Include ALL hooks found. If repo has 0 hooks for a type, note it.
```

### Wave 2: Hook-Type Synthesis (8 parallel agents)

After extraction, synthesize patterns BY HOOK TYPE:

```
Agent A: Synthesize ALL SessionStart patterns → SESSION_START_PATTERNS.md
Agent B: Synthesize ALL PreToolUse patterns → PRE_TOOL_USE_PATTERNS.md
Agent C: Synthesize ALL PostToolUse patterns → POST_TOOL_USE_PATTERNS.md
Agent D: Synthesize ALL PreCompact patterns → PRE_COMPACT_PATTERNS.md
Agent E: Synthesize ALL Stop patterns → STOP_PATTERNS.md
Agent F: Synthesize ALL SubagentStop patterns → SUBAGENT_STOP_PATTERNS.md
Agent G: Synthesize ALL UserPromptSubmit patterns → USER_PROMPT_PATTERNS.md
Agent H: Synthesize ALL Notification patterns → NOTIFICATION_PATTERNS.md
```

**Synthesis Agent Prompt Template:**

```markdown
## Hook Pattern Synthesis: {HookEventName}

### INPUT CONTRACT
Read ALL extracted pattern files:
- 02-research/patterns/patterns_safety_net.yaml
- 02-research/patterns/patterns_tools.yaml
- ... (all 10 files)

Filter for: hook_event == "{HookEventName}"

### SYNTHESIS REQUIREMENTS
Create a comprehensive guide for this hook type:

1. **Overview**
   - What this hook does
   - When it fires
   - Can it block? (Yes/No)
   - JSON input schema
   - JSON output schema

2. **Pattern Catalog**
   For each unique pattern found:
   - Pattern name
   - Source repos (may appear in multiple)
   - Description
   - Implementation approach
   - Code example (best version)
   - Pros/cons

3. **Inspiration Ideas**
   Based on patterns, suggest NEW use cases:
   - What ELSE could this hook do?
   - Combinations with other hooks
   - Advanced applications

4. **Implementation Recommendations**
   - Best patterns to adopt
   - Patterns to avoid
   - Performance considerations
   - Testing approach

### OUTPUT CONTRACT
Write to: 02-research/hook-guides/{HOOK_EVENT_NAME}_PATTERNS.md
```

---

## Execution Plan

### Phase 1: Repository Cloning (if needed)

```bash
# Check which repos need cloning
repos=(
  "cchooks:https://github.com/GowayLee/cchooks"
  "HCOM:https://github.com/aannoo/claude-hook-comms"
)

for repo in "${repos[@]}"; do
  name="${repo%%:*}"
  url="${repo#*:}"
  if [ ! -d "04-workspace/repos/$name" ]; then
    git clone "$url" "04-workspace/repos/$name"
  fi
done
```

### Phase 2: Wave 1 Execution (10 parallel agents)

```python
# Spawn 10 extraction agents in parallel
agents = []
for repo in REPOSITORIES:
    agent = Task(
        subagent_type="general-purpose",
        prompt=EXTRACTION_PROMPT.format(repo_name=repo),
        description=f"Extract patterns from {repo}"
    )
    agents.append(agent)

# Wait for all to complete
results = await gather(*agents)
```

### Phase 3: Wave 2 Execution (8 parallel agents)

```python
# Spawn 8 synthesis agents in parallel
HOOK_TYPES = [
    "SessionStart", "PreToolUse", "PostToolUse", "PreCompact",
    "Stop", "SubagentStop", "UserPromptSubmit", "Notification"
]

agents = []
for hook_type in HOOK_TYPES:
    agent = Task(
        subagent_type="general-purpose",
        prompt=SYNTHESIS_PROMPT.format(hook_type=hook_type),
        description=f"Synthesize {hook_type} patterns"
    )
    agents.append(agent)

results = await gather(*agents)
```

### Phase 4: Final Integration

Create master document: `HOOK_PATTERN_CATALOG.md`

```markdown
# Claude Code Hook Pattern Catalog

## Quick Reference
| Hook Type | # Patterns | Key Use Cases | Recommended |
|-----------|------------|---------------|-------------|
| SessionStart | 5 | Init, greeting, state | ★★★ |
| PreToolUse | 23 | Safety, validation | ★★★★★ |
| ... | ... | ... | ... |

## Detailed Guides
1. [SessionStart Patterns](hook-guides/SESSION_START_PATTERNS.md)
2. [PreToolUse Patterns](hook-guides/PRE_TOOL_USE_PATTERNS.md)
...
```

---

## Output Structure

```
02-projects/14-advanced-hook-system/02-research/
├── patterns/                      # Wave 1 outputs (per-repo)
│   ├── patterns_safety_net.yaml
│   ├── patterns_tools.yaml
│   ├── patterns_mastery.yaml
│   ├── patterns_evanl1.yaml
│   ├── patterns_codex.yaml
│   ├── patterns_tdd_guard.yaml
│   ├── patterns_cc_tools.yaml
│   ├── patterns_claude_hooks.yaml
│   ├── patterns_cchooks.yaml
│   └── patterns_hcom.yaml
│
├── hook-guides/                   # Wave 2 outputs (per-hook-type)
│   ├── SESSION_START_PATTERNS.md
│   ├── PRE_TOOL_USE_PATTERNS.md
│   ├── POST_TOOL_USE_PATTERNS.md
│   ├── PRE_COMPACT_PATTERNS.md
│   ├── STOP_PATTERNS.md
│   ├── SUBAGENT_STOP_PATTERNS.md
│   ├── USER_PROMPT_PATTERNS.md
│   └── NOTIFICATION_PATTERNS.md
│
└── HOOK_PATTERN_CATALOG.md        # Final integration
```

---

## Success Criteria

- [ ] All 10 repos analyzed
- [ ] All 8 hook types have synthesis documents
- [ ] Each synthesis has 3+ concrete patterns
- [ ] Each synthesis has "Inspiration Ideas" section
- [ ] Master catalog created with recommendations
- [ ] Actionable patterns ready for Phase 1 implementation

---

## Timeline

| Phase | Agents | Est. Time |
|-------|--------|-----------|
| Wave 1 (Extraction) | 10 parallel | 5-10 min |
| Wave 2 (Synthesis) | 8 parallel | 5-10 min |
| Integration | 1 | 5 min |
| **Total** | | **15-25 min** |

---

**Ready to execute?** Say "run wave 1" to start extraction.
