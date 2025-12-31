#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["google-generativeai"]
# ///

"""
Session Summary Hook - Generate human-readable session summary via Gemini.

Triggered on Stop event. Fetches executables from observability server,
generates summary via Gemini 2.5 Flash, posts back to server.
"""

import json
import sys
import os
import urllib.request
import urllib.error
from datetime import datetime

# Gemini API
import google.generativeai as genai

SERVER_URL = os.environ.get("OBSERVABILITY_SERVER_URL", "http://localhost:7777")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "AIzaSyD0lTdUB7_4QSKYVno5zkF8tjnhVtFC4RU")


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


def generate_summary_gemini(executables: list, session_info: dict) -> str:
    """Use Gemini 2.5 Flash to generate human-readable summary."""
    if not executables:
        return "No executables loaded in this session."

    # Configure Gemini
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-2.5-flash")

    # Build context
    exec_list = "\n".join([
        f"{i+1}. [{e.get('type', 'unknown')}] {e.get('executable_id', 'unknown')} "
        f"(detected via {e.get('detection_method', 'unknown')})"
        for i, e in enumerate(executables)
    ])

    # Calculate duration if available
    duration_info = ""
    if session_info.get("started_at") and session_info.get("ended_at"):
        try:
            start = datetime.fromisoformat(session_info["started_at"].replace("Z", "+00:00"))
            end = datetime.fromisoformat(session_info["ended_at"].replace("Z", "+00:00"))
            duration_mins = (end - start).total_seconds() / 60
            duration_info = f"\nSession duration: {duration_mins:.1f} minutes"
        except Exception:
            pass

    prompt = f"""Analyze this Claude Code session and provide a concise 2-3 sentence summary.

Session executables loaded (in order):
{exec_list}
{duration_info}

Focus on:
1. What was the user likely trying to accomplish?
2. Which agents/skills were central to the work?
3. Any notable patterns (debugging, creation, analysis)?

Be concise and insightful. No bullet points - just flowing prose."""

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"[summary] Gemini API error: {e}", file=sys.stderr)
        # Fallback to basic summary
        types = {}
        for e in executables:
            t = e.get("type", "unknown")
            types[t] = types.get(t, 0) + 1
        type_str = ", ".join([f"{v} {k}(s)" for k, v in types.items()])
        return f"Session loaded {len(executables)} executables: {type_str}."


def send_summary_to_server(session_id: str, summary: str, primary_agent: str = "unknown") -> bool:
    """POST summary to backend metadata endpoint."""
    try:
        url = f"{SERVER_URL}/api/v2/session/{session_id}/meta"
        payload = {
            "agent_name": primary_agent,
            "agent_version": "1.0",
            "summary": summary,
            "generated_at": datetime.now().isoformat(),
            "generator": "gemini-2.5-flash"
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

        # 2. Generate summary via Gemini
        summary = generate_summary_gemini(executables, session_info)

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
