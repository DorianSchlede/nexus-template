---
batch_id: 2
field: agent_modeling
papers_read: [18-Multi-Agent_Architecture_Taxonomy_LLM, 20-Agentic_RAG_Survey, 23-UFO_Story_Ontological_Foundations, 31-BBO_BPMN_Ontology]
chunks_read: 8
patterns_found: 32
extracted_at: "2025-12-28T14:30:00Z"
---

# Batch Extraction: agent_modeling (Batch 2)

## Patterns Extracted

### Pattern: LLM-Powered Intelligent Agents as Foundational Components

- **Source**: 18-Multi-Agent_Architecture_Taxonomy_LLM (Chunk 1:467-474)
- **Description**: Intelligent agents are defined as the foundational structural components of multi-agent systems. Each agent is endowed with unique competencies including a clearly defined role, individual memory, and access to contextual resources. The reasoning capabilities are rooted in large language models (LLMs) which enable agents to reflect, plan, process tasks, access resources, and communicate with other agents.
- **Quote**: "At the core of these systems, intelligent agents structure the system as the foundational components. Each agent is endowed with a unique set of competencies, which include a clearly defined role, an individual memory, as well as access to further contextual resources, such as data, tools, or foundation models (see below), required for solving the tasks assigned to them. The backbone of their reasoning and interpretative capabilities is rooted in the incorporation of large language models (LLMs)."
- **Context**: This describes the core architecture concept for autonomous LLM-powered multi-agent systems, part of the characteristics overview section.

---

### Pattern: Agent as Decision-Making Entity in Triadic Interplay

- **Source**: 18-Multi-Agent_Architecture_Taxonomy_LLM (Chunk 1:496-506)
- **Description**: Agents are modeled as one of three primary decision-making entities in the system architecture, alongside human users and governing mechanisms/rules. Autonomy denotes agents' capacity for self-organized strategy and operation independent of predefined rules and human supervision. Alignment ensures system actions sync with human intentions and values.
- **Quote**: "This complexity can be traced back to the triadic interplay and inherent tensions among the primary decision-making entities: human users, LLM-powered agents, and governing mechanisms or rules integrated into the system. Alignment, in this context, ensures that the system's actions are in sync with human intentions and values. On the other side of the spectrum, autonomy denotes the agents' inherent capacity for self-organized strategy and operation, allowing them to function independent of predefined rules and mechanism and without human supervision."
- **Context**: This establishes the conceptual model for balancing autonomy and alignment in multi-agent systems.

---

### Pattern: Agent Type Taxonomy - Task Management, Domain Role, and Technical Agents

- **Source**: 18-Multi-Agent_Architecture_Taxonomy_LLM (Chunk 1:902-921)
- **Description**: Agents are classified into three distinct generic types based on their roles and functionalities within the collaborative network: Task-Management Agents (specialized in organizing processes), Domain Role Agents (domain-specific experts collaborating with peers), and Technical Agents (tech-savvy agents interfacing with platforms and tools).
- **Quote**: "Task-Management Agents: These agents are specialized in organizing the processes related to the task-management activity... Domain Role Agents: These agents are domain-specific experts. They excel in specialized roles within the application domain, collaborating with peer role agents when needed... Technical Agents: These agents are tech-savvies, typically tasked with interfacing with technical platforms or development tools."
- **Context**: This is part of the domain-ontology model specification, detailing how different agent types are conceptualized.

---

### Pattern: Task-Management Agent Sub-Types

- **Source**: 18-Multi-Agent_Architecture_Taxonomy_LLM (Chunk 2:6-12)
- **Description**: Task-Management Agents are further decomposed into three specialized sub-types: Task-Creation Agent (generating new tasks, including breaking down complex tasks), Task-Prioritization Agent (assigning urgency and resolving dependencies), and Task-Execution Agent (ensuring efficient task completion).
- **Quote**: "Task-Creation Agent: Generating new tasks, which optionally also includes deriving tasks by breaking down complex tasks. Task-Prioritization Agent: Assigning urgency or importance to tasks, which includes to resolve the dependencies between the tasks. Task-Execution Agent: Ensuring efficient task completion."
- **Context**: This provides a finer-grained taxonomy of agent types for task management activities.

---

### Pattern: Agent Memory Variability Pattern

