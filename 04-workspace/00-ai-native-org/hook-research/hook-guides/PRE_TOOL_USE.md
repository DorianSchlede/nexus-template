# PreToolUse Hook Pattern Guide

> Comprehensive synthesis of PreToolUse patterns from 15 source repositories

---

## 1. Overview

### What This Hook Does

The **PreToolUse** hook fires **before** Claude executes any tool operation. It gives you the opportunity to:

- **Inspect** the tool name and input parameters
- **Block** dangerous or disallowed operations (exit code 2)
- **Prompt for confirmation** via the "ask" decision
- **Allow** operations to proceed (default)
- **Inject context** via `permissionDecisionReason` that Claude sees

### When It Fires (Trigger Conditions)

PreToolUse fires immediately before Claude invokes any tool, including:

| Tool | Typical Use Case |
|------|------------------|
| `Bash` | Shell command execution |
| `Write` | Creating new files |
| `Edit` | Modifying existing files |
| `MultiEdit` | Batch file edits |
| `Read` | Reading file contents |
| `Glob` | File pattern matching |
| `Grep` | Content searching |
| `WebFetch` | HTTP requests |
| `TodoWrite` | Task management |
| `Task` | Subagent spawning |
| MCP tools | Any MCP-provided tools |

### Can It Block?

**Yes.** PreToolUse can block tool execution via:

1. **Exit code 2** - Hard block, tool execution is prevented
2. **`permissionDecision: "deny"`** - JSON response that blocks with reason
3. **`permissionDecision: "ask"`** - Prompts user for confirmation

### JSON Input Schema

The hook receives JSON on stdin with this structure:

```json
{
  "hook_event_name": "PreToolUse",
  "session_id": "abc123-def456",
  "transcript_path": "/path/to/.claude/projects/.../transcript.jsonl",
  "tool_name": "Bash",
  "tool_input": {
    "command": "rm -rf /tmp/test",
    "timeout": 30000,
    "description": "Remove test directory"
  }
}
```

**Tool-specific `tool_input` examples:**

```json
// Write tool
{ "file_path": "/path/to/file.ts", "content": "..." }

// Edit tool
{ "file_path": "/path/to/file.ts", "old_string": "...", "new_string": "...", "replace_all": false }

// Glob tool
{ "pattern": "**/*.ts", "path": "/project" }

// Grep tool
{ "pattern": "TODO", "path": "/project", "include": "*.ts" }
```

### JSON Output Schema

Return JSON to stdout:

```json
// Allow (default) - empty object or no output
{}

// Allow with logging only
{ "permissionDecision": "allow" }

// Block with reason shown to Claude
{
  "permissionDecision": "deny",
  "permissionDecisionReason": "Command 'rm -rf /' is not allowed for safety"
}

// Prompt user for confirmation
{
  "permissionDecision": "ask",
  "permissionDecisionReason": "This will modify production files. Continue?"
}

// Stop the entire session
{
  "continue": false,
  "stopReason": "Critical safety violation detected"
}
```

---

## 2. Pattern Catalog

### Pattern: Dangerous Command Blocker

**Sources**: claude-hooks, cc-tools-py, safety-net
**Description**: Blocks destructive bash commands like `rm -rf /`, `rm -rf ~`, `chmod 777`, etc.
**Decision Type**: deny

**Implementation (TypeScript)**:
```typescript
const preToolUse: PreToolUseHandler = async (payload) => {
  if (payload.tool_name === 'Bash' && payload.tool_input && 'command' in payload.tool_input) {
    const command = (payload.tool_input as {command: string}).command

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

**Implementation (Python)**:
```python
#!/usr/bin/env python3
import json
import sys

DANGEROUS_PATTERNS = [
    "rm -rf /",
    "rm -rf ~",
    "chmod 777",
    "dd if=/dev/zero",
    "> /dev/sda",
    "mkfs.",
    ":(){:|:&};:",  # Fork bomb
]

