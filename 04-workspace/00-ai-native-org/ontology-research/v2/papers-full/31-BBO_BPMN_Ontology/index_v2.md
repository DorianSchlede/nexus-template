---
paper_id: "31-BBO_BPMN_Ontology"
title: "BBO: BPMN 2.0 Based Ontology for Business Process Representation"
authors:
  - "Amina Annane"
  - "Nathalie Aussenac-Gilles"
  - "Mouna Kamel"
year: 2019
venue: "20th European Conference on Knowledge Management (ECKM 2019)"
schema_version: "2.0-discovery"
extraction_date: "2025-12-31"

# V2 DISCOVERY-ORIENTED EXTRACTION

ontological_primitives:
  - term: "FlowElement"
    definition: "Abstract class for all elements that can be part of a Process flow"
    source: "Chunk 1:220-221"
    unique_aspects: "BPMN-specific - not found in foundational ontologies. Unifies SequenceFlow and FlowNode under common parent"
  - term: "FlowNode"
    definition: "Class that groups the activities that compose a process - includes Activity, Event, Gateway"
    source: "Chunk 1:221-223"
    unique_aspects: "The actual 'things that happen' in a process, distinguished from the flows between them"
  - term: "SequenceFlow"
    definition: "Transitions that ensure the move from the source FlowNode to the target one"
    source: "Chunk 1:221-223"
    unique_aspects: "First-class representation of ordering - flows are entities, not mere predicates"
  - term: "Activity"
    definition: "The work to be performed"
    source: "Chunk 1:229"
    unique_aspects: "Abstract class with concrete subtypes (Task, SubProcess, CallActivity) - BPMN models activities as work units, not occurrences"
  - term: "Task"
    definition: "An atomic task - the work to be performed by operators"
    source: "Chunk 1:230-231, 154-155"
    unique_aspects: "ATOMIC - cannot be decomposed further. This is a strong ontological commitment about granularity"
  - term: "Event"
    definition: "Something that 'happens' during the course of a process"
    source: "Chunk 1:236-237"
    unique_aspects: "NOT a data entity but a control flow element. Events 'affect the flow' and 'have a cause or impact'"
  - term: "Resource"
    definition: "Englobes all resource types" (BBO interpretation vs ambiguous BPMN definition)
    source: "Chunk 1:290-301"
    unique_aspects: "BBO REDEFINES Resource broadly - BPMN limits it to agents. This is a deliberate ontological commitment"
  - term: "Expression"
    definition: "Represents a condition that a SequenceFlow may depend on"
    source: "Chunk 1:222-223"
    unique_aspects: "Rules/conditions are not first-class entities but Expression instances attached to flows"

