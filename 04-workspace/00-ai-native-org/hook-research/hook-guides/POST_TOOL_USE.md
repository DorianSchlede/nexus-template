# PostToolUse Hook - Comprehensive Guide

## 1. Overview

### What This Hook Does
The **PostToolUse** hook fires immediately after a Claude Code tool completes execution, but before the result is returned to Claude. This allows you to:
- Inspect the tool's output
- Log completed operations for audit trails
- Run automated quality checks (linting, formatting)
- Block further operations based on results
- Inject additional context based on what was just done

### When It Fires (Trigger Conditions)
PostToolUse fires after ANY tool execution completes, including:
- `Write` - After a file is written
- `Edit` - After a file edit is applied
- `MultiEdit` - After multiple edits are applied
- `Bash` - After a shell command completes
- `Read` - After a file is read
- `Glob` - After file pattern matching
- `Grep` - After content search
- `Task` - After a subagent task completes
- Any MCP tools

The hook receives the **tool response** in addition to the original input.

### Can It Block?
**Yes** - Exit code 2 or returning `permissionDecision: "deny"` blocks further processing. However, since the tool has already executed, blocking at PostToolUse typically:
1. Prevents Claude from seeing the result
2. Forces a retry or alternative approach
3. Allows you to signal that the operation needs correction

### JSON Input Schema
```json
{
  "hook_event_name": "PostToolUse",
  "session_id": "string",
  "transcript_path": "/path/to/transcript.jsonl",
  "tool_name": "Write|Edit|Bash|...",
  "tool_input": {
    // Original tool input - varies by tool
    "file_path": "string",    // For Write/Edit
    "command": "string",       // For Bash
    "content": "string",       // For Write
    "old_string": "string",    // For Edit
    "new_string": "string"     // For Edit
  },
  "tool_response": {
    // Tool execution result - varies by tool
    "success": true,
    "output": "string",
    // ... tool-specific fields
  }
}
```

### JSON Output Schema

**Allow/Continue (exit 0 with empty or approve response):**
```json
{}
```
or
```json
{
  "hookSpecificOutput": {
    "hookEventName": "PostToolUse",
    "permissionDecision": "allow"
  }
}
```

**Block with reason (exit 0 with deny, or exit 2):**
```json
{
  "hookSpecificOutput": {
    "hookEventName": "PostToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "Explanation shown to Claude"
  }
}
```

**Inject context via systemMessage:**
```json
{
  "systemMessage": "Additional context injected into Claude's view"
}
```

---

## 2. Pattern Catalog

### Pattern: Event Logging
**Sources**: hooks-mastery, claude-hooks-ts, EvanL1/claude-code-hooks

**Description**: Logs all completed tool executions to JSON files for comprehensive audit trails. Captures tool name, input, response, and timestamp.

**Decision Type**: allow (exit 0)

**Implementation (Python)**:
```python
import json
import sys
from pathlib import Path

def main():
    try:
        input_data = json.load(sys.stdin)

        log_dir = Path.cwd() / 'logs'
        log_dir.mkdir(parents=True, exist_ok=True)
        log_path = log_dir / 'post_tool_use.json'

        if log_path.exists():
            with open(log_path, 'r') as f:
                try:
                    log_data = json.load(f)
                except (json.JSONDecodeError, ValueError):
                    log_data = []
        else:
            log_data = []

        log_data.append(input_data)

        with open(log_path, 'w') as f:
            json.dump(log_data, f, indent=2)

        sys.exit(0)

    except json.JSONDecodeError:
        sys.exit(0)
    except Exception:
        sys.exit(0)

if __name__ == '__main__':
    main()
```

**Pros**:
- Complete audit trail of all tool operations
- Enables post-session analysis and debugging
- Silent operation - never disrupts workflow
- Graceful error handling ensures reliability

**Cons**:
- Log files can grow large over time
- Synchronous file I/O adds small latency
- No log rotation built-in

**Use When**: You need compliance auditing, debugging traces, or usage analytics

