---
paper_id: "07-Classifying_Processes_Barry_Smith"
title: "Classifying Processes: An Essay in Applied Ontology"
authors:
  - "Barry Smith"
year: 2012
extraction_date: "2026-01-01"
extraction_focus: "Temporal/Event Patterns for UDWO Metamodel"
schema_version: "1.0"

# HIGH PRIORITY FIELDS

event_types:
  - type: "Process"
    description: "Four-dimensional occurrent entity that occupies a spatiotemporal region and spans a temporal interval; processes ARE changes in independent continuant participants"
    source: "Chunk 1:547-563"
  - type: "Process Boundary"
    description: "Instantaneous occurrent marking beginnings and endings of processes; spans temporal instants rather than intervals"
    source: "Chunk 1:548-549, 562-563"
  - type: "Occurrent"
    description: "Entity extended in time that can be sliced along both spatial and temporal dimensions; exists in entirety within its spatiotemporal boundaries"
    source: "Chunk 1:299-300, 370-381"
  - type: "Temporal Part"
    description: "An occurrent that is the exact restriction of a larger process to a proper temporal subregion"
    source: "Chunk 1:577-593"
  - type: "Process Profile"
    description: "That part of a process which serves as the target of selective abstraction focused on a single structural dimension; what two qualitatively similar processes share"
    source: "Chunk 2:119-131"
  - type: "Quality Process Profile"
    description: "Simplest process profile - sequence of determinate quality instances plotted over time (e.g., temperature change)"
    source: "Chunk 2:152-168"
  - type: "Rate Process Profile"
    description: "Process profile focused on ratios between quality magnitudes and elapsed time intervals (e.g., speed, acceleration)"
    source: "Chunk 2:174-197"
  - type: "Cyclical Process Profile"
    description: "Subtype of rate process profile where salient ratio is number of cycles per unit time (e.g., heartbeat rate)"
    source: "Chunk 2:238-260"

event_definitions:
  Process:
    definition: "An occurrent that occupies a spatiotemporal region and spans a temporal interval; processes are changes in their independent continuant participants"
    temporal_properties:
      - "occupies (spatiotemporal region)"
      - "spans (temporal interval)"
      - "has temporal parts"
      - "duration (via temporal region)"
    source: "Chunk 1:547-563"
  Process_Boundary:
    definition: "An occurrent that occupies a spatiotemporal region and spans a temporal instant (not interval); marks beginnings and endings"
    temporal_properties:
      - "spans (temporal instant)"
      - "not temporally extended"
    source: "Chunk 1:548-549, 561-563"
  Temporal_Part:
    definition: "a temporal_part_of b iff a is occurrent_part_of b AND for some temporal region r (a spans r AND for all occurrents c, r' if (c spans r' AND r' occurrent_part_of r) then (c occurrent_part_of a iff c occurrent_part_of b))"
    temporal_properties:
      - "occurrent_part_of"
      - "spans (restricted temporal region)"
    source: "Chunk 1:577-582"
  Process_Profile:
    definition: "That part of a process which is the target of selective abstraction focused on one structural dimension; an occurrent entity in the process itself that serves as fundamentum comparationis"
    temporal_properties:
      - "inherits temporal span from containing process"
      - "can be plotted against time"
    source: "Chunk 2:144-146"
  Quality_Process_Profile:
    definition: "Process profile tracking a sequence of determinate quality instances over time; representable as graph of quality values vs time"
    temporal_properties:
      - "sequence of quality instances at successive instants"
      - "can be graphed against time"
    source: "Chunk 2:152-168"
  Rate_Process_Profile:
    definition: "Process profile focused on ratios between quality magnitudes and elapsed time intervals"
    temporal_properties:
      - "ratio per unit time"
      - "can change over time (rates of rates)"
      - "hierarchical: speed -> acceleration -> jerk"
    source: "Chunk 2:174-197"
  Cyclical_Process_Profile:
    definition: "Rate process profile where salient ratio is number of cycles per unit time"
    temporal_properties:
      - "cycles per unit time"
      - "regular vs irregular patterns"
    source: "Chunk 2:238-260"

