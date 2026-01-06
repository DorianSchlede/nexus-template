# claude-code-hooks-mastery Findings

**Repository:** claude-code-hooks-mastery
**Author:** IndyDevDan
**Source:** https://github.com/indydevdan/claude-code-hooks-mastery
**Analyzed:** 2025-12-31

---

## Key Patterns

### 1. UV Single-File Scripts Architecture
- All hooks use the `uv run` pattern with inline PEP 723 dependency declarations
- Each script is self-contained with embedded dependencies in script comments
- No virtual environment management needed - UV handles dependencies automatically
- Fast execution with lightning-fast dependency resolution

### 2. Graceful Error Handling
- All hooks exit gracefully on any error (JSON decode, exceptions)
- Exit code 0 for success, 2 for blocking actions
- Silent failures prevent hook errors from breaking Claude Code

### 3. Centralized Logging Architecture
- All hooks log to `logs/` directory as JSON arrays
- Consistent pattern: read existing, append, write back
- Separate log files per hook type for easy debugging

### 4. TTS Service Priority Chain
- ElevenLabs (highest priority) > OpenAI > pyttsx3 (offline fallback)
- API key detection determines which service to use
- Graceful degradation if no API keys available

### 5. LLM Service Priority Chain
- OpenAI > Anthropic > Ollama (local) > Random fallback
- Used for generating dynamic completion messages and agent names
- Fastest models chosen for each provider (gpt-4.1-nano, claude-3-5-haiku, gpt-oss:20b)

### 6. Session Data Management
- Sessions stored in `.claude/data/sessions/<session_id>.json`
- Tracks prompts, agent names, and custom metadata
- Auto-generated unique agent names via LLM

---

## Complete settings.json Configuration

```json
{
  "permissions": {
    "allow": [
      "Bash(mkdir:*)",
      "Bash(uv:*)",
      "Bash(find:*)",
      "Bash(mv:*)",
      "Bash(grep:*)",
      "Bash(npm:*)",
      "Bash(ls:*)",
      "Bash(cp:*)",
      "Write",
      "Edit",
      "Bash(chmod:*)",
      "Bash(touch:*)"
    ],
    "deny": []
  },
  "statusLine": {
    "type": "command",
    "command": "uv run .claude/hooks/status_lines/status_line.py",
    "padding": 0
  },
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "uv run .claude/hooks/pre_tool_use.py"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "uv run .claude/hooks/post_tool_use.py"
          }
        ]
      }
    ],
    "Notification": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "uv run .claude/hooks/notification.py --notify"
          }
        ]
      }
    ],
    "Stop": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "uv run .claude/hooks/stop.py --chat"
          }
        ]
      }
    ],
    "SubagentStop": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "uv run .claude/hooks/subagent_stop.py --notify"
          }
        ]
      }
    ],
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "uv run .claude/hooks/user_prompt_submit.py --log-only --store-last-prompt --name-agent"
          }
        ]
      }
    ],
    "PreCompact": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "uv run .claude/hooks/pre_compact.py"
          }
        ]
      }
    ],
    "SessionStart": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "uv run .claude/hooks/session_start.py"
          }
        ]
      }
    ]
  }
}
```

---

## Session Start Pattern

**File:** `.claude/hooks/session_start.py`

### Features
- Logs session start events to `logs/session_start.json`
- Git branch detection via subprocess
- Uncommitted changes count
- Context file loading (.claude/CONTEXT.md, .claude/TODO.md, TODO.md, .github/ISSUE_TEMPLATE.md)
- GitHub issues integration via `gh` CLI
- Optional TTS announcement

### Key Code Pattern

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "python-dotenv",
# ]
# ///

import argparse
import json
import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv is optional


def get_git_status():
    """Get current git status information."""
    try:
        # Get current branch
        branch_result = subprocess.run(
            ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
            capture_output=True,
            text=True,
            timeout=5
        )
        current_branch = branch_result.stdout.strip() if branch_result.returncode == 0 else "unknown"

        # Get uncommitted changes count
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


