# Temporal Event Patterns Extraction - Execution Steps

**Last Updated**: 2026-01-01

**IMPORTANT**: This file tracks project progress. Mark tasks complete with [x] as you finish them.

---

## Phase 1: Setup & Planning

- [x] Create project structure (Project 20)
- [x] Define research question in `_briefing.md`
- [x] Create extraction schema (11 temporal fields)
- [x] Create `_extraction_guide.md` with field definitions
- [x] Link existing paper corpus from workspace
- [x] Update `plan.md` with orchestrator instructions
- [x] Create `_analysis_kit.md` for subagent context

---

## Phase 2: Priority Paper Extraction

Extract temporal patterns from 6 priority papers:

- [x] 01-UFO: UFO-B Perdurants, temporal parts, disposition
- [x] 03-PROV-AGENT: Activity timing, wasStartedBy/wasEndedBy
- [x] 07-Classifying_Processes: BFO process theory, Process Profiles
- [x] 09-OCEL_20: Event-Object model, timestamps, dynamic attrs
- [x] 11-Event_Knowledge_Graphs: DF-paths, correlation, actor behavior
- [x] 20-Agentic_RAG: Workflow patterns, orchestration timing

**Output per paper**: `03-working/{paper_id}_temporal.md`

---

## Phase 3: Secondary Paper Scan

Quick scan of 5 secondary papers for additional patterns:

- [x] 05-DOLCE: Perdurant theory
- [x] 10-OC-PM: Lifecycle, flattening, traces
- [x] 12-Foundations_Event_Data: XES standard, event requirements
- [x] 18-Multi_Agent_Taxonomy: Task-Management Activity
- [x] 19-Graph_of_Thoughts: Thought transformations (temporal)

---

## Phase 4: Synthesis & Outputs

- [x] Consolidate temporal_relations vocabulary
- [x] Build canonical Event entity model
- [x] Create lifecycle FSM template
- [x] Document agent-event participation patterns
- [x] Write synthesis report

**Outputs**:
- `04-outputs/temporal_vocabulary.yaml` ✓
- `04-outputs/event_entity_model.md` ✓
- `04-outputs/lifecycle_fsm.md` ✓
- `04-outputs/agent_event_patterns.md` ✓
- `04-outputs/temporal_synthesis.md` ✓

---

## Phase 5: Validation & Closure

- [x] Validate vocabulary covers all extracted relations
- [x] Cross-check Event model against source definitions
- [x] Update Project 20 overview with findings
- [x] Mark project COMPLETE

---

## Notes

**Source Corpus**:
- Papers already analyzed in `04-workspace/00-ai-native-org/ontology-research/`
- No download needed - reuse existing chunks

**Key Files**:
- `02-resources/_briefing.md` - Research question
- `02-resources/_extraction_guide.md` - Field definitions
- `02-resources/_paper_corpus.md` - Paper links
- `01-planning/plan.md` - Orchestrator instructions

---

*Mark tasks complete with [x] as you finish them*
