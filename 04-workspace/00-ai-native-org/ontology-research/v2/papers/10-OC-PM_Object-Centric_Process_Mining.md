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
schema_version: "2.3"

chunk_index:
  1:
    token_count: 9157
    fields_found:
      entity_types: true
      entity_definitions: true
      entity_relationships: true
      entity_count: partial
      abstraction_level: true
      framework_comparison: partial
      methodology: true
      ai_integration: false
      agent_modeling: false
      agentic_workflows: false
      generative_ai_patterns: false
      agent_ontology_integration: false
      empirical_evidence: partial
      limitations: partial
      tools_standards: true
  2:
    token_count: 8364
    fields_found:
      entity_types: partial
      entity_definitions: partial
      entity_relationships: false
      entity_count: false
      abstraction_level: false
      framework_comparison: true
      methodology: partial
      ai_integration: false
      agent_modeling: false
      agentic_workflows: false
      generative_ai_patterns: false
      agent_ontology_integration: partial
      empirical_evidence: false
      limitations: true
      tools_standards: true

entity_types:
  - item: "Event"
    chunk: 1
    lines: "46-48"
    quote: "In such event logs, a case is a collection of events related to a particular process execution."
  - item: "Case"
    chunk: 1
    lines: "48-52"
    quote: "For example, in a sales order management system, a case may refer to all the events related to the creation and confirmation of the order, collecting and packing the different order items, the delivery, and invoicing."
  - item: "Object"
    chunk: 1
    lines: "79-86"
    quote: "Object-centric event logs are a novel representation of the event data in the information systems, where each event is related to different objects of different types."
  - item: "Object Type"
    chunk: 1
    lines: "440-441"
    quote: "Uot is the universe of objects types. Example: Uot = {order, item, ...}"
  - item: "Activity"
    chunk: 1
    lines: "226-227"
    quote: "Uact is the universe of activities. Example: Uact = {place order, check availability, ...}"
  - item: "Timestamp"
    chunk: 1
    lines: "229-232"
    quote: "Utimest is the universe of timestamps. Example: Utimest = {2020-07-09T08:21:01.527+01:00, ...}"
  - item: "Attribute"
    chunk: 1
    lines: "424-428"
    quote: "Uatt is the universe of attribute names. Example: Uatt = {resource, weight, ...} Uval is the universe of attribute values. Example: Uval = {500, 1000, Mike, ...}"
  - item: "Lifecycle"
    chunk: 1
    lines: "601-611"
    quote: "The lifecycle of an object o in O as the sequence of events to which the object is related: lif(o) = case_FL(L,piotyp(o))(o)"
  - item: "Directly-Follows Graph (DFG)"
    chunk: 1
    lines: "303-308"
    quote: "A directly-follows graph (DFG) is a simple process model describing the directly-follows relationship between the different activities of a process."
  - item: "Object-Centric Directly-Follows Multigraph (OC-DFG)"
    chunk: 1
    lines: "764-786"
    quote: "An object-centric directly-follows multigraph (OC-DFG) is a tuple (A, OT, N, F, pi_freqn, pi_freqe) where: A is a set of activities, OT is a set of object types, N is the set of nodes of the graph..."

entity_definitions:
  Event: "An element from Ue with associated activity (piact), timestamp (pitime), attribute values (pivmap), and related objects (piomap). Chunk 1:454-456"
  Case: "A collection of events related to a particular process execution. picase: E -> P(Uc) \\ {} associates a non-empty set of cases to each event. Chunk 1:247-248"
  Object: "An element from Uo with associated object type (piotyp) and attribute values (piovmap). O subseteq Uo is the set of object identifiers. Chunk 1:473-474"
  Object_Type: "Classifies objects into categories. OT subseteq Uot is the set of object types; piotyp in O -> OT assigns one type per object. Chunk 1:470-512"
  Activity: "An element from Uact. piact: E -> Uact associates an activity to each event. Chunk 1:481-483"
  Lifecycle: "The sequence of events related to an object: lif(o) = case_FL(L,piotyp(o))(o). Chunk 1:605-611"
  Object_Centric_Event_Log: "A tuple L = (E, AN, AV, AT, OT, O, pitype, piact, pitime, pivmap, piomap, piotyp, piovmap, <=). Chunk 1:448-527"
  Flattening: "Operation FL(L, ot) transforming object-centric event log to traditional event log using an object type. Chunk 1:555-598"
  OC_DFG: "Tuple (A, OT, N, F, pifreqn, pifreqe) with activities, object types, nodes, typed arcs, and frequency measures. Chunk 1:764-786"