structural_patterns:
  - pattern_name: "FlowElementsContainer Pattern"
    structure: "Container -[has_flowElements]-> FlowElement* (FlowNode | SequenceFlow)"
    instances:
      - "Process contains FlowElements"
      - "SubProcess contains FlowElements (recursive)"
    source: "Chunk 1:220-223"
    notes: "Recursive containment - SubProcess IS a FlowNode that CONTAINS FlowNodes"
  - pattern_name: "Source-Target Flow Triad"
    structure: "FlowNode -[has_outgoing]-> SequenceFlow -[has_targetRef]-> FlowNode"
    instances:
      - "StartEvent -> SequenceFlow -> Task"
      - "Task -> SequenceFlow -> Gateway"
      - "Gateway -> SequenceFlow -> EndEvent"
    source: "Chunk 1:221-223, 513-517"
    notes: "Flows are ENTITIES with source/target relationships - not simple edges. This allows conditions to be attached"
  - pattern_name: "Gateway Cardinality Pattern"
    structure: "GatewayType defined by cardinality restrictions on incoming/outgoing SequenceFlows"
    instances:
      - "ConvergingGateway: min 2 incoming, exactly 1 outgoing"
      - "DivergingGateway: exactly 1 incoming, min 2 outgoing"
      - "MixedGateway: min 2 incoming, min 2 outgoing"
    source: "Chunk 1:248-252, 440-444"
    notes: "SURPRISE: Gateway types are DEFINED by cardinality axioms, not by attributes. Ontological definition via structural constraint"
  - pattern_name: "InputOutputSpecification Mediator"
    structure: "Activity -[has_ioSpecification]-> InputOutputSpecification -[has_resourceInput/Output]-> Resource"
    instances:
      - "Task -> IO Spec -> Software, Data, Tool"
      - "Process -> IO Spec -> Resource set"
    source: "Chunk 1:282-289"
    notes: "INDIRECT resource binding via mediator object - allows multiple inputs/outputs per activity"
  - pattern_name: "Agent Role Indirection"
    structure: "Activity can be assigned Agent (direct) OR Role (indirect, resolves to multiple Agents)"
    instances:
      - "Task -> specific Agent (direct assignment)"
      - "Task -> Role -> Agent* (indirect assignment)"
    source: "Chunk 1:351-353"
    notes: "Two distinct assignment mechanisms with different semantics for flexibility"
  - pattern_name: "Hierarchical Facility Containment"
    structure: "Factory contains Shop contains Cell contains Station"
    instances:
      - "Factory -> Shop -> Cell -> Station"
    source: "Chunk 1:309-317"
    notes: "Linear containment hierarchy - no cross-cutting. Task limited to ONE ManufacturingFacility"

novel_concepts:
  - concept: "Gateway Type as Cardinality Restriction"
    definition: "Gateway types (Converging, Diverging, Mixed) defined via OWL cardinality restrictions on flow relationships"
    novelty_claim: "Natural language BPMN spec formalized as OWL axioms - enables automatic classification"
    source: "Chunk 1:246-252, 440-444"
  - concept: "Resource Semantic Disambiguation"
    definition: "BBO explicitly adopts the BROAD definition of Resource (all types) vs BPMN's ambiguous usage (sometimes limited to agents)"
    novelty_claim: "Resolves longstanding BPMN ambiguity documented in literature"
    source: "Chunk 1:290-301"
  - concept: "Job-Role Differentiation"
    definition: "Job (organizational position with subordination) vs Role (authorization level for activity execution)"
    novelty_claim: "Two persons with same Job may have different Roles - provides flexibility not in BPMN"
    source: "Chunk 1:350-351"
  - concept: "WorkProduct as MaterialResource subtype"
    definition: "Products ARE resources - once produced, can be input for another activity"
    novelty_claim: "Unifies product and resource under single taxonomy via ISO 10303-239 interpretation"
    source: "Chunk 1:326-331"
  - concept: "ManufacturingFacility Taxonomy"
    definition: "Station/Cell/Shop/Factory hierarchy - Task limited to ONE facility, Process may span multiple"
    novelty_claim: "Not supported by BPMN - fills identified gap for industrial process representation"
    source: "Chunk 1:309-317"
  - concept: "Competency Question-Driven Specification"
    definition: "22 competency questions from industrial experts and literature drive ontology scope"
    novelty_claim: "Explicit requirements traceability from questions to concepts"
    source: "Chunk 1:164-177"

