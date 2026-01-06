# UserPromptSubmit Hook - Comprehensive Guide

## 1. Overview

### What This Hook Does

The `UserPromptSubmit` hook fires **before Claude processes a user's prompt**, allowing you to:
- Validate, filter, or block prompts before they reach Claude
- Modify or augment the prompt text
- Inject additional context files
- Add system-level context/instructions
- Implement runtime toggle commands
- Log user interactions for analytics/audit
- Route prompts to different workflows

### When It Fires (Trigger Conditions)

This hook fires **every time a user submits a prompt** to Claude Code, including:
- Initial prompts in a new session
- Follow-up prompts in an existing conversation
- Slash commands (e.g., `/commit`, `/review`)
- Special command triggers (e.g., `>resume`, `tdd-guard on`)

### Can It Block?

**Yes** - Exit code 2 blocks the prompt, or return JSON with `decision: "block"` and a `reason`.

When blocked:
- The prompt is **not** sent to Claude
- The `reason` is displayed to the user
- The session continues, allowing the user to submit a different prompt

### JSON Input Schema

```json
{
  "hook_event_name": "UserPromptSubmit",
  "session_id": "string",
  "transcript_path": "string",
  "prompt": "string"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `hook_event_name` | string | Always `"UserPromptSubmit"` |
| `session_id` | string | Unique identifier for the current session |
| `transcript_path` | string | Path to the JSONL transcript file |
| `prompt` | string | The user's submitted prompt text |

### JSON Output Schema

```json
{
  "decision": "approve" | "block" | undefined,
  "reason": "string (optional)",
  "contextFiles": ["string"],
  "updatedPrompt": "string (optional)",
  "hookSpecificOutput": {
    "hookEventName": "UserPromptSubmit",
    "additionalContext": "string (optional)"
  },
  "continue": true | false,
  "stopReason": "string (optional)",
  "suppressOutput": true | false
}
```

| Field | Type | Description |
|-------|------|-------------|
| `decision` | string | `"approve"` (allow), `"block"` (stop), or omit for default |
| `reason` | string | Explanation shown to user when blocking |
| `contextFiles` | string[] | Glob patterns for files to add to Claude's context |
| `updatedPrompt` | string | Modified version of the user's prompt |
| `hookSpecificOutput.additionalContext` | string | Extra context injected into the session |
| `continue` | boolean | If `false`, stops processing (legacy) |
| `stopReason` | string | Reason for stopping (used with `continue: false`) |
| `suppressOutput` | boolean | If `true`, suppresses hook output display |

---

## 2. Pattern Catalog

### Pattern: Prompt Logging

**Sources**: claude-code-hooks-mastery
**Description**: Logs all user prompts to a JSON file for debugging, analytics, and audit trails.
**Decision Type**: allow

**Implementation** (Python):
```python
def log_user_prompt(session_id, input_data):
    """Log user prompt to logs directory."""
    log_dir = Path("logs")
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / 'user_prompt_submit.json'

    if log_file.exists():
        with open(log_file, 'r') as f:
            try:
                log_data = json.load(f)
            except (json.JSONDecodeError, ValueError):
                log_data = []
    else:
        log_data = []

    log_data.append(input_data)

    with open(log_file, 'w') as f:
        json.dump(log_data, f, indent=2)
