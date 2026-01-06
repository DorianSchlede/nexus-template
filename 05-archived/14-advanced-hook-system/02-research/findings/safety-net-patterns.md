# claude-code-safety-net Findings

**Repository**: claude-code-safety-net
**Analysis Date**: 2025-12-31
**Purpose**: Extract patterns for Nexus Advanced Hook System

---

## Overview

The `claude-code-safety-net` is a Claude Code plugin that blocks destructive git and filesystem commands before execution. It works as a PreToolUse hook that intercepts Bash commands and denies dangerous operations.

### Architecture Summary

```
Entry Point: scripts/safety_net.py
    -> scripts/safety_net_impl/hook.py (main logic)
        -> shell.py (parsing utilities)
        -> rules_rm.py (rm -rf detection)
        -> rules_git.py (git safety rules)
```

---

## Key Patterns

### Pattern 1: Exit Code Behavior
- **Exit 0 with JSON containing `permissionDecision: "deny"`** = block command
- **Exit 0 with no output** = allow command
- Always exits 0 - the hook response determines behavior, not exit code

### Pattern 2: JSON Input/Output Protocol
```python
# Input structure (from stdin)
{
    "tool_name": "Bash",
    "tool_input": {"command": "..."},
    "cwd": "/optional/path",
    "session_id": "optional-session-id"
}

# Output structure (to stdout)
{
    "hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": "BLOCKED by Safety Net\n\nReason: ..."
    }
}
```

### Pattern 3: Environment Variable Modes
- `SAFETY_NET_STRICT=1`: Fail-closed on unparseable input/commands
- `SAFETY_NET_PARANOID=1`: Enable all paranoid checks
- `SAFETY_NET_PARANOID_RM=1`: Block non-temp rm -rf even within cwd
- `SAFETY_NET_PARANOID_INTERPRETERS=1`: Block interpreter one-liners

### Pattern 4: Layered Analysis
1. Split command on shell operators (`;`, `&&`, `|`, `||`, `&`, newline)
2. Tokenize each segment with shlex
3. Strip wrappers (sudo, env, command)
4. Identify command head and dispatch to specific analyzer

### Pattern 5: Recursion Depth Limiting
- Max recursion depth of 5 for nested shell wrappers
- Prevents infinite loops in `bash -c 'bash -c "..."'` patterns

---

## rm -rf Detection Patterns

### Core Detection Logic

```python
def _analyze_rm(
    tokens: list[str],
    *,
    allow_tmpdir_var: bool = True,
    cwd: str | None = None,
    paranoid: bool = False,
) -> str | None:
    # 1. Extract options and check for recursive + force
    opts_lower = [t.lower() for t in opts]
    short = _short_opts(opts)  # Extracts single-char options
    recursive = "--recursive" in opts_lower or "r" in short or "R" in short
    force = "--force" in opts_lower or "f" in short

    if not (recursive and force):
        return None  # Not rm -rf, allow

    # 2. Check targets for safety
    targets = _rm_targets(tokens)

    # 3. Block root/home paths unconditionally
    if any(_is_root_or_home_path(t) for t in targets):
        return _REASON_RM_RF_ROOT_HOME

    # 4. Block deleting cwd itself
    if cwd and any(_is_cwd_itself(t, cwd) for t in targets):
        return _REASON_RM_RF

    # 5. Allow temp paths
    if targets and all(_is_temp_path(t, allow_tmpdir_var=allow_tmpdir_var) for t in targets):
        return None

    # 6. Paranoid mode blocks all
    if paranoid:
        return _REASON_RM_RF + _PARANOID_SUFFIX

    # 7. Allow within cwd (except home)
    if cwd and targets:
        home = os.environ.get("HOME")
        if home and posixpath.normpath(cwd) == posixpath.normpath(home):
            return _REASON_RM_RF_ROOT_HOME
        if all(_is_path_within_cwd(t, cwd) for t in targets):
            return None

    return _REASON_RM_RF
```

### Temp Path Detection

```python
def _is_temp_path(path: str, *, allow_tmpdir_var: bool) -> bool:
    # Absolute paths
    if path.startswith("/"):
        normalized = posixpath.normpath(path)
        return (
            normalized == "/tmp"
            or normalized.startswith("/tmp/")
            or normalized == "/var/tmp"
            or normalized.startswith("/var/tmp/")
        )

    # TMPDIR variable
    if not allow_tmpdir_var:
        return False

    for prefix in ("$TMPDIR", "${TMPDIR}"):
        if path == prefix:
            return True
        if path.startswith(prefix + "/"):
            rest = path[len(prefix) + 1:]
            if ".." in rest.split("/"):
                return False  # Traversal attempt
            return True

    return False
```

