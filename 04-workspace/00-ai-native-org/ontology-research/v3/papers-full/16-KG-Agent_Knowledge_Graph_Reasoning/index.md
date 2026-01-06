---
paper_id: "16-KG-Agent_Knowledge_Graph_Reasoning"
title: "KG-Agent: An Efficient Autonomous Agent Framework for Complex Reasoning over Knowledge Graph"
authors:
  - "Jinhao Jiang"
  - "Kun Zhou"
  - "Wayne Xin Zhao"
  - "Yang Song"
  - "Chen Zhu"
  - "Hengshu Zhu"
  - "Ji-Rong Wen"
year: 2024
chunks_expected: 2
chunks_read: 2
analysis_complete: true
schema_version: "2.3"

chunk_index:
  1:
    token_count: 11122
    fields_found:
      entity_types: true
      entity_definitions: true
      entity_relationships: true
      entity_count: partial
      abstraction_level: true
      framework_comparison: true
      methodology: true
      ai_integration: true
      agent_modeling: true
      agentic_workflows: true
      generative_ai_patterns: true
      agent_ontology_integration: true
      empirical_evidence: true
      limitations: true
      tools_standards: true
  2:
    token_count: 8301
    fields_found:
      entity_types: true
      entity_definitions: true
      entity_relationships: partial
      entity_count: false
      abstraction_level: false
      framework_comparison: partial
      methodology: true
      ai_integration: partial
      agent_modeling: false
      agentic_workflows: false
      generative_ai_patterns: false
      agent_ontology_integration: true
      empirical_evidence: true
      limitations: true
      tools_standards: true

entity_types:
  - item: "Entity (KG)"
    chunk: 1
    lines: "176-182"
    quote: "A knowledge graph typically consists of a large number of fact triples, expressed as G = {<e, r, e'>|e, e' in E, r in R}, where E and R denote the entity set and relation set, respectively."
  - item: "Relation"
    chunk: 1
    lines: "177-180"
    quote: "A triple <e, r, e'> describes a factual knowledge that a relation r exists between the head entity e and tail entity e'."
  - item: "Entity Type"
    chunk: 1
    lines: "180-183"
    quote: "Each entity e is assigned a unique entity ID (or string value), and belongs to one entity type t such as Country and Person."
  - item: "Neighboring Relations"
    chunk: 1
    lines: "183-190"
    quote: "we introduce neighboring relations to denote both the incoming and outgoing relations for a set of entities {e}, denoted as R{e} = {r|<e, r, e'> in G} union {r|<e', r, e> in G}."
  - item: "LLM-based Planner"
    chunk: 1
    lines: "537-539"
    quote: "the core instruction-tuned LLM (Section 4.2), referred to as the LLM-based planner"
  - item: "Toolbox"
    chunk: 1
    lines: "539-540"
    quote: "the multifunctional toolbox (Section 4.1)"
  - item: "KG-based Executor"
    chunk: 1
    lines: "540-541"
    quote: "the KG-based executor for executing the tool invocation"
  - item: "Knowledge Memory"
    chunk: 1
    lines: "540-542"
    quote: "the knowledge memory to record the context and currently useful information in the whole process"
  - item: "Extraction Tools"
    chunk: 1
    lines: "241-249"
    quote: "Extraction tools aim to facilitate the access to information from KG. Considering the basic data types in KG, we design five tools to support the access to the relations (get_relation), the head/tail entities (get_head_entity/get_tail_entity), and entities with specific type or constraint (get_entity_by_type/get_entity_by_constraint)"
  - item: "Logic Tools"
    chunk: 1
    lines: "250-255"
    quote: "Logic tools aim to support basic manipulation operations on the extracted KG information, including entity counting (count), entity set intersection (intersect) and union (union), condition verification (judge), and ending the reasoning process with the current entity set as the final answer(s) (end)."
  - item: "Semantic Tools"
    chunk: 1
    lines: "256-259"
    quote: "Semantic tools are developed by utilizing pre-trained models to implement specific functions, including relation retrieval (retrieve_relation) and entity disambiguation (disambiguate_entity)."

