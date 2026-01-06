# Claude Code Hooks - Complete Use Case Catalog

A comprehensive inventory of all use cases found across Claude Code hook ecosystem repositories.

---

## 1. Overview

### Summary Statistics

| Metric | Value |
|--------|-------|
| **Total Use Cases** | 127 |
| **Source Repositories** | 15 |
| **Hook Types Covered** | 8 |

### Distribution by Hook Type

| Hook Type | Use Cases | Percentage |
|-----------|-----------|------------|
| PreToolUse | 52 | 41% |
| PostToolUse | 24 | 19% |
| SessionStart | 12 | 9% |
| Notification | 11 | 9% |
| Stop | 8 | 6% |
| UserPromptSubmit | 9 | 7% |
| SubagentStop | 5 | 4% |
| PreCompact | 4 | 3% |
| StatusLine | 2 | 2% |

### Distribution by Category

| Category | Use Cases | Percentage |
|----------|-----------|------------|
| Safety | 38 | 30% |
| Quality | 28 | 22% |
| Observability | 22 | 17% |
| Communication | 16 | 13% |
| Context | 12 | 9% |
| Productivity | 8 | 6% |
| Coordination | 3 | 2% |

---

## 2. Use Case Table (Complete)

| # | Use Case | Hook Type | Source Repo | Category | Complexity |
|---|----------|-----------|-------------|----------|------------|
| 1 | Block rm -rf commands | PreToolUse | hooks-mastery | Safety | medium |
| 2 | Block rm -rf root/home paths | PreToolUse | safety-net | Safety | high |
| 3 | Block .env file access | PreToolUse | hooks-mastery | Safety | medium |
| 4 | Block git checkout -- (pathspec) | PreToolUse | safety-net | Safety | medium |
| 5 | Block git restore (worktree) | PreToolUse | safety-net | Safety | low |
| 6 | Block git reset --hard | PreToolUse | safety-net | Safety | low |
| 7 | Block git clean -f | PreToolUse | safety-net | Safety | low |
| 8 | Block git push --force | PreToolUse | safety-net | Safety | low |
| 9 | Block git branch -D (force delete) | PreToolUse | safety-net | Safety | low |
| 10 | Block git stash drop/clear | PreToolUse | safety-net | Safety | low |
| 11 | Block find -delete patterns | PreToolUse | safety-net | Safety | medium |
| 12 | Block xargs rm -rf | PreToolUse | safety-net | Safety | high |
| 13 | Block parallel rm -rf | PreToolUse | safety-net | Safety | high |
| 14 | Block interpreter one-liners with destructive code | PreToolUse | safety-net | Safety | medium |
| 15 | Shell wrapper recursive analysis | PreToolUse | safety-net | Safety | high |
| 16 | Protected branch deletion blocking | PreToolUse | evanl1 | Safety | medium |
| 17 | Block --no-verify flag usage | PreToolUse | evanl1 | Safety | medium |
| 18 | Dangerous AWS operations warning | PreToolUse | evanl1 | Safety | medium |
| 19 | npm suspicious package warning | PreToolUse | evanl1 | Safety | low |
| 20 | Secret detection in commits | PreToolUse | awesome | Safety | medium |
| 21 | Test validation before commit | PreToolUse | awesome | Safety | medium |
| 22 | Build validation before commit | PreToolUse | awesome | Safety | medium |
| 23 | Pre-commit lint blocking | PreToolUse | awesome | Safety | medium |
| 24 | Security scan on file changes | PostToolUse | awesome | Safety | medium |
| 25 | TDD validation gate | PreToolUse | tdd-guard | Safety | high |
| 26 | Zod schema input validation | PreToolUse | tdd-guard | Safety | medium |
| 27 | Dangerous command blocking (Claude hooks TS) | PreToolUse | claude-hooks-ts | Safety | low |
| 28 | Dangerous prompt blocking | UserPromptSubmit | claude-hooks-ts | Safety | low |
| 29 | Git commit confirmation modal | PreToolUse | codex-settings | Safety | medium |
| 30 | PR creation confirmation modal | PreToolUse | codex-settings | Safety | medium |
| 31 | rm TRASH pattern (move instead of delete) | PreToolUse | cc-tools-py | Safety | low |
| 32 | Git add smart staging (tiered protection) | PreToolUse | cc-tools-py | Safety | high |
| 33 | Git checkout uncommitted warning | PreToolUse | cc-tools-py | Safety | medium |
| 34 | Git commit ask permission | PreToolUse | cc-tools-py | Safety | low |
| 35 | Environment file protection (env-safe CLI suggestion) | PreToolUse | cc-tools-py | Safety | low |
| 36 | Strict mode fail-closed | PreToolUse | safety-net | Safety | low |
| 37 | Paranoid rm mode | PreToolUse | safety-net | Safety | low |
| 38 | Secret redaction in logs | PreToolUse | safety-net | Safety | medium |
| 39 | Ripgrep over grep enforcer | PreToolUse | codex-settings | Quality | low |
| 40 | Whitespace line cleaner | PostToolUse | codex-settings | Quality | low |
| 41 | Python docstring formatter (Google style) | PostToolUse | codex-settings | Quality | high |
| 42 | Python ruff quality gate | PostToolUse | codex-settings | Quality | medium |
| 43 | Prettier auto-formatter | PostToolUse | codex-settings | Quality | low |
| 44 | Markdown code block formatter | PostToolUse | codex-settings | Quality | high |
| 45 | Bash script formatter | PostToolUse | codex-settings | Quality | low |
| 46 | TypeScript type checking hook | PostToolUse | awesome | Quality | medium |
| 47 | Pre-edit type blocking | PreToolUse | awesome | Quality | medium |
| 48 | Auto-format hook (Prettier) | PostToolUse | awesome | Quality | low |
| 49 | ESLint auto-fix hook | PostToolUse | awesome | Quality | low |
| 50 | British English conversion (Britfix) | PostToolUse | awesome | Quality | medium |
| 51 | TypeScript quality hooks (SHA256 caching) | PostToolUse | awesome | Quality | high |
| 52 | Lint notification block (Refactor phase) | PreToolUse | tdd-guard | Quality | medium |
| 53 | AI-powered TDD compliance validator | PreToolUse | tdd-guard | Quality | high |
| 54 | Rust mod.rs restriction | PreToolUse | evanl1 | Quality | low |
| 55 | Naming restrictions (no test.py, temp.txt) | PreToolUse | evanl1 | Quality | medium |
| 56 | Python uv enforcer | PreToolUse | evanl1 | Quality | low |
| 57 | Commit message filter (no Claude signatures) | PreToolUse | evanl1 | Quality | low |
| 58 | Docker image naming enforcement | PreToolUse | evanl1 | Quality | low |
| 59 | Cargo format reminder | PreToolUse | evanl1 | Quality | low |
| 60 | Java build check (wrapper usage) | PreToolUse | evanl1 | Quality | medium |
| 61 | Validation helpers (runtime response checking) | N/A (utility) | claude-hooks-ts | Quality | medium |
| 62 | Dependency injection testability pattern | N/A (utility) | cc-tools-go | Quality | high |
| 63 | Graceful error handling pattern | PostToolUse | hooks-mastery | Quality | low |
| 64 | File length limit speed bump | PreToolUse | cc-tools-py | Quality | medium |
| 65 | Session logging | SessionStart | hooks-mastery | Observability | low |
| 66 | PreToolUse event logging | PreToolUse | hooks-mastery | Observability | low |
| 67 | PostToolUse event logging | PostToolUse | hooks-mastery | Observability | low |
| 68 | Pre-compact event logging | PreCompact | hooks-mastery | Observability | low |
| 69 | Stop event logging | Stop | hooks-mastery | Observability | low |
| 70 | SubagentStop event logging | SubagentStop | hooks-mastery | Observability | low |
| 71 | Notification logging | Notification | hooks-mastery | Observability | low |
| 72 | Prompt logging and auditing | UserPromptSubmit | hooks-mastery | Observability | low |
| 73 | Command logger (daily JSON files) | PreToolUse | evanl1 | Observability | low |
| 74 | Dev event notifier (categorized events) | PreToolUse | evanl1 | Observability | medium |
| 75 | File stats after edits | PostToolUse | evanl1 | Observability | medium |
| 76 | Transcript export to JSON | Stop | hooks-mastery | Observability | low |
| 77 | Subagent transcript export | SubagentStop | hooks-mastery | Observability | low |
| 78 | Audit logging per session | PreToolUse | safety-net | Observability | low |
| 79 | Session state persistence (JSONL) | All | claude-hooks-ts | Observability | low |
| 80 | File edit logger | PreToolUse | claude-hooks-ts | Observability | low |
| 81 | File write success logger | PostToolUse | claude-hooks-ts | Observability | low |
| 82 | Session end logger | Stop | claude-hooks-ts | Observability | low |
| 83 | Powerline statusline (context bar) | StatusLine | cc-tools-py | Observability | medium |
| 84 | High-performance Go statusline | Status | cc-tools-go | Observability | high |
| 85 | Context progress bar (token usage) | Status | cc-tools-go | Observability | medium |
| 86 | OS desktop notification sender | Notification | codex-settings | Communication | low |
| 87 | TTS session announcement | SessionStart | hooks-mastery | Communication | low |
| 88 | TTS completion announcement (LLM-generated) | Stop | hooks-mastery | Communication | medium |
| 89 | Cascading TTS provider selection | Stop | hooks-mastery | Communication | low |
| 90 | Subagent completion TTS notification | SubagentStop | hooks-mastery | Communication | low |
| 91 | TTS audio alert on input request | Notification | hooks-mastery | Communication | medium |
| 92 | Notification filtering (smart) | Notification | hooks-mastery | Communication | low |
| 93 | Multi-provider TTS (ElevenLabs) | Notification | hooks-mastery | Communication | low |
| 94 | Multi-provider TTS (OpenAI streaming) | Notification | hooks-mastery | Communication | medium |
| 95 | Offline TTS fallback (pyttsx3) | Notification | hooks-mastery | Communication | low |
| 96 | Personalized notification messages | Notification | hooks-mastery | Communication | low |
| 97 | Desktop notifications (CC Notify) | Stop | awesome | Communication | low |
| 98 | Audio feedback (Claudio) | Stop | awesome | Communication | low |
| 99 | Terminal UI beautifier | UserPromptSubmit | evanl1 | Communication | low |
| 100 | Development context injection | SessionStart | hooks-mastery | Context | medium |
| 101 | Git status extraction | SessionStart | hooks-mastery | Context | low |
| 102 | GitHub issues integration | SessionStart | hooks-mastery | Context | low |
| 103 | Transcript backup before compaction | PreCompact | hooks-mastery | Context | low |
| 104 | Session state reset | SessionStart | tdd-guard | Context | low |
| 105 | Default instructions initialization | SessionStart | tdd-guard | Context | low |
| 106 | Multi-source context assembly | PreToolUse | tdd-guard | Context | medium |
| 107 | Multi-language file type detection | PreToolUse | tdd-guard | Context | low |
| 108 | Session source detection | SessionStart | claude-hooks-ts | Context | low |
| 109 | Pre-compact trigger logger | PreCompact | claude-hooks-ts | Context | low |
| 110 | Transcript reader utilities | All (utility) | claude-hooks-ts | Context | medium |
| 111 | Shell command splitting (quote-aware) | PreToolUse | safety-net | Context | medium |
| 112 | Wrapper stripping (sudo/env/command) | PreToolUse | safety-net | Context | medium |
| 113 | WebFetch to Tavily redirect | PreToolUse | codex-settings | Productivity | low |
| 114 | WebSearch to Tavily redirect | PreToolUse | codex-settings | Productivity | low |
| 115 | Tavily extract depth upgrader | PreToolUse | codex-settings | Productivity | low |
| 116 | Marketplace to plugin sync | PostToolUse | codex-settings | Productivity | medium |
| 117 | Auto context file injection | UserPromptSubmit | claude-hooks-ts | Productivity | low |
| 118 | LLM agent name generation | UserPromptSubmit | hooks-mastery | Productivity | medium |
| 119 | File pattern ignore gate | PreToolUse | tdd-guard | Productivity | low |
| 120 | Guard toggle state check | PreToolUse | tdd-guard | Productivity | low |
| 121 | User command toggle (tdd-guard on/off) | UserPromptSubmit | tdd-guard | Productivity | low |
| 122 | Resume trigger clipboard | UserPromptSubmit | cc-tools-py | Productivity | medium |
| 123 | Subagent stop guard (loop prevention) | SubagentStop | claude-hooks-ts | Coordination | low |
| 124 | Multi-agent communication (HCOM) | SubagentStop | awesome | Coordination | medium |
| 125 | Unified hook router | PostToolUse | tdd-guard | Coordination | medium |
| 126 | Type-safe hook runner | All | claude-hooks-ts | SDK | medium |
| 127 | Typed handler registry | All | claude-hooks-ts | SDK | low |

