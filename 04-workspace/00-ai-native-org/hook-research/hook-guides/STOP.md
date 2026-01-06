# Stop Hook Guide

## 1. Overview

### What This Hook Does
The **Stop** hook fires when Claude Code completes its response and returns control to the user. This hook intercepts the session termination event, allowing you to:
- Log session completion for analytics
- Export conversation transcripts
- Announce task completion via audio/notifications
- Perform cleanup operations
- Optionally block the stop (keeping Claude active)

### When It Fires (Trigger Conditions)
The Stop hook fires when:
- Claude finishes responding and has no more actions to take
- The agent loop completes (all tool calls resolved)
- User explicitly stops Claude with Ctrl+C or escape (in some cases)

**Important**: Stop fires for the main agent only. For subagent (Task tool) completions, use `SubagentStop` instead.

### Can It Block?
**Yes** - Exit code 2 or returning `decision: "block"` can prevent the session from stopping.

When blocked, Claude remains active with the `reason` field shown as context for why it should continue working.

### JSON Input Schema
```json
{
  "hook_event_name": "Stop",
  "session_id": "string - unique session identifier",
  "transcript_path": "string - path to JSONL transcript file",
  "stop_hook_active": "boolean - true if another Stop hook is running (prevents loops)"
}
```

### JSON Output Schema
```json
{
  "decision": "block" | undefined,
  "reason": "string - explanation when blocking (required if decision is 'block')",
  "continue": "boolean - (optional) if false, stops further hooks",
  "stopReason": "string - (optional) reason for stopping hook chain",
  "suppressOutput": "boolean - (optional) suppress hook output from logs"
}
```

**Exit Codes:**
- `0` - Allow stop (or no decision needed)
- `2` - Block stop (Claude continues)

---

## 2. Pattern Catalog

### Pattern: Stop Event Logging
**Sources**: claude-code-hooks-mastery, claude-hooks (TypeScript)
**Description**: Logs all stop events to a persistent JSON file for audit trails, analytics, and debugging session behavior.
**Decision Type**: none (exit 0)

**Implementation**:
```python
#!/usr/bin/env python3
import json
import sys
import os
from pathlib import Path

def main():
    try:
        input_data = json.load(sys.stdin)

        # Ensure log directory exists
        log_dir = Path("logs")
        log_dir.mkdir(parents=True, exist_ok=True)
        log_path = log_dir / "stop.json"

        # Read existing log data or initialize
        if log_path.exists():
            with open(log_path, 'r') as f:
                try:
                    log_data = json.load(f)
                except (json.JSONDecodeError, ValueError):
                    log_data = []
        else:
            log_data = []

        # Append new stop event
        log_data.append(input_data)

        # Write back with formatting
        with open(log_path, 'w') as f:
            json.dump(log_data, f, indent=2)

        sys.exit(0)

    except Exception:
        sys.exit(0)  # Fail silently to avoid blocking

if __name__ == '__main__':
    main()
```

**Pros**:
- Simple implementation
- Creates audit trail of session completions
- Useful for debugging session patterns

**Cons**:
- Log file grows unbounded without rotation
- Disk I/O on every stop

**Use When**: Tracking session frequency, debugging premature stops, compliance auditing
**Avoid When**: High-frequency session turnover, disk space is limited

---

### Pattern: Transcript Export to JSON
**Sources**: claude-code-hooks-mastery
**Description**: Converts the session transcript from JSONL format to a formatted JSON array file for easier reading and external tool processing.
**Decision Type**: none (exit 0)

**Implementation**:
```python
#!/usr/bin/env python3
import json
import sys
import os

def main():
    try:
        input_data = json.load(sys.stdin)

        log_dir = os.path.join(os.getcwd(), "logs")
        os.makedirs(log_dir, exist_ok=True)

        # Export transcript if available
        if 'transcript_path' in input_data:
            transcript_path = input_data['transcript_path']
            if os.path.exists(transcript_path):
                chat_data = []
                with open(transcript_path, 'r') as f:
                    for line in f:
                        line = line.strip()
                        if line:
                            try:
                                chat_data.append(json.loads(line))
                            except json.JSONDecodeError:
                                pass  # Skip malformed lines

                chat_file = os.path.join(log_dir, 'chat.json')
                with open(chat_file, 'w') as f:
                    json.dump(chat_data, f, indent=2)

        sys.exit(0)

    except Exception:
        sys.exit(0)

if __name__ == '__main__':
    main()
```

