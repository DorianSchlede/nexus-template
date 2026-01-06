# Canonical Event Entity Model for UDWO Metamodel

**Synthesized from**: 11 ontology research papers
**Generated**: 2026-01-01
**Version**: 1.0

---

## Executive Summary

This document defines a canonical Event entity for the UDWO metamodel, synthesizing patterns from foundational ontologies (UFO, DOLCE, BFO), provenance standards (PROV-O), process mining specifications (OCEL 2.0, XES), and agentic workflow research. The Event entity serves as the atomic unit connecting agents, tasks, and data.

---

## 1. Core Definition

### 1.1 Event (Perdurant)

**Definition**: An Event is a concrete particular that unfolds in time, occupying a spatiotemporal region and accumulating temporal parts. Events are manifestations of dispositions inhering in participating entities.

**Key Properties**:
- **Temporal extent**: Events span temporal intervals (or instants for atomic events)
- **Modally fragile**: Events cannot be different from what they are; all properties are necessary
- **Participatory**: Events require participants (endurants/entities) to exist
- **Causal**: Events manifest dispositions and may cause state changes

### 1.2 Formal Axioms

```
# Core Event Axioms (from UFO, BFO, DOLCE)

Event(e) → ConcreteParticular(e)
Event(e) → ∃t (spans(e, t) ∧ TemporalRegion(t))
Event(e) → ∃p (participates(p, e) ∧ Entity(p))

# Modal fragility (UFO)
Event(e) ∧ constitutedBy(e, e') → □(exists(e) → constitutedBy(e, e'))

# Participation axiom (DOLCE)
Event(e) ∧ present(e, t) → ∃p (participates(p, e, t))

# Manifestation axiom (UFO)
manifests(e, d) → Event(e) ∧ Disposition(d)
```

---

## 2. Event Structure

### 2.1 Essential Attributes

| Attribute | Type | Required | Description | Source |
|-----------|------|----------|-------------|--------|
| `id` | UUID | Yes | Unique event identifier | OCEL, XES |
| `type` | EventType | Yes | Activity/event classification | OCEL, XES |
| `timestamp` | DateTime | Yes | When event occurred | All sources |
| `end_timestamp` | DateTime | No | For extended events | XES lifecycle |
| `lifecycle_state` | LifecycleState | No | Transition type (start, complete, etc.) | XES |

### 2.2 Temporal Properties

```yaml
temporal_properties:
  # Primary temporal marker
  timestamp:
    type: DateTime
    format: ISO8601
    description: "Point in time when event occurred or started"
    required: true

  # For extended events
  end_timestamp:
    type: DateTime
    format: ISO8601
    description: "Point in time when event completed (if extended)"
    required: false

  # Duration (computed or explicit)
  duration:
    type: Duration
    computed_from: "end_timestamp - timestamp"
    description: "Temporal extent of event"

  # Lifecycle transition (XES standard)
  lifecycle_transition:
    type: enum
    values: [schedule, assign, start, suspend, resume, complete, abort]
    description: "Lifecycle state change represented by event"
    default: "complete"
```

### 2.3 Relational Properties

```yaml
relational_properties:
  # Participants
  participants:
    type: Set[Entity]
    cardinality: "1..*"
    description: "Entities participating in event"

  # Primary performer (agent)
  performer:
    type: Agent
    cardinality: "0..1"
    description: "Agent that performed the event"

  # Objects affected
  affected_objects:
    type: Set[Object]
    cardinality: "0..*"
    description: "Objects whose state changed due to event"

  # Causal predecessors
  caused_by:
    type: Set[Event]
    cardinality: "0..*"
    description: "Events that caused this event"

  # Part-of hierarchy
  part_of:
    type: Event
    cardinality: "0..1"
    description: "Parent composite event if this is a temporal part"

  # Temporal parts
  temporal_parts:
    type: Set[Event]
    cardinality: "0..*"
    description: "Sub-events if this is a composite event"
```

---

## 3. Event Type Hierarchy

### 3.1 Base Classification (DOLCE/UFO-B)

```
Event (Perdurant)
├── Stative (cumulative)
│   ├── State (homeomeric - all parts same type)
│   └── Process (non-homeomeric - parts can differ)
└── Eventive (non-cumulative)
    ├── Achievement (atomic, instantaneous)
    └── Accomplishment (extended, has completion point)
```

### 3.2 Process Mining Classification

```
Event
├── LifecycleEvent
│   ├── ScheduleEvent
│   ├── StartEvent
│   ├── SuspendEvent
│   ├── ResumeEvent
│   ├── CompleteEvent
│   └── AbortEvent
└── AtomicEvent (default, no lifecycle)
```

