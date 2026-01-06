# HANDOVER DOCUMENT: Create Skill-Chain Skill

## FOR THE NEXT AGENT - READ THIS FIRST

This document contains EVERYTHING you need to continue this project. The previous agent ran out of context after extensive research and planning. DO NOT start from scratch - use this context.

---

## ⚠️ CRITICAL ARCHITECTURE UPDATE ⚠️

**USER REQUEST (2025-12-27)**:
> "A skill chain should NOT be a single skill chain skill, but MULTIPLE skills in a big one. NESTED SKILLS actually. We can also nest all the research skills in 03 properly."

**THIS CHANGES THE ARCHITECTURE FUNDAMENTALLY:**

A skill-chain is NOT a single skill file - it's a **NAMESPACE/CONTAINER** that holds MULTIPLE nested skills organized hierarchically.

---

## MISSION (UPDATED)

Create a `create-skill-chain` skill that:

1. **Creates a NESTED SKILL STRUCTURE** - a parent folder containing child skills
2. Guides users through defining phases, orchestrators, and sub-skills
3. Generates the complete folder hierarchy with nested SKILL.md files
4. Generates the YAML contract for validation
5. Creates proper references between parent and child skills

**ADDITIONALLY**: Reorganize existing research pipeline skills under `03-skills/research-pipeline/` as the first nested skill-chain example.

**This is a META-SKILL** - it creates infrastructure for other skill-chains as NESTED SKILLS.

---

## CRITICAL FILES TO READ (IN ORDER)

### 1. Understand Existing Research Pipeline (THE MODEL)

```
03-skills/create-research-project/SKILL.md        # Phase 1 orchestrator (750 lines)
03-skills/execute-research-project/SKILL.md       # Phase 2 orchestrator (670 lines)
03-skills/paper-analyze/SKILL.md                  # Sub-skill example
03-skills/paper-analyze-core/SKILL.md             # Shared methodology pattern
03-skills/paper-synthesize/SKILL.md               # Synthesis pattern
```

### 2. Understand Existing Validation Patterns

```
03-skills/paper-analyze/scripts/validate_analysis.py     # 530 lines - analysis validation
03-skills/paper-synthesize/scripts/validate_synthesis.py # 420 lines - synthesis validation
03-skills/paper-analyze-core/references/analysis_log_template.md  # Schema v2.2
03-skills/paper-synthesize/references/synthesis_validation_contract.md
```

### 3. Understand Phase Handoffs

```
03-skills/create-research-project/references/phase1_planning.md
03-skills/execute-research-project/references/phase2_execution.md
03-skills/create-research-project/references/abstract_review.md
```

### 4. Understand Documentation Created

```
00-system/documentation/research-algorithm-en.md  # Full pipeline docs with Mermaid
00-system/documentation/research-algorithm-de.md  # German version
```

### 5. Understand Project 04 (Skill-Chain VALIDATION - sibling project)

```
02-projects/04-skill-chain-validation-system/01-planning/overview.md
02-projects/04-skill-chain-validation-system/01-planning/plan.md
02-projects/04-skill-chain-validation-system/01-planning/steps.md
```

---

## WHAT WE LEARNED FROM THE RESEARCH PIPELINE

### Architecture Pattern (UPDATED FOR NESTED SKILLS)

