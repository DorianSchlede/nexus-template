---
id: 14-advanced-hook-system
name: Advanced Hook System for Nexus
status: COMPLETE
description: Load when user mentions 'hooks', 'pre-tool-use', 'safety guards', 'observability', 'session hooks'
created: 2025-12-31
completed: 2026-01-04
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

---

## ULTRATHINK Research: Advanced Hook Patterns

### UserPromptSubmit - Context Injection

**Use Case**: Inject sprint priorities, project context, or rules into EVERY prompt.

```json
{
  "hooks": {
    "UserPromptSubmit": [{
      "hooks": [{
        "type": "command",
        "command": "cat ./current-sprint-context.md"
      }]
    }]
  }
}
```

**Key Points**:
- Plain text stdout = added to context (simplest)
- JSON with `additionalContext` = more control
- `"decision": "block"` = prevents prompt processing
- Use for security filtering (block prompts with secrets)

### PostToolUse - Auto Quality Checks

**Pattern**: Run linters, formatters, type-checks after edits.

```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Edit:*.ts|Edit:*.tsx",
      "hooks": [{
        "type": "command",
        "command": "pnpm type:check --noEmit"
      }]
    }]
  }
}
```

**Best Practices**:
- Keep PostToolUse fast; heavy checks → Stop hook
- Use `$CLAUDE_FILE_PATHS` for file list
- Scope with specific matchers (not `*`)

### Stop/SubagentStop - Prevent Early Termination

**Pattern**: Force Claude to continue until tasks complete.

```json
{
  "hooks": {
    "Stop": [{
      "hooks": [{
        "type": "prompt",
        "prompt": "Analyze if all tasks are complete. Return {\"decision\": \"block\", \"reason\": \"...\"} if not.",
        "timeout": 30
      }]
    }]
  }
}
```

**Decision Control**:
- `"decision": "block"` + `"reason"` = force continue
- `undefined` = allow stop
- Prompt-based hooks (LLM evaluation) only for Stop/SubagentStop

### PermissionRequest - Auto-Approve/Deny

**Pattern**: Programmatic permission control without manual intervention.

```json
{
  "hooks": {
    "PermissionRequest": [{
      "matcher": "Bash(npm test*)",
      "hooks": [{
        "type": "command",
        "command": ".claude/hooks/permission-handler.sh"
      }]
    }]
  }
}
```

**Decision Logic** (from community):
```python
# Order matters: deny → allow → prompt
deny_patterns = ['rm -rf /', 'sudo', 'git reset --hard']
allow_patterns = ['ls', 'cat', 'git status', 'npm test']
# Unknown → fall through to user prompt
```

### Notification - Desktop Alerts

**Matchers**:
- `permission_prompt` - Claude needs permission
- `idle_prompt` - Idle 60+ seconds, waiting for input
- `auth_success` - Authentication completed
- `elicitation_dialog` - MCP tool needs input

```json
{
  "hooks": {
    "Notification": [{
      "matcher": "permission_prompt|idle_prompt",
      "hooks": [{
        "type": "command",
        "command": ".claude/hooks/notify-desktop.sh",
        "timeout": 5
      }]
    }]
  }
}
```

### MCP Tool Hooks

**Pattern**: `mcp__<server>__<tool>`

```json
{
  "matcher": "mcp__memory__.*",
  "hooks": [{"type": "command", "command": "echo 'Memory op' >> log"}]
}
```

---

## Exit Code Reference

| Code | Meaning | Behavior |
|------|---------|----------|
| **0** | Success | Continue; stdout shown in transcript (Ctrl-R) |
| **2** | Block | Halt action; stderr fed to Claude as feedback |
| **Other** | Non-blocking error | Continue; stderr shown to user only |

**Critical**: For blocking, write to **stderr**, not stdout!
```python
print("BLOCKED: reason", file=sys.stderr)
sys.exit(2)
```

---

## Debugging Hooks

