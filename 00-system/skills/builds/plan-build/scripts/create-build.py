#!/usr/bin/env python3
"""
[DEPRECATED] - Use init_build.py instead

This script is deprecated. Use the new improved script:
    python 00-system/skills/plan-build/scripts/init_build.py "Build Name" --path 02-builds

New improvements:
- Auto-assigns build IDs (no manual ID selection)
- Creates 4-folder structure: 01-planning/, 02-resources/, 03-working/, 04-outputs/
- Generates 3 planning files: overview.md, plan.md, steps.md (simpler than 4 files)
- Supports mental models and collaborative planning workflow
- Aligned with plan-build skill's interactive planning mode

This file is kept for backward compatibility only and will be removed in a future version.

---

OLD DOCUMENTATION (for reference):

plan-build.py - Initialize a new build with proper structure and YAML frontmatter

Usage:
    python plan-build.py <build-name> --id <number>
    python plan-build.py website-development --id 05

Example:
    python plan-build.py client-proposal-system --id 06
"""

import sys
from pathlib import Path
from datetime import datetime

# Display deprecation warning
print("\n" + "="*70)
print("[DEPRECATED] DEPRECATION WARNING")
print("="*70)
print("This script (plan-build.py) is deprecated.")
print("\nPlease use the new script instead:")
print("  python 00-system/skills/plan-build/scripts/init_build.py \"Build Name\" --path 02-builds")
print("\nThe new script provides:")
print("  - Auto-assigned build IDs")
print("  - Improved 4-folder structure (with 02-resources/)")
print("  - Simplified 3-file planning (overview, plan, steps)")
print("  - Mental models integration")
print("="*70 + "\n")
print("Continuing with deprecated script...\n")

BUILD_OVERVIEW_TEMPLATE = """---
id: {build_id}
name: {build_name}
status: PLANNING
description: {description}
created: {created_date}
last_worked: {created_date}
tags: []
---

# Build: {build_name}

## Purpose

[TODO: Describe what this build is about in 1-2 paragraphs]

## Success Criteria

[TODO: How will you know this build succeeded?]
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## Constraints

**Timeline**: [TODO]
**Budget**: [TODO]
**Resources**: [TODO]

## Current Status

**Status**: PLANNING
**Progress**: 0/0 tasks complete
**Next Step**: Complete planning documents

---

**Note**: This build was created using the `plan-build` script.
Use the planning files below to define requirements, design, and tasks.
"""

REQUIREMENTS_TEMPLATE = """# Requirements: {build_name}

## Overview

[TODO: High-level summary of what needs to be built/accomplished]

## Functional Requirements

### FR-1: [Category Name]
- [ ] Requirement detail 1
- [ ] Requirement detail 2

### FR-2: [Category Name]
- [ ] Requirement detail 1
- [ ] Requirement detail 2

## Non-Functional Requirements

**Performance**: [TODO]
**Usability**: [TODO]
**Reliability**: [TODO]

## Constraints

**Timeline**: [TODO]
**Budget**: [TODO]
**Technical**: [TODO]

## Assumptions

- [TODO: What are we assuming is true?]

## Stakeholders

- [TODO: Who's involved and what do they need?]

## Out of Scope

- [TODO: What are we explicitly NOT doing?]
"""

DESIGN_TEMPLATE = """# Design: {build_name}

## Approach Overview

[TODO: High-level strategy and reasoning]

## Architecture / Structure

[TODO: How components fit together]

```
Component A
  ├── Sub-component 1
  └── Sub-component 2

Component B
  ├── Sub-component 3
  └── Sub-component 4
```

## Implementation Strategy

### Phase 1: [Phase Name]
[TODO: What happens in this phase and why]

### Phase 2: [Phase Name]
[TODO: What happens in this phase and why]

## Key Decisions

### Decision 1: [Decision Name]
**Options Considered**: A, B, C
**Chosen**: A
**Rationale**: [Why]

## Dependencies

- [TODO: External dependencies, prerequisites]

## Risks & Mitigations

### Risk 1: [Description]
**Likelihood**: Medium
**Impact**: High
**Mitigation**: [How we'll handle it]

## Technical Notes

**Tools**: [TODO]
**Platforms**: [TODO]
**Technologies**: [TODO]
"""

