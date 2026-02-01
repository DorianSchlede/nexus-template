# {{build_name}} - Execution Steps

**Build Type**: Skill
**Status**: Planning

---

## Context Requirements

**Build Location**: `02-builds/{{build_id}}/`

**Files to Load for Execution**:
- `01-planning/02-discovery.md` - Skill requirements
- `01-planning/03-plan.md` - Workflow design

**Output Location**: `03-skills/{{skill_slug}}/` or `00-system/skills/{{category}}/{{skill_slug}}/`

**Update Resume After Each Section**: Update `resume-context.md` with current_section, tasks_completed

---

## Phase 1: Setup

**Goal**: Create skill directory structure
**Context**: Load 02-discovery.md for anatomy

- [ ] Create skill folder at output location **[REQ-{{number}}]**
- [ ] Create scripts/ subfolder (if needed)
- [ ] Create references/ subfolder (if needed)
- [ ] **CHECKPOINT**: Directory structure ready

---

## Phase 2: SKILL.md Creation

**Goal**: Write the main workflow definition
**Context**: Load 03-plan.md workflow outline

### 2.1 Write SKILL.md Header **[REQ-{{number}}]**

- [ ] Add YAML frontmatter (name, description)
- [ ] Write Purpose section
- [ ] Add trigger phrases

### 2.2 Write Workflow Steps **[REQ-{{number}}]**

- [ ] Write Step 1: {{description}}
- [ ] Write Step 2: {{description}}
- [ ] Write Step 3: {{description}}
- [ ] **CHECKPOINT**: Workflow is complete and under 200 lines

---

## Phase 3: Supporting Resources

**Goal**: Create scripts and references
**Context**: SKILL.md complete

- [ ] Create {{script_name}}.py (if needed) **[REQ-{{number}}]**
- [ ]* Write unit tests for scripts (optional)
- [ ] Create {{reference}}.md (if needed)
- [ ] **CHECKPOINT**: All resources in place

---

## Phase 4: Integration

**Goal**: Register skill and verify it loads
**Context**: All files created

- [ ] Verify skill loads correctly via nexus-loader.py
- [ ] Test trigger phrases work
- [ ] **CHECKPOINT**: Skill invocable

---

## Phase 5: Validation

**Goal**: Verify against requirements
**Context**: Skill integrated

- [ ] Verify all functional requirements met
- [ ] Verify all non-functional requirements met
- [ ] Run through manual test scenarios
- [ ] **CHECKPOINT**: All tests pass

---

## Phase 6: Finalization

**Goal**: Complete build
**Context**: Validation passed

- [ ] Update resume-context.md: current_phase: "complete"
- [ ] Update 01-overview.md success criteria checkboxes

---

## Summary

| Phase | Tasks | Optional | Checkpoints |
|-------|-------|----------|-------------|
| Phase 1 | {{count}} | 0 | 1 |
| Phase 2 | {{count}} | 0 | 1 |
| Phase 3 | {{count}} | {{count}} | 1 |
| Phase 4 | {{count}} | 0 | 1 |
| Phase 5 | {{count}} | 0 | 1 |
| Phase 6 | {{count}} | 0 | 0 |
| **Total** | **{{total}}** | **{{optional}}** | **{{checkpoints}}** |

---

*Mark tasks complete with [x] as you finish them*
*Optional tasks marked with `*` can be skipped for faster MVP*
