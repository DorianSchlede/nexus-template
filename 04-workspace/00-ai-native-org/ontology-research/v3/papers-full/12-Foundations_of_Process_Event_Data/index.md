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
schema_version: "2.3"

chunk_index:
  1:
    token_count: 13785
    fields_found:
      entity_types: true
      entity_definitions: true
      entity_relationships: true
      entity_count: false
      abstraction_level: partial
      framework_comparison: partial
      methodology: true
      ai_integration: false
      agent_modeling: false
      agentic_workflows: false
      generative_ai_patterns: false
      agent_ontology_integration: partial
      empirical_evidence: true
      limitations: true
      tools_standards: true

entity_types:
  - item: "Event"
    chunk: 1
    lines: "32-33"
    quote: "events in an event log, which can be considered as the observations (rows) in our dataset"
  - item: "Case/Process Instance"
    chunk: 1
    lines: "68-72"
    quote: "each event should be linked to a case or process instance, typically by using a Case ID"
  - item: "Activity"
    chunk: 1
    lines: "92-94"
    quote: "each event should correspond to an activity executed within the process"
  - item: "Trace"
    chunk: 1
    lines: "169"
    quote: "IEEE XES specifies the concept of a log, a trace, and an attribute component"
  - item: "Log"
    chunk: 1
    lines: "169"
    quote: "IEEE XES specifies the concept of a log, a trace, and an attribute component"
  - item: "Attribute"
    chunk: 1
    lines: "169-172"
    quote: "an attribute component. Event and/or trace classifiers are used to assign an identity to traces and events"

entity_definitions:
  Event:
    chunk: 1
    lines: "168"
    quote: "In IEEE XES, events are considered as an observed atomic granule of activity"
  Case_ID:
    chunk: 1
    lines: "68-75"
    quote: "each event should be linked to a case or process instance, typically by using a Case ID. This is 'Requirement 1'. In the simple example, each case or process instance will refer to one procurement of a product or service"
  Activity:
    chunk: 1
    lines: "92-102"
    quote: "each event should correspond to an activity executed within the process. More specifically, an assumption is made that there exists a restricted set of labels, reflecting the activities in the business process, to which each event is mapped"
  Timestamp:
    chunk: 1
    lines: "110-116"
    quote: "the last requirement ('Requirement 3') entails that there exists an ordering of the events pertaining to a case. As such, each case logically consists of a sequence of events. Most often, this ordering will be derived from a timestamp attribute"
  Trace:
    chunk: 1
    lines: "169-170"
    quote: "Event and/or trace classifiers are used to assign an identity to traces and events"
  Event_Lifecycle:
    chunk: 1
    lines: "181-186"
    quote: "the concept of event types or lifecycle transitions of activities. When sourcing events from many process-aware information systems, events oftentimes relate to the transactional lifecycle that activities undergo"

entity_relationships:
  - item: "Event belongs-to Case"
    chunk: 1
    lines: "68-69"
    quote: "each event should be linked to a case or process instance"
  - item: "Event corresponds-to Activity"
    chunk: 1
    lines: "92-94"
    quote: "each event should correspond to an activity executed within the process"
  - item: "Events form Trace (sequence)"
    chunk: 1
    lines: "110-112"
    quote: "each case logically consists of a sequence of events"
  - item: "Traces compose Log"
    chunk: 1
    lines: "169"
    quote: "IEEE XES specifies the concept of a log, a trace, and an attribute component"
  - item: "Attribute describes Event/Trace/Log"
    chunk: 1
    lines: "171-174"
    quote: "An extension can be used to define a set of attributes for events, traces and/or logs"

abstraction_level:
  level: "domain"
  chunk: 1
  lines: "14-20"
  quote: "Process event data is a fundamental building block for process mining as event logs portray the execution trails of business processes from which knowledge and insights can be extracted"
  rationale: "Domain-level (Process Mining). This paper operates at the domain level for process mining, defining the fundamental data structures (events, cases, traces, logs) required for process mining analysis. It does not address foundational ontologies like UFO or PROV-O."

