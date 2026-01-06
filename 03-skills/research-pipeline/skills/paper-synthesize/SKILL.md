---
name: paper-synthesize
description: Synthesize insights across analyzed papers in a collection. Load when user says "synthesize collection", "cross-paper analysis", "compare papers", "aggregate findings", or "generate synthesis". Reads all index.md YAML frontmatter and produces synthesis documents.
---

# Paper Synthesize

Generate cross-paper synthesis documents from analyzed paper collections.

## Prerequisites

- All papers in collection must have `index.md` (from paper-analyze)
- Collection must have `_briefing.md` with synthesis types defined

## Workflow

### Step 1: Gather Paper Indexes

1. Read `_briefing.md` to get research question and synthesis types
2. List all paper folders with `index.md`
3. Read YAML frontmatter from each `index.md`
4. Build aggregated view of: topics, methods, findings, limitations

### Step 2: Generate Synthesis Documents

For each synthesis type in `_briefing.md`:

| Type | Output | Purpose |
|------|--------|---------|
| methodology_comparison | `_synthesis_methodology.md` | Compare methods across papers |
| llm_best_practices | `_synthesis_llm_practices.md` | Extract LLM usage patterns |
| evaluation_approaches | `_synthesis_evaluation.md` | Compare quality metrics |
| gaps | `_synthesis_gaps.md` | Identify research gaps |
| themes | `_synthesis_themes.md` | Common themes across papers |

### Step 3: Cross-Paper Analysis

For each synthesis document:

1. **Aggregate**: Collect relevant fields from all index.md files
2. **Compare**: Identify patterns, contradictions, evolution
3. **Synthesize**: Generate insights that span papers
4. **Cite**: Reference specific papers (e.g., "Braun & Clarke 2006")

## Synthesis Document Template

```markdown
# {Synthesis Title}

**Research Question**: {from briefing}
**Papers Analyzed**: {count} papers
**Generated**: {timestamp}

## Overview

[2-3 paragraph synthesis of this aspect across all papers]

## Comparative Analysis

### {Dimension 1}
| Paper | Approach | Notes |
|-------|----------|-------|
| Braun & Clarke 2006 | Six-phase TA | Foundational method |
| ... | ... | ... |

### {Dimension 2}
[Continue comparison across dimensions]

## Key Patterns

1. **Pattern 1**: Description with paper citations
2. **Pattern 2**: Description with paper citations

## Contradictions & Debates

- **Topic**: Paper A argues X, while Paper B argues Y

## Research Gaps

- Gap 1: No papers address...
- Gap 2: Limited evidence for...

## Synthesis Summary

[Key takeaways for this synthesis type]
```

## Execution

### Synthesize Collection

```
User: "Synthesize the TA_LLM collection"

1. Read 04-workspace/papers/TA_LLM/_briefing.md
2. Read all index.md YAML frontmatter (topics, methods, findings, etc.)
3. For each synthesis_type in briefing:
   a. Spawn subagent with aggregated data
   b. Generate _synthesis_{type}.md
4. Report: "Generated 3 synthesis documents"
```

### Single Synthesis Type

```
User: "Generate methodology comparison for TA_LLM"

1. Read all index.md files
2. Generate only _synthesis_methodology.md
```

## Subagent Prompt Template

```
You are generating a cross-paper synthesis.

## Research Question
{research_question from briefing}

## Synthesis Type
{type}: {description from briefing}

## Papers Analyzed
{For each paper, include:}
- Title: {title}
- Authors: {authors}
- Year: {year}
- Topics: {topics}
- Methods: {methods}
- Key Findings: {key_findings}
- Limitations: {limitations}

## Task
Generate a comprehensive synthesis document comparing and contrasting
the {type} across all papers. Follow the synthesis template format.

## Output
Write to: {collection_path}/_synthesis_{type}.md
```

## Token Management

- Read only YAML frontmatter from index.md (not full chunk navigation)
- Each synthesis is independent (can be parallelized)
- Subagent context: ~50k tokens for aggregated metadata

## Error Handling

| Error | Action |
|-------|--------|
| No index.md files | Abort, suggest running paper-analyze first |
| No synthesis_types in briefing | Use default types: themes, gaps |
| Subagent fails | Retry once, log failure |

---

## Synthesis Validation (NEW)

**After generating synthesis, run validation:**

```bash
python 03-skills/research-pipeline/skills/paper-synthesize/scripts/validate_synthesis.py \
  {project_path} --spot-check 10
```

### Required Frontmatter Contract

Every `_synthesis.md` MUST include:

```yaml
---
synthesized_at: "{timestamp}"
research_question: "{RQ}"
papers_included: 38
papers_excluded: 5
papers_read: ["01-autogen", "02-autogen-studio", "..."]  # REQUIRED: actual papers read
total_patterns_extracted:
  handover_patterns: 47
  quality_mechanisms: 32
  prompt_templates: 28
  orchestration_algo: 19
coverage_percentage: 85
---
```

### Validation Checks

| Check | Threshold | Action if Fail |
|-------|-----------|----------------|
| Frontmatter complete | 100% required fields | Regenerate |
| Paper references exist | >90% | Warn |
| Spot-check verification | >70% | Regenerate |
| Coverage | >60% | Warn |

### Subagent Validation Contract

Add to synthesis subagent prompt:

```
VALIDATION CONTRACT:
1. You MUST read ALL index.md files (glob: papers/*/index.md)
2. You MUST list papers_read in frontmatter (actual paper_ids read)
3. Every claim MUST cite paper_id (e.g., "MAPoRL achieves 91%")
4. Include total_patterns_extracted counts in frontmatter
5. I will validate by spot-checking 10 random claims against sources
```

### Two-Pass Synthesis (for high-reliability)

**Pass 1: Aggregation**
- Read all index.md files
- Generate draft synthesis

**Pass 2: Verification**
- Cross-reference 20% of claims
- Flag mismatches
- Add confidence score

See: `references/synthesis_validation_contract.md` for full specification.

---

## Scripts

### validate_synthesis.py

Validates synthesis documents after generation.

```bash
python 03-skills/research-pipeline/skills/paper-synthesize/scripts/validate_synthesis.py \
  {project_path} --spot-check 10
```

### aggregate_field.py

Aggregates a specific extraction field across all papers with full source citations. Reads ALREADY EXTRACTED data from index.md frontmatter - does NOT re-analyze papers.

**Usage:**
```bash
# Aggregate a single field
python 03-skills/research-pipeline/skills/paper-synthesize/scripts/aggregate_field.py \
  {project_path} --field entity_types

# With custom output file
python 03-skills/research-pipeline/skills/paper-synthesize/scripts/aggregate_field.py \
  {project_path} --field ai_integration --output _synthesis_ai.md
```

**What it does:**
1. Reads all `index.md` files in `02-resources/papers/*/`
2. Extracts the specified field from YAML frontmatter
3. Aggregates items across all papers
4. Outputs markdown with full source citations (Paper-ID, Chunk:Line)

**Example output:**
```markdown
# Aggregated: entity_types

## Items (47 total from 23 papers)

### Endurant (Continuant)
- **Source**: 02-Knowledge_Graphs (Chunk 2:128-133)
- **Quote**: "An entity wholly present at any time..."

### Perdurant (Occurrent)
- **Source**: 05-DOLCE (Chunk 1:89-95)
- **Quote**: "Events and processes that unfold over time"
```

---

**Version**: 2.1 (2025-12-29)
**Changes**:
- v2.0: Synthesis validation contract, validation script, two-pass synthesis
- v2.1: Documented aggregate_field.py script
