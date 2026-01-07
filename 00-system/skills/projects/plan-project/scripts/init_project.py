#!/usr/bin/env python3
"""
Project Initializer - Creates a new Nexus project from template

Usage:
    init_project.py <project-name> --path <path>

Examples:
    init_project.py website-redesign --path Projects
    init_project.py client-portal --path Projects
    init_project.py "Marketing Campaign" --path Projects

The script will:
1. Auto-assign the next available project ID
2. Create the project directory structure
3. Generate all planning files from templates
4. Create the outputs directory
"""

import sys
from pathlib import Path
import re
from datetime import datetime

script_dir = Path(__file__).parent

# Template for 01-overview.md
OVERVIEW_TEMPLATE = """---
id: {project_id}-{sanitized_name}
name: {project_name}
status: PLANNING
description: "{description}"
created: {date}
project_path: 02-projects/{project_id}-{sanitized_name}/
---

# {project_name}

## Project Files

| File | Purpose |
|------|---------|
| 01-overview.md | This file - purpose, success criteria |
| 02-discovery.md | Dependencies, patterns, risks |
| 03-plan.md | Approach, decisions |
| 04-steps.md | Execution tasks |
| 02-resources/ | Reference materials |
| 03-working/ | Work in progress |
| 04-outputs/ | Final deliverables |

---

## Purpose

{description}

---

## Success Criteria

**Must achieve**:
- [ ] [Measurable outcome 1]
- [ ] [Measurable outcome 2]

**Nice to have**:
- [ ] [Optional outcome]

---

## Context

**Background**: [What's the current situation?]

**Stakeholders**: [Who cares about this?]

**Constraints**: [What limitations exist?]

---

*Next: Fill in 02-discovery.md*
"""

# Template for 02-discovery.md
DISCOVERY_TEMPLATE = """# Discovery

**Time**: 5-15 min max | **Purpose**: Surface dependencies before planning

---

## Context

**Load First**: `01-planning/01-overview.md` - Understand project purpose
**Output To**: `01-planning/03-plan.md` - Dependencies section auto-populated from this file

---

## Dependencies

*Files, systems, APIs this project will touch*

**Files to Modify**:
- [To be filled during discovery - use full paths like `00-system/skills/X/SKILL.md`]

**Files to Create**:
- [To be filled during discovery - specify target paths]

**External Systems**:
- [To be filled during discovery]

---

## Existing Patterns

*Skills, templates, code to reuse*

**Related Skills**:
- [To be filled during discovery - use paths like `00-system/skills/X/SKILL.md`]

**Related Projects**:
- [To be filled during discovery - use paths like `02-projects/XX-name/`]

**Code Patterns**:
- [To be filled during discovery]

---

## Risks & Unknowns

*What could derail? What don't we know?*

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| [To be filled] | | |

**Open Questions**:
- [ ] [To be filled during discovery]

---

*Auto-populate 03-plan.md Dependencies section from findings above*
"""

# Template for 03-plan.md
PLAN_TEMPLATE = """# {project_name} - Plan

**Last Updated**: {date}

---

## Context

**Load Before Reading**:
- `01-planning/01-overview.md` - Purpose and success criteria
- `01-planning/02-discovery.md` - Dependencies discovered

---

## Approach

[How will you tackle this? What's your strategy?]

---

## Key Decisions

[What important choices have you made? Why?]

| Decision | Choice | Why |
|----------|--------|-----|
| [Decision 1] | [Choice] | [Rationale] |

---

## Dependencies & Links

*Auto-populated from 02-discovery.md*

**Files Impacted**:
- [From discovery]

**External Systems**:
- [From discovery]

**Related Projects**:
- [From discovery]

---

## Open Questions

- [ ] [Question that needs answering]

---

*Next: Break down execution in 04-steps.md*
"""

# Template for 04-steps.md
STEPS_TEMPLATE = """# {project_name} - Execution Steps

**Last Updated**: {date}

---

## Context Requirements

**Project Location**: `02-projects/{project_id}-{sanitized_name}/`

**Files to Load for Execution**:
- `01-planning/01-overview.md` - Purpose, success criteria
- `01-planning/02-discovery.md` - Dependencies, patterns, risks
- `01-planning/03-plan.md` - Approach, decisions
- `01-planning/04-steps.md` - This file (execution tasks)
- `01-planning/resume-context.md` - Resume state

**Output Locations**:
- `03-working/` - Work in progress files
- `04-outputs/` - Final deliverables

---

## Phase 1: Planning

- [ ] Complete 01-overview.md
- [ ] Complete 02-discovery.md
- [ ] Complete 03-plan.md
- [ ] Complete 04-steps.md
- [ ] Review with stakeholder

---

## Phase 2: [Name this phase]

- [ ] [Step 1]
- [ ] [Step 2]
- [ ] [Step 3]

---

## Phase 3: [Name this phase]

- [ ] [Step 1]
- [ ] [Step 2]

---

## Phase 4: Testing & Launch

- [ ] Test with sample data
- [ ] Gather feedback and iterate
- [ ] Full deployment
- [ ] Document and hand off

---

## Notes

**Current blockers**: [What's preventing progress?]

**Dependencies**: [What are you waiting on?]

---

*Mark tasks complete with [x] as you finish them*
"""


