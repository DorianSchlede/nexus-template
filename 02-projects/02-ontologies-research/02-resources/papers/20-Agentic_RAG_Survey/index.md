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
high_priority_fields_found: 9

# Extraction fields
entity_types:
  - "Agent"
  - "Activity"
  - "Entity"
  - "Tool"
  - "Memory"
  - "Goal"
  - "Data"

entity_definitions:
  Agent: "An intelligent entity capable of perceiving, reasoning, and autonomously executing tasks, comprising LLM, Memory, Planning, and Tools (Chunk 1:104-107, 484-502)"
  Agentic_RAG: "A paradigm that embeds autonomous AI agents into the RAG pipeline, enabling dynamic retrieval strategies, contextual understanding, and iterative refinement (Chunk 1:55-60)"
  Memory: "Short-term memory tracks immediate conversation state; long-term memory stores accumulated knowledge and agent experiences (Chunk 1:491-493)"
  Tool: "External capabilities including Vector Search, Web Search, APIs that expand the agent's capabilities beyond text generation (Chunk 1:500-501)"

entity_relationships:
  - from: "Agent"
    to: "LLM"
    relationship: "contains"
    source: "Chunk 1:487-488"
  - from: "Agent"
    to: "Memory"
    relationship: "contains"
    source: "Chunk 1:491-493"
  - from: "Agent"
    to: "Tool"
    relationship: "uses"
    source: "Chunk 1:500-501"
  - from: "Agent"
    to: "Activity"
    relationship: "performs"
    source: "Chunk 1:104-107"
  - from: "Coordinator_Agent"
    to: "Specialized_Agent"
    relationship: "delegates_to"
    source: "Chunk 1:886-888"

abstraction_level: "application"

framework_comparison:
  - compared_to: "Traditional RAG"
    relationship: "extends"
    details: "Agentic RAG overcomes static workflows and limited contextual adaptability through autonomous agents"
    source: "Chunk 1:461-472"
  - compared_to: "Graph RAG"
    relationship: "integrates_with"
    details: "Agent-G and GeAR combine graph knowledge bases with agentic retrieval"
    source: "Chunk 2:449-452, 586-600"
  - compared_to: "Modular RAG"
    relationship: "builds_upon"
    details: "Agentic RAG builds on modularity while adding agent-based autonomy"
    source: "Chunk 1:344-346"

ai_integration:
  - pattern: "Dynamic Retrieval"
    description: "Agents autonomously manage retrieval strategies based on query complexity"
    source: "Chunk 1:357-358"
  - pattern: "Query Reformulation"
    description: "Query Refinement Agent rewrites queries to improve retrieval precision"
    source: "Chunk 2:208-209, 236-237"
  - pattern: "Multi-Step Reasoning"
    description: "Iterative retrieval and refinement for complex queries"
    source: "Chunk 2:342-344"
  - pattern: "Knowledge Graph Integration"
    description: "Agent-G integrates graph knowledge bases with document retrieval"
    source: "Chunk 2:449-452"

agent_modeling:
  - aspect: "Component Architecture"
    description: "Agent = LLM + Memory + Planning + Tools"
    source: "Chunk 1:484-502"
  - aspect: "Memory Types"
    description: "Short-term (conversation state) and long-term (accumulated knowledge)"
    source: "Chunk 1:491-493"
  - aspect: "Autonomous Decision-Making"
    description: "Agents independently evaluate and manage retrieval strategies"
    source: "Chunk 1:357-358"
  - aspect: "Self-Correction"
    description: "Agents can self-correct through reflection and feedback loops"
    source: "Chunk 1:515-525"

agentic_workflows:
  - pattern: "Prompt Chaining"
    description: "Sequential processing where each step builds on previous output"
    source: "Chunk 1:620-632"
  - pattern: "Routing"
    description: "Classification-based input direction to specialized processes"
    source: "Chunk 1:644-655"
  - pattern: "Parallelization"
    description: "Concurrent execution of independent tasks (sectioning/voting)"
    source: "Chunk 1:671-676"
  - pattern: "Orchestrator-Workers"
    description: "Central orchestrator delegates to specialized worker agents"
    source: "Chunk 1:696-707"
  - pattern: "Evaluator-Optimizer"
    description: "Iterative refinement through evaluation feedback"
    source: "Chunk 1:721-731"

generative_ai_patterns:
  - pattern: "Reflection"
    description: "Agents iteratively evaluate and refine outputs through self-feedback"
    source: "Chunk 1:512-531"
  - pattern: "Planning"
    description: "Autonomous task decomposition into manageable subtasks"
    source: "Chunk 1:540-549"
  - pattern: "Tool Use"
    description: "External tool/API interaction for extended capabilities"
    source: "Chunk 1:555-569"
  - pattern: "Multi-Agent Collaboration"
    description: "Task specialization and parallel processing via agent communication"
    source: "Chunk 1:575-592"
  - pattern: "Self-Refine"
    description: "Iterative refinement with self-feedback mechanisms"
    source: "Chunk 1:531"
  - pattern: "ReAct"
    description: "Referenced as agentic pattern foundation"
    source: "Chunk 1:71"

