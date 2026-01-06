---
paper_id: "07-Classifying_Processes_Barry_Smith"
title: "Classifying Processes: An Essay in Applied Ontology"
authors:
  - "Barry Smith"
year: 2012
chunks_expected: 2
chunks_read: 2
analysis_complete: true
schema_version: "2.3"

chunk_index:
  1:
    token_count: 10515
    fields_found:
      entity_types: true
      entity_definitions: true
      entity_relationships: true
      entity_count: true
      abstraction_level: true
      framework_comparison: true
      methodology: true
      ai_integration: false
      agent_modeling: false
      agentic_workflows: false
      generative_ai_patterns: false
      agent_ontology_integration: false
      empirical_evidence: partial
      limitations: partial
      tools_standards: true
  2:
    token_count: 3005
    fields_found:
      entity_types: true
      entity_definitions: true
      entity_relationships: true
      entity_count: false
      abstraction_level: partial
      framework_comparison: false
      methodology: partial
      ai_integration: false
      agent_modeling: false
      agentic_workflows: false
      generative_ai_patterns: false
      agent_ontology_integration: false
      empirical_evidence: partial
      limitations: false
      tools_standards: false

entity_types:
  - item: "Continuant"
    chunk: 1
    lines: "293-296"
    quote: "BFO takes as its starting point a familiar distinction between two sets of views, which we can refer to as four-dimensionalist and three-dimensionalist, respectively."
  - item: "Occurrent"
    chunk: 1
    lines: "299-300"
    quote: "Four-dimensionalists (in simple terms) see reality as consisting exclusively of four-dimensional entities (variously referred to as processes, events, occurrents, perdurants, spacetime-worms, and so forth)."
  - item: "Independent Continuant"
    chunk: 1
    lines: "447-449"
    quote: "BFO draws on Aristotle's ideas concerning the division of substances and accidents, which reappears in BFO as the division between independent and dependent continuants."
  - item: "Dependent Continuant"
    chunk: 1
    lines: "405-406"
    quote: "BFO generalizes Zemach's idea of a continuant entity by allowing not only things (such as pencils and people) as continuants, but also entities that are dependent on things, such as qualities and dispositions such as solubility and fragility."
  - item: "Quality"
    chunk: 1
    lines: "458-459"
    quote: "Qualities are first-class entities in the BFO ontology (of the sort referred to elsewhere in the literature as 'tropes', or 'individual accidents')."
  - item: "Process"
    chunk: 1
    lines: "547-552"
    quote: "BFO uses 'occupies' to refer to the relation that holds between an occurrent and the spatiotemporal region which it exactly fills. Processes and process boundaries occupy spatiotemporal regions and they span temporal intervals and temporal instants, respectively."
  - item: "Process Boundary"
    chunk: 1
    lines: "548-549"
    quote: "BFO's treatment of occurrents, which include processes, process boundaries (for example beginnings and endings), spatiotemporal regions, and temporal intervals and temporal instants."
  - item: "Spatiotemporal Region"
    chunk: 1
    lines: "548-549"
    quote: "occurrents, which include processes, process boundaries (for example beginnings and endings), spatiotemporal regions, and temporal intervals and temporal instants"
  - item: "Generically Dependent Continuant"
    chunk: 1
    lines: "625-627"
    quote: "the BFO:generically dependent continuant expression: '1.7 m tall'."
  - item: "Process Profile"
    chunk: 2
    lines: "119-125"
    quote: "When comparing two heart beating processes as being for example of the same rate, or when comparing two games of chess as consisting of the same series of moves, then there is something in each of the two processes which is - not numerically but qualitatively - 'the same'. This something which the two processes share in common we shall refer to in what follows to as a process profile."
  - item: "Universal/Type"
    chunk: 1
    lines: "100-103"
    quote: "representing types or universals, which are the sorts of entities represented by the general terms used in formulating scientific theories such as 'cell' or 'electron' and which have instances which are the sorts of entities that are observed in scientific experiments."

