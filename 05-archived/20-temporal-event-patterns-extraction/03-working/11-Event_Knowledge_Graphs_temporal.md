---
paper_id: "11-Process_Mining_Event_Knowledge_Graphs"
title: "Process Mining over Multiple Behavioral Dimensions with Event Knowledge Graphs"
authors:
  - "Dirk Fahland"
year: 2022
extraction_version: "1.0"
extraction_date: "2026-01-01"
extraction_focus: "temporal_event_patterns"

event_types:
  - type: "Event (graph node)"
    description: "A node in a labeled property graph that records an activity name and a timestamp. Each event e records which action has been executed at which time."
    source: "Chunk 1:201-206, 624-631"
  - type: "Starting Event"
    description: "An event with no incoming df-relationship at all, or no incoming df-relationship for a specific entity, indicating the start of a df-path."
    source: "Chunk 2:88-92"
  - type: "Ending Event"
    description: "An event with no outgoing df-relationship at all, or no outgoing df-relationship for a specific entity, indicating completion of a df-path."
    source: "Chunk 2:88-92"
  - type: "Intermediate Event"
    description: "An event that is neither starting nor ending in a df-path of an entity; occurs within the middle of an entity's execution."
    source: "Chunk 2:106-107"
  - type: "Shared Event"
    description: "An event where two or more entities' df-paths synchronize, indicating entity interaction."
    source: "Chunk 2:157-160"
  - type: "Batching Event"
    description: "An event where multiple entities of the same type synchronize, representing batch processing."
    source: "Chunk 2:174-176"
  - type: "Task Instance"
    description: "A subgraph over event nodes e1,...,ek where an actor's df-path and an entity's df-path meet in e1, diverge in ek, and synchronize in each node between."
    source: "Chunk 2:621-625"

event_definitions:
  Event:
    definition: "A record in a labeled property graph that captures an activity name and timestamp. Each event e records an activity via e.act and a time via e.time."
    temporal_properties:
      - "time (timestamp of occurrence)"
      - "act (activity name)"
    graph_properties:
      - "node label: Event"
      - "corr relationships to Entity nodes"
      - "df relationships to other Event nodes"
    source: "Chunk 1:201-206, 624-642"
  Entity:
    definition: "A named object handled by a process, identified by entity type attributes. Entities are correlated to events and define local directly-follows orderings."
    temporal_properties:
      - "df-path (sequence of temporally ordered events)"
      - "starting_event (first event in df-path)"
      - "ending_event (last event in df-path)"
    source: "Chunk 1:248-254, 667-672"
  DF-Path:
    definition: "A path of directly-follows relationships between events for a single entity, analogous to a trace in classical event logs."
    temporal_properties:
      - "sequence of events ordered by time"
      - "entity-local temporal ordering"
    source: "Chunk 1:667-672"
  Task_Instance:
    definition: "A unit of work materializing as a subgraph where an Actor's df-path and an Entity's df-path synchronize over consecutive events, representing a larger unit of work consisting of multiple related activities."
    temporal_properties:
      - "contains multiple sequential events"
      - "synchronizes actor and entity df-paths"
    source: "Chunk 2:621-625"