- **Source**: 18-Multi-Agent_Architecture_Taxonomy_LLM (Chunk 2:24-27)
- **Description**: Agents vary in their reliance on memory. Some agents harness memory or action logs for reflecting or planning tasks, while others function without these recollections. Agents without memories are preferred for technical aspects or actions that demand an unprejudiced or unbiased lens.
- **Quote**: "An essential distinction to note is the variability in agent memory reliance. While some agents harness the power of memory or an action log, e.g., for reflecting or planning tasks, others function devoid of these recollections. Specifically, for technical aspects or actions that demand an unprejudiced or unbiased lens, agents without memories are often preferred."
- **Context**: This describes an architectural choice pattern for agent design based on memory usage.

---

### Pattern: Agent Action Type Taxonomy

- **Source**: 18-Multi-Agent_Architecture_Taxonomy_LLM (Chunk 2:35-49)
- **Description**: Agents execute different kinds of actions which are categorized into six sub-types: DecomposeTask, Create Task, DelegateTask (to a Receiver agent), ExecuteTask, EvaluateResult, and MergeResult. Each action can be part of another action and include multiple LLM interactions.
- **Quote**: "DecomposeTask: Breaking down a task into multiple sub-tasks, optionally ordering and prioritizing the tasks. Create Task: Defining and generating new tasks. DelegateTask: Delegating a task to another agent, addressed as Receiver. ExecuteTask: Actually executing a given task. EvaluateResult: Assessing the outcomes of a task. MergeResult: Integrating or combining two or more task results."
- **Context**: This defines the ontological categories of agent behaviors within multi-agent collaboration.

---

### Pattern: Agent Prompt-Driven Communication

- **Source**: 18-Multi-Agent_Architecture_Taxonomy_LLM (Chunk 2:56-68)
- **Description**: Agents interact through prompt-driven communication. An Agent Prompt is generated by an Agent, triggered within an Action, sent to and processed by the LLM, which generates a Response. Before receiving the prompt, it may undergo Prompt Augmentation integrating the agent's Role, Memory, Context Information, or Prompt Templates.
- **Quote**: "For this purpose, an Agent Prompt generated by an Agent and triggered within a certain Action is send to and then processed by the LLM, which generates a Response informing and/or guiding the next steps within the triggering action... Before the LLM receives the Agent Prompt, it may undergo Prompt Augmentation. This process can integrate additional specifics like the aspects or parts of the agent's Role or Memory, Context Information (e.g., data excerpts) acquired from previous Context Utilization, or chosen Prompt Templates."
- **Context**: This describes the communication mechanism between agents and LLMs.

---

### Pattern: Communication Protocol Patterns for Agent Collaboration

- **Source**: 18-Multi-Agent_Architecture_Taxonomy_LLM (Chunk 2:75-92)
- **Description**: Agent collaboration is governed by Communication Protocols that provide structured frameworks for message exchanges. Three distinct protocols are identified: Strict finite processes (predefined action sequences with endpoints), Dialogue cycles (alternating DelegateTask and ExecuteTask creating feedback loops), and Multi-cycle process frameworks (greater dynamism in agent interactions).
- **Quote**: "Strict finite processes or execution chains with predefined action sequences, interactions between predefined agents, and typically having a well-defined endpoint, which might represent the production of a specific output or artefact. Dialogue cycles characterized by alternating DelegateTask and ExecuteTask actions between two agents, creating a feedback loop of instruction and execution. Multi-cycle process frameworks with interactions between generic agent types, allowing for greater dynamism in agent interactions."
- **Context**: This establishes the communication protocol taxonomy for multi-agent collaboration.

---

### Pattern: Agent Autonomy Levels (Static, Adaptive, Self-Organizing)

- **Source**: 18-Multi-Agent_Architecture_Taxonomy_LLM (Chunk 2:300-352)
- **Description**: Agents are characterized by three levels of autonomy: L0 Static Autonomy (systems follow defined rules, agents cannot modify rules during runtime), L1 Adaptive Autonomy (agents can adjust operations within a framework established by architects), and L2 Self-Organizing Autonomy (agents as principal actors capable of self-organization, learning, and dynamic tailoring based on environmental cues).
- **Quote**: "L0: Static Autonomy - At this foundational level, systems are primarily automated, relying heavily on the rules, conditions, and mechanisms embedded by system architects... L1: Adaptive Autonomy - Evolving from the static level, systems at this stage possess the capability to adapt their behavior within a structure and procedural guidelines... L2: Self-Organizing Autonomy - At this highest level of autonomy, LLM-powered agents emerge as the principal actors, capable of self-organization, actively learning and dynamically tailoring their operations in real-time based on environmental cues and experiences."
- **Context**: This is the core taxonomy dimension for classifying agent behavior regarding autonomy.

