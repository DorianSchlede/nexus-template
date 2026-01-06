---
paper_id: "03-PROV-AGENT_Unified_Provenance_for_AI_Agents"
title: "PROV-AGENT: Unified Provenance for Tracking AI Agent Interactions in Agentic Workflows"
authors:
  - "Renan Souza"
  - "Amal Gueroudji"
  - "Stephen DeWitt"
  - "Daniel Rosendo"
  - "Tirthankar Ghosal"
  - "Robert Ross"
  - "Prasanna Balaprakash"
  - "Rafael Ferreira da Silva"
year: 2025
chunks_expected: 1
chunks_read: 1
analysis_complete: true
schema_version: "2.3"

chunk_index:
  1:
    token_count: 8940
    fields_found:
      entity_types: true
      entity_definitions: true
      entity_relationships: true
      entity_count: false
      abstraction_level: true
      framework_comparison: true
      methodology: partial
      ai_integration: true
      agent_modeling: true
      agentic_workflows: true
      generative_ai_patterns: true
      agent_ontology_integration: true
      empirical_evidence: true
      limitations: partial
      tools_standards: true

entity_types:
  - item: "Agent (W3C PROV core class)"
    chunk: 1
    lines: "200-204"
    quote: "W3C PROV standard already defines Agent, the central abstraction in this work, as one of its three core classes, alongside Entity (data) and Activity (process), with agents representing either software or human actors responsible for activities."
  - item: "Entity (W3C PROV core class)"
    chunk: 1
    lines: "200-201"
    quote: "three core classes, alongside Entity (data) and Activity (process)"
  - item: "Activity (W3C PROV core class)"
    chunk: 1
    lines: "200-201"
    quote: "three core classes, alongside Entity (data) and Activity (process)"
  - item: "AIAgent"
    chunk: 1
    lines: "278-284"
    quote: "We extend the abstract W3C PROV Agent by modeling AIAgent as its subclass, enabling a natural integration of agent actions and interactions into the broader workflow provenance graph."
  - item: "AgentTool"
    chunk: 1
    lines: "285-286"
    quote: "Following the MCP terminology, an AI agent can be associated with one or many tool executions (AgentTool)"
  - item: "AIModelInvocation"
    chunk: 1
    lines: "287-288"
    quote: "each tool may be informed by (PROV wasInformedBy) one or many AIModelInvocations"
  - item: "AIModel"
    chunk: 1
    lines: "288-291"
    quote: "Each AIModelInvocation uses a Prompt and a specific AIModel, which holds model metadata, including its name, type, provider, temperature, and other parameters"
  - item: "Prompt"
    chunk: 1
    lines: "288"
    quote: "Each AIModelInvocation uses a Prompt and a specific AIModel"
  - item: "ResponseData"
    chunk: 1
    lines: "291-292"
    quote: "generates a ResponseData object, which is attributedTo the corresponding agent"
  - item: "DataObject"
    chunk: 1
    lines: "274-276"
    quote: "modeled as subclasses of DataObject, which is a subclass of PROV Entity"
  - item: "DomainData"
    chunk: 1
    lines: "265-266"
    quote: "Tasks consume (PROV used) and produce (PROV generated) domain-specific data objects (DomainData)"
  - item: "SchedulingData"
    chunk: 1
    lines: "267-272"
    quote: "Tasks also generate two additional types of metadata: SchedulingData and TelemetryData. SchedulingData contains where the task ran, including details such as compute node, CPU core, or GPU ID."
  - item: "TelemetryData"
    chunk: 1
    lines: "273-274"
    quote: "TelemetryData contains runtime metrics such as CPU and GPU usage, and disk usage."
  - item: "Campaign"
    chunk: 1
    lines: "263-264"
    quote: "the model includes standard workflow structures such as Campaign, Workflow, and Task, modeled as subclasses of PROV Activities"
  - item: "Workflow"
    chunk: 1
    lines: "263-264"
    quote: "the model includes standard workflow structures such as Campaign, Workflow, and Task, modeled as subclasses of PROV Activities"
  - item: "Task"
    chunk: 1
    lines: "263-265"
    quote: "the model includes standard workflow structures such as Campaign, Workflow, and Task, modeled as subclasses of PROV Activities"

