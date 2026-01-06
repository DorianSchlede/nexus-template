---
paper_id: "01-UFO_Unified_Foundational_Ontology"
title: "UFO: Unified Foundational Ontology"
authors:
  - "Giancarlo Guizzardi"
  - "Alessander Botti Benevides"
  - "Claudenir M. Fonseca"
  - "Daniele Porello"
  - "Joao Paulo A. Almeida"
  - "Tiago Prince Sales"
year: 2021
extraction_date: "2026-01-01"
extraction_version: "1.0"
schema_version: "temporal-events-v1"

event_types:
  - type: "Perdurant"
    description: "Individuals that unfold in time accumulating temporal parts. They are manifestations of dispositions and only exist in the past. Modally fragile entities that cannot be different from what they are."
    source: "Chunk 1:289-296"
  - type: "Event (synonym for Perdurant)"
    description: "Common name for perdurants; modally fragile entities that cannot genuinely change. They cannot bear modal properties."
    source: "Chunk 1:308, Chunk 3:103-105"
  - type: "Process"
    description: "A special perdurant that is the life of an endurant - the sum of everything that is a manifestation of the dispositions inhering in that endurant. Represents the current life of an endurant at each point in time."
    source: "Chunk 2:528-533"
  - type: "Jogging Event (atomic)"
    description: "Direct manifestations of dispositions constituting a Jog mode. Individual event instances."
    source: "Chunk 3:150-158"
  - type: "Jogging Process (composite)"
    description: "Constituted by Jogging Events; represents cumulative aggregation of manifestations of a Jog mode. A new process arises each time a new event takes place."
    source: "Chunk 3:150-165"
  - type: "Jog State (stative/homeomeric)"
    description: "A type of Jogging Event that is stative/homeomerous - all temporal parts are of the same type."
    source: "Chunk 3:186-187"
  - type: "Jogging Locomotion (dynamic)"
    description: "A type of Jogging Event that is dynamic/sequences of changes. Can be Walk While Jogging or Run While Jogging based on speed quality."
    source: "Chunk 3:187-204"

event_definitions:
  Perdurant:
    definition: "Individuals that unfold in time accumulating temporal parts. Manifestations of dispositions. Only exist in the past. Modally fragile - no cross-world identity possible."
    temporal_properties:
      - "temporal_parts"
      - "unfolds_in_time"
      - "meets (consecutive in time)"
    formal_axioms:
      - "Perdurant(x) -> ConcreteIndividual(x) [a12]"
      - "Endurant(x) -> NOT Perdurant(x) [a13]"
      - "constitutedBy(x,y) AND Perdurant(x) -> NECESSARILY (ex(x) -> constitutedBy(x,y)) [a60]"
    source: "Chunk 1:289-296, Chunk 1:530-537"
  Event:
    definition: "Synonym for perdurant. Cannot genuinely change - alleged changes are either variation (temporal parts with different properties) or changes to underlying endurants that are the focus of the event."
    temporal_properties:
      - "modally_fragile"
      - "cannot_change"
      - "has_temporal_parts"
    source: "Chunk 3:103-117, Chunk 3:251-263"
  Process:
    definition: "The life of an endurant - mereological sum of all events that manifest dispositions inhering in that endurant. Every single manifestation changes the life (a change OF life, not change IN life)."
    temporal_properties:
      - "lifeOf(process, endurant)"
      - "constitutedBy(process, event)"
    formal_axioms:
      - "lifeOf(x, y) <-> Perdurant(x) AND Endurant(y) AND forall z (O(z,x) <-> Perdurant(z) AND manifests(z, y)) [a103]"
    source: "Chunk 2:505-533"

temporal_relations:
  - relation: "meets"
    domain: "Perdurant"
    range: "Perdurant"
    semantics: "Two perdurants are consecutive in time (Allen's temporal algebra). If processes meet and manifest same endurant, all constituents of preceding process also constitute succeeding process."
    source: "Chunk 2:508-509, Chunk 3:176-183"
  - relation: "constitutedBy"
    domain: "Perdurant"
    range: "Perdurant"
    semantics: "Constitution between events. For perdurants, all parts and constituents are necessary constituents (modally fragile). Temporal interval of constituent is part of interval framing constituted."
    source: "Chunk 2:69-76, Chunk 2:98-100"
  - relation: "manifests"
    domain: "Perdurant"
    range: "Endurant"
    semantics: "Event manifests dispositions inhering in an endurant. Core connection between perdurants and endurants."
    source: "Chunk 2:505-507"
  - relation: "participates-in"
    domain: "Endurant"
    range: "Perdurant"
    semantics: "An endurant participates in a perdurant if that perdurant has a part that is a manifestation of a disposition inhering in that endurant."
    source: "Chunk 1:295-296"
  - relation: "foundedBy"
    domain: "ExternallyDependentMode OR Relator"
    range: "Perdurant"
    semantics: "Externally dependent modes and relators are founded by means of a unique event. Foundation is immutable once established."
    source: "Chunk 2:207-219"

