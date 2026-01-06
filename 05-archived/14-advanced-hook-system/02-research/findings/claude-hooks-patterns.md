# claude-hooks (TypeScript) Findings

**Repository**: `johnlindquist/claude-hooks`
**Language**: TypeScript
**Runtime**: Bun (required for hook execution)
**CLI Framework**: oclif
**Version Analyzed**: 1.1.7

## Overview

`claude-hooks` is a TypeScript-powered hook system for Claude Code that provides full type safety, auto-completion, and strongly-typed payloads. It generates a complete hook infrastructure in the `.claude/` directory with type definitions and utilities.

---

## Key Patterns

### Pattern 1: Centralized Hook Router with Handler Registry

The system uses a single entry point (`index.ts`) that routes to different handlers based on the hook type passed as a CLI argument. This is a clean separation of concerns:

```typescript
// Main hook runner - routes based on CLI argument
export function runHook(handlers: HookHandlers): void {
  const hook_type = process.argv[2]  // Hook type passed as CLI arg

  process.stdin.on('data', async (data) => {
    const payload = JSON.parse(data.toString())

    switch (hook_type) {
      case 'PreToolUse':
        if (handlers.preToolUse) {
          const response = await handlers.preToolUse(payload)
          console.log(JSON.stringify(response))
        }
        break
      // ... other cases
    }
  })
}
```

**Key Insight**: The hook type is passed as a command-line argument, and payload data comes via stdin as JSON.

### Pattern 2: Typed Handler Function Signatures

Each hook type has a dedicated handler type with specific payload and response types:

```typescript
export type PreToolUseHandler = (payload: PreToolUsePayload) => Promise<PreToolUseResponse> | PreToolUseResponse
export type PostToolUseHandler = (payload: PostToolUsePayload) => Promise<PostToolUseResponse> | PostToolUseResponse
export type NotificationHandler = (payload: NotificationPayload) => Promise<BaseHookResponse> | BaseHookResponse
export type StopHandler = (payload: StopPayload) => Promise<StopResponse> | StopResponse
```

**Key Insight**: Handlers can return either a Promise or a sync response, providing flexibility.

### Pattern 3: Handler Registry Pattern

All handlers are registered in a single object passed to `runHook()`:

```typescript
interface HookHandlers {
  preToolUse?: PreToolUseHandler
  postToolUse?: PostToolUseHandler
  notification?: NotificationHandler
  stop?: StopHandler
  subagentStop?: SubagentStopHandler
  userPromptSubmit?: UserPromptSubmitHandler
  preCompact?: PreCompactHandler
  sessionStart?: SessionStartHandler
}

// Usage
runHook({
  sessionStart,
  preToolUse,
  postToolUse,
  notification,
  stop,
  subagentStop,
  userPromptSubmit,
  preCompact,
})
```

### Pattern 4: Settings Configuration Structure

The `.claude/settings.json` follows a matcher-based hook registration:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "",  // Empty = match all
        "hooks": [
          {
            "type": "command",
            "command": "bun .claude/hooks/index.ts PreToolUse"
          }
        ]
      }
    ]
  }
}
```

**Key Insight**: The `matcher` field allows filtering which hooks run for specific tools/events.

### Pattern 5: Permission Decision Pattern

PreToolUse hooks can control tool execution with permission decisions:

```typescript
interface PreToolUseResponse extends BaseHookResponse {
  permissionDecision?: 'allow' | 'deny' | 'ask'
  permissionDecisionReason?: string
}

// Example: Block dangerous commands
if (command.includes('rm -rf /')) {
  return {
    permissionDecision: 'deny',
    permissionDecisionReason: `Dangerous command detected: ${command}`,
  }
}
```

---

## TypeScript Architecture

### File Structure

```
.claude/
├── settings.json          # Hook configuration (or settings.json.local)
└── hooks/
    ├── index.ts           # Main hook handlers (user-editable)
    ├── lib.ts             # Type definitions and utilities
    └── session.ts         # Session tracking utilities
