---
paper_id: "11-Process_Mining_Event_Knowledge_Graphs"
title: "Process Mining over Multiple Behavioral Dimensions with Event Knowledge Graphs"
authors:
  - "Dirk Fahland"
year: 2022
chunks_expected: 3
chunks_read: 3
analysis_complete: true
schema_version: "2.3"

chunk_index:
  1:
    token_count: 13508
    fields_found:
      entity_types: true
      entity_definitions: true
      entity_relationships: true
      entity_count: partial
      abstraction_level: partial
      framework_comparison: true
      methodology: true
      ai_integration: false
      agent_modeling: partial
      agentic_workflows: false
      generative_ai_patterns: false
      agent_ontology_integration: false
      empirical_evidence: partial
      limitations: true
      tools_standards: true
  2:
    token_count: 13678
    fields_found:
      entity_types: true
      entity_definitions: true
      entity_relationships: true
      entity_count: partial
      abstraction_level: partial
      framework_comparison: true
      methodology: true
      ai_integration: false
      agent_modeling: true
      agentic_workflows: false
      generative_ai_patterns: false
      agent_ontology_integration: false
      empirical_evidence: true
      limitations: true
      tools_standards: true
  3:
    token_count: 4389
    fields_found:
      entity_types: partial
      entity_definitions: partial
      entity_relationships: partial
      entity_count: false
      abstraction_level: false
      framework_comparison: true
      methodology: partial
      ai_integration: false
      agent_modeling: partial
      agentic_workflows: false
      generative_ai_patterns: false
      agent_ontology_integration: false
      empirical_evidence: partial
      limitations: partial
      tools_standards: true

entity_types:
  - item: "Event"
    chunk: 1
    lines: "201-206"
    quote: "An event table T = (E, Attr, #) is a set E of events, a set Attr of attribute names with act, time in Attr... Each event e in E records an activity and a timestamp"
  - item: "Entity"
    chunk: 1
    lines: "218-220"
    quote: "An event table with entities types T = (E, Attr, #, ENT) additionally designates one or more attributes ENT as Attr as names of entity types"
  - item: "Entity Types (Order, Supplier Order, Item, Invoice, Payment, Resource)"
    chunk: 1
    lines: "232-233"
    quote: "ENT = {Resource, Order, Supplier Order, Item, Invoice, Payment}"
  - item: "Labeled Property Graph (LPG)"
    chunk: 1
    lines: "574-583"
    quote: "A labeled property graph (LPG) G = (N, R, lambda, #) is a graph with nodes N, and relationships R... Each node n in N carries a label... Each relationship r in R carries a label and defines a directed edge"
  - item: "Event Knowledge Graph"
    chunk: 1
    lines: "624-627"
    quote: "An event knowledge graph (or just graph) is an LPG G = (N, R, lambda, #) with node labels {Event, Entity} and relationship labels {df, corr} indicating 'directly-follows' and 'correlation'"
  - item: "Actor"
    chunk: 2
    lines: "597-601"
    quote: "Workers are performing this actual work. Often called 'resources' in process management literature, we prefer the term Actor used in organizations research, as each actor follows its own behavior."
  - item: "Task Instance"
    chunk: 2
    lines: "621-625"
    quote: "A task instance of an actor R working on an entity X materializes in an event knowledge graph as a specific subgraph over event nodes e1,...,ek: (1) the df-paths of R and X both meet in e1, (2) diverge in ek, (3) synchronize in each event node"
  - item: "Class (aggregated event type)"
    chunk: 2
    lines: "333-338"
    quote: "For each value c in {e.Activity | e in N^Event} of the Activity property that we find among the events in the graph, we create a new node c with label Class (representing the class of events with the same Activity property)"
  - item: "Derived Entity"
    chunk: 1
    lines: "893-896"
    quote: "We reify the relation between two entity types ent1 and ent2 into a new derived entity type (ent1, ent2). That is, we make each pair (n1, n2) in R^related an entity node (n1, n2) in N^Entity"

