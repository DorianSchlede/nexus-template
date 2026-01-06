---
name: paper-analyze-core
description: "SHARED METHODOLOGY for paper analysis subagents. DO NOT LOAD DIRECTLY. This skill is loaded by the paper-analyze orchestrator and provides the analysis methodology, index.md template, file reading rules, and quality criteria for all paper analysis subagents."
---

# Paper Analyze Core

**⚠️ DO NOT LOAD DIRECTLY** - This skill is loaded by `paper-analyze` orchestrator into subagents.

Shared methodology foundation for consistent paper analysis across all subagents.

---

## MUST READ FILES (Orchestrator Provides Paths)

**Before starting analysis, read these files IN ORDER:**

| Order | File | Purpose | Path Provided By |
|-------|------|---------|------------------|
| 1 | `_analysis_kit.md` | Research question, extraction schema, validation contract | Orchestrator: `{project}/02-resources/_analysis_kit.md` |
| 2 | `_extraction_guide.md` | Field-specific examples, controlled vocabulary | Orchestrator: `{project}/02-resources/_extraction_guide.md` |
| 3 | `_metadata.json` | Chunk count and filenames for this paper | Orchestrator: `{paper_folder}/_metadata.json` |
| 4 | All chunk files | Paper content to analyze | Orchestrator: `{paper_folder}/{paper_id}_1.md`, `_2.md`, etc. |

**The orchestrator MUST provide absolute paths for all files in the subagent prompt.**

### DO NOT Read

- `{paper}.pdf` - Already preprocessed into chunks
- `index.md` - You're creating this
- Other papers - Only analyze your assigned paper

### Path Format

All paths provided by orchestrator will be absolute, e.g.:
```
C:\Users\...\02-projects\02-ontologies-research\02-resources\_analysis_kit.md
C:\Users\...\02-projects\02-ontologies-research\02-resources\papers\01-UFO\01-UFO_1.md
```

---

## Methodology (7 Steps)

### Step 0: Initialize Analysis Log (REQUIRED FIRST)

**Create `_analysis_log.md` BEFORE doing any analysis.**

See [references/analysis_log_template.md](references/analysis_log_template.md) for full schema v2.0.

```yaml
---
schema_version: "2.0"
paper_id: "{paper_folder_name}"
paper_title: ""  # Fill after reading metadata
paper_folder: "{absolute_path}"
analyzer: "claude-opus-4"
analysis_started: "{ISO8601_timestamp}"
analysis_completed: ""  # Fill at end
duration_seconds: 0     # Calculate at end

steps:
  step1_read_briefing:
    completed: false
    # ... (all fields from template)
  # ... (all other steps initialized to false)
---
```

**Why first?** The log tracks what you actually read. If you fail mid-analysis, the partial log shows exactly where you stopped.

### Step 1: Read Briefing

Load `_briefing.md` from the collection folder.

Extract:
- **Research question** - What we're trying to answer
- **Research purpose** - WHY this research matters (G22a context)
- **Fields to extract** - Which fields to populate in index.md
- **Focus areas** - What to prioritize
- **Skip sections** - What to ignore (acknowledgments, etc.)

**Update log** after reading:
```yaml
steps.step1_read_briefing:
  completed: true
  briefing_path: "{absolute_path}"
  research_question: "{extracted_RQ}"
  research_purpose: "{from _briefing.md}"  # G22a context
  fields_required: {count}
  fields_to_assess: ["entity_types", "entity_definitions", ...]  # ALL field names
  focus_areas: ["{area1}", "{area2}"]
```

### Step 1b: Field Calibration (REQUIRED - Gap G1)

After reading `_briefing.md`, you MUST understand how to assess each field.

**CALIBRATION: What Counts as TRUE/PARTIAL/FALSE**

For EACH field from `_briefing.md`, use this decision tree when analyzing chunks:

