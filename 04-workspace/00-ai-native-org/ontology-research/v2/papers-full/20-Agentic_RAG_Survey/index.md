---
paper_id: "20-Agentic_RAG_Survey"
title: "Agentic Retrieval-Augmented Generation: A Survey on Agentic RAG"
authors:
  - "Aditi Singh"
  - "Abul Ehtesham"
  - "Saket Kumar"
  - "Tala Talaei Khoei"
year: 2024
chunks_expected: 3
chunks_read: 3
analysis_complete: true
schema_version: "2.3"
high_priority_fields_found: 10

chunk_index:
  1:
    token_count: 10732
    fields_found:
      entity_types: true
      entity_definitions: true
      entity_relationships: true
      entity_count: partial
      abstraction_level: true
      framework_comparison: true
      methodology: partial
      ai_integration: true
      agent_modeling: true
      agentic_workflows: true
      generative_ai_patterns: true
      agent_ontology_integration: true
      empirical_evidence: false
      limitations: true
      tools_standards: partial
  2:
    token_count: 8622
    fields_found:
      entity_types: true
      entity_definitions: true
      entity_relationships: true
      entity_count: false
      abstraction_level: partial
      framework_comparison: true
      methodology: partial
      ai_integration: true
      agent_modeling: true
      agentic_workflows: true
      generative_ai_patterns: true
      agent_ontology_integration: true
      empirical_evidence: partial
      limitations: true
      tools_standards: partial
  3:
    token_count: 10695
    fields_found:
      entity_types: partial
      entity_definitions: partial
      entity_relationships: partial
      entity_count: false
      abstraction_level: false
      framework_comparison: partial
      methodology: false
      ai_integration: true
      agent_modeling: partial
      agentic_workflows: true
      generative_ai_patterns: partial
      agent_ontology_integration: true
      empirical_evidence: true
      limitations: true
      tools_standards: true

entity_types:
  - item: "Agent"
    chunk: 1
    lines: "484-501"
    quote: "In essence, an AI agent comprises: LLM (with defined Role and Task), Memory (Short-Term and Long-Term), Planning (Reflection & Self-Critique), Tools (Vector Search, Web Search, APIs, etc.)"
  - item: "LLM"
    chunk: 1
    lines: "487-489"
    quote: "LLM (with defined Role and Task): Serves as the agent's primary reasoning engine and dialogue interface. It interprets user queries, generates responses, and maintains coherence."
  - item: "Memory"
    chunk: 1
    lines: "491-493"
    quote: "Memory (Short-Term and Long-Term): Captures context and relevant data across interactions. Short-term memory tracks immediate conversation state, while long-term memory stores accumulated knowledge and agent experiences."
  - item: "Planning"
    chunk: 1
    lines: "496-497"
    quote: "Planning (Reflection & Self-Critique): Guides the agent's iterative reasoning process through reflection, query routing, or self-critique, ensuring that complex tasks are broken down effectively."
  - item: "Tools"
    chunk: 1
    lines: "500-501"
    quote: "Tools (Vector Search, Web Search, APIs, etc.): Expands the agent's capabilities beyond text generation, enabling access to external resources, real-time data, or specialized computations."
  - item: "Retriever"
    chunk: 1
    lines: "161-163"
    quote: "Retrieval: Responsible for querying external data sources such as knowledge bases, APIs, or vector databases. Advanced retrievers leverage dense vector search and transformer-based models to improve retrieval precision and semantic relevance."
  - item: "Augmentation"
    chunk: 1
    lines: "165-166"
    quote: "Augmentation: Processes retrieved data, extracting and summarizing the most relevant information to align with the query context."
  - item: "Generation"
    chunk: 1
    lines: "168-169"
    quote: "Generation: Combines retrieved information with the LLM's pre-trained knowledge to generate coherent, contextually appropriate responses."
  - item: "Coordinator Agent"
    chunk: 1
    lines: "764-766"
    quote: "The process begins when a user submits a query. A coordinating agent (or master retrieval agent) receives the query and analyzes it to determine the most suitable sources of information."
  - item: "Specialized Retrieval Agent"
    chunk: 1
    lines: "890-904"
    quote: "Specialized Retrieval Agents: The query is distributed among multiple retrieval agents, each focusing on a specific type of data source or task."

