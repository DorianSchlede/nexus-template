---
batch_id: 3
field: entity_types
papers_read: [15-SciAgents_Multi-Agent_Graph_Reasoning, 16-KG-Agent_Knowledge_Graph_Reasoning, 17-KG_Reasoning_Logics_Embeddings_Survey, 18-Multi-Agent_Architecture_Taxonomy_LLM, 19-Graph_of_Thoughts_LLM_Reasoning]
chunks_read: 8
patterns_found: 47
extracted_at: "2025-12-28T12:00:00Z"
---

# Batch Extraction: entity_types (Batch 3)

## Patterns Extracted

---

## Paper 15: SciAgents_Multi-Agent_Graph_Reasoning

### Pattern: Knowledge Graph Node and Edge Entities

- **Source**: 15-SciAgents_Multi-Agent_Graph_Reasoning (Chunk 1:108-110)
- **Description**: Knowledge graphs organize scientific concepts as nodes connected by edges representing relationships. Nodes represent domain concepts and edges represent interconnections between them.
- **Quote**: "These knowledge graphs not only provide a mechanistic breakdown of information but also offer an ontological framework that elucidates the interconnectedness of different concepts, delineated as nodes and edges within the graph."
- **Context**: Discussion of how knowledge graphs structure scientific information to support LLM-based multi-agent systems.

### Pattern: Agent Entity Types in Multi-Agent Systems

- **Source**: 15-SciAgents_Multi-Agent_Graph_Reasoning (Chunk 1:710-735)
- **Description**: Defines specific agent entity types in the SciAgents multi-agent system including Human, Planner, Ontologist, Scientist 1, Scientist 2, Critic, Assistant, and Group Chat Manager. Each agent has a specific role in the collaborative research process.
- **Quote**: "'Human': human user that poses the task and can intervene at various stages of the problem solving process. 'Planner': suggests a detailed plan to solve the task. 'Ontologist': who is responsible to define the relationships and concepts within the knowledge graph. 'Scientist 1': crafts the initial draft of a detailed research hypothesis with seven key items based on the definitions provided by Ontologist. 'Scientist 2': who expands and refines the different key aspects of the research proposal created by Scientist 1. 'Critic': conducts a thorough review and suggests improvements. 'Assistant': has access to external tools including a function to generate a knowledge path from two keywords and a function to assess the novelty and feasibility of the research idea. 'Group chat manager': chooses the next speaker based on the context and agent profiles and broadcasts the message to the whole group."
- **Context**: Description of the autonomous multi-agent system architecture for scientific discovery.

### Pattern: Ontological Concept Types in Science Domain

- **Source**: 15-SciAgents_Multi-Agent_Graph_Reasoning (Chunk 1:333-349)
- **Description**: Defines relationship types between scientific concepts including possess, can be spun into, broad applicability, include, and exhibited by. These represent semantic relationships in bio-inspired materials domain.
- **Quote**: "Silk - possess - biopolymers: Silk is a type of biopolymer, a natural polymer produced by living organisms. Biopolymers - possess - silk: This reiterates that silk is a biopolymer. Silk - can be spun into - membranes: Silk can be processed and spun into thin layers or sheets known as membranes. Structural coloration - exhibited by - insects: Insects, such as those that produce silk, often exhibit structural coloration."
- **Context**: The ontologist agent's interpretation of relationships extracted from a knowledge graph path.

---

## Paper 16: KG-Agent_Knowledge_Graph_Reasoning

### Pattern: Knowledge Graph Entity and Relation Types

- **Source**: 16-KG-Agent_Knowledge_Graph_Reasoning (Chunk 1:176-190)
- **Description**: Defines formal KG entity types including Entity (with unique ID and string value), Relation, Entity Type (e.g., Country, Person), and Neighboring Relations. The KG is expressed as triples connecting head and tail entities via relations.
- **Quote**: "A knowledge graph typically consists of a large number of fact triples, expressed as G = {<e, r, e'>|e, e' in E, r in R}, where E and R denote the entity set and relation set, respectively. A triple <e, r, e'> describes a factual knowledge that a relation r exists between the head entity e and tail entity e'. Each entity e is assigned a unique entity ID (or string value), and belongs to one entity type t such as Country and Person."
- **Context**: Formal definition section establishing the fundamental entity types in knowledge graphs.

