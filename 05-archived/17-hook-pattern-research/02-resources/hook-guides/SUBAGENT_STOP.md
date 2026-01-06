# SubagentStop Hook Guide

## 1. Overview

### What This Hook Does
The `SubagentStop` hook fires when a subagent (spawned via the Task tool) completes its work. This enables parent agents to receive notifications, perform cleanup, log analytics, or take action when delegated tasks finish.

### When It Fires (Trigger Conditions)
- When a Task tool invocation completes (successfully or with errors)
- After the subagent has finished all its work and is about to return control to the parent agent
- Both for normal completion and early termination scenarios

### Can It Block?
**Yes** - Exit code 2 blocks the subagent completion (though this is rarely useful in practice since the work is already done).

More practically, the hook can output JSON with `decision: 'block'` and a `reason` to prompt Claude with follow-up instructions.

### JSON Input Schema

The SubagentStop hook receives the following JSON payload on stdin:

```json
{
  "hook_event_name": "SubagentStop",
  "session_id": "string - unique session identifier",
  "transcript_path": "string - path to JSONL transcript file",
  "stop_hook_active": "boolean - true if another stop hook is already running (prevents infinite loops)"
}
```

**Key Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `hook_event_name` | `"SubagentStop"` | Identifies this as a SubagentStop event |
| `session_id` | `string` | Unique identifier for the current session |
| `transcript_path` | `string` | Path to the JSONL file containing the subagent's conversation |
| `stop_hook_active` | `boolean` | Prevents infinite loops when hooks trigger other stop events |

### JSON Output Schema

```json
{
  "decision": "block",           // Optional: "block" to provide follow-up message
  "reason": "string",            // Required when decision is "block"
  "continue": true,              // Optional: allow subagent to complete normally
  "stopReason": "string",        // Optional: reason for stopping
  "suppressOutput": false        // Optional: suppress hook output
}
```

**Decision Types:**

| Decision | Effect |
|----------|--------|
| `undefined` or empty `{}` | Subagent completes normally |
| `"block"` + `reason` | Claude receives the reason as a follow-up message |

---

## 2. Pattern Catalog

### Pattern: Subagent Stop Event Logging
**Sources**: claude-code-hooks-mastery
**Description**: Logs all subagent stop events to a dedicated JSON file for multi-agent workflow tracking and analytics.
**Decision Type**: none (exit 0)

**Implementation**:
```python
#!/usr/bin/env python3
import json
import os
import sys

def main():
    try:
        input_data = json.load(sys.stdin)

        # Ensure log directory exists
        log_dir = os.path.join(os.getcwd(), "logs")
        os.makedirs(log_dir, exist_ok=True)
        log_path = os.path.join(log_dir, "subagent_stop.json")

        # Read existing log data or initialize empty list
        if os.path.exists(log_path):
            with open(log_path, 'r') as f:
                try:
                    log_data = json.load(f)
                except (json.JSONDecodeError, ValueError):
                    log_data = []
        else:
            log_data = []

        # Append new data
        log_data.append(input_data)

        # Write back to file with formatting
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
- Enables analytics on subagent task patterns
- Helps debug multi-agent coordination issues
- Creates audit trail for delegated tasks
- Separate from main Stop log for cleaner analysis

**Cons**:
- Log file grows with each subagent invocation
- No automatic log rotation

**Use When**: Orchestrating multiple subagents and need to track their individual completion patterns.
**Avoid When**: Not using Task tool functionality; concerned about disk space.

---

### Pattern: Subagent Completion TTS Notification
**Sources**: claude-code-hooks-mastery
**Description**: Announces subagent task completion via text-to-speech with a fixed "Subagent Complete" message.
**Decision Type**: none (exit 0)

**Implementation**:
```python
#!/usr/bin/env python3
import os
import subprocess
import sys
from pathlib import Path