def load_development_context(source):
    """Load relevant development context based on session source."""
    context_parts = []

    # Add timestamp
    context_parts.append(f"Session started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    context_parts.append(f"Session source: {source}")

    # Add git information
    branch, changes = get_git_status()
    if branch:
        context_parts.append(f"Git branch: {branch}")
        if changes > 0:
            context_parts.append(f"Uncommitted changes: {changes} files")

    # Load project-specific context files if they exist
    context_files = [
        ".claude/CONTEXT.md",
        ".claude/TODO.md",
        "TODO.md",
        ".github/ISSUE_TEMPLATE.md"
    ]

    for file_path in context_files:
        if Path(file_path).exists():
            try:
                with open(file_path, 'r') as f:
                    content = f.read().strip()
                    if content:
                        context_parts.append(f"\n--- Content from {file_path} ---")
                        context_parts.append(content[:1000])  # Limit to first 1000 chars
            except Exception:
                pass

    return "\n".join(context_parts)


def main():
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument('--load-context', action='store_true')
        parser.add_argument('--announce', action='store_true')
        args = parser.parse_args()

        input_data = json.loads(sys.stdin.read())
        session_id = input_data.get('session_id', 'unknown')
        source = input_data.get('source', 'unknown')  # "startup", "resume", or "clear"

        # Log session start
        log_session_start(input_data)

        # Load context if requested
        if args.load_context:
            context = load_development_context(source)
            if context:
                output = {
                    "hookSpecificOutput": {
                        "hookEventName": "SessionStart",
                        "additionalContext": context
                    }
                }
                print(json.dumps(output))
                sys.exit(0)

        sys.exit(0)

    except Exception:
        sys.exit(0)
```

### Session Input Payload
```json
{
  "session_id": "unique-session-id",
  "source": "startup" | "resume" | "clear"
}
```

---

## Pre Tool Use Pattern

**File:** `.claude/hooks/pre_tool_use.py`

### Features
- Blocks dangerous `rm -rf` commands
- Blocks `.env` file access (allows .env.sample)
- Comprehensive regex pattern matching
- Exit code 2 blocks tool execution and shows error to Claude

### Key Code Pattern

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# ///

import json
import sys
import re
from pathlib import Path

def is_dangerous_rm_command(command):
    """Comprehensive detection of dangerous rm commands."""
    normalized = ' '.join(command.lower().split())

    patterns = [
        r'\brm\s+.*-[a-z]*r[a-z]*f',  # rm -rf, rm -fr, rm -Rf
        r'\brm\s+.*-[a-z]*f[a-z]*r',  # rm -fr variations
        r'\brm\s+--recursive\s+--force',
        r'\brm\s+--force\s+--recursive',
        r'\brm\s+-r\s+.*-f',
        r'\brm\s+-f\s+.*-r',
    ]

    for pattern in patterns:
        if re.search(pattern, normalized):
            return True

    # Check for recursive flag with dangerous paths
    dangerous_paths = [
        r'/', r'/\*', r'~', r'~/', r'\$HOME',
        r'\.\.', r'\*', r'\.', r'\.\s*$',
    ]

    if re.search(r'\brm\s+.*-[a-z]*r', normalized):
        for path in dangerous_paths:
            if re.search(path, normalized):
                return True

    return False


def is_env_file_access(tool_name, tool_input):
    """Check if any tool is trying to access .env files."""
    if tool_name in ['Read', 'Edit', 'MultiEdit', 'Write', 'Bash']:
        if tool_name in ['Read', 'Edit', 'MultiEdit', 'Write']:
            file_path = tool_input.get('file_path', '')
            if '.env' in file_path and not file_path.endswith('.env.sample'):
                return True

        elif tool_name == 'Bash':
            command = tool_input.get('command', '')
            env_patterns = [
                r'\b\.env\b(?!\.sample)',
                r'cat\s+.*\.env\b(?!\.sample)',
                r'echo\s+.*>\s*\.env\b(?!\.sample)',
                r'touch\s+.*\.env\b(?!\.sample)',
                r'cp\s+.*\.env\b(?!\.sample)',
                r'mv\s+.*\.env\b(?!\.sample)',
            ]

            for pattern in env_patterns:
                if re.search(pattern, command):
                    return True

    return False


def main():
    try:
        input_data = json.load(sys.stdin)
        tool_name = input_data.get('tool_name', '')
        tool_input = input_data.get('tool_input', {})

        # Block .env file access
        if is_env_file_access(tool_name, tool_input):
            print("BLOCKED: Access to .env files is prohibited", file=sys.stderr)
            print("Use .env.sample for template files instead", file=sys.stderr)
            sys.exit(2)  # Exit code 2 blocks tool call

        # Block dangerous rm commands
        if tool_name == 'Bash':
            command = tool_input.get('command', '')
            if is_dangerous_rm_command(command):
                print("BLOCKED: Dangerous rm command detected", file=sys.stderr)
                sys.exit(2)

        # Log and continue
        log_to_file(input_data)
        sys.exit(0)

    except Exception:
        sys.exit(0)
```

### Tool Input Payload
```json
{
  "tool_name": "Bash",
  "tool_input": {
    "command": "rm -rf /tmp/test"
  }
}
```

---

## Other Hook Patterns

### Post Tool Use Hook

**Purpose:** Log tool execution results, convert transcripts to JSON

```python
def main():
    try:
        input_data = json.load(sys.stdin)

        # Log to logs/post_tool_use.json
        log_dir = Path.cwd() / 'logs'
        log_dir.mkdir(parents=True, exist_ok=True)
        log_path = log_dir / 'post_tool_use.json'

        # Read existing, append, write back
        log_data = load_log(log_path)
        log_data.append(input_data)
        save_log(log_path, log_data)

        sys.exit(0)
    except Exception:
        sys.exit(0)
```

### Pre-Compact Hook

**Purpose:** Backup transcripts before compaction

```python
def backup_transcript(transcript_path, trigger):
    """Create a backup of the transcript before compaction."""
    backup_dir = Path("logs") / "transcript_backups"
    backup_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    session_name = Path(transcript_path).stem
    backup_name = f"{session_name}_pre_compact_{trigger}_{timestamp}.jsonl"
    backup_path = backup_dir / backup_name

    import shutil
    shutil.copy2(transcript_path, backup_path)
    return str(backup_path)
```

**Input Payload:**
```json
{
  "session_id": "...",
  "transcript_path": "/path/to/transcript.jsonl",
  "trigger": "manual" | "auto",
  "custom_instructions": "..."
}
```

### Stop Hook

**Purpose:** TTS announcement on completion, save chat transcript

```python
def get_llm_completion_message():
    """Generate completion message using available LLM services."""
    script_dir = Path(__file__).parent
    llm_dir = script_dir / "utils" / "llm"

    # Try OpenAI first
    if os.getenv('OPENAI_API_KEY'):
        result = subprocess.run(["uv", "run", str(llm_dir / "oai.py"), "--completion"], ...)
        if result.returncode == 0:
            return result.stdout.strip()

    # Try Anthropic
    if os.getenv('ANTHROPIC_API_KEY'):
        result = subprocess.run(["uv", "run", str(llm_dir / "anth.py"), "--completion"], ...)
        if result.returncode == 0:
            return result.stdout.strip()

    # Try Ollama (local)
    result = subprocess.run(["uv", "run", str(llm_dir / "ollama.py"), "--completion"], ...)
    if result.returncode == 0:
        return result.stdout.strip()

    # Fallback to random message
    return random.choice(["Work complete!", "All done!", "Task finished!"])
```

### Subagent Stop Hook

**Purpose:** Simple TTS "Subagent Complete" announcement

```python
def announce_subagent_completion():
    tts_script = get_tts_script_path()
    if tts_script:
        subprocess.run(["uv", "run", tts_script, "Subagent Complete"], ...)
```

### User Prompt Submit Hook

**Purpose:** Log prompts, manage session data, generate agent names

```python
def manage_session_data(session_id, prompt, name_agent=False):
    """Manage session data in JSON structure."""
    sessions_dir = Path(".claude/data/sessions")
    sessions_dir.mkdir(parents=True, exist_ok=True)

    session_file = sessions_dir / f"{session_id}.json"

    # Load or create session
    if session_file.exists():
        session_data = json.load(open(session_file))
    else:
        session_data = {"session_id": session_id, "prompts": []}

    # Add prompt
    session_data["prompts"].append(prompt)

    # Generate agent name if requested
    if name_agent and "agent_name" not in session_data:
        # Try Ollama -> Anthropic -> Fallback
        name = generate_agent_name()
        session_data["agent_name"] = name

    # Save
    json.dump(session_data, open(session_file, 'w'), indent=2)
```

### Notification Hook

**Purpose:** TTS alert when agent needs input

```python
def announce_notification():
    engineer_name = os.getenv('ENGINEER_NAME', '').strip()

    # 30% chance to include name
    if engineer_name and random.random() < 0.3:
        notification_message = f"{engineer_name}, your agent needs your input"
    else:
        notification_message = "Your agent needs your input"

    tts_script = get_tts_script_path()
    subprocess.run(["uv", "run", tts_script, notification_message], ...)
```

---

## Utility Functions

### TTS Service Selection

```python
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
```

### ElevenLabs TTS Script

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# dependencies = [
#     "elevenlabs",
#     "python-dotenv",
# ]
# ///

from elevenlabs.client import ElevenLabs
from elevenlabs import play

def main():
    api_key = os.getenv('ELEVENLABS_API_KEY')
    elevenlabs = ElevenLabs(api_key=api_key)

    text = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "The first move is what sets everything in motion."

    audio = elevenlabs.text_to_speech.convert(
        text=text,
        voice_id="WejK3H1m7MI9CHnIjW9K",
        model_id="eleven_turbo_v2_5",
        output_format="mp3_44100_128",
    )
    play(audio)
```

### OpenAI TTS Script

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# dependencies = [
#     "openai",
#     "openai[voice_helpers]",
#     "python-dotenv",
# ]
# ///

async def main():
    from openai import AsyncOpenAI
    from openai.helpers import LocalAudioPlayer

    openai = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    text = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "Default text"

    async with openai.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice="nova",
        input=text,
        instructions="Speak in a cheerful, positive yet professional tone.",
        response_format="mp3",
    ) as response:
        await LocalAudioPlayer().play(response)
```

### pyttsx3 TTS Script (Offline Fallback)

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# dependencies = [
#     "pyttsx3",
# ]
# ///

def main():
    import pyttsx3

    engine = pyttsx3.init()
    engine.setProperty('rate', 180)
    engine.setProperty('volume', 0.8)

    text = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "Work complete!"
    engine.say(text)
    engine.runAndWait()
```

### LLM Prompt Function (OpenAI)

```python
def prompt_llm(prompt_text):
    """Base OpenAI LLM prompting method using fastest model."""
    from openai import OpenAI

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    response = client.chat.completions.create(
        model="gpt-4.1-nano",  # Fastest OpenAI model
        messages=[{"role": "user", "content": prompt_text}],
        max_tokens=100,
        temperature=0.7,
    )

    return response.choices[0].message.content.strip()
```

### LLM Prompt Function (Anthropic)

```python
def prompt_llm(prompt_text):
    """Base Anthropic LLM prompting method using fastest model."""
    import anthropic

    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    message = client.messages.create(
        model="claude-3-5-haiku-20241022",  # Fastest Anthropic model
        max_tokens=100,
        temperature=0.7,
        messages=[{"role": "user", "content": prompt_text}],
    )

    return message.content[0].text.strip()
```

### LLM Prompt Function (Ollama - Local)

```python
def prompt_llm(prompt_text):
    """Base Ollama LLM prompting using OpenAI-compatible API."""
    from openai import OpenAI

    client = OpenAI(
        base_url="http://localhost:11434/v1",
        api_key="ollama",  # required but unused
    )

    model = os.getenv("OLLAMA_MODEL", "gpt-oss:20b")

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt_text}],
        max_tokens=1000,
    )

    return response.choices[0].message.content.strip()