---

### Pattern: Agent Role Definition Autonomy Pattern

- **Source**: 18-Multi-Agent_Architecture_Taxonomy_LLM (Chunk 3:201-236)
- **Description**: Agent roles can be defined at different autonomy levels: L0 (predefined and rule-driven roles and competencies), L1 (extensible competencies and modifiable roles within a framework), and L2 (agents autonomously define and generate types based on real-time needs). Alignment levels determine whether role constraints are embedded in design, configurable pre-runtime, or adjustable during operation.
- **Quote**: "Static Autonomy (L0): This level features a predefined and rule-driven composition and constellation of agents. Rules and mechanisms manage the creating of agents, select the agent types, and delineate their roles and competencies... Adaptive Autonomy (L1): While a system at this level provides predefined structures, it grants a degree of flexibility, permitting LLM-powered agents to adapt their composition and constellation... Self-Organizing Autonomy (L2): LLM-powered agents operating at this level exhibit the ability to autonomously define and generate types and establish collaborative networks."
- **Context**: This specifies the autonomy and alignment criteria for agent composition aspects.

---

### Pattern: Agent Network Management Pattern

- **Source**: 18-Multi-Agent_Architecture_Taxonomy_LLM (Chunk 3:207-208)
- **Description**: Network Management addresses how the constellation and relationships among agents are managed. This includes agent relationships, hierarchy structures, and communication topologies within the multi-agent network.
- **Quote**: "Network Management (how the constellation and relationships among agents are managed)"
- **Context**: Part of the Agent Composition viewpoint aspects in the taxonomic structure.

---

### Pattern: AI Agent Core Components Model

- **Source**: 20-Agentic_RAG_Survey (Chunk 1:484-501)
- **Description**: An AI agent comprises four essential components: LLM (with defined Role and Task) as the reasoning engine and dialogue interface, Memory (Short-Term and Long-Term) capturing context across interactions, Planning (Reflection and Self-Critique) guiding iterative reasoning, and Tools (Vector Search, Web Search, APIs) expanding capabilities beyond text generation.
- **Quote**: "In essence, an AI agent comprises: LLM (with defined Role and Task): Serves as the agent's primary reasoning engine and dialogue interface. It interprets user queries, generates responses, and maintains coherence. Memory (Short-Term and Long-Term): Captures context and relevant data across interactions. Short-term memory tracks immediate conversation state, while long-term memory stores accumulated knowledge and agent experiences. Planning (Reflection & Self-Critique): Guides the agent's iterative reasoning process through reflection, query routing, or self-critique, ensuring that complex tasks are broken down effectively. Tools (Vector Search, Web Search, APIs, etc.): Expands the agent's capabilities beyond text generation, enabling access to external resources, real-time data, or specialized computations."
- **Context**: This provides a formal component model for autonomous AI agents in the Agentic RAG paradigm.

---

### Pattern: Agentic Design Patterns (Reflection, Planning, Tool Use, Multi-Agent)

- **Source**: 20-Agentic_RAG_Survey (Chunk 1:507-509)
- **Description**: Agentic Patterns provide structured methodologies guiding agent behavior. Four key patterns underpin agentic workflows: Reflection, Planning, Tool Use, and Multi-Agent collaboration. These enable agents to dynamically adapt, plan, and collaborate for complex real-world tasks.
- **Quote**: "Agentic Patterns provide structured methodologies that guide the behavior of agents in Agentic Retrieval-Augmented Generation (RAG) systems. These patterns enable agents to dynamically adapt, plan, and collaborate, ensuring that the system can handle complex, real-world tasks with precision and scalability. Four key patterns underpin agentic workflows."
- **Context**: This establishes the foundational behavioral patterns for agent modeling in Agentic RAG systems.

---

