---
paper_id: "04"
title: "A semantic approach to mapping the Provenance Ontology to Basic Formal Ontology"
authors: ["Tim Prudhomme", "Giacomo De Colle", "Austin Liebers", "Alec Sculley", "Peihong Karl Xie", "Sydney Cohen", "John Beverley"]
year: 2025
source: "Nature Scientific Data (accepted)"
doi: "10.1038/s41597-025-04580-1"
extraction_version: "2.0"
extraction_date: "2025-12-31"

ontological_primitives:
  - term: "ontology mapping"
    definition: "A statement <s, p, o> such that 's' is a subject term representing a class or object property in an ontology, 'o' is an object term representing a class or object property in some other ontology, and 'p' is a predicate that specifies how s and o relate"
    source: "Chunk 1:51-53"
    unique_aspects: "Treats mappings as first-class semantic objects with formal structure, not informal associations"

  - term: "ontology alignment"
    definition: "A set of ontology mappings"
    source: "Chunk 1:54"
    unique_aspects: "Distinguishes single mappings from complete alignment sets"

  - term: "synonymous alignment"
    definition: "Maximum semantic interoperability achieved via alignment where every term in both ontologies is mapped using only predicates representing equivalence relations"
    source: "Chunk 1:66-69"
    unique_aspects: "Defines theoretical upper bound of semantic interoperability - bidirectional interpretation between theories"

  - term: "conservative extension"
    definition: "An alignment that does not change the semantic relationships between terms WITHIN each ontology - specifically not changing subsumption relationships entailed by formulae of an ontology's signature"
    source: "Chunk 1:240-257"
    unique_aspects: "Uses approximate deductive difference as tractable proxy for undecidable full conservativity"

  - term: "translation definition"
    definition: "An equivalence relation mapping which conservatively extends a logical theory"
    source: "Chunk 1:297-300"
    unique_aspects: "The building block for full interpretability between ontologies"

  - term: "process boundary"
    definition: "BFO concept - indivisible boundaries of processes that exist only at an instant of time"
    source: "Chunk 1:913-915"
    unique_aspects: "Key distinction for handling instantaneous vs extended temporal entities"

  - term: "Qualification Pattern"
    definition: "A form of reification in PROV-O that reifies binary relations as instances of class PROV Influence to allow n-ary information representation"
    source: "Chunk 1:892-906"
    unique_aspects: "Standard PROV technique for circumventing description logic's binary relation limits"

structural_patterns:
  - pattern_name: "Triadic Provenance Core"
    structure: "Entity-Activity-Agent triad connected by participation/influence relations"
    instances:
      - "PROV Entity - wasGeneratedBy -> PROV Activity"
      - "PROV Activity - wasAssociatedWith -> PROV Agent"
      - "PROV Agent - participates in -> PROV Activity - affects -> PROV Entity"
    source: "Chunk 1:633-648, 734-764"

  - pattern_name: "Disjoint Union Stratification"
    structure: "A parent class mapped to disjoint union of mutually exclusive subclasses"
    instances:
      - "PROV Influence -> disjoint union of (BFO process OR BFO process boundary)"
      - "BFO entity -> disjoint (continuant OR occurrent)"
      - "PROV Entity mapped to union of (independent continuant NOT spatial region) OR (generically dependent continuant) OR (specifically dependent continuant)"
    source: "Chunk 1:911-920, Chunk 2:16-24"

  - pattern_name: "Subsumption Cascade"
    structure: "Single-direction bridge allowing multiple source terms to map to one target term"
    instances:
      - "Multiple PROV object properties -> subproperty of -> BFO participates in"
      - "PROV wasGeneratedBy, wasInvalidatedBy, wasAssociatedWith all subsume to BFO/RO participates in variants"
    source: "Chunk 1:158-164, 734-764"

  - pattern_name: "Intersection Equivalence"
    structure: "Equivalence defined as intersection of concepts from different ontologies"
    instances:
      - "PROV Person = intersection of (CCO Person AND PROV Agent)"
      - "PROV Organization = intersection of (CCO Organization AND PROV Agent)"
    source: "Chunk 1:773-788"

  - pattern_name: "Role-Realization Dependency"
    structure: "Agent -> bears -> Role -> realized in -> Activity"
    instances:
      - "PROV Agent mapped to BFO material entity that bears BFO role realized in PROV Activity"
    source: "Chunk 1:654-669"

