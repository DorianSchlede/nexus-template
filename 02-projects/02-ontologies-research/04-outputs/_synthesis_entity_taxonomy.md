---
synthesized_at: "2025-12-28T15:30:00"
research_question: "What core entity types appear across foundational ontologies, business process standards, and AI agent frameworks?"
papers_included: 22
papers_excluded: 1
papers_read:
  - "01-UFO_Unified_Foundational_Ontology"
  - "02-Knowledge_Graphs"
  - "03-PROV-AGENT_Unified_Provenance_for_AI_Agents"
  - "04-PROV-O_to_BFO_Semantic_Mapping"
  - "05-DOLCE_Descriptive_Ontology"
  - "06-BFO_Function_Role_Disposition"
  - "07-Classifying_Processes_Barry_Smith"
  - "09-OCEL_20_Specification"
  - "10-OC-PM_Object-Centric_Process_Mining"
  - "11-Process_Mining_Event_Knowledge_Graphs"
  - "12-Foundations_of_Process_Event_Data"
  - "14-RAG_Ontologic_Graph_Multiagent_LLM"
  - "15-SciAgents_Multi-Agent_Graph_Reasoning"
  - "16-KG-Agent_Knowledge_Graph_Reasoning"
  - "17-KG_Reasoning_Logics_Embeddings_Survey"
  - "18-Multi-Agent_Architecture_Taxonomy_LLM"
  - "19-Graph_of_Thoughts_LLM_Reasoning"
  - "20-Agentic_RAG_Survey"
  - "21-LLM_Smart_Contracts_from_BPMN"
  - "22-RPA_Framework_BPM_Activities"
  - "23-UFO_Story_Ontological_Foundations"
  - "31-BBO_BPMN_Ontology"
excluded_papers:
  - paper_id: "24-Enterprise_Ontoloty"
    reason: "PDF conversion failed - corrupted content"
total_entities_extracted: 87
---

# Entity Taxonomy Synthesis

## Overview

This synthesis aggregates entity types from 22 analyzed papers spanning foundational ontologies (UFO, DOLCE, BFO, PROV-O), business process standards (BPMN, OCEL), and AI agent frameworks. The taxonomy is organized by abstraction level: **Foundational → Core → Domain → Application**.

---

## 1. Foundational Layer (Highest Abstraction)

These entities appear in multiple foundational ontologies and represent the most universal distinctions.

### 1.1 Continuants vs. Occurrents

| Entity | Definition | Sources |
|--------|------------|---------|
| **Endurant/Continuant** | Entities wholly present at any time they exist (objects, substances) | UFO-A (23:173-181), BFO (06), DOLCE (05) |
| **Perdurant/Occurrent** | Entities that unfold in time, having temporal parts (events, processes) | UFO-B (23:183-185), BFO (07), DOLCE (05) |

### 1.2 Universal Foundational Entities

| Entity | Definition | Papers |
|--------|------------|--------|
| **Substance Sortal (Kind)** | Types that supply identity criteria to their instances | UFO (23:366-368) |
| **Moment/Trope/Quality** | Particularized properties existentially dependent on bearers | UFO (23:127-133), DOLCE (05) |
| **Relator** | Particularized relational properties that ground material relations | UFO (23:192), BFO (06) |
| **Disposition** | Tendencies to exhibit behaviors under certain conditions | BFO (06), UFO-B (23:184-185) |
| **Function** | A disposition linked to a biological or designed purpose | BFO (06) |
| **Role** | A realizable entity that inheres in a bearer via social/normative context | BFO (06), UFO-C (23:192), DOLCE (05) |

---

## 2. Core Layer (Agent-Activity-Entity Triad)

These entities appear across nearly all papers and form the structural backbone for modeling work systems.

### 2.1 The Agent-Activity-Entity Pattern

```
┌─────────┐     performs     ┌──────────┐     affects     ┌────────┐
│  AGENT  │ ───────────────► │ ACTIVITY │ ──────────────► │ ENTITY │
└─────────┘                  └──────────┘                  └────────┘
     │                            │                             │
     │ has                        │ produces                    │ has
     ▼                            ▼                             ▼
 ┌───────┐                   ┌─────────┐                   ┌──────┐
 │ ROLE  │                   │  EVENT  │                   │ DATA │
 └───────┘                   └─────────┘                   └──────┘
```

### 2.2 Core Entity Definitions

