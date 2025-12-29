---
paper_id: "23-UFO_Story_Ontological_Foundations"
title: "Towards ontological foundations for conceptual modeling: The unified foundational ontology (UFO) story"
authors:
  - "Giancarlo Guizzardi"
  - "Gerd Wagner"
  - "Joao Paulo Andrade Almeida"
  - "Renata S.S. Guizzardi"
year: 2015
doi: "10.3233/AO-150157"
chunks_expected: 1
chunks_read: 1
analysis_complete: true
high_priority_fields_found: 7

# ============================================
# EXTRACTION FIELDS (All 15)
# ============================================

entity_types:
  - name: "Endurant"
    description: "Entities wholly present at any time they exist (objects, substances)"
    chunk_ref: "1:173-181"
    quote: "UFO-A: An Ontology of Endurants dealing with structural conceptual modeling..."
  - name: "Perdurant"
    description: "Entities that unfold in time, having temporal parts (events, processes)"
    chunk_ref: "1:183-185"
    quote: "UFO-B: An Ontology of Perdurants dealing with Mereology, Temporal Ordering..."
  - name: "Intentional Entity"
    description: "Mental states and intentional phenomena (beliefs, desires, intentions, goals)"
    chunk_ref: "1:191-193"
    quote: "notions such as Beliefs, Desires, Intentions, Goals, Actions..."
  - name: "Social Entity"
    description: "Social constructs and relational complexes (commitments, claims, social roles)"
    chunk_ref: "1:191-193"
    quote: "Commitments and Claims, Social Roles and Social Particularized Relational Complexes..."
  - name: "Moment (Trope/Mode/Quality)"
    description: "Particularized properties - existentially dependent on bearers"
    chunk_ref: "1:127-133"
    quote: "accidents (particularized properties, moments, qualities, modes, tropes)..."
  - name: "Substance Sortal (Kind)"
    description: "Types that supply identity criteria to their instances"
    chunk_ref: "1:366-368"
    quote: "substance sortals (kinds), phased-sortals (roles and phases)..."
  - name: "Relator"
    description: "Particularized relational properties that ground material relations"
    chunk_ref: "1:192"
    quote: "Social Particularized Relational Complexes (Social Relators)"

entity_definitions:
  Four-Category Ontology: "An ontological framework countenancing both individuals and universals, including substantial individuals/universals and accidents (particularized properties, moments, qualities, modes, tropes)"
  Endurant: "Entity dealing with structural conceptual modeling aspects, organized as Four-Category ontology comprising theories of Types, Taxonomic Structures, Part-Whole Relations, Particularized Properties, Attributes, Datatypes, Relations and Roles"
  Perdurant: "Entity dealing with events and processes including Perdurant Mereology, Temporal Ordering, Object Participation, Causation, Change, and connection to Endurants via Dispositions"
  Intentional_Entity: "Social entity addressing Beliefs, Desires, Intentions, Goals, Actions, Commitments, Claims, Social Roles and Social Relators - built on top of UFO-A and UFO-B"
  Substance_Sortal: "A kind that provides identity criteria for its instances, distinguishing them from phased-sortals (roles, phases) and non-sortals (categories, mixins, role mixins)"
  Moment: "A particularized property (also called trope, quality, mode, aspect, way, abstract particular) that is existentially dependent on a bearer"

entity_relationships:
  - from: "UFO-C"
    to: "UFO-A"
    relationship: "constructed on top of"
    source: "Chunk 1:191"
  - from: "UFO-C"
    to: "UFO-B"
    relationship: "constructed on top of"
    source: "Chunk 1:191"
  - from: "Perdurant"
    to: "Endurant"
    relationship: "connected via Dispositions"
    source: "Chunk 1:184-185"
  - from: "Relator"
    to: "Material Relation"
    relationship: "grounds"
    source: "Chunk 1:264-265"
  - from: "Agent"
    to: "Action"
    relationship: "performs"
    source: "Chunk 1:191-193"
  - from: "Moment"
    to: "Bearer"
    relationship: "existentially dependent on"
    source: "Chunk 1:127-133"

abstraction_level: "foundational"

framework_comparison:
  - compared_to: "BWW (Bunge-Wand-Weber)"
    relationship: "critiques and extends"
    details: "BWW based on Bunge's philosophy of science inadequate for conceptual modeling which requires descriptive metaphysics accounting for cognition and linguistic competence"
    source: "Chunk 1:105-125"
  - compared_to: "DOLCE"
    relationship: "unifies with GFO to create UFO"
    details: "Both DOLCE and GFO based on Aristotelian Square (Four-Category Ontologies), but DOLCE lacks universals as category and rich theory of relations"
    source: "Chunk 1:138-162"
  - compared_to: "GFO"
    relationship: "unifies with DOLCE to create UFO"
    details: "GFO theory of relations subject to Bradley Regress making it unsuitable for conceptual modeling applications"
    source: "Chunk 1:137-162"
  - compared_to: "OntoClean"
    relationship: "extends with richer type theory"
    details: "UFO systematizes notions pervasive in conceptual modeling (types, roles, phases, mixins) that OntoClean addresses partially"
    source: "Chunk 1:152-156"
  - compared_to: "UML"
    relationship: "provides ontological foundations for"
    details: "OntoUML is ontologically well-founded version of UML 2.0 class diagrams"
    source: "Chunk 1:213-222"
  - compared_to: "TOGAF, ArchiMate, RM-ODP, TROPOS, AORML, ARIS, BPMN"
    relationship: "used to analyze and reengineer"
    details: "UFO employed as basis for analyzing, reengineering and integrating many modeling languages and standards"
    source: "Chunk 1:196-198"