entity_definitions:
  Agent: "W3C PROV core class representing software or human actors responsible for activities."
  Entity: "W3C PROV core class representing data artifacts in the provenance model."
  Activity: "W3C PROV core class representing processes that use or generate entities."
  AIAgent: "Subclass of W3C PROV Agent that enables integration of agent actions and interactions into workflow provenance graph. Supports multi-agent workflows with individual tools and reasoning paths."
  AgentTool: "Subclass of Activity representing an MCP tool execution, associated with the executing agent and linked to inputs/outputs using PROV relationships."
  AIModelInvocation: "Activity capturing a call to an AI model, linked to the model used, prompt sent, and response generated. Related to AgentTool via wasInformedBy."
  AIModel: "Entity holding model metadata including name, type, provider, temperature, and other parameters. Designed to be modality-agnostic."
  Prompt: "Entity representing the input prompt used by an AIModelInvocation."
  ResponseData: "Entity generated by AIModelInvocation and attributed to the corresponding AIAgent."
  DataObject: "Subclass of PROV Entity serving as base for domain data, prompts, responses, and system metadata."
  DomainData: "Subclass of DataObject containing domain-specific data such as parameters, arguments, KPIs, QoIs, and pointers to data files."
  SchedulingData: "Subclass of DataObject containing execution location metadata such as compute node, CPU core, or GPU ID."
  TelemetryData: "Subclass of DataObject containing runtime metrics such as CPU/GPU usage and disk usage."
  Campaign: "Subclass of PROV Activity representing a high-level experimental campaign, associated with Person or Organization agents."
  Workflow: "Subclass of PROV Activity representing a workflow within a campaign."
  Task: "Subclass of PROV Activity that consumes (used) and produces (generated) data objects."

entity_relationships:
  - item: "AIAgent wasAssociatedWith AgentTool"
    chunk: 1
    lines: "349-351"
    quote: "This activity is associated with the executing agent and linked to its inputs and outputs using the PROV relationships defined in the PROV-AGENT model."
  - item: "AgentTool wasInformedBy AIModelInvocation"
    chunk: 1
    lines: "365-367"
    quote: "When a tool depends on LLM results, Flowcept establishes a wasInformedBy relationship from the AgentTool to the relevant AIModelInvocation activities."
  - item: "AIModelInvocation used Prompt"
    chunk: 1
    lines: "288"
    quote: "Each AIModelInvocation uses a Prompt and a specific AIModel"
  - item: "AIModelInvocation used AIModel"
    chunk: 1
    lines: "288-290"
    quote: "Each AIModelInvocation uses a Prompt and a specific AIModel, which holds model metadata"
  - item: "AIModelInvocation wasGeneratedBy ResponseData"
    chunk: 1
    lines: "290-292"
    quote: "and generates a ResponseData object, which is attributedTo the corresponding agent"
  - item: "ResponseData wasAttributedTo AIAgent"
    chunk: 1
    lines: "291-292"
    quote: "generates a ResponseData object, which is attributedTo the corresponding agent"
  - item: "Task used DomainData"
    chunk: 1
    lines: "265"
    quote: "Tasks consume (PROV used) and produce (PROV generated) domain-specific data objects (DomainData)"
  - item: "Task wasGeneratedBy DomainData"
    chunk: 1
    lines: "265"
    quote: "Tasks consume (PROV used) and produce (PROV generated) domain-specific data objects (DomainData)"
  - item: "Task wasGeneratedBy SchedulingData"
    chunk: 1
    lines: "267-268"
    quote: "Tasks also generate two additional types of metadata: SchedulingData and TelemetryData"
  - item: "Task wasGeneratedBy TelemetryData"
    chunk: 1
    lines: "267-268"
    quote: "Tasks also generate two additional types of metadata: SchedulingData and TelemetryData"
  - item: "Campaign wasAssociatedWith Person/Organization"
    chunk: 1
    lines: "264"
    quote: "Campaigns are associated with Person or Organization agents via wasAssociatedWith"
  - item: "subClassOf hierarchy"
    chunk: 1
    lines: "260"
    quote: "Dashed arrows represent subClassOf"

entity_count: "NOT_FOUND"

abstraction_level: "Domain-level ontology extending W3C PROV foundational standard for agentic AI workflows. Bridges foundational provenance concepts (Entity, Activity, Agent) with AI-specific entities (AIAgent, AgentTool, AIModelInvocation, Prompt, ResponseData)."

