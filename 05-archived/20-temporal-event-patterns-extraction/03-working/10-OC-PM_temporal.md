# Temporal/Event Pattern Extraction: OC-PM Object-Centric Process Mining

**Paper**: OC-PM: analyzing object-centric event logs and process models
**Authors**: Alessandro Berti, Wil M. P. van der Aalst (2022)
**Focus**: Object-centric process mining addressing convergence/divergence problems

---

## event_types

| Type | Description | Source |
|------|-------------|--------|
| Event | An occurrence with activity, timestamp, and related objects. Element from Ue with associated activity (piact), timestamp (pitime), attribute values (pivmap), and related objects (piomap) | Chunk 1:454-456 |
| Activity Event | An event associated with a specific activity from Uact universe (e.g., "place order", "check availability") | Chunk 1:226-227, 481-483 |
| Start Event | First event in an object's lifecycle; defines process initiation point | Chunk 1:616-617 |
| End Event | Last event in an object's lifecycle; defines process termination point | Chunk 1:619-620 |
| Lifecycle Event | Event that is part of an object's lifecycle sequence; the sequence of events to which an object is related | Chunk 1:601-611 |

---

## event_definitions

```yaml
Event:
  definition: "An element e from Ue with associated activity (piact: E -> Uact), timestamp (pitime: E -> Utimest), attribute values (pivmap: E -> (AN -> AV)), and related objects (piomap: E -> P(O))"
  temporal_properties:
    - "timestamp (pitime)"
    - "total ordering (<=)"
    - "position in lifecycle sequence"
  formal_notation: "E subseteq Ue is the set of event identifiers"
  source: "Chunk 1:454-456, 485-488, 526-527"

Activity:
  definition: "An element from Uact representing the action performed in an event"
  temporal_properties:
    - "start activity (first in lifecycle)"
    - "end activity (last in lifecycle)"
  formal_notation: "piact: E -> Uact associates an activity to each event"
  source: "Chunk 1:226-227, 481-483"

Lifecycle:
  definition: "The sequence of events to which an object is related, extracted via flattening"
  temporal_properties:
    - "ordered sequence of events"
    - "duration (last_timestamp - first_timestamp)"
    - "length (number of events)"
  formal_notation: "lif(o) = case_FL(L,piotyp(o))(o)"
  source: "Chunk 1:605-611"

Trace:
  definition: "The sequence of activities of the events belonging to an object's lifecycle"
  temporal_properties:
    - "activity sequence ordering"
    - "start activity"
    - "end activity"
  formal_notation: "trace(o) = trace_FL(L,piotyp(o))(o)"
  source: "Chunk 1:613-614"
```

---

## temporal_relations

| Relation | Domain | Range | Semantics | Source |
|----------|--------|-------|-----------|--------|
| directly-follows | Activity | Activity | Activity a2 directly follows a1 iff (a1, a2) appears consecutively in a trace; edge (a1, a2) in DFG exists iff a1 immediately precedes a2 in at least one case | Chunk 1:303-308, 346-368 |
| before (total order) | Event | Event | e1 <= e2 is a total order on events respecting antisymmetry, transitivity, and connexity | Chunk 1:250, 526-527 |
| during (lifecycle membership) | Event | Lifecycle | Event e belongs to lifecycle lif(o) iff o in piomap(e) | Chunk 1:609-611 |
| typed-directly-follows | Activity | Activity | (n1, ot, n2) in F where edge is typed by object type ot; captures object-type-specific flow | Chunk 1:781-782, 798-799 |
| start-of | Activity | Object | start(o) = first activity in trace(o); identifies process initiation | Chunk 1:616-617 |
| end-of | Activity | Object | end(o) = last activity in trace(o); identifies process termination | Chunk 1:619-620 |

---

## lifecycle_patterns

```yaml
- entity: "Object"
  states: ["created", "in-lifecycle", "completed"]
  transitions:
    - from: "created"
      to: "in-lifecycle"
      trigger: "First event correlation (piomap includes object)"
    - from: "in-lifecycle"
      to: "in-lifecycle"
      trigger: "Subsequent events in lifecycle sequence"
    - from: "in-lifecycle"
      to: "completed"
      trigger: "End activity reached (no more events correlated)"
  metrics:
    - "lifecycle duration: pitime(lif(o)(|lif(o)|)) - pitime(lif(o)(1))"
    - "lifecycle length: |lif(o)|"
  source: "Chunk 1:601-627, Chunk 2:89-101"

- entity: "Object (per Object Type)"
  states: ["start activity", "intermediate activities", "end activity"]
  transitions:
    - from: "start activity"
      to: "intermediate activities"
      trigger: "directly-follows edge traversal"
    - from: "intermediate activities"
      to: "end activity"
      trigger: "directly-follows edge to terminating activity"
  notes: "Each object type has distinct start/end nodes in OC-DFG (n_S,ot and n_E,ot)"
  source: "Chunk 1:773-779, 809-820"

- entity: "Process Execution (Case)"
  states: ["initiated", "executing", "terminated"]
  transitions:
    - from: "initiated"
      to: "executing"
      trigger: "First event in case"
    - from: "executing"
      to: "terminated"
      trigger: "Last event in case"
  source: "Chunk 1:48-52, 270-286"
```