**Avoid When**: High-frequency file operations where disk I/O is a concern

---

### Pattern: File Statistics Reporter
**Sources**: EvanL1/claude-code-hooks

**Description**: After file writes/edits, displays statistics including line count, character count, function count, and class count.

**Decision Type**: allow (exit 0)

**Implementation (Python)**:
```python
import json
import sys
import re
import os

def count_functions(content, file_ext):
    function_counts = {
        "python": len(re.findall(r"^\s*def\s+\w+", content, re.MULTILINE))
                 + len(re.findall(r"^\s*async\s+def\s+\w+", content, re.MULTILINE)),
        "javascript": len(re.findall(r"function\s+\w+\s*\(|const\s+\w+\s*=\s*\(", content, re.MULTILINE)),
        "go": len(re.findall(r"^\s*func\s+", content, re.MULTILINE)),
        "rust": len(re.findall(r"^\s*fn\s+\w+", content, re.MULTILINE)),
        "typescript": len(re.findall(r"function\s+\w+\s*\(|const\s+\w+\s*=\s*\(", content, re.MULTILINE)),
    }
    ext_map = {".py": "python", ".js": "javascript", ".go": "go", ".rs": "rust", ".ts": "typescript"}
    return function_counts.get(ext_map.get(file_ext, ""), 0)

def main():
    try:
        input_data = json.load(sys.stdin)
        tool_name = input_data.get("tool_name", "")
        tool_input = input_data.get("tool_input", {})

        if tool_name not in ["Write", "Edit", "MultiEdit"]:
            sys.exit(0)

        file_path = tool_input.get("file_path", "")
        if not file_path or not os.path.exists(file_path):
            sys.exit(0)

        with open(file_path, 'r') as f:
            content = f.read()

        lines = content.split('\n')
        _, ext = os.path.splitext(file_path)
        basename = os.path.basename(file_path)

        stats = {
            "lines": len(lines),
            "characters": len(content),
            "functions": count_functions(content, ext)
        }

        print(f"File stats: {basename} - Lines: {stats['lines']}, Characters: {stats['characters']}, Functions: {stats['functions']}")
        sys.exit(0)

    except Exception:
        sys.exit(0)

if __name__ == '__main__':
    main()
```

**Pros**:
- Provides immediate feedback on file changes
- Language-aware function counting
- Helps track code growth and complexity

**Cons**:
- Re-reads file after write (slight overhead)
- Function counting is regex-based (not AST-accurate)

**Use When**: Monitoring file changes, tracking code growth

**Avoid When**: High-frequency file operations where output would be noisy

---

### Pattern: TypeScript Quality Hooks (Auto-Fix Pipeline)
**Sources**: awesome-claude-code (bartolli), claude-codex-settings

**Description**: Quality check hook that runs TypeScript compilation, ESLint auto-fixing, and Prettier formatting after file edits. Uses SHA256 config caching for <5ms validation performance.

**Decision Type**: allow_with_modification (auto-fix) or block (on unfixable errors)

**Implementation (Python)**:
```python
import json
import sys
import subprocess
import os
from pathlib import Path

def main():
    try:
        input_data = json.load(sys.stdin)
        tool_name = input_data.get("tool_name", "")
        tool_input = input_data.get("tool_input", {})

        if tool_name not in ["Write", "Edit", "MultiEdit"]:
            sys.exit(0)

        file_path = tool_input.get("file_path", "")
        if not file_path:
            sys.exit(0)

        path = Path(file_path)

        # Only process TypeScript/JavaScript files
        if path.suffix not in ['.ts', '.tsx', '.js', '.jsx']:
            sys.exit(0)

        # Skip node_modules and virtual envs
        if 'node_modules' in str(path) or '.venv' in str(path):
            sys.exit(0)

        # Run ruff check with auto-fix (for Python) or ESLint for JS/TS
        try:
            result = subprocess.run([
                'npx', 'eslint', '--fix', str(path)
            ], capture_output=True, text=True, timeout=30)

            if result.returncode != 0 and result.stderr:
                # ESLint had unfixable errors
                print(json.dumps({
                    "systemMessage": f"ESLint issues in {path.name}",
                    "hookSpecificOutput": {
                        "hookEventName": "PostToolUse",
                        "permissionDecision": "deny",
                        "permissionDecisionReason": f"Fix ESLint errors:\n{result.stderr[:500]}"
                    }
                }))
                sys.exit(0)
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass

        # Run Prettier
        try:
            subprocess.run([
                'npx', 'prettier', '--write', str(path)
            ], capture_output=True, timeout=10)
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass

        sys.exit(0)

    except Exception:
        sys.exit(0)

if __name__ == '__main__':
    main()
```

