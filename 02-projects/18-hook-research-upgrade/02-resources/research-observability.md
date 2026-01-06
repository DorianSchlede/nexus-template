# Observability Research Results

## Executive Summary

Observability patterns in Claude Code hooks enable real-time monitoring of agent behavior, tool usage, and session state without blocking execution. The key patterns include: (1) **Fire-and-forget event streaming** - non-blocking HTTP calls to observability servers, (2) **Statusline visualization** - real-time token metrics and context pressure display, and (3) **Notification hooks** - desktop alerts, TTS announcements, and logging. The existing Nexus system already implements a solid fire-and-forget pattern that should be preserved and extended additively.

---

## 1. Event Types to Stream

### 1.1 Tool Call Events
**What**: Every tool call is logged with full context
**Payload**:
```json
{
    "type": "tool_call",
    "tool_name": "Bash",
    "tool_input": {
        "command": "git status"
    },
    "timestamp": "2026-01-01T12:00:00.000Z",
    "session_id": "abc123"
}
```
**Nexus uses this?**: Yes - via `send_event.py` with `--event-type PreToolUse/PostToolUse`
**Current implementation**: Sends to `http://localhost:7777/events` with full payload

### 1.2 Block Events
**What**: When a tool call is blocked by safety guards
**Payload**:
```json
{
    "type": "block",
    "reason": "rm -rf detected",
    "tool_name": "Bash",
    "command": "rm -rf /",
    "timestamp": "2026-01-01T12:00:00.000Z",
    "session_id": "abc123"
}
```
**Nexus uses this?**: No - blocks happen but are not streamed
**Should add?**: Yes - critical for security auditing and understanding blocked actions

### 1.3 Executable Detection Events
**What**: When agent/skill/task/workflow is activated
**Payload** (from Architech pre_tool_use.py):
```json
{
    "type": "agent",
    "executable_id": "meta-architect",
    "target": "architech/00-meta/01-agents/meta-architect/current/meta-architect.md",
    "shortcut": "~meta-architect",
    "detection_method": "bash",
    "timestamp": "2026-01-01T12:00:00.000Z"
}
```
**Endpoint**: `/api/v2/sessions/{session_id}/executable`
**Detection methods**:
- `bash`: Extracted from `shortcut_resolver.py ~shortcut` commands
- `read`: Detected from file path patterns matching `/01-agents/`, `/02-skills/`, etc.

### 1.4 Session Events
**What**: Session lifecycle events (start, end, compact)
**Payload examples**:
```json
// Session Start
{
    "source_app": "nexus",
    "session_id": "abc123",
    "hook_event_type": "SessionStart",
    "timestamp": 1704067200000
}

// Session End (Stop hook)
{
    "source_app": "nexus",
    "session_id": "abc123",
    "hook_event_type": "Stop",
    "timestamp": 1704067800000
}
```
**Nexus uses this?**: Yes - via `send_event.py` with different `--event-type` values

### 1.5 Notification Events
**What**: When Claude wants to notify the user
**Payload** (from Claude Code):
```json
{
    "session_id": "abc123",
    "transcript_path": "/path/to/transcript.jsonl",
    "hook_event_name": "Notification",
    "message": "Claude is waiting for your input",
    "title": "Claude Code"
}
```
**Nexus uses this?**: Partially - notification hooks are configured but not streaming events

---

## 2. Current Nexus Event System

### Endpoints Currently Used
From `send_event.py` and `http.py`:
- **Base URL**: `http://localhost:7777` (via `OBSERVABILITY_SERVER_URL` env var)
- **Events endpoint**: `/events` (main event stream)
- **Health endpoint**: `/health` (server health check)
- **Session executable**: `/api/v2/sessions/{id}/executable` (from Architech reference)

### Event Types Currently Sent
From `send_event.py` argument parsing:
- `PreToolUse` - Before tool execution
- `PostToolUse` - After tool execution
- `SessionStart` - Session initialization
- `Stop` - Session termination
- Custom types via `--event-type` argument

### Fire-and-Forget Pattern
Current implementation from `http.py`:
```python
SERVER_URL = os.environ.get("OBSERVABILITY_SERVER_URL", "http://localhost:7777")
TIMEOUT_SECONDS = 5

def send_to_server(endpoint: str, payload: dict) -> bool:
    """
    Fire-and-forget: Returns True/False, never raises, never blocks long.
    """
    try:
        url = f"{SERVER_URL}{endpoint}"

        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "User-Agent": "Claude-Hook/1.0"
            },
            method="POST"
        )

        with urllib.request.urlopen(req, timeout=TIMEOUT_SECONDS) as response:
            return response.status in (200, 201)

    except urllib.error.URLError as e:
        print(f"[hook] Server connection error: {e}", file=sys.stderr)
        return False
    except urllib.error.HTTPError as e:
        print(f"[hook] Server HTTP error: {e.code}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"[hook] Server error: {e}", file=sys.stderr)
        return False
```

