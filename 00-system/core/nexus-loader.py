#!/usr/bin/env python3
"""
nexus-loader.py - Context loader and directive executor for Nexus-v3

Usage:
    python nexus-loader.py --startup
    python nexus-loader.py --execute-directive
    python nexus-loader.py --project 05-website-development
    python nexus-loader.py --skill weekly-status-report
    python nexus-loader.py --list-projects
    python nexus-loader.py --list-skills
"""

import os
import re
import sys
import yaml
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any

# Token counting constants
CHARS_PER_TOKEN = 4  # Rough estimate: 1 token ≈ 4 characters
CONTEXT_WINDOW = 200000  # Claude's context window
METADATA_BUDGET_WARNING = 7000  # Warn if metadata >7K tokens (3.5% of window)

# MANDATORY NAVIGATION MAPS (Always loaded at startup)
# These provide core system navigation and context
MANDATORY_MAPS = [
    "00-system/system-map.md",              # System structure and navigation hub
]


def extract_yaml_frontmatter(file_path: str) -> Optional[Dict[str, Any]]:
    """Extract YAML frontmatter from markdown file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Match YAML frontmatter: ---\n[yaml]\n---
        match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
        if not match:
            return None

        yaml_content = match.group(1)
        metadata = yaml.safe_load(yaml_content)

        if metadata:
            # Convert any date objects to ISO format strings for JSON serialization
            for key, value in metadata.items():
                if hasattr(value, 'isoformat'):  # datetime, date objects
                    metadata[key] = value.isoformat()

            metadata['_file_path'] = str(file_path)
            metadata['_file_name'] = Path(file_path).name

        return metadata

    except Exception as e:
        return {'error': str(e), '_file_path': str(file_path)}


def load_file_content(file_path: str) -> str:
    """Load full file content."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"ERROR: {e}"


def estimate_tokens(text: str) -> int:
    """Estimate token count from text (rough approximation)."""
    if not text:
        return 0
    return len(text) // CHARS_PER_TOKEN


def calculate_bundle_tokens(result: Dict[str, Any]) -> Dict[str, int]:
    """Calculate token costs for loaded bundle."""
    token_counts = {
        'total': 0,
        'files': 0,
        'metadata': 0,
        'by_file': {}
    }

    # Count tokens in files
    for file_key, file_data in result.get('files', {}).items():
        if isinstance(file_data, dict) and 'content' in file_data:
            tokens = estimate_tokens(file_data['content'])
            token_counts['files'] += tokens
            token_counts['by_file'][file_key] = tokens

    # Count tokens in metadata
    metadata = result.get('metadata', {})
    if metadata:
        metadata_str = json.dumps(metadata)
        token_counts['metadata'] = estimate_tokens(metadata_str)

    token_counts['total'] = token_counts['files'] + token_counts['metadata']

    # Calculate percentage of context window
    token_counts['percentage'] = round((token_counts['total'] / CONTEXT_WINDOW) * 100, 2)

    return token_counts


def count_checkboxes(steps_file: Path) -> tuple:
    """
    Count checkboxes in steps.md file.
    Returns: (total, completed, uncompleted)
    """
    if not steps_file.exists():
        return (0, 0, 0)

    try:
        content = steps_file.read_text(encoding='utf-8')

        # Match checkbox patterns: - [ ] or - [x] or - [X]
        checked = len(re.findall(r'^\s*-\s*\[x\]', content, re.MULTILINE | re.IGNORECASE))
        unchecked = len(re.findall(r'^\s*-\s*\[\s\]', content, re.MULTILINE))

        total = checked + unchecked
        return (total, checked, unchecked)
    except Exception:
        return (0, 0, 0)


