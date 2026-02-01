#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# ///

"""
PostToolUse Hook - Enhanced with Micro-Lesson Injection

Existing functionality:
- Session ID injection to resume-context.md
- Tool use logging

NEW functionality:
- Micro-lesson detection and injection (contextual teaching)
- First-time encounter tracking
- Anti-pattern detection for build naming
"""

import json
import re
import sys
from pathlib import Path
from typing import Optional, Dict, Callable
from utils.constants import ensure_session_log_dir


# ============================================================
# MICRO-LESSONS CONFIGURATION
# ============================================================

# Type alias for trigger functions
TriggerFunc = Callable[[str, str], bool]

MICRO_LESSONS: Dict[str, Dict] = {
    'build_created': {
        'triggers': [
            # Build overview.md or any file in 02-builds/ planning folder
            lambda tool, path: (
                tool == 'Write' and
                '02-builds/' in path and
                ('overview.md' in path or '/01-planning/' in path)
            ),
        ],
        'content': '''
━━━ QUICK TIP: BUILDS ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
You just created your first BUILD.

BUILD = Work with an END (this project)
SKILL = Work that REPEATS (weekly reports)

Your build lives in 02-builds/ with planning, resources,
working, and outputs folders.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
'''
    },

    'skill_loaded': {
        'triggers': [
            # SKILL.md read from any skills folder
            lambda tool, path: (
                tool == 'Read' and
                'SKILL.md' in path and
                ('03-skills/' in path or '00-system/skills/' in path)
            ),
        ],
        'content': '''
━━━ QUICK TIP: SKILLS ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
You just loaded a SKILL - a reusable workflow.

SKILL = Same steps, repeat forever (templates, processes)
BUILD = One-time work with an end (projects)

Your custom skills go in 03-skills/
System skills are in 00-system/skills/
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
'''
    },

    'workspace_used': {
        'triggers': [
            lambda tool, path: tool == 'Write' and '04-workspace/' in path,
        ],
        'content': '''
━━━ QUICK TIP: WORKSPACE ━━━━━━━━━━━━━━━━━━━━━━━━━━━
You saved a file to your WORKSPACE (04-workspace/).

This is YOUR space for files, notes, research.
Organize it however makes sense for your work.

The workspace-map.md tracks your folder structure.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
'''
    },

    'memory_updated': {
        'triggers': [
            lambda tool, path: (
                tool == 'Write' and
                '01-memory/' in path and
                ('goals.md' in path or 'core-learnings.md' in path)
            ),
        ],
        'content': '''
━━━ QUICK TIP: MEMORY ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
I just updated your MEMORY (01-memory/).

Memory = What I remember about you between sessions
- goals.md = Your role and objectives
- core-learnings.md = Insights from our work together
- user-config.yaml = Preferences and settings

This context loads automatically every session.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
'''
    },

    'close_session_used': {
        'triggers': [
            # close-session skill loaded
            lambda tool, path: (
                tool == 'Read' and
                'close-session/SKILL.md' in path
            ),
        ],
        'content': '''
━━━ QUICK TIP: CLOSE SESSION ━━━━━━━━━━━━━━━━━━━━━━━
You're closing your session properly - great habit!

CLOSE SESSION does:
- Saves progress to resume-context.md
- Updates core-learnings.md with insights
- Ensures work can be resumed next time

Say "done" or "close session" when finishing work.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
'''
    },

    'resume_update_reminder': {
        'triggers': [
            # Edit to 04-steps.md (checkbox completion)
            lambda tool, path: (
                tool == 'Edit' and
                '04-steps.md' in path and
                '02-builds/' in path
            ),
        ],
        'content': '''
━━━ REMINDER: UPDATE PROGRESS SUMMARY ━━━━━━━━━━━━━━
You just updated 04-steps.md checkboxes.

**Now update resume-context.md Progress Summary:**

### Latest Session (DATE)

**Completed this session:**
- [x] Task description
- [x] Another task

**Key decisions:**
- Decision made and why

**Next steps:**
1. Next task to do
2. Following task

This helps future sessions resume smoothly.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
'''
    },
}


# ============================================================
# ANTI-PATTERN DETECTION
# ============================================================

ANTI_PATTERNS: Dict[str, Dict] = {
    'repeated_build_pattern': {
        'detect': lambda name: bool(re.search(
            r'.*-\d+$|'                           # ends with number (task-1)
            r'.*-(january|february|march|april|may|june|july|august|september|october|november|december)$|'  # full month names
            r'.*-(jan|feb|mar|apr|jun|jul|aug|sep|oct|nov|dec)$|'  # abbreviated months
            r'.*-week-?\d+$|'                     # week-1, week1
            r'.*-v\d+$',                          # version numbers (report-v2)
            name.lower()
        )),
        'warning': '''
[!] PATTERN CHECK

You're creating "{name}" - this looks like it might repeat.

BUILDS are for one-time work (has a finish line)
SKILLS are for repeating work (same steps, new data)

If you'll create "{name}-february", "{name}-march"...
-> Consider making this a SKILL instead

Continue with Build? Just say "yes" or create a skill with "create skill".
'''
    }
}