temporal_relations:
  - relation: "occupies"
    domain: "Occurrent"
    range: "Spatiotemporal Region"
    semantics: "The occurrent exactly fills the spatiotemporal region"
    source: "Chunk 1:550-552"
  - relation: "spans"
    domain: "Process"
    range: "Temporal Interval"
    semantics: "The temporal projection of the occupied spatiotemporal region"
    source: "Chunk 1:552-553"
  - relation: "spans (instant)"
    domain: "Process Boundary"
    range: "Temporal Instant"
    semantics: "Process boundaries span instants, not intervals"
    source: "Chunk 1:552-553"
  - relation: "temporal_part_of"
    domain: "Occurrent"
    range: "Occurrent"
    semantics: "a is the exact restriction of b to a proper temporal subregion of b's temporal span"
    source: "Chunk 1:577-582"
  - relation: "occurrent_part_of"
    domain: "Occurrent"
    range: "Occurrent"
    semantics: "Standard parthood between occurrents (broader than temporal_part_of)"
    source: "Chunk 1:564-569"
  - relation: "before"
    domain: "Temporal Part"
    range: "Temporal Part"
    semantics: "Implicit in discussion of sub-processes p1 and p2 where p2 is 'subsequent' to p1"
    source: "Chunk 1:747-750"

lifecycle_patterns:
  - entity: "Process"
    states:
      - "not-yet-occurring"
      - "occurring (spans temporal interval)"
      - "occurred (completed)"
    transitions:
      - from: "not-yet-occurring"
        to: "occurring"
        trigger: "process boundary (beginning)"
      - from: "occurring"
        to: "occurred"
        trigger: "process boundary (ending)"
    source: "Chunk 1:548-549, 585-589"
    notes: "BFO processes cannot change - they ARE changes. Lifecycle is about existence/occurrence, not state change within the process."
  - entity: "Continuant (as participant)"
    states:
      - "exists"
      - "participates in process"
      - "changed (post-participation)"
    transitions:
      - from: "exists"
        to: "participates in process"
        trigger: "participation relation onset"
      - from: "participates in process"
        to: "changed"
        trigger: "process completion"
    source: "Chunk 1:686-692, 719-727"
    notes: "Continuants CAN change through processes - processes are changes in continuants"
  - entity: "Quality (of Continuant)"
    states:
      - "instantiates determinate universal D1 at t1"
      - "instantiates determinate universal D2 at t2"
    transitions:
      - from: "D1 at t1"
        to: "D2 at t2"
        trigger: "quality process profile progression"
    source: "Chunk 1:506-510, Chunk 2:154-157"
    notes: "Quality instances persist but instantiate different determinate universals over time"

state_change_mechanisms:
  - mechanism: "Process as change in continuant"
    description: "Processes ARE changes in their independent continuant participants; the process itself does not change"
    source: "Chunk 1:688-692"
  - mechanism: "Disposition realization"
    description: "Dispositions (like solubility, fragility) require a process to be realized or manifested"
    source: "Chunk 1:406-409"
  - mechanism: "Quality value change over time"
    description: "A quality instance (e.g., John's temperature) persists but instantiates different determinate universals (37C, 38C) at different times"
    source: "Chunk 1:506-510"
  - mechanism: "Part gain/loss"
    description: "Continuants may gain and lose parts over time (indexed by time); occurrent parthood is timeless"
    source: "Chunk 1:719-727"
  - mechanism: "Universal instantiation shift"
    description: "Continuants can shift between non-rigid universals (larva -> pupa -> adult); occurrents always instantiate rigid universals"
    source: "Chunk 1:729-738"

agent_participation:
  - participation_type: "participates_in"
    description: "The fundamental relation connecting continuants to occurrents; independent continuants participate in processes"
    source: "Chunk 1:437-440"
  - participation_type: "is-bearer-of (qualities)"
    description: "Independent continuants bear qualities (dependent continuants); processes depend on the qualities of participants"
    source: "Chunk 1:498-502, 848-852"
  - participation_type: "specific_dependence"
    description: "Processes specifically depend on their independent continuant participants (analogous to quality-bearer relation)"
    source: "Chunk 1:848-852"
  - participation_type: "realizes (disposition)"
    description: "Agent's dispositions are realized through participation in appropriate processes"
    source: "Chunk 1:406-409"

