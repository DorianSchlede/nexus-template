---
paper_id: "12"
title: "Foundations of Process Event Data"
authors: ["Jochen De Weerdt", "Moe Thandar Wynn"]
year: 2022
venue: "Process Mining Handbook, LNBIP 448"
doi: "10.1007/978-3-031-08848-3_6"
extraction_version: "2.0"
extraction_date: "2025-12-31"
extraction_approach: "DISCOVERY"

# V2 EXTRACTION FIELDS

ontological_primitives:
  - term: "Event"
    definition: "An observed atomic granule of activity - the fundamental unit of process execution data"
    source: "Chunk 1:168-169"
    unique_aspects: "Explicitly atomic - cannot be decomposed further in this framework. Events are NOT independent observations but intrinsically correlated via case dimension and temporal ordering."

  - term: "Case (Process Instance)"
    definition: "An overarching dimension that groups related events; represents one execution of a business process"
    source: "Chunk 1:34-35, 68-71"
    unique_aspects: "The case is what makes process data fundamentally different from classical attribute-value datasets. The Case ID is Requirement 1 for analysis-ready event logs."

  - term: "Trace"
    definition: "A sequence of events pertaining to a single case, ordered temporally"
    source: "Chunk 1:110-112, 169-170"
    unique_aspects: "Traces are NOT just sets - they are ordered sequences. The ordering is semantically critical."

  - term: "Activity (Activity Label)"
    definition: "A restricted set of labels reflecting process steps to which each event is mapped"
    source: "Chunk 1:93-102"
    unique_aspects: "Activities are assumed to form a finite, controlled vocabulary. This is Requirement 2 for event logs."

  - term: "Timestamp"
    definition: "Temporal marker that enables ordering of events within a case"
    source: "Chunk 1:110-116"
    unique_aspects: "Not strictly mandatory - ordering could come from database record order. This is Requirement 3 for event logs."

  - term: "Attribute"
    definition: "Additional data elements attached to events, traces, or logs beyond the three essential requirements"
    source: "Chunk 1:130-153"
    unique_aspects: "Attributes can be event-level (changing per event) or case-level (constant within a case). They enable filtering, contextual analysis, and advanced mining techniques."

  - term: "Log"
    definition: "A container for multiple traces, representing a collection of process executions"
    source: "Chunk 1:169"
    unique_aspects: "The log level allows for extensions and metadata that apply across all traces."

structural_patterns:
  - pattern_name: "Three-Requirement Foundation"
    structure: "Event -> Case ID + Activity Label + Timestamp = Analysis-Ready Log"
    instances:
      - "Case ID groups events into traces"
      - "Activity Label classifies what happened"
      - "Timestamp orders what happened"
    source: "Chunk 1:62-116"
    note: "This is the minimal viable structure for process mining. Remove any one and the log becomes unusable for standard techniques."

  - pattern_name: "Log-Trace-Event Hierarchy"
    structure: "Log contains Traces; Traces contain Events; Events have Attributes"
    instances:
      - "XES metadata structure (Figure 2)"
      - "Hierarchical nesting: log > trace > event > attribute"
    source: "Chunk 1:163-175"
    note: "This is a strict containment hierarchy, not a network."

  - pattern_name: "Activity Lifecycle State Machine"
    structure: "Activity transitions through states: start -> running -> complete (with variations)"
    instances:
      - "BPMN 2.0 lifecycle (Figure 3a) - more complex with ready, active, completing states"
      - "XES lifecycle extension (Figure 3b) - simpler state machine"
    source: "Chunk 1:181-224"
    note: "The lifecycle allows multiple events per activity execution, enabling distinction between waiting time and execution time."

  - pattern_name: "Extraction-Correlation-Abstraction Trident"
    structure: "Three-pronged event log preparation: Extract -> Correlate -> Abstract"
    instances:
      - "Extraction: obtaining data from source systems"
      - "Correlation: mapping events to cases (generating Case IDs)"
      - "Abstraction: translating low-level events to business-level activities"
    source: "Chunk 1:383-395, Figure 5"
    note: "This is the canonical preprocessing pipeline for process mining, distinct from classical data science pipelines."

  - pattern_name: "Granularity Translation"
    structure: "Low-level events -> Abstraction techniques -> Business-level activities"
    instances:
      - "IoT sensor readings -> process activities"
      - "Database transactions -> business steps"
      - "Clustering-based: group similar event sequences"
      - "Pattern-based: match local subsequence patterns"
      - "Supervised: use domain knowledge or process models"
    source: "Chunk 1:476-523"

