# claude-code-tools Safety Hooks Findings

**Source Repository**: claude-code-tools (safety-hooks plugin)
**Path**: `c:\Users\dsber\infinite\auto-company\strategy-nexus\04-workspace\00-ai-native-org\hook-repos\claude-code-tools\plugins\safety-hooks\`
**Author**: Prasad Chalasani
**Extracted**: 2025-12-31

---

## Overview

The safety-hooks plugin provides a comprehensive suite of pre-tool-use hooks that intercept Claude Code tool calls and either:
- **Block** dangerous operations with helpful alternatives
- **Ask** for user confirmation on risky operations
- **Approve** safe operations

The plugin uses a unified architecture where individual check functions are composed into a main `bash_hook.py` orchestrator.

---

## Key Patterns

### 1. Three-Decision Response System
Hooks return one of three decisions:
- `allow` / `approve` - Operation proceeds normally
- `ask` - User prompted for confirmation before proceeding
- `block` / `deny` - Operation blocked with helpful message

### 2. Unified Hook Orchestrator
A single `bash_hook.py` combines all Bash-related checks, running them in sequence with priority: `block > ask > allow`

### 3. Compound Command Parsing
All hooks use `extract_subcommands()` to handle chained commands (`&&`, `||`, `;`)

### 4. Fail-Safe Design
On errors, hooks default to `approve` to avoid breaking Claude's workflow

### 5. Speed Bump Pattern
For file length limits, uses a flag file to implement "first block, second allow" pattern

---

## TRASH Folder Pattern

**File**: `rm_block_hook.py`

Instead of allowing destructive `rm` commands, redirect to a TRASH folder with documentation.

### Implementation

```python
def check_rm_command(command):
    """
    Check if a command contains rm that should be blocked.
    Returns tuple: (should_block: bool, reason: str or None)
    """
    # Normalize the command
    normalized_cmd = ' '.join(command.strip().split())

    # Check if it's an rm command
    # Catches: rm, /bin/rm, /usr/bin/rm, etc.
    if (normalized_cmd.startswith("rm ") or normalized_cmd == "rm" or
        re.search(r'(^|[;&|]\s*)(/\S*/)?rm\b', normalized_cmd)):
        reason_text = (
            "Instead of using 'rm':\n "
            "- MOVE files using `mv` to the TRASH directory in the CURRENT folder (create it if needed), \n"
            "- Add an entry in a markdown file called 'TRASH-FILES.md' in the current directory, "
            "  where you show a one-liner with the file name, where it moved, and the reason to trash it, e.g.:\n\n"
            "```\n"
            "test_script.py - moved to TRASH/ - temporary test script\n"
            "data/junk.txt - moved to TRASH/ - data file we don't need\n"
            "```"
        )
        return True, reason_text

    return False, None
```

### Key Techniques
- **Regex pattern**: `r'(^|[;&|]\s*)(/\S*/)?rm\b'` catches all variations:
  - `rm file.txt`
  - `/bin/rm file.txt`
  - `cd dir; rm file.txt`
- **Documentation**: Requires logging in `TRASH-FILES.md`
- **Recoverable**: Files can be restored from TRASH/

---

## Git Safety Patterns

### Git Checkout Safety Hook

**File**: `git_checkout_safety_hook.py`

**Purpose**: Block dangerous checkout operations and warn about uncommitted changes.

#### Dangerous Pattern Detection

```python
dangerous_patterns = [
    (r'\bgit\s+checkout\s+(-f|--force)\b',
     "'git checkout -f' FORCES checkout and DISCARDS all uncommitted changes!"),
    (r'\bgit\s+checkout\s+\.',
     "'git checkout .' will DISCARD ALL changes in current directory!"),
    (r'\bgit\s+checkout\s+.*\s+--\s+\.',
     "This will DISCARD ALL changes in current directory!"),
    (r'\bgit\s+checkout\s+.*\s+--\s+',
     "This will overwrite your local file with version from another branch/commit!"),
]
```

#### Live Git Status Check

```python
# Run git status --porcelain to detect uncommitted changes
status_result = subprocess.run(
    ["git", "status", "--porcelain"],
    capture_output=True,
    text=True,
    cwd=os.getcwd()
)

