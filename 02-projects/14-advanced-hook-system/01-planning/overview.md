---
id: 14-advanced-hook-system
name: Advanced Hook System for Nexus
status: PLANNING
description: Load when user mentions 'hooks', 'pre-tool-use', 'safety guards', 'observability', 'session hooks'
created: 2025-12-31
---

# Advanced Hook System for Nexus

## Goal

Implement a comprehensive Claude Code hook system for Nexus that:
1. **Automates startup** - No more manual nexus-loader commands
2. **Enables multi-session** - 10+ parallel Claude sessions with isolated caches
3. **Adds safety guards** - Block dangerous commands before execution

## Hooks to Implement

### 1. SessionStart Hook (HIGH PRIORITY)
**Input** (from Claude Code):
```json
{
  "session_id": "abc123",
  "source": "startup" | "resume" | "clear" | "compact",
  "hook_event_name": "SessionStart"
}
```

**Behavior**:
- Write `$NEXUS_SESSION_ID` to `$CLAUDE_ENV_FILE` for persistence
- Output nexus-loader command via stdout → injected as context
- Detect startup vs resume from `source` field

**Output** (stdout → additionalContext):
```
Run: python 00-system/core/nexus-loader.py --startup --session "abc123"
```

### 2. PreToolUse Hook (Safety)
**Matcher**: `Bash` (only intercept shell commands)

**Blocks** (exit code 2):
- `rm -rf /`, `rm -rf ~`, `rm -rf *` patterns
- `.env` file access (except `.env.sample`)

**Allows** (exit code 0):
- All other commands pass through

### 3. PreCompact Hook (EXISTING)
Already implemented in Project 12. Saves `_resume.md` before context compaction.

## Multi-Session Architecture

```
Session A (session_id: abc123)          Session B (session_id: def456)
├── $NEXUS_SESSION_ID = abc123          ├── $NEXUS_SESSION_ID = def456
├── context_startup_abc123.json         ├── context_startup_def456.json
└── Independent project work            └── Independent project work
```

## Key Technical Details

| Feature | Implementation |
|---------|----------------|
| State Detection | `source` field: startup/resume/clear/compact |
| Env Persistence | Write to `$CLAUDE_ENV_FILE` |
| Context Injection | stdout with exit 0 → additionalContext |
| Blocking | stderr with exit 2 → shown to Claude |
| Multi-Session | Session-isolated cache files |

## Files to Create

```
.claude/hooks/
├── session_start.py     # Auto-startup, env persistence
├── pre_tool_use.py      # Safety guards
├── save_resume_state.py # (existing) PreCompact hook
└── utils/
    ├── safety.py        # rm -rf, .env detection patterns
    └── platform.py      # Windows UTF-8 encoding fix
```

## Critical Findings from Research

### SessionStart Hook - Known Issues & Workarounds

**Bug (Issue #13650)**: SessionStart stdout can be silently dropped in some versions.

**Workarounds**:
1. Wrap `additionalContext` in XML-like tags: `<Context>...</Context>`
2. Use v2.0.76+ where this is reportedly fixed
3. Keep output concise and well-formatted

**Working Pattern**:
```python
result = {
    "hookSpecificOutput": {
        "hookEventName": "SessionStart",
        "additionalContext": "<NexusContext>\n" + content + "\n</NexusContext>"
    }
}
print(json.dumps(result), flush=True)
sys.exit(0)
```

### PreToolUse Safety Patterns (from claude-code-safety-net)

**Credential File Protection**:
```python
# Block .env but allow .env.sample, .env.example
r'\.env(?!\.sample|\.example)'
# Block: client_secret.json, .credentials.json, token.pickle
# Block: *.pem, *.key certificate files
```

**Destructive Command Detection**:
```python
# rm patterns (6 variants)
r'\brm\s+.*-[a-z]*r[a-z]*f'      # rm -rf, rm -fr, rm -Rf
r'\brm\s+--recursive\s+--force'  # long form
r'\brm\s+-r\s+.*-f'              # separated flags

# Dangerous paths (with recursive flag)
dangerous_paths = ['/', '/*', '~', '~/', '$HOME', '..', '*', '.']
```

**Git Blocking**:
```python
# Block: git push --force, git reset --hard, git config --global
# Allow: git checkout -b (new branch), git push (normal)
```

### Multi-Session Architecture Options

| Approach | Isolation | Complexity | Best For |
|----------|-----------|------------|----------|
| **Session ID Only** | Cache files | Low | Most cases |
| **Git Worktree** | Full filesystem | Medium | Parallel features |
| **ccswarm/ccmanager** | Full + orchestration | High | Agent teams |

**For Nexus**: Session ID isolation is sufficient - just namespace cache files.

### Environment Variable Persistence

**CLAUDE_ENV_FILE** is the key:
```python
env_file = os.environ.get("CLAUDE_ENV_FILE")
if env_file:
    with open(env_file, "a") as f:
        f.write(f'export NEXUS_SESSION_ID="{session_id}"\n')
```

This persists across ALL subsequent Bash commands in the session.

## References

- Official: [Claude Code Hooks Reference](https://code.claude.com/docs/en/hooks)
- Safety: [claude-code-safety-net](https://github.com/kenryu42/claude-code-safety-net)
- YOLO Safety: [Taming Claude YOLO Mode](https://www.agentic-engineer.com/blog/2025-10-13-taming-claude-yolo-mode)
- Examples: [Steve Kinney Hook Examples](https://stevekinney.com/courses/ai-development/claude-code-hook-examples)
- Multi-session: [GitButler Parallel Sessions](https://blog.gitbutler.com/parallel-claude-code)
- Bug Tracker: [SessionStart stdout issue #13650](https://github.com/anthropics/claude-code/issues/13650)
- Pattern: `04-workspace/00-ai-native-org/hook-system-reference.system.doc.md`