```

### Agent Name Generation

```python
def generate_agent_name():
    """Generate a one-word agent name."""
    example_names = [
        "Phoenix", "Sage", "Nova", "Echo", "Atlas", "Cipher", "Nexus",
        "Oracle", "Quantum", "Zenith", "Aurora", "Vortex", "Nebula"
    ]

    prompt_text = """Generate exactly ONE unique agent/assistant name.

Requirements:
- Single word only (no spaces, hyphens, or punctuation)
- Abstract and memorable
- Professional sounding
- Easy to pronounce

Respond with ONLY the name, nothing else."""

    try:
        response = prompt_llm(prompt_text)
        name = response.strip().split()[0]
        name = ''.join(c for c in name if c.isalnum())
        name = name.capitalize()

        if name and 3 <= len(name) <= 20:
            return name
    except:
        pass

    return random.choice(example_names)
```

### JSON Logging Pattern

```python
def log_to_file(log_path, input_data):
    """Consistent logging pattern used across all hooks."""
    log_dir = Path.cwd() / 'logs'
    log_dir.mkdir(parents=True, exist_ok=True)

    # Read existing log data or initialize empty list
    if log_path.exists():
        with open(log_path, 'r') as f:
            try:
                log_data = json.load(f)
            except (json.JSONDecodeError, ValueError):
                log_data = []
    else:
        log_data = []

    # Append new data
    log_data.append(input_data)

    # Write back with formatting
    with open(log_path, 'w') as f:
        json.dump(log_data, f, indent=2)
