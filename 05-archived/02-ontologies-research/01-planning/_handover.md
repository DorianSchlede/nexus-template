# CRITICAL HANDOVER: Synthesize Research Project Skill Design

**Updated**: 2025-12-28T17:45:00
**Priority**: CRITICAL - CONTEXT HANDOVER
**Status**: ✅ SKILL CREATED - Ready to test on ontologies-research

---

## COMPLETED ACTIONS

1. ✅ Created `03-skills/research-pipeline/orchestrators/synthesize-research-project/SKILL.md`
2. ✅ Renamed `execute-research-project` → `analyze-research-project`
3. ✅ Removed synthesis from `analyze-research-project` (now analysis only)
4. ✅ Updated `research-pipeline/SKILL.md` routing table

---

## IMMEDIATE CONTEXT

We designed and implemented a NEW skill: `synthesize-research-project`.

The 3-skill chain is now complete:
- `create-research-project` - Phase 1: Acquisition
- `analyze-research-project` (renamed from execute) - Phase 2: Paper-level analysis only
- `synthesize-research-project` (NEW) - Phase 3: Cross-paper synthesis

---

## THE 3-SKILL CHAIN

```
create-research-project  →  analyze-research-project  →  synthesize-research-project
(Phase 1: Acquisition)      (Phase 2: Analysis)          (Phase 3: Synthesis)
        ↓                           ↓                            ↓
    _briefing.md               index.md per paper         _synthesis_report.md
    chunks ready               extracted frontmatter      FULL MARKDOWN REPORT
```

---

## SYNTHESIZE-RESEARCH-PROJECT DESIGN (APPROVED)

### Core Principle
**AI reads ALL chunk details. No shortcuts. Full citations preserved through every level.**

### Architecture: 4-Level Hierarchical Synthesis

```
LEVEL 1: ROUTING (Script)
├── Input: All index.md files + _briefing.md
├── Script: prepare_synthesis_chunks.py (EXISTS)
├── Output: _synthesis_routing.yaml
└── Calculates: batches of ~5-6 chunks per subagent

LEVEL 2: PARALLEL BATCH EXTRACTION (Subagents)
├── For each batch: spawn subagent
├── Subagent reads FULL chunk content (not just frontmatter!)
├── Extracts patterns with chunk:line citations
├── Includes QUOTES, context, full detail
└── Output: 03-working/_batch_{field}_{N}.md (MARKDOWN)

LEVEL 3: FIELD AGGREGATION (Subagent per field)
├── Reads all _batch_{field}_*.md files
├── Merges patterns, preserves ALL sources
├── Groups by theme, notes conflicts
└── Output: 04-outputs/_synthesis_{field}.md (MARKDOWN)

LEVEL 4: FINAL REPORT (Orchestrator or Subagent)
├── Reads all _synthesis_{field}.md files
├── Generates cross-field insights
├── Full markdown with inline citations
├── Block quotes from sources
├── Complete reference list
└── Output: 04-outputs/_synthesis_report.md (FULL MARKDOWN REPORT)
```

### Citation Format (PRESERVED AT EVERY LEVEL)
```
Paper-ID (Chunk N:Line-Line)
Example: 16-KG-Agent (Chunk 1:240-259)
```

---

## OUTPUT REQUIREMENTS

### 1. EVERY LEVEL OUTPUTS MARKDOWN (NOT YAML)

### 2. Batch Extraction Must Include:
- Pattern name
- **Source**: Paper-ID (Chunk N:Line-Line)
- **Description**: Full detail from chunk
- **Quote**: Exact text from source
- **Context**: Surrounding information

### 3. Field Synthesis Must Include:
- Executive summary
- Theme groupings
- Comparison tables with sources
- Cross-paper insights
- Conflicts/debates
- Gaps

### 4. Final Report Must Include:
- Title + metadata
- Executive summary with inline citations [Paper-ID]
- Key findings with evidence tables
- Block quotes from original chunks
- Cross-field insights
- Recommendations
- **Full reference list** (all papers with titles, years)

---

## SCRIPTS ALREADY CREATED

| Script | Location | Purpose |
|--------|----------|---------|
| `aggregate_frontmatter.py` | paper-query/scripts/ | Aggregate all index.md frontmatter |
| `prepare_synthesis_chunks.py` | paper-query/scripts/ | Generate routing table |
| `aggregate_field.py` | paper-synthesize/scripts/ | Aggregate single field with sources |

---

## SUBAGENT PROMPT TEMPLATES

### Batch Extraction Subagent
```
BATCH EXTRACTION: {field_name} (Batch {N} of {total})

## Your Assignment
Papers: {paper_list}
Chunks to read (FULL CONTENT):
  - {paper_1}/{paper_1}_{chunk}.md
  - {paper_2}/{paper_2}_{chunk}.md
  ...

## Instructions
1. Read EACH chunk completely - do not skim
2. Extract ALL {field_name} patterns
3. For EVERY pattern include:
   - Source: Paper-ID (Chunk N:Line-Line)
   - Description: Full detail from chunk
   - Quote: "{exact text}"
   - Context: Surrounding information

## Output
Write: 03-working/_batch_{field}_{N}.md

---
batch_id: {N}
field: {field_name}
papers_read: [list]
chunks_read: {count}
patterns_found: {count}
---

## Patterns Extracted

### Pattern: {name}
- **Source**: Paper-ID (Chunk N:Line-Line)
- **Description**: {full detail}
- **Quote**: "{exact text from chunk}"
- **Context**: {surrounding info}

### Pattern: {name2}
...
```

