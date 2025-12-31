#!/usr/bin/env python3
"""
PreCompact Hook: Save Resume State

This hook is triggered before Claude Code compacts the context.
It automatically updates the active project's _resume.md file
to preserve the current skill/phase state for the next session.

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
from datetime import datetime
from pathlib import Path


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


def load_cache_context(nexus_root: Path) -> dict:
    """Load the cached startup context to get the active project."""
    cache_file = nexus_root / "00-system" / ".cache" / "context_startup.json"
    if not cache_file.exists():
        return {}

    try:
        return json.loads(cache_file.read_text(encoding="utf-8"))
    except Exception:
        return {}


def get_active_project(cache_context: dict) -> dict | None:
    """Get the most recently active IN_PROGRESS project from cache."""
    projects = cache_context.get("metadata", {}).get("projects", [])

    # Find first IN_PROGRESS project (they're sorted by most recent)
    for project in projects:
        if project.get("status") == "IN_PROGRESS":
            return project

    return None


def parse_transcript_for_skill(transcript_path: str) -> str | None:
    """
    Parse the transcript JSONL to find the last --skill invocation.

    Looks for patterns like:
    - python nexus-loader.py --skill execute-project
    - python 00-system/core/nexus-loader.py --skill analyze-research-project
    """
    path = Path(transcript_path).expanduser()
    if not path.exists():
        return None

    last_skill = None
    skill_pattern = re.compile(r'--skill\s+([a-z0-9-]+)', re.IGNORECASE)

    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    entry = json.loads(line.strip())
                    # Look for Bash tool calls with --skill
                    content = str(entry)
                    matches = skill_pattern.findall(content)
                    if matches:
                        last_skill = matches[-1]  # Take the last one in this entry
                except json.JSONDecodeError:
                    continue
    except Exception:
        pass

    return last_skill


def skill_to_phase(skill_name: str) -> str:
    """Map skill name to phase."""
    phase_map = {
        "analyze-research-project": "analysis",
        "synthesize-research-project": "synthesis",
        "execute-project": "execution",
        "create-project": "planning",
    }
    return phase_map.get(skill_name, "execution")


def write_resume_file(project_path: Path, skill: str, phase: str, project_id: str) -> bool:
    """Write the _resume.md file with current state."""
    resume_file = project_path / "_resume.md"

    now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

    content = f"""---
updated: "{now}"
phase: "{phase}"
last_skill: "{skill}"
project_id: "{project_id}"
---

# Resume Context

Auto-saved by PreCompact hook at {now}.

## State
- **Phase**: {phase}
- **Last Skill**: {skill}
- **Project**: {project_id}

## Notes
This file was automatically generated before context compaction.
The next session will use this to load the correct skill.
"""

    try:
        resume_file.write_text(content, encoding="utf-8")
        return True
    except Exception as e:
        print(f"Failed to write _resume.md: {e}", file=sys.stderr)
        return False


def main():
    # Read hook input from stdin
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON input: {e}", file=sys.stderr)
        sys.exit(1)

    # Get session info
    session_id = input_data.get("session_id", "unknown")
    transcript_path = input_data.get("transcript_path", "")
    trigger = input_data.get("trigger", "unknown")

    # Find Nexus root
    nexus_root = find_nexus_root()

    # Clean up old session cache (new one will be created after compaction)
    cleanup_session_cache(nexus_root, session_id)

    # Load cached context for active project
    cache_context = load_cache_context(nexus_root)
    active_project = get_active_project(cache_context)

    if not active_project:
        # No active project, nothing to save
        print(json.dumps({
            "message": "No active project found, skipping resume state save"
        }))
        sys.exit(0)

    project_id = active_project.get("id", "")
    project_file_path = active_project.get("_file_path", "")

    if not project_file_path:
        print(json.dumps({
            "message": f"No file path for project {project_id}"
        }))
        sys.exit(0)

    # Derive project directory from overview.md path
    project_path = Path(project_file_path).parent.parent

    # Parse transcript for last skill
    last_skill = parse_transcript_for_skill(transcript_path)

    # Default to execute-project if no skill found
    if not last_skill:
        last_skill = "execute-project"

    # Determine phase from skill
    phase = skill_to_phase(last_skill)

    # Write the resume file
    success = write_resume_file(project_path, last_skill, phase, project_id)

    if success:
        # Output context for the compacted conversation
        # This becomes part of the summary that Claude sees after compaction
        compact_context = f"""<NexusResumeContext>
CONTINUE PROJECT: {project_id}
PHASE: {phase}
LAST SKILL: {last_skill}

MANDATORY NEXT STEP:
Run: python 00-system/core/nexus-loader.py --resume --session {session_id}
Then read the cache file and continue working on {project_id}.
</NexusResumeContext>"""

        print(compact_context)
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