---

## 3. Categories Deep-Dive

### 3.1 Safety Use Cases

Safety hooks protect against destructive operations, data loss, and security vulnerabilities.

#### Blocking Dangerous Operations

| Use Case | Hook Type | Source | Technique |
|----------|-----------|--------|-----------|
| Block rm -rf commands | PreToolUse | hooks-mastery | Regex pattern matching on command variants |
| Block rm -rf root/home paths | PreToolUse | safety-net | Intelligent path analysis, allows temp/cwd paths |
| Block .env file access | PreToolUse | hooks-mastery | File path and bash command pattern matching |
| Block git checkout -- (pathspec) | PreToolUse | safety-net | Detects double-dash pathspec that discards changes |
| Block git restore (worktree) | PreToolUse | safety-net | Allows --staged, blocks default restore |
| Block git reset --hard | PreToolUse | safety-net | Prevents destruction of uncommitted changes |
| Block git clean -f | PreToolUse | safety-net | Prevents removal of untracked files |
| Block git push --force | PreToolUse | safety-net | Allows --force-with-lease, blocks naked --force |
| Block git branch -D | PreToolUse | safety-net | Case-sensitive detection (-D vs -d) |
| Block git stash drop/clear | PreToolUse | safety-net | Protects stashed work |
| Block find -delete | PreToolUse | safety-net | Parses find args, skips -exec blocks |
| Block xargs rm -rf | PreToolUse | safety-net | Extracts child command, handles replacement mode |
| Block parallel rm -rf | PreToolUse | safety-net | Expands {} placeholders, analyzes rm commands |
| Shell wrapper analysis | PreToolUse | safety-net | Recursive analysis up to 5 levels (bash -c) |
| Interpreter one-liner detection | PreToolUse | safety-net | Detects destructive patterns in Python/Node/Ruby |

