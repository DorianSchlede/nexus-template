---
paper_id: "09-OCEL_20_Specification"
title: "OCEL (Object-Centric Event Log) 2.0 Specification"
authors: ["Alessandro Berti", "Istvan Koren", "Jan Niklas Adams", "Gyunam Park", "Benedikt Knopp", "Nina Graves", "Majid Rafiei", "Lukas Liss", "Leah Tacke Genannt Unterberg", "Yisong Zhang", "Christopher Schwanen", "Marco Pegoraro", "Wil M.P. van der Aalst"]
year: 2023
venue: "RWTH Aachen University / OCEL Standard"
domain: "Object-Centric Process Mining"
extraction_version: "v2"
extraction_date: "2025-12-31"

ontological_primitives:
  - term: "Event"
    definition: "A unique entity corresponding to a specific action or observation at a specific point in time. Events are atomic (do not take time), have a timestamp, and may have additional attributes. Events are typed."
    source: "Chunk 1:149-154"
    unique_aspects: "Explicitly atomic/instantaneous - contrasts with extended processes. Events can relate to MULTIPLE objects, not just one."

  - term: "Event Type"
    definition: "Categories of events based on their nature or function (e.g., Order Created, Order Approved). Each event is of exactly one type. Sometimes called 'activity'."
    source: "Chunk 1:157-161"
    unique_aspects: "Serves as classification mechanism. The paper explicitly notes 'activity' is synonym for event type."

  - term: "Object"
    definition: "Entities involved in events - can be physical items (products, machines, workers) or abstract/information entities (orders, invoices, contracts). Objects have attributes with values that may change over time."
    source: "Chunk 1:164-167"
    unique_aspects: "Objects are NOT equivalent to 'cases' - the paper explicitly breaks from case-centric thinking. Objects have DYNAMIC attributes."

  - term: "Object Type"
    definition: "Each object is of one type. The object is an instantiation of its type (e.g., Product, Order, Invoice, Supplier)."
    source: "Chunk 1:170-171"
    unique_aspects: "Simple type system without inheritance in base spec, though inheritance mentioned as future possibility."

  - term: "Qualifier"
    definition: "A string that characterizes the role an object plays in a relationship. Used for both E2O and O2O relationships."
    source: "Chunk 1:372-380 (Definition 1)"
    unique_aspects: "Novel mechanism for role differentiation. Allows same object to participate in same event with different roles (e.g., meeting organizer vs participant)."

  - term: "Attribute"
    definition: "Named properties of events or objects. Event attributes are static per event; object attributes can change over time with timestamped values."
    source: "Chunk 1:362-365, 414-433"
    unique_aspects: "Attribute values for objects are FUNCTIONS of time - oaval(o, oa, t) - creating temporal versioning."

  - term: "Timestamp"
    definition: "Point in time with total ordering. Uses special values 0 (earliest/start) and infinity (latest/end) for convenience."
    source: "Chunk 1:368-388"
    unique_aspects: "Maps to non-negative reals formally, ISO 8601 in practice. The epoch (1970-01-01 00:00 UTC) represents initial values."

structural_patterns:
  - pattern_name: "Event-Object Many-to-Many (E2O)"
    structure: "Events relate to multiple objects; objects participate in multiple events"
    instances:
      - "One event (e3: Create Purchase Order) relates to both PR1 and PO1"
      - "One object (PO1) participates in events e3, e4, e5, e6"
    source: "Chunk 1:178-185, Definition 2"
    significance: "PARADIGM SHIFT from case-centric (one case per event) to object-centric (many objects per event)"

  - pattern_name: "Object-Object Relationships (O2O)"
    structure: "Objects relate to other objects independent of events, forming a network"
    instances:
      - "PR1 -> PO1 (PO from PR)"
      - "PO1 -> R1, R2 (Invoice from PO)"
      - "R1 -> P1 (Payment from invoice)"
    source: "Chunk 1:191-194, Table 21"
    significance: "Creates persistent object graph structure beyond event sequence"

  - pattern_name: "Qualified Relationship Triad"
    structure: "(Source, Qualifier, Target) for both E2O and O2O"
    instances:
      - "E2O: (event, qualifier, object) - e.g., (e3, 'Created order from PR', PR1)"
      - "O2O: (source_object, qualifier, target_object) - e.g., (PO2, 'Maverick buying', R3)"
    source: "Chunk 1:436-439"
    significance: "Qualifiers are FIRST-CLASS - they differentiate roles, enabling same object to participate multiple ways"

  - pattern_name: "Type-Instance Hierarchy"
    structure: "Types define structure (attributes), instances carry values"
    instances:
      - "Event Type 'Insert Invoice' defines attribute 'invoice_inserter'"
      - "Event e5 (of type Insert Invoice) has invoice_inserter='Luke'"
    source: "Chunk 1:404-421, Section 6.3"
    significance: "Clean separation enables dense table storage - each type gets its own table"

  - pattern_name: "Temporal Attribute Versioning"
    structure: "Object attributes have (object, attribute, time) -> value mapping"
    instances:
      - "PO1.po_quantity at 1970-01-01 = 500"
      - "PO1.po_quantity at 2022-01-13 = 600"
      - "R3.is_blocked toggles: No -> Yes -> No with timestamps"
    source: "Chunk 2:182-197, Table 17-18"
    significance: "Enables reconstruction of object state at any point in time via oaval[t]"