has_changes = bool(status_result.stdout.strip())

if has_changes:
    # Get detailed file list
    all_changes = status_result.stdout.strip().split('\n')
    modified_files = [f for f in all_changes if f.strip()]
    num_changes = len(modified_files)

    # Build warning with file list (max 10 shown)
    warning = f"WARNING: You have {num_changes} uncommitted change(s)!\n\n"
    warning += "Modified files:\n"
    for change in modified_files[:10]:
        warning += f"  {change}\n"
    if num_changes > 10:
        warning += f"  ... and {num_changes - 10} more\n"
```

#### Safe Patterns (Allowed)

```python
# Creating new branches or help commands are always safe
if "-b" in command or "--help" in command or "-h" in command:
    return False, None
```

### Git Add Safety Hook

**File**: `git_add_block_hook.py`

#### Blocked Patterns (Hard Block)

```python
# Wildcards
if '*' in normalized_cmd and normalized_cmd.startswith('git add'):
    return True, "BLOCKED: Wildcard patterns are not allowed..."

# Dangerous patterns: -A, --all, -a, ., ../, etc.
dangerous_pattern = re.compile(
    r'^git\s+add\s+(?:.*\s+)?('
    r'-[a-zA-Z]*[Aa][a-zA-Z]*(\s|$)|'  # Flags containing 'A' or 'a'
    r'--all(\s|$)|'                     # Long form --all
    r'\.(\s|$)|'                        # git add . (current directory)
    r'\.\./[\.\w/]*(\s|$)'             # git add ../ or ../.. patterns
    r')', re.IGNORECASE
)
```

#### Ask Patterns (User Confirmation)

```python
# Directory staging - uses dry-run to preview
result = subprocess.run(
    ['git', 'add', '--dry-run', dir_path + '/'],
    capture_output=True, text=True, cwd=os.getcwd()
)

# Parse dry-run output for files
files = []
for line in result.stdout.strip().split('\n'):
    if line.startswith('add '):
        fname = line[4:].strip().strip("'")
        files.append(fname)

# Check status of each file
for f in files:
    status_result = subprocess.run(
        ['git', 'status', '--porcelain', f],
        capture_output=True, text=True, cwd=os.getcwd()
    )
    status = status_result.stdout.strip()
    if status:
        status_code = status[:2]
        if '?' in status_code:
            new_files.append(f)
        else:
            modified_files.append(f)

# New files only = auto-approve
# Modified files = ask for permission
if modified_files:
    return "ask", f"Staging modified files: {file_list}"
```

### Git Commit Safety Hook

**File**: `git_commit_block_hook.py`

Simple hook that always asks for user permission before commits:

```python
def check_git_commit_command(command):
    for subcmd in extract_subcommands(command):
        normalized = ' '.join(subcmd.strip().split())
        if normalized.startswith('git commit'):
            return "ask", "Git commit requires your approval."
    return "allow", None
