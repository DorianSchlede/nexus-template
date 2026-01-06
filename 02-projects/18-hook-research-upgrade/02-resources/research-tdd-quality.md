# TDD & Quality Patterns Research Results

## Executive Summary

TDD enforcement hooks implement a sophisticated multi-phase validation pattern using AI-powered compliance checking and stateful notification systems. The core patterns include: (1) AI-based TDD validation gates that block operations violating test-first principles, (2) two-phase notification/block patterns that warn before enforcing, and (3) auto-formatter chains that run linters and formatters after file modifications. These patterns use persistent JSON file storage for state management across hook invocations.

---

## 1. TDD Enforcement Patterns

### 1.1 AI-Powered TDD Validation Gate

**Concept**: Intercept Write/Edit/MultiEdit operations, build context from test results and modifications, send to AI model for TDD compliance check, block operations that violate test-first principles.

**Source**: tdd-guard repository

**Implementation**:
```python
import json
import sys
from pathlib import Path
import subprocess

def validate_tdd_compliance(context: dict) -> dict:
    """
    Send operation context to AI for TDD compliance validation.
    Returns {"decision": "block"|"allow", "reason": str}
    """
    prompt = build_tdd_prompt(context)

    # Call Claude CLI for validation
    result = subprocess.run(
        ["claude", "-p", prompt],
        capture_output=True, text=True, timeout=30
    )

    # Parse AI response (expects JSON with decision and reason)
    response = extract_json_from_response(result.stdout)
    return {
        "decision": response.get("decision", "allow"),
        "reason": response.get("reason", "")
    }

def build_tdd_prompt(context: dict) -> str:
    """Build TDD validation prompt with context."""
    return f"""## TDD Fundamentals

### The TDD Cycle
1. **Red Phase**: Write ONE failing test that describes desired behavior
2. **Green Phase**: Write MINIMAL code to make the test pass
3. **Refactor Phase**: Improve code structure while keeping tests green

### Current Operation
{json.dumps(context.get("modifications", {}), indent=2)}

### Test Results
{context.get("test", "No test results available")}

### Current Todos
{context.get("todo", "No todos")}

### Lint Issues
{context.get("lint", "No lint issues")}

Analyze if this operation follows TDD principles. Return JSON:
{{"decision": "block" or "allow", "reason": "explanation"}}
"""

def main():
    try:
        data = json.load(sys.stdin)
        tool_name = data.get("tool_name", "")

        # Only validate file modification operations
        if tool_name not in ["Write", "Edit", "MultiEdit"]:
            sys.exit(0)

        # Load context from storage
        context = load_context_from_storage()
        context["modifications"] = data.get("tool_input", {})

        # Validate with AI
        result = validate_tdd_compliance(context)

        if result["decision"] == "block":
            print(json.dumps({
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny",
                    "permissionDecisionReason": result["reason"]
                }
            }))

        sys.exit(0)

    except Exception:
        sys.exit(0)  # Fail-open

if __name__ == "__main__":
    main()
```

**When to use**: Strict TDD enforcement in AI-assisted development. Prevents implementation without failing tests.

**When NOT to use**: Quick prototyping, exploratory coding, or non-testable files (config, docs).

### 1.2 Test-Before-Commit Pattern

**Concept**: Block git commits if tests are not passing.

**Implementation**:
```python
import json
import sys
import subprocess

def main():
    try:
        data = json.load(sys.stdin)
        tool_name = data.get("tool_name", "")
        tool_input = data.get("tool_input", {})

        # Only check git commit commands
        if tool_name != "Bash":
            sys.exit(0)

        command = tool_input.get("command", "")
        if "git commit" not in command:
            sys.exit(0)

        # Run tests
        test_result = subprocess.run(
            ["pytest", "--tb=short", "-q"],
            capture_output=True, text=True, timeout=120
        )

        if test_result.returncode != 0:
            print(json.dumps({
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny",
                    "permissionDecisionReason": f"Tests must pass before committing:\n{test_result.stdout[:500]}"
                }
            }))
            sys.exit(0)

        sys.exit(0)

    except Exception:
        sys.exit(0)

if __name__ == "__main__":
    main()
```

