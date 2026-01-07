# Improve Plan-Project Skill - Execution Steps

**Last Updated**: 2026-01-07
**Status**: REVISED v2.3 - KIRO Task Patterns Applied
**Project Type**: Build

---

## Context Requirements

**Project Location**: `02-projects/30-improve-plan-project-skill/`

**Files to Load for Execution**:
- `02-resources/architecture-v2.md` - **SINGLE SOURCE OF TRUTH v2.2**
- `02-resources/KIRO-spec.md` - Task patterns reference
- `01-planning/03-plan.md` - Requirements and Correctness Properties
- `01-planning/02-discovery.md` - Dependency analysis

**Output Location**: `00-system/skills/projects/plan-project/`

**Update Resume After Each Section**: Update `resume-context.md` with current_section, tasks_completed

---

## Phase 1: Planning - COMPLETE

- [x] Complete 01-overview.md
- [x] Complete 02-discovery.md (deep analysis v2.2)
- [x] Complete 03-plan.md (EARS requirements v2.3)
- [x] Complete 04-steps.md (KIRO task patterns v2.3)
- [x] Review with stakeholder (REVISED v2.1: steps as enforcement)

---

## Phase 2: Create Template Structure

**Goal**: Create `templates/types/` folder structure with all 8 type templates
**Context**: Load `02-resources/architecture-v2.md` for _type.yaml schema

### 2.1 Create Directory Structure **[REQ-NF-1]**

- [ ] Create `plan-project/templates/types/` directory
- [ ] Create 8 subfolders: build, integration, research, strategy, content, process, skill, generic
- [ ] **CHECKPOINT**: Verify 8 folders exist, ask user if questions arise

### 2.2 Create _type.yaml Files **[REQ-NF-2, REQ-2]**

- [ ] Create `types/build/_type.yaml` - inline discovery, EARS enabled
- [ ] Create `types/integration/_type.yaml` - routes to add-integration skill
- [ ] Create `types/research/_type.yaml` - routes to create-research-project skill
- [ ] Create `types/strategy/_type.yaml` - inline discovery, decision frameworks
- [ ] Create `types/content/_type.yaml` - inline discovery, creative brief
- [ ] Create `types/process/_type.yaml` - inline discovery, workflow optimization
- [ ] Create `types/skill/_type.yaml` - routes to create-skill skill, EARS enabled
- [ ] Create `types/generic/_type.yaml` - minimal inline discovery
- [ ] **CHECKPOINT**: Verify all 8 _type.yaml files have valid schema

### 2.3 Create Templates for Build Type **[REQ-NF-4, REQ-NF-5]**

- [ ] Create `types/build/overview.md` template
- [ ] Create `types/build/discovery.md` template with EARS requirements section
- [ ] Create `types/build/plan.md` template with Correctness Properties section
- [ ] Create `types/build/steps.md` template with checkpoint tasks
- [ ]* Write validation tests for build templates (optional) **[Property 5]**

### 2.4 Create Templates for Skill Type **[REQ-NF-4, REQ-NF-5]**

- [ ] Create `types/skill/overview.md` template
- [ ] Create `types/skill/discovery.md` template with EARS requirements section
- [ ] Create `types/skill/plan.md` template with Correctness Properties section
- [ ] Create `types/skill/steps.md` template with checkpoint tasks
- [ ]* Write validation tests for skill templates (optional) **[Property 5]**

### 2.5 Create Templates for Sub-Skill Types **[REQ-4]**

- [ ] Create `types/integration/` 4 templates (overview, discovery, plan, steps)
- [ ] Create `types/research/` 4 templates (overview, discovery, plan, steps)
- [ ] **CHECKPOINT**: Verify sub-skill routing config in _type.yaml files

### 2.6 Create Templates for Inline Discovery Types **[REQ-5]**

- [ ] Create `types/strategy/` 4 templates
- [ ] Create `types/content/` 4 templates
- [ ] Create `types/process/` 4 templates
- [ ] Create `types/generic/` 4 templates
- [ ] **CHECKPOINT**: Verify all 40 template files exist (8 types × 5 files)

### 2.7 Create Reference Files **[REQ-11, REQ-12]**