framework_comparison:
  - item: "W3C PROV extension"
    chunk: 1
    lines: "118-121"
    quote: "PROV-AGENT, a provenance model that extends the W3C PROV standard and incorporates concepts from the Model Context Protocol (MCP) to represent agent actions and their connections to data and workflow tasks"
  - item: "Model Context Protocol (MCP) integration"
    chunk: 1
    lines: "144-150"
    quote: "These frameworks support MCP, which is emerging as a standard in academia and industry. MCP defines core agentic AI development concepts, including tools, prompts, resources, context management, and agent-client architecture"
  - item: "vs PROV-DfA"
    chunk: 1
    lines: "212-214"
    quote: "PROV-DfA extends PROV to capture human actions in human-steered workflows"
  - item: "vs ProvONE"
    chunk: 1
    lines: "214-216"
    quote: "ProvONE adds workflow-specific metadata and aims at supporting existing workflow management systems"
  - item: "vs PROV-ML"
    chunk: 1
    lines: "240-241"
    quote: "PROV-ML combines general workflow concepts with ML-specific artifacts, especially for model training and evaluation"
  - item: "vs FAIR4ML"
    chunk: 1
    lines: "241-243"
    quote: "FAIR4ML adopts a model-centric approach to support the Findability, Accessibility, Interoperability, and Reproducibility (FAIR) principles"
  - item: "vs earlier agent extensions"
    chunk: 1
    lines: "244-246"
    quote: "Although the W3C PROV has been extended for agents and multi-agent systems, these earlier efforts predate agentic workflows, lacking support for core agentic AI concepts and how they relate to broader workflow."

methodology: "Extension-based approach building on established W3C PROV standard. System implementation with decorator-based instrumentation (@flowcept_agent_tool) and LLM wrapper (FlowceptLLM). Preliminary evaluation using additive manufacturing use case at ORNL."

ai_integration:
  - item: "MCP (Model Context Protocol) integration"
    chunk: 1
    lines: "120-121"
    quote: "incorporates concepts from the Model Context Protocol (MCP) to represent agent actions and their connections to data and workflow tasks"
  - item: "RAG support"
    chunk: 1
    lines: "149-150"
    quote: "Retrieval-Augmented Generation (RAG) to dynamically augment prompts"
  - item: "LLM wrapper (FlowceptLLM)"
    chunk: 1
    lines: "358-361"
    quote: "this first implementation of PROV-AGENT focuses on supporting LLMs by providing a generic wrapper for abstract LLM objects, compatible with models from popular LLM interfaces, including CrewAI, LangChain, and OpenAI"
  - item: "Prompt-response capture"
    chunk: 1
    lines: "359-361"
    quote: "Whenever a prompt is sent to an LLM service provider in the cloud (e.g., OpenAI, SambaNova, Azure), the wrapper captures the prompt, response, model metadata"
  - item: "Hallucination tracking"
    chunk: 1
    lines: "21-26"
    quote: "agents can hallucinate or reason incorrectly, propagating errors when one agent's output becomes another's input. Thus, assuring that agents' actions are transparent, traceable, reproducible, and reliable is critical to assess hallucination risks and mitigate their workflow impacts."
  - item: "Natural language querying"
    chunk: 1
    lines: "372-377"
    quote: "Flowcept also provides an MCP agent with a Streamlit GUI that enables users to interact with the provenance database through natural language queries at runtime."

agent_modeling:
  - item: "AIAgent as PROV Agent subclass"
    chunk: 1
    lines: "200-203"
    quote: "the W3C PROV standard already defines Agent, the central abstraction in this work, as one of its three core classes, alongside Entity (data) and Activity (process), with agents representing either software or human actors responsible for activities"
  - item: "Multi-agent workflow support"
    chunk: 1
    lines: "281-284"
    quote: "This modeling is not constrained to single-agent scenarios. Multi-agentic workflows, with other AI agents, each with their own tools and reasoning paths, can be instantiated within the same provenance graph, enabling the representation of collaborative or parallel agent behaviors within a workflow."
  - item: "Agent attribution for generated data"
    chunk: 1
    lines: "301-303"
    quote: "When instances of subclasses of DataObject are generated by agent tools, they are attributed to (wasAttributedTo) the instance of the agent."
  - item: "Autonomous decision-making agents"
    chunk: 1
    lines: "51-54"
    quote: "This shift has driven the emergence of agentic workflows, where autonomous agents make decisions, plan tasks, and coordinate with humans and other agents."