---

## state_change_mechanisms

| Mechanism | Description | Source |
|-----------|-------------|--------|
| Event-to-Object correlation | Events cause state changes by correlating to objects via piomap; each event updates the object's lifecycle position | Chunk 1:502-505 |
| Lifecycle progression | Object state advances through lifecycle as new events are correlated; lifecycle = ordered sequence of events | Chunk 1:609-611 |
| Activity occurrence | Each activity occurrence is an event that marks a state transition in the process | Chunk 1:481-483 |
| Attribute value assignment | Events carry attribute values (pivmap) that can represent state data at event time | Chunk 1:490-500 |
| Object attribute values | Objects have static attributes (piovmap) representing object state properties | Chunk 1:514-524 |
| Conformance violation detection | CC2 rule detects objects with lifecycle duration outside bounds (anomalous state progression) | Chunk 2:89-101 |

---

## agent_participation

| Participation Type | Description | Source |
|--------------------|-------------|--------|
| resource | Agent/resource attribute at event level; identifies who performed the activity | Chunk 1:424-425, 459-460 |
| N/A - not explicitly modeled | Paper focuses on object-event correlation, not agent/resource modeling in depth | General observation |

**Note**: The OC-PM paper does not extensively model agent participation. The "resource" attribute is mentioned as an example event attribute, but no formal agent participation ontology is defined. This is a limitation for UDWO metamodel extraction.

---

## event_correlation

| Pattern | Description | Source |
|---------|-------------|--------|
| Event-to-Object (piomap) | Many-to-many correlation: piomap: E -> P(O) associates each event to a set of related object identifiers. Resolves convergence problem. | Chunk 1:502-505 |
| Object-to-ObjectType (piotyp) | One-to-one correlation: piotyp in O -> OT assigns precisely one object type to each object | Chunk 1:510-512 |
| Event-to-Activity (piact) | One-to-one correlation: piact: E -> Uact maps each event to exactly one activity | Chunk 1:481-483 |
| Event-to-Timestamp (pitime) | One-to-one correlation: pitime: E -> Utimest maps each event to exactly one timestamp | Chunk 1:485-488 |
| Event-to-Case (traditional) | One-to-many correlation: picase: E -> P(Uc) \ {} - causes convergence problem when same event in multiple cases | Chunk 1:247-248, 69-78 |
| Flattening correlation | FL(L, ot) transforms object-centric log to traditional log by choosing object type as case notion | Chunk 1:555-598 |

### Convergence/Divergence Problem

**Convergence Problem**: Same event relates to different cases/objects. In XES format, this leads to event replication.

**Divergence Problem**: Case contains different instances of same activity (e.g., multiple "pack item" events for one order).

**OC-PM Solution**: Object-centric event logs allow events to relate to multiple objects of different types simultaneously, avoiding artificial case boundaries.

Source: Chunk 1:69-78, 79-101

---

## ordering_mechanisms

| Mechanism | Description | Source |
|-----------|-------------|--------|
| Total order (<=) | Events have a total order respecting antisymmetry, transitivity, and connexity properties | Chunk 1:250, 526-527 |
| Timestamp ordering | Events ordered by pitime: E -> Utimest; timestamps are totally ordered with difference operation (seconds) | Chunk 1:229-232, 244-245 |
| Lifecycle sequence | lif(o) provides ordered sequence of events for object o based on timestamp ordering | Chunk 1:605-611 |
| Trace ordering | trace(o) = sequence of activities from lifecycle, preserving temporal order | Chunk 1:613-614 |
| OC-DFG (Object-Centric Directly-Follows Graph) | Multigraph with typed edges (n1, ot, n2) capturing activity sequences per object type | Chunk 1:764-786 |
| DFG edge discovery | Edge (a1, a2) exists iff a1 directly precedes a2 in at least one case trace | Chunk 1:346-368 |
| Per-object-type ordering | Flattening creates separate orderings per object type; OC-DFG collapses these into typed edges | Chunk 1:584-598, 788-791 |

---

## causation_patterns

