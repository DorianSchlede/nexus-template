---
paper_id: "04-PROV-O_to_BFO_Semantic_Mapping"
title: "A semantic approach to mapping the Provenance Ontology to Basic Formal Ontology"
authors:
  - "Tim Prudhomme"
  - "Giacomo De Colle"
  - "Austin Liebers"
  - "Alec Sculley"
  - "Peihong Karl Xie"
  - "Sydney Cohen"
  - "John Beverley"
year: 2025
chunks_expected: 2
chunks_read: 2
analysis_complete: true
high_priority_fields_found: 7

# Extraction fields
entity_types:
  - "Entity"
  - "Agent"
  - "Activity"
  - "Influence"
  - "InstantaneousEvent"
  - "Generation"
  - "Start"
  - "End"
  - "Communication"
  - "Derivation"
  - "EntityInfluence"
  - "ActivityInfluence"
  - "AgentInfluence"
  - "Role"
  - "Plan"
  - "Location"
  - "Bundle"
  - "Collection"
  - "Person"
  - "Organization"
  - "SoftwareAgent"

entity_definitions:
  Entity: "A physical, digital, conceptual, or other kind of thing with some fixed aspects; entities may be real or imaginary. Can exist entirely at different times and persist its identity over time with all spatial parts and no temporal parts (Chunk 1:633-641)"
  Agent: "A material entity that bears some form of responsibility for an activity taking place, for the existence of an entity, or another agent's activity. Bears some role that is realized in a PROV Activity (Chunk 1:654-665)"
  Activity: "Something that occurs over a period of time and acts upon or with entities. An entity that unfolds itself in time - equivalent to BFO process (Chunk 1:682-691)"
  Influence: "The capacity of an entity, activity, or agent to have an effect on the character, development, or behavior of another by means of usage, start, end, generation, invalidation, communication, derivation, attribution, association, or delegation (Chunk 2:32-34)"
  Role: "The function of an entity or agent with respect to an activity, in the context of a usage, generation, invalidation, association, start, and end (Chunk 2:103-104)"
  Plan: "An Information Content Entity that represents a set of actions or steps intended by one or more agents to achieve some goals (Chunk 2:119-124)"
  Location: "Equivalent to BFO site - a three-dimensional immaterial entity whose boundaries coincide with material entities (Chunk 1:808-815)"

entity_relationships:
  - from: "Entity"
    to: "Activity"
    relationship: "disjoint (mapped to continuant vs occurrent)"
    source: "Chunk 1:643-645"
  - from: "Agent"
    to: "Activity"
    relationship: "participates in"
    source: "Chunk 1:662-663"
  - from: "Agent"
    to: "Role"
    relationship: "bears (role realized in Activity)"
    source: "Chunk 1:655"
  - from: "Entity"
    to: "Activity"
    relationship: "wasGeneratedBy"
    source: "Chunk 1:735-738"
  - from: "Activity"
    to: "Agent"
    relationship: "wasAssociatedWith"
    source: "Chunk 1:758-761"
  - from: "Entity"
    to: "Entity"
    relationship: "wasDerivedFrom (causal)"
    source: "Chunk 1:818-821"
  - from: "Activity"
    to: "InstantaneousEvent"
    relationship: "has temporal part (Start/End)"
    source: "Chunk 2:164-167"
  - from: "Influence"
    to: "Agent/Activity/Entity"
    relationship: "influencer/qualifiedInfluence"
    source: "Chunk 2:150-154"

abstraction_level: "core"
# Note: PROV-O is a core/mid-level ontology that bridges foundational BFO with domain applications

