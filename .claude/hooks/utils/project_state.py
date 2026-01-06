"""
Project State Detection Utility

Extracts status, phase, and progress metadata from project files.
Based on analysis from project 28-handover-test-suite Phase 7.

This utility provides enhanced state detection using metadata patterns
identified in init_project.py generated files:
- overview.md YAML frontmatter (status, created date)
- resume-context.md YAML frontmatter (current_phase, next_action, progress)
- steps.md checkbox tracking (completion ratios, phase markers)
"""

import re
import logging
from pathlib import Path
from typing import Dict, Optional, Any
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ProjectState:
    """Complete project state snapshot."""
    project_id: str
    name: str
    status: str  # PLANNING | IN_PROGRESS | COMPLETE
    current_phase: str  # planning | execution
    next_action: str  # plan-project | execute-project
    current_section: int
    tasks_completed: int
    tasks_total: int
    progress_percent: float
    last_updated: Optional[str] = None
    created: Optional[str] = None
    session_ids: list[str] = None

    def __post_init__(self):
        if self.session_ids is None:
            self.session_ids = []


def extract_yaml_frontmatter(file_path: Path) -> Dict[str, Any]:
    """
    Extract YAML frontmatter from markdown file.

    Args:
        file_path: Path to markdown file with YAML frontmatter

    Returns:
        Dictionary of YAML fields, or empty dict if no frontmatter
    """
    if not file_path.exists():
        return {}

    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception as e:
        logging.warning(f"Could not read {file_path}: {e}")
        return {}

    # Match YAML frontmatter block
    yaml_pattern = re.compile(r'^---\s*\n(.*?)\n---', re.MULTILINE | re.DOTALL)
    match = yaml_pattern.match(content)

    if not match:
        return {}

    yaml_block = match.group(1)
    metadata = {}

    # Parse simple YAML fields (field: value)
    for line in yaml_block.split('\n'):
        line = line.strip()
        if not line or line.startswith('#'):
            continue

        # Handle list fields (session_ids, files_to_load)
        if line.startswith('- '):
            continue  # Skip list items for now

        # Simple field: value
        if ':' in line:
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")

            # Track if we're entering a list
            if value == '' or value.startswith('['):
                # Check if this is an inline list
                if value.startswith('['):
                    # Parse inline list: ["id1", "id2"]
                    list_match = re.findall(r'"([^"]+)"', value)
                    metadata[key] = list_match
                continue

            metadata[key] = value

    # Special handling for session_ids list (multiline YAML list)
    # Match session_ids: followed by list items (with flexible whitespace)
    session_ids_pattern = re.compile(
        r'session_ids:\s*$((?:\s*-\s*"[^"]+"\s*$)+)',
        re.MULTILINE
    )
    session_match = session_ids_pattern.search(yaml_block)
    if session_match:
        session_lines = session_match.group(1)
        session_ids = re.findall(r'"([^"]+)"', session_lines)
        metadata['session_ids'] = session_ids

    return metadata


def get_project_status_from_overview(project_path: Path) -> Optional[str]:
    """
    Extract status field from overview.md.

    Args:
        project_path: Path to project root (e.g., 02-projects/28-handover-test-suite)

    Returns:
        Status string (PLANNING | IN_PROGRESS | COMPLETE) or None
    """
    overview = project_path / "01-planning" / "01-overview.md"
    metadata = extract_yaml_frontmatter(overview)
    return metadata.get('status')


def get_project_metadata_from_resume(project_path: Path) -> Dict[str, Any]:
    """
    Extract rich metadata from resume-context.md.

    Args:
        project_path: Path to project root

    Returns:
        Dictionary with current_phase, next_action, current_section,
        tasks_completed, last_updated, session_ids
    """
    resume = project_path / "01-planning" / "resume-context.md"
    return extract_yaml_frontmatter(resume)


