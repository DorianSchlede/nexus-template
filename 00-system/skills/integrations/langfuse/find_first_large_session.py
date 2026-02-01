#!/usr/bin/env python3
"""
Find first Langfuse session with trace count above threshold (stops early).

Usage:
    python find_first_large_session.py --min-traces 300 --first
"""

import json
import subprocess
import sys
import argparse

def get_trace_count(session_id):
    """Get trace count for a session."""
    try:
        result = subprocess.run(
            ["python", "03-skills/langfuse/langfuse-list-traces/scripts/list_traces.py",
             "--session-id", session_id, "--limit", "1", "--output", "temp_first_check.json"],
            capture_output=True,
            text=True,
            timeout=15
        )

        if result.returncode != 0:
            return None

        with open("temp_first_check.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            return data["meta"]["totalItems"]
    except Exception as e:
        return None

def main():
    parser = argparse.ArgumentParser(description="Find first large Langfuse session (fast)")
    parser.add_argument("--min-traces", type=int, default=300, help="Minimum trace count")
    parser.add_argument("--first", action="store_true", help="Stop after finding first match")
    args = parser.parse_args()

    print(f"Searching for first session with {args.min_traces}+ traces...")
    print(f"(Will stop after finding first match if --first is set)")
    print("=" * 60)

    page = 1
    total_checked = 0
    candidates = []

    while True:
        # Fetch page of sessions
        result = subprocess.run(
            ["python", "03-skills/langfuse/langfuse-list-sessions/scripts/list_sessions.py",
             "--limit", "50", "--page", str(page)],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode != 0:
            break

        data = json.loads(result.stdout)
        sessions = data["data"]

        if not sessions:
            break

        # Check each session
        for session in sessions:
            session_id = session["id"]
            total_checked += 1

            trace_count = get_trace_count(session_id)

            if trace_count is None:
                continue

            print(f"{total_checked}. {session_id[:30]}: {trace_count} traces", end="")

            if trace_count >= args.min_traces:
                print(f" [OK] FOUND!")
                candidate = {
                    "session_id": session_id,
                    "trace_count": trace_count,
                    "created_at": session["createdAt"]
                }
                candidates.append(candidate)

                if args.first:
                    print("\n" + "=" * 60)
                    print(f"\nFirst match found: {session_id}")
                    print(f"Trace count: {trace_count}")
                    print(f"Created: {session['createdAt']}")
                    return
            else:
                print()

        # Check if more pages
        if data["meta"]["page"] >= data["meta"]["totalPages"]:
            break

        page += 1

    print("\n" + "=" * 60)
    if candidates:
        print(f"\nFound {len(candidates)} sessions with {args.min_traces}+ traces:")
        for c in candidates:
            print(f"  - {c['session_id']}: {c['trace_count']} traces")
    else:
        print(f"\nNo sessions found with {args.min_traces}+ traces")
        print(f"Checked {total_checked} sessions")

    # Cleanup
    try:
        import os
        os.remove("temp_first_check.json")
    except:
        pass

if __name__ == "__main__":
    main()
