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

[TODO: What problem does this project solve? What value does it create?]

**Why this matters**:
- [TODO: Key reason 1]
- [TODO: Key reason 2]
- [TODO: Key reason 3]

---

## Context

[TODO: Background information, constraints, and relevant context]

**Current situation**:
- [TODO: What's the current state?]
- [TODO: What's changing?]

**Stakeholders**:
- [TODO: Who cares about this project?]
- [TODO: Who needs to be involved?]

---

## Success Criteria

[TODO: How will we know this project succeeded?]

**Must achieve**:
- [ ] [TODO: Critical success factor 1]
- [ ] [TODO: Critical success factor 2]
- [ ] [TODO: Critical success factor 3]

**Would be great**:
- [ ] [TODO: Nice-to-have outcome 1]
- [ ] [TODO: Nice-to-have outcome 2]

---

## Timeline

**Target completion**: [TODO: When should this be done?]

**Key milestones**:
- [TODO: Milestone 1] - [Target date]
- [TODO: Milestone 2] - [Target date]
- [TODO: Milestone 3] - [Target date]

---

## Notes

[TODO: Any additional context, links, or information]

---

*Next: Complete requirements.md to define what needs to be built*
"""

# Template for requirements.md
REQUIREMENTS_TEMPLATE = """# {project_name} - Requirements

**Last Updated**: {date}

---

## Functional Requirements

[TODO: What must the solution DO? List specific features and capabilities]

### Core Features

**1. [TODO: Feature name]**
- Description: [What it does]
- User value: [Why it matters]
- Acceptance criteria:
  - [ ] [Specific, testable criterion 1]
  - [ ] [Specific, testable criterion 2]

**2. [TODO: Feature name]**
- Description: [What it does]
- User value: [Why it matters]
- Acceptance criteria:
  - [ ] [Specific, testable criterion 1]
  - [ ] [Specific, testable criterion 2]

**3. [TODO: Feature name]**
- Description: [What it does]
- User value: [Why it matters]
- Acceptance criteria:
  - [ ] [Specific, testable criterion 1]
  - [ ] [Specific, testable criterion 2]

---

## Non-Functional Requirements

[TODO: How should the solution PERFORM? Quality attributes and constraints]

### Performance
- [TODO: Speed, latency, throughput requirements]
- [TODO: Scalability requirements]

### Security
- [TODO: Authentication/authorization needs]
- [TODO: Data protection requirements]

### Usability
- [TODO: User experience requirements]
- [TODO: Accessibility requirements]

### Technical
- [TODO: Technology stack constraints]
- [TODO: Integration requirements]

---

## User Stories

[TODO: Describe what users need to accomplish, in the format: "As a [role], I want [goal] so that [benefit]"]

**Story 1**: As a [role], I want [goal] so that [benefit]
- Acceptance criteria:
  - [ ] [Criterion 1]
  - [ ] [Criterion 2]

**Story 2**: As a [role], I want [goal] so that [benefit]
- Acceptance criteria:
  - [ ] [Criterion 1]
  - [ ] [Criterion 2]

---

## Out of Scope

[TODO: What is explicitly NOT included in this project?]

- [TODO: Out of scope item 1]
- [TODO: Out of scope item 2]
- [TODO: Out of scope item 3]

---

## Dependencies

[TODO: What external factors does this project depend on?]

- [TODO: External system/API/service]
- [TODO: Third-party library/tool]
- [TODO: Other project or team deliverable]

---

## Assumptions

[TODO: What are we assuming is true?]

- [TODO: Assumption 1]
- [TODO: Assumption 2]
- [TODO: Assumption 3]

---

*Next: Complete design.md to plan the solution architecture*
"""

# Template for design.md
DESIGN_TEMPLATE = """# {project_name} - Design

**Last Updated**: {date}

---

## Architecture Overview

[TODO: High-level diagram or description of how the solution is structured]

**Key components**:
1. [TODO: Component 1] - [Purpose]
2. [TODO: Component 2] - [Purpose]
3. [TODO: Component 3] - [Purpose]

**Data flow**:
```
[TODO: Describe how data/information flows through the system]
User -> [Component] -> [Component] -> Output
```

---

## Technical Approach

[TODO: What technologies, frameworks, or methodologies will be used?]

### Technology Stack

**Frontend** (if applicable):
- [TODO: Framework/library]
- [TODO: Key dependencies]

**Backend** (if applicable):
- [TODO: Language/framework]
- [TODO: Database]
- [TODO: APIs/services]

**Infrastructure**:
- [TODO: Hosting/deployment]
- [TODO: CI/CD]

---

## Data Model

[TODO: What data needs to be stored and how is it structured?]

### Entities

**[Entity 1 Name]**:
- Field 1: [Type] - [Description]
- Field 2: [Type] - [Description]
- Relationships: [Connected to what?]

**[Entity 2 Name]**:
- Field 1: [Type] - [Description]
- Field 2: [Type] - [Description]
- Relationships: [Connected to what?]

---

## User Interface Design

[TODO: How will users interact with the solution?]

### Key Screens/Pages

**[Screen 1 Name]**:
- Purpose: [What user accomplishes here]
- Layout: [Brief description or sketch]
- Actions: [What can user do?]

**[Screen 2 Name]**:
- Purpose: [What user accomplishes here]
- Layout: [Brief description or sketch]
- Actions: [What can user do?]

---

## API Design

[TODO: What endpoints or interfaces are exposed?]

### Endpoints

**[Endpoint 1]**: `[HTTP METHOD] /path`
- Purpose: [What it does]
- Request: [Parameters/body]
- Response: [What it returns]

**[Endpoint 2]**: `[HTTP METHOD] /path`
- Purpose: [What it does]
- Request: [Parameters/body]
- Response: [What it returns]

---

## Security Considerations

[TODO: How will the solution be secured?]

- Authentication: [Method/approach]
- Authorization: [Permissions model]
- Data protection: [Encryption, validation]
- Vulnerabilities: [Known risks and mitigations]

---

## Alternatives Considered

[TODO: What other approaches were evaluated?]

**Alternative 1**: [Approach name]
- Pros: [Benefits]
- Cons: [Drawbacks]
- Decision: [Why not chosen]

**Alternative 2**: [Approach name]
- Pros: [Benefits]
- Cons: [Drawbacks]
- Decision: [Why not chosen]

---

## Open Questions

[TODO: What design decisions still need to be made?]

- [ ] [Question 1 that needs answering]
- [ ] [Question 2 that needs answering]
- [ ] [Question 3 that needs answering]

---

*Next: Complete tasks.md to break down the implementation work*
"""

# Template for tasks.md
TASKS_TEMPLATE = """# {project_name} - Tasks

**Last Updated**: {date}

---

## Task Breakdown

[TODO: Break the project into concrete, actionable tasks. Mark with [x] as you complete them]

### Phase 1: Setup & Planning

- [ ] Complete overview.md with project purpose and goals
- [ ] Complete requirements.md with all features and criteria
- [ ] Complete design.md with technical architecture
- [ ] Review all planning docs with stakeholders
- [ ] Set up development environment
- [ ] Create project repository (if applicable)

### Phase 2: Foundation

[TODO: Add foundational tasks - infrastructure, data models, core setup]

- [ ] [TODO: Foundation task 1]
- [ ] [TODO: Foundation task 2]
- [ ] [TODO: Foundation task 3]

### Phase 3: Core Features

[TODO: Add tasks for building the main features]

- [ ] [TODO: Core feature task 1]
- [ ] [TODO: Core feature task 2]
- [ ] [TODO: Core feature task 3]

### Phase 4: Integration

[TODO: Add tasks for connecting components and integrations]

- [ ] [TODO: Integration task 1]
- [ ] [TODO: Integration task 2]
- [ ] [TODO: Integration task 3]

### Phase 5: Testing & Refinement

[TODO: Add tasks for testing, bug fixes, and polish]

- [ ] [TODO: Testing task 1]
- [ ] [TODO: Testing task 2]
- [ ] [TODO: Testing task 3]

### Phase 6: Deployment

[TODO: Add tasks for launching and deploying]

- [ ] [TODO: Deployment task 1]
- [ ] [TODO: Deployment task 2]
- [ ] Final testing in production environment
- [ ] Update documentation
- [ ] Notify stakeholders of completion

---

## Task Management

**How to use this file**:
1. Break down each phase into specific, actionable tasks
2. Mark tasks as complete with `[x]` as you finish them
3. Add new tasks as they're discovered
4. Reorder tasks if priorities change
5. Use `update-tasks` skill to track progress (auto-calculates metrics)

---

## Notes

[TODO: Add any task-specific notes, blockers, or context]

**Current blockers**:
- [TODO: Any blockers preventing progress]

**Dependencies**:
- [TODO: External dependencies affecting tasks]

---

*Use the update-tasks skill during work to mark tasks complete interactively*
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


def init_project(project_name, path):
    """
    Initialize a new project directory with all planning files from templates.

    Args:
        project_name: Name of the project (will be sanitized)
        path: Path to the Projects directory

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

    # Create 03-working-files/ directory
    working_files_dir = project_dir / "03-working-files"
    try:
        working_files_dir.mkdir(exist_ok=False)
        print("[OK] Created 03-working-files/ directory")
    except Exception as e:
        print(f"[ERROR] Error creating 03-working-files directory: {e}")
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

    # Create requirements.md from template
    try:
        requirements_content = REQUIREMENTS_TEMPLATE.format(
            project_name=project_name,
            date=current_date
        )
        requirements_path = planning_dir / "requirements.md"
        requirements_path.write_text(requirements_content)
        print("[OK] Created planning/requirements.md")
    except Exception as e:
        print(f"[ERROR] Error creating requirements.md: {e}")
        return None

    # Create design.md from template
    try:
        design_content = DESIGN_TEMPLATE.format(
            project_name=project_name,
            date=current_date
        )
        design_path = planning_dir / "design.md"
        design_path.write_text(design_content)
        print("[OK] Created planning/design.md")
    except Exception as e:
        print(f"[ERROR] Error creating design.md: {e}")
        return None

    # Create tasks.md from template
    try:
        tasks_content = TASKS_TEMPLATE.format(
            project_name=project_name,
            date=current_date
        )
        tasks_path = planning_dir / "tasks.md"
        tasks_path.write_text(tasks_content)
        print("[OK] Created planning/tasks.md")
    except Exception as e:
        print(f"[ERROR] Error creating tasks.md: {e}")
        return None

    # Print success message and next steps
    print(f"\n[SUCCESS] Project '{project_name}' initialized successfully!")
    print(f"   Project ID: {project_id}")
    print(f"   Location: {project_dir}")
    print("\nProject structure created:")
    print(f"  {project_dirname}/")
    print("    01-planning/")
    print("      overview.md     (project purpose & goals)")
    print("      requirements.md (features & criteria)")
    print("      design.md       (architecture & approach)")
    print("      tasks.md        (actionable task breakdown)")
    print("    02-resources/     (reference materials, links, docs)")
    print("    03-working-files/ (drafts, experiments, temp files)")
    print("    04-outputs/       (final deliverables)")
    print("\nNext steps:")
    print("1. Review and complete the TODO items in 01-planning/overview.md")
    print("2. Define features and acceptance criteria in 01-planning/requirements.md")
    print("3. Design the technical approach in 01-planning/design.md")
    print("4. Break down work into tasks in 01-planning/tasks.md")
    print("5. Start working! Use 'update-tasks' to track progress")

    return project_dir


def main():
    if len(sys.argv) < 4 or sys.argv[2] != '--path':
        print("Usage: init_project.py <project-name> --path <path>")
        print("\nProject name:")
        print("  - Can include spaces (will be converted to hyphens)")
        print("  - Will be sanitized to lowercase with hyphens")
        print("  - Project ID is auto-assigned (next available number)")
        print("\nPath:")
        print("  - Should point to your 02-projects/ directory")
        print("  - Will be created if it doesn't exist")
        print("\nExamples:")
        print('  init_project.py "Website Redesign" --path 02-projects')
        print('  init_project.py client-portal --path 02-projects')
        print('  init_project.py "Marketing Campaign Q1" --path 02-projects')
        print("\nProject structure created:")
        print("  02-projects/")
        print("    NN-project-name/        (ID auto-assigned)")
        print("      01-planning/")
        print("        overview.md")
        print("        requirements.md")
        print("        design.md")
        print("        tasks.md")
        print("      02-resources/     (reference materials)")
        print("      03-working-files/ (drafts, experiments)")
        print("      04-outputs/       (final deliverables)")
        sys.exit(1)

    project_name = sys.argv[1]
    path = sys.argv[3]

    print(f"Initializing project: {project_name}")
    print(f"Location: {path}")
    print()

    result = init_project(project_name, path)

    if result:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
