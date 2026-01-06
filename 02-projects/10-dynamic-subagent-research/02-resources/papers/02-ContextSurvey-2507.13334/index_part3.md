---
# PARTIAL INDEX HEADER
paper_id: "02-ContextSurvey-2507.13334"
title: "Context Engineering for LLMs - Survey (References Section)"
chunks_analyzed: [15, 16, 17, 18, 19, 20]
part: 3
total_parts: 4
partial: true
schema_version: "2.3"
analysis_complete: true

# CHUNK-LEVEL FIELD ASSESSMENT
chunk_index:
  15:
    token_count: 6242
    fields_found:
      pattern_definition: false
      mechanism_type: false
      failure_mode: false
      implementation_detail: false
      integration_point: false
      quality_metric: false
      limitation: false
      related_pattern: partial
  16:
    token_count: 6409
    fields_found:
      pattern_definition: false
      mechanism_type: false
      failure_mode: false
      implementation_detail: false
      integration_point: false
      quality_metric: false
      limitation: false
      related_pattern: partial
  17:
    token_count: 6514
    fields_found:
      pattern_definition: false
      mechanism_type: false
      failure_mode: false
      implementation_detail: false
      integration_point: false
      quality_metric: false
      limitation: false
      related_pattern: partial
  18:
    token_count: 6353
    fields_found:
      pattern_definition: false
      mechanism_type: false
      failure_mode: false
      implementation_detail: false
      integration_point: false
      quality_metric: false
      limitation: false
      related_pattern: partial
  19:
    token_count: 6306
    fields_found:
      pattern_definition: false
      mechanism_type: false
      failure_mode: false
      implementation_detail: false
      integration_point: false
      quality_metric: false
      limitation: false
      related_pattern: partial
  20:
    token_count: 6644
    fields_found:
      pattern_definition: false
      mechanism_type: false
      failure_mode: false
      implementation_detail: false
      integration_point: false
      quality_metric: false
      limitation: false
      related_pattern: partial

# DYNAMIC EXTRACTION FIELDS
pattern_definition:
  - item: "NOT_FOUND"
    chunk: null
    lines: null
    quote: null
    reason: "Chunks 15-20 are reference/bibliography sections containing citations only"

mechanism_type:
  - item: "NOT_FOUND"
    chunk: null
    lines: null
    quote: null
    reason: "Reference section - no mechanism definitions"

failure_mode:
  - item: "NOT_FOUND"
    chunk: null
    lines: null
    quote: null
    reason: "Reference section - no failure mode definitions"

implementation_detail:
  - item: "NOT_FOUND"
    chunk: null
    lines: null
    quote: null
    reason: "Reference section - no implementation details"

integration_point:
  - item: "NOT_FOUND"
    chunk: null
    lines: null
    quote: null
    reason: "Reference section - no integration point definitions"

quality_metric:
  - item: "NOT_FOUND"
    chunk: null
    lines: null
    quote: null
    reason: "Reference section - no quality metrics"

limitation:
  - item: "NOT_FOUND"
    chunk: null
    lines: null
    quote: null
    reason: "Reference section - no limitation discussions"

# Related patterns identified via reference titles
related_pattern:
  - name: "Agent Communication Protocol (ACP)"
    relationship: "reference"
    note: "IBM reference on ACP (Chunk 15:71-72)"
    source: "Chunk 15:71-72"
  - name: "MCP x A2A Framework"
    relationship: "reference"
    note: "Study on MCP x A2A framework for LLM agent interoperability (Chunk 15:150-152)"
    source: "Chunk 15:150-152"
  - name: "Model Context Protocol (MCP)"
    relationship: "reference"
    note: "MCP for telemetry-aware AI development patterns (Chunk 15:488-490)"
    source: "Chunk 15:488-490"
  - name: "Memory Sandbox"
    relationship: "reference"
    note: "Transparent and interactive memory management for conversational agents (Chunk 15:41-47)"
    source: "Chunk 15:41-47"
  - name: "LM2: Large Memory Models"
    relationship: "reference"
    note: "Large memory model architecture (Chunk 15:328-330)"
    source: "Chunk 15:328-330"
  - name: "A2A and MCP Integration"
    relationship: "reference"
    note: "Critical analysis of A2A and MCP integration for scalable agent systems (Chunk 17:25-27)"
    source: "Chunk 17:25-27"
  - name: "ScaleMCP"
    relationship: "reference"
    note: "Dynamic and auto-synchronizing MCP tools for LLM agents (Chunk 18:124-126)"
    source: "Chunk 18:124-126"
  - name: "MemGPT"
    relationship: "reference"
    note: "LLMs as operating systems with memory management (Chunk 19:221-228)"
    source: "Chunk 19:221-228"
  - name: "MemoRAG"
    relationship: "reference"
    note: "Global memory-enhanced retrieval augmentation for long context (Chunk 20:59-61)"
    source: "Chunk 20:59-61"
  - name: "Hierarchical-Categorical Memory"
    relationship: "reference"
    note: "Efficiently enhancing agents with hierarchical-categorical memory (Chunk 20:72-74)"
    source: "Chunk 20:72-74"
  - name: "MCP Software Design Patterns"
    relationship: "reference"
    note: "Survey of LLM agent communication with MCP - software design pattern review (Chunk 20:415-417)"
    source: "Chunk 20:415-417"
  - name: "ToolLLM"
    relationship: "reference"
    note: "Facilitating LLMs to master 16000+ real-world APIs (Chunk 20:111-114)"
    source: "Chunk 20:111-114"

