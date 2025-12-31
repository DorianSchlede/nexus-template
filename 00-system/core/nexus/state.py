"""
State detection and instruction building for Nexus.

This module handles:
- System state classification
- Instruction generation based on state
- Display hints for menu rendering
- Stats compilation
"""

import re
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml

from .config import (
    MANDATORY_MAPS,
    MEMORY_DIR,
    ONBOARDING_SKILLS,
    WORKSPACE_DIR,
)
from .models import SystemState
from .utils import is_template_file


def detect_system_state(
    files_exist: Dict[str, bool],
    goals_path: Path,
    projects: List[Dict[str, Any]],
    resume_mode: bool = False,
) -> SystemState:
    """
    Classify the current system state based on file existence and project status.

    Args:
        files_exist: Dict mapping file keys to existence status
        goals_path: Path to goals.md file
        projects: List of project metadata
        resume_mode: Whether we're resuming from context summary

    Returns:
        SystemState enum value
    """
    if resume_mode:
        return SystemState.RESUME

    # STATE 1: First Time Setup (no goals.md)
    if not files_exist.get("goals", False):
        return SystemState.FIRST_TIME_WITH_DEFAULTS

    # STATE 2: Goals exist but are still templates
    if is_template_file(str(goals_path)):
        return SystemState.FIRST_TIME_WITH_DEFAULTS

    # STATE 3: Goals exist and personalized
    active_projects = [p for p in projects if p.get("status") == "IN_PROGRESS"]

    if active_projects:
        return SystemState.OPERATIONAL_WITH_ACTIVE_PROJECTS

    return SystemState.OPERATIONAL


def build_instructions(
    state: SystemState,
    projects: List[Dict[str, Any]],
    display_hints: List[str],
) -> Dict[str, Any]:
    """
    Build execution instructions based on system state.

    Args:
        state: Current system state
        projects: List of project metadata
        display_hints: List of display hints for menu

    Returns:
        Instructions dictionary
    """
    active_projects = [p for p in projects if p.get("status") == "IN_PROGRESS"]

    instructions = {
        "action": "display_menu",
        "execution_mode": "interactive",
        "message": "",
        "reason": "",
        "workflow": [],
    }

    if display_hints:
        instructions["display_hints"] = display_hints

    if state == SystemState.FIRST_TIME_WITH_DEFAULTS:
        instructions.update({
            "suggest_onboarding": True,
            "message": "Welcome to Nexus! Quick Start Mode active.",
            "reason": "Smart defaults created - system ready for immediate use",
            "workflow": [
                "Display modern Nexus header",
                "Show Quick Start Mode notice",
                "Display empty projects section",
                "Show available skills",
                'Suggest: "setup goals" to personalize (optional)',
                "Wait for user input - can work immediately",
            ],
        })

    elif state == SystemState.OPERATIONAL_WITH_ACTIVE_PROJECTS:
        most_recent = active_projects[0] if active_projects else None
        instructions.update({
            "message": f"Welcome back! You have {len(active_projects)} active project(s)",
            "reason": f"Active projects detected: {most_recent['id'] if most_recent else 'unknown'}",
            "workflow": [
                "Display Nexus banner",
                "Show user goals (from goals.md)",
                f"Highlight {len(active_projects)} active projects",
                "Show available skills",
                "Wait for user input (can resume projects or start new work)",
            ],
        })

    elif state == SystemState.OPERATIONAL:
        instructions.update({
            "message": "System ready - what would you like to work on?",
            "reason": "No active projects",
            "workflow": [
                "Display Nexus banner",
                "Show user goals (from goals.md)",
                "List completed projects",
                "Show available skills",
                'Suggest: "create project" or use skills',
                "Wait for user input",
            ],
        })

    elif state == SystemState.RESUME:
        if active_projects:
            most_recent = active_projects[0]
            project_id = most_recent["id"]
            instructions.update({
                "action": "continue_working",
                "execution_mode": "immediate",
                "suggest_project": project_id,
                "message": "Context restored. Loading project context now.",
                "reason": "Resumed from context summary with active project",
                "critical_warning": "⚠️ FAILURE TO LOAD PROJECT FILES CAUSES CONTEXT LOSS AND ERRORS",
                "loading_sequence": [
                    {
                        "step": 1,
                        "action": "READ_CACHE_FILE",
                        "description": "Read cached startup context for full metadata",
                        "file": "00-system/.cache/context_startup.json",
                    },
                    {
                        "step": 2,
                        "action": "LOAD_SKILL",
                        "description": "Load execute-project skill for project interaction",
                        "command": "python 00-system/core/nexus-loader.py --skill execute-project",
                    },
                    {
                        "step": 3,
                        "action": "LOAD_PROJECT",
                        "description": "Load full project context (overview, plan, steps)",
                        "command": f"python 00-system/core/nexus-loader.py --project {project_id}",
                    },
                ],
                "workflow": [
                    "1. Read cache file for full context",
                    "2. Load execute-project skill",
                    f"3. Load project {project_id} with all files",
                    "4. Continue working from summary instructions",
                    "DO NOT skip any step - context integrity depends on this",
                ],
            })
        else:
            instructions.update({
                "action": "continue_working",
                "execution_mode": "immediate",
                "message": "Context restored. Ready to continue.",
                "reason": "Resumed from context summary - no active project",
                "loading_sequence": [
                    {
                        "step": 1,
                        "action": "READ_CACHE_FILE",
                        "description": "Read cached startup context for full metadata",
                        "file": "00-system/.cache/context_startup.json",
                    },
                ],
                "workflow": [
                    "1. Read cache file for full context",
                    "2. Continue from previous conversation context",
                    "3. Follow user instructions from summary",
                ],
            })

    return instructions


