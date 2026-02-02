#!/usr/bin/env python3
"""
Skill Packager - Creates a distributable .skill file of a skill folder

Usage:
    python utils/package_skill.py <path/to/skill-folder> [output-directory]

Example:
    python utils/package_skill.py skills/public/my-skill
    python utils/package_skill.py skills/public/my-skill ./dist
"""

import sys
import zipfile
from pathlib import Path
from quick_validate import validate_skill

# Configure UTF-8 output for cross-platform compatibility
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass  # Python < 3.7


def package_skill(skill_path, output_dir=None):
    """
    Package a skill folder into a .skill file.

    Args:
        skill_path: Path to the skill folder
        output_dir: Optional output directory for the .skill file (defaults to current directory)

    Returns:
        Path to the created .skill file, or None if error
    """
    skill_path = Path(skill_path).resolve()

    # Validate skill folder exists
    if not skill_path.exists():
        print(f"[ERROR] Skill folder not found: {skill_path}")
        return None

    if not skill_path.is_dir():
        print(f"[ERROR] Path is not a directory: {skill_path}")
        return None

    # Validate SKILL.md exists
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        print(f"[ERROR] SKILL.md not found in {skill_path}")
        return None

    # Run validation before packaging
    print("[CHECK] Validating skill...")
    valid, message = validate_skill(skill_path)
    if not valid:
        print(f"[ERROR] Validation failed: {message}")
        print("   Please fix the validation errors before packaging.")
        return None
    print(f"[OK] {message}\n")

    # Determine output location
    skill_name = skill_path.name
    if output_dir:
        output_path = Path(output_dir).resolve()
        output_path.mkdir(parents=True, exist_ok=True)
    else:
        output_path = Path.cwd()

    skill_filename = output_path / f"{skill_name}.skill"

    # Create the .skill file (zip format)
    try:
        with zipfile.ZipFile(skill_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Walk through the skill directory
            for file_path in skill_path.rglob('*'):
                if file_path.is_file():
                    # Calculate the relative path within the zip
                    arcname = file_path.relative_to(skill_path.parent)
                    zipf.write(file_path, arcname)
                    print(f"  Added: {arcname}")

        print(f"\n[OK] Successfully packaged skill to: {skill_filename}")

        # Check Notion export readiness
        try:
            from validate_for_notion import validate_for_notion
            print("\n[CHECK] Checking Notion export readiness...")
            is_ready, warnings, suggestions = validate_for_notion(skill_path)

            if warnings:
                print("\n[!]  Notion Export Warnings:")
                for w in warnings:
                    print(f"  {w}")

            if suggestions:
                print("")
                for s in suggestions:
                    print(f"  {s}")

            print("\n" + "="*60)
            print("[UPLOAD] SHARE WITH TEAM")
            print("="*60)
            print("\nWould you like to export this skill to Notion?")
            print("  -> Makes skill discoverable by your team")
            print("  -> Enables collaborative improvement")
            print("  -> Recommended for production-ready skills")
            print("\nTo export, say: 'export this skill to Notion'")
            print("="*60)

        except ImportError:
            # validate_for_notion not available, skip check
            pass

        return skill_filename

    except Exception as e:
        print(f"[ERROR] Error creating .skill file: {e}")
        return None


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description='Package a skill folder into a distributable .skill file',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  package_skill.py 03-skills/my-skill              # Package to current directory
  package_skill.py 03-skills/my-skill ./dist       # Package to ./dist directory

The .skill file is a zip archive containing the entire skill folder.
Validation is run automatically before packaging.
'''
    )
    parser.add_argument('skill_path', help='Path to the skill folder')
    parser.add_argument('output_dir', nargs='?', default=None,
                        help='Output directory for .skill file (default: current directory)')

    args = parser.parse_args()

    print(f"[PACK] Packaging skill: {args.skill_path}")
    if args.output_dir:
        print(f"   Output directory: {args.output_dir}")
    print()

    result = package_skill(args.skill_path, args.output_dir)

    if result:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()