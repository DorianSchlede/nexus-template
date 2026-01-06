---
batch_id: 1
field: generative_ai_patterns
papers_read: [15-SciAgents_Multi-Agent_Graph_Reasoning, 16-KG-Agent_Knowledge_Graph_Reasoning, 18-Multi-Agent_Architecture_Taxonomy_LLM, 19-Graph_of_Thoughts_LLM_Reasoning]
chunks_read: 8
patterns_found: 42
extracted_at: "2025-12-28T12:00:00Z"
---

# Batch Extraction: generative_ai_patterns (Batch 1)

## Patterns Extracted

### Pattern: Multi-Agent System with In-Situ Learning

- **Source**: 15-SciAgents_Multi-Agent_Graph_Reasoning (Chunk 1:30-43)
- **Description**: SciAgents leverages three core concepts for automating scientific discovery: (1) large-scale ontological knowledge graphs to organize scientific concepts, (2) a suite of LLMs and data retrieval tools, and (3) multi-agent systems with in-situ learning capabilities. The framework autonomously generates and refines research hypotheses.
- **Quote**: "In this work, we present SciAgents, an approach that leverages three core concepts: (1) the use of large-scale ontological knowledge graphs to organize and interconnect diverse scientific concepts, (2) a suite of large language models (LLMs) and data retrieval tools, and (3) multi-agent systems with _in-situ_ learning capabilities."
- **Context**: Abstract section describing the core architecture of SciAgents for scientific discovery automation.

---

### Pattern: In-Context Learning for LLM Enhancement

- **Source**: 15-SciAgents_Multi-Agent_Graph_Reasoning (Chunk 1:95-102)
- **Description**: In-context learning emerges as a strategy to enhance LLM performance without costly fine-tuning. This approach exploits the model's inherent ability to adapt responses based on context embedded within prompts, derived from various sources.
- **Quote**: "In response to these challenges, in-context learning emerges as a compelling strategy to enhance the performance of LLMs without the need for costly and time-intensive fine-tuning. This approach exploits the model's inherent ability to adapt its responses based on the context embedded within the prompt, which can be derived from a variety of sources."
- **Context**: Discussion of strategies to improve LLM reasoning and problem-solving capabilities.

---

### Pattern: Knowledge Graph Augmented Generation

- **Source**: 15-SciAgents_Multi-Agent_Graph_Reasoning (Chunk 1:105-110)
- **Description**: Construction of knowledge bases and strategic retrieval from them enhances LLM generative capabilities. Knowledge graphs provide mechanistic breakdown and ontological framework showing interconnectedness of concepts as nodes and edges.
- **Quote**: "The construction of knowledge bases and the strategic retrieval of information from them are gaining traction as effective methods to enhance the generative capabilities of LLMs. Recent advancements in generative AI allow for the efficient mining of vast scientific datasets, transforming unstructured natural language into structured data such as comprehensive ontological knowledge graphs."
- **Context**: Describing methods to enhance LLM capabilities through structured knowledge integration.

---

### Pattern: Multi-Agent AI for Complex Problem Solving

- **Source**: 15-SciAgents_Multi-Agent_Graph_Reasoning (Chunk 1:113-120)
- **Description**: Single-LLM-based agents fall short for complex scientific discovery demands. Multi-agent AI systems are better suited for tackling complex problems by pooling capabilities across different domains through collaborative approaches.
- **Quote**: "While single-LLM-based agents can generate more accurate responses when enhanced with well-designed prompts and context, they often fall short for the complex demands of scientific discovery. Creating new scientific insights involves a series of steps, deep thinking, and the integration of diverse, sometimes conflicting information, making it a challenging task for a single agent."
- **Context**: Justification for using multi-agent systems over single-agent approaches.

---

### Pattern: Role-Based Agent Specialization

- **Source**: 15-SciAgents_Multi-Agent_Graph_Reasoning (Chunk 1:126-130)
- **Description**: Within the generative framework, discovery workflow is systematically broken down into subtasks. Each agent is assigned a distinct role, optimized through complex prompting strategies to ensure targeted expertise and precision for each subtask.
- **Quote**: "Within this generative framework, the discovery workflow is systematically broken down into more manageable subtasks. Each agent in the system is assigned a distinct role, optimized through complex prompting strategies to ensure that every subtask is tackled with targeted expertise and precision."
- **Context**: Describing the architecture of the multi-agent system for scientific discovery.

---

### Pattern: Pre-Programmed vs Autonomous Agent Interactions

