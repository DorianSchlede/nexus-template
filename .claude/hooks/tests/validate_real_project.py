"""
Validate project_state utility against real project 28.
"""

from pathlib import Path
import sys

# Add hooks to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.project_state import detect_project_state, find_most_recent_project_enhanced

def main():
    # Test Project 28
    project_path = Path("02-projects/28-handover-test-suite")

    print("=== Testing Real Project Detection ===\n")

    # Test single project state detection
    print("1. Detecting Project 28 state...")
    state = detect_project_state(project_path)

    if state:
        print(f"   Project: {state.project_id} - {state.name}")
        print(f"   Status: {state.status}")
        print(f"   Phase: {state.current_phase} -> {state.next_action}")
        print(f"   Progress: {state.tasks_completed}/{state.tasks_total} ({state.progress_percent}%)")
        print(f"   Section: {state.current_section}")
        print(f"   Session IDs: {state.session_ids}")
        print(f"   Last Updated: {state.last_updated}")
        print(f"   Created: {state.created}")
        print("   SUCCESS!\n")
    else:
        print("   FAILED: Could not detect project state\n")
        return 1

    # Test most recent project detection
    print("2. Finding most recent project...")
    projects_dir = Path("02-projects")
    most_recent = find_most_recent_project_enhanced(projects_dir)

    if most_recent:
        print(f"   Most Recent: {most_recent.project_id} - {most_recent.name}")
        print(f"   Progress: {most_recent.progress_percent}%")
        print(f"   SUCCESS!\n")
    else:
        print("   FAILED: No projects found\n")
        return 1

    print("=== All Real Project Tests Passed ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
