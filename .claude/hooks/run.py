#!/usr/bin/env python3
"""
Universal hook runner - works on ALL platforms (macOS, Linux, Windows)

Usage: python .claude/hooks/run.py <script.py> [args...]

Features:
- Finds uv in common locations across all platforms
- Outputs diagnostic JSON for Claude if hook fails
- Single file, no dependencies beyond stdlib
"""

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path


def find_uv() -> str | None:
    """Find uv executable across platforms."""
    # Check PATH first
    uv_path = shutil.which("uv")
    if uv_path:
        return uv_path

    # Common installation locations
    home = Path.home()
    candidates = [
        home / ".local" / "bin" / "uv",
        home / ".cargo" / "bin" / "uv",
        Path("/usr/local/bin/uv"),
        Path("/opt/homebrew/bin/uv"),
    ]

    # Windows-specific locations
    if sys.platform == "win32":
        localappdata = os.environ.get("LOCALAPPDATA", "")
        if localappdata:
            candidates.append(Path(localappdata) / "uv" / "uv.exe")
        candidates.extend([
            home / ".local" / "bin" / "uv.exe",
            home / ".cargo" / "bin" / "uv.exe",
        ])

    for candidate in candidates:
        if candidate.exists():
            return str(candidate)

    return None


def output_error(error_msg: str, script_name: str) -> None:
    """Output error in format Claude can understand."""
    is_session_start = "session_start" in script_name.lower()

    if is_session_start:
        # SessionStart needs additionalContext format
        install_cmd = (
            "irm https://astral.sh/uv/install.ps1 | iex"
            if sys.platform == "win32"
            else "curl -LsSf https://astral.sh/uv/install.sh | sh"
        )
        error_xml = f"""<nexus-context version="v4" mode="error">
  <error type="hook_execution_failed">
    <message>{error_msg}</message>
    <script>{script_name}</script>
    <platform>{sys.platform}</platform>
  </error>
  <instruction importance="MANDATORY">
    HOOK EXECUTION FAILED. To fix:
    1. Install uv: {install_cmd}
    2. Restart your terminal/VSCode
    3. Run /clear to reload context

    For now, read 00-system/core/orchestrator.md and display menu.
  </instruction>
</nexus-context>"""
        output = {
            "hookSpecificOutput": {
                "hookEventName": "SessionStart",
                "additionalContext": error_xml
            }
        }
    else:
        output = {"error": error_msg, "script": script_name}

    print(json.dumps(output), flush=True)


def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No script specified"}), flush=True)
        sys.exit(0)

    script = sys.argv[1]
    args = sys.argv[2:]

    # Find uv
    uv_path = find_uv()
    if not uv_path:
        output_error(
            "uv not found. Install with: curl -LsSf https://astral.sh/uv/install.sh | sh (Unix) or irm https://astral.sh/uv/install.ps1 | iex (Windows)",
            script
        )
        sys.exit(0)  # Exit 0 so Claude processes the output

    # Run the hook
    try:
        result = subprocess.run(
            [uv_path, "run", script] + args,
            capture_output=False,  # Let stdout/stderr pass through
            text=True,
        )
        if result.returncode != 0:
            output_error(f"Hook exited with code {result.returncode}", script)
            sys.exit(0)
    except Exception as e:
        output_error(f"Failed to run hook: {e}", script)
        sys.exit(0)


if __name__ == "__main__":
    main()