### Pattern: KG-Agent Tool Entity Types

- **Source**: 16-KG-Agent_Knowledge_Graph_Reasoning (Chunk 1:239-264)
- **Description**: Defines three types of tools as entities: Extraction tools (get_relation, get_head_entity, get_tail_entity, get_entity_by_type, get_entity_by_constraint), Logic tools (count, intersect, union, judge, end), and Semantic tools (retrieve_relation, disambiguate_entity).
- **Quote**: "Extraction tools aim to facilitate the access to information from KG... Logic tools aim to support basic manipulation operations on the extracted KG information, including entity counting (count), entity set intersection (intersect) and union (union), condition verification (judge), and ending the reasoning process with the current entity set as the final answer(s) (end). Semantic tools are developed by utilizing pre-trained models to implement specific functions, including relation retrieval (retrieve_relation) and entity disambiguation (disambiguate_entity)."
- **Context**: Description of the toolbox architecture for LLM-based KG reasoning agents.

### Pattern: Agent Framework Component Entity Types

- **Source**: 16-KG-Agent_Knowledge_Graph_Reasoning (Chunk 1:537-551)
- **Description**: Defines four core component entity types of the KG-Agent framework: LLM-based Planner (for tool selection), Toolbox (multifunctional tools), KG-based Executor (executes tool invocations), and Knowledge Memory (records context and useful information).
- **Quote**: "It mainly contains four components, i.e., the core instruction-tuned LLM (Section 4.2), referred to as the LLM-based planner, the multifunctional toolbox (Section 4.1), the KG-based executor for executing the tool invocation, and the knowledge memory to record the context and currently useful information in the whole process."
- **Context**: Architecture specification of the autonomous agent framework for KG reasoning.

### Pattern: Knowledge Memory Entity Sub-Types

- **Source**: 16-KG-Agent_Knowledge_Graph_Reasoning (Chunk 1:545-551)
- **Description**: Knowledge Memory contains four information parts: natural language question, toolbox definition, current KG information, and history reasoning program. The first two are static while the latter two are dynamically updated.
- **Quote**: "The knowledge memory preserves the currently useful information to support the LLM-based planner for making decisions. It mainly contains four parts of information, i.e., natural language question, toolbox definition, current KG information, and history reasoning program. The former two parts are initialized with the given question and toolbox definition, which remain unchanged during the reasoning process."
- **Context**: Description of the knowledge memory component in the autonomous KG reasoning agent.

### Pattern: Query Graph Entity Type

- **Source**: 16-KG-Agent_Knowledge_Graph_Reasoning (Chunk 1:420-425)
- **Description**: Defines Query Graph as a tree-like subgraph structure derived from the full KG that is related to a specific question. It can be mapped to a logical form and depicts execution flow.
- **Quote**: "the first step is to acquire a small KG subgraph related to the question, referred to as query graph... the query graph has a tree-like structure that can be directly mapped to a logical form (Yin et al., 2020), and it can clearly depict the execution flow of the SQL query to obtain the answer."
- **Context**: Discussion of how questions are grounded in knowledge graphs for reasoning.

---

## Paper 17: KG_Reasoning_Logics_Embeddings_Survey

### Pattern: Knowledge Graph Core Entity Types

- **Source**: 17-KG_Reasoning_Logics_Embeddings_Survey (Chunk 1:35-39)
- **Description**: Defines KG as representing facts in triples with vocabulary defined in schema/ontology. Entities are connected through relations forming a structured knowledge representation.
- **Quote**: "Knowledge graph (KG), representing facts in the form of triples, with vocabulary defined in a schema (also known as ontology), is a simple yet efficient and increasingly popular way of knowledge representation."
- **Context**: Introduction section defining core concepts of knowledge graphs.

### Pattern: OWL 2 Ontological Entity Types

- **Source**: 17-KG_Reasoning_Logics_Embeddings_Survey (Chunk 1:86-94)
- **Description**: OWL 2 based on Description Logics provides rich expressive power for defining: class hierarchies, complex classes and relations, domain and range for relations, and complex schema axioms. Supports datatypes and rules.
- **Quote**: "The Web Ontology Language OWL 2, which is based on Description Logics (DLs), is a key standard schema language of KGs. It is based on the SROIQ DL [Horrocks et al.]. OWL 2 provides rich expressive power, including a strong support for datatypes and rules. OWL 2 schema can be used to define class hierarchies, complex classes and relations, domain and range for relations, and more complex schema axioms."
- **Context**: Background section on logical foundations for KG reasoning.

