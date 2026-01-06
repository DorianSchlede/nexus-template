---
paper_id: "23-UFO_Story_Ontological_Foundations"
title: "Towards ontological foundations for conceptual modeling: The unified foundational ontology (UFO) story"
authors:
  - "Giancarlo Guizzardi"
  - "Gerd Wagner"
  - "Joao Paulo Andrade Almeida"
  - "Renata S.S. Guizzardi"
year: 2015
chunks_expected: 1
chunks_read: 1
analysis_complete: true
schema_version: "2.3"

chunk_index:
  1:
    token_count: 14731
    fields_found:
      entity_types: true
      entity_definitions: true
      entity_relationships: true
      entity_count: partial
      abstraction_level: true
      framework_comparison: true
      methodology: true
      ai_integration: false
      agent_modeling: partial
      agentic_workflows: false
      generative_ai_patterns: false
      agent_ontology_integration: false
      empirical_evidence: true
      limitations: partial
      tools_standards: true

entity_types:
  - item: "Endurant"
    chunk: 1
    lines: "173-181"
    quote: "UFO-A: An Ontology of Endurants dealing with aspects of structural conceptual modeling. It is organized as a Four-Category ontology comprising theories of Types and Taxonomic Structures"
  - item: "Perdurant (Events, Processes)"
    chunk: 1
    lines: "183-185"
    quote: "UFO-B: An Ontology of Perdurants (Events, Processes) dealing with aspects such as Perdurant Mereology, Temporal Ordering of Perdurants, Object Participation in Perdurants, Causation, Change"
  - item: "Intentional and Social Entities"
    chunk: 1
    lines: "191-193"
    quote: "UFO-C: An Ontology of Intentional and Social Entities, which is constructed on top of UFO-A and UFO-B, and which addresses notions such as Beliefs, Desires, Intentions, Goals, Actions, Commitments and Claims, Social Roles and Social Particularized Relational Complexes (Social Relators)"
  - item: "Substance Sortals (Kinds)"
    chunk: 1
    lines: "366-368"
    quote: "These include distinctions between substance sortals (kinds), phased-sortals (roles and phases) and non-sortals (categories, mixins and role mixins)."
  - item: "Phased-Sortals (Roles, Phases)"
    chunk: 1
    lines: "366-368"
    quote: "These include distinctions between substance sortals (kinds), phased-sortals (roles and phases) and non-sortals (categories, mixins and role mixins)."
  - item: "Non-Sortals (Categories, Mixins, Role Mixins)"
    chunk: 1
    lines: "366-368"
    quote: "These include distinctions between substance sortals (kinds), phased-sortals (roles and phases) and non-sortals (categories, mixins and role mixins)."
  - item: "Modes and Relators"
    chunk: 1
    lines: "369-370"
    quote: "these 'subversions' called our attention to the fact that, like full-fledged endurants, modes and relators also have their identity supplied by substance sortals (i.e., mode kinds and relator kinds)"
  - item: "Accidents (Particularized Properties, Moments, Qualities, Modes, Tropes)"
    chunk: 1
    lines: "127-129"
    quote: "we needed a theory that would include not only substantial individuals and universals but also accidents (particularized properties, moments, qualities, modes, tropes, abstract particulars, aspects, ways) and accident universals"
  - item: "Powertypes"
    chunk: 1
    lines: "382-385"
    quote: "Powertypes can be loosely defined as 'types whose instances are other types' (e.g., the type Organization Position, which can be instantiated by the types Director, Manager and Secretary, or the type Bird Species, which can be instantiated by the types Golden Eagle and Emperor Penguin)"
  - item: "Disposition"
    chunk: 1
    lines: "184-185"
    quote: "the connection between Perdurants and Endurants via Dispositions"

