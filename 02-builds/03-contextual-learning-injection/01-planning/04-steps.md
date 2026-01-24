# {{build_name}} - Execution Steps

**Build Type**: Build
**Status**: Planning

---

## Context Requirements

**Build Location**: `02-builds/{{build_id}}/`

**Files to Load for Execution**:
- `01-planning/02-discovery.md` - Requirements
- `01-planning/03-plan.md` - Approach and decisions

**Output Location**: {{output_location}}

**Update Resume After Each Section**: Update `resume-context.md` with current_section, tasks_completed

---

## Phase 1: Setup

**Goal**: Prepare environment and validate requirements
**Context**: Load 02-discovery.md

- [ ] Verify all dependencies are available **[REQ-{{number}}]**
- [ ] Create output directory structure
- [ ] **CHECKPOINT**: Environment ready, ask user if questions arise

---

## Phase 2: Core Implementation

**Goal**: Implement core functionality
**Context**: Load 03-plan.md approach section

### 2.1 {{section_name}} **[REQ-{{number}}]**

- [ ] {{task_1}}
- [ ] {{task_2}}
- [ ]* Write unit tests (optional) **[Property {{number}}]**
- [ ] **CHECKPOINT**: Verify {{section_name}} works correctly

### 2.2 {{section_name}} **[REQ-{{number}}]**

- [ ] {{task_1}}
- [ ] {{task_2}}
- [ ]* Write unit tests (optional) **[Property {{number}}]**

---

## Phase 3: Integration

**Goal**: Connect components and verify end-to-end
**Context**: All components implemented

- [ ] Wire up components **[REQ-{{number}}]**
- [ ] Verify integration points
- [ ] **CHECKPOINT**: End-to-end flow works

---

## Phase 4: Validation

**Goal**: Verify against requirements and properties
**Context**: Implementation complete

- [ ] Verify all functional requirements met
- [ ] Verify all non-functional requirements met
- [ ] Run property-based tests **[Property 1, Property 2]**
- [ ] **CHECKPOINT**: All tests pass, ask user if questions arise

---

## Phase 5: Finalization

**Goal**: Complete build and update state
**Context**: All validation passed

- [ ] Update documentation if needed
- [ ] Update resume-context.md: current_phase: "complete"
- [ ] Update 01-overview.md success criteria checkboxes

---

## Summary

| Phase | Tasks | Optional | Checkpoints |
|-------|-------|----------|-------------|
| Phase 1 | {{count}} | 0 | 1 |
| Phase 2 | {{count}} | {{count}} | {{count}} |
| Phase 3 | {{count}} | 0 | 1 |
| Phase 4 | {{count}} | 0 | 1 |
| Phase 5 | {{count}} | 0 | 0 |
| **Total** | **{{total}}** | **{{optional}}** | **{{checkpoints}}** |

---

*Mark tasks complete with [x] as you finish them*
*Optional tasks marked with `*` can be skipped for faster MVP*
