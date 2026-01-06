# Hook Pattern Catalog

**Generated**: 2026-01-01
**Project**: 17-hook-pattern-research
**Purpose**: Comprehensive catalog of Claude Code hook patterns for Project 14 (Advanced Hook System)

---

## Executive Summary

This catalog synthesizes **150+ hook patterns** from **9 community repositories** across **8 hook event types**. The research provides concrete implementation examples, context loading mechanisms, and use cases for building the Nexus Advanced Hook System.

### Key Findings

1. **PreToolUse dominates** - 60%+ of patterns focus on pre-execution validation/blocking
2. **Safety patterns are mature** - rm/git/env protection well-established
3. **Context loading underutilized** - Only 3 repos use systemMessage injection
4. **SDK abstractions emerging** - TypeScript (claude-hooks) and Go (cc-tools) lead
5. **Multi-agent patterns nascent** - SubagentStop patterns rare but high-value

---

## Quick Reference

### Hook Events at a Glance

| Hook Event | Can Block | Primary Use Cases | Guide |
|------------|-----------|-------------------|-------|
| **SessionStart** | No | Context injection, state init, greetings | [SESSION_START.md](../02-resources/hook-guides/SESSION_START.md) |
| **PreToolUse** | Yes (exit 2) | Safety gates, validation, tool redirection | [PRE_TOOL_USE.md](../02-resources/hook-guides/PRE_TOOL_USE.md) |
| **PostToolUse** | Yes (exit 2) | Quality checks, auto-format, notifications | [POST_TOOL_USE.md](../02-resources/hook-guides/POST_TOOL_USE.md) |
| **PreCompact** | No | State preservation, checkpoints | [PRE_COMPACT.md](../02-resources/hook-guides/PRE_COMPACT.md) |
| **Stop** | Yes | Session cleanup, reports, TTS | [STOP.md](../02-resources/hook-guides/STOP.md) |
| **SubagentStop** | Yes | Multi-agent coordination | [SUBAGENT_STOP.md](../02-resources/hook-guides/SUBAGENT_STOP.md) |
| **UserPromptSubmit** | Yes | Input filtering, routing, commands | [USER_PROMPT.md](../02-resources/hook-guides/USER_PROMPT.md) |
| **Notification** | No | Desktop alerts, TTS, sound | [NOTIFICATION.md](../02-resources/hook-guides/NOTIFICATION.md) |

### Cross-Cutting Guides

| Guide | Purpose |
|-------|---------|
| [CONTEXT_LOADING.md](../02-resources/hook-guides/CONTEXT_LOADING.md) | How hooks inject context INTO Claude |
| [USE_CASE_CATALOG.md](../02-resources/hook-guides/USE_CASE_CATALOG.md) | Complete inventory of all use cases |

---

## Source Repositories

| Repo | Language | Focus | Patterns |
|------|----------|-------|----------|
| claude-code-safety-net | Python | rm/git safety | 18 |
| claude-code-tools | Python | TRASH, git, statusline | 9 |
| claude-code-hooks-mastery | Python | All 8 hooks reference | 25+ |
| claude-code-hooks (evanl1) | Python | Git-specific | 14 |
| claude-codex-settings | Python | Tool redirection, quality | 14 |
| tdd-guard | TypeScript | TDD enforcement | 28 |
| cc-tools | Go | High-perf statusline | 16 |
| claude-hooks | TypeScript | SDK/types | 13 |
| awesome-claude-code | Markdown | Resource index | 20 |

**Total Pattern Files**: 19 YAML files (~11,500 lines)
**Total Hook Guides**: 10 MD files (~8,100 lines)

---

## Top 10 Patterns for Project 14

Based on impact/complexity analysis:

| Rank | Pattern | Hook | Source | Why |
|------|---------|------|--------|-----|
| 1 | **Dangerous Command Blocker** | PreToolUse | safety-net | Essential safety, well-tested |
| 2 | **TRASH Pattern** | PreToolUse | cc-tools-py | Non-destructive rm alternative |
| 3 | **TDD Guard** | PreToolUse | tdd-guard | Quality enforcement framework |
| 4 | **Context Injection** | SessionStart | hooks-mastery | Dynamic context loading |
| 5 | **Tool Redirection** | PreToolUse | codex-settings | WebSearch→Tavily pattern |
| 6 | **Auto-Formatter Chain** | PostToolUse | codex-settings | Quality pipeline |
| 7 | **Statusline** | UserPromptSubmit | cc-tools-go | High-perf Go implementation |
| 8 | **TTS Notification** | Notification | hooks-mastery | Multi-provider cascade |
| 9 | **Transcript Backup** | PreCompact | hooks-mastery | State preservation |
| 10 | **Resume Handler** | UserPromptSubmit | cc-tools-py | Session handoff |