def get_tts_script_path():
    """
    Determine which TTS script to use based on available API keys.
    Priority order: ElevenLabs > OpenAI > pyttsx3
    """
    script_dir = Path(__file__).parent
    tts_dir = script_dir / "utils" / "tts"

    # Check for ElevenLabs API key (highest priority)
    if os.getenv('ELEVENLABS_API_KEY'):
        elevenlabs_script = tts_dir / "elevenlabs_tts.py"
        if elevenlabs_script.exists():
            return str(elevenlabs_script)

    # Check for OpenAI API key (second priority)
    if os.getenv('OPENAI_API_KEY'):
        openai_script = tts_dir / "openai_tts.py"
        if openai_script.exists():
            return str(openai_script)

    # Fall back to pyttsx3 (no API key required)
    pyttsx3_script = tts_dir / "pyttsx3_tts.py"
    if pyttsx3_script.exists():
        return str(pyttsx3_script)

    return None

def announce_subagent_completion():
    """Announce subagent completion using the best available TTS service."""
    try:
        tts_script = get_tts_script_path()
        if not tts_script:
            return  # No TTS scripts available

        # Use fixed message for subagent completion
        completion_message = "Subagent Complete"

        # Call the TTS script with the completion message
        subprocess.run([
            "uv", "run", tts_script, completion_message
        ],
        capture_output=True,  # Suppress output
        timeout=10  # 10-second timeout
        )

    except (subprocess.TimeoutExpired, subprocess.SubprocessError, FileNotFoundError):
        pass  # Fail silently
    except Exception:
        pass  # Fail silently

def main():
    try:
        # Announce completion via TTS
        announce_subagent_completion()
        sys.exit(0)
    except Exception:
        sys.exit(0)

if __name__ == '__main__':
    main()
```

**Pros**:
- Audible notification when working on other tasks
- Distinct from main agent stop notification
- Cascading TTS provider selection (premium to free fallback)

**Cons**:
- Can be noisy if subagents complete frequently
- Requires TTS infrastructure

**Use When**: Running long-running delegated tasks; want audio notification when each completes.
**Avoid When**: Subagents complete frequently; shared/quiet environments.

---

### Pattern: Subagent Transcript Export
**Sources**: claude-code-hooks-mastery
**Description**: Exports subagent transcript from JSONL to formatted JSON array for external analysis.
**Decision Type**: none (exit 0)

**Implementation**:
```python
#!/usr/bin/env python3
import argparse
import json
import os
import sys

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--chat', action='store_true', help='Export transcript to chat.json')
    args = parser.parse_args()

    try:
        input_data = json.load(sys.stdin)

        log_dir = os.path.join(os.getcwd(), "logs")
        os.makedirs(log_dir, exist_ok=True)

        # Handle --chat switch
        if args.chat and 'transcript_path' in input_data:
            transcript_path = input_data['transcript_path']
            if os.path.exists(transcript_path):
                chat_data = []
                try:
                    with open(transcript_path, 'r') as f:
                        for line in f:
                            line = line.strip()
                            if line:
                                try:
                                    chat_data.append(json.loads(line))
                                except json.JSONDecodeError:
                                    pass

                    # Write to logs/subagent_chat.json
                    chat_file = os.path.join(log_dir, 'subagent_chat.json')
                    with open(chat_file, 'w') as f:
                        json.dump(chat_data, f, indent=2)
                except Exception:
                    pass

        sys.exit(0)

    except Exception:
        sys.exit(0)

if __name__ == '__main__':
    main()
```

**Pros**:
- Makes subagent conversations accessible for review
- Enables post-hoc analysis of delegated tasks
- Standard JSON format for external tools

**Cons**:
- Duplicates data (transcript already exists as JSONL)
- Large transcripts can be slow to convert

**Use When**: Need to review subagent conversations; building analytics dashboards.
**Avoid When**: Transcripts contain sensitive data; storage is limited.

---

### Pattern: Stop Hook Loop Prevention Guard
**Sources**: claude-hooks (TypeScript SDK)
**Description**: Checks `stop_hook_active` flag to prevent infinite hook loops when subagent stops.
**Decision Type**: none (exit 0)

**Implementation**:
```typescript
import type { SubagentStopHandler, SubagentStopPayload } from './lib'

