# Templates & Artifacts Patterns - Research Pipeline Analysis

**Source**: Subagent analysis of `03-skills/research-pipeline/` templates and shared artifacts
**Agent ID**: a3038f3
**Date**: 2026-01-07

---

## 1. Architecture Overview

### Three-Phase, Seven-Level System

```
Phase 1: PLANNING          Phase 2: ANALYSIS           Phase 3: SYNTHESIS
├─ _briefing.md            ├─ _analysis_log.md         ├─ Level 1: Routing
├─ _analysis_kit.md        ├─ index.md                 ├─ Level 2: Allocation
├─ _extraction_guide.md    └─ Validation               ├─ Level 3: Prompts
└─ plan.md (allocation)                                ├─ Level 4: Extraction
                                                       ├─ Level 5: Verification
                                                       ├─ Level 6: Aggregation
                                                       └─ Level 7: Report
```

---

## 2. Core Template Structures

### 2.1 _briefing.md (Research Definition)

**Purpose**: Single source of truth for extraction requirements

```yaml
---
research_question: "What are foundational ontologies for digital work?"
research_purpose: "Validate 8-entity hypothesis for UDWO metamodel"
domain: "Ontology Engineering"

extraction_schema:
  - field: entity_types
    description: "Core entities defined in ontology"
    priority: high
  - field: ai_integration
    description: "How ontology enables AI agents"
    priority: medium

focus_areas:
  - "Foundational concepts"
  - "Entity relationships"

skip_sections:
  - "Acknowledgments"
  - "Author Contributions"
---
```

**Key Patterns**:
- **AI Field Generation**: Step 2 analyzes RQ and suggests domain-specific fields
- **Research Purpose Context**: Helps subagents understand "why" for prioritization
- **Priority Levels**: high/medium for allocation planning

### 2.2 _analysis_kit.md (Subagent Context)

**Purpose**: Consolidates everything subagents need

```yaml
---
project_id: "{project_id}"
project_path: "02-projects/{project_id}"
generated: "{date}"
schema_version: "2.0"
---

## Research Question
{from _briefing.md}

## Research Purpose
**WHY this research matters:**
{research_purpose}

## Synthesis Goals
**What synthesis will aggregate:**
1. **Compare**: {comparison_goal}
2. **Identify**: {identification_goal}
3. **Analyze**: {analysis_goal}

## Extraction Schema
| Field | Description | Priority |

## Output Requirements

### 1. Analysis Log (_analysis_log.md)
- Record evidence spans for each finding
- Chunk reference for every extraction

### 2. Index File (index.md)
**REQUIRED YAML frontmatter fields:**
---
paper_id: "{paper_id}"
chunks_expected: {N}
chunks_read: {N}
analysis_complete: true
---
```

### 2.3 _extraction_guide.md (Quality Standards)

**Purpose**: Ensure consistent extraction quality

```markdown
## Format Rules

| Type | When to Use | Format |
|------|-------------|--------|
| Array of strings | Multiple discrete items | `["Item 1", "Item 2"]` |
| Array of objects | Items with properties | `[{name: "X", source: "Chunk 2"}]` |

## Extraction Quality Criteria

### DO
- Use exact terminology from paper
- Include chunk reference for every extraction
- Quote significant definitions

### DON'T
- Paraphrase when exact quote is better
- Merge distinct concepts
- Infer what paper doesn't state

## Confidence Levels

| Level | When to Use |
|-------|-------------|
| **high** | Explicit statement, direct quote |
| **medium** | Clear implication, consistent context |
| **low** | Inference, interpretation, ambiguous |

**Always flag low confidence**: `[LOW CONFIDENCE: reason]`
```

---

## 3. Analysis Output Templates

### 3.1 _analysis_log.md (Schema v2.3)

**Purpose**: Structured validation log for programmatic verification

```yaml
---
schema_version: "2.3"

# METADATA
paper_id: ""
paper_title: ""
analyzer: "claude-opus-4"
analysis_started: ""
analysis_completed: ""

# STEP COMPLETION
steps:
  step1_read_briefing:
    completed: false
    briefing_path: ""
    research_question: ""

  step2_read_metadata:
    completed: false
    chunks_expected: 0

  step3_analyze_chunks:
    completed: false
    chunks_total: 0
    chunks_read: []
    chunk_evidence: {}  # 2-POINT ANTI-HALLUCINATION

  step4_compile_index:
    completed: false
    yaml_valid: false

  step5_validate:
    completed: false
    checklist: {}

# ERROR RECOVERY
error_handling:
  timeout_occurred: false
  partial_success: false
  chunks_completed: []
  chunks_remaining: []

# EXTRACTION TRACKING
extractions: {}
# extractions:
#   handover_patterns:
#     - name: "Auto-Reply Mechanism"
#       chunk: 1
#       lines: "127-134"
#       quote: "First 150 chars proving extraction..."
---
```

