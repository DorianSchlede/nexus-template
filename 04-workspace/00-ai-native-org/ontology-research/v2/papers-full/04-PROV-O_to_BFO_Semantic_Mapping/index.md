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
schema_version: "2.3"

chunk_index:
  1:
    token_count: 14954
    fields_found:
      entity_types: true
      entity_definitions: true
      entity_relationships: true
      entity_count: true
      abstraction_level: true
      framework_comparison: true
      methodology: true
      ai_integration: false
      agent_modeling: true
      agentic_workflows: false
      generative_ai_patterns: false
      agent_ontology_integration: false
      empirical_evidence: true
      limitations: partial
      tools_standards: true
  2:
    token_count: 8899
    fields_found:
      entity_types: true
      entity_definitions: true
      entity_relationships: true
      entity_count: false
      abstraction_level: false
      framework_comparison: true
      methodology: partial
      ai_integration: false
      agent_modeling: partial
      agentic_workflows: false
      generative_ai_patterns: false
      agent_ontology_integration: false
      empirical_evidence: true
      limitations: true
      tools_standards: true

entity_types:
  - item: "Entity (PROV)"
    chunk: 1
    lines: "633-646"
    quote: "PROV Entity is defined as 'a physical, digital, conceptual, or other kind of thing with some fixed aspects; entities may be real or imaginary'. Our interpretation of this is that a PROV Entity can exist entirely at different times and persist its identity over time with all spatial parts and no temporal parts."
  - item: "Agent (PROV)"
    chunk: 1
    lines: "654-668"
    quote: "PROV Agent is mapped as a subclass of BFO material entities that both participate in some PROV Activity and bear some BFO role that is realized in a PROV Activity."
  - item: "Activity (PROV)"
    chunk: 1
    lines: "682-691"
    quote: "PROV Activity is mapped as equivalent to the class BFO process. The definition of PROV Activity includes 'something that occurs over a period of time and acts upon or with entities'."
  - item: "Continuant (BFO)"
    chunk: 1
    lines: "636-641"
    quote: "We therefore map PROV Entity as a subclass of BFO continuant with one exception. BFO spatial regions are continuants that neither participate in processes nor bear qualities."
  - item: "Occurrent (BFO)"
    chunk: 1
    lines: "684-686"
    quote: "A BFO occurrent - the parent class of BFO process - is defined as 'an entity that unfolds itself in time or it is the start or end of such an entity or it is a temporal or spatiotemporal region'."
  - item: "Process (BFO)"
    chunk: 1
    lines: "682-687"
    quote: "PROV Activity is mapped as equivalent to the class BFO process."
  - item: "Process Boundary (BFO)"
    chunk: 1
    lines: "911-920"
    quote: "PROV Influence, as the superclass of 16 Qualified Influence classes, is mapped to a subclass of the disjoint union of BFO process and BFO process boundary."
  - item: "Influence (PROV)"
    chunk: 1
    lines: "911-920"
    quote: "PROV Influence, as the superclass of 16 Qualified Influence classes, is mapped to a subclass of the disjoint union of BFO process and BFO process boundary."
  - item: "InstantaneousEvent (PROV)"
    chunk: 1
    lines: "913-915"
    quote: "PROV InstantaneousEvent, which is equivalently mapped to BFO process boundary since instances of PROV InstantaneousEvent are indivisible boundaries of some PROV Activity."
  - item: "Role (PROV)"
    chunk: 2
    lines: "103-113"
    quote: "PROV Role is defined as 'the function of an entity or agent with respect to an activity, in the context of a usage, generation, invalidation, association, start, and end'. We map PROV Role directly as a subclass of BFO role."
  - item: "Plan (PROV)"
    chunk: 2
    lines: "116-143"
    quote: "PROV Plan is mapped to a subclass of CCO Information Content Entity. According to CCO, an Information Content Entity is a BFO generically dependent continuant (GDC) that generically depends on some CCO Information Bearing Entity."
  - item: "Location (PROV)"
    chunk: 1
    lines: "808-815"
    quote: "PROV Location is mapped as equivalent to BFO site, which is defined as 'a three-dimensional immaterial entity whose boundaries either (partially or wholly) coincide with the boundaries of one or more material entities'."
  - item: "Bundle (PROV)"
    chunk: 1
    lines: "798-806"
    quote: "PROV Bundle is defined as 'a named set of provenance descriptions' that 'constitute islands of provenance information'. It is intended for annotating metadata about RDF documents. We therefore map it as a subclass of CCO Information Content Entity and also BFO generically dependent continuant."
  - item: "Collection (PROV)"
    chunk: 1
    lines: "802-806"
    quote: "We did not provide a more specific mapping for PROV Collection because it is defined more generically as 'an entity that provides a structure to some constituents, which are themselves entities'."

