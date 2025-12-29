# Create Skill-Chain Skill - Execution Steps

**Last Updated**: 2025-12-27

**IMPORTANT**: This file tracks project progress. Mark tasks complete with [x] as you finish them.

**CRITICAL**: Read `02-resources/_handover.md` FIRST for full context!

---

## ⚠️ ARCHITECTURE UPDATE (2025-12-27)

User requested: **"A skill chain should NOT be a single skill chain skill, but MULTIPLE skills in a big one. NESTED SKILLS actually."**

This changes everything. A skill-chain is now a **NAMESPACE** containing multiple nested skills, not a single skill.

---

## Phase 0: MIGRATE RESEARCH PIPELINE ⭐ (FIRST PRIORITY)

**Proves the nested pattern before building generators.**

### 0.1 Create Research Pipeline Namespace
- [x] Create `03-skills/research-pipeline/` parent folder
- [x] Create `orchestrators/` subfolder
- [x] Create `skills/` subfolder
- [x] Create `shared/` subfolder
- [x] Create `validation/` subfolder

### 0.2 Create Parent Router Skill
- [x] Create `03-skills/research-pipeline/SKILL.md` (parent router)
  - [x] Add YAML frontmatter with `type: skill-chain`
  - [x] Add routing table for child skills
  - [x] Add documentation links
  - [x] Add child skill references

### 0.3 Create Chain Contract
- [x] Create `03-skills/research-pipeline/_chain.yaml`
  - [x] Define structure section (type: nested, subfolders)
  - [x] Define all skills with paths
  - [x] Define gates
  - [x] Define schemas

### 0.4 Move Orchestrators
- [x] Move `03-skills/create-research-project/` → `research-pipeline/orchestrators/`
- [x] Move `03-skills/execute-research-project/` → `research-pipeline/orchestrators/`
- [ ] Update internal references in SKILL.md files

### 0.5 Move Sub-Skills
- [x] Move `03-skills/paper-search/` → `research-pipeline/skills/`
- [x] Move `03-skills/pdf-preprocess/` → `research-pipeline/skills/`
- [x] Move `03-skills/paper-analyze/` → `research-pipeline/skills/`
- [x] Move `03-skills/paper-synthesize/` → `research-pipeline/skills/`
- [x] Move `03-skills/paper-query/` → `research-pipeline/skills/`
- [x] Move `03-skills/paper-manage/` → `research-pipeline/skills/`
- [ ] Update internal references in SKILL.md files

### 0.6 Move Shared Methodologies
- [x] Move `03-skills/paper-analyze-core/` → `research-pipeline/shared/`
- [ ] Update subagent prompts to use new path

### 0.7 Move Validation Scripts
- [x] Copy `paper-analyze/scripts/validate_analysis.py` → `research-pipeline/validation/`
- [x] Copy `paper-synthesize/scripts/validate_synthesis.py` → `research-pipeline/validation/`
- [ ] Update import paths in scripts

### 0.8 Update All References
- [ ] Update orchestrator SKILL.md sub-skill references
- [ ] Update skill descriptions with new paths
- [ ] Update any hardcoded paths in scripts
- [ ] Update references/ folder paths

### 0.9 Generate Documentation
- [x] Create `03-skills/research-pipeline/_index.md`
  - [x] Add Mermaid diagram
  - [x] Add skill inventory
  - [x] Add usage instructions

### 0.10 Test Migration
- [ ] Verify parent SKILL.md loads correctly
- [ ] Verify orchestrator skills work
- [ ] Verify sub-skills are callable
- [ ] Verify validation scripts run
- [ ] Test full research pipeline flow

---

## Phase 1: Context Loading (COMPLETED)

- [x] Create project structure
- [x] Write handover document (`02-resources/_handover.md`)
- [x] Complete overview.md
- [x] Complete plan.md
- [x] Complete steps.md
- [x] Read all files listed in handover "CRITICAL FILES TO READ"
  - [x] Read `03-skills/create-research-project/SKILL.md`
  - [x] Read `03-skills/execute-research-project/SKILL.md`
  - [x] Read `03-skills/paper-analyze/SKILL.md`
  - [x] Read `03-skills/paper-analyze-core/SKILL.md`
  - [x] Read `03-skills/paper-synthesize/SKILL.md`
  - [x] Read `03-skills/paper-analyze/scripts/validate_analysis.py`
  - [x] Read `03-skills/paper-synthesize/scripts/validate_synthesis.py`
  - [x] Read `03-skills/create-research-project/references/phase1_planning.md`
  - [x] Read `03-skills/execute-research-project/references/phase2_execution.md`
  - [x] Read Project 04 planning docs
- [x] Update handover with NESTED SKILLS architecture

---

## Phase 2: Parent Skill Pattern Design

- [ ] Document parent SKILL.md router pattern
  - [ ] How parent routes to children based on user intent
  - [ ] YAML frontmatter with `type: skill-chain`
  - [ ] Routing table format
- [ ] Document naming conventions for nested paths
- [ ] Create `references/nested-skill-patterns.md`

---

## Phase 3: Contract Schema (Updated for Nested)

- [ ] Review Project 04 contract schema design
- [ ] Add `structure` section to contract format
  - [ ] `type: nested`
  - [ ] `parent_skill: SKILL.md`
  - [ ] `subfolders: [orchestrators, skills, shared, validation]`
