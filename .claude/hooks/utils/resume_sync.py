"""
Resume Context Sync Utility

Provides functions to synchronize resume-context.md with actual build state.
Used by PreCompact and PostToolUse hooks to keep progress accurate.

Build 05: Resume Context Improvement
"""

from __future__ import annotations

import re
import logging
from pathlib import Path
from typing import Dict, Any, Optional, Tuple
from datetime import datetime, timezone

# PyYAML is optional - graceful degradation
try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False
    yaml = None


def count_checkboxes(steps_path: Path) -> Tuple[int, int, int]:
    """
    Count checkboxes in a steps.md file.

    Args:
        steps_path: Path to 04-steps.md

    Returns:
        Tuple of (total, completed, uncompleted)
    """
    if not steps_path.exists():
        return (0, 0, 0)

    try:
        content = steps_path.read_text(encoding="utf-8")

        # Match checkbox patterns: - [ ] or - [x] or - [X]
        checked = len(re.findall(r"^\s*-\s*\[x\]", content, re.MULTILINE | re.IGNORECASE))
        unchecked = len(re.findall(r"^\s*-\s*\[\s\]", content, re.MULTILINE))

        total = checked + unchecked
        return (total, checked, unchecked)
    except Exception as e:
        logging.warning(f"count_checkboxes failed: {e}")
        return (0, 0, 0)


def find_current_section(steps_path: Path) -> int:
    """
    Find the first phase with unchecked tasks.

    Templates use "## Phase N:" format (enforced by init_build.py).

    Args:
        steps_path: Path to 04-steps.md

    Returns:
        Phase number (1-indexed), or 1 if no phases found
    """
    if not steps_path.exists():
        return 1

    try:
        content = steps_path.read_text(encoding="utf-8")

        # Find all phase headers: ## Phase N: (templates use this format)
        section_pattern = re.compile(
            r'^##\s*Phase\s+(\d+)[:\s]',
            re.MULTILINE | re.IGNORECASE
        )

        # Split content by sections
        sections = section_pattern.split(content)

        # sections alternates: [before_first_section, section_num, section_content, ...]
        if len(sections) < 3:
            # No numbered sections found, check for any unchecked
            if re.search(r'^\s*-\s*\[\s\]', content, re.MULTILINE):
                return 1
            return 1

        # Iterate through section content (index 2, 4, 6, ...)
        for i in range(1, len(sections), 2):
            section_num = int(sections[i])
            section_content = sections[i + 1] if i + 1 < len(sections) else ""

            # Check if this section has unchecked tasks
            if re.search(r'^\s*-\s*\[\s\]', section_content, re.MULTILINE):
                return section_num

        # All sections complete - return last section number
        return int(sections[-2]) if len(sections) >= 2 else 1

    except Exception as e:
        logging.warning(f"find_current_section failed: {e}")
        return 1


def find_current_task(steps_path: Path) -> int:
    """
    Find the task number of the first unchecked task.

    Counts all checkboxes sequentially and returns the position
    of the first unchecked one.

    Args:
        steps_path: Path to 04-steps.md

    Returns:
        Task number (1-indexed), or total+1 if all complete
    """
    if not steps_path.exists():
        return 1

    try:
        content = steps_path.read_text(encoding="utf-8")

        # Find all checkboxes in order
        checkbox_pattern = re.compile(r'^\s*-\s*\[([x\s])\]', re.MULTILINE | re.IGNORECASE)
        matches = checkbox_pattern.finditer(content)

        task_num = 0
        for match in matches:
            task_num += 1
            if match.group(1).strip() == '':  # Unchecked
                return task_num

        # All complete
        return task_num + 1 if task_num > 0 else 1

    except Exception as e:
        logging.warning(f"find_current_task failed: {e}")
        return 1


def detect_phase(steps_path: Path) -> str:
    """
    Detect build phase based on task completion.

    Phase logic:
    - "complete": ALL tasks done (100%)
    - "execution": Phase 1 complete, work in progress
    - "planning": Phase 1 incomplete

    Templates use "## Phase N:" format (enforced by init_build.py).

    Args:
        steps_path: Path to 04-steps.md

    Returns:
        "planning", "execution", or "complete"
    """
    if not steps_path.exists():
        return "planning"

    try:
        content = steps_path.read_text(encoding="utf-8")

        # First: Check if ALL tasks are complete (100%)
        total_all, completed_all, _ = count_checkboxes(steps_path)
        if total_all > 0 and completed_all == total_all:
            return "complete"

        # Find Phase 1 section (templates use "## Phase 1:" format)
        phase1_pattern = re.compile(
            r'^##\s*Phase 1[:\s][^\n]*\n(.*?)(?=^##\s*Phase [2-9]|\Z)',
            re.MULTILINE | re.DOTALL
        )
        match = phase1_pattern.search(content)

        if not match:
            # No explicit Phase 1 - fallback: any unchecked = planning
            unchecked = re.findall(r'^\s*-\s*\[\s\]', content, re.MULTILINE)
            return "planning" if unchecked else "execution"

        phase1_content = match.group(1)

        # Count checkboxes in Phase 1
        completed = len(re.findall(r'^\s*-\s*\[x\]', phase1_content, re.MULTILINE | re.IGNORECASE))
        total = len(re.findall(r'^\s*-\s*\[[x\s]\]', phase1_content, re.MULTILINE | re.IGNORECASE))

        if total == 0:
            return "planning"

        # All Phase 1 tasks complete = execution
        return "execution" if completed == total else "planning"

    except Exception as e:
        logging.warning(f"detect_phase failed: {e}")
        return "planning"


