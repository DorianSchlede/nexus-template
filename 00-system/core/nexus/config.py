"""
Configuration constants for Nexus.

This module centralizes all constants, paths, and settings
that were previously scattered throughout nexus-loader.py.
"""

from pathlib import Path
from typing import Dict, List

# =============================================================================
# TOKEN COUNTING CONSTANTS
# =============================================================================

CHARS_PER_TOKEN = 4  # Rough estimate: 1 token ~ 4 characters
CONTEXT_WINDOW = 200000  # Claude's context window
METADATA_BUDGET_WARNING = 7000  # Warn if metadata >7K tokens (3.5% of window)
BASH_OUTPUT_LIMIT = 30000  # Claude Code bash output truncation limit

# Cache configuration
CACHE_DIR = "00-system/.cache"  # Relative to Nexus root
CACHE_STARTUP_FILE = "context_startup.json"  # Used by nexus-loader.py CLI fallback

# =============================================================================
# MANDATORY NAVIGATION MAPS
# =============================================================================

# These files provide core system navigation and context
# Always loaded at startup - ORDER MATTERS (orchestrator first!)
MANDATORY_MAPS: List[str] = [
    "00-system/core/orchestrator.md",  # AI behavior rules, routing, menu display - LOAD FIRST
    "00-system/system-map.md",  # System structure and navigation hub
]

# =============================================================================
# UPSTREAM SYNC CONFIGURATION
# =============================================================================

# Default upstream repository URL (users can override in user-config.yaml)
DEFAULT_UPSTREAM_URL = "https://github.com/DorianSchlede/nexus-template.git"

# Paths to sync from upstream (system files only)
SYNC_PATHS: List[str] = [
    "00-system/",
    "CLAUDE.md",
    "README.md",
]

# Paths to NEVER touch (user's personal data)
PROTECTED_PATHS: List[str] = [
    "01-memory/",
    "02-builds/",
    "03-skills/",
    "04-workspace/",
    ".env",
    ".claude/",
    ".sync-backup/",
]

# =============================================================================
# INTEGRATION DETECTION
# =============================================================================

# Map integration names to their required environment variables
INTEGRATION_ENV_VARS: Dict[str, str] = {
    "airtable": "AIRTABLE_API_KEY",
    "notion": "NOTION_API_KEY",
    "beam": "BEAM_API_KEY",
    "hubspot": "HUBSPOT_ACCESS_TOKEN",
}

# =============================================================================
# ONBOARDING SKILLS CONFIGURATION
# =============================================================================

# Maps skill keys to their metadata for proactive suggestions
ONBOARDING_SKILLS: Dict[str, Dict[str, str]] = {
    "setup_memory": {
        "name": "setup-memory",
        "trigger": "setup memory",
        "priority": "critical",
        "time": "8 min",
    },
    "create_folders": {
        "name": "create-folders",
        "trigger": "create folders",
        "priority": "high",
        "time": "5-8 min",
    },
    "learn_builds": {
        "name": "learn-builds",
        "trigger": "learn builds",
        "priority": "high",
        "time": "8-10 min",
    },
    "learn_skills": {
        "name": "learn-skills",
        "trigger": "learn skills",
        "priority": "high",
        "time": "10-12 min",
    },
    "learn_integrations": {
        "name": "learn-integrations",
        "trigger": "learn integrations",
        "priority": "high",
        "time": "10-12 min",
    },
    "learn_nexus": {
        "name": "learn-nexus",
        "trigger": "learn nexus",
        "priority": "medium",
        "time": "15-18 min",
    },
}

# =============================================================================
# DIRECTORY STRUCTURE
# =============================================================================

# Standard Nexus directory names (relative to base path)
SYSTEM_DIR = "00-system"
MEMORY_DIR = "01-memory"
BUILDS_DIR = "02-builds"
SKILLS_DIR = "03-skills"
WORKSPACE_DIR = "04-workspace"

# Memory file names
GOALS_FILE = "goals.md"
USER_CONFIG_FILE = "user-config.yaml"
MEMORY_MAP_FILE = "memory-map.md"
CORE_LEARNINGS_FILE = "core-learnings.md"

# Build structure
PLANNING_SUBDIR = "01-planning"
RESOURCES_SUBDIR = "02-resources"
WORKING_SUBDIR = "03-working"
OUTPUTS_SUBDIR = "04-outputs"

# Planning file names
OVERVIEW_FILE = "overview.md"
PLAN_FILE = "plan.md"
STEPS_FILE = "steps.md"
REQUIREMENTS_FILE = "requirements.md"
DESIGN_FILE = "design.md"

# =============================================================================
# PATH HELPERS
# =============================================================================


def get_templates_dir() -> Path:
    """Return the path to the templates directory."""
    return Path(__file__).parent / "templates"


def get_memory_path(base_path: Path, filename: str) -> Path:
    """Return the full path to a memory file."""
    return base_path / MEMORY_DIR / filename


def get_build_path(base_path: Path, build_id: str) -> Path:
    """Return the full path to a build directory."""
    return base_path / BUILDS_DIR / build_id


def get_skill_path(base_path: Path, skill_name: str, user_skill: bool = False) -> Path:
    """Return the full path to a skill directory."""
    if user_skill:
        return base_path / SKILLS_DIR / skill_name
    return base_path / SYSTEM_DIR / "skills" / skill_name