def build_display_hints(
    update_info: Dict[str, Any],
    pending_onboarding: List[Dict[str, Any]],
    goals_personalized: bool,
    workspace_configured: bool,
) -> List[str]:
    """
    Build display hints - critical items AI must show in menu.

    Args:
        update_info: Update check results
        pending_onboarding: List of incomplete onboarding skills
        goals_personalized: Whether goals have been personalized
        workspace_configured: Whether workspace has been configured

    Returns:
        List of display hint strings
    """
    hints = []

    if update_info.get("update_available", False):
        local_ver = update_info.get("local_version", "unknown")
        upstream_ver = update_info.get("upstream_version", "latest")
        hints.append(f"SHOW_UPDATE_BANNER: v{local_ver} → v{upstream_ver}")

    if pending_onboarding:
        hints.append(f"ONBOARDING_INCOMPLETE: {len(pending_onboarding)} skills pending")

    if not goals_personalized:
        hints.append("PROMPT_SETUP_GOALS: Goals not yet personalized")

    if not workspace_configured:
        hints.append("PROMPT_SETUP_WORKSPACE: Workspace not configured")

    return hints


def build_pending_onboarding(learning_completed: Dict[str, bool]) -> List[Dict[str, Any]]:
    """
    Build list of pending onboarding skills.

    Args:
        learning_completed: Dict mapping skill keys to completion status

    Returns:
        List of pending onboarding skill metadata
    """
    pending = []

    for key, info in ONBOARDING_SKILLS.items():
        if not learning_completed.get(key, False):
            pending.append({
                "key": key,
                "name": info["name"],
                "trigger": info["trigger"],
                "priority": info["priority"],
                "time": info["time"],
            })

    return pending


def extract_learning_completed(config_path: Path) -> Dict[str, bool]:
    """
    Extract learning_tracker.completed from user-config.yaml.

    Args:
        config_path: Path to user-config.yaml

    Returns:
        Dict mapping skill keys to completion status
    """
    default_completed = {
        "setup_memory": False,
        "setup_workspace": False,
        "learn_integrations": False,
        "learn_projects": False,
        "learn_skills": False,
        "learn_nexus": False,
    }

    if not config_path.exists():
        return default_completed

    try:
        content = config_path.read_text(encoding="utf-8")
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 2:
                config_data = yaml.safe_load(parts[1])
                if config_data and "learning_tracker" in config_data:
                    tracker = config_data["learning_tracker"]
                    if "completed" in tracker and isinstance(tracker["completed"], dict):
                        default_completed.update(tracker["completed"])
    except Exception:
        pass

    return default_completed


