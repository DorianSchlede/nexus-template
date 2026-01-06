# Context-Loading Research Results

## Executive Summary

Claude Code Hooks provide **6 distinct mechanisms** for injecting context into Claude's working memory. These range from invisible directives (`systemMessage`) to visible explanations (`permissionDecisionReason`) to silent input transformations (`updatedInput`). The most powerful insight is that hooks should not just block operations - they should **guide Claude** with explanations, alternatives, and next steps that help it learn project constraints.

---

## 1. The 6 Context Mechanisms

### 1.1 systemMessage

**What it does**: Injects invisible directives into Claude's context that only Claude sees - the user never sees this content. Ideal for behavioral steering, tool preferences, and workflow guidance.

**When to use**:
- Redirecting Claude to use alternative tools
- Providing contextual tips or warnings
- Injecting workflow-specific instructions
- Guiding Claude toward preferred patterns without cluttering user UI

**Visibility**: Invisible to user, only Claude sees it

**Which Hooks Support It**:
- PreToolUse: Inject guidance before tool execution
- PostToolUse: Provide context after tool completion
- SessionStart: Load project context at session initialization
- UserPromptSubmit: Add hidden context to prompts

**Code Example**:
```python
# Tool Redirection (from claude-codex-settings)
print(json.dumps({
    "systemMessage": "WebFetch detected. AI is directed to use Tavily extract instead.",
    "hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": f"Please use mcp__tavily__tavily-extract with urls: ['{url}']"
    }
}))
```

```python
# Quality Gate Error Context (from claude-codex-settings)
output = {
    'systemMessage': f'Ruff errors detected in {py_file.name}',
    'hookSpecificOutput': {
        'hookEventName': 'PostToolUse',
        'decision': 'block',
        'reason': error_msg
    },
}
```

**Best Practices**:
1. Keep it concise - systemMessage content consumes context window tokens
2. Be directive - use clear imperative language ("Use X instead of Y")
3. Complement with permissionDecisionReason - pair invisible guidance with visible explanation
4. Use for behavioral steering - ideal for workflow preferences, tool selection
5. Avoid sensitive data - content may be included in future API calls

**Nexus Application**: Use to inject skill-specific guidance when Claude attempts tool calls in skill directories. Could automatically load SKILL.md guidance without user seeing the injection.

---

### 1.2 permissionDecisionReason

**What it does**: Provides Claude with an explanation of why an operation was blocked and what to do instead. Creates a feedback loop that teaches Claude project constraints. Shown to the user when blocking.

**When to use**:
- Blocking dangerous operations with explanations
- Enforcing workflow rules with context
- Providing alternative approaches when denying actions
- Teaching Claude what to avoid in future attempts

**Visibility**: Shown to user when blocking

**Code Example**:
```python
# Safety Blocking with Alternatives (from claude-code-safety-net)
output = {
    "hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": f"""BLOCKED by Safety Net

Reason: {reason}

Command: {_redact_secrets(segment)[:100]}...

What to do:
- Use 'git stash' first if you want to save changes
- Use -d instead of -D for safer branch deletion
- Ask the user for explicit permission if this is truly needed"""
    }
}
```

```python
# TDD Enforcement (from tdd-guard)
return {
    'decision': 'block',
    'reason': '''Over-implementation violation detected.

You are implementing more than the minimum code needed to pass the current failing test.

Next steps:
1. Remove the extra implementation
2. Create only the empty class/function signature
3. Run tests to confirm they still fail for the right reason
4. Add implementation incrementally'''
}
```

**Anti-Patterns**:
1. Vague reasons: "Operation not allowed" - provides no guidance
2. Technical jargon only: "Exit code 2 from validator" - not actionable
3. Missing alternatives: Blocking without suggesting what to do instead
4. Overly long reasons: Wall of text that obscures the key point
5. No context: "Blocked" without explaining what was blocked

**Nexus Application**: When blocking operations that violate project rules (e.g., writing to wrong directories), provide clear explanation + alternative approach. Could be used to guide Claude to proper skill usage.

---

### 1.3 updatedInput

