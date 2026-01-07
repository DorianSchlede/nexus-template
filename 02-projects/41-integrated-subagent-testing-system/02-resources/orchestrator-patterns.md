# Orchestrator Patterns - Research Pipeline Analysis

**Source**: Subagent analysis of `03-skills/research-pipeline/orchestrators/`
**Agent ID**: a841a72
**Date**: 2026-01-07

---

## 1. Three-Phase Chain Architecture

```
Phase 1: PLANNING & ACQUISITION        Phase 2: ANALYSIS              Phase 3: SYNTHESIS
(create-research-project)              (analyze-research-project)     (synthesize-research-project)
        ↓                                      ↓                            ↓
- Define research question           - Spawn subagents for papers    - Cross-paper aggregation
- Extract schema/fields              - Generate index.md per paper   - Field-level synthesis
- Search & download papers           - Validate analysis logs        - Full markdown report
- Preprocess to chunks               - Record chunk evidence         - Citations + sources
- Gate: READY_FOR_EXECUTION          - Gate: READY_FOR_SYNTHESIS     - Gate: COMPLETE
```

**Key Innovation**: Pre-calculated subagent allocation at end of Phase 1, preventing recalculation in Phase 2.

---

## 2. Task Splitting Patterns

### 2.1 Pre-Calculated Allocation (Phase 1 → Phase 2)

**Pattern**: Token-based bin-packing calculated BEFORE analysis begins.

```python
def get_subagent_count(chunks: int) -> int:
    """Allocation rules based on chunk count"""
    if chunks <= 12:
        return 1  # Small papers: 1 subagent
    else:
        return 2  # Large papers: 2+ subagents (split)
```

**Key Principle**: Allocation is calculated in Phase 1, written to `plan.md`, and READ (not recalculated) in Phase 2.

```yaml
# Written to plan.md during Phase 1, Step 12
## Subagent Allocation Plan

| Paper ID | Chunks | Est. Tokens | Subagents | Splits |
|----------|--------|-------------|-----------|--------|
| Small_Paper | 3 | ~35,000 | 1 | 1-3 |
| Large_Paper | 10 | ~120,000 | 2 | 1-6, 7-10 |
| Survey_Paper | 16 | ~190,000 | 3 | 1-6, 7-12, 13-16 |
```

### 2.2 Chunk Range Splitting (Multi-Subagent Papers)

**Pattern**: For papers exceeding 12 chunks, split into 5-6 chunk segments.

```python
subagents = 1
if chunks <= 6:
    splits = [f"1-{chunks}"]
elif chunks <= 12:
    subagents = 1
    splits = ["1-6", f"7-{chunks}"]
else:
    subagents = ceil(chunks / 6)
    splits = [f"{i*6+1}-{min((i+1)*6, chunks)}" for i in range(subagents)]
```

**Example**: 16-chunk paper → 3 subagents:
- Subagent 1: Chunks 1-6 → `index_part1.md`
- Subagent 2: Chunks 7-12 → `index_part2.md`
- Subagent 3: Chunks 13-16 → `index_part3.md`

---

## 3. Subagent Communication Patterns

### 3.1 INPUT CONTRACT (Strict File Access)

```markdown
## INPUT CONTRACT (STRICT)

### Files You MUST Read (in this order)
1. `03-skills/research-pipeline/shared/paper-analyze-core/SKILL.md`
2. `{project_path}/02-resources/_briefing.md`
3. `{project_path}/02-resources/_analysis_kit.md`
4. `{project_path}/02-resources/_extraction_guide.md`
5. `{paper_path}/_metadata.json`
6. `{paper_path}/{paper_id}_1.md`
[... exact chunk list from _metadata.json]

### Files You MUST NOT Read
- ANY `.pdf` file
- ANY folder except `{paper_path}/`
- ANY other paper folder in `02-resources/papers/`
```

**Validation**: INPUT CONTRACT violations cause analysis to fail validation.

### 3.2 OUTPUT CONTRACT (Structured Format)