# Chunk Evidence (3-point verification)
chunk_evidence:
  15:
    start: "[454] Sirui Huang, Hanqian Li, Yanggan Gu, Xuming Hu, Qing Li, and Guandong Xu. Hyperg"
    mid: "[486] Cheonsu Jeong. A study on the mcp x a2a framework for enhancing interoperability"
    end: "[556] Tomás Kociský, Jonathan Schwarz, Phil Blunsom, Chris Dyer, Karl Moritz Hermann"
  16:
    start: "retrieval-augmented generation. arXiv preprint, 2025."
    mid: "[591] Younghun Lee, Sungchul Kim, Ryan A. Rossi, Tong Yu, and Xiang Chen. Learning to"
    end: "[636] Yucheng Li. Unlocking context constraints of llms: Enhancing context efficiency"
  17:
    start: "[618] M Li, Y Zhao, B Yu, F Song, H Li, H Yu, and Z Li.... Api-bank: A comprehensive"
    mid: "[663] David Lillis. Internalising interaction protocols as first-class programming elements"
    end: "[714] Liqiang Lu, Yicheng Jin, Hangrui Bi, Zizhang Luo, Peng Li, Tao Wang, and Yun Liang"
  18:
    start: "Enabling language representation with knowledge graph. AAAI Conference on Artificial"
    mid: "[745] Zhao Mandi, Shreeya Jain, and Shuran Song. Roco: Dialectic multi-robot collaboration"
    end: "[794] Marius Mosbach, Tiago Pimentel, Shauli Ravfogel, D. Klakow, and Yanai Elazar"
  19:
    start: "[774] Thomas Merth, Qichen Fu, Mohammad Rastegari, and Mahyar Najibi. Superposition"
    mid: "[831] J. Park, Joseph C. O'Brien, Carrie J. Cai, M. Morris, Percy Liang, and Michael S."
    end: "[873] Libo Qin, Fuxuan Wei, Qiguang Chen, Jingxuan Zhou, Shijue Huang, Jiasheng Si"
  20:
    start: "[856] Pranav Putta, Edmund Mills, Naman Garg, S. Motwani, Chelsea Finn, Divyansh Garg"
    mid: "[903] S. Rizvi, Nazreen Pallikkavaliyaveetil, David Zhang, Zhuoyang Lyu, Nhi Nguyen"
    end: "[950] Junhong Shen, Atishay Jain, Zedian Xiao, Ishan Amlekar, Mouad Hadji, Aaron Podolny"
---

# Context Engineering for LLMs Survey - Partial Index (Part 3 of 4)

## Paper Overview

- **Source**: 02-ContextSurvey-2507.13334.pdf
- **Chunks Covered**: 15-20 of 26
- **Analyzed**: 2025-12-28
- **Content Type**: References/Bibliography Section

## Key Observations

Chunks 15-20 contain the **References section** of this survey paper. These chunks consist entirely of numbered bibliographic citations (approximately refs [454] through [950]).

While no primary pattern definitions, mechanisms, or implementations are present in these reference-only sections, they do provide valuable pointers to related work in multi-agent communication protocols and memory systems.

### Relevant Reference Categories Identified

