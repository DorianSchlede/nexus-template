---
batch_id: 1
field: agentic_workflows
papers_read: [15-SciAgents_Multi-Agent_Graph_Reasoning, 16-KG-Agent_Knowledge_Graph_Reasoning, 18-Multi-Agent_Architecture_Taxonomy_LLM, 19-Graph_of_Thoughts_LLM_Reasoning, 20-Agentic_RAG_Survey]
chunks_read: 9
patterns_found: 47
extracted_at: "2025-12-28T12:00:00Z"
---

# Batch Extraction: agentic_workflows (Batch 1)

## Patterns Extracted

### Pattern: Multi-Agent Research Proposal Generation System

- **Source**: 15-SciAgents_Multi-Agent_Graph_Reasoning (Chunk 4:894-906)
- **Description**: A multi-agent system architecture for scientific research proposal generation. The system comprises multiple specialized agents including: planner, assistant, ontologist, scientist, hypothesis_agent, outcome_agent, mechanism_agent, design_principles_agent, unexpected_properties_agent, comparison_agent, novelty_agent, and critic_agent. Each agent has a specific role in the research proposal development pipeline.
- **Quote**: "user: An attentive HUMAN user who can answer questions about the task, and can perform tasks such as running Python code or inputting command line commands at a Linux terminal and reporting back the execution results. planner: A planner who can suggest a plan to solve the task by breaking down the task into simpler sub-tasks. assistant: An assistant who calls the appropriate tools and functions and returns the results. ontologist: An ontologist who defines each of the terms and discusses the relationships in the path. scientist: A scientist who can craft the research proposal with key aspects based on the definitions and relationships acquired by the ontologist."
- **Context**: Part of the SciAgents system that uses knowledge graphs to generate research proposals through coordinated agent interactions.

### Pattern: Sequential Agent Workflow for Research Proposals

- **Source**: 15-SciAgents_Multi-Agent_Graph_Reasoning (Chunk 4:9-19)
- **Description**: A five-phase sequential workflow where specialized agents process a research proposal in order: (1) Define Terms and Relationships by ontologist, (2) Craft Research Proposal by scientist, (3) Expand Key Aspects by specialized agents, (4) Critique and Improve by critic_agent, (5) Rate Novelty and Feasibility by assistant calling evaluation functions.
- **Quote**: "1. **Define Terms and Relationships** : The ontologist will define each term in the knowledge path and discuss the relationships between them. 2. **Craft the Research Proposal** : The scientist will craft a research proposal based on the definitions and relationships provided by the ontologist. 3. **Expand Key Aspects** : Each specialized agent (hypothesis_agent, outcome_agent, mechanism_agent, design_principles_agent, unexpected_properties_agent, comparison_agent, novelty_agent) will expand on their respective sections of the research proposal. 4. **Critique and Improve** : The critic_agent will summarize, critique, and suggest improvements to the research proposal. 5. **Rate Novelty and Feasibility** : Finally, the assistant will call the appropriate function to rate the novelty and feasibility of the research idea."
- **Context**: Defines the orchestration pattern for how multiple agents collaborate on a single task through sequential handoffs.

### Pattern: Specialized Aspect-Expansion Agents

- **Source**: 15-SciAgents_Multi-Agent_Graph_Reasoning (Chunk 4:3-6)
- **Description**: Specialized agents that each expand on one specific aspect of a research proposal. Each agent focuses on a single domain: hypothesis, outcome, mechanism, design principles, unexpected properties, comparison, and novelty. The critic_agent provides final summarization and improvement suggestions.
- **Quote**: "design_principle aspect of the research proposal crafted by the 'scientist'. unexpected_properties_agent: unexpected_properties_agent who can expand the 'unexpected_properties' aspect of the research proposal crafted by the 'scientist'. comparison_agent: comparison_agent who can expand the 'comparison' aspect of the research proposal crafted by the 'scientist'. novelty_agent: novelty_agent who can expand the 'novelty' aspect of the research proposal crafted by the 'scientist'. critic_agent: Summarizes, critiques, and suggests improvements after all seven aspects of the proposal have been expanded by the agents."
- **Context**: Part of a divide-and-conquer approach where complex tasks are decomposed into specialized subtasks handled by domain-specific agents.

### Pattern: Function Calling Tool Integration

- **Source**: 15-SciAgents_Multi-Agent_Graph_Reasoning (Chunk 4:73)
- **Description**: Integration of function calling capabilities where the assistant agent can invoke specific tools like rate_novelty_feasibility to perform evaluations. This demonstrates tool use as a core agentic pattern.
- **Quote**: "The assistant will call the functions.rate_novelty_feasibility function to rate the research idea."
- **Context**: Shows how agents can leverage external tools and functions to extend their capabilities beyond pure language generation.

### Pattern: Knowledge Path-Based Agent Workflow

- **Source**: 15-SciAgents_Multi-Agent_Graph_Reasoning (Chunk 3:884-891)
- **Description**: Agents use knowledge graph paths as input to guide research proposal generation. The knowledge path describes relationships between concepts that the agents explore and expand upon.
- **Quote**: "silk -- provide functionalities -- biological materials -- can be integrated -- novel functionalities -- can be integrated -- biological materials -- uses for creating -- low-temperature processing -- uses for creating -- biological materials -- have -- multi-scale organization -- have -- biological materials -- provide functionalities -- dandelion -- provide functionalities -- biological materials -- can guide nanoscale organization via -- pigments -- do not use -- insects -- are -- energy-intensive"
- **Context**: Demonstrates how structured knowledge representations guide multi-agent workflows in scientific discovery.

