#!/usr/bin/env python3
"""
nexus-loader.py - Context loader and directive executor for Nexus

Usage:
    python nexus-loader.py --startup           # Load session context + return instructions
    python nexus-loader.py --resume            # Resume from context summary
    python nexus-loader.py --project ID        # Load specific project
    python nexus-loader.py --skill name        # Load specific skill
    python nexus-loader.py --list-projects     # Scan project metadata
    python nexus-loader.py --list-skills       # Scan skill metadata
    python nexus-loader.py --show-tokens       # Display token costs
    python nexus-loader.py --check-update      # Check if upstream updates available
    python nexus-loader.py --sync              # Sync system files from upstream
"""

import os
import re
import sys
import yaml
import json
import shutil
import argparse
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple

# Token counting constants
CHARS_PER_TOKEN = 4  # Rough estimate: 1 token ≈ 4 characters
CONTEXT_WINDOW = 200000  # Claude's context window
METADATA_BUDGET_WARNING = 7000  # Warn if metadata >7K tokens (3.5% of window)
BASH_OUTPUT_LIMIT = 30000  # Claude Code bash output truncation limit

# MANDATORY NAVIGATION MAPS (Always loaded at startup)
# These provide core system navigation and context
MANDATORY_MAPS = [
    "00-system/system-map.md",              # System structure and navigation hub
]

# =============================================================================
# UPSTREAM SYNC CONFIGURATION
# =============================================================================

# Default upstream repository URL (users can override in user-config.yaml)
DEFAULT_UPSTREAM_URL = "https://github.com/DorianSchlede/nexus-template.git"

# Paths to sync from upstream (system files only)
SYNC_PATHS = [
    "00-system/",
    "CLAUDE.md",
    "README.md",
]

# Paths to NEVER touch (user's personal data)
PROTECTED_PATHS = [
    "01-memory/",
    "02-projects/",
    "03-skills/",
    "04-workspace/",
    ".env",
    ".claude/",
    ".sync-backup/",
]

# =============================================================================
# SMART DEFAULT TEMPLATES (B5: Optional Onboarding)
# These templates are auto-created on first run so system works immediately
# =============================================================================

SMART_DEFAULT_GOALS = """---
smart_default: true
---
# Your Goals

> **Purpose**: Define what you want to achieve (for AI context)
>
> **Updated**: Set via 'setup goals' skill, revised as needed

---

## Current Role

[TODO: Say 'setup goals' to personalize]

---

## Short-Term Goal (3 months)

[TODO: Say 'setup goals' to personalize]

**Why This Matters**:
[TODO: Why is this important to you?]

**Success Metrics**:
- [ ] Metric 1
- [ ] Metric 2
- [ ] Metric 3

---

## Long-Term Vision (1-3 years)

[TODO: Say 'setup goals' to personalize]

---

## Work Style & Preferences

**Best Working Hours**: [TODO]
**Typical Session Length**: [TODO: 30min, 2hrs, etc.]
**Focus Areas**: [TODO: What types of work are you doing?]

---

**Last Updated**: [TODO: Updated after 'setup goals']
"""

SMART_DEFAULT_CONFIG = """---
# User Configuration
# Purpose: Store persistent user preferences (loaded every session)
# Updated: Set during onboarding, modified anytime

smart_default: true

user_preferences:
  language: ""
  timezone: ""
  date_format: "YYYY-MM-DD"

  system:
    python_cmd: "python"

onboarding:
  status: "skipped"
  current_session: 0
  last_completed: null
  sessions_completed: []

learning_tracker:
  session_count: 0
  completed:
    setup_goals: false
    setup_workspace: false
    learn_integrations: false
    learn_projects: false
    learn_skills: false
    learn_nexus: false
  dismissed: []
  last_suggested: null
  suggestion_preference: "normal"

created: null
updated: null
---

# Instructions for AI

When this file is loaded (every session via --startup):
1. Respect the language preference throughout ALL interactions
2. Use timezone for accurate session timestamps
3. Format dates according to user preference
4. Check learning_tracker for onboarding skill suggestions

If smart_default is true:
- System is using default templates (not personalized)
- Suggest onboarding skills when contextually appropriate
- User can work immediately without setup

If language is not set (empty string):
- Default to English
- Prompt user to set preference during setup-goals skill
"""

SMART_DEFAULT_LEARNINGS = """# Core Learnings

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

**Last Updated**: Not yet updated
"""

SMART_DEFAULT_MEMORY_MAP = """# Memory Map

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

**Quick Start** (Smart Defaults):
- Template files auto-created on first run
- User can work immediately
- Personalize anytime with "setup goals" skill

**Personalized** (After setup-goals skill):
- goals.md → Populated with user's actual goals
- roadmap.md → Created with milestones
- user-config.yaml → Language and preferences set
- core-learnings.md → Grows over time via close-session

---

**This map helps the AI understand your memory system structure.**
"""


# =============================================================================
# TEMPLATE DETECTION FUNCTIONS (B5: Smart Default Detection)
# =============================================================================

