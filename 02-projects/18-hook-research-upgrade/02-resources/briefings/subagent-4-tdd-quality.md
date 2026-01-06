# Subagent Briefing: TDD & Quality Patterns Research

**Priority**: MEDIUM
**Output Path**: `02-projects/18-hook-research-upgrade/02-resources/research-tdd-quality.md`

---

## Mission

Research TDD enforcement patterns and code quality automation (formatters, linters). Understand how PostToolUse hooks can automatically format code and enforce testing requirements.

---

## Required Reading (IN ORDER - READ EVERYTHING)

### Step 1: Understand Research Structure
```
READ: 04-workspace/00-ai-native-org/hook-research/_index.md
```
Navigation hub.

### Step 2: TDD Guard Patterns (28 PATTERNS!)
```
READ: 04-workspace/00-ai-native-org/hook-research/patterns/tdd-guard-tool.yaml
```
Test-driven development enforcement patterns.

### Step 3: PostToolUse Guide
```
READ: 04-workspace/00-ai-native-org/hook-research/hook-guides/POST_TOOL_USE.md
```
What happens AFTER tool execution. Quality chains.

### Step 4: Codex Settings (Auto-formatters)
```
READ: 04-workspace/00-ai-native-org/hook-research/patterns/codex-settings.yaml
```
Formatter configuration patterns.

### Step 5: Two-Phase Notification
```
READ: 04-workspace/00-ai-native-org/hook-research/patterns/two-phase.yaml
```
Warn first, block on repeat pattern.

---

## Current Nexus System (FOR COMPARISON)

### Current PostToolUse
```
READ: .claude/hooks/post_tool_use.py
```
What does Nexus do after tool execution? Very minimal currently.

---

## Output Format

Create file at:
```
02-projects/18-hook-research-upgrade/02-resources/research-tdd-quality.md
```

Structure:

```markdown
# TDD & Quality Patterns Research Results

## Executive Summary
[2-3 sentences: What quality enforcement patterns exist?]

---

## 1. TDD Enforcement Patterns

### 1.1 Test-Before-Commit Pattern
**Concept**: Block commits if tests don't pass
**Implementation**:
\`\`\`python
[Code from tdd-guard-tool.yaml]
\`\`\`
**When to use**: PreToolUse on git commit

### 1.2 Test-After-Edit Pattern
**Concept**: Run tests after editing test files
**Implementation**:
\`\`\`python
[Code pattern]
\`\`\`
**When to use**: PostToolUse after Edit on *_test.py

### 1.3 Coverage Check Pattern
**Concept**: Warn if coverage drops
**Implementation**:
\`\`\`python
[Code pattern]
\`\`\`

---

## 2. Auto-Formatter Chains

### 2.1 Python Formatting (Ruff/Black)
**Trigger**: After Write/Edit on .py files
**Implementation**:
\`\`\`python
def format_python_file(file_path: str) -> tuple[bool, str]:
    """Run ruff/black on file. Returns (success, output)."""
    result = subprocess.run(
        ["ruff", "check", "--fix", file_path],
        capture_output=True, text=True, timeout=30
    )
    return result.returncode == 0, result.stdout + result.stderr
\`\`\`

### 2.2 JavaScript/TypeScript (Prettier/ESLint)
**Trigger**: After Write/Edit on .js/.ts files
**Implementation**:
\`\`\`python
[Code pattern]
\`\`\`

### 2.3 Multi-Language Detection
\`\`\`python
FORMATTERS = {
    ".py": ["ruff", "check", "--fix"],
    ".js": ["prettier", "--write"],
    ".ts": ["prettier", "--write"],
    ".go": ["gofmt", "-w"],
}

def get_formatter(file_path: str) -> list[str] | None:
    ext = Path(file_path).suffix
    return FORMATTERS.get(ext)
\`\`\`

---

## 3. Two-Phase Notification Pattern

### Concept
- First occurrence: WARN (allow with message)
- Second occurrence: BLOCK

### Use Cases
- Lint errors: warn first, block on repeat
- Missing tests: warn first, block on repeat
- Style violations: warn first, block on repeat

### Implementation
\`\`\`python
STATE_FILE = Path.home() / ".nexus" / "hook_state.json"

def load_state() -> dict:
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {"warnings": {}}

def save_state(state: dict):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state))

def two_phase_check(issue_key: str, message: str) -> tuple[bool, str]:
    """
    Returns (should_block, message_to_show)
    """
    state = load_state()
    warnings = state.get("warnings", {})

    if issue_key in warnings:
        # Second time - BLOCK
        return True, f"BLOCKED (repeated warning): {message}"
    else:
        # First time - WARN
        warnings[issue_key] = datetime.now().isoformat()
        state["warnings"] = warnings
        save_state(state)
        return False, f"WARNING (will block next time): {message}"
\`\`\`

---

## 4. PostToolUse Quality Chain

### Proposed Flow
\`\`\`
Tool Execution Complete
        │
        ▼
┌──────────────────────┐
│   PostToolUse Hook   │
│                      │
│  1. Check file type  │
│  2. Run formatter    │
│  3. Check lint       │
│  4. Two-phase warn   │
└──────────────────────┘
        │
        ▼
    Continue
\`\`\`

### Implementation
\`\`\`python
def main():
    data = json.load(sys.stdin)
    tool_name = data.get("tool_name")
    tool_input = data.get("tool_input", {})

    # Only process Write/Edit on code files
    if tool_name not in ["Write", "Edit"]:
        sys.exit(0)

    file_path = tool_input.get("file_path", "")
    if not file_path:
        sys.exit(0)

    # Get formatter for file type
    formatter = get_formatter(file_path)
    if not formatter:
        sys.exit(0)

    # Run formatter
    success, output = run_formatter(formatter, file_path)
    if not success:
        # Use two-phase pattern
        issue_key = f"format:{file_path}"
        should_block, message = two_phase_check(issue_key, output)
        if should_block:
            output_block(message)
            sys.exit(2)
        else:
            output_warn(message)

    sys.exit(0)
\`\`\`

---

## 5. Integration Notes

### Current PostToolUse State
[Document what post_tool_use.py currently does]

### Safe to Add
- Formatter execution (subprocess, no database)
- Two-phase state (local file)
- Warning output

### Performance Budget
- PostToolUse: <50ms typical, <200ms max
- Formatter timeout: 30s max
- Run async if possible

### Must Not Break
- Any existing database calls in post_tool_use.py
```

---

## Success Criteria

- [ ] All TDD enforcement patterns documented
- [ ] Auto-formatter chain pattern documented
- [ ] Two-phase notification pattern fully documented
- [ ] PostToolUse integration plan
- [ ] Performance considerations noted
- [ ] Copy-paste-ready code templates

---

## DO NOT

- ❌ Implement anything - research only
- ❌ Skip two-phase pattern - it's important for UX
- ❌ Suggest blocking formatters (use subprocess)
- ❌ Suggest long-running operations in hooks
