---
batch_id: 4
field: entity_types
papers_read: [20-Agentic_RAG_Survey, 21-LLM_Smart_Contracts_from_BPMN, 22-RPA_Framework_BPM_Activities, 23-UFO_Story_Ontological_Foundations, 31-BBO_BPMN_Ontology]
chunks_read: 5
patterns_found: 28
extracted_at: "2025-12-28T12:00:00Z"
---

# Batch Extraction: entity_types (Batch 4)

## Patterns Extracted

### Pattern: AI Agent Components

- **Source**: 20-Agentic_RAG_Survey (Chunk 1:484-501)
- **Description**: Core components of an AI agent in Agentic RAG systems, defining the essential entity types that comprise autonomous agents including their reasoning engine, memory systems, planning capabilities, and tool access.
- **Quote**: "In essence, an AI agent comprises (Figure. 7): LLM (with defined Role and Task): Serves as the agent's primary reasoning engine and dialogue interface. It interprets user queries, generates responses, and maintains coherence. Memory (Short-Term and Long-Term): Captures context and relevant data across interactions. Short-term memory tracks immediate conversation state, while long-term memory stores accumulated knowledge and agent experiences. Planning (Reflection & Self-Critique): Guides the agent's iterative reasoning process through reflection, query routing, or self-critique, ensuring that complex tasks are broken down effectively. Tools Vector Search, Web Search, APIs, etc.): Expands the agent's capabilities beyond text generation, enabling access to external resources, real-time data, or specialized computations."
- **Context**: Presented as part of the core principles of agentic intelligence in Agentic RAG systems, distinguishing agents from simpler LLM applications.

---

### Pattern: RAG Core Components

- **Source**: 20-Agentic_RAG_Survey (Chunk 1:155-169)
- **Description**: The three primary entity types that constitute RAG system architecture: Retrieval, Augmentation, and Generation components.
- **Quote**: "The architecture of RAG systems integrates three primary components (Figure2): Retrieveal: Responsible for querying external data sources such as knowledge bases, APIs, or vector databases. Advanced retrievers leverage dense vector search and transformer-based models to improve retrieval precision and semantic relevance. Augmentation: Processes retrieved data, extracting and summarizing the most relevant information to align with the query context. Generation: Combines retrieved information with the LLM's pre-trained knowledge to generate coherent, contextually appropriate responses."
- **Context**: Foundation of understanding RAG system architecture and how entities interact within retrieval-augmented generation pipelines.

---

### Pattern: Single-Agent Architecture Entities

- **Source**: 20-Agentic_RAG_Survey (Chunk 1:755-798)
- **Description**: Entity types in single-agent RAG architecture including coordinating agent, knowledge sources (structured databases, semantic search, web search, recommendation systems), and LLM synthesis component.
- **Quote**: "A Single-Agent Agentic RAG: serves as a centralized decision-making system where a single agent manages the retrieval, routing, and integration of information... Knowledge Source Selection: Based on the query's type, the coordinating agent chooses from a variety of retrieval options: Structured Databases: For queries requiring tabular data access, the system may use a Text-to-SQL engine... Semantic Search: When dealing with unstructured information, it retrieves relevant documents... Web Search: For real-time or broad contextual information... Recommendation Systems: For personalized or contextual queries..."
- **Context**: Taxonomy section describing single-agent architecture patterns and the entity types involved in query processing workflows.

---

### Pattern: Multi-Agent System Entities

- **Source**: 20-Agentic_RAG_Survey (Chunk 1:874-917)
- **Description**: Entity types in multi-agent RAG systems including coordinator agent, specialized retrieval agents, and their distinct roles for different data source types.
- **Quote**: "Multi-Agent RAG represents a modular and scalable evolution of single-agent architectures... Specialized Retrieval Agents: The query is distributed among multiple retrieval agents, each focusing on a specific type of data source or task. Examples include: Agent 1: Handles structured queries, such as interacting with SQL-based databases like PostgreSQL or MySQL. Agent 2: Manages semantic searches for retrieving unstructured data from sources like PDFs, books, or internal records. Agent 3: Focuses on retrieving real-time public information from web searches or APIs. Agent 4: Specializes in recommendation systems, delivering context-aware suggestions based on user behavior or profiles."
- **Context**: Multi-agent taxonomy within Agentic RAG systems, showing specialization of agent types for different retrieval functions.