def main():
    data = json.load(sys.stdin)

    if data.get("tool_name") != "Bash":
        print("{}")
        return

    command = data.get("tool_input", {}).get("command", "")

    for pattern in DANGEROUS_PATTERNS:
        if pattern in command:
            print(json.dumps({
                "permissionDecision": "deny",
                "permissionDecisionReason": f"Blocked dangerous command pattern: {pattern}"
            }))
            return

    print("{}")

if __name__ == "__main__":
    main()
```

**Pros**:
- Simple pattern matching is fast (<10ms)
- Easy to extend with new patterns
- Clear feedback to Claude on why command was blocked

**Cons**:
- Pattern matching can have false positives
- Sophisticated bypass possible with encoding/obfuscation
- Static patterns may miss novel dangerous commands

**Use When**: Always - as a fundamental safety layer for bash commands
**Avoid When**: Never - this is a baseline safety pattern

---

### Pattern: TDD Enforcement Gate

**Sources**: tdd-guard, hooks-mastery-part1
**Description**: Blocks file modifications that violate Test-Driven Development principles. Validates that tests exist and pass before allowing implementation changes.
**Decision Type**: block (exit code 2)

**Implementation (TypeScript)**:
```typescript
export async function handlePreToolUse(
  hookData: string,
  storage: Storage,
  testRunner: TestRunner
): Promise<ValidationResult> {
  const validatedHookData = parseAndValidateHookData(hookData)
  if (!validatedHookData) {
    return DEFAULT_RESULT
  }

  // Skip validation for test files themselves
  const filePath = extractFilePath(validatedHookData)
  if (filePath && isTestFile(filePath)) {
    return DEFAULT_RESULT
  }

  // Check for existing lint issues (two-phase warning system)
  const lintData = await storage.getLint()
  if (lintData?.hasNotifiedAboutLintIssues) {
    // User was already warned, now check if issues persist
    const hasIssues = lintData.errorCount > 0 || lintData.warningCount > 0
    if (hasIssues) {
      return {
        decision: 'block',
        reason: formatLintIssues(lintData)
      }
    }
  }

  // Run TDD validation via AI model
  const context = await buildValidationContext(storage)
  const validationResult = await validateTddCompliance(context, testRunner)

  if (!validationResult.isCompliant) {
    return {
      decision: 'block',
      reason: `TDD violation: ${validationResult.reason}\n\nPlease write tests first.`
    }
  }

  return DEFAULT_RESULT
}

function isTestFile(filePath: string): boolean {
  return /\.(test|spec)\.(ts|js|tsx|jsx)$/.test(filePath) ||
         filePath.includes('__tests__') ||
         filePath.includes('/test/')
}
```

**Pros**:
- Enforces test-first development workflow
- AI-powered validation catches subtle TDD violations
- Two-phase warning system (warn first, block on repeat)

**Cons**:
- Can be disruptive during rapid prototyping
- AI validation adds latency (50-100ms)
- Requires test framework configuration

**Use When**: Projects with strict TDD requirements, teaching TDD practices
**Avoid When**: Prototyping, exploratory coding, projects without test infrastructure

---

### Pattern: File Ignore Patterns

**Sources**: tdd-guard, hooks-mastery-part2
**Description**: Skips validation for files matching configurable glob patterns (e.g., *.md, *.json, *.yml)
**Decision Type**: allow (early exit)

**Implementation (TypeScript)**:
```typescript
import { minimatch } from 'minimatch'

export class GuardManager {
  private readonly minimatchOptions = {
    matchBase: true,  // *.ext matches in any directory
    nobrace: false,   // enables {a,b} expansion
    dot: true,        // matches files starting with .
  } as const

  static readonly DEFAULT_IGNORE_PATTERNS = [
    '*.md',
    '*.txt',
    '*.log',
    '*.json',
    '*.yml',
    '*.yaml',
    '*.xml',
    '*.html',
    '*.css',
    '*.rst',
  ]

  async shouldIgnoreFile(filePath: string): Promise<boolean> {
    const patterns = await this.getIgnorePatterns()
    return patterns.some((pattern) =>
      minimatch(filePath, pattern, this.minimatchOptions)
    )
  }
}

