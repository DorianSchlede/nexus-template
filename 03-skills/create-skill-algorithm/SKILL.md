---
name: create-skill-algorithm
description: "Create a new nested skill-chain. Load when user mentions 'create skill chain', 'new skill chain', 'build algorithm', 'generate skill chain'. Interactive workflow that defines phases, orchestrators, and sub-skills, then generates the complete nested folder structure."
type: meta-skill
version: "1.0"
---

# Create Skill-Chain

Build complete nested skill-chains following the connect/router pattern.

## Purpose

This META-SKILL creates infrastructure for other skill-chains. It:

1. **Guides** users through defining a skill-chain interactively
2. **Generates** complete nested folder structure
3. **Creates** parent SKILL.md router
4. **Creates** _chain.yaml contract
5. **Creates** orchestrator and sub-skill stubs
6. **Generates** _index.md documentation with Mermaid diagrams

**Pattern Reference**: See `00-system/skills/system/add-integration/references/integration-architecture.md`

---

## Workflow Overview

```
┌─────────────────────────────────────────────────────────┐
│               CREATE SKILL-CHAIN                         │
├─────────────────────────────────────────────────────────┤
│  Step 1: Initialize TodoList                            │
│  Step 2: Chain metadata (name, description)             │
│  Step 3: Define phases                                  │
│  Step 4: Define orchestrators per phase                 │
│  Step 5: Define sub-skills per orchestrator             │
│  Step 6: Define shared methodologies                    │
│  Step 7: Define outputs and gates                       │
│  Step 8: Review and confirm                             │
│  Step 9: Generate structure                             │
│  Step 10: Display results                               │
└─────────────────────────────────────────────────────────┘
```

---

## Workflow

### Step 1: Initialize TodoList

Create TodoWrite with all workflow steps:
```
- [ ] Gather chain metadata
- [ ] Define phases
- [ ] Define orchestrators
- [ ] Define sub-skills
- [ ] Define shared methodologies
- [ ] Define outputs and gates
- [ ] Review and confirm
- [ ] Generate structure
```

---

### Step 2: Chain Metadata

Display:
```
Let's create a new skill-chain!

A skill-chain is a NESTED folder containing multiple related skills
that work together (like research-pipeline).

What's the name of this skill-chain?
(Use kebab-case, e.g., "interview-analysis", "content-pipeline")

Name:
```

**Wait for user response.**

Then ask:
```
Brief description of what this skill-chain does:
```

**Capture**:
- `chain_name` (kebab-case)
- `chain_description` (one line)

---

### Step 3: Define Phases

Display:
```
Skill-chains are organized into PHASES.

Each phase has:
- One ORCHESTRATOR (user-facing entry point)
- Multiple SUB-SKILLS (called by the orchestrator)

Example (research-pipeline):
- Phase 1: Planning (create-research-project)
- Phase 2: Execution (execute-research-project)

How many phases does {chain_name} have? (1-5)
```

**Wait for user response.**

Then for each phase:
```
Phase {N} name? (e.g., "planning", "execution", "review")
```

**Capture**:
- `phases` array with names

---

### Step 4: Define Orchestrators

For each phase:
```
Phase {N}: {phase_name}

What's the orchestrator skill name?
(This is the user-facing entry point for this phase)

Example: "create-research-project", "execute-interview-project"

Orchestrator name:
```

**Capture**:
- `phases[N].orchestrator` name

---

### Step 5: Define Sub-Skills

For each orchestrator:
```
Orchestrator: {orchestrator_name}

What sub-skills does this orchestrator use?
(Comma-separated list)

Example: "paper-search, pdf-preprocess, paper-analyze"

Sub-skills:
```

**Capture**:
- `phases[N].sub_skills` array

---

### Step 6: Define Shared Methodologies

Display:
```
SHARED METHODOLOGIES are skills loaded by subagents, never directly.

Example: "paper-analyze-core" is loaded by analysis subagents

Does {chain_name} have any shared methodologies? (y/n)
```

If yes:
```
List shared methodology names (comma-separated):
```

**Capture**:
- `shared_skills` array

---

### Step 7: Define Outputs and Gates

For each orchestrator:
```
Orchestrator: {orchestrator_name}

What files does this orchestrator produce?
(One per line, prefix with * for required)

Example:
*_briefing.md
*_analysis_kit.md
papers/*/_metadata.json

Outputs (empty line to finish):
```

Then:
```
What conditions must pass before the NEXT phase can start?
(Gate conditions, one per line, empty to finish)

Example:
papers_with_chunks > 0
_briefing.md exists

Gate conditions:
```

**Capture**:
- `phases[N].outputs` array
- `phases[N].gate` conditions

---

### Step 8: Review and Confirm

Display:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SKILL-CHAIN SUMMARY: {chain_name}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Description: {chain_description}

PHASES:
{for each phase}
  Phase {N}: {phase_name}
    Orchestrator: {orchestrator}
    Sub-skills: {sub_skills}
    Outputs: {outputs}
    Gate: {gate_name}
{end}

