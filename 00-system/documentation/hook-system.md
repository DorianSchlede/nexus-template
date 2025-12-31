# Nexus Hook System

This document describes the Claude Code hook system used by Nexus for automatic context injection, session management, and safety guards.

## Overview

Nexus uses Claude Code hooks to:
1. **Auto-inject context** - Load Nexus context directly into Claude's conversation (no manual commands)
2. **Manage sessions** - Track session lifecycle (start, resume, compact, end)
3. **Preserve state** - Save resume state before context compaction
4. **Enforce safety** - Block dangerous commands before execution

## Key Insight: "Skills Inform, Hooks Enforce"

The critical difference between skills and hooks:
- **Skills** = Claude knows preferences (can be ignored)
- **Hooks** = Claude cannot forget them (enforced by system)

**Important**: Don't tell Claude to run a command - run it FOR Claude and inject the result directly.

## Hook Files

```
.claude/hooks/
├── session_start.py     # Auto-inject Nexus context on startup/resume
├── pre_tool_use.py      # Safety guards for dangerous commands
├── save_resume_state.py # Preserve state before compaction (PreCompact)
├── session_end.py       # Cleanup on session termination
└── utils/
    ├── http.py          # HTTP utilities for server communication
    ├── server.py        # Server management utilities
    └── registry.py      # Registry utilities
```

## SessionStart Hook

**File**: `.claude/hooks/session_start.py`

**Triggered by**:
- New session start (`source=startup`)
- Session resume (`source=resume`)
- After `/clear` command (`source=clear`)
- After compaction (`source=compact`)

**Behavior**:
1. Receives session info via stdin JSON
2. **Executes** `nexus-loader.py` directly (doesn't tell Claude to run it)
3. Reads the cache file content
4. Outputs context wrapped in `<NexusContext>` tags
5. Context is injected as `additionalContext` in Claude's conversation

**Input** (from Claude Code):
```json
{
  "session_id": "abc123",
  "source": "startup",
  "hook_event_name": "SessionStart"
}
```

**Output** (to Claude via stdout):
```xml
<NexusContext source="startup" session="abc123">
{... 80KB+ of cached context ...}
</NexusContext>
```

**Why Direct Execution?**

Previous approach (FAILED):
```python
# Hook outputs instruction
print("Run NOW: python nexus-loader.py --startup")
# Claude receives instruction but may ignore it
```

Current approach (WORKS):
```python
# Hook executes loader directly
result = subprocess.run(["python", "nexus-loader.py", "--startup"], ...)
cache_content = read_cache_file(session_id)
print(f"<NexusContext>{cache_content}</NexusContext>")
# Claude receives actual context - cannot ignore
```

**Windows Compatibility**:
- Cache files may contain Unicode (arrows, emojis)
- stdout must be ASCII for Windows compatibility
- Solution: `content.encode("ascii", errors="replace").decode("ascii")`

## PreCompact Hook

**File**: `.claude/hooks/save_resume_state.py`

**Triggered by**: Before context compaction

**Behavior**:
1. Identifies the active IN_PROGRESS project
2. Parses transcript for last `--skill` invocation
3. Writes `_resume.md` with current state
4. Cleans up session-specific cache
5. Outputs resume context for post-compaction

**Output** (for compacted conversation):
```xml
<NexusResumeContext>
CONTINUE PROJECT: 14-advanced-hook-system
PHASE: execution
LAST SKILL: execute-project

MANDATORY NEXT STEP:
Run: python 00-system/core/nexus-loader.py --resume --session abc123
Then read the cache file and continue working on 14-advanced-hook-system.
</NexusResumeContext>
```

## SessionEnd Hook

**File**: `.claude/hooks/session_end.py`

**Triggered by**:
- `/clear` command (`reason=clear`)
- User logout (`reason=logout`)
- Prompt input exit (`reason=prompt_input_exit`)
- Other termination (`reason=other`)

**Behavior**:
1. Cleans up session-specific cache file
2. Cleans up stale caches (>60 minutes old)
3. Sends session end event to server
4. Saves transcript locally as backup
5. Sends transcript to server for analysis

## PreToolUse Hook (Safety)

**File**: `.claude/hooks/pre_tool_use.py`

**Matcher**: `Bash` (intercepts shell commands)

**Blocks** (exit code 2 + stderr):
- `rm -rf /`, `rm -rf ~`, `rm -rf *` patterns
- `.env` file access (except `.env.sample`, `.env.example`)

**Allows** (exit code 0):
- All other commands pass through

**Blocking Pattern**:
```python
# Blocking requires stderr + exit code 2
print("BLOCKED: Dangerous rm -rf command detected", file=sys.stderr)
sys.exit(2)
```

## Exit Code Reference

| Code | Meaning | Behavior |
|------|---------|----------|
| **0** | Success | Continue; stdout added to context |
| **2** | Block | Halt action; stderr fed to Claude as feedback |
| **Other** | Non-blocking error | Continue; stderr shown to user only |

## Multi-Session Support

Sessions are isolated using MD5 hashed session IDs:

```
Session A (abc123)          Session B (def456)
├── context_startup_a1b2.json   ├── context_startup_c3d4.json
└── Independent context         └── Independent context
```

**Cache file naming**: `context_startup_{md5(session_id)[:8]}.json`

## Configuration

Located in `.claude/settings.json`:

```json
{
  "hooks": {
    "SessionStart": [{
      "hooks": [{
        "type": "command",
        "command": "python .claude/hooks/session_start.py"
      }]
    }],
    "PreCompact": [{
      "hooks": [{
        "type": "command",
        "command": "python .claude/hooks/save_resume_state.py"
      }]
    }],
    "SessionEnd": [{
      "hooks": [{
        "type": "command",
        "command": "python .claude/hooks/session_end.py"
      }]
    }],
    "PreToolUse": [{
      "matcher": "Bash",
      "hooks": [{
        "type": "command",
        "command": "python .claude/hooks/pre_tool_use.py"
      }]
    }]
  }
}
```

## Debugging

```bash
# View hook configuration
/hooks

# Run with debug output
claude --debug

# Test hook manually
echo '{"session_id":"test","source":"startup"}' | python .claude/hooks/session_start.py

# Check exit code
echo $?
```

**Common Issues**:
1. Script not executable: `chmod +x script.py`
2. Wrong paths: Use `$CLAUDE_PROJECT_DIR`
3. stdout vs stderr: Blocking uses stderr only
4. JSON not flushed: Use `flush=True`
5. Windows encoding: Use ASCII with `errors="replace"`

## References

- [Claude Code Hooks Docs](https://code.claude.com/docs/en/hooks)
- [awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code)
- [claude-code-safety-net](https://github.com/kenryu42/claude-code-safety-net)
- Project 14: `02-projects/14-advanced-hook-system/`