```
SKILL-CHAIN = NESTED FOLDER with Parent SKILL.md + Child Skills + Contracts + Validation

CURRENT (FLAT - WRONG):
03-skills/
├── create-research-project/SKILL.md
├── execute-research-project/SKILL.md
├── paper-search/SKILL.md
├── paper-analyze/SKILL.md
├── paper-analyze-core/SKILL.md
├── paper-synthesize/SKILL.md
├── paper-query/SKILL.md
├── paper-manage/SKILL.md
└── pdf-preprocess/SKILL.md

TARGET (NESTED - CORRECT):
03-skills/
└── research-pipeline/                    # SKILL-CHAIN NAMESPACE
    ├── SKILL.md                          # PARENT: Routes to child skills, docs
    ├── _chain.yaml                       # CONTRACT: Defines chain structure
    ├── _index.md                         # GENERATED: Skill-chain overview
    │
    ├── orchestrators/                    # PHASE ORCHESTRATORS (user-facing)
    │   ├── create-research-project/
    │   │   └── SKILL.md
    │   └── execute-research-project/
    │       └── SKILL.md
    │
    ├── skills/                           # SUB-SKILLS (called by orchestrators)
    │   ├── paper-search/
    │   │   ├── SKILL.md
    │   │   └── scripts/
    │   ├── pdf-preprocess/
    │   │   ├── SKILL.md
    │   │   └── scripts/
    │   ├── paper-analyze/
    │   │   ├── SKILL.md
    │   │   └── scripts/
    │   ├── paper-synthesize/
    │   │   ├── SKILL.md
    │   │   └── scripts/
    │   ├── paper-query/
    │   │   └── SKILL.md
    │   └── paper-manage/
    │       └── SKILL.md
    │
    ├── shared/                           # SHARED METHODOLOGIES (loaded by subagents)
    │   └── paper-analyze-core/
    │       └── SKILL.md
    │
    └── validation/                       # VALIDATION SCRIPTS
        ├── validate_analysis.py
        └── validate_synthesis.py

KEY CHANGES:
1. All skills grouped under parent namespace (research-pipeline/)
2. Parent SKILL.md routes to child skills based on user intent
3. Clear separation: orchestrators/ vs skills/ vs shared/
4. Contract (_chain.yaml) lives at chain root
5. Validation scripts co-located with chain
```

### Key Patterns Discovered

1. **Orchestrator + Sub-skill Pattern**
   - Orchestrator = user-facing skill that coordinates
   - Sub-skills = specialized skills called by orchestrator
   - Some sub-skills are "shared methodology" (loaded by subagents, never directly)

2. **Phase Gate Pattern**
   - Each phase ends with a gate (boolean checks)
   - Gate must pass before next phase starts
   - Example: `readiness-gate` checks `papers_with_chunks > 0`

3. **Contract-Based Validation**
   - Each skill declares what it produces
   - Validation checks outputs exist and are valid
   - Anti-hallucination: 3-point evidence (start/mid/end + hash)

4. **Handoff Document Pattern**
   - Phase 1 creates `_analysis_kit.md` for Phase 2
   - Contains all context needed by subagents
   - Prevents context loss between phases

5. **Two-Tier Detail Strategy**
   - `_analysis_log.md`: Full traceability (150-char quotes)
   - `index.md` frontmatter: Compact for synthesis (50-80 char quotes)

---

## SKILL-CHAIN CONTRACT FORMAT (DESIGNED IN PROJECT 04)

```yaml
# contracts/research-pipeline.yaml
name: research-pipeline
version: "1.0"
description: "Academic paper research, analysis, and synthesis"

skills:
  - id: create-research-project
    phase: 1
    type: orchestrator
    produces:
      - path: "02-resources/_briefing.md"
        required: true
        schema: briefing
      - path: "02-resources/_analysis_kit.md"
        required: true
      - path: "03-working/_selection_log.md"
        required: true
        validates:
          - field: "approved_by_user"
            equals: true
      - path: "02-resources/papers/*/_metadata.json"
        required: true
        min_count: 1
    gate: readiness-gate

  - id: execute-research-project
    phase: 2
    type: orchestrator
    requires:
      - skill: create-research-project
        outputs: all
    produces:
      - path: "02-resources/papers/*/index.md"
        required: true
        validates:
          - has_yaml_frontmatter: true
      - path: "02-resources/papers/*/_analysis_log.md"
        required: true
        validates:
          - field: "schema_version"
            in: ["2.0", "2.1", "2.2"]
      - path: "04-outputs/_synthesis.md"
        required: true
      - path: "04-outputs/_validation_report.md"
        required: true

schemas:
  briefing:
    required_fields:
      - research_question
      - extraction_schema
    optional_fields:
      - focus_areas
      - skip_sections

gates:
  readiness-gate:
    checks:
      - "papers_with_chunks > 0"
      - "_briefing.md exists"
      - "_analysis_kit.md exists"
      - "overview.md status == READY_FOR_EXECUTION"
```