### 3.3 Agentic Event Classification

```
AgenticEvent
├── Task
│   ├── DecomposeTask
│   ├── CreateTask
│   ├── DelegateTask
│   ├── ExecuteTask
│   ├── EvaluateResult
│   └── MergeResult
├── ToolInvocation
│   ├── AgentTool
│   └── AIModelInvocation
├── Transformation
│   ├── Aggregation
│   ├── Generation
│   ├── Refining
│   └── Split
└── WorkflowEvent
    ├── QueryEvent
    ├── RetrievalEvent
    ├── SynthesisEvent
    └── EvaluationEvent
```

---

## 4. Event-Entity Relationships

### 4.1 Participation Patterns

Based on DOLCE, UFO, and PROV-AGENT:

```yaml
participation_patterns:

  # Generic participation (DOLCE)
  participates:
    definition: "Entity participates in event during event's occurrence"
    formal: "PC(e, p, t) → Entity(e) ∧ Event(p) ∧ Time(t)"
    cardinality: "event requires at least one participant"

  # Constant participation (DOLCE)
  constant_participation:
    definition: "Entity participates throughout entire event"
    formal: "PCC(e, p) → ∀t(present(p, t) → PC(e, p, t))"

  # Agent association (PROV)
  was_associated_with:
    definition: "Agent had responsibility for activity"
    formal: "wasAssociatedWith(a, ag) → Activity(a) ∧ Agent(ag)"

  # Entity generation (PROV)
  was_generated_by:
    definition: "Entity was produced by activity completion"
    formal: "wasGeneratedBy(e, a) → Entity(e) ∧ Activity(a)"

  # Entity usage (PROV)
  used:
    definition: "Activity consumed entity as input"
    formal: "used(a, e) → Activity(a) ∧ Entity(e)"
```

### 4.2 Event-Object Correlation (OCEL 2.0)

```yaml
event_object_correlation:

  # Event-to-Object (E2O)
  E2O:
    definition: "Qualified many-to-many between events and objects"
    formal: "E2O ⊆ E × U_qual × O"
    qualifier_examples:
      - "created_by"
      - "processed_by"
      - "triggers"
      - "affects"

  # Object-to-Object (O2O)
  O2O:
    definition: "Object relationships outside event context"
    formal: "O2O ⊆ O × U_qual × O"
    qualifier_examples:
      - "part_of"
      - "derived_from"
      - "belongs_to"
```

---

## 5. State Change Mechanisms

How events cause state changes in participating entities:

### 5.1 Disposition Realization (UFO)

Events are manifestations of dispositions. When a disposition is realized, it produces an event that may change the disposition-bearer's state.

```
Disposition(d) ∧ inheres(d, e) ∧ realizes(ev, d)
  → Event(ev) ∧ participates(e, ev)
```

### 5.2 Quality Value Change (DOLCE)

Individual qualities can change their qualia (values) over time through events.

```
Quality(q) ∧ inheres(q, e) ∧ quale(q, v1, t1) ∧ Event(ev)
  ∧ during(ev, [t1, t2]) ∧ affects(ev, q)
  → quale(q, v2, t2) ∧ v1 ≠ v2
```

### 5.3 Dynamic Object Attributes (OCEL 2.0)

Object attributes change over time, tracked via timestamped attribute values.

```yaml
dynamic_attribute_change:
  function: "oaval: (O × OA × U_time) → U_val"
  semantics: "Object o has attribute oa with value v at time t"
  lookup: "oaval^[t]_oa(o) returns latest value at time t"
  epoch: "1970-01-01 00:00 UTC represents initial values"
```

### 5.4 Phase Transition (UFO)

Entities can transition between phases (anti-rigid sortals) through events.

```
Phase(p1) ∧ Phase(p2) ∧ Entity(e) ∧ instantiates(e, p1, t1)
  ∧ Event(ev) ∧ causes(ev, transition(e, p1, p2))
  → instantiates(e, p2, t2) ∧ t2 > t1
```

---

## 6. Temporal Ordering

### 6.1 Ordering Properties

```yaml
temporal_ordering:

  # Timestamp-based total ordering
  timestamp_order:
    type: "total order"
    definition: "e1.time < e2.time implies before(e1, e2)"
    source: "OCEL, XES"

  # Entity-local ordering (Event Knowledge Graphs)
  entity_local_order:
    type: "local total order per entity"
    definition: "directly-follows per entity, not global"
    advantage: "Avoids false convergence/divergence"

  # Temporal part ordering (UFO/BFO)
  temporal_part_order:
    type: "partial order via parthood"
    definition: "temporal_part(e1, e2) implies temporal containment"
```

