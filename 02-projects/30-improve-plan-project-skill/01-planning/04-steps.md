# Improve Plan-Project Skill - Execution Steps

**Last Updated**: 2026-01-07
**Status**: REVISED v2.4 - Simplified Skill Invocation
**Project Type**: Build

---

## Context Requirements

**Project Location**: `02-projects/30-improve-plan-project-skill/`

**Files to Load for Execution**:
- `02-resources/architecture-v2.md` - **SINGLE SOURCE OF TRUTH v2.3**
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

## Phase 2: Create Template Structure - COMPLETE

**Goal**: Create `templates/types/` folder structure with all 8 type templates
**Context**: Load `02-resources/architecture-v2.md` for _type.yaml schema

### 2.1 Create Directory Structure **[REQ-NF-1]**

- [x] Create `plan-project/templates/types/` directory
- [x] Create 8 subfolders: build, integration, research, strategy, content, process, skill, generic
- [x] **CHECKPOINT**: Verify 8 folders exist, ask user if questions arise

### 2.2 Create _type.yaml Files **[REQ-NF-2, REQ-2]**

- [x] Create `types/build/_type.yaml` - inline discovery, EARS enabled
- [x] Create `types/integration/_type.yaml` - routes to add-integration skill
- [x] Create `types/research/_type.yaml` - routes to create-research-project skill
- [x] Create `types/strategy/_type.yaml` - inline discovery, decision frameworks
- [x] Create `types/content/_type.yaml` - inline discovery, creative brief
- [x] Create `types/process/_type.yaml` - inline discovery, workflow optimization
- [x] Create `types/skill/_type.yaml` - routes to create-skill skill, EARS enabled
- [x] Create `types/generic/_type.yaml` - minimal inline discovery
- [x] **CHECKPOINT**: Verify all 8 _type.yaml files have valid schema

### 2.3 Create Templates for Build Type **[REQ-NF-4, REQ-NF-5]**

- [x] Create `types/build/overview.md` template
- [x] Create `types/build/discovery.md` template with EARS requirements section
- [x] Create `types/build/plan.md` template with Correctness Properties section
- [x] Create `types/build/steps.md` template with checkpoint tasks
- [ ]* Write validation tests for build templates (optional) **[Property 5]**

### 2.4 Create Templates for Skill Type **[REQ-NF-4, REQ-NF-5]**

- [x] Create `types/skill/overview.md` template
- [x] Create `types/skill/discovery.md` template with EARS requirements section
- [x] Create `types/skill/plan.md` template with Correctness Properties section
- [x] Create `types/skill/steps.md` template with checkpoint tasks
- [ ]* Write validation tests for skill templates (optional) **[Property 5]**

### 2.5 Create Templates for Sub-Skill Types **[REQ-4]**

- [x] Create `types/integration/` 4 templates (overview, discovery, plan, steps)
- [x] Create `types/research/` 4 templates (overview, discovery, plan, steps)
- [x] **CHECKPOINT**: Verify sub-skill routing config in _type.yaml files

### 2.6 Create Templates for Inline Discovery Types **[REQ-5]**

- [x] Create `types/strategy/` 4 templates
- [x] Create `types/content/` 4 templates
- [x] Create `types/process/` 4 templates
- [x] Create `types/generic/` 4 templates
- [x] **CHECKPOINT**: Verify all 40 template files exist (8 types × 5 files)

### 2.7 Create Reference Files **[REQ-11, REQ-12]**

- [x] Create `references/routing-logic.md` - Router decision tree
- [x] Create `references/ears-patterns.md` - EARS templates for Build/Skill
- [x] Create `references/incose-rules.md` - INCOSE quality rules
- [ ]* Create `references/type-detection.md` - Semantic matching guide (optional)

### 2.8 Update Resume Context

- [x] Update resume-context.md: current_section: 3, tasks_completed: +19

---

## Phase 3: Rewrite plan-project SKILL.md - COMPLETE

**Goal**: Transform SKILL.md into router-only pattern
**Context**: Load current SKILL.md, architecture-v2.md, gap analysis from 02-discovery.md

### 3.1 Preserve Existing Sections **[REQ-1]**

- [x] Copy YAML frontmatter (lines 1-4)
- [x] Copy Onboarding Awareness section (lines 6-40)
- [x] Copy Mode Detection Logic (lines 118-135)
- [x] Copy Error Handling (lines 314-337)
- [x] Copy Why This Design rationale (lines 340-367)

