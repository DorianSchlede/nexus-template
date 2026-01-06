# Current Nexus Hook System Analysis

## Executive Summary

The Nexus Hook System is a comprehensive Claude Code extension that provides observability, safety controls, and context management for AI agent sessions. It connects to an external observability server at `http://localhost:7777` via fire-and-forget HTTP POST requests, tracking session lifecycle events, executable loading (agents/skills/tasks/workflows), and Claude's message streams. The system also provides local logging, TTS notifications, and automatic context loading through the nexus-loader integration.

---

## System Architecture

### Data Flow Diagram

```
                                 CLAUDE CODE RUNTIME
                                         |
    +------------------------------------+------------------------------------+
    |                                    |                                    |
    v                                    v                                    v
+----------------+              +----------------+              +----------------+
| SESSION HOOKS  |              |  TOOL HOOKS    |              |  STOP HOOKS    |
+----------------+              +----------------+              +----------------+
| session_start  |              | pre_tool_use   |              | stop           |
| session_end    |              | post_tool_use  |              | subagent_stop  |
+----------------+              | user_prompt    |              | notification   |
        |                       +----------------+              +----------------+
        |                               |                               |
        v                               v                               v
+-----------------------------------------------------------------------+
|                           UTILITY LAYER                                |
+-----------------------------------------------------------------------+
| http.py          - Fire-and-forget POST to server                      |
| server.py        - Health check and auto-start server                  |
| constants.py     - Log directory paths                                 |
| registry.py      - Shortcut lookup for executable detection            |
| summarizer.py    - LLM-powered event summaries (uses anth.py)          |
+-----------------------------------------------------------------------+
        |
        v
+-----------------------------------------------------------------------+
|                      OBSERVABILITY SERVER                              |
|                   http://localhost:7777                                |
+-----------------------------------------------------------------------+
| Endpoints:                                                             |
|   POST /api/v2/sessions/{id}/start       - Session start event         |
|   POST /api/v2/sessions/{id}/end         - Session end event           |
|   POST /api/v2/sessions/{id}/executable  - Agent/skill/task loaded     |
|   POST /api/v2/sessions/{id}/transcript  - Full JSONL transcript       |
|   POST /api/v2/session/{id}/meta         - Session summary/metadata    |
|   GET  /api/v2/sessions/{id}             - Get session info            |
|   GET  /api/v2/sessions/{id}/executables - Get session executables     |
|   POST /events                           - Generic event streaming     |
|   GET  /health                           - Health check                |
+-----------------------------------------------------------------------+
```

### Database Connection

- **Server URL**: `http://localhost:7777` (from `OBSERVABILITY_SERVER_URL` env var)
- **Timeout**: 5 seconds for HTTP requests
- **Protocol**: HTTP POST with JSON body, fire-and-forget pattern
- **Error Handling**: Silent failure - never blocks Claude Code operations

---

## Hook File Analysis

### 1. session_start.py

**Trigger**: New session start, resume, /clear command, or after compaction
**Purpose**: Initialize session, run nexus-loader to populate context cache, inject mandatory read instructions into Claude's context
**Database Events**:
- Endpoint: `POST /api/v2/sessions/{session_id}/start`
- Payload:
```json
{
  "source_app": "mutagent-obsidian",
  "source": "startup|resume|clear|compact",
  "timestamp": "ISO 8601"
}
```

**Dependencies**:
- `utils/http.py` (send_to_server)
- `utils/server.py` (ensure_server_running)
- `00-system/core/nexus-loader.py` (external)

**Key Functions**:
- `run_nexus_loader(session_id, resume_mode)`: Executes nexus-loader.py subprocess with --startup or --resume flag
- `read_cache_file(session_id)`: Reads context_startup.json cache and returns slim summary
- `main()`: Orchestrates session initialization, writes session file, outputs mandatory context injection

**Output**: Prints `<NexusContext>` block with mandatory file read instruction to stdout (becomes additionalContext)

