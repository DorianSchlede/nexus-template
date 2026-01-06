# Batch Extraction: limitations (Batch 3 of 3)

## INPUT CONTRACT (STRICT - Gap G13)

### Files You MUST Read (in this order)
1. `c:\Users\dsber\infinite\auto-company\strategy-nexus\02-projects\09-ontologies-research-v22-archive/02-resources/_briefing.md`
2. `c:\Users\dsber\infinite\auto-company\strategy-nexus\02-projects\09-ontologies-research-v22-archive/02-resources/_extraction_guide.md`
3. `c:\Users\dsber\infinite\auto-company\strategy-nexus\02-projects\09-ontologies-research-v22-archive/02-resources/papers/03-PROV-AGENT_Unified_Provenance_for_AI_Agents/03-PROV-AGENT_Unified_Provenance_for_AI_Agents_1.md`

### Files You MUST NOT Read
- ANY `.pdf` file
- ANY other batch's chunks
- ANY file in 04-outputs/
- ANY file outside `c:\Users\dsber\infinite\auto-company\strategy-nexus\02-projects\09-ontologies-research-v22-archive/`

### Directory Traversal FORBIDDEN
- Do NOT use `../` paths
- Do NOT follow symbolic links
- Stay within `c:\Users\dsber\infinite\auto-company\strategy-nexus\02-projects\09-ontologies-research-v22-archive/` boundary

VIOLATION = Extraction fails validation.

---

## CONTEXT

### Research Purpose (Gap G22a)
Validate the 8-entity hypothesis (Goal, Task, Rule, Resource, Role, Data, Event, Agent) for UDWO metamodel grounding. Inform internal ontology design for AI agent orchestration platform. Enable ontology-guided LLM reasoning and structured generation patterns.

### Synthesis Goals (Gap G22b)
Extract patterns that support cross-paper synthesis (synthesis goals not specified in _analysis_kit.md)

---

## EXTRACTION CONTRACT

For field "limitations":
1. Read EACH chunk file completely - do not skim
2. Extract ALL patterns related to "limitations"
3. For EVERY pattern you find, include:
   - name: Pattern name (specific, not generic)
   - chunk_ref: "Paper-ID (Chunk N:Line-Line)"
   - quote: "Exact text from chunk" (100-150 chars)
   - description: Full context and detail

4. Write YAML output to: `c:\Users\dsber\infinite\auto-company\strategy-nexus\02-projects\09-ontologies-research-v22-archive/03-working/_batch_limitations_3.yaml`

---

## OUTPUT SCHEMA

```yaml
---
batch_id: "limitations_3"
field: limitations
extracted_at: "{timestamp}"
chunks_read: {count}
patterns_found: {count}
---

patterns:
  - name: "Pattern Name"
    chunk_ref: "Paper-ID (Chunk N:Line-Line)"
    quote: "Exact text proving pattern exists in this chunk..."
    description: "Full context: what this pattern means, how it relates to limitations"

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