```

---

## .env File Protection

**File**: `env_file_protection_hook.py`

Comprehensive protection against reading, writing, or searching .env files.

### Protected Operations

```python
env_patterns = [
    # Direct file reading
    r'\bcat\s+.*\.env\b',
    r'\bless\s+.*\.env\b',
    r'\bmore\s+.*\.env\b',
    r'\bhead\s+.*\.env\b',
    r'\btail\s+.*\.env\b',

    # Editors - both reading and writing
    r'\bnano\s+.*\.env\b',
    r'\bvi\s+.*\.env\b',
    r'\bvim\s+.*\.env\b',
    r'\bemacs\s+.*\.env\b',
    r'\bcode\s+.*\.env\b',
    r'\bsubl\s+.*\.env\b',
    r'\batom\s+.*\.env\b',
    r'\bgedit\s+.*\.env\b',

    # Writing/modifying .env files
    r'>\s*\.env\b',          # Redirect to .env
    r'>>\s*\.env\b',         # Append to .env
    r'\becho\s+.*>\s*\.env\b',
    r'\bsed\s+.*-i.*\.env\b',  # sed in-place editing
    r'\btee\s+.*\.env\b',
    r'\bcp\s+.*\.env\b',
    r'\bmv\s+.*\.env\b',
    r'\btouch\s+.*\.env\b',

    # Searching .env files
    r'\bgrep\s+.*\.env\b',
    r'\brg\s+.*\.env\b',
    r'\bag\s+.*\.env\b',
    r'\back\s+.*\.env\b',
    r'\bfind\s+.*-name\s+["\']?\.env',
]
```

### Safe Alternative Messaging

```python
reason_text = (
    "Blocked: Direct access to .env files is not allowed for security reasons.\n\n"
    "For safe inspection, use the `env-safe` command:\n"
    "  - `env-safe list` - List all environment variable keys\n"
    "  - `env-safe list --status` - Show keys with defined/empty status\n"
    "  - `env-safe check KEY_NAME` - Check if a specific key exists\n"
    "  - `env-safe count` - Count variables in the file\n"
    "  - `env-safe validate` - Check .env file syntax\n\n"
    "To modify .env files, please edit them manually outside of Claude Code."
)
```

---

## File Length Limit Hook

**File**: `file_length_limit_hook.py`

### Configuration

```python
MAX_FILE_LINES = 10000

SOURCE_CODE_EXTENSIONS = {
    '.py', '.tsx', '.ts', '.jsx', '.js', '.rs', '.c', '.cpp', '.cc',
    '.cxx', '.h', '.hpp', '.go', '.java', '.kt', '.swift', '.rb',
    '.php', '.cs', '.scala', '.m', '.mm', '.r', '.jl',
}
```

### Speed Bump Pattern

```python
# Check flag file for speed bump pattern
flag_file = Path('.claude_file_length_warning.flag')

# If flag exists, allow and clear flag (second attempt)
if flag_file.exists():
    flag_file.unlink()
    return False, None

# First attempt - block and create flag
flag_file.touch()

reason = f"""
**File length limit exceeded ({resulting_lines} lines > {MAX_FILE_LINES} lines).**

**Please pause and ask the user:**
"This operation would create a file with {resulting_lines} lines. Would you like me to:
1. Refactor the code into smaller, more modular files?
2. Proceed with the large file anyway?"

**Only retry this operation if the user approves proceeding with the large file.**
"""
```

### Line Count Calculation for Edit Operations

```python
def get_resulting_line_count(tool_name, file_path, tool_input):
    if tool_name == "Write":
        content = tool_input.get("content", "")
        return count_lines_in_content(content)

    elif tool_name == "Edit":
        old_string = tool_input.get("old_string", "")
        new_string = tool_input.get("new_string", "")

        # Read current file
        with open(file_path, 'r', encoding='utf-8') as f:
            current_content = f.read()

        # Calculate result of edit
        replace_all = tool_input.get("replace_all", False)
        if replace_all:
            result_content = current_content.replace(old_string, new_string)
        else:
            result_content = current_content.replace(old_string, new_string, 1)

        return count_lines_in_content(result_content)
```

---

## Command Parsing Utilities

**File**: `command_utils.py`

### extract_subcommands

```python
def extract_subcommands(command: str) -> list[str]:
    """
    Split compound bash command into individual subcommands.
    Splits on &&, ||, and ; operators.

    Example:
        >>> extract_subcommands("cd /tmp && git add . && git commit -m 'msg'")
        ['cd /tmp', 'git add .', "git commit -m 'msg'"]
    """
    if not command:
        return []
    subcommands = re.split(r'\s*(?:&&|\|\||;)\s*', command)
    return [cmd.strip() for cmd in subcommands if cmd.strip()]