agentic_workflows:
  - item: "Definition of agentic workflows"
    chunk: 1
    lines: "51-56"
    quote: "agentic workflows, where autonomous agents make decisions, plan tasks, and coordinate with humans and other agents. These agents operate in dynamic environments across heterogeneous computing platforms, including edge devices, cloud systems, and high-performance computing (HPC)."
  - item: "Non-deterministic and cyclic behavior"
    chunk: 1
    lines: "81-84"
    quote: "agentic workflows are non-deterministic, shaped by near real-time data, adaptive decisions, and evolving interactions. They often display dynamic, cyclic behavior, where agent outputs inform subsequent decisions or feedback loops."
  - item: "Cross-facility workflow execution"
    chunk: 1
    lines: "151-159"
    quote: "A growing challenge in these workflows involves managing execution across physically and logically distributed facilities that include edge devices, cloud services, and HPC systems"
  - item: "Agentic framework ecosystem"
    chunk: 1
    lines: "141-144"
    quote: "LangChain, AutoGen, LangGraph, Academy, and CrewAI support multi-agent systems that interact through prompt exchanges, calls to foundation models typically hosted by AI service providers in the cloud"
  - item: "Iterative feedback loops"
    chunk: 1
    lines: "438-445"
    quote: "each decision informs the decision logic in the next, enabling the system to learn over the course of a print. However, because the agent relies on an LLM, there is a risk of hallucinated or incorrect outputs. Since each decision influences the next in this iterative loop, a single error may propagate across layers"

generative_ai_patterns:
  - item: "Prompt-invocation-response interaction model"
    chunk: 1
    lines: "293-296"
    quote: "PROV-AGENT is designed to be modality-agnostic and supports other foundation models, such as those for vision, audio, or multimodal reasoning, as long as they follow a prompt-invocation-response interaction model."
  - item: "Hallucination propagation"
    chunk: 1
    lines: "87-88"
    quote: "hallucinated or incorrect outputs, especially when relying on generative models, which can propagate through the workflow, compounding errors"
  - item: "Structured prompts for decision-making"
    chunk: 1
    lines: "436-438"
    quote: "The agents use structured prompts to decide which control result is best for print control based on their scores and other data in the agent context, such as previous decisions and user guidance."
  - item: "Prompt engineering refinement"
    chunk: 1
    lines: "554-555"
    quote: "continuous agent improvement through the comparison of decisions across prompt engineering refinements or fine-tuning of model parameters"
  - item: "Model parameter tuning"
    chunk: 1
    lines: "190-191"
    quote: "refining prompts or tuning model parameters to reduce hallucinations"
  - item: "Foundation model invocation"
    chunk: 1
    lines: "46-50"
    quote: "foundation models, often referred to as Large X Models (LxMs)... excel in language, vision, time-series, and robotics tasks"

agent_ontology_integration:
  - item: "Agent actions as first-class workflow components"
    chunk: 1
    lines: "102-104"
    quote: "A unified provenance graph that considers AI agent actions as first-class components, on par with traditional workflow tasks, enables comprehensive traceability and analysis."
  - item: "Standard PROV constructs for queryable graphs"
    chunk: 1
    lines: "306-312"
    quote: "Since the relationships are explicitly modeled using standard PROV constructs such as used, wasGeneratedBy, wasAssociatedWith, and wasInformedBy, the resulting graph is fully connected and queryable. This enables users to trace a final output or decision all the way back through agent reasoning, prompts, input data, system context, and execution metadata"
  - item: "Integration of agent data with workflow context"
    chunk: 1
    lines: "299-301"
    quote: "This allows agents to consume and produce not only DomainData, but also system-level and contextual data such as SchedulingData and TelemetryData."
  - item: "MCP concepts mapped to PROV"
    chunk: 1
    lines: "255-256"
    quote: "It extends W3C PROV and incorporates MCP concepts to unify agents and traditional components as first-class elements."
  - item: "Critical provenance queries enabled"
    chunk: 1
    lines: "105-111"
    quote: "What specific input data led an agent to make a particular decision? How did an agent's decision influence the control or data flow within the workflow? Which downstream outputs were affected by a specific agent interaction?"