**When to use**: PreToolUse on Bash when command contains "git commit"

### 1.3 Test-After-Edit Pattern

**Concept**: Run tests after editing test files to verify they still pass/fail as expected.

**Implementation**:
```python
import json
import sys
import subprocess
from pathlib import Path

def main():
    try:
        data = json.load(sys.stdin)
        tool_name = data.get("tool_name", "")
        tool_input = data.get("tool_input", {})

        if tool_name not in ["Write", "Edit", "MultiEdit"]:
            sys.exit(0)

        file_path = tool_input.get("file_path", "")

        # Check if it's a test file
        if not is_test_file(file_path):
            sys.exit(0)

        # Run the specific test file
        result = subprocess.run(
            ["pytest", file_path, "-v", "--tb=short"],
            capture_output=True, text=True, timeout=60
        )

        # Store results for context
        save_test_results(result)

        # Output test status as system message
        if result.returncode != 0:
            print(json.dumps({
                "systemMessage": f"Test results:\n{result.stdout[-500:]}"
            }))

        sys.exit(0)

    except Exception:
        sys.exit(0)

def is_test_file(path: str) -> bool:
    p = Path(path)
    return (
        p.name.startswith("test_") or
        p.name.endswith("_test.py") or
        "tests/" in str(p) or
        p.suffix in [".test.ts", ".test.js", ".spec.ts", ".spec.js"]
    )

if __name__ == "__main__":
    main()
```

**When to use**: PostToolUse after Edit on test files (*_test.py, *.test.ts, etc.)

### 1.4 Coverage Check Pattern

**Concept**: Warn if code coverage drops below threshold after edits.

**Implementation**:
```python
import json
import sys
import subprocess
import re
from pathlib import Path

COVERAGE_THRESHOLD = 80  # Minimum coverage percentage

def main():
    try:
        data = json.load(sys.stdin)
        tool_name = data.get("tool_name", "")
        tool_input = data.get("tool_input", {})

        if tool_name not in ["Write", "Edit", "MultiEdit"]:
            sys.exit(0)

        file_path = tool_input.get("file_path", "")

        # Skip non-Python/JS files
        if not file_path.endswith((".py", ".js", ".ts")):
            sys.exit(0)

        # Run coverage
        if file_path.endswith(".py"):
            result = subprocess.run(
                ["pytest", "--cov", "--cov-report=term-missing", "-q"],
                capture_output=True, text=True, timeout=120
            )
            coverage = extract_python_coverage(result.stdout)
        else:
            result = subprocess.run(
                ["npm", "test", "--", "--coverage"],
                capture_output=True, text=True, timeout=120
            )
            coverage = extract_js_coverage(result.stdout)

        if coverage is not None and coverage < COVERAGE_THRESHOLD:
            print(json.dumps({
                "systemMessage": f"WARNING: Coverage dropped to {coverage}% (threshold: {COVERAGE_THRESHOLD}%)"
            }))

        sys.exit(0)

    except Exception:
        sys.exit(0)

def extract_python_coverage(output: str) -> float | None:
    match = re.search(r"TOTAL\s+\d+\s+\d+\s+(\d+)%", output)
    return float(match.group(1)) if match else None

if __name__ == "__main__":
    main()
```

---

## 2. Auto-Formatter Chains

### 2.1 Python Formatting (Ruff/Black)

**Trigger**: After Write/Edit on .py files