entity_definitions:
  Continuant:
    chunk: 1
    lines: "351-354"
    quote: "The former, for Zemach, are defined by the fact that they can be sliced (in actuality, or in imagination) to yield parts only along the spatial dimension - for example those parts of your table which we call its legs, top, nails, and so on."
  Occurrent:
    chunk: 1
    lines: "370-381"
    quote: "An event is an entity that exists, in its entirety, in the area defined by its spatiotemporal boundaries, and each part of this area contains a part of the whole event."
  Quality:
    chunk: 1
    lines: "407-409"
    quote: "A quality, for BFO, is a dependent continuant that does not require such a process of realization of this sort."
  Determinable_Universal:
    chunk: 1
    lines: "500-502"
    quote: "Qualities instantiate quality universals, which are divided into determinable (such as temperature, length and mass) and determinate (such as 37.0C temperature, 1.6 meter length, and 4 kg mass)."
  Rigid_Universal:
    chunk: 1
    lines: "503-506"
    quote: "Determinable quality universals are rigid in the sense that, if a determinable quality universal is exemplified by a particular bearer at any time during which this bearer exists, then it is exemplified at every such time."
  Specific_Dependence:
    chunk: 1
    lines: "633-636"
    quote: "The temperature of your laptop, in contrast, is specifically dependent on the laptop, since a temperature (a specific instance of the universal temperature) cannot migrate from one body to another."
  Generic_Dependence:
    chunk: 1
    lines: "631-633"
    quote: "The record is said to be generically dependent upon its bearer since it can be transferred to another laptop through a process of exact copying."
  Process_Profile:
    chunk: 2
    lines: "126-131"
    quote: "What they share in common more precisely is that each contains an instantiation of the same process profile universal. The figure illustrates multiple instantiations of multiple process profile universals reflecting the fact that we can measure and compare cardiac processes along multiple different axes, each of which corresponds, in our proposed terminology, to a different determinable process profile universal."
  Quality_Process_Profile:
    chunk: 2
    lines: "152-157"
    quote: "The simplest example of a process profile is that part of a process which serves as the target of selective abstraction focused on a sequence of instances of determinate qualities such as temperature or height."
  Rate_Process_Profile:
    chunk: 2
    lines: "174-179"
    quote: "On a somewhat higher level of complexity are what we shall call rate process profiles, which are the targets of selective abstraction focused not on determinate quality magnitudes plotted over successive instants of time, but rather on certain ratios between these magnitudes and associated intervals of elapsed time."
  Cyclical_Process_Profile:
    chunk: 2
    lines: "238-243"
    quote: "Cyclical process profiles are a subtype of rate process profiles in which the salient ratio is not distance covered but rather number of cycles per unit of time."

entity_relationships:
  - item: "is_a (subtype of)"
    chunk: 1
    lines: "104-106"
    quote: "The nodes in the graph are joined by edges representing relations between the types, of which the most important (illustrated in Figure 1) are is_a (abbreviating 'is a subtype of') and part_of."
  - item: "part_of"
    chunk: 1
    lines: "135-143"
    quote: "When two nodes are joined together by the part_of relation, as in viral receptor activity part_of response to virus then this represents an assertion to the effect that every instance of the first type is a part of some instance of the second type."
  - item: "instance_of"
    chunk: 1
    lines: "133-134"
    quote: "this represents an assertion to the effect that all instances of the first type are also instances of the second type."
  - item: "occupies (occurrent-spatiotemporal region)"
    chunk: 1
    lines: "550-552"
    quote: "BFO uses 'occupies' to refer to the relation that holds between an occurrent and the spatiotemporal region which it exactly fills."
  - item: "spans (process-temporal interval)"
    chunk: 1
    lines: "551-552"
    quote: "Processes and process boundaries occupy spatiotemporal regions and they span temporal intervals and temporal instants, respectively."
  - item: "participates_in (continuant-occurrent)"
    chunk: 1
    lines: "437-440"
    quote: "Certainly there are manifold connections between continuants and occurrents, but they are secured in BFO not through parthood relations, but rather through relations of participation."
  - item: "temporal_part_of"
    chunk: 1
    lines: "577-582"
    quote: "a temporal_part_of b =Def. a occurrent_part_of b & for some temporal region r (a spans r & for all occurrents c, r' if (c spans r' & r' occurrent_part_of r) then (c occurrent_part_of a iff c occurrent_part_of b)))"
  - item: "inheres_in (quality-bearer)"
    chunk: 1
    lines: "498-502"
    quote: "They are entities which are dependent on the independent continuant entities (such as molecules, organisms, planets) which are their bearers."
  - item: "specifically_depends_on"
    chunk: 1
    lines: "848-852"
    quote: "Processes themselves stand to the independent continuants which are their participants in a relation that is analogous to that in which qualities stand to the independent continuants which are their bearers. In both cases we have to deal with the relation of what BFO calls specific dependence."