```

### Module System

- Uses ES Modules (`"type": "module"` in package.json)
- TypeScript target: ES2022
- Module resolution: Node16
- Strict mode enabled

### Bun Integration

Hooks are designed to run with Bun runtime:
- Shebang: `#!/usr/bin/env bun`
- Fast startup time critical for hook execution
- Uses `bun init` to set up TypeScript project in hooks directory

---

## Type Definitions

### Base Payload Interface

```typescript
interface BasePayload {
  session_id: string
  transcript_path: string
}
```

### Hook-Specific Payloads

```typescript
export interface PreToolUsePayload {
  session_id: string
  transcript_path: string
  hook_event_name: 'PreToolUse'
  tool_name: string
  tool_input: Record<string, unknown>
}

export interface PostToolUsePayload {
  session_id: string
  transcript_path: string
  hook_event_name: 'PostToolUse'
  tool_name: string
  tool_input: Record<string, unknown>
  tool_response: Record<string, unknown> & {
    success?: boolean
  }
}

export interface NotificationPayload {
  session_id: string
  transcript_path: string
  hook_event_name: 'Notification'
  message: string
  title?: string
}

export interface StopPayload {
  session_id: string
  transcript_path: string
  hook_event_name: 'Stop'
  stop_hook_active: boolean
}

export interface SubagentStopPayload {
  session_id: string
  transcript_path: string
  hook_event_name: 'SubagentStop'
  stop_hook_active: boolean
}

export interface UserPromptSubmitPayload {
  session_id: string
  transcript_path: string
  hook_event_name: 'UserPromptSubmit'
  prompt: string
}

export interface PreCompactPayload {
  session_id: string
  transcript_path: string
  hook_event_name: 'PreCompact'
  trigger: 'manual' | 'auto'
}

export interface SessionStartPayload {
  session_id: string
  transcript_path: string
  hook_event_name: 'SessionStart'
  source: string  // 'vscode', 'web', etc.
}
```

### Response Types

```typescript
// Base response fields available to all hooks
export interface BaseHookResponse {
  continue?: boolean
  stopReason?: string
  suppressOutput?: boolean
}

// PreToolUse specific response
export interface PreToolUseResponse extends BaseHookResponse {
  permissionDecision?: 'allow' | 'deny' | 'ask'
  permissionDecisionReason?: string
}

// PostToolUse specific response
export interface PostToolUseResponse extends BaseHookResponse {
  decision?: 'block'
  reason?: string
}

// Stop/SubagentStop specific response
export interface StopResponse extends BaseHookResponse {
  decision?: 'block'
  reason?: string  // Required when decision is 'block'
}

// UserPromptSubmit specific response
export interface UserPromptSubmitResponse extends BaseHookResponse {
  decision?: 'approve' | 'block'
  reason?: string
  contextFiles?: string[]  // Glob patterns to add to context
  updatedPrompt?: string
  hookSpecificOutput?: {
    hookEventName: 'UserPromptSubmit'
    additionalContext?: string
  }
}

// PreCompact specific response
export interface PreCompactResponse extends BaseHookResponse {
  decision?: 'approve' | 'block'
  reason?: string
}

// SessionStart specific response
export interface SessionStartResponse extends BaseHookResponse {
  decision?: 'approve' | 'block'
  reason?: string
  hookSpecificOutput?: {
    hookEventName: 'SessionStart'
    additionalContext?: string
  }
}
```

### Tool-Specific Input Types

```typescript
export namespace ToolInputs {
  export interface Write {
    file_path: string
    content: string
  }

  export interface Edit {
    file_path: string
    old_string: string
    new_string: string
    replace_all?: boolean
  }

  export interface Bash {
    command: string
    timeout?: number
    description?: string
  }

  export interface Read {
    file_path: string
    limit?: number
    offset?: number
  }

  export interface Glob {
    pattern: string
    path?: string
  }

  export interface Grep {
    pattern: string
    path?: string
    include?: string
  }
}
```

