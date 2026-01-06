---
paper_id: "11"
title: "Process Mining over Multiple Behavioral Dimensions with Event Knowledge Graphs"
authors: ["Dirk Fahland"]
venue: "Process Mining Handbook, LNBIP 448"
year: 2022
doi: "10.1007/978-3-031-08848-3_9"

extraction_version: "2.0"
extraction_date: "2025-12-31"
extractor: "Claude Opus 4.5"

ontological_primitives:
  - term: "Event"
    definition: "A record that has at minimum an activity name (e.act) and a timestamp (e.time), representing an occurrence in a process"
    source: "Chunk 1:201-206"
    unique_aspects: "Events are nodes in a labeled property graph, not just records in a table. Events can be correlated to MULTIPLE entities simultaneously"

  - term: "Entity"
    definition: "Any identifiable thing that events can be correlated to - including objects handled by the process AND organizational entities that execute it"
    source: "Chunk 1:31-34, 248-254"
    unique_aspects: "Deliberately broad - includes tangible objects (Orders, Items), organizational actors (workers, machines), AND abstract concepts like Activity itself. Paper refuses to privilege 'case' as a special entity type"

  - term: "Entity Type"
    definition: "A classification of entities designated by attribute columns in the event table (ent in ENT subset of Attr)"
    source: "Chunk 1:218-221"
    unique_aspects: "NOT a rigid ontological category - emerges from data schema. Multiple entity types can coexist. Paper uses Resource, Order, Supplier Order, Item, Invoice, Payment as examples"

  - term: "Correlation"
    definition: "The relationship (e, n) between an event e and an entity n when the entity identifier appears in the event's attributes"
    source: "Chunk 1:265-277"
    unique_aspects: "ONE event can be correlated to MANY entities. This is the key primitive that enables multi-entity analysis. Correlation is NOT derived from a single case identifier"

  - term: "Directly-Follows (per Entity)"
    definition: "e1 directly-follows e2 from the perspective of entity n iff both are correlated to n, e1 occurred before e2, and no other event correlated to n occurred in between"
    source: "Chunk 1:519-530"
    unique_aspects: "LOCAL not global. Each entity has its own directly-follows relation. This is the fundamental departure from classical process mining"

  - term: "df-path"
    definition: "A path of directly-follows relationships where all relationships are defined for the same entity"
    source: "Chunk 1:667-673"
    unique_aspects: "Replaces 'trace' from classical event logs. Multiple df-paths can pass through the same event. A maximal df-path represents the complete behavior for one entity"

  - term: "Derived Entity"
    definition: "A reified pair (n1, n2) of related entities that becomes a first-class entity with its own correlation and df-path"
    source: "Chunk 1:893-906"
    unique_aspects: "Interactions BETWEEN entities become entities themselves. This allows capturing inter-entity dependencies that are invisible in single-entity views"

  - term: "Labeled Property Graph (LPG)"
    definition: "A graph where nodes and edges have labels (types) and can carry attribute-value pairs as properties"
    source: "Chunk 1:574-584"
    unique_aspects: "Native data structure for knowledge graphs. Supports properties on relationships (unlike RDF), which is essential for df-relationships that reference their entity"

  - term: "Class Node"
    definition: "Aggregated node representing all events with the same Activity property value"
    source: "Chunk 2:330-341"
    unique_aspects: "Different from Entity nodes semantically - Class aggregates existing df-relationships, while Activity-as-Entity derives NEW df-relationships"

  - term: "Task Instance"
    definition: "A subgraph where an Actor's df-path and another entity's df-path meet, synchronize over consecutive events, then diverge"
    source: "Chunk 2:621-627"
    unique_aspects: "A larger 'unit of work' than a single activity. Emerges from graph patterns, not predefined. Reveals how workers actually perform sequences of activities"

