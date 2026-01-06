---
paper_id: "18-Multi-Agent_Architecture_Taxonomy_LLM"
title: "Balancing Autonomy and Alignment: A Multi-Dimensional Taxonomy for Autonomous LLM-Powered Multi-Agent Architectures"
authors:
  - "Thorsten Haendler"
year: 2023
chunks_expected: 4
chunks_read: 4
analysis_complete: true
schema_version: "2.3"

chunk_index:
  1:
    token_count: 11209
    fields_found:
      entity_types: true
      entity_definitions: true
      entity_relationships: true
      entity_count: partial
      abstraction_level: true
      framework_comparison: partial
      methodology: true
      ai_integration: true
      agent_modeling: true
      agentic_workflows: true
      generative_ai_patterns: true
      agent_ontology_integration: partial
      empirical_evidence: false
      limitations: partial
      tools_standards: true
  2:
    token_count: 14179
    fields_found:
      entity_types: true
      entity_definitions: true
      entity_relationships: true
      entity_count: true
      abstraction_level: true
      framework_comparison: false
      methodology: true
      ai_integration: true
      agent_modeling: true
      agentic_workflows: true
      generative_ai_patterns: true
      agent_ontology_integration: true
      empirical_evidence: false
      limitations: partial
      tools_standards: true
  3:
    token_count: 11293
    fields_found:
      entity_types: true
      entity_definitions: true
      entity_relationships: true
      entity_count: true
      abstraction_level: true
      framework_comparison: false
      methodology: true
      ai_integration: true
      agent_modeling: true
      agentic_workflows: true
      generative_ai_patterns: true
      agent_ontology_integration: true
      empirical_evidence: true
      limitations: partial
      tools_standards: false
  4:
    token_count: 10956
    fields_found:
      entity_types: partial
      entity_definitions: partial
      entity_relationships: partial
      entity_count: false
      abstraction_level: false
      framework_comparison: false
      methodology: partial
      ai_integration: true
      agent_modeling: true
      agentic_workflows: true
      generative_ai_patterns: true
      agent_ontology_integration: true
      empirical_evidence: true
      limitations: true
      tools_standards: false

entity_types:
  - item: "Agent"
    chunk: 1
    lines: "467-474"
    quote: "At the core of these systems, intelligent agents structure the system as the foundational components. Each agent is endowed with a unique set of competencies, which include a clearly defined role, an individual memory, as well as access to further contextual resources"
  - item: "Task"
    chunk: 1
    lines: "854-856"
    quote: "this user-prompted Goal (which might represent a directive, problem, question, or mission) undergoes decomposition into Tasks or Sub-Tasks to be manageable by the Agents"
  - item: "Goal"
    chunk: 1
    lines: "453-461"
    quote: "Goal-driven Task Management. Autonomous LLM-powered multi-agent systems are designed to accomplish user-prompted goals or complex tasks."
  - item: "Action"
    chunk: 2
    lines: "35-49"
    quote: "DecomposeTask: Breaking down a task into multiple sub-tasks... Create Task: Defining and generating new tasks... DelegateTask: Delegating a task to another agent... ExecuteTask: Actually executing a given task... EvaluateResult: Assessing the outcomes of a task... MergeResult: Integrating or combining two or more task results"
  - item: "Context"
    chunk: 2
    lines: "99-101"
    quote: "For executing the task-related actions, the LLM-powered agents are able to leverage specialized competencies and further information provided by additional Context which can be distinguished into Tools, Data, and Foundation Models"
  - item: "Tools"
    chunk: 2
    lines: "104-124"
    quote: "Tools in terms of contextual resources for multi-agent systems can be categorized into: Search and Analysis Tools, Execution Tools, Reasoning Tools, Development Tools, Communication Tools"
  - item: "Data"
    chunk: 2
    lines: "127-144"
    quote: "Data types in multi-agent architectures encompass: Structured Text Data, Unstructured Text Data, Multimodal Data, Domain-specific Data"
  - item: "Foundation Models"
    chunk: 2
    lines: "150-171"
    quote: "Foundation Models refer to expansive machine learning models trained on vast amounts of data. These models are versatile, suitable for addressing a variety of tasks across different modalities"
  - item: "Role"
    chunk: 1
    lines: "893-894"
    quote: "Each agent is differentiated by its unique Role in the activity and possesses an individual Memory"
  - item: "Memory"
    chunk: 1
    lines: "893-897"
    quote: "Each agent is differentiated by its unique Role in the activity and possesses an individual Memory - a repository that encompasses condensed experiences and knowledge gained by the agent"
  - item: "Communication Protocol"
    chunk: 2
    lines: "75-79"
    quote: "A Communication Protocol provides a structured framework and methodology for agents' collaboration, guiding the execution of specific Actions by establishing rules and mechanisms for message exchanges within the multi-agent network"
  - item: "Network"
    chunk: 1
    lines: "889-890"
    quote: "Within each Task-Management Activity, a set of intelligent Agents collaborate, forming a multi-agent Network"
  - item: "Task-Management Activity"
    chunk: 1
    lines: "856-868"
    quote: "Task decomposition is the first of three core phases within the Task-Management Activity: Decomposition, Orchestration, Synthesis"