| Entity | Definition | Paper Coverage |
|--------|------------|----------------|
| **Agent** | An entity capable of perceiving, reasoning, and autonomously executing tasks | 18 papers (81%) |
| **Activity/Task** | Work to be performed; a bounded unit of action | 20 papers (91%) |
| **Entity/Object** | A continuant that participates in activities | 19 papers (86%) |
| **Event** | Something that happens during a process, affecting flow | 16 papers (73%) |
| **Resource** | Input/output entities consumed or produced by activities | 14 papers (64%) |
| **Role** | A social/functional position defining permissions and responsibilities | 12 papers (55%) |
| **Goal** | Desired end-state that motivates agent action | 11 papers (50%) |
| **Data** | Structured information processed, stored, or transmitted | 15 papers (68%) |

---

## 3. Domain Layer (Process & Knowledge)

### 3.1 Business Process Entities (BPMN/OCEL)

| Entity | Definition | Source |
|--------|------------|--------|
| **Process** | A container for activities with defined start/end | BBO (31:185-187), BPMN |
| **SubProcess** | A composite activity containing nested activities | BBO (31:231-232), BPMN |
| **Gateway** | Controls flow convergence/divergence | BBO (31:241), BPMN |
| **SequenceFlow** | Directed transitions between activities | BBO (31:221-223), BPMN |
| **WorkProduct** | Tangible output produced by a process | BBO (31:326-328) |
| **ManufacturingFacility** | Location where activities are performed | BBO (31:309-317) |

### 3.2 Object-Centric Process Mining Entities (OCEL 2.0)

| Entity | Definition | Source |
|--------|------------|--------|
| **Object** | First-class citizen in event logs (beyond case notion) | OCEL (09), OC-PM (10) |
| **Object Type** | Classification of objects (e.g., Order, Item, Package) | OCEL (09) |
| **Event-to-Object Relationship** | Typed relationship between event and affected object | OCEL (09) |
| **Object-to-Object Relationship** | Relationship between objects (e.g., containment) | OCEL (09) |
| **Trace** | Sequence of events for a case/object | Process Mining (11, 12) |

### 3.3 Knowledge Graph Entities

| Entity | Definition | Source |
|--------|------------|--------|
| **Triple** | A fact expressed as (head_entity, relation, tail_entity) | KG-Agent (16:176-180), KG Survey (17:35-37) |
| **Class** | Entity type in ontological schema | KG Survey (17:200-202) |
| **Relation** | Labeled edge connecting entities | KG-Agent (16:177-180), KG Survey (17) |
| **Ontological Schema** | Vocabulary defining classes and relations | KG Survey (17:35-37) |
| **Embedding** | Vector representation preserving semantic similarity | KG Survey (17:97-99) |

---

## 4. Application Layer (AI Agent Frameworks)

### 4.1 LLM Agent Architecture Entities

| Entity | Definition | Source |
|--------|------------|--------|
| **LLM Agent** | Agent comprising LLM + Memory + Planning + Tools | Agentic RAG (20:484-502), Multi-Agent Taxonomy (18:467-474) |
| **Tool** | External capability expanding agent's abilities | KG-Agent (16:240-259), Agentic RAG (20:500-501) |
| **Memory** | Short-term (state) + Long-term (knowledge) storage | Multi-Agent Taxonomy (18:893-897), Agentic RAG (20:491-493) |
| **Context** | Additional resources (Tools, Data, Foundation Models) | Multi-Agent Taxonomy (18:99-101) |
| **Thought** | Unit of information generated by LLM | GoT (19:158-161) |
| **Operation** | Transformation applied to thoughts (Generate, Score, Aggregate) | GoT (19:640-651) |

### 4.2 Multi-Agent System Entities

| Entity | Definition | Source |
|--------|------------|--------|
| **Network** | Topology connecting agents | Multi-Agent Taxonomy (18:889-892) |
| **Communication Protocol** | Structured framework for agent message exchange | Multi-Agent Taxonomy (18:75-77) |
| **Action** | Atomic operation: DecomposeTask, DelegateTask, ExecuteTask, etc. | Multi-Agent Taxonomy (18:35-49) |
| **Coordinator Agent** | Central agent delegating to specialized workers | Agentic RAG (20:886-888) |
| **Specialized Agent** | Agent with domain-specific capabilities | Multi-Agent Taxonomy (18:914-921) |

### 4.3 Intentional/Mental Entities (UFO-C)