**Implementation**:
```python
import json
import sys
import subprocess
from pathlib import Path

def format_python_file(file_path: str) -> tuple[bool, str]:
    """Run ruff check --fix and ruff format. Returns (success, output)."""
    path = Path(file_path)

    if not path.exists() or path.suffix != ".py":
        return True, ""

    # Skip virtual environments and cache
    if ".venv" in str(path) or "__pycache__" in str(path):
        return True, ""

    # Run ruff check with auto-fix
    check_result = subprocess.run(
        [
            "ruff", "check", "--fix",
            "--extend-select", "F,I,D,UP,RUF,FA",
            "--target-version", "py39",
            str(path)
        ],
        capture_output=True, text=True, timeout=30
    )

    if check_result.returncode != 0:
        return False, check_result.stdout + check_result.stderr

    # Run ruff format
    format_result = subprocess.run(
        ["ruff", "format", "--line-length", "120", str(path)],
        capture_output=True, text=True, timeout=30
    )

    return format_result.returncode == 0, format_result.stdout + format_result.stderr

def main():
    try:
        data = json.load(sys.stdin)
        tool_name = data.get("tool_name", "")
        tool_input = data.get("tool_input", {})

        if tool_name not in ["Write", "Edit", "MultiEdit"]:
            sys.exit(0)

        file_path = tool_input.get("file_path", "")
        if not file_path.endswith(".py"):
            sys.exit(0)

        success, output = format_python_file(file_path)

        if not success:
            print(json.dumps({
                "systemMessage": f"Ruff errors in {Path(file_path).name}",
                "hookSpecificOutput": {
                    "hookEventName": "PostToolUse",
                    "permissionDecision": "deny",
                    "permissionDecisionReason": f"Fix these ruff errors:\n{output[:500]}"
                }
            }))

        sys.exit(0)

    except Exception:
        sys.exit(0)

if __name__ == "__main__":
    main()
```

### 2.2 JavaScript/TypeScript (Prettier/ESLint)

**Trigger**: After Write/Edit on .js/.ts/.jsx/.tsx files

**Implementation**:
```python
import json
import sys
import subprocess
import re
from pathlib import Path

PRETTIER_EXTENSIONS = {".js", ".jsx", ".ts", ".tsx", ".css", ".less", ".scss",
                       ".json", ".yml", ".yaml", ".html", ".vue", ".svelte"}
LOCK_FILE_PATTERN = re.compile(r".*lock\.(json|yaml|yml)$|.*\.lock$")

def format_with_prettier_eslint(file_path: str) -> tuple[bool, str]:
    """Run ESLint --fix and Prettier. Returns (success, output)."""
    path = Path(file_path)

    if path.suffix not in PRETTIER_EXTENSIONS:
        return True, ""

    # Skip lock files and node_modules
    if LOCK_FILE_PATTERN.match(path.name) or "node_modules" in str(path):
        return True, ""

    output = ""

    # Run ESLint with auto-fix for JS/TS files
    if path.suffix in [".js", ".jsx", ".ts", ".tsx"]:
        eslint_result = subprocess.run(
            ["npx", "eslint", "--fix", str(path)],
            capture_output=True, text=True, timeout=30
        )
        if eslint_result.returncode != 0 and eslint_result.stderr:
            return False, eslint_result.stderr[:500]
        output += eslint_result.stdout

    # Run Prettier
    try:
        prettier_result = subprocess.run(
            ["npx", "prettier", "--write", "--print-width", "120", str(path)],
            capture_output=True, text=True, timeout=10
        )
        output += prettier_result.stdout
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass

    return True, output

def main():
    try:
        data = json.load(sys.stdin)
        tool_name = data.get("tool_name", "")
        tool_input = data.get("tool_input", {})

        if tool_name not in ["Write", "Edit", "MultiEdit"]:
            sys.exit(0)

        file_path = tool_input.get("file_path", "")
        path = Path(file_path)

        if path.suffix not in PRETTIER_EXTENSIONS:
            sys.exit(0)

        success, output = format_with_prettier_eslint(file_path)

        if not success:
            print(json.dumps({
                "hookSpecificOutput": {
                    "hookEventName": "PostToolUse",
                    "permissionDecision": "deny",
                    "permissionDecisionReason": f"ESLint errors:\n{output}"
                }
            }))

        sys.exit(0)

    except Exception:
        sys.exit(0)

if __name__ == "__main__":
    main()
```

