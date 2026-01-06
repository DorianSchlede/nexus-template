---
paper_id: "07-Classifying_Processes_Barry_Smith"
title: "Classifying Processes: An Essay in Applied Ontology"
authors: ["Barry Smith"]
year: 2012
source: "Ratio (new series) XXV 4"
extraction_version: "2.0"
extraction_date: "2025-12-31"

ontological_primitives:
  - term: "Continuant"
    definition: "Entity that can be sliced to yield parts only along the spatial dimension; wholly present at each moment of its existence; exists in time but has no temporal parts"
    source: "Chunk 1:350-362, 398-402"
    unique_aspects: "Adapted from Zemach's 'things' but generalized to include dependent entities like qualities and dispositions, not just substances"

  - term: "Occurrent"
    definition: "Entity that can be sliced to yield parts along any spatial and temporal dimension; four-dimensional; occurs rather than exists"
    source: "Chunk 1:370-382, 430-440"
    unique_aspects: "BFO departs from Zemach - multiple occurrents can occupy same spatiotemporal region (running + getting warmer)"

  - term: "Process"
    definition: "An occurrent that occupies spatiotemporal regions and spans temporal intervals; is temporally extended; ARE changes in independent continuant participants"
    source: "Chunk 1:548-563, 691-692"
    unique_aspects: "Processes cannot change (they ARE changes). No qualities of processes exist - attribution handled via instantiation of universals"

  - term: "Process Boundary"
    definition: "An occurrent that spans temporal instants rather than intervals; beginnings and endings of processes"
    source: "Chunk 1:548-563"
    unique_aspects: "Distinguished from processes by lacking temporal extension"

  - term: "Quality"
    definition: "A dependent continuant that does not require a process of realization; first-class entity (trope/individual accident); inheres in independent continuants"
    source: "Chunk 1:405-409, 458-459, 499-502"
    unique_aspects: "BFO explicitly accepts qualities as first-class entities, distinguishing them from dispositions which require realization"

  - term: "Disposition"
    definition: "A dependent continuant that requires a process in order to be realized or manifested (e.g., solubility, fragility)"
    source: "Chunk 1:405-409"
    unique_aspects: "Contrasted with quality - needs realization process"

  - term: "Process Profile"
    definition: "That part of a process which serves as the target of selective abstraction focused on a specific structural dimension; the fundamentum comparationis between processes"
    source: "Chunk 2:124-146"
    unique_aspects: "NOVEL CONCEPT - enables comparison of processes along specific dimensions while abstracting away others; not reducible to spatiotemporal regions"

  - term: "Universal (Type)"
    definition: "The sorts of entities represented by general terms in scientific theories; have instances which are observed in experiments"
    source: "Chunk 1:100-104"
    unique_aspects: "Used synonymously with 'type'; some literature uses 'class' for same concept"

  - term: "Determinable Universal"
    definition: "A quality universal that is rigid - if exemplified at any time during bearer's existence, exemplified at every such time (e.g., temperature, length, mass)"
    source: "Chunk 1:500-510"
    unique_aspects: "Rigidity is key distinguishing feature from determinates"

  - term: "Determinate Universal"
    definition: "A specification of a determinable universal with a specific value (e.g., 37.0 C temperature, 1.6 meter length, 4 kg mass)"
    source: "Chunk 1:500-502"
    unique_aspects: "Independent of unit systems - would be instantiated even without any measurement system"