// In PreToolUse handler:
const filePath = extractFilePath(parsedData)
if (filePath && await guardManager.shouldIgnoreFile(filePath)) {
  return {} // Allow without validation
}
```

**Pros**:
- Reduces noise from non-code file validations
- Configurable per-project
- Fast pattern matching (<10ms)

**Cons**:
- May accidentally skip files that need validation
- Patterns require maintenance as project evolves

**Use When**: Any hook that validates file content but not all file types
**Avoid When**: Hooks that must examine all files regardless of type

---

### Pattern: Tool Redirection

**Sources**: awesome (fcakyon), hooks-mastery-session
**Description**: Redirects tool usage to preferred alternatives (e.g., force Tavily over WebFetch)
**Decision Type**: deny with guidance

**Implementation (Python)**:
```python
#!/usr/bin/env python3
import json
import sys

TOOL_REDIRECTS = {
    "WebFetch": {
        "alternative": "mcp__tavily__search",
        "reason": "Please use Tavily MCP tool for web searches - it provides better structured results"
    },
    "WebSearch": {
        "alternative": "mcp__tavily__search",
        "reason": "Use Tavily for web searches to ensure consistent results format"
    }
}

def main():
    data = json.load(sys.stdin)
    tool_name = data.get("tool_name", "")

    if tool_name in TOOL_REDIRECTS:
        redirect = TOOL_REDIRECTS[tool_name]
        print(json.dumps({
            "permissionDecision": "deny",
            "permissionDecisionReason": f"{redirect['reason']}\n\nUse: {redirect['alternative']}"
        }))
        return

    print("{}")

if __name__ == "__main__":
    main()
```

**Pros**:
- Standardizes tool usage across team
- Can enforce MCP tool preferences
- Clear guidance on what to use instead

**Cons**:
- May frustrate users who prefer blocked tools
- Needs updates when new tools added

**Use When**: Standardizing tool preferences, enforcing MCP tool usage
**Avoid When**: Flexible tool requirements

---

### Pattern: Path-Based Permission Gates

**Sources**: cc-tools-py, safety-net, hooks-mastery-user
**Description**: Blocks or warns when Claude attempts to modify files in protected directories
**Decision Type**: deny or ask

**Implementation (Python)**:
```python
#!/usr/bin/env python3
import json
import sys
import os

PROTECTED_PATHS = [
    "/etc/",
    "/usr/",
    "/bin/",
    "/sbin/",
    "~/.ssh/",
    "~/.gnupg/",
    ".env",
    "credentials",
    "secrets",
]

WARN_PATHS = [
    "/production/",
    "/prod/",
    "main.py",
    "index.ts",
]

def main():
    data = json.load(sys.stdin)
    tool_name = data.get("tool_name", "")
    tool_input = data.get("tool_input", {})

    # Extract file path based on tool type
    file_path = ""
    if tool_name in ["Write", "Edit", "Read"]:
        file_path = tool_input.get("file_path", "")
    elif tool_name == "Bash":
        command = tool_input.get("command", "")
        # Simple extraction - production would use proper parsing
        file_path = command

    # Expand home directory
    file_path = os.path.expanduser(file_path)

    # Check protected paths
    for protected in PROTECTED_PATHS:
        protected = os.path.expanduser(protected)
        if protected in file_path:
            print(json.dumps({
                "permissionDecision": "deny",
                "permissionDecisionReason": f"Access to {protected} is blocked for safety"
            }))
            return

    # Check warning paths
    for warn_path in WARN_PATHS:
        if warn_path in file_path:
            print(json.dumps({
                "permissionDecision": "ask",
                "permissionDecisionReason": f"This will modify {file_path}. Are you sure?"
            }))
            return

    print("{}")

if __name__ == "__main__":
    main()
