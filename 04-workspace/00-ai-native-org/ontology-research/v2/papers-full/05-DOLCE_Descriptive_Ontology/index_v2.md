---
paper_id: "05-DOLCE_Descriptive_Ontology"
title: "DOLCE: A Descriptive Ontology for Linguistic and Cognitive Engineering"
authors: ["Stefano Borgo", "Roberta Ferrario", "Aldo Gangemi", "Nicola Guarino", "Claudio Masolo", "Daniele Porello", "Emilio M. Sanfilippo", "Laure Vieu"]
publication: "Applied Ontology"
year: 2023  # Based on 20-year anniversary framing from 2003
extraction_version: "v2"
extraction_date: "2025-12-31"
extractor: "Claude Opus 4.5"

ontological_primitives:
  - term: "Endurant"
    definition: "An entity wholly present (i.e., with all their parts) at any time in which they are present"
    source: "Chunk 1:128-133"
    unique_aspects: "Contrasts with perdurants - can acquire and lose properties/parts through time while remaining wholly present. Called 'object' in DOLCE-CORE."

  - term: "Perdurant"
    definition: "Entities that can be partially present, so that at any time in which they unfold only a part of them is present"
    source: "Chunk 1:128-133"
    unique_aspects: "Fixed in time - cannot change. Called 'event' in DOLCE-CORE. Distinguished by having time as main dimension."

  - term: "Quality"
    definition: "What can be perceived and measured; particulars inhering in endurants or perdurants"
    source: "Chunk 1:166-176"
    unique_aspects: "Individual qualities specific to their bearers (individual qualities). Can have qualities themselves (complex qualities)."

  - term: "Quale"
    definition: "The position occupied by an individual quality within a quality space"
    source: "Chunk 1:178-181"
    unique_aspects: "Enables comparison of qualities - two qualities are distinct but can have the same quale (same position in quality space)."

  - term: "Abstract"
    definition: "Entities that have neither spatial nor temporal qualities and are not qualities themselves"
    source: "Chunk 1:216-219"
    unique_aspects: "Examples include quality regions, quality spaces, sets, and facts."

  - term: "Concept"
    definition: "Particulars that classify entities, introduced as a category under Non-Agentive Social Object"
    source: "Chunk 1:236-237, 405-406"
    unique_aspects: "Reified as particulars rather than universals - allows concepts to be domain entities."

  - term: "Role"
    definition: "Concepts that are anti-rigid and founded - properties that can be temporarily acquired/lost and depend on external entities/contexts"
    source: "Chunk 1:184-189, 428-430"
    unique_aspects: "Dynamic properties with relational nature. Distinguished from essential properties."

structural_patterns:
  - pattern_name: "Participation Triad"
    structure: "Endurant participates-in Perdurant at Time"
    instances:
      - "Person participates-in conference talk (Chunk 1:136-137)"
      - "Person participates-in their own life (Chunk 1:136)"
      - "Constant participation (PCC) - participation during whole perdurant (Chunk 1:369-370)"
    source: "Chunk 1:134-137, 365-380"

  - pattern_name: "Quality-Quale-Space Triad"
    structure: "Individual Quality has Quale in Quality Space"
    instances:
      - "Rose's red color quality has position in color space (Chunk 1:169-181)"
      - "Flower color changing from red region to brown region in color space (Chunk 1:915-928)"
      - "Speed quality changing position in speed space (Chunk 2:130-165)"
    source: "Chunk 1:166-181, Chunk 2:130-165"

  - pattern_name: "Constitution vs Composition Distinction"
    structure: "Constitution (intercategorical) vs Parthood (intracategorical)"
    instances:
      - "Wood constitutes table (matter->artifact)"
      - "Legs are parts of table (artifact->artifact)"
      - "Statue constituted by matter but distinct from it"
    source: "Chunk 1:206-214, 486-497"

  - pattern_name: "Classification Pattern"
    structure: "Entity classified-by Concept at Time"
    instances:
      - "Person classified by Teacher role at time"
      - "Relationship classified by Marriage concept"
      - "Perdurant classified by Plan concept"
    source: "Chunk 1:405-430, Chunk 2:360-410"

  - pattern_name: "Anti-rigid Type Pattern"
    structure: "Role/Phase that can be acquired and lost without identity change"
    instances:
      - "Teacher role (Chunk 1:720-748)"
      - "Student role (Chunk 1:742-748)"
      - "Legal marriage concepts evolving (Chunk 2:360-410)"
    source: "Chunk 1:187-189, 720-748"

  - pattern_name: "Stative/Eventive Distinction"
    structure: "Perdurants divided by cumulativity property"
    instances:
      - "Stative: cumulative (sum of two sittings is still sitting)"
      - "Process: cumulative but not homeomeric (Chunk 1:160-161)"
      - "Events: non-cumulative (achievements if atomic, accomplishments if not)"
    source: "Chunk 1:156-163"