temporal_relations:
  - relation: "directly-follows (df)"
    domain: "Event"
    range: "Event"
    semantics: "e2 directly follows e1 from perspective of entity n iff (1) both e1 and e2 are correlated to n, (2) e1.time < e2.time, and (3) no other event e' correlated to n occurs between e1.time and e2.time"
    source: "Chunk 1:519-529, 636-642"
  - relation: "correlation (corr)"
    domain: "Event"
    range: "Entity"
    semantics: "Event e is correlated to entity n if the entity identifier appears in the event's attributes; r = (e, n) is a directed edge from event node to entity node"
    source: "Chunk 1:265-269, 633-635"
  - relation: "synchronization"
    domain: "Entity"
    range: "Entity"
    semantics: "Two or more entities n1,...,nk synchronize in a shared event e if two or more df-paths of n1,...,nk go through e"
    source: "Chunk 2:157-160"
  - relation: "directly-depends-on"
    domain: "Event"
    range: "Event"
    semantics: "Event e directly depends on any event ei that directly precedes e via an incoming df-relationship (ei, e) along some entity"
    source: "Chunk 2:232-235"
  - relation: "delayed-by"
    domain: "Event"
    range: "Event"
    semantics: "For events e1,...,ek preceding e sorted by delay to e, each later event ei (i>1) delayed the synchronization as entity ni became ready later"
    source: "Chunk 2:236-241"
  - relation: "related (between entities)"
    domain: "Entity"
    range: "Entity"
    semantics: "Two entities are related if they co-occur in the same event record; R(ent1,ent2) = {(e.ent1, e.ent2) | e.ent1 != null, e.ent2 != null}"
    source: "Chunk 1:300-302"
  - relation: "derived"
    domain: "Derived Entity"
    range: "Entity"
    semantics: "Traceability relationship from a reified derived entity (n1, n2) back to original entities n1 and n2"
    source: "Chunk 1:897-898"
  - relation: "observes"
    domain: "Event"
    range: "Class"
    semantics: "Links each event e to its aggregated Class node c where e.Activity = c"
    source: "Chunk 2:336-338"
  - relation: "contains"
    domain: "TaskInstance"
    range: "Event"
    semantics: "Links a TaskInstance node to each Event node that is part of the task instance"
    source: "Chunk 2:714-716"

lifecycle_patterns:
  - entity: "Entity (generic)"
    states: ["not-visible", "first-event-observed", "active", "last-event-observed"]
    transitions:
      - from: "not-visible"
        to: "first-event-observed"
        trigger: "Starting event (no incoming df for entity)"
      - from: "first-event-observed"
        to: "active"
        trigger: "Intermediate event occurrence"
      - from: "active"
        to: "active"
        trigger: "Subsequent intermediate events"
      - from: "active"
        to: "last-event-observed"
        trigger: "Ending event (no outgoing df for entity)"
    source: "Chunk 2:88-92, 170-173, 182-193"
    notes: "Paper notes that entities may exist before/after observation window; 'created' and 'closed' refer to visibility scope, not physical existence"
  - entity: "Order (example)"
    states: ["created", "invoice-created", "packed", "shipped"]
    transitions:
      - from: "created"
        to: "invoice-created"
        trigger: "Create Invoice event"
      - from: "invoice-created"
        to: "packed"
        trigger: "Pack Shipment event"
      - from: "packed"
        to: "shipped"
        trigger: "Ship event"
    source: "Chunk 2:112-113"
  - entity: "Supplier Order (example)"
    states: ["placed", "updated", "received", "unpacked"]
    transitions:
      - from: "placed"
        to: "updated"
        trigger: "Update SO event (optional)"
      - from: "placed"
        to: "received"
        trigger: "Receive SO event"
      - from: "updated"
        to: "received"
        trigger: "Receive SO event"
      - from: "received"
        to: "unpacked"
        trigger: "Multiple Unpack events"
    source: "Chunk 2:115-116"
  - entity: "Item (example)"
    states: ["received", "unpacked", "scanned", "stored", "retrieved", "packed"]
    transitions:
      - from: "received"
        to: "unpacked"
        trigger: "Unpack event"
      - from: "unpacked"
        to: "scanned"
        trigger: "Scan event"
      - from: "scanned"
        to: "stored"
        trigger: "Store event"
      - from: "stored"
        to: "retrieved"
        trigger: "Retrieve event"
      - from: "retrieved"
        to: "packed"
        trigger: "Pack Shipment event"
    source: "Chunk 2:118-119, 484-492"

state_change_mechanisms:
  - mechanism: "Intermediate synchronization"
    description: "An event that is intermediate for multiple entities represents an update or state change of one or more entities that requires the involvement of the other entities."
    source: "Chunk 2:163-168"
  - mechanism: "Entity creation/initiation"
    description: "An event that is intermediate for entity n but a starting event for entities n1,...,nk can be interpreted as entity n 'created' or 'initiated' entities n1,...,nk."
    source: "Chunk 2:170-171"
  - mechanism: "Entity closing/completion"
    description: "An event that is intermediate for entity n and ending event for n1,...,nk is 'closing' or 'completing' entities n1,...,nk."
    source: "Chunk 2:172-173"
  - mechanism: "Batching"
    description: "An event where multiple entities of the same type synchronize represents batch processing where multiple entities are handled together."
    source: "Chunk 2:174-176"
  - mechanism: "Dynamic attribute update"
    description: "Relations between entities are updated dynamically by the process over time, though the paper's approach captures only static aggregated view."
    source: "Chunk 1:338-342"

