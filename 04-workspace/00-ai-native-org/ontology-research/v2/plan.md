# Ontologies Research (Migration Test) - Plan

**Last Updated**: 2025-12-28
**Status**: Migration Test Ready
**Schema**: v2.2 → v2.3

---

## Research Question

**Primary RQ**: What are the foundational ontologies for digital work, and how do they ground entity definitions, framework comparisons, and AI agent/generative AI integration patterns?

**Focus Areas**:
- Foundational ontologies: UFO, PROV-O, BBO, DOLCE, GFO, BFO
- The Agent-Activity-Entity triad as universal pattern
- Entity count abstraction-dependency (4-106 entities based on purpose)
- Validation of 8-entity hypothesis (Goal, Task, Rule, Resource, Role, Data, Event, Agent)
- AI agent integration with ontological structures
- **AI Agents & Generative AI** (expanded scope):
  - LLM-based agent architectures (ReAct, Chain-of-Thought, function calling)
  - Multi-agent systems and orchestration frameworks
  - Ontology-guided reasoning and structured generation
  - Knowledge graphs as agent memory substrate
  - Agentic workflow patterns for process automation

## Extraction Schema

| Field | Description | Priority |
|-------|-------------|----------|
| entity_types | Core entity types defined | high |
| entity_definitions | Formal definitions and characteristics | high |
| entity_relationships | Relationships between entities | high |
| abstraction_level | Level and purpose | high |
| framework_comparison | Comparison to other ontologies | high |
| ai_integration | How ontology enables AI agents | high |
| agent_modeling | How agents/actors are modeled | high |
| **agentic_workflows** | Multi-agent systems, orchestration, tool use | **high** |
| **generative_ai_patterns** | LLM reasoning, CoT, ReAct, function calling | **high** |
| **agent_ontology_integration** | RAG, KG querying, ontology-guided reasoning | **high** |
| entity_count | Number of classes and rationale | medium |
| methodology | Top-down vs bottom-up | medium |
| empirical_evidence | Real-world validation | medium |
| limitations | What cannot be captured | medium |
| tools_standards | Technical implementations | medium |

---

## Current State

| Metric | Value |
|--------|-------|
| Phase | 3b-Migration Test (CLEAN STATE) |
| Schema Version | v2.2 → v2.3 |
| Papers Approved | 31 |
| Papers Downloaded | 23 |
| Papers with Chunks | 23 |
| Total Chunks | 76 |
| Papers Analyzed | 0 (v2.2 outputs deleted) |
| Test Papers Selected | 3 |
| Project Files Updated | No (G22a/G22b pending) |

---

## Approach

1. **Search Phase**: Query academic databases for foundational ontology papers
2. **Selection Phase**: Review abstracts, score relevance, user approval
3. **Acquisition Phase**: Download PDFs, preprocess to markdown chunks
4. **Analysis Phase**: Extract schema fields from each paper via subagents
5. **Synthesis Phase**: Cross-paper analysis, validate hypotheses

---

## Key Decisions

- **Focus on foundational ontologies**: UFO, PROV-O, BBO as primary targets (per user input)
- **Comprehensive extraction**: All fields (entities, frameworks, AI patterns, empirical evidence)
- **Build on existing synthesis**: Claude and Gemini documents provide starting hypotheses to validate

---

## Resources Needed

**Data Sources**:
- Semantic Scholar API
- arXiv API
- OpenAlex API
- CrossRef API

**Context Documents**:
- `04-workspace/09-ontology research/input/claude-dr-ontology-model.md`
- `04-workspace/09-ontology research/input/gemini-onlogoy-model.md`

---

## Dependencies & Links

**Related Workspace**:
- `04-workspace/09-ontology research/` - Input documents and working files

**Skills Used**:
- `paper-search` - Academic paper search
- `pdf-preprocess` - PDF to markdown conversion
- `paper-analyze` - Subagent analysis orchestration

---

## Open Questions

- [ ] How many papers are available on foundational ontologies?
- [ ] Which foundational ontologies have the most empirical validation?
- [ ] How well does the 8-entity hypothesis hold up against academic literature?

---

## Research Methodology

**Research Questions**:

*Foundational Ontologies:*
1. What entities are universal across foundational ontologies?
2. How does the Agent-Activity-Entity triad manifest?
3. What is the relationship between abstraction level and entity count?
4. How can foundational ontologies ground the 8-entity hypothesis?

