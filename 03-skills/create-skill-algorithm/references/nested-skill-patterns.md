# Nested Skill Patterns

Best practices for designing and implementing nested skill-chains.

---

## Core Pattern: CONNECT/ROUTER

A skill-chain follows the **CONNECT/ROUTER** pattern (like `{service}-connect` in integrations):

```
03-skills/{chain-name}/
├── SKILL.md                    ← ROUTER: Only discoverable entry point
├── _chain.yaml                 ← CONTRACT: Defines structure
├── _index.md                   ← DOCS: Auto-generated
├── orchestrators/              ← USER-FACING: Phase entry points
├── skills/                     ← INTERNAL: Called by orchestrators
├── shared/                     ← SUBAGENT: Loaded by spawned agents
└── validation/                 ← SCRIPTS: Validation tools
```

### Key Insight

**Users talk to the parent SKILL.md only.** The parent routes to appropriate children based on user intent. Users never need to know about the internal structure.

---

## Folder Structure

### `orchestrators/`

**Purpose**: User-facing phase entry points.

**Characteristics**:
- Each orchestrator handles ONE phase of the workflow
- Orchestrators coordinate sub-skills
- Users can invoke orchestrators directly via parent routing
- Each has its own folder with SKILL.md

**Example**:
```
orchestrators/
├── create-research-project/    # Phase 1
│   ├── SKILL.md
│   ├── references/
│   └── scripts/
└── execute-research-project/   # Phase 2
    ├── SKILL.md
    ├── references/
    └── scripts/
```

### `skills/`

**Purpose**: Sub-skills called by orchestrators.

**Characteristics**:
- Called by orchestrators, not directly by users
- Each handles one specific task
- May have scripts, references, etc.
- Routable via parent for direct access if needed

**Example**:
```
skills/
├── paper-search/
│   ├── SKILL.md
│   └── scripts/
│       └── paper_search.py
├── pdf-preprocess/
│   ├── SKILL.md
│   └── scripts/
└── paper-analyze/
    └── SKILL.md
```

### `shared/`

**Purpose**: Methodologies loaded by subagents, NEVER directly.

**Characteristics**:
- Loaded by spawned subagents
- Contains reusable methodology
- SKILL.md has "DO NOT LOAD DIRECTLY" warning
- Parent routing should NOT route here

**Example**:
```
shared/
└── paper-analyze-core/
    ├── SKILL.md           # Has warning header
    └── references/
        └── analysis_log_template.md
```

### `validation/`

**Purpose**: Validation scripts for the chain.

**Characteristics**:
- Python scripts for output validation
- Called by orchestrators or externally
- Use `_chain.yaml` contract as source of truth

**Example**:
```
validation/
├── validate_analysis.py
└── validate_synthesis.py
```

---

## Parent SKILL.md Pattern

The parent SKILL.md is a **router** that:

1. **Has comprehensive trigger phrases** in its description
2. **Routes to children** based on user intent
3. **Documents all children** for reference

### Template Structure

```markdown
---
name: {chain-name}
description: "... Load when user mentions '{triggers}'. This is the MASTER entry point."
type: skill-chain
---

# {Chain Name}

**This is a CONNECT/ROUTER skill** - routes to specialized skills.

## Routing Table

| User Intent | Route To |
|-------------|----------|
| "phrase 1" | `orchestrators/{skill}/SKILL.md` |
| "phrase 2" | `skills/{skill}/SKILL.md` |

## Skill Inventory

### Orchestrators
- [skill-name](orchestrators/skill-name/SKILL.md)

### Sub-Skills
- [skill-name](skills/skill-name/SKILL.md)

### Shared (DO NOT LOAD)
- [skill-name](shared/skill-name/SKILL.md)
```

---

## Path Conventions

### Relative Paths

Within a skill-chain, use **relative paths**:

| From | To | Path |
|------|-----|------|
| Parent | Orchestrator | `orchestrators/{name}/SKILL.md` |
| Parent | Sub-skill | `skills/{name}/SKILL.md` |
| Orchestrator | Sub-skill | `../../skills/{name}/SKILL.md` |
| Sub-skill | Parent | `../../SKILL.md` |
| Sub-skill | Sibling | `../{name}/SKILL.md` |

### Never Use Absolute Paths

❌ `03-skills/research-pipeline/skills/paper-search/SKILL.md`
✓ `../../skills/paper-search/SKILL.md`

---

## Naming Conventions

### Chain Names
- Use **kebab-case**: `research-pipeline`, `interview-analysis`
- Be descriptive but concise

### Orchestrator Names
- Action-oriented: `create-{thing}`, `execute-{thing}`, `run-{thing}`
- Phase-indicative: `prepare-{project}`, `analyze-{project}`

### Sub-Skill Names
- Noun-verb: `paper-search`, `pdf-preprocess`, `paper-analyze`
- Clear function: what does this skill DO?

### Shared Methodology Names
- Suffix with `-core`: `paper-analyze-core`, `transcript-analyze-core`
- Indicates it's a methodology, not a standalone skill

---

## Anti-Patterns

### ❌ Flat Structure

```
03-skills/
├── create-research-project/
├── execute-research-project/
├── paper-search/
├── paper-analyze/
└── paper-synthesize/
```

**Problem**: No grouping, hard to understand relationships.

### ❌ Direct Loading of Shared

```markdown
# In orchestrator:
Load: shared/paper-analyze-core/SKILL.md
```

**Problem**: Shared methodologies are for subagents only. The orchestrator should spawn a subagent that loads the methodology.

### ❌ Circular Dependencies

```
orchestrators/a/ uses skills/b/
skills/b/ uses orchestrators/a/
```

**Problem**: Creates infinite loops. Skills should have clear hierarchy.

---

## Migration from Flat to Nested

When converting existing flat skills to nested:

1. **Create parent folder** (`03-skills/{chain-name}/`)
2. **Create subfolders** (`orchestrators/`, `skills/`, `shared/`, `validation/`)
3. **Move skills** using `git mv` to preserve history
4. **Create parent SKILL.md** with routing table
5. **Create `_chain.yaml`** contract
6. **Update internal paths** (relative paths from new locations)
7. **Generate `_index.md`** documentation

### Using `git mv`

```bash
# Preserve git history
git mv 03-skills/paper-search 03-skills/research-pipeline/skills/paper-search
```

---

## Quality Checklist

Before completing a skill-chain, verify:

### Structure
- [ ] Parent SKILL.md exists with routing table
- [ ] `_chain.yaml` contract exists
- [ ] All orchestrators in `orchestrators/`
- [ ] All sub-skills in `skills/`
- [ ] Shared methodologies in `shared/`

### Parent SKILL.md
- [ ] Has `type: skill-chain` in frontmatter
- [ ] Has comprehensive trigger phrases in description
- [ ] Has routing table for all child skills
- [ ] Lists all children with links
- [ ] Notes which skills are "DO NOT LOAD DIRECTLY"

### Contract
- [ ] All skills listed with correct paths
- [ ] Outputs defined for orchestrators
- [ ] Gates defined between phases
- [ ] Schemas defined if needed

### Child Skills
- [ ] Reference parent with relative path
- [ ] Orchestrators list their sub-skills
- [ ] Sub-skills note their calling orchestrator
- [ ] Shared skills have "DO NOT LOAD" warning

---

## See Also

- [Contract Schema](contract-schema.md) - Full contract format
- [Research Pipeline](../../../research-pipeline/SKILL.md) - Reference implementation
- [Create Skill-Chain](../SKILL.md) - Interactive generator
