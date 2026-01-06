# claude-code-hooks (EvanL1) Findings

**Repository**: https://github.com/EvanL1/claude-code-hooks
**Analysis Date**: 2025-12-31
**Total Hooks**: 15 (6 Blocking, 4 Warning, 3 Audit, 1 UI, 1 Filter)

---

## Key Patterns

### Pattern 1: Standard Hook Structure
All hooks follow a consistent pattern:
1. Read JSON from stdin (`sys.stdin.read()`)
2. Parse JSON to get `tool_use` object
3. Check `tool_name` to filter relevant tools
4. Extract command/arguments from `tool_input`
5. Exit with appropriate code (0 = allow, 2 = block)

### Pattern 2: Dual Input Format Support
Hooks support both old and new Claude Code formats:
```python
tool = tool_use.get("tool") or tool_use.get("tool_name")
arguments = tool_use.get("arguments") or tool_use.get("tool_input", {})
```

### Pattern 3: Silent Failure Principle
All hooks wrap execution in try/except and exit(0) on errors to avoid blocking operations due to hook failures:
```python
except Exception:
    # Don't block on errors - exit silently
    sys.exit(0)
```

### Pattern 4: Exit Code Convention
- **Exit 0**: Allow operation (default)
- **Exit 2**: Block operation with error message

### Pattern 5: Error to stderr, Info to stdout
- Blocking errors: `print(error_msg, file=sys.stderr)`
- Warnings/info: `print(message)` (stdout)

---

## Git Safety Patterns

### Protected Branch Detection
```python
# Protected branches list
protected_branches = ["main", "master", "production", "prod"]

# Branch deletion detection
for branch in protected_branches:
    # Push-based deletion
    if f"git push origin :{branch}" in command:
        error_msg = f"Blocked deletion of protected branch '{branch}'"
        print(error_msg, file=sys.stderr)
        sys.exit(2)

    # Branch command deletion
    if re.search(rf"git\s+branch\s+-[dD].*{branch}", command):
        error_msg = f"Blocked deletion of protected branch '{branch}'"
        print(error_msg, file=sys.stderr)
        sys.exit(2)
```

### --no-verify Blocking with Message Context Detection
Smart detection that avoids false positives in commit messages:
```python
# Detect --no-verify as command parameter (not in quoted strings)
if re.search(r'(^|\s)--no-verify(\s|$)', command):
    # Check if inside -m "..." or heredoc
    msg_match = re.search(r'-m\s+["\'].*?["\']', command)
    heredoc_match = re.search(r'<<["\']?EOF["\']?.*?EOF', command, re.DOTALL)

    verify_pos = command.find('--no-verify')
    safe_in_message = False

    if msg_match and msg_match.start() < verify_pos < msg_match.end():
        safe_in_message = True
    if heredoc_match and heredoc_match.start() < verify_pos < heredoc_match.end():
        safe_in_message = True

    if not safe_in_message:
        print("Blocked: --no-verify bypasses Git Hooks!", file=sys.stderr)
        sys.exit(2)
```

### Dangerous Operations (Warning Only)
```python
dangerous_patterns = [
    (r"git\s+push\s+.*\s+--force", "Force push may overwrite remote history"),
    (r"git\s+reset\s+--hard", "Hard reset loses uncommitted changes"),
    (r"git\s+clean\s+-[fd]", "Clean operation deletes untracked files"),
]
```

---

## npm Safety Patterns

### Dangerous Operations Detection
```python
dangerous_operations = {
    r"npm\s+publish": "Publishing package to npm registry",
    r"npm\s+unpublish": "Unpublish affects users depending on this package",
    r"npm\s+link": "Global link may affect other projects",
    r"npm\s+install\s+.*--global": "Global install affects system environment",
    r"npm\s+install\s+.*--force": "Force install may cause dependency conflicts",
    r"npm\s+audit\s+fix\s+--force": "Force fix may introduce breaking changes",
    r"yarn\s+publish": "Publishing to registry",
    r"yarn\s+link": "Global link may affect other projects",
}
```

### Suspicious Packages List
```python
suspicious_packages = [
    "node-ipc",   # Had malicious code incident
    "colors",     # Had malicious code incident
    "faker",      # Deleted by author
]

for pkg in suspicious_packages:
    if f"install {pkg}" in command or f"add {pkg}" in command:
        messages.append(f"Warning: Package '{pkg}' has security concerns")
```

### Best Practice Suggestions
```python
# Suggest npm ci in CI environments
if "npm install" in command and ("CI" in command or "ci" in command.lower()):
    messages.append("Suggestion: Use 'npm ci' instead of 'npm install' in CI")
```