novel_concepts:
  - concept: "Event Correlation"
    definition: "The problem of automatically or semi-automatically generating Case IDs when they are not readily available in source data"
    novelty_claim: "Addresses a fundamental gap between how operational systems store data (often without process perspective) and what process mining needs"
    source: "Chunk 1:77-85, 450-470"
    note: "Correlation is a distinct preprocessing challenge not found in classical data mining."

  - concept: "Event Abstraction"
    definition: "Mapping one or more lower-level events into higher-level events pertaining to business process activities"
    novelty_claim: "Bridges the granularity gap between how data is stored and how processes are understood by business experts"
    source: "Chunk 1:473-523"
    note: "Multiple techniques exist: clustering, pattern-based, supervised learning. No single solution dominates."

  - concept: "Non-IID Data Nature of Event Logs"
    definition: "Events in a log are intrinsically correlated (via case and time), violating the Independent and Identically Distributed assumption of most ML techniques"
    novelty_claim: "Explains why classical data science techniques cannot be straightforwardly applied to event logs"
    source: "Chunk 1:364-369"
    note: "This is a fundamental theoretical insight that justifies the existence of process mining as a distinct field."

  - concept: "Event Log Imperfection Patterns"
    definition: "Systematic categorization of data quality issues specific to event logs: form-based event capture, inadvertent time travel, unanchored event, scattered event, elusive case, scattered case, collateral event, polluted label, distorted label, synonymous labels, homonymous labels"
    novelty_claim: "Eleven domain-specific patterns for detecting and repairing event log quality issues"
    source: "Chunk 1:579-583"
    note: "These are process-mining-specific quality patterns, not general data quality dimensions."

  - concept: "Object-Centric Event Data (OCEL)"
    definition: "Events linked to multiple objects rather than a single case, enabling multiple case notions in a single log"
    novelty_claim: "Breaks from the traditional single-case-centric assumption of process mining"
    source: "Chunk 1:424-433"
    note: "Represents a paradigm shift from case-centric to object-centric process mining."

  - concept: "Quality Annotations for Event Logs"
    definition: "Metadata at event, trace, and log levels to track data quality issues and repairs"
    novelty_claim: "Enables quality-informed process mining where algorithms consider data quality"
    source: "Chunk 1:603-608"

semantic_commitments:
  - commitment: "Atomicity of Events"
    position: "Events are atomic - they cannot be meaningfully decomposed"
    implications: "If you need finer granularity, you need more events, not sub-events"
    source: "Chunk 1:168"

  - commitment: "Case-Centric Worldview (Traditional)"
    position: "Every event belongs to exactly one case"
    implications: "Cannot natively model shared resources, interacting processes, or multi-object scenarios. OCEL challenges this."
    source: "Chunk 1:68-75"

  - commitment: "Finite Activity Vocabulary"
    position: "Activities form a restricted (finite, predefined) set of labels"
    implications: "Process discovery assumes a closed world of possible activities"
    source: "Chunk 1:93-95"

  - commitment: "Total Ordering Within Cases"
    position: "Events within a case can be totally ordered (usually by timestamp)"
    implications: "Partial ordering (concurrent events with same timestamp) is treated as a quality problem, not a feature"
    source: "Chunk 1:110-116, 621-622"

  - commitment: "Data Reflects Reality (With Imperfection)"
    position: "Event logs are meant to reflect actual process execution, but imperfections occur"
    implications: "Tension between 'repair data' vs 'data reflects reality' philosophies"
    source: "Chunk 1:565-567"