**Critical Behavior**:
- Writes session tracking file to `.claude/sessions/{hash}.session`
- Calls `ensure_server_running()` to auto-start observability server if needed
- Exit code 0 always (never blocks)

---

### 2. pre_tool_use.py

**Trigger**: Before every tool call (Read, Bash, Edit, Write, etc.)
**Purpose**: Safety checks (block dangerous commands), executable detection and streaming, local logging
**Database Events**:
- Endpoint: `POST /api/v2/sessions/{session_id}/executable`
- Payload:
```json
{
  "type": "agent|skill|task|workflow",
  "executable_id": "meta-architect",
  "target": "/path/to/file.md",
  "shortcut": "~meta-architect",
  "detection_method": "bash|read",
  "timestamp": "ISO 8601"
}
```

**Current Safety Checks**:
- [x] Block .env file access (prevents reading sensitive credentials)
- [x] Block dangerous rm -rf commands (prevents accidental file deletion)

**Dependencies**:
- `utils/constants.py` (ensure_session_log_dir)
- `utils/http.py` (send_to_server)
- `utils/registry.py` (lookup_shortcut, detect_type_from_path, extract_id_from_path)

**Key Functions**:
- `detect_executable(tool_name, tool_input)`: Detects if tool call is loading an agent/skill/task/workflow
- `parse_shortcut_for_type(shortcut)`: Extracts type and id from ~shortcut syntax
- `detect_from_path_patterns(file_path)`: Fallback detection from file paths
- `stream_executable(executable, session_id)`: Sends executable event to server
- `is_dangerous_rm_command(command)`: Comprehensive rm -rf detection
- `is_env_file_access(tool_name, tool_input)`: Detects .env file access attempts

**Exit Codes**:
- 0 = allow tool call
- 2 = block tool call and show error to Claude

**Local Logging**: Appends to `logs/{session_id}/pre_tool_use.json`

---

### 3. post_tool_use.py

**Trigger**: After every tool call completes
**Purpose**: Local logging only (no database events)
**Database Events**: NONE

**Dependencies**:
- `utils/constants.py` (ensure_session_log_dir)

**Key Functions**:
- `main()`: Reads input, appends to log file

**Local Logging**: Appends to `logs/{session_id}/post_tool_use.json`

**Exit Codes**: Always 0

---

### 4. user_prompt_submit.py

**Trigger**: When user submits a prompt
**Purpose**: Log user prompts, optional validation (currently no active blocks)
**Database Events**: NONE

**Dependencies**:
- `utils/constants.py` (ensure_session_log_dir)

**Key Functions**:
- `log_user_prompt(session_id, input_data)`: Writes to session log
- `validate_prompt(prompt)`: Validates prompt against blocked patterns (currently empty)

**Local Logging**: Appends to `logs/{session_id}/user_prompt_submit.json`

**Exit Codes**:
- 0 = allow prompt
- 2 = block prompt (if validation enabled)

---

### 5. stop.py

**Trigger**: When Claude's turn ends (main agent)
**Purpose**: Log stop events, TTS completion announcement, optional transcript copy
**Database Events**: NONE (local only)

**Dependencies**:
- `utils/constants.py` (ensure_session_log_dir)
- `utils/tts/*.py` (TTS scripts)
- `utils/llm/anth.py` and `utils/llm/oai.py` (for LLM-generated completion messages)

**Key Functions**:
- `get_tts_script_path()`: Priority: ElevenLabs > OpenAI > pyttsx3
- `get_llm_completion_message()`: Priority: Anthropic > OpenAI > random fallback
- `announce_completion()`: Plays TTS completion message

**Local Logging**: Appends to `logs/{session_id}/stop.json`

**Special Features**:
- `--chat` flag copies transcript to `chat.json`
- TTS notification on completion

---

### 6. subagent_stop.py

**Trigger**: When a subagent's turn ends
**Purpose**: Log subagent stop events, TTS notification
**Database Events**: NONE

**Dependencies**:
- `utils/constants.py` (ensure_session_log_dir)
- `utils/tts/*.py` (TTS scripts)

