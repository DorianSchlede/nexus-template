---
paper_id: "22-RPA_Framework_BPM_Activities"
title: "A framework to evaluate the viability of robotic process automation for business process activities"
authors:
  - "Christian Wellmann"
  - "Matthias Stierle"
  - "Sebastian Dunzer"
  - "Martin Matzner"
year: 2020
venue: "RPA Forum at BPM 2020"
doi: "10.1007/978-3-030-58779-6_14"
chunks_expected: 1
chunks_read: 1
analysis_complete: true
high_priority_fields_found: 5

# HIGH PRIORITY FIELDS

entity_types:
  - "Activity"
  - "Task"
  - "Agent/Robot"
  - "Resource"
  - "Data"
  - "System"

entity_definitions:
  Activity: "A process step that can be evaluated for RPA viability based on 13 criteria across 5 perspectives (Chunk 1:325-327)"
  RPA: "An automation technology which performs work on the presentation layer, can be set up by a business user, and is managed on a centralized platform (Chunk 1:107-109)"
  Standardization: "A process's degree of structure where every process element is unambiguous and execution order remains the same (Chunk 1:326-331)"
  Maturity: "Indicates no frequent changes to process flow; processes are specified and predictable over time (Chunk 1:332-334)"
  Determinism: "Activities consisting of logical execution steps without cognitive assessment; rule-based without human judgment (Chunk 1:335-340)"
  FailureRate: "Amount of deviations from ideal process flow caused by failures; unsuccessful terminations and rework loops (Chunk 1:341-344)"

entity_relationships:
  - from: "Agent"
    to: "Activity"
    relationship: "performs"
    source: "Chunk 1:539-540"
  - from: "Activity"
    to: "Data"
    relationship: "processes"
    source: "Chunk 1:365-370"
  - from: "Activity"
    to: "System"
    relationship: "interacts_with"
    source: "Chunk 1:377-382"
  - from: "Resource"
    to: "Task"
    relationship: "executes"
    source: "Chunk 1:311-313"
  - from: "Robot"
    to: "Activity"
    relationship: "automates"
    source: "Chunk 1:89-95"

abstraction_level: "application"

framework_comparison:
  - compared_to: "Process Mining"
    relationship: "integrates_with"
    details: "Uses event logs and process mining software (Celonis) to evaluate RPA viability criteria"
    source: "Chunk 1:422-426"
  - compared_to: "BPM"
    relationship: "extends"
    details: "Framework specifically targets BPM activities for RPA assessment"
    source: "Chunk 1:16-23"

# AI-RELATED FIELDS (N/A - paper predates LLM era)

ai_integration: "N/A - paper published 2020, predates LLM/AI integration discussion"

agent_modeling:
  - aspect: "Robot Agent"
    description: "Software robots that mimic human execution on presentation layer"
    source: "Chunk 1:89-95"
  - aspect: "Human Agent"
    description: "Users involved in process execution, counted as resources"
    source: "Chunk 1:311-313"

agentic_workflows: "N/A - paper focuses on single-task RPA automation rather than multi-agent orchestration"

generative_ai_patterns: "N/A - paper predates LLM/generative AI discussion"

agent_ontology_integration: "N/A - no ontology-AI integration discussed"

# MEDIUM PRIORITY FIELDS

entity_count:
  count: 6
  rationale: "Implicit entities derived from 5 framework perspectives: Activity, Task, Agent/Robot, Resource, Data, System"
  source: "Chunk 1:235-236"

methodology: "bottom-up"

empirical_evidence:
  - type: "Event log analysis"
    description: "BPI Challenge 2019 dataset with 1.5M events, 251,734 cases from P2P process of multinational enterprise"
    source: "Chunk 1:433-438"
  - type: "Case study"
    description: "Applied to 'Change Quantity' activity in SAP ECC P2P process"
    source: "Chunk 1:441-443"

limitations:
  - "Single dataset validation only (Chunk 1:595-597)"
  - "Missing UI interaction data prevents determinism assessment (Chunk 1:561-572)"
  - "Cannot distinguish system vs human errors in exceptions (Chunk 1:564-566)"
  - "Qualitative criteria not fully testable with event logs (Chunk 1:598-600)"

tools_standards:
  - "Process Mining"
  - "Celonis"
  - "SAP ECC"
  - "Event Logs"
  - "PAIS (Process-Aware Information Systems)"
---

# A framework to evaluate the viability of robotic process automation for business process activities - Analysis Index

## Paper Overview