const subagentStop: SubagentStopHandler = async (payload: SubagentStopPayload) => {
  console.log(`Subagent task completed`)

  // Check for hook loop prevention
  if (payload.stop_hook_active) {
    console.log('Stop hook is already active, skipping additional processing')
    // Exit early to prevent loops
    return {}
  }

  // Safe to perform additional processing here
  // ...

  return {}
}
```

**Pros**:
- Prevents infinite hook loops
- Essential safety check for any non-trivial SubagentStop hook
- Simple to implement

**Cons**:
- Must remember to check this flag
- May skip desired processing if not handled carefully

**Use When**: Always - this is a fundamental safety pattern.
**Avoid When**: Never skip this check.

---

### Pattern: Multi-Agent Communication Hub
**Sources**: awesome-claude-code (claude-hook-comms reference)
**Description**: Enables real-time communication between Claude Code subagents using hooks.
**Decision Type**: none

**Implementation** (Conceptual):
```python
#!/usr/bin/env python3
"""
Multi-agent communication via SubagentStop hook.
When a subagent completes, notify other agents via shared message queue.
"""
import json
import os
import sys
from pathlib import Path

def main():
    try:
        input_data = json.load(sys.stdin)
        session_id = input_data.get('session_id', '')

        # Shared message directory for inter-agent communication
        msg_dir = Path.home() / ".claude-hcom" / "messages"
        msg_dir.mkdir(parents=True, exist_ok=True)

        # Write completion notification for other agents to pick up
        msg_file = msg_dir / f"{session_id}_complete.json"
        msg_file.write_text(json.dumps({
            "type": "subagent_complete",
            "session_id": session_id,
            "timestamp": __import__('datetime').datetime.now().isoformat()
        }))

        sys.exit(0)
    except Exception:
        sys.exit(0)

if __name__ == '__main__':
    main()
```

**Pros**:
- Enables sophisticated multi-agent orchestration
- Zero-dependency file-based communication
- @-mention targeting possible

**Cons**:
- Complex to implement correctly
- Requires careful state management
- Currently unstable (per awesome-claude-code notes)

**Use When**: Building complex multi-agent workflows requiring coordination.
**Avoid When**: Single-agent tasks; simple delegation scenarios.

---

### Pattern: Graceful Error Handling
**Sources**: claude-code-hooks-mastery
**Description**: Universal pattern for SubagentStop hooks that ensures they never block the agent on errors.
**Decision Type**: none (always exit 0)

**Implementation**:
```python
#!/usr/bin/env python3
import json
import sys

def main():
    try:
        input_data = json.load(sys.stdin)

        # ... your hook logic here ...

        sys.exit(0)

    except json.JSONDecodeError:
        # Handle JSON decode errors gracefully
        sys.exit(0)
    except Exception:
        # Handle any other errors gracefully
        sys.exit(0)

if __name__ == '__main__':
    main()