agent_ontology_integration:
  - mechanism: "Vector Database Querying"
    description: "Agents query vector databases for semantic retrieval"
    source: "Chunk 1:161-163"
  - mechanism: "Knowledge Graph Integration"
    description: "Agent-G integrates graph knowledge bases with document retrieval"
    source: "Chunk 2:449-478"
  - mechanism: "Graph Expansion"
    description: "GeAR expands retrieval to include graph-structured entity relationships"
    source: "Chunk 2:595-597"
  - mechanism: "Ontology-Guided Retrieval"
    description: "Graph hierarchies structure multi-hop reasoning"
    source: "Chunk 2:466-467"
  - mechanism: "Hybrid Structured-Unstructured"
    description: "Combining graph data with document retrieval for comprehensive answers"
    source: "Chunk 2:450-451"

entity_count: null

methodology: "top-down"

empirical_evidence:
  - type: "Industry Case Studies"
    description: "Twitch ad sales enhancement using agentic RAG on Amazon Bedrock"
    source: "Chunk 3:5-8"
  - type: "Healthcare Application"
    description: "Patient case summaries integrating EHR with medical literature"
    source: "Chunk 3:31-34"
  - type: "Benchmark Datasets"
    description: "HotpotQA, MuSiQue, 2WikiMultihopQA for multi-hop evaluation"
    source: "Chunk 3:247-262"

limitations:
  - "Coordination Complexity: Managing inter-agent communication requires sophisticated orchestration (Chunk 1:370-371)"
  - "Computational Overhead: Multiple agents increase resource requirements (Chunk 1:374)"
  - "Scalability Limitations: Dynamic nature can strain resources for high query volumes (Chunk 1:377-378)"
  - "Lack of specialized benchmarks for evaluating agentic capabilities (Chunk 3:354-356)"

tools_standards:
  - "LangChain"
  - "LangGraph"
  - "LlamaIndex"
  - "Hugging Face Transformers"
  - "Qdrant"
  - "CrewAI"
  - "AutoGen/AG2"
  - "OpenAI Swarm"
  - "Vertex AI"
  - "Semantic Kernel"
  - "Amazon Bedrock"
  - "IBM Watson"
  - "Neo4j"
  - "Weaviate"
  - "Pinecone"
  - "Milvus"
---

# Agentic Retrieval-Augmented Generation: A Survey on Agentic RAG - Analysis Index

## Paper Overview

- **Source**: 20-Agentic_RAG_Survey.pdf
- **Chunks**: 3 chunks, ~31,253 estimated tokens
- **Analyzed**: 2025-12-28

## Key Extractions

This comprehensive survey explores Agentic RAG, a paradigm that integrates autonomous AI agents into Retrieval-Augmented Generation pipelines. The paper provides a taxonomy of RAG evolution, core agentic patterns, workflow architectures, and practical frameworks for implementation.

### Entity Types and Definitions

The paper defines key entity types in the agentic RAG context:

| Entity | Definition | Source |
|--------|------------|--------|
| Agent | Intelligent entity with LLM, Memory, Planning, Tools | Chunk 1:484-502 |
| Memory | Short-term (state) + Long-term (knowledge) | Chunk 1:491-493 |
| Tool | Vector Search, Web Search, APIs for extended capabilities | Chunk 1:500-501 |
| Activity | Retrieval, Augmentation, Generation processes | Chunk 1:161-169 |

### Agentic Patterns (Four Core Patterns)

| Pattern | Description | Source |
|---------|-------------|--------|
| Reflection | Self-evaluation and iterative output refinement | Chunk 1:512-531 |
| Planning | Autonomous task decomposition | Chunk 1:540-549 |
| Tool Use | External tool/API interaction | Chunk 1:555-569 |
| Multi-Agent | Task specialization and parallel processing | Chunk 1:575-592 |

### Agentic Workflow Patterns (Five Workflow Types)

| Pattern | Description | Source |
|---------|-------------|--------|
| Prompt Chaining | Sequential step-by-step processing | Chunk 1:620-632 |
| Routing | Classification-based process direction | Chunk 1:644-655 |
| Parallelization | Concurrent independent task execution | Chunk 1:671-676 |
| Orchestrator-Workers | Central delegation to specialized workers | Chunk 1:696-707 |
| Evaluator-Optimizer | Iterative refinement via evaluation | Chunk 1:721-731 |

### RAG System Architectures