entity_definitions:
  Entity_PROV:
    definition: "A physical, digital, conceptual, or other kind of thing with some fixed aspects; entities may be real or imaginary"
    chunk: 1
    lines: "633-635"
  Agent_PROV:
    definition: "Material entity that participates in some PROV Activity and bears some BFO role that is realized in a PROV Activity; bears responsibility for an activity, entity existence, or another agent's activity"
    chunk: 1
    lines: "654-665"
  Activity_PROV:
    definition: "Something that occurs over a period of time and acts upon or with entities; equivalent to BFO process"
    chunk: 1
    lines: "682-684"
  Influence_PROV:
    definition: "The capacity of an entity, activity, or agent to have an effect on the character, development, or behavior of another by means of usage, start, end, generation, invalidation, communication, derivation, attribution, association, or delegation"
    chunk: 1
    lines: "927-929"
  Role_PROV:
    definition: "The function of an entity or agent with respect to an activity, in the context of a usage, generation, invalidation, association, start, and end"
    chunk: 2
    lines: "103-104"
  Plan_PROV:
    definition: "Represents a set of actions or steps intended by one or more agents to achieve some goals; a generically dependent continuant that may have multiple copies"
    chunk: 2
    lines: "119-124"
  Continuant_BFO:
    definition: "Entity that can exist entirely at different times and persist its identity over time with all spatial parts and no temporal parts"
    chunk: 1
    lines: "634-636"
  Occurrent_BFO:
    definition: "Entity that unfolds itself in time or it is the start or end of such an entity or it is a temporal or spatiotemporal region"
    chunk: 1
    lines: "684-686"
  Process_BFO:
    definition: "A type of occurrent that has material entity as participant (though not formalized as logical axiom)"
    chunk: 1
    lines: "687-691"
  Process_Boundary_BFO:
    definition: "Indivisible boundaries of some process; instances exist at an instant of time"
    chunk: 1
    lines: "914-915"