**What it does**: Silently modifies tool inputs before execution without user awareness. Powerful for enforcing consistency, upgrading parameters, or applying transformations.

**When to use**:
- Parameter normalization (relative to absolute paths)
- Adding default timeout values
- Injecting required flags
- Sanitizing inputs
- Converting deprecated parameter names
- Transparently routing to better tool implementations

**Security Implications**:
- Invisible changes: Users don't see the transformation
- Trust requirement: Should only modify in well-understood ways
- Audit trail: Consider logging original vs modified inputs
- Reversibility: Changes should be predictable and documented

**Code Example**:
```python
# Parameter Upgrading (from claude-codex-settings)
tool_input = data["tool_input"]
tool_input["extract_depth"] = "advanced"  # Upgrade from default

print(json.dumps({
    "hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "allow",
        "updatedInput": tool_input,
    }
}))
```

```python
# Tool Redirection (from claude-codex-settings)
if tool_name == "WebSearch":
    output = {
        "updatedToolName": "mcp__tavily__tavily_search",
        "updatedInput": {
            "query": tool_input.get("query", ""),
            "max_results": 5,
            "search_depth": "advanced"
        }
    }
    print(json.dumps(output))
```

```python
# Generic Pattern for Input Modification
def modify_tool_input(tool_name, tool_input):
    """Modify tool input before execution."""
    modified = tool_input.copy()

    if tool_name == "Bash":
        # Add timeout if not specified
        if "timeout" not in modified:
            modified["timeout"] = 30000

    elif tool_name == "Write":
        # Normalize file paths
        if "file_path" in modified:
            modified["file_path"] = os.path.abspath(modified["file_path"])

    return modified

print(json.dumps({
    "hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "allow",
        "updatedInput": modify_tool_input(tool_name, tool_input),
    }
}))
```

**Nexus Application**: Could normalize file paths to project directories, add standard parameters to skill script calls, or redirect tool calls to Nexus-enhanced versions.

---

### 1.4 Transcript Reading

**What it does**: Read conversation history from `transcript_path` field in hook payloads. Provides access to full JSONL transcript of current session for context-aware decisions.

**When to use**:
- Understanding conversation context for informed decisions
- Tracking what files were edited
- Determining test coverage state
- Analyzing user interaction patterns
- Session resumption context

**Privacy Considerations**:
- Transcripts contain full user prompts and Claude responses
- May include sensitive information shared during session
- Should redact secrets before logging
- Consider data retention policies

**Code Example**:
```go
// Token Metrics Extraction (from cc-tools-go)
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
                } `json:"usage"`
            } `json:"message"`
            IsSidechain bool `json:"isSidechain"`
        }

        if json.Unmarshal([]byte(line), &msg) == nil && msg.Message.Usage.InputTokens > 0 {
            metrics.InputTokens += msg.Message.Usage.InputTokens
            metrics.OutputTokens += msg.Message.Usage.OutputTokens
        }
    }
    return metrics
}
```

```typescript
// Conversation History Extraction (from claude-hooks TypeScript)
export async function getConversationHistory(transcriptPath: string): Promise<Array<{role: 'user' | 'assistant'; content: string}>> {
    const fileStream = fs.createReadStream(transcriptPath)
    const rl = readline.createInterface({ input: fileStream, crlfDelay: Infinity })
    const history: Array<{role: 'user' | 'assistant'; content: string}> = []

    for await (const line of rl) {
        if (!line.trim()) continue
        const message = JSON.parse(line) as TranscriptMessage
        if (message.type === 'summary') continue

        if (message.type === 'user' && typeof message.message.content === 'string') {
            history.push({ role: 'user', content: message.message.content })
        }
        if (message.type === 'assistant') {
            const textContent = message.message.content
                .filter(c => c.type === 'text')
                .map(c => c.text)
                .join('\n')
            if (textContent) {
                history.push({ role: 'assistant', content: textContent })
            }
        }
    }
    return history
}
```

