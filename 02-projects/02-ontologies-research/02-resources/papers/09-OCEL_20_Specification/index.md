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
  - "Lukas Lis"
  - "Leah Tacke Genannt Unterberg"
  - "Yisong Zhang"
  - "Christopher Schwanen"
  - "Marco Pegoraro"
  - "Wil M.P. van der Aalst"
year: 2023
chunks_expected: 4
chunks_read: 4
analysis_complete: true
high_priority_fields_found: 7

# Entity Types (HIGH)
entity_types:
  - "Event"
  - "Event Type (Activity)"
  - "Object"
  - "Object Type"
  - "Event-to-Object (E2O) Relationship"
  - "Object-to-Object (O2O) Relationship"
  - "Attribute"
  - "Qualifier"

# Entity Definitions (HIGH)
entity_definitions:
  Event: "Discrete action at a specific point in time; atomic, has timestamp and type (Chunk 1:149-154)"
  Event_Type: "Category of events based on nature/function; also called 'activity' (Chunk 1:157-161)"
  Object: "Entity involved in events; physical items or abstract/information entities with attributes (Chunk 1:164-168)"
  Object_Type: "Category of objects; object is instantiation of its type (Chunk 1:170-171)"
  E2O_Relationship: "Qualified association between events and objects with role qualifier (Chunk 1:178-185)"
  O2O_Relationship: "Qualified relationship between objects outside event context (Chunk 1:191-194)"
  OCEL: "Tuple L = (E, O, EA, OA, evtype, time, objtype, eatype, oatype, eaval, oaval, E2O, O2O) (Chunk 1:395-396)"

# Entity Relationships (HIGH)
entity_relationships:
  - from: "Event"
    to: "Object"
    relationship: "E2O (qualified, many-to-many)"
    source: "Chunk 1:436-437"
  - from: "Object"
    to: "Object"
    relationship: "O2O (qualified, many-to-many)"
    source: "Chunk 1:439-440"
  - from: "Event"
    to: "Event Type"
    relationship: "evtype (each event has exactly one type)"
    source: "Chunk 1:408-409"
  - from: "Object"
    to: "Object Type"
    relationship: "objtype (each object has exactly one type)"
    source: "Chunk 1:424-425"
  - from: "Event"
    to: "Attribute"
    relationship: "eaval (event attributes with values)"
    source: "Chunk 1:420-421"
  - from: "Object"
    to: "Attribute"
    relationship: "oaval (object attributes with temporal values)"
    source: "Chunk 1:433-434"

# Abstraction Level (HIGH)
abstraction_level: "domain"
abstraction_rationale: "OCEL 2.0 is a domain-specific standard for object-centric process mining, not a foundational ontology but a practical data exchange format grounded in process mining theory (Chunk 1:88-96)"

# Framework Comparison (HIGH)
framework_comparison:
  - compared_to: "XES"
    relationship: "supersedes"
    details: "More expressive, less complicated, better readable than XES (Chunk 1:37-39)"
    source: "Chunk 1:37-39"
  - compared_to: "OCEL 1.0"
    relationship: "extends"
    details: "Adds O2O relationships, dynamic object attributes, relationship qualifiers (Chunk 1:286-308)"
    source: "Chunk 1:142-144"
  - compared_to: "Traditional event logs"
    relationship: "replaces"
    details: "Eliminates need for flattening, supports many-to-many event-object relations (Chunk 1:115-127)"
    source: "Chunk 1:115-127"

# AI Integration (HIGH)
ai_integration:
  - pattern: "AI taxonomy potential"
    description: "Inheritance-based taxonomies of object/event types enable generative and discriminative AI (Chunk 4:401-405)"
    source: "Chunk 4:401-405"
ai_integration_note: "Paper is 2023 specification document; AI integration discussed as future possibility, not current implementation"

# Agent Modeling (HIGH)
agent_modeling: "N/A - OCEL 2.0 does not model agents as autonomous entities; 'resources' (human actors like Mike, Mario, Sam) are event attributes, not first-class agent entities"

# Agentic Workflows (HIGH)
agentic_workflows: "N/A - Not addressed; focus is on event data standard, not agent orchestration"