- **Source**: 15-SciAgents_Multi-Agent_Graph_Reasoning (Chunk 1:186-197)
- **Description**: Two distinct strategies for multi-agent interactions: (1) pre-programmed interactions following predefined sequence ensuring consistency and reliability, and (2) fully automated agent interactions without predetermined order, providing flexible and adaptive framework with human-in-the-loop capability.
- **Quote**: "The key difference between these approaches lies in the nature of the interaction between the agents. In the first approach (Figure 1b), the interactions between agents are pre-programmed and follow a predefined sequence of tasks that ensure consistency and reliability in hypothesis generation. In contrast, the second approach features fully automated agent interactions without any predetermined order of how interactions between agents unfold, providing a more flexible and adaptive framework that can dynamically respond to the evolving context of the research process."
- **Context**: Comparison of two distinct multi-agent system architectures.

---

### Pattern: Hierarchical Expansion Strategy

- **Source**: 15-SciAgents_Multi-Agent_Graph_Reasoning (Chunk 1:200-210)
- **Description**: Answers are successively refined and improved, enriched with retrieved data, critiqued and amended through adversarial prompting. Process begins with keyword identification, path sampling to create subgraph, then generating structured output in JSON following specific aspects.
- **Quote**: "We employ a hierarchical expansion strategy where answers are successively refined and improved, enriched with retrieved data, critiqued and amended by identification or critical modeling, simulation and experimental tasks and adversarial prompting."
- **Context**: Describing the iterative refinement process in hypothesis generation.

---

### Pattern: Random Path Sampling for Knowledge Graph Exploration

- **Source**: 15-SciAgents_Multi-Agent_Graph_Reasoning (Chunk 1:239-247)
- **Description**: Unlike using shortest paths, random path approach infuses richer array of concepts and relationships, enabling broader spectrum exploration. This expanded exploration enhances depth and breadth of insights and fosters novelty of generated hypotheses.
- **Quote**: "Unlike in earlier work [6] where the shortest path was utilized, our study employs a random path approach. As illustrated in Figure 4, the random approach infuses the path with a richer array of concepts and relationships, enabling our agents to explore a broader spectrum of domains, as opposed to the shortest path where only a few concepts are included."
- **Context**: Path generation methodology for knowledge graph reasoning.

---

### Pattern: Ontologist Agent for Dynamic Knowledge Generation

- **Source**: 15-SciAgents_Multi-Agent_Graph_Reasoning (Chunk 1:289-296)
- **Description**: LLM-powered ontologist agent examines connections and nuances among identified concepts, transitioning from static knowledge retrieval to dynamic knowledge generation. Applies advanced reasoning and inference techniques to synthesize and interpret complex data webs.
- **Quote**: "By examining the connections and nuances among the identified concepts, the agent helps transition from static knowledge retrieval to dynamic knowledge generation. This crucial shift is what enables the model to identify gaps in existing research and propose new angles of inquiry, thereby laying the groundwork for novel ideas and hypotheses."
- **Context**: Description of the ontologist agent's role in the multi-agent system.

---

### Pattern: Scientist Agent with Structured Output Generation

- **Source**: 15-SciAgents_Multi-Agent_Graph_Reasoning (Chunk 1:356-365)
- **Description**: Scientist agent synthesizes novel research proposals through complex prompting, delivering detailed hypotheses that are innovative and logically grounded. Creates proposals addressing seven key aspects: hypothesis, outcome, mechanisms, design principles, unexpected properties, comparison, and novelty.
- **Quote**: "Through complex prompting, as shown in Figure 5, the agent is assigned specific roles and is tasked with synthesizing a novel research proposal that integrates all key concepts from the knowledge graph. The designated agent, Scientist_1, is configured to deliver a detailed hypothesis that is both innovative and logically grounded, aiming to advance the understanding or application of the provided concepts."
- **Context**: Description of how the scientist agent generates structured research proposals.

---

### Pattern: Critic Agent for Scientific Review

- **Source**: 15-SciAgents_Multi-Agent_Graph_Reasoning (Chunk 1:511-516)
- **Description**: Critic agent thoroughly reviews research proposals, summarizes key points, and recommends improvements. Delivers comprehensive scientific critique highlighting strengths and weaknesses while suggesting refinement areas and identifying impactful scientific questions.
- **Quote**: "At the final stage of our research development process is the Critic agent, responsible for thoroughly reviewing the research proposal, summarizing its key points, and recommending improvements. This agent delivers a comprehensive scientific critique, highlighting both the strengths and weaknesses of the research idea while suggesting areas for refinement."
- **Context**: Description of the critic agent's role in the adversarial review process.

