# Inductive Corpus Analysis - Execution Steps

**Last Updated**: 2026-01-01

---

## Phase 1: Setup

- [x] Create project structure
- [ ] Define unprimed extraction prompts
- [ ] List all source papers with chunk counts

---

## Phase 2: Raw Entity Extraction

For each paper, extract:
- What entities/concepts does the author explicitly define?
- What terms do they introduce or emphasize?
- Use their exact terminology

Papers to process:
- [ ] 01-UFO
- [ ] 02-Knowledge_Graphs
- [ ] 03-PROV-AGENT
- [ ] 04-PROV-O_to_BFO
- [ ] 05-DOLCE
- [ ] 06-BFO
- [ ] 07-Classifying_Processes
- [ ] 09-OCEL_20
- [ ] 10-OC-PM
- [ ] 11-Event_KG
- [ ] 12-Foundations
- [ ] 14-RAG_Ontologic
- [ ] 15-SciAgents
- [ ] 16-KG-Agent
- [ ] 17-KG_Reasoning
- [ ] 18-Multi-Agent_Taxonomy
- [ ] 19-Graph_of_Thoughts
- [ ] 20-Agentic_RAG
- [ ] 21-LLM_Smart_Contracts
- [ ] 22-RPA_Framework
- [ ] 23-UFO_Story
- [ ] 24-Enterprise_Ontology
- [ ] 31-BBO

**Output**: `03-working/{paper_id}_raw_entities.md`

---

## Phase 3: Raw Relationship Extraction

For each paper, extract:
- What relationships between concepts does the author describe?
- What verbs connect entities?
- What dependencies are stated?

**Output**: `03-working/{paper_id}_raw_relationships.md`

---

## Phase 4: Pattern Emergence

- [ ] Aggregate all raw entities
- [ ] Count frequency of terms
- [ ] Cluster similar concepts
- [ ] Note contradictions between papers

**Output**: `04-outputs/emergent_entities.yaml`

---

## Phase 5: Relationship Emergence

- [ ] Aggregate all raw relationships
- [ ] Identify common relationship types
- [ ] Map connection patterns

**Output**: `04-outputs/emergent_relationships.yaml`

---

## Phase 6: Domain-Specific Patterns

- [ ] Workflow/coordination patterns (from AI agent papers)
- [ ] Tool/capability categories (from KG-Agent, Multi-Agent)
- [ ] Process patterns (from OCEL, Event KG)
- [ ] Reasoning patterns (from GoT, KG Reasoning)

**Outputs**:
- `04-outputs/emergent_workflows.yaml`
- `04-outputs/emergent_tools.yaml`

---

## Phase 7: Gaps & Limitations

- [ ] Extract problems authors explicitly state
- [ ] Note what papers say they cannot capture
- [ ] Identify contradictions between sources

**Output**: `04-outputs/emergent_gaps.yaml`

---

## Phase 8: Synthesis

- [ ] Write inductive synthesis report
- [ ] No theoretical framing - just what data shows
- [ ] Include frequency analysis
- [ ] Note surprises vs. prior assumptions

**Output**: `04-outputs/inductive_synthesis.md`

---

*Mark tasks complete with [x] as you finish them*
