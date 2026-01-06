#!/usr/bin/env python3
"""
PreCompact Hook: Save Resume State

This hook is triggered before Claude Code compacts the context.
It updates the active project's resume-context.md timestamp for
cross-session resume detection.

CRITICAL REQUIREMENTS:
- MUST return {} (empty object) - cannot inject context via return value
- MUST execute in <50ms

Input (stdin JSON):
{
  "session_id": "abc123",
  "transcript_path": "~/.claude/projects/.../xxx.jsonl",
  "hook_event_name": "PreCompact",
  "trigger": "manual" | "auto",
  "custom_instructions": ""
}
"""

import json
import os
import re
import sys
import time
import logging
from datetime import datetime, timezone
from pathlib import Path

# Add parent directory to path for utils imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.transcript import parse_transcript_for_project, find_project_by_session_id

# Performance tracking
START_TIME = time.perf_counter()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - PreCompact - %(levelname)s - %(message)s'
)


def find_nexus_root() -> Path:
    """Find the Nexus root directory from CLAUDE_PROJECT_DIR."""
    project_dir = os.environ.get("CLAUDE_PROJECT_DIR", "")
    if project_dir:
        return Path(project_dir)
    # Fallback: try current directory
    return Path.cwd()


def cleanup_session_cache(nexus_root: Path, session_id: str) -> bool:
    """Delete session-specific cache before compaction (new one will be created after)."""
    if not session_id or session_id == "unknown":
        return False

    try:
        import hashlib
        session_hash = hashlib.md5(session_id.encode()).hexdigest()[:8]
        cache_file = nexus_root / "00-system" / ".cache" / f"context_startup_{session_hash}.json"

        if cache_file.exists():
            cache_file.unlink()
            return True
        return False
    except Exception:
        return False


def update_project_resume_context(nexus_root: Path, project_id: str, session_id: str) -> bool:
    """
    Update project's resume-context.md with session_id list and timestamp.

    MULTI-SESSION ENHANCEMENT:
    - Maintains session_ids list (all sessions that touched this project)
    - Keeps legacy session_id field (most recent, for backward compat)
    - Prevents duplicates in the list

    This enables SessionStart to:
    1. Find project via ANY session in the list (multi-session support)
    2. Find most recently active project via last_updated
    """
    project_path = nexus_root / "02-projects" / project_id / "01-planning"
    resume_file = project_path / "resume-context.md"

    if not resume_file.exists():
        logging.info(f"No resume-context.md for project {project_id}")
        return False

    try:
        content = resume_file.read_text(encoding="utf-8")
        timestamp = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

        # Extract existing session_ids list
        existing_ids = []
        session_ids_match = re.search(
            r'session_ids:\s*\[(.*?)\]',  # Inline list format
            content,
            re.DOTALL
        )
        if session_ids_match:
            # Parse inline list: ["id1", "id2"]
            id_list_str = session_ids_match.group(1)
            existing_ids = re.findall(r'"([^"]+)"', id_list_str)
        else:
            # Try multiline format
            session_ids_match = re.search(
                r'session_ids:\s*\n((?:\s*-\s*"[^"]+"\s*\n)+)',
                content
            )
            if session_ids_match:
                id_lines = session_ids_match.group(1)
                existing_ids = re.findall(r'"([^"]+)"', id_lines)

        # Add current session if not already in list
        if session_id not in existing_ids:
            existing_ids.append(session_id)
            logging.info(f"Added session {session_id[:8]}... to project {project_id} (total: {len(existing_ids)} sessions)")
        else:
            logging.info(f"Session {session_id[:8]}... already tracked for project {project_id}")

        # Format as inline YAML list for simplicity
        session_ids_str = "[" + ", ".join([f'"{sid}"' for sid in existing_ids]) + "]"

        # Update or add session_ids list
        if "session_ids:" in content:
            # Replace existing list (both inline and multiline formats)
            content = re.sub(
                r'session_ids:\s*\[.*?\]',  # Inline
                f'session_ids: {session_ids_str}',
                content,
                flags=re.DOTALL
            )
            content = re.sub(
                r'session_ids:\s*\n(?:\s*-\s*"[^"]+"\s*\n)+',  # Multiline
                f'session_ids: {session_ids_str}\n',
                content
            )
        else:
            # Add new session_ids field
            content = content.replace(
                "---\n",
                f'---\nsession_ids: {session_ids_str}\n',
                1
            )

        # Update legacy session_id field (most recent, for backward compat)
        if "session_id:" in content and "session_ids:" not in content[:content.index("session_id:")]:
            # Only update if it's the standalone field, not inside session_ids
            content = re.sub(
                r'(?<!session_)session_id:\s*"[^"]*"',
                f'session_id: "{session_id}"',
                content
            )
        elif "session_ids:" in content and "session_id:" not in content:
            # Add legacy field for backward compat
            session_ids_line = content.find("session_ids:")
            insert_pos = content.find("\n", session_ids_line) + 1
            content = content[:insert_pos] + f'session_id: "{session_id}"\n' + content[insert_pos:]

        # Update or add last_updated
        if "last_updated:" in content:
            content = re.sub(
                r'last_updated:\s*"[^"]*"',
                f'last_updated: "{timestamp}"',
                content
            )
        else:
            # Add last_updated after first ---
            content = content.replace(
                "---\n",
                f'---\nlast_updated: "{timestamp}"\n',
                1
            )

        resume_file.write_text(content, encoding="utf-8")
        logging.info(f"Updated resume-context.md for project {project_id} ({len(existing_ids)} sessions tracked)")
        return True
    except Exception as e:
        logging.error(f"Failed to update resume-context.md for {project_id}: {e}")
        return False


def main():
    # Read hook input from stdin
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        logging.error(f"Invalid JSON input: {e}")
        sys.exit(1)

    # Get session info
    session_id = input_data.get("session_id", "unknown")
    transcript_path = input_data.get("transcript_path", "")

    # Find Nexus root
    nexus_root = find_nexus_root()

    # Clean up old session cache (new one will be created after compaction)
    cleanup_session_cache(nexus_root, session_id)

    # Detect active project - try session_id match first (from previous compact), then transcript
    projects_dir = str(nexus_root / "02-projects")
    active_project_id = find_project_by_session_id(projects_dir, session_id)

    if not active_project_id:
        # Fallback: parse transcript for tool_use patterns
        active_project_id, _ = parse_transcript_for_project(transcript_path)
        if active_project_id:
            logging.info(f"Fallback: found project {active_project_id} from transcript")

    # Update project's resume-context.md with session_id for exact matching
    if active_project_id:
        update_project_resume_context(nexus_root, active_project_id, session_id)

    # Performance check
    elapsed_ms = (time.perf_counter() - START_TIME) * 1000
    if elapsed_ms > 50:
        logging.warning(f"PreCompact hook exceeded 50ms budget: {elapsed_ms:.2f}ms")
    else:
        logging.info(f"PreCompact hook completed in {elapsed_ms:.2f}ms")

    # CRITICAL: Return empty object (hooks cannot inject context via return value)
    print(json.dumps({}))
    sys.exit(0)


if __name__ == "__main__":
    main()