agent_participation:
  - participation_type: "performs"
    description: "Actor executes activities on entities. Each actor follows its own behavioral patterns across multiple entities."
    source: "Chunk 2:597-601, 605-608"
  - participation_type: "synchronizes-with"
    description: "Actor's df-path synchronizes with entity's df-path in shared events during task execution."
    source: "Chunk 2:621-625"
  - participation_type: "hands-over-to"
    description: "One actor hands work over to another actor, revealed by df-relationships between task instances."
    source: "Chunk 2:643-648"
  - participation_type: "interrupts"
    description: "Actor interrupts work on one entity to perform work on another, causing context switches and delays."
    source: "Chunk 2:660-667"
  - participation_type: "singleton-task"
    description: "Actor performs single activity on entity then moves to next entity, synchronizing only in one event."
    source: "Chunk 2:605-608, 633"
  - participation_type: "multi-activity-task"
    description: "Actor performs multiple related activities on same entity, with df-path synchronizing over multiple consecutive events."
    source: "Chunk 2:619-620, 637-638"

event_correlation:
  - pattern: "Event-to-Entity correlation (corr)"
    description: "Each event can be correlated to multiple entities via corr relationships. An event e is correlated to entity n if e.ent = n or n in e.ent."
    source: "Chunk 1:265-269, 633-635"
  - pattern: "Entity-local directly-follows"
    description: "Instead of global case-based ordering, each entity has its own local directly-follows relation defining temporal ordering only for events correlated to that entity."
    source: "Chunk 1:519-529"
  - pattern: "Multi-entity event correlation"
    description: "An event can be correlated to multiple entities simultaneously, allowing df-paths of different entities to meet/synchronize in shared events."
    source: "Chunk 2:157-160"
  - pattern: "Derived entity correlation"
    description: "Events correlated to either n1 or n2 become correlated to derived entity (n1, n2), enabling analysis of entity interactions."
    source: "Chunk 1:899-902"
  - pattern: "Activity-as-entity correlation"
    description: "Treating Activity property as entity identifier reveals how entities pass through activity 'stations' and queue behavior."
    source: "Chunk 2:478-492"
  - pattern: "Resource/Actor correlation"
    description: "Actor entities correlated to events reveal task execution patterns and work handovers between actors."
    source: "Chunk 2:597-604"

ordering_mechanisms:
  - mechanism: "Timestamp ordering"
    description: "Events are ordered by their time property (e1.time < e2.time). Timestamps are from a totally ordered universe Valtime."
    source: "Chunk 1:198, 527"
  - mechanism: "Local directly-follows (per entity)"
    description: "Temporal ordering is local to each entity rather than global. e2 directly follows e1 from perspective of n iff both correlated to n, e1.time < e2.time, and no other event of n in between."
    source: "Chunk 1:519-529"
  - mechanism: "DF-path construction"
    description: "For each entity n, events correlated to n are sorted by time to form a maximal df-path; paths meet when events are correlated to multiple entities."
    source: "Chunk 1:667-672, 800-810"
  - mechanism: "Transitive delay analysis"
    description: "Build delay*(e) set of transitive predecessors that delayed e most by recursively finding the event that delayed each predecessor most."
    source: "Chunk 2:247-250"
  - mechanism: "Performance Spectrum visualization"
    description: "Setting x-coordinate by time and y-coordinate by Activity entity reveals temporal queuing behavior including FIFO violations."
    source: "Chunk 2:517-527, 569-577"

