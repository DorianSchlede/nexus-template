#!/usr/bin/env python3
from __future__ import annotations
"""
SessionStart Hook - MVC v3.2 + Resume Enhancement (Minimum Viable Context)

ZERO DEPENDENCIES. No yaml. No loaders.py. Just stdlib.

Key changes in v3.2:
- Skill priority CORRECTED: 00-system/skills/ > 03-skills/
- Extended never_do rules from create-skill
- Plan/Execute mode rules added
- Routing: Skill -> Integration -> Build

Phase 2 Resume Enhancement:
- Reads precompact_state.json (FLAT schema) from PreCompact hook
- Loads resume-context.md from detected build
- Injects catastrophic loading instructions via additionalContext
- Performance target: <200ms execution time

Triggered by Claude Code on:
- New session start (source=startup)
- Session resume (source=resume) - NOW WITH AUTO-RESUME
- After /clear command (source=clear) - EXCLUDED from auto-resume
- After compaction (source=compact) - NOW WITH AUTO-RESUME
"""

import json
import sys
import os
import re
import time
import logging
from pathlib import Path
from datetime import datetime

# Performance tracking
START_TIME = time.perf_counter()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - SessionStart - %(levelname)s - %(message)s'
)

# Add parent directory to path for utils imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.http import send_to_server
from utils.server import ensure_server_running
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
    builds_path = str(Path(build_dir) / "02-builds")
    last_build = find_build_by_session_id(builds_path, session_id)

    # Rule 2b: FALLBACK - Parse transcript for tool_use patterns
    if not last_build:
        last_build, _ = parse_transcript_for_build(transcript_path)
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

        builds_dir = Path(build_dir) / "02-builds"

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
    builds_dir = Path(build_dir) / "02-builds"

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

        build_path = Path(build_dir) / "02-builds" / build_id
        phase, skill = detect_phase_from_metadata(build_path)

        logging.info(f"Detected phase for {build_id}: {phase} → {skill}")
        return skill

    except ImportError:
        # Fallback to legacy logic if utils not available
        logging.warning("build_state utility not available, using legacy phase detection")
        pass

    # Legacy fallback implementation
    steps_file = Path(build_dir) / "02-builds" / build_id / "01-planning" / "04-steps.md"

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
    build_path = Path(build_dir) / "02-builds" / build_id / "01-planning"

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

def build_startup_xml(build_dir: str, session_id: str, source: str, action: str = "display_menu") -> str:
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
        Complete XML context string
    """
    base_path = Path(build_dir)
    timestamp = datetime.now().isoformat()

    # Load required data
    try:
        # Add nexus core to path for loaders
        nexus_core = base_path / "00-system" / "core"
        if str(nexus_core) not in sys.path:
            sys.path.insert(0, str(nexus_core))

        from nexus.loaders import scan_builds, build_skills_xml_compact, load_full_startup_context, build_next_action_instruction
        from nexus.state import (
            check_goals_personalized,
            check_workspace_configured,
            build_pending_onboarding,
            extract_learning_completed,
        )
    except ImportError as e:
        logging.error(f"Failed to import nexus modules: {e}")
        # Return minimal fallback XML
        return f"""<nexus-context version="v4" mode="startup">
  <session id="{escape_xml_attribute(session_id)}" source="{escape_xml_attribute(source)}" timestamp="{timestamp}"/>
  <error>Failed to load nexus modules: {escape_xml_content(str(e))}</error>
  <instruction importance="MANDATORY">
    Read 00-system/core/orchestrator.md and display menu.
  </instruction>
