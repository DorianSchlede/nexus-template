---
paper_id: "23-UFO_Story_Ontological_Foundations"
title: "Towards ontological foundations for conceptual modeling: The unified foundational ontology (UFO) story"
authors:
  - "Giancarlo Guizzardi"
  - "Gerd Wagner"
  - "Joao Paulo Andrade Almeida"
  - "Renata S.S. Guizzardi"
year: 2015
venue: "Applied Ontology"
extraction_version: "v2-discovery"
extracted_at: "2025-12-31"

# V2 DISCOVERY EXTRACTION (12 fields)

ontological_primitives:
  - term: "Endurant"
    definition: "Entities wholly present whenever they exist; the subject of UFO-A dealing with structural conceptual modeling aspects"
    source: "Chunk 1:173-177"
    unique_aspects: "Contrasts with perdurant; endurants are central to structural conceptual modeling"

  - term: "Perdurant"
    definition: "Events and processes; entities that unfold over time"
    source: "Chunk 1:183-185"
    unique_aspects: "UFO-B addresses perdurants including mereology, temporal ordering, participation, and causation"

  - term: "Moment (Accident/Trope)"
    definition: "Particularized properties - also called accidents, qualities, modes, tropes, abstract particulars, aspects, or 'ways'"
    source: "Chunk 1:128-129"
    unique_aspects: "Critical for making sense of language and cognition; enables modeling weak entities and reified relationships"

  - term: "Substance Sortal (Kind)"
    definition: "Type that supplies identity to its instances"
    source: "Chunk 1:366-367"
    unique_aspects: "Modes and relators also have identity supplied by substance sortals (mode kinds, relator kinds)"

  - term: "Phased-Sortal"
    definition: "Types that can be gained or lost without identity change - includes Roles and Phases"
    source: "Chunk 1:367"
    unique_aspects: "Anti-rigid types applicable to all endurant categories, not just objects"

  - term: "Non-Sortal"
    definition: "Categories, mixins, and role mixins - types without identity supply"
    source: "Chunk 1:367"
    unique_aspects: "Part of the taxonomy of universal distinctions"

  - term: "Relator"
    definition: "Particularized relational property that mediates entities; makes relationships first-class citizens"
    source: "Chunk 1:132-136, 180-181"
    unique_aspects: "Solves problems that cannot be addressed without considering particularized properties; avoids Bradley Regress"

  - term: "Powertype"
    definition: "Types whose instances are other types (e.g., Organization Position instantiated by Director, Manager)"
    source: "Chunk 1:383-387"
    unique_aspects: "Interpreted not as higher-order universals but as concrete resemblance structures that are themselves endurants"

  - term: "Disposition"
    definition: "Connection between perdurants and endurants; enables causal laws as foundation of transition rules"
    source: "Chunk 1:184-185"
    unique_aspects: "Links UFO-A (endurants) with UFO-B (events) via causation and change"

structural_patterns:
  - pattern_name: "Four-Category Ontology"
    structure: "Individuals + Universals crossed with Substances + Accidents"
    instances:
      - "Substantial individuals (objects)"
      - "Substantial universals (kinds)"
      - "Accident individuals (moments, tropes, modes)"
      - "Accident universals (quality types)"
    source: "Chunk 1:127-129, 147"
    notes: "Based on Aristotelian Square; shared commitment with DOLCE and GFO"

  - pattern_name: "Three-Strata Architecture"
    structure: "UFO-A (Endurants) -> UFO-B (Perdurants) -> UFO-C (Intentional/Social)"
    instances:
      - "UFO-A: structural modeling, types, part-whole, attributes, relations, roles"
      - "UFO-B: events, processes, participation, causation, change"
      - "UFO-C: beliefs, desires, intentions, goals, actions, commitments, social relators"
    source: "Chunk 1:170-193"
    notes: "Layered construction - UFO-C builds on both UFO-A and UFO-B"

  - pattern_name: "Relator-Material Relation Pattern"
    structure: "Relator mediates Material Relation between entities"
    instances:
      - "Marriage (relator) mediates married-to (material relation) between Persons"
      - "Employment (relator) mediates works-for between Person and Organization"
    source: "Chunk 1:264"
    notes: "One of the ontological patterns implemented in OntoUML"

  - pattern_name: "Role with Disjoint Allowed Types"
    structure: "Role type constrained to disjoint base types"
    instances:
      - "Modeling pattern for capturing role constraints"
    source: "Chunk 1:263-264"
    notes: "Ontological pattern reflecting UFO micro-theories"

  - pattern_name: "Qualities with Alternative Quality Spaces"
    structure: "Quality type with multiple possible measurement structures"
    instances:
      - "Color quality with RGB, HSV, CMYK quality spaces"
    source: "Chunk 1:265"
    notes: "Addresses datatypes as measure structures"

  - pattern_name: "Anti-Pattern / Pattern Rectification"
    structure: "Detect recurrent error structure -> Propose solution pattern"
    instances:
      - "Ontological anti-patterns catalogued empirically"
      - "Rectification solutions eliminate deviation between valid and intended instances"
    source: "Chunk 1:325-337"
    notes: "Empirically discovered through repository analysis; novel methodological contribution"