### 2.3 Multi-Language Detection

```python
from pathlib import Path
import subprocess

FORMATTERS = {
    ".py": {
        "check": ["ruff", "check", "--fix"],
        "format": ["ruff", "format", "--line-length", "120"],
    },
    ".js": {"format": ["npx", "prettier", "--write"]},
    ".jsx": {"format": ["npx", "prettier", "--write"]},
    ".ts": {"format": ["npx", "prettier", "--write"]},
    ".tsx": {"format": ["npx", "prettier", "--write"]},
    ".go": {"format": ["gofmt", "-w"]},
    ".rs": {"format": ["rustfmt"]},
    ".sh": {"format": ["npx", "prettier", "--write", "--plugin=prettier-plugin-sh"]},
    ".bash": {"format": ["npx", "prettier", "--write", "--plugin=prettier-plugin-sh"]},
}

def get_formatter(file_path: str) -> dict | None:
    """Get formatter config for file type."""
    ext = Path(file_path).suffix
    return FORMATTERS.get(ext)

def run_formatter(file_path: str) -> tuple[bool, str]:
    """Run appropriate formatter for file type."""
    config = get_formatter(file_path)
    if not config:
        return True, ""

    output = ""

    # Run check/lint first if available
    if "check" in config:
        result = subprocess.run(
            config["check"] + [file_path],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode != 0:
            return False, result.stdout + result.stderr
        output += result.stdout

    # Run format
    if "format" in config:
        result = subprocess.run(
            config["format"] + [file_path],
            capture_output=True, text=True, timeout=30
        )
        output += result.stdout

    return True, output
```

---

## 3. Two-Phase Notification Pattern

### Concept

The two-phase pattern provides a "warning shot" before hard blocking:
- **First occurrence**: WARN (allow with message) and set notification flag
- **Second occurrence**: BLOCK (if issues persist)

This prevents disruption during iterative development while still enforcing quality.

### Use Cases

1. **Lint errors**: Warn first, block on repeat
2. **Missing tests**: Warn first, block on repeat
3. **Style violations**: Warn first, block on repeat
4. **Coverage drops**: Warn first, block on repeat

### Implementation

```python
import json
import sys
from pathlib import Path
from datetime import datetime

STATE_FILE = Path.home() / ".nexus" / "hook_state.json"

def load_state() -> dict:
    """Load hook state from persistent storage."""
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text())
        except json.JSONDecodeError:
            return {"warnings": {}}
    return {"warnings": {}}

def save_state(state: dict):
    """Save hook state to persistent storage."""
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2))

def two_phase_check(issue_key: str, message: str) -> tuple[bool, str]:
    """
    Implement two-phase notification pattern.

    Args:
        issue_key: Unique identifier for this issue (e.g., "lint:src/foo.py")
        message: The warning/error message to show

    Returns:
        (should_block, message_to_show)
    """
    state = load_state()
    warnings = state.get("warnings", {})

    if issue_key in warnings:
        # Second time seeing this issue - BLOCK
        return True, f"BLOCKED (repeated warning): {message}"
    else:
        # First time seeing this issue - WARN
        warnings[issue_key] = {
            "first_seen": datetime.now().isoformat(),
            "message": message
        }
        state["warnings"] = warnings
        save_state(state)
        return False, f"WARNING (will block next time): {message}"

def clear_warning(issue_key: str):
    """Clear a warning when issue is resolved."""
    state = load_state()
    warnings = state.get("warnings", {})
    if issue_key in warnings:
        del warnings[issue_key]
        state["warnings"] = warnings
        save_state(state)

def clear_all_warnings():
    """Clear all warnings (call on session start)."""
    save_state({"warnings": {}})
```

### Integration with PostToolUse

