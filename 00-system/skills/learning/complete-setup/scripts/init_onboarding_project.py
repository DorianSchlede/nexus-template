#!/usr/bin/env python3
"""
init_onboarding_project.py - Initialize onboarding project structure

Creates 02-builds/00-onboarding-session/ with:
- 01-planning/ (with overview.md and steps.md)
- 02-resources/ (for file-analysis.json)
- 03-working/ (with input/ symlink to 04-workspace/input/)
- 04-outputs/

Run this at the start of setup-system skill execution.

Usage:
    python init_onboarding_project.py [--workspace /path/to/nexus]
"""

import os
import sys
from pathlib import Path
from datetime import datetime


def get_workspace_root() -> Path:
    """Get workspace root from args or detect from script location."""
    if len(sys.argv) > 2 and sys.argv[1] == "--workspace":
        return Path(sys.argv[2])

    # Script is at: 00-system/skills/learning/setup-system/scripts/
    # Workspace is 5 levels up
    script_path = Path(__file__).resolve()
    return script_path.parent.parent.parent.parent.parent.parent


def init_onboarding_project(workspace: Path) -> dict:
    """
    Initialize onboarding project structure.

    Args:
        workspace: Path to Nexus workspace root

    Returns:
        dict with status and created paths
    """
    project_path = workspace / "02-builds" / "00-onboarding-session"
    created_paths = []

    # Create standard 4 subfolders
    folders = [
        "01-planning",
        "02-resources",
        "03-working",
        "04-outputs"
    ]

    for folder in folders:
        folder_path = project_path / folder
        folder_path.mkdir(parents=True, exist_ok=True)
        created_paths.append(str(folder_path.relative_to(workspace)))

    # Create overview.md
    overview_path = project_path / "01-planning" / "01-overview.md"
    if not overview_path.exists():
        overview_content = f"""---
id: 00-onboarding-session
name: Onboarding Session
status: IN_PROGRESS
description: "Initial system setup and configuration"
created: {datetime.now().strftime('%Y-%m-%d')}
build_path: 02-builds/00-onboarding-session/
---

# Onboarding Session

## Purpose

This temporary project tracks your initial Nexus setup:
- File analysis results (if you uploaded files)
- Goals and context captured during setup
- Roadmap generated from your input
- Workspace structure created

## Outputs

After setup completes:
- `01-memory/goals.md` - Your goals (loaded every session)
- `01-memory/roadmap.md` - Your planned projects
- `04-workspace/workspace-map.md` - Your folder structure
- Project scaffolds in `02-builds/`

## Lifecycle

This project will be archived to `05-archived/` after setup completes.
Your actual work happens in the builds created from your roadmap.
"""
        overview_path.write_text(overview_content, encoding='utf-8')
        created_paths.append(str(overview_path.relative_to(workspace)))

    # Create steps.md
    steps_path = project_path / "01-planning" / "04-steps.md"
    if not steps_path.exists():
        steps_content = """# Onboarding Steps

## Progress

- [ ] Step 1: Context Upload (optional)
- [ ] Step 2: Define Your Goals
- [ ] Step 3: Generate Roadmap
- [ ] Step 4: Create Workspace Structure
- [ ] Step 5: Initiate Projects
- [ ] Step 6: Save Everything
- [ ] Step 7: End Session

## Outputs Created

- [ ] goals.md saved to 01-memory/
- [ ] roadmap.md saved to 01-memory/
- [ ] workspace-map.md updated in 04-workspace/
- [ ] Project scaffolds created in 02-builds/
"""
        steps_path.write_text(steps_content, encoding='utf-8')
        created_paths.append(str(steps_path.relative_to(workspace)))

    # Create symlink: 03-working/input/ → 04-workspace/input/
    input_link = project_path / "03-working" / "input"
    target_input = workspace / "04-workspace" / "input"

    # Ensure target exists
    target_input.mkdir(parents=True, exist_ok=True)

    # Create symlink if it doesn't exist
    if not input_link.exists():
        try:
            # Use relative path for symlink
            relative_target = Path("../../../04-workspace/input")
            input_link.symlink_to(relative_target)
            created_paths.append(f"{input_link.relative_to(workspace)} -> {relative_target}")
        except OSError as e:
            # Symlink might fail on some systems, just note it
            print(f"Warning: Could not create symlink: {e}", file=sys.stderr)

    return {
        "status": "success",
        "project_path": str(project_path.relative_to(workspace)),
        "created": created_paths
    }


def main():
    workspace = get_workspace_root()

    if not workspace.exists():
        print(f"Error: Workspace not found: {workspace}", file=sys.stderr)
        sys.exit(1)

    # Validate it's a Nexus workspace
    if not (workspace / "00-system").exists():
        print(f"Error: Not a Nexus workspace (no 00-system/): {workspace}", file=sys.stderr)
        sys.exit(1)

    result = init_onboarding_project(workspace)

    print(f"Onboarding project initialized: {result['project_path']}")
    print(f"Created {len(result['created'])} paths:")
    for path in result['created']:
        print(f"  - {path}")


if __name__ == "__main__":
    main()