```yaml
---
paper_id: "{paper_id}"
title: "{extracted title}"
chunks_expected: {from _metadata.json}
chunks_read: {must equal chunks_expected}
analysis_complete: true
schema_version: "2.3"

chunk_index:
  1:
    token_count: {len(chunk_content) // 4}
    fields_found:
      {field_1}: true|partial|false
      {field_2}: true|partial|false
  2:
    token_count: ...
    fields_found: ...
```

---

## 4. Merge/Synthesis Patterns

### 4.1 Paper-Level Merge (Multi-Part Analysis)

**Pattern**: Spawn specialized merge subagent to combine split analyses.

```python
if paper['Subagents'] > 1:
    # First: Spawn analysis subagents for each split
    for split in paper['Splits']:
        Task(subagent_type="general-purpose",
             prompt=f"Analyze chunks {split} → index_part{N}.md")

    # Wait for all to complete
    wait_for_all()

    # Then: Spawn merge subagent
    Task(subagent_type="general-purpose",
         prompt=f"Merge index_part1.md + index_part2.md → index.md")
```

### 4.2 Field-Level Extraction (Synthesis Level 4)

**Pattern**: Batch extraction subagents work on specific fields.

```python
# For each field from _briefing.md:
chunks_for_field = _synthesis_routing[field]

# Allocate to batches (70k tokens each)
batches = greedy_bin_pack(chunks_for_field, max_tokens=70000)

# Spawn extraction subagents in parallel (max 15)
for batch in batches:
    Task(subagent_type="general-purpose",
         prompt=f"Extract {field} patterns from chunks in batch")
```

### 4.3 Cross-Field Aggregation (Synthesis Level 6)

**Pattern**: Deterministic script merges batch outputs.

```python
def aggregate_patterns(batch_files: List[Path]) -> dict:
    """Merge patterns across batches for a field."""
    all_patterns = []

    for batch_file in batch_files:
        batch_data = read_yaml(batch_file)
        all_patterns.extend(batch_data['patterns'])

    # Deduplicate by fuzzy match (90% similarity)
    merged = fuzzy_merge(all_patterns, threshold=0.9)
    return merged
```

---

## 5. Progress Tracking & Recovery

### 5.1 Resume Checkpoints

**Pattern**: Update `_resume.md` at strategic points.

```yaml
---
updated: "{timestamp}"
phase: "analysis|validation|complete"
project_id: "{project_id}"
---

## Current State
- Phase: {current phase}
- Papers analyzed: {N}/{total}
- Last completed batch: {batch_number}

## Pending Work
- Papers remaining: [list]
- Next batch: {batch_number}
```

**Update Rules**:
1. After every ~60% context usage
2. After completing each batch
3. After each validation step

### 5.2 Progress Files

```
project_path/
├── 01-planning/
│   ├── steps.md           # Checkbox progress
│   └── plan.md            # Orchestrator instructions
├── 02-resources/
│   ├── _synthesis_routing.yaml  # (Level 1)
│   └── _subagent_plan.yaml      # (Level 2)
├── 03-working/
│   ├── prompts/_prompt_*.md     # Generated prompts (Level 3)
│   ├── _batch_*.yaml            # Batch outputs (Level 4)
│   └── _verification_report.yaml # Quote verification (Level 5)
└── 04-outputs/
    ├── _synthesis_*.yaml         # Aggregated patterns (Level 6)
    └── _synthesis_report.md      # Final report (Level 7)
```

---

## 6. Error Handling & Retry

### 6.1 Timeout Partial Save Protocol

```yaml
error_handling:
  timeout_occurred: true
  partial_success: true
  chunks_completed: [1, 2, 3]
  chunks_remaining: [4, 5]
  recovery_notes: "Resume from chunk 4"
```

**Resume Handler**:
```python
resume_log = read(_analysis_log.md)
chunks_remaining = resume_log['chunks_remaining']
Task(prompt=f"Resume from chunk {chunks_remaining[0]}, APPEND to index.md")
```