entity_definitions:
  Agent: "An intelligent entity capable of perceiving, reasoning, and autonomously executing tasks. Comprises LLM (reasoning engine), Memory (short-term and long-term), Planning (reflection & self-critique), and Tools (vector search, web search, APIs). Source: Chunk 1:484-501"
  Agentic_RAG: "Agentic Retrieval-Augmented Generation transcends traditional RAG limitations by embedding autonomous AI agents into the RAG pipeline. These agents leverage agentic design patterns - reflection, planning, tool use, and multi-agent collaboration - to dynamically manage retrieval strategies. Source: Chunk 1:55-60"
  Traditional_RAG: "Retrieval-Augmented Generation combines the generative capabilities of LLMs with external retrieval mechanisms to enhance relevance and timeliness of responses by retrieving real-time information from knowledge bases, APIs, or the web. Source: Chunk 1:96-101"
  Reflection: "A foundational design pattern in agentic workflows enabling agents to iteratively evaluate and refine their outputs through self-feedback mechanisms to identify and address errors, inconsistencies, and areas for improvement. Source: Chunk 1:515-531"
  Planning: "A key design pattern that enables agents to autonomously decompose complex tasks into smaller, manageable subtasks, essential for multi-hop reasoning and iterative problem-solving in dynamic scenarios. Source: Chunk 1:540-549"
  Tool_Use: "A pattern that enables agents to extend their capabilities by interacting with external tools, APIs, or computational resources, allowing them to gather information, perform computations, and manipulate data beyond pre-trained knowledge. Source: Chunk 1:555-569"
  Multi_Agent_Collaboration: "A design pattern enabling task specialization and parallel processing where agents communicate and share intermediate results, ensuring efficient and coherent workflows through distributed subtasks among specialized agents. Source: Chunk 1:575-597"
  Corrective_RAG: "A RAG paradigm that introduces mechanisms to self-correct retrieval results through intelligent agents, ensuring iterative refinement of context documents and responses while minimizing errors and maximizing relevance. Source: Chunk 2:190-263"
  Adaptive_RAG: "A RAG system that dynamically adjusts query handling strategies based on complexity of incoming queries, using a classifier to determine appropriate approach from single-step retrieval to multi-step reasoning. Source: Chunk 2:314-398"

entity_relationships:
  - relationship: "Agent contains LLM"
    chunk: 1
    lines: "484-489"
    quote: "In essence, an AI agent comprises: LLM (with defined Role and Task): Serves as the agent's primary reasoning engine and dialogue interface."
  - relationship: "Agent contains Memory"
    chunk: 1
    lines: "484-493"
    quote: "an AI agent comprises... Memory (Short-Term and Long-Term): Captures context and relevant data across interactions."
  - relationship: "Agent contains Planning"
    chunk: 1
    lines: "484-497"
    quote: "an AI agent comprises... Planning (Reflection & Self-Critique): Guides the agent's iterative reasoning process."
  - relationship: "Agent uses Tools"
    chunk: 1
    lines: "484-501"
    quote: "an AI agent comprises... Tools (Vector Search, Web Search, APIs, etc.): Expands the agent's capabilities beyond text generation."
  - relationship: "Agentic RAG extends Traditional RAG"
    chunk: 1
    lines: "55-60"
    quote: "Agentic Retrieval-Augmented Generation (Agentic RAG) transcends these limitations by embedding autonomous AI agents into the RAG pipeline."
  - relationship: "Coordinator Agent delegates to Specialized Agents"
    chunk: 1
    lines: "886-904"
    quote: "The process begins with a user query, which is received by a coordinator agent or master retrieval agent. This agent acts as the central orchestrator, delegating the query to specialized retrieval agents."
  - relationship: "Hierarchical Agent oversees Subordinate Agents"
    chunk: 2
    lines: "103-106"
    quote: "Agents are organized in a hierarchy, with higher-level agents overseeing and directing lower-level agents. This structure enables multi-level decision-making."
  - relationship: "Critic Module validates Retrieved Data"
    chunk: 2
    lines: "493-499"
    quote: "Critic Module: Validates retrieved data for relevance and quality. Flags low-confidence results for re-retrieval or refinement."

abstraction_level: "Application-level framework for AI agent architectures. The paper presents a taxonomy of Agentic RAG systems ranging from single-agent to multi-agent to hierarchical architectures, focusing on practical implementation patterns rather than foundational ontological theory. Source: Chunk 1:746-751"