```

**Pros**:
- Protects system and sensitive directories
- Two-tier system (block vs warn) for flexibility
- Works across all file-touching tools

**Cons**:
- Path parsing can be complex for bash commands
- May need OS-specific path handling

**Use When**: Any environment where certain paths should be protected
**Avoid When**: Sandboxed/containerized environments with no sensitive paths

---

### Pattern: Pre-Execution Lint Check

**Sources**: tdd-guard, typescript-quality-hooks
**Description**: Sets notification flag and warns about existing lint issues before allowing file edits. Works with PostToolUse for two-phase enforcement.
**Decision Type**: allow (with notification state)

**Implementation (TypeScript)**:
```typescript
export async function handlePreToolLint(
  hookData: string,
  storage: Storage
): Promise<ValidationResult> {
  const validatedHookData = parseAndValidateHookData(hookData)
  if (!validatedHookData) {
    return DEFAULT_RESULT
  }

  // Only process file-modifying tools
  const toolName = validatedHookData.tool_name
  if (!['Write', 'Edit', 'MultiEdit'].includes(toolName)) {
    return DEFAULT_RESULT
  }

  // Check for existing lint issues
  const lintData = await storage.getLint()
  if (!lintData) {
    return DEFAULT_RESULT
  }

  const hasIssues = lintData.errorCount > 0 || lintData.warningCount > 0

  if (hasIssues && !lintData.hasNotifiedAboutLintIssues) {
    // First time seeing issues - warn but allow, set notification flag
    const updatedLintData = { ...lintData, hasNotifiedAboutLintIssues: true }
    await storage.saveLint(JSON.stringify(updatedLintData))

    return {
      decision: undefined, // Allow to proceed
      reason: `Warning: ${lintData.errorCount} errors, ${lintData.warningCount} warnings exist.\nPlease fix before making more changes.`
    }
  }

  return DEFAULT_RESULT
}
```

**Pros**:
- "Warning shot" before hard blocking
- Works with PostToolUse for complete enforcement
- Less disruptive than immediate blocking

**Cons**:
- Requires state persistence between hook calls
- More complex than single-hook patterns

**Use When**: Gradual enforcement, teaching scenarios
**Avoid When**: Immediate blocking is required for safety

---

### Pattern: File Edit Logging/Audit

**Sources**: claude-hooks, hooks-mastery-tool
**Description**: Logs all file modification attempts for audit trail
**Decision Type**: allow (logging only)

**Implementation (TypeScript)**:
```typescript
const preToolUse: PreToolUseHandler = async (payload) => {
  const timestamp = new Date().toISOString()

  if (payload.tool_name === 'Edit' && payload.tool_input) {
    const { file_path } = payload.tool_input as { file_path: string }
    console.error(`[${timestamp}] EDIT: ${file_path}`)
  }

  if (payload.tool_name === 'Write' && payload.tool_input) {
    const { file_path } = payload.tool_input as { file_path: string }
    console.error(`[${timestamp}] WRITE: ${file_path}`)
  }

  if (payload.tool_name === 'Bash' && payload.tool_input) {
    const { command, description } = payload.tool_input as { command: string; description?: string }
    console.error(`[${timestamp}] BASH: ${description || command.substring(0, 100)}`)
  }

  return {} // Always allow
}
```

**Implementation (Bash)**:
```bash
#!/bin/bash
# Log all PreToolUse events to file

LOG_FILE="${HOME}/.claude/audit.log"
INPUT=$(cat)

TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // "unknown"')
TIMESTAMP=$(date -Iseconds)

echo "[$TIMESTAMP] PreToolUse: $TOOL_NAME" >> "$LOG_FILE"
echo "$INPUT" | jq -c '.tool_input' >> "$LOG_FILE"

# Always allow
echo '{}'
```

**Pros**:
- Zero impact on workflow
- Complete audit trail
- Simple to implement

**Cons**:
- Log files can grow large
- No enforcement, only observation

**Use When**: Audit requirements, debugging hook behavior
**Avoid When**: You need actual enforcement

---

### Pattern: Context-Aware Skill Activation

**Sources**: awesome (claude-infrastructure-showcase)
**Description**: Dynamically loads relevant skills/context based on tool being used and project state
**Decision Type**: allow with context injection

**Implementation (TypeScript)**:
```typescript
interface SkillMapping {
  tools: string[]
  skillPath: string
  condition?: (toolInput: Record<string, unknown>) => boolean
}

