---
paper_id: "09-OCEL_20_Specification"
title: "OCEL (Object-Centric Event Log) 2.0 Specification"
authors:
  - "Alessandro Berti"
  - "Istvan Koren"
  - "Jan Niklas Adams"
  - "Gyunam Park"
  - "Benedikt Knopp"
  - "Nina Graves"
  - "Majid Rafiei"
  - "Lukas Liss"
  - "Leah Tacke Genannt Unterberg"
  - "Yisong Zhang"
  - "Christopher Schwanen"
  - "Marco Pegoraro"
  - "Wil M.P. van der Aalst"
year: 2023
chunks_expected: 4
chunks_read: 4
analysis_complete: true
schema_version: "2.3"

chunk_index:
  1:
    token_count: 10514
    fields_found:
      entity_types: true
      entity_definitions: true
      entity_relationships: true
      entity_count: true
      abstraction_level: true
      framework_comparison: true
      methodology: partial
      ai_integration: false
      agent_modeling: partial
      agentic_workflows: false
      generative_ai_patterns: false
      agent_ontology_integration: false
      empirical_evidence: true
      limitations: true
      tools_standards: true
  2:
    token_count: 6846
    fields_found:
      entity_types: partial
      entity_definitions: partial
      entity_relationships: true
      entity_count: false
      abstraction_level: false
      framework_comparison: false
      methodology: false
      ai_integration: false
      agent_modeling: true
      agentic_workflows: false
      generative_ai_patterns: false
      agent_ontology_integration: false
      empirical_evidence: false
      limitations: false
      tools_standards: true
  3:
    token_count: 4444
    fields_found:
      entity_types: false
      entity_definitions: false
      entity_relationships: partial
      entity_count: false
      abstraction_level: false
      framework_comparison: false
      methodology: false
      ai_integration: false
      agent_modeling: false
      agentic_workflows: false
      generative_ai_patterns: false
      agent_ontology_integration: false
      empirical_evidence: false
      limitations: false
      tools_standards: true
  4:
    token_count: 3745
    fields_found:
      entity_types: false
      entity_definitions: false
      entity_relationships: false
      entity_count: false
      abstraction_level: false
      framework_comparison: false
      methodology: false
      ai_integration: true
      agent_modeling: false
      agentic_workflows: false
      generative_ai_patterns: true
      agent_ontology_integration: true
      empirical_evidence: false
      limitations: true
      tools_standards: true

entity_types:
  - item: "Event"
    chunk: 1
    lines: "149-154"
    quote: "Events: Object-centric process mining works on discrete events. They represent the various actions or activities that occur within a system or process, such as approving an order, shipping an item, or making a payment. Every event is unique and corresponds to a specific action or observation at a specific point in time. Events are atomic (i.e., do not take time), have a timestamp, and may have additional attributes. Events are typed."
  - item: "Event Type"
    chunk: 1
    lines: "157-161"
    quote: "Event Types: Events are categorized into different types based on their nature or function. For example, a procurement process might have event types such as Order Created, Order Approved, or Invoice Sent. Each type of event represents a specific kind of action that can take place in the process. Each event is of exactly one type. Sometimes, we use the term activity to refer to an event type."
  - item: "Object"
    chunk: 1
    lines: "164-167"
    quote: "Objects: In object-centric process mining, objects represent the entities that are involved in events. These might be physical items like products in a supply chain, machines, workers, or abstract/information entities like orders, invoices, or contracts in a procurement process. Objects have attributes with values, e.g., prices. These values may change over time."
  - item: "Object Type"
    chunk: 1
    lines: "170-171"
    quote: "Object Types: Each object is of one type. The object is an instantiation of its type. Object types might include categories like Product, Order, Invoice, or Supplier."
  - item: "Event-to-Object (E2O) Relationship"
    chunk: 1
    lines: "178-185"
    quote: "Event-to-Object (E2O) Relationships: Events are associated with objects. This relationship describes that an object affects an event or that an event affects an object. In contrast to traditional event logs, events can be related to multiple objects. Furthermore, these relationships can be qualified differently, describing the role an object plays in the occurrence of this specific event."
  - item: "Object-to-Object (O2O) Relationship"
    chunk: 1
    lines: "191-194"
    quote: "Object-to-Object (O2O) Relationships: Objects can also be related to other objects outside the context of an event. For example, an employee may be part of an organizational unit. In addition to the mere existence of a relation, this relationship can also be qualified (e.g., part-of, reports-to, or belongs-to)."
  - item: "Qualifier"
    chunk: 1
    lines: "306-308"
    quote: "Relationship Qualifiers: OCEL 2.0 offers capabilities to express qualifiers for relationships, both for Object-to-Object (O2O) and Event-to-Object (E2O) relationships. E2O relationship qualifiers describe in which role an object takes part in an event, while O2O relationship qualifiers can further characterize the association between two objects."
  - item: "Attribute"
    chunk: 1
    lines: "362-365"
    quote: "U_attr is the universe of attribute names. U_val is the universe of attribute values."
  - item: "Timestamp"
    chunk: 1
    lines: "368-369"
    quote: "U_time is the universe of timestamps (with 0 as the smallest element and infinity as the largest element)"