```

**Pros**:
- Creates audit trail for compliance and debugging
- Enables analytics on user interaction patterns
- Simple append-only pattern is reliable

**Cons**:
- Disk I/O on every prompt
- Log file grows unbounded without rotation
- Privacy considerations for sensitive prompts

**Use When**: Building analytics, debugging prompt handling, compliance auditing
**Avoid When**: High-frequency usage where logging overhead matters, privacy-sensitive environments

---

### Pattern: Dangerous Prompt Blocker

**Sources**: claude-hooks (TypeScript SDK)
**Description**: Blocks user prompts containing dangerous keywords like "delete all" before Claude processes them.
**Decision Type**: block

**Implementation** (TypeScript):
```typescript
const userPromptSubmit: UserPromptSubmitHandler = async (payload) => {
  await saveSessionData('UserPromptSubmit', {...payload, hook_type: 'UserPromptSubmit'} as const)
  console.log(`User prompt: ${payload.prompt}`)

  if (payload.prompt.includes('delete all')) {
    console.error('Dangerous prompt detected! Blocking.')
    return {decision: 'block', reason: 'Prompts containing "delete all" are not allowed'}
  }

  return {}
}
```

**Pros**:
- Prevents dangerous operations at the earliest possible point
- Simple pattern matching is fast and deterministic
- User sees clear explanation of why prompt was blocked

**Cons**:
- Simple keyword matching can have false positives
- Sophisticated users can bypass with rephrasing
- Requires maintaining a blocklist

**Use When**: Enforcing prompt-level safety policies, preventing known dangerous patterns
**Avoid When**: When all prompts should be allowed, when more sophisticated analysis is needed

---

### Pattern: Auto Context File Injection

**Sources**: claude-hooks (TypeScript SDK)
**Description**: Automatically adds relevant files to Claude's context based on prompt keywords (e.g., adds test files when "test" is mentioned).
**Decision Type**: allow

**Implementation** (TypeScript):
```typescript
const userPromptSubmit: UserPromptSubmitHandler = async (payload) => {
  const contextFiles: string[] = []

  if (payload.prompt.toLowerCase().includes('test')) {
    contextFiles.push('**/*.test.ts', '**/*.test.js')
    console.log('Auto-adding test files to context')
  }

  if (payload.prompt.toLowerCase().includes('config')) {
    contextFiles.push('**/config.*', '**/*.config.*')
  }

  if (payload.prompt.toLowerCase().includes('readme')) {
    contextFiles.push('**/README.md', '**/readme.md')
  }

  return contextFiles.length > 0 ? {contextFiles} : {}
}
```

**Pros**:
- Reduces manual context management burden
- Claude gets relevant files without user explicitly specifying
- Improves response quality by providing relevant context

**Cons**:
- May include irrelevant files
- Keyword matching is imprecise
- Can bloat context with too many files

**Use When**: Projects with predictable file structure, reducing user friction
**Avoid When**: When precise manual context control is preferred, large codebases where glob patterns would match too many files

---

### Pattern: User Command Toggle

**Sources**: tdd-guard
**Description**: Intercepts special user commands ("tdd-guard on", "tdd-guard off") to enable/disable features mid-session. Commands are consumed by the hook and do not reach Claude.
**Decision Type**: block (consumes command)

**Implementation** (TypeScript):
```typescript
export class UserPromptHandler {
  private readonly guardManager: GuardManager
  private readonly GUARD_COMMANDS = {
    ON: 'tdd-guard on',
    OFF: 'tdd-guard off'
  } as const

  async processUserCommand(hookData: string): Promise<ValidationResult | undefined> {
    const data = JSON.parse(hookData)

    if (data.hook_event_name !== 'UserPromptSubmit') {
      return undefined
    }

    const command = data.prompt?.toLowerCase()

    switch (command) {
      case this.GUARD_COMMANDS.ON:
        await this.guardManager.enable()
        return this.createBlockResult('TDD Guard enabled')

      case this.GUARD_COMMANDS.OFF:
        await this.guardManager.disable()
        return this.createBlockResult('TDD Guard disabled')

      default:
        return undefined
    }
  }

  private createBlockResult(message: string): ValidationResult {
    return {
      decision: undefined,
      reason: message,
      continue: false,
      stopReason: message
    }
  }
}
```

**Pros**:
- Enables runtime control without editing config
- Commands are processed silently without cluttering conversation
- State persists across hook invocations

**Cons**:
- Commands could conflict with normal user prompts
- Requires state management (file-based or in-memory)
- Users must know the command syntax

**Use When**: Features that users need to toggle frequently, temporary suspension of enforcement
**Avoid When**: Commands that are too generic and could match normal prompts, when toggle state should not persist

---

### Pattern: Session Prompt Tracking

**Sources**: claude-code-hooks-mastery
**Description**: Stores prompts per session in individual JSON files, enabling session history and status line display.
**Decision Type**: allow

**Implementation** (Python):
```python
def manage_session_data(session_id, prompt, name_agent=False):
    """Manage session data in the new JSON structure."""
    sessions_dir = Path(".claude/data/sessions")
    sessions_dir.mkdir(parents=True, exist_ok=True)

    session_file = sessions_dir / f"{session_id}.json"

    if session_file.exists():
        try:
            with open(session_file, 'r') as f:
                session_data = json.load(f)
        except (json.JSONDecodeError, ValueError):
            session_data = {"session_id": session_id, "prompts": []}
    else:
        session_data = {"session_id": session_id, "prompts": []}

    session_data["prompts"].append(prompt)

    with open(session_file, 'w') as f:
        json.dump(session_data, f, indent=2)