boundary_definitions:
  - entity_type: "Event vs Event Type (Lifecycle Transition)"
    identity_criteria: "An event is a single occurrence; an event type describes what kind of lifecycle transition it represents (start, complete, etc.)"
    boundary_cases: "Is 'start' and 'complete' one activity execution or two events? Answer: Two events, one activity."
    source: "Chunk 1:178-224"

  - entity_type: "Case Boundary"
    identity_criteria: "Defined by the Case ID - all events with the same Case ID belong to the same case"
    boundary_cases: "Patient ID vs Admission ID yields different case boundaries and different analyses. The choice is analytical, not ontological."
    source: "Chunk 1:119-124"

  - entity_type: "Activity Granularity"
    identity_criteria: "What counts as 'one activity' depends on the analysis viewpoint"
    boundary_cases: "One activity per event? Or abstract multiple low-level events into one activity? The boundary is methodological choice."
    source: "Chunk 1:103-109"

temporal_modeling:
  - aspect: "Event Timestamps"
    approach: "Point-based timestamps attached to events"
    mechanism: "Each event has a timestamp; order derived from comparing timestamps"
    source: "Chunk 1:110-116"

  - aspect: "Activity Duration"
    approach: "Derived from lifecycle events (start vs complete)"
    mechanism: "Duration = complete_timestamp - start_timestamp; requires two events per activity"
    source: "Chunk 1:219-224"

  - aspect: "Waiting Time vs Execution Time"
    approach: "Distinguished only when start and complete events are recorded"
    mechanism: "Single-event-per-activity logs cannot distinguish waiting from working"
    source: "Chunk 1:221-224"

  - aspect: "Same-Timestamp Problem"
    approach: "Treated as data quality issue requiring repair"
    mechanism: "Multiple events with identical timestamps need ordering resolution"
    source: "Chunk 1:591-593, 621-622"

  - aspect: "Inadvertent Time Travel"
    approach: "Recognized as imperfection pattern"
    mechanism: "Events appearing out of expected temporal order"
    source: "Chunk 1:581"

agency_spectrum:
  - agent_type: "Resource"
    capabilities: "Mentioned as additional data attribute - resources are employed within the process"
    constraints: "Not elaborated beyond being an attribute; no intentionality model"
    source: "Chunk 1:148-151"
    note: "The paper does NOT provide a rich agency model. Resources are data, not actors."

  - agent_type: "Implicit Human Actor"
    capabilities: "Business experts who interpret activities and define abstraction levels"
    constraints: "Outside the data model; involved in annotation, repair, and interpretation"
    source: "Chunk 1:105-106, 522-523"

  - agent_type: "No Explicit Agent Primitive"
    capabilities: "N/A"
    constraints: "N/A"
    source: "Entire document"
    note: "SURPRISE: This foundational process mining paper has NO agent primitive. Events just happen; who/what causes them is an attribute, not a first-class entity."

knowledge_representation:
  - mechanism: "XES (eXtensible Event Stream)"
    formalism: "XML-based schema; W3C XML Schema definition"
    reasoning: "No reasoning built in - XES is a storage/interchange format, not an inference system"
    source: "Chunk 1:163-175"

  - mechanism: "Event Log as Attribute-Value Data"
    formalism: "Tabular structure (events as rows, attributes as columns) with case and temporal correlation"
    reasoning: "Requires process mining algorithms that respect the non-IID nature"
    source: "Chunk 1:159-162, 364-369"

  - mechanism: "Ontology-Based Data Access (OBDA)"
    formalism: "Ontological view of domain linked to database schema (Onprom tool)"
    reasoning: "Enables extraction of event logs from relational databases via ontological mediation"
    source: "Chunk 1:427-431"

  - mechanism: "Data Virtualization / Federation"
    formalism: "Querying multiple sources as if single database, without consolidation"
    reasoning: "Flexible integration without data duplication"
    source: "Chunk 1:467-470"

emergence_indicators:
  - phenomenon: "Process Model Emergence"
    mechanism: "Process models are discovered from event logs, not prescribed"
    evidence: "Process discovery algorithms extract models from data"
    source: "Chunk 1:26-29"
    note: "The 'process' emerges from the data rather than being defined a priori."

  - phenomenon: "Behavioral Patterns Not Visible at Event Level"
    mechanism: "Classical ML on events gives 'useless or biased results' because case-level behavior is not captured"
    evidence: "Process mining techniques needed because single-event analysis misses the emergent case-level patterns"
    source: "Chunk 1:29-35"

  - phenomenon: "Organizational Patterns from Event Data"
    mechanism: "Organizational mining discovers resource patterns from event attributes"
    evidence: "Referenced but not detailed"
    source: "Chunk 1:151"

