# Documentation Sync - Execution Steps

**Build Type**: Content (Documentation Update)
**Status**: Ready for Execution

---

## Context Requirements

**Build Location**: `02-builds/01-documentation-sync-framework-scan/`

**Files to Load for Execution**:
- `01-planning/02-discovery.md` - Discrepancy analysis
- `01-planning/03-plan.md` - Update approach

**Target Files**:
- `00-system/documentation/product-overview.md`
- `00-system/documentation/framework-overview.md`
- `00-system/documentation/ux-onboarding-philosophy.md`

---

## Phase 1: Update product-overview.md

**Goal**: Update user-facing overview with current system state
**Context**: Use discovery.md findings

- [ ] Update title from "Nexus-v3" to "Nexus" (remove version)
- [ ] Update 5-folder structure diagram (show numbered planning files)
- [ ] Update build example structure (01-overview.md, 02-discovery.md, etc.)
- [ ] Add hooks mention in "How It Works" section
- [ ] Update "System Skills" count in skills section
- [ ] Add integrations ecosystem mention (8 integrations, 119 skills)
- [ ] Update session pattern to reflect hooks-based loading
- [ ] Remove outdated CLI example (`nexus-loader.py --startup` → `nexus-load`)
- [ ] **CHECKPOINT**: product-overview.md updated

---

## Phase 2: Update framework-overview.md

**Goal**: Update technical architecture documentation
**Context**: Use discovery.md findings + CLI audit

- [ ] Update system skills count (change "25" to "152 across 7 categories")
- [ ] Update mental models count (change "59" to "90+ across 12 categories")
- [ ] Update build structure section (numbered files: 01-overview, 02-discovery, 03-plan, 04-steps)
- [ ] Add resume-context.md to build structure documentation
- [ ] Update CLI commands section with full command list and flags
- [ ] Add hooks system section (6 hooks: SessionStart, SessionEnd, etc.)
- [ ] Update onboarding skills list (6 learning skills)
- [ ] Update integration skills section (8 integrations with counts)
- [ ] Update Version footer (V4.0 → V5.0, date → 2026-02-01)
- [ ] Fix file paths where outdated (nexus-loader.py → nexus-load)
- [ ] **CHECKPOINT**: framework-overview.md updated

---

## Phase 3: Update ux-onboarding-philosophy.md

**Goal**: Update UX design standards document
**Context**: Verify references still accurate

- [ ] Update "Last Updated" date in header (2025-11-04 → 2026-02-01)
- [ ] Review Build 00 V2.0 case study for accuracy
- [ ] Check if "4 builds" onboarding references match current system
- [ ] Verify metrics in Measurement Framework still apply
- [ ] Update any deprecated skill/feature references
- [ ] **CHECKPOINT**: ux-onboarding-philosophy.md updated

---

## Phase 4: Validation

**Goal**: Verify all changes are accurate
**Context**: Cross-reference with actual system

- [ ] Run `nexus-load --list-skills` and verify count matches docs
- [ ] Verify CLI commands documented exist in pyproject.toml
- [ ] Check folder structure in 02-builds/active/ matches documented structure
- [ ] Read orchestrator.md to verify routing rules match docs
- [ ] **CHECKPOINT**: All documentation validated

---

## Phase 5: Finalization

**Goal**: Complete build
**Context**: All docs updated and validated

- [ ] Update resume-context.md: current_phase: "complete"
- [ ] Mark success criteria in 01-overview.md as complete
- [ ] Create summary of changes made

---

## Summary

| Phase | Tasks | Checkpoints |
|-------|-------|-------------|
| Phase 1: product-overview | 9 | 1 |
| Phase 2: framework-overview | 11 | 1 |
| Phase 3: ux-onboarding | 6 | 1 |
| Phase 4: Validation | 5 | 1 |
| Phase 5: Finalization | 3 | 0 |
| **Total** | **34** | **4** |

---

*Mark tasks complete with [x] as you finish them*