### CWD Protection Logic

```python
def _is_path_within_cwd(path: str, cwd: str) -> bool:
    """Return True if path resolves to something inside cwd."""

    # Reject home-relative paths
    if path.startswith(("~", "$HOME", "${HOME}")):
        return False

    # Reject paths with variables or command substitution
    if "$" in path or "`" in path:
        return False

    normalized = posixpath.normpath(path)
    if normalized in {".", ""}:
        return False  # Don't allow deleting cwd itself

    # Resolve path
    if path.startswith("/"):
        resolved = posixpath.normpath(path)
    else:
        resolved = posixpath.normpath(posixpath.join(cwd, path))

    cwd_normalized = posixpath.normpath(cwd)

    if resolved == cwd_normalized:
        return False  # Don't allow deleting cwd itself

    return resolved.startswith(cwd_normalized + "/")


def _is_cwd_itself(path: str, cwd: str) -> bool:
    """Return True if path resolves to the cwd itself."""
    normalized = posixpath.normpath(path)
    if normalized in {".", ""}:
        return True

    if path.startswith("/"):
        resolved = posixpath.normpath(path)
    else:
        resolved = posixpath.normpath(posixpath.join(cwd, path))

    return resolved == posixpath.normpath(cwd)
```

### Root/Home Path Detection

```python
def _is_root_or_home_path(path: str) -> bool:
    return (
        path == "/"
        or (path.startswith("/") and posixpath.normpath(path) == "/")
        or path == "~"
        or path.startswith("~/")
        or path == "$HOME"
        or path.startswith("$HOME/")
        or path.startswith("${HOME}")
    )
```

### Target Extraction

```python
def _rm_targets(tokens: list[str]) -> list[str]:
    """Extract targets from rm command, handling -- separator."""
    targets: list[str] = []
    after_double_dash = False
    for tok in tokens[1:]:
        if after_double_dash:
            targets.append(tok)
            continue
        if tok == "--":
            after_double_dash = True
            continue
        if tok.startswith("-") and tok != "-":
            continue  # Skip options
        targets.append(tok)
    return targets
```

---

## Git Safety Rules

### All 12+ Git Rules

| Subcommand | Trigger | Block Reason |
|------------|---------|--------------|
| `checkout --` | `--` at index 0 | Discards uncommitted changes permanently |
| `checkout <ref> -- <path>` | `--` with ref before it | Overwrites working tree |
| `checkout <ref> <pathspec>` | 2+ positional args | Overwrites working tree |
| `checkout --pathspec-from-file` | Option present | Overwrites working tree |
| `restore` | No `--staged` | Discards uncommitted changes |
| `restore --worktree` | `--worktree` flag | Discards uncommitted changes permanently |
| `reset --hard` | `--hard` flag | Destroys uncommitted changes |
| `reset --merge` | `--merge` flag | Can lose uncommitted changes |
| `clean -f` | `-f` or `--force` | Removes untracked files permanently |
| `push --force` | `-f` or `--force` without `--force-with-lease` | Can destroy remote history |
| `worktree remove --force` | `--force` or `-f` | Can delete worktree files |
| `branch -D` | `-D` (uppercase) | Force-deletes without merge check |
| `stash drop` | `drop` subcommand | Permanently deletes stashed changes |
| `stash clear` | `clear` subcommand | Permanently deletes ALL stashed changes |

### Git Analysis Implementation

```python
def _analyze_git(tokens: list[str]) -> str | None:
    sub, rest = _git_subcommand_and_rest(tokens)
    if not sub:
        return None

    sub = sub.lower()
    rest_lower = [t.lower() for t in rest]
    short = _short_opts(rest)

    if sub == "checkout":
        if "--" in rest:
            idx = rest.index("--")
            return (
                _REASON_GIT_CHECKOUT_DOUBLE_DASH if idx == 0
                else _REASON_GIT_CHECKOUT_REF_DOUBLE_DASH
            )
        # Allow branch creation
        if "-b" in rest or "b" in short or "-B" in rest or "B" in short:
            return None
        if "--orphan" in rest_lower:
            return None

        # Check pathspec-from-file
        has_pathspec_from_file = any(
            t == "--pathspec-from-file" or t.startswith("--pathspec-from-file=")
            for t in rest_lower
        )
        if has_pathspec_from_file:
            return _REASON_GIT_CHECKOUT_PATHSPEC_FROM_FILE

        # Check for <ref> <pathspec> pattern
        positional = _checkout_positional_args(rest)
        if len(positional) >= 2:
            return _REASON_GIT_CHECKOUT_REF_PATHSPEC
        return None

    if sub == "restore":
        if "-h" in rest_lower or "--help" in rest_lower or "--version" in rest_lower:
            return None
        if "--worktree" in rest_lower:
            return _REASON_GIT_RESTORE_WORKTREE
        if "--staged" in rest_lower:
            return None  # Safe - only unstages
        return _REASON_GIT_RESTORE

    if sub == "reset":
        if "--hard" in rest_lower:
            return _REASON_GIT_RESET_HARD
        if "--merge" in rest_lower:
            return _REASON_GIT_RESET_MERGE
        return None

    if sub == "clean":
        has_force = "--force" in rest_lower or "f" in short
        if has_force:
            return _REASON_GIT_CLEAN_FORCE
        return None

    if sub == "push":
        has_force_with_lease = any(
            t.startswith("--force-with-lease") for t in rest_lower
        )
        has_force = "--force" in rest_lower or "f" in short
        # Block if force without force-with-lease
        if has_force and not has_force_with_lease:
            return _REASON_GIT_PUSH_FORCE
        # Block if both are present (explicit --force overrides)
        if "--force" in rest_lower and has_force_with_lease:
            return _REASON_GIT_PUSH_FORCE
        if "f" in short and has_force_with_lease:
            return _REASON_GIT_PUSH_FORCE
        return None

    if sub == "worktree":
        if not rest_lower or rest_lower[0] != "remove":
            return None
        rest_for_opts = rest
        if "--" in rest_for_opts:
            rest_for_opts = rest_for_opts[:rest_for_opts.index("--")]
        rest_for_opts_lower = [t.lower() for t in rest_for_opts]
        short_for_opts = _short_opts(rest_for_opts)
        has_force = "--force" in rest_for_opts_lower or "f" in short_for_opts
        if has_force:
            return _REASON_GIT_WORKTREE_REMOVE_FORCE
        return None

    if sub == "branch":
        # Note: -D (uppercase) is force delete, -d (lowercase) is safe
        if "-D" in rest or "D" in short:
            return _REASON_GIT_BRANCH_DELETE_FORCE
        return None

    if sub == "stash":
        if not rest_lower:
            return None
        if rest_lower[0] == "drop":
            return _REASON_GIT_STASH_DROP
        if rest_lower[0] == "clear":
            return _REASON_GIT_STASH_CLEAR
        return None

    return None
