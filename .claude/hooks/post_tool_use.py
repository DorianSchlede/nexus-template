#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# ///

import json
import os
import re
import sys
from pathlib import Path
from utils.constants import ensure_session_log_dir


def inject_session_id_to_resume_context(file_path: str, session_id: str) -> bool:
    """
    Inject session_id into newly created resume-context.md files.

    This enables SessionStart to find the project by exact session_id match.
    Called after Write tool creates a resume-context.md file.
    """
    if not file_path or not session_id or session_id == "unknown":
        return False

    path = Path(file_path)
    if not path.name == "resume-context.md":
        return False

    if not path.exists():
        return False

    try:
        content = path.read_text(encoding="utf-8")

        # Skip if session_id already present
        if "session_id:" in content:
            return False

        # Add session_id after first ---
        if content.startswith("---"):
            content = content.replace(
                "---\n",
                f'---\nsession_id: "{session_id}"\n',
                1
            )
            path.write_text(content, encoding="utf-8")
            return True

        return False
    except Exception:
        return False


def main():
    try:
        # Read JSON input from stdin
        input_data = json.load(sys.stdin)

        # Extract session_id
        session_id = input_data.get("session_id", "unknown")
        tool_name = input_data.get("tool_name", "")
        tool_input = input_data.get("tool_input", {})

        # Inject session_id into newly created resume-context.md files
        if tool_name == "Write":
            file_path = tool_input.get("file_path", "")
            inject_session_id_to_resume_context(file_path, session_id)

        # Ensure session log directory exists
        log_dir = ensure_session_log_dir(session_id)
        log_path = log_dir / "post_tool_use.json"

        # Read existing log data or initialize empty list
        if log_path.exists():
            with open(log_path, "r") as f:
                try:
                    log_data = json.load(f)
                except (json.JSONDecodeError, ValueError):
                    log_data = []
        else:
            log_data = []

        # Append new data
        log_data.append(input_data)

        # Write back to file with formatting
        with open(log_path, "w") as f:
            json.dump(log_data, f, indent=2)

        sys.exit(0)

    except json.JSONDecodeError:
        # Handle JSON decode errors gracefully
        sys.exit(0)
    except Exception:
        # Exit cleanly on any other error
        sys.exit(0)


if __name__ == "__main__":
    main()