```

**Pros**:
- Per-session organization enables session-specific features
- Data can feed status line displays
- Easy to clean up old sessions

**Cons**:
- Creates many small files
- Requires periodic cleanup
- Session ID as filename may have character issues

**Use When**: Building session-aware features, status lines, conversation tracking
**Avoid When**: Simple single-session usage, storage-constrained environments

---

### Pattern: Prompt Validation Framework

**Sources**: claude-code-hooks-mastery
**Description**: Extensible framework for validating user prompts against blocked patterns before processing.
**Decision Type**: block

**Implementation** (Python):
```python
def validate_prompt(prompt):
    """
    Validate the user prompt for security or policy violations.
    Returns tuple (is_valid, reason).
    """
    blocked_patterns = [
        ('rm -rf /', 'Dangerous command detected'),
        ('drop table', 'SQL injection attempt detected'),
        ('delete all users', 'Dangerous operation detected'),
        # Add more patterns as needed
    ]

    prompt_lower = prompt.lower()

    for pattern, reason in blocked_patterns:
        if pattern.lower() in prompt_lower:
            return False, reason

    return True, None

# In main():
if args.validate and not args.log_only:
    is_valid, reason = validate_prompt(prompt)
    if not is_valid:
        # Exit code 2 blocks the prompt with error message
        print(f"Prompt blocked: {reason}", file=sys.stderr)
        sys.exit(2)
```

**Pros**:
- Extensible pattern list
- Clear separation of validation logic
- Exit code 2 provides standard blocking mechanism

**Cons**:
- Simple substring matching has limitations
- Requires ongoing pattern maintenance
- No semantic understanding of intent

**Use When**: Implementing content policies, input filtering, prompt injection detection
**Avoid When**: When all prompts should pass through, when sophisticated NLP is needed

---

### Pattern: Resume Trigger with Clipboard

**Sources**: claude-code-tools
**Description**: Detects ">resume"/">continue"/">handoff" prompts, copies session ID to clipboard, blocks prompt with instructions to run resume command.
**Decision Type**: block

**Implementation** (Python):
```python
TRIGGERS = (">resume", ">continue", ">handoff")

def copy_to_clipboard(text: str) -> bool:
    clipboard_commands = [
        ["pbcopy"],       # macOS
        ["xclip", "-selection", "clipboard"],  # Linux X11
        ["wl-copy"],      # Linux Wayland
        ["clip"],         # Windows
    ]
    for cmd in clipboard_commands:
        try:
            proc = subprocess.run(cmd, input=text.encode(), capture_output=True)
            if proc.returncode == 0:
                return True
        except (subprocess.SubprocessError, FileNotFoundError):
            continue
    return False

def main():
    data = json.load(sys.stdin)
    session_id = data.get("session_id", "")
    prompt = data.get("prompt", "").strip()

    if not any(prompt.startswith(t) for t in TRIGGERS):
        sys.exit(0)  # Not our trigger, pass through

    copied = copy_to_clipboard(session_id)

    message = "Session ID copied to clipboard!\n"
    message += "To continue: quit Claude, run: aichat resume <paste>"

    print(json.dumps({"decision": "block", "reason": message}))
```

**Pros**:
- Cross-platform clipboard support
- Enables seamless session handoff
- Clear user instructions in block message

**Cons**:
- Requires clipboard utilities installed
- Assumes specific workflow (aichat resume)
- Trigger words could conflict with normal prompts

**Use When**: Long sessions approaching context limits, multi-tool workflows
**Avoid When**: When different session management is preferred, environments without clipboard access

---

### Pattern: Terminal UI Beautifier

**Sources**: claude-code-hooks (EvanL1)
**Description**: Displays a beautified terminal header with timestamp, current path, and mode indicator when user submits a prompt.
**Decision Type**: allow

**Implementation** (Bash):
```bash
#!/bin/bash
# Terminal UI Hook - beautified terminal interface