---

## AWS Safety Patterns

### Comprehensive Danger Detection
```python
dangerous_operations = {
    r"aws\s+.*\s+delete": "Delete operation - confirm target resource",
    r"aws\s+.*\s+terminate": "Terminate operation - permanently removes resource",
    r"aws\s+.*\s+remove": "Remove operation - confirm target",
    r"aws\s+s3\s+rm.*--recursive": "Recursive S3 delete - use with caution",
    r"aws\s+cloudformation\s+delete-stack": "Stack deletion removes all resources",
    r"aws\s+rds\s+delete-db": "RDS deletion - confirm backup exists",
    r"aws\s+ec2\s+terminate-instances": "EC2 termination - data will be lost",
}
```

### Production Environment Detection
```python
prod_indicators = ["prod", "production", "prd"]
for indicator in prod_indicators:
    if indicator in command.lower():
        messages.append("WARNING: Possible production environment operation")
        break
```

### S3 Security Checks
```python
if "s3" in command:
    # Public access check
    if "--acl public-read" in command or "--acl public-read-write" in command:
        messages.append("Security: Public access permission detected")

    # Sync delete check
    if "s3 sync" in command and "--delete" in command:
        messages.append("Note: sync --delete removes files not in source")
```

### IAM Security
```python
if "iam" in command:
    if "attach-" in command and "AdministratorAccess" in command:
        messages.append("Security: Attaching admin privileges - confirm necessity")

    if "create-access-key" in command:
        messages.append("Security: Store access keys securely, avoid leaks")
```

### Cost Awareness
```python
cost_operations = ["run-instances", "create-db-instance", "create-cluster"]
for op in cost_operations:
    if op in command:
        messages.append("Cost: This operation incurs AWS charges")
        break
```

### Best Practices
```python
# Profile recommendation
if "aws" in command and "--profile" not in command:
    messages.append("Suggestion: Use --profile to specify AWS configuration")

# Region recommendation
if "--region" not in command and "AWS_DEFAULT_REGION" not in os.environ:
    messages.append("Suggestion: Use --region to specify AWS region")
```

---

## Docker Safety Patterns

### Image Naming Validation
```python
def validate_docker_command(tool_use):
    command = tool_use.get("tool_input", {}).get("command", "")

    if "docker build" in command or "docker tag" in command:
        # Find -t tag parameter
        tag_pattern = r"-t\s+([^\s]+)"
        matches = re.findall(tag_pattern, command)

        for tag in matches:
            # Check for disallowed suffixes
            bad_suffixes = ["-v2", "-v3", "-test", "-dev", "-prod", "-staging"]
            image_name = tag.split(":")[0]

            for suffix in bad_suffixes:
                if image_name.endswith(suffix):
                    clean_name = image_name[:-len(suffix)]
                    tag_part = tag.split(":")[1] if ":" in tag else "latest"
                    error_msg = f"Image name should not use '{suffix}'. Use: {clean_name}:{tag_part}"
                    print(error_msg, file=sys.stderr)
                    sys.exit(2)
```

---

## Notification Patterns

### Event Detection by Command Pattern
```python
event_patterns = {
    # Build events
    r"(cargo|maven|gradle|npm|yarn|pnpm)\s+(build|compile)": ("build_start", "Build started"),
    r"cargo\s+check": ("build_check", "Code check"),
    r"npm\s+run\s+build": ("build_start", "Frontend build"),

    # Test events
    r"(cargo|npm|yarn|pytest|jest)\s+test": ("test_start", "Test started"),
    r"mvn\s+test": ("test_start", "Maven test"),

    # Deploy events
    r"aws\s+.*\s+deploy": ("deploy_start", "AWS deployment"),
    r"docker\s+push": ("deploy_start", "Docker image push"),
    r"git\s+push.*production": ("deploy_start", "Production deployment"),

    # Git events
    r"git\s+commit": ("code_commit", "Code commit"),
    r"git\s+push": ("code_push", "Code push"),
    r"git\s+merge": ("code_merge", "Code merge"),

    # Security events
    r"npm\s+audit": ("security_check", "Dependency security check"),
    r"cargo\s+audit": ("security_check", "Rust security audit"),
}
```

### Event Logging
```python
def log_event(event_type, description, command):
    log_dir = os.path.expanduser("~/.claude/logs/events")
    os.makedirs(log_dir, exist_ok=True)

    log_file = os.path.join(log_dir, f"events_{datetime.now().strftime('%Y%m%d')}.log")

    log_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "event_type": event_type,
        "description": description,
        "command": command,
        "user": os.environ.get("USER", "Unknown"),
        "cwd": os.getcwd(),
    }

    with open(log_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
```