---

### Pattern: Autonomous Agentic Modeling with Dynamic Interactions

- **Source**: 15-SciAgents_Multi-Agent_Graph_Reasoning (Chunk 1:700-748)
- **Description**: Automated multi-agent system consists of team of AI agents, each powered by GPT-4 family models. Includes Human, Planner, Ontologist, Scientist 1, Scientist 2, Critic, Assistant with tool access, and Group chat manager who chooses next speaker based on context and broadcasts messages.
- **Quote**: "The automated multi-agent system consists of a team of AI agents, each powered by a state-of-the-art general purpose large language model from the GPT-4 family [11], accessed via the OpenAI API [44]. Each agent has a specific role and focus in the system which is described by a unique profile."
- **Context**: Description of the autonomous multi-agent architecture.

---

### Pattern: Shared Memory vs Filtered Information Propagation

- **Source**: 15-SciAgents_Multi-Agent_Graph_Reasoning (Chunk 1:784-799)
- **Description**: In pre-programmed approach, agents receive only filtered subset of information from previous interactions. In automated approach, agents share memory with full visibility of collaboration history. This difference leads to variations in hypothesis details.
- **Quote**: "In the first approach, during the generation process, the agents receive only a filtered subset of information from previous interactions (see 4.3 for more details). In contrast, the second approach allows agents to share memory, giving them access to all the content generated in previous interactions. This means they operate with full visibility of the history of their collaboration."
- **Context**: Comparison of information sharing strategies between different multi-agent approaches.

---

### Pattern: Planner Agent with Breakdown Execution Plan

- **Source**: 15-SciAgents_Multi-Agent_Graph_Reasoning (Chunk 4:9-18)
- **Description**: Overview of agent-based plan with five stages: (1) Define Terms and Relationships by ontologist, (2) Craft Research Proposal by scientist, (3) Expand Key Aspects by specialized agents, (4) Critique and Improve by critic agent, (5) Rate Novelty and Feasibility by assistant calling functions.
- **Quote**: "1. **Define Terms and Relationships** : The ontologist will define each term in the knowledge path and discuss the relationships between them. 2. **Craft the Research Proposal** : The scientist will craft a research proposal based on the definitions and relationships provided by the ontologist. 3. **Expand Key Aspects** : Each specialized agent... will expand on their respective sections of the research proposal. 4. **Critique and Improve** : The critic_agent will summarize, critique, and suggest improvements. 5. **Rate Novelty and Feasibility** : Finally, the assistant will call the appropriate function to rate the novelty and feasibility of the research idea."
- **Context**: Detailed breakdown of the planner agent's execution plan.

---

### Pattern: Specialized Expansion Agents

- **Source**: 15-SciAgents_Multi-Agent_Graph_Reasoning (Chunk 4:3-6)
- **Description**: Multiple specialized agents expand different aspects of research proposals: hypothesis_agent, outcome_agent, mechanism_agent, design_principles_agent, unexpected_properties_agent, comparison_agent, novelty_agent, each expanding their respective sections.
- **Quote**: "design _principle" aspect of the research proposal crafted by the "scientist". unexpected_ properties _agent: unexpected_ properties _agent who can expand the "unexpected_ properties" aspect of the research proposal crafted by the "scientist. comparison _agent: comparison_ agent who can expand the "comparison" aspect of the research proposal crafted by the "scientist"."
- **Context**: Description of specialized agent roles for expanding research proposal components.

---

### Pattern: Function-Based Novelty and Feasibility Rating

- **Source**: 15-SciAgents_Multi-Agent_Graph_Reasoning (Chunk 4:67-73)
- **Description**: Assistant agent calls functions to rate novelty and feasibility of research ideas. Uses external tools like Semantic Scholar API to assess novelty against existing literature, providing objective measures of research potential.
- **Quote**: "**Reasoning** : Rating the novelty and feasibility will provide an objective measure of the research idea's potential. **Actions** : The assistant will call the functions.rate_novelty_feasibility function to rate the research idea."
- **Context**: Description of tool-based evaluation mechanism for research ideas.

---

### Pattern: Molecular Dynamics Simulation Integration

- **Source**: 15-SciAgents_Multi-Agent_Graph_Reasoning (Chunk 4:298-303)
- **Description**: MD simulations integrated to understand interaction between materials. Simulations provide insights into binding affinity, stability, and self-assembly processes of functionalized materials.
- **Quote**: "**Molecular Dynamics (MD) Simulations** : To understand the interaction between silk proteins and nanoscale pigments, MD simulations will be conducted. These simulations will provide insights into the binding affinity and stability of the functionalized silk."
- **Context**: Integration of computational simulation tools into the multi-agent research framework.