entity_definitions:
  knowledge_graph:
    chunk: 1
    lines: "176-180"
    definition: "A knowledge graph typically consists of a large number of fact triples, expressed as G = {<e, r, e'>|e, e' in E, r in R}, where E and R denote the entity set and relation set, respectively. A triple <e, r, e'> describes a factual knowledge that a relation r exists between the head entity e and tail entity e'."
  entity:
    chunk: 1
    lines: "180-182"
    definition: "Each entity e is assigned a unique entity ID (or string value), and belongs to one entity type t such as Country and Person."
  query_graph:
    chunk: 1
    lines: "420-425"
    definition: "A small KG subgraph related to the question. The query graph has a tree-like structure that can be directly mapped to a logical form, and it can clearly depict the execution flow of the SQL query to obtain the answer."
  knowledge_memory:
    chunk: 1
    lines: "545-551"
    definition: "The knowledge memory preserves the currently useful information to support the LLM-based planner for making decisions. It mainly contains four parts of information: natural language question, toolbox definition, current KG information, and history reasoning program."
  llm_based_planner:
    chunk: 1
    lines: "554-565"
    definition: "Based on the current knowledge memory, the LLM-based planner selects a tool to interact with KG at each step. The planner needs to invoke tools from the pre-defined toolbox to address four types of task requirements: linking the mentioned entity to KG, accessing the KG information, processing the intermediate results, or returning the final answer."
  kg_based_executor:
    chunk: 1
    lines: "568-626"
    definition: "After the planner generates the function call, the KG-based executor will execute it using a program compiler. It can cache or operate the intermediate variables, and extract new entities or relations from the KG. After execution, the knowledge memory will be accordingly updated."

entity_relationships:
  - relationship: "Agent uses Toolbox"
    chunk: 1
    lines: "537-542"
    quote: "It mainly contains four components, i.e., the core instruction-tuned LLM (Section 4.2), referred to as the LLM-based planner, the multifunctional toolbox (Section 4.1), the KG-based executor for executing the tool invocation, and the knowledge memory"
  - relationship: "Planner selects Tool"
    chunk: 1
    lines: "554-558"
    quote: "Based on the current knowledge memory, the LLM-based planner selects a tool to interact with KG at each step. Specifically, all the parts in the current knowledge memory will be formatted with corresponding prompt template to compose the input, and then the LLM will generate one function call by selecting a tool and its arguments from the input."
  - relationship: "Executor updates Memory"
    chunk: 1
    lines: "620-626"
    quote: "After execution, the knowledge memory will be accordingly updated. First, the current function call will be added to the history reasoning program. Second, if the invoked tool is to obtain the new information from the KG (e.g., 'get_relation'), the executor will add it to the KG information for updating the knowledge memory."
  - relationship: "Entity connected-by Relation"
    chunk: 1
    lines: "177-180"
    quote: "A triple <e, r, e'> describes a factual knowledge that a relation r exists between the head entity e and tail entity e'."
  - relationship: "Entity belongs-to EntityType"
    chunk: 1
    lines: "180-182"
    quote: "Each entity e is assigned a unique entity ID (or string value), and belongs to one entity type t such as Country and Person."

abstraction_level: "Application-level framework for LLM-based autonomous agents reasoning over knowledge graphs. Focuses on practical implementation of agent-KG interaction rather than foundational ontology theory."

framework_comparison:
  - comparison: "vs ReAct"
    chunk: 1
    lines: "154-158"
    quote: "ReAct proposes a prompting method to convert LLMs (e.g., ChatGPT) as language agents, to interact with the external environment, receive the feedback, and then generate the action for next step reasoning."
  - comparison: "vs AutoGPT"
    chunk: 1
    lines: "158-159"
    quote: "AutoGPT further empowers LLMs (i.e., GPT4) with long/short-term memory management and external tools like search engines to autonomously address a user request."
  - comparison: "vs StructGPT"
    chunk: 1
    lines: "646-651"
    quote: "StructGPT (Jiang et al., 2023b)... crafted a pre-defined interaction way between LLM and KG, which cannot flexibly adapt to various complex tasks."
  - comparison: "vs ChatDB"
    chunk: 1
    lines: "652-656"
    quote: "ChatBD (Hu et al., 2023a), conducted autonomous reasoning with chain-of-thought and memory augmented. However, it relies on the strong closed-source LLM APIs (e.g., ChatGPT) and cannot use tools to implement some specialized operations."
  - comparison: "vs KB-BINDER, Pangu, RoG"
    chunk: 1
    lines: "645-650"
    quote: "KB-BINDER (Li et al., 2023), Pangu (Gu et al., 2023), StructGPT (Jiang et al., 2023b), and RoG (Luo et al., 2023), crafted a pre-defined interaction way between LLM and KG, which cannot flexibly adapt to various complex tasks."

