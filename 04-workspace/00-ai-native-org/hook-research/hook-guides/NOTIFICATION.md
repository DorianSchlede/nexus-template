# Notification Hook - Comprehensive Pattern Guide

## 1. Overview

### What This Hook Does

The **Notification** hook fires when Claude Code wants to notify the user about something. This is primarily used when Claude needs user input or has completed a task and wants to alert the user. It enables custom notification handling such as audio alerts, desktop notifications, terminal bells, or logging.

### When It Fires (Trigger Conditions)

The Notification hook fires when:
- Claude is waiting for user input
- A task or conversation turn completes
- Claude wants to communicate status updates to the user
- The terminal/IDE notification system is triggered

### Can It Block?

**No** - The Notification hook cannot block or modify Claude's behavior. It is purely observational/reactive. The hook receives notification data and can perform side effects (sounds, desktop notifications, logging) but cannot prevent the notification or change its content.

### JSON Input Schema

```json
{
  "session_id": "string",
  "transcript_path": "string",
  "hook_event_name": "Notification",
  "message": "string",
  "title": "string (optional)"
}
```

**Field Descriptions:**
- `session_id`: Unique identifier for the current Claude Code session
- `transcript_path`: Path to the JSONL transcript file for this session
- `hook_event_name`: Always "Notification" for this hook type
- `message`: The notification message content (e.g., "Claude is waiting for your input")
- `title`: Optional title for the notification

### JSON Output Schema

Since Notification hooks cannot block, the output is minimal:

```json
{}
```

Or with optional fields:

```json
{
  "suppressOutput": true
}
```

**Output Options:**
- Empty object `{}`: Continue with default notification behavior
- `suppressOutput: true`: Suppress hook's stdout from being displayed

---

## 2. Pattern Catalog

### Pattern: Notification Logging

**Sources**: hooks-mastery-part3, claude-hooks

**Description**: Logs all Claude Code notifications to a JSON file for monitoring, debugging, and analyzing agent communication patterns.

**Decision Type**: None (observation only)

**Implementation (Python)**:
```python
#!/usr/bin/env python3
import json
import os
import sys

# Read JSON input from stdin
input_data = json.loads(sys.stdin.read())

# Ensure log directory exists
log_dir = os.path.join(os.getcwd(), 'logs')
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, 'notification.json')

# Read existing log data or initialize empty list
if os.path.exists(log_file):
    with open(log_file, 'r') as f:
        try:
            log_data = json.load(f)
        except (json.JSONDecodeError, ValueError):
            log_data = []
else:
    log_data = []

# Append new data
log_data.append(input_data)

# Write back to file with formatting
with open(log_file, 'w') as f:
    json.dump(log_data, f, indent=2)
```

**Implementation (TypeScript)**:
```typescript
const notification: NotificationHandler = async (payload) => {
  await saveSessionData('Notification', {...payload, hook_type: 'Notification'} as const)
  console.log(`${payload.message}`)
  return {}
}
```

**Pros**:
- Creates audit trail of all notifications
- Useful for debugging agent interaction patterns
- Can analyze notification frequency and timing

**Cons**:
- Adds I/O overhead for every notification
- Log files can grow large over time

**Use When**: You need compliance auditing, debugging traces, or analytics on notification patterns

**Avoid When**: Disk I/O is a concern or logs aren't being monitored

---

### Pattern: TTS Audio Alert on Input Request

**Sources**: hooks-mastery-part3

**Description**: Announces via text-to-speech when Claude needs user input, with multi-provider TTS fallback (ElevenLabs > OpenAI > pyttsx3) and optional personalization.

**Decision Type**: None (audio output side effect)

**Implementation (Python)**:
```python
#!/usr/bin/env python3
import json
import os
import random
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

    if os.getenv('ELEVENLABS_API_KEY'):
        return str(tts_dir / "elevenlabs_tts.py")
    if os.getenv('OPENAI_API_KEY'):
        return str(tts_dir / "openai_tts.py")
    return str(tts_dir / "pyttsx3_tts.py")  # Fallback offline TTS

def announce_notification():
    tts_script = get_tts_script_path()
    if not tts_script:
        return

    engineer_name = os.getenv('ENGINEER_NAME', '').strip()

    # 30% chance to include personalized name
    if engineer_name and random.random() < 0.3:
        message = f"{engineer_name}, your agent needs your input"
    else:
        message = "Your agent needs your input"

    subprocess.run(["uv", "run", tts_script, message],
                  capture_output=True, timeout=10)

if __name__ == "__main__":
    input_data = json.loads(sys.stdin.read())

    # Only announce meaningful notifications
    if input_data.get('message') != 'Claude is waiting for your input':
        announce_notification()
```