entity_relationships:
  - item: "PROV Entity subClassOf BFO continuant (excluding spatial regions)"
    chunk: 1
    lines: "636-646"
    quote: "We therefore map PROV Entity as a subclass of BFO continuant with one exception... mapping PROV Entity to a subclass of things that are independent continuants and not spatial regions, in a union with generically dependent and specifically dependent continuants in BFO."
  - item: "PROV Activity equivalentClass BFO process"
    chunk: 1
    lines: "682"
    quote: "PROV Activity is mapped as equivalent to the class BFO process."
  - item: "PROV Agent subClassOf BFO material entity"
    chunk: 1
    lines: "654-655"
    quote: "PROV Agent is mapped as a subclass of BFO material entities that both participate in some PROV Activity and bear some BFO role that is realized in a PROV Activity."
  - item: "PROV Agent equivalentClass (CCO Agent AND agent_in some PROV Activity)"
    chunk: 1
    lines: "676-679"
    quote: "A PROV Agent is equivalent to the intersection of CCO agents that are a CCO agent in some PROV Activity."
  - item: "PROV InstantaneousEvent equivalentClass BFO process boundary"
    chunk: 1
    lines: "913-915"
    quote: "PROV InstantaneousEvent, which is equivalently mapped to BFO process boundary since instances of PROV InstantaneousEvent are indivisible boundaries of some PROV Activity."
  - item: "PROV Influence subClassOf (BFO process OR BFO process boundary)"
    chunk: 1
    lines: "911-912"
    quote: "PROV Influence, as the superclass of 16 Qualified Influence classes, is mapped to a subclass of the disjoint union of BFO process and BFO process boundary."
  - item: "PROV Location equivalentClass BFO site"
    chunk: 1
    lines: "808"
    quote: "PROV Location is mapped as equivalent to BFO site."
  - item: "PROV Role subClassOf BFO role"
    chunk: 2
    lines: "109-111"
    quote: "We map PROV Role directly as a subclass of BFO role on the grounds that a PROV Role is externally determined by the context in which the bearer plays the role."
  - item: "PROV Plan subClassOf CCO Information Content Entity"
    chunk: 2
    lines: "116-117"
    quote: "PROV Plan is mapped to a subclass of CCO Information Content Entity."
  - item: "PROV Start equivalentClass CCO process beginning"
    chunk: 2
    lines: "93-94"
    quote: "PROV Start is equivalently mapped to CCO process beginning."
  - item: "PROV End equivalentClass CCO process ending"
    chunk: 2
    lines: "94-95"
    quote: "PROV End is equivalently mapped to CCO process ending."
  - item: "PROV Person equivalentClass (CCO Person AND PROV Agent)"
    chunk: 1
    lines: "773-776"
    quote: "We map PROV Person as equivalent to the intersection of CCO Person and PROV Agent."
  - item: "PROV Organization equivalentClass (CCO Organization AND PROV Agent)"
    chunk: 1
    lines: "787-788"
    quote: "PROV Organization is equivalent to the intersection of CCO Organization and PROV Agent."
  - item: "PROV wasGeneratedBy subPropertyOf BFO participates_in"
    chunk: 1
    lines: "735-740"
    quote: "Since the domain and range of PROV wasGeneratedBy are PROV Entity and PROV Activity, respectively, it is mapped as a subproperty of BFO participates in."
  - item: "PROV wasAssociatedWith subPropertyOf BFO has_participant"
    chunk: 1
    lines: "758-761"
    quote: "This object property is mapped as a subproperty of BFO has participant, which is the inverse of BFO participates in."
  - item: "PROV wasDerivedFrom subPropertyOf RO causally_influenced_by"
    chunk: 1
    lines: "819-821"
    quote: "PROV wasDerivedFrom with domain and range of PROV Entity, which is mapped as a subproperty of RO causally influenced by."

entity_count:
  value: 153
  chunk: 1
  lines: "577-578"
  quote: "A total alignment in the sense of Criterion 4 was achieved by mapping all 153 classes and object properties in PROV-O and its extensions using equivalence and subsumption relations."

abstraction_level: "Top-level/Upper ontology mapping - This paper maps PROV-O (a domain-generic provenance ontology) to BFO (a top-level ontology ISO standard), with extensions to CCO (mid-level ontologies) and RO (relations ontology). The mapping bridges foundational ontological categories (continuant/occurrent) with provenance-specific concepts (Entity/Activity/Agent). Chunk 1:78-84"