novel_concepts:
  - concept: "Approximate Deductive Difference"
    definition: "The set of subsumptions, for a given ontology signature, entailed in one ontology but not in another"
    novelty_claim: "Tractable substitute for undecidable full conservativity checking in OWL 2 DL"
    source: "Chunk 1:248-257"

  - concept: "Interpretability as Interoperability"
    definition: "One ontology is interpretable in another if there exists a set of translation definitions such that the second ontology combined with alignment entails the first"
    novelty_claim: "Formalizes semantic interoperability as logical interpretability - 'interpretability enhances interoperability'"
    source: "Chunk 1:304-346"

  - concept: "SWRL-mediated conditional mapping"
    definition: "Using SWRL rules to restrict domain/range of mappings based on runtime type of instances"
    novelty_claim: "Allows one PROV property (atLocation) to map to different BFO properties (occurs in vs located in) depending on whether subject is Activity vs Entity"
    source: "Chunk 1:836-880"

  - concept: "Influence-as-Event (not Capacity)"
    definition: "PROV Influence reinterpreted as BFO processes/process boundaries rather than BFO dispositions/capacities"
    novelty_claim: "Radical divergence from original PROV-O definition - influences are events in time, not capacities of agents"
    source: "Chunk 1:923-971, Chunk 2:28-76"

semantic_commitments:
  - commitment: "Continuant-Occurrent Disjointness"
    position: "Strict enforcement - nothing can be both a continuant and occurrent"
    implications: "Prevents PROV Agent from being PROV Activity despite PROV-O Requirement VI4 allowing this"
    source: "Chunk 1:694-731"

  - commitment: "Endurantism for Agents"
    position: "PROV Agents are material entities wholly present at each moment, not 4D spacetime worms"
    implications: "Software agents are material realizations of software (the hardware running the code), not abstract"
    source: "Chunk 1:654-659"

  - commitment: "Open-World Assumption"
    position: "OWL 2 open-world semantics - existence axioms don't require data presence"
    implications: "Saying Agent participates in Activity doesn't require Activity data to be present"
    source: "Chunk 1:663-665"

  - commitment: "Moderate Realism about Roles"
    position: "Roles are externally determined (unlike functions which are internally determined by physical makeup)"
    implications: "PROV Role is subclass of BFO Role, not BFO Function - context-dependent, not intrinsic"
    source: "Chunk 2:103-114"

  - commitment: "GDC for Information Content"
    position: "Information entities are Generically Dependent Continuants - can have multiple copies without specific bearer"
    implications: "PROV Plan is GDC, PROV Bundle is CCO Information Content Entity"
    source: "Chunk 2:116-143"

boundary_definitions:
  - entity_type: "PROV Entity vs PROV Activity"
    identity_criteria: "Disjoint in PROV-O by axiom; mapped to BFO continuant vs BFO occurrent which are also disjoint"
    boundary_cases: "Some W3C examples violate this - publication activity mistakenly tagged with wasAttributedTo (Entity domain)"
    source: "Chunk 1:641-645, Chunk 2:233-239"

  - entity_type: "Process vs Process Boundary"
    identity_criteria: "Process is temporally extended; process boundary is instantaneous"
    boundary_cases: "PROV Influence subclasses split - Generation/Start/End are process boundaries; Communication/Derivation are processes"
    source: "Chunk 1:911-920, Chunk 2:16-24"

  - entity_type: "CCO Agent vs PROV Agent"
    identity_criteria: "CCO Person is NOT subclass of CCO Agent; PROV Person IS subclass of PROV Agent"
    boundary_cases: "Requires intersection mapping - PROV Person = CCO Person AND PROV Agent"
    source: "Chunk 1:770-788"

  - entity_type: "PROV Plan vs CCO Plan"
    identity_criteria: "CCO Plan constrained to prescription of intentional acts; PROV Plan allows any activities/processes"
    boundary_cases: "No equivalent mapping despite similar labels - PROV Plan is broader"
    source: "Chunk 2:127-143"

