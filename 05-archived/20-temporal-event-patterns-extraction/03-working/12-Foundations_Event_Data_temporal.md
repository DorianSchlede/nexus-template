# Temporal Event Pattern Extraction: 12-Foundations_of_Process_Event_Data

**Paper**: Foundations of Process Event Data
**Authors**: Jochen De Weerdt, Moe Thandar Wynn
**Year**: 2022
**Source**: Process Mining Handbook, LNBIP 448
**Extraction Date**: 2026-01-01
**Schema Version**: 1.0

---

## Summary

This paper establishes the foundational data requirements for process mining event logs. It defines the three essential requirements (Case ID, Activity Label, Timestamp), explores lifecycle transitions via XES and BPMN 2.0, and documents 11 event log imperfection patterns that affect temporal analysis quality. Highly relevant for defining canonical Event entity structure in UDWO metamodel.

---

## HIGH PRIORITY FIELDS

### event_types

```yaml
event_types:
  - type: "Event"
    description: "Observed atomic granule of activity in IEEE XES; fundamental observation unit in event logs"
    source: "Chunk 1:167-168"
  - type: "Trace"
    description: "Ordered sequence of events pertaining to a single case/process instance"
    source: "Chunk 1:169"
  - type: "Log"
    description: "Collection of traces representing execution history of a business process"
    source: "Chunk 1:169"
  - type: "Lifecycle Event"
    description: "Events relating to transactional lifecycle states of activities (start, complete, suspend, etc.)"
    source: "Chunk 1:181-186"
  - type: "Completion Event"
    description: "Default event type when no lifecycle specified; assumes activity has completed"
    source: "Chunk 1:219-221"
  - type: "Start Event"
    description: "Event indicating activity execution has begun; enables waiting vs execution time distinction"
    source: "Chunk 1:223-224"
```

---

### event_definitions

```yaml
event_definitions:
  Event:
    definition: "An observed atomic granule of activity recorded in an event log"
    essential_requirements:
      - requirement: "Case ID (Requirement 1)"
        description: "Each event must be linked to a case or process instance"
        source: "Chunk 1:68-75"
      - requirement: "Activity Label (Requirement 2)"
        description: "Each event must correspond to an activity from a restricted set of labels"
        source: "Chunk 1:92-102"
      - requirement: "Timestamp/Ordering (Requirement 3)"
        description: "Events within a case must be orderable, typically via timestamps"
        source: "Chunk 1:110-116"
    temporal_properties:
      - "timestamp"
      - "ordering_within_case"
      - "lifecycle_transition"
    source: "Chunk 1:62-116, 167-168"

  Case:
    definition: "A process instance identified by Case ID to which events are correlated"
    properties:
      - "case_id: unique identifier"
      - "events: ordered sequence forming a trace"
      - "case_attributes: instance-level properties"
    source: "Chunk 1:68-75"

  Trace:
    definition: "A sequence of events pertaining to a single case, ordered temporally"
    temporal_properties:
      - "sequence_ordering"
      - "start_time (first event)"
      - "end_time (last event)"
    source: "Chunk 1:110-112, 169"

  Activity:
    definition: "A step executed within a process, represented by a label from a restricted set"
    temporal_properties:
      - "execution_time (if start+complete events)"
      - "waiting_time (if start+complete events)"
      - "lifecycle_state"
    source: "Chunk 1:92-102, 221-224"
```

---

### temporal_relations

```yaml
temporal_relations:
  - relation: "before"
    domain: "Event"
    range: "Event"
    semantics: "e1 before e2 iff e1.timestamp < e2.timestamp within same case"
    source: "Chunk 1:110-112"
    notes: "Derived from timestamp attribute; forms basis for trace ordering"

  - relation: "sequence"
    domain: "Event"
    range: "Trace"
    semantics: "Events within a case form an ordered sequence based on timestamps"
    source: "Chunk 1:111-112"
    quote: "each case logically consists of a sequence of events"

  - relation: "lifecycle-transition"
    domain: "Activity"
    range: "Activity"
    semantics: "Valid state transitions within activity lifecycle (e.g., start -> complete)"
    source: "Chunk 1:181-186"
    standards:
      - "BPMN 2.0 lifecycle model"
      - "IEEE XES lifecycle extension"

  - relation: "correlates-to"
    domain: "Event"
    range: "Case"
    semantics: "Event is associated with a specific process instance via Case ID"
    source: "Chunk 1:68-69"
    quote: "each event should be linked to a case or process instance"
```