# Generative AI Patterns (HIGH)
generative_ai_patterns: "N/A - Not addressed in this specification document"

# Agent-Ontology Integration (HIGH)
agent_ontology_integration: "N/A - Not addressed; however, structured OCEL 2.0 data could serve as grounding for agent memory/reasoning"

# Entity Count (MEDIUM)
entity_count:
  count: 8
  rationale: "Core metamodel entities: Event, Object, Event Type, Object Type, Event Attribute, Object Attribute, E2O Relationship, O2O Relationship"
  source: "Chunk 1:279-308"

# Methodology (MEDIUM)
methodology: "bottom-up"
methodology_rationale: "OCEL 2.0 derived from actual event data in ERP, CRM, MES systems; empirically grounded in process mining practice (Chunk 1:134-144)"

# Empirical Evidence (MEDIUM)
empirical_evidence:
  - type: "Running example"
    description: "Procurement process with purchase requisitions, orders, invoices, payments; includes compliance scenario (maverick buying)"
    source: "Chunk 1:631-767"
  - type: "Industry adoption"
    description: "Based on OCEL 1.0 experiences since 2020; IEEE Task Force survey with 289 participants"
    source: "Chunk 1:262-278"
  - type: "Enterprise systems"
    description: "Designed for ERP, CRM, MES system integration"
    source: "Chunk 1:136-137"

# Limitations (MEDIUM)
limitations:
  - "Middle ground between simplicity and expressiveness - intentional design tradeoff (Chunk 4:342-343)"
  - "Does not model agents as first-class entities - actors are event attributes only"
  - "No built-in support for process models - focuses on event data only"
  - "Temporal granularity limited to timestamps - no duration modeling for events"

# Tools and Standards (MEDIUM)
tools_standards:
  - "SQLite (relational database format)"
  - "XML with XSD validation schema"
  - "JSON with JSON Schema validation"
  - "ISO 8601 timestamp format"
  - "ocel-standard.org (official website and tools)"
---

# OCEL 2.0 Specification - Analysis Index

## Paper Overview

- **Source**: 09-OCEL_20_Specification.pdf
- **Chunks**: 4 chunks, ~26,500 estimated tokens
- **Analyzed**: 2025-12-28
- **Institution**: RWTH Aachen University, Process and Data Science Group
- **Version**: 2.0 (October 16, 2023)

## Key Extractions

### Core Contribution

OCEL 2.0 is the official specification for Object-Centric Event Logs, providing a standardized way to record and exchange event data that involves multiple objects per event. It addresses limitations of traditional case-centric event logs and the earlier OCEL 1.0 standard.

### Entity Types and Metamodel

| Entity | Definition | Source |
|--------|------------|--------|
| Event | Discrete action at specific time, atomic, typed | Chunk 1:149-154 |
| Object | Entity involved in events (physical or abstract) | Chunk 1:164-168 |
| Event Type | Category of events (also called "activity") | Chunk 1:157-161 |
| Object Type | Category of objects | Chunk 1:170-171 |
| E2O Relationship | Qualified event-to-object association | Chunk 1:178-185 |
| O2O Relationship | Qualified object-to-object relationship | Chunk 1:191-194 |

### OCEL 2.0 Extensions over OCEL 1.0

| Feature | Description | Source |
|---------|-------------|--------|
| O2O Relationships | Objects can relate to other objects outside events | Chunk 1:286-290 |
| Dynamic Object Attributes | Attribute values can change over time | Chunk 1:293-297 |
| Relationship Qualifiers | Both E2O and O2O relationships can be qualified | Chunk 1:306-308 |
| Relational Format | SQLite-based storage with dense tables | Chunk 1:316-321 |

### Formal Definition (OCEL Tuple)

The complete formal definition from Chunk 1:395-440:

```
L = (E, O, EA, OA, evtype, time, objtype, eatype, oatype, eaval, oaval, E2O, O2O)
```

Where:
- E: Set of events
- O: Set of objects
- EA, OA: Event and object attributes
- evtype, objtype: Type assignment functions
- time: Timestamp function
- eatype, oatype: Attribute type assignment
- eaval, oaval: Attribute value functions
- E2O: Qualified event-to-object relations
- O2O: Qualified object-to-object relations