---

### Pattern: Autonomous LLM Agent Framework for KG Reasoning

- **Source**: 16-KG-Agent_Knowledge_Graph_Reasoning (Chunk 1:19-38)
- **Description**: KG-Agent is an autonomous LLM-based agent framework enabling small LLMs to actively make decisions until finishing reasoning over knowledge graphs. Integrates LLM, multifunctional toolbox, KG-based executor, and knowledge memory with iteration mechanism for autonomous tool selection and memory updates.
- **Quote**: "we propose an autonomous LLM-based agent framework, called **KG-Agent**, which enables a small LLM to actively make decisions until finishing the reasoning process over KGs. In KG-Agent, we integrate the LLM, multifunctional toolbox, KG-based executor, and knowledge memory, and develop an iteration mechanism that autonomously selects the tool then updates the memory for reasoning over KG."
- **Context**: Abstract describing the core architecture of KG-Agent.

---

### Pattern: Code-Based Instruction Dataset for LLM Fine-Tuning

- **Source**: 16-KG-Agent_Knowledge_Graph_Reasoning (Chunk 1:31-38)
- **Description**: Program language is used to formulate multi-hop reasoning process over KG. A code-based instruction dataset is synthesized to fine-tune base LLM, enabling effective reasoning with only 10K samples on LLaMA-7B.
- **Quote**: "To guarantee the effectiveness, we leverage program language to formulate the multi-hop reasoning process over the KG, and synthesize a code-based instruction dataset to fine-tune the base LLM. Extensive experiments demonstrate that only using 10K samples for tuning LLaMA-7B can outperform state-of-the-art methods using larger LLMs or more data."
- **Context**: Description of the training methodology for KG-Agent.

---

### Pattern: Retrieval-Augmented vs Synergy-Augmented Methods

- **Source**: 16-KG-Agent_Knowledge_Graph_Reasoning (Chunk 1:54-68)
- **Description**: Two main approaches for enhancing LLMs with KG data: retrieval-augmented (retrieves and serializes task-related triples as prompt) and synergy-augmented (designs information interaction mechanism between KG and LLMs for iterative solution finding).
- **Quote**: "Recent work mainly adopts _retrieval-augmented_ (Ye et al., 2022) or _synergy-augmented_ (Jiang et al., 2023b) methods to enhance LLMs with KG data. The former approach retrieves and serializes the task-related triples as part of the prompt for LLMs, while the latter approach designs an information interaction mechanism between KG and LLMs to iteratively find the solution to the question."
- **Context**: Classification of KG-LLM integration approaches.

---

### Pattern: Three-Type Toolbox for KG Operations

- **Source**: 16-KG-Agent_Knowledge_Graph_Reasoning (Chunk 1:236-259)
- **Description**: Toolbox contains three types of tools: (1) Extraction tools for accessing KG information (get_relation, get_head_entity, get_tail_entity), (2) Logic tools for manipulation (count, intersect, union, judge, end), (3) Semantic tools using pre-trained models (retrieve_relation, disambiguate_entity).
- **Quote**: "we design three types of tools for LLMs reasoning over KG, _i.e.,_ extraction, semantic, and logic tools. **Extraction tools** aim to facilitate the access to information from KG... **Logic tools** aim to support basic manipulation operations on the extracted KG information... **Semantic tools** are developed by utilizing pre-trained models to implement specific functions."
- **Context**: Description of the toolbox architecture for KG reasoning.

---

### Pattern: KG Reasoning Program Generation from SQL

- **Source**: 16-KG-Agent_Knowledge_Graph_Reasoning (Chunk 1:278-293)
- **Description**: Leverages existing KGQA datasets to synthesize KG reasoning programs instead of distilling from closed-source LLMs. SQL queries are grounded on KG to obtain query graphs, then reasoning chains are extracted and decomposed into code snippets.
- **Quote**: "Instead of distilling from close-sourced LLMs ( _e.g.,_ GPT-4), we propose to leverage existing KGQA datasets to synthesize the KG reasoning program. These KGQA datasets contain the annotated SQL queries that can be executed to directly extract the answer entities for each question."
- **Context**: Description of the training data generation methodology.

---

### Pattern: Breadth-First Search for Reasoning Chain Extraction

