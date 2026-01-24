#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# ///

import json
import sys
import os
import re
from pathlib import Path
from datetime import datetime

# Add parent directory to path for utils imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.constants import ensure_session_log_dir
from utils.registry import lookup_shortcut, detect_type_from_path, extract_id_from_path


# =============================================================================
# EXECUTABLE DETECTION SYSTEM (v2 - Registry-based)
# =============================================================================
# Executables: agent, skill, task, workflow
# Non-executables: definition, blueprint, rule, checklist, automation, documentation, mental-model
#
# Detection Strategy:
# - Bash: Registry lookup from shortcut (single source of truth)
# - Read: Path pattern matching (fallback)
# =============================================================================

EXECUTABLE_TYPES = {"agent", "skill", "task", "workflow"}


def detect_executable(tool_name, tool_input):
    """
    Detect if this tool call is loading an executable entity.

    Strategy:
    - Bash: Registry lookup from shortcut, or parse shortcut prefix
    - Read: Path pattern matching (fallback)

    Returns:
        dict with {type, id, target, shortcut, detection_method} or None
    """
    if tool_name == "Bash":
        command = tool_input.get("command", "")
        # Extract shortcut from shortcut_resolver call
        match = re.search(r"shortcut_resolver\.py\s+(~[a-zA-Z0-9_:-]+)", command)
        if match:
            shortcut = match.group(1)
            # Registry lookup - single source of truth
            resolved = lookup_shortcut(shortcut)
            if resolved and resolved["type"] in EXECUTABLE_TYPES:
                return {
                    "type": resolved["type"],
                    "id": resolved["id"],
                    "target": resolved["path"],
                    "shortcut": shortcut,
                    "detection_method": "bash"
                }

            # Fallback: Parse shortcut prefix for type (e.g., ~agent:name, ~task:name)
            # Also handle direct agent shortcuts like ~meta-architect
            shortcut_parsed = parse_shortcut_for_type(shortcut)
            if shortcut_parsed and shortcut_parsed["type"] in EXECUTABLE_TYPES:
                return {
                    "type": shortcut_parsed["type"],
                    "id": shortcut_parsed["id"],
                    "target": "",  # Unknown without registry
                    "shortcut": shortcut,
                    "detection_method": "bash"
                }

    elif tool_name == "Read":
        file_path = tool_input.get("file_path", "")
        # Path pattern matching (fallback for direct file reads)
        detected = detect_from_path_patterns(file_path)
        if detected:
            return {
                "type": detected["type"],
                "id": detected["id"],
                "target": file_path,
                "shortcut": None,
                "detection_method": "read"
            }

    return None


def parse_shortcut_for_type(shortcut):
    """
    Parse shortcut to extract type and id from explicit prefix format.

    Formats:
    - ~agent:meta-architect -> type=agent, id=meta-architect
    - ~task:plan-build -> type=task, id=plan-build
    - ~skill:paper-search -> type=skill, id=paper-search
    - ~workflow:research -> type=workflow, id=research

    Note: For shortcuts without explicit type prefix (e.g., ~meta-architect),
    use the registry lookup instead. This function only handles explicit prefixes.

    Returns: {"type": "...", "id": "..."} or None
    """
    # Explicit type prefix: ~type:id
    match = re.match(r"~(agent|skill|task|workflow):([a-zA-Z0-9_-]+)", shortcut)
    if match:
        return {
            "type": match.group(1),
            "id": match.group(2)
        }

    return None


def detect_from_path_patterns(file_path):
    """
    Detect executable from file path using registry utilities.

    Uses detect_type_from_path() and extract_id_from_path() from registry.py
    as the single source of truth for path pattern matching.
    """
    exec_type = detect_type_from_path(file_path)
    if exec_type and exec_type in EXECUTABLE_TYPES:
        return {
            "type": exec_type,
            "id": extract_id_from_path(file_path),
        }
    return None




def is_dangerous_rm_command(command):
    """
    Comprehensive detection of dangerous rm commands.
    Matches various forms of rm -rf and similar destructive patterns.
    """
    # Normalize command by removing extra spaces and converting to lowercase
    normalized = " ".join(command.lower().split())

    # Pattern 1: Standard rm -rf variations
    patterns = [
        r"\brm\s+.*-[a-z]*r[a-z]*f",  # rm -rf, rm -fr, rm -Rf, etc.
        r"\brm\s+.*-[a-z]*f[a-z]*r",  # rm -fr variations
        r"\brm\s+--recursive\s+--force",  # rm --recursive --force
        r"\brm\s+--force\s+--recursive",  # rm --force --recursive
        r"\brm\s+-r\s+.*-f",  # rm -r ... -f
        r"\brm\s+-f\s+.*-r",  # rm -f ... -r
    ]

    # Check for dangerous patterns
    for pattern in patterns:
        if re.search(pattern, normalized):
            return True

    # Pattern 2: Check for rm with recursive flag targeting dangerous paths
    dangerous_paths = [
        r"/",  # Root directory
        r"/\*",  # Root with wildcard
        r"~",  # Home directory
        r"~/",  # Home directory path
        r"\$HOME",  # Home environment variable
        r"\.\.",  # Parent directory references
        r"\*",  # Wildcards in general rm -rf context
        r"\.",  # Current directory
        r"\.\s*$",  # Current directory at end of command
    ]

    if re.search(r"\brm\s+.*-[a-z]*r", normalized):  # If rm has recursive flag
        for path in dangerous_paths:
            if re.search(path, normalized):
                return True

    return False


# =============================================================================
# GIT DANGEROUS OPERATIONS SAFETY
# =============================================================================
# These operations can cause irreversible data loss and should be blocked
# unless user explicitly confirms they understand the risk.
# =============================================================================

