---
paper_id: "10-OC-PM_Object-Centric_Process_Mining"
title: "OC-PM: analyzing object-centric event logs and process models"
authors:
  - "Alessandro Berti"
  - "Wil M. P. van der Aalst"
year: 2022
chunks_expected: 2
chunks_read: 2
analysis_complete: true
high_priority_fields_found: 5

# HIGH PRIORITY FIELDS
entity_types:
  - "Event"
  - "Object"
  - "Activity"
  - "Object Type"
  - "Case"
  - "Attribute"
  - "Timestamp"

entity_definitions:
  Event: "A recorded occurrence in a process, associated with an activity, timestamp, and set of related objects (Chunk 1:236-251)"
  Object: "An identifier with a specific type that participates in events; objects have lifecycles and attributes (Chunk 1:448-475)"
  Activity: "A labeled action type from the universe of activities Uact (Chunk 1:226-228)"
  Object_Type: "A classification for objects from the universe Uot, e.g., order, item, package (Chunk 1:440-441)"
  Lifecycle: "The sequence of events to which an object is related, defining start and end activities (Chunk 1:605-621)"
  Traditional_Event_Log: "Tuple TL = (E, piact, pitime, picase, <=) with events, activities, timestamps, cases, and ordering (Chunk 1:236-251)"
  Object_Centric_Event_Log: "Tuple L = (E, AN, AV, AT, OT, O, pityp, piact, pitime, pivmap, piomap, piotyp, piovmap, <=) (Chunk 1:448-527)"

entity_relationships:
  - from: "Event"
    to: "Object"
    relationship: "piomap - many-to-many mapping"
    source: "Chunk 1:502-505"
  - from: "Object"
    to: "Object Type"
    relationship: "piotyp - exactly one type per object"
    source: "Chunk 1:510-512"
  - from: "Event"
    to: "Activity"
    relationship: "piact - each event has one activity"
    source: "Chunk 1:481-483"
  - from: "Event"
    to: "Timestamp"
    relationship: "pitime - temporal ordering"
    source: "Chunk 1:485-488"
  - from: "Activity"
    to: "Activity"
    relationship: "directly-follows in DFG"
    source: "Chunk 1:303-308"

abstraction_level: "domain"

framework_comparison:
  - compared_to: "XES"
    relationship: "extends"
    details: "OCEL resolves convergence/divergence problems in XES by allowing events to relate to multiple objects without replication"
    source: "Chunk 1:69-78"
  - compared_to: "Artifact-Centric Process Mining"
    relationship: "related_to"
    details: "Similar focus on business artifacts but OCEL provides standardized format and avoids relational database dependency"
    source: "Chunk 2:315-352"
  - compared_to: "Colored Petri Nets"
    relationship: "builds_on"
    details: "Object-centric Petri nets support subset of colored Petri net semantics with simpler discovery"
    source: "Chunk 2:376-450"
  - compared_to: "Traditional DFG"
    relationship: "extends"
    details: "OC-DFG is a multigraph with typed edges for each object type, discovered via flattening"
    source: "Chunk 1:758-801"

ai_integration: "N/A - paper predates LLM/AI integration discussion (published 2022, focused on process mining foundations)"

agent_modeling:
  - aspect: "Object Lifecycle"
    description: "Objects have complete lifecycles with start/end activities, but no autonomous agent behavior modeled"
    source: "Chunk 1:605-627"

agentic_workflows: "N/A - paper focuses on process mining analysis, not agent orchestration"

generative_ai_patterns: "N/A - no discussion of LLM patterns"

agent_ontology_integration: "N/A - no AI agent integration discussed"

# MEDIUM PRIORITY FIELDS
entity_count:
  count: 7
  rationale: "Core entities: Event, Object, Activity, Object Type, Case, Attribute, Timestamp - designed for process mining"
  source: "Chunk 1:215-527"

methodology: "bottom-up"

empirical_evidence:
  - type: "ERP System Application"
    description: "Designed for analyzing event data from mainstream information systems such as SAP ERP"
    source: "Chunk 1:23-31"
  - type: "Sales Order Example"
    description: "Detailed example with order, item, package, delivery objects in sales order management"
    source: "Chunk 1:50-51, 85-86, 166-182"
  - type: "Tool Validation"
    description: "OC-PM web tool and ProM plugin implementation with sample event logs"
    source: "Chunk 2:162-306"

limitations:
  - "No real-life event log assessment in current paper (Chunk 2:504-507)"
  - "Discipline still in early development stage (Chunk 1:111)"
  - "Graph database scalability for process mining needs investigation (Chunk 2:413-416)"
  - "Does not model autonomous agent behavior or AI integration"

tools_standards:
  - "OCEL (Object-Centric Event Log format)"
  - "JSON-OCEL"
  - "XML-OCEL"
  - "MongoDB"
  - "ProM 6.x"
  - "XES"
  - "OC-DFG (Object-Centric Directly-Follows Multigraph)"
  - "Object-Centric Petri Nets"
---

# OC-PM: analyzing object-centric event logs and process models - Analysis Index

## Paper Overview

- **Source**: 10-OC-PM_Object-Centric_Process_Mining.pdf
- **Chunks**: 2 chunks, ~18,222 estimated tokens
- **Analyzed**: 2025-12-28
- **Authors**: Alessandro Berti, Wil M. P. van der Aalst (RWTH Aachen University)
- **Published**: International Journal on Software Tools for Technology Transfer, 2022

