# Revised Architecture: Mandatory Router + Template-First

**Date**: 2026-01-07
**Status**: APPROVED (supersedes architecture-decision.md)

---

## Core Principles

1. **Router is MANDATORY** - All project creation goes through plan-project
2. **Templates define types** - Add a type by adding a template folder
3. **Skills are execution engines** - Called BY router, not directly
4. **Mental models always run** - Scaled by type complexity
5. **Same structure, different depth** - All projects have same folders, templates control planning depth

---

## Key Insight

From AI perspective, even a "full project" is **2-3 hours of work**. The structure ensures quality and completeness, not because work takes weeks.

**Everything is a project. Types determine planning depth.**

---

## Architecture Flow

```
User: "integrate slack" or "create project"
         │
         ▼
┌─────────────────────────────────────────────────────────┐
│              plan-project (MANDATORY ROUTER)            │
├─────────────────────────────────────────────────────────┤
│                                                         │
│ Step 1: Type Detection                                  │
│   - Parse keywords from user input                      │
│   - Match against templates/types/*/_type.yaml          │
│   - OR ask user to select type                          │
│                                                         │
│ Step 2: Mental Models (ALWAYS, scaled by type)          │
│   - Load mental_models config from _type.yaml           │
│   - Quick types: First Principles + Success Criteria    │
│   - Complex types: Full suite with type-specific focus  │
│                                                         │
│ Step 3: Create Project Structure                        │
│   - Run init_project.py --type {type}                   │
│   - Creates standard 4-folder structure                 │
│   - Populates plan.md from type template                │
│   - Populates steps.md from type template               │
│                                                         │
│ Step 4: Type-Specific Discovery                         │
│   - IF _type.yaml has discovery.skill:                  │
│       → Route to specialized skill (entry_mode=router)  │
│   - ELSE:                                               │
│       → Use inline discovery.md template                │
│                                                         │
│ Step 5: Return Project Ready for Execution              │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## Directory Structure

```
plan-project/
├── SKILL.md                      # Router logic (simplified, references templates)
├── scripts/
│   └── init_project.py           # Project scaffolding (enhanced)
│
├── templates/
│   └── types/                    # ONE FOLDER PER TYPE
│       │
│       ├── build/
│       │   ├── _type.yaml        # Type metadata + routing config
│       │   ├── plan.md           # Plan template sections
│       │   ├── steps.md          # Steps template with phases
│       │   └── discovery.md      # Discovery guidance (inline)
│       │
│       ├── integration/
│       │   ├── _type.yaml        # Links to add-integration skill
│       │   ├── plan.md           # Integration-specific plan sections
│       │   ├── steps.md          # Integration phases
│       │   └── discovery.md      # Inline fallback (skill preferred)
│       │
│       ├── research/
│       │   ├── _type.yaml        # Links to create-research-project
│       │   ├── plan.md           # Research-specific plan sections
│       │   ├── steps.md          # Research phases (3-phase pipeline)
│       │   └── discovery.md      # Inline fallback
│       │
│       ├── strategy/
│       │   ├── _type.yaml
│       │   ├── plan.md           # Decision framework sections
│       │   ├── steps.md
│       │   └── discovery.md
│       │
│       ├── content/
│       │   ├── _type.yaml
│       │   ├── plan.md           # Creative brief sections
│       │   ├── steps.md
│       │   └── discovery.md
│       │
│       ├── process/
│       │   ├── _type.yaml
│       │   ├── plan.md           # Current/future state sections
│       │   ├── steps.md
│       │   └── discovery.md
│       │
│       └── generic/
│           ├── _type.yaml
│           ├── plan.md           # Minimal sections
│           ├── steps.md
│           └── discovery.md
│
└── references/
    ├── type-detection.md         # Auto-generated keyword → type mapping
    └── routing-logic.md          # How the router works
```

---

## _type.yaml Schema

```yaml
# Required fields
name: string                      # Display name
description: string               # When to use this type
keywords: string[]                # Trigger words for auto-detection