def scan_projects(base_path: str = ".", minimal: bool = True) -> List[Dict[str, Any]]:
    """Scan all projects and extract YAML metadata + count actual tasks.
    
    Args:
        base_path: Root path to scan from
        minimal: If True, return only essential fields for routing/display (default)
                 If False, return all YAML fields
    """
    projects = []
    projects_dir = Path(base_path) / "02-projects"

    if not projects_dir.exists():
        return []

    # Look for all overview.md files in root and onboarding folder
    patterns = [
        "*/01-planning/overview.md",
        "00-onboarding/*/01-planning/overview.md"
    ]

    for pattern in patterns:
        for overview_file in projects_dir.glob(pattern):
            metadata = extract_yaml_frontmatter(str(overview_file))
            if metadata and 'error' not in metadata:
                # Count actual checkboxes from steps.md
                project_dir = overview_file.parent.parent
                steps_file = project_dir / "01-planning" / "steps.md"

                total, completed, uncompleted = count_checkboxes(steps_file)

                # OVERRIDE YAML metadata with actual counts from steps.md
                # This ensures single source of truth: steps.md checkboxes
                metadata['tasks_total'] = total
                metadata['tasks_completed'] = completed
                metadata['progress'] = round(completed / total, 3) if total > 0 else 0.0

                # Add current task (first unchecked task)
                if steps_file.exists() and uncompleted > 0:
                    try:
                        content = steps_file.read_text(encoding='utf-8')
                        # Find first unchecked task
                        match = re.search(r'^\s*-\s*\[\s\]\s*(.+)$', content, re.MULTILINE)
                        if match:
                            metadata['current_task'] = match.group(1).strip()
                    except Exception:
                        pass

                # PROGRESSIVE DISCLOSURE: Return minimal fields for efficiency
                if minimal:
                    # Keep only essential fields for routing and menu display
                    description = metadata.get('description', '')
                    
                    metadata = {
                        'id': metadata.get('id'),
                        'name': metadata.get('name'),
                        'description': description,
                        'status': metadata.get('status'),
                        'onboarding': metadata.get('onboarding', False),
                        'created': metadata.get('created'),
                        'updated': metadata.get('updated'),
                        'progress': metadata['progress'],
                        'tasks_total': metadata['tasks_total'],
                        'tasks_completed': metadata['tasks_completed'],
                        'current_task': metadata.get('current_task'),
                        '_file_path': metadata.get('_file_path'),
                        '_file_name': metadata.get('_file_name')
                    }

                projects.append(metadata)

    return projects


def scan_skills(base_path: str = ".", minimal: bool = True) -> List[Dict[str, Any]]:
    """Scan all skills and extract YAML metadata.
    
    Args:
        base_path: Root path to scan from
        minimal: If True, return only essential fields for routing/display (default)
                 If False, return all YAML fields
    """
    skills = []

    # Try both 03-skills/ (user skills) and 00-system/skills/ (system skills)
    skills_dirs = [
        Path(base_path) / "03-skills",
        Path(base_path) / "00-system" / "skills"
    ]

    for skills_dir in skills_dirs:
        if not skills_dir.exists():
            continue

        # Look for all SKILL.md files
        for skill_file in skills_dir.glob("*/SKILL.md"):
            metadata = extract_yaml_frontmatter(str(skill_file))
            if metadata and 'error' not in metadata:
                
                # PROGRESSIVE DISCLOSURE: Return minimal fields for efficiency
                if minimal:
                    description = metadata.get('description', '')
                    
                    metadata = {
                        'name': metadata.get('name'),
                        'description': description,
                        '_file_path': metadata.get('_file_path'),
                        '_file_name': metadata.get('_file_name')
                    }
                
                skills.append(metadata)

    return skills


