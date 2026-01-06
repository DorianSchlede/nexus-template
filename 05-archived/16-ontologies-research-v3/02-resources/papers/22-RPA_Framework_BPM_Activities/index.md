---
paper_id: "22-RPA_Framework_BPM_Activities"
title: "A framework to evaluate the viability of robotic process automation for business process activities"
authors:
  - "Christian Wellmann"
  - "Matthias Stierle"
  - "Sebastian Dunzer"
  - "Martin Matzner"
year: 2020
chunks_expected: 1
chunks_read: 1
analysis_complete: true
schema_version: "2.3"

chunk_index:
  1:
    token_count: 10331
    fields_found:
      entity_types: true
      entity_definitions: true
      entity_relationships: true
      entity_count: true
      abstraction_level: true
      framework_comparison: partial
      methodology: true
      ai_integration: partial
      agent_modeling: partial
      agentic_workflows: false
      generative_ai_patterns: false
      agent_ontology_integration: false
      empirical_evidence: true
      limitations: true
      tools_standards: true

entity_types:
  - item: "Process Activity"
    chunk: 1
    lines: "62-63"
    quote: "What are the characteristics of a process activity, or a set of process activities, that facilitate viable robotic process automation?"
  - item: "Software Robot/Bot"
    chunk: 1
    lines: "88-90"
    quote: "This is achieved by the application of software algorithms known as software robots or bots, which are imitating the execution flow of humans on the front-end"
  - item: "Task"
    chunk: 1
    lines: "235-236"
    quote: "We present five perspectives - task, time, data, system, and human - that contain several characteristics that analysts can use to evaluate a process accordingly"
  - item: "Resource"
    chunk: 1
    lines: "311-312"
    quote: "Resources: Number of users performing same task, Number of users involved in process"
  - item: "Event"
    chunk: 1
    lines: "201"
    quote: "the triggering of events, when a task is completed"
  - item: "Data"
    chunk: 1
    lines: "289"
    quote: "Data: Structuredness - Consistent use of data objects"
  - item: "System"
    chunk: 1
    lines: "297-307"
    quote: "System perspective includes Interfaces, Stability, Number of systems"
  - item: "User/Human"
    chunk: 1
    lines: "300-316"
    quote: "Human perspective deals with human computer interaction focusing on the human. The perspective comes with two peculiarities, resources and proneness to human error"
---

# A framework to evaluate the viability of robotic process automation for business process activities

## Summary

This paper presents the **Process Characteristics Evaluation Framework (PCEF)** for assessing the suitability of business process activities for Robotic Process Automation (RPA). The framework consists of **13 criteria** organized into **5 perspectives**: Task, Time, Data, System, and Human.

---

## Entity Definitions

| Entity | Definition | Source |
|--------|------------|--------|
| Process Activity | A discrete step within a business process that can be evaluated for automation suitability based on characteristics like standardization, maturity, determinism, and failure rate | Chunk 1:325-344 |
| Software Robot | Software algorithms that imitate human execution flow on the front-end, interacting with user interfaces through mouse clicks, keyboard interactions, and interpretation of text and graphics | Chunk 1:89-96 |
| RPA | An automation technology which performs work on the presentation layer, can be set up by a business user, and is managed on a centralized platform | Chunk 1:107-109 |
| Standardization | A process's degree of structure where every process element is unambiguous and execution order remains the same in each process instance | Chunk 1:326-331 |
| Maturity | Indicator that no frequent changes to the process flow are observable; processes are specified and predictable over time | Chunk 1:332-334 |
| Determinism | Activities consisting of logical execution steps without any form of cognitive assessment - fundamental requirement for software robots | Chunk 1:335-340 |
| Failure Rate | Self loops to repair previous executions and non-recoverable unsuccessful termination; deviations from ideal process flow caused by failures | Chunk 1:341-344 |

---

## Entity Relationships

| Relationship | Source |
|--------------|--------|
| Framework contains Perspectives: "We present five perspectives - task, time, data, system, and human" | Chunk 1:235-236 |
| Perspectives contain Criteria: Task (standardization, maturity, determinism, failure rate), Time (frequency, duration, urgency), Data (structuredness), System (interfaces, stability, number of systems), Human (resources, proneness to human error) | Chunk 1:247-319 |
| Process Activity evaluated-by Framework: "To support practitioners in evaluating the viability of RPA for process activities, we summarized the findings of our literature review in a framework" | Chunk 1:232-236 |
| Software Robot performs Process Activity: "we define RPA as an automation technology which performs work on the presentation layer" | Chunk 1:107-109 |

---

## Entity Count

**Count**: 13 criteria across 5 perspectives

**Rationale**: "We design a framework that consists of thirteen criteria grouped into five perspectives which offer different evaluation aspects" (Chunk 1:20-21, 580)

The 13 criteria are:
1. Standardization (Task)
2. Maturity (Task)
3. Determinism (Task)
4. Failure Rate (Task)
5. Frequency (Time)
6. Duration (Time)
7. Urgency (Time)
8. Structuredness (Data)
9. Interfaces (System)
10. Stability (System)
11. Number of Systems (System)
12. Resources (Human)
13. Proneness to Human Error (Human)

---

## Abstraction Level

**Level**: Domain/Application-level framework for BPM/RPA evaluation

This is not a foundational ontology but a practical evaluation framework providing 13 criteria across 5 perspectives for assessing process activity suitability for robotic process automation.