#### Git Safety

| Use Case | Hook Type | Source | Technique |
|----------|-----------|--------|-----------|
| Protected branch deletion | PreToolUse | evanl1 | Regex on git push origin :branch and git branch -d |
| Block --no-verify flag | PreToolUse | evanl1 | Excludes quoted contexts |
| Git commit confirmation | PreToolUse | codex-settings | Parses heredoc, shows staged files |
| PR creation confirmation | PreToolUse | codex-settings | Resolves @me to username |
| Git add smart staging | PreToolUse | cc-tools-py | Tiered: block dangerous, ask modified, allow new |
| Git checkout uncommitted warning | PreToolUse | cc-tools-py | Shows file list, suggests stash/commit |
| Git commit ask permission | PreToolUse | cc-tools-py | Uses permissionDecision: "ask" |

#### Code Quality Enforcement

| Use Case | Hook Type | Source | Technique |
|----------|-----------|--------|-----------|
| TDD validation gate | PreToolUse | tdd-guard | AI model validates TDD compliance |
| Secret detection | PreToolUse | awesome | Scans for API keys, passwords |
| Test/build validation | PreToolUse | awesome | Runs tests/build before commits |

### 3.2 Quality Use Cases

Quality hooks enforce code standards, formatting, and best practices.

#### Auto-Formatting