GIT_DANGEROUS_PATTERNS = [
    # Hard reset - loses uncommitted changes
    (r"git\s+reset\s+--hard", "git reset --hard (loses uncommitted changes)"),
    (r"git\s+reset\s+--merge", "git reset --merge (discards merge conflicts)"),

    # Force push - can rewrite remote history
    (r"git\s+push\s+.*--force(?!-with-lease)", "git push --force (use --force-with-lease instead)"),
    (r"git\s+push\s+.*-f\b(?!orce-with-lease)", "git push -f (use --force-with-lease instead)"),

    # Branch deletion with force
    (r"git\s+branch\s+-D\b", "git branch -D (force delete, use -d for safe delete)"),

    # Dangerous checkout that discards changes
    (r"git\s+checkout\s+--\s+\.", "git checkout -- . (discards all local changes)"),

    # Clean with force - deletes untracked files
    (r"git\s+clean\s+.*-[a-z]*f", "git clean -f (deletes untracked files permanently)"),

    # Stash operations that lose data
    (r"git\s+stash\s+(drop|clear)", "git stash drop/clear (loses stashed changes)"),
]


def is_dangerous_git_command(command):
    """
    Detect dangerous git commands that could cause data loss.

    Returns:
        tuple: (is_dangerous: bool, reason: str)
    """
    normalized = " ".join(command.lower().split())

    for pattern, reason in GIT_DANGEROUS_PATTERNS:
        if re.search(pattern, normalized, re.IGNORECASE):
            return True, reason

    return False, ""


# TRASH pattern guidance for safe file deletion
TRASH_GUIDANCE = """
SAFE ALTERNATIVE: Instead of rm, use the TRASH pattern:
1. Create TRASH/ directory if needed: mkdir -p TRASH
2. Move files: mv <files> TRASH/
3. Add entry in TRASH-FILES.md with date and reason
4. Files can be recovered until manually purged
"""


def is_env_file_access(tool_name, tool_input):
    """
    Check if any tool is trying to access .env files containing sensitive data.
    """
    if tool_name in ["Read", "Edit", "MultiEdit", "Write", "Bash"]:
        # Check file paths for file-based tools
        if tool_name in ["Read", "Edit", "MultiEdit", "Write"]:
            file_path = tool_input.get("file_path", "")
            if ".env" in file_path and not file_path.endswith(".env.sample"):
                return True

        # Check bash commands for .env file access
        elif tool_name == "Bash":
            command = tool_input.get("command", "")
            # Pattern to detect .env file access (but allow .env.sample)
            env_patterns = [
                r"\b\.env\b(?!\.sample)",  # .env but not .env.sample
                r"cat\s+.*\.env\b(?!\.sample)",  # cat .env
                r"echo\s+.*>\s*\.env\b(?!\.sample)",  # echo > .env
                r"touch\s+.*\.env\b(?!\.sample)",  # touch .env
                r"cp\s+.*\.env\b(?!\.sample)",  # cp .env
                r"mv\s+.*\.env\b(?!\.sample)",  # mv .env
            ]

            for pattern in env_patterns:
                if re.search(pattern, command):
                    return True

    return False


def main():
    try:
        # Read JSON input from stdin
        input_data = json.load(sys.stdin)

        tool_name = input_data.get("tool_name", "")
        tool_input = input_data.get("tool_input", {})

        # Check for .env file access (blocks access to sensitive environment files)
        if is_env_file_access(tool_name, tool_input):
            print(
                "BLOCKED: Access to .env files containing sensitive data is prohibited",
                file=sys.stderr,
            )
            print("Use .env.sample for template files instead", file=sys.stderr)
            sys.exit(2)  # Exit code 2 blocks tool call and shows error to Claude

        # Check for dangerous Bash commands
        if tool_name == "Bash":
            command = tool_input.get("command", "")

            # Block rm -rf commands with comprehensive pattern matching
            if is_dangerous_rm_command(command):
                print(
                    "BLOCKED: Dangerous rm command detected and prevented",
                    file=sys.stderr,
                )
                print(TRASH_GUIDANCE, file=sys.stderr)
                sys.exit(2)  # Exit code 2 blocks tool call and shows error to Claude

            # Block dangerous git commands
            is_dangerous_git, git_reason = is_dangerous_git_command(command)
            if is_dangerous_git:
                print(
                    f"BLOCKED: {git_reason}",
                    file=sys.stderr,
                )
                print("These operations can cause irreversible data loss.", file=sys.stderr)
                print("If you need to proceed, ask user to run the command manually.", file=sys.stderr)
                sys.exit(2)  # Exit code 2 blocks tool call

        # Extract session_id
        session_id = input_data.get("session_id", "unknown")

        # Ensure session log directory exists
        log_dir = ensure_session_log_dir(session_id)
        log_path = log_dir / "pre_tool_use.json"

        # =================================================================
        # EXECUTABLE DETECTION (v2)
        # =================================================================
        # Detect if this tool call is loading an executable (agent/skill/task/workflow)
        # Note: Observability server removed - detection kept for future use
        executable = detect_executable(tool_name, tool_input)

        # Read existing log data or initialize empty list
        if log_path.exists():
            with open(log_path, "r") as f:
                try:
                    log_data = json.load(f)
                except (json.JSONDecodeError, ValueError):
                    log_data = []
        else:
            log_data = []

        # Append new data
        log_data.append(input_data)

        # Write back to file with formatting
        with open(log_path, "w") as f:
            json.dump(log_data, f, indent=2)

        sys.exit(0)

    except json.JSONDecodeError:
        # Gracefully handle JSON decode errors
        sys.exit(0)
    except Exception:
        # Handle any other errors gracefully
        sys.exit(0)


if __name__ == "__main__":
    main()