novel_concepts:
  - concept: "Quality Space"
    definition: "A space in which individual qualities are positioned, based on Gardenfors' conceptual spaces"
    novelty_claim: "Enables comparison of qualities by their position rather than direct comparison - two distinct quality instances can occupy same position"
    source: "Chunk 1:178-181, 197-198"

  - concept: "Functional Role"
    definition: "A role that can classify only one entity at each time"
    novelty_claim: "Distinguishes roles with individual rights/duties (teacher) from collective roles (student)"
    source: "Chunk 1:774-793"

  - concept: "Temporary Parthood"
    definition: "Time-indexed parthood relation for endurants that drops antisymmetry"
    novelty_claim: "Enables modeling parts changing over time while entity persists (table with replaced leg)"
    source: "Chunk 1:253-299, 475-497"

  - concept: "Concept Evolution/Drift"
    definition: "Concepts can persist through time while partially changing in their characterization"
    novelty_claim: "Allows modeling how social/legal concepts evolve while preserving identity (marriage concept)"
    source: "Chunk 2:323-410"

  - concept: "Descriptive Metaphysics"
    definition: "Making explicit already existing conceptualizations influenced by natural language, cognition, and social practices"
    novelty_claim: "Contrasts with referentialist metaphysics - categories situated at mesoscopic level and may change"
    source: "Chunk 1:39-43"

  - concept: "ExecutesPlan Relation"
    definition: "Connects a perdurant to a plan, stating that event complies with plan requirements"
    novelty_claim: "Enables modeling partial plan execution - event can execute plan without completing it"
    source: "Chunk 2:207-212"

semantic_commitments:
  - commitment: "Endurantism vs Perdurantism"
    position: "Multiplicative - both endurants (wholly present) and perdurants (temporally extended) coexist"
    implications: "Objects and events are distinct categories with different temporal behavior"
    source: "Chunk 1:128-137"

  - commitment: "Particulars vs Universals"
    position: "Domain of discourse formed by particulars; properties and relations are universals"
    implications: "Concepts/roles reified as particulars to bring them into domain discourse"
    source: "Chunk 1:42-43, Chunk 1:77-78"

  - commitment: "Possibilism"
    position: "Domain of quantification contains all possible entities, regardless of actual existence"
    implications: "Uses modal logic QS5 with Barcan formulas - things can exist without being present"
    source: "Chunk 1:227-230"

  - commitment: "Descriptive vs Prescriptive Ontology"
    position: "Descriptive - captures commonsense view influenced by cognition and language"
    implications: "Categories may change as scientific knowledge or social consensus evolves"
    source: "Chunk 1:39-43"

  - commitment: "Quality Individuation"
    position: "Qualities are particular, bearer-specific instances (this redness, not redness in general)"
    implications: "Comparison requires quality spaces - same quale in space = same qualitative value"
    source: "Chunk 1:168-181"

boundary_definitions:
  - entity_type: "Endurant"
    identity_criteria: "Essential properties (what makes it that kind of thing) vs accidental properties (can change)"
    boundary_cases: "Table: is being-a-table essential or accidental? DOLCE allows both artifact-based and role-based modeling"
    source: "Chunk 1:453-472, 468-472"

  - entity_type: "Artifact"
    identity_criteria: "Intentionally produced products with persistence based on suitable shape and right functionalities"
    boundary_cases: "Table persists if tabletop not substituted - legs can be replaced without identity change"
    source: "Chunk 1:475-485"

  - entity_type: "Constitution vs Identity"
    identity_criteria: "Constituted entities distinguishable by histories, persistence conditions, or relational properties"
    boundary_cases: "Statue and clay: statue started later, requires sculptor, can be destroyed while clay survives"
    source: "Chunk 1:208-214"

  - entity_type: "Perdurant Classification"
    identity_criteria: "Cumulativity (stative/eventive) and homeomericity (process distinction)"
    boundary_cases: "Sum of two sittings = sitting (stative), but sum of two runnings may not be running"
    source: "Chunk 1:156-163"

  - entity_type: "Concept"
    identity_criteria: "Debated - can concepts change while preserving identity?"
    boundary_cases: "Marriage concept: same concept persists while legal characterization changes from lm to lm'"
    source: "Chunk 2:332-346"