```

---

## Dependencies

### Core Dependencies (All Hooks)
- **python-dotenv** - Environment variable loading from .env files
- **Python 3.8+** (some hooks require 3.11+)

### TTS Dependencies
- **elevenlabs** - ElevenLabs TTS API
- **openai[voice_helpers]** - OpenAI TTS with LocalAudioPlayer
- **pyttsx3** - Offline TTS (no API required)

### LLM Dependencies
- **openai** - OpenAI API client
- **anthropic** - Anthropic API client
- **openai** (for Ollama) - Uses OpenAI-compatible API

### Environment Variables
```bash
ANTHROPIC_API_KEY=       # Anthropic API key
ELEVENLABS_API_KEY=      # ElevenLabs TTS API key
ENGINEER_NAME=           # Engineer name for personalized messages
OLLAMA_HOST=             # Ollama server host (default: localhost:11434)
OLLAMA_MODEL=            # Ollama model (default: gpt-oss:20b)
OPENAI_API_KEY=          # OpenAI API key
```

---

## Notes for Implementation

### 1. UV Script Header Pattern
Every hook should start with:
```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# dependencies = [
#     "python-dotenv",
# ]
# ///
```

### 2. Exit Code Semantics
- **Exit 0**: Success, continue normally
- **Exit 2**: Block action, show stderr to Claude/user
- **Other**: Non-blocking error, show stderr to user

### 3. Hook Blocking Capabilities
| Hook | Can Block |
|------|-----------|
| UserPromptSubmit | Yes - blocks prompts |
| PreToolUse | Yes - blocks tool execution |
| PostToolUse | No - tool already executed |
| Notification | No |
| Stop | Yes - forces continuation |
| SubagentStop | Yes - blocks subagent stop |
| PreCompact | No |
| SessionStart | No |

### 4. JSON Output Control
Hooks can return structured JSON for advanced control:
```json
{
  "continue": true,
  "stopReason": "string",
  "suppressOutput": true,
  "decision": "approve" | "block",
  "reason": "Explanation"
}
```

### 5. Status Line Integration
- Configure in settings.json under `statusLine`
- Receives session data via stdin as JSON
- First line of stdout becomes the status line
- Can include ANSI color codes

### 6. Session Data Structure
```json
{
  "session_id": "unique-id",
  "prompts": ["prompt1", "prompt2"],
  "agent_name": "Phoenix",
  "extras": {
    "project": "myapp",
    "status": "debugging"
  }
}
```

### 7. Hook Execution Environment
- 60-second timeout per hook
- All matching hooks run in parallel
- Inherits Claude Code environment variables
- Runs in current project directory
- Input via stdin, output via stdout/stderr

### 8. Error Handling Best Practice
Always wrap main logic in try/except and exit gracefully:
```python
try:
    # main logic
    sys.exit(0)