- [ ] Create `references/routing-logic.md` - Router decision tree
- [ ] Create `references/entry-mode-contract.md` - Sub-skill data contract
- [ ] Create `references/ears-patterns.md` - EARS templates for Build/Skill
- [ ] Create `references/incose-rules.md` - INCOSE quality rules
- [ ]* Create `references/type-detection.md` - Semantic matching guide (optional)

### 2.8 Update Resume Context

- [ ] Update resume-context.md: current_section: 3, tasks_completed: +19

---

## Phase 3: Rewrite plan-project SKILL.md

**Goal**: Transform SKILL.md into router-only pattern
**Context**: Load current SKILL.md, architecture-v2.md, gap analysis from 02-discovery.md

### 3.1 Preserve Existing Sections **[REQ-1]**

- [ ] Copy YAML frontmatter (lines 1-4)
- [ ] Copy Onboarding Awareness section (lines 6-40)
- [ ] Copy Mode Detection Logic (lines 118-135)
- [ ] Copy Error Handling (lines 314-337)
- [ ] Copy Why This Design rationale (lines 340-367)

### 3.2 Rewrite Core Workflow **[REQ-2, REQ-6]**

- [ ] Replace Critical Execution Requirements with router sequence
- [ ] Add semantic type detection from _type.yaml descriptions
- [ ] Add discovery → mental models → re-discovery flow
- [ ] Add explicit bash commands for sub-skill loading **[REQ-4]**
- [ ] Add template reference paths for inline discovery **[REQ-5]**
- [ ] **CHECKPOINT**: Verify workflow matches architecture-v2.md §Full Flow

### 3.3 Add New Sections **[REQ-10, REQ-11]**

- [ ] Add Router Logic section with decision tree
- [ ] Add Sub-Skill Loading section with bash commands
- [ ] Add Entry Mode Contract reference
- [ ] Add Template References section
- [ ] Add resume-context.md update instructions at each phase

### 3.4 Update Resources Section **[REQ-NF-1]**

- [ ] Update scripts/ to reference init_project.py with --type flag
- [ ] Add templates/types/ structure documentation
- [ ] Update references/ with new files
- [ ]* Write integration tests for router workflow (optional) **[Property 1, Property 2]**

### 3.5 Update Supporting Files

- [ ] Update `references/workflows.md` for template-based flow
- [ ] Update `references/project-types.md` with skill type **[REQ-NF-3]**
- [ ] **CHECKPOINT**: Verify SKILL.md < 400 lines (router should be concise)

### 3.6 Update Resume Context

- [ ] Update resume-context.md: current_section: 4, tasks_completed: +15

---

## Phase 4: Update Specialized Skills

**Goal**: Add entry_mode handling to sub-skills
**Context**: Load current add-integration, create-research-project, create-skill SKILLs

### 4.1 Update add-integration **[REQ-12, REQ-15]**

- [ ] Add entry_mode check at workflow start (after Step 0)
- [ ] Add conditional: IF entry_mode=from_router THEN skip Steps 1, 6
- [ ] Add: write findings to `{project_path}/01-planning/02-discovery.md`
- [ ] Add deprecation notice for direct invocation
- [ ] Add instruction: "Use `plan project` for new integrations"
- [ ]* Write test for entry_mode behavior (optional) **[Property 3]**

### 4.2 Update create-research-project **[REQ-12, REQ-15]**

- [ ] Add entry_mode check at workflow start
- [ ] Add conditional: IF entry_mode=from_router THEN skip Step 1
- [ ] Add: write findings to `{project_path}/01-planning/02-discovery.md`
- [ ] Add deprecation notice for direct invocation
- [ ] Add instruction: "Use `plan project` for new research"
- [ ]* Write test for entry_mode behavior (optional) **[Property 3]**

### 4.3 Update create-skill **[REQ-12, REQ-15]**

- [ ] Add entry_mode check at workflow start
- [ ] Add conditional: IF entry_mode=from_router THEN skip project creation
- [ ] Add: write findings to `{project_path}/01-planning/02-discovery.md`
- [ ] Add deprecation notice for direct invocation
- [ ] Add instruction: "Use `plan project` for new skills"
- [ ]* Write test for entry_mode behavior (optional) **[Property 3]**
- [ ] **CHECKPOINT**: Verify all 3 skills have entry_mode handling

