---
batch_id: 2
field: generative_ai_patterns
papers_read: [20-Agentic_RAG_Survey, 21-LLM_Smart_Contracts_from_BPMN]
chunks_read: 4
patterns_found: 32
extracted_at: "2025-12-28T12:00:00Z"
---

# Batch Extraction: generative_ai_patterns (Batch 2)

## Patterns Extracted

---

### Pattern: Agentic Design Patterns (Core Four)

- **Source**: 20-Agentic_RAG_Survey (Chunk 1:55-57)
- **Description**: Four foundational agentic design patterns that enable autonomous AI agents to dynamically manage retrieval strategies and adapt workflows: reflection, planning, tool use, and multi-agent collaboration.
- **Quote**: "These agents leverage agentic design patterns - reflection, planning, tool use, and multi-agent collaboration - to dynamically manage retrieval strategies, iteratively refine contextual understanding, and adapt workflows through clearly defined operational structures ranging from sequential steps to adaptive collaboration."
- **Context**: Introduced in the abstract as the core patterns that distinguish Agentic RAG from traditional RAG systems, enabling unparalleled flexibility, scalability, and context-awareness.

---

### Pattern: Reflection Pattern

- **Source**: 20-Agentic_RAG_Survey (Chunk 1:515-531)
- **Description**: A foundational design pattern enabling agents to iteratively evaluate and refine their outputs through self-feedback mechanisms. Agents critique their outputs for correctness, style, and efficiency, then incorporate this feedback into subsequent iterations. Can involve distinct roles in multi-agent systems where one agent generates outputs while another critiques them.
- **Quote**: "Reflection is a foundational design pattern in agentic workflows, enabling agents to iteratively evaluate and refine their outputs. By incorporating self-feedback mechanisms, agents can identify and address errors, inconsistencies, and areas for improvement, enhancing performance across tasks like code generation, text production, and question answering"
- **Context**: External tools like unit tests or web searches can enhance this process by validating results. Referenced studies include Self-Refine, Reflexion, and CRITIC.

---

### Pattern: Planning Pattern

- **Source**: 20-Agentic_RAG_Survey (Chunk 1:540-549)
- **Description**: A key design pattern enabling agents to autonomously decompose complex tasks into smaller, manageable subtasks. Essential for multi-hop reasoning and iterative problem-solving in dynamic and uncertain scenarios. Agents dynamically determine the sequence of steps needed to accomplish larger objectives.
- **Quote**: "Planning is a key design pattern in agentic workflows that enables agents to autonomously decompose complex tasks into smaller, manageable subtasks. This capability is essential for multi-hop reasoning and iterative problem-solving in dynamic and uncertain scenarios"
- **Context**: While powerful, Planning can produce less predictable outcomes compared to deterministic workflows like Reflection. Suited for tasks requiring dynamic adaptation where predefined workflows are insufficient.

---

### Pattern: Tool Use Pattern

- **Source**: 20-Agentic_RAG_Survey (Chunk 1:555-569)
- **Description**: Enables agents to extend their capabilities by interacting with external tools, APIs, or computational resources. Allows agents to gather information, perform computations, and manipulate data beyond their pre-trained knowledge. Modern implementations include GPT-4's function calling capabilities.
- **Quote**: "Tool Use enables agents to extend their capabilities by interacting with external tools, APIs, or computational resources. This pattern allows agents to gather information, perform computations, and manipulate data beyond their pre-trained knowledge. By dynamically integrating tools into workflows, agents can adapt to complex tasks and provide more accurate and contextually relevant outputs."
- **Context**: Has evolved significantly with advancements like GPT-4's function calling capabilities. Challenges remain in optimizing tool selection, with RAG-inspired heuristic-based selection proposed as a solution.

---

### Pattern: Multi-Agent Collaboration Pattern