def extract_yaml_frontmatter(file_path: Path) -> Dict[str, Any]:
    """
    Extract YAML frontmatter from markdown file.

    Handles both simple key: value and list formats.

    Args:
        file_path: Path to markdown file

    Returns:
        Dictionary of YAML fields, empty dict if none
    """
    if not file_path.exists():
        return {}

    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception as e:
        logging.warning(f"Could not read {file_path}: {e}")
        return {}

    # Match YAML frontmatter block
    match = re.match(r'^---\s*\n(.*?)\n---', content, re.MULTILINE | re.DOTALL)
    if not match:
        return {}

    yaml_block = match.group(1)

    # Try PyYAML first
    if HAS_YAML:
        try:
            metadata = yaml.safe_load(yaml_block)
            return metadata if isinstance(metadata, dict) else {}
        except yaml.YAMLError as e:
            logging.warning(f"YAML parse error: {e}")
            # Fall through to manual parsing

    # Manual parsing fallback
    metadata = {}
    current_list_key = None
    current_list = []

    for line in yaml_block.split('\n'):
        stripped = line.strip()

        # Skip empty lines and comments
        if not stripped or stripped.startswith('#'):
            # Save pending list
            if current_list_key and current_list:
                metadata[current_list_key] = current_list
                current_list_key = None
                current_list = []
            continue

        # List item
        if stripped.startswith('- '):
            item = stripped[2:].strip().strip('"').strip("'")
            current_list.append(item)
            continue

        # Key: value pair
        if ':' in stripped:
            # Save pending list first
            if current_list_key and current_list:
                metadata[current_list_key] = current_list
                current_list = []

            key, _, value = stripped.partition(':')
            key = key.strip()
            value = value.strip()

            if value == '' or value == '[]':
                # Start of list
                current_list_key = key
                current_list = []
            elif value.startswith('['):
                # Inline list
                items = re.findall(r'"([^"]+)"', value)
                metadata[key] = items
                current_list_key = None
            else:
                # Simple value
                value = value.strip('"').strip("'")
                # Type conversion
                if value.lower() == 'true':
                    value = True
                elif value.lower() == 'false':
                    value = False
                elif value.isdigit():
                    value = int(value)
                metadata[key] = value
                current_list_key = None

    # Don't forget trailing list
    if current_list_key and current_list:
        metadata[current_list_key] = current_list

    return metadata


def write_yaml_frontmatter(file_path: Path, metadata: Dict[str, Any]) -> bool:
    """
    Write YAML frontmatter to file, preserving markdown content.

    IMPORTANT: This preserves ALL existing fields and only updates
    the specified ones. Uses a predefined order for consistency.

    Args:
        file_path: Path to markdown file
        metadata: Dictionary of fields to update (merged with existing)

    Returns:
        True on success, False on failure
    """
    if not file_path.exists():
        logging.warning(f"File does not exist: {file_path}")
        return False

    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception as e:
        logging.warning(f"Could not read {file_path}: {e}")
        return False

    # Extract existing frontmatter
    existing = extract_yaml_frontmatter(file_path)

    # Merge: existing values + new values (new takes precedence)
    merged = {**existing, **metadata}

    # Define field order (COMPLETE list to prevent field loss)
    # Based on resume-context.md schema
    field_order = [
        # Session tracking
        'session_id',
        'session_ids',
        'resume_schema_version',
        'last_updated',
        # Build identification
        'build_id',
        'build_name',
        'build_type',
        'current_phase',
        # Loading instructions
        'next_action',
        'files_to_load',
        # Discovery state
        'rediscovery_round',
        'discovery_complete',
        # Progress tracking
        'current_section',
        'current_task',
        'total_tasks',
        'tasks_completed',
    ]

    # Build YAML output
    yaml_lines = ['---']
    written_keys = set()

    # Write in defined order first
    for key in field_order:
        if key in merged:
            yaml_lines.append(_format_yaml_field(key, merged[key]))
            written_keys.add(key)

    # Write any remaining fields not in order (future-proofing)
    for key, value in merged.items():
        if key not in written_keys:
            yaml_lines.append(_format_yaml_field(key, value))

    yaml_lines.append('---')

    # Find where markdown content starts (after frontmatter)
    match = re.match(r'^---\s*\n.*?\n---\s*\n?', content, re.DOTALL)
    if match:
        markdown_content = content[match.end():]
    else:
        markdown_content = content

    # Combine and write
    new_content = '\n'.join(yaml_lines) + '\n' + markdown_content

    try:
        file_path.write_text(new_content, encoding="utf-8")
        return True
    except Exception as e:
        logging.warning(f"Could not write {file_path}: {e}")
        return False