causation_patterns:
  - pattern: "Process-as-change"
    description: "Processes do not cause change; they ARE changes in the continuants that participate in them"
    source: "Chunk 1:688-692"
  - pattern: "Disposition realization"
    description: "Dispositions (e.g., solubility) require realization through a process; the process manifests the disposition"
    source: "Chunk 1:406-409"
  - pattern: "Specific dependence chain"
    description: "Processes depend on independent continuants which bear qualities and dispositions; the process realizes these dependent continuants"
    source: "Chunk 1:848-852, 412-414"
  - pattern: "Nested process wholes"
    description: "Processes are embedded within larger process wholes (ball motion relative to table, table-earth system, earth-sun system)"
    source: "Chunk 2:283-289"

# MEDIUM PRIORITY FIELDS

ordering_mechanisms:
  - mechanism: "Temporal interval spanning"
    description: "Processes span temporal intervals; temporal regions have their own ordering"
    source: "Chunk 1:550-553"
  - mechanism: "Temporal parthood"
    description: "Temporal parts create ordering through their restriction to sub-intervals"
    source: "Chunk 1:577-582, 585-593"
  - mechanism: "Sequential sub-processes"
    description: "Process p has temporal parts p1 (first 10 min) followed by p2 (second 10 min)"
    source: "Chunk 1:740-750"
  - mechanism: "Quality sequence ordering"
    description: "Quality process profiles track sequences of quality instances at successive instants"
    source: "Chunk 2:154-157"

temporal_standards:
  - standard: "BFO Temporal Region"
    description: "Temporal intervals and temporal instants as first-class occurrent entities"
    source: "Chunk 1:548-549"
  - standard: "Timeless occurrent relations"
    description: "Occurrent parthood holds timelessly (unlike time-indexed continuant parthood)"
    source: "Chunk 1:722-727"
  - standard: "Limit definition for instantaneous rates"
    description: "Speed at instant t defined via epsilon-delta: for any e, exists interval around t where speed differs by less than e from v"
    source: "Chunk 2:218-232"

event_correlation:
  - pattern: "Process-to-Participant"
    description: "Processes correlated to independent continuants through participation relation"
    source: "Chunk 1:437-440, 848-852"
  - pattern: "Process-to-Spatiotemporal-Region"
    description: "Process occupies exactly one spatiotemporal region; multiple processes can co-occupy same region"
    source: "Chunk 1:426-429, 550-552"
  - pattern: "Process-to-Quality-Sequence"
    description: "Quality process profiles correlate process to sequence of quality instances in participants"
    source: "Chunk 2:154-157"
  - pattern: "Process-Profile-to-Universal"
    description: "Process profiles instantiate process profile universals enabling comparison across processes"
    source: "Chunk 2:126-131"

# ADDITIONAL EXTRACTED CONCEPTS

bfo_34_term_upper_ontology:
  entity_types:
    continuants:
      - "Independent Continuant"
      - "Dependent Continuant"
      - "Quality"
      - "Disposition"
      - "Role"
      - "Function"
      - "Generically Dependent Continuant"
      - "Specifically Dependent Continuant"
      - "Continuant Fiat Boundary"
    occurrents:
      - "Process"
      - "Process Boundary"
      - "Spatiotemporal Region"
      - "Temporal Region"
      - "Temporal Interval"
      - "Temporal Instant"
  source: "Chunk 1:285-290"

process_profile_hierarchy:
  determinable_universals:
    - "process profile"
    - "quality process profile"
    - "rate process profile"
    - "cyclical process profile"
  determinate_examples:
    quality_profiles:
      - "temperature change profile"
      - "height change profile"
    rate_profiles:
      - "constant speed profile"
      - "2 mph constant speed profile"
      - "acceleration profile"
      - "32 ft/s^2 acceleration profile"
    cyclical_profiles:
      - "regular cyclical process profile"
      - "3 bpm cyclical process profile"
      - "irregular cyclical process profile"
  source: "Chunk 2:174-252"