def load_startup(base_path: str = ".") -> Dict[str, Any]:
    """
    Load startup context and determine complete execution plan.

    This function is the MASTER CONTROLLER for Nexus startup.
    It analyzes system state and returns EXACTLY what the AI should do.

    Returns:
    - system_state: Classification of current state
    - files_to_load: Array of file paths to load via Read tool
    - instructions: Complete execution plan with action, message, steps
    - metadata: All projects and skills
    - stats: System statistics
    """
    base = Path(base_path)

    result = {
        'loaded_at': datetime.now().isoformat(),
        'bundle': 'startup',
        'system_state': None,      # State classification
        'files_to_load': [],       # Files to load via Read tool
        'instructions': None,      # Complete execution plan
        'metadata': {},
        'stats': {}
    }

    # Step 1: ALWAYS load mandatory navigation maps first (if they exist)
    # These provide core system structure and context for every session
    for map_path in MANDATORY_MAPS:
        full_path = base / map_path
        if full_path.exists():
            result['files_to_load'].append(str(full_path))

    # Step 2: Load additional optional context files (if they exist)
    optional_files = {
        'memory_map': base / "01-memory" / "memory-map.md",
        'goals': base / "01-memory" / "goals.md",
        'user_config': base / "01-memory" / "user-config.yaml",
    }

    files_exist = {
        key: path.exists() for key, path in optional_files.items()
    }

    # Add optional files to load list
    for key, path in optional_files.items():
        if files_exist[key]:
            result['files_to_load'].append(str(path))

    # Step 3: Scan project and skill metadata
    projects = scan_projects(base_path)
    result['metadata']['projects'] = projects

    skills = scan_skills(base_path)
    result['metadata']['skills'] = skills

    # Step 4: Intelligent state detection (NO DIRECTIVES!)
    # The script analyzes file existence and project metadata to decide what to do

    # STATE 1: First Time Setup (no goals.md)
    if not files_exist['goals']:
        result['system_state'] = 'first_time_setup'
        result['instructions'] = {
            'action': 'load_and_execute_project',
            'project_id': '00-define-goals',
            'execution_mode': 'immediate',
            'message': 'Welcome to Nexus! Starting onboarding...',
            'reason': 'First time setup - goals.md not initialized',
            'workflow': [
                'Load Project 00: Define Goals',
                'Execute steps.md in sequence',
                'Create goals.md, roadmap.md, and memory system'
            ]
        }

    # STATE 2: Goals exist - check onboarding status
    else:
        # Identify onboarding projects (use semantic metadata, not string patterns)
        onboarding_projects = [p for p in projects if p.get('onboarding') is True]

        # Find first incomplete onboarding project
        incomplete_onboarding = None
        for proj in sorted(onboarding_projects, key=lambda x: x['id']):
            if proj.get('progress', 0) < 1.0:  # Not 100% complete
                incomplete_onboarding = proj
                break

        # STATE 2A: Onboarding in progress
        if incomplete_onboarding:
            result['system_state'] = 'onboarding_in_progress'
            result['instructions'] = {
                'action': 'load_and_execute_project',
                'project_id': incomplete_onboarding['id'],
                'execution_mode': 'immediate',
                'message': f"Continuing onboarding: {incomplete_onboarding['name']}",
                'reason': f"Onboarding project {incomplete_onboarding['id']} not yet complete",
                'workflow': [
                    f"Load project {incomplete_onboarding['id']} planning files",
                    'Resume from first unchecked task',
                    'Continue executing onboarding sequence'
                ]
            }

        # STATE 2B: Onboarding complete - check for active projects
        else:
            active_projects = [p for p in projects if p.get('status') == 'IN_PROGRESS']

            # STATE 2B-i: Has active projects
            if active_projects:
                # Find most recently updated
                most_recent = active_projects[0]  # Assume first is most recent from scan

                result['system_state'] = 'operational_with_active_projects'
                result['instructions'] = {
                    'action': 'display_menu',
                    'execution_mode': 'interactive',
                    'message': f"Welcome back! You have {len(active_projects)} active project(s)",
                    'reason': f'Active projects detected: {most_recent["id"]}',
                    'workflow': [
                        'Display Nexus banner',
                        'Show user goals (from goals.md)',
                        f'Highlight {len(active_projects)} active projects',
                        'Show available skills',
                        'Wait for user input (can resume projects or start new work)'
                    ]
                }

            # STATE 2B-ii: No active projects (normal operational state)
            else:
                result['system_state'] = 'operational'
                result['instructions'] = {
                    'action': 'display_menu',
                    'execution_mode': 'interactive',
                    'message': 'System ready - what would you like to work on?',
                    'reason': 'Onboarding complete, no active projects',
                    'workflow': [
                        'Display Nexus banner',
                        'Show user goals (from goals.md)',
                        'List completed projects',
                        'Show available skills',
                        'Suggest: "create project" or use skills',
                        'Wait for user input'
                    ]
                }

    # Step 5: Generate stats
    # Count how many mandatory maps exist
    mandatory_maps_found = sum(1 for map_path in MANDATORY_MAPS if (base / map_path).exists())

    result['stats'] = {
        'files_found': len(result['files_to_load']),
        'mandatory_maps_loaded': mandatory_maps_found,
        'mandatory_maps_total': len(MANDATORY_MAPS),
        'total_projects': len(projects),
        'total_skills': len(skills),
        'active_projects': len([p for p in projects if p.get('status') == 'IN_PROGRESS']),
    }

    return result


