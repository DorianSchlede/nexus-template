# claude-codex-settings (fcakyon) Findings

**Repository:** https://github.com/fcakyon/claude-codex-settings
**Version:** 2.0.2
**License:** Apache-2.0
**Author:** Fatih Akyon

## Overview

This repository is a comprehensive Claude Code/Codex settings collection featuring a modular plugin system with hooks, commands, agents, skills, and MCP integrations. It represents one of the most mature examples of Claude Code customization in the ecosystem.

## Key Patterns

### 1. Plugin-Based Architecture
- Each feature is organized as a self-contained plugin in `plugins/` directory
- Plugins contain: `.claude-plugin/plugin.json`, `hooks/`, `commands/`, `skills/`, `agents/`
- Uses `${CLAUDE_PLUGIN_ROOT}` environment variable for relative paths within hooks

### 2. Hook Event Types
- **PreToolUse**: Intercept before tool execution (validation, redirection, confirmation)
- **PostToolUse**: Process after tool execution (formatting, notifications)
- **Notification**: React to Claude Code notifications

### 3. Permission Decisions
- `allow`: Permit the tool call (optionally with modified input via `updatedInput`)
- `deny`: Block the tool call with a reason message
- `ask`: Prompt user for confirmation with a formatted message

### 4. Exit Codes Convention
- `0`: Success/allow the operation
- `1`: Error in hook execution
- `2`: Block the operation and show stderr to Claude

---

## Tool Redirection Pattern

### WebFetch to Tavily Extract

**File:** `plugins/tavily-tools/hooks/scripts/webfetch_to_tavily_extract.py`

```python
#!/usr/bin/env python3
"""PreToolUse hook: intercept WebFetch -> suggest using tavily-extract instead"""
import json
import sys

try:
    data = json.load(sys.stdin)
    url = data["tool_input"]["url"]
except (KeyError, json.JSONDecodeError) as err:
    print(f"hook-error: {err}", file=sys.stderr)
    sys.exit(1)

print(json.dumps({
    "systemMessage": "WebFetch detected. AI is directed to use Tavily extract instead.",
    "hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": f"Please use mcp__tavily__tavily-extract with urls: ['{url}'] and extract_depth: 'advanced'"
    }
}, separators=(',', ':')))
sys.exit(0)
```

**Key Insights:**
- Uses `deny` decision to block the original tool
- Provides a helpful `permissionDecisionReason` that instructs AI to use alternative
- Includes `systemMessage` for AI context
- Preserves original parameters (URL) in the redirection message

### WebSearch to Tavily Search

**File:** `plugins/tavily-tools/hooks/scripts/websearch_to_tavily_search.py`

```python
#!/usr/bin/env python3
"""PreToolUse hook: intercept WebSearch -> suggest using Tavily search instead"""
import json
import sys

try:
    data = json.load(sys.stdin)
    tool_input = data["tool_input"]
    query = tool_input["query"]
except (KeyError, json.JSONDecodeError) as err:
    print(f"hook-error: {err}", file=sys.stderr)
    sys.exit(1)

print(json.dumps({
    "systemMessage": "WebSearch detected. AI is directed to use Tavily search instead.",
    "hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": f"Please use mcp__tavily__tavily_search with query: '{query}'"
    }
}, separators=(',', ':')))
sys.exit(0)
```

### Input Modification Pattern (Tavily Extract Upgrade)

**File:** `plugins/tavily-tools/hooks/scripts/tavily_extract_to_advanced.py`

