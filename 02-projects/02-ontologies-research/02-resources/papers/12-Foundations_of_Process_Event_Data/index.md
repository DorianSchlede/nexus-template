---
paper_id: "12-Foundations_of_Process_Event_Data"
title: "Foundations of Process Event Data"
authors:
  - "Jochen De Weerdt"
  - "Moe Thandar Wynn"
year: 2022
chunks_expected: 1
chunks_read: 1
analysis_complete: true
high_priority_fields_found: 5

# HIGH PRIORITY FIELDS (1-5: Ontology focus)
entity_types:
  - "Event"
  - "Case"
  - "Activity"
  - "Trace"
  - "Log"
  - "Attribute"

entity_definitions:
  Event: "An observed atomic granule of activity (Chunk 1:168)"
  Case: "A process instance to which events are linked via Case ID (Chunk 1:68-74)"
  Activity: "A step executed within the process, mapped to events via activity labels (Chunk 1:92-102)"
  Trace: "A sequence of events pertaining to a case (Chunk 1:111)"
  Log: "A collection of traces with associated metadata (Chunk 1:163-169)"
  Attribute: "Additional data columns pertaining to events, activities, or cases (Chunk 1:130-136)"

entity_relationships:
  - from: "Event"
    to: "Case"
    relationship: "belongs_to"
    source: "Chunk 1:68-69"
  - from: "Event"
    to: "Activity"
    relationship: "corresponds_to"
    source: "Chunk 1:92-93"
  - from: "Event"
    to: "Trace"
    relationship: "forms_sequence"
    source: "Chunk 1:111"
  - from: "Trace"
    to: "Log"
    relationship: "contained_in"
    source: "Chunk 1:169"
  - from: "Attribute"
    to: "Event"
    relationship: "attached_to"
    source: "Chunk 1:130-136"
  - from: "Attribute"
    to: "Case"
    relationship: "attached_to"
    source: "Chunk 1:132-133"

abstraction_level: "domain"

framework_comparison:
  - compared_to: "OCEL"
    relationship: "describes"
    details: "OCEL standard for object-centric event data with multiple case notions"
    source: "Chunk 1:431-433"
  - compared_to: "BPMN 2.0"
    relationship: "references"
    details: "Uses BPMN 2.0 activity lifecycle model for event types"
    source: "Chunk 1:183-186"
  - compared_to: "OnProm/ODBA"
    relationship: "references"
    details: "Discusses ontology-based data access for event log extraction from databases"
    source: "Chunk 1:428-431"
  - compared_to: "XES"
    relationship: "defines"
    details: "Core paper for XES IEEE standard event data structure"
    source: "Chunk 1:163-175"

# HIGH PRIORITY FIELDS (6-10: AI focus)
ai_integration: "N/A - paper predates LLM/AI integration discussion"
agent_modeling: "N/A - paper focuses on event data structure, not agent modeling"
agentic_workflows: "N/A - paper predates agentic workflow patterns"
generative_ai_patterns: "N/A - paper predates generative AI patterns"
agent_ontology_integration: "N/A - paper predates AI-ontology integration patterns"

# MEDIUM PRIORITY FIELDS
entity_count:
  count: 6
  rationale: "Minimal core entities for process event data: Event, Case, Activity, Trace, Log, Attribute"
  source: "Chunk 1:45-175"

methodology: "bottom-up"

empirical_evidence:
  - type: "Survey"
    description: "XES survey with 289 participants (practitioners, researchers, vendors, end-users)"
    source: "Chunk 1:326-329"
  - type: "Industry patterns"
    description: "Eleven event log imperfection patterns from 20+ Australian industry datasets"
    source: "Chunk 1:579-580"
  - type: "Data quality study"
    description: "60-80% of process mining effort spent on data preprocessing"
    source: "Chunk 1:576-578"

limitations:
  - "Non-IID assumption: event log rows are intrinsically correlated, violating machine learning assumptions (Chunk 1:364-369)"
  - "Data quality issues: comprehensive framework for bad quality data still needed (Chunk 1:529-535)"
  - "Granularity gap: IoT sensor data often too fine-grained for business activities (Chunk 1:319-320)"
  - "Case ID correlation: not always straightforwardly available (Chunk 1:76-79)"

tools_standards:
  - "XES (IEEE Standard 1849-2016)"
  - "OCEL 2.0"
  - "BPMN 2.0"
  - "ProM Import Framework"
  - "XESame"
  - "OnProm"
  - "EVS Model Builder"
  - "XTract"
  - "Eventifier"
  - "CRISP-DM"
  - "PM2 methodology"
---

# Foundations of Process Event Data - Analysis Index

## Paper Overview

- **Source**: 12-Foundations_of_Process_Event_Data.pdf
- **Chunks**: 1 chunk, ~14,300 estimated tokens
- **Analyzed**: 2025-12-28T14:45:00
- **Authors**: Jochen De Weerdt (KU Leuven), Moe Thandar Wynn (QUT)
- **Publication**: Process Mining Handbook, LNBIP 448, pp. 193-211 (2022)

## Key Extractions

### Core Contribution