structural_patterns:
  - pattern_name: "Multi-Correlation Star"
    structure: "One Event node connected via multiple corr relationships to multiple Entity nodes"
    instances:
      - "Event e27 correlated to Order O1, Item X1, Item X2, Item Y1 (Chunk 1:779-780)"
      - "Event e30 correlated to Invoice I1, Invoice I2, Payment P1 (Chunk 1:272-273)"
    source: "Throughout paper - core structural insight"

  - pattern_name: "df-Path Fabric"
    structure: "Network of interweaving df-paths that meet at shared events and diverge"
    instances:
      - "Figure 9 - Complete event knowledge graph showing all entity df-paths interleaving"
      - "Item df-paths traverse Activity df-paths 'largely in parallel' (Chunk 2:492-493)"
    source: "Chunk 1:148-149, Chunk 2:74"

  - pattern_name: "Entity-Activity Grid (Performance Spectrum)"
    structure: "2D layout with Activities on y-axis, time on x-axis, showing how entities traverse activities"
    instances:
      - "Figure 17 - Items X1..Y2 passing through Receive SO, Unpack, Scan, Store, Retrieve, Pack Shipment"
    source: "Chunk 2:520-577"
    unique_aspects: "Visual representation reveals queuing behavior, FIFO violations, batching patterns"

  - pattern_name: "Derived Entity Bridge"
    structure: "(n1, n2) derived entity with df-path connecting events from n1 and n2"
    instances:
      - "(Order, Payment) derived entities bridging Order events to Payment events via Invoice"
      - "df-path from Create Invoice in O1 via Clear Invoice in P1 to Pack Shipment in O2"
    source: "Chunk 1:908-912"

  - pattern_name: "Actor-Entity Synchronization"
    structure: "Actor df-path and Entity df-path meeting in shared events"
    instances:
      - "R4's df-path synchronizing with O1 over e27, e28 (Pack Shipment, Ship)"
      - "R2 interrupting work on A to perform task on I2 (context switch visible in graph)"
    source: "Chunk 2:618-627"

  - pattern_name: "Multi-Entity DFG"
    structure: "Aggregation where each df-relationship between Class nodes is specific to one entity type"
    instances:
      - "Figure 12 - Aggregated model showing df-relationships labeled by entity type"
    source: "Chunk 2:366-367"
    unique_aspects: "Also called 'multi-viewpoint DFG' or 'artifact-centric model'"

  - pattern_name: "Synchronous Proclet"
    structure: "Multiple Petri nets (one per entity type) with synchronization edges between transitions"
    instances:
      - "Figure 21 - Proclets for Order, Supplier Order, Invoice, Item, Payment, (Order,Payment), plus Actor proclets"
    source: "Chunk 2:885-907, Chunk 3:5-46"
    unique_aspects: "Cardinality annotations show how many entities participate (e.g., R4 packs 2-3 Items into 1 Shipment)"

  - pattern_name: "Process Knowledge Graph Layers"
    structure: "Multiple layers: Event-Entity -> Task Instance -> Task -> Class, with contains/observes relationships between layers"
    instances:
      - "Figure 19 showing Event Entity Layer, Task Instance Layer, Task Layer, Class Layer"
    source: "Chunk 2:698-761"