def count_tasks_in_steps(project_path: Path) -> tuple[int, int]:
    """
    Count total and completed tasks from steps.md checkbox tracking.

    Args:
        project_path: Path to project root

    Returns:
        Tuple of (completed_count, total_count)
    """
    steps_file = project_path / "01-planning" / "04-steps.md"

    if not steps_file.exists():
        return (0, 0)

    try:
        content = steps_file.read_text(encoding="utf-8")
    except Exception as e:
        logging.warning(f"Could not read steps.md: {e}")
        return (0, 0)

    # Count checkboxes
    completed = len(re.findall(r'^\s*- \[x\]', content, re.MULTILINE | re.IGNORECASE))
    total = len(re.findall(r'^\s*- \[[x ]\]', content, re.MULTILINE | re.IGNORECASE))

    return (completed, total)


def detect_project_state(project_path: Path) -> Optional[ProjectState]:
    """
    Detect complete project state from metadata files.

    Combines data from:
    - overview.md (status, name, created)
    - resume-context.md (phase, next_action, progress, session_ids)
    - steps.md (task counts, fallback for phase detection)

    Args:
        project_path: Path to project root directory

    Returns:
        ProjectState object with complete metadata, or None if project invalid
    """
    # Validate project structure
    planning_dir = project_path / "01-planning"
    if not planning_dir.exists():
        logging.warning(f"Invalid project structure: {project_path} (no 01-planning/)")
        return None

    # Extract project ID and name from folder
    folder_name = project_path.name
    parts = folder_name.split('-', 1)
    if len(parts) != 2:
        logging.warning(f"Invalid project folder name: {folder_name} (expected ID-name)")
        return None

    project_id = parts[0]
    name = parts[1].replace('-', ' ').title()

    # Get status from overview.md
    overview_metadata = extract_yaml_frontmatter(planning_dir / "01-overview.md")
    status = overview_metadata.get('status', 'IN_PROGRESS')
    created = overview_metadata.get('created')

    # Get rich metadata from resume-context.md
    resume_metadata = get_project_metadata_from_resume(project_path)
    current_phase = resume_metadata.get('current_phase', 'planning')
    next_action = resume_metadata.get('next_action', 'plan-project')
    current_section = int(resume_metadata.get('current_section', 1))
    last_updated = resume_metadata.get('last_updated')
    session_ids = resume_metadata.get('session_ids', [])

    # Also check legacy single session_id field
    if 'session_id' in resume_metadata and resume_metadata['session_id']:
        legacy_id = resume_metadata['session_id']
        if legacy_id not in session_ids:
            session_ids.append(legacy_id)

    # Get task counts from steps.md
    tasks_completed, tasks_total = count_tasks_in_steps(project_path)

    # Override with resume-context if available (more authoritative)
    if 'tasks_completed' in resume_metadata:
        tasks_completed = int(resume_metadata['tasks_completed'])
    if 'total_tasks' in resume_metadata:
        tasks_total = int(resume_metadata['total_tasks'])

    # Calculate progress
    progress_percent = 0.0
    if tasks_total > 0:
        progress_percent = round((tasks_completed / tasks_total) * 100, 1)

    return ProjectState(
        project_id=project_id,
        name=name,
        status=status,
        current_phase=current_phase,
        next_action=next_action,
        current_section=current_section,
        tasks_completed=tasks_completed,
        tasks_total=tasks_total,
        progress_percent=progress_percent,
        last_updated=last_updated,
        created=created,
        session_ids=session_ids
    )


