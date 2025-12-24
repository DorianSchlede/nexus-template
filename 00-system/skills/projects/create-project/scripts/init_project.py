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


# Template for overview.md
OVERVIEW_TEMPLATE = """---
id: {project_id}-{sanitized_name}
name: {project_name}
status: PLANNING
description: "[TODO: Load when user mentions X, Y, or Z]"
created: {date}
---

# {project_name}

## Purpose

[What problem does this solve? What value does it create?]

Example: "Reduce lead qualification time from 30 min to 2 min while maintaining 90% accuracy"

---

## Success Criteria

[How will you know this succeeded?]

**Must achieve**:
- [ ] [Measurable outcome 1]
- [ ] [Measurable outcome 2]

Example:
- [ ] Process 50+ leads/day with <2 min avg time
- [ ] Achieve 90%+ accuracy vs manual qualification

**Nice to have**:
- [ ] [Optional outcome]

---

## Context

**Background**: [What's the current situation?]

**Stakeholders**: [Who cares about this?]

**Constraints**: [What limitations exist?]

Example: "Sales team manually qualifies leads using 10-question form. Takes 30 min/lead. Need automation that integrates with existing Airtable CRM."

---

## Timeline

**Target**: [When should this be done?]

**Milestones**:
- [Milestone 1] - [Date]
- [Milestone 2] - [Date]

Example:
- MVP ready - 2 weeks
- Full deployment - 4 weeks

---

*Next: Complete plan.md to define your approach*
"""

# Template for plan.md
PLAN_TEMPLATE = """# {project_name} - Plan

**Last Updated**: {date}

---

## Approach

[How will you tackle this? What's your strategy?]

Example: "Build AI-powered qualification workflow: Airtable form -> GPT-4 analysis -> Slack notification to sales team"

---

## Key Decisions

[What important choices have you made? Why?]

Example:
- **Use GPT-4 vs rule-based**: GPT-4 handles nuance better, worth the API cost
- **Slack vs email**: Sales team lives in Slack, faster response time

---

## Resources Needed

[What do you need to execute this?]

**Tools/Access**:
- [Tool 1]
- [Tool 2]

**People/Expertise**:
- [Who you need]

**Information/Data**:
- [What you need to know]

Example:
- Airtable API access
- GPT-4 API key
- Sales team input on qualification criteria

---

## Dependencies & Links

**Files Impacted**:
- `path/to/file.py` - [What changes]

**External Systems**:
- [System name]: [Link] - [How it's used]

**Related Projects**:
- Project NN: [Name] - [Relationship]

**Skills/Workflows**:
- [Skill name] - [How it's invoked]

Example:
- `03-skills/lead-qualification/SKILL.md` - Main workflow definition
- Airtable Base: "Leads" - Source of lead data
- Project 03: CRM Integration - Shares Airtable connection

---

## Open Questions

- [ ] [Question that needs answering]
- [ ] [Decision that needs making]

Example:
- [ ] What's the fallback if AI confidence is <80%?
- [ ] Should we notify sales for ALL leads or just qualified ones?

---

## Mental Models Applied

[Which thinking frameworks did you use during planning?]

**Socratic Questioning**:
- What assumptions are you making?
- What evidence supports this approach?

**Devil's Advocate**:
- What could go wrong with this plan?
- What am I not considering?

Example:
- Assumption: Sales team will trust AI qualification -> Need to validate with pilot
- Risk: API costs could spike with high volume -> Add cost monitoring

---

*Next: Complete steps.md to break down execution*
"""

# Template for steps.md
STEPS_TEMPLATE = """# {project_name} - Execution Steps

**Last Updated**: {date}

**IMPORTANT**: This file tracks project progress. Mark tasks complete with [x] as you finish them.

---

## Phase 1: Setup & Planning

- [ ] Complete overview.md
- [ ] Complete plan.md
- [ ] Complete steps.md
- [ ] Review with stakeholders

---

## Phase 2: [Name this phase]

[Break down the work into concrete, actionable steps]

- [ ] [Step 1]
- [ ] [Step 2]
- [ ] [Step 3]

Example for "Build Lead Qualification":
- [ ] Set up Airtable webhook
- [ ] Create GPT-4 prompt template
- [ ] Build Slack notification function

---

## Phase 3: [Name this phase]

- [ ] [Step 1]
- [ ] [Step 2]

---

## Phase 4: Testing & Launch

- [ ] Test with sample data
- [ ] Pilot with small group
- [ ] Gather feedback and iterate
- [ ] Full deployment
- [ ] Document and hand off

---

## Notes

**Current blockers**: [What's preventing progress?]

**Dependencies**: [What are you waiting on?]

Example:
- Blocker: Waiting for Airtable API access
- Dependency: Sales team needs to finalize qualification criteria

---

*Mark tasks complete with [x] as you finish them*
"""


