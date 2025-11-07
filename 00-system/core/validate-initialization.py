#!/usr/bin/env python3
"""
Validate Nexus-v3 initialization requirements.

This script checks that all required files and folders exist for proper
Nexus-v3 operation. Run this before using the system to catch issues early.

Usage:
    python 00-system/core/validate-initialization.py

Returns:
    0 if all critical checks pass
    1 if any critical checks fail
"""

import os
import sys
from pathlib import Path

# Use ASCII-safe symbols for Windows compatibility
CHECK = "[OK]"
CROSS = "[X]"
WARN = "[!]"


def check_core_files():
    """Verify core system files exist."""
    print("Checking: Core Files")

    required_files = [
        "CLAUDE.md",
        "00-system/core/orchestrator.md",
        "00-system/core/nexus-loader.py",
        "00-system/system-map.md"
    ]

    missing = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing.append(file_path)
        else:
            print(f"  [OK] {file_path}")

    if missing:
        print("\n[X] Missing core files:")
        for f in missing:
            print(f"   - {f}")
        return False

    print("[OK] All core files present")
    return True


def check_folder_structure():
    """Verify required folders exist."""
    print("\nChecking: Folder Structure")

    required_folders = [
        "00-system",
        "00-system/core",
        "00-system/skills",
        "01-memory",
        "02-projects",
        "03-skills",
        "04-workspace"
    ]

    missing = []
    for folder in required_folders:
        if not os.path.isdir(folder):
            missing.append(folder)
        else:
            print(f"  [OK] {folder}/")

    if missing:
        print("\n[X] Missing folders:")
        for f in missing:
            print(f"   - {f}/")
        return False

    print("[OK] All required folders present")
    return True


def check_memory_files():
    """Verify memory system files (non-critical for templates)."""
    print("\nChecking: Memory Files")

    memory_files = [
        "01-memory/memory-map.md",
        "01-memory/goals.md",
        "02-projects/project-map.md",
        "04-workspace/workspace-map.md"
    ]

    missing = []
    present = []

    for file_path in memory_files:
        if not os.path.exists(file_path):
            missing.append(file_path)
        else:
            present.append(file_path)
            print(f"  [OK] {file_path}")

    if missing:
        print("\n[!]  Memory files missing (expected for new instance):")
        for f in missing:
            print(f"   - {f}")
        print("\nNote: These files are created during initialization.")
        print("This is normal for a template or new instance.")

    if present:
        print("[OK] Some memory files present (system may be initialized)")

    # Always return True - missing memory files are OK for templates
    return True


def check_loader_script():
    """Verify nexus-loader.py is valid Python."""
    print("\nChecking: Loader Script")

    loader = "00-system/core/nexus-loader.py"

    if not os.path.exists(loader):
        print(f"[X] Loader script missing: {loader}")
        return False

    # Check if it's a valid Python file
    try:
        with open(loader, 'r', encoding='utf-8') as f:
            content = f.read()

        # Basic validation - check for Python syntax
        if 'def ' not in content and 'class ' not in content:
            print(f"[!]  Warning: {loader} doesn't appear to contain Python code")
            return False

        print(f"  [OK] {loader} exists")
        print(f"  [OK] Contains Python code")
        print("[OK] Loader script valid")
        return True

    except Exception as e:
        print(f"[X] Error reading loader script: {e}")
        return False


def check_path_references():
    """Verify CLAUDE.md references correct paths."""
    print("\nChecking: Path References")

    claude_md = "CLAUDE.md"

    if not os.path.exists(claude_md):
        print(f"[X] {claude_md} not found")
        return False

    try:
        with open(claude_md, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check for correct orchestrator path
        correct_path = "00-system/core/orchestrator.md"
        wrong_paths = [
            "00-System/Agents/orchestrator.md",
            "00-System/core/orchestrator.md",
            "System/orchestrator.md"
        ]

        issues = []

        if correct_path in content:
            print(f"  [OK] CLAUDE.md references correct path: {correct_path}")
        else:
            issues.append(f"CLAUDE.md doesn't reference {correct_path}")

        for wrong_path in wrong_paths:
            if wrong_path in content:
                issues.append(f"CLAUDE.md references incorrect path: {wrong_path}")

        if issues:
            print("\n[X] Path reference issues:")
            for issue in issues:
                print(f"   - {issue}")
            return False

        print("[OK] Path references correct")
        return True

    except Exception as e:
        print(f"[X] Error reading {claude_md}: {e}")
        return False


def check_system_skills():
    """Verify system skills exist."""
    print("\nChecking: System Skills")

    system_skills = [
        "00-system/skills/create-project",
        "00-system/skills/create-skill",
        "00-system/skills/close-session",
        "00-system/skills/validate-system",
        "00-system/skills/add-integration"
    ]

    missing = []
    present = []

    for skill_path in system_skills:
        skill_file = os.path.join(skill_path, "SKILL.md")
        if os.path.exists(skill_file):
            present.append(skill_path)
            skill_name = os.path.basename(skill_path)
            print(f"  [OK] {skill_name}")
        else:
            missing.append(skill_path)

    if missing:
        print("\n[!]  Missing system skills:")
        for s in missing:
            skill_name = os.path.basename(s)
            print(f"   - {skill_name}")
        print("\nNote: Some skills may be optional.")

    if len(present) >= 3:  # At least 3 core skills
        print("[OK] Core system skills present")
        return True
    else:
        print("[X] Too few system skills found")
        return False


def main():
    """Run all validation checks."""
    print("Validating Nexus-v3 Initialization...")
    print("=" * 60)
    print()

    checks = [
        ("Core Files", check_core_files),
        ("Folder Structure", check_folder_structure),
        ("System Skills", check_system_skills),
        ("Path References", check_path_references),
        ("Loader Script", check_loader_script),
        ("Memory Files", check_memory_files)
    ]

    results = []
    critical_checks = ["Core Files", "Folder Structure", "Path References", "Loader Script"]

    for name, check_fn in checks:
        try:
            result = check_fn()
            results.append((name, result))
        except Exception as e:
            print(f"\n[X] Error in {name} check: {e}")
            results.append((name, False))
        print()

    # Summary
    print("=" * 60)
    print("VALIDATION SUMMARY")
    print("=" * 60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    critical_passed = sum(1 for name, result in results if result and name in critical_checks)
    critical_total = len(critical_checks)

    for name, result in results:
        status = "[OK] PASS" if result else "[X] FAIL"
        critical = " (CRITICAL)" if name in critical_checks else ""
        print(f"{status:12} {name}{critical}")

    print()
    print(f"Critical Checks: {critical_passed}/{critical_total} passed")
    print(f"Total Checks:    {passed}/{total} passed")
    print()

    # Determine exit status
    if critical_passed == critical_total:
        print("[OK] All critical validation checks passed!")
        print("System ready for initialization.")
        print()
        print("Next steps:")
        print("  1. Run: python 00-system/core/nexus-loader.py --startup")
        print("  2. Follow orchestrator initialization sequence")
        return 0
    else:
        print("[X] Some critical checks failed.")
        print("Please fix issues before initializing the system.")
        print()
        print("Common fixes:")
        print("  - Ensure you're running from project root directory")
        print("  - Check that all files were copied correctly")
        print("  - Verify CLAUDE.md has correct path references")
        return 1


if __name__ == "__main__":
    sys.exit(main())