novel_concepts:
  - concept: "Systematic Language Subversions"
    definition: "Purposeful grammatically incorrect models that users create to express conceptualizations the language cannot otherwise represent"
    novelty_claim: "Uses language 'abuse' as empirical signal for needed language evolution"
    source: "Chunk 1:340-352"
    surprise_factor: "HIGH - treats syntax violations as valuable user feedback, not just errors"

  - concept: "Ontology-Based Language Engineering"
    definition: "Method for designing languages where the worldview embedded through primitives is isomorphic to a foundational ontology's distinctions"
    novelty_claim: "Systematic approach to creating languages with explicit formal AND real-world semantics"
    source: "Chunk 1:214-222"

  - concept: "Visual Simulation for Model Validation"
    definition: "Automatically generating visual instances (exemplars) of a conceptual model to confront modelers with what their model actually represents"
    novelty_claim: "Contrasts formally-valid instances with intended instances to detect over/underconstraining"
    source: "Chunk 1:291-301"

  - concept: "Descriptive Metaphysics vs Revisionary Ontology"
    definition: "Ontological foundations should account for human cognition and linguistic competence, not revise them"
    novelty_claim: "Explicit rejection of Bunge's philosophy-of-hard-science approach for conceptual modeling"
    source: "Chunk 1:116-121"
    surprise_factor: "Strongly positions UFO against BWW approach"

  - concept: "Powertypes as Endurants"
    definition: "Powertypes interpreted as concrete resemblance structures that are endurants, not higher-order universals"
    novelty_claim: "Novel interpretation of type-instance stratification"
    source: "Chunk 1:382-387"

semantic_commitments:
  - commitment: "Four-Category Ontology"
    position: "Reality includes both individuals and universals, both substances and accidents"
    implications: "Must model types, instances, intrinsic properties, and relational properties as distinct categories"
    source: "Chunk 1:127-129"

  - commitment: "Descriptive Metaphysics"
    position: "Ontology should align with human cognition and language, not prescribe revised reality"
    implications: "Rejects Bunge's revisionary approach; validates modeler intuitions"
    source: "Chunk 1:116-121"

  - commitment: "Particularized Properties (Tropes)"
    position: "Properties are individual instances, not just universal predicates"
    implications: "Enables modeling relationships as bearers of properties; weak entities become natural"
    source: "Chunk 1:128-136"

  - commitment: "Anti-Rigidity Extension"
    position: "Anti-rigid type distinctions (roles, phases) apply to ALL endurant categories, not just objects"
    implications: "Modes and relators can have phases and roles too"
    source: "Chunk 1:375-381"

  - commitment: "Separation of Conceptualization and Codification"
    position: "Conceptual modeling phase uses different language than implementation/codification phase"
    implications: "One OntoUML model can map to multiple codifications (OWL, RDFS, Haskell, SQL, etc.)"
    source: "Chunk 1:302-317"

boundary_definitions:
  - entity_type: "Endurant vs Perdurant"
    identity_criteria: "Wholly present at each moment vs unfolds through temporal parts"
    boundary_cases: "Not addressed: when does a persistent entity become a process?"
    source: "Chunk 1:173-185"

  - entity_type: "Substance vs Moment"
    identity_criteria: "Existential independence vs existential dependence on bearer"
    boundary_cases: "Moments depend on substances; moments can be bearers of other moments"
    source: "Chunk 1:128-136"

  - entity_type: "Sortal vs Non-Sortal"
    identity_criteria: "Supplies identity to instances vs does not supply identity"
    boundary_cases: "Categories, mixins, role mixins are non-sortals"
    source: "Chunk 1:366-367"

  - entity_type: "Pattern vs Anti-Pattern"
    identity_criteria: "Higher-granularity cluster with fixed configuration (pattern) vs recurrent error structure (anti-pattern)"
    boundary_cases: "Anti-patterns detected empirically from model repository"
    source: "Chunk 1:257-262, 325-337"