---

### lifecycle_patterns

```yaml
lifecycle_patterns:
  - entity: "Activity"
    standard: "BPMN 2.0"
    description: "Transactional lifecycle model from BPMN 2.0 standard"
    states: ["Ready", "Active", "Withdrawing", "Completing", "Failing", "Compensating", "Closed"]
    transitions:
      - note: "Full state machine shown in Fig. 3a of paper"
    source: "Chunk 1:183-184"
    quote: "This is the transition lifecycle model of the BPMN 2.0 standard"

  - entity: "Activity"
    standard: "IEEE XES"
    description: "Default activity lifecycle from IEEE XES lifecycle extension"
    states: ["schedule", "assign", "reassign", "start", "suspend", "resume", "complete", "autoskip", "manualskip", "withdraw", "abort_activity", "abort_case", "pi_abort", "ate_abort", "unknown"]
    transitions:
      - note: "State machine shown in Fig. 3b of paper; most typical transitions"
      - from: "schedule"
        to: "start"
        trigger: "activity assignment"
      - from: "start"
        to: "suspend"
        trigger: "activity paused"
      - from: "suspend"
        to: "resume"
        trigger: "activity continued"
      - from: "start"
        to: "complete"
        trigger: "activity finished"
    source: "Chunk 1:185-186"
    quote: "Also in IEEE XES, a lifecycle extension has been approved"

  - entity: "Activity"
    standard: "Minimal (2-event)"
    description: "Minimal lifecycle with start and complete events only"
    states: ["started", "completed"]
    transitions:
      - from: "started"
        to: "completed"
        trigger: "activity execution finishes"
    purpose: "Enables distinction between waiting time and execution time"
    source: "Chunk 1:221-224"

  - entity: "Activity"
    standard: "Single-event"
    description: "Default assumption when no lifecycle transitions available"
    states: ["completed"]
    transitions: []
    assumption: "Single event per activity represents completion"
    source: "Chunk 1:219-221"
    quote: "one typically assumes that an event pertaining to the execution of an activity reflects the completion of the activity"
```

---

### event_correlation

```yaml
event_correlation:
  - pattern: "Case ID Correlation"
    description: "Primary correlation via Case ID linking events to process instances"
    source: "Chunk 1:68-75"
    challenge: "Case IDs are not always straightforwardly available"

  - pattern: "Attribute-based Correlation"
    description: "Using additional event attributes to infer case correlation when Case ID missing"
    source: "Chunk 1:458 (Reference [12,15,42,44,48])"
    approaches:
      - "Using additional event data attributes"
      - "Aided by conceptual model"
      - "Aided by process model"

  - pattern: "Object-centric Correlation"
    description: "Correlating events to objects rather than single case; multiple case notions"
    source: "Chunk 1:424-433"
    standard: "OCEL"
    quote: "the recently introduced OCEL standard is another relevant piece of work, putting forward a general standard to interchange object-centric event data with multiple case notions"

  - pattern: "Stream Correlation"
    description: "Correlation in event streams where Case ID is more complicated"
    source: "Chunk 1:83-85"
    challenge: "In event streams, the notion of a CaseID is often even more complicated"
```

---

### agent_participation

```yaml
agent_participation:
  - participation_type: "performs"
    description: "Resource/actor who performs activities within the process"
    source: "Chunk 1:148-152"
    notes: "Additional data attributes on resources enable organizational mining"

  - participation_type: "is-affected-by"
    description: "Process instance (case) that undergoes changes through events"
    source: "Chunk 1:68-75"
    notes: "Each event affects a process instance identified by Case ID"
```

