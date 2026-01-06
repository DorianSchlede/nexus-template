# SYNTHESIS: Multi-Agent Repository Exploration

**Project:** Nexus Advanced Hook System
**Date:** 2025-12-31
**Status:** Research Complete

---

## Executive Summary

This document synthesizes findings from a comprehensive exploration of 10 Claude Code hook repositories using parallel agents. The research identified key patterns, best practices, and reusable code that will inform the implementation of the Nexus Advanced Hook System.

### Repositories Analyzed

| # | Repository | Language | Focus Area | Quality |
|---|------------|----------|------------|---------|
| 1 | claude-code-safety-net | Python | Safety patterns (rm, git rules) | **Excellent** |
| 2 | claude-code-tools | Python | Safety-hooks plugin architecture | **Excellent** |
| 3 | claude-code-hooks-mastery | Python | All 8 hook events, TTS/LLM | **Excellent** |
| 4 | claude-code-hooks (EvanL1) | Python | Git-specific hooks (15 hooks) | **Good** |
| 5 | claude-codex-settings | Python | Tool redirection, code quality | **Excellent** |
| 6 | tdd-guard | TypeScript | TDD enforcement, multi-reporter | **Excellent** |
| 7 | cc-tools | Go | High-performance statusline | **Excellent** |
| 8 | claude-hooks | TypeScript | Type-safe hook architecture | **Good** |
| 9 | awesome-claude-code | Markdown | Resource index, community | Reference |

---

## Core Findings

### 1. Hook Protocol Standards

#### Exit Code Semantics (Universal)
| Exit Code | Meaning | Behavior |
|-----------|---------|----------|
| 0 | Success/Allow | Operation proceeds normally |
| 2 | Block | Operation blocked, stderr shown to Claude |
| Other | Non-blocking error | stderr shown to user, operation continues |

#### JSON Protocol
All hooks use stdin/stdout JSON communication:

```python
# Input (stdin)
{
    "tool_name": "Bash",
    "tool_input": {"command": "..."},
    "session_id": "...",
    "transcript_path": "..."
}

# Output (stdout) - Allow
{"decision": "approve"}

# Output (stdout) - Block
{
    "hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": "Blocked: ..."
    }
}

# Output (stdout) - Ask for confirmation
{
    "hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "ask",
        "permissionDecisionReason": "Confirm: ..."
    }
}
```

### 2. All 8 Hook Event Types

| Hook Event | Purpose | Can Block | Input Fields |
|------------|---------|-----------|--------------|
| SessionStart | Session initialization | No | `session_id`, `source` (startup/resume/clear) |
| PreToolUse | Before tool execution | **Yes** | `tool_name`, `tool_input` |
| PostToolUse | After tool execution | **Yes** | `tool_name`, `tool_input`, `tool_response` |
| PreCompact | Before context compaction | No | `transcript_path`, `trigger` |
| Stop | Session ends | **Yes** | `stop_hook_active` |
| SubagentStop | Subagent task ends | **Yes** | `stop_hook_active` |
| UserPromptSubmit | User submits prompt | **Yes** | `prompt` |
| Notification | Claude sends notification | No | `message`, `title` |

### 3. Permission Decision Types

| Decision | Effect | When to Use |
|----------|--------|-------------|
| `allow`/`approve` | Operation proceeds | Safe operations |
| `deny`/`block` | Operation blocked | Dangerous operations |
| `ask` | User prompted | Risky but legitimate operations |

---

## Key Patterns Identified

### Pattern 1: TRASH Folder Alternative (claude-code-tools)

Instead of blocking `rm` commands, redirect to a documented TRASH folder:

```python
reason_text = (
    "Instead of using 'rm':\n"
    "- MOVE files using `mv` to the TRASH directory in the CURRENT folder\n"
    "- Add an entry in 'TRASH-FILES.md' with filename, destination, and reason\n"
)
```

**Benefits:**
- Files recoverable
- Documentation of deletions
- Less disruptive than hard blocking

### Pattern 2: Three-Decision Response System (claude-code-tools)

Hooks return one of three decisions with priority: `block > ask > allow`