- **Source**: 20-Agentic_RAG_Survey (Chunk 1:575-597)
- **Description**: A key design pattern enabling task specialization and parallel processing through multiple agents that communicate and share intermediate results. Each agent operates with its own memory and workflow, which can include use of tools, reflection, or planning, enabling dynamic and collaborative problem-solving.
- **Quote**: "Multi-agent collaboration is a key design pattern in agentic workflows that enables task specialization and parallel processing. Agents communicate and share intermediate results, ensuring the overall workflow remains efficient and coherent. By distributing subtasks among specialized agents, this pattern improves the scalability and adaptability of complex workflows."
- **Context**: Less predictable than Reflection and Tool Use patterns. Emerging frameworks include AutoGen, Crew AI, and LangGraph.

---

### Pattern: Prompt Chaining Workflow

- **Source**: 20-Agentic_RAG_Survey (Chunk 1:620-642)
- **Description**: Decomposes a complex task into multiple sequential steps, where each step builds upon the previous one. This structured approach improves accuracy by simplifying each subtask before moving forward, though it may increase latency due to sequential processing.
- **Quote**: "Prompt chaining decomposes a complex task into multiple steps, where each step builds upon the previous one. This structured approach improves accuracy by simplifying each subtask before moving forward. However, it may increase latency due to sequential processing."
- **Context**: Most effective when a task can be broken down into fixed subtasks. Example applications include generating marketing content in one language then translating it, and structuring document creation by generating outline, verifying completeness, then developing full text.

---

### Pattern: Routing Workflow

- **Source**: 20-Agentic_RAG_Survey (Chunk 1:645-668)
- **Description**: Classifies an input and directs it to an appropriate specialized prompt or process. Ensures distinct queries or tasks are handled separately, improving efficiency and response quality.
- **Quote**: "Routing involves classifying an input and directing it to an appropriate specialized prompt or process. This method ensures distinct queries or tasks are handled separately, improving efficiency and response quality."
- **Context**: Ideal for scenarios where different types of input require distinct handling strategies. Examples include directing customer service queries into categories (technical support, refund requests, general inquiries) and assigning simple queries to smaller models while complex requests go to advanced models.

---

### Pattern: Parallelization Workflow

- **Source**: 20-Agentic_RAG_Survey (Chunk 1:671-694)
- **Description**: Divides a task into independent processes that run simultaneously, reducing latency and improving throughput. Can be categorized into sectioning (independent subtasks) and voting (multiple outputs for accuracy).
- **Quote**: "Parallelization divides a task into independent processes that run simultaneously, reducing latency and improving throughput. It can be categorized into sectioning (independent subtasks) and voting (multiple outputs for accuracy)."
- **Context**: Useful when tasks can be executed independently to enhance speed or when multiple outputs improve confidence. Examples include content moderation with parallel screening and response generation, and multiple models cross-checking code for vulnerabilities.

---

### Pattern: Orchestrator-Workers Workflow

- **Source**: 20-Agentic_RAG_Survey (Chunk 1:696-719)
- **Description**: Features a central orchestrator model that dynamically breaks tasks into subtasks, assigns them to specialized worker models, and compiles the results. Unlike parallelization, it adapts to varying input complexity with real-time task decomposition.
- **Quote**: "This workflow features a central orchestrator model that dynamically breaks tasks into subtasks, assigns them to specialized worker models, and compiles the results. Unlike parallelization, it adapts to varying input complexity."
- **Context**: Best suited for tasks requiring dynamic decomposition and real-time adaptation where subtasks are not predefined. Examples include automatically modifying multiple files in a codebase and conducting real-time research by gathering and synthesizing information from multiple sources.

---

### Pattern: Evaluator-Optimizer Workflow

- **Source**: 20-Agentic_RAG_Survey (Chunk 1:721-741)
- **Description**: Iteratively improves content by generating an initial output and refining it based on feedback from an evaluation model. Creates a feedback loop between generation and evaluation.
- **Quote**: "The evaluator-optimizer workflow iteratively improves content by generating an initial output and refining it based on feedback from an evaluation model."
- **Context**: Effective when iterative refinement significantly enhances response quality, especially when clear evaluation criteria exist. Examples include improving literary translations through multiple evaluation cycles and multi-round research queries.

---

### Pattern: Iterative Retrieval (Multi-hop Reasoning)