lifecycle_patterns:
  - entity: "Walk (as endurant mode)"
    states:
      - "OngoingWalk"
      - "FinalizedWalk"
    transitions:
      - from: "OngoingWalk"
        to: "FinalizedWalk"
        trigger: "Walk perdurant manifestation completes"
    nested_types:
      FinalizedWalk:
        states:
          - "SuccessfulWalk"
          - "RedirectedWalk"
        transitions:
          - from: "FinalizedWalk"
            to: "SuccessfulWalk"
            trigger: "arrivedAt(walk, originallyIntendedDestination)"
          - from: "FinalizedWalk"
            to: "RedirectedWalk"
            trigger: "arrivedAt(walk, differentDestination)"
    source: "Chunk 3:317-340"
  - entity: "Endurant (general)"
    states:
      - "exists"
      - "destroyed"
    transitions:
      - from: "exists"
        to: "destroyed"
        trigger: "end of life perdurant"
    notes: "Endurants can qualitatively change while maintaining numerical identity. The sorts of changes defined by the Kind they instantiate."
    source: "Chunk 1:286-288"
  - entity: "Jog (mode)"
    states:
      - "active"
    transitions: []
    notes: "Jog mode is manifested by JoggingProcess. Each new JoggingEvent creates new JoggingProcess (monotonic accumulation)."
    source: "Chunk 3:161-165"

state_change_mechanisms:
  - mechanism: "Disposition realization"
    description: "Events are manifestations of dispositions inhering in endurants. When a disposition is realized/manifested, this creates a perdurant (event). The endurant participates in the perdurant."
    source: "Chunk 1:295-296, Chunk 3:106-110"
  - mechanism: "Quality value change"
    description: "Qualities (particularized properties) inhere in endurants via characterization. The hasValue relation between quality and quale is one of generic dependence - values can change across situations while inherence is immutable."
    source: "Chunk 3:82-86"
  - mechanism: "Phase transition"
    description: "Endurants can transition between Phases (anti-rigid sortals with intrinsic contingent conditions). Phase change represents qualitative change while maintaining identity."
    source: "Chunk 1:373-375, Chunk 3:317-328"
  - mechanism: "Role acquisition/relinquishment"
    description: "Endurants can acquire/lose Roles (anti-rigid sortals with relational conditions) through mediation by relators. Role change occurs when relator is created/destroyed."
    source: "Chunk 1:376-377, Chunk 2:279-296"
  - mechanism: "Event constitution"
    description: "Complex events (processes) are constituted by simpler events. Constitution between events uses specific dependence - all constituents are necessary (modally fragile)."
    source: "Chunk 2:69-76"

agent_participation:
  - participation_type: "performs"
    description: "Agent (as Jogger role) performs Jogging through bearing a Jog mode that is manifested by Jogging perdurants."
    source: "Chunk 3:129-131"
  - participation_type: "participates-in"
    description: "Generic participation: endurant participates in perdurant if perdurant has a part that is manifestation of disposition inhering in that endurant."
    source: "Chunk 1:295-296"
  - participation_type: "is-focus-of"
    description: "Endurant (e.g., Walk mode) is the focus of an event. Events are carved out of scenes by having underlying endurants as their focus."
    source: "Chunk 3:107-110, Chunk 3:255-261"
  - participation_type: "is-mediated-by"
    description: "Agents (as role-bearing persons) are mediated by relators (e.g., Employment, Marriage). The relator connects multiple endurants in relational statements."
    source: "Chunk 2:279-284"
  - participation_type: "bears-disposition"
    description: "Agent bears dispositions (modes including functions, capabilities, capacities) which when realized create perdurants."
    source: "Chunk 1:321-323"