```python
def normalize_check_result(result):
    decision, reason = result
    if isinstance(decision, bool):
        return ("block" if decision else "allow", reason)
    return (decision, reason)

# Process all checks, collect decisions
for check_func in checks:
    decision, reason = normalize_check_result(check_func(command))
    if decision == "block":
        block_reasons.append(reason)
    elif decision == "ask":
        ask_reasons.append(reason)
```

### Pattern 3: UV Single-File Scripts (hooks-mastery)

PEP 723 inline dependencies for self-contained hooks:

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# dependencies = [
#     "python-dotenv",
# ]
# ///

import json
import sys
# ... rest of hook
```

**Benefits:**
- No virtual environment management
- Fast dependency resolution
- Self-contained scripts

### Pattern 4: Live Git Status Checking (claude-code-tools)

Real-time verification before dangerous operations:

```python
status_result = subprocess.run(
    ["git", "status", "--porcelain"],
    capture_output=True,
    text=True,
    timeout=5
)

has_changes = bool(status_result.stdout.strip())
if has_changes:
    # Block and show modified files
    all_changes = status_result.stdout.strip().split('\n')
```

### Pattern 5: Tool Redirection (claude-codex-settings)

Block one tool and suggest another:

```python
print(json.dumps({
    "systemMessage": "WebFetch detected. AI is directed to use Tavily instead.",
    "hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": f"Please use mcp__tavily__tavily-extract with urls: ['{url}']"
    }
}))
```

### Pattern 6: Input Modification (claude-codex-settings)

Silently modify tool inputs:

```python
tool_input["extract_depth"] = "advanced"

print(json.dumps({
    "hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "allow",
        "updatedInput": tool_input,
    }
}))
```

### Pattern 7: Compound Command Parsing (claude-code-tools)

Handle chained commands (`&&`, `||`, `;`):

```python
def extract_subcommands(command: str) -> list[str]:
    if not command:
        return []
    subcommands = re.split(r'\s*(?:&&|\|\||;)\s*', command)
    return [cmd.strip() for cmd in subcommands if cmd.strip()]
```

### Pattern 8: TTS Service Priority Chain (hooks-mastery)

Graceful degradation across TTS providers:

```python
# Priority: ElevenLabs > OpenAI > pyttsx3 (offline)
def get_tts_script_path():
    if os.getenv('ELEVENLABS_API_KEY'):
        return str(tts_dir / "elevenlabs_tts.py")
    if os.getenv('OPENAI_API_KEY'):
        return str(tts_dir / "openai_tts.py")
    return str(tts_dir / "pyttsx3_tts.py")  # Fallback
```

### Pattern 9: Zod Schema Validation (tdd-guard)

Runtime validation with TypeScript type inference:

```typescript
import { z } from 'zod'

export const HookDataSchema = HookContextSchema.extend({
    tool_name: z.string(),
    tool_input: z.unknown(),
})

export type HookData = z.infer<typeof HookDataSchema>
```

### Pattern 10: Dependency Injection (cc-tools, tdd-guard)

Interface-based design for testability:

```go
type Dependencies struct {
    FileReader    FileReader
    CommandRunner CommandRunner
    EnvReader     EnvReader
    TerminalWidth TerminalWidth
}
```

---

## Safety Rules Catalog

### rm -rf Detection (from claude-code-safety-net)

```python
patterns = [
    r'\brm\s+.*-[a-z]*r[a-z]*f',      # rm -rf, rm -fr, rm -Rf
    r'\brm\s+.*-[a-z]*f[a-z]*r',      # rm -fr variations
    r'\brm\s+--recursive\s+--force',   # long form
    r'\brm\s+-r\s+.*-f',              # separated flags
]

