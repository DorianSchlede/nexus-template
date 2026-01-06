# Safety Patterns Research Results

## Executive Summary

The research uncovered **18+ comprehensive safety patterns** from `claude-code-safety-net` and `claude-code-tools` repositories. Key patterns include: intelligent rm -rf blocking with path analysis, git dangerous operation protection (8 specific patterns), .env file access prevention, and the TRASH pattern for safe deletion alternatives. These patterns use `permissionDecisionReason` for context injection and exit code 2 for blocking.

---

## 1. Dangerous Command Patterns

### 1.1 rm -rf / Destructive Delete

**Danger**: Deletes files irrecoverably, can destroy entire systems

**Regex Patterns** (from safety-net.yaml):
```python
RM_PATTERNS = [
    r"\brm\s+.*-[a-z]*r[a-z]*f",      # rm -rf, rm -fr, rm -Rf, etc.
    r"\brm\s+.*-[a-z]*f[a-z]*r",      # rm -fr variations
    r"\brm\s+--recursive\s+--force",  # rm --recursive --force
    r"\brm\s+--force\s+--recursive",  # rm --force --recursive
    r"\brm\s+-r\s+.*-f",              # rm -r ... -f (separated flags)
    r"\brm\s+-f\s+.*-r",              # rm -f ... -r (separated flags)
]

# Additional patterns from safety-net (rules_rm.py):
# Detects --recursive and -r/-R in short flags
# Detects --force and -f in short flags
```

**Intelligent Path Analysis** (from safety-net.yaml):
```python
def _analyze_rm(tokens, *, allow_tmpdir_var=True, cwd=None, paranoid=False):
    """
    Smart rm -rf detection:
    - ALLOW: /tmp, $TMPDIR paths (temp directories)
    - ALLOW: Paths within current working directory (in non-paranoid mode)
    - BLOCK: Root (/), home (~, $HOME), parent refs (..)
    - BLOCK: cwd itself (rm -rf .)
    - BLOCK: Paths outside cwd
    """
    recursive = "--recursive" in opts_lower or "r" in short or "R" in short
    force = "--force" in opts_lower or "f" in short

    if not (recursive and force):
        return None  # Not rm -rf, allow

    targets = _rm_targets(tokens)

    # Block root/home paths
    if any(_is_root_or_home_path(t) for t in targets):
        return _REASON_RM_RF_ROOT_HOME

    # Block deleting cwd itself
    if cwd and any(_is_cwd_itself(t, cwd) for t in targets):
        return _REASON_RM_RF

    # Allow temp paths
    if targets and all(_is_temp_path(t, allow_tmpdir_var=allow_tmpdir_var) for t in targets):
        return None

    # Allow within cwd (non-paranoid mode)
    if cwd and targets and all(_is_path_within_cwd(t, cwd) for t in targets):
        return None

    return _REASON_RM_RF
```

**Dangerous Paths** (block additionally):
```python
DANGEROUS_PATHS = [
    r"/",       # Root
    r"/\*",     # Root wildcard
    r"~",       # Home
    r"~/",      # Home path
    r"\$HOME",  # Home env
    r"\.\.",    # Parent refs (escape attempt)
    r"\.",      # Current dir (rm -rf .)
]
```

**permissionDecisionReason Template**:
```
BLOCKED: Destructive delete command detected

Command: {command}

rm -rf is destructive and cannot be undone.

Instead:
- Use TRASH pattern: mv {file} ./TRASH/
- Create TRASH-FILES.md with deletion log
- Or list files first, then delete individually
- If truly needed, ask user for explicit confirmation

Why this is dangerous:
- Files cannot be recovered after rm -rf
- May delete more than intended with wildcards
- Parent directory references (..) can escape intended scope
```

---

### 1.2 git reset --hard / Force Operations

**Danger**: Loses uncommitted changes permanently, rewrites history