**Key Design Decisions**:
- **5 second timeout**: Prevents blocking if server is down
- **Never raises exceptions**: Observability failures don't break tool execution
- **Silent stderr logging**: Errors are logged but don't affect Claude
- **Standard library only**: Uses `urllib.request`, no external dependencies

### Server Management
From `server.py`:
```python
def ensure_server_running() -> bool:
    """
    Ensure server is running, starting if necessary.
    """
    if check_server_health():
        return True

    print("[hook] Starting observability server...", file=sys.stderr)
    if start_server() and wait_for_ready():
        print("[hook] Server ready", file=sys.stderr)
        return True

    print("[hook] Server unavailable - continuing without observability", file=sys.stderr)
    return False
```

**Auto-start cascade** (in priority order):
1. PM2 (if available)
2. Bun (primary for claude-agent-tracer)
3. npm start
4. Direct node

---

## 3. Statusline Pattern

### Concept
Shows in console:
- Token usage (input/output/cached)
- Git branch + status
- Current context info
- Model identifier

Visual format:
```
[main +] 45.2k in / 12.3k out / 8.1k cached | Project: ontologies-research
```

### Implementation (from cc-tools-go.yaml)

#### Token Metrics from Transcript
```go
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
                    CacheCreationInputTokens  int
                } `json:"usage"`
            } `json:"message"`
            IsSidechain       bool
            IsApiErrorMessage bool
            Timestamp         string
        }

        if json.Unmarshal([]byte(line), &msg) == nil && msg.Message.Usage.InputTokens > 0 {
            metrics.InputTokens += msg.Message.Usage.InputTokens
            metrics.OutputTokens += msg.Message.Usage.OutputTokens
            metrics.CachedTokens += msg.Message.Usage.CacheReadInputTokens
            metrics.CachedTokens += msg.Message.Usage.CacheCreationInputTokens
        }
    }
    return metrics
}
```

#### Context Progress Bar
```go
func (s *Statusline) getContextColors(percentage float64) (string, string, string) {
    switch {
    case percentage < 40.0:
        return s.colors.GreenBG(), s.colors.GreenFG(), s.colors.GreenLightBG()
    case percentage < 60.0:
        return s.colors.YellowBG(), s.colors.YellowFG(), s.colors.YellowLightBG()
    case percentage < 80.0:
        return s.colors.PeachBG(), s.colors.PeachFG(), s.colors.PeachLightBG()
    default:
        return s.colors.RedBG(), s.colors.RedFG(), s.colors.RedLightBG()
    }
}
```

### Python Equivalent
```python
import json
from pathlib import Path
from typing import Dict

def get_token_metrics(transcript_path: str) -> Dict[str, int]:
    """Extract token usage from transcript JSONL."""
    metrics = {"input": 0, "output": 0, "cached": 0, "context_length": 0}
    most_recent_input = 0
    most_recent_cached = 0

    transcript = Path(transcript_path)
    if not transcript.exists():
        return metrics

    with open(transcript, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            try:
                msg = json.loads(line)
                usage = msg.get("message", {}).get("usage", {})

                if usage.get("input_tokens"):
                    metrics["input"] += usage.get("input_tokens", 0)
                    metrics["output"] += usage.get("output_tokens", 0)
                    metrics["cached"] += usage.get("cache_read_input_tokens", 0)
                    metrics["cached"] += usage.get("cache_creation_input_tokens", 0)

                    # Track most recent for context length
                    if not msg.get("isSidechain") and not msg.get("isApiErrorMessage"):
                        most_recent_input = usage.get("input_tokens", 0)
                        most_recent_cached = usage.get("cache_read_input_tokens", 0)
                        most_recent_cached += usage.get("cache_creation_input_tokens", 0)

            except json.JSONDecodeError:
                continue

    metrics["context_length"] = most_recent_input + most_recent_cached
    return metrics


def format_tokens(count: int) -> str:
    """Format token count for display (e.g., 45200 -> '45.2k')."""
    if count >= 1000:
        return f"{count/1000:.1f}k"
    return str(count)


def get_context_color(percentage: float) -> str:
    """Get ANSI color code based on context fill percentage."""
    if percentage < 40.0:
        return "\033[32m"  # Green
    elif percentage < 60.0:
        return "\033[33m"  # Yellow
    elif percentage < 80.0:
        return "\033[38;2;250;179;135m"  # Peach (true color)
    else:
        return "\033[31m"  # Red


def get_context_percentage(context_length: int, model_id: str) -> float:
    """Calculate context window fill percentage."""
    # Model-specific context limits
    if "claude-sonnet-4-5" in model_id and "[1m]" in model_id.lower():
        max_tokens = 1000000  # 1M context
    else:
        max_tokens = 200000   # 200k default

    usable_tokens = int(max_tokens * 0.8)  # 80% usable
    return (context_length / usable_tokens) * 100


def render_statusline(transcript_path: str, model_id: str = "") -> str:
    """Render a statusline string with token metrics."""
    metrics = get_token_metrics(transcript_path)
    reset = "\033[0m"

    percentage = get_context_percentage(metrics["context_length"], model_id)
    color = get_context_color(percentage)

    return (
        f"{color}"
        f"{format_tokens(metrics['input'])} in / "
        f"{format_tokens(metrics['output'])} out / "
        f"{format_tokens(metrics['cached'])} cached"
        f"{reset}"
    )
```

