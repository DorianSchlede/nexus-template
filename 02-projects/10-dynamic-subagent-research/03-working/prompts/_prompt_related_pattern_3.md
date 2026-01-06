# Batch Extraction: related_pattern (Batch 3 of 5)

## INPUT CONTRACT (STRICT - Gap G13)

### Files You MUST Read (in this order)
1. `C:\Users\dsber\infinite\auto-company\strategy-nexus\02-projects\10-dynamic-subagent-research/02-resources/_briefing.md`
2. `C:\Users\dsber\infinite\auto-company\strategy-nexus\02-projects\10-dynamic-subagent-research/02-resources/_extraction_guide.md`
3. `C:\Users\dsber\infinite\auto-company\strategy-nexus\02-projects\10-dynamic-subagent-research/02-resources/papers/04-GCC-2508.00031/04-GCC-2508.00031_1.md`
4. `C:\Users\dsber\infinite\auto-company\strategy-nexus\02-projects\10-dynamic-subagent-research/02-resources/papers/04-GCC-2508.00031/04-GCC-2508.00031_2.md`
5. `C:\Users\dsber\infinite\auto-company\strategy-nexus\02-projects\10-dynamic-subagent-research/02-resources/papers/07-ProtocolBench-2510.17149/07-ProtocolBench-2510.17149_2.md`
6. `C:\Users\dsber\infinite\auto-company\strategy-nexus\02-projects\10-dynamic-subagent-research/02-resources/papers/07-ProtocolBench-2510.17149/07-ProtocolBench-2510.17149_6.md`
7. `C:\Users\dsber\infinite\auto-company\strategy-nexus\02-projects\10-dynamic-subagent-research/02-resources/papers/07-ProtocolBench-2510.17149/07-ProtocolBench-2510.17149_7.md`
8. `C:\Users\dsber\infinite\auto-company\strategy-nexus\02-projects\10-dynamic-subagent-research/02-resources/papers/08-LACP-2510.13821/08-LACP-2510.13821_1.md`
9. `C:\Users\dsber\infinite\auto-company\strategy-nexus\02-projects\10-dynamic-subagent-research/02-resources/papers/08-LACP-2510.13821/08-LACP-2510.13821_2.md`
10. `C:\Users\dsber\infinite\auto-company\strategy-nexus\02-projects\10-dynamic-subagent-research/02-resources/papers/09-SEMAP-2510.12120/09-SEMAP-2510.12120_1.md`
11. `C:\Users\dsber\infinite\auto-company\strategy-nexus\02-projects\10-dynamic-subagent-research/02-resources/papers/10-TalkHier-2502.11098/10-TalkHier-2502.11098_1.md`
12. `C:\Users\dsber\infinite\auto-company\strategy-nexus\02-projects\10-dynamic-subagent-research/02-resources/papers/10-TalkHier-2502.11098/10-TalkHier-2502.11098_2.md`
13. `C:\Users\dsber\infinite\auto-company\strategy-nexus\02-projects\10-dynamic-subagent-research/02-resources/papers/12-CollabSurvey-2501.06322/12-CollabSurvey-2501.06322_1.md`
14. `C:\Users\dsber\infinite\auto-company\strategy-nexus\02-projects\10-dynamic-subagent-research/02-resources/papers/12-CollabSurvey-2501.06322/12-CollabSurvey-2501.06322_2.md`

### Files You MUST NOT Read
- ANY `.pdf` file
- ANY other batch's chunks
- ANY file in 04-outputs/
- ANY file outside `C:\Users\dsber\infinite\auto-company\strategy-nexus\02-projects\10-dynamic-subagent-research/`

### Directory Traversal FORBIDDEN
- Do NOT use `../` paths
- Do NOT follow symbolic links
- Stay within `C:\Users\dsber\infinite\auto-company\strategy-nexus\02-projects\10-dynamic-subagent-research/` boundary

VIOLATION = Extraction fails validation.

---

## CONTEXT

### Research Purpose (Gap G22a)
Wissenschaftliche Analyse der entwickelten Dynamic Subagent Patterns für High-Quality Data Transfer. Ziel: Pattern-Catalog, Best-Practice Guidelines, und akademische Publikation.

### Synthesis Goals (Gap G22b)
Extract patterns that support cross-paper synthesis (synthesis goals not specified in _analysis_kit.md)

---

## EXTRACTION CONTRACT

For field "related_pattern":
1. Read EACH chunk file completely - do not skim
2. Extract ALL patterns related to "related_pattern"
3. For EVERY pattern you find, include:
   - name: Pattern name (specific, not generic)
   - chunk_ref: "Paper-ID (Chunk N:Line-Line)"
   - quote: "Exact text from chunk" (100-150 chars)
   - description: Full context and detail

4. Write YAML output to: `C:\Users\dsber\infinite\auto-company\strategy-nexus\02-projects\10-dynamic-subagent-research/03-working/_batch_related_pattern_3.yaml`

---

## OUTPUT SCHEMA

```yaml
---
batch_id: "related_pattern_3"
field: related_pattern
extracted_at: "{timestamp}"
chunks_read: {count}
patterns_found: {count}
---

patterns:
  - name: "Pattern Name"
    chunk_ref: "Paper-ID (Chunk N:Line-Line)"
    quote: "Exact text proving pattern exists in this chunk..."
    description: "Full context: what this pattern means, how it relates to related_pattern"

  - name: "Another Pattern"
    chunk_ref: "Paper-ID (Chunk M:Line-Line)"
    quote: "Another exact quote..."
    description: "Context for this pattern"
```

---

## CRITICAL REQUIREMENTS

1. You MUST read the actual chunk files listed above
2. You MUST include exact quotes with line numbers
3. You MUST use citation format: Paper-ID (Chunk N:Line-Line)
4. Do NOT summarize - include full detail from chunks
5. Do NOT skip any relevant patterns in the chunks
6. Do NOT read any files not listed in INPUT CONTRACT