entity_definitions:
  Event: "A record in an event table that captures an activity name and timestamp. Each event e records which action has been executed at which time. Chunk 1:201-206"
  Entity: "A named object handled by a process, identified by entity type attributes in the event table. Entities can be Orders, Supplier Orders, Items, Invoices, Payments, or Resources. Chunk 1:248-254"
  Entity_Type: "A column in the event table designating a category of entities (e.g., Order, Invoice). Each value in that column refers to a specific entity. Chunk 1:218-220"
  Correlation: "The relationship between an event and an entity. Event e is correlated to entity n if the entity identifier appears in the event's attributes. Chunk 1:265-269"
  Directly_Follows: "Local temporal ordering between events correlated to the same entity. Event e2 directly follows e1 from perspective of n iff both are correlated to n, e1 occurred before e2, and no other event of n occurs in between. Chunk 1:519-529"
  Event_Knowledge_Graph: "A labeled property graph with Event and Entity nodes, plus df (directly-follows) and corr (correlation) relationship types, capturing multi-entity process behavior. Chunk 1:624-627"
  DF_Path: "A path of directly-follows relationships between events for a single entity, analogous to a trace in classical event logs. Chunk 1:667-672"
  Actor: "An organizational entity (human worker or machine) that executes process activities. Follows its own behavioral patterns. Chunk 2:597-601"
  Task_Instance: "A subgraph where an Actor's df-path and an Entity's df-path synchronize over consecutive events, representing a unit of work. Chunk 2:621-625"

entity_relationships:
  - item: "Correlation (corr) - Event to Entity"
    chunk: 1
    lines: "633-635"
    quote: "Every correlation relationship r in R^corr, r = (e, n) is defined from an event node to an entity node, e in N^Event, n in N^Entity"
  - item: "Directly-Follows (df) - Event to Event"
    chunk: 1
    lines: "636-642"
    quote: "Any directly-follows relationship df in R^df, df = (e1, e2) is defined between event nodes e1, e2 in N^Event and refers to a specific entity df.ent = n"
  - item: "Related - Entity to Entity"
    chunk: 1
    lines: "300-302"
    quote: "The relation between ent1 and ent2 in T is R(ent1,ent2) = {(e.ent1, ent2) | e.ent1 != null, e.ent2 != null}"
  - item: "Derived - Derived Entity to Original Entities"
    chunk: 1
    lines: "897-898"
    quote: "For traceability, we add a new relationship d in R^derived with label derived from entity (n1, n2) to n1 and to n2"
  - item: "Observes - Event to Class"
    chunk: 2
    lines: "336-338"
    quote: "We add an observes relationship from each event e to the Class node c in N^Class if e.Activity = c"
  - item: "Contains - TaskInstance to Event"
    chunk: 2
    lines: "714-716"
    quote: "We add a new contains relationship (ti, e) in R^contains from each TaskInstance node ti to each Event node e that is part of the task instance"
  - item: "Synchronization - Multiple entity df-paths meeting in shared event"
    chunk: 2
    lines: "157-160"
    quote: "Two or more entities n1,...,nk synchronize in a shared event e if two or more df-paths of n1,...,nk go through e"

abstraction_level: "Domain/Applied - The paper presents a domain-specific framework for process mining that extends foundational graph theory (labeled property graphs) to the process mining domain. It bridges theoretical graph formalism with practical event data analysis. Chunk 1:16-21"

