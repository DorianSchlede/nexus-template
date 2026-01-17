# {{build_name}} - Execution Steps

**Build Type**: Integration
**Status**: Planning

---

## Context Requirements

**Build Location**: `02-builds/{{build_id}}/`

**Files to Load for Execution**:
- `01-planning/02-discovery.md` - API configuration
- `02-resources/integration-config.json` - Generated config

**Output Location**: `03-skills/{{service_slug}}/`

---

## Phase 1: Discovery (via add-integration)

**Goal**: Discover API and select endpoints
**Skill**: add-integration

- [ ] Load add-integration skill
- [ ] Perform API documentation search
- [ ] Parse and cache API endpoints
- [ ] User selects endpoints to implement
- [ ] Generate integration-config.json
- [ ] **CHECKPOINT**: Config file ready

---

## Phase 2: Scaffolding

**Goal**: Generate integration structure
**Context**: integration-config.json ready

- [ ] Run scaffold_integration.py with config
- [ ] Verify master skill created
- [ ] Verify connect skill created
- [ ] Verify operation skills created
- [ ] **CHECKPOINT**: All skills scaffolded

---

## Phase 3: Configuration

**Goal**: Set up authentication
**Context**: Skills scaffolded

- [ ] Add environment variable for API key/token
- [ ] Run connect skill to verify auth
- [ ] **CHECKPOINT**: Authentication works

---

## Phase 4: Validation

**Goal**: Test all operations
**Context**: Auth configured

- [ ] Test each operation skill
- [ ] Verify error handling
- [ ] **CHECKPOINT**: All operations work

---

## Phase 5: Finalization

**Goal**: Complete build
**Context**: Validation passed

- [ ] Update resume-context.md: current_phase: "complete"
- [ ] Update 01-overview.md success criteria checkboxes

---

## Summary

| Phase | Tasks | Checkpoints |
|-------|-------|-------------|
| Phase 1 | 6 | 1 |
| Phase 2 | 5 | 1 |
| Phase 3 | 3 | 1 |
| Phase 4 | 3 | 1 |
| Phase 5 | 2 | 0 |
| **Total** | **19** | **4** |

---

*Mark tasks complete with [x] as you finish them*
