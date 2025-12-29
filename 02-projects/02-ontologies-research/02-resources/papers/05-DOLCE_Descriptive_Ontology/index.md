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
year: 2021
chunks_expected: 2
chunks_read: 2
analysis_complete: true
high_priority_fields_found: 7

# Extraction fields
entity_types:
  - "Endurant (Continuant)"
  - "Perdurant (Occurrent)"
  - "Quality"
  - "Abstract"
  - "Physical Object (POB)"
  - "Agentive Physical Object (APO)"
  - "Non-Agentive Physical Object"
  - "Feature"
  - "Process (PRO)"
  - "Event"
  - "Achievement"
  - "Accomplishment (ACC)"
  - "State"
  - "Concept (C)"
  - "Role (RL)"
  - "Artifact"
  - "Physical Quality (PQ)"
  - "Temporal Quality (TQ)"
  - "Abstract Quality (AQ)"
  - "Quale"
  - "Quality Space/Region"
  - "Matter (M)"
  - "Social Object (SOB)"
  - "Non-Agentive Social Object (NASO)"

entity_definitions:
  Endurant: "An entity wholly present (i.e., with all its parts) at any time in which it is present. Examples: table, person, cat, planet. (Chunk 1:128-133)"
  Perdurant: "An entity that can be partially present, so that at any time in which it unfolds only a part of it is present. Examples: tennis match, conference talk, manufacturing process. (Chunk 1:131-133)"
  Quality: "What can be perceived and measured; particulars inhering in endurants or perdurants. They are specific to their bearers (individual qualities). (Chunk 1:168-172)"
  Quale: "The position occupied by an individual quality within a quality space. Enables comparison of qualities of the same kind. (Chunk 1:178-181)"
  Abstract: "Entities that have neither spatial nor temporal qualities and are not qualities themselves. Examples: quality regions, sets, facts. (Chunk 1:216-218)"
  Role: "Concepts that are anti-rigid and founded, meaning they have dynamic properties and relational nature - depend on other roles and contexts. (Chunk 1:187-189)"
  Participation: "The relation connecting endurants and perdurants. An endurant can be in time by participating in a perdurant, and perdurants happen by having endurants as participants. (Chunk 1:134-137)"
  Constitution: "A temporalized relation holding between either endurants or perdurants. Used to single out entities that are spatio-temporally co-located but distinguishable by histories or persistence conditions. (Chunk 1:208-213)"
  Process: "A stative perdurant that is cumulative but not homeomeric - has parts of different types. (Chunk 1:160-161)"
  Achievement: "An eventive occurrence that is atomic. (Chunk 1:162-163)"
  Accomplishment: "An eventive occurrence that is not atomic. (Chunk 1:162-163)"
  Agentive_Physical_Object: "A physical object with agentive capacity (APO). Examples: persons. (Chunk 1:751)"

entity_relationships:
  - from: "Endurant"
    to: "Perdurant"
    relationship: "participates (PC)"
    source: "Chunk 1:365-368"
  - from: "Endurant"
    to: "Endurant"
    relationship: "constitutes (K)"
    source: "Chunk 1:386-396"
  - from: "Perdurant"
    to: "Perdurant"
    relationship: "constitutes (K)"
    source: "Chunk 1:390-391"
  - from: "Endurant"
    to: "Endurant"
    relationship: "parthood (P) - time-indexed"
    source: "Chunk 1:206-207"
  - from: "Perdurant"
    to: "Perdurant"
    relationship: "parthood (P) - atemporal"
    source: "Chunk 1:206-207"
  - from: "Quality"
    to: "Endurant/Perdurant"
    relationship: "inheres in (qt)"
    source: "Chunk 1:305-306"
  - from: "Quality"
    to: "Quale"
    relationship: "has quale (ql)"
    source: "Chunk 1:316-317"
  - from: "Concept"
    to: "Endurant"
    relationship: "classifies (CF)"
    source: "Chunk 1:408-409"
  - from: "Role"
    to: "Entity"
    relationship: "classifies (CF) - anti-rigid"
    source: "Chunk 1:427-428"

abstraction_level: "foundational"