### 6.2 Validation Failure Retry

```python
def verify_subagent_output(batch_files: List[Path]) -> dict:
    """Spot-check 10% of extracted patterns."""
    failed_patterns = []

    for batch in batch_files:
        for pattern in sample(batch['patterns'], rate=0.1):
            chunk_ref = pattern['chunk_ref']
            quote = pattern['quote']

            actual_lines = read_chunk(chunk_ref)
            if quote not in actual_lines:
                failed_patterns.append({...})

    if len(failed_patterns) / len(patterns) < 0.1:
        return PASS
    else:
        return FAIL  # Re-extract worst batches
```

---

## 7. Concurrency & Performance

### 7.1 Max Concurrent Subagents

```python
MAX_CONCURRENT = 15  # Parallel subagent limit

# Applied at different stages:
# - Phase 2 (Analysis): 15 concurrent paper analyses
# - Level 4 (Extraction): 15 concurrent field batches
# - Level 7 (Report): 1-3 passes depending on budget
```

### 7.2 Token Budget Management

```python
def calculate_level7_budget(synthesis_files: List[Path]) -> dict:
    """Pre-calculate token budget for final report."""
    total_input_tokens = sum(len(f.read_text()) // 4 for f in synthesis_files)

    budget = {
        'methodology': 3000,
        'briefing': 2000,
        'synthesis_files': total_input_tokens,
        'output_reservation': 20000,
        'total_available': 100000,
        'usable': 100000 - 3000 - 2000 - 20000 - total_input_tokens
    }

    if budget['usable'] < 10000:
        budget['requires_split'] = True
        budget['split_strategy'] = 'group_by_priority'

    return budget
```

---

## 8. Key Design Principles

1. **Pre-Calculation Over Dynamics**: All allocation happens upfront, written to files, read back in next phase
2. **Strict Contracts**: INPUT/OUTPUT contracts enforced, violations cause failures
3. **Citation Preservation**: Every level maintains Paper-ID (Chunk:Line) format
4. **Deterministic Scripts for Aggregation**: YAML-to-YAML merging uses Python scripts, not subagents
5. **Token Budgets as Real Constraints**: Level 7 has calculated budget with split strategy
6. **Verification at Every Level**: Quote-line checking, schema validation, anti-hallucination rules
7. **Graceful Partial Saves**: Timeout recovery with chunks_completed/chunks_remaining
8. **Domain-Aware Personalization**: Dynamic persona selection based on keywords

---

## Example: Complete Paper Analysis Flow

```
INPUT: 1 large paper (14 chunks)
├─ Phase 1, Step 12: Allocation calculated → 2 subagents
│  └─ Written to plan.md: "Large_Paper | 14 | ~85,000 | 2 | 1-7, 8-14"
│
├─ Phase 2, Step 1.5: READ allocation from plan.md
│  └─ Do NOT recalculate
│
├─ Phase 2, Step 2: Spawn subagents
│  ├─ Subagent 1: Analyze chunks 1-7 → index_part1.md
│  │  ├─ INPUT CONTRACT lists chunks 1-7 only
│  │  └─ OUTPUT: YAML frontmatter with chunk_index[1-7]
│  │
│  ├─ Subagent 2: Analyze chunks 8-14 → index_part2.md
│  │  ├─ INPUT CONTRACT lists chunks 8-14 only
│  │  └─ OUTPUT: YAML frontmatter with chunk_index[8-14]
│  │
│  └─ Wait for both (max 15 concurrent papers)
│
├─ Merge Subagent: Combine parts → index.md
│  ├─ INPUT: Read index_part1.md + index_part2.md
│  ├─ OUTPUT: Single index.md with chunk_index[1-14]
│  └─ Validation: chunks_read (14) == chunks_expected (14)
│
└─ Phase 2, Step 3: Validate
   └─ Check index.md YAML schema, quote-line verification
```

---

*Generated by orchestrator subagent analysis*