const SKILL_MAPPINGS: SkillMapping[] = [
  {
    tools: ['Write', 'Edit'],
    skillPath: '.claude/skills/code-review.md',
    condition: (input) => {
      const path = (input.file_path as string) || ''
      return path.endsWith('.ts') || path.endsWith('.tsx')
    }
  },
  {
    tools: ['Bash'],
    skillPath: '.claude/skills/devops.md',
    condition: (input) => {
      const cmd = (input.command as string) || ''
      return cmd.includes('docker') || cmd.includes('kubectl')
    }
  },
  {
    tools: ['WebFetch'],
    skillPath: '.claude/skills/research.md'
  }
]

const preToolUse: PreToolUseHandler = async (payload) => {
  const matchingSkills: string[] = []

  for (const mapping of SKILL_MAPPINGS) {
    if (!mapping.tools.includes(payload.tool_name)) continue
    if (mapping.condition && !mapping.condition(payload.tool_input)) continue
    matchingSkills.push(mapping.skillPath)
  }

  if (matchingSkills.length > 0) {
    // Load skills and inject as context
    const skillContents = await Promise.all(
      matchingSkills.map(path => readFile(path, 'utf-8').catch(() => ''))
    )

    return {
      permissionDecision: 'allow',
      permissionDecisionReason: skillContents.filter(Boolean).join('\n\n---\n\n')
    }
  }

  return {}
}
```

**Pros**:
- Dynamic context without manual loading
- Tool-specific expertise injection
- Composable skill system

**Cons**:
- Skill file I/O adds latency
- Complex condition logic maintenance

**Use When**: Projects with specialized skills, context-dependent workflows
**Avoid When**: Simple projects, latency-sensitive operations

---

### Pattern: Request Confirmation for Risky Operations

**Sources**: hooks-mastery-user, safety-net
**Description**: Uses "ask" decision to prompt user confirmation for operations that are risky but not outright forbidden
**Decision Type**: ask

**Implementation (Python)**:
```python
#!/usr/bin/env python3
import json
import sys
import re

CONFIRM_PATTERNS = {
    "Bash": [
        (r"git push.*--force", "Force push can overwrite remote history"),
        (r"git reset --hard", "Hard reset will discard uncommitted changes"),
        (r"npm publish", "This will publish package to npm registry"),
        (r"docker.*--rm", "Container will be removed after execution"),
    ],
    "Write": [
        (r"\.env$", "Environment files may contain secrets"),
        (r"package\.json$", "Modifying package.json affects dependencies"),
    ],
    "Edit": [
        (r"migration", "Database migrations should be reviewed carefully"),
    ]
}

def main():
    data = json.load(sys.stdin)
    tool_name = data.get("tool_name", "")
    tool_input = data.get("tool_input", {})

    patterns = CONFIRM_PATTERNS.get(tool_name, [])

    # Get the relevant string to check
    check_string = ""
    if tool_name == "Bash":
        check_string = tool_input.get("command", "")
    elif tool_name in ["Write", "Edit"]:
        check_string = tool_input.get("file_path", "")

    for pattern, reason in patterns:
        if re.search(pattern, check_string, re.IGNORECASE):
            print(json.dumps({
                "permissionDecision": "ask",
                "permissionDecisionReason": f"{reason}\n\nProceed with this operation?"
            }))
            return

    print("{}")

if __name__ == "__main__":
    main()
```

**Pros**:
- Adds human oversight without blocking workflow
- Educates users about risky operations
- Flexible middle ground between allow and deny

**Cons**:
- Can become annoying if too many confirmations
- User may develop "click fatigue"

**Use When**: Operations that are risky but legitimate
**Avoid When**: Truly dangerous operations (use deny), routine operations

---

### Pattern: Guard State Check (Early Exit)

**Sources**: tdd-guard
**Description**: Checks if the guard is disabled and returns early, enabling runtime toggle of enforcement
**Decision Type**: allow (bypass)

**Implementation (TypeScript)**:
```typescript
export class GuardManager {
  private readonly storage: Storage

  async isEnabled(): Promise<boolean> {
    const config = await this.storage.getConfig()
    return config?.enabled ?? true // Default to enabled
  }
}

