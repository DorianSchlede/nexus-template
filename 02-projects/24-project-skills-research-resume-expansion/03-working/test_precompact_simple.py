#!/usr/bin/env python3
"""
Simple PreCompact Hook Test

Creates a realistic test scenario with mock transcript
and validates hook behavior.
"""

import json
import subprocess
import sys
import tempfile
import time
from pathlib import Path

def create_mock_transcript(tmp_path: Path) -> Path:
    """Create a mock transcript with project references."""
    transcript_file = tmp_path / "test-transcript.jsonl"

    # Mock transcript entries with project file operations
    entries = [
        {
            "type": "tool_use",
            "name": "Read",
            "input": {"file_path": "c:/Users/dsber/infinite/auto-company/strategy-nexus/02-projects/24-project-skills-research-resume-expansion/01-planning/overview.md"}
        },
        {
            "type": "tool_use",
            "name": "Write",
            "input": {"file_path": "c:/Users/dsber/infinite/auto-company/strategy-nexus/02-projects/24-project-skills-research-resume-expansion/03-working/test.py"}
        },
        {
            "type": "bash",
            "command": "python 00-system/core/nexus-loader.py --project 24-project-skills-research-resume-expansion"
        }
    ]

    with open(transcript_file, "w", encoding="utf-8") as f:
        for entry in entries:
            f.write(json.dumps(entry) + "\n")

    return transcript_file


def test_hook():
    print("=" * 80)
    print("PreCompact Hook Simple Test")
    print("=" * 80)
    print()

    # Find hook
    script_dir = Path(__file__).parent
    nexus_root = script_dir.parent.parent.parent
    hook_path = nexus_root / ".claude" / "hooks" / "save_resume_state.py"

    if not hook_path.exists():
        print(f"[FAIL] Hook not found at {hook_path}")
        return False

    print(f"Hook: {hook_path}")
    print(f"Nexus Root: {nexus_root}")
    print()

    # Create mock transcript
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        transcript_file = create_mock_transcript(tmp_path)

        print(f"Created mock transcript: {transcript_file}")
        print()

        # Prepare hook input
        hook_input = {
            "session_id": "test-session-123",
            "transcript_path": str(transcript_file),
            "hook_event_name": "PreCompact",
            "trigger": "auto"
        }

        # Run hook
        start = time.perf_counter()

        result = subprocess.run(
            ["python", str(hook_path)],
            input=json.dumps(hook_input),
            capture_output=True,
            text=True,
            timeout=1.0,
            env={"CLAUDE_PROJECT_DIR": str(nexus_root)}
        )

        elapsed_ms = (time.perf_counter() - start) * 1000

        # Test 1: Hook returns {}
        print("=" * 80)
        print("TEST 1: Hook Returns {}")
        print("=" * 80)

        try:
            output = json.loads(result.stdout.strip())
            if output == {}:
                print("[OK] PASS: Hook returned empty object")
            else:
                print(f"[FAIL] FAIL: Hook returned {output} instead of {{}}")
                return False
        except json.JSONDecodeError as e:
            print(f"[FAIL] FAIL: Invalid JSON output: {e}")
            print(f"stdout: {result.stdout}")
            return False

        print()

        # Test 2: precompact_state.json exists
        print("=" * 80)
        print("TEST 2: State File Created")
        print("=" * 80)

        state_file = nexus_root / "00-system" / ".cache" / "precompact_state.json"

        if not state_file.exists():
            print(f"[FAIL] FAIL: State file not created at {state_file}")
            if result.stderr:
                print(f"stderr: {result.stderr}")
            return False

        print(f"[OK] PASS: State file exists")
        print()

        # Test 3: Validate FLAT schema
        print("=" * 80)
        print("TEST 3: FLAT Schema Validation")
        print("=" * 80)

        state = json.loads(state_file.read_text(encoding="utf-8"))
        print("Schema contents:")
        print(json.dumps(state, indent=2))
        print()

        # Check FLAT structure
        if "project_detection" in state:
            print("[FAIL] FAIL: Schema is NESTED (has 'project_detection' key)")
            return False

        # Required fields
        required = ["active_project_id", "confidence", "detection_method", "timestamp"]
        for field in required:
            if field not in state:
                print(f"[FAIL] FAIL: Missing required field: {field}")
                return False

        # Validate detected project
        expected_project_id = "24-project-skills-research-resume-expansion"
        if state.get("active_project_id") == expected_project_id:
            print(f"[OK] PASS: Detected project: {expected_project_id}")
        else:
            print(f"[FAIL] FAIL: Expected project {expected_project_id}, got {state.get('active_project_id')}")
            return False

        # Validate confidence
        if state.get("confidence") in ("high", "medium", "low"):
            print(f"[OK] PASS: Valid confidence: {state.get('confidence')}")
        else:
            print(f"[FAIL] FAIL: Invalid confidence: {state.get('confidence')}")
            return False

        # Validate detection method
        if state.get("detection_method") in ("transcript", "cache", "fallback"):
            print(f"[OK] PASS: Valid detection method: {state.get('detection_method')}")
        else:
            print(f"[FAIL] FAIL: Invalid detection_method: {state.get('detection_method')}")
            return False

        print()

        # Test 4: Performance
        print("=" * 80)
        print("TEST 4: Performance <50ms")
        print("=" * 80)

        if elapsed_ms < 50:
            print(f"[OK] PASS: Hook executed in {elapsed_ms:.2f}ms")
        else:
            print(f"[WARN] WARNING: Hook took {elapsed_ms:.2f}ms (exceeds 50ms budget)")
            # Don't fail on this - just warn

        print()

        # Clean up test state file
        if state_file.exists():
            state_file.unlink()

        return True


def main():
    try:
        success = test_hook()

        print("=" * 80)
        if success:
            print("[OK] ALL TESTS PASSED")
            print("=" * 80)
            sys.exit(0)
        else:
            print("[FAIL] TESTS FAILED")
            print("=" * 80)
            sys.exit(1)
    except Exception as e:
        print(f"[FAIL] Test error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