TASKS_TEMPLATE = """# Tasks: {build_name}

**Total Estimate**: [TODO: X hours/days/weeks]
**Priority**: [TODO: High/Medium/Low]

---

## Phase 1: Planning

**Goal**: Complete all planning documents
**Estimate**: 1-2 hours

- [ ] Fill out requirements.md
- [ ] Fill out design.md
- [ ] Break down tasks in detail

**Milestone**: Planning complete, ready to execute

---

## Phase 2: [Main Work Phase]

**Goal**: [TODO: What this phase accomplishes]
**Estimate**: [TODO]

- [ ] Task 1
- [ ] Task 2
- [ ] Task 3

**Milestone**: [TODO: What "done" looks like]

---

## Phase 3: Completion

**Goal**: Finalize and validate
**Estimate**: [TODO]

- [ ] Final review of deliverables
- [ ] Validate against success criteria
- [ ] Document learnings
- [ ] Build complete!

---

**Notes**:
- Check off tasks as you complete them (- [x])
- close-session will track your progress automatically
- Feel free to add tasks as you discover them
"""

GITKEEP = ""

def title_case_name(kebab_name):
    """Convert kebab-case to Title Case."""
    return ' '.join(word.capitalize() for word in kebab_name.split('-'))


def generate_description(build_name):
    """Generate description from build name."""
    words = build_name.split('-')

    # Take first word, first two words, and full name
    triggers = []
    if len(words) >= 1:
        triggers.append(f'"{words[0]}"')
    if len(words) >= 2:
        triggers.append(f'"{" ".join(words[:2])}"')
    if len(words) > 2:
        triggers.append(f'"{build_name}"')

    return f"Load when user mentions {', '.join(triggers)}"


def create_build(build_name: str, build_id: str, base_path: str = "."):
    """
    Create a new build with structure and templates.

    Args:
        build_name: Kebab-case build name
        build_id: Two-digit build ID
        base_path: Base path to Nexus-v3

    Returns:
        Path to created build, or None if error
    """
    base = Path(base_path)
    build_folder = f"{build_id}-{build_name}"
    build_path = base / "02-Builds" / build_folder

    # Check if already exists
    if build_path.exists():
        print(f"[ERROR] Build already exists: {build_path}")
        return None

    # Create folder structure
    try:
        build_path.mkdir(parents=True)
        (build_path / "01-planning").mkdir()
        (build_path / "02-working").mkdir()
        (build_path / "03-outputs").mkdir()
        print(f"[OK] Created {build_folder}/")
        print(f"[OK] Created 01-planning/, 02-working/, and 03-outputs/ folders")
    except Exception as e:
        print(f"[ERROR] Failed to create folders: {e}")
        return None

    # Generate content
    today = datetime.now().strftime('%Y-%m-%d')
    title_name = title_case_name(build_name)
    description = generate_description(build_name)

    # Write files
    files = {
        '01-planning/overview.md': BUILD_OVERVIEW_TEMPLATE.format(
            build_id=f"{build_id}-{build_name}",
            build_name=title_name,
            description=description,
            created_date=today
        ),
        '01-planning/requirements.md': REQUIREMENTS_TEMPLATE.format(
            build_name=title_name
        ),
        '01-planning/design.md': DESIGN_TEMPLATE.format(
            build_name=title_name
        ),
        '01-planning/tasks.md': TASKS_TEMPLATE.format(
            build_name=title_name
        ),
        '03-outputs/.gitkeep': GITKEEP
    }

    for file_path, content in files.items():
        full_path = build_path / file_path
        try:
            full_path.write_text(content, encoding='utf-8')
            print(f"[OK] Created {file_path}")
        except Exception as e:
            print(f"[ERROR] Failed to create {file_path}: {e}")
            return None

    print(f"\n[DONE] Build '{build_folder}' created successfully!")
    print(f"\nNext steps:")
    print(f"1. Edit 02-Builds/{build_folder}/01-planning/overview.md")
    print(f"2. Fill out requirements.md, design.md, and tasks.md in 01-planning/")
    print(f"3. Run 'python validate.py --build 02-Builds/{build_folder}' to validate")

    return build_path


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Create a new Nexus-v3 build")
    parser.add_argument('name', help='Build name in kebab-case (e.g., website-development)')
    parser.add_argument('--id', required=True, help='Two-digit build ID (e.g., 05)')
    parser.add_argument('--base-path', default='.', help='Base path to Nexus-v3')

    args = parser.parse_args()

    # Validate name format
    if not re.match(r'^[a-z0-9-]+$', args.name):
        print("[ERROR] Build name must be kebab-case (lowercase letters, digits, hyphens)")
        print("Examples: website-development, client-proposal-system, data-analysis")
        sys.exit(1)

    # Validate ID format
    if not re.match(r'^\d{2}$', args.id):
        print("[ERROR] Build ID must be two digits (e.g., 05, 10, 23)")
        sys.exit(1)

    # Create build
    print(f"Creating build: {args.id}-{args.name}")
    print()

    result = create_build(args.name, args.id, args.base_path)

    if result:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    import re
    main()