### Pattern: Autonomous LLM-Based Agent Framework for KG Reasoning

- **Source**: 16-KG-Agent_Knowledge_Graph_Reasoning (Chunk 1:19-39)
- **Description**: KG-Agent is an autonomous agent framework enabling small LLMs to actively make decisions during reasoning over knowledge graphs. It integrates LLM, multifunctional toolbox, KG-based executor, and knowledge memory with an iteration mechanism for autonomous tool selection and memory updating.
- **Quote**: "we propose an autonomous LLM-based agent framework, called KG-Agent, which enables a small LLM to actively make decisions until finishing the reasoning process over KGs. In KG-Agent, we integrate the LLM, multifunctional toolbox, KG-based executor, and knowledge memory, and develop an iteration mechanism that autonomously selects the tool then updates the memory for reasoning over KG."
- **Context**: Addresses limitations of pre-defined interaction mechanisms between LLMs and KGs by enabling autonomous decision-making.

### Pattern: Three-Category Toolbox for KG Operations

- **Source**: 16-KG-Agent_Knowledge_Graph_Reasoning (Chunk 1:239-264)
- **Description**: A toolbox organized into three categories supporting KG reasoning: (1) Extraction tools for accessing KG information (get_relation, get_head_entity, get_tail_entity, get_entity_by_type, get_entity_by_constraint), (2) Logic tools for manipulation operations (count, intersect, union, judge, end), (3) Semantic tools using pre-trained models (retrieve_relation, disambiguate_entity).
- **Quote**: "Extraction tools aim to facilitate the access to information from KG... Logic tools aim to support basic manipulation operations on the extracted KG information, including entity counting (count), entity set intersection (intersect) and union (union), condition verification (judge), and ending the reasoning process with the current entity set as the final answer(s) (end). Semantic tools are developed by utilizing pre-trained models to implement specific functions, including relation retrieval (retrieve_relation) and entity disambiguation (disambiguate_entity)."
- **Context**: Demonstrates a systematic approach to extending LLM capabilities through specialized tool categories.

### Pattern: Code-Based Instruction Tuning for Agents

- **Source**: 16-KG-Agent_Knowledge_Graph_Reasoning (Chunk 1:99-106)
- **Description**: Using program language to formulate multi-hop reasoning processes and synthesizing code-based instruction datasets to fine-tune base LLMs for autonomous reasoning capabilities.
- **Quote**: "we leverage program language to formulate the multi-hop reasoning process over the KG, and synthesize a code-based instruction dataset to fine-tune the base LLM."
- **Context**: Shows how agents can be trained using code-structured data to improve reasoning over structured knowledge.

### Pattern: Knowledge Memory for Agent State Management

- **Source**: 16-KG-Agent_Knowledge_Graph_Reasoning (Chunk 1:546-551)
- **Description**: Knowledge memory maintains currently useful information for agent decision-making, containing four parts: natural language question, toolbox definition, current KG information, and history reasoning program. The first two remain unchanged while the latter two update at each reasoning step.
- **Quote**: "The knowledge memory preserves the currently useful information to support the LLM-based planner for making decisions. It mainly contains four parts of information, i.e., natural language question, toolbox definition, current KG information, and history reasoning program. The former two parts are initialized with the given question and toolbox definition, which remain unchanged during the reasoning process. The later two parts are initialized as an empty list, which will be constantly updated at each step after LLM generating the function call and executor invoking the corresponding tool."
- **Context**: Critical for maintaining context across iterative reasoning steps in autonomous agents.

### Pattern: Autonomous Iteration Mechanism

- **Source**: 16-KG-Agent_Knowledge_Graph_Reasoning (Chunk 1:629-638)
- **Description**: An iterative mechanism where the agent autonomously performs tool selection and memory updation in cycles until reaching answer entities. The process walks on the KG along relations through multi-turn decision-making.
- **Quote**: "The KG-Agent framework autonomously iterates the above tool selection and memory updation process to perform step-by-step reasoning, where the knowledge memory is used to maintain the accessed information from KG. In this way, the multi-turn decision-making process of the agent is like walking on the KG along relations. Once reaching the answer entities, the agent will automatically stop the iterative process."
- **Context**: Describes the core loop of autonomous agent operation without human intervention.

### Pattern: Planner-Executor Architecture

- **Source**: 16-KG-Agent_Knowledge_Graph_Reasoning (Chunk 1:537-551)
- **Description**: A two-component architecture where an LLM-based planner selects tools based on knowledge memory, and a KG-based executor executes tool invocations and updates memory. The planner addresses four task types: entity linking, KG information access, intermediate result processing, and final answer return.
- **Quote**: "the LLM-based planner selects a tool to interact with KG at each step... Generally, the planner needs to invoke tools from the pre-defined toolbox to address four types of task requirements, i.e., linking the mentioned entity to KG... accessing the KG information... processing the intermediate results... or returning the final answer to end the reasoning process"
- **Context**: Shows separation of concerns between planning/decision-making and execution components.

### Pattern: Task Management Agent Roles

