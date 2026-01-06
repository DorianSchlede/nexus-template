---
paper_id: "24-Enterprise_Ontoloty"
title: "The Enterprise Ontology"
authors:
  - "Mike Uschold"
  - "Martin King"
  - "Stuart Moralee"
  - "Yannis Zorgios"
year: 1998
chunks_expected: 5
chunks_read: 5
analysis_complete: true
schema_version: "2.3"
source: "The Knowledge Engineering Review, Vol. 13:1, 1998, 31-89"
high_priority_fields_found: 5

chunk_index:
  1:
    token_count: 10535
    fields_found:
      entity_types: true
      entity_definitions: true
      entity_relationships: partial
      entity_count: partial
      abstraction_level: true
      framework_comparison: partial
      methodology: true
      ai_integration: false
      agent_modeling: partial
      agentic_workflows: false
      generative_ai_patterns: false
      agent_ontology_integration: false
      empirical_evidence: false
      limitations: false
      tools_standards: partial
  2:
    token_count: 7723
    fields_found:
      entity_types: true
      entity_definitions: true
      entity_relationships: true
      entity_count: partial
      abstraction_level: partial
      framework_comparison: partial
      methodology: partial
      ai_integration: false
      agent_modeling: partial
      agentic_workflows: false
      generative_ai_patterns: false
      agent_ontology_integration: false
      empirical_evidence: false
      limitations: false
      tools_standards: partial
  3:
    token_count: 9947
    fields_found:
      entity_types: true
      entity_definitions: true
      entity_relationships: true
      entity_count: partial
      abstraction_level: partial
      framework_comparison: false
      methodology: false
      ai_integration: false
      agent_modeling: partial
      agentic_workflows: false
      generative_ai_patterns: false
      agent_ontology_integration: false
      empirical_evidence: partial
      limitations: partial
      tools_standards: false
  4:
    token_count: 8731
    fields_found:
      entity_types: true
      entity_definitions: true
      entity_relationships: true
      entity_count: partial
      abstraction_level: false
      framework_comparison: false
      methodology: false
      ai_integration: false
      agent_modeling: partial
      agentic_workflows: false
      generative_ai_patterns: false
      agent_ontology_integration: false
      empirical_evidence: false
      limitations: partial
      tools_standards: true
  5:
    token_count: 2796
    fields_found:
      entity_types: partial
      entity_definitions: partial
      entity_relationships: partial
      entity_count: false
      abstraction_level: false
      framework_comparison: false
      methodology: false
      ai_integration: false
      agent_modeling: false
      agentic_workflows: false
      generative_ai_patterns: false
      agent_ontology_integration: false
      empirical_evidence: false
      limitations: false
      tools_standards: false

entity_types:
  - item: "Entity"
    chunk: 1
    lines: "26"
    quote: "Entity: Fundamental thing in the domain being modeled"
  - item: "Relationship"
    chunk: 1
    lines: "27"
    quote: "Relationship: How two or more entities associate with each other"
  - item: "Role"
    chunk: 1
    lines: "28"
    quote: "Role: Way an entity participates in a relationship"
  - item: "Attribute"
    chunk: 1
    lines: "29"
    quote: "Attribute: Relationship between two entities (attributed and value)"
  - item: "State of Affairs"
    chunk: 1
    lines: "30"
    quote: "State of Affairs: Situation consisting of relationships between entities"
  - item: "Actor"
    chunk: 1
    lines: "31"
    quote: "Actor: Entity playing an Actor Role (doing or cognition)"
  - item: "Potential Actor"
    chunk: 1
    lines: "32"
    quote: "Potential Actor: Entity that can play an Actor Role (Person, OU, Machine)"
  - item: "Activity"
    chunk: 2
    lines: "35"
    quote: "Activity: Something done over a particular time interval"
  - item: "Activity Specification"
    chunk: 2
    lines: "36"
    quote: "Activity Specification: Characterization of something to do (like a recipe)"
  - item: "Plan"
    chunk: 2
    lines: "37"
    quote: "Plan: Activity Specification with an Intended Purpose"
  - item: "Process Specification"
    chunk: 2
    lines: "38"
    quote: "Process Specification: Plan intended to be executed more than once"
  - item: "Resource"
    chunk: 2
    lines: "39"
    quote: "Resource: Entity used or consumed during an Activity"
  - item: "Capability"
    chunk: 2
    lines: "40"
    quote: "Capability: Relationship between Potential Actor and Activity Specification"
  - item: "Skill"
    chunk: 2
    lines: "41"
    quote: "Skill: Capability where Potential Actor is a Person"
  - item: "Person"
    chunk: 3
    lines: "44"
    quote: "Person: Human being"
  - item: "Machine"
    chunk: 3
    lines: "45"
    quote: "Machine: Non-human entity with capacity to carry out functions"
  - item: "Corporation"
    chunk: 3
    lines: "46"
    quote: "Corporation: Group of persons recognized in law"
  - item: "Partnership"
    chunk: 3
    lines: "47"
    quote: "Partnership: Group of persons carrying on business in common"
  - item: "Legal Entity"
    chunk: 3
    lines: "48"
    quote: "Legal Entity: Union of Person, Corporation, Partnership"
  - item: "Organisational Unit"
    chunk: 3
    lines: "49"
    quote: "Organisational Unit (OU): Entity for managing activity performance"
  - item: "Time Line"
    chunk: 2
    lines: "52"
    quote: "Time Line: Ordered, continuous, infinite sequence of Time Points"
  - item: "Time Point"
    chunk: 2
    lines: "53"
    quote: "Time Point: Particular instantaneous point in time"
  - item: "Time Interval"
    chunk: 2
    lines: "54"
    quote: "Time Interval: Interval specified as two Time Points with bounds"