novel_concepts:
  - concept: "Object-Centric Event Data (OCED)"
    definition: "Event data where events can reference multiple objects of different types, rather than being tied to a single 'case'. A 'better abstraction of reality' than case-based logs."
    novelty_claim: "Paradigm shift from case-centric process mining. No flattening required."
    source: "Chunk 1:134-141"

  - concept: "Dynamic Object Attribute Values"
    definition: "Object attributes can change over time, with each change tracked via timestamp. The system can query the value at any point: oaval[t](o)."
    novelty_claim: "OCEL 1.0 had static attributes. OCEL 2.0 adds temporal versioning without linking changes to events."
    source: "Chunk 1:293-297, Chunk 2:182-197"

  - concept: "Relationship Qualifiers"
    definition: "Strings that describe the role/nature of E2O or O2O relationships, enabling same object pair to have multiple qualified relationships."
    novelty_claim: "Neither OCEL 1.0 nor XES had qualifiers. This enables rich role semantics."
    source: "Chunk 1:306-308"

  - concept: "Dense Table Architecture"
    definition: "Each event/object type gets its own relational table containing only relevant attributes, avoiding sparse mega-tables."
    novelty_claim: "Novel relational implementation enabling efficient storage and querying at scale."
    source: "Chunk 1:316-321"

  - concept: "Flattening Problem"
    definition: "The loss of information when forcing multi-object events into single-case format. Leads to 'misleading analysis results' and 'more complex' models."
    novelty_claim: "Explicit articulation of what's wrong with case-centric approaches."
    source: "Chunk 1:121-127"

  - concept: "Maverick Buying Pattern"
    definition: "Running example of unethical procurement where invoice precedes proper purchase order - demonstrating compliance violations capturable in OCEL."
    novelty_claim: "Shows OCEL's ability to capture real-world process deviations involving multiple objects."
    source: "Chunk 1:645-649"

semantic_commitments:
  - commitment: "Events as Atomic/Instantaneous"
    position: "Events are atomic - they 'do not take time'. They occur at a single timestamp."
    implications: "Extended activities must be modeled as pairs of events (start/end) or derived. Cannot directly model durations."
    source: "Chunk 1:152-153"

  - commitment: "Object Identity Over Time"
    position: "Objects persist with changing attributes. Identity is maintained via unique identifier."
    implications: "Endurantist view - objects are wholly present at each moment, attributes vary. Not 4D spacetime worms."
    source: "Chunk 2:182-188"

  - commitment: "Open-World Attribute Semantics"
    position: "Missing attribute values are allowed (partial functions). Attributes only exist for appropriate types."
    implications: "Cannot assume closed-world. Must handle incomplete data gracefully."
    source: "Chunk 1:443-457"

  - commitment: "Type Disjointness"
    position: "Universes (events, objects, event types, object types, attributes, values, timestamps, qualifiers) are pairwise disjoint."
    implications: "No polymorphism between categories. An object cannot be used as an event, etc."
    source: "Chunk 1:374-376"

  - commitment: "Attribute-to-Type Binding"
    position: "Each attribute belongs to exactly one event type or object type (eatype, oatype functions)."
    implications: "No shared attributes across types. Each type has its own attribute namespace."
    source: "Chunk 1:416-421"