- **Source**: 16-KG-Agent_Knowledge_Graph_Reasoning (Chunk 1:426-433)
- **Description**: Starting from mentioned entity in question, breadth-first search (BFS) visits all nodes on query graph. This produces reasoning chain linking start entity to answer entity, with constraint conditions and numerical operations naturally involved.
- **Quote**: "starting from the mentioned entity in the question ( _i.e., Cristiano Ronaldo_ ), we adopt breadth-first search (BFS) to visit all the nodes on the query graph. This strategy would finally produce a reasoning chain ( _e.g., teams->roster_team_ ) linking the start entity to the answer entity, and the relevant constraint conditions ( _e.g., roster_from_ = '2011') or numerical operation ( _e.g., founded_ must be last) can be naturally involved in this process."
- **Context**: Algorithm for extracting reasoning chains from query graphs.

---

### Pattern: Input-Output Pair Construction for Instruction Tuning

- **Source**: 16-KG-Agent_Knowledge_Graph_Reasoning (Chunk 1:470-515)
- **Description**: For each function call, input-output pair is constructed as instruction. Input contains question, toolbox definition, current KG information, and history reasoning program. Output is the function call at current step. Unified prompt template formats the pairs.
- **Quote**: "Specifically, the input contains the question, toolbox definition, current KG information ( _i.e.,_ the next candidate relations of the current entity set), and history reasoning program before the current step; and the output is the function call at the current step."
- **Context**: Description of instruction tuning data construction methodology.

---

### Pattern: Knowledge Memory for Autonomous Reasoning

- **Source**: 16-KG-Agent_Knowledge_Graph_Reasoning (Chunk 1:545-551)
- **Description**: Knowledge memory preserves currently useful information for LLM-based planner decision-making. Contains four parts: natural language question, toolbox definition, current KG information, and history reasoning program. Former two remain unchanged; latter two updated at each step.
- **Quote**: "The knowledge memory preserves the currently useful information to support the LLM-based planner for making decisions. It mainly contains four parts of information, _i.e.,_ natural language question, toolbox definition, current KG information, and history reasoning program."
- **Context**: Description of memory architecture for autonomous agent reasoning.

---

### Pattern: LLM-Based Planner for Tool Selection

- **Source**: 16-KG-Agent_Knowledge_Graph_Reasoning (Chunk 1:554-565)
- **Description**: Based on current knowledge memory, LLM-based planner selects tool to interact with KG at each step. Memory parts formatted with prompt template compose input, then LLM generates one function call by selecting tool and arguments.
- **Quote**: "Based on the current knowledge memory, the LLM-based planner selects a tool to interact with KG at each step. Specifically, all the parts in the current knowledge memory will be formatted with corresponding prompt template to compose the input (used in Agent Instruction Tuning in Section 4.2.2), and then the LLM will generate one function call by selecting a tool and its arguments from the input."
- **Context**: Description of the planner's decision-making mechanism.

---

### Pattern: Executor for Memory Updation

- **Source**: 16-KG-Agent_Knowledge_Graph_Reasoning (Chunk 1:568-626)
- **Description**: After planner generates function call, KG-based executor executes it using program compiler. It caches/operates intermediate variables and extracts new entities/relations from KG. Knowledge memory is accordingly updated with function call added to history and new KG information added.
- **Quote**: "After the planner generates the function call, the KG-based executor will execute it using a program compiler. It can cache or operate the intermediate variables, and extract new entities or relations from the KG. After execution, the knowledge memory will be accordingly updated."
- **Context**: Description of the executor's role in the agent framework.

---

### Pattern: Iterative Autonomous KG-Agent

- **Source**: 16-KG-Agent_Knowledge_Graph_Reasoning (Chunk 1:629-638)
- **Description**: KG-Agent framework autonomously iterates tool selection and memory updation for step-by-step reasoning. Multi-turn decision-making is like walking on KG along relations. Agent automatically stops once reaching answer entities. Process is agnostic to task types and specific KGs.
- **Quote**: "The KG-Agent framework autonomously iterates the above tool selection and memory updation process to perform step-by-step reasoning, where the knowledge memory is used to maintain the accessed information from KG. In this way, the multi-turn decision-making process of the agent is like walking on the KG along relations. Once reaching the answer entities, the agent will automatically stop the iterative process."
- **Context**: Description of the autonomous iteration mechanism.

---

### Pattern: Autonomy-Alignment Balance in Multi-Agent Systems