- **Source**: 18-Multi-Agent_Architecture_Taxonomy_LLM (Chunk 2:6-17)
- **Description**: Three specialized agent roles for task management: Task-Creation Agent (generating and breaking down tasks), Task-Prioritization Agent (assigning urgency and resolving dependencies), and Task-Execution Agent (ensuring efficient completion). Additionally, Domain Role Agents handle specialized roles and Technical Agents interface with platforms/tools.
- **Quote**: "Task-Creation Agent: Generating new tasks, which optionally also includes deriving tasks by breaking down complex tasks. Task-Prioritization Agent: Assigning urgency or importance to tasks, which includes to resolve the dependencies between the tasks. Task-Execution Agent: Ensuring efficient task completion. Domain Role Agents: These agents are domain-specific experts. They excel in specialized roles within the application domain, collaborating with peer role agents when needed. Technical Agents: These agents are tech-savvies, typically tasked with interfacing with technical platforms or development tools."
- **Context**: Taxonomy of agent types in LLM-powered multi-agent systems for software development and task automation.

### Pattern: Multi-Agent Action Types

- **Source**: 18-Multi-Agent_Architecture_Taxonomy_LLM (Chunk 2:30-49)
- **Description**: Six distinct action types performed by agents in multi-agent collaboration: DecomposeTask (breaking down tasks), CreateTask (generating new tasks), DelegateTask (assigning to other agents), ExecuteTask (performing tasks), EvaluateResult (assessing outcomes), MergeResult (combining results).
- **Quote**: "DecomposeTask: Breaking down a task into multiple sub-tasks, optionally ordering and prioritizing the tasks. Create Task: Defining and generating new tasks. DelegateTask: Delegating a task to another agent, addressed as Receiver. ExecuteTask: Actually executing a given task. EvaluateResult: Assessing the outcomes of a task. MergeResult: Integrating or combining two or more task results."
- **Context**: Defines the vocabulary of agent actions in collaborative workflows.

### Pattern: Communication Protocol Types

- **Source**: 18-Multi-Agent_Architecture_Taxonomy_LLM (Chunk 2:71-92)
- **Description**: Three types of communication protocols for multi-agent collaboration: (1) Strict finite processes with predefined action sequences, (2) Dialogue cycles with alternating DelegateTask and ExecuteTask actions between two agents, (3) Multi-cycle process frameworks with dynamic interactions between generic agent types.
- **Quote**: "Strict finite processes or execution chains with predefined action sequences, interactions between predefined agents, and typically having a well-defined endpoint, which might represent the production of a specific output or artefact. Dialogue cycles characterized by alternating DelegateTask and ExecuteTask actions between two agents, creating a feedback loop of instruction and execution. Multi-cycle process frameworks with interactions between generic agent types, allowing for greater dynamism in agent interactions."
- **Context**: Describes patterns for structuring inter-agent communication and task handoffs.

### Pattern: Prompt Augmentation in Agent Actions

- **Source**: 18-Multi-Agent_Architecture_Taxonomy_LLM (Chunk 2:56-68)
- **Description**: Agent prompts undergo augmentation before being processed by the LLM, integrating additional specifics like agent role, memory, context information, or prompt templates. This agent-driven prompt engineering is pivotal for LLM-powered multi-agent systems.
- **Quote**: "Before the LLM receives the Agent Prompt, it may undergo Prompt Augmentation. This process can integrate additional specifics like the aspects or parts of the agent's Role or Memory, Context Information (e.g., data excerpts) acquired from previous Context Utilization, or chosen Prompt Templates prepared and/or adapted for certain kinds of actions. Such agent-driven prompt engineering is pivotal for LLM-powered multi-agent systems."
- **Context**: Describes how agents enhance their LLM interactions through dynamic prompt construction.

### Pattern: Context Resource Categories

- **Source**: 18-Multi-Agent_Architecture_Taxonomy_LLM (Chunk 2:99-144)
- **Description**: Five categories of tools available to agents: Search and Analysis Tools (probing and analyzing data), Execution Tools (interfacing with environments), Reasoning Tools (computational intelligence like Wolfram Alpha), Development Tools (coding and debugging), Communication Tools (external interactions like email). Data types include Structured Text, Unstructured Text, Multimodal Data, and Domain-specific Data.
- **Quote**: "Search and Analysis Tools: These tools offer specialized capabilities for probing and analyzing data... Execution Tools: These are responsible for interfacing with and executing tasks within other environments... Reasoning Tools: Enhancing the capacity for logical thought, these tools bolster reasoning capabilities in specialized areas such as computational intelligence. For instance, platforms like WOLFRAM ALPHA empower agents with advanced computational skills. Development Tools: Tailored for software development endeavors... Communication Tools: These facilitate interactions with external entities"
- **Context**: Comprehensive taxonomy of contextual resources available to agents in multi-agent architectures.

### Pattern: Autonomy-Alignment Matrix

- **Source**: 18-Multi-Agent_Architecture_Taxonomy_LLM (Chunk 2:269-297)
- **Description**: A three-dimensional matrix for classifying multi-agent systems combining autonomy levels (L0 Static, L1 Adaptive, L2 Self-Organizing) with alignment levels (L0 Integrated, L1 User-Guided, L2 Real-Time Responsive). This creates 9 combinations from Rule-Driven Automation to User-Responsive Autonomy.
- **Quote**: "By combining these two dimensions in our matrix (see Table 1), we provide a comprehensive view of the interplay between diverse gradations of autonomy and alignment within LLM-powered multi-agent systems."
- **Context**: Framework for understanding the design space of autonomous multi-agent systems.