---

### Pattern: BPMN Core Flow Entities

- **Source**: 21-LLM_Smart_Contracts_from_BPMN (Chunk 1:136-139)
- **Description**: BPMN entity types referenced for business process modeling that LLMs need to understand for smart contract generation.
- **Quote**: "Due to their generality and the training input, LLMs can perform complex tasks beyond language understanding and generation, including analyzing and creating business process models and smart contracts."
- **Context**: Discussion of LLM capabilities for processing BPMN models and generating executable smart contracts.

---

### Pattern: BPMN Process Elements

- **Source**: 21-LLM_Smart_Contracts_from_BPMN (Chunk 1:247-251)
- **Description**: Core BPMN entity types used in process model evaluation including events, tasks, and gateways.
- **Quote**: "For the remainder of the paper, we use common terminology. We loosely denote an event log as a set of events, where each event is associated with a case identifier that groups it into a case. A trace is the ordered sequence of events (activities) that occurred for a specific case. Each event represents a task (activity) in the model. A trace can be said to be in conformance with a process model if it represents a valid execution path through that model."
- **Context**: Background section establishing terminology for BPMN elements used in the benchmarking framework.

---

### Pattern: Choreography Model Elements

- **Source**: 21-LLM_Smart_Contracts_from_BPMN (Chunk 1:414-421)
- **Description**: BPMN 2.0 Choreography entity types including tasks, events, and gateways supported by the evaluation framework.
- **Quote**: "Chorpiler supports all basic elements of BPMN Choreographies Choreography tasks, start and end event, exclusive, event, and parallel gateways, sub choreographies, and loops in the model."
- **Context**: Description of the Chorpiler tool and the BPMN choreography elements it can process for smart contract generation.

---

### Pattern: RPA Process Activity Characteristics

- **Source**: 22-RPA_Framework_BPM_Activities (Chunk 1:59-68)
- **Description**: Entity types related to process activity characteristics for RPA viability assessment including process activities, process steps, and evaluation criteria.
- **Quote**: "The objective of this work is to offer practitioners a process characteristic evaluation framework including a set of criteria and exemplary evaluation metrics. To understand the parameters of RPA, the following research question needs to be answered: What are the characteristics of a process activity, or a set of process activities, that facilitate viable robotic process automation?"
- **Context**: Introduction establishing the focus on process activities as core entity types for RPA automation assessment.

---

### Pattern: PCEF Perspectives and Criteria

- **Source**: 22-RPA_Framework_BPM_Activities (Chunk 1:235-236, 248-319)
- **Description**: The Process Characteristics Evaluation Framework defines five perspective entity types (Task, Time, Data, System, Human) with associated criteria entities.
- **Quote**: "We present five perspectives - task, time, data, system, and human - that contain several characteristics that analysts can use to evaluate a process accordingly... Perspective Criteria: Task (Standardization, Maturity, Determinism, Failure rate), Time (Frequency, Duration, Urgency), Data (Structuredness), System (Interfaces, Stability, Number of systems), Human (Resources, Proneness to human error)"
- **Context**: Framework presentation showing structured categorization of entity types for RPA process evaluation.

---

### Pattern: Event Log Entity Structure

- **Source**: 22-RPA_Framework_BPM_Activities (Chunk 1:461-490)
- **Description**: Entity types within event logs used for process mining evaluation including Case ID, Activity, Resource, Timestamp, Variant, and various contextual attributes.
- **Quote**: "Attribute Value: Case ID 2000000000 00001, Activity Record Goods Receipt, Resource user 000, Complete Timestamp 2018/03/06 07:44:00.000, Variant Variant 65, Variant index 65, (case) Company companyID 0000, (case) Document Type EC Purchase order..."
- **Context**: Example showing the structure of event log entities used in the process characteristic evaluation framework.

---

### Pattern: UFO Four-Category Ontology

- **Source**: 23-UFO_Story_Ontological_Foundations (Chunk 1:126-136)
- **Description**: UFO's foundational entity type structure based on Four-Category Ontology distinguishing individuals/universals and substantials/accidents.
- **Quote**: "It was clear to us from the outset that we needed an ontological theory that would countenance both individuals and universals and one that would include not only substantial individuals and universals but also accidents (particularized properties, moments, qualities, modes, tropes, abstract particulars, aspects, ways) and accident universals. In other words, we needed a Four-Category Ontology (Lowe, 2006)."
- **Context**: Historical background explaining the philosophical foundation for UFO's entity type categories.