- **Source**: 18-Multi-Agent_Architecture_Taxonomy_LLM (Chunk 1:83-91)
- **Description**: Central challenge for LLM-powered multi-agent architectures is finding optimal balance between autonomy and alignment. System should be aligned to human goals/intentions while accomplishing prompted goal in self-organizing manner. High autonomy risks straying from purpose; high alignment may lack flexibility.
- **Quote**: "One of the central challenges for the effective operation of LLM-powered multi-agent architectures (as with many AI systems) lies in finding the optimal _balance between autonomy and alignment_... a system with high autonomy may handle complex tasks efficiently, but risks straying from its intended purpose if not sufficiently aligned, resulting in unexpected consequences and uncontrollable side effects."
- **Context**: Framing the core challenge addressed by the taxonomy.

---

### Pattern: Goal-Driven Task Management with Divide and Conquer

- **Source**: 18-Multi-Agent_Architecture_Taxonomy_LLM (Chunk 1:453-461)
- **Description**: Systems accomplish user-prompted goals through interactive, multi-perspective strategy for problem solving (slow thinking). Complex tasks are broken down into smaller, manageable tasks distributed among agents with specific competencies. Effective orchestration and result synthesis is crucial.
- **Quote**: "When faced with such challenges, the system adeptly breaks down the complex task into smaller, manageable tasks. These sub-tasks are subsequently distributed among various agents, each equipped with specific competencies. A crucial aspect of this _divide & conquer_ strategy lies in the effective orchestration of these interconnected sub-tasks and the subsequent synthesis of partial results."
- **Context**: Description of the goal-driven task management characteristic.

---

### Pattern: LLM-Powered Intelligent Agents with Role, Memory, and Context

- **Source**: 18-Multi-Agent_Architecture_Taxonomy_LLM (Chunk 1:467-474)
- **Description**: Intelligent agents are foundational components with unique competencies: clearly defined role, individual memory, and access to contextual resources (data, tools, foundation models). LLM backbone enables reflection on tasks, planning, processing, utilizing resources, and communicating with other agents.
- **Quote**: "Each agent is endowed with a unique set of competencies, which include a clearly defined role, an individual memory, as well as access to further contextual resources, such as data, tools, or foundation models (see below), required for solving the tasks assigned to them. The backbone of their reasoning and interpretative capabilities is rooted in the incorporation of large language models (LLMs)."
- **Context**: Description of the agent composition characteristic.

---

### Pattern: Cognitive Synergy through Multi-Agent Collaboration

- **Source**: 18-Multi-Agent_Architecture_Taxonomy_LLM (Chunk 1:477-484)
- **Description**: Interaction layer provides workspace for network of collaborating LLM-powered agents. Agents collaborate via prompt-driven message exchanges to delegate responsibilities, seek assistance, or evaluate peer results. Power emerges from coordinated collective efforts (society of mind concept).
- **Quote**: "While executing the assigned tasks, these specialized agents collaborate with each other via prompt-driven message exchanges to delegate responsibilities, seek assistance, or evaluate the results of tasks undertaken by their peers. Key to the agents' collaboration is to effectively combine the strengths of each agent to collectively meet the defined goals, exemplifying _cognitive synergy_."
- **Context**: Description of multi-agent collaboration dynamics.

---

### Pattern: Context Interaction with External Resources

- **Source**: 18-Multi-Agent_Architecture_Taxonomy_LLM (Chunk 1:487-493)
- **Description**: Tasks require utilization of contextual resources: expert tools, data, specialized foundation models, or other applications. These extend ability to gather environmental information, create/modify artefacts, or initiate external processes.
- **Quote**: "Some tasks require the utilization of contextual resources, such as expert tools, data, further specialized foundation models, or other applications. These resources extend their ability to gather environmental information, create or modify artefacts, or initiate external processes."
- **Context**: Description of context interaction characteristic.

---

### Pattern: Triadic Interplay of Decision-Making Entities

- **Source**: 18-Multi-Agent_Architecture_Taxonomy_LLM (Chunk 1:496-506)
- **Description**: Complexity traced to triadic interplay and inherent tensions among: human users, LLM-powered agents, and governing mechanisms/rules integrated into system. Alignment ensures sync with human intentions; autonomy denotes capacity for self-organized operation.
- **Quote**: "this complexity can be traced back to the triadic interplay and inherent tensions among the primary _decision-making entities_ : human users, LLM-powered agents, and governing mechanisms or rules integrated into the system. _Alignment_, in this context, ensures that the system's actions are in sync with human intentions and values. On the other side of the spectrum, _autonomy_ denotes the agents' inherent capacity for self-organized strategy and operation."
- **Context**: Framework for understanding autonomy-alignment dynamics.

---

