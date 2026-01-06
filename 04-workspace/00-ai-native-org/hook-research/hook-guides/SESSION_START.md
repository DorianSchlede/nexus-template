# SessionStart Hook Guide

A comprehensive guide to implementing SessionStart hooks for Claude Code, synthesized from patterns across multiple repositories.

---

## 1. Overview

### What This Hook Does

The **SessionStart** hook fires when a new Claude Code session begins. It provides an opportunity to:
- Initialize session state
- Load project context
- Clear transient data
- Log session events for auditing
- Announce session start via audio/notifications

### When It Fires (Trigger Conditions)

SessionStart fires in three scenarios, indicated by the `source` field in the payload:

| Source | Description |
|--------|-------------|
| `startup` | Fresh session start (new conversation) |
| `resume` | Resuming a previous session |
| `clear` | Session cleared and restarted |

**Matcher Pattern:** `startup|resume|clear` (or empty for all)

### Can It Block?

**No.** SessionStart is an informational hook only. It cannot block or prevent session initialization. All decisions (approve/block) are ignored. The hook is purely for setup, context injection, and side effects.

### JSON Input Schema

```json
{
  "hook_event_name": "SessionStart",
  "session_id": "string (UUID)",
  "transcript_path": "string (path to JSONL transcript)",
  "source": "startup" | "resume" | "clear"
}
```

### JSON Output Schema

```json
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "string (optional - injected into system context)"
  }
}
```

**Note:** Returning an empty object `{}` is valid and signals no action needed.

---

## 2. Pattern Catalog

### Pattern: Session State Reset

**Sources:** tdd-guard, claude-code-hooks-mastery

**Description:** Clears transient session data (test results, todos, modifications, lint data) on session start while preserving persistent configuration. Ensures each session begins with a clean slate.

**Decision Type:** none (SessionStart cannot block)

**Implementation (TypeScript):**
```typescript
export class SessionHandler {
  private readonly storage: Storage

  constructor(storage?: Storage) {
    this.storage = storage ?? new FileStorage()
  }

  async processSessionStart(hookData: string): Promise<void> {
    const parsedData = JSON.parse(hookData)
    const sessionStartResult = SessionStartSchema.safeParse(parsedData)

    if (!sessionStartResult.success) {
      return
    }

    await this.ensureInstructionsExist()
    await this.storage.clearTransientData()
  }

  private async ensureInstructionsExist(): Promise<void> {
    const existingInstructions = await this.storage.getInstructions()
    if (!existingInstructions) {
      await this.storage.saveInstructions(RULES)
    }
  }
}
```

**Pros:**
- Prevents state pollution between sessions
- Maintains consistent starting conditions
- Distinguishes transient vs persistent data

**Cons:**
- May lose useful state in resumed sessions
- Requires careful categorization of what to clear

**Use When:** Hook maintains state across tool calls that should be reset between sessions.

**Avoid When:** State needs to persist across sessions (e.g., user preferences, learned patterns).

---

### Pattern: Session Event Logging

**Sources:** claude-code-hooks-mastery, hooks-mastery-session, hooks-mastery-part1

**Description:** Logs all session start events to a JSON file with full input data for audit trail and debugging.

**Decision Type:** none