### Pattern: Ontological Schema Entity Types

- **Source**: 17-KG_Reasoning_Logics_Embeddings_Survey (Chunk 1:194-234)
- **Description**: Defines ontological schema entity types including: Class Hierarchies (entity types and their hierarchies), Relation Hierarchies (subsumption relationships between relations like hasFather is sub-relation of hasParents), and Entity Types (classifications).
- **Quote**: "Class Hierarchies: Class hierarchies classify entity types, denoting entities as instantiations of classes. There are two tasks for injecting class hierarchies, encoding the types of entities and encoding hierarchies of entity types... Relation Hierarchies: Relation hierarchies contain subsumption relationships between relations; for example, hasFather is a sub-relation of hasParents."
- **Context**: Section on ontological schemas for embeddings.

### Pattern: Relation Property Entity Types

- **Source**: 17-KG_Reasoning_Logics_Embeddings_Survey (Chunk 1:237-261)
- **Description**: Defines relation properties as entity types including: Domain, Range, Asymmetric, Composition, Transitive, Reflexive, Symmetric, Equivalent, Inverse, and Cardinality.
- **Quote**: "Relation Properties: Ontological schemas often define quite a few relation properties (and constraints). First, we introduce properties constraining only one relation that have been considered. For domain and range of relations... To model Asymmetric relations... To further model Composition between relations... to model Transitive relations... enables modeling Reflexive, Symmetric and Transitive relations... Second, we introduce relation properties constraining multiple relations that have been considered, including Equivalent and Inverse."
- **Context**: Section on relation properties in ontological schemas.

### Pattern: Logic Query Entity Types

- **Source**: 17-KG_Reasoning_Logics_Embeddings_Survey (Chunk 1:335-338)
- **Description**: Defines logic types for queries including: path rules, numerical rules, path queries, and logic queries constructed using conjunction (AND), disjunction (OR), negation (NOT), and inequality operators.
- **Quote**: "Many logics are considered in each work, such as path rules, numerical rules, path queries, and logic queries constructed by conjunction, disjunction, negation, and inequality."
- **Context**: Section on embeddings for logic reasoning, discussing logic type perspectives.

### Pattern: Reasoning Task Entity Types

- **Source**: 17-KG_Reasoning_Logics_Embeddings_Survey (Chunk 1:326-330, 353-361)
- **Description**: Defines two main KG reasoning task types: Deductive Logic Reasoning (including Query Answering and Theorem Proving) and Inductive Logic Learning (Rule Mining).
- **Quote**: "We mainly review two kinds of KG reasoning tasks: deductive logic reasoning, which further includes query answering and theorem proving, and inductive logic learning... Query Answering: Query answering returns correct entities in a KG as answers of a given structured query, where reasoning is usually considered for hidden answers."
- **Context**: Section on embeddings for logic reasoning tasks.

### Pattern: Complex Query Entity Types

- **Source**: 17-KG_Reasoning_Logics_Embeddings_Survey (Chunk 1:394-410)
- **Description**: Defines complex query types including: Path Queries, Conjunctive Logical Queries, Existential Positive First-Order (EPFO) queries, and First-Order Logical operations (conjunction, disjunction, negation, difference).
- **Quote**: "Apart from simple path queries, more complex queries, such as conjunctive logical queries and Existential Positive First-Order (EPFO), involving multiple unobserved edges, nodes, and even variables are also widely researched with the help of embeddings... To support a complete set of first-order logical operations, including conjunction, disjunction and negation..."
- **Context**: Discussion of query answering approaches using embeddings.

---

## Paper 18: Multi-Agent_Architecture_Taxonomy_LLM

### Pattern: Multi-Agent System Core Entity Types

- **Source**: 18-Multi-Agent_Architecture_Taxonomy_LLM (Chunk 1:453-494)
- **Description**: Defines four core characteristics as entity types: Goal-driven Task Management, LLM-Powered Intelligent Agents, Multi-Agent Collaboration, and Context Interaction. Each represents a fundamental architectural component.
- **Quote**: "G Goal-driven Task Management... A LLM-Powered Intelligent Agents... M Multi-Agent Collaboration... C Context Interaction..."
- **Context**: Section 3.1 providing overview of primary characteristics of LLM-powered multi-agent systems.