echo -e "\033[3J\033[H\033[2J\033[1;36m"
echo "    =============================================="
echo -e "    |           Claude Code Terminal           |"
echo -e "    =============================================="
echo -e "    Time: $(date '+%A, %B %d, %Y at %I:%M %p')"
echo -e "    Path: $(pwd | sed "s|$HOME|~|")"
echo -e "    Mode: Interactive"

# Loading animation
for i in {1..3}; do
    echo -ne "\r    Initializing..."
    sleep 0.2
done
echo -ne "\r    Ready!                       "
```

**Pros**:
- Enhanced visual experience
- Provides session context awareness
- Simple bash implementation

**Cons**:
- Adds latency (>100ms with animation)
- May not work in all terminal emulators
- Purely cosmetic, no functional benefit

**Use When**: Enhanced visual experience, session context awareness
**Avoid When**: Scripted/automated sessions, minimal output environments, performance-sensitive workflows

---

### Pattern: LLM Agent Naming

**Sources**: claude-code-hooks-mastery
**Description**: Generates unique agent names using LLM (Ollama or Anthropic) on first prompt of a session.
**Decision Type**: allow

**Implementation** (Python):
```python
def manage_session_data(session_id, prompt, name_agent=False):
    sessions_dir = Path(".claude/data/sessions")
    sessions_dir.mkdir(parents=True, exist_ok=True)
    session_file = sessions_dir / f"{session_id}.json"

    if session_file.exists():
        with open(session_file, 'r') as f:
            session_data = json.load(f)
    else:
        session_data = {"session_id": session_id, "prompts": []}

    session_data["prompts"].append(prompt)

    # Generate agent name via LLM with fallback on first prompt
    if name_agent and "agent_name" not in session_data:
        try:
            # Try Ollama first (local, fast)
            result = subprocess.run(
                ["uv", "run", ".claude/hooks/utils/llm/ollama.py", "--agent-name"],
                capture_output=True, text=True, timeout=5
            )
            if result.returncode == 0 and result.stdout.strip():
                agent_name = result.stdout.strip()
                if len(agent_name.split()) == 1 and agent_name.isalnum():
                    session_data["agent_name"] = agent_name
                else:
                    raise Exception("Invalid name from Ollama")
        except Exception:
            # Fall back to Anthropic if Ollama fails
            result = subprocess.run(
                ["uv", "run", ".claude/hooks/utils/llm/anth.py", "--agent-name"],
                capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0:
                session_data["agent_name"] = result.stdout.strip()

    with open(session_file, 'w') as f:
        json.dump(session_data, f, indent=2)
```

**Pros**:
- Creates memorable, unique session identifiers
- Multi-provider fallback for reliability
- Persists across session

**Cons**:
- Adds 5-10 seconds latency on first prompt
- Requires LLM API access
- May fail if no LLM available

**Use When**: Running multiple agent sessions, need unique identifiers for tracking/display
**Avoid When**: Latency is critical, LLM APIs unavailable

---

### Pattern: Guard State Early Exit

**Sources**: tdd-guard
**Description**: Checks if a feature guard is disabled and returns early with no-op result, bypassing all validation logic.
**Decision Type**: allow

**Implementation** (TypeScript):
```typescript
async getDisabledResult(): Promise<ValidationResult | undefined> {
  const isEnabled = await this.guardManager.isEnabled()
  if (!isEnabled) {
    return { decision: undefined, reason: '' }
  }
  return undefined
}

// Called from processHookData.ts:
const disabledResult = await userPromptHandler.getDisabledResult()
if (disabledResult) {
  return disabledResult
}
```

**Pros**:
- Efficient early exit when disabled
- Pairs with toggle pattern for runtime control
- Minimal overhead when disabled

**Cons**:
- Requires state management
- State checking adds latency when enabled
- Could be bypassed by other hooks

**Use When**: Paired with user-command-toggle pattern, features that need on/off control
**Avoid When**: Critical safety hooks that should never be disabled

---

### Pattern: TDD Context Injection

**Sources**: tdd-guard, context-loading.yaml
**Description**: Injects TDD guidance and test results as system context before Claude processes user requests, enabling Claude to be aware of test status.
**Decision Type**: allow (with context)

**Implementation** (TypeScript):
```typescript
export async function handleUserPrompt(
  context: ValidationContext
): Promise<HookResult> {
  const testState = await loadTestState();
  const systemMessage = buildTDDGuidance(testState);
  return {
    systemMessage,
    hookSpecificOutput: { hookEventName: 'UserPromptSubmit' }
  };
}

function buildTDDGuidance(testState: TestState): string {
  let guidance = "TDD Mode Active:\n";

  if (testState.failingTests.length > 0) {
    guidance += `- ${testState.failingTests.length} tests failing\n`;
    guidance += "- Focus on fixing tests before adding features\n";
  }

  if (testState.untestedFiles.length > 0) {
    guidance += `- ${testState.untestedFiles.length} files need tests\n`;
  }

  return guidance;
}
```

**Pros**:
- Provides Claude with workflow context
- Enables Claude to adapt behavior based on test state
- Non-blocking - guidance only

**Cons**:
- Requires state management for test results
- Adds tokens to each prompt
- Guidance may not always be relevant

**Use When**: Enforcing TDD workflow, providing Claude with development context
**Avoid When**: Simple one-off tasks, non-TDD workflows

---

### Pattern: Typed Hook Handler (TypeScript SDK)

**Sources**: claude-hooks (johnlindquist)
**Description**: Type-safe UserPromptSubmit handler with full TypeScript typing for payload and response.
**Decision Type**: varies

**Implementation** (TypeScript):
```typescript
// Type definitions
export interface UserPromptSubmitPayload {
  session_id: string
  transcript_path: string
  hook_event_name: 'UserPromptSubmit'
  prompt: string
}

export interface UserPromptSubmitResponse {
  decision?: 'approve' | 'block'
  reason?: string
  contextFiles?: string[]
  updatedPrompt?: string
  hookSpecificOutput?: {
    hookEventName: 'UserPromptSubmit'
    additionalContext?: string
  }
  continue?: boolean
  stopReason?: string
  suppressOutput?: boolean
}

export type UserPromptSubmitHandler = (
  payload: UserPromptSubmitPayload
) => Promise<UserPromptSubmitResponse>

// Handler registration
runHook({
  userPromptSubmit: async (payload) => {
    // Full type inference here
    console.log(`User prompt: ${payload.prompt}`)

    if (payload.prompt.includes('delete all')) {
      return {decision: 'block', reason: 'Dangerous prompt'}
    }

    return {}
  }
})
```

**Pros**:
- Full type safety and autocomplete
- Compile-time error catching
- Self-documenting code

**Cons**:
- Requires TypeScript setup
- More verbose than simple scripts
- Runtime overhead of type checking

**Use When**: TypeScript projects, complex hook logic
**Avoid When**: Simple one-off scripts, non-TypeScript environments

---

## 3. Inspiration Ideas

Based on the patterns found, here are additional use cases for UserPromptSubmit:

### Input Filtering and Safety

1. **Prompt Injection Detection**: Scan prompts for injection patterns that attempt to override instructions.

2. **PII Detection**: Block or redact prompts containing personal information (emails, phone numbers, SSNs).

3. **Rate Limiting**: Track prompt frequency and block/throttle excessive requests.

4. **Language Filtering**: Block prompts in unsupported languages or profanity.

5. **Complexity Gating**: Reject overly complex prompts that would consume too many tokens.

### Prompt Enhancement

1. **Prompt Templating**: Detect shorthand prompts (e.g., "fix lint") and expand them into detailed instructions with best practices.

2. **Language Detection and Translation**: Detect prompt language and add translation context.

3. **Intent Classification**: Use a small/fast model to classify prompt intent (debug, feature, refactor) and add appropriate context.

4. **Prompt Quality Scoring**: Score prompt clarity/specificity and suggest improvements before processing.

5. **Smart Expansion**: Expand abbreviations and shorthand based on project conventions.

### Context Management

1. **Project Context Auto-Load**: On first prompt, automatically inject CLAUDE.md, project structure, and recent git history.

2. **Smart File Injection**: Analyze prompt semantics to inject relevant files beyond simple keyword matching.

3. **Session Resume Context**: On session resume, automatically inject summary of previous session's work.

4. **RAG Integration**: Query a vector database based on prompt and inject relevant documentation snippets.

5. **Dependency Tracking**: When prompt mentions a file, auto-inject its imports/dependencies.

### Routing and Workflow

1. **Multi-Model Routing**: Route prompts to different models based on complexity or domain.

2. **Prompt Caching**: Hash prompts and return cached responses for identical requests.

3. **A/B Testing**: Route a percentage of prompts through experimental prompt modifications.

4. **Workflow Branching**: Route "debug" prompts through different processing than "feature" prompts.

5. **Team Policy Enforcement**: Block prompts requesting changes to protected files/branches based on user role.

### Analytics and Observability

1. **Cost Estimation**: Estimate token usage based on prompt + auto-loaded context, warn user if high.

2. **Prompt History Deduplication**: Detect if user is re-asking a recent question and suggest looking at previous response.

3. **Telemetry Pipeline**: Stream prompt metadata to analytics service for usage insights.

4. **Session Health Monitoring**: Track prompt patterns that indicate confusion or frustration.

### Combinations with Other Hooks

1. **UserPromptSubmit + SessionStart**: SessionStart loads project context, UserPromptSubmit adds task-specific context based on prompt keywords.

2. **UserPromptSubmit + PreToolUse**: UserPromptSubmit sets session-level flags, PreToolUse checks those flags for conditional tool blocking.

3. **UserPromptSubmit + Stop**: UserPromptSubmit tracks task start time, Stop calculates and logs task duration.

4. **UserPromptSubmit + Notification**: UserPromptSubmit triggers desktop notification for long prompts, Notification triggers when Claude needs input.

5. **UserPromptSubmit + PreCompact**: UserPromptSubmit logs critical context, PreCompact preserves it before compaction.

### Patterns from Other Domains

1. **API Gateway Pattern**: UserPromptSubmit as a gateway for rate limiting, authentication, and request transformation.

2. **Middleware Chain**: Multiple UserPromptSubmit hooks running in sequence, each adding or modifying context.

3. **Circuit Breaker**: Track prompt failure patterns and block potentially problematic prompts.

4. **Feature Flags**: Use prompt content to check feature flags and enable/disable capabilities.

---

## 4. Implementation Recommendations

### Best Patterns to Adopt (Ranked)

| Rank | Pattern | Value | Complexity | Performance |
|------|---------|-------|------------|-------------|
| 1 | **Prompt Logging** | Essential for debugging | Low | <10ms |
| 2 | **Auto Context File Injection** | High productivity boost | Low | <10ms |
| 3 | **Dangerous Prompt Blocker** | Basic safety layer | Low | <10ms |
| 4 | **User Command Toggle** | Runtime control | Medium | <10ms |
| 5 | **Prompt Validation Framework** | Extensible policies | Low | <10ms |
| 6 | **Session Prompt Tracking** | Session features | Low | <10ms |
| 7 | **TDD Context Injection** | Workflow awareness | Medium | 10-50ms |

### Patterns to Avoid or Use Carefully

| Pattern | Concern | When OK |
|---------|---------|---------|
| **Terminal UI Beautifier** | Adds latency, no functional benefit | Demo/presentation only |
| **LLM Agent Naming** | 5-10s latency | Session tracking is critical |
| **Heavy prompt processing** | Blocks user experience | Can be made async |

### Performance Budget

| Latency Target | Suitable Patterns |
|----------------|-------------------|
| **<10ms** | Prompt logging, keyword blocking, context file injection, toggle commands |
| **10-50ms** | Session tracking, state file operations, simple file reads |
| **50-100ms** | Git operations, subprocess calls |
| **>100ms** | LLM calls, network requests - avoid unless necessary |

**Performance Best Practices**:
- Keep hook execution under 50ms for responsive UX
- Use exit code 0 for non-blocking operations
- Avoid synchronous network calls
- Cache expensive computations (file reads, API calls)
- Use parallel I/O when reading multiple files

### Exit Code Reference

| Exit Code | Meaning | Use Case |
|-----------|---------|----------|
| **0** | Success, allow prompt | Logging, context injection, passthrough |
| **1** | Error (allow prompt) | Hook failure, graceful degradation |
| **2** | Block prompt | Policy violation, dangerous content |

### Context Loading Mechanisms

| Mechanism | Field | Description |
|-----------|-------|-------------|
| **Block with reason** | `decision: "block", reason: "..."` | Show message, prevent prompt |
| **Context files** | `contextFiles: ["*.ts"]` | Add files to Claude's context |
| **Modified prompt** | `updatedPrompt: "..."` | Replace user's prompt text |
| **Additional context** | `hookSpecificOutput.additionalContext` | Inject system context |
| **System message** | `systemMessage: "..."` | Top-level instructions for Claude |

### Testing Approach

1. **Unit Tests**: Test pattern matching and decision logic in isolation
```python
def test_dangerous_prompt_detection():
    assert validate_prompt("delete all files")[0] == False
    assert validate_prompt("help me debug")[0] == True
```

2. **Integration Tests**: Test JSON input/output contract
```python
def test_hook_json_output():
    result = run_hook('{"prompt": "delete all", "session_id": "test"}')
    output = json.loads(result)
    assert output["decision"] == "block"
    assert "reason" in output
```

3. **End-to-End Tests**: Test with Claude Code CLI
```bash
echo '{"hook_event_name":"UserPromptSubmit","prompt":"test"}' | python hook.py
```

4. **Regression Tests**: Maintain a corpus of prompts and expected decisions
```yaml
prompts:
  - input: "delete all"
    expected_decision: "block"
  - input: "help me write tests"
    expected_decision: null
```

### Configuration Template

**Minimal Setup** (Python):
```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "python .claude/hooks/user_prompt_submit.py"
          }
        ]
      }
    ]
  }
}
```

**TypeScript Setup** (Bun):
```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "bun .claude/hooks/index.ts UserPromptSubmit"
          }
        ]
      }
    ]
  }
}
```

**Note**: Empty `matcher` matches all prompts. Use regex patterns to match specific prompt formats if needed.

### Starter Template (Python)

```python
#!/usr/bin/env python3
"""UserPromptSubmit hook - template for common patterns."""
import json
import sys
from pathlib import Path