```

### Git Global Options Handling

```python
def _git_subcommand_and_rest(tokens: list[str]) -> tuple[str | None, list[str]]:
    """Extract the git subcommand, skipping global options."""
    if not tokens or tokens[0].lower() != "git":
        return None, []

    opts_with_value = {
        "-c", "-C", "--exec-path", "--git-dir", "--namespace",
        "--super-prefix", "--work-tree",
    }
    opts_no_value = {
        "-p", "-P", "-h", "--help", "--no-pager", "--paginate",
        "--version", "--bare", "--no-replace-objects",
        "--literal-pathspecs", "--noglob-pathspecs", "--icase-pathspecs",
    }

    i = 1
    while i < len(tokens):
        tok = tokens[i]
        if tok == "--":
            i += 1
            break
        if not tok.startswith("-") or tok == "-":
            break

        if tok in opts_no_value:
            i += 1
            continue
        if tok in opts_with_value:
            i += 2
            continue

        # Handle --option=value
        if tok.startswith("--") and "=" in tok:
            opt, _value = tok.split("=", 1)
            if opt in opts_with_value:
                i += 1
                continue

        # Handle -Crepo, -cname=value (attached values)
        if tok.startswith("-C") and len(tok) > 2:
            i += 1
            continue
        if tok.startswith("-c") and len(tok) > 2:
            i += 1
            continue

        i += 1

    if i >= len(tokens):
        return None, []

    return tokens[i], tokens[i + 1:]