**Note**: This paper does not deeply model agent/resource participation semantics. It mentions resources as additional attributes enabling organizational mining but does not define formal agent participation types.

---

## MEDIUM PRIORITY FIELDS

### ordering_mechanisms

```yaml
ordering_mechanisms:
  - mechanism: "Timestamp ordering"
    description: "Events ordered by timestamp attribute within a case"
    source: "Chunk 1:112-113"
    quote: "Most often, this ordering will be derived from a timestamp attribute"

  - mechanism: "Recording order"
    description: "Alternative ordering based on database recording sequence"
    source: "Chunk 1:113-116"
    quote: "the order could also be derived from the order in which events are recorded in a database or table"
    caveat: "Only valid if recording order matches factual execution order"

  - mechanism: "Trace sequence"
    description: "Events within a trace form an ordered sequence per case"
    source: "Chunk 1:110-112"
    quote: "each case logically consists of a sequence of events"
```

---

### temporal_standards

```yaml
temporal_standards:
  - standard: "IEEE XES (IEEE Std 1849-2016)"
    description: "IEEE Standards Association-approved language for transporting, storing, and exchanging event data"
    key_features:
      - "W3C XML Schema definition language"
      - "Extensible via extensions for attributes"
      - "Defines log, trace, event components"
      - "Lifecycle extension for activity transitions"
    source: "Chunk 1:162-175, 185-186"

  - standard: "BPMN 2.0"
    description: "Business Process Model and Notation standard defining activity lifecycle transitions"
    source: "Chunk 1:183-184"
    url: "https://www.omg.org/spec/BPMN/2.0/"

  - standard: "OCEL"
    description: "Object-Centric Event Log standard for multi-case-notion event data"
    source: "Chunk 1:431-433"
    url: "http://ocel-standard.org/"

  - standard: "JSON"
    description: "Default format for web-based platform event data"
    source: "Chunk 1:314-315"
```

---

### event_log_formats

```yaml
event_log_formats:
  - format: "IEEE XES (XML)"
    description: "Extensible Event Stream format using W3C XML Schema"
    structure:
      - "Log: container for traces"
      - "Trace: container for events with classifiers"
      - "Event: atomic activity granule with attributes"
      - "Extension: domain-specific attribute sets"
    source: "Chunk 1:162-175"

  - format: "OCEL"
    description: "Object-Centric Event Log format for multiple case notions"
    source: "Chunk 1:431-433"

  - format: "JSON"
    description: "Common format for web platform event data (MOOCs, etc.)"
    source: "Chunk 1:314-315"

  - format: "Relational/ETL"
    description: "Event data extracted from relational databases via ETL processing"
    source: "Chunk 1:464-470"
```

---

## DATA QUALITY PATTERNS

### 11 Event Log Imperfection Patterns (Suriadi et al.)

```yaml
event_log_imperfection_patterns:
  source: "Chunk 1:579-583"
  quote: "Suriadi et al. identified eleven event log imperfection patterns based on their experience with over 20 Australian industry data sets"

  patterns:
    - pattern: "Form-based event capture"
      description: "Events recorded from form submissions may have quality issues from data entry"

    - pattern: "Inadvertent time travel"
      description: "Events with timestamps that violate temporal ordering (future timestamps, etc.)"

    - pattern: "Unanchored event"
      description: "Events that cannot be linked to any case (missing Case ID)"

    - pattern: "Scattered event"
      description: "Events belonging to same activity but recorded across multiple entries"

    - pattern: "Elusive case"
      description: "Cases that are difficult to identify or correlate events to"

    - pattern: "Scattered case"
      description: "Case information scattered across multiple data sources"

    - pattern: "Collateral event"
      description: "Events incorrectly associated with a case they don't belong to"

    - pattern: "Polluted label"
      description: "Activity labels containing noise or irrelevant information"

    - pattern: "Distorted label"
      description: "Activity labels that have been corrupted or incorrectly modified"

    - pattern: "Synonymous labels"
      description: "Different labels used for the same activity"

    - pattern: "Homonymous labels"
      description: "Same label used for different activities"
```

