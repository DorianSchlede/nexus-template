"""
Loaders for Nexus.

This module handles scanning and loading of:
- Projects (from 02-projects/)
- Skills (from 03-skills/ and 00-system/skills/)
- Memory files (from 01-memory/)
- Integrations (from .env and skill folders)
"""

import re
from pathlib import Path
from typing import Any, Dict, List, Optional

from .config import (
    INTEGRATION_ENV_VARS,
    MEMORY_DIR,
    PROJECTS_DIR,
    SKILLS_DIR,
    SYSTEM_DIR,
    get_templates_dir,
)
from .utils import (
    count_checkboxes,
    extract_yaml_frontmatter,
    get_first_unchecked_task,
    is_template_file,
    parse_env_file,
)


def scan_projects(base_path: str = ".", minimal: bool = True) -> List[Dict[str, Any]]:
    """
    Scan all projects and extract YAML metadata + count actual tasks.

    Args:
        base_path: Root path to scan from
        minimal: If True, return only essential fields for routing/display (default)
                 If False, return all YAML fields

    Returns:
        List of project metadata dictionaries
    """
    projects = []
    projects_dir = Path(base_path) / PROJECTS_DIR

    if not projects_dir.exists():
        return []

    # Look for all overview.md files in root and onboarding folder
    patterns = [
        "*/01-planning/overview.md",
        "00-onboarding/*/01-planning/overview.md",
    ]

    for pattern in patterns:
        for overview_file in projects_dir.glob(pattern):
            metadata = extract_yaml_frontmatter(str(overview_file))
            if metadata and "error" not in metadata:
                # Count actual checkboxes from steps.md
                project_dir = overview_file.parent.parent
                steps_file = project_dir / "01-planning" / "steps.md"

                total, completed, uncompleted = count_checkboxes(steps_file)

                # OVERRIDE YAML metadata with actual counts from steps.md
                # This ensures single source of truth: steps.md checkboxes
                metadata["tasks_total"] = total
                metadata["tasks_completed"] = completed
                metadata["progress"] = round(completed / total, 3) if total > 0 else 0.0

                # Add current task (first unchecked task)
                if steps_file.exists() and uncompleted > 0:
                    try:
                        content = steps_file.read_text(encoding="utf-8")
                        current_task = get_first_unchecked_task(content)
                        if current_task:
                            metadata["current_task"] = current_task
                    except Exception:
                        pass

                # PROGRESSIVE DISCLOSURE: Return minimal fields for efficiency
                if minimal:
                    metadata = {
                        "id": metadata.get("id"),
                        "name": metadata.get("name"),
                        "description": metadata.get("description", ""),
                        "status": metadata.get("status"),
                        "onboarding": metadata.get("onboarding", False),
                        "created": metadata.get("created"),
                        "updated": metadata.get("updated"),
                        "progress": metadata["progress"],
                        "tasks_total": metadata["tasks_total"],
                        "tasks_completed": metadata["tasks_completed"],
                        "current_task": metadata.get("current_task"),
                        "_file_path": metadata.get("_file_path"),
                    }

                projects.append(metadata)

    return projects