causation_patterns:
  - pattern: "Direct dependency"
    description: "Event e directly depends on any event ei that directly precedes e via an incoming df-relationship (ei, e) along some entity ni."
    source: "Chunk 2:232-235"
  - pattern: "Delay propagation"
    description: "If e1,...,ek precede e sorted by delay to e, event e1 was first ready; each later ei delayed synchronization as entity ni became ready later."
    source: "Chunk 2:236-241"
  - pattern: "Transitive delay chain"
    description: "Set delay*(e) contains transitive predecessors delaying e, found by adding event e' that delayed e most, then e'' that delayed e' most, etc."
    source: "Chunk 2:247-250"
  - pattern: "Bottleneck cascade"
    description: "Aggregating high-level events detecting performance anomalies and mining for cause-effect relations reveals how performance anomalies cascade through a process."
    source: "Chunk 2:866-868"
  - pattern: "Synchronous interaction"
    description: "Event e where df-paths of n1 and n2 synchronize represents a synchronous (simultaneous) interaction between entities."
    source: "Chunk 2:197-198"
  - pattern: "Asynchronous interaction"
    description: "A df-path for entity n describes an asynchronous interaction between n1 and n2 if n synchronizes with both in different events."
    source: "Chunk 2:198-200"
  - pattern: "Message passing"
    description: "If the df-path for n has only 2 events <e1, e2>, entity n can be interpreted as a message from n1 to n2."
    source: "Chunk 2:200-201"
  - pattern: "Handover"
    description: "An event e that is ending event of entity n1 and starting event of entity n2 represents a handover from n1 to n2."
    source: "Chunk 2:201-202"

temporal_standards:
  - standard: "Timestamp (Valtime)"
    description: "Events record timestamps from a totally ordered universe of time values (Valtime subset of Val)"
    source: "Chunk 1:198"
  - standard: "Labeled Property Graph (LPG)"
    description: "Data model for event knowledge graphs with typed nodes (Event, Entity) and relationships (df, corr) carrying properties"
    source: "Chunk 1:574-583"
  - standard: "Neo4j / Cypher"
    description: "Implementation standard for event knowledge graphs using graph database with Cypher query language"
    source: "Chunk 1:182-184, Chunk 2:60-61"

event_log_formats:
  - format: "Event Knowledge Graph"
    description: "LPG with Event and Entity node labels, df and corr relationship labels. Events carry act and time properties; df relationships carry entity reference."
    source: "Chunk 1:624-642"
  - format: "Event Table with Entity Types"
    description: "Input format T = (E, Attr, #, ENT) where ENT designates entity type attributes for correlation"
    source: "Chunk 1:218-220"
  - format: "Object-Centric Event Log (OCEL)"
    description: "Formal equivalent to event table with entity types; paper uses more general term 'entity' instead of 'object'"
    source: "Chunk 1:236-239"
  - format: "Multi-entity Directly-Follows Graph"
    description: "Aggregated view with Class nodes for activities and df-relationships between classes per entity type"
    source: "Chunk 2:362-367"
  - format: "Synchronous Proclet Model"
    description: "Multi-entity process model where each proclet is a Petri net for one entity type with synchronization edges between shared transitions"
    source: "Chunk 2:884-890"

key_concepts_for_UDWO:
  event_as_graph_node:
    description: "Events modeled as nodes in labeled property graphs with activity and timestamp properties, connected via typed relationships"
    relevance: "Foundation for graph-based event representation in UDWO"
    source: "Chunk 1:624-631"
  local_directly_follows:
    description: "Temporal ordering is local to each entity rather than global; avoids convergence/divergence problems of case-centric logs"
    relevance: "Key pattern for multi-entity event ordering in agent systems"
    source: "Chunk 1:514-541"
  entity_synchronization:
    description: "Multiple entities synchronize in shared events where their df-paths meet, representing entity interactions"
    relevance: "Captures agent-object and agent-agent interactions at event level"
    source: "Chunk 2:155-160"
  actor_as_autonomous_entity:
    description: "Actors (workers/resources) modeled as entities with their own df-paths and behavioral patterns"
    relevance: "Direct mapping to agent modeling in UDWO"
    source: "Chunk 2:597-601"
  task_instance_as_synchronized_paths:
    description: "Task instances emerge as subgraphs where actor and entity df-paths synchronize over consecutive events"
    relevance: "Pattern for agent task execution modeling"
    source: "Chunk 2:621-625"
  derived_entity_for_interactions:
    description: "Reifying relations between entities into derived entities enables explicit modeling of entity interactions"
    relevance: "Pattern for modeling relationships between agents and objects"
    source: "Chunk 1:893-906"
  multi_layer_process_graphs:
    description: "Event knowledge graphs can be extended with additional layers (Task Instance, Task, Class) linked by relationships"
    relevance: "Architecture for multi-abstraction process representation"
    source: "Chunk 2:674-759"