---

## Framework Comparison

| Compared To | Relationship | Details | Source |
|-------------|--------------|---------|--------|
| Prior RPA selection methods | Extends | Builds on literature from BPM and RPA domains; extends Wanner et al. criteria with comprehensive literature review | Chunk 1:119-123 |
| Process Mining | Integrates with | Framework designed to be applied using process mining software (Celonis) on event logs | Chunk 1:422-426 |
| Event log standards | Uses | "The evaluation focuses on event logs generated through PAIS. Event logs reveal insights about the business process and its execution" | Chunk 1:422-423 |

---

## AI Integration

**Status**: Partial - Brief mention only

"Although RPA typically favors less complex and cognitive tasks, advances in machine learning can extend the range of RPA application in the future" (Chunk 1:106)

Note: Paper focuses on rule-based RPA, not AI/LLM integration.

---

## Agent Modeling

**Status**: Partial - Minimal treatment

Software robots are treated as deterministic automation tools that mimic human user actions on the presentation layer. They are non-autonomous, rule-based execution agents without intentionality or BDI characteristics.

"Software algorithms known as software robots or bots, which are imitating the execution flow of humans on the front-end" (Chunk 1:88-90)

---

## Agentic Workflows

**Status**: Not addressed

Paper discusses single-robot automation of individual activities, not multi-agent orchestration or collaboration patterns.

---

## Generative AI Patterns

**Status**: Not addressed

Paper predates LLM era (2020); focuses on rule-based RPA without generative AI components.

---

## Agent Ontology Integration

**Status**: Not addressed

No ontology-based reasoning or knowledge graph integration discussed.

---

## Methodology

**Approach**: Bottom-up empirical approach combining literature review with practical validation

- Conducted systematic literature review using Scopus, Google Scholar, IEEE Xplore to identify process characteristics from 21 papers
- Framework validated against real-life BPI Challenge 2019 dataset (P2P process from multinational coatings enterprise)
- Used process mining software (Celonis) for analysis

Source: Chunk 1:119-123, 422-427

---

## Empirical Evidence

| Evidence Type | Details | Source |
|---------------|---------|--------|
| BPI Challenge 2019 dataset validation | "In total, the data set includes more than 1.5 million events, and 251,734 purchase order items (cases) in 76,349 purchase orders... These filters result in 197,010 cases with 136 process variants" | Chunk 1:433-438 |
| Change Quantity activity analysis | "The average number of 'Change Quantity' occurrences is 31 times a day" | Chunk 1:507-508 |
| Process duration impact | "while processes without have an average throughput time of 64 days, processes including the activity take 93 days on average" | Chunk 1:518-520 |
| Failure rate measurement | "Reworking 'Change Quantity' occurs in 3,91%, and the process determination with order item deletion happens in 1,42%... The resulting failure rate of the process is 5,33%" | Chunk 1:501-506 |
| User involvement | "Analyzing the number of users that execute the 'Change Quantity' unveils that 138 different users execute the task" | Chunk 1:539-540 |

---

## Limitations

| Limitation | Source |
|------------|--------|
| Single dataset validation: "Despite the demonstration and application of the framework, it is tested only with one data set and process" | Chunk 1:595-597 |
| Cannot evaluate determinism from event logs: "The event log does not include information about the performance of the activity 'Change Quantity' on the presentation layer. Therefore, the criterion can not be evaluated for this data set" | Chunk 1:496-500 |
| Missing front-end interaction data: "crucial information about the interaction on the user interface is missing and prevents the examination of the criteria determinism, structuredness of data, interfaces and number of systems" | Chunk 1:566-572 |
| Anonymized dataset constraints: "the data set was anonymized and modified before publishing, limiting the accessible information stored in the event logs" | Chunk 1:606-607 |
| Qualitative criteria not fully tested: "the framework contains qualitative criteria that could not be tested with the data set. Further evaluation of these criteria - e.g. through case studies - is necessary" | Chunk 1:598-600 |

---

## Tools and Standards

| Tool/Standard | Source |
|---------------|--------|
| Process Mining Software (Celonis): "We determine process characteristics with Process Mining Software... https://www.celonis.com" | Chunk 1:425, 455 |
| Event Logs / PAIS: "The evaluation focuses on event logs generated through PAIS" | Chunk 1:422 |
| SAP ECC: "Since the event log originates from an SAP ECC system" | Chunk 1:535 |
| User Interaction Logger: "the use of an user interaction logger can bridge the gap between front-end and back-end information gathering" | Chunk 1:571 |
| BPI Challenge 2019 Dataset | Chunk 1:654-656 |

---

## 8-Entity Hypothesis Mapping

| PCEF Entity | Maps to Hypothesis Entity | Coverage |
|-------------|---------------------------|----------|
| Process Activity | Task | Strong |
| Software Robot | Agent | Partial |
| Resource (User) | Role | Partial |
| Data | Data | Strong |
| Event | Event | Partial |
| Rule-based criteria | Rule | Partial |
| System | Resource | Partial |
| Goal (implicit) | Goal | Weak |

---

## Key Contributions

1. **PCEF Framework**: 13 criteria across 5 perspectives (Task, Time, Data, System, Human) for evaluating process activities for RPA suitability
2. **Literature Synthesis**: Concept matrix from 21 papers identifying RPA-relevant process characteristics
3. **Empirical Validation**: Demonstrated framework application on BPI Challenge 2019 dataset