**Pros**:
- Makes conversation history accessible to external tools
- Human-readable format with proper indentation
- Enables post-session analysis

**Cons**:
- Duplicates transcript data
- Can be slow for very long sessions

**Use When**: Building analytics dashboards, archiving sessions, debugging conversation flow
**Avoid When**: Transcripts contain sensitive data, disk space is limited

---

### Pattern: TTS Completion Announcement
**Sources**: claude-code-hooks-mastery
**Description**: Announces task completion via text-to-speech when Claude stops, with tiered provider selection (ElevenLabs > OpenAI > pyttsx3 offline).
**Decision Type**: none (exit 0)

**Implementation**:
```python
#!/usr/bin/env python3
import json
import sys
import os
import subprocess
from pathlib import Path

def get_tts_script_path():
    """Select best available TTS provider based on API keys."""
    script_dir = Path(__file__).parent
    tts_dir = script_dir / "utils" / "tts"

    # Priority: ElevenLabs > OpenAI > pyttsx3 (offline)
    if os.getenv('ELEVENLABS_API_KEY'):
        elevenlabs_script = tts_dir / "elevenlabs_tts.py"
        if elevenlabs_script.exists():
            return str(elevenlabs_script)

    if os.getenv('OPENAI_API_KEY'):
        openai_script = tts_dir / "openai_tts.py"
        if openai_script.exists():
            return str(openai_script)

    # Fallback to offline TTS
    pyttsx3_script = tts_dir / "pyttsx3_tts.py"
    if pyttsx3_script.exists():
        return str(pyttsx3_script)

    return None

def announce_completion():
    """Announce completion using best available TTS."""
    try:
        tts_script = get_tts_script_path()
        if not tts_script:
            return

        completion_message = "Task complete"

        subprocess.run(
            ["python", tts_script, completion_message],
            capture_output=True,
            timeout=10
        )
    except Exception:
        pass  # Fail silently

def main():
    try:
        input_data = json.load(sys.stdin)
        announce_completion()
        sys.exit(0)
    except Exception:
        sys.exit(0)

if __name__ == '__main__':
    main()
```

**Pros**:
- Audio feedback for task completion
- Graceful degradation across providers
- Enables hands-free workflows

**Cons**:
- Adds latency (100ms+)
- Requires audio hardware
- Can be disruptive in shared environments

**Use When**: Working away from screen, accessibility needs, long-running tasks
**Avoid When**: Quiet/shared environments, fast session turnover, headless servers

---

### Pattern: LLM-Generated Completion Messages
**Sources**: claude-code-hooks-mastery
**Description**: Generates dynamic, personalized completion messages using LLM APIs (OpenAI > Anthropic > Ollama) with fallback to predefined messages.
**Decision Type**: none (exit 0)

**Implementation**:
```python
#!/usr/bin/env python3
import json
import sys
import os
import subprocess
import random
from pathlib import Path

def get_completion_messages():
    """Fallback message pool."""
    return [
        "Task complete!",
        "All done!",
        "Ready for the next challenge!",
        "Mission accomplished!",
        "Work complete, awaiting instructions!"
    ]

def get_llm_completion_message():
    """Generate dynamic message via LLM if available."""
    script_dir = Path(__file__).parent
    llm_dir = script_dir / "utils" / "llm"

    # Try OpenAI
    if os.getenv('OPENAI_API_KEY'):
        oai_script = llm_dir / "oai.py"
        if oai_script.exists():
            try:
                result = subprocess.run(
                    ["python", str(oai_script), "--completion"],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                if result.returncode == 0 and result.stdout.strip():
                    return result.stdout.strip()
            except Exception:
                pass

    # Fallback to random message
    return random.choice(get_completion_messages())

def main():
    try:
        input_data = json.load(sys.stdin)
        message = get_llm_completion_message()
        # Use message for TTS or logging
        print(message)  # Or pass to TTS
        sys.exit(0)
    except Exception:
        sys.exit(0)

if __name__ == '__main__':
    main()
```

**Pros**:
- Varied, engaging completion messages
- Optional personalization via ENGINEER_NAME env var
- Graceful fallback chain

**Cons**:
- High latency (100ms+) for LLM calls
- API costs for each completion
- Non-deterministic output

**Use When**: Building engaging user experiences, personalized assistant feel
**Avoid When**: Cost sensitivity, fast turnaround required, deterministic behavior needed

---

### Pattern: Session End Logger (TypeScript SDK)
**Sources**: claude-hooks (TypeScript)
**Description**: Logs session end events using the TypeScript SDK pattern with type-safe payloads and session state persistence.
**Decision Type**: none (empty object return)