**Key Functions**:
- `announce_subagent_completion()`: Fixed message "Subagent Complete"

**Local Logging**: Appends to `logs/{session_id}/subagent_stop.json`

---

### 7. notification.py

**Trigger**: When Claude needs user input
**Purpose**: Log notification events, optional TTS alert
**Database Events**: NONE

**Dependencies**:
- `utils/constants.py` (ensure_session_log_dir)
- `utils/tts/*.py` (TTS scripts)

**Key Functions**:
- `announce_notification()`: Says "Your agent needs your input" (30% chance includes engineer name)

**Local Logging**: Appends to `logs/{session_id}/notification.json`

**Special Behavior**: Skips TTS for generic "Claude is waiting for your input" message

---

### 8. send_event.py

**Trigger**: Called as CLI tool by other scripts
**Purpose**: Generic event dispatcher to observability server
**Database Events**:
- Endpoint: `POST http://localhost:7777/events`
- Payload:
```json
{
  "source_app": "<from --source-app>",
  "session_id": "<from input>",
  "hook_event_type": "<from --event-type>",
  "payload": "<stdin JSON>",
  "timestamp": "<epoch ms>",
  "chat": "[optional, if --add-chat]",
  "summary": "[optional, if --summarize]"
}
```

**Dependencies**:
- `utils/summarizer.py` (generate_event_summary)

**Key Functions**:
- `send_event_to_server(event_data, server_url)`: POST to /events endpoint

**CLI Arguments**:
- `--source-app` (required): Application name
- `--event-type` (required): Hook event type
- `--server-url`: Override server URL
- `--add-chat`: Include transcript
- `--summarize`: Generate AI summary of event

**Exit Codes**: Always 0 (never blocks)

---

### 9. save_resume_state.py

**Trigger**: PreCompact hook (before context compaction)
**Purpose**: Save resume state to `_resume.md` for active project
**Database Events**: NONE

**Dependencies**:
- None (standalone)

**Key Functions**:
- `find_nexus_root()`: Gets project directory from CLAUDE_PROJECT_DIR
- `cleanup_session_cache(nexus_root, session_id)`: Deletes session-specific cache
- `load_cache_context(nexus_root)`: Reads context_startup.json
- `get_active_project(cache_context)`: Finds first IN_PROGRESS project
- `parse_transcript_for_skill(transcript_path)`: Extracts last --skill invocation
- `skill_to_phase(skill_name)`: Maps skill to phase (analysis/synthesis/execution/planning)
- `write_resume_file(...)`: Writes _resume.md with YAML frontmatter

**Output**: Prints `<NexusResumeContext>` with mandatory next step instruction

---

### 10. session_end.py

**Trigger**: /clear, logout, exit, or other termination
**Purpose**: Cleanup caches, send session end event, capture transcript
**Database Events**:
- Endpoint: `POST /api/v2/sessions/{session_id}/end`
- Payload:
```json
{
  "reason": "clear|logout|prompt_input_exit|other",
  "timestamp": "ISO 8601"
}
```
- Endpoint: `POST /api/v2/sessions/{session_id}/transcript`
- Payload:
```json
{
  "transcript": "<full JSONL content>",
  "format": "jsonl",
  "timestamp": "ISO 8601"
}
```

**Dependencies**:
- `utils/http.py` (send_to_server)

**Key Functions**:
- `save_transcript_locally(session_id, transcript_path)`: Backup to `logs/{session_id}/transcript.jsonl`
- `cleanup_session_cache(session_id)`: Delete session-specific Nexus cache
- `cleanup_stale_caches(max_age_minutes)`: Delete orphaned caches > 60 min old
- `send_transcript_to_server(session_id, transcript_path)`: POST full transcript

---

### 11. session_summary.py