```

---

## Shell Parsing Utilities

### Command Splitting

```python
def _split_shell_commands(command: str) -> list[str]:
    """Split on shell operators: ;, &&, ||, |, &, newline"""
    parts: list[str] = []
    buf: list[str] = []
    in_single = False
    in_double = False
    escape = False

    i = 0
    while i < len(command):
        ch = command[i]

        if escape:
            buf.append(ch)
            escape = False
            i += 1
            continue

        if ch == "\\" and not in_single:
            buf.append(ch)
            escape = True
            i += 1
            continue

        if ch == "'" and not in_double:
            in_single = not in_single
            buf.append(ch)
            i += 1
            continue

        if ch == '"' and not in_single:
            in_double = not in_double
            buf.append(ch)
            i += 1
            continue

        if not in_single and not in_double:
            # Handle &&, ||
            if command.startswith("&&", i) or command.startswith("||", i):
                part = "".join(buf).strip()
                if part:
                    parts.append(part)
                buf = []
                i += 2
                continue
            # Handle |&
            if command.startswith("|&", i):
                part = "".join(buf).strip()
                if part:
                    parts.append(part)
                buf = []
                i += 2
                continue
            # Handle single |
            if ch == "|":
                part = "".join(buf).strip()
                if part:
                    parts.append(part)
                buf = []
                i += 1
                continue
            # Handle & (but not in redirections)
            if ch == "&":
                prev = command[i - 1] if i > 0 else ""
                nxt = command[i + 1] if i + 1 < len(command) else ""
                if prev in {">", "<"} or nxt == ">":
                    buf.append(ch)
                    i += 1
                    continue
                part = "".join(buf).strip()
                if part:
                    parts.append(part)
                buf = []
                i += 1
                continue
            # Handle ; and newline
            if ch in {";", "\n"}:
                part = "".join(buf).strip()
                if part:
                    parts.append(part)
                buf = []
                i += 1
                continue

        buf.append(ch)
        i += 1

    part = "".join(buf).strip()
    if part:
        parts.append(part)
    return parts
```

### Short Options Extraction

```python
def _short_opts(tokens: list[str]) -> set[str]:
    """Extract single-character options from tokens."""
    opts: set[str] = set()
    for tok in tokens:
        if tok.startswith("--") or not tok.startswith("-") or tok == "-":
            continue
        opts.update(tok[1:])  # Add each character
    return opts
```

### Wrapper Stripping

```python
def _strip_wrappers(tokens: list[str]) -> list[str]:
    """Strip sudo, env, command prefixes iteratively."""
    previous: list[str] | None = None
    depth = 0
    while tokens and tokens != previous and depth < 20:
        previous = tokens
        depth += 1

        tokens = _strip_env_assignments(tokens)
        if not tokens:
            return tokens

        head = tokens[0].lower()

        if head == "sudo":
            i = 1
            while i < len(tokens) and tokens[i].startswith("-") and tokens[i] != "--":
                i += 1
            if i < len(tokens) and tokens[i] == "--":
                i += 1
            tokens = tokens[i:]
            continue

        if head == "env":
            # Skip env options and assignments
            i = 1
            while i < len(tokens):
                tok = tokens[i]
                if tok == "--":
                    i += 1
                    break
                if tok in {"-u", "--unset", "-C", "-P", "-S"}:
                    i += 2
                    continue
                if tok.startswith("--unset=") or tok.startswith("-u") and len(tok) > 2:
                    i += 1
                    continue
                if tok.startswith("-") and tok != "-":
                    i += 1
                    continue
                break
            tokens = tokens[i:]
            continue

        if head == "command":
            i = 1
            while i < len(tokens):
                tok = tokens[i]
                if tok == "--":
                    i += 1
                    break
                if tok in {"-p", "-v", "-V"}:
                    i += 1
                    continue
                if tok.startswith("-") and tok != "-" and not tok.startswith("--"):
                    chars = tok[1:]
                    if chars and all(ch in {"p", "v", "V"} for ch in chars):
                        i += 1
                        continue
                break
            tokens = tokens[i:]
            continue

        break

    return _strip_env_assignments(tokens)


def _strip_env_assignments(tokens: list[str]) -> list[str]:
    """Strip VAR=value prefixes from command."""
    i = 0
    while i < len(tokens):
        tok = tokens[i]
        if "=" not in tok:
            break
        key, _value = tok.split("=", 1)
        if not key or not (key[0].isalpha() or key[0] == "_"):
            break
        if not all(ch.isalnum() or ch == "_" for ch in key[1:]):
            break
        i += 1
    return tokens[i:]
```

---

## Advanced Detection Patterns

### Interpreter One-Liner Detection

```python
# Detect destructive commands hidden in interpreter calls
if head in {"python", "python3", "node", "ruby", "perl"}:
    code = _extract_pythonish_code_arg(tokens)
    if code is not None:
        reason = _dangerous_in_text(code) or _dangerous_find_delete_in_text(code)
        if reason:
            return segment, reason
        if paranoid_interpreters:
            return (
                segment,
                "Cannot safely analyze interpreter one-liners." + _PARANOID_SUFFIX,
            )
```

### xargs Detection

```python
def _extract_xargs_child_command(tokens: list[str]) -> list[str] | None:
    """Extract the command xargs will execute."""
    # ... option parsing logic ...

# In analysis:
if head == "xargs":
    child = _extract_xargs_child_command(tokens)
    if child and _normalize_cmd_token(child[0]) == "rm":
        if _rm_has_recursive_force(["rm", *child[1:]]):
            return segment, _REASON_XARGS_RM_RF