novel_concepts:
  - concept: "Event Knowledge Graph"
    definition: "An LPG with Event and Entity nodes, corr and df relationship types, where df relationships are per-entity and reference their entity"
    novelty_claim: "First formal definition combining knowledge graphs with process mining. Replaces traces with a graph fabric"
    source: "Chunk 1:624-655 (Definition 8)"

  - concept: "Local Directly-Follows"
    definition: "Directly-follows relation computed separately for each entity rather than globally for a case"
    novelty_claim: "Avoids convergence and divergence problems of classical event logs. Preserves correct behavioral information"
    source: "Chunk 1:492-542"

  - concept: "Convergence and Divergence"
    definition: "False behavioral information introduced when flattening multi-entity data to case-centric traces. Convergence: false order between unrelated events. Divergence: event duplication across cases"
    novelty_claim: "Named and formalized as the fundamental problems event knowledge graphs solve"
    source: "Chunk 1:441-446"

  - concept: "Entity Reification"
    definition: "Converting a relation R(ent1, ent2) between entities into a new derived entity (n1, n2) that can have its own df-path"
    novelty_claim: "Makes inter-entity interactions first-class citizens with their own behavioral traces"
    source: "Chunk 1:893-906"

  - concept: "Activity as Entity"
    definition: "Treating the Activity property as an entity identifier to infer Activity entities and their df-paths"
    novelty_claim: "Reveals queue structure - space between activities where entities wait. Semantically different from Class aggregation"
    source: "Chunk 2:478-501"

  - concept: "Performance Spectrum"
    definition: "Visualization with Activity on y-axis, time on x-axis, showing how entities traverse activities"
    novelty_claim: "Reveals FIFO violations, batching, overtaking patterns invisible in other representations"
    source: "Chunk 2:520-525"

  - concept: "Task Instance Detection"
    definition: "Identifying subgraphs where Actor and Entity df-paths synchronize over consecutive events"
    novelty_claim: "Discovers actual 'units of work' larger than single activities from graph patterns"
    source: "Chunk 2:621-628"

  - concept: "Multi-Layered Process Knowledge Graph"
    definition: "Event knowledge graph extended with aggregation layers (TaskInstance, Task, Class) linked by contains/observes relationships"
    novelty_claim: "Enables analysis at multiple abstraction levels while maintaining traceability to events"
    source: "Chunk 2:698-761"

  - concept: "Delay Chain Analysis"
    definition: "Building set delay*(e) of transitive predecessors that delayed event e the most"
    novelty_claim: "Enables root cause analysis for delays by following the delay chain backward"
    source: "Chunk 2:247-253"

semantic_commitments:
  - commitment: "Event-centric vs Case-centric"
    position: "Events are the primitive atoms, not cases. Cases (if needed) are derived from entity correlations"
    implications: "No privileged 'case' notion. Any entity type can serve as a grouping mechanism. Multiple valid perspectives coexist"
    source: "Chunk 1:119-120"

  - commitment: "Graph vs Sequential"
    position: "Process behavior is fundamentally a graph fabric, not a collection of sequences"
    implications: "Traces are projections onto entities, not the fundamental structure. Synchronization and interleaving are first-class"
    source: "Chunk 1:148-149, 163-165"

  - commitment: "Local vs Global Ordering"
    position: "Temporal ordering is LOCAL to each entity. No global total order across all events"
    implications: "Partial order semantics. Events can be concurrent. Avoids false dependencies"
    source: "Chunk 1:514-516, Chunk 2:684"

  - commitment: "Entity Generalization"
    position: "Entities include tangible objects, actors, AND abstract concepts like activities or queues"
    implications: "Unified treatment of control-flow, organizational, and data perspectives. All are entities with df-paths"
    source: "Chunk 2:418-424"

  - commitment: "Inference from Data"
    position: "Entities, correlations, relations, and df-paths are INFERRED from data, not predefined"
    implications: "Schema recovery rather than schema prescription. Process structure emerges from data"
    source: "Chunk 1:292-294, 330-332"

  - commitment: "Open World / Incomplete Data"
    position: "Data may be incomplete. Entities exist before entering visibility and after leaving it"
    implications: "Starting/ending events show visibility boundaries, not creation/destruction. Graph may be extended with new events"
    source: "Chunk 2:183-194"