def sanitize_project_name(name):
    """
    Sanitize project name to be filesystem-safe.
    Converts to lowercase, replaces spaces with hyphens, removes special chars.
    """
    # Convert to lowercase and replace spaces with hyphens
    name = name.lower().replace(' ', '-')
    # Remove any characters that aren't alphanumeric or hyphens
    name = re.sub(r'[^a-z0-9-]', '', name)
    # Remove multiple consecutive hyphens
    name = re.sub(r'-+', '-', name)
    # Remove leading/trailing hyphens
    name = name.strip('-')
    return name


def load_type_template(project_type):
    """
    Load type-specific template sections from templates/ directory.

    Args:
        project_type: Type of project (build, research, strategy, content, process, generic)

    Returns:
        Template content as string, or empty string if template not found
    """
    script_dir = Path(__file__).parent
    templates_dir = script_dir / "templates"
    template_file = templates_dir / f"template-{project_type}.md"

    if not template_file.exists():
        print(f"[WARNING] Template not found for type '{project_type}', using minimal")
        return ""

    try:
        return template_file.read_text(encoding='utf-8')
    except Exception as e:
        print(f"[WARNING] Error reading template: {e}")
        return ""


def get_next_project_id(projects_path):
    """
    Scan the projects directory to determine the next available project ID.

    Args:
        projects_path: Path to the Projects directory

    Returns:
        Next available ID as a zero-padded string (e.g., "01", "02", "10")
    """
    projects_dir = Path(projects_path).resolve()

    # If Projects directory doesn't exist, start at 01
    if not projects_dir.exists():
        return "01"

    # Find all directories that match the pattern: NN-name
    existing_ids = []
    for item in projects_dir.iterdir():
        if item.is_dir():
            match = re.match(r'^(\d{2})-', item.name)
            if match:
                existing_ids.append(int(match.group(1)))

    # If no projects exist, start at 01
    if not existing_ids:
        return "01"

    # Return next ID after the highest existing one
    next_id = max(existing_ids) + 1
    return f"{next_id:02d}"


def init_project(project_name, path, project_type='generic'):
    """
    Initialize a new project directory with all planning files from templates.

    Args:
        project_name: Name of the project (will be sanitized)
        path: Path to the Projects directory
        project_type: Type of project (build, research, strategy, content, process, generic)

    Returns:
        Path to created project directory, or None if error
    """
    # Sanitize project name
    sanitized_name = sanitize_project_name(project_name)

    if not sanitized_name:
        print("[ERROR] Invalid project name. Must contain at least one alphanumeric character.")
        return None

    # Get next project ID
    project_id = get_next_project_id(path)

    # Create full project directory name: ID-name
    project_dirname = f"{project_id}-{sanitized_name}"
    project_dir = Path(path).resolve() / project_dirname

    # Check if directory already exists
    if project_dir.exists():
        print(f"[ERROR] Project directory already exists: {project_dir}")
        return None

    # Create project directory structure
    try:
        project_dir.mkdir(parents=True, exist_ok=False)
        print(f"[OK] Created project directory: {project_dir}")
    except Exception as e:
        print(f"[ERROR] Error creating directory: {e}")
        return None

    # Create 01-planning/ directory
    planning_dir = project_dir / "01-planning"
    try:
        planning_dir.mkdir(exist_ok=False)
        print("[OK] Created 01-planning/ directory")
    except Exception as e:
        print(f"[ERROR] Error creating 01-planning directory: {e}")
        return None

    # Create 02-resources/ directory
    resources_dir = project_dir / "02-resources"
    try:
        resources_dir.mkdir(exist_ok=False)
        print("[OK] Created 02-resources/ directory")
    except Exception as e:
        print(f"[ERROR] Error creating 02-resources directory: {e}")
        return None

    # Create 03-working/ directory
    working_dir = project_dir / "03-working"
    try:
        working_dir.mkdir(exist_ok=False)
        print("[OK] Created 03-working/ directory")
    except Exception as e:
        print(f"[ERROR] Error creating 03-working directory: {e}")
        return None

    # Create 04-outputs/ directory
    outputs_dir = project_dir / "04-outputs"
    try:
        outputs_dir.mkdir(exist_ok=False)
        print("[OK] Created 04-outputs/ directory")
    except Exception as e:
        print(f"[ERROR] Error creating 04-outputs directory: {e}")
        return None

    # Get current date for templates
    current_date = datetime.now().strftime("%Y-%m-%d")

    # Create overview.md from template
    try:
        overview_content = OVERVIEW_TEMPLATE.format(
            project_name=project_name,
            project_id=project_id,
            sanitized_name=sanitized_name,
            date=current_date
        )
        overview_path = planning_dir / "overview.md"
        overview_path.write_text(overview_content)
        print("[OK] Created planning/overview.md")
    except Exception as e:
        print(f"[ERROR] Error creating overview.md: {e}")
        return None

    # Create plan.md from template with type-specific sections
    try:
        # Load type-specific template sections
        type_sections = load_type_template(project_type)

        # Create base plan content
        plan_content = PLAN_TEMPLATE.format(
            project_name=project_name,
            date=current_date
        )

        # Inject type-specific sections before "## Mental Models Applied"
        if type_sections:
            insertion_marker = "## Mental Models Applied"
            plan_content = plan_content.replace(
                insertion_marker,
                type_sections + "\n" + insertion_marker
            )

        plan_path = planning_dir / "plan.md"
        plan_path.write_text(plan_content)
        print(f"[OK] Created planning/plan.md (type: {project_type})")
    except Exception as e:
        print(f"[ERROR] Error creating plan.md: {e}")
        return None

    # Create steps.md from template
    try:
        steps_content = STEPS_TEMPLATE.format(
            project_name=project_name,
            date=current_date
        )
        steps_path = planning_dir / "steps.md"
        steps_path.write_text(steps_content)
        print("[OK] Created planning/steps.md")
    except Exception as e:
        print(f"[ERROR] Error creating steps.md: {e}")
        return None

    # Print success message and next steps
    print(f"\n[SUCCESS] Project '{project_name}' initialized successfully!")
    print(f"   Project ID: {project_id}")
    print(f"   Location: {project_dir}")
    print("\nProject structure created:")
    print(f"  {project_dirname}/")
    print("    01-planning/")
    print("      overview.md  (purpose, goals, success criteria)")
    print("      plan.md      (approach, decisions, dependencies)")
    print("      steps.md     (execution checklist)")
    print("    02-resources/  (reference materials)")
    print("    03-working/    (work-in-progress files)")
    print("    04-outputs/    (final deliverables)")
    print("\nNext steps:")
    print("1. Fill in overview.md with project purpose and goals")
    print("2. Define your approach and dependencies in plan.md")
    print("3. Break down work into phases in steps.md")
    print("4. Start executing! Mark steps complete as you go")

    return project_dir