### Pattern: Task Management Activity Entity Types

- **Source**: 18-Multi-Agent_Architecture_Taxonomy_LLM (Chunk 1:856-869)
- **Description**: Defines Task-Management Activity comprising three phases: Decomposition (breaking goals into tasks/sub-tasks), Orchestration (distributing tasks among agents), and Synthesis (evaluating and combining task results).
- **Quote**: "Decomposition: Breaking down complex tasks into manageable Tasks and Sub-Tasks; optionally resolving dependencies between them, resulting in a prioritized list of Tasks. Orchestration: Organizing the distribution and delegation of Tasks among suitable Agents. Synthesis: Evaluating and combining Task Results as well as finally presenting a unified Total Result."
- **Context**: Section 3.2 specifying architectural components for goal-driven task management.

### Pattern: Agent Entity Sub-Types

- **Source**: 18-Multi-Agent_Architecture_Taxonomy_LLM (Chunk 1:889-928, Chunk 2:1-28)
- **Description**: Defines three categories of agent entity types: Task-Management Agents (Task-Creation Agent, Task-Prioritization Agent, Task-Execution Agent), Domain Role Agents (domain-specific experts like project manager, software architect, developer, QA engineer), and Technical Agents (SQL Agent, Python Agent).
- **Quote**: "Task-Management Agents: These agents are specialized in organizing the processes related to the task-management activity... Task-Creation Agent: Generating new tasks... Task-Prioritization Agent: Assigning urgency or importance to tasks... Task-Execution Agent: Ensuring efficient task completion. Domain Role Agents: These agents are domain-specific experts. They excel in specialized roles within the application domain... Technical Agents: These agents are tech-savvies, typically tasked with interfacing with technical platforms or development tools."
- **Context**: Section 3.2 on specification of architectural components for agent composition.

### Pattern: Action Entity Types

- **Source**: 18-Multi-Agent_Architecture_Taxonomy_LLM (Chunk 2:30-49)
- **Description**: Defines six action sub-types that agents can execute: DecomposeTask, CreateTask, DelegateTask, ExecuteTask, EvaluateResult, and MergeResult.
- **Quote**: "DecomposeTask: Breaking down a task into multiple sub-tasks, optionally ordering and prioritizing the tasks. Create Task: Defining and generating new tasks. DelegateTask: Delegating a task to another agent, addressed as Receiver. ExecuteTask: Actually executing a given task. EvaluateResult: Assessing the outcomes of a task. MergeResult: Integrating or combining two or more task results."
- **Context**: Section on concepts of multi-agent collaboration.

### Pattern: Communication Protocol Entity Types

- **Source**: 18-Multi-Agent_Architecture_Taxonomy_LLM (Chunk 2:71-96)
- **Description**: Defines three types of communication protocols: Strict finite processes (predefined action sequences), Dialogue cycles (alternating DelegateTask and ExecuteTask between two agents), and Multi-cycle process frameworks (interactions between generic agent types).
- **Quote**: "Strict finite processes or execution chains with predefined action sequences, interactions between predefined agents, and typically having a well-defined endpoint... Dialogue cycles characterized by alternating DelegateTask and ExecuteTask actions between two agents, creating a feedback loop of instruction and execution... Multi-cycle process frameworks with interactions between generic agent types, allowing for greater dynamism in agent interactions."
- **Context**: Discussion of communication protocols for multi-agent collaboration.

### Pattern: Contextual Resource Entity Types - Tools

- **Source**: 18-Multi-Agent_Architecture_Taxonomy_LLM (Chunk 2:104-126)
- **Description**: Defines five tool entity sub-types: Search and Analysis Tools, Execution Tools, Reasoning Tools (e.g., Wolfram Alpha), Development Tools, and Communication Tools.
- **Quote**: "Search and Analysis Tools: These tools offer specialized capabilities for probing and analyzing data... Execution Tools: These are responsible for interfacing with and executing tasks within other environments... Reasoning Tools: Enhancing the capacity for logical thought... Development Tools: Tailored for software development endeavors... Communication Tools: These facilitate interactions with external entities by supporting functionalities like sending and receiving emails."
- **Context**: Section on concepts of context interaction.