key_axioms:
  - axiom: "Processes cannot change"
    formulation: "Processes ARE changes (in their independent continuant participants)"
    implication: "No qualities of occurrents; process attributes handled via instantiation"
    source: "Chunk 1:688-692, 803-807"
  - axiom: "Occurrent universals are rigid"
    formulation: "If an occurrent instantiates a universal at some time, it instantiates it at all times"
    implication: "Sub-processes instantiate more specific universals, not the whole process"
    source: "Chunk 1:735-750"
  - axiom: "Occurrent parthood is timeless"
    formulation: "If p1 is part of p2, this holds timelessly (unlike time-indexed continuant parthood)"
    source: "Chunk 1:722-727"
  - axiom: "Multiple processes can co-occupy"
    formulation: "Multiple processes able to occupy same spatiotemporal region (running + getting warmer)"
    source: "Chunk 1:426-429"

---

# Temporal Event Patterns Extraction: Classifying Processes (Barry Smith 2012)

## Executive Summary

This paper presents BFO's (Basic Formal Ontology) treatment of processes and introduces the novel concept of **Process Profiles** for classifying process types. The key temporal/event contributions for UDWO are:

1. **Processes ARE changes** - they do not undergo change; they are changes in their continuant participants
2. **Process Profiles** - structured abstractions for comparing processes along dimensions (quality, rate, cyclical)
3. **Temporal parthood** - formal definition for process decomposition
4. **Participation relation** - connects continuants (potential agents) to processes (activities)

## Key Temporal Patterns for UDWO

### 1. Process Classification via Profiles

The paper introduces three types of process profiles that enable systematic process comparison:

| Profile Type | Focus | Example | Representation |
|-------------|-------|---------|----------------|
| Quality | Sequence of quality values | Temperature change | Graph: quality vs time |
| Rate | Ratio of magnitude to time | Speed, acceleration | Graph: rate vs time |
| Cyclical | Cycles per unit time | Heartbeat rate | Frequency measurement |

### 2. Temporal Structure

**Process Boundary Pattern:**
- Beginnings and endings are process boundaries
- Boundaries span temporal instants (not intervals)
- Useful for defining start/end events

**Temporal Parthood:**
```
a temporal_part_of b iff:
  - a occurrent_part_of b
  - a spans some temporal region r
  - All occurrents spanning sub-parts of r are parts of both a and b
```

### 3. Participation as Agent-Activity Link

The `participates_in` relation connects continuants (including agents) to processes:
- Continuants exist during temporal intervals
- Processes occur during temporal intervals
- Connection is through participation, not parthood
- Processes specifically depend on their participants

## Relevance to UDWO Event Entity

### Canonical Event Definition
From BFO: An Event/Process is an occurrent that:
- Occupies a spatiotemporal region
- Spans a temporal interval (or instant for boundaries)
- Has temporal parts
- Cannot change (it IS a change)
- Specifically depends on participating continuants

### Lifecycle States
BFO implies minimal lifecycle:
- **Scheduled/Planned** (not in scope - see plans/protocols)
- **Occurring** (spans temporal interval)
- **Completed** (has occurred)

### Temporal Operators
- `spans` - process to temporal region
- `occupies` - process to spatiotemporal region
- `temporal_part_of` - process decomposition
- `before/after` - via temporal region ordering

### Agent Participation Types
- `participates_in` - fundamental continuant-process relation
- `realizes` - process realizes disposition of participant
- `specifically_depends_on` - process depends on participants

## Integration Notes

1. **Process Profiles for Activity Types**: Use quality/rate/cyclical profiles to classify agent activities
2. **Temporal Parthood for Workflow Steps**: Workflow steps as temporal parts of larger workflow processes
3. **Participation for Agent Correlation**: Link agents to activities via BFO participation pattern
4. **Disposition Realization for Capability Modeling**: Agent capabilities as dispositions realized through activities