semantic_commitments:
  - commitment: "Events as Control Flow vs Data Entities"
    position: "Events are FlowNodes that affect process execution, NOT standalone data entities to be stored"
    implications: "BPMN Events are more like 'triggers' than 'occurrences' - cannot query past events without extension"
    source: "Chunk 1:236-239"
  - commitment: "Task Atomicity"
    position: "Task is ATOMIC - cannot be decomposed further"
    implications: "Granularity locked at Task level. What constitutes 'atomic' is domain-dependent"
    source: "Chunk 1:230-231, 317"
  - commitment: "Open World Assumption (with noted issues)"
    position: "OWL reasoning uses Open World Assumption"
    implications: "Cardinality constraints don't enforce completeness - authors note this causes issues with ManufacturingFacility assignment"
    source: "Chunk 1:525-527"
  - commitment: "Execution Semantics from BPMN 2.0"
    position: "BPMN 2.0 'contains a full formalization of the execution semantics for all BPMN elements'"
    implications: "BBO inherits execution semantics, not just structural representation"
    source: "Chunk 1:125-126"
  - commitment: "Resource Realism"
    position: "Resources exist as entities with types (Material, Software, Human, Tool, Data)"
    implications: "Resources are first-class ontological entities, not just labels"
    source: "Chunk 1:299-303"
  - commitment: "Agent as HumanResource or SoftwareResource"
    position: "Agent is EITHER human OR software, nothing else"
    implications: "No collective agents, no organizational agents, no hybrid agents"
    source: "Chunk 1:346"

boundary_definitions:
  - entity_type: "Task vs SubProcess"
    identity_criteria: "Task is atomic; SubProcess contains multiple Tasks"
    boundary_cases: "At what granularity does something become a Task vs SubProcess? Domain-dependent"
    source: "Chunk 1:230-233"
  - entity_type: "Process vs SubProcess"
    identity_criteria: "Process is top-level FlowElementsContainer; SubProcess is both Activity AND Container"
    boundary_cases: "SubProcess has dual nature - is an Activity (can be in flow) AND a Container (has flow elements)"
    source: "Chunk 1:220-221, 231-232"
  - entity_type: "Direct vs Indirect Agent Assignment"
    identity_criteria: "Direct = specific Agent instance; Indirect = Role that multiple Agents can play"
    boundary_cases: "Same Agent can be assigned directly AND via Role - what takes precedence?"
    source: "Chunk 1:351-353"
  - entity_type: "Resource Type Boundaries"
    identity_criteria: "MaterialResource, SoftwareResource, HumanResource, Tool, DataResource as distinct types"
    boundary_cases: "What about a document (data) stored on a USB drive (material)? Classification unclear"
    source: "Chunk 1:299-303, Figure 6"
  - entity_type: "Event vs Activity"
    identity_criteria: "Event 'happens' and affects flow; Activity is 'work to be performed'"
    boundary_cases: "Is checking a condition an Event or an Activity? BPMN treats it as Event"
    source: "Chunk 1:236-239"

temporal_modeling:
  - aspect: "Process Flow Ordering"
    approach: "SequenceFlow entities connect FlowNodes - ordering is structural, not temporal"
    mechanism: "has_sourceRef and has_targetRef properties define order; conditions via conditionExpression"
    source: "Chunk 1:221-223"
  - aspect: "Event Occurrence"
    approach: "Events 'happen' but NO timestamp or duration primitives in BBO"
    mechanism: "BPMN Event types (Timer, Conditional) but no explicit time representation"
    source: "Chunk 1:236-239, 263"
  - aspect: "Iteration/Looping"
    approach: "Activity class related to LoopCharacteristics"
    mechanism: "Loop specification attached to Activity, not to flow structure"
    source: "Chunk 1:234"
  - aspect: "Process History"
    approach: "NOT SUPPORTED - identified as limitation"
    mechanism: "The current version of BBO proposes the classes required to model a process run but it keeps no trace of previous runs"
    source: "Chunk 1:577-578"
  - aspect: "TimerEvent"
    approach: "Event type with TimerEventDefinition"
    mechanism: "Exists but formalization of time values not detailed"
    source: "Chunk 1:263, 444"