temporal_modeling:
  - aspect: "Instantaneous Events"
    approach: "Process boundaries - exist only at instants, indivisible"
    mechanism: "PROV InstantaneousEvent equivalentClass BFO process boundary"
    source: "Chunk 1:913-915, Chunk 2:17-20"

  - aspect: "Extended Processes"
    approach: "BFO process - unfolds over temporal interval"
    mechanism: "PROV Activity equivalentClass BFO process; PROV Communication, Derivation subclass of BFO process"
    source: "Chunk 1:682-691"

  - aspect: "Process Start/End"
    approach: "Temporal boundaries of processes"
    mechanism: "PROV Start equivalentClass CCO process beginning; PROV End equivalentClass CCO process ending"
    source: "Chunk 2:93-100"

  - aspect: "Time Data Properties"
    approach: "Complex multi-entity chain rather than direct property"
    mechanism: "Activity -> occupies -> temporal region -> has first instant -> instant -> designated by -> Time of Day Identifier -> has date time value -> xsd:dateTime"
    source: "Chunk 2:200-218"

agency_spectrum:
  - agent_type: "PROV Agent (general)"
    capabilities: "Bears responsibility for activity, exists as material entity, participates in activities"
    constraints: "Must participate in some activity; must bear role realized in activity"
    source: "Chunk 1:654-668"

  - agent_type: "PROV Person"
    capabilities: "Full human agency, intersection of CCO Person and PROV Agent"
    constraints: "Not all CCO Persons are PROV Agents (must have participated in activity)"
    source: "Chunk 1:770-777"

  - agent_type: "PROV SoftwareAgent"
    capabilities: "Running software as agent"
    constraints: "Mapped as material entity - the physical realization (hardware running code), not abstract"
    source: "Chunk 1:657-659"

  - agent_type: "PROV Organization"
    capabilities: "Collective agent, intersection of CCO Organization and PROV Agent"
    constraints: "CCO Group of Agents is subclass of BFO object aggregate; can also be singular agent (e.g., sports team)"
    source: "Chunk 1:787-796"

knowledge_representation:
  - mechanism: "Ontology Language"
    formalism: "OWL 2 DL (SROIQ description logic) for BFO/RO/CCO; OWL 2 RL (DLP) for PROV-O"
    reasoning: "HermiT reasoner - hypertableau calculus for satisfiability/consistency; automated classification"
    source: "Chunk 1:201-206, 428-431"

  - mechanism: "Mapping Serialization"
    formalism: "RDF Turtle with reified OWL axioms using annotatedSource/annotatedProperty/annotatedTarget"
    reasoning: "SPARQL queries for validation; ROBOT tool for ontology operations"
    source: "Chunk 1:510-528"

  - mechanism: "Complex Mappings"
    formalism: "SWRL rules for conditional domain/range restrictions; OWL property chains for relation composition"
    reasoning: "HermiT implements SWRL; allows runtime type-dependent mapping selection"
    source: "Chunk 1:168-183, 843-880"

  - mechanism: "Mapping Metadata"
    formalism: "SSSOM vocabulary annotations (subject_label, object_label, mapping_justification)"
    reasoning: "Machine-readable provenance for each mapping decision"
    source: "Chunk 1:546-558"