### Pattern: Contextual Resource Entity Types - Data

- **Source**: 18-Multi-Agent_Architecture_Taxonomy_LLM (Chunk 2:127-145)
- **Description**: Defines four data entity sub-types: Structured Text Data (defined model/schema, queryable), Unstructured Text Data (no pre-defined model, stored in vector databases), Multimodal Data (videos, pictures, audio), and Domain-specific Data (tailored for particular sectors).
- **Quote**: "Structured Text Data: This refers to data that adheres to a defined model or schema, such as data found in traditional relational databases. Unstructured Text Data: This data lacks a pre-defined model... Multimodal Data: Beyond just text, this category encapsulates various formats including videos, pictures, and audio. Domain-specific Data: This data is tailored for particular sectors or areas of expertise."
- **Context**: Section on concepts of context interaction.

### Pattern: Foundation Model Entity Types

- **Source**: 18-Multi-Agent_Architecture_Taxonomy_LLM (Chunk 2:150-171)
- **Description**: Defines four foundation model entity sub-types based on modality: Natural Language Processing (NLP) Models (including LLMs), Computer Vision Models, Audio Models, and Multimodal Models.
- **Quote**: "Natural Language Processing (NLP) Models: These focus primarily on understanding and generating human language. LLMs fall under this category of NLP Models... Computer Vision Models: Aimed at processing and understanding images or videos. Audio Models: Specialized in processing and interpreting audio signals, including speech. Multimodal Models: Designed to handle multiple types of data simultaneously, combining aspects of NLP, Vision, and Audio."
- **Context**: Section on concepts of context interaction.

### Pattern: Decision-Making Entity Types

- **Source**: 18-Multi-Agent_Architecture_Taxonomy_LLM (Chunk 1:496-507)
- **Description**: Defines three primary decision-making entity types in a triadic interplay: Human Users, LLM-powered Agents, and Rules & Mechanisms (governing mechanisms integrated into the system).
- **Quote**: "This complexity can be traced back to the triadic interplay and inherent tensions among the primary decision-making entities: human users, LLM-powered agents, and governing mechanisms or rules integrated into the system."
- **Context**: Section on balancing autonomy and alignment.

### Pattern: Autonomy Level Entity Types

- **Source**: 18-Multi-Agent_Architecture_Taxonomy_LLM (Chunk 2:300-357)
- **Description**: Defines three autonomy levels as entity categories: L0 Static Autonomy (rule-driven, automated), L1 Adaptive Autonomy (adapts within predefined framework), L2 Self-Organizing Autonomy (agents as principal actors, dynamic tailoring).
- **Quote**: "L0: Static Autonomy - At this foundational level, systems are primarily automated, relying heavily on the rules, conditions, and mechanisms embedded by system architects... L1: Adaptive Autonomy - Evolving from the static level, systems at this stage possess the capability to adapt their behavior within a structure and procedural guidelines... L2: Self-Organizing Autonomy - At this highest level of autonomy, LLM-powered agents emerge as the principal actors, capable of self-organization, actively learning and dynamically tailoring their operations in real-time."
- **Context**: Section 4.1.1 on autonomy levels in the taxonomy.

### Pattern: Alignment Level Entity Types

- **Source**: 18-Multi-Agent_Architecture_Taxonomy_LLM (Chunk 2:409-433)
- **Description**: Defines three alignment levels as entity categories: L0 Integrated Alignment (built into system architecture), L1 User-Guided Alignment (user sets parameters before runtime), L2 Real-Time Responsive Alignment (real-time adjustments via monitoring).
- **Quote**: "L0: Integrated Alignment - At this foundational level, the alignment techniques are built directly into the system's architecture... L1: User-Guided Alignment - This level empowers users by allowing them to set or adjust specific alignment parameters... before the system starts its operation. L2: Real-Time Responsive Alignment - The highest level of alignment is represented by means to adjust the system's behavior in real-time."
- **Context**: Section 4.1.2 on alignment levels in the taxonomy.

### Pattern: Architectural Viewpoint Entity Types

