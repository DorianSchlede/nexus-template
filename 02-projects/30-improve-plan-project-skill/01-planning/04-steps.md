# Improve Plan-Project Skill - Execution Steps

**Last Updated**: 2026-01-07
**Status**: REVISED - Mandatory Router + Template-First Architecture

---

## Context Requirements

**Project Location**: `02-projects/30-improve-plan-project-skill/`

**Files to Load for Execution**:
- `01-planning/03-plan.md` - Approach, decisions
- `02-resources/revised-architecture.md` - **CURRENT** architecture spec
- `01-planning/04-steps.md` - This file

**Output Location**: `00-system/skills/projects/plan-project/`

---

## Phase 1: Planning

- [x] Complete 01-overview.md
- [x] Complete 02-discovery.md
- [x] Complete 03-plan.md
- [x] Complete 04-steps.md
- [x] Review with stakeholder (REVISED: mandatory router, template-first)

---

## Phase 2: Create Template Structure (~1 hr)

**Goal**: Create `templates/types/` folder structure with all 7 type templates

### 2.1 Create Directory Structure
- [ ] Create `plan-project/templates/types/`
- [ ] Create subfolders: build, integration, research, strategy, content, process, generic

### 2.2 Create _type.yaml for Each Type
- [ ] `types/build/_type.yaml` - keywords, mental_models, inline discovery
- [ ] `types/integration/_type.yaml` - routes to add-integration skill
- [ ] `types/research/_type.yaml` - routes to create-research-project skill
- [ ] `types/strategy/_type.yaml` - deep planning, decision frameworks
- [ ] `types/content/_type.yaml` - creative brief structure
- [ ] `types/process/_type.yaml` - workflow optimization
- [ ] `types/generic/_type.yaml` - minimal fallback

### 2.3 Create Templates for Each Type
- [ ] `types/build/` - plan.md, steps.md, discovery.md
- [ ] `types/integration/` - plan.md, steps.md, discovery.md
- [ ] `types/research/` - plan.md, steps.md, discovery.md
- [ ] `types/strategy/` - plan.md, steps.md, discovery.md
- [ ] `types/content/` - plan.md, steps.md, discovery.md
- [ ] `types/process/` - plan.md, steps.md, discovery.md
- [ ] `types/generic/` - plan.md, steps.md, discovery.md

### 2.4 Create References
- [ ] `references/routing-logic.md` - How router works

---

## Phase 3: Update plan-project SKILL.md (~30 min)

**Goal**: Simplify SKILL.md to reference templates, add type detection

- [ ] Remove hardcoded type logic
- [ ] Add template-based type detection (scan _type.yaml keywords)
- [ ] Add routing logic that reads discovery.skill from _type.yaml
- [ ] Add mental model step that reads mental_models from _type.yaml
- [ ] Update description to reflect mandatory router role

---

## Phase 4: Update Specialized Skills (~30 min)

**Goal**: Add entry_mode handling, deprecation notices

### 4.1 Update add-integration
- [ ] Add entry_mode check at workflow start
- [ ] Skip Steps 1, 6 when entry_mode=from_router
- [ ] Add deprecation notice for direct invocation
- [ ] Point users to `plan project` instead

### 4.2 Update create-research-project
- [ ] Add entry_mode check at workflow start
- [ ] Skip Step 1 when entry_mode=from_router
- [ ] Add deprecation notice for direct invocation
- [ ] Point users to `plan project` instead

---

## Phase 5: Testing (~30 min)

**Goal**: Verify all flows work with mandatory router

- [ ] Test: "plan project for slack integration" → detects integration → routes
- [ ] Test: "plan project for ontology research" → detects research → routes
- [ ] Test: "plan project for new feature" → detects build → inline discovery
- [ ] Test: Mental models apply before routing (check output)
- [ ] Test: Direct "add integration" shows deprecation notice
- [ ] Test: Direct "create research project" shows deprecation notice

---

## Notes

**Estimated Total**: ~2.5 hours AI time

**Key Architecture Reference**: `02-resources/revised-architecture.md`

**Key Decision**: Router is MANDATORY. No backwards compatibility for direct skill invocation.

---

*Mark tasks complete with [x] as you finish them*