**Pros**:
- Automatic code quality enforcement
- Consistent formatting across all edits
- Fast with caching

**Cons**:
- Requires ESLint/Prettier installed
- May modify files unexpectedly

**Use When**: TypeScript/JavaScript projects requiring consistent formatting

**Avoid When**: Non-TypeScript projects or projects with custom formatters

---

### Pattern: British English Spelling Converter (Britfix)
**Sources**: awesome-claude-code (Talieisin)

**Description**: Converts American spellings to British English after file writes. Context-aware: only converts comments and docstrings in code files, never identifiers or string literals.

**Decision Type**: allow_with_modification

**Implementation Concept**:
```python
# Conceptual - full implementation requires spelling dictionary
import json
import sys
import re

# American -> British spelling map (sample)
SPELLING_MAP = {
    'color': 'colour',
    'favor': 'favour',
    'behavior': 'behaviour',
    'center': 'centre',
    'organize': 'organise',
    # ... extensive dictionary
}

def convert_in_comments(content, file_ext):
    """Only convert spellings in comments, not in code."""
    if file_ext in ['.py']:
        # Convert in # comments and docstrings
        # Complex regex to identify comment/docstring regions
        pass
    elif file_ext in ['.js', '.ts']:
        # Convert in // and /* */ comments
        pass
    return content

def main():
    input_data = json.load(sys.stdin)
    tool_name = input_data.get("tool_name", "")
    tool_input = input_data.get("tool_input", {})

    if tool_name not in ["Write", "Edit"]:
        sys.exit(0)

    file_path = tool_input.get("file_path", "")
    # ... read file, convert, write back
    sys.exit(0)
```

**Pros**:
- Maintains regional spelling consistency
- Smart enough to avoid breaking code
- Important for compliance in UK/Commonwealth organizations

**Cons**:
- Requires comprehensive spelling dictionary
- Complex to implement correctly for code files

**Use When**: UK/Commonwealth organizations, compliance requirements

**Avoid When**: US-based projects, technical documentation with American tooling terms

---

### Pattern: Lint Enforcement (Two-Phase Block)
**Sources**: tdd-guard

**Description**: Runs linter on modified files after edits. Uses a two-phase approach: first warns, then blocks on repeat issues. Works with PreToolUse notification flag for coordinated enforcement.

**Decision Type**: block (on repeat lint failures)

**Implementation (TypeScript)**:
```typescript
interface LintData {
  errorCount: number;
  warningCount: number;
  hasNotifiedAboutLintIssues: boolean;
  issues: Array<{file: string; line: number; column: number; severity: string; message: string}>;
}

async function handlePostToolLint(hookData: string, storage: Storage, linter: Linter): Promise<ValidationResult> {
  const parsedData = JSON.parse(hookData);

  if (!['Write', 'Edit', 'MultiEdit'].includes(parsedData.tool_name)) {
    return { decision: undefined, reason: '' };
  }

  const filePaths = extractFilePaths(parsedData);
  if (filePaths.length === 0) return { decision: undefined, reason: '' };

  const storedLintData = await storage.getLint();
  const lintResults = await linter.lint(filePaths);

  const hasIssues = lintResults.errorCount > 0 || lintResults.warningCount > 0;

  // Block if: PreToolUse already notified AND issues persist
  if (storedLintData?.hasNotifiedAboutLintIssues && hasIssues) {
    return {
      decision: 'block',
      reason: formatLintIssues(lintResults)
    };
  }

  // Update storage for next check
  await storage.saveLint({
    ...lintResults,
    hasNotifiedAboutLintIssues: hasIssues
  });

  return { decision: undefined, reason: '' };
}
```