entity_definitions:
  Agent: "At the core of these systems, intelligent agents structure the system as the foundational components. Each agent is endowed with a unique set of competencies, which include a clearly defined role, an individual memory, as well as access to further contextual resources, such as data, tools, or foundation models. The backbone of their reasoning and interpretative capabilities is rooted in the incorporation of large language models (LLMs). (Chunk 1:467-474)"
  Task: "User-prompted Goals undergo decomposition into Tasks or Sub-Tasks to be manageable by the Agents. These tasks can be interconnected in different ways, such as sequential tasks or graph tasks, which requires appropriate task prioritization. (Chunk 1:854-856)"
  Goal: "A directive, problem, question, or mission prompted by the user that the system aims to accomplish through task decomposition and agent collaboration. (Chunk 1:853-854)"
  Action: "Sub-types include DecomposeTask, CreateTask, DelegateTask, ExecuteTask, EvaluateResult, and MergeResult. Each Action can be part of another Action and can include multiple interactions with an LLM. (Chunk 2:35-58)"
  Context: "Contextual resources that agents leverage for executing task-related actions, distinguished into Tools, Data, and Foundation Models. (Chunk 2:99-101)"
  Role: "The unique function or responsibility that differentiates each agent within the activity. Domain Role Agents are domain-specific experts (e.g., project manager, software architect, developer, QA engineer). (Chunk 1:893, 914-917)"
  Memory: "A repository that encompasses condensed experiences and knowledge gained by the agent. Can manifest in multiple formats - textual records, structured databases, or embeddings. Includes short-term memory (compressed information via context window) and long-term memory (via vector databases). (Chunk 1:893-897)"
  Communication_Protocol: "A structured framework and methodology for agents' collaboration, guiding the execution of specific Actions by establishing rules and mechanisms for message exchanges within the multi-agent network. Three distinct protocols observed: strict finite processes, dialogue cycles, and multi-cycle process frameworks. (Chunk 2:75-93)"

entity_relationships:
  - relationship: "Agent executes Action"
    chunk: 2
    lines: "34-35"
    quote: "the Agents execute different kinds of Actions which in sum aim at achieving the user-prompted Goal"
  - relationship: "Goal decomposes-into Task"
    chunk: 1
    lines: "854-856"
    quote: "this user-prompted Goal undergoes decomposition into Tasks or Sub-Tasks to be manageable by the Agents"
  - relationship: "Agent has Role"
    chunk: 1
    lines: "893"
    quote: "Each agent is differentiated by its unique Role in the activity"
  - relationship: "Agent has Memory"
    chunk: 1
    lines: "893-894"
    quote: "Each agent is differentiated by its unique Role in the activity and possesses an individual Memory"
  - relationship: "Agent utilizes Context"
    chunk: 2
    lines: "99-101"
    quote: "For executing the task-related actions, the LLM-powered agents are able to leverage specialized competencies and further information provided by additional Context"
  - relationship: "Context contains Tools, Data, Foundation Models"
    chunk: 2
    lines: "99-101"
    quote: "Context which can be distinguished into Tools, Data, and Foundation Models"
  - relationship: "Action produces Task Result"
    chunk: 1
    lines: "892"
    quote: "each related to a certain Task and/or contributing to its Task Result"
  - relationship: "Task-Management Activity comprises Decomposition, Orchestration, Synthesis"
    chunk: 1
    lines: "860-868"
    quote: "Task decomposition is the first of three core phases within the Task-Management Activity: Decomposition, Orchestration, Synthesis"
  - relationship: "Agents form Network"
    chunk: 1
    lines: "889-890"
    quote: "Within each Task-Management Activity, a set of intelligent Agents collaborate, forming a multi-agent Network"
  - relationship: "Communication Protocol guides Action execution"
    chunk: 2
    lines: "75-77"
    quote: "A Communication Protocol provides a structured framework and methodology for agents' collaboration, guiding the execution of specific Actions"

