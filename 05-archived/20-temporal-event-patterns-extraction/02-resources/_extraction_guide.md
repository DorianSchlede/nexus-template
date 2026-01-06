# Extraction Guide: Temporal Event Patterns

**Purpose**: Ensure consistent extraction of temporal and event-related concepts from ontology papers.

---

## Field Definitions

### Field: event_types
**Definition**: Types of events/perdurants defined in the paper
**Format**: Array of objects with `type`, `description`, `source` keys
**Priority**: HIGH

**Example GOOD extraction**:
```yaml
event_types:
  - type: "Atomic Event"
    description: "Instantaneous occurrence with no duration"
    source: "Chunk 1:145-152"
  - type: "Process"
    description: "Extended event with temporal parts that unfolds over time"
    source: "Chunk 1:156-163"
  - type: "State"
    description: "Homeomeric process where all temporal parts are same type"
    source: "Chunk 2:34-41"
```

**Example BAD extraction**:
```yaml
event_types:
  - "events"
  - "things that happen"
```

---

### Field: event_definitions
**Definition**: Formal definitions of events with temporal properties
**Format**: Object with event type as key, definition object as value
**Priority**: HIGH

**Example GOOD extraction**:
```yaml
event_definitions:
  Event:
    definition: "A perdurant that occupies a temporal region and has temporal parts"
    temporal_properties:
      - "start_time"
      - "end_time"
      - "duration"
    source: "Chunk 1:189-196"
  Activity:
    definition: "A process that depends on exactly one agent"
    temporal_properties:
      - "wasStartedBy"
      - "wasEndedBy"
    source: "Chunk 2:45-52"
```

**Example BAD extraction**:
```yaml
event_definitions:
  Event: "something that happens"
```

---

### Field: temporal_relations
**Definition**: Relations between events (ordering, overlap, causation)
**Format**: Array of objects with `relation`, `domain`, `range`, `semantics`, `source`
**Priority**: HIGH

**Example GOOD extraction**:
```yaml
temporal_relations:
  - relation: "directly-follows"
    domain: "Event"
    range: "Event"
    semantics: "e2 directly follows e1 iff e1.end <= e2.start and no event between"
    source: "Chunk 3:67-74"
  - relation: "during"
    domain: "Event"
    range: "Event"
    semantics: "e1 during e2 iff e1.start > e2.start AND e1.end < e2.end"
    source: "Chunk 3:78-85"
  - relation: "triggers"
    domain: "Event"
    range: "Event"
    semantics: "e1 triggers e2 iff e1 causally initiates e2"
    source: "Chunk 4:23-30"
```

**Controlled vocabulary for temporal relations**:
| Paper Uses | Standardize To |
|------------|----------------|
| "precedes", "before", "prior to" | "before" |
| "follows", "after", "subsequent to" | "after" |
| "overlaps", "concurrent", "simultaneous" | "overlaps" |
| "during", "within", "contained by" | "during" |
| "triggers", "initiates", "starts" | "triggers" |
| "causes", "leads to", "results in" | "causes" |

---

### Field: lifecycle_patterns
**Definition**: Event/object lifecycle states and valid transitions
**Format**: Array of objects with `entity`, `states`, `transitions`, `source`
**Priority**: HIGH

**Example GOOD extraction**:
```yaml
lifecycle_patterns:
  - entity: "Activity"
    states: ["scheduled", "started", "suspended", "completed", "aborted"]
    transitions:
      - from: "scheduled"
        to: "started"
        trigger: "wasStartedBy"
      - from: "started"
        to: "completed"
        trigger: "wasEndedBy"
      - from: "started"
        to: "suspended"
        trigger: "wasSuspendedBy"
    source: "Chunk 2:112-125"
  - entity: "Object"
    states: ["created", "active", "archived", "deleted"]
    transitions:
      - from: "created"
        to: "active"
        trigger: "first event correlation"
    source: "Chunk 3:45-58"
```

---

### Field: state_change_mechanisms
**Definition**: How events cause state changes in objects/agents
**Format**: Array of objects with `mechanism`, `description`, `source`
**Priority**: HIGH

**Example GOOD extraction**:
```yaml
state_change_mechanisms:
  - mechanism: "Dynamic attribute update"
    description: "OCEL 2.0 allows object attributes to change over time via events"
    source: "Chunk 1:293-297"
  - mechanism: "Disposition realization"
    description: "UFO-B: Events realize dispositions, causing state changes in endurants"
    source: "Chunk 2:67-75"
  - mechanism: "wasGeneratedBy"
    description: "PROV-O: Entity comes into existence through Activity completion"
    source: "Chunk 3:34-41"
```

---

### Field: agent_participation
**Definition**: How agents participate in events
**Format**: Array of objects with `participation_type`, `description`, `source`
**Priority**: HIGH

**Example GOOD extraction**:
```yaml
agent_participation:
  - participation_type: "initiates"
    description: "Agent starts an activity through intentional action"
    source: "Chunk 2:89-96"
  - participation_type: "performs"
    description: "Agent executes the activity as the responsible party"
    source: "Chunk 2:98-105"
  - participation_type: "observes"
    description: "Agent perceives event without active participation"
    source: "Chunk 3:23-30"
  - participation_type: "wasAssociatedWith"
    description: "PROV-O: Agent had some role in Activity"
    source: "Chunk 4:56-63"
```