| Pattern | Description | Source |
|---------|-------------|--------|
| Directly-follows causation | Activity a1 causally precedes a2 if (a1, a2) edge exists in DFG; implies potential causal relationship | Chunk 1:303-308 |
| Lifecycle causation | Events in lifecycle sequence form causal chain; earlier events are prerequisites for later events | Chunk 1:601-627 |
| N/A - explicit causation | Paper does not formally define causal relationships beyond temporal ordering | General observation |

**Note**: OC-PM focuses on temporal ordering (directly-follows) rather than explicit causal semantics. The directly-follows relationship is observational (temporal precedence) rather than causal (one event causes another).

---

## temporal_standards

| Standard | Description | Source |
|----------|-------------|--------|
| ISO 8601 timestamps | Utimest examples follow ISO 8601 format: "2020-07-09T08:21:01.527+01:00" | Chunk 1:229-230 |
| OCEL format | Object-centric event log standard with JSON-OCEL and XML-OCEL implementations | Chunk 1:529-533 |
| XES format | Traditional event log format (IEEE standard); causes convergence problem with multi-case events | Chunk 1:71, 255-257 |
| Duration calculation | Difference operation: pitime(e2) - pitime(e1) = seconds between events | Chunk 1:231-232 |

---

## event_log_formats

| Format | Description | Source |
|--------|-------------|--------|
| OCEL (Object-Centric Event Log) | Tuple L = (E, AN, AV, AT, OT, O, pitype, piact, pitime, pivmap, piomap, piotyp, piovmap, <=) with 14 components | Chunk 1:448-527 |
| JSON-OCEL | JSON implementation of OCEL format | Chunk 1:529-530 |
| XML-OCEL | XML implementation of OCEL format | Chunk 1:529-530 |
| MongoDB storage | Scalable database storage for OCEL | Chunk 1:530 |
| XES (traditional) | IEEE standard for traditional event logs; single case per event | Chunk 1:71, Chunk 2:285 |

---

## Key Concepts for UDWO Metamodel

### 1. Event-Object Correlation Model

The paper formalizes a many-to-many relationship between events and objects:

```
piomap: E -> P(O)   -- Event to set of Objects
piotyp: O -> OT     -- Object to ObjectType
piact: E -> Uact    -- Event to Activity
pitime: E -> Utimest -- Event to Timestamp
```

This resolves the convergence/divergence problem in traditional process mining.

### 2. Lifecycle Formalization

Object lifecycle is formally defined as:
- **lif(o)**: Ordered sequence of events related to object o
- **trace(o)**: Sequence of activities from lifecycle events
- **start(o)**: First activity in trace
- **end(o)**: Last activity in trace

### 3. Temporal Ordering Hierarchy

1. **Global**: Total order <= on all events
2. **Per-Object**: Lifecycle sequence per object
3. **Per-ObjectType**: Flattened log ordering
4. **Per-Activity-Pair**: Directly-follows frequency

### 4. Object-Centric DFG Structure

```
OC-DFG = (A, OT, N, F, pi_freqn, pi_freqe)
- A: Activities
- OT: Object types
- N: Nodes = A + start/end nodes per type
- F: Typed edges (n1, ot, n2)
- pi_freqn: Node frequencies
- pi_freqe: Edge frequencies
```

### 5. Conformance Metrics

- **CC1**: Number of objects per event bounds checking
- **CC2**: Lifecycle duration bounds checking (temporal anomaly detection)

---

## Limitations for UDWO

1. **No explicit agent modeling**: Resource is just an attribute, not a first-class entity
2. **No causal semantics**: Only temporal ordering (directly-follows), not true causation
3. **Static object attributes**: piovmap doesn't capture attribute change over time (addressed in OCEL 2.0)
4. **No lifecycle states**: Objects don't have explicit states, only event sequences
5. **No event lifecycle**: Events are atomic, no transactional lifecycle (started/completed)

---

## Quality Checklist

- [x] event_types extracted with chunk:line references
- [x] event_definitions with temporal properties and formal notation
- [x] temporal_relations with domain/range/semantics (6 relations)
- [x] lifecycle_patterns with states/transitions (3 patterns)
- [x] state_change_mechanisms (6 mechanisms)
- [x] agent_participation - limited, marked as gap
- [x] event_correlation patterns (6 patterns + convergence/divergence explanation)
- [x] ordering_mechanisms (7 mechanisms)
- [x] causation_patterns - limited, noted as observational not causal
- [x] temporal_standards (4 standards)
- [x] event_log_formats (5 formats)

---

**Extraction Version**: 1.0
**Extracted**: 2026-01-01
**Extractor**: Claude (Project 20 - Temporal Event Patterns)