- **Source**: 20-Agentic_RAG_Survey (Chunk 1:253-255)
- **Description**: Advanced RAG introduces multi-hop retrieval mechanisms, enabling reasoning across multiple documents for complex queries. Allows the system to iteratively refine and retrieve information.
- **Quote**: "Iterative Retrieval: Advanced RAG introduces multi-hop retrieval mechanisms, enabling reasoning across multiple documents for complex queries."
- **Context**: Part of Advanced RAG paradigm that builds upon limitations of Naive RAG through semantic understanding and enhanced retrieval techniques.

---

### Pattern: Dense Vector Search

- **Source**: 20-Agentic_RAG_Survey (Chunk 1:245-247)
- **Description**: Queries and documents are represented in high-dimensional vector spaces, enabling better semantic alignment between user query and retrieved documents.
- **Quote**: "Dense Vector Search: Queries and documents are represented in high-dimensional vector spaces, enabling better semantic alignment between the user query and retrieved documents."
- **Context**: A key feature of Advanced RAG systems that improves retrieval precision over keyword-based approaches.

---

### Pattern: Contextual Re-Ranking

- **Source**: 20-Agentic_RAG_Survey (Chunk 1:249-250)
- **Description**: Neural models re-rank retrieved documents to prioritize the most contextually relevant information.
- **Quote**: "Contextual Re-Ranking: Neural models re-rank retrieved documents to prioritize the most contextually relevant information."
- **Context**: Part of Advanced RAG enhancements that improve upon simple keyword-based retrieval.

---

### Pattern: Hybrid Retrieval Strategies

- **Source**: 20-Agentic_RAG_Survey (Chunk 1:274-276)
- **Description**: Combining sparse retrieval methods (e.g., BM25) with dense retrieval techniques (e.g., DPR - Dense Passage Retrieval) to maximize accuracy across diverse query types.
- **Quote**: "Hybrid Retrieval Strategies: Combining sparse retrieval methods (e.g., a sparse encoder-BM25) with dense retrieval techniques (e.g., DPR - Dense Passage Retrieval) to maximize accuracy across diverse query types."
- **Context**: Key innovation in Modular RAG that enables more flexible and accurate retrieval.

---

### Pattern: AI Agent Component Architecture

- **Source**: 20-Agentic_RAG_Survey (Chunk 1:484-501)
- **Description**: An AI agent comprises four core components: LLM (with defined Role and Task) as the primary reasoning engine; Memory (Short-Term and Long-Term) for capturing context; Planning (Reflection & Self-Critique) for iterative reasoning; and Tools (Vector Search, Web Search, APIs) for expanding capabilities.
- **Quote**: "In essence, an AI agent comprises: LLM (with defined Role and Task): Serves as the agent's primary reasoning engine and dialogue interface. Memory (Short-Term and Long-Term): Captures context and relevant data across interactions. Planning (Reflection & Self-Critique): Guides the agent's iterative reasoning process through reflection, query routing, or self-critique. Tools (Vector Search, Web Search, APIs, etc.): Expands the agent's capabilities beyond text generation"
- **Context**: Foundational architecture description for AI agents that underpins Agentic RAG systems.

---

### Pattern: Single-Agent Router Architecture

- **Source**: 20-Agentic_RAG_Survey (Chunk 1:755-825)
- **Description**: A centralized decision-making system where a single agent manages retrieval, routing, and integration of information. The agent evaluates queries, selects knowledge sources (structured databases, semantic search, web search, recommendation systems), integrates data, and synthesizes responses through an LLM.
- **Quote**: "A Single-Agent Agentic RAG serves as a centralized decision-making system where a single agent manages the retrieval, routing, and integration of information. This architecture simplifies the system by consolidating these tasks into one unified agent"
- **Context**: Particularly effective for setups with limited number of tools or data sources. Advantages include centralized simplicity, efficiency, dynamic routing, and versatility across tools.

---

### Pattern: Multi-Agent RAG Architecture