framework_comparison:
  - comparison: "Naive RAG vs Advanced RAG vs Modular RAG vs Graph RAG vs Agentic RAG"
    chunk: 1
    lines: "419-426"
    quote: "Table 1 provides comparative analysis showing: Naive RAG uses keyword-based retrieval; Advanced RAG uses dense retrieval with multi-hop; Modular RAG uses hybrid retrieval with tool integration; Graph RAG integrates graph structures; Agentic RAG uses autonomous agents with dynamic decision-making."
  - comparison: "Traditional RAG vs Agentic RAG vs Agentic Document Workflows"
    chunk: 2
    lines: "810-870"
    quote: "Table 2 provides comprehensive comparative analysis: Traditional RAG has limited context maintenance and minimal dynamic adaptability; Agentic RAG enables context through memory modules with high adaptability; ADW maintains state across multi-step workflows with document-centric focus."
  - comparison: "Single-Agent vs Multi-Agent vs Hierarchical Agentic RAG"
    chunk: 1
    lines: "746-751"
    quote: "Agentic RAG systems can be categorized into distinct architectural frameworks based on their complexity and design principles. These include single-agent architectures, multi-agent systems, and hierarchical agentic architectures."

ai_integration:
  - pattern: "RAG Pipeline Integration"
    chunk: 1
    lines: "55-60"
    quote: "Agentic RAG transcends these limitations by embedding autonomous AI agents into the RAG pipeline. These agents leverage agentic design patterns - reflection, planning, tool use, and multi-agent collaboration."
  - pattern: "LLM as Reasoning Engine"
    chunk: 1
    lines: "487-489"
    quote: "LLM (with defined Role and Task): Serves as the agent's primary reasoning engine and dialogue interface. It interprets user queries, generates responses, and maintains coherence."
  - pattern: "Dynamic Retrieval Strategy Selection"
    chunk: 2
    lines: "317-328"
    quote: "Adaptive RAG dynamically tailors retrieval strategies based on query complexity: straightforward queries use pre-existing knowledge; simple queries perform single-step retrieval; complex queries employ multi-step retrieval."
  - pattern: "Graph-Enhanced RAG"
    chunk: 2
    lines: "449-452"
    quote: "Agent-G introduces a novel agentic architecture that integrates graph knowledge bases with unstructured document retrieval, combining structured and unstructured data sources."

agent_modeling:
  - model: "Autonomous Agent with Four Components"
    chunk: 1
    lines: "484-501"
    quote: "An AI agent comprises: LLM (with defined Role and Task), Memory (Short-Term and Long-Term), Planning (Reflection & Self-Critique), Tools (Vector Search, Web Search, APIs, etc.)"
  - model: "Role-Based Specialization"
    chunk: 1
    lines: "890-904"
    quote: "Specialized Retrieval Agents: Agent 1 handles structured queries (SQL databases); Agent 2 manages semantic searches; Agent 3 focuses on real-time public information; Agent 4 specializes in recommendation systems."
  - model: "Hierarchical Agent Structure"
    chunk: 2
    lines: "103-127"
    quote: "Agents are organized in a hierarchy, with higher-level agents overseeing and directing lower-level agents. Top-tier agent evaluates query complexity; Subordinate agents execute specialized tasks independently."

agentic_workflows:
  - workflow: "Prompt Chaining"
    chunk: 1
    lines: "620-632"
    quote: "Prompt chaining decomposes a complex task into multiple steps, where each step builds upon the previous one. This structured approach improves accuracy by simplifying each subtask before moving forward."
  - workflow: "Routing"
    chunk: 1
    lines: "644-668"
    quote: "Routing involves classifying an input and directing it to an appropriate specialized prompt or process. This method ensures distinct queries or tasks are handled separately, improving efficiency."
  - workflow: "Parallelization"
    chunk: 1
    lines: "671-693"
    quote: "Parallelization divides a task into independent processes that run simultaneously, reducing latency and improving throughput. It can be categorized into sectioning (independent subtasks) and voting (multiple outputs for accuracy)."
  - workflow: "Orchestrator-Workers"
    chunk: 1
    lines: "696-719"
    quote: "This workflow features a central orchestrator model that dynamically breaks tasks into subtasks, assigns them to specialized worker models, and compiles the results."
  - workflow: "Evaluator-Optimizer"
    chunk: 1
    lines: "721-740"
    quote: "The evaluator-optimizer workflow iteratively improves content by generating an initial output and refining it based on feedback from an evaluation model."
  - workflow: "Corrective RAG Workflow"
    chunk: 2
    lines: "226-244"
    quote: "The Corrective RAG system is built on five key agents: Context Retrieval Agent, Relevance Evaluation Agent, Query Refinement Agent, External Knowledge Retrieval Agent, Response Synthesis Agent."

