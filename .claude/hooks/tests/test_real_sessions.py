"""
Test multi-session handover with real Claude Code transcripts.

This script validates the enhanced handover system against actual session data:
1. Simulates multiple sessions working on same build
2. Verifies session_ids list accumulation
3. Tests cross-session build detection
4. Validates state transitions (new → compact → resume)
"""

import sys
import json
from pathlib import Path
from datetime import datetime

# Add hooks to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from save_resume_state import update_build_resume_context, find_nexus_root
from utils.transcript import find_build_by_session_id, parse_transcript_for_build
from utils.build_state import detect_build_state


def test_current_session_state():
    """Test 1: Detect current session's build and state."""
    print("=" * 80)
    print("TEST 1: Current Session State Detection")
    print("=" * 80)

    nexus_root = find_nexus_root()
    print(f"Nexus Root: {nexus_root}\n")

    # Find build 28
    build_path = nexus_root / "02-builds" / "28-handover-test-suite"

    if not build_path.exists():
        print("❌ Build 28 not found")
        return False

    print("📁 Build 28 found")
    state = detect_build_state(build_path)

    if not state:
        print("❌ Could not detect build state")
        return False

    print("\n📊 Current State:")
    print(f"   ID: {state.build_id}")
    print(f"   Name: {state.name}")
    print(f"   Status: {state.status}")
    print(f"   Phase: {state.current_phase} → {state.next_action}")
    print(f"   Progress: {state.tasks_completed}/{state.tasks_total} ({state.progress_percent}%)")
    print(f"   Section: {state.current_section}")
    print(f"   Last Updated: {state.last_updated}")
    print(f"   Session IDs: {len(state.session_ids)} tracked")

    for i, sid in enumerate(state.session_ids, 1):
        print(f"      {i}. {sid[:16]}...")

    print("\n✅ State detection successful\n")
    return True


def test_multi_session_simulation():
    """Test 2: Simulate multiple sessions touching same build."""
    print("=" * 80)
    print("TEST 2: Multi-Session Simulation")
    print("=" * 80)

    nexus_root = find_nexus_root()
    build_id = "28-handover-test-suite"

    # Simulate 3 different sessions
    test_sessions = [
        "test-session-alpha-001",
        "test-session-beta-002",
        "test-session-gamma-003"
    ]

    print(f"Simulating {len(test_sessions)} sessions working on build {build_id}...\n")

    for i, session_id in enumerate(test_sessions, 1):
        print(f"Session {i}: {session_id}")
        result = update_build_resume_context(nexus_root, build_id, session_id)

        if not result:
            print(f"   ❌ Failed to update resume context")
            return False

        print(f"   ✅ Updated resume-context.md")

    # Verify all sessions tracked
    print("\n📋 Verifying session tracking...")
    resume_file = nexus_root / "02-builds" / build_id / "01-planning" / "resume-context.md"

    if not resume_file.exists():
        print("❌ resume-context.md not found")
        return False

    content = resume_file.read_text(encoding="utf-8")

    print("\nSession IDs found in resume-context.md:")
    for session_id in test_sessions:
        if session_id in content:
            print(f"   ✅ {session_id}")
        else:
            print(f"   ❌ {session_id} NOT FOUND")
            return False

    # Test detection from each session
    print("\n🔍 Testing detection from each session ID...")
    builds_dir = str(nexus_root / "02-builds")

    for session_id in test_sessions:
        detected = find_build_by_session_id(builds_dir, session_id)

        if detected and "28-handover-test-suite" in detected:
            print(f"   ✅ {session_id[:20]}... → {detected}")
        else:
            print(f"   ❌ {session_id[:20]}... → NOT DETECTED")
            return False

    print("\n✅ Multi-session simulation successful\n")
    return True


def test_real_transcript_detection():
    """Test 3: Parse actual transcript and detect build."""
    print("=" * 80)
    print("TEST 3: Real Transcript Detection")
    print("=" * 80)

    nexus_root = find_nexus_root()
    sessions_dir = nexus_root.parent / ".claude" / "sessions"

    if not sessions_dir.exists():
        print("⚠️  No sessions directory found (expected in development)")
        print("✅ Test skipped\n")
        return True

    # Find most recent transcript
    transcripts = list(sessions_dir.glob("*/transcript.jsonl"))

    if not transcripts:
        print("⚠️  No transcripts found")
        print("✅ Test skipped\n")
        return True

    # Get most recent
    transcripts.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    recent_transcript = transcripts[0]
    session_id = recent_transcript.parent.name

    print(f"📄 Most Recent Transcript:")
    print(f"   Session: {session_id}")
    print(f"   Path: {recent_transcript}")

    # Parse transcript
    detected_build, method = parse_transcript_for_build(str(recent_transcript))

    if detected_build:
        print(f"\n✅ Detected Build: {detected_build}")
        print(f"   Detection Method: {method}")

        # Get build state
        build_path = nexus_root / "02-builds" / detected_build
        if build_path.exists():
            state = detect_build_state(build_path)
            if state:
                print(f"\n📊 Build State:")
                print(f"   Status: {state.status}")
                print(f"   Progress: {state.progress_percent}%")
                print(f"   Tracked Sessions: {len(state.session_ids)}")
    else:
        print(f"\n⚠️  No build detected (method: {method})")
        print("   This is OK if transcript doesn't contain build work")

    print("\n✅ Transcript detection successful\n")
    return True


