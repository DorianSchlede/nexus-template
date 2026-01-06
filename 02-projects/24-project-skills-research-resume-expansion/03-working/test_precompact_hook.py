#!/usr/bin/env python3
"""
Test PreCompact Hook Implementation

Validates:
1. Hook outputs FLAT JSON schema
2. Hook returns {} (empty object)
3. Hook executes in <50ms
4. Hook redacts secrets properly
5. Schema matches Phase 0 precompact_state_v1.json
"""

import json
import subprocess
import sys
import time
from pathlib import Path

# Test fixture: mock hook input
MOCK_HOOK_INPUT = {
    "session_id": "test-session-123",
    "transcript_path": "~/.claude/test-transcript.jsonl",
    "hook_event_name": "PreCompact",
    "trigger": "auto",
    "custom_instructions": ""
}


def run_hook(hook_path: Path, input_data: dict) -> tuple[str, str, float]:
    """
    Run hook with mock input and capture output.

    Returns:
        Tuple of (stdout, stderr, elapsed_ms)
    """
    start = time.perf_counter()

    result = subprocess.run(
        ["python", str(hook_path)],
        input=json.dumps(input_data),
        capture_output=True,
        text=True,
        timeout=1.0  # Generous timeout (should be <50ms)
    )

    elapsed_ms = (time.perf_counter() - start) * 1000

    return result.stdout, result.stderr, elapsed_ms


def validate_flat_schema(state: dict) -> list[str]:
    """
    Validate FLAT schema structure.

    Required fields (all at top level, NOT nested):
    - active_project_id: string | null
    - confidence: "high" | "medium" | "low"
    - detection_method: "transcript" | "cache" | "fallback"
    - timestamp: ISO-8601 string
    """
    errors = []

    # Check top-level structure (no nesting)
    if "project_detection" in state:
        errors.append("CRITICAL: Schema is NESTED (has 'project_detection' key) - MUST be FLAT")

    # Required fields
    required_fields = {
        "active_project_id": (str, type(None)),
        "confidence": str,
        "detection_method": str,
        "timestamp": str
    }

    for field, expected_types in required_fields.items():
        if field not in state:
            errors.append(f"Missing required field: {field}")
        elif not isinstance(state[field], expected_types):
            errors.append(f"Field '{field}' has wrong type: {type(state[field]).__name__} (expected {expected_types})")

    # Validate enums
    if "confidence" in state and state["confidence"] not in ("high", "medium", "low"):
        errors.append(f"Invalid confidence value: {state['confidence']} (must be high/medium/low)")

    if "detection_method" in state and state["detection_method"] not in ("transcript", "cache", "fallback"):
        errors.append(f"Invalid detection_method: {state['detection_method']} (must be transcript/cache/fallback)")

    # Validate timestamp format (basic ISO-8601 check)
    if "timestamp" in state:
        ts = state["timestamp"]
        if not (isinstance(ts, str) and "T" in ts and ts.endswith("Z")):
            errors.append(f"Invalid timestamp format: {ts} (must be ISO-8601 with Z suffix)")

    return errors