abstraction_level: "Domain-level ontology for autonomous LLM-powered multi-agent systems. The paper presents a domain-ontology model represented as a UML class diagram structuring architectural concepts and their interrelations. The taxonomy operates at a high-level view, abstracting from technical details and specifics typical of individual systems to support clarity and accessibility. (Chunk 1:795-831)"

framework_comparison:
  - comparison: "Comparison to existing taxonomies for autonomous systems"
    chunk: 1
    lines: "243-266"
    quote: "Taxonomies for Autonomous Systems mainly categorize systems based on the level and type of autonomy, intelligence, learning capabilities, and ability to interact with their environment. These taxonomies, such as those by [94, 12, 44, 21, 78], are essential for understanding the spectrum of capabilities... However, while these taxonomies offer valuable insights into the capabilities and behaviors of autonomous systems, they don't inherently address the complexity and nuances involved when multiple agents powered by large language models are working together"
  - comparison: "Comparison to multi-agent system taxonomies"
    chunk: 1
    lines: "269-293"
    quote: "Taxonomies for Multi-Agent Systems extend beyond the confines of individual agent characteristics, integrating the dynamics of interactions and collaborations among multiple agents... While these taxonomies have contributed significantly to our understanding of communication protocols and agent constellation within multi-agent systems, they were developed prior to the advent of large language models (LLMs), and thus do not encapsulate the characteristic challenges associated with LLM-based multi-agent architectures"
  - comparison: "Orientation to Kruchten's 4+1 view model"
    chunk: 2
    lines: "641-643"
    quote: "For our taxonomy, we orient to Kruchten's renowned 4+1 view model of software architecture, an established standard viewpoint model for software architecture, adapting it to suit the architectural characteristics of LLM-powered multi-agent systems"

ai_integration:
  - pattern: "LLM-powered reasoning for agents"
    chunk: 1
    lines: "467-474"
    quote: "The backbone of their reasoning and interpretative capabilities is rooted in the incorporation of large language models (LLMs). This enables the agents not only to reflect upon the tasks or to plan and process the assigned tasks efficiently, but also to access and utilize contextual resources, as well as to communicate with other agents"
  - pattern: "Prompt-driven collaboration"
    chunk: 1
    lines: "477-480"
    quote: "While executing the assigned tasks, these specialized agents collaborate with each other via prompt-driven message exchanges to delegate responsibilities, seek assistance, or evaluate the results of tasks undertaken by their peers"
  - pattern: "Prompt Augmentation"
    chunk: 2
    lines: "59-68"
    quote: "Before the LLM receives the Agent Prompt, it may undergo Prompt Augmentation. This process can integrate additional specifics like the aspects or parts of the agent's Role or Memory, Context Information (e.g., data excerpts) acquired from previous Context Utilization, or chosen Prompt Templates"
  - pattern: "LLM as central controller"
    chunk: 3
    lines: "699-706"
    quote: "HUGGINGGPT follows a different strategy by leveraging the LLM as an autonomous controller that combines various multi-modal AI models to solve complex tasks... This singular central LLM-powered agent is autonomous in breaking down the goal or complex task into manageable tasks as well as in selecting, combining, and applying the appropriate models via prompting"