def scan_skills(base_path: str = ".", minimal: bool = True) -> List[Dict[str, Any]]:
    """
    Scan all skills and extract YAML metadata.

    Args:
        base_path: Root path to scan from
        minimal: If True, return only essential fields for routing/display (default)
                 If False, return all YAML fields

    Returns:
        List of skill metadata dictionaries, ordered by priority:
        1. CORE skills (create-project, execute-project, create-skill)
        2. LEARNING skills (setup-goals, learn-projects, etc.)
        3. All other skills
    """
    skills = []
    core_skills = []
    learning_skills = []

    # CORE SKILLS - highest priority, always at top
    CORE_SKILL_NAMES = {"create-project", "execute-project", "create-skill"}

    # LEARNING SKILLS - second priority, for onboarding
    LEARNING_SKILL_NAMES = {
        "setup-memory", "setup-workspace", "learn-projects",
        "learn-skills", "learn-integrations", "learn-nexus"
    }

    # Try both 03-skills/ (user skills) and 00-system/skills/ (system skills)
    skills_dirs = [
        Path(base_path) / SKILLS_DIR,
        Path(base_path) / SYSTEM_DIR / "skills",
    ]

    for skills_dir in skills_dirs:
        if not skills_dir.exists():
            continue

        # Look for all SKILL.md files (recursive to support category subfolders)
        for skill_file in skills_dir.glob("**/SKILL.md"):
            metadata = extract_yaml_frontmatter(str(skill_file))
            if metadata and "error" not in metadata:
                skill_name = metadata.get("name", "")

                # PROGRESSIVE DISCLOSURE: Return minimal fields for efficiency
                if minimal:
                    metadata = {
                        "name": skill_name,
                        "description": metadata.get("description", ""),
                        "_file_path": metadata.get("_file_path"),
                    }

                # Categorize by priority
                if skill_name in CORE_SKILL_NAMES:
                    core_skills.append(metadata)
                elif skill_name in LEARNING_SKILL_NAMES:
                    learning_skills.append(metadata)
                else:
                    skills.append(metadata)

    # Return in priority order: CORE → LEARNING → others
    return core_skills + learning_skills + skills


def detect_configured_integrations(base_path: str = ".") -> List[Dict[str, Any]]:
    """
    Detect which integrations are actually configured (have credentials).

    An integration is considered "active" if:
    1. It has a master skill folder (00-system/skills/{integration}/{integration}-master/)
    2. The required environment variable is set in .env

    Returns:
        List of dicts with integration name, available skills, and active status
    """
    integrations = []
    skills_dir = Path(base_path) / SYSTEM_DIR / "skills"

    if not skills_dir.exists():
        return []

    # Load .env file if exists
    env_vars = parse_env_file(Path(base_path) / ".env")

    # Known integration patterns (folders that represent external service integrations)
    # These follow the master/connect/specialized pattern
    for category_dir in skills_dir.iterdir():
        if not category_dir.is_dir():
            continue

        category_name = category_dir.name

        # Check if this category has a master skill (indicates it's an integration)
        master_skill = category_dir / f"{category_name}-master"
        if master_skill.exists() and (master_skill / "SKILL.md").exists():
            # Check if credentials are configured
            required_env = INTEGRATION_ENV_VARS.get(category_name.lower())
            is_active = required_env and required_env in env_vars

            integration = {
                "name": category_name,
                "slug": category_name.lower(),
                "skills": [],
                "active": is_active,
                "required_env": required_env,
            }

            # List all skills in this integration
            for skill_dir in category_dir.iterdir():
                if skill_dir.is_dir() and (skill_dir / "SKILL.md").exists():
                    integration["skills"].append(skill_dir.name)

            integrations.append(integration)

    return integrations


def load_memory_files(base_path: str = ".") -> Dict[str, Any]:
    """
    Load memory file paths and check their existence.

    Args:
        base_path: Root path to Nexus installation

    Returns:
        Dictionary with file paths and existence status
    """
    base = Path(base_path)
    memory_path = base / MEMORY_DIR

    files = {
        "goals": memory_path / "goals.md",
        "user_config": memory_path / "user-config.yaml",
        "memory_map": memory_path / "memory-map.md",
        "core_learnings": memory_path / "core-learnings.md",
    }

    return {
        "paths": {key: str(path) for key, path in files.items()},
        "exists": {key: path.exists() for key, path in files.items()},
    }