### Pattern: Static Autonomy Level (L0)

- **Source**: 18-Multi-Agent_Architecture_Taxonomy_LLM (Chunk 2:331-337)
- **Description**: Systems at L0 autonomy operate based on rules, conditions, and mechanisms embedded by system architects. Agents follow defined rules and predetermined mechanisms with some flexibility from rule-based options but cannot modify rules during runtime.
- **Quote**: "L0: Static Autonomy - At this foundational level, systems are primarily automated, relying heavily on the rules, conditions, and mechanisms embedded by system architects. The systems follow defined rules and predetermined mechanisms. This, however, includes some degree of flexibility resulting from rule-based options and alternatives. Anyway, the agents in these systems, are not empowered to modify rules during runtime."
- **Context**: Describes the lowest level of agent autonomy in the taxonomy.

### Pattern: Adaptive Autonomy Level (L1)

- **Source**: 18-Multi-Agent_Architecture_Taxonomy_LLM (Chunk 2:339-344)
- **Description**: Systems at L1 possess capability to adapt behavior within structures and procedural guidelines established by architects. LLM-powered agents can adjust operations within the provided framework but not beyond it.
- **Quote**: "L1: Adaptive Autonomy - Evolving from the static level, systems at this stage possess the capability to adapt their behavior within a structure and procedural guidelines established by the system architects. The LLM-powered agents are capable of adjusting the system's operations within this provided framework (such as flexible infrastructures and protocols) due to the needs of the given application scenarios, but not beyond."
- **Context**: Describes the middle level of agent autonomy with bounded adaptation.

### Pattern: Self-Organizing Autonomy Level (L2)

- **Source**: 18-Multi-Agent_Architecture_Taxonomy_LLM (Chunk 2:346-352)
- **Description**: At L2, LLM-powered agents emerge as principal actors capable of self-organization, actively learning and dynamically tailoring operations in real-time based on environmental cues. Autonomy is independent of architect-defined rules, not user intervention.
- **Quote**: "L2: Self-Organizing Autonomy - At this highest level of autonomy, LLM-powered agents emerge as the principal actors, capable of self-organization, actively learning and dynamically tailoring their operations in real-time based on environmental cues and experiences. The autonomy lies not in being independent from user intervention, but in being independent of architect-defined rules and mechanisms."
- **Context**: Describes the highest level of agent autonomy with full self-organization.

### Pattern: Alignment Levels for User Control

- **Source**: 18-Multi-Agent_Architecture_Taxonomy_LLM (Chunk 2:409-432)
- **Description**: Three alignment levels: L0 Integrated (built into architecture, user cannot adjust), L1 User-Guided (users set parameters before runtime via UI), L2 Real-Time Responsive (system solicits user feedback at critical junctures for ongoing collaboration).
- **Quote**: "L0: Integrated Alignment - At this foundational level, the alignment techniques are built directly into the system's architecture. In such system, alignment mechanisms are static and rule-driven, and cannot be altered by the users. L1: User-Guided Alignment - This level empowers users by allowing them to set or adjust specific alignment parameters, such as conditions, rules, or boundaries, before the system starts its operation. L2: Real-Time Responsive Alignment - The highest level of alignment is represented by means to adjust the system's behavior in real-time."
- **Context**: Framework for understanding different levels of human oversight in agent systems.

### Pattern: Goal-Driven Task Management Viewpoint

- **Source**: 18-Multi-Agent_Architecture_Taxonomy_LLM (Chunk 2:646-651)
- **Description**: A functional architectural viewpoint focused on the system's capabilities to decompose user-prompted goals into manageable tasks, orchestrate task execution, combine results, and deliver final responses.
- **Quote**: "Goal-driven Task Management (Functional Viewpoint): Kruchten's functional viewpoint refers to the system's visible functionalities as experienced by its users. In the context of autonomous LLM-powered multi-agent systems, we see Goal-driven Task Management as a manifestation of this functional viewpoint. It entails the system's capabilities and mechanisms to decompose user-prompted goals or complex tasks into smaller, more manageable tasks, and subsequently, orchestrate task execution, combine the results, and deliver the final result forming the response for the user"
- **Context**: One of four architectural viewpoints for analyzing multi-agent systems.

### Pattern: Agent Composition Viewpoint

- **Source**: 18-Multi-Agent_Architecture_Taxonomy_LLM (Chunk 2:654-658)
- **Description**: A development architectural viewpoint focusing on the system's internal composition, particularly the assembly and constellation of agents including types, roles, memory usage, and relationships between agents.
- **Quote**: "Agent Composition (Development Viewpoint): According to Kruchten, the development viewpoint is primarily focusing on the system's software architecture, the breakdown into components, and their organization. In our context, we interpret this as Agent Composition, focusing on the system's internal composition, particularly the assembly and constellation of agents. It includes the types and roles of agents, their memory usage, the relationships between agents"
- **Context**: Architectural viewpoint for analyzing agent structure and organization.

### Pattern: Multi-Agent Collaboration Viewpoint

