#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# ///

"""
SessionStart Hook - Auto-load Nexus context into Claude.

Triggered by Claude Code on:
- New session start (source=startup)
- Session resume (source=resume)
- After /clear command (source=clear)
- After compaction (source=compact)

KEY INSIGHT: Don't tell Claude to run the loader - RUN IT FOR CLAUDE
and inject the result directly as additionalContext.
"""

import json
import subprocess
import sys
import os
from pathlib import Path

# Add parent directory to path for utils imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime
from utils.http import send_to_server
from utils.server import ensure_server_running


def run_nexus_loader(session_id: str, resume_mode: bool) -> str:
    """Execute nexus-loader and return its output."""
    try:
        project_dir = os.environ.get("CLAUDE_PROJECT_DIR", "")
        if not project_dir:
            return ""

        loader_path = Path(project_dir) / "00-system" / "core" / "nexus-loader.py"
        if not loader_path.exists():
            return ""

        # Build command
        cmd = ["python", str(loader_path)]
        if resume_mode:
            cmd.append("--resume")
        else:
            cmd.append("--startup")
        cmd.extend(["--session", session_id])

        # Execute loader
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=10,
            cwd=project_dir
        )

        return result.stdout.strip()
    except Exception as e:
        return f"[nexus-loader error: {e}]"


def read_cache_file(session_id: str) -> str:
    """Read the cache file content directly."""
    try:
        project_dir = os.environ.get("CLAUDE_PROJECT_DIR", "")
        if not project_dir:
            return ""

        import hashlib
        session_hash = hashlib.md5(session_id.encode()).hexdigest()[:8]

        # Try session-specific cache first
        cache_path = Path(project_dir) / "00-system" / ".cache" / f"context_startup_{session_hash}.json"
        if not cache_path.exists():
            # Fall back to default cache
            cache_path = Path(project_dir) / "00-system" / ".cache" / "context_startup.json"

        if cache_path.exists():
            content = cache_path.read_text(encoding="utf-8")
            # Strip non-ASCII for Windows compatibility in stdout
            return content.encode("ascii", errors="replace").decode("ascii")
        return ""
    except Exception as e:
        return f"[cache read error: {e}]"


def main():
    try:
        input_data = json.load(sys.stdin)
        session_id = input_data.get("session_id", "unknown")
        source = input_data.get("source", "startup")  # startup | resume | clear | compact

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

        # 2. Determine mode and run loader
        resume_mode = source in ("resume", "compact")

        # Run the loader to populate/refresh cache
        loader_output = run_nexus_loader(session_id, resume_mode)

        # 3. Read the cache file content
        cache_content = read_cache_file(session_id)

        # 4. Output context directly - NO instruction for Claude to follow!
        # This IS the context, not a command to get it
        output = f"""<NexusContext source="{source}" session="{session_id}">
{cache_content if cache_content else loader_output}
</NexusContext>"""

        print(output, flush=True)

        # 5. Ensure server is running (fire-and-forget)
        ensure_server_running()

        # 6. Send session start event (fire-and-forget)
        send_to_server(
            f"/api/v2/sessions/{session_id}/start",
            {
                "source_app": "mutagent-obsidian",
                "source": source,
                "timestamp": datetime.now().isoformat()
            }
        )

        sys.exit(0)

    except json.JSONDecodeError:
        # No input or invalid JSON - still continue
        sys.exit(0)
    except Exception as e:
        # Never block Claude Code - log and continue
        print(f"[session_start] Error: {e}", file=sys.stderr)
        sys.exit(0)


if __name__ == "__main__":
    main()