agent_modeling:
  - model: "Task-Management Agents"
    chunk: 1
    lines: "902-912"
    quote: "Task-Management Agents: These agents are specialized in organizing the processes related to the task-management activity. Includes Task-Creation Agent (generating new tasks), Task-Prioritization Agent (assigning urgency or importance), Task-Execution Agent (ensuring efficient task completion)"
  - model: "Domain Role Agents"
    chunk: 1
    lines: "914-917"
    quote: "Domain Role Agents: These agents are domain-specific experts. They excel in specialized roles within the application domain, collaborating with peer role agents when needed. Examples encompass roles in the software-development process, such as project manager, software architect, developer, or QA engineer"
  - model: "Technical Agents"
    chunk: 2
    lines: "19-21"
    quote: "Technical Agents: These agents are tech-savvies, typically tasked with interfacing with technical platforms or development tools. Exemplary technical agents are represented by the SQL Agent for database interactions or the Python Agent for developing Python scripts"
  - model: "Autonomy levels for agents"
    chunk: 2
    lines: "331-352"
    quote: "L0: Static Autonomy - systems are primarily automated, relying heavily on rules... L1: Adaptive Autonomy - systems possess the capability to adapt their behavior within a structure... L2: Self-Organizing Autonomy - LLM-powered agents emerge as the principal actors, capable of self-organization"

agentic_workflows:
  - workflow: "Divide and Conquer Strategy"
    chunk: 1
    lines: "63-71"
    quote: "Such systems tackle user-prompted goals by employing a divide & conquer strategy, by breaking them down into smaller manageable tasks. These tasks are then assigned to specialized agents, each equipped with a dedicated role and the reasoning capabilities of an LLM... the key to the systems' problem-solving capability lies in orchestrating the iterative collaboration"
  - workflow: "Task-Management Activity phases"
    chunk: 1
    lines: "860-868"
    quote: "Decomposition: Breaking down complex tasks into manageable Tasks and Sub-Tasks... Orchestration: Organizing the distribution and delegation of Tasks among suitable Agents... Synthesis: Evaluating and combining Task Results as well as finally presenting a unified Total Result"
  - workflow: "Strict finite processes"
    chunk: 2
    lines: "82-84"
    quote: "Strict finite processes or execution chains with predefined action sequences, interactions between predefined agents, and typically having a well-defined endpoint, which might represent the production of a specific output or artefact"
  - workflow: "Dialogue cycles"
    chunk: 2
    lines: "87-88"
    quote: "Dialogue cycles characterized by alternating DelegateTask and ExecuteTask actions between two agents, creating a feedback loop of instruction and execution"
  - workflow: "Multi-cycle process frameworks"
    chunk: 2
    lines: "91-92"
    quote: "Multi-cycle process frameworks with interactions between generic agent types, allowing for greater dynamism in agent interactions"

generative_ai_patterns:
  - pattern: "Slow thinking / deep reasoning"
    chunk: 1
    lines: "455-461"
    quote: "the system employs an interactive and multi-perspective strategy for problem solving, often referred to as deep reasoning or slow thinking enabled by the capabilities of large language models (LLMs)"
  - pattern: "Chain-of-thought via prompting"
    chunk: 1
    lines: "850-851"
    quote: "The prompts can be enriched with detailed instructions, exemplifications like reasoning sequences, role specifications, or output expectations"
  - pattern: "Agent-driven prompt engineering"
    chunk: 2
    lines: "67-68"
    quote: "Such agent-driven prompt engineering is pivotal for LLM-powered multi-agent systems"
  - pattern: "Reflection and planning"
    chunk: 2
    lines: "54-56"
    quote: "The LLM's reasoning capabilities are employed in multiple directions within an Action, such as for reflecting memories and instructions, observing existing results, planning steps and/or weighing options to proceed"
  - pattern: "Self-criticism and evaluation"
    chunk: 3
    lines: "651-654"
    quote: "Following the completion of each task, the agent evaluates the intermediate results, engaging in self-criticism. The tasks are optionally re-prioritized"

agent_ontology_integration:
  - integration: "Domain-ontology model as UML class diagram"
    chunk: 1
    lines: "795-797"
    quote: "Domain-ontology model represented as UML class diagram structuring selected architectural concepts and concept relations relevant for the domain of autonomous LLM-powered multi-agent systems"
  - integration: "Ontology for shared understanding"
    chunk: 1
    lines: "804-813"
    quote: "Domain ontologies, embraced across fields from philosophy to information systems, facilitate a shared understanding of domain-specific concepts. While they aid automated knowledge dissemination among software entities as formal ontologies, they are also devised as conceptual models to support human understanding of the addressed domain"
  - integration: "Conceptual model using UML2"
    chunk: 1
    lines: "816-820"
    quote: "Our domain ontology is represented as a conceptual model in terms of a class diagram of the Unified Modeling Language (UML2), which allows for organizing the identified concepts as classes and their relationships in terms of generalizations and kinds of associations with indicated multiplicities"