framework_comparison:
  - item: "PROV-O vs BFO: Entity/Activity/Agent mapped to continuant/process/material entity"
    chunk: 1
    lines: "636-682"
    quote: "PROV Entity as a subclass of BFO continuant... PROV Activity is mapped as equivalent to the class BFO process... PROV Agent is mapped as a subclass of BFO material entities."
  - item: "PROV-O vs CCO: Agent, Person, Organization, Plan mappings"
    chunk: 1
    lines: "676-679"
    quote: "A PROV Agent is equivalent to the intersection of CCO agents that are a CCO agent in some PROV Activity. The BFO and CCO mappings are both provided for BFO users who are not CCO users."
  - item: "PROV Plan vs CCO Plan: Not equivalent due to scope differences"
    chunk: 2
    lines: "127-143"
    quote: "PROV Plan is not mapped to CCO Plan, though they are similar to some degree. A CCO Plan is a Directive Information Content Entity that prescribes some set of intended CCO Intentional Acts... but PROV Plan is allowed to prescribe activities or processes that are broader than intentional acts."
  - item: "BFO role vs BFO function distinction"
    chunk: 2
    lines: "105-110"
    quote: "BFO distinguishes between roles and functions. While a BFO function must be partially internally determined by the physical make-up of its bearer, a BFO role could be completely externally determined and can be gained or lost by its bearer."
  - item: "PROV Influence as occurrent vs disposition: Divergence from PROV-O definition"
    chunk: 1
    lines: "923-944"
    quote: "In our view, PROV-O authors' conception of influence as capacity is intended to emphasize the dependent nature of PROV Influence... However, the dependent nature of PROV influences is better explained by classifying these as BFO processes or process boundaries that depend on agents through relations such as BFO has participant."
  - item: "PROV-O vs SOSA alignment compatibility"
    chunk: 1
    lines: "439-445"
    quote: "The alignments were further tested for consistency with an alignment between PROV-O and the SOSA (Sensor, Observation, Sample, and Actuator) ontology... No inconsistencies were found when testing our alignments with this alignment plus example SOSA instances."

methodology: "Semi-automated curation leveraging conceptual analysis and semantic web technologies. The approach involves: (1) carefully evaluating necessary and sufficient conditions for class/relation membership, (2) theoretical criteria for alignment (types of mapping relations, coherence/consistency, conservativity, scope), and (3) engineering techniques using SPARQL queries, SWRL rules, HermiT reasoner, and ROBOT tool for verification. Chunk 1:123-131"

ai_integration: "NOT_FOUND"

agent_modeling:
  - item: "PROV Agent as material entity with role participation"
    chunk: 1
    lines: "654-668"
    quote: "PROV Agent is mapped as a subclass of BFO material entities that both participate in some PROV Activity and bear some BFO role that is realized in a PROV Activity. The reason for this mapping is that a PROV Agent always has some matter as a part that persists in time."
  - item: "Software agents as material realizations"
    chunk: 1
    lines: "657-659"
    quote: "This is true even for instances of its subclass, PROV SoftwareAgent, which is defined as 'running software', because every particular instance of a PROV SoftwareAgent is a material realization of some software."
  - item: "Agent responsibility formalized through role realization"
    chunk: 1
    lines: "660-665"
    quote: "The definition of PROV Agent also states that an agent 'bears some form of responsibility for an activity taking place, for the existence of an entity, or another agent's activity'. This is formalized in axioms which entail that every PROV Agent participates in, and bears some role that is realized in, some PROV Activity."
  - item: "Agent as non-intrinsic characteristic"
    chunk: 1
    lines: "706-708"
    quote: "Being an agent is not an intrinsic characteristic of an entity or activity. Instead, it is the very presence of responsibility relations that implies that some entities or activities are also agents."

agentic_workflows: "NOT_FOUND"

generative_ai_patterns: "NOT_FOUND"

agent_ontology_integration: "NOT_FOUND"

empirical_evidence:
  - item: "312 canonical W3C example instances tested"
    chunk: 1
    lines: "426-436"
    quote: "Every canonical example instance from the W3C documentation for PROV-O and its extensions was copied into RDF files... 312 instances were counted, including either named or anonymous individuals represented with blank nodes. The HermiT reasoner tested the consistency of these example instances."
  - item: "Inconsistencies detected in W3C examples"
    chunk: 2
    lines: "229-239"
    quote: "Two examples from the W3C PROV-O documentation were discovered to be inconsistent with PROV-O itself, independently of our alignments."
  - item: "Two alignment-specific inconsistencies found"
    chunk: 2
    lines: "242-258"
    quote: "Two example instances were found to be inconsistent with our PROV-BFO alignment. One is an instance of PROV Entity, a digested protein sample that is related to a different, (non-digested)... This demonstrates how our alignments can be used to find mistakes that are otherwise consistent with PROV-O."