- **Source**: 18-Multi-Agent_Architecture_Taxonomy_LLM (Chunk 2:661-667)
- **Description**: A process architectural viewpoint emphasizing collaborative task execution and interactions among agents, including communication protocols, action management dynamics, task delegation, result evaluation and merging, and prompt/template management.
- **Quote**: "Multi-Agent Collaboration (Process Viewpoint): Kruchten's process viewpoint concerns the dynamic aspects of a system, specifically the system procedures and interactions between components. We apply this to the Multi-Agent Collaboration in our model, emphasizing the collaborative task execution and interactions among agents. This encompasses the application of communication protocols, the dynamics of actions management, such as the actual task execution, mutual task delegation, as well as the evaluation and merging of task results on agent level"
- **Context**: Architectural viewpoint for analyzing agent interaction dynamics.

### Pattern: Context Interaction Viewpoint

- **Source**: 18-Multi-Agent_Architecture_Taxonomy_LLM (Chunk 2:670-675)
- **Description**: A physical architectural viewpoint focusing on the system's interaction with the external environment, including how the system acquires, integrates, and utilizes contextual resources such as external data, expert tools, and foundation models.
- **Quote**: "Context Interaction (Physical Viewpoint): According to Kruchten, the physical viewpoint involves the system's mapping to physical resources. We extend this to Context Interaction, focusing on the system's interaction with the external environment. It includes how the system acquires, integrates, and utilizes contextual resources such as external data, expert tools, and further foundation models as well as the organized distribution and utilization of contextual resources within the agent network"
- **Context**: Architectural viewpoint for analyzing agent-environment interaction.

### Pattern: Availability-Driven Dependencies (Low Autonomy)

- **Source**: 18-Multi-Agent_Architecture_Taxonomy_LLM (Chunk 2:697-776)
- **Description**: In low-autonomy systems, functionality relies on predefined capabilities where Goal-driven Task Management depends on all other dimensions, Multi-Agent Collaboration derives from Agent Composition and Context Interaction, and Agent Composition relies on Context Interaction availability.
- **Quote**: "For low-autonomy multi-agent systems, as depicted in Fig. 7 (a), the architecture operates predominantly under pre-established automation. In these systems, functionality largely relies on pre-configured rules and mechanisms. Thus, the functionality of such multi-agent system is contingent upon the predefined capabilities of the system processes, which are defined by the structure of the system and the resources available."
- **Context**: Describes dependency patterns in rule-driven multi-agent architectures.

### Pattern: Requirements-Driven Dependencies (High Autonomy)

- **Source**: 18-Multi-Agent_Architecture_Taxonomy_LLM (Chunk 2:779-800)
- **Description**: In high-autonomy systems, architectural components adapt to requirements rather than relying on availability. The user-prompted goal sets requirements that all viewpoints adapt to, with inverse dependency relationships compared to low-autonomy systems.
- **Quote**: "In highly-autonomous multi-agent systems, the user-prompted goal delineates the requirements, charting the course for the entire architectural edifice of the system. All other viewpoints adapt to the envisioned functional behavior expressed as Goal-driven Task Management. Based on the complexity of the goal, its decomposition into tasks and their distribution, the other architectural aspects inherent to the three further viewpoints undergo adaptations to fit the needs of the given situation."
- **Context**: Describes how self-organizing systems adapt their structure to requirements.

### Pattern: Graph of Thoughts (GoT) Operations

- **Source**: 19-Graph_of_Thoughts_LLM_Reasoning (Chunk 7:630-650)
- **Description**: GoT uses four distinct operation types for document merging tasks: Generate (instructing LLM to merge documents), Score (evaluating merged output), Aggregate (combining multiple merge attempts), and Improve (refining merged content). Each operation has specific prompts and purposes.
- **Quote**: "For document merging, we employ four distinct types of operations that interact with the LLM, each with its corresponding prompts. First, there is the Generate operation, utilizing the merge_prompt to instruct the LLM to merge the 4 NDAs into 1. Second, the Score operations instructs the LLM to score a given merged NDA using the score_prompt. Next, the Aggregate operation employs the aggregate_prompt to instruct the LLM to aggregate multiple merge attempts into a single, better one. Finally, the Improve operation leverages the improve_prompt to instruct the LLM to improve a merged NDA."
- **Context**: Defines primitive operations for graph-based reasoning workflows.

### Pattern: Hierarchical Merge-Score-Keep Pipeline

- **Source**: 19-Graph_of_Thoughts_LLM_Reasoning (Chunk 7:636-678)
- **Description**: A recursive pipeline pattern for GoT where problems are split into subproblems, each solved independently with k attempts, locally scored, best kept (KeepBestN), then aggregated in merge steps, scored again, and iteratively refined. The pattern scales with problem size (32, 64, 128 elements).
- **Quote**: "Generate(k=1) # Split second set into two halves of 16 elements foreach subset: Generate(k=5) # Determine intersected subset Score(k=1) # Score locally the intersected subsets KeepBestN(1) # Keep the best intersected subset Aggregate(10) # Merge both intersected subsets Score(k=1) # Score locally the intersected result sets KeepBestN(1) # Keep the best result GroundTruth() # Compare to precomputed result"
- **Context**: Shows how GoT structures reasoning as a graph of operations with scoring and selection.

### Pattern: Divide-Aggregate-Refine Pattern in GoT

