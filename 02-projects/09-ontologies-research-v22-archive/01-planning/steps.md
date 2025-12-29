# Ontologies Research - Migration Test Steps

**Last Updated**: 2025-12-28
**Schema Version**: v2.2 → v2.3 (Migration Test)
**Purpose**: Test Schema v2.3 migration before applying to Project 02

**IMPORTANT**: This file tracks migration test progress. Mark tasks complete with [x] as you finish them.

---

## Phase 1: Planning & Definition ✅ COMPLETE (ORIGINAL)

> Original work from Project 02 - preserved for reference

- [x] Create project structure
- [x] Define research question and extraction schema
- [x] Search academic databases (46 papers found)
- [x] Filter AI papers to ontology/knowledge representation focus only
- [x] Review abstracts and assess relevance
- [x] User approves paper selection (31 papers selected)

---

## Phase 2: Paper Acquisition ✅ COMPLETE (ORIGINAL)

> Original work from Project 02 - preserved for reference

- [x] Download papers (20 acquired automatically)
- [x] User adds missing papers (books + critical papers)
- [x] Preprocess PDFs to markdown chunks (23 PDFs → 76 chunks)
- [x] Verify acquisition completeness

---

## Phase 3: Analysis (Schema v2.2) 🗑️ RESET

> v2.2 analysis outputs DELETED to create clean test environment

- [x] ~~Analyze all 23 papers with Schema v2.2~~ (outputs deleted)
- [x] ~~All index.md files validated~~ (outputs deleted)

---

## Phase 3b: Schema v2.3 Migration Test 🔄 IN PROGRESS

**Purpose**: Test Schema v2.3 migration on this project before applying to production.

### 3b.1 Update Project Files ✅ COMPLETE

- [x] Update `_briefing.md` with `research_purpose` (G22a) - already present from copy
- [x] Update `_analysis_kit.md` with `synthesis_goals` (G22b) - already present from copy
- [x] Update `_analysis_kit.md` with Schema v2.3 chunk_index requirements
- [x] Update project_id references to point to Project 09

### 3b.2 Test Re-analysis (3 papers minimum) ⏳ PENDING

**Test Papers** (selected for variety - small, medium, large):
| # | Paper ID | Chunks | Status |
|---|----------|--------|--------|
| 01 | 03-PROV-AGENT_Unified_Provenance_for_AI_Agents | 1 | [ ] |
| 02 | 09-OCEL_20_Specification | 4 | [ ] |
| 03 | 15-SciAgents_Multi-Agent_Graph_Reasoning | 10 | [ ] |

### 3b.3 Validate Test Results ⏳ PENDING

- [ ] Run `validate_analysis.py --check-chunk-index` on test papers
- [ ] Check: Test papers have `chunk_index` in frontmatter
- [ ] Check: Test papers have 3-state `fields_found` (true/partial/false)
- [ ] Check: Structured N/A format used where applicable (G18)

---

## Phase 3c: Full Migration (Optional) ⏳ PENDING

> Only proceed if Phase 3b passes validation

### Full Paper List (23 total)

| # | Paper ID | Status |
|---|----------|--------|
| 01 | 01-UFO_Unified_Foundational_Ontology | [ ] |
| 02 | 02-Knowledge_Graphs | [ ] |
| 03 | 03-PROV-AGENT_Unified_Provenance_for_AI_Agents | [ ] |
| 04 | 04-PROV-O_to_BFO_Semantic_Mapping | [ ] |
| 05 | 05-DOLCE_Descriptive_Ontology | [ ] |
| 06 | 06-BFO_Function_Role_Disposition | [ ] |
| 07 | 07-Classifying_Processes_Barry_Smith | [ ] |
| 08 | 09-OCEL_20_Specification | [ ] |
| 09 | 10-OC-PM_Object-Centric_Process_Mining | [ ] |
| 10 | 11-Process_Mining_Event_Knowledge_Graphs | [ ] |
| 11 | 12-Foundations_of_Process_Event_Data | [ ] |
| 12 | 14-RAG_Ontologic_Graph_Multiagent_LLM | [ ] |
| 13 | 15-SciAgents_Multi-Agent_Graph_Reasoning | [ ] |
| 14 | 16-KG-Agent_Knowledge_Graph_Reasoning | [ ] |
| 15 | 17-KG_Reasoning_Logics_Embeddings_Survey | [ ] |
| 16 | 18-Multi-Agent_Architecture_Taxonomy_LLM | [ ] |
| 17 | 19-Graph_of_Thoughts_LLM_Reasoning | [ ] |
| 18 | 20-Agentic_RAG_Survey | [ ] |
| 19 | 21-LLM_Smart_Contracts_from_BPMN | [ ] |
| 20 | 22-RPA_Framework_BPM_Activities | [ ] |
| 21 | 23-UFO_Story_Ontological_Foundations | [ ] |
| 22 | 24-Enterprise_Ontoloty | [ ] |
| 23 | 31-BBO_BPMN_Ontology | [ ] |

---

## Phase 4: Synthesis ⏳ PENDING

> Only proceed if Phase 3b or 3c passes validation

- [ ] Run `build_synthesis_routing.py` (L1)
- [ ] Run `calculate_subagent_allocation.py` (L2)
- [ ] Run `generate_subagent_prompts.py` (L3)
- [ ] Execute synthesis subagents (L4)
- [ ] Verify outputs (L5)
- [ ] Aggregate patterns (L6)
- [ ] Generate final report (L7)

---

## Current Status Summary

**Migration Test Ready (CLEAN STATE)**:
- 23 papers with PDFs + 76 markdown chunks
- All v2.2 analysis outputs DELETED (index.md, _analysis_log.md removed)
- Project files updated with G22a/G22b ✅
- Schema v2.3 requirements documented in _analysis_kit.md ✅

**Next Action**: Run test analysis on 3 papers (small/medium/large)

---

## Key Files

- `02-resources/_briefing.md` - Research question (needs research_purpose)
- `02-resources/_analysis_kit.md` - Extraction schema (needs synthesis_goals)
- `02-resources/papers/` - 23 PDFs + 76 markdown chunks (clean - no index.md)
- `01-planning/plan.md` - Full research plan with orchestrator instructions

---

*Mark tasks complete with [x] as you finish them*