temporal_modeling:
  - aspect: "Presence vs Existence"
    approach: "PRE(x,t) - being present at time, derived from having temporal quale"
    mechanism: "Things exist if they have temporal quale - present when that quale includes time t"
    source: "Chunk 1:352-359"

  - aspect: "Temporal Parthood"
    approach: "Time-indexed relation P(x,y,t) for endurants"
    mechanism: "Both part and whole must be present for parthood to hold; drops antisymmetry"
    source: "Chunk 1:274-291"

  - aspect: "Temporal Quale of Perdurants"
    approach: "Quale associated with time location quality (TL)"
    mechanism: "ql_T,PD(t,x) = PD(x) AND exists z (qt(TL,z,x) AND ql(t,z))"
    source: "Chunk 1:320-322"

  - aspect: "Temporal Quale of Endurants"
    approach: "Sum of all times during which endurant participates in some perdurant"
    mechanism: "ql_T,ED(t,x) = ED(x) AND t = sigma_t'(exists y(PC(x,y,t')))"
    source: "Chunk 1:323-325"

  - aspect: "Process Phases"
    approach: "Events divided into temporally ordered subevents"
    mechanism: "Walk + SpeedUp + Run as sum of perdurants with temporal ordering"
    source: "Chunk 2:55-62, 145-150"

  - aspect: "Quality Change Over Time"
    approach: "Same quality instance, different quale positions at different times"
    mechanism: "Flower color quality q has quale l in red region at t0, l' in brown region at t1"
    source: "Chunk 1:915-928"

agency_spectrum:
  - agent_type: "Agentive Physical Object (APO)"
    capabilities: "Implicit in taxonomy - category for persons and entities with agency"
    constraints: "Not extensively characterized in this paper"
    source: "Chunk 1:751, 961"

  - agent_type: "Non-Agentive Physical Object (NAPO)"
    capabilities: "Physical objects without agency (artifacts, natural objects)"
    constraints: "Cannot be classified under agentive categories"
    source: "Chunk 1:125 (Figure 1)"

  - agent_type: "Collective/Organizational Agency"
    capabilities: "Mentioned as extension (organizations, groups)"
    constraints: "Not modeled in core DOLCE - requires Porello et al. 2014 extensions"
    source: "Chunk 1:780-783"

  - agent_type: "Plan Executor"
    capabilities: "Entities that execute plans - plans classify perdurants"
    constraints: "Plans as concepts that perdurants comply with"
    source: "Chunk 2:196-212"

knowledge_representation:
  - mechanism: "First-Order Modal Logic"
    formalism: "QS5 with Barcan and converse Barcan formulas"
    reasoning: "Possibilistic view - domain contains all possible entities"
    source: "Chunk 1:227-230"

  - mechanism: "OWL Approximations"
    formalism: "DOLCE-lite, DOLCE-ultralite, DOLCE-zero, DUL"
    reasoning: "Trade-off between expressiveness and computability - lite versions for applications"
    source: "Chunk 1:60-62, 68-70"

  - mechanism: "CLIF (Common Logic)"
    formalism: "ISO 24707 syntax for logical representation"
    reasoning: "Available for ISO 21838 standardization"
    source: "Chunk 1:109-111"

  - mechanism: "Description and Situations (D&S)"
    formalism: "Ontology design pattern framework extending DOLCE"
    reasoning: "Overcomes OWL expressivity limits, leverages OWL2 punning"
    source: "Chunk 2:427-433"

  - mechanism: "OntoClean Methodology"
    formalism: "Meta-properties analysis (rigidity, identity, dependence)"
    reasoning: "Quality evaluation of ontological choices"
    source: "Chunk 1:73-75"

emergence_indicators:
  - phenomenon: "Concept Drift"
    mechanism: "Social/legal concepts evolve through changing characterizations"
    evidence: "Marriage concept persists while legal requirements change"
    source: "Chunk 2:323-346"

  - phenomenon: "Multiplicative Ontology"
    mechanism: "Same spatiotemporal location can host multiple entities (statue and clay)"
    evidence: "Constitution relation enables this multiplicity"
    source: "Chunk 1:208-214, Chunk 2:573-574"

  - phenomenon: "Role Dynamics"
    mechanism: "Roles can be acquired/lost/transferred without identity change"
    evidence: "Teacher role passes from Potter to Bumblebee"
    source: "Chunk 1:720-748"