- **Source**: 19-Graph_of_Thoughts_LLM_Reasoning (Chunk 5:1-77)
- **Description**: GoT splits input text into multiple paragraphs, processes each independently (counting keywords), then combines results through step-by-step aggregation. Multiple responses are generated and the best selected based on error counts.
- **Quote**: "Split the following input text into 4 paragraphs of approximately same length... To count the frequency for each country follow these steps: 1. Split the input passage into four paragraphs of similar length. 2. Count the frequency of each country in each paragraph. 3. Combine the frequencies of each country from each paragraph by adding them together."
- **Context**: Demonstrates decomposition and aggregation pattern in reasoning workflows.

### Pattern: Agentic RAG Core Architecture

- **Source**: 20-Agentic_RAG_Survey (Chunk 1:55-60)
- **Description**: Agentic RAG embeds autonomous AI agents into the RAG pipeline leveraging four agentic design patterns: reflection, planning, tool use, and multi-agent collaboration. These enable dynamic retrieval strategy management, iterative contextual refinement, and adaptive workflows.
- **Quote**: "Agentic Retrieval-Augmented Generation (Agentic RAG) transcends these limitations by embedding autonomous AI agents into the RAG pipeline. These agents leverage agentic design patterns - reflection, planning, tool use, and multi-agent collaboration - to dynamically manage retrieval strategies, iteratively refine contextual understanding, and adapt workflows through clearly defined operational structures ranging from sequential steps to adaptive collaboration."
- **Context**: Defines the fundamental architecture combining RAG with agentic capabilities.

### Pattern: Four Core Agentic Patterns

- **Source**: 20-Agentic_RAG_Survey (Chunk 1:104-107)
- **Description**: Four key patterns underpinning agentic workflows: reflection (self-evaluation and output refinement), planning (task decomposition), tool use (external capability integration), and multi-agent collaboration (task specialization and parallel processing).
- **Quote**: "These agents leverage agentic patterns, such as reflection, planning, tool use, and multi-agent collaboration, to enhance decision-making and adaptability."
- **Context**: Core design patterns for building agentic systems.

### Pattern: AI Agent Components

- **Source**: 20-Agentic_RAG_Survey (Chunk 1:484-501)
- **Description**: An AI agent comprises four core components: (1) LLM with defined Role and Task as primary reasoning engine, (2) Memory with short-term (conversation state) and long-term (accumulated knowledge) components, (3) Planning through reflection and self-critique for iterative reasoning, (4) Tools for accessing external resources and computations.
- **Quote**: "LLM (with defined Role and Task): Serves as the agent's primary reasoning engine and dialogue interface. It interprets user queries, generates responses, and maintains coherence. Memory (Short-Term and Long-Term): Captures context and relevant data across interactions. Short-term memory tracks immediate conversation state, while long-term memory stores accumulated knowledge and agent experiences. Planning (Reflection & Self-Critique): Guides the agent's iterative reasoning process through reflection, query routing, or self-critique, ensuring that complex tasks are broken down effectively. Tools (Vector Search, Web Search, APIs, etc.): Expands the agent's capabilities beyond text generation, enabling access to external resources, real-time data, or specialized computations."
- **Context**: Foundational architecture for autonomous AI agents.

### Pattern: Reflection Pattern

- **Source**: 20-Agentic_RAG_Survey (Chunk 1:515-531)
- **Description**: Reflection enables agents to iteratively evaluate and refine outputs through self-feedback mechanisms, identifying errors, inconsistencies, and areas for improvement. Can involve prompting agent to critique for correctness, style, efficiency, with external validation through unit tests or web searches. In multi-agent systems, distinct roles for generating and critiquing outputs.
- **Quote**: "Reflection is a foundational design pattern in agentic workflows, enabling agents to iteratively evaluate and refine their outputs. By incorporating self-feedback mechanisms, agents can identify and address errors, inconsistencies, and areas for improvement, enhancing performance across tasks like code generation, text production, and question answering."
- **Context**: Core pattern for iterative self-improvement in agentic systems.

### Pattern: Planning Pattern

- **Source**: 20-Agentic_RAG_Survey (Chunk 1:540-549)
- **Description**: Planning enables agents to autonomously decompose complex tasks into smaller, manageable subtasks, essential for multi-hop reasoning and iterative problem-solving in dynamic scenarios. Allows dynamic determination of step sequences for larger objectives.
- **Quote**: "Planning is a key design pattern in agentic workflows that enables agents to autonomously decompose complex tasks into smaller, manageable subtasks. This capability is essential for multi-hop reasoning and iterative problem-solving in dynamic and uncertain scenarios."
- **Context**: Pattern for task decomposition and sequencing in agent workflows.

### Pattern: Tool Use Pattern

- **Source**: 20-Agentic_RAG_Survey (Chunk 1:555-569)
- **Description**: Tool Use extends agent capabilities through interaction with external tools, APIs, or computational resources for gathering information, performing computations, and manipulating data beyond pre-trained knowledge. Implementation includes GPT-4's function calling and systems managing numerous tools.
- **Quote**: "Tool Use enables agents to extend their capabilities by interacting with external tools, APIs, or computational resources. This pattern allows agents to gather information, perform computations, and manipulate data beyond their pre-trained knowledge. By dynamically integrating tools into workflows, agents can adapt to complex tasks and provide more accurate and contextually relevant outputs."
- **Context**: Pattern for extending agent capabilities through external integrations.

