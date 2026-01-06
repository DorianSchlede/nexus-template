# Subagent Briefing: Safety Patterns Research

**Priority**: HIGH
**Output Path**: `02-projects/18-hook-research-upgrade/02-resources/research-safety-patterns.md`

---

## Mission

Extract ALL safety patterns from research with complete regex patterns, TRASH implementation, and permissionDecisionReason templates. Analyze how to integrate these into Nexus pre_tool_use.py WITHOUT breaking database connections.

---

## Required Reading (IN ORDER - READ EVERYTHING)

### Step 1: Understand Research Structure
```
READ: 04-workspace/00-ai-native-org/hook-research/_index.md
```
Navigation hub.

### Step 2: PreToolUse Guide (MAIN DOCUMENT)
```
READ: 04-workspace/00-ai-native-org/hook-research/hook-guides/PRE_TOOL_USE.md
```
**33KB - READ COMPLETELY!** 60%+ of all patterns are here. Contains:
- Safety gate patterns
- Blocking mechanisms
- Exit codes (0=allow, 2=block)

### Step 3: Safety-Net Patterns (18 PATTERNS!)
```
READ: 04-workspace/00-ai-native-org/hook-research/patterns/safety-net.yaml
```
**CRITICAL!** Contains:
- rm -rf regex patterns
- git reset/force patterns
- .env protection patterns
- Secret redaction helpers

### Step 4: TRASH Pattern + More
```
READ: 04-workspace/00-ai-native-org/hook-research/patterns/cc-tools-py.yaml
```
Contains the TRASH pattern implementation (move instead of delete).

---

## Current Nexus System (FOR COMPARISON)

### Current PreToolUse
```
READ: .claude/hooks/pre_tool_use.py
```
What does Nexus currently check? What does it block? What events does it send to the database?

---

## Output Format

Create file at:
```
02-projects/18-hook-research-upgrade/02-resources/research-safety-patterns.md
```

Structure:

```markdown
# Safety Patterns Research Results

## Executive Summary
[2-3 sentences: What safety patterns exist?]

---

## 1. Dangerous Command Patterns

### 1.1 rm -rf / Destructive Delete
**Danger**: Deletes files irrecoverably
**Regex Patterns** (from safety-net.yaml):
\`\`\`python
RM_PATTERNS = [
    r"\brm\s+.*-[a-z]*r[a-z]*f",      # rm -rf, rm -fr, rm -Rf
    r"\brm\s+.*-[a-z]*f[a-z]*r",      # rm -fr variants
    r"\brm\s+--recursive\s+--force",  # Long form
    r"\brm\s+--force\s+--recursive",  # Long form alt
    r"\brm\s+-r\s+.*-f",              # Separated flags
    r"\brm\s+-f\s+.*-r",              # Separated flags alt
]
\`\`\`

**Dangerous Paths** (block additionally):
\`\`\`python
DANGEROUS_PATHS = [
    r"/",       # Root
    r"/\*",     # Root wildcard
    r"~",       # Home
    r"~/",      # Home path
    r"\$HOME",  # Home env
    r"\.\.",    # Parent refs
    r"\.",      # Current dir
]
\`\`\`

**permissionDecisionReason Template**:
\`\`\`
BLOCKED: Destructive delete command detected

Command: {command}

Instead:
- Use TRASH pattern: mv {file} ./TRASH/
- Create TRASH-FILES.md with deletion log
- Or ask user for explicit confirmation

Why this is dangerous:
- Files cannot be recovered after rm -rf
- May delete more than intended with wildcards
\`\`\`

---

### 1.2 git reset --hard / Force Operations
**Danger**: Loses uncommitted changes permanently
**Regex Patterns**:
\`\`\`python
GIT_DANGEROUS_PATTERNS = [
    r"git\s+reset\s+--hard",
    r"git\s+push\s+.*--force",
    r"git\s+push\s+.*-f\b",
    r"git\s+branch\s+-[dD]\s+",
    r"git\s+checkout\s+--\s+\.",
    r"git\s+clean\s+-[a-z]*f",
]
\`\`\`

**permissionDecisionReason Template**:
\`\`\`
BLOCKED: Dangerous git operation detected

Command: {command}

Instead:
- git stash (to save changes first)
- git branch backup-{date} (before force operations)
- Ask user for explicit confirmation

Why this is dangerous:
- Uncommitted changes will be lost forever
- Cannot be recovered with git reflog in all cases
\`\`\`

---

### 1.3 .env File Access
**Danger**: Credentials exposure
**Regex Patterns**:
\`\`\`python
ENV_PATTERNS = [
    r"\.env\b(?!\.sample)",         # .env but not .env.sample
    r"cat\s+.*\.env\b(?!\.sample)",
    r"echo\s+.*>\s*\.env\b",
    r"touch\s+.*\.env\b",
    r"cp\s+.*\.env\b",
    r"mv\s+.*\.env\b",
]
\`\`\`

**Tools to Check**: Read, Edit, Write, Bash

**permissionDecisionReason Template**:
\`\`\`
BLOCKED: Credential file access detected

File: {file_path}

Environment files contain secrets that should not be:
- Read into context
- Modified programmatically
- Copied or moved without explicit permission

Instead:
- Use .env.sample as reference
- Ask user for specific values needed
\`\`\`

---

## 2. TRASH Pattern Implementation

**Concept**: Instead of `rm`, move to TRASH folder

**Implementation** (from cc-tools-py.yaml):
\`\`\`python
def handle_rm_command(command: str, cwd: str) -> tuple[bool, str]:
    """
    Returns (should_block, reason_text)
    """
    # Check if rm command
    if not re.search(r"\brm\b", command):
        return False, None

    reason_text = (
        "Instead of using 'rm':\\n"
        "- MOVE files using `mv` to TRASH directory in CURRENT folder\\n"
        "- Create TRASH/ if it doesn't exist\\n"
        "- Add entry in TRASH-FILES.md with:\\n"
        "  - File name\\n"
        "  - Where it was moved\\n"
        "  - Reason for deletion\\n"
        "  - Date"
    )
    return True, reason_text
\`\`\`

**TRASH-FILES.md Format**:
\`\`\`markdown
# Deleted Files Log

| File | Moved To | Reason | Date |
|------|----------|--------|------|
| old_config.py | ./TRASH/old_config.py | Replaced by new config | 2026-01-01 |
\`\`\`

---

## 3. Secret Redaction Helper

**From safety-net.yaml**:
\`\`\`python
def redact_secrets(text: str) -> str:
    """Redact sensitive values before logging."""
    redacted = text
    # KEY=VALUE patterns
    redacted = re.sub(
        r"\b([A-Z0-9_]*(?:TOKEN|SECRET|PASSWORD|KEY)[A-Z0-9_]*)=([^\s]+)",
        r"\1=<redacted>",
        redacted, flags=re.IGNORECASE
    )
    # Authorization headers
    redacted = re.sub(r"(?i)(authorization\s*:\s*)([^\s\"']+)", r"\1<redacted>", redacted)
    # GitHub tokens
    redacted = re.sub(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b", "<redacted>", redacted)
    return redacted
\`\`\`

---

## 4. Integration with Current pre_tool_use.py

### Current State Analysis
[Document what pre_tool_use.py currently does]
[Note all database calls that MUST be preserved]

### Upgrade Plan (ADDITIVE ONLY)

\`\`\`python
# Add these functions - DO NOT remove existing code

def is_dangerous_rm_command(command: str) -> bool:
    for pattern in RM_PATTERNS:
        if re.search(pattern, command, re.IGNORECASE):
            return True
    return False

def is_dangerous_git_command(command: str) -> bool:
    for pattern in GIT_DANGEROUS_PATTERNS:
        if re.search(pattern, command, re.IGNORECASE):
            return True
    return False

def is_env_file_access(tool_name: str, tool_input: dict) -> bool:
    # Check Read, Edit, Write tools
    file_path = tool_input.get("file_path", "")
    if re.search(r"\.env\b(?!\.sample)", file_path):
        return True
    # Check Bash for .env access
    if tool_name == "Bash":
        command = tool_input.get("command", "")
        for pattern in ENV_PATTERNS:
            if re.search(pattern, command):
                return True
    return False

def output_block(reason: str, guidance: str):
    output = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": f"{reason}\\n\\n{guidance}"
        }
    }
    print(json.dumps(output))
\`\`\`

### Integration Point
\`\`\`python
# In main() - ADD to existing checks, don't replace

if tool_name == "Bash":
    command = tool_input.get("command", "")

    # NEW: Safety checks
    if is_dangerous_rm_command(command):
        output_block("Destructive delete detected", TRASH_GUIDANCE)
        sys.exit(2)

    if is_dangerous_git_command(command):
        output_block("Dangerous git operation", GIT_GUIDANCE)
        sys.exit(2)

# NEW: .env protection (for all tools)
if is_env_file_access(tool_name, tool_input):
    output_block("Credential file access", ENV_GUIDANCE)
    sys.exit(2)

# PRESERVE: All existing database calls
# ... existing code continues ...
\`\`\`

---

## 5. Complete Regex Reference (Copy-Paste)

### All rm Patterns
\`\`\`python
RM_PATTERNS = [
    # Complete list from safety-net.yaml
]
\`\`\`

### All git Patterns
\`\`\`python
GIT_DANGEROUS_PATTERNS = [
    # Complete list
]
\`\`\`

### All .env Patterns
\`\`\`python
ENV_PATTERNS = [
    # Complete list
]
\`\`\`

---

## 6. Database Impact Analysis

### Existing Database Calls (MUST PRESERVE)
[List all send_to_server() or send_event() calls in pre_tool_use.py]

### New Code (NO Database Impact)
- Safety check functions: pure Python, no external calls
- Block output: only JSON to stdout
- Exit codes: standard (0=allow, 2=block)
```

---

## Success Criteria

- [ ] All rm -rf regex patterns extracted
- [ ] All git dangerous patterns extracted
- [ ] All .env protection patterns extracted
- [ ] TRASH pattern fully documented
- [ ] permissionDecisionReason templates for each block type
- [ ] Secret redaction helper included
- [ ] Integration plan for pre_tool_use.py (additive only)
- [ ] Copy-paste-ready code
- [ ] Database calls clearly identified as MUST PRESERVE

---

## DO NOT

- ❌ Implement anything - research only
- ❌ Invent patterns - only extract from research
- ❌ Skip the YAML files - they have the code snippets!
- ❌ Suggest removing any database calls
- ❌ Suggest replacing existing code - only add to it