ai_integration:
  - pattern: "Autonomous LLM-based agent framework"
    chunk: 1
    lines: "23-30"
    quote: "we propose an autonomous LLM-based agent framework, called KG-Agent, which enables a small LLM to actively make decisions until finishing the reasoning process over KGs. In KG-Agent, we integrate the LLM, multifunctional toolbox, KG-based executor, and knowledge memory"
  - pattern: "Instruction tuning for KG reasoning"
    chunk: 1
    lines: "267-276"
    quote: "To enable the autonomous reasoning process, we construct a high-quality instruction dataset for fine-tuning a small LLM (i.e., LLaMA2-7B). For this purpose, we first leverage existing KG based question answering (KGQA) datasets to generate the KG reasoning program, and then decompose it into multiple steps."
  - pattern: "Code-based instruction synthesis"
    chunk: 1
    lines: "31-38"
    quote: "we leverage program language to formulate the multi-hop reasoning process over the KG, and synthesize a code-based instruction dataset to fine-tune the base LLM. Extensive experiments demonstrate that only using 10K samples for tuning LLaMA-7B can outperform state-of-the-art methods"
  - pattern: "Tool-augmented reasoning"
    chunk: 1
    lines: "91-95"
    quote: "we extend the LLM's capacity to manipulate structured data by curating a multifunctional toolbox, enabling LLM to perform discrete or advanced operations (e.g., filtering, counting, and retrieval) on KG data and intermediate results."

agent_modeling:
  - aspect: "Autonomous decision-making"
    chunk: 1
    lines: "85-89"
    quote: "designing autonomous reasoning approaches that can actively make decisions during reasoning, without human assistance; (2) enabling relatively small models (e.g., 7B LLM) to effectively perform complex reasoning, without reliance on close-sourced LLM APIs"
  - aspect: "Four component architecture"
    chunk: 1
    lines: "537-542"
    quote: "It mainly contains four components, i.e., the core instruction-tuned LLM (Section 4.2), referred to as the LLM-based planner, the multifunctional toolbox (Section 4.1), the KG-based executor for executing the tool invocation, and the knowledge memory"
  - aspect: "Iterative reasoning mechanism"
    chunk: 1
    lines: "629-638"
    quote: "The KG-Agent framework autonomously iterates the above tool selection and memory updation process to perform step-by-step reasoning, where the knowledge memory is used to maintain the accessed information from KG. In this way, the multi-turn decision-making process of the agent is like walking on the KG along relations."

agentic_workflows:
  - workflow: "Tool selection and memory update iteration"
    chunk: 1
    lines: "629-639"
    quote: "The KG-Agent framework autonomously iterates the above tool selection and memory updation process to perform step-by-step reasoning, where the knowledge memory is used to maintain the accessed information from KG... Once reaching the answer entities, the agent will automatically stop the iterative process."
  - workflow: "Knowledge memory initialization and update"
    chunk: 1
    lines: "545-551"
    quote: "The knowledge memory preserves the currently useful information to support the LLM-based planner for making decisions. It mainly contains four parts of information, i.e., natural language question, toolbox definition, current KG information, and history reasoning program."
  - workflow: "Reasoning chain extraction via BFS"
    chunk: 1
    lines: "426-434"
    quote: "starting from the mentioned entity in the question (i.e., Cristiano Ronaldo), we adopt breadth-first search (BFS) to visit all the nodes on the query graph. This strategy would finally produce a reasoning chain (e.g., teams->roster_team) linking the start entity to the answer entity"