---

## Context Loading Mechanisms

| Mechanism | How It Works | Best For |
|-----------|--------------|----------|
| `systemMessage` | JSON output field injected as system message | Dynamic context, guidance |
| `permissionDecisionReason` | Shown when blocking/asking | Teaching Claude alternatives |
| `updatedInput` | Silently modifies tool input | Tool redirection, enhancement |
| Transcript reading | Hook reads `transcript_path` | Conversation analysis |
| State files | Persist JSON/YAML between hooks | Cross-hook coordination |
| CLAUDE.md modification | Edit project instructions | Persistent context |

See [CONTEXT_LOADING.md](../02-resources/hook-guides/CONTEXT_LOADING.md) for detailed examples.

---

## Implementation Recommendations for Nexus

### Phase 1: Essential Safety (Immediate)

1. **PreToolUse safety gate** - Block rm -rf, git reset --hard, env access
2. **TRASH pattern** - Move files instead of delete
3. **Git protection** - Block force push, branch delete

### Phase 2: Quality & Productivity

1. **TDD enforcement** - Block code without tests
2. **Auto-formatters** - PostToolUse quality chain
3. **Statusline** - Context usage visualization

### Phase 3: Advanced Features

1. **Context injection** - SessionStart dynamic loading
2. **Multi-agent coordination** - SubagentStop patterns
3. **Tool redirection** - WebSearch→Tavily pattern

### Architecture Recommendations

1. **Use SDK abstractions** - Don't reinvent JSON protocol
2. **Fail gracefully** - Exit 0 on errors (except safety)
3. **Performance budget** - PreToolUse <10ms, PostToolUse <50ms
4. **Modular design** - One file per hook type

---

## File Index

### Pattern Extractions (`02-resources/patterns/`)

```
safety-net.yaml           # rm/git safety patterns
cc-tools-py.yaml          # TRASH, git, statusline
hooks-mastery-part1.yaml  # SessionStart, PreToolUse, PostToolUse
hooks-mastery-part2.yaml  # PreCompact, Stop, SubagentStop
hooks-mastery-part3.yaml  # UserPromptSubmit, Notification
hooks-evanl1.yaml         # Git-specific hooks
codex-settings.yaml       # Tool redirection, quality
tdd-guard-part1.yaml      # Core handlers, config
tdd-guard-part2.yaml      # Test detection, state
cc-tools-go.yaml          # High-perf Go statusline
claude-hooks-ts.yaml      # TypeScript SDK patterns
awesome.yaml              # Resource index
context-loading.yaml      # Cross-cutting: context mechanisms
sdk-abstractions.yaml     # Cross-cutting: SDK patterns
```

### Hook Guides (`02-resources/hook-guides/`)

```
SESSION_START.md          # SessionStart patterns
PRE_TOOL_USE.md           # PreToolUse patterns (largest)
POST_TOOL_USE.md          # PostToolUse patterns
PRE_COMPACT.md            # PreCompact patterns
STOP.md                   # Stop patterns
SUBAGENT_STOP.md          # SubagentStop patterns
USER_PROMPT.md            # UserPromptSubmit patterns
NOTIFICATION.md           # Notification patterns
CONTEXT_LOADING.md        # How to inject context
USE_CASE_CATALOG.md       # Complete use case inventory
```

---

## Next Steps

1. **Review hook guides** - Start with [PRE_TOOL_USE.md](../02-resources/hook-guides/PRE_TOOL_USE.md)
2. **Select Phase 1 patterns** - Safety essentials
3. **Design Nexus hook architecture** - Use SDK patterns from [sdk-abstractions.yaml](../02-resources/patterns/sdk-abstractions.yaml)
4. **Implement** - Follow examples in pattern files

---

*Generated by Project 17: Hook Pattern Research*
*For Project 14: Advanced Hook System*