// In PreToolUse handler:
export async function processPreToolUse(hookData: string): Promise<ValidationResult> {
  const guardManager = new GuardManager(storage)

  // Early exit if guard is disabled
  if (!await guardManager.isEnabled()) {
    return {} // Allow everything
  }

  // Continue with normal validation...
  return performValidation(hookData)
}
```

**Pros**:
- Runtime toggle without config file changes
- Fast bypass when disabled
- Pairs well with UserPromptSubmit toggle commands

**Cons**:
- Users might disable and forget to re-enable
- Potential security gap if disabled

**Use When**: Hooks that should be temporarily disableable
**Avoid When**: Critical safety hooks that should never be bypassed

---

### Pattern: Bash Command Parsing and Validation

**Sources**: cc-tools-py, safety-net, hooks-mastery-part1
**Description**: Parses bash commands to extract and validate individual components, flags, and file targets
**Decision Type**: deny or allow based on parsed components

**Implementation (Python)**:
```python
#!/usr/bin/env python3
import json
import sys
import shlex

BLOCKED_COMMANDS = {'rm', 'mkfs', 'dd', 'shutdown', 'reboot', 'halt'}
BLOCKED_FLAGS = {'--force', '-f', '--no-preserve-root'}
ALLOWED_RM_PATTERNS = {'-rf node_modules', '-rf dist', '-rf build', '-rf .cache'}

def parse_command(command: str) -> dict:
    """Parse bash command into components."""
    try:
        tokens = shlex.split(command)
    except ValueError:
        return {"raw": command, "tokens": [], "error": "parse_failed"}

    if not tokens:
        return {"raw": command, "tokens": [], "base_command": None}

    # Handle pipes and chains
    if '|' in command or '&&' in command or ';' in command:
        return {
            "raw": command,
            "tokens": tokens,
            "is_chain": True,
            "warning": "Command contains chaining"
        }

    base_command = tokens[0].split('/')[-1]  # Handle /usr/bin/rm -> rm
    flags = [t for t in tokens[1:] if t.startswith('-')]
    args = [t for t in tokens[1:] if not t.startswith('-')]

    return {
        "raw": command,
        "tokens": tokens,
        "base_command": base_command,
        "flags": flags,
        "args": args
    }

def validate_command(parsed: dict) -> tuple[bool, str]:
    """Validate parsed command. Returns (allowed, reason)."""

    if parsed.get("error"):
        return False, "Failed to parse command safely"

    if parsed.get("is_chain"):
        return True, ""  # Allow but could add chain validation

    base = parsed.get("base_command", "")
    flags = set(parsed.get("flags", []))

    # Check blocked commands
    if base in BLOCKED_COMMANDS:
        # Check for allowed exceptions
        raw = parsed.get("raw", "")
        for allowed in ALLOWED_RM_PATTERNS:
            if allowed in raw:
                return True, ""
        return False, f"Command '{base}' is blocked"

    # Check blocked flags
    blocked = flags & BLOCKED_FLAGS
    if blocked:
        return False, f"Flags {blocked} are blocked"

    return True, ""

def main():
    data = json.load(sys.stdin)

    if data.get("tool_name") != "Bash":
        print("{}")
        return

    command = data.get("tool_input", {}).get("command", "")
    parsed = parse_command(command)
    allowed, reason = validate_command(parsed)

    if not allowed:
        print(json.dumps({
            "permissionDecision": "deny",
            "permissionDecisionReason": reason
        }))
    else:
        print("{}")

if __name__ == "__main__":
    main()
```

**Pros**:
- Fine-grained command analysis
- Can allow safe variations of dangerous commands
- Handles edge cases like paths in commands

**Cons**:
- Complex bash parsing is error-prone
- May miss obfuscated commands
- Performance overhead from parsing

**Use When**: Nuanced bash command control needed
**Avoid When**: Simple pattern matching is sufficient

---

### Pattern: Type-Safe Hook Handler (SDK)

**Sources**: claude-hooks
**Description**: TypeScript SDK pattern for type-safe PreToolUse handler with full payload typing
**Decision Type**: varies (SDK abstraction)

**Implementation (TypeScript)**:
```typescript
// Type definitions
export interface PreToolUsePayload {
  hook_event_name: 'PreToolUse'
  session_id: string
  transcript_path: string
  tool_name: string
  tool_input: Record<string, unknown>
}

