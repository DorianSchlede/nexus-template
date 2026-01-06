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

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False
    yaml = None

from .config import (
    MANDATORY_MAPS,
    MEMORY_DIR,
    ONBOARDING_SKILLS,
    WORKSPACE_DIR,
)
from .models import SystemState
from .utils import is_template_file, parse_simple_yaml


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
            project_name = most_recent.get("name", project_id)
            project_desc = most_recent.get("description", "").lower()
            progress = most_recent.get("progress", 0) * 100

            # Check for _resume.md to get last active skill/phase
            last_skill = None
            last_phase = None
            project_file_path = most_recent.get("_file_path", "")
            if project_file_path:
                project_dir = Path(project_file_path).parent.parent
                resume_file = project_dir / "_resume.md"
                if resume_file.exists():
                    try:
                        resume_content = resume_file.read_text(encoding="utf-8")
                        if resume_content.startswith("---"):
                            parts = resume_content.split("---", 2)
                            if len(parts) >= 2:
                                if HAS_YAML:
                                    resume_yaml = yaml.safe_load(parts[1])
                                else:
                                    resume_yaml = parse_simple_yaml(parts[1])
                                if resume_yaml:
                                    last_skill = resume_yaml.get("last_skill")
                                    last_phase = resume_yaml.get("phase")
                    except Exception:
                        pass

            # Build skill loading step from _resume.md
            if last_skill:
                # Explicit skill from _resume.md
                skill_step = {
                    "step": 2,
                    "action": "RUN",
                    "command": f"python 00-system/core/nexus-loader.py --skill {last_skill}",
                    "why": f"Last active skill: {last_skill}" + (f" (phase: {last_phase})" if last_phase else ""),
                    "REQUIRED": True,
                    "detected_from": "_resume.md",
                }
            elif last_phase:
                # Phase but no skill - map phase to skill
                phase_skill_map = {
                    "analysis": "analyze-research-project",
                    "synthesis": "synthesize-research-project",
                    "planning": "execute-project",
                    "execution": "execute-project",
                }
                skill_name = phase_skill_map.get(last_phase, "execute-project")
                skill_step = {
                    "step": 2,
                    "action": "RUN",
                    "command": f"python 00-system/core/nexus-loader.py --skill {skill_name}",
                    "why": f"Phase '{last_phase}' from _resume.md",
                    "REQUIRED": True,
                    "detected_from": "_resume.md",
                }
            else:
                # No _resume.md or empty - fallback
                skill_step = {
                    "step": 2,
                    "action": "RUN",
                    "command": "python 00-system/core/nexus-loader.py --skill execute-project",
                    "why": "Default skill (no _resume.md found)",
                    "REQUIRED": True,
                }

            instructions.update({
                "action": "EXECUTE_MANDATORY_LOADING_SEQUENCE",
                "execution_mode": "blocking",
                "project_id": project_id,
                "project_name": project_name,
                "project_phase": last_phase,
                "project_progress": f"{progress:.0f}%",

                # CRITICAL ENFORCEMENT
                "STOP": "🛑 DO NOT CONTINUE WORKING WITHOUT LOADING CONTEXT FIRST",
                "MANDATORY": "You MUST execute ALL steps below BEFORE continuing work",
                "REASON": "Context summary lost project details. Without loading, you will hallucinate.",

                "EXECUTE_NOW": [
                    {
                        "step": 1,
                        "action": "READ",
                        "target": "00-system/.cache/context_startup.json",
                        "why": "Contains full metadata, skills list, project states",
                        "REQUIRED": True,
                    },
                    skill_step,
                    {
                        "step": 3,
                        "action": "RUN",
                        "command": f"python 00-system/core/nexus-loader.py --project {project_id}",
                        "why": "Loads overview.md, plan.md, steps.md - the actual project state",
                        "REQUIRED": True,
                    },
                ],

                "AFTER_LOADING": f"Continue working on '{project_name}' from context summary instructions",

                "FAILURE_CONSEQUENCES": [
                    "You will not know current task progress",
                    "You will not know which steps are done vs pending",
                    "You will make up file contents that don't exist",
                    "User will lose trust when you contradict previous work",
                ],
            })
        else:
            instructions.update({
                "action": "EXECUTE_MANDATORY_LOADING_SEQUENCE",
                "execution_mode": "blocking",

                "STOP": "🛑 DO NOT CONTINUE WORKING WITHOUT LOADING CONTEXT FIRST",
                "MANDATORY": "You MUST execute the step below BEFORE continuing work",

                "EXECUTE_NOW": [
                    {
                        "step": 1,
                        "action": "READ",
                        "target": "00-system/.cache/context_startup.json",
                        "why": "Contains full metadata, skills list, system state",
                        "REQUIRED": True,
                    },
                ],

                "AFTER_LOADING": "Continue from context summary instructions",
            })

    return instructions