event_correlation:
  - pattern: "Event-to-Endurant via manifestation"
    description: "Perdurants manifest dispositions inhering in endurants. The manifests relation connects events to their underlying endurants."
    source: "Chunk 2:505-507"
  - pattern: "Event-to-Mode via foundation"
    description: "Externally dependent modes and relators are founded by unique events. The foundedBy relation connects modes/relators to their foundational event."
    source: "Chunk 2:207-219"
  - pattern: "Event-to-Life via lifeOf"
    description: "The life of an endurant is the mereological sum of all events that manifest it. lifeOf is functional relation associating endurant with its complete manifestation history."
    source: "Chunk 2:506-507"
  - pattern: "Process-to-Event via constitution"
    description: "Processes are constituted by events. Complex perdurants composed of simpler perdurants via constitutedBy relation."
    source: "Chunk 3:150-165"

ordering_mechanisms:
  - mechanism: "Temporal part accumulation"
    description: "Perdurants unfold in time accumulating temporal parts. Events have temporal parts that can be ordered."
    source: "Chunk 1:289-291"
  - mechanism: "Meet relation (Allen's algebra)"
    description: "Two perdurants meet when consecutive in time. Used for ordering events in a process."
    source: "Chunk 2:508-509, Chunk 3:176-183"
  - mechanism: "Monotonic constitution"
    description: "For processes manifesting same endurant, if p1 meets p2, all constituents of p1 also constitute p2. Establishes cumulative ordering."
    source: "Chunk 3:180-183"
  - mechanism: "Temporal interval containment"
    description: "For parthood between events, temporal interval framing parts is part of interval framing whole. For constitution, interval of constituent is part of interval of constituted."
    source: "Chunk 2:98-100"

causation_patterns:
  - pattern: "Disposition realization"
    description: "Dispositions (functions, capabilities, vulnerabilities) when realized produce manifestation events. Causation flows from disposition to event."
    source: "Chunk 1:321-323, Chunk 3:106-107"
  - pattern: "Event foundation"
    description: "Events found relators and externally dependent modes. E.g., wedding event founds marriage relator. Causal relationship from foundational event to dependent entity."
    source: "Chunk 2:207-210"
  - pattern: "Event constitution"
    description: "Simple events constitute complex events. E.g., punching events constitute boxing match. Causal aggregation pattern."
    source: "Chunk 2:69-73"
  - pattern: "Change via event variation"
    description: "Different temporal parts of event have different properties. Not genuine change but variation within modally fragile entity."
    source: "Chunk 3:114-117, Chunk 3:253-255"
  - pattern: "Change via focus endurant"
    description: "Genuine change in underlying endurant (the focus) causes different perdurant manifestations. E.g., change in intention causes different walking perdurant."
    source: "Chunk 3:256-263"

temporal_standards:
  - standard: "Allen's Interval Algebra (referenced)"
    description: "Meet relation between perdurants uses Allen's temporal relations. Events can meet (be consecutive in time)."
    source: "Chunk 3:176"
  - standard: "3D Ontology (vs 4D)"
    description: "UFO is a 3D ontology with fundamental distinction between endurants (exist wholly in time) and perdurants (unfold in time). Not 4D where all entities are perdurants."
    source: "Chunk 1:283-285"
  - standard: "Modal Fragility"
    description: "Events are modally fragile - no cross-world identity. They cannot be different from what they are. All parts and constituents are necessary."
    source: "Chunk 1:290-292, Chunk 2:72-73"

event_log_formats:
  - format: "N/A - Not addressed"
    description: "UFO does not define specific event log serialization formats. It is a foundational ontology providing conceptual foundations for event modeling."
    source: null

# Additional UFO-Specific Temporal Concepts

ufo_b_perdurant_theory:
  core_distinctions:
    - name: "Endurant vs Perdurant"
      description: "Endurants exist in time with all parts (can change); Perdurants unfold in time accumulating temporal parts (cannot change)."
      source: "Chunk 1:283-296"
    - name: "Modally fragile"
      description: "Perdurants have no cross-world identity. They cannot be different from what they are. All properties, parts, constituents are necessary."
      source: "Chunk 1:290-292"
    - name: "Past entities"
      description: "Perdurants only exist in the past - they are completed manifestations."
      source: "Chunk 1:289-290"

  event_endurant_connection:
    - mechanism: "Disposition manifestation"
      description: "Events are polygenic manifestations of (bundles of) dispositions. These dispositions are the focuses of the events."
      source: "Chunk 3:106-110"
    - mechanism: "Participation via disposition"
      description: "Endurant participates in perdurant if perdurant has part that is manifestation of disposition inhering in endurant."
      source: "Chunk 1:295-296"
    - mechanism: "Life as sum of manifestations"
      description: "Life of endurant = mereological sum of all manifestations. Each new manifestation creates new life (change OF life)."
      source: "Chunk 2:528-533"

  change_theory:
    - type: "Change IN endurant"
      description: "Endurant qualitatively changes while maintaining numerical identity. Properties vary across situations."
      source: "Chunk 1:286-288, Chunk 3:112-114"
    - type: "Change OF perdurant (variation)"
      description: "Different temporal parts of perdurant have different properties. Not genuine change."
      source: "Chunk 3:114-116, Chunk 3:253-255"
    - type: "Change to focus"
      description: "Change in underlying endurant (focus) causes different perdurant manifestations."
      source: "Chunk 3:256-263"

