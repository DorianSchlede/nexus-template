# Context Loading Mechanisms in Claude Code Hooks

A comprehensive guide to injecting context into Claude's working memory through hooks.

---

## 1. Overview

### Why Context Loading Matters

Claude Code hooks are not just gates that approve or block operations - they can fundamentally shape Claude's understanding and behavior by injecting context at critical moments. This context loading capability transforms hooks from simple validators into powerful steering mechanisms that can:

- Guide Claude toward preferred tools, patterns, or workflows
- Provide explanations when operations are blocked
- Inject project-specific knowledge at session start
- Modify tool inputs silently for consistency
- Surface historical conversation data for decision-making
- Persist state across tool invocations

### The 6 Mechanisms Available

| Mechanism | Direction | Visibility | Primary Use Case |
|-----------|-----------|------------|------------------|
| **systemMessage** | Hook to Claude | Invisible to user | Directives, tips, redirection guidance |
| **permissionDecisionReason** | Hook to Claude | Visible to user | Blocking explanations, next steps |
| **updatedInput** | Hook to Claude | Silent | Tool input transformation |
| **Transcript Reading** | Conversation to Hook | N/A | Historical context for decisions |
| **State Files** | Hook to Hook | N/A | Cross-invocation persistence |
| **CLAUDE.md Modification** | Hook to Claude | Varies | Dynamic project context |

### When Each Is Appropriate

| Scenario | Best Mechanism |
|----------|----------------|
| Blocking a dangerous command with explanation | `permissionDecisionReason` |
| Redirecting to a different tool | `systemMessage` + `permissionDecisionReason` |
| Silently upgrading tool parameters | `updatedInput` |
| Loading project context at session start | `hookSpecificOutput.additionalContext` |
| Tracking notification flags across calls | State Files |
| Context-aware decisions based on conversation | Transcript Reading |

---

## 2. Mechanism Deep-Dives

### 2.1 systemMessage Field

#### What It Does

The `systemMessage` field allows hooks to inject invisible directives into Claude's context. Unlike `permissionDecisionReason`, which is shown to the user, `systemMessage` content is only seen by Claude, making it ideal for steering behavior without cluttering the user interface.

#### Which Hooks Support It

- **PreToolUse**: Inject guidance before tool execution
- **PostToolUse**: Provide context after tool completion
- **SessionStart**: Load project context at session initialization
- **UserPromptSubmit**: Add hidden context to prompts

#### Code Examples from Repos

**Tool Redirection (claude-codex-settings)**
```python
# webfetch_to_tavily_extract.py - Redirects WebFetch to Tavily
print(json.dumps({
    "systemMessage": "WebFetch detected. AI is directed to use Tavily extract instead.",
    "hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": f"Please use mcp__tavily__tavily-extract with urls: ['{url}'] and extract_depth: 'advanced'"
    }
}))
```

**GitHub URL Tip (claude-codex-settings)**
```python
# tavily_extract_to_advanced.py - Tips for GitHub URLs
if github_urls:
    print(json.dumps({
        "systemMessage": "Tip: For GitHub URLs, use gh CLI: `gh api repos/{owner}/{repo}/contents/{path}`...",
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "allow",
            "updatedInput": tool_input,
        },
    }))
```

**Quality Gate Error Context (claude-codex-settings)**
```python
# python_code_quality.py - Ruff error context
output = {
    'systemMessage': f'Ruff errors detected in {py_file.name}',
    'hookSpecificOutput': {
        'hookEventName': 'PostToolUse',
        'decision': 'block',
        'reason': error_msg
    },
}
```

#### Best Practices

1. **Keep it concise**: systemMessage content consumes context window tokens
2. **Be directive**: Use clear imperative language ("Use X instead of Y")
3. **Complement with permissionDecisionReason**: Pair invisible guidance with visible explanation
4. **Use for behavioral steering**: Ideal for workflow preferences, tool selection
5. **Avoid sensitive data**: Content may be included in future API calls

---

### 2.2 permissionDecisionReason

#### How It Guides Claude When Blocking

When a hook blocks an operation (via `permissionDecision: "deny"` or exit code 2), the `permissionDecisionReason` field provides Claude with an explanation of why the operation was blocked and what to do instead. This creates a feedback loop that teaches Claude your project's constraints.

#### Examples of Effective Reasons