**Regex Patterns** (from safety-net.yaml - 8 SPECIFIC PATTERNS):
```python
GIT_DANGEROUS_PATTERNS = [
    # git reset --hard - destroys uncommitted changes
    r"git\s+reset\s+--hard",

    # git reset --merge - can destroy uncommitted changes
    r"git\s+reset\s+--merge",

    # git push --force - rewrites remote history (but allow --force-with-lease)
    r"git\s+push\s+.*--force(?!-with-lease)",
    r"git\s+push\s+.*-f\b(?!orce-with-lease)",

    # git branch -D - force deletes without merge check
    r"git\s+branch\s+-D\b",  # Case sensitive! -D vs -d

    # git checkout -- . - discards all changes in directory
    r"git\s+checkout\s+--\s+\.",
    r"git\s+checkout\s+\.",

    # git checkout <ref> -- <pathspec> - discards changes to specific files
    r"git\s+checkout\s+.*--",

    # git clean -f - permanently removes untracked files
    r"git\s+clean\s+.*-[a-z]*f",

    # git stash drop/clear - permanently deletes stashed changes
    r"git\s+stash\s+drop",
    r"git\s+stash\s+clear",

    # git restore (without --staged) - discards working tree changes
    r"git\s+restore\s+(?!.*--staged)",
    r"git\s+restore\s+--worktree",
]
```

**Detailed Pattern Analysis from safety-net.yaml**:

| Pattern | Danger | Safe Alternative |
|---------|--------|------------------|
| `git reset --hard` | Destroys uncommitted changes | `git stash` first |
| `git reset --merge` | Can destroy uncommitted changes | `git stash` first |
| `git push --force` | Rewrites remote history | `git push --force-with-lease` |
| `git branch -D` | Force delete without merge check | `git branch -d` (safe delete) |
| `git checkout -- .` | Discards ALL changes | `git stash` or `git diff` first |
| `git checkout <ref> -- <path>` | Discards specific file changes | `git stash` first |
| `git clean -f` | Removes untracked files permanently | `git clean -n` (dry run first) |
| `git stash drop` | Deletes stashed changes | `git stash list` first |
| `git stash clear` | Deletes ALL stashes | `git stash list` first |
| `git restore <path>` | Discards working tree changes | `git restore --staged` (safe) |

**permissionDecisionReason Templates**:

**git reset --hard**:
```
BLOCKED: git reset --hard destroys uncommitted changes

Command: {command}

This will permanently lose uncommitted changes.

Instead:
- git stash (save changes first)
- git branch backup-$(date +%Y%m%d) (create backup branch)
- git diff HEAD (review what will be lost)

Why this is dangerous:
- Uncommitted changes will be lost forever
- Cannot always be recovered with git reflog
```

**git push --force**:
```
BLOCKED: Force push can destroy remote history

Command: {command}

Force push overwrites the remote branch, losing commits others may depend on.

Instead:
- git push --force-with-lease (safer - fails if remote changed)
- git pull --rebase origin main (sync first)

Why this is dangerous:
- Other developers may lose work
- CI/CD pipelines may break
- History becomes inconsistent
```

**git checkout --**:
```
BLOCKED: git checkout -- discards uncommitted changes permanently

Command: {command}

This will discard changes to the specified files with no recovery.

Instead:
- git stash (save changes first)
- git diff {file} (review changes first)

Why this is dangerous:
- Changes are lost immediately
- Cannot be recovered
```

---

### 1.3 .env File Access

**Danger**: Credentials exposure, secret leakage

**Regex Patterns** (from cc-tools-py.yaml):
```python
ENV_PATTERNS = [
    # Direct file reading
    r"\.env\b(?!\.sample)",         # .env but not .env.sample
    r"cat\s+.*\.env\b(?!\.sample)",
    r"less\s+.*\.env\b(?!\.sample)",
    r"head\s+.*\.env\b(?!\.sample)",
    r"tail\s+.*\.env\b(?!\.sample)",

    # Editors
    r"vi\s+.*\.env\b",
    r"vim\s+.*\.env\b",
    r"nano\s+.*\.env\b",
    r"code\s+.*\.env\b",

    # Writing/modifying
    r"echo\s+.*>\s*\.env\b(?!\.sample)",
    r">\s*\.env\b(?!\.sample)",
    r"touch\s+.*\.env\b(?!\.sample)",
    r"cp\s+.*\.env\b(?!\.sample)",
    r"mv\s+.*\.env\b(?!\.sample)",

    # Searching (could expose keys in output)
    r"grep\s+.*\.env\b(?!\.sample)",
    r"rg\s+.*\.env\b(?!\.sample)",

    # Sed in-place editing
    r"sed\s+.*-i.*\.env\b",
]
```

