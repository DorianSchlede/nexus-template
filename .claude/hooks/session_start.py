#!/usr/bin/env -S python3 -B
from __future__ import annotations
"""
SessionStart Hook - Nexus v5 Context Injection

Loads Nexus operating context via XML injection to Claude's additionalContext.

What it does:
- Detects workspace from transcript path (multi-window safe)
- Loads orchestrator, skills, builds, and user goals from nexus modules
- Injects complete context as XML for STARTUP or COMPACT mode
- Auto-resumes active builds based on session_id matching

Triggered by Claude Code on:
- New session start (source=new)
- Session resume (source=resume)
- After /clear command (source=clear)
- After compaction (source=compact)

Performance target: <200ms execution time
"""

import sys
sys.dont_write_bytecode = True  # Prevent .pyc creation for subsequently imported modules

import os
import json
import re
import time
import logging
import shutil
from pathlib import Path
from datetime import datetime

# Clean stale caches on every invocation (fast, <1ms)
for _cache in [Path(__file__).parent / "utils" / "__pycache__",
               Path(__file__).parent.parent.parent / "00-system" / "core" / "nexus" / "__pycache__"]:
    shutil.rmtree(_cache, ignore_errors=True)

# Performance tracking
START_TIME = time.perf_counter()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - SessionStart - %(levelname)s - %(message)s'
)

# Add parent directory to path for utils imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.transcript import parse_transcript_for_build, find_build_by_session_id
from utils.xml import escape_xml_content, escape_xml_attribute, load_file_to_xml


def extract_user_preferences(config_path: Path) -> dict:
    """
    Extract user preferences from user-config.yaml using regex (no yaml dependency).

    Returns:
        Dict with language, timezone, date_format (empty strings if not set)
    """
    preferences = {
        "language": "",
        "timezone": "",
        "date_format": "YYYY-MM-DD"
    }

    if not config_path.exists():
        return preferences

    try:
        content = config_path.read_text(encoding="utf-8")

        # Extract language (handles both quoted and unquoted values)
        lang_match = re.search(r'language:\s*["\']?([^"\'\n]*)["\']?', content)
        if lang_match and lang_match.group(1).strip():
            preferences["language"] = lang_match.group(1).strip()

        # Extract timezone
        tz_match = re.search(r'timezone:\s*["\']?([^"\'\n]*)["\']?', content)
        if tz_match and tz_match.group(1).strip():
            preferences["timezone"] = tz_match.group(1).strip()

        # Extract date_format
        df_match = re.search(r'date_format:\s*["\']?([^"\'\n]*)["\']?', content)
        if df_match and df_match.group(1).strip():
            preferences["date_format"] = df_match.group(1).strip()

        logging.info(f"User preferences extracted: language={preferences['language'] or 'not set'}")

    except Exception as e:
        logging.warning(f"Failed to extract user preferences: {e}")

    return preferences


def extract_onboarding_state(config_path: Path) -> dict:
    """
    Extract onboarding state from user-config.yaml for cross-session resume.

    Returns:
        Dict with onboarding status, in_progress_skill, language_preference,
        path_chosen, quick_start_state, and complete_setup_state fields.
    """
    state = {
        "status": "not_started",
        "in_progress_skill": None,
        "language_preference": None,
        "path_chosen": None,
        "quick_start_state": {
            "step_completed": 0,
            "intention_captured": False,
            "first_build_created": False,
            "workspace_created": False,
            "hi_menu_taught": False
        },
        "complete_setup_state": {
            "step_completed": 0,
            "files_uploaded": False,
            "file_analysis_done": False,
            "role_captured": False,
            "goals_captured": False,
            "roadmap_created": False,
            "workspace_created": False,
            "first_build_created": False,
            "hi_menu_taught": False
        }
    }

    if not config_path.exists():
        return state

    try:
        content = config_path.read_text(encoding="utf-8")

        # Extract onboarding.status
        status_match = re.search(r'onboarding:\s*\n(?:.*\n)*?\s*status:\s*["\']?([^"\'\n]+)["\']?', content)
        if status_match:
            state["status"] = status_match.group(1).strip()

        # Extract in_progress_skill (can be null or a string)
        skill_match = re.search(r'in_progress_skill:\s*["\']?([^"\'\n]*)["\']?', content)
        if skill_match:
            val = skill_match.group(1).strip()
            state["in_progress_skill"] = val if val and val != "null" else None

        # Extract language_preference
        lang_pref_match = re.search(r'language_preference:\s*["\']?([^"\'\n]*)["\']?', content)
        if lang_pref_match:
            val = lang_pref_match.group(1).strip()
            state["language_preference"] = val if val and val != "null" else None

        # Extract path_chosen (v5)
        path_chosen_match = re.search(r'path_chosen:\s*["\']?([^"\'\n]*)["\']?', content)
        if path_chosen_match:
            val = path_chosen_match.group(1).strip()
            state["path_chosen"] = val if val and val != "null" else None

        # Extract step_completed from quick_start_state (v5)
        # Need to find it within the quick_start_state block
        quick_start_block = re.search(r'quick_start_state:\s*\n((?:.*\n)*?)\s*(?:\n\s*\w+_\w+_state:|complete_setup_state:|# |$)', content)
        if quick_start_block:
            block_content = quick_start_block.group(1)
            step_match = re.search(r'step_completed:\s*(\d+)', block_content)
            if step_match:
                state["quick_start_state"]["step_completed"] = int(step_match.group(1))

        # Extract step_completed from complete_setup_state
        # Need to find it within the complete_setup_state block
        complete_setup_block = re.search(r'complete_setup_state:\s*\n((?:.*\n)*?)\s*(?:\n\s*# |$)', content)
        if complete_setup_block:
            block_content = complete_setup_block.group(1)
            step_match = re.search(r'step_completed:\s*(\d+)', block_content)
            if step_match:
                state["complete_setup_state"]["step_completed"] = int(step_match.group(1))

        logging.info(f"Onboarding state: status={state['status']}, in_progress_skill={state['in_progress_skill']}, path_chosen={state['path_chosen']}")

    except Exception as e:
        logging.warning(f"Failed to extract onboarding state: {e}")

    return state