### Display Format
```
[main +] 45.2k in / 12.3k out / 8.1k cached | Project: ontologies-research
```

Components:
- Git branch and status (green/yellow/red based on state)
- Token metrics (input/output/cached)
- Context pressure indicator (color-coded)
- Optional project/workspace name

---

## 4. Notification Patterns

### Desktop Notifications
```python
import os
import subprocess
import sys

def notify(title: str, message: str) -> bool:
    """Send OS-native desktop notification."""
    try:
        if sys.platform == "darwin":
            # macOS
            script = f'display notification "{message}" with title "{title}" sound name "Glass"'
            subprocess.run(["osascript", "-e", script], capture_output=True, timeout=5)
            return True

        elif sys.platform == "win32":
            # Windows PowerShell
            ps_script = f'''
            [Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null
            $template = [Windows.UI.Notifications.ToastTemplateType]::ToastText02
            $xml = [Windows.UI.Notifications.ToastNotificationManager]::GetTemplateContent($template)
            $xml.GetElementsByTagName("text")[0].AppendChild($xml.CreateTextNode("{title}"))
            $xml.GetElementsByTagName("text")[1].AppendChild($xml.CreateTextNode("{message}"))
            $notifier = [Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier("Claude Code")
            $notifier.Show([Windows.UI.Notifications.ToastNotification]::new($xml))
            '''
            subprocess.run(["powershell", "-Command", ps_script], capture_output=True, timeout=5)
            return True

        elif sys.platform.startswith("linux"):
            # Linux notify-send
            subprocess.run(
                ["notify-send", title, message, "-u", "normal", "-i", "terminal"],
                capture_output=True,
                timeout=5
            )
            return True

    except Exception:
        pass

    return False


def terminal_bell():
    """Trigger terminal bell (visual in VSCode)."""
    print('\a', end='', flush=True)
```

### TTS (Text-to-Speech)
**Use Case**: "Task complete" announcement
**Providers** (from research, in priority order):

#### Provider 1: ElevenLabs (highest quality)
```python
# Requires: ELEVENLABS_API_KEY env var
# pip install elevenlabs

import os
from elevenlabs.client import ElevenLabs
from elevenlabs import play

def tts_elevenlabs(text: str):
    api_key = os.getenv('ELEVENLABS_API_KEY')
    client = ElevenLabs(api_key=api_key)

    audio = client.text_to_speech.convert(
        text=text,
        voice_id="WejK3H1m7MI9CHnIjW9K",
        model_id="eleven_turbo_v2_5",
        output_format="mp3_44100_128",
    )
    play(audio)
```

#### Provider 2: OpenAI TTS (good quality, streaming)
```python
# Requires: OPENAI_API_KEY env var
# pip install openai

import asyncio
import os
from openai import AsyncOpenAI
from openai.helpers import LocalAudioPlayer

async def tts_openai(text: str):
    client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    async with client.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice="nova",
        input=text,
        instructions="Speak in a cheerful, positive yet professional tone.",
        response_format="mp3",
    ) as response:
        await LocalAudioPlayer().play(response)
```