entity_definitions:
  Event:
    chunk: 1
    lines: "149-154"
    definition: "Discrete actions or activities within a system/process. Unique, atomic (do not take time), have a timestamp and may have additional attributes. Events are typed."
  Event_Type:
    chunk: 1
    lines: "157-161"
    definition: "Categories of events based on their nature or function (e.g., Order Created, Order Approved). Each event is of exactly one type. Also referred to as 'activity'."
  Object:
    chunk: 1
    lines: "164-167"
    definition: "Entities involved in events - physical items (products, machines, workers) or abstract/information entities (orders, invoices, contracts). Objects have attributes with values that may change over time."
  Object_Type:
    chunk: 1
    lines: "170-171"
    definition: "Classification category for objects. Each object is an instantiation of one type (e.g., Product, Order, Invoice, Supplier)."
  E2O_Relationship:
    chunk: 1
    lines: "178-185"
    definition: "Qualified association between events and objects. Describes that an object affects an event or vice versa. Events can relate to multiple objects with different qualifiers describing the role."
  O2O_Relationship:
    chunk: 1
    lines: "191-194"
    definition: "Qualified association between objects outside the context of events (e.g., part-of, reports-to, belongs-to relationships)."
  Qualifier:
    chunk: 1
    lines: "372"
    definition: "U_qual is the universe of qualifiers - used to describe the nature/role of relationships between entities."
  Dynamic_Object_Attribute:
    chunk: 1
    lines: "293-297"
    definition: "OCEL 2.0 allows object attribute values to change over time. Instead of a single fixed value, an object attribute may have a value that changes during the process."

entity_relationships:
  - item: "Event has Event Type (1:1)"
    chunk: 1
    lines: "408"
    quote: "evtype: E -> U_etype assigns types to events."
  - item: "Object has Object Type (1:1)"
    chunk: 1
    lines: "424"
    quote: "objtype: O -> U_otype assigns types to objects."
  - item: "Event-to-Object (E2O) many-to-many qualified"
    chunk: 1
    lines: "436"
    quote: "E2O is a subset of E x U_qual x O are the qualified event-to-object relations."
  - item: "Object-to-Object (O2O) many-to-many qualified"
    chunk: 1
    lines: "439"
    quote: "O2O is a subset of O x U_qual x O are the qualified object-to-object relations."
  - item: "Event has Timestamp (1:1)"
    chunk: 1
    lines: "411"
    quote: "time: E -> U_time assigns timestamps to events."
  - item: "Event has Event Attributes"
    chunk: 1
    lines: "414-421"
    quote: "EA is the set of event attributes. eatype: EA -> U_etype assigns event types to event attributes. eaval: (E x EA) -> U_val assigns values to event attributes."
  - item: "Object has Object Attributes (time-varying)"
    chunk: 1
    lines: "429-433"
    quote: "OA is the set of object attributes. oatype: OA -> U_otype assigns object types to object attributes. oaval: (O x OA x U_time) -> U_val assigns values to object attributes."

entity_count:
  value: 8
  chunk: 1
  lines: "346-372"
  quote: "We define the following pairwise disjoint universes: U_ev (universe of events), U_etype (universe of event types/activities), U_obj (universe of objects), U_otype (universe of object types), U_attr (universe of attribute names), U_val (universe of attribute values), U_time (universe of timestamps), U_qual (universe of qualifiers)"
  rationale: "The formal model defines 8 fundamental universes as the basis for all OCEL 2.0 constructs. These are pairwise disjoint, ensuring clear separation of concepts."

abstraction_level:
  level: "Domain/Application Standard"
  chunk: 1
  lines: "88-96"
  quote: "This document introduces the OCEL 2.0 standard to record and exchange object-centric event logs. The purpose of the standard is to guide the implementation of conformant process mining tools... OCEL 2.0 and its metamodel are designed from the ground up to facilitate the exchange of event logs coming from a wide variety of information systems."
  purpose: "Practical interoperability standard for Object-Centric Process Mining (OCPM). Bridges foundational concepts with concrete implementations (SQLite, XML, JSON)."