def check_fresh_install(build_dir: str) -> bool:
    """
    Check if this is a fresh install that needs initial setup.

    Fresh install is detected when ALL of these are true:
    1. `.claude/.setup_complete` does NOT exist
    2. `01-memory/user-config.yaml` exists (Nexus files were cloned)

    Returns:
        True if fresh install detected, False otherwise
    """
    base_path = Path(build_dir) if build_dir else Path.cwd()

    # Check for setup complete marker
    setup_complete_marker = base_path / ".claude" / ".setup_complete"
    if setup_complete_marker.exists():
        return False  # Already set up

    # Check if Nexus was cloned (user-config.yaml exists)
    user_config = base_path / "01-memory" / "user-config.yaml"
    if not user_config.exists():
        return False  # Not a valid Nexus installation

    logging.info("Fresh install detected - setup not completed")
    return True


def determine_onboarding_action(session_source: str, onboarding_state: dict, build_dir: str = "") -> dict:
    """
    Determine what to show user based on onboarding state.

    Args:
        session_source: "new" | "compact" | "resume"
        onboarding_state: dict from extract_onboarding_state()
        build_dir: workspace root path for fresh install detection

    Returns:
        dict with action, skill, template, resume_step
    """
    # Priority 0: Check for fresh install (needs setup before onboarding)
    if build_dir and check_fresh_install(build_dir):
        return {
            "action": "run_setup",
            "skill": "setup",
            "template": "startup_first_run",
            "fresh_install": True
        }

    status = onboarding_state.get("status", "not_started")
    in_progress_skill = onboarding_state.get("in_progress_skill")

    # Check if in-progress skill (cross-session continuity)
    if in_progress_skill and session_source in ("compact", "resume"):
        if in_progress_skill == "quick-start":
            step = onboarding_state["quick_start_state"]["step_completed"]
            return {
                "action": "resume_skill",
                "skill": "quick-start",
                "resume_from_step": step + 1,
                "template": "compact_onboarding_resume"
            }
        elif in_progress_skill == "complete-setup":
            step = onboarding_state["complete_setup_state"]["step_completed"]
            return {
                "action": "resume_skill",
                "skill": "complete-setup",
                "resume_from_step": step + 1,
                "template": "compact_onboarding_resume"
            }
        elif in_progress_skill == "how-nexus-works":
            return {
                "action": "resume_skill",
                "skill": "how-nexus-works",
                "template": "compact_onboarding_resume"
            }

    # Route based on status
    if status == "not_started":
        return {
            "action": "show_heroic_intro",
            "template": "startup_first_run"
        }

    # v5: in_progress - check path_chosen
    elif status == "in_progress":
        path_chosen = onboarding_state.get("path_chosen")

        if path_chosen == "quick_start":
            step = onboarding_state["quick_start_state"]["step_completed"]
            return {
                "action": "resume_skill",
                "skill": "quick-start",
                "resume_from_step": step + 1,
                "template": "compact_onboarding_resume"
            }
        elif path_chosen == "complete_setup":
            step = onboarding_state["complete_setup_state"]["step_completed"]
            return {
                "action": "resume_skill",
                "skill": "complete-setup",
                "resume_from_step": step + 1,
                "template": "compact_onboarding_resume"
            }
        else:
            # Shouldn't happen, but fallback to showing intro
            return {
                "action": "show_heroic_intro",
                "template": "startup_first_run"
            }

    # v5: complete - normal operation
    elif status == "complete":
        return {
            "action": "normal_menu",
            "template": None  # Use standard menu
        }

    # ===== BACKWARD COMPATIBILITY FOR v4 STATUSES =====

    elif status == "tour_complete":
        return {
            "action": "load_complete_setup",
            "skill": "complete-setup",
            "message": "Welcome back! Ready to set up your system?",
            "template": "startup_onboarding_incomplete"
        }

    elif status == "system_setup_complete":
        return {
            "action": "show_roadmap",
            "message": "Welcome back! Time to start your first build.",
            "template": "startup_system_ready"
        }

    elif status == "first_build_started":
        return {
            "action": "normal_menu",
            "template": None  # Use standard menu
        }

    # Fallback for old in-progress states (v4)
    elif status == "tour_in_progress":
        return {
            "action": "resume_skill",
            "skill": "how-nexus-works",
            "template": "compact_onboarding_resume"
        }

    elif status == "setup_in_progress":
        step = onboarding_state.get("complete_setup_state", {}).get("step_completed", 0)
        return {
            "action": "resume_skill",
            "skill": "complete-setup",
            "resume_from_step": step + 1,
            "template": "compact_onboarding_resume"
        }

    # Default fallback
    return {
        "action": "normal_menu",
        "template": None
    }