| Use Case | Hook Type | Source | Technique |
|----------|-----------|--------|-----------|
| Prettier auto-formatter | PostToolUse | codex-settings | Runs prettier --write on JS/TS/CSS/JSON |
| Python ruff quality gate | PostToolUse | codex-settings | ruff check --fix + ruff format |
| Whitespace line cleaner | PostToolUse | codex-settings | sed to strip whitespace-only lines |
| Python docstring formatter | PostToolUse | codex-settings | AST-based Google style formatting |
| Bash script formatter | PostToolUse | codex-settings | prettier-plugin-sh |
| Markdown code block formatter | PostToolUse | codex-settings | Extracts blocks, formats with ruff/prettier |
| British English conversion | PostToolUse | awesome (Britfix) | Context-aware, only comments/docstrings |
| TypeScript quality hooks | PostToolUse | awesome | TSC + ESLint + Prettier with SHA256 caching |

#### Linting & Type Checking

| Use Case | Hook Type | Source | Technique |
|----------|-----------|--------|-----------|
| ESLint auto-fix | PostToolUse | awesome | eslint --fix after edits |
| TypeScript type checking | PostToolUse | awesome | tsc --noEmit, feedback via additionalContext |
| Pre-edit type blocking | PreToolUse | awesome | Blocks edits if type errors exist |
| Lint notification block | PreToolUse | tdd-guard | Two-phase: warn first, block on repeat |
| Post-tool lint enforcement | PostToolUse | tdd-guard | ESLint on modified files, tracks notification state |