def load_project(project_id: str, base_path: str = ".") -> Dict[str, Any]:
    """Load complete project context (all planning files)."""
    base = Path(base_path)
    project_path = None

    # Find project by ID
    search_dirs = [
        base / "02-projects",
        base / "02-projects" / "00-onboarding"
    ]
    
    for search_dir in search_dirs:
        if not search_dir.exists(): continue
        for proj_dir in search_dir.glob("*"):
            if proj_dir.is_dir() and proj_dir.name.startswith(project_id):
                project_path = proj_dir
                break
        if project_path: break

    if not project_path:
        return {'error': f'Project not found: {project_id}'}

    result = {
        'loaded_at': datetime.now().isoformat(),
        'bundle': 'project',
        'project_id': project_id,
        'project_path': str(project_path),
        'files': {}
    }

    # Load all planning files
    planning_files = [
        '01-planning/overview.md',
        '01-planning/requirements.md',
        '01-planning/design.md',
        '01-planning/steps.md'
    ]

    for file_rel in planning_files:
        file_path = project_path / file_rel
        if file_path.exists():
            # Extract YAML metadata
            metadata = extract_yaml_frontmatter(str(file_path))

            # Load content only for line counting (not returned to avoid truncation)

            result['files'][file_rel] = {
                'path': str(file_path),
                'metadata': metadata
                # NO 'content' field - use Read tool for complete content
            }

    # List outputs directory
    outputs_path = project_path / "03-outputs"
    if outputs_path.exists():
        result['outputs'] = [str(f.relative_to(outputs_path)) for f in outputs_path.rglob("*") if f.is_file()]

    return result