entity_count:
  value: 34
  chunk: 1
  lines: "285-290"
  quote: "BFO is, by the standards predominant in contemporary ontology, very small, consisting of just 34 terms (see Figure 2), including both familiar terms such as 'process', 'object', 'function', 'role' and 'disposition', and less familiar terms such as 'generically dependent continuant' and 'continuant fiat boundary'."

abstraction_level: "Foundational ontology (top-level). BFO is explicitly designed as a domain-neutral top-level ontology serving as common starting point for domain ontologies in biology, medicine, and other sciences. The paper states BFO consists of just 34 terms (Chunk 1:285) and is used by more than 100 ontology development groups (Chunk 1:283-284)."

framework_comparison:
  - item: "Gene Ontology (GO)"
    chunk: 1
    lines: "190-207"
    quote: "It is the Gene Ontology (GO), portions of which are illustrated in Figure 1, which is the most successful ontology currently being used by scientists in reasoning with experimental data. The GO consists of three sub-ontologies, together comprehending some 30,000 terms representing types and subtypes of biological processes, molecular functions, and cellular components."
  - item: "Zemach's Four Ontologies"
    chunk: 1
    lines: "348-361"
    quote: "BFO's treatment of the dichotomy between continuants and occurrents is adapted in part from the strategy proposed by Zemach in his 'Four Ontologies' for distinguishing between continuant and non-continuant entities, which Zemach calls 'things' and 'events', respectively."
  - item: "Aristotle's Ontological Square"
    chunk: 1
    lines: "447-452"
    quote: "BFO draws on Aristotle's ideas concerning the division of substances and accidents, which reappears in BFO as the division between independent and dependent continuants. Given that BFO accepts also the distinction between universals and particulars, it thus recapitulates Aristotle's ontological square."
  - item: "Ontology for Biomedical Investigations (OBI)"
    chunk: 1
    lines: "239-252"
    quote: "This aspect of the unification of science is addressed by the Ontology for Biomedical Investigations (OBI), which comprehends a set of terms which can be used to describe the attributes of experiments in biological and related domains."

ai_integration: "NOT_FOUND"

agent_modeling: "NOT_FOUND"

agentic_workflows: "NOT_FOUND"

generative_ai_patterns: "NOT_FOUND"

agent_ontology_integration: "NOT_FOUND"

methodology: "Top-down theoretical approach grounded in philosophical ontology. BFO adopts a bicategorial approach combining three-dimensionalist and four-dimensionalist perspectives (Chunk 1:339-342). The methodology is realist, assuming ontologies should employ classifications based on established scientific understanding (Chunk 1:67-71). Process attributions are treated through instantiation rather than quality predication (Chunk 1:803-808)."

empirical_evidence:
  - item: "Gene Ontology usage in biology"
    chunk: 1
    lines: "190-207"
    quote: "The GO consists of three sub-ontologies, together comprehending some 30,000 terms... The GO is used by researchers in biology and biomedicine as a controlled vocabulary for describing in species-neutral fashion the attributes of genes and gene products."
  - item: "Cardiac physiology measurement (Wiggers diagram)"
    chunk: 2
    lines: "33-37"
    quote: "consider Figure 4, which illustrates the cardiac events occurring in the left ventricle of a human heart. This figure tells us that each successive beating of the heart is such as to involve multiple different sorts of physiological processes, corresponding to measurements along the six distinct dimensions."
  - item: "BFO adoption"
    chunk: 1
    lines: "283-284"
    quote: "BFO provides a formal-ontological architecture and a set of very general terms and relations that are currently being used by more than 100 ontology development groups in biology and other fields."

