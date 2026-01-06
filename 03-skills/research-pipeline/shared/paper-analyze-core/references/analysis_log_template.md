# Analysis Log Template (Schema v2.3)

**Purpose**: Structured validation log for paper analysis subagents. Enables programmatic validation of analysis quality, anti-hallucination checks, and extraction traceability.

**Usage**: Subagents MUST create `_analysis_log.md` as their FIRST output file, before writing `index.md`.

---

## YAML Frontmatter Schema v2.3

```yaml
---
schema_version: "2.3"

# ============================================
# METADATA
# ============================================
paper_id: ""                      # Paper folder name (e.g., "Braun_Clarke_2006")
paper_title: ""                   # Full paper title from metadata
paper_folder: ""                  # Absolute path to paper folder
analyzer: "claude-opus-4"         # Model used for analysis
analysis_started: ""              # ISO8601 timestamp (e.g., 2025-12-18T14:30:00)
analysis_completed: ""            # ISO8601 timestamp
duration_seconds: 0               # Elapsed time in seconds

# ============================================
# STEP COMPLETION (all must be true for valid analysis)
# ============================================
steps:
  step1_read_briefing:
    completed: false
    briefing_path: ""             # Absolute path to _briefing.md
    research_question: ""         # Extracted RQ from briefing
    fields_required: 0            # Count of schema fields to populate
    focus_areas: []               # List of focus areas from briefing

  step2_read_metadata:
    completed: false
    metadata_path: ""             # Absolute path to _metadata.json
    chunks_expected: 0            # Total chunks from metadata
    tokens_estimated: 0           # Estimated tokens (chars // 4) - Standard formula

  step3_analyze_chunks:
    completed: false
    chunks_total: 0               # Total chunks in paper
    chunks_read: []               # List of chunk numbers read (e.g., [1, 2, 3])
    all_chunks_read: false        # AUTO-VALIDATE: len(chunks_read) == chunks_total
    # ------------------------------------------
    # ANTI-HALLUCINATION: 2-point evidence (start + end sampling)
    # ------------------------------------------
    # For each chunk, record:
    # - start: First ~100 chars AFTER the header line (skip "# Chunk N" etc.)
    # - end: Last ~100 chars of the chunk
    chunk_evidence: {}
    # Example:
    # chunk_evidence:
    #   1:
    #     start: "Thematic analysis is a method for identifying..."
    #     end: "...patterns within qualitative data (Braun & Clarke, 2006)."
    #   2:
    #     start: "The six phases of thematic analysis..."
    #     end: "...reflexive approach to coding."

  step4_compile_index:
    completed: false
    index_path: ""                # Absolute path to index.md
    yaml_valid: false             # YAML frontmatter parses correctly
    fields_populated: 0           # Count of non-empty schema fields
    fields_missing: []            # List of empty required fields

  step5_validate:
    completed: false
    checklist:
      all_briefing_fields_addressed: false
      all_chunks_have_navigation: false
      load_triggers_are_specific: false
      quotes_have_chunk_refs: false
      uncertainties_flagged: false

# ============================================
# ERROR RECOVERY
# ============================================
error_handling:
  retries: 0                      # Number of retry attempts
  timeout_occurred: false         # Did analysis hit timeout?
  partial_success: false          # Did we complete some but not all?
  recovery_notes: ""              # Details of any errors/recovery

# ============================================
# PERFORMANCE METRICS
# ============================================
performance:
  tokens_used: 0                  # Actual tokens consumed
  tokens_available: 100000        # Context budget (100k)
  time_per_chunk_avg: 0           # Average seconds per chunk

# ============================================
# QUALITY METRICS
# ============================================
quality:
  relevance_score: 0              # 1-5 scale (5 = highly relevant)
  relevance_rationale: ""         # Why this score?
  domain_match: false             # Paper matches research domain?
  has_llm_content: false          # Paper discusses LLMs/AI?
  extraction_confidence: ""       # "high" | "medium" | "low"

# ============================================
# OUTPUT VALIDATION
# ============================================
outputs:
  index_md_created: false
  index_md_path: ""               # Absolute path to index.md
  index_md_yaml_valid: false      # YAML frontmatter is valid
  index_md_word_count: 0          # Word count of index.md

# ============================================
# EXTRACTION TRACKING (NEW - v2.2)
# ============================================
# Every schema field extraction MUST be tracked with:
# - chunk: Source chunk number
# - lines: Line range in chunk (e.g., "42-47")
# - quote: Exact text (first 150 chars) proving extraction
# - confidence: high/medium/low
extractions: {}
# Example:
# extractions:
#   handover_patterns:
#     - name: "Auto-Reply Mechanism"
#       chunk: 1
#       lines: "127-134"
#       quote: "Once an agent receives a message from another agent, it automatically invokes generate_reply..."
#       confidence: "high"
#     - name: "Unified Interface"
#       chunk: 1
#       lines: "89-95"
#       quote: "Agents share send/receive functions for message passing..."
#       confidence: "high"
#   quality_mechanisms:
#     - name: "Grounding Agent"
#       chunk: 2
#       lines: "89-95"
#       quote: "We introduce a grounding agent, which supplies crucial commonsense knowledge..."
#       confidence: "high"
#   prompt_templates:
#     - name: "Default System Message"
#       chunk: 2
#       lines: "156-180"
#       quote: "Figure 5 shows the default system message for the built-in assistant agent..."
#       confidence: "high"

# ============================================
# ISSUES & WARNINGS
# ============================================
issues: []                        # Critical problems that may invalidate analysis
warnings: []                      # Non-critical notes for review
---
```

