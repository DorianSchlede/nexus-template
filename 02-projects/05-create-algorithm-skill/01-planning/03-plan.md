# Create Skill-Chain Skill - Plan

**Last Updated**: 2025-12-27

---

## CRITICAL: READ HANDOVER FIRST

**Before reading this plan, read**: `02-resources/_handover.md`

That document contains ALL context from the previous agent session including:
- Research pipeline architecture analysis
- Contract format design
- Files to read for context
- Detailed implementation guidance

---

## Approach

Build an interactive META-SKILL that guides users through defining skill-chains and generates:
1. YAML contract files (compatible with Project 04 validate-skill-chain)
2. Skill folder structures with proper templates
3. Orchestrator and sub-skill SKILL.md files
4. Validation integration hooks
5. Mermaid documentation diagrams

**Strategy**: Use the research pipeline as the GOLD STANDARD reference. Every pattern used there should be extractable and reproducible via this skill.

---

## Key Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Interactive vs batch | Interactive workflow | Users need guidance; chain design is complex |
| Template engine | Jinja2 | Python-native, powerful, widely used |
| Contract format | YAML (Project 04 schema) | Human-readable, already designed |
| Generation location | `03-skills/{chain-name}/` | Standard Nexus skill location |
| Validation integration | Hook into validate-skill-chain | Reuse existing validation system |

---

## Resources Needed

**Tools/Access**:
- Python 3.x
- Jinja2 for templating
- PyYAML for contract generation
- pathlib for file operations

**Information/Data**:
- Research pipeline structure (fully documented in handover)
- Project 04 contract schema
- Nexus skill conventions

---

## Dependencies & Links

**CRITICAL FILES TO READ** (in order):

### Research Pipeline (Reference Implementation)
```
03-skills/create-research-project/SKILL.md
03-skills/execute-research-project/SKILL.md
03-skills/paper-analyze/SKILL.md
03-skills/paper-analyze-core/SKILL.md
03-skills/paper-synthesize/SKILL.md
```

### Validation Patterns
```
03-skills/paper-analyze/scripts/validate_analysis.py
03-skills/paper-synthesize/scripts/validate_synthesis.py
03-skills/paper-analyze-core/references/analysis_log_template.md
```

### Phase Handoffs
```
03-skills/create-research-project/references/phase1_planning.md
03-skills/execute-research-project/references/phase2_execution.md
```

### Documentation Created
```
00-system/documentation/research-algorithm-en.md
00-system/documentation/research-algorithm-de.md
```

### Sibling Project (Validation)
```
02-projects/04-skill-chain-validation-system/01-planning/overview.md
02-projects/04-skill-chain-validation-system/01-planning/plan.md
02-projects/04-skill-chain-validation-system/01-planning/steps.md
```

---

## Technical Architecture

**System Components**:

```
03-skills/create-skill-chain/
├── SKILL.md                           # Interactive workflow definition
├── scripts/
│   ├── generate_contract.py           # User input → YAML contract
│   ├── generate_skill_structure.py    # Create folder tree
│   ├── generate_orchestrator.py       # Generate orchestrator SKILL.md
│   ├── generate_subskill_stub.py      # Generate sub-skill templates
│   └── generate_mermaid.py            # Generate diagrams
├── templates/
│   ├── contract.yaml.j2               # Contract template
│   ├── orchestrator_skill.md.j2       # Orchestrator template
│   ├── subskill_stub.md.j2            # Sub-skill template
│   ├── shared_methodology.md.j2       # Shared methodology template
│   └── validation_hook.py.j2          # Validation script template
└── references/
    ├── contract-schema.md             # Full schema documentation
    ├── skill-chain-patterns.md        # Best practices
    └── examples/
        ├── research-pipeline.yaml     # Extracted from existing
        └── interview-analysis.yaml    # Test example
```

**Data Flow**:

```
User Questions
     ↓
[Interactive Workflow in SKILL.md]
     ↓
Collected Chain Definition (in-memory)
     ↓
generate_contract.py → contracts/{chain}.yaml
     ↓
generate_skill_structure.py → folder tree
     ↓
generate_orchestrator.py → orchestrator SKILL.md files
     ↓
generate_subskill_stub.py → sub-skill stubs
     ↓
generate_mermaid.py → documentation with diagrams
     ↓
[User reviews generated files]
     ↓
[Validate with validate-skill-chain]
```

**Technology Stack**:
- Python for generation scripts
- Jinja2 for templates
- YAML for contracts
- Markdown for skill files
- Mermaid for diagrams

---

## Implementation Strategy

**Development Phases**:

### Phase 1: Contract Schema Finalization
- Finalize YAML format from Project 04
- Document all fields, types, validation rules
- Create `references/contract-schema.md`

### Phase 2: Template Design
- Create Jinja2 templates for all file types
- Test templates produce valid output
- Include variable sections for different skill types