### Implementation Formats

| Format | Description | Validation Schema |
|--------|-------------|-------------------|
| SQLite | Relational database with dense tables | SQL constraints |
| XML | Hierarchical with type definitions | XSD (ocel20-schema-xml.xsd) |
| JSON | Lightweight web-native format | JSON Schema (ocel20-schema-json.json) |

### Relevance to Research Questions

**Entity Definitions**: OCEL 2.0 provides precise formal definitions for Event, Object, and their relationships - directly relevant to understanding the Event entity in the 8-entity hypothesis.

**Framework Comparison**: Explicitly positions itself relative to XES (IEEE standard) and OCEL 1.0, providing clear evolution path in process mining standards.

**AI Integration Potential**: Authors explicitly mention that standardized object/event type taxonomies "create possibilities for both generative and discriminative AI" (Chunk 4:401-405).

## Chunk Navigation

### Chunk 1: Introduction, Metamodel, and Formal Definitions
- **Summary**: Introduces OCEL 2.0, explains limitations of traditional process mining, presents the metamodel (Figure 1), provides complete formal definitions (Definitions 1-2), and begins the running example.
- **Key concepts**: [OCPM, flattening problem, metamodel, formal universes, OCEL tuple, E2O, O2O]
- **Key quotes**:
  - Line 33-39: "OCEL 2.0 forms the new, more expressive standard... Compared to XES, it is more expressive, less complicated, and better readable"
  - Line 134-135: "Object-Centric Process Mining (OCPM) represents a paradigm shift"
  - Line 395-396: "An Object-Centric Event Log (OCEL) is a tuple L = (E, O, EA, OA, evtype, time, objtype, eatype, oatype, eaval, oaval, E2O, O2O)"
- **Load when**: User asks about OCEL 2.0 definition, event-object relationships, formal process mining ontology, or XES comparison

### Chunk 2: Relational Implementation and XML Format
- **Summary**: Details the SQLite relational implementation with dense tables, event/object type tables, E2O/O2O relationship tables. Begins XML format specification with example code.
- **Key concepts**: [SQLite, dense tables, event_map_type, object_map_type, foreign keys, E2O table, O2O table, XML schema]
- **Key quotes**:
  - Line 10-13: "we also create two additional tables, hosting the event/object identifiers... to allow for the definition of E2O/O2O tables with proper foreign keys"
  - Line 275-277: "The event_object table contains the event-to-object relationships (E2O in Definition 2)"
- **Load when**: User asks about OCEL 2.0 database implementation, relational schema, SQL storage, or E2O/O2O table structure

### Chunk 3: XML Schema and JSON Format
- **Summary**: Completes XML example, provides full XSD validation schema, introduces JSON format with example code. Shows how object attributes track temporal changes.
- **Key concepts**: [XSD validation, key/keyref constraints, JSON format, temporal attributes, relationship qualifiers in XML/JSON]
- **Key quotes**:
  - Line 122-124: "A machine-readable XML Schema Definition (XSD) file is provided to check whether an example XML OCEL 2.0 is valid"
  - Line 457-458: "The JSON format provides a lightweight structure for web-native process mining applications"
- **Load when**: User asks about OCEL 2.0 XML or JSON format, schema validation, or temporal attribute tracking

### Chunk 4: JSON Schema and Conclusion
- **Summary**: Completes JSON example, provides JSON Schema definition, and concludes with benefits, future directions, and AI integration possibilities.
- **Key concepts**: [JSON Schema, standard object/event types, AI taxonomy, future directions, sustainability]
- **Key quotes**:
  - Line 339-345: "Given the increasing importance of Object-Centric Process Mining (OCPM), it is important to be able to standardize Object-Centric Event Data (OCED)"
  - Line 401-405: "It is possible to define taxonomies of object types and event types using inheritance notions. This creates possibilities for both generative and discriminative Artificial Intelligence (AI)"
  - Line 386-388: "We also hope that OCEL 2.0 will also be the basis for creating standard object and event types for different application domains"
- **Load when**: User asks about OCEL 2.0 future directions, AI integration, standard taxonomies, or domain-specific event types