# Mental models configuration
mental_models:
  mode: quick | thorough          # How deep to go
  focus: string[]                 # Which models to emphasize (optional)

# Discovery configuration
discovery:
  skill: string                   # Skill to route to (optional)
  entry_mode: from_router         # Required if skill specified
  skip_steps: number[]            # Steps to skip in target skill (optional)
  inline: boolean                 # Use discovery.md template (default if no skill)
```

### Example: integration/_type.yaml

```yaml
name: Integration
description: Connect external APIs and services to Nexus
keywords:
  - integrate
  - integration
  - API
  - connect
  - webhook
  - oauth
  # Service names detected dynamically

mental_models:
  mode: thorough
  focus:
    - first-principles      # What's the core need?
    - devils-advocate       # What could break?
    - pre-mortem           # API changes, rate limits

discovery:
  skill: add-integration
  entry_mode: from_router
  skip_steps: [1, 6]        # Skip project creation (1) and project setup (6)
```

### Example: build/_type.yaml

```yaml
name: Build
description: Create new software, features, or systems
keywords:
  - build
  - create
  - implement
  - develop
  - feature
  - component

mental_models:
  mode: thorough
  focus:
    - first-principles
    - stakeholder-mapping
    - pre-mortem

discovery:
  inline: true              # No specialized skill, use discovery.md
```

---

## Adding a New Type

To add a new type (e.g., "automation"):

1. **Create folder**: `templates/types/automation/`

2. **Create _type.yaml**:
   ```yaml
   name: Automation
   description: Automate repetitive workflows and processes
   keywords:
     - automate
     - automation
     - workflow
     - schedule
     - cron
     - trigger

   mental_models:
     mode: thorough
     focus:
       - first-principles
       - pre-mortem
       - process-mapping

   discovery:
     inline: true
   ```

3. **Create plan.md template** with automation-specific sections

4. **Create steps.md template** with automation phases

5. **Create discovery.md** with automation discovery guidance

**That's it.** Router auto-discovers from folder structure.

---

## Specialized Skill Contract

When router calls a specialized skill:

```yaml
# Passed to skill
entry_mode: from_router
project_path: "02-projects/XX-name/"
mental_models_applied: true
success_criteria:
  - "Criterion 1 from mental model phase"
  - "Criterion 2"
```

Skill MUST:
- Check `entry_mode` at start
- Skip project creation steps if `entry_mode == from_router`
- Use provided `project_path` for all file operations
- Respect that mental models already ran

---

## Changes from Original Plan

| Original | Revised |
|----------|---------|
| Router optional | Router MANDATORY |
| Templates in flat folders | Templates grouped by type |
| Type detection in SKILL.md | Type detection from _type.yaml keywords |
| Mental models hardcoded | Mental models per-type in _type.yaml |
| Backwards compat for direct invocation | No direct invocation (router only) |
| Add type = modify multiple files | Add type = add one folder |

---

## Migration: Existing Skills

### add-integration
- Keep all logic
- Add entry_mode check at start
- When `entry_mode == from_router`: skip Steps 1, 6
- Direct invocation: Show deprecation notice, suggest `plan project`

### create-research-project
- Keep all logic
- Add entry_mode check at start
- When `entry_mode == from_router`: skip Step 1
- Direct invocation: Show deprecation notice, suggest `plan project`

---

## Benefits

1. **Single entry point** - Users always use `plan project`
2. **Consistent quality** - Mental models always applied
3. **Easy extensibility** - Add folder = add type
4. **Self-documenting** - _type.yaml describes each type
5. **Clean separation** - Router logic vs type templates vs execution skills

---

## Timeline (AI Hours)

| Phase | Work | AI Time |
|-------|------|---------|
| Phase 1 | Create template folders + files | ~1 hour |
| Phase 2 | Update plan-project SKILL.md | ~30 min |
| Phase 3 | Update add-integration + create-research-project | ~30 min |
| Phase 4 | Testing | ~30 min |
| **Total** | | **~2.5 hours** |