```
Does chunk EXPLICITLY discuss this field?
├─ YES → Does it provide extractable content (definitions, lists, examples)?
│        ├─ YES → fields_found: TRUE
│        └─ NO (just mentions) → fields_found: PARTIAL
└─ NO → fields_found: FALSE
```

**3-State Definition:**

| State | Meaning | Include in Synthesis? | Calibration Rule |
|-------|---------|----------------------|------------------|
| `true` | Field explicitly discussed with extractable content | YES (primary) | Has definitions, lists, examples |
| `partial` | Field mentioned/referenced but not detailed | YES (secondary) | Referenced but no extractable content |
| `false` | Field not present in chunk | NO | No mention at all |

**Examples by Field Type:**

| Field Type | TRUE (extract) | PARTIAL (include, lower priority) | FALSE (skip) |
|------------|----------------|-----------------------------------|--------------|
| `entity_types` | "The framework defines three entity types: Agent, Activity, Entity" | "Various entity types exist in the literature" | No mention of entities |
| `methodology` | "We conducted semi-structured interviews with 15 participants" | "Following standard qualitative methods" | No methodology section |
| `limitations` | "This approach is limited by X, Y, Z" | "Further work is needed" | No limitations mentioned |

**CRITICAL**: Read `_extraction_guide.md` for project-specific calibration examples.

### Step 2: Read Metadata

Load `_metadata.json` from the paper folder.

Extract:
- `title` - Paper title
- `chunks` - Total chunk count
- `total_chars` - For token estimation
- Any other available metadata (authors, year, DOI)

**EDGE CASE**: If `chunks == 0`, STOP immediately:
```yaml
issues: ["Corrupted PDF: 0 chunks found"]
```
Write log and exit - do not proceed with analysis.

**Update log** after reading:
```yaml
paper_title: "{title from metadata}"
steps.step2_read_metadata:
  completed: true
  metadata_path: "{absolute_path}"
  chunks_expected: {count}
  tokens_estimated: {chars / 5 * 1.3}
```

### Step 3: Analyze Chunks (with Forced Field Assessment)

For each chunk `{paper}_N.md` in order:

1. **Read FULL chunk content** (not just headers!)
2. **ASSESS FIELDS** (REQUIRED - 3-STATE - see below)
3. **Record multi-point evidence** (REQUIRED - see Anti-Hallucination section)
4. **Extract fields WITH CHUNK:LINE REFERENCES** (REQUIRED - see Extraction Tracking)
5. **Write chunk summary** - 2-3 sentences capturing key content
6. **Identify load triggers** - Natural language queries that should surface this chunk
7. **Record key quotes with line numbers** - For synthesis validation

**Keep running notes** of all extractions to compile at end.

#### REQUIRED: Forced Field Assessment (3-STATE)

**For EVERY field from `_briefing.md`, you MUST assess EVERY chunk:**

```yaml
chunk_index:
  {N}:
    token_count: {calculate using STANDARD FORMULA: len(content) // 4}
    fields_found:
      entity_types: true      # Has extractable entity types
      entity_definitions: true
      entity_relationships: partial  # Mentioned, not detailed
      ai_integration: false
      # ... EVERY field from _briefing.md must be listed!
```

**Note**: Hash is computed by validation script, not recorded in output.

**CRITICAL RULES:**
- You MUST assess EVERY field for EVERY chunk
- Missing fields = validation failure
- Use calibration from Step 1b to determine state
- Extract items only for fields where `fields_found[field]` in [true, partial]

**Token Count Formula (Gap G3 - STANDARD):**
```python
token_count = len(chunk_content) // 4  # Characters divided by 4
```
Do NOT use other formulas like `chars / 5 * 1.3`. Use `chars // 4` consistently.

#### REQUIRED: Extraction Tracking with Chunk:Line References

**Every extraction MUST include:**
- `chunk`: Which chunk (1, 2, 3...)
- `lines`: Line range in chunk (e.g., "42-47")
- `quote`: Exact text (first 150 chars) proving the extraction
- `confidence`: high/medium/low