framework_comparison:
  - item: "Comparison with XES"
    chunk: 1
    lines: "237-244"
    quote: "The first comprehensive standard for storing event data was the IEEE Standard for eXtensible Event Stream (XES). XES became an official IEEE standard in 2016... Compared to XES, [OCEL 2.0] is more expressive, less complicated, and better readable."
  - item: "Extension of OCEL 1.0"
    chunk: 1
    lines: "33-40"
    quote: "OCEL 1.0 was first released in 2020 and triggered the development of a range of OCPM techniques. OCEL 2.0 forms the new, more expressive standard, allowing for more extensive process analyses... In contrast to the first OCEL standard, it can depict changes in objects, provide information on object relationships, and qualify these relationships."
  - item: "Limitations of OCEL 1.0"
    chunk: 1
    lines: "198-201"
    quote: "The first OCEL format (OCEL 1.0) provided an event log standard that could capture events related to multiple objects with attributes but did not include Object-to-Object (O2O) relationship, qualifiers for either O2O and E2O relationships, or changing object attribute values."
  - item: "Comparison with traditional process mining"
    chunk: 1
    lines: "115-127"
    quote: "Traditional process mining considers processes involving single cases, their events, and event attributes. The approach falls short when dealing with complex, multi-dimensional processes, where events possibly relate to a variety of entities or objects that interact and evolve over time."

methodology:
  approach: "Hybrid - top-down formal specification with empirical validation"
  chunk: 1
  lines: "335-342"
  quote: "The metamodel Figure 1 is supported by a formalization that adds more details. The theoretical foundation is crucial for understanding and using OCEL 2.0. These definitions form the basis for concrete exchange formats discussed later. The connection between theory and practice ensures that both the relational model and XML schema respect the standard's principles."

ai_integration:
  - item: "Potential for AI/ML applications"
    chunk: 4
    lines: "401-405"
    quote: "It is possible to define taxonomies of object types and event types using inheritance notions. This creates possibilities for both generative and discriminative Artificial Intelligence (AI). Therefore, researchers and solution providers should focus on creating standard object and event types and the corresponding normative object-centric process models."

agent_modeling:
  - item: "Implicit agent representation via event attributes"
    chunk: 1
    lines: "667-683"
    quote: "pr_creator is the resource that created the purchase requisition in the system. pr_approver is the resource that approved the purchase requisition in the system. po_creator is the resource that created the purchase order in the system."
  - item: "Robot/automated agent support"
    chunk: 2
    lines: "162-164"
    quote: "payment_inserter: Robot (for e7, e8, e13 events)"

agentic_workflows: "NOT_FOUND"

generative_ai_patterns:
  - item: "Taxonomy-based AI enablement"
    chunk: 4
    lines: "400-405"
    quote: "It is possible to define taxonomies of object types and event types using inheritance notions. This creates possibilities for both generative and discriminative Artificial Intelligence (AI)."

agent_ontology_integration:
  - item: "System-agnostic data for AI"
    chunk: 4
    lines: "349-351"
    quote: "Using OCEL 2.0, it is possible to create a system-agnostic, single source of truth. Event data should capture real business-relevant events without being limited by a single-case notion."
  - item: "Standard types for AI applications"
    chunk: 4
    lines: "394-396"
    quote: "Event data in OCEL 2.0 format enables process discovery, conformance checking, performance analysis, and operational support without the need to process the data further."

empirical_evidence:
  - item: "Enterprise system grounding"
    chunk: 1
    lines: "135-139"
    quote: "OCPM starts from the actual events and objects that leave traces in ERP (Enterprise Resource Planning), CRM (Customer Relationship Management), MES (Manufacturing Execution System), and other IT systems. In the databases of such systems, one-to-one relationships are the exception. Most relationships are one-to-many or many-to-many."
  - item: "IEEE survey validation"
    chunk: 1
    lines: "266-268"
    quote: "In 2021, a survey was conducted by the IEEE Task Force on Process Mining. The goal was to collect requirements for a new standard succeeding XES. The online survey with 289 participants, spanning the roles of practitioners, researchers, software vendors and end-users, showed the need for supporting object-centricity."

limitations:
  - item: "OCEL 1.0 limitations addressed"
    chunk: 1
    lines: "198-201"
    quote: "The first OCEL format (OCEL 1.0)... did not include Object-to-Object (O2O) relationship, qualifiers for either O2O and E2O relationships, or changing object attribute values. OCEL 2.0 addresses these limitations."
  - item: "Traditional process mining limitations"
    chunk: 1
    lines: "121-127"
    quote: "Traditional process mining approaches require the flattening of event data in order to satisfy this assumption. This may lead to misleading analysis results. Process mining results also tend to become more complex because different objects get intertwined while trying to straitjacket the processes."
  - item: "Standard is a stepping stone"
    chunk: 4
    lines: "406-413"
    quote: "It is essential to note that the rapidly evolving field of object-centric process mining continues to present new challenges and opportunities. As such, the OCEL 2.0 standard, despite its substantial contribution, should be seen as a stepping stone in this exciting journey rather than a final destination."