**Trigger**: Stop hook (after session ends)
**Purpose**: Generate AI summary of session using Gemini, post to backend
**Database Events**:
- GET: `/api/v2/sessions/{session_id}` - Fetch session info
- GET: `/api/v2/sessions/{session_id}/executables` - Fetch loaded executables
- POST: `/api/v2/session/{session_id}/meta` - Post summary (note: singular "session" not "sessions")
- Payload:
```json
{
  "agent_name": "meta-architect",
  "agent_version": "1.0",
  "summary": "<Gemini-generated summary>",
  "generated_at": "ISO 8601",
  "generator": "gemini-2.5-flash"
}
```

**Dependencies**:
- `google-generativeai` (Gemini SDK)

**Key Functions**:
- `get_session_executables(session_id)`: GET from backend
- `get_session_info(session_id)`: GET from backend
- `generate_summary_gemini(executables, session_info)`: Generate 2-3 sentence summary
- `send_summary_to_server(session_id, summary, primary_agent)`: POST to backend

**External API**: Google Gemini API (uses hardcoded API key as fallback)

---

### 12. shortcut_resolver.py

**Trigger**: Called as CLI tool for ~shortcut resolution
**Purpose**: Resolve ~shortcuts to file paths using registry
**Database Events**: NONE

**Dependencies**:
- `pyyaml` (for registry parsing)

**Key Functions**:
- `ShortcutResolver.__init__()`: Loads registry from `.architech/navigation/shortcut-registry.yaml`
- `resolve(shortcut, feature)`: Returns file path for shortcut
- `validate_shortcut(shortcut)`: Check if shortcut exists in registry
- `load_content(shortcut, feature, warn_large_files)`: Resolve and load file content

**CLI Arguments**:
- `shortcut`: The ~shortcut to resolve
- `--feature`: Feature name for feature-specific shortcuts
- `--validate`: Validate shortcut exists
- `--content`: Return file content
- `--content-only`: Return only content
- `--json`: Return JSON with path, content, metadata
- `--max-size`: Maximum file size limit
- `--quiet`: Suppress warnings

---

### 13. stream_claude_message.py

**Trigger**: PostToolUse hook
**Purpose**: Stream Claude's latest message content to server
**Database Events**:
- Endpoint: `POST /events`
- Payload:
```json
{
  "source_app": "claude-code",
  "session_id": "<session_id>",
  "hook_event_type": "claude_message",
  "payload": {
    "type": "claude_message",
    "content": "<Claude's text>",
    "content_length": 1234,
    "after_tool": "Read",
    "tool_use_id": "abc123",
    "tool_calls_in_message": ["Read", "Bash"],
    "message_index": 5,
    "conversation_stats": {"user": 3, "assistant": 3, "system": 1},
    "total_entries": 7,
    "timestamp": "ISO 8601"
  },
  "chat": [{"role": "assistant", "content": "<truncated to 5000 chars>"}]
}
```

**Dependencies**:
- `utils/http.py` (send_to_server)

**Key Functions**:
- `parse_transcript(transcript_path)`: Parse JSONL file
- `extract_latest_claude_message(entries)`: Find last assistant message with text
- `count_messages_by_type(entries)`: Count user/assistant/system messages

---

## Utility Analysis

### http.py - Database Connection

**Server URL**: `http://localhost:7777` (from `OBSERVABILITY_SERVER_URL` env var)
**Timeout**: 5 seconds
**Error Handling**: Silent failure - logs to stderr but returns False
**Pattern**: Fire-and-forget (never blocks or raises)

**Key Function**:
```python
def send_to_server(endpoint: str, payload: dict) -> bool:
    # POST to {SERVER_URL}{endpoint} with JSON body
    # Returns True on 200/201, False on any error
```

### server.py - Server Auto-Start

**Server URL**: `http://localhost:7777` (from `OBSERVABILITY_SERVER_URL` env var)
**Startup Timeout**: 10 seconds
**Health Check**: GET `/health` with 2 second timeout

**Start Methods** (in priority order):
1. PM2: `pm2 start observability-server --silent`
2. Bun: `bun run {server_dir}/apps/server/src/index.ts`
3. npm: `npm start --prefix {server_dir}`
4. Node: `node {server_dir}/dist/index.js`

