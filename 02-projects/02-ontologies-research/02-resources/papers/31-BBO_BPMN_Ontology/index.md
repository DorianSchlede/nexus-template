---
paper_id: "31-BBO_BPMN_Ontology"
title: "BBO: BPMN 2.0 Based Ontology for Business Process Representation"
authors: ["Amina Annane", "Nathalie Aussenac-Gilles", "Mouna Kamel"]
year: 2019
chunks_expected: 1
chunks_read: 1
analysis_complete: true
high_priority_fields_found: 7

# HIGH PRIORITY FIELDS (1-5: Ontology focus)
entity_types:
  - "Process"
  - "Activity"
  - "Task"
  - "SubProcess"
  - "CallActivity"
  - "Agent"
  - "Event"
  - "Gateway"
  - "SequenceFlow"
  - "Resource"
  - "HumanResource"
  - "SoftwareResource"
  - "MaterialResource"
  - "WorkProduct"
  - "ManufacturingFacility"
  - "Station"
  - "Cell"
  - "Shop"
  - "Factory"
  - "Role"
  - "Job"
  - "InputOutputSpecification"
  - "Parameter"
  - "ParameterValue"

entity_definitions:
  Process: "A particular procedure for doing something involving one or more steps or operations. The process may produce a product, a property of a product, or an aspect of a product (ISO, 1998)"
  Activity: "The work to be performed. Has three sub-classes: Task (atomic), Sub-Process (complex with several Tasks), CallActivity (calls a reusable GlobalTask or Sub-Process)"
  Task: "An atomic task - the basic unit of work to be performed by operators"
  Agent: "The actor that performs a given process activity. May be HumanResource or SoftwareResource"
  Event: "Something that 'happens' during the course of a process. Events affect the flow of the process and usually have a cause or an impact and may require or allow for a reaction"
  Gateway: "Used to control how SequenceFlows interact as they converge or diverge within a Process"
  SequenceFlow: "Represents transitions that ensure the move from the source FlowNode to the target one. May depend on a condition (Expression)"
  Resource: "Englobes all resource types (broader than BPMN's agent-only definition)"
  WorkProduct: "Thing or substance produced by a natural or artificial process (ISO, 2005). A particular type of MaterialResource"
  ManufacturingFacility: "The place where process activities should be performed"
  Station: "Where a particular job is performed"
  Cell: "The place that groups a set of related operations in the production flow"
  Role: "Defines permissions and responsibilities. Differentiated from Job for flexibility"
  Job: "Organizational position with subordinated and superior relations"

entity_relationships:
  - from: "Process"
    to: "Activity"
    relationship: "decomposes_into"
    source: "Chunk 1:185-187"
  - from: "Activity"
    to: "Task"
    relationship: "specializes"
    source: "Chunk 1:229-231"
  - from: "Activity"
    to: "SubProcess"
    relationship: "specializes"
    source: "Chunk 1:231-232"
  - from: "Activity"
    to: "Resource"
    relationship: "has_resourceInput/has_resourceOutput"
    source: "Chunk 1:285-286"
  - from: "Agent"
    to: "Activity"
    relationship: "performs"
    source: "Chunk 1:351-353"
  - from: "Agent"
    to: "Role"
    relationship: "plays"
    source: "Chunk 1:352-353"
  - from: "SequenceFlow"
    to: "FlowNode"
    relationship: "has_sourceRef/has_targetRef"
    source: "Chunk 1:221-223"
  - from: "Gateway"
    to: "SequenceFlow"
    relationship: "has_incoming/has_outgoing"
    source: "Chunk 1:241"
  - from: "WorkProduct"
    to: "Resource"
    relationship: "is_composedOf"
    source: "Chunk 1:330-331"
  - from: "Task"
    to: "ManufacturingFacility"
    relationship: "takesPlaceAt"
    source: "Chunk 1:313-317"
  - from: "Agent"
    to: "HumanResource"
    relationship: "specializes"
    source: "Chunk 1:346"
  - from: "Agent"
    to: "SoftwareResource"
    relationship: "specializes"
    source: "Chunk 1:346"
  - from: "Job"
    to: "Job"
    relationship: "subordinated/superior"
    source: "Chunk 1:347"

abstraction_level: "domain"

framework_comparison:
  - compared_to: "BPMN 2.0"
    relationship: "extends"
    details: "BBO extracts and extends BPMN 2.0 process-execution fragment, adding resource taxonomies, manufacturing facilities, and enhanced agent modeling not supported by BPMN"
    source: "Chunk 1:89-92"
  - compared_to: "Enterprise Ontology (Uschold)"
    relationship: "related"
    details: "Both address business process representation, but Enterprise Ontology is more general"
    source: "Chunk 1:110-116"
  - compared_to: "SUPER project ontologies"
    relationship: "related"
    details: "Both emerged from BP representation research, BBO focuses on process execution"
    source: "Chunk 1:110-112"
  - compared_to: "Karray maintenance ontology"
    relationship: "reuses"
    details: "BBO resource taxonomy inspired by Karray's industrial maintenance process ontology"
    source: "Chunk 1:302-303"
  - compared_to: "Chungoora manufacturing ontology"
    relationship: "reuses"
    details: "ManufacturingFacility taxonomy reused from Chungoora's model-driven ontology"
    source: "Chunk 1:309-310"
  - compared_to: "EPC (Event Process Chain)"
    relationship: "superior"
    details: "BPMN offers finer grained representation than EPC and an execution logic for its elements"
    source: "Chunk 1:113-115"

