---
paper_id: "10-OC-PM"
title: "OC-PM: analyzing object-centric event logs and process models"
authors: ["Alessandro Berti", "Wil M. P. van der Aalst"]
year: 2022
venue: "International Journal on Software Tools for Technology Transfer"
doi: "10.1007/s10009-022-00668-w"

extraction_version: "2.0"
extraction_date: "2025-12-31"
extraction_approach: "DISCOVERY"

ontological_primitives:
  - term: "Event"
    definition: "An occurrence with identifier, activity, timestamp, and related objects. Formally: e in E with functions pi_act(e), pi_time(e), pi_omap(e)"
    source: "Chunk 1:236-251, Def 2 and Def 7"
    unique_aspects: "Events are NOT owned by cases - they can relate to multiple objects simultaneously. This breaks the traditional one-event-per-case assumption."

  - term: "Object"
    definition: "An entity with identifier, type, and attribute values. Formally: o in O with pi_otyp(o) and pi_ovmap(o)"
    source: "Chunk 1:448-475, Def 7"
    unique_aspects: "Objects are first-class citizens with their own lifecycles, not just case identifiers. Objects have typed attributes independent of events."

  - term: "Object Type"
    definition: "A classification of objects (OT subset of U_ot). Examples: order, item, package, delivery"
    source: "Chunk 1:440-441, 470-471"
    unique_aspects: "Types provide polymorphism - the same event can involve objects of different types simultaneously (e.g., order and items)."

  - term: "Activity"
    definition: "A named action that occurs in an event. Formally: element of U_act"
    source: "Chunk 1:226-227"
    unique_aspects: "Activities are shared across object types - same activity can appear in multiple object lifecycles simultaneously."

  - term: "Lifecycle"
    definition: "The sequence of events to which an object is related: lif(o) = case_FL(L,pi_otyp(o))(o)"
    source: "Chunk 1:601-621, Def 10"
    unique_aspects: "Critical primitive - each object has its OWN lifecycle as a first-class sequence, derived via flattening. This is NOT a global process but object-local."

  - term: "Case (Traditional)"
    definition: "A collection of events related to a particular process execution, with single case identifier"
    source: "Chunk 1:47-52, 205-212, Def 2"
    unique_aspects: "Explicitly deprecated as insufficient - paper exists to overcome case-centric limitations."

  - term: "Directly-Follows Relationship"
    definition: "Ordered succession between activities in object lifecycles, captured as typed edges in OC-DFG"
    source: "Chunk 1:300-386, Def 4-5"
    unique_aspects: "In OC-PM, directly-follows is typed by object type - same activity pair can have multiple edges for different types."

structural_patterns:
  - pattern_name: "Object-Event Many-to-Many"
    structure: "Events <--> Objects (M:N relationship via pi_omap)"
    instances:
      - "One event 'create order' relates to 1 order + 2 items simultaneously (Chunk 1:84-86)"
      - "Same event logged once, visible in multiple object lifecycles"
    source: "Chunk 1:82-86, 502-505, Def 7"
    significance: "Fundamental departure from traditional process mining. Eliminates convergence problem."

  - pattern_name: "Flattening-Collation Pipeline"
    structure: "Object-centric log -> [Flatten per type] -> [Process per type] -> [Collate results]"
    instances:
      - "OC-DFG discovery: flatten, discover DFG per type, combine into multigraph"
      - "Object-centric Petri net discovery uses same pattern"
    source: "Chunk 1:743-791, Def 16"
    significance: "Bridges object-centric to traditional techniques. Enables reuse of existing algorithms."

  - pattern_name: "Typed Multigraph"
    structure: "Nodes (activities) + Typed edges (activity, object_type, activity)"
    instances:
      - "OC-DFG: F subset of N x OT x N - edges carry type information"
      - "Start/end nodes per object type: n_S,ot and n_E,ot"
    source: "Chunk 1:764-786, Def 15"
    significance: "Allows simultaneous visualization of multiple object lifecycles with their intersections."

  - pattern_name: "Convergence-Divergence Duality"
    structure: "Convergence (event belongs to multiple cases) vs Divergence (case has multiple instances of same activity)"
    instances:
      - "Sales order: order items have convergent packing events"
      - "Order has divergent collection/packing for different items"
    source: "Chunk 1:69-78"
    significance: "These twin problems motivated the entire object-centric paradigm. Traditional approaches fail on both."

  - pattern_name: "Three-Level Counting"
    structure: "Events (E) / Unique Objects (UO) / Total Objects (TO) as parallel metrics"
    instances:
      - "Activity metrics: AF1=Events, AF2=Unique Objects, AF3=Total Objects"
      - "Path metrics: EC=Event Couples, UO=Objects with path, TO=Total occurrences"
    source: "Chunk 1:882-948, Def 18-19"
    significance: "Recognizes that counting differs by granularity - same activity can have very different E vs UO vs TO."