framework_comparison:
  - compared_to: "BFO"
    relationship: "maps_to"
    details: "Total alignment of 153 classes and object properties. PROV Activity = BFO process; PROV Entity subclass of BFO continuant; PROV Agent subclass of BFO material entity"
    source: "Chunk 1:577-598"
  - compared_to: "CCO"
    relationship: "extends_to"
    details: "PROV Agent = CCO Agent intersection; PROV Person = CCO Person intersection; PROV Plan subclass of CCO Information Content Entity; PROV Start = CCO process beginning; PROV End = CCO process ending"
    source: "Chunk 1:676-679, Chunk 2:93-100, 116-124"
  - compared_to: "RO"
    relationship: "maps_to"
    details: "25 terms explicitly mapped using 26 subsumption relations. wasDerivedFrom mapped to RO causally influenced by"
    source: "Chunk 1:594-595, 818-821"
  - compared_to: "SOSA"
    relationship: "compatible_with"
    details: "Alignments tested for consistency with PROV-SOSA alignment; no inconsistencies found"
    source: "Chunk 1:439-445"

ai_integration: "N/A - paper predates LLM/AI integration discussion (2025 ontology mapping focus)"

agent_modeling:
  - aspect: "Responsibility-bearing"
    description: "Agents bear responsibility for activities through formalized participation and role-bearing axioms"
    source: "Chunk 1:660-665"
  - aspect: "Material realization"
    description: "PROV Agent always has matter as part - even SoftwareAgent is material realization of software"
    source: "Chunk 1:654-659"
  - aspect: "Agent-Activity disjointness"
    description: "Mapping to BFO implies agents (continuants) are disjoint from activities (occurrents), contradicting PROV Requirement V14"
    source: "Chunk 1:715-718"
  - aspect: "Role-based"
    description: "Agents bear BFO roles that are realized in activities; roles are externally determined by context"
    source: "Chunk 2:103-113"

agentic_workflows: "N/A - paper focuses on ontology alignment, not workflow patterns"

generative_ai_patterns: "N/A - paper predates generative AI discussion"

agent_ontology_integration:
  - mechanism: "Knowledge graph integration"
    description: "Alignment enables SPARQL queries over PROV-O data using BFO classes; semantic reasoners can discover implicit information"
    source: "Chunk 1:106-112"
  - mechanism: "Automated reasoning"
    description: "HermiT reasoner used to test consistency and materialize inferences from combined ontologies"
    source: "Chunk 1:424-436"
  - mechanism: "Error detection"
    description: "Alignments used to automatically detect mistakes in canonical PROV-O examples"
    source: "Chunk 1:110-112, Chunk 2:226-258"

entity_count:
  count: 153
  rationale: "Total classes and object properties in PROV-O and extensions (PROV-AQ, PROV-Dictionary, PROV-Links, PROV-Inverses, PROV Dublin Core)"
  source: "Chunk 1:577-578"

methodology: "hybrid"
# Semi-automated: manual conceptual analysis + automated verification via SPARQL/reasoners

empirical_evidence:
  - type: "Consistency testing"
    description: "312 canonical example instances from W3C documentation tested with HermiT reasoner"
    source: "Chunk 1:425-436"
  - type: "Error detection"
    description: "2 examples inconsistent with PROV-O itself; 2 examples inconsistent with PROV-BFO alignment (errors in W3C docs)"
    source: "Chunk 1:432-436, Chunk 2:226-258"
  - type: "Conservativity verification"
    description: "SPARQL CONSTRUCT queries confirmed no changes to subsumption hierarchies within each ontology"
    source: "Chunk 1:448-458"

limitations:
  - "Data properties not formally mapped due to OWL/RDF representational limits (Chunk 2:191-212)"
  - "Agent-Activity disjointness contradicts PROV Requirement V14 allowing agents to be activities (Chunk 1:694-731)"
  - "Complex temporal mappings (startedAtTime, endedAtTime) require multi-step BFO/CCO relationships (Chunk 2:201-212)"
  - "SKOS mappings not included as formal alignment criteria - only supplementary (Chunk 1:376-378)"