```typescript
// Initial Message Extraction (from claude-hooks TypeScript)
export async function getInitialMessage(transcriptPath: string): Promise<string | null> {
    const fileStream = fs.createReadStream(transcriptPath)
    const rl = readline.createInterface({ input: fileStream, crlfDelay: Infinity })

    for await (const line of rl) {
        if (!line.trim()) continue
        const message = JSON.parse(line) as TranscriptMessage
        if (message.type === 'summary') continue
        if (message.type === 'user' && message.message.role === 'user') {
            if (typeof message.message.content === 'string') {
                return message.message.content
            }
        }
    }
    return null
}
```

**Nexus Application**: Could analyze transcript to detect which project/skill Claude is working on and auto-inject relevant context. Could track file edits to update project progress automatically.

---

### 1.5 State Files

**What it does**: Persist data between hook invocations using files in `.claude/` directories or temp directories. Enables cross-invocation communication since hooks execute as separate processes.

**When to use**:
- Maintaining state across multiple hook invocations
- Two-phase notification patterns (warn first, block on repeat)
- Speed bump patterns (allow override after warning)
- Tracking session history for audit/debugging
- Storing configuration and rules

**File Formats**: JSON is dominant due to native support in all languages, easy atomic read/write, and human-readability for debugging.

**Code Example**:
```typescript
// Storage Interface (from tdd-guard)
export const TRANSIENT_DATA = ['test', 'todo', 'modifications', 'lint'] as const

export interface Storage {
    saveTest(content: string): Promise<void>
    saveTodo(content: string): Promise<void>
    saveModifications(content: string): Promise<void>
    saveLint(content: string): Promise<void>
    saveConfig(content: string): Promise<void>
    getTest(): Promise<string | null>
    getTodo(): Promise<string | null>
    getModifications(): Promise<string | null>
    getLint(): Promise<string | null>
    getConfig(): Promise<string | null>
    clearTransientData(): Promise<void>  // Called on SessionStart
}

// File paths in .claude/tdd-guard/data/
// - test.json: Latest test results
// - todos.json: Claude's current todo list
// - modifications.json: File change history
// - lint.json: Lint results with notification flag
// - config.json: Guard enable/disable state
```

```typescript
// Two-Phase Notification Pattern (from tdd-guard)
interface LintData {
    errorCount: number
    warningCount: number
    issues: Array<{file: string; line: number; message: string}>
    hasNotifiedAboutLintIssues: boolean  // State flag
}

// PreToolUse: First warning
if (hasIssues && !lintData.hasNotifiedAboutLintIssues) {
    await storage.saveLint(JSON.stringify({
        ...lintData,
        hasNotifiedAboutLintIssues: true  // Set flag
    }))
    return { decision: 'block', reason: 'Code quality issues detected...' }
}

// PostToolUse: Block on repeat
if (storedLintData?.hasNotifiedAboutLintIssues && hasIssues) {
    return createBlockResult(lintData)  // Now block hard
}
```

```python
# Speed Bump Pattern (from claude-code-tools)
flag_file = Path('.claude_file_length_warning.flag')

if flag_file.exists():
    flag_file.unlink()  # Clear flag, allow operation this time
    return False, None

# First attempt - block and create flag
flag_file.touch()
return True, f"File would be {resulting_lines} lines. Ask user to approve or refactor."
```

```python
# Audit Logging (from claude-code-safety-net)
def _write_audit_log(session_id, command, segment, reason, cwd) -> None:
    logs_dir = Path.home() / ".cc-safety-net" / "logs"
    safe_session_id = _sanitize_session_id_for_filename(session_id)

    logs_dir.mkdir(parents=True, exist_ok=True)
    log_file = logs_dir / f"{safe_session_id}.jsonl"

    entry = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "command": _redact_secrets(command)[:300],  # Truncate and redact
        "segment": _redact_secrets(segment)[:300],
        "reason": reason,
        "cwd": cwd,
    }

    with log_file.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")
```

**Nexus Application**: Already partially used (save_resume_state.py in PreCompact). Could expand to track which skills have been invoked, project progress, and session continuity data.

---

### 1.6 hookSpecificOutput.additionalContext

**What it does**: Inject context at session start via the `additionalContext` field in `hookSpecificOutput`. This is the primary mechanism for SessionStart hooks to provide Claude with project awareness.

