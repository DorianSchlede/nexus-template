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

    # Look for all 01-overview.md files (numbered naming convention)
    patterns = [
        "*/01-planning/01-overview.md",
        "00-onboarding/*/01-planning/01-overview.md",
    ]

    for pattern in patterns:
        for overview_file in projects_dir.glob(pattern):
            metadata = extract_yaml_frontmatter(str(overview_file))
            if metadata and "error" not in metadata:
                # Count actual checkboxes from 04-steps.md (numbered naming convention)
                project_dir = overview_file.parent.parent
                steps_file = project_dir / "01-planning" / "04-steps.md"

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


def scan_skills_tiered(base_path: str = ".") -> Dict[str, Any]:
    """
    Tiered skill loading for token optimization (~900 tokens vs ~8,250 tokens).

    Strategy:
    - Tier 1 (ALL system skills): Load ALL 00-system/skills/ with descriptions
    - Tier 2 (User connectors): For 03-skills/ folders with *-connect/ subdirectory,
               load connector with description
    - Tier 3 (Other user skills): Auto-add all 03-skills/ skills WITHOUT connect pattern,
               with descriptions

    Returns:
        {
            "core": {
                "projects": [{"name": "create-project", "description": "..."}, ...],
                "learning": [...],
                ...
            },
            "integrations": [{"name": "airtable-connect", "description": "..."}, ...],
            "user": [{"name": "skill-name", "description": "..."}, ...]
        }
    """
    result = {
        "core": {},
        "integrations": [],
        "user": []
    }

    # === TIER 1: ALL System Skills (00-system/skills/) with descriptions ===
    system_skills_dir = Path(base_path) / SYSTEM_DIR / "skills"
    if system_skills_dir.exists() and system_skills_dir.is_dir():
        try:
            # Categorize system skills by their parent folder
            for skill_file in system_skills_dir.glob("**/SKILL.md"):
                try:
                    metadata = extract_yaml_frontmatter(str(skill_file))
                    if not metadata or "error" in metadata:
                        continue

                    skill_name = metadata.get("name", "").strip()
                    skill_desc = metadata.get("description", "").strip()

                    # Skip if name is empty
                    if not skill_name:
                        continue

                    # Determine category from path (e.g., 00-system/skills/projects/create-project)
                    skill_path = Path(metadata.get("_file_path", ""))
                    try:
                        # Get category (parent folder of skill)
                        parts = skill_path.parts
                        skills_idx = parts.index("skills")
                        if skills_idx + 2 < len(parts):
                            category = parts[skills_idx + 1]
                        else:
                            category = "other"
                    except (ValueError, IndexError):
                        category = "other"

                    # Add to category
                    if category not in result["core"]:
                        result["core"][category] = []

                    result["core"][category].append({
                        "name": skill_name,
                        "description": skill_desc
                    })
                except Exception:
                    # Skip individual skill errors, continue processing
                    continue
        except Exception:
            # If glob fails entirely, continue with empty core skills
            pass

    # === TIER 2 + 3: User Skills (03-skills/) ===
    user_skills_dir = Path(base_path) / SKILLS_DIR
    if user_skills_dir.exists() and user_skills_dir.is_dir():
        try:
            # First pass: Detect which skills have *-connect pattern
            connect_skills = set()
            try:
                for item in user_skills_dir.iterdir():
                    if not item.is_dir():
                        continue
                    try:
                        # Check if this folder has a *-connect/ subdirectory
                        for subdir in item.iterdir():
                            if subdir.is_dir() and subdir.name.endswith("-connect"):
                                connect_skills.add(item.name)

                                # Load the connect skill's description (Tier 2)
                                connect_skill_file = subdir / "SKILL.md"
                                skill_desc = ""
                                if connect_skill_file.exists():
                                    try:
                                        metadata = extract_yaml_frontmatter(str(connect_skill_file))
                                        if metadata and "error" not in metadata:
                                            skill_desc = metadata.get("description", "").strip()
                                    except Exception:
                                        pass

                                result["integrations"].append({
                                    "name": subdir.name,
                                    "description": skill_desc
                                })
                                break  # Only add first *-connect found
                    except (OSError, PermissionError):
                        # Skip inaccessible subdirectories
                        continue
            except (OSError, PermissionError):
                # If iterdir fails, continue with empty connect_skills
                pass

            # Second pass: Load all other user skills with descriptions (Tier 3)
            try:
                for skill_file in user_skills_dir.glob("**/SKILL.md"):
                    try:
                        metadata = extract_yaml_frontmatter(str(skill_file))
                        if not metadata or "error" in metadata:
                            continue

                        skill_name = metadata.get("name", "").strip()

                        # Skip if name is empty
                        if not skill_name:
                            continue

                        # Skip if this is a connect skill (already in integrations)
                        if skill_name.endswith("-connect"):
                            continue

                        # Determine parent category folder
                        skill_path = Path(metadata.get("_file_path", ""))
                        try:
                            parts = skill_path.parts
                            skills_idx = parts.index("03-skills")
                            if skills_idx + 1 < len(parts):
                                parent_category = parts[skills_idx + 1]
                            else:
                                parent_category = None
                        except (ValueError, IndexError):
                            parent_category = None

                        # Only add if parent category does NOT have connect pattern
                        # (if parent has connect, we already added the connect skill)
                        if parent_category not in connect_skills:
                            result["user"].append({
                                "name": skill_name,
                                "description": metadata.get("description", "").strip()
                            })
                    except Exception:
                        # Skip individual skill errors
                        continue
            except Exception:
                # If glob fails, continue with empty user skills
                pass
        except Exception:
            # If entire user skills processing fails, continue
            pass

    return result


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
                "status": "configured" if is_active else "available",
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