# ============================================================
# STATE MANAGEMENT
# ============================================================

def get_first_encounters(config_path: Path) -> Dict[str, bool]:
    """Read first_encounters from user-config.yaml using regex."""
    if not config_path.exists():
        return {}

    try:
        content = config_path.read_text(encoding='utf-8')
    except Exception:
        return {}

    encounters = {}

    # Parse YAML-like structure with regex
    for key in MICRO_LESSONS.keys():
        pattern = rf'{key}:\s*(true|false)'
        match = re.search(pattern, content)
        if match:
            encounters[key] = match.group(1) == 'true'
        else:
            encounters[key] = False

    return encounters


def get_onboarding_status(config_path: Path) -> str:
    """Read onboarding.status from user-config.yaml.

    Returns: 'not_started', 'in_progress', or 'complete'
    """
    if not config_path.exists():
        return 'not_started'

    try:
        content = config_path.read_text(encoding='utf-8')
    except Exception:
        return 'not_started'

    # Parse YAML-like structure with regex
    pattern = r'^\s*status:\s*["\']?([^"\'\n]+)["\']?'

    # Search within onboarding section
    onboarding_section_match = re.search(r'onboarding:\s*\n((?:  .*\n)*)', content, re.MULTILINE)
    if onboarding_section_match:
        onboarding_content = onboarding_section_match.group(1)
        status_match = re.search(pattern, onboarding_content, re.MULTILINE)
        if status_match:
            return status_match.group(1).strip()

    return 'not_started'


def get_anti_patterns_warned(config_path: Path) -> Dict[str, bool]:
    """Read anti_patterns_warned from user-config.yaml."""
    if not config_path.exists():
        return {}

    try:
        content = config_path.read_text(encoding='utf-8')
    except Exception:
        return {}

    warned = {}

    for key in ANTI_PATTERNS.keys():
        pattern = rf'{key}:\s*(true|false)'
        match = re.search(pattern, content)
        if match:
            warned[key] = match.group(1) == 'true'
        else:
            warned[key] = False

    return warned


def update_config_flag(config_path: Path, section: str, flag: str, value: bool = True) -> bool:
    """Update a flag in user-config.yaml."""
    if not config_path.exists():
        return False

    try:
        content = config_path.read_text(encoding='utf-8')
    except Exception:
        return False

    value_str = 'true' if value else 'false'

    # Check if section exists
    if f'{section}:' not in content:
        # Add section before learning_tracker or at end of frontmatter
        if 'learning_tracker:' in content:
            content = content.replace(
                'learning_tracker:',
                f'{section}:\n  {flag}: {value_str}\n\nlearning_tracker:'
            )
        elif '---\n\n#' in content:
            # Add before the closing --- that ends frontmatter
            content = content.replace(
                '---\n\n#',
                f'{section}:\n  {flag}: {value_str}\n---\n\n#'
            )
        else:
            # Fallback: insert before last ---
            parts = content.rsplit('---', 1)
            if len(parts) == 2:
                content = parts[0] + f'{section}:\n  {flag}: {value_str}\n---' + parts[1]
    else:
        # Update or add the specific flag
        pattern = rf'({flag}:\s*)(true|false)'
        if re.search(pattern, content):
            content = re.sub(pattern, rf'\g<1>{value_str}', content)
        else:
            # Add after section header
            content = re.sub(
                rf'({section}:)',
                rf'\1\n  {flag}: {value_str}',
                content
            )

    try:
        config_path.write_text(content, encoding='utf-8')
        return True
    except Exception:
        return False


# ============================================================
# LESSON CHECKING
# ============================================================

def is_checkbox_completion(tool_input: dict) -> bool:
    """Check if an Edit operation completes a checkbox (- [ ] → - [x])."""
    old_string = tool_input.get('old_string', '')
    new_string = tool_input.get('new_string', '')

    # Check if we're converting unchecked to checked
    has_unchecked_before = '- [ ]' in old_string
    has_checked_after = '- [x]' in new_string or '- [X]' in new_string

    return has_unchecked_before and has_checked_after


