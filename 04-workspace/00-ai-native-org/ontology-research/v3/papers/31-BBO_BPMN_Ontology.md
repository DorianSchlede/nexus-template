---
paper_id: "31-BBO_BPMN_Ontology"
title: "BBO: BPMN 2.0 Based Ontology for Business Process Representation"
authors:
  - "Amina Annane"
  - "Nathalie Aussenac-Gilles"
  - "Mouna Kamel"
year: 2019
chunks_expected: 1
chunks_read: 1
analysis_complete: true
schema_version: "2.3"

chunk_index:
  1:
    token_count: 9979
    fields_found:
      entity_types: true
      entity_definitions: true
      entity_relationships: true
      entity_count: true
      abstraction_level: true
      framework_comparison: true
      methodology: true
      ai_integration: partial
      agent_modeling: true
      agentic_workflows: false
      generative_ai_patterns: false
      agent_ontology_integration: partial
      empirical_evidence: true
      limitations: partial
      tools_standards: true

entity_types:
  - item: "Process"
    chunk: 1
    lines: "185-187"
    quote: "Process: it is the key concept. The ontology should enable (i) to represent the decomposition of a given process in activities (sub-processes and tasks), and (ii) to well describe the order in which these activities should be performed"
  - item: "Activity"
    chunk: 1
    lines: "229-234"
    quote: "Activity is the work to be performed. Activity class has three sub-classes: Task (an atomic task), Sub-Process (complex task that contains several Tasks), CallActivity (an activity that calls a CallableElement)"
  - item: "Task"
    chunk: 1
    lines: "230-231"
    quote: "Task: an atomic task"
  - item: "Sub-Process"
    chunk: 1
    lines: "231-233"
    quote: "Sub-Process: complex task that contains several Tasks"
  - item: "CallActivity"
    chunk: 1
    lines: "232-233"
    quote: "CallActivity: an activity that calls a CallableElement that may be a GlobalTask (i.e., a reusable task) or Sub-Process"
  - item: "Event"
    chunk: 1
    lines: "236-239"
    quote: "Event is something that 'happens' during the course of a process. Events affect the flow of the process and usually have a cause or an impact and may require or allow for a reaction"
  - item: "Gateway"
    chunk: 1
    lines: "241-242"
    quote: "Gateway is used to control how SequenceFlows interact as they converge or diverge within a Process"
  - item: "FlowNode"
    chunk: 1
    lines: "221-223"
    quote: "FlowNode class groups the activities that compose a process"
  - item: "SequenceFlow"
    chunk: 1
    lines: "221-223"
    quote: "SequenceFlow represents transitions that ensure the move from the source FlowNode to the target one. A SequenceFlow may depend on a given condition"
  - item: "Agent"
    chunk: 1
    lines: "191-192"
    quote: "Agent: the actor that performs a given process activity. Indeed, it is important to specify who is responsible for the accomplishment of a given activity"
  - item: "Resource"
    chunk: 1
    lines: "290-294"
    quote: "The Resource concept exists in the BPMN meta-model. However, its semantics and definition are ambiguous... we adopt the first definition of Resource, that englobes all resource types"
  - item: "WorkProduct"
    chunk: 1
    lines: "326-331"
    quote: "In (ISO, 2005), the term Product is defined as follows 'Thing or substance produced by a natural or artificial process.' We adopt this definition for the WorkProduct concept"
  - item: "ManufacturingFacility"
    chunk: 1
    lines: "309-317"
    quote: "A workstation, Station, is where a particular job is performed. Cell is the place that groups a set of related operations in the production flow, while Shop is the area where production is carried out, and Factory is the place where those production areas are located"
  - item: "InputOutputSpecification"
    chunk: 1
    lines: "282-289"
    quote: "an activity may have at most one InputOutputSpecification that is related to the required Input/Output Data... we have added the two relations 'has_resourceInput' and 'has_resourceOutput'"
  - item: "Job"
    chunk: 1
    lines: "350-351"
    quote: "we differentiated Job from Role to offer more flexibility. Indeed, two persons that have the same Job, may have different authorization levels to execute Activities"
  - item: "Role"
    chunk: 1
    lines: "350-353"
    quote: "For a given Activity, we may assign a specific Agent (i.e., direct assignment), or a Role (i.e., indirect assignment). In the case of indirect assignment, all agents playing the assigned role are potential performers of the Activity"