def determine_context_mode(source: str, transcript_path: str, build_dir: str, session_id: str = "") -> dict:
    """
    Determine context mode based on session source and build detection.

    Detection priority:
    1. session_id match in resume-context.md (exact, bulletproof)
    2. Transcript tool_use parsing (fallback)

    Returns dict with:
    - mode: "startup" | "compact"
    - build_id: str | None
    - phase: "planning" | "execution" | None
    - skill: "plan-build" | "execute-build" | None
    - action: "display_menu" | "continue_working"

    Cases:
    1. new → startup + display_menu
    2. compact + build + planning → compact + plan-build + continue
    3. compact + build + execution → compact + execute-build + continue
    4. compact + no_build → startup + continue_working
    5. resume + build + planning → compact + plan-build + continue
    6. resume + build + execution → compact + execute-build + continue
    7. resume + no_build → startup + display_menu (tries most recent first)

    NOTE: Once in a build, you STAY in build context. No skill switch detection.
    """
    # ✅ FIX: Validate source="compact" makes sense (defend against VSCode bugs)
    if source in ("compact", "resume"):
        if not transcript_path or transcript_path == "unknown":
            logging.warning(f"Source is '{source}' but no transcript path provided")
            logging.warning("Treating as new session")
            source = "new"
        elif not Path(transcript_path).exists():
            logging.warning(f"Source is '{source}' but transcript doesn't exist: {transcript_path}")
            logging.warning("Treating as new session")
            source = "new"

    # Rule 1: New session = STARTUP with menu
    if source == "new":
        logging.info("Case 1: new session → startup + display_menu")
        return {
            "mode": "startup",
            "build_id": None,
            "phase": None,
            "skill": None,
            "action": "display_menu"
        }

    # Rule 2: PRIMARY - Find build by session_id match (bulletproof)
    builds_path = str(Path(build_dir) / "02-builds" / "active")
    last_build = find_build_by_session_id(builds_path, session_id)

    # Rule 2b: FALLBACK - Parse transcript for tool_use patterns
    if not last_build:
        last_build, _ = parse_transcript_for_build(
            transcript_path,
            workspace_builds_dir=builds_path  # ✅ Validate against workspace
        )
        if last_build:
            logging.info(f"Fallback: found build {last_build} from transcript")

    # Rule 3: Compact without build = STARTUP + continue_working
    # NOTE: We no longer check for skill switches - once in a build, stay in build
    if source == "compact" and not last_build:
        logging.info("Case 5-6: compact + no_build → startup + continue_working")
        return {
            "mode": "startup",
            "build_id": None,
            "phase": None,
            "skill": None,
            "action": "continue_working"
        }

    # Rule 5: Resume without build = STARTUP with menu
    if source == "resume" and not last_build:
        # For resume, try most recent build by timestamp
        last_build = find_most_recent_build(build_dir)
        if not last_build:
            logging.info("Case 10: resume + no_build → startup + display_menu")
            return {
                "mode": "startup",
                "build_id": None,
                "phase": None,
                "skill": None,
                "action": "display_menu"
            }

    # Rule 6: Build work detected - determine phase
    if last_build:
        # ✅ FIX: Validate build exists in workspace (multi-window safety)
        # Check in active/ first, then complete/
        build_path = Path(build_dir) / "02-builds" / "active" / last_build
        if not build_path.exists():
            build_path = Path(build_dir) / "02-builds" / "complete" / last_build
        if not build_path.exists():
            logging.error("=" * 80)
            logging.error("BUILD NOT FOUND IN WORKSPACE")
            logging.error(f"  Build ID: {last_build}")
            logging.error(f"  Expected path: {build_path}")
            logging.error(f"  Workspace: {build_dir}")
            logging.error("  This is likely a cross-workspace contamination bug")
            logging.error("  Falling back to startup mode for safety")
            logging.error("=" * 80)
            return {
                "mode": "startup",
                "build_id": None,
                "phase": None,
                "skill": None,
                "action": "display_menu"
            }

        detected_skill = detect_build_phase(build_dir, last_build)
        phase = "planning" if detected_skill == "plan-build" else "execution"

        logging.info(f"Cases 2-3/7-9: {source} + build={last_build} + phase={phase} → compact + {detected_skill} + continue_working")
        return {
            "mode": "compact",
            "build_id": last_build,
            "phase": phase,
            "skill": detected_skill,
            "action": "continue_working"
        }

    # Fallback
    logging.info("Fallback: startup + display_menu")
    return {
        "mode": "startup",
        "build_id": None,
        "phase": None,
        "skill": None,
        "action": "display_menu"
    }


def find_most_recent_build(build_dir: str) -> str | None:
    """
    Find the most recently updated non-COMPLETE build for RESUME source.

    Uses build_state utility to filter by status (excludes COMPLETE by default).
    Falls back to legacy implementation if utility not available.

    Returns:
        Build ID or None if no builds found
    """
    # Try enhanced detection first
    try:
        from utils.build_state import find_most_recent_build_enhanced

        builds_dir = Path(build_dir) / "02-builds" / "active"

        if not builds_dir.exists():
            return None

        # Use enhanced detection (excludes COMPLETE builds)
        state = find_most_recent_build_enhanced(
            builds_dir,
            exclude_complete=True,
            exclude_archived=True
        )

        if state:
            build_folder = f"{state.build_id}-{state.name.lower().replace(' ', '-')}"
            logging.info(f"Most recent build: {build_folder} ({state.progress_percent}% complete, status={state.status})")
            return build_folder
        else:
            logging.info("No active builds found")
            return None

    except ImportError:
        # Fallback to legacy implementation
        logging.warning("build_state utility not available, using legacy most-recent detection")
        pass

    # Legacy fallback implementation
    builds_dir = Path(build_dir) / "02-builds" / "active"

    if not builds_dir.exists():
        return None

    most_recent_build = None
    most_recent_time = None

    for build_path in builds_dir.iterdir():
        if not build_path.is_dir():
            continue

        # Skip archived builds
        build_name = build_path.name
        if build_name.startswith("_") or build_name.startswith("."):
            continue

        # Check for resume-context.md
        resume_file = build_path / "01-planning" / "resume-context.md"
        if not resume_file.exists():
            continue

        try:
            content = resume_file.read_text(encoding="utf-8")

            # Extract last_updated from YAML frontmatter
            match = re.search(r'last_updated:\s*"([^"]+)"', content)
            if match:
                timestamp_str = match.group(1)
                # Parse ISO timestamp
                timestamp = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))

                if most_recent_time is None or timestamp > most_recent_time:
                    most_recent_time = timestamp
                    most_recent_build = build_name
        except Exception as e:
            logging.warning(f"Error reading resume-context.md for {build_name}: {e}")
            continue

    if most_recent_build:
        logging.info(f"Most recent build: {most_recent_build} (last_updated: {most_recent_time})")
    else:
        logging.info("No builds with resume-context.md found")

    return most_recent_build


def detect_build_phase(build_dir: str, build_id: str) -> str:
    """
    Detect planning vs execution phase with metadata-first approach.

    Priority:
    1. resume-context.md current_phase + next_action (explicit, authoritative)
    2. 04-steps.md Phase 1 checkbox analysis (fallback)

    Returns: "plan-build" or "execute-build"
    """
    # Import here to avoid circular dependency
    try:
        from utils.build_state import detect_phase_from_metadata

        # Check in active/ first, then complete/
        build_path = Path(build_dir) / "02-builds" / "active" / build_id
        if not build_path.exists():
            build_path = Path(build_dir) / "02-builds" / "complete" / build_id
        phase, skill = detect_phase_from_metadata(build_path)

        logging.info(f"Detected phase for {build_id}: {phase} → {skill}")
        return skill

    except ImportError:
        # Fallback to legacy logic if utils not available
        logging.warning("build_state utility not available, using legacy phase detection")
        pass

    # Legacy fallback implementation - check active/ first, then complete/
    steps_file = Path(build_dir) / "02-builds" / "active" / build_id / "01-planning" / "04-steps.md"
    if not steps_file.exists():
        steps_file = Path(build_dir) / "02-builds" / "complete" / build_id / "01-planning" / "04-steps.md"

    if not steps_file.exists():
        logging.info(f"No 04-steps.md found for {build_id} - defaulting to plan-build")
        return "plan-build"

    try:
        content = steps_file.read_text(encoding='utf-8')

        # Find Phase 1 section (stops at Phase 2 or end of file)
        phase1_match = re.search(r'## Phase 1[^\n]*\n(.*?)(?=\n## Phase 2|\n## Phase|\Z)', content, re.DOTALL)
        if not phase1_match:
            logging.info(f"No Phase 1 section found in {build_id}/04-steps.md - defaulting to plan-build")
            return "plan-build"

        phase1_content = phase1_match.group(1)

        # Count checkboxes in Phase 1
        total_tasks = len(re.findall(r'- \[[ x]\]', phase1_content))
        completed_tasks = len(re.findall(r'- \[x\]', phase1_content))

        logging.info(f"Phase 1 progress for {build_id}: {completed_tasks}/{total_tasks} tasks complete")

        if total_tasks > 0 and completed_tasks == total_tasks:
            logging.info(f"Phase 1 COMPLETE for {build_id} - using execute-build")
            return "execute-build"

        logging.info(f"Phase 1 INCOMPLETE for {build_id} - using plan-build")
        return "plan-build"

    except Exception as e:
        logging.error(f"Error detecting phase for {build_id}: {e}")
        return "plan-build"