integration_surfaces:
  - surface: "BPMN 2.0"
    connects_to: ["Activity lifecycle states", "Process model notation"]
    alignment_quality: "Good - BPMN lifecycle directly informs event type semantics"
    source: "Chunk 1:183-186"

  - surface: "XES Extensions"
    connects_to: ["Domain-specific attribute sets", "Lifecycle extension"]
    alignment_quality: "Designed for extensibility; standard extensions available"
    source: "Chunk 1:172-175"

  - surface: "ERP/CRM Systems"
    connects_to: ["SAP", "Salesforce", "Enterprise data sources"]
    alignment_quality: "Requires extraction connectors; often not process-aware by design"
    source: "Chunk 1:277-284, 327-329"

  - surface: "OCEL Standard"
    connects_to: ["Object-centric process mining", "Multiple case notions"]
    alignment_quality: "Extends XES paradigm; enables multi-object scenarios"
    source: "Chunk 1:431-433"

  - surface: "IoT Data"
    connects_to: ["Sensor readings", "Actuator data", "Physical processes"]
    alignment_quality: "Requires significant abstraction; granularity gap is challenging"
    source: "Chunk 1:317-322, 484-497"

  - surface: "ETL Tools and Data Warehouses"
    connects_to: ["Business Intelligence", "Data lakes"]
    alignment_quality: "Good fit for correlation and integration tasks"
    source: "Chunk 1:296-300, 464-466"

gaps_and_tensions:
  - gap_type: "Omission"
    description: "No explicit agent or actor model - who/what performs activities is relegated to an optional attribute"
    implications: "Cannot reason about agency, responsibility, or intentionality at the structural level"
    source: "Implicit - resource mentioned only as attribute"

  - gap_type: "Omission"
    description: "No goal or outcome primitive - what the process is trying to achieve is not modeled"
    implications: "Success/failure of process instances must be derived from attributes, not structure"
    source: "Implicit - not discussed"

  - gap_type: "Omission"
    description: "No rule or constraint primitive - governance and compliance are external to the data model"
    implications: "Conformance checking requires external reference models"
    source: "Implicit - conformance checking mentioned but not grounded in data model"

  - gap_type: "Tension"
    description: "Single-case vs Object-centric paradigms"
    implications: "Traditional XES assumes one case per event; OCEL allows multiple. Paradigm shift underway."
    source: "Chunk 1:424-433"

  - gap_type: "Tension"
    description: "Data repair vs Data-as-truth philosophies"
    implications: "Some advocate repairing bad data; others say data reflects reality. No resolution offered."
    source: "Chunk 1:565-567"

  - gap_type: "Underspecified"
    description: "Activity abstraction is acknowledged as crucial but no single best method"
    implications: "Multiple techniques exist (clustering, pattern, supervised) but guidance on when to use which is limited"
    source: "Chunk 1:500-523"

  - gap_type: "Tension"
    description: "Process-aware vs non-process-aware source systems"
    implications: "BPMS provides ready data; most enterprise systems require significant extraction/correlation work"
    source: "Chunk 1:265-270, 403-406"

empirical_grounding:
  - type: "Survey"
    domain: "Process mining community"
    scale: "289 participants"
    findings: "SAP ECC, SAP S/4 HANA, Salesforce are top three source systems; 60-90% of effort spent on preprocessing"
    source: "Chunk 1:326-329, 576-578"

  - type: "Industry Experience"
    domain: "Australian healthcare, general industry"
    scale: "20+ datasets"
    findings: "11 event log imperfection patterns identified from real-world experience"
    source: "Chunk 1:579-583"

  - type: "Case Study Reference"
    domain: "Healthcare (road trauma retrieval)"
    scale: "Not specified"
    findings: "CRISP-DM adapted for healthcare process mining datasets"
    source: "Chunk 1:374-375"

  - type: "Data Sources Taxonomy"
    domain: "Cross-industry"
    scale: "8 source system categories"
    findings: "BPMS, case management, ERP/CRM, operational DB, project management, data warehouses, web data, IoT"
    source: "Chunk 1:262-322"

