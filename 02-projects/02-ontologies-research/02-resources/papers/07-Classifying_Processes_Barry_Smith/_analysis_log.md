---
schema_version: "2.0"
paper_id: "07-Classifying_Processes_Barry_Smith"
paper_title: "Classifying Processes: An Essay in Applied Ontology"
paper_folder: "C:/Users/dsber/strategy-nexus/02-projects/02-ontologies-research/02-resources/papers/07-Classifying_Processes_Barry_Smith"
analyzer: "claude-opus-4"
analysis_started: "2025-12-28T14:30:00"
analysis_completed: "2025-12-28T14:45:00"
duration_seconds: 900

steps:
  step1_read_briefing:
    completed: true
    briefing_path: "C:/Users/dsber/strategy-nexus/02-projects/02-ontologies-research/02-resources/_analysis_kit.md"
    research_question: "What are the foundational ontologies for digital work, and how do they ground entity definitions, framework comparisons, and AI agent/generative AI integration patterns?"
    fields_required: 15
    focus_areas: ["Foundational ontologies", "Entity definitions", "Entity relationships", "BFO framework", "Process classification"]

  step2_read_metadata:
    completed: true
    metadata_path: "C:/Users/dsber/strategy-nexus/02-projects/02-ontologies-research/02-resources/papers/07-Classifying_Processes_Barry_Smith/_metadata.json"
    chunks_expected: 2
    tokens_estimated: 14062

  step3_analyze_chunks:
    completed: true
    chunks_total: 2
    chunks_read: [1, 2]
    all_chunks_read: true
    chunk_evidence:
      1:
        start: "We begin by describing recent developments in the burgeoning discipline of applied ontology, focusing especially"
        mid: "table, or between the first half of a football match and the whole match.) 1.2 The Common Logic Interchange"
        end: "Phonocardiogram"
        lines_read: 1000
      2:
        start: "constant speed running process cardiovascular exercise process air-displacement process compression sock testing"
        mid: "in the case of a regular cyclical process profile, a rate can be assigned in the simplest possible fashion by"
        end: "phismith@buffalo.edu"
        lines_read: 343

extractions:
  entity_types:
    - name: "Continuant"
      chunk: 1
      lines: "293-296"
      quote: "BFO takes as its starting point a familiar distinction between two sets of views... four-dimensionalist and three-dimensionalist"
      confidence: "high"
    - name: "Occurrent"
      chunk: 1
      lines: "299-300"
      quote: "Four-dimensionalists see reality as consisting exclusively of four-dimensional entities (variously referred to as processes, events, occurrents, perdurants)"
      confidence: "high"
    - name: "Independent Continuant"
      chunk: 1
      lines: "448-449"
      quote: "the division of substances and accidents, which reappears in BFO as the division between independent and dependent continuants"
      confidence: "high"
    - name: "Dependent Continuant"
      chunk: 1
      lines: "405-409"
      quote: "entities that are dependent on things, such as qualities and dispositions such as solubility and fragility"
      confidence: "high"
    - name: "Quality"
      chunk: 1
      lines: "458-459"
      quote: "Qualities are first-class entities in the BFO ontology (of the sort referred to elsewhere in the literature as 'tropes')"
      confidence: "high"
    - name: "Process"
      chunk: 1
      lines: "548-552"
      quote: "occurrents, which include processes, process boundaries, spatiotemporal regions, and temporal intervals"
      confidence: "high"
    - name: "Process Profile"
      chunk: 2
      lines: "124-126"
      quote: "This something which the two processes share in common we shall refer to in what follows to as a process profile"
      confidence: "high"

  entity_definitions:
    - name: "Continuant"
      chunk: 1
      lines: "350-354"
      quote: "entities which can be sliced to yield parts only along the spatial dimension - for example those parts of your table which we call its legs, top, nails"
      confidence: "high"
    - name: "Occurrent"
      chunk: 1
      lines: "370-381"
      quote: "An event is an entity that exists, in its entirety, in the area defined by its spatiotemporal boundaries, and each part of this area contains a part of the whole event"
      confidence: "high"
    - name: "Process"
      chunk: 1
      lines: "691-692"
      quote: "processes are changes (they are changes in those independent continuant entities which are their participants)"
      confidence: "high"
    - name: "Process Profile"
      chunk: 2
      lines: "152-157"
      quote: "that part of a process which serves as the target of selective abstraction focused on a sequence of instances of determinate qualities such as temperature or height"
      confidence: "high"

  entity_relationships:
    - from: "Process"
      to: "Independent Continuant"
      relationship: "specifically depends on"
      chunk: 1
      lines: "848-852"
      quote: "Processes themselves stand to the independent continuants which are their participants in a relation... of what BFO calls specific dependence"
      confidence: "high"
    - from: "Quality"
      to: "Independent Continuant"
      relationship: "inheres in"
      chunk: 1
      lines: "499-502"
      quote: "Qualities... are entities which are dependent on the independent continuant entities (such as molecules, organisms, planets) which are their bearers"
      confidence: "high"
    - from: "Continuant"
      to: "Occurrent"
      relationship: "participates in"
      chunk: 1
      lines: "437-440"
      quote: "there are manifold connections between continuants and occurrents, but they are secured in BFO not through parthood relations, but rather through relations of participation"
      confidence: "high"
    - from: "Process"
      to: "Spatiotemporal Region"
      relationship: "occupies"
      chunk: 1
      lines: "550-552"
      quote: "Processes and process boundaries occupy spatiotemporal regions and they span temporal intervals and temporal instants"
      confidence: "high"

  abstraction_level:
    value: "foundational"
    chunk: 1
    lines: "280-284"
    quote: "Basic Formal Ontology (BFO) is a domain-neutral resource used by biologists and others to provide a top-level ontology that can serve as a common starting point for the creation of domain ontologies"
    confidence: "high"

  framework_comparison:
    - compared_to: "Gene Ontology"
      relationship: "provides top-level framework for"
      chunk: 1
      lines: "190-195"
      quote: "Gene Ontology (GO)... consists of three sub-ontologies, together comprehending some 30,000 terms representing types and subtypes"
      confidence: "high"
    - compared_to: "Aristotle's Ontological Square"
      relationship: "recapitulates"
      chunk: 1
      lines: "450-452"
      quote: "it thus recapitulates Aristotle's ontological square"
      confidence: "high"
    - compared_to: "Zemach's Four Ontologies"
      relationship: "adapts from"
      chunk: 1
      lines: "348-350"
      quote: "BFO's treatment of the dichotomy between continuants and occurrents is adapted in part from the strategy proposed by Zemach in his 'Four Ontologies'"
      confidence: "high"

  methodology:
    value: "top-down"
    chunk: 1
    lines: "276-279"
    quote: "the principal concerns of applied ontologists are highly practical in nature. Just occasionally, however, they still face problems of a recognizably philosophical sort"
    confidence: "high"

  tools_standards:
    - name: "OWL"
      chunk: 1
      lines: "157-161"
      quote: "OWL-DL is a fragment of the language of first order logic belonging to the family of what are called Description Logics"
      confidence: "high"
    - name: "CLIF"
      chunk: 1
      lines: "156-158"
      quote: "Common Logic Interchange Format... Common Logic is an ISO Standard family of languages with an expressivity equivalent to that of first-order logic"
      confidence: "high"

  entity_count:
    count: 34
    chunk: 1
    lines: "285-287"
    quote: "BFO is, by the standards predominant in contemporary ontology, very small, consisting of just 34 terms"
    confidence: "high"

  limitations:
    - limitation: "No qualities of occurrents"
      chunk: 1
      lines: "677-678"
      quote: "there is no counterpart on the occurrent side for BFO's qualities of independent continuants"
      confidence: "high"
    - limitation: "Processes cannot change"
      chunk: 1
      lines: "688-692"
      quote: "it follows trivially from BFO's four-dimensionalist account of occurrents that occurrents cannot change"
      confidence: "high"