generative_ai_patterns:
  - pattern: "Reflection/Self-Refine"
    chunk: 1
    lines: "515-531"
    quote: "Reflection is a foundational design pattern enabling agents to iteratively evaluate and refine their outputs. By incorporating self-feedback mechanisms, agents can identify and address errors. Studies like Self-Refine, Reflexion, and CRITIC demonstrate significant performance improvements."
  - pattern: "Planning/Task Decomposition"
    chunk: 1
    lines: "540-549"
    quote: "Planning enables agents to autonomously decompose complex tasks into smaller, manageable subtasks. This capability is essential for multi-hop reasoning and iterative problem-solving."
  - pattern: "Tool Use/Function Calling"
    chunk: 1
    lines: "555-569"
    quote: "Tool Use enables agents to extend their capabilities by interacting with external tools, APIs, or computational resources. The implementation has evolved significantly with advancements like GPT-4's function calling capabilities."
  - pattern: "Multi-Agent Collaboration"
    chunk: 1
    lines: "575-597"
    quote: "Multi-agent collaboration enables task specialization and parallel processing. Each agent operates with its own memory and workflow, which can include the use of tools, reflection, or planning."
  - pattern: "Iterative Refinement"
    chunk: 1
    lines: "361-362"
    quote: "Iterative Refinement: Incorporates feedback loops to improve retrieval accuracy and response relevance."

agent_ontology_integration:
  - integration: "Knowledge Graph RAG Integration"
    chunk: 2
    lines: "449-478"
    quote: "Agent-G introduces a novel agentic architecture that integrates graph knowledge bases with unstructured document retrieval. Graph Knowledge Bases provide structured data for extracting relationships, hierarchies, and connections."
  - integration: "Vector Database Integration"
    chunk: 3
    lines: "214-217"
    quote: "Neo4j, a prominent open-source graph database, excels in handling complex relationships and semantic queries. Alongside Neo4j, vector databases like Weaviate, Pinecone, Milvus, and Qdrant provide efficient similarity search."
  - integration: "Document Workflow Orchestration"
    chunk: 2
    lines: "704-708"
    quote: "Agentic Document Workflows extend traditional RAG by enabling end-to-end knowledge work automation. These workflows orchestrate complex document-centric processes, integrating document parsing, retrieval, reasoning, and structured outputs."

entity_count: null

methodology: "Survey methodology synthesizing existing literature on RAG paradigms and agentic AI systems. The paper provides a taxonomy-based analysis of Agentic RAG architectures with use case examples and comparative tables. Source: Chunk 1:63-67"

empirical_evidence:
  - evidence: "Twitch Ad Sales Case Study"
    chunk: 3
    lines: "5-8"
    quote: "Twitch leveraged an agentic workflow with RAG on Amazon Bedrock to streamline ad sales. The system dynamically retrieved advertiser data, historical campaign performance, and audience demographics to generate detailed ad proposals."
  - evidence: "Healthcare EHR Integration"
    chunk: 3
    lines: "31-34"
    quote: "Agentic RAG systems have been applied in generating patient case summaries. By integrating electronic health records (EHR) and up-to-date medical literature, the system generates comprehensive summaries for clinicians."
  - evidence: "Benchmark Datasets"
    chunk: 3
    lines: "223-282"
    quote: "Current benchmarks include BEIR, MS MARCO, TREC, MuSiQue, 2WikiMultihopQA, AgentG, HotpotQA, RAGBench, BERGEN, FlashRAG, and GNN-RAG for evaluating RAG systems."

limitations:
  - limitation: "Coordination Complexity"
    chunk: 1
    lines: "370-371"
    quote: "Coordination Complexity: Managing interactions between agents requires sophisticated orchestration mechanisms."
  - limitation: "Computational Overhead"
    chunk: 1
    lines: "374"
    quote: "Computational Overhead: The use of multiple agents increases resource requirements for complex workflows."
  - limitation: "Scalability Limitations"
    chunk: 1
    lines: "377-378"
    quote: "Scalability Limitations: While scalable, the dynamic nature of the system can strain computational resources for high query volumes."
  - limitation: "Lack of Specialized Benchmarks"
    chunk: 3
    lines: "354-357"
    quote: "The lack of specialized benchmarks and datasets tailored to evaluate agentic capabilities poses a significant hurdle. Developing evaluation methodologies that capture the unique aspects of Agentic RAG will be crucial."

