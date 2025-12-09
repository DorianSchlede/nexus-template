#!/usr/bin/env python3
"""
init-memory.py - Initialize the complete memory system (01-memory/) with templates

PURPOSE: Infrastructure script called BY Project 00 during onboarding
         Creates file structure + templates, which Project 00 then populates with user data

Usage:
    python 00-system/core/init-memory.py

Called by: Project 00 (Task 7.3)
Workflow:
  1. Project 00 runs this script → creates templates with [TODO] placeholders
  2. Project 00 populates files → replaces [TODO] with user's ACTUAL data
  3. Result: Fully personalized memory system (no placeholders)

This creates:
- 01-memory/goals.md (template with [TODO] placeholders)
- 01-memory/roadmap.md (template with [TODO] placeholders)
- 01-memory/user-config.yaml (template with empty language: "")
- 01-memory/core-learnings.md (empty template)
- 01-memory/memory-map.md (complete reference - no placeholders)
- 01-memory/session-reports/ (folder)

Note: Can also be used standalone for testing/development purposes
"""

import sys
from pathlib import Path
from datetime import datetime
import subprocess
import re

def detect_python_cmd() -> str:
    """Return the first working python command (python or python3)."""
    for cmd in ("python", "python3"):
        try:
            # Check if command exists and runs
            subprocess.run([cmd, "--version"], check=True, 
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return cmd
        except Exception:
            continue
    # Fallback to python if detection fails (though unlikely if script is running)
    return "python"

def update_orchestrator(base_path: Path, python_cmd: str):
    """
    Update orchestrator.md to use the detected python command.
    This ensures future startup commands work on this specific system.
    """
    orch_path = base_path / "00-system" / "core" / "orchestrator.md"
    if not orch_path.exists():
        return

    try:
        content = orch_path.read_text(encoding='utf-8')
        
        # Pattern to find the startup command block
        # We look for the specific line in the bash block
        pattern = r"(```bash\s*\n)(python)( 00-system/core/nexus-loader\.py --startup)"
        
        if re.search(pattern, content):
            # Replace 'python' with detected command
            new_content = re.sub(pattern, f"\\1{python_cmd}\\3", content)
            
            # Add a note about auto-configuration if not present
            if "<!-- Auto-configured -->" not in new_content:
                note = f"\n<!-- Auto-configured for this system: using {python_cmd} -->"
                new_content = re.sub(r"(### Step 1: Run Startup Script)", f"\\1{note}", new_content)
            
            orch_path.write_text(new_content, encoding='utf-8')
            print(f"[AUTO-FIX] Updated orchestrator.md to use '{python_cmd}'")
    except Exception as e:
        print(f"[WARNING] Could not auto-update orchestrator.md: {e}")


GOALS_TEMPLATE = """# Your Goals

> **Purpose**: Define what you want to achieve (for AI context)
>
> **Updated**: Set during onboarding, revised as needed

---

## Current Role

[TODO: What do you do currently? Student, freelancer, founder, etc.]

---

## Short-Term Goal (3 months)

[TODO: What do you want to achieve in the next 3 months?]

**Why This Matters**:
[TODO: Why is this important to you?]

**Success Metrics**:
- [ ] Metric 1
- [ ] Metric 2
- [ ] Metric 3

---

## Long-Term Vision (1-3 years)

[TODO: Where do you want to be in 1-3 years?]

---

## Work Style & Preferences

**Best Working Hours**: [TODO]
**Typical Session Length**: [TODO: 30min, 2hrs, etc.]
**Focus Areas**: [TODO: What types of work are you doing?]

---

**Last Updated**: {created_date}
"""

ROADMAP_TEMPLATE = """# Your Roadmap

> **Purpose**: Break down goals into milestones (for strategic planning)
>
> **Updated**: Created in onboarding, refined as work evolves

---

## Goal Breakdown

**Main Goal**: [TODO: From goals.md]

---

## Milestones

### Milestone 1: [Name]
**Target**: [TODO: Date or timeframe]
**Status**: NOT_STARTED
**Why**: [TODO: Why this milestone matters]

**Key Activities**:
- [ ] Activity 1
- [ ] Activity 2

---

### Milestone 2: [Name]
**Target**: [TODO]
**Status**: NOT_STARTED
**Why**: [TODO]

**Key Activities**:
- [ ] Activity 1
- [ ] Activity 2

---

### Milestone 3: [Name]
**Target**: [TODO]
**Status**: NOT_STARTED
**Why**: [TODO]

**Key Activities**:
- [ ] Activity 1
- [ ] Activity 2

---

## Timeline View

```
Month 1-2: Milestone 1
Month 3-4: Milestone 2
Month 5-6: Milestone 3
```

---

## Next Steps

[TODO: What's the immediate next action?]

---

**Last Updated**: {created_date}
"""

CORE_LEARNINGS_TEMPLATE = """# Core Learnings

> **Purpose**: Capture insights, patterns, and best practices (accumulates over time)
>
> **Updated**: Automatically by close-session skill after each session

---

## What Works Well

<!-- Session reports automatically add to this section -->

---

## What to Avoid

<!-- Mistakes and challenges automatically captured here -->

---

## Best Practices

<!-- Successful patterns extracted here -->

---

## Insights

<!-- Strategic insights and realizations -->

---

**Last Updated**: {created_date}
"""

MEMORY_MAP_TEMPLATE = """# Memory Map

<!-- AI CONTEXT FILE -->
<!-- Purpose: Help AI navigate the memory system -->
<!-- Updated by: System (static framework documentation) -->

> **Purpose**: Help AI navigate the memory system
>
> **Audience**: AI agent (loaded every session via --startup)
>
> **Maintenance**: Static system documentation

---

## Memory System Overview

The `01-memory/` folder contains context that persists across all sessions:

### Core Files (Always Loaded)

**goals.md** - What you want to achieve
- Current role and work context
- Short-term goal (3 months)
- Long-term vision (1-3 years)
- Success metrics

**roadmap.md** - How you'll get there
- Goal breakdown into milestones
- Timeline and sequencing
- Key activities per milestone

**core-learnings.md** - What you've learned
- What works well (successes)
- What to avoid (mistakes)
- Best practices (patterns)
- Insights (strategic realizations)

**memory-map.md** - This file
- System navigation for AI
- Structure explanation

**user-config.yaml** - Your preferences
- Language preference
- Timezone
- Date format

---

## Session Reports (Historical)

**session-reports/** - Generated after each session
- Dated session summaries
- Progress tracking
- Key decisions and outcomes
- Never loaded automatically (only on request)

---

## When AI Loads Memory Files

**Every Session** (via --startup):
- goals.md
- memory-map.md
- user-config.yaml

**Strategic Discussion**:
- roadmap.md (when talking about milestones, timeline, planning)

**Pattern Recognition**:
- core-learnings.md (when similar situations arise)

**Historical Context**:
- session-reports/ (only when user explicitly asks about past sessions)

---

## How Memory Evolves

**Onboarding** (Projects 00-03):
- goals.md → Created in Project 00
- roadmap.md → Created in Project 00
- user-config.yaml → Created in Project 00
- core-learnings.md → Starts empty, grows over time

**Operational** (After onboarding):
- close-session updates core-learnings.md automatically
- close-session creates session reports
- User updates goals.md and roadmap.md as needed

---

**This map helps the AI understand your memory system structure.**
"""

USER_CONFIG_TEMPLATE = """---
# User Configuration
# Purpose: Store persistent user preferences (loaded every session)
# Updated: Set during onboarding, modified anytime

user_preferences:
  language: ""  # Set during Project 00 onboarding (e.g., "English", "Deutsch", "Español")
  timezone: ""  # Optional (e.g., "Europe/Berlin", "America/New_York")
  date_format: "YYYY-MM-DD"  # Optional date format preference
  
  system:
    python_cmd: "{python_cmd}"  # Auto-detected system command

created: {created_date}
updated: {created_date}
---

# Instructions for AI

When this file is loaded (every session via --startup):
1. Respect the language preference throughout ALL interactions
2. Use timezone for accurate session timestamps
3. Format dates according to user preference

If language is not set (empty string):
- Default to English
- Prompt user to set preference during next onboarding step
"""

SESSION_REPORTS_README = """# Session Reports

This folder contains dated session summaries generated by the `close-session` skill.

**Format**: `YYYY-MM-DD-session-report.md`

**Content**:
- Session date and duration
- What was accomplished
- Projects worked on
- Key decisions made
- Learnings captured
- Next session priorities

**AI Loading**:
- Never loaded automatically
- Only loaded when user explicitly requests historical context
- Example: "What did I work on last week?"

**Maintenance**:
- Created automatically by close-session
- Never delete (historical record)
- Reference for progress tracking
"""


def create_memory_system(
    base_path: str = ".",
    user_language: str = "",
    user_role: str = "",
    short_term_goal: str = "",
    long_term_goal: str = "",
    python_cmd: str = "python"
):
    """
    Create complete memory system structure with personalized content.

    Args:
        base_path: Base path to Nexus-v3
        user_language: User's preferred language (e.g., "English", "Deutsch")
        user_role: User's current role (e.g., "Student", "Freelancer", "Founder")
        short_term_goal: User's 3-month goal
        long_term_goal: User's 1-3 year vision

    Returns:
        Path to created memory folder, or None if error
    """
    base = Path(base_path)
    memory_path = base / "01-memory"

    # Check if already exists (ignoring .gitkeep)
    if memory_path.exists():
        existing_files = [f for f in memory_path.iterdir() if f.name != ".gitkeep"]
        if existing_files:
            print(f"[WARNING] Memory system already exists: {memory_path}")
            print(f"[INFO] Existing files will not be overwritten")
            return None

    # Create folder structure
    try:
        memory_path.mkdir(parents=True, exist_ok=True)
        (memory_path / "session-reports").mkdir(exist_ok=True)
        print(f"[OK] Created 01-memory/")
        print(f"[OK] Created session-reports/ folder")
    except Exception as e:
        print(f"[ERROR] Failed to create folders: {e}")
        return None

    # Generate content
    today = datetime.now().strftime('%Y-%m-%d')

    # Populate templates with user data or use placeholders
    role_text = user_role if user_role else "[TODO: What do you do currently? Student, freelancer, founder, etc.]"
    short_goal_text = short_term_goal if short_term_goal else "[TODO: What do you want to achieve in the next 3 months?]"
    long_goal_text = long_term_goal if long_term_goal else "[TODO: Where do you want to be in 1-3 years?]"
    language_text = user_language if user_language else ""

    # Customize goals template
    goals_content = GOALS_TEMPLATE.format(created_date=today)
    if user_role:
        goals_content = goals_content.replace(
            "[TODO: What do you do currently? Student, freelancer, founder, etc.]",
            role_text
        )
    if short_term_goal:
        goals_content = goals_content.replace(
            "[TODO: What do you want to achieve in the next 3 months?]",
            short_goal_text
        )
    if long_term_goal:
        goals_content = goals_content.replace(
            "[TODO: Where do you want to be in 1-3 years?]",
            long_goal_text
        )

    # Customize user-config template
    config_content = USER_CONFIG_TEMPLATE.format(created_date=today, python_cmd=python_cmd)
    if user_language:
        config_content = config_content.replace(
            'language: ""',
            f'language: "{language_text}"'
        )

    # Define files
    files = {
        'goals.md': goals_content,
        'roadmap.md': ROADMAP_TEMPLATE.format(created_date=today),
        'core-learnings.md': CORE_LEARNINGS_TEMPLATE.format(created_date=today),
        'memory-map.md': MEMORY_MAP_TEMPLATE,
        'user-config.yaml': config_content,
        'session-reports/README.md': SESSION_REPORTS_README
    }

    # Write files
    for file_path, content in files.items():
        full_path = memory_path / file_path

        # Skip if file already exists (don't overwrite user data)
        if full_path.exists():
            print(f"[SKIP] {file_path} already exists")
            continue

        try:
            full_path.write_text(content, encoding='utf-8')
            print(f"[OK] Created {file_path}")
        except Exception as e:
            print(f"[ERROR] Failed to create {file_path}: {e}")
            return None

    print(f"\n[SUCCESS] Memory system initialized successfully!")
    print(f"\nCreated:")
    print(f"  - 01-memory/goals.md (template)")
    print(f"  - 01-memory/roadmap.md (template)")
    print(f"  - 01-memory/core-learnings.md (template)")
    print(f"  - 01-memory/memory-map.md (complete reference)")
    print(f"  - 01-memory/user-config.yaml (template)")
    print(f"  - 01-memory/session-reports/ (folder for future reports)")

    print(f"\nNext steps:")
    print(f"1. Edit 01-memory/goals.md during Project 00 onboarding")
    print(f"2. Set language preference in user-config.yaml")
    print(f"3. System will load these files automatically with --startup")

    return memory_path


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Initialize Nexus-v3 memory system with personalized content"
    )
    parser.add_argument(
        '--base-path',
        default='.',
        help='Base path to Nexus-v3 (default: current directory)'
    )
    parser.add_argument(
        '--language',
        default='',
        help='User preferred language (e.g., "English", "Deutsch", "Español")'
    )
    parser.add_argument(
        '--role',
        default='',
        help='User current role (e.g., "Student", "Freelancer", "Founder")'
    )
    parser.add_argument(
        '--short-goal',
        default='',
        help='User short-term goal (3 months)'
    )
    parser.add_argument(
        '--long-goal',
        default='',
        help='User long-term vision (1-3 years)'
    )

    args = parser.parse_args()

    print("Initializing memory system...")
    
    # Detect Python command
    py_cmd = detect_python_cmd()
    print(f"Detected system Python command: {py_cmd}")

    if args.language or args.role or args.short_goal or args.long_goal:
        print("Personalizing with user data...")
    print()

    result = create_memory_system(
        base_path=args.base_path,
        user_language=args.language,
        user_role=args.role,
        short_term_goal=args.short_goal,
        long_term_goal=args.long_goal,
        python_cmd=py_cmd
    )
    
    # Auto-fix orchestrator
    if result:
        update_orchestrator(Path(args.base_path), py_cmd)

    if result:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