### Pattern: Reflection Pattern for Iterative Self-Improvement

- **Source**: 20-Agentic_RAG_Survey (Chunk 1:515-531)
- **Description**: Reflection enables agents to iteratively evaluate and refine their outputs through self-feedback mechanisms. Agents identify and address errors, inconsistencies, and improvement areas. In multi-agent systems, Reflection can involve distinct roles where one agent generates outputs while another critiques them, fostering collaborative improvement.
- **Quote**: "Reflection is a foundational design pattern in agentic workflows, enabling agents to iteratively evaluate and refine their outputs. By incorporating self-feedback mechanisms, agents can identify and address errors, inconsistencies, and areas for improvement... In multi-agent systems, Reflection can involve distinct roles, such as one agent generating outputs while another critiques them, fostering collaborative improvement."
- **Context**: This describes a key behavioral pattern for agent self-improvement and quality assurance.

---

### Pattern: Planning Pattern for Autonomous Task Decomposition

- **Source**: 20-Agentic_RAG_Survey (Chunk 1:540-549)
- **Description**: Planning enables agents to autonomously decompose complex tasks into smaller, manageable subtasks. This capability is essential for multi-hop reasoning and iterative problem-solving. Agents dynamically determine the sequence of steps needed, ensuring flexibility in decision-making in dynamic and uncertain scenarios.
- **Quote**: "Planning is a key design pattern in agentic workflows that enables agents to autonomously decompose complex tasks into smaller, manageable subtasks. This capability is essential for multi-hop reasoning and iterative problem-solving in dynamic and uncertain scenarios. By leveraging planning, agents can dynamically determine the sequence of steps needed to accomplish a larger objective. This adaptability allows agents to handle tasks that cannot be predefined, ensuring flexibility in decision-making."
- **Context**: This describes how agents model task decomposition and execution planning.

---

### Pattern: Tool Use Pattern for Extended Agent Capabilities

- **Source**: 20-Agentic_RAG_Survey (Chunk 1:555-564)
- **Description**: Tool Use enables agents to extend capabilities by interacting with external tools, APIs, or computational resources. Agents gather information, perform computations, and manipulate data beyond pre-trained knowledge. Agents dynamically integrate tools and autonomously select and execute the most relevant tools for given tasks.
- **Quote**: "Tool Use enables agents to extend their capabilities by interacting with external tools, APIs, or computational resources. This pattern allows agents to gather information, perform computations, and manipulate data beyond their pre-trained knowledge. By dynamically integrating tools into workflows, agents can adapt to complex tasks and provide more accurate and contextually relevant outputs."
- **Context**: This describes how agents are modeled to interact with external resources.

---

### Pattern: Multi-Agent Collaboration for Task Specialization

- **Source**: 20-Agentic_RAG_Survey (Chunk 1:575-592)
- **Description**: Multi-agent collaboration enables task specialization and parallel processing. Agents communicate and share intermediate results ensuring workflow efficiency. Each agent operates with its own memory and workflow (including tools, reflection, or planning), enabling dynamic and collaborative problem-solving. Tasks are distributed among specialized agents.
- **Quote**: "Multi-agent collaboration is a key design pattern in agentic workflows that enables task specialization and parallel processing. Agents communicate and share intermediate results, ensuring the overall workflow remains efficient and coherent. By distributing subtasks among specialized agents, this pattern improves the scalability and adaptability of complex workflows... Each agent operates with its own memory and workflow, which can include the use of tools, reflection, or planning, enabling dynamic and collaborative problem-solving."
- **Context**: This describes the multi-agent collaboration model for distributed task execution.

---

### Pattern: Single-Agent Router Architecture

- **Source**: 20-Agentic_RAG_Survey (Chunk 1:755-758)
- **Description**: A Single-Agent serves as a centralized decision-making system where a single agent manages retrieval, routing, and information integration. This architecture consolidates tasks into one unified agent, making it effective for setups with limited tools or data sources.
- **Quote**: "A Single-Agent Agentic RAG: serves as a centralized decision-making system where a single agent manages the retrieval, routing, and integration of information. This architecture simplifies the system by consolidating these tasks into one unified agent, making it particularly effective for setups with a limited number of tools or data sources."
- **Context**: This describes a simplified agent architecture pattern for Agentic RAG.

---