def load_resume_context(build_dir: str, build_id: str) -> dict | None:
    """
    Load resume-context.md from detected build.

    Checks both new name (resume-context.md) and legacy name (_resume.md)
    for backward compatibility during migration.

    Returns:
        Dict with files_to_load list or None if file doesn't exist/invalid
    """
    # Check in active/ first, then complete/
    build_path = Path(build_dir) / "02-builds" / "active" / build_id / "01-planning"
    if not build_path.exists():
        build_path = Path(build_dir) / "02-builds" / "complete" / build_id / "01-planning"

    # Check new name first
    new_file = build_path / "resume-context.md"
    old_file = build_path / "_resume.md"

    resume_file = new_file if new_file.exists() else (old_file if old_file.exists() else None)

    if not resume_file:
        logging.info(f"No resume file found for build {build_id}")
        return None

    try:
        content = resume_file.read_text(encoding="utf-8")

        # Extract files_to_load from YAML frontmatter
        # Supports both inline [a, b] and multiline list formats
        files_to_load = []

        # Try inline format: files_to_load: [file1, file2]
        inline_match = re.search(r'files_to_load:\s*\[([^\]]*)\]', content)
        if inline_match:
            list_content = inline_match.group(1).strip()
            if list_content:
                files_to_load = [item.strip().strip('"').strip("'") for item in list_content.split(",")]
        else:
            # Try multiline format:
            # files_to_load:
            #   - file1
            #   - file2
            multiline_match = re.search(r'files_to_load:\s*\n((?:\s*-\s*.+\n?)+)', content)
            if multiline_match:
                list_block = multiline_match.group(1)
                files_to_load = [
                    line.strip()[2:].strip().strip('"').strip("'")
                    for line in list_block.split("\n")
                    if line.strip().startswith("- ")
                ]

        return {"files_to_load": files_to_load}

    except Exception as e:
        logging.error(f"Failed to parse resume file {resume_file}: {e}")
        return None


# ============================================================================
# Template Loader
# ============================================================================

def load_instruction_template(name: str, **kwargs) -> str:
    """
    Load instruction template from .md file and format with kwargs.

    Args:
        name: Template name (without .md extension)
        **kwargs: Format variables (build_id, current_task, etc.)

    Returns:
        Formatted template content
    """
    template_path = Path(__file__).parent / "templates" / f"{name}.md"
    try:
        template = template_path.read_text(encoding='utf-8')
        return template.format(**kwargs) if kwargs else template
    except FileNotFoundError:
        logging.error(f"Template not found: {template_path}")
        return f"Template {name} not found"
    except KeyError as e:
        logging.error(f"Missing template variable: {e}")
        return template_path.read_text(encoding='utf-8')  # Return unformatted


# ============================================================================
# XML Context Builders (Phase 3 - XML Context Restructure)
# ============================================================================

