#!/usr/bin/env python3
"""
Build Initializer - Creates a new Nexus build from template

Usage:
    init_build.py <build-name> --path <path>

Examples:
    init_build.py website-redesign --path Builds
    init_build.py client-portal --path Builds
    init_build.py "Marketing Campaign" --path Builds

The script will:
1. Auto-assign the next available build ID
2. Create the build directory structure
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
id: {build_id}-{sanitized_name}
name: {build_name}
status: PLANNING
description: "{description}"
created: {date}
build_path: 02-builds/active/{build_id}-{sanitized_name}/
---

# {build_name}

## Build Files

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

**Load First**: `01-planning/01-overview.md` - Understand build purpose
**Output To**: `01-planning/03-plan.md` - Dependencies section auto-populated from this file

---

## Dependencies

*Files, systems, APIs this build will touch*

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

**Related Builds**:
- [To be filled during discovery - use paths like `02-builds/XX-name/`]

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
PLAN_TEMPLATE = """# {build_name} - Plan

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

**Related Builds**:
- [From discovery]

---

## Open Questions

- [ ] [Question that needs answering]

---

*Next: Break down execution in 04-steps.md*
"""

# Template for 04-steps.md
STEPS_TEMPLATE = """# {build_name} - Execution Steps

**Last Updated**: {date}

---

## Context Requirements

**Build Location**: `02-builds/active/{build_id}-{sanitized_name}/`

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


def count_checkboxes_in_file(file_path):
    """
    Count checkboxes in a markdown file.

    Returns:
        Tuple of (total, completed)
    """
    try:
        content = file_path.read_text(encoding='utf-8')
        import re
        checked = len(re.findall(r'^\s*-\s*\[x\]', content, re.MULTILINE | re.IGNORECASE))
        unchecked = len(re.findall(r'^\s*-\s*\[\s\]', content, re.MULTILINE))
        return (checked + unchecked, checked)
    except Exception:
        return (0, 0)


def sanitize_build_name(name):
    """
    Sanitize build name to be filesystem-safe.
    Converts to lowercase, replaces spaces with hyphens, removes special chars.
    """
    name = name.lower().replace(' ', '-')
    name = re.sub(r'[^a-z0-9-]', '', name)
    name = re.sub(r'-+', '-', name)
    name = name.strip('-')
    return name


def load_type_template(build_type, template_name):
    """
    Load type-specific template from templates/types/{type}/ directory.

    Args:
        build_type: One of the 8 build types (build, integration, etc.)
        template_name: Name of template file (overview.md, discovery.md, plan.md, steps.md)

    Returns:
        Template content as string, or None if not found
    """
    templates_dir = script_dir.parent / "templates" / "types" / build_type
    template_file = templates_dir / template_name

    if not template_file.exists():
        return None

    try:
        return template_file.read_text(encoding='utf-8')
    except Exception as e:
        print(f"[WARNING] Error reading template {template_name}: {e}")
        return None


def get_type_config(build_type):
    """
    Load _type.yaml configuration for a build type.

    Returns:
        Dict with type configuration or empty dict if not found
    """
    type_yaml = script_dir.parent / "templates" / "types" / build_type / "_type.yaml"

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
        print(f"[WARNING] Error reading _type.yaml for {build_type}: {e}")
        return {}


def get_next_build_id(builds_path):
    """
    Scan the builds directory to determine the next available build ID.
    """
    builds_dir = Path(builds_path).resolve()

    if not builds_dir.exists():
        return "01"

    existing_ids = []
    for item in builds_dir.iterdir():
        if item.is_dir():
            match = re.match(r'^(\d{2})-', item.name)
            if match:
                existing_ids.append(int(match.group(1)))

    if not existing_ids:
        return "01"

    next_id = max(existing_ids) + 1
    return f"{next_id:02d}"


