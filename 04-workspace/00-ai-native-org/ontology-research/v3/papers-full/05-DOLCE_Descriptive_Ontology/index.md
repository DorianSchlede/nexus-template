---
paper_id: "05-DOLCE_Descriptive_Ontology"
title: "DOLCE: A Descriptive Ontology for Linguistic and Cognitive Engineering"
authors:
  - "Stefano Borgo"
  - "Roberta Ferrario"
  - "Aldo Gangemi"
  - "Nicola Guarino"
  - "Claudio Masolo"
  - "Daniele Porello"
  - "Emilio M. Sanfilippo"
  - "Laure Vieu"
year: 2003
chunks_expected: 2
chunks_read: 2
analysis_complete: true
schema_version: "2.3"

chunk_index:
  1:
    token_count: 12168
    fields_found:
      entity_types: true
      entity_definitions: true
      entity_relationships: true
      entity_count: partial
      abstraction_level: true
      framework_comparison: partial
      methodology: true
      ai_integration: false
      agent_modeling: true
      agentic_workflows: false
      generative_ai_patterns: false
      agent_ontology_integration: false
      empirical_evidence: partial
      limitations: true
      tools_standards: true
  2:
    token_count: 7760
    fields_found:
      entity_types: partial
      entity_definitions: partial
      entity_relationships: partial
      entity_count: false
      abstraction_level: partial
      framework_comparison: true
      methodology: false
      ai_integration: partial
      agent_modeling: false
      agentic_workflows: false
      generative_ai_patterns: false
      agent_ontology_integration: false
      empirical_evidence: true
      limitations: false
      tools_standards: true

entity_types:
  - item: "Endurant (Continuant)"
    chunk: 1
    lines: "121-122"
    quote: "the basic categories of DOLCE are endurant (aka continuant), perdurant (occurrent), quality, and abstract."
  - item: "Perdurant (Occurrent)"
    chunk: 1
    lines: "121-122"
    quote: "the basic categories of DOLCE are endurant (aka continuant), perdurant (occurrent), quality, and abstract."
  - item: "Quality"
    chunk: 1
    lines: "121-122"
    quote: "the basic categories of DOLCE are endurant (aka continuant), perdurant (occurrent), quality, and abstract."
  - item: "Abstract"
    chunk: 1
    lines: "121-122"
    quote: "the basic categories of DOLCE are endurant (aka continuant), perdurant (occurrent), quality, and abstract."
  - item: "Physical Object (POB)"
    chunk: 1
    lines: "149-150"
    quote: "features (e.g., edges, holes, bumps, etc.) are endurants whose existence depends on some physical object (the feature bearer), while physical objects are independent entities"
  - item: "Process"
    chunk: 1
    lines: "156-162"
    quote: "In DOLCE processes and events are special types of perdurants...processes are cumulative but not homeomeric"
  - item: "Event (Accomplishment/Achievement)"
    chunk: 1
    lines: "162-163"
    quote: "eventive occurrences (events) are not cumulative, and they are called achievements if they are atomic, otherwise they are accomplishments"
  - item: "State"
    chunk: 1
    lines: "159-160"
    quote: "Common examples of stative perdurants are states; e.g., a sitting state is stative because the sum of two sittings is still a sitting"
  - item: "Concept"
    chunk: 1
    lines: "245-246"
    quote: "we include in this paper the categories Concept and Role as specializations of Non-Agentive Social Object"
  - item: "Role"
    chunk: 1
    lines: "184-189"
    quote: "Roles are represented as (social) concepts, which are connected to other entities...roles are concepts that are anti-rigid and founded"
  - item: "Artefact"
    chunk: 1
    lines: "246-247"
    quote: "the category Artefact as specialization of Non-Agentive Physical Object"
  - item: "Quale"
    chunk: 1
    lines: "178-181"
    quote: "A quale is the position occupied by an individual quality within a quality space...if the rose and the book cover exhibit the same shade of red, their individual colors occupy the same position (quale) in the color space"
  - item: "Matter"
    chunk: 1
    lines: "500-501"
    quote: "matter (M), physical object (POB), and Time (T)"
  - item: "Agentive Physical Object (APO)"
    chunk: 1
    lines: "751"
    quote: "agentive physical object (APO), non-agentive social object (NASO), and Time (T)"
  - item: "Non-Agentive Social Object (NASO)"
    chunk: 1
    lines: "751"
    quote: "agentive physical object (APO), non-agentive social object (NASO), and Time (T)"

