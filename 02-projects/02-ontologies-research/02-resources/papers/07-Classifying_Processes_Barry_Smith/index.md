---
paper_id: "07-Classifying_Processes_Barry_Smith"
title: "Classifying Processes: An Essay in Applied Ontology"
authors: ["Barry Smith"]
year: 2012
chunks_expected: 2
chunks_read: 2
analysis_complete: true
high_priority_fields_found: 7

# HIGH PRIORITY EXTRACTIONS

entity_types:
  - "Continuant"
  - "Occurrent"
  - "Independent Continuant"
  - "Dependent Continuant"
  - "Quality"
  - "Disposition"
  - "Process"
  - "Process Boundary"
  - "Spatiotemporal Region"
  - "Temporal Region"
  - "Process Profile"
  - "Generically Dependent Continuant"
  - "Specifically Dependent Continuant"

entity_definitions:
  Continuant: "Entities which can be sliced to yield parts only along the spatial dimension; they have no parts along the time axis (Chunk 1:350-354, 398-402)"
  Occurrent: "An entity that exists in its entirety in the area defined by its spatiotemporal boundaries, where each part of this area contains a part of the whole entity (Chunk 1:376-378)"
  Process: "Changes in independent continuant entities which are their participants; occurrents that are temporally extended (Chunk 1:691-692)"
  Process_Profile: "That part of a process which serves as the target of selective abstraction focused on a sequence of instances of determinate qualities (Chunk 2:152-157)"
  Quality: "A dependent continuant that does not require a process of realization; first-class entities dependent on independent continuants (Chunk 1:408-409, 458-459)"
  Disposition: "A dependent continuant that requires a process (e.g., dissolving) to be realized or manifested (Chunk 1:405-407)"
  Independent_Continuant: "Substances such as molecules, organisms, planets - bearers of dependent entities (Chunk 1:499)"
  Dependent_Continuant: "Entities dependent on independent continuants, including qualities and dispositions (Chunk 1:405-409)"
  Generically_Dependent_Continuant: "Information artifacts that can be transferred through exact copying (Chunk 1:631-632)"
  Specifically_Dependent_Continuant: "Entities like temperature that cannot migrate from one bearer to another (Chunk 1:634-636)"

entity_relationships:
  - from: "Process"
    to: "Independent Continuant"
    relationship: "specifically depends on (participation)"
    source: "Chunk 1:848-852"
  - from: "Quality"
    to: "Independent Continuant"
    relationship: "inheres in (bearer)"
    source: "Chunk 1:499-502"
  - from: "Continuant"
    to: "Occurrent"
    relationship: "participates in"
    source: "Chunk 1:437-440"
  - from: "Process"
    to: "Spatiotemporal Region"
    relationship: "occupies"
    source: "Chunk 1:550-552"
  - from: "Process"
    to: "Temporal Region"
    relationship: "spans"
    source: "Chunk 1:552"
  - from: "Process Profile"
    to: "Process"
    relationship: "part of"
    source: "Chunk 2:144-146"
  - from: "Determinate Universal"
    to: "Determinable Universal"
    relationship: "is_a (specification of)"
    source: "Chunk 1:500-502"

abstraction_level: "foundational"

framework_comparison:
  - compared_to: "Gene Ontology"
    relationship: "provides top-level framework"
    details: "BFO serves as domain-neutral starting point for GO's 30,000 terms"
    source: "Chunk 1:190-195, 280-284"
  - compared_to: "Aristotle's Ontological Square"
    relationship: "recapitulates and extends"
    details: "BFO extends to ontological sextet including occurrents"
    source: "Chunk 1:450-452, 853-854"
  - compared_to: "Zemach's Four Ontologies"
    relationship: "adapts"
    details: "Adapts distinction between things (continuants) and events (occurrents)"
    source: "Chunk 1:348-354"
  - compared_to: "DOLCE"
    relationship: "similar bicategorial approach"
    details: "Both use endurant/perdurant distinction"
    source: "Chunk 1:299-300"

ai_integration: "N/A - paper predates LLM/AI integration discussion (2012)"

agent_modeling:
  - aspect: "Participation"
    description: "Agents (as independent continuants) participate in processes; connection is through participation relation not parthood"
    source: "Chunk 1:437-440"

agentic_workflows: "N/A - paper predates agentic AI discussion"

generative_ai_patterns: "N/A - paper predates LLM discussion"

agent_ontology_integration: "N/A - paper predates AI agent discussion"

# MEDIUM PRIORITY EXTRACTIONS

entity_count:
  count: 34
  rationale: "BFO is intentionally small as a top-level ontology to serve as common starting point"
  source: "Chunk 1:285-287"

methodology: "top-down"

empirical_evidence:
  - type: "Biomedical applications"
    description: "BFO used by 100+ ontology development groups in biology and medicine"
    source: "Chunk 1:283-284"
  - type: "Gene Ontology adoption"
    description: "GO uses BFO framework for 30,000 terms across biological processes, molecular functions, cellular components"
    source: "Chunk 1:193-195"
  - type: "Cardiac physiology"
    description: "Wiggers diagram demonstrates process profile classification for cardiac events"
    source: "Chunk 2:33-41"

limitations:
  - "No qualities of occurrents - processes cannot have attributes that change (Chunk 1:677-678)"
  - "Processes cannot change - they ARE changes in participants (Chunk 1:688-692)"
  - "Occurrent universals are always rigid - if instantiated at any time, instantiated at all times (Chunk 1:735-738)"

tools_standards:
  - "OWL (Web Ontology Language)"
  - "OWL-DL (Description Logic variant)"
  - "CLIF (Common Logic Interchange Format)"
  - "First-order logic"
  - "ISO Standard for Common Logic"