#### Code Standards

| Use Case | Hook Type | Source | Technique |
|----------|-----------|--------|-----------|
| Ripgrep over grep enforcer | PreToolUse | codex-settings | Blocks grep, suggests rg alternatives |
| Rust mod.rs restriction | PreToolUse | evanl1 | Enforces modern module organization |
| Naming restrictions | PreToolUse | evanl1 | Blocks test.py, temp1.txt, foo.js |
| Python uv enforcer | PreToolUse | evanl1 | Blocks pip/python, suggests uv commands |
| Commit message filter | PreToolUse | evanl1 | Blocks Claude auto-generated signatures |
| Docker image naming | PreToolUse | evanl1 | Blocks -v2/-test suffixes, suggests tags |
| File length limit | PreToolUse | cc-tools-py | Speed bump at 10,000 lines |

### 3.3 Productivity Use Cases

Productivity hooks automate workflows, provide shortcuts, and enhance developer experience.

#### Tool Redirection

| Use Case | Hook Type | Source | Technique |
|----------|-----------|--------|-----------|
| WebFetch to Tavily redirect | PreToolUse | codex-settings | Denies WebFetch, guides to mcp__tavily |
| WebSearch to Tavily redirect | PreToolUse | codex-settings | Denies WebSearch, guides to mcp__tavily |
| Tavily extract depth upgrader | PreToolUse | codex-settings | Modifies input to set extract_depth='advanced' |

#### Session Management

| Use Case | Hook Type | Source | Technique |
|----------|-----------|--------|-----------|
| Resume trigger clipboard | UserPromptSubmit | cc-tools-py | Detects >resume, copies session_id to clipboard |
| User command toggle | UserPromptSubmit | tdd-guard | "tdd-guard on/off" controls enforcement |
| Guard toggle state check | PreToolUse | tdd-guard | Early exit when guard disabled |
| Auto context file injection | UserPromptSubmit | claude-hooks-ts | Adds test files when prompt mentions "test" |

#### Code Generation

| Use Case | Hook Type | Source | Technique |
|----------|-----------|--------|-----------|
| LLM agent name generation | UserPromptSubmit | hooks-mastery | Ollama/Anthropic generates unique agent names |
| Marketplace to plugin sync | PostToolUse | codex-settings | Syncs marketplace.json to individual plugin.json |
| File pattern ignore gate | PreToolUse | tdd-guard | Skips validation for *.md, *.json, etc. |

### 3.4 Communication Use Cases

Communication hooks provide notifications, audio alerts, and user feedback.

#### Text-to-Speech

| Use Case | Hook Type | Source | Technique |
|----------|-----------|--------|-----------|
| TTS session announcement | SessionStart | hooks-mastery | Different messages for startup/resume/clear |
| TTS completion announcement | Stop | hooks-mastery | LLM-generated dynamic messages |
| Subagent completion TTS | SubagentStop | hooks-mastery | Fixed "Subagent Complete" message |
| TTS audio alert on input | Notification | hooks-mastery | Announces when Claude needs input |
| Cascading TTS provider | Stop | hooks-mastery | ElevenLabs > OpenAI > pyttsx3 |
| ElevenLabs Turbo v2.5 | Notification | hooks-mastery | High-quality voice synthesis |
| OpenAI streaming TTS | Notification | hooks-mastery | gpt-4o-mini-tts with LocalAudioPlayer |
| pyttsx3 offline fallback | Notification | hooks-mastery | Cross-platform offline TTS |

#### Desktop Notifications

| Use Case | Hook Type | Source | Technique |
|----------|-----------|--------|-----------|
| OS notification sender | Notification | codex-settings | osascript (macOS), notify-send (Linux) |
| CC Notify integration | Stop | awesome | One-click jump to VS Code, task duration |
| Claudio audio feedback | Stop | awesome | OS-native sounds |

#### User Interface

| Use Case | Hook Type | Source | Technique |
|----------|-----------|--------|-----------|
| Personalized notifications | Notification | hooks-mastery | ENGINEER_NAME in 30% of messages |
| Notification filtering | Notification | hooks-mastery | Skips generic "waiting for input" |
| Terminal UI beautifier | UserPromptSubmit | evanl1 | ANSI box drawing, timestamp, mode |

