---
project_id: "16-ontologies-research-v3"
project_path: "02-projects/16-ontologies-research-v3"
generated: "2025-12-28T16:00:00"
schema_version: "v2.3"
---

# Analysis Kit for Ontologies Research

**This file contains everything a subagent needs to analyze a paper in this project.**

---

## Research Question

**What are the foundational ontologies for digital work, and how do they ground entity definitions, framework comparisons, and AI agent/generative AI integration patterns?**

### Sub-questions

1. What entities are universal across foundational ontologies (UFO, PROV-O, BBO)?
2. How does the Agent-Activity-Entity triad manifest in different frameworks?
3. What is the relationship between abstraction level and entity count?
4. How can foundational ontologies ground the 8-entity hypothesis (Goal, Task, Rule, Resource, Role, Data, Event, Agent)?
5. What patterns enable AI agents to interact with ontological structures?
6. How do LLM-based agents use ontologies for reasoning, planning, and tool selection?
7. What multi-agent architectures leverage ontological knowledge?

---

## Synthesis Goals (G22b)

> **Why This Matters to Subagents**: The synthesis phase will aggregate your extractions across all papers. Understanding what the final synthesis needs helps you prioritize what to extract.

### Primary Synthesis Outputs

1. **Entity Taxonomy**: Cross-framework comparison of entity types, showing how UFO, PROV-O, BBO, and domain ontologies define similar concepts differently
2. **Agent-Activity-Entity Triad Validation**: Evidence for/against the universality of this foundational pattern
3. **8-Entity Hypothesis Grounding**: Map extracted entities to Goal, Task, Rule, Resource, Role, Data, Event, Agent
4. **AI Integration Patterns Catalog**: How ontologies enable LLM reasoning, tool selection, and structured outputs
5. **Abstraction-Entity Count Relationship**: Data points showing how purpose drives entity granularity

### What Makes a High-Value Extraction

- **Definitions with distinguishing criteria**: "X differs from Y because..."
- **Explicit relationships**: "X participates-in Y", "A is-a B"
- **Concrete examples**: Real implementations, not just theory
- **Comparisons to other frameworks**: Cross-references to UFO, PROV-O, ArchiMate
- **AI/LLM integration patterns**: Specific techniques, not generic claims

### Low-Value Extractions (Avoid)

- Generic definitions available on Wikipedia
- Marketing claims without evidence
- Theoretical possibilities without examples
- Duplicate information already captured by another field

---

## Extraction Schema

Extract these fields from each paper:

| Field | Description | Priority |
|-------|-------------|----------|
| entity_types | Core entity types defined (e.g., Agent, Activity, Entity, Endurant, Perdurant) | HIGH |
| entity_definitions | Formal definitions and distinguishing characteristics of each entity | HIGH |
| entity_relationships | Relationships between entities (structural, behavioral, organizational) | HIGH |
| abstraction_level | Level of abstraction (foundational, domain, application) and purpose | HIGH |
| framework_comparison | How this ontology compares to others (UFO, PROV-O, BBO, ArchiMate, TOGAF, OCEL) | HIGH |
| ai_integration | How ontology enables AI agents, LLMs, RAG, planning, guardrails | HIGH |
| agent_modeling | How agents/actors are modeled (autonomous, intentional, role-based) | HIGH |
| agentic_workflows | Multi-agent systems, agent orchestration, tool use, planning strategies | HIGH |
| generative_ai_patterns | LLM reasoning, chain-of-thought, ReAct, function calling, structured outputs | HIGH |
| agent_ontology_integration | How AI agents interact with ontologies (RAG, KG querying, ontology-guided reasoning) | HIGH |
| entity_count | Number of entity classes/types in the framework and rationale | MEDIUM |
| methodology | Top-down (theoretical) vs bottom-up (empirical) approach | MEDIUM |
| empirical_evidence | Process mining data, enterprise logs, real-world validation | MEDIUM |
| limitations | What the ontology cannot capture (tacit knowledge, improvisation, etc.) | MEDIUM |
| tools_standards | Technical implementations (OWL, RDF, BPMN, CMMN, DMN, OCEL 2.0) | MEDIUM |

---

## Focus Areas

Look specifically for:
- Foundational ontologies: UFO (Unified Foundational Ontology), PROV-O, BBO
- The Agent-Activity-Entity triad as universal pattern
- Entity count abstraction-dependency (4-106 entities based on purpose)
- Integration with BPM+ standards (BPMN, CMMN, DMN, SDMN)
- Object-Centric Process Mining (OCEL 2.0) empirical grounding
- MVO metamodel and AI agent integration patterns
- Validation of 8-entity hypothesis (Goal, Task, Rule, Resource, Role, Data, Event, Agent)
- AI Agent architectures: ReAct, Chain-of-Thought, function calling, tool use
- Multi-agent systems and agent orchestration frameworks
- Ontology-guided LLM reasoning and structured generation
- Knowledge graphs as agent memory and reasoning substrate
- Agentic workflow patterns for business process automation