def check_integrations_configured(base_path: Path) -> bool:
    """
    Check if any integrations are configured.

    Detection: core-learnings.md has ## Integrations section with ### headers.

    Args:
        base_path: Root path to Nexus installation

    Returns:
        True if integrations are configured
    """
    core_learnings_path = base_path / MEMORY_DIR / "core-learnings.md"

    if not core_learnings_path.exists():
        return False

    try:
        content = core_learnings_path.read_text(encoding="utf-8")
        if "## Integrations" in content:
            # Look for ### headers under ## Integrations
            integrations_match = re.search(
                r"## Integrations\s*\n(.*?)(?=\n## |\Z)", content, re.DOTALL
            )
            if integrations_match:
                section_content = integrations_match.group(1)
                return "### " in section_content
    except Exception:
        pass

    return False


def check_workspace_configured(base_path: Path) -> bool:
    """
    Check if workspace is configured.

    Args:
        base_path: Root path to Nexus installation

    Returns:
        True if workspace-map.md exists and is not a template
    """
    workspace_map_path = base_path / WORKSPACE_DIR / "workspace-map.md"
    return workspace_map_path.exists() and not is_template_file(str(workspace_map_path))


def check_goals_personalized(goals_path: Path) -> bool:
    """
    Check if goals have been personalized.

    Args:
        goals_path: Path to goals.md

    Returns:
        True if goals exist and are not a template
    """
    return goals_path.exists() and not is_template_file(str(goals_path))


def build_stats(
    base_path: Path,
    memory_content: Dict[str, str],
    projects: List[Dict[str, Any]],
    skills: List[Dict[str, Any]],
    files_exist: Dict[str, bool],
    goals_path: Path,
    config_path: Path,
    update_info: Dict[str, Any],
    configured_integrations: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """
    Build comprehensive stats for menu display.

    Args:
        base_path: Root path to Nexus installation
        memory_content: Embedded file contents
        projects: List of project metadata
        skills: List of skill metadata
        files_exist: Dict mapping file keys to existence status
        goals_path: Path to goals.md
        config_path: Path to user-config.yaml
        update_info: Update check results
        configured_integrations: List of detected integrations

    Returns:
        Stats dictionary
    """
    # Count user skills vs system skills
    user_skills = [s for s in skills if "03-skills" in s.get("_file_path", "")]

    # Check configuration status
    goals_personalized = check_goals_personalized(goals_path)
    workspace_configured = check_workspace_configured(base_path)
    integrations_configured = check_integrations_configured(base_path)

    # Get learning completion status
    learning_completed = extract_learning_completed(config_path)

    # Build pending onboarding
    pending_onboarding = build_pending_onboarding(learning_completed)

    # Build display hints
    display_hints = build_display_hints(
        update_info=update_info,
        pending_onboarding=pending_onboarding,
        goals_personalized=goals_personalized,
        workspace_configured=workspace_configured,
    )

    # Count mandatory maps loaded
    mandatory_maps_found = sum(
        1 for map_path in MANDATORY_MAPS if (base_path / map_path).exists()
    )

    # Filter to non-complete projects
    active_projects = [p for p in projects if p.get("status") != "COMPLETE"]

    return {
        "display_hints": display_hints,
        "files_embedded": len(memory_content),
        "mandatory_maps_loaded": mandatory_maps_found,
        "mandatory_maps_total": len(MANDATORY_MAPS),
        "total_projects": len(projects),
        "active_projects": len([p for p in projects if p.get("status") == "IN_PROGRESS"]),
        "non_complete_projects": len(active_projects),
        "total_skills": len(skills),
        "user_skills": len(user_skills),
        "goals_personalized": goals_personalized,
        "workspace_configured": workspace_configured,
        "integrations_configured": integrations_configured,
        "configured_integrations": configured_integrations,
        "learning_completed": learning_completed,
        "pending_onboarding": pending_onboarding,
        "onboarding_complete": len(pending_onboarding) == 0,
        "update_available": update_info.get("update_available", False),
        "update_info": update_info,
    }