structural_patterns:
  - pattern_name: "Bicategorial Architecture"
    structure: "Two fundamental categories (continuant/occurrent) with different logico-ontological orders, connected through participation rather than parthood"
    instances:
      - "Continuants vs Occurrents in BFO"
      - "Three-dimensionalism vs Four-dimensionalism unified"
      - "SNAP vs SPAN ontologies"
    source: "Chunk 1:339-342, 430-440"

  - pattern_name: "Ontological Square"
    structure: "2x2 grid: (Universal vs Particular) x (Independent vs Dependent) = 4 categories"
    instances:
      - "Independent Continuant Type (planet, organism, cell)"
      - "Independent Continuant Instance (this planet, this organism)"
      - "Dependent Continuant Type (temperature, sickle shape)"
      - "Dependent Continuant Instance (John's temperature, this sickle shape)"
    source: "Chunk 1:446-452, 478-496"

  - pattern_name: "Ontological Sextet"
    structure: "Extension of square to 2x3: adds Occurrent column (Type/Instance); shows processes as dependent on independent continuants via specific dependence"
    instances:
      - "Occurrent Type (course of temperature changes, life of organism)"
      - "Occurrent Instance (John's life, the life of this cell)"
    source: "Chunk 1:852-859, 872-891"

  - pattern_name: "Determinable-Determinate Hierarchy"
    structure: "Genus-species cascade from general (determinable) to specific (determinate) quality/process universals"
    instances:
      - "temperature -> 37.0 C temperature"
      - "speed profile -> constant speed profile -> 2 mph constant speed profile"
      - "cyclical process profile -> regular cyclical process profile -> 3 bpm cyclical process profile"
    source: "Chunk 1:500-510, Chunk 2:185-197, 246-254"

  - pattern_name: "Specific Dependence Relation"
    structure: "Entity A specifically depends on Entity B = A cannot migrate to another bearer (contrasted with generic dependence)"
    instances:
      - "Quality depends on its bearer (temperature of laptop cannot migrate)"
      - "Process depends on its participants"
    source: "Chunk 1:631-636, 848-852"

  - pattern_name: "Temporal vs Occurrent Parthood"
    structure: "temporal_part_of is narrower than occurrent_part_of; temporal part is exact restriction of process to a proper temporal subregion"
    instances:
      - "First quarter of football game IS temporal part of game"
      - "Footballer's single heartbeat IS occurrent part but NOT temporal part of game"
    source: "Chunk 1:570-593"

  - pattern_name: "Process Profile Hierarchy"
    structure: "Nested levels of abstraction for process classification: quality profiles -> rate profiles -> cyclical profiles"
    instances:
      - "Quality process profiles (temperature sequence)"
      - "Rate process profiles (speed, acceleration)"
      - "Cyclical process profiles (heartbeat, drumming)"
    source: "Chunk 2:149-254"

novel_concepts:
  - concept: "Process Profile"
    definition: "That occurrent entity in processes themselves which serves as fundamentum comparationis when comparing processes along structural dimensions"
    novelty_claim: "Solves the problem of classifying process measurement data without introducing qualities of occurrents; enables principled comparison of processes"
    source: "Chunk 2:124-146"

  - concept: "Process Profile Universal"
    definition: "A universal instantiated by process profiles; the basis for saying two processes share 'the same' rate, rhythm, etc."
    novelty_claim: "Provides typing mechanism for processes that respects four-dimensionalist constraints (no change in occurrents)"
    source: "Chunk 2:126-131"

  - concept: "Rate Process Profile"
    definition: "Process profile focused on ratios between quality magnitudes and intervals of elapsed time (e.g., speed = distance/time)"
    novelty_claim: "Hierarchy of rate profiles (speed -> acceleration -> jerk) provides systematic classification"
    source: "Chunk 2:174-197"

  - concept: "Cyclical Process Profile"
    definition: "Subtype of rate process profile where salient ratio is number of cycles per unit time"
    novelty_claim: "Handles regular and irregular cyclical processes (diagnostic significance)"
    source: "Chunk 2:238-273"

  - concept: "Ontological Sextet"
    definition: "Extension of Aristotelian ontological square to include occurrent universals and instances alongside continuants"
    novelty_claim: "Bridges classical substance/accident metaphysics with four-dimensionalist process ontology"
    source: "Chunk 1:852-859, 872-891"

  - concept: "Processes as Changes (not changing entities)"
    definition: "Processes ARE changes in continuant participants; therefore processes cannot change themselves"
    novelty_claim: "Resolves apparent paradox of 'speeding up a process' - we ensure different (quicker) process occurs, not that same process changes"
    source: "Chunk 1:691-697"

  - concept: "Generic vs Specific Dependence"
    definition: "Generic dependence allows migration via copying (information artifacts); specific dependence ties entity to particular bearer"
    novelty_claim: "Information artifacts (measurement records) are generically dependent; qualities/processes are specifically dependent"
    source: "Chunk 1:631-636"