## Key Extractions

### Entity Types and Definitions

This paper provides formal definitions for object-centric process mining entities, grounding the OCEL 2.0 standard. The core entity types form a clear ontological structure:

| Entity | Definition | Source |
|--------|------------|--------|
| Event | Recorded occurrence with activity, timestamp, related objects | Chunk 1:236-251 |
| Object | Typed identifier with lifecycle and attributes | Chunk 1:448-475 |
| Activity | Labeled action type from universe Uact | Chunk 1:226-228 |
| Object Type | Classification for objects (order, item, etc.) | Chunk 1:440-441 |
| Lifecycle | Sequence of events for an object | Chunk 1:605-621 |

### Entity Relationships

The paper formalizes key relationships using mathematical notation:

| Relationship | Description | Source |
|--------------|-------------|--------|
| piomap: E -> P(O) | Event-to-objects (many-to-many) | Chunk 1:502-505 |
| piotyp: O -> OT | Object-to-type (exactly one) | Chunk 1:510-512 |
| piact: E -> Uact | Event-to-activity | Chunk 1:481-483 |
| Directly-follows | Activity sequence in DFG | Chunk 1:303-308 |

### Framework Comparison

| Framework | Relationship | Details | Source |
|-----------|--------------|---------|--------|
| XES | Extends | Resolves convergence/divergence by multi-object events | Chunk 1:69-78 |
| Artifact-Centric | Related | Similar focus but standardized, no DB dependency | Chunk 2:315-352 |
| Colored Petri Nets | Builds on | Simpler semantics for discovery | Chunk 2:376-450 |

### Empirical Evidence

The paper provides empirical grounding through:
1. **SAP ERP application**: Designed for mainstream information systems (Chunk 1:23-31)
2. **Sales order example**: Detailed walkthrough with order/item/package objects (Chunk 1:166-182)
3. **Tool validation**: OC-PM web tool and ProM plugin (Chunk 2:162-306)

### Key Contributions

1. **OCEL Format**: Formal specification with JSON-OCEL and XML-OCEL implementations
2. **OC-DFG**: Object-centric directly-follows multigraph for process discovery
3. **Flattening Operation**: Projection from object-centric to traditional event logs
4. **Conformance Checking**: Model-independent approaches (CC1: object count, CC2: lifecycle duration)

## Chunk Navigation

### Chunk 1: Introduction, Background, and Core Definitions

- **Summary**: Introduces object-centric process mining, defines traditional and object-centric event logs formally, presents OCEL format, flattening operations, filtering approaches, and OC-DFG discovery. Contains all core entity definitions with mathematical notation.
- **Key concepts**: [Event, Object, Activity, Object Type, Lifecycle, Flattening, OCEL, Directly-follows graph, Convergence/divergence problems]
- **Key quotes**:
  - Line 23-25: "Object-centric process mining is a novel branch of process mining that aims to analyze event data from mainstream information systems..."
  - Line 79-82: "Object-centric event logs have been proposed to resolve the convergence and divergence problems..."
  - Line 448-451: "An object-centric event log is a tuple L = (E, AN, AV, AT, OT, O, pityp, piact, pitime, pivmap, piomap, piotyp, piovmap, <=)"
  - Line 605-611: "The lifecycle of an object o in O as the sequence of events to which the object is related"
- **Load when**: "User asks about OCEL format", "Query mentions object-centric event logs", "Questions about event-object relationships", "Convergence or divergence in process mining"

### Chunk 2: Metrics, Conformance, Tools, and Related Work

- **Summary**: Continues with activity/path frequency metrics, conformance checking approaches (CC1, CC2), comprehensive tool descriptions (OC-PM web tool, ProM plugin), and extensive related work including artifact-centric approaches, Petri nets, graph databases, and flattening-based discovery.
- **Key concepts**: [Activity metrics, Path metrics, Conformance checking, OC-PM tool, ProM framework, Artifact-centric process mining, Colored Petri nets, Object-centric Petri nets, Graph databases]
- **Key quotes**:
  - Line 71-75: "Conformance Checking - Model Independent Approaches... Number of Objects related to an Activity..."
  - Line 162-166: "This section presents two tool supports for the process discovery techniques... a web-based tool and an implementation on top of the ProM process mining framework"
  - Line 315-320: "Artifact-centric process mining is based on defining the properties of key business-relevant entities called business artifacts"
  - Line 470-476: "The current paper describes a set of object-centric process mining techniques which can be used to analyze object-centric event logs"
- **Load when**: "User asks about process mining tools", "Questions about conformance checking in OCEL", "Comparison with artifact-centric approaches", "ProM framework usage"

## Relevance to Research Questions

### Entity Types Universal Across Ontologies
This paper contributes the Event-Object-Activity triad specific to process mining, which maps to the broader Agent-Activity-Entity pattern when considering objects as entities that participate in activities (events).

### Empirical Grounding
Strong empirical grounding through SAP ERP application and comprehensive tool implementation (OC-PM, ProM), validating the OCEL 2.0 standard.

### AI Integration
**N/A** - Paper focuses on process mining foundations (2022), predates LLM integration discussions. However, the formal entity definitions could serve as grounding for future AI agent integration with process data.

### 8-Entity Hypothesis Validation
Partial mapping: Event aligns with Event, Activity with Task, Object Type with Resource/Data categories. The paper's formal definitions could inform a more complete mapping.