def build_startup_xml(build_dir: str, session_id: str, source: str, action: str = "display_menu") -> tuple:
    """
    Build complete STARTUP mode XML context.

    STARTUP mode is for:
    - Fresh sessions (source="new")
    - Non-build continuations (compact/resume without active build)

    Token target: ~20K max

    Args:
        build_dir: Root build directory
        session_id: Current session UUID
        source: Session source (new|compact|resume)
        action: "display_menu" or "continue_working"

    Returns:
        Tuple of (xml_string, state_metadata_dict)
    """
    base_path = Path(build_dir)
    timestamp = datetime.now().isoformat()

    # Load required data
    try:
        # Add nexus core to path for loaders
        nexus_core = base_path / "00-system" / "core"
        if str(nexus_core) not in sys.path:
            sys.path.insert(0, str(nexus_core))

        from nexus.loaders import scan_builds, build_skills_xml_compact, load_full_startup_context, build_next_action_instruction, detect_configured_integrations
        from nexus.state import (
            build_pending_onboarding,
            extract_learning_completed,
        )
    except ImportError as e:
        logging.error(f"Failed to import nexus modules: {e}")
        logging.error(f"Attempted workspace: {build_dir}")
        logging.error(f"Nexus core path: {nexus_core}")
        logging.error(f"Nexus core exists: {nexus_core.exists()}")

        # Return minimal fallback XML (must return tuple!)
        fallback_xml = f"""<nexus-context version="v4" mode="startup">
  <session id="{escape_xml_attribute(session_id)}" source="{escape_xml_attribute(source)}" timestamp="{timestamp}"/>
  <error>
[ERROR] NEXUS NOT FOUND

VSCode opened in wrong workspace.

Expected: Nexus instance root (with 00-system/, 01-memory/, etc.)
Got: {escape_xml_content(str(base_path))}
Looking for: {escape_xml_content(str(nexus_core))}
Exists: {nexus_core.exists()}

Fix: Open VSCode in the correct Nexus workspace folder.
  </error>
  <instruction importance="MANDATORY">
Tell the user to open VSCode in the correct Nexus workspace folder (the directory containing 00-system/, 01-memory/, 02-builds/, etc.).

Current directory: {escape_xml_content(str(base_path))}
  </instruction>
</nexus-context>"""
        return fallback_xml, {}

    # User config path (used for both preferences and onboarding state)
    config_path = base_path / "01-memory" / "user-config.yaml"

    # Migrate config schema if needed (v4 → v5)
    try:
        from nexus.migrate import migrate_if_needed
        migrate_if_needed(config_path, create_backup=True)
    except Exception as e:
        logging.warning(f"Config migration skipped: {e}")

    # Extract onboarding state for cross-session continuity
    onboarding_state = extract_onboarding_state(config_path)
    onboarding_action = determine_onboarding_action(source, onboarding_state, build_dir)

    logging.info(f"Onboarding action: {onboarding_action.get('action')}, skill={onboarding_action.get('skill')}")

    # Build XML parts
    xml_parts = []

    # Header comment
    xml_parts.append(f'''<nexus-context version="v4" mode="startup">
<!--
================================================================================
NEXUS OPERATING SYSTEM - PRIMARY CONTEXT INJECTION
================================================================================
This is the HYPER IMPORTANT primary working mode of Claude Code operating
inside the NEXUS system. All routing decisions, skill loading, and build
management flows through this context.

MODE: startup ({source} session)
ACTION: {action}
ONBOARDING: {onboarding_state.get("status", "not_started")}
================================================================================
-->

  <session id="{escape_xml_attribute(session_id)}" source="{escape_xml_attribute(source)}" timestamp="{timestamp}"/>''')

    # User preferences (language, timezone) - CRITICAL for non-English users
    user_prefs = extract_user_preferences(config_path)

    if user_prefs["language"]:
        xml_parts.append(f'''
  <user-preferences>
    <language importance="CRITICAL">{escape_xml_content(user_prefs["language"])}</language>
    <instruction>You MUST respond in {escape_xml_content(user_prefs["language"])} for ALL communication with the user.</instruction>
  </user-preferences>''')
    if user_prefs["timezone"]:
        xml_parts.append(f'''    <timezone>{escape_xml_content(user_prefs["timezone"])}</timezone>''')

    # Orchestrator content
    orchestrator_path = base_path / "00-system" / "core" / "orchestrator.md"
    orchestrator_xml = load_file_to_xml(orchestrator_path, "orchestrator-file", "00-system/core/orchestrator.md", indent=2)
    if orchestrator_xml:
        xml_parts.append(f'\n{orchestrator_xml}')

    # System maps (orientation for new sessions)
    system_maps = [
        ("00-system/system-map.md", "Folder structure and execution flow"),
        ("01-memory/memory-map.md", "Memory persistence layer"),
        ("04-workspace/workspace-map.md", "User workspace organization"),
    ]
    for map_file, description in system_maps:
        full_path = base_path / map_file
        map_xml = load_file_to_xml(full_path, "map-file", map_file, indent=2)
        if map_xml:
            xml_parts.append(f'\n{map_xml}')

    # User goals
    goals_path = base_path / "01-memory" / "goals.md"
    if goals_path.exists():
        goals_content = escape_xml_content(goals_path.read_text(encoding='utf-8'))
        xml_parts.append(f'''
  <user-goals>
{goals_content}
  </user-goals>''')

    # Active builds (include ACTIVE for backwards compatibility with older builds)
    all_builds = scan_builds(str(base_path), minimal=True)
    active_builds = [p for p in all_builds if p.get("status") in ("IN_PROGRESS", "PLANNING", "ACTIVE")]

    xml_parts.append('\n  <active-builds>')
    for proj in active_builds:
        proj_id = escape_xml_attribute(str(proj.get("id", "")))
        proj_name = escape_xml_content(str(proj.get("name", "")))
        proj_status = escape_xml_attribute(str(proj.get("status", "")))
        proj_progress = proj.get("progress", 0)
        proj_task = escape_xml_content(str(proj.get("current_task", "")))
        xml_parts.append(f'''    <build id="{proj_id}" status="{proj_status}" progress="{proj_progress}">
      <name>{proj_name}</name>
      <current-task>{proj_task}</current-task>
    </build>''')
    xml_parts.append('  </active-builds>')

    # Skills (from build_skills_xml_compact - CLI discovery pattern)
    skills_xml = build_skills_xml_compact(str(base_path))
    xml_parts.append(f'\n{skills_xml}')

    # State detection - SINGLE SOURCE OF TRUTH: learning_tracker.completed
    # Refactored 2026-01-18: Use learning_tracker instead of check_* functions
    from nexus.utils import is_template_file
    import hashlib

    config_path = base_path / "01-memory" / "user-config.yaml"
    learning_completed = extract_learning_completed(config_path)

    # Derive state from learning_tracker (single source of truth)
    goals_personalized = learning_completed.get("setup_memory", False)
    workspace_configured = learning_completed.get("create_folders", False)

    # Keep template checks for debug logging only (not for state)
    goals_is_template = is_template_file(str(goals_path))
    workspace_map_path = base_path / "04-workspace" / "workspace-map.md"
    workspace_is_template = is_template_file(str(workspace_map_path))

    logging.info(f"State detection: goals_path={goals_path}, exists={goals_path.exists()}")
    logging.info(f"State detection: goals_personalized={goals_personalized} (from learning_tracker.setup_memory)")
    logging.info(f"State detection: goals_is_template={goals_is_template} (debug only)")
    logging.info(f"State detection: workspace_map_path={workspace_map_path}, exists={workspace_map_path.exists()}")
    logging.info(f"State detection: workspace_configured={workspace_configured} (from learning_tracker.create_folders)")
    logging.info(f"State detection: workspace_is_template={workspace_is_template} (debug only)")
    pending_onboarding = build_pending_onboarding(learning_completed)

    logging.info(f"State detection: pending_onboarding count={len(pending_onboarding)}")

    onboarding_complete = len(pending_onboarding) == 0

    # Generate state hash for tamper detection
    state_str = f"goals={goals_personalized}|workspace={workspace_configured}|onboarding={onboarding_complete}"
    state_hash = hashlib.md5(state_str.encode()).hexdigest()[:8]

    xml_parts.append(f'''
  <state hash="{state_hash}">
    <goals-personalized>{str(goals_personalized).lower()}</goals-personalized>
    <workspace-configured>{str(workspace_configured).lower()}</workspace-configured>
    <onboarding-complete>{str(onboarding_complete).lower()}</onboarding-complete>''')

    if pending_onboarding:
        xml_parts.append('    <pending-onboarding>')
        for item in pending_onboarding:
            # item is a dict with keys: key, name, trigger, priority, time
            item_name = escape_xml_attribute(str(item.get("name", "")))
            item_trigger = escape_xml_attribute(str(item.get("trigger", "")))
            item_time = escape_xml_attribute(str(item.get("time", "")))
            xml_parts.append(f'      <item name="{item_name}" trigger="{item_trigger}" time="{item_time}"/>')
        xml_parts.append('    </pending-onboarding>')

    xml_parts.append('  </state>')

    # Stats
    total_skills = len([s for s in scan_builds(str(base_path), minimal=True)])  # Approximate
    xml_parts.append(f'''
  <stats builds="{len(all_builds)}" active="{len(active_builds)}" skills="50"/>''')

    # Action and instruction
    xml_parts.append(f'''
  <action>{action}</action>''')

    # Extract user role from goals.md for menu display
    user_role = ""
    if goals_path.exists():
        try:
            goals_text = goals_path.read_text(encoding='utf-8')
            role_match = re.search(r'## Current Role\s*\n+([^\n#]+)', goals_text)
            if role_match:
                user_role = role_match.group(1).strip()
        except Exception:
            pass

    # Detect configured integrations (safe - returns [] on error)
    try:
        all_integrations = detect_configured_integrations(str(base_path))
        configured_integrations = [i["name"] for i in all_integrations if i.get("active")]
    except Exception:
        configured_integrations = []

    # Build context for MECE state templates
    mece_context = {
        "pending_onboarding": pending_onboarding,
        "active_builds": active_builds,
        "workspace_needs_validation": False,
        "total_builds": len(all_builds),
        "goals_personalized": goals_personalized,
        "workspace_configured": workspace_configured,
        "user_role": user_role,
        "configured_integrations": configured_integrations,
        # New onboarding state (v5)
        "onboarding_state": onboarding_state,
        "onboarding_action": onboarding_action,
        "session_source": source,
    }

    # Use MECE state templates for dynamic instruction generation
    instruction_content = build_next_action_instruction(mece_context)

    xml_parts.append(f'''
  <instruction importance="MANDATORY">
{instruction_content}
  </instruction>''')

    xml_parts.append('\n</nexus-context>')

    # Return XML and state metadata for debugging
    state_metadata = {
        "state_hash": state_hash,
        "goals_personalized": goals_personalized,
        "goals_is_template": goals_is_template,
        "goals_path": str(goals_path.resolve()),
        "workspace_configured": workspace_configured,
        "workspace_is_template": workspace_is_template,
        "workspace_path": str(workspace_map_path.resolve()),
        "onboarding_complete": onboarding_complete,
        "pending_onboarding_count": len(pending_onboarding),
        "build_dir": build_dir,
    }

    return '\n'.join(xml_parts), state_metadata