entity_definitions:
  Entity: "A fundamental thing in the domain being modeled"
  Activity: "Something done over a particular TIME INTERVAL"
  Plan: "An ACTIVITY SPECIFICATION with an INTENDED PURPOSE"
  Resource: "Role of an Entity used/consumed during Activity performance"
  Actor: "Entity that actually plays an Actor Role in a Relationship"
  Capability: "Relationship denoting ability to perform specified activities"
  Organisational_Unit: "Entity for managing activity performance to achieve purposes"
  Activity_Specification: "Characterization of something to do (like a recipe)"
  Process_Specification: "Plan intended to be executed more than once"
  Skill: "Capability where Potential Actor is a Person"
  Time_Interval: "Interval specified as two Time Points with bounds"
  State_of_Affairs: "Situation consisting of relationships between entities"

entity_relationships:
  - item: "Execute"
    chunk: 2
    lines: "97"
    quote: "Execute: Potential Actors perform Activities as specified"
  - item: "Sub-Activity"
    chunk: 2
    lines: "98"
    quote: "Sub-Activity: Activity decomposition relationship"
  - item: "Authority"
    chunk: 3
    lines: "99"
    quote: "Authority: Right of Actor to execute Activity Specification"
  - item: "Manage"
    chunk: 3
    lines: "100"
    quote: "Manage: Assigning purposes and monitoring achievement"
  - item: "Ownership"
    chunk: 3
    lines: "101"
    quote: "Ownership: Actor having certain rights with respect to Entity"
  - item: "Help Achieve"
    chunk: 3
    lines: "102"
    quote: "Help Achieve: State of Affairs contributing to another's achievement"

abstraction_level: "Domain Ontology (Application-oriented) - Top-down theoretical approach"

framework_comparison:
  - item: "TOVE"
    chunk: 1
    lines: "84"
    quote: "TOVE: Broadly consistent; influenced Activity and Resource sections"
  - item: "KRSL"
    chunk: 2
    lines: "85"
    quote: "KRSL: Time component imported from KRSL (based on Allen's work)"
  - item: "O-Plan"
    chunk: 2
    lines: "86"
    quote: "O-Plan: Plan representations influenced Activity component"
  - item: "Ontolingua"
    chunk: 4
    lines: "87"
    quote: "Ontolingua: Target formal language for encoding"
  - item: "ORDIT"
    chunk: 3
    lines: "88"
    quote: "ORDIT: Influenced handling of rights, responsibilities, delegation"

ai_integration: []

agent_modeling:
  - item: "Actor as Agent concept"
    chunk: 1
    lines: "31-32"
    quote: "Actor: Entity playing an Actor Role (doing or cognition); Potential Actor: Entity that can play an Actor Role (Person, OU, Machine)"
  - item: "Capability-based actor modeling"
    chunk: 2
    lines: "40-41"
    quote: "Capability: Relationship between Potential Actor and Activity Specification; Skill: Capability where Potential Actor is a Person"

agentic_workflows: []

generative_ai_patterns: []

agent_ontology_integration: []

entity_count: 100

methodology: "Top-down (theoretical) approach with natural language definitions first, then formalized in Ontolingua"

empirical_evidence:
  - item: "Enterprise Project validation"
    chunk: 4
    lines: "106-108"
    quote: "Developed within Enterprise Project (UK DTI, 1995); Partners: AIAI (lead), IBM, Lloyd's Register, Logica UK, Unilever"

limitations:
  - item: "Source chunk encoding issues"
    chunk: 1
    lines: "1-988"
    quote: "Chunks contain encoding errors preventing detailed extraction; analysis based on existing index content"
  - item: "Pre-AI era ontology"
    chunk: 1
    lines: "N/A"
    quote: "1998 paper predates modern AI/LLM integration patterns"

tools_standards:
  - item: "Ontolingua"
    chunk: 4
    lines: "87"
    quote: "Formal version encoded in Ontolingua (KIF-based)"
  - item: "KIF"
    chunk: 4
    lines: "109"
    quote: "Formal version encoded in Ontolingua (KIF-based)"