entity_count: 13

methodology: "Top-down theoretical approach combined with empirical system analysis. The domain-ontology model derives from an examination of the code and architectural documentation of several representative multi-agent architectures (AutoGPT, SuperAGI, MetaGPT, Generative Agents project, LangChain framework). Through an iterative process, the authors analyzed these systems to understand their components, interactions, and overarching structures to identify and abstract recurrent architectural characteristics. (Chunk 1:833-841)"

empirical_evidence:
  - evidence: "Classification of 7 LLM-powered multi-agent systems"
    chunk: 3
    lines: "282-289"
    quote: "We have chosen a set of seven state-of-the-art multi-agent systems for this assessment: AUTOGPT, BABYAGI, SUPERAGI, HUGGINGGPT, METAGPT, CAMEL, and AGENTGPT... For each selected system, we gathered relevant information by examining the technical documentation and research papers, where available, as well as reviewing the code base. We further engaged with each system to explore its real-time functionalities"
  - evidence: "Taxonomic assessment results"
    chunk: 3
    lines: "315-317"
    quote: "Assessment of autonomy (AU) and alignment (AL) levels across viewpoint-specific aspects of selected LLM-powered multi-agent systems"
  - evidence: "System comparison using radar charts"
    chunk: 3
    lines: "629-638"
    quote: "Radar charts illustrating the system profiles based on an assessment of architectural aspects in terms of autonomy (blue graph) and alignment (green dashed graph) levels"

limitations:
  - limitation: "LLM hallucination risks"
    chunk: 1
    lines: "52-60"
    quote: "LLMs also have inherent limitations... their outputs might seem plausible on the surface, but can be factually incorrect or even hallucinated. Moreover, despite their proficiency in handling vast amounts of textual information, LLMs struggle with maintaining consistent logic across extended chains of reasoning"
  - limitation: "Autonomy scope limitation"
    chunk: 4
    lines: "206-209"
    quote: "Within this, we reference high autonomy to the agents' self-organization capabilities for decision-making and further operational impact. However, it's essential to consider that autonomy can span beyond this definition, encompassing facets like an agent's ability for self-enhancement and proactive agency"
  - limitation: "Alignment scope limitation"
    chunk: 4
    lines: "211-215"
    quote: "The alignment dimension employed by the taxonomy reflects two key aspects, i.e., the origin of the alignment, and the moment of its communication to the system... However, one must note that this dimension does not reflect the quality, efficacy, or depth of the applied techniques"
  - limitation: "Lack of real-time alignment in current systems"
    chunk: 4
    lines: "158-163"
    quote: "The obvious lack of real-time adjustment capabilities can be seen founded in the nature of autonomous agent systems... The absence of user interaction and control during runtime restricts the potential for dynamic alignment"
  - limitation: "Prompt-driven collaboration robustness"
    chunk: 4
    lines: "134-139"
    quote: "Collaboration between LLM-powered agents basically relies on prompt-driven message exchange... This communication mechanism, founded on a sequence of prompts, heavily relies on the quality of LLM responses, which are susceptible to errors in terms of incorrect or hallucinated results"

tools_standards:
  - standard: "UML2 (Unified Modeling Language)"
    chunk: 1
    lines: "816-820"
    quote: "Our domain ontology is represented as a conceptual model in terms of a class diagram of the Unified Modeling Language (UML2)"
  - standard: "LangChain framework"
    chunk: 1
    lines: "347-352"
    quote: "Some of these recent multi-agent systems as well as further related projects are built upon the LANGCHAIN Python framework, which allows to realize the aforementioned interaction layer to define agents and chains of tasks"
  - standard: "Vector databases (Pinecone, Chroma)"
    chunk: 2
    lines: "134-136"
    quote: "For optimal processing by LLMs, unstructured text is typically stored in vector databases like PINECONE or CHROMA. These databases support semantic searches through vector embeddings"
  - standard: "Hugging Face platform"
    chunk: 2
    lines: "170-171"
    quote: "Platforms like HUGGING FACE even offer access to numerous models provided by the global machine learning community"
  - standard: "APIs for LLM and resource access"
    chunk: 2
    lines: "174-177"
    quote: "Access to LLMs, as well as associated resources such as tools, foundation models, and external data resources, is typically facilitated through Application Programming Interfaces (APIs)"
