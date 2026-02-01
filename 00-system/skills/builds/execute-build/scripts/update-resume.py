#!/usr/bin/env python3
"""
Update resume-context.md YAML frontmatter fields.

This script is called by execute-build skill to automatically update
resume state at task/section completion checkpoints.

Usage:
    update_resume_context.py --build BUILD_ID --field FIELD_NAME --value VALUE
    update_resume_context.py --build BUILD_ID --task 5 --completed 25
    update_resume_context.py --build BUILD_ID --section 3

Examples:
    # Update current task number
    update_resume_context.py --build 24-build-skills --task 15

    # Update completion counters
    update_resume_context.py --build 24-build-skills --task 16 --completed 16

    # Update section (also sets current_task to 1)
    update_resume_context.py --build 24-build-skills --section 3

    # Update phase
    update_resume_context.py --build 24-build-skills --phase execution

    # Custom field update
    update_resume_context.py --build 24-build-skills --field next_action --value "test-build"
"""

import sys
import argparse
from pathlib import Path
from datetime import datetime, timezone
import shutil
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(message)s'
)

def parse_yaml_frontmatter(content):
    """Parse YAML frontmatter from markdown content (zero-dependency parser)."""

    if '---' not in content:
        logging.error("No YAML frontmatter delimiter found")
        return None, None

    parts = content.split('---', 2)
    if len(parts) < 3:
        logging.error("Invalid YAML frontmatter structure (need 2 --- delimiters)")
        return None, None

    yaml_content = parts[1].strip()
    body_content = parts[2]

    # Parse YAML manually
    metadata = {}
    current_key = None
    current_list = None

    for line in yaml_content.split('\n'):
        line_stripped = line.strip()

        # Skip comments and empty lines
        if not line_stripped or line_stripped.startswith('#'):
            continue

        # Check if this is a list item
        if line_stripped.startswith('-') and current_list is not None:
            # List item for current key
            value = line_stripped[1:].strip().strip('"').strip("'")
            current_list.append(value)
        elif ':' in line_stripped:
            # Key-value pair
            if current_list is not None:
                # Finish previous list
                metadata[current_key] = current_list
                current_list = None
                current_key = None

            key, value = line_stripped.split(':', 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")

            if not value:
                # This might be a list or multi-line value
                current_key = key
                current_list = []
            else:
                metadata[key] = value

    # Finish any pending list
    if current_list is not None:
        metadata[current_key] = current_list

    return metadata, body_content

def format_yaml_value(value):
    """Format a Python value for YAML output."""
    if isinstance(value, list):
        # Multi-line list format
        result = "\n"
        for item in value:
            result += f'  - "{item}"\n'
        return result.rstrip('\n')
    elif isinstance(value, (int, float)):
        return str(value)
    elif isinstance(value, str):
        # Quote strings if they contain special characters
        if any(c in value for c in [':', '#', '\n', '"']):
            return f'"{value}"'
        return value
    else:
        return str(value)

def write_yaml_frontmatter(metadata, body_content):
    """Write YAML frontmatter + body back to markdown format.

    CRITICAL: This function must preserve ALL fields from the original file.
    The order list defines display order; any fields not in order are appended.
    """

    lines = ["---"]

    # Write metadata in specific order (preserve structure)
    # COMPLETE LIST - includes ALL resume-context.md fields to prevent data loss
    order = [
        # Session tracking
        'session_id',
        'session_ids',
        'resume_schema_version',
        'last_updated',
        '# BUILD',
        'build_id',
        'build_name',
        'build_type',
        'current_phase',
        '# LOADING - Updated dynamically',
        'next_action',
        'files_to_load',
        '# DISCOVERY STATE',
        'rediscovery_round',
        'discovery_complete',
        '# PROGRESS',
        'current_section',
        'current_task',
        'total_tasks',
        'tasks_completed'
    ]

    written_keys = set()

    for key in order:
        if key.startswith('#'):
            # Comment line
            lines.append('')
            lines.append(key)
        elif key in metadata:
            value = metadata[key]
            formatted_value = format_yaml_value(value)

            if '\n' in formatted_value:
                # Multi-line value (lists)
                lines.append(f"{key}:{formatted_value}")
            else:
                lines.append(f"{key}: {formatted_value}")
            written_keys.add(key)

    # CRITICAL: Write any remaining fields not in the order list (future-proofing)
    for key, value in metadata.items():
        if key not in written_keys:
            formatted_value = format_yaml_value(value)
            if '\n' in formatted_value:
                lines.append(f"{key}:{formatted_value}")
            else:
                lines.append(f"{key}: {formatted_value}")
            logging.warning(f"Field '{key}' not in standard order - appended at end")

    lines.append("---")

    # Add body
    content = '\n'.join(lines) + body_content

    return content

def update_resume_context(build_path, updates):
    """
    Update resume-context.md YAML frontmatter.

    Args:
        build_path: Path to build directory
        updates: Dict of fields to update

    Returns:
        bool: True if successful, False otherwise
    """

    resume_file = build_path / "01-planning" / "resume-context.md"

    if not resume_file.exists():
        logging.error(f"Resume file not found: {resume_file}")
        return False

    # Create backup
    backup_file = resume_file.with_suffix('.md.backup')
    try:
        shutil.copy2(resume_file, backup_file)
        logging.info(f"Created backup: {backup_file}")
    except Exception as e:
        logging.error(f"Failed to create backup: {e}")
        return False

    # Read current content
    try:
        content = resume_file.read_text(encoding='utf-8')
    except Exception as e:
        logging.error(f"Failed to read resume file: {e}")
        return False

    # Parse YAML
    metadata, body = parse_yaml_frontmatter(content)
    if metadata is None:
        logging.error("Failed to parse YAML frontmatter")
        return False

    # Apply updates
    for key, value in updates.items():
        old_value = metadata.get(key)
        metadata[key] = value
        logging.info(f"Updated {key}: {old_value} -> {value}")

    # Always update timestamp
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    metadata["last_updated"] = timestamp
    logging.info(f"Updated last_updated: {timestamp}")

    # Write back
    try:
        new_content = write_yaml_frontmatter(metadata, body)
        resume_file.write_text(new_content, encoding='utf-8')
        logging.info(f"Successfully updated {resume_file}")
        return True
    except Exception as e:
        logging.error(f"Failed to write resume file: {e}")
        # Restore from backup
        try:
            shutil.copy2(backup_file, resume_file)
            logging.info("Restored from backup after write failure")
        except Exception as restore_error:
            logging.error(f"CRITICAL: Failed to restore backup: {restore_error}")
        return False

def main():
    parser = argparse.ArgumentParser(
        description='Update resume-context.md YAML frontmatter fields',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    parser.add_argument('--build', required=True,
                       help='Build ID (e.g., 24-build-skills-research)')

    parser.add_argument('--task', type=int,
                       help='Set current_task number')

    parser.add_argument('--section', type=int,
                       help='Set current_section number (also resets current_task to 1)')

    parser.add_argument('--phase', type=str,
                       help='Set current_phase (research|planning|execution|testing|review)')

    parser.add_argument('--completed', type=int,
                       help='Set tasks_completed counter')

    parser.add_argument('--field', type=str,
                       help='Custom field name to update')

    parser.add_argument('--value', type=str,
                       help='Custom field value (use with --field)')

    args = parser.parse_args()

    # Find build directory (check from current working directory first)
    cwd = Path.cwd()

    # Try to find 02-builds from CWD
    build_path = None

    # Check if CWD has 02-builds
    if (cwd / "02-builds" / args.build).exists():
        build_path = cwd / "02-builds" / args.build
    # Check if CWD parent has 02-builds
    elif (cwd.parent / "02-builds" / args.build).exists():
        build_path = cwd.parent / "02-builds" / args.build
    # Check if CWD grandparent has 02-builds
    elif (cwd.parent.parent / "02-builds" / args.build).exists():
        build_path = cwd.parent.parent / "02-builds" / args.build
    # Fallback: calculate from script location
    else:
        project_root = Path(__file__).resolve().parents[4]
        build_path = project_root / "02-builds" / args.build

    if not build_path or not build_path.exists():
        logging.error(f"Build directory not found: {build_path}")
        logging.error(f"CWD: {cwd}")
        logging.error(f"Looked in: {cwd / '02-builds' / args.build}")
        logging.error(f"Also tried: {cwd.parent / '02-builds' / args.build}")
        sys.exit(1)

    # Build updates dict
    updates = {}

    if args.section is not None:
        updates['current_section'] = args.section
        updates['current_task'] = 1  # Reset task to 1 when changing sections

    if args.task is not None:
        updates['current_task'] = args.task

    if args.phase:
        valid_phases = ['research', 'planning', 'execution', 'testing', 'review', 'complete', 'ready-for-implementation']
        if args.phase not in valid_phases:
            logging.error(f"Invalid phase: {args.phase}. Must be one of: {valid_phases}")
            sys.exit(1)
        updates['current_phase'] = args.phase

    if args.completed is not None:
        updates['tasks_completed'] = args.completed

    if args.field and args.value:
        updates[args.field] = args.value
    elif args.field or args.value:
        logging.error("Both --field and --value must be provided together")
        sys.exit(1)

    if not updates:
        logging.error("No updates specified. Use --task, --section, --phase, --completed, or --field/--value")
        sys.exit(1)

    # Perform update
    success = update_resume_context(build_path, updates)

    if success:
        logging.info("Resume update successful!")
        sys.exit(0)
    else:
        logging.error("Resume update failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
