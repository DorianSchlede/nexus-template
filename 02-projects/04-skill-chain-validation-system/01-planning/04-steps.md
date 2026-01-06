# Skill-Chain Validation System - Execution Steps

**Last Updated**: 2025-12-27

**IMPORTANT**: This file tracks project progress. Mark tasks complete with [x] as you finish them.

---

## Phase 1: Setup & Planning

- [x] Complete overview.md
- [x] Complete plan.md
- [x] Complete steps.md
- [ ] Review planning documents

---

## Phase 2: Contract Schema Design

- [ ] Define YAML contract format structure
- [ ] Document `skills` array (id, phase, produces, requires)
- [ ] Document `produces` output spec (path, required, validates)
- [ ] Document `gates` definition (checks array)
- [ ] Document `schemas` for field validation
- [ ] Create `references/contract-schema.md`
- [ ] Create `references/validation-rules.md`

---

## Phase 3: Research Pipeline Contract

- [ ] Read create-research-project SKILL.md for outputs
- [ ] Read execute-research-project SKILL.md for outputs
- [ ] Scan 02-ontologies-research for actual file structure
- [ ] Map Phase 1 outputs to contract format
- [ ] Map Phase 2 outputs to contract format
- [ ] Define selection-gate conditions
- [ ] Define readiness-gate conditions
- [ ] Define analysis-gate conditions
- [ ] Create `contracts/research-pipeline.yaml`

---

## Phase 4: Core Validation Scripts

- [ ] Create `scripts/contract_loader.py`
  - [ ] Load YAML contract by name
  - [ ] Validate contract structure
  - [ ] Return parsed contract object
- [ ] Create `scripts/validate_chain.py`
  - [ ] Accept project path + chain name
  - [ ] Check file existence for each output
  - [ ] Validate YAML fields where specified
  - [ ] Evaluate gate conditions
  - [ ] Return validation results object
- [ ] Create `scripts/report_generator.py`
  - [ ] Generate markdown report from results
  - [ ] Include pass/fail/pending status
  - [ ] Include actionable recommendations
- [ ] Add CLI interface (`--validate`, `--chain`, `--project`)

---

## Phase 5: History Tracking

- [ ] Design history JSON schema
- [ ] Implement save_history() function
- [ ] Implement load_history() function
- [ ] Add `--history` CLI command to view past runs
- [ ] Add trend detection (optional)

---

## Phase 6: Test on Ontologies Project

- [ ] Run validation on 02-ontologies-research
- [ ] Compare report to actual project state
- [ ] Fix any contract mismatches
- [ ] Document findings

---

## Phase 7: Fix Workflow

- [ ] Create `scripts/fix_planner.py`
  - [ ] Step 1: Research - analyze what's wrong
  - [ ] Step 2: Plan - propose fixes
  - [ ] Step 3: Execute - apply fixes
- [ ] Integrate with main CLI (`--fix`)
- [ ] Test fix workflow on identified issues

---

## Phase 8: Package as Skill

- [ ] Create `03-skills/validate-skill-chain/` folder
- [ ] Move scripts to skill folder
- [ ] Move contracts to skill folder
- [ ] Create SKILL.md with workflow
- [ ] Test skill invocation ("validate research pipeline")
- [ ] Update skill catalog if needed

---

## Phase 9: Finalization

- [ ] Final testing of complete workflow
- [ ] Update project overview.md status to COMPLETE
- [ ] Archive project or mark complete

---

## Notes

**Current blockers**: None

**Dependencies**:
- Ontologies project at 29% - good test case for partial validation

---

*Mark tasks complete with [x] as you finish them*