- **Source**: 22-RPA_Framework_BPM_Activities.pdf
- **Chunks**: 1 chunk, ~10,750 estimated tokens
- **Analyzed**: 2025-12-28T14:45:00Z
- **Authors**: Wellmann, Stierle, Dunzer, Matzner (FAU Erlangen-Nurnberg)

## Key Extractions

This paper presents the **Process Characteristics Evaluation Framework (PCEF)** for assessing RPA viability of business process activities. Based on a literature review of 21 papers, it identifies 13 criteria grouped into 5 perspectives.

### Entity Types (Implicit from Framework)

| Entity | Role in Framework | Source |
|--------|-------------------|--------|
| Activity | Unit of evaluation for RPA viability | Chunk 1:325-327 |
| Task | Synonym for activity in task perspective | Chunk 1:259 |
| Agent/Robot | Software robots mimicking human execution | Chunk 1:89-95 |
| Resource | Human users performing tasks | Chunk 1:311-313 |
| Data | Structured information processed between systems | Chunk 1:289 |
| System | Information systems with interfaces | Chunk 1:377-382 |

### Framework Structure: 5 Perspectives, 13 Criteria

| Perspective | Criteria | Source |
|-------------|----------|--------|
| Task | Standardization, Maturity, Determinism, Failure Rate | Chunk 1:259-344 |
| Time | Frequency, Duration, Urgency | Chunk 1:347-359 |
| Data | Structuredness | Chunk 1:365-374 |
| System | Interfaces, Stability, Number of Systems | Chunk 1:377-394 |
| Human | Resources, Proneness to Human Error | Chunk 1:397-416 |

### Key Definitions

- **Standardization** (Chunk 1:326-331): "A process's degree of structure. In standardized processes, every process element is unambiguous, and the execution order remains the same in each process instance."

- **Determinism** (Chunk 1:335-340): "Deterministic activities consist of logical execution steps without any form of cognitive assessment... human judgment aggravates automation."

- **RPA** (Chunk 1:107-109): "An automation technology which performs work on the presentation layer, can be set up by a business user, and is managed on a centralized platform."

### Empirical Validation

| Metric | Value | Source |
|--------|-------|--------|
| Events | 1.5 million | Chunk 1:433 |
| Cases | 251,734 purchase order items | Chunk 1:433-434 |
| Process Variants | 136 | Chunk 1:437-438 |
| Users Analyzed | 138 different users | Chunk 1:539-540 |
| Failure Rate Found | 5.33% | Chunk 1:506 |

## Chunk Navigation

### Chunk 1: Full Paper (Lines 1-728)

**Summary**: Complete paper covering introduction to RPA, literature review producing concept matrix of 20 process characteristics, the PCEF framework with 5 perspectives and 13 criteria, empirical evaluation using BPI Challenge 2019 P2P dataset, and conclusions with limitations.

**Key concepts**:
- RPA viability assessment
- Process characteristics evaluation
- 5 perspectives (Task, Time, Data, System, Human)
- 13 evaluation criteria
- Process mining integration
- Event log analysis

**Key quotes**:
- Line 107-109: "we define RPA as an automation technology which performs work on the presentation layer"
- Line 235-236: "five perspectives - task, time, data, system, and human"
- Line 326-327: "standardization refers to a process's degree of structure"
- Line 335-337: "Determinism is one of the most distinctive criteria to assess the viability of RPA"
- Line 422-425: "The evaluation focuses on event logs generated through PAIS"

**Load when**:
- "RPA viability assessment criteria"
- "How to evaluate process activities for automation"
- "Process characteristics for RPA selection"
- "PCEF framework"
- "Task perspective for automation"
- "Process mining for RPA assessment"

## Relevance to Research Question

**Moderate relevance (3/5)** to the ontologies research question.

**Strengths**:
- Provides implicit entity taxonomy through framework perspectives (Activity, Task, Resource, Data, Agent, System)
- Strong empirical grounding with process mining validation
- Clear entity relationships (Agent-performs-Activity, Activity-processes-Data)

**Limitations**:
- No engagement with foundational ontologies (UFO, PROV-O, BBO)
- Application-level framework rather than formal ontology
- Pre-dates AI/LLM integration (2020)
- Entity definitions are pragmatic rather than ontologically grounded

**Synthesis Notes**:
- Use for practical automation-focused entity categorization
- Framework perspectives map loosely to 8-entity hypothesis: Task/Activity, Resource, Data, Agent (Robot + Human)
- Missing explicit: Goal, Rule, Event, Role (though implicitly present in criteria like standardization, determinism)
