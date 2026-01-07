#!/usr/bin/env python3
"""
Initialize Test Folder Structure in a Project

Creates the 02-resources/tests/ folder with scenarios.yaml template.

Usage:
    python init-tests.py --project 41-integrated-subagent-testing-system
    python init-tests.py --project-path 02-projects/41-integrated-subagent-testing-system
"""

import argparse
import shutil
import sys
from pathlib import Path


def get_repo_root() -> Path:
    """Get the repository root by looking for .git folder."""
    current = Path(__file__).resolve()
    while current != current.parent:
        if (current / ".git").exists():
            return current
        current = current.parent
    raise RuntimeError("Not in a git repository")


def find_project(project_id: str, repo_root: Path) -> Path:
    """Find project folder by ID."""
    projects_dir = repo_root / "02-projects"

    # Try exact match first
    for folder in projects_dir.iterdir():
        if folder.is_dir() and folder.name == project_id:
            return folder
        # Also try partial match (e.g., "41" matches "41-integrated-...")
        if folder.is_dir() and folder.name.startswith(f"{project_id}-"):
            return folder

    raise ValueError(f"Project not found: {project_id}")


def init_tests(project_path: Path, repo_root: Path) -> dict:
    """Initialize test folder structure in a project."""
    results = {
        "project": str(project_path.relative_to(repo_root)),
        "created": [],
        "skipped": [],
        "errors": []
    }

    # Create 02-resources/tests/ folder
    tests_dir = project_path / "02-resources" / "tests"

    if tests_dir.exists():
        results["skipped"].append(str(tests_dir.relative_to(repo_root)))
        print(f"[SKIP] Test folder already exists: {tests_dir}")
    else:
        tests_dir.mkdir(parents=True, exist_ok=True)
        results["created"].append(str(tests_dir.relative_to(repo_root)))
        print(f"[OK] Created test folder: {tests_dir}")

    # Copy scenarios template
    template_path = repo_root / "00-system" / "skills" / "system" / "validate-feature" / "templates" / "scenarios-template.yaml"
    scenarios_path = tests_dir / "scenarios.yaml"

    if scenarios_path.exists():
        results["skipped"].append(str(scenarios_path.relative_to(repo_root)))
        print(f"[SKIP] Scenarios file already exists: {scenarios_path}")
    else:
        if template_path.exists():
            # Read template and replace project_id placeholder
            content = template_path.read_text(encoding="utf-8")
            project_id = project_path.name
            content = content.replace("{PROJECT-ID}", project_id)

            scenarios_path.write_text(content, encoding="utf-8")
            results["created"].append(str(scenarios_path.relative_to(repo_root)))
            print(f"[OK] Created scenarios file: {scenarios_path}")
        else:
            results["errors"].append(f"Template not found: {template_path}")
            print(f"[ERROR] Template not found: {template_path}")

    # Create 04-outputs/validation-reports/ folder
    reports_dir = project_path / "04-outputs" / "validation-reports"

    if reports_dir.exists():
        results["skipped"].append(str(reports_dir.relative_to(repo_root)))
        print(f"[SKIP] Reports folder already exists: {reports_dir}")
    else:
        reports_dir.mkdir(parents=True, exist_ok=True)
        results["created"].append(str(reports_dir.relative_to(repo_root)))
        print(f"[OK] Created reports folder: {reports_dir}")

        # Add .gitkeep
        gitkeep = reports_dir / ".gitkeep"
        gitkeep.touch()

    return results


def main():
    parser = argparse.ArgumentParser(
        description="Initialize test folder structure in a project"
    )
    parser.add_argument(
        "--project", "-p", type=str,
        help="Project ID or name (e.g., '41' or '41-integrated-subagent-testing-system')"
    )
    parser.add_argument(
        "--project-path", type=str,
        help="Full path to project folder"
    )

    args = parser.parse_args()

    if not args.project and not args.project_path:
        print("Error: Specify --project or --project-path")
        sys.exit(1)

    repo_root = get_repo_root()

    if args.project_path:
        project_path = Path(args.project_path)
        if not project_path.is_absolute():
            project_path = repo_root / project_path
    else:
        project_path = find_project(args.project, repo_root)

    if not project_path.exists():
        print(f"Error: Project path does not exist: {project_path}")
        sys.exit(1)

    print(f"\nInitializing tests for: {project_path.name}")
    print("=" * 60)

    results = init_tests(project_path, repo_root)

    print("\n" + "=" * 60)
    print(f"Created: {len(results['created'])} items")
    print(f"Skipped: {len(results['skipped'])} items (already exist)")

    if results["errors"]:
        print(f"Errors: {len(results['errors'])}")
        for err in results["errors"]:
            print(f"  - {err}")

    print("\nNext steps:")
    print(f"  1. Edit {project_path.name}/02-resources/tests/scenarios.yaml")
    print(f"  2. Define your test scenarios")
    print(f"  3. Run: python scripts/run-tests.py --project {project_path.name}")


if __name__ == "__main__":
    main()
