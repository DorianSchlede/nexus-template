#!/usr/bin/env python3
"""
Reset Instance Script

Resets a Nexus instance to initial clean state.

Commands:
    scan    - Returns JSON manifest of what will be reset
    execute - Performs the reset operations

Flags:
    --include-skills - Also clear user skills in 03-skills/
"""

import argparse
import json
import shutil
import sys
from pathlib import Path

# ============================================================================
# Constants
# ============================================================================

# Find Nexus root (script is in 00-system/skills/system/reset-instance/scripts/)
SCRIPT_DIR = Path(__file__).parent
NEXUS_ROOT = SCRIPT_DIR.parent.parent.parent.parent.parent

# Templates
TEMPLATES_DIR = NEXUS_ROOT / "00-system" / "core" / "nexus" / "templates"

# File mappings: template source -> target destination
FILE_MAPPINGS = {
    TEMPLATES_DIR / "goals.md": NEXUS_ROOT / "01-memory" / "goals.md",
    TEMPLATES_DIR / "user-config.yaml": NEXUS_ROOT / "01-memory" / "user-config.yaml",
    TEMPLATES_DIR / "core-learnings.md": NEXUS_ROOT / "01-memory" / "core-learnings.md",
    TEMPLATES_DIR / "workspace-map.md": NEXUS_ROOT / "04-workspace" / "workspace-map.md",
}

# Paths to delete
DELETE_PATHS = {
    "roadmap": NEXUS_ROOT / "01-memory" / "roadmap.yaml",
    "setup_marker": NEXUS_ROOT / ".claude" / ".setup_complete",
}

# Folders to clear (delete contents, keep folder)
CLEAR_FOLDERS = {
    "session_reports": NEXUS_ROOT / "01-memory" / "session-reports",
    "builds_active": NEXUS_ROOT / "02-builds" / "active",
    "builds_complete": NEXUS_ROOT / "02-builds" / "complete",
}

# Folders to delete entirely
DELETE_FOLDERS = {
    "input": NEXUS_ROOT / "01-memory" / "input",
}

# User skills folder
SKILLS_FOLDER = NEXUS_ROOT / "03-skills"


# ============================================================================
# Scan Functions
# ============================================================================

def scan_instance() -> dict:
    """Scan instance and return manifest of what will be reset."""
    manifest = {
        "files_to_restore": [],
        "files_to_delete": [],
        "folders_to_clear": [],
        "folders_to_delete": [],
        "builds": {"active": 0, "complete": 0},
        "skills_found": 0,
        "warnings": [],
    }

    # Check template files exist
    for template, target in FILE_MAPPINGS.items():
        if template.exists():
            manifest["files_to_restore"].append({
                "template": str(template.relative_to(NEXUS_ROOT)),
                "target": str(target.relative_to(NEXUS_ROOT)),
                "target_exists": target.exists(),
            })
        else:
            manifest["warnings"].append(f"Template missing: {template.relative_to(NEXUS_ROOT)}")

    # Check files to delete
    for name, path in DELETE_PATHS.items():
        if path.exists():
            manifest["files_to_delete"].append(str(path.relative_to(NEXUS_ROOT)))

    # Check folders to clear
    for name, folder in CLEAR_FOLDERS.items():
        if folder.exists():
            items = list(folder.iterdir())
            count = len(items)
            manifest["folders_to_clear"].append({
                "path": str(folder.relative_to(NEXUS_ROOT)),
                "item_count": count,
            })
            if name == "builds_active":
                manifest["builds"]["active"] = count
            elif name == "builds_complete":
                manifest["builds"]["complete"] = count

    # Check folders to delete entirely
    for name, folder in DELETE_FOLDERS.items():
        if folder.exists():
            manifest["folders_to_delete"].append(str(folder.relative_to(NEXUS_ROOT)))

    # Count user skills
    if SKILLS_FOLDER.exists():
        skills = [d for d in SKILLS_FOLDER.iterdir() if d.is_dir() and d.name != "__pycache__"]
        manifest["skills_found"] = len(skills)

    return manifest


# ============================================================================
# Reset Operations
# ============================================================================

def restore_memory_files() -> list[str]:
    """Restore memory files from templates."""
    results = []
    memory_templates = {
        TEMPLATES_DIR / "goals.md": NEXUS_ROOT / "01-memory" / "goals.md",
        TEMPLATES_DIR / "user-config.yaml": NEXUS_ROOT / "01-memory" / "user-config.yaml",
        TEMPLATES_DIR / "core-learnings.md": NEXUS_ROOT / "01-memory" / "core-learnings.md",
    }

    for template, target in memory_templates.items():
        if template.exists():
            shutil.copy2(template, target)
            results.append(f"[OK] Restored {target.name}")
        else:
            results.append(f"[WARN] Template missing: {template.name}")

    return results