---

### Data Quality Dimensions

```yaml
data_quality_dimensions:
  source: "Chunk 1:549-552"

  dimensions:
    - dimension: "Missing data"
      impact: "Incomplete traces, unknown Case IDs, missing timestamps"

    - dimension: "Incorrect data"
      impact: "Data items not recorded correctly; significant consequences for analysis"

    - dimension: "Imprecise data"
      impact: "Recorded values too coarse to be useful (e.g., day-level timestamps)"

    - dimension: "Irrelevant data"
      impact: "Data not pertinent to the analysis objectives"
```

---

### Timestamp-Specific Quality Issues

```yaml
timestamp_quality_issues:
  source: "Chunk 1:612-623"

  issues:
    - issue: "Zero timestamps"
      description: "Timestamps with null or zero values"

    - issue: "Wrong timestamps"
      description: "Timestamps that do not reflect actual event occurrence time"

    - issue: "Same timestamps for multiple activities"
      description: "Multiple events recorded with identical timestamps (precision issue)"
      repair: "Automatic repair approach presented in reference [16]"

    - issue: "Different timestamp granularity"
      description: "Inconsistent precision across events (seconds vs. days)"

    - issue: "Event ordering imperfections"
      description: "Order inconsistencies detected and repaired interactively"
      repair: "Interactive approach in reference [22]"
```

---

## STATE CHANGE MECHANISMS

```yaml
state_change_mechanisms:
  - mechanism: "Activity lifecycle transition"
    description: "Activities change state via lifecycle events (start, suspend, complete, etc.)"
    source: "Chunk 1:181-186"

  - mechanism: "Event-level attribute update"
    description: "Attributes can be updated throughout process execution at event level"
    source: "Chunk 1:133-136"
    quote: "attributes can pertain to events or activities, and might be updated throughout the execution of a process instance"
```

---

## RELEVANCE TO UDWO METAMODEL

### Canonical Event Entity Requirements

Based on this paper, the canonical Event entity should have:

1. **Mandatory Properties**:
   - `case_id`: Correlation to process instance (Requirement 1)
   - `activity_label`: Activity type from restricted vocabulary (Requirement 2)
   - `timestamp`: Temporal ordering attribute (Requirement 3)

2. **Optional Lifecycle Properties**:
   - `lifecycle_transition`: State in activity lifecycle (XES: schedule, start, suspend, complete, etc.)
   - `start_time` / `end_time`: For duration calculation

3. **Correlation Properties**:
   - `object_correlations`: For object-centric event logs (OCEL)
   - `resource`: Actor/agent who performed activity

4. **Quality Metadata**:
   - `data_quality_annotation`: Track imperfection patterns
   - `timestamp_precision`: Granularity of temporal data

### Temporal Operators Needed

- **before(e1, e2)**: Timestamp ordering within case
- **directly-follows(e1, e2)**: Sequential adjacency in trace
- **lifecycle-transition(activity, from_state, to_state)**: Valid state changes

---

## QUALITY CHECKLIST

- [x] All 6 HIGH priority fields extracted (event_types, event_definitions, temporal_relations, lifecycle_patterns, event_correlation, agent_participation)
- [x] Every extraction has chunk:line reference
- [x] Temporal relation vocabulary standardized (before, sequence, correlates-to)
- [x] Lifecycle states form valid FSM (XES and BPMN 2.0 models)
- [x] Agent participation types use controlled vocabulary (performs, is-affected-by)
- [x] Event definitions include temporal properties (timestamp, ordering, lifecycle)
- [x] 11 data imperfection patterns documented
- [x] Timestamp quality issues captured

---

**Extraction Version**: 1.0
**Extracted By**: Claude Code Agent
**For Project**: 20-temporal-event-patterns-extraction