def build_compact_xml(build_dir: str, session_id: str, source: str, mode_result: dict) -> str:
    """
    Build complete COMPACT mode XML context for build continuation.

    COMPACT mode is for:
    - Build work continuation after auto-summary
    - Resume with active build

    Token target: ~10K max

    Args:
        build_dir: Root build directory
        session_id: Current session UUID
        source: Session source (compact|resume)
        mode_result: Dict from determine_context_mode() with build_id, phase, skill

    Returns:
        Complete XML context string
    """
    base_path = Path(build_dir)
    timestamp = datetime.now().isoformat()

    build_id = mode_result.get("build_id", "")
    phase = mode_result.get("phase", "execution")
    skill = mode_result.get("skill", "execute-build")

    # Check in active/ first, then complete/
    build_path = base_path / "02-builds" / "active" / build_id
    if not build_path.exists():
        build_path = base_path / "02-builds" / "complete" / build_id

    # Load resume-context for files_to_load
    resume_metadata = load_resume_context(build_dir, build_id)
    files_to_load = resume_metadata.get("files_to_load", []) if resume_metadata else []

    # Fallback: if resume-context has no files_to_load, use defaults for execution
    if not files_to_load and phase == "execution":
        files_to_load = ["01-planning/01-overview.md", "01-planning/04-steps.md"]

    # Get current task from 04-steps.md
    current_task = ""
    completed = 0
    total = 0
    steps_file = build_path / "01-planning" / "04-steps.md"
    if steps_file.exists():
        try:
            content = steps_file.read_text(encoding='utf-8')
            # Count checkboxes
            total = len(re.findall(r'- \[[ x]\]', content))
            completed = len(re.findall(r'- \[x\]', content))
            # Find first unchecked
            match = re.search(r'- \[ \] (.+)', content)
            if match:
                current_task = match.group(1).strip()
        except Exception as e:
            logging.error(f"Error reading 04-steps.md: {e}")

    # Build XML
    xml_parts = []

    # Header comment
    xml_parts.append(f'''<nexus-context version="v4" mode="compact">
<!--
================================================================================
NEXUS OPERATING SYSTEM - BUILD CONTINUATION CONTEXT
================================================================================
This is the HYPER IMPORTANT build continuation mode of Claude Code operating
inside the NEXUS system. User was actively working on a build in the previous
session - load full context and continue.

MODE: compact (continuing build work after auto-summary)
BUILD: {build_id}
PHASE: {phase}
SKILL: {skill}
================================================================================
-->

  <session id="{escape_xml_attribute(session_id)}" source="{escape_xml_attribute(source)}" timestamp="{timestamp}"/>

  <resume-build id="{escape_xml_attribute(build_id)}" phase="{escape_xml_attribute(phase)}">
    <skill>{escape_xml_content(skill)}</skill>
    <current-task>{escape_xml_content(current_task)}</current-task>
    <progress>{completed}/{total} tasks</progress>
  </resume-build>''')

    # User preferences (language, timezone) - CRITICAL for non-English users
    config_path = base_path / "01-memory" / "user-config.yaml"
    user_prefs = extract_user_preferences(config_path)

    if user_prefs["language"]:
        xml_parts.append(f'''
  <user-preferences>
    <language importance="CRITICAL">{escape_xml_content(user_prefs["language"])}</language>
    <instruction>You MUST respond in {escape_xml_content(user_prefs["language"])} for ALL communication with the user.</instruction>
  </user-preferences>''')

    # System files (focused for build work)
    system_files = [
        ("00-system/core/orchestrator.md", "AI behavior rules, routing, menu display"),
        ("00-system/system-map.md", "Folder structure for file operations"),
        ("04-workspace/workspace-map.md", "User context and projects"),
    ]

    xml_parts.append('\n  <system-files>')
    for sys_file, description in system_files:
        full_path = base_path / sys_file
        xml = load_file_to_xml(full_path, "file", sys_file, indent=4)
        if xml:
            xml_parts.append(xml)
    xml_parts.append('  </system-files>')

    # User goals (may have been updated during build work)
    goals_path = base_path / "01-memory" / "goals.md"
    if goals_path.exists():
        goals_content = escape_xml_content(goals_path.read_text(encoding='utf-8'))
        xml_parts.append(f'''
  <user-goals>
{goals_content}
  </user-goals>''')

    # Build files
    xml_parts.append(f'\n  <build-files build-id="{escape_xml_attribute(build_id)}">')
    for file_path in files_to_load:
        full_path = build_path / file_path
        xml = load_file_to_xml(full_path, "file", file_path, indent=4)
        if xml:
            xml_parts.append(xml)
    xml_parts.append('  </build-files>')

    # Skill file
    skill_paths = {
        "plan-build": "00-system/skills/builds/plan-build/SKILL.md",
        "execute-build": "00-system/skills/builds/execute-build/SKILL.md",
    }
    skill_path = skill_paths.get(skill, f"00-system/skills/builds/{skill}/SKILL.md")
    skill_file = base_path / skill_path
    skill_xml = load_file_to_xml(skill_file, "skill-file", skill_path, indent=2)
    if skill_xml:
        xml_parts.append(f'\n{skill_xml}')

    # Action and instruction
    xml_parts.append('''
  <action>continue_working</action>''')

    # Load instruction template based on phase
    escaped_task = escape_xml_content(current_task)
    if phase == "planning":
        instruction_content = load_instruction_template(
            "compact_planning",
            build_id=build_id,
            current_task=escaped_task
        )
    else:
        instruction_content = load_instruction_template(
            "compact_execution",
            build_id=build_id,
            current_task=escaped_task
        )

    xml_parts.append(f'''
  <instruction importance="MANDATORY">
{instruction_content}
  </instruction>''')

    xml_parts.append('\n</nexus-context>')

    return '\n'.join(xml_parts)