agency_spectrum:
  - agent_type: "HumanResource"
    capabilities: "Performs tasks, has Job (organizational position), plays Roles"
    constraints: "Must be assigned to Activity (directly or via Role)"
    source: "Chunk 1:346-353"
  - agent_type: "SoftwareResource"
    capabilities: "Can be Agent that performs Activity"
    constraints: "Same assignment mechanism as HumanResource; no special automation semantics"
    source: "Chunk 1:346"
  - agent_type: "Virtual Assistant (system using BBO)"
    capabilities: "Supports operators in execution step-by-step, answers questions about processes"
    constraints: "Not modeled IN the ontology - it's the CONSUMER of the ontology"
    source: "Chunk 1:77-78, 140-141"
  - agent_type: "MISSING: Organizational Agent"
    capabilities: "N/A"
    constraints: "No concept of organization-as-agent, department-as-agent, team-as-agent"
    source: "Implicit - not discussed"
  - agent_type: "MISSING: Collective Agent"
    capabilities: "N/A"
    constraints: "No aggregation of agents into collective entities with unified agency"
    source: "Implicit - not discussed"

knowledge_representation:
  - mechanism: "OWL 2 DL"
    formalism: "Description Logic subset of OWL suitable for decidable reasoning"
    reasoning: "Classification, consistency checking via Hermit/Fact/Pellet reasoners"
    source: "Chunk 1:359, 426-428"
  - mechanism: "UML-to-OWL Transformation"
    formalism: "Systematic conversion rules from UML class diagrams"
    reasoning: "Cardinalities become qualified cardinality restrictions"
    source: "Chunk 1:368-386"
  - mechanism: "Natural Language to OWL Formalization"
    formalism: "Manual conversion of BPMN spec text to OWL axioms"
    reasoning: "Captures semantics lost in UML/XML representations of BPMN"
    source: "Chunk 1:395-403"
  - mechanism: "SPARQL Querying"
    formalism: "SPARQL queries for competency questions"
    reasoning: "Open world reasoning noted as issue for certain queries"
    source: "Chunk 1:485-486, 524-532"
  - mechanism: "Reuse of Existing Ontologies"
    formalism: "UO (Unit of Measure), taxonomies from Karray et al., Chungoora et al."
    reasoning: "Modular composition rather than monolithic development"
    source: "Chunk 1:288-289, 309-310, 340"

emergence_indicators:
  - phenomenon: "Process-level Properties"
    mechanism: "Process has properties (ManufacturingFacility, InputOutputSpecification) that don't reduce to Task properties"
    evidence: "A process may require several manufacturing facilities while a Task requires exactly one"
    source: "Chunk 1:316-317"
  - phenomenon: "Organizational Structure from Job Hierarchy"
    mechanism: "subordinated/superior relations on Job create organizational model"
    evidence: "'The concept Job with the two relations subordinated and superior represent the organizational model of the company'"
    source: "Chunk 1:346-348"
  - phenomenon: "Workflow Behavior from Component Composition"
    mechanism: "Gateway types control convergence/divergence of parallel flows"
    evidence: "ConvergingGateway combines multiple flows; DivergingGateway splits - emergent flow patterns"
    source: "Chunk 1:241-242, 248-252"

integration_surfaces:
  - surface: "BPMN 2.0 Meta-model"
    connects_to: ["BPMN 2.0 Specification", "Camunda BPMN tools"]
    alignment_quality: "High - BBO core extracted from BPMN 2.0, preserves execution semantics"
    source: "Chunk 1:45-47, 89-91"
  - surface: "Enterprise Ontology"
    connects_to: ["Uschold et al. 1998"]
    alignment_quality: "Partial - Enterprise Ontology is more general; BBO more detailed for BP"
    source: "Chunk 1:110-116"
  - surface: "UO (Unit of Measure Ontology)"
    connects_to: ["http://purl.obolibrary.org/obo/uo.owl"]
    alignment_quality: "Direct reuse - Unit and Prefix concepts imported"
    source: "Chunk 1:288-289"
  - surface: "Industrial Maintenance Ontology (Karray et al.)"
    connects_to: ["Resource taxonomy from Karray 2012"]
    alignment_quality: "Direct reuse - Resource hierarchy adopted"
    source: "Chunk 1:302-303"
  - surface: "Manufacturing Interoperability (Chungoora et al.)"
    connects_to: ["ManufacturingFacility taxonomy"]
    alignment_quality: "Direct reuse - Station/Cell/Shop/Factory hierarchy"
    source: "Chunk 1:309-310"
  - surface: "Software Process Ontology (Ruiz et al., Falbo et al.)"
    connects_to: ["Agent sub-ontology"]
    alignment_quality: "Direct reuse - Agent/Job/Role structure from Ruiz 2004"
    source: "Chunk 1:340-341, 302-303"
  - surface: "POTENTIAL: PROV-O"
    connects_to: ["PROV-O Agent/Activity/Entity triad"]
    alignment_quality: "Unmapped - BBO Agent/Activity similar to PROV-O but no explicit alignment"
    source: "Implicit - not discussed"