### Union Type with Discriminator

```typescript
export type HookPayload =
  | (PreToolUsePayload & {hook_type: 'PreToolUse'})
  | (PostToolUsePayload & {hook_type: 'PostToolUse'})
  | (NotificationPayload & {hook_type: 'Notification'})
  | (StopPayload & {hook_type: 'Stop'})
  | (SubagentStopPayload & {hook_type: 'SubagentStop'})
  | (UserPromptSubmitPayload & {hook_type: 'UserPromptSubmit'})
  | (PreCompactPayload & {hook_type: 'PreCompact'})
  | (SessionStartPayload & {hook_type: 'SessionStart'})
```

---

## Transcript Parsing Utilities

The library includes comprehensive transcript parsing for analyzing Claude session history:

### Transcript Message Types

```typescript
export interface TranscriptUserMessage {
  parentUuid: string | null
  isSidechain: boolean
  userType: 'external'
  cwd: string
  sessionId: string
  version: string
  gitBranch?: string
  type: 'user'
  message: {
    role: 'user'
    content: string | Array<{
      tool_use_id?: string
      type: 'tool_result' | 'text'
      content?: string
      is_error?: boolean
    }>
  }
  uuid: string
  timestamp: string
  toolUseResult?: {
    stdout: string
    stderr: string
    interrupted: boolean
    isImage: boolean
  }
}

export interface TranscriptAssistantMessage {
  parentUuid: string
  message: {
    id: string
    type: 'message'
    role: 'assistant'
    model: string
    content: Array<{
      type: 'text' | 'tool_use'
      text?: string
      id?: string
      name?: string
      input?: Record<string, unknown>
    }>
    stop_reason: string | null
    usage: {
      input_tokens: number
      cache_creation_input_tokens: number
      cache_read_input_tokens: number
      output_tokens: number
      service_tier: string
    }
  }
  type: 'assistant'
  uuid: string
  timestamp: string
}
```

### Transcript Helper Functions

```typescript
// Get the first user message from a transcript
export async function getInitialMessage(transcriptPath: string): Promise<string | null>

// Get all messages from a transcript
export async function getAllMessages(transcriptPath: string): Promise<TranscriptMessage[]>

// Get formatted conversation history
export async function getConversationHistory(
  transcriptPath: string,
): Promise<Array<{role: 'user' | 'assistant'; content: string}>>

// Extract tool usage data
export async function getToolUsage(
  transcriptPath: string,
): Promise<Array<{tool: string; input: Record<string, unknown>; timestamp: string}>>
```

---

## Session Tracking System

Session data is persisted to the system temp directory:

```typescript
const SESSIONS_DIR = path.join(tmpdir(), 'claude-hooks-sessions')

export async function saveSessionData(hookType: string, payload: HookPayload): Promise<void> {
  await mkdir(SESSIONS_DIR, {recursive: true})

  const timestamp = new Date().toISOString()
  const sessionFile = path.join(SESSIONS_DIR, `${payload.session_id}.json`)

  let sessionData: Array<{timestamp: string; hookType: string; payload: HookPayload}> = []
  try {
    const existing = await readFile(sessionFile, 'utf-8')
    sessionData = JSON.parse(existing)
  } catch {
    // File doesn't exist yet
  }

  sessionData.push({timestamp, hookType, payload})
  await writeFile(sessionFile, JSON.stringify(sessionData, null, 2))
}
```

**Key Insight**: Session logs accumulate all hook events for a session in a single JSON file.

---

## Type Guards