### 3.5 Coordination Use Cases

Coordination hooks manage multi-agent workflows and state.

| Use Case | Hook Type | Source | Technique |
|----------|-----------|--------|-----------|
| Subagent stop guard | SubagentStop | claude-hooks-ts | Checks stop_hook_active to prevent loops |
| Multi-agent communication | SubagentStop | awesome (HCOM) | @-mention targeting, live dashboard |
| Unified hook router | PostToolUse | tdd-guard | Single entry dispatches to specialized handlers |
| Session data management | UserPromptSubmit | hooks-mastery | Per-session JSON files with prompt history |

### 3.6 Context Use Cases

Context hooks load, manage, and preserve session state.

#### Session Context Loading

| Use Case | Hook Type | Source | Technique |
|----------|-----------|--------|-----------|
| Development context injection | SessionStart | hooks-mastery | Git status, TODO.md, CONTEXT.md, GitHub issues |
| Git status extraction | SessionStart | hooks-mastery | git rev-parse, git status --porcelain |
| GitHub issues integration | SessionStart | hooks-mastery | gh issue list --limit 5 |
| Session source detection | SessionStart | claude-hooks-ts | Detects VSCode/web/terminal source |
| Session state reset | SessionStart | tdd-guard | Clears transient data, preserves config |
| Default instructions init | SessionStart | tdd-guard | Creates TDD rules file if missing |

#### Context Preservation

| Use Case | Hook Type | Source | Technique |
|----------|-----------|--------|-----------|
| Transcript backup | PreCompact | hooks-mastery | Timestamped copy before compaction |
| Session state persistence | All | claude-hooks-ts | Appends to session-specific JSON files |
| Pre-compact trigger logger | PreCompact | claude-hooks-ts | Logs manual vs auto triggers |

#### Context Utilities

| Use Case | Hook Type | Source | Technique |
|----------|-----------|--------|-----------|
| Transcript reader utilities | All | claude-hooks-ts | Stream-based JSONL parsing |
| Multi-source context assembly | PreToolUse | tdd-guard | Parallel fetch from storage sources |
| Shell command splitting | PreToolUse | safety-net | Quote-aware parsing on ;, &&, ||, | |
| Wrapper stripping | PreToolUse | safety-net | Strips sudo, env, command prefixes |

### 3.7 Observability Use Cases

Observability hooks provide logging, metrics, and debugging capabilities.

#### Event Logging

| Use Case | Hook Type | Source | Technique |
|----------|-----------|--------|-----------|
| Session logging | SessionStart | hooks-mastery | JSON array file append |
| PreToolUse logging | PreToolUse | hooks-mastery | Full input data to JSON |
| PostToolUse logging | PostToolUse | hooks-mastery | Tool name, input, and response |
| Pre-compact logging | PreCompact | hooks-mastery | Trigger type (manual/auto) |
| Stop event logging | Stop | hooks-mastery | Session end tracking |
| SubagentStop logging | SubagentStop | hooks-mastery | Delegated task completion |
| Notification logging | Notification | hooks-mastery | All notification events |
| Prompt logging | UserPromptSubmit | hooks-mastery | Full input data for audit |
| Command logger | PreToolUse | evanl1 | Daily JSON files at ~/.claude/logs/ |
| Audit logging per session | PreToolUse | safety-net | JSONL in ~/.cc-safety-net/logs/ |

#### Transcript Export

| Use Case | Hook Type | Source | Technique |
|----------|-----------|--------|-----------|
| Transcript to JSON | Stop | hooks-mastery | JSONL to formatted JSON array |
| Subagent transcript export | SubagentStop | hooks-mastery | Same as Stop hook |

#### Status Display

| Use Case | Hook Type | Source | Technique |
|----------|-----------|--------|-----------|
| Powerline statusline | StatusLine | cc-tools-py | jq parsing, ANSI colors, context bar |
| Go statusline | Status | cc-tools-go | Sub-ms rendering, git/k8s/AWS context |
| Context progress bar | Status | cc-tools-go | Color-coded token usage (green/yellow/red) |
| Git status (file-based) | Status | cc-tools-go | Reads .git/HEAD directly, no subprocess |

#### Analytics