boundary_definitions:
  - entity_type: "Event"
    identity_criteria: "Unique node in the graph. Identified by combination of timestamp and activity (plus any additional attributes)"
    boundary_cases: "Same activity at same timestamp for different entities - are they one event or multiple? Depends on data recording"
    source: "Chunk 1:201-206"

  - entity_type: "Entity"
    identity_criteria: "Unique identifier value in an entity type attribute"
    boundary_cases: "Entity identifiers may be reused across types (handled by type qualification). Dynamically changing relationships not fully addressed"
    source: "Chunk 1:248-254, 340-342"

  - entity_type: "df-path"
    identity_criteria: "Maximal sequence of df-relationships for the same entity"
    boundary_cases: "When does a path 'start' or 'end'? Paper explicitly notes starting/ending events show visibility boundaries, not process boundaries"
    source: "Chunk 1:988-994"

  - entity_type: "Task Instance"
    identity_criteria: "Actor and Entity df-paths meet, synchronize over consecutive events, diverge, with at least one having no other events in between"
    boundary_cases: "Interruptions (like R2's context switch) create separate task instances. What if actor works on multiple entities simultaneously?"
    source: "Chunk 2:621-627"

  - entity_type: "Process Execution"
    identity_criteria: "NOT defined as primitive. Classical 'case' is just one entity type among many"
    boundary_cases: "The paper explicitly asks 'what exactly IS a process execution in our example?' and shows it cannot be cleanly defined for multi-entity data"
    source: "Chunk 1:135-140"

temporal_modeling:
  - aspect: "Event Timestamps"
    approach: "Each event has a timestamp e.time from a totally ordered domain Val_time"
    mechanism: "Timestamps establish local ordering within entity df-paths"
    source: "Chunk 1:198-199, 205-206"

  - aspect: "Directly-Follows Semantics"
    approach: "e1 directly-follows e2 for entity n iff e1.time < e2.time and no other n-correlated event in between"
    mechanism: "Local temporal ordering per entity rather than global ordering"
    source: "Chunk 1:527-529"

  - aspect: "Delay Calculation"
    approach: "e.time - ei.time for each predecessor ei"
    mechanism: "Used to identify which entity/event delayed synchronization the most"
    source: "Chunk 2:235-241"

  - aspect: "Performance Spectrum Visualization"
    approach: "Time on x-axis shows when entities enter/exit activities"
    mechanism: "Reveals waiting times, throughput, overtaking, batching patterns"
    source: "Chunk 2:520-577"

  - aspect: "Dynamic Relations"
    approach: "Acknowledged but not fully addressed"
    mechanism: "References XOC event logs [39,40] for modeling dynamically changing relationships"
    source: "Chunk 1:339-342"
    limitations: "'We have to ignore this aspect in the remainder' - gap in current approach"

agency_spectrum:
  - agent_type: "Human Worker (Actor)"
    capabilities: "Executes activities, makes decisions (e.g., bundling orders), performs context switches, follows routines"
    constraints: "Bounded by organizational policies. Can make mistakes (wrong supplier order). Has specializations"
    source: "Chunk 1:83-84, Chunk 2:601-648"

  - agent_type: "Machine (Automated Warehouse)"
    capabilities: "Stores, retrieves, scans items. Generates events"
    constraints: "Follows fixed policies (FIFO for some queues). No intentional decision-making visible"
    source: "Chunk 1:52, 83-84, Chunk 2:431-436"

  - agent_type: "Entity as Passive Participant"
    capabilities: "Is created, updated, completed by events. 'Passes through' activities"
    constraints: "No agency attributed to Orders, Items, Invoices. They are worked ON, not working"
    source: "Chunk 2:163-177"

  - agent_type: "Process/System"
    capabilities: "Enforces policies (e.g., ship only if at most one unpaid invoice). Schedules (pickups at 15:00)"
    constraints: "Emergent from entity interactions. Not explicitly modeled as an agent"
    source: "Chunk 1:77-80"