integration_surfaces:
  - surface: "Endurant/Perdurant Distinction"
    connects_to: ["BFO Continuant/Occurrent", "UFO Endurant/Perdurant"]
    alignment_quality: "High - shared terminology with BFO, explicit alignment discussions"
    source: "Chunk 1:121-122"

  - surface: "Quality Ontology"
    connects_to: ["Gardenfors Conceptual Spaces", "BFO Quality"]
    alignment_quality: "Novel - quality spaces based on Gardenfors, differs from BFO approach"
    source: "Chunk 1:197-198"

  - surface: "Role Theory"
    connects_to: ["UFO Role", "Enterprise Ontology Social Roles"]
    alignment_quality: "Good - shares anti-rigidity concept, differs in reification approach"
    source: "Chunk 1:184-189"

  - surface: "Semantic Web Standards"
    connects_to: ["DBpedia", "WordNet", "CIDOC CRM", "SSN", "SAREF"]
    alignment_quality: "Demonstrated - DUL used to improve these resources"
    source: "Chunk 2:456-465"

  - surface: "Process Ontology"
    connects_to: ["BPMN Plans", "Process Mining Events"]
    alignment_quality: "Partial - process/event/accomplishment distinctions map to BPM"
    source: "Chunk 1:156-163"

gaps_and_tensions:
  - gap_type: "Omission"
    description: "Function not formalized in core DOLCE - delegated to extensions"
    implications: "Artifact functionality requires Borgo et al. 2010, Mizoguchi et al. 2016 extensions"
    source: "Chunk 1:184-185"

  - gap_type: "Omission"
    description: "Organizational/collective agency not in core ontology"
    implications: "Modeling companies, groups as agents requires Porello et al. 2014 extensions"
    source: "Chunk 1:780-783"

  - gap_type: "Tension"
    description: "Whether concepts can change while preserving identity - disagreement exists"
    implications: "DOLCE allows both views - knowledge engineer must choose perspective"
    source: "Chunk 2:332-343"

  - gap_type: "Trade-off"
    description: "Modal logic expressiveness vs computability"
    implications: "Full DOLCE not computable - requires OWL approximations for applications"
    source: "Chunk 1:60-62"

  - gap_type: "Underspecified"
    description: "Agency/intentionality criteria for Agentive Physical Objects"
    implications: "Distinction between agentive and non-agentive not deeply characterized"
    source: "Chunk 1:751 (mentioned but not elaborated)"

  - gap_type: "Modeling Choice"
    description: "Artifact-based vs Role-based modeling - DOLCE neutral between them"
    implications: "Same scenario can be modeled differently depending on essential properties view"
    source: "Chunk 1:453-472"

empirical_grounding:
  - type: "Semantic Web Applications"
    domain: "Multiple"
    scale: "25+ large ontology projects cited"
    findings: "DUL reuse in e-learning, medicine, law, events, robotics, manufacturing, etc."
    source: "Chunk 2:450-455"

  - type: "DBpedia Improvement"
    domain: "Knowledge Graphs"
    scale: "Millions of inconsistencies identified"
    findings: "DOLCE used to identify and fix inconsistencies, discover anti-patterns"
    source: "Chunk 2:456-458"

  - type: "WordNet Reorganization"
    domain: "Lexical Resources"
    scale: "Princeton WordNet top level"
    findings: "Caused inclusion of individual/class distinction in lexicon"
    source: "Chunk 2:459-461"

  - type: "Standards Alignment"
    domain: "Domain Standards"
    scale: "CIDOC CRM, SSN, SAREF"
    findings: "Standard or de facto standards based on or compatible with DUL"
    source: "Chunk 2:462-465"

  - type: "Framester Knowledge Graph"
    domain: "Linguistic Databases"
    scale: "Massive - unifies many linguistic databases"
    findings: "Frame semantics mapped to ontologies under common DUL framework"
    source: "Chunk 2:461-462"