except json.JSONDecodeError:
    sys.exit(0)
except Exception:
    sys.exit(0)
```

---

## File Structure Reference

```
.claude/
├── settings.json              # Hook configuration
├── hooks/
│   ├── session_start.py       # Session initialization
│   ├── pre_tool_use.py        # Security blocking
│   ├── post_tool_use.py       # Result logging
│   ├── pre_compact.py         # Transcript backup
│   ├── stop.py                # Completion announcement
│   ├── subagent_stop.py       # Subagent completion
│   ├── user_prompt_submit.py  # Prompt logging
│   ├── notification.py        # Input needed alerts
│   └── utils/
│       ├── tts/
│       │   ├── elevenlabs_tts.py
│       │   ├── openai_tts.py
│       │   └── pyttsx3_tts.py
│       └── llm/
│           ├── oai.py
│           ├── anth.py
│           └── ollama.py
├── status_lines/
│   ├── status_line.py         # Basic status
│   ├── status_line_v2.py      # Smart prompts
│   ├── status_line_v3.py      # Agent sessions
│   └── status_line_v4.py      # Extended metadata
├── data/
│   └── sessions/              # Session JSON files
└── agents/                    # Sub-agent definitions

logs/
├── session_start.json
├── pre_tool_use.json
├── post_tool_use.json
├── pre_compact.json
├── stop.json
├── subagent_stop.json
├── user_prompt_submit.json
├── notification.json
├── status_line.json
├── chat.json                  # Transcript (overwritten each session)
└── transcript_backups/        # Pre-compaction backups
```