novel_concepts:
  - concept: "Object-Centric Event Log (OCEL)"
    definition: "Event log where each event relates to multiple objects of potentially different types, with formal structure L = (E, AN, AV, AT, OT, O, pi_typ, pi_act, pi_time, pi_vmap, pi_omap, pi_otyp, pi_ovmap, <=)"
    novelty_claim: "Replaces case-centric logs entirely. No case notion required. Events are not replicated."
    source: "Chunk 1:79-110, 448-528, Def 7"

  - concept: "Flattening Operation"
    definition: "Transform object-centric log to traditional log by selecting one object type: FL(L, ot)"
    novelty_claim: "Creates bridge to traditional process mining while preserving object semantics. Formally defined projection."
    source: "Chunk 1:555-598, Def 9"

  - concept: "Object-Centric Directly-Follows Multigraph (OC-DFG)"
    definition: "Process model with activities as nodes and typed edges: (A, OT, N, F, pi_freqn, pi_freqe)"
    novelty_claim: "Extends DFG to show multiple object type perspectives simultaneously. Edges are triples (node, type, node)."
    source: "Chunk 1:758-800, Def 15-16"

  - concept: "Lifecycle as Object-Local Process"
    definition: "Each object has its own event sequence (lifecycle) independent of global process"
    novelty_claim: "Shifts from process-centric to object-centric view. Process emerges from object interactions."
    source: "Chunk 1:601-627, Def 10"

  - concept: "Model-Independent Conformance Checking"
    definition: "Conformance rules based on log properties alone: CC1 (number of related objects), CC2 (lifecycle duration)"
    novelty_claim: "Conformance without explicit process model. Statistical deviation detection."
    source: "Chunk 1:959-991, Chunk 2:71-112, Def 20"

semantic_commitments:
  - commitment: "Object-Centric vs Case-Centric"
    position: "Object-centric - events belong to objects, not cases"
    implications: "No case identifier required. No event replication. Many-to-many event-object relationships native."
    source: "Chunk 1:79-110"

  - commitment: "Lifecycle Individuation"
    position: "Objects have individual lifecycles that are first-class entities"
    implications: "Process model is emergent from object lifecycles, not primary. Each object type has distinct lifecycle patterns."
    source: "Chunk 1:601-627"

  - commitment: "Type-Preserving Abstraction"
    position: "Object types are preserved through all transformations (flattening, discovery)"
    implications: "Type information flows through entire analysis pipeline. Enables type-specific filtering and metrics."
    source: "Chunk 1:727-733, Def 14 F7"

  - commitment: "Event Atomicity"
    position: "Events are atomic occurrences with single timestamp"
    implications: "No duration for events themselves. Duration only at lifecycle level. Instantaneous event model."
    source: "Chunk 1:229-232"

boundary_definitions:
  - entity_type: "Object"
    identity_criteria: "Unique object identifier (o in U_o) with single type assignment"
    boundary_cases: "When does an object 'end'? Paper uses end activity but doesn't address object death/creation formally."
    source: "Chunk 1:433-434, 510-512"

  - entity_type: "Event"
    identity_criteria: "Unique event identifier (e in U_e) with timestamp"
    boundary_cases: "Events at same timestamp? Total order <= implies deterministic ordering even for simultaneous events."
    source: "Chunk 1:220-221, 526-527"

  - entity_type: "Object Lifecycle"
    identity_criteria: "Bounded by first and last events related to the object"
    boundary_cases: "Incomplete lifecycles (improper termination) detected via end activity analysis. No explicit 'death' event required."
    source: "Chunk 1:616-627"

  - entity_type: "Process Model Boundary"
    identity_criteria: "Start/end nodes per object type in OC-DFG"
    boundary_cases: "Objects may have different start/end activities. Process boundary is type-dependent, not global."
    source: "Chunk 1:773-779"