| Use Case | Hook Type | Source | Technique |
|----------|-----------|--------|-----------|
| Dev event notifier | PreToolUse | evanl1 | Categorizes build/test/deploy/code/security |
| File stats after edits | PostToolUse | evanl1 | Lines, chars, functions, classes by language |
| Transcript token parsing | Status | cc-tools-go | Accumulates input/output/cached tokens |

---

## 4. Hook Type Distribution

### 4.1 PreToolUse (52 use cases)

The most common hook type, used for:
- **Safety blocking** - Preventing dangerous operations (28 use cases)
- **Quality enforcement** - Blocking violations before they occur (12 use cases)
- **Observability** - Logging tool calls (8 use cases)
- **Productivity** - Tool redirection (4 use cases)

**Top 3 Use Cases:**
1. Block rm -rf commands (Safety)
2. Block .env file access (Safety)
3. PreToolUse event logging (Observability)

**Unique Capabilities:**
- `permissionDecision: deny` - Block tool execution
- `permissionDecision: ask` - Trigger confirmation dialog
- `permissionDecision: allow` - Bypass permission system
- `updatedInput` - Modify tool inputs silently

### 4.2 PostToolUse (24 use cases)

Used for:
- **Auto-formatting** - Running formatters after edits (8 use cases)
- **Logging** - Recording tool results (6 use cases)
- **Quality gates** - Validating outputs (5 use cases)
- **Sync operations** - Triggering side effects (3 use cases)
- **Feedback** - Providing guidance to Claude (2 use cases)

**Top 3 Use Cases:**
1. Prettier auto-formatter (Quality)
2. PostToolUse event logging (Observability)
3. Python ruff quality gate (Quality)

**Unique Capabilities:**
- Access to `tool_response` - See what the tool returned
- `decision: block` + `reason` - Prompt Claude to retry
- Silent file modification - Fix issues automatically

### 4.3 SessionStart (12 use cases)

Used for:
- **Context loading** - Inject project state (6 use cases)
- **Session logging** - Track session lifecycle (3 use cases)
- **Initialization** - Set up defaults (2 use cases)
- **Announcements** - Audio notifications (1 use case)

**Top 3 Use Cases:**
1. Development context injection (Context)
2. Session logging (Observability)
3. Git status extraction (Context)

**Unique Capabilities:**
- `additionalContext` - Inject context into Claude's system prompt
- Access to `source` field - Know if startup/resume/clear

### 4.4 Notification (11 use cases)

Used for:
- **Audio alerts** - TTS notifications (6 use cases)
- **Desktop notifications** - OS-level alerts (2 use cases)
- **Logging** - Track notification events (2 use cases)
- **Filtering** - Skip generic messages (1 use case)

**Top 3 Use Cases:**
1. TTS audio alert on input (Communication)
2. OS desktop notification sender (Communication)
3. Notification logging (Observability)

**Unique Capabilities:**
- Triggered when Claude needs user input
- Access to `message` field for filtering

### 4.5 Stop (8 use cases)

Used for:
- **Completion announcements** - TTS and desktop alerts (4 use cases)
- **Logging** - Session end tracking (2 use cases)
- **Export** - Transcript conversion (2 use cases)

**Top 3 Use Cases:**
1. TTS completion announcement (Communication)
2. Stop event logging (Observability)
3. Transcript export to JSON (Observability)

**Unique Capabilities:**
- Access to full `transcript_path` for export
- Final opportunity to process session data

### 4.6 UserPromptSubmit (9 use cases)

Used for:
- **Prompt filtering** - Block dangerous prompts (2 use cases)
- **Prompt enhancement** - Add context files (2 use cases)
- **Session management** - Track prompts (2 use cases)
- **Command handling** - Toggle settings (2 use cases)
- **UI enhancement** - Terminal beautification (1 use case)

**Top 3 Use Cases:**
1. Prompt logging and auditing (Observability)
2. Auto context file injection (Productivity)
3. User command toggle (Productivity)

**Unique Capabilities:**
- `contextFiles` - Add glob patterns to Claude's context
- `updatedPrompt` - Modify the prompt before processing
- `decision: block` - Prevent prompt from reaching Claude

### 4.7 SubagentStop (5 use cases)

Used for:
- **Logging** - Track subagent completion (2 use cases)
- **Notifications** - Audio alerts (1 use case)
- **Coordination** - Multi-agent communication (1 use case)
- **Loop prevention** - Check stop_hook_active (1 use case)

