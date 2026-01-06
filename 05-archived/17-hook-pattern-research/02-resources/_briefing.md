---
research_question: "What concrete implementation patterns exist for each of the 8 Claude Code hook event types, and what can be built with them?"

research_purpose: "Build a comprehensive pattern catalog for the Nexus Advanced Hook System (Project 14). Enable informed decisions about which patterns to implement first and how."

domain: "Claude Code Hooks / AI Agent Tooling"

extraction_schema:
  - field: session_start_patterns
    description: "Patterns for SessionStart hook: initialization, greeting, state setup, environment checks"
    priority: medium
    can_block: false

  - field: pre_tool_use_patterns
    description: "Patterns for PreToolUse hook: safety gates, validation, blocking, input modification, tool redirection"
    priority: high
    can_block: true

  - field: post_tool_use_patterns
    description: "Patterns for PostToolUse hook: logging, quality checks, notifications, result modification"
    priority: high
    can_block: true

  - field: pre_compact_patterns
    description: "Patterns for PreCompact hook: state preservation, context saving, checkpoint creation"
    priority: medium
    can_block: false

  - field: stop_patterns
    description: "Patterns for Stop hook: session cleanup, reports, summaries, notifications, TTS announcements"
    priority: medium
    can_block: true

  - field: subagent_stop_patterns
    description: "Patterns for SubagentStop hook: multi-agent communication, handoff, coordination, @-mention targeting"
    priority: medium
    can_block: true

  - field: user_prompt_submit_patterns
    description: "Patterns for UserPromptSubmit hook: input filtering, routing, enhancement, prompt injection detection"
    priority: medium
    can_block: true

  - field: notification_patterns
    description: "Patterns for Notification hook: desktop alerts, TTS, sound effects, visual feedback"
    priority: low
    can_block: false

  - field: sdk_abstractions
    description: "SDK/library patterns that abstract hook JSON protocol (Python, TypeScript, Go, PHP)"
    priority: medium

  - field: architecture_patterns
    description: "Overall architecture patterns: modular hooks, single-file scripts, handler registries, dependency injection"
    priority: high

  - field: context_loading_patterns
    description: "How hooks load context into Claude: systemMessage injection, CLAUDE.md modification, transcript reading, session state files"
    priority: high

  - field: use_case_catalog
    description: "Complete catalog of ALL use cases found with source attribution: what problem each hook solves"
    priority: high

focus_areas:
  - Safety and blocking patterns (rm, git, .env protection)
  - Input/output modification patterns
  - Multi-agent communication patterns
  - Performance optimization patterns
  - SDK abstraction patterns
  - Testing patterns
  - Context loading mechanisms (systemMessage, CLAUDE.md, state files)
  - Complete use case enumeration with sources

additional_research_questions:
  - "How can hooks inject context into Claude's working memory?"
  - "What mechanisms exist for hooks to communicate information TO Claude?"
  - "What is the complete inventory of use cases across all repos?"

skip_sections:
  - License files
  - CI/CD configuration
  - Package manager files (package.json deps, go.mod, etc.)
  - README badges and installation instructions
---

# Hook Pattern Research Briefing

## Research Question

> What concrete implementation patterns exist for each of the 8 Claude Code hook event types, and what can be built with them?

## Purpose

Build a comprehensive pattern catalog to inform implementation of the Nexus Advanced Hook System. This research will:

1. Identify ALL patterns across 10 community repositories
2. Categorize by hook event type (8 types)
3. Extract reusable code snippets and techniques
4. Generate "inspiration ideas" for novel applications
5. Prioritize patterns for Phase 1 implementation

## The 8 Hook Event Types

| # | Hook Event | Can Block | Fires When |
|---|------------|-----------|------------|
| 1 | **SessionStart** | No | Session begins (startup/resume/clear) |
| 2 | **PreToolUse** | Yes | Before any tool executes |
| 3 | **PostToolUse** | Yes | After tool completes |
| 4 | **PreCompact** | No | Before context compaction |
| 5 | **Stop** | Yes | Session ends |
| 6 | **SubagentStop** | Yes | Subagent task completes |
| 7 | **UserPromptSubmit** | Yes | User submits a prompt |
| 8 | **Notification** | No | Claude sends notification |

## Extraction Requirements

For each pattern found, extract:

1. **Pattern Name** - Descriptive identifier
2. **Hook Event** - Which of the 8 types
3. **Source Repository** - Where it came from
4. **Description** - What it does (1-2 sentences)
5. **Decision Type** - block/ask/allow/modify/none
6. **Key Technique** - Core implementation approach
7. **Code Snippet** - Relevant code (max 30 lines)
8. **Use Case** - When to use / when NOT to use
9. **Complexity** - low/medium/high
10. **Dependencies** - External packages needed

## Source Corpus

9 repositories containing Claude Code hook implementations:

1. claude-code-safety-net (Python) - rm/git safety
2. claude-code-tools (Python) - TRASH pattern, git safety
3. claude-code-hooks-mastery (Python) - ALL 8 hooks reference
4. claude-code-hooks (Python) - git-specific hooks
5. claude-codex-settings (Python) - tool redirection, quality
6. tdd-guard (TypeScript) - TDD enforcement
7. cc-tools (Go) - high-performance statusline
8. claude-hooks (TypeScript) - type definitions
9. awesome-claude-code (Markdown) - resource index

---

## Context Loading Mechanisms (KEY RESEARCH AREA)

Hooks can inject context into Claude through several mechanisms. Extract ALL instances of:

### 1. systemMessage Field
```json
{
  "systemMessage": "Additional context injected by hook..."
}
```
- When returned by a hook, this text is shown to Claude
- Can provide dynamic context based on hook logic

### 2. permissionDecisionReason
```json
{
  "hookSpecificOutput": {
    "permissionDecision": "deny",
    "permissionDecisionReason": "Blocked because... Use this instead..."
  }
}
```
- Explanation shown to Claude when blocking/asking
- Can guide Claude to alternative approaches

### 3. updatedInput Modification
```json
{
  "hookSpecificOutput": {
    "permissionDecision": "allow",
    "updatedInput": { "command": "modified command..." }
  }
}
```
- Silently modifies tool input before execution
- Claude sees the modification in PostToolUse

### 4. Transcript Reading
- Hooks receive `transcript_path` - can read full conversation
- Extract patterns that analyze transcript for context

### 5. State Files
- Session state files (JSON/YAML) that persist across hooks
- Patterns for maintaining context between hook invocations

### 6. CLAUDE.md Modification (Dynamic)
- Any patterns that modify CLAUDE.md at runtime
- Project-specific context injection

**For each context loading pattern found, extract:**
- Mechanism used (systemMessage, reason, updatedInput, etc.)
- What context is being loaded
- When/why this pattern is useful
- Source repo and file

---

## Use Case Catalog Requirements

For the `use_case_catalog` field, create a COMPLETE inventory:

| Use Case | Hook Type | Source Repo | Description |
|----------|-----------|-------------|-------------|
| {name} | {hook} | {repo} | {what it does} |

**Categories to look for:**
- Safety (blocking dangerous operations)
- Quality (enforcing code standards)
- Productivity (automation, shortcuts)
- Communication (notifications, TTS)
- Coordination (multi-agent, handoff)
- Context (state management, memory)
- Observability (logging, metrics)