gaps_and_tensions:
  - gap_type: "Omission"
    description: "No Goal/Objective entity - processes have purposes but not modeled"
    implications: "Cannot reason about WHY a process exists or whether it achieved its goal"
    source: "Implicit - not discussed"
  - gap_type: "Omission"
    description: "No Rule/Constraint first-class entity - rules embedded in Expressions and Gateway logic"
    implications: "Cannot query 'what rules govern this process?' - rules hidden in flow structure"
    source: "Chunk 1:222-223, 246-252"
  - gap_type: "Omission"
    description: "No process history/trace - only current run modeled"
    implications: "Cannot do process mining on BBO data without extension. Authors note this as future work"
    source: "Chunk 1:577-578"
  - gap_type: "Tension"
    description: "OWL Open World Assumption vs Industrial Completeness Requirements"
    implications: "Cardinality constraints don't enforce data completeness; authors note workarounds needed"
    source: "Chunk 1:525-527"
  - gap_type: "Tension"
    description: "BPMN Resource ambiguity resolved by fiat"
    implications: "BBO's broad Resource definition may conflict with BPMN tools expecting narrow definition"
    source: "Chunk 1:290-301"
  - gap_type: "Tension"
    description: "Static model vs Dynamic execution"
    implications: "'It is not always simple to answer to this question, because of the dynamic aspect of BPs' - condition evaluation happens at runtime"
    source: "Chunk 1:529-530"
  - gap_type: "Underspecified"
    description: "Time/duration not formally represented"
    implications: "TimerEvent exists but no vocabulary for expressing time values"
    source: "Chunk 1:263"
  - gap_type: "Underspecified"
    description: "Task atomicity boundary"
    implications: "What granularity constitutes 'atomic'? Domain-dependent, not formalized"
    source: "Chunk 1:230-231"
  - gap_type: "Gap"
    description: "No collective/organizational agency"
    implications: "Cannot model 'the department performs...' or team-level agency"
    source: "Implicit - Agent = Human OR Software only"

empirical_grounding:
  - type: "Industrial Collaboration"
    domain: "Aerospace (Thales Alenia Space) and Automotive (Continental)"
    scale: "20 technical documents, 10-30 pages each"
    findings: "Documents describe BP stages, devices, resources - validated BBO scope requirements"
    source: "Chunk 1:150-155, 73-78"
  - type: "Competency Question Collection"
    domain: "Industrial operators and business analysts"
    scale: "22 competency questions collected"
    findings: "Questions from experts + literature drove specification of 5 main concepts"
    source: "Chunk 1:164-177, 183-195"
  - type: "Use Case Instantiation"
    domain: "Real industrial BP example with 3 tasks"
    scale: "Single process with 2 tasks, 1 subprocess, 6 sequence flows"
    findings: "BBO successfully instantiated; SPARQL queries return expected answers"
    source: "Chunk 1:480-532"
  - type: "Schema Metrics Evaluation"
    domain: "Ontology quality assessment"
    scale: "106 concepts, 125 non-isA relationships, 83 isA relationships"
    findings: "RD=0.60 (rich relationships), SD=0.78 (deep/vertical ontology)"
    source: "Chunk 1:457-473"
  - type: "Reasoner Validation"
    domain: "OWL consistency checking"
    scale: "Multiple BP models instantiated"
    findings: "Hermit, Fact, Pellet all confirm consistency after population"
    source: "Chunk 1:426-428"