def load_skill(skill_name: str, base_path: str = ".") -> Dict[str, Any]:
    """Load complete skill context."""
    base = Path(base_path)

    # Try both 03-skills/ (user skills) and 00-system/skills/ (system skills)
    skill_path = base / "03-skills" / skill_name
    if not skill_path.exists():
        skill_path = base / "00-system" / "skills" / skill_name

    if not skill_path.exists():
        return {'error': f'Skill not found: {skill_name}'}

    result = {
        'loaded_at': datetime.now().isoformat(),
        'bundle': 'skill',
        'skill_name': skill_name,
        'skill_path': str(skill_path),
        'files': {},
        'references_loaded': [],
        'scripts_loaded': [],
        'assets_available': []
    }

    # Load SKILL.md
    skill_file = skill_path / "SKILL.md"
    if skill_file.exists():
        metadata = extract_yaml_frontmatter(str(skill_file))

        result['files']['SKILL.md'] = {
            'path': str(skill_file),
            'metadata': metadata
        }

        # AUTO-LOAD references declared in YAML
        if metadata and 'load_references' in metadata:
            references_path = skill_path / "references"
            if references_path.exists():
                for ref_file in metadata['load_references']:
                    ref_path = references_path / ref_file
                    if ref_path.exists():
                        result['files'][f'references/{ref_file}'] = {
                            'path': str(ref_path),
                        }
                        result['references_loaded'].append(ref_file)

        # AUTO-LOAD scripts declared in YAML
        if metadata and 'load_scripts' in metadata:
            scripts_path = skill_path / "scripts"
            if scripts_path.exists():
                for script_file in metadata['load_scripts']:
                    script_path = scripts_path / script_file
                    if script_path.exists():
                        result['files'][f'scripts/{script_file}'] = {
                            'path': str(script_path),
                        }
                        result['scripts_loaded'].append(script_file)

    # List remaining references (not auto-loaded)
    references_path = skill_path / "references"
    if references_path.exists():
        all_refs = [f.name for f in references_path.glob("*") if f.is_file()]
        result['references_available'] = [r for r in all_refs if r not in result['references_loaded']]

    # List remaining scripts (not auto-loaded)
    scripts_path = skill_path / "scripts"
    if scripts_path.exists():
        all_scripts = [f.name for f in scripts_path.glob("*") if f.is_file()]
        result['scripts_available'] = [s for s in all_scripts if s not in result['scripts_loaded']]

    # List assets (never auto-loaded)
    assets_path = skill_path / "assets"
    if assets_path.exists():
        result['assets_available'] = [f.name for f in assets_path.glob("*") if f.is_file()]

    return result


# NOTE: All directive parsing/validation functions removed!
# The system now uses intelligent state detection based on file existence
# and project metadata. No directives needed!


def main():
    # Configure UTF-8 output for Windows console
    if sys.stdout.encoding != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')

    # DYNAMIC BASE PATH DETECTION
    # Script lives in: {nexus-root}/00-system/core/nexus-loader.py
    # So nexus-root is 2 levels up from script location
    script_path = Path(__file__).resolve()  # Absolute path to this script
    detected_nexus_root = script_path.parent.parent.parent  # Go up 2 levels: core -> 00-system -> nexus-root

    parser = argparse.ArgumentParser(description="Nexus-v3 Context Loader")
    parser.add_argument('--startup', action='store_true', help='Load startup context with intelligent state detection')
    parser.add_argument('--project', help='Load project by ID')
    parser.add_argument('--skill', help='Load skill by name')
    parser.add_argument('--list-projects', action='store_true', help='List all projects')
    parser.add_argument('--list-skills', action='store_true', help='List all skills')
    parser.add_argument('--full', action='store_true', help='Return complete metadata (default: minimal fields for efficiency)')
    parser.add_argument('--base-path', default=str(detected_nexus_root), help=f'Base path to Nexus-v3 (default: auto-detected from script location)')
    parser.add_argument('--show-tokens', action='store_true', help='Include token cost analysis')

    args = parser.parse_args()

    # Execute command
    if args.startup:
        result = load_startup(args.base_path)
    elif args.project:
        result = load_project(args.project, args.base_path)
    elif args.skill:
        result = load_skill(args.skill, args.base_path)
    elif args.list_projects:
        projects = scan_projects(args.base_path, minimal=not args.full)
        result = {'projects': projects}
    elif args.list_skills:
        skills = scan_skills(args.base_path, minimal=not args.full)
        result = {'skills': skills}
    else:
        parser.print_help()
        return

    # Add token analysis if requested
    if args.show_tokens:
        token_stats = calculate_bundle_tokens(result)
        result['token_cost'] = token_stats

        # Warn if metadata budget exceeded
        if token_stats.get('metadata', 0) > METADATA_BUDGET_WARNING:
            result['warnings'] = result.get('warnings', [])
            result['warnings'].append(
                f"Metadata tokens ({token_stats['metadata']}) exceeds recommended budget ({METADATA_BUDGET_WARNING})"
            )

    # Output JSON (always pretty-printed for human readability)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