surprises_and_discoveries:
  - surprise: "Quality Space Architecture"
    description: "Qualities are particular instances (this-redness) not universals, compared via position in quality spaces"
    implication: "Fundamentally different from treating qualities as types/classes"

  - surprise: "Concepts as Particulars"
    description: "DOLCE reifies concepts as particular entities in the domain of discourse"
    implication: "Enables concepts themselves to participate in relations, be classified, change over time"

  - surprise: "Possibilistic Domain"
    description: "Domain of quantification includes all possible entities regardless of actual existence"
    implication: "Things can exist without being present - separation of existence and presence"

  - surprise: "Neutral on Essential Properties"
    description: "DOLCE does not prescribe whether being-a-table is essential or accidental"
    implication: "Same scenario can be validly modeled in incompatible ways - ontological pluralism"

  - surprise: "Constitution Not Identity"
    description: "Statue and clay can be co-located but are distinct entities with different persistence"
    implication: "Multiplicative ontology - challenges common assumption of unique occupancy"

  - surprise: "20-Year Stability"
    description: "Core DOLCE has remained stable since 2003 while enabling extensive extension"
    implication: "Demonstrates foundational ontologies can achieve both stability and extensibility"
---

# DOLCE: A Descriptive Ontology for Linguistic and Cognitive Engineering

## Summary

DOLCE (Descriptive Ontology for Linguistic and Cognitive Engineering) is a foundational ontology that adopts a **descriptive metaphysics** approach, aiming to make explicit existing conceptualizations influenced by natural language, human cognition, and social practices. Unlike referentialist approaches, DOLCE focuses on the "commonsense view of reality" at the mesoscopic level, acknowledging that categories may evolve with scientific knowledge and social consensus.

## Core Architecture

### Four Basic Categories

1. **Endurant** (Continuant): Entities wholly present at any time they exist - tables, persons, cats
2. **Perdurant** (Occurrent): Entities that unfold in time, only partially present at any moment - tennis matches, manufacturing processes
3. **Quality**: Perceivable/measurable particulars inhering in entities - the specific red of this rose
4. **Abstract**: Entities without spatial or temporal qualities - sets, facts, quality spaces

### Key Structural Innovation: Quality Spaces

DOLCE introduces a distinctive treatment of qualities where:
- Qualities are **particular instances** (individual qualities), not universals
- Comparison occurs via **qualia** - positions in **quality spaces** (based on Gardenfors' conceptual spaces)
- Two distinct quality instances can share the same quale (position) in a space

This enables modeling property change without identity change: a flower's color quality persists while its quale moves from the red region to the brown region of color space.

## Distinctive Features

### Participation as Fundamental Relation

Endurants and perdurants are connected through **participation**:
- An endurant IS in time by participating in perdurants
- A perdurant HAPPENS by having endurant participants
- "A person is in time by participating in her own life"

### Constitution vs Composition

DOLCE clearly distinguishes:
- **Constitution** (intercategorical): Dependence between entities with different essential properties (wood constitutes table)
- **Composition** (intracategorical): Parthood among entities of same category (tabletop is part of table)

This enables the "multiplicative ontology" where a statue and its clay can be co-located but distinct entities.

### Roles as Anti-Rigid Founded Concepts

Roles are characterized by:
- **Anti-rigidity**: Can be acquired and lost (Potter stops being teacher, Bumblebee starts)
- **Foundedness**: Defined through relation to other concepts/contexts (teacher role depends on school context)

### Concept Evolution

DOLCE allows (but doesn't require) concepts to persist through changes in characterization - enabling modeling of how the concept "marriage" persists while its legal requirements evolve.

## Formalization

DOLCE is axiomatized in first-order modal logic QS5 with a **possibilistic** view - the domain contains all possible entities regardless of actual existence. This requires distinguishing:
- **Existence**: Having a temporal quale (being in the domain)
- **Presence**: PRE(x,t) - being at a specific time

Practical implementations include OWL approximations (DOLCE-lite, DOLCE-ultralite, DUL) that trade expressiveness for computability.

## Critical Gaps

1. **Function**: Not formalized in core ontology - requires extensions
2. **Collective Agency**: Organizations/groups as agents require separate modules
3. **Agentive Criteria**: What makes something agentive is underspecified
4. **Computability**: Full modal logic version is not computable

## Integration and Impact

DOLCE has achieved remarkable stability (20 years) while enabling extensive application:
- Improved DBpedia (millions of inconsistencies fixed)
- Reorganized WordNet top-level
- Foundation for standards (CIDOC CRM, SSN, SAREF)
- 25+ major application domains

## Key Tensions for Synthesis

1. **Quality-as-particular vs Quality-as-universal**: DOLCE's approach differs from BFO
2. **Descriptive vs Prescriptive**: DOLCE embraces cognitive/linguistic grounding that may not align with scientific ontology
3. **Modeling Choice Neutrality**: Same scenario validly modeled in incompatible ways (artifact vs role approach)
4. **Modal Expressiveness vs Practical Use**: Full semantics requires approximation for applications
