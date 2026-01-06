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
extraction_type: "temporal_event_patterns"
extraction_version: "1.0"
extraction_date: "2026-01-01"

event_types:
  - type: "Event"
    description: "Discrete, atomic action with timestamp representing actions or activities within a system. Events are unique, do not take time (instantaneous), have a timestamp and additional attributes. Each event belongs to exactly one Event Type."
    source: "Chunk 1:149-154"
  - type: "Event Type (Activity)"
    description: "Category of events based on their nature or function. Examples include Order Created, Order Approved, Invoice Sent. Each event is of exactly one type. The term 'activity' is used synonymously."
    source: "Chunk 1:157-161"

event_definitions:
  Event:
    definition: "Discrete, atomic actions within a system/process representing specific actions or observations at a specific point in time. Events are atomic (do not take time), have a timestamp, and may have additional typed attributes."
    temporal_properties:
      - "timestamp (time: E -> U_time)"
    source: "Chunk 1:149-154, 411"
    formal: "e in U_ev; time: E -> U_time assigns timestamps to events"
  Event_Type:
    definition: "Categories of events (activities) based on their nature or function. Each event is of exactly one type via evtype function."
    temporal_properties: []
    source: "Chunk 1:157-161, 408"
    formal: "evtype: E -> U_etype assigns types to events"
  OCEL:
    definition: "Object-Centric Event Log tuple L = (E, O, EA, OA, evtype, time, objtype, eatype, oatype, eaval, oaval, E2O, O2O) - complete formal structure for object-centric event data"
    temporal_properties:
      - "time: E -> U_time (event timestamps)"
      - "oaval: (O x OA x U_time) -> U_val (time-varying object attributes)"
    source: "Chunk 1:395-440"

temporal_relations:
  - relation: "timestamp-ordering"
    domain: "Event"
    range: "Event"
    semantics: "Total ordering on timestamps, with 0 as earliest and infinity as latest. For any t in U_time: 0 <= t <= infinity. Events are ordered by their assigned timestamp."
    source: "Chunk 1:382-388"
  - relation: "directly-follows (implicit)"
    domain: "Event"
    range: "Event"
    semantics: "Implicit via timestamp ordering - events related to same object can be ordered to form directly-follows relations per object lifecycle (basis for process discovery techniques)"
    source: "Chunk 1:115-127 (context of DFGs mentioned)"

lifecycle_patterns:
  - entity: "Object"
    states: ["initial", "modified", "final"]
    transitions:
      - from: "initial"
        to: "modified"
        trigger: "Event with E2O relationship that causes attribute change"
      - from: "modified"
        to: "modified"
        trigger: "Subsequent event with E2O relationship that changes attribute value"
      - from: "modified"
        to: "final"
        trigger: "No further events; oaval_oa(o) = oaval_oa^[infinity](o)"
    source: "Chunk 1:293-297, 476-498"
    note: "OCEL 2.0 tracks object attribute values over time via oaval function with timestamp parameter"
  - entity: "Invoice (example from running scenario)"
    states: ["created (is_blocked=No)", "blocked (is_blocked=Yes)", "unblocked (is_blocked=No)"]
    transitions:
      - from: "created"
        to: "blocked"
        trigger: "Set Payment Block event"
      - from: "blocked"
        to: "unblocked"
        trigger: "Remove Payment Block event"
    source: "Chunk 2:236-255 (Table 18)"
  - entity: "Purchase Order (example from running scenario)"
    states: ["initial quantity", "modified quantity"]
    transitions:
      - from: "initial quantity"
        to: "modified quantity"
        trigger: "Change PO Quantity event"
    source: "Chunk 2:220-235 (Table 17)"