**Controlled vocabulary**:
| Paper Uses | Standardize To |
|------------|----------------|
| "performs", "executes", "carries out" | "performs" |
| "initiates", "starts", "begins" | "initiates" |
| "observes", "witnesses", "perceives" | "observes" |
| "is affected by", "receives", "undergoes" | "is-affected-by" |

---

### Field: event_correlation
**Definition**: How events are correlated to cases, objects, agents
**Format**: Array of objects with `pattern`, `description`, `source`
**Priority**: HIGH

**Example GOOD extraction**:
```yaml
event_correlation:
  - pattern: "Event-to-Object (E2O)"
    description: "Events relate to multiple objects with qualified relationships"
    source: "Chunk 1:178-185 (OCEL 2.0)"
  - pattern: "Case correlation"
    description: "Each event linked to case ID for process instance identification"
    source: "Chunk 2:68-72"
  - pattern: "Resource correlation"
    description: "Events correlated to actors/resources who performed them"
    source: "Chunk 3:45-52"
```

---

### Field: ordering_mechanisms
**Definition**: How temporal ordering is established
**Format**: Array of objects with `mechanism`, `description`, `source`
**Priority**: MEDIUM

**Example GOOD extraction**:
```yaml
ordering_mechanisms:
  - mechanism: "Timestamp ordering"
    description: "Events ordered by timestamp attribute (ISO 8601)"
    source: "Chunk 1:387-388"
  - mechanism: "Directly-follows graph"
    description: "Local ordering per entity based on correlation"
    source: "Chunk 2:303-308"
  - mechanism: "Happens-before"
    description: "Partial order based on causal dependencies"
    source: "Chunk 3:67-74"
```

---

### Field: causation_patterns
**Definition**: Causal relationships between events
**Format**: Array of objects with `pattern`, `description`, `source`
**Priority**: MEDIUM

**Example GOOD extraction**:
```yaml
causation_patterns:
  - pattern: "wasDerivedFrom"
    description: "PROV-O: Entity derived from another through transformation"
    source: "Chunk 2:78-85"
  - pattern: "wasInformedBy"
    description: "PROV-O: Activity used entity generated by prior activity"
    source: "Chunk 2:89-96"
  - pattern: "Disposition realization"
    description: "BFO: Event realizes disposition, causing manifestation"
    source: "Chunk 3:45-52"
```

---

### Field: temporal_standards
**Definition**: Standards for representing time
**Format**: Array of objects with `standard`, `description`, `source`
**Priority**: MEDIUM

**Example GOOD extraction**:
```yaml
temporal_standards:
  - standard: "ISO 8601"
    description: "Timestamp format for event occurrence times"
    source: "Chunk 1:387-388"
  - standard: "Allen's Interval Algebra"
    description: "13 temporal relations between intervals (before, after, during, etc.)"
    source: "Chunk 2:56-63"
  - standard: "XES Lifecycle"
    description: "IEEE standard lifecycle transitions (schedule, start, complete)"
    source: "Chunk 3:181-186"
```

---

### Field: event_log_formats
**Definition**: Event data formats and schemas
**Format**: Array of objects with `format`, `description`, `source`
**Priority**: MEDIUM

**Example GOOD extraction**:
```yaml
event_log_formats:
  - format: "OCEL 2.0"
    description: "Object-centric event log with E2O/O2O relations, dynamic attributes"
    source: "Chunk 1:33-40"
  - format: "XES"
    description: "IEEE standard for extensible event streams"
    source: "Chunk 2:163-175"
  - format: "Labeled Property Graph"
    description: "Neo4j-based event knowledge graphs with typed edges"
    source: "Chunk 3:574-583"
```

---

## Paper-Specific Extraction Notes

### UFO (Paper 01, 23)
- **Focus**: UFO-B perdurants, temporal parts, disposition realization
- **Key sections**: Perdurant mereology, Object participation, Causation
- **Expected fields**: event_types, event_definitions, state_change_mechanisms

### BFO/Barry Smith (Paper 06, 07)
- **Focus**: Process classification, Process Profiles, temporal parts
- **Key sections**: Process types, Function realization
- **Expected fields**: event_types, lifecycle_patterns, causation_patterns

### OCEL 2.0 (Paper 09)
- **Focus**: Event-Object relationships, dynamic attributes, qualifiers
- **Key sections**: E2O, O2O, timestamp handling
- **Expected fields**: event_correlation, ordering_mechanisms, event_log_formats

### Process Mining (Papers 10, 11, 12)
- **Focus**: Directly-follows graphs, event knowledge graphs, lifecycle
- **Key sections**: DF-paths, correlation, actor behavior
- **Expected fields**: temporal_relations, ordering_mechanisms, lifecycle_patterns

### PROV-AGENT (Paper 03)
- **Focus**: Activity timing, wasStartedBy/wasEndedBy, derivation chains
- **Key sections**: W3C PROV extensions, AI agent tracking
- **Expected fields**: agent_participation, temporal_relations, causation_patterns

### Agentic RAG (Paper 20)
- **Focus**: Workflow patterns, orchestration timing
- **Key sections**: Multi-agent coordination, planning patterns
- **Expected fields**: agent_participation, lifecycle_patterns

---

## Quality Checklist

Before completing analysis, verify:

- [ ] All 6 HIGH priority fields extracted or marked "N/A - reason"
- [ ] Every extraction has chunk:line reference
- [ ] Temporal relation vocabulary standardized
- [ ] Lifecycle states form valid FSM (no orphan states)
- [ ] Agent participation types use controlled vocabulary
- [ ] Event definitions include temporal properties

---

**Version**: 1.0 (2026-01-01)