temporal_modeling:
  - aspect: "Event Timestamps"
    approach: "Single timestamp per event from totally ordered universe U_timest"
    mechanism: "pi_time: E -> U_timest with difference operation (- as seconds between timestamps)"
    source: "Chunk 1:229-232, 244-245"

  - aspect: "Lifecycle Duration"
    approach: "Computed as difference between last and first event timestamps"
    mechanism: "pi_time(lif(o)(|lif(o)|)) - pi_time(lif(o)(1)) gives lifecycle span"
    source: "Chunk 1:980-989, Def 20 CC2"

  - aspect: "Event Ordering"
    approach: "Total order on events (antisymmetric, transitive, connex)"
    mechanism: "<= relation on E provides deterministic sequencing"
    source: "Chunk 1:250-251, 526-527"

  - aspect: "Trace Sequencing"
    approach: "Activity sequences per object: trace(o) as ordered list of activities"
    mechanism: "Derived from lifecycle via pi_act application"
    source: "Chunk 1:281, 612-614"

agency_spectrum:
  - agent_type: "Resource (Implicit)"
    capabilities: "Executes activities. Attribute 'resource' appears in event attributes."
    constraints: "Not formalized as first-class entity. Just an attribute value."
    source: "Chunk 1:424-425 (resource in U_att)"

  - agent_type: "Information System"
    capabilities: "Generates event data. SAP mentioned as source."
    constraints: "No agency model for the system itself. Treated as passive data source."
    source: "Chunk 1:23-24, Chunk 2:474-475"

  - agent_type: "NOTABLE ABSENCE"
    capabilities: "No agent/actor primitive in OCEL"
    constraints: "Paper treats who performs activities as optional attribute, not core ontology"
    source: "Implicit - no Agent in Def 7"

knowledge_representation:
  - mechanism: "Object-Centric Event Log (OCEL)"
    formalism: "JSON-OCEL, XML-OCEL formats; formal tuple definition"
    reasoning: "No inference. Query/filter operations. Statistical aggregation."
    source: "Chunk 1:529-533"

  - mechanism: "Directly-Follows Multigraph"
    formalism: "Typed directed graph with frequency annotations"
    reasoning: "Path analysis, frequency-based filtering, conformance deviation detection"
    source: "Chunk 1:758-800"

  - mechanism: "Flattened Traditional Log"
    formalism: "XES format (for export to traditional tools)"
    reasoning: "Enables use of existing process mining algorithms"
    source: "Chunk 2:284-285"

  - mechanism: "Graph Database Storage"
    formalism: "Neo4j mentioned for multi-dimensional event data (related work)"
    reasoning: "Path queries, graph patterns - but scalability issues noted"
    source: "Chunk 2:403-416"

emergence_indicators:
  - phenomenon: "Process Model from Object Lifecycles"
    mechanism: "OC-DFG emerges from aggregating individual object lifecycles via flattening-collation"
    evidence: "No explicit process defined; model discovered from object behavior patterns"
    source: "Chunk 1:743-800"

  - phenomenon: "Object Interactions"
    mechanism: "Events that relate to multiple objects reveal inter-object dependencies"
    evidence: "Single event touching order + items shows implicit coordination"
    source: "Chunk 1:84-86, 109-110"

  - phenomenon: "Convergence/Divergence as Systemic Properties"
    mechanism: "These problems only visible at system level, not individual object level"
    evidence: "Require cross-object view to detect; motivate entire paradigm shift"
    source: "Chunk 1:69-78"