limitations:
  - item: "Data property mappings not computably encoded"
    chunk: 2
    lines: "191-212"
    quote: "While we considered complex mappings for PROV-O data properties, we were unable to encode these in a computable format due to representational limits of OWL, RDF, and SWRL."
  - item: "Total alignment of BFO to PROV-O not possible"
    chunk: 1
    lines: "358-362"
    quote: "BFO represents domains that are not represented in PROV-O, such as those covering spatial and temporal regions. Thus, not every term in BFO can be mapped to some term in PROV-O. A total alignment of BFO to PROV-O, much less a synonymous alignment, is not possible."
  - item: "PROV Agent/Activity disjointness conflicts with PROV requirement VI4"
    chunk: 1
    lines: "694-720"
    quote: "Requirement VI4 in 'The Rationale of PROV', which states: 'prov is to allow agents to be activities'... We decided not to include it, as this would ultimately go against the spirit of BFO's core axiom that continuants and occurrents are disjoint."
  - item: "Complex mappings require SWRL rules with limited support"
    chunk: 1
    lines: "837-880"
    quote: "PROV atLocation is mapped using SWRL rules. Its domain is the union of PROV Agent, PROV Activity, PROV Entity and PROV InstantaneousEvent... In order to map PROV atLocation to both of these object properties, SWRL rules were used to restrict the domain and range of particular instances."

tools_standards:
  - item: "OWL 2 DL (Web Ontology Language)"
    chunk: 1
    lines: "41-43"
    quote: "A popular way to construct ontologies, and the way relevant to this paper, is by leveraging the W3C standards Web Ontology Language (OWL) and Resource Description Framework (RDF)."
  - item: "RDF (Resource Description Framework)"
    chunk: 1
    lines: "42"
    quote: "Resource Description Framework (RDF)"
  - item: "SPARQL queries for verification"
    chunk: 1
    lines: "398-403"
    quote: "A SPARQL query was developed for automatically verifying the Totality of the combined alignments as described in Criterion 4."
  - item: "SWRL rules for complex mappings"
    chunk: 1
    lines: "168-183"
    quote: "SWRL rules are especially useful for restricting the domain or range of an OWL object property in order to use it in a valid mapping. An advantage of SWRL is that it is implemented by semantic reasoners such as HermiT."
  - item: "HermiT reasoner"
    chunk: 1
    lines: "428-431"
    quote: "The HermiT reasoner tested the consistency of these example instances with PROV, BFO, RO, CCO, and the alignments between them. HermiT determines whether a set of OWL 2 DL axioms and assertions are satisfiable."
  - item: "ROBOT command-line tool"
    chunk: 1
    lines: "419"
    quote: "ROBOT command-line tool"
  - item: "GNU Make for pipeline automation"
    chunk: 1
    lines: "470-474"
    quote: "Automated tests for the techniques described above were implemented as part of an ontology engineering pipeline using ROBOT and GNU Make... These Makefile tasks are run within a continuous development pipeline using GitHub Actions."
  - item: "SSSOM (Simple Standard for Sharing Ontology Mappings)"
    chunk: 1
    lines: "546-558"
    quote: "Annotation properties from the Simple Standard for Sharing Ontology Mappings (SSSOM) vocabulary were also used. The SSSOM annotation properties subject label and object label provide convenient, human friendly references."
  - item: "SKOS vocabulary"
    chunk: 1
    lines: "186-195"
    quote: "Mapping predicates from the SKOS vocabulary represent informal relations between terms which may be interpreted by users to be intuitively similar."
  - item: "RDF Turtle serialization"
    chunk: 1
    lines: "426"
    quote: "RDF files serialized in the Terse Triple Language (TTL or 'RDF Turtle')"
  - item: "Protege ontology editor"
    chunk: 1
    lines: "571"
    quote: "For viewing the alignments in context in Protege and for testing with reasoners and SPARQL queries."
  - item: "GitHub Actions for CI/CD"
    chunk: 1
    lines: "473-474"
    quote: "These Makefile tasks are run within a continuous development pipeline using GitHub Actions."