### Pattern: Multi-Agent RAG with Specialized Retrieval Agents

- **Source**: 20-Agentic_RAG_Survey (Chunk 1:877-903)
- **Description**: Multi-Agent RAG distributes responsibilities across multiple specialized agents instead of relying on a single agent. A coordinator agent acts as central orchestrator, delegating queries to specialized retrieval agents. Each agent focuses on specific data sources or tasks (structured queries, semantic searches, real-time information, recommendations).
- **Quote**: "Multi-Agent RAG represents a modular and scalable evolution of single-agent architectures, designed to handle complex workflows and diverse query types by leveraging multiple specialized agents. Instead of relying on a single agent to manage all tasks—reasoning, retrieval, and response generation—this system distributes responsibilities across multiple agents, each optimized for a specific role or data source."
- **Context**: This describes the distributed multi-agent architecture for complex retrieval systems.

---

### Pattern: Agent Task Specialization and Modularity

- **Source**: 20-Agentic_RAG_Survey (Chunk 2:40-55)
- **Description**: Agents in multi-agent systems exhibit modularity and task specialization. Each agent operates independently, allowing seamless addition or removal. Each agent is optimized for a specific type of query or data source, improving accuracy and retrieval relevance. Tasks are distributed to minimize bottlenecks.
- **Quote**: "Modularity: Each agent operates independently, allowing for seamless addition or removal of agents based on system requirements. Scalability: Parallel processing by multiple agents enables the system to handle high query volumes efficiently. Task Specialization: Each agent is optimized for a specific type of query or data source, improving accuracy and retrieval relevance. Efficiency: By distributing tasks across specialized agents, the system minimizes bottlenecks and enhances performance for complex workflows."
- **Context**: This describes key architectural properties of multi-agent systems.

---

### Pattern: Hierarchical Agent Architecture with Tiered Decision-Making

- **Source**: 20-Agentic_RAG_Survey (Chunk 2:103-127)
- **Description**: Hierarchical agents employ a structured multi-tiered approach. Agents are organized in a hierarchy with higher-level agents overseeing and directing lower-level agents. Top-tier agents evaluate query complexity and delegate to subordinate agents. This enables multi-level decision-making and strategic prioritization.
- **Quote**: "Hierarchical Agentic RAG: systems employ a structured, multi-tiered approach to information retrieval and processing, enhancing both efficiency and strategic decision-making. Agents are organized in a hierarchy, with higher-level agents overseeing and directing lower-level agents. This structure enables multi-level decision-making, ensuring that queries are handled by the most appropriate resources."
- **Context**: This describes the hierarchical organization pattern for agent systems.

---

### Pattern: Corrective RAG Agent Roles

- **Source**: 20-Agentic_RAG_Survey (Chunk 2:226-244)
- **Description**: Corrective RAG systems define five specialized agent roles: Context Retrieval Agent (retrieves initial context), Relevance Evaluation Agent (assesses document relevance and flags for correction), Query Refinement Agent (rewrites queries for better retrieval), External Knowledge Retrieval Agent (performs web searches for additional data), and Response Synthesis Agent (synthesizes validated information into responses).
- **Quote**: "The Corrective RAG system is built on five key agents: Context Retrieval Agent: Responsible for retrieving initial context documents from a vector database. Relevance Evaluation Agent: Assesses the retrieved documents for relevance and flags any irrelevant or ambiguous documents for corrective actions. Query Refinement Agent: Rewrites queries to improve retrieval, leveraging semantic understanding to optimize results. External Knowledge Retrieval Agent: Performs web searches or accesses alternative data sources when the context documents are insufficient. Response Synthesis Agent: Synthesizes all validated information into a coherent and accurate response."
- **Context**: This provides a specific agent role taxonomy for self-correcting retrieval systems.

---

### Pattern: Adaptive Agent Strategy Selection

- **Source**: 20-Agentic_RAG_Survey (Chunk 2:317-328)
- **Description**: Adaptive RAG agents dynamically adjust query handling strategies based on complexity. A classifier assesses query complexity and determines the appropriate approach - from single-step retrieval to multi-step reasoning or bypassing retrieval altogether. This models agents as adaptive decision-makers.
- **Quote**: "Adaptive Retrieval-Augmented Generation (Adaptive RAG) enhances the flexibility and efficiency of large language models (LLMs) by dynamically adjusting query handling strategies based on the complexity of the incoming query. Unlike static retrieval workflows, Adaptive RAG employs a classifier to assess query complexity and determine the most appropriate approach, ranging from single-step retrieval to multi-step reasoning, or even bypassing retrieval altogether for straightforward queries."
- **Context**: This describes adaptive agent behavior based on task complexity assessment.