ai_integration: "N/A - paper published 2015, predates LLM/AI integration discussion"

agent_modeling:
  - aspect: "Intentionality (BDI)"
    description: "Agents modeled with Beliefs, Desires, Intentions following BDI tradition"
    source: "Chunk 1:191-193"
  - aspect: "Goals and Actions"
    description: "Goal-directed action as core agent capability"
    source: "Chunk 1:191-193"
  - aspect: "Social Commitments"
    description: "Agents make and hold commitments and claims in social context"
    source: "Chunk 1:192"
  - aspect: "Social Roles"
    description: "Agents occupy social roles defining permissions and responsibilities"
    source: "Chunk 1:192"

agentic_workflows: "N/A - paper predates agentic AI workflow discussion"

generative_ai_patterns: "N/A - paper published 2015, predates generative AI"

agent_ontology_integration: "N/A - paper predates AI agent-ontology integration patterns"

entity_count:
  count: "Three-layer structure (UFO-A, UFO-B, UFO-C) with multiple micro-theories"
  rationale: "Stratified design to address different aspects of reality - structural, temporal, and intentional/social"
  source: "Chunk 1:170-193"

methodology: "top-down"

empirical_evidence:
  - type: "Model Repository"
    description: "Repository containing OntoUML models in domains like telecommunications, government, biodiversity, bioinformatics; sizes from dozens to thousands of concepts"
    source: "Chunk 1:318-322"
  - type: "Industrial Validation"
    description: "Validation study with large industrial model demonstrating high correlation between anti-patterns and proposed solutions"
    source: "Chunk 1:334-337"
  - type: "Government Adoption"
    description: "Considered for OMG SIMF after successful use by U.S. Department of Defense"
    source: "Chunk 1:223-225"
  - type: "Academic Adoption"
    description: "Adopted by ORM 2.0 and used in projects across academic, government, and industrial institutions"
    source: "Chunk 1:225-228"

limitations:
  - "Original OntoUML focused on structural/endurantistic aspects, required extension for perdurants (Chunk 1:353-357)"
  - "Introduction of UFO-B substantially increases diagram complexity, requiring new complexity management tools (Chunk 1:361-364)"
  - "Predates AI/LLM era, no discussion of AI agent integration patterns"

tools_standards:
  - "OntoUML (conceptual modeling language based on UFO-A)"
  - "UML 2.0 Profile"
  - "OWL (6 different transformation styles)"
  - "XML"
  - "Smalltalk"
  - "Modal Prolog"
  - "OCL (constraint language)"
  - "Temporal OCL"
  - "SBVR (model verbalization)"
  - "Alloy (formal validation)"
---

# Towards ontological foundations for conceptual modeling: The UFO story - Analysis Index

## Paper Overview

- **Source**: 23-UFO_Story_Ontological_Foundations.pdf
- **Chunks**: 1 chunk, ~15,339 tokens estimated
- **Analyzed**: 2025-12-28T15:15:00
- **Journal**: Applied Ontology 10 (2015) 259-271

## Key Extractions

This seminal position paper describes the development of the Unified Foundational Ontology (UFO) and its primary application OntoUML. UFO is a foundational ontology specifically designed to address conceptual modeling requirements, developed by unifying insights from DOLCE and GFO while extending them with richer theories of types, relations, and particularized properties.