---

## WHAT CREATE-SKILL-CHAIN SHOULD DO

### Interactive Workflow

```
User: "create skill chain for interview analysis"

AI: "Let's define your skill-chain. I'll guide you through:
     1. Chain metadata (name, description, version)
     2. Skills in the chain (orchestrators + sub-skills)
     3. Outputs per skill (what files each produces)
     4. Gates between phases (validation checkpoints)
     5. Schemas for field validation

     Let's start with the basics..."

[Step 1: Chain Metadata]
AI: "What's the name of this skill-chain?"
User: "interview-analysis"

AI: "Brief description?"
User: "Analyze interview transcripts for themes and insights"

[Step 2: Define Skills]
AI: "How many phases does this chain have?"
User: "2 - preparation and analysis"

AI: "Let's define Phase 1. What's the orchestrator skill called?"
User: "prepare-interview-project"

AI: "What sub-skills does Phase 1 use?"
User: "transcript-import, transcript-preprocess"

[Step 3: Define Outputs]
AI: "What files does prepare-interview-project produce?"
User: "_briefing.md, _interview_kit.md, transcripts/*/_metadata.json"

AI: "Are any of these required?"
User: "All of them"

[Step 4: Define Gates]
AI: "What conditions must be true before Phase 2 can start?"
User: "transcripts_preprocessed > 0, _briefing.md exists"

[Step 5: Generate Contract]
AI: "Generating contracts/interview-analysis.yaml..."
    "Generating validate-skill-chain integration..."
    "Creating skill folder structure..."

[Output]
03-skills/interview-analysis-chain/
├── SKILL.md
├── contracts/
│   └── interview-analysis.yaml
├── scripts/
│   └── (validation scripts)
└── references/
    └── contract-schema.md
```

### Generated Outputs

1. **Chain Contract YAML** - `contracts/{chain-name}.yaml`
2. **Orchestrator Skill Templates** - One per phase
3. **Sub-Skill Stubs** - Basic structure for each sub-skill
4. **Validation Integration** - Hooks into validate-skill-chain skill
5. **Documentation** - Auto-generated Mermaid diagrams

---

## RELATIONSHIP TO PROJECT 04

```
Project 04: validate-skill-chain (VALIDATION)
├── Validates EXISTING skill-chains
├── Reads contract YAML
├── Checks project state against contract
├── Reports what's missing/broken
└── 3-step fix workflow

Project 05: create-skill-chain (CREATION) ← THIS PROJECT
├── Creates NEW skill-chains
├── Interactive workflow to define chain
├── Generates contract YAML
├── Generates skill folder structure
├── Generates validation hooks

THEY WORK TOGETHER:
create-skill-chain → generates → contract.yaml
validate-skill-chain → reads → contract.yaml → validates project
```

---

## TECHNICAL DECISIONS MADE

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Contract format | YAML | Human-readable, Python-friendly |
| Contract location | `03-skills/{chain-name}/contracts/` | Co-located with skill |
| Skill structure | Orchestrator + Sub-skills | Proven pattern from research pipeline |
| Validation | Integrate with validate-skill-chain | Reuse existing validation system |
| Generation | Python scripts + templates | Consistent with Nexus patterns |

---

## FILES TO CREATE