knowledge_representation:
  - mechanism: "Labeled Property Graph"
    formalism: "Neo4j graph database with Cypher queries"
    reasoning: "Graph pattern matching, path queries, aggregation. No formal logic reasoning"
    source: "Chunk 1:182-184, 601-603"

  - mechanism: "Event Knowledge Graph Schema"
    formalism: "Node labels {Event, Entity}, relationship labels {df, corr}, properties on nodes and relationships"
    reasoning: "Type-based filtering, entity-specific df-paths, df-relationship properties"
    source: "Chunk 1:624-655"

  - mechanism: "Derived Entities and Relations"
    formalism: "Reification of relations as new Entity nodes with 'derived' relationships to source entities"
    reasoning: "Enables treating inter-entity behavior as first-class"
    source: "Chunk 1:893-906"

  - mechanism: "Multi-Layer Extension"
    formalism: "Additional node labels (TaskInstance, Task, Class) with contains/observes relationships"
    reasoning: "Aggregation and abstraction while maintaining traceability"
    source: "Chunk 2:698-761"

  - mechanism: "Process Models"
    formalism: "Synchronous proclets (multi-entity Petri nets), object-centric Petri nets, DCR graphs mentioned"
    reasoning: "Discovered from df-paths per entity type, composed via synchronization"
    source: "Chunk 2:869-931, Chunk 3:17-45"

emergence_indicators:
  - phenomenon: "Process Fabric"
    mechanism: "Individual entity behaviors weave together into a complex network via shared events"
    evidence: "'The behavior itself is a larger fabric of multiple entities that are inter-related and inter-twined over time' (Chunk 1:148-149)"
    source: "Chunk 1:148-152"

  - phenomenon: "Bottleneck Cascades"
    mechanism: "Delays propagate through delay chains. One entity's delay affects synchronizing entities"
    evidence: "Update SO delayed delivery of items Y1, Y2 needed for both O1 and O2, causing delay cascade"
    source: "Chunk 2:304-308"

  - phenomenon: "Dynamic Bottlenecks"
    mechanism: "Short-term performance anomalies emerge from system-level behavior"
    evidence: "'How performance anomalies cascade through a process' (Chunk 2:866-868)"
    source: "Chunk 2:863-868"

  - phenomenon: "Queue Behavior"
    mechanism: "Activity-as-Entity reveals waiting space between activities"
    evidence: "FIFO violations visible in Performance Spectrum - X3 overtaken by X1, X2; Y1 overtaken by Y2"
    source: "Chunk 2:524-526"

  - phenomenon: "Task Patterns"
    mechanism: "Larger 'units of work' emerge from synchronization of Actor and Entity df-paths"
    evidence: "R4 always performs Pack Shipment then Ship as a unit. R2 follows cyclic structured behavior"
    source: "Chunk 2:619-621, 755-756"

integration_surfaces:
  - surface: "OCEL (Object-Centric Event Logs)"
    connects_to: ["Definition 2 explicitly cites OCEL", "Multi-entity event data model"]
    alignment_quality: "Strong - paper formalizes OCEL in graph terms. Uses 'entity' instead of 'object' for generality"
    source: "Chunk 1:236-239"

  - surface: "Classical Process Mining"
    connects_to: ["Event logs", "DFG", "Inductive Miner"]
    alignment_quality: "Extends/replaces - shows classical approaches fail for multi-entity data, proposes alternative"
    source: "Chunk 1:13-16, 91-92, 458-461"

  - surface: "Knowledge Graphs"
    connects_to: ["Labeled Property Graphs", "Neo4j", "Cypher"]
    alignment_quality: "Good - adopts LPG formalism. Mentions RDF lacks relationship properties needed for df"
    source: "Chunk 1:550-552, 681-682"

  - surface: "Petri Nets"
    connects_to: ["Synchronous proclets", "Object-centric Petri nets", "Colored Petri nets"]
    alignment_quality: "Partial - proclets compose per-entity-type nets. Paper notes limitations for unstructured interactions"
    source: "Chunk 2:885-914, Chunk 3:17-32"

  - surface: "Artifact-Centric Process Models"
    connects_to: ["Multi-viewpoint DFG", "Artifact lifecycle discovery"]
    alignment_quality: "Strong alignment with artifact-centric tradition. References [41,46]"
    source: "Chunk 2:367"

  - surface: "Ontology-Based Data Access"
    connects_to: ["OnProm tool", "Ontologies for log extraction"]
    alignment_quality: "Mentioned as technique for incorporating domain knowledge in extraction. References [6,7]"
    source: "Chunk 2:856-857"

  - surface: "Routines Research"
    connects_to: ["Task instances", "Actor patterning", "Goh & Pentland"]
    alignment_quality: "Novel connection - applies organizational research concepts to process mining"
    source: "Chunk 2:647-648"