```python
def main():
    try:
        data = json.load(sys.stdin)
        tool_name = data.get("tool_name", "")
        tool_input = data.get("tool_input", {})

        if tool_name not in ["Write", "Edit", "MultiEdit"]:
            sys.exit(0)

        file_path = tool_input.get("file_path", "")
        if not file_path:
            sys.exit(0)

        # Run formatter/linter
        success, output = run_formatter(file_path)

        if not success:
            # Use two-phase pattern
            issue_key = f"format:{file_path}"
            should_block, message = two_phase_check(issue_key, output)

            if should_block:
                print(json.dumps({
                    "hookSpecificOutput": {
                        "hookEventName": "PostToolUse",
                        "permissionDecision": "deny",
                        "permissionDecisionReason": message
                    }
                }))
            else:
                print(json.dumps({
                    "systemMessage": message
                }))
        else:
            # Issue resolved - clear warning
            clear_warning(f"format:{file_path}")

        sys.exit(0)

    except Exception:
        sys.exit(0)

if __name__ == "__main__":
    main()
```

### Coordination Between PreToolUse and PostToolUse

The tdd-guard pattern uses coordinated state between hooks:

```python
# PreToolUse: Set notification flag when issues detected
async def handle_pre_tool_use(data, storage):
    lint_data = await storage.get_lint()
    has_issues = lint_data.error_count > 0

    if has_issues and not lint_data.has_notified_about_lint_issues:
        # First time - notify and set flag
        lint_data.has_notified_about_lint_issues = True
        await storage.save_lint(lint_data)
        return {
            "decision": "block",
            "reason": "Code quality issues detected. Fix before proceeding."
        }

    return {"decision": None}  # Allow

# PostToolUse: Block if notified AND issues persist
async def handle_post_tool_use(data, storage, linter):
    file_paths = extract_file_paths(data)
    lint_results = await linter.lint(file_paths)

    stored_lint_data = await storage.get_lint()
    has_issues = lint_results.error_count > 0

    # Block if: PreToolUse notified AND issues still exist
    if stored_lint_data.has_notified_about_lint_issues and has_issues:
        return {
            "decision": "block",
            "reason": format_lint_issues(lint_results)
        }

    # Update storage
    await storage.save_lint(lint_results)
    return {"decision": None}  # Allow
```

---

## 4. PostToolUse Quality Chain

### Proposed Flow

```
Tool Execution Complete
        |
        v
+----------------------+
|   PostToolUse Hook   |
|                      |
|  1. Check file type  |
|  2. Run formatter    |
|  3. Check lint       |
|  4. Two-phase warn   |
+----------------------+
        |
        v
    Continue
```

### Complete Implementation