**Pros**:
- Alerts user even when away from screen
- Multiple TTS provider support with graceful fallback
- Personalization adds engagement
- Works in accessible environments

**Cons**:
- Requires TTS dependencies or API keys
- Audio interruptions may be unwanted
- Network latency with cloud TTS providers

**Use When**: Working away from screen, in accessible environments, or wanting audio feedback for agent states

**Avoid When**: In quiet environments, headless servers, or when immediate audio feedback isn't needed

---

### Pattern: Notification Filtering

**Sources**: hooks-mastery-part3

**Description**: Filters out generic 'waiting for input' notifications to only announce meaningful state changes, reducing notification fatigue.

**Decision Type**: None (filtering logic)

**Implementation (Python)**:
```python
#!/usr/bin/env python3
import json
import sys

input_data = json.loads(sys.stdin.read())

# Only announce meaningful notifications, skip generic waiting messages
if input_data.get('message') != 'Claude is waiting for your input':
    # Proceed with notification handling
    announce_notification()
```

**Pros**:
- Reduces notification noise
- Only surfaces important state changes
- Prevents notification fatigue

**Cons**:
- May miss some legitimate notifications
- Requires knowing which messages are "generic"

**Use When**: Reducing notification noise and only surfacing important state changes

**Avoid When**: You need to capture every notification for auditing

---

### Pattern: OS Desktop Notification Sender

**Sources**: codex-settings

**Description**: Sends OS desktop notifications when Claude Code completes tasks; also triggers terminal bell for VSCode visual feedback.

**Decision Type**: None (notification side effect)

**Implementation (Bash)**:
```bash
#!/usr/bin/env bash
input=$(cat)
message=$(echo "$input" | grep -o '"message":"[^"]*"' | cut -d'"' -f4)
title="Claude Code"

# Terminal bell - triggers VSCode visual bell icon
printf '\a'

# Send OS notification
if [[ "$OSTYPE" == "darwin"* ]]; then
  osascript -e "display notification \"${message}\" with title \"${title}\" sound name \"Glass\""
elif command -v notify-send &> /dev/null; then
  notify-send "${title}" "${message}" -u normal -i terminal
fi
```

**Pros**:
- Cross-platform (macOS and Linux)
- Uses native OS notification system
- Terminal bell provides visual feedback in VSCode
- No external dependencies beyond OS tools

**Cons**:
- Windows support requires additional implementation
- Native notifications may not be available in all environments
- Sound names are platform-specific

**Use When**: Alert user when long-running Claude tasks complete or need attention

**Avoid When**: Headless environments without notification support, or where notifications would be disruptive

---

### Pattern: Multi-Provider TTS with ElevenLabs

**Sources**: hooks-mastery-part3

**Description**: High-quality text-to-speech using ElevenLabs Turbo v2.5 model with configurable voice settings for natural-sounding notifications.

**Decision Type**: None (audio output)

**Implementation (Python)**:
```python
#!/usr/bin/env python3
# /// script
# dependencies = ["elevenlabs"]
# ///

import os
import sys
from elevenlabs.client import ElevenLabs
from elevenlabs import play

api_key = os.getenv('ELEVENLABS_API_KEY')
elevenlabs = ElevenLabs(api_key=api_key)

text = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "Default message"

audio = elevenlabs.text_to_speech.convert(
    text=text,
    voice_id="WejK3H1m7MI9CHnIjW9K",  # Specific voice ID
    model_id="eleven_turbo_v2_5",
    output_format="mp3_44100_128",
)

play(audio)
```

**Pros**:
- Highest quality, most natural-sounding TTS
- Fast turbo model minimizes latency
- Many voice options available
- Consistent cross-platform audio

**Cons**:
- Requires paid API key
- Network dependency
- API rate limits may apply

**Use When**: High-quality, natural-sounding voice output is required

**Avoid When**: API costs are a concern, offline operation is needed, or in low-bandwidth environments

---

### Pattern: Multi-Provider TTS with OpenAI

**Sources**: hooks-mastery-part3

**Description**: Text-to-speech using OpenAI gpt-4o-mini-tts model with async streaming playback and voice instructions for tone control.