gaps_and_tensions:
  - gap_type: "Omission"
    description: "Dynamic relations between entities not addressed"
    implications: "Cannot model when Order O1 BECOMES related to Item X1 (only at e27). Relations are static snapshots"
    source: "Chunk 1:338-342 - 'We have to ignore this aspect in the remainder'"

  - gap_type: "Underspecified"
    description: "Multiple dynamics over multiple entities (top-right quadrant of Fig. 20)"
    implications: "Open question how to analyze multiple actors working on multiple entities simultaneously"
    source: "Chunk 2:845-846"

  - gap_type: "Omission"
    description: "No governance/constraint layer"
    implications: "Policies like 'ship only if at most one unpaid invoice' mentioned but not formalized"
    source: "Chunk 1:77-80 - described in natural language only"

  - gap_type: "Tension"
    description: "Class nodes vs Entity nodes for Activity"
    implications: "Two different semantics when treating Activity as aggregation target vs entity type. Paper acknowledges semantic difference but both coexist"
    source: "Chunk 2:496-501"

  - gap_type: "Limitation"
    description: "Entity interactions often produce overly complex models"
    implications: "Proclets describing inter-entity behavior tend to be unstructured. Declarative models suggested as alternative"
    source: "Chunk 3:25-32"

  - gap_type: "Omission"
    description: "No explicit agent/intentionality model"
    implications: "Actors are just another entity type. No distinction between intentional agents and passive objects except by interpretation"
    source: "Implicit - never discussed"

  - gap_type: "Technical Gap"
    description: "Constructing event knowledge graphs from relational databases while preserving entities"
    implications: "Existing conversion techniques create entity nodes from records, not event nodes. Needs new methods"
    source: "Chunk 2:849-852"

  - gap_type: "Open Question"
    description: "True process discovery with precise semantics from event knowledge graphs"
    implications: "Multi-entity DFG discovery works, but getting models with behavioral semantics remains unaddressed"
    source: "Chunk 2:869-874"

empirical_grounding:
  - type: "Running Example"
    domain: "Retail order fulfillment"
    scale: "2 orders, 5 items, 2 supplier orders, 34 events (synthetic but realistic)"
    findings: "Demonstrates convergence/divergence problems, delay analysis, task detection"
    source: "Chunk 1:37-80, Table 1"

  - type: "Public Datasets"
    domain: "BPI Challenges 2014-2019"
    scale: "Multiple real-world datasets with millions of events"
    findings: "Event knowledge graphs constructed and made available as datasets [19-24]"
    source: "Chunk 1:962-963, Chunk 3:112-123"

  - type: "Implementation"
    domain: "Neo4j graph database"
    scale: "Complete Cypher query implementation"
    findings: "All concepts implemented and available on GitHub"
    source: "Chunk 1:182-184, Chunk 3:132"

  - type: "Visual Analytics Tool"
    domain: "Performance Spectrum Miner"
    scale: "Production tool"
    findings: "Performance Spectrum implemented as visual analytics tool [15]"
    source: "Chunk 2:590-592"

discovery_notes:
  surprises:
    - "The paper treats Activity-as-Entity differently from Activity-as-Class with explicit semantic distinction"
    - "Queue structure EMERGES from treating Activity as Entity - not designed in but discovered"
    - "Connection to routines research (Goh & Pentland) bridges organizational theory and process mining"
    - "Petri's principle cited: 'most events happen due to synchronous interaction of two or more entities' - grounding in concurrency theory"

  unexpected_connections:
    - "Performance Spectrum relates to queueing theory and operations research"
    - "Task instance detection connects to work psychology and ergonomics concepts"
    - "Proclets with synchronization edges resemble distributed systems formalisms"

  tensions_with_other_frameworks:
    - "Rejects case-centric assumption fundamental to classical process mining"
    - "Uses graphs instead of ontology languages - pragmatic rather than formal semantics"
    - "Actors as entities rather than agents - no intentionality commitment"

  key_quotes:
    - "'The behavior itself is a larger fabric of multiple entities that are inter-related and inter-twined over time' (Chunk 1:148-149)"
    - "'Most events happen due to synchronous interaction of two or more entities, and most physical entities are never created from nothing and never disappear into nothing' (Chunk 2:191-193)"
    - "'What exactly IS a process execution in our example?' (Chunk 1:135)"