### Core Skill (create-skill-chain)
```
03-skills/create-skill-chain/
├── SKILL.md                           # Main skill workflow
├── scripts/
│   ├── generate_chain.py              # MAIN: Generates complete nested chain
│   ├── generate_contract.py           # Generate _chain.yaml from user input
│   ├── generate_skill_structure.py    # Create nested folder structure
│   ├── generate_parent_skill.py       # Generate parent SKILL.md (router)
│   ├── generate_orchestrator.py       # Generate orchestrator SKILL.md
│   ├── generate_subskill_stub.py      # Generate sub-skill templates
│   ├── migrate_flat_to_nested.py      # MIGRATION: Convert flat skills to nested
│   └── generate_chain_docs.py         # Generate _index.md with Mermaid
├── templates/
│   ├── chain.yaml.j2                  # Jinja2 template for _chain.yaml
│   ├── parent_skill.md.j2             # Template for parent router SKILL.md
│   ├── orchestrator_skill.md.j2       # Template for orchestrator
│   ├── subskill_stub.md.j2            # Template for sub-skill
│   ├── shared_methodology.md.j2       # Template for shared/ skills
│   └── chain_index.md.j2              # Template for _index.md overview
└── references/
    ├── contract-schema.md             # Full contract format docs
    ├── nested-skill-patterns.md       # Best practices for nesting
    ├── skill-chain-patterns.md        # Orchestrator patterns
    └── examples/
        └── research-pipeline/         # GENERATED: Example after migration
            ├── _chain.yaml
            └── structure-preview.md
```

### Reorganized Research Pipeline (FIRST PRIORITY)
```
03-skills/research-pipeline/           # NEW: Nested skill-chain
├── SKILL.md                           # Parent router
├── _chain.yaml                        # Contract
├── _index.md                          # Auto-generated docs
├── orchestrators/
│   ├── create-research-project/       # Moved from 03-skills/
│   └── execute-research-project/      # Moved from 03-skills/
├── skills/
│   ├── paper-search/                  # Moved from 03-skills/
│   ├── pdf-preprocess/                # Moved from 03-skills/
│   ├── paper-analyze/                 # Moved from 03-skills/
│   ├── paper-synthesize/              # Moved from 03-skills/
│   ├── paper-query/                   # Moved from 03-skills/
│   └── paper-manage/                  # Moved from 03-skills/
├── shared/
│   └── paper-analyze-core/            # Moved from 03-skills/
└── validation/
    ├── validate_analysis.py           # Moved from paper-analyze/scripts/
    └── validate_synthesis.py          # Moved from paper-synthesize/scripts/
```

### Integration Points
```
03-skills/validate-skill-chain/        # Reads _chain.yaml from any chain
02-projects/*/                         # Test against real projects
```

---

## IMPLEMENTATION PHASES (UPDATED FOR NESTED SKILLS)

### Phase 0: MIGRATE RESEARCH PIPELINE FIRST ⭐
**This is the FIRST PRIORITY** - proves the pattern before building generators.

1. Create `03-skills/research-pipeline/` parent folder
2. Create parent `SKILL.md` (router skill)
3. Create `_chain.yaml` contract
4. Move orchestrators to `orchestrators/` subfolder
5. Move sub-skills to `skills/` subfolder
6. Move paper-analyze-core to `shared/` subfolder
7. Move validation scripts to `validation/` subfolder
8. Update all internal references/imports
9. Test that skills still work
10. Generate `_index.md` documentation

### Phase 1: Parent Skill Pattern Design
- Design parent SKILL.md router pattern
- Define how parent routes to child skills
- Define naming conventions for nested paths
- Document in `nested-skill-patterns.md`

### Phase 2: Contract Schema (Updated)
- Add `structure` section to contract for folder layout
- Add `parent` and `children` relationships
- Add `routing` rules for parent SKILL.md
- Create `contract-schema.md` reference

### Phase 3: Template Design
- `parent_skill.md.j2` - Router that loads appropriate child
- `chain.yaml.j2` - Contract with nested structure
- `orchestrator_skill.md.j2` - Phase orchestrators
- `subskill_stub.md.j2` - Regular sub-skills
- `shared_methodology.md.j2` - Shared skills (with DO NOT LOAD warning)
- `chain_index.md.j2` - Auto-generated documentation