---

## Validation Rules

### Rule 1: All Steps Completed
Every `steps.*.completed` must be `true`.

```python
for step in steps.values():
    assert step['completed'] == True, f"Step incomplete: {step}"
```

### Rule 2: All Chunks Read
`chunks_read` must equal `range(1, chunks_total + 1)`.

```python
expected = list(range(1, chunks_total + 1))
assert chunks_read == expected, f"Missing chunks: {set(expected) - set(chunks_read)}"
```

### Rule 3: Evidence Integrity (Anti-Hallucination) - 2-Point Sampling

For each chunk N:
- `chunk_evidence[N].start` must match first ~100 chars of chunk (after header)
- `chunk_evidence[N].end` must match last ~100 chars of chunk

```python
for chunk_num, evidence in chunk_evidence.items():
    chunk_content = read_file(f"{paper}__{chunk_num}.md")

    # Skip header line (e.g., "# Chunk 1: Introduction")
    content_after_header = chunk_content.split('\n', 1)[1] if '\n' in chunk_content else chunk_content

    # Validate start
    assert content_after_header[:100].strip() == evidence['start'].strip(), \
        f"Chunk {chunk_num}: start mismatch"

    # Validate end
    assert chunk_content[-100:].strip() == evidence['end'].strip(), \
        f"Chunk {chunk_num}: end mismatch"
```

### Rule 4: Index Created
`outputs.index_md_created` must be `true`.

### Rule 5: YAML Valid
`outputs.index_md_yaml_valid` must be `true`.

### Rule 6: Edge Cases

```python
# Reject corrupted PDFs (0 chunks)
assert chunks_total > 0, "Corrupted PDF: 0 chunks"

# Reject old schema
assert schema_version == "2.3", f"Schema upgrade required: {schema_version} -> 2.3"

# Reject if no evidence provided
assert len(chunk_evidence) > 0, "No chunk evidence provided"
```

### Rule 7: Extraction Traceability (NEW - v2.2)

Every extraction in `extractions` must have valid chunk:line references that can be verified:

```python
for field_name, items in extractions.items():
    for item in items:
        # Must have chunk reference
        assert 'chunk' in item, f"Extraction {item['name']} missing chunk reference"
        assert item['chunk'] in chunks_read, f"Extraction references unread chunk {item['chunk']}"

        # Must have line range
        assert 'lines' in item, f"Extraction {item['name']} missing line reference"
        assert re.match(r'^\d+-\d+$', item['lines']), f"Invalid line format: {item['lines']}"

        # Must have quote
        assert 'quote' in item and len(item['quote']) >= 50, \
            f"Extraction {item['name']} missing or too short quote"

        # Must have confidence
        assert item.get('confidence') in ['high', 'medium', 'low'], \
            f"Invalid confidence: {item.get('confidence')}"
```

### Rule 8: Quote Verification (NEW - v2.2)

Quotes in extractions must match source chunks at specified lines:

```python
def verify_extraction_quote(paper_folder, extraction):
    chunk_file = f"{paper_folder}/{paper_id}_{extraction['chunk']}.md"
    chunk_content = read_file(chunk_file)
    lines = chunk_content.split('\n')

    # Parse line range (e.g., "127-134")
    start_line, end_line = map(int, extraction['lines'].split('-'))

    # Extract text from specified lines
    source_text = '\n'.join(lines[start_line-1:end_line])

    # Quote must appear in source text (first 150 chars of quote)
    quote_start = extraction['quote'][:150].strip()
    assert quote_start in source_text, \
        f"Quote not found at Chunk {extraction['chunk']}:{extraction['lines']}"
```

---

## Example: Completed Analysis Log