framework_comparison:
  - item: "Classical Event Logs vs Event Knowledge Graphs"
    chunk: 1
    lines: "119-134"
    quote: "In contrast to classical event logs, Table 1 contains no typical case identifier attribute by which each event is related to one specific process execution. Instead, we see multiple sparsely filled attributes identifying multiple entities"
  - item: "Object-Centric Event Logs (OCEL)"
    chunk: 1
    lines: "236-239"
    quote: "Definition 2 formalizes the object-centric event logs (OCEL) described in Sect. 3.4 of [1]; we here use the more general term 'entity' instead of 'object'"
  - item: "Labeled Property Graphs vs RDF"
    chunk: 1
    lines: "679-682"
    quote: "While the nodes and relationships of Definition 8 can also be encoded in RDF, the df-paths rely on attributes of relationships which are not supported by RDF but by LPGs"
  - item: "Multi-entity DFG vs Artifact-Centric Model"
    chunk: 2
    lines: "366-367"
    quote: "The resulting graph is a multi-entity directly-follows graph, also called multi-viewpoint DFG or artifact-centric model"
  - item: "Proclets vs Object-Centric Petri Nets"
    chunk: 3
    lines: "17-23"
    quote: "Object-centric Petri nets also first discover one Petri net per entity type, then annotate the places and arcs with entity identifiers... However, synchronization by composition prevents explicitly modeling interactions between entities"
  - item: "Declarative Models (DCR Graphs)"
    chunk: 3
    lines: "29-32"
    quote: "Extensions of declarative models such as modular DCR graphs, that apply similar principles as synchronous proclets, could be more suitable"

ai_integration: "NOT_FOUND"

agent_modeling:
  - item: "Actor as autonomous entity"
    chunk: 2
    lines: "597-601"
    quote: "We prefer the term Actor used in organizations research, as each actor follows its own behavior"
  - item: "Actor behavioral patterns"
    chunk: 2
    lines: "605-608"
    quote: "The df-path of R1 synchronizes with any other entity only in one event, and then moves on to the next entity O1, O2, A, B, always performing just a single activity on each"
  - item: "Task execution routines"
    chunk: 2
    lines: "643-648"
    quote: "The df-relationships between task instances also reveal patterns of how work is handed over between actors. For example R1 hands work over to R2 in all Supplier Orders"

agentic_workflows: "NOT_FOUND"

generative_ai_patterns: "NOT_FOUND"

agent_ontology_integration: "NOT_FOUND"

entity_count: "The paper does not specify a fixed number of entity types. The running example uses 7 entity types (Order, Supplier Order, Item, Invoice, Payment, Resource/Actor, and derived entities like Order-Payment). The framework is designed to handle arbitrary numbers of entity types. Chunk 1:83-85"

methodology: "Formal/deductive methodology. The paper builds from formal definitions (event tables, labeled property graphs) to construct event knowledge graphs through inference rules. Three-step construction: (1) create event nodes, (2) infer entities and correlation, (3) infer directly-follows relationships. Chunk 1:693-704"

empirical_evidence:
  - item: "Neo4j implementation and tutorial"
    chunk: 1
    lines: "182-184"
    quote: "All concepts for constructing and analyzing event knowledge graphs presented in this chapter are implemented as Cypher queries on the graph database system Neo4j at https://github.com/multi-dimensional-process-mining/eventgraph_tutorial"
  - item: "Real-life BPI Challenge datasets"
    chunk: 2
    lines: "62-65"
    quote: "to construct event knowledge graphs in a graph database for our running example as well as for various real-life datasets comprising single and multiple event tables; several event knowledge graphs of real-life processes are available"
  - item: "Published datasets"
    chunk: 3
    lines: "112-124"
    quote: "Event Graph of BPI Challenge 2014, 2015, 2016, 2017, 2019. Dataset. Event Data and Queries for Multi-Dimensional Event Data in the Neo4j Graph Database"

limitations:
  - item: "Static vs Dynamic Relations"
    chunk: 1
    lines: "338-342"
    quote: "relations and their cardinalities recovered according to Definition 5 are a static view of the relations obtained by aggregating all observations over time while a process updates relations dynamically"
  - item: "Incompleteness of observation"
    chunk: 2
    lines: "182-193"
    quote: "Both the graph and the data from which it was created may be incomplete. Entities that are 'created' or 'closed' may continue to exist both prior and after the data recorded"
  - item: "Entity interactions complexity"
    chunk: 3
    lines: "25-29"
    quote: "while proclets can describe entity interactions, the behavior of entity interactions tends to be rather unstructured resulting in overly complex models"
  - item: "Open research question on multiple dynamics over multiple entities"
    chunk: 2
    lines: "845-846"
    quote: "How to analyze the combination of multiple dynamics over multiple entities (top right quadrant in Fig. 20) is an open question"