**Tools to Check**: Read, Edit, Write, MultiEdit, Bash

**File Path Check** (for non-Bash tools):
```python
def is_env_file(file_path: str) -> bool:
    """Check if file path is a .env file (not .env.sample)"""
    return ".env" in file_path and not file_path.endswith(".env.sample")
```

**permissionDecisionReason Template**:
```
BLOCKED: Credential file access detected

File: {file_path}

Environment files contain secrets that should not be:
- Read into Claude's context (could be logged/leaked)
- Modified programmatically (could corrupt secrets)
- Copied or moved without explicit permission

Instead:
- Use .env.sample as reference
- Use env-safe CLI: `env-safe list`, `env-safe check KEY_NAME`
- Ask user for specific values needed

Why this is dangerous:
- API keys, passwords, tokens could be exposed
- Secrets could appear in logs or error messages
- Accidental commits could leak credentials
```

---

## 2. TRASH Pattern Implementation

**Concept**: Instead of `rm`, move files to a TRASH folder with audit log

**Implementation** (from cc-tools-py.yaml):
```python
def check_rm_command(command: str) -> tuple[bool, str]:
    """
    Block ALL rm commands and provide TRASH pattern guidance.
    Returns (should_block, reason_text)
    """
    normalized_cmd = ' '.join(command.strip().split())

    # Detect rm command in various forms
    if (normalized_cmd.startswith("rm ") or
        normalized_cmd == "rm" or
        re.search(r'(^|[;&|]\s*)(/\S*/)?rm\b', normalized_cmd)):

        reason_text = (
            "Instead of using 'rm':\n"
            "- MOVE files using `mv` to TRASH directory in CURRENT folder\n"
            "- Create TRASH/ if it doesn't exist\n"
            "- Add entry in TRASH-FILES.md with:\n"
            "  - File name\n"
            "  - Where it was moved\n"
            "  - Reason for deletion\n"
            "  - Date"
        )
        return True, reason_text

    return False, None
```

**TRASH-FILES.md Format**:
```markdown
# Deleted Files Log

| File | Moved To | Reason | Date |
|------|----------|--------|------|
| old_config.py | ./TRASH/old_config.py | Replaced by new config | 2026-01-01 |
| test_file.ts | ./TRASH/test_file.ts | Unused test file | 2026-01-01 |
```

**Full Workflow**:
```bash
# Instead of: rm old_file.py

# Do this:
mkdir -p TRASH
mv old_file.py TRASH/
echo "| old_file.py | ./TRASH/old_file.py | Replaced by new version | $(date +%Y-%m-%d) |" >> TRASH-FILES.md
```

---

## 3. Secret Redaction Helper

**From safety-net.yaml** - Use in all logging/output:
```python
def redact_secrets(text: str) -> str:
    """Redact sensitive values before logging or displaying."""
    redacted = text

    # KEY=VALUE patterns for secret-ish keys
    redacted = re.sub(
        r"\b([A-Z0-9_]*(?:TOKEN|SECRET|PASSWORD|PASS|KEY|CREDENTIALS)[A-Z0-9_]*)=([^\s]+)",
        r"\1=<redacted>",
        redacted,
        flags=re.IGNORECASE
    )

    # Authorization headers
    redacted = re.sub(
        r"(?i)(authorization\s*:\s*)([^\s\"']+)",
        r"\1<redacted>",
        redacted
    )

    # URL credentials: scheme://user:pass@host
    redacted = re.sub(
        r"(?i)(https?://)([^\s/:@]+):([^\s@]+)@",
        r"\1<redacted>:<redacted>@",
        redacted
    )

    # GitHub token prefixes (ghp_, gho_, ghu_, ghs_, ghr_)
    redacted = re.sub(
        r"\bgh[pousr]_[A-Za-z0-9]{20,}\b",
        "<redacted>",
        redacted
    )

    # AWS access keys (AKIA...)
    redacted = re.sub(
        r"\bAKIA[0-9A-Z]{16}\b",
        "<redacted>",
        redacted
    )

    return redacted
```