### Pattern: Task-Management Activity Phases

- **Source**: 18-Multi-Agent_Architecture_Taxonomy_LLM (Chunk 1:856-869)
- **Description**: Three core phases within Task-Management Activity: (1) Decomposition - breaking complex tasks into manageable Tasks/Sub-Tasks with dependency resolution, (2) Orchestration - organizing distribution and delegation among suitable Agents, (3) Synthesis - evaluating and combining Task Results to present unified Total Result.
- **Quote**: "- `Decomposition` : Breaking down complex tasks into manageable `Tasks` and `Sub-Tasks` ; optionally resolving dependencies between them, resulting in a prioritized list of `Tasks` . - `Orchestration` : Organizing the distribution and delegation of `Tasks` among suitable `Agents` . - `Synthesis` : Evaluating and combining `Task Results` as well as finally presenting a unified `Total` `Result`."
- **Context**: Detailed specification of task management phases.

---

### Pattern: Agent Type Classification

- **Source**: 18-Multi-Agent_Architecture_Taxonomy_LLM (Chunk 2:1-27)
- **Description**: Three generic agent types: (1) Task-Management Agents (Task-Creation, Task-Prioritization, Task-Execution), (2) Domain Role Agents (domain-specific experts like project manager, developer, QA engineer), (3) Technical Agents (interface with platforms/tools like SQL Agent, Python Agent).
- **Quote**: "- `Task-Management Agents` : These agents are specialized in organizing the processes related to the task-management activity... - `Domain Role Agents` : These agents are domain-specific experts. They excel in specialized roles within the application domain... - `Technical Agents` : These agents are tech-savvies, typically tasked with interfacing with technical platforms or development tools."
- **Context**: Classification of agent types within multi-agent systems.

---

### Pattern: Action Types in Multi-Agent Collaboration

- **Source**: 18-Multi-Agent_Architecture_Taxonomy_LLM (Chunk 2:30-49)
- **Description**: Six sub-types of Action performed by Agents: DecomposeTask, Create Task, DelegateTask (to Receiver agent), ExecuteTask, EvaluateResult, MergeResult. Each Action can include multiple LLM interactions for reflecting memories, observing results, planning steps, and weighing options.
- **Quote**: "- `DecomposeTask` : Breaking down a task into multiple sub-tasks, optionally ordering and prioritizing the tasks. - `Create Task` : Defining and generating new tasks. - `DelegateTask` : Delegating a task to another agent, addressed as `Receiver` . - `ExecuteTask` : Actually executing a given task. - `EvaluateResult` : Assessing the outcomes of a task. - `MergeResult` : Integrating or combining two or more task results."
- **Context**: Taxonomy of actions in multi-agent systems.

---

### Pattern: Prompt Augmentation for Agent Actions

- **Source**: 18-Multi-Agent_Architecture_Taxonomy_LLM (Chunk 2:56-68)
- **Description**: Before LLM receives Agent Prompt, it may undergo Prompt Augmentation. This process integrates additional specifics: parts of agent's Role or Memory, Context Information from previous utilization, or chosen Prompt Templates. This agent-driven prompt engineering is pivotal for LLM-powered multi-agent systems.
- **Quote**: "Before the LLM receives the `Agent Prompt`, it may undergo `Prompt Augmentation` [72]. This process can integrate additional specifics like the aspects or parts of the agent's `Role` or `Memory`, `Context Information` (e.g., data excerpts) acquired from previous `Context Utilization`, or chosen `Prompt Templates` prepared and/or adapted for certain kinds of actions."
- **Context**: Description of prompt engineering in multi-agent systems.

---

### Pattern: Communication Protocols for Agent Collaboration

- **Source**: 18-Multi-Agent_Architecture_Taxonomy_LLM (Chunk 2:71-93)
- **Description**: Three distinct protocols observable: (1) Strict finite processes with predefined action sequences and endpoints, (2) Dialogue cycles with alternating DelegateTask and ExecuteTask creating feedback loops, (3) Multi-cycle process frameworks with generic agent types allowing greater dynamism.
- **Quote**: "- _Strict finite processes_ or execution chains with predefined action sequences, interactions between predefined agents, and typically having a well-defined endpoint... - _Dialogue cycles_ characterized by alternating `DelegateTask` and `ExecuteTask` actions between two agents, creating a feedback loop of instruction and execution... - _Multi-cycle process frameworks_ with interactions between generic agent types, allowing for greater dynamism in agent interactions."
- **Context**: Classification of communication protocols in multi-agent systems.

---

### Pattern: Contextual Resource Types