```python
#!/usr/bin/env python3
"""Intercept mcp__tavily__tavily-extract to upgrade extract_depth and suggest gh CLI for GitHub URLs."""

import json
import sys

try:
    data = json.load(sys.stdin)
    tool_input = data["tool_input"]
    urls = tool_input.get("urls", [])

    # Always ensure extract_depth="advanced"
    tool_input["extract_depth"] = "advanced"

    # Check for GitHub URLs and add soft suggestion
    github_domains = ("github.com", "raw.githubusercontent.com", "gist.github.com")
    github_urls = [url for url in urls if any(domain in url for domain in github_domains)]

    if github_urls:
        # Allow but suggest GitHub MCP/gh CLI for next time
        print(
            json.dumps(
                {
                    "systemMessage": "Tip: For GitHub URLs, use gh CLI: `gh api repos/{owner}/{repo}/contents/{path} --jq '.content' | base64 -d` for files, `gh pr view` for PRs, `gh issue view` for issues.",
                    "hookSpecificOutput": {
                        "hookEventName": "PreToolUse",
                        "permissionDecision": "allow",
                        "updatedInput": tool_input,
                    },
                },
                separators=(",", ":"),
            )
        )
        sys.exit(0)

    # Allow the call to proceed with modified input
    print(
        json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "allow",
                    "updatedInput": tool_input,
                }
            },
            separators=(",", ":"),
        )
    )
    sys.exit(0)

except (KeyError, json.JSONDecodeError) as err:
    print(f"hook-error: {err}", file=sys.stderr)
    sys.exit(1)
```

**Key Insights:**
- Uses `allow` with `updatedInput` to silently modify parameters
- Adds `systemMessage` as a "soft suggestion" without blocking
- Domain-based URL classification for context-aware tips

---

## Grep to Ripgrep Enforcement

**File:** `plugins/general-dev/hooks/scripts/enforce_rg_over_grep.py`

```python
#!/usr/bin/env python3
import json
import re
import sys

# Define validation rules as a list of (regex pattern, message) tuples
VALIDATION_RULES = [
    (
        r"\bgrep\b(?!.*\|)",
        "Use 'rg' (ripgrep) instead of 'grep' for better performance and features",
    ),
    (
        r"\bfind\s+\S+\s+-name\b",
        "Use 'rg --files | rg pattern' or 'rg --files -g pattern' instead of 'find -name' for better performance",
    ),
]


def validate_command(command: str) -> list[str]:
    issues = []
    for pattern, message in VALIDATION_RULES:
        if re.search(pattern, command):
            issues.append(message)
    return issues


try:
    input_data = json.load(sys.stdin)
except json.JSONDecodeError as e:
    print(f"Error: Invalid JSON input: {e}", file=sys.stderr)
    sys.exit(1)

tool_name = input_data.get("tool_name", "")
tool_input = input_data.get("tool_input", {})
command = tool_input.get("command", "")

if tool_name != "Bash" or not command:
    sys.exit(0)

# Validate the command
issues = validate_command(command)

if issues:
    for message in issues:
        print(f"* {message}", file=sys.stderr)
    # Exit code 2 blocks tool call and shows stderr to Claude
    sys.exit(2)
```

**Key Insights:**
- Rule-based validation with configurable patterns
- Uses exit code 2 to block and show feedback to Claude
- Regex patterns allow sophisticated matching (e.g., `(?!.*\|)` for negation)
- Extensible design with VALIDATION_RULES list

---

## Git Workflow Hooks

### Git Commit Confirmation

**File:** `plugins/github-dev/hooks/scripts/git_commit_confirm.py`

