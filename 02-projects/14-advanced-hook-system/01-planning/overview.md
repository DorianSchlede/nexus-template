---
id: 14-advanced-hook-system
name: Advanced Hook System for Nexus
status: PLANNING
description: Load when user mentions 'hooks', 'pre-tool-use', 'safety guards', 'observability', 'session hooks'
created: 2025-12-31
---

# Advanced Hook System for Nexus

## Goal

Implement a comprehensive Claude Code hook system for Nexus based on the Architech hook architecture. This extends beyond the PreCompact hook to cover safety, observability, and session management.

## Hooks to Implement

### 1. PreToolUse Hook (Safety)
- Block dangerous `rm -rf` commands
- Protect `.env` files from access
- Validate bash commands before execution

### 2. SessionStart Hook
- Auto-run `nexus-loader.py --startup` on new sessions
- Detect resume vs fresh start
- Set environment variables for session

### 3. PostToolUse Hook (Optional)
- Log tool executions for observability
- Track file modifications

### 4. Stop Hook (Optional)
- Validate task completion before stopping
- Ensure todo list is updated

## Key Features from Architech Reference

- Fire-and-forget observability (never blocks)
- Exit code 2 = BLOCK, Exit code 0 = ALLOW
- JSON input via stdin
- Platform compatibility (Windows UTF-8)

## Files to Create

```
.claude/hooks/
├── pre_tool_use.py      # Safety guards
├── session_start.py     # Auto-startup
├── utils/
│   ├── safety.py        # rm -rf, .env detection
│   └── platform.py      # UTF-8 encoding fix
```

## Reference

Based on: `04-workspace/00-ai-native-org/hook-system-reference.system.doc.md`