state_change_mechanisms:
  - mechanism: "Dynamic object attribute update via oaval"
    description: "OCEL 2.0 allows object attribute values to change over time. oaval: (O x OA x U_time) -> U_val assigns values to object attributes at specific timestamps. The function oaval^[t]_oa(o) returns the latest attribute value at time t by finding the most recent timestamp t' <= t where a value was recorded."
    source: "Chunk 1:293-297, 433, 476-498"
  - mechanism: "Epoch initialization"
    description: "Rows with timestamp 1970-01-01 00:00 UTC (epoch = 0 in Definition 2) represent initial values of all attributes for a given object. This provides consistent starting point across all objects."
    source: "Chunk 2:182-188"
  - mechanism: "Changed field tracking"
    description: "In relational format, rows with non-epoch timestamps include ocel_changed_field column indicating which specific attribute changed at that time."
    source: "Chunk 2:191-192"
  - mechanism: "Time-bounded attribute validity"
    description: "An attribute value recorded at time t' is valid from t' until an attribute with the same name and greater timestamp is recorded. This creates temporal intervals of attribute validity."
    source: "Chunk 2:481-485 (XML format description)"

agent_participation:
  - participation_type: "performs"
    description: "Resources (human or Robot) perform activities. Tracked via event attributes like pr_creator, pr_approver, po_creator, po_editor, invoice_inserter, invoice_blocker, invoice_block_rem, payment_inserter."
    source: "Chunk 1:667-683"
  - participation_type: "automated-performs"
    description: "Robot/automated agents can perform events. Example: payment_inserter: Robot for Insert Payment events (e7, e8, e13)."
    source: "Chunk 2:162-164"
  - participation_type: "E2O-qualified-participation"
    description: "Event-to-Object relationships can be qualified to describe the role an object plays in event occurrence. Example: distinguishing regular participants from meeting organizer."
    source: "Chunk 1:178-185"

event_correlation:
  - pattern: "Event-to-Object (E2O)"
    description: "Events are associated with objects via qualified many-to-many relationships. E2O subset of E x U_qual x O. An event can relate to multiple objects, and each relationship has a qualifier describing the role (e.g., 'Invoice created with identifier', 'Payment for the invoice')."
    source: "Chunk 1:178-185, 436"
  - pattern: "Object-to-Object (O2O)"
    description: "Objects can be related to other objects outside event context via qualified relationships. O2O subset of O x U_qual x O. Examples: part-of, reports-to, belongs-to, 'PO from PR', 'Invoice from PO'."
    source: "Chunk 1:191-194, 439"
  - pattern: "Qualified relationships (E2O)"
    description: "E2O qualifiers describe the role an object plays in a specific event occurrence. Same object can have different qualifiers for same event. Examples: 'Regular placement of PR', 'Created order from PR', 'Invoice created starting from the PO'."
    source: "Chunk 1:306-308; Chunk 2:286-314 (Table 20)"
  - pattern: "Qualified relationships (O2O)"
    description: "O2O qualifiers characterize associations between objects. Same pair of objects can be related through different qualifiers. Examples: 'PO from PR', 'Invoice from PO', 'Payment from invoice', 'Maverick buying'."
    source: "Chunk 1:306-308; Chunk 2:319-342 (Table 21)"
  - pattern: "Multi-object event correlation"
    description: "Unlike traditional event logs where events relate to single case, OCEL 2.0 events can relate to multiple objects of different types simultaneously. Example: e3 relates to both PR1 and PO1."
    source: "Chunk 1:92-94, 120-121, 178-180"

ordering_mechanisms:
  - mechanism: "Timestamp ordering"
    description: "Total ordering on timestamps with 0 as smallest element (earliest) and infinity as largest (latest). For any t in U_time: 0 <= t <= infinity. Concrete implementations use ISO 8601 time format."
    source: "Chunk 1:368-369, 382-388"
  - mechanism: "Object attribute temporal ordering"
    description: "Object attribute values are ordered by timestamp via oaval function. oaval^[t]_oa(o) finds latest value at time t by locating most recent t' <= t where (o, oa, t') in dom(oaval). Missing timestamps interpreted as time 0."
    source: "Chunk 1:482-498"
  - mechanism: "Epoch reference point"
    description: "1970-01-01 00:00 UTC serves as epoch (0) for initial attribute values, providing consistent reference frame across all objects."
    source: "Chunk 2:182-188"