```

### Command Normalization Pattern

Used across multiple hooks:

```python
# Normalize the command - handle multiple spaces, tabs, etc.
normalized_cmd = ' '.join(command.strip().split())
```

---

## JSON Response Format

### Block/Deny Response

```python
# Simple format (older style)
print(json.dumps({
    "decision": "block",
    "reason": reason
}))

# hookSpecificOutput format (preferred)
print(json.dumps({
    "hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": reason
    }
}))
```

### Ask Response (User Confirmation)

```python
print(json.dumps({
    "hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "ask",
        "permissionDecisionReason": reason
    }
}))
```

### Approve Response

```python
print(json.dumps({"decision": "approve"}))
```

### Error Handling

```python
try:
    # ... hook logic ...
except Exception as e:
    # On error, approve to avoid breaking Claude
    print(json.dumps({
        "decision": "approve",
        "error": str(e)
    }))
    sys.exit(0)
```

---

## Configuration Examples

### hooks.json

```json
{
  "description": "Safety hooks to block or require approval for dangerous commands",
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "python3 ${CLAUDE_PLUGIN_ROOT}/hooks/bash_hook.py",
            "timeout": 10
          }
        ]
      },
      {
        "matcher": "Edit",
        "hooks": [
          {
            "type": "command",
            "command": "python3 ${CLAUDE_PLUGIN_ROOT}/hooks/file_length_limit_hook.py",
            "timeout": 10
          }
        ]
      },
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "python3 ${CLAUDE_PLUGIN_ROOT}/hooks/file_length_limit_hook.py",
            "timeout": 10
          }
        ]
      }
    ]
  }
}
```

### plugin.json

```json
{
  "name": "safety-hooks",
  "version": "0.1.0",
  "description": "Safety hooks to block or require user approval for dangerous commands",
  "author": {
    "name": "Prasad Chalasani"
  }
}
```

---

## Unified Hook Orchestrator

**File**: `bash_hook.py`

The main entry point that combines all Bash-related checks:

```python
def normalize_check_result(result):
    """
    Normalize check results to (decision, reason) format.
    Handles both old format (bool, reason) and new format (decision_str, reason).
    """
    decision, reason = result
    if isinstance(decision, bool):
        # Old format: (should_block: bool, reason)
        return ("block" if decision else "allow", reason)
    # New format: (decision: str, reason)
    return (decision, reason)


def main():
    data = json.load(sys.stdin)

    tool_name = data.get("tool_name")
    if tool_name != "Bash":
        print(json.dumps({"decision": "approve"}))
        sys.exit(0)

    command = data.get("tool_input", {}).get("command", "")

    # Run all checks
    checks = [
        check_rm_command,
        check_git_add_command,
        check_git_checkout_command,
        check_git_commit_command,
        check_env_file_access,
    ]

    block_reasons = []
    ask_reasons = []

    for check_func in checks:
        decision, reason = normalize_check_result(check_func(command))
        if decision == "block":
            block_reasons.append(reason)
        elif decision == "ask":
            ask_reasons.append(reason)

    # Priority: block > ask > allow
    if block_reasons:
        # Combine multiple block reasons
        combined_reason = block_reasons[0] if len(block_reasons) == 1 else \
            "Multiple safety checks failed:\n\n" + \
            "\n\n".join(f"{i}. {r}" for i, r in enumerate(block_reasons, 1))

        print(json.dumps({
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": combined_reason
            }
        }, ensure_ascii=False))
    elif ask_reasons:
        combined_reason = ask_reasons[0] if len(ask_reasons) == 1 else \
            "Approval required: " + "; ".join(ask_reasons)

        print(json.dumps({
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "ask",
                "permissionDecisionReason": combined_reason
            }
        }))
    else:
        print(json.dumps({"decision": "approve"}))