```

**Pros**:
- Prevents hook failures from blocking Claude
- Silent degradation rather than hard failure
- Essential for observability-only hooks

**Cons**:
- May hide bugs in hook logic
- Makes debugging harder

**Use When**: In any hook where you want logging/notification but must never block.
**Avoid When**: Never for safety-critical hooks that should block on errors.

---

## 3. Inspiration Ideas

Based on the patterns found, here are novel use cases for SubagentStop:

### Advanced Applications

1. **Subagent Performance Metrics**
   - Track execution time between SubagentStart (if implemented) and SubagentStop
   - Measure token usage from transcript analysis
   - Build dashboards showing subagent efficiency

2. **Result Aggregation Pipeline**
   - When subagent completes, extract key results from transcript
   - Aggregate results from multiple subagents into a summary file
   - Enable "map-reduce" style parallel task execution

3. **Automatic Quality Gates**
   - Analyze subagent transcript for error patterns
   - Block completion and inject retry instructions if quality thresholds not met
   - Implement automatic rollback on subagent failures

4. **Session Handoff Preparation**
   - When subagent completes, prepare handoff notes for parent agent
   - Extract key decisions and artifacts from transcript
   - Create structured summary for seamless context transfer

5. **Webhook Integration**
   - POST subagent completion to external services (Slack, Discord, webhooks)
   - Enable external monitoring of multi-agent workflows
   - Trigger downstream automation pipelines

### Combinations with Other Hooks

1. **SubagentStop + SessionStart**
   - Track subagent sessions as a graph
   - Build parent-child relationship maps
   - Visualize agent delegation patterns

2. **SubagentStop + PreToolUse (in parent)**
   - After subagent completes, inject its results into parent's context
   - Enable parent to validate subagent's work before proceeding

3. **SubagentStop + Notification**
   - Different notification styles for subagent vs main agent completion
   - Priority-based notifications (critical subagents get urgent alerts)

### Patterns from Other Domains

1. **From CI/CD: Job Completion Handlers**
   - Treat subagent completion like a CI job finishing
   - Collect artifacts, update status badges, notify stakeholders

2. **From Microservices: Distributed Tracing**
   - Inject trace IDs into subagent sessions
   - Build correlation maps across agent hierarchies
   - Enable end-to-end latency analysis

3. **From Kubernetes: Pod Lifecycle Hooks**
   - PreStop equivalent: Save state before subagent terminates
   - PostStop equivalent: Cleanup resources after completion

---

## 4. Implementation Recommendations

### Best Patterns to Adopt (Ranked)

1. **Graceful Error Handling** (Essential)
   - Always implement try/except with exit 0 fallback
   - Prevents hook failures from disrupting workflows

2. **Stop Hook Loop Prevention Guard** (Essential)
   - Always check `stop_hook_active` before processing
   - Prevents infinite loops in complex hook chains

3. **Subagent Stop Event Logging** (Recommended)
   - Low overhead, high value for debugging
   - Essential for multi-agent workflow analytics

4. **Subagent Completion TTS Notification** (Optional)
   - Useful for long-running delegated tasks
   - Consider frequency of subagent completions

5. **Subagent Transcript Export** (Situational)
   - Valuable for post-hoc analysis
   - Consider storage implications

### Patterns to Avoid

1. **Blocking on SubagentStop**
   - The work is already done; blocking rarely makes sense
   - Exception: Quality gates that trigger retry instructions

2. **Heavy Processing in Hook**
   - Subagent completion should be fast
   - Move heavy analysis to async background jobs

3. **Ignoring `stop_hook_active` Flag**
   - Will cause infinite loops in complex scenarios
   - Always check this flag first

### Performance Considerations

| Pattern | Typical Latency | Disk I/O | Network I/O |
|---------|-----------------|----------|-------------|
| Event Logging | <10ms | Write | None |
| TTS Notification | 50-200ms | None | API call |
| Transcript Export | 10-50ms | Read + Write | None |
| Loop Prevention | <1ms | None | None |

**Recommendations:**
- Keep total hook latency under 100ms for responsive UX
- Async processing for anything that might be slow
- File-based logging is fast; network calls should be optional

### Testing Approach

1. **Unit Testing**
   - Mock stdin with sample SubagentStop payloads
   - Verify correct exit codes for various scenarios
   - Test graceful error handling

2. **Integration Testing**
   - Use Task tool to spawn subagent
   - Verify hook fires on completion
   - Check log files are created correctly

3. **Sample Test Payload**:
```json
{
  "hook_event_name": "SubagentStop",
  "session_id": "test-session-12345",
  "transcript_path": "/tmp/test-transcript.jsonl",
  "stop_hook_active": false
}
```

4. **Test Command**:
```bash
echo '{"hook_event_name":"SubagentStop","session_id":"test","transcript_path":"/tmp/test.jsonl","stop_hook_active":false}' | python your_hook.py
echo $?  # Should be 0
```

---

## Configuration Example

Add to `.claude/settings.json`:

```json
{
  "hooks": {
    "SubagentStop": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "python .claude/hooks/subagent_stop.py"
          }
        ]
      }
    ]
  }
}
```

For combined logging and notification:

```json
{
  "hooks": {
    "SubagentStop": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "python .claude/hooks/subagent_stop.py --log"
          },
          {
            "type": "command",
            "command": "python .claude/hooks/subagent_stop.py --notify"
          }
        ]
      }
    ]
  }
}
```

---

## Summary

SubagentStop is an underutilized hook with significant potential for multi-agent orchestration. The primary use cases are:

- **Observability**: Logging subagent completions for analytics and debugging
- **Communication**: Audio/visual notifications when delegated tasks complete
- **Coordination**: Enabling communication between agents in complex workflows

Key takeaways:
1. Always implement graceful error handling
2. Always check `stop_hook_active` to prevent loops
3. Keep hooks fast (<100ms) for responsive UX
4. Consider the frequency of subagent completions when designing notifications
5. This hook fires after work is complete - blocking is rarely useful