- **Source**: 20-Agentic_RAG_Survey (Chunk 1:877-968)
- **Description**: A modular and scalable architecture that distributes responsibilities across multiple specialized agents instead of relying on a single agent. Features a coordinator agent that delegates to specialized retrieval agents, each optimized for specific data sources or tasks.
- **Quote**: "Multi-Agent RAG represents a modular and scalable evolution of single-agent architectures, designed to handle complex workflows and diverse query types by leveraging multiple specialized agents. Instead of relying on a single agent to manage all tasks—reasoning, retrieval, and response generation—this system distributes responsibilities across multiple agents, each optimized for a specific role or data source."
- **Context**: Enables parallel processing, task specialization, and scalability. Challenges include coordination complexity, computational overhead, and data integration across diverse sources.

---

### Pattern: Hierarchical Agentic RAG Architecture

- **Source**: 20-Agentic_RAG_Survey (Chunk 2:100-161)
- **Description**: A structured, multi-tiered approach where agents are organized in a hierarchy with higher-level agents overseeing and directing lower-level agents. Top-tier agents assess query complexity and delegate to subordinate specialized agents.
- **Quote**: "Hierarchical Agentic RAG systems employ a structured, multi-tiered approach to information retrieval and processing, enhancing both efficiency and strategic decision-making. Agents are organized in a hierarchy, with higher-level agents overseeing and directing lower-level agents. This structure enables multi-level decision-making, ensuring that queries are handled by the most appropriate resources."
- **Context**: Enables strategic prioritization based on query complexity, reliability, or context. Top-tier agents can prioritize data sources and apply strategic oversight to improve accuracy.

---

### Pattern: Corrective RAG

- **Source**: 20-Agentic_RAG_Survey (Chunk 2:190-263)
- **Description**: Introduces mechanisms to self-correct retrieval results through multiple specialized agents: Context Retrieval Agent, Relevance Evaluation Agent, Query Refinement Agent, External Knowledge Retrieval Agent, and Response Synthesis Agent. Documents below relevance threshold trigger corrective steps.
- **Quote**: "Corrective RAG introduces mechanisms to self-correct retrieval results, enhancing document utilization and improving response generation quality. By embedding intelligent agents into the workflow, Corrective RAG ensures iterative refinement of context documents and responses, minimizing errors and maximizing relevance."
- **Context**: Key features include iterative correction, dynamic adaptability with real-time web searches, agentic modularity, and factuality assurance to minimize hallucination or misinformation.

---

### Pattern: Adaptive RAG

- **Source**: 20-Agentic_RAG_Survey (Chunk 2:317-398)
- **Description**: Dynamically adjusts query handling strategies based on complexity using a classifier. For straightforward queries, bypasses retrieval; for simple queries, performs single-step retrieval; for complex queries, employs multi-step retrieval with iterative refinement.
- **Quote**: "Adaptive Retrieval-Augmented Generation (Adaptive RAG) enhances the flexibility and efficiency of large language models (LLMs) by dynamically adjusting query handling strategies based on the complexity of the incoming query. Unlike static retrieval workflows, Adaptive RAG employs a classifier to assess query complexity and determine the most appropriate approach, ranging from single-step retrieval to multi-step reasoning, or even bypassing retrieval altogether for straightforward queries"
- **Context**: Key features include dynamic adaptability, resource efficiency (minimizes overhead for simple queries), enhanced accuracy through iterative refinement, and flexibility to incorporate domain-specific tools or external APIs.

---

### Pattern: Agent-G (Graph RAG Agentic Framework)

- **Source**: 20-Agentic_RAG_Survey (Chunk 2:449-533)
- **Description**: An agentic architecture that integrates graph knowledge bases with unstructured document retrieval. Features modular retriever banks, dynamic agent interaction, a critic module for validating relevance and quality, and feedback loops for iterative refinement.
- **Quote**: "Agent-G introduces a novel agentic architecture that integrates graph knowledge bases with unstructured document retrieval. By combining structured and unstructured data sources, this framework enhances retrieval-augmented generation (RAG) systems with improved reasoning and retrieval accuracy."
- **Context**: The critic module evaluates relevance and flags low-confidence results for re-retrieval. Supports scalable modularity through addition of new agents for specialized tasks.