| Category | Representative References | Source Chunks |
|----------|--------------------------|---------------|
| Agent Communication Protocols | A2A, MCP, ACP, LACP | 15, 17, 18, 20 |
| Memory Systems for LLMs | MemGPT, MemoRAG, Memory Sandbox | 15, 19, 20 |
| Multi-Agent Systems | CAMEL, ChatDev, MetaAgents | 16, 20 |
| Tool Learning | ToolLLM, API-Bank, ToolFormer | 17, 20 |
| Context Engineering | Context compression, RAG | 15, 16, 19 |

## Chunk Navigation

### Chunk 15: References [454]-[556]
- **Summary**: Bibliography entries covering hypergraph LLMs, language models as planners, memory sandbox systems, MCP x A2A framework studies, multi-agent reinforcement learning, and early knowledge graph approaches.
- **Key references**:
  - [468] IBM ACP definition
  - [486] MCP x A2A framework interoperability study
  - [461-462] Memory Sandbox for conversational agents
  - [522] LM2: Large Memory Models
- **Load when**: "Query references agent communication protocols" / "User asks about memory management in agents"

### Chunk 16: References [537]-[636]
- **Summary**: Bibliography entries covering RAG systems, context compression, multi-agent workflows, LLM-based collaborative agents, and context efficiency methods.
- **Key references**:
  - [577] LangChain memory in LangGraph
  - [606] CAMEL: Communicative agents for mind exploration
  - [622] A2A and MCP integration analysis
  - [631] Survey on LLM-based multi-agent systems
- **Load when**: "Query references multi-agent collaboration" / "User asks about context compression"

### Chunk 17: References [618]-[714]
- **Summary**: Bibliography entries covering API benchmarks, knowledge editing, multi-agent collaboration, interaction protocols, and dynamic agent networks.
- **Key references**:
  - [618, 621] API-Bank benchmark for tool-augmented LLMs
  - [622] A2A and MCP integration for scalable agents
  - [663] Internalizing interaction protocols in MAS
  - [704] Dynamic LLM-powered agent network
- **Load when**: "Query references tool learning" / "User asks about interaction protocols"

### Chunk 18: References [696]-[794]
- **Summary**: Bibliography entries covering knowledge graphs, agent collaboration protocols, MCP tools, multi-agent reasoning, and prompt engineering.
- **Key references**:
  - [685] ACPS: Agent collaboration protocols for Internet of Agents
  - [719] ScaleMCP: Dynamic MCP tools for LLM agents
  - [725] Large Language Model Agent survey
  - [732] Role of LLM in multi-agent systems
- **Load when**: "Query references agent collaboration protocols" / "User asks about ScaleMCP"

### Chunk 19: References [774]-[873]
- **Summary**: Bibliography entries covering RAG improvements, LLM agents with computer systems insights, memory systems, generative agents, and tool use.
- **Key references**:
  - [776] Building LLM agents with computer systems insights
  - [819-820] MemGPT: LLMs as operating systems
  - [831] Generative agents - interactive simulacra
  - [856] Agent Q: Advanced reasoning for autonomous agents
- **Load when**: "Query references MemGPT" / "User asks about generative agents"

### Chunk 20: References [856]-[950]
- **Summary**: Bibliography entries covering agent reasoning, MemoRAG, hierarchical memory, MCP design patterns, tool learning, and prompt engineering surveys.
- **Key references**:
  - [866] MemoRAG: Memory-enhanced retrieval augmentation
  - [868] Hierarchical-categorical memory for agents
  - [874-875] Tool learning with foundation models, ToolLLM
  - [934] Survey of LLM agent communication with MCP
- **Load when**: "Query references MemoRAG" / "User asks about MCP design patterns"

## Extraction Summary

| Field | Count | Notes |
|-------|-------|-------|
| pattern_definition | 0 | N/A - Reference section only |
| mechanism_type | 0 | N/A - Reference section only |
| failure_mode | 0 | N/A - Reference section only |
| implementation_detail | 0 | N/A - Reference section only |
| integration_point | 0 | N/A - Reference section only |
| quality_metric | 0 | N/A - Reference section only |
| limitation | 0 | N/A - Reference section only |
| related_pattern | 12 | References to relevant protocols/systems |

**Note**: Primary pattern definitions and mechanisms should be extracted from earlier chunks (1-14) containing the main body of the survey.