**Implementation**:
```typescript
import type { StopHandler, StopPayload } from './lib'
import { saveSessionData } from './session'

const stop: StopHandler = async (payload: StopPayload) => {
  // Persist to session-specific JSON file
  await saveSessionData('Stop', { ...payload, hook_type: 'Stop' } as const)

  console.log(`Session ended: ${payload.session_id}`)

  // Check stop_hook_active to prevent loops
  if (payload.stop_hook_active) {
    console.log('Stop hook already active, skipping additional processing')
  }

  return {}  // Empty object = allow stop
}

export { stop }
```

**Pros**:
- Full TypeScript type safety
- Handles stop_hook_active loop prevention
- Integrates with unified handler system

**Cons**:
- Requires Bun/Node runtime
- More complex setup than Python

**Use When**: TypeScript projects, need type-safe hook development, unified multi-hook systems
**Avoid When**: Simple one-off hooks, environments without Node.js

---

### Pattern: Stop Hook Loop Prevention
**Sources**: claude-hooks (TypeScript)
**Description**: Uses the `stop_hook_active` flag to prevent infinite loops when a Stop hook itself triggers actions that would cause another stop.
**Decision Type**: none

**Implementation**:
```typescript
const stop: StopHandler = async (payload) => {
  // CRITICAL: Check if stop hook is already active
  if (payload.stop_hook_active) {
    // Another stop hook is running - avoid recursion
    console.log('Stop hook already active, skipping')
    return {}
  }

  // Safe to proceed with stop processing
  await performStopActions(payload)

  return {}
}
```

```python
# Python equivalent
def main():
    input_data = json.load(sys.stdin)

    # Check stop_hook_active to prevent loops
    if input_data.get('stop_hook_active', False):
        sys.exit(0)  # Early exit to prevent recursion

    # Safe to proceed
    perform_stop_actions(input_data)
    sys.exit(0)
```

**Pros**:
- Prevents infinite hook loops
- Built-in to Claude Code's hook system
- Simple boolean check

**Cons**:
- Limits what secondary hooks can do
- Requires explicit handling

**Use When**: Always - this is a defensive pattern that should be standard
**Avoid When**: Never - always check this flag

---

### Pattern: Blocking Stop for Incomplete Tasks
**Sources**: Derived from hook specification (theoretical pattern)
**Description**: Blocks the stop event when tasks are incomplete, keeping Claude active with guidance on what to finish.
**Decision Type**: block (exit 2 or decision: "block")

**Implementation**:
```python
#!/usr/bin/env python3
import json
import sys
from pathlib import Path

def check_incomplete_tasks():
    """Check for incomplete tasks that should block stop."""
    todo_file = Path(".claude/todos.json")

    if not todo_file.exists():
        return None

    try:
        with open(todo_file, 'r') as f:
            todos = json.load(f)

        incomplete = [t for t in todos if t.get('status') != 'completed']
        if incomplete:
            task_list = "\n".join([f"- {t['content']}" for t in incomplete[:5]])
            return f"Incomplete tasks remain:\n{task_list}\n\nPlease complete these before stopping."

    except Exception:
        pass

    return None

def main():
    try:
        input_data = json.load(sys.stdin)

        # Check for incomplete work
        block_reason = check_incomplete_tasks()

        if block_reason:
            output = {
                "decision": "block",
                "reason": block_reason
            }
            print(json.dumps(output))
            sys.exit(0)

        sys.exit(0)

    except Exception:
        sys.exit(0)

if __name__ == '__main__':
    main()
```

**Pros**:
- Ensures tasks are completed before stopping
- Provides clear guidance on what remains
- Can enforce workflow completion

**Cons**:
- May trap users in unwanted loops
- Requires reliable task state tracking
- Can be frustrating if blocking logic is flawed

**Use When**: Critical workflows that must complete, enforcing checklist completion
**Avoid When**: General development where users need control, unreliable task tracking

---

## 3. Inspiration Ideas

### New Use Cases Based on Patterns

1. **Session Analytics Dashboard**
   - Combine stop logging with a real-time dashboard
   - Track: session duration, tool usage counts, error rates
   - Visualize patterns over time

2. **Git Commit Summary on Stop**
   - On stop, summarize all git operations performed
   - List files changed, commits made, branches touched
   - Useful for session wrap-up reports

3. **Conversation Export to Multiple Formats**
   - Extend transcript export to support Markdown, HTML, PDF
   - Generate shareable session reports
   - Integrate with documentation systems