def sanitize_project_name(name):
    """
    Sanitize project name to be filesystem-safe.
    Converts to lowercase, replaces spaces with hyphens, removes special chars.
    """
    name = name.lower().replace(' ', '-')
    name = re.sub(r'[^a-z0-9-]', '', name)
    name = re.sub(r'-+', '-', name)
    name = name.strip('-')
    return name


def load_type_template(project_type, template_name):
    """
    Load type-specific template from templates/types/{type}/ directory.

    Args:
        project_type: One of the 8 project types (build, integration, etc.)
        template_name: Name of template file (overview.md, discovery.md, plan.md, steps.md)

    Returns:
        Template content as string, or None if not found
    """
    templates_dir = script_dir.parent / "templates" / "types" / project_type
    template_file = templates_dir / template_name

    if not template_file.exists():
        return None

    try:
        return template_file.read_text(encoding='utf-8')
    except Exception as e:
        print(f"[WARNING] Error reading template {template_name}: {e}")
        return None


def get_type_config(project_type):
    """
    Load _type.yaml configuration for a project type.

    Returns:
        Dict with type configuration or empty dict if not found
    """
    type_yaml = script_dir.parent / "templates" / "types" / project_type / "_type.yaml"

    if not type_yaml.exists():
        return {}

    try:
        # Simple YAML parsing without external dependency
        content = type_yaml.read_text(encoding='utf-8')
        config = {}
        for line in content.split('\n'):
            if ':' in line and not line.strip().startswith('#'):
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip().strip('"').strip("'")
                if value:
                    config[key] = value
        return config
    except Exception as e:
        print(f"[WARNING] Error reading _type.yaml for {project_type}: {e}")
        return {}


def get_next_project_id(projects_path):
    """
    Scan the projects directory to determine the next available project ID.
    """
    projects_dir = Path(projects_path).resolve()

    if not projects_dir.exists():
        return "01"

    existing_ids = []
    for item in projects_dir.iterdir():
        if item.is_dir():
            match = re.match(r'^(\d{2})-', item.name)
            if match:
                existing_ids.append(int(match.group(1)))

    if not existing_ids:
        return "01"

    next_id = max(existing_ids) + 1
    return f"{next_id:02d}"