integration_surfaces:
  - surface: "Traditional Process Mining"
    connects_to: ["XES event logs", "ProM framework", "DFG discovery", "Petri nets"]
    alignment_quality: "Good via flattening operation. OCEL can be projected to traditional logs."
    source: "Chunk 1:555-598, Chunk 2:288-306"

  - surface: "Petri Net Formalism"
    connects_to: ["Colored Petri nets", "Object-centric Petri nets", "Token-based replay"]
    alignment_quality: "Extended with object-centric semantics. Places and arcs typed by object type."
    source: "Chunk 2:376-450"

  - surface: "Graph Databases"
    connects_to: ["Neo4j", "Property graphs"]
    alignment_quality: "Partial - OCEL can be stored in graph DB but scalability concerns noted"
    source: "Chunk 2:403-416"

  - surface: "Artifact-Centric Approaches"
    connects_to: ["Business artifacts", "Artifact lifecycle models"]
    alignment_quality: "Conceptually related but OCEL more general (not dependent on database schema)"
    source: "Chunk 2:315-352"

  - surface: "ABSENT: Foundational Ontologies"
    connects_to: []
    alignment_quality: "No connection to UFO, BFO, DOLCE, PROV-O. Paper is purely technical, not ontologically grounded."
    source: "Implicit - no ontology references"

gaps_and_tensions:
  - gap_type: "Omission"
    description: "No agent/actor as first-class primitive"
    implications: "Cannot model who does what natively. Resource is just an attribute. Misses PROV-O Agent concept."
    source: "Implicit - absent from Def 7"

  - gap_type: "Omission"
    description: "No goal/intention modeling"
    implications: "Objects exist and have lifecycles but no teleological grounding. Why does the process exist?"
    source: "Implicit - not discussed"

  - gap_type: "Omission"
    description: "No rule/constraint formalization beyond statistical deviation"
    implications: "CC1/CC2 are statistical, not semantic. No business rule language."
    source: "Chunk 1:959-991"

  - gap_type: "Tension"
    description: "Flattening loses multi-object event semantics"
    implications: "Flattening to single type loses the very relationships OCEL was designed to capture. Bridge technique sacrifices novelty."
    source: "Chunk 1:555-598"

  - gap_type: "Underspecified"
    description: "Object creation/deletion not formalized"
    implications: "Objects just 'are' - no birth/death semantics. Lifecycle has start/end activities but no ontological status for object existence."
    source: "Chunk 1:601-627"

  - gap_type: "Underspecified"
    description: "Object relationships beyond event co-occurrence"
    implications: "If item belongs-to order, this is only implicit via shared events. No explicit object-object relationships."
    source: "Implicit - not in OCEL definition"

  - gap_type: "Tension"
    description: "Scalability of graph database storage"
    implications: "Paper notes Neo4j performance is 'disappointing' for process mining tasks despite conceptual fit"
    source: "Chunk 2:413-416"

  - gap_type: "Acknowledged Limitation"
    description: "No model-based conformance checking"
    implications: "Paper only provides model-independent conformance. Comparing log to OC-DFG not formalized."
    source: "Chunk 2:502-507"

empirical_grounding:
  - type: "Tool Implementation"
    domain: "General (web-based OC-PM tool)"
    scale: "Available at ocpm.info; supports JSON-OCEL and XML-OCEL"
    findings: "Demonstrates feasibility of proposed techniques"
    source: "Chunk 2:162-285, Section 4"

  - type: "Framework Integration"
    domain: "ProM process mining framework"
    scale: "Plugin implementation (OCELStandard package)"
    findings: "Integration with established tool ecosystem"
    source: "Chunk 2:288-306"

  - type: "Illustrative Example"
    domain: "Sales order management"
    scale: "Synthetic example (Table 1, Table 2, Figure 1)"
    findings: "Demonstrates orders, items, packages, deliveries - multiple object types interacting"
    source: "Chunk 1:50-52, 84-87, 166-182"

  - type: "NOTABLE ABSENCE"
    domain: "Real-world evaluation"
    scale: "None"
    findings: "Paper explicitly acknowledges: 'assessment of the proposed techniques on real-life event logs is missing'"
    source: "Chunk 2:505-506"