causation_patterns:
  - pattern: "Event-triggered attribute change"
    description: "Events implicitly cause object attribute changes. While OCEL 2.0 does not explicitly link events to attribute changes, the timestamp correlation allows inferring that events at time t may have caused attribute changes recorded at same timestamp."
    source: "Chunk 1:293-297, 616-622"
  - pattern: "Process flow causation (implicit)"
    description: "E2O and O2O relationships combined with timestamps enable reconstruction of process flows. Example: PR1 created -> PR1 approved -> PO1 created from PR1 -> invoices from PO1 -> payments for invoices."
    source: "Chunk 1:638-650 (running example scenario)"

temporal_standards:
  - standard: "ISO 8601"
    description: "Timestamp format for event occurrence times in concrete implementations. Used in XML, JSON, and SQLite formats."
    source: "Chunk 1:387-388; Chunk 2:412-413"
  - standard: "UNIX Epoch (1970-01-01 00:00:00 UTC)"
    description: "Reference timestamp representing time 0 for initial object attribute values. Provides consistent starting point across all objects."
    source: "Chunk 2:182-188"

event_log_formats:
  - format: "OCEL 2.0 Relational (SQLite)"
    description: "Dense table structure with separate tables per event/object type. Includes: event_map_type, object_map_type, event, object, event_<type> tables (with timestamp and attributes), object_<type> tables (with timestamp, attributes, changed_field), event_object (E2O with qualifier), object_object (O2O with qualifier)."
    source: "Chunk 1:316-321, 801-846"
    url: "https://www.ocel-standard.org/2.0/ocel20-schema-relational.pdf"
  - format: "OCEL 2.0 XML"
    description: "Hierarchical XML structure with object-types, event-types, objects, events elements. Events have id, type, time attributes. Objects have time-stamped attributes for tracking changes. XSD validation available."
    source: "Chunk 2:410-502"
    url: "https://www.ocel-standard.org/2.0/ocel20-schema-xml.xsd"
  - format: "OCEL 2.0 JSON"
    description: "Lightweight structure with top-level arrays: eventTypes, objectTypes, events, objects. Events have id, type, time (ISO format), attributes array, relationships array. Objects have time-stamped attributes. JSON Schema validation available."
    source: "Chunk 3:455-481"
    url: "https://www.ocel-standard.org/2.0/ocel20-schema-json.json"

fundamental_universes:
  - universe: "U_ev"
    description: "Universe of events - unique event identifiers"
    source: "Chunk 1:350"
  - universe: "U_etype"
    description: "Universe of event types (activities)"
    source: "Chunk 1:353"
  - universe: "U_obj"
    description: "Universe of objects - unique object identifiers"
    source: "Chunk 1:356"
  - universe: "U_otype"
    description: "Universe of object types"
    source: "Chunk 1:359"
  - universe: "U_attr"
    description: "Universe of attribute names"
    source: "Chunk 1:362"
  - universe: "U_val"
    description: "Universe of attribute values"
    source: "Chunk 1:365"
  - universe: "U_time"
    description: "Universe of timestamps (with 0 as smallest, infinity as largest)"
    source: "Chunk 1:368-369"
  - universe: "U_qual"
    description: "Universe of qualifiers (for E2O and O2O relationships)"
    source: "Chunk 1:372"

key_formal_functions:
  - function: "evtype: E -> U_etype"
    description: "Assigns event types to events"
    source: "Chunk 1:408"
  - function: "time: E -> U_time"
    description: "Assigns timestamps to events"
    source: "Chunk 1:411"
  - function: "objtype: O -> U_otype"
    description: "Assigns object types to objects"
    source: "Chunk 1:424"
  - function: "eaval: (E x EA) -> U_val"
    description: "Assigns values to event attributes (partial function)"
    source: "Chunk 1:420-421"
  - function: "oaval: (O x OA x U_time) -> U_val"
    description: "Assigns values to object attributes at specific times (partial function, enables dynamic attributes)"
    source: "Chunk 1:433"
  - function: "oaval^[t]_oa(o)"
    description: "Returns latest object attribute value at time t (semantic helper function)"
    source: "Chunk 1:482-489"
  - function: "E2O subset of E x U_qual x O"
    description: "Qualified event-to-object relations"
    source: "Chunk 1:436"
  - function: "O2O subset of O x U_qual x O"
    description: "Qualified object-to-object relations"
    source: "Chunk 1:439"