*AI Agents & Generative AI:*
5. What patterns enable AI agents to interact with ontological structures?
6. How do LLM-based agents use ontologies for reasoning, planning, and tool selection?
7. What multi-agent architectures leverage ontological knowledge?
8. How can ontologies structure and constrain generative AI outputs?
9. What role do knowledge graphs play as agent memory and reasoning substrate?

**Data Sources**:
- Academic papers on UFO, PROV-O, BBO
- Enterprise architecture frameworks (ArchiMate, TOGAF)
- Process mining literature (OCEL 2.0)
- AI/LLM agent research
- **Multi-agent system architectures (AutoGen, LangGraph, CrewAI)**
- **Ontology + LLM integration papers**
- **Knowledge graph reasoning for agents**
- **Agentic workflow patterns research**

**Analysis Framework**:
- Extract entities and relationships from each paper
- Map to 8-entity hypothesis
- Compare across frameworks
- Identify gaps and extensions

---

## Synthesis Plan

**Reporting Format**:
- Entity taxonomy with definitions
- Framework comparison matrix
- AI integration patterns catalog
- Validation/refinement of 8-entity hypothesis
- **Agentic workflow ontology mapping**
- **LLM + Ontology integration patterns**

**Deliverables**:
- `04-outputs/entity-taxonomy.md`
- `04-outputs/framework-comparison.md`
- `04-outputs/ai-integration-patterns.md`
- `04-outputs/agentic-workflows-ontology.md` (NEW)
- `04-outputs/llm-ontology-patterns.md` (NEW)
- `04-outputs/synthesis-report.md`

---

## Orchestrator Instructions

### Constants

```
PROJECT = "C:/Users/dsber/strategy-nexus/02-projects/02-ontologies-research"
PAPERS = "{PROJECT}/02-resources/papers"
KIT = "{PROJECT}/02-resources/_analysis_kit.md"
GUIDE = "{PROJECT}/02-resources/_extraction_guide.md"
METHODOLOGY = "C:/Users/dsber/strategy-nexus/03-skills/research-pipeline/shared/paper-analyze-core/SKILL.md"
```

---

### Phase 4: Paper Analysis

#### 4.1 Subagent Prompt Template

```
Analyze paper: {paper_id}

Read IN ORDER (absolute paths):
1. C:/Users/dsber/strategy-nexus/02-projects/02-ontologies-research/02-resources/_analysis_kit.md
2. C:/Users/dsber/strategy-nexus/02-projects/02-ontologies-research/02-resources/_extraction_guide.md
3. C:/Users/dsber/strategy-nexus/03-skills/research-pipeline/shared/paper-analyze-core/SKILL.md
4. C:/Users/dsber/strategy-nexus/02-projects/02-ontologies-research/02-resources/papers/{paper_id}/_metadata.json
5. ALL chunks listed in _metadata.json:
   - C:/Users/dsber/strategy-nexus/02-projects/02-ontologies-research/02-resources/papers/{paper_id}/{paper_id}_1.md
   - C:/Users/dsber/strategy-nexus/02-projects/02-ontologies-research/02-resources/papers/{paper_id}/{paper_id}_2.md
   ... (continue for all chunks)

Write to:
1. C:/Users/dsber/strategy-nexus/02-projects/02-ontologies-research/02-resources/papers/{paper_id}/_analysis_log.md
2. C:/Users/dsber/strategy-nexus/02-projects/02-ontologies-research/02-resources/papers/{paper_id}/index.md

CRITICAL:
- Read ALL chunks (validation checks chunks_read == chunks_expected)
- Include chunk:line refs for every extraction (e.g., "Chunk 2:45-52")
- Set analysis_complete: true in index.md frontmatter
- Do NOT read the PDF file
```

#### 4.2 Batch Execution (Based on Subagent Allocation Plan)

**Launch ALL 27 subagents in parallel (max 15 concurrent):**

