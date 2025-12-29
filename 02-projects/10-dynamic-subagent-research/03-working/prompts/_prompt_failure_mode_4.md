# Batch Extraction: failure_mode (Batch 4 of 4)

## INPUT CONTRACT (STRICT - Gap G13)

### Files You MUST Read (in this order)
1. `C:\Users\dsber\infinite\auto-company\strategy-nexus\02-projects\10-dynamic-subagent-research/02-resources/_briefing.md`
2. `C:\Users\dsber\infinite\auto-company\strategy-nexus\02-projects\10-dynamic-subagent-research/02-resources/_extraction_guide.md`
3. `C:\Users\dsber\infinite\auto-company\strategy-nexus\02-projects\10-dynamic-subagent-research/02-resources/papers/18-HallucinationSurvey-2509.18970/18-HallucinationSurvey-2509.18970_3.md`
4. `C:\Users\dsber\infinite\auto-company\strategy-nexus\02-projects\10-dynamic-subagent-research/02-resources/papers/18-HallucinationSurvey-2509.18970/18-HallucinationSurvey-2509.18970_4.md`
5. `C:\Users\dsber\infinite\auto-company\strategy-nexus\02-projects\10-dynamic-subagent-research/02-resources/papers/18-HallucinationSurvey-2509.18970/18-HallucinationSurvey-2509.18970_8.md`
6. `C:\Users\dsber\infinite\auto-company\strategy-nexus\02-projects\10-dynamic-subagent-research/02-resources/papers/19-HalMit-2507.15903/19-HalMit-2507.15903_1.md`
7. `C:\Users\dsber\infinite\auto-company\strategy-nexus\02-projects\10-dynamic-subagent-research/02-resources/papers/19-HalMit-2507.15903/19-HalMit-2507.15903_2.md`
8. `C:\Users\dsber\infinite\auto-company\strategy-nexus\02-projects\10-dynamic-subagent-research/02-resources/papers/22-PROV-AGENT-2508.02866/22-PROV-AGENT-2508.02866_1.md`
9. `C:\Users\dsber\infinite\auto-company\strategy-nexus\02-projects\10-dynamic-subagent-research/02-resources/papers/22-PROV-AGENT-2508.02866/22-PROV-AGENT-2508.02866_2.md`
10. `C:\Users\dsber\infinite\auto-company\strategy-nexus\02-projects\10-dynamic-subagent-research/02-resources/papers/24-EffectiveCollab-2412.05449/24-EffectiveCollab-2412.05449_3.md`

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

For field "failure_mode":
1. Read EACH chunk file completely - do not skim
2. Extract ALL patterns related to "failure_mode"
3. For EVERY pattern you find, include:
   - name: Pattern name (specific, not generic)
   - chunk_ref: "Paper-ID (Chunk N:Line-Line)"
   - quote: "Exact text from chunk" (100-150 chars)
   - description: Full context and detail

4. Write YAML output to: `C:\Users\dsber\infinite\auto-company\strategy-nexus\02-projects\10-dynamic-subagent-research/03-working/_batch_failure_mode_4.yaml`

---

## OUTPUT SCHEMA

```yaml
---
batch_id: "failure_mode_4"
field: failure_mode
extracted_at: "{timestamp}"
chunks_read: {count}
patterns_found: {count}
---

patterns:
  - name: "Pattern Name"
    chunk_ref: "Paper-ID (Chunk N:Line-Line)"
    quote: "Exact text proving pattern exists in this chunk..."
    description: "Full context: what this pattern means, how it relates to failure_mode"

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