**Decision Type**: None (audio output)

**Implementation (Python)**:
```python
#!/usr/bin/env python3
# /// script
# dependencies = ["openai"]
# ///

import asyncio
import os
import sys
from openai import AsyncOpenAI
from openai.helpers import LocalAudioPlayer

openai = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
text = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "Your agent needs input"

async def main():
    async with openai.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice="nova",
        input=text,
        instructions="Speak in a cheerful, positive yet professional tone.",
        response_format="mp3",
    ) as response:
        await LocalAudioPlayer().play(response)

asyncio.run(main())
```

**Pros**:
- Good quality with streaming playback
- Voice instructions allow tone customization
- Uses existing OpenAI API key
- Lower latency with streaming

**Cons**:
- Requires OpenAI API key
- Async implementation adds complexity
- API costs apply

**Use When**: OpenAI is already being used and streaming audio playback is desired

**Avoid When**: ElevenLabs is preferred for quality, or offline operation is needed

---

### Pattern: Offline TTS Fallback with pyttsx3

**Sources**: hooks-mastery-part3

**Description**: Offline text-to-speech using pyttsx3 for environments without API keys or network access, with configurable rate and volume.

**Decision Type**: None (audio output)

**Implementation (Python)**:
```python
#!/usr/bin/env python3
# /// script
# dependencies = ["pyttsx3"]
# ///

import random
import sys
import pyttsx3

engine = pyttsx3.init()
engine.setProperty('rate', 180)    # Speech rate (words per minute)
engine.setProperty('volume', 0.8)  # Volume (0.0 to 1.0)

text = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else random.choice([
    "Work complete!", "All done!", "Task finished!",
    "Job complete!", "Ready for next task!"
])

engine.say(text)
engine.runAndWait()
```

**Pros**:
- Fully offline operation
- No API keys required
- Cross-platform support
- Zero cost

**Cons**:
- Lower quality than cloud TTS
- Voice options are system-dependent
- May sound robotic

**Use When**: No API keys are available, offline operation is required, or cost is a concern

**Avoid When**: Natural-sounding voice is important

---

### Pattern: TypeScript Notification Handler SDK

**Sources**: claude-hooks

**Description**: Type-safe notification handler using the claude-hooks TypeScript SDK, with session persistence for debugging.

**Decision Type**: None

**Implementation (TypeScript)**:
```typescript
import type { NotificationHandler, NotificationPayload } from './lib'
import { saveSessionData } from './session'

// NotificationPayload type:
// {
//   session_id: string
//   transcript_path: string
//   hook_event_name: 'Notification'
//   message: string
//   title?: string
// }

const notification: NotificationHandler = async (payload: NotificationPayload) => {
  // Persist to session data for debugging
  await saveSessionData('Notification', {...payload, hook_type: 'Notification'} as const)

  // Log notification
  console.log(`[${payload.title || 'Notification'}] ${payload.message}`)

  // Could extend with:
  // - Desktop notifications (node-notifier)
  // - Slack/Discord webhooks
  // - Sound playback (play-sound)

  return {} // Empty response - notifications can't block
}

export { notification }
```

**Pros**:
- Full TypeScript type safety
- Clean handler interface
- Session data persistence built-in
- Easy to extend with additional notification channels

**Cons**:
- Requires Bun runtime
- TypeScript compilation overhead

**Use When**: Building TypeScript-based hook systems with full type safety

**Avoid When**: Simple shell scripts are sufficient

---

## 3. Inspiration Ideas

### What ELSE Could This Hook Do?

1. **Slack/Discord/Teams Integration**
   - Send notifications to team channels when Claude needs input
   - Include session context and elapsed time
   - Enable remote monitoring of Claude sessions

2. **Push Notifications (Mobile)**
   - Send push notifications via Pushover, Pushbullet, or ntfy
   - Alert on mobile when working remotely
   - Include one-tap links to return to session

3. **Smart Home Integration**
   - Trigger smart bulb color changes (Hue, LIFX)
   - Play sounds on smart speakers
   - Flash lights when input needed

4. **Productivity Tracking**
   - Log notification timing to time-tracking systems
   - Calculate "agent wait time" metrics
   - Integrate with productivity dashboards

5. **Context-Aware Notification Routing**
   - Route notifications based on time of day
   - Suppress during focus hours
   - Escalate if no response after timeout