```python
#!/usr/bin/env python3
"""PreToolUse hook: show confirmation modal before creating git commit."""
import json
import re
import subprocess
import sys


def parse_git_commit_message(command: str) -> dict[str, str]:
    """Parse git commit command to extract commit message."""
    params = {"message": "", "is_amend": False}

    # Check for --amend flag
    params["is_amend"] = "--amend" in command

    # Try to extract heredoc format: git commit -m "$(cat <<'EOF' ... EOF)"
    heredoc_match = re.search(r"<<'EOF'\s*\n(.*?)\nEOF", command, re.DOTALL)
    if heredoc_match:
        params["message"] = heredoc_match.group(1).strip()
        return params

    # Try to extract simple -m "message" format
    simple_matches = re.findall(r'(?:-m|--message)\s+["\']([^"\']+)["\']', command)
    if simple_matches:
        # Join multiple -m flags with double newlines
        params["message"] = "\n\n".join(simple_matches)
        return params

    return params


def get_staged_files() -> tuple[list[str], str]:
    """Get list of staged files and diff stats."""
    try:
        # Get list of staged files
        files_result = subprocess.run(
            ["git", "diff", "--cached", "--name-only"],
            capture_output=True,
            text=True,
            timeout=5,
        )

        # Get diff stats
        stats_result = subprocess.run(
            ["git", "diff", "--cached", "--stat"],
            capture_output=True,
            text=True,
            timeout=5,
        )

        files = []
        if files_result.returncode == 0:
            files = [f for f in files_result.stdout.strip().split("\n") if f]

        stats = ""
        if stats_result.returncode == 0:
            stats_lines = stats_result.stdout.strip().split("\n")
            if stats_lines:
                stats = stats_lines[-1]

        return files, stats

    except (subprocess.TimeoutExpired, FileNotFoundError):
        return [], ""


def format_confirmation_message(message: str, is_amend: bool, files: list[str], stats: str) -> str:
    """Format commit parameters into readable confirmation message."""
    lines = []

    # Header
    if is_amend:
        lines.append("Amend Previous Commit?")
    else:
        lines.append("Create Commit?")
    lines.append("")

    # Commit message
    if message:
        lines.append("Message:")
        lines.append(message)
        lines.append("")

    # Files
    if files:
        lines.append(f"Files to be committed ({len(files)}):")
        display_files = files[:15]
        for f in display_files:
            lines.append(f"- {f}")
        if len(files) > 15:
            lines.append(f"... and {len(files) - 15} more files")
        lines.append("")

    # Stats
    if stats:
        lines.append("Stats:")
        lines.append(stats)

    # Warning if no files staged
    if not files:
        lines.append("Warning: No files staged for commit")

    return "\n".join(lines)


# Main execution
try:
    input_data = json.load(sys.stdin)
except json.JSONDecodeError as e:
    print(f"Error: Invalid JSON input: {e}", file=sys.stderr)
    sys.exit(1)

tool_name = input_data.get("tool_name", "")
tool_input = input_data.get("tool_input", {})
command = tool_input.get("command", "")

# Only handle git commit commands
if tool_name != "Bash" or not command.strip().startswith("git commit"):
    sys.exit(0)

# Parse commit message
params = parse_git_commit_message(command)

# Get staged files and stats
files, stats = get_staged_files()

# Format confirmation message
message = format_confirmation_message(params["message"], params["is_amend"], files, stats)

# Return JSON with ask decision
output = {
    "hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "ask",
        "permissionDecisionReason": message,
    }
}

print(json.dumps(output))
sys.exit(0)
```

**Key Insights:**
- Uses `ask` decision to prompt user confirmation
- Enriches confirmation with git context (staged files, stats)
- Handles both simple `-m` and heredoc commit message formats
- Truncates file list to first 15 for readability
- Warns if no files are staged

### PR Creation Confirmation

**File:** `plugins/github-dev/hooks/scripts/gh_pr_create_confirm.py`

```python
#!/usr/bin/env python3
"""PreToolUse hook: show confirmation modal before creating GitHub PR via gh CLI."""
import json
import re
import subprocess
import sys


def parse_gh_pr_create(command: str) -> dict[str, str]:
    """Parse gh pr create command to extract PR parameters."""
    params = {"title": "", "body": "", "assignee": "", "reviewer": ""}

    # Extract title (-t or --title)
    title_match = re.search(r'(?:-t|--title)\s+["\']([^"\']+)["\']', command)
    if title_match:
        params["title"] = title_match.group(1)

    # Extract body - handle HEREDOC syntax first, then simple quotes
    heredoc_match = re.search(
        r'(?:-b|--body)\s+"?\$\(cat\s+<<["\']?(\w+)["\']?\s+(.*?)\s+\1\s*\)"?',
        command,
        re.DOTALL,
    )
    if heredoc_match:
        params["body"] = heredoc_match.group(2).strip()
    else:
        body_match = re.search(r'(?:-b|--body)\s+"([^"]+)"', command)
        if body_match:
            params["body"] = body_match.group(1)

    # Extract assignee (-a or --assignee)
    assignee_match = re.search(r'(?:-a|--assignee)\s+([^\s]+)', command)
    if assignee_match:
        params["assignee"] = assignee_match.group(1)

    # Extract reviewer (-r or --reviewer)
    reviewer_match = re.search(r'(?:-r|--reviewer)\s+([^\s]+)', command)
    if reviewer_match:
        params["reviewer"] = reviewer_match.group(1)

    return params


def resolve_username(assignee: str) -> str:
    """Resolve @me to actual GitHub username."""
    if assignee == "@me":
        try:
            result = subprocess.run(
                ["gh", "api", "user", "--jq", ".login"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            if result.returncode == 0:
                return result.stdout.strip()
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass
    return assignee


def format_confirmation_message(params: dict[str, str]) -> str:
    """Format PR parameters into readable confirmation message."""
    # Truncate body if too long
    body = params["body"]
    if len(body) > 500:
        body = body[:500] + "..."

    # Resolve assignee
    assignee = resolve_username(params["assignee"]) if params["assignee"] else "None"

    lines = ["Create Pull Request?", "", f"Title: {params['title']}", ""]

    if body:
        lines.extend(["Body:", body, ""])

    lines.append(f"Assignee: {assignee}")

    if params["reviewer"]:
        lines.append(f"Reviewer: {params['reviewer']}")

    return "\n".join(lines)


# Main execution
try:
    input_data = json.load(sys.stdin)
except json.JSONDecodeError as e:
    print(f"Error: Invalid JSON input: {e}", file=sys.stderr)
    sys.exit(1)

tool_name = input_data.get("tool_name", "")
tool_input = input_data.get("tool_input", {})
command = tool_input.get("command", "")

# Only handle gh pr create commands
if tool_name != "Bash" or not command.strip().startswith("gh pr create"):
    sys.exit(0)

# Parse PR parameters
params = parse_gh_pr_create(command)

# Format confirmation message
message = format_confirmation_message(params)

# Return JSON with ask decision
output = {
    "hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "ask",
        "permissionDecisionReason": message,
    }
}

print(json.dumps(output))
sys.exit(0)
```