entity_relationships:
  - item: "Event-to-Object (piomap)"
    chunk: 1
    lines: "502-505"
    quote: "piomap: E -> P(O) is the function associating an event (identifier) to a set of related object identifiers. Example: piomap(e1) = {o1, i1, i2}."
  - item: "Object-to-ObjectType (piotyp)"
    chunk: 1
    lines: "510-512"
    quote: "piotyp in O -> OT assigns precisely one object type to each object identifier. Example: piotyp(o1) = order."
  - item: "Event-to-Activity (piact)"
    chunk: 1
    lines: "481-483"
    quote: "piact: E -> Uact is the function associating an event (identifier) to its activity."
  - item: "Event-to-Timestamp (pitime)"
    chunk: 1
    lines: "485-488"
    quote: "pitime: E -> Utimest is the function associating an event (identifier) to a timestamp."
  - item: "Directly-Follows Relationship"
    chunk: 1
    lines: "303-308"
    quote: "A directly-follows graph (DFG) is a simple process model describing the directly-follows relationship between the different activities of a process."
  - item: "Typed Arc Relationship (OC-DFG)"
    chunk: 1
    lines: "781-782"
    quote: "F subseteq N x OT x N is a set of typed arcs."

entity_count:
  count: "4-8 core entity types"
  rationale: "Core: Event, Object, ObjectType, Activity. Extended with Attribute, Lifecycle, Trace. Universes defined: Ue, Uc, Uact, Utimest, Uatt, Uval, Utyp, Uo, Uot (9 universes). Object-centric event log tuple has 14 components."
  source: "Chunk 1:215-527"

abstraction_level: "Domain-level (Process Mining). OCEL provides domain-specific abstraction for object-centric process mining, above raw event data but below foundational ontologies. Chunk 1:23-30"

framework_comparison:
  - item: "Traditional Event Logs (XES)"
    chunk: 1
    lines: "69-78"
    quote: "We have a convergence problem when the same event is related to different cases. In event log formats such as XES, this leads to replicating the same event."
  - item: "Artifact-Centric Process Mining"
    chunk: 2
    lines: "315-352"
    quote: "Artifact-centric process mining is based on defining the properties of key business-relevant entities called business artifacts."
  - item: "Object-Centric Behavioral Constraint Models (OCBC)"
    chunk: 2
    lines: "356-364"
    quote: "The object-centric behavioral constraint models (OCBC) are proposed as declarative models with rich semantics."
  - item: "Colored Petri Nets"
    chunk: 2
    lines: "376-389"
    quote: "Colored Petri nets allow the storage of a data value for each token. The data value is called the token color."
  - item: "Object-Centric Petri Nets"
    chunk: 2
    lines: "436-450"
    quote: "Object-centric Petri nets have been proposed to support a subset of the semantics of colored Petri nets."

ai_integration: "NOT_FOUND"

agent_modeling: "NOT_FOUND"

agentic_workflows: "NOT_FOUND"

generative_ai_patterns: "NOT_FOUND"

agent_ontology_integration:
  - item: "Ontology-based extraction reference"
    chunk: 2
    lines: "417-418"
    quote: "An approach for ontology-based extraction of event data has been proposed in [22]."

methodology: "Formal mathematical approach with empirical grounding. Uses set theory and tuple notation for OCEL metamodel. Designed for event logs from SAP ERP and similar systems. Bottom-up from practical problems (convergence/divergence). Chunk 1:41-45, Chunk 2:473-477"

empirical_evidence:
  - item: "SAP ERP Event Logs"
    chunk: 1
    lines: "23-26"
    quote: "Object-centric process mining aims to analyze event data from mainstream information systems (such as SAP) more naturally."
  - item: "Tool Implementation"
    chunk: 2
    lines: "496-501"
    quote: "Comprehensive tool support available as web interface and ProM framework plugin for ingestion, exploration, discovery of OC-DFGs and object-centric Petri nets."