entity_definitions:
  Endurant: "Entities that are wholly present (i.e., with all their parts) at any time in which they are present. Examples include a table, a person, a cat, or a planet. (Chunk 1:128-133)"
  Perdurant: "Entities that can be partially present, so that at any time in which they unfold only a part of them is present. Examples include a tennis match, a conference talk or a manufacturing process. (Chunk 1:128-133)"
  Quality: "What can be perceived and measured; they are particulars inhering in endurants or perdurants. For example, when we talk about the red of a rose, we are talking about a particular quality which inheres in a particular endurant. (Chunk 1:166-172)"
  Abstract: "Entities that have neither spatial nor temporal qualities and are not qualities themselves. Examples include quality regions, quality spaces, sets, and facts. (Chunk 1:216-219)"
  Quale: "The position occupied by an individual quality within a quality space. If two objects exhibit the same shade of red, their individual colors occupy the same position (quale) in the color space. (Chunk 1:178-181)"
  Role: "Concepts that are anti-rigid and founded, meaning (i) they have dynamic properties and (ii) they have a relational nature depending on other roles and on contexts. (Chunk 1:187-189)"
  Process: "Perdurants that are cumulative but not homeomeric, namely, they have parts of different types; e.g., there are temporal parts of a running that are not themselves runnings. (Chunk 1:160-162)"
  Achievement: "Eventive occurrences (events) that are atomic. (Chunk 1:162-163)"
  Accomplishment: "Eventive occurrences (events) that are not atomic. (Chunk 1:162-163)"
  Constitution: "Temporalized relation holding between entities with different essential properties (intercategorical) like the dependence of a table from the matter it is made of. (Chunk 1:486-491)"
  Participation: "The relation connecting endurants and perdurants. An endurant can be in time by participating in a perdurant, and perdurants happen in time by having endurants as participants. (Chunk 1:134-137)"

entity_relationships:
  - item: "Participation (PC)"
    chunk: 1
    lines: "134-137, 365-377"
    quote: "The relation connecting endurants and perdurants is called participation. An endurant can be in time by participating in a perdurant, and perdurants happen in time by having endurants as participants."
  - item: "Parthood (P) - Temporal"
    chunk: 1
    lines: "206-207, 253-265"
    quote: "An important relation in DOLCE is parthood, which is time-indexed when connecting endurants and a-temporal when holding between perdurants or abstracts"
  - item: "Constitution (K)"
    chunk: 1
    lines: "208-214, 386-396"
    quote: "Constitution is another temporalized relation in DOLCE, holding between either endurants or perdurants. It is often used to single out entities that are spatio-temporally co-located but nonetheless distinguishable for their histories, persistence conditions, or relational properties."
  - item: "Quality Inherence (qt)"
    chunk: 1
    lines: "305-306, 341"
    quote: "The relation being a quality of (qt) is primitive in DOLCE...a quality inheres in one and only one entity"
  - item: "Classification (CF)"
    chunk: 1
    lines: "405-430"
    quote: "The classification relationship CF applies to an endurant, a concept and a time, requires the endurant to be present when it is classified, and is not symmetrical"
  - item: "Being Present (PRE)"
    chunk: 1
    lines: "352-359"
    quote: "Actual existence in DOLCE is represented by means of the being present at (PRE) relation. The assumption here is that things exist if they have a temporal quale."
  - item: "Constant Participation (PCC)"
    chunk: 1
    lines: "369-380"
    quote: "the relation of constant participation (PCC)...participation during the whole perdurant"
  - item: "Quale (ql)"
    chunk: 1
    lines: "316-327"
    quote: "DOLCE defines the temporal quale (relation ql), i.e., the position occupied by an individual quality within a quality space"

abstraction_level: "Foundational (top-level) ontology. DOLCE is not directly concerned with domain knowledge. Its purpose is to provide the general categories and relations needed to give a coherent view of reality, to integrate domain knowledge, and to mediate across domains. (Chunk 1:19-22)"

framework_comparison:
  - item: "OntoClean methodology integration"
    chunk: 1
    lines: "73-75"
    quote: "The analysis underlying the formalization of DOLCE leverages the techniques of ontological engineering and the study of classes' meta-properties of the OntoClean methodology"
  - item: "DOLCE-CORE simplification"
    chunk: 1
    lines: "79-89"
    quote: "In 2009, DOLCE-CORE was introduced...the most basic categories, which in DOLCE were called 'endurant' and 'perdurant' and which become 'object' and 'event' in DOLCE-CORE"
  - item: "DOLCE+D&S Ultralite (DUL)"
    chunk: 2
    lines: "432-449"
    quote: "DOLCE+D&S Ultralite (DUL) OWL ontology was intended to popularize DOLCE to the Semantic Web community. DUL uses DOLCE, D&S, and a few more ontology design patterns"
  - item: "Alignment with CIDOC CRM"
    chunk: 2
    lines: "463-465"
    quote: "Several other standard or de facto standard are based on or compatible with DUL, e.g., CIDOC CRM (CIDOC Conceptual Reference Model)"
  - item: "Alignment with SSN"
    chunk: 2
    lines: "463-465"
    quote: "SSN (Semantic Sensor Network Ontology)"
  - item: "Alignment with SAREF"
    chunk: 2
    lines: "463-465"
    quote: "SAREF (Smart REFerence Ontology)"
  - item: "DBpedia improvement"
    chunk: 2
    lines: "456-458"
    quote: "DUL has been applied as a tool to improve existing semantic resources. This has happened for example in identifying and fixing millions of inconsistencies in DBpedia"
  - item: "WordNet integration"
    chunk: 2
    lines: "459-461"
    quote: "the very inception of DOLCE, used to reorganize the WordNet top level and causing Princeton WordNet developers to include the individual/class distinction in their lexicon"
  - item: "ISO 21838 standardization"
    chunk: 1
    lines: "109-111"
    quote: "Today DOLCE is becoming part of the ISO 21838 standard, under development, and is available also in CLIF, a syntax of Common Logic ISO 24707"

