# Paper Corpus: Temporal Event Patterns Extraction

**Source**: Existing analyzed papers from ontology research workspace
**Location**: `04-workspace/00-ai-native-org/ontology-research/papers/`

---

## Priority Papers (Core Temporal Content)

| Paper ID | Title | Temporal Relevance | Status |
|----------|-------|-------------------|--------|
| 01-UFO | UFO: Unified Foundational Ontology | UFO-B Perdurants, temporal parts, disposition | ready |
| 03-PROV-AGENT | PROV-AGENT: Unified Provenance for AI Agents | Activity timing, wasStartedBy/wasEndedBy | ready |
| 07-Classifying_Processes | Classifying Processes (Barry Smith) | BFO process theory, Process Profiles | ready |
| 09-OCEL_20 | OCEL 2.0 Specification | Event-Object model, timestamps, dynamic attrs | ready |
| 11-Event_Knowledge_Graphs | Process Mining with Event Knowledge Graphs | DF-paths, correlation, actor behavior | ready |
| 20-Agentic_RAG | Agentic RAG Survey | Workflow patterns, orchestration | ready |

## Secondary Papers (Supporting Content)

| Paper ID | Title | Temporal Relevance | Status |
|----------|-------|-------------------|--------|
| 05-DOLCE | DOLCE Descriptive Ontology | Perdurant theory (alternative view) | ready |
| 10-OC-PM | Object-Centric Process Mining | Lifecycle, flattening, traces | ready |
| 12-Foundations_Event_Data | Foundations of Process Event Data | XES standard, event requirements | ready |
| 18-Multi_Agent_Taxonomy | Multi-Agent Architecture Taxonomy | Task-Management Activity entity | ready |
| 19-Graph_of_Thoughts | Graph of Thoughts LLM Reasoning | Thought transformations (temporal) | ready |

---

## Paper Locations (Full Analysis Files)

All papers have been previously analyzed with index files available:

```
04-workspace/00-ai-native-org/ontology-research/papers/
├── 01-UFO_Unified_Foundational_Ontology.md           # Quick reference
├── 03-PROV-AGENT_Unified_Provenance_for_AI_Agents.md
├── 07-Classifying_Processes_Barry_Smith.md
├── 09-OCEL_20_Specification.md
├── 10-OC-PM_Object-Centric_Process_Mining.md
├── 11-Process_Mining_Event_Knowledge_Graphs.md
├── 12-Foundations_of_Process_Event_Data.md
├── 18-Multi-Agent_Architecture_Taxonomy_LLM.md
├── 19-Graph_of_Thoughts_LLM_Reasoning.md
└── 20-Agentic_RAG_Survey.md

04-workspace/00-ai-native-org/ontology-research/papers-full/
├── 01-UFO_Unified_Foundational_Ontology/             # Full chunks
│   ├── index.md
│   ├── 01-UFO_..._1.md through _4.md
│   └── _analysis_log.md
├── 03-PROV-AGENT_.../
├── 07-Classifying_Processes_.../
├── 09-OCEL_20_.../
...
```

---

## Extraction Strategy

### Phase 1: Priority Papers Deep Dive
Re-read the 6 priority papers with temporal-focused extraction:
1. Read existing index.md for each paper
2. Extract temporal fields not previously captured
3. Create temporal-specific _temporal_extraction.md per paper

### Phase 2: Secondary Papers Scan
Quick scan of 5 secondary papers for additional patterns:
1. Check if temporal content exists in index
2. Only deep-dive if significant new patterns found

### Phase 3: Cross-Paper Synthesis
1. Consolidate all temporal_relations into unified vocabulary
2. Build canonical Event entity model
3. Create lifecycle state machine template
4. Document agent-event participation patterns

---

## Expected Outputs

| Output | Location | Description |
|--------|----------|-------------|
| Temporal extractions per paper | 03-working/{paper_id}_temporal.md | Field-by-field extractions |
| Unified temporal vocabulary | 04-outputs/temporal_vocabulary.yaml | Standardized terms |
| Event entity model | 04-outputs/event_entity_model.md | Canonical Event definition |
| Lifecycle FSM template | 04-outputs/lifecycle_fsm.md | State machine patterns |
| Agent-Event patterns | 04-outputs/agent_event_patterns.md | Participation types |