improvements_over_ocel_1:
  - improvement: "Dynamic Object Attribute Values"
    description: "Object attributes can now change over time, tracked via oaval with timestamp parameter. Provides realistic view of process instances where object attributes evolve."
    source: "Chunk 1:293-297"
  - improvement: "Object-to-Object (O2O) Relationships"
    description: "Objects can be directly related to other objects outside event context. Reveals insights about process performance through network analysis."
    source: "Chunk 1:286-290"
  - improvement: "Relationship Qualifiers"
    description: "Both E2O and O2O relationships can be qualified to describe the nature/role of the relationship."
    source: "Chunk 1:306-308"

ai_integration_notes:
  - note: "Taxonomy-based AI enablement"
    description: "Standardized object and event types using inheritance notions create possibilities for both generative and discriminative AI applications."
    source: "Chunk 4:400-405"
  - note: "System-agnostic data foundation"
    description: "OCEL 2.0 enables creation of system-agnostic single source of truth for AI/ML applications in process mining."
    source: "Chunk 4:349-351"
---

# OCEL 2.0 Temporal Event Patterns Extraction

## Summary

OCEL 2.0 provides a comprehensive formal model for object-centric event data with strong temporal semantics. The specification defines 8 fundamental universes (events, event types, objects, object types, attributes, values, timestamps, qualifiers) and formal functions for tracking events and their relationships to objects over time.

## Key Temporal Contributions for UDWO

### 1. Event Model
- **Atomic events**: Events are instantaneous (do not take time) and occur at specific timestamps
- **Typed events**: Each event belongs to exactly one Event Type (activity)
- **Event attributes**: Events have type-specific attributes with values

### 2. Temporal Ordering
- **Total timestamp ordering**: 0 <= t <= infinity for all timestamps
- **ISO 8601**: Concrete implementation standard for timestamps
- **Epoch reference**: 1970-01-01 00:00 UTC as time 0 for initial values

### 3. Dynamic Object State
- **Time-varying attributes**: oaval(O x OA x U_time) -> U_val tracks attribute changes
- **Temporal lookup**: oaval^[t]_oa(o) returns latest value at any time t
- **State history**: Complete audit trail of object attribute changes over time

### 4. Qualified Relationships
- **E2O (Event-to-Object)**: Many-to-many with qualifiers describing role
- **O2O (Object-to-Object)**: Direct object relationships with qualifiers
- **Multi-object correlation**: Events relate to multiple objects simultaneously

### 5. Lifecycle Implicit Patterns
- Objects transition through states via events that change their attributes
- Event sequences per object enable directly-follows graph construction
- Process discovery leverages E2O relationships and timestamps

## Relevance to UDWO Metamodel

| OCEL 2.0 Concept | UDWO Mapping Suggestion |
|------------------|-------------------------|
| Event (atomic, timestamped) | Event entity with start_time = end_time |
| Event Type | Activity type classification |
| Object | Participant/Entity with lifecycle |
| oaval with timestamp | State change mechanism |
| E2O qualified | Event-Entity participation with role |
| O2O qualified | Entity-Entity relationship |
| U_time ordering | Temporal ordering constraint |
| Dynamic attributes | Entity state transitions |

## Notable Quotes

> "Events are atomic (i.e., do not take time), have a timestamp, and may have additional attributes." (Chunk 1:152-153)

> "OCEL 2.0 adopts a dynamic approach where attribute values can change over time." (Chunk 1:293-294)

> "Using OCEL 2.0, it is possible to create a system-agnostic, single source of truth." (Chunk 4:349)

## Quality Checklist

- [x] All HIGH priority fields extracted (event_types, event_definitions, temporal_relations, lifecycle_patterns, state_change_mechanisms, agent_participation, event_correlation)
- [x] Every extraction has chunk:line reference
- [x] Temporal relation vocabulary standardized
- [x] Lifecycle states form valid FSM (initial -> modified -> final)
- [x] Agent participation types use controlled vocabulary (performs, automated-performs)
- [x] Event definitions include temporal properties
