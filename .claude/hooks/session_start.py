#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# ///

"""
SessionStart Hook - Initialize session and ensure server is running.

Triggered by Claude Code on:
- New session start
- Session resume
- After /clear command
"""

import json
import sys
import os

# Add parent directory to path for utils imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime
from utils.http import send_to_server
from utils.server import ensure_server_running


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

        # 2. Output nexus-loader command to stdout → becomes additionalContext
        # This auto-injects the loader command into Claude's context!
        if source in ("startup", "clear"):
            print(f"Run NOW: python 00-system/core/nexus-loader.py --startup --session {session_id}")
        elif source in ("resume", "compact"):
            print(f"Run NOW: python 00-system/core/nexus-loader.py --resume --session {session_id}")

        # 3. Ensure server is running (fire-and-forget)
        ensure_server_running()

        # 4. Send session start event (fire-and-forget)
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