```

### find -delete Detection

```python
def _find_has_delete(args: list[str]) -> bool:
    """Detect -delete in find, avoiding false positives."""
    # Predicates that consume one argument
    consumes_one = {
        "-name", "-iname", "-path", "-ipath", "-wholename",
        "-iwholename", "-regex", "-iregex", "-lname", "-ilname",
        "-samefile", "-newer", "-newerxy", "-perm", "-user",
        "-group", "-printf", "-fprintf", "-fprint", "-fprint0", "-fls",
    }

    exec_like = {"-exec", "-execdir", "-ok", "-okdir"}

    i = 0
    while i < len(args):
        tok = _strip_token_wrappers(args[i]).lower()

        # Skip over -exec blocks
        if tok in exec_like:
            i += 1
            while i < len(args):
                end = _strip_token_wrappers(args[i])
                if end in {";", "+"}:
                    i += 1
                    break
                i += 1
            continue

        # Skip predicates with arguments
        if tok in consumes_one:
            i += 2
            continue

        if tok == "-delete":
            return True

        i += 1

    return False
```

### Fallback Text-Based Detection

```python
def _dangerous_in_text(text: str) -> str | None:
    """Last-resort heuristic detection when parsing fails."""
    t = text.lower()

    # rm -rf regex pattern
    if re.search(
        r"(?<![\w/\\])(?:/[^\s'\";|&]+/)?rm\b[^\n;|&]*(?:\s-(?:[a-z]*r[a-z]*f|[a-z]*f[a-z]*r)\b|\s-r\b[^\n;|&]*\s-f\b|\s-f\b[^\n;|&]*\s-r\b|\s--recursive\b[^\n;|&]*\s--force\b|\s--force\b[^\n;|&]*\s--recursive\b)",
        t,
    ):
        return "rm -rf is destructive..."

    if "git reset --hard" in t:
        return "git reset --hard destroys uncommitted changes..."
    # ... more patterns ...