---

# BBO: BPMN 2.0 Based Ontology for Business Process Representation

## Summary

This paper presents BBO (BPMN 2.0 Based Ontology), a domain ontology for business process representation developed for the AVIREX project. BBO extends the BPMN 2.0 meta-model with additional concepts to support fine-grained industrial process representation, including resources, manufacturing facilities, agents, and work products.

## Extracted Data

### entity_definitions

| Entity | Definition | Source |
|--------|------------|--------|
| Process | The key concept representing the decomposition of activities (sub-processes and tasks) and the order in which these activities should be performed, controlled by events and conditions | Chunk 1:185-187 |
| Activity | The work to be performed, with three sub-classes: Task (atomic task), Sub-Process (complex task with several Tasks), and CallActivity (calls a CallableElement) | Chunk 1:229-234 |
| Task | An atomic task - the work to be performed by operators | Chunk 1:154-155, 230-231 |
| SubProcess | Complex task that contains several Tasks | Chunk 1:231-232 |
| Event | Something that 'happens' during the course of a process, affecting the flow and usually having a cause or impact that may require or allow for a reaction | Chunk 1:236-239 |
| Gateway | Used to control how SequenceFlows interact as they converge or diverge within a Process; includes ConvergingGateway, DivergingGateway, MixedGateway, UnspecifiedGateway | Chunk 1:241-242, 246-252 |
| SequenceFlow | Transitions that ensure the move from the source FlowNode to the target one, may depend on a given condition represented as an Expression | Chunk 1:221-223 |
| Agent | The actor that performs a given process activity; may be a HumanResource or a SoftwareResource | Chunk 1:191-192, 346 |
| Resource | Englobes all resource types including MaterialResource, SoftwareResource, HumanResource | Chunk 1:290-301 |
| WorkProduct | Thing or substance produced by a natural or artificial process; considered as a particular type of MaterialResource | Chunk 1:326-331 |
| ManufacturingFacility | The place where process activities should be performed; includes Station, Cell, Shop, Factory | Chunk 1:309-317 |
| InputOutputSpecification | Specifies the required Input/Output Data and resources for an activity; related to has_resourceInput and has_resourceOutput | Chunk 1:282-289 |
| Role | Enables indirect assignment of agents to activities; all agents playing the assigned role are potential performers | Chunk 1:350-353 |
| Job | Organizational position differentiated from Role for flexibility; two persons with same Job may have different authorization levels | Chunk 1:346-351 |

### entity_relationships

| Relationship | Source | Target | Source Location |
|--------------|--------|--------|-----------------|
| has_flowElements | Process | FlowNode | Chunk 1:220-223 |
| has_ioSpecification | Activity | InputOutputSpecification | Chunk 1:282-284 |
| has_resourceInput | InputOutputSpecification | Resource | Chunk 1:285-286 |
| has_resourceOutput | InputOutputSpecification | Resource | Chunk 1:285-286 |
| has_sourceRef | SequenceFlow | FlowNode | Chunk 1:221-222 |
| has_targetRef | SequenceFlow | FlowNode | Chunk 1:221-222 |
| has_conditionExpression | SequenceFlow | Expression | Chunk 1:222-223 |
| takesPlaceAt | Activity | ManufacturingFacility | Chunk 1:309-313 |
| is_composedOf | WorkProduct | Resource | Chunk 1:330-331 |
| subordinated | Job | Job | Chunk 1:346-348 |
| superior | Job | Job | Chunk 1:346-348 |
| has_incoming | Gateway | SequenceFlow | Chunk 1:248-249 |
| has_outgoing | Gateway | SequenceFlow | Chunk 1:248-249 |