semantic_commitments:
  - commitment: "Bicategorialism"
    position: "Both three-dimensionalist (continuant) and four-dimensionalist (occurrent) perspectives have validity and are unified within single framework"
    implications: "Avoids forced choice between perspectives; can use most natural framework for each domain"
    source: "Chunk 1:339-342"

  - commitment: "No Qualities of Occurrents"
    position: "Processes do not have qualities; process attributions are handled through instantiation of process universals"
    implications: "Maintains ontological parsimony; 'has speed v' means 'instance_of motion with speed v'"
    source: "Chunk 1:677-678, 794-808"

  - commitment: "Occurrents Cannot Change"
    position: "Four-dimensionalist treatment of occurrents entails that processes cannot change (they ARE changes)"
    implications: "No time-indexed parthood for occurrents (unlike continuants); universals of occurrents are always rigid"
    source: "Chunk 1:688-698, 728-738"

  - commitment: "Ontological Realism"
    position: "Ontology should employ classifications based on established scientific understanding of entities and relations"
    implications: "Ontologies are not merely conventions but track real types in the world"
    source: "Chunk 1:67-77, 90-91"

  - commitment: "Universals Exist"
    position: "Types/universals are real entities represented by general terms; have instances"
    implications: "Recapitulates Aristotelian realism about universals"
    source: "Chunk 1:100-104, 450-451"

  - commitment: "Unit-Independence of Universals"
    position: "Determinate quality/process universals are independent of measurement systems; would be instantiated even without any unit system"
    implications: "The universal 37C temperature is real independent of Celsius scale"
    source: "Chunk 1:511-516, Chunk 2:200-204"

boundary_definitions:
  - entity_type: "Continuant vs Occurrent"
    identity_criteria: "Sliceability: continuants slice only spatially; occurrents slice spatially AND temporally"
    boundary_cases: "The distinction is categorical - no entity is both; all parts of continuants are continuants, all parts of occurrents are occurrents"
    source: "Chunk 1:350-354, 370-382, 430-433"

  - entity_type: "Process"
    identity_criteria: "Occupies spatiotemporal region; has temporal extension; multiple processes can occupy same region"
    boundary_cases: "Running down street and getting warmer can be co-located distinct processes"
    source: "Chunk 1:426-429, 548-563"

  - entity_type: "Temporal Part vs Occurrent Part"
    identity_criteria: "Temporal part: exact restriction to proper temporal subregion; Occurrent part: any part of occurrent"
    boundary_cases: "Heartbeat is occurrent part but not temporal part of football game (other things co-occur)"
    source: "Chunk 1:574-593"

  - entity_type: "Process Profile"
    identity_criteria: "Occurrent entity IN the process that serves as basis for comparison; not reducible to spatiotemporal/temporal regions"
    boundary_cases: "Duration comparisons don't need profiles (use temporal regions); profiles needed when something in process itself is fundamentum comparationis"
    source: "Chunk 2:139-146"

  - entity_type: "Specific vs Generic Dependence"
    identity_criteria: "Specific: cannot migrate (temperature); Generic: can be copied/transferred (information artifact)"
    boundary_cases: "Is a digital copy of data the same data or different data? (generically dependent)"
    source: "Chunk 1:631-636"