def init_project(project_name, path, project_type='generic', description='', project_id_override=None):
    """
    Initialize a new project directory with all planning files from templates.

    Args:
        project_name: Human-readable project name
        path: Path to projects directory (e.g., 02-projects)
        project_type: One of build, integration, research, strategy, content, process, skill, generic
        description: Project description for overview
        project_id_override: Optional project ID (auto-assigned if not provided)
    """
    sanitized_name = sanitize_project_name(project_name)

    if not sanitized_name:
        print("[ERROR] Invalid project name. Must contain at least one alphanumeric character.")
        return None

    if project_id_override:
        project_id = f"{int(project_id_override):02d}"
    else:
        project_id = get_next_project_id(path)

    project_dirname = f"{project_id}-{sanitized_name}"
    project_dir = Path(path).resolve() / project_dirname

    if project_dir.exists():
        print(f"[ERROR] Project directory already exists: {project_dir}")
        return None

    # Default description if not provided
    if not description:
        description = f"Project: {project_name}"

    # Create project directory structure
    try:
        project_dir.mkdir(parents=True, exist_ok=False)
        print(f"[OK] Created project directory: {project_dir}")
    except Exception as e:
        print(f"[ERROR] Error creating directory: {e}")
        return None

    # Create subdirectories
    for subdir in ["01-planning", "02-resources", "03-working", "04-outputs"]:
        try:
            (project_dir / subdir).mkdir(exist_ok=False)
            print(f"[OK] Created {subdir}/ directory")
        except Exception as e:
            print(f"[ERROR] Error creating {subdir} directory: {e}")
            return None

    planning_dir = project_dir / "01-planning"
    current_date = datetime.now().strftime("%Y-%m-%d")
    timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")

    # Create 01-overview.md
    try:
        overview_content = OVERVIEW_TEMPLATE.format(
            project_name=project_name,
            project_id=project_id,
            sanitized_name=sanitized_name,
            date=current_date,
            description=description
        )
        (planning_dir / "01-overview.md").write_text(overview_content, encoding='utf-8')
        print("[OK] Created 01-overview.md")
    except Exception as e:
        print(f"[ERROR] Error creating 01-overview.md: {e}")
        return None

    # Create 02-discovery.md (prefer type-specific template)
    try:
        discovery_content = load_type_template(project_type, "discovery.md")
        if not discovery_content:
            # Fall back to generic template
            discovery_template_path = script_dir / "templates" / "discovery-template.md"
            if discovery_template_path.exists():
                discovery_content = discovery_template_path.read_text(encoding='utf-8')
            else:
                discovery_content = DISCOVERY_TEMPLATE
        (planning_dir / "02-discovery.md").write_text(discovery_content, encoding='utf-8')
        print(f"[OK] Created 02-discovery.md (type: {project_type})")
    except Exception as e:
        print(f"[ERROR] Error creating 02-discovery.md: {e}")
        return None

    # Create 03-plan.md (prefer type-specific template)
    try:
        plan_content = load_type_template(project_type, "plan.md")
        if not plan_content:
            # Fall back to generic template
            plan_content = PLAN_TEMPLATE.format(
                project_name=project_name,
                date=current_date
            )
        (planning_dir / "03-plan.md").write_text(plan_content, encoding='utf-8')
        print(f"[OK] Created 03-plan.md (type: {project_type})")
    except Exception as e:
        print(f"[ERROR] Error creating 03-plan.md: {e}")
        return None

    # Create 04-steps.md (prefer type-specific template)
    try:
        steps_content = load_type_template(project_type, "steps.md")
        if not steps_content:
            # Fall back to generic template
            steps_content = STEPS_TEMPLATE.format(
                project_name=project_name,
                project_id=project_id,
                sanitized_name=sanitized_name,
                date=current_date
            )
        (planning_dir / "04-steps.md").write_text(steps_content, encoding='utf-8')
        print(f"[OK] Created 04-steps.md (type: {project_type})")
    except Exception as e:
        print(f"[ERROR] Error creating 04-steps.md: {e}")
        return None

    # Create resume-context.md
    try:
        resume_content = f"""---
session_id: ""
session_ids: []
resume_schema_version: "2.0"
last_updated: "{timestamp}"

# PROJECT
project_id: "{project_id}-{sanitized_name}"
project_name: "{project_name}"
project_type: "{project_type}"
current_phase: "planning"

# LOADING - Updated dynamically
next_action: "plan-project"
files_to_load:
  - "01-planning/01-overview.md"
  - "01-planning/02-discovery.md"
  - "01-planning/03-plan.md"
  - "01-planning/04-steps.md"

# SKILL TRACKING (v2.3 simplified - optional)
# current_skill: ""

# DISCOVERY STATE
rediscovery_round: 0
discovery_complete: false

# PROGRESS
current_section: 1
current_task: 1
total_tasks: 0
tasks_completed: 0
---

## Progress Summary

**Project Type**: {project_type}
**Phase**: Planning

---

*Auto-updated by execute-project skill on task/section completion*
"""
        (planning_dir / "resume-context.md").write_text(resume_content, encoding='utf-8')
        print("[OK] Created resume-context.md")
    except Exception as e:
        print(f"[ERROR] Error creating resume-context.md: {e}")
        return None

    # Print success message
    print(f"\n[SUCCESS] Project '{project_name}' initialized successfully!")
    print(f"   Project ID: {project_id}")
    print(f"   Location: {project_dir}")
    print("\nProject structure created:")
    print(f"  {project_dirname}/")
    print("    01-planning/")
    print("      01-overview.md     (purpose, goals, success criteria)")
    print("      02-discovery.md    (dependencies, patterns, risks)")
    print("      03-plan.md         (approach, decisions)")
    print("      04-steps.md        (execution checklist)")
    print("      resume-context.md  (session resume state)")
    print("    02-resources/  (reference materials)")
    print("    03-working/    (work-in-progress files)")
    print("    04-outputs/    (final deliverables)")
    print("\nPlanning workflow:")
    print("1. 01-overview.md  - Define purpose and success criteria")
    print("2. 02-discovery.md - Scan for dependencies, patterns, risks")
    print("3. 03-plan.md      - Define approach (Dependencies from discovery)")
    print("4. 04-steps.md     - Break down execution phases")

    return project_dir


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Initialize a new Nexus project with templates",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  init_project.py "Website Redesign" --path 02-projects --type build
  init_project.py "Market Research" --path 02-projects --type research
  init_project.py my-feature --path 02-projects -d "Add new feature" --id 15

Project structure created:
  02-projects/
    NN-project-name/
      01-planning/
        01-overview.md   (purpose, goals)
        02-discovery.md  (dependencies, patterns, risks)
        03-plan.md       (approach, decisions)
        04-steps.md      (execution checklist)
        resume-context.md
      02-resources/
      03-working/
      04-outputs/
"""
    )

    parser.add_argument("name", help="Project name (spaces or hyphens)")
    parser.add_argument("--path", "-p", default="02-projects",
                        help="Path to projects directory (default: 02-projects)")
    parser.add_argument("--type", "-t", default="generic",
                        choices=["build", "integration", "research", "strategy", "content", "process", "skill", "generic"],
                        help="Project type for template selection (default: generic)")
    parser.add_argument("--description", "-d", default="",
                        help="Project description")
    parser.add_argument("--id", type=int, default=None,
                        help="Override auto-assigned project ID")

    args = parser.parse_args()

    print(f"Initializing project: {args.name}")
    print(f"Location: {args.path}")
    print(f"Type: {args.type}")
    if args.description:
        print(f"Description: {args.description}")
    if args.id:
        print(f"ID Override: {args.id:02d}")
    print()

    result = init_project(
        project_name=args.name,
        path=args.path,
        project_type=args.type,
        description=args.description,
        project_id_override=args.id
    )

    if result:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
