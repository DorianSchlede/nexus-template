# Skill-Chain Contract Schema

**Version**: 1.0
**Format**: YAML

---

## Overview

The `_chain.yaml` contract defines the complete structure, skills, outputs, and validation rules for a skill-chain. This file is used by:

1. **Skill discovery** - Understanding what skills exist in the chain
2. **Validation tools** - Verifying chain execution produces expected outputs
3. **Documentation generators** - Auto-generating skill-chain docs

---

## Contract Location

```
03-skills/{chain-name}/
├── SKILL.md              # Parent router (references contract)
├── _chain.yaml           # ← CONTRACT FILE
├── _index.md             # Generated documentation
└── ...
```

---

## Full Schema

```yaml
# Required: Chain identification
name: string                    # kebab-case chain name (e.g., "research-pipeline")
version: string                 # Semantic version (e.g., "1.0", "2.1.0")
description: string             # Human-readable description

# Auto-generated
generated: ISO8601              # Generation date (YYYY-MM-DD)

# Required: Structure definition
structure:
  type: nested                  # Always "nested" for skill-chains
  parent_skill: SKILL.md        # Path to parent router
  subfolders:                   # Standard subfolders
    - orchestrators             # User-facing phase skills
    - skills                    # Sub-skills called by orchestrators
    - shared                    # Shared methodologies (subagent-only)
    - validation                # Validation scripts

# Required: Skill definitions
skills:
  - id: string                  # Skill name (kebab-case)
    phase: int                  # Phase number (1, 2, 3...)
    type: orchestrator|sub-skill|shared-methodology
    path: string                # Relative path from chain root
    description: string         # What this skill does

    # For orchestrators only:
    uses: [string]              # Sub-skills this orchestrator uses

    # For sub-skills only:
    called_by: string           # Orchestrator that calls this skill

    # For shared only:
    note: string                # Usually "DO NOT LOAD DIRECTLY"

    # Output definition (optional, typically for orchestrators):
    produces:
      - path: string            # Output file path (glob patterns allowed)
        required: bool          # true if output must exist
        schema: string          # Reference to schemas section
        min_count: int          # Minimum matches for glob patterns
        validates:              # Field-level validation rules
          - field: string
            equals|in|exists: value

    # Dependency definition (optional):
    requires:
      - skill: string           # Skill ID that must complete first
        outputs: all|[paths]    # Which outputs are needed

    # Gate reference (optional):
    gate: string                # Reference to gates section

# Optional: Schema definitions for output validation
schemas:
  schema_name:
    required_fields: [string]   # YAML frontmatter fields that must exist
    optional_fields: [string]   # YAML frontmatter fields that may exist

# Optional: Gate definitions for phase transitions
gates:
  gate_name:
    after_phase: int            # Phase number this gate follows
    checks: [string]            # Boolean expressions that must all pass
```

---

## Field Details

### `name`
- **Type**: String (kebab-case)
- **Required**: Yes
- **Example**: `"research-pipeline"`, `"interview-analysis"`

### `version`
- **Type**: String (semver)
- **Required**: Yes
- **Example**: `"1.0"`, `"2.1.0"`

### `structure.type`
- **Type**: String
- **Required**: Yes
- **Value**: Always `"nested"` for skill-chains

### `skills[].type`
- **Type**: Enum
- **Values**:
  - `orchestrator` - User-facing phase coordinator
  - `sub-skill` - Called by orchestrators
  - `shared-methodology` - Loaded by subagents only

### `skills[].produces[].path`
- **Type**: String
- **Supports**: Glob patterns (`*`, `**`)
- **Examples**:
  - `"02-resources/_briefing.md"` - Exact file
  - `"02-resources/papers/*/_metadata.json"` - Glob pattern

### `skills[].produces[].validates`
- **Type**: Array of validation rules
- **Rule Types**:
  - `field: "name"` + `equals: "value"` - Field must equal value
  - `field: "name"` + `in: [values]` - Field must be in list
  - `has_yaml_frontmatter: true` - File must have YAML frontmatter

### `gates[].checks`
- **Type**: Array of boolean expressions
- **Examples**:
  - `"papers_with_chunks > 0"`
  - `"_briefing.md exists"`
  - `"overview.md status == READY_FOR_EXECUTION"`

---

## Example Contract

```yaml
name: interview-analysis
version: "1.0"
description: "Analyze interview transcripts for themes and insights"
generated: 2025-12-27

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
    description: "Phase 1: Import and preprocess transcripts"
    uses:
      - transcript-import
      - transcript-preprocess
    produces:
      - path: "02-resources/_briefing.md"
        required: true
      - path: "02-resources/transcripts/*/_metadata.json"
        required: true
        min_count: 1
    gate: readiness-gate

  - id: transcript-import
    phase: 1
    type: sub-skill
    path: skills/transcript-import/SKILL.md
    called_by: prepare-interview-project

  - id: transcript-preprocess
    phase: 1
    type: sub-skill
    path: skills/transcript-preprocess/SKILL.md
    called_by: prepare-interview-project

  - id: execute-interview-analysis
    phase: 2
    type: orchestrator
    path: orchestrators/execute-interview-analysis/SKILL.md
    description: "Phase 2: Analyze and synthesize themes"
    requires:
      - skill: prepare-interview-project
        outputs: all
    uses:
      - transcript-analyze
      - theme-synthesize
    produces:
      - path: "02-resources/transcripts/*/index.md"
        required: true
      - path: "04-outputs/_synthesis.md"
        required: true

  - id: transcript-analyze-core
    type: shared-methodology
    path: shared/transcript-analyze-core/SKILL.md
    note: "DO NOT LOAD DIRECTLY - loaded by subagents"

gates:
  readiness-gate:
    after_phase: 1
    checks:
      - "transcripts_preprocessed > 0"
      - "_briefing.md exists"
```

---

## Validation Rules Reference

### File Existence
```yaml
produces:
  - path: "path/to/file.md"
    required: true  # File must exist
```

### Glob with Minimum Count
```yaml
produces:
  - path: "papers/*/_metadata.json"
    required: true
    min_count: 1  # At least 1 match required
```

### YAML Frontmatter Validation
```yaml
produces:
  - path: "papers/*/index.md"
    validates:
      - has_yaml_frontmatter: true
```

### Field Value Validation
```yaml
produces:
  - path: "03-working/_selection_log.md"
    validates:
      - field: "approved_by_user"
        equals: true
```

### Field Enum Validation
```yaml
produces:
  - path: "papers/*/_analysis_log.md"
    validates:
      - field: "schema_version"
        in: ["2.0", "2.1", "2.2"]
```

---

## Gate Expression Syntax

Gates use simple boolean expressions:

| Expression | Meaning |
|------------|---------|
| `file.md exists` | File exists in project |
| `count > N` | Count variable exceeds N |
| `field == value` | Field equals value |
| `field != value` | Field not equals value |

**Examples**:
```yaml
gates:
  readiness-gate:
    checks:
      - "papers_with_chunks > 0"
      - "_briefing.md exists"
      - "overview.md status == READY_FOR_EXECUTION"
```

---

## Integration with Validation Tools

The contract is read by `validate-skill-chain` to:

1. **Check skill existence** - All paths in `skills[].path` must exist
2. **Check outputs** - All `produces[].path` files must exist (if required)
3. **Validate fields** - Run `validates` rules on output files
4. **Check gates** - Evaluate gate conditions for phase transitions

---

**See Also**:
- [Nested Skill Patterns](nested-skill-patterns.md) - Best practices
- [Research Pipeline Contract](../../../research-pipeline/_chain.yaml) - Reference implementation