**Pros**:
- Enforces code quality during TDD refactor phase
- Two-phase approach prevents disruption
- Coordinates with PreToolUse for complete coverage

**Cons**:
- Requires linter setup
- State management adds complexity
- May slow down rapid iteration

**Use When**: Enforcing strict code quality, TDD workflows

**Avoid When**: Prototyping, exploratory coding

---

### Pattern: Marketplace to Plugin Sync
**Sources**: claude-codex-settings

**Description**: After editing marketplace.json, automatically syncs plugin entries to individual plugin.json manifest files.

**Decision Type**: allow (with side effects)

**Implementation (Python)**:
```python
import json
import sys
from pathlib import Path

def main():
    input_data = json.load(sys.stdin)
    tool_name = input_data.get("tool_name", "")
    tool_input = input_data.get("tool_input", {})

    if tool_name not in ["Write", "Edit", "MultiEdit"]:
        sys.exit(0)

    file_path = tool_input.get("file_path", "")
    if not file_path.endswith("marketplace.json"):
        sys.exit(0)

    marketplace_path = Path(file_path)
    if not marketplace_path.exists():
        sys.exit(0)

    marketplace = json.loads(marketplace_path.read_text())
    plugins = marketplace.get("plugins", [])

    for plugin in plugins:
        source = plugin.get("source")
        plugin_dir = (marketplace_path.parent / source).resolve()
        plugin_json_path = plugin_dir / ".claude-plugin" / "plugin.json"

        plugin_json_path.parent.mkdir(parents=True, exist_ok=True)

        plugin_data = {
            "name": plugin.get("name", ""),
            "version": plugin.get("version", ""),
            "description": plugin.get("description", ""),
        }

        plugin_json_path.write_text(json.dumps(plugin_data, indent=2))

    sys.exit(0)

if __name__ == '__main__':
    main()
```

**Pros**:
- Maintains consistency across plugin manifests
- Automatic - no manual sync needed
- Supports plugin marketplace workflows

**Cons**:
- Specific to plugin architecture
- May overwrite manual changes

**Use When**: Plugin-based architectures with centralized manifest

**Avoid When**: Single-plugin projects

---

### Pattern: Whitespace Line Cleaner
**Sources**: claude-codex-settings

**Description**: Removes whitespace-only lines from Python/JS/TS files after edits using sed.

**Decision Type**: allow (with side effects)

**Implementation (Bash inline hook)**:
```bash
file_path=$(cat | jq -r '.tool_input.file_path // empty' 2>/dev/null)
if [[ -n "$file_path" && -f "$file_path" ]]; then
  case "$file_path" in
    *.py|*.js|*.jsx|*.ts|*.tsx)
      if [[ "$OSTYPE" == "darwin"* ]]; then
        sed -i '' 's/^[[:space:]]*$//g' "$file_path" 2>/dev/null || true
      else
        sed -i 's/^[[:space:]]*$//g' "$file_path" 2>/dev/null || true
      fi
    ;;
  esac
fi
```

**Pros**:
- Enforces consistent whitespace handling
- Simple and fast
- Cross-platform (macOS/Linux)

**Cons**:
- Modifies files silently
- May break intentional blank lines with whitespace

**Use When**: Enforcing consistent whitespace in source files

**Avoid When**: Projects with intentional whitespace formatting

---

### Pattern: Python Docstring Formatter
**Sources**: claude-codex-settings

**Description**: Formats Python docstrings to Google style after file edits, using AST-based detection.

**Decision Type**: block on failure, allow with modification on success