### Category-Based Display
```python
level_emoji = {
    "build": "hammer",
    "test": "test_tube",
    "deploy": "rocket",
    "code": "floppy_disk",
    "security": "lock",
}

category = event_type.split("_")[0]
emoji = level_emoji.get(category, "memo")
print(f"{emoji} {description}")
```

---

## Command Logging

### Multi-Tool Logging Support
```python
def log_command(tool_use):
    log_dir = os.path.expanduser("~/.claude/logs")
    os.makedirs(log_dir, exist_ok=True)

    log_file = os.path.join(log_dir, f"commands_{datetime.now().strftime('%Y%m%d')}.log")

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    tool = tool_use.get("tool") or tool_use.get("tool_name", "Unknown")

    log_entry = {
        "timestamp": timestamp,
        "tool": tool,
    }

    arguments = tool_use.get("arguments") or tool_use.get("tool_input", {})

    # Tool-specific logging
    if tool == "Bash":
        log_entry["command"] = arguments.get("command", "")
    elif tool in ["Write", "Edit", "MultiEdit"]:
        log_entry["file"] = arguments.get("file_path", "")
    elif tool == "Read":
        log_entry["file"] = arguments.get("file_path", "")
    elif tool in ["Grep", "Glob"]:
        log_entry["pattern"] = arguments.get("pattern", "")
        log_entry["path"] = arguments.get("path", ".")

    with open(log_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
```

---

## File Statistics Pattern

### Multi-Language Function Counting
```python
def count_functions(content, file_ext):
    function_counts = {
        "python": len(re.findall(r"^\s*def\s+\w+", content, re.MULTILINE))
                + len(re.findall(r"^\s*async\s+def\s+\w+", content, re.MULTILINE)),
        "javascript": len(re.findall(
            r"function\s+\w+\s*\(|const\s+\w+\s*=\s*\(|^\s*\w+\s*\(",
            content, re.MULTILINE)),
        "java": len(re.findall(
            r"^\s*(public|private|protected)?\s*(static)?\s*\w+\s+\w+\s*\(",
            content, re.MULTILINE)),
        "go": len(re.findall(r"^\s*func\s+", content, re.MULTILINE)),
        "rust": len(re.findall(r"^\s*fn\s+\w+", content, re.MULTILINE)),
    }

    ext_map = {
        ".py": "python",
        ".js": "javascript", ".jsx": "javascript",
        ".ts": "javascript", ".tsx": "javascript",
        ".java": "java",
        ".go": "go",
        ".rs": "rust",
    }

    lang = ext_map.get(file_ext, None)
    return function_counts.get(lang, 0) if lang else 0
```

### File Analysis Output
```python
def analyze_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    lines = content.split("\n")
    file_ext = os.path.splitext(file_path)[1]

    stats = {
        "lines": len(lines),
        "characters": len(content),
        "words": len(content.split()),
        "functions": count_functions(content, file_ext),
        "classes": len(re.findall(r"^\s*class\s+\w+", content, re.MULTILINE)),
    }
    return stats
```

---

## Configuration Examples

### Settings.json Structure
```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "type": "command",
        "command": "/path/to/hooks/terminal-ui.sh"
      }
    ],
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {"type": "command", "command": "/path/to/hooks/docker-validator.py"},
          {"type": "command", "command": "/path/to/hooks/git-safety-check.py"},
          {"type": "command", "command": "/path/to/hooks/npm-safety-check.py"},
          {"type": "command", "command": "/path/to/hooks/cargo-auto-format.py"},
          {"type": "command", "command": "/path/to/hooks/java-build-check.py"},
          {"type": "command", "command": "/path/to/hooks/aws-safety-check.py"},
          {"type": "command", "command": "/path/to/hooks/dev-event-notifier.py"},
          {"type": "command", "command": "/path/to/hooks/commit-message-filter.py"}
        ]
      },
      {
        "matcher": ".*",
        "hooks": [
          {"type": "command", "command": "/path/to/hooks/command-logger.py"}
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Write|Edit|MultiEdit",
        "hooks": [
          {"type": "command", "command": "/path/to/hooks/file-stats.py"}
        ]
      }
    ]
  }
}
```

### Hook Lifecycle Events
- **UserPromptSubmit**: Before user prompt is processed (UI hooks)
- **PreToolUse**: Before any tool execution (safety/validation hooks)
- **PostToolUse**: After tool execution (stats/logging hooks)