The paper makes a compelling case against using general philosophy of science ontologies (like Bunge's used in BWW) for conceptual modeling, arguing that conceptual modeling requires descriptive metaphysics that takes human cognition and linguistic competence seriously. This led to the requirement for a Four-Category Ontology that includes not just individuals and universals, but also substantial entities and accidents (particularized properties/moments/tropes).

UFO is organized in three strata: UFO-A (Endurants for structural modeling), UFO-B (Perdurants for events and processes), and UFO-C (Intentional and Social Entities built on top of A and B). The paper details the successful implementation of UFO-A as OntoUML and describes extensive tooling including pattern-based construction, formal verification, visual simulation, model verbalization, code generation, and anti-pattern detection.

### Entity Types

| Entity Type | Layer | Description | Source |
|-------------|-------|-------------|--------|
| Endurant | UFO-A | Wholly present at any time; objects, substances | Chunk 1:173-181 |
| Perdurant | UFO-B | Temporal parts; events, processes | Chunk 1:183-185 |
| Intentional Entity | UFO-C | Mental states: beliefs, desires, intentions | Chunk 1:191-193 |
| Social Entity | UFO-C | Commitments, claims, social roles, relators | Chunk 1:191-193 |
| Moment/Trope | UFO-A | Particularized properties dependent on bearers | Chunk 1:127-133 |
| Substance Sortal | UFO-A | Identity-providing types (kinds) | Chunk 1:366-368 |
| Relator | UFO-A | Particularized relational properties | Chunk 1:192 |

### Framework Comparisons

| Compared To | Relationship | Key Insight | Source |
|-------------|--------------|-------------|--------|
| BWW | Critiques | Bunge's philosophy of science inadequate for descriptive metaphysics | Chunk 1:105-125 |
| DOLCE | Unifies | Lacks universals and rich relation theory | Chunk 1:138-162 |
| GFO | Unifies | Bradley Regress makes it unsuitable for CM | Chunk 1:137-162 |
| UML, TOGAF, ArchiMate | Grounds | UFO provides ontological foundations | Chunk 1:196-198 |

### Agent Modeling (UFO-C)

The paper describes UFO-C as an ontology of intentional and social entities addressing:
- **BDI Mental States**: Beliefs, Desires, Intentions (Chunk 1:191-193)
- **Goal-Directed Action**: Goals and Actions as core primitives (Chunk 1:191-193)
- **Social Commitments**: Commitments and Claims in social context (Chunk 1:192)
- **Social Roles**: Role-based permissions and responsibilities (Chunk 1:192)

### Key Findings

1. **Four-Category Requirement** (Chunk 1:126-129): "We needed an ontological theory that would countenance both individuals and universals and one that would include not only substantial individuals and universals but also accidents (particularized properties, moments, qualities, modes, tropes)."

2. **Descriptive Metaphysics** (Chunk 1:116-118): "Any attempt to develop ontological foundations for conceptual modeling should take both human cognition and human linguistic competence seriously; it should be a project in descriptive metaphysics."

3. **Three-Layer Architecture** (Chunk 1:170-193): UFO organized as UFO-A (Endurants), UFO-B (Perdurants), UFO-C (Intentional/Social), with C built on top of A and B.

4. **OntoUML Success** (Chunk 1:223-225): "OntoUML has been adopted by many research, industrial and government institutions worldwide... considered as a candidate for addressing the OMG SIMF Request for Proposal after a report of its successful use by the U.S. Department of Defense."

5. **Systematic Subversions** (Chunk 1:340-352): Users deliberately subverting OntoUML syntax revealed need for new constructs, demonstrating co-evolution of theory and practice.

## Chunk Navigation

### Chunk 1: Complete Paper (Introduction through References)

- **Summary**: Position paper presenting the complete UFO story - historical context, three-layer architecture (UFO-A/B/C), OntoUML development, tooling ecosystem (pattern-based construction, verification, validation, verbalization, code generation, anti-pattern detection), empirical validation through model repositories and industrial studies, and lessons learned from systematic language subversions.

- **Key concepts**:
  - Four-Category Ontology
  - Endurant/Perdurant distinction
  - Substance sortals vs phased-sortals
  - Particularized properties (moments/tropes)
  - Relators and material relations
  - BDI mental states
  - Social roles and commitments
  - OntoUML
  - Ontological patterns and anti-patterns
  - Model validation via visual simulation
  - Descriptive metaphysics

- **Key quotes**:
  - Line 87-88: "the opposite of ontology is not non-ontology, but bad ontology" (Collier)
  - Line 116-118: "any attempt to develop ontological foundations for conceptual modeling should take both human cognition and human linguistic competence seriously"
  - Line 145-146: "hence, the name Unified Foundational Ontology"
  - Line 349-352: "the users of the language were speaking to us via these systematic subversions"

- **Load when**:
  - "User asks about UFO foundational ontology"
  - "Query mentions OntoUML or ontology-driven conceptual modeling"
  - "User wants comparison of foundational ontologies (UFO vs DOLCE vs GFO vs BWW)"
  - "Query about Four-Category Ontology or Aristotelian Square"
  - "User asks about endurant/perdurant distinction"
  - "Query mentions BDI agents or intentional entities"
  - "User asks about ontological patterns or anti-patterns"

## Relevance to Research Questions

### RQ1: Universal Entities Across Foundational Ontologies
UFO demonstrates the Agent-Activity-Entity pattern through UFO-C's intentional agents performing actions that affect entities. The paper explicitly discusses how UFO shares the Four-Category structure with DOLCE and GFO.

### RQ2: Agent-Activity-Entity Triad
UFO-C explicitly models Agents with BDI mental states, Actions/Activities as perdurants, and Entities as endurants - directly manifesting this triad.

### RQ3: Abstraction Level and Entity Count
The paper demonstrates stratified abstraction - UFO-A/B/C layers address different aspects while sharing foundational commitments. Entity count increases with domain specificity.

### RQ4: 8-Entity Hypothesis Grounding
UFO provides direct grounding for Goal, Task (Action), Role (Social Role), Resource (Entity), Agent, Event (Perdurant). Rule maps to normative aspects in UFO-C. Data maps to informational aspects.

### RQ5-7: AI Agent Patterns
Paper predates LLM era (2015) but UFO-C's agent modeling (BDI, social commitments, roles) provides theoretical foundation for AI agent ontological grounding.