**Key Functions**:
- `check_server_health()`: GET /health
- `start_server()`: Try each start method
- `wait_for_ready(timeout)`: Poll until healthy
- `ensure_server_running()`: Health check, start if needed

### registry.py - Shortcut Lookup

**Registry Path**: `.architech/navigation/shortcut-registry.yaml`
**Caching**: Caches registry with mtime check for reloads

**Entity Type Patterns**:
```python
{
    "agent": r"/01-agents/",
    "skill": r"/02-skills/",
    "task": r"/03-tasks/",
    "workflow": r"/04-workflows/",
}
```

**Key Functions**:
- `load_registry()`: Load and cache YAML registry
- `detect_type_from_path(path)`: Match against patterns
- `extract_id_from_path(path)`: Extract entity ID from path
- `lookup_shortcut(shortcut)`: Returns `{"type", "id", "path"}` or None

### constants.py - Log Directory

**Base Directory**: `logs/` (from `CLAUDE_HOOKS_LOG_DIR` env var)

**Key Functions**:
- `get_session_log_dir(session_id)`: Returns `logs/{session_id}`
- `ensure_session_log_dir(session_id)`: Creates directory if needed

### summarizer.py - Event Summaries

**Dependencies**: `utils/llm/anth.py` (Anthropic Claude Haiku)

**Key Function**:
```python
def generate_event_summary(event_data: Dict) -> Optional[str]:
    # Uses Claude 3.5 Haiku to generate 1-sentence summary
    # Returns None if API call fails
```

---

## Critical Paths (DO NOT BREAK)

### Database Event Flow

```
1. Hook triggers (session_start, pre_tool_use, session_end, etc.)
2. Hook imports utils/http.py
3. Calls send_to_server(endpoint, payload)
4. http.py POSTs to http://localhost:7777{endpoint}
5. Returns True/False (never raises/blocks)
```

### Files That Send to Database

| File | Sends to Database | Endpoint(s) |
|------|-------------------|-------------|
| session_start.py | YES | `/api/v2/sessions/{id}/start` |
| pre_tool_use.py | YES | `/api/v2/sessions/{id}/executable` |
| post_tool_use.py | NO | - |
| user_prompt_submit.py | NO | - |
| stop.py | NO | - |
| subagent_stop.py | NO | - |
| notification.py | NO | - |
| send_event.py | YES | `/events` |
| save_resume_state.py | NO | - |
| session_end.py | YES | `/api/v2/sessions/{id}/end`, `/api/v2/sessions/{id}/transcript` |
| session_summary.py | YES | GET `/api/v2/sessions/{id}`, GET `/api/v2/sessions/{id}/executables`, POST `/api/v2/session/{id}/meta` |
| shortcut_resolver.py | NO | - |
| stream_claude_message.py | YES | `/events` |

---

## Integration Points

### With nexus-loader.py

- `session_start.py` executes `nexus-loader.py` via subprocess
- Passes `--startup` or `--resume` flag based on source
- Passes `--session {session_id}` for cache isolation
- Reads resulting cache file for slim summary injection

### With External Server (Observability)

**Server**: `http://localhost:7777` (claude-agent-tracer)
**Data Sent**:
- Session lifecycle events (start, end)
- Executable loading events (agent, skill, task, workflow)
- Full transcripts on session end
- Claude message streams
- AI-generated session summaries

### With External APIs

- **Anthropic API**: Used by `utils/llm/anth.py` for completion messages and summaries
- **OpenAI API**: Used by `utils/llm/oai.py` as fallback
- **Google Gemini API**: Used by `session_summary.py` for session summaries
- **ElevenLabs API**: Used by TTS for voice notifications
- **OpenAI TTS**: Fallback TTS

---

## All API Endpoints Summary

### POST Endpoints