emergence_indicators:
  - phenomenon: "Emergent Inconsistencies"
    mechanism: "Alignment discovers inconsistencies not visible in individual ontologies"
    evidence: "Found 4 inconsistent examples in W3C PROV-O documentation - 2 inconsistent with PROV-O alone, 2 inconsistent with alignment"
    source: "Chunk 2:229-257"

  - phenomenon: "Inference Enrichment"
    mechanism: "BFO axioms produce new inferences over PROV-O data"
    evidence: "New SPARQL queries possible using BFO classes; semantic reasoner discovers implicit information"
    source: "Chunk 1:106-112"

  - phenomenon: "Cross-Ontology Disjointness"
    mechanism: "Mapping induces new disjoint relations not in either source ontology"
    evidence: "PROV Agent becomes disjoint with PROV Activity via BFO continuant/occurrent disjointness"
    source: "Chunk 1:715-720, 457-458"

integration_surfaces:
  - surface: "Agent concept"
    connects_to: ["PROV Agent", "BFO material entity", "CCO Agent", "BFO role bearer"]
    alignment_quality: "Good for CCO Agent (equivalence via 'agent in' relation); subsumption for BFO"
    source: "Chunk 1:654-679"

  - surface: "Activity/Process"
    connects_to: ["PROV Activity", "BFO process", "BFO occurrent"]
    alignment_quality: "Strong equivalence - PROV Activity equivalentClass BFO process"
    source: "Chunk 1:682-691"

  - surface: "Entity concept"
    connects_to: ["PROV Entity", "BFO continuant", "BFO independent/generically dependent/specifically dependent continuant"]
    alignment_quality: "Subsumption only - PROV Entity is complex union, not equivalent to single BFO class"
    source: "Chunk 1:633-645"

  - surface: "SOSA/SSN Alignment"
    connects_to: ["SOSA ontology", "Semantic Sensor Network", "PROV-SOSA alignment"]
    alignment_quality: "Consistent - PROV-BFO alignment combined with PROV-SOSA alignment produces SOSA-BFO alignment"
    source: "Chunk 1:439-445, Chunk 2:313-315"

  - surface: "Location concept"
    connects_to: ["PROV Location", "BFO site"]
    alignment_quality: "Equivalence - but note PROV Location allows 'non-geographic place' like database row"
    source: "Chunk 1:808-816"

gaps_and_tensions:
  - gap_type: "Fundamental Design Tension"
    description: "PROV-O Requirement VI4 states 'agents can be activities' but BFO enforces strict continuant/occurrent disjointness"
    implications: "Authors chose to VIOLATE PROV-O requirement in favor of BFO metaphysics; no example actually uses agent-as-activity"
    source: "Chunk 1:694-731"

  - gap_type: "Definition Mismatch"
    description: "PROV-O defines Influence as 'capacity' but authors reinterpret as event/process"
    implications: "Radical reinterpretation - dispositions are continuants but influences mapped to occurrents"
    source: "Chunk 1:923-971, Chunk 2:28-76"

  - gap_type: "Data Property Incompleteness"
    description: "Data property mappings could not be encoded in computable format due to OWL/RDF/SWRL limits"
    implications: "startedAtTime, endedAtTime, atTime require complex multi-entity chains not expressible in OWL"
    source: "Chunk 2:188-218"

  - gap_type: "Non-Total Reverse Mapping"
    description: "Total alignment PROV->BFO achieved, but NOT BFO->PROV (BFO has domains not in PROV like spatial/temporal regions)"
    implications: "Interoperability is asymmetric; not all BFO data can be represented in PROV"
    source: "Chunk 1:358-366"

  - gap_type: "CCO Agent Hierarchy Divergence"
    description: "CCO Person is NOT subclass of CCO Agent, unlike PROV where Person IS subclass of Agent"
    implications: "Requires intersection mappings; not all CCO Persons are agents (only those that participated in activities)"
    source: "Chunk 1:770-796"

  - gap_type: "Qualified Property Mapping Limitations"
    description: "Some qualified properties (qualifiedGeneration, qualifiedInvalidation) couldn't be mapped with subsumption - range is process boundary but similar CCO properties have range process"
    implications: "Had to use SKOS relatedMatch as 'last resort' - weaker than desired formal mapping"
    source: "Chunk 2:170-181"