temporal_modeling:
  - aspect: "Two Modes of Temporal Existence"
    approach: "Continuants 'exist' during temporal intervals; Occurrents 'occur' during temporal intervals"
    mechanism: "Fundamental ontological difference in relation to time"
    source: "Chunk 1:434-437"

  - aspect: "Temporal Parthood (Occurrents)"
    approach: "Non-indexed; if p1 is part of p2, this holds timelessly (like t1 being part of t2)"
    mechanism: "Defined via exact restriction to temporal subregion"
    source: "Chunk 1:574-582, 722-727"

  - aspect: "Continuant Parthood"
    approach: "Time-indexed; continuants gain and lose parts over time"
    mechanism: "part_of(x, y, t) relation"
    source: "Chunk 1:719-723"

  - aspect: "Rigidity of Occurrent Universals"
    approach: "If occurrent instantiates universal at some time, instantiates it at all times"
    mechanism: "Contrasts with non-rigid continuant universals (larva, fetus)"
    source: "Chunk 1:735-738"

  - aspect: "Instantaneous Rate Values"
    approach: "Defined as limit of interval-based values"
    mechanism: "John has speed v at t = for any epsilon, exists interval around t where speed differs from v by less than epsilon"
    source: "Chunk 2:218-232"

  - aspect: "Process Duration"
    approach: "Process p has duration d = p spans temporal region t and t instance_of universal temporal region with duration d"
    mechanism: "Attribution handled via instantiation, not quality predication"
    source: "Chunk 1:834-836"

agency_spectrum:
  - agent_type: "Human Organism"
    capabilities: "Bearer of qualities, participant in processes; has dispositions requiring realization"
    constraints: "Not explicitly discussed as agent - paper focuses on processes/participants, not intentionality"
    source: "Implicit throughout (John as example bearer)"

  - agent_type: "Participant (Independent Continuant)"
    capabilities: "Participates in processes; bears qualities and dispositions; has spatial location"
    constraints: "Paper uses 'participant' rather than 'agent' - more general relation"
    source: "Chunk 1:337, 412-414, 848-850"

knowledge_representation:
  - mechanism: "Ontology as Directed Acyclic Graph"
    formalism: "Nodes = types/universals; Edges = is_a and part_of relations"
    reasoning: "is_a: all instances of subtype are instances of supertype; part_of: every instance of part type is part of some instance of whole type"
    source: "Chunk 1:78-106, 126-147"

  - mechanism: "Common Logic Interchange Format (CLIF)"
    formalism: "ISO Standard; expressivity equivalent to first-order logic"
    reasoning: "Full first-order reasoning"
    source: "Chunk 1:154-158"

  - mechanism: "Web Ontology Language (OWL-DL)"
    formalism: "Description Logic fragment of FOL; restricted expressivity"
    reasoning: "Decidable classification and consistency checking via reasoners"
    source: "Chunk 1:159-184"

  - mechanism: "Process Classification via Universal Instantiation"
    formalism: "motion p has speed v translates to: motion p instance_of universal motion with speed v"
    reasoning: "Attributions become type assertions; enables systematic classification"
    source: "Chunk 1:794-801"

emergence_indicators:
  - phenomenon: "Nested Process Wholes"
    mechanism: "Processes embedded within larger process wholes (ball motion -> ball-table system -> ball-table-earth system -> solar system)"
    evidence: "Physiological processes nested: left ventricle interior -> cardiovascular system -> bodily systems -> organism -> population"
    source: "Chunk 2:279-302"

  - phenomenon: "Normal Processes"
    mechanism: "Defined for larger population; individual deviations measured relative to population norm"
    evidence: "Normal qualities defined for population; normal processes analogously defined"
    source: "Chunk 2:300-302"

  - phenomenon: "Process Profiles as Truthmakers"
    mechanism: "Time series graphs have process profiles as their truthmakers; graphs represent but don't constitute the process"
    evidence: "Proposed extension: ontology of time series graphs based on process profiles"
    source: "Chunk 2:303-310"