framework_comparison:
  - item: "XES vs BPMN 2.0 lifecycle models"
    chunk: 1
    lines: "183-186"
    quote: "One example of such a transactional lifecycle model is shown in Fig. 3a. This is the transition lifecycle model of the BPMN 2.0 standard. Such a transactional lifecycle model describes the states and state transitions which an activity might take in its execution. Also in IEEE XES, a lifecycle extension has been approved"
  - item: "Process mining vs classical data analytics"
    chunk: 1
    lines: "339-345"
    quote: "in comparison to classical data preprocessing stages within an analytics process, starker differences exist at the level of cleaning and transforming data"
  - item: "PM2 vs CRISP-DM methodologies"
    chunk: 1
    lines: "370-375"
    quote: "When making an assessment of one of the most recently introduced process mining methodologies, i.e. PM2, four event data preprocessing tasks are defined... In CRISP-DM, data preparation includes selection, cleaning, construction, integration and formatting of data"

ai_integration: "NOT_FOUND"

agent_modeling: "NOT_FOUND"

agentic_workflows: "NOT_FOUND"

generative_ai_patterns: "NOT_FOUND"

agent_ontology_integration:
  - item: "Ontology-based data access (ODBA) for event log extraction"
    chunk: 1
    lines: "428-431"
    quote: "One noteworthy scientific initiative in this context is ontology-based data access (ODBA) for event log extraction. The approach is based on an ontological view of the domain of interest and linking it as such to a database schema and has been implemented in the Onprom tool"

entity_count: "NOT_FOUND"

methodology:
  approach: "bottom-up"
  chunk: 1
  lines: "259-329"
  quote: "In an online survey with 289 participants spanning the roles of practitioners, researchers, software vendors, and end-users"
  rationale: "The paper takes a practical, empirical approach based on real-world event log requirements from process mining practice. It draws from industry experience and surveys rather than top-down theoretical ontological design."

empirical_evidence:
  - item: "XES survey with 289 participants"
    chunk: 1
    lines: "326-329"
    quote: "In an online survey with 289 participants spanning the roles of practitioners, researchers, software vendors, and end-users, SAP ECC (R/3), SAP S/4 HANA, and Salesforce are selected as the top three most analyzed source systems"
  - item: "Data preprocessing effort estimates"
    chunk: 1
    lines: "232-233"
    quote: "Estimates indicate that 80% of resources in typical data science projects is devoted to data preprocessing"
  - item: "Process mining data quality study"
    chunk: 1
    lines: "576-578"
    quote: "many spending 60-80% of their efforts while some spending up to 90% of their total efforts on this step"
  - item: "11 event log imperfection patterns"
    chunk: 1
    lines: "579-583"
    quote: "Suriadi et al. identified eleven event log imperfection patterns based on their experience with over 20 Australian industry data sets"

limitations:
  - item: "Non-IID data assumption violation"
    chunk: 1
    lines: "364-369"
    quote: "The typical data format of event logs, consisting of events pertaining to cases, make that the 'rows' in event log are intrinsically correlated. This invalidates the assumption of data being independent and identically distributed (IID)"
  - item: "Granularity gap with IoT data"
    chunk: 1
    lines: "319-322"
    quote: "the granularity gap between typical IoT data (sensor readings) and event data is sometimes challenging to bridge"
  - item: "Case ID not always available"
    chunk: 1
    lines: "76-79"
    quote: "it should be pointed out that Case IDs are not always straightforwardly available. This problem has been addressed in both process mining literature, as well as in practice, and is often referred to as event correlation"
  - item: "Activity granularity mismatch"
    chunk: 1
    lines: "103-109"
    quote: "oftentimes, natural log data is stored at lower levels of granularity than desired for analysis purposes... a lot of event data exists for which the granularity level is much lower"

