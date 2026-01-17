#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# ///

"""
SessionEnd Hook - Finalize session and capture full transcript.

Triggered by Claude Code on:
- /clear command (reason: "clear")
- User logout (reason: "logout")
- Prompt input exit (reason: "prompt_input_exit")
- Other termination (reason: "other")

Now also captures the full JSONL transcript for deep analysis.
"""

import json
import sys
import os
from pathlib import Path

# Add parent directory to path for utils imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime
from utils.http import send_to_server

# Local logs directory for transcript backup
LOGS_DIR = Path(__file__).parent.parent.parent / "logs"

# Nexus cache directory (for cleanup)
NEXUS_CACHE_DIR = Path(__file__).parent.parent.parent / "00-system" / ".cache"


def save_transcript_locally(session_id: str, transcript_path: str) -> bool:
    """Save transcript to local logs directory as backup."""
    try:
        if not os.path.exists(transcript_path):
            return False

        # Create session log directory
        session_dir = LOGS_DIR / session_id
        session_dir.mkdir(parents=True, exist_ok=True)

        # Copy transcript
        dest = session_dir / "transcript.jsonl"
        with open(transcript_path, 'r', encoding='utf-8') as src:
            content = src.read()
        with open(dest, 'w', encoding='utf-8') as dst:
            dst.write(content)

        return True
    except Exception:
        return False


def cleanup_session_cache(session_id: str) -> bool:
    """Delete session-specific Nexus cache file."""
    try:
        if not NEXUS_CACHE_DIR.exists():
            return False

        # Session cache uses MD5 hash of session ID (same as nexus-loader.py)
        import hashlib
        session_hash = hashlib.md5(session_id.encode()).hexdigest()[:8]
        cache_file = NEXUS_CACHE_DIR / f"context_startup_{session_hash}.json"

        if cache_file.exists():
            cache_file.unlink()
            return True
        return False
    except Exception:
        return False


def cleanup_stale_caches(max_age_minutes: int = 60) -> int:
    """Delete cache files older than max_age_minutes. Returns count deleted."""
    try:
        if not NEXUS_CACHE_DIR.exists():
            return 0

        import time
        now = time.time()
        max_age_seconds = max_age_minutes * 60
        deleted = 0

        for cache_file in NEXUS_CACHE_DIR.glob("context_startup_*.json"):
            # Skip the default cache (no session suffix)
            if cache_file.name == "context_startup.json":
                continue

            file_age = now - cache_file.stat().st_mtime
            if file_age > max_age_seconds:
                cache_file.unlink()
                deleted += 1

        return deleted
    except Exception:
        return 0


def send_transcript_to_server(session_id: str, transcript_path: str) -> bool:
    """Send full transcript to server for storage and analysis."""
    try:
        if not os.path.exists(transcript_path):
            return False

        with open(transcript_path, 'r', encoding='utf-8') as f:
            transcript_content = f.read()

        # Send to server
        send_to_server(
            f"/api/v2/sessions/{session_id}/transcript",
            {
                "transcript": transcript_content,
                "format": "jsonl",
                "timestamp": datetime.now().isoformat()
            }
        )
        return True
    except Exception:
        return False


def main():
    try:
        input_data = json.load(sys.stdin)
        session_id = input_data.get("session_id", "unknown")
        reason = input_data.get("reason", "other")
        transcript_path = input_data.get("transcript_path", "")

        # 1. Cleanup session-specific Nexus cache
        cleanup_session_cache(session_id)

        # 2. Cleanup stale caches from crashed/orphaned sessions (older than 60 min)
        cleanup_stale_caches(max_age_minutes=60)

        # 3. Send session end event
        send_to_server(
            f"/api/v2/sessions/{session_id}/end",
            {
                "reason": reason,
                "timestamp": datetime.now().isoformat()
            }
        )

        # 4. Capture and send full transcript
        if transcript_path:
            # Save locally as backup
            save_transcript_locally(session_id, transcript_path)

            # Send to server for analysis
            send_transcript_to_server(session_id, transcript_path)

        sys.exit(0)

    except json.JSONDecodeError:
        # No input or invalid JSON - still continue
        sys.exit(0)
    except Exception as e:
        # Never block Claude Code - log and continue
        print(f"[session_end] Error: {e}", file=sys.stderr)
        sys.exit(0)


if __name__ == "__main__":
    main()