```typescript
export function isPreToolUseInput(input: HookInput): input is PreToolUseInput {
  return 'tool_name' in input && !('tool_response' in input)
}

export function isPostToolUseInput(input: HookInput): input is PostToolUseInput {
  return 'tool_name' in input && 'tool_response' in input
}

export function isNotificationInput(input: HookInput): input is NotificationInput {
  return 'message' in input && 'title' in input
}

export function isStopInput(input: HookInput): input is StopInput | SubagentStopInput {
  return 'stop_hook_active' in input
}
```

---

## Validation Functions

```typescript
export function validateStopResponse(response: StopResponse): string | null {
  if (response.decision === 'block' && !response.reason) {
    return 'reason is required when decision is "block"'
  }
  return null
}

export function validateHookResponse(
  hookType: 'PreToolUse' | 'PostToolUse' | 'Stop' | 'SubagentStop' | 'Notification',
  response: any,
): string | null {
  if ('decision' in response) {
    switch (hookType) {
      case 'PreToolUse':
        if (response.decision && !['approve', 'block'].includes(response.decision)) {
          return `Invalid decision for PreToolUse: ${response.decision}`
        }
        break
      case 'PostToolUse':
      case 'Stop':
      case 'SubagentStop':
        if (response.decision && response.decision !== 'block') {
          return `Invalid decision for ${hookType}: ${response.decision}`
        }
        break
      case 'Notification':
        if (response.decision) {
          return 'Notification hooks should not have a decision field'
        }
        break
    }
  }
  return null
}
```

---

## CLI Architecture (oclif)

### Command Structure

```typescript
import {Command, Flags} from '@oclif/core'

export default class Init extends Command {
  static description = `Initialize Claude Code hooks in your project`

  static flags = {
    force: Flags.boolean({char: 'f', description: 'Overwrite existing hooks'}),
    local: Flags.boolean({char: 'l', description: 'Create settings.json.local'}),
  }

  public async run(): Promise<void> {
    const {flags} = await this.parse(Init)
    // Implementation
  }
}
```

### Default Command Pattern

```javascript
// bin/run.js - Default to 'init' command when no args provided
const args = process.argv.slice(2)
if (args.length === 0) {
  process.argv.push('init')
}
```

---

## Hook Types Summary

| Hook Type | When Called | Can Block | Response Type |
|-----------|-------------|-----------|---------------|
| SessionStart | New session starts | Yes | SessionStartResponse |
| PreToolUse | Before tool execution | Yes (deny/allow/ask) | PreToolUseResponse |
| PostToolUse | After tool execution | Yes (block) | PostToolUseResponse |
| Notification | Claude sends notification | No | BaseHookResponse |
| Stop | Session ends | Yes (block) | StopResponse |
| SubagentStop | Subagent task ends | Yes (block) | StopResponse |
| UserPromptSubmit | User submits prompt | Yes (block) | UserPromptSubmitResponse |
| PreCompact | Before conversation compact | Yes (block) | PreCompactResponse |

---

## Notes for Implementation

### 1. Stdin/Stdout Communication Protocol
- Hook receives JSON payload via stdin
- Hook returns JSON response via stdout
- Hook type passed as CLI argument
- Empty object `{}` means continue with default behavior

### 2. Error Handling Pattern
```typescript
try {
  const inputData = JSON.parse(data.toString())
  // Process hook
} catch (error) {
  console.error('Hook error:', error)
  console.log(JSON.stringify({action: 'continue'}))  // Fail-safe
}
```

### 3. Async Support
All handlers support both sync and async returns:
```typescript
// Both valid:
const preToolUse: PreToolUseHandler = async (payload) => { ... }
const preToolUse: PreToolUseHandler = (payload) => { ... }
```

### 4. Context Files Pattern (UserPromptSubmit)
Can dynamically add files to context based on prompt:
```typescript
const userPromptSubmit: UserPromptSubmitHandler = async (payload) => {
  const contextFiles: string[] = []
  if (payload.prompt.toLowerCase().includes('test')) {
    contextFiles.push('**/*.test.ts', '**/*.test.js')
  }
  return contextFiles.length > 0 ? {contextFiles} : {}
}
```