**Batch 1** (15 subagents - max concurrent):
| Paper ID | Subagent | Chunks | Type |
|----------|----------|--------|------|
| 01-UFO | 1 | 1-4 | standard |
| 02-Knowledge_Graphs | 1 | 1-6 | split-part1 |
| 02-Knowledge_Graphs | 2 | 7-12 | split-part2 |
| 02-Knowledge_Graphs | 3 | 13-15 | split-part3 |
| 03-PROV-AGENT | 1 | 1 | standard |
| 04-PROV-O_to_BFO | 1 | 1-2 | standard |
| 05-DOLCE | 1 | 1-2 | standard |
| 06-BFO_Function | 1 | 1 | standard |
| 07-Classifying_Processes | 1 | 1-2 | standard |
| 09-OCEL_20 | 1 | 1-4 | standard |
| 10-OC-PM | 1 | 1-2 | standard |
| 11-Process_Mining_Event | 1 | 1-3 | standard |
| 12-Foundations_Process | 1 | 1 | standard |
| 14-RAG_Ontologic | 1 | 1-3 | standard |
| 15-SciAgents | 1 | 1-6 | split-part1 |

**Batch 2** (12 subagents):
| Paper ID | Subagent | Chunks | Type |
|----------|----------|--------|------|
| 15-SciAgents | 2 | 7-10 | split-part2 |
| 16-KG-Agent | 1 | 1-2 | standard |
| 17-KG_Reasoning | 1 | 1 | standard |
| 18-Multi-Agent | 1 | 1-4 | standard |
| 19-Graph_of_Thoughts | 1 | 1-6 | split-part1 |
| 19-Graph_of_Thoughts | 2 | 7 | split-part2 |
| 20-Agentic_RAG | 1 | 1-3 | standard |
| 21-LLM_Smart_Contracts | 1 | 1 | standard |
| 22-RPA_Framework | 1 | 1 | standard |
| 23-UFO_Story | 1 | 1 | standard |
| 24-Enterprise_Ontoloty | 1 | 1-5 | standard |
| 31-BBO_BPMN | 1 | 1 | standard |

**After Batch 2**: Spawn 3 merge subagents for split papers:
- Merge 02-Knowledge_Graphs (parts 1-3 → index.md)
- Merge 15-SciAgents (parts 1-2 → index.md)
- Merge 19-Graph_of_Thoughts (parts 1-2 → index.md)

**Total**: 23 papers, 76 chunks, 27 analysis subagents + 3 merge subagents = 30 subagents

---

### Phase 4.5: Validation (AFTER EACH BATCH)

**Run validation on completed papers:**

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

---

### Phase 5: Synthesis

**Only run after Phase 4.5 validation passes for all papers:**

```
Task(
  subagent_type="general-purpose",
  prompt="Synthesize findings across all papers.

Read:
1. {PROJECT}/02-resources/_analysis_kit.md (research question)
2. 03-skills/research-pipeline/skills/paper-synthesize/SKILL.md (methodology)
3. ALL {PROJECT}/02-resources/papers/*/index.md files

Write: {PROJECT}/04-outputs/_synthesis.md

Focus on:
- Entity taxonomy across foundational ontologies
- Framework comparison matrix
- AI agent integration patterns
- Validation of 8-entity hypothesis
- Agentic workflow ontology mapping"
)
```

---

### Concurrency Settings

| Setting | Value |
|---------|-------|
| Max parallel subagents | 15 |
| Timeout per subagent | 5 minutes |
| Retry on failure | 1 attempt |
| Validation | After each batch |

---

## Paper Corpus (Updated from _metadata.json)

| Paper ID | Chunks | Status |
|----------|--------|--------|
| 01-UFO_Unified_Foundational_Ontology | 4 | ready |
| 02-Knowledge_Graphs | 15 | ready |
| 03-PROV-AGENT_Unified_Provenance_for_AI_Agents | 1 | ready |
| 04-PROV-O_to_BFO_Semantic_Mapping | 2 | ready |
| 05-DOLCE_Descriptive_Ontology | 2 | ready |
| 06-BFO_Function_Role_Disposition | 1 | ready |
| 07-Classifying_Processes_Barry_Smith | 2 | ready |
| 09-OCEL_20_Specification | 4 | ready |
| 10-OC-PM_Object-Centric_Process_Mining | 2 | ready |
| 11-Process_Mining_Event_Knowledge_Graphs | 3 | ready |
| 12-Foundations_of_Process_Event_Data | 1 | ready |
| 14-RAG_Ontologic_Graph_Multiagent_LLM | 3 | ready |
| 15-SciAgents_Multi-Agent_Graph_Reasoning | 10 | ready |
| 16-KG-Agent_Knowledge_Graph_Reasoning | 2 | ready |
| 17-KG_Reasoning_Logics_Embeddings_Survey | 1 | ready |
| 18-Multi-Agent_Architecture_Taxonomy_LLM | 4 | ready |
| 19-Graph_of_Thoughts_LLM_Reasoning | 7 | ready |
| 20-Agentic_RAG_Survey | 3 | ready |
| 21-LLM_Smart_Contracts_from_BPMN | 1 | ready |
| 22-RPA_Framework_BPM_Activities | 1 | ready |
| 23-UFO_Story_Ontological_Foundations | 1 | ready |
| 24-Enterprise_Ontoloty | 5 | ready |
| 31-BBO_BPMN_Ontology | 1 | ready |