**Top 3 Use Cases:**
1. Subagent stop logging (Observability)
2. Subagent completion TTS (Communication)
3. Multi-agent communication (Coordination)

**Unique Capabilities:**
- `stop_hook_active` - Prevent infinite hook loops
- Distinct from main Stop for subagent tracking

### 4.8 PreCompact (4 use cases)

Used for:
- **Logging** - Track compaction events (2 use cases)
- **Backup** - Preserve full transcript (1 use case)
- **Feedback** - Show compaction details (1 use case)

**Top 3 Use Cases:**
1. Pre-compact event logging (Observability)
2. Transcript backup before compaction (Context)
3. Pre-compact verbose feedback (Observability)

**Unique Capabilities:**
- `trigger` field - Know if manual or auto compaction
- Last chance to preserve full context before compression

---

## 5. Recommendations

### High-Value Use Cases to Implement First

1. **Safety Essentials**
   - Block rm -rf commands (prevents catastrophic data loss)
   - Block .env file access (protects secrets)
   - Git commit confirmation (prevents accidental commits)

2. **Quality Fundamentals**
   - Auto-formatter (Prettier/Ruff) - maintains code consistency
   - Pre-commit lint blocking - catches issues early
   - TypeScript type checking - prevents type errors

3. **Productivity Quick Wins**
   - Tool redirection (WebFetch to Tavily) - better results
   - Auto context file injection - reduces manual work
   - Command logger - audit trail for debugging

4. **Communication Basics**
   - Desktop notification on completion - awareness
   - TTS for input requests - hands-free workflow

### Combinations That Work Well Together

1. **TDD Workflow Bundle**
   - TDD validation gate (PreToolUse)
   - Lint notification block (PreToolUse)
   - Post-tool lint enforcement (PostToolUse)
   - Test validation before commit (PreToolUse)

2. **Safety Net Bundle**
   - Dangerous rm blocking (PreToolUse)
   - Git safety checks (PreToolUse)
   - Secret detection (PreToolUse)
   - .env file protection (PreToolUse)

3. **Quality Automation Bundle**
   - Prettier auto-formatter (PostToolUse)
   - ESLint auto-fix (PostToolUse)
   - TypeScript type checking (PostToolUse)
   - Pre-edit type blocking (PreToolUse)

4. **Full Observability Bundle**
   - Session logging (SessionStart)
   - PreToolUse logging (PreToolUse)
   - PostToolUse logging (PostToolUse)
   - Transcript export (Stop)
   - Context progress bar (StatusLine)

5. **Communication Bundle**
   - TTS session announcement (SessionStart)
   - TTS completion announcement (Stop)
   - Desktop notifications (Notification)
   - Notification filtering (Notification)

### Gaps in Current Ecosystem

1. **Missing Hook Coverage**
   - Few PreCompact hooks - opportunity for context preservation
   - Limited SubagentStop usage - multi-agent coordination needs work
   - No widely-adopted UserPromptSubmit SDK patterns

2. **Under-explored Use Cases**
   - Real-time collaboration hooks
   - Cost tracking and budget enforcement
   - Performance profiling hooks
   - Custom skill routing
   - Semantic caching

3. **Technical Gaps**
   - No streaming hook support
   - Limited Windows-specific implementations
   - No hook composition/chaining frameworks
   - Missing hook testing utilities

4. **Integration Gaps**
   - Limited IDE integration beyond VS Code
   - No CI/CD pipeline hook patterns
   - Missing cloud service integrations (AWS/GCP/Azure)
   - No database operation hooks

---

## Appendix: Source Repository Quick Reference

| Repository | Primary Focus | Language | Notable Features |
|------------|---------------|----------|------------------|
| hooks-mastery | Full lifecycle hooks | Python | TTS, logging, context loading |
| safety-net | Bash command safety | Python | Comprehensive rm/git analysis |
| tdd-guard | TDD enforcement | TypeScript | AI-powered validation |
| codex-settings | Quality & productivity | Python | Plugin architecture |
| claude-hooks-ts | TypeScript SDK | TypeScript | Type-safe handlers |
| cc-tools-py | Safety & statusline | Python/Bash | TRASH pattern, statusline |
| cc-tools-go | High-perf statusline | Go | Sub-ms rendering |
| evanl1 | Safety & quality | Python | Comprehensive validators |
| awesome | Community index | Various | Curated hook collection |