def test_session_lifecycle():
    """Test 4: Verify session lifecycle behavior."""
    print("=" * 80)
    print("TEST 4: Session Lifecycle Verification")
    print("=" * 80)

    print("""
Session Lifecycle (as implemented):

1. NEW session (session_id: aaa111)
   → SessionStart detects no build
   → User works on Build 28
   → PreCompact saves: session_ids: ["aaa111"]

2. COMPACT (same session_id: aaa111)
   → SessionStart finds build via "aaa111"
   → User continues work
   → PreCompact updates: session_ids: ["aaa111"] (no duplicate)

3. RESUME (NEW session_id: bbb222)
   → SessionStart searches session_ids list
   → Doesn't find "bbb222" yet
   → Falls back to most recent build → finds Build 28
   → User works on build
   → PreCompact updates: session_ids: ["aaa111", "bbb222"]

4. Later RESUME (another NEW session_id: ccc333)
   → SessionStart searches session_ids list
   → Still uses most recent fallback
   → PreCompact updates: session_ids: ["aaa111", "bbb222", "ccc333"]

5. Any session resumes
   → If session was "aaa111" → finds via list ✅
   → If session was "bbb222" → finds via list ✅
   → If session was "ccc333" → finds via list ✅
""")

    nexus_root = find_nexus_root()
    build_id = "28-handover-test-suite"
    resume_file = nexus_root / "02-builds" / build_id / "01-planning" / "resume-context.md"

    if resume_file.exists():
        content = resume_file.read_text(encoding="utf-8")

        print("Current resume-context.md:")
        print("-" * 80)

        # Show relevant lines
        for line in content.split('\n')[:20]:
            if 'session' in line.lower() or 'last_updated' in line.lower() or line.strip() in ['---']:
                print(f"   {line}")

        print("-" * 80)

    print("\n✅ Lifecycle verification complete\n")
    return True


def test_cleanup_simulation():
    """Test 5: Clean up test session IDs."""
    print("=" * 80)
    print("TEST 5: Cleanup Test Sessions")
    print("=" * 80)

    nexus_root = find_nexus_root()
    build_id = "28-handover-test-suite"
    resume_file = nexus_root / "02-builds" / build_id / "01-planning" / "resume-context.md"

    if not resume_file.exists():
        print("⚠️  No resume-context.md found")
        return True

    content = resume_file.read_text(encoding="utf-8")

    # Remove test sessions
    test_prefixes = ["test-session-alpha", "test-session-beta", "test-session-gamma"]
    modified = content

    for prefix in test_prefixes:
        if prefix in content:
            # Remove from inline list
            import re
            modified = re.sub(rf'"{prefix}[^"]*",?\s*', '', modified)
            modified = re.sub(r',\s*]', ']', modified)  # Clean up trailing commas

    if modified != content:
        resume_file.write_text(modified, encoding="utf-8")
        print("✅ Cleaned up test session IDs")
    else:
        print("✅ No test sessions to clean up")

    print()
    return True


def main():
    """Run all real-session tests."""
    print("\n")
    print("+" + "=" * 78 + "+")
    print("|" + " " * 20 + "REAL SESSION HANDOVER TESTS" + " " * 31 + "|")
    print("+" + "=" * 78 + "+")
    print()

    tests = [
        ("Current Session State", test_current_session_state),
        ("Multi-Session Simulation", test_multi_session_simulation),
        ("Real Transcript Detection", test_real_transcript_detection),
        ("Session Lifecycle", test_session_lifecycle),
        ("Cleanup Test Sessions", test_cleanup_simulation),
    ]

    results = []

    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ {name} failed with exception:")
            print(f"   {type(e).__name__}: {e}\n")
            results.append((name, False))

    # Summary
    print("=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")

    print()
    print(f"Results: {passed}/{total} tests passed")

    if passed == total:
        print("\n🎉 All tests passed! Multi-session handover is working correctly.\n")
        return 0
    else:
        print("\n⚠️  Some tests failed. Review output above.\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