def test_hook_output(hook_path: Path, nexus_root: Path) -> dict:
    """Run all hook tests."""
    results = {
        "passed": [],
        "failed": [],
        "warnings": []
    }

    print("=" * 80)
    print("TEST 1: Hook Returns Empty Object {}")
    print("=" * 80)

    try:
        stdout, stderr, elapsed_ms = run_hook(hook_path, MOCK_HOOK_INPUT)

        # Parse hook output
        try:
            output = json.loads(stdout.strip())
        except json.JSONDecodeError as e:
            results["failed"].append(f"Test 1 FAILED: Hook output is not valid JSON: {e}")
            print(f"[FAIL] FAIL: Output is not valid JSON")
            print(f"   stdout: {stdout}")
            return results

        # Check if output is empty object
        if output == {}:
            results["passed"].append("Test 1: Hook returns {} OK")
            print(f"[OK] PASS: Hook returns empty object")
        else:
            results["failed"].append(f"Test 1 FAILED: Hook returned {output} instead of {{}}")
            print(f"[FAIL] FAIL: Hook returned {output} instead of {{}}")

    except Exception as e:
        results["failed"].append(f"Test 1 FAILED: {e}")
        print(f"[FAIL] FAIL: {e}")

    print()

    # Test 2: Check precompact_state.json was written
    print("=" * 80)
    print("TEST 2: precompact_state.json Written with FLAT Schema")
    print("=" * 80)

    state_file = nexus_root / "00-system" / ".cache" / "precompact_state.json"

    if not state_file.exists():
        results["failed"].append("Test 2 FAILED: precompact_state.json not found")
        print(f"[FAIL] FAIL: File not found at {state_file}")
        return results

    try:
        state = json.loads(state_file.read_text(encoding="utf-8"))
        print(f"[OK] PASS: File exists and is valid JSON")
        print(f"\nSchema contents:")
        print(json.dumps(state, indent=2))

        # Validate FLAT schema
        schema_errors = validate_flat_schema(state)
        if schema_errors:
            for error in schema_errors:
                results["failed"].append(f"Test 2 Schema Error: {error}")
                print(f"[FAIL] SCHEMA ERROR: {error}")
        else:
            results["passed"].append("Test 2: FLAT schema validation OK")
            print(f"\n[OK] PASS: Schema structure is FLAT and valid")

    except Exception as e:
        results["failed"].append(f"Test 2 FAILED: {e}")
        print(f"[FAIL] FAIL: {e}")

    print()

    # Test 3: Performance <50ms
    print("=" * 80)
    print("TEST 3: Performance <50ms")
    print("=" * 80)

    if elapsed_ms < 50:
        results["passed"].append(f"Test 3: Performance {elapsed_ms:.2f}ms OK")
        print(f"[OK] PASS: Hook executed in {elapsed_ms:.2f}ms (< 50ms budget)")
    else:
        results["failed"].append(f"Test 3 FAILED: Hook took {elapsed_ms:.2f}ms (>50ms)")
        print(f"[FAIL] FAIL: Hook took {elapsed_ms:.2f}ms (exceeds 50ms budget)")

    print()

    # Test 4: Secret Redaction (check for common patterns)
    print("=" * 80)
    print("TEST 4: Secret Redaction")
    print("=" * 80)

    state_json = state_file.read_text(encoding="utf-8")

    # Patterns that should NOT appear in state file
    forbidden_patterns = [
        (r'sk_[a-zA-Z0-9]{20,}', "Stripe/OpenAI secret keys"),
        (r'Bearer [a-zA-Z0-9._-]{20,}', "Bearer tokens"),
        (r'@gmail\.com', "Email addresses (specific)"),
    ]

    redaction_passed = True
    for pattern, description in forbidden_patterns:
        import re
        if re.search(pattern, state_json):
            results["failed"].append(f"Test 4 FAILED: Found {description} in state file (not redacted)")
            print(f"[FAIL] FAIL: Found {description} (not redacted)")
            redaction_passed = False

    if redaction_passed:
        results["passed"].append("Test 4: Secret redaction OK")
        print(f"[OK] PASS: No secrets detected in state file")

    return results


def main():
    # Find hook and nexus root
    script_dir = Path(__file__).parent
    project_root = script_dir.parent.parent.parent  # Up to strategy-nexus
    hook_path = project_root / ".claude" / "hooks" / "save_resume_state.py"

    if not hook_path.exists():
        print(f"ERROR: Hook not found at {hook_path}")
        sys.exit(1)

    print("Testing PreCompact Hook Implementation")
    print(f"Hook: {hook_path}")
    print(f"Nexus Root: {project_root}")
    print()

    # Run tests
    results = test_hook_output(hook_path, project_root)

    # Summary
    print()
    print("=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)

    print(f"\n[OK] PASSED: {len(results['passed'])}")
    for test in results['passed']:
        print(f"   - {test}")

    if results['warnings']:
        print(f"\n[WARN] WARNINGS: {len(results['warnings'])}")
        for warning in results['warnings']:
            print(f"   - {warning}")

    if results['failed']:
        print(f"\n[FAIL] FAILED: {len(results['failed'])}")
        for failure in results['failed']:
            print(f"   - {failure}")
        print()
        print("=" * 80)
        sys.exit(1)
    else:
        print()
        print("=" * 80)
        print("[OK] ALL TESTS PASSED")
        print("=" * 80)
        sys.exit(0)


if __name__ == "__main__":
    main()