**Safety Blocking (claude-code-safety-net)**
```python
# Comprehensive git protection with actionable guidance
output = {
    "hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": f"""BLOCKED by Safety Net

Reason: {reason}

Command: {_redact_secrets(segment)[:100]}...

What to do:
- Use 'git stash' first if you want to save changes
- Use -d instead of -D for safer branch deletion
- Ask the user for explicit permission if this is truly needed"""
    }
}
```

**TDD Enforcement (tdd-guard)**
```python
# AI-generated TDD violation explanation
return {
    'decision': 'block',
    'reason': '''Over-implementation violation detected.

You are implementing more than the minimum code needed to pass the current failing test.

Next steps:
1. Remove the extra implementation
2. Create only the empty class/function signature
3. Run tests to confirm they still fail for the right reason
4. Add implementation incrementally'''
}
```

**Lint Issues Notification (tdd-guard)**
```python
# Two-phase notification pattern
return {
    'decision': 'block',
    'reason': '''Code quality issues detected. Fix those first...

Lint issues detected:
/src/utils.ts
  10:5  error  Missing semicolon  semi
  15:1  warning  Unexpected console statement  no-console

X 2 problems (1 error, 1 warning)

Please fix these issues before proceeding.'''
}
```

**TRASH Pattern Guidance (claude-code-tools)**
```python
# Alternative workflow instruction
reason_text = (
    "Instead of using 'rm':\n "
    "- MOVE files using `mv` to the TRASH directory in the CURRENT folder (create it if needed), \n"
    "- Add an entry in a markdown file called 'TRASH-FILES.md' in the current directory, "
    "  where you show a one-liner with the file name, where it moved, and the reason to trash it"
)
return True, reason_text
```

#### Anti-Patterns

1. **Vague reasons**: "Operation not allowed" - provides no guidance
2. **Technical jargon only**: "Exit code 2 from validator" - not actionable
3. **Missing alternatives**: Blocking without suggesting what to do instead
4. **Overly long reasons**: Wall of text that obscures the key point
5. **No context**: "Blocked" without explaining what was blocked

---

### 2.3 updatedInput Modification

#### Silent Input Transformation

The `updatedInput` field allows hooks to modify tool inputs before execution without user awareness. This is powerful for enforcing consistency, upgrading parameters, or applying transformations.

#### Security Implications

- **Invisible changes**: Users don't see the transformation
- **Trust requirement**: Should only modify in well-understood ways
- **Audit trail**: Consider logging original vs modified inputs
- **Reversibility**: Changes should be predictable and documented

#### Use Cases

**Parameter Upgrading (claude-codex-settings)**
```python
# tavily_extract_to_advanced.py - Always use advanced extraction
tool_input = data["tool_input"]
tool_input["extract_depth"] = "advanced"  # Upgrade from default

print(json.dumps({
    "hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "allow",
        "updatedInput": tool_input,
    }
}))
```

**Potential Use Cases**:
- Normalizing file paths (relative to absolute)
- Adding default timeout values to commands
- Injecting required flags (e.g., always add `--verbose`)
- Sanitizing inputs (removing dangerous characters)
- Converting deprecated parameter names

#### Code Example Pattern
```python
def modify_tool_input(tool_name, tool_input):
    """Modify tool input before execution."""
    modified = tool_input.copy()

    if tool_name == "Bash":
        # Add timeout if not specified
        if "timeout" not in modified:
            modified["timeout"] = 30000

    elif tool_name == "Write":
        # Normalize file paths
        if "file_path" in modified:
            modified["file_path"] = os.path.abspath(modified["file_path"])

    return modified

# Output with updated input
print(json.dumps({
    "hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "allow",
        "updatedInput": modify_tool_input(tool_name, tool_input),
    }
}))
```

---

### 2.4 Transcript Reading

#### Reading Conversation History

The `transcript_path` field in hook payloads provides access to the full JSONL transcript of the current session. This enables context-aware decisions based on conversation history.

#### Privacy Considerations

- Transcripts contain full user prompts and Claude responses
- May include sensitive information shared during session
- Should redact secrets before logging (see claude-code-safety-net)
- Consider data retention policies

#### Pattern Examples