---

## Subagent Allocation Plan

**Calculated from _metadata.json (Phase 1 Step 12)**
**Token estimation**: Each chunk ≈ 10-15k tokens
**Usable budget**: 74k tokens per subagent

| Paper ID | Chunks | Est. Tokens | Subagents | Splits |
|----------|--------|-------------|-----------|--------|
| 01-UFO_Unified_Foundational_Ontology | 4 | ~47,000 | 1 | 1-4 |
| 02-Knowledge_Graphs | 15 | ~168,000 | 3 | 1-6, 7-12, 13-15 |
| 03-PROV-AGENT_Unified_Provenance_for_AI_Agents | 1 | ~9,000 | 1 | 1 |
| 04-PROV-O_to_BFO_Semantic_Mapping | 2 | ~25,000 | 1 | 1-2 |
| 05-DOLCE_Descriptive_Ontology | 2 | ~21,000 | 1 | 1-2 |
| 06-BFO_Function_Role_Disposition | 1 | ~7,000 | 1 | 1 |
| 07-Classifying_Processes_Barry_Smith | 2 | ~14,000 | 1 | 1-2 |
| 09-OCEL_20_Specification | 4 | ~27,000 | 1 | 1-4 |
| 10-OC-PM_Object-Centric_Process_Mining | 2 | ~18,000 | 1 | 1-2 |
| 11-Process_Mining_Event_Knowledge_Graphs | 3 | ~33,000 | 1 | 1-3 |
| 12-Foundations_of_Process_Event_Data | 1 | ~14,000 | 1 | 1 |
| 14-RAG_Ontologic_Graph_Multiagent_LLM | 3 | ~18,000 | 1 | 1-3 |
| 15-SciAgents_Multi-Agent_Graph_Reasoning | 10 | ~143,000 | 2 | 1-6, 7-10 |
| 16-KG-Agent_Knowledge_Graph_Reasoning | 2 | ~20,000 | 1 | 1-2 |
| 17-KG_Reasoning_Logics_Embeddings_Survey | 1 | ~12,000 | 1 | 1 |
| 18-Multi-Agent_Architecture_Taxonomy_LLM | 4 | ~50,000 | 1 | 1-4 |
| 19-Graph_of_Thoughts_LLM_Reasoning | 7 | ~48,000 | 2 | 1-6, 7 |
| 20-Agentic_RAG_Survey | 3 | ~31,000 | 1 | 1-3 |
| 21-LLM_Smart_Contracts_from_BPMN | 1 | ~12,000 | 1 | 1 |
| 22-RPA_Framework_BPM_Activities | 1 | ~11,000 | 1 | 1 |
| 23-UFO_Story_Ontological_Foundations | 1 | ~15,000 | 1 | 1 |
| 24-Enterprise_Ontoloty | 5 | ~41,000 | 1 | 1-5 |
| 31-BBO_BPMN_Ontology | 1 | ~10,000 | 1 | 1 |

**Total subagents**: 27
**Max concurrent**: 15
**Estimated batches**: 2

### Papers Requiring Split Analysis

| Paper ID | Strategy |
|----------|----------|
| 02-Knowledge_Graphs | 3 subagents: Part 1 (chunks 1-6), Part 2 (chunks 7-12), Part 3 (chunks 13-15) → merge |
| 15-SciAgents | 2 subagents: Part 1 (chunks 1-6), Part 2 (chunks 7-10) → merge |
| 19-Graph_of_Thoughts | 2 subagents: Part 1 (chunks 1-6), Part 2 (chunk 7) → merge |

---

*Ready for execution: run "execute research project 02" to begin analysis*