generative_ai_patterns:
  - pattern: "Instruction fine-tuning"
    chunk: 1
    lines: "518-528"
    quote: "Based on the above formatted instruction tuning data, we perform supervised fine-tuning on a small LLM (i.e., LLaMA-7B)... During the instruction tuning process, we feed the input x and output y into the decoder-only LLM and minimize the cross-entropy loss on the ground-truth response y"
  - pattern: "Code-based reasoning programs"
    chunk: 1
    lines: "436-456"
    quote: "After extracting the reasoning chain, we next convert it into multiple interrelated triples, where each triple generally corresponds to an intermediate reasoning step. Finally, we reformulate the triples into several function calls with the code format, which represents the tool invocation and can be executed"
  - pattern: "Function call generation"
    chunk: 1
    lines: "554-558"
    quote: "all the parts in the current knowledge memory will be formatted with corresponding prompt template to compose the input, and then the LLM will generate one function call by selecting a tool and its arguments from the input"

agent_ontology_integration:
  - integration: "Knowledge graph as reasoning substrate"
    chunk: 1
    lines: "49-51"
    quote: "Knowledge graph (KG), which stores massive knowledge triples in a graph-structured format, has been broadly used to complement LLMs with external knowledge"
  - integration: "Structured KG access via tools"
    chunk: 1
    lines: "230-239"
    quote: "Since LLMs struggle to accurately manipulate the structured data, we construct a supporting toolbox for easing the utilization of the KG information. According to existing work, reasoning over KG (e.g., Freebase or Wikidata) typically requires three fundamental operations, namely extracting information from KG, filtering irrelevant information based on the semantics of the question, and operating on the extracted information."
  - integration: "Synergy-augmented LLM-KG interaction"
    chunk: 1
    lines: "62-68"
    quote: "synergy-augmented methods can benefit from the structured search on KG (e.g., SPARQL) and the language understanding capacity of LLMs, achieving comparable or even better performance compared with previous state-of-the-art methods"
  - integration: "Tool definitions for KG operations"
    chunk: 2
    lines: "752-844"
    quote: "Table 8: The detailed definition and usage of all the tools (includes get_relation, get_head_entity, get_tail_entity, get_entity_by_type, get_candidate_entity, count, intersect, union, judge, end, retrieve_relation, disambiguate_entity, get_entity_by_constraint)"

entity_count: null

methodology: "Code-based instruction synthesis from existing KGQA datasets. Supervised fine-tuning (SFT) of LLaMA2-7B using 10K samples. Autonomous iteration mechanism combining tool selection and memory update. Evaluation on both in-domain (WebQSP, CWQ, GrailQA, KQA Pro) and out-of-domain (ODQA) datasets."

empirical_evidence:
  - evidence: "Performance on WebQSP, CWQ, GrailQA"
    chunk: 1
    lines: "590-616"
    quote: "Ours 83.3 81.0 72.2 69.8 86.1 92.0 80.0 86.3 (Table 2 results showing KG-Agent outperforming baselines including ChatGPT, GPT-4, StructGPT)"
  - evidence: "Performance on KQA Pro"
    chunk: 1
    lines: "685-706"
    quote: "Ours 92.15 91.03 87.90 96.32 91.28 88.21 92.86 91.40 (Table 3 results on Wikidata-based dataset)"
  - evidence: "Zero-shot transfer performance"
    chunk: 1
    lines: "782-790"
    quote: "our KG-Agent only needs to learn how to interact with KG instead of memorizing the specific knowledge. Thus, it can utilize the external KG in zero-shot setting, and achieve consistent improvement compared to fine-tuned pre-trained language models."
  - evidence: "Data efficiency"
    chunk: 1
    lines: "34-37"
    quote: "only using 10K samples for tuning LLaMA-7B can outperform state-of-the-art methods using larger LLMs or more data, on both in-domain and out-domain datasets"
  - evidence: "MetaQA transfer results"
    chunk: 1
    lines: "770-774"
    quote: "Ours 97.1 98.0 92.1 (Table 5 showing transfer to domain-specific movie KG)"