```python
#!/usr/bin/env python3
"""
PostToolUse Quality Chain Hook
Runs formatters and linters after file modifications.
"""

import json
import sys
import subprocess
from pathlib import Path
from datetime import datetime

# Configuration
STATE_FILE = Path.home() / ".nexus" / "quality_state.json"

FORMATTERS = {
    ".py": {
        "check": ["ruff", "check", "--fix", "--extend-select", "F,I,D,UP,RUF,FA"],
        "format": ["ruff", "format", "--line-length", "120"],
    },
    ".js": {"format": ["npx", "prettier", "--write"]},
    ".ts": {"format": ["npx", "prettier", "--write"]},
    ".jsx": {"format": ["npx", "prettier", "--write"]},
    ".tsx": {"format": ["npx", "prettier", "--write"]},
}

SKIP_PATTERNS = [
    "node_modules/",
    ".venv/",
    "__pycache__/",
    ".git/",
    "dist/",
    "build/",
]


def should_skip_file(file_path: str) -> bool:
    """Check if file should be skipped."""
    return any(pattern in file_path for pattern in SKIP_PATTERNS)


def load_state() -> dict:
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text())
        except json.JSONDecodeError:
            pass
    return {"warnings": {}}


def save_state(state: dict):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2))


def two_phase_check(issue_key: str, message: str) -> tuple[bool, str]:
    state = load_state()
    warnings = state.get("warnings", {})

    if issue_key in warnings:
        return True, f"BLOCKED: {message}"
    else:
        warnings[issue_key] = datetime.now().isoformat()
        state["warnings"] = warnings
        save_state(state)
        return False, f"WARNING (will block next time): {message}"


def clear_warning(issue_key: str):
    state = load_state()
    warnings = state.get("warnings", {})
    if issue_key in warnings:
        del warnings[issue_key]
        state["warnings"] = warnings
        save_state(state)


def run_formatter(file_path: str) -> tuple[bool, str]:
    """Run appropriate formatter for file type."""
    path = Path(file_path)
    config = FORMATTERS.get(path.suffix)

    if not config or not path.exists():
        return True, ""

    output_parts = []

    # Run check/lint
    if "check" in config:
        try:
            result = subprocess.run(
                config["check"] + [str(path)],
                capture_output=True, text=True, timeout=30
            )
            if result.returncode != 0:
                return False, result.stdout + result.stderr
            output_parts.append(result.stdout)
        except (subprocess.TimeoutExpired, FileNotFoundError) as e:
            output_parts.append(f"Check skipped: {e}")

    # Run format
    if "format" in config:
        try:
            result = subprocess.run(
                config["format"] + [str(path)],
                capture_output=True, text=True, timeout=30
            )
            output_parts.append(result.stdout)
        except (subprocess.TimeoutExpired, FileNotFoundError) as e:
            output_parts.append(f"Format skipped: {e}")

    return True, "\n".join(output_parts)


def extract_file_paths(data: dict) -> list[str]:
    """Extract file paths from tool input."""
    tool_input = data.get("tool_input", {})
    paths = []

    # Single file_path
    if "file_path" in tool_input:
        paths.append(tool_input["file_path"])

    # MultiEdit edits array
    if "edits" in tool_input and isinstance(tool_input["edits"], list):
        for edit in tool_input["edits"]:
            if "file_path" in edit:
                paths.append(edit["file_path"])

    return list(set(paths))  # Deduplicate


def main():
    try:
        data = json.load(sys.stdin)
        tool_name = data.get("tool_name", "")

        # Only process file modification tools
        if tool_name not in ["Write", "Edit", "MultiEdit"]:
            sys.exit(0)

        file_paths = extract_file_paths(data)

        for file_path in file_paths:
            # Skip excluded files
            if should_skip_file(file_path):
                continue

            # Run formatter
            success, output = run_formatter(file_path)

            if not success:
                # Two-phase pattern
                issue_key = f"quality:{file_path}"
                should_block, message = two_phase_check(issue_key, output[:500])

                if should_block:
                    print(json.dumps({
                        "hookSpecificOutput": {
                            "hookEventName": "PostToolUse",
                            "permissionDecision": "deny",
                            "permissionDecisionReason": message
                        }
                    }))
                    sys.exit(0)
                else:
                    print(json.dumps({
                        "systemMessage": message
                    }))
            else:
                # Clear warning on success
                clear_warning(f"quality:{file_path}")

        sys.exit(0)

    except json.JSONDecodeError:
        sys.exit(0)
    except Exception:
        sys.exit(0)


if __name__ == "__main__":
    main()
```

---

## 5. Integration Notes

### Current PostToolUse State

The current Nexus `post_tool_use.py` does minimal processing:
- Reads JSON from stdin
- Logs to session-specific JSON file
- Uses session_id for log directory organization
- Graceful error handling (always exits 0)

**Location**: `.claude/hooks/post_tool_use.py`

### Safe to Add

The following patterns can be safely integrated:

1. **Formatter execution** (subprocess, no database dependency)
2. **Two-phase state** (local JSON file in ~/.nexus/)
3. **Warning output** (systemMessage for non-blocking feedback)
4. **File statistics** (count lines, functions, classes)

### Must Not Break

- Session logging functionality
- Graceful error handling (fail-open)
- Performance budget

### Performance Budget