# HIGH PRIORITY FIELDS (6-10: AI focus) - N/A for pre-2020 paper
ai_integration: "N/A - paper predates LLM/AI integration discussion (2019)"

agent_modeling:
  - aspect: "Agent Types"
    description: "Agents classified as HumanResource or SoftwareResource"
    source: "Chunk 1:346"
  - aspect: "Direct Assignment"
    description: "Specific Agent can be directly assigned to an Activity"
    source: "Chunk 1:352"
  - aspect: "Indirect Assignment"
    description: "Role can be assigned to Activity; all agents playing the role are potential performers"
    source: "Chunk 1:352-353"
  - aspect: "Job-Role Distinction"
    description: "Job and Role are differentiated - persons with same Job may have different authorization levels via Roles"
    source: "Chunk 1:350-351"
  - aspect: "Organizational Hierarchy"
    description: "Job concept with subordinated/superior relations represents company organizational model"
    source: "Chunk 1:347-348"
  - aspect: "Virtual Agent Support"
    description: "Ontology designed to be exploited by a virtual assistant to monitor process execution"
    source: "Chunk 1:140"

agentic_workflows: "N/A - paper predates multi-agent AI systems discussion"

generative_ai_patterns: "N/A - paper predates LLM/generative AI patterns"

agent_ontology_integration: "N/A - paper predates AI-ontology integration patterns"

# MEDIUM PRIORITY FIELDS
entity_count:
  count: 106
  non_inheritance_relations: 125
  inheritance_relations: 83
  rationale: "Designed for detailed business process representation covering process decomposition, resources, agents, facilities"
  source: "Chunk 1:471-473"

methodology: "top-down"

empirical_evidence:
  - type: "Industrial case study"
    description: "AVIREX project with Thales Alenia Space and Continental as industrial partners"
    source: "Chunk 1:73-78"
  - type: "Technical documents"
    description: "20 technical documents (10-30 pages each) describing industrial business processes"
    source: "Chunk 1:150-152"
  - type: "Competency questions"
    description: "22 competency questions collected from experts and literature"
    source: "Chunk 1:164-166"
  - type: "Schema metrics"
    description: "Evaluated using Tartir & Arpinar metrics: RD=0.60 (rich relationships), SD=0.78 (deep/detailed)"
    source: "Chunk 1:457-466"
  - type: "SPARQL validation"
    description: "Competency questions converted to SPARQL queries and validated against populated KB"
    source: "Chunk 1:485"

limitations:
  - "No trace of previous process runs - only models current execution (Chunk 1:577-578)"
  - "Requires manual instantiation from technical documents (Chunk 1:581-582)"
  - "BPMN graphical/collaboration elements excluded - focuses on process execution only (Chunk 1:218-219)"
  - "Open world assumption may not detect missing manufacturing facility assignments (Chunk 1:525-527)"

tools_standards:
  - "OWL 2 DL"
  - "BPMN 2.0"
  - "Protege"
  - "SPARQL"
  - "RDF/RDFS"
  - "METHONTOLOGY"
  - "UML (for conceptualization)"
  - "Camunda (for BPMN graphical representation)"
---

# BBO: BPMN 2.0 Based Ontology for Business Process Representation - Analysis Index

## Paper Overview

- **Source**: 31-BBO_BPMN_Ontology.pdf
- **Chunks**: 1 chunk, ~10,374 estimated tokens
- **Analyzed**: 2025-12-28T14:45:00
- **DOI**: https://doi.org/10.34190/KM.19.113
- **Venue**: 20th European Conference on Knowledge Management (ECKM 2019)

## Key Extractions

BBO (BPMN 2.0 Based Ontology) is a domain-level ontology for representing industrial business processes. It extends BPMN 2.0 by adding concepts not supported in the original meta-model, including resource taxonomies, manufacturing facilities, and enhanced agent/role modeling.

### Entity Types

| Entity | Type | Source |
|--------|------|--------|
| Process | Core concept - container for activities | Chunk 1:185-187 |
| Activity | Work to be performed (Task, SubProcess, CallActivity) | Chunk 1:229-234 |
| Agent | Actor performing activities (Human/Software) | Chunk 1:346 |
| Event | Something that happens during process | Chunk 1:236-239 |
| Gateway | Controls SequenceFlow convergence/divergence | Chunk 1:241 |
| Resource | All resource types (broader than BPMN) | Chunk 1:290-300 |
| WorkProduct | Thing produced by process | Chunk 1:326-328 |
| ManufacturingFacility | Where activities are performed | Chunk 1:309-317 |

### Entity Relationships