tools_standards:
  - item: "Neo4j Graph Database"
    chunk: 1
    lines: "182-183"
    quote: "implemented as Cypher queries on the graph database system Neo4j"
  - item: "Cypher Query Language"
    chunk: 2
    lines: "60-61"
    quote: "All steps of the method can be implemented as a series of Cypher queries"
  - item: "Labeled Property Graphs (LPG)"
    chunk: 1
    lines: "550-552"
    quote: "A typed graph data model such as labeled property graphs allows to distinguish different types of nodes (events, entities) and relationships (directly-follows, correlated-to)"
  - item: "Object-Centric Event Logs (OCEL)"
    chunk: 1
    lines: "236-237"
    quote: "Definition 2 formalizes the object-centric event logs (OCEL)"
  - item: "RDF (comparison)"
    chunk: 1
    lines: "681"
    quote: "the nodes and relationships of Definition 8 can also be encoded in RDF"
  - item: "Petri Nets / Synchronous Proclets"
    chunk: 2
    lines: "884-886"
    quote: "using a multi-entity extension for Petri nets, called synchronous proclets"
  - item: "Object-Centric Petri Nets"
    chunk: 3
    lines: "17-20"
    quote: "Object-centric Petri nets also first discover one Petri net per entity type, then annotate the places and arcs with entity identifiers"
  - item: "Inductive Miner (IM)"
    chunk: 1
    lines: "458-460"
    quote: "the corresponding process model discovered with the Inductive Miner (IM) annotated with the mean waiting times"
---

# Process Mining over Multiple Behavioral Dimensions with Event Knowledge Graphs

## Summary

This paper by Dirk Fahland from Eindhoven University of Technology introduces **event knowledge graphs** as a data structure for process mining over multiple entities. The key contribution is addressing the limitations of classical process mining which relies on a single case identifier, leading to false behavioral information (convergence and divergence) when analyzing multi-entity processes.

## Key Concepts

### Event Knowledge Graph Structure
- **Event nodes**: Capture activity executions with timestamps
- **Entity nodes**: Represent objects handled by the process (Orders, Items, Invoices, etc.) and actors/resources
- **Correlation relationships (corr)**: Link events to the entities they affect
- **Directly-follows relationships (df)**: Capture local temporal ordering per entity

### Core Innovation: Local Directly-Follows
Instead of a global directly-follows relation based on a single case identifier, the paper defines a **local directly-follows relation per entity**. This prevents false behavioral information that arises when flattening multi-entity data into sequential traces.

### Multi-Dimensional Analysis
The framework enables analysis across:
1. **Control-flow dimension**: Traditional process behavior
2. **Actor dimension**: How workers organize and execute tasks
3. **System/Queue dimension**: How entities pass through activity "stations"

### Aggregation and Discovery
- Events can be aggregated into **Class nodes** to create multi-entity directly-follows graphs
- **Task instances** emerge as subgraphs where actor and entity df-paths synchronize
- Supports discovery of **synchronous proclet models** and **object-centric Petri nets**

## Relevance to Research Questions

### Entity Types and Relationships
The paper provides formal definitions for:
- Events, entities, entity types
- Correlation and directly-follows relationships
- Derived entities for modeling inter-entity interactions

### Framework Comparison
Compares event knowledge graphs to:
- Classical event logs (single case identifier)
- Object-centric event logs (OCEL)
- RDF (lacks relationship properties needed for df-paths)
- Artifact-centric models and proclets

### Agent/Actor Modeling
While not AI-focused, the paper models human actors as autonomous entities with their own behavioral patterns, providing a foundation for understanding how agents (human or artificial) interact with processes.

## Technical Implementation

All concepts are implemented as:
- Cypher queries on Neo4j graph database
- Available at: https://github.com/multi-dimensional-process-mining/eventgraph_tutorial
- Real-life datasets from BPI Challenges 2014-2019

## Limitations Noted

1. Relations are captured statically (aggregated over time) vs. dynamic updates
2. Observation windows may be incomplete
3. Entity interaction behavior can be complex/unstructured
4. Combining multiple dynamics over multiple entities remains an open question