def is_template_file(file_path: str) -> bool:
    """
    Check if a file is a smart default template (not yet personalized).

    Detection methods:
    1. Check for `smart_default: true` in YAML frontmatter
    2. Fallback: Check for `[TODO: Set in onboarding` pattern

    Args:
        file_path: Path to file to check

    Returns:
        True if file is a template, False if personalized or doesn't exist
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Method 1: Check YAML frontmatter for smart_default flag
        match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
        if match:
            try:
                yaml_content = yaml.safe_load(match.group(1))
                if yaml_content and yaml_content.get('smart_default') is True:
                    return True
            except yaml.YAMLError:
                pass

        # Method 2: Fallback - check for TODO placeholder pattern
        if '[TODO: Set in onboarding' in content:
            return True

        return False

    except Exception:
        return False


def are_defaults_personalized(base_path: str) -> bool:
    """
    Check if smart defaults have been personalized by the user.

    Args:
        base_path: Root path to Nexus installation

    Returns:
        True if goals.md exists AND is NOT a template (personalized)
        False if goals.md doesn't exist OR is still a template
    """
    goals_path = Path(base_path) / "01-memory" / "goals.md"

    if not goals_path.exists():
        return False

    return not is_template_file(str(goals_path))


def create_smart_defaults(base_path: str) -> Dict[str, Any]:
    """
    Create smart default template files for immediate system operation.

    This enables users to start working immediately without onboarding.
    Files are created with `smart_default: true` flag for detection.

    Args:
        base_path: Root path to Nexus installation

    Returns:
        Dict with 'created' and 'skipped' lists of file names
    """
    base = Path(base_path)
    memory_path = base / "01-memory"

    result = {
        'created': [],
        'skipped': [],
        'errors': []
    }

    # Ensure directories exist
    try:
        memory_path.mkdir(parents=True, exist_ok=True)
        (memory_path / "session-reports").mkdir(exist_ok=True)
    except Exception as e:
        result['errors'].append(f"Failed to create directories: {e}")
        return result

    # Define template files to create
    templates = {
        'goals.md': SMART_DEFAULT_GOALS,
        'user-config.yaml': SMART_DEFAULT_CONFIG,
        'memory-map.md': SMART_DEFAULT_MEMORY_MAP,
        'core-learnings.md': SMART_DEFAULT_LEARNINGS,
    }

    # Create each file (skip if exists)
    for filename, content in templates.items():
        file_path = memory_path / filename

        if file_path.exists():
            result['skipped'].append(filename)
            continue

        try:
            file_path.write_text(content, encoding='utf-8')
            result['created'].append(filename)
        except Exception as e:
            result['errors'].append(f"Failed to create {filename}: {e}")

    return result


def extract_yaml_frontmatter(file_path: str) -> Optional[Dict[str, Any]]:
    """Extract YAML frontmatter from markdown file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Match YAML frontmatter: ---\n[yaml]\n---
        match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
        if not match:
            return None

        yaml_content = match.group(1)
        metadata = yaml.safe_load(yaml_content)

        if metadata:
            # Convert any date objects to ISO format strings for JSON serialization
            for key, value in metadata.items():
                if hasattr(value, 'isoformat'):  # datetime, date objects
                    metadata[key] = value.isoformat()

            metadata['_file_path'] = str(file_path)
            metadata['_file_name'] = Path(file_path).name

        return metadata

    except Exception as e:
        return {'error': str(e), '_file_path': str(file_path)}


