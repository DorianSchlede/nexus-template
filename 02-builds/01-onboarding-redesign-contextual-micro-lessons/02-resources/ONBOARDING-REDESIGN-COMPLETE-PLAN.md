# NEXUS ONBOARDING REDESIGN - COMPLETE IMPLEMENTATION PLAN

> **CRITICAL CONTEXT PRESERVATION DOCUMENT**
> Created: 2026-01-17
> Purpose: Capture ALL implementation details for "Teach Through Doing" onboarding redesign
> Status: PLANNING COMPLETE - READY FOR IMPLEMENTATION

---

## TABLE OF CONTENTS

1. [Problem Analysis](#1-problem-analysis)
2. [Core Philosophy](#2-core-philosophy)
3. [Technical Architecture](#3-technical-architecture)
4. [Implementation Details](#4-implementation-details)
5. [File Changes Required](#5-file-changes-required)
6. [Micro-Lessons Content](#6-micro-lessons-content)
7. [Anti-Pattern Detection](#7-anti-pattern-detection)
8. [Testing Plan](#8-testing-plan)
9. [Migration Path](#9-migration-path)

---

## 1. PROBLEM ANALYSIS

### Source: Sascha-Dorian Onboarding Transcript (2+ hours)

**Key Pain Points Observed:**

1. **Concept Overload at Start**
   - User got overwhelmed by Skills, Builds, Workspace, Memory thrown at them simultaneously
   - Quote: *"du gibst mir jetzt hier ganz viele Konzepte... führe mich mal bitte Stück für Stück durchs Onboarding"*

2. **Explaining Before Doing**
   - AI explained concepts user didn't understand yet
   - Quote: *"Ja, jetzt werden halt hier Skills erklärt, aber du weißt noch gar nicht, was Skills sind"*

3. **No Immediate Value**
   - After 2 hours, user got no tangible output
   - Quote: *"Hast du jetzt schon Value bekommen? Ich würde sagen, nein."*

4. **Terminology Confusion**
   - "Build" not intuitive
   - Quote: *"Ich mache ein Bild. Hört sich irgendwie nicht so geil an."*

5. **Time to First Value Problem**
   - Quote: *"Time to first value ist extrem wichtig und das ist bei dem Ding so ein bisschen das Problem"*

### Current Learning Skills Structure (FRAGMENTED)

```
00-system/skills/learning/
├── setup-memory/SKILL.md      (8 min)
├── setup-workspace/SKILL.md   (5-8 min)
├── learn-builds/SKILL.md      (8-10 min) - NOW learn-builds
├── learn-skills/SKILL.md      (10-12 min)
├── learn-integrations/SKILL.md (10-12 min)
└── learn-nexus/SKILL.md       (15-18 min)
```

**Problem:** User doesn't know which to do first, or why these concepts matter. Skills assume user already understands Nexus model.

---

## 2. CORE PHILOSOPHY

### The Golden Rule (from Dorian)

> *"Du willst halt die Leute machen einfach was... und nachdem es passiert ist, sagst du ihm, was gerade passiert ist und wieso es für sie relevant ist"*

**Translation:** Let users DO something, then explain what just happened and why it matters.

### The Pattern: Show Then Tell

```
1. User states intent → "I want to plan my career transition"
2. System acts → Creates Build structure, loads plan-build skill
3. System explains → "I just created a Build folder for this.
                      Builds are how Nexus tracks work with a
                      beginning and end. You'll find it in 02-builds/"
4. User continues → Works on their actual goal
5. Concepts emerge → Each new concept explained at moment of encounter
```

### Key Principles

| Principle | Description |
|-----------|-------------|
| **Action First** | Never explain before action. Always explain AFTER action. |
| **15 Seconds Max** | Each explanation takes 15 seconds max, then continue work |
| **One Lesson Per Session** | Never overwhelm - one concept at a time |
| **Show Don't Tell** | Point to what was created, name it, explain why |
| **Capture Through Work** | Goals captured FROM builds, not before them |

---

## 3. TECHNICAL ARCHITECTURE

### The Mechanism: PostToolUse Hook with additionalContext

Claude Code hooks can inject content into Claude's context using this pattern:

```python
# Hook outputs JSON to stdout:
{
    "hookSpecificOutput": {
        "hookEventName": "PostToolUse",
        "additionalContext": "━━━ QUICK TIP: BUILDS ━━━..."
    }
}
```

This `additionalContext` gets injected as a `<system-reminder>` that Claude sees BEFORE generating its response.

### Flow Diagram

```
User: "Create a build for career planning"
                ↓
Claude calls Write tool
    → Creates 02-builds/01-career-planning/overview.md
                ↓
Claude Code runs PostToolUse hook
    → Hook receives: {tool_name: "Write", tool_input: {file_path: "..."}}
    → Hook detects: path matches build_created trigger
    → Hook checks: first_encounters.build_created == false
    → Hook updates: user-config.yaml → build_created: true
    → Hook outputs: JSON with additionalContext
                ↓
Claude Code injects into Claude's context:
    <system-reminder>
    PostToolUse hook additional context: ━━━ QUICK TIP: BUILDS ━━━...
    </system-reminder>
                ↓
Claude generates response incorporating the lesson naturally
                ↓
Next build: hook sees build_created: true, skips lesson
```

### State Storage in user-config.yaml

```yaml
# Add to 01-memory/user-config.yaml
first_encounters:
  build_created: false      # First build folder created
  skill_loaded: false       # First SKILL.md read
  workspace_used: false     # First file saved to 04-workspace/
  memory_updated: false     # First update to 01-memory/
  close_session_used: false # First close-session skill used
  integration_connected: false # First integration setup

# Anti-patterns (warn once)
anti_patterns_warned:
  repeated_build_pattern: false  # report-jan, report-feb detected
```

---

## 4. IMPLEMENTATION DETAILS

### A. PostToolUse Hook Enhancement

**File:** `.claude/hooks/post_tool_use.py`

**Add to existing hook:**

```python
#!/usr/bin/env python3
"""
PostToolUse Hook - Enhanced with Micro-Lesson Injection

Existing functionality:
- Session ID injection to resume-context.md
- Tool use logging

NEW functionality:
- Micro-lesson detection and injection
- First-time encounter tracking
- Anti-pattern detection
"""

import json
import sys
import re
from pathlib import Path

# ============================================================
# MICRO-LESSONS CONFIGURATION
# ============================================================

MICRO_LESSONS = {
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
}

# ============================================================
# ANTI-PATTERN DETECTION
# ============================================================

ANTI_PATTERNS = {
    'repeated_build_pattern': {
        'detect': lambda name: bool(re.search(
            r'.*-\d+$|'                           # ends with number
            r'.*-(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)$|'  # month names
            r'.*-week-?\d+$|'                     # week-1, week1
            r'.*-v\d+$',                          # version numbers
            name.lower()
        )),
        'warning': '''
⚠️ PATTERN CHECK

You're creating "{name}" - this looks like it might repeat.

BUILDS are for one-time work (has a finish line)
SKILLS are for repeating work (same steps, new data)

If you'll create "{name}-february", "{name}-march"...
→ Consider making this a SKILL instead

Continue with Build? Just say "yes" or create a skill with "create skill".
'''
    }
}

# ============================================================
# STATE MANAGEMENT
# ============================================================

def get_first_encounters(config_path: Path) -> dict:
    """Read first_encounters from user-config.yaml using regex."""
    if not config_path.exists():
        return {}

    content = config_path.read_text()
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


def get_anti_patterns_warned(config_path: Path) -> dict:
    """Read anti_patterns_warned from user-config.yaml."""
    if not config_path.exists():
        return {}

    content = config_path.read_text()
    warned = {}

    for key in ANTI_PATTERNS.keys():
        pattern = rf'{key}:\s*(true|false)'
        match = re.search(pattern, content)
        if match:
            warned[key] = match.group(1) == 'true'
        else:
            warned[key] = False

    return warned


def update_config_flag(config_path: Path, section: str, flag: str, value: bool = True):
    """Update a flag in user-config.yaml."""
    if not config_path.exists():
        return

    content = config_path.read_text()
    value_str = 'true' if value else 'false'

    # Check if section exists
    if f'{section}:' not in content:
        # Add section before learning_tracker or at end
        if 'learning_tracker:' in content:
            content = content.replace(
                'learning_tracker:',
                f'{section}:\n  {flag}: {value_str}\n\nlearning_tracker:'
            )
        else:
            content += f'\n{section}:\n  {flag}: {value_str}\n'
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

    config_path.write_text(content)


# ============================================================
# LESSON CHECKING
# ============================================================

def check_micro_lesson(tool_name: str, tool_input: dict, config_path: Path) -> str | None:
    """Check if a micro-lesson should be shown. Returns lesson content or None."""

    file_path = tool_input.get('file_path', '')

    # Get current state
    encounters = get_first_encounters(config_path)

    for lesson_id, lesson_data in MICRO_LESSONS.items():
        # Skip if already shown
        if encounters.get(lesson_id, False):
            continue

        # Check triggers
        for trigger_fn in lesson_data['triggers']:
            try:
                if trigger_fn(tool_name, file_path):
                    # Mark as shown
                    update_config_flag(config_path, 'first_encounters', lesson_id, True)
                    return lesson_data['content']
            except Exception:
                continue

    return None


def check_anti_pattern(tool_name: str, tool_input: dict, config_path: Path) -> str | None:
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
# MAIN HOOK FUNCTION
# ============================================================

def main():
    try:
        input_data = json.load(sys.stdin)
        tool_name = input_data.get('tool_name', '')
        tool_input = input_data.get('tool_input', {})
        session_id = input_data.get('session_id', 'unknown')

        # --- EXISTING FUNCTIONALITY ---
        # (Keep existing session_id injection and logging code)

        # Inject session_id into resume-context.md
        if tool_name == 'Write':
            file_path = tool_input.get('file_path', '')
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
        sys.exit(0)
    except Exception:
        sys.exit(0)


# ============================================================
# EXISTING HELPER FUNCTIONS (Keep these)
# ============================================================

def inject_session_id_to_resume_context(file_path: str, session_id: str) -> bool:
    """Existing function - keep as-is."""
    # ... existing implementation ...
    pass


def log_tool_use(input_data: dict, session_id: str):
    """Existing function - keep as-is."""
    # ... existing implementation ...
    pass


if __name__ == '__main__':
    main()
```

### B. User-Config Template Update

**File:** `00-system/core/nexus/templates/user-config.yaml`

**Add these sections:**

```yaml
# ============================================================
# FIRST ENCOUNTERS - Micro-lesson tracking
# ============================================================
# These flags track whether user has seen each contextual lesson.
# Set to true after first encounter - lesson never shown again.

first_encounters:
  build_created: false      # First build folder created
  skill_loaded: false       # First SKILL.md read
  workspace_used: false     # First file saved to 04-workspace/
  memory_updated: false     # First update to 01-memory/
  close_session_used: false # First close-session skill used

# ============================================================
# ANTI-PATTERNS WARNED - One-time warnings
# ============================================================
# Tracks which anti-pattern warnings have been shown.

anti_patterns_warned:
  repeated_build_pattern: false  # report-jan, report-feb detected
```

### C. Orchestrator Update

**File:** `00-system/core/orchestrator.md`

**Add this section:**

```markdown
<section id="contextual-teaching">
## Contextual Teaching (Micro-Lessons)

**Principle**: Never explain before action. Always explain AFTER action, briefly.

### How It Works

The PostToolUse hook automatically injects micro-lessons when users encounter
concepts for the first time. You don't need to do anything special - the hook
handles detection and injection.

### When Lessons Appear

| First-Time Action | Lesson Shown |
|-------------------|--------------|
| Create build folder | "BUILD = Work with an END" |
| Load SKILL.md | "SKILL = Work that REPEATS" |
| Save to 04-workspace/ | "WORKSPACE = Your file space" |
| Update 01-memory/ | "MEMORY = Cross-session context" |
| Use close-session | "CLOSE SESSION = Proper ending" |

### Your Role

1. **Continue naturally** - The lesson appears, incorporate it smoothly
2. **Don't repeat** - Lessons only show once, no need to re-explain
3. **Stay on task** - 15 seconds for lesson, then back to user's goal

### Anti-Pattern Detection

The hook also warns about anti-patterns (once per pattern):

| Pattern | Warning |
|---------|---------|
| `report-january`, `task-1` | "This looks like repeating work - consider a Skill" |

</section>
```

---

## 5. FILE CHANGES REQUIRED

### Must Change

| File | Change Type | Description |
|------|-------------|-------------|
| `.claude/hooks/post_tool_use.py` | MODIFY | Add micro-lesson detection and injection |
| `01-memory/user-config.yaml` | MODIFY | Add first_encounters and anti_patterns_warned sections |
| `00-system/core/nexus/templates/user-config.yaml` | MODIFY | Add template for new sections |
| `00-system/core/orchestrator.md` | MODIFY | Add contextual-teaching section |

### Optional (Phase 2)

| File | Change Type | Description |
|------|-------------|-------------|
| `00-system/skills/learning/learn-builds/SKILL.md` | RENAME/MODIFY | Become optional "deep-dive" skill |
| `00-system/skills/learning/learn-skills/SKILL.md` | RENAME/MODIFY | Become optional "deep-dive" skill |
| `.claude/hooks/session_start.py` | MODIFY | Update startup to ask "What do you want to work on?" |

### No Change Needed

| File | Reason |
|------|--------|
| `00-system/skills/builds/plan-build/SKILL.md` | Teaching happens via hook, not skill |
| `00-system/skills/builds/execute-build/SKILL.md` | Teaching happens via hook, not skill |
| Any other skill files | Hook handles injection centrally |

---

## 6. MICRO-LESSONS CONTENT

### Lesson: build_created

```
━━━ QUICK TIP: BUILDS ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
You just created your first BUILD.

BUILD = Work with an END (this project)
SKILL = Work that REPEATS (weekly reports)

Your build lives in 02-builds/ with planning, resources,
working, and outputs folders.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Trigger:** Write to `02-builds/*/overview.md` or `02-builds/*/01-planning/*`

---

### Lesson: skill_loaded

```
━━━ QUICK TIP: SKILLS ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
You just loaded a SKILL - a reusable workflow.

SKILL = Same steps, repeat forever (templates, processes)
BUILD = One-time work with an end (projects)

Your custom skills go in 03-skills/
System skills are in 00-system/skills/
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Trigger:** Read `SKILL.md` from `03-skills/` or `00-system/skills/`

---

### Lesson: workspace_used

```
━━━ QUICK TIP: WORKSPACE ━━━━━━━━━━━━━━━━━━━━━━━━━━━
You saved a file to your WORKSPACE (04-workspace/).

This is YOUR space for files, notes, research.
Organize it however makes sense for your work.

The workspace-map.md tracks your folder structure.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Trigger:** Write to `04-workspace/*`

---

### Lesson: memory_updated

```
━━━ QUICK TIP: MEMORY ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
I just updated your MEMORY (01-memory/).

Memory = What I remember about you between sessions
- goals.md = Your role and objectives
- core-learnings.md = Insights from our work together
- user-config.yaml = Preferences and settings

This context loads automatically every session.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Trigger:** Write to `01-memory/goals.md` or `01-memory/core-learnings.md`

---

### Lesson: close_session_used

```
━━━ QUICK TIP: CLOSE SESSION ━━━━━━━━━━━━━━━━━━━━━━━
You're closing your session properly - great habit!

CLOSE SESSION does:
- Saves progress to resume-context.md
- Updates core-learnings.md with insights
- Ensures work can be resumed next time

Say "done" or "close session" when finishing work.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Trigger:** Read `close-session/SKILL.md`

---

## 7. ANTI-PATTERN DETECTION

### Pattern: repeated_build_pattern

**Detection Regex:**
```python
r'.*-\d+$|'                           # ends with number (task-1)
r'.*-(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)$|'  # month names
r'.*-week-?\d+$|'                     # week-1, week1
r'.*-v\d+$'                           # version numbers (report-v2)
```

**Warning Message:**
```
⚠️ PATTERN CHECK

You're creating "{name}" - this looks like it might repeat.

BUILDS are for one-time work (has a finish line)
SKILLS are for repeating work (same steps, new data)

If you'll create "{name}-february", "{name}-march"...
→ Consider making this a SKILL instead

Continue with Build? Just say "yes" or create a skill with "create skill".
```

**Trigger:** Write to `02-builds/XX-{name}/` where name matches pattern

---

## 8. TESTING PLAN

### Unit Tests

```python
# tests/test_micro_lessons.py

def test_build_created_trigger():
    """First build creation triggers lesson."""
    tool_name = "Write"
    tool_input = {"file_path": "02-builds/01-career-plan/01-planning/overview.md"}

    # Mock config with build_created: false
    lesson = check_micro_lesson(tool_name, tool_input, mock_config_path)

    assert lesson is not None
    assert "QUICK TIP: BUILDS" in lesson
    # Verify flag updated
    assert get_first_encounters(mock_config_path)['build_created'] == True


def test_build_created_no_repeat():
    """Second build creation does NOT trigger lesson."""
    tool_name = "Write"
    tool_input = {"file_path": "02-builds/02-another-build/01-planning/overview.md"}

    # Mock config with build_created: true
    lesson = check_micro_lesson(tool_name, tool_input, mock_config_already_seen)

    assert lesson is None


def test_skill_loaded_trigger():
    """First skill load triggers lesson."""
    tool_name = "Read"
    tool_input = {"file_path": "00-system/skills/builds/plan-build/SKILL.md"}

    lesson = check_micro_lesson(tool_name, tool_input, mock_config_path)

    assert lesson is not None
    assert "QUICK TIP: SKILLS" in lesson


def test_anti_pattern_detection():
    """Repeated naming pattern triggers warning."""
    tool_name = "Write"
    tool_input = {"file_path": "02-builds/01-report-january/overview.md"}

    warning = check_anti_pattern(tool_name, tool_input, mock_config_path)

    assert warning is not None
    assert "PATTERN CHECK" in warning
    assert "report-january" in warning


def test_anti_pattern_no_repeat():
    """Anti-pattern warning only shows once."""
    tool_name = "Write"
    tool_input = {"file_path": "02-builds/02-report-february/overview.md"}

    # Mock config with repeated_build_pattern: true
    warning = check_anti_pattern(tool_name, tool_input, mock_config_already_warned)

    assert warning is None
```

### Integration Tests

```python
# tests/test_hook_integration.py

def test_hook_json_output_format():
    """Verify hook outputs valid JSON with additionalContext."""
    input_data = {
        "hook_event_name": "PostToolUse",
        "tool_name": "Write",
        "tool_input": {"file_path": "02-builds/01-test/overview.md"},
        "session_id": "test-session"
    }

    result = run_hook_with_input(input_data)

    assert result['exit_code'] == 0
    output = json.loads(result['stdout'])
    assert 'hookSpecificOutput' in output
    assert output['hookSpecificOutput']['hookEventName'] == 'PostToolUse'
    assert 'additionalContext' in output['hookSpecificOutput']


def test_hook_graceful_error_handling():
    """Verify hook handles malformed input gracefully."""
    result = run_hook_with_input("not valid json")

    assert result['exit_code'] == 0  # Should not crash
```

### Manual Testing Checklist

- [ ] Fresh install: Create first build → See build lesson
- [ ] Same session: Create second build → No lesson
- [ ] Fresh install: Load first skill → See skill lesson
- [ ] Save to workspace for first time → See workspace lesson
- [ ] Update goals.md for first time → See memory lesson
- [ ] Use close-session for first time → See close session lesson
- [ ] Create "report-january" build → See anti-pattern warning
- [ ] Create "report-february" after warning → No second warning

---

## 9. MIGRATION PATH

### Phase 1: Core Implementation (This PR)

1. Update `post_tool_use.py` with micro-lesson logic
2. Update `user-config.yaml` template with new sections
3. Update existing user-config files (add missing sections)
4. Add orchestrator section on contextual teaching
5. Test all micro-lessons fire correctly

### Phase 2: Startup Flow Update (Future PR)

1. Modify SessionStart hook to ask "What do you want to work on?"
2. Remove setup menu as default (show on request)
3. Route directly to plan-build when user states intent
4. Capture goals THROUGH first build, not before

### Phase 3: Learning Skills Transformation (Future PR)

1. Rename `learn-builds` → `understand-builds` (optional deep-dive)
2. Rename `learn-skills` → `understand-skills` (optional deep-dive)
3. Trigger suggestion after user has 2+ builds: "Want to understand the full lifecycle?"
4. Remove from required onboarding, make optional

### Phase 4: Goal Capture Through Work (Future PR)

1. Add implicit goal extraction to plan-build workflow
2. When user shares context, extract: role, goal, focus area
3. Update goals.md from work conversation
4. Remove explicit goal-setting upfront

---

## APPENDIX A: Official Hook Documentation Reference

### PostToolUse Output Schema (from claude-hooks-docs.md)

```json
{
  "decision": "block" | undefined,
  "reason": "Explanation for decision",
  "hookSpecificOutput": {
    "hookEventName": "PostToolUse",
    "additionalContext": "Additional information for Claude"
  }
}
```

- `additionalContext` adds context for Claude to consider
- `decision: "block"` automatically prompts Claude with `reason`
- Exit code 0 required for JSON processing

### Key Insight

> `additionalContext` in PostToolUse works the same as in SessionStart - it gets injected into Claude's context as a `<system-reminder>`.

---

## APPENDIX B: Sascha-Dorian Session Quotes

Key quotes from the transcript that informed this redesign:

1. **On concept overload:**
   > *"du gibst mir jetzt hier ganz viele Konzepte... führe mich mal bitte Stück für Stück durchs Onboarding"*

2. **On explaining before doing:**
   > *"Ja, jetzt werden halt hier Skills erklärt, aber du weißt noch gar nicht, was Skills sind"*

3. **On time to value:**
   > *"Hast du jetzt schon Value bekommen? Ich würde sagen, nein."*
   > *"Time to first value ist extrem wichtig"*

4. **On contextual teaching:**
   > *"Du willst halt die Leute machen einfach was... nachdem es passiert ist, sagst du ihm, was gerade passiert ist"*

5. **On build terminology:**
   > *"Ich mache ein Bild. Hört sich irgendwie nicht so geil an."*

---

## APPENDIX C: Quick Reference

### Trigger → Lesson Map

| Tool | Path Pattern | Lesson |
|------|--------------|--------|
| Write | `02-builds/*/overview.md` | build_created |
| Write | `02-builds/*/01-planning/*` | build_created |
| Read | `*/SKILL.md` in skills folders | skill_loaded |
| Write | `04-workspace/*` | workspace_used |
| Write | `01-memory/goals.md` | memory_updated |
| Write | `01-memory/core-learnings.md` | memory_updated |
| Read | `close-session/SKILL.md` | close_session_used |

### State Flags

| Flag | Section | Purpose |
|------|---------|---------|
| `build_created` | first_encounters | Track first build lesson |
| `skill_loaded` | first_encounters | Track first skill lesson |
| `workspace_used` | first_encounters | Track first workspace lesson |
| `memory_updated` | first_encounters | Track first memory lesson |
| `close_session_used` | first_encounters | Track first close-session lesson |
| `repeated_build_pattern` | anti_patterns_warned | Track repeated naming warning |

---

**END OF DOCUMENT**

*This document contains the complete implementation plan for the Nexus "Teach Through Doing" onboarding redesign. All code, configurations, and rationale are preserved here for context continuity.*