def main():
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)  # Graceful failure

    prompt = input_data.get("prompt", "")
    session_id = input_data.get("session_id", "")

    # Pattern 1: Logging
    log_prompt(session_id, prompt)

    # Pattern 2: Validation
    is_valid, reason = validate_prompt(prompt)
    if not is_valid:
        print(json.dumps({"decision": "block", "reason": reason}))
        sys.exit(0)

    # Pattern 3: Context injection
    context_files = get_context_files(prompt)
    if context_files:
        print(json.dumps({"contextFiles": context_files}))
        sys.exit(0)

    # Default: allow
    sys.exit(0)

def log_prompt(session_id, prompt):
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / "prompts.jsonl"
    with open(log_file, "a") as f:
        f.write(json.dumps({"session_id": session_id, "prompt": prompt}) + "\n")

def validate_prompt(prompt):
    blocked = [("delete all", "Destructive operation not allowed")]
    for pattern, reason in blocked:
        if pattern.lower() in prompt.lower():
            return False, reason
    return True, None

def get_context_files(prompt):
    files = []
    if "test" in prompt.lower():
        files.extend(["**/*.test.*", "**/*_test.*"])
    return files

if __name__ == "__main__":
    main()
```

---

## Summary

The UserPromptSubmit hook is Claude Code's input gateway, enabling:

| Capability | Mechanism |
|------------|-----------|
| **Block dangerous prompts** | `decision: "block"` or exit code 2 |
| **Log interactions** | Write to log files |
| **Inject context files** | `contextFiles: [...]` |
| **Modify prompts** | `updatedPrompt: "..."` |
| **Add system context** | `systemMessage: "..."` or `hookSpecificOutput.additionalContext` |
| **Runtime toggles** | State file + command detection |

Key patterns discovered across repositories:
- **claude-code-hooks-mastery**: Logging, session tracking, LLM naming
- **claude-hooks (TypeScript)**: Type-safe handlers, dangerous prompt blocking, auto context injection
- **claude-code-tools**: Resume triggers, clipboard integration
- **tdd-guard**: Toggle commands, TDD context injection, guard state management
- **EvanL1/claude-code-hooks**: Terminal UI beautification

The most valuable patterns are those that are **fast** (<10ms), **non-blocking**, and **enhance context** without requiring user action.
