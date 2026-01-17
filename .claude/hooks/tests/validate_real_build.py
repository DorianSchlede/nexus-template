"""
Validate build_state utility against real build 28.
"""

from pathlib import Path
import sys

# Add hooks to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.build_state import detect_build_state, find_most_recent_build_enhanced

def main():
    # Test Build 28
    build_path = Path("02-builds/28-handover-test-suite")

    print("=== Testing Real Build Detection ===\n")

    # Test single build state detection
    print("1. Detecting Build 28 state...")
    state = detect_build_state(build_path)

    if state:
        print(f"   Build: {state.build_id} - {state.name}")
        print(f"   Status: {state.status}")
        print(f"   Phase: {state.current_phase} -> {state.next_action}")
        print(f"   Progress: {state.tasks_completed}/{state.tasks_total} ({state.progress_percent}%)")
        print(f"   Section: {state.current_section}")
        print(f"   Session IDs: {state.session_ids}")
        print(f"   Last Updated: {state.last_updated}")
        print(f"   Created: {state.created}")
        print("   SUCCESS!\n")
    else:
        print("   FAILED: Could not detect build state\n")
        return 1

    # Test most recent build detection
    print("2. Finding most recent build...")
    builds_dir = Path("02-builds")
    most_recent = find_most_recent_build_enhanced(builds_dir)

    if most_recent:
        print(f"   Most Recent: {most_recent.build_id} - {most_recent.name}")
        print(f"   Progress: {most_recent.progress_percent}%")
        print(f"   SUCCESS!\n")
    else:
        print("   FAILED: No builds found\n")
        return 1

    print("=== All Real Build Tests Passed ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