boundary_definitions:
  - entity_type: "Event"
    identity_criteria: "Unique identifier in U_ev. Each event is of exactly one type with one timestamp."
    boundary_cases: "What if same action occurs twice at same timestamp with same objects? Still distinct events with different IDs."
    source: "Chunk 1:150-154, Definition 2"

  - entity_type: "Object"
    identity_criteria: "Unique identifier in U_obj. Persists across time with changing attributes."
    boundary_cases: "When does an object cease to exist? Not modeled - no lifecycle/deletion events required."
    source: "Chunk 1:164-167, Definition 2"

  - entity_type: "Event-to-Object Relationship"
    identity_criteria: "Tuple (event, qualifier, object) - all three form composite identity."
    boundary_cases: "Same event-object pair can have MULTIPLE relationships with different qualifiers."
    source: "Chunk 1:436-437, Table 20 note"

  - entity_type: "Process Instance"
    identity_criteria: "NOT DEFINED - intentionally absent"
    boundary_cases: "This is the key innovation: there IS no single process instance/case. Multiple objects interweave."
    source: "Implicit - core thesis of paper"

temporal_modeling:
  - aspect: "Event Timestamps"
    approach: "Single instant per event, totally ordered"
    mechanism: "time: E -> U_time assigns exactly one timestamp to each event"
    source: "Chunk 1:410-411"

  - aspect: "Object Attribute History"
    approach: "Timestamped value changes forming a discrete timeline"
    mechanism: "oaval: (O x OA x U_time) -> U_val partial function. Query via oaval[t] to get value at any time."
    source: "Chunk 1:432-433, 482-492"

  - aspect: "Initial State Convention"
    approach: "Epoch timestamp (1970-01-01 00:00 UTC = 0) represents initial values"
    mechanism: "First row in object type table has epoch timestamp with all initial attribute values"
    source: "Chunk 2:182-188"

  - aspect: "Change Tracking"
    approach: "ocel_changed_field column indicates which attribute changed"
    mechanism: "Non-initial rows have specific timestamp and indicate which column changed"
    source: "Chunk 2:191-192"

  - aspect: "Object-to-Object Relationships"
    approach: "Static/atemporal - no timestamp on O2O"
    mechanism: "O2O relationships exist independent of time in the base model"
    source: "Chunk 1:618-619 (implicit), Table 21"
    surprise: "O2O lacks temporal dimension - cannot model when relationships form/dissolve"

agency_spectrum:
  - agent_type: "Human Actor"
    capabilities: "Performs business activities (creates, approves, blocks actions)"
    constraints: "Represented as attribute values (e.g., pr_creator='Mike'), not as first-class objects"
    source: "Chunk 2:84 (Mike), 94 (Tania), 142 (Sam)"

  - agent_type: "Robot/Automated Actor"
    capabilities: "Performs automated tasks like payment insertion"
    constraints: "Same representation as humans - attribute value 'Robot'"
    source: "Chunk 2:162-164 (payment_inserter='Robot')"

  - agent_type: "No Explicit Agent Model"
    capabilities: "N/A"
    constraints: "OCEL 2.0 does NOT have an Agent primitive. Actors are captured via event attributes, not as a separate entity type."
    source: "Implicit - agent not in Definition 1 or 2"
    surprise: "Despite 'Robot' appearing as actor, there's no ontological distinction between human/machine agency"

knowledge_representation:
  - mechanism: "Metamodel/Schema"
    formalism: "Set-theoretic formal definitions with UML-like visualization"
    reasoning: "Definitions enable consistency checking but no inference rules specified"
    source: "Chunk 1:333-342, Figure 1"

  - mechanism: "Relational Storage (SQLite)"
    formalism: "Normalized relational tables with foreign keys and constraints"
    reasoning: "SQL queries for validation; efficient joins for E2O/O2O traversal"
    source: "Section 6, Chunk 1:801-844"

  - mechanism: "XML Format"
    formalism: "Hierarchical document with XSD schema validation"
    reasoning: "XPath queries, keyref constraints for referential integrity"
    source: "Section 7, Chunk 3:119-156"

  - mechanism: "JSON Format"
    formalism: "Nested JSON with JSON Schema validation"
    reasoning: "Web-native, JavaScript object access patterns"
    source: "Section 8, Chunk 3:455-482"

  - mechanism: "Formal Semantics"
    formalism: "Set-theoretic functions and constraints"
    reasoning: "Enables formal proofs about log properties; no automated reasoning engine specified"
    source: "Chunk 1:346-498 (Definition 1-2)"