**Record in analysis log as you extract:**

```yaml
extractions:
  handover_patterns:
    - name: "Auto-Reply Mechanism"
      chunk: 1
      lines: "127-134"
      quote: "Once an agent receives a message from another agent, it automatically invokes generate_reply..."
      confidence: "high"

  quality_mechanisms:
    - name: "Grounding Agent Pattern"
      chunk: 2
      lines: "89-95"
      quote: "We are able to introduce a grounding agent, which supplies crucial commonsense knowledge..."
      confidence: "high"
```

**Why line numbers?** Enables spot-check validation against source chunks during synthesis.

#### REQUIRED: Evidence Recording

**For EACH chunk**, record evidence that you read the content:

```yaml
chunk_evidence:
  {N}:
    start: "{first ~100 chars after header}"
    end: "{last ~100 chars}"
```

**Example**:
```yaml
chunk_evidence:
  1:
    start: "Thematic analysis is a method for identifying..."
    end: "...widely used across a range of epistemologies."
```

**Note**: Validation script verifies this evidence exists in chunk files.

**Update log** after ALL chunks read:
```yaml
steps.step3_analyze_chunks:
  completed: true
  chunks_total: {N}
  chunks_read: [1, 2, 3, ..., N]
  all_chunks_read: true
  chunk_evidence:
    1: {start: "...", end: "..."}
    2: {start: "...", end: "..."}
    # ... all chunks
```

### Step 4: Compile index.md

Generate `index.md` with:
1. **YAML frontmatter** - All extracted schema fields
2. **Paper overview** - Source, chunks, analysis timestamp
3. **Key extractions** - Summary of most important findings
4. **Chunk navigation** - Summary + load triggers for each chunk