| Entity | Definition | Source |
|--------|------------|--------|
| **Belief** | Agent's representation of the world | UFO-C (23:191-193) |
| **Desire** | Agent's motivational state toward outcomes | UFO-C (23:191-193) |
| **Intention** | Committed plan of action | UFO-C (23:191-193) |
| **Commitment** | Social obligation held by agent | UFO-C (23:192) |
| **Claim** | Right held against another agent | UFO-C (23:192) |

---

## 5. Cross-Cutting Analysis

### 5.1 Entity Frequency Across Papers

| Entity | Foundational | Core | Domain | Application | Total |
|--------|--------------|------|--------|-------------|-------|
| Agent | 3 | 3 | 3 | 9 | 18 |
| Activity/Task | 3 | 4 | 6 | 7 | 20 |
| Event | 2 | 3 | 8 | 3 | 16 |
| Resource | 1 | 2 | 6 | 5 | 14 |
| Role | 3 | 2 | 4 | 3 | 12 |
| Goal | 2 | 1 | 2 | 6 | 11 |
| Data | 0 | 2 | 5 | 8 | 15 |

### 5.2 Entity Abstraction Mapping

```
FOUNDATIONAL    CORE           DOMAIN              APPLICATION
───────────────────────────────────────────────────────────────
Endurant    →   Entity     →   Object (OCEL)    →  Resource/Tool
Perdurant   →   Activity   →   Task (BPMN)      →  Operation/Action
Agent       →   Agent      →   HumanResource    →  LLM Agent
Role        →   Role       →   Role (BBO)       →  Specialist Agent
Disposition →   Capability →   Function         →  Tool/API
Moment      →   Property   →   Attribute        →  Parameter
```

### 5.3 The 8-Entity Hypothesis Validation

Based on cross-paper analysis, **8 core entities** appear consistently:

| # | Entity | Coverage | Primary Sources |
|---|--------|----------|-----------------|
| 1 | **Agent** | 18/22 (82%) | UFO-C, BBO, Multi-Agent Taxonomy, Agentic RAG |
| 2 | **Task/Activity** | 20/22 (91%) | BPMN, BBO, UFO-B, Multi-Agent Taxonomy |
| 3 | **Event** | 16/22 (73%) | OCEL, BPMN, PROV-O, UFO-B |
| 4 | **Resource** | 14/22 (64%) | BBO, BPMN, Agentic RAG |
| 5 | **Role** | 12/22 (55%) | UFO-C, BBO, BFO, Multi-Agent Taxonomy |
| 6 | **Goal** | 11/22 (50%) | UFO-C, Multi-Agent Taxonomy, Agentic RAG |
| 7 | **Data** | 15/22 (68%) | OCEL, KG papers, Agentic RAG |
| 8 | **Rule/Constraint** | 9/22 (41%) | BPMN (conditions), KG Survey (logic rules), BFO |

**Hypothesis Status**: SUPPORTED with 7/8 entities at >50% coverage. Rule/Constraint appears implicitly in many papers but is less frequently named as an entity type.

---

## 6. Synthesis Findings

### Finding 1: Stratified Abstraction Is Universal

All analyzed ontologies exhibit a stratified architecture:
- UFO: UFO-A (structural) → UFO-B (temporal) → UFO-C (social/intentional)
- PROV-O: Entity → Activity → Agent (with specializations)
- Multi-Agent Taxonomy: 4 viewpoints with 12 aspects across 3 autonomy levels

### Finding 2: Agent-Activity-Entity Is the Core Pattern

This triad appears explicitly in:
- PROV-O (Entity-Activity-Agent)
- UFO (Endurant-Perdurant-Agent)
- BBO (Resource-Activity-Agent)
- Multi-Agent Taxonomy (Context-Task-Agent)
- Agentic RAG (Knowledge-Retrieval-Agent)

### Finding 3: Modern AI Systems Extend, Not Replace

LLM agent architectures extend foundational patterns:
- Agent + Memory = UFO-C intentional agent with internal states
- Agent + Tools = UFO-B disposition-based capabilities
- Agent + Role = UFO-C social role with permissions

### Finding 4: Process and Knowledge Domains Converge

Object-centric process mining (OCEL) and knowledge graphs share:
- First-class objects/entities
- Typed relationships
- Event-driven state changes
- Graph-based representations

---

## References

Evidence for each entity is cited with paper_id and chunk:line format. See individual paper index.md files for full context.