---

## Skip Sections

Don't extract from:
- Acknowledgments
- Author biographies
- Conference logistics
- Funding statements
- References (unless citing specific patterns)

---

## Output Requirements

### 1. Analysis Log (`_analysis_log.md`)

For methodology reference, read: `03-skills/research-pipeline/shared/paper-analyze-core/references/analysis_log_template.md`

Key requirements:
- Record evidence (start + end) for each chunk
- Include chunk:line reference for every extraction
- Log which chunks were read

### 2. Index File (`index.md`)

For output format, read: `03-skills/research-pipeline/shared/paper-analyze-core/references/index_template.md`

**REQUIRED YAML frontmatter fields (Schema v2.3):**

```yaml
---
paper_id: "{paper_id}"
title: "{paper title}"
schema_version: "v2.3"
chunks_expected: {N}      # From _metadata.json
chunks_read: {N}          # Must equal chunks_expected
analysis_complete: true   # Set to true when done
high_priority_fields_found: {N}  # Count of HIGH priority fields with extractions

# Schema v2.3: chunk_index with per-chunk fields_found (3-state)
chunk_index:
  1:
    token_count: {N}      # len(chunk_text) // 4
    fields_found:
      entity_types: true|partial|false
      entity_definitions: true|partial|false
      entity_relationships: true|partial|false
      # ... all 15 fields
  2:
    token_count: {N}
    fields_found: {...}
  # ... for all chunks

# Extraction fields (all 15)
entity_types: []
entity_definitions: {}
entity_relationships: []
abstraction_level: ""
framework_comparison: []
ai_integration: []
agent_modeling: []
agentic_workflows: []
generative_ai_patterns: []
agent_ontology_integration: []
entity_count: null
methodology: ""
empirical_evidence: []
limitations: []
tools_standards: []
---
```

**Schema v2.3 Requirements:**
- `chunk_index`: Per-chunk metadata with `fields_found` assessment
- `fields_found`: 3-state value for each field:
  - `true`: Clear, extractable content found
  - `partial`: Some relevant content, but incomplete
  - `false`: Field not addressed in this chunk
- `token_count`: Estimated as `len(chunk_text) // 4`
- Hash is computed by validation script (not required in output)

---

## File Locations

The orchestrator provides absolute paths. Relative structure:

| Purpose | Relative Path |
|---------|---------------|
| Paper chunks | `02-resources/papers/{paper_id}/{paper_id}_N.md` |
| Chunk metadata | `02-resources/papers/{paper_id}/_metadata.json` |
| Analysis log output | `02-resources/papers/{paper_id}/_analysis_log.md` |
| Index output | `02-resources/papers/{paper_id}/index.md` |

---

## Subagent Instructions

1. Read this analysis kit (you're reading it now)
2. Read the extraction guide: `02-resources/_extraction_guide.md`
3. Read the methodology: `03-skills/research-pipeline/shared/paper-analyze-core/SKILL.md`
4. Read the paper's `_metadata.json` to get chunk list
5. Read ALL chunks listed in `_metadata.json`
6. Extract findings per the schema above
7. Write `_analysis_log.md` and `index.md` with REQUIRED frontmatter

**CRITICAL RULES:**
- Do NOT read the PDF file
- Do NOT skip any chunks
- Include chunk:line reference for every finding (e.g., "Chunk 3:45-52")
- Set `chunks_read` = `chunks_expected` (validates you read everything)
- Set `analysis_complete: true` only when fully done
- For AI papers: focus on HIGH priority fields 6-10 (ai_integration through agent_ontology_integration)
- For ontology papers: focus on HIGH priority fields 1-5 (entity_types through framework_comparison)

---

## Validation Contract (Schema v2.3)

Your output will be validated. The following MUST be true:

| Check | Requirement |
|-------|-------------|
| `index.md` exists | File must be created |
| `_analysis_log.md` exists | File must be created |
| `schema_version == "v2.3"` | Must be Schema v2.3 |
| `chunks_read == chunks_expected` | All chunks were read |
| `analysis_complete == true` | Analysis finished |
| `high_priority_fields_found >= 1` | At least 1 HIGH priority extraction |
| `chunk_index` exists | Per-chunk metadata required |
| `chunk_index` has all chunks | Entry for each chunk (1 to N) |
| `fields_found` uses 3-state | Values must be true/partial/false |
| Evidence has chunk:line refs | Every finding cites chunk and lines |
| Evidence complete | Each chunk has start + end evidence |

**Schema v2.3 Validation (run with `--check-chunk-index`):**
```bash
python 03-skills/research-pipeline/skills/paper-analyze/scripts/validate_analysis.py \
  02-projects/16-ontologies-research-v3/02-resources/papers/{paper_id} \
  --check-chunk-index
```

**If validation fails, the paper will be retried.**
