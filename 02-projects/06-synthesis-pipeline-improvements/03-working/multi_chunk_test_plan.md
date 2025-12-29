# Multi-Chunk Subagent Test Plan

**Date**: 2025-12-28
**Test Paper**: 02-Knowledge_Graphs
**Purpose**: Validate subagent behavior on large multi-chunk paper before full migration

---

## Why This Test

Paper 03 (PROV-AGENT) had only 1 chunk. Paper 02 (Knowledge_Graphs) has 15 chunks:
- Tests chunk navigation across multiple files
- Tests chunk_index generation with per-chunk fields_found
- Tests 3-point evidence recording for each chunk
- Tests hash computation for multiple files
- Validates token budget handling (~162k tokens total)

---

## Paper 02 Statistics

| Metric | Value |
|--------|-------|
| Total chunks | 15 |
| Total chars | 647,843 |
| Estimated tokens | ~162,000 (chars // 4) |
| Lines per chunk | ~1000 |
| Overlap | 100 lines |

### Chunk Breakdown

| Chunk | Chars | Est. Tokens |
|-------|-------|-------------|
| 1 | 39,624 | 9,906 |
| 2 | 41,670 | 10,418 |
| 3 | 35,157 | 8,789 |
| 4 | 40,867 | 10,217 |
| 5 | 45,892 | 11,473 |
| 6 | 43,704 | 10,926 |
| 7 | 44,136 | 11,034 |
| 8 | 45,137 | 11,284 |
| 9 | 50,983 | 12,746 |
| 10 | 51,328 | 12,832 |
| 11 | 50,686 | 12,672 |
| 12 | 49,749 | 12,437 |
| 13 | 39,869 | 9,967 |
| 14 | 40,878 | 10,220 |
| 15 | 28,163 | 7,041 |

---

## Test Procedure

### Step 1: Delete Old Analysis (if exists)

```bash
rm -f 02-projects/09-ontologies-research-v22-archive/02-resources/papers/02-Knowledge_Graphs/index.md
rm -f 02-projects/09-ontologies-research-v22-archive/02-resources/papers/02-Knowledge_Graphs/_analysis_log.md
```

### Step 2: Spawn Subagent

Subagent must:
1. Read `_analysis_kit.md` for extraction schema
2. Read `paper-analyze-core/SKILL.md` for methodology
3. Read `_metadata.json` for chunk count (15)
4. Read ALL 15 chunk files in order
5. For EACH chunk:
   - Record 3-point evidence (start, mid, end)
   - Compute SHA256 hash (8-char prefix)
   - Assess fields_found (true/partial/false)
   - Estimate token count (chars // 4)
6. Write `_analysis_log.md` with chunk_evidence for all 15 chunks
7. Write `index.md` with chunk_index containing all 15 entries

### Step 3: Validate Output

```bash
python validate_analysis.py 02-projects/09-ontologies-research-v22-archive/02-resources/papers \
  --paper 02-Knowledge_Graphs \
  --check-chunk-index
```

Expected: PASSED (0 errors, 0 warnings)

---

## Expected Output Structure

### _analysis_log.md

```yaml
schema_version: "2.0"
paper_id: "02-Knowledge_Graphs"
steps:
  step3_analyze_chunks:
    chunks_total: 15
    chunks_read: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    all_chunks_read: true
    chunk_evidence:
      1:
        start: "..."
        mid: "..."
        end: "..."
        hash: "xxxxxxxx"
      2:
        start: "..."
        mid: "..."
        end: "..."
        hash: "xxxxxxxx"
      # ... chunks 3-15
```

### index.md (Schema v2.3)

```yaml
schema_version: "v2.3"
chunks_expected: 15
chunks_read: 15
chunk_index:
  1:
    token_count: 9906
    hash: "xxxxxxxx"
    fields_found:
      entity_types: true/partial/false
      entity_definitions: true/partial/false
      # ... all 15 fields
  2:
    token_count: 10418
    hash: "xxxxxxxx"
    fields_found:
      # ...
  # ... chunks 3-15
```

---

## Success Criteria

1. **All chunks read**: `chunks_read: 15`
2. **All chunks have evidence**: 15 entries in `chunk_evidence`
3. **All chunks have index**: 15 entries in `chunk_index`
4. **Hashes match**: Each chunk hash matches computed SHA256[:8]
5. **Validation passes**: 0 errors, 0 warnings

---

## Risk Factors

| Risk | Mitigation |
|------|------------|
| Context limit exceeded | May need to read chunks in batches |
| Subagent timeout | Monitor progress, allow longer timeout |
| Fields assessment incomplete | Verify all 15 fields assessed per chunk |

---

## Next Steps After Success

If this test passes:
1. Mark paper 02 complete in steps.md
2. Proceed with parallel analysis of remaining 21 papers
3. Or spawn multiple subagents for batch processing

---

*Plan created: 2025-12-28*