---

# A semantic approach to mapping the Provenance Ontology to Basic Formal Ontology

## Summary

This paper presents a comprehensive semantic mapping between PROV-O (the W3C Provenance Ontology) and BFO (Basic Formal Ontology), including extensions to CCO (Common Core Ontologies) and RO (OBO Relations Ontology). The work addresses the ontology silo problem by creating a total alignment of all 153 classes and object properties in PROV-O and its extensions (PROV-AQ, PROV-Dictionary, PROV-Links, PROV-Inverses, PROV Dublin Core) to BFO-based ontologies.

## Key Contributions

### 1. Alignment Methodology
The paper establishes four criteria for ontology alignment:
- **Types of Mapping Relations**: Equivalence (owl:equivalentClass, owl:equivalentProperty) and subsumption (rdfs:subClassOf, rdfs:subPropertyOf)
- **Coherence and Consistency**: All formulae satisfiable, no contradictions
- **Conservativity**: No changes to semantic relationships within each ontology
- **Scope**: Total alignment with interpretability toward synonymy

### 2. Core Entity Mappings

| PROV-O Term | BFO/CCO Mapping | Relation Type |
|-------------|-----------------|---------------|
| PROV Entity | BFO continuant (non-spatial) | subClassOf |
| PROV Activity | BFO process | equivalentClass |
| PROV Agent | BFO material entity (with role) | subClassOf |
| PROV Agent | CCO Agent (in Activity) | equivalentClass |
| PROV InstantaneousEvent | BFO process boundary | equivalentClass |
| PROV Location | BFO site | equivalentClass |
| PROV Role | BFO role | subClassOf |
| PROV Plan | CCO Information Content Entity | subClassOf |

### 3. The Agent-Activity-Entity Triad
The paper validates the fundamental Agent-Activity-Entity triad pattern:
- **Entity**: Things with fixed aspects that persist through time (continuants)
- **Activity**: Processes that occur over time and act upon entities (occurrents)
- **Agent**: Material entities bearing roles realized in activities

### 4. Technical Implementation
- 35 terms explicitly mapped to BFO (6 equivalence, 24 subsumption, 8 SWRL rules)
- 37 terms explicitly mapped to CCO (5 equivalence, 23 subsumption, 1 property chain, 6 SWRL rules)
- 25 terms explicitly mapped to RO (26 subsumption relations)
- Verified against 312 canonical W3C example instances

### 5. Inconsistencies Detected
The alignment revealed errors in W3C documentation:
- Two examples inconsistent with PROV-O itself
- Two examples inconsistent with the PROV-BFO alignment
- Demonstrates value of upper ontology alignment for data quality

## Relevance to Research Questions

### Entity Types Universal Across Foundational Ontologies
Confirms the Agent-Activity-Entity pattern maps to BFO's continuant/occurrent distinction, validating cross-ontology universality.

### Agent-Activity-Entity Triad Manifestation
The mapping shows how this triad manifests differently:
- PROV: Agent can potentially be Activity (Requirement VI4)
- BFO: Agent (continuant) disjoint from Activity (occurrent)
- The paper chose BFO's stricter interpretation

### Abstraction Level and Entity Count
153 terms in PROV-O extensions mapped, demonstrating how domain-specific provenance concepts specialize foundational categories.

## Limitations

1. Data property mappings could not be encoded computably due to OWL/RDF limitations
2. PROV requirement VI4 (agents as activities) conflicts with BFO's continuant/occurrent disjointness
3. Total BFO-to-PROV-O alignment not achievable (BFO has domains not in PROV-O)

## Resources

- GitHub: https://github.com/BFO-Mappings/PROV-to-BFO
- Zenodo: https://doi.org/10.5281/zenodo.14692262
- DOI: https://doi.org/10.1038/s41597-025-04580-1