def restore_workspace_map() -> str:
    """Restore workspace-map.md from template."""
    template = TEMPLATES_DIR / "workspace-map.md"
    target = NEXUS_ROOT / "04-workspace" / "workspace-map.md"

    if template.exists():
        shutil.copy2(template, target)
        return "[OK] Restored workspace-map.md"
    else:
        return "[WARN] Template missing: workspace-map.md"


def clear_builds() -> list[str]:
    """Remove all builds from active/ and complete/."""
    results = []

    for name in ["active", "complete"]:
        folder = NEXUS_ROOT / "02-builds" / name
        if folder.exists():
            items = list(folder.iterdir())
            count = 0
            for item in items:
                if item.is_dir():
                    shutil.rmtree(item)
                    count += 1
                elif item.is_file() and item.name != ".gitkeep":
                    item.unlink()
                    count += 1
            results.append(f"[OK] Cleared 02-builds/{name}/ ({count} builds)")
        else:
            results.append(f"[SKIP] 02-builds/{name}/ not found")

    return results


def remove_roadmap() -> str:
    """Delete roadmap.yaml if exists."""
    path = NEXUS_ROOT / "01-memory" / "roadmap.yaml"
    if path.exists():
        path.unlink()
        return "[OK] Removed roadmap.yaml"
    return "[SKIP] roadmap.yaml not found"


def clear_session_reports() -> str:
    """Remove all files in session-reports/."""
    folder = NEXUS_ROOT / "01-memory" / "session-reports"
    if folder.exists():
        count = 0
        for item in folder.iterdir():
            if item.is_file() and item.name != ".gitkeep":
                item.unlink()
                count += 1
            elif item.is_dir():
                shutil.rmtree(item)
                count += 1
        return f"[OK] Cleared session-reports/ ({count} files)"
    return "[SKIP] session-reports/ not found"


def clear_input_folder() -> str:
    """Remove input/ folder entirely."""
    folder = NEXUS_ROOT / "01-memory" / "input"
    if folder.exists():
        shutil.rmtree(folder)
        return "[OK] Removed input/ folder"
    return "[SKIP] input/ not found"


def clear_setup_marker() -> str:
    """Remove .claude/.setup_complete marker."""
    path = NEXUS_ROOT / ".claude" / ".setup_complete"
    if path.exists():
        path.unlink()
        return "[OK] Removed .claude/.setup_complete"
    return "[SKIP] .setup_complete not found"


def clear_skills() -> str:
    """Remove user skills from 03-skills/ (preserves README.md)."""
    folder = SKILLS_FOLDER
    if folder.exists():
        count = 0
        for item in folder.iterdir():
            if item.name in ["README.md", ".gitkeep", "__pycache__"]:
                continue
            if item.is_dir():
                shutil.rmtree(item)
                count += 1
            elif item.is_file():
                item.unlink()
                count += 1
        return f"[OK] Cleared 03-skills/ ({count} skills)"
    return "[SKIP] 03-skills/ not found"


def execute_reset(include_skills: bool = False, keep_builds: bool = False) -> list[str]:
    """Execute all reset operations in correct order."""
    results = []

    # 1. Delete builds (unless --keep-builds)
    if keep_builds:
        results.append("[SKIP] Keeping builds (--keep-builds)")
    else:
        results.extend(clear_builds())

    # 2. Delete roadmap (unless keeping builds)
    if keep_builds:
        results.append("[SKIP] Keeping roadmap.yaml (--keep-builds)")
    else:
        results.append(remove_roadmap())

    # 3. Clear session reports
    results.append(clear_session_reports())

    # 4. Delete input folder
    results.append(clear_input_folder())

    # 5. Delete setup marker
    results.append(clear_setup_marker())

    # 6. Clear skills if requested
    if include_skills:
        results.append(clear_skills())

    # 7. Restore memory files from templates
    results.extend(restore_memory_files())

    # 8. Restore workspace-map
    results.append(restore_workspace_map())

    return results


# ============================================================================
# CLI Interface
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Reset Nexus instance to initial state"
    )
    parser.add_argument(
        "command",
        choices=["scan", "execute"],
        help="scan: show what will be reset; execute: perform reset"
    )
    parser.add_argument(
        "--include-skills",
        action="store_true",
        help="Also clear user skills in 03-skills/"
    )
    parser.add_argument(
        "--keep-builds",
        action="store_true",
        help="Preserve builds and roadmap (only reset memory/config)"
    )

    args = parser.parse_args()

    if args.command == "scan":
        manifest = scan_instance()
        print(json.dumps(manifest, indent=2))

    elif args.command == "execute":
        print("Resetting instance...")
        results = execute_reset(
            include_skills=args.include_skills,
            keep_builds=args.keep_builds
        )
        for result in results:
            print(f"  {result}")
        print("\nReset complete!")


if __name__ == "__main__":
    main()