```

---

## Architecture Diagram

```
hooks.json
    |
    +-- PreToolUse
         |
         +-- Bash -> bash_hook.py (orchestrator)
         |            |
         |            +-- rm_block_hook.py
         |            +-- git_add_block_hook.py
         |            +-- git_checkout_safety_hook.py
         |            +-- git_commit_block_hook.py
         |            +-- env_file_protection_hook.py
         |            |
         |            +-- command_utils.py (shared)
         |
         +-- Edit -> file_length_limit_hook.py
         |
         +-- Write -> file_length_limit_hook.py
```

---

## Notes for Implementation

### 1. Decision Priority
Always process decisions in order: `block > ask > allow`. A single block should override any asks.

### 2. Compound Command Handling
Always parse compound commands (`&&`, `||`, `;`) and check each subcommand. One dangerous subcommand should block the entire chain.

### 3. User-Friendly Messages
Block messages should:
- Explain **why** the operation is blocked
- Provide **safe alternatives**
- Be actionable and educational

### 4. Live State Checks
For git operations, run actual `git status --porcelain` to get real-time state rather than relying on cached data.

### 5. Fail-Safe Default
On any error, default to `approve` to avoid breaking Claude's workflow. Log the error for debugging.

### 6. Speed Bump Pattern
For operations that should be allowed after explicit user approval, use a flag file:
1. First attempt: Block and create flag
2. Second attempt: Allow and delete flag

### 7. Environment Variable for Plugin Root
Use `CLAUDE_PLUGIN_ROOT` environment variable to locate shared modules.

### 8. Timeout Configuration
Set appropriate timeouts (10 seconds is the default) to prevent hooks from hanging.

### 9. JSON Encoding
Use `ensure_ascii=False` when outputting JSON to properly handle Unicode characters in messages.

### 10. Tool Input Access
Access tool parameters via: `data.get("tool_input", {}).get("parameter_name", "")`

---

## Reusable Code Snippets

### Standard Hook Template

```python
#!/usr/bin/env python3
import json
import sys
import os

# Add plugin hooks directory to Python path
PLUGIN_ROOT = os.environ.get('CLAUDE_PLUGIN_ROOT')
if PLUGIN_ROOT:
    hooks_dir = os.path.join(PLUGIN_ROOT, 'hooks')
    if hooks_dir not in sys.path:
        sys.path.insert(0, hooks_dir)

from command_utils import extract_subcommands


def check_my_command(command):
    """
    Check if a command should be blocked/asked/allowed.
    Returns tuple: (decision: str, reason: str or None)

    decision is one of: "allow", "ask", "block"
    """
    for subcmd in extract_subcommands(command):
        normalized = ' '.join(subcmd.strip().split())
        # Your check logic here
        if should_block:
            return "block", "Reason for blocking"
        if should_ask:
            return "ask", "Reason for asking"

    return "allow", None


if __name__ == "__main__":
    try:
        data = json.load(sys.stdin)

        tool_name = data.get("tool_name")
        if tool_name != "Bash":
            print(json.dumps({"decision": "approve"}))
            sys.exit(0)

        command = data.get("tool_input", {}).get("command", "")
        decision, reason = check_my_command(command)

        if decision == "block":
            print(json.dumps({
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny",
                    "permissionDecisionReason": reason
                }
            }))
        elif decision == "ask":
            print(json.dumps({
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "ask",
                    "permissionDecisionReason": reason
                }
            }))
        else:
            print(json.dumps({"decision": "approve"}))

        sys.exit(0)

    except Exception as e:
        # Fail-safe: approve on error
        print(json.dumps({
            "decision": "approve",
            "error": str(e)
        }))
        sys.exit(0)
```

---

## Summary

The claude-code-tools safety-hooks plugin provides a well-architected, extensible system for:

1. **Preventing destructive operations** (rm, dangerous git commands)
2. **Protecting sensitive data** (.env files)
3. **Enforcing code quality standards** (file length limits)
4. **Requiring human approval** for significant changes (git commits)

Key architectural decisions:
- Composable check functions with unified orchestrator
- Three-tier decision system (block/ask/allow)
- Fail-safe defaults
- User-friendly messaging with alternatives
- Live state verification via subprocess calls