---

## 4. Integration with Current pre_tool_use.py

### Current State Analysis

The current `pre_tool_use.py` already implements:

**1. .env File Protection** (lines 223-251):
```python
def is_env_file_access(tool_name, tool_input):
    """Check if any tool is trying to access .env files"""
    # Checks Read, Edit, MultiEdit, Write, Bash tools
    # Blocks .env access, allows .env.sample
```
Status: **IMPLEMENTED** - Already has comprehensive .env protection

**2. Dangerous rm Command Detection** (lines 179-220):
```python
def is_dangerous_rm_command(command):
    """Comprehensive detection of dangerous rm commands"""
    # Has basic rm -rf patterns
    # Has dangerous path detection
```
Status: **PARTIALLY IMPLEMENTED** - Has basic patterns, could be enhanced

**3. Database/Server Calls** (MUST PRESERVE):
```python
# Line 176: stream_executable(executable, session_id)
# Uses: send_to_server(f"/api/v2/sessions/{session_id}/executable", payload)

# Lines 287-314: Local logging to session log directory
# Uses: ensure_session_log_dir(session_id), log_path.exists(), json.dump()
```

### Missing Patterns (From Research)

The following patterns from research are NOT in current implementation:

1. **git Dangerous Operations** - MISSING
   - git reset --hard
   - git push --force
   - git checkout --
   - git clean -f
   - git branch -D
   - git stash drop/clear
   - git restore (worktree)

2. **Shell Wrapper Recursive Analysis** - MISSING
   - bash -c "rm -rf /"
   - sh -c "git reset --hard"

3. **TRASH Pattern Guidance** - MISSING
   - Currently just blocks rm, doesn't provide TRASH alternative

4. **JSON Output Format** - DIFFERENT
   - Current: Prints to stderr, exits with code 2
   - Research: Returns JSON with permissionDecisionReason

5. **Intelligent Path Analysis** - PARTIAL
   - Current: Basic path patterns
   - Research: cwd-relative, temp path detection

### Upgrade Plan (ADDITIVE ONLY)

```python
# =============================================================================
# ADD THESE CONSTANTS (after existing imports)
# =============================================================================

GIT_DANGEROUS_PATTERNS = [
    r"git\s+reset\s+--hard",
    r"git\s+reset\s+--merge",
    r"git\s+push\s+.*--force(?!-with-lease)",
    r"git\s+push\s+.*-f\b(?!orce-with-lease)",
    r"git\s+branch\s+-D\b",
    r"git\s+checkout\s+--\s+\.",
    r"git\s+checkout\s+\.",
    r"git\s+clean\s+.*-[a-z]*f",
    r"git\s+stash\s+drop",
    r"git\s+stash\s+clear",
    r"git\s+restore\s+--worktree",
]

TRASH_GUIDANCE = """
Instead of using 'rm':
- MOVE files using `mv` to TRASH directory in CURRENT folder
- Create TRASH/ if it doesn't exist
- Add entry in TRASH-FILES.md with file name, destination, reason, date

Example:
mkdir -p TRASH && mv {file} TRASH/ && echo "| {file} | ./TRASH/{file} | reason | $(date +%Y-%m-%d) |" >> TRASH-FILES.md
"""

GIT_GUIDANCE = """
This git command can cause permanent data loss.

Safe alternatives:
- git stash (save changes first)
- git branch backup-$(date +%Y%m%d) (create backup)
- git push --force-with-lease (safer force push)
- git clean -n (dry run first)
- git branch -d (safe delete with merge check)

If truly needed, ask user for explicit confirmation.
"""

# =============================================================================
# ADD THESE FUNCTIONS (after existing functions)
# =============================================================================

def is_dangerous_git_command(command: str) -> bool:
    """Check for dangerous git operations that can lose data."""
    for pattern in GIT_DANGEROUS_PATTERNS:
        if re.search(pattern, command, re.IGNORECASE):
            return True
    return False


def output_block_json(reason: str, guidance: str):
    """Output JSON block response (alternative to stderr + exit 2)."""
    output = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": f"{reason}\n\n{guidance}"
        }
    }
    print(json.dumps(output))


# =============================================================================
# INTEGRATION IN main() - ADD to existing checks, don't replace
# =============================================================================

# In main(), after the existing is_env_file_access check:

if tool_name == "Bash":
    command = tool_input.get("command", "")

    # EXISTING: Block rm -rf commands
    if is_dangerous_rm_command(command):
        print(
            "BLOCKED: Dangerous rm command detected and prevented",
            file=sys.stderr,
        )
        print(TRASH_GUIDANCE, file=sys.stderr)  # ADD: TRASH guidance
        sys.exit(2)

    # NEW: Block dangerous git operations
    if is_dangerous_git_command(command):
        print(
            "BLOCKED: Dangerous git operation detected",
            file=sys.stderr,
        )
        print(GIT_GUIDANCE, file=sys.stderr)
        sys.exit(2)

# PRESERVE: All existing database calls and logging
# ... existing code continues unchanged ...
```