def create_smart_defaults(base_path: str) -> Dict[str, Any]:
    """
    Create smart default template files for immediate system operation.

    This enables users to start working immediately without onboarding.
    Files are created with `smart_default: true` flag for detection.

    Args:
        base_path: Root path to Nexus installation

    Returns:
        Dict with 'created' and 'skipped' lists of file names
    """
    base = Path(base_path)
    memory_path = base / MEMORY_DIR
    templates_dir = get_templates_dir()

    result = {
        "created": [],
        "skipped": [],
        "errors": [],
    }

    # Ensure directories exist
    try:
        memory_path.mkdir(parents=True, exist_ok=True)
        (memory_path / "session-reports").mkdir(exist_ok=True)
    except Exception as e:
        result["errors"].append(f"Failed to create directories: {e}")
        return result

    # Define template files to create
    templates = {
        "goals.md": "goals.md",
        "user-config.yaml": "user-config.yaml",
        "memory-map.md": "memory-map.md",
        "core-learnings.md": "core-learnings.md",
    }

    # Create each file (skip if exists)
    for filename, template_name in templates.items():
        file_path = memory_path / filename

        if file_path.exists():
            result["skipped"].append(filename)
            continue

        try:
            template_path = templates_dir / template_name
            if template_path.exists():
                content = template_path.read_text(encoding="utf-8")
            else:
                result["errors"].append(f"Template not found: {template_name}")
                continue

            file_path.write_text(content, encoding="utf-8")
            result["created"].append(filename)
        except Exception as e:
            result["errors"].append(f"Failed to create {filename}: {e}")

    return result


def load_project(project_id: str, base_path: str = ".") -> Dict[str, Any]:
    """
    Load complete project context (all planning files).

    Args:
        project_id: Project ID or folder name prefix
        base_path: Root path to Nexus installation

    Returns:
        Dictionary with project files and metadata
    """
    from datetime import datetime

    base = Path(base_path)
    project_path = None

    # Find project by ID
    search_dirs = [
        base / PROJECTS_DIR,
        base / PROJECTS_DIR / "00-onboarding",
    ]

    for search_dir in search_dirs:
        if not search_dir.exists():
            continue
        for proj_dir in search_dir.glob("*"):
            if proj_dir.is_dir() and proj_dir.name.startswith(project_id):
                project_path = proj_dir
                break
        if project_path:
            break

    if not project_path:
        return {"error": f"Project not found: {project_id}"}

    result = {
        "loaded_at": datetime.now().isoformat(),
        "bundle": "project",
        "project_id": project_id,
        "project_path": str(project_path),
        "files": {},
    }

    # Load all planning files
    planning_files = [
        "01-planning/overview.md",
        "01-planning/plan.md",
        "01-planning/requirements.md",
        "01-planning/design.md",
        "01-planning/steps.md",
    ]

    for file_rel in planning_files:
        file_path = project_path / file_rel
        if file_path.exists():
            # Extract YAML metadata
            metadata = extract_yaml_frontmatter(str(file_path))

            result["files"][file_rel] = {
                "path": str(file_path),
                "metadata": metadata,
                # NO 'content' field - use Read tool for complete content
            }

    # List outputs directory
    outputs_path = project_path / "03-outputs"
    if outputs_path.exists():
        result["outputs"] = [
            str(f.relative_to(outputs_path)) for f in outputs_path.rglob("*") if f.is_file()
        ]

    return result


