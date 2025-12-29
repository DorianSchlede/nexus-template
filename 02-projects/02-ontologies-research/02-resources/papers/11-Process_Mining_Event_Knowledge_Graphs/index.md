---
paper_id: "11-Process_Mining_Event_Knowledge_Graphs"
title: "Process Mining over Multiple Behavioral Dimensions with Event Knowledge Graphs"
authors:
  - "Dirk Fahland"
year: 2022
chunks: 3
chunks_expected: 3
chunks_read: 3
analysis_complete: true
high_priority_fields_found: 6
tokens_estimated: 32826
analyzed_at: "2025-12-28T14:30:00"

entity_types:
  - "Event"
  - "Entity"
  - "Entity Type"
  - "Labeled Property Graph (LPG)"
  - "Event Knowledge Graph"
  - "Class (aggregated event type)"
  - "TaskInstance"

entity_definitions:
  Event: "A record with activity name and timestamp in an event table (Chunk 1:201-206)"
  Entity: "A value in entity type column that events are correlated to (Chunk 1:248-254)"
  Event_Knowledge_Graph: "LPG with node labels Event Entity and relationship labels df corr (Chunk 1:624-628)"
  Class: "Aggregated node for events with same Activity property value (Chunk 2:330-338)"
  TaskInstance: "Subgraph where Actor and Entity df-paths synchronize on consecutive events (Chunk 2:619-627)"

entity_relationships:
  - from: "Event"
    to: "Entity"
    relationship: "corr (correlation)"
    source: "Chunk 1:265-269"
  - from: "Event"
    to: "Event"
    relationship: "df (directly-follows)"
    source: "Chunk 1:519-529"
  - from: "Entity"
    to: "Entity"
    relationship: "related"
    source: "Chunk 1:871-877"

abstraction_level: "domain"

framework_comparison:
  - compared_to: "Classical Event Logs"
    relationship: "extends"
    details: "Replaces single case identifier with multi-entity correlation"
    source: "Chunk 1:119-144"
  - compared_to: "OCEL"
    relationship: "formalizes"
    details: "Event tables with entity types formalize OCEL"
    source: "Chunk 1:234-239"
  - compared_to: "RDF"
    relationship: "differs"
    details: "LPGs support attributed relationships; RDF does not"
    source: "Chunk 1:679-682"

ai_integration: "N/A - paper predates LLM/AI integration discussion (2022)"

agent_modeling:
  - aspect: "Actor as Entity"
    description: "Actors modeled as entity type with own df-paths"
    source: "Chunk 2:595-627"
  - aspect: "Task Instance"
    description: "Work unit where actor and object entity df-paths synchronize"
    source: "Chunk 2:619-627"

agentic_workflows: "N/A - paper focuses on descriptive process mining"

generative_ai_patterns: "N/A - paper predates generative AI patterns"

agent_ontology_integration:
  - mechanism: "Graph-based knowledge representation"
    description: "Event knowledge graphs as LPGs enable ontology-like reasoning"
    source: "Chunk 1:550-603"

entity_count:
  count: 7
  rationale: "Event, Entity, Entity Type, LPG, EKG, Class, TaskInstance"
  source: "Chunk 1:624-628"

methodology: "bottom-up"

empirical_evidence:
  - type: "Process mining datasets"
    description: "BPI Challenge datasets 2014-2019 as event knowledge graphs"
    source: "Chunk 3:112-123"
  - type: "Running example"
    description: "Retail order fulfillment with 7 entity types"
    source: "Chunk 1:37-81"

limitations:
  - "Assumes accurate entity identifiers and timestamps (Chunk 2:54-59)"
  - "Static view of relations; dynamic changes not modeled (Chunk 1:338-342)"
  - "Complex entity interactions may yield complex models (Chunk 3:25-29)"

tools_standards:
  - "Neo4j"
  - "Cypher"
  - "Labeled Property Graphs"
  - "Object-centric Petri nets"
  - "Synchronous proclets"
---

# Process Mining with Event Knowledge Graphs - Analysis Index

## Paper Overview

- **Source**: 11-Process_Mining_Event_Knowledge_Graphs.pdf
- **Chunks**: 3 chunks
- **Author**: Dirk Fahland (TU Eindhoven)
- **Publication**: Process Mining Handbook, LNBIP 448, pp. 274-319, Springer 2022

## Key Extractions

This paper introduces Event Knowledge Graphs as a graph-based data structure for modeling process behavior over multiple entities.

### Entity Types

| Entity | Definition | Source |
|--------|------------|--------|
| Event | Record with activity and timestamp | Chunk 1:201-206 |
| Entity | Value in entity type column | Chunk 1:248-254 |
| Event Knowledge Graph | LPG with Event/Entity nodes | Chunk 1:624-628 |
| Class | Aggregated event type node | Chunk 2:330-338 |
| TaskInstance | Actor-Entity synchronization | Chunk 2:619-627 |

### Entity Relationships

| Relationship | From | To | Source |
|--------------|------|-----|--------|
| corr | Event | Entity | Chunk 1:265-269 |
| df | Event | Event | Chunk 1:519-529 |
| related | Entity | Entity | Chunk 1:871-877 |

### Framework Comparison

- vs Classical Event Logs (Chunk 1:119-144): Replaces single case identifier with multi-entity correlation
- vs OCEL (Chunk 1:234-239): Formalizes object-centric event logs
- vs RDF (Chunk 1:679-682): LPGs support attributed relationships

## Chunk Navigation

### Chunk 1: Foundations
- Event tables, entities, correlation, directly-follows
- Formal definition of event knowledge graphs
- Three-step construction procedure

### Chunk 2: Behavior Analysis
- df-path interpretation and synchronization
- Entity interactions and delays
- Multi-dimensional analysis with actors and queues

### Chunk 3: Process Models
- Synchronous proclets and object-centric Petri nets
- Declarative alternatives (DCR graphs)
- Research challenges and outlook

## Validation

- chunks_read (3) == chunks_expected (3): YES
- analysis_complete: true
- HIGH priority fields found: 6
