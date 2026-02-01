#!/usr/bin/env python3
"""
Find Langfuse sessions with trace count above threshold.

Usage:
    python find_sessions_by_trace_count.py --min-traces 300
    python find_sessions_by_trace_count.py --min-traces 100 --output large_sessions.json
"""

import json
import subprocess
import sys
import argparse
from datetime import datetime

def get_all_sessions(limit_per_page=50):
    """Fetch all sessions from Langfuse."""
    all_sessions = []
    page = 1

    while True:
        print(f"Fetching page {page}...", end="\r")
        result = subprocess.run(
            ["python", "03-skills/langfuse/langfuse-list-sessions/scripts/list_sessions.py",
             "--limit", str(limit_per_page), "--page", str(page)],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode != 0:
            print(f"\nError fetching page {page}: {result.stderr}")
            break

        data = json.loads(result.stdout)
        page_sessions = data["data"]
        all_sessions.extend(page_sessions)

        # Check if we've reached the end
        if len(page_sessions) < limit_per_page:
            break
        if data["meta"]["page"] >= data["meta"]["totalPages"]:
            break

        page += 1

    print(f"\nFetched {len(all_sessions)} total sessions")
    return all_sessions

def get_trace_count(session_id):
    """Get trace count for a session."""
    try:
        result = subprocess.run(
            ["python", "03-skills/langfuse/langfuse-list-traces/scripts/list_traces.py",
             "--session-id", session_id, "--limit", "1", "--output", "temp_trace_count.json"],
            capture_output=True,
            text=True,
            timeout=15
        )

        if result.returncode != 0:
            return None

        with open("temp_trace_count.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            return data["meta"]["totalItems"]
    except Exception as e:
        return None

def main():
    parser = argparse.ArgumentParser(description="Find Langfuse sessions by trace count")
    parser.add_argument("--min-traces", type=int, default=300, help="Minimum trace count (default: 300)")
    parser.add_argument("--output", type=str, help="Output JSON file (optional)")
    parser.add_argument("--show-all", action="store_true", help="Show all sessions, not just those above threshold")
    args = parser.parse_args()

    print(f"Searching for sessions with {args.min_traces}+ traces...")
    print("=" * 60)

    # Get all sessions
    sessions = get_all_sessions()

    # Check trace counts
    results = []
    found_above_threshold = []

    for i, session in enumerate(sessions, 1):
        session_id = session["id"]
        print(f"Checking {i}/{len(sessions)}: {session_id[:20]}...", end="\r")

        trace_count = get_trace_count(session_id)

        if trace_count is None:
            continue

        result = {
            "session_id": session_id,
            "trace_count": trace_count,
            "created_at": session["createdAt"],
            "environment": session.get("environment", "default")
        }
        results.append(result)

        # Print if above threshold
        if trace_count >= args.min_traces:
            found_above_threshold.append(result)
            print(f"\n[OK] FOUND: {session_id}: {trace_count} traces ({session['createdAt']})")
        elif args.show_all and trace_count >= 50:
            print(f"\n  {session_id}: {trace_count} traces")

    print("\n" + "=" * 60)
    print(f"\nResults:")
    print(f"  Total sessions checked: {len(results)}")
    print(f"  Sessions with {args.min_traces}+ traces: {len(found_above_threshold)}")

    if found_above_threshold:
        print(f"\nSessions above threshold:")
        for s in sorted(found_above_threshold, key=lambda x: x['trace_count'], reverse=True):
            print(f"  - {s['session_id']}: {s['trace_count']} traces ({s['created_at']})")

        # Find largest
        largest = max(found_above_threshold, key=lambda x: x['trace_count'])
        print(f"\nLargest session: {largest['session_id']} with {largest['trace_count']} traces")
    else:
        # Show top 10 by trace count
        top_10 = sorted(results, key=lambda x: x['trace_count'], reverse=True)[:10]
        print(f"\nTop 10 sessions by trace count:")
        for i, s in enumerate(top_10, 1):
            print(f"  {i}. {s['session_id']}: {s['trace_count']} traces ({s['created_at']})")

    # Save to file if requested
    if args.output:
        output_data = {
            "search_config": {
                "min_traces": args.min_traces,
                "search_date": datetime.now().isoformat()
            },
            "total_sessions_checked": len(results),
            "sessions_above_threshold": found_above_threshold,
            "all_sessions": results
        }
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(output_data, f, indent=2)
        print(f"\nResults saved to {args.output}")

    # Cleanup temp file
    try:
        import os
        os.remove("temp_trace_count.json")
    except:
        pass

if __name__ == "__main__":
    main()
