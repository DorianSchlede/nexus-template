#!/usr/bin/env python3
"""
End-to-End Integration Test: PreCompact → SessionStart Flow

Simulates the complete resume workflow:
1. PreCompact hook detects active project and writes state
2. SessionStart hook reads state and injects resume instructions
"""

import json
import subprocess
import tempfile
import time
from pathlib import Path


def run_hook(hook_name: str, hook_path: Path, input_data: dict, project_dir: Path) -> tuple[dict, str, float]:
    """Run a hook and return output, stderr, elapsed time."""
    start = time.perf_counter()

    result = subprocess.run(
        ["python", str(hook_path)],
        input=json.dumps(input_data),
        capture_output=True,
        text=True,
        timeout=2.0,
        env={"CLAUDE_PROJECT_DIR": str(project_dir)}
    )

    elapsed_ms = (time.perf_counter() - start) * 1000

    try:
        output = json.loads(result.stdout.strip())
    except json.JSONDecodeError as e:
        print(f"[ERROR] {hook_name} output is not valid JSON: {e}")
        print(f"stdout: {result.stdout}")
        raise

    return output, result.stderr, elapsed_ms


def test_end_to_end_flow():
    """Test complete PreCompact -> SessionStart flow."""
    print("=" * 80)
    print("END-TO-END INTEGRATION TEST")
    print("PreCompact Hook -> SessionStart Hook")
    print("=" * 80)
    print()

    script_dir = Path(__file__).parent
    nexus_root = script_dir.parent.parent.parent

    precompact_hook = nexus_root / ".claude" / "hooks" / "save_resume_state.py"
    sessionstart_hook = nexus_root / ".claude" / "hooks" / "session_start.py"

    if not precompact_hook.exists():
        print(f"[FAIL] PreCompact hook not found: {precompact_hook}")
        return False

    if not sessionstart_hook.exists():
        print(f"[FAIL] SessionStart hook not found: {sessionstart_hook}")
        return False

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)

        # Setup: Create mock project with resume-context.md
        project_id = "99-test-e2e"
        project_dir = tmp_path / "02-projects" / project_id / "01-planning"
        project_dir.mkdir(parents=True, exist_ok=True)

        resume_file = project_dir / "resume-context.md"
        resume_content = """---
project_id: 99-test-e2e
project_name: End-to-End Test Project
current_phase: Phase 2
progress: 75%
next_action: execute-project
files_to_load:
  - 01-planning/overview.md
  - 01-planning/steps.md
---

# Resume Context

## Validation Gate

Before continuing, answer:

1. What is the current phase?
2. What is the progress percentage?
3. What skill should be executed next?

## Context

This project tests the complete PreCompact → SessionStart resume flow.
"""
        resume_file.write_text(resume_content, encoding="utf-8")

        # Setup: Create mock transcript with project activity
        # Use paths that match PreCompact detection pattern: 02-projects/{id}/
        transcript_file = tmp_path / "transcript.jsonl"
        transcript_entries = [
            {"type": "tool_use", "name": "Read", "input": {"file_path": f"02-projects/{project_id}/01-planning/overview.md"}},
            {"type": "tool_use", "name": "Write", "input": {"file_path": f"02-projects/{project_id}/03-working/test.py"}},
        ]

        with open(transcript_file, "w", encoding="utf-8") as f:
            for entry in transcript_entries:
                f.write(json.dumps(entry) + "\n")

        print("STEP 1: Run PreCompact Hook")
        print("-" * 80)

        precompact_input = {
            "session_id": "e2e-session-123",
            "transcript_path": str(transcript_file),
            "hook_event_name": "PreCompact",
            "trigger": "auto"
        }

        precompact_output, precompact_stderr, precompact_time = run_hook(
            "PreCompact", precompact_hook, precompact_input, tmp_path
        )

        # Verify PreCompact returned {}
        if precompact_output != {}:
            print(f"[FAIL] PreCompact should return {{}}, got: {precompact_output}")
            return False

        print(f"[OK] PreCompact returned empty object")
        print(f"[OK] PreCompact execution time: {precompact_time:.2f}ms")

        # Verify precompact_state.json was created
        state_file = tmp_path / "00-system" / ".cache" / "precompact_state.json"
        if not state_file.exists():
            print(f"[FAIL] precompact_state.json not created")
            return False

        state = json.loads(state_file.read_text(encoding="utf-8"))
        print(f"[OK] precompact_state.json created")
        print(f"[INFO] State: {json.dumps(state, indent=2)}")

        # Verify detected project
        if state.get("active_project_id") != project_id:
            print(f"[FAIL] Expected project {project_id}, got {state.get('active_project_id')}")
            return False

        print(f"[OK] Detected project: {project_id}")
        print()

        print("STEP 2: Run SessionStart Hook (source=compact)")
        print("-" * 80)

        sessionstart_input = {
            "session_id": "e2e-session-456",
            "hook_event_name": "SessionStart",
            "source": "compact",
            "trigger": "auto"
        }

        sessionstart_output, sessionstart_stderr, sessionstart_time = run_hook(
            "SessionStart", sessionstart_hook, sessionstart_input, tmp_path
        )

        # Verify SessionStart returned hookSpecificOutput
        if "hookSpecificOutput" not in sessionstart_output:
            print(f"[FAIL] SessionStart should return hookSpecificOutput")
            print(f"Output keys: {list(sessionstart_output.keys())}")
            return False

        hook_output = sessionstart_output["hookSpecificOutput"]
        if "additionalContext" not in hook_output:
            print(f"[FAIL] No additionalContext in hookSpecificOutput")
            return False

        context = hook_output["additionalContext"]

        print(f"[OK] SessionStart returned hookSpecificOutput.additionalContext")
        print(f"[OK] SessionStart execution time: {sessionstart_time:.2f}ms")
        print(f"[OK] Context length: {len(context)} chars")
        print()

        print("STEP 3: Verify Resume Instructions")
        print("-" * 80)

        # Check for required resume instructions
        required_strings = [
            "MANDATORY: Resume Project After Compaction",
            "End-to-End Test Project",
            project_id,
            "Phase 2",
            "75%",
            "STEP 1: Load Required Files",
            "01-planning/overview.md",
            "01-planning/steps.md",
            "STEP 2: Validation Gate",
            "What is the current phase?",
            "What is the progress percentage?",
            "STEP 3: Execute Skill",
            "execute-project"
        ]

        missing = []
        for s in required_strings:
            if s not in context:
                missing.append(s)

        if missing:
            print(f"[FAIL] Missing required strings:")
            for s in missing:
                print(f"  - {s}")
            print(f"\nContext preview:\n{context[:1000]}")
            return False

        print(f"[OK] All required resume instructions present")
        print()

        print("STEP 4: Debug Information")
        print("-" * 80)

        # Parse and display injected context structure
        print("Injected Resume Instructions:")
        print()

        # Extract sections
        if "STEP 1:" in context:
            step1_start = context.find("STEP 1:")
            step1_end = context.find("STEP 2:", step1_start) if "STEP 2:" in context else len(context)
            step1 = context[step1_start:step1_end].strip()
            print(f"  [OK] STEP 1 found ({len(step1)} chars)")
        else:
            print(f"  [WARN] STEP 1 not found")

        if "STEP 2:" in context:
            step2_start = context.find("STEP 2:")
            step2_end = context.find("STEP 3:", step2_start) if "STEP 3:" in context else len(context)
            step2 = context[step2_start:step2_end].strip()
            print(f"  [OK] STEP 2 found ({len(step2)} chars)")

            # Count validation questions
            validation_questions = step2.count("?")
            print(f"      Validation questions: {validation_questions}")
        else:
            print(f"  [WARN] STEP 2 not found")

        if "STEP 3:" in context:
            step3_start = context.find("STEP 3:")
            step3 = context[step3_start:].strip()
            print(f"  [OK] STEP 3 found ({len(step3)} chars)")
        else:
            print(f"  [WARN] STEP 3 not found")

        # Check file loading instructions
        files_in_context = context.count("01-planning/")
        print(f"\n  Files to load: {files_in_context} references")

        # Check metadata
        metadata_fields = ["Project Detected:", "Phase:", "Progress:"]
        for field in metadata_fields:
            if field in context:
                # Extract value after field
                field_start = context.find(field)
                field_end = context.find("\n", field_start)
                value = context[field_start:field_end]
                print(f"  [OK] {field} {value.split(field)[1].strip()}")
            else:
                print(f"  [WARN] {field} not found")

        print()

        print("STEP 5: Performance Analysis")
        print("-" * 80)

        total_time = precompact_time + sessionstart_time

        print(f"PreCompact: {precompact_time:.2f}ms")
        print(f"SessionStart: {sessionstart_time:.2f}ms")
        print(f"Total: {total_time:.2f}ms")

        if precompact_time < 50:
            print(f"[OK] PreCompact under 50ms budget")
        else:
            print(f"[WARN] PreCompact exceeded 50ms budget")

        if sessionstart_time < 200:
            print(f"[OK] SessionStart under 200ms budget")
        else:
            print(f"[WARN] SessionStart exceeded 200ms budget")

        if total_time < 250:
            print(f"[OK] Total time under 250ms combined budget")
        else:
            print(f"[WARN] Total time exceeded 250ms combined budget")

        print()
        print("=" * 80)
        print("[OK] END-TO-END TEST PASSED")
        print("=" * 80)
        print()
        print("Summary:")
        print("1. PreCompact detected active project from transcript")
        print("2. PreCompact wrote FLAT JSON schema to .cache/")
        print("3. SessionStart read state and loaded resume-context.md")
        print("4. SessionStart injected catastrophic instructions")
        print("5. All required resume data present in context")

        return True


def main():
    try:
        success = test_end_to_end_flow()

        if success:
            print("\n[OK] Integration test PASSED")
            return 0
        else:
            print("\n[FAIL] Integration test FAILED")
            return 1

    except Exception as e:
        print(f"[FAIL] Test error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