# DISCOVERY NOTES

surprises:
  - "NO AGENT PRIMITIVE: This is a foundational process mining paper, yet 'agent' is not a first-class entity. Events have resources as attributes, but there is no structured concept of who/what acts. This is a major gap compared to PROV-O's Agent-Activity-Entity triad."
  - "EVENTS ARE NON-IID: Explicit statement that event log data violates the IID assumption, explaining why classical ML fails on process data. This is a fundamental theoretical insight."
  - "CASE DEFINITION IS ANALYTICAL CHOICE: What constitutes a 'case' is not ontologically fixed - patient ID vs admission ID yields different analyses. The boundary is methodological, not natural."
  - "OBJECT-CENTRIC PARADIGM SHIFT: The paper acknowledges OCEL as a move away from single-case assumption. This suggests the foundational model itself is evolving."

quality_signals:
  terminology_preserved: true
  novel_concepts_found: 6
  gaps_identified: 6
  tensions_documented: 4
  surprises_noted: 4

meta_observations:
  - "This paper is practical/technical rather than philosophical. It does not engage with formal ontology traditions (BFO, UFO, DOLCE)."
  - "The primitives here are data-structural (event, trace, log) rather than ontological (entity, process, quality)."
  - "There is an implicit commitment to a process-centric worldview where 'things happen' in sequences grouped by cases."
  - "The lack of agent/goal/rule primitives positions this as a DATA model, not a full ONTOLOGY of processes."
  - "Integration opportunity: Could benefit from grounding in formal ontology to add agency, intentionality, and normative dimensions."
---

# Foundations of Process Event Data

## Overview

This chapter from the Process Mining Handbook provides a practical and technical foundation for understanding process event data. It defines the minimal structural requirements for event logs (Case ID, Activity Label, Timestamp), discusses data sources, preprocessing pipelines, and data quality considerations.

## Core Contribution

The paper establishes that process event data is fundamentally different from classical attribute-value datasets because:
1. Events are correlated via the case dimension
2. Events are temporally ordered within cases
3. The data violates IID assumptions, requiring specialized techniques

## The Three Requirements

| Requirement | Element | Purpose |
|-------------|---------|---------|
| 1 | Case ID | Groups events into process instances |
| 2 | Activity Label | Classifies what type of step occurred |
| 3 | Timestamp | Orders events within a case |

## Key Insight: Non-IID Nature

> "Events in an event log... are related to each other in terms of time and by means of an overarching case dimension, which, when not taken into account via dedicated analysis techniques, results in useless or biased results." (Chunk 1:33-36)

This explains why process mining exists as a distinct field from general data science.

## The Extraction-Correlation-Abstraction Trident

The paper introduces a process-mining-specific preprocessing pipeline:
- **Extraction**: Getting data from source systems (often not process-aware)
- **Correlation**: Generating Case IDs when not available
- **Abstraction**: Translating low-level events to business-level activities

## Paradigm Shift: Object-Centric Event Data

The traditional assumption (one case per event) is being challenged by OCEL, which allows events to link to multiple objects. This represents a significant evolution in the field's foundational assumptions.

## Critical Gap: No Agent Model

**SURPRISE**: This foundational paper does not include an agent or actor primitive. Resources are mentioned as optional attributes, but there is no first-class concept of "who/what acts." This contrasts sharply with PROV-O's Agent-Activity-Entity triad and represents a significant gap for modeling responsibility, intentionality, and accountability in processes.

## Integration Opportunities

This data-structural model could be enriched by:
1. Adding agent primitives (who acts)
2. Adding goal primitives (why actions occur)
3. Adding rule/constraint primitives (what governs actions)
4. Grounding in formal ontology (BFO, UFO) for philosophical clarity

## Quality Assessment

The paper provides excellent empirical grounding through survey data and industry experience, but remains at the data engineering level rather than engaging with formal ontology traditions.