---

## 5. Complete Regex Reference (Copy-Paste Ready)

### All rm Patterns
```python
RM_PATTERNS = [
    # Standard rm -rf variations
    r"\brm\s+.*-[a-z]*r[a-z]*f",      # rm -rf, rm -fr, rm -Rf
    r"\brm\s+.*-[a-z]*f[a-z]*r",      # rm -fr variations
    r"\brm\s+--recursive\s+--force",  # Long form
    r"\brm\s+--force\s+--recursive",  # Long form alt
    r"\brm\s+-r\s+.*-f",              # Separated flags
    r"\brm\s+-f\s+.*-r",              # Separated flags alt
]

DANGEROUS_PATHS = [
    r"^/$",              # Root exactly
    r"^/\*$",            # Root wildcard
    r"^~/?",             # Home directory
    r"^\$HOME",          # Home env var
    r"\.\./",            # Parent traversal
    r"^\.$",             # Current dir exactly
]

# Simple rm detection (for TRASH pattern)
RM_ANY_PATTERN = r'(^|[;&|]\s*)(/\S*/)?rm\b'
```

### All git Patterns
```python
GIT_DANGEROUS_PATTERNS = [
    # Reset operations
    r"git\s+reset\s+--hard",
    r"git\s+reset\s+--merge",

    # Force push (but allow --force-with-lease)
    r"git\s+push\s+.*--force(?!-with-lease)",
    r"git\s+push\s+.*-f\b(?!orce-with-lease)",

    # Branch force delete
    r"git\s+branch\s+-D\b",

    # Checkout discard operations
    r"git\s+checkout\s+--\s+\.",
    r"git\s+checkout\s+\.",
    r"git\s+checkout\s+(-f|--force)\b",

    # Clean operations
    r"git\s+clean\s+.*-[a-z]*f",

    # Stash destruction
    r"git\s+stash\s+drop",
    r"git\s+stash\s+clear",

    # Restore operations (without --staged)
    r"git\s+restore\s+--worktree",
    r"git\s+restore\s+(?!.*--staged)(?!.*-h)(?!.*--help)",
]
```

### All .env Patterns
```python
ENV_PATTERNS = [
    # File path patterns (for Read/Edit/Write tools)
    r"\.env$",                        # Ends with .env
    r"\.env[^a-z]",                   # .env followed by non-letter

    # Bash command patterns
    r"cat\s+.*\.env\b(?!\.sample)",
    r"less\s+.*\.env\b(?!\.sample)",
    r"head\s+.*\.env\b(?!\.sample)",
    r"tail\s+.*\.env\b(?!\.sample)",
    r"vi\s+.*\.env\b",
    r"vim\s+.*\.env\b",
    r"nano\s+.*\.env\b",
    r"code\s+.*\.env\b",
    r"echo\s+.*>\s*\.env\b(?!\.sample)",
    r">\s*\.env\b(?!\.sample)",
    r"touch\s+.*\.env\b(?!\.sample)",
    r"cp\s+.*\.env\b(?!\.sample)",
    r"mv\s+.*\.env\b(?!\.sample)",
    r"grep\s+.*\.env\b(?!\.sample)",
    r"rg\s+.*\.env\b(?!\.sample)",
    r"sed\s+.*-i.*\.env\b",
]
```