### Pattern: Multi-Agent Collaboration Pattern

- **Source**: 20-Agentic_RAG_Survey (Chunk 1:575-597)
- **Description**: Multi-agent collaboration enables task specialization and parallel processing where agents communicate and share intermediate results. Each agent operates with its own memory and workflow including tools, reflection, or planning. Frameworks include AutoGen, Crew AI, and LangGraph.
- **Quote**: "Multi-agent collaboration is a key design pattern in agentic workflows that enables task specialization and parallel processing. Agents communicate and share intermediate results, ensuring the overall workflow remains efficient and coherent. By distributing subtasks among specialized agents, this pattern improves the scalability and adaptability of complex workflows."
- **Context**: Pattern for coordinating multiple specialized agents on complex tasks.

### Pattern: Prompt Chaining Workflow

- **Source**: 20-Agentic_RAG_Survey (Chunk 1:620-632)
- **Description**: Prompt chaining decomposes complex tasks into multiple sequential steps where each builds upon the previous, improving accuracy by simplifying each subtask. May increase latency due to sequential processing. Best when task can be broken into fixed subtasks contributing to final output.
- **Quote**: "Prompt chaining decomposes a complex task into multiple steps, where each step builds upon the previous one. This structured approach improves accuracy by simplifying each subtask before moving forward. However, it may increase latency due to sequential processing."
- **Context**: Sequential workflow pattern for step-by-step task execution.

### Pattern: Routing Workflow

- **Source**: 20-Agentic_RAG_Survey (Chunk 1:647-656)
- **Description**: Routing classifies input and directs it to appropriate specialized prompts or processes, ensuring distinct queries are handled separately for improved efficiency and response quality. Ideal when different input types require distinct handling strategies.
- **Quote**: "Routing involves classifying an input and directing it to an appropriate specialized prompt or process. This method ensures distinct queries or tasks are handled separately, improving efficiency and response quality."
- **Context**: Pattern for input classification and specialized handling in workflows.

### Pattern: Parallelization Workflow

- **Source**: 20-Agentic_RAG_Survey (Chunk 1:674-694)
- **Description**: Parallelization divides tasks into independent processes running simultaneously, reducing latency and improving throughput. Two sub-patterns: sectioning (independent subtasks) and voting (multiple outputs for accuracy through cross-checking).
- **Quote**: "Parallelization divides a task into independent processes that run simultaneously, reducing latency and improving throughput. It can be categorized into sectioning (independent subtasks) and voting (multiple outputs for accuracy)."
- **Context**: Pattern for concurrent execution and result aggregation.

### Pattern: Orchestrator-Workers Workflow

- **Source**: 20-Agentic_RAG_Survey (Chunk 1:699-707)
- **Description**: A central orchestrator model dynamically breaks tasks into subtasks, assigns them to specialized worker models, and compiles results. Unlike parallelization, it adapts to varying input complexity with subtasks not predefined.
- **Quote**: "This workflow features a central orchestrator model that dynamically breaks tasks into subtasks, assigns them to specialized worker models, and compiles the results. Unlike parallelization, it adapts to varying input complexity."
- **Context**: Dynamic task delegation pattern with central coordination.

### Pattern: Evaluator-Optimizer Workflow

- **Source**: 20-Agentic_RAG_Survey (Chunk 1:724-731)
- **Description**: Iteratively improves content by generating initial output then refining it based on feedback from an evaluation model. Effective when iterative refinement significantly enhances quality and clear evaluation criteria exist.
- **Quote**: "The evaluator-optimizer workflow iteratively improves content by generating an initial output and refining it based on feedback from an evaluation model."
- **Context**: Pattern for iterative quality improvement through evaluation loops.

### Pattern: Single-Agent Agentic RAG Router

- **Source**: 20-Agentic_RAG_Survey (Chunk 1:755-798)
- **Description**: A centralized single agent manages retrieval, routing, and integration. Workflow: (1) Query submission and evaluation, (2) Knowledge source selection (structured DBs, semantic search, web search, recommendation systems), (3) Data integration and LLM synthesis, (4) Output generation. Features centralized simplicity, efficiency, and dynamic routing.
- **Quote**: "A Single-Agent Agentic RAG serves as a centralized decision-making system where a single agent manages the retrieval, routing, and integration of information. This architecture simplifies the system by consolidating these tasks into one unified agent, making it particularly effective for setups with a limited number of tools or data sources."
- **Context**: Simplest agentic RAG architecture with unified agent control.

### Pattern: Multi-Agent Agentic RAG System

- **Source**: 20-Agentic_RAG_Survey (Chunk 1:874-919)
- **Description**: Distributes responsibilities across multiple specialized agents instead of single agent. Coordinator agent orchestrates, with specialized agents for different data sources (SQL databases, semantic search, web search, recommendation systems). Retrieval executes in parallel with tool access (vector search, text-to-SQL, web search, APIs).
- **Quote**: "Multi-Agent RAG represents a modular and scalable evolution of single-agent architectures, designed to handle complex workflows and diverse query types by leveraging multiple specialized agents. Instead of relying on a single agent to manage all tasks—reasoning, retrieval, and response generation—this system distributes responsibilities across multiple agents, each optimized for a specific role or data source."
- **Context**: Scalable architecture with specialized agents for different retrieval tasks.