integration_surfaces:
  - surface: "Ontological Square -> Ontological Sextet"
    connects_to: ["Aristotle's Categories", "Lowe's Four-Category Ontology", "Traditional substance/accident metaphysics"]
    alignment_quality: "Good - explicit extension that preserves classical structure while adding occurrents"
    source: "Chunk 1:446-452, 464-469, 852-859"

  - surface: "Zemach's Four Ontologies"
    connects_to: ["Continuant/occurrent distinction origins", "Sliceability criterion"]
    alignment_quality: "Partial - BFO generalizes Zemach (adds dependent continuants, allows co-located occurrents)"
    source: "Chunk 1:349-354, 403-429"

  - surface: "Gene Ontology (GO)"
    connects_to: ["Biological process sub-ontology", "Molecular function", "Cellular component"]
    alignment_quality: "Good - GO uses BFO as upper ontology; 30,000 terms for biological processes"
    source: "Chunk 1:190-207"

  - surface: "Ontology for Biomedical Investigations (OBI)"
    connects_to: ["Experimental protocols", "Sample processing", "Statistical algorithms"]
    alignment_quality: "Good - OBI aims to annotate experimental results using BFO-conformant vocabulary"
    source: "Chunk 1:239-252"

  - surface: "RICORDO Project"
    connects_to: ["Physiological models", "Ordinary differential equations", "Biomedical data interoperability"]
    alignment_quality: "Proposed - process profiles as foundation for interoperability of physiological models"
    source: "Chunk 2:104-108"

  - surface: "Mathematical Models of Dynamic Systems"
    connects_to: ["Differential equations", "Time series", "Physics models"]
    alignment_quality: "Proposed future work - process profiles as semantics for differential equations"
    source: "Chunk 2:307-310"

gaps_and_tensions:
  - gap_type: "Omission"
    description: "No account of agency, intentionality, or goal-directedness"
    implications: "Cannot distinguish intentional action from mere process; no connection to agent-based frameworks"
    source: "Implicit - 'participant' used but never 'agent' with intentional connotations"

  - gap_type: "Omission"
    description: "No treatment of causation between processes"
    implications: "Cannot model causal chains or dependencies between processes"
    source: "Implicit - only participation relation discussed, not causation"

  - gap_type: "Omission"
    description: "No formalization of process profile theory"
    implications: "Process profiles introduced conceptually but not axiomatized; boundary between profile types unclear"
    source: "Chunk 2:276-310 acknowledges 'first steps' and future work needed"

  - gap_type: "Tension"
    description: "Processes cannot change, but we speak of 'speeding up' processes"
    implications: "Linguistic intuitions conflict with ontological commitment; requires reinterpretation of common speech"
    source: "Chunk 1:693-697"

  - gap_type: "Tension"
    description: "Bicategorialism aims to unify but maintains categorical divide"
    implications: "Continuants and occurrents never share parts or stand in parthood relations; connection only through participation"
    source: "Chunk 1:430-440"

  - gap_type: "Underspecified"
    description: "When do multiple dimensions warrant multiple process profiles vs single complex profile?"
    implications: "Wiggers diagram shows 6 dimensions - are there 6 profiles or 1 composite profile?"
    source: "Chunk 2:33-41, 127-137"

  - gap_type: "Underspecified"
    description: "Relationship between process profiles and the processes they are 'in'"
    implications: "Is profile a part of process? A dependent entity? A projection? Ontological status unclear"
    source: "Chunk 2:145-146 says 'in the processes themselves' but doesn't formalize"

  - gap_type: "Underspecified"
    description: "How plans/protocols relate to processes they define"
    implications: "Score represents AND instructs performance - dual role not analyzed"
    source: "Chunk 2:326-333 mentions as future work"

empirical_grounding:
  - type: "Biomedical Ontology Application"
    domain: "Gene/protein annotation"
    scale: "30,000 terms in Gene Ontology; 100+ BFO user groups"
    findings: "GO enables cross-species comparison of genomic data; supports computational reasoning over experimental results"
    source: "Chunk 1:190-207, 283-284"

  - type: "Physiological Measurement"
    domain: "Cardiac processes"
    scale: "Wiggers diagram - 6 measurement dimensions for left ventricle"
    findings: "Multiple simultaneous process profiles instantiated in each heartbeat; supports systematic classification of cardiac events"
    source: "Chunk 2:33-41"

  - type: "Clinical Temperature Monitoring"
    domain: "Patient vital signs"
    scale: "Individual patient over time"
    findings: "Temperature chart records sequence of determinate temperature qualities; 'normal' defined relative to population"
    source: "Chunk 2:154-158, 300-302"