### 5. Session Source Detection (SessionStart)
Can detect and adapt to different session sources:
```typescript
if (payload.source === 'vscode') {
  // IDE-specific features
} else if (payload.source === 'web') {
  // Web session handling
}
```

### 6. Stop Hook Loop Prevention
Important to check `stop_hook_active` to prevent infinite loops:
```typescript
if (payload.stop_hook_active) {
  console.log('Stop hook already active, skipping')
  return {}
}
```

### 7. Settings Precedence
- `settings.json.local` for personal configuration (not committed)
- `settings.json` for project-wide hooks (committed)

### 8. Matcher System
The settings allow tool-specific hooks via matcher:
```json
{
  "matcher": "Bash",  // Only run for Bash tool
  "hooks": [...]
}
```

### 9. Logging Utility
Simple timestamped logging:
```typescript
export function log(...args: unknown[]): void {
  console.log(`[${new Date().toISOString()}]`, ...args)
}
```

---

## Example Usage Patterns

### Security: Block Dangerous Commands
```typescript
const preToolUse: PreToolUseHandler = async (payload) => {
  if (payload.tool_name === 'Bash' && 'command' in payload.tool_input) {
    const command = payload.tool_input.command as string
    if (command.includes('rm -rf /') || command.includes('rm -rf ~')) {
      return {
        permissionDecision: 'deny',
        permissionDecisionReason: `Dangerous command detected: ${command}`,
      }
    }
  }
  return {}
}
```

### Analytics: Track Tool Usage
```typescript
const postToolUse: PostToolUseHandler = async (payload) => {
  await saveSessionData('PostToolUse', {...payload, hook_type: 'PostToolUse'})
  if (payload.tool_name === 'Write' && payload.tool_response) {
    console.log(`File written successfully!`)
  }
  return {}
}
```

### Context Enhancement: Auto-Add Related Files
```typescript
const userPromptSubmit: UserPromptSubmitHandler = async (payload) => {
  const contextFiles: string[] = []
  if (payload.prompt.toLowerCase().includes('test')) {
    contextFiles.push('**/*.test.ts', '**/*.test.js')
  }
  return contextFiles.length > 0 ? {contextFiles} : {}
}
```

### Quality Gate: Force Documentation Updates
```typescript
const stop: StopHandler = async (payload) => {
  // Force Claude to continue and add documentation
  return {
    decision: 'block',
    reason: 'Please also update the documentation for this change',
  }
}
```

---

## Dependencies

### Runtime Dependencies
- `@oclif/core` - CLI framework
- `chalk` - Terminal styling
- `fs-extra` - File system utilities
- `inquirer` - Interactive prompts
- `ora` - Spinner for progress indication

### Development Dependencies
- TypeScript 5.x
- Biome (linting/formatting)
- Mocha/Chai (testing)
- NYC (code coverage)

---

## Testing Strategy

1. **Unit Tests**: Individual command testing
2. **Integration Tests**: Full CLI behavior
3. **Smoke Tests**: Validate generated files work correctly
4. **Cross-Platform**: CI runs on Ubuntu, Windows, macOS with Node 18 & 20

---

## Key Takeaways for Nexus Implementation

1. **Type-First Design**: Comprehensive TypeScript types for all payloads and responses
2. **Stdin/Stdout Protocol**: Clean JSON-based communication
3. **Handler Registry Pattern**: Flexible registration of hook handlers
4. **Fail-Safe Defaults**: Empty object `{}` continues execution
5. **Session Persistence**: Accumulating session logs for analytics
6. **Transcript Access**: Full conversation history available via `transcript_path`
7. **Context Enhancement**: UserPromptSubmit can dynamically add files
8. **Source Detection**: SessionStart provides session source info
9. **Loop Prevention**: `stop_hook_active` flag prevents recursive issues
10. **Matcher System**: Tool-specific hook registration via settings