quality_checklist:
  used_paper_terminology: true
  novel_concepts_captured: 9
  gaps_found: 8
  surprises_noted: 4
  chunk_references: true
  no_category_forcing: true
  nuance_preserved: true
---

# Process Mining over Multiple Behavioral Dimensions with Event Knowledge Graphs

## Summary

This paper introduces **event knowledge graphs** as a data structure for process mining over event data involving multiple entities. The core insight is that classical process mining's assumption of a unique case identifier fails for multi-entity processes, introducing **convergence** (false ordering between unrelated events) and **divergence** (event duplication across cases).

The solution: replace global case-based traces with **local directly-follows relations per entity**. Each event can be correlated to multiple entities, and each entity has its own df-path through events. These paths form a **fabric** of interweaving behaviors that meet at shared events (synchronization points).

## Key Contributions

### 1. Event Knowledge Graph Formalism
- Labeled property graph with Event and Entity nodes
- corr relationships for event-entity correlation
- df relationships for local directly-follows (carrying entity reference)
- Formal definitions 1-13 building from event tables to complete graphs

### 2. Behavioral Analysis Primitives
- **Selection**: Keep entities, get their correlated events
- **Projection**: Keep events, recompute df-relationships
- **Aggregation**: Events to Classes, lift df-relationships
- **Delay analysis**: delay*(e) for root cause identification

### 3. Multi-Dimensional Extensions
- **Activity as Entity**: Reveals queue structure between activities
- **Actor as Entity**: Reveals task instances and work patterns
- **Derived Entities**: Reifies inter-entity relations for interaction analysis
- **Multi-layer graphs**: Event -> TaskInstance -> Task -> Class

### 4. Process Discovery
- Multi-entity directly-follows graphs
- Synchronous proclets (Petri nets with synchronization edges)
- Object-centric Petri nets mentioned as alternative

## Novel Terminology

| Term | Classical Equivalent | Key Difference |
|------|---------------------|----------------|
| Entity | Case | Any correlated identifier, not privileged |
| df-path | Trace | Per-entity, can share events with other paths |
| Correlation | Case attribute | Event to multiple entities |
| Local df | Global df | Computed per entity |
| Fabric | Log | Network of interweaving paths |
| Derived Entity | - | Reified relation becoming entity |
| Task Instance | - | Emergent unit of actor-entity work |

## Architectural Pattern

The paper defines a three-step construction:
1. **Event nodes** from table records
2. **Entity inference** from attribute values + correlation relationships
3. **df inference** from temporal ordering per entity

Extended by:
4. **Relation inference** between entities
5. **Reification** of relations into derived entities
6. **Aggregation** into Class/Task/TaskInstance layers

## Critical Insights for Synthesis

1. **No privileged perspective**: Any entity type can be the "case". All are equally valid views
2. **Synchronization is key**: Shared events where df-paths meet reveal process structure
3. **Queues emerge**: Treating Activity as Entity reveals waiting space
4. **Tasks emerge**: Synchronization patterns between Actor and Entity reveal work units
5. **Delay chains**: Following predecessors backward identifies bottleneck sources
6. **Graph is extensible**: New events can be added locally without rebuilding

## Gaps for Future Work

- Dynamic relations (when entities BECOME related)
- Multiple dynamics over multiple entities
- Process discovery with precise behavioral semantics
- Constructing from relational DBs while preserving entity structure
- Governance/constraint modeling