---

# BBO: BPMN 2.0 Based Ontology for Business Process Representation (V2 Discovery Analysis)

## Summary

BBO is a domain ontology for industrial business process representation, built by extracting and extending BPMN 2.0. Developed for the AVIREX project with Thales Alenia Space and Continental, it targets virtual assistant support for process execution monitoring.

## Key Discoveries

### SURPRISE 1: Gateway Types Defined by Cardinality Axioms
The most interesting ontological move is defining Gateway subtypes (Converging, Diverging, Mixed) via OWL cardinality restrictions rather than attributes. A ConvergingGateway is DEFINED as having min 2 incoming and exactly 1 outgoing SequenceFlow. This enables automatic classification.

### SURPRISE 2: Resource Semantic Disambiguation as Explicit Commitment
BPMN's Resource definition is documented as "ambiguous" in the literature - sometimes meaning all resource types, sometimes only agents. BBO explicitly takes a position: Resource englobes all types. This is a deliberate ontological commitment that resolves documented ambiguity.

### SURPRISE 3: Events Are NOT Data Entities
In BBO/BPMN, Events are FlowNodes - control flow elements that "affect the flow" - not data entities that can be stored and queried. This contrasts sharply with event-centric ontologies like OCEL. You cannot ask "what events occurred last week?" without extending BBO.

### SURPRISE 4: Process History Explicitly Unsupported
The authors explicitly acknowledge "the current version of BBO proposes the classes required to model a process run but it keeps no trace of previous runs." This is a known gap, not an oversight.

### TENSION: Open World Assumption vs Industrial Requirements
The authors explicitly note that OWL's Open World Assumption causes problems: "Even if the minimum cardinality of the property linking Task and ManufacturingFacility is one, the KB is still consistent" even when no facility is specified. Industrial use cases need closed-world enforcement.

## Structural Patterns Found

1. **FlowElementsContainer Pattern**: Recursive containment where SubProcess is both Activity (in flow) and Container (has flow elements)
2. **Source-Target Flow Triad**: SequenceFlow as first-class entity mediating FlowNodes - allows conditions to attach
3. **Gateway Cardinality Pattern**: Types defined by structural constraints, not attributes
4. **IO Specification Mediator**: Indirect resource binding via mediator object
5. **Agent Role Indirection**: Two distinct assignment mechanisms (direct/indirect) with different semantics

## What's Missing (Gaps)

- **Goal/Objective**: No representation of process purpose or outcome evaluation
- **Rule/Constraint as first-class**: Rules hidden in Expressions and Gateway logic
- **Process History/Trace**: Cannot do process mining without extension
- **Collective Agency**: No organization-as-agent, team-as-agent concepts
- **Temporal Representation**: TimerEvent exists but time values not formalized

## Integration Opportunities

BBO maps well to PROV-O (Agent/Activity/Entity triad is structurally similar) but no explicit alignment exists. The authors reuse ontologies (UO, Karray, Chungoora) but don't discuss upper ontology grounding (no BFO, DOLCE, or UFO alignment).

## Quality Check

- [x] Used paper's OWN terminology (FlowElement, FlowNode, SequenceFlow, etc.)
- [x] Captured novel concepts (Gateway cardinality definition, Resource disambiguation)
- [x] Found gaps and tensions (OWA issues, missing history, no goals)
- [x] Noted surprises (Events as flow elements, not data)
- [x] All extractions have chunk:line references
- [x] Did NOT force-fit to predefined categories
- [x] Preserved nuance (BPMN ambiguity, atomic task domain-dependence)