**Key Insights:**
- Resolves `@me` to actual GitHub username via `gh api`
- Handles HEREDOC body format commonly used in PR descriptions
- Truncates long bodies to 500 characters for confirmation display

---

## Code Quality Hooks

### Python Code Quality (ruff)

**File:** `plugins/ultralytics-dev/hooks/scripts/python_code_quality.py`

```python
#!/usr/bin/env python3
"""PostToolUse hook: Auto-format Python files with ruff and block on errors"""

import json
import shutil
import subprocess
import sys
from pathlib import Path


def main():
    try:
        data = json.load(sys.stdin)

        # Get file path from tool input
        file_path = data.get("tool_input", {}).get("file_path", "")

        # Only process Python files
        if not file_path.endswith('.py'):
            sys.exit(0)

        py_file = Path(file_path)

        # Skip virtual env, cache, and .claude directories
        skip_dirs = ['.venv', 'venv', 'site-packages', '__pycache__', '.claude']
        if not py_file.exists() or any(p in py_file.parts for p in skip_dirs):
            sys.exit(0)

        # Check if ruff is available - silent exit if not (no blocking)
        if not shutil.which('ruff'):
            sys.exit(0)

        work_dir = py_file.parent

        # Run ruff check with fixes
        check_result = subprocess.run([
            'ruff', 'check',
            '--fix',
            '--extend-select', 'F,I,D,UP,RUF,FA',
            '--target-version', 'py39',
            '--ignore', 'D100,D104,D203,D205,D212,D213,D401,D406,D407,D413,RUF001,RUF002,RUF012',
            str(py_file)
        ], capture_output=True, text=True, cwd=work_dir)

        # Block only if ruff check finds unfixable errors
        if check_result.returncode != 0:
            error_output = check_result.stdout.strip() or check_result.stderr.strip()
            error_msg = f'ERROR running ruff check: {error_output}'
            print(error_msg, file=sys.stderr)
            output = {
                'systemMessage': f'Ruff errors detected in {py_file.name}',
                'hookSpecificOutput': {
                    'hookEventName': 'PostToolUse',
                    'decision': 'block',
                    'reason': error_msg
                },
            }
            print(json.dumps(output), file=sys.stderr)
            sys.exit(2)

        # Run ruff format
        format_result = subprocess.run([
            'ruff', 'format',
            '--line-length', '120',
            str(py_file)
        ], capture_output=True, text=True, cwd=work_dir)

        # Block only if ruff format fails
        if format_result.returncode != 0:
            error_output = format_result.stderr.strip()
            error_msg = f'ERROR running ruff format: {error_output}'
            print(error_msg, file=sys.stderr)
            output = {
                'systemMessage': f'Ruff format failed for {py_file.name}',
                'hookSpecificOutput': {
                    'hookEventName': 'PostToolUse',
                    'decision': 'block',
                    'reason': error_msg
                },
            }
            print(json.dumps(output), file=sys.stderr)
            sys.exit(2)

    except Exception as e:
        error_msg = f'Python code quality hook error: {e}'
        print(error_msg, file=sys.stderr)
        sys.exit(2)

    # Success - no errors
    sys.exit(0)


if __name__ == '__main__':
    main()
```