```yaml
---
schema_version: "2.3"

paper_id: "Braun_Clarke_2006"
paper_title: "Using thematic analysis in psychology"
paper_folder: "C:/Users/dsber/thematic-analysis-v2/04-workspace/papers/TA_LLM/Braun_Clarke_2006"
analyzer: "claude-opus-4"
analysis_started: "2025-12-18T14:30:00"
analysis_completed: "2025-12-18T14:32:45"
duration_seconds: 165

steps:
  step1_read_briefing:
    completed: true
    briefing_path: "C:/Users/dsber/thematic-analysis-v2/04-workspace/papers/TA_LLM/_briefing.md"
    research_question: "How can LLMs be effectively integrated into thematic analysis workflows?"
    fields_required: 8
    focus_areas:
      - "TA methodology phases"
      - "Coding techniques"
      - "Quality criteria"
      - "LLM integration approaches"

  step2_read_metadata:
    completed: true
    metadata_path: "C:/Users/dsber/thematic-analysis-v2/04-workspace/papers/TA_LLM/Braun_Clarke_2006/_metadata.json"
    chunks_expected: 3
    tokens_estimated: 12000  # Using chars // 4 formula

  step3_analyze_chunks:
    completed: true
    chunks_total: 3
    chunks_read: [1, 2, 3]
    all_chunks_read: true
    chunk_evidence:
      1:
        start: "Thematic analysis is a method for identifying, analysing and reporting"
        end: "widely used across a range of epistemologies and research questions."
      2:
        start: "The process of thematic analysis involves six phases: familiarisation"
        end: "flexibility in terms of theoretical framework and research question."
      3:
        start: "Quality in thematic analysis can be assessed through several criteria"
        end: "ensuring rigorous and trustworthy qualitative research outcomes."

  step4_compile_index:
    completed: true
    index_path: "C:/Users/dsber/thematic-analysis-v2/04-workspace/papers/TA_LLM/Braun_Clarke_2006/index.md"
    yaml_valid: true
    fields_populated: 8
    fields_missing: []

  step5_validate:
    completed: true
    checklist:
      all_briefing_fields_addressed: true
      all_chunks_have_navigation: true
      load_triggers_are_specific: true
      quotes_have_chunk_refs: true
      uncertainties_flagged: true

error_handling:
  retries: 0
  timeout_occurred: false
  partial_success: false
  recovery_notes: ""

performance:
  tokens_used: 18500
  tokens_available: 100000
  time_per_chunk_avg: 45

quality:
  relevance_score: 5
  relevance_rationale: "Foundational paper defining TA methodology, highly relevant to research question"
  domain_match: true
  has_llm_content: false
  extraction_confidence: "high"

outputs:
  index_md_created: true
  index_md_path: "C:/Users/dsber/thematic-analysis-v2/04-workspace/papers/TA_LLM/Braun_Clarke_2006/index.md"
  index_md_yaml_valid: true
  index_md_word_count: 1250

# ============================================
# EXTRACTION TRACKING (NEW - v2.2)
# ============================================
extractions:
  ta_methodology:
    - name: "Six-Phase Framework"
      chunk: 1
      lines: "45-67"
      quote: "The process of thematic analysis involves six phases: familiarisation with data, generating initial codes, searching for themes, reviewing themes, defining and naming themes, and producing the report."
      confidence: "high"
    - name: "Recursive Nature"
      chunk: 1
      lines: "89-95"
      quote: "Analysis is not a linear process of simply moving from one phase to the next. Instead, it is a more recursive process, where movement is back and forth as needed..."
      confidence: "high"
  coding_techniques:
    - name: "Data-Driven vs Theory-Driven"
      chunk: 2
      lines: "34-48"
      quote: "Themes can be identified in one of two primary ways: an inductive or 'bottom up' way, or a theoretical or deductive or 'top down' way..."
      confidence: "high"
    - name: "Semantic vs Latent Codes"
      chunk: 2
      lines: "112-128"
      quote: "Thematic analysis can focus on the semantic or surface meanings of the data, or go beyond this to identify latent or underlying ideas, assumptions, and conceptualisations..."
      confidence: "high"
  quality_criteria:
    - name: "15-Point Checklist"
      chunk: 3
      lines: "156-195"
      quote: "We provide a 15-point checklist of criteria for good thematic analysis covering transcription, coding, analysis, overall, and written report quality..."
      confidence: "high"

issues: []
warnings:
  - "Paper predates LLMs (2006); LLM-specific content not expected"
---

# Analysis Log: Braun_Clarke_2006

Analysis completed successfully with full extraction traceability.

## Summary

| Metric | Value |
|--------|-------|
| Duration | 2m 45s |
| Chunks Read | 3/3 |
| Confidence | High |
| Extractions | 5 items across 3 schema fields |
| Issues | None |

## Extraction Summary

| Field | Count | Chunks | Key Findings |
|-------|-------|--------|--------------|
| ta_methodology | 2 | 1 | Six-phase framework, recursive analysis |
| coding_techniques | 2 | 2 | Inductive/deductive, semantic/latent |
| quality_criteria | 1 | 3 | 15-point checklist for TA quality |

## Evidence Trail

### Chunk Evidence (2-Point Sampling)
All chunk evidence validated. Start+end sampling confirms content was read.

### Extraction Evidence (Chunk:Line References)
All 5 extractions have verified chunk:line references:
- Chunk 1:45-67 ✓ Six-Phase Framework
- Chunk 1:89-95 ✓ Recursive Nature
- Chunk 2:34-48 ✓ Data-Driven vs Theory-Driven
- Chunk 2:112-128 ✓ Semantic vs Latent Codes
- Chunk 3:156-195 ✓ 15-Point Checklist

## Key Quotes for Synthesis

1. **Definition of TA** (Chunk 1:12-18): "Thematic analysis is a method for identifying, analysing and reporting patterns (themes) within data."

2. **Six Phases** (Chunk 1:45-52): "1. Familiarising yourself with your data, 2. Generating initial codes, 3. Searching for themes, 4. Reviewing themes, 5. Defining and naming themes, 6. Producing the report."

3. **Quality Standard** (Chunk 3:180-185): "Good thematic analysis requires: adequate time, checking coded data extracts, multiple coding passes, and themes that capture something important in relation to the research question."

## Notes

This is a foundational methodology paper. No LLM-specific content present (published 2006), but provides essential TA framework context for the research question. The 15-point checklist in Chunk 3 is particularly valuable for evaluating LLM-assisted TA implementations.
```