This foundational chapter from the Process Mining Handbook establishes the ontological structure of process event data. It defines the essential entities (Event, Case, Activity, Trace, Log) and their relationships, specifies the three mandatory requirements for process mining-ready event logs, and provides comprehensive coverage of the XES and OCEL standards.

### Entity Types (Chunk 1:26-175)

| Entity | Definition | Source |
|--------|------------|--------|
| Event | Observed atomic granule of activity | Chunk 1:168 |
| Case | Process instance linked via Case ID | Chunk 1:68-74 |
| Activity | Step executed within process, mapped via labels | Chunk 1:92-102 |
| Trace | Sequence of events for a case | Chunk 1:111 |
| Log | Collection of traces with metadata | Chunk 1:163-169 |
| Attribute | Additional data for events/cases | Chunk 1:130-136 |

### Three Essential Requirements (Chunk 1:62-116)

1. **Case ID** (Requirement 1): Each event linked to a case/process instance
2. **Activity Label** (Requirement 2): Each event corresponds to a process activity
3. **Timestamp** (Requirement 3): Events have ordering via timestamps

### Event Log Preparation Trident (Chunk 1:383-523)

| Technique | Purpose | Key Methods |
|-----------|---------|-------------|
| Extraction | Obtain event data from source systems | Connectors, ODBA, OnProm |
| Correlation | Map events to cases (Case ID generation) | ETL, data virtualization, attribute-based |
| Abstraction | Map low-level events to business activities | Clustering, pattern-based, supervised learning |

### Framework Comparisons

| Framework | Relationship | Details | Source |
|-----------|--------------|---------|--------|
| XES | Core standard | IEEE 1849-2016 for event data interchange | Chunk 1:163-175 |
| OCEL | Extension | Object-centric event logs with multiple case notions | Chunk 1:431-433 |
| BPMN 2.0 | Activity lifecycle | State machine for activity execution states | Chunk 1:183-186 |
| OnProm/ODBA | Extraction method | Ontology-based data access for event extraction | Chunk 1:428-431 |

### Data Quality Dimensions (Chunk 1:526-625)

Four broad quality dimensions identified:
1. **Missing data**: Events, attributes, case IDs not recorded
2. **Incorrect data**: Data items recorded incorrectly
3. **Imprecise data**: Values too coarse for analysis
4. **Irrelevant data**: Noise in event logs

Eleven imperfection patterns identified from 20+ industry datasets (Chunk 1:579-583).

## Chunk Navigation

### Chunk 1: Complete Paper (Lines 1-855)

- **Summary**: Comprehensive coverage of process event data foundations. Defines core entity structure (Event, Case, Activity, Trace, Log), establishes three essential requirements for event logs, discusses XES/OCEL standards, covers event log preparation (extraction, correlation, abstraction), and addresses data quality considerations for process mining.

- **Key concepts**:
  - Event log structure
  - Three essential requirements (Case ID, Activity, Timestamp)
  - XES IEEE Standard
  - OCEL object-centric event logs
  - Event log preparation (extraction, correlation, abstraction)
  - Data quality dimensions
  - Event abstraction techniques
  - Activity lifecycle models

- **Key quotes**:
  - Line 26-34: "events in an event log... are related to each other in terms of time and by means of an overarching case dimension"
  - Line 68-69: "each event should be linked to a case or process instance, typically by using a Case ID"
  - Line 163-165: "eXtensible Event Stream (XES) standard, an IEEE Standards Association-approved language to transport, store, and exchange event data"
  - Line 431-433: "the recently introduced OCEL standard... putting forward a general standard to interchange object-centric event data with multiple case notions"
  - Line 476-480: "abstraction techniques can be considered as mapping techniques that can translate one or more lower-level events into higher-level events pertaining to business process activities"

- **Load when**:
  - "What is the structure of process event logs?"
  - "What are the requirements for event data in process mining?"
  - "How do XES and OCEL standards work?"
  - "What is event abstraction in process mining?"
  - "How to extract event logs from enterprise systems?"
  - "What are data quality issues in process mining?"
  - "How to correlate events to cases?"

## Relevance to Research Questions

### Ontology Grounding
This paper provides the **empirical grounding layer** for process-oriented ontologies. The Event-Case-Activity-Trace-Log structure maps directly to:
- **UFO**: Events as perdurants, Cases as endurants
- **PROV-O**: Activity-Entity relationships
- **BBO**: BPMN activity lifecycle alignment

### Entity Validation
The six core entities (Event, Case, Activity, Trace, Log, Attribute) partially validate the 8-entity hypothesis:
- **Event**: Directly covered
- **Activity/Task**: Activity entity
- **Data**: Attribute entity (partial)
- **Agent/Resource**: Mentioned but not formalized as core entity

### Standards Integration
Strong coverage of technical standards:
- XES (IEEE 1849-2016) for event interchange
- OCEL for object-centric processes
- BPMN 2.0 activity lifecycle
- Integration with CRISP-DM and PM2 methodologies

### AI Integration Gap
Paper predates LLM/AI agent discussion. However, provides foundation for:
- Event log as knowledge source for AI agents
- Ontological structure for process-aware AI systems
- Data quality requirements for reliable AI reasoning