### Phase 4: Generation Scripts
- `generate_chain.py` - Main orchestrator script
- `generate_skill_structure.py` - Create nested folders
- `generate_parent_skill.py` - Parent router SKILL.md
- `generate_orchestrator.py` - Orchestrator SKILL.md
- `generate_subskill_stub.py` - Sub-skill templates
- `migrate_flat_to_nested.py` - Migration helper
- `generate_chain_docs.py` - Auto-generate _index.md

### Phase 5: Interactive Workflow
- Chain metadata (name, description)
- Phases (how many, names)
- Orchestrators per phase
- Sub-skills per orchestrator
- Shared methodologies
- Outputs per skill
- Gates between phases
- Generate full nested structure

### Phase 6: Integration & Testing
- Test with interview-analysis chain
- Verify validate-skill-chain works with nested chains
- Test routing from parent to children
- Verify all paths resolve correctly

### Phase 7: Documentation
- Full SKILL.md with nested examples
- `nested-skill-patterns.md` best practices
- Migration guide for existing flat skills

---

## PARENT SKILL.MD ROUTER PATTERN (NEW!)

**KEY INSIGHT**: This follows the same pattern as `{service}-connect` in the integration architecture!

See: `00-system/skills/system/add-integration/references/integration-architecture.md`

The parent SKILL.md acts as a **CONNECT/ROUTER** that:
1. **Is the ONLY discoverable entry point** - its `description` triggers loading
2. **Routes to appropriate child skill** based on user intent
3. **Users never need to know about internal structure** - they just talk to the parent
4. **Child skills can use relative paths** - no need to update all references

**IMPLICATION**: We DON'T need to update all internal paths in child skills! The parent handles discovery, and child skills work with relative paths internally.

**Example: `03-skills/research-pipeline/SKILL.md`**:

```yaml
---
name: research-pipeline
description: "Academic paper research, analysis, and synthesis skill-chain. Load when user mentions 'research papers', 'analyze papers', 'paper synthesis', 'academic research'. This is a NESTED skill-chain containing multiple child skills."
type: skill-chain
---

# Research Pipeline

A complete skill-chain for academic paper research, from search to synthesis.

## Overview

This skill-chain contains:
- **2 Orchestrators**: Phase 1 (Planning) and Phase 2 (Execution)
- **7 Sub-skills**: paper-search, pdf-preprocess, paper-analyze, etc.
- **1 Shared**: paper-analyze-core methodology

## Routing

Based on user intent, load the appropriate child skill:

| User Says | Load This Skill |
|-----------|-----------------|
| "create research project", "new research on [topic]" | `orchestrators/create-research-project/SKILL.md` |
| "execute research project", "analyze papers" | `orchestrators/execute-research-project/SKILL.md` |
| "search for papers", "find papers about" | `skills/paper-search/SKILL.md` |
| "preprocess pdf", "convert pdf" | `skills/pdf-preprocess/SKILL.md` |
| "analyze papers", "run analysis" | `skills/paper-analyze/SKILL.md` |
| "synthesize papers", "cross-paper analysis" | `skills/paper-synthesize/SKILL.md` |
| "query papers", "what papers discuss" | `skills/paper-query/SKILL.md` |
| "manage collection", "list papers" | `skills/paper-manage/SKILL.md` |

## Chain Documentation

See `_index.md` for auto-generated documentation with Mermaid diagrams.
See `_chain.yaml` for the validation contract.

## Child Skills

### Orchestrators (User-Facing)
- [create-research-project](orchestrators/create-research-project/SKILL.md) - Phase 1
- [execute-research-project](orchestrators/execute-research-project/SKILL.md) - Phase 2

### Sub-Skills (Called by Orchestrators)
- [paper-search](skills/paper-search/SKILL.md)
- [pdf-preprocess](skills/pdf-preprocess/SKILL.md)
- [paper-analyze](skills/paper-analyze/SKILL.md)
- [paper-synthesize](skills/paper-synthesize/SKILL.md)
- [paper-query](skills/paper-query/SKILL.md)
- [paper-manage](skills/paper-manage/SKILL.md)

### Shared Methodologies (DO NOT LOAD DIRECTLY)
- [paper-analyze-core](shared/paper-analyze-core/SKILL.md) - Loaded by subagents
```