tools_standards:
  - item: "SQLite Relational Format"
    chunk: 1
    lines: "38-39"
    quote: "OCEL 2.0 offers three exchange formats: a relational database (SQLite), XML, and JSON format."
  - item: "XML Format with XSD validation"
    chunk: 2
    lines: "410-413"
    quote: "We propose an XML implementation following Definition 2. The timestamps are assumed to follow the ISO format specification."
  - item: "JSON Format with JSON Schema"
    chunk: 3
    lines: "455-458"
    quote: "The JSON format provides a lightweight structure for web-native process mining applications. It is conceptually similar to the XML format with its top-level arrays events, eventTypes, objects, and objectTypes."
  - item: "Validation schemas URLs"
    chunk: 1
    lines: "22-27"
    quote: "Validation Schemes: XML: https://www.ocel-standard.org/2.0/ocel20-schema-xml.xsd, JSON: https://www.ocel-standard.org/2.0/ocel20-schema-json.json, Relational: https://www.ocel-standard.org/2.0/ocel20-schema-relational.pdf"
  - item: "ISO 8601 timestamp format"
    chunk: 1
    lines: "387-388"
    quote: "In the formalization, time is mapped on the non-negative reals, but concrete implementations will use, for example, the ISO 8601 time format."
  - item: "Dense table structure"
    chunk: 1
    lines: "316-321"
    quote: "Relational Specification based on Dense Tables: One major feature of OCEL 2.0 is its data structure using dense tables. Each table corresponds to a unique event or object type, storing only relevant attributes. This results in efficient use of storage space and less data redundancy."
---

# OCEL (Object-Centric Event Log) 2.0 Specification

## Summary

This document provides the official specification for OCEL 2.0, a standard for recording and exchanging Object-Centric Event Data (OCED) for Object-Centric Process Mining (OCPM). OCEL 2.0 extends OCEL 1.0 (released 2020) with three key enhancements: Object-to-Object relationships, dynamic object attribute values, and relationship qualifiers for both E2O and O2O relationships.

## Key Contributions

### Entity Model (Metamodel)
The OCEL 2.0 metamodel defines 8 fundamental universes:
1. **Events** - Discrete, atomic actions with timestamps and attributes
2. **Event Types** - Categories of events (activities)
3. **Objects** - Entities involved in events (physical or abstract)
4. **Object Types** - Categories of objects
5. **Attributes** - Named properties with values
6. **Attribute Values** - The actual values (can change over time for objects)
7. **Timestamps** - Temporal ordering
8. **Qualifiers** - Describe the nature of relationships

### Relationship Types
- **Event-to-Object (E2O)**: Qualified many-to-many relationships between events and objects
- **Object-to-Object (O2O)**: Qualified relationships between objects (independent of events)

### Key Improvements over OCEL 1.0
1. **Dynamic Object Attributes**: Object attribute values can change over time
2. **O2O Relationships**: Objects can be directly related to other objects
3. **Relationship Qualifiers**: Both E2O and O2O relationships can be qualified (e.g., part-of, reports-to)

## Implementation Formats

OCEL 2.0 provides three exchange formats:
1. **Relational SQLite** - Dense table structure with separate tables per event/object type
2. **XML** - With XSD validation schema
3. **JSON** - Lightweight format for web applications with JSON Schema validation

## Relevance to Research Questions

### Entity Types and Definitions
The paper provides formal definitions for all core entity types in Definition 1 (universes) and Definition 2 (OCEL tuple). The Event-Object relationship model is central to the standard.

### Framework Comparison
OCEL 2.0 is explicitly compared to:
- **XES**: More expressive, less complicated, better readable
- **OCEL 1.0**: Adds O2O relationships, qualifiers, dynamic attributes
- **Traditional Process Mining**: Overcomes single-case limitation

### AI Integration Potential
The paper mentions that standardized object and event types create possibilities for both generative and discriminative AI applications, though specific AI integration patterns are not detailed.

## Notable Quotes

> "Object-Centric Process Mining (OCPM) represents a paradigm shift, intended to address and overcome the inherent limitations of traditional case-centric process mining methods." (Chunk 1:134-135)

> "Using OCEL 2.0, it is possible to create a system-agnostic, single source of truth." (Chunk 4:349)

> "This creates possibilities for both generative and discriminative Artificial Intelligence (AI)." (Chunk 4:402)