#### Provider 3: macOS `say` (offline, simple)
```python
import subprocess
import sys

def tts_macos(text: str):
    if sys.platform == "darwin":
        subprocess.run(["say", text], timeout=30)
```

#### Provider 4: pyttsx3 (offline, cross-platform)
```python
# pip install pyttsx3

import pyttsx3

def tts_pyttsx3(text: str):
    engine = pyttsx3.init()
    engine.setProperty('rate', 180)
    engine.setProperty('volume', 0.8)
    engine.say(text)
    engine.runAndWait()
```

#### Multi-Provider Cascade
```python
import os

def get_tts_function():
    """Select best available TTS provider."""
    if os.getenv('ELEVENLABS_API_KEY'):
        return tts_elevenlabs
    if os.getenv('OPENAI_API_KEY'):
        return tts_openai
    if sys.platform == "darwin":
        return tts_macos
    return tts_pyttsx3  # Fallback
```

---

## 5. Recommended Extensions

### 5.1 Block Event Logging (NEW)
**Purpose**: Track all blocked operations for security auditing
**Implementation**:
```python
from datetime import datetime
from utils.http import send_to_server

def send_block_event(
    session_id: str,
    reason: str,
    tool_name: str,
    details: dict
) -> bool:
    """Stream blocked operation event to observability server."""
    payload = {
        "type": "block",
        "reason": reason,
        "tool_name": tool_name,
        "details": details,
        "timestamp": datetime.now().isoformat()
    }
    return send_to_server(f"/api/v2/sessions/{session_id}/blocks", payload)

# Usage in pre_tool_use.py:
if is_dangerous_rm_command(command):
    send_block_event(session_id, "dangerous_rm", "Bash", {"command": command})
    print("BLOCKED: Dangerous rm command detected", file=sys.stderr)
    sys.exit(2)
```
**Database Impact**: New endpoint, additive (no existing endpoints modified)

### 5.2 Token Metrics Streaming (NEW)
**Purpose**: Track context usage over time for analytics
**Implementation**:
```python
def send_token_metrics(
    session_id: str,
    transcript_path: str
) -> bool:
    """Stream current token metrics to observability server."""
    metrics = get_token_metrics(transcript_path)
    payload = {
        "type": "token_metrics",
        "input_tokens": metrics["input"],
        "output_tokens": metrics["output"],
        "cached_tokens": metrics["cached"],
        "context_length": metrics["context_length"],
        "timestamp": datetime.now().isoformat()
    }
    return send_to_server(f"/api/v2/sessions/{session_id}/metrics", payload)
```
**Trigger**: PostToolUse hook (after each tool call)
**Database Impact**: New endpoint, additive

### 5.3 Audit Trail (NEW)
**Purpose**: Local log of all blocked commands for compliance
**Implementation**:
```python
import json
from pathlib import Path
from datetime import datetime

def write_audit_log(session_id: str, event: dict):
    """Write event to local audit log (JSONL format)."""
    log_dir = Path.home() / ".nexus" / "audit"
    log_dir.mkdir(parents=True, exist_ok=True)

    log_path = log_dir / f"{session_id}.jsonl"
    event["logged_at"] = datetime.now().isoformat()

    with open(log_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(event) + "\n")

# Usage:
write_audit_log(session_id, {
    "type": "block",
    "reason": "dangerous_rm",
    "command": "rm -rf /"
})
```
**Database Impact**: None - local only

### 5.4 Notification Event Streaming (NEW)
**Purpose**: Track notification patterns and response times
**Implementation**:
```python
def stream_notification_event(
    session_id: str,
    message: str,
    title: str = None
) -> bool:
    """Stream notification event to observability server."""
    payload = {
        "type": "notification",
        "message": message,
        "title": title,
        "timestamp": datetime.now().isoformat()
    }
    return send_to_server(f"/api/v2/sessions/{session_id}/notifications", payload)
```
**Database Impact**: New endpoint, additive

---

## 6. Integration Notes

### Must Preserve
These existing patterns MUST NOT be modified:

1. **Fire-and-forget pattern** in `http.py`:
   - 5 second timeout
   - Never raises exceptions
   - Silent failure with stderr logging

2. **All existing send_to_server() calls**:
   - Current `/events` endpoint
   - Current event payload structure

3. **Server auto-start mechanism** in `server.py`:
   - Health check cascade
   - Multi-method server start

4. **Error handling philosophy**:
   - Observability failures never block Claude
   - Exit 0 on any observability error