---

# Classifying Processes: An Essay in Applied Ontology - Analysis Index

## Paper Overview

- **Source**: 07-Classifying_Processes_Barry_Smith.pdf
- **Authors**: Barry Smith (University at Buffalo)
- **Published**: Ratio (new series) XXV 4, December 2012
- **Chunks**: 2 chunks, ~14,062 estimated tokens
- **Analyzed**: 2025-12-28

## Key Extractions

This paper provides a foundational treatment of Basic Formal Ontology (BFO), with particular focus on the classification of processes (occurrents). BFO is a bicategorial ontology that uniquely combines three-dimensionalist (continuant) and four-dimensionalist (occurrent) perspectives within a single coherent framework.

### Entity Types and Definitions

| Entity Type | Definition | Source |
|-------------|------------|--------|
| Continuant | Entities with parts only along spatial dimensions, not temporal | Chunk 1:350-354 |
| Occurrent | Entities existing in spatiotemporal regions, with temporal parts | Chunk 1:376-378 |
| Process | Changes in independent continuants; temporally extended occurrents | Chunk 1:691-692 |
| Quality | Dependent continuant not requiring realization process | Chunk 1:408-409 |
| Disposition | Dependent continuant requiring process for manifestation | Chunk 1:405-407 |
| Process Profile | Abstracted part of process for measurement along specific dimension | Chunk 2:152-157 |

### Entity Relationships

| From | To | Relationship | Source |
|------|-----|-------------|--------|
| Process | Independent Continuant | specifically depends on | Chunk 1:848-852 |
| Quality | Independent Continuant | inheres in | Chunk 1:499-502 |
| Continuant | Occurrent | participates in | Chunk 1:437-440 |
| Process | Spatiotemporal Region | occupies | Chunk 1:550-552 |
| Process Profile | Process | occurrent part of | Chunk 2:144-146 |

### Framework Comparisons

- **vs Gene Ontology**: BFO provides top-level framework; GO has 30,000 domain terms (Chunk 1:190-195)
- **vs Aristotle's Ontological Square**: BFO recapitulates and extends to "ontological sextet" (Chunk 1:450-452)
- **vs Zemach's Four Ontologies**: Adapts continuant/occurrent distinction (Chunk 1:348-354)

### Key Findings

- **Bicategorial Architecture** (Chunk 1:339-342): "BFO is founded on a bicategorial approach which seeks to combine elements of both the three-dimensionalist and four-dimensionalist perspectives"

- **Processes Cannot Change** (Chunk 1:688-692): "Processes cannot change on the four-dimensionalist view, because processes ARE changes"

- **Participation Not Parthood** (Chunk 1:437-440): "there are manifold connections between continuants and occurrents, but they are secured in BFO not through parthood relations, but rather through relations of participation"

- **Process Profiles** (Chunk 2:124-126): "This something which the two processes share in common we shall refer to... as a process profile"

## Chunk Navigation

### Chunk 1: Introduction, BFO Framework, Continuants and Occurrents
- **Summary**: Introduces applied ontology in biology, presents BFO as a 34-term top-level ontology, explains the continuant/occurrent distinction adapted from Zemach, discusses the ontological square, quality measurement, and the problem of process measurement data.
- **Key concepts**: [Applied ontology, BFO, Continuant, Occurrent, Gene Ontology, OWL, Quality, Disposition, Ontological Square, Process measurement, Temporal parthood]
- **Key quotes**:
  - Line 280-284: "Basic Formal Ontology (BFO) is a domain-neutral resource used by biologists and others to provide a top-level ontology"
  - Line 339-342: "BFO is founded on a bicategorial approach which seeks to combine elements of both"
  - Line 437-440: "connections between continuants and occurrents... are secured in BFO not through parthood relations, but rather through relations of participation"
  - Line 691-692: "processes are changes (they are changes in those independent continuant entities which are their participants)"
- **Load when**: "User asks about BFO structure", "Query about continuant vs occurrent", "Question about ontological foundations", "How do entities relate to processes", "What is the ontological square"

### Chunk 2: Process Profiles and Classification
- **Summary**: Introduces process profiles as the basis for classifying and measuring processes. Distinguishes quality process profiles (temperature changes), rate process profiles (speed, acceleration), and cyclical process profiles (heartbeat). Concludes with future directions for time series ontology.
- **Key concepts**: [Process profile, Quality process profile, Rate process profile, Cyclical process profile, Determinable/determinate universals, Cardiac processes, Wiggers diagram, Time series]
- **Key quotes**:
  - Line 124-126: "This something which the two processes share in common we shall refer to in what follows to as a process profile"
  - Line 152-157: "The simplest example of a process profile is that part of a process which serves as the target of selective abstraction"
  - Line 241-243: "Cyclical process profiles are a subtype of rate process profiles in which the salient ratio is number of cycles per unit of time"
- **Load when**: "User asks about process classification", "Question about measuring processes", "How to compare processes", "What are process profiles", "Rate and speed in ontology"

## Relevance to Research Question

This paper is highly relevant to the research question about foundational ontologies. It:

1. **Defines core entity types**: Establishes the fundamental continuant/occurrent distinction and their subtypes
2. **Provides formal entity definitions**: Gives precise definitions for Process, Quality, Disposition, Process Profile
3. **Maps entity relationships**: Defines participation, dependence, and parthood relations
4. **Positions BFO in ontology landscape**: Compares to Aristotle, Zemach, and shows relationship to domain ontologies like GO
5. **Addresses measurement problem**: Process profiles enable quantitative treatment of occurrents

The 34-term BFO serves as a top-level ontology that grounds domain ontologies - directly relevant to the 8-entity hypothesis and framework comparison questions.