# Additional protections:
# - Block root/home paths unconditionally
# - Allow temp paths (/tmp, /var/tmp, $TMPDIR)
# - Allow paths within CWD
# - Paranoid mode blocks all
```

### Git Safety Rules (from claude-code-safety-net)

| Command | Trigger | Reason |
|---------|---------|--------|
| `git checkout --` | `--` at index 0 | Discards uncommitted changes |
| `git checkout <ref> -- <path>` | `--` with ref | Overwrites working tree |
| `git restore` | No `--staged` | Discards uncommitted changes |
| `git reset --hard` | `--hard` flag | Destroys uncommitted changes |
| `git clean -f` | `-f` or `--force` | Removes untracked files |
| `git push --force` | Without `--force-with-lease` | Destroys remote history |
| `git branch -D` | `-D` (uppercase) | Force-deletes branch |
| `git stash drop/clear` | `drop`/`clear` | Permanently deletes stash |

### .env Protection (from claude-code-tools)

```python
env_patterns = [
    # Reading
    r'\bcat\s+.*\.env\b', r'\bless\s+.*\.env\b', r'\bhead\s+.*\.env\b',
    # Editors
    r'\bvim\s+.*\.env\b', r'\bnano\s+.*\.env\b', r'\bcode\s+.*\.env\b',
    # Writing
    r'>\s*\.env\b', r'>>\s*\.env\b', r'\bsed\s+.*-i.*\.env\b',
    # Searching
    r'\bgrep\s+.*\.env\b', r'\brg\s+.*\.env\b',
]
```

### Protected Branches (from claude-code-hooks)

```python
protected_branches = ["main", "master", "production", "prod"]

# Patterns blocked:
# - git push origin :main (deletion)
# - git branch -D main
# - git push --force main
```

---

## Architecture Recommendations

### 1. Hook File Structure

```
.claude/
├── settings.json              # Hook configuration
├── hooks/
│   ├── __init__.py           # Make it a package
│   ├── session_start.py       # SessionStart handler
│   ├── pre_tool_use.py        # PreToolUse handler (safety)
│   ├── post_tool_use.py       # PostToolUse handler (logging)
│   ├── stop.py                # Stop handler (notifications)
│   └── utils/
│       ├── safety.py          # Shared safety patterns
│       ├── shell.py           # Command parsing
│       ├── git.py             # Git utilities
│       └── tts.py             # TTS service chain
└── data/
    └── sessions/              # Session state

logs/
├── hooks.jsonl               # All hook events
├── blocked.jsonl             # Blocked operations
└── sessions/                 # Per-session logs
```

### 2. Settings.json Template

```json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "hooks": {
    "SessionStart": [{
      "matcher": "",
      "hooks": [{
        "type": "command",
        "command": "uv run .claude/hooks/session_start.py"
      }]
    }],
    "PreToolUse": [{
      "matcher": "Bash",
      "hooks": [{
        "type": "command",
        "command": "uv run .claude/hooks/pre_tool_use.py",
        "timeout": 10
      }]
    }],
    "PostToolUse": [{
      "matcher": "Edit|MultiEdit|Write",
      "hooks": [{
        "type": "command",
        "command": "uv run .claude/hooks/post_tool_use.py"
      }]
    }],
    "Stop": [{
      "matcher": "",
      "hooks": [{
        "type": "command",
        "command": "uv run .claude/hooks/stop.py"
      }]
    }],
    "Notification": [{
      "matcher": "",
      "hooks": [{
        "type": "command",
        "command": "uv run .claude/hooks/notification.py"
      }]
    }]
  }
}
```

### 3. Standard Hook Template

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# dependencies = ["python-dotenv"]
# ///

import json
import sys
import os

# Add hooks directory to path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)


def main():
    try:
        data = json.load(sys.stdin)
        tool_name = data.get("tool_name", "")
        tool_input = data.get("tool_input", {})

        # Skip if not applicable
        if tool_name != "Bash":
            sys.exit(0)

        # Your validation logic here
        command = tool_input.get("command", "")

        # Check for dangerous patterns
        if is_dangerous(command):
            print(json.dumps({
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny",
                    "permissionDecisionReason": "Blocked: ..."
                }
            }))
            sys.exit(0)

        # Allow by default
        print(json.dumps({"decision": "approve"}))
        sys.exit(0)

    except Exception as e:
        # Fail-safe: approve on error
        print(json.dumps({"decision": "approve"}))
        sys.exit(0)


if __name__ == "__main__":
    main()
```

---

## Implementation Priorities

### Phase 1: Core Safety (HIGH PRIORITY)

1. **rm -rf blocking** with TRASH folder alternative
2. **Git dangerous operations** (reset --hard, push --force, stash drop)
3. **.env file protection**
4. **Protected branch protection**

### Phase 2: Enhanced Safety (MEDIUM PRIORITY)

1. **Compound command parsing**
2. **Live git status checking**
3. **Interpreter one-liner detection**
4. **Credential file blocking** (*.pem, *.key)