entity_definitions:
  Four-Category Ontology:
    chunk: 1
    lines: "129"
    quote: "we needed a Four-Category Ontology"
    definition: "An ontological theory that countenances both individuals and universals, including substantial individuals/universals and accidents/accident universals"
  Endurant:
    chunk: 1
    lines: "173-181"
    definition: "Entities that persist through time while maintaining identity; addressed by UFO-A including Types, Taxonomic Structures, Part-Whole Relations, Particularized Properties, Attributes, Relations, and Roles"
  Perdurant:
    chunk: 1
    lines: "183-185"
    definition: "Entities that unfold over time (events, processes); addressed by UFO-B including aspects of mereology, temporal ordering, object participation, causation, and change"
  Substance Sortal:
    chunk: 1
    lines: "366-369"
    definition: "Also called 'kinds'; types that supply identity to their instances (e.g., mode kinds, relator kinds)"
  Particularized Relational Property:
    chunk: 1
    lines: "132-136"
    quote: "particularized relations (relationships) and particularized intrinsic properties (e.g., often represented by the so-called weak entities) are frequently modeled as bearers of other particularized properties"
  Disposition:
    chunk: 1
    lines: "184-185"
    definition: "The ontological mechanism connecting endurants to perdurants in UFO-B"
  Powertype:
    chunk: 1
    lines: "382-387"
    definition: "Types whose instances are other types; not higher-order universals but resemblance structures that are themselves endurants"

entity_relationships:
  - item: "UFO-C builds on UFO-A and UFO-B"
    chunk: 1
    lines: "191"
    quote: "UFO-C: An Ontology of Intentional and Social Entities, which is constructed on top of UFO-A and UFO-B"
  - item: "Dispositions connect Endurants to Perdurants"
    chunk: 1
    lines: "184-185"
    quote: "the connection between Perdurants and Endurants via Dispositions"
  - item: "Relator-Material Relation Pattern"
    chunk: 1
    lines: "264"
    quote: "the relator-material relation pattern (Guizzardi and Wagner, 2008)"
  - item: "Part-Whole Relations with Transitivity Scoping"
    chunk: 1
    lines: "266-267"
    quote: "the editor also implements a number of topological patterns that allows for isolating the scope of transitivity of part-whole relations"
  - item: "Types instantiate Powertypes"
    chunk: 1
    lines: "382-385"
    quote: "Powertypes can be loosely defined as 'types whose instances are other types'"
  - item: "Object participates_in Perdurant"
    chunk: 1
    lines: "183-185"
    quote: "Object Participation in Perdurants"
  - item: "Kind classifies Object"
    chunk: 1
    lines: "366-369"
    quote: "like full-fledged endurants, modes and relators also have their identity supplied by substance sortals (i.e., mode kinds and relator kinds)"

abstraction_level: "Foundational ontology - UFO is designed as a comprehensive foundational ontology for conceptual modeling, organized into three strata (UFO-A, UFO-B, UFO-C) addressing different aspects of reality. It provides theoretical grounding for domain and application ontologies rather than domain-specific content."

framework_comparison:
  - item: "UFO vs BWW (Bunge-Wand-Weber)"
    chunk: 1
    lines: "105-125"
    quote: "the predictions made by the BWW approach found themselves in strong contrast with the intuitions and practical knowledge of modelers... the BWW dictum that 'mutual properties (or relations) should never be modeled as classes' was in conflict with modeling predictions made by other foundational theories"
  - item: "UFO vs DOLCE"
    chunk: 1
    lines: "138-162"
    quote: "DOLCE does not include universal as a category (DOLCE was designed as an ontology of particulars)... DOLCE still does not include a theory of particularized relational properties (relational qualities)"
  - item: "UFO vs GFO (General Formalized Ontology)"
    chunk: 1
    lines: "156-159"
    quote: "GFO's theory of universals still does not recognize these notions and... the GFO theory of relations is subject to the so-called Bradley Regress and, hence, it can only be instantiated by infinite (logical) models"
  - item: "UFO applied to analyze TOGAF, ArchiMate, RM-ODP, TROPOS, AORML, ARIS, BPMN"
    chunk: 1
    lines: "196-198"
    quote: "UFO has been employed as a basis for analyzing, reengineering and integrating many modeling languages and standards in different domains (e.g., UML, TOGAF, ArchiMate, RM-ODP, TROPOS/i*, AORML, ARIS, BPMN)"
  - item: "OntoUML vs UML"
    chunk: 1
    lines: "213-221"
    quote: "OntoUML was conceived as an ontologically well-founded version of the UML 2.0 fragment of class diagrams... we have managed to build a modeling language with explicitly defined formal and real-world semantics"
  - item: "OntoUML influenced ORM 2.0"
    chunk: 1
    lines: "225-226"
    quote: "some of the foundational theories underlying OntoUML have also been adopted by other conceptual modeling languages, e.g., ORM 2.0"