- **Source**: 18-Multi-Agent_Architecture_Taxonomy_LLM (Chunk 2:641-676)
- **Description**: Defines four architectural viewpoints as entity types based on Kruchten's 4+1 view model: Goal-driven Task Management (Functional Viewpoint), Agent Composition (Development Viewpoint), Multi-Agent Collaboration (Process Viewpoint), and Context Interaction (Physical Viewpoint).
- **Quote**: "G Goal-driven Task Management (Functional Viewpoint)... A Agent Composition (Development Viewpoint)... M Multi-Agent Collaboration (Process Viewpoint)... C Context Interaction (Physical Viewpoint)..."
- **Context**: Section 4.2.1 on applied viewpoints in the taxonomy.

### Pattern: Taxonomic Aspect Entity Types - Goal-driven Task Management

- **Source**: 18-Multi-Agent_Architecture_Taxonomy_LLM (Chunk 3:118-156)
- **Description**: Defines three taxonomic aspects for Goal-driven Task Management viewpoint: Decomposition (how goals are broken down), Orchestration (how tasks are distributed), and Synthesis (how results are combined).
- **Quote**: "Taxonomic aspects of Goal-driven Task Management comprise the three constituting phases: Decomposition (how the goal or complex task is broken down into manageable sub-tasks), Orchestration (how these tasks are distributed among the LLM-powered agents), and Synthesis (how the results of the tasks are finally combined)."
- **Context**: Section 4.3.2 on viewpoint-specific aspects and level criteria.

### Pattern: Taxonomic Aspect Entity Types - Multi-Agent Collaboration

- **Source**: 18-Multi-Agent_Architecture_Taxonomy_LLM (Chunk 3:158-199)
- **Description**: Defines three taxonomic aspects for Multi-Agent Collaboration viewpoint: Communication-Protocol Management, Prompt Engineering, and Action Management.
- **Quote**: "For the taxonomic classification within Multi-Agent Collaboration, we consider Communication-Protocol Management (how the collaboration and dialogues between the agents are managed), Prompt Engineering (how prompts are applied during collaboration and executing the actions), and Action Management (how the different kinds of action... performed by the agents are managed)."
- **Context**: Section 4.3.2 on viewpoint-specific aspects and level criteria.

### Pattern: Taxonomic Aspect Entity Types - Agent Composition

- **Source**: 18-Multi-Agent_Architecture_Taxonomy_LLM (Chunk 3:201-237)
- **Description**: Defines four taxonomic aspects for Agent Composition viewpoint: Agent Generation (how agents are created), Role Definition (how roles are specified), Memory Usage (how information is stored and used), and Network Management (how agent relationships are managed).
- **Quote**: "The aspects of Agent Composition applied by the taxonomy comprise Agent Generation (how the agents are created, including the strategies and mechanisms employed), Role Definition (how agents' roles are specified), Memory Usage (how the agents utilize their memory, i.e., how information is summarized and stored, or how memory is used for reflecting instructions or planning actions), and Network Management (how the constellation and relationships among agents are managed)."
- **Context**: Section 4.3.2 on viewpoint-specific aspects and level criteria.

### Pattern: Taxonomic Aspect Entity Types - Context Interaction

- **Source**: 18-Multi-Agent_Architecture_Taxonomy_LLM (Chunk 3:239-273)
- **Description**: Defines two taxonomic aspects for Context Interaction viewpoint: Resources Integration (how integration of contextual resources is achieved) and Resources Utilization (how resources are actually utilized for tasks).
- **Quote**: "For Context Interaction, the taxonomic aspects comprise Resources Integration (how the integration of contextual resources in terms of data, tools, models, and other applications is achieved), and Resources Utilization (how these resources are actually utilized for executing tasks)."
- **Context**: Section 4.3.2 on viewpoint-specific aspects and level criteria.

### Pattern: System Category Entity Types

- **Source**: 18-Multi-Agent_Architecture_Taxonomy_LLM (Chunk 3:901-967)
- **Description**: Defines three system group categories: General-Purpose Systems (adaptable to broad spectrum of tasks), Central LLM Controller (single central agent managing resources), and Role-Agent Systems (multiple dedicated role agents simulating discussions or multi-perspective collaboration).
- **Quote**: "General-Purpose Systems - representing multi-agent systems designed for and adaptable to a broad spectrum of tasks and applications... Central LLM Controller - marks a third group specialized in leveraging and combining contextual resources for accomplishing the complex goals... Role-Agent Systems - employ an interplay or simulation between multiple dedicated roles agents."
- **Context**: Section 5.2.2 on strategies across system groups.