**Implementation Concept**:
```python
import ast
import json
import sys

def format_docstring(docstring: str) -> str:
    """Apply Google-style formatting to docstring."""
    lines = docstring.split('\n')

    # Capitalize first word if not URL
    if lines[0] and not lines[0].startswith('http'):
        lines[0] = lines[0][0].upper() + lines[0][1:]

    # Add period if missing
    if lines[0] and not lines[0].rstrip().endswith(('.', '!', '?', ':')):
        lines[0] = lines[0].rstrip() + '.'

    # Normalize section names
    section_map = {'Arguments': 'Args', 'Return': 'Returns', 'Raise': 'Raises'}
    # ... apply section normalization

    return '\n'.join(lines)

class DocstringVisitor(ast.NodeVisitor):
    def __init__(self):
        self.docstrings = []

    def visit_FunctionDef(self, node):
        docstring = ast.get_docstring(node)
        if docstring:
            self.docstrings.append((node.lineno, docstring))
        self.generic_visit(node)

def main():
    input_data = json.load(sys.stdin)
    # ... extract file, parse AST, format docstrings, write back
    sys.exit(0)
```

**Pros**:
- Enforces consistent docstring style
- AST-based detection is accurate
- Applies Google style conventions

**Cons**:
- Complex implementation
- May conflict with other docstring styles

**Use When**: Python projects requiring Google-style docstrings

**Avoid When**: Projects using NumPy or other docstring styles

---

### Pattern: Ruff Quality Gate
**Sources**: claude-codex-settings

**Description**: Auto-formats Python files with ruff check --fix and ruff format. Blocks on unfixable errors.

**Decision Type**: block on unfixable, allow with modification on success

**Implementation (Python)**:
```python
import json
import sys
import subprocess
from pathlib import Path

def main():
    input_data = json.load(sys.stdin)
    tool_name = input_data.get("tool_name", "")
    tool_input = input_data.get("tool_input", {})

    if tool_name not in ["Write", "Edit", "MultiEdit"]:
        sys.exit(0)

    file_path = tool_input.get("file_path", "")
    if not file_path.endswith('.py'):
        sys.exit(0)

    py_file = Path(file_path)
    if not py_file.exists():
        sys.exit(0)

    # Run ruff check with fixes
    check_result = subprocess.run([
        'ruff', 'check', '--fix',
        '--extend-select', 'F,I,D,UP,RUF,FA',
        '--target-version', 'py39',
        str(py_file)
    ], capture_output=True, text=True)

    if check_result.returncode != 0:
        print(json.dumps({
            'systemMessage': f'Ruff errors in {py_file.name}',
            'hookSpecificOutput': {
                'hookEventName': 'PostToolUse',
                'permissionDecision': 'deny',
                'permissionDecisionReason': f'Fix these ruff errors:\n{check_result.stdout}'
            }
        }))
        sys.exit(0)

    # Run ruff format
    subprocess.run(['ruff', 'format', '--line-length', '120', str(py_file)], capture_output=True)

    sys.exit(0)

if __name__ == '__main__':
    main()
```

**Pros**:
- Modern Python linting and formatting
- Fast (ruff is Rust-based)
- Auto-fixes many issues

**Cons**:
- Requires ruff installed
- May conflict with existing lint configs

**Use When**: Python projects using ruff

**Avoid When**: Projects with different linting tools

---

### Pattern: Prettier Auto-Formatter
**Sources**: claude-codex-settings

**Description**: Auto-formats JS/TS/CSS/JSON/YAML/HTML files with Prettier after edits.

**Decision Type**: allow with modification