SHARED METHODOLOGIES:
  {shared_skills or "None"}

STRUCTURE TO GENERATE:
03-skills/{chain_name}/
├── SKILL.md                 (parent router)
├── _chain.yaml              (contract)
├── _index.md                (documentation)
├── orchestrators/
│   {for each orchestrator}
│   └── {orchestrator}/
│       └── SKILL.md
│   {end}
├── skills/
│   {for each sub_skill}
│   └── {sub_skill}/
│       └── SKILL.md
│   {end}
├── shared/
│   {for each shared}
│   └── {shared}/
│       └── SKILL.md
│   {end}
└── validation/

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Generate this structure? (y/n)
```

**Wait for confirmation.**

---

### Step 9: Generate Structure

Run the generation script:
```bash
python 03-skills/create-skill-chain/scripts/generate_chain.py \
  --name "{chain_name}" \
  --config "{json_config}"
```

The script will:
1. Create `03-skills/{chain_name}/` folder
2. Create subfolders: `orchestrators/`, `skills/`, `shared/`, `validation/`
3. Generate `SKILL.md` (parent router) from template
4. Generate `_chain.yaml` (contract) from template
5. Generate orchestrator SKILL.md stubs
6. Generate sub-skill SKILL.md stubs
7. Generate shared methodology stubs
8. Generate `_index.md` with Mermaid diagrams

---

### Step 10: Display Results

```
Skill-chain generated!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Created: 03-skills/{chain_name}/
├── SKILL.md                 ✓
├── _chain.yaml              ✓
├── _index.md                ✓
├── orchestrators/
│   └── {N} orchestrator(s)  ✓
├── skills/
│   └── {N} sub-skill(s)     ✓
├── shared/
│   └── {N} shared skill(s)  ✓
└── validation/              ✓

NEXT STEPS:
1. Review generated SKILL.md files
2. Implement sub-skill logic (scripts/, references/)
3. Test the chain: "run {orchestrator_name}"
4. Validate with: validate-skill-chain {chain_name}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Generated Files

### Parent SKILL.md (Router)

Generated from `templates/parent_skill.md.j2`:
- YAML frontmatter with `type: skill-chain`
- Description includes all trigger phrases
- Routing table mapping intents to child skills
- Links to _chain.yaml and _index.md

### _chain.yaml (Contract)

Generated from `templates/chain.yaml.j2`:
- Structure definition (nested type, subfolders)
- All skills with paths
- Outputs per skill
- Gate definitions

### Orchestrator SKILL.md

Generated from `templates/orchestrator_skill.md.j2`:
- Phase description
- Sub-skill references
- Workflow steps (TODO)
- Gate conditions

### Sub-skill SKILL.md

Generated from `templates/subskill_stub.md.j2`:
- Basic structure
- TODO markers for implementation
- Reference to parent chain

### Shared Methodology SKILL.md

Generated from `templates/shared_methodology.md.j2`:
- "DO NOT LOAD DIRECTLY" warning
- Designed for subagent loading
- Methodology template

### _index.md (Documentation)

Generated from `templates/chain_index.md.j2`:
- Mermaid architecture diagram
- Skill inventory tables
- Output mappings
- Usage examples

---

## Scripts

| Script | Purpose |
|--------|---------|
| `generate_chain.py` | Main generator - orchestrates all others |
| `generate_contract.py` | Generate _chain.yaml |
| `generate_parent_skill.py` | Generate parent SKILL.md |
| `generate_orchestrator.py` | Generate orchestrator stubs |
| `generate_subskill_stub.py` | Generate sub-skill stubs |
| `generate_chain_docs.py` | Generate _index.md with Mermaid |

---

## Templates

All in `templates/`:
- `parent_skill.md.j2`
- `chain.yaml.j2`
- `orchestrator_skill.md.j2`
- `subskill_stub.md.j2`
- `shared_methodology.md.j2`
- `chain_index.md.j2`

---

## Example: Interview Analysis Chain

```
User: "create skill chain"
AI: "What's the name? interview-analysis"
AI: "Description? Analyze interview transcripts for themes"
AI: "How many phases? 2"
AI: "Phase 1 name? preparation"
AI: "Phase 1 orchestrator? prepare-interview-project"
AI: "Phase 1 sub-skills? transcript-import, transcript-preprocess"
AI: "Phase 2 name? analysis"
AI: "Phase 2 orchestrator? execute-interview-project"
AI: "Phase 2 sub-skills? transcript-analyze, theme-synthesize"
AI: "Shared methodologies? transcript-analyze-core"
...
AI: "Generate? y"
→ Creates complete 03-skills/interview-analysis/ structure
```

---

## References

- [Research Pipeline](../research-pipeline/) - Reference implementation
- [Integration Architecture](../../00-system/skills/system/add-integration/references/integration-architecture.md) - Connect pattern
- [Contract Schema](references/contract-schema.md) - _chain.yaml format
- [Nested Skill Patterns](references/nested-skill-patterns.md) - Best practices

---

**Version**: 1.0
**Created**: 2025-12-27