temporal_modeling:
  - aspect: "Endurant-Perdurant Split"
    approach: "Separate strata for structural (timeless) and temporal (event-based) aspects"
    mechanism: "UFO-A for endurants, UFO-B for perdurants; dispositions connect them"
    source: "Chunk 1:170-185"

  - aspect: "Perdurant Mereology"
    approach: "Events and processes have temporal parts and ordering"
    mechanism: "Part-whole relations specific to perdurants"
    source: "Chunk 1:183-184"

  - aspect: "Change and Causation"
    approach: "Dispositions enable causal laws as foundation of transition rules"
    mechanism: "Connection between endurants and perdurants"
    source: "Chunk 1:184-185"

  - aspect: "Modal Properties"
    approach: "Essential vs accidental properties; anti-rigid types can be gained/lost"
    mechanism: "Formal semantics in Sortal Quantified Modal Logic"
    source: "Chunk 1:175-176, 375-376"

  - aspect: "Temporal OCL Constraints"
    approach: "Representing dynamic invariants"
    mechanism: "Temporal OCL support in OntoUML editor"
    source: "Chunk 1:288-290"

agency_spectrum:
  - agent_type: "Human Agent (Implicit)"
    capabilities: "Beliefs, desires, intentions, goals, commitments, claims"
    constraints: "Not explicitly bounded in the paper"
    source: "Chunk 1:191-193"
    notes: "UFO-C addresses intentional and social entities"

  - agent_type: "Software Agent (Implicit)"
    capabilities: "Actions, social roles"
    constraints: "Unclear whether software has full intentionality"
    source: "Chunk 1:191-193"
    notes: "Paper mentions TROPOS/i* and AORML analysis"

  - agent_type: "Organizational Agent (Implicit)"
    capabilities: "Social relators, organizational structures"
    constraints: "Modeled as social structures, not as primitive agents"
    source: "Chunk 1:199-200"
    notes: "Organizational Structures domain ontology developed using UFO"

knowledge_representation:
  - mechanism: "OntoUML"
    formalism: "UML Profile with ontologically-grounded stereotypes"
    reasoning: "Formal verification against metamodel constraints; visual simulation"
    source: "Chunk 1:213-222"

  - mechanism: "OWL Mapping"
    formalism: "Six different OntoUML-to-OWL transformations"
    reasoning: "Different styles for different non-functional requirements"
    source: "Chunk 1:313-317"

  - mechanism: "Alloy Transformation"
    formalism: "Transformation from OntoUML to Alloy for lightweight formal verification"
    reasoning: "Model validation via constraint checking"
    source: "Chunk 1:442-443"

  - mechanism: "SBVR Verbalization"
    formalism: "Model verbalization in structured English following SBVR"
    reasoning: "Enables domain expert review without modeling notation expertise"
    source: "Chunk 1:271-276"

  - mechanism: "Sortal Quantified Modal Logic"
    formalism: "Formal semantics for object identifiers and modal properties"
    reasoning: "Cross-world identity, essential vs accidental properties"
    source: "Chunk 1:175-176"

emergence_indicators:
  - phenomenon: "Ontological Patterns from Repository"
    mechanism: "Empirical observation of model structures across domains"
    evidence: "Domain-related patterns extracted from Core Ontologies for reuse"
    source: "Chunk 1:267-270"

  - phenomenon: "Anti-Pattern Discovery"
    mechanism: "Statistical analysis of recurrent error structures in large model corpus"
    evidence: "High correlation between anti-pattern presence and adoption of rectification solutions"
    source: "Chunk 1:318-337"

  - phenomenon: "Language Evolution from User Behavior"
    mechanism: "Systematic subversions signal needed language extensions"
    evidence: "Users modeling perdurants in OntoUML despite syntax prohibition triggered UFO-B integration"
    source: "Chunk 1:353-364"

  - phenomenon: "Theory Evolution from Practice"
    mechanism: "Users applying type distinctions to modes/relators triggered theory expansion"
    evidence: "Anti-rigid types now applicable to all endurant categories"
    source: "Chunk 1:365-381"