---

# Analysis Summary

## Paper Overview

This paper introduces a comprehensive multi-dimensional taxonomy for analyzing autonomous LLM-powered multi-agent systems, focusing on the dynamic interplay between autonomy and alignment across system architectures. The taxonomy employs a three-dimensional structure: levels of autonomy (L0-L2: Static, Adaptive, Self-Organizing), levels of alignment (L0-L2: Integrated, User-Guided, Real-Time Responsive), and four architectural viewpoints (Goal-driven Task Management, Agent Composition, Multi-Agent Collaboration, Context Interaction).

## Key Contributions to Ontology Research

### 1. Domain-Ontology Model (High Relevance)

The paper presents a domain-ontology model as a UML class diagram that structures the architectural concepts and relationships relevant to LLM-powered multi-agent systems. This model provides:

- **13 core entity types**: Agent, Task, Goal, Action, Context, Tools, Data, Foundation Models, Role, Memory, Communication Protocol, Network, Task-Management Activity
- **Clear entity definitions** with distinguishing characteristics
- **Explicit relationships** between entities (executes, decomposes-into, has, utilizes, contains, produces, comprises, guides)

### 2. Agent-Activity-Entity Triad Manifestation

The paper validates patterns similar to the Agent-Activity-Entity triad through:
- **Agent**: LLM-powered intelligent agents as autonomous actors
- **Activity**: Task-Management Activity with Decomposition, Orchestration, Synthesis phases
- **Entity**: Tasks, Goals, Results, Artefacts, Context (Tools, Data, Models)

### 3. Multi-Agent Architecture Patterns

Three distinct system categories identified:
1. **General-Purpose Systems** (AutoGPT, BabyAGI, SuperAGI, AgentGPT): Multi-cycle process frameworks with task-management agents
2. **Central LLM Controller** (HuggingGPT): Single controller combining multiple AI models
3. **Role-Agent Systems** (MetaGPT, CAMEL): Domain-specific role agents with direct collaboration

### 4. Agentic Workflow Patterns

Key workflow patterns documented:
- Divide and conquer strategy for goal decomposition
- Strict finite processes (execution chains)
- Dialogue cycles (instruction-execution feedback loops)
- Multi-cycle process frameworks

### 5. AI Integration Patterns

- LLM-powered reasoning for reflection, planning, and task processing
- Prompt-driven collaboration between agents
- Prompt augmentation with role, memory, and context information
- Agent-driven prompt engineering

## Relevance to 8-Entity Hypothesis

The paper's ontology provides partial grounding for the 8-entity hypothesis:

| Hypothesis Entity | Paper Mapping |
|-------------------|---------------|
| Goal | Goal (explicit) |
| Task | Task, Sub-Task (explicit) |
| Agent | Agent (explicit, with 3 subtypes) |
| Role | Role (explicit, as agent attribute) |
| Resource | Context (Tools, Data, Foundation Models) |
| Data | Data (explicit, 4 subtypes) |
| Event | Action (6 subtypes as events) |
| Rule | Communication Protocol, Alignment Techniques |

## Abstraction Level Analysis

The taxonomy operates at the **domain level**, providing a conceptual framework that:
- Abstracts from technical implementation details
- Enables comparison across different multi-agent systems
- Supports both automated knowledge dissemination and human understanding
- Maps 12 architectural aspects across 4 viewpoints, yielding 108 single configuration options

## Limitations Identified

1. Autonomy scope limited to self-organization capabilities (excludes self-enhancement)
2. Alignment dimension does not measure quality or efficacy of techniques
3. No performance benchmarks for efficiency, accuracy, or scalability
4. Current systems lack real-time responsive alignment options
5. Prompt-driven collaboration susceptible to LLM hallucination errors