---

## Why 2-Point Evidence?

### Rationale

2-point sampling (start + end) provides sufficient validation:
- **Start**: Confirms subagent read beginning of chunk (after header)
- **End**: Confirms subagent read to end of chunk

This is combined with **extraction tracking** (chunk:line references) which provides the real anti-hallucination guarantee - every claim must cite its source location.

### Why NOT 3-Point or Hash?

| Approach | Problem |
|----------|---------|
| Mid-point sampling | Adds complexity, minimal benefit over extraction tracking |
| SHA256 hash | Doesn't prove understanding, just byte-level match. Also prone to typos/encoding issues |

### Detection Strategy

| Attack | Detection Method |
|--------|------------------|
| Only read header | Start evidence won't match (header is skipped) |
| Didn't read to end | End evidence won't match |
| Fabricated extractions | Quote-line verification in synthesis catches this |
| Made up claims | Extraction tracking requires chunk:line citations |

**Bottom line**: 2-point evidence + extraction tracking provides practical validation without unnecessary complexity.

---

## Integration with paper-analyze-core

### Step 0 (NEW): Create Analysis Log

**BEFORE** following the 5-step methodology, subagents must:

1. Create `_analysis_log.md` with schema v2.0 header
2. Set `analysis_started` timestamp
3. Initialize all `steps.*.completed` to `false`

### During Step 3: Record 2-Point Evidence

While reading each chunk:

```python
# After reading chunk N content
content_after_header = content.split('\n', 1)[1] if '\n' in content else content

chunk_evidence[N] = {
    "start": content_after_header[:100].strip(),
    "end": content[-100:].strip()
}
chunks_read.append(N)
```

### Step 6 (NEW): Complete Analysis Log

**AFTER** validation (Step 5):

1. Set `analysis_completed` timestamp
2. Calculate `duration_seconds`
3. Set all `steps.*.completed` to `true`
4. Set `outputs.*` fields
5. Write final `_analysis_log.md`

---

## Token Budget Impact

| Component | Tokens | Notes |
|-----------|--------|-------|
| Analysis log overhead | ~2,000 | Fixed per paper |
| 2-point evidence | ~26 × chunks | Start + end strings |

**Revised usable budget**: `75,000 - (26 × chunk_count)`

For typical paper (10 chunks): 74,740 tokens usable (99.7% of original).

---

**Version**: 2.3 (schema alignment)
**Created**: 2025-12-18
**Updated**: 2025-12-29
**Changes**:
- v2.0: Initial structured validation log
- v2.1: Added multi-point sampling anti-hallucination
- v2.2: Added extraction tracking with chunk:line references, key quotes for synthesis
- v2.3: Simplified to 2-point evidence (start+end), removed hash, standardized token formula to chars//4
**Author**: Project 07 - Research Pipeline 10x Improvement
