---
name: paper-analyze
description: Orchestrate paper analysis by spawning Claude Code subagents. Load when user says "analyze papers", "analyze collection", "process papers", or "run analysis on papers". Spawns subagents that follow paper-analyze-core methodology to produce index.md for each paper.
---

# Paper Analyze

Orchestrate paper analysis by spawning Claude Code subagents for each paper.

## Prerequisites

- Papers must be preprocessed (chunks exist via `pdf-preprocess`)
- Collection must have `_briefing.md` with research question and fields
- `paper-analyze-core` skill must exist (methodology for subagents)

## Workflow

### Step 1: Validate Collection

1. Read `_briefing.md` from collection folder
2. List all paper folders (subdirectories with `_metadata.json`)
3. Filter papers that need analysis (no `index.md` yet)

### Step 2: Estimate Tokens & Plan Subagent Allocation

**Token estimation**: Each chunk ≈ 10-15k tokens (1000 lines × ~50 chars/line)
**Usable budget**: 74k tokens per subagent (after 26k methodology overhead)

For each paper:

```python
# Token estimation from _metadata.json
chunks = metadata.total_chunks
chars = metadata.total_chars
tokens = (chars / 5) * 1.3  # ~12k tokens per chunk on average

# Allocation rules
if chunks <= 6:
    subagents = 1
    split = None
elif chunks <= 12:
    subagents = 2
    split = [range(1, 7), range(7, chunks + 1)]
elif chunks <= 18:
    subagents = 3
    split = [range(1, 7), range(7, 13), range(13, chunks + 1)]
else:
    # Split into 5-6 chunk segments
    subagents = ceil(chunks / 6)
    split = [range(i*6 + 1, min((i+1)*6 + 1, chunks + 1)) for i in range(subagents)]
```

| Chunk Count | Subagents | Strategy |
|-------------|-----------|----------|
| 1-6 chunks | 1 | Single subagent |
| 7-12 chunks | 2 | Split at chunk 6 |
| 13-18 chunks | 3 | Split into 6-chunk segments |
| 19+ chunks | 4+ | Split into 5-6 chunk segments |

### Step 3: Spawn Subagents

For each paper, spawn a Task with `subagent_type="general-purpose"`:

**Subagent Prompt Template (Schema v2.0):**

```
You are analyzing a paper for the research pipeline.

## Instructions

Read these files IN ORDER:
1. 03-skills/research-pipeline/shared/paper-analyze-core/SKILL.md (methodology - includes Schema v2.0)
2. 03-skills/research-pipeline/shared/paper-analyze-core/references/analysis_log_template.md (log template)
3. {collection_path}/_briefing.md (research question + fields)
4. {paper_path}/_metadata.json (paper info)
5. {paper_path}/{paper}_1.md, {paper}_2.md, ... (all chunks)

Follow the 7-step methodology in paper-analyze-core:
0. Initialize analysis log (FIRST)
1. Read briefing
2. Read metadata
3. Analyze chunks (with multi-point evidence)
4. Compile index.md
5. Validate
6. Complete analysis log (LAST)

## CRITICAL: Anti-Hallucination Requirements

You MUST record multi-point evidence for EACH chunk in _analysis_log.md:
- `start`: First 100 chars AFTER header line
- `end`: Last 100 chars of chunk
- `hash`: SHA256 of full chunk content

This evidence will be validated. If it doesn't match the actual chunks, your analysis fails.

## Output

Write TWO files:

### 1. Analysis Log (FIRST - Schema v2.0)
Write to: {paper_path}/_analysis_log.md

Use the full YAML schema from analysis_log_template.md. Include:
- All step completion fields
- Multi-point chunk evidence (start/end/hash for each chunk)
- Performance metrics
- Quality assessment

### 2. Index File (SECOND)
Write to: {paper_path}/index.md

[Follow paper-analyze-core methodology for index.md format]

Do NOT read any other files. Do NOT read the PDF.
```

### Step 4: Handle Large Papers

If `parts > 1`, spawn multiple subagents with chunk subsets:

**Part Subagent Prompt:**

```
You are analyzing PART {N} of {TOTAL} for paper: {title}

Read chunks {start} through {end} only.
Produce index_part{N}.md instead of index.md.

[Same methodology instructions]
```