**Key ruff configuration:**
- `--extend-select`: F (Pyflakes), I (isort), D (docstrings), UP (pyupgrade), RUF (ruff-specific), FA (future annotations)
- `--target-version`: py39
- `--ignore`: Various docstring rules for flexibility
- `--line-length`: 120 for formatting

### Python Docstring Formatter

**File:** `plugins/ultralytics-dev/hooks/scripts/format_python_docstrings.py`

This is a sophisticated 265-line script that:
- Parses Python AST to find docstrings
- Validates Google-style docstring format
- Normalizes section names (Arguments -> Args, Return -> Returns)
- Wraps text while preserving code blocks and tables
- Auto-capitalizes summary lines and adds periods

### Prettier Formatting

**File:** `plugins/ultralytics-dev/hooks/scripts/prettier_formatting.py`

```python
#!/usr/bin/env python3
"""PostToolUse hook: Auto-format JS/TS/CSS/JSON/YAML/HTML/Vue/Svelte files with prettier"""
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

PRETTIER_EXTENSIONS = {'.js', '.jsx', '.ts', '.tsx', '.css', '.less', '.scss',
                      '.json', '.yml', '.yaml', '.html', '.vue', '.svelte'}
LOCK_FILE_PATTERN = re.compile(r'.*lock\.(json|yaml|yml)$|.*\.lock$')


def check_prettier_version() -> bool:
    """Check if prettier is installed and warn if version differs from 3.6.2."""
    if not shutil.which('npx'):
        return False
    try:
        result = subprocess.run(['npx', 'prettier', '--version'],
                                capture_output=True, text=True, check=False, timeout=5)
        if result.returncode == 0:
            version = result.stdout.strip()
            if '3.6.2' not in version:
                print(f"Warning: Prettier version mismatch: expected 3.6.2, found {version}")
            return True
    except Exception:
        pass
    return False


def main():
    try:
        data = json.load(sys.stdin)
        file_path = data.get("tool_input", {}).get("file_path", "")

        if not file_path:
            sys.exit(0)

        py_file = Path(file_path)
        if not py_file.exists() or py_file.suffix not in PRETTIER_EXTENSIONS:
            sys.exit(0)

        # Skip virtual env, cache, .claude directories, lock files, and minified assets
        skip_patterns = ['.venv', 'venv', 'site-packages', '__pycache__', '.claude']
        if any(p in py_file.parts for p in skip_patterns):
            sys.exit(0)
        if LOCK_FILE_PATTERN.match(py_file.name) or py_file.name == 'model.json':
            sys.exit(0)
        if py_file.name.endswith(('.min.js', '.min.css')):
            sys.exit(0)

        if not check_prettier_version():
            sys.exit(0)

        subprocess.run([
            'npx', 'prettier', '--write', '--list-different', '--print-width', '120', str(py_file)
        ], capture_output=True, check=False, cwd=py_file.parent)

    except Exception:
        pass

    sys.exit(0)


if __name__ == "__main__":
    main()
```

---

## Configuration Examples

### hooks.json Structure

**General Dev:**
```json
{
  "description": "General development hooks for code quality",
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/hooks/scripts/enforce_rg_over_grep.py"
          }
        ]
      }
    ]
  }
}
```

**GitHub Dev (multiple hooks on same matcher):**
```json
{
  "description": "Git workflow confirmation hooks for GitHub operations",
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/hooks/scripts/git_commit_confirm.py"
          },
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/hooks/scripts/gh_pr_create_confirm.py"
          }
        ]
      }
    ]
  }
}
```