limitations:
  - limitation: "Single backbone LLM tested"
    chunk: 1
    lines: "909-914"
    quote: "First, we only use the LLaMA2-7B as the backbone LLM, which has a strong capability after instruction tuning. Hence, more experiments are required to evaluate other LLMs with comparable parameter sizes, such as Mistral-7B or CodeLLaMA-7b."
  - limitation: "Limited to KG knowledge sources"
    chunk: 1
    lines: "915-918"
    quote: "Second, we focus on reasoning over the KG to answer the factual questions. We should consider extending our framework to deal with more types of knowledge sources, e.g., databases or tables."
  - limitation: "Limited evaluation scenarios"
    chunk: 1
    lines: "918-923"
    quote: "Third, we only evaluate factual question answering tasks based on KG. Future work should include wider evaluation scenarios to evaluate the universality of our method, e.g., data-to-text and formal-language-to-text."
  - limitation: "Safety and filtering concerns"
    chunk: 1
    lines: "923-927"
    quote: "we should add more rule-based methods to post-process the predictions and filter the illegal responses."

tools_standards:
  - tool: "Freebase KG"
    chunk: 1
    lines: "234-235"
    description: "Knowledge graph used for reasoning, containing fact triples"
  - tool: "Wikidata KG"
    chunk: 1
    lines: "677-678"
    description: "Alternative knowledge graph used for KQA Pro dataset"
  - tool: "SPARQL"
    chunk: 1
    lines: "66-67"
    description: "Structured query language for KG, mentioned as alternative to agent approach"
  - tool: "LLaMA2-7B"
    chunk: 1
    lines: "271"
    description: "Base LLM used for instruction tuning"
  - tool: "12 defined tools"
    chunk: 2
    lines: "752-844"
    description: "get_relation, get_head_entity, get_tail_entity, get_entity_by_type, get_candidate_entity, count, intersect, union, judge, end, retrieve_relation, disambiguate_entity, get_entity_by_constraint"
---

# KG-Agent: An Efficient Autonomous Agent Framework for Complex Reasoning over Knowledge Graph

## Summary

This paper presents KG-Agent, an autonomous LLM-based agent framework for complex reasoning over knowledge graphs. The key innovation is enabling a relatively small LLM (LLaMA2-7B) to autonomously make decisions during multi-hop reasoning over KGs, without relying on closed-source LLM APIs or pre-defined interaction patterns.

## Key Contributions

1. **Autonomous Agent Framework**: Four-component architecture integrating LLM-based planner, multifunctional toolbox, KG-based executor, and knowledge memory
2. **Code-Based Instruction Tuning**: Synthesizes reasoning programs from KGQA datasets as instruction data
3. **Tool-Augmented Reasoning**: Three tool categories (Extraction, Logic, Semantic) enable structured KG manipulation
4. **Data Efficiency**: Only 10K training samples needed to outperform methods using larger LLMs or more data

## Architecture Components

### Entity Types in KG-Agent

- **Knowledge Graph Entities**: Entity, Relation, Entity Type, Neighboring Relations
- **Agent Components**: LLM-based Planner, Toolbox, KG-based Executor, Knowledge Memory
- **Tool Categories**: Extraction Tools (5), Logic Tools (5), Semantic Tools (2)

### Tool Definitions

| Category | Tools |
|----------|-------|
| Extraction | get_relation, get_head_entity, get_tail_entity, get_entity_by_type, get_candidate_entity |
| Logic | count, intersect, union, judge, end |
| Semantic | retrieve_relation, disambiguate_entity |

## Relevance to Research Questions

### Agent-Ontology Integration Patterns
- Demonstrates structured access to KG via typed tool interfaces
- Knowledge memory maintains reasoning state across iterations
- Synergy-augmented approach combines LLM language understanding with structured KG search

### Agentic Workflow Patterns
- Iterative tool selection and memory update cycle
- Autonomous stopping condition when answer entities reached
- BFS-based reasoning chain extraction from query graphs

### AI Integration Patterns
- Instruction fine-tuning from code-based reasoning programs
- Function call generation for tool invocation
- Small model (7B) achieving competitive performance through specialized training

## Experimental Results

- Outperforms ChatGPT, GPT-4, and StructGPT on KGQA benchmarks
- Zero-shot transfer to out-of-domain datasets
- Successfully transfers to domain-specific KGs (MetaQA movie domain)