---

### Pattern: UFO-A Endurant Categories

- **Source**: 23-UFO_Story_Ontological_Foundations (Chunk 1:173-181)
- **Description**: UFO-A ontology entity types for structural conceptual modeling including Types, Taxonomic Structures, Part-Whole Relations, Particularized Properties, Attributes, Relations, and Roles.
- **Quote**: "UFO-A: An Ontology of Endurants dealing with aspects of structural conceptual modeling. It is organized as a Four-Category ontology comprising theories of Types and Taxonomic Structures connected to a theory of object identifiers, Part-Whole Relations, Particularized Intrinsic Properties, Attributes and Attribute Value Spaces (including a theory of Datatypes as Measure Structures), Particularized Relational Properties and Relations and Roles"
- **Context**: Description of UFO-A stratum explaining its core entity types for endurant modeling.

---

### Pattern: UFO-B Perdurant Categories

- **Source**: 23-UFO_Story_Ontological_Foundations (Chunk 1:183-185)
- **Description**: UFO-B ontology entity types for events and processes including Perdurant Mereology, Temporal Ordering, Object Participation, Causation, Change, and Dispositions.
- **Quote**: "UFO-B: An Ontology of Perdurants (Events, Processes) dealing with aspects such as Perdurant Mereology, Temporal Ordering of Perdurants, Object Participation in Perdurants, Causation, Change and the connection between Perdurans and Endurants via Dispositions"
- **Context**: Description of UFO-B stratum explaining entity types for temporal and event modeling.

---

### Pattern: UFO-C Intentional and Social Entities

- **Source**: 23-UFO_Story_Ontological_Foundations (Chunk 1:191-193)
- **Description**: UFO-C ontology entity types for intentional and social aspects including Beliefs, Desires, Intentions, Goals, Actions, Commitments, Claims, Social Roles, and Social Relators.
- **Quote**: "UFO-C: An Ontology of Intentional and Social Entities, which is constructed on top of UFO-A and UFO-B, and which addresses notions such as Beliefs, Desires, Intentions, Goals, Actions, Commitments and Claims, Social Roles and Social Particularized Relational Complexes (Social Relators), among others"
- **Context**: Description of UFO-C stratum built on UFO-A and UFO-B for social and intentional entity modeling.

---

### Pattern: OntoUML Universal Types

- **Source**: 23-UFO_Story_Ontological_Foundations (Chunk 1:366-368)
- **Description**: Types of universals in OntoUML including substance sortals (kinds), phased-sortals (roles and phases), and non-sortals (categories, mixins, role mixins).
- **Quote**: "As previously mentioned, in the original version of UFO (and, hence, also in OntoUML), we had a number of ontological distinctions representing different sorts of universals. These include distinctions between substance sortals (kinds), phased-sortals (roles and phases) and non-sortals (categories, mixins and role mixins)."
- **Context**: Discussion of systematic language subversions leading to evolution of UFO and OntoUML entity type distinctions.

---

### Pattern: Entity Types and Relationship Types

- **Source**: 23-UFO_Story_Ontological_Foundations (Chunk 1:149-152)
- **Description**: The two fundamental constructs in conceptual modeling that UFO addresses: Entity Types and Relationship Types (hence Entity-Relationship approach).
- **Quote**: "In particular, ontological foundations for conceptual modeling would demand micro-theories to address conceptual modeling's most fundamental constructs, namely, Entity Types and Relationship Types (hence, the name of the so-called Entity-Relationship approach that gives the name to the most important conference in conceptual modeling!)."
- **Context**: Discussion of why UFO needed specific micro-theories beyond existing foundational ontologies.

---

### Pattern: Particularized Properties (Moments/Tropes)