**Token Metrics Extraction (cc-tools-go)**
```go
// Parse transcript JSONL for token usage
func (s *Statusline) getTokenMetrics(transcriptPath string) TokenMetrics {
    content, err := s.deps.FileReader.ReadFile(transcriptPath)
    if err != nil { return TokenMetrics{} }

    lines := strings.Split(string(content), "\n")
    metrics := TokenMetrics{}

    for _, line := range lines {
        if line == "" { continue }
        var msg struct {
            Message struct {
                Usage struct {
                    InputTokens, OutputTokens int
                    CacheReadInputTokens      int
                } `json:"usage"`
            } `json:"message"`
            IsSidechain bool `json:"isSidechain"`
        }

        if json.Unmarshal([]byte(line), &msg) == nil && msg.Message.Usage.InputTokens > 0 {
            metrics.InputTokens += msg.Message.Usage.InputTokens
            metrics.OutputTokens += msg.Message.Usage.OutputTokens
        }
    }
    return metrics
}
```

**Conversation History Extraction (claude-hooks TypeScript)**
```typescript
// templates/hooks/lib.ts
export async function getConversationHistory(transcriptPath: string): Promise<Array<{role: 'user' | 'assistant'; content: string}>> {
    const fileStream = fs.createReadStream(transcriptPath)
    const rl = readline.createInterface({ input: fileStream, crlfDelay: Infinity })
    const history: Array<{role: 'user' | 'assistant'; content: string}> = []

    for await (const line of rl) {
        if (!line.trim()) continue
        const message = JSON.parse(line) as TranscriptMessage
        if (message.type === 'summary') continue

        if (message.type === 'user' && typeof message.message.content === 'string') {
            history.push({ role: 'user', content: message.message.content })
        }
        if (message.type === 'assistant') {
            const textContent = message.message.content
                .filter(c => c.type === 'text')
                .map(c => c.text)
                .join('\n')
            if (textContent) {
                history.push({ role: 'assistant', content: textContent })
            }
        }
    }
    return history
}

export async function getToolUsage(transcriptPath: string): Promise<Array<{tool: string; input: Record<string, unknown>; timestamp: string}>>
```

**Initial Message Extraction (claude-hooks TypeScript)**
```typescript
export async function getInitialMessage(transcriptPath: string): Promise<string | null> {
    const fileStream = fs.createReadStream(transcriptPath)
    const rl = readline.createInterface({ input: fileStream, crlfDelay: Infinity })

    for await (const line of rl) {
        if (!line.trim()) continue
        const message = JSON.parse(line) as TranscriptMessage
        if (message.type === 'summary') continue
        if (message.type === 'user' && message.message.role === 'user') {
            if (typeof message.message.content === 'string') {
                return message.message.content
            }
        }
    }
    return null
}
```

---

### 2.5 State Files

#### Persisting Context Between Invocations

Hooks execute as separate processes, so state must be persisted to files for cross-invocation communication. Common patterns include JSON files in `.claude/` directories or temp directories.

#### File Formats (JSON, YAML)

**JSON is dominant** due to:
- Native support in all languages
- Easy atomic read/write
- Human-readable for debugging

#### Session State Management

**Per-Session Files (tdd-guard)**
```typescript
// Storage interface for hook state
export const TRANSIENT_DATA = ['test', 'todo', 'modifications', 'lint'] as const

export interface Storage {
    saveTest(content: string): Promise<void>
    saveTodo(content: string): Promise<void>
    saveModifications(content: string): Promise<void>
    saveLint(content: string): Promise<void>
    saveConfig(content: string): Promise<void>
    getTest(): Promise<string | null>
    getTodo(): Promise<string | null>
    getModifications(): Promise<string | null>
    getLint(): Promise<string | null>
    getConfig(): Promise<string | null>
    clearTransientData(): Promise<void>  // Called on SessionStart
}

// File paths in .claude/tdd-guard/data/
// - test.json: Latest test results
// - todos.json: Claude's current todo list
// - modifications.json: File change history
// - lint.json: Lint results with notification flag
// - config.json: Guard enable/disable state
```

**Two-Phase Notification Pattern (tdd-guard)**
```typescript
// Using hasNotifiedAboutLintIssues flag
interface LintData {
    errorCount: number
    warningCount: number
    issues: Array<{file: string; line: number; message: string}>
    hasNotifiedAboutLintIssues: boolean  // State flag
}

// PreToolUse: First warning
if (hasIssues && !lintData.hasNotifiedAboutLintIssues) {
    await storage.saveLint(JSON.stringify({
        ...lintData,
        hasNotifiedAboutLintIssues: true  // Set flag
    }))
    return { decision: 'block', reason: 'Code quality issues detected...' }
}

// PostToolUse: Block on repeat
if (storedLintData?.hasNotifiedAboutLintIssues && hasIssues) {
    return createBlockResult(lintData)  // Now block hard
}
```