def load_skill(skill_name: str, base_path: str = ".") -> Dict[str, Any]:
    """
    Load complete skill context.

    Args:
        skill_name: Name of the skill to load
        base_path: Root path to Nexus installation

    Returns:
        Dictionary with skill files and metadata
    """
    from datetime import datetime

    base = Path(base_path)

    # Search for skill in both locations (supports category subfolders)
    skill_path = None

    for skills_dir in [base / SKILLS_DIR, base / SYSTEM_DIR / "skills"]:
        if not skills_dir.exists():
            continue

        # First try direct path (e.g., skills/notion-connect)
        direct_path = skills_dir / skill_name
        if direct_path.exists() and (direct_path / "SKILL.md").exists():
            skill_path = direct_path
            break

        # Then search recursively in category subfolders (e.g., skills/notion/notion-connect)
        for skill_file in skills_dir.glob(f"**/{skill_name}/SKILL.md"):
            skill_path = skill_file.parent
            break

        if skill_path:
            break

    if not skill_path:
        return {"error": f"Skill not found: {skill_name}"}

    result = {
        "loaded_at": datetime.now().isoformat(),
        "bundle": "skill",
        "skill_name": skill_name,
        "skill_path": str(skill_path),
        "files": {},
        "references_loaded": [],
        "scripts_loaded": [],
        "assets_available": [],
    }

    # Load SKILL.md with full content
    skill_file = skill_path / "SKILL.md"
    if skill_file.exists():
        metadata = extract_yaml_frontmatter(str(skill_file))

        # Read full content
        try:
            with open(skill_file, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            content = f"ERROR reading file: {e}"

        result["files"]["SKILL.md"] = {
            "path": str(skill_file),
            "metadata": metadata,
            "content": content,
        }

        # AUTO-LOAD references declared in YAML (with content)
        if metadata and "load_references" in metadata:
            references_path = skill_path / "references"
            if references_path.exists():
                for ref_file in metadata["load_references"]:
                    ref_path = references_path / ref_file
                    if ref_path.exists():
                        try:
                            with open(ref_path, "r", encoding="utf-8") as f:
                                ref_content = f.read()
                        except Exception as e:
                            ref_content = f"ERROR reading file: {e}"
                        result["files"][f"references/{ref_file}"] = {
                            "path": str(ref_path),
                            "content": ref_content,
                        }
                        result["references_loaded"].append(ref_file)

        # AUTO-LOAD scripts declared in YAML (with content)
        if metadata and "load_scripts" in metadata:
            scripts_path = skill_path / "scripts"
            if scripts_path.exists():
                for script_file in metadata["load_scripts"]:
                    script_path_file = scripts_path / script_file
                    if script_path_file.exists():
                        try:
                            with open(script_path_file, "r", encoding="utf-8") as f:
                                script_content = f.read()
                        except Exception as e:
                            script_content = f"ERROR reading file: {e}"
                        result["files"][f"scripts/{script_file}"] = {
                            "path": str(script_path_file),
                            "content": script_content,
                        }
                        result["scripts_loaded"].append(script_file)

    # List remaining references (not auto-loaded)
    references_path = skill_path / "references"
    if references_path.exists():
        all_refs = [f.name for f in references_path.glob("*") if f.is_file()]
        result["references_available"] = [r for r in all_refs if r not in result["references_loaded"]]

    # List remaining scripts (not auto-loaded)
    scripts_path = skill_path / "scripts"
    if scripts_path.exists():
        all_scripts = [f.name for f in scripts_path.glob("*") if f.is_file()]
        result["scripts_available"] = [s for s in all_scripts if s not in result["scripts_loaded"]]

    # List assets (never auto-loaded)
    assets_path = skill_path / "assets"
    if assets_path.exists():
        result["assets_available"] = [f.name for f in assets_path.glob("*") if f.is_file()]

    return result


def load_metadata(base_path: str = ".") -> Dict[str, Any]:
    """
    Load ONLY project and skill metadata (no memory content).

    Use this as a second call after --startup to get full metadata
    when the combined output would exceed bash limits (~30K chars).

    Args:
        base_path: Root path to Nexus installation

    Returns:
        - projects: Full project metadata list
        - skills: Full skill metadata list
        - stats: Counts and summary
    """
    from datetime import datetime

    result = {
        "loaded_at": datetime.now().isoformat(),
        "bundle": "metadata",
        "projects": scan_projects(base_path, minimal=True),
        "skills": scan_skills(base_path, minimal=True),
    }

    result["stats"] = {
        "total_projects": len(result["projects"]),
        "total_skills": len(result["skills"]),
        "active_projects": len([p for p in result["projects"] if p.get("status") == "IN_PROGRESS"]),
    }

    return result