- [ ] Add `path` field to each skill definition
- [ ] Finalize YAML contract format
  - [ ] Define `name`, `version`, `description` fields
  - [ ] Define `skills` array with paths
  - [ ] Define `produces` output specification
  - [ ] Define `requires` dependency specification
  - [ ] Define `gates` structure
  - [ ] Define `schemas` for field validation
- [ ] Create `references/contract-schema.md` with full documentation
- [ ] Create `references/validation-rules.md` with rule types

---

## Phase 4: Template Design (Updated for Nested)

- [ ] Create `templates/` folder
- [ ] Design parent router template
  - [ ] Create `templates/parent_skill.md.j2`
  - [ ] Include routing table
  - [ ] Include child skill links
- [ ] Design chain contract template
  - [ ] Create `templates/chain.yaml.j2`
  - [ ] Include structure section
  - [ ] Include skill paths
- [ ] Design orchestrator skill template
  - [ ] Create `templates/orchestrator_skill.md.j2`
  - [ ] Include YAML frontmatter
  - [ ] Include sub-skill references with nested paths
- [ ] Design sub-skill stub template
  - [ ] Create `templates/subskill_stub.md.j2`
  - [ ] Include basic structure
  - [ ] Include TODO markers
- [ ] Design shared methodology template
  - [ ] Create `templates/shared_methodology.md.j2`
  - [ ] Include "DO NOT LOAD DIRECTLY" warning
- [ ] Design chain documentation template
  - [ ] Create `templates/chain_index.md.j2`
  - [ ] Include Mermaid diagram placeholder

---

## Phase 5: Generation Scripts (Updated for Nested)

### 5.1 Main Chain Generator
- [ ] Create `scripts/generate_chain.py`
  - [ ] Orchestrates all other generators
  - [ ] Creates complete nested structure
  - [ ] Runs validation at end

### 5.2 Structure Generator
- [ ] Create `scripts/generate_skill_structure.py`
  - [ ] Create parent folder
  - [ ] Create orchestrators/ subfolder
  - [ ] Create skills/ subfolder
  - [ ] Create shared/ subfolder
  - [ ] Create validation/ subfolder

### 5.3 Parent Skill Generator
- [ ] Create `scripts/generate_parent_skill.py`
  - [ ] Generate SKILL.md router
  - [ ] Include routing table from definition
  - [ ] Include all child skill links

### 5.4 Contract Generator
- [ ] Create `scripts/generate_contract.py`
  - [ ] Generate _chain.yaml
  - [ ] Include structure section
  - [ ] Include all skills with paths

### 5.5 Orchestrator Generator
- [ ] Create `scripts/generate_orchestrator.py`
  - [ ] Generate orchestrator SKILL.md
  - [ ] Use nested paths for sub-skill references

### 5.6 Sub-skill Stub Generator
- [ ] Create `scripts/generate_subskill_stub.py`
  - [ ] Generate SKILL.md stubs
  - [ ] Detect skill type (regular vs shared)

### 5.7 Documentation Generator
- [ ] Create `scripts/generate_chain_docs.py`
  - [ ] Generate _index.md
  - [ ] Generate Mermaid diagrams

### 5.8 Migration Helper
- [ ] Create `scripts/migrate_flat_to_nested.py`
  - [ ] Move skills to nested locations
  - [ ] Update references automatically
  - [ ] Generate parent SKILL.md

---

## Phase 6: Interactive Workflow

- [ ] Design question flow for nested chains
  - [ ] Step 1: Chain metadata (name, description)
  - [ ] Step 2: Phases (count, names)
  - [ ] Step 3: Orchestrators per phase
  - [ ] Step 4: Sub-skills per orchestrator
  - [ ] Step 5: Shared methodologies
  - [ ] Step 6: Outputs per skill
  - [ ] Step 7: Gates between phases
  - [ ] Step 8: Review and confirm
- [ ] Implement in SKILL.md workflow
- [ ] Add validation at each step

---

## Phase 7: Integration with Project 04

- [ ] Ensure _chain.yaml format matches validate-skill-chain expectations
- [ ] Update validate-skill-chain to read nested structure
- [ ] Test end-to-end flow:
  - [ ] Create chain with create-skill-chain
  - [ ] Validate with validate-skill-chain
  - [ ] Verify reports are accurate

---

## Phase 8: Test with Interview-Analysis Chain

- [ ] Run interactive workflow
- [ ] Generate complete nested structure
- [ ] Review generated files
- [ ] Verify all paths resolve correctly
- [ ] Test validation
- [ ] Document findings

---

## Phase 9: Documentation

- [ ] Complete SKILL.md with nested workflow
- [ ] Create `references/nested-skill-patterns.md`
- [ ] Create `references/skill-chain-patterns.md`
- [ ] Add migration guide
- [ ] Add examples (research-pipeline, interview-analysis)

---

## Phase 10: Finalization

- [ ] Final testing
- [ ] Move to `03-skills/create-skill-chain/`
- [ ] Update project status to COMPLETE

---

## Notes

**Current blockers**: None

**Dependencies**:
- Phase 0 (migration) must complete first to prove pattern
- Project 04 should understand nested structure

**Critical Files Created**:
- `02-resources/_handover.md` - Full context with nested architecture

---

## Agent Instructions

**For the next agent that picks this up**:

1. **START by reading** `02-resources/_handover.md`
2. **EXECUTE Phase 0** - Migrate research pipeline first!
3. **THEN continue** with Phase 2+ (building generators)
4. **TEST** with interview-analysis chain

---

*Mark tasks complete with [x] as you finish them*