4. **Cost Tracking on Stop**
   - Calculate token usage from transcript
   - Estimate API costs for the session
   - Alert if session exceeded budget threshold

5. **Auto-Backup Before Stop**
   - Create git stash or checkpoint before stopping
   - Ensure no work is lost if session ends unexpectedly
   - Similar to PreCompact backup pattern

6. **Stop Confirmation for Long Sessions**
   - Block stop for sessions over N hours
   - Require explicit confirmation before ending
   - Prevent accidental exit from important work

7. **Multi-Agent Coordination**
   - On stop, notify other agents in a multi-agent system
   - Update shared state or message queue
   - Trigger handoff to next agent in pipeline

### Combinations with Other Hooks

- **Stop + PreCompact**: Backup transcript both before compaction and on stop
- **Stop + Notification**: Chain TTS completion with desktop notification
- **Stop + SessionStart**: Track session duration (start to stop)
- **Stop + PostToolUse**: Correlate stop events with final tool actions

### Advanced Applications

1. **Graceful Shutdown Orchestration**
   - Clean up temporary files created during session
   - Close MCP connections properly
   - Release any held resources

2. **Session Continuity Bridge**
   - On stop, save session state to enable "resume" functionality
   - Copy session ID to clipboard for handoff
   - Generate resume command for next session

3. **Quality Gate on Stop**
   - Run final quality checks (tests, lint)
   - Block stop if code quality degraded during session
   - Ensure no regressions introduced

---

## 4. Implementation Recommendations

### Best Patterns to Adopt (Ranked)

1. **Stop Event Logging** (Essential)
   - Low complexity, high value
   - Foundation for analytics and debugging
   - Always include as baseline

2. **Stop Hook Loop Prevention** (Critical)
   - Must always check `stop_hook_active`
   - Prevents system hangs
   - No downside to including

3. **Transcript Export** (Recommended)
   - Enables post-session analysis
   - Useful for debugging and documentation
   - Low overhead

4. **TTS Completion Announcement** (Optional)
   - Great for accessibility
   - Useful when working away from screen
   - Environment-dependent value

5. **Blocking Stop Pattern** (Use Cautiously)
   - High-value for critical workflows
   - Can be frustrating if misused
   - Requires reliable state tracking

### Patterns to Avoid

1. **Unconditional Stop Blocking**
   - Never block stop without a clear escape path
   - Users must always be able to exit

2. **Heavy Processing in Stop**
   - Avoid long-running operations
   - Users expect quick session termination
   - Use async/background processing instead

3. **Ignoring stop_hook_active**
   - Always check this flag
   - Failure to check can cause infinite loops

### Performance Considerations

| Pattern | Expected Latency | Impact |
|---------|------------------|--------|
| Stop Logging | <10ms | Negligible |
| Transcript Export | 10-50ms | Acceptable |
| TTS Announcement | 100-500ms | Noticeable |
| LLM Message Generation | 500ms-2s | Significant |
| Stop Blocking Check | <10ms | Negligible |

**Recommendation**: Keep total stop hook processing under 100ms for responsive feel. If using TTS or LLM features, make them optional and clearly documented.

### Testing Approach

1. **Unit Testing**
   - Mock stdin JSON input
   - Verify correct exit codes
   - Test error handling (malformed input)

2. **Integration Testing**
   - Test with actual Claude Code sessions
   - Verify transcript_path accessibility
   - Test stop_hook_active behavior

3. **Edge Cases to Test**
   - Empty session (immediate stop)
   - Very long sessions (large transcripts)
   - Multiple stop hooks chained
   - Missing transcript file
   - Permission errors on log directories

**Example Test Setup**:
```python
import subprocess
import json

def test_stop_hook():
    input_data = {
        "hook_event_name": "Stop",
        "session_id": "test-session-123",
        "transcript_path": "/tmp/test_transcript.jsonl",
        "stop_hook_active": False
    }

    result = subprocess.run(
        ["python", "stop_hook.py"],
        input=json.dumps(input_data),
        capture_output=True,
        text=True
    )

    assert result.returncode == 0
    # Verify log file was created
    # Verify expected output format
```

---

## Summary

The Stop hook is your opportunity to perform session cleanup, logging, and user notification when Claude Code completes its work. The most valuable patterns are simple logging and transcript export, with optional TTS for accessibility. Always check `stop_hook_active` to prevent loops, and be cautious with blocking patterns that could trap users. Keep processing fast (<100ms) for a responsive user experience.