### Pattern: Hierarchical Agentic RAG

- **Source**: 20-Agentic_RAG_Survey (Chunk 2:100-135)
- **Description**: Multi-tiered approach with agents organized in hierarchy, higher-level agents overseeing lower-level. Workflow: top-tier receives query and makes strategic decisions, delegates to subordinate agents, results aggregated and synthesized by higher-level agent. Enables strategic prioritization and multi-level decision-making.
- **Quote**: "Hierarchical Agentic RAG systems employ a structured, multi-tiered approach to information retrieval and processing, enhancing both efficiency and strategic decision-making. Agents are organized in a hierarchy, with higher-level agents overseeing and directing lower-level agents. This structure enables multi-level decision-making, ensuring that queries are handled by the most appropriate resources."
- **Context**: Tiered architecture for strategic coordination of agent activities.

### Pattern: Corrective RAG with Agent Pipeline

- **Source**: 20-Agentic_RAG_Survey (Chunk 2:193-244)
- **Description**: Self-correcting retrieval through five specialized agents: Context Retrieval Agent (initial retrieval), Relevance Evaluation Agent (assessing documents), Query Refinement Agent (rewriting queries), External Knowledge Retrieval Agent (web searches), Response Synthesis Agent (final synthesis). Features document relevance evaluation, query refinement, and dynamic external retrieval.
- **Quote**: "The core principle of Corrective RAG lies in its ability to evaluate retrieved documents dynamically, perform corrective actions, and refine queries to enhance the quality of generated responses... The Corrective RAG system is built on five key agents: Context Retrieval Agent, Relevance Evaluation Agent, Query Refinement Agent, External Knowledge Retrieval Agent, Response Synthesis Agent."
- **Context**: Architecture for iterative document relevance improvement through specialized agents.

### Pattern: Adaptive RAG with Complexity Classification

- **Source**: 20-Agentic_RAG_Survey (Chunk 2:317-379)
- **Description**: Dynamic query handling based on complexity classification. A classifier predicts query complexity, then selects strategy: straightforward queries bypass retrieval, simple queries use single-step retrieval, complex queries employ multi-step retrieval with iterative refinement.
- **Quote**: "Adaptive Retrieval-Augmented Generation (Adaptive RAG) enhances the flexibility and efficiency of large language models (LLMs) by dynamically adjusting query handling strategies based on the complexity of the incoming query. Unlike static retrieval workflows, Adaptive RAG employs a classifier to assess query complexity and determine the most appropriate approach, ranging from single-step retrieval to multi-step reasoning, or even bypassing retrieval altogether for straightforward queries."
- **Context**: Dynamic workflow selection based on query complexity analysis.

### Pattern: Agent-G Graph RAG Framework

- **Source**: 20-Agentic_RAG_Survey (Chunk 2:449-517)
- **Description**: Integrates graph knowledge bases with unstructured document retrieval through four components: Retriever Bank (modular agents for graph/unstructured data), Critic Module (validates relevance and quality), Dynamic Agent Interaction (task-specific collaboration), LLM Integration (synthesis with iterative feedback). Enables combined structured relationship and contextual information reasoning.
- **Quote**: "Agent-G introduces a novel agentic architecture that integrates graph knowledge bases with unstructured document retrieval... The Agent-G system is built on four primary components: Retriever Bank, Critic Module, Dynamic Agent Interaction, LLM Integration."
- **Context**: Architecture combining graph-structured and unstructured retrieval through specialized agents.

### Pattern: GeAR Graph-Enhanced Agent

- **Source**: 20-Agentic_RAG_Survey (Chunk 2:583-622)
- **Description**: Enhances RAG with graph expansion techniques and agent-based architecture. Graph Expansion Module integrates graph data enabling multi-hop query handling. Agent-Based Retrieval manages dynamic selection and combination of strategies with autonomous decision-making for graph-expanded retrieval paths.
- **Quote**: "GeAR advances RAG performance through two primary innovations: Graph Expansion: Enhances conventional base retrievers (e.g., BM25) by expanding the retrieval process to include graph-structured data, enabling the system to capture complex relationships and dependencies between entities. Agent Framework: Incorporates an agent-based architecture that utilizes graph expansion to manage retrieval tasks more effectively, allowing for dynamic and autonomous decision-making in the retrieval process."
- **Context**: Agent architecture for graph-enhanced multi-hop retrieval.

### Pattern: Agentic Document Workflows (ADW)

- **Source**: 20-Agentic_RAG_Survey (Chunk 2:704-748)
- **Description**: End-to-end knowledge work automation orchestrating document-centric processes. Five-step workflow: (1) Document Parsing and Information Structuring, (2) State Maintenance Across Processes, (3) Knowledge Retrieval from external bases, (4) Agentic Orchestration applying business rules, (5) Actionable Output Generation. Features state maintenance, multi-step orchestration, and domain-specific intelligence.
- **Quote**: "Agentic Document Workflows (ADW) extend traditional Retrieval-Augmented Generation (RAG) paradigms by enabling end-to-end knowledge work automation. These workflows orchestrate complex document-centric processes, integrating document parsing, retrieval, reasoning, and structured outputs with intelligent agents."
- **Context**: Architecture for document-centric workflow automation with intelligent agents.
