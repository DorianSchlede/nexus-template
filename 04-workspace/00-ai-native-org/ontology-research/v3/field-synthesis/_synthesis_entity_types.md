# Entity Types

**Source**: Project 16 Ontologies Research v3

**Type**: Synthesis Analysis (UDWO-Primed)

**Field**: entity_types

**Aggregated**: 2026-01-01T16:22:23.892932

**Batches Merged**: 11

---

## Table of Contents

- [Patterns](#patterns)

## Patterns

**Total Patterns**: 411

### 1. Endurant-Perdurant Dichotomy

The most fundamental entity type distinction in UFO. Endurants exist in time with all their parts and can qualitatively change while maintaining identity. Perdurants unfold in time accumulating temporal parts. This maps to the 8-entity hypothesis where Events are perdurants and most other entities (Agent, Resource, Data, Role) are endurants.

**Sources**:

- **01-UFO (Chunk 1:283-288)**
  > UFO is a 3D ontology having, as a fundamental distinction, the one between endurants and perdurants, as opposed to a 4D ontology in which all concrete individuals are perdurants

---

### 2. Endurant Definition

Core entity type definition. Endurants can change properties while remaining the same individual. The unique Kind they instantiate defines what changes are permissible. This supports modeling Agents, Resources, Roles as entities that persist through change.

**Sources**:

- **01-UFO (Chunk 1:285-288)**
  > Endurants are individuals that exist in time with all their parts. They have essential and accidental properties and, hence, they can qualitatively change while maintaining their numerical identity

---

### 3. Perdurant Definition

Events in the 8-entity hypothesis correspond to perdurants. They cannot change - any apparent change is variation between temporal parts or change in underlying endurants. Events are founded on dispositions inhering in endurants.

**Sources**:

- **01-UFO (Chunk 1:289-296)**
  > Perdurants are individuals that unfold in time accumulating temporal parts. They are manifestations of dispositions and only exist in the past. As such, perdurants are modally fragile

---

### 4. Substantial vs Moment Partition

Endurants partition into Substantials (independent, e.g., Mick Jagger, an organization) and Moments (existentially dependent, e.g., a headache, a marriage). This is the Aristotelian Square four-category ontology structure.

**Sources**:

- **01-UFO (Chunk 1:297-301)**
  > UFO is an ontology based of the so-called Aristotelian Square, thus, accounting for both substantial individuals (or Substantials), i.e., independent entities, as well as particularized properties, i.e., existentially dependent entities or moments

---

### 5. Object Entity Type

Merged from 4 sources. Objects are substantials with parts that have distinct functional roles. Maps to Agent (organizations are objects), Resource (computers, tools are objects). Unity comes from functional integration of parts.

**Sources**:

- **01-UFO (Chunk 1:360-361)**
  > Objects (aka functional complexes) are entities whose parts play differentiated functional roles with respect to the whole, e.g, a human body, an organization, a computer

- **02-Knowledge_Graphs (Chunk 6:489-491)**
  > Report crime claimant station date Pickpocketing XY12SDA Viña del Mar 2019-04-12

- **18-Multi-Agent_Taxonomy (Chunk 1:867-868)**
  > Synthesis: Evaluating and combining Task Results as well as finally presenting a unified Total Result

- **18-Multi-Agent_Taxonomy (Chunk 2:179-182)**
  > Context Utilization might involve the creation or modification of Artefacts. Beyond mere artefact manipulation, this utilization can manifest as external Impact, such as initiating external processes

---

### 6. Collective Entity Type

Collectives are substantials whose parts are homogeneous in role. Could model teams, groups of agents, resource pools. Distinct from Objects where parts have differentiated roles.

**Sources**:

- **01-UFO (Chunk 1:356-358)**
  > Collectives are entities whose parts play the same role with respect to the whole, e.g., the Black Forest (as a collective of trees), a deck of cards, the Dutch-speaking group

---

### 7. Quantity Entity Type

Merged from 3 sources. Activity can be treated as an entity type by using the Activity property as an entity identifier. This reveals queues between activities as entities that other objects pass through.

**Sources**:

- **01-UFO (Chunk 1:353-354)**
  > Quantities are maximally-topologically-self-connected (e.g., pieces) of homeomerous amounts of matter, e.g., that puddle of water, this particular pile of sand

- **02-Knowledge_Graphs (Chunk 6:205-207)**
  > typically targetting mentions of people, organisations, locations, and potentially other types

- **11-Process_Mining_Event_Knowledge_Graphs (Chunk 2:478-486)**
  > For example, if we pick the Activity property as 'entity identifier', we infer entities such as Receive SO, Unpack, Scan, Store, Retrieve, Pack Shipment...

---

### 8. Intrinsic Moment - Quality

Merged from 2 sources. Modes are intrinsic moments that cannot be directly projected to values but can bear other moments. Dispositions are key mode subtype - functions, capabilities map to what Agents and Resources can do.

**Sources**:

- **01-UFO (Chunk 1:302-306)**
  > Intrinsic moments are existentially dependent on a single individual. These include qualities, i.e., reifications of categorical properties such as color, height, weight, electrical charge

- **01-UFO (Chunk 1:321-323)**
  > Modes can bear their own moments, including their own qualities, which can vary in independent ways. The category of modes include dispositions (e.g., functions, capabilities, capacities, vulnerabilities)

---

### 9. Externally Dependent Mode

Merged from 2 sources. Modes that depend on entities other than their bearer. Example: John's love for Mary inheres in John but depends on Mary. Models relational properties between entities.

**Sources**:

- **01-UFO (Chunk 1:322-326)**
  > Externally dependent modes inhere in an entity while being externally dependent on another entity. A particularly interesting type of externally dependent mode is a qua individual

- **01-UFO (Chunk 2:189-196)**
  > a mode x that is existentially dependent on an entity that is independent of the bearer of x... ExternallyDependentMode(x) iff Mode(x) and exists y such that externallyDependent(x, y)

---

### 10. Relator Entity Type

Merged from 2 sources. Relators are aggregations of qua individuals sharing a foundational event. Examples: marriages, enrollments, employments, contracts, presidential mandates. Critical for modeling relationships between Agents, Roles, and Resources in the 8-entity hypothesis.

**Sources**:

- **01-UFO (Chunk 1:329-334)**
  > a relator is a moment (i.e., an existentially dependent entity) that is an aggregation of qua individuals. For instance, John and Mary's Marriage is composed of John-qua-husband-of-Mary and Mary-qua-wife-of-John

- **23-UFO_Story_Ontological_Foundations (Chunk 1:132-133)**
  > particularized relations (relationships) and particularized intrinsic properties (e.g., often represented by the so-called weak entities) are frequently modeled as bearers of other particularized properties

---

### 11. Qua Individual

Qua individuals aggregate externally dependent modes with common bearer and foundation. John-qua-husband-of-Mary bundles all John's conjugal commitments to Mary from their wedding. Models role-based identity aspects.

**Sources**:

- **01-UFO (Chunk 1:325-328)**
  > a qua individual is a mode composed of other externally dependent modes that share the same bearer, the same source of external dependence, and the same foundational event

---

### 12. Kind Entity Type

Merged from 9 sources. Kinds provide identity criteria - what makes an individual the same over time. Person, dog, computer, car, organization, marriage are kinds. Each endurant instantiates exactly one kind. Foundational for typing Agents, Resources, Roles.

**Sources**:

- **01-UFO (Chunk 1:368-369)**
  > a fundamental sort of endurant type is a kind, which provides uniform principles of individuation, identity, and persistence to its instances

- **01-UFO (Chunk 1:375-377)**
  > sortals whose contingent classification conditions are relational, termed roles (e.g., employee as a role of a person in the scope of an employment relator, and husband as a role of a person)

- **31-BBO_BPMN_Ontology (Chunk 1:350-353)**
  > we differentiated Job from Role to offer more flexibility. Indeed, two persons that have the same Job, may have different authorization levels to execute Activities

- **02-Knowledge_Graphs (Chunk 7:181-184)**
  > We may, for example, specify a shape City whose target nodes have at most one country. Then, given the edges [Chile] country Santiago country Cuba

- **18-Multi-Agent_Taxonomy (Chunk 1:453-461)**
  > Autonomous LLM-powered multi-agent systems are designed to accomplish user-prompted goals or complex tasks. For this purpose, the system employs an interactive and multi-perspective strategy

- **18-Multi-Agent_Taxonomy (Chunk 1:854-861)**
  > Internally, this user-prompted Goal (which might represent a directive, problem, question, or mission) undergoes decomposition into Tasks or Sub-Tasks to be manageable by the Agents

- **18-Multi-Agent_Taxonomy (Chunk 1:876)**
  > Actions within this activity are delegated to specialized Agents - each characterized by a distinct Role, Type, and further competencies

- **18-Multi-Agent_Taxonomy (Chunk 2:104-124)**
  > Tools in terms of contextual resources for multi-agent systems can be categorized into... Search and Analysis Tools... Execution Tools... Reasoning Tools... Development Tools... Communication Tools

- **18-Multi-Agent_Taxonomy (Chunk 2:127-144)**
  > Data types in multi-agent architectures encompass: Structured Text Data... Unstructured Text Data... Multimodal Data... Domain-specific Data

---

### 13. Sortal Entity Type

Merged from 3 sources. Person is a fundamental entity type recognized in knowledge graph construction. People entities are identified through Named Entity Recognition and linked to graph nodes.

**Sources**:

- **01-UFO (Chunk 1:369-372)**
  > A sortal is either a kind or a specialization of a kind, and every sortal that is not a kind specializes exactly one kind. These specializations can be either themselves rigid (subkinds)

- **02-Knowledge_Graphs (Chunk 6:205-207)**
  > The NER task identifies mentions of named entities in a text, typically targetting mentions of people, organisations, locations

- **19-GoT_Reasoning (Chunk 1:406-410)**
  > The Parser extracts information from LLM thoughts. For each such thought, the Parser constructs the thought state, which contains this extracted information

---

### 14. Phase Entity Type

Merged from 6 sources. Event is defined as an occurrence that happens during process execution, affecting flow and requiring reactions. This directly validates the Event entity in the 8-entity hypothesis. BPMN distinguishes interrupting vs non-interrupting events and multiple types (TimerEvent, ConditionalEvent, etc.).

**Sources**:

- **01-UFO (Chunk 1:373-375)**
  > sortals whose contingent classification conditions are intrinsic, termed Phases (e.g., teenager as a phase of person, hemorrhagic dengue fever as a phase of dengue fever)

- **31-BBO_BPMN_Ontology (Chunk 1:236-239)**
  > Event is something that 'happens' during the course of a process. Events affect the flow of the process and usually have a cause or an impact

- **31-BBO_BPMN_Ontology (Chunk 1:191-192)**
  > Agent: the actor that performs a given process activity. Indeed, it is important to specify who is responsible for the accomplishment of a given activity

- **02-Knowledge_Graphs (Chunk 8:324-328)**
  > quasi-identifiers (passport, plane ticket) have been converted into blank nodes, ensuring that the passenger (the dashed blank node) cannot be distinguished

- **02-Knowledge_Graphs (Chunk 14:11)**
  > σ(Santa Lucía, Venue) = 1

- **11-Process_Mining_Event_Knowledge_Graphs (Chunk 2:595-604)**
  > Often called 'resources' in process management literature, we prefer the term Actor used in organizations research, as each actor follows its own behavior.

---

### 15. Category (Non-Sortal)

Categories are rigid non-sortals abstracting essential properties across kinds. Physical Object applies to cars, persons, bridges. Enables cross-kind generalization.

**Sources**:

- **01-UFO (Chunk 1:381-383)**
  > categories: rigid types that define essential properties for their instances, e.g., the category 'physical object' describing the properties of having a mass and a spatial extension

---

### 16. Phase Mixin (Non-Sortal)

Phase mixins abstract intrinsic contingent properties across kinds. Living Animal applies to persons, dogs, horses. Non-sortal version of phases.

**Sources**:

- **01-UFO (Chunk 1:385-388)**
  > phase mixins: anti-rigid types that define contingent properties for their instances. Their instantiation is characterized by intrinsic contingent conditions. For example, 'living animal'

---

### 17. Role Mixin (Non-Sortal)

Role mixins abstract relational contingent properties across kinds. Customer applies to persons and organizations. Non-sortal version of roles.

**Sources**:

- **01-UFO (Chunk 1:390-392)**
  > role mixins: anti-rigid types that define contingent properties for their instances. Their instantiation is characterized by relational contingent conditions. Examples include 'customer'

---

### 18. Mixin (Semi-Rigid Non-Sortal)

Mixins have properties essential to some instances, accidental to others. Music artist essential to bands, accidental to people. Captures cross-kind type variation.

**Sources**:

- **01-UFO (Chunk 1:394-395)**
  > mixins: semi-rigid types that define properties that are essential to some of their instances but accidental to some other instances (e.g., being a 'music artist' is essential to bands but accidental to people)

---

### 19. UFO-A: Endurant Ontology

First fragment of UFO covering all endurant types - substantials, moments, qualities, modes, relators. Foundation for modeling persistent entities.

**Sources**:

- **01-UFO (Chunk 1:273)**
  > UFO-A, which is an ontology of endurants

---

### 20. UFO-B: Perdurant Ontology

Second fragment covering events, processes, temporal entities. Foundation for modeling Events in the 8-entity hypothesis.

**Sources**:

- **01-UFO (Chunk 1:275)**
  > UFO-B, which is an ontology of perdurants

---

### 21. UFO-C: Social and Intentional Ontology

Third fragment building on UFO-A and UFO-B for social reality - agents, goals, commitments. Critical for Agent modeling in the 8-entity hypothesis.

**Sources**:

- **01-UFO (Chunk 1:277-279)**
  > UFO-C, which is an ontology of social and intentional entities build on the foundations provided by the other two

---

### 22. Type Definition (Formal)

Formal definition: Type(x) iff possibly exists y such that y instantiates x. Types are patterns that can have instances.

**Sources**:

- **01-UFO (Chunk 1:454)**
  > types are implicitly defined as those entities that are possibly instantiated (a1)

---

### 23. Individual Definition (Formal)

Formal definition: Individuals cannot have instances. The domain partitions into types and individuals.

**Sources**:

- **01-UFO (Chunk 1:462-463)**
  > Individual(x) iff necessarily not exists y such that y instantiates x

---

### 24. Concrete vs Abstract Individual

Individuals split into concrete (endurants, perdurants) and abstract (sets, quales). Abstract individuals include quality structures.

**Sources**:

- **01-UFO (Chunk 1:507-509)**
  > Among the individuals, there are concrete individuals and abstract individuals. Concrete individuals are further differentiated into endurants and perdurants

---

### 25. EndurantType and PerdurantType

Type-level distinction mirrors individual distinction. EndurantTypes have only endurant instances, PerdurantTypes have only perdurant instances.

**Sources**:

- **01-UFO (Chunk 1:541-542)**
  > types are classified into types of endurants and types of perdurants, which are both disjoint

---

### 26. Rigid Type

Rigidity classifies how necessarily types apply. Rigid types apply necessarily to instances. Anti-rigid types apply contingently. Semi-rigid types are neither.

**Sources**:

- **01-UFO (Chunk 1:557-558)**
  > rigidity of endurant types as rigid, anti-rigid and semi-rigid

---

### 27. Anti-Rigid Type

Anti-rigid types classify contingently - instances can cease instantiating them. Phases, roles, phase mixins, role mixins are anti-rigid.

**Sources**:

- **01-UFO (Chunk 1:564)**
  > AntiRigid(t) iff EndurantType(t) and for all x, if possibly x instantiates t then possibly x does not instantiate t

---

### 28. Substantial-Moment Partition (Formal)

Formal taxonomy: Endurant = Substantial + Moment. Substantial = Object + Collective + Quantity. Complete and disjoint partition.

**Sources**:

- **01-UFO (Chunk 1:702-703)**
  > Endurant is partitioned into Substantial and Moment. Additionally, Substantial is partitioned into Object, Collective and Quantity

---

### 29. Moment Partition (Formal)

Formal taxonomy: Moment = Relator + IntrinsicMoment. IntrinsicMoment = Mode + Quality. Six leaf endurant categories: Object, Collective, Quantity, Relator, Mode, Quality.

**Sources**:

- **01-UFO (Chunk 1:709-712)**
  > Moment is partitioned into Relator and IntrinsicMoment. Finally, IntrinsicMoment is partitioned into Mode and Quality

---

### 30. Parthood Relations

UFO includes formal mereology for part-whole relations. Supports modeling complex entities composed of parts - organizations from departments, tasks from subtasks.

**Sources**:

- **01-UFO (Chunk 1:874-888)**
  > we formalize general extensional mereology. reflexivity, anti-symmetry, transitivity, Overlap, Strong supplementation, Proper Part

---

### 31. ComponentOf Relation

ComponentOf combines parthood with functional dependence. Parts function in roles relative to wholes. Enables functional decomposition of complex entities.

**Sources**:

- **01-UFO (Chunk 1:909-912)**
  > We can now introduce the notion of component of... componentOf(x, x', y, y') iff x proper-part-of y and individual-functional-dependence(x, x', y, y')

---

### 32. Constitution Relation

Constitution relates entities of same category but different kinds. A statue is constituted by clay - same category (endurant) but different kinds. Not identity - different lifecycle, modal properties.

**Sources**:

- **01-UFO (Chunk 2:18-22)**
  > constitution is a relation that holds between things of the same ontological category... However, following Baker (2007), constitution holds between things of different Kinds

---

### 33. Inherence Relation

Inherence ties moments to bearers. Non-reflexive, asymmetric, anti-transitive. A quality inheres in exactly one bearer. Foundational for modeling properties of Agents, Resources.

**Sources**:

- **01-UFO (Chunk 2:137-139)**
  > The relation that connects moments to the object that they are about is the relation of inherence. Inherence is a type of existential dependence relation holding between a moment and an entity

---

### 34. Foundational Event

Externally dependent modes and relators have a unique foundational event. The wedding founds the marriage relator. Links Events to Roles and relationships.

**Sources**:

- **01-UFO (Chunk 2:207-210)**
  > Externally dependent modes (as well as relators) are founded by means of a unique event. E.g., John's conjugal commitments towards Mary are founded on the event of the wedding

---

### 35. Relator (Formal Definition)

Formal relator definition: aggregation of mutually dependent qua individuals with common foundational event. Relators mediate at least two distinct individuals.

**Sources**:

- **01-UFO (Chunk 2:247-264)**
  > relators are sums of qua individuals that share the same foundation and are existentially dependent on each other

---

### 36. Mediation Relation

Mediation links relators to the individuals they connect. A marriage relator mediates husband and wife. Critical for modeling Role-based relationships.

**Sources**:

- **01-UFO (Chunk 2:279-280)**
  > We introduce the relation of mediation, mediates(x, y), between a relator x and an individual y that the relator connects in a relational statement

---

### 37. Quality Structure

Quality structures define value spaces for quality types. Contains quales (singular values). Partitions into quality dimensions (one-dimensional) and quality domains (multi-dimensional).

**Sources**:

- **01-UFO (Chunk 2:349-357)**
  > A quality structure is defined as an entity associated with a unique quality type. quality structures are non-empty sets. The members of quality structures are quales

---

### 38. Quality Dimension vs Domain

Quality dimensions are one-dimensional (height, weight). Quality domains combine dimensions (color as hue+saturation+brightness). Structures measurable properties.

**Sources**:

- **01-UFO (Chunk 2:351-352)**
  > A quality structure is partitioned into quality dimension and quality domain

---

### 39. HasValue Relation

Each quality has exactly one value (quale) at a time. Values come from associated quality structure. Enables property change while maintaining quality identity.

**Sources**:

- **01-UFO (Chunk 2:386-388)**
  > The hasValue relation holds from qualities to quales, where hasValue is functional

---

### 40. Manifestation Relation

Manifestation links endurants to their events. The life of an endurant is the sum of all events manifesting it. Connects Agents to their Events/Activities.

**Sources**:

- **01-UFO (Chunk 2:505-507)**
  > Any endurant is connected to a perdurant by the manifestation relation... The life of an endurant is then specified by a functional relation that associates the endurant with the mereological sum of all events

---

### 41. AI Agent Entity

Defines AI agents as intelligent entities with perception, reasoning, and autonomous execution capabilities. This maps to the Agent entity type in the 8-entity hypothesis, with autonomous and intentional characteristics.

**Sources**:

- **20-Agentic_RAG_Survey (Chunk 1:104-107)**
  > Modern agents, including LLM-powered and mobile agents, are intelligent entities capable of perceiving, reasoning, and autonomously executing tasks

---

### 42. Agent Components - LLM Role and Task

Identifies Role and Task as core components of an AI agent. The LLM serves both a Role (reasoning engine) and executes Tasks (interpreting queries, generating responses). This supports the Task and Role entity types.

**Sources**:

- **20-Agentic_RAG_Survey (Chunk 1:487-488)**
  > LLM (with defined Role and Task): Serves as the agent's primary reasoning engine and dialogue interface. It interprets user queries, generates responses

---

### 43. Agent Memory Entity

Memory as a distinct entity type within agents, with temporal differentiation (short-term vs long-term). This relates to Data entity type as persistent information storage.

**Sources**:

- **20-Agentic_RAG_Survey (Chunk 1:491-493)**
  > Memory (Short-Term and Long-Term): Captures context and relevant data across interactions. Short-term memory tracks immediate conversation state, while long-term memory stores accumulated knowledge

---

### 44. Agent Planning Entity

Planning as an entity that decomposes complex tasks into subtasks. This directly supports the Goal and Task entity hierarchy, where plans bridge goals to executable tasks.

**Sources**:

- **20-Agentic_RAG_Survey (Chunk 1:496-497)**
  > Planning (Reflection & Self-Critique): Guides the agent's iterative reasoning process through reflection, query routing, or self-critique, ensuring that complex tasks are broken down effectively

---

### 45. Agent Tools Entity

Tools as distinct entities that extend agent capabilities. Maps to Resource entity type - external capabilities agents can invoke to accomplish tasks.

**Sources**:

- **20-Agentic_RAG_Survey (Chunk 1:500-501)**
  > Tools (Vector Search, Web Search, APIs, etc.): Expands the agent's capabilities beyond text generation, enabling access to external resources, real-time data, or specialized computations

---

### 46. Retrieval Entity

Retrieval as a core component entity in RAG architecture. Functions as a Resource/Tool that interfaces between agents and Data sources (knowledge bases, APIs, databases).

**Sources**:

- **20-Agentic_RAG_Survey (Chunk 1:161-163)**
  > Retrieval: Responsible for querying external data sources such as knowledge bases, APIs, or vector databases. Advanced retrievers leverage dense vector search and transformer-based models

---

### 47. Query Entity

Query as an entity that initiates processing workflows. Represents a specific type of Event that triggers agent activities and retrieval processes.

**Sources**:

- **20-Agentic_RAG_Survey (Chunk 1:764-766)**
  > Query Submission and Evaluation: The process begins when a user submits a query. A coordinating agent (or master retrieval agent) receives the query and analyzes it

---

### 48. Knowledge Base Entity

Merged from 2 sources. A structured entity representing chains of concepts connected by relationships extracted from a knowledge graph. Knowledge paths serve as the input substrate for multi-agent reasoning.

**Sources**:

- **20-Agentic_RAG_Survey (Chunk 1:98-99)**
  > These systems retrieve real-time information from sources such as knowledge bases, APIs, or the web, effectively bridging the gap between static training data and the demands of dynamic applications

- **15-SciAgents (Chunk 3:888-892)**
  > silk -- provide functionalities -- biological materials -- can be integrated -- novel functionalities -- can be integrated -- biological materials...

---

### 49. Document Entity

Document as a Data entity type that contains textual content retrievable by agents. Documents are processed, evaluated for relevance, and used in response generation.

**Sources**:

- **20-Agentic_RAG_Survey (Chunk 2:229)**
  > Context Retrieval Agent: Responsible for retrieving initial context documents from a vector database

---

### 50. Graph Knowledge Entity

Graph knowledge bases as structured Data entities that encode relationships between concepts. Enables multi-hop reasoning through connected entity relationships.

**Sources**:

- **20-Agentic_RAG_Survey (Chunk 2:466-467)**
  > Graph Knowledge Bases: Structured data is used to extract relationships, hierarchies, and connections (e.g., disease-to-symptom mappings in healthcare)

---

### 51. Coordinator Agent Entity

Coordinator/Master agent as a specialized Agent entity type with orchestration responsibilities. Delegates work to specialized agents, embodying hierarchical Role patterns.

**Sources**:

- **20-Agentic_RAG_Survey (Chunk 1:886-888)**
  > Query Submission: The process begins with a user query, which is received by a coordinator agent or master retrieval agent. This agent acts as the central orchestrator

---

### 52. Specialized Retrieval Agent Entity

Specialized agents as Agent subtypes with domain-specific capabilities. Examples include SQL agent, semantic search agent, web search agent - each with distinct Resource access patterns.

**Sources**:

- **20-Agentic_RAG_Survey (Chunk 1:890-904)**
  > Specialized Retrieval Agents: The query is distributed among multiple retrieval agents, each focusing on a specific type of data source or task

---

### 53. Workflow Entity

Workflow as a pattern entity that orchestrates Task sequences. Includes routing, parallelization, and evaluation patterns - procedural structures that organize agent activities.

**Sources**:

- **20-Agentic_RAG_Survey (Chunk 1:110-112)**
  > These agents employ agentic workflow patterns, such as prompt chaining, routing, parallelization, orchestrator-worker models, and evaluator-optimizer, to structure and optimize task execution

---

### 54. Response Entity

Response/Output as a Data entity produced by agent processing. Represents synthesized information delivered to users after retrieval and generation steps.

**Sources**:

- **20-Agentic_RAG_Survey (Chunk 2:33-34)**
  > Output Generation: The system generates a comprehensive response, which is delivered back to the user in an actionable and concise format

---

### 55. Evaluation Agent Entity

Evaluation agent as an Agent subtype that applies Rules (relevance criteria) to Data (documents). Implements quality control through judgment and classification activities.

**Sources**:

- **20-Agentic_RAG_Survey (Chunk 2:232-234)**
  > Relevance Evaluation Agent: Assesses the retrieved documents for relevance and flags any irrelevant or ambiguous documents for corrective actions

---

### 56. Critic Module Entity

Critic as a component entity that validates Data quality. Applies Rules (confidence thresholds) to filter and refine retrieved information.

**Sources**:

- **20-Agentic_RAG_Survey (Chunk 2:493-499)**
  > Critic Module: Validates retrieved data for relevance and quality. Flags low-confidence results for re-retrieval or refinement

---

### 57. Large Language Model Entity

LLMs as a distinct Agent entity type - AI systems capable of code generation and natural language understanding. They can perform complex tasks including analyzing business process models.

**Sources**:

- **21-LLM_Smart_Contracts_from_BPMN (Chunk 1:131-133)**
  > Large Language Models (LLMs) are transformer-based neural network systems. LLMs are a specific class of Foundation Models, a class of machine learning models trained on extensive data sets

---

### 58. Smart Contract Entity

Smart contracts as executable Rule entities that enforce process logic on blockchain. They codify business Rules as immutable, automatically executed code.

**Sources**:

- **21-LLM_Smart_Contracts_from_BPMN (Chunk 1:93-94)**
  > we present an exploratory study investigating the use of LLMs to generate smart contract code from business process descriptions

---

### 59. Business Process Entity

Business process as a structured entity containing Tasks, control flow, and Rules. Process models serve as input specifications that can be transformed into executable artifacts.

**Sources**:

- **21-LLM_Smart_Contracts_from_BPMN (Chunk 1:54-55)**
  > Blockchain-based business process execution relies on a model-driven paradigm, where process descriptions are transformed into executable artefacts based on rule-based transformation tools

---

### 60. BPMN Choreography Entity

BPMN Choreography as a process model entity type representing multi-participant collaboration. Contains choreography tasks, start/end events, gateways, and sub-choreographies.

**Sources**:

- **21-LLM_Smart_Contracts_from_BPMN (Chunk 1:338-340)**
  > In the current instantiation of our framework, we support BPMN 2.0 Choreographies. This is a purely practical implementation choice

---

### 61. Task Entity in BPMN

Task as the fundamental activity unit in business processes. Has ordering constraints (control flow), Resource assignment (initiator), and can be gated by conditions.

**Sources**:

- **21-LLM_Smart_Contracts_from_BPMN (Chunk 1:467-469)**
  > enforcing: (i) the control flow, i.e., the order of tasks, (ii) that only the respective initiator can execute a task, and (iii) the autonomous enforcement of gateways

---

### 62. Participant Entity

Participant as an Agent/Role entity in choreography models. Participants are mapped to blockchain addresses and authorized to execute specific tasks.

**Sources**:

- **21-LLM_Smart_Contracts_from_BPMN (Chunk 1:313-314)**
  > The simulator also generates an encoding that maps the events and participants to how they should be represented in the smart contract (taskIDs and participantIDs)

---

### 63. Gateway Entity

Merged from 2 sources. Gateway is a flow control entity type that manages branching and merging of process flows. Four subtypes: ConvergingGateway, DivergingGateway, MixedGateway, UnspecifiedGateway. This relates to Rule entity type as gateways encode decision logic.

**Sources**:

- **21-LLM_Smart_Contracts_from_BPMN (Chunk 1:355-358)**
  > As we also want to benchmark data-based exclusive gateways (XOR), we had to extend the playout functionality to generate appropriate data manipulation events

- **31-BBO_BPMN_Ontology (Chunk 1:241)**
  > Gateway is used to control how SequenceFlows interact as they converge or diverge within a Process

---

### 64. Event Entity in Process

Event as an occurrence entity in process execution logs. Events represent task executions, grouped by case ID, forming traces that record process instances.

**Sources**:

- **21-LLM_Smart_Contracts_from_BPMN (Chunk 1:247-250)**
  > each event is associated with a case identifier that groups it into a case. A trace is the ordered sequence of events (activities) that occurred for a specific case

---

### 65. Trace Entity

Trace as a sequence of Events that records one complete process execution. Traces are validated against process models for conformance checking.

**Sources**:

- **21-LLM_Smart_Contracts_from_BPMN (Chunk 1:250)**
  > A trace can be said to be in conformance with a process model if it represents a valid execution path through that model

---

### 66. Token Entity

Token as the atomic Data unit for LLM processing. Tokens influence computational load and cost, serving as the currency of LLM interactions.

**Sources**:

- **21-LLM_Smart_Contracts_from_BPMN (Chunk 1:148-150)**
  > Tokens are the units of input and output for LLMs. Tokens can be whole words, subwords (parts of words), individual characters, punctuation, or special characters

---

### 67. Software Robot Entity

Software robot as an Agent entity that automates human tasks. Bots interact with user interfaces through mouse clicks, keyboard interactions, and text interpretation.

**Sources**:

- **22-RPA_Framework_BPM_Activities (Chunk 1:88-90)**
  > This is achieved by the application of software algorithms known as software robots or bots, which are imitating the execution flow of humans on the front-end

---

### 68. Process Activity Entity

Process activity as the fundamental Task entity for RPA evaluation. Activities have measurable characteristics (standardization, frequency, determinism) that determine automation viability.

**Sources**:

- **22-RPA_Framework_BPM_Activities (Chunk 1:62-63)**
  > What are the characteristics of a process activity, or a set of process activities, that facilitate viable robotic process automation?

---

### 69. User Interface Entity

User interface as a Resource/tool entity that mediates between agents (human or robot) and information systems. The presentation layer through which activities are executed.

**Sources**:

- **22-RPA_Framework_BPM_Activities (Chunk 1:95-96)**
  > Just as a human user, robots can interact with the user interface through mouse clicks, key board interactions and interpretation of text and graphics

---

### 70. Information System Entity

Information systems as Data/Resource infrastructure entities. Multiple systems may be involved in a process, requiring data transfer and interaction coordination.

**Sources**:

- **22-RPA_Framework_BPM_Activities (Chunk 1:98-99)**
  > RPA usually does not require defined interfaces as the software sits on top of information systems and accesses applications only through the presentation layer

---

### 71. Task Perspective Entity

Merged from 3 sources. Task perspective as an evaluation framework dimension. Contains criteria for assessing Task entity characteristics: standardization, maturity, determinism, failure rate.

**Sources**:

- **22-RPA_Framework_BPM_Activities (Chunk 1:325-326)**
  > Task perspective: The task perspective refers to the execution of process activities. Its criteria are standardization, maturity, determinism, and failure rate

- **22-RPA_Framework_BPM_Activities (Chunk 1:347-349)**
  > Time perspective: The criteria listed under the time perspective focus on the duration and frequency of processes and process steps

- **22-RPA_Framework_BPM_Activities (Chunk 1:365-368)**
  > Data perspective: In many processes, information is processed in multiple systems. Therefore, the data perspective resembles the structuredness of data

---

### 72. System Perspective Entity

System perspective as an evaluation dimension for Resource/infrastructure characteristics. Evaluates interface interactions, stability, and number of systems involved.

**Sources**:

- **22-RPA_Framework_BPM_Activities (Chunk 1:377-379)**
  > System perspective: The fourth perspective in the framework is related to the underlying systems. The perspective poses the interaction with interfaces, and the stability

---

### 73. Human Perspective Entity

Human perspective as an evaluation dimension for Role/Agent characteristics. Assesses human resource involvement and error proneness in process execution.

**Sources**:

- **22-RPA_Framework_BPM_Activities (Chunk 1:397-398)**
  > Human perspective: The last perspective deals with humans computer interaction focusing on the human. The perspective comes with two peculiarities, resources and proneness to human error

---

### 74. Exception Entity

Exception as an Event entity representing deviation from normal process flow. Exceptions indicate failure, require intervention, and reduce automation viability.

**Sources**:

- **22-RPA_Framework_BPM_Activities (Chunk 1:146-148)**
  > Candidate processes suited for RPA show little or no amount of exceptions when tasks are being executed and do not require human intervention

---

### 75. Endurant Entity

Endurant as a foundational entity type in UFO - entities wholly present at any time they exist. Includes objects, roles, and their properties. Distinguishes from perdurants (events/processes).

**Sources**:

- **23-UFO_Story_Ontological_Foundations (Chunk 1:173-178)**
  > UFO-A: An Ontology of Endurants dealing with aspects of structural conceptual modeling. It is organized as a Four-Category ontology comprising theories of Types and Taxonomic Structures

---

### 76. Perdurant Entity

Perdurant as a foundational entity type - entities that unfold in time with temporal parts. Includes Events and Processes. Connected to endurants through participation and dispositions.

**Sources**:

- **23-UFO_Story_Ontological_Foundations (Chunk 1:183-185)**
  > UFO-B: An Ontology of Perdurants (Events, Processes) dealing with aspects such as Perdurant Mereology, Temporal Ordering of Perdurants, Object Participation in Perdurants, Causation

---

### 77. Intentional Entity

Intentional entities in UFO including Beliefs, Desires, Intentions, Goals, and Actions. These cognitive/volitional states underpin Goal and Agent entity types with mental content.

**Sources**:

- **23-UFO_Story_Ontological_Foundations (Chunk 1:191-193)**
  > UFO-C: An Ontology of Intentional and Social Entities, which is constructed on top of UFO-A and UFO-B, and which addresses notions such as Beliefs, Desires, Intentions, Goals, Actions

---

### 78. Social Entity

Social entities in UFO including Commitments, Claims, Social Roles, and Social Relators. These ground interpersonal relationships and organizational structures.

**Sources**:

- **23-UFO_Story_Ontological_Foundations (Chunk 1:192-193)**
  > notions such as Beliefs, Desires, Intentions, Goals, Actions, Commitments and Claims, Social Roles and Social Particularized Relational Complexes (Social Relators)

---

### 79. Universal Entity

Universal as a meta-entity type in Four-Category Ontology. Universals are types/classes that individuals instantiate. Required for modeling entity types and taxonomies.

**Sources**:

- **23-UFO_Story_Ontological_Foundations (Chunk 1:126-129)**
  > we needed an ontological theory that would countenance both individuals and universals and one that would include not only substantial individuals and universals but also accidents

---

### 80. Moment/Trope Entity

Moments/tropes as particularized properties - individual instances of qualities or modes inhering in objects. Examples include specific color instances, relationships between individuals.

**Sources**:

- **23-UFO_Story_Ontological_Foundations (Chunk 1:128-129)**
  > we needed a Four-Category Ontology. We needed particularized properties not only because they were of great importance in making sense of language and cognition

---

### 81. Role Entity in UFO

Merged from 2 sources. Kind as a substance sortal in UFO that supplies identity criteria to individuals. Kinds are rigid types (Person, Organization) that define what something essentially is.

**Sources**:

- **23-UFO_Story_Ontological_Foundations (Chunk 1:154-156)**
  > we needed something in the spirit of the ontology of universals underlying the OntoClean methodology in order to systematize a number of notions that were pervasive in the conceptual modeling literature (e.g., types, roles, phases or states, mixins)

- **23-UFO_Story_Ontological_Foundations (Chunk 1:367)**
  > These distinctions, however, were considered to be distinctions among object universals. However, consciously ignoring this rule, users of the language started to systematically employ these distinctions

---

### 82. Process as Key Entity

Process is identified as the central entity type in BBO. It supports hierarchical decomposition into sub-processes and tasks, with ordering constraints controlled by events and conditions. This maps to the Activity entity in the 8-entity hypothesis.

**Sources**:

- **31-BBO_BPMN_Ontology (Chunk 1:185-187)**
  > Process: it is the key concept. The ontology should enable (i) to represent the decomposition of a given process in activities

---

### 83. Activity Entity Type with Three Subclasses

Activity is defined as the work entity with a clear taxonomy: Task (atomic), Sub-Process (composite), and CallActivity (reusable). This supports the Task entity type in the 8-entity hypothesis with clear atomic/composite distinction.

**Sources**:

- **31-BBO_BPMN_Ontology (Chunk 1:229-234)**
  > Activity is the work to be performed. Activity class has three sub-classes: Task: an atomic task, Sub-Process: complex task that contains several Tasks, CallActivity

---

### 84. Agent Subclasses - Human and Software

Agent is taxonomized into HumanResource and SoftwareResource. This supports AI agent integration patterns where software agents are first-class entities alongside human actors. Job entity captures organizational hierarchy.

**Sources**:

- **31-BBO_BPMN_Ontology (Chunk 1:346-347)**
  > An Agent may be a HumanResource or a SoftwareResource. The concept Job with the two relations 'subordinated' and 'superior' represent the organizational model

---

### 85. Resource Entity Type

Merged from 2 sources. Resource is defined broadly to encompass all resource types (not just agents). BBO adopts a comprehensive Resource taxonomy including MaterialResource, SoftwareResource, HumanResource, etc. Validates Resource entity in 8-entity hypothesis.

**Sources**:

- **31-BBO_BPMN_Ontology (Chunk 1:290-293)**
  > The Resource concept exists in the BPMN meta-model. However, its semantics and definition are ambiguous... we adopt the first definition of Resource, that englobes all resource types

- **11-Process_Mining_Event_Knowledge_Graphs (Chunk 2:188-193)**
  > This is because our graph of Fig. 9 is incomplete as we did not (a) infer the Resource entity and the corresponding df-relationships from Table 1...

---

### 86. Resource Taxonomy

BBO defines a formal Resource taxonomy with multiple types including MaterialResource, SoftwareResource, ExecutableScript, Tool, DataResource. This provides rich typing for the Resource entity.

**Sources**:

- **31-BBO_BPMN_Ontology (Chunk 1:300-303)**
  > Hence, we may define a resource taxonomy (Figure 6). This taxonomy actually is relevant to answer to some competency questions like 'What is the type of a given resource?'

---

### 87. Input/Output Specifications Entity

InputOutputSpecification is an entity type that captures data flow - what resources/parameters flow into and out of activities. This relates to the Data entity in 8-entity hypothesis.

**Sources**:

- **31-BBO_BPMN_Ontology (Chunk 1:188-190)**
  > Input/output specifications: tasks may require some input requirements (resources or parameter values) before being performed, or they may produce outcomes

---

### 88. Data Resource Entity Type

DataResource is a subtype of Resource representing data objects that flow between activities. Combined with InputOutputSpecification, this validates the Data entity type in 8-entity hypothesis.

**Sources**:

- **31-BBO_BPMN_Ontology (Chunk 1:282-284)**
  > we need to represent the input and output of each activity. In BPMN meta-model, an activity may have at most one InputOutputSpecification that is related to the required Input/Output Data

---

### 89. WorkProduct Entity Type

WorkProduct is an entity type representing outputs of processes. Defined as a subtype of MaterialResource since products can become inputs for subsequent activities. Relates to Data/Resource entities.

**Sources**:

- **31-BBO_BPMN_Ontology (Chunk 1:326-331)**
  > the term Product is defined as follows 'Thing or substance produced by a natural or artificial process.' We adopt this definition for the WorkProduct concept

---

### 90. ManufacturingFacility Entity Type

ManufacturingFacility is an entity type for location/place where activities occur. Taxonomy includes Station, Cell, Shop, Factory. This could be considered a specialized Resource type.

**Sources**:

- **31-BBO_BPMN_Ontology (Chunk 1:193-195)**
  > Manufacturing facility: the place where the process activities should be performed

---

### 91. ManufacturingFacility Taxonomy

ManufacturingFacility has a hierarchical taxonomy: Station (workstation), Cell (grouped operations), Shop (production area), Factory (overall facility). Provides granular location modeling.

**Sources**:

- **31-BBO_BPMN_Ontology (Chunk 1:311-313)**
  > A workstation, Station, is where a particular job is performed. Cell is the place that groups a set of related operations in the production flow, while Shop is the area where production is carried out

---

### 92. FlowElement Entity Type

FlowElement is a supertype for process components with two main subclasses: SequenceFlow (transitions) and FlowNode (activities, events, gateways). This provides structural organization for process entities.

**Sources**:

- **31-BBO_BPMN_Ontology (Chunk 1:220-223)**
  > Describing a process consists in defining the FlowElements that compose it. FlowElements class has two subclasses: SequenceFlow and FlowNode

---

### 93. SequenceFlow Entity Type

SequenceFlow is an entity type representing directed transitions between process nodes. Can be conditional, default, or normal. Encodes process flow logic.

**Sources**:

- **31-BBO_BPMN_Ontology (Chunk 1:221-222)**
  > SequenceFlow represents transitions that ensure the move from the source FlowNode to the target one. A SequenceFlow may depend on a given condition

---

### 94. SequenceFlow Subtypes

SequenceFlow has three subtypes based on conditionality: ConditionalSequenceFlow (condition-dependent), DefaultSequenceFlow (fallback path), NormalSequenceFlow (unconditional transition).

**Sources**:

- **31-BBO_BPMN_Ontology (Chunk 1:259)**
  > SequenceFlow: ConditionalSequenceFlow, DefaultSequenceFlow, NormalSequenceFlow

---

### 95. Expression Entity Type

Expression is an entity type for conditions and constraints. Used to define conditional logic for sequence flows and events. Relates to Rule entity in 8-entity hypothesis.

**Sources**:

- **31-BBO_BPMN_Ontology (Chunk 1:222-223)**
  > A SequenceFlow may depend on a given condition, which is represented as an instance of Expression class

---

### 96. Event Subtypes

Event entity has extensive subtyping: CancelEvent, ConditionalEvent, ErrorEvent, MultipleEvent, NoneEvent, TimerEvent, and more. StartEvent and EndEvent are positional subtypes.

**Sources**:

- **31-BBO_BPMN_Ontology (Chunk 1:263)**
  > Event: cancelEvent, conditionalEvent, ErrorEvent, MultipleEvent, NoneEvent, TimerEvent, etc.

---

### 97. Parameter Entity Types

Parameter is an entity type with two subtypes: QualitativeParameter and QuantitativeParameter. Related entities include ParameterValue, ParameterExpectedValue, and ParameterValueBinding for value specifications.

**Sources**:

- **31-BBO_BPMN_Ontology (Chunk 1:287-288)**
  > we have added the concepts: ParameterValueBinding, Parameter and its subclasses QualitativeParameter and QuantitativeParameter, ParameterValue, ParameterExpectedValue

---

### 98. UnitOfMeasure Entity Type

UnitOfMeasure is an entity type for measurement units, composed of Unit and Prefix. Reused from external UO ontology for standardization.

**Sources**:

- **31-BBO_BPMN_Ontology (Chunk 1:288-289)**
  > The UnitOfMeasure class is specified using the two concepts Unit and Prefix of the unit measures ontology UO

---

### 99. Job Entity Type

Merged from 2 sources. Entity types (like Order, Supplier Order, Item, Invoice, Payment, Resource) categorize entities in event knowledge graphs. Each column designating entities becomes an entity type. Entity types structure the multi-dimensional behavioral analysis.

**Sources**:

- **31-BBO_BPMN_Ontology (Chunk 1:346-348)**
  > The concept Job with the two relations 'subordinated' and 'superior' represent the organizational model of the company

- **11-Process_Mining_Event_Knowledge_Graphs (Chunk 1:218-220)**
  > An event table with entities types additionally designates one or more attributes as names of entity types

---

### 100. LoopCharacteristics Entity Type

LoopCharacteristics is an entity type that captures iteration/repetition specifications for activities. Enables modeling of loops and repeated task execution.

**Sources**:

- **31-BBO_BPMN_Ontology (Chunk 1:234)**
  > Activity class is related to LoopCharacteristics to represent iteration specifications

---

### 101. FlowElementsContainer Entity Type

FlowElementsContainer is a supertype for entities that contain flow elements. Process is its primary subclass. Provides containment semantics for process structure.

**Sources**:

- **31-BBO_BPMN_Ontology (Chunk 1:220)**
  > Process is a sub-class of FlowElementsContainer. Describing a process consists in defining the FlowElements that compose it

---

### 102. BBO Entity Count - 106 Classes

BBO contains 106 ontology classes (entity types), 125 non-inheritance relationships, and 83 isA (inheritance) relationships. The relationship diversity (0.60) indicates rich semantic connections beyond taxonomy.

**Sources**:

- **31-BBO_BPMN_Ontology (Chunk 1:471-473)**
  > Concepts: 106, Relationships others than isA: 125, isA relations: 83, Metrics: RD = 125/(125+83) = 0.60, SD = 83/106 = 0.78

---

### 103. Five Main Concept Categories

BBO identifies five main entity categories from specification analysis: Process (activities), Input/Output Specifications (data flow), Agent (performers), Work Product (outputs), Manufacturing Facility (locations). Maps partially to 8-entity hypothesis.

**Sources**:

- **31-BBO_BPMN_Ontology (Chunk 1:183-196)**
  > we have identified five main concepts that must be covered by BBO ontology: Process, Input/output specifications, Agent, Work product, Manufacturing facility

---

### 104. GlobalTask Entity Type

GlobalTask is an entity type representing reusable task definitions that can be called from multiple processes via CallActivity. Enables task reuse patterns.

**Sources**:

- **31-BBO_BPMN_Ontology (Chunk 1:232-233)**
  > CallActivity: an activity that calls a CallableElement that may be a GlobalTask (i.e., a reusable task) or Sub-Process

---

### 105. SubProcess Subtypes

SubProcess has a subtype EventBasedSubProcess for processes triggered by events. Combined with AdHocSubProcess (mentioned in constraints), provides flexible subprocess modeling.

**Sources**:

- **31-BBO_BPMN_Ontology (Chunk 1:260)**
  > SubProcess: EventBasedSubProcess

---

### 106. ObjectKind as Substantial Universal

UFO defines ObjectKind as a category for substantial universals - types that provide identity criteria for their instances. Flower exemplifies an ObjectKind, meaning instances (individual flowers) have essential properties derived from being flowers.

**Sources**:

- **01-UFO (Chunk 3:29)**
  > ObjectKind(Flower)

---

### 107. SubKind Specialization Pattern

SubKind represents a specialization of an ObjectKind that inherits identity criteria from its parent. Rose is a SubKind of Flower, demonstrating hierarchical entity type organization where subkinds do not add new identity criteria but specialize existing ones.

**Sources**:

- **01-UFO (Chunk 3:32-34)**
  > SubKind(Rose) Rose ⊑ Flower

---

### 108. Quality as Dependent Entity Type

Quality is an entity type representing measurable/perceivable properties that inhere in bearers. FlowerColor is a quality type that characterizes Flower, demonstrating the dependent nature of qualities - they cannot exist without their bearers.

**Sources**:

- **01-UFO (Chunk 3:37-51)**
  > SubKind(Color) SubKind(FlowerColor) FlowerColor ⊑ Color... characterization(Flower, FlowerColor)

---

### 109. QualityStructure Value Space

QualityStructure defines the value space (domain) for quality types. FlowerColorValues is a non-empty set of possible values (Red, Yellow, Brown, White) that FlowerColor qualities can take, grounding abstract qualities in concrete value domains.

**Sources**:

- **01-UFO (Chunk 3:45-72)**
  > QualityStructure(FlowerColorValues)... Red ∈ FlowerColorValues ∧ Yellow ∈ FlowerColorValues

---

### 110. Role as Anti-Rigid Entity Type

Role is an anti-rigid entity type - entities can gain or lose role membership while maintaining identity. Jogger is a role played by Person when bearing a Jog mode. Roles are relationally dependent on contexts (here, the jogging activity).

**Sources**:

- **01-UFO (Chunk 3:129-135)**
  > Role(Jogger) Jogger ⊑ Person

---

### 111. ModeKind as Intrinsic Moment

ModeKind represents intrinsic moments (non-quality intrinsic properties) that characterize entities. Jog is a ModeKind comprising intentions and capacities that inhere in the Jogger, representing the internal state enabling jogging behavior.

**Sources**:

- **01-UFO (Chunk 3:141-149)**
  > ModeKind(Jog) characterization(Jogger, Jog)

---

### 112. EventType as Perdurant Category

EventType categorizes perdurants (entities that unfold in time). JoggingProcess and JoggingEvent are event types where events are manifestations of dispositions (modes). Events are modally fragile - they cannot change properties once occurred.

**Sources**:

- **01-UFO (Chunk 3:154-158)**
  > EventType(JoggingProcess) EventType(JoggingEvent)

---

### 113. Process as Cumulative Manifestation

Process is an event type representing the cumulative aggregation of event manifestations. JoggingProcess is constituted by the sum of JoggingEvents that manifest a Jog mode, with each new event creating a new process as its 'life'.

**Sources**:

- **01-UFO (Chunk 3:161-174)**
  > At each situation, we have a particular type of maximal Jogging Process (termed the life of a Jog)

---

### 114. Stative vs Dynamic Event Partition

Events partition into stative (homeomerous, uniform) and dynamic (sequences of changes) subtypes. JogState is stative while JoggingLocomotion (with WalkWhileJogging, RunWhileJogging subtypes) is dynamic, capturing temporal structure of activities.

**Sources**:

- **01-UFO (Chunk 3:186-203)**
  > Jogging Events can be stative/homeomerous and some are dynamic/sequences of changes

---

### 115. Walker Role with External Dependence

Walker demonstrates a role characterized by an externally dependent mode (Walk). The Walk mode inheres in Walker but is externally dependent on Place (destination), showing how roles connect endurants to broader situational contexts.

**Sources**:

- **01-UFO (Chunk 3:272-285)**
  > Role(Walker) Walker ⊑ Person... ModeKind(Walk) characterization(Walk, Walker)

---

### 116. Place and Destination Role Hierarchy

Place is an ObjectKind with Destination as a dependent role. OriginallyIntendedDestination specializes Destination, showing layered role types where objects acquire roles through relationships with intentional entities (Walk modes).

**Sources**:

- **01-UFO (Chunk 3:299-311)**
  > ObjectKind(Place) Role(Destination) Role(OriginallyIntendedDestination) Destination ⊑ Place

---

### 117. Phase Partition of Modes

Phases partition entity types based on intrinsic properties. Walk partitions into OngoingWalk and FinalizedWalk phases, where FinalizedWalk further partitions into SuccessfulWalk and RedirectedWalk based on arrival outcomes.

**Sources**:

- **01-UFO (Chunk 3:317-328)**
  > isPartitionedInto(Walk, OngoingWalk, FinalizedWalk)

---

### 118. RelatorKind for Material Relations

RelatorKind represents entities that mediate material relations between other entities. ConjugalRelationship is a relator mediating between Spouses, demonstrating how UFO grounds n-ary relations through reified relational entities.

**Sources**:

- **01-UFO (Chunk 3:439-456)**
  > RelatorKind(ConjugalRelationship)... ∀x (x :: Spouse → ∃y (y :: ConjugalRelationship ∧ mediates(y,x))

---

### 119. Higher-Order Types (Powertypes)

Higher-order types have types as instances (powertype pattern). ConjugalRelationshipType categorizes first-order types like MonogamousHeterosexualMarriage, enabling concept evolution where invariant structures accommodate type-level change.

**Sources**:

- **01-UFO (Chunk 3:419-429)**
  > types whose instances are themselves types... categorizes(ConjugalRelationshipType, ConjugalRelationship)

---

### 120. SpouseType as Second-Order Role

SpouseType is a second-order type categorizing first-order spouse roles (Husband, Wife, Partner). This multi-level structure allows flexible modeling where specific conjugal relationships determine compatible spouse types.

**Sources**:

- **01-UFO (Chunk 3:445-462)**
  > categorizes(SpouseType, Spouse)... Husband :: SpouseType Wife :: SpouseType

---

### 121. Entity as Knowledge Graph Node

Entity is the fundamental node type in knowledge graphs - real-world things of interest. The definition emphasizes entities as semantic anchors connected by typed relations, distinguishing KG nodes from abstract graph nodes.

**Sources**:

- **02-KG (Chunk 1:140-142)**
  > whose nodes represent entities of interest and whose edges represent relations between these entities

---

### 122. Class as Entity Grouping

Class is a semantic schema entity type defining groupings of similar entities. Classes like Event and City organize nodes, with subclasses (Open Market, Food Market) creating hierarchies that enable type-based reasoning and querying.

**Sources**:

- **02-KG (Chunk 1:106-118)**
  > define classes to denote these groupings, such as Event, City, etc... Open Market, Food Market, Drinks Festival

---

### 123. Property as Typed Edge Label

Property is the entity type for edge labels in knowledge graphs. Properties form hierarchies (city, venue as sub-properties of location), with domain/range constraints linking them to classes and enabling semantic inference.

**Sources**:

- **02-KG (Chunk 1:120-127)**
  > define the semantics of edge labels, aka properties... city and venue are sub-properties of a more general property location

---

### 124. Directed Edge-Labelled Graph Node Types

The directed edge-labelled graph model defines nodes and edges as basic entity types. Nodes represent entities (Santiago, Arica, events), edges represent relations between entities, forming the structural foundation of knowledge graphs.

**Sources**:

- **02-KG (Chunk 1:404-419)**
  > A directed edge-labelled graph... is defined as a set of nodes... and a set of directed labelled edges

---

### 125. IRI as Entity Identifier Type

IRI (Internationalized Resource Identifier) is a special node type for globally unique entity identification. IRIs enable distributed knowledge graphs where entities can be unambiguously referenced across web-scale data integration.

**Sources**:

- **02-KG (Chunk 1:437-442)**
  > Internationalized Resource Identifiers (IRIs) which allow for global identification of entities on the Web

---

### 126. Literal as Datatype Value Node

Literal is a node type for datatype values (strings, dates, numbers) in RDF graphs. Literals are terminal nodes that cannot have outgoing edges, representing the leaf values that ground entity descriptions in concrete data.

**Sources**:

- **02-KG (Chunk 1:474-475)**
  > literals, which allow for representing strings (with or without language tags) and other datatype values

---

### 127. Blank Node as Existential Entity

Blank node is an entity type for anonymous, existentially quantified entities. Blank nodes represent entities known to exist but not identified, enabling modeling of incomplete knowledge where relationships exist but targets are unknown.

**Sources**:

- **02-KG (Chunk 1:476-478)**
  > blank nodes, which are anonymous nodes that are not assigned an identifier

---

### 128. Heterogeneous Graph with Typed Nodes

Heterogeneous graphs explicitly type nodes as part of the data model (not as special relations). This enables partitioning entities by type for machine learning while typically restricting nodes to single-type membership.

**Sources**:

- **02-KG (Chunk 1:483-502)**
  > heterogeneous graph... where each node and edge is assigned one type... type of node forms part of the graph model itself

---

### 129. Property Graph Node with Attributes

Property graph extends the entity model with attributes. Nodes carry property-value pairs (latitude, longitude) and labels (City), combining identity (id), classification (label), and description (properties) in a unified entity structure.

**Sources**:

- **02-KG (Chunk 1:505-561)**
  > property graph allows a set of property-value pairs and a label to be associated with both nodes and edges

---

### 130. Named Graph as Container Entity

Named graph is a meta-entity type - graphs as first-class entities with identifiers. Named graphs enable provenance tracking, access control, and contextual grouping of edges, treating collections of statements as unified entities.

**Sources**:

- **02-KG (Chunk 1:575-611)**
  > graph dataset then consists of a set of named graphs and a default graph. Each named graph is a pair of a graph ID and a graph

---

### 131. Shape as Validation Entity Type

Shape is a schema entity type for validation. Shapes (Event, Place, Venue, City) define constraints on node structure - required properties, cardinalities, value types - enabling declarative data quality specifications.

**Sources**:

- **02-KG (Chunk 2:250-267)**
  > A shape targets a set of nodes in a data graph and specifies constraints on those nodes

---

### 132. Semantic vs Validating Schema Distinction

Two complementary schema entity categories: semantic schemas define meaning and enable inference (subclass hierarchies), while validating schemas define structure and enable validation (shapes with constraints).

**Sources**:

- **02-KG (Chunk 2:246-249)**
  > semantic schemata allow for inferring new graph data, validating schemata allow for validating existing graph data

---

### 133. Quotient Graph as Emergent Schema

Quotient graph is an emergent entity type discovered from data. Partition nodes (event, venue, city) abstract entity groups, with quotient edges preserving structural relationships - a form of schema induction from data.

**Sources**:

- **02-KG (Chunk 2:439-457)**
  > quotient graphs, which partition groups of nodes... according to some equivalence relation while preserving structural properties

---

### 134. Datatype Node with Lexical Form

Datatype entity combines lexical representation with type annotation. '2020-03-29T20:00:00'^^xsd:dateTime shows how datatype nodes encode values with their semantic types, enabling typed operations and comparisons.

**Sources**:

- **02-KG (Chunk 2:714-727)**
  > datatype node is given as a pair (l,d) where l is a lexical string... and d is an IRI denoting the datatype

---

### 135. Existential Node for Incomplete Knowledge

Existential nodes model incomplete knowledge - entities known to exist but not identified. Useful for co-located events with unannounced venues, preserving relationship semantics without requiring full entity specification.

**Sources**:

- **02-KG (Chunk 2:779-810)**
  > existential nodes... we may know that there must exist a particular node in the graph with particular relationships

---

### 136. Temporal Context Entity (Interval)

Temporal interval is a context entity type for scoping truth. Time intervals constrain when edges hold, enabling temporal reasoning about knowledge validity periods and historical state tracking.

**Sources**:

- **02-KG (Chunk 3:107-118)**
  > Temporal RDF allows for annotating edges with time intervals, such as Chile [2006,2010] M. Bachelet

---

### 137. Fuzzy Value as Confidence Entity

Fuzzy value is an entity type for graded truth. Values 0-1 express confidence/degree (0.8 for semi-arid climate), enabling probabilistic knowledge representation beyond binary true/false assertions.

**Sources**:

- **02-KG (Chunk 3:115-118)**
  > Fuzzy RDF allows for annotating edges with a degree of truth such as Santiago 0.8 Semi-Arid

---

### 138. Annotation as Contextual Metadata

Annotation is a domain-independent context entity type. Semi-ring structures (with meet/join operators) generalize temporal, fuzzy, and provenance annotations, enabling unified contextual reasoning across domains.

**Sources**:

- **02-KG (Chunk 3:120-127)**
  > Annotated RDF allows for representing various forms of context modelled as semi-rings

---

### 139. Individual as Assertional Entity

Individual is the OWL entity type for specific instances (Santiago, EID16). Individuals participate in assertions, carry same-as/different-from relationships, and instantiate classes - the ground-level entities of ontologies.

**Sources**:

- **02-KG (Chunk 3:473-489)**
  > individuals (e.g., Santiago, EID16), sometimes distinguished from classes and properties

---

### 140. Domain Graph Entity vs Data Graph Node

Domain graph distinguishes semantic entities (what nodes refer to) from syntactic nodes (graph structure). This interpretation layer maps data terms to real-world entities, enabling semantic reasoning beyond surface syntax.

**Sources**:

- **02-KG (Chunk 3:368-394)**
  > the nodes of the domain graph as entities, and the edges of the domain graph as relations

---

### 141. Model as Satisfying Interpretation

Model is a semantic entity type - interpretations satisfying all graph axioms. Models ground formal semantics, where entailment means all models of premises are models of conclusions, linking syntax to semantic truth.

**Sources**:

- **02-KG (Chunk 3:714-731)**
  > The interpretations that satisfy a graph are called models of the graph

---

### 142. Rule Body and Head as Graph Patterns

Rule components (body, head) are entity types from graph patterns. Rules like '?x type ?c subc. of ?d => ?x type ?d' use pattern matching for deductive inference, bridging graph structure and logical entailment.

**Sources**:

- **02-KG (Chunk 4:21-35)**
  > A rule is composed of a body (if) and a head (then). Both the body and head are given as graph patterns

---

### 143. Concept (Class) in Description Logic

Concept/Class in DL represents categories with formal semantics. City as a concept supports subsumption reasoning (City subclass of Place), unary relations on individuals, and complex class expressions.

**Sources**:

- **02-KG (Chunk 4:149-161)**
  > classes (aka concepts) such as City... class axiom City ⊑ Place states that the former class is a subclass

---

### 144. Role (Property) in Description Logic

Role/Property in DL represents binary relations with formal semantics. flight as a role supports property hierarchies, domain/range constraints, and complex property expressions enabling relational reasoning.

**Sources**:

- **02-KG (Chunk 4:150-162)**
  > properties (aka roles) such as flight... flight ⊑ connectsTo states that the former property is a subproperty

---

### 145. A-Box Individual Assertions

A-Box (Assertional Box) contains individual entity assertions. City(Santiago) and flight(Santiago,Arica) exemplify unary (class membership) and binary (property relation) assertions grounding abstract schemas in specific instances.

**Sources**:

- **02-KG (Chunk 4:152-156)**
  > Assertional axioms can be either unary class relations on individuals... or binary property relations... forming the Assertional Box

---

### 146. T-Box Class Axioms

T-Box (Terminology Box) contains class/concept axioms. Axioms like City ⊑ Place define subsumption relationships forming the conceptual schema layer that governs individual entity classification.

**Sources**:

- **02-KG (Chunk 4:157-161)**
  > defining class axioms (forming the Terminology Box, or T-Box for short)

---

### 147. R-Box Property Axioms

R-Box (Role Box) contains property/role axioms. Axioms like flight ⊑ connectsTo define property subsumption, domain/range, and complex property characteristics governing relational structure.

**Sources**:

- **02-KG (Chunk 4:159-162)**
  > property axioms (forming the Role Box, R-Box)

---

### 148. Knowledge Graph Embedding Entity

Embedding is a numeric entity representation type. Entity embeddings (vectors e) and relation embeddings (vectors r) encode nodes and edges in continuous space, enabling similarity computation and link prediction.

**Sources**:

- **02-KG (Chunk 4:795-803)**
  > entity embedding for each node: a vector with d dimensions that we denote by e; and a relation embedding for each edge label

---

### 149. Entity Embedding in Knowledge Graphs

Entities in knowledge graphs are represented as embeddings (vector representations). Each entity is mapped to a numeric vector that captures its semantic properties. This pattern shows how entity types are fundamental data objects that can be numerically encoded for machine learning tasks.

**Sources**:

- **02-Knowledge_Graphs (Chunk 5:16-18)**
  > Figure 27 provides a toy example of two-dimensional (d = 2) entity and relation embeddings computed by TransE

---

### 150. Node as Entity Representation

Entities are represented as nodes in knowledge graphs. The paper establishes that nodes serve as the fundamental entity representation, with edge labels representing relations between these entity nodes. Source/head and target/tail terminology describes the directional nature of entity relationships.

**Sources**:

- **02-Knowledge_Graphs (Chunk 5:8-12)**
  > Translational models interpret edge labels as transformations from subject nodes (aka the source or head) to object nodes (aka the target or tail)

---

### 151. Entity Vector Representation

Entities are represented by embedding vectors (e_s for subject entity, e_o for object entity). This foundational pattern shows how entity types are encoded as numeric vectors for computational reasoning, where each unique entity gets its own vector representation.

**Sources**:

- **02-Knowledge_Graphs (Chunk 5:13-14)**
  > TransE learns vectors es, rp, and eo aiming to make es + rp as close as possible to eo

---

### 152. Graph Neural Network Node Classification

Entities (nodes) in knowledge graphs can be classified using graph neural networks. GNNs learn to categorize entity types based on their structural properties and relationships within the graph, enabling type prediction for unknown entities.

**Sources**:

- **02-Knowledge_Graphs (Chunk 5:427-439)**
  > A graph neural network (GNN) builds a neural network based on the topology of the data graph...GNNs can be used to classify elements of the graph or the graph itself

---

### 153. Feature Vectors for Nodes

Entities (nodes) carry feature vectors that encode their type information, attributes, and other characteristics. This pattern shows how entity type information is captured as numeric features for machine learning.

**Sources**:

- **02-Knowledge_Graphs (Chunk 5:468-476)**
  > Each node in the graph is also associated with a feature vector that can capture node and edge labels, weights, etc. These feature vectors remain fixed throughout the process

---

### 154. State Vectors for Entity Processing

Entities maintain dynamic state vectors that evolve through iterative message passing with neighboring entities. This captures how entity representations can be refined through relational context.

**Sources**:

- **02-Knowledge_Graphs (Chunk 5:470-474)**
  > Each node in the graph is also associated with a state vector, which is recursively updated based on information from the node's neighbours

---

### 155. Symbolic Learning for Entity Hypotheses

Entity relationships can be learned through symbolic (logical) methods that produce interpretable rules. This pattern contrasts with purely numeric approaches, showing how entity types can be reasoned about symbolically.

**Sources**:

- **02-Knowledge_Graphs (Chunk 5:667-674)**
  > An alternative approach is to adopt symbolic learning in order to learn hypotheses in a symbolic (logical) language that explain a given set of positive and negative edges

---

### 156. Rule Mining for Entity Relations

Entity relationships can be mined as rules from knowledge graphs. This pattern shows how recurring patterns among entity types can be discovered and formalized as logical rules.

**Sources**:

- **02-Knowledge_Graphs (Chunk 5:704-712)**
  > Rule mining, in the general sense, refers to discovering meaningful patterns in the form of rules from large collections of background knowledge

---

### 157. Class/Concept in Axiom Mining

Entity types can be classes with formal semantic relationships (like disjointness). The example shows how DomesticAirport and InternationalAirport are mutually exclusive entity types, demonstrating ontological class relationships.

**Sources**:

- **02-Knowledge_Graphs (Chunk 5:912-924)**
  > Among systems mining specific types of axioms, disjointness axioms are a popular target...the disjointness axiom DomesticAirport ⊓ InternationalAirport ≡⊥

---

### 158. DL Class Description for Entities

Entities can be grouped into learned class descriptions using Description Logic. This pattern shows automated entity type discovery through logical class learning from positive and negative examples.

**Sources**:

- **02-Knowledge_Graphs (Chunk 5:959-968)**
  > DL Learner, which is based on algorithms for class learning (aka concept learning), whereby given a set of positive nodes and negative nodes, the goal is to find a logical class description

---

### 159. Named Entity Recognition Entity Types

Named Entity Recognition (NER) identifies core entity types from text including people, organizations, locations, and other types. These recognized entities become nodes in the knowledge graph.

**Sources**:

- **02-Knowledge_Graphs (Chunk 6:84-86)**
  > Named Entity Santiago Rapa Nui World Heritage Site 1995 Recognition

---

### 160. Entity Linking to Knowledge Graph Nodes

Entity Linking (EL) connects mentions of entities in text to existing nodes in the knowledge graph. This establishes correspondence between textual entity references and formal entity representations.

**Sources**:

- **02-Knowledge_Graphs (Chunk 6:88-89)**
  > Entity Linking: Santiago Easter Island World Heritage Site 1995

---

### 161. Entity with Temporal Context

Entities can participate in n-ary relations that capture temporal context. Anonymous nodes are used to reify events and temporal relationships, creating event-type entities that connect multiple participants.

**Sources**:

- **02-Knowledge_Graphs (Chunk 6:300-304)**
  > an n-ary relation captures additional temporal context, denoting when Rapa Nui was named a World Heritage site; an anonymous node is created to represent the higher-arity relation

---

### 162. Organisation Entity Type

Organisation is a core entity type in knowledge graphs. Organizations are recognized as distinct entities that can have relationships with people, locations, and other entities.

**Sources**:

- **02-Knowledge_Graphs (Chunk 6:205-207)**
  > typically targetting mentions of people, organisations, locations, and potentially other types

---

### 163. Claimant Entity in Relational Data

Claimant represents a person entity type in relational database context. This shows how entity types from structured sources map to knowledge graph nodes with associated properties (id, name, country).

**Sources**:

- **02-Knowledge_Graphs (Chunk 6:484-486)**
  > Claimant id name country XY12SDA John Smith U.S.

---

### 164. Entity in Accuracy Definition

Entities are the core data objects in knowledge graphs, encoded as nodes. This definition establishes entities as representations of real-world phenomena, highlighting their semantic grounding.

**Sources**:

- **02-Knowledge_Graphs (Chunk 7:20-22)**
  > Accuracy refers to the extent to which entities and relations – encoded by nodes and edges in the graph – correctly represent real-life phenomena

---

### 165. Class as Entity Type Schema

Classes define entity types in the schema layer. Schema completeness measures how well entity type definitions (classes) are represented in the actual data graph instances.

**Sources**:

- **02-Knowledge_Graphs (Chunk 7:99-101)**
  > schema completeness refers to the degree to which the classes and properties of a schema are represented in the data graph

---

### 166. Instance as Entity Exemplar

Instances are individual entities of a particular type. Population completeness measures coverage of entity instances, showing the distinction between entity types (classes) and their instances.

**Sources**:

- **02-Knowledge_Graphs (Chunk 7:105-107)**
  > population completeness provides the percentage of all real-world entities of a particular type that are represented in the datasets

---

### 167. Schema Element Types

Entity types are defined at the schema level as classes. The schema contains properties, classes, and shapes that define the structure of entity types and their relationships.

**Sources**:

- **02-Knowledge_Graphs (Chunk 7:204-208)**
  > intensional conciseness (schema level), which refers to the case when the data does not contain redundant schema elements (properties, classes, shapes, etc.)

---

### 168. Agent in Knowledge Graph Usage

Agent appears as a user/consumer of knowledge graphs. Agents interact with knowledge graphs through various access protocols, representing autonomous actors that process graph data.

**Sources**:

- **02-Knowledge_Graphs (Chunk 8:16-20)**
  > dumps are only suited to certain use-cases, in particular for agents that wish to maintain a full local copy of a knowledge graph

---

### 169. Food Festival Entity Type

Food Festival is a specific event entity type. This example shows how entity types (Food Festival) are queried through graph patterns with type constraints and location relationships.

**Sources**:

- **02-Knowledge_Graphs (Chunk 8:44-46)**
  > to find all food festivals in Santiago – represented by the graph pattern Food Festival type ?ff location Santiago

---

### 170. Event Entity with Type Classification

Events are entity types that can be classified (typed). The type relationship connects entity instances to their class definitions, enabling entity classification queries.

**Sources**:

- **02-Knowledge_Graphs (Chunk 8:68)**
  > of edge patterns are ?ff type Food Festival or ?ff location Santiago, etc., where any term can be a variable or a constant

---

### 171. EventGraph as Named Entity Collection

EventGraph represents a collection of event entities. Named graphs can organize entities by type, with EventGraph containing event-type entities as a coherent data unit.

**Sources**:

- **02-Knowledge_Graphs (Chunk 8:196-198)**
  > the permission to Modify, Distribute, and Derive work from the EventGraph

---

### 172. LocationGraph Entity Set

LocationGraph is a named graph containing location entities. This pattern shows entity type organization into named graphs for usage policy enforcement.

**Sources**:

- **02-Knowledge_Graphs (Chunk 8:261)**
  > states that the process Analyse of LocationGraph can be performed on InternalServers

---

### 173. Goal as Entity Type in Plan Graphs

Goal is an entity type in planning knowledge graphs. Goals are nodes representing objectives with dependency relationships, showing intentional entities in knowledge representations.

**Sources**:

- **02-Knowledge_Graphs (Chunk 13:5-9)**
  > Jiang and Ma (2002) introduce the notion of 'plan knowledge graphs' where nodes represent goals and edges dependencies between goals

---

### 174. Knowledge Actor Entity Type

Knowledge Actor is an entity type representing agents in knowledge flow. Subtypes include creators, sharers, and users - roles that entities can play in knowledge processes.

**Sources**:

- **02-Knowledge_Graphs (Chunk 13:11-17)**
  > Helms and Buijsrogge (2005) propose a knowledge graph to represent the flow of knowledge...with nodes representing knowledge actors (creators, sharers, users)

---

### 175. Event as Causal Node

Event is an entity type representing occurrences with causal relationships. Events are connected through causal edges, creating explanation graphs for reasoning about why things happen.

**Sources**:

- **02-Knowledge_Graphs (Chunk 13:38-42)**
  > Pechsiri and Piriyakul (2010) use knowledge graphs to capture 'explanation knowledge'...by representing events as nodes and causal relationships as edges

---

### 176. Wikipedia Article/Category as Entity

Wikipedia Articles and Categories serve as entity types. Articles represent specific entity instances while categories represent entity type classifications in encyclopedic knowledge graphs.

**Sources**:

- **02-Knowledge_Graphs (Chunk 13:29-35)**
  > Coursey and Mihalcea (2009) construct a knowledge graph from Wikipedia, where nodes represent Wikipedia articles and categories

---

### 177. Entity in Modern KG Definition

Entity is the fundamental ontological unit in knowledge graphs. This definition establishes entities as nodes representing things of interest, with edges capturing relationships between entities.

**Sources**:

- **02-Knowledge_Graphs (Chunk 13:60-62)**
  > all of the works of this period consider a knowledge graph to be formed of a set of nodes denoting entities of interest and a set of edges denoting relations between those entities

---

### 178. Real-World Entity Representation

Real-world entities are the core subjects of knowledge graphs. Google's influential definition emphasizes that nodes represent actual things in the world, not abstract concepts.

**Sources**:

- **02-Knowledge_Graphs (Chunk 13:108-110)**
  > Google Knowledge Graph...described as '[a graph] that understands real-world entities and their relationships to one another'

---

### 179. DBpedia Entity Types (Person, Place, etc.)

Entity types are defined in schemas as possible classes. Real-world entities are organized into classes (like Person, Place, Organisation) with defined relations between them.

**Sources**:

- **02-Knowledge_Graphs (Chunk 13:178-180)**
  > a knowledge graph 'mainly describes real world entities and their interrelations, organized in a graph; defines possible classes and relations of entities in a schema'

---

### 180. Event Entity with Shape Validation

Event, Venue, and Place are entity types with shape constraints. Shape maps validate that entity instances conform to their type definitions, showing formal entity type validation.

**Sources**:

- **02-Knowledge_Graphs (Chunk 14:10-12)**
  > a shapes map where σ(EID15, Event) = 1, σ(Santa Lucía, Venue) = 1, σ(Santa Lucía, Place) = 1

---

### 181. Individual as DL Entity

Individual is the Description Logic term for entity instance. Individuals are elements of the interpretation domain, representing specific entities as opposed to classes (entity types).

**Sources**:

- **02-Knowledge_Graphs (Chunk 14:354-359)**
  > The interpretation function accepts a definition of either an individual a, a class C, or a relation R, mapping them, respectively, to an element of the domain

---

### 182. DL Class as Entity Type

Class in Description Logics represents entity type. Classes are interpreted as subsets of the domain, with individuals belonging to zero or more classes, defining entity type membership.

**Sources**:

- **02-Knowledge_Graphs (Chunk 14:357-358)**
  > a class C...a subset of the domain (C^I ⊆ Δ^I)

---

### 183. Airport Entity Type

Merged from 3 sources. Airport is an entity type with formal ontological relationships. The axiom states that entities with flight relationships must be near an Airport, showing how entity types have logical constraints.

**Sources**:

- **02-Knowledge_Graphs (Chunk 14:369-371)**
  > T := {City ⊑ Place, ∃flight.⊤ ⊑ ∃nearby.Airport}

- **18-Multi-Agent_Taxonomy (Chunk 1:874-875)**
  > systems might feature a Library, a repository storing best practices, lessons learned, or reusable knowledge, such as Prompt Templates or specific information like API credentials

- **18-Multi-Agent_Taxonomy (Chunk 1:889-891)**
  > Within each Task-Management Activity, a set of intelligent Agents collaborate, forming a multi-agent Network

---

### 184. City Entity Type with Subsumption

City is an entity type that is a subclass of Place. Arica and Santiago are instances (individuals) of the City type, demonstrating entity type hierarchy and instantiation.

**Sources**:

- **02-Knowledge_Graphs (Chunk 14:368-370)**
  > A := {City(Arica), City(Santiago), flight(Arica,Santiago)}; T := {City ⊑ Place}

---

### 185. Node as Entity in Graph Neural Networks

Graph neural networks operate on nodes as fundamental entity types within directed vector-labelled graphs. Nodes serve as the primary entities that receive feature vectors and participate in aggregation functions.

**Sources**:

- **02-Knowledge_Graphs (Chunk 15:378-382)**
  > We now provide high-level definitions for graph neural networks (GNNs)... We assume that the GNN accepts a directed vector-labelled graph as input

---

### 186. Edge as Relationship Entity

Edges represent relationships between entities in knowledge graphs. The distinction between positive edges (true relationships) and negative edges (false/unknown relationships) is fundamental to hypothesis mining and graph completion.

**Sources**:

- **02-Knowledge_Graphs (Chunk 15:539-542)**
  > a set of positive edges E+ such that G does not entail any edge in E+... and a set of negative edges E-

---

### 187. Hypothesis Entity in Symbolic Learning

Hypotheses are treated as entities that can be induced from background knowledge. They represent potential relationships or rules that can explain observed data patterns.

**Sources**:

- **02-Knowledge_Graphs (Chunk 15:536-538)**
  > We first abstractly define a recursive graph neural network... The task of hypothesis induction assumes a particular graph entailment relation

---

### 188. Agent (W3C PROV Core)

Agent is one of three core entity types in W3C PROV, representing either software or human actors responsible for activities. This forms the foundational triad: Agent-Activity-Entity.

**Sources**:

- **03-PROV-AGENT (Chunk 1:200-204)**
  > the W3C PROV standard already defines Agent, the central abstraction in this work, as one of its three core classes, alongside Entity (data) and Activity (process)

---

### 189. Entity (W3C PROV Core)

Entity in PROV represents data or things that are used or produced by activities. It is one of the three core classes forming the provenance triad.

**Sources**:

- **03-PROV-AGENT (Chunk 1:201-202)**
  > alongside Entity (data) and Activity (process), with agents representing either software or human actors responsible for activities

---

### 190. Activity (W3C PROV Core)

Activity represents processes or actions in the PROV model. Activities consume entities as inputs and produce entities as outputs, with agents responsible for their execution.

**Sources**:

- **03-PROV-AGENT (Chunk 1:201-202)**
  > alongside Entity (data) and Activity (process)

---

### 191. AIAgent (PROV-AGENT Extension)

AIAgent is a specialized subclass of PROV Agent designed for AI/LLM-based agents in agentic workflows. It captures agent-specific metadata like tools, prompts, and reasoning paths.

**Sources**:

- **03-PROV-AGENT (Chunk 1:278-284)**
  > We extend the abstract W3C PROV Agent by modeling AIAgent as its subclass, enabling a natural integration of agent actions and interactions into the broader workflow provenance graph

---

### 192. AgentTool (MCP Concept)

AgentTool represents tool executions performed by AI agents, following Model Context Protocol (MCP) terminology. It links agent activities to specific tool invocations.

**Sources**:

- **03-PROV-AGENT (Chunk 1:285-287)**
  > Following the MCP terminology, an AI agent can be associated with one or many tool executions (AgentTool) and each tool may be informed by one or many AIModelInvocations

---

### 193. AIModelInvocation

AIModelInvocation represents individual calls to AI/LLM models, capturing the prompt used, model metadata (name, type, provider, temperature), and response generated.

**Sources**:

- **03-PROV-AGENT (Chunk 1:287-291)**
  > each tool may be informed by (PROV wasInformedBy) one or many AIModelInvocations. Each AIModelInvocation uses a Prompt and a specific AIModel

---

### 194. AIModel

AIModel entity holds metadata about the AI/LLM model being invoked, including name, type, provider, and configuration parameters like temperature.

**Sources**:

- **03-PROV-AGENT (Chunk 1:289-291)**
  > AIModel, which holds model metadata, including its name, type, provider, temperature, and other parameters

---

### 195. Prompt

Prompt is an entity type representing input prompts sent to AI models. It is consumed by AIModelInvocation activities.

**Sources**:

- **03-PROV-AGENT (Chunk 1:288)**
  > Each AIModelInvocation uses a Prompt and a specific AIModel

---

### 196. ResponseData

ResponseData represents the output generated by AI model invocations. It is attributed to the agent that initiated the invocation.

**Sources**:

- **03-PROV-AGENT (Chunk 1:290-292)**
  > generates a ResponseData object, which is attributedTo the corresponding agent

---

### 197. DomainData

DomainData represents domain-specific data objects that are consumed and produced by workflow tasks, including parameters, arguments, KPIs, and pointers to data files.

**Sources**:

- **03-PROV-AGENT (Chunk 1:265-266)**
  > Tasks consume (PROV used) and produce (PROV generated) domain-specific data objects (DomainData)

---

### 198. SchedulingData

SchedulingData captures infrastructure-level context about where tasks executed, including compute node, CPU core, and GPU identifiers.

**Sources**:

- **03-PROV-AGENT (Chunk 1:271-273)**
  > SchedulingData contains where the task ran, including details such as compute node, CPU core, or GPU ID

---

### 199. TelemetryData

TelemetryData captures runtime performance metrics including CPU usage, GPU usage, and disk usage for workflow monitoring and analysis.

**Sources**:

- **03-PROV-AGENT (Chunk 1:273-274)**
  > TelemetryData contains runtime metrics such as CPU and GPU usage, and disk usage

---

### 200. Task (Workflow Entity)

Task is a subclass of PROV Activity representing individual workflow tasks that consume and produce data objects.

**Sources**:

- **03-PROV-AGENT (Chunk 1:263-264)**
  > At its core, the model includes standard workflow structures such as Campaign, Workflow, and Task, modeled as subclasses of PROV Activities

---

### 201. Campaign

Campaign represents a high-level organizational structure for workflows, associated with persons or organizations via wasAssociatedWith.

**Sources**:

- **03-PROV-AGENT (Chunk 1:263-264)**
  > At its core, the model includes standard workflow structures such as Campaign, Workflow, and Task

---

### 202. Workflow

Workflow represents the overall workflow structure as a PROV Activity subclass, containing tasks and agent interactions.

**Sources**:

- **03-PROV-AGENT (Chunk 1:263-264)**
  > standard workflow structures such as Campaign, Workflow, and Task, modeled as subclasses of PROV Activities

---

### 203. BFO Continuant

BFO continuant is the category of entities that persist through time with all their parts present at any given moment. PROV Entity maps as subclass of continuant (excluding spatial regions).

**Sources**:

- **04-PROV-O_to_BFO (Chunk 1:636-637)**
  > PROV Entity is mapped to a subclass of things that are independent continuants and not spatial regions, in a union with generically dependent and specifically dependent continuants in BFO

---

### 204. BFO Occurrent (Process)

BFO process (occurrent) represents entities that unfold over time. PROV Activity is mapped as equivalent to BFO process, establishing fundamental alignment between the ontologies.

**Sources**:

- **04-PROV-O_to_BFO (Chunk 1:682-687)**
  > PROV Activity is mapped as equivalent to the class BFO process. The definition of PROV Activity includes 'something that occurs over a period of time and acts upon or with entities'

---

### 205. BFO Material Entity

BFO material entity is a type of independent continuant with matter as a part. PROV Agent maps as a subclass of material entities that participate in activities and bear roles.

**Sources**:

- **04-PROV-O_to_BFO (Chunk 1:654-655)**
  > PROV Agent is mapped as a subclass of BFO material entities that both participate in some PROV Activity and bear some BFO role that is realized in a PROV Activity

---

### 206. BFO Role

BFO role is a realizable entity that can be gained or lost by its bearer without physical change. PROV Role maps as subclass of BFO role.

**Sources**:

- **04-PROV-O_to_BFO (Chunk 1:655-656)**
  > PROV Agent... bear some BFO role that is realized in a PROV Activity

---

### 207. BFO Process Boundary

Merged from 2 sources. Process boundaries are instantaneous occurrents that mark beginnings and endings of processes. They span temporal instants rather than intervals, distinguishing them from temporally extended processes.

**Sources**:

- **04-PROV-O_to_BFO (Chunk 1:913-915)**
  > PROV InstantaneousEvent, which is equivalently mapped to BFO process boundary since instances of PROV InstantaneousEvent are indivisible boundaries of some PROV Activity

- **07-Classifying_Processes_Barry_Smith (Chunk 1:548-552)**
  > BFO's treatment of occurrents, which include processes, process boundaries (for example beginnings and endings), spatiotemporal regions, and temporal intervals

---

### 208. BFO Generically Dependent Continuant

Merged from 2 sources. Generically dependent continuants are entities like information artifacts that can be transferred through exact copying. They contrast with specifically dependent entities (like temperature) that cannot migrate from one bearer to another.

**Sources**:

- **04-PROV-O_to_BFO (Chunk 1:801-802)**
  > PROV Bundle... We therefore map it as a subclass of CCO Information Content Entity and also BFO generically dependent continuant

- **07-Classifying_Processes_Barry_Smith (Chunk 1:625-632)**
  > the BFO:generically dependent continuant expression: '1.7 m tall'. It is an information artifact. It can be stored, for instance, as a record

---

### 209. BFO Site

BFO site represents three-dimensional immaterial regions bounded by material entities. PROV Location maps equivalently to BFO site.

**Sources**:

- **04-PROV-O_to_BFO (Chunk 1:808-811)**
  > PROV Location is mapped as equivalent to BFO site, which is defined as 'a three-dimensional immaterial entity whose boundaries either coincide with the boundaries of material entities'

---

### 210. PROV Influence

PROV Influence represents the capacity of an entity, activity, or agent to affect another. It maps to either BFO process or process boundary depending on whether it spans time or is instantaneous.

**Sources**:

- **04-PROV-O_to_BFO (Chunk 1:911-913)**
  > PROV Influence, as the superclass of 16 Qualified Influence classes, is mapped to a subclass of the disjoint union of BFO process and BFO process boundary

---

### 211. PROV Generation

PROV Generation represents the instantaneous event of entity creation. As a subclass of InstantaneousEvent, it maps to BFO process boundary.

**Sources**:

- **04-PROV-O_to_BFO (Chunk 1:913)**
  > Some of its subclasses such as PROV Generation, PROV Start, and PROV End are subsumed under PROV InstantaneousEvent

---

### 212. PROV Start/End

PROV Start and End represent the beginning and ending boundaries of activities. They map equivalently to CCO process beginning and ending.

**Sources**:

- **04-PROV-O_to_BFO (Chunk 2:93-100)**
  > PROV Start is equivalently mapped to CCO process beginning, while PROV End is equivalently mapped to CCO process ending

---

### 213. PROV Plan

PROV Plan represents information about intended actions or steps. It maps to CCO Information Content Entity (subclass of BFO generically dependent continuant).

**Sources**:

- **04-PROV-O_to_BFO (Chunk 2:116-124)**
  > The case of PROV Plan is more complicated. It is mapped to a subclass of CCO Information Content Entity... A PROV Plan is clearly about some entity since it 'represents a set of actions or steps intended by one or more agents'

---

### 214. CCO Agent

CCO Agent is a mid-level ontology class representing agents. PROV Agent maps equivalently to the intersection of CCO Agent and participation in PROV Activity.

**Sources**:

- **04-PROV-O_to_BFO (Chunk 1:676-679)**
  > A PROV Agent is equivalent to the intersection of CCO agents that are a CCO agent in some PROV Activity

---

### 215. CCO Information Content Entity

CCO Information Content Entity represents information that can exist in multiple bearers. PROV Plan and PROV Bundle map as subclasses.

**Sources**:

- **04-PROV-O_to_BFO (Chunk 2:117-118)**
  > It is mapped to a subclass of CCO Information Content Entity. According to CCO, an Information Content Entity is a BFO generically dependent continuant

---

### 216. Endurant (Continuant)

Endurant (also called continuant) is a DOLCE basic category for entities wholly present at any time they exist. Examples include tables, persons, cats, planets.

**Sources**:

- **05-DOLCE (Chunk 1:121-122)**
  > As depicted in the taxonomy in Figure 1, the basic categories of DOLCE are endurant (aka continuant), perdurant (occurrent), quality, and abstract

---

### 217. Perdurant (Occurrent)

Perdurant (occurrent) in DOLCE represents entities that unfold in time and can be partially present. Examples include tennis matches, conference talks, manufacturing processes.

**Sources**:

- **05-DOLCE (Chunk 1:128-133)**
  > perdurants are fixed in time. Their fundamental difference concerns therefore their presence in time: endurants are wholly present at any time in which they are present; differently, perdurants can be partially present

---

### 218. Quality (DOLCE)

Quality in DOLCE represents perceivable and measurable properties that inhere in endurants or perdurants. They are specific to their bearers (individual qualities).

**Sources**:

- **05-DOLCE (Chunk 1:166-176)**
  > Qualities are, roughly speaking, what can be perceived and measured; they are particulars inhering in endurants or perdurants. For example, when we talk about the red of a rose, we are talking about a particular quality

---

### 219. Abstract (DOLCE)

Abstract in DOLCE represents entities without spatial or temporal qualities. Examples include quality regions, quality spaces, sets, and facts.

**Sources**:

- **05-DOLCE (Chunk 1:216-219)**
  > abstracts. These are entities that have neither spatial nor temporal qualities and are not qualities themselves. We will not deal with them in the current paper, so it should suffice to give a few examples: quality regions (and therefore also quality spaces), sets, and facts

---

### 220. Physical Object

Physical object in DOLCE is an independent endurant that can bear features and qualities. It serves as the bearer for dependent entities.

**Sources**:

- **05-DOLCE (Chunk 1:149-153)**
  > features (e.g., edges, holes, bumps, etc.) are endurants whose existence depends on some physical object (the feature bearer), while physical objects are independent entities

---

### 221. Role (DOLCE)

Role in DOLCE is a concept that is anti-rigid (can be gained/lost without physical change) and founded (depends on external context). Examples: teacher, student roles.

**Sources**:

- **05-DOLCE (Chunk 1:184-189)**
  > Roles are represented as (social) concepts, which are connected to other entities by the relation of classification. In particular, roles are concepts that are anti-rigid and founded

---

### 222. Concept (DOLCE)

Concept in DOLCE represents entities that classify other entities. Roles are a subcategory of Concept with specific anti-rigidity and foundedness properties.

**Sources**:

- **05-DOLCE (Chunk 1:405-408)**
  > the relation of classification (CF)... applies to the category Concept (C), and to its subcategories including Role (RL), which informally collects particulars that classify

---

### 223. Artefact

Artefact in DOLCE represents intentionally produced entities. They are a specialization of physical object with distinct persistence conditions based on function and design.

**Sources**:

- **05-DOLCE (Chunk 1:453-456)**
  > The first option, which we call artifact-based... considers entities like tables and legs as ontological entities on their own because of their artifactual status, namely, the fact that tables and the legs are intentionally produced products

---

### 224. Process (DOLCE)

Process in DOLCE is a stative perdurant that is cumulative (sum of two processes is a process) but not homeomeric (has parts of different types).

**Sources**:

- **05-DOLCE (Chunk 1:156-163)**
  > a perdurant(-type) is stative or eventive according to whether it holds of the mereological sum of two of its instances... Among stative perdurants, processes are cumulative but not homeomeric

---

### 225. Event (Achievement/Accomplishment)

Event in DOLCE is an eventive (non-cumulative) perdurant. Achievements are atomic events; accomplishments are non-atomic events.

**Sources**:

- **05-DOLCE (Chunk 1:162-163)**
  > eventive occurrences (events) are not cumulative, and they are called achievements if they are atomic, otherwise they are accomplishments

---

### 226. Quale

Quale in DOLCE represents the position of a quality within a quality space, enabling comparison of qualities of the same kind across different bearers.

**Sources**:

- **05-DOLCE (Chunk 1:177-181)**
  > A quale is the position occupied by an individual quality within a quality space. In our example, if the rose and the book cover exhibit the same shade of red, their individual colors occupy the same position (quale)

---

### 227. Matter

Matter in DOLCE represents quantities of material substance. It is distinguished from the object constituted by the matter and the artifact functional role.

**Sources**:

- **05-DOLCE (Chunk 1:483-485)**
  > DOLCE allows distinguishing between quantities of matter (e.g., the wood of which a table is made), the object constituted by the matter (that object made of that wood), and the artifact

---

### 228. Person (Agentive Physical Object)

Person in DOLCE is a specialization of Agentive Physical Object (APO). Persons can bear roles like teacher, student, etc.

**Sources**:

- **05-DOLCE (Chunk 1:751-752)**
  > we need four instances of Person, namely Mr. Potter, Mrs. Bumblebee, Mary, and John, as well as two instances of Object

---

### 229. Continuant (BFO)

BFO continuant represents entities that persist through time. Major subtypes include independent continuants (objects), dependent continuants (qualities, realizable entities), and spatial regions.

**Sources**:

- **06-BFO_Function_Role (Chunk 1:54-57)**
  > BFO adopts a view of reality as comprising (1) continuants, entities that continue or persist through time, such as objects, qualities, and functions

---

### 230. Occurrent (BFO)

BFO occurrent represents events or happenings in which continuants participate. Subtypes include processes, process boundaries, and temporal/spatiotemporal regions.

**Sources**:

- **06-BFO_Function_Role (Chunk 1:55-56)**
  > (2) occurrents, the events or happenings in which continuants participate

---

### 231. Independent Continuant

Independent continuant in BFO represents entities that can exist on their own as bearers of dependent continuants. Examples include material objects, sites, and object boundaries.

**Sources**:

- **06-BFO_Function_Role (Chunk 1:175-177)**
  > The principle examples of independent continuants are the objects we see around us every day. These serve as the bearers or carriers of dependent continuants

---

### 232. Dependent Continuant

Dependent continuant in BFO requires another entity (bearer) to exist. Includes qualities (like color, mass) and realizable entities (roles, dispositions, functions).

**Sources**:

- **06-BFO_Function_Role (Chunk 1:186-191)**
  > Dependent continuants are related to their bearers by inherence... dependent continuants, such as qualities, functions, roles, and dispositions can exist only insofar as they are the qualities, functions, roles, and dispositions of specific independent continuants

---

### 233. Realizable Entity

Realizable entity in BFO is a dependent continuant that can be manifested in processes. Subtypes include role, disposition, capability, and function.

**Sources**:

- **06-BFO_Function_Role (Chunk 1:240-243)**
  > A realizable entity is defined as a specifically dependent continuant that has an independent continuant entity as its bearer, and whose instances can be realized (manifested, actualized, executed) in associated processes

---

### 234. Role (BFO)

BFO role is an externally-grounded realizable entity. It depends on external circumstances, not the bearer's physical makeup. Examples: analyte role, drug role, pathogen role.

**Sources**:

- **06-BFO_Function_Role (Chunk 1:268-270)**
  > A role is a realizable entity which exists because the bearer is in some special physical, social, or institutional set of circumstances... and is not such that, if it ceases to exist, then the physical make-up of the bearer is thereby changed

---

### 235. Disposition (BFO)

BFO disposition is an internally-grounded realizable entity based on the bearer's physical makeup. Examples: fragility, solubility, tendency to decay.

**Sources**:

- **06-BFO_Function_Role (Chunk 1:333-334)**
  > A disposition is a realizable entity which is such that, if it ceases to exist, then its bearer is physically changed, and whose realization occurs in virtue of the bearer's physical make-up

---

### 236. Function (BFO)

BFO function is a disposition that exists due to the bearer's physical makeup resulting from evolution (biological) or intentional design (artifactual). Functions are realized in 'functionings'.

**Sources**:

- **06-BFO_Function_Role (Chunk 1:385-388)**
  > A function is a disposition that exists in virtue of the bearer's physical make-up, and this physical make-up is something the bearer possesses because it came into being, either through evolution or through intentional design

---

### 237. Capability (BFO)

Capability in BFO is a type of realizable entity representing what an entity is able to do. It is listed alongside role, disposition, and function in the BFO hierarchy.

**Sources**:

- **06-BFO_Function_Role (Chunk 1:78-82)**
  > realizable entity: role, disposition, capability, function

---

### 238. Artifactual Function

Artifactual function in BFO is a function arising from intentional design. Examples: function of a pycnometer to hold liquid, function of a fan to circulate air.

**Sources**:

- **06-BFO_Function_Role (Chunk 1:434-436)**
  > An artifactual function is a function whose bearer's physical make-up has been designed and made intentionally (typically by one or more human beings) to function in a certain way

---

### 239. Biological Function

Biological function in BFO is a function arising from evolution in organisms. Examples: function of mitochondria to produce ATP, function of heart to pump blood.

**Sources**:

- **06-BFO_Function_Role (Chunk 1:449-451)**
  > A biological function is a function whose bearer is part of an organism, and exists and has the physical make-up it has because it has evolved that way and contributes to the organism's realization of a life plan

---

### 240. Specifically Dependent Continuant

Specifically dependent continuant in BFO cannot migrate between bearers. The redness of this ball cannot become the redness of that ball. Includes qualities and realizable entities.

**Sources**:

- **06-BFO_Function_Role (Chunk 1:189-191)**
  > an instance of a quality such as round or red is termed a specific dependent continuant since it cannot exist except as a quality of a specific independent continuant such as this ball

---

### 241. Generically Dependent Continuant

Generically dependent continuant in BFO can exist in multiple bearers simultaneously. Examples: PDF files, information content, data patterns.

**Sources**:

- **06-BFO_Function_Role (Chunk 1:209-211)**
  > Specifically dependent continuants, such as headaches or talents, cannot migrate from one bearer to another, as contrasted with generically dependent continuants, such as the pdf file on your laptop

---

### 242. BFO Continuant Entity Type

Continuants are entities that are wholly present at any time they exist. They can be sliced along spatial dimensions but not temporal ones. Examples include things (pencils, people), qualities, and dispositions. In BFO, continuants may change from one time to the next by gaining and losing qualities.

**Sources**:

- **07-Classifying_Processes_Barry_Smith (Chunk 1:293-294)**
  > BFO takes as its starting point a familiar distinction between two sets of views, which we can refer to as four-dimensionalist and three-dimensionalist

---

### 243. BFO Occurrent Entity Type

Occurrents are entities that unfold in time and have temporal parts. They include processes, process boundaries (beginnings and endings), spatiotemporal regions, temporal intervals and instants. Occurrents cannot change - they ARE changes in the independent continuant entities which are their participants.

**Sources**:

- **07-Classifying_Processes_Barry_Smith (Chunk 1:299-300)**
  > Four-dimensionalists see reality as consisting exclusively of four-dimensional entities (variously referred to as processes, events, occurrents, perdurants, spacetime-worms)

---

### 244. BFO Independent Continuant

Independent continuants are substances like molecules, organisms, planets - entities that can exist on their own. They serve as bearers for dependent continuants (qualities, dispositions). The BFO ontological square distinguishes independent continuants at both type and instance levels.

**Sources**:

- **07-Classifying_Processes_Barry_Smith (Chunk 1:447-449)**
  > In allowing not only things but also entities that are dependent on things as continuants, BFO draws on Aristotle's ideas concerning the division of substances and accidents

---

### 245. BFO Dependent Continuant

Dependent continuants include qualities and dispositions (like solubility, fragility). They depend on independent continuants as their bearers. A quality does not require a process of realization, while a disposition (like solubility) requires a process to be manifested.

**Sources**:

- **07-Classifying_Processes_Barry_Smith (Chunk 1:405-409)**
  > BFO generalizes Zemach's idea of a continuant entity by allowing not only things (such as pencils and people) as continuants, but also entities that are dependent on things, such as qualities and dispositions

---

### 246. BFO Quality Entity Type

Qualities are dependent entities that inhere in independent continuants. They instantiate quality universals divided into determinable (temperature, length, mass) and determinate (37.0C temperature, 1.6 meter length). Quality universals can be rigid (always exemplified while bearer exists).

**Sources**:

- **07-Classifying_Processes_Barry_Smith (Chunk 1:458-459)**
  > Qualities are first-class entities in the BFO ontology (of the sort referred to elsewhere in the literature as 'tropes', or 'individual accidents')

---

### 247. BFO Process Entity Type

Processes are temporally extended occurrents that occupy spatiotemporal regions and span temporal intervals. They stand to independent continuants (their participants) in a relation of specific dependence, analogous to how qualities relate to their bearers.

**Sources**:

- **07-Classifying_Processes_Barry_Smith (Chunk 1:547-552)**
  > Our primary concern in the remainder of this essay is with BFO's treatment of occurrents, which include processes, process boundaries, spatiotemporal regions, and temporal intervals and instants

---

### 248. BFO Type/Universal Entity

Types/universals are general entities that have instances. The is_a relation between types represents subtype relationships (all instances of first type are instances of second). Ontologies comprise theoretical terms representing types together with relational expressions.

**Sources**:

- **07-Classifying_Processes_Barry_Smith (Chunk 1:100-102)**
  > We can think of the nodes in such a graph as representing types or universals, which are the sorts of entities represented by the general terms used in formulating scientific theories such as 'cell' or 'electron'

---

### 249. BFO Instance/Particular Entity

Instances/particulars are the entities observed in experiments - specific occurrences of types. The BFO ontological square captures both the type-instance and independent-dependent distinctions creating four categories.

**Sources**:

- **07-Classifying_Processes_Barry_Smith (Chunk 1:101-103)**
  > types or universals which have instances which are the sorts of entities that are observed in scientific experiments

---

### 250. BFO Object Entity Type

Object is a core BFO term representing independent continuants that can serve as participants in processes. Objects are three-dimensional things like you and me - entities with spatial parts but no temporal parts.

**Sources**:

- **07-Classifying_Processes_Barry_Smith (Chunk 1:285-287)**
  > BFO is very small, consisting of just 34 terms, including both familiar terms such as 'process', 'object', 'function', 'role' and 'disposition'

---

### 251. BFO Function Entity Type

Function is a core BFO term for a type of realizable entity (disposition) that is realized through processes. Functions are dependent continuants that require specific kinds of processes for their realization.

**Sources**:

- **07-Classifying_Processes_Barry_Smith (Chunk 1:285-286)**
  > BFO is very small, consisting of just 34 terms, including both familiar terms such as 'process', 'object', 'function', 'role' and 'disposition'

---

### 252. BFO Role Entity Type

Role is a core BFO term representing a type of realizable dependent continuant. Roles define the part an entity plays in relation to other entities and can be gained or lost over time unlike essential qualities.

**Sources**:

- **07-Classifying_Processes_Barry_Smith (Chunk 1:285-286)**
  > BFO is very small, consisting of just 34 terms, including both familiar terms such as 'process', 'object', 'function', 'role' and 'disposition'

---

### 253. BFO Disposition Entity Type

Disposition is a BFO term for realizable dependent continuants like solubility and fragility. Dispositions require a process of realization to be manifested - the solubility of salt requires a dissolving process.

**Sources**:

- **07-Classifying_Processes_Barry_Smith (Chunk 1:286)**
  > familiar terms such as 'process', 'object', 'function', 'role' and 'disposition', and less familiar terms such as 'generically dependent continuant'

---

### 254. BFO Spatiotemporal Region

Spatiotemporal regions are occurrent entities that processes occupy. They define the path of motion and provide the dimensional framework for process measurement and attribution.

**Sources**:

- **07-Classifying_Processes_Barry_Smith (Chunk 1:652-654)**
  > the BFO:spatiotemporal region occupied by this process (the path of the motion), the BFO:temporal region spanned by this process (the temporal projection)

---

### 255. BFO Process Profile Entity Type

Process profiles are occurrent entities that represent what processes share when they can be compared along certain dimensions (rate, speed, etc.). They are the targets of selective abstraction focused on specific structural dimensions of processes.

**Sources**:

- **07-Classifying_Processes_Barry_Smith (Chunk 2:119-126)**
  > When comparing two heart beating processes as being for example of the same rate, there is something in each of the two processes which is - not numerically but qualitatively - 'the same'. This something we shall refer to as a process profile

---

### 256. BFO Quality Process Profile

Quality process profiles capture sequences of quality instances plotted over time, like a temperature chart. They represent the simplest form of process profile where quality values are measured against time.

**Sources**:

- **07-Classifying_Processes_Barry_Smith (Chunk 2:152-157)**
  > The simplest example of a process profile is that part of a process which serves as the target of selective abstraction focused on a sequence of instances of determinate qualities such as temperature or height

---

### 257. BFO Rate Process Profile

Rate process profiles capture ratios like speed (distance/time). They include subtypes like constant speed profiles, acceleration profiles, with a hierarchy of process profile universals at successive levels of generality.

**Sources**:

- **07-Classifying_Processes_Barry_Smith (Chunk 2:174-179)**
  > On a somewhat higher level of complexity are what we shall call rate process profiles, which are the targets of selective abstraction focused on certain ratios between these magnitudes and associated intervals of elapsed time

---

### 258. BFO Cyclical Process Profile

Cyclical process profiles are a subtype of rate process profiles where the salient ratio is number of cycles per unit time. Includes regular and irregular cyclical profiles, important for clinical and diagnostic applications.

**Sources**:

- **07-Classifying_Processes_Barry_Smith (Chunk 2:238-243)**
  > One important sub-family of rate process profiles is illustrated by cyclical processes, for example the 60 beats per minute beating process of John's heart

---

### 259. OCEL Event Entity Type

Events are atomic, discrete occurrences with a timestamp that represent actions or activities in a process. Every event is unique, corresponds to a specific action at a specific point in time, may have attributes, and is typed. Events are the fundamental unit of observation in OCEL.

**Sources**:

- **09-OCEL_20_Specification (Chunk 1:149-154)**
  > Events: Object-centric process mining works on discrete events. They represent the various actions or activities that occur within a system or process, such as approving an order

---

### 260. OCEL Event Type Entity

Event types (also called activities) categorize events by their nature or function. Each event belongs to exactly one type. Event types define the kinds of actions possible in a process and group events that represent the same kind of activity.

**Sources**:

- **09-OCEL_20_Specification (Chunk 1:157-161)**
  > Event Types: Events are categorized into different types based on their nature or function. For example, a procurement process might have event types such as Order Created, Order Approved

---

### 261. OCEL Object Entity Type

Objects are entities involved in events - physical items (products, machines, workers) or abstract entities (orders, invoices, contracts). Objects have attributes with values that may change over time, capturing the dynamic nature of business entities.

**Sources**:

- **09-OCEL_20_Specification (Chunk 1:164-167)**
  > Objects: In object-centric process mining, objects represent the entities that are involved in events. These might be physical items like products in a supply chain, or abstract entities like orders, invoices

---

### 262. OCEL Object Type Entity

Object types categorize objects into classes like Product, Order, Invoice, Supplier. Each object belongs to exactly one type. Object types define the schema of attributes applicable to objects of that type.

**Sources**:

- **09-OCEL_20_Specification (Chunk 1:170-171)**
  > Object Types: Each object is of one type. The object is an instantiation of its type. Object types might include categories like Product, Order, Invoice, or Supplier

---

### 263. OCEL Event-to-Object Relationship

E2O relationships link events to objects with optional qualifiers describing the role an object plays in an event. Unlike traditional logs where events relate to one case, OCEL events can relate to multiple objects. Qualifiers distinguish roles (e.g., meeting organizer vs participant).

**Sources**:

- **09-OCEL_20_Specification (Chunk 1:178-185)**
  > Event-to-Object (E2O) Relationships: Events are associated with objects. This relationship describes that an object affects an event or that an event affects an object

---

### 264. OCEL Object-to-Object Relationship

O2O relationships link objects to each other independent of events, with qualifiers describing the relationship nature (part-of, reports-to, belongs-to). This captures organizational and structural relationships between business entities.

**Sources**:

- **09-OCEL_20_Specification (Chunk 1:191-194)**
  > Object-to-Object (O2O) Relationships: Objects can also be related to other objects outside the context of an event. For example, an employee may be part of an organizational unit

---

### 265. OCEL Attribute Entity

Attributes are named properties that can be assigned to events and objects. Event attributes are static per event while object attributes can be dynamic, changing over time. Attributes provide the data perspective alongside the control flow.

**Sources**:

- **09-OCEL_20_Specification (Chunk 1:362-365)**
  > Uattr is the universe of attribute names. Uval is the universe of attribute values

---

### 266. OCEL Timestamp Entity

Timestamps are totally ordered temporal values that record when events occur and when object attributes change. The temporal dimension enables reconstructing process execution order and analyzing performance.

**Sources**:

- **09-OCEL_20_Specification (Chunk 1:368-369)**
  > Utime is the universe of timestamps (with 0 as the smallest element and infinity as the largest element)

---

### 267. OCEL Qualifier Entity

Qualifiers are strings that describe the nature of relationships between events/objects. They enable rich semantic annotation of how entities relate (e.g., 'Invoice created starting from the PO', 'Payment block due to unethical buying').

**Sources**:

- **09-OCEL_20_Specification (Chunk 1:372)**
  > Uqual is the universe of qualifiers

---

### 268. OCEL Dynamic Object Attribute

Dynamic object attributes capture how object properties evolve during process execution. Values are tracked with timestamps allowing reconstruction of attribute state at any point in time. This reflects realistic business scenarios.

**Sources**:

- **09-OCEL_20_Specification (Chunk 1:293-297)**
  > Dynamic Object Attribute Values: OCEL 2.0 adopts a dynamic approach where attribute values can change over time. Instead of having a single, fixed value, an object attribute may have a value that changes

---

### 269. OC-PM Event Entity

Events in OC-PM are records extracted from databases that capture process execution. Each event has an activity, timestamp, and can be related to multiple objects of different types, enabling richer process representation than traditional single-case logs.

**Sources**:

- **10-OC-PM_Object-Centric_Process_Mining (Chunk 1:46-49)**
  > Mainstream process mining techniques start from an event log, i.e., a collection of events extracted from the databases supporting the process execution

---

### 270. OC-PM Case Entity (Traditional)

In traditional process mining, a case groups events belonging to one process execution. However, defining cases introduces convergence (same event in multiple cases) and divergence (multiple instances of same activity) problems that object-centric mining addresses.

**Sources**:

- **10-OC-PM_Object-Centric_Process_Mining (Chunk 1:48-52)**
  > In such event logs, a case is a collection of events related to a particular process execution. For example, in a sales order management system, a case may refer to all events related to the creation and confirmation of the order

---

### 271. OC-PM Object Entity

Objects in OC-PM are typed entities (like order, item, package, delivery) that events relate to. Objects can have attributes with values. The object-centric approach describes lifecycle of different objects without convergence/divergence problems.

**Sources**:

- **10-OC-PM_Object-Centric_Process_Mining (Chunk 1:82-86)**
  > each event is related to different objects of different types. An informal representation of an object-centric event log is contained in Table 1

---

### 272. OC-PM Object Type

Object types categorize objects in OC-PM (e.g., order, item, package, delivery). Each object belongs to one type which determines applicable attributes and lifecycle patterns. Object types enable typed analysis of process behavior.

**Sources**:

- **10-OC-PM_Object-Centric_Process_Mining (Chunk 1:440-441)**
  > Uot is the universe of objects types. Example: Uot = {order, item, ...}

---

### 273. OC-PM Activity Entity

Activities are the actions or operations that events represent in OC-PM. Activities are associated with events through the activity function and form the basis for directly-follows graphs and process model discovery.

**Sources**:

- **10-OC-PM_Object-Centric_Process_Mining (Chunk 1:226-227)**
  > Uact is the universe of activities. Example: Uact = {place order, check availability, ...}

---

### 274. OC-PM Lifecycle Entity

Lifecycle captures the sequence of events related to an object throughout its existence. Start and end activities identify process boundaries. Lifecycles enable object-centric analysis without artificial case flattening.

**Sources**:

- **10-OC-PM_Object-Centric_Process_Mining (Chunk 1:601-611)**
  > The lifecycle of an object o is the sequence of events to which the object is related. The trace of an object is the sequence of activities of the events belonging to its lifecycle

---

### 275. OC-DFG Node Entity

OC-DFG nodes include activities plus start/end nodes for each object type. This structure captures how different object types have different entry and exit points in the process, enabling multi-perspective process views.

**Sources**:

- **10-OC-PM_Object-Centric_Process_Mining (Chunk 1:769-774)**
  > N = A union {nS,ot | ot in OT} union {nE,ot | ot in OT} is the set of nodes of the graph, which includes the set of activities and a start/end node for each object type

---

### 276. OC-DFG Arc Entity

OC-DFG arcs are typed edges connecting nodes and carrying object type information. This allows the same activities to be connected by different edge types representing different object type flows through the process.

**Sources**:

- **10-OC-PM_Object-Centric_Process_Mining (Chunk 1:781)**
  > F is subset of N x OT x N is a set of typed arcs

---

### 277. EKG Event Node Entity

Event nodes in event knowledge graphs represent discrete events with activity and timestamp properties. Events can be correlated to multiple entities, enabling rich multi-entity process analysis without the limitations of single-case event logs.

**Sources**:

- **11-Process_Mining_Event_Knowledge_Graphs (Chunk 1:16-18)**
  > We introduce event knowledge graphs as data structure that allows to naturally model behavior over multiple entities as a network of events

---

### 278. EKG Entity Node

Entity nodes represent the objects and organizational units involved in processes. Entity types include objects (Orders, Items, Invoices) and actors (human workers, machines). Entities are correlated to events and can be related to each other.

**Sources**:

- **11-Process_Mining_Event_Knowledge_Graphs (Chunk 1:31-34)**
  > the actual processes are rather complex and emerge from the interplay of multiple inter-related entities: the various objects handled by the process as well as the organizational entities that execute the process

---

### 279. EKG Directly-Follows Relationship

Directly-follows relationships are defined locally per entity, not globally per case. This avoids false behavioral information from convergence/divergence. Each df-relationship references the specific entity it holds for, enabling multi-perspective analysis.

**Sources**:

- **11-Process_Mining_Event_Knowledge_Graphs (Chunk 1:519-529)**
  > e2 directly follows e1 from the perspective of n, written e1 <n,T e2 iff both are correlated to n, e1 occurred before e2, and there is no other event correlated to n in between

---

### 280. EKG Correlation Relationship

Correlation relationships link events to entities they involve. An event can be correlated to multiple entities of different types. Correlation forms the basis for deriving directly-follows relationships and understanding entity interactions.

**Sources**:

- **11-Process_Mining_Event_Knowledge_Graphs (Chunk 1:261-268)**
  > Event e is correlated to entity n, written (e,n) in corr iff n = e.ent or n in e.ent

---

### 281. EKG Related Relationship

Relations between entity types are inferred from event data when events reference multiple entity types. Relations have cardinalities (1-to-1, n-to-1, n-to-m) and can be composed to derive transitive relationships between entities.

**Sources**:

- **11-Process_Mining_Event_Knowledge_Graphs (Chunk 1:300-302)**
  > The relation between ent1 and ent2 in T is R(ent1,ent2) = {(e.ent1, ent2) | e.ent1 != null, e.ent2 != null}

---

### 282. EKG Derived Entity

Derived entities are created by reifying relationships between entity types. They enable analysis of interactions between related entities (like Order-Payment pairs). Events correlated to either original entity become correlated to the derived entity.

**Sources**:

- **11-Process_Mining_Event_Knowledge_Graphs (Chunk 1:893-896)**
  > We reify the relation between two entity types ent1 and ent2 into a new derived entity type (ent1, ent2). That is, we make each pair (n1, n2) an entity node

---

### 283. EKG df-path Entity

df-paths are sequences of directly-follows relationships for a single entity, similar to traces in classical event logs. Multiple df-paths can meet at events correlated to multiple entities, capturing synchronization points in multi-entity processes.

**Sources**:

- **11-Process_Mining_Event_Knowledge_Graphs (Chunk 1:668-672)**
  > A path of df-relationships is a directly-follows path (df-path) iff all relationships are defined for the same entity

---

### 284. EKG Actor Entity

Actors are a type of entity representing human workers who execute process activities. Actors can specialize in specific activities across multiple object types. The actor perspective enables analysis of resource behavior and handoffs.

**Sources**:

- **11-Process_Mining_Event_Knowledge_Graphs (Chunk 1:83-85)**
  > This process relies on 7 different types of entities. Actors (human workers) and machines (an automated warehouse) together handle 5 types of objects

---

### 285. EKG Machine Entity

Machines are entities like automated warehouses that participate in process execution alongside human actors. They represent the automated/system dimension of process behavior distinct from human actors.

**Sources**:

- **11-Process_Mining_Event_Knowledge_Graphs (Chunk 1:83-84)**
  > Actors (human workers) and machines (an automated warehouse) together handle 5 types of objects

---

### 286. EKG Labeled Property Graph Structure

The underlying data structure for event knowledge graphs. LPGs support typed nodes (Event, Entity) and relationships (df, corr, related) with properties. This enables graph database storage and Cypher query support for process mining.

**Sources**:

- **11-Process_Mining_Event_Knowledge_Graphs (Chunk 1:574-583)**
  > A labeled property graph (LPG) G = (N, R, lambda, #) is a graph with nodes N, and relationships R where each node carries a label and each relationship carries a label and defines a directed edge

---

### 287. EKG Convergence/Divergence Problem Entities

Convergence occurs when events relate to multiple cases causing duplication. Divergence occurs when cases contain multiple instances of the same activity. Event knowledge graphs avoid these by using local directly-follows per entity rather than global case-based traces.

**Sources**:

- **11-Process_Mining_Event_Knowledge_Graphs (Chunk 1:69-78)**
  > establishing a case notion can lead to the known convergence and divergence problems. We have a convergence problem when the same event is related to different cases

---

### 288. EKG Multi-Entity Process Fabric

Processes over multiple entities form a complex network/fabric where entity lifecycles synchronize and interact. This fabric cannot be partitioned into independent cases. Event knowledge graphs represent this fabric as a network of synchronized df-paths.

**Sources**:

- **11-Process_Mining_Event_Knowledge_Graphs (Chunk 1:147-153)**
  > the behavior itself is a larger 'fabric' of multiple entities that are inter-related and inter-twined over time

---

### 289. Entity Node Type

Entity is a core node type in event knowledge graphs. Entities are constructed based on the presence of an entity identifier or a relation, representing objects or concepts being tracked through the process (e.g., Order, Payment, Item, Invoice).

**Sources**:

- **11-Process_Mining_Event_Knowledge_Graphs (Chunk 2:51-56)**
  > This method for constructing event knowledge graphs uses basic principles of information inference: (1) construct entities and correlation based on...

---

### 290. Event Node Type

Event is a fundamental node type representing atomic occurrences in process execution. Events have properties like time and activity, and serve as starting, ending, or intermediate points in entity df-paths.

**Sources**:

- **11-Process_Mining_Event_Knowledge_Graphs (Chunk 2:86-91)**
  > Event e is starting or ending event if it has no incoming or outgoing df-relationship at all... Event e is starting or ending event for entity n if it has no incoming...

---

### 291. Derived Entity Type

Derived Entity is a composite entity type created by reifying relations between two entities (e.g., Order, Payment becomes a derived entity type). This enables tracking interactions between related entities as first-class objects.

**Sources**:

- **11-Process_Mining_Event_Knowledge_Graphs (Chunk 2:3-12)**
  > Then we can treat any derived entity (n1, n2) just like any other entity and infer the df-relationships for (n1, n2), which results in a new path describing the interactions...

---

### 292. Order Entity Type (Business Object)

Order is a domain-specific entity type representing customer orders in the retail process example. Orders are tracked through their lifecycle via df-paths from creation to shipment.

**Sources**:

- **11-Process_Mining_Event_Knowledge_Graphs (Chunk 2:112-113)**
  > O1 and O2 both start with Create Order and end with Ship events with Create Invoice followed by Pack Shipment in between.

---

### 293. Item Entity Type (Business Object)

Item is an entity type representing physical items being processed. Items have their own df-paths tracking their journey through receiving, unpacking, and packing operations.

**Sources**:

- **11-Process_Mining_Event_Knowledge_Graphs (Chunk 2:118-119)**
  > Items X1, ..., Y2 start with Receive SO followed by Unpack and end with Pack Shipment

---

### 294. Payment Entity Type

Merged from 3 sources. Proclets are behavioral model components that describe entity type behavior. Each proclet (Order, Supplier Order, Invoice, Item, Payment, derived entity types, Actors) represents a distinct entity type with its own behavioral specification.

**Sources**:

- **11-Process_Mining_Event_Knowledge_Graphs (Chunk 2:8-10)**
  > Figure 8 shows the result of reifying the relation between Order and Payment entities of Fig. 7 into derived entities (O1, P1) and (O2, P1) of type (Order, Payment)...

- **11-Process_Mining_Event_Knowledge_Graphs (Chunk 3:5-7)**
  > Item, Payment, and (Order,Payment) are each discovered from the entity type's df-paths of the graph in Fig. 9. The proclets for the Actors however are created manually...

- **18-Multi-Agent_Taxonomy (Chunk 2:99-101)**
  > LLM-powered agents are able to leverage specialized competencies and further information provided by additional Context which can be distinguished into Tools, Data, and Foundation Models

---

### 295. Invoice Entity Type

Invoice is an entity type representing billing documents in the process. Invoices have defined lifecycles tracked through df-paths from creation to clearance.

**Sources**:

- **11-Process_Mining_Event_Knowledge_Graphs (Chunk 2:121-122)**
  > I1 and I2 start with Create Invoice and end with Clear Invoice

---

### 296. Supplier Order Entity Type

Supplier Order is an entity type representing orders placed with suppliers. These entities track the procurement side of the process from placement through receipt.

**Sources**:

- **11-Process_Mining_Event_Knowledge_Graphs (Chunk 2:115-116)**
  > A and B both start with Place SO (eventually) followed by Receive SO, ending with multiple Unpack events.

---

### 297. Class Node Type (Activity Aggregation)

Class is a node type created through aggregation that represents activity types shared by multiple events. Class nodes enable abstraction from individual events to activity-level analysis.

**Sources**:

- **11-Process_Mining_Event_Knowledge_Graphs (Chunk 2:330-338)**
  > For each value c in {e.Activity | e in N^Event} of the Activity property that we find among the events in the graph, we create a new node c with label Class...

---

### 298. TaskInstance Node Type

TaskInstance is a higher-level node type representing a unit of work performed by an actor on an entity. Task instances are identified by subgraph patterns where actor and entity df-paths synchronize over consecutive events.

**Sources**:

- **11-Process_Mining_Event_Knowledge_Graphs (Chunk 2:621-627)**
  > A task instance of an actor R working on an entity X materializes in an event knowledge graph as a specific subgraph over event nodes e1,...,ek...

---

### 299. Task Node Type

Task is an aggregated node type that groups TaskInstance nodes by their task description. Tasks represent recurring patterns of work activity (e.g., Place SO, Update SO, Receive SO followed by Unpack).

**Sources**:

- **11-Process_Mining_Event_Knowledge_Graphs (Chunk 2:730-736)**
  > To understand which tasks are performed and how often, we aggregate TaskInstance nodes into Task nodes by their Task property...

---

### 300. Object-Centric Petri Net Entity Types

In object-centric Petri nets, each entity type has its own Petri net model that is composed with others. Entity types are distinguished by unique identifiers annotated on places and arcs.

**Sources**:

- **11-Process_Mining_Event_Knowledge_Graphs (Chunk 3:17-23)**
  > Object-centric Petri nets also first discover one Petri net per entity type, then annotate the places and arcs with entity identifiers...

---

### 301. Event (Fundamental Unit)

Event is the fundamental atomic unit in process mining. Events are observations (rows) in event log datasets that are related to each other through time and case dimensions.

**Sources**:

- **12-Foundations_of_Process_Event_Data (Chunk 1:14-20)**
  > Process event data is a fundamental building block for process mining as event logs portray the execution trails of business processes from which knowledge...

---

### 302. Case (Process Instance)

Case (or Process Instance) is a core entity type representing a single execution of a business process. Each case has a unique Case ID that links related events together.

**Sources**:

- **12-Foundations_of_Process_Event_Data (Chunk 1:68-74)**
  > First, each event should be linked to a case or process instance, typically by using a Case ID. This is 'Requirement 1'...

---

### 303. Activity

Activity is an entity type representing discrete steps or operations in a business process. Events map to activities through activity labels drawn from a restricted set of process activities.

**Sources**:

- **12-Foundations_of_Process_Event_Data (Chunk 1:92-106)**
  > The second key requirement for event log data is the fact that each event should correspond to an activity executed within the process. More specifically, an assumption is made...

---

### 304. Trace

Trace is an ordered sequence of events belonging to a single case. Traces represent the complete execution path of a process instance from start to finish.

**Sources**:

- **12-Foundations_of_Process_Event_Data (Chunk 1:110-116)**
  > Finally, the last requirement entails that there exists an ordering of the events pertaining to a case. As such, each case logically consists of a sequence of events.

---

### 305. Log

Log is a container entity type in the XES standard that holds multiple traces. Logs represent collections of process executions and can have attributes at the log level.

**Sources**:

- **12-Foundations_of_Process_Event_Data (Chunk 1:163-175)**
  > In IEEE XES, events are considered as an observed atomic granule of activity. Next to events, IEEE XES specifies the concept of a log, a trace, and an attribute component.

---

### 306. Attribute

Attribute is an entity type representing properties of events, traces, or logs. Attributes can be process instance-level (constant within case) or event-level (varying across events).

**Sources**:

- **12-Foundations_of_Process_Event_Data (Chunk 1:127-136)**
  > In addition to the mandatory elements of a Case ID, Activity, and Timestamp, event logs will usually contain several or often many additional attributes (columns).

---

### 307. Extension

Extension is a meta-entity type in XES that defines standard attribute sets for specific domains. Extensions provide schema definitions for common attribute patterns.

**Sources**:

- **12-Foundations_of_Process_Event_Data (Chunk 1:172-175)**
  > The standard does not define a specific set of attributes for events, traces or logs. However, it does allow for extensions. An extension can be used to define a set of attributes...

---

### 308. Classifier

Classifier is a meta-entity type that assigns identity to traces and events. Classifiers determine how events and traces are uniquely identified within a log.

**Sources**:

- **12-Foundations_of_Process_Event_Data (Chunk 1:169-171)**
  > Event and/or trace classifiers are used to assign an identity to traces and events.

---

### 309. Lifecycle Transition

Lifecycle Transition is an entity type representing states and state changes in activity execution (e.g., start, complete, suspend, resume). The XES lifecycle extension defines a standard activity lifecycle state machine.

**Sources**:

- **12-Foundations_of_Process_Event_Data (Chunk 1:181-186)**
  > When sourcing events from many process-aware information systems, events oftentimes relate to the transactional lifecycle that activities undergo...

---

### 310. Object (Artifact)

Object (or Artifact) is an entity type in object-centric process mining representing business objects tracked across processes. The OCEL standard supports multiple object types per event.

**Sources**:

- **12-Foundations_of_Process_Event_Data (Chunk 1:424-433)**
  > Another important stream of research within the realm of event extraction addresses object or artifact centricity... Oftentimes, assumptions in terms of a desired perspective...

---

### 311. Agent (LLM-Based)

Agent is a core entity type representing autonomous LLM-powered actors in the multi-agent system. Agents have specialized roles (Ontologist, Scientist, Critic, Planner) and interact to accomplish complex scientific discovery tasks.

**Sources**:

- **15-SciAgents_Multi-Agent_Graph_Reasoning (Chunk 1:117-120)**
  > Multi-agent AI systems are known for their ability to tackle complex problems across different domains by pooling their capabilities...

---

### 312. Ontologist Agent

Merged from 2 sources. Ontologist is a specialized agent type responsible for analyzing knowledge graph paths and defining concepts and relationships. The Ontologist provides deep insights that transition from static knowledge retrieval to dynamic knowledge generation.

**Sources**:

- **15-SciAgents_Multi-Agent_Graph_Reasoning (Chunk 1:225-226)**
  > Each agent plays a specialized role: The Ontologist defines key concepts and relationships...

- **15-SciAgents (Chunk 3:899)**
  > ontologist: An ontologist who defines each of the terms and discusses the relationships in the path

---

### 313. Scientist Agent

Merged from 2 sources. Scientist is a specialized agent type for hypothesis generation and refinement. Scientist_1 creates initial research proposals while Scientist_2 expands with quantitative details, chemical formulas, and modeling techniques.

**Sources**:

- **15-SciAgents_Multi-Agent_Graph_Reasoning (Chunk 1:226-227)**
  > Scientist 1 crafts a detailed research proposal, Scientist 2 expands and refines the proposal...

- **15-SciAgents (Chunk 3:899-900)**
  > scientist: A scientist who can craft the research proposal with key aspects based on the definitions and relationships acquired by the ontologist

---

### 314. Critic Agent

Merged from 2 sources. Critic is a specialized agent type responsible for evaluating research proposals. The Critic identifies strengths and weaknesses, suggests improvements, and proposes specific molecular modeling and experimental priorities.

**Sources**:

- **15-SciAgents_Multi-Agent_Graph_Reasoning (Chunk 1:227-228)**
  > and the Critic agent conducts a thorough review and suggests improvements.

- **15-SciAgents (Chunk 3:905-906)**
  > critic_agent: Summarizes, critiques, and suggests improvements after all seven aspects of the proposal have been expanded by the agents

---

### 315. Planner Agent

Planner is a specialized agent type in the automated multi-agent system that develops detailed execution plans for research hypothesis generation tasks.

**Sources**:

- **15-SciAgents_Multi-Agent_Graph_Reasoning (Chunk 1:227-228)**
  > The Planner in the second approach develops a detailed plan...

---

### 316. Node (Knowledge Graph)

Merged from 2 sources. Path is an entity type representing a sequence of connected nodes and edges between two concepts in the knowledge graph. Paths (random or shortest) provide context for hypothesis generation by revealing concept relationships.

**Sources**:

- **15-SciAgents_Multi-Agent_Graph_Reasoning (Chunk 1:108-110)**
  > These knowledge graphs not only provide a mechanistic breakdown of information but also offer an ontological framework that elucidates the interconnectedness of different concepts, delineated as nodes and edges...

- **15-SciAgents_Multi-Agent_Graph_Reasoning (Chunk 1:239-246)**
  > At the core of our model is an expansive knowledge graph... we provide it with a sub-graph derived from this more extensive knowledge graph. This sub-graph depicts a pathway...

---

### 317. Edge (Knowledge Graph Relationship)

Edge is an entity type representing relationships between concepts in the knowledge graph. Edges connect nodes with semantic relationships like 'provides', 'possess', 'include', 'is'.

**Sources**:

- **15-SciAgents_Multi-Agent_Graph_Reasoning (Chunk 1:108-110)**
  > ...delineated as nodes and edges within the graph.

---

### 318. Hypothesis

Hypothesis is a structured entity type representing a research proposal. Hypotheses have defined components including outcome, mechanisms, design principles, unexpected properties, comparison, and novelty assessment.

**Sources**:

- **15-SciAgents_Multi-Agent_Graph_Reasoning (Chunk 1:362-364)**
  > The agent creates a proposal that carefully addresses the following seven key aspects: hypothesis, outcome, mechanisms, design principles, unexpected properties, comparison, and novelty.

---

### 319. Human Agent

Human is an agent type representing the human user in the multi-agent system. Human agents pose tasks, provide feedback, and can intervene at various stages of the automated research process.

**Sources**:

- **15-SciAgents_Multi-Agent_Graph_Reasoning (Chunk 1:720)**
  > 'Human': human user that poses the task and can intervene at various stages of the problem solving process.

---

### 320. Assistant Agent

Assistant is a specialized agent type with access to external tools (Semantic Scholar API, path generation functions). The Assistant executes tool calls and assesses research hypothesis novelty.

**Sources**:

- **15-SciAgents_Multi-Agent_Graph_Reasoning (Chunk 1:733-735)**
  > 'Assistant': has access to external tools including a function to generate a knowledge path from two keywords and a function to assess the novelty and feasibility...

---

### 321. Group Chat Manager

Group Chat Manager is a coordination entity type that orchestrates multi-agent interactions. It selects the next speaking agent based on context and broadcasts messages to enable collaborative problem-solving.

**Sources**:

- **15-SciAgents_Multi-Agent_Graph_Reasoning (Chunk 1:737-738)**
  > 'Group chat manager': chooses the next speaker based on the context and agent profiles and broadcasts the message to the whole group.

---

### 322. Tool

Tool is an entity type representing functions that agents can invoke. Tools have names, descriptions, and input properties, enabling agents to perform actions like knowledge path generation and novelty assessment.

**Sources**:

- **15-SciAgents_Multi-Agent_Graph_Reasoning (Chunk 2:498-499)**
  > All the tools implemented in this work are defined as python functions. Each function is characterized by a name, a description, and input properties...

---

### 323. Novelty Assistant Agent

Novelty Assistant is a specialized agent type dedicated to assessing research hypothesis novelty against existing literature. It queries the Semantic Scholar API with different keyword combinations and analyzes abstracts.

**Sources**:

- **15-SciAgents_Multi-Agent_Graph_Reasoning (Chunk 2:505-509)**
  > To ensure a thorough assessment of the research idea, we have implemented a tool featuring an AI agent named the 'novelty assistant', which calls the Semantic Scholar API three times...

---

### 324. Subgraph

Subgraph is an entity type representing a focused portion of the larger knowledge graph. Subgraphs include path nodes and their neighbors, providing contextual knowledge for reasoning tasks.

**Sources**:

- **15-SciAgents_Multi-Agent_Graph_Reasoning (Chunk 2:256-260)**
  > After the path is found, a subgraph consisting of the path nodes and their second-hop neighbors is generated, providing a broader context for the discovered route.

---

### 325. JSON Structure (Research Output)

JSON Structure is a data entity type used to represent structured research outputs. The structure contains fields for hypothesis, outcome, mechanisms, design_principles, unexpected_properties, comparison, and novelty.

**Sources**:

- **15-SciAgents_Multi-Agent_Graph_Reasoning (Chunk 2:305-307)**
  > This output is formatted as a JSON object with fields like 'hypothesis', 'outcome', and 'design_principles', each reflecting different aspects of the potential research...

---

### 326. Multi-Agent Role Specialization Types

The SciAgents framework defines specialized agent types organized by function: user (human-in-the-loop), planner (task decomposition), assistant (tool execution), ontologist (term definitions), scientist (proposal crafting), and multiple specialized agents for different proposal aspects (hypothesis_agent, outcome_agent, mechanism_agent, design_principles_agent, unexpected_properties_agent, comparison_agent, novelty_agent, critic_agent). This demonstrates role-based agent typing where each agent has a specific responsibility in the collaborative workflow.

**Sources**:

- **15-SciAgents (Chunk 3:894-906)**
  > user: An attentive HUMAN user... planner: A planner who can suggest a plan... assistant: An assistant who calls the appropriate tools...

---

### 327. Hypothesis Agent Type

A specialized agent type focused on expanding and elaborating the hypothesis component of research proposals. Part of the seven specialized aspect agents.

**Sources**:

- **15-SciAgents (Chunk 3:900-901)**
  > hypothesis_agent: hypothesis_agent who can expand the 'hypothesis' aspect of the research proposal crafted by the 'scientist'

---

### 328. Silk Entity

A domain entity type representing a biological material with specific properties (strength, biocompatibility). Used as a source concept in knowledge graph reasoning.

**Sources**:

- **15-SciAgents (Chunk 4:92)**
  > Silk: A natural protein fiber produced by certain insects, most notably silkworms, used in textiles and biomedical applications

---

### 329. Biological Materials Entity

Merged from 2 sources. A general category entity type encompassing materials derived from living organisms. Serves as a bridging concept in knowledge graph paths.

**Sources**:

- **15-SciAgents (Chunk 4:93)**
  > Biological Materials: Substances that are produced by or derived from living organisms, including proteins, polysaccharides, and other biopolymers

- **15-SciAgents (Chunk 5:244)**
  > Biomimetic Materials: Materials designed to imitate the structure and function of natural biological systems

---

### 330. Novel Functionalities Entity

An abstract entity type representing emergent or designed capabilities. Links material entities to performance outcomes in knowledge graphs.

**Sources**:

- **15-SciAgents (Chunk 4:94)**
  > Novel Functionalities: New or unique capabilities or properties that are not typically associated with a material or system

---

### 331. Low-Temperature Processing Entity

A process entity type defining manufacturing methods with specific temperature constraints. Links to material preservation and energy efficiency outcomes.

**Sources**:

- **15-SciAgents (Chunk 4:95)**
  > Low-Temperature Processing: Techniques for fabricating or manipulating materials at temperatures that do not cause thermal degradation, often below 100C

---

### 332. Multi-Scale Organization Entity

A structural entity type representing hierarchical organization across scales. Key for biomimetic material design.

**Sources**:

- **15-SciAgents (Chunk 4:96)**
  > Multi-Scale Organization: The arrangement of structures at various scales, from the molecular to the macroscopic level, within a material or system

---

### 333. Pigments Entity

A material entity type with specific optical properties. Used in combination with biological materials for structural coloration.

**Sources**:

- **15-SciAgents (Chunk 4:98)**
  > Pigments: Substances that provide color to materials by absorbing certain wavelengths of light

---

### 334. Energy-Intensive Entity

A process attribute entity characterizing energy consumption. Used to compare traditional vs. novel manufacturing approaches.

**Sources**:

- **15-SciAgents (Chunk 4:100)**
  > Energy-Intensive: Processes or activities that require a large amount of energy to perform

---

### 335. Heat Transfer Performance Entity

A performance metric entity type quantifying thermal properties of materials and systems.

**Sources**:

- **15-SciAgents (Chunk 5:238)**
  > Heat Transfer Performance: The efficiency with which heat is transferred from one medium to another

---

### 336. Surface Wettability Entity

A material property entity type characterizing surface-liquid interactions.

**Sources**:

- **15-SciAgents (Chunk 5:239)**
  > Surface Wettability: The ability of a liquid to maintain contact with a solid surface, influenced by intermolecular interactions

---

### 337. Soft Lithography Entity

A fabrication technique entity type for creating microstructures. Links to biocompatibility improvements.

**Sources**:

- **15-SciAgents (Chunk 5:240)**
  > Soft Lithography: A set of techniques for fabricating or replicating structures using elastomeric stamps, molds, and conformable photomasks

---

### 338. Biocompatibility Entity

A material property entity type critical for biomedical applications. Qualifies materials for biological system integration.

**Sources**:

- **15-SciAgents (Chunk 5:241)**
  > Biocompatibility: The ability of a material to perform with an appropriate host response in a specific application

---

### 339. Biocompatible Materials Entity

A material category entity type defined by biological compatibility constraints.

**Sources**:

- **15-SciAgents (Chunk 5:242)**
  > Biocompatible Materials: Materials that are compatible with living tissue and do not produce an immunological response

---

### 340. Biomaterials Entity

A general material category entity type defined by biological interaction capability.

**Sources**:

- **15-SciAgents (Chunk 5:245)**
  > Biomaterials: Any matter, surface, or construct that interacts with biological systems

---

### 341. Cyclic Loading Conditions Entity

A testing condition entity type for evaluating material durability and fatigue behavior.

**Sources**:

- **15-SciAgents (Chunk 5:246)**
  > Cyclic Loading Conditions: Repeated application of load or force on a material over time

---

### 342. Microfluidic Chips Entity

A device entity type combining materials science with fluid dynamics for biomedical applications.

**Sources**:

- **15-SciAgents (Chunk 5:247)**
  > Microfluidic Chips: Devices that manipulate small volumes of fluids using channels with dimensions of tens to hundreds of micrometers

---

### 343. Lamellar Structure Entity

A structural organization entity type characterizing hierarchical layering in materials.

**Sources**:

- **15-SciAgents (Chunk 5:248)**
  > Lamellar Structure: A layered structure often found in biological materials, providing strength and flexibility

---

### 344. Keratin Scales Entity

A biological structure entity type providing inspiration for biomimetic material design.

**Sources**:

- **15-SciAgents (Chunk 5:249)**
  > Keratin Scales: Hard, protective structures made of keratin, found in various animals

---

### 345. Stiffness Memory Entity

A material property entity type describing reversible mechanical behavior.

**Sources**:

- **15-SciAgents (Chunk 6:302)**
  > Stiffness memory: The ability of a material to return to its original stiffness after being deformed

---

### 346. Dynamic 3D Structures Entity

A structural entity type characterized by stimulus-responsive behavior.

**Sources**:

- **15-SciAgents (Chunk 6:304)**
  > Dynamic 3D structures: Three-dimensional structures that can change or move in response to external stimuli

---

### 347. Cell Signaling Entity

A biological process entity type mediating cellular communication and material-cell interactions.

**Sources**:

- **15-SciAgents (Chunk 6:306)**
  > Cell signaling: The process by which cells communicate with each other through chemical signals

---

### 348. Crashworthiness Entity

A performance property entity type for safety-critical material applications.

**Sources**:

- **15-SciAgents (Chunk 6:310)**
  > Crashworthiness: The ability of a structure to protect its occupants during an impact

---

### 349. Multi-Agent Role Taxonomy

SciAgents defines a comprehensive multi-agent taxonomy with distinct entity roles: user (human interaction), planner (task decomposition), assistant (tool execution), ontologist (term definition), scientist (proposal crafting), hypothesis_agent, outcome_agent, mechanism_agent, design_principles_agent, unexpected_properties_agent, comparison_agent, novelty_agent, and critic_agent. Each agent has a specialized function in the research proposal workflow.

**Sources**:

- **15-SciAgents (Chunk 7:474-486)**
  > user: An attentive HUMAN user... planner: A planner who can suggest a plan... assistant: An assistant who calls tools... ontologist: An ontologist who defines terms...

---

### 350. Ontologist Agent Entity Type

The ontologist is defined as an entity type with the specific function of defining terminology and analyzing relationships. This represents a meta-ontological role - an agent whose purpose is ontology work itself, making explicit the connection between agent types and ontological reasoning.

**Sources**:

- **15-SciAgents (Chunk 7:479)**
  > ontologist: An ontologist who defines each of the terms and discusses the relationships in the path

---

### 351. Knowledge Path Entity Structure

Entity relationships are represented as knowledge paths with typed edges connecting concept nodes. The path structure shows: Entity -- Relationship -- Entity patterns, representing both physical entities (material, scaffolds) and abstract concepts (processability, properties).

**Sources**:

- **15-SciAgents (Chunk 7:576-577)**
  > tunable processability -- Allows for -- material extrusion -- Allows for Creation of -- controlled pore sizes -- Achieved through varying...

---

### 352. Hierarchical Structure Entity Type

Hierarchical structure is identified as an entity type that spans multiple abstraction levels (molecular, cellular, macroscale). This represents a key pattern for ontology design: entities that inherently contain nested sub-entities organized at different scales.

**Sources**:

- **15-SciAgents (Chunk 7:196-199)**
  > Hierarchical 3D Porous Architecture: Engineering collagen into a multi-level structure that enhances crashworthiness and stiffness memory

---

### 353. Agent-Tool-Executor Triad

The assistant agent entity type is defined by its relationship to tools (calls/invokes) and results (returns). This establishes a fundamental pattern: Agent entities are characterized by their capacity to use Resource entities (tools) and produce Data entities (results).

**Sources**:

- **15-SciAgents (Chunk 7:477-478)**
  > assistant: An assistant who calls the appropriate tools and functions and returns the results

---

### 354. Design Principles Entity Type

Design principles emerge as a distinct entity type encompassing methodology, computational approaches, and manufacturing techniques. This represents Rule entities that constrain how other entities (materials, structures) can be created and combined.

**Sources**:

- **15-SciAgents (Chunk 7:238-242)**
  > Design and Fabrication: Computational Modeling: Use finite element analysis (FEA) to design the hierarchical structure... Advanced Manufacturing: Fabricate using 3D printing...

---

### 355. Mechanism Entity Type

Mechanisms are identified as process-oriented entity types that explain causal relationships between other entities. They bridge structural entities (collagen, architecture) with behavioral outcomes (deformation, energy absorption).

**Sources**:

- **15-SciAgents (Chunk 7:289-290)**
  > The mechanisms involve collagen self-assembly, reversible deformation at the molecular and cellular levels, and energy absorption through the hierarchical structure

---

### 356. Novelty Rating Entity

Novelty is quantified as a measurable entity attribute (8/10 scale), representing an evaluation dimension. This shows how abstract qualities can be reified as entity properties with defined value ranges.

**Sources**:

- **15-SciAgents (Chunk 7:442-445)**
  > Novelty: 8/10 The proposed hypothesis is quite novel, especially in the context of combining hierarchical collagen-based materials with dynamic 3D porous architectures

---

### 357. Feasibility Entity Attribute

Feasibility is defined as an entity attribute with quantitative scoring (7/10) and qualitative justification. Paired with Novelty, these form evaluation dimensions that can be applied to Goal or Task entities.

**Sources**:

- **15-SciAgents (Chunk 7:450-456)**
  > Feasibility: 7/10 The feasibility of this research is moderately high... integrating these components into a cohesive study... adds complexity

---

### 358. Properties Entity Category

Properties form a distinct entity category that can be expected or unexpected. Each property (self-healing, biocompatibility, thermal stability) is an entity type that characterizes other entities (materials, scaffolds).

**Sources**:

- **15-SciAgents (Chunk 8:93-97)**
  > We predict that the integration of nanocomposites may lead to unexpected properties such as: 1. Self-Healing... 2. Enhanced Biocompatibility...

---

### 359. Quantitative Metrics Entity Type

Quantitative metrics emerge as Data entities with measurement methods, units, and target values. Examples include healing efficiency (percentage), healing time (hours), tensile strength (MPa), establishing a pattern for how metrics are ontologically modeled.

**Sources**:

- **15-SciAgents (Chunk 8:108-112)**
  > Healing Efficiency: Measure the percentage of mechanical property recovery after damage... Healing Time: The time required for the scaffold to recover its mechanical properties

---

### 360. Comparison Entity Type

Comparison is defined as a relational entity type that links two or more entities through comparative analysis. It includes dimensions (tensile strength, elasticity), baseline values, and expected improvements.

**Sources**:

- **15-SciAgents (Chunk 8:197-200)**
  > Compared to traditional collagen-based scaffolds: 1. Tensile Strength: Traditional Scaffolds: Typically exhibit tensile strengths in the range of 0.5-1 MPa

---

### 361. Gene Circuit Entity Type

Gene circuits represent a biological control entity type that regulates protein expression and assembly. This extends the Agent concept to include programmed biological systems that exhibit goal-directed behavior.

**Sources**:

- **15-SciAgents (Chunk 9:44-47)**
  > Gene Circuit Regulation: The hypothesis extends to the use of synthetic biology to control the production of amyloid-forming proteins

---

### 362. Knowledge Graph Entity Structure

Merged from 2 sources. Knowledge graphs are structured as Entity-Relationship-Entity paths where each node is an entity type (platelets, nacre, biomaterials) and edges are typed relationships (arranged_in, constituent_part_of, example_of, consists_of).

**Sources**:

- **15-SciAgents (Chunk 9:803-805)**
  > hexagonally packed -- arranged in -- platelets -- constituent part of -- nacre -- example of -- biomaterials -- consists of -- hierarchical structure

- **17-KG_Reasoning (Chunk 1:35-39)**
  > Knowledge graph (KG), representing facts in the form of triples, with vocabulary defined in a schema (also known as ontology)

---

### 363. Amyloid Fibrils Entity Type

Amyloid fibrils are defined as a specific biological entity type with structural characteristics (fibrous) and functional associations (disease-related). This exemplifies domain-specific entity specialization.

**Sources**:

- **15-SciAgents (Chunk 9:823)**
  > Amyloid Fibrils: Protein aggregates that form fibrous structures and are associated with various diseases

---

### 364. AFM Imaging Entity Type

AFM imaging represents a measurement/observation entity type that produces Data entities (images, measurements). It is characterized by its scale (nanoscale), output type (images), and what it reveals (structure, properties).

**Sources**:

- **15-SciAgents (Chunk 9:85-91)**
  > AFM Imaging: Nanoscale Analysis: Atomic Force Microscopy (AFM) allows for the measurement of mechanical properties at the nanoscale level

---

### 365. Researcher Team Entity Structure

The research team is modeled as a collection of Agent entity types with specialized roles. The 'caller' role is particularly notable as a coordinator agent that manages the sequence of agent interactions.

**Sources**:

- **15-SciAgents (Chunk 9:697-709)**
  > user: An attentive HUMAN user... planner: I can suggest a plan... scientist: I can craft the research proposal... caller: I am responsible to pick the next agent

---

### 366. Knowledge Graph Triple Entity

Knowledge graphs are formally defined using entity types E (entities), R (relations), and the triple structure <e, r, e'>. This provides a foundational entity model: Entity-Relation-Entity triples as atomic knowledge units.

**Sources**:

- **16-KG-Agent (Chunk 1:176-180)**
  > A knowledge graph typically consists of a large number of fact triples, expressed as G = {<e, r, e'>|e, e' in E, r in R}... A triple <e, r, e'> describes a factual knowledge

---

### 367. Entity ID and Type Assignment

Entities have two key attributes: unique identifier (entity ID) and type classification (entity type t). Examples like Country and Person show how abstract types categorize concrete instances.

**Sources**:

- **16-KG-Agent (Chunk 1:180-182)**
  > Each entity e is assigned a unique entity ID (or string value), and belongs to one entity type t such as Country and Person

---

### 368. Neighboring Relations Entity Pattern

Neighboring relations define the relational context of entities - both outgoing (entity as subject) and incoming (entity as object) edges. This captures how entities are embedded in a relational network.

**Sources**:

- **16-KG-Agent (Chunk 1:183-190)**
  > we introduce neighboring relations to denote both the incoming and outgoing relations for a set of entities {e}, denoted as R{e} = {r|<e, r, e'> in G} U {r|<e', r, e> in G}

---

### 369. Toolbox Entity Category

Tools are categorized into three entity types: extraction tools (access KG data), semantic tools (use pre-trained models), and logic tools (manipulate results). This tripartite classification enables structured agent-tool interaction.

**Sources**:

- **16-KG-Agent (Chunk 1:227-239)**
  > we construct a supporting toolbox for easing the utilization of KG information... we design three types of tools for LLMs reasoning over KG, i.e., extraction, semantic, and logic tools

---

### 370. Extraction Tool Entity Types

Extraction tools are specialized entity types: get_relation, get_head_entity, get_tail_entity, get_entity_by_type, get_entity_by_constraint. Each tool operates on specific entity types (relations, entities) with defined input-output signatures.

**Sources**:

- **16-KG-Agent (Chunk 1:241-249)**
  > Extraction tools aim to facilitate the access to information from KG... five tools to support the access to the relations (get_relation), the head/tail entities (get_head_entity/get_tail_entity)

---

### 371. Logic Tool Entity Types

Logic tools are operation-oriented entity types for KG manipulation: count, intersect, union, judge (condition verification), and end (terminal). These represent procedural entities that transform Data entities.

**Sources**:

- **16-KG-Agent (Chunk 1:251-255)**
  > Logic tools aim to support basic manipulation operations on the extracted KG information, including entity counting (count), entity set intersection (intersect) and union (union)

---

### 372. Semantic Tool Entity Types

Semantic tools leverage neural models for advanced operations: retrieve_relation (find relevant relations) and disambiguate_entity (resolve entity references). These bridge symbolic KG entities with neural representations.

**Sources**:

- **16-KG-Agent (Chunk 1:257-259)**
  > Semantic tools are developed by utilizing pre-trained models to implement specific functions, including relation retrieval (retrieve_relation) and entity disambiguation (disambiguate_entity)

---

### 373. Knowledge Memory Entity Structure

Knowledge memory is a composite entity type containing: question (Data), toolbox definition (Resource), current KG information (Data), and history reasoning program (Data). This defines the agent's working memory structure.

**Sources**:

- **16-KG-Agent (Chunk 1:537-551)**
  > The knowledge memory preserves the currently useful information... It mainly contains four parts: natural language question, toolbox definition, current KG information, and history reasoning program

---

### 374. Planner Entity Type

The Planner is defined as an Agent entity type that performs tool selection based on knowledge memory state. It generates function calls (action specifications) by choosing tools and their parameters.

**Sources**:

- **16-KG-Agent (Chunk 1:554-565)**
  > Based on the current knowledge memory, the LLM-based planner selects a tool to interact with KG at each step... the LLM will generate one function call by selecting a tool and its arguments

---

### 375. Executor Entity Type

Merged from 2 sources. The Executor is an Agent entity type that translates function calls into actual operations. It maintains state (caches intermediate variables) and produces results from KG queries, completing the plan-execute cycle.

**Sources**:

- **16-KG-Agent (Chunk 1:568-570)**
  > After the planner generates the function call, the KG-based executor will execute it using a program compiler. It can cache or operate the intermediate variables

- **19-GoT_Reasoning (Chunk 1:400-402)**
  > The Prompter prepares the prompts to be sent to the LLM. This module is responsible for the specifics of encoding the graph structure within the prompt

---

### 376. Agent Framework Four-Component Model

The KG-Agent architecture defines four core entity types: LLM-based planner (reasoning Agent), toolbox (Resource collection), executor (action Agent), and knowledge memory (Data store). This provides a complete agent system ontology.

**Sources**:

- **16-KG-Agent (Chunk 1:536-541)**
  > It mainly contains four components, i.e., the core instruction-tuned LLM (planner), the multifunctional toolbox, the KG-based executor, and the knowledge memory

---

### 377. Autonomous Iteration Pattern

Autonomous iteration defines a behavioral pattern where Agent entities cycle through: tool selection, execution, memory update, and termination check. This process is characterized as 'walking on the KG along relations'.

**Sources**:

- **16-KG-Agent (Chunk 1:629-638)**
  > The KG-Agent framework autonomously iterates the above tool selection and memory updation process... the multi-turn decision-making process of the agent is like walking on the KG along relations

---

### 378. Entity and Relation Embeddings

Entities and relations are core entity types in knowledge graphs, represented as vector embeddings that preserve semantic relationships in vector space.

**Sources**:

- **17-KG_Reasoning (Chunk 1:52-54)**
  > KG embedding, which represents entities and relations as vectors (embeddings) with their relationships reflected

---

### 379. Logic Rule Atoms

Atoms are the basic entity types in logical rules - head atoms and body atoms form the structure of inference rules for knowledge graph reasoning.

**Sources**:

- **17-KG_Reasoning (Chunk 1:79-85)**
  > One rule, which can be simply represented as B1 B2 ... Bn, means that the head atom H can be inferred H by the body atoms B1, ..., Bn

---

### 380. OWL Class Hierarchies

Classes and relations are core ontological entity types defined through OWL 2 schema, with class hierarchies providing structural organization.

**Sources**:

- **17-KG_Reasoning (Chunk 1:86-92)**
  > OWL 2 schema can be used to define class hierarchies, complex classes and relations, domain and range for relations

---

### 381. Entity Types in KG Schema

Entity types are fundamental categories in knowledge graphs, organized through class hierarchies where entities instantiate classes.

**Sources**:

- **17-KG_Reasoning (Chunk 1:200-202)**
  > Class hierarchies classify entity types, denoting entities as instantiations of classes

---

### 382. Relation Hierarchies

Relations form hierarchical structures through subsumption, creating taxonomic organization of relationship types in knowledge graphs.

**Sources**:

- **17-KG_Reasoning (Chunk 1:224-228)**
  > Relation hierarchies contain subsumption relationships between relations; for example, hasFather is a sub-relation of hasParents

---

### 383. Relation Properties

Relations have multiple typed properties including domain, range, asymmetry, composition, transitivity, reflexivity, and symmetry - defining the behavioral characteristics of relationships.

**Sources**:

- **17-KG_Reasoning (Chunk 1:237-250)**
  > Ontological schemas often define quite a few relation properties (and constraints)... domain and range of relations... Asymmetric relations... Composition... Transitive relations

---

### 384. Query Answering Entity Types

Entities and structured queries are interacting entity types in knowledge graph query answering tasks.

**Sources**:

- **17-KG_Reasoning (Chunk 1:359-365)**
  > Query answering returns correct entities in a KG as answers of a given structured query, where reasoning is usually considered for hidden answers

---

### 385. Logic Quantification Types

First-order logical operations (conjunction, disjunction, negation, difference) are entity types that structure complex queries over knowledge graphs.

**Sources**:

- **17-KG_Reasoning (Chunk 1:393-410)**
  > To support a complete set of first-order logical operations, including conjunction, disjunction and negation... further supports queries including Difference

---

### 386. LLM-Powered Intelligent Agent

Agent is the foundational entity type in LLM-powered multi-agent systems, possessing role, memory, and access to contextual resources as defining competencies.

**Sources**:

- **18-Multi-Agent_Taxonomy (Chunk 1:467-474)**
  > At the core of these systems, intelligent agents structure the system as the foundational components. Each agent is endowed with a unique set of competencies

---

### 387. Memory Entity Type

Memory is an entity type representing agent state - repository of experiences and knowledge that can manifest as textual records, structured databases, or embeddings.

**Sources**:

- **18-Multi-Agent_Taxonomy (Chunk 1:893-897)**
  > each agent is differentiated by its unique Role in the activity and possesses an individual Memory - a repository that encompasses condensed experiences and knowledge gained by the agent

---

### 388. Action Entity Type

Action is an entity type with multiple subtypes (DecomposeTask, CreateTask, DelegateTask, ExecuteTask, EvaluateResult, MergeResult) representing discrete operations performed by agents.

**Sources**:

- **18-Multi-Agent_Taxonomy (Chunk 2:34-49)**
  > the Agents execute different kinds of Actions which in sum aim at achieving the user-prompted Goal... DecomposeTask, Create Task, DelegateTask, ExecuteTask, EvaluateResult, MergeResult

---

### 389. Task-Management Agent Types

Task-Management Agents are specialized entity types including Task-Creation, Task-Prioritization, and Task-Execution agents that organize multi-agent workflows.

**Sources**:

- **18-Multi-Agent_Taxonomy (Chunk 1:902-913)**
  > Task-Management Agents: These agents are specialized in organizing the processes... Task-Creation Agent... Task-Prioritization Agent... Task-Execution Agent

---

### 390. Domain Role Agent Type

Domain Role Agents are entity types representing domain experts with specialized roles such as project manager, software architect, developer, or QA engineer.

**Sources**:

- **18-Multi-Agent_Taxonomy (Chunk 2:14-17)**
  > Domain Role Agents: These agents are domain-specific experts. They excel in specialized roles within the application domain... project manager, software architect, developer, or QA engineer

---

### 391. Technical Agent Type

Technical Agents are entity types specialized for technical platform integration, exemplified by SQL Agent for database interactions or Python Agent for script development.

**Sources**:

- **18-Multi-Agent_Taxonomy (Chunk 2:19-21)**
  > Technical Agents: These agents are tech-savvies, typically tasked with interfacing with technical platforms or development tools. Exemplary technical agents are represented by the SQL Agent

---

### 392. Foundation Model Entity Type

Foundation Model is an entity type categorized by modality: NLP Models (including LLMs), Computer Vision, Audio, and Multimodal models providing agent reasoning capabilities.

**Sources**:

- **18-Multi-Agent_Taxonomy (Chunk 2:150-166)**
  > Foundation Models refer to expansive machine learning models trained on vast amounts of data... NLP Models... Computer Vision Models... Audio Models... Multimodal Models

---

### 393. Agent Prompt Entity Type

Agent Prompt is an entity type representing the structured communication from agents to LLMs, triggering reasoning and response generation within actions.

**Sources**:

- **18-Multi-Agent_Taxonomy (Chunk 2:56-60)**
  > an Agent Prompt generated by an Agent and triggered within a certain Action is send to and then processed by the LLM, which generates a Response

---

### 394. Communication Protocol Entity Type

Communication Protocol is an entity type that structures inter-agent collaboration through predefined rules and mechanisms for message exchanges.

**Sources**:

- **18-Multi-Agent_Taxonomy (Chunk 2:75-84)**
  > A Communication Protocol provides a structured framework and methodology for agents' collaboration, guiding the execution of specific Actions by establishing rules and mechanisms

---

### 395. Artefact Entity Type

Artefact is an entity type representing tangible outputs including text, graphics, multimedia created or modified during task execution.

**Sources**:

- **18-Multi-Agent_Taxonomy (Chunk 1:879-881)**
  > This result might also include multiple Artefacts, encompassing text, graphics, multimedia, and more

---

### 396. Human User Entity Type

Human User is an entity type representing the external actor who initiates goals and provides alignment through prompts and preferences.

**Sources**:

- **18-Multi-Agent_Taxonomy (Chunk 1:848-850)**
  > Typically, a Human User initiates system operations via a User Prompt through the User Interface

---

### 397. Preference Entity Type

Preference is an entity type representing user-specified alignment parameters that refine goal execution and system behavior.

**Sources**:

- **18-Multi-Agent_Taxonomy (Chunk 2:189-191)**
  > The user-prompted Goal can be further refined pre-runtime through supplementary Preferences provided by the Human User via the User Interface

---

### 398. Activity Log Entity Type

Activity Log is an entity type for maintaining transparency by capturing all action details throughout task-management activity.

**Sources**:

- **18-Multi-Agent_Taxonomy (Chunk 1:871-873)**
  > each Task-Management Activity embodies an Activity Log and an Activity Memory. To maintain transparency and traceability of all Actions performed

---

### 399. Prompt Template Entity Type

Prompt Template is an entity type representing pre-prepared prompts that can be augmented and adapted for specific action types in agent workflows.

**Sources**:

- **18-Multi-Agent_Taxonomy (Chunk 2:66-68)**
  > chosen Prompt Templates prepared and/or adapted for certain kinds of actions. Such agent-driven prompt engineering is pivotal for LLM-powered multi-agent systems

---

### 400. Autonomy Level Entity Type

Autonomy is an entity type with levels (L0 Static, L1 Adaptive, L2 Self-Organizing) characterizing the degree of agent self-organization capability.

**Sources**:

- **18-Multi-Agent_Taxonomy (Chunk 2:303-315)**
  > The degree of autonomy refers to the extent to which an AI system can make decisions and act independently of rules and mechanisms defined by humans

---

### 401. Alignment Level Entity Type

Alignment is an entity type with levels (L0 Integrated, L1 User-Guided, L2 Real-Time Responsive) characterizing human influence over system behavior.

**Sources**:

- **18-Multi-Agent_Taxonomy (Chunk 2:362-370)**
  > alignment techniques can be seen as a detailed calibration of conditions tied to user-specified objectives or complex tasks. This includes preferences, policies, constraints, and boundaries

---

### 402. Task-Management Activity Entity Type

Task-Management Activity is an entity type comprising three phases (Decomposition, Orchestration, Synthesis) that structure goal accomplishment.

**Sources**:

- **18-Multi-Agent_Taxonomy (Chunk 1:857-858)**
  > Task decomposition is the first of three core phases within the Task-Management Activity: Decomposition... Orchestration... Synthesis

---

### 403. Thought Entity Type

Thought is the fundamental entity type in Graph of Thoughts - units of LLM-generated information modeled as vertices in a reasoning graph.

**Sources**:

- **19-GoT_Reasoning (Chunk 1:20-22)**
  > units of information ('LLM thoughts') are vertices, and edges correspond to dependencies between these vertices

---

### 404. Graph Structure for Reasoning

The reasoning process is modeled as entity types: Graph (overall structure), Vertices (thoughts/solutions), and Edges (dependencies between thoughts).

**Sources**:

- **19-GoT_Reasoning (Chunk 1:244-252)**
  > We model the reasoning process as a directed graph G = (V, E); V is a set of vertices and E is a set of edges. A vertex contains a solution to a problem at hand

---

### 405. Thought Classes

Thought classes are entity subtypes categorizing thoughts by function - e.g., plan thoughts vs. content thoughts in heterogeneous reasoning graphs.

**Sources**:

- **19-GoT_Reasoning (Chunk 1:253-259)**
  > In certain use cases, graph nodes belong to different classes. For example, in writing tasks, some vertices model plans of writing a paragraph, while other vertices model the actual paragraphs

---

### 406. Thought Transformation Types

Transformation is an entity type with subtypes: Aggregation (combining thoughts), Refining (modifying thought content), and Generation (creating new thoughts from existing ones).

**Sources**:

- **19-GoT_Reasoning (Chunk 1:306-365)**
  > GoT enables novel transformations of thoughts... Aggregation Transformations... Refining Transformations... Generation Transformations

---

### 407. Evaluator and Ranking Functions

Evaluator (E) and Ranking (R) are entity types representing functions for scoring individual thoughts and selecting top-ranked thoughts in reasoning.

**Sources**:

- **19-GoT_Reasoning (Chunk 1:370-374)**
  > Thoughts are scored to understand whether the current solution is good enough. A score is modeled as a general function E(v, G, p_theta). GoT can also rank thoughts... R(G, p_theta, h)

---

### 408. Controller Entity Type

Controller is an entity type coordinating reasoning, containing GoO (static operation graph) and GRS (dynamic reasoning state) as sub-entity types.

**Sources**:

- **19-GoT_Reasoning (Chunk 1:390-395)**
  > The Controller contains two further important elements: the Graph of Operations (GoO) and the Graph Reasoning State (GRS). GoO is a static structure that specifies the graph decomposition

---

### 409. Graph of Operations Entity Type

Graph of Operations (GoO) is an entity type representing static execution plans that prescribe thought transformations and their dependencies.

**Sources**:

- **19-GoT_Reasoning (Chunk 1:434-437)**
  > The user constructs a GoO instance, which prescribes the execution plan of thought operations. The GoO is a static structure that is constructed once, before the execution starts

---

### 410. Graph Reasoning State Entity Type

Graph Reasoning State (GRS) is an entity type maintaining dynamic execution state including operation progress, thought states, validity, and scores.

**Sources**:

- **19-GoT_Reasoning (Chunk 1:438-443)**
  > during the execution, an instance of the GRS maintains the continually updated information about the LLM reasoning process. This includes which operation has been executed so far, the states of all generated LLM thoughts

---

### 411. Volume Metric Entity Type

Volume is a metric entity type measuring the number of predecessor thoughts potentially contributing to a given thought through graph paths.

**Sources**:

- **19-GoT_Reasoning (Chunk 1:734-741)**
  > We define volume - for a given thought t - as the number of preceding LLM thoughts that could have impacted t. Formally, the volume of t is the number of thoughts from which there exists a path to t

---