**Speed Bump Pattern (claude-code-tools)**
```python
# file_length_limit_hook.py - Flag file for one-time warning
flag_file = Path('.claude_file_length_warning.flag')

if flag_file.exists():
    flag_file.unlink()  # Clear flag, allow operation this time
    return False, None

# First attempt - block and create flag
flag_file.touch()
return True, f"File would be {resulting_lines} lines. Ask user to approve or refactor."
```

**Session Data Persistence (claude-hooks TypeScript)**
```typescript
// templates/hooks/session.ts
const SESSIONS_DIR = path.join(tmpdir(), 'claude-hooks-sessions')

export async function saveSessionData(hookType: string, payload: HookPayload): Promise<void> {
    await mkdir(SESSIONS_DIR, {recursive: true})
    const sessionFile = path.join(SESSIONS_DIR, `${payload.session_id}.json`)

    let sessionData: Array<{timestamp: string; hookType: string; payload: HookPayload}> = []
    try {
        const existing = await readFile(sessionFile, 'utf-8')
        sessionData = JSON.parse(existing)
    } catch {}

    sessionData.push({ timestamp: new Date().toISOString(), hookType, payload })
    await writeFile(sessionFile, JSON.stringify(sessionData, null, 2))
}
```

**Audit Logging (claude-code-safety-net)**
```python
def _write_audit_log(session_id, command, segment, reason, cwd) -> None:
    logs_dir = Path.home() / ".cc-safety-net" / "logs"
    safe_session_id = _sanitize_session_id_for_filename(session_id)

    logs_dir.mkdir(parents=True, exist_ok=True)
    log_file = logs_dir / f"{safe_session_id}.jsonl"

    entry = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "command": _redact_secrets(command)[:300],  # Truncate and redact
        "segment": _redact_secrets(segment)[:300],
        "reason": reason,
        "cwd": cwd,
    }

    with log_file.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")
```

---

### 2.6 CLAUDE.md Modification

#### Dynamic Project Context

While not a hook response field per se, hooks can modify CLAUDE.md files to inject persistent project context that Claude reads on every turn.

#### Runtime vs Static Injection

| Approach | When | Use Case |
|----------|------|----------|
| Static CLAUDE.md | Pre-session | Project rules, coding standards |
| Hook-injected | SessionStart | Dynamic context (git status, issues) |
| hookSpecificOutput.additionalContext | Per-event | Just-in-time context |

#### Examples

**SessionStart Context Injection (hooks-mastery)**
```python
# session_start.py - Development context loading
def load_development_context(source):
    """Load relevant development context based on session source."""
    context_parts = []

    context_parts.append(f"Session started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    context_parts.append(f"Session source: {source}")

    # Git status
    branch, changes = get_git_status()
    if branch:
        context_parts.append(f"Git branch: {branch}")
        if changes > 0:
            context_parts.append(f"Uncommitted changes: {changes} files")

    # Project files
    context_files = [
        ".claude/CONTEXT.md", ".claude/TODO.md",
        "TODO.md", ".github/ISSUE_TEMPLATE.md"
    ]

    for file_path in context_files:
        if Path(file_path).exists():
            with open(file_path, 'r') as f:
                content = f.read().strip()[:1000]  # Truncate
                context_parts.append(f"\n--- Content from {file_path} ---")
                context_parts.append(content)

    # GitHub issues
    issues = get_recent_issues()
    if issues:
        context_parts.append("\n--- Recent GitHub Issues ---")
        context_parts.append(issues)

    return "\n".join(context_parts)

# Return via hookSpecificOutput
output = {
    "hookSpecificOutput": {
        "hookEventName": "SessionStart",
        "additionalContext": load_development_context(source)
    }
}
```

**Default Instructions Initialization (tdd-guard)**
```typescript
// SessionStart: Ensure instructions file exists
private async ensureInstructionsExist(): Promise<void> {
    const existingInstructions = await this.storage.getInstructions()
    if (!existingInstructions) {
        await this.storage.saveInstructions(RULES)  // Write default TDD rules
    }
}

// The RULES content is later read during validation and included in AI prompt
```