emergence_indicators:
  - phenomenon: "Process Behavior from Object Interactions"
    mechanism: "Following E2O relationships reveals process flow; O2O reveals structural dependencies"
    evidence: "Running example shows procurement flow emerging from PR->PO->Invoice->Payment relationships"
    source: "Section 5, Tables 3, 20, 21"

  - phenomenon: "Compliance Violations as Patterns"
    mechanism: "Maverick buying detected when invoice precedes purchase order creation"
    evidence: "R3 created (e9) BEFORE PO2 created (e10) - temporal anomaly visible in event sequence"
    source: "Chunk 1:645-649"

  - phenomenon: "Object Lifecycle Patterns"
    mechanism: "Attribute changes over time reveal state machine-like behavior"
    evidence: "Invoice R3: is_blocked No->Yes->No traces blocking lifecycle"
    source: "Chunk 2:251-254, Table 18"

integration_surfaces:
  - surface: "XES Standard"
    connects_to: ["IEEE 1849-2023", "Traditional process mining tools"]
    alignment_quality: "Intentional departure - XES is case-centric. OCEL is 'more expressive, less complicated, and better readable'."
    source: "Chunk 1:37-38, Chunk 1:238-244"

  - surface: "Enterprise Systems"
    connects_to: ["ERP (SAP)", "CRM", "MES"]
    alignment_quality: "High - designed to capture 'actual events and objects that leave traces' in these systems"
    source: "Chunk 1:135-137"

  - surface: "BPMN/Process Models"
    connects_to: ["DFGs", "BPMN models", "UML activity diagrams", "Workflow nets", "Process trees"]
    alignment_quality: "Tension - traditional models assume single case. Object-centric Petri nets mentioned as compatible."
    source: "Chunk 1:118-120, Chunk 1:258"

  - surface: "Domain Ontologies"
    connects_to: ["Standard object/event types", "P2P ontologies", "O2C ontologies"]
    alignment_quality: "Future aspiration - paper calls for standardization of types across domains"
    source: "Chunk 4:386-405"

  - surface: "AI/ML Systems"
    connects_to: ["Generative AI", "Discriminative AI", "Predictive process mining"]
    alignment_quality: "Anticipated - paper mentions AI possibilities with standardized types"
    source: "Chunk 4:401-405"

gaps_and_tensions:
  - gap_type: "Omission"
    description: "No Agent as first-class primitive. Actors captured only as string attribute values."
    implications: "Cannot model agent capabilities, permissions, relationships, or track agent behavior across events."
    source: "Implicit - Definition 1 lists 8 universes, none for agents"

  - gap_type: "Omission"
    description: "No temporal dimension for O2O relationships."
    implications: "Cannot model when object relationships form or dissolve. All O2O is implicitly 'eternal'."
    source: "Implicit - Table 21 has no timestamp column"

  - gap_type: "Omission"
    description: "No rules/constraints/governance layer."
    implications: "Cannot declaratively specify what SHOULD happen, only what DID happen."
    source: "Implicit - not in metamodel"

  - gap_type: "Omission"
    description: "No goal/intention modeling."
    implications: "Cannot capture WHY events occurred or what actors were trying to achieve."
    source: "Implicit - not in metamodel"

  - gap_type: "Tension"
    description: "Events are atomic but real activities have duration."
    implications: "Must use start/end event pairs for duration modeling - workaround, not native support."
    source: "Chunk 1:152-153"

  - gap_type: "Underspecified"
    description: "Object lifecycle (creation, deletion) not formally modeled."
    implications: "Objects implicitly exist; no mechanism for object death/archival."
    source: "Implicit - Definition 2 has O as static set"

  - gap_type: "Tension"
    description: "Inheritance for types mentioned but not specified."
    implications: "Cannot currently model type hierarchies (e.g., PremiumCustomer is-a Customer)."
    source: "Chunk 4:400-401 - mentioned as future possibility"

  - gap_type: "Omission"
    description: "No support for uncertainty or probability."
    implications: "All facts are certain. Cannot model 'likely' events or fuzzy timestamps."
    source: "Implicit - all values are definite"

empirical_grounding:
  - type: "Running Example"
    domain: "Procurement (Purchase-to-Pay)"
    scale: "13 events, 8 objects, 4 object types"
    findings: "Demonstrates qualification, dynamic attributes, maverick buying detection"
    source: "Section 5"

  - type: "Industry Survey"
    domain: "Process Mining Community"
    scale: "289 participants (practitioners, researchers, vendors, end-users)"
    findings: "Showed need for object-centricity; drove requirements for OCEL 2.0"
    source: "Chunk 1:266-268"

  - type: "OCEL 1.0 Experience"
    domain: "Research and Industry"
    scale: "3 years (2020-2023)"
    findings: "Triggered development of OCPM techniques; identified limitations addressed in 2.0"
    source: "Chunk 1:141-143, Chunk 1:261-264"

  - type: "Tool Ecosystem"
    domain: "Process Mining"
    scale: "40+ vendors offering process mining software"
    findings: "Market validation of process mining; OCEL aims to become 'default exchange format'"
    source: "Chunk 1:110-111, Chunk 1:94-96"