tools_standards:
  - tool: "LangChain and LangGraph"
    chunk: 3
    lines: "164-167"
    quote: "LangChain provides modular components for building RAG pipelines. LangGraph complements this by introducing graph-based workflows that support loops, state persistence, and human-in-the-loop interactions."
  - tool: "LlamaIndex"
    chunk: 3
    lines: "169-172"
    quote: "LlamaIndex's Agentic Document Workflows (ADW) enable end-to-end automation of document processing, retrieval, and structured reasoning with a meta-agent architecture."
  - tool: "CrewAI and AutoGen"
    chunk: 3
    lines: "182-185"
    quote: "CrewAI supports hierarchical and sequential processes, robust memory systems, and tool integrations. AG2 (formerly AutoGen) excels in multi-agent collaboration with advanced support for code generation."
  - tool: "OpenAI Swarm Framework"
    chunk: 3
    lines: "188-189"
    quote: "An educational framework designed for ergonomic, lightweight multi-agent orchestration, emphasizing agent autonomy and structured collaboration."
  - tool: "Semantic Kernel"
    chunk: 3
    lines: "198-202"
    quote: "Semantic Kernel is an open-source SDK by Microsoft that integrates large language models into applications. It supports agentic patterns, enabling creation of autonomous AI agents."
  - tool: "Vector Databases"
    chunk: 3
    lines: "214-217"
    quote: "Neo4j, Weaviate, Pinecone, Milvus, and Qdrant provide efficient similarity search and retrieval capabilities, forming the backbone of high-performance Agentic RAG workflows."
---

# Agentic Retrieval-Augmented Generation: A Survey on Agentic RAG

## Summary

This comprehensive survey explores Agentic Retrieval-Augmented Generation (Agentic RAG), a paradigm that integrates autonomous AI agents into the RAG pipeline to overcome limitations of traditional RAG systems. The paper provides:

1. **Foundational Principles**: Evolution from Naive RAG through Advanced RAG, Modular RAG, and Graph RAG to Agentic RAG
2. **Agent Architecture**: Four-component model (LLM, Memory, Planning, Tools) for AI agents
3. **Agentic Patterns**: Reflection, Planning, Tool Use, and Multi-Agent Collaboration
4. **Workflow Patterns**: Prompt Chaining, Routing, Parallelization, Orchestrator-Workers, Evaluator-Optimizer
5. **System Taxonomy**: Single-Agent, Multi-Agent, Hierarchical, Corrective, Adaptive, and Graph-Based architectures
6. **Applications**: Healthcare, Finance, Legal, Education, Customer Support domains
7. **Tools and Frameworks**: LangChain, LlamaIndex, CrewAI, AutoGen, Semantic Kernel, and vector databases

## Key Contributions to Ontology Research

### Agent-Activity-Entity Triad Relevance
The paper validates an agent-centric model where:
- **Agent**: Autonomous entity with LLM, Memory, Planning, and Tools
- **Activity**: Retrieval, Augmentation, Generation, and Workflow orchestration
- **Entity**: Queries, Documents, Knowledge Bases, Responses

### Entity Type Mappings to 8-Entity Hypothesis
| Paper Entity | 8-Entity Mapping |
|-------------|------------------|
| Agent (Coordinator, Specialized) | Agent |
| LLM, Memory, Planning | Resource |
| Query, Response | Data |
| Workflow Patterns | Task |
| Tools, APIs | Resource |
| Agentic Patterns | Rule |
| Agent Roles | Role |
| Retrieval/Generation Events | Event |

### AI Integration Patterns
1. **Dynamic Retrieval Strategy Selection**: Adaptive approaches based on query complexity
2. **Multi-Agent Orchestration**: Hierarchical and parallel agent coordination
3. **Graph-Enhanced RAG**: Integration of knowledge graphs with unstructured retrieval
4. **Iterative Refinement**: Self-correction through reflection and feedback loops

## Relevance Score: HIGH

This paper is highly relevant to the research questions as it provides:
- Detailed agent modeling with explicit component definitions
- Comprehensive workflow patterns for agentic systems
- Framework comparisons across RAG paradigms
- Practical tool and implementation guidance for AI-ontology integration

---

## Citation

```bibtex
@article{singh2024agenticrag,
  title={Agentic Retrieval-Augmented Generation: A Survey on Agentic RAG},
  author={Singh, Aditi and Ehtesham, Abul and Kumar, Saket and Khoei, Tala Talaei},
  journal={arXiv preprint},
  year={2024},
  url={https://github.com/asinghcsu/AgenticRAG-Survey}
}
```