framework_comparison:
  - compared_to: "ISO 21838"
    relationship: "becoming_part_of"
    details: "DOLCE is becoming part of the ISO 21838 standard under development"
    source: "Chunk 1:109-111"
  - compared_to: "CIDOC CRM"
    relationship: "influenced"
    details: "DOLCE has been used to develop or improve CIDOC CRM"
    source: "Chunk 1:18-19"
  - compared_to: "DBpedia"
    relationship: "improved"
    details: "Used to identify and fix millions of inconsistencies in DBpedia"
    source: "Chunk 2:456-458"
  - compared_to: "WordNet"
    relationship: "improved"
    details: "Used to reorganize WordNet top level and include individual/class distinction"
    source: "Chunk 2:459-461"
  - compared_to: "SSN (Semantic Sensor Network)"
    relationship: "compatible"
    details: "SSN is based on or compatible with DUL"
    source: "Chunk 2:463"
  - compared_to: "SAREF"
    relationship: "compatible"
    details: "SAREF is based on or compatible with DUL"
    source: "Chunk 2:465"
  - compared_to: "BFO/DOLCE-CORE"
    relationship: "related_terminology"
    details: "DOLCE-CORE uses 'object' and 'event' instead of 'endurant' and 'perdurant'"
    source: "Chunk 1:87-89"

ai_integration: "N/A - paper predates LLM/AI integration discussion (foundational ontology paper focused on formal axiomatization)"

agent_modeling:
  - aspect: "Agentive vs Non-Agentive distinction"
    description: "Physical objects are classified as agentive (APO) or non-agentive, distinguishing entities with agency"
    source: "Chunk 1:751"
  - aspect: "Role-based classification"
    description: "Agents can have roles temporarily - roles are anti-rigid and founded, can be acquired and lost, depend on context"
    source: "Chunk 1:719-721"
  - aspect: "Participation in events"
    description: "Agents (endurants) exist in time through participation in perdurants. Every endurant participates in at least one perdurant"
    source: "Chunk 1:366-368"
  - aspect: "Functional roles"
    description: "Functional roles can classify only one entity at each time (e.g., teacher role)"
    source: "Chunk 1:777"

agentic_workflows: "N/A - paper predates agentic workflow discussion"

generative_ai_patterns: "N/A - paper predates generative AI patterns"

agent_ontology_integration: "N/A - paper predates AI agent ontology integration patterns"

entity_count:
  count: 24
  rationale: "Core foundational categories plus subcategories for physical objects, perdurants, qualities, and social entities"
  source: "Chunk 1:121-125"

methodology: "top-down"

empirical_evidence:
  - type: "Standard adoption"
    description: "ISO 21838 standardization, CIDOC CRM, SSN, SAREF compatibility"
    source: "Chunk 2:462-465"
  - type: "Knowledge graph improvement"
    description: "Fixed millions of inconsistencies in DBpedia"
    source: "Chunk 2:456-458"
  - type: "Lexical resource improvement"
    description: "WordNet top level reorganization"
    source: "Chunk 2:459-461"
  - type: "Domain applications"
    description: "25+ large ontology projects in e-learning, medicine, law, robotics, industry, etc."
    source: "Chunk 2:451-455"

limitations:
  - "Non-computable due to rich axiomatization in first-order modal logic - requires 'lite' versions for applications (Chunk 1:60-62)"
  - "Not directly used for applications - provides conceptual handles rather than operational ontology (Chunk 1:100-102)"
  - "Requires approximated and partial translations for application-oriented languages (Chunk 1:61-62)"

tools_standards:
  - "First-order modal logic QS5"
  - "OWL (multiple versions: DOLCE-lite, DOLCE-ultralite, DOLCE-zero)"
  - "CLIF (Common Logic ISO 24707)"
  - "DOLCE+D&S Ultralite (DUL)"
  - "OWL2"
  - "General Extensional Mereology (GEM)"
---

# DOLCE: A Descriptive Ontology for Linguistic and Cognitive Engineering - Analysis Index

## Paper Overview

- **Source**: 05-DOLCE_Descriptive_Ontology.pdf
- **Chunks**: 2 chunks, ~20,741 estimated tokens
- **Analyzed**: 2025-12-28T14:45:00

## Key Extractions

DOLCE (Descriptive Ontology for Linguistic and Cognitive Engineering) is the first top-level foundational ontology to be axiomatized, remaining stable for 20 years. It adopts a descriptive metaphysics grounded in natural language, cognition, and social practices. The ontology is formalized in first-order quantified modal logic QS5.

### Entity Types (Chunk 1:121-125)

The core taxonomy comprises four basic categories:

| Entity Type | Description | Source |
|-------------|-------------|--------|
| Endurant | Wholly present at any time of existence | Chunk 1:128-133 |
| Perdurant | Unfolds in time, only partially present | Chunk 1:131-133 |
| Quality | Perceivable/measurable, inheres in bearers | Chunk 1:168-172 |
| Abstract | No spatial/temporal qualities | Chunk 1:216-218 |

### Entity Relationships (Chunk 1:206-430)

| Relationship | Description | Source |
|--------------|-------------|--------|
| Participation (PC) | Connects endurants to perdurants at a time | Chunk 1:365-368 |
| Constitution (K) | Spatio-temporal co-location with different persistence | Chunk 1:208-213 |
| Parthood (P) | Time-indexed for endurants, atemporal for perdurants | Chunk 1:206-207 |
| Quality of (qt) | Primitive relation for quality inherence | Chunk 1:305-306 |
| Classification (CF) | Concepts/roles classifying entities at a time | Chunk 1:408-409 |

### Perdurant Subtypes (Chunk 1:156-163)

| Subtype | Cumulative | Homeomeric | Atomic |
|---------|-----------|------------|--------|
| State | Yes | Yes | - |
| Process | Yes | No | - |
| Achievement | No | - | Yes |
| Accomplishment | No | - | No |

### Role Modeling (Chunk 1:719-777)

- **Anti-rigidity**: Roles can be acquired and lost at will
- **Foundedness**: Roles depend on external context/entities
- **Functional roles**: Can classify only one entity at a time (e.g., "the teacher of class 2C")

### Framework Impact (Chunk 2:456-465)

DOLCE has influenced or improved:
- ISO 21838 standard (under development)
- CIDOC CRM (cultural heritage)
- SSN (Semantic Sensor Network)
- SAREF (Smart Reference Ontology)
- DBpedia (millions of inconsistencies fixed)
- WordNet (top-level reorganization)

### Key Findings (with evidence)

- **Foundational purpose** (Chunk 1:19-22): "Its purpose is to provide the general categories and relations needed to give a coherent view of reality, to integrate domain knowledge, and to mediate across domains"

- **Endurant-Perdurant distinction** (Chunk 1:128-131): "endurants are wholly present (i.e., with all their parts) at any time in which they are present; differently, perdurants can be partially present"

- **Participation as central relation** (Chunk 1:134-137): "An endurant can be in time by participating in a perdurant, and perdurants happen in time by having endurants as participants"

- **20 years of stability** (Chunk 1:22-23): "DOLCE has shown that applied ontologies can be stable and that interoperability across reference and domain ontologies is a reality"

## Chunk Navigation

### Chunk 1: Foundational Categories and Formalization

- **Summary**: Introduces DOLCE's history, core categories (Endurant, Perdurant, Quality, Abstract), and provides formal axiomatization in first-order logic including mereology, quality/quale, participation, constitution, and role classification. Includes modeling examples for composition/constitution, roles, and property change.
- **Key concepts**: [Endurant, Perdurant, Quality, Abstract, Participation, Constitution, Parthood, Role, OntoClean, First-order modal logic QS5]
- **Key quotes**:
  - Line 13-14: "DOLCE, the first top-level (foundational) ontology to be axiomatized"
  - Line 128-130: "endurants are wholly present (i.e., with all their parts) at any time in which they are present"
  - Line 134-135: "The relation connecting endurants and perdurants is called participation"
- **Load when**: "Query about DOLCE entity types" / "User asks about endurant vs perdurant distinction" / "Question about foundational ontology categories" / "Need formal definitions of ontological primitives"

### Chunk 2: Modeling Examples and Community Impact

- **Summary**: Continues modeling examples (speed change, event change, concept evolution), then describes DOLCE's usage in the community including OWL versions (DUL), application to DBpedia and WordNet, and compatibility with standards like CIDOC CRM, SSN, and SAREF. Concludes with references.
- **Key concepts**: [DOLCE+D&S Ultralite (DUL), OWL2, Semantic Web, DBpedia, WordNet, CIDOC CRM, SSN, SAREF, Ontology design patterns, Concept evolution]
- **Key quotes**:
  - Line 456-458: "identifying and fixing millions of inconsistencies in DBpedia"
  - Line 468-476: "DOLCE can be used to foster different design approaches: as an upper ontology... as an expressive axiomatic theory... as a coherence/consistency stabilizer... as a source of patterns"
- **Load when**: "Query about DOLCE applications" / "User asks about OWL implementations of DOLCE" / "Question about DUL ontology" / "Need information on DOLCE's influence on standards"
