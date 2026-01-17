"""
Transcript parsing utilities for Claude Code hooks.

Shared logic for extracting build information from transcript JSONL files.
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


# Build detection pattern: 02-builds/{id}-{name}/
BUILD_PATTERN = re.compile(r'02-builds[/\\]([0-9]{2}-[a-zA-Z0-9_-]+)', re.IGNORECASE)

# Session ID pattern in YAML frontmatter
SESSION_ID_PATTERN = re.compile(r'session_id:\s*"([^"]+)"')


def find_build_by_session_id(builds_dir: str, session_id: str) -> Optional[str]:
    """
    Find build by session_id match in resume-context.md files.

    MULTI-SESSION ENHANCEMENT:
    - Checks session_ids list first (all sessions)
    - Falls back to legacy session_id field (backward compat)

    This is the PRIMARY detection method - bulletproof for multi-session resume.
    PreCompact adds to session_ids list, SessionStart searches it.

    Args:
        builds_dir: Path to 02-builds/ directory
        session_id: Session ID to search for

    Returns:
        build_id (e.g., "29-build-skill-handover") or None
    """
    if not session_id or session_id == "unknown":
        return None

    builds_path = Path(builds_dir)
    if not builds_path.exists():
        logging.info(f"Builds directory not found: {builds_dir}")
        return None

    try:
        # Scan all build resume-context.md files
        for build_dir in builds_path.iterdir():
            if not build_dir.is_dir():
                continue

            resume_file = build_dir / "01-planning" / "resume-context.md"
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
                        build_id = build_dir.name
                        logging.info(f"Found build {build_id} in session_ids list (multi-session)")
                        return build_id
                else:
                    # Try multiline format
                    session_ids_match = re.search(
                        r'session_ids:\s*\n((?:\s*-\s*"[^"]+"\s*\n)+)',
                        content
                    )
                    if session_ids_match:
                        id_list = re.findall(r'"([^"]+)"', session_ids_match.group(1))
                        if session_id in id_list:
                            build_id = build_dir.name
                            logging.info(f"Found build {build_id} in session_ids list (multi-session)")
                            return build_id

                # Fallback to legacy session_id field (backward compat)
                match = SESSION_ID_PATTERN.search(content)
                if match and match.group(1) == session_id:
                    build_id = build_dir.name
                    logging.info(f"Found build {build_id} by legacy session_id match")
                    return build_id

            except Exception:
                continue

        logging.info(f"No build found with session_id {session_id[:8]}...")
        return None

    except Exception as e:
        logging.error(f"Error finding build by session_id: {e}")
        return None


def parse_transcript_for_build(transcript_path: str, max_entries: int = 500) -> Tuple[Optional[str], str]:
    """
    Parse transcript JSONL to detect active build from tool calls.

    Detection method: Extract file_path from actual tool_use entries (Read, Write, Edit, Glob, Bash).
    Only counts builds from real file operations, NOT from text content or examples.

    Args:
        transcript_path: Path to transcript JSONL file
        max_entries: Maximum number of entries to scan from end (default 500)

    Returns:
        Tuple of (build_id, detection_method)
        - build_id: e.g., "30-xml-context-restructure" or None
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

        # Track build mentions with recency (last mention wins)
        build_mentions = {}

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

                    # Match build pattern against actual file path
                    match = BUILD_PATTERN.search(file_path)
                    if match:
                        build_id = match.group(1)
                        build_mentions[build_id] = idx
                        logging.debug(f"Found build {build_id} from {tool_name} tool")

            except json.JSONDecodeError:
                continue
            except Exception:
                continue

        # Multi-build detection: if 3+ builds touched, this is bulk work, not focused build
        if len(build_mentions) >= 3:
            logging.info(f"Multi-build session detected ({len(build_mentions)} builds) - no single active build")
            return None, "none"

        # Return most recently mentioned build (only if 1-2 builds touched)
        if build_mentions:
            most_recent_build = max(build_mentions.items(), key=lambda x: x[1])[0]
            logging.info(f"Found build in transcript from tool_use: {most_recent_build}")
            return most_recent_build, "transcript"

        logging.info("No build found in transcript tool_use entries")
        return None, "none"

    except Exception as e:
        logging.error(f"Error parsing transcript: {e}")
        return None, "none"


def check_skill_switch_after_build(transcript_path: str, build_id: Optional[str]) -> bool:
    """
    Check if user switched to a non-build skill AFTER loading a build.

    This distinguishes:
    - User loaded build, then switched to paper-search skill → True (moved on)
    - User loaded build, was chatting about it (no skill switch) → False (still in context)

    Skill switch patterns (means LEFT build):
    - 03-skills/*/SKILL.md - user skills
    - 00-system/skills/(?!builds/) - system skills EXCEPT build skills

    Args:
        transcript_path: Path to transcript JSONL file
        build_id: The build ID to check against

    Returns:
        True if skill was loaded AFTER build, False otherwise
    """
    if not build_id:
        return False

    path = Path(transcript_path).expanduser()
    if not path.exists():
        return False

    try:
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        last_entries = lines[-50:] if len(lines) > 50 else lines

        # Patterns
        build_pattern = re.compile(rf'02-builds/{re.escape(build_id)}/')
        user_skill_pattern = re.compile(r'03-skills/[^/]+/SKILL\.md')
        system_skill_pattern = re.compile(r'00-system/skills/(?!builds/)[^/]+/SKILL\.md')

        last_build_idx = -1
        last_skill_idx = -1

        for idx, line in enumerate(last_entries):
            if build_pattern.search(line):
                last_build_idx = idx
            if user_skill_pattern.search(line) or system_skill_pattern.search(line):
                last_skill_idx = idx

        # If skill was loaded AFTER build, user switched away
        if last_build_idx >= 0 and last_skill_idx > last_build_idx:
            logging.info(f"Skill switch detected after build {build_id}")
            return True

        return False

    except Exception as e:
        logging.error(f"Error checking skill switch: {e}")
        return False