empirical_grounding:
  - type: "Canonical Example Validation"
    domain: "W3C PROV-O documentation examples"
    scale: "312 individuals (named and blank node instances)"
    findings: "4 inconsistencies discovered - 2 inconsistent with PROV-O alone (mistakes in W3C docs), 2 inconsistent with alignment (also mistakes)"
    source: "Chunk 1:425-436, Chunk 2:229-257"

  - type: "Automated Pipeline Testing"
    domain: "Ontology engineering"
    scale: "Continuous integration via GitHub Actions"
    findings: "SPARQL queries verify totality; HermiT verifies coherence/consistency; ROBOT diff verifies conservativity"
    source: "Chunk 1:461-474"

  - type: "Cross-Ontology Validation"
    domain: "Sensor networks (SOSA/SSN)"
    scale: "W3C SOSA documentation examples"
    findings: "No inconsistencies when combining PROV-BFO alignment with PROV-SOSA alignment"
    source: "Chunk 1:439-445"

# Discovery Notes - SURPRISES and OBSERVATIONS

surprises:
  - "Authors deliberately VIOLATE an explicit PROV-O design requirement (VI4: agents can be activities) - this is unusual for an alignment paper"
  - "Influence redefined from 'capacity' to 'event' - this is not a mapping but a conceptual reinterpretation"
  - "Data property mapping is fundamentally blocked by OWL expressivity limits - temporal data requires multi-hop chain that can't be axiomatized"
  - "Alignment FOUND BUGS in W3C specification examples - the enriched semantics catch errors invisible to single ontology"
  - "Software agents mapped as MATERIAL entities (the hardware) - counterintuitive but follows from BFO's physicalism"

cross_paper_connections:
  - "BFO function/role distinction connects to UFO's distinction between intrinsic and relational moments"
  - "Qualification Pattern (reification) relates to UFO's Relator concept for first-class relationships"
  - "Process boundary concept relates to OCEL's event model - instantaneous vs extended"
  - "Conservative extension principle relates to modular ontology design patterns"

synthesis_opportunities:
  - "The SWRL conditional mapping technique could be generalized for other alignment scenarios with polymorphic domain/range"
  - "The 'interpretability enhances interoperability' principle could guide AI agent interoperability design"
  - "Approximate deductive difference is a practical tool for ontology evolution management"
  - "Alignment-as-bug-finder: using richer ontologies to validate data against less expressive schemas"

methodology_notes:
  - "Semi-automated curation combining conceptual analysis with SPARQL/reasoner tooling"
  - "SSSOM vocabulary for mapping metadata enables tracking provenance of mapping decisions"
  - "Separate files for BFO/CCO/RO alignments allows modular adoption"
  - "GitHub Actions CI pipeline for continuous validation of alignment properties"
---

# Paper Analysis: PROV-O to BFO Semantic Mapping

## Overview

This paper presents a comprehensive methodology and implementation for mapping the W3C Provenance Ontology (PROV-O) to Basic Formal Ontology (BFO) and its extensions (CCO, RO). The work achieves a **total alignment** of all 153 PROV-O classes and object properties using formal semantic mappings.

## Key Contributions

### 1. Formal Alignment Methodology

The paper defines four progressive criteria for ontology alignment quality:

1. **Coherence**: All formulae in aligned ontologies are satisfiable
2. **Consistency**: No entailed contradictions
3. **Conservativity**: Alignment doesn't change internal relationships within either ontology
4. **Totality/Interpretability/Synonymy**: Increasing degrees of semantic coverage