**When to use**:
- Session initialization context (git status, project state)
- Loading project-specific files (TODO.md, CONTEXT.md)
- Injecting GitHub issues or other external context
- One-time context load at session beginning

**Code Example**:
```python
# Development Context Injection (from hooks-mastery)
def load_development_context(source):
    """Load relevant development context based on session source."""
    context_parts = []

    context_parts.append(f"Session started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    context_parts.append(f"Session source: {source}")

    # Git status
    branch, changes = get_git_status()
    if branch:
        context_parts.append(f"Git branch: {branch}")
        if changes > 0:
            context_parts.append(f"Uncommitted changes: {changes} files")

    # Project files
    context_files = [
        ".claude/CONTEXT.md", ".claude/TODO.md",
        "TODO.md", ".github/ISSUE_TEMPLATE.md"
    ]

    for file_path in context_files:
        if Path(file_path).exists():
            with open(file_path, 'r') as f:
                content = f.read().strip()[:1000]  # Truncate
                context_parts.append(f"\n--- Content from {file_path} ---")
                context_parts.append(content)

    # GitHub issues
    issues = get_recent_issues()
    if issues:
        context_parts.append("\n--- Recent GitHub Issues ---")
        context_parts.append(issues)

    return "\n".join(context_parts)

# Return via hookSpecificOutput
output = {
    "hookSpecificOutput": {
        "hookEventName": "SessionStart",
        "additionalContext": load_development_context(source)
    }
}
print(json.dumps(output))
```

```typescript
// Auto Context Files on User Prompt (from claude-hooks TypeScript)
const userPromptSubmit: UserPromptSubmitHandler = async (payload) => {
    const contextFiles: string[] = []

    if (payload.prompt.toLowerCase().includes('test')) {
        contextFiles.push('**/*.test.ts', '**/*.test.js')
    }

    return contextFiles.length > 0 ? {contextFiles} : {}
}
```

**Nexus Application**: Already used in session_start.py! Current implementation runs nexus-loader and injects a slim summary pointing to the cache file. Could be enhanced to include more dynamic context based on session type.

---

## 2. Gap Analysis

### What Nexus Currently Uses:

| Mechanism | Current Status | Notes |
|-----------|---------------|-------|
| SessionStart additionalContext | **USED** | Via nexus-loader cache file pointer |
| systemMessage | **NOT USED** | Major opportunity for skill-aware guidance |
| permissionDecisionReason | **NOT USED** | Could guide when blocking operations |
| updatedInput | **NOT USED** | Could normalize paths, add parameters |
| Transcript reading | **NOT USED** | Could detect project context from conversation |
| State files | **PARTIALLY USED** | save_resume_state.py exists, but limited |

### Current session_start.py Analysis:

**What it does**:
1. Runs nexus-loader.py to populate/refresh cache
2. Reads cache file and extracts slim summary
3. Outputs pointer to cache file with MANDATORY STOP instruction
4. Sends session start event to server
5. Ensures background server is running

**What it outputs**:
```
<NexusContext source="startup" session="...">
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!  MANDATORY STOP - DO NOT CONTINUE WORKING                  !!!
!!!  YOU MUST READ THE CACHE FILE BEFORE ANY OTHER ACTION      !!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

System State: active
Active Projects: 3
  - 02: Ontologies Research (75%)
    Current: Synthesize findings into report
...

REQUIRED FIRST ACTION:
  Read("00-system/.cache/context_startup.json")
</NexusContext>
```

**Gap**: Currently uses only `additionalContext` via print(). Does NOT use proper JSON output format with `hookSpecificOutput`.

### Opportunities:

1. **Skill-Aware Context (UserPromptSubmit)**: Detect skill keywords in user prompts and inject SKILL.md content as systemMessage
2. **Project-Aware Context (PreToolUse)**: When tool targets file in project folder, inject project overview
3. **Block Guidance (PreToolUse)**: Use systemMessage + permissionDecisionReason when blocking dangerous operations
4. **Input Normalization (PreToolUse)**: Normalize file paths to project directories using updatedInput
5. **Conversation Context (UserPromptSubmit)**: Read transcript to detect ongoing project/skill work
6. **Two-Phase Warnings**: Implement speed bump pattern for destructive operations

