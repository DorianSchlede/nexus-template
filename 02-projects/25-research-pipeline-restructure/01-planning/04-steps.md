# Discovery Step Implementation - Steps

**Last Updated**: 2026-01-04

---

## Phase 1: Planning (COMPLETE)

- [x] Complete overview.md, plan.md, steps.md
- [x] Execute discovery → 01-planning/discovery.md
- [x] Review with stakeholder

---

## Phase 2: Implementation (COMPLETE)

### 2.1 Create Template
- [x] Create `discovery-template.md` in `create-project/scripts/templates/`
  - 3 sections: Dependencies, Patterns, Risks
  - Time-box header: "5-15 min max"
  - Format for plan.md Dependencies auto-population

### 2.2 Merge workflows into SKILL.md
- [x] Merge workflows.md content into create-project SKILL.md
- [x] Add Step 4.5: Discovery (after init_project.py)
- [x] Add proposal prompt with skip option
- [x] Document discovery → plan.md Dependencies flow
- [x] Move workflows.md to TRASH/

### 2.3 Update SKILL.md
- [x] Add discovery to CRITICAL EXECUTION REQUIREMENTS
- [x] Document always-propose + skip behavior

---

## Phase 3: Testing (COMPLETE)

- [x] Happy path: Create project with discovery, verify Dependencies populated
- [x] Skip path: "skip"/"no" proceeds to overview (02-discovery.md remains template)
- [x] Edge case: Empty discovery still creates file (via init_project.py)

---

## Phase 4: Finalize (COMPLETE)

- [x] Final review + test complete workflow
- [x] Mark project COMPLETE

---

*Mark tasks [x] as you finish*