---

## EXAMPLE: GENERATING INTERVIEW-ANALYSIS CHAIN (NESTED)

**Input from user**:
```yaml
name: interview-analysis
description: "Analyze interview transcripts for themes and insights"
phases:
  - name: preparation
    orchestrator: prepare-interview-project
    sub_skills:
      - transcript-import
      - transcript-preprocess
    outputs:
      - _briefing.md (required)
      - _interview_kit.md (required)
      - transcripts/*/_metadata.json (required, min_count: 1)
    gate:
      - transcripts_with_chunks > 0
      - _briefing.md exists

  - name: analysis
    orchestrator: execute-interview-project
    sub_skills:
      - transcript-analyze
      - transcript-analyze-core (shared methodology)
      - theme-synthesize
    outputs:
      - transcripts/*/index.md (required)
      - transcripts/*/_analysis_log.md (required)
      - 04-outputs/_synthesis.md (required)
```

**Generated NESTED structure**:
```
03-skills/interview-analysis/          # SKILL-CHAIN NAMESPACE
├── SKILL.md                           # Parent router (auto-generated)
├── _chain.yaml                        # Contract (auto-generated)
├── _index.md                          # Docs with Mermaid (auto-generated)
│
├── orchestrators/
│   ├── prepare-interview-project/
│   │   └── SKILL.md                   # Phase 1 orchestrator
│   └── execute-interview-project/
│       └── SKILL.md                   # Phase 2 orchestrator
│
├── skills/
│   ├── transcript-import/
│   │   └── SKILL.md                   # Stub for implementation
│   ├── transcript-preprocess/
│   │   └── SKILL.md                   # Stub for implementation
│   ├── transcript-analyze/
│   │   └── SKILL.md                   # Stub for implementation
│   └── theme-synthesize/
│       └── SKILL.md                   # Stub for implementation
│
├── shared/
│   └── transcript-analyze-core/
│       └── SKILL.md                   # Shared methodology
│
└── validation/
    └── validate_analysis.py           # Stub for implementation
```

**Generated contract** (`_chain.yaml`):
```yaml
name: interview-analysis
version: "1.0"
description: "Analyze interview transcripts for themes and insights"
created: "2025-12-27"
author: "auto-generated by create-skill-chain"

structure:
  type: nested
  parent_skill: SKILL.md
  subfolders:
    - orchestrators
    - skills
    - shared
    - validation

skills:
  - id: prepare-interview-project
    phase: 1
    type: orchestrator
    path: orchestrators/prepare-interview-project/SKILL.md
    description: "Prepare interview transcripts for analysis"
    sub_skills:
      - transcript-import
      - transcript-preprocess
    produces:
      - path: "02-resources/_briefing.md"
        required: true
      - path: "02-resources/_interview_kit.md"
        required: true
      - path: "02-resources/transcripts/*/_metadata.json"
        required: true
        min_count: 1
    gate: preparation-gate

  - id: execute-interview-project
    phase: 2
    type: orchestrator
    path: orchestrators/execute-interview-project/SKILL.md
    description: "Analyze transcripts and synthesize themes"
    requires:
      - skill: prepare-interview-project
        outputs: all
    sub_skills:
      - transcript-analyze
      - transcript-analyze-core
      - theme-synthesize
    produces:
      - path: "02-resources/transcripts/*/index.md"
        required: true
      - path: "02-resources/transcripts/*/_analysis_log.md"
        required: true
      - path: "04-outputs/_synthesis.md"
        required: true

  - id: transcript-analyze-core
    type: shared
    path: shared/transcript-analyze-core/SKILL.md
    description: "SHARED METHODOLOGY - DO NOT LOAD DIRECTLY"

gates:
  preparation-gate:
    checks:
      - "transcripts_with_chunks > 0"
      - "_briefing.md exists"
      - "_interview_kit.md exists"
```