---

## 3. Pattern Catalog

### 3.1 Context Injection Patterns

| Pattern Name | Mechanism | Source Repo | Context Loaded | When Useful |
|--------------|-----------|-------------|----------------|-------------|
| Development Context Injection | hookSpecificOutput.additionalContext | hooks-mastery | Git status, TODO files, GitHub issues | Session start for development workflows |
| Tool Redirection Guidance | systemMessage + permissionDecisionReason | claude-codex-settings | Directive to use alternative tool | Standardizing on preferred tools |
| Parameter Upgrade | updatedInput | claude-codex-settings | Modified tool_input (extract_depth) | Ensuring optimal tool configuration |
| TDD Violation Explanation | permissionDecisionReason | tdd-guard | AI-generated violation details + next steps | Enforcing development methodology |
| Safety Block with Alternatives | permissionDecisionReason | claude-code-safety-net | Redacted command + safe alternatives | Protecting against dangerous operations |
| Lint Issue Report | permissionDecisionReason | tdd-guard | Formatted lint output with file:line:message | Code quality enforcement |
| TRASH Pattern Guidance | permissionDecisionReason | claude-code-tools | Instructions for TRASH workflow | Teaching alternative deletion approach |

### 3.2 State Persistence Patterns

| Pattern Name | Mechanism | Source Repo | Context Loaded | When Useful |
|--------------|-----------|-------------|----------------|-------------|
| Two-Phase Notification | State file (hasNotifiedAboutLintIssues) | tdd-guard | Notification state flag | Warn first, block on repeat |
| Speed Bump | Flag file (.flag) | claude-code-tools | One-time warning acknowledgment | Allow override after warning |
| Session State Reset | clearTransientData() on SessionStart | tdd-guard | Cleared transient data | Clean slate for new sessions |
| Per-Session Audit Log | JSONL files per session_id | claude-code-safety-net | Blocked command history | Security auditing |
| Session Data Persistence | JSON files in temp directory | claude-hooks | All hook invocations | Debugging and analysis |

### 3.3 Transcript Reading Patterns

| Pattern Name | Mechanism | Source Repo | Context Loaded | When Useful |
|--------------|-----------|-------------|----------------|-------------|
| Token Metrics Extraction | transcript_path parsing | cc-tools-go | Input/output/cached tokens | Context window visualization |
| Conversation History | JSONL stream parsing | claude-hooks | User/assistant messages | Context-aware decisions |
| Initial Message | First user message extraction | claude-hooks | Opening prompt | Task classification |
| Tool Usage History | Tool call extraction | claude-hooks | Tool names and inputs | Usage pattern analysis |

### 3.4 Code Examples by Pattern

**Tool Redirection (claude-codex-settings)**
```python
# Intercept WebFetch, redirect to Tavily
print(json.dumps({
    "systemMessage": "WebFetch detected. AI is directed to use Tavily extract instead.",
    "hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": f"Please use mcp__tavily__tavily-extract with urls: ['{url}']"
    }
}))
```

**Development Context (hooks-mastery)**
```python
# Load git + project context at session start
context = load_development_context(source)
print(json.dumps({
    "hookSpecificOutput": {
        "hookEventName": "SessionStart",
        "additionalContext": context
    }
}))
```

**Safety Gate with Guidance (claude-code-safety-net)**
```python
# Block with actionable guidance
output = {
    "hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": f"BLOCKED by Safety Net\n\nReason: {reason}\n\nWhat to do:\n- Use 'git stash' first\n- Ask user for explicit permission"
    }
}
```

**Auto Context Files (claude-hooks TypeScript)**
```typescript
// Auto-add test files when prompt mentions "test"
const userPromptSubmit: UserPromptSubmitHandler = async (payload) => {
    const contextFiles: string[] = []

    if (payload.prompt.toLowerCase().includes('test')) {
        contextFiles.push('**/*.test.ts', '**/*.test.js')
    }

    return contextFiles.length > 0 ? {contextFiles} : {}
}
```

---

## 4. Recommendations

### Best Mechanisms for Each Use Case