### 3.2 Rewrite Core Workflow **[REQ-2, REQ-6]**

- [x] Replace Critical Execution Requirements with router sequence
- [x] Add semantic type detection from _type.yaml descriptions
- [x] Add discovery → mental models → re-discovery flow
- [x] Add explicit bash commands for sub-skill loading **[REQ-4]**
- [x] Add template reference paths for inline discovery **[REQ-5]**
- [x] **CHECKPOINT**: Verify workflow matches architecture-v2.md §Full Flow

### 3.3 Add New Sections **[REQ-10, REQ-11]**

- [x] Add Router Logic section with decision tree
- [x] Add Sub-Skill Loading section with bash commands
- [x] Add Entry Mode Contract reference
- [x] Add Template References section
- [x] Add resume-context.md update instructions at each phase

### 3.4 Update Resources Section **[REQ-NF-1]**

- [x] Update scripts/ to reference init_project.py with --type flag
- [x] Add templates/types/ structure documentation
- [x] Update references/ with new files
- [ ]* Write integration tests for router workflow (optional) **[Property 1, Property 2]**

### 3.5 Update Supporting Files

- [x] Update `references/workflows.md` for template-based flow
- [x] Update `references/project-types.md` with skill type **[REQ-NF-3]**
- [x] **CHECKPOINT**: Verify SKILL.md < 400 lines (365 lines - PASS)

### 3.6 Update Resume Context

- [x] Update resume-context.md: current_section: 4, tasks_completed: +15

---

## Phase 4: Add Deprecation Notices (v2.4 Simplified) - COMPLETE

**Goal**: Add deprecation notices to skills (no entry_mode needed)
**Context**: Load current add-integration, create-research-project, create-skill SKILLs

### 4.1 Update add-integration **[REQ-13]**

- [x] Add deprecation notice at workflow start
- [x] Add instruction: "Use `plan project` for new integrations"
- [x] **CHECKPOINT**: Verify deprecation notice displays correctly

### 4.2 Update create-research-project **[REQ-13]**

- [x] Add deprecation notice at workflow start
- [x] Add instruction: "Use `plan project` for new research"

### 4.3 Update create-skill **[REQ-13]**

- [x] Add deprecation notice at workflow start
- [x] Add instruction: "Use `plan project` for new skills"
- [x] **CHECKPOINT**: Verify all 3 skills have deprecation notice

### 4.4 Update Resume Context

- [x] Update resume-context.md: current_section: 5, tasks_completed: +7

**NOTE**: Hook enforcement DEFERRED to future project.

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

### 5.3 Test Skill Discovery Output **[Property 3]**

- [ ] Test: add-integration writes findings to project's 02-discovery.md
- [ ] Test: create-research-project writes findings to project's 02-discovery.md
- [ ] Test: create-skill writes findings to project's 02-discovery.md

### 5.4 Test Resume Context **[Property 4]**

- [ ] Test: Resume reloads correct context after compaction
- [ ] Test: Phase transitions update resume-context.md correctly
- [ ] **CHECKPOINT**: Verify state consistency across resume cycle

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

## Summary (v2.4 Simplified)

| Phase | Tasks | Optional | Checkpoints |
|-------|-------|----------|-------------|
| Phase 1 | 5 | 0 | 0 |
| Phase 2 | 19 | 3 | 5 |
| Phase 3 | 15 | 1 | 2 |
| Phase 4 | 7 | 0 | 2 |
| Phase 5 | 17 | 1 | 4 |
| **Total** | **63** | **5** | **13** |

**Estimated Time**: ~3 hours AI time

**Key Files Created**:
- 40 template files (8 types × 5 files)
- 4 reference files
- 1 rewritten SKILL.md
- 3 skills with deprecation notices

**Requirements Coverage**:
- All 13 functional requirements (REQ-1 to REQ-13) mapped to tasks
- All 5 non-functional requirements (REQ-NF-1 to REQ-NF-5) mapped to tasks
- All 6 correctness properties have validation tasks

**NOTE**: Hook enforcement DEFERRED to future project.

---

*Mark tasks complete with [x] as you finish them*
*Optional tasks marked with `*` can be skipped for faster MVP*