### 3.2 index.md (Analysis Output)

**Purpose**: Analysis index with YAML frontmatter + chunk navigation

```yaml
---
paper_id: ""
title: ""
authors: []
year: null
chunks: 0
tokens_estimated: 0
analyzed_at: ""

# CHUNK-LEVEL FIELD ASSESSMENT
chunk_index:
  1:
    token_count: 12500
    fields_found:
      entity_types: true      # true|partial|false
      methodology: false

# EXTRACTION FIELDS
entity_types:
  - item: "Endurant (Continuant)"
    chunk: 1
    lines: "128-133"
    quote: "An entity wholly present at any time..."

# STRUCTURED N/A
methodology:
  - item: "NOT_FOUND"
    chunk: null
    lines: null
    reason: "Paper does not discuss research methodology"
---

# {Paper Title} - Analysis Index

## Chunk Navigation

### Chunk 1: {Section Title}
- **Summary**: 2-3 sentence description
- **Key concepts**: [concept1, concept2]
- **Load when**: "User asks about X"
```

---

## 4. Shared Constants & Contracts

### 4.1 constants.py (Single Source of Truth)

```python
# Token estimation formula - CONSISTENT EVERYWHERE
TOKEN_FORMULA = lambda chars: chars // 4

# Current schema version
SCHEMA_VERSION = "2.3"

# Resource limits
MAX_TOKENS_PER_BATCH = 70000        # Per subagent
MAX_CONCURRENT_SUBAGENTS = 15       # Parallel execution

# Verification
VERIFICATION_SAMPLE_RATE = 0.10     # 10% of patterns
VERIFICATION_PASS_THRESHOLD = 0.90  # 90% must verify

# Field states
FIELD_STATE_TRUE = True
FIELD_STATE_PARTIAL = "partial"
FIELD_STATE_FALSE = False

# Sparsity warning
SPARSITY_THRESHOLD = 0.80           # Warn if field matches >80%
```

### 4.2 script_registry.py (7-Level Architecture)

| Level | Script | Purpose |
|-------|--------|---------|
| 1 | build_synthesis_routing.py | Route fields to chunks via chunk_index.fields_found |
| 2 | calculate_subagent_allocation.py | Greedy bin-pack chunks into 70K token batches |
| 3 | generate_subagent_prompts.py | Generate prompts with INPUT CONTRACT |
| 4 | (Subagent execution) | Extract patterns from chunks |
| 5 | verify_subagent_output.py | Verify quotes at cited line numbers |
| 6 | aggregate_patterns.py | Fuzzy deduplicate, preserve sources |
| 7 | (Final report generation) | Synthesize findings with citations |

---

## 5. Prompt Engineering Patterns

### 5.1 Field Generation Pattern

```
AI: Based on your research question, I'll suggest extraction fields.

   ANALYZING RESEARCH QUESTION...
   Domain detected: {detected_domain}
   Key concepts: {extracted_concepts}

   SUGGESTED FIELDS:
   ┌─────────────────────────────────────┐
   │ 1. {field_1} - {description_1}      │
   │ 2. {field_2} - {description_2}      │
   └─────────────────────────────────────┘

   FIELD QUALITY CHECK:
   ⚠ "{generic_field}" is generic
   ✓ All others are domain-specific

   Commands: 'ok' | 'remove N' | 'add ...' | 'edit N: ...'
```

### 5.2 Subagent Prompt Template

```python
Task(
  subagent_type="general-purpose",
  prompt=f"""
## Paper Analysis Task: {paper_id}

## INPUT CONTRACT (STRICT)
{INPUT_CONTRACT_TEXT}

## CONTEXT
Research Purpose: {research_purpose}
Synthesis Goals: {synthesis_goals}

## PROCESSING CONTRACT
1. Read files IN ORDER listed in INPUT CONTRACT
2. For EVERY chunk, assess EVERY field: true/partial/false
3. Extract items only for true/partial fields
4. Record evidence (start + end) for each chunk

## OUTPUT CONTRACT
Write these files:
1. `{paper_path}/_analysis_log.md` (Schema v2.3)
2. `{paper_path}/index.md` (REQUIRED YAML frontmatter)
"""
)
```