---

## 3. Recommendations for Automatic Loading

### 3.1 Skill-Aware Context (UserPromptSubmit)

**Trigger**: User message matches skill description/keywords
**Action**: Inject SKILL.md content as systemMessage
**Hook to Modify**: NEW - user_prompt_submit.py

**Implementation**:
```python
#!/usr/bin/env python3
"""UserPromptSubmit hook - Skill-aware context injection."""
import json
import sys
from pathlib import Path

def load_skills_index():
    """Load skills from cache or scan."""
    cache_path = Path("00-system/.cache/context_startup.json")
    if cache_path.exists():
        data = json.loads(cache_path.read_text())
        return data.get("metadata", {}).get("skills", [])
    return []

def match_skill(prompt: str, skills: list) -> dict | None:
    """Find best matching skill based on prompt keywords."""
    prompt_lower = prompt.lower()
    for skill in skills:
        # Check name match
        if skill.get("name", "").lower() in prompt_lower:
            return skill
        # Check trigger keywords
        for trigger in skill.get("triggers", []):
            if trigger.lower() in prompt_lower:
                return skill
    return None

def load_skill_content(skill_path: str) -> str:
    """Load SKILL.md content for injection."""
    skill_md = Path(skill_path) / "SKILL.md"
    if skill_md.exists():
        content = skill_md.read_text()[:2000]  # Truncate for context window
        return f"[Skill Guidance: {skill_path}]\n{content}"
    return ""

def main():
    try:
        data = json.load(sys.stdin)
        prompt = data.get("prompt", "")

        skills = load_skills_index()
        matched = match_skill(prompt, skills)

        if matched:
            skill_content = load_skill_content(matched.get("path", ""))
            if skill_content:
                output = {
                    "systemMessage": skill_content,
                    "hookSpecificOutput": {
                        "hookEventName": "UserPromptSubmit"
                    }
                }
                print(json.dumps(output))
                sys.exit(0)

        # No match - pass through
        sys.exit(0)
    except Exception:
        sys.exit(0)  # Never block on errors

if __name__ == "__main__":
    main()
```

**Database Impact**: None - additive only, does not modify existing session start flow

---

### 3.2 Project-Aware Context (PreToolUse)