ai_integration:
  - item: "Computer vision integration"
    chunk: 1
    lines: "96-97"
    quote: "Others showed a possible integration with machine learning and in particular computer vision (Conigliaro et al., 2017)"
  - item: "Knowledge graph support"
    chunk: 2
    lines: "479-481"
    quote: "Especially (3) and (4) are central to the current needs of the huge knowledge graphs maintained by the Web stakeholders"

agent_modeling:
  - item: "Agentive Physical Object category"
    chunk: 1
    lines: "751, 987"
    quote: "Person(x) -> APO(x) - The formulas above state that a person is an agentive physical object"
  - item: "Role-based agent modeling"
    chunk: 1
    lines: "719-748"
    quote: "Roles are properties that an entity can have temporarily (roles can be acquired and lost at will), and they depend on an external entity, often indicated as the context"
  - item: "Functional role constraints"
    chunk: 1
    lines: "774-777"
    quote: "Formula (12) states that a functional role (y) can classify only one entity at each time."

agentic_workflows: "NOT_FOUND"

generative_ai_patterns: "NOT_FOUND"

agent_ontology_integration: "NOT_FOUND"

entity_count: "Four basic categories (endurant, perdurant, quality, abstract) with multiple subcategories forming a rich taxonomy. The paper does not provide a precise entity count but references the taxonomy in Figure 1. (Chunk 1:121-122)"

methodology: "Top-down theoretical approach grounded in philosophical principles. DOLCE adopts a descriptive (rather than referentialist) metaphysics, making explicit already existing conceptualizations through categories influenced by natural language, human cognition, and social practices. Formalized in first-order quantified modal logic QS5. (Chunk 1:39-43, 227-230)"

empirical_evidence:
  - item: "DBpedia inconsistency detection"
    chunk: 2
    lines: "456-458"
    quote: "identifying and fixing millions of inconsistencies in DBpedia, on-the-go discovering modelling anti-patterns that were completely opaque to the axioms of the DBpedia ontology"
  - item: "WordNet top-level reorganization"
    chunk: 2
    lines: "459-461"
    quote: "used to reorganize the WordNet top level and causing Princeton WordNet developers to include the individual/class distinction in their lexicon"
  - item: "Application domains"
    chunk: 2
    lines: "451-455"
    quote: "25 large ontology projects for: e-learning systems, water quality systems; in multimedia: annotation facets, content annotation, audiovisual formal descriptions; in medicine...law; events; geo-spatial data; robotics and automation; industry and smart products, textile manufacturing; cybersecurity; enterprise integration; process mining"
  - item: "20-year stability"
    chunk: 1
    lines: "13-14"
    quote: "DOLCE, the first top-level (foundational) ontology to be axiomatized, has remained stable for twenty years"

limitations:
  - item: "Computability trade-off"
    chunk: 1
    lines: "60-62"
    quote: "Such richness greatly enhances expressiveness but, on the other hand, it makes foundational ontologies non computable, due to the well-known trade-off between formal expressiveness and computability"
  - item: "Not directly used for applications"
    chunk: 1
    lines: "100-102"
    quote: "Given the emphasis on formal expressivity, recall that foundational ontologies are not directly used for applications; rather, they provide conceptual handles to solve cases of misunderstandings"
  - item: "Categories may evolve"
    chunk: 1
    lines: "41-43"
    quote: "such categories are mostly situated at a mesoscopic level, and may change while scientific knowledge or social consensus evolve"