### Aggregation Subagent
```
AGGREGATE SYNTHESIS: {field_name}

## Input Files
Read ALL batch files:
  - 03-working/_batch_{field}_1.md
  - 03-working/_batch_{field}_2.md
  - ... (all batches)

## Instructions
1. Read ALL batch files completely
2. Merge patterns - preserve ALL source citations
3. Group similar patterns (dedupe names, keep all sources)
4. Create comparison table with multi-paper sources
5. Identify themes across papers
6. Note conflicts/contradictions between papers
7. Identify gaps (what's NOT covered)

## Output
Write: 04-outputs/_synthesis_{field_name}.md

---
field: "{field_name}"
synthesized_at: "{timestamp}"
papers_included: [full list]
patterns_found: {count}
batches_merged: {count}
---

# {Field Name} - Cross-Paper Synthesis

## Executive Summary
{2-3 paragraphs with inline citations}

## Themes

### Theme 1: {name}
{description}

| Paper | Evidence | Key Insight |
|-------|----------|-------------|
| Paper-ID | Chunk N:Line | insight |

## All Patterns

### Pattern: {name}
**Found in**: Paper-A (1:100), Paper-B (2:50), Paper-C (1:200)
**Description**: {merged from all sources}

## Conflicts & Debates
{where papers disagree}

## Gaps
{what's not covered}
```

### Final Report Subagent
```
FINAL SYNTHESIS REPORT

## Input Files
Read all field syntheses:
  - 04-outputs/_synthesis_entity_types.md
  - 04-outputs/_synthesis_framework_comparison.md
  - 04-outputs/_synthesis_ai_integration.md
  - ... (all field syntheses)

Also read:
  - 02-resources/_briefing.md (research question)

## Instructions
1. Read ALL field synthesis files
2. Answer the research question with evidence
3. Identify cross-field patterns
4. Include inline citations: [Paper-ID (Chunk:Line)]
5. Include block quotes for key evidence
6. Generate full reference list

## Output
Write: 04-outputs/_synthesis_report.md

---
synthesized_at: "{timestamp}"
research_question: "{RQ}"
papers_included: {count}
fields_synthesized: [list]
---

# Research Synthesis: {Title}

## Executive Summary

{3-4 paragraphs answering research question with inline citations}

## Key Findings

### Finding 1: {title}

{description with evidence}

| Source | Evidence | Implication |
|--------|----------|-------------|
| Paper-ID | Chunk:Line | text |

> "Direct quote from source demonstrating finding"
> — Paper-ID (Chunk N:Line-Line)

### Finding 2: {title}
...

## Cross-Field Insights

{patterns that emerge across multiple fields}

## Recommendations

Based on this synthesis:
1. {recommendation with evidence}
2. {recommendation with evidence}

## Limitations

{what this synthesis cannot address}

## References

| Paper ID | Title | Year | Chunks Cited |
|----------|-------|------|--------------|
| 16-KG-Agent | KG-Agent: An Efficient... | 2024 | 1:240, 2:100 |
| 23-UFO | Towards Ontological... | 2015 | 1:173, 1:191 |
...
```

---

## ONTOLOGIES PROJECT STATUS

| Metric | Value |
|--------|-------|
| Papers analyzed | 23 |
| Valid index.md | 21 |
| Routing generated | YES (_synthesis_routing.yaml) |
| Batches calculated | 15 fields, varying chunks |
| Synthesis started | 2 files (manual, incomplete) |

### Files Created So Far
- `04-outputs/_synthesis_entity_taxonomy.md` (partial)
- `04-outputs/_synthesis_framework_comparison.md` (partial)
- `02-resources/_synthesis_routing.yaml` (complete)
- `02-resources/_aggregated_index.json` (complete)

---

## FILES TO READ ON RESUME

1. **This file**: `02-projects/02-ontologies-research/01-planning/_handover.md`
2. **Routing**: `02-resources/_synthesis_routing.yaml`
3. **Briefing**: `02-resources/_briefing.md`
4. **Existing skills**:
   - `03-skills/research-pipeline/orchestrators/create-research-project/SKILL.md`
   - `03-skills/research-pipeline/orchestrators/execute-research-project/SKILL.md`
5. **Paper-query skill**: `03-skills/research-pipeline/skills/paper-query/SKILL.md`

---

## NEXT ACTIONS (IN ORDER)

1. **Create `synthesize-research-project/SKILL.md`** in `03-skills/research-pipeline/orchestrators/`
   - Use the design and templates above
   - Include step-by-step workflow
   - Include all subagent prompts

2. **Rename `execute-research-project` → `analyze-research-project`**
   - Remove PHASE C (Synthesis) completely
   - Update description and handoff

3. **Update skill chain references**
   - create → analyze → synthesize

4. **Test on ontologies-research project**
   - Run full synthesis with new skill
   - Verify citations preserved
   - Generate final report

---

## CRITICAL REMINDERS

1. **NO YAML OUTPUT** - Everything is full markdown
2. **PRESERVE CITATIONS** - Every level keeps Paper-ID (Chunk:Line)
3. **READ FULL CHUNKS** - Subagents read complete chunk content, not summaries
4. **BATCH BY CHUNK COUNT** - Target ~5-6 chunks per batch
5. **QUOTES REQUIRED** - Include exact text from sources
6. **FINAL REPORT = FULL DOCUMENT** - Not a summary, a complete research synthesis

---

## Quick Resume Command

```
"Continue ontologies research - we were designing the synthesize-research-project skill. Read the handover file first."
```

---

*Handover saved 2025-12-28T16:30:00*