def check_micro_lesson(tool_name: str, tool_input: dict, config_path: Path) -> Optional[str]:
    """Check if a micro-lesson should be shown. Returns lesson content or None."""

    file_path = tool_input.get('file_path', '')

    # IMPORTANT: Suppress micro-learnings during onboarding
    onboarding_status = get_onboarding_status(config_path)
    if onboarding_status == 'in_progress':
        return None

    # Get current state
    encounters = get_first_encounters(config_path)

    for lesson_id, lesson_data in MICRO_LESSONS.items():
        # Skip if already shown
        if encounters.get(lesson_id, False):
            continue

        # Special case: resume_update_reminder needs checkbox completion check
        if lesson_id == 'resume_update_reminder':
            if tool_name == 'Edit' and '04-steps.md' in file_path and '02-builds/' in file_path:
                if is_checkbox_completion(tool_input):
                    update_config_flag(config_path, 'first_encounters', lesson_id, True)
                    return lesson_data['content']
            continue

        # Check triggers (standard path)
        for trigger_fn in lesson_data['triggers']:
            try:
                if trigger_fn(tool_name, file_path):
                    # Mark as shown
                    update_config_flag(config_path, 'first_encounters', lesson_id, True)
                    return lesson_data['content']
            except Exception:
                continue

    return None


def check_anti_pattern(tool_name: str, tool_input: dict, config_path: Path) -> Optional[str]:
    """Check for anti-patterns. Returns warning or None."""

    file_path = tool_input.get('file_path', '')

    # Only check on build creation
    if tool_name != 'Write' or '02-builds/' not in file_path:
        return None

    # Extract build name from path
    # Pattern: 02-builds/XX-build-name/...
    match = re.search(r'02-builds/\d+-([^/]+)/', file_path)
    if not match:
        return None

    build_name = match.group(1)

    # Get warned state
    warned = get_anti_patterns_warned(config_path)

    for pattern_id, pattern_data in ANTI_PATTERNS.items():
        # Skip if already warned
        if warned.get(pattern_id, False):
            continue

        try:
            if pattern_data['detect'](build_name):
                # Mark as warned
                update_config_flag(config_path, 'anti_patterns_warned', pattern_id, True)
                return pattern_data['warning'].format(name=build_name)
        except Exception:
            continue

    return None


# ============================================================
# EXISTING HELPER FUNCTIONS
# ============================================================

def inject_session_id_to_resume_context(file_path: str, session_id: str) -> bool:
    """
    Inject session_id into newly created resume-context.md files.

    This enables SessionStart to find the build by exact session_id match.
    Called after Write tool creates a resume-context.md file.
    """
    if not file_path or not session_id or session_id == "unknown":
        return False

    path = Path(file_path)
    if not path.name == "resume-context.md":
        return False

    if not path.exists():
        return False

    try:
        content = path.read_text(encoding="utf-8")

        # Skip if session_id already present
        if "session_id:" in content:
            return False

        # Add session_id after first ---
        if content.startswith("---"):
            content = content.replace(
                "---\n",
                f'---\nsession_id: "{session_id}"\n',
                1
            )
            path.write_text(content, encoding="utf-8")
            return True

        return False
    except Exception:
        return False


def log_tool_use(input_data: dict, session_id: str) -> None:
    """Log tool use to session log directory."""
    try:
        log_dir = ensure_session_log_dir(session_id)
        log_path = log_dir / "post_tool_use.json"

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
    except Exception:
        pass  # Silent failure for logging


# ============================================================
# MAIN HOOK FUNCTION
# ============================================================

def main():
    try:
        # Read JSON input from stdin
        input_data = json.load(sys.stdin)

        # Extract data
        session_id = input_data.get("session_id", "unknown")
        tool_name = input_data.get("tool_name", "")
        tool_input = input_data.get("tool_input", {})

        # --- EXISTING FUNCTIONALITY ---

        # Inject session_id into newly created resume-context.md files
        if tool_name == "Write":
            file_path = tool_input.get("file_path", "")
            inject_session_id_to_resume_context(file_path, session_id)

        # Log tool use
        log_tool_use(input_data, session_id)

        # --- NEW: MICRO-LESSON INJECTION ---

        config_path = Path('01-memory/user-config.yaml')

        # Check for micro-lesson first
        lesson = check_micro_lesson(tool_name, tool_input, config_path)
        if lesson:
            output = {
                "hookSpecificOutput": {
                    "hookEventName": "PostToolUse",
                    "additionalContext": lesson
                }
            }
            print(json.dumps(output), flush=True)
            sys.exit(0)

        # Check for anti-pattern warning
        warning = check_anti_pattern(tool_name, tool_input, config_path)
        if warning:
            output = {
                "hookSpecificOutput": {
                    "hookEventName": "PostToolUse",
                    "additionalContext": warning
                }
            }
            print(json.dumps(output), flush=True)
            sys.exit(0)

        # No lesson or warning - exit cleanly
        sys.exit(0)

    except json.JSONDecodeError:
        # Handle JSON decode errors gracefully
        sys.exit(0)
    except Exception:
        # Exit cleanly on any other error
        sys.exit(0)


if __name__ == "__main__":
    main()
