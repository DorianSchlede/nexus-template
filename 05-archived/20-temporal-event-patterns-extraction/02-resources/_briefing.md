---
research_question: "What are the temporal and event patterns across foundational ontologies, and how can they inform AI agent workflow design?"

research_purpose: |
  Extract a unified temporal/event model from existing research corpus to:
  1. Define canonical Event entity with lifecycle states and temporal operators
  2. Identify causation and ordering patterns (before, after, during, triggers)
  3. Map how agents participate in events across different frameworks
  4. Create a temporal vocabulary for UDWO metamodel event handling

domain: "Ontology + Process Mining + AI Agents"

# Papers to analyze (existing workspace - NO DOWNLOAD NEEDED)
source_corpus:
  location: "04-workspace/00-ai-native-org/ontology-research/papers/"
  priority_papers:
    - "01-UFO_Unified_Foundational_Ontology.md"      # UFO-B Perdurants
    - "03-PROV-AGENT_Unified_Provenance_for_AI_Agents.md"  # Activity timing
    - "07-Classifying_Processes_Barry_Smith.md"      # BFO Process theory
    - "09-OCEL_20_Specification.md"                  # Event-Object model
    - "11-Process_Mining_Event_Knowledge_Graphs.md"  # Event KG patterns
    - "20-Agentic_RAG_Survey.md"                     # Agent workflow patterns
  secondary_papers:
    - "05-DOLCE_Descriptive_Ontology.md"             # Perdurant theory
    - "10-OC-PM_Object-Centric_Process_Mining.md"    # Lifecycle patterns
    - "12-Foundations_of_Process_Event_Data.md"      # Event log structure
    - "18-Multi-Agent_Architecture_Taxonomy_LLM.md"  # Task-Management Activity
    - "19-Graph_of_Thoughts_LLM_Reasoning.md"        # Thought transformation timing

extraction_schema:
  # TEMPORAL ENTITY TYPES
  - field: event_types
    description: "Types of events/perdurants defined (atomic, composite, process, state change)"
    priority: high

  - field: event_definitions
    description: "Formal definitions of events with temporal properties (start, end, duration)"
    priority: high

  - field: temporal_relations
    description: "Relations between events (before, after, during, overlaps, triggers, causes)"
    priority: high

  # LIFECYCLE & STATE
  - field: lifecycle_patterns
    description: "Event/object lifecycle states and valid transitions (created→active→completed)"
    priority: high

  - field: state_change_mechanisms
    description: "How events cause state changes in objects/agents"
    priority: high

  # AGENT-EVENT INTERACTION
  - field: agent_participation
    description: "How agents participate in events (initiates, performs, observes, is-affected-by)"
    priority: high

  - field: event_correlation
    description: "How events are correlated to cases, objects, agents (E2O, correlation patterns)"
    priority: high

  # ORDERING & CAUSATION
  - field: ordering_mechanisms
    description: "How temporal ordering is established (timestamps, sequence, directly-follows)"
    priority: medium

  - field: causation_patterns
    description: "Causal relationships between events (triggers, enables, prevents)"
    priority: medium

  # STANDARDS & IMPLEMENTATION
  - field: temporal_standards
    description: "Standards for representing time (ISO 8601, Allen's interval algebra, XES lifecycle)"
    priority: medium

  - field: event_log_formats
    description: "Event data formats and schemas (XES, OCEL, JSON, RDF)"
    priority: medium

focus_areas:
  - "Event as ontological category (UFO-B, BFO, DOLCE)"
  - "Event-Object relationships (OCEL E2O, O2O)"
  - "Agent-Activity-Entity temporal binding"
  - "Process vs Event distinction"
  - "Lifecycle state machines"
  - "Causation and temporal ordering"

skip_sections:
  - "Acknowledgments"
  - "Author Contributions"
  - "Funding"
  - "References" # (unless citing temporal standards)
---

# Temporal Event Patterns Extraction

## Research Context

This research project extracts temporal/event patterns from your existing ontology research corpus. Unlike typical research projects that download papers, this one **references papers already analyzed** in:

```
04-workspace/00-ai-native-org/ontology-research/papers/
```

## Key Research Questions

1. **Event Ontology**: How do UFO-B, BFO, and DOLCE define events/perdurants?
2. **Event-Object Relations**: How does OCEL 2.0 model Event-to-Object relationships?
3. **Agent Participation**: How do agents participate in events across frameworks?
4. **Temporal Ordering**: What ordering mechanisms exist (directly-follows, causation)?
5. **Lifecycle States**: What state machines govern entity lifecycles?

## Expected Outputs

1. **Canonical Event Entity Model**: Unified definition with properties
2. **Temporal Relation Vocabulary**: Standardized relation types
3. **Lifecycle State Machine Template**: Generic FSM for entities
4. **Agent-Event Participation Patterns**: How agents bind to events