The theoretical goal is **synonymy** - bidirectional interpretation where each ontology entails the other.

### 2. Critical Mapping Decisions

**PROV Activity = BFO process** (equivalence)
- Both represent temporally extended occurrents
- Excludes temporal regions (like "the year 1986")

**PROV Entity subclass of BFO continuant** (subsumption)
- Complex union: (independent continuant NOT spatial region) OR generically/specifically dependent continuant
- Accounts for physical, digital, and conceptual entities

**PROV Agent subclass of BFO material entity** (subsumption)
- Must participate in some activity
- Must bear role realized in activity
- Even software agents are material (the hardware running code)

### 3. Radical Reinterpretation of Influence

The paper **deliberately diverges** from PROV-O's definition of Influence as "capacity":

> Original: "Influence is the capacity of an entity, activity, or agent to have an effect..."

> Reinterpretation: Influences are events (BFO processes or process boundaries), not capacities (BFO dispositions)

This is justified by observing that canonical examples show influences as temporal events, not as inherent capacities.

### 4. Design Requirement Violation

The paper explicitly chooses to violate PROV-O Requirement VI4 ("agents can be activities"):

> "We decided not to include it, as this would ultimately go against the spirit of BFO's core axiom that continuants and occurrents are disjoint."

This represents a principled decision to favor BFO's metaphysical consistency over PROV-O's permissiveness.

## Technical Implementation

### Mapping Mechanisms

- **owl:equivalentClass/Property**: 11 equivalence mappings
- **rdfs:subClassOf/subPropertyOf**: 73 subsumption mappings
- **SWRL rules**: 14 rules for conditional mappings
- **OWL property chains**: 1 complex property mapping
- **SKOS relatedMatch**: 4 informal associations (fallback)

### SWRL for Polymorphic Mapping

Novel use of SWRL to handle PROV `atLocation`:
- If subject is Activity -> map to BFO `occurs in`
- If subject is Entity -> map to BFO `located in`

```
prov:atLocation(?x,?y) ^ prov:Activity(?x) -> obo:BFO_0000066(?x,?y)
```

### Validation Pipeline

- **HermiT reasoner**: Consistency/coherence checking
- **SPARQL queries**: Totality verification, conservativity checking
- **GitHub Actions**: Continuous integration
- **312 test instances**: From W3C documentation

## Discoveries from Alignment

The enriched semantics revealed **4 bugs** in W3C PROV-O documentation:
1. Activity mistakenly used with `wasAttributedTo` (Entity domain)
2. Entity mistakenly used with `wasAssociatedWith` (Activity domain)
3. Entity tagged as EntityInfluence (occurrent vs continuant clash)
4. Activity tagged with `atTime` instead of `startedAtTime`

## Gaps Identified

1. **Data properties**: Cannot be formally mapped due to OWL expressivity limits
2. **Reverse totality**: BFO->PROV mapping is not total (BFO covers more domains)
3. **Some qualified properties**: Had to fall back to SKOS due to domain/range incompatibility

## Implications for AI Agent Ontologies

1. **Agent as material entity**: Software/AI agents are their physical substrates
2. **Role-based agency**: Agency defined by participation and role-bearing, not intrinsic
3. **Influence as event**: Actions have temporal extent, not just dispositional capacity
4. **Strict type discipline**: Entity/Activity/Agent cannot overlap (unlike loose PROV-O)

## Quality Assessment

**Strong Discovery Signals**:
- Multiple surprising findings (requirement violation, influence reinterpretation)
- Clear identification of gaps and tensions
- Empirical validation with real inconsistencies found
- Novel SWRL technique for polymorphic mapping

**Paper demonstrates**:
- High rigor in formal semantics
- Practical tooling for validation
- Honest acknowledgment of limitations
- Principled design decisions with clear rationale