| Use Case | Recommended Mechanism | Why |
|----------|----------------------|-----|
| Blocking dangerous operations | `permissionDecisionReason` | User sees explanation, Claude learns constraint |
| Tool preference enforcement | `systemMessage` + `deny` | Invisible directive + visible alternative |
| Parameter normalization | `updatedInput` | Silent, consistent transformations |
| Session initialization | `hookSpecificOutput.additionalContext` | One-time context load |
| Cross-hook state | State files in `.claude/` | Persistent, debuggable |
| Context-aware decisions | Transcript reading | Full conversation history |
| Code quality feedback | `permissionDecisionReason` with formatted output | Actionable guidance |

### Performance Considerations

| Mechanism | Overhead | Optimization Tips |
|-----------|----------|-------------------|
| systemMessage | Minimal | Keep under 500 chars |
| permissionDecisionReason | Minimal | Truncate long outputs |
| updatedInput | Minimal | Avoid deep copies |
| Transcript reading | 50-100ms | Stream parsing, early exit |
| State files | 10-50ms | Use JSON, not YAML |
| CLAUDE.md modification | N/A | Avoid per-hook modifications |

**High-Performance Pattern (cc-tools-go)**
```go
// Direct .git file reading instead of subprocess
func (s *Statusline) getGitInfo(dir string) GitInfo {
    // Walk up to find .git
    gitPath := filepath.Join(current, ".git")
    if s.deps.FileReader.Exists(gitPath) {
        // Read HEAD file directly - no subprocess
        headPath := filepath.Join(gitDir, "HEAD")
        if content, err := s.deps.FileReader.ReadFile(headPath); err == nil {
            head := strings.TrimSpace(string(content))
            if strings.HasPrefix(head, "ref: refs/heads/") {
                info.Branch = strings.TrimPrefix(head, "ref: refs/heads/")
            }
        }
    }
}
```

### Security Best Practices

1. **Secret Redaction in Logs**
```python
# claude-code-safety-net pattern
def _redact_secrets(text: str) -> str:
    redacted = text
    # KEY=VALUE patterns
    redacted = re.sub(
        r"\b([A-Z0-9_]*(?:TOKEN|SECRET|PASSWORD|KEY)[A-Z0-9_]*)=([^\s]+)",
        r"\1=<redacted>",
        redacted, flags=re.IGNORECASE
    )
    # Authorization headers
    redacted = re.sub(r"(?i)(authorization\s*:\s*)([^\s\"']+)", r"\1<redacted>", redacted)
    # GitHub tokens
    redacted = re.sub(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b", "<redacted>", redacted)
    return redacted
```

2. **Fail-Open vs Fail-Closed**
```python
# Default: Fail-open (allow on errors)
try:
    input_data = json.load(sys.stdin)
except json.JSONDecodeError:
    sys.exit(0)  # Allow through

# Strict mode: Fail-closed (block on errors)
if _env_truthy("SAFETY_NET_STRICT"):
    print(json.dumps({"permissionDecision": "deny", "reason": "Unable to parse safely"}))
```

3. **Validate Inputs with Schemas**
```typescript
// tdd-guard pattern with Zod
export const ToolOperationSchema = z.discriminatedUnion('tool_name', [
    EditOperationSchema,
    MultiEditOperationSchema,
    WriteOperationSchema,
    TodoWriteOperationSchema,
])

const operationResult = ToolOperationSchema.safeParse(hookData)
if (!operationResult.success) {
    return defaultResult  // Invalid input, allow through
}
```

4. **Graceful Error Handling**
```python
# hooks-mastery pattern - never crash the workflow
def main():
    try:
        input_data = json.load(sys.stdin)
        # ... processing logic ...
        sys.exit(0)
    except json.JSONDecodeError:
        sys.exit(0)  # Handle JSON errors gracefully
    except Exception:
        sys.exit(0)  # Handle any other errors
```

---

## Summary

Context loading in Claude Code hooks enables sophisticated steering of Claude's behavior. The six mechanisms provide a spectrum from invisible directives (`systemMessage`) to visible explanations (`permissionDecisionReason`) to silent transformations (`updatedInput`).

For most safety and quality enforcement, `permissionDecisionReason` provides the right balance of visibility and guidance. For tool preferences and behavioral steering, `systemMessage` offers invisible control. For state management across invocations, JSON state files in `.claude/` directories are the standard approach.

The key insight from analyzing these repositories is that the best hooks don't just block - they guide. By providing clear explanations, alternatives, and next steps in the context they inject, hooks become teaching tools that help Claude learn your project's constraints and preferences.