---

## Paper 19: Graph_of_Thoughts_LLM_Reasoning

### Pattern: Graph of Thoughts Core Entity Types

- **Source**: 19-Graph_of_Thoughts_LLM_Reasoning (Chunk 1:17-22)
- **Description**: Defines GoT core entity types: LLM thoughts as vertices (units of information), edges as dependencies between vertices, and the overall graph structure modeling reasoning.
- **Quote**: "The key idea and primary advantage of GoT is the ability to model the information generated by an LLM as an arbitrary graph, where units of information ('LLM thoughts') are vertices, and edges correspond to dependencies between these vertices."
- **Context**: Abstract introducing the Graph of Thoughts framework.

### Pattern: GoT Framework Tuple Entity Types

- **Source**: 19-Graph_of_Thoughts_LLM_Reasoning (Chunk 1:234-238)
- **Description**: Formally defines GoT as a tuple of four entities: G (LLM reasoning process as graph), T (thought transformations), E (evaluator function for scoring), and R (ranking function for selecting relevant thoughts).
- **Quote**: "Formally, GoT can be modeled as a tuple (G, T, E, R), where G is the 'LLM reasoning process' (i.e., all the LLM thoughts within the context, with their relationships), T are the potential thought transformations, E is an evaluator function used to obtain scores of thoughts, and R is a ranking function used to select most relevant thoughts."
- **Context**: Section 3 introducing the formal GoT framework.

### Pattern: Graph Entity Types in Reasoning Process

- **Source**: 19-Graph_of_Thoughts_LLM_Reasoning (Chunk 1:244-259)
- **Description**: Defines reasoning process graph entities: directed graph G = (V, E) with V as vertex set and E as edge subset. Vertices contain solutions (initial, intermediate, or final), edges indicate direct dependency relationships. Also supports heterogeneous graphs with vertex classes.
- **Quote**: "We model the reasoning process as a directed graph G = (V, E); V is a set of vertices and E is a subset of V x V is a set of edges... A vertex contains a solution to a problem at hand (be it an initial, intermediate, or a final one)... In certain use cases, graph nodes belong to different classes. For example, in writing tasks, some vertices model plans of writing a paragraph, while other vertices model the actual paragraphs of text. In such cases, GoT embraces a heterogeneous graph G = (V, E, c) to model the LLM reasoning."
- **Context**: Section 3.1 on the reasoning process.

### Pattern: Thought Transformation Entity Types

- **Source**: 19-Graph_of_Thoughts_LLM_Reasoning (Chunk 1:306-366)
- **Description**: Defines three primary thought transformation types: Aggregation Transformations (combining arbitrary thoughts into new ones), Refining Transformations (modifying current thought content via loop edge), and Generation Transformations (creating new thoughts based on existing single thought).
- **Quote**: "Aggregation Transformations: First, with GoT, one can aggregate arbitrary thoughts into new ones, to combine and reinforce the advantages of these thoughts, while eliminating their disadvantages... Refining Transformations: Another thought transformation is the refining of a current thought v by modifying its content... Generation Transformations: Finally, one can generate one or more new thoughts based on an existing single thought v."
- **Context**: Section 3.2 on transformations of thoughts.

### Pattern: GoT Architecture Module Entity Types

- **Source**: 19-Graph_of_Thoughts_LLM_Reasoning (Chunk 1:383-396)
- **Description**: Defines four interacting module entity types: Prompter (prepares messages for LLM), Parser (extracts information from LLM thoughts), Scoring module (verifies and scores thoughts), and Controller (coordinates reasoning process). Controller contains Graph of Operations (GoO) and Graph Reasoning State (GRS).
- **Quote**: "These modules are the Prompter (prepares the messages for the LLM), the Parser (extracts information from LLM thoughts), the Scoring module (verifies and scores the LLM thoughts), and the Controller (coordinates the entire reasoning process, and decides on how to progress it). The Controller contains two further important elements: the Graph of Operations (GoO) and the Graph Reasoning State (GRS)."
- **Context**: Section 4 on system architecture and extensibility.