methodology: "Top-down theoretical approach grounded in formal ontology, cognitive science, linguistics, and philosophical logics. UFO was developed by 'consistently putting together a number of theories originating from areas such as Formal Ontology in philosophy, cognitive science, linguistics and philosophical logics' (lines 168-169). The approach advocates for descriptive metaphysics rather than revisionary ontology, taking 'both human cognition and human linguistic competence seriously' (lines 117-118)."

ai_integration: []

agent_modeling:
  - item: "Intentional entities in UFO-C"
    chunk: 1
    lines: "191-193"
    quote: "UFO-C: An Ontology of Intentional and Social Entities... addresses notions such as Beliefs, Desires, Intentions, Goals, Actions, Commitments and Claims, Social Roles"
  - item: "Agent-Based Simulation foundations"
    chunk: 1
    lines: "552-553"
    quote: "Towards and ontological foundation of agent-based simulation"

agentic_workflows: []

generative_ai_patterns: []

agent_ontology_integration: []

entity_count: null

empirical_evidence:
  - item: "OntoUML Model Repository"
    chunk: 1
    lines: "318-322"
    quote: "we have managed to assemble a model repository containing OntoUML models in different domains (e.g., telecommunications, government, biodiversity, bioinformatics), different sizes (e.g., ranging from dozens of concepts to thousand of concepts), and produced in different types of contexts"
  - item: "Anti-Pattern Validation Study"
    chunk: 1
    lines: "334-337"
    quote: "Sales and Guizzardi (2015) have presented a validation study developed with a large industrial model and managed to empirically demonstrate, for the vast majority of the identified anti-patterns, a very high correlation between the presence of these anti-patterns and the adoption of our proposed solutions"
  - item: "Systematic Language Subversions"
    chunk: 1
    lines: "343-352"
    quote: "we have managed to observe a number of different ways in which people would slightly subvert the syntax of the language, ultimately creating what we could call 'systematic subversions' of the language"
  - item: "U.S. Department of Defense adoption"
    chunk: 1
    lines: "224-225"
    quote: "it has been considered as a candidate for addressing the OMG SIMF (Semantic Information Model Federation) Request for Proposal, after a report of its successful use over the years by a branch of the U.S. Department of Defense (2011)"

limitations:
  - item: "Complexity management challenges"
    chunk: 1
    lines: "361-364"
    quote: "given that the introduction of this new perspective substantially increases the complexity of the resulting diagrams, new complexity management theories and tools for OntoUML diagrams need to be developed (e.g., dealing with model filtering, modularization, viewpoint selection)"
  - item: "Original OntoUML limited to structural (endurant) modeling"
    chunk: 1
    lines: "353-357"
    quote: "the language was created to represent structural conceptual models expressing endurantistic aspects of reality. However, systematically, a number of authors... started to produce OntoUML models in which perdurants (and perdurant relations) would appear as modeling primitives"