empirical_evidence:
  - item: "Oak Ridge National Laboratory additive manufacturing use case"
    chunk: 1
    lines: "419-425"
    quote: "We employ PROV-AGENT in an autonomous additive manufacturing workflow being developed at Oak Ridge National Laboratory (ORNL). This envisioned workflow integrates a metal 3D printer at ORNL's Manufacturing Demonstration Facility (MDF) on the Edge with an HPC system at the ORNL Leadership Computing Facility (OLCF)"
  - item: "Cross-facility Edge-Cloud-HPC evaluation"
    chunk: 1
    lines: "36-38"
    quote: "a cross-facility evaluation spanning edge, cloud, and HPC environments, demonstrating support for critical provenance queries and agent reliability analysis"
  - item: "Layer-by-layer sensor data streaming"
    chunk: 1
    lines: "429-432"
    quote: "At MDF, sensor drivers collect data layer by layer as a metal component is fabricated. This layer-specific data are used to estimate the current state of the system."
  - item: "Five query examples (Q1-Q5)"
    chunk: 1
    lines: "487-538"
    quote: "With PROV-AGENT, several new queries are enabled to support agent accountability and tracing back when errors/hallucinations happen."

limitations:
  - item: "Implementation focus on LLMs"
    chunk: 1
    lines: "356-358"
    quote: "Given our driving use cases and that most agentic workflow users employ LLMs for their agents, this first implementation of PROV-AGENT focuses on supporting LLMs"
  - item: "Limited metadata capture in initial implementation"
    chunk: 1
    lines: "367-369"
    quote: "While this implementation records only the agent's ID and name, the model supports extended metadata, such as model and tools' version control state, and further configuration parameters."
  - item: "Early-stage foundation"
    chunk: 1
    lines: "560-561"
    quote: "While this is an early step, it establishes a foundation that researchers and practitioners can build on"

tools_standards:
  - item: "W3C PROV standard"
    chunk: 1
    lines: "119"
    quote: "a provenance model that extends the W3C PROV standard"
  - item: "Model Context Protocol (MCP)"
    chunk: 1
    lines: "144-146"
    quote: "MCP, which is emerging as a standard in academia and industry"
  - item: "Flowcept open-source framework"
    chunk: 1
    lines: "321-323"
    quote: "we extend Flowcept, an open-source distributed provenance framework designed for complex, heterogeneous workflows spanning experimental facilities at the edge, cloud platforms, and HPC environments"
  - item: "Python decorators (@flowcept_agent_tool)"
    chunk: 1
    lines: "346-351"
    quote: "since MCP tools have well-defined input arguments and return values, we introduce a new decorator, @flowcept_agent_tool, which creates a corresponding AgentTool execution activity for each tool execution"
  - item: "FlowceptLLM wrapper"
    chunk: 1
    lines: "358-359"
    quote: "providing a generic wrapper for abstract LLM objects, compatible with models from popular LLM interfaces, including CrewAI, LangChain, and OpenAI"
  - item: "Streamlit GUI"
    chunk: 1
    lines: "372-373"
    quote: "Flowcept also provides an MCP agent with a Streamlit GUI that enables users to interact with the provenance database"
  - item: "Data streaming services"
    chunk: 1
    lines: "329-332"
    quote: "from data streaming services and storage layers such as Redis, Kafka, SQLite, file systems, and object stores while the workflows run"
---

# PROV-AGENT: Unified Provenance for Tracking AI Agent Interactions in Agentic Workflows

## Paper Overview

- **Source**: 03-PROV-AGENT_Unified_Provenance_for_AI_Agents.pdf
- **Chunks**: 1 chunk, ~8940 estimated tokens
- **Analyzed**: 2025-12-31
- **Venue**: IEEE International Conference on e-Science 2025

## Summary

PROV-AGENT is a provenance model that extends W3C PROV to capture AI agent interactions, model invocations, and their relationships to non-agentic tasks and data in agentic workflows. The model incorporates Model Context Protocol (MCP) concepts to unify agents and traditional workflow components as first-class elements in a queryable provenance graph.

## Key Contributions

1. **PROV-AGENT Model**: A provenance model extending W3C PROV with AI agent-specific concepts including AIAgent, AgentTool, AIModelInvocation, AIModel, Prompt, and ResponseData entity types.

2. **Open-source Implementation**: Extension of Flowcept framework with Python decorators (@flowcept_agent_tool) and LLM wrappers (FlowceptLLM) for capturing agentic provenance at runtime.

3. **Cross-facility Evaluation**: Demonstration using Oak Ridge National Laboratory's additive manufacturing workflow spanning edge devices, cloud services, and HPC systems.

## Key Extractions

### Entity Types and Definitions