quality_checklist:
  event_types_extracted: true
  event_definitions_extracted: true
  temporal_relations_extracted: true
  lifecycle_patterns_extracted: true
  state_change_mechanisms_extracted: true
  agent_participation_extracted: true
  event_correlation_extracted: true
  ordering_mechanisms_extracted: true
  causation_patterns_extracted: true
  temporal_standards_extracted: true

relevance_to_udwo:
  event_entity: "UFO provides strong foundation: Perdurants as events, with temporal parts, modally fragile, manifest dispositions. Key axioms formalized in FOL."
  lifecycle_states: "Phases provide intrinsic lifecycle states; examples include Walk phases (Ongoing -> Finalized -> Successful/Redirected)."
  temporal_operators: "Meet relation from Allen's algebra; temporal part containment; monotonic constitution for ordering."
  causation: "Disposition realization pattern connects endurants to events via causation. Event foundation creates relators."
  agent_participation: "Participation via disposition manifestation; roles mediated by relators; focus relationship for intentional agents."
---

# UFO Temporal/Event Pattern Extraction

## Summary

This extraction captures UFO's theory of perdurants (events) and their relationships to endurants, with focus on:

1. **Event Types**: UFO distinguishes perdurants (events/processes) from endurants. Perdurants are modally fragile entities that unfold in time accumulating temporal parts. They include atomic events and composite processes.

2. **Event-Endurant Connection**: Events are manifestations of dispositions inhering in endurants. Endurants participate in events through this manifestation relationship. The "life" of an endurant is the sum of all its manifestations.

3. **Change Theory**: UFO carefully distinguishes:
   - Change IN endurant (genuine qualitative change while maintaining identity)
   - Change OF perdurant (variation - different temporal parts have different properties)
   - Change via focus (underlying endurant changes causing different manifestations)

4. **Temporal Relations**: Key relations include `meets` (Allen's temporal algebra for consecutive events), `constitutedBy` (event composition), `manifests` (event-disposition connection), and `lifeOf` (life as sum of manifestations).

5. **Lifecycle Patterns**: Phases represent intrinsic lifecycle states (e.g., Walk: OngoingWalk -> FinalizedWalk -> SuccessfulWalk/RedirectedWalk).

6. **State Change Mechanisms**: Disposition realization, quality value changes, phase transitions, role acquisition/relinquishment, and event constitution.

7. **Agent Participation**: Agents participate through role-playing (mediated by relators), bearing dispositions that manifest as events, and serving as focus of intentional events.

## Key Axioms for UDWO Integration

```
# Core Perdurant Axioms
Perdurant(x) -> ConcreteIndividual(x)
Endurant(x) -> NOT Perdurant(x)

# Manifestation/Participation
manifests(x, y) -> Endurant(x) AND Perdurant(y)
lifeOf(x, y) <-> Perdurant(x) AND Endurant(y) AND forall z (O(z,x) <-> Perdurant(z) AND manifests(z, y))

# Meet (temporal ordering)
meet(x, y) -> Perdurant(x) AND Perdurant(y)

# Event constitution (modally necessary for perdurants)
constitutedBy(x, y) AND Perdurant(x) -> NECESSARILY (ex(x) -> constitutedBy(x, y))

# Foundation (events found relators/modes)
foundedBy(x, y) -> (ExternallyDependentMode(x) OR Relator(x)) AND Perdurant(y)
```

## Gaps/Limitations

- UFO-B (full perdurant theory) not fully detailed in this paper
- No event log serialization format specified (foundational ontology, not data format)
- UFO-C (social/intentional entities including agents) mentioned but not detailed
- Temporal operators limited to Allen's meet relation; no formal temporal logic integration