def main():
    if len(sys.argv) < 4 or sys.argv[2] != '--path':
        print("Usage: init_project.py <project-name> --path <path> [--type <type>]")
        print("\nProject name:")
        print("  - Can include spaces (will be converted to hyphens)")
        print("  - Will be sanitized to lowercase with hyphens")
        print("  - Project ID is auto-assigned (next available number)")
        print("\nPath:")
        print("  - Should point to your 02-projects/ directory")
        print("  - Will be created if it doesn't exist")
        print("\nType (optional):")
        print("  - build: Build/Create projects (software, products, tools)")
        print("  - research: Research/Analysis projects")
        print("  - strategy: Strategy/Planning projects")
        print("  - content: Content/Creative projects")
        print("  - process: Process/Operations projects")
        print("  - generic: Generic/Flexible projects (default)")
        print("\nExamples:")
        print('  init_project.py "Website Redesign" --path 02-projects --type build')
        print('  init_project.py "Market Research" --path 02-projects --type research')
        print('  init_project.py "Q1 Strategy" --path 02-projects --type strategy')
        print("\nProject structure created:")
        print("  02-projects/")
        print("    NN-project-name/        (ID auto-assigned)")
        print("      01-planning/")
        print("        overview.md  (purpose, goals, success)")
        print("        plan.md      (approach, decisions, type-specific sections)")
        print("        steps.md     (execution checklist)")
        print("      02-resources/  (reference materials)")
        print("      03-working/    (work-in-progress)")
        print("      04-outputs/    (final deliverables)")
        sys.exit(1)

    project_name = sys.argv[1]
    path = sys.argv[3]

    # Parse optional --type argument
    project_type = 'generic'  # Default
    if len(sys.argv) >= 6 and sys.argv[4] == '--type':
        requested_type = sys.argv[5]
        valid_types = ['build', 'research', 'strategy', 'content', 'process', 'generic']
        if requested_type in valid_types:
            project_type = requested_type
        else:
            print(f"[WARNING] Invalid project type: {requested_type}. Using 'generic' instead.")
            print(f"Valid types: {', '.join(valid_types)}")

    print(f"Initializing project: {project_name}")
    print(f"Location: {path}")
    print(f"Type: {project_type}")
    print()

    result = init_project(project_name, path, project_type)

    if result:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