def derive_workspace_from_transcript(transcript_path: str) -> str:
    """
    Derive workspace root from transcript path.

    Transcript is typically at:
    {workspace}/.claude/transcripts/{session_id}.jsonl

    Extract {workspace} from this path.
    """
    if not transcript_path or transcript_path == "unknown":
        return ""

    try:
        transcript = Path(transcript_path).resolve()

        # Look for .claude directory in parents
        current = transcript.parent
        while current != current.parent:
            if current.name == ".claude":
                # Workspace is parent of .claude
                return str(current.parent)
            current = current.parent
    except Exception as e:
        logging.warning(f"Failed to derive workspace from transcript: {e}")

    return ""


def determine_workspace_root(input_data: dict) -> str:
    """
    Determine workspace root with fallback chain.

    Priority:
    0. Hook file location (MOST RELIABLE - hook is always at .claude/hooks/)
    1. workspace_root from VSCode (if available in future)
    2. Derive from transcript_path (multi-window safe)
    3. CLAUDE_PROJECT_DIR env var
    4. Current working directory (LEAST RELIABLE)
    """
    # Priority 0: Hook file location (hook is at .claude/hooks/session_start.py)
    # Workspace is 2 levels up: .claude/hooks/ -> .claude/ -> workspace/
    hook_file = Path(__file__).resolve()
    workspace_from_hook = hook_file.parent.parent.parent

    # Validate it looks like a Nexus instance (has 00-system/)
    if (workspace_from_hook / "00-system").exists():
        logging.info(f"Using workspace from hook location: {workspace_from_hook}")
        return str(workspace_from_hook)
    else:
        logging.warning(f"Hook location doesn't look like Nexus: {workspace_from_hook}")

    # Priority 1: Direct from VSCode (future enhancement)
    workspace = input_data.get("workspace_root", "")
    if workspace and Path(workspace).exists():
        logging.info(f"Using workspace from VSCode: {workspace}")
        return workspace

    # Priority 2: Derive from transcript (BEST for multi-window)
    transcript_path = input_data.get("transcript_path", "")
    if transcript_path:
        workspace = derive_workspace_from_transcript(transcript_path)
        if workspace and Path(workspace).exists():
            logging.info(f"Derived workspace from transcript: {workspace}")
            return workspace

    # Priority 3: Environment variable
    workspace = os.environ.get("CLAUDE_PROJECT_DIR", "") or os.environ.get("CLAUDE_BUILD_DIR", "")
    if workspace and Path(workspace).exists():
        logging.info(f"Using workspace from env var: {workspace}")
        return workspace

    # Priority 4: Current working directory (LEAST RELIABLE)
    workspace = str(Path.cwd())
    logging.warning(f"Falling back to current working directory: {workspace}")
    return workspace