tools_standards:
  - item: "First-Order Modal Logic QS5"
    chunk: 1
    lines: "227-230"
    quote: "The formal theory of DOLCE is written in the first-order quantified modal logic QS5, including the Barcan and the converse Barcan formula"
  - item: "CLIF (Common Logic)"
    chunk: 1
    lines: "109-111"
    quote: "available also in CLIF, a syntax of Common Logic ISO 24707 (2018)"
  - item: "OWL versions"
    chunk: 1
    lines: "69-70"
    quote: "several application-oriented, 'lite' versions were later published, including DOLCE-lite, DOLCE-ultralite, and DOLCE-zero"
  - item: "OWL2 DUL"
    chunk: 2
    lines: "432-449"
    quote: "DOLCE+D&S Ultralite (DUL) OWL ontology...semantic-web-oriented OWL2 modeling styles"
  - item: "ISO 21838 standardization"
    chunk: 1
    lines: "109-110"
    quote: "Today DOLCE is becoming part of the ISO 21838 standard, under development"
  - item: "D&S (Description and Situations) pattern"
    chunk: 2
    lines: "428-431"
    quote: "reusing the D&S (Description and Situations) ontology pattern framework, which was early designed to overcome the expressivity limits of OWL"
  - item: "Framester knowledge graph"
    chunk: 2
    lines: "461-462"
    quote: "the recent massive Framester knowledge graph (Gangemi et al., 2016), which unifies many different linguistic databases under a frame semantics"
  - item: "General Extensional Mereology (GEM)"
    chunk: 1
    lines: "264-265"
    quote: "The first follows the principles of the General Extensional Mereology (GEM)"
  - item: "OntoClean methodology"
    chunk: 1
    lines: "73-75"
    quote: "the study of classes' meta-properties of the OntoClean methodology, firstly developed in the early 2000s by Guarino and Welty"
---

# DOLCE: A Descriptive Ontology for Linguistic and Cognitive Engineering

## Summary

DOLCE (Descriptive Ontology for Linguistic and Cognitive Engineering) is the first top-level (foundational) ontology to be axiomatized, remaining stable for twenty years. It is inspired by cognitive and linguistic considerations and aims to model a commonsense view of reality. DOLCE provides general categories and relations needed to give a coherent view of reality, integrate domain knowledge, and mediate across domains.

## Key Contributions

1. **Foundational Ontology Framework**: Four basic categories (endurant, perdurant, quality, abstract) with rich subcategorization and formal axiomatization in first-order modal logic QS5.

2. **Endurant/Perdurant Distinction**: Clear distinction between entities wholly present at any time (endurants) and entities that unfold through time (perdurants), connected via the participation relation.

3. **Quality and Quale Theory**: Individual qualities as particulars inhering in entities, with qualia as positions in quality spaces enabling comparison across instances.

4. **Role and Concept Formalization**: Roles as anti-rigid, founded concepts that classify entities temporally, enabling dynamic property modeling.

5. **Multiple Modeling Approaches**: Support for artifact-based and role-based modeling approaches depending on application needs.

## Relevance to Research Questions

### Entity Types and Definitions
DOLCE provides a comprehensive taxonomy of entity types with formal definitions distinguishing:
- Endurants vs. Perdurants (presence in time)
- Independent vs. Dependent entities
- Processes vs. Events (stative vs. eventive perdurants)
- Physical vs. Abstract qualities

### Framework Comparison
DOLCE has influenced and aligned with multiple standards:
- CIDOC CRM (cultural heritage)
- SSN (Semantic Sensor Network)
- SAREF (Smart Applications)
- DBpedia and WordNet improvements

### Agent Modeling
Provides agent modeling through:
- Agentive Physical Object (APO) category
- Role-based agent representation
- Classification relation for temporal property assignment
- Functional role constraints

### AI Integration
Minimal direct AI integration, though:
- Computer vision integration demonstrated
- Knowledge graph support for semantic web applications
- No LLM/agentic workflow patterns present

## Mapping to 8-Entity Hypothesis

| Hypothesis Entity | DOLCE Mapping | Notes |
|-------------------|---------------|-------|
| Agent | Agentive Physical Object (APO) | Persons, autonomous entities |
| Activity/Task | Perdurant (Process, Accomplishment) | Events that unfold in time |
| Goal | Plan (Concept subcategory) | Via D&S extension |
| Role | Role (Concept subcategory) | Anti-rigid, founded concepts |
| Resource | Physical Object / Matter | Material entities |
| Data | Abstract / Quality | Non-temporal entities |
| Event | Achievement / Accomplishment | Atomic vs. non-atomic occurrences |
| Rule | Concept | Social/legal constraints |

## Technical Implementation

- **Formalization**: First-order modal logic QS5 with Barcan formulas
- **OWL Versions**: DOLCE-lite, DOLCE-ultralite, DOLCE-zero, DUL
- **Standards**: ISO 21838 (in development), CLIF (Common Logic ISO 24707)
- **Patterns**: D&S (Description and Situations), Plan, Information Object, Collection

## Limitations for AI/Agent Research

1. No direct support for AI agent reasoning patterns
2. No LLM integration or generative AI considerations
3. Non-computable in full form due to expressivity
4. Requires "lite" versions for practical applications
5. No agentic workflow or multi-agent system patterns