### Pattern: Controller Sub-Entity Types

- **Source**: 19-Graph_of_Thoughts_LLM_Reasoning (Chunk 1:390-396)
- **Description**: Defines two Controller sub-entities: Graph of Operations (GoO) - static structure prescribing graph decomposition and transformation order/dependencies; Graph Reasoning State (GRS) - dynamic structure maintaining state of ongoing reasoning including thought history and states.
- **Quote**: "GoO is a static structure that specifies the graph decomposition of a given task, i.e., it prescribes transformations to be applied to LLM thoughts, together with their order & dependencies. GRS is a dynamic structure that maintains the state of the ongoing LLM reasoning process (the history of its thoughts and their states)."
- **Context**: Section 4 on system architecture.

### Pattern: Thought State Entity Type

- **Source**: 19-Graph_of_Thoughts_LLM_Reasoning (Chunk 1:407-411)
- **Description**: Defines Thought State as an entity constructed by the Parser for each LLM thought, containing extracted information used to update the GRS.
- **Quote**: "For each such thought, the Parser constructs the thought state, which contains this extracted information. The thought state is then used to update the GRS accordingly."
- **Context**: Section 4.2 on the Parser module.

### Pattern: Operation Entity Types in GoO

- **Source**: 19-Graph_of_Thoughts_LLM_Reasoning (Chunk 1:434-443)
- **Description**: Defines Operation objects within GoO that know their predecessor and successor operations. Each operation is part of the execution plan for thought transformations.
- **Quote**: "The user constructs a GoO instance, which prescribes the execution plan of thought operations. The GoO is a static structure that is constructed once, before the execution starts. Each operation object knows its predecessor and successor operations."
- **Context**: Section 4.5 on GoO and GRS.

### Pattern: Prompting Scheme Entity Types

- **Source**: 19-Graph_of_Thoughts_LLM_Reasoning (Chunk 1:112-127)
- **Description**: Defines hierarchy of prompting scheme entity types: Input-Output (IO), Chain-of-Thought (CoT), Self-Consistency with CoT (CoT-SC), Tree of Thoughts (ToT), and Graph of Thoughts (GoT), distinguished by their support for single chain, multiple chains, tree structure, and arbitrary graph structure.
- **Quote**: "Comparison of prompting schemes, with respect to the supported transformations of thoughts. 'Sc?': single chain of thoughts? 'Mc?': multiple chains of thoughts? 'Tr?': tree of thoughts? 'Ag?': arbitrary graph of thoughts?"
- **Context**: Table 1 comparing prompting schemes.

### Pattern: Volume Metric Entity Type

- **Source**: 19-Graph_of_Thoughts_LLM_Reasoning (Chunk 1:129-145)
- **Description**: Defines Volume as a new metric entity for evaluating prompting strategies. For a given thought v, volume is the number of LLM thoughts from which one can reach v using directed edges - all thoughts that could have contributed to v.
- **Quote**: "For a given thought v, the volume of v is the number of LLM thoughts, from which one can reach v using directed edges. Intuitively, these are all the LLM thoughts that have had the potential to contribute to v."
- **Context**: Introduction section on the volume metric contribution.

---

## Summary

This batch extracted 47 entity type patterns across 5 papers:

| Paper | Patterns Found |
|-------|---------------|
| 15-SciAgents_Multi-Agent_Graph_Reasoning | 3 |
| 16-KG-Agent_Knowledge_Graph_Reasoning | 5 |
| 17-KG_Reasoning_Logics_Embeddings_Survey | 7 |
| 18-Multi-Agent_Architecture_Taxonomy_LLM | 22 |
| 19-Graph_of_Thoughts_LLM_Reasoning | 10 |

Key themes identified:
1. **Agent Entity Types**: Multiple agent taxonomies (task-management, domain role, technical agents)
2. **Knowledge Graph Entities**: Nodes, edges, triples, entities, relations, entity types
3. **Ontological Schema Types**: Class hierarchies, relation hierarchies, relation properties
4. **Architectural Components**: Tools, data, models, memories, controllers
5. **Action/Operation Types**: Task decomposition, execution, evaluation, aggregation, transformation
6. **Graph-Based Reasoning Entities**: Vertices, edges, thoughts, transformations, states