**Implementation (Python)**:
```python
import json
import sys
import subprocess
import re
from pathlib import Path

PRETTIER_EXTENSIONS = {'.js', '.jsx', '.ts', '.tsx', '.css', '.less', '.scss',
                       '.json', '.yml', '.yaml', '.html', '.vue', '.svelte'}
LOCK_FILE_PATTERN = re.compile(r'.*lock\.(json|yaml|yml)$|.*\.lock$')

def main():
    input_data = json.load(sys.stdin)
    tool_name = input_data.get("tool_name", "")
    tool_input = input_data.get("tool_input", {})

    if tool_name not in ["Write", "Edit", "MultiEdit"]:
        sys.exit(0)

    file_path = tool_input.get("file_path", "")
    path = Path(file_path)

    # Skip non-prettier files
    if path.suffix not in PRETTIER_EXTENSIONS:
        sys.exit(0)

    # Skip lock files
    if LOCK_FILE_PATTERN.match(path.name):
        sys.exit(0)

    # Skip node_modules and venvs
    if 'node_modules' in str(path) or '.venv' in str(path):
        sys.exit(0)

    try:
        subprocess.run([
            'npx', 'prettier', '--write', '--print-width', '120', str(path)
        ], capture_output=True, timeout=10)
    except Exception:
        pass

    sys.exit(0)

if __name__ == '__main__':
    main()
```

**Pros**:
- Consistent formatting across web frontend files
- Widely adopted standard
- Handles many file types

**Cons**:
- Requires Node.js/npx
- May conflict with project prettier config

**Use When**: Web projects with Prettier configured

**Avoid When**: Projects with custom formatters

---

### Pattern: Graceful Error Handling
**Sources**: hooks-mastery, tdd-guard

**Description**: Implements fail-safe error handling that prevents hook failures from disrupting Claude's workflow. Always exits 0 on errors.

**Decision Type**: allow (fail-open)

**Implementation (Python)**:
```python
import json
import sys

def main():
    try:
        input_data = json.load(sys.stdin)

        # ... processing logic ...

        sys.exit(0)

    except json.JSONDecodeError:
        # Handle JSON decode errors gracefully
        sys.exit(0)
    except Exception:
        # Exit cleanly on any other error
        sys.exit(0)

if __name__ == '__main__':
    main()
```

**Pros**:
- Hooks never block on internal errors
- Robust against malformed input
- Silent failure prevents confusion

**Cons**:
- Errors may go unnoticed
- Debugging is harder without error logs

**Use When**: Observability hooks where blocking would be harmful

**Avoid When**: Safety-critical hooks where failure should be visible

---

### Pattern: File Write Success Logger
**Sources**: claude-hooks-ts

**Description**: Logs successful file write operations after completion.

**Decision Type**: allow (logging only)

**Implementation (TypeScript)**:
```typescript
const postToolUse: PostToolUseHandler = async (payload) => {
  await saveSessionData('PostToolUse', {...payload, hook_type: 'PostToolUse'} as const)

  if (payload.tool_name === 'Write' && payload.tool_response) {
    console.log(`File written successfully!`)
  }

  return {}
}
```

**Pros**:
- Simple confirmation of operations
- Useful for debugging
- Minimal overhead

**Cons**:
- Limited information

**Use When**: Tracking successful file operations

**Avoid When**: Minimal logging preferred

---

## 3. Inspiration Ideas

Based on the patterns found, here are additional use cases PostToolUse hooks could enable:

### New Use Cases

1. **Git Auto-Commit After Edits**: Automatically stage and commit files after successful edits with meaningful commit messages derived from the edit content.

2. **Test Runner Trigger**: After editing a source file, automatically run the corresponding test file and report results.

3. **Documentation Sync**: After editing code, automatically update related markdown documentation or JSDoc comments.

4. **Dependency Checker**: After package.json edits, verify dependencies are installed and compatible.

5. **Security Scanner**: After file writes, scan for hardcoded secrets, API keys, or sensitive data patterns.

6. **Backup Before Write**: Create timestamped backups of files before they're modified (capture the "before" state in PostToolUse of a Read, or use PreToolUse).

7. **Code Complexity Reporter**: After edits, calculate and report cyclomatic complexity changes.

8. **Import Organizer**: After TypeScript/JavaScript edits, automatically sort and organize imports.