### Safe to Add
These extensions are additive and safe:

1. **New event types**:
   - Block events (`/api/v2/sessions/{id}/blocks`)
   - Token metrics (`/api/v2/sessions/{id}/metrics`)
   - Notifications (`/api/v2/sessions/{id}/notifications`)

2. **Local audit logging**:
   - No network dependency
   - No blocking on Claude operations

3. **Statusline rendering**:
   - stdout only (no server dependency)
   - Can be triggered from UserPromptSubmit hook

4. **Notification enhancements**:
   - Desktop notifications (non-blocking subprocess)
   - TTS (non-blocking subprocess)

### Performance Budgets
From cc-tools-go research:

| Operation | Target | Notes |
|-----------|--------|-------|
| Fire-and-forget HTTP | <5s timeout | Already implemented |
| Token metrics parsing | <50ms | File I/O bound |
| Statusline rendering | <10ms | String formatting |
| Desktop notification | subprocess | Non-blocking |
| TTS | subprocess | Non-blocking |

---

## 7. Copy-Paste Ready Templates

### Template 1: Stream Block Event
```python
# Add to pre_tool_use.py
from datetime import datetime
from utils.http import send_to_server

def stream_block_event(session_id: str, reason: str, tool_name: str, details: dict):
    """Fire-and-forget block event streaming."""
    send_to_server(f"/api/v2/sessions/{session_id}/blocks", {
        "type": "block",
        "reason": reason,
        "tool_name": tool_name,
        "details": details,
        "timestamp": datetime.now().isoformat()
    })
```

### Template 2: Token Metrics Helper
```python
# Add as utils/metrics.py
import json
from pathlib import Path
from typing import Dict

def get_token_metrics(transcript_path: str) -> Dict[str, int]:
    """Extract token usage from transcript JSONL."""
    metrics = {"input": 0, "output": 0, "cached": 0, "context_length": 0}

    transcript = Path(transcript_path)
    if not transcript.exists():
        return metrics

    try:
        with open(transcript, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    msg = json.loads(line)
                    usage = msg.get("message", {}).get("usage", {})
                    if usage.get("input_tokens"):
                        metrics["input"] += usage.get("input_tokens", 0)
                        metrics["output"] += usage.get("output_tokens", 0)
                        metrics["cached"] += usage.get("cache_read_input_tokens", 0)
                        metrics["cached"] += usage.get("cache_creation_input_tokens", 0)
                except json.JSONDecodeError:
                    continue
    except Exception:
        pass

    return metrics
```

### Template 3: Desktop Notification
```python
# Add as utils/notify.py
import subprocess
import sys

def send_desktop_notification(title: str, message: str):
    """Cross-platform desktop notification (non-blocking)."""
    try:
        if sys.platform == "darwin":
            script = f'display notification "{message}" with title "{title}"'
            subprocess.Popen(["osascript", "-e", script],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        elif sys.platform == "win32":
            # Use toast notification via PowerShell
            subprocess.Popen(["powershell", "-Command",
                f'New-BurntToastNotification -Text "{title}", "{message}"'],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            subprocess.Popen(["notify-send", title, message],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        pass  # Silent failure - notifications are non-critical
```

### Template 4: Audit Log Writer
```python
# Add as utils/audit.py
import json
from pathlib import Path
from datetime import datetime

def write_audit_log(session_id: str, event_type: str, details: dict):
    """Write to local audit log (JSONL). Never raises."""
    try:
        log_dir = Path.home() / ".nexus" / "audit"
        log_dir.mkdir(parents=True, exist_ok=True)

        log_path = log_dir / f"{session_id}.jsonl"
        entry = {
            "type": event_type,
            "details": details,
            "timestamp": datetime.now().isoformat()
        }

        with open(log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
    except Exception:
        pass  # Silent failure - audit is non-critical
```

---

## 8. Sources

### Pattern Files Analyzed
- `patterns/cc-tools-go.yaml` - High-performance Go statusline implementation
- `hook-guides/NOTIFICATION.md` - Desktop alerts, TTS, sound patterns
- `hook-system-reference.system.doc.md` - Section 6: Pre-Tool-Use Hook

### Current Nexus Files Analyzed
- `.claude/hooks/send_event.py` - Event streaming entry point
- `.claude/hooks/utils/http.py` - Fire-and-forget HTTP implementation
- `.claude/hooks/utils/server.py` - Server health check and auto-start

---

*Research completed: 2026-01-01*
*Subagent 3: Observability Research*