**Implementation (Python):**
```python
def log_session_start(input_data):
    """Log session start event to logs directory."""
    log_dir = Path("logs")
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / 'session_start.json'

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

**Pros:**
- Creates audit trail of all sessions
- Enables debugging of session issues
- Tracks session frequency and patterns

**Cons:**
- Log file grows without bounds
- Adds I/O overhead on every session start

**Use When:** You need to track session history, debug session behavior, or audit session events.

**Avoid When:** Logging overhead is a concern or disk space is limited.

---

### Pattern: Development Context Injection

**Sources:** claude-code-hooks-mastery, hooks-mastery-session, hooks-mastery-part1

**Description:** Loads git status, project context files (TODO.md, CONTEXT.md), and GitHub issues at session start to provide Claude with relevant development context.

**Decision Type:** none

**Implementation (Python):**
```python
def load_development_context(source):
    """Load relevant development context based on session source."""
    context_parts = []

    context_parts.append(f"Session started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    context_parts.append(f"Session source: {source}")

    branch, changes = get_git_status()
    if branch:
        context_parts.append(f"Git branch: {branch}")
        if changes > 0:
            context_parts.append(f"Uncommitted changes: {changes} files")

    context_files = [
        ".claude/CONTEXT.md",
        ".claude/TODO.md",
        "TODO.md",
        ".github/ISSUE_TEMPLATE.md"
    ]

    for file_path in context_files:
        if Path(file_path).exists():
            with open(file_path, 'r') as f:
                content = f.read().strip()
                if content:
                    context_parts.append(f"\n--- Content from {file_path} ---")
                    context_parts.append(content[:1000])  # Limit size

    issues = get_recent_issues()
    if issues:
        context_parts.append("\n--- Recent GitHub Issues ---")
        context_parts.append(issues)

    return "\n".join(context_parts)

# Output via hookSpecificOutput.additionalContext
output = {
    "hookSpecificOutput": {
        "hookEventName": "SessionStart",
        "additionalContext": load_development_context(source)
    }
}
print(json.dumps(output))
```

**Pros:**
- Claude starts with project awareness
- Reduces manual context sharing
- Integrates with existing project workflows

**Cons:**
- Adds latency on session start
- May load irrelevant context
- Depends on external tools (git, gh)

**Use When:** Claude needs project awareness at session start; for development workflows with git and GitHub.

**Avoid When:** For simple one-off tasks where project context is irrelevant.

---

### Pattern: Git Status Check

**Sources:** claude-code-hooks-mastery, hooks-mastery-session, hooks-mastery-part1

**Description:** Retrieves current git branch and count of uncommitted changes at session start for development awareness.

**Decision Type:** none

**Implementation (Python):**
```python
def get_git_status():
    """Get current git status information."""
    try:
        branch_result = subprocess.run(
            ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
            capture_output=True,
            text=True,
            timeout=5
        )
        current_branch = branch_result.stdout.strip() if branch_result.returncode == 0 else "unknown"

        status_result = subprocess.run(
            ['git', 'status', '--porcelain'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if status_result.returncode == 0:
            changes = status_result.stdout.strip().split('\n') if status_result.stdout.strip() else []
            uncommitted_count = len(changes)
        else:
            uncommitted_count = 0

        return current_branch, uncommitted_count
    except Exception:
        return None, None
```

**Pros:**
- Fast execution (<50ms)
- Provides essential version control context
- Works in any git repository

**Cons:**
- Fails silently in non-git directories
- Subprocess overhead

**Use When:** When Claude needs git repository awareness; for development workflows.

**Avoid When:** For non-git projects or when git info is irrelevant.

---

### Pattern: GitHub Issues Fetch

**Sources:** claude-code-hooks-mastery, hooks-mastery-session, hooks-mastery-part1

**Description:** Fetches recent open GitHub issues using gh CLI to provide task context at session start.

**Decision Type:** none

**Implementation (Python):**
```python
def get_recent_issues():
    """Get recent GitHub issues if gh CLI is available."""
    try:
        gh_check = subprocess.run(['which', 'gh'], capture_output=True)
        if gh_check.returncode != 0:
            return None

        result = subprocess.run(
            ['gh', 'issue', 'list', '--limit', '5', '--state', 'open'],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    except Exception:
        pass
    return None
```

**Pros:**
- Surfaces relevant GitHub issues for context
- Integrates with issue-driven development
- Falls back gracefully when gh unavailable

**Cons:**
- Requires gh CLI installation and authentication
- Adds network latency (50-100ms)
- May fetch irrelevant issues

**Use When:** When Claude should be aware of open issues/tasks; for issue-driven development.

**Avoid When:** For non-GitHub projects; when issue list is very large or irrelevant.

---

### Pattern: Session Source Detection

**Sources:** claude-hooks (TypeScript SDK)

**Description:** Detects the source of a new Claude session (startup, resume, clear, or client type like VSCode/web) and applies source-specific initialization logic.

**Decision Type:** none

**Implementation (TypeScript):**
```typescript
const sessionStart: SessionStartHandler = async (payload) => {
  await saveSessionData('SessionStart', {...payload, hook_type: 'SessionStart'} as const)

  console.log(`New session started from: ${payload.source}`)
  console.log(`Session ID: ${payload.session_id}`)

  if (payload.source === 'vscode') {
    console.log('VS Code session detected - enabling IDE-specific features')
  } else if (payload.source === 'web') {
    console.log('Web session detected')
  } else if (payload.source === 'startup') {
    console.log('Fresh startup - initializing from scratch')
  } else if (payload.source === 'resume') {
    console.log('Resuming previous session')
  }

  return {} // Empty object means continue normally
}
```

**Pros:**
- Enables different behavior based on session type
- Supports IDE-specific optimizations
- Simple pattern matching

**Cons:**
- Limited to known source values
- May need updates as new sources are added

**Use When:** You need different behavior based on where Claude is running or session type.

**Avoid When:** Session source is irrelevant to your use case.

---

### Pattern: TTS Session Announcement

**Sources:** claude-code-hooks-mastery, hooks-mastery-session, hooks-mastery-part1

**Description:** Announces session start via text-to-speech with different messages for startup, resume, and clear session types.

**Decision Type:** none

**Implementation (Python):**
```python
if args.announce:
    try:
        script_dir = Path(__file__).parent
        tts_script = script_dir / "utils" / "tts" / "pyttsx3_tts.py"

        if tts_script.exists():
            messages = {
                "startup": "Claude Code session started",
                "resume": "Resuming previous session",
                "clear": "Starting fresh session"
            }
            message = messages.get(source, "Session started")

            subprocess.run(
                ["uv", "run", str(tts_script), message],
                capture_output=True,
                timeout=5
            )
    except Exception:
        pass  # Fail silently
```

**Pros:**
- Provides audio feedback for session lifecycle
- Useful for accessibility
- Context-aware messaging

**Cons:**
- Adds 50-100ms latency
- Requires audio output capability
- May be disruptive in shared environments

**Use When:** When you want audio feedback for session lifecycle events; accessibility scenarios; hands-free operation.

**Avoid When:** In shared/quiet environments; when low latency is critical.

---

### Pattern: Default Instructions Initialization

**Sources:** tdd-guard

**Description:** Ensures rule/instruction files exist on session start. If no custom instructions file exists, creates one with default rules. Preserves existing custom instructions if already present.

**Decision Type:** none

**Implementation (TypeScript):**
```typescript
private async ensureInstructionsExist(): Promise<void> {
  const existingInstructions = await this.storage.getInstructions()
  if (!existingInstructions) {
    await this.storage.saveInstructions(RULES)
  }
}

// From rules.ts - the default RULES content:
export const RULES = `## TDD Fundamentals

### The TDD Cycle
The foundation of TDD is the Red-Green-Refactor cycle:

1. **Red Phase**: Write ONE failing test that describes desired behavior
2. **Green Phase**: Write MINIMAL code to make the test pass
3. **Refactor Phase**: Improve code structure while keeping tests green
...`
```

**Pros:**
- Users get working behavior immediately
- Customizable via file editing
- Idempotent (safe to run multiple times)

**Cons:**
- File creation could conflict with project structure
- Users may not know to customize

**Use When:** Hook requires configuration or instruction files that should have sensible defaults.

**Avoid When:** Defaults would be harmful or confusing; file creation could conflict with project.

---

### Pattern: Session Data Persistence

**Sources:** claude-hooks (TypeScript SDK)

**Description:** Appends hook invocations to session-specific JSON files in temp directory for debugging and analysis.

**Decision Type:** none

**Implementation (TypeScript):**
```typescript
const SESSIONS_DIR = path.join(tmpdir(), 'claude-hooks-sessions')

export async function saveSessionData(hookType: string, payload: HookPayload): Promise<void> {
  try {
    await mkdir(SESSIONS_DIR, {recursive: true})
    const sessionFile = path.join(SESSIONS_DIR, `${payload.session_id}.json`)

    let sessionData: Array<{timestamp: string; hookType: string; payload: HookPayload}> = []
    try {
      const existing = await readFile(sessionFile, 'utf-8')
      sessionData = JSON.parse(existing)
    } catch {}

    sessionData.push({
      timestamp: new Date().toISOString(),
      hookType,
      payload
    })
    await writeFile(sessionFile, JSON.stringify(sessionData, null, 2))
  } catch (error) {
    console.error('Failed to save session data:', error)
  }
}
```

**Pros:**
- Complete hook invocation history per session
- Useful for debugging hook behavior
- Grouped by session ID

**Cons:**
- Adds disk I/O overhead
- Temp files may not persist across reboots
- Can grow large for long sessions

**Use When:** Debugging hook behavior or analyzing session patterns.

**Avoid When:** In production where disk I/O overhead is a concern.

---

### Pattern: Dynamic Skill Selection

**Sources:** awesome-claude-code (claude-infrastructure-showcase)

**Description:** Uses SessionStart hooks to intelligently select and activate appropriate Skills based on the current project context, enabling context-aware skill loading.

**Decision Type:** none

**Implementation Concept:**
```python
def select_skills_for_context():
    """Select appropriate skills based on project context."""
    skills = []

    # Check for project indicators
    if Path("package.json").exists():
        skills.extend(["npm-helper", "node-debugger"])

    if Path("Cargo.toml").exists():
        skills.extend(["rust-analyzer", "cargo-helper"])

    if Path("pyproject.toml").exists() or Path("requirements.txt").exists():
        skills.extend(["python-linter", "uv-helper"])

    if Path(".github").is_dir():
        skills.append("github-actions-helper")

    return skills

# Inject skill context
output = {
    "hookSpecificOutput": {
        "hookEventName": "SessionStart",
        "additionalContext": f"Available skills for this project: {', '.join(select_skills_for_context())}"
    }
}
```

**Pros:**
- Adapts Claude's capabilities to project type
- Reduces manual skill activation
- Enables project-aware workflows

**Cons:**
- Requires well-defined skill catalog
- May activate unnecessary skills
- Complex to maintain

**Use When:** Projects with multiple specialized skills that benefit from automatic selection.

**Avoid When:** Simple single-purpose projects; when manual control is preferred.

---

## 3. Inspiration Ideas

### Novel Use Cases Based on Found Patterns

1. **Project Health Dashboard**
   - Combine git status, test coverage, lint warnings into a "health score"
   - Inject summary into Claude's context on startup
   - Suggest priorities based on health metrics

2. **Session Continuity Manager**
   - On `resume`, read transcript and summarize previous session
   - Inject summary as context for continuity
   - Track session chains across days

3. **Environment Validator**
   - Check for required tools (node, python, docker) on startup
   - Warn if environment is incomplete
   - Suggest setup commands

4. **Time-Aware Context**
   - Inject day-of-week, time, and calendar context
   - Different behavior for morning vs evening sessions
   - Meeting-aware mode (reduced interruptions)

5. **Team Context Loader**
   - Load team member assignments from CODEOWNERS
   - Inject relevant PR/review context
   - Show who's available for help

6. **Security Posture Check**
   - Scan for exposed secrets in recent commits
   - Check dependency vulnerability status
   - Inject security warnings into context

### Combinations with Other Hooks

| SessionStart + | Pattern |
|---------------|---------|
| PreToolUse | Load rules at session start, enforce in PreToolUse |
| Stop | Log session duration by tracking start/stop times |
| PreCompact | Backup important context before compaction |
| Notification | Announce both session start and end |
| UserPromptSubmit | Initialize prompt filtering rules |

### Advanced Applications

1. **Multi-Agent Coordination**
   - Register session with central coordinator
   - Receive assigned tasks on startup
   - Enable cross-agent communication

2. **Learning/Personalization**
   - Load user preferences from persistent store
   - Track session patterns for optimization
   - Suggest based on historical behavior

3. **Compliance/Audit Mode**
   - Initialize comprehensive logging
   - Record session metadata for compliance
   - Enable enhanced security checks

---

## 4. Implementation Recommendations

### Best Patterns to Adopt (Ranked)

1. **Session Event Logging** - Essential for debugging, minimal overhead
2. **Development Context Injection** - High value for dev workflows
3. **Session State Reset** - Critical for stateful hooks
4. **Git Status Check** - Broadly useful, fast execution
5. **Default Instructions Initialization** - Good for onboarding

### Patterns to Use Carefully

- **TTS Announcement** - Great for accessibility, but adds latency and may be disruptive
- **GitHub Issues Fetch** - Useful but adds network dependency
- **Dynamic Skill Selection** - Powerful but complex to maintain

### Patterns to Avoid

- **Heavy initialization** that blocks session start for >100ms
- **Network-dependent** operations without graceful fallback
- **Attempting to block** (SessionStart cannot block sessions)

### Performance Considerations

| Pattern | Expected Latency | Notes |
|---------|-----------------|-------|
| Logging | <10ms | File I/O only |
| State Reset | <10ms | File deletion |
| Git Status | 10-50ms | Subprocess |
| GitHub Issues | 50-100ms | Network |
| TTS Announcement | 50-100ms | Audio synthesis |
| Context Loading | 50-100ms | Multiple files |

**Total Budget:** Keep SessionStart hooks under 200ms total to avoid noticeable delay.

### Testing Approach

1. **Unit Test Schema Validation**
   ```typescript
   test('parses valid SessionStart payload', () => {
     const payload = {
       hook_event_name: 'SessionStart',
       session_id: 'abc-123',
       transcript_path: '/tmp/transcript.jsonl',
       source: 'startup'
     }
     expect(SessionStartSchema.safeParse(payload).success).toBe(true)
   })
   ```

2. **Integration Test Context Loading**
   ```python
   def test_context_loading_with_git_repo(tmp_path, git_repo):
       context = load_development_context('startup')
       assert 'Git branch:' in context
   ```

3. **Mock External Dependencies**
   ```typescript
   const mockStorage = {
     clearTransientData: jest.fn(),
     getInstructions: jest.fn().mockResolvedValue(null),
     saveInstructions: jest.fn()
   }
   ```

4. **Test All Source Types**
   - Test with `source: 'startup'`
   - Test with `source: 'resume'`
   - Test with `source: 'clear'`

### Configuration Example

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup|resume|clear",
        "hooks": [
          {
            "type": "command",
            "command": "python .claude/hooks/session_start.py --context --log"
          }
        ]
      }
    ]
  }
}
```

---

## Quick Reference

### Input Fields

| Field | Type | Description |
|-------|------|-------------|
| `hook_event_name` | string | Always "SessionStart" |
| `session_id` | string | Unique session identifier (UUID) |
| `transcript_path` | string | Path to session transcript JSONL file |
| `source` | string | "startup", "resume", or "clear" |

### Output Fields

| Field | Type | Description |
|-------|------|-------------|
| `hookSpecificOutput.hookEventName` | string | Must be "SessionStart" |
| `hookSpecificOutput.additionalContext` | string | Text injected into Claude's context |

### Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success (only valid code for SessionStart) |
| Non-zero | Ignored (SessionStart cannot block) |

---

## See Also

- [Stop Hook Guide](./STOP.md) - Session end patterns
- [PreToolUse Hook Guide](./PRE_TOOL_USE.md) - Tool interception patterns
- [Claude Code Hooks Documentation](https://docs.anthropic.com/claude-code/hooks)