surprises:
  - surprise: "No Agent Primitive Despite Process Focus"
    description: "Given this is process mining, the absence of agent/resource as first-class entity is striking. PROV-O has Agent prominently; OCEL does not."
    implication: "OCEL is purely about what happens to objects, not who makes it happen."

  - surprise: "Flattening Undermines the Core Innovation"
    description: "The paper's central innovation (many-to-many event-object) is deliberately lost in the discovery algorithm via flattening. The bridge to traditional techniques sacrifices what makes OCEL novel."
    implication: "True object-centric discovery algorithms remain future work."

  - surprise: "No Ontological References"
    description: "Paper cites extensive process mining literature but zero foundational ontology work (no UFO, BFO, DOLCE, even PROV-O). Purely technical treatment."
    implication: "Opportunity for ontological grounding of OCEL concepts."

  - surprise: "Objects Without Relationships"
    description: "OCEL defines objects but no explicit object-to-object relationships. If an item 'belongs to' an order, this is only recoverable via shared event participation."
    implication: "Missing structural layer that could be added (see OCEL 2.0 which addresses this)."

synthesis_potential:
  - connection: "OCEL Event to PROV-O Activity"
    insight: "OCEL Events could be mapped to PROV-O Activities, with OCEL Objects as PROV-O Entities. Missing piece: who is the Agent?"

  - connection: "Object Lifecycle to UFO Perdurant"
    insight: "An object's lifecycle is essentially a perdurant (temporal entity). The object itself is an endurant that participates in this perdurant."

  - connection: "Object Type to UFO Kind/Category"
    insight: "OCEL object types could be grounded in UFO sortal types. Order, Item, Package are Kinds with lifecycle patterns."

  - connection: "Event-Object Relation to UFO Participation"
    insight: "pi_omap (event-to-objects) is a participation relation. Objects participate in events."

---

# OC-PM: Object-Centric Process Mining - V2 Discovery Extraction

## Paper Overview

This paper introduces **Object-Centric Process Mining (OC-PM)**, a paradigm shift in process mining that replaces case-centric event logs with object-centric event logs (OCEL). The core innovation is allowing events to relate to multiple objects of different types simultaneously, solving the long-standing **convergence** and **divergence** problems in traditional process mining.

## Key Primitives Discovered

The paper defines a formal ontology for object-centric event data with these irreducible elements:

1. **Event (E)** - Atomic occurrences with activity, timestamp, and object mappings
2. **Object (O)** - Entities with types and attributes, having their own lifecycles
3. **Object Type (OT)** - Classification of objects (order, item, package, etc.)
4. **Activity (Uact)** - Named actions that occur in events
5. **Lifecycle** - Object-local event sequence (first-class concept)

## Structural Innovation

The **many-to-many event-object relationship** (pi_omap: E -> P(O)) is the paper's central structural innovation. This single change enables:
- No event replication (solves convergence)
- No artificial case boundaries (solves divergence)
- Objects as first-class citizens with individual lifecycles

## Process Model: OC-DFG

The **Object-Centric Directly-Follows Multigraph** is a novel process model where:
- Nodes are activities (plus type-specific start/end nodes)
- Edges are triples: (source_node, object_type, target_node)
- Multiple edge types between same activity pair (one per object type)

## Critical Gap: Agency

Despite being about business processes, OCEL has **no agent/actor primitive**. Resources appear only as optional event attributes, not as first-class entities. This is a significant departure from PROV-O which centers Agent alongside Activity and Entity.

## Bridge to Traditional Techniques

The **flattening operation** (FL(L, ot)) projects object-centric logs to traditional logs by selecting one object type. This enables reuse of existing process discovery algorithms but **sacrifices the multi-object semantics** that OCEL was designed to capture.

## Conformance Approach

The paper introduces **model-independent conformance checking** based on statistical deviation:
- CC1: Anomalous number of objects per event
- CC2: Anomalous lifecycle duration

No model-based conformance is provided.

## Integration Opportunity

This paper presents a **technically mature but ontologically ungrounded** framework. Clear opportunities exist to map OCEL concepts to foundational ontologies:
- OCEL Event <-> PROV-O Activity
- OCEL Object <-> PROV-O Entity / UFO Endurant
- Object Lifecycle <-> UFO Perdurant
- (Missing) Agent mapping

## Quality Assessment

- **Surprise Level**: High - The absence of Agent and explicit object-object relationships is unexpected
- **Specificity**: Excellent - Formal definitions with set-theoretic notation throughout
- **Tensions Found**: Yes - Flattening sacrifices core innovation; scalability concerns with graph DBs
- **Gaps Identified**: Yes - Agent, goals, rules, object relationships all missing
- **Novelty**: High - OCEL and OC-DFG are genuinely new contributions