performance:
  tokens_used: 14062
  tokens_available: 100000
  time_per_chunk_avg: 450

quality:
  relevance_score: 5
  relevance_rationale: "Core BFO paper directly addressing foundational ontology entity types and their relationships - highly relevant to research question about foundational ontologies"
  domain_match: true
  has_llm_content: false
  extraction_confidence: "high"

outputs:
  index_md_created: true
  index_md_path: "C:/Users/dsber/strategy-nexus/02-projects/02-ontologies-research/02-resources/papers/07-Classifying_Processes_Barry_Smith/index.md"
  index_md_yaml_valid: true
  index_md_word_count: 1200

issues: []
warnings: []
---

# Analysis Log: Classifying Processes - Barry Smith

## Summary

This paper by Barry Smith (2012) provides a foundational treatment of Basic Formal Ontology (BFO), focusing specifically on the classification of processes (occurrents). The paper presents BFO's bicategorial approach that combines three-dimensionalist (continuant) and four-dimensionalist (occurrent) perspectives. A key contribution is the concept of "process profiles" for classifying and measuring processes.

## Key Findings

1. **BFO Bicategorial Architecture**: BFO uniquely combines both continuant and occurrent ontologies within a single framework, unlike approaches that force a choice between 3D and 4D views.

2. **Ontological Square/Sextet**: The paper extends Aristotle's ontological square to include occurrents, creating an "ontological sextet" that maps type/instance distinctions across independent continuants, dependent continuants, and occurrents.

3. **Process Profiles**: Novel contribution - process profiles are "that part of a process which serves as the target of selective abstraction" enabling measurement and comparison of processes along specific dimensions.

4. **No Qualities of Occurrents**: A key design decision - BFO does not allow qualities of processes because "processes are changes" and cannot themselves change.

5. **Participation Relation**: Continuants and occurrents are connected through participation relations, not parthood relations.

## Chunks Analyzed

- Chunk 1 (lines 1-1000): Applied ontology background, BFO introduction, continuant/occurrent distinction, qualities, process measurement
- Chunk 2 (lines 1-343): Process profiles (quality, rate, cyclical), conclusion on time series graphs