**Tavily Tools (multiple matchers):**
```json
{
  "description": "Web search and Tavily integration hooks",
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "WebFetch",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/hooks/scripts/webfetch_to_tavily_extract.py"
          }
        ]
      },
      {
        "matcher": "WebSearch",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/hooks/scripts/websearch_to_tavily_search.py"
          }
        ]
      },
      {
        "matcher": "mcp__tavily__tavily-extract",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/hooks/scripts/tavily_extract_to_advanced.py"
          }
        ]
      }
    ]
  }
}
```

**Ultralytics Dev (PostToolUse with pipe matcher):**
```json
{
  "description": "Code formatting and quality hooks for Ultralytics development",
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|MultiEdit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "file_path=$(jq -r '.tool_input.file_path // empty' 2>/dev/null); if [[ -n \"$file_path\" && -f \"$file_path\" ]]; then case \"$file_path\" in *.py|*.js|*.jsx|*.ts|*.tsx) if [[ \"$OSTYPE\" == \"darwin\"* ]]; then sed -i '' 's/^[[:space:]]*$//g' \"$file_path\" 2>/dev/null || true; else sed -i 's/^[[:space:]]*$//g' \"$file_path\" 2>/dev/null || true; fi ;; esac; fi"
          },
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/hooks/scripts/format_python_docstrings.py"
          },
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/hooks/scripts/python_code_quality.py"
          },
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/hooks/scripts/prettier_formatting.py"
          },
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/hooks/scripts/markdown_formatting.py"
          },
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/hooks/scripts/bash_formatting.py"
          }
        ]
      }
    ]
  }
}
```

**Notification Tools (empty matcher for all events):**
```json
{
  "description": "OS notifications on Claude Code events",
  "hooks": {
    "Notification": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/hooks/scripts/notify.sh"
          }
        ]
      }
    ]
  }
}
```

### settings.json Structure

```json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "env": {
    "CLAUDE_BASH_MAINTAIN_PROJECT_WORKING_DIR": "1",
    "DISABLE_BUG_COMMAND": "1",
    "DISABLE_ERROR_REPORTING": "1",
    "DISABLE_TELEMETRY": "1",
    "ANTHROPIC_DEFAULT_OPUS_MODEL": "claude-opus-4-5-20251101",
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "claude-opus-4-5-20251101",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL": "claude-sonnet-4-5-20250929",
    "CLAUDE_CODE_SUBAGENT_MODEL": "claude-opus-4-5-20251101",
    "MAX_MCP_OUTPUT_TOKENS": "40000"
  },
  "includeCoAuthoredBy": false,
  "permissions": {
    "allow": [
      "Bash(find:*)",
      "Bash(rg:*)",
      "Bash(git diff:*)",
      "Bash(git status:*)",
      "Bash(gh pr list:*)",
      "Bash(ruff:*)",
      "mcp__tavily__tavily_extract",
      "mcp__tavily__tavily_search",
      "mcp__context7__resolve-library-id"
    ]
  },
  "model": "opusplan",
  "extraKnownMarketplaces": {
    "claude-settings": {
      "source": {
        "source": "github",
        "repo": "fcakyon/claude-codex-settings"
      }
    }
  },
  "spinnerTipsEnabled": false,
  "alwaysThinkingEnabled": true
}
```

### plugin.json Structure

```json
{
  "name": "ultralytics-dev",
  "version": "2.0.2",
  "description": "Auto-formatting hooks for Python, JavaScript, Markdown, and Bash with Google-style docstrings and code quality checks.",
  "author": {
    "name": "Fatih Akyon"
  },
  "homepage": "https://github.com/fcakyon/claude-codex-settings#plugins",
  "repository": "https://github.com/fcakyon/claude-codex-settings",
  "license": "Apache-2.0"
}
```

---

## Reusable Code Patterns

### Standard Hook Boilerplate

```python
#!/usr/bin/env python3
"""Hook description."""
import json
import sys

try:
    data = json.load(sys.stdin)
    tool_name = data.get("tool_name", "")
    tool_input = data.get("tool_input", {})
except (KeyError, json.JSONDecodeError) as err:
    print(f"hook-error: {err}", file=sys.stderr)
    sys.exit(1)

# Early exit if not applicable
if tool_name != "TargetTool":
    sys.exit(0)

# Hook logic here...

# Output decision
print(json.dumps({
    "hookSpecificOutput": {
        "hookEventName": "PreToolUse",  # or "PostToolUse"
        "permissionDecision": "allow",  # or "deny", "ask"
        # Optional: "updatedInput": modified_input,
        # Optional: "permissionDecisionReason": "message for user/AI"
    }
}, separators=(',', ':')))
sys.exit(0)
```