### entity_count

- **Count**: 106 concepts
- **Source**: Chunk 1:471-473
- **Quote**: "Concepts: 106, Relationships others than isA: 125, isA relations: 83"
- **Rationale**: Domain ontology for fine-grained business process representation; high entity count reflects need to capture process decomposition, resources, agents, facilities, and their relationships

### abstraction_level

**Level**: Domain ontology for business process representation

**Details**: Bridges foundational level (BPMN 2.0 meta-model) with application level (industrial manufacturing). Purpose: Enable fine-grained representation of industrial business processes, support virtual assistant for process execution monitoring, answer competency questions about processes.

**Source**: Chunk 1:45-50, 72-78

### framework_comparison

| Framework | Relationship | Details | Source |
|-----------|--------------|---------|--------|
| BPMN 2.0 | extends | BBO core is extracted from BPMN 2.0, extended with resource taxonomies, manufacturing facilities, work products, and agent modeling not supported by BPMN | Chunk 1:45-47, 81-88 |
| EPC (Event Process driven Chain) | more expressive | BPMN offers finer grained representation than EPC and an execution logic for its elements | Chunk 1:113-115 |
| Enterprise Ontology | more specific | Enterprise ontology is very general; BBO provides detailed BP representation | Chunk 1:110-116 |
| SUPER (Semantics Utilised for Process management) | comparison | Representing BPs was the focus of several research projects such as Enterprise and SUPER | Chunk 1:110-112 |
| Rospocher BPMN 1.0 Ontology | improves upon | Previous work transformed BPMN 1.0; BBO uses the richer BPMN 2.0 with full formalization of execution semantics | Chunk 1:122-126 |
| UO (Unit of Measure Ontology) | reuses | The UnitOfMeasure class is specified using the two concepts Unit and Prefix of the unit measures ontology UO | Chunk 1:288-289 |

### methodology

**Approach**: Top-down methodology following METHONTOLOGY (Fernandez et al., 1997)

**Stages**:
1. Specification - why ontology is built, intended uses, end-users
2. Conceptualization - structuring domain knowledge in conceptual model using UML
3. Formalization - transforms conceptual model into formal OWL model
4. Implementation - builds computable models
5. Maintenance - updates and corrections

**Source**: Chunk 1:95-104

### ai_integration

| Pattern | Description | Source |
|---------|-------------|--------|
| Virtual assistant for process execution | Once populated with BP data, the ontology forms a knowledge base (KB) that will be exploited by a virtual agent to support operators in the execution of BP step-by-step | Chunk 1:77-78, 140-141 |
| Knowledge base for question answering | Our ontology will be exploited only by a virtual assistant to monitor process execution step by step, and to answer questions about processes | Chunk 1:140-141 |
| SPARQL-based reasoning | We design SPARQL queries corresponding to the competency questions and check their results | Chunk 1:485-486, 524-532 |

**Note**: Paper predates LLM/GenAI integration patterns (2019). AI integration limited to rule-based virtual assistants and SPARQL querying.

### agent_modeling

| Aspect | Description | Source |
|--------|-------------|--------|
| Agent types | Agent may be HumanResource or SoftwareResource, distinguishing human operators from automated software agents | Chunk 1:346 |
| Direct vs indirect assignment | For a given Activity, we may assign a specific Agent (i.e., direct assignment), or a Role (i.e., indirect assignment). In the case of indirect assignment, all agents playing the assigned role are potential performers of the Activity | Chunk 1:351-353 |
| Organizational hierarchy | The concept Job with the two relations 'subordinated' and 'superior' represent the organizational model of the company, which is not supported by BPMN meta-model | Chunk 1:346-350 |

### agentic_workflows

N/A - Paper focuses on business process representation, not multi-agent system orchestration patterns.

### generative_ai_patterns

N/A - Paper predates LLM/generative AI discussion (2019).

### agent_ontology_integration