### Phase 3: Quality Gates (OPTIONAL)

1. **Tool redirection** (grep → rg)
2. **Auto-formatting** (ruff, prettier)
3. **File length limits**
4. **Git commit confirmation**

### Phase 4: Notifications (OPTIONAL)

1. **TTS announcements**
2. **Desktop notifications**
3. **Session logging**

---

## Code to Adopt

### From claude-code-safety-net:
- Complete shell parsing module (`_split_shell_commands`, `_strip_wrappers`)
- rm -rf detection with temp path allowlist
- Git command analysis with subcommand extraction
- Test patterns for safety hooks

### From claude-code-tools:
- Three-decision response system
- TRASH folder pattern
- Live git status checking
- Compound command parsing (`extract_subcommands`)

### From hooks-mastery:
- UV single-file script pattern
- TTS service priority chain
- Session data management
- Complete settings.json template

### From claude-codex-settings:
- Tool redirection pattern
- Input modification pattern
- Git commit/PR confirmation with context enrichment
- ruff configuration for Python quality

### From tdd-guard:
- Storage abstraction interface
- Zod schema validation pattern
- Multi-reporter architecture
- Guard enable/disable with ignore patterns

### From cc-tools:
- Dependency injection via interfaces
- Graceful degradation pattern
- Terminal width detection fallbacks
- Debug logging system

---

## Testing Strategy

### Unit Tests

```python
class SafetyNetTestCase(unittest.TestCase):
    def _run_guard(self, command, cwd=None):
        # Run hook with command and return parsed output
        pass

    def _assert_blocked(self, command, reason_contains, cwd=None):
        output = self._run_guard(command, cwd=cwd)
        self.assertIsNotNone(output)
        self.assertEqual(output["hookSpecificOutput"]["permissionDecision"], "deny")
        self.assertIn(reason_contains, output["hookSpecificOutput"]["permissionDecisionReason"])

    def _assert_allowed(self, command, cwd=None):
        output = self._run_guard(command, cwd=cwd)
        self.assertIsNone(output)  # No output = allowed
```

### Test Categories

1. **rm -rf variants** - All flag combinations
2. **Git operations** - checkout, reset, push, stash, clean
3. **.env protection** - read, write, search operations
4. **Compound commands** - && and || chains
5. **Edge cases** - bash -c wrappers, interpreters

---

## Success Metrics

After implementation, verify:

- [ ] All rm -rf variants blocked (test 6+ patterns)
- [ ] Git dangerous operations blocked (test 12+ rules)
- [ ] .env access blocked (test 15+ patterns)
- [ ] Compound commands parsed correctly
- [ ] TRASH folder alternative working
- [ ] No false positives on safe operations
- [ ] < 100ms hook execution time
- [ ] Graceful failure on hook errors

---

## References

### Findings Documents

1. [safety-net-patterns.md](findings/safety-net-patterns.md) - rm/git detection
2. [claude-code-tools-patterns.md](findings/claude-code-tools-patterns.md) - TRASH, git safety
3. [hooks-mastery-patterns.md](findings/hooks-mastery-patterns.md) - 8 hooks, TTS
4. [claude-code-hooks-patterns.md](findings/claude-code-hooks-patterns.md) - EvanL1 hooks
5. [claude-codex-settings-patterns.md](findings/claude-codex-settings-patterns.md) - redirection
6. [tdd-guard-patterns.md](findings/tdd-guard-patterns.md) - TypeScript patterns
7. [cc-tools-patterns.md](findings/cc-tools-patterns.md) - Go patterns
8. [claude-hooks-patterns.md](findings/claude-hooks-patterns.md) - TypeScript types
9. [awesome-index.md](findings/awesome-index.md) - Community resources

### Original Repositories

- https://github.com/kenryu42/claude-code-safety-net
- https://github.com/pchalasani/claude-code-tools
- https://github.com/disler/claude-code-hooks-mastery
- https://github.com/EvanL1/claude-code-hooks
- https://github.com/fcakyon/claude-codex-settings
- https://github.com/nizos/tdd-guard
- https://github.com/Veraticus/cc-tools
- https://github.com/johnlindquist/claude-hooks
- https://github.com/hesreallyhim/awesome-claude-code

---

*Document generated by multi-agent repository exploration on 2025-12-31*