limitations:
  - item: "Early Development Stage"
    chunk: 1
    lines: "111-119"
    quote: "The discipline is still in an early development stage. Some important aspects such as exploration and filtering have been marginally explored."
  - item: "Missing Real-Life Assessment"
    chunk: 2
    lines: "502-507"
    quote: "An assessment of the proposed techniques on real-life event logs is missing from the current paper."
  - item: "Graph Database Scalability"
    chunk: 2
    lines: "413-416"
    quote: "The scalability of graph databases on process mining tasks still needs to be investigated thoroughly. Execution time in Neo4J is disappointing."
  - item: "OCBC Scalability Issues"
    chunk: 2
    lines: "362-364"
    quote: "The discovery of the rich set of constraints and the proposed event log format have scalability issues."

tools_standards:
  - item: "OCEL Format (JSON-OCEL, XML-OCEL)"
    chunk: 1
    lines: "529-533"
    quote: "The OCEL format has been proposed for object-centric event logs. Two implementations: JSON-OCEL, XML-OCEL, MongoDB."
  - item: "XES Standard"
    chunk: 1
    lines: "71"
    quote: "In event log formats such as XES, this leads to replicating the same event."
  - item: "OC-PM Web Tool"
    chunk: 2
    lines: "187-199"
    quote: "OC-PM tool available at https://ocpm.info, HTML/Javascript content running in browser without backend."
  - item: "ProM Framework Plugin"
    chunk: 2
    lines: "288-298"
    quote: "Implementation on ProM 6.x framework in OCELStandard package."
  - item: "Python/Java/Javascript Libraries"
    chunk: 1
    lines: "530-531"
    quote: "Tool support available for Java/ProM framework, Javascript, Python."
---

# OC-PM: analyzing object-centric event logs and process models

## Summary

This paper by Berti and van der Aalst (2022) presents a comprehensive approach to object-centric process mining, addressing convergence and divergence problems in traditional event logs. The key contribution is the OCEL (Object-Centric Event Log) format and associated techniques for exploration, filtering, and process discovery.

## Key Entity Types

The OCEL metamodel defines the following core entities:

1. **Event** - An occurrence with activity, timestamp, and related objects
2. **Object** - A business entity with type and attributes
3. **Object Type** - Classification of objects (e.g., order, item, package)
4. **Activity** - The action performed in an event
5. **Case** - (Traditional) A collection of events for a process execution
6. **Lifecycle** - The sequence of events related to an object
7. **Directly-Follows Graph (DFG)** - Simple process model showing activity sequences
8. **Object-Centric DFG (OC-DFG)** - Multi-typed process model with typed arcs

## Core Relationships

- **Event-to-Object (piomap)**: Many-to-many relationship allowing events to relate to multiple objects
- **Object-to-Type (piotyp)**: Each object has exactly one type
- **Directly-Follows**: Sequential relationship between activities per object lifecycle
- **Typed Arcs**: Edges in OC-DFG are typed by object type

## Relevance to Research Questions

### Entity Definitions
The paper provides formal mathematical definitions for all core entities using set theory and function notation. Strong example of precise entity specification in a domain ontology.

### Framework Comparison
Explicitly compares to:
- XES (traditional event logs) - shows convergence/divergence problems
- Artifact-centric process mining
- Object-centric behavioral constraint models (OCBC)
- Colored Petri nets

### Tools and Standards
- OCEL format (JSON-OCEL, XML-OCEL)
- OC-PM web tool (https://ocpm.info)
- ProM framework plugin
- Support libraries for Python, Java, Javascript

## Limitations

1. Early development stage of the field
2. No real-life event log assessment in this paper
3. Scalability issues with graph database approaches
4. Missing model-based conformance checking

## AI/Agent Integration

This paper does not address AI agents, LLMs, or agentic workflows. It is purely focused on data modeling and algorithmic aspects of object-centric process mining.

## Key Contribution to Ontology Research

The paper's primary value is formalizing the **Event-Object-ObjectType** triad for process mining:

1. **Resolves convergence/divergence**: Events can relate to multiple objects
2. **Object lifecycle formalization**: lif(o) and trace(o) definitions
3. **Flattening operation**: Bridge to traditional process mining
4. **OC-DFG**: Object-centric process model with typed edges

This is foundational for OCEL 2.0 and provides empirical grounding for ontology design in process mining domains.