---

## 6. Database Impact Analysis

### Existing Database Calls (MUST PRESERVE)

| Location | Function | Purpose |
|----------|----------|---------|
| Line 176 | `stream_executable(executable, session_id)` | Streams executable detection to observability server |
| Line 176 | `send_to_server(f"/api/v2/sessions/{session_id}/executable", payload)` | HTTP POST to server |
| Lines 287-314 | `ensure_session_log_dir(session_id)` | Creates session log directory |
| Lines 300-314 | `json.dump(log_data, f, indent=2)` | Writes to pre_tool_use.json |

### New Code (NO Database Impact)

All proposed safety check additions are:
- **Pure Python functions** - no external calls
- **Regex-based pattern matching** - no I/O
- **Exit code 2 or JSON output** - standard hook response

```python
# These functions have ZERO database impact:
is_dangerous_git_command(command)  # Pure regex
output_block_json(reason, guidance)  # stdout JSON only
```

### Critical: Do Not Modify

```python
# NEVER change these lines:
send_to_server(...)        # Observability streaming
ensure_session_log_dir(...)  # Session logging
log_data.append(input_data)  # Local audit
json.dump(log_data, ...)     # Local persistence
```

---

## 7. Advanced Patterns (From safety-net.yaml)

### Shell Wrapper Recursive Analysis
```python
_MAX_RECURSION_DEPTH = 5

def analyze_command(command, depth=0, cwd=None):
    """Recursively analyze commands wrapped in shell invocations."""
    if depth >= _MAX_RECURSION_DEPTH:
        return "Command analysis recursion limit reached."

    tokens = shlex.split(command)
    head = tokens[0].lower()

    # Detect shell wrappers
    if head in {"bash", "sh", "zsh", "dash", "ksh"}:
        cmd_str = extract_dash_c_arg(tokens)
        if cmd_str:
            return analyze_command(cmd_str, depth=depth+1, cwd=cwd)

    # Check for dangerous commands
    if head == "rm":
        return check_rm_danger(tokens)
    if head == "git":
        return check_git_danger(tokens)

    return None
```

### Strict Mode (Fail-Closed)
```python
def strict_mode() -> bool:
    """Enable via SAFETY_NET_STRICT=1 environment variable."""
    return os.getenv("SAFETY_NET_STRICT", "").lower() in ("1", "true", "yes")

# In main():
try:
    input_data = json.load(sys.stdin)
except json.JSONDecodeError:
    if strict_mode():
        output_block_json("Invalid hook input", "Strict mode: cannot parse")
        sys.exit(2)
    sys.exit(0)  # Allow through in default mode
```

### Paranoid Mode (Maximum Protection)
```python
def paranoid_mode() -> bool:
    """Enable via SAFETY_NET_PARANOID=1 - blocks rm -rf even in cwd."""
    return os.getenv("SAFETY_NET_PARANOID", "").lower() in ("1", "true", "yes")
```

---

## 8. Success Criteria Checklist

- [x] All rm -rf regex patterns extracted
- [x] All git dangerous patterns extracted (8 specific patterns)
- [x] All .env protection patterns extracted
- [x] TRASH pattern fully documented
- [x] permissionDecisionReason templates for each block type
- [x] Secret redaction helper included
- [x] Integration plan for pre_tool_use.py (additive only)
- [x] Copy-paste-ready code
- [x] Database calls clearly identified as MUST PRESERVE
- [x] Shell wrapper recursive analysis documented
- [x] Strict/paranoid modes documented