def find_most_recent_project_enhanced(
    projects_dir: Path,
    exclude_complete: bool = True,
    exclude_archived: bool = True
) -> Optional[ProjectState]:
    """
    Find most recent project based on last_updated timestamp.

    Enhanced version that:
    - Filters by status (optionally exclude COMPLETE)
    - Skips archived projects
    - Returns full ProjectState, not just ID

    Args:
        projects_dir: Path to 02-projects/ directory
        exclude_complete: Skip COMPLETE projects (default True)
        exclude_archived: Skip archived projects (default True)

    Returns:
        ProjectState of most recent project, or None
    """
    most_recent = None
    most_recent_time = None

    for project_path in projects_dir.iterdir():
        if not project_path.is_dir():
            continue

        # Skip archived projects (name starts with underscore)
        if exclude_archived and project_path.name.startswith('_'):
            logging.info(f"Skipping archived project: {project_path.name}")
            continue

        # Detect project state
        state = detect_project_state(project_path)
        if not state:
            continue

        # Filter by status
        if exclude_complete and state.status == "COMPLETE":
            logging.info(f"Skipping COMPLETE project: {project_path.name}")
            continue

        # Check timestamp
        if not state.last_updated:
            continue

        try:
            # Parse ISO timestamp
            updated_time = datetime.fromisoformat(state.last_updated.replace('Z', '+00:00'))

            if most_recent_time is None or updated_time > most_recent_time:
                most_recent = state
                most_recent_time = updated_time
        except ValueError as e:
            logging.warning(f"Invalid timestamp in {project_path.name}: {e}")
            continue

    return most_recent


def detect_phase_from_metadata(project_path: Path) -> tuple[str, str]:
    """
    Detect project phase with fallback logic.

    Priority:
    1. resume-context.md current_phase + next_action (explicit)
    2. steps.md checkbox analysis (fallback)

    Args:
        project_path: Path to project root

    Returns:
        Tuple of (phase, skill) where:
        - phase: 'planning' | 'execution'
        - skill: 'plan-project' | 'execute-project'
    """
    # Try resume-context.md first (most authoritative)
    resume_metadata = get_project_metadata_from_resume(project_path)
    if 'current_phase' in resume_metadata and 'next_action' in resume_metadata:
        phase = resume_metadata['current_phase']
        skill = resume_metadata['next_action']
        logging.info(f"Using explicit phase from resume-context: {phase} → {skill}")
        return (phase, skill)

    # Fallback: Analyze steps.md checkboxes
    steps_file = project_path / "01-planning" / "04-steps.md"
    if not steps_file.exists():
        logging.warning(f"No steps.md found, defaulting to planning phase")
        return ('planning', 'plan-project')

    try:
        content = steps_file.read_text(encoding="utf-8")
    except Exception as e:
        logging.warning(f"Could not read steps.md: {e}")
        return ('planning', 'plan-project')

    # Look for "Phase 1" section
    phase1_pattern = re.compile(
        r'^##\s*Phase 1[^\n]*\n(.*?)(?=^##\s*Phase [2-9]|\Z)',
        re.MULTILINE | re.DOTALL
    )
    match = phase1_pattern.search(content)

    if not match:
        logging.info("No Phase 1 section found, defaulting to planning")
        return ('planning', 'plan-project')

    phase1_content = match.group(1)

    # Count checkboxes in Phase 1
    completed = len(re.findall(r'^\s*- \[x\]', phase1_content, re.MULTILINE | re.IGNORECASE))
    total = len(re.findall(r'^\s*- \[[x ]\]', phase1_content, re.MULTILINE | re.IGNORECASE))

    if total == 0:
        logging.info("No tasks in Phase 1, defaulting to planning")
        return ('planning', 'plan-project')

    # If ALL Phase 1 tasks complete → execution
    if completed == total:
        logging.info(f"Phase 1 complete ({completed}/{total}), moving to execution")
        return ('execution', 'execute-project')
    else:
        logging.info(f"Phase 1 incomplete ({completed}/{total}), staying in planning")
        return ('planning', 'plan-project')


# Backward compatibility: expose as function matching old signature
def detect_project_phase(nexus_root: str, project_id: str) -> str:
    """
    Legacy function signature for detect_project_phase.

    Returns skill name ('plan-project' | 'execute-project').
    """
    project_path = Path(nexus_root) / "02-projects"
    for folder in project_path.iterdir():
        if folder.name.startswith(f"{project_id}-"):
            _, skill = detect_phase_from_metadata(folder)
            return skill

    return 'plan-project'  # Default