---

## 6. Anti-Hallucination Patterns

### 6.1 2-Point Evidence Sampling

```yaml
chunk_evidence:
  1:
    start: "First ~100 chars AFTER header line"
    end: "Last ~100 chars of chunk"
```

**Validation**:
```python
for chunk_num, evidence in chunk_evidence.items():
    chunk_content = read_file(f"{paper}__{chunk_num}.md")
    content_after_header = chunk_content.split('\n', 1)[1]

    assert content_after_header[:100].strip() == evidence['start'].strip()
    assert chunk_content[-100:].strip() == evidence['end'].strip()
```

**Why 2-point?**:
- Start ⟹ confirms read beginning
- End ⟹ confirms read to completion
- Simpler than 3-point/hash approaches

### 6.2 Extraction Tracking with Chunk:Line References

```yaml
extractions:
  handover_patterns:
    - name: "Auto-Reply Mechanism"
      chunk: 1
      lines: "127-134"
      quote: "Once an agent receives a message..."
      confidence: "high"
```

**Verification**: Quote must appear in source at specified lines (±5 tolerance).

### 6.3 Timeout Partial Save

```yaml
error_handling:
  timeout_occurred: true
  partial_success: true
  chunks_completed: [1, 2, 3]
  chunks_remaining: [4, 5]
  recovery_notes: "Resume from chunk 4..."
```

---

## 7. Configuration Patterns

### 7.1 _chain.yaml (Skill-Chain Contract)

```yaml
name: research-pipeline
version: "1.0"

skills:
  - id: create-research-project
    phase: 1
    produces:
      - path: "02-resources/_briefing.md"
      - path: "02-resources/_analysis_kit.md"
    gate: readiness-gate

  - id: analyze-research-project
    phase: 2
    requires:
      - skill: create-research-project
        outputs: all
    produces:
      - path: "02-resources/papers/*/index.md"
    gate: completion-gate

gates:
  readiness-gate:
    checks:
      - "papers_with_chunks > 0"
      - "_briefing.md exists"

  completion-gate:
    checks:
      - "all papers have index.md"
      - "validation pass rate > 80%"
```

---

## 8. Reusable Artifact Inventory

| Artifact | Location | Purpose |
|----------|----------|---------|
| `_briefing.md` template | Generated | Research definition |
| `_analysis_kit.md` template | `references/` | Subagent context |
| `_extraction_guide.md` template | `shared/references/` | Quality standards |
| `analysis_log_template.md` | `shared/references/` | Validation schema |
| `index_template.md` | `shared/references/` | Output format |
| `constants.py` | `shared/contracts/` | Configuration |
| `script_registry.py` | `shared/contracts/` | Metadata + docs |
| `_chain.yaml` | Root | Skill-chain contract |

---

## 9. Key Gaps Addressed

| Gap | Pattern | Solution |
|-----|---------|----------|
| G1: Field calibration | 3-state fields_found | true/partial/false in chunk_index |
| G3: Token formula | constants.py | `chars // 4` everywhere |
| G5: Field generation | AI-driven | Suggests domain-specific fields |
| G13: File access | INPUT CONTRACT | Whitelist approach |
| G15: Quote verification | Chunk:line matching | ±5 line tolerance |
| G16: Timeout recovery | Partial save | chunks_completed/remaining |
| G18: Structured N/A | NOT_FOUND items | Distinguished from errors |
| G19: Sparsity warning | THRESHOLD = 0.80 | Flag fields matching >80% |
| G22a: Research purpose | Context injection | WHY in _briefing.md |
| G22b: Synthesis goals | Context injection | WHAT in _analysis_kit.md |

---

## 10. Best Practices Observed

1. **Single Source of Truth**: constants.py prevents drift
2. **Explicit Contracts**: INPUT/OUTPUT/PROCESSING contracts
3. **Schema Versioning**: v2.3 with backward compatibility
4. **Progressive Disclosure**: Frontmatter (synthesis) vs analysis_log (validation)
5. **Structured Uncertainty**: LOW CONFIDENCE flags, Structured N/A
6. **Deterministic Allocation**: Pre-calculated in Phase 1, read in Phase 2
7. **Sampling-based Verification**: 10% at Level 5 (practical, not exhaustive)
8. **Context Injection**: research_purpose + synthesis_goals
9. **Recovery Mechanisms**: Partial save on timeout, resume mode
10. **Token Budgeting**: Per-batch limits, final report budget upfront

---

*Generated by templates/artifacts subagent analysis*