---

## SUCCESS CRITERIA (UPDATED)

1. **Nested Architecture**: Skills are properly nested under parent namespace
2. **Migration Complete**: Research pipeline reorganized under `03-skills/research-pipeline/`
3. **Parent Router Works**: Parent SKILL.md correctly routes to child skills
4. **Contracts Updated**: `_chain.yaml` includes structure information
5. **Usability**: User can create new skill-chains through guided workflow
6. **Integration**: Works with validate-skill-chain
7. **Documentation**: Auto-generated `_index.md` with Mermaid diagrams

---

## NEXT STEPS FOR AGENT

### FIRST PRIORITY: Migrate Research Pipeline
1. **CREATE** `03-skills/research-pipeline/` folder structure
2. **CREATE** parent `SKILL.md` router (use template above)
3. **CREATE** `_chain.yaml` contract
4. **MOVE** existing skills to nested locations:
   - `create-research-project` → `orchestrators/`
   - `execute-research-project` → `orchestrators/`
   - `paper-*` skills → `skills/`
   - `paper-analyze-core` → `shared/`
   - validation scripts → `validation/`
5. **UPDATE** all internal references in SKILL.md files
6. **TEST** that skills still work correctly
7. **GENERATE** `_index.md` documentation

### THEN: Build the create-skill-chain skill
1. Design templates for nested generation
2. Implement generation scripts
3. Create interactive workflow
4. Test with interview-analysis chain

---

## CONTEXT THAT MAY BE LOST

- **USER REQUEST (2025-12-27)**: "A skill chain should NOT be a single skill chain skill, but MULTIPLE skills in a big one. NESTED SKILLS actually."
- User wants "HYPERDETAILED ULTRAFUCKING PLANNING"
- This is a META-SKILL that creates other skill-chains AS NESTED STRUCTURES
- Project 04 (validation) and Project 05 (creation) are siblings
- Research pipeline is the GOLD STANDARD - MIGRATE IT FIRST
- Anti-hallucination patterns are critical (3-point evidence, hash validation)
- User prefers 3-step fix workflow (research → plan → execute)
- History tracking is important for validation
- Contracts should live at chain root as `_chain.yaml`

---

## DETAILED MIGRATION PLAN FOR RESEARCH PIPELINE

**Source** (current flat structure):
```
03-skills/
├── create-research-project/
├── execute-research-project/
├── paper-analyze/
├── paper-analyze-core/
├── paper-manage/
├── paper-query/
├── paper-search/
├── paper-synthesize/
└── pdf-preprocess/
```

**Target** (nested structure):
```
03-skills/
└── research-pipeline/
    ├── SKILL.md                    # NEW: Parent router
    ├── _chain.yaml                 # NEW: Contract
    ├── _index.md                   # NEW: Auto-generated docs
    ├── orchestrators/
    │   ├── create-research-project/  # MOVED
    │   └── execute-research-project/ # MOVED
    ├── skills/
    │   ├── paper-analyze/          # MOVED
    │   ├── paper-manage/           # MOVED
    │   ├── paper-query/            # MOVED
    │   ├── paper-search/           # MOVED
    │   ├── paper-synthesize/       # MOVED
    │   └── pdf-preprocess/         # MOVED
    ├── shared/
    │   └── paper-analyze-core/     # MOVED
    └── validation/
        ├── validate_analysis.py    # MOVED from paper-analyze/scripts/
        └── validate_synthesis.py   # MOVED from paper-synthesize/scripts/
```

**Files to update after move**:
1. Each SKILL.md - update relative paths to references/scripts
2. Orchestrator SKILL.md files - update paths to sub-skills
3. Validation scripts - update import paths
4. Any files that reference skill paths

---

**END OF HANDOVER DOCUMENT**

*Created: 2025-12-27*
*Updated: 2025-12-27 - Added NESTED SKILLS architecture*
*Previous agent context: ~95% full before handover*