limitations:
  - item: "No qualities of occurrents"
    chunk: 1
    lines: "804-807"
    quote: "There are no qualities of occurrents, in BFO, just as there are no qualities of qualities, and also no qualities of spatial or temporal regions."
  - item: "Processes cannot change"
    chunk: 1
    lines: "688-692"
    quote: "Processes, in particular, cannot change on the four-dimensionalist view, because processes are changes (they are changes in those independent continuant entities which are their participants)."

tools_standards:
  - item: "Common Logic Interchange Format (CLIF)"
    chunk: 1
    lines: "156-159"
    quote: "Prominent examples are the (CLIF) Common Logic Interchange Format and the (OWL) Web Ontology Language. Common Logic is an ISO Standard family of languages with an expressivity equivalent to that of first-order logic."
  - item: "Web Ontology Language (OWL-DL)"
    chunk: 1
    lines: "159-162"
    quote: "OWL-DL is a fragment of the language of first order logic belonging to the family of what are called Description Logics. While OWL-DL is marked by severe restrictions on its expressivity, the theories formulated in its terms have desirable computational properties."
  - item: "Reasoners"
    chunk: 1
    lines: "182-184"
    quote: "the consistency of such mergers can be checked automatically using dedicated software applications called 'reasoners'."
---

# Classifying Processes: An Essay in Applied Ontology

**Author:** Barry Smith
**Year:** 2012
**Source:** Ratio (new series) XXV 4 December 2012, pp. 463-488

## Summary

This paper presents Basic Formal Ontology (BFO) as a domain-neutral top-level ontology for scientific data representation, with particular focus on the classification of processes. BFO is a bicategorial ontology that combines three-dimensionalist (continuant) and four-dimensionalist (occurrent) perspectives within a unified framework.

## Key Contributions

### 1. BFO's Bicategorial Architecture

BFO distinguishes between:
- **Continuants**: Entities that persist through time while maintaining identity, including independent continuants (objects like organisms, cells) and dependent continuants (qualities, dispositions)
- **Occurrents**: Entities extended in time (processes, events), which cannot change because they ARE changes

### 2. The Ontological Square and Sextet

The paper extends Aristotle's ontological square (substances vs accidents, universals vs particulars) into a sextet by adding the occurrent dimension, showing how:
- Independent continuants have qualities (dependent continuants)
- Both continuants and occurrents have type (universal) and instance (particular) levels
- Processes specifically depend on the continuants that participate in them

### 3. Process Profiles

A novel contribution for classifying processes through "process profiles" - the something that two processes share when they are qualitatively the same along some dimension:

- **Quality Process Profiles**: Sequences of determinate quality instances (e.g., temperature changes over time)
- **Rate Process Profiles**: Ratios between magnitudes and elapsed time (e.g., speed, acceleration)
- **Cyclical Process Profiles**: Number of cycles per unit time (e.g., heartbeat rate)

### 4. Process Attribution via Instantiation

Unlike qualities of continuants, process attributes are handled through instantiation rather than predication:
- "motion p has speed v" is interpreted as "motion p instance_of universal motion-with-speed-v"
- This maintains BFO's simplicity by avoiding qualities of occurrents

## Relevance to Research Questions

### Entity Types and Definitions
BFO provides a foundational set of 34 entity types organized around the continuant/occurrent distinction. The paper gives precise definitions distinguishing:
- Continuants (spatial parts only) vs occurrents (spatiotemporal parts)
- Independent vs dependent continuants
- Determinable vs determinate universals
- Rigid vs non-rigid universals

### Framework Comparison
BFO is positioned as:
- More general than domain ontologies like GO (30,000 terms)
- Rooted in Aristotelian and Zemachian traditions
- Compatible with OBI for experiment description
- Formalized in CLIF and OWL-DL

### Agent-Activity-Entity Triad
While not explicitly addressing AI agents, BFO's continuant-process-participation structure provides a foundational pattern:
- Continuants (potential agents) participate in processes (activities)
- Qualities and dispositions characterize continuants
- Processes depend on but are not parts of continuants

## Limitations for AI/Agent Research

This paper predates modern AI agent systems (published 2012) and does not address:
- AI agent modeling or autonomous behavior
- LLM integration or generative AI patterns
- Agentic workflows or multi-agent systems
- Ontology-guided reasoning for AI

However, BFO's rigorous treatment of processes, participation, and temporal structure provides foundational concepts that could ground agent-activity modeling in more recent work.