tools_standards:
  - item: "OntoUML (UML Profile)"
    chunk: 1
    lines: "243-246"
    quote: "The decision to build the language as a version of UML (technically, as a UML profile) was mainly motivated by the fact that UML... has a standardized and explicitly defined metamodel"
  - item: "Enterprise Architect Plugin"
    chunk: 1
    lines: "246-247"
    quote: "an OntoUML plug-in has been implemented for the professional tool Enterprise Architect"
  - item: "OWL Mappings"
    chunk: 1
    lines: "313-315"
    quote: "we have implemented six different automatic mappings from OntoUML to OWL contemplating different transformation styles that were designed to address different sets of non-functional requirements"
  - item: "SBVR (Semantics for Business Vocabularies and Rules)"
    chunk: 1
    lines: "275-276"
    quote: "generating model verbalization in structured English following a slightly modified version of the SBVR (Semantics for Business Vocabularies and Rules) OMG proposal"
  - item: "OCL and Temporal OCL"
    chunk: 1
    lines: "288-290"
    quote: "the current editor supports the specification of OCL and temporal OCL formal constraints... The editor provides support for syntax highlighting, code-completion and syntax verification"
  - item: "Alloy (formal verification)"
    chunk: 1
    lines: "442-443"
    quote: "Transforming OntoUML into alloy: Towards conceptual model validation using a lightweight formal method"
  - item: "XML, Smalltalk, Modal Prolog mappings"
    chunk: 1
    lines: "316-317"
    quote: "other authors have implemented alternative mappings from OntoUML to languages such as XML, Smalltalk, OWL and a version of a Modal Prolog"
---

# Paper Analysis: UFO Story - Ontological Foundations

## Summary

This position paper describes the long-term research program behind the Unified Foundational Ontology (UFO) and its primary application, the OntoUML conceptual modeling language. UFO was developed to provide rigorous ontological foundations for conceptual modeling, addressing limitations in prior approaches like the BWW (Bunge-Wand-Weber) ontology.

## Key Contributions

### 1. Three-Stratum Architecture of UFO

UFO is organized into three complementary layers:

- **UFO-A (Endurants)**: Structural conceptual modeling including types, taxonomic structures, part-whole relations, particularized properties, attributes, relations, and roles
- **UFO-B (Perdurants)**: Events and processes including mereology, temporal ordering, object participation, causation, and change
- **UFO-C (Intentional/Social Entities)**: Built on UFO-A and UFO-B; covers beliefs, desires, intentions, goals, actions, commitments, claims, social roles, and social relators

### 2. Four-Category Ontology

UFO is grounded in a Four-Category Ontology that distinguishes:
- Individuals vs. Universals
- Substantial entities vs. Accidents (particularized properties)

This structure enables representation of concepts that other foundational ontologies (BWW, DOLCE, GFO) could not adequately handle.

### 3. OntoUML Tooling Ecosystem

The paper documents comprehensive tooling support:
- Pattern-based model construction
- Model verbalization (SBVR-based)
- Formal constraint specification (OCL, temporal OCL)
- Model validation via visual simulation
- Ontology codification (6 OWL mappings)
- Anti-pattern detection and rectification

### 4. Empirical Grounding

The research is empirically grounded through:
- A model repository with OntoUML models across multiple domains
- Validation studies on anti-patterns with industrial models
- Observation of "systematic language subversions" that drove theory evolution
- Adoption by U.S. Department of Defense and consideration for OMG SIMF

## Relevance to Research Questions

### Entity Types and Definitions
UFO provides rich entity type distinctions: substance sortals (kinds), phased-sortals (roles, phases), non-sortals (categories, mixins, role mixins), modes, relators, qualities, and powertypes.

### Framework Comparison
Extensive comparison with BWW, DOLCE, GFO, and application to analyze UML, TOGAF, ArchiMate, BPMN, and other standards.

### Agent Modeling
UFO-C addresses intentional entities (beliefs, desires, intentions, goals) and social entities (commitments, claims, social roles), providing foundations for agent modeling.

### AI/LLM Integration
This 2015 paper predates modern AI/LLM integration patterns; no content on generative AI, agentic workflows, or AI-ontology integration.

## Notable Quotes

> "the opposite of ontology is not non-ontology, but bad ontology" (Collier, 1994)

> "any representation system that has some real-world semantics (as opposed to mere formal semantics) makes an ontological commitment"

> "we needed a Four-Category Ontology" - distinguishing individuals/universals and substantials/accidents