Use template in [index.md Template](#indexmd-template) section.

**Update log** after writing index.md:
```yaml
steps.step4_compile_index:
  completed: true
  index_path: "{absolute_path_to_index.md}"
  yaml_valid: true  # Verify YAML parses correctly
  fields_populated: {count of non-empty fields}
  fields_missing: ["field1", "field2"]  # List any empty required fields
```

### Step 5: Validate

Before finishing, verify:
- [ ] All briefing fields populated (or marked N/A with reason)
- [ ] Every chunk has navigation entry
- [ ] "Load when" triggers are specific and queryable
- [ ] Direct quotes include chunk references (e.g., "Chunk 3")
- [ ] Uncertain extractions flagged with [UNCERTAIN]

**Update log** with validation checklist:
```yaml
steps.step5_validate:
  completed: true
  checklist:
    all_briefing_fields_addressed: true
    all_chunks_have_navigation: true
    load_triggers_are_specific: true
    quotes_have_chunk_refs: true
    uncertainties_flagged: true
```

### Step 6: Complete Analysis Log (REQUIRED LAST)

**Finalize the analysis log with timestamps and metrics:**

```yaml
# Timestamps
analysis_completed: "{ISO8601_timestamp}"
duration_seconds: {end_time - start_time}

# Performance
performance:
  tokens_used: {estimate based on content processed}
  tokens_available: 100000
  time_per_chunk_avg: {duration_seconds / chunks_total}

# Quality assessment
quality:
  relevance_score: {1-5}
  relevance_rationale: "{why this score}"
  domain_match: true/false
  has_llm_content: true/false
  extraction_confidence: "high" | "medium" | "low"

# Output validation
outputs:
  index_md_created: true
  index_md_path: "{absolute_path}"
  index_md_yaml_valid: true
  index_md_word_count: {word count}

# Issues/warnings
issues: []  # Critical problems
warnings: []  # Non-critical notes
```

**Write final `_analysis_log.md`** with all fields populated.

---

## index.md Template

### YAML Frontmatter Schema (v2.3)

```yaml
---
# REQUIRED (always present)
paper_id: ""                 # Paper folder name
title: ""                    # Paper title
authors: []                  # List of authors (if available)
year: null                   # Publication year (if available)
chunks_expected: 0           # From _metadata.json
chunks_read: 0               # Must equal chunks_expected
analysis_complete: true      # Set to true when done
schema_version: "2.3"        # Schema version for validation

# CHUNK-LEVEL FIELD ASSESSMENT (for synthesis routing)
chunk_index:
  1:
    token_count: 12500       # len(content) // 4
    fields_found:            # 3-STATE: true = extractable, partial = mentioned, false = absent
      entity_types: true
      entity_definitions: true
      entity_relationships: partial
      methodology: false
      # ... ALL fields from _briefing.md MUST be listed
  2:
    token_count: 8200
    fields_found:
      entity_types: partial
      entity_definitions: false
      framework_comparison: true
      # ... ALL fields

# DYNAMIC EXTRACTION FIELDS (from _briefing.md)
# Standardized item schema for all fields
entity_types:
  - item: "Endurant (Continuant)"
    chunk: 1
    lines: "128-133"
    quote: "An entity wholly present at any time..."
  - item: "Perdurant (Occurrent)"
    chunk: 1
    lines: "131-133"
    quote: "An entity that can be partially present..."

# Use Structured N/A for missing fields (Gap G18)
methodology:
  - item: "NOT_FOUND"
    chunk: null
    lines: null
    quote: null
    reason: "Paper does not discuss research methodology"
---
```

### Body Structure

```markdown
# {Paper Title} - Analysis Index

## Paper Overview

- **Source**: {pdf filename}
- **Chunks**: {N} chunks, ~{tokens} estimated tokens
- **Analyzed**: {timestamp}

## Key Extractions

[2-3 paragraph summary of most important findings, organized by schema fields]

### {Schema Field 1} (e.g., Handover Patterns)

| Pattern | Source | Quote |
|---------|--------|-------|
| Auto-Reply Mechanism | Chunk 1:127-134 | "Once an agent receives a message..." |
| Unified Interface | Chunk 1:89-95 | "Agents share send/receive functions..." |

### {Schema Field 2} (e.g., Quality Mechanisms)

| Mechanism | Source | Quote |
|-----------|--------|-------|
| Grounding Agent | Chunk 2:89-95 | "We introduce a grounding agent..." |
| Safeguard Validation | Chunk 2:156-163 | "Commander checks code safety..." |

**REQUIRED FORMAT**: Every extraction MUST use `Chunk N:lines` format (e.g., `Chunk 2:89-95`)

### Key Findings (with evidence)

- **Finding 1** (Chunk 2:45-52): "Exact quote from paper proving this finding..."
- **Finding 2** (Chunk 3:112-118): "Another exact quote..."

## Chunk Navigation

### Chunk 1: {Section Title or Description}
- **Summary**: 2-3 sentence description of chunk content
- **Key concepts**: [concept1, concept2, concept3]
- **Key quotes**:
  - Line 45: "Important statement about X..."
  - Line 127: "Definition of key concept Y..."
- **Load when**: "User asks about X" / "Query mentions Y"

### Chunk 2: {Section Title or Description}
- **Summary**: ...
- **Key concepts**: [...]
- **Key quotes**:
  - Line 89: "Quote for validation..."
- **Load when**: "..."

[Continue for ALL chunks]
```

**VALIDATION REQUIREMENT**: Synthesis subagents will spot-check quotes against source chunks. If quote at `Chunk 2:89` doesn't match source file line 89, analysis fails validation.

---

## Structured N/A Format (Gap G18)

When a field has NO content in the paper (all chunks have `fields_found: false`), use this structured format instead of leaving it empty or undefined:

```yaml
methodology:
  - item: "NOT_FOUND"
    chunk: null
    lines: null
    quote: null
    reason: "Paper does not discuss research methodology"
```

**Standard Reasons** (use exactly these phrases):
- `"Paper does not discuss {field_name}"` - Field topic not covered
- `"Field not applicable to this paper type"` - e.g., methodology in a survey paper
- `"Content exists but is insufficient for extraction"` - Mentioned but too vague

**DO NOT:**
- Leave field empty: `methodology: []`
- Omit field entirely
- Use generic "N/A" without reason

**Why structured N/A?** Enables validation scripts to distinguish between:
1. "Analyzed but not found" (structured N/A)
2. "Forgot to analyze" (missing field = validation error)

---

## File Reading Rules

**See "MUST READ FILES" section at top of this document.**

The orchestrator provides all paths. Read in order:
1. `_analysis_kit.md` → Research question + extraction schema
2. `_extraction_guide.md` → Field examples + controlled vocabulary
3. `_metadata.json` → Paper structure + chunk list
4. All chunks in order → Maintain context flow

---

## Large Paper Handling

### When to Split

If you're told this is a **partial analysis** (part N of M), you're analyzing a subset of chunks.

**Produce `index_part{N}.md` instead of `index.md`** with:

```yaml
---
# PARTIAL INDEX HEADER
partial: true
part: 1                      # Which part (1, 2, 3...)
total_parts: 2               # Total parts
chunks_covered: [1, 2, 3, 4, 5]  # Which chunks this part analyzes

# Standard fields (partial data)
title: "Paper Title"
topics: ["topic from this part"]
methods: ["method from this part"]
# ... other schema fields
---

# {Paper Title} - Partial Index (Part 1 of 2)

## Chunks Covered: 1-5

[Standard chunk navigation for chunks 1-5 only]
```

### Merge Instructions

A separate merge subagent will:
1. Read all `index_part*.md` files
2. Combine arrays (deduplicate topics, methods, etc.)
3. Merge chunk navigation sections sequentially
4. Produce final unified `index.md`

---

## Quality Criteria

### Extraction Quality

| Criterion | Check |
|-----------|-------|
| **Completeness** | All briefing fields populated or marked N/A |
| **Specificity** | Topics/methods are specific, not generic |
| **Traceability** | Findings cite chunk numbers |
| **Accuracy** | Extractions match paper content |

### Navigation Quality

| Criterion | Check |
|-----------|-------|
| **Coverage** | Every chunk has an entry |
| **Summaries** | 2-3 sentences, capture key content |
| **Load triggers** | Specific queries, not vague |
| **Key concepts** | 3-5 concepts per chunk |

### Uncertainty Handling

- Flag uncertain extractions: `[UNCERTAIN: reason]`
- Mark missing data: `N/A - not mentioned in paper`
- Note ambiguities: `[AMBIGUOUS: could mean X or Y]`

---

## Examples

See [references/examples/](references/examples/) for:
- `example_index.md` - Complete index.md output
- `example_briefing.md` - Example _briefing.md input

---

## Token Budget

You have ~100k token context. Budget:

**STANDARD TOKEN FORMULA** (use consistently EVERYWHERE - Gap G3):
```python
def estimate_tokens(text: str) -> int:
    """Standard token estimation for all pipeline components.

    Source: 00-system/core/nexus/config.py:15
    DO NOT use other formulas like chars/5*1.3
    """
    return len(text) // 4
```

| Component | Tokens | Notes |
|-----------|--------|-------|
| This methodology | ~3,000 | Fixed |
| _briefing.md | ~2,000 | Variable (+30-50 for research_purpose) |
| _analysis_kit.md | ~500 | Variable (+50-100 for synthesis_goals) |
| _metadata.json | ~500 | Small |
| Analysis log overhead | ~3,500 | Schema v2.3 (with chunk_index + fields_found) |
| Paper chunks | ~74,000 | **Main content** |
| Output generation | ~17,000 | index.md + log |

**Revised usable budget**: `74,000 - (39 × chunk_count) - (150 × extraction_count)` tokens.

The extraction tracking adds ~150 tokens per extraction (quote + metadata). For typical papers with 10 extractions, this is ~1,500 tokens.

If paper exceeds budget, you'll be given a subset of chunks (partial analysis).

## Detail Balance for Synthesis

**Goal**: Maximize useful detail while staying under synthesis context budget.

**Synthesis reads**: YAML frontmatter from index.md (~40 papers × ~500 tokens = 20k tokens)

**Rule of Thumb**: Each index.md frontmatter should be 400-600 tokens max.

### What to Include (HIGH VALUE for synthesis)

| Element | Example | Tokens |
|---------|---------|--------|
| Extraction name | "Auto-Reply Mechanism" | ~3 |
| Chunk:line ref | "Chunk 2:89-95" | ~2 |
| Short quote | "agents automatically invoke..." (50-80 chars) | ~15 |
| Confidence | "high" | ~1 |

### What to Exclude (LOW VALUE for synthesis)

| Element | Why Exclude |
|---------|-------------|
| Full 150-char quotes | Keep in analysis_log, not frontmatter |
| Detailed rationales | Put in body, not frontmatter |
| Metadata paths | Not needed for synthesis |
| Hash values | For validation only |

### Frontmatter Size Target

```yaml
# GOOD: ~500 tokens (fits 40+ papers in synthesis context)
handover_patterns:
  - name: "Auto-Reply Mechanism"
    chunk_ref: "1:127-134"
    quote: "agents automatically invoke generate_reply..." # 50 chars
  - name: "Unified Interface"
    chunk_ref: "1:89-95"
    quote: "shared send/receive functions..." # 40 chars

# BAD: ~1500 tokens (only fits 13 papers)
handover_patterns:
  - name: "Auto-Reply Mechanism"
    description: "Long description of how the mechanism works in detail..."
    chunk: 1
    lines: "127-134"
    quote: "Very long quote that captures the full context of the mechanism as described in the paper including all surrounding sentences that provide additional context..."
    confidence: "high"
    rationale: "This is a core pattern because..."
```

**Bottom line**: Short quotes in frontmatter, full quotes in analysis_log.

---

## Output Files

Each paper analysis produces TWO files:

1. **`_analysis_log.md`** - Structured validation log (Schema v2.2)
   - Created FIRST (Step 0)
   - Completed LAST (Step 6)
   - Contains FULL extraction details (150-char quotes, chunk:line refs)
   - Used by validation script to verify analysis quality
   - **Detail level**: HIGH (full traceability)

2. **`index.md`** - Analysis output
   - Created in Step 4
   - Contains YAML frontmatter + chunk navigation
   - **Frontmatter**: SHORT quotes (50-80 chars), chunk:line refs
   - **Body**: Summaries, key concepts, load triggers
   - Used by paper-query and paper-synthesize skills
   - **Detail level**: MEDIUM (synthesis-optimized)

### Two-Tier Detail Strategy

| File | Purpose | Quote Length | Full Evidence |
|------|---------|--------------|---------------|
| `_analysis_log.md` | Validation | 150 chars | Yes (extractions field) |
| `index.md` frontmatter | Synthesis | 50-80 chars | No (references log) |
| `index.md` body | Navigation | N/A | Key concepts only |

This enables:
- **Validation**: Full traceability via analysis_log
- **Synthesis**: Compact frontmatter for 40+ papers
- **Progressive disclosure**: Load full details from log when needed

---

**Version**: 2.3 (2025-12-28)
**Changes**:
- v2.0: Initial methodology with 5 steps
- v2.1: Added 3-point anti-hallucination sampling
- v2.2: Added chunk:line extraction tracking, two-tier detail strategy, synthesis-optimized frontmatter
- v2.3: Added Step 1b Field Calibration (G1), 3-state fields_found in chunk_index, Structured N/A format (G18), Token formula standardization to chars//4 (G3), research_purpose context (G22a)
