# Improve Add-Integration Skill - Execution Steps

**Last Updated**: 2026-01-07
**Status**: PLANNING COMPLETE
**Approach**: Option 2 - Auto-Execute Scaffold After Config

---

## Context Requirements

**Project Location**: `02-projects/36-improve-add-integration-skill/`

**Files to Load for Execution**:
- `01-planning/01-overview.md` - Purpose, success criteria
- `01-planning/02-discovery.md` - Dependencies, patterns, risks
- `01-planning/03-plan.md` - Approach, decisions
- `01-planning/04-steps.md` - This file (execution tasks)
- `02-resources/audit-add-integration.md` - Full audit (699 lines)
- `02-resources/fix-options-analysis.md` - Implementation details

**Skill Location**: `00-system/skills/system/add-integration/`

**Output Locations**:
- `03-working/` - Work in progress files
- `04-outputs/` - Final deliverables

---

## Phase 1: Planning - COMPLETE

- [x] Complete 01-overview.md (audit findings, success criteria)
- [x] Complete 02-discovery.md (full dependency analysis)
- [x] Complete 03-plan.md (Option 2 approach)
- [x] Complete 04-steps.md (this file)
- [x] Copy resources from Project 30 audits
- [ ] Review with stakeholder

---

## Phase 2: Core Fix - Auto-Execute Scaffold

**Goal**: Make `scaffold_integration.py` actually run during workflow
**Context**: Load `02-resources/fix-options-analysis.md` for implementation details

### 2.1 Update SKILL.md Workflow

- [ ] Read current `add-integration/SKILL.md`
- [ ] Add Step 7.5 after config finalization:
  ```markdown
  ### Step 7.5: Execute Scaffold (AUTOMATIC)

  After config is finalized, IMMEDIATELY execute:

  ```bash
  python 00-system/skills/system/add-integration/scripts/scaffold_integration.py \
    --config {project_path}/02-resources/integration-config.json \
    --output 03-skills/{service_slug}/
  ```

  **DO NOT** proceed until scaffold completes successfully.
  ```
- [ ] Add verification step after scaffold
- [ ] **CHECKPOINT**: Verify SKILL.md workflow is complete

### 2.2 Update Final Message

- [ ] Change final message from "run scaffold manually" to "integration created"
- [ ] Add summary of what was generated:
  ```
  Generated:
  - 03-skills/{service}-master/ (shared resources)
  - 03-skills/{service}-connect/ (entry point)
  - 03-skills/{service}-{operation}/ (per endpoint)
  ```

### 2.3 Add Error Handling

- [ ] Add try/catch around scaffold execution
- [ ] Add rollback instructions if scaffold fails
- [ ] Add "scaffold already ran" detection (check if folders exist)

### 2.4 Update Resume Context

- [ ] Update resume-context.md: current_section: 3, tasks_completed: +8

---

## Phase 3: Merge Components from create-master-skill

**Goal**: Add high-value components missing from add-integration
**Context**: Load `02-resources/merge-from-create-master-skill.md` for details

### 3.1 Add Test Templates

- [ ] Create `add-integration/templates/tests/` directory
- [ ] Copy and adapt `run_tests.py.template`:
  ```python
  def test_config_script_runs():
      script = os.path.join(SCRIPTS_DIR, 'check_{{SERVICE_SLUG}}_config.py')
      result = subprocess.run([sys.executable, script, '--json'],
                            capture_output=True, text=True)
      assert result.returncode in [0, 1]

  def test_api_connection():
      # Test actual API connectivity
      pass
  ```
- [ ] Copy `README.md.template` for tests documentation
- [ ] Update `scaffold_integration.py` to generate tests/ folder

### 3.2 Add Research Checklist

- [ ] Copy `references/research-checklist.md` from create-master-skill
- [ ] Adapt for add-integration workflow (10 search areas):
  1. Official API documentation
  2. Authentication guides
  3. Rate limiting documentation
  4. Pagination patterns
  5. Error response formats
  6. Webhook documentation
  7. SDK/client libraries
  8. API changelog/versioning
  9. Community forums/issues
  10. Example implementations
- [ ] Reference in SKILL.md Step 2 (API research)

### 3.3 Add Master Skill Patterns Doc

- [ ] Copy `references/master-skill-patterns.md`
- [ ] Add to generated master skill's references/
- [ ] Documents DRY architecture, shared resources pattern

### 3.4 Add Resource Discovery Script

- [ ] Copy `templates/discover_resources.py.template`
- [ ] Adapt for integration context
- [ ] Add to scaffold output

### 3.5 Update Resume Context

- [ ] Update resume-context.md: current_section: 4, tasks_completed: +12

---

## Phase 4: Testing & Validation

**Goal**: Verify the fix works with a real API

### 4.1 Test with Public API

- [ ] Run `plan-project` with "add integration for JSONPlaceholder API"
- [ ] Verify type detection routes to add-integration
- [ ] Verify scaffold executes automatically
- [ ] Verify all folders created:
  - [ ] `03-skills/jsonplaceholder-master/`
  - [ ] `03-skills/jsonplaceholder-connect/`
  - [ ] `03-skills/jsonplaceholder-{operation}/` (at least one)
- [ ] **CHECKPOINT**: Integration structure complete

### 4.2 Test Generated Skills

- [ ] Run `check_jsonplaceholder_config.py --json`
- [ ] Verify connect skill loads correctly
- [ ] Test one operation skill

### 4.3 Test Edge Cases

- [ ] Test with invalid API URL
- [ ] Test with API requiring auth
- [ ] Test scaffold failure handling
- [ ] Test "already exists" detection

### 4.4 Document Results

- [ ] Create test report in `03-working/test-report.md`
- [ ] Update success criteria checkboxes in 01-overview.md

### 4.5 Update Resume Context

- [ ] Update resume-context.md: current_phase: "complete"

---

## Phase 5: Final Cleanup

- [ ] Update add-integration/SKILL.md version/date
- [ ] Archive working files if needed
- [ ] Update project status to COMPLETE
- [ ] Commit changes with descriptive message

---

## Summary

| Phase | Tasks | Status |
|-------|-------|--------|
| Phase 1: Planning | 6 | COMPLETE |
| Phase 2: Core Fix | 8 | PENDING |
| Phase 3: Merge Components | 12 | PENDING |
| Phase 4: Testing | 10 | PENDING |
| Phase 5: Cleanup | 4 | PENDING |
| **Total** | **40** | |

**Estimated Time**: ~10 hours AI time

---

## Notes

**Current blockers**: None - ready to execute

**Dependencies**:
- Project 30 must be complete (plan-project router) for end-to-end testing
- No external dependencies for core fix

**Key Files to Modify**:
| File | Changes |
|------|---------|
| `add-integration/SKILL.md` | Add Step 7.5, update final message |
| `add-integration/scripts/scaffold_integration.py` | Add error handling, tests generation |
| `add-integration/templates/` | Add tests/, research-checklist.md |

---

*Mark tasks complete with [x] as you finish them*