| Endpoint | Payload | Source File |
|----------|---------|-------------|
| `POST /api/v2/sessions/{id}/start` | `{source_app, source, timestamp}` | session_start.py |
| `POST /api/v2/sessions/{id}/end` | `{reason, timestamp}` | session_end.py |
| `POST /api/v2/sessions/{id}/executable` | `{type, executable_id, target, shortcut, detection_method, timestamp}` | pre_tool_use.py |
| `POST /api/v2/sessions/{id}/transcript` | `{transcript, format, timestamp}` | session_end.py |
| `POST /api/v2/session/{id}/meta` | `{agent_name, agent_version, summary, generated_at, generator}` | session_summary.py |
| `POST /events` | `{source_app, session_id, hook_event_type, payload, timestamp, chat?, summary?}` | send_event.py, stream_claude_message.py |

### GET Endpoints

| Endpoint | Purpose | Source File |
|----------|---------|-------------|
| `GET /health` | Server health check | server.py |
| `GET /api/v2/sessions/{id}` | Get session info | session_summary.py |
| `GET /api/v2/sessions/{id}/executables` | Get session executables | session_summary.py |

---

## Recommendations for Safe Upgrades

### Safe to Modify (No Database Impact)

- `post_tool_use.py` - Local logging only
- `user_prompt_submit.py` - Local logging only
- `stop.py` - TTS and local logging only
- `subagent_stop.py` - TTS and local logging only
- `notification.py` - TTS and local logging only
- `save_resume_state.py` - Local file operations only
- `shortcut_resolver.py` - File path resolution only
- `utils/constants.py` - Constants only
- `utils/registry.py` - Local registry parsing only
- `utils/tts/*.py` - Voice synthesis only
- `utils/llm/*.py` - LLM API calls (not to observability server)

### Dangerous to Modify (Database Connection)

- `session_start.py` - Sends session start events
- `pre_tool_use.py` - Sends executable detection events
- `session_end.py` - Sends session end and transcript events
- `session_summary.py` - Fetches data and sends summaries
- `send_event.py` - Generic event dispatcher
- `stream_claude_message.py` - Streams Claude messages
- `utils/http.py` - Core HTTP transport layer
- `utils/server.py` - Server auto-start logic
- `utils/summarizer.py` - Uses external API (Anthropic)

### Must Preserve

1. **All `/api/v2/` endpoint calls** - These are the contract with the observability backend
2. **Fire-and-forget pattern in http.py** - Never block Claude Code operations
3. **Exit code conventions**:
   - 0 = allow (continue operation)
   - 2 = block (show error to Claude)
4. **Session ID propagation** - All database calls use session_id from input
5. **Timestamp formats** - ISO 8601 for timestamps
6. **Server URL configuration** - `OBSERVABILITY_SERVER_URL` environment variable
7. **Safety checks in pre_tool_use.py** - .env blocking and rm -rf blocking

---

## Environment Variables

| Variable | Default | Used By |
|----------|---------|---------|
| `OBSERVABILITY_SERVER_URL` | `http://localhost:7777` | http.py, server.py, session_summary.py |
| `OBSERVABILITY_SERVER_DIR` | `../architech/claude-agent-tracer` | server.py |
| `CLAUDE_PROJECT_DIR` | (none) | session_start.py, save_resume_state.py |
| `CLAUDE_HOOKS_LOG_DIR` | `logs` | constants.py |
| `ANTHROPIC_API_KEY` | (required) | utils/llm/anth.py, summarizer.py |
| `OPENAI_API_KEY` | (optional) | utils/llm/oai.py, TTS |
| `ELEVENLABS_API_KEY` | (optional) | TTS |
| `GEMINI_API_KEY` | (hardcoded fallback) | session_summary.py |
| `ENGINEER_NAME` | (optional) | notification.py, anth.py |

---

## Success Checklist

- [x] All 13 hook files documented
- [x] All 5 utility files documented
- [x] Database connection fully mapped (http.py, server.py)
- [x] All event types listed with payloads (8 endpoints total)
- [x] Clear "safe to modify" vs "dangerous" classification
- [x] Data flow diagram showing database connection
- [x] Environment variables documented
- [x] Exit code conventions documented
- [x] Integration points identified (nexus-loader, observability server, external APIs)