The model introduces a clear hierarchy:
- **Core PROV classes**: Agent, Entity, Activity
- **AI extensions**: AIAgent (extends Agent), AgentTool (extends Activity), AIModelInvocation
- **Data types**: DataObject, DomainData, Prompt, ResponseData, SchedulingData, TelemetryData, AIModel

| Entity | Type | Source | Quote |
|--------|------|--------|-------|
| AIAgent | Agent subclass | Chunk 1:278-284 | "We extend the abstract W3C PROV Agent by modeling AIAgent as its subclass" |
| AgentTool | Activity | Chunk 1:285-286 | "agent associated with tool executions (AgentTool)" |
| AIModelInvocation | Activity | Chunk 1:287-288 | "informed by one or many AIModelInvocations" |
| DataObject | Entity subclass | Chunk 1:274-276 | "subclasses of DataObject, subclass of PROV Entity" |

### Entity Relationships

Standard PROV relationships are used throughout:

| Relationship | Purpose | Source |
|-------------|---------|--------|
| used | Task/Invocation consumes data | Chunk 1:265,288 |
| wasGeneratedBy | Task/Invocation produces data | Chunk 1:265-266,290 |
| wasInformedBy | Tool informed by LLM invocation | Chunk 1:365-367 |
| wasAttributedTo | Response attributed to agent | Chunk 1:291-292 |
| wasAssociatedWith | Campaign/Tool associated with agent | Chunk 1:264,349 |

### AI Integration Patterns

| Pattern | Source | Quote |
|---------|--------|-------|
| MCP integration | Chunk 1:120-121 | "incorporates MCP to represent agent actions" |
| RAG support | Chunk 1:149-150 | "RAG to dynamically augment prompts" |
| FlowceptLLM wrapper | Chunk 1:358-361 | "compatible with CrewAI, LangChain, OpenAI" |
| Hallucination tracking | Chunk 1:21-26 | "assess hallucination risks and mitigate workflow impacts" |

### Framework Comparisons

| Framework | Comparison | Source |
|-----------|------------|--------|
| W3C PROV | Base standard being extended | Chunk 1:118-121 |
| MCP | Source of agentic concepts | Chunk 1:144-150 |
| PROV-DfA | Human-steered workflows (complementary) | Chunk 1:212-214 |
| ProvONE | Workflow-specific metadata (complementary) | Chunk 1:214-216 |
| PROV-ML | ML artifacts (complementary) | Chunk 1:240-241 |
| FAIR4ML | FAIR principles (complementary) | Chunk 1:241-243 |

### Key Findings (with evidence)

- **Agent-Activity-Entity Validation** (Chunk 1:200-204): "W3C PROV standard already defines Agent, the central abstraction in this work, as one of its three core classes, alongside Entity (data) and Activity (process)"

- **Multi-agent Support** (Chunk 1:281-284): "This modeling is not constrained to single-agent scenarios. Multi-agentic workflows, with other AI agents, each with their own tools and reasoning paths"

- **Queryable Provenance Graph** (Chunk 1:306-312): "the resulting graph is fully connected and queryable. This enables users to trace a final output or decision all the way back through agent reasoning"

## Chunk Navigation

### Chunk 1: Full Paper Content (Lines 1-707)

- **Summary**: Complete paper covering PROV-AGENT provenance model for agentic workflows. Extends W3C PROV with AI-specific entities (AIAgent, AgentTool, AIModelInvocation). Includes MCP integration, Flowcept implementation, and ORNL additive manufacturing use case evaluation.

- **Key concepts**: [W3C PROV, Agent-Activity-Entity triad, AIAgent, AgentTool, AIModelInvocation, MCP, Flowcept, provenance graph, hallucination tracking, cross-facility workflow]

- **Key quotes**:
  - Line 200: "W3C PROV standard already defines Agent, the central abstraction..."
  - Line 278: "We extend the abstract W3C PROV Agent by modeling AIAgent as its subclass..."
  - Line 285: "Following the MCP terminology, an AI agent can be associated with one or many tool executions..."
  - Line 306-312: "the resulting graph is fully connected and queryable..."

- **Load when**:
  - "Query about W3C PROV extensions for AI agents"
  - "How to track AI agent provenance"
  - "Agent-Activity-Entity relationships"
  - "MCP integration with provenance"
  - "Hallucination tracking in workflows"
  - "Cross-facility agentic workflow patterns"