integration_surfaces:
  - surface: "UML Metamodel"
    connects_to: ["UML 2.0 Class Diagrams", "Enterprise Architect", "UML tools"]
    alignment_quality: "High - OntoUML is a UML Profile"
    source: "Chunk 1:243-249"

  - surface: "DOLCE"
    connects_to: ["DOLCE ontology", "LOA work"]
    alignment_quality: "Partial - UFO extends beyond DOLCE's particulars-only scope"
    source: "Chunk 1:138-145"

  - surface: "GFO/GOL"
    connects_to: ["General Formalized Ontology"]
    alignment_quality: "Partial - GFO relation theory has Bradley Regress issue"
    source: "Chunk 1:137-138, 158-159"

  - surface: "OntoClean"
    connects_to: ["OntoClean methodology", "meta-properties"]
    alignment_quality: "High - UFO systematizes notions underlying OntoClean"
    source: "Chunk 1:153-156"

  - surface: "Enterprise Architecture Languages"
    connects_to: ["TOGAF", "ArchiMate", "RM-ODP", "ARIS", "BPMN"]
    alignment_quality: "Analyzed and reengineered using UFO"
    source: "Chunk 1:196-198"

  - surface: "Agent-Oriented Languages"
    connects_to: ["TROPOS/i*", "AORML"]
    alignment_quality: "Analyzed and integrated via UFO-C"
    source: "Chunk 1:197-198"

gaps_and_tensions:
  - gap_type: "Omission"
    description: "No explicit treatment of AI agents or autonomous software systems"
    implications: "LLM agents would need to be positioned within UFO-C's intentional agent model"
    source: "Implicit - paper from 2015, pre-LLM era"

  - gap_type: "Tension"
    description: "Endurant-focused language (OntoUML) needed to represent perdurants by user demand"
    implications: "Led to UFO-B integration work; complexity management challenges acknowledged"
    source: "Chunk 1:353-364"

  - gap_type: "Underspecified"
    description: "UFO-C (intentional/social) less developed than UFO-A"
    implications: "Goals, commitments, social roles mentioned but not detailed in this paper"
    source: "Chunk 1:191-193"

  - gap_type: "Tension"
    description: "BWW approach predicts relations should not be classes; UFO allows reified relationships"
    implications: "Explicit rejection of BWW; practitioners' intuitions validated"
    source: "Chunk 1:121-125"

  - gap_type: "Practical Challenge"
    description: "UFO-B integration increases diagram complexity"
    implications: "Needs new complexity management theories and tools (filtering, modularization, viewpoints)"
    source: "Chunk 1:361-364"

  - gap_type: "Underspecified"
    description: "Rule and constraint layer not a first-class part of UFO strata"
    implications: "OCL and temporal OCL used but not grounded in ontological micro-theory"
    source: "Chunk 1:286-290"

empirical_grounding:
  - type: "Model Repository Analysis"
    domain: "Multiple (telecommunications, government, biodiversity, bioinformatics)"
    scale: "Models ranging from dozens to thousands of concepts"
    findings: "Anti-patterns catalogued; high correlation between anti-pattern presence and rectification adoption"
    source: "Chunk 1:318-337"

  - type: "U.S. Department of Defense Adoption"
    domain: "Government/Defense"
    scale: "Enterprise Logical Data Model"
    findings: "Successful use led to SIMF proposal consideration"
    source: "Chunk 1:223-225, 355"

  - type: "Domain Ontology Applications"
    domain: "Geology, Biodiversity, Organ Donation, Petroleum, Disaster Management, etc."
    scale: "Multiple industrial and government projects internationally"
    findings: "Practical applicability across diverse domains"
    source: "Chunk 1:227-242"

  - type: "Language Subversion Studies"
    domain: "Various"
    scale: "Multiple institutions over years"
    findings: "Systematic patterns of syntax violation revealed needed language extensions"
    source: "Chunk 1:343-352"

# DISCOVERY NOTES

surprises:
  - "Treating syntax violations as valuable empirical data for language evolution - counterintuitive but productive"
  - "Powertypes as endurants rather than higher-order types - novel interpretation"
  - "Explicit rejection of Bunge/BWW despite being inspired by its goals"
  - "Anti-rigid type distinctions extended to moments/relators based on user behavior"

tensions_with_other_papers:
  - "BWW approach: UFO explicitly rejects the prediction that relations should not be modeled as classes"
  - "DOLCE: UFO extends to include universals; DOLCE is particulars-only"
  - "GFO: UFO avoids Bradley Regress issue present in GFO relation theory"

