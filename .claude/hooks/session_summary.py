#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# ///

"""
Session Summary Hook - Generate session summary.

Triggered on SessionEnd event. Fetches executables from observability server,
generates basic summary, posts back to server.
"""

import json
import sys
import os
import urllib.request
import urllib.error
from datetime import datetime

SERVER_URL = os.environ.get("OBSERVABILITY_SERVER_URL", "http://localhost:7777")


def get_session_executables(session_id: str) -> list:
    """Fetch executables from observability server."""
    try:
        url = f"{SERVER_URL}/api/v2/sessions/{session_id}/executables"
        req = urllib.request.Request(url, method="GET")
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode())
            return data.get("data", [])
    except Exception as e:
        print(f"[summary] Failed to fetch executables: {e}", file=sys.stderr)
        return []


def get_session_info(session_id: str) -> dict:
    """Fetch session details from observability server."""
    try:
        url = f"{SERVER_URL}/api/v2/sessions/{session_id}"
        req = urllib.request.Request(url, method="GET")
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode())
            return data.get("data", {})
    except Exception:
        return {}


def generate_summary(executables: list, session_info: dict) -> str:
    """Generate a basic session summary."""
    if not executables:
        return "No executables loaded in this session."

    # Build basic summary from executables
    types = {}
    for e in executables:
        t = e.get("type", "unknown")
        types[t] = types.get(t, 0) + 1

    type_str = ", ".join([f"{v} {k}(s)" for k, v in types.items()])

    # Calculate duration if available
    duration_info = ""
    if session_info.get("started_at") and session_info.get("ended_at"):
        try:
            start = datetime.fromisoformat(session_info["started_at"].replace("Z", "+00:00"))
            end = datetime.fromisoformat(session_info["ended_at"].replace("Z", "+00:00"))
            duration_mins = (end - start).total_seconds() / 60
            duration_info = f" Duration: {duration_mins:.1f} minutes."
        except Exception:
            pass

    return f"Session loaded {len(executables)} executables: {type_str}.{duration_info}"


def send_summary_to_server(session_id: str, summary: str, primary_agent: str = "unknown") -> bool:
    """POST summary to backend metadata endpoint."""
    try:
        url = f"{SERVER_URL}/api/v2/session/{session_id}/meta"
        payload = {
            "agent_name": primary_agent,
            "agent_version": "1.0",
            "summary": summary,
            "generated_at": datetime.now().isoformat(),
            "generator": "basic"
        }
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=5) as resp:
            return resp.status in (200, 201)
    except Exception as e:
        print(f"[summary] Failed to send summary: {e}", file=sys.stderr)
        return False


def main():
    try:
        input_data = json.load(sys.stdin)
        session_id = input_data.get("session_id", "unknown")

        # Skip if this is a recursive stop hook call
        if input_data.get("stop_hook_active", False):
            sys.exit(0)

        # 1. Get session info and executables from backend
        session_info = get_session_info(session_id)
        executables = get_session_executables(session_id)

        if not executables:
            print("[summary] No executables found, skipping summary", file=sys.stderr)
            sys.exit(0)

        # 2. Generate summary
        summary = generate_summary(executables, session_info)

        # 3. Find primary agent (first agent loaded, or "unknown")
        primary_agent = "unknown"
        for e in executables:
            if e.get("type") == "agent":
                primary_agent = e.get("executable_id", "unknown")
                break

        # 4. Send to backend
        success = send_summary_to_server(session_id, summary, primary_agent)

        # 4. Output for verbose mode
        if success:
            print(f"[summary] {summary}")
        else:
            print(f"[summary] Generated but failed to save: {summary}", file=sys.stderr)

        sys.exit(0)

    except Exception as e:
        print(f"[summary] Error: {e}", file=sys.stderr)
        sys.exit(0)  # Never block Claude Code


if __name__ == "__main__":
    main()
