# Orchestrator Instructions Template

**Copy this section into plan.md after Step 9 (Acquisition Complete)**

---

## Orchestrator Instructions

### Constants

```
PROJECT = "02-projects/{project_id}"
PAPERS = "{PROJECT}/02-resources/papers"
KIT = "{PROJECT}/02-resources/_analysis_kit.md"
METHODOLOGY = "03-skills/paper-analyze-core/SKILL.md"
```

---

### Phase 4: Paper Analysis

#### 4.1 Subagent Prompt Template (GENERIC)

```
TEMPLATE = """Analyze paper: {paper_id}

Read IN ORDER:
1. {PROJECT}/02-resources/_analysis_kit.md
2. 03-skills/paper-analyze-core/SKILL.md
3. {PROJECT}/02-resources/papers/{paper_id}/_metadata.json
4. ALL chunks listed in _metadata.json

Write:
1. {PROJECT}/02-resources/papers/{paper_id}/_analysis_log.md
2. {PROJECT}/02-resources/papers/{paper_id}/index.md

CRITICAL:
- Read ALL chunks (validation will check chunks_read == chunks_expected)
- Include chunk refs for every finding
- Set analysis_complete: true in index.md frontmatter"""
```

#### 4.2 Batch Execution

**Launch papers in parallel batches (max 10 concurrent):**

| Batch | Paper IDs | Count |
|-------|-----------|-------|
| 1 | {batch_1_papers} | {count} |
| 2 | {batch_2_papers} | {count} |
| ... | ... | ... |

**For each paper_id in batch, spawn:**
```
Task(
  subagent_type="general-purpose",
  prompt=TEMPLATE.format(paper_id=paper_id)
)
```

#### 4.3 Large Paper Split (>8 chunks)

For papers with >8 chunks, split into 2 subagents:
- **Part 1**: Chunks 1-{mid} → writes `index_part1.md`
- **Part 2**: Chunks {mid+1}-end → writes `index_part2.md`
- **Merge**: Orchestrator combines into `index.md`

---

### Phase 4.5: Validation (AFTER EACH BATCH)

**Run hallucination check on completed papers:**

For each paper with `index.md`:

```python
def validate_paper(paper_id):
    index_path = f"{PAPERS}/{paper_id}/index.md"
    metadata_path = f"{PAPERS}/{paper_id}/_metadata.json"

    # 1. index.md exists
    if not exists(index_path):
        return FAIL("index.md missing")

    # 2. Parse YAML frontmatter
    frontmatter = parse_yaml(index_path)
    metadata = parse_json(metadata_path)

    # 3. chunks_read == chunks_expected
    expected = len(metadata["chunks"])
    actual = frontmatter.get("chunks_read", 0)
    if actual != expected:
        return FAIL(f"Chunk mismatch: read {actual}, expected {expected}")

    # 4. analysis_complete == true
    if not frontmatter.get("analysis_complete"):
        return FAIL("analysis_complete not set")

    # 5. At least 1 high-priority field found
    if frontmatter.get("high_priority_fields_found", 0) < 1:
        return WARN("No high-priority fields extracted")

    return PASS
```

**Actions:**
- PASS → Mark paper complete in steps.md
- WARN → Flag for review but continue
- FAIL → Add to retry queue

**Retry queue processed after all batches complete.**

---

### Phase 5: Synthesis

**Only run after Phase 4.5 validation passes for all papers:**

```
Task(
  subagent_type="general-purpose",
  prompt="Synthesize findings across all papers.

Read:
1. {PROJECT}/02-resources/_analysis_kit.md (research question)
2. 03-skills/paper-synthesize/SKILL.md (methodology)
3. ALL {PROJECT}/02-resources/papers/*/index.md files

Write: {PROJECT}/04-outputs/_synthesis.md

Focus on:
{synthesis_focus_areas}"
)
```

---

### Concurrency Settings

| Setting | Value |
|---------|-------|
| Max parallel subagents | **10** |
| Timeout per subagent | 5 minutes |
| Retry on failure | 1 attempt |
| Validation | After each batch |
