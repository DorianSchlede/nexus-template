---
id: 30-improve-plan-project-skill
name: Improve Plan-Project Skill
status: PLANNING
description: "Project: Improve Plan-Project Skill"
created: 2026-01-07
project_path: 02-projects/30-improve-plan-project-skill/
---

# Improve Plan-Project Skill

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

Merge the specialized planning capabilities from `add-integration` and `create-research-project` skills INTO the core `plan-project` skill. Currently, these exist as separate skills with duplicated project creation logic. After this improvement:

1. **plan-project** becomes the SINGLE entry point for ALL project creation
2. **add-integration** becomes a "project type" within plan-project (not a separate skill)
3. **create-research-project** becomes a "project type" within plan-project (not a separate skill)
4. Project type detection triggers type-specific discovery and planning workflows

**Vision**: One skill to rule all project creation, with intelligent type-specific enhancements.

---

## Success Criteria

**Must achieve**:
- [ ] plan-project detects "Integration" project type and triggers API discovery workflow
- [ ] plan-project detects "Research" project type and triggers paper search workflow
- [ ] add-integration skill is deprecated or redirects to `plan-project --type integration`
- [ ] create-research-project skill is deprecated or redirects to `plan-project --type research`
- [ ] Existing project types (Build, Strategy, Content, Process, Generic) still work

**Nice to have**:
- [ ] Unified mental model selection works for all project types
- [ ] Type-specific discovery results populate plan.md automatically
- [ ] Web search integration for integration projects works seamlessly

---

## Context

**Background**:
Currently we have THREE skills that create projects:
1. `plan-project` - Generic project planning with mental models
2. `add-integration` - API discovery + project creation for integrations
3. `create-research-project` - Paper search + preprocessing for research

This creates duplication and confusion. Users need to know which skill to invoke.

**Stakeholders**:
- Nexus users who create projects
- The orchestrator routing logic (simpler with one entry point)
- Future maintainers (less code to maintain)

**Constraints**:
- Must preserve the specialized discovery workflows (API discovery, paper search)
- Must maintain backward compatibility (existing projects still work)
- Mental model selection should remain consistent across types

---

## Key Changes

### 1. Merge Integration Discovery into plan-project
- When user selects "Integration" type, trigger web search for API docs
- Parse endpoints, present for selection (like add-integration Step 5)
- Store in `02-resources/integration-config.json`

### 2. Merge Research Discovery into plan-project
- When user selects "Research" type, trigger paper search workflow
- Handle paper selection, download, preprocessing
- Generate `_briefing.md`, `_analysis_kit.md`, etc.

### 3. Unified Project Type Selection
```
What type of project is this?

1. Build/Create     - Software, features, systems
2. Research         - Academic papers, literature reviews ← ENHANCED
3. Strategy         - Business decisions, planning
4. Content          - Documents, presentations
5. Integration      - Connect external APIs/services ← ENHANCED
6. Process          - Workflows, automation
7. Generic          - Other projects
```

---

*Next: Fill in 02-discovery.md*