---

### Pattern: Graph-Based Agent Framework with Retriever Banks

- **Source**: 20-Agentic_RAG_Survey (Chunk 2:461-478)
- **Description**: Agent-G introduces an agentic architecture integrating graph knowledge bases with document retrieval. It employs modular retriever banks where specialized agents handle graph-based or unstructured data. A Critic Module validates retrieved data quality, and feedback loops refine retrieval and synthesis through iterative validation.
- **Quote**: "The core principle of Agent-G lies in its ability to dynamically assign retrieval tasks to specialized agents, leveraging both graph knowledge bases and textual documents. Agent-G adjusts its retrieval strategy as follows: Graph Knowledge Bases: Structured data is used to extract relationships, hierarchies, and connections... Critic Module: Evaluates the relevance and quality of retrieved information, ensuring alignment with the query. Feedback Loops: Refines retrieval and synthesis through iterative validation and re-querying."
- **Context**: This describes a specialized agent framework for graph-enhanced retrieval.

---

### Pattern: Agent-Based Retrieval with Autonomous Path Selection

- **Source**: 20-Agentic_RAG_Survey (Chunk 2:615-622)
- **Description**: GeAR employs an agent framework that utilizes graph expansion to manage retrieval tasks. Agents enable dynamic selection and combination of retrieval strategies based on query complexity. Agents can autonomously decide to utilize graph-expanded retrieval paths to improve relevance and accuracy.
- **Quote**: "Agent-Based Retrieval: Employs an agent framework to manage the retrieval process, enabling dynamic selection and combination of retrieval strategies based on the query's complexity. Agents can autonomously decide to utilize graph-expanded retrieval paths to improve the relevance and accuracy of retrieved information."
- **Context**: This describes autonomous agent decision-making for retrieval path selection.

---

### Pattern: Agentic Document Workflow Orchestration

- **Source**: 20-Agentic_RAG_Survey (Chunk 2:704-742)
- **Description**: Agentic Document Workflows extend RAG by enabling end-to-end knowledge work automation. Intelligent agents orchestrate complex document-centric processes, maintaining state across multi-step workflows and applying domain-specific logic. Agents coordinate document parsing, retrieval, reasoning, and structured outputs.
- **Quote**: "Agentic Document Workflows (ADW) extend traditional Retrieval-Augmented Generation (RAG) paradigms by enabling end-to-end knowledge work automation. These workflows orchestrate complex document-centric processes, integrating document parsing, retrieval, reasoning, and structured outputs with intelligent agents. ADW systems address limitations of Intelligent Document Processing (IDP) and RAG by maintaining state, coordinating multi-step workflows, and applying domain-specific logic to documents."
- **Context**: This describes agent roles in document processing automation.

---

### Pattern: UFO Four-Category Ontology for Agents

- **Source**: 23-UFO_Story_Ontological_Foundations (Chunk 1:126-136)
- **Description**: UFO adopts a Four-Category Ontology that countenances both individuals and universals, including substantial individuals/universals and accidents (particularized properties, moments, modes, tropes). This ontological foundation is essential for modeling entities including agents with particularized properties and relational qualities.
- **Quote**: "It was clear to us from the outset that we needed an ontological theory that would countenance both individuals and universals and one that would include not only substantial individuals and universals but also accidents (particularized properties, moments, qualities, modes, tropes, abstract particulars, aspects, ways) and accident universals. In other words, we needed a Four-Category Ontology."
- **Context**: This establishes the foundational ontological framework used in UFO for modeling entities.

---

### Pattern: UFO-C Ontology of Intentional and Social Entities

