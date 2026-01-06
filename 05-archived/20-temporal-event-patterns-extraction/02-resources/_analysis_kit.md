---
project_id: "20-temporal-event-patterns-extraction"
project_path: "02-projects/20-temporal-event-patterns-extraction"
generated: "2026-01-01"
---

# Analysis Kit: Temporal Event Patterns Extraction

## Research Question

**Primary RQ**: What are the temporal and event patterns across foundational ontologies, and how can they inform AI agent workflow design?

**Purpose**: Extract a unified temporal/event model from existing research corpus to:
1. Define canonical Event entity with lifecycle states and temporal operators
2. Identify causation and ordering patterns (before, after, during, triggers)
3. Map how agents participate in events across different frameworks
4. Create a temporal vocabulary for UDWO metamodel event handling

---

## Source Corpus Location

**Quick Reference Indices**:
```
04-workspace/00-ai-native-org/ontology-research/papers/
```

**Full Chunk Files**:
```
04-workspace/00-ai-native-org/ontology-research/papers-full/{paper_id}/
```

---

## Extraction Schema

| Field | Description | Priority | Format |
|-------|-------------|----------|--------|
| event_types | Types of events/perdurants | HIGH | Array of objects |
| event_definitions | Formal definitions with temporal properties | HIGH | Object |
| temporal_relations | Relations between events | HIGH | Array of objects |
| lifecycle_patterns | Event/object lifecycle states and transitions | HIGH | Array of objects |
| state_change_mechanisms | How events cause state changes | HIGH | Array of objects |
| agent_participation | How agents participate in events | HIGH | Array of objects |
| event_correlation | How events correlate to cases/objects/agents | HIGH | Array of objects |
| ordering_mechanisms | How temporal ordering is established | MEDIUM | Array of objects |
| causation_patterns | Causal relationships between events | MEDIUM | Array of objects |
| temporal_standards | Standards for representing time | MEDIUM | Array of objects |
| event_log_formats | Event data formats and schemas | MEDIUM | Array of objects |

---

## Controlled Vocabulary

### Temporal Relations
| Paper Uses | Standardize To |
|------------|----------------|
| "precedes", "before", "prior to" | **before** |
| "follows", "after", "subsequent to" | **after** |
| "overlaps", "concurrent", "simultaneous" | **overlaps** |
| "during", "within", "contained by" | **during** |
| "triggers", "initiates", "starts" | **triggers** |
| "causes", "leads to", "results in" | **causes** |
| "directly-follows", "immediately after" | **directly-follows** |

### Agent Participation Types
| Paper Uses | Standardize To |
|------------|----------------|
| "performs", "executes", "carries out" | **performs** |
| "initiates", "starts", "begins" | **initiates** |
| "observes", "witnesses", "perceives" | **observes** |
| "is affected by", "receives", "undergoes" | **is-affected-by** |
| "wasAssociatedWith" (PROV-O) | **associated-with** |

---

## Validation Contract

Your output will be validated:
- All HIGH priority fields extracted OR marked "N/A - reason"
- Every extraction has chunk:line reference (e.g., "Chunk 2:45-52")
- Controlled vocabulary applied consistently
- Event definitions include temporal properties
- Lifecycle states form valid FSM (no orphan states)

---

## Output Format

Write temporal extractions to:
```
02-projects/20-temporal-event-patterns-extraction/03-working/{paper_id}_temporal.md
```

Use YAML frontmatter + markdown body:
```yaml
---
paper_id: "{paper_id}"
extracted_date: "{date}"
fields_extracted:
  event_types: true|false
  event_definitions: true|false
  temporal_relations: true|false
  # ... etc
---

# Temporal Extraction: {Paper Title}

## event_types
...

## event_definitions
...
```

---

## Paper-Specific Guidance

### UFO (01)
- Focus: UFO-B perdurants, temporal parts, disposition realization
- Key chunks: Look for "perdurant", "temporal", "participation"

### PROV-AGENT (03)
- Focus: Activity timing, wasStartedBy/wasEndedBy, derivation
- Key chunks: W3C PROV extensions, AI agent tracking

### BFO/Barry Smith (07)
- Focus: Process classification, Process Profiles
- Key chunks: Process types, function realization

### OCEL 2.0 (09)
- Focus: Event-Object relationships, timestamps, dynamic attributes
- Key chunks: E2O, O2O, timestamp handling

### Event Knowledge Graphs (11)
- Focus: Directly-follows, correlation, actor behavior
- Key chunks: DF-paths, event nodes

### Agentic RAG (20)
- Focus: Workflow patterns, orchestration timing
- Key chunks: Multi-agent coordination