After all parts complete, spawn merge subagent:

**Merge Subagent Prompt:**

```
Merge partial indexes into final index.md:

1. Read all index_part*.md files
2. Combine YAML frontmatter (deduplicate arrays)
3. Merge chunk navigation sections in order
4. Write final index.md
5. Delete index_part*.md files
```

### Step 5: Validate Analysis Logs

**After ALL subagents complete**, run validation on each paper:

```python
for paper in analyzed_papers:
    log_path = f"{paper_path}/_analysis_log.md"

    # Check log exists
    if not exists(log_path):
        results[paper] = {"status": "FAILED", "reason": "No analysis log"}
        continue

    # Parse YAML frontmatter
    log = parse_yaml(log_path)

    # Validate schema version
    if log.get("schema_version") != "2.0":
        results[paper] = {"status": "FAILED", "reason": "Schema v2.0 required"}
        continue

    # Validate all steps completed
    for step in log["steps"].values():
        if not step.get("completed"):
            results[paper] = {"status": "FAILED", "reason": f"Step incomplete"}
            continue

    # Validate chunk evidence
    for chunk_num, evidence in log["steps"]["step3_analyze_chunks"]["chunk_evidence"].items():
        chunk_path = f"{paper_path}/{paper}_{chunk_num}.md"
        chunk_content = read_file(chunk_path)

        # Skip header, get first 100 chars
        content_after_header = chunk_content.split('\n', 1)[1] if '\n' in chunk_content else chunk_content
        if content_after_header[:100].strip() != evidence["start"].strip():
            results[paper] = {"status": "FAILED", "reason": f"Evidence mismatch chunk {chunk_num} (start)"}
            continue

        # Check last 100 chars
        if chunk_content[-100:].strip() != evidence["end"].strip():
            results[paper] = {"status": "FAILED", "reason": f"Evidence mismatch chunk {chunk_num} (end)"}
            continue

        # Check hash
        computed_hash = sha256(chunk_content)
        if computed_hash != evidence["hash"]:
            results[paper] = {"status": "FAILED", "reason": f"Hash mismatch chunk {chunk_num}"}
            continue

    results[paper] = {"status": "PASSED", "validation_passed": True}
```

**Note**: For full validation script, see `scripts/validate_analysis.py`.

### Step 6: Report Results

```
Analysis Complete
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ Analyzed: 5 papers
  ✓ Validated: 4 papers (logs pass all checks)
  ⚠ Warnings: 1 paper (minor issues, usable)
✗ Failed: 1 paper (Smith_2020 - evidence mismatch)
⊘ Skipped: 2 papers (already have index.md)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Validation Report: {collection_path}/_validation_report.md
```

## Execution

### Analyze Entire Collection

```
User: "Analyze all papers in TA_LLM collection"

1. Read 04-workspace/papers/TA_LLM/_briefing.md
2. Find papers: Braun_Clarke_2006, Smith_2020, ...
3. Spawn subagents for each (max 15 concurrent)
4. Report results
```

### Analyze Single Paper

```
User: "Analyze the Braun Clarke paper"

1. Find paper folder
2. Estimate tokens
3. Spawn single subagent
4. Report result
```

### Re-analyze (Force)

```
User: "Re-analyze all papers (overwrite existing)"

1. Delete existing index.md files
2. Run full analysis
```

## Concurrency

- **Max concurrent subagents**: 15 (parallel analysis for speed)
- **Timeout per paper**: 5 minutes
- **Retry on failure**: 1 attempt

## Error Handling

| Error | Action |
|-------|--------|
| No _briefing.md | Abort with error message |
| No chunks found | Skip paper, log warning |
| Subagent fails | Retry once, then log failure |
| Subagent timeout | Log timeout, continue to next |

## Token Budgets

| Component | Tokens | Notes |
|-----------|--------|-------|
| Subagent context | 100,000 | Claude model limit |
| Methodology | 3,000 | paper-analyze-core |
| Briefing | 2,000 | _briefing.md |
| Metadata | 500 | _metadata.json |
| **Paper content** | **75,000** | Usable for chunks |
| Output buffer | 19,500 | index.md generation |

Papers exceeding 75k tokens are split into parts.