- **Source**: 23-UFO_Story_Ontological_Foundations (Chunk 1:191-193)
- **Description**: UFO-C provides an ontology of intentional and social entities built on UFO-A and UFO-B. It addresses notions such as Beliefs, Desires, Intentions, Goals, Actions, Commitments and Claims, Social Roles, and Social Particularized Relational Complexes (Social Relators) - key concepts for modeling intentional agents.
- **Quote**: "UFO-C: An Ontology of Intentional and Social Entities, which is constructed on top of UFO-A and UFO-B, and which addresses notions such as Beliefs, Desires, Intentions, Goals, Actions, Commitments and Claims, Social Roles and Social Particularized Relational Complexes (Social Relators), among others."
- **Context**: This describes the specific UFO layer for modeling intentional agents and their social aspects.

---

### Pattern: Role, Phase, and Mixin Type Distinctions for Agent Universals

- **Source**: 23-UFO_Story_Ontological_Foundations (Chunk 1:366-378)
- **Description**: UFO provides ontological distinctions for different sorts of universals: substance sortals (kinds), phased-sortals (roles and phases), and non-sortals (categories, mixins, role mixins). These distinctions apply not just to object universals but also to modes and relators, enabling rich modeling of agent types that can contingently instantiate anti-rigid types.
- **Quote**: "In the original version of UFO (and, hence, also in OntoUML), we had a number of ontological distinctions representing different sorts of universals. These include distinctions between substance sortals (kinds), phased-sortals (roles and phases) and non-sortals (categories, mixins and role mixins). These distinctions, however, were considered to be distinctions among object universals. However, consciously ignoring this rule, users of the language started to systematically employ these distinctions also when characterizing universals whose instances are existentially dependent endurants."
- **Context**: This describes the type hierarchy applicable to modeling agent roles and phases.

---

### Pattern: Agent as Human or Software Resource

- **Source**: 31-BBO_BPMN_Ontology (Chunk 1:346-353)
- **Description**: In BBO ontology, an Agent may be either a HumanResource or a SoftwareResource. The Job concept with subordinated/superior relations represents organizational hierarchy. Job is differentiated from Role for flexibility - persons with the same Job may have different authorization levels to execute Activities. Activities can be assigned directly to an Agent or indirectly via a Role.
- **Quote**: "An Agent may be a HumanResource or a SoftwareResource. The concept Job with the two relations 'subordinated' and 'superior' represent the organizational model of the company, which is not supported by BPMN meta-model. Note that, we differentiated Job from Role to offer more flexibility. Indeed, two persons that have the same Job, may have different authorization levels to execute Activities. For a given Activity, we may assign a specific Agent (i.e., direct assignment), or a Role (i.e., indirect assignment). In the case of indirect assignment, all agents playing the assigned role are potential performers of the Activity."
- **Context**: This describes the agent modeling pattern in BPMN-based business process ontology.

---

### Pattern: Agent Specification as Activity Performer

- **Source**: 31-BBO_BPMN_Ontology (Chunk 1:191-195)
- **Description**: Agent is identified as one of five main concepts in business process ontology. It represents the actor that performs a given process activity. Specifying who is responsible for the accomplishment of a given activity is considered essential for complete process representation.
- **Quote**: "Agent: the actor that performs a given process activity. Indeed, it is important to specify who is responsible for the accomplishment of a given activity."
- **Context**: This establishes agent as a core concept in business process modeling.

---

### Pattern: Resource vs Agent Semantic Distinction in BPMN

- **Source**: 31-BBO_BPMN_Ontology (Chunk 1:291-303)
- **Description**: In BPMN, the Resource concept has ambiguous semantics - sometimes covering all resource types, sometimes limited to agents responsible for performing work. BBO adopts the broader definition where Resource encompasses all types, and Agent becomes a subclass. This enables a resource taxonomy distinguishing material resources, human resources, software resources, etc.
- **Quote**: "The Resource concept exists in the BPMN meta-model. However, its semantics and definition are ambiguous. Indeed, on p. 95 of BPMN specification, the Resource class is supposed to cover all resource types. However, the definition of the relation that assigns resources to a process (p. 148) or an activity (p.152), limits the set of resources to the agents responsible for performing the work. The last definition seems to be most adopted. Indeed, in (Awad et al., 2009; Stroppi, Chiotti and Villarreal, 2011) Resource in BPMN is equivalent to Agents. In BBO, like in (Karray et al., 2012), we adopt the first definition of Resource, that englobes all resource types."
- **Context**: This describes the semantic modeling choice for agent/resource relationships.