surprises_and_discoveries:
  - surprise: "No Agent Primitive Despite Resource/Actor Usage"
    description: "The running example uses 'Mike', 'Tania', 'Sam', 'Robot' as actors, but they're just string values in attributes - no ontological status."
    implication: "Process mining tradition focuses on WHAT happened, not WHO as a first-class concern."

  - surprise: "O2O Relationships Are Atemporal"
    description: "Unlike object attributes which have timestamps, O2O relationships have no temporal dimension."
    implication: "Can't model relationship evolution - big gap for organizational modeling."

  - surprise: "Explicit Rejection of Single-Case Paradigm"
    description: "Paper is philosophically committed against 'flattening' - not just a technical choice but epistemological stance."
    implication: "OCEL represents genuine paradigm shift, not incremental improvement."

  - surprise: "Future Vision Includes Standard Type Taxonomies"
    description: "Paper envisions standardized object/event types for domains like O2C, P2P - almost like an upper ontology for process mining."
    implication: "OCEL 2.0 is positioned as foundation for broader standardization effort."

  - surprise: "Qualifiers Are Strings, Not Typed"
    description: "Despite rich type system for objects/events, qualifiers are just free-form strings."
    implication: "No controlled vocabulary - could lead to inconsistency across logs."
---

# OCEL 2.0 Specification - V2 Discovery Analysis

## Executive Summary

OCEL 2.0 represents a **paradigm shift** in process mining from case-centric to object-centric thinking. Its core innovation is allowing events to relate to multiple objects while tracking object attribute changes over time. The specification provides rigorous formal definitions and three storage formats (SQLite, XML, JSON).

## Key Ontological Contribution

The paper's fundamental claim is that **"case-centric" process mining distorts reality**. Real business processes involve many-to-many relationships between events and objects. Forcing these into single-case format ("flattening") loses information and creates misleading analysis.

### The Core Primitives

OCEL 2.0 has a minimalist primitive set:
1. **Event** - atomic, timestamped, typed
2. **Object** - persistent, typed, with temporal attributes
3. **Event Type** / **Object Type** - classification mechanisms
4. **Attribute** - named properties (static for events, temporal for objects)
5. **Qualifier** - role labels for relationships
6. **Timestamp** - temporal ordering

Notably **missing**: Agent, Goal, Rule, Resource as first-class citizens.

## Structural Innovation: Qualified Many-to-Many

The key structural pattern is the **qualified relationship triad**:
- E2O: `(event, qualifier, object)` - "this event affected this object in this role"
- O2O: `(object1, qualifier, object2)` - "these objects are related this way"

This enables:
- One event linking to multiple objects with different roles
- Same object pair having multiple relationship types
- Rich provenance without case flattening

## Temporal Model

Events are **instantaneous** (atomic, no duration). Object attributes have **versioned values** with timestamps, enabling state reconstruction at any point via `oaval[t](o)`.

Critical gap: O2O relationships are **atemporal** - no way to model when relationships form/dissolve.

## What's Not There

The paper is refreshingly honest about scope. OCEL 2.0 deliberately excludes:
- **Agent/Actor ontology** - people appear only as attribute values
- **Goals/Intentions** - no "why" modeling
- **Rules/Constraints** - no normative layer
- **Inheritance** - no type hierarchies (mentioned as future work)
- **Uncertainty** - all facts are definite

## Integration Points

OCEL 2.0 positions itself against XES (the IEEE standard) as simpler and more expressive. It's designed for enterprise systems (ERP, CRM, MES) and anticipates future domain-specific type taxonomies.

## Discovery Signals

### Confirmed Patterns
- Event-Activity terminology alignment
- Object-Entity alignment
- Temporal versioning for object state

### Novel/Unexpected
- Strong philosophical commitment against case-centricity (not just technical choice)
- Qualifiers as untyped strings (surprising given otherwise rigorous type system)
- Vision for standardized domain ontologies built on OCEL
- Robot actors treated identically to humans (no agency spectrum)

### Gaps Relevant to AI Agents
For AI/LLM agent systems, OCEL 2.0 is **insufficient** as-is:
- No agent identity/capability modeling
- No goal/intention representation
- No rule/constraint layer for governance
- No uncertainty handling

However, its object-centric foundation could be extended to support these needs.