- **Source**: 23-UFO_Story_Ontological_Foundations (Chunk 1:128-136)
- **Description**: UFO entity type for particularized properties including modes, qualities, relational properties, and their importance in conceptual modeling.
- **Quote**: "We needed particularized properties not only because they were of great importance in making sense of language and cognition but because they would repeatedly appear in the discourse of conceptual modelers. As previously mentioned, particularized relations (relationships) and particularized intrinsic properties (e.g., often represented by the so-called weak entities) are frequently modeled as bearers of other particularized properties in the practice of conceptual modeling."
- **Context**: Explanation of why particularized properties were essential additions beyond Bunge-Wand-Weber ontology.

---

### Pattern: BBO Process Entity Types

- **Source**: 31-BBO_BPMN_Ontology (Chunk 1:220-243)
- **Description**: Core BPMN 2.0 entity types reused in BBO ontology including Process, FlowElementsContainer, FlowElements, SequenceFlow, FlowNode, Activity, Task, Sub-Process, CallActivity, Event, and Gateway.
- **Quote**: "Process is a sub-class of FlowElementsContainer. Describing a process consists in defining the FlowElements that compose it. FlowElements class has two sub-classes: SequenceFlow and FlowNode. SequenceFlow represents transitions that ensure the move from the source FlowNode to the target one... FlowNode class groups the activities that compose a process: Activity is the work to be performed. Activity class has three sub-classes: Task: an atomic task, Sub-Process: complex task that contains several Tasks, CallActivity: an activity that calls a CallableElement..."
- **Context**: Conceptualization section of BBO describing BPMN-based process entity hierarchy.

---

### Pattern: BBO Activity Subtypes

- **Source**: 31-BBO_BPMN_Ontology (Chunk 1:229-234)
- **Description**: Activity entity subtypes in BBO including Task (atomic task), Sub-Process (complex task containing several Tasks), and CallActivity (calls a CallableElement).
- **Quote**: "Activity is the work to be performed. Activity class has three sub-classes: a. Task: an atomic task b. Sub-Process: complex task that contains several Tasks c. CallActivity: an activity that calls a CallableElement that may be a GlobalTask (i.e., a reusable task) or Sub-Process."
- **Context**: BBO conceptualization explaining activity type hierarchy from BPMN.

---

### Pattern: BBO Event Entity Type

- **Source**: 31-BBO_BPMN_Ontology (Chunk 1:236-239)
- **Description**: Event entity type in BBO representing occurrences during process execution that affect flow and require reactions.
- **Quote**: "Event is something that 'happens' during the course of a process. Events affect the flow of the process and usually have a cause or an impact and may require or allow for a reaction. In BPMN, events may be interrupting (i.e, when the events occurs, the activity related to this event is stopped) or not. Moreover, several types of event exist: TimerEvent, ConditionalEvent, etc."
- **Context**: BBO conceptualization describing event types from BPMN specification.

---

### Pattern: BBO Gateway Entity Type

- **Source**: 31-BBO_BPMN_Ontology (Chunk 1:241)
- **Description**: Gateway entity type in BBO used to control SequenceFlow convergence and divergence within processes.
- **Quote**: "Gateway is used to control how SequenceFlows interact as they converge or diverge within a Process."
- **Context**: BBO conceptualization of gateway entity type from BPMN.

---

### Pattern: BBO Extended Entity Types from BPMN Text

- **Source**: 31-BBO_BPMN_Ontology (Chunk 1:255-265)
- **Description**: Additional entity subtypes extracted from BPMN natural language specification including gateway types, sequence flow types, event types, and expression types.
- **Quote**: "Concept Sub-concepts: SequenceFlow (ConditionalSequenceFlow, DefaultSequenceFlow, NormalSequenceFlow), SubProcess (EventBasedSubProcess), Gateway (ConvergingGateway, DivergingGateway, MixedGateway, UnspecifiedGateway), EventBasedGateway (ExclusiveEventBasedGateway, parallelEventBasedGateway), Event (cancelEvent, conditionalEvent, ErrorEvent, MultipleEvent, NoneEvent, TimerEvent, etc.), Expression (UnderspecifiedExpression)"
- **Context**: Table showing additional classes BBO extracted from textual BPMN specifications.

---

### Pattern: BBO Five Main Concept Categories

