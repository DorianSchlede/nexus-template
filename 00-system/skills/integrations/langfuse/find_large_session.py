import json
import subprocess
import sys

# Get list of sessions (check more pages)
all_sessions = []
for page in range(1, 8):  # 343 sessions / 50 = ~7 pages
    result = subprocess.run(
        ["python", "03-skills/langfuse/langfuse-list-sessions/scripts/list_sessions.py",
         "--limit", "50", "--page", str(page)],
        capture_output=True,
        text=True
    )
    page_data = json.loads(result.stdout)["data"]
    all_sessions.extend(page_data)
    if len(page_data) < 50:
        break

print(f"Checking {len(all_sessions)} sessions for trace counts...")
sessions = all_sessions
print()

large_sessions = []

for session in sessions:
    session_id = session["id"]

    # Get trace count for this session
    try:
        result = subprocess.run(
            ["python", "03-skills/langfuse/langfuse-list-traces/scripts/list_traces.py",
             "--session-id", session_id, "--limit", "1", "--output", "temp_check.json"],
            capture_output=True,
            text=True,
            timeout=10
        )

        with open("temp_check.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            trace_count = data["meta"]["totalItems"]

            if trace_count >= 300:
                large_sessions.append({
                    "session_id": session_id,
                    "trace_count": trace_count,
                    "created_at": session["createdAt"]
                })
                print(f"[OK] {session_id}: {trace_count} traces")
            elif trace_count >= 100:
                print(f"  {session_id}: {trace_count} traces")

    except Exception as e:
        print(f"[FAIL] {session_id}: Error - {e}")
        continue

print()
print(f"Found {len(large_sessions)} sessions with 300+ traces:")
for s in large_sessions:
    print(f"  {s['session_id']}: {s['trace_count']} traces ({s['created_at']})")

if large_sessions:
    best = max(large_sessions, key=lambda x: x['trace_count'])
    print()
    print(f"Largest session: {best['session_id']} with {best['trace_count']} traces")
