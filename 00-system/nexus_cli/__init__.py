#!/usr/bin/env python3
"""Nexus CLI - Entry points for all framework hooks and build tools.

Commands use `nexus-` namespace prefix:

Lifecycle Hooks (called by Claude Code):
  - nexus-session-start       - Session start hook
  - nexus-session-end         - Session end hook
  - nexus-session-summary     - Session summary hook
  - nexus-pre-tool-use        - Pre-tool-use hook
  - nexus-post-tool-use       - Post-tool-use hook
  - nexus-user-prompt-submit  - User prompt submit hook
  - nexus-save-resume-state   - Save resume state hook

Build Management:
  - nexus-load                - Load skills, builds, or startup context
  - nexus-init-build          - Initialize a new build folder
  - nexus-bulk-complete       - Mark multiple tasks complete
  - nexus-update-resume       - Update resume-context.md

Mental Models:
  - nexus-mental-models       - Select and display mental models

Skill Development:
  - nexus-init-skill          - Initialize a new skill folder
  - nexus-package-skill       - Package a skill for sharing
  - nexus-validate-skill      - Quick validate a skill

Validation:
  - nexus-validate-workspace  - Validate workspace map accuracy

Usage: nexus-load --startup

The CLI finds the project by checking (in order):
1. CLAUDE_PROJECT_DIR environment variable (set by Claude Code)
2. Current working directory
3. Relative to the CLI module (for development)
"""

import os
import subprocess
import sys
from pathlib import Path

__version__ = "5.0.0"


def _get_project_path() -> Path:
    """Find project root - uses CLAUDE_PROJECT_DIR if set, otherwise cwd."""
    # Claude Code sets this when running hooks
    project_dir = os.environ.get("CLAUDE_PROJECT_DIR")
    if project_dir:
        return Path(project_dir)

    # Fallback: look in current directory for Nexus markers
    cwd = Path.cwd()
    if (cwd / ".claude").exists() or (cwd / "00-system").exists():
        return cwd

    # Last resort: relative to this file (for development)
    dev_root = Path(__file__).resolve().parent.parent
    if (dev_root / ".claude").exists():
        return dev_root

    return cwd


def _get_hooks_path() -> Path:
    """Find hooks directory - uses CLAUDE_PROJECT_DIR if set, otherwise cwd."""
    return _get_project_path() / ".claude" / "hooks"


def _run_hook(script_name: str) -> None:
    """Generic hook runner using uv."""
    hooks_path = _get_hooks_path()
    script = hooks_path / script_name

    if not script.exists():
        print(f"ERROR: Hook script not found: {script}", file=sys.stderr)
        print(f"", file=sys.stderr)
        print(f"Make sure you're in a Nexus project directory, or set CLAUDE_PROJECT_DIR.", file=sys.stderr)
        sys.exit(1)

    try:
        # Change to project dir if set (hooks expect this)
        project_dir = os.environ.get("CLAUDE_PROJECT_DIR")
        cwd = project_dir if project_dir else None

        result = subprocess.run(
            ["uv", "run", str(script)] + sys.argv[1:],
            cwd=cwd
        )
        sys.exit(result.returncode)
    except FileNotFoundError:
        print("ERROR: 'uv' not found. Install with: curl -LsSf https://astral.sh/uv/install.sh | sh", file=sys.stderr)
        sys.exit(1)


def _run_script(relative_path: str, extra_args: list[str] | None = None) -> None:
    """Run a script from 00-system/ directory."""
    project_path = _get_project_path()
    script = project_path / relative_path

    if not script.exists():
        print(f"ERROR: Script not found: {script}", file=sys.stderr)
        print(f"", file=sys.stderr)
        print(f"Make sure you're in a Nexus project directory, or set CLAUDE_PROJECT_DIR.", file=sys.stderr)
        sys.exit(1)

    try:
        args = ["uv", "run", str(script)]
        if extra_args:
            args.extend(extra_args)
        else:
            args.extend(sys.argv[1:])

        result = subprocess.run(args, cwd=str(project_path))
        sys.exit(result.returncode)
    except FileNotFoundError:
        print("ERROR: 'uv' not found. Install with: curl -LsSf https://astral.sh/uv/install.sh | sh", file=sys.stderr)
        sys.exit(1)