def load_project(project_id: str, base_path: str = ".", part: int = 0) -> Dict[str, Any]:
    """
    Load project context with metadata and file paths.

    Returns metadata and paths for all planning files. AI should use Read tool
    to load file contents (keeps output under bash limit).

    Args:
        project_id: Project ID or folder name prefix
        base_path: Root path to Nexus installation
        part: Reserved for future use (ignored)

    Returns:
        Dictionary with project metadata and file paths (use Read for content)
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

    # List planning files with metadata (no content - use Read tool)
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
            # Extract YAML metadata only
            metadata = extract_yaml_frontmatter(str(file_path))

            result["files"][file_rel] = {
                "path": str(file_path),
                "metadata": metadata,
                # No content - use Read tool for file contents
            }

    # List outputs directory
    outputs_path = project_path / "03-outputs"
    if outputs_path.exists():
        result["outputs"] = [
            str(f.relative_to(outputs_path)) for f in outputs_path.rglob("*") if f.is_file()
        ]

    # Instructions for AI
    result["_usage"] = {
        "note": "Use Read tool to load file contents in parallel",
        "recommended_reads": [
            f["path"] for f in result["files"].values()
        ],
    }

    return result


def load_skill_slim(skill_name: str, base_path: str = ".") -> Dict[str, Any]:
    """
    Load skill with file tree + SKILL.md only (no reference content).

    This is a lightweight version of load_skill that shows:
    - Skill path
    - Full directory tree with file sizes
    - SKILL.md content
    - List of available references/scripts (paths only, no content)

    Use this when you want to see the skill structure without loading
    all reference files. You can then Read() specific files as needed.

    Args:
        skill_name: Name of the skill to load
        base_path: Root path to Nexus installation

    Returns:
        Dictionary with skill structure and SKILL.md content
    """
    from datetime import datetime

    base = Path(base_path)

    # Search for skill in both locations (supports category subfolders)
    skill_path = None
    for skills_dir in [base / SKILLS_DIR, base / SYSTEM_DIR / "skills"]:
        if not skills_dir.exists():
            continue

        # Direct path (e.g., skills/notion-connect)
        direct_path = skills_dir / skill_name
        if direct_path.exists() and (direct_path / "SKILL.md").exists():
            skill_path = direct_path
            break

        # Search recursively in category subfolders
        for skill_file in skills_dir.glob(f"**/{skill_name}/SKILL.md"):
            skill_path = skill_file.parent
            break

        if skill_path:
            break

    if not skill_path:
        return {"error": f"Skill not found: {skill_name}"}

    # Build file tree representation
    def build_tree(path: Path, prefix: str = "") -> List[str]:
        """Build tree representation of directory."""
        entries = []
        items = sorted(path.iterdir(), key=lambda x: (x.is_file(), x.name))
        for i, item in enumerate(items):
            is_last = i == len(items) - 1
            connector = "└── " if is_last else "├── "
            if item.is_file():
                size = item.stat().st_size
                size_str = f"{size:,} bytes" if size < 10000 else f"{size // 1024}KB"
                entries.append(f"{prefix}{connector}{item.name} ({size_str})")
            else:
                entries.append(f"{prefix}{connector}{item.name}/")
                extension = "    " if is_last else "│   "
                entries.extend(build_tree(item, prefix + extension))
        return entries

    tree_lines = [f"{skill_path.name}/"] + build_tree(skill_path)

    # Read SKILL.md content
    skill_file = skill_path / "SKILL.md"
    skill_content = ""
    if skill_file.exists():
        try:
            skill_content = skill_file.read_text(encoding="utf-8")
        except Exception as e:
            skill_content = f"ERROR reading file: {e}"

    # List available files (paths only, no content)
    references = []
    scripts = []
    assets = []

    refs_path = skill_path / "references"
    if refs_path.exists():
        references = [str(f.relative_to(skill_path)) for f in refs_path.glob("*") if f.is_file()]

    scripts_path = skill_path / "scripts"
    if scripts_path.exists():
        scripts = [str(f.relative_to(skill_path)) for f in scripts_path.glob("*") if f.is_file()]

    assets_path = skill_path / "assets"
    if assets_path.exists():
        assets = [str(f.relative_to(skill_path)) for f in assets_path.glob("*") if f.is_file()]

    return {
        "loaded_at": datetime.now().isoformat(),
        "bundle": "skill_slim",
        "skill_name": skill_name,
        "skill_path": str(skill_path),
        "file_tree": "\n".join(tree_lines),
        "SKILL.md": skill_content,
        "available_files": {
            "references": references,
            "scripts": scripts,
            "assets": assets,
        },
        "hint": "Use Read tool on any file path to load its content",
    }
# =============================================================================
# MVC (Minimum Viable Context) - Slim Generators for Session Start
# =============================================================================
# These functions generate context small enough for hookSpecificOutput.additionalContext
# Target: <8K tokens for startup, <4K tokens for resume
# =============================================================================


def build_skills_xml_compact(base_path: str = ".") -> str:
    """
    Build COMPACT XML representation of skills using CLI discovery pattern.

    Token-optimized (~2,500 tokens vs ~9,500 for full):
    - System skills: Full descriptions (essential for routing)
    - Integration categories: Just connector + CLI hint + operations count
    - User skill categories: Grouped by folder with CLI hint

    Use 'load-skill {category} --help' for full skill listings.

    Returns:
        XML string ready for inclusion in nexus-context
    """
    from xml.sax.saxutils import escape

    xml_parts = []

    # === SYSTEM SKILLS (00-system/skills/) - Full descriptions (essential) ===
    system_skills_dir = Path(base_path) / SYSTEM_DIR / "skills"
    categories: Dict[str, List[Dict[str, str]]] = {}

    if system_skills_dir.exists():
        for skill_file in system_skills_dir.glob("**/SKILL.md"):
            try:
                metadata = extract_yaml_frontmatter(str(skill_file))
                if not metadata or "error" in metadata:
                    continue

                skill_name = metadata.get("name", "").strip()
                skill_desc = metadata.get("description", "").strip()

                if not skill_name:
                    continue

                # Determine category from path
                parts = skill_file.parts
                try:
                    skills_idx = parts.index("skills")
                    category = parts[skills_idx + 1] if skills_idx + 1 < len(parts) else "other"
                except (ValueError, IndexError):
                    category = "other"

                if category not in categories:
                    categories[category] = []

                categories[category].append({
                    "name": skill_name,
                    "description": skill_desc,
                })
            except Exception:
                continue

    # Build system-skills XML (full descriptions)
    xml_parts.append('  <system-skills location="00-system/skills/">')
    for category, skills in sorted(categories.items()):
        xml_parts.append(f'    <category name="{escape(category)}">')
        for skill in skills:
            desc = escape(skill['description']) if skill['description'] else ""
            xml_parts.append(f'      <skill name="{escape(skill["name"])}">{desc}</skill>')
        xml_parts.append('    </category>')
    xml_parts.append('  </system-skills>')

    # === INTEGRATION CATEGORIES (03-skills/*-connect/) - CLI pattern ===
    user_skills_dir = Path(base_path) / SKILLS_DIR
    integration_categories: Dict[str, Dict[str, Any]] = {}

    if user_skills_dir.exists():
        for skill_file in user_skills_dir.glob("**/SKILL.md"):
            try:
                metadata = extract_yaml_frontmatter(str(skill_file))
                if not metadata or "error" in metadata:
                    continue

                skill_name = metadata.get("name", "").strip()
                skill_desc = metadata.get("description", "").strip()

                if not skill_name:
                    continue

                # Get parent folder as category
                parts = skill_file.parts
                try:
                    skills_idx = parts.index("03-skills")
                    category = parts[skills_idx + 1] if skills_idx + 1 < len(parts) else "user"
                except (ValueError, IndexError):
                    category = "user"

                if skill_name.endswith("-connect"):
                    # This is a connector skill
                    if category not in integration_categories:
                        integration_categories[category] = {
                            "connector": None,
                            "operations": 0
                        }
                    integration_categories[category]["connector"] = {
                        "name": skill_name,
                        "description": skill_desc
                    }
                else:
                    # Count as operation in this category
                    if category not in integration_categories:
                        integration_categories[category] = {
                            "connector": None,
                            "operations": 0
                        }
                    integration_categories[category]["operations"] += 1

            except Exception:
                continue

    # Build integration-skills XML (CLI pattern - connector + count + hint)
    xml_parts.append('  <integration-skills location="03-skills/*-connect/">')
    for category, data in sorted(integration_categories.items()):
        if data["connector"]:
            conn = data["connector"]
            desc = escape(conn['description']) if conn['description'] else ""
            ops = data["operations"]
            xml_parts.append(f'    <category name="{escape(category)}" operations="{ops}">')
            xml_parts.append(f'      <connector name="{escape(conn["name"])}">{desc}</connector>')
            if ops > 0:
                xml_parts.append(f'      <cli>load-skill {escape(category)} --help</cli>')
            xml_parts.append('    </category>')
    xml_parts.append('  </integration-skills>')

    # === USER SKILLS (03-skills/ non-connect) - Category summary ===
    user_categories: Dict[str, List[str]] = {}

    if user_skills_dir.exists():
        for skill_file in user_skills_dir.glob("**/SKILL.md"):
            try:
                metadata = extract_yaml_frontmatter(str(skill_file))
                if not metadata or "error" in metadata:
                    continue

                skill_name = metadata.get("name", "").strip()
                if not skill_name or skill_name.endswith("-connect"):
                    continue

                # Get parent folder as category
                parts = skill_file.parts
                try:
                    skills_idx = parts.index("03-skills")
                    category = parts[skills_idx + 1] if skills_idx + 1 < len(parts) else "user"
                except (ValueError, IndexError):
                    category = "user"

                # Skip if this is an integration category (has connector)
                if category in integration_categories and integration_categories[category].get("connector"):
                    continue

                if category not in user_categories:
                    user_categories[category] = []
                user_categories[category].append(skill_name)

            except Exception:
                continue

    # Build user-skills XML (category summary with skill count)
    xml_parts.append('  <user-skills location="03-skills/">')
    for category, skills in sorted(user_categories.items()):
        count = len(skills)
        xml_parts.append(f'    <category name="{escape(category)}" count="{count}">')
        xml_parts.append(f'      <cli>load-skill {escape(category)} --help</cli>')
        xml_parts.append('    </category>')
    xml_parts.append('  </user-skills>')

    return '\n'.join(xml_parts)


def build_skills_xml(base_path: str = ".") -> str:
    """
    Build FULL XML representation of all skills (DEPRECATED - use build_skills_xml_compact).

    Returns XML string with:
    - <system-skills> - All skills from 00-system/skills/ grouped by category
    - <integration-skills> - Skills ending with -connect from 03-skills/
    - <user-skills> - All other skills from 03-skills/

    Each skill has action="read {path}" attribute for direct loading.

    Returns:
        XML string ready for inclusion in nexus-context
    """
    from xml.sax.saxutils import escape

    xml_parts = []

    # === SYSTEM SKILLS (00-system/skills/) ===
    system_skills_dir = Path(base_path) / SYSTEM_DIR / "skills"
    categories: Dict[str, List[Dict[str, str]]] = {}

    if system_skills_dir.exists():
        for skill_file in system_skills_dir.glob("**/SKILL.md"):
            try:
                metadata = extract_yaml_frontmatter(str(skill_file))
                if not metadata or "error" in metadata:
                    continue

                skill_name = metadata.get("name", "").strip()
                skill_desc = metadata.get("description", "").strip()
                skill_path = metadata.get("_file_path", str(skill_file))

                if not skill_name:
                    continue

                # Determine category from path
                parts = Path(skill_path).parts
                try:
                    skills_idx = parts.index("skills")
                    category = parts[skills_idx + 1] if skills_idx + 1 < len(parts) else "other"
                except (ValueError, IndexError):
                    category = "other"

                if category not in categories:
                    categories[category] = []

                categories[category].append({
                    "name": skill_name,
                    "description": skill_desc,
                    "path": skill_path
                })
            except Exception:
                continue

    # Build system-skills XML
    xml_parts.append('  <system-skills location="00-system/skills/">')
    for category, skills in sorted(categories.items()):
        xml_parts.append(f'    <category name="{escape(category)}">')
        for skill in skills:
            action = f"read {skill['path']}"
            desc = escape(skill['description']) if skill['description'] else ""
            xml_parts.append(f'      <skill name="{escape(skill["name"])}" action="{escape(action)}">')
            xml_parts.append(f'        {desc}')
            xml_parts.append('      </skill>')
        xml_parts.append('    </category>')
    xml_parts.append('  </system-skills>')

    # === INTEGRATION SKILLS (03-skills/*-connect/) ===
    user_skills_dir = Path(base_path) / SKILLS_DIR
    integration_skills = []
    other_user_skills = []

    if user_skills_dir.exists():
        for skill_file in user_skills_dir.glob("**/SKILL.md"):
            try:
                metadata = extract_yaml_frontmatter(str(skill_file))
                if not metadata or "error" in metadata:
                    continue

                skill_name = metadata.get("name", "").strip()
                skill_desc = metadata.get("description", "").strip()
                skill_path = metadata.get("_file_path", str(skill_file))

                if not skill_name:
                    continue

                if skill_name.endswith("-connect"):
                    integration_skills.append({
                        "name": skill_name,
                        "description": skill_desc,
                        "path": skill_path
                    })
                else:
                    other_user_skills.append({
                        "name": skill_name,
                        "description": skill_desc,
                        "path": skill_path
                    })
            except Exception:
                continue

    # Build integration-skills XML
    xml_parts.append('  <integration-skills location="03-skills/*-connect/">')
    for skill in integration_skills:
        action = f"read {skill['path']}"
        desc = escape(skill['description']) if skill['description'] else ""
        xml_parts.append(f'    <skill name="{escape(skill["name"])}" action="{escape(action)}">')
        xml_parts.append(f'      {desc}')
        xml_parts.append('    </skill>')
    xml_parts.append('  </integration-skills>')

    # Build user-skills XML
    xml_parts.append('  <user-skills location="03-skills/">')
    for skill in other_user_skills:
        action = f"read {skill['path']}"
        desc = escape(skill['description']) if skill['description'] else ""
        xml_parts.append(f'    <skill name="{escape(skill["name"])}" action="{escape(action)}">')
        xml_parts.append(f'      {desc}')
        xml_parts.append('    </skill>')
    xml_parts.append('  </user-skills>')

    return '\n'.join(xml_parts)


def extract_essential_orchestrator(base_path: str = ".") -> Dict[str, Any]:
    """
    Extract MINIMAL routing rules from orchestrator.md (~500 tokens vs ~4K).

    Returns structured data instead of full prose:
    - Routing priority table
    - Core skill triggers
    - Never-do list
    - Mode rules

    For full orchestrator content, AI should read the file directly when needed.
    """
    return {
        "routing": [
            {"priority": 1, "match": "skill trigger", "action": "load matched skill"},
            {"priority": 2, "match": "integration keyword", "action": "load {name}-connect"},
            {"priority": 3, "match": "project number/name", "action": "execute-project"},
            {"priority": 4, "match": "no match", "action": "respond naturally"},
        ],
        "core_skills": {
            "plan-project": "User wants to START something NEW with deliverable",
            "execute-project": "User references EXISTING project by name/ID",
            "create-skill": "User wants to AUTOMATE repeating work",
        },
        "skill_priority": "00-system/skills/ > 03-skills/ (System skills have priority!)",
        "concepts": {
            "project": "Temporal work with beginning/end. Location: 02-projects/",
            "skill": "Reusable workflow. 00-system/skills/ (system, priority) > 03-skills/ (user)",
            "decision": "Will do ONCE? → Project. Will do AGAIN? → Skill.",
        },
        "never_do": [
            "Never create project/skill folders directly → use create-* skills",
            "Never auto-load learning skills → suggest, user decides",
            "Never create README.md, CHANGELOG.md in skills → clutter",
            "Never add documentation not needed for AI execution",
        ],
        "mode_rules": {
            "plan_mode": "Project status=PLANNING: Read files, discuss approach",
            "execute_mode": "Project status=IN_PROGRESS: Follow steps.md, don't read files directly",
        },
    }


def load_full_startup_context(base_path: str = ".") -> Dict[str, Any]:
    """
    Load FULL startup context for SessionStart hook additionalContext injection.

    Loading order (Attention-Based - Revised):
    Optimized for LLM attention with identity-first approach:

    PRIMACY (WHO AM I - Most critical):
    1. user_goals - WHO I am, WHAT I want (identity/purpose)

    EARLY (Current context):
    2. user_projects - WHAT I'm working on now (minimal: id, name, status, progress, current_task)
    3. orchestrator - HOW to behave (rules, but after knowing WHO)

    MIDDLE (Bulk data - lower attention):
    4. skills - WHERE to route (reference, less critical during attention scan)

    LATE (Reference material):
    5. workspace_map - HOW workspace is organized
    6. memory_map - HOW memory system works
    7. system_map - HOW system is structured

    RECENCY (Memory anchor):
    8. stats - Quick summary (last thing seen)

    Returns:
        Complete context bundle with all nexus data
    """
    from datetime import datetime

    base = Path(base_path)
    result = {
        "loaded_at": datetime.now().isoformat(),
        "bundle": "full_startup",
    }

    # === PRIMACY: WHO AM I ===

    # 1. User Goals - WHO AM I, WHAT I WANT (Most critical context)
    try:
        goals_path = base / "01-memory" / "goals.md"
        if goals_path.exists():
            result["user_goals"] = goals_path.read_text(encoding="utf-8")
    except Exception:
        pass

    # === EARLY: Current Work + Behavior ===

    # 2. Projects - WHAT user is doing now (minimal metadata only)
    # Include ACTIVE for backwards compatibility with older projects
    all_projects = scan_projects(base_path, minimal=True)
    active_projects = [
        p for p in all_projects
        if p.get("status") in ("IN_PROGRESS", "PLANNING", "ACTIVE")
    ]
    # Minimize to essential fields only
    result["user_projects"] = [
        {
            "id": p["id"],
            "name": p["name"],
            "status": p["status"],
            "progress": p.get("progress", 0),
            "current_task": p.get("current_task")
        }
        for p in active_projects
    ]

    # 3. Orchestrator - HOW to behave (after knowing WHO)
    try:
        orch_path = base / "00-system" / "core" / "orchestrator.md"
        if orch_path.exists():
            result["orchestrator"] = extract_essential_orchestrator(base_path)
    except Exception as e:
        result["orchestrator"] = {"error": str(e)}

    # === MIDDLE: Bulk Data (Lower Attention) ===

    # 4. Skills - Routing reference (WHERE to route) - TIERED LOADING
    result["skills"] = scan_skills_tiered(base_path)

    # === LATE: Reference Material ===
    # NOTE: Full map contents REMOVED to prevent duplication with resume context.
    # Maps are loaded on-demand when AI needs them, not in every context bundle.
    # This saves ~6K tokens per session.

    # === RECENCY: Memory Anchor ===

    # 8. Stats - Quick summary (recency effect)
    # Calculate total skills from tiered structure
    total_skills_count = 0
    if isinstance(result.get("skills"), dict):
        # Count core skills
        for category_skills in result["skills"].get("core", {}).values():
            total_skills_count += len(category_skills)
        # Count integration connectors
        total_skills_count += len(result["skills"].get("integrations", []))
        # Count user skills
        total_skills_count += len(result["skills"].get("user", []))

    result["stats"] = {
        "total_projects": len(all_projects),
        "active_projects": len(result["user_projects"]),
        "total_skills": total_skills_count,
    }

    # === ACTION INSTRUCTIONS & STATE DETECTION ===
    # Use state.py functions for comprehensive state detection and instructions

    try:
        from .state import (
            check_goals_personalized,
            check_workspace_configured,
            build_display_hints,
            build_pending_onboarding,
            extract_learning_completed,
        )
    except ImportError:
        # Fallback if state.py not available
        check_goals_personalized = None
        check_workspace_configured = None
        build_display_hints = None
        build_pending_onboarding = None
        extract_learning_completed = None

    # Check goals personalization
    goals_path = base / "01-memory" / "goals.md"
    if check_goals_personalized:
        goals_personalized = check_goals_personalized(goals_path)
    else:
        # Fallback: simple check
        goals_personalized = False
        try:
            if goals_path.exists():
                content = goals_path.read_text(encoding="utf-8")
                if "smart_default: true" not in content.lower():
                    goals_personalized = True
        except Exception:
            pass

    # Check workspace configuration
    if check_workspace_configured:
        workspace_configured = check_workspace_configured(base)
    else:
        workspace_configured = False

    # Get learning completion status
    learning_completed = {}
    pending_onboarding = []
    if extract_learning_completed and build_pending_onboarding:
        try:
            config_path = base / "01-memory" / "user-config.yaml"
            learning_completed = extract_learning_completed(config_path)
            pending_onboarding = build_pending_onboarding(learning_completed)
        except Exception:
            pass

    # Build display hints (for menu rendering suggestions)
    display_hints = []
    if build_display_hints:
        try:
            display_hints = build_display_hints(
                update_info={},  # TODO: Add update check integration
                pending_onboarding=pending_onboarding,
                goals_personalized=goals_personalized,
                workspace_configured=workspace_configured,
            )
        except Exception:
            display_hints = []

    # State detection for onboarding suggestions
    result["state"] = {
        "goals_personalized": goals_personalized,
        "workspace_configured": workspace_configured,
        "has_active_projects": len(result["user_projects"]) > 0,
        "has_planning_projects": len([p for p in result["user_projects"] if p.get("status") == "PLANNING"]) > 0,
        "has_in_progress_projects": len([p for p in result["user_projects"] if p.get("status") == "IN_PROGRESS"]) > 0,
        "learning_completed": learning_completed,
        "pending_onboarding": pending_onboarding,
        "onboarding_complete": len(pending_onboarding) == 0,
        "display_hints": display_hints,
    }

    # Action instruction based on state
    result["action"] = "display_menu"

    # Build state-aware instruction
    instruction_parts = [
        "Display the complete Nexus menu from orchestrator.md:",
        "- ASCII banner with version",
        "- User memory status (use state.goals_personalized flag)",
        "- Active projects (user_projects)",
        "- Available skills by category (skills.core, skills.integrations, skills.user)",
        "- Workspace status (use state.workspace_configured flag)",
        "- Integrations status",
    ]

    # Add onboarding guidance if needed
    if not goals_personalized:
        instruction_parts.append("⚠️  ONBOARDING: Goals not personalized - prominently suggest 'setup memory' as #1 next step")
    if not workspace_configured:
        instruction_parts.append("⚠️  ONBOARDING: Workspace not configured - suggest 'setup workspace' in next steps")

    # Add display hints guidance
    if display_hints:
        instruction_parts.append(f"📌 DISPLAY HINTS: {', '.join(display_hints)}")

    instruction_parts.append("- Suggested next steps (numbered, state-aware, see orchestrator.md for logic)")

    result["instruction"] = "\n".join(instruction_parts)

    return result


# =============================================================================
# State Template Functions for Dynamic Instructions (MECE Compliant)
# =============================================================================
# These functions generate state-specific instructions using priority-based selection.
# Uses MECE principle: Mutually Exclusive, Collectively Exhaustive.
# First match wins - no overlapping states.
# =============================================================================


def build_next_action_instruction(context: Dict[str, Any]) -> str:
    """
    Generate state-specific instruction using priority-based selection.

    Uses MECE principle: Mutually Exclusive, Collectively Exhaustive.
    First match wins - no overlapping states.

    Args:
        context: Full startup context with stats, projects, onboarding

    Returns:
        Markdown string with clear next-action directive
    """
    # Priority 0: First run (no goals, no projects) - auto-trigger setup
    if not context.get("goals_personalized", False) and context.get("total_projects", 0) == 0:
        return _template_first_run(context)

    # Priority 1: Onboarding incomplete (goals set but other onboarding pending)
    if len(context.get("pending_onboarding", [])) > 0:
        return _template_onboarding_incomplete(context)

    # Priority 2: Active work exists
    if len(context.get("active_projects", [])) > 0:
        return _template_active_projects(context)

    # Priority 3: Workspace needs sync
    if context.get("workspace_needs_validation", False):
        return _template_workspace_modified(context)

    # Priority 4: Fresh start (goals configured, no projects yet)
    if context.get("total_projects", 0) == 0:
        return _template_fresh_workspace(context)

    # Priority 5: System ready (fallback)
    return _template_system_ready(context)


def _load_state_template(template_name: str, **kwargs) -> str:
    """Load state template from .claude/hooks/templates/ and format with kwargs."""
    # Templates are in .claude/hooks/templates/ relative to project root
    # loaders.py is in 00-system/core/nexus/, so go up 3 levels to project root
    template_dir = Path(__file__).parent.parent.parent.parent / ".claude" / "hooks" / "templates"
    template_path = template_dir / f"{template_name}.md"

    try:
        template = template_path.read_text(encoding='utf-8')
        return template.format(**kwargs) if kwargs else template
    except FileNotFoundError:
        return f"Template {template_name} not found at {template_path}"
    except KeyError as e:
        # Return unformatted if missing variable
        return template_path.read_text(encoding='utf-8')


def _template_first_run(context: Dict[str, Any]) -> str:
    """STARTUP STATE 0: First run - auto-trigger setup-memory skill."""
    return _load_state_template("startup_first_run")


def _template_onboarding_incomplete(context: Dict[str, Any]) -> str:
    """STARTUP STATE 1: Onboarding incomplete - gently suggest completing setup."""
    pending = context.get("pending_onboarding", [])
    pending_list = "\n".join(f"- {skill}" for skill in pending[:3])
    return _load_state_template("startup_onboarding_incomplete", pending_list=pending_list)


def _template_active_projects(context: Dict[str, Any]) -> str:
    """STARTUP STATE 2: Active projects exist - highlight project continuations."""
    projects = context.get("active_projects", [])[:2]  # Max 2
    project_list = "\n".join(
        f"- Project {p.get('id', '?')}: {p.get('name', 'Unknown')} ({p.get('status', '?')}, {p.get('progress', 0)}%)"
        for p in projects
    )
    return _load_state_template("startup_active_projects", project_list=project_list)


def _template_workspace_modified(context: Dict[str, Any]) -> str:
    """STARTUP STATE 3: Workspace changes detected - suggest running update-workspace-map."""
    return _load_state_template("startup_workspace_modified")


def _template_fresh_workspace(context: Dict[str, Any]) -> str:
    """STARTUP STATE 4: Fresh workspace (configured but no projects) - emphasize starting first project."""
    return _load_state_template("startup_fresh_workspace")


def _template_system_ready(context: Dict[str, Any]) -> str:
    """STARTUP STATE 5: System ready (fallback) - open-ended, ready for anything."""
    return _load_state_template("startup_system_ready")


def build_suggested_next_steps(context: Dict[str, Any]) -> List[str]:
    """
    Build prioritized list of suggested actions based on state.

    Returns ordered list of suggestions (max 5).
    """
    suggestions = []

    # Priority 1: Critical onboarding
    if not context.get("goals_personalized"):
        suggestions.append("'setup memory' - configure your goals and role (5 min)")

    if not context.get("workspace_configured"):
        suggestions.append("'setup workspace' - organize your folder structure (10 min)")

    # Priority 2: Active work
    active_projects = context.get("active_projects", [])

    for proj in active_projects[:2]:  # Max 2 project suggestions
        name = proj.get("name", "Unknown")
        progress = proj.get("progress", 0)
        suggestions.append(f"'continue {name}' - resume at {progress}%")

    # Priority 3: Workspace maintenance
    if context.get("workspace_needs_validation"):
        suggestions.append("'validate workspace' - sync workspace-map.md")

    # Priority 4: End of session
    suggestions.append("'close session' - save progress and learnings")

    # Priority 5: Exploration (if room)
    if len(suggestions) < 5:
        if context.get("total_projects") == 0:
            suggestions.append("'create project' - start your first project")
        else:
            suggestions.append("'explain nexus' - learn system capabilities")

    # Return top 5
    return suggestions[:5]


# =============================================================================
# CLI Discovery Functions for Integration Skills
# =============================================================================
# Use: load-skill {category} --help
# Returns formatted list of all skills in a category without auto-loading them
# =============================================================================


def discover_skills_in_category(category: str, base_path: str = ".") -> Dict[str, Any]:
    """
    Discover all skills in an integration category.

    This enables the `load-skill {category} --help` pattern that prevents
    auto-loading all skills (e.g., 28 langfuse skills) at startup.

    Args:
        category: Integration category name (e.g., "langfuse", "slack", "notion")
        base_path: Root path to Nexus installation

    Returns:
        Dictionary with:
        - category: Category name
        - skills: List of skill metadata dicts
        - count: Number of skills found
        - formatted: Ready-to-display formatted output

    Usage:
        result = discover_skills_in_category("langfuse")
        print(result["formatted"])  # Formatted skill list
    """
    base = Path(base_path)
    result = {
        "category": category,
        "skills": [],
        "count": 0,
        "formatted": "",
    }

    # Search in both user skills (03-skills/) and system skills (00-system/skills/)
    search_dirs = [
        base / SKILLS_DIR / category,  # 03-skills/{category}/
        base / SYSTEM_DIR / "skills" / category,  # 00-system/skills/{category}/
    ]

    found_skills = []

    for skills_dir in search_dirs:
        if not skills_dir.exists() or not skills_dir.is_dir():
            continue

        # Find all SKILL.md files in this category
        for skill_file in skills_dir.glob("*/SKILL.md"):
            try:
                metadata = extract_yaml_frontmatter(str(skill_file))
                if not metadata or "error" in metadata:
                    continue

                skill_name = metadata.get("name", "").strip()
                skill_desc = metadata.get("description", "").strip()
                skill_path = metadata.get("_file_path", str(skill_file))

                if not skill_name:
                    continue

                # Skip the *-connect skill (connector is loaded separately)
                # But include it in discovery for completeness
                found_skills.append({
                    "name": skill_name,
                    "description": skill_desc,
                    "path": skill_path,
                    "is_connector": skill_name.endswith("-connect"),
                })
            except Exception:
                continue

    # Sort: connector first, then alphabetically
    found_skills.sort(key=lambda x: (not x["is_connector"], x["name"]))

    result["skills"] = found_skills
    result["count"] = len(found_skills)

    # Build formatted output
    if found_skills:
        lines = [
            f"{category.title()} Operations ({len(found_skills)} skills):",
            "",
        ]

        # Group by connector vs operations
        connector = [s for s in found_skills if s["is_connector"]]
        operations = [s for s in found_skills if not s["is_connector"]]

        if connector:
            lines.append("[Connector]")
            for skill in connector:
                lines.append(f"  - {skill['name']}: {skill['description']}")
            lines.append("")

        if operations:
            lines.append("[Operations]")
            for skill in operations:
                lines.append(f"  - {skill['name']}: {skill['description']}")
            lines.append("")

        lines.append(f"To load a skill: read {category}/{{skill-name}}/SKILL.md")

        result["formatted"] = "\n".join(lines)
    else:
        result["formatted"] = f"No skills found in category: {category}"

    return result


def list_integration_categories(base_path: str = ".") -> List[Dict[str, Any]]:
    """
    List all available integration categories.

    Scans 03-skills/ for folders with *-connect subdirectories.

    Returns:
        List of category dicts with name, path, and skill count
    """
    base = Path(base_path)
    categories = []

    user_skills_dir = base / SKILLS_DIR

    if not user_skills_dir.exists():
        return categories

    for item in user_skills_dir.iterdir():
        if not item.is_dir():
            continue

        # Check if this has a *-connect subdirectory
        has_connect = False
        for subdir in item.iterdir():
            if subdir.is_dir() and subdir.name.endswith("-connect"):
                has_connect = True
                break

        if has_connect:
            # Count skills in this category
            skill_count = sum(1 for f in item.glob("*/SKILL.md"))
            categories.append({
                "name": item.name,
                "path": str(item),
                "skill_count": skill_count,
            })

    return sorted(categories, key=lambda x: x["name"])