| Operation | Target | Max |
|-----------|--------|-----|
| PostToolUse total | <50ms | <200ms |
| Formatter (per file) | <100ms | 30s timeout |
| State file I/O | <5ms | <10ms |
| JSON parsing | <1ms | <5ms |

### Performance Tips

1. **Use caching**: Cache formatter availability checks
2. **Run with --cache**: Use `ruff --cache`, `prettier --cache`
3. **Skip unchanged**: Hash file content to skip formatting
4. **Parallel formatting**: Use asyncio for multiple files
5. **Early exit**: Check file extension before subprocess

### Testing Approach

```python
import json
import pytest

def test_handles_write_tool():
    """Test that Write tool triggers formatting."""
    input_data = {
        "hook_event_name": "PostToolUse",
        "tool_name": "Write",
        "tool_input": {"file_path": "/tmp/test.py", "content": "print('hello')"},
        "tool_response": {"success": True}
    }
    result = process_hook(json.dumps(input_data))
    assert result["exit_code"] == 0

def test_handles_malformed_json():
    """Test graceful handling of invalid JSON."""
    result = process_hook("not valid json")
    assert result["exit_code"] == 0  # Fail-open

def test_ignores_non_file_tools():
    """Test that non-file tools are ignored."""
    input_data = {
        "hook_event_name": "PostToolUse",
        "tool_name": "Bash",
        "tool_input": {"command": "ls"}
    }
    result = process_hook(json.dumps(input_data))
    assert result["exit_code"] == 0

def test_two_phase_warn_then_block():
    """Test two-phase notification pattern."""
    clear_all_warnings()

    # First time - warn
    blocked, msg = two_phase_check("test:key", "error message")
    assert not blocked
    assert "WARNING" in msg

    # Second time - block
    blocked, msg = two_phase_check("test:key", "error message")
    assert blocked
    assert "BLOCKED" in msg

def test_clear_warning_on_fix():
    """Test that fixing issues clears the warning."""
    clear_all_warnings()

    # Set warning
    two_phase_check("test:key", "error")

    # Clear it
    clear_warning("test:key")

    # Should warn again, not block
    blocked, msg = two_phase_check("test:key", "error")
    assert not blocked
```

---

## 6. File Ignore Patterns

The tdd-guard uses minimatch patterns to skip validation for certain file types:

```python
from fnmatch import fnmatch

DEFAULT_IGNORE_PATTERNS = [
    "*.md",
    "*.txt",
    "*.log",
    "*.json",
    "*.yml",
    "*.yaml",
    "*.xml",
    "*.html",
    "*.css",
    "*.rst",
    "*.lock",
    "*lock.json",
]

def should_ignore_file(file_path: str, patterns: list[str] = None) -> bool:
    """Check if file should be ignored based on patterns."""
    patterns = patterns or DEFAULT_IGNORE_PATTERNS
    name = Path(file_path).name

    for pattern in patterns:
        if fnmatch(name, pattern):
            return True
    return False
```

---

## Summary

### Key Patterns Documented

1. **AI-Powered TDD Validation Gate** - Semantic TDD compliance checking
2. **Test-Before-Commit** - Block commits without passing tests
3. **Test-After-Edit** - Run tests after editing test files
4. **Coverage Check** - Warn when coverage drops
5. **Python Ruff Formatter** - Auto-fix and format Python files
6. **Prettier/ESLint Chain** - Format JS/TS files
7. **Multi-Language Detection** - Route to appropriate formatter
8. **Two-Phase Notification** - Warn first, block on repeat
9. **PostToolUse Quality Chain** - Complete formatter chain

### Best Practices

1. **Fail-open**: Always exit 0 on errors
2. **Performance**: Keep total time <200ms
3. **Two-phase**: Warn before blocking
4. **State persistence**: Use local JSON files
5. **File filtering**: Skip non-code files
6. **Timeouts**: 30s max for formatters

### Ready for Implementation

All patterns include copy-paste-ready code templates with:
- Error handling
- Performance considerations
- Integration points
- Test examples