surprises:
  - "PROCESSES CANNOT CHANGE - This is counterintuitive but follows necessarily from 4D treatment. Processes ARE changes, so saying a process changes is saying 'a change changes'. The paper resolves this by reinterpreting 'speed up the process' as 'ensure a different, quicker process occurs.'"

  - "NO QUALITIES OF PROCESSES - There is no counterpart on the occurrent side for qualities of continuants. Speed is NOT a quality of a motion; rather, the motion INSTANTIATES a speed-type universal. This is ontologically parsimonious but conceptually surprising."

  - "PROCESS PROFILES ARE NOVEL - The entire concept of process profile appears to be original to this paper. It solves a genuine problem (how to classify process measurements without violating 4D constraints) in an elegant way."

  - "MULTIPLE OCCURRENTS CAN OVERLAP SPATIOTEMPORALLY - Unlike Zemach's events which are the whole content of a region, BFO processes can co-occupy the same spacetime (running AND getting warmer). This is a substantive departure from the source framework."

  - "BICATEGORIALISM IS NOT PLURALISM - BFO doesn't say 'use whichever framework you prefer'; it says both perspectives are UNIFIED within a single framework through the participation relation. The division is maintained but bridged."

quality_checklist:
  used_paper_terminology: true
  novel_concepts_found: 6
  gaps_found: 8
  surprises_noted: 5
  chunk_references_included: true
  avoided_category_forcing: true
  preserved_nuance: true
---

# Classifying Processes: An Essay in Applied Ontology

## Paper Summary

This 2012 paper by Barry Smith introduces a framework for classifying processes within Basic Formal Ontology (BFO), addressing a specific problem: how to represent measurement data about processes (speed, rate, rhythm) when the BFO ontology lacks qualities of occurrents.

## Core Contribution

The paper's main innovation is the concept of **Process Profile** - an occurrent entity within a process that serves as the basis for comparison along specific structural dimensions. This allows process measurement attributions to be handled through universal instantiation rather than quality predication, maintaining BFO's ontological parsimony.

## Key Arguments

1. **Bicategorialism**: BFO unifies three-dimensionalist (continuant) and four-dimensionalist (occurrent) perspectives within a single framework, avoiding forced choice between them.

2. **Processes Cannot Change**: Since processes ARE changes in their continuant participants, they cannot themselves change. This resolves apparent paradoxes in how we speak about processes.

3. **Attribution via Instantiation**: "Motion p has speed v" should be interpreted as "Motion p instance_of universal motion-with-speed-v", not as predication of a quality.

4. **Process Profiles Enable Classification**: By abstracting along structural dimensions (speed, rate, rhythm), we can systematically classify processes into hierarchies of determinable and determinate universals.

## Theoretical Framework

The paper extends the classical Aristotelian Ontological Square (universal/particular x independent/dependent) into an **Ontological Sextet** by adding the occurrent column. This shows how processes relate to process universals analogously to how continuants relate to continuant universals.

## Surprising Findings

1. No qualities of processes exist in BFO - all attribution is via instantiation
2. Multiple processes can occupy the same spatiotemporal region (departure from Zemach)
3. The participation relation is the only bridge between continuants and occurrents - no shared parts
4. Process profiles are first-class occurrent entities, not mere abstractions
5. The theory is explicitly preliminary - formalization acknowledged as future work

## Connections to Other Work

- **Gene Ontology**: 30,000 terms for biological processes using BFO
- **PROV-O**: Shares activity/participant structure (not explicitly cited but compatible)
- **Zemach's Four Ontologies**: Source of continuant/occurrent distinction, but significantly modified
- **Aristotle's Categories**: Ontological square recapitulated and extended

## Gaps and Limitations

- No account of agency or intentionality
- Causation between processes not addressed
- Process profile theory not axiomatized
- Relationship between profiles and their host processes underspecified
- Plans/protocols and their relationship to processes left as future work