```

---

## Secret Redaction

```python
def _redact_secrets(text: str) -> str:
    """Heuristic redaction for logs."""
    redacted = text

    # KEY=VALUE patterns
    redacted = re.sub(
        r"\b([A-Z0-9_]*(?:TOKEN|SECRET|PASSWORD|PASS|KEY|CREDENTIALS)[A-Z0-9_]*)=([^\s]+)",
        r"\1=<redacted>",
        redacted,
        flags=re.IGNORECASE,
    )

    # Authorization headers
    redacted = re.sub(
        r"(?i)([\"']\s*authorization\s*:\s*)([^\"']+)([\"'])",
        r"\1<redacted>\3",
        redacted,
    )

    # URL credentials
    redacted = re.sub(
        r"(?i)(https?://)([^\s/:@]+):([^\s@]+)@",
        r"\1<redacted>:<redacted>@",
        redacted,
    )

    # GitHub tokens
    redacted = re.sub(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b", "<redacted>", redacted)

    return redacted
```

---

## Code to Copy

### Complete Shell Parsing Module

```python
"""Shell parsing helpers for the safety net."""

import shlex


def _split_shell_commands(command: str) -> list[str]:
    """Split command on shell operators: ;, &&, ||, |, &, newline."""
    parts: list[str] = []
    buf: list[str] = []
    in_single = False
    in_double = False
    escape = False

    i = 0
    while i < len(command):
        ch = command[i]

        if escape:
            buf.append(ch)
            escape = False
            i += 1
            continue

        if ch == "\\" and not in_single:
            buf.append(ch)
            escape = True
            i += 1
            continue

        if ch == "'" and not in_double:
            in_single = not in_single
            buf.append(ch)
            i += 1
            continue

        if ch == '"' and not in_single:
            in_double = not in_double
            buf.append(ch)
            i += 1
            continue

        if not in_single and not in_double:
            if command.startswith("&&", i) or command.startswith("||", i):
                part = "".join(buf).strip()
                if part:
                    parts.append(part)
                buf = []
                i += 2
                continue
            if command.startswith("|&", i):
                part = "".join(buf).strip()
                if part:
                    parts.append(part)
                buf = []
                i += 2
                continue
            if ch == "|":
                part = "".join(buf).strip()
                if part:
                    parts.append(part)
                buf = []
                i += 1
                continue
            if ch == "&":
                prev = command[i - 1] if i > 0 else ""
                nxt = command[i + 1] if i + 1 < len(command) else ""
                if prev in {">", "<"} or nxt == ">":
                    buf.append(ch)
                    i += 1
                    continue
                part = "".join(buf).strip()
                if part:
                    parts.append(part)
                buf = []
                i += 1
                continue
            if ch in {";", "\n"}:
                part = "".join(buf).strip()
                if part:
                    parts.append(part)
                buf = []
                i += 1
                continue

        buf.append(ch)
        i += 1

    part = "".join(buf).strip()
    if part:
        parts.append(part)
    return parts


def _shlex_split(segment: str) -> list[str] | None:
    """Safe shlex.split with error handling."""
    try:
        return shlex.split(segment, posix=True)
    except ValueError:
        return None


def _short_opts(tokens: list[str]) -> set[str]:
    """Extract single-character options from tokens."""
    opts: set[str] = set()
    for tok in tokens:
        if tok.startswith("--") or not tok.startswith("-") or tok == "-":
            continue
        opts.update(tok[1:])
    return opts


def _strip_env_assignments(tokens: list[str]) -> list[str]:
    """Strip VAR=value prefixes."""
    i = 0
    while i < len(tokens):
        tok = tokens[i]
        if "=" not in tok:
            break
        key, _value = tok.split("=", 1)
        if not key or not (key[0].isalpha() or key[0] == "_"):
            break
        if not all(ch.isalnum() or ch == "_" for ch in key[1:]):
            break
        i += 1
    return tokens[i:]


def _strip_wrappers(tokens: list[str]) -> list[str]:
    """Strip sudo, env, command prefixes."""
    previous: list[str] | None = None
    depth = 0
    while tokens and tokens != previous and depth < 20:
        previous = tokens
        depth += 1

        tokens = _strip_env_assignments(tokens)
        if not tokens:
            return tokens

        head = tokens[0].lower()
        if head == "sudo":
            i = 1
            while i < len(tokens) and tokens[i].startswith("-") and tokens[i] != "--":
                i += 1
            if i < len(tokens) and tokens[i] == "--":
                i += 1
            tokens = tokens[i:]
            continue

        if head == "env":
            i = 1
            while i < len(tokens):
                tok = tokens[i]
                if tok == "--":
                    i += 1
                    break
                if tok in {"-u", "--unset", "-C", "-P", "-S"}:
                    i += 2
                    continue
                if tok.startswith("--unset="):
                    i += 1
                    continue
                if tok.startswith("-u") and len(tok) > 2:
                    i += 1
                    continue
                if tok.startswith("-C") and len(tok) > 2:
                    i += 1
                    continue
                if tok.startswith("-P") and len(tok) > 2:
                    i += 1
                    continue
                if tok.startswith("-S") and len(tok) > 2:
                    i += 1
                    continue
                if tok.startswith("-") and tok != "-":
                    i += 1
                    continue
                break
            tokens = tokens[i:]
            continue

        if head == "command":
            i = 1
            while i < len(tokens):
                tok = tokens[i]
                if tok == "--":
                    i += 1
                    break
                if tok in {"-p", "-v", "-V"}:
                    i += 1
                    continue
                if tok.startswith("-") and tok != "-" and not tok.startswith("--"):
                    chars = tok[1:]
                    if chars and all(ch in {"p", "v", "V"} for ch in chars):
                        i += 1
                        continue
                break
            tokens = tokens[i:]
            continue

        break

    return _strip_env_assignments(tokens)
```

### Test Base Class

```python
"""Shared helpers for safety-net tests."""

import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock


class TempDirTestCase(unittest.TestCase):
    """Base test class with temporary directory."""

    tmpdir: Path
    _tmpdir_obj: tempfile.TemporaryDirectory

    def setUp(self) -> None:
        super().setUp()
        self._tmpdir_obj = tempfile.TemporaryDirectory()
        self.tmpdir = Path(self._tmpdir_obj.name)

    def tearDown(self) -> None:
        self._tmpdir_obj.cleanup()
        super().tearDown()


class SafetyNetTestCase(TempDirTestCase):
    """Base test case with helpers for running the safety-net guard."""

    def _run_guard(self, command: str, *, cwd: str | None = None) -> dict | None:
        """Run the guard with a Bash command and return parsed output or None."""
        from your_module import safety_net  # Adjust import

        input_data: dict = {"tool_name": "Bash", "tool_input": {"command": command}}
        if cwd is not None:
            input_data["cwd"] = cwd
        with mock.patch("sys.stdin", io.StringIO(json.dumps(input_data))):
            with mock.patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
                result = safety_net.main()
                output = mock_stdout.getvalue()

        self.assertEqual(result, 0)
        if output.strip():
            parsed: dict = json.loads(output)
            return parsed
        return None

    def _assert_blocked(
        self, command: str, reason_contains: str, *, cwd: str | None = None
    ) -> None:
        """Assert that a command is blocked with a reason containing the given text."""
        output = self._run_guard(command, cwd=cwd)
        self.assertIsNotNone(output, f"Expected {command!r} to be blocked")
        assert output is not None
        hook_output = output.get("hookSpecificOutput", {})
        self.assertEqual(hook_output.get("permissionDecision"), "deny")
        reason = hook_output.get("permissionDecisionReason", "")
        self.assertIn(reason_contains, reason)

    def _assert_allowed(self, command: str, *, cwd: str | None = None) -> None:
        """Assert that a command is allowed (no output)."""
        output = self._run_guard(command, cwd=cwd)
        self.assertIsNone(output, f"Expected {command!r} to be allowed, got {output}")
```

---

## Test Cases to Copy

### rm -rf Tests

```python
class RmRfBlockedTests(SafetyNetTestCase):
    def test_rm_rf_blocked(self) -> None:
        self._assert_blocked("rm -rf /some/path", "rm -rf")

    def test_rm_Rf_blocked(self) -> None:
        self._assert_blocked("rm -Rf /some/path", "rm -rf")

    def test_rm_R_f_blocked(self) -> None:
        self._assert_blocked("rm -R -f /some/path", "rm -rf")

    def test_rm_fr_blocked(self) -> None:
        self._assert_blocked("rm -fr /some/path", "rm -rf")

    def test_rm_rf_home_blocked(self) -> None:
        self._assert_blocked("rm -rf ~/projects", "rm -rf")

    def test_rm_rf_root_path_blocked(self) -> None:
        self._assert_blocked("rm -rf /", "root or home")

    def test_rm_rf_home_path_blocked(self) -> None:
        self._assert_blocked("rm -rf ~", "root or home")

    def test_rm_rf_bash_c_blocked(self) -> None:
        self._assert_blocked("bash -c 'rm -rf /some/path'", "rm -rf")

    def test_rm_rf_bin_path_blocked(self) -> None:
        self._assert_blocked("/bin/rm -rf /some/path", "rm -rf")

    def test_rm_rf_busybox_blocked(self) -> None:
        self._assert_blocked("busybox rm -rf /some/path", "rm -rf")

    def test_command_substitution_rm_rf_blocked(self) -> None:
        self._assert_blocked("echo $(rm -rf /some/path)", "rm -rf")


class RmRfAllowedTests(SafetyNetTestCase):
    def test_rm_rf_tmp_allowed(self) -> None:
        self._assert_allowed("rm -rf /tmp/test-dir")

    def test_rm_rf_var_tmp_allowed(self) -> None:
        self._assert_allowed("rm -rf /var/tmp/test-dir")

    def test_rm_rf_tmpdir_allowed(self) -> None:
        self._assert_allowed("rm -rf $TMPDIR/test-dir")

    def test_rm_r_without_force_allowed(self) -> None:
        self._assert_allowed("rm -r /some/path")

    def test_rm_f_without_recursive_allowed(self) -> None:
        self._assert_allowed("rm -f /some/path")


class RmRfCwdAwareTests(SafetyNetTestCase):
    def test_rm_rf_relative_path_allowed(self) -> None:
        self._assert_allowed("rm -rf build", cwd=str(self.tmpdir))

    def test_rm_rf_dot_slash_path_allowed(self) -> None:
        self._assert_allowed("rm -rf ./dist", cwd=str(self.tmpdir))

    def test_rm_rf_escapes_cwd_blocked(self) -> None:
        self._assert_blocked("rm -rf ../other", "rm -rf", cwd=str(self.tmpdir))

    def test_rm_rf_dot_blocked(self) -> None:
        self._assert_blocked("rm -rf .", "rm -rf", cwd=str(self.tmpdir))

    def test_rm_rf_after_cd_bypasses_cwd_allowlist_blocked(self) -> None:
        self._assert_blocked("cd .. && rm -rf build", "rm -rf", cwd=str(self.tmpdir))
```

### Git Tests

```python
class GitCheckoutTests(SafetyNetTestCase):
    def test_git_checkout_double_dash_blocked(self) -> None:
        self._assert_blocked("git checkout -- file.txt", "git checkout --")

    def test_git_checkout_ref_double_dash_blocked(self) -> None:
        self._assert_blocked("git checkout HEAD -- file.txt", "git checkout <ref> -- <path>")

    def test_git_checkout_b_allowed(self) -> None:
        self._assert_allowed("git checkout -b new-branch")

    def test_git_checkout_branch_only_allowed(self) -> None:
        self._assert_allowed("git checkout main")


class GitResetTests(SafetyNetTestCase):
    def test_git_reset_hard_blocked(self) -> None:
        self._assert_blocked("git reset --hard", "git reset --hard")

    def test_git_reset_hard_head_blocked(self) -> None:
        self._assert_blocked("git reset --hard HEAD~1", "git reset --hard")

    def test_git_reset_hard_nested_wrapper_bypass_blocked(self) -> None:
        self._assert_blocked("sudo env VAR=1 git reset --hard", "git reset --hard")


class GitCleanTests(SafetyNetTestCase):
    def test_git_clean_f_blocked(self) -> None:
        self._assert_blocked("git clean -f", "git clean")

    def test_git_clean_n_allowed(self) -> None:
        self._assert_allowed("git clean -n")


class GitPushTests(SafetyNetTestCase):
    def test_git_push_force_blocked(self) -> None:
        self._assert_blocked("git push --force", "Force push")

    def test_git_push_force_with_lease_allowed(self) -> None:
        self._assert_allowed("git push --force-with-lease")


class GitStashTests(SafetyNetTestCase):
    def test_git_stash_drop_blocked(self) -> None:
        self._assert_blocked("git stash drop", "git stash drop")

    def test_git_stash_clear_blocked(self) -> None:
        self._assert_blocked("git stash clear", "git stash clear")

    def test_git_stash_allowed(self) -> None:
        self._assert_allowed("git stash")
```

---

## Configuration Examples

### hooks.json

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/safety_net.py"
          }
        ]
      }
    ]
  }
}
```

### pyproject.toml (relevant sections)

```toml
[project]
requires-python = ">=3.10"

[tool.mypy]
python_version = "3.10"
strict = true
disallow_untyped_defs = true

[tool.ruff]
line-length = 88
```

---

## Dependencies

- **Python 3.10+**: Uses modern type hints (`X | None` syntax)
- **Standard library only**: `shlex`, `json`, `os`, `posixpath`, `re`, `sys`
- **No external dependencies** for the core hook

---

## Notes for Implementation

### Note 1: Always Exit 0
The hook always exits 0. The decision to block is communicated via JSON output, not exit code. This is important for hook protocol compliance.

### Note 2: Defense in Depth
Multiple layers of detection:
1. Proper token parsing with shlex
2. Fallback text-based detection when parsing fails
3. Recursive analysis of shell wrappers
4. Interpreter one-liner scanning

### Note 3: CWD Invalidation After cd
When `cd`, `pushd`, or `popd` is detected in a segment, subsequent segments are analyzed without CWD context (set to None) because the working directory has changed.

### Note 4: Case Sensitivity Matters
- Git subcommands are case-insensitive (`git RESET --hard` works)
- Git options may be case-sensitive (`-D` vs `-d` for branch deletion)
- rm options are case-sensitive for `-r` vs `-R` (both mean recursive)

### Note 5: Paranoid Mode vs Strict Mode
- **Strict mode**: Fail-closed on unparseable input (security-focused)
- **Paranoid mode**: Block more aggressively (extra safety for sensitive environments)

### Note 6: Audit Logging
Denied commands are logged to `~/.cc-safety-net/logs/{session_id}.jsonl` with:
- Timestamp (UTC ISO format)
- Command (redacted, max 300 chars)
- Segment that triggered the block
- Reason for blocking
- Current working directory

### Note 7: Token Normalization
Use `posixpath.basename()` to normalize command tokens, allowing detection of `/bin/rm`, `/usr/bin/rm`, etc.

### Note 8: Double-Dash Handling
The `--` separator is critical:
- `rm -rf -- /path` - targets after `--` are paths, not options
- `git checkout --` at position 0 = discard changes
- `git checkout HEAD --` = checkout from ref with pathspec

### Note 9: xargs/parallel Complexity
These commands dynamically substitute input, making static analysis difficult. The implementation:
- Detects replacement tokens (`{}`, `-I`, `-J`)
- Blocks `rm -rf` in templates even when paths look safe
- Recursively analyzes shell wrappers in templates

### Note 10: Cross-Platform Considerations
The implementation uses `posixpath` for path operations to maintain POSIX semantics even on Windows. For true cross-platform support, consider:
- Windows path separators (`\` vs `/`)
- Windows temp paths (`%TEMP%`, `%TMP%`)
- PowerShell equivalents of dangerous commands

---

## Summary

The claude-code-safety-net provides a comprehensive, layered approach to blocking destructive commands:

1. **Protocol**: JSON stdin/stdout with specific hook output structure
2. **Analysis**: Multi-stage parsing with fallback heuristics
3. **Rules**: Modular rule functions for different command types
4. **Modes**: Configurable strictness via environment variables
5. **Testing**: Extensive test coverage with reusable test helpers
6. **Logging**: Audit trail for blocked commands

Key strengths to replicate:
- Thorough edge case handling (wrappers, interpreters, xargs/parallel)
- Safe defaults with configurable paranoid modes
- Clean separation of concerns (parsing, rules, main hook logic)
- Comprehensive test patterns