### Path Filtering Pattern

```python
from pathlib import Path

file_path = data.get("tool_input", {}).get("file_path", "")
path = Path(file_path)

# Skip common non-project directories
skip_dirs = ['.venv', 'venv', 'site-packages', '__pycache__', '.claude', 'node_modules']
if any(p in path.parts for p in skip_dirs):
    sys.exit(0)

# Extension filtering
if path.suffix not in {'.py', '.js', '.ts'}:
    sys.exit(0)

# File existence check
if not path.exists():
    sys.exit(0)
```

### Tool Availability Check

```python
import shutil

def check_tool_available(tool_name: str) -> bool:
    """Check if a CLI tool is available."""
    return shutil.which(tool_name) is not None

# Graceful degradation - don't block if tool missing
if not check_tool_available('ruff'):
    sys.exit(0)
```

### Subprocess with Timeout

```python
import subprocess

try:
    result = subprocess.run(
        ["command", "arg1", "arg2"],
        capture_output=True,
        text=True,
        timeout=5,  # 5 second timeout
        cwd=working_directory,  # Optional working directory
    )
    if result.returncode == 0:
        output = result.stdout.strip()
    else:
        error = result.stderr.strip()
except (subprocess.TimeoutExpired, FileNotFoundError):
    pass  # Handle gracefully
```

### Notification Script (bash)

```bash
#!/usr/bin/env bash

# Read JSON input from Claude Code hook
input=$(cat)

# Extract message from JSON
message=$(echo "$input" | grep -o '"message":"[^"]*"' | cut -d'"' -f4)
title="Claude Code"

# Terminal bell
printf '\a'

# Cross-platform notification
if [[ "$OSTYPE" == "darwin"* ]]; then
  osascript -e "display notification \"${message}\" with title \"${title}\" sound name \"Glass\""
elif command -v notify-send &> /dev/null; then
  notify-send "${title}" "${message}" -u normal -i terminal
fi
```

---

## Notes for Implementation

### Architecture Decisions

1. **Graceful Degradation**: Hooks should exit cleanly (code 0) when tools aren't available rather than failing
2. **Skip Patterns**: Always skip virtual environments, caches, and generated files
3. **Timeout Protection**: Use timeouts on all subprocess calls to prevent hanging
4. **Error Isolation**: Each hook should handle its own errors and not affect other hooks

### Matcher Patterns

- Single tool: `"matcher": "Bash"`
- Multiple tools: `"matcher": "Edit|MultiEdit|Write"`
- MCP tools: `"matcher": "mcp__tavily__tavily-extract"`
- All events: `"matcher": ""`

### Hook Execution Order

Hooks in the same matcher block execute sequentially. Use inline bash for pre-processing:
```json
{
  "type": "command",
  "command": "file_path=$(jq -r '.tool_input.file_path // empty' 2>/dev/null); ..."
}
```

### Input/Output Contract

**Input (stdin):**
```json
{
  "tool_name": "Bash",
  "tool_input": {
    "command": "git commit -m 'message'"
  }
}
```

**Output (stdout for allow/deny/ask):**
```json
{
  "systemMessage": "Optional context for AI",
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow|deny|ask",
    "permissionDecisionReason": "Message shown to user/AI",
    "updatedInput": {}  // Optional modified tool_input
  }
}
```

### Best Practices from This Repo

1. **Use JSON separators**: `separators=(',', ':')` for compact output
2. **Provide actionable messages**: When denying, tell AI exactly what to do instead
3. **Add system messages**: Help AI understand context for better behavior
4. **Parse command carefully**: Use regex for both simple and heredoc formats
5. **Enrich confirmations**: Add context like file lists, stats, resolved usernames
6. **Version pin tools**: Check for specific versions (e.g., prettier 3.6.2)
7. **Use $CLAUDE_PLUGIN_ROOT**: For portable hook paths within plugins