limitations_noted:
  - item: "Static vs Dynamic Relations"
    description: "Relations recovered from event data are a static view aggregated over time while processes update relations dynamically"
    source: "Chunk 1:338-342"
  - item: "Observation window incompleteness"
    description: "Both the graph and input data may be incomplete; entities 'created' or 'closed' may exist before/after recorded data"
    source: "Chunk 2:182-193"
  - item: "Multiple dynamics over multiple entities"
    description: "How to analyze combination of multiple dynamics over multiple entities (top right quadrant) is an open question"
    source: "Chunk 2:845-846"
  - item: "Entity interaction complexity"
    description: "While proclets can describe entity interactions, the behavior tends to be rather unstructured resulting in overly complex models"
    source: "Chunk 3:25-29"
---

# Temporal Pattern Extraction: Process Mining Event Knowledge Graphs

## Summary

This paper by Dirk Fahland introduces **event knowledge graphs** as a data structure for process mining over multiple entities. The key temporal innovation is the **local directly-follows relation per entity** rather than a global case-based ordering, which avoids false behavioral information (convergence and divergence) when analyzing multi-entity processes.

## Key Temporal Contributions

### 1. Event as Graph Node
Events are modeled as nodes in labeled property graphs (LPGs) with:
- **act** property: activity name
- **time** property: timestamp from totally ordered universe
- **corr** relationships: linking to correlated entity nodes
- **df** relationships: local directly-follows edges to other events

### 2. Local Directly-Follows Relation
The paper's central temporal contribution is defining directly-follows **per entity** rather than globally:
- e2 directly follows e1 from perspective of entity n iff:
  1. Both e1 and e2 are correlated to n
  2. e1.time < e2.time
  3. No other event e' correlated to n occurs between e1.time and e2.time

This avoids false temporal orderings when flattening multi-entity data.

### 3. Entity Synchronization Patterns
Multiple entities can **synchronize** in shared events where their df-paths meet:
- **Intermediate synchronization**: Entity state update requiring other entities
- **Entity creation**: Starting event for n1,...,nk that is intermediate for n
- **Entity completion**: Ending event for n1,...,nk that is intermediate for n
- **Batching**: Multiple entities of same type synchronizing in one event

### 4. Actor as Autonomous Entity
Actors (human workers or machines) are modeled as entities with their own behavioral patterns:
- Each actor has a df-path showing their work sequence
- **Task instances** emerge where actor and entity df-paths synchronize
- Task handovers visible as df-relationships between task instances

### 5. Delay and Dependency Analysis
Temporal dependency patterns for performance analysis:
- **Direct dependency**: Event e depends on all events with incoming df-relationships
- **Delay propagation**: Later arriving entities delay synchronization events
- **Transitive delay chain**: Set delay*(e) traces back through most-delaying predecessors

## Relevance to UDWO Metamodel

### Event Entity Definition
The paper provides a graph-based event definition suitable for UDWO:
- Events as first-class nodes with temporal properties
- Multi-entity correlation (not single case)
- Local temporal ordering per participant entity

### Agent Participation Patterns
Actor modeling directly maps to agent participation:
- Actors have autonomous behavioral patterns (df-paths)
- Task instances show agent-object synchronization
- Work handovers between agents are explicit relationships

### Entity Lifecycle in Graph Structure
Lifecycle patterns emerge from df-path positions:
- Starting event (no incoming df) = creation/visibility
- Intermediate events = state updates
- Ending event (no outgoing df) = completion/invisibility

### Synchronization as Interaction
Entity synchronization patterns model interactions:
- Synchronous: both entities in same event
- Asynchronous: via intermediate entity df-path
- Message: 2-event entity path between synchronizing entities
- Handover: ending event for one, starting for another
