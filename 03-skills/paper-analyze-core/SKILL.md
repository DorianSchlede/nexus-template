---
name: paper-analyze-core
description: "SHARED METHODOLOGY for paper analysis subagents. DO NOT LOAD DIRECTLY. This skill is loaded by the paper-analyze orchestrator and provides the analysis methodology, index.md template, file reading rules, and quality criteria for all paper analysis subagents."
---

# Paper Analyze Core

**⚠️ DO NOT LOAD DIRECTLY** - This skill is loaded by `paper-analyze` orchestrator into subagents.

Shared methodology foundation for consistent paper analysis across all subagents.

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
- **Fields to extract** - Which fields to populate in index.md
- **Focus areas** - What to prioritize
- **Skip sections** - What to ignore (acknowledgments, etc.)

**Update log** after reading:
```yaml
steps.step1_read_briefing:
  completed: true
  briefing_path: "{absolute_path}"
  research_question: "{extracted_RQ}"
  fields_required: {count}
  focus_areas: ["{area1}", "{area2}"]
```

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

### Step 3: Analyze Chunks (with Anti-Hallucination Evidence)

For each chunk `{paper}_N.md` in order:

1. **Read FULL chunk content** (not just headers!)
2. **Record multi-point evidence** (REQUIRED - see below)
3. **Extract fields WITH CHUNK:LINE REFERENCES** (REQUIRED - see Extraction Tracking)
4. **Write chunk summary** - 2-3 sentences capturing key content
5. **Identify load triggers** - Natural language queries that should surface this chunk
6. **Record key quotes with line numbers** - For synthesis validation

**Keep running notes** of all extractions to compile at end.

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

#### REQUIRED: 3-Point Evidence Recording

**After reading EACH chunk**, record evidence proving you read the full content:

```yaml
chunk_evidence:
  {N}:
    start: "{first 100 chars AFTER header line}"
    mid: "{100 chars from 50% position}"
    end: "{last 100 chars of chunk}"
    hash: "{SHA256 of full chunk content}"
```

**Example for Chunk 1**:

If chunk content is:
```markdown
# Chunk 1: Introduction

Thematic analysis is a method for identifying, analysing and reporting patterns...
[... 5000 chars of content ...]
...semantic content or latent level which examines underlying ideas...
[... 5000 chars of content ...]
...widely used across a range of epistemologies and research questions.
```

Record:
```yaml
chunk_evidence:
  1:
    start: "Thematic analysis is a method for identifying, analysing and reporting"
    mid: "semantic content or latent level which examines underlying ideas"
    end: "widely used across a range of epistemologies and research questions."
    hash: "a7b8c9d0e1f2..."
```

**Note**: Skip the header line (`# Chunk 1: ...`) when recording `start`. Mid is 100 chars centered at 50% position.

**Update log** after ALL chunks read:
```yaml
steps.step3_analyze_chunks:
  completed: true
  chunks_total: {N}
  chunks_read: [1, 2, 3, ..., N]
  all_chunks_read: true
  chunk_evidence:
    1: {start: "...", mid: "...", end: "...", hash: "..."}
    2: {start: "...", mid: "...", end: "...", hash: "..."}
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

### YAML Frontmatter Schema

```yaml
---
# REQUIRED (always present)
title: ""                    # Paper title
authors: []                  # List of authors (if available)
year: null                   # Publication year (if available)
chunks: 0                    # Total chunks in paper
tokens_estimated: 0          # Estimated token count (words × 1.3)
analyzed_at: ""              # ISO timestamp (YYYY-MM-DDTHH:MM:SS)

# DYNAMIC (from _briefing.md)
# Populate fields listed in briefing
topics: []
methods: []
key_findings: []
limitations: []
relevance_triggers: []
# ... additional custom fields from briefing
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

## File Reading Rules

### MUST READ (in order)

1. `_briefing.md` - FIRST, contains analysis schema
2. `_metadata.json` - Paper info, chunk count
3. `{paper}_1.md`, `{paper}_2.md`, ... - All chunks in sequence

### NEVER READ

- `{paper}.pdf` - Already preprocessed into chunks!
- `index.md` - You're creating this!
- `index_part*.md` - Partial outputs from split papers

### ORDER MATTERS

1. **_briefing.md** → Understand what to extract
2. **_metadata.json** → Understand paper structure
3. **Chunks in order** → Maintain context flow across paper

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

| Component | Tokens | Notes |
|-----------|--------|-------|
| This methodology | ~3,000 | Fixed |
| _briefing.md | ~2,000 | Variable |
| _metadata.json | ~500 | Small |
| Analysis log overhead | ~3,500 | Schema v2.2 (with extractions) |
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

**Version**: 2.2 (2025-12-19)
**Changes**:
- v2.0: Initial methodology with 5 steps
- v2.1: Added 3-point anti-hallucination sampling
- v2.2: Added chunk:line extraction tracking, two-tier detail strategy, synthesis-optimized frontmatter