def _format_yaml_field(key: str, value: Any) -> str:
    """Format a single YAML field for output."""
    # Add section comments for readability
    section_comments = {
        'build_id': '\n# BUILD',
        'next_action': '\n# LOADING - Updated dynamically',
        'rediscovery_round': '\n# DISCOVERY STATE',
        'current_section': '\n# PROGRESS',
    }

    prefix = section_comments.get(key, '')

    if isinstance(value, list):
        if not value:
            return f"{prefix}\n{key}:" if prefix else f"{key}:"
        # Multi-line list format
        lines = [f"{prefix}" if prefix else ""]
        lines.append(f"{key}:")
        for item in value:
            lines.append(f'  - "{item}"')
        return '\n'.join(lines).strip()
    elif isinstance(value, bool):
        return f"{prefix}\n{key}: {str(value).lower()}" if prefix else f"{key}: {str(value).lower()}"
    elif isinstance(value, int):
        return f"{prefix}\n{key}: {value}" if prefix else f"{key}: {value}"
    else:
        # String value - quote if contains special chars
        str_value = str(value) if value is not None else ""
        if ':' in str_value or '\n' in str_value:
            return f'{prefix}\n{key}: "{str_value}"' if prefix else f'{key}: "{str_value}"'
        return f"{prefix}\n{key}: \"{str_value}\"" if prefix else f"{key}: \"{str_value}\""


def sync_progress_fields(resume_path: Path, steps_path: Path) -> Dict[str, Any]:
    """
    Sync progress fields from steps.md to resume-context.md.

    Updates:
    - total_tasks: count of all checkboxes
    - tasks_completed: count of checked boxes
    - current_section: first section with unchecked task
    - current_task: position of first unchecked task
    - current_phase: "planning", "execution", or "complete"
    - next_action: "plan-build" or "execute-build"
    - last_updated: current timestamp

    Args:
        resume_path: Path to resume-context.md
        steps_path: Path to 04-steps.md

    Returns:
        Dictionary of updated fields (for logging/verification)
    """
    # Calculate current values
    total, completed, _ = count_checkboxes(steps_path)
    current_section = find_current_section(steps_path)
    current_task = find_current_task(steps_path)
    phase = detect_phase(steps_path)

    # Get existing next_action to check for custom values
    existing = extract_yaml_frontmatter(resume_path)
    existing_action = existing.get('next_action', '')

    # Standard next_action values that we auto-manage
    STANDARD_ACTIONS = {'plan-build', 'execute-build', ''}

    # Only auto-set next_action if it's a standard value
    # This preserves custom values like "implement-phase-3"
    if existing_action in STANDARD_ACTIONS:
        if phase == "planning":
            next_action = "plan-build"
        else:  # "execution" or "complete"
            next_action = "execute-build"
    else:
        # Preserve custom next_action
        next_action = existing_action
        logging.info(f"Preserving custom next_action: {next_action}")

    # Build update dict
    updates = {
        'total_tasks': total,
        'tasks_completed': completed,
        'current_section': current_section,
        'current_task': current_task,
        'current_phase': phase,
        'next_action': next_action,
        'last_updated': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
    }

    # Write updates
    success = write_yaml_frontmatter(resume_path, updates)

    if success:
        logging.info(f"Synced progress: {completed}/{total} tasks, phase={phase}, section={current_section}")
    else:
        logging.warning("Failed to sync progress fields")

    return updates


def add_session_id(resume_path: Path, session_id: str) -> bool:
    """
    Add a session ID to the session_ids list if not already present.

    Also updates session_id (singular) for backward compatibility.

    Args:
        resume_path: Path to resume-context.md
        session_id: Session ID to add

    Returns:
        True if added/updated, False on error
    """
    if not session_id:
        return False

    existing = extract_yaml_frontmatter(resume_path)

    # Get existing session_ids list
    session_ids = existing.get('session_ids', [])
    if not isinstance(session_ids, list):
        session_ids = [session_ids] if session_ids else []

    # Add if not present
    if session_id not in session_ids:
        session_ids.append(session_id)

    # Update both fields
    updates = {
        'session_id': session_id,  # Singular for current session
        'session_ids': session_ids,  # List for history
    }

    return write_yaml_frontmatter(resume_path, updates)


# Convenience function for hooks
def get_resume_path(build_path: Path) -> Path:
    """Get the standard resume-context.md path for a build."""
    return build_path / "01-planning" / "resume-context.md"


def get_steps_path(build_path: Path) -> Path:
    """Get the standard 04-steps.md path for a build."""
    return build_path / "01-planning" / "04-steps.md"