# Lifecycle hooks - called by Claude Code
def session_start_main() -> None:
    """Session start hook - initializes Nexus context."""
    _run_hook("session_start.py")


def session_end_main() -> None:
    """Session end hook - cleanup and logging."""
    _run_hook("session_end.py")


def session_summary_main() -> None:
    """Session summary hook - generates session report."""
    _run_hook("session_summary.py")


def pre_tool_use_main() -> None:
    """Pre-tool-use hook - runs before each tool invocation."""
    _run_hook("pre_tool_use.py")


def post_tool_use_main() -> None:
    """Post-tool-use hook - runs after each tool invocation."""
    _run_hook("post_tool_use.py")


def user_prompt_submit_main() -> None:
    """User prompt submit hook - processes user input."""
    _run_hook("user_prompt_submit.py")


def save_resume_state_main() -> None:
    """Save resume state hook - persists state before compact."""
    _run_hook("save_resume_state.py")


# Build management tools
def load_main() -> None:
    """Load skills, builds, or startup context.

    Usage:
        nexus-load --startup         Load startup context
        nexus-load --skill NAME      Load a specific skill
        nexus-load --build ID        Load a build by ID
        nexus-load --resume          Load from resume context
        nexus-load --list-skills     List available skills
    """
    _run_script("00-system/core/nexus-loader.py")


def init_build_main() -> None:
    """Initialize a new build folder.

    Usage:
        nexus-init-build "Build Name" --type build|research|strategy
        nexus-init-build "Build Name" --path 02-builds/active
    """
    _run_script("00-system/skills/builds/plan-build/scripts/init_build.py")


def bulk_complete_main() -> None:
    """Mark multiple tasks complete in steps.md.

    Usage:
        nexus-bulk-complete BUILD_PATH STEP_NUMBERS...
        nexus-bulk-complete 02-builds/active/01-my-build 1 2 3
    """
    _run_script("00-system/skills/builds/execute-build/scripts/bulk-complete.py")


def update_resume_main() -> None:
    """Update resume-context.md with current progress.

    Usage:
        nexus-update-resume BUILD_PATH
        nexus-update-resume 02-builds/active/01-my-build
    """
    _run_script("00-system/skills/builds/execute-build/scripts/update-resume.py")


# Mental models tools
def mental_models_main() -> None:
    """Select and display mental models for decision-making.

    Usage:
        nexus-mental-models --format brief    List models briefly
        nexus-mental-models --format full     Show full model details
        nexus-mental-models --category X      Filter by category
    """
    _run_script("00-system/mental-models/scripts/select_mental_models.py")


# Skill development tools
def init_skill_main() -> None:
    """Initialize a new skill folder structure.

    Usage:
        nexus-init-skill "Skill Name"
        nexus-init-skill "my-skill" --path 03-skills
    """
    _run_script("00-system/skills/skill-dev/create-skill/scripts/init_skill.py")


def package_skill_main() -> None:
    """Package a skill for sharing or upload.

    Usage:
        nexus-package-skill SKILL_PATH
        nexus-package-skill 03-skills/my-skill
    """
    _run_script("00-system/skills/skill-dev/create-skill/scripts/package_skill.py")


def validate_skill_main() -> None:
    """Quick validate a skill's structure and content.

    Usage:
        nexus-validate-skill SKILL_PATH
        nexus-validate-skill 03-skills/my-skill
    """
    _run_script("00-system/skills/skill-dev/create-skill/scripts/quick_validate.py")


# Validation tools
def validate_workspace_main() -> None:
    """Validate workspace map accuracy against actual folders.

    Usage:
        nexus-validate-workspace
        nexus-validate-workspace --fix   Auto-fix discrepancies
    """
    _run_script("00-system/skills/system/update-workspace-map/scripts/validate-workspace.py")