| From | Relationship | To | Source |
|------|--------------|-----|--------|
| Process | decomposes_into | Activity | Chunk 1:185-187 |
| Activity | has_resourceInput/Output | Resource | Chunk 1:285-286 |
| Agent | performs | Activity | Chunk 1:351-353 |
| Agent | plays | Role | Chunk 1:352-353 |
| SequenceFlow | has_sourceRef/targetRef | FlowNode | Chunk 1:221-223 |
| Task | takesPlaceAt | ManufacturingFacility | Chunk 1:313-317 |
| WorkProduct | is_composedOf | Resource | Chunk 1:330-331 |
| Job | subordinated/superior | Job | Chunk 1:347 |

### Framework Comparison

| Framework | Relationship | Details |
|-----------|-------------|---------|
| BPMN 2.0 | extends | Core of BBO; adds resources, facilities, agent modeling |
| EPC | superior | BPMN offers finer-grained representation with execution logic |
| Karray maintenance ontology | reuses | Resource taxonomy inspiration |
| Chungoora manufacturing ontology | reuses | ManufacturingFacility taxonomy |

### Key Findings (with evidence)

- **106 concepts with rich relationships** (Chunk 1:471-473): "Concepts: 106, Relationships others than isA: 125, isA relations: 83, RD = 0.60, SD = 0.78"
- **BPMN 2.0 extension rationale** (Chunk 1:83-88): "BPMN does not support the representation of some process specifications such as the material resources required to carry out a given task, or the workstation where a given task should be performed"
- **Agent-Role distinction** (Chunk 1:350-351): "we differentiated Job from Role to offer more flexibility. Indeed, two persons that have the same Job, may have different authorization levels"
- **Virtual assistant design** (Chunk 1:77-78): "the ontology forms a knowledge base (KB) that will be exploited by a virtual agent to support operators in the execution of BP step-by-step"

## Chunk Navigation

### Chunk 1: Complete Paper (Introduction through References)
- **Summary**: Single chunk containing the complete BBO paper. Presents the ontology developed using METHONTOLOGY to represent industrial business processes. Covers specification (competency questions, technical documents), conceptualization (5 main concepts: Process, Input/Output, Agent, WorkProduct, ManufacturingFacility), formalization (UML to OWL conversion, NL specifications to axioms), and evaluation (schema metrics, SPARQL queries, industrial case study).
- **Key concepts**: [BBO, BPMN 2.0, business process ontology, OWL 2 DL, resource taxonomy, agent-role modeling, manufacturing facility, METHONTOLOGY, Industry 4.0, competency questions]
- **Key quotes**:
  - Line 40-41: "Any industrial company has its own business processes, which is a number of related tasks that have to be executed to reach well-defined goals"
  - Line 60-62: "a process is a particular procedure for doing something involving one or more steps or operations"
  - Line 229: "Activity is the work to be performed"
  - Line 346-347: "An Agent may be a HumanResource or a SoftwareResource"
  - Line 471-473: "Concepts: 106, Relationships others than isA: 125, isA relations: 83"
- **Load when**: "Query about BPMN-based ontologies", "How to model business processes with OWL", "Resource modeling in process ontologies", "Agent-role relationships in BPM", "Manufacturing facility ontology", "BPMN 2.0 extensions", "Industry 4.0 semantic web"

## Relevance to Research Questions

### Agent-Activity-Entity Triad
BBO implements a clear Agent-Activity-Entity pattern:
- **Agent**: HumanResource or SoftwareResource that performs Activities
- **Activity**: Work to be performed (Task, SubProcess, CallActivity)
- **Entity**: Resources (input/output), WorkProducts, Events

### Entity Definitions
Provides formal definitions for 106 concepts with OWL axioms derived from both BPMN 2.0 UML diagrams and natural language specifications.

### Framework Comparison
Explicitly extends BPMN 2.0 and reuses fragments from multiple ontologies (Karray, Chungoora, Ruiz) while addressing BPMN's limitations for resource and facility representation.

### AI Agent Integration
While predating LLM systems, BBO explicitly targets virtual assistant support:
- "exploited by a virtual agent to support operators in the execution of BP step-by-step"
- "provide answers to operators' questions about the process execution"
- SPARQL queries demonstrate knowledge retrieval patterns

## 8-Entity Hypothesis Validation

| Hypothesis Entity | BBO Equivalent | Present | Notes |
|------------------|----------------|---------|-------|
| Goal | [Implicit in Process] | Partial | Process has "well-defined goals" but no explicit Goal class |
| Task | Task | Yes | Atomic unit of work |
| Rule | Expression, Condition | Partial | Conditions on SequenceFlow, no explicit Rule class |
| Resource | Resource (+ taxonomy) | Yes | Rich taxonomy: Material, Human, Software, Data |
| Role | Role | Yes | Distinct from Job for authorization flexibility |
| Data | DataResource | Yes | Subclass of Resource |
| Event | Event | Yes | Comprehensive event taxonomy from BPMN |
| Agent | Agent | Yes | HumanResource or SoftwareResource |

**Score**: 6.5/8 entities explicitly present (Goal and Rule are implicit/partial)
