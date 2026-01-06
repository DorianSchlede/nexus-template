# Subagent Briefing: Context-Loading Research

**Priority**: HIGHEST
**Output Path**: `02-projects/18-hook-research-upgrade/02-resources/research-context-loading.md`

---

## Mission

Understand ALL context injection mechanisms in Claude Code Hooks. Analyze how Nexus can use these to automatically load context at relevant points WITHOUT breaking the existing database connection.

---

## Required Reading (IN ORDER - READ EVERYTHING)

### Step 1: Understand Research Structure
```
READ: 04-workspace/00-ai-native-org/hook-research/_index.md
```
Navigation hub showing where everything is.

### Step 2: MAIN DOCUMENT - Context Loading Deep Dive
```
READ: 04-workspace/00-ai-native-org/hook-research/hook-guides/CONTEXT_LOADING.md
```
**28KB - READ COMPLETELY!** Contains:
- 6 context mechanisms (systemMessage, permissionDecisionReason, updatedInput, etc.)
- Code examples for each mechanism
- Best practices and anti-patterns

### Step 3: Code Patterns for Context Loading
```
READ: 04-workspace/00-ai-native-org/hook-research/patterns/context-loading.yaml
```
YAML with concrete code snippets.

### Step 4: SessionStart Patterns
```
READ: 04-workspace/00-ai-native-org/hook-research/hook-guides/SESSION_START.md
```
How context is injected at session start.

### Step 5: UserPromptSubmit Patterns
```
READ: 04-workspace/00-ai-native-org/hook-research/hook-guides/USER_PROMPT.md
```
How context is injected on user input (skill-aware routing).

---

## Current Nexus System (FOR COMPARISON)

### Current Context Injection
```
READ: .claude/hooks/session_start.py
```
What does Nexus currently do at SessionStart?

### What Gets Loaded?
```
READ: 00-system/core/nexus-loader.py (first 300 lines)
```
What data does the Nexus loader provide?

---

## Output Format

Create file at:
```
02-projects/18-hook-research-upgrade/02-resources/research-context-loading.md
```

Structure:

```markdown
# Context-Loading Research Results

## Executive Summary
[2-3 sentences: What context loading mechanisms exist?]

---

## 1. The 6 Context Mechanisms

### 1.1 systemMessage
**What it does**: [Description]
**When to use**: [Use cases]
**Visibility**: Invisible to user, only Claude sees it
**Code Example**:
\`\`\`python
print(json.dumps({
    "systemMessage": "Your guidance here...",
    "hookSpecificOutput": {...}
}))
\`\`\`
**Nexus Application**: [How could Nexus use this?]

### 1.2 permissionDecisionReason
**What it does**: [Description]
**When to use**: [Use cases]
**Visibility**: Shown to user when blocking
**Code Example**:
\`\`\`python
[Code from research]
\`\`\`
**Nexus Application**: [How could Nexus use this?]

### 1.3 updatedInput
**What it does**: Silently modifies tool input before execution
**When to use**: [Use cases]
**Security implications**: [Notes]
**Code Example**:
\`\`\`python
[Code from research]
\`\`\`
**Nexus Application**: [How could Nexus use this?]

### 1.4 Transcript Reading
**What it does**: Read conversation history from transcript_path
**When to use**: [Use cases]
**Code Example**:
\`\`\`python
[Code from research]
\`\`\`
**Nexus Application**: [How could Nexus use this?]

### 1.5 State Files
**What it does**: Persist data between hook invocations
**When to use**: [Use cases]
**Code Example**:
\`\`\`python
[Code from research]
\`\`\`
**Nexus Application**: [How could Nexus use this?]

### 1.6 hookSpecificOutput.additionalContext
**What it does**: Inject context at session start
**When to use**: [Use cases]
**Code Example**:
\`\`\`python
[Code from research]
\`\`\`
**Nexus Application**: [Already used in session_start.py]

---

## 2. Gap Analysis

### What Nexus Currently Uses:
- [x] SessionStart additionalContext (via nexus-loader)
- [ ] systemMessage - NOT USED
- [ ] permissionDecisionReason - NOT USED
- [ ] updatedInput - NOT USED
- [ ] Transcript reading - NOT USED
- [ ] State files - Partially (save_resume_state.py)

### Opportunities:
1. [Opportunity 1 with concrete use case]
2. [Opportunity 2 with concrete use case]
...

---

## 3. Recommendations for Automatic Loading

### 3.1 Skill-Aware Context (UserPromptSubmit)
**Trigger**: User message matches skill description
**Action**: Inject SKILL.md content as systemMessage
**Hook to Modify**: user_prompt_submit.py
**Implementation**:
\`\`\`python
[Concrete code]
\`\`\`
**Database Impact**: None - does not change event flow

### 3.2 Project-Aware Context (PreToolUse)
**Trigger**: Tool call targets file in project folder
**Action**: Load project overview.md + current task
**Hook to Modify**: pre_tool_use.py
**Implementation**:
\`\`\`python
[Concrete code]
\`\`\`
**Database Impact**: None - additive only

### 3.3 Block Guidance (PreToolUse)
**Trigger**: When blocking a dangerous operation
**Action**: Use systemMessage + permissionDecisionReason to guide
**Implementation**:
\`\`\`python
[Concrete code]
\`\`\`

### 3.4 [More recommendations...]

---

## 4. Code Templates (Copy-Paste Ready)

### Template: systemMessage Output
\`\`\`python
def output_with_system_message(message: str, allow: bool = True):
    output = {
        "systemMessage": message,
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "allow" if allow else "deny"
        }
    }
    print(json.dumps(output))
    sys.exit(0 if allow else 2)
\`\`\`

### Template: permissionDecisionReason Output
\`\`\`python
[Ready-to-use code]
\`\`\`

### Template: Skill-Aware Routing
\`\`\`python
[Ready-to-use code]
\`\`\`

---

## 5. Integration Notes

### Must Preserve
- Existing database calls in session_start.py
- send_to_server() calls must remain unchanged
- Exit code conventions (0=allow, 2=block)

### Safe to Add
- systemMessage output (additive)
- New context injection (additive)
- Skill matching logic (new functionality)
```

---

## Success Criteria

- [ ] All 6 mechanisms documented with code examples
- [ ] Gap analysis between research and current Nexus system
- [ ] At least 4 concrete recommendations for automatic loading
- [ ] Copy-paste-ready code templates
- [ ] Database impact clearly noted for each recommendation

---

## DO NOT

- ❌ Implement anything - research only
- ❌ Skip documents - read everything
- ❌ Invent patterns - only extract from research
- ❌ Write too briefly - we need details
- ❌ Suggest removing database calls
