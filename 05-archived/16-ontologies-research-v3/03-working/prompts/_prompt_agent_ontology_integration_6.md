# Batch Extraction: agent_ontology_integration (Batch 6 of 6)

## INPUT CONTRACT (STRICT - Gap G13)

### Files You MUST Read (in this order)
1. `C:\Users\dsber\infinite\auto-company\strategy-nexus\02-projects\16-ontologies-research-v3/02-resources/_briefing.md`
2. `C:\Users\dsber\infinite\auto-company\strategy-nexus\02-projects\16-ontologies-research-v3/02-resources/_extraction_guide.md`
3. `C:\Users\dsber\infinite\auto-company\strategy-nexus\02-projects\16-ontologies-research-v3/02-resources/papers/21-LLM_Smart_Contracts_from_BPMN/21-LLM_Smart_Contracts_from_BPMN_1.md`
4. `C:\Users\dsber\infinite\auto-company\strategy-nexus\02-projects\16-ontologies-research-v3/02-resources/papers/31-BBO_BPMN_Ontology/31-BBO_BPMN_Ontology_1.md`

### Files You MUST NOT Read
- ANY `.pdf` file
- ANY other batch's chunks
- ANY file in 04-outputs/
- ANY file outside `C:\Users\dsber\infinite\auto-company\strategy-nexus\02-projects\16-ontologies-research-v3/`

### Directory Traversal FORBIDDEN
- Do NOT use `../` paths
- Do NOT follow symbolic links
- Stay within `C:\Users\dsber\infinite\auto-company\strategy-nexus\02-projects\16-ontologies-research-v3/` boundary

VIOLATION = Extraction fails validation.

---

## CONTEXT

### Research Purpose (Gap G22a)
Validate the 8-entity hypothesis (Goal, Task, Rule, Resource, Role, Data, Event, Agent) for UDWO metamodel grounding. Inform internal ontology design for AI agent orchestration platform. Enable ontology-guided LLM reasoning and structured generation patterns.

### Synthesis Goals (Gap G22b)
Extract patterns that support cross-paper synthesis (synthesis goals not specified in _analysis_kit.md)

---

## EXTRACTION CONTRACT

For field "agent_ontology_integration":
1. Read EACH chunk file completely - do not skim
2. Extract ALL patterns related to "agent_ontology_integration"
3. For EVERY pattern you find, include:
   - name: Pattern name (specific, not generic)
   - chunk_ref: "Paper-ID (Chunk N:Line-Line)"
   - quote: "Exact text from chunk" (100-150 chars)
   - description: Full context and detail

4. Write YAML output to: `C:\Users\dsber\infinite\auto-company\strategy-nexus\02-projects\16-ontologies-research-v3/03-working/_batch_agent_ontology_integration_6.yaml`

---

## OUTPUT SCHEMA

```yaml
---
batch_id: "agent_ontology_integration_6"
field: agent_ontology_integration
extracted_at: "{timestamp}"
chunks_read: {count}
patterns_found: {count}
---

patterns:
  - name: "Pattern Name"
    chunk_ref: "Paper-ID (Chunk N:Line-Line)"
    quote: "Exact text proving pattern exists in this chunk..."
    description: "Full context: what this pattern means, how it relates to agent_ontology_integration"

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