export interface PreToolUseResponse {
  permissionDecision?: 'allow' | 'deny' | 'ask'
  permissionDecisionReason?: string
  continue?: boolean
  stopReason?: string
  suppressOutput?: boolean
}

export type PreToolUseHandler = (payload: PreToolUsePayload) => Promise<PreToolUseResponse>

// Handler registry
export interface HookHandlers {
  preToolUse?: PreToolUseHandler
  postToolUse?: PostToolUseHandler
  // ... other handlers
}

// Runner
export function runHook(handlers: HookHandlers): void {
  const hook_type = process.argv[2]

  process.stdin.on('data', async (data) => {
    try {
      const inputData = JSON.parse(data.toString())
      const payload = { ...inputData, hook_type }

      switch (payload.hook_type) {
        case 'PreToolUse':
          if (handlers.preToolUse) {
            const response = await handlers.preToolUse(payload)
            console.log(JSON.stringify(response))
          } else {
            console.log('{}')
          }
          break
        // ... other cases
      }
    } catch (error) {
      console.log('{}')
    }
  })
}

// Usage
runHook({
  preToolUse: async (payload) => {
    // Type-safe access to payload.tool_name, payload.tool_input, etc.
    return {}
  }
})
```

**Pros**:
- Full TypeScript type safety
- IDE autocomplete for payloads and responses
- Single file handles all hook types

**Cons**:
- Requires TypeScript/Bun runtime
- More setup than simple scripts

**Use When**: TypeScript projects, complex hook logic
**Avoid When**: Simple one-off hooks, shell-only environments

---

## 3. Inspiration Ideas

### New Use Cases Based on Patterns

1. **Cost Guardian**
   - Track estimated API costs from tool usage
   - Warn when session cost exceeds threshold
   - Block expensive operations (large file reads, many MCP calls)

2. **Branch Protection**
   - Block edits to files on protected git branches
   - Require PR creation instead of direct edits
   - Integrate with git hooks for enforcement

3. **Time-Based Access Control**
   - Block production file access outside business hours
   - Require additional confirmation during deployment windows
   - Log all after-hours operations

4. **Dependency Validation**
   - Before `npm install` or `pip install`, check against allowlist
   - Block installation of deprecated/vulnerable packages
   - Require lockfile updates

5. **Context Size Guardian**
   - Monitor context window usage from transcript
   - Warn when approaching limits
   - Suggest compaction before overflow

6. **Tool Usage Quotas**
   - Limit number of WebFetch calls per session
   - Throttle Bash commands per minute
   - Enforce read/write ratios

### Combination Patterns

1. **PreToolUse + PostToolUse Pipeline**
   - PreToolUse: Capture "before" state, set flags
   - PostToolUse: Compare "after" state, enforce constraints
   - Example: Ensure all edits pass type checking

2. **PreToolUse + UserPromptSubmit**
   - UserPromptSubmit: Set session-level policies
   - PreToolUse: Enforce those policies on each tool
   - Example: "strict mode" toggle that changes enforcement level

3. **PreToolUse + SessionStart**
   - SessionStart: Load project-specific rules
   - PreToolUse: Apply loaded rules to tool calls
   - Example: Different projects have different forbidden commands

### Advanced Applications

1. **ML-Based Intent Detection**
   - Use small local model to classify command intent
   - Block commands that seem malicious even if pattern doesn't match
   - Learn from user feedback on false positives

2. **Git-Aware Validation**
   - Parse current git diff to understand change scope
   - Block operations that would conflict with staged changes
   - Warn about operations affecting unstaged files

3. **Project Structure Enforcement**
   - Validate file paths against project conventions
   - Enforce naming patterns (e.g., *.test.ts in __tests__)
   - Block creation of files in wrong directories

4. **Semantic Code Analysis**
   - Parse AST of files being edited
   - Block changes that would break type signatures
   - Enforce architectural boundaries

---

## 4. Implementation Recommendations

### Best Patterns to Adopt (Ranked)

1. **Dangerous Command Blocker** (Essential)
   - Every PreToolUse implementation should include basic safety patterns
   - Fast, simple, high-value protection

2. **File Ignore Patterns** (High Value)
   - Reduces noise dramatically
   - Makes other validations more meaningful
   - Easy to customize per project

3. **Path-Based Permission Gates** (High Value)
   - Protects sensitive areas without blocking workflow
   - Two-tier (deny/ask) provides flexibility

4. **Guard State Check** (Recommended)
   - Runtime disable capability is essential for debugging
   - Pair with UserPromptSubmit toggle

5. **Type-Safe SDK** (Recommended for TS projects)
   - Prevents runtime errors from payload mishandling
   - Better IDE support speeds development

### Patterns to Avoid

1. **Overly Aggressive Blocking**
   - Too many blocks frustrates users
   - Use "ask" for questionable but not dangerous operations

2. **Complex Bash Parsing Without Fallback**
   - Bash is too complex for perfect parsing
   - Always have pattern-based fallback for edge cases

3. **Blocking Without Clear Reason**
   - Always provide `permissionDecisionReason`
   - Claude and users need to understand why

4. **Slow Validation Without Caching**
   - PreToolUse fires frequently
   - Cache AI validations, lint results, etc.

### Performance Considerations

| Pattern Type | Target Latency | Techniques |
|--------------|----------------|------------|
| Pattern matching | <10ms | Regex compilation, early exit |
| File checks | <20ms | Stat cache, async I/O |
| Lint/type check | <50ms | Result caching, incremental checks |
| AI validation | <100ms | Batch requests, response caching |

**Key Performance Tips**:
- Parse stdin once, pass parsed data to validation functions
- Use async/parallel for independent checks
- Cache results that don't change within session (lint config, ignore patterns)
- Exit early when possible (disabled guard, ignored file type)

### Testing Approach

1. **Unit Tests for Validators**
```typescript
describe('DangerousCommandValidator', () => {
  it('blocks rm -rf /', () => {
    const result = validateCommand({ command: 'rm -rf /' })
    expect(result.permissionDecision).toBe('deny')
  })

  it('allows rm -rf node_modules', () => {
    const result = validateCommand({ command: 'rm -rf node_modules' })
    expect(result.permissionDecision).toBeUndefined()
  })
})
```

2. **Integration Tests with Mock Payloads**
```typescript
describe('PreToolUse Handler', () => {
  it('processes Bash tool correctly', async () => {
    const payload = {
      hook_event_name: 'PreToolUse',
      tool_name: 'Bash',
      tool_input: { command: 'echo hello' }
    }
    const result = await handler(payload)
    expect(result).toEqual({})
  })
})
```

3. **E2E Tests with Claude Code**
- Create test project with hook configured
- Run Claude with scripted prompts
- Verify hook responses in audit log

4. **Manual Testing Checklist**
- [ ] Hook loads without error
- [ ] Safe commands pass through
- [ ] Dangerous commands are blocked
- [ ] Block reason is clear and helpful
- [ ] Performance is acceptable (<100ms typical)
- [ ] Guard disable works
- [ ] Guard re-enable works

---

## Appendix: Configuration Examples

### Basic Safety Hook

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash|Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "python .claude/hooks/safety.py"
          }
        ]
      }
    ]
  }
}
```

### TDD Enforcement

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit|MultiEdit",
        "hooks": [
          {
            "type": "command",
            "command": "npx tdd-guard"
          }
        ]
      }
    ]
  }
}
```

### TypeScript SDK (All Hooks)

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "bun .claude/hooks/index.ts PreToolUse"
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
            "command": "bun .claude/hooks/index.ts PostToolUse"
          }
        ]
      }
    ]
  }
}
```

---

*Generated from pattern analysis of: hooks-mastery-*, hooks-evanl1, safety-net, cc-tools-py, codex-settings, tdd-guard-*, cc-tools-go, claude-hooks-ts, awesome*