tools_standards:
  - item: "IEEE XES (eXtensible Event Stream)"
    chunk: 1
    lines: "163-175"
    quote: "the eXtensible Event Stream (XES) standard, an IEEE Standards Association-approved language to transport, store, and exchange event data. Its metadata structure is represented in Fig. 2. XES uses the W3C XML Schema definition language"
  - item: "BPMN 2.0"
    chunk: 1
    lines: "183"
    quote: "This is the transition lifecycle model of the BPMN 2.0 standard"
  - item: "OCEL (Object-Centric Event Log) standard"
    chunk: 1
    lines: "431-433"
    quote: "the recently introduced OCEL standard is another relevant piece of work, putting forward a general standard to interchange object-centric event data with multiple case notions"
  - item: "ProM Import Framework"
    chunk: 1
    lines: "416-418"
    quote: "One of the first tools stemming from scientific research was the ProM Import Framework. Already in these early days, the idea of an extensible plug-in architecture allowing to develop adapters to hook into a large variety of systems was proposed"
  - item: "XESame"
    chunk: 1
    lines: "419-420"
    quote: "With the uptake of XES, XESame was developed as a more flexible successor to the ProM Import Framework"
  - item: "Onprom (ODBA tool)"
    chunk: 1
    lines: "428-431"
    quote: "ontology-based data access (ODBA) for event log extraction. The approach is based on an ontological view of the domain of interest and linking it as such to a database schema and has been implemented in the Onprom tool"
  - item: "EVS Model Builder"
    chunk: 1
    lines: "421-422"
    quote: "Other researchers have focused on extraction from ERP systems, e.g. the EVS Model Builder and XTract"
  - item: "JSON format"
    chunk: 1
    lines: "314-315"
    quote: "a default standard for web-based platforms to store data is JSON (JavaScript Object Notation)"
---

# Foundations of Process Event Data

## Summary

This chapter from the Process Mining Handbook (LNBIP 448, 2022) provides a comprehensive foundation for understanding process event data - the core building block for process mining. The paper focuses on practical data requirements rather than foundational ontologies, making it relevant for understanding how process data is structured, extracted, correlated, and quality-assured.

## Key Contributions

### Three Essential Requirements for Event Logs

The paper establishes three fundamental requirements for event logs to be analysis-ready:

1. **Case ID (Requirement 1)**: Each event must be linked to a case or process instance
2. **Activity Label (Requirement 2)**: Each event must correspond to an activity with a restricted set of labels
3. **Timestamp/Ordering (Requirement 3)**: Events within a case must be orderable, typically via timestamps

### Event Log Data Sources

The paper categorizes major sources of event data:
- BPMS (Business Process Management Systems)
- Case management and ticketing systems
- ERP/CRM systems
- Operational databases
- Project management software
- Data warehouses and data lakes
- Web data
- IoT systems

### Event Log Preparation Trident

Three key preparation techniques are identified:
1. **Extraction**: Obtaining event data from source systems
2. **Correlation**: Mapping events to cases when Case IDs are missing
3. **Abstraction**: Translating low-level events to business-understandable activities

### Data Quality Framework

The paper addresses data quality dimensions specific to process mining:
- Missing data
- Incorrect data
- Imprecise data
- Irrelevant data

It documents 11 event log imperfection patterns and discusses detection/repair approaches.

## Relevance to Research Questions

### Relevance to Entity Definitions
- Defines core process mining entities: Event, Case, Trace, Log, Activity, Attribute
- These are domain-level entities, not foundational ontology entities (UFO, PROV-O)

### Relevance to Agent-Activity-Entity Triad
- Limited relevance - no explicit agent modeling
- Activities are defined as executed steps, not as W3C PROV-O activities with agents

### Relevance to AI Integration
- No AI/LLM integration patterns discussed
- Paper predates significant LLM adoption in process mining
- Only mentions ontology-based data access (ODBA) for extraction, not reasoning

## Limitations for This Research

This paper is primarily a **practical technical guide** for process mining data handling rather than an ontological foundation paper. It does not address:
- Foundational ontologies (UFO, PROV-O, BBO)
- Agent modeling or intentional agents
- AI/LLM integration patterns
- Multi-agent systems
- Agentic workflows

However, it provides valuable context on:
- How event data standards (XES, OCEL) structure process information
- The practical challenges of event data preparation
- Data quality considerations for process mining