tools_standards:
  - "OWL 2 DL"
  - "RDF"
  - "SPARQL"
  - "SWRL"
  - "RDF Turtle"
  - "SSSOM"
  - "SKOS"
  - "HermiT reasoner"
  - "ROBOT"
  - "GNU Make"
  - "GitHub Actions"
  - "Protege"
---

# A semantic approach to mapping the Provenance Ontology to Basic Formal Ontology - Analysis Index

## Paper Overview

- **Source**: 04-PROV-O_to_BFO_Semantic_Mapping.pdf
- **Chunks**: 2 chunks, ~24,836 estimated tokens
- **Analyzed**: 2025-12-28T14:45:00
- **DOI**: https://doi.org/10.1038/s41597-025-04580-1
- **Repository**: https://github.com/BFO-Mappings/PROV-to-BFO

## Key Extractions

This paper presents a rigorous methodology for creating semantic mappings between PROV-O (W3C Provenance Ontology) and BFO (Basic Formal Ontology), achieving a total alignment of 153 classes and object properties. The work is essential for understanding how the Agent-Activity-Entity triad manifests across foundational ontologies.

### Core Mapping Results

| PROV-O Term | BFO/CCO Mapping | Relation | Source |
|-------------|-----------------|----------|--------|
| Activity | BFO process | equivalentClass | Chunk 1:682-683 |
| Entity | BFO continuant (non-spatial) | subClassOf | Chunk 1:636-641 |
| Agent | BFO material entity + role | subClassOf | Chunk 1:654-655 |
| InstantaneousEvent | BFO process boundary | equivalentClass | Chunk 1:914-915 |
| Location | BFO site | equivalentClass | Chunk 1:808 |
| Start | CCO process beginning | equivalentClass | Chunk 2:93-94 |
| End | CCO process ending | equivalentClass | Chunk 2:94-95 |
| Person | CCO Person AND PROV Agent | equivalentClass | Chunk 1:773-776 |
| Plan | CCO Information Content Entity | subClassOf | Chunk 2:116-124 |
| Role | BFO role | subClassOf | Chunk 2:109-110 |

### Mapping Methodology Criteria (Chunk 1:143-378)

1. **Criterion 1: Types of Mapping Relations**
   - Equivalence (owl:equivalentClass, owl:equivalentProperty)
   - Subsumption (rdfs:subClassOf, rdfs:subPropertyOf)
   - Complex mappings via SWRL rules and property chains

2. **Criterion 2: Coherence and Consistency**
   - All formulae satisfiable (coherent)
   - No entailed contradictions (consistent)

3. **Criterion 3: Conservativity**
   - Alignment should not change semantic relationships within each ontology

4. **Criterion 4: Scope of Alignment**
   - Total alignment: every term in PROV-O mapped to some BFO term
   - Interpretability: PROV-O implications preserved in BFO
   - Synonymy: theoretical limit of bidirectional interpretation

### Agent-Activity-Entity Triad Analysis

The paper validates the Agent-Activity-Entity triad as a universal pattern:

- **Entity** (Chunk 1:633-645): Maps to BFO continuant - things with fixed aspects that persist identity over time
- **Activity** (Chunk 1:682-691): Equivalent to BFO process - things that unfold in time
- **Agent** (Chunk 1:654-668): Subclass of material entities bearing responsibility roles

Key insight: The triad maps to the fundamental BFO distinction between **continuants** (entities that exist wholly at any time) and **occurrents** (entities with temporal parts).

### Framework Integration

| Framework | Integration Approach | Source |
|-----------|---------------------|--------|
| BFO | 35 explicit mappings (6 equivalence, 24 subsumption, 8 SWRL) | Chunk 1:591-593 |
| CCO | 37 explicit mappings (5 equivalence, 23 subsumption, 1 chain, 6 SWRL) | Chunk 1:593-594 |
| RO | 25 explicit mappings (26 subsumption) | Chunk 1:594-595 |
| SOSA | Compatible via PROV-SOSA alignment chain | Chunk 1:439-445 |