### 4.4 Update SessionStart Hook (if needed) **[REQ-13]**

- [ ] Add sub_skill field reading from resume-context.md
- [ ] Add routing: WHEN sub_skill present, reload that skill instead of project
- [ ] Add sub_skill_step handling for workflow position
- [ ]* Write test for sub_skill resume behavior (optional) **[Property 4]**

### 4.5 Update Resume Context

- [ ] Update resume-context.md: current_section: 5, tasks_completed: +14

---

## Phase 5: Testing & Validation

**Goal**: Verify all flows work with mandatory router
**Context**: All implementation complete

### 5.1 Test Type Detection **[Property 1, Property 6]**

- [ ] Test: "plan project for slack integration" → detects integration
- [ ] Test: "plan project for ontology research" → detects research
- [ ] Test: "plan project for new feature" → detects build
- [ ] Test: "plan project for new skill" → detects skill
- [ ] Test: "plan project for content calendar" → detects content
- [ ] Test: "plan project for workflow automation" → detects process
- [ ]* Run property-based tests with hypothesis (optional)

### 5.2 Test Discovery Flow **[Property 2]**

- [ ] Test: Integration creates 02-discovery.md with API findings
- [ ] Test: Research creates 02-discovery.md with paper findings
- [ ] Test: Build creates 02-discovery.md with EARS requirements
- [ ] Test: Skill creates 02-discovery.md with EARS requirements
- [ ] **CHECKPOINT**: Verify discovery always completes before mental models

### 5.3 Test Sub-Skill Contract **[Property 3]**

- [ ] Test: Router passes entry_mode=from_router to add-integration
- [ ] Test: Router passes project_path to add-integration
- [ ] Test: add-integration skips project creation when entry_mode=from_router
- [ ] Test: add-integration writes to provided project_path
- [ ]* Repeat tests for create-research-project and create-skill (optional)

### 5.4 Test Resume Context **[Property 4]**

- [ ] Test: Compaction preserves sub-skill state
- [ ] Test: Resume reloads correct context after compaction
- [ ] Test: Phase transitions update resume-context.md correctly
- [ ] **CHECKPOINT**: Verify state consistency across 3 simulated compactions

### 5.5 Test Template Structure **[Property 5]**

- [ ] Verify: All 8 type folders exist
- [ ] Verify: Each folder has exactly 5 files
- [ ] Verify: _type.yaml schema is valid for all types
- [ ] Verify: Build/Skill discovery.md has EARS section
- [ ] Verify: Build/Skill plan.md has Correctness Properties section

### 5.6 Test Deprecation Notices **[REQ-15]**

- [ ] Test: Direct "add integration" shows deprecation notice
- [ ] Test: Direct "create research project" shows deprecation notice
- [ ] Test: Direct "create skill" shows deprecation notice

### 5.7 Final Validation

- [ ] **CHECKPOINT**: All tests pass, ask user if questions arise
- [ ] Update resume-context.md: current_phase: "complete"
- [ ] Update 01-overview.md success criteria checkboxes

---

## Summary

| Phase | Tasks | Optional | Checkpoints |
|-------|-------|----------|-------------|
| Phase 1 | 5 | 0 | 0 |
| Phase 2 | 19 | 3 | 5 |
| Phase 3 | 15 | 1 | 2 |
| Phase 4 | 14 | 4 | 1 |
| Phase 5 | 20 | 2 | 4 |
| **Total** | **73** | **10** | **12** |

**Estimated Time**: ~4 hours AI time

**Key Files Created**:
- 40 template files (8 types × 5 files)
- 5 reference files
- 1 rewritten SKILL.md
- 3 updated sub-skill SKILLs

**Requirements Coverage**:
- All 15 functional requirements (REQ-1 to REQ-15) mapped to tasks
- All 5 non-functional requirements (REQ-NF-1 to REQ-NF-5) mapped to tasks
- All 6 correctness properties have validation tasks

---

*Mark tasks complete with [x] as you finish them*
*Optional tasks marked with `*` can be skipped for faster MVP*