6. **Notification Aggregation**
   - Batch notifications when multiple fire quickly
   - Debounce rapid-fire notifications
   - Summarize notification patterns

### Combinations with Other Hooks

1. **Notification + Stop Hook**
   - Send final summary notification when session ends
   - Include session duration, tool usage stats
   - Archive session transcript link

2. **Notification + PreToolUse**
   - Announce when expensive operations start
   - Alert on potentially long-running commands
   - Notify before destructive operations

3. **Notification + UserPromptSubmit**
   - Confirm prompt received with acknowledgment notification
   - Show estimated response time
   - Queue position for busy systems

### Advanced Applications

1. **Adaptive Notification Behavior**
   - Learn user response patterns
   - Adjust notification urgency based on history
   - Predict optimal notification timing

2. **Multi-Agent Coordination Notifications**
   - Notify when subagents complete tasks
   - Alert on inter-agent communication
   - Dashboard showing agent fleet status

3. **Sentiment-Aware Notifications**
   - Analyze notification content for urgency
   - Adjust tone/priority based on message content
   - Custom sounds for different notification types

### Patterns from Other Domains

1. **GitHub Actions Notifications**
   - Model notification channels after CI/CD systems
   - Support multiple notification targets
   - Configurable notification rules

2. **Monitoring System Alerts (PagerDuty, OpsGenie)**
   - Escalation policies for unresponded notifications
   - On-call rotation integration
   - Incident management workflows

3. **Accessibility Patterns**
   - Screen reader integration
   - Haptic feedback for mobile
   - Visual indicators for deaf/HoH users

---

## 4. Implementation Recommendations

### Best Patterns to Adopt (Ranked)

1. **OS Desktop Notification Sender** - Essential baseline
   - Cross-platform, no dependencies
   - Works in most environments
   - Easy to implement and maintain

2. **Notification Filtering** - Must-have for UX
   - Reduces notification fatigue
   - Simple to implement
   - Significant impact on usability

3. **Multi-Provider TTS with Fallback Chain** - Premium experience
   - Graceful degradation
   - Works offline and online
   - Flexible configuration

4. **Notification Logging** - For debugging
   - Valuable for troubleshooting
   - Low overhead
   - Useful analytics potential

5. **TypeScript SDK Handler** - For type safety
   - Best for complex hook systems
   - Maintainable and extensible
   - Good developer experience

### Patterns to Avoid

1. **Blocking or Modifying Notifications**
   - Notification hook cannot block - don't try
   - Any blocking logic will be ignored

2. **Excessive Network Calls**
   - Notifications fire frequently
   - Heavy network operations will cause lag
   - Cache or queue network requests

3. **Synchronous Long Operations**
   - TTS with network calls should be async/subprocess
   - File operations should be quick
   - Don't block the main thread

### Performance Considerations

- **Target**: <10ms for core notification handling
- **TTS calls**: Run in subprocess to avoid blocking
- **File logging**: Use append mode, batch if needed
- **Network calls**: Make async, use timeouts
- **Filtering**: Do early to skip unnecessary processing

### Testing Approach

1. **Unit Testing**
   - Mock stdin with sample notification JSON
   - Verify output/side effects
   - Test filtering logic

2. **Integration Testing**
   - Trigger actual notifications in Claude Code
   - Verify audio plays (manual)
   - Check desktop notifications appear

3. **Load Testing**
   - Rapid-fire notifications
   - Verify no memory leaks in logging
   - Confirm notification debouncing works

### Sample Configuration

```json
{
  "hooks": {
    "Notification": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "python3 .claude/hooks/notification.py"
          }
        ]
      }
    ]
  }
}
```

### TypeScript/Bun Configuration

```json
{
  "hooks": {
    "Notification": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "bun .claude/hooks/index.ts Notification"
          }
        ]
      }
    ]
  }
}
```

---

## Source Pattern Files

Patterns synthesized from:
- hooks-mastery-part3.yaml (Notification Logging, TTS patterns, Filtering)
- codex-settings.yaml (OS Notification Sender)
- claude-hooks-ts.yaml (TypeScript SDK Handler)
- hooks-evanl1.yaml (no Notification hooks)
- safety-net.yaml (no Notification hooks)
- cc-tools-py.yaml (no Notification hooks)
- cc-tools-go.yaml (no Notification hooks)
- tdd-guard-pre.yaml (no Notification hooks)
- tdd-guard-other.yaml (no Notification hooks)
- awesome.yaml (references to CC Notify, Claudio)