def build_display_hints(
    update_info: Dict[str, Any],
    pending_onboarding: List[Dict[str, Any]],
    goals_personalized: bool,
    workspace_configured: bool,
) -> List[str]:
    """
    Build display hints optimized for orchestrator.md menu rendering.

    These hints map directly to conditional sections in orchestrator.md:
    - SHOW_UPDATE_BANNER → Display at top of menu
    - ONBOARDING_INCOMPLETE → Emphasize in suggested steps
    - Individual skill hints → Add to numbered suggestions

    Args:
        update_info: Update check results
        pending_onboarding: List of incomplete onboarding skills
        goals_personalized: Whether goals have been personalized
        workspace_configured: Whether workspace has been configured

    Returns:
        List of display hint strings matching orchestrator.md patterns
    """
    hints = []

    # Update banner (if available)
    if update_info.get("update_available", False):
        local_ver = update_info.get("local_version", "unknown")
        upstream_ver = update_info.get("upstream_version", "latest")
        hints.append(f"SHOW_UPDATE_BANNER: v{local_ver} → v{upstream_ver}")

    # Onboarding summary (for emphasis in suggested steps)
    if pending_onboarding:
        # Sort by priority (setup_memory first, then others)
        priority_order = ["setup_memory", "setup_workspace", "learn_projects", "learn_skills", "learn_integrations", "learn_nexus"]
        sorted_pending = sorted(pending_onboarding, key=lambda x: priority_order.index(x["key"]) if x["key"] in priority_order else 99)

        hints.append(f"ONBOARDING_INCOMPLETE: {len(pending_onboarding)} skills pending")

        # Add individual skill hints for menu rendering
        for skill in sorted_pending:
            skill_key = skill["key"]
            skill_name = skill["name"]

            if skill_key == "setup_memory":
                hints.append(f"SUGGEST_ONBOARDING: 'setup memory' - teach Nexus about you ({skill['time']})")
            elif skill_key == "setup_workspace":
                hints.append(f"SUGGEST_ONBOARDING: 'setup workspace' - organize your files ({skill['time']})")
            elif skill_key == "learn_projects":
                hints.append(f"SUGGEST_ONBOARDING: 'learn projects' - understand projects vs skills ({skill['time']})")
            elif skill_key == "learn_skills":
                hints.append(f"SUGGEST_ONBOARDING: 'learn skills' - automate repeating work ({skill['time']})")
            elif skill_key == "learn_integrations":
                hints.append(f"SUGGEST_ONBOARDING: 'learn integrations' - connect external tools ({skill['time']})")
            elif skill_key == "learn_nexus":
                hints.append(f"SUGGEST_ONBOARDING: 'learn nexus' - deep dive into the system ({skill['time']})")

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
                if HAS_YAML:
                    config_data = yaml.safe_load(parts[1])
                else:
                    config_data = parse_simple_yaml(parts[1])
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