## Chunk Navigation

### Chunk 1: Introduction, Methods, Starting Point/Expanded Mappings

- **Summary**: Introduces the data silo and ontology silo problems, presents the four mapping criteria (types, coherence/consistency, conservativity, scope), and details the Starting Point class mappings (Entity, Agent, Activity) plus Expanded class mappings (Person, Organization, Bundle, Location, Collection). Covers object property mappings like wasGeneratedBy, wasAssociatedWith, wasDerivedFrom, and atLocation (via SWRL rules).

- **Key concepts**: [ontology alignment, equivalence mapping, subsumption mapping, conservativity, totality, interpretability, synonymy, SWRL rules, Agent-Activity-Entity triad, BFO continuant, BFO occurrent, material entity, process boundary]

- **Key quotes**:
  - Line 39-40: "Ontologies are well-structured vocabularies that logically define classes and relationships in the interest of promoting interoperability"
  - Line 682-683: "PROV Activity is mapped as equivalent to the class BFO process"
  - Line 654-655: "PROV Agent is mapped as a subclass of BFO material entities that both participate in some PROV Activity and bear some BFO role"
  - Line 728-729: "every PROV Agent bears some BFO role that is realized in a PROV Activity"

- **Load when**: "User asks about PROV-O to BFO mapping" / "Query mentions Agent-Activity-Entity triad" / "Question about ontology alignment methodology" / "Interest in equivalence vs subsumption mappings"

### Chunk 2: Qualified Classes, Data Properties, Inconsistencies, Discussion

- **Summary**: Details Qualified class mappings (Influence hierarchy, Role, Plan), explains data property mapping challenges, documents inconsistencies found in W3C examples (2 PROV-O internal, 2 with alignment), and discusses practical applications of the alignments. Covers PROV Start/End to CCO process beginning/ending, Role to BFO role, Plan to CCO Information Content Entity.

- **Key concepts**: [Qualification Pattern, reification, PROV Influence, process boundary, CCO process beginning/ending, Information Content Entity, BFO role vs function, data property limitations, consistency testing, error detection]

- **Key quotes**:
  - Line 16-17: "PROV Influence, as the superclass of 16 Qualified Influence classes, is mapped to a subclass of the disjoint union of BFO process and BFO process boundary"
  - Line 103-104: "PROV Role is defined as the function of an entity or agent with respect to an activity"
  - Line 109-110: "we map PROV Role directly as a subclass of BFO role on the grounds that a PROV Role is externally determined by the context"
  - Line 312-316: "the alignments demonstrate how BFO and related ontologies can be used to find inconsistencies in data by enriching it with additional logical axioms"

- **Load when**: "User asks about Qualified Pattern in PROV-O" / "Query mentions reification in ontologies" / "Question about Role vs Function distinction" / "Interest in ontology-based error detection"

## Relevance to Research Questions

### RQ1: Universal entities across foundational ontologies
**HIGH RELEVANCE**: Demonstrates Agent-Activity-Entity as universal pattern mapping directly between PROV-O and BFO. Entity types map to continuant/occurrent distinction.

### RQ2: Agent-Activity-Entity triad manifestation
**HIGH RELEVANCE**: Core focus of paper. Provides formal semantics for triad with precise mappings and constraints.

### RQ3: Abstraction level and entity count
**MEDIUM RELEVANCE**: Shows 153 PROV-O terms vs broader BFO framework. PROV-O as mid-level ontology between foundational and domain.

### RQ4: 8-entity hypothesis grounding
**MEDIUM RELEVANCE**: Validates Agent, Activity (Task), Role, Event (InstantaneousEvent), Data (Entity). Goal partially via Plan. Resource and Rule not explicitly covered.

### RQ5-7: AI Agent patterns
**LOW RELEVANCE**: Paper predates LLM/AI agent discussion. However, automated reasoning via HermiT and SPARQL querying patterns relevant to ontology-guided AI.
