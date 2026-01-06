# Temporal Event Patterns Extraction - Plan

**Last Updated**: 2026-01-01

---

## Research Question

**Primary RQ**: What are the temporal and event patterns across foundational ontologies, and how can they inform AI agent workflow design?

**Focus Areas**:
- Event as ontological category (UFO-B, BFO, DOLCE)
- Event-Object relationships (OCEL E2O, O2O)
- Agent-Activity-Entity temporal binding
- Process vs Event distinction
- Lifecycle state machines
- Causation and temporal ordering

---

## Approach

**Strategy**: Re-analyze existing ontology research corpus with temporal-focused extraction lens.

Unlike typical research projects that download new papers, this project:
1. Uses **existing analyzed papers** from `04-workspace/00-ai-native-org/ontology-research/`
2. Applies **new extraction schema** focused on temporal/event patterns
3. Synthesizes cross-paper **temporal vocabulary and patterns**

---

## Extraction Schema

| Field | Description | Priority |
|-------|-------------|----------|
| event_types | Types of events/perdurants (atomic, composite, process) | high |
| event_definitions | Formal definitions with temporal properties | high |
| temporal_relations | Relations between events (before, after, triggers) | high |
| lifecycle_patterns | Event/object lifecycle states and transitions | high |
| state_change_mechanisms | How events cause state changes | high |
| agent_participation | How agents participate in events | high |
| event_correlation | How events correlate to cases/objects/agents | high |
| ordering_mechanisms | How temporal ordering is established | medium |
| causation_patterns | Causal relationships between events | medium |
| temporal_standards | Standards for representing time | medium |
| event_log_formats | Event data formats and schemas | medium |

---

## Current State

| Metric | Value |
|--------|-------|
| Phase | 1-Planning (complete) |
| Papers in Corpus | 11 |
| Priority Papers | 6 |
| Secondary Papers | 5 |
| Papers with Full Chunks | 11 (all from prior project) |
| Papers Analyzed | 0 |

---

## Paper Corpus

### Priority Papers (Core Temporal Content)

| Paper ID | Temporal Relevance | Chunks | Status |
|----------|-------------------|--------|--------|
| 01-UFO | UFO-B Perdurants, temporal parts | 4 | ready |
| 03-PROV-AGENT | Activity timing, wasStartedBy/wasEndedBy | 1 | ready |
| 07-Classifying_Processes | BFO process theory, Process Profiles | 2 | ready |
| 09-OCEL_20 | Event-Object model, timestamps | 4 | ready |
| 11-Event_Knowledge_Graphs | DF-paths, correlation, actor behavior | 3 | ready |
| 20-Agentic_RAG | Workflow patterns, orchestration | 1 | ready |

### Secondary Papers

| Paper ID | Temporal Relevance | Chunks | Status |
|----------|-------------------|--------|--------|
| 05-DOLCE | Perdurant theory | 2 | ready |
| 10-OC-PM | Lifecycle, flattening | 2 | ready |
| 12-Foundations_Event_Data | XES standard | 1 | ready |
| 18-Multi_Agent_Taxonomy | Task-Management Activity | 1 | ready |
| 19-Graph_of_Thoughts | Thought transformations | 1 | ready |

---

## Key Decisions

1. **Use existing corpus**: Papers already downloaded and chunked from Project 16
2. **New extraction schema**: Temporal-specific fields not previously extracted
3. **Cross-reference indices**: Read existing index.md files first, then chunks for new fields
4. **Output as vocabulary**: Synthesize into reusable temporal vocabulary for UDWO

---

## Dependencies & Links

**Source Corpus**:
- `04-workspace/00-ai-native-org/ontology-research/papers/` - Quick reference indices
- `04-workspace/00-ai-native-org/ontology-research/papers-full/` - Full chunk files

**Project Files**:
- `02-resources/_briefing.md` - Research question and schema
- `02-resources/_extraction_guide.md` - Field-by-field extraction guidance
- `02-resources/_paper_corpus.md` - Paper inventory and links

**Related Projects**:
- Project 16: Ontologies Research V3 - Source of analyzed papers
- Project 02: Ontologies Research - Original corpus

---

## Orchestrator Instructions

### Constants

```
PROJECT = "02-projects/20-temporal-event-patterns-extraction"
PAPERS_QUICK = "04-workspace/00-ai-native-org/ontology-research/papers/"
PAPERS_FULL = "04-workspace/00-ai-native-org/ontology-research/papers-full/"
BRIEFING = "{PROJECT}/02-resources/_briefing.md"
GUIDE = "{PROJECT}/02-resources/_extraction_guide.md"
```

### Phase 1: Read Existing Indices

For each priority paper:
1. Read `{PAPERS_QUICK}/{paper_id}.md` (quick reference)
2. Check if temporal fields already extracted
3. If NOT extracted or incomplete → proceed to Phase 2

### Phase 2: Deep Temporal Extraction

For papers needing extraction:
1. Read chunks from `{PAPERS_FULL}/{paper_id}/`
2. Extract fields per `_extraction_guide.md`
3. Write to `{PROJECT}/03-working/{paper_id}_temporal.md`

### Subagent Prompt Template

```
You are analyzing paper {paper_id} for TEMPORAL/EVENT patterns.

READ FIRST:
- {PROJECT}/02-resources/_extraction_guide.md (field definitions)
- {PAPERS_FULL}/{paper_id}/index.md (existing analysis)

THEN READ chunks:
- {PAPERS_FULL}/{paper_id}/{paper_id}_1.md through _N.md

EXTRACT these fields (see _extraction_guide.md for format):
- event_types
- event_definitions
- temporal_relations
- lifecycle_patterns
- state_change_mechanisms
- agent_participation
- event_correlation
- ordering_mechanisms (if present)
- causation_patterns (if present)
- temporal_standards (if present)
- event_log_formats (if present)

OUTPUT to: {PROJECT}/03-working/{paper_id}_temporal.md
```

### Phase 3: Synthesis

After all papers analyzed:
1. Consolidate temporal_relations into unified vocabulary
2. Build canonical Event entity model
3. Create lifecycle FSM template
4. Document agent-event participation patterns

---

## Expected Outputs

| Output | Location | Description |
|--------|----------|-------------|
| Per-paper extractions | 03-working/{paper_id}_temporal.md | Temporal field extractions |
| Temporal vocabulary | 04-outputs/temporal_vocabulary.yaml | Standardized relation types |
| Event entity model | 04-outputs/event_entity_model.md | Canonical Event definition |
| Lifecycle FSM | 04-outputs/lifecycle_fsm.md | State machine template |
| Agent-Event patterns | 04-outputs/agent_event_patterns.md | Participation types |
| Synthesis report | 04-outputs/temporal_synthesis.md | Cross-paper analysis |

---

## Open Questions

- [x] Use existing corpus or download new? → Use existing
- [ ] How to handle papers with minimal temporal content?
- [ ] Should lifecycle patterns include error/exception states?

---

*Next: Execute extraction with analyze-research-project skill*