---

### Pattern: GeAR (Graph-Enhanced Agent for RAG)

- **Source**: 20-Agentic_RAG_Survey (Chunk 2:586-658)
- **Description**: Enhances traditional RAG through graph expansion techniques and agent-based architecture. Graph expansion integrates graph-based data into retrieval, enabling multi-hop queries. Agents autonomously decide to utilize graph-expanded retrieval paths.
- **Quote**: "GeAR introduces an agentic framework that enhances traditional Retrieval-Augmented Generation (RAG) systems by incorporating graph-based retrieval mechanisms. By leveraging graph expansion techniques and an agent-based architecture, GeAR addresses challenges in multi-hop retrieval scenarios"
- **Context**: Key innovations include graph expansion (enhancing base retrievers like BM25 with graph-structured data) and agent framework (utilizing graph expansion for autonomous decision-making).

---

### Pattern: Agentic Document Workflows (ADW)

- **Source**: 20-Agentic_RAG_Survey (Chunk 2:701-801)
- **Description**: End-to-end knowledge work automation that orchestrates complex document-centric processes. Integrates document parsing, retrieval, reasoning, and structured outputs with intelligent agents. Maintains state across multi-step workflows and applies domain-specific logic.
- **Quote**: "Agentic Document Workflows (ADW) extend traditional Retrieval-Augmented Generation (RAG) paradigms by enabling end-to-end knowledge work automation. These workflows orchestrate complex document-centric processes, integrating document parsing, retrieval, reasoning, and structured outputs with intelligent agents."
- **Context**: Workflow includes document parsing and information structuring, state maintenance across processes, knowledge retrieval from external bases, agentic orchestration with business rules, and actionable output generation.

---

### Pattern: Zero-Shot Prompting

- **Source**: 21-LLM_Smart_Contracts_from_BPMN (Chunk 1:144-147)
- **Description**: Models complete tasks based solely on instructions without prior examples. The model leverages its pre-trained knowledge to perform tasks without being shown any examples of the specific task.
- **Quote**: "In zero-shot prompting, models complete tasks based solely on instructions without prior examples, whereas few-shot prompting involves providing a handful of illustrative examples directly within the input"
- **Context**: Enables LLMs to deliver high performance out of the box for many usage scenarios, eliminating the need for fine-tuning or training from scratch.

---

### Pattern: Few-Shot Prompting

- **Source**: 21-LLM_Smart_Contracts_from_BPMN (Chunk 1:144-147)
- **Description**: Providing a handful of illustrative examples directly within the input to guide the model's response. Contrasted with zero-shot prompting which provides no examples.
- **Quote**: "In zero-shot prompting, models complete tasks based solely on instructions without prior examples, whereas few-shot prompting involves providing a handful of illustrative examples directly within the input"
- **Context**: Used in the paper's experiments with one-shot and two-shot variants to test smart contract generation from BPMN models.

---

### Pattern: Temperature Control for Output Determinism

- **Source**: 21-LLM_Smart_Contracts_from_BPMN (Chunk 1:171-174)
- **Description**: A setting that controls randomness of generated text. Lower temperatures make outputs more predictable and focused by selecting most probable tokens; higher temperatures encourage more creative and varied responses by selecting less probable tokens.
- **Quote**: "Temperature is a setting for LLMs that controls the randomness of generated text; lower temperatures make outputs more predictable and focused (by selecting the most probable tokens), while higher temperatures encourage more creative and varied responses (by selecting less probable tokens)."
- **Context**: The experiment used temperature set to 0 for quasi-deterministic inference results, though tie breaking between tokens of equal probabilities may still cause stochasticity.

---

### Pattern: Reasoning Models (Chain-of-Thought Generation)

- **Source**: 21-LLM_Smart_Contracts_from_BPMN (Chunk 1:156-163)
- **Description**: Models that perform complex reasoning by generating a plan to answer a query, executing the steps in the plan, and possibly checking their work. Require many more tokens than regular LLMs due to the planning and verification process.
- **Quote**: "Models that perform complex reasoning (so called reasoning models) typically generate a plan to answer a query, execute the steps in the plan, and possibly check their work; hence they require many more tokens than regular LLMs."
- **Context**: Balancing model size, token usage, and capability is essential for developing efficient and sustainable LLM-based applications.