9. **Type Annotation Checker**: After Python edits, verify type annotations are complete using mypy.

10. **Change Notification**: Send Slack/Discord notifications when specific files are modified.

### Combinations with Other Hooks

1. **PreToolUse + PostToolUse Timing**: Measure and report how long tool operations take.

2. **SessionStart + PostToolUse Analytics**: Track which tools are used most in a session.

3. **PostToolUse + Notification**: Trigger desktop notifications on successful file operations.

4. **PostToolUse + SubagentStop**: Aggregate results from subagent file operations.

### Advanced Applications

1. **Machine Learning Model Validator**: After editing ML config files, validate the model can still be loaded.

2. **Database Migration Checker**: After editing migration files, validate SQL syntax.

3. **CI/CD Pipeline Trigger**: After editing certain files, trigger a CI pipeline run.

4. **Performance Regression Checker**: After edits, run benchmarks and compare to baseline.

5. **Visual Regression Testing**: After editing React components, take screenshots and compare.

---

## 4. Implementation Recommendations

### Best Patterns to Adopt (Ranked)

1. **Graceful Error Handling** - Essential for all hooks. Always exit 0 on errors.

2. **Event Logging** - Provides audit trail without disrupting workflow.

3. **Ruff/Prettier Quality Gates** - Auto-fix where possible, block only on unfixable errors.

4. **Two-Phase Lint Enforcement** - Warn first, block on repeat. Less disruptive.

5. **File Statistics Reporter** - Useful feedback without blocking.

### Patterns to Avoid

1. **Aggressive Blocking** - PostToolUse blocks after the operation is done. Use sparingly.

2. **Heavy Processing** - Keep PostToolUse hooks fast (<100ms). Heavy work should be async.

3. **Modifying tool_response** - Not supported. PostToolUse can only block or allow.

4. **Complex State Management** - Use simple file-based state. Avoid databases.

### Performance Considerations

| Pattern | Typical Latency | Notes |
|---------|-----------------|-------|
| Event Logging | <10ms | File append is fast |
| File Stats | 10-50ms | Depends on file size |
| Prettier/ESLint | 50-100ms | Tool startup overhead |
| Ruff | 20-50ms | Faster than ESLint |
| Lint + Format Chain | 100-200ms | Consider async |

**Tips**:
- Use caching (SHA256 of config) to skip unchanged files
- Run formatters with `--cache` flags where available
- Consider running heavy processing asynchronously

### Testing Approach

1. **Unit Test JSON Parsing**: Test that your hook handles malformed JSON gracefully.

2. **Test Each Tool Type**: Verify behavior for Write, Edit, Bash, etc.

3. **Test Error Paths**: Ensure errors don't cause hook failures.

4. **Integration Test with Claude Code**: Use `claude --print-hooks` to verify hook is running.

5. **Log Output Testing**: Verify log files are created and contain expected data.

**Example Test Structure**:
```python
def test_handles_write_tool():
    input_data = {
        "hook_event_name": "PostToolUse",
        "tool_name": "Write",
        "tool_input": {"file_path": "/tmp/test.py", "content": "print('hello')"},
        "tool_response": {"success": True}
    }
    result = process_hook(json.dumps(input_data))
    assert result["exit_code"] == 0

def test_handles_malformed_json():
    result = process_hook("not valid json")
    assert result["exit_code"] == 0  # Graceful handling

def test_ignores_non_file_tools():
    input_data = {"tool_name": "Bash", "tool_input": {"command": "ls"}}
    result = process_hook(json.dumps(input_data))
    # Should exit quickly without processing
```

---

## Summary

PostToolUse hooks are ideal for:
- **Audit logging** - Track all operations
- **Quality enforcement** - Lint, format, validate
- **Metrics collection** - File stats, timing
- **Side effects** - Sync files, trigger builds

Key principles:
1. Always handle errors gracefully (exit 0)
2. Keep processing fast (<100ms)
3. Use blocking sparingly - the tool already ran
4. Log to files for debugging
5. Test with malformed input