### Matcher Patterns
- `"Bash"`: Only Bash tool
- `"Write|Edit|MultiEdit"`: File modification tools
- `".*"`: All tools (universal logging)

---

## Code to Copy

### Base Hook Template
```python
#!/usr/bin/env python3
"""
Hook Name - Brief description
"""

import sys
import json
import re


def check_operation(tool_use):
    """Main validation logic"""
    tool = tool_use.get("tool") or tool_use.get("tool_name")
    if tool != "Bash":
        return

    arguments = tool_use.get("arguments") or tool_use.get("tool_input", {})
    command = arguments.get("command", "")

    # Your validation logic here
    if dangerous_condition(command):
        print("Error message", file=sys.stderr)
        sys.exit(2)


def main():
    """Main entry point"""
    try:
        tool_use_json = sys.stdin.read()
        tool_use = json.loads(tool_use_json)

        check_operation(tool_use)

        # Allow operation if no issues
        sys.exit(0)

    except Exception:
        # Silent failure - don't block on hook errors
        sys.exit(0)


if __name__ == "__main__":
    main()
```

### Pattern-Based Warning Hook
```python
def check_command(command):
    """Pattern-based command checking"""
    messages = []

    warning_patterns = {
        r"pattern1": "Warning message 1",
        r"pattern2": "Warning message 2",
    }

    for pattern, warning in warning_patterns.items():
        if re.search(pattern, command, re.IGNORECASE):
            messages.append(f"Warning: {warning}")

    return messages

def main():
    try:
        tool_use_json = sys.stdin.read()
        tool_use = json.loads(tool_use_json)

        tool = tool_use.get("tool") or tool_use.get("tool_name")
        if tool != "Bash":
            sys.exit(0)

        arguments = tool_use.get("arguments") or tool_use.get("tool_input", {})
        command = arguments.get("command", "")

        messages = check_command(command)
        if messages:
            print("\n".join(messages))

        sys.exit(0)  # Warning only, never block

    except Exception:
        sys.exit(0)
```

### ANSI Color Output
```python
# ANSI color codes for terminal output
red = "\033[1;31m"
yellow = "\033[1;33m"
green = "\033[1;32m"
blue = "\033[1;34m"
reset = "\033[0m"

error_msg = f"""{red}Error: Something went wrong{reset}
{yellow}Command:{reset} {command}
{green}Suggestion:{reset} Use alternative approach
{blue}Learn more:{reset} https://example.com"""
```

---

## Notes for Implementation

### Note 1: Error Handling Priority
Always prioritize not blocking legitimate operations. Use try/except with silent exit(0) to avoid hook failures disrupting workflow.

### Note 2: Context-Aware Detection
When detecting patterns in commit messages or heredocs, verify position to avoid false positives (see --no-verify pattern).

### Note 3: Multi-Format Support
Support both `tool_name`/`tool_input` (new) and `tool`/`arguments` (old) formats for compatibility.

### Note 4: Log Directory Structure
Use consistent log structure: `~/.claude/logs/` for general logs, `~/.claude/logs/events/` for events, with date-based file naming.

### Note 5: Hook Categories
- **Blocking (exit 2)**: Security-critical, naming violations, dangerous operations
- **Warning (exit 0 + stdout)**: Best practices, suggestions, reminders
- **Audit (exit 0)**: Logging, statistics, notifications

### Note 6: Tool-Specific Matchers
Use appropriate matchers to minimize unnecessary hook execution:
- `Bash`: Shell commands, git, npm, docker
- `Write|Edit|MultiEdit`: File modifications
- `.*`: Universal (logging only)

### Note 7: Internationalization
The repository includes Chinese (zh-CN) messages. Consider i18n support for user-facing messages.

### Note 8: Terminal UI Enhancement
For UI hooks, use ANSI escape codes for colors and box-drawing characters for visual appeal.

---

## Summary Statistics

| Category | Count | Exit Code |
|----------|-------|-----------|
| Blocking Hooks | 6 | 2 |
| Warning Hooks | 4 | 0 |
| Audit Hooks | 3 | 0 |
| UI Hooks | 1 | 0 |
| Filter Hooks | 1 | 2 |

### Tools Covered
- Git operations
- npm/yarn/pnpm package management
- AWS CLI commands
- Docker build/tag operations
- Cargo/Rust builds
- Maven/Gradle Java builds
- Python tool enforcement (uv)
- File naming conventions

---

*Document generated for Nexus Advanced Hook System research*