</nexus-context>"""

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
================================================================================
-->

  <session id="{escape_xml_attribute(session_id)}" source="{escape_xml_attribute(source)}" timestamp="{timestamp}"/>''')

    # User preferences (language, timezone) - CRITICAL for non-English users
    config_path = base_path / "01-memory" / "user-config.yaml"
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

    # State detection with detailed logging
    from nexus.utils import is_template_file

    goals_is_template = is_template_file(str(goals_path))
    goals_personalized = check_goals_personalized(goals_path)

    workspace_map_path = base_path / "04-workspace" / "workspace-map.md"
    workspace_is_template = is_template_file(str(workspace_map_path))
    workspace_configured = check_workspace_configured(base_path)

    logging.info(f"State detection: goals_path={goals_path}, exists={goals_path.exists()}")
    logging.info(f"State detection: goals_is_template={goals_is_template}, goals_personalized={goals_personalized}")
    logging.info(f"State detection: workspace_map_path={workspace_map_path}, exists={workspace_map_path.exists()}")
    logging.info(f"State detection: workspace_is_template={workspace_is_template}, workspace_configured={workspace_configured}")

    config_path = base_path / "01-memory" / "user-config.yaml"
    learning_completed = extract_learning_completed(config_path)
    pending_onboarding = build_pending_onboarding(learning_completed)

    logging.info(f"State detection: pending_onboarding count={len(pending_onboarding)}")

    onboarding_complete = len(pending_onboarding) == 0

    xml_parts.append(f'''
  <state>
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

    # Build context for MECE state templates
    mece_context = {
        "pending_onboarding": pending_onboarding,
        "active_builds": active_builds,
        "workspace_needs_validation": False,  # TODO: detect workspace changes
        "total_builds": len(all_builds),
        "goals_personalized": goals_personalized,
    }

    # Use MECE state templates for dynamic instruction generation
    instruction_content = build_next_action_instruction(mece_context)

    xml_parts.append(f'''
  <instruction importance="MANDATORY">
{instruction_content}
  </instruction>''')

    xml_parts.append('\n</nexus-context>')

    return '\n'.join(xml_parts)


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

    build_path = base_path / "02-builds" / build_id

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

    # System files
    system_files = [
        ("00-system/core/orchestrator.md", "AI behavior rules, routing, menu display"),
        ("00-system/system-map.md", "Folder structure and metadata formats"),
        ("01-memory/memory-map.md", "Memory persistence layer"),
        ("04-workspace/workspace-map.md", "User workspace organization"),
    ]

    xml_parts.append('\n  <system-files>')
    for sys_file, description in system_files:
        full_path = base_path / sys_file
        xml = load_file_to_xml(full_path, "file", sys_file, indent=4)
        if xml:
            xml_parts.append(xml)
    xml_parts.append('  </system-files>')

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


# ============================================================================
# Langfuse Auto-Start Functions
# ============================================================================

def ensure_langfuse_running(build_dir: str) -> dict:
    """
    Ensure Langfuse containers and monitor are running.

    Checks:
    1. Docker containers (langfuse-langfuse-web-1)
    2. claude-langfuse-monitor process

    Starts them if not running. Fire-and-forget, non-blocking.

    Returns:
        Dict with status: {"langfuse": "running|started|failed", "monitor": "running|started|failed"}
    """
    import subprocess

    result = {"langfuse": "unknown", "monitor": "unknown"}
    langfuse_dir = Path(build_dir) / "04-workspace" / "langfuse"

    # Skip if langfuse not installed
    if not langfuse_dir.exists():
        logging.info("Langfuse not installed in 04-workspace/langfuse - skipping auto-start")
        return {"langfuse": "not_installed", "monitor": "not_installed"}

    try:
        # 1. Check if Langfuse containers are running
        check_cmd = ["docker", "ps", "--filter", "name=langfuse-langfuse-web", "--format", "{{.Names}}"]
        check_result = subprocess.run(check_cmd, capture_output=True, text=True, timeout=5)

        if "langfuse-langfuse-web" in check_result.stdout:
            result["langfuse"] = "running"
            logging.info("Langfuse containers already running")
        else:
            # Start Langfuse containers
            logging.info("Starting Langfuse containers...")
            start_cmd = ["docker", "compose", "up", "-d"]
            subprocess.Popen(
                start_cmd,
                cwd=str(langfuse_dir),
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
            )
            result["langfuse"] = "started"
            logging.info("Langfuse containers starting in background")
    except subprocess.TimeoutExpired:
        result["langfuse"] = "timeout"
        logging.warning("Docker check timed out - Docker might not be running")
    except FileNotFoundError:
        result["langfuse"] = "docker_not_found"
        logging.warning("Docker not found in PATH")
    except Exception as e:
        result["langfuse"] = "failed"
        logging.error(f"Failed to check/start Langfuse: {e}")

    try:
        # 2. Check if monitor is running (look for node process with claude-langfuse)
        if os.name == 'nt':
            # Windows: use tasklist
            check_cmd = ["tasklist", "/FI", "IMAGENAME eq node.exe", "/FO", "CSV"]
            check_result = subprocess.run(check_cmd, capture_output=True, text=True, timeout=5, shell=True)
            # Can't easily distinguish monitor from other node processes on Windows
            # Just check if config exists and assume it might be running
            config_file = Path.home() / ".claude-langfuse" / "config.json"
            if config_file.exists():
                result["monitor"] = "configured"
                logging.info("claude-langfuse-monitor configured (can't verify if running on Windows)")
            else:
                result["monitor"] = "not_configured"
        else:
            # Unix: use pgrep
            check_cmd = ["pgrep", "-f", "claude-langfuse-monitor"]
            check_result = subprocess.run(check_cmd, capture_output=True, text=True, timeout=5)
            if check_result.returncode == 0:
                result["monitor"] = "running"
                logging.info("claude-langfuse-monitor already running")
            else:
                # Start monitor
                logging.info("Starting claude-langfuse-monitor...")
                subprocess.Popen(
                    ["npx", "claude-langfuse-monitor", "start"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    start_new_session=True
                )
                result["monitor"] = "started"
    except Exception as e:
        result["monitor"] = "failed"
        logging.error(f"Failed to check/start monitor: {e}")

    return result


def main():
    try:
        input_data = json.load(sys.stdin)
        session_id = input_data.get("session_id", "unknown")
        source = input_data.get("source", "startup")
        transcript_path = input_data.get("transcript_path", "unknown")

        build_dir = os.environ.get("CLAUDE_BUILD_DIR", "")

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

        # 1.5. Auto-start Langfuse if installed (fire-and-forget)
        if build_dir:
            langfuse_status = ensure_langfuse_running(build_dir)
            logging.info(f"Langfuse auto-start: {langfuse_status}")

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
        if mode == "compact" and mode_result.get("build_id"):
            # COMPACT mode: Build continuation with full context
            additional_context_str = build_compact_xml(build_dir, session_id, source, mode_result)
            logging.info(f"Built COMPACT XML context ({len(additional_context_str)} chars)")
        else:
            # STARTUP mode: Full menu with all skills and builds
            additional_context_str = build_startup_xml(build_dir, session_id, source, action)
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
                        f.write(f"⚠️  OVER TARGET by {int(estimated_tokens - target_tokens):,} tokens\n")
                    else:
                        f.write(f"✓ Within target ({int(target_tokens - estimated_tokens):,} tokens headroom)\n")
            except Exception:
                pass

        # 7. Ensure server is running (fire-and-forget)
        ensure_server_running()

        # 8. Send session start event (fire-and-forget)
        send_to_server(
            f"/api/v2/sessions/{session_id}/start",
            {
                "source_app": "nexus",
                "source": source,
                "mode": mode,
                "build_id": build_id,
                "timestamp": datetime.now().isoformat()
            }
        )

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