def load_file_content(file_path: str) -> str:
    """Load full file content."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"ERROR: {e}"


def estimate_tokens(text: str) -> int:
    """Estimate token count from text (rough approximation)."""
    if not text:
        return 0
    return len(text) // CHARS_PER_TOKEN


def calculate_bundle_tokens(result: Dict[str, Any]) -> Dict[str, int]:
    """Calculate token costs for loaded bundle."""
    token_counts = {
        'total': 0,
        'files': 0,
        'metadata': 0,
        'by_file': {}
    }

    # Count tokens in files
    for file_key, file_data in result.get('files', {}).items():
        if isinstance(file_data, dict) and 'content' in file_data:
            tokens = estimate_tokens(file_data['content'])
            token_counts['files'] += tokens
            token_counts['by_file'][file_key] = tokens

    # Count tokens in metadata
    metadata = result.get('metadata', {})
    if metadata:
        metadata_str = json.dumps(metadata)
        token_counts['metadata'] = estimate_tokens(metadata_str)

    token_counts['total'] = token_counts['files'] + token_counts['metadata']

    # Calculate percentage of context window
    token_counts['percentage'] = round((token_counts['total'] / CONTEXT_WINDOW) * 100, 2)

    return token_counts


def count_checkboxes(steps_file: Path) -> tuple:
    """
    Count checkboxes in steps.md file.
    Returns: (total, completed, uncompleted)
    """
    if not steps_file.exists():
        return (0, 0, 0)

    try:
        content = steps_file.read_text(encoding='utf-8')

        # Match checkbox patterns: - [ ] or - [x] or - [X]
        checked = len(re.findall(r'^\s*-\s*\[x\]', content, re.MULTILINE | re.IGNORECASE))
        unchecked = len(re.findall(r'^\s*-\s*\[\s\]', content, re.MULTILINE))

        total = checked + unchecked
        return (total, checked, unchecked)
    except Exception:
        return (0, 0, 0)


def scan_projects(base_path: str = ".", minimal: bool = True) -> List[Dict[str, Any]]:
    """Scan all projects and extract YAML metadata + count actual tasks.
    
    Args:
        base_path: Root path to scan from
        minimal: If True, return only essential fields for routing/display (default)
                 If False, return all YAML fields
    """
    projects = []
    projects_dir = Path(base_path) / "02-projects"

    if not projects_dir.exists():
        return []

    # Look for all overview.md files in root and onboarding folder
    patterns = [
        "*/01-planning/overview.md",
        "00-onboarding/*/01-planning/overview.md"
    ]

    for pattern in patterns:
        for overview_file in projects_dir.glob(pattern):
            metadata = extract_yaml_frontmatter(str(overview_file))
            if metadata and 'error' not in metadata:
                # Count actual checkboxes from steps.md
                project_dir = overview_file.parent.parent
                steps_file = project_dir / "01-planning" / "steps.md"

                total, completed, uncompleted = count_checkboxes(steps_file)

                # OVERRIDE YAML metadata with actual counts from steps.md
                # This ensures single source of truth: steps.md checkboxes
                metadata['tasks_total'] = total
                metadata['tasks_completed'] = completed
                metadata['progress'] = round(completed / total, 3) if total > 0 else 0.0

                # Add current task (first unchecked task)
                if steps_file.exists() and uncompleted > 0:
                    try:
                        content = steps_file.read_text(encoding='utf-8')
                        # Find first unchecked task
                        match = re.search(r'^\s*-\s*\[\s\]\s*(.+)$', content, re.MULTILINE)
                        if match:
                            metadata['current_task'] = match.group(1).strip()
                    except Exception:
                        pass

                # PROGRESSIVE DISCLOSURE: Return minimal fields for efficiency
                if minimal:
                    # Keep only essential fields for routing and menu display
                    description = metadata.get('description', '')
                    
                    metadata = {
                        'id': metadata.get('id'),
                        'name': metadata.get('name'),
                        'description': description,
                        'status': metadata.get('status'),
                        'onboarding': metadata.get('onboarding', False),
                        'created': metadata.get('created'),
                        'updated': metadata.get('updated'),
                        'progress': metadata['progress'],
                        'tasks_total': metadata['tasks_total'],
                        'tasks_completed': metadata['tasks_completed'],
                        'current_task': metadata.get('current_task'),
                        '_file_path': metadata.get('_file_path'),
                        '_file_name': metadata.get('_file_name')
                    }

                projects.append(metadata)

    return projects


def detect_configured_integrations(base_path: str = ".") -> List[Dict[str, Any]]:
    """
    Detect which integrations are actually configured (have credentials).

    An integration is considered "active" if:
    1. It has a master skill folder (00-system/skills/{integration}/{integration}-master/)
    2. The required environment variable is set in .env

    Returns:
        List of dicts with integration name, available skills, and active status
    """
    integrations = []
    skills_dir = Path(base_path) / "00-system" / "skills"

    if not skills_dir.exists():
        return []

    # Map integration names to their required env vars
    INTEGRATION_ENV_VARS = {
        'airtable': 'AIRTABLE_API_KEY',
        'notion': 'NOTION_API_KEY',
        'beam': 'BEAM_API_KEY',
        'hubspot': 'HUBSPOT_ACCESS_TOKEN',
    }

    # Load .env file if exists
    env_vars = {}
    env_file = Path(base_path) / ".env"
    if env_file.exists():
        try:
            with open(env_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, _, value = line.partition('=')
                        # Remove quotes if present
                        value = value.strip().strip('"').strip("'")
                        if value:  # Only count if value is non-empty
                            env_vars[key.strip()] = value
        except Exception:
            pass

    # Known integration patterns (folders that represent external service integrations)
    # These follow the master/connect/specialized pattern
    for category_dir in skills_dir.iterdir():
        if not category_dir.is_dir():
            continue

        category_name = category_dir.name

        # Check if this category has a master skill (indicates it's an integration)
        master_skill = category_dir / f"{category_name}-master"
        if master_skill.exists() and (master_skill / "SKILL.md").exists():
            # Check if credentials are configured
            required_env = INTEGRATION_ENV_VARS.get(category_name.lower())
            is_active = required_env and required_env in env_vars

            integration = {
                'name': category_name,
                'slug': category_name.lower(),
                'skills': [],
                'active': is_active,
                'required_env': required_env,
            }

            # List all skills in this integration
            for skill_dir in category_dir.iterdir():
                if skill_dir.is_dir() and (skill_dir / "SKILL.md").exists():
                    integration['skills'].append(skill_dir.name)

            integrations.append(integration)

    return integrations


def scan_skills(base_path: str = ".", minimal: bool = True) -> List[Dict[str, Any]]:
    """Scan all skills and extract YAML metadata.
    
    Args:
        base_path: Root path to scan from
        minimal: If True, return only essential fields for routing/display (default)
                 If False, return all YAML fields
    """
    skills = []

    # Try both 03-skills/ (user skills) and 00-system/skills/ (system skills)
    skills_dirs = [
        Path(base_path) / "03-skills",
        Path(base_path) / "00-system" / "skills"
    ]

    for skills_dir in skills_dirs:
        if not skills_dir.exists():
            continue

        # Look for all SKILL.md files (recursive to support category subfolders)
        for skill_file in skills_dir.glob("**/SKILL.md"):
            metadata = extract_yaml_frontmatter(str(skill_file))
            if metadata and 'error' not in metadata:
                
                # PROGRESSIVE DISCLOSURE: Return minimal fields for efficiency
                if minimal:
                    description = metadata.get('description', '')
                    
                    metadata = {
                        'name': metadata.get('name'),
                        'description': description,
                        '_file_path': metadata.get('_file_path'),
                        '_file_name': metadata.get('_file_name')
                    }
                
                skills.append(metadata)

    return skills


def embed_file_contents(file_paths: List[str]) -> Dict[str, str]:
    """
    Read all files and return their contents keyed by filename.

    Args:
        file_paths: List of absolute file paths to read

    Returns:
        Dictionary with filename as key and file content as value
    """
    contents = {}
    for file_path in file_paths:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                filename = Path(file_path).name
                contents[filename] = f.read()
        except Exception as e:
            filename = Path(file_path).name
            contents[filename] = f"ERROR reading file: {e}"
    return contents


def load_metadata(base_path: str = ".") -> Dict[str, Any]:
    """
    Load ONLY project and skill metadata (no memory content).

    Use this as a second call after --startup to get full metadata
    when the combined output would exceed bash limits (~30K chars).

    Args:
        base_path: Root path to Nexus installation

    Returns:
        - projects: Full project metadata list
        - skills: Full skill metadata list
        - stats: Counts and summary
    """
    result = {
        'loaded_at': datetime.now().isoformat(),
        'bundle': 'metadata',
        'projects': scan_projects(base_path, minimal=True),
        'skills': scan_skills(base_path, minimal=True),
    }

    result['stats'] = {
        'total_projects': len(result['projects']),
        'total_skills': len(result['skills']),
        'active_projects': len([p for p in result['projects'] if p.get('status') == 'IN_PROGRESS']),
    }

    return result


def load_startup(base_path: str = ".", include_metadata: bool = True, resume_mode: bool = False, check_updates: bool = True) -> Dict[str, Any]:
    """
    Load startup context and determine complete execution plan.

    This function is the MASTER CONTROLLER for Nexus startup.
    It analyzes system state and returns EXACTLY what the AI should do.
    Memory file contents are embedded directly - no separate Read calls needed.

    Args:
        base_path: Root path to Nexus installation
        include_metadata: If True, include full project/skill metadata (default)
                         If False, return only core + instructions (use --metadata separately)
        resume_mode: If True, we're resuming after a context summary (skip menu display)
        check_updates: If True, check for upstream updates (default). Set False for faster startup.

    Returns:
    - system_state: Classification of current state
    - memory_content: Dict of file contents (keyed by filename)
    - instructions: Complete execution plan with action, message, steps
    - metadata: All projects and skills (if include_metadata=True)
    - stats: System statistics (includes update_available if check_updates=True)
    """
    base = Path(base_path)

    result = {
        'loaded_at': datetime.now().isoformat(),
        'bundle': 'startup',
        'system_state': None,      # State classification
        'memory_content': {},      # Embedded file contents
        'instructions': None,      # Complete execution plan
        'metadata': {},
        'stats': {}
    }

    # Track files to embed
    files_to_embed = []

    # Step 1: ALWAYS load mandatory navigation maps first (if they exist)
    # These provide core system structure and context for every session
    for map_path in MANDATORY_MAPS:
        full_path = base / map_path
        if full_path.exists():
            files_to_embed.append(str(full_path))

    # Step 2: Load additional optional context files (if they exist)
    optional_files = {
        'memory_map': base / "01-memory" / "memory-map.md",
        'goals': base / "01-memory" / "goals.md",
        'user_config': base / "01-memory" / "user-config.yaml",
    }

    files_exist = {
        key: path.exists() for key, path in optional_files.items()
    }

    # Add optional files to embed list
    for key, path in optional_files.items():
        if files_exist[key]:
            files_to_embed.append(str(path))

    # Step 3: Scan project and skill metadata (if requested)
    if include_metadata:
        projects = scan_projects(base_path)
        result['metadata']['projects'] = projects

        skills = scan_skills(base_path)
        result['metadata']['skills'] = skills
    else:
        # Minimal scan for state detection only
        projects = scan_projects(base_path)
        skills = []
        result['metadata'] = {'note': 'Use --metadata for full project/skill data'}

    # Step 4: Intelligent state detection (NO DIRECTIVES!)
    # The script analyzes file existence and project metadata to decide what to do

    # STATE 1: First Time Setup (no goals.md) - Create smart defaults
    if not files_exist['goals']:
        # B5: Create smart defaults so system works immediately
        defaults_result = create_smart_defaults(base_path)
        result['smart_defaults_created'] = defaults_result

        # Re-check files after creation
        for key, path in optional_files.items():
            if path.exists() and str(path) not in files_to_embed:
                files_to_embed.append(str(path))
                files_exist[key] = True

        # NEW STATE: first_time_with_defaults - Show menu, suggest onboarding
        result['system_state'] = 'first_time_with_defaults'
        result['instructions'] = {
            'action': 'display_menu',
            'execution_mode': 'interactive',
            'suggest_onboarding': True,
            'message': 'Welcome to Nexus! Quick Start Mode active.',
            'reason': 'Smart defaults created - system ready for immediate use',
            'workflow': [
                'Display modern Nexus header',
                'Show Quick Start Mode notice',
                'Display empty projects section',
                'Show available skills',
                'Suggest: "setup goals" to personalize (optional)',
                'Wait for user input - can work immediately'
            ]
        }

    # STATE 2: Goals exist but are still templates (smart defaults)
    elif is_template_file(str(optional_files['goals'])):
        result['system_state'] = 'first_time_with_defaults'
        result['instructions'] = {
            'action': 'display_menu',
            'execution_mode': 'interactive',
            'suggest_onboarding': True,
            'message': 'Welcome back! Quick Start Mode still active.',
            'reason': 'Goals not yet personalized - smart defaults in use',
            'workflow': [
                'Display modern Nexus header',
                'Show Quick Start Mode notice',
                'Display any projects created',
                'Show available skills',
                'Suggest: "setup goals" to personalize (optional)',
                'Wait for user input'
            ]
        }

    # STATE 3: Goals exist and personalized - check for active projects
    # Note: Onboarding is now skill-based (via learning_tracker in user-config.yaml)
    # and optional - no forced project-based onboarding
    else:
        active_projects = [p for p in projects if p.get('status') == 'IN_PROGRESS']

        # STATE 3A: Has active projects
        if active_projects:
            # Find most recently updated
            most_recent = active_projects[0]  # Assume first is most recent from scan

            result['system_state'] = 'operational_with_active_projects'
            result['instructions'] = {
                'action': 'display_menu',
                'execution_mode': 'interactive',
                'message': f"Welcome back! You have {len(active_projects)} active project(s)",
                'reason': f'Active projects detected: {most_recent["id"]}',
                'workflow': [
                    'Display Nexus banner',
                    'Show user goals (from goals.md)',
                    f'Highlight {len(active_projects)} active projects',
                    'Show available skills',
                    'Wait for user input (can resume projects or start new work)'
                ]
            }

        # STATE 3B: No active projects (normal operational state)
        else:
            result['system_state'] = 'operational'
            result['instructions'] = {
                'action': 'display_menu',
                'execution_mode': 'interactive',
                'message': 'System ready - what would you like to work on?',
                'reason': 'No active projects',
                'workflow': [
                    'Display Nexus banner',
                    'Show user goals (from goals.md)',
                    'List completed projects',
                    'Show available skills',
                    'Suggest: "create project" or use skills',
                    'Wait for user input'
                ]
            }

    # Step 5: Override instructions for resume mode
    # When resuming from a context summary, don't show menu - continue working
    if resume_mode:
        result['bundle'] = 'resume'

        # Find active projects to suggest continuation
        active_projects = [p for p in projects if p.get('status') == 'IN_PROGRESS']

        if active_projects:
            # Suggest continuing the most recent active project
            most_recent = active_projects[0]
            result['instructions'] = {
                'action': 'continue_working',
                'execution_mode': 'immediate',
                'suggest_project': most_recent['id'],
                'message': f"Context restored. Continue where you left off.",
                'reason': 'Resumed from context summary - skip menu, continue work',
                'workflow': [
                    'Context has been restored from summary',
                    'DO NOT display menu - continue working on previous task',
                    f"Active project available: {most_recent['name']} ({most_recent.get('progress', 0)*100:.0f}% complete)",
                    'Continue from previous conversation context',
                    'If user gives new instructions, follow them'
                ]
            }
        else:
            result['instructions'] = {
                'action': 'continue_working',
                'execution_mode': 'immediate',
                'message': 'Context restored. Ready to continue.',
                'reason': 'Resumed from context summary - skip menu, await instructions',
                'workflow': [
                    'Context has been restored from summary',
                    'DO NOT display menu',
                    'Continue from previous conversation context',
                    'Follow user instructions from summary'
                ]
            }

    # Step 6: Embed memory content (always - no separate Read calls needed)
    if files_to_embed:
        result['memory_content'] = embed_file_contents(files_to_embed)

    # Step 7: Generate stats with empty state flags for menu display
    mandatory_maps_found = sum(1 for map_path in MANDATORY_MAPS if (base / map_path).exists())

    # Count user skills (from 03-skills/) vs system skills
    user_skills = [s for s in skills if '03-skills' in s.get('_file_path', '')]

    # Check if goals are personalized (not smart default)
    goals_personalized = files_exist['goals'] and not is_template_file(str(optional_files['goals']))

    # Check if workspace is configured (workspace-map.md exists and has content beyond template)
    workspace_map_path = base / "04-workspace" / "workspace-map.md"
    workspace_configured = workspace_map_path.exists() and not is_template_file(str(workspace_map_path))

    # Extract learning_tracker.completed from user-config.yaml
    learning_completed = {
        'setup_goals': False,
        'setup_workspace': False,
        'learn_integrations': False,
        'learn_projects': False,
        'learn_skills': False,
        'learn_nexus': False,
    }
    if files_exist['user_config']:
        try:
            with open(optional_files['user_config'], 'r', encoding='utf-8') as f:
                config_content = f.read()
                # Parse YAML frontmatter
                if config_content.startswith('---'):
                    parts = config_content.split('---', 2)
                    if len(parts) >= 2:
                        import yaml
                        config_data = yaml.safe_load(parts[1])
                        if config_data and 'learning_tracker' in config_data:
                            tracker = config_data['learning_tracker']
                            if 'completed' in tracker and isinstance(tracker['completed'], dict):
                                learning_completed.update(tracker['completed'])
        except Exception:
            pass  # Keep defaults on error

    # Build pending_onboarding list - ONLY incomplete onboarding skills
    # This is the definitive list AI should use for proactive suggestions
    # Maps skill names to their user-facing triggers
    ONBOARDING_SKILLS = {
        'setup_goals': {'name': 'setup-goals', 'trigger': 'setup goals', 'priority': 'critical', 'time': '8 min'},
        'setup_workspace': {'name': 'setup-workspace', 'trigger': 'setup workspace', 'priority': 'high', 'time': '5-8 min'},
        'learn_projects': {'name': 'learn-projects', 'trigger': 'learn projects', 'priority': 'high', 'time': '8-10 min'},
        'learn_skills': {'name': 'learn-skills', 'trigger': 'learn skills', 'priority': 'high', 'time': '10-12 min'},
        'learn_integrations': {'name': 'learn-integrations', 'trigger': 'learn integrations', 'priority': 'high', 'time': '10-12 min'},
        'learn_nexus': {'name': 'learn-nexus', 'trigger': 'learn nexus', 'priority': 'medium', 'time': '15-18 min'},
    }

    pending_onboarding = []
    for key, info in ONBOARDING_SKILLS.items():
        if not learning_completed.get(key, False):
            pending_onboarding.append({
                'key': key,
                'name': info['name'],
                'trigger': info['trigger'],
                'priority': info['priority'],
                'time': info['time'],
            })

    # Filter to non-complete projects for menu
    active_projects = [p for p in projects if p.get('status') != 'COMPLETE']

    # Check if any integrations are configured
    # Detection methods (any one is sufficient):
    # 1. core-learnings.md has ## Integrations section with actual integration entries (### headers)
    # 2. User has completed learn_integrations skill (tracked in learning_completed)
    integrations_configured = False
    core_learnings_path = base / "01-memory" / "core-learnings.md"
    if core_learnings_path.exists():
        try:
            with open(core_learnings_path, 'r', encoding='utf-8') as f:
                learnings_content = f.read()
                # Check for Integrations section with actual integration entries (### subsections)
                if '## Integrations' in learnings_content:
                    # Look for ### headers under ## Integrations (indicates actual integrations added)
                    integrations_match = re.search(r'## Integrations\s*\n(.*?)(?=\n## |\Z)', learnings_content, re.DOTALL)
                    if integrations_match:
                        section_content = integrations_match.group(1)
                        # Has actual integrations if there are ### subsections (e.g., ### Notion, ### GitHub)
                        integrations_configured = '### ' in section_content
        except Exception:
            pass

    # Also check if user has completed learn_integrations (they understand integrations even if none configured)
    # This is stored separately in learning_completed['learn_integrations']

    # Detect built integrations (have master/connect skill pattern)
    configured_integrations = detect_configured_integrations(base_path)

    # Check for updates (non-blocking - network errors won't fail startup)
    update_info = {
        'update_available': False,
        'local_version': get_local_version(base_path),
        'upstream_version': None,
        'checked': False
    }
    if check_updates:
        try:
            update_result = check_for_updates(base_path)
            update_info = {
                'update_available': update_result.get('update_available', False),
                'local_version': update_result.get('local_version', 'unknown'),
                'upstream_version': update_result.get('upstream_version'),
                'checked': update_result.get('checked', False),
                'changes_count': update_result.get('changes_count', 0)
            }
        except Exception:
            # Network/git errors should NOT fail startup
            pass

    # Build display_hints - critical items AI must not miss when rendering menu
    # These are top-level action items that should be impossible to overlook
    display_hints = []
    if update_info['update_available']:
        display_hints.append(f"SHOW_UPDATE_BANNER: v{update_info['local_version']} → v{update_info.get('upstream_version', 'latest')}")
    if pending_onboarding:
        display_hints.append(f"ONBOARDING_INCOMPLETE: {len(pending_onboarding)} skills pending")
    if not goals_personalized:
        display_hints.append("PROMPT_SETUP_GOALS: Goals not yet personalized")
    if not workspace_configured:
        display_hints.append("PROMPT_SETUP_WORKSPACE: Workspace not configured")

    result['stats'] = {
        # DISPLAY_HINTS: Critical items AI must show in menu - check this FIRST
        'display_hints': display_hints,
        'files_embedded': len(result['memory_content']),
        'mandatory_maps_loaded': mandatory_maps_found,
        'mandatory_maps_total': len(MANDATORY_MAPS),
        'total_projects': len(projects),
        'active_projects': len([p for p in projects if p.get('status') == 'IN_PROGRESS']),
        'non_complete_projects': len(active_projects),
        'total_skills': len(skills),
        'user_skills': len(user_skills),
        'goals_personalized': goals_personalized,
        'workspace_configured': workspace_configured,
        'integrations_configured': integrations_configured,
        'configured_integrations': configured_integrations,  # List of built integrations
        'learning_completed': learning_completed,
        # ONBOARDING: Only incomplete onboarding skills - AI should use this for proactive suggestions
        # If this list is empty, user has completed all onboarding
        'pending_onboarding': pending_onboarding,
        'onboarding_complete': len(pending_onboarding) == 0,
        'update_available': update_info['update_available'],
        'update_info': update_info,
    }

    return result


def load_project(project_id: str, base_path: str = ".") -> Dict[str, Any]:
    """Load complete project context (all planning files)."""
    base = Path(base_path)
    project_path = None

    # Find project by ID
    search_dirs = [
        base / "02-projects",
        base / "02-projects" / "00-onboarding"
    ]
    
    for search_dir in search_dirs:
        if not search_dir.exists(): continue
        for proj_dir in search_dir.glob("*"):
            if proj_dir.is_dir() and proj_dir.name.startswith(project_id):
                project_path = proj_dir
                break
        if project_path: break

    if not project_path:
        return {'error': f'Project not found: {project_id}'}

    result = {
        'loaded_at': datetime.now().isoformat(),
        'bundle': 'project',
        'project_id': project_id,
        'project_path': str(project_path),
        'files': {}
    }

    # Load all planning files
    planning_files = [
        '01-planning/overview.md',
        '01-planning/requirements.md',
        '01-planning/design.md',
        '01-planning/steps.md'
    ]

    for file_rel in planning_files:
        file_path = project_path / file_rel
        if file_path.exists():
            # Extract YAML metadata
            metadata = extract_yaml_frontmatter(str(file_path))

            # Load content only for line counting (not returned to avoid truncation)

            result['files'][file_rel] = {
                'path': str(file_path),
                'metadata': metadata
                # NO 'content' field - use Read tool for complete content
            }

    # List outputs directory
    outputs_path = project_path / "03-outputs"
    if outputs_path.exists():
        result['outputs'] = [str(f.relative_to(outputs_path)) for f in outputs_path.rglob("*") if f.is_file()]

    return result


def load_skill(skill_name: str, base_path: str = ".") -> Dict[str, Any]:
    """Load complete skill context."""
    base = Path(base_path)

    # Search for skill in both locations (supports category subfolders)
    skill_path = None

    for skills_dir in [base / "03-skills", base / "00-system" / "skills"]:
        if not skills_dir.exists():
            continue

        # First try direct path (e.g., skills/notion-connect)
        direct_path = skills_dir / skill_name
        if direct_path.exists() and (direct_path / "SKILL.md").exists():
            skill_path = direct_path
            break

        # Then search recursively in category subfolders (e.g., skills/notion/notion-connect)
        for skill_file in skills_dir.glob(f"**/{skill_name}/SKILL.md"):
            skill_path = skill_file.parent
            break

        if skill_path:
            break

    if not skill_path:
        return {'error': f'Skill not found: {skill_name}'}

    result = {
        'loaded_at': datetime.now().isoformat(),
        'bundle': 'skill',
        'skill_name': skill_name,
        'skill_path': str(skill_path),
        'files': {},
        'references_loaded': [],
        'scripts_loaded': [],
        'assets_available': []
    }

    # Load SKILL.md with full content
    skill_file = skill_path / "SKILL.md"
    if skill_file.exists():
        metadata = extract_yaml_frontmatter(str(skill_file))

        # Read full content
        try:
            with open(skill_file, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            content = f"ERROR reading file: {e}"

        result['files']['SKILL.md'] = {
            'path': str(skill_file),
            'metadata': metadata,
            'content': content
        }

        # AUTO-LOAD references declared in YAML (with content)
        if metadata and 'load_references' in metadata:
            references_path = skill_path / "references"
            if references_path.exists():
                for ref_file in metadata['load_references']:
                    ref_path = references_path / ref_file
                    if ref_path.exists():
                        try:
                            with open(ref_path, 'r', encoding='utf-8') as f:
                                ref_content = f.read()
                        except Exception as e:
                            ref_content = f"ERROR reading file: {e}"
                        result['files'][f'references/{ref_file}'] = {
                            'path': str(ref_path),
                            'content': ref_content
                        }
                        result['references_loaded'].append(ref_file)

        # AUTO-LOAD scripts declared in YAML (with content)
        if metadata and 'load_scripts' in metadata:
            scripts_path = skill_path / "scripts"
            if scripts_path.exists():
                for script_file in metadata['load_scripts']:
                    script_path_file = scripts_path / script_file
                    if script_path_file.exists():
                        try:
                            with open(script_path_file, 'r', encoding='utf-8') as f:
                                script_content = f.read()
                        except Exception as e:
                            script_content = f"ERROR reading file: {e}"
                        result['files'][f'scripts/{script_file}'] = {
                            'path': str(script_path_file),
                            'content': script_content
                        }
                        result['scripts_loaded'].append(script_file)

    # List remaining references (not auto-loaded)
    references_path = skill_path / "references"
    if references_path.exists():
        all_refs = [f.name for f in references_path.glob("*") if f.is_file()]
        result['references_available'] = [r for r in all_refs if r not in result['references_loaded']]

    # List remaining scripts (not auto-loaded)
    scripts_path = skill_path / "scripts"
    if scripts_path.exists():
        all_scripts = [f.name for f in scripts_path.glob("*") if f.is_file()]
        result['scripts_available'] = [s for s in all_scripts if s not in result['scripts_loaded']]

    # List assets (never auto-loaded)
    assets_path = skill_path / "assets"
    if assets_path.exists():
        result['assets_available'] = [f.name for f in assets_path.glob("*") if f.is_file()]

    return result


# NOTE: All directive parsing/validation functions removed!
# The system now uses intelligent state detection based on file existence
# and project metadata. No directives needed!


# =============================================================================
# UPSTREAM SYNC FUNCTIONS
# =============================================================================

def run_git_command(args: List[str], cwd: str = None) -> Tuple[bool, str]:
    """
    Run a git command and return (success, output).

    Args:
        args: Git command arguments (e.g., ['status', '--porcelain'])
        cwd: Working directory (default: current directory)

    Returns:
        Tuple of (success: bool, output: str)
    """
    try:
        result = subprocess.run(
            ['git'] + args,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=30
        )
        output = result.stdout.strip() or result.stderr.strip()
        return result.returncode == 0, output
    except subprocess.TimeoutExpired:
        return False, "Git command timed out"
    except FileNotFoundError:
        return False, "Git is not installed"
    except Exception as e:
        return False, str(e)


def get_local_version(base_path: str) -> str:
    """Read local version from 00-system/VERSION file."""
    version_file = Path(base_path) / "00-system" / "VERSION"
    try:
        if version_file.exists():
            return version_file.read_text(encoding='utf-8').strip()
        return "unknown"
    except Exception:
        return "unknown"


def get_upstream_url(base_path: str) -> str:
    """
    Get upstream URL from user-config.yaml or use default.
    """
    config_path = Path(base_path) / "01-memory" / "user-config.yaml"

    if config_path.exists():
        try:
            content = config_path.read_text(encoding='utf-8')
            if content.startswith('---'):
                parts = content.split('---', 2)
                if len(parts) >= 2:
                    config = yaml.safe_load(parts[1])
                    if config and 'sync' in config:
                        url = config['sync'].get('upstream_url')
                        if url:
                            return url
        except Exception:
            pass

    return DEFAULT_UPSTREAM_URL


def ensure_upstream_remote(base_path: str) -> Tuple[bool, str]:
    """
    Ensure 'upstream' remote exists. Add it if missing.

    Returns:
        Tuple of (success, message)
    """
    # Check if upstream already exists
    success, output = run_git_command(['remote', 'get-url', 'upstream'], cwd=base_path)

    if success:
        return True, output  # Already configured

    # Add upstream remote
    upstream_url = get_upstream_url(base_path)
    success, output = run_git_command(['remote', 'add', 'upstream', upstream_url], cwd=base_path)

    if success:
        return True, upstream_url
    else:
        return False, f"Failed to add upstream: {output}"


def check_for_updates(base_path: str) -> Dict[str, Any]:
    """
    Check if updates are available from upstream.

    This is designed to be FAST - called on every startup.
    Only fetches refs, doesn't download content.

    Returns:
        Dict with update status and version info
    """
    result = {
        'checked': True,
        'update_available': False,
        'local_version': get_local_version(base_path),
        'upstream_version': None,
        'error': None
    }

    # Pre-flight: Check if we're in a git repo
    success, _ = run_git_command(['rev-parse', '--git-dir'], cwd=base_path)
    if not success:
        result['checked'] = False
        result['error'] = "Not a git repository"
        return result

    # Ensure upstream remote exists
    success, upstream_url = ensure_upstream_remote(base_path)
    if not success:
        result['checked'] = False
        result['error'] = upstream_url  # Contains error message
        return result

    result['upstream_url'] = upstream_url

    # Fetch upstream (just refs, fast)
    success, output = run_git_command(['fetch', 'upstream', '--quiet'], cwd=base_path)
    if not success:
        # Network error - don't fail startup, just note it
        result['checked'] = False
        result['error'] = f"Could not reach upstream: {output}"
        return result

    # Compare local vs upstream 00-system/
    # Get hash of local 00-system/
    success, local_hash = run_git_command(
        ['rev-parse', 'HEAD:00-system'],
        cwd=base_path
    )
    if not success:
        local_hash = "unknown"

    # Get hash of upstream 00-system/
    success, upstream_hash = run_git_command(
        ['rev-parse', 'upstream/main:00-system'],
        cwd=base_path
    )
    if not success:
        result['error'] = f"Could not read upstream version: {output}"
        return result

    # Try to read upstream VERSION file
    success, upstream_version = run_git_command(
        ['show', 'upstream/main:00-system/VERSION'],
        cwd=base_path
    )
    if success:
        result['upstream_version'] = upstream_version.strip()

    # Compare hashes
    if local_hash != upstream_hash:
        result['update_available'] = True

        # Get list of changed files
        success, diff_output = run_git_command(
            ['diff', '--name-only', 'HEAD', 'upstream/main', '--', '00-system/', 'CLAUDE.md', 'README.md'],
            cwd=base_path
        )
        if success and diff_output:
            result['changed_files'] = diff_output.split('\n')
            result['changes_count'] = len(result['changed_files'])

    return result


def sync_from_upstream(base_path: str, dry_run: bool = False, force: bool = False) -> Dict[str, Any]:
    """
    Sync system files from upstream repository.

    Args:
        base_path: Root path to Nexus installation
        dry_run: If True, show what would change without changing
        force: If True, skip confirmation prompts

    Returns:
        Dict with sync results
    """
    result = {
        'success': False,
        'dry_run': dry_run,
        'local_version': get_local_version(base_path),
        'upstream_version': None,
        'files_updated': [],
        'backup_path': None,
        'error': None
    }

    # Pre-flight checks
    # 1. Check git installed and we're in a repo
    success, _ = run_git_command(['rev-parse', '--git-dir'], cwd=base_path)
    if not success:
        result['error'] = "Not a git repository"
        return result

    # 2. Check for uncommitted changes (warn user)
    success, status_output = run_git_command(['status', '--porcelain'], cwd=base_path)
    if success and status_output and not force:
        result['error'] = "Uncommitted changes detected. Commit first or use --force."
        result['uncommitted_changes'] = status_output.split('\n')
        return result

    # 3. Ensure upstream exists and fetch
    success, upstream_url = ensure_upstream_remote(base_path)
    if not success:
        result['error'] = upstream_url
        return result

    result['upstream_url'] = upstream_url

    success, _ = run_git_command(['fetch', 'upstream'], cwd=base_path)
    if not success:
        result['error'] = "Could not fetch from upstream. Check your internet connection."
        return result

    # Get upstream version
    success, upstream_version = run_git_command(
        ['show', 'upstream/main:00-system/VERSION'],
        cwd=base_path
    )
    if success:
        result['upstream_version'] = upstream_version.strip()

    # Get changed files
    success, diff_output = run_git_command(
        ['diff', '--name-only', 'HEAD', 'upstream/main', '--', '00-system/', 'CLAUDE.md', 'README.md'],
        cwd=base_path
    )

    if not success or not diff_output.strip():
        result['success'] = True
        result['message'] = "Already up-to-date"
        return result

    changed_files = [f for f in diff_output.strip().split('\n') if f]
    result['files_to_update'] = changed_files

    # Dry run - just show what would change
    if dry_run:
        result['success'] = True
        result['message'] = f"Would update {len(changed_files)} files"
        return result

    # Create backup of local system files that will be overwritten
    backup_dir = Path(base_path) / ".sync-backup" / datetime.now().strftime("%Y-%m-%d-%H%M%S")
    backup_dir.mkdir(parents=True, exist_ok=True)
    result['backup_path'] = str(backup_dir)

    for file_path in changed_files:
        local_file = Path(base_path) / file_path
        if local_file.exists():
            backup_file = backup_dir / file_path
            backup_file.parent.mkdir(parents=True, exist_ok=True)
            try:
                shutil.copy2(local_file, backup_file)
            except Exception as e:
                result['error'] = f"Backup failed: {e}"
                return result

    # Perform the sync - checkout system files from upstream
    for sync_path in SYNC_PATHS:
        success, output = run_git_command(
            ['checkout', 'upstream/main', '--', sync_path],
            cwd=base_path
        )
        if success:
            result['files_updated'].append(sync_path)
        else:
            # Non-fatal: file might not exist in upstream
            pass

    result['success'] = True
    result['message'] = f"Updated {len(result['files_updated'])} paths from upstream"

    return result


def main():
    # Configure UTF-8 output for Windows console
    if sys.stdout.encoding != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')

    # DYNAMIC BASE PATH DETECTION
    # Script lives in: {nexus-root}/00-system/core/nexus-loader.py
    # So nexus-root is 2 levels up from script location
    script_path = Path(__file__).resolve()  # Absolute path to this script
    detected_nexus_root = script_path.parent.parent.parent  # Go up 2 levels: core -> 00-system -> nexus-root

    parser = argparse.ArgumentParser(description="Nexus-v4 Context Loader")
    parser.add_argument('--startup', action='store_true', help='Load startup context with embedded memory files')
    parser.add_argument('--resume', action='store_true', help='Resume after context summary (skip menu, continue working)')
    parser.add_argument('--skip-update-check', action='store_true', help='Skip update check during startup (faster startup)')
    parser.add_argument('--metadata', action='store_true', help='Load only project/skill metadata (use after --startup --no-metadata)')
    parser.add_argument('--no-metadata', action='store_true', help='Exclude metadata from startup (smaller output, use --metadata separately)')
    parser.add_argument('--project', help='Load project by ID')
    parser.add_argument('--skill', help='Load skill by name')
    parser.add_argument('--list-projects', action='store_true', help='List all projects')
    parser.add_argument('--list-skills', action='store_true', help='List all skills')
    parser.add_argument('--full', action='store_true', help='Return complete metadata (default: minimal fields for efficiency)')
    parser.add_argument('--base-path', default=str(detected_nexus_root), help=f'Base path to Nexus-v4 (default: auto-detected from script location)')
    parser.add_argument('--show-tokens', action='store_true', help='Include token cost analysis')
    # Sync commands
    parser.add_argument('--check-update', action='store_true', help='Check if upstream updates are available')
    parser.add_argument('--sync', action='store_true', help='Sync system files from upstream')
    parser.add_argument('--dry-run', action='store_true', help='Show what would change without changing (use with --sync)')
    parser.add_argument('--force', action='store_true', help='Skip confirmation prompts (use with --sync)')

    args = parser.parse_args()

    # Execute command
    if args.check_update:
        result = check_for_updates(args.base_path)
    elif args.sync:
        result = sync_from_upstream(args.base_path, dry_run=args.dry_run, force=args.force)
    elif args.startup or args.resume:
        include_metadata = not args.no_metadata
        check_updates = not args.skip_update_check
        result = load_startup(args.base_path, include_metadata=include_metadata, resume_mode=args.resume, check_updates=check_updates)
    elif args.metadata:
        result = load_metadata(args.base_path)
    elif args.project:
        result = load_project(args.project, args.base_path)
    elif args.skill:
        result = load_skill(args.skill, args.base_path)
    elif args.list_projects:
        projects = scan_projects(args.base_path, minimal=not args.full)
        result = {'projects': projects}
    elif args.list_skills:
        skills = scan_skills(args.base_path, minimal=not args.full)
        result = {'skills': skills}
    else:
        parser.print_help()
        return

    # Add token analysis if requested
    if args.show_tokens:
        token_stats = calculate_bundle_tokens(result)
        result['token_cost'] = token_stats

        # Warn if metadata budget exceeded
        if token_stats.get('metadata', 0) > METADATA_BUDGET_WARNING:
            result['warnings'] = result.get('warnings', [])
            result['warnings'].append(
                f"Metadata tokens ({token_stats['metadata']}) exceeds recommended budget ({METADATA_BUDGET_WARNING})"
            )

    # Output JSON (always pretty-printed for human readability)
    output = json.dumps(result, indent=2, ensure_ascii=False)
    output_chars = len(output)

    # Add truncation detection metadata at the very end
    # AI can check: if received chars < output_chars, output was truncated
    result['_output'] = {
        'chars': output_chars,
        'truncation_risk': output_chars > BASH_OUTPUT_LIMIT * 0.9,  # >90% of limit
        'split_recommended': output_chars > BASH_OUTPUT_LIMIT,
    }

    # Re-serialize with metadata (adds ~100 chars)
    final_output = json.dumps(result, indent=2, ensure_ascii=False)
    print(final_output)


if __name__ == "__main__":
    main()