- **Source**: 18-Multi-Agent_Architecture_Taxonomy_LLM (Chunk 2:99-166)
- **Description**: Context distinguished into Tools (Search/Analysis, Execution, Reasoning, Development, Communication), Data (Structured Text, Unstructured Text in vector databases, Multimodal, Domain-specific), and Foundation Models (NLP including LLMs, Computer Vision, Audio, Multimodal).
- **Quote**: "For executing the task-related actions, the LLM-powered agents are able to leverage specialized competencies and further information provided by additional `Context` which can be distinguished into `Tools`, `Data`, and `Foundation Models`."
- **Context**: Taxonomy of contextual resources for multi-agent systems.

---

### Pattern: Graph of Thoughts (GoT) Framework

- **Source**: 19-Graph_of_Thoughts_LLM_Reasoning (Chunk 1:17-28)
- **Description**: GoT models LLM-generated information as arbitrary graph where LLM thoughts are vertices and edges correspond to dependencies. Enables combining arbitrary thoughts into synergistic outcomes, distilling essence of thought networks, or enhancing thoughts using feedback loops.
- **Quote**: "The key idea and primary advantage of GoT is the ability to model the information generated by an LLM as an _arbitrary graph_, where units of information ('LLM thoughts') are vertices, and edges correspond to dependencies between these vertices. This approach enables combining arbitrary LLM thoughts into synergistic outcomes, distilling the essence of whole networks of thoughts, or enhancing thoughts using feedback loops."
- **Context**: Introduction to Graph of Thoughts framework.

---

### Pattern: Thought Transformation Operations

- **Source**: 19-Graph_of_Thoughts_LLM_Reasoning (Chunk 1:306-366)
- **Description**: Three primary graph-enabled thought transformations: (1) Aggregation - combining arbitrary thoughts into new ones to reinforce advantages and eliminate disadvantages, (2) Refining - modifying thought content through loops, (3) Generation - producing one or more new thoughts from existing single thought.
- **Quote**: "**Aggregation Transformations** First, with GoT, one can **aggregate arbitrary thoughts** into new ones, to combine and reinforce the advantages of these thoughts, while eliminating their disadvantages... **Refining Transformations** Another thought transformation is the **refining** of a current thought _v_ by modifying its content... **Generation Transformations** Finally, one can **generate one or more new thoughts based on an existing single thought**."
- **Context**: Description of core thought transformation operations in GoT.

---

### Pattern: GoT System Architecture Components

- **Source**: 19-Graph_of_Thoughts_LLM_Reasoning (Chunk 1:383-443)
- **Description**: GoT architecture consists of: Prompter (prepares LLM messages), Parser (extracts information from thoughts), Scoring module (verifies and scores thoughts), Controller (coordinates reasoning with Graph of Operations (GoO) and Graph Reasoning State (GRS)).
- **Quote**: "The GoT architecture consists of a set of interacting modules... These modules are the Prompter (prepares the messages for the LLM), the Parser (extracts information from LLM thoughts), the Scoring module (verifies and scores the LLM thoughts), and the Controller (coordinates the entire reasoning process, and decides on how to progress it)."
- **Context**: Description of GoT system architecture.

---

### Pattern: Volume of Thought Metric

- **Source**: 19-Graph_of_Thoughts_LLM_Reasoning (Chunk 1:728-753)
- **Description**: Volume metric measures number of preceding LLM thoughts that could have impacted a given thought. GoT offers superior latency-volume tradeoff: log_k N latency with N volume, compared to CoT (N/N), CoT-SC (N/k / N/k), or ToT (log_k N / O(log_k N)).
- **Quote**: "We define volume - for a given thought _t_ - as _the number of preceding LLM thoughts that could have im-pacted t_. Formally, the volume of _t_ is the number of thoughts from which there exists a path to _t_ in the graph of thoughts."
- **Context**: Introduction of novel evaluation metric for prompting strategies.

---

### Pattern: Merge-Based Reasoning for Complex Tasks

- **Source**: 19-Graph_of_Thoughts_LLM_Reasoning (Chunk 1:471-478)
- **Description**: For sorting, GoT employs merge-based approach: decompose input into subarrays, sort individually, then merge into final solution. This decomposition into simpler subtasks that are solved individually and then merged is well-suited for GoT.
- **Quote**: "In GoT, we employ merge-based sorting: First, one decomposes the input sequence of numbers into subarrays. Then, one sorts these subarrays individually, and then respectively merges them into a final solution."
- **Context**: Example of GoT application to sorting problem.

