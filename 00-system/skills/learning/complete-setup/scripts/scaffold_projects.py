#!/usr/bin/env python3
"""
scaffold_projects.py - Create project scaffolds from roadmap

Used by setup-system skill during Step 5 (Initiate Projects).

Creates for each roadmap item:
- Project folder in 02-builds/
- 4 subfolders (01-planning, 02-resources, 03-working, 04-outputs)
- 01-overview.md with AI-generated content
- Empty templates (02-discovery.md, 03-plan.md, 04-steps.md)
- resume-context.md with dependencies

Usage:
    from scaffold_projects import ProjectScaffolder

    scaffolder = ProjectScaffolder(workspace_path)
    scaffolder.create_project_from_roadmap_item(item, goals_context)
"""

import re
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional
from dataclasses import dataclass


@dataclass
class RoadmapItem:
    """A single item from the user's roadmap."""
    name: str
    type: str  # BUILD, SKILL, INTEGRATION
    priority: str  # high, medium, low
    dependencies: List[str]
    rationale: str
    order: int


@dataclass
class ProjectScaffold:
    """Created project scaffold."""
    project_id: str
    name: str
    path: Path
    files_created: List[str]


class ProjectScaffolder:
    """
    Creates project scaffolds from roadmap items.

    Each project gets:
    - Unique ID (e.g., "05-sales-playbook")
    - Standard 4-folder structure
    - Overview.md with context
    - Empty planning templates
    - Resume context for continuity
    """

    def __init__(self, workspace_path: Path):
        """
        Initialize scaffolder.

        Args:
            workspace_path: Path to Nexus workspace root
        """
        self.workspace = workspace_path
        self.builds_dir = workspace_path / "02-builds"
        self.created_projects: List[ProjectScaffold] = []

    def get_next_project_id(self) -> int:
        """
        Get next available project ID number.

        Scans 02-builds/ for existing projects and returns next number.
        Skips special projects (00-onboarding-session, archived).
        """
        max_id = 0

        if not self.builds_dir.exists():
            return 1

        for item in self.builds_dir.iterdir():
            if item.is_dir() and not item.name.startswith((".", "_")):
                # Extract number prefix if exists
                match = re.match(r'^(\d+)-', item.name)
                if match:
                    num = int(match.group(1))
                    if num > max_id and num != 0:  # Skip 00-onboarding
                        max_id = num

        return max_id + 1

    def slugify(self, name: str) -> str:
        """Convert name to URL-safe slug."""
        slug = name.lower()
        slug = re.sub(r'[^a-z0-9]+', '-', slug)
        slug = slug.strip('-')
        return slug

    def create_project_from_roadmap_item(
        self,
        item: RoadmapItem,
        goals_context: Optional[Dict[str, Any]] = None,
        file_analysis: Optional[Dict[str, Any]] = None
    ) -> ProjectScaffold:
        """
        Create a single project scaffold from roadmap item.

        Args:
            item: RoadmapItem to scaffold
            goals_context: User's goals for context (optional)
            file_analysis: File analysis results for context (optional)

        Returns:
            ProjectScaffold with created paths
        """
        # Generate project ID
        next_num = self.get_next_project_id()
        slug = self.slugify(item.name)
        project_id = f"{next_num:02d}-{slug}"

        project_path = self.builds_dir / project_id
        files_created = []

        # Create 4 standard folders
        folders = ["01-planning", "02-resources", "03-working", "04-outputs"]
        for folder in folders:
            folder_path = project_path / folder
            folder_path.mkdir(parents=True, exist_ok=True)
            files_created.append(str(folder_path.relative_to(self.workspace)))

        # Create 01-overview.md
        overview_content = self._generate_overview(item, goals_context, file_analysis, project_id)
        overview_path = project_path / "01-planning" / "01-overview.md"
        overview_path.write_text(overview_content, encoding='utf-8')
        files_created.append(str(overview_path.relative_to(self.workspace)))

        # Create empty templates
        templates = {
            "02-discovery.md": self._empty_discovery_template(item.name),
            "03-plan.md": self._empty_plan_template(item.name),
            "04-steps.md": self._empty_steps_template(item.name),
        }

        for filename, content in templates.items():
            file_path = project_path / "01-planning" / filename
            file_path.write_text(content, encoding='utf-8')
            files_created.append(str(file_path.relative_to(self.workspace)))

        # Create resume-context.md
        resume_content = self._generate_resume_context(project_id, item)
        resume_path = project_path / "01-planning" / "resume-context.md"
        resume_path.write_text(resume_content, encoding='utf-8')
        files_created.append(str(resume_path.relative_to(self.workspace)))

        scaffold = ProjectScaffold(
            project_id=project_id,
            name=item.name,
            path=project_path,
            files_created=files_created
        )

        self.created_projects.append(scaffold)
        return scaffold

    def create_all_from_roadmap(
        self,
        roadmap: List[RoadmapItem],
        goals_context: Optional[Dict[str, Any]] = None,
        file_analysis: Optional[Dict[str, Any]] = None
    ) -> List[ProjectScaffold]:
        """
        Create scaffolds for all roadmap items.

        Args:
            roadmap: List of RoadmapItem objects
            goals_context: User's goals context
            file_analysis: File analysis results

        Returns:
            List of created ProjectScaffold objects
        """
        results = []
        for item in roadmap:
            scaffold = self.create_project_from_roadmap_item(
                item, goals_context, file_analysis
            )
            results.append(scaffold)
        return results

    def _generate_overview(
        self,
        item: RoadmapItem,
        goals_context: Optional[Dict[str, Any]],
        file_analysis: Optional[Dict[str, Any]],
        build_id: str
    ) -> str:
        """Generate overview.md content matching standard build format."""
        today = datetime.now().strftime('%Y-%m-%d')

        # Build context section
        context_parts = []
        if goals_context:
            if goals_context.get("role"):
                context_parts.append(f"- **User Role**: {goals_context['role']}")
            if goals_context.get("short_term_goal"):
                context_parts.append(f"- **Goal Context**: {goals_context['short_term_goal']}")

        if file_analysis and file_analysis.get("professional_context"):
            ctx = file_analysis["professional_context"]
            if ctx.get("domain"):
                context_parts.append(f"- **Domain**: {ctx['domain']}")

        context_section = '\n'.join(context_parts) if context_parts else "Created during initial setup"

        # Dependencies as constraints
        constraints = []
        if item.dependencies:
            constraints.append(f"Depends on: {', '.join(item.dependencies)}")
        constraints.append(f"Priority: {item.priority.upper()}")
        constraints.append(f"Type: {item.type}")
        constraints_section = '\n'.join(f"- {c}" for c in constraints)

        return f"""---
id: {build_id}
name: {item.name}
status: PLANNING
description: "{item.rationale}"
created: {today}
build_path: 02-builds/{build_id}/
---

# {item.name}

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

{item.rationale}

---

## Success Criteria

**Must achieve**:
- [ ] [Define measurable outcome 1]
- [ ] [Define measurable outcome 2]

**Nice to have**:
- [ ] [Optional outcome]

---

## Context

**Background**: {context_section}

**Stakeholders**: [Who benefits from this?]

**Constraints**:
{constraints_section}

---

*Next: Fill in 02-discovery.md*
"""

    def _empty_discovery_template(self, name: str) -> str:
        """Generate empty discovery template matching build format."""
        return f"""---
status: not_started
---

# Discovery: {name}

## Dependencies

**Internal**: [Other builds this depends on]

**External**: [APIs, tools, or resources needed]

---

## Existing Patterns

**Related Code/Files**: [What exists that we can build on?]

**Conventions**: [Patterns to follow]

---

## Risks & Open Questions

| Risk/Question | Impact | Mitigation |
|---------------|--------|------------|
| [Risk 1] | [High/Med/Low] | [How to address] |

---

## Research Notes

[Add notes from research, conversations, examples]

---

*Next: Complete discovery, then fill 03-plan.md*
"""

    def _empty_plan_template(self, name: str) -> str:
        """Generate empty plan template matching build format."""
        return f"""---
status: not_started
---

# Plan: {name}

## Approach

[Describe the high-level implementation approach]

---

## Key Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| [Decision 1] | [Choice made] | [Why this choice] |

---

## Components

1. **[Component 1]**: [Purpose]
2. **[Component 2]**: [Purpose]
3. **[Component 3]**: [Purpose]

---

## Mental Models Applied

[Which mental models inform this plan? First Principles? Pre-mortem?]

---

*Next: Get plan approved, then fill 04-steps.md*
"""

    def _empty_steps_template(self, name: str) -> str:
        """Generate empty steps template matching build format."""
        return f"""---
status: not_started
total_tasks: 0
completed_tasks: 0
current_section: 0
current_task: 0
---

# Steps: {name}

## Checkpoint 1: [Name]

**Goal**: [What this checkpoint achieves]

- [ ] Task 1 **[REQ-01]**
- [ ] Task 2 **[REQ-02]**

## Checkpoint 2: [Name]

**Goal**: [What this checkpoint achieves]

- [ ] Task 3 **[REQ-03]**
- [ ] Task 4 **[REQ-04]**

## Checkpoint 3: [Name]

**Goal**: [What this checkpoint achieves]

- [ ] Task 5 **[REQ-05]**
- [ ] Task 6 **[REQ-06]**

---

*Fill in tasks after plan is approved. Use checkpoints to group related work.*
"""

    def _generate_resume_context(self, build_id: str, item: RoadmapItem) -> str:
        """Generate resume-context.md for cross-session continuity."""
        today = datetime.now().isoformat()

        deps_section = ""
        if item.dependencies:
            deps_list = '\n'.join(f'  - "{dep}"' for dep in item.dependencies)
            deps_section = f"""dependencies:
{deps_list}
"""

        return f"""---
session_id: ""
session_ids: []
resume_schema_version: "2.0"
last_updated: "{today}"

# BUILD IDENTITY
build_id: "{build_id}"
build_name: "{item.name}"
current_phase: "planning"

# LOADING CONTEXT
next_action: "start-discovery"
files_to_load:
  - "01-planning/01-overview.md"
  - "01-planning/02-discovery.md"

# PROGRESS TRACKING
current_section: 0
current_task: 0
total_tasks: 0
tasks_completed: 0
{deps_section}---

## Progress Summary

**Status**: PLANNING
**Phase**: Not Started

**Next Action**:
Start discovery - read overview and begin 02-discovery.md

---

*Auto-generated during setup-system*
"""


def main():
    """CLI for testing scaffolding."""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python scaffold_projects.py <workspace_path>")
        sys.exit(1)

    workspace = Path(sys.argv[1])
    scaffolder = ProjectScaffolder(workspace)

    # Test with sample roadmap
    sample_roadmap = [
        RoadmapItem(
            name="Sales Playbook",
            type="BUILD",
            priority="high",
            dependencies=[],
            rationale="Foundation for all sales automation - captures methodology",
            order=1
        ),
        RoadmapItem(
            name="Proposal Generator",
            type="SKILL",
            priority="high",
            dependencies=["Sales Playbook"],
            rationale="Automates proposal creation using playbook as template",
            order=2
        ),
    ]

    results = scaffolder.create_all_from_roadmap(sample_roadmap)

    print(f"Created {len(results)} project scaffolds:")
    for scaffold in results:
        print(f"  - {scaffold.project_id}: {scaffold.name}")
        print(f"    Path: {scaffold.path}")
        print(f"    Files: {len(scaffold.files_created)}")


if __name__ == "__main__":
    main()