---

### Pattern: LLM Judge Evaluation

- **Source**: 21-LLM_Smart_Contracts_from_BPMN (Chunk 1:194-197)
- **Description**: An evaluation approach where LLMs assess the output of other LLMs, particularly useful for open-ended tasks that are difficult to evaluate automatically.
- **Quote**: "A similar study to ours was conducted by Berti et al., which presents a benchmark on the performance of LLMs for different Process Mining tasks, the open-ended nature of these tasks requires a LLM judge evaluation approach, where LLMs assess the output of other LLMs."
- **Context**: Used when the open-ended nature of tasks makes traditional automated evaluation difficult. Referenced from PM-LLM-Benchmark study.

---

### Pattern: LLM for Code Generation from Models

- **Source**: 21-LLM_Smart_Contracts_from_BPMN (Chunk 1:12-27)
- **Description**: Using LLMs to generate executable code from process descriptions or models, aiming to overcome limitations of traditional rule-based code generation approaches. Explored for generating smart contracts from BPMN business process descriptions.
- **Quote**: "Large language models (LLMs) have changed the reality of how software is produced. Within the wider software engineering community, among many other purposes, they are explored for code generation use cases from different types of input. In this work, we present an exploratory study to investigate the use of LLMs for generating smart contract code from business process descriptions, an idea that has emerged in recent literature to overcome the limitations of traditional rule-based code generation approaches."
- **Context**: Current LLM-based work evaluates generated code on small samples using manual inspection or testing whether code compiles while ignoring correct execution. The study introduces automated evaluation framework for larger datasets.

---

### Pattern: LLM Non-Determinism Challenge

- **Source**: 21-LLM_Smart_Contracts_from_BPMN (Chunk 1:67-68)
- **Description**: LLM outputs are inherently non-deterministic, making them unreliable for consistent behavior in contexts requiring perfect reliability like smart contracts.
- **Quote**: "LLM outputs are inherently non-deterministic, making them unreliable for consistent behaviour."
- **Context**: Identified as a fundamental challenge for using LLMs in blockchain-based smart contracts where any weakness may be exploited. Even temperature=0 settings produce quasi-deterministic results with potential stochasticity from tie-breaking.

---

### Pattern: LLM-Assisted Verification and Enhancement

- **Source**: 21-LLM_Smart_Contracts_from_BPMN (Chunk 1:650-670)
- **Description**: Using LLMs not to directly generate production code, but to propose code snippets that are then verified against formal specifications or using automated theorem provers. LLMs can also generate test cases, identify vulnerabilities, and extend functionality of existing code generation tools.
- **Quote**: "Future work should explore integrating LLM capabilities into existing smart contract generation tools. For smart contract development, which demands high security, LLM integration must rely on extensive evaluation and robust verification of generated outcomes. This could involve using LLMs to propose code snippets or modifications, which are then rigorously checked against formal specifications or verified using automated theorem provers, before being considered."
- **Context**: Proposed as a responsible integration pattern where LLMs enhance rather than replace existing tools. Includes generating flexible templates, code snippets for edge cases, suggesting optimizations, and assisting in translation between languages/platforms.

---

### Pattern: Structured Output from LLMs (Token-Based Process Execution)

- **Source**: 21-LLM_Smart_Contracts_from_BPMN (Chunk 1:482-485)
- **Description**: Prompting LLMs to generate code following specific structural patterns, such as using bitmasking techniques for encoding state in smart contracts for more efficient token-based execution.
- **Quote**: "Our prompt also specifies that the state of the contract should be encoded using a bitmasking technique, as it is the most efficient encoding for a token-based execution. This variant did, on average, not perform worse than a prompt asking for a more naive implementation during our pre-runs."
- **Context**: Demonstrates how structured output requirements can be incorporated into prompts to guide LLM code generation toward efficient implementations.

---