### Phase 3: Interactive Workflow Design
- Define question flow:
  1. Chain metadata (name, description)
  2. Phases (how many, names)
  3. Per-phase: orchestrator skill
  4. Per-phase: sub-skills
  5. Per-skill: outputs (paths, required, validates)
  6. Per-phase: gate conditions
- Implement in SKILL.md

### Phase 4: Generation Scripts
- `generate_contract.py` - Main contract generation
- `generate_skill_structure.py` - Folder creation
- `generate_orchestrator.py` - Orchestrator SKILL.md
- `generate_subskill_stub.py` - Sub-skill stubs
- `generate_mermaid.py` - Diagram generation

### Phase 5: Integration
- Test with validate-skill-chain
- Create interview-analysis chain as test case
- Refine based on testing

### Phase 6: Documentation
- Complete SKILL.md with full workflow
- skill-chain-patterns.md best practices
- Example contracts

**Testing Approach**:
1. Generate interview-analysis chain from scratch
2. Validate with validate-skill-chain
3. Manually review generated files for correctness
4. Test end-to-end workflow

---

## Interactive Workflow Detail

### Step 1: Chain Metadata
```
AI: "What is the name of your skill-chain?"
    → Validate: kebab-case, unique

AI: "Brief description (one sentence)?"
    → Store for YAML and SKILL.md
```

### Step 2: Phase Definition
```
AI: "How many phases does this chain have?"
    → Typically 2-4

AI: "Name for Phase 1?"
    → e.g., "preparation", "planning", "acquisition"

AI: "What is the orchestrator skill for Phase 1?"
    → e.g., "prepare-interview-project"
```

### Step 3: Sub-Skills
```
AI: "What sub-skills does [orchestrator] use?"
    → e.g., "transcript-import, transcript-preprocess"

AI: "Are any of these 'shared methodology' (loaded by subagents only)?"
    → Mark as type: shared
```

### Step 4: Outputs
```
AI: "What files does [skill] produce?"
    → e.g., "_briefing.md, transcripts/*/_metadata.json"

AI: "Which are required?"
    → Mark as required: true

AI: "Any field validations needed?"
    → e.g., "approved_by_user equals true"
```

### Step 5: Gates
```
AI: "What conditions must pass before Phase 2 starts?"
    → e.g., "transcripts_with_chunks > 0, _briefing.md exists"
```

### Step 6: Generation
```
AI: "I'll now generate:
    1. contracts/interview-analysis.yaml
    2. 03-skills/interview-analysis-chain/
       ├── prepare-interview-project/
       ├── execute-interview-project/
       ├── transcript-import/
       └── ... (sub-skills)

    Proceed? [Y/n]"
```

---

## Contract Schema (from Project 04)

```yaml
name: string                    # kebab-case chain name
version: string                 # semver
description: string             # human-readable
created: ISO8601               # auto-generated
author: string                 # "create-skill-chain"

skills:
  - id: string                 # skill name (kebab-case)
    phase: int                 # 1, 2, 3...
    type: orchestrator|subskill|shared
    description: string
    sub_skills: [string]       # for orchestrators
    requires:
      - skill: string          # previous skill
        outputs: all|[paths]
    produces:
      - path: string           # glob pattern allowed
        required: bool
        min_count: int         # for glob patterns
        schema: string         # reference to schemas section
        validates:
          - field: string
            equals|in|exists: value
    gate: string               # reference to gates section

schemas:
  schema_name:
    required_fields: [string]
    optional_fields: [string]

gates:
  gate_name:
    checks: [string]           # boolean expressions
```

---

## Mental Models Applied

### First Principles
- Core need: Turn skill-chain DESIGN into skill-chain IMPLEMENTATION
- Fundamental outputs: Contract YAML + Skill folders
- Everything else is derivable from these

### Systems Thinking
- Skill-chains are systems with feedback loops
- Gates are control points preventing bad state propagation
- Validation is the feedback mechanism

### Pre-Mortem Analysis
| Failure Mode | Prevention |
|--------------|------------|
| Generated contracts invalid | Validate against schema before writing |
| Generated skills don't follow conventions | Use templates from working examples |
| Users give incomplete input | Validate each step, don't proceed until complete |
| Integration with validation breaks | Test with validate-skill-chain after generation |

---

## Open Questions

- [ ] How much should be generated vs stubbed for sub-skills?
- [ ] Should shared methodology skills have special handling?
- [ ] How to handle validation script generation?

---

## Success Metrics

1. Can generate research-pipeline-equivalent from scratch
2. Generated contract validates with Project 04 validator
3. Generated skills pass Nexus convention checks
4. User can create interview-analysis chain in <15 min
5. Generated documentation includes accurate Mermaid diagrams

---

*Next: Complete steps.md to break down execution*
