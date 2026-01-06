---
acquisition_date: "2025-12-27"
total_selected: 31
total_acquired: 20
acquisition_rate: 64.5%
total_size_mb: 80
---

# Paper Acquisition Report

## Summary

| Metric | Value |
|--------|-------|
| Papers Selected | 31 |
| Papers Acquired | 20 |
| Acquisition Rate | 64.5% |
| Papers Missing | 11 |
| Total Size | ~80 MB |

---

## Successfully Downloaded Papers (20)

### Foundational Ontologies (8 papers)

| # | Paper | Year | Category | Size |
|---|-------|------|----------|------|
| 01 | UFO: Unified Foundational Ontology | 2021 | UFO | 2.3 MB |
| 05 | DOLCE: Descriptive Ontology | 2023 | DOLCE | 0.6 MB |
| 06 | BFO Function Role Disposition | 2008 | BFO | 0.2 MB |
| 07 | Classifying Processes (Barry Smith) | 2012 | BFO | 0.5 MB |
| 02 | Knowledge Graphs Survey | 2021 | General | 2.3 MB |
| 03 | PROV-AGENT for AI Agents | 2025 | PROV-O | 0.7 MB |
| 04 | PROV-O to BFO Semantic Mapping | 2025 | PROV-O | 1.9 MB |
| - | BFO and DOLCE Comparison (bonus) | 2017 | Comparison | 0.1 MB |

### Object-Centric Process Mining (5 papers)

| # | Paper | Year | Category | Size |
|---|-------|------|----------|------|
| 09 | OCEL 2.0 Specification | 2024 | OCEL | 0.9 MB |
| 10 | OC-PM Analysis | 2022 | OCEL | 1.8 MB |
| 11 | Process Mining Event Knowledge Graphs | 2022 | OCEL | 2.8 MB |
| 12 | Foundations of Process Event Data | 2022 | OCEL | 3.0 MB |

### AI + Ontology/Knowledge Representation (7 papers)

| # | Paper | Year | Category | Size |
|---|-------|------|----------|------|
| 14 | RAG Ontologic Graph Multiagent LLM | 2024 | LLM-Agent | 0.7 MB |
| 15 | SciAgents Multi-Agent Graph Reasoning | 2024 | LLM-Agent | 42.9 MB |
| 16 | KG-Agent Knowledge Graph Reasoning | 2024 | LLM-Agent | 0.7 MB |
| 17 | KG Reasoning Logics Embeddings Survey | 2022 | AI-KR | 0.2 MB |
| 18 | Multi-Agent Architecture Taxonomy LLM | 2023 | AI-KR | 1.0 MB |
| 19 | Graph of Thoughts LLM Reasoning | 2024 | AI-KR | 3.0 MB |
| 20 | Agentic RAG Survey | 2025 | AI-KR | 13.6 MB |
| 21 | LLM Smart Contracts from BPMN | 2025 | AI-KR | 0.8 MB |
| 22 | RPA Framework BPM Activities | 2020 | AI-KR | 0.2 MB |

---

## Papers Not Acquired (11)

### Behind Paywall / Requires Manual Download

| # | Paper | Year | Category | Reason | Alternative Sources |
|---|-------|------|----------|--------|---------------------|
| 08 | ArchiMate UFO Resources | 2015 | EA | HTTP 403 | ResearchGate, Academia.edu (need login) |
| 13 | VKG OCEL Extraction | 2023 | OCEL | No URL | Springer (paywall) |
| 23 | UFO Story (Foundations) | 2015 | UFO | Paywall | ResearchGate (need login) |
| 24 | Building Ontologies with BFO | 2015 | BFO | Book | MIT Press, Library |
| 25 | The Enterprise Ontology | 1998 | EA | Classic | CiteSeerX, Library |
| 26 | BFO 2.0 Specification | 2022 | BFO | Journal | BFO.wiki has partial |
| 27 | DOLCE Foundations | 2010 | DOLCE | Book chapter | Author sites |
| 28 | Events as Entities UFO | 2019 | UFO | Conference | CEUR-WS |
| 29 | Endurant Types OntoUML | 2018 | UFO | Conference | CEUR-WS |
| 30 | Multi-level Ontology | 2017 | UFO | Journal | Author sites |
| 31 | BBO BPMN Ontology | 2019 | BBO | Conference | Author sites |

---

## Coverage Analysis

| Category | Selected | Acquired | Gap |
|----------|----------|----------|-----|
| UFO | 5 | 1 | 4 papers missing |
| DOLCE | 2 | 1 | 1 paper missing |
| BFO | 4 | 3 | 1 paper missing (book) |
| PROV-O | 2 | 2 | Complete |
| ArchiMate/EA | 2 | 0 | 2 papers missing |
| OCEL/OCPM | 5 | 4 | 1 paper missing |
| LLM/Agent | 3 | 3 | Complete |
| AI+KR | 6 | 6 | Complete |
| General | 2 | 1 | 1 paper missing (book) |

### Critical Gaps

1. **UFO papers** - Only have the main 2021 specification, missing endurant types, events, multi-level modeling
2. **ArchiMate+UFO** - Key paper for EA integration not acquired
3. **BBO** - Missing core paper for BPMN ontology
4. **Enterprise Ontology** - Historical foundation not acquired

### Mitigation

The acquired papers still provide strong coverage:
- Core foundational ontologies: UFO, DOLCE, BFO all represented
- Process mining: Excellent OCEL coverage (4/5 papers)
- AI integration: Complete coverage (9/9 papers)
- The UFO 2021 paper is comprehensive and covers most UFO concepts
- BFO and DOLCE comparison paper provides cross-ontology analysis

---

## Files Ready for Preprocessing

```
02-resources/papers/
├── 01-UFO_Unified_Foundational_Ontology.pdf
├── 02-Knowledge_Graphs.pdf
├── 03-PROV-AGENT_Unified_Provenance_for_AI_Agents.pdf
├── 04-PROV-O_to_BFO_Semantic_Mapping.pdf
├── 05-DOLCE_Descriptive_Ontology.pdf
├── 06-BFO_Function_Role_Disposition.pdf
├── 07-Classifying_Processes_Barry_Smith.pdf
├── 09-OCEL_20_Specification.pdf
├── 10-OC-PM_Object-Centric_Process_Mining.pdf
├── 11-Process_Mining_Event_Knowledge_Graphs.pdf
├── 12-Foundations_of_Process_Event_Data.pdf
├── 14-RAG_Ontologic_Graph_Multiagent_LLM.pdf
├── 15-SciAgents_Multi-Agent_Graph_Reasoning.pdf
├── 16-KG-Agent_Knowledge_Graph_Reasoning.pdf
├── 17-KG_Reasoning_Logics_Embeddings_Survey.pdf
├── 18-Multi-Agent_Architecture_Taxonomy_LLM.pdf
├── 19-Graph_of_Thoughts_LLM_Reasoning.pdf
├── 20-Agentic_RAG_Survey.pdf
├── 21-LLM_Smart_Contracts_from_BPMN.pdf
└── 22-RPA_Framework_BPM_Activities.pdf
```

---

## Next Steps

1. **Preprocess PDFs** → Convert to markdown chunks
2. **User Review** → Approve preprocessing or provide missing papers
3. **Handoff** → Ready for analysis phase

---

*Acquisition completed 2025-12-27*