def main():
    try:
        input_data = json.load(sys.stdin)
        session_id = input_data.get("session_id", "unknown")
        source = input_data.get("source", "startup")
        transcript_path = input_data.get("transcript_path", "unknown")

        # ✅ FIX: Use multi-window safe workspace detection
        build_dir = determine_workspace_root(input_data)

        # Validate workspace exists and is a Nexus instance
        if not build_dir:
            logging.error("Could not determine workspace root - using fallback mode")
            build_dir = str(Path.cwd())

        workspace_path = Path(build_dir)
        if not workspace_path.exists():
            logging.error(f"Workspace directory doesn't exist: {build_dir}")
            # Return minimal startup context
            source = "new"

        # Validate transcript belongs to this workspace (multi-window safety)
        if transcript_path and transcript_path != "unknown":
            transcript_file = Path(transcript_path).resolve()
            expected_transcript_dir = workspace_path / ".claude" / "transcripts"

            try:
                if not transcript_file.is_relative_to(expected_transcript_dir):
                    logging.error("=" * 80)
                    logging.error("WORKSPACE MISMATCH DETECTED (multi-window)")
                    logging.error(f"  Transcript: {transcript_file}")
                    logging.error(f"  Expected in: {expected_transcript_dir}")
                    logging.error(f"  Workspace: {workspace_path}")
                    logging.error("  This usually means VSCode passed wrong transcript path")
                    logging.error("  Forcing new session mode for safety")
                    logging.error("=" * 80)
                    source = "new"  # Force startup mode
            except (ValueError, AttributeError):
                # is_relative_to might fail on older Python or cross-drive paths
                logging.warning("Could not validate transcript path - proceeding with caution")

        # 1. Write session ID to session-specific file for tracking
        if session_id != "unknown":
            try:
                import hashlib
                session_hash = hashlib.md5(session_id.encode()).hexdigest()[:8]
                sessions_dir = Path(__file__).parent.parent / "sessions"
                sessions_dir.mkdir(exist_ok=True)
                session_file = sessions_dir / f"{session_hash}.session"
                session_file.write_text(session_id)
            except Exception:
                pass

        # =======================================================================
        # NEW XML CONTEXT INJECTION (Build 30 - XML Context Restructure)
        # =======================================================================
        # Uses determine_context_mode() to detect STARTUP vs COMPACT mode
        # Then calls appropriate XML builder function
        # =======================================================================

        # 2. Determine context mode using transcript analysis
        mode_result = determine_context_mode(source, transcript_path, build_dir, session_id)
        mode = mode_result.get("mode", "startup")
        action = mode_result.get("action", "display_menu")

        logging.info(f"Context mode determined: mode={mode}, action={action}, build={mode_result.get('build_id')}")

        # 3. Build XML context based on mode
        state_metadata = None  # Only populated for startup mode
        if mode == "compact" and mode_result.get("build_id"):
            # COMPACT mode: Build continuation with full context
            additional_context_str = build_compact_xml(build_dir, session_id, source, mode_result)
            logging.info(f"Built COMPACT XML context ({len(additional_context_str)} chars)")
        else:
            # STARTUP mode: Full menu with all skills and builds
            additional_context_str, state_metadata = build_startup_xml(build_dir, session_id, source, action)
            logging.info(f"Built STARTUP XML context ({len(additional_context_str)} chars)")

        # 4. Output as proper hook response with additionalContext
        hook_output: dict = {
            "hookSpecificOutput": {
                "hookEventName": "SessionStart",
                "additionalContext": additional_context_str
            }
        }

        # systemMessage shown to user in UI
        build_id = mode_result.get("build_id")
        if mode == "compact" and build_id:
            phase = mode_result.get("phase", "execution")
            hook_output["systemMessage"] = f"SessionStart:{mode} hook success: Resumed {build_id} ({phase})"
        else:
            hook_output["systemMessage"] = f"SessionStart:{mode} hook success: Success"

        # 5. Performance check
        elapsed_ms = (time.perf_counter() - START_TIME) * 1000
        if elapsed_ms > 200:
            logging.warning(f"SessionStart hook exceeded 200ms budget: {elapsed_ms:.2f}ms")
        else:
            logging.info(f"SessionStart hook completed in {elapsed_ms:.2f}ms")

        print(json.dumps(hook_output), flush=True)

        # 6. Log output to file for debugging
        if build_dir:
            try:
                cache_dir = Path(build_dir) / "00-system" / ".cache"
                cache_dir.mkdir(parents=True, exist_ok=True)

                # Summary log
                log_path = cache_dir / "session_start_output.log"
                with open(log_path, "w", encoding="utf-8") as f:
                    f.write(f"=== SessionStart Hook Output (XML Context v1.0) ===\n")
                    f.write(f"Timestamp: {datetime.now().isoformat()}\n")
                    f.write(f"Session: {session_id}\n")
                    f.write(f"Source: {source}\n")
                    f.write(f"Mode: {mode}\n")
                    f.write(f"Action: {action}\n")
                    f.write(f"Build: {build_id or 'None'}\n")
                    f.write(f"Phase: {mode_result.get('phase', 'N/A')}\n")
                    f.write(f"Skill: {mode_result.get('skill', 'N/A')}\n")
                    f.write(f"Performance: {elapsed_ms:.2f}ms\n")
                    f.write(f"XML Size: {len(additional_context_str):,} chars\n")
                    f.write(f"Estimated Tokens: {int(len(additional_context_str) / 4):,}\n")
                    f.write(f"---\n")

                # Full XML context dump
                xml_dump_path = cache_dir / "session_start_context.xml"
                with open(xml_dump_path, "w", encoding="utf-8") as f:
                    f.write(additional_context_str)

                # Timestamped state log (append-only for debugging stale context issues)
                if state_metadata:
                    state_log_path = cache_dir / "session_state_history.log"
                    with open(state_log_path, "a", encoding="utf-8") as f:
                        f.write(f"\n--- {datetime.now().isoformat()} | session={session_id} ---\n")
                        f.write(f"build_dir={state_metadata.get('build_dir', 'unknown')}\n")
                        f.write(f"state_hash={state_metadata['state_hash']}\n")
                        f.write(f"goals_path={state_metadata.get('goals_path', 'unknown')}\n")
                        f.write(f"goals_personalized={state_metadata['goals_personalized']} (is_template={state_metadata['goals_is_template']})\n")
                        f.write(f"workspace_path={state_metadata.get('workspace_path', 'unknown')}\n")
                        f.write(f"workspace_configured={state_metadata['workspace_configured']} (is_template={state_metadata['workspace_is_template']})\n")
                        f.write(f"onboarding_complete={state_metadata['onboarding_complete']}\n")
                        f.write(f"pending_onboarding_count={state_metadata['pending_onboarding_count']}\n")

                # Token estimation report
                estimated_tokens = len(additional_context_str) / 4
                token_report_path = cache_dir / "session_start_tokens.txt"
                with open(token_report_path, "w", encoding="utf-8") as f:
                    f.write(f"=== SessionStart XML Context Token Analysis ===\n")
                    f.write(f"Timestamp: {datetime.now().isoformat()}\n")
                    f.write(f"Session: {session_id}\n")
                    f.write(f"Source: {source}\n")
                    f.write(f"Mode: {mode}\n\n")
                    f.write(f"Total Characters: {len(additional_context_str):,}\n")
                    f.write(f"Estimated Tokens: {int(estimated_tokens):,} (~4 chars/token)\n\n")
                    target_tokens = 20000 if mode == "startup" else 10000
                    f.write(f"Target: {target_tokens:,} tokens\n")
                    if estimated_tokens > target_tokens:
                        f.write(f"[!]  OVER TARGET by {int(estimated_tokens - target_tokens):,} tokens\n")
                    else:
                        f.write(f"[OK] Within target ({int(target_tokens - estimated_tokens):,} tokens headroom)\n")
            except Exception:
                pass

        sys.exit(0)

    except json.JSONDecodeError:
        sys.exit(0)
    except Exception as e:
        # Fallback: output minimal XML context even on error
        fallback_xml = f"""<nexus-context version="v4" mode="fallback">
  <error>{escape_xml_content(str(e))}</error>
  <instruction importance="MANDATORY">
    Read 00-system/core/orchestrator.md and display menu.
    Error occurred during context loading: {escape_xml_content(str(e))}
  </instruction>
</nexus-context>"""
        fallback = {
            "hookSpecificOutput": {
                "hookEventName": "SessionStart",
                "additionalContext": fallback_xml
            }
        }
        print(json.dumps(fallback), flush=True)
        sys.exit(0)


if __name__ == "__main__":
    main()