| Architecture | Key Feature | Source |
|--------------|-------------|--------|
| Single-Agent RAG | Centralized router for retrieval decisions | Chunk 1:752-798 |
| Multi-Agent RAG | Specialized agents for different data sources | Chunk 1:874-968 |
| Hierarchical RAG | Multi-tiered agent organization | Chunk 2:100-160 |
| Corrective RAG | Self-correction of retrieval results | Chunk 2:190-262 |
| Adaptive RAG | Query complexity-based strategy selection | Chunk 2:314-400 |
| Graph-Based RAG | Knowledge graph integration (Agent-G, GeAR) | Chunk 2:443-698 |

### Agent-Ontology Integration Mechanisms

| Mechanism | Description | Source |
|-----------|-------------|--------|
| Knowledge Graph Querying | Agent-G integrates graph knowledge bases | Chunk 2:449-478 |
| Graph Expansion | GeAR expands to graph-structured relationships | Chunk 2:595-597 |
| Hybrid Retrieval | Combining structured (graph) and unstructured (docs) | Chunk 2:450-451 |
| Critic Module | Validates relevance of retrieved information | Chunk 2:474-475 |

### Key Findings

- **Agent Architecture** (Chunk 1:484-502): "An AI agent comprises: LLM (with defined Role and Task), Memory (Short-Term and Long-Term), Planning (Reflection & Self-Critique), Tools (Vector Search, Web Search, APIs)"

- **Agentic RAG Definition** (Chunk 1:55-60): "Agentic RAG transcends these limitations by embedding autonomous AI agents into the RAG pipeline. These agents leverage agentic design patterns - reflection, planning, tool use, and multi-agent collaboration"

- **Multi-Agent Collaboration** (Chunk 1:575-577): "Multi-agent collaboration is a key design pattern that enables task specialization and parallel processing. Agents communicate and share intermediate results, ensuring the overall workflow remains efficient"

- **Graph Integration** (Chunk 2:449-452): "Agent-G introduces a novel agentic architecture that integrates graph knowledge bases with unstructured document retrieval. By combining structured and unstructured data sources, this framework enhances RAG systems"

## Chunk Navigation

### Chunk 1: Introduction, Foundations, and Core Patterns

- **Summary**: Covers the abstract, introduction to RAG evolution (Naive, Advanced, Modular, Graph RAG), core AI agent components, four agentic patterns (Reflection, Planning, Tool Use, Multi-Agent), five workflow patterns, and single-agent/multi-agent architectures.
- **Key concepts**: [Agentic RAG, RAG paradigms, Agent components, Reflection, Planning, Tool Use, Multi-Agent, Prompt Chaining, Routing, Parallelization, Orchestrator-Workers]
- **Key quotes**:
  - Line 55-60: "Agentic RAG transcends these limitations by embedding autonomous AI agents into the RAG pipeline"
  - Line 484-502: Agent architecture definition
  - Line 512-531: Reflection pattern explanation
- **Load when**: "User asks about agentic patterns", "Query about RAG evolution", "Multi-agent system architectures"

### Chunk 2: Advanced Architectures and Graph-Based RAG

- **Summary**: Covers Multi-Agent RAG details, Hierarchical RAG, Corrective RAG, Adaptive RAG, Agent-G (graph knowledge integration), GeAR (graph expansion), Agentic Document Workflows, comparative analysis, and applications overview.
- **Key concepts**: [Hierarchical agents, Corrective RAG, Adaptive RAG, Agent-G, GeAR, Graph expansion, Knowledge graph integration, Document workflows]
- **Key quotes**:
  - Line 103-106: "Hierarchical Agentic RAG systems employ a structured, multi-tiered approach"
  - Line 449-452: "Agent-G introduces a novel agentic architecture that integrates graph knowledge bases"
  - Line 586-600: GeAR graph expansion mechanism
- **Load when**: "User asks about knowledge graph integration with agents", "Query about corrective or adaptive RAG", "Graph-based retrieval mechanisms"

### Chunk 3: Applications, Tools, Benchmarks, and Conclusion

- **Summary**: Covers industry applications (Healthcare, Finance, Legal, Education), tools and frameworks (LangChain, LlamaIndex, CrewAI, AutoGen, Semantic Kernel, Neo4j, vector databases), benchmarks and datasets (BEIR, MS MARCO, HotpotQA, RAGBench), and conclusion with future directions.
- **Key concepts**: [LangChain, LangGraph, LlamaIndex, CrewAI, AutoGen, Semantic Kernel, Neo4j, Vector databases, BEIR, HotpotQA, RAGBench]
- **Key quotes**:
  - Line 164-167: "LangChain provides modular components for building RAG pipelines"
  - Line 182-185: "CrewAI supports hierarchical and sequential processes"
  - Line 214-217: "Neo4j excels in handling complex relationships"
- **Load when**: "User asks about RAG implementation tools", "Query about agent frameworks", "Benchmarks for RAG evaluation"