unique_contributions:
  - "Four-Category Ontology systematized for conceptual modeling"
  - "Three-strata architecture (UFO-A/B/C) separating structural, temporal, and intentional concerns"
  - "Ontology-based language engineering method"
  - "Visual simulation for model validation"
  - "Anti-pattern detection and rectification methodology"
  - "Empirical approach to foundational ontology development"

potential_synthesis_opportunities:
  - "UFO-C's intentional model + modern AI agent architectures"
  - "UFO's relator concept + process mining event-object relationships"
  - "OntoUML patterns + knowledge graph construction"
  - "Visual simulation + LLM-based model explanation"

quality_checklist:
  used_paper_terminology: true
  captured_novel_concepts: true
  found_gaps_or_tensions: true
  noted_surprises: true
  chunk_references_included: true
  avoided_category_forcing: true
  preserved_nuance: true
---

# Paper Analysis: UFO Story - Ontological Foundations for Conceptual Modeling

## Summary

This is a position paper describing the 10+ year research program behind UFO (Unified Foundational Ontology) and its primary application, the OntoUML conceptual modeling language. The paper provides historical context, theoretical foundations, practical applications, and reflections on how empirical observation of language use has driven both language and theory evolution.

## Core Contribution

UFO is a **Four-Category Ontology** distinguishing:
- Individuals vs Universals
- Substances vs Accidents (moments/tropes)

Organized into three strata:
- **UFO-A**: Endurants (structural conceptual modeling)
- **UFO-B**: Perdurants (events, processes, causation)
- **UFO-C**: Intentional/Social entities (beliefs, goals, commitments)

## Key Theoretical Positions

### Descriptive Metaphysics
UFO explicitly adopts descriptive metaphysics over revisionary ontology. This means:
> "Any attempt to develop ontological foundations for conceptual modeling should take both human cognition and human linguistic competence seriously" (Chunk 1:116-118)

This positions UFO against the BWW (Bunge-Wand-Weber) approach, which used philosophy of hard sciences for conceptual modeling.

### Particularized Properties (Tropes)
UFO commits to tropes/moments as fundamental:
> "We needed particularized properties not only because they were of great importance in making sense of language and cognition...but because they would repeatedly appear in the discourse of conceptual modelers." (Chunk 1:130-132)

This enables:
- Relationships modeled as first-class entities (relators)
- Weak entities with properties
- Properties bearing other properties

## Methodological Innovation: Learning from Subversions

The most surprising contribution is treating **systematic language subversions** as empirical data:

> "These 'subversions' would (purposefully) produce models that were grammatically incorrect, but which were needed to express the intended characterization of their underlying conceptualizations that could not be expressed otherwise." (Chunk 1:347-349)

Examples:
1. Users modeling perdurants in OntoUML (endurant-only language) -> triggered UFO-B integration
2. Users applying role/phase distinctions to modes and relators -> expanded theory of anti-rigid types

## OntoUML: The Language Instantiation

OntoUML is designed such that:
> "The worldview embedded in the language through its conceptual primitives...should be isomorphic to the ontological distinctions put forth by UFO-A" (Chunk 1:217-218)

Engineering support includes:
- Pattern-based model construction
- Visual simulation for validation
- Anti-pattern detection and rectification
- Multiple OWL mapping strategies
- SBVR verbalization

## Gaps Identified

1. **AI Agents**: Paper predates LLM era; UFO-C's intentional model would need extension for AI agency
2. **Rule Layer**: Constraints handled via OCL but not grounded in ontological micro-theory
3. **Complexity Management**: UFO-B integration acknowledged to increase diagram complexity
4. **UFO-C Depth**: Intentional/social layer less detailed than UFO-A

## Integration Surfaces

Strong alignment with:
- UML (OntoUML is a UML Profile)
- OntoClean methodology
- Enterprise Architecture languages (analyzed/reengineered)

Partial alignment with:
- DOLCE (UFO extends to universals)
- GFO (UFO avoids Bradley Regress)

## Relevance for AI Agent Ontologies

UFO provides:
- Robust theory of intentional entities (beliefs, desires, goals) in UFO-C
- Action and commitment concepts
- Social role and relator patterns
- Disposition-based causation linking agents to events

But would need extension for:
- Bounded/delegated agency (AI vs human)
- Knowledge base integration
- Tool use and environment interaction
- Multi-agent coordination patterns
