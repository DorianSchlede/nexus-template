#!/usr/bin/env python3
"""
Debug test to trace SessionStart hook execution.
"""

import json
import subprocess
import tempfile
from pathlib import Path


def main():
    # Create temp directory
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)

        # Create precompact_state.json
        cache_dir = tmp_path / "00-system" / ".cache"
        cache_dir.mkdir(parents=True, exist_ok=True)

        state_file = cache_dir / "precompact_state.json"
        state = {
            "active_project_id": "99-test-debug",
            "confidence": "high",
            "detection_method": "transcript",
            "timestamp": "2026-01-04T12:00:00Z"
        }
        state_file.write_text(json.dumps(state, indent=2), encoding="utf-8")

        print(f"Created precompact_state.json: {state_file}")
        print(f"Contents: {json.dumps(state, indent=2)}")
        print()

        # Create resume-context.md
        project_dir = tmp_path / "02-projects" / "99-test-debug" / "01-planning"
        project_dir.mkdir(parents=True, exist_ok=True)

        resume_file = project_dir / "resume-context.md"
        content = """---
project_id: 99-test-debug
project_name: Debug Test
current_phase: Phase 1
progress: 50%
next_action: execute-project
files_to_load:
  - file1.md
  - file2.md
---

# Resume Context

## Validation Gate

Test validation gate content.
"""
        resume_file.write_text(content, encoding="utf-8")

        print(f"Created resume-context.md: {resume_file}")
        print()

        # Run hook
        hook_path = Path(__file__).parent.parent.parent.parent / ".claude" / "hooks" / "session_start.py"

        hook_input = {
            "session_id": "test-debug-123",
            "hook_event_name": "SessionStart",
            "source": "compact",  # TOP LEVEL
            "trigger": "auto"
        }

        print(f"Running hook: {hook_path}")
        print(f"Project dir: {tmp_path}")
        print(f"Hook input: {json.dumps(hook_input, indent=2)}")
        print()

        result = subprocess.run(
            ["python", str(hook_path)],
            input=json.dumps(hook_input),
            capture_output=True,
            text=True,
            timeout=2.0,
            env={"CLAUDE_PROJECT_DIR": str(tmp_path)}
        )

        print("=" * 80)
        print("HOOK STDOUT:")
        print("=" * 80)
        print(result.stdout)
        print()

        print("=" * 80)
        print("HOOK STDERR:")
        print("=" * 80)
        print(result.stderr if result.stderr else "(empty)")
        print()

        # Check log file
        log_file = cache_dir / "session_start_output.log"
        if log_file.exists():
            print("=" * 80)
            print("HOOK LOG FILE:")
            print("=" * 80)
            print(log_file.read_text(encoding="utf-8"))
        else:
            print("No log file created")


if __name__ == "__main__":
    main()
