"""
Transcript parsing utilities for Claude Code hooks.

Shared logic for extracting project information from transcript JSONL files.
Used by both SessionStart and PreCompact hooks.

Detection priority:
1. session_id match in resume-context.md (exact, bulletproof)
2. Transcript tool_use parsing (fallback for PreCompact)
"""

import json
import re
import logging
from pathlib import Path
from typing import Optional, Tuple


# Project detection pattern: 02-projects/{id}-{name}/
PROJECT_PATTERN = re.compile(r'02-projects[/\\]([0-9]{2}-[a-zA-Z0-9_-]+)', re.IGNORECASE)

# Session ID pattern in YAML frontmatter
SESSION_ID_PATTERN = re.compile(r'session_id:\s*"([^"]+)"')


def find_project_by_session_id(projects_dir: str, session_id: str) -> Optional[str]:
    """
    Find project by session_id match in resume-context.md files.

    MULTI-SESSION ENHANCEMENT:
    - Checks session_ids list first (all sessions)
    - Falls back to legacy session_id field (backward compat)

    This is the PRIMARY detection method - bulletproof for multi-session resume.
    PreCompact adds to session_ids list, SessionStart searches it.

    Args:
        projects_dir: Path to 02-projects/ directory
        session_id: Session ID to search for

    Returns:
        project_id (e.g., "29-project-skill-handover") or None
    """
    if not session_id or session_id == "unknown":
        return None

    projects_path = Path(projects_dir)
    if not projects_path.exists():
        logging.info(f"Projects directory not found: {projects_dir}")
        return None

    try:
        # Scan all project resume-context.md files
        for project_dir in projects_path.iterdir():
            if not project_dir.is_dir():
                continue

            resume_file = project_dir / "01-planning" / "resume-context.md"
            if not resume_file.exists():
                continue

            try:
                content = resume_file.read_text(encoding="utf-8")

                # Check session_ids list first (multi-session support)
                session_ids_match = re.search(
                    r'session_ids:\s*\[(.*?)\]',  # Inline format
                    content,
                    re.DOTALL
                )
                if session_ids_match:
                    id_list = re.findall(r'"([^"]+)"', session_ids_match.group(1))
                    if session_id in id_list:
                        project_id = project_dir.name
                        logging.info(f"Found project {project_id} in session_ids list (multi-session)")
                        return project_id
                else:
                    # Try multiline format
                    session_ids_match = re.search(
                        r'session_ids:\s*\n((?:\s*-\s*"[^"]+"\s*\n)+)',
                        content
                    )
                    if session_ids_match:
                        id_list = re.findall(r'"([^"]+)"', session_ids_match.group(1))
                        if session_id in id_list:
                            project_id = project_dir.name
                            logging.info(f"Found project {project_id} in session_ids list (multi-session)")
                            return project_id

                # Fallback to legacy session_id field (backward compat)
                match = SESSION_ID_PATTERN.search(content)
                if match and match.group(1) == session_id:
                    project_id = project_dir.name
                    logging.info(f"Found project {project_id} by legacy session_id match")
                    return project_id

            except Exception:
                continue

        logging.info(f"No project found with session_id {session_id[:8]}...")
        return None

    except Exception as e:
        logging.error(f"Error finding project by session_id: {e}")
        return None


def parse_transcript_for_project(transcript_path: str, max_entries: int = 500) -> Tuple[Optional[str], str]:
    """
    Parse transcript JSONL to detect active project from tool calls.

    Detection method: Extract file_path from actual tool_use entries (Read, Write, Edit, Glob, Bash).
    Only counts projects from real file operations, NOT from text content or examples.

    Args:
        transcript_path: Path to transcript JSONL file
        max_entries: Maximum number of entries to scan from end (default 500)

    Returns:
        Tuple of (project_id, detection_method)
        - project_id: e.g., "30-xml-context-restructure" or None
        - detection_method: "transcript" or "none"
    """
    path = Path(transcript_path).expanduser()
    if not path.exists():
        logging.info(f"Transcript not found: {transcript_path}")
        return None, "none"

    try:
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        # Read last N entries (most recent at end)
        last_entries = lines[-max_entries:] if len(lines) > max_entries else lines

        # Track project mentions with recency (last mention wins)
        project_mentions = {}

        for idx, line in enumerate(last_entries):
            try:
                data = json.loads(line)
                msg = data.get('message', {})

                # Only look at assistant messages with tool_use
                if msg.get('role') != 'assistant':
                    continue

                content = msg.get('content', [])
                for item in content:
                    if item.get('type') != 'tool_use':
                        continue

                    tool_name = item.get('name', '')
                    # Only consider file operation tools
                    if tool_name not in ('Read', 'Write', 'Edit', 'Glob', 'Grep', 'Bash'):
                        continue

                    tool_input = item.get('input', {})

                    # Extract file path from tool input
                    file_path = tool_input.get('file_path', '') or tool_input.get('path', '')

                    # Match project pattern against actual file path
                    match = PROJECT_PATTERN.search(file_path)
                    if match:
                        project_id = match.group(1)
                        project_mentions[project_id] = idx
                        logging.debug(f"Found project {project_id} from {tool_name} tool")

            except json.JSONDecodeError:
                continue
            except Exception:
                continue

        # Multi-project detection: if 3+ projects touched, this is bulk work, not focused project
        if len(project_mentions) >= 3:
            logging.info(f"Multi-project session detected ({len(project_mentions)} projects) - no single active project")
            return None, "none"

        # Return most recently mentioned project (only if 1-2 projects touched)
        if project_mentions:
            most_recent_project = max(project_mentions.items(), key=lambda x: x[1])[0]
            logging.info(f"Found project in transcript from tool_use: {most_recent_project}")
            return most_recent_project, "transcript"

        logging.info("No project found in transcript tool_use entries")
        return None, "none"

    except Exception as e:
        logging.error(f"Error parsing transcript: {e}")
        return None, "none"


def check_skill_switch_after_project(transcript_path: str, project_id: Optional[str]) -> bool:
    """
    Check if user switched to a non-project skill AFTER loading a project.

    This distinguishes:
    - User loaded project, then switched to paper-search skill → True (moved on)
    - User loaded project, was chatting about it (no skill switch) → False (still in context)

    Skill switch patterns (means LEFT project):
    - 03-skills/*/SKILL.md - user skills
    - 00-system/skills/(?!projects/) - system skills EXCEPT project skills

    Args:
        transcript_path: Path to transcript JSONL file
        project_id: The project ID to check against

    Returns:
        True if skill was loaded AFTER project, False otherwise
    """
    if not project_id:
        return False

    path = Path(transcript_path).expanduser()
    if not path.exists():
        return False

    try:
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        last_entries = lines[-50:] if len(lines) > 50 else lines

        # Patterns
        project_pattern = re.compile(rf'02-projects/{re.escape(project_id)}/')
        user_skill_pattern = re.compile(r'03-skills/[^/]+/SKILL\.md')
        system_skill_pattern = re.compile(r'00-system/skills/(?!projects/)[^/]+/SKILL\.md')

        last_project_idx = -1
        last_skill_idx = -1

        for idx, line in enumerate(last_entries):
            if project_pattern.search(line):
                last_project_idx = idx
            if user_skill_pattern.search(line) or system_skill_pattern.search(line):
                last_skill_idx = idx

        # If skill was loaded AFTER project, user switched away
        if last_project_idx >= 0 and last_skill_idx > last_project_idx:
            logging.info(f"Skill switch detected after project {project_id}")
            return True

        return False

    except Exception as e:
        logging.error(f"Error checking skill switch: {e}")
        return False