**Commands**:
```bash
# View hook configuration
/hooks

# Run with debug output
claude --debug

# Test hook manually
echo '{"tool_name":"Bash","tool_input":{"command":"rm -rf /"}}' | python .claude/hooks/pre_tool_use.py
```

**Common Issues**:
1. Script not executable: `chmod +x script.sh`
2. Wrong paths: Use `$CLAUDE_PROJECT_DIR`
3. stdout vs stderr: Blocking uses stderr only
4. JSON not flushed: Use `flush=True`

---

## Plugin Architecture (2025)

```
plugin-name/
├── .claude-plugin/
│   └── plugin.json      # Metadata
├── commands/            # Slash commands
├── agents/              # Subagents
├── skills/              # Agent Skills
├── hooks/
│   └── hooks.json       # Hook definitions
└── .mcp.json            # MCP servers
```

**Key Insight**: "Skills inform, hooks enforce"
- Skills = Claude knows preferences
- Hooks = Claude can't forget them

---

## References

**Official**:
- [Claude Code Hooks Reference](https://code.claude.com/docs/en/hooks)
- [How to Configure Hooks](https://claude.com/blog/how-to-configure-hooks)

**Awesome Lists & Plugin Hubs** (BEST RESOURCES):
- [awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code) - 18k+ Stars, comprehensive collection
- [awesome-claude-code-plugins](https://github.com/ccplugins/awesome-claude-code-plugins) - Curated plugins list
- [awesome-claude-plugins](https://github.com/quemsah/awesome-claude-plugins) - 243 plugins indexed
- [claudeforge/marketplace](https://github.com/claudeforge/marketplace) - 161 plugins

**Hooks Repositories** (COPY-PASTE READY):
- [claude-code-hooks-mastery](https://github.com/disler/claude-code-hooks-mastery) - All 8 hook events covered
- [claude-code-hooks](https://github.com/EvanL1/claude-code-hooks) - 15 Git-specific hooks

**Safety**:
- [claude-code-safety-net](https://github.com/kenryu42/claude-code-safety-net)
- [Taming Claude YOLO Mode](https://www.agentic-engineer.com/blog/2025-10-13-taming-claude-yolo-mode)
- [Bash Permission Hook Gist](https://gist.github.com/cruftyoldsysadmin/84b2c66ddd0fa170a840fc0cb649612b)

**Examples**:
- [Steve Kinney Hook Examples](https://stevekinney.com/courses/ai-development/claude-code-hook-examples)
- [Hook Control Flow](https://stevekinney.com/courses/ai-development/claude-code-hook-control-flow)
- [Automated Quality Checks](https://www.letanure.dev/blog/2025-08-06--claude-code-part-8-hooks-automated-quality-checks)

**Notifications**:
- [Desktop Notification Hooks](https://alexop.dev/posts/claude-code-notification-hooks/)
- [ntfy Integration](https://andrewford.co.nz/articles/claude-code-instant-notifications-ntfy/)

**Multi-Session**:
- [GitButler Parallel Sessions](https://blog.gitbutler.com/parallel-claude-code)
- [ccswarm Multi-Agent](https://github.com/nwiizo/ccswarm)
- [ccmanager Session Manager](https://github.com/kbwo/ccmanager)

**Architecture**:
- [Full Stack: MCP, Skills, Subagents, Hooks](https://alexop.dev/posts/understanding-claude-code-full-stack/)
- [Plugin Structure](https://claude-plugins.dev/skills/@anthropics/claude-plugins-official/plugin-structure)

**Bug Tracker**:
- [SessionStart stdout issue #13650](https://github.com/anthropics/claude-code/issues/13650)
- [Notification type missing #11964](https://github.com/anthropics/claude-code/issues/11964)
- [Hook System Issues #2814](https://github.com/anthropics/claude-code/issues/2814)

**Local Reference**:
- `04-workspace/00-ai-native-org/hook-system-reference.system.doc.md`