def init_build(build_name, path, build_type='generic', description='', build_id_override=None):
    """
    Initialize a new build directory with all planning files from templates.

    Args:
        build_name: Human-readable build name
        path: Path to builds directory (e.g., 02-builds)
        build_type: One of build, integration, research, strategy, content, process, skill, generic
        description: Build description for overview
        build_id_override: Optional build ID (auto-assigned if not provided)
    """
    sanitized_name = sanitize_build_name(build_name)

    if not sanitized_name:
        print("[ERROR] Invalid build name. Must contain at least one alphanumeric character.")
        return None

    if build_id_override:
        build_id = f"{int(build_id_override):02d}"
    else:
        build_id = get_next_build_id(path)

    build_dirname = f"{build_id}-{sanitized_name}"
    build_dir = Path(path).resolve() / build_dirname

    if build_dir.exists():
        print(f"[ERROR] Build directory already exists: {build_dir}")
        return None

    # Default description if not provided
    if not description:
        description = f"Build: {build_name}"

    # Create build directory structure
    try:
        build_dir.mkdir(parents=True, exist_ok=False)
        print(f"[OK] Created build directory: {build_dir}")
    except Exception as e:
        print(f"[ERROR] Error creating directory: {e}")
        return None

    # Create subdirectories
    for subdir in ["01-planning", "02-resources", "03-working", "04-outputs"]:
        try:
            (build_dir / subdir).mkdir(exist_ok=False)
            print(f"[OK] Created {subdir}/ directory")
        except Exception as e:
            print(f"[ERROR] Error creating {subdir} directory: {e}")
            return None

    planning_dir = build_dir / "01-planning"
    current_date = datetime.now().strftime("%Y-%m-%d")
    timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")

    # Create 01-overview.md
    try:
        overview_content = OVERVIEW_TEMPLATE.format(
            build_name=build_name,
            build_id=build_id,
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
        discovery_content = load_type_template(build_type, "discovery.md")
        if not discovery_content:
            # Fall back to generic template
            discovery_template_path = script_dir / "templates" / "discovery-template.md"
            if discovery_template_path.exists():
                discovery_content = discovery_template_path.read_text(encoding='utf-8')
            else:
                discovery_content = DISCOVERY_TEMPLATE
        (planning_dir / "02-discovery.md").write_text(discovery_content, encoding='utf-8')
        print(f"[OK] Created 02-discovery.md (type: {build_type})")
    except Exception as e:
        print(f"[ERROR] Error creating 02-discovery.md: {e}")
        return None

    # Create 03-plan.md (prefer type-specific template)
    try:
        plan_content = load_type_template(build_type, "plan.md")
        if not plan_content:
            # Fall back to generic template
            plan_content = PLAN_TEMPLATE.format(
                build_name=build_name,
                date=current_date
            )
        (planning_dir / "03-plan.md").write_text(plan_content, encoding='utf-8')
        print(f"[OK] Created 03-plan.md (type: {build_type})")
    except Exception as e:
        print(f"[ERROR] Error creating 03-plan.md: {e}")
        return None

    # Create 04-steps.md (prefer type-specific template)
    try:
        steps_content = load_type_template(build_type, "steps.md")
        if not steps_content:
            # Fall back to generic template
            steps_content = STEPS_TEMPLATE.format(
                build_name=build_name,
                build_id=build_id,
                sanitized_name=sanitized_name,
                date=current_date
            )
        (planning_dir / "04-steps.md").write_text(steps_content, encoding='utf-8')
        print(f"[OK] Created 04-steps.md (type: {build_type})")
    except Exception as e:
        print(f"[ERROR] Error creating 04-steps.md: {e}")
        return None

    # Count checkboxes in the steps file we just created
    steps_file = planning_dir / "04-steps.md"
    total_tasks, tasks_completed = count_checkboxes_in_file(steps_file)
    print(f"[OK] Counted {total_tasks} tasks in 04-steps.md")

    # Create resume-context.md with actual task count
    try:
        resume_content = f"""---
# AUTO-SYNCED by PreCompact hook (don't manually update these)
session_id: ""
session_ids: []
resume_schema_version: "2.0"
last_updated: "{timestamp}"

# BUILD (static - set at creation)
build_id: "{build_id}-{sanitized_name}"
build_name: "{build_name}"
build_type: "{build_type}"

# AUTO-SYNCED: current_phase detected from Phase 1 completion in 04-steps.md
# Values: "planning" (Phase 1 incomplete), "execution" (Phase 1 done), "complete" (100%)
current_phase: "planning"

# LOADING
# next_action: AUTO-SYNCED unless you set a custom value (e.g., "implement-phase-3")
# Custom values are preserved; standard values (plan-build, execute-build) are auto-managed
next_action: "plan-build"
# files_to_load: MANUAL - update this when creating working files
files_to_load:
  - "01-planning/01-overview.md"
  - "01-planning/02-discovery.md"
  - "01-planning/03-plan.md"
  - "01-planning/04-steps.md"

# DISCOVERY STATE (MANUAL)
rediscovery_round: 0
discovery_complete: false

# PROGRESS - AUTO-SYNCED from 04-steps.md checkbox counts
current_section: 1
current_task: 1
total_tasks: {total_tasks}
tasks_completed: {tasks_completed}
---

## Progress Summary

**Build Type**: {build_type}
**Phase**: Planning | 0/{total_tasks} tasks (0%)

### Latest Session

**Completed this session:**
- (none yet)

**Next steps:**
1. Complete 01-overview.md with purpose and success criteria
2. Complete 02-discovery.md with dependencies

---

*Update this summary after each session with accomplishments and next steps*
"""
        (planning_dir / "resume-context.md").write_text(resume_content, encoding='utf-8')
        print("[OK] Created resume-context.md")
    except Exception as e:
        print(f"[ERROR] Error creating resume-context.md: {e}")
        return None

    # Print success message
    print(f"\n[SUCCESS] Build '{build_name}' initialized successfully!")
    print(f"   Build ID: {build_id}")
    print(f"   Location: {build_dir}")
    print("\nBuild structure created:")
    print(f"  {build_dirname}/")
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

    return build_dir


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Initialize a new Nexus build with templates",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  init_build.py "Website Redesign" --path 02-builds/active --type build
  init_build.py "Market Research" --path 02-builds/active --type research
  init_build.py my-feature --path 02-builds/active -d "Add new feature" --id 15

Build structure created:
  02-builds/active/
    NN-build-name/
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

    parser.add_argument("name", help="Build name (spaces or hyphens)")
    parser.add_argument("--path", "-p", default="02-builds/active",
                        help="Path to builds directory (default: 02-builds/active)")
    parser.add_argument("--type", "-t", default="generic",
                        choices=["build", "integration", "research", "strategy", "content", "process", "skill", "generic"],
                        help="Build type for template selection (default: generic)")
    parser.add_argument("--description", "-d", default="",
                        help="Build description")
    parser.add_argument("--id", type=int, default=None,
                        help="Override auto-assigned build ID")

    args = parser.parse_args()

    print(f"Initializing build: {args.name}")
    print(f"Location: {args.path}")
    print(f"Type: {args.type}")
    if args.description:
        print(f"Description: {args.description}")
    if args.id:
        print(f"ID Override: {args.id:02d}")
    print()

    result = init_build(
        build_name=args.name,
        path=args.path,
        build_type=args.type,
        description=args.description,
        build_id_override=args.id
    )

    if result:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