### 6.2 Ordering Axioms

```
# Timestamp ordering (total)
∀e1, e2: e1.timestamp < e2.timestamp → before(e1, e2)

# Entity-local directly-follows
df(e1, e2, n) ↔ corr(e1, n) ∧ corr(e2, n)
  ∧ e1.time < e2.time
  ∧ ¬∃e'(corr(e', n) ∧ e1.time < e'.time < e2.time)

# Temporal parthood
temporal_part(e1, e2) → during(temporal_extent(e1), temporal_extent(e2))
```

---

## 7. Causation Patterns

### 7.1 Direct Causation

```yaml
causation_patterns:

  # Disposition realization (UFO)
  disposition_realization:
    pattern: "Disposition → Event"
    description: "Dispositions when realized produce events"
    formal: "realizes(e, d) → causes(triggering_event, e)"

  # Event foundation (UFO)
  event_foundation:
    pattern: "Event → Relator"
    description: "Events found relators/modes"
    example: "wedding event founds marriage relator"

  # Activity chaining (PROV)
  was_informed_by:
    pattern: "Activity → Activity"
    description: "a2 used entity generated by a1"
    formal: "wasInformedBy(a2, a1) → before(a1, a2)"

  # Error propagation (PROV-AGENT)
  error_propagation:
    pattern: "Error → Downstream errors"
    description: "Hallucinated output propagates across layers"
```

### 7.2 Causal Chain Tracing

```yaml
causal_chain:
  # Transitive delay analysis (Event Knowledge Graphs)
  delay_chain:
    definition: "Set of transitive predecessors that delayed event most"
    computation: "Recursively find event that delayed each predecessor most"

  # End-to-end lineage (PROV-AGENT)
  lineage:
    definition: "Complete causal chain from output back through all activities"
    components: ["agent reasoning", "prompts", "input data", "sensors"]
```

---

## 8. Implementation Considerations

### 8.1 Recommended Schema

```typescript
interface Event {
  // Identity
  id: UUID;
  type: EventType;

  // Temporal
  timestamp: DateTime;
  endTimestamp?: DateTime;
  lifecycleState?: LifecycleState;

  // Participants
  performer?: Agent;
  participants: Entity[];
  affectedObjects: Object[];

  // Correlations (OCEL-style)
  objectRelations: EventObjectRelation[];

  // Causation
  causedBy?: Event[];
  wasInformedBy?: Event[];

  // Composition
  partOf?: Event;
  temporalParts?: Event[];

  // Attributes
  attributes: Map<string, AttributeValue>;
}

interface EventObjectRelation {
  object: Object;
  qualifier: string;  // e.g., "created_by", "processes"
}
```

### 8.2 Storage Formats

| Format | Use Case | Sources |
|--------|----------|---------|
| OCEL 2.0 JSON/XML/SQLite | Process mining, multi-object | OCEL spec |
| XES | Single-case event logs | XES standard |
| Event Knowledge Graph (Neo4j) | Graph queries, df-analysis | Event KG paper |
| PROV-N / PROV-JSON | Provenance tracking | W3C PROV |

---

## 9. Validation Rules

```yaml
validation:

  # Temporal consistency
  temporal:
    - rule: "end_timestamp >= timestamp"
      description: "End cannot be before start"
    - rule: "∀ temporal_part p: during(p.extent, self.extent)"
      description: "Parts contained in whole"

  # Participation
  participation:
    - rule: "participants.size >= 1"
      description: "Events require at least one participant"
    - rule: "performer ∈ participants OR performer is null"
      description: "Performer must be a participant"

  # Causation
  causation:
    - rule: "∀ cause ∈ causedBy: cause.timestamp < self.timestamp"
      description: "Causes must precede effects"
    - rule: "¬(self ∈ causedBy)"
      description: "Events cannot cause themselves"
```

---

## 10. Cross-Framework Mapping

| UDWO Event | UFO | DOLCE | BFO | PROV | OCEL | XES |
|------------|-----|-------|-----|------|------|-----|
| Event | Perdurant | Perdurant | Process | Activity | Event | Event |
| timestamp | temporal part | qlT | spans | - | time | time:timestamp |
| type | - | - | - | - | evtype | concept:name |
| performer | participates | PC | participates_in | wasAssociatedWith | resource attr | org:resource |
| causedBy | constitutedBy | - | - | wasInformedBy | - | - |
| partOf | temporal part | P | temporal_part_of | - | - | - |

---

*Generated by Claude Opus 4.5 from temporal pattern extraction of 11 ontology research papers*