| Pattern | Description | Source |
|---------|-------------|--------|
| Ontology-based process monitoring | The ontology forms a knowledge base (KB) that will be exploited by a virtual agent to support operators in the execution of BP step-by-step | Chunk 1:77-78 |
| Competency question answering via SPARQL | We design SPARQL queries corresponding to the competency questions and check their results | Chunk 1:485-486 |

### empirical_evidence

| Type | Description | Source |
|------|-------------|--------|
| Industrial use case validation | Collaboration with two industrial companies (Thales Alenia Space, Continental) providing 20 technical documents describing business processes | Chunk 1:150-155, 480-488 |
| Real business process instantiation | Figure 8 shows the graphical representation of the example with BPMN graphical elements. We populated BBO with assertions representing the above process | Chunk 1:494-502 |
| Schema metrics evaluation | Relationship diversity (RD=0.60) and schema deepness (SD=0.78) indicate rich, deep ontology | Chunk 1:457-466 |

### limitations

| Limitation | Source |
|------------|--------|
| No trace of previous process runs - The current version of BBO proposes the classes required to model a process run but it keeps no trace of previous runs | Chunk 1:577-578 |
| Dynamic aspects require runtime evaluation - It is not always simple to answer to this question, because of the dynamic aspect of BPs | Chunk 1:529-530 |
| Open world assumption issues - Even if the minimum cardinality of the property linking Task and ManufacturingFacility is one, the KB is still consistent because of the open world reasoning assumption | Chunk 1:525-527 |

### tools_standards

| Tool/Standard | Description | Source |
|---------------|-------------|--------|
| OWL 2 DL | Formalization and implementation language | Chunk 1:359 |
| Protege | Development environment | Chunk 1:359 |
| BPMN 2.0 | Source meta-model for BBO core | Chunk 1:45-47 |
| SPARQL | Query language for competency questions | Chunk 1:485, 556-561 |
| Camunda | Open source BPMN modeling software | Chunk 1:482-483 |
| Hermit/Fact/Pellet | OWL reasoners for consistency checking | Chunk 1:426-428 |
| UML | Conceptualization diagrams | Chunk 1:204-206 |

---

## Key Insights for Research Questions

### Relevance to 8-Entity Hypothesis

BBO provides strong evidence for several entities in the hypothesis:

| UDWO Entity | BBO Mapping | Evidence |
|-------------|-------------|----------|
| **Task** | Task, Activity, SubProcess | Core concepts with clear hierarchy (Chunk 1:229-233) |
| **Agent** | Agent, HumanResource, SoftwareResource | Explicit modeling with role-based assignment (Chunk 1:340-353) |
| **Role** | Role, Job | Differentiated for flexibility (Chunk 1:350-351) |
| **Resource** | Resource taxonomy (Material, Software, Data, Tool) | Rich taxonomy extending BPMN (Chunk 1:299-303) |
| **Data** | DataResource, InputOutputSpecification | Part of resource taxonomy (Chunk 1:282-289) |
| **Event** | Event hierarchy (Start, End, Timer, Conditional) | BPMN event semantics preserved (Chunk 1:236-239) |
| **Goal** | *Implicit* - process outcomes, work products | Not explicitly modeled as entity type |
| **Rule** | Expression, ConditionalExpression, Gateway logic | Embedded in flow control, not first-class entity |

### Agent-Activity-Entity Triad Validation

BBO demonstrates the triad pattern:
- **Agent** performs **Activity** (Task/SubProcess)
- **Activity** uses/produces **Entity** (Resource types)
- Clear separation of who (Agent), what (Activity), and with-what (Resource)

### Entity Count Analysis

- **106 concepts** places BBO in the detailed domain ontology range
- Aligns with briefing's framework comparison (BBO: 106 vs ArchiMate: 57, TOGAF: 33)
- High entity count reflects fine-grained industrial process requirements

### Gaps for UDWO

1. **Goal** not explicitly represented as entity class
2. **Rule** embedded in expressions/gateways rather than first-class concept
3. No explicit **Event** as entity (BPMN Events are control flow elements, not data entities)