- **Source**: 31-BBO_BPMN_Ontology (Chunk 1:183-196)
- **Description**: The five main concept categories that BBO ontology covers: Process, Input/output specifications, Agent, Work product, and Manufacturing facility.
- **Quote**: "Based on the study of the previous knowledge sources, we have identified five main concepts that must be covered by BBO ontology: 1. Process: it is the key concept... 2. Input/output specifications: tasks may require some input requirements (resources or parameter values) before being performed, or they may produce outcomes... 3. Agent: the actor that performs a given process activity... 4. Work product: to specify the process or processes that are required to produce a given product... 5. Manufacturing facility: the place where the process activities should be performed."
- **Context**: Specification section identifying core entity categories BBO must represent.

---

### Pattern: BBO Resource Taxonomy

- **Source**: 31-BBO_BPMN_Ontology (Chunk 1:299-303, 326-331)
- **Description**: Resource entity type taxonomy in BBO extending BPMN with hierarchical resource classification and WorkProduct as a specific MaterialResource type.
- **Quote**: "In BBO, like in (Karray et al., 2012), we adopt the first definition of Resource, that englobes all resource types. Hence, we may define a resource taxonomy (Figure 6). This taxonomy actually is relevant to answer to some competency questions like 'What is the type of a given resource?'... In (ISO, 2005), the term Product is defined as follows 'Thing or substance produced by a natural or artificial process.' We adopt this definition for the WorkProduct concept. In addition, we consider WorkProduct as a particular type of MaterialResource"
- **Context**: BBO conceptualization extending BPMN's limited resource representation.

---

### Pattern: BBO Manufacturing Facility Hierarchy

- **Source**: 31-BBO_BPMN_Ontology (Chunk 1:309-317)
- **Description**: Manufacturing facility entity type hierarchy in BBO including Station, Cell, Shop, and Factory with spatial containment relationships.
- **Quote**: "To specify where the task should be performed, we reused the taxonomies introduced in (Chungoora et al., 2013) and (Fraga, Vegetti and Leone, 2018)... A workstation, Station, is the place where a particular job is performed. Cell is the place that groups a set of related operations in the production flow, while Shop is the area where production is carried out, and Factory is the place where those production areas are located."
- **Context**: BBO conceptualization for manufacturing facility entity types not covered by BPMN.

---

### Pattern: BBO Agent Hierarchy

- **Source**: 31-BBO_BPMN_Ontology (Chunk 1:340-353)
- **Description**: Agent entity type hierarchy in BBO including HumanResource, SoftwareResource, Job, and Role with organizational relationships.
- **Quote**: "We reused the Agent sub-ontology proposed in (Ru'IZ et al., 2004)... An Agent may be a HumanResource or a SoftwareResource. The concept Job with the two relations 'subordinated' and 'superior' represent the organizational model of the company, which is not supported by BPMN meta-model. Note that, we differentiated Job from Role to offer more flexibility. Indeed, two persons that have the same Job, may have different authorization levels to execute Activities."
- **Context**: BBO agent conceptualization extending beyond BPMN's limited agent representation.

---

### Pattern: BBO InputOutputSpecification Entities

- **Source**: 31-BBO_BPMN_Ontology (Chunk 1:282-289)
- **Description**: Input/Output specification entity types in BBO including ParameterValueBinding, Parameter (Qualitative and Quantitative), ParameterValue, ParameterExpectedValue, and UnitOfMeasure.
- **Quote**: "Moreover, to represent the parameter values specifications, we have added the concepts: ParameterValueBinding, Parameter and its subclasses QualitativeParameter and QuantitativeParameter, ParameterValue, ParameterExpectedValue, and UnitOfMeasure. The UnitOfMeasure class is specified using the two concepts Unit and Prefix of the unit measures ontology UO"
- **Context**: BBO extension to BPMN for detailed input/output parameter representation.

---

### Pattern: BBO OWL Class Formalization

- **Source**: 31-BBO_BPMN_Ontology (Chunk 1:440-445)
- **Description**: Examples of how BPMN natural language specifications are converted to formal OWL class definitions with equivalence axioms.
- **Quote**: "ConvergingGateway equivalentTo (Gateway and (has_incoming min 2 SequenceFlow) and (has_outgoing exactly 1 SequenceFlow)); ConditionalSequenceFlow equivalentTo (SequenceFlow and has_conditionExpression some Expression); TimerEvent equivalentTo (Event and (has_eventDefinition exactly 1 TimerEventDefinition))"
- **Context**: Formalization section showing how entity types are defined with OWL restrictions.