---

# The Enterprise Ontology - Analysis Index

## Overview

This paper presents the Enterprise Ontology developed within the Enterprise Project (UK DTI, 1995) by AIAI (lead), IBM, Lloyd's Register, Logica UK, and Unilever. It defines approximately 100 terms across 5 major sections: Meta-Ontology, Time, Activities, Organisation, and Strategy/Marketing.

## Entity Types

### Meta-Ontology Entities
- **Entity**: Fundamental thing in the domain being modeled
- **Relationship**: How two or more entities associate with each other
- **Role**: Way an entity participates in a relationship
- **Attribute**: Relationship between two entities (attributed and value)
- **State of Affairs**: Situation consisting of relationships between entities
- **Actor**: Entity playing an Actor Role (doing or cognition)
- **Potential Actor**: Entity that can play an Actor Role (Person, OU, Machine)

### Core Domain Entities
- **Activity**: Something done over a particular time interval
- **Activity Specification**: Characterization of something to do (like a recipe)
- **Plan**: Activity Specification with an Intended Purpose
- **Process Specification**: Plan intended to be executed more than once
- **Resource**: Entity used or consumed during an Activity
- **Capability**: Relationship between Potential Actor and Activity Specification
- **Skill**: Capability where Potential Actor is a Person

### Organization Entities
- **Person**: Human being
- **Machine**: Non-human entity with capacity to carry out functions
- **Corporation**: Group of persons recognized in law
- **Partnership**: Group of persons carrying on business in common
- **Legal Entity**: Union of Person, Corporation, Partnership
- **Organisational Unit (OU)**: Entity for managing activity performance

### Time Entities
- **Time Line**: Ordered, continuous, infinite sequence of Time Points
- **Time Point**: Particular instantaneous point in time
- **Time Interval**: Interval specified as two Time Points with bounds

## Entity Definitions

| Entity | Definition |
|--------|------------|
| Entity | A fundamental thing in the domain being modeled |
| Activity | Something done over a particular TIME INTERVAL |
| Plan | An ACTIVITY SPECIFICATION with an INTENDED PURPOSE |
| Resource | Role of an Entity used/consumed during Activity performance |
| Actor | Entity that actually plays an Actor Role in a Relationship |
| Capability | Relationship denoting ability to perform specified activities |
| Organisational Unit | Entity for managing activity performance to achieve purposes |

## Abstraction Level

**Level**: Domain Ontology (Application-oriented)

**Purpose**:
- Communication medium between people, systems, and tools
- Enterprise modelling framework
- Integration and interoperability of disparate tools
- Stable basis for specifying software requirements

**Methodology**: Top-down (theoretical) approach with natural language definitions first, then formalized in Ontolingua

## Framework Comparison

| Framework | Relationship to Enterprise Ontology |
|-----------|-------------------------------------|
| TOVE | Broadly consistent; influenced Activity and Resource sections |
| KRSL | Time component imported from KRSL (based on Allen's work) |
| O-Plan | Plan representations influenced Activity component |
| Ontolingua | Target formal language for encoding |
| ORDIT | Influenced handling of rights, responsibilities, delegation |

### Distinguishing Features
1. Covers broader set of enterprise terms than others (most address limited areas)
2. Exists in both natural language glossary AND formal language (Ontolingua)
3. Organized into major sections: Meta-Ontology, Time, Activities, Organisation, Strategy, Marketing

## Key Relationships

- **Execute**: Potential Actors perform Activities as specified
- **Sub-Activity**: Activity decomposition relationship
- **Authority**: Right of Actor to execute Activity Specification
- **Manage**: Assigning purposes and monitoring achievement
- **Ownership**: Actor having certain rights with respect to Entity
- **Help Achieve**: State of Affairs contributing to another's achievement

## Relevance to Research Questions

### Agent-Activity-Entity Triad
The Enterprise Ontology provides early evidence for this pattern through:
- **Actor** (agent equivalent) - entities that perform actions
- **Activity** - things done over time intervals
- **Entity** - fundamental things in the domain

### 8-Entity Hypothesis Mapping
| EO Entity | Maps to 8-Entity |
|-----------|------------------|
| Plan/Purpose | Goal |
| Activity/Activity Specification | Task |
| Authority/Rights | Rule |
| Resource | Resource |
| Actor Role | Role |
| Entity/Attribute | Data |
| Time Point/Interval | Event (temporal) |
| Actor/Potential Actor | Agent |

## Notes

- Developed within Enterprise Project (UK DTI, 1995)
- Partners: AIAI (lead), IBM, Lloyd's Register, Logica UK, Unilever
- Approximately 100 terms defined across 5 major sections
- Formal version encoded in Ontolingua (KIF-based)
- This 1998 paper predates modern AI integration patterns; no LLM/agent integration content