**Trigger**: Tool call targets file in project folder (02-projects/*)
**Action**: Load project overview.md + current task as systemMessage
**Hook to Modify**: NEW or enhance pre_tool_use.py

**Implementation**:
```python
#!/usr/bin/env python3
"""PreToolUse hook - Project-aware context injection."""
import json
import sys
from pathlib import Path
import re

def extract_project_from_path(file_path: str) -> str | None:
    """Extract project ID from file path like 02-projects/07-test/..."""
    match = re.match(r'.*02-projects/(\d+)-[^/]+', file_path)
    if match:
        return match.group(1)
    return None

def load_project_context(project_id: str) -> str:
    """Load project overview and current task."""
    project_dir = Path(f"02-projects/{project_id:02d}-*").parent

    # Try to find matching project directory
    projects = list(Path("02-projects").glob(f"{project_id.zfill(2)}-*"))
    if not projects:
        return ""

    project_path = projects[0]
    context_parts = []

    # Load overview if exists
    overview = project_path / "01-planning" / "overview.md"
    if overview.exists():
        context_parts.append(f"[Project Overview]\n{overview.read_text()[:1000]}")

    # Load current task from steps.md
    steps = project_path / "01-planning" / "steps.md"
    if steps.exists():
        content = steps.read_text()
        # Extract current (incomplete) task
        lines = content.split('\n')
        for line in lines:
            if '[ ]' in line:  # First incomplete task
                context_parts.append(f"[Current Task] {line.strip()}")
                break

    return "\n".join(context_parts)

def main():
    try:
        data = json.load(sys.stdin)
        tool_name = data.get("tool_name", "")
        tool_input = data.get("tool_input", {})

        # Only process file operations
        file_path = tool_input.get("file_path") or tool_input.get("path", "")
        if not file_path:
            sys.exit(0)

        project_id = extract_project_from_path(file_path)
        if project_id:
            context = load_project_context(project_id)
            if context:
                output = {
                    "systemMessage": context,
                    "hookSpecificOutput": {
                        "hookEventName": "PreToolUse",
                        "permissionDecision": "allow"
                    }
                }
                print(json.dumps(output))
                sys.exit(0)

        sys.exit(0)
    except Exception:
        sys.exit(0)

if __name__ == "__main__":
    main()
```

**Database Impact**: None - additive guidance only

---

### 3.3 Block Guidance (PreToolUse)

**Trigger**: When blocking a dangerous operation (rm, git reset, etc.)
**Action**: Use systemMessage + permissionDecisionReason to provide both invisible guidance and visible explanation

**Implementation**:
```python
def block_with_guidance(reason: str, guidance: str, alternative: str):
    """Block operation with both visible reason and invisible guidance."""
    output = {
        "systemMessage": guidance,  # Claude sees this
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": f"""BLOCKED: {reason}

Alternative: {alternative}

If you need to proceed, ask the user for explicit permission."""
        }
    }
    print(json.dumps(output))
    sys.exit(0)

# Example usage:
if "rm -rf" in command:
    block_with_guidance(
        reason="Destructive rm command detected",
        guidance="Remember: Nexus uses TRASH pattern. Move files to TRASH/ instead of deleting.",
        alternative="Move files to 04-workspace/TRASH/ directory instead"
    )
```

---

### 3.4 Proper JSON Output for SessionStart

**Current Issue**: session_start.py uses `print()` directly instead of proper JSON format
**Trigger**: Every session start
**Action**: Output proper JSON with hookSpecificOutput.additionalContext

**Implementation**:
```python
# In session_start.py, replace direct print with:
output = {
    "hookSpecificOutput": {
        "hookEventName": "SessionStart",
        "additionalContext": f"""<NexusContext source="{source}" session="{session_id}">
{summary}

REQUIRED FIRST ACTION:
  Read("{cache_path}")

This file contains your behavior rules and project state.
</NexusContext>"""
    }
}
print(json.dumps(output))
```

**Database Impact**: None - same server calls preserved

---

### 3.5 Auto Context Files (UserPromptSubmit)

**Trigger**: User prompt contains keywords like "test", "config", "readme"
**Action**: Automatically add relevant files to context via `contextFiles` field

**Implementation**:
```python
def get_context_files(prompt: str) -> list[str]:
    """Determine context files to inject based on prompt keywords."""
    files = []
    prompt_lower = prompt.lower()

    if "test" in prompt_lower:
        files.extend(["**/*.test.*", "**/*_test.*", "**/test_*.py"])

    if "config" in prompt_lower:
        files.extend(["**/config.*", "**/*.config.*", "**/*.yaml", "**/*.json"])

    if "skill" in prompt_lower:
        files.extend(["03-skills/**/SKILL.md"])

    if "project" in prompt_lower:
        files.extend(["02-projects/**/overview.md", "02-projects/**/_resume.md"])

    return files

# In UserPromptSubmit hook:
context_files = get_context_files(prompt)
if context_files:
    print(json.dumps({"contextFiles": context_files}))
```

---

### 3.6 Two-Phase Warning Pattern

**Trigger**: First attempt at risky operation
**Action**: Warn on first attempt, block on repeat without explicit approval

**Implementation**:
```python
def check_speed_bump(operation_id: str) -> bool:
    """Check if this operation should be allowed (second attempt)."""
    flag_file = Path(f".claude/warnings/{operation_id}.warned")

    if flag_file.exists():
        flag_file.unlink()  # Clear flag
        return True  # Allow this time

    # First attempt - create warning flag
    flag_file.parent.mkdir(parents=True, exist_ok=True)
    flag_file.touch()
    return False  # Block this time

# Usage in PreToolUse:
if is_risky_operation(command):
    op_id = hashlib.md5(command.encode()).hexdigest()[:8]
    if not check_speed_bump(op_id):
        output = {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": """This operation may have unintended consequences.

If you're sure you want to proceed, try again immediately.
Otherwise, consider an alternative approach."""
            }
        }
        print(json.dumps(output))
        sys.exit(0)
```

---

## 4. Code Templates (Copy-Paste Ready)

### Template: systemMessage Output
```python
def output_with_system_message(message: str, allow: bool = True):
    """Output hook result with system message for Claude."""
    output = {
        "systemMessage": message,
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "allow" if allow else "deny"
        }
    }
    print(json.dumps(output))
    sys.exit(0)
```

### Template: permissionDecisionReason Output
```python
def block_with_reason(reason: str, alternatives: list[str] = None):
    """Block operation with explanation and alternatives."""
    reason_text = f"BLOCKED: {reason}"
    if alternatives:
        reason_text += "\n\nAlternatives:\n" + "\n".join(f"- {a}" for a in alternatives)

    output = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason_text
        }
    }
    print(json.dumps(output))
    sys.exit(0)
```

### Template: Skill-Aware Routing
```python
def route_to_skill(skill_name: str, skill_guidance: str):
    """Inject skill guidance as system message."""
    output = {
        "systemMessage": f"[{skill_name} Skill Active]\n{skill_guidance}",
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit"
        }
    }
    print(json.dumps(output))
    sys.exit(0)
```

### Template: SessionStart Context Injection
```python
def inject_session_context(context: str, source: str):
    """Inject context at session start."""
    output = {
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": context
        }
    }
    print(json.dumps(output))
    sys.exit(0)
```

### Template: Updated Tool Input
```python
def modify_and_allow(tool_input: dict, modifications: dict):
    """Allow operation with modified input parameters."""
    updated = {**tool_input, **modifications}
    output = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "allow",
            "updatedInput": updated
        }
    }
    print(json.dumps(output))
    sys.exit(0)
```

### Template: Context Files Injection
```python
def inject_context_files(file_patterns: list[str]):
    """Add files to Claude's context based on patterns."""
    output = {
        "contextFiles": file_patterns,
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit"
        }
    }
    print(json.dumps(output))
    sys.exit(0)
```

---

## 5. Integration Notes

### Must Preserve
- Existing database calls in session_start.py (`send_to_server()`)
- Server startup logic (`ensure_server_running()`)
- Exit code conventions (0=allow/success, 2=block)
- Cache file generation and reading
- Session ID tracking for multi-instance support

### Safe to Add
- systemMessage output (additive to any hook)
- New context injection via hookSpecificOutput.additionalContext
- Skill matching logic in UserPromptSubmit (new functionality)
- Project context in PreToolUse (new functionality)
- Two-phase warning state files (new state management)

### Performance Considerations

| Mechanism | Overhead | Optimization Tips |
|-----------|----------|-------------------|
| systemMessage | Minimal | Keep under 500 chars |
| permissionDecisionReason | Minimal | Truncate long outputs |
| updatedInput | Minimal | Avoid deep copies |
| Transcript reading | 50-100ms | Stream parsing, early exit |
| State files | 10-50ms | Use JSON, not YAML |
| Skill matching | 10-50ms | Cache skills index |

**Total Budget**: Keep SessionStart hooks under 200ms, PreToolUse under 50ms, UserPromptSubmit under 100ms.

### Exit Code Reference

| Code | Meaning | Use Case |
|------|---------|----------|
| 0 | Success, allow | Logging, context injection, passthrough |
| 1 | Error (allow) | Hook failure, graceful degradation |
| 2 | Block | Policy violation, dangerous content |

---

## Summary

The 6 context mechanisms provide a comprehensive toolkit for injecting context into Claude:

1. **systemMessage**: Invisible guidance for Claude only
2. **permissionDecisionReason**: Visible explanation when blocking
3. **updatedInput**: Silent tool input transformation
4. **Transcript reading**: Historical conversation analysis
5. **State files**: Cross-invocation persistence
6. **hookSpecificOutput.additionalContext**: Session start context

Nexus currently uses only `additionalContext` at SessionStart. The biggest opportunities are:
- **systemMessage** for skill-aware guidance
- **permissionDecisionReason** for better block explanations
- **State files** for two-phase warning patterns
- **Transcript reading** for automatic project detection

All recommendations are additive and preserve existing database integration.
