# Generative Ai Patterns

**Source**: Project 16 Ontologies Research v3

**Type**: Synthesis Analysis (UDWO-Primed)

**Field**: generative_ai_patterns

**Aggregated**: 2026-01-01T16:22:26.835369

**Batches Merged**: 5

---

## Table of Contents

- [Patterns](#patterns)

## Patterns

**Total Patterns**: 139

### 1. Prompt-Response-Decision Provenance Pattern

Pattern for tracking the complete chain of LLM interactions including prompts sent, responses received, and decisions made. Enables traceability from final outputs back through the reasoning process for debugging and reliability analysis.

**Sources**:

- **03-PROV-AGENT (Chunk 1:27-29)**
  > existing methods fail to capture and relate agent-centric metadata such as prompts, responses, and decisions with the broader workflow context

---

### 2. Retrieval-Augmented Generation (RAG) for Prompt Enhancement

Pattern where agents use external knowledge bases or web pages to dynamically enhance prompts with contextual information before sending to LLM. Improves response accuracy by grounding generation in retrieved knowledge.

**Sources**:

- **03-PROV-AGENT (Chunk 1:148-150)**
  > Retrieval-Augmented Generation (RAG) to dynamically augment prompts

---

### 3. Model Context Protocol (MCP) Tool Integration

Standardized pattern for LLM agents to interact with external tools, manage prompts, handle resources, and maintain context. Provides structured interface for function calling and tool use in agentic workflows.

**Sources**:

- **03-PROV-AGENT (Chunk 1:144-147)**
  > MCP defines core agentic AI development concepts, including tools, prompts, resources, context management, and agent-client architecture

---

### 4. LLM Invocation Wrapper Pattern

Pattern of wrapping LLM calls (FlowceptLLM) to capture prompts, responses, model metadata, and telemetry automatically. Enables standardized instrumentation across different LLM providers.

**Sources**:

- **03-PROV-AGENT (Chunk 1:356-364)**
  > a generic wrapper for abstract LLM objects, compatible with models from popular LLM interfaces, including CrewAI, LangChain, and OpenAI

---

### 5. Agent Tool Decorator Pattern

Pattern using decorators to instrument agent tool functions, automatically capturing inputs, outputs, and linking to agent identity. Enables automatic provenance capture during function calling.

**Sources**:

- **03-PROV-AGENT (Chunk 1:344-351)**
  > @flowcept_agent_tool decorator... creates a corresponding AgentTool execution activity for each tool execution

---

### 6. Hallucination Detection via Lineage Tracing

Pattern for detecting and diagnosing LLM hallucinations by tracing back through the provenance graph to find the exact prompt and response that led to an erroneous output. Enables root cause analysis.

**Sources**:

- **03-PROV-AGENT (Chunk 1:486-492)**
  > What was the LLM prompt and response when a surprising agent decision was identified?

---

### 7. Decision Propagation Tracking

Pattern for tracking how LLM decisions cascade through downstream tasks using provenance relationships. Enables understanding the impact of individual LLM outputs on final results.

**Sources**:

- **03-PROV-AGENT (Chunk 1:523-529)**
  > How did an agent decision influence subsequent workflow activities?... the query recursively navigates on the used/wasGeneratedBy relationships

---

### 8. Iterative Agent Learning Loop

Pattern where LLM agent decisions in iteration i influence the context and decision logic for iteration i+1, creating a learning feedback loop. Enables adaptive behavior through accumulated context.

**Sources**:

- **03-PROV-AGENT (Chunk 1:438-445)**
  > the decision made for each layer informs the decision logic in the next, enabling the system to learn over the course of a print

---

### 9. In-Context Learning from Knowledge Graph

Pattern where LLMs adapt responses based on context embedded within prompts derived from knowledge graphs. Avoids fine-tuning by providing relevant context dynamically during inference.

**Sources**:

- **15-SciAgents (Chunk 1:95-102)**
  > in-context learning emerges as a compelling strategy to enhance the performance of LLMs without the need for costly and time-intensive fine-tuning

---

### 10. Knowledge Graph Path Sampling for Context

Pattern of sampling paths between concepts in a knowledge graph to create contextual substrate for LLM reasoning. Random path approach enriches context with broader conceptual relationships.

**Sources**:

- **15-SciAgents (Chunk 1:133-148)**
  > We implemented a novel sampling strategy to extract relevant sub-graphs from this comprehensive knowledge graph, allowing us to identify and understand the key concepts

---

### 11. Multi-Agent Role Specialization

Merged from 2 sources. Pattern where multiple specialized LLM agents are assigned distinct roles (hypothesis, outcome, mechanism, design principles, unexpected properties, comparison, novelty, critic) to collaboratively expand different aspects of a research proposal. Each agent has a focused responsibility contributing to a comprehensive output.

**Sources**:

- **15-SciAgents (Chunk 1:126-130)**
  > Each agent in the system is assigned a distinct role, optimized through complex prompting strategies to ensure that every subtask is tackled with targeted expertise

- **15-SciAgents (Chunk 4:1-6)**
  > design_principle agent...unexpected_properties_agent...comparison_agent...novelty_agent...critic_agent: Summarizes, critiques, and suggests improvements

---

### 12. Hierarchical Expansion Strategy

Pattern of iteratively expanding and refining LLM outputs through multiple passes: initial generation, expansion with details, critique, and amendment. Produces comprehensive outputs from structured iteration.

**Sources**:

- **15-SciAgents (Chunk 1:200-210)**
  > We employ a hierarchical expansion strategy where answers are successively refined and improved, enriched with retrieved data, critiqued and amended

---

### 13. Structured JSON Output Generation

Pattern of prompting LLMs to generate structured JSON outputs with predefined fields (hypothesis, outcome, mechanisms, design principles, novelty). Enables downstream parsing and systematic expansion.

**Sources**:

- **15-SciAgents (Chunk 1:205-206)**
  > generating structured output in JSON following a specific set of aspects that the model is tasked to develop

---

### 14. Ontologist Agent for Concept Definition

Pattern of using a dedicated LLM agent to analyze knowledge graph paths, define concepts, explain relationships, and prepare semantic context for downstream hypothesis generation.

**Sources**:

- **15-SciAgents (Chunk 1:289-296)**
  > the ontologist agent... applies advanced reasoning and inference techniques to synthesize and interpret the complex web of data

---

### 15. Scientist Agent for Hypothesis Generation

Pattern of using specialized LLM agent with structured prompts to synthesize novel hypotheses from ontological context. Agent generates proposals addressing hypothesis, mechanisms, outcomes, and novelty.

**Sources**:

- **15-SciAgents (Chunk 1:356-365)**
  > The scientist agent harnesses the extensive knowledge parsed from the knowledge graph... to propose novel research ideas. Through complex prompting

---

### 16. Critic Agent for Hypothesis Review

Pattern of adversarial review by dedicated LLM agent that evaluates generated hypotheses for strengths, weaknesses, and suggests improvements. Implements peer-review-like quality control.

**Sources**:

- **15-SciAgents (Chunk 1:511-516)**
  > the Critic agent, responsible for thoroughly reviewing the research proposal, summarizing its key points, and recommending improvements

---

### 17. Pre-programmed vs Autonomous Agent Interactions

Two patterns for multi-agent orchestration: (1) pre-programmed sequence ensuring consistency, (2) autonomous dynamic interactions adapting to evolving context. Second approach allows human-in-the-loop intervention.

**Sources**:

- **15-SciAgents (Chunk 1:186-197)**
  > In the first approach... interactions between agents are pre-programmed and follow a predefined sequence... In contrast, the second approach features fully automated agent interactions

---

### 18. Novelty Assessment via Literature Search

Pattern of using external API tools (Semantic Scholar) to validate novelty of LLM-generated hypotheses by searching existing literature. Prevents redundant or unoriginal outputs.

**Sources**:

- **15-SciAgents (Chunk 1:195-197)**
  > empowered our automated multi-agent model with the Semantic Scholar API as a tool that provides it with an ability to check the novelty of the generated hypothesis against existing literature

---

### 19. Swarm Intelligence for Scientific Discovery

Pattern of using multiple specialized LLM agents working together in iterative cycles, mimicking biological swarm intelligence. Enables more nuanced reasoning than single-agent zero-shot approaches.

**Sources**:

- **15-SciAgents (Chunk 2:138-142)**
  > harnessing a modular, hierarchically organized swarm of intelligence similar to biological systems with multiple iterations to model the process of negotiation

---

### 20. Graph-Based Context Retrieval for Reasoning

Pattern of using knowledge graphs as foundational context for LLM reasoning. Graph structure ensures generated outputs are grounded in interconnected scientific concepts rather than pure hallucination.

**Sources**:

- **15-SciAgents (Chunk 2:145-149)**
  > The ontological knowledge graph representation of data plays a crucial role... ensuring that the hypotheses proposed by the AI agents are both informed by and rooted in a vast network

---

### 21. Heuristic Pathfinding with Random Waypoints

Pattern for sampling knowledge graph paths using embeddings and randomization to create diverse context for LLM prompts. Balances heuristic search with stochastic exploration.

**Sources**:

- **15-SciAgents (Chunk 2:245-260)**
  > The algorithm... combines heuristic-based pathfinding with node embeddings and randomized waypoints to discover diverse paths in a graph

---

### 22. Prompt-Driven Aspect Expansion

Pattern of iterating through structured JSON fields and using targeted prompts to expand each aspect with specific details (chemical formulas, sequences, methods). Enables systematic depth enhancement.

**Sources**:

- **15-SciAgents (Chunk 2:343-376)**
  > systematically expanding specific aspects of the hypothesis using a series of targeted prompts... asking the model to expand upon the original content by adding quantitative details

---

### 23. Scientific Critique Prompt Pattern

Pattern of prompting LLM to perform critical scientific review identifying strengths, weaknesses, and improvements. Implements automated peer review quality control.

**Sources**:

- **15-SciAgents (Chunk 2:410-421)**
  > a prompt is issued to the model to critically review the entire document. The review is designed to evaluate both the strengths and weaknesses

---

### 24. Modeling Priority Identification

Pattern of prompting LLM to identify key actionable research questions and outline experimental or simulation steps. Translates hypotheses into concrete research plans.

**Sources**:

- **15-SciAgents (Chunk 2:427-452)**
  > the model is prompted to identify the most impactful scientific questions related to molecular modeling and synthetic biology

---

### 25. AutoGen Multi-Agent Framework Integration

Pattern of implementing multi-agent LLM systems using AutoGen framework with specialized agent types (UserProxy, Assistant) and group chat management for coordinated reasoning.

**Sources**:

- **15-SciAgents (Chunk 2:480-492)**
  > The automated multi-agent collaboration is implemented in the AutoGen framework... using UserProxyAgent, AssistantAgent, and GroupChatManager classes

---

### 26. Novelty Assistant with Multi-Query Search

Pattern of using specialized LLM agent to perform multiple literature searches with varied keywords, then analyzing abstracts to assess novelty. Implements robust novelty verification.

**Sources**:

- **15-SciAgents (Chunk 2:505-510)**
  > an AI agent named the novelty assistant, which calls the Semantic Scholar API three times using different combinations of keywords

---

### 27. Molecular Dynamics Simulation Planning

Pattern of LLM generating detailed molecular dynamics simulation plans including software recommendations (GROMACS, AMBER), force field selection, and analysis protocols. Bridges AI reasoning with computational chemistry.

**Sources**:

- **15-SciAgents (Chunk 3:101-108)**
  > Molecular Dynamics (MD) Simulations: Use MD simulations to model the interactions... Software such as GROMACS or AMBER can be employed to study the self-assembly process

---

### 28. Step-by-Step Rationale Generation

Pattern of LLM generating explicit step-by-step rationale with specific procedural details (chemicals, temperatures, durations). Implements chain-of-thought reasoning with domain-specific expertise.

**Sources**:

- **15-SciAgents (Chunk 3:28-41)**
  > Rationale and Step-by-Step Reasoning... Extract silk fibroin from Bombyx mori cocoons using a degumming process

---

### 29. Multi-Agent Research Proposal Pipeline

Complete pipeline pattern for automated scientific discovery: ontologist defines concepts, scientist drafts proposal, specialized agents expand aspects (hypothesis, mechanism, novelty), critic reviews, assistant rates feasibility.

**Sources**:

- **15-SciAgents (Chunk 3:909-918)**
  > ontologist will define each term... scientist will craft a research proposal... specialized agents... will expand on their respective sections... critic_agent will summarize, critique

---

### 30. Ontologist-First Knowledge Grounding

Pattern where an ontologist agent first defines terms and their relationships before any creative generation occurs. This grounds subsequent LLM reasoning in explicit semantic definitions, preventing hallucination and ensuring conceptual consistency.

**Sources**:

- **15-SciAgents (Chunk 4:12-13)**
  > Define Terms and Relationships: The ontologist will define each term in the knowledge path and discuss the relationships between them

---

### 31. Sequential Plan Execution with Reasoning

Pattern of structured multi-step execution where each step has explicit reasoning (why it matters) and actions (what to do). The LLM follows a predetermined plan with clear phase transitions and role handoffs between specialized agents.

**Sources**:

- **15-SciAgents (Chunk 4:9-18)**
  > Overview of the Plan: 1. Define Terms and Relationships...2. Craft the Research Proposal...3. Expand Key Aspects...4. Critique and Improve...5. Rate Novelty

---

### 32. Function Calling for Structured Outputs

Pattern where LLM agents invoke structured function calls (tools) to produce standardized outputs like novelty/feasibility ratings. This constrains the output format and enables programmatic processing of agent decisions.

**Sources**:

- **15-SciAgents (Chunk 4:73)**
  > The assistant will call the functions.rate_novelty_feasibility function to rate the research idea

---

### 33. Critic Agent Review Pattern

Pattern where a dedicated critic agent reviews all outputs from specialist agents, providing meta-level evaluation, identifying weaknesses, and suggesting improvements. This creates a quality control layer in multi-agent systems.

**Sources**:

- **15-SciAgents (Chunk 4:5-6)**
  > critic_agent: Summarizes, critiques, and suggests improvements after all seven aspects of the proposal have been expanded by the agents

---

### 34. Knowledge Graph Path-Guided Generation

Pattern where LLM generation is guided by paths extracted from a knowledge graph. Random or intentional keyword selection seeds the generation, and relationships between concepts structure the creative output.

**Sources**:

- **15-SciAgents (Chunk 5:145-146)**
  > Use the generate_path function to generate a knowledge path between two randomly selected keywords

---

### 35. Structured Research Proposal Template

Merged from 2 sources. Pattern of using a fixed 7-section template (Hypothesis, Outcome, Mechanisms, Design Principles, Unexpected Properties, Comparison, Novelty) to structure LLM-generated research proposals. Each section has specific semantic expectations and is expanded by specialized agents.

**Sources**:

- **15-SciAgents (Chunk 4:148-225)**
  > Research Proposal: 1- Hypothesis...2- Outcome...3- Mechanisms...4- Design Principles...5- Unexpected Properties...6- Comparison...7- Novelty

- **15-SciAgents (Chunk 9:497-511)**
  > The key aspects of the proposal include: 1. Hypothesis... 2. Outcome... 3. Mechanisms... 4. Design Principles... 5. Unexpected Properties... 6. Comparison... 7. Novelty...

---

### 36. Quantitative Goal Setting in Prompts

Pattern where prompts include specific quantitative targets and metrics that the LLM must address. This constrains outputs to include measurable, verifiable claims rather than vague qualitative statements.

**Sources**:

- **15-SciAgents (Chunk 4:162-164)**
  > Mechanical Strength: Enhanced tensile strength of up to 1.5 GPa...Energy Efficiency: Reduction in energy consumption by 30%

---

### 37. Modeling and Simulation Technique Specification

Pattern where LLM outputs must specify concrete computational methods (MD simulations, FEA) with parameters. Forces the LLM to ground abstract claims in specific, executable scientific methodologies.

**Sources**:

- **15-SciAgents (Chunk 4:298-311)**
  > Molecular Dynamics (MD) Simulations: To understand the interaction...Finite Element Analysis (FEA): FEA will be used to model the mechanical behavior

---

### 38. Experimental Validation Method Specification

Pattern requiring LLM to specify concrete experimental methods with parameters for validating proposed mechanisms. Prevents purely theoretical outputs by demanding actionable experimental protocols.

**Sources**:

- **15-SciAgents (Chunk 4:311-319)**
  > Electrospinning: Parameters such as voltage, flow rate, and collector distance will be optimized...Tensile Testing...Cell Culture Studies

---

### 39. Novelty and Feasibility Rating Pattern

Merged from 2 sources. Pattern of explicitly rating research ideas on numeric scales for novelty and feasibility, with detailed justification citing literature support and technical challenges. Enables quantitative comparison of generated ideas.

**Sources**:

- **15-SciAgents (Chunk 4:985-998)**
  > Novelty: 7/10...Multi-scale Organizational Properties of Silk: The concept...is well-documented...Feasibility: 8/10

- **15-SciAgents (Chunk 9:639-646)**
  > Novelty: 7/10 - The idea of mimicking nacre's hierarchical structure to enhance mechanical properties is well-explored... Feasibility: 8/10 - The feasibility of creating nacre-like structures using modern fabrication techniques

---

### 40. Literature-Grounded Validation

Pattern where LLM-generated hypotheses are validated against literature search results. The system queries academic databases and uses the presence or absence of prior work to assess novelty claims.

**Sources**:

- **15-SciAgents (Chunk 6:144-165)**
  > Query 1: biomimetic materials microfluidic chips...Total Results: 36...Relevant Papers: Surface treatments for microfluidic biocompatibility

---

### 41. Strengths-Weaknesses-Improvements Review Structure

Pattern of structured critique using explicit Strengths, Weaknesses, and Suggested Improvements sections. Provides balanced evaluation and actionable feedback rather than unstructured commentary.

**Sources**:

- **15-SciAgents (Chunk 6:54-82)**
  > Strengths: 1. Innovative Approach...Weaknesses: 1. Complex Fabrication Process...Suggested Improvements: 1. Pilot Studies

---

### 42. Multi-Scale Mechanism Decomposition

Pattern where LLM must decompose mechanisms across multiple spatial scales (molecular, cellular, macroscale). Forces hierarchical thinking about cause-effect relationships at different levels of organization.

**Sources**:

- **15-SciAgents (Chunk 6:636-748)**
  > Molecular Scale Mechanisms...Cellular Scale Mechanisms...Macroscale Mechanisms

---

### 43. Impactful Scientific Question Generation

Pattern where LLM generates specific scientific questions identified as most impactful, along with concrete key steps for addressing them through molecular modeling or synthetic biology experiments.

**Sources**:

- **15-SciAgents (Chunk 6:85-115)**
  > Most Impactful Scientific Question for Molecular Modeling: How does the lamellar structure...Key Steps for Molecular Modeling: 1. Model Development...2. Parameterization

---

### 44. Agent Team Assembly Declaration

Pattern of explicitly declaring the multi-agent team composition at the start of a collaborative task. Each agent's role and capabilities are stated upfront, establishing clear responsibilities and coordination structure.

**Sources**:

- **15-SciAgents (Chunk 5:127-139)**
  > Hello everyone. We have assembled a great team today...user: An attentive HUMAN user...planner...assistant...ontologist...scientist...hypothesis_agent

---

### 45. Random Keyword Path Generation

Pattern of using random keyword selection to seed novel research idea generation. By not specifying keywords, the system explores unexpected concept combinations from the knowledge graph.

**Sources**:

- **15-SciAgents (Chunk 5:163-165)**
  > The assistant will call the generate_path function with keyword_1 and keyword_2 set to None to generate a path between randomly selected nodes

---

### 46. Comparative Benchmark Analysis

Pattern of structured comparison between traditional/baseline approaches and proposed innovations. Each comparison includes typical performance benchmarks, expected improvements with quantitative goals, and explicit rationale.

**Sources**:

- **15-SciAgents (Chunk 7:88-132)**
  > Traditional Materials: Typical Performance...Quantitative Benchmark...Proposed Material: Expected Performance...Quantitative Goal...Rationale

---

### 47. Sequential Agent Calling Pattern

A structured multi-agent workflow where a caller agent orchestrates sequential invocations of specialized agents (hypothesis_agent, outcome_agent, mechanism_agent, design_principles_agent, etc.) to iteratively expand and refine outputs. Each agent has a specific role in the generation pipeline.

**Sources**:

- **15-SciAgents (Chunk 9:34-37)**
  > Agent caller, please proceed by calling the hypothesis_agent to expand on the 'hypothesis' aspect of the research proposal.

---

### 48. Role-Based Agent Specialization

LLM agents are assigned distinct personas and specialized roles (planner, ontologist, scientist, critic, hypothesis_agent, outcome_agent, etc.) that constrain and guide their outputs. Each role has defined responsibilities and output expectations.

**Sources**:

- **15-SciAgents (Chunk 9:673-679)**
  > planner: Who can suggest a step-by-step plan... ontologist: I can define each of the terms... scientist: I can craft the research proposal... critic_agent: I can summarize, critique

---

### 49. Literature Review Integration

Integration of structured literature review into the generation pipeline, where the LLM synthesizes existing research to inform and validate novel hypothesis generation, providing evidence-based grounding.

**Sources**:

- **15-SciAgents (Chunk 9:562-635)**
  > Literature Review Summary: 1. Fusion of Seashell Nacre and Marine Bioadhesive Analogs... 2. Peptide-Polymer Conjugates... 3. Materiomics: Biological Protein Materials

---

### 50. Critical Scientific Review Pattern

A structured critique pattern where the critic_agent evaluates generated content through systematic analysis of strengths, weaknesses, and suggested improvements, enabling iterative refinement.

**Sources**:

- **15-SciAgents (Chunk 9:517-546)**
  > Strengths: 1. Innovative Approach... 2. Comprehensive Design... Weaknesses: 1. Complexity... 2. Scalability... Suggested Improvements: 1. Simplification...

---

### 51. Knowledge Path Generation

A pattern for generating conceptual knowledge paths between entities using function calling, establishing relationships that inform subsequent research proposal generation.

**Sources**:

- **15-SciAgents (Chunk 9:688-703)**
  > Generate Knowledge Path: Identify the key concepts and relationships between graphene and proteins... Assistant will call the functions.generate_path function with 'graphene' and 'proteins' as keywords

---

### 52. Ontologist Definition Pattern

Structured extraction of definitions and relationships from knowledge graphs, where an ontologist agent provides formal semantic grounding for terms used in the generation process.

**Sources**:

- **15-SciAgents (Chunk 9:759-789)**
  > Definitions: Graphene: A single layer of carbon atoms... Relationships: Graphene -- bind -- Amyloid Fibrils: Graphene can interact with amyloid fibrils

---

### 53. Quantitative Hypothesis Specification

A pattern for generating specific, quantitative predictions within hypotheses, transforming vague claims into measurable expectations with numerical targets.

**Sources**:

- **15-SciAgents (Chunk 10:22-29)**
  > Conductivity Mechanism: The hypothesis posits that the incorporation of amyloid fibrils into graphene will create conductive pathways... Quantitative Conductivity Improvement: We anticipate that the electrical conductivity... will be significantly higher

---

### 54. Molecular Modeling Integration Pattern

A structured pattern for generating computational methodology, including technique selection, parameter specification, and validation approaches, enabling LLM-guided scientific workflow generation.

**Sources**:

- **15-SciAgents (Chunk 10:505-566)**
  > Select Appropriate Modeling Techniques: Molecular Dynamics (MD) Simulations... Density Functional Theory (DFT)... Monte Carlo Simulations... Set Up the Simulation Environment: Force Fields: Choose suitable force fields

---

### 55. Emergent Properties Prediction

A generative pattern for predicting emergent and unexpected properties in novel materials, encouraging creative extrapolation beyond explicitly stated hypotheses.

**Sources**:

- **15-SciAgents (Chunk 10:253-274)**
  > Expanded Unexpected Properties: 1. Emergent Electrical Properties: Quantum Effects... 2. Enhanced Mechanical Properties: Synergistic Reinforcement... Self-Healing Ability

---

### 56. Comparative Analysis Generation

Structured generation of multi-dimensional comparisons across relevant benchmarks, providing systematic evaluation of novel proposals against existing approaches.

**Sources**:

- **15-SciAgents (Chunk 10:313-364)**
  > Expanded Comparison: 1. Electrical Conductivity: Graphene vs. Amyloid Fibrils... Graphene Composites... 2. Mechanical Properties... 3. Biocompatibility

---

### 57. Novelty Assessment with Evidence

A rating pattern that combines quantitative scores with explicit reasoning chains, grounding novelty and feasibility assessments in specific evidence from the literature review.

**Sources**:

- **15-SciAgents (Chunk 10:619-631)**
  > Novelty: 8/10 - The hypothesis presents a novel integration of graphene and amyloid fibrils for bioelectronic applications, with an innovative approach of using engineered gene circuits... Feasibility: 7/10

---

### 58. Autonomous Tool Selection Pattern

An autonomous agent pattern where the LLM iteratively selects appropriate tools from a toolbox, executes them, and updates memory state without human intervention in the reasoning loop.

**Sources**:

- **16-KG-Agent (Chunk 1:26-29)**
  > we integrate the LLM, multifunctional toolbox, KG-based executor, and knowledge memory, and develop an iteration mechanism that autonomously selects the tool then updates the memory

---

### 59. Code-Based Instruction Synthesis

A pattern for converting natural language reasoning into structured code-like function calls, enabling more precise and executable reasoning traces that can be used for LLM fine-tuning.

**Sources**:

- **16-KG-Agent (Chunk 1:31-34)**
  > we leverage program language to formulate the multi-hop reasoning process over the KG, and synthesize a code-based instruction dataset to fine-tune the base LLM

---

### 60. Three-Tool-Type Architecture

A systematic toolbox organization pattern with extraction tools (get_relation, get_entity), logic tools (count, intersect, judge, end), and semantic tools (retrieve_relation, disambiguate_entity) for structured KG reasoning.

**Sources**:

- **16-KG-Agent (Chunk 1:239-259)**
  > Extraction tools aim to facilitate the access to information from KG... Logic tools aim to support basic manipulation operations... Semantic tools are developed by utilizing pre-trained models

---

### 61. Knowledge Memory Pattern

A structured memory architecture for LLM agents containing question context, available tools, retrieved KG information, and execution history to support informed decision-making.

**Sources**:

- **16-KG-Agent (Chunk 1:546-551)**
  > The knowledge memory preserves the currently useful information to support the LLM-based planner for making decisions. It mainly contains four parts of information: natural language question, toolbox definition, current KG information, and history reasoning program

---

### 62. Function Call Generation Pattern

A pattern for LLMs to generate structured function calls (e.g., get_relation, get_tail_entity, get_entity_by_constraint) that can be programmatically executed against knowledge graphs.

**Sources**:

- **16-KG-Agent (Chunk 1:437-456)**
  > we reformulate the triples into several function calls with the code format, which represents the tool invocation and can be executed to obtain the corresponding triples... get_relation(e) function call to obtain the current candidate relations

---

### 63. Iterative Planner-Executor Loop

An iterative reasoning pattern where planning (tool selection) and execution (memory update) alternate until the agent determines reasoning is complete, enabling multi-hop inference.

**Sources**:

- **16-KG-Agent (Chunk 1:629-638)**
  > The KG-Agent framework autonomously iterates the above tool selection and memory updation process to perform step-by-step reasoning, where the knowledge memory is used to maintain the accessed information

---

### 64. Query Graph to Program Conversion

A systematic conversion pattern from structured query graphs to executable reasoning programs through BFS traversal, generating ordered function call sequences.

**Sources**:

- **16-KG-Agent (Chunk 1:419-433)**
  > the query graph has a tree-like structure that can be directly mapped to a logical form... starting from the mentioned entity in the question, we adopt breadth-first search (BFS) to visit all the nodes on the query graph

---

### 65. Divide and Conquer Goal Decomposition

A fundamental LLM-powered multi-agent pattern where complex goals are decomposed into subtasks assigned to specialized agents, mimicking Minsky's 'society of mind' theory for collective problem-solving.

**Sources**:

- **18-Multi-Agent (Chunk 1:66-71)**
  > Such systems tackle user-prompted goals by employing a divide & conquer strategy, by breaking them down into smaller manageable tasks. These tasks are then assigned to specialized agents

---

### 66. Prompt Augmentation Pattern

A systematic pattern for enriching agent prompts with role context, memory contents, retrieved information, and templates before LLM processing, enabling more informed and contextual responses.

**Sources**:

- **18-Multi-Agent (Chunk 1:959-968)**
  > Before the LLM receives the Agent Prompt, it may undergo Prompt Augmentation. This process can integrate additional specifics like the aspects or parts of the agent's Role or Memory, Context Information... or chosen Prompt Templates

---

### 67. Task-Management Agent Types

A taxonomy of specialized agent types for task management: creation agents (decomposition), prioritization agents (dependency resolution), and execution agents (task completion), each with distinct LLM-powered capabilities.

**Sources**:

- **18-Multi-Agent (Chunk 2:2-12)**
  > Task-Creation Agent: Generating new tasks, which optionally also includes deriving tasks by breaking down complex tasks. Task-Prioritization Agent: Assigning urgency... Task-Execution Agent: Ensuring efficient task completion

---

### 68. Action Type Taxonomy

A comprehensive taxonomy of agent actions enabling structured collaboration: task decomposition, creation, delegation, execution, evaluation, and result merging, forming the vocabulary of multi-agent coordination.

**Sources**:

- **18-Multi-Agent (Chunk 2:38-49)**
  > DecomposeTask: Breaking down a task into multiple sub-tasks... Create Task... DelegateTask: Delegating a task to another agent... ExecuteTask... EvaluateResult... MergeResult

---

### 69. Communication Protocol Patterns

Three distinct communication protocol patterns for multi-agent LLM systems: (1) strict sequential chains, (2) two-agent dialogue cycles, and (3) flexible multi-cycle frameworks, each suited to different task complexities.

**Sources**:

- **18-Multi-Agent (Chunk 2:82-96)**
  > Strict finite processes or execution chains with predefined action sequences... Dialogue cycles characterized by alternating DelegateTask and ExecuteTask actions... Multi-cycle process frameworks with interactions between generic agent types

---

### 70. Contextual Resource Integration

Merged from 2 sources. A comprehensive framework for integrating contextual resources into LLM agents, categorizing tools (search, execution, reasoning, development, communication), data types (structured, unstructured, multimodal, domain-specific), and foundation models.

**Sources**:

- **18-Multi-Agent (Chunk 2:104-171)**
  > Tools: Search and Analysis Tools... Execution Tools... Reasoning Tools... Development Tools... Communication Tools... Data types: Structured Text Data... Unstructured Text Data... Multimodal Data... Foundation Models

- **18-Multi-Agent_Architecture_Taxonomy_LLM (Chunk 3:264-266)**
  > LLM-powered agents possess the autonomy to interface with a diverse pool of contextual resources. They can discerningly select, integrate, and harness these resources

---

### 71. Autonomy-Alignment Balance Matrix

A nine-cell matrix categorizing LLM multi-agent systems by autonomy levels (static/adaptive/self-organizing) and alignment levels (integrated/user-guided/real-time), providing systematic architectural classification.

**Sources**:

- **18-Multi-Agent (Chunk 2:278-297)**
  > L2: Real-time: User-Supervised Automation / User-Collaborative Adaptation / User-Responsive Autonomy... L1: User-Guided... L0: Integrated: Rule-Driven Automation / Pre-Configured Adaptation / Bounded Autonomy

---

### 72. Slow Thinking via Multi-Agent Deliberation

Multi-agent architectures address LLM limitations in extended reasoning by distributing cognitive load across specialized agents, enabling deliberate 'slow thinking' through iterative collaboration and mutual feedback.

**Sources**:

- **18-Multi-Agent (Chunk 1:56-60)**
  > LLMs struggle with maintaining consistent logic across extended chains of reasoning. This deficiency hinders their ability to engage in a deliberate, in-depth, and iterative thought process (aka slow thinking)

---

### 73. Goal Decomposition Autonomy

LLM-powered agents autonomously decompose complex goals into manageable sub-tasks. This is a core generative AI pattern where the LLM reasons about task structure and generates a task decomposition strategy. Most systems achieve L2 (self-organizing) autonomy for decomposition.

**Sources**:

- **18-Multi-Agent_Architecture_Taxonomy_LLM (Chunk 3:118-124)**
  > Taxonomic aspects of Goal-driven Task Management comprise: Decomposition (how the goal or complex task is broken down into manageable sub-tasks)

---

### 74. Task Orchestration Pattern

Pattern for coordinating task distribution and result synthesis across multiple LLM agents. Includes decomposition, orchestration, and synthesis phases. Most current systems use predefined orchestration (L0) with autonomous execution.

**Sources**:

- **18-Multi-Agent_Architecture_Taxonomy_LLM (Chunk 3:122-123)**
  > Orchestration (how these tasks are distributed among the LLM-powered agents), and Synthesis (how the results of the tasks are finally combined)

---

### 75. Adaptive Prompt Engineering

Pattern where LLM agents adapt prompt templates during execution based on scenario requirements. Systems typically use predefined but adaptable prompt templates (L1 autonomy), allowing agents to modify prompts within a defined framework.

**Sources**:

- **18-Multi-Agent_Architecture_Taxonomy_LLM (Chunk 3:162-165)**
  > Prompt Engineering (how prompts are applied during collaboration and executing the actions), and Action Management (how the different kinds of action performed by the agents are managed)

---

### 76. Self-Organizing Collaboration Protocol

Pattern where LLM agents autonomously plan and execute collaboration strategies, self-organize communication protocols, negotiate action execution among the agent network. Represents L2 self-organizing autonomy in multi-agent collaboration.

**Sources**:

- **18-Multi-Agent_Architecture_Taxonomy_LLM (Chunk 3:189-193)**
  > Agents operating at this level showcase the capability to independently strategize their collaboration for task execution...LLM-powered agents can self-organize protocols for collaboration

---

### 77. Dynamic Role Definition

Pattern for dynamically defining and adapting agent roles during execution. Agents can modify or extend their competencies, roles, and relationships based on scenario requirements. Some systems achieve L2 autonomy for role definition.

**Sources**:

- **18-Multi-Agent_Architecture_Taxonomy_LLM (Chunk 3:204-208)**
  > Agent Generation (how the agents are created), Role Definition (how agents' roles are specified), Memory Usage (how agents utilize their memory), and Network Management

---

### 78. Central LLM Controller Pattern

Pattern where a single central LLM acts as controller to orchestrate multiple specialized foundation models. The LLM breaks down tasks, selects appropriate models, and coordinates execution through prompting. Achieves L2 autonomy for most aspects.

**Sources**:

- **18-Multi-Agent_Architecture_Taxonomy_LLM (Chunk 3:699-705)**
  > HUGGINGGPT follows a different strategy by leveraging the LLM as an autonomous controller that combines various multi-modal AI models to solve complex tasks

---

### 79. Role-Agent Collaboration Pattern

Pattern where multiple LLM agents take on dedicated roles with specific responsibilities and collaborate through dynamic exchange. Enables multi-perspective collaboration and domain simulation (e.g., software development project with different roles).

**Sources**:

- **18-Multi-Agent_Architecture_Taxonomy_LLM (Chunk 4:51-58)**
  > Role-Agent Systems employ an interplay or simulation between multiple dedicated roles agents. This collaboration can serve different purposes, such as simulating a discussion

---

### 80. Instructor-Executor Pattern

Multi-agent pattern where one agent (AI-user/instructor) provides directives and another agent (AI-assistant/executor) performs execution. Used in CAMEL and similar systems for structured task collaboration between LLM agents.

**Sources**:

- **18-Multi-Agent_Architecture_Taxonomy_LLM (Chunk 4:58-62)**
  > This collaboration is realized by communication protocols employing a dynamic exchange between agents with instructor and executor roles

---

### 81. Bounded Autonomy Pattern

Architectural pattern where LLM agents have high autonomy (L2) in certain aspects (decomposition, action execution, resource utilization) but are constrained by low-autonomy predefined mechanisms in other aspects, creating a balance between agency and control.

**Sources**:

- **18-Multi-Agent_Architecture_Taxonomy_LLM (Chunk 4:76-78)**
  > these high-autonomy aspects are mostly combined with low alignment levels, resulting in bounded autonomy aspects

---

### 82. Intertwined Dependencies Pattern

Pattern describing how autonomous LLM behaviors depend on predefined mechanisms as constraints. High-autonomy aspects are balanced by low-autonomy aspects that provide integrated alignment and control, ensuring accurate operation.

**Sources**:

- **18-Multi-Agent_Architecture_Taxonomy_LLM (Chunk 4:82-90)**
  > Autonomous decomposition directly depends on the user-prompted goal. Autonomous action management depends on strict or predefined communication protocol. Autonomous resource utilization depends on strict or predefined resource integration

---

### 83. Prompt-Driven Agent Communication

Pattern where multi-agent collaboration is achieved through sequences of prompts for task delegation, questioning, and result evaluation. Susceptible to errors and hallucinations, requiring robust control mechanisms for quality checking.

**Sources**:

- **18-Multi-Agent_Architecture_Taxonomy_LLM (Chunk 4:134-139)**
  > Collaboration between LLM-powered agents basically relies on prompt-driven message exchange, such as by delegating tasks, asking questions, or evaluating task results

---

### 84. Real-Time Responsive Alignment

Pattern for enabling dynamic realignment of LLM agents during runtime through interceptor mechanisms. Supports explainable AI, feedback loops, and human intervention. Key for hybrid teamwork between autonomous agents and human co-workers.

**Sources**:

- **18-Multi-Agent_Architecture_Taxonomy_LLM (Chunk 4:169-172)**
  > the interaction layer allows the integration of interceptor mechanisms. This not only allows real-time monitoring...but also to implement effective feedback and intervention options

---

### 85. Self-Reflection and Planning Pattern

Pattern where LLM agents evaluate their own outputs, engage in self-criticism, and adjust task prioritization based on intermediate results. Enables iterative improvement through autonomous reflection on execution outcomes.

**Sources**:

- **18-Multi-Agent_Architecture_Taxonomy_LLM (Chunk 3:647-654)**
  > the agent evaluates the intermediate results, engaging in self-criticism. The tasks are optionally re-prioritized. The final result represents an aggregate of all partial results

---

### 86. Graph of Thoughts (GoT)

Framework that advances prompting capabilities by modeling LLM reasoning as an arbitrary graph. Thoughts are vertices, edges are dependencies. Enables combining arbitrary thoughts into synergistic outcomes, distilling networks of thoughts, and enhancing thoughts using feedback loops.

**Sources**:

- **19-Graph_of_Thoughts_LLM_Reasoning (Chunk 1:17-28)**
  > The key idea and primary advantage of GoT is the ability to model the information generated by an LLM as an arbitrary graph, where units of information ('LLM thoughts') are vertices

---

### 87. Chain-of-Thought (CoT) Prompting

Foundational prompting pattern that includes intermediate reasoning steps in the prompt to improve LLM problem-solving. Significantly enhances mathematical, commonsense, and symbolic reasoning without model updates.

**Sources**:

- **19-Graph_of_Thoughts_LLM_Reasoning (Chunk 1:47-48)**
  > Chain-of-Thought (CoT) is an approach for prompting, in which one includes the intermediate steps of reasoning within the prompt (intermediate 'thoughts')

---

### 88. Self-Consistency with CoT (CoT-SC)

Extension of Chain-of-Thought that generates multiple independent reasoning chains and selects the best outcome. Offers opportunity to explore different reasoning paths but lacks local exploration within a path.

**Sources**:

- **19-Graph_of_Thoughts_LLM_Reasoning (Chunk 1:55-57)**
  > One major improvement over CoT, Self-Consistency with CoT (CoT-SC), is a scheme where multiple CoTs are generated, and then the best one is selected as the outcome

---

### 89. Tree of Thoughts (ToT)

Prompting paradigm that models LLM reasoning as a tree structure. Each node represents a partial solution. Enables thought generation, state evaluation, and search algorithms (BFS/DFS) for exploring reasoning paths with backtracking capability.

**Sources**:

- **19-Graph_of_Thoughts_LLM_Reasoning (Chunk 1:58-61)**
  > Tree of Thoughts (ToT) models the LLM reasoning process with a tree. This facilitates using different paths of thoughts, and offers novel capabilities such as backtracking

---

### 90. Thought Aggregation Transformation

Graph-enabled transformation that merges multiple LLM thoughts into synergistic new thoughts. Creates vertices with multiple incoming edges to aggregate reasoning paths. Enables combining most promising partial solutions while eliminating weaknesses.

**Sources**:

- **19-Graph_of_Thoughts_LLM_Reasoning (Chunk 1:344-352)**
  > with GoT, one can aggregate arbitrary thoughts into new ones, to combine and reinforce the advantages of these thoughts, while eliminating their disadvantages

---

### 91. Thought Refining Transformation

Transformation pattern where an LLM thought is iteratively refined through self-loops in the reasoning graph. Enables improvement of thoughts through repeated modification while maintaining the same thought connections.

**Sources**:

- **19-Graph_of_Thoughts_LLM_Reasoning (Chunk 1:355-357)**
  > refining of a current thought v by modifying its content: V+ = {} and E+ = {(v, v)}. This loop in the graph indicates an iterated thought

---

### 92. Thought Generation Transformation

Transformation that generates k new thoughts from an existing thought. Foundation for branching in reasoning graphs. Creates multiple candidate solutions from a single state for parallel exploration and selection.

**Sources**:

- **19-Graph_of_Thoughts_LLM_Reasoning (Chunk 1:360-364)**
  > one can generate one or more new thoughts based on an existing single thought v. This class embraces analogous reasoning steps from earlier schemes, such as ToT or CoT-SC

---

### 93. Graph of Operations (GoO)

Static execution plan that prescribes the sequence of thought transformations (Generate, Aggregate, Score, KeepBest) to be applied for solving a task. Defines the graph decomposition strategy before execution.

**Sources**:

- **19-Graph_of_Thoughts_LLM_Reasoning (Chunk 1:390-393)**
  > the Graph of Operations (GoO)...is a static structure that specifies the graph decomposition of a given task, i.e., it prescribes transformations to be applied to LLM thoughts

---

### 94. Graph Reasoning State (GRS)

Dynamic data structure that tracks the evolving state of LLM reasoning during execution. Maintains thought history, validity scores, and other relevant information for controlling the reasoning process.

**Sources**:

- **19-Graph_of_Thoughts_LLM_Reasoning (Chunk 1:394-395)**
  > GRS is a dynamic structure that maintains the state of the ongoing LLM reasoning process (the history of its thoughts and their states)

---

### 95. Thought Scoring Pattern

Merged from 2 sources. Pattern for evaluating LLM thoughts to determine solution quality. Scoring can be done by the LLM itself, by human evaluators, or by local scoring functions. Enables selection of best thoughts for further processing.

**Sources**:

- **19-Graph_of_Thoughts_LLM_Reasoning (Chunk 1:370-378)**
  > Thoughts are scored to understand whether the current solution is good enough. A score is modeled as a general function E(v, G, p_theta)

- **19-Graph_of_Thoughts_LLM_Reasoning (Chunk 1:373-374)**
  > GoT can also rank thoughts. We model this with a function R(G, p_theta, h) where h specifies the number of highest-ranking thoughts in G to be returned

---

### 96. Decompose-Solve-Merge Pattern

Task decomposition pattern where complex problems are split into smaller subtasks, solved individually, and merged. Analogous to divide-and-conquer algorithms. Particularly effective for sorting, set operations, and document merging.

**Sources**:

- **19-Graph_of_Thoughts_LLM_Reasoning (Chunk 1:477-478)**
  > First, one decomposes the input sequence of numbers into subarrays. Then, one sorts these subarrays individually, and then respectively merges them into a final solution

---

### 97. Volume of Thought Metric

Novel metric for evaluating prompting strategies. Measures how many preceding thoughts could have influenced a given thought. GoT achieves high volume (N) with low latency (log_k N), superior to CoT, CoT-SC, and ToT.

**Sources**:

- **19-Graph_of_Thoughts_LLM_Reasoning (Chunk 1:129-133)**
  > the volume of v is the number of LLM thoughts, from which one can reach v using directed edges. Intuitively, these are all the LLM thoughts that have had the potential to contribute to v

---

### 98. Latency-Volume Tradeoff

Fundamental tradeoff in prompting schemes between latency (hops to reach final thought) and volume (information scope). GoT uniquely achieves optimal tradeoff through thought aggregation, combining low latency with high information volume.

**Sources**:

- **19-Graph_of_Thoughts_LLM_Reasoning (Chunk 1:743-754)**
  > GoT is the only scheme to come with both a low latency of log_k N and a high volume N. This is enabled by the fact that GoT harnesses aggregations of thoughts

---

### 99. Multiple Response Generation with Selection

Pattern of generating k parallel responses at each step and selecting best outcomes. Key parameter in ToT and GoT for balancing exploration breadth vs. computational cost. More responses typically improve quality but increase expense.

**Sources**:

- **19-Graph_of_Thoughts_LLM_Reasoning (Chunk 1:780-788)**
  > We experiment extensively with the branching factor k and the number of levels L to ensure that we compare GoT to cost-effective and advantageous configurations

---

### 100. Few-Shot Prompt Engineering

Pattern of using templated prompts with few-shot examples that are dynamically populated at runtime. Enables consistent prompt structure while adapting to specific inputs. Examples demonstrate expected format and reasoning approach.

**Sources**:

- **19-Graph_of_Thoughts_LLM_Reasoning (Chunk 3:576-580)**
  > First, we present the prompt stubs (Table 3), serving as templates to dynamically generate appropriate prompts at runtime. For clarity, we display their corresponding few-shot examples separately

---

### 101. Structured Output Formatting

Pattern of constraining LLM output to specific JSON/structured format. Prompts explicitly specify output schema and prohibit additional text. Enables reliable parsing and processing of LLM responses.

**Sources**:

- **19-Graph_of_Thoughts_LLM_Reasoning (Chunk 3:603-616)**
  > Only output the final 2 lists in the following format without any additional text or thoughts!: {{ 'List 1': [...], 'List 2': [...] }}

---

### 102. Step-by-Step Approach Specification

Pattern of including explicit algorithmic steps in prompts to guide LLM reasoning. Specifies procedural approach for task completion. Improves reliability by providing structured methodology rather than open-ended instructions.

**Sources**:

- **19-Graph_of_Thoughts_LLM_Reasoning (Chunk 3:633-647)**
  > <Approach> To fix the incorrectly sorted list follow these steps: 1. For each number from 0 to 9, compare the frequency... 2. Iterate through the incorrectly sorted list...

---

### 103. Error Correction Prompting

Pattern for iterative improvement where LLM is given incorrect output and asked to fix it. Used in improve/refine operations. Leverages LLM ability to compare and correct errors against ground truth or constraints.

**Sources**:

- **19-Graph_of_Thoughts_LLM_Reasoning (Chunk 3:627-631)**
  > The following two lists represent an unsorted list of numbers and a sorted variant of that list. The sorted variant is not correct. Fix the sorted variant so that it is correct

---

### 104. Document Aggregation Pattern

Multi-step pattern for merging multiple documents using LLM. Combines generation, scoring, aggregation, and improvement operations. Goal is maximizing information retention while minimizing redundancy.

**Sources**:

- **19-Graph_of_Thoughts_LLM_Reasoning (Chunk 5:599-608)**
  > For document merging, we employ four distinct types of operations: Generate (merge 4 NDAs into 1), Score (score merged NDA), Aggregate (aggregate multiple merge attempts into one), Improve

---

### 105. LLM Self-Scoring Pattern

Pattern where LLM evaluates its own outputs on specified criteria. Provides structured scoring rubric (0-10 scale) with clear definitions. Enables automated quality assessment for thought selection and comparison.

**Sources**:

- **19-Graph_of_Thoughts_LLM_Reasoning (Chunk 6:519-528)**
  > Please score the merged NDA in terms of how much redundant information is contained...as well as how much information is retained from the original NDAs. A score of 10 for redundancy implies...

---

### 106. Reflection Pattern

A core agentic pattern where agents incorporate self-feedback mechanisms to identify and address errors, inconsistencies, and areas for improvement. Involves prompting an agent to critique its outputs for correctness, style, and efficiency, then incorporating this feedback into subsequent iterations. External tools like unit tests or web searches can validate results. In multi-agent systems, distinct roles can be assigned where one agent generates outputs while another critiques them.

**Sources**:

- **20-Agentic_RAG_Survey (Chunk 1:512-531)**
  > Reflection is a foundational design pattern in agentic workflows, enabling agents to iteratively evaluate and refine their outputs

---

### 107. Planning Pattern

An agentic pattern essential for multi-hop reasoning and iterative problem-solving in dynamic and uncertain scenarios. Agents dynamically determine the sequence of steps needed to accomplish a larger objective. This adaptability allows agents to handle tasks that cannot be predefined. While powerful, Planning can produce less predictable outcomes compared to deterministic workflows like Reflection.

**Sources**:

- **20-Agentic_RAG_Survey (Chunk 1:537-549)**
  > Planning is a key design pattern in agentic workflows that enables agents to autonomously decompose complex tasks into smaller, manageable subtasks

---

### 108. Tool Use Pattern

A pattern allowing agents to gather information, perform computations, and manipulate data beyond their pre-trained knowledge. Includes information retrieval, computational reasoning, and interfacing with external systems. Has evolved significantly with advancements like GPT-4's function calling capabilities. Techniques inspired by RAG, such as heuristic-based selection, address challenges in optimizing tool selection when many options are available.

**Sources**:

- **20-Agentic_RAG_Survey (Chunk 1:552-569)**
  > Tool Use enables agents to extend their capabilities by interacting with external tools, APIs, or computational resources

---

### 109. Multi-Agent Collaboration Pattern

A design pattern where agents communicate and share intermediate results while maintaining workflow efficiency and coherence. Distributes subtasks among specialized agents to improve scalability and adaptability. Each agent operates with its own memory and workflow, which can include the use of tools, reflection, or planning. Frameworks such as AutoGen, Crew AI, and LangGraph provide implementations for multi-agent solutions.

**Sources**:

- **20-Agentic_RAG_Survey (Chunk 1:572-597)**
  > Multi-agent collaboration is a key design pattern in agentic workflows that enables task specialization and parallel processing

---

### 110. Prompt Chaining

An agentic workflow pattern that improves accuracy by simplifying each subtask before moving forward. Most effective when a task can be broken down into fixed subtasks, each contributing to the final output. Particularly useful in scenarios where step-by-step reasoning enhances accuracy. May increase latency due to sequential processing. Example applications include generating marketing content and translating it, or structuring document creation through outline-verify-develop phases.

**Sources**:

- **20-Agentic_RAG_Survey (Chunk 1:620-642)**
  > Prompt chaining decomposes a complex task into multiple steps, where each step builds upon the previous one

---

### 111. Routing Pattern

An agentic workflow pattern ensuring distinct queries or tasks are handled separately, improving efficiency and response quality. Ideal for scenarios where different types of input require distinct handling strategies. Example applications include directing customer service queries into categories (technical support, refund requests, general inquiries) or assigning simple queries to smaller models for cost efficiency while routing complex requests to advanced models.

**Sources**:

- **20-Agentic_RAG_Survey (Chunk 1:644-668)**
  > Routing involves classifying an input and directing it to an appropriate specialized prompt or process

---

### 112. Parallelization Pattern

An agentic workflow pattern that can be categorized into sectioning (independent subtasks) and voting (multiple outputs for accuracy). Useful when tasks can be executed independently to enhance speed or when multiple outputs improve confidence. Example applications include splitting tasks like content moderation (one model screens input while another generates response) or using multiple models to cross-check code for vulnerabilities.

**Sources**:

- **20-Agentic_RAG_Survey (Chunk 1:671-694)**
  > Parallelization divides a task into independent processes that run simultaneously, reducing latency and improving throughput

---

### 113. Orchestrator-Workers Pattern

An agentic workflow pattern where unlike parallelization, it adapts to varying input complexity. Best suited for tasks requiring dynamic decomposition and real-time adaptation, where subtasks are not predefined. Example applications include automatically modifying multiple files in a codebase based on the nature of requested changes, or conducting real-time research by gathering and synthesizing relevant information from multiple sources.

**Sources**:

- **20-Agentic_RAG_Survey (Chunk 1:696-719)**
  > This workflow features a central orchestrator model that dynamically breaks tasks into subtasks, assigns them to specialized worker models, and compiles the results

---

### 114. Evaluator-Optimizer Pattern

An agentic workflow pattern effective when iterative refinement significantly enhances response quality, especially when clear evaluation criteria exist. Example applications include improving literary translations through multiple evaluation and refinement cycles, or conducting multi-round research queries where additional iterations refine search results.

**Sources**:

- **20-Agentic_RAG_Survey (Chunk 1:721-741)**
  > The evaluator-optimizer workflow iteratively improves content by generating an initial output and refining it based on feedback from an evaluation model

---

### 115. Single-Agent Router Architecture

An architecture that simplifies the system by consolidating retrieval, routing, and integration tasks into one unified agent. Particularly effective for setups with limited number of tools or data sources. The coordinating agent evaluates queries and selects from retrieval options including structured databases (Text-to-SQL), semantic search, web search, and recommendation systems. Features centralized simplicity, efficiency, resource optimization, dynamic routing, and versatility across tools.

**Sources**:

- **20-Agentic_RAG_Survey (Chunk 1:752-827)**
  > A Single-Agent Agentic RAG serves as a centralized decision-making system where a single agent manages the retrieval, routing, and integration of information

---

### 116. Multi-Agent RAG Architecture

A modular architecture that distributes responsibilities across multiple specialized agents instead of relying on a single agent. A coordinator agent delegates queries to specialized retrieval agents based on requirements. Features modularity (seamless addition/removal of agents), scalability (parallel processing), task specialization, and efficiency. Challenges include coordination complexity, computational overhead, and data integration from diverse sources.

**Sources**:

- **20-Agentic_RAG_Survey (Chunk 2:1-99)**
  > Multi-Agent RAG represents a modular and scalable evolution of single-agent architectures, designed to handle complex workflows and diverse query types

---

### 117. Hierarchical Agentic RAG

An architecture where agents are organized in a hierarchy with higher-level agents overseeing and directing lower-level agents. Top-tier agents evaluate query complexity and prioritize data sources. Enables multi-level decision-making, strategic prioritization, and scalability for complex multi-faceted queries. Challenges include coordination complexity across multiple levels and efficient resource allocation to avoid bottlenecks.

**Sources**:

- **20-Agentic_RAG_Survey (Chunk 2:100-188)**
  > Hierarchical Agentic RAG systems employ a structured, multi-tiered approach to information retrieval and processing, enhancing both efficiency and strategic decision-making

---

### 118. Corrective RAG Pattern

A pattern embedding intelligent agents for iterative refinement of context documents and responses. Core principle lies in ability to evaluate retrieved documents dynamically, perform corrective actions, and refine queries. Built on five key agents: Context Retrieval Agent, Relevance Evaluation Agent, Query Refinement Agent, External Knowledge Retrieval Agent, and Response Synthesis Agent. Features iterative correction, dynamic adaptability, agentic modularity, and factuality assurance.

**Sources**:

- **20-Agentic_RAG_Survey (Chunk 2:190-312)**
  > Corrective RAG introduces mechanisms to self-correct retrieval results, enhancing document utilization and improving response generation quality

---

### 119. Adaptive RAG Pattern

A pattern employing a classifier to assess query complexity and determine the most appropriate approach, ranging from single-step retrieval to multi-step reasoning, or bypassing retrieval altogether. For straightforward queries, generates answers using pre-existing knowledge. For simple queries, performs single-step retrieval. For complex queries, employs multi-step retrieval with progressive refinement. Features dynamic adaptability, resource efficiency, enhanced accuracy through iterative refinement, and flexibility for domain-specific extensions.

**Sources**:

- **20-Agentic_RAG_Survey (Chunk 2:314-441)**
  > Adaptive Retrieval-Augmented Generation (Adaptive RAG) enhances the flexibility and efficiency of large language models by dynamically adjusting query handling strategies

---

### 120. Agent-G Graph RAG Framework

An agentic framework combining structured and unstructured data sources for improved reasoning and retrieval accuracy. Employs modular retriever banks, dynamic agent interaction, and feedback loops. Core components: Retriever Bank (modular agents for graph/unstructured data), Critic Module (validates relevance and quality), Dynamic Agent Interaction (task-specific collaboration), and LLM Integration (synthesizes validated data). Features enhanced reasoning, dynamic adaptability, improved accuracy, and scalable modularity.

**Sources**:

- **20-Agentic_RAG_Survey (Chunk 2:443-581)**
  > Agent-G introduces a novel agentic architecture that integrates graph knowledge bases with unstructured document retrieval

---

### 121. GeAR Graph-Enhanced Agent Framework

A framework advancing RAG through Graph Expansion (enhances base retrievers by expanding to include graph-structured data) and Agent Framework (agent-based architecture for dynamic, autonomous decision-making in retrieval). Graph Expansion Module integrates graph-based data, allowing system to consider entity relationships during retrieval. Agent-Based Retrieval enables dynamic selection and combination of retrieval strategies. Features enhanced multi-hop retrieval, agentic decision-making, improved accuracy, and scalability.

**Sources**:

- **20-Agentic_RAG_Survey (Chunk 2:583-699)**
  > GeAR introduces an agentic framework that enhances traditional Retrieval-Augmented Generation (RAG) systems by incorporating graph-based retrieval mechanisms

---

### 122. Agentic Document Workflows (ADW)

A pattern orchestrating complex document-centric processes, integrating document parsing, retrieval, reasoning, and structured outputs with intelligent agents. Addresses limitations of Intelligent Document Processing (IDP) and RAG by maintaining state, coordinating multi-step workflows, and applying domain-specific logic. Workflow: Document Parsing/Structuring, State Maintenance, Knowledge Retrieval, Agentic Orchestration, Actionable Output Generation. Features state maintenance, multi-step orchestration, domain-specific intelligence, scalability, and enhanced productivity.

**Sources**:

- **20-Agentic_RAG_Survey (Chunk 2:701-803)**
  > Agentic Document Workflows (ADW) extend traditional Retrieval-Augmented Generation (RAG) paradigms by enabling end-to-end knowledge work automation

---

### 123. Real-Time Adaptability in Agentic Systems

A key benefit of agentic RAG systems enabling dynamic integration of evolving data in real-time applications. Customer support systems can incorporate live service outages, pricing updates, or other changing information into responses without requiring system reconfiguration. This enables personalized, context-aware replies that enhance user engagement.

**Sources**:

- **20-Agentic_RAG_Survey (Chunk 3:14-21)**
  > Real-Time Adaptability: Dynamically integrates evolving data, such as live service outages or pricing updates

---

### 124. Patient-Specific Data Integration Pattern

A healthcare application pattern where agentic RAG integrates electronic health records (EHR) and up-to-date medical literature to generate comprehensive summaries for clinicians. Enables personalized care tailored to individual patient needs, time efficiency through streamlined retrieval of relevant research, and accuracy through recommendations based on latest evidence and patient-specific parameters.

**Sources**:

- **20-Agentic_RAG_Survey (Chunk 3:24-46)**
  > Agentic RAG systems enable this by retrieving real-time clinical guidelines, medical literature, and patient history to assist clinicians

---

### 125. Legal Contract Analysis Pattern

An application pattern combining semantic search capabilities with legal knowledge graphs to automate contract review. Automatically flags clauses that deviate from standard terms, reduces time spent on contract review processes, and handles large volumes of contracts simultaneously. Ensures compliance and mitigates risks through automated analysis.

**Sources**:

- **20-Agentic_RAG_Survey (Chunk 3:49-71)**
  > A legal agentic RAG system can analyze contracts, extract critical clauses, and identify potential risks

---

### 126. Financial Risk Analysis with Multi-Step Reasoning

A finance application pattern for investment decisions, market analysis, and risk management. Delivers real-time analytics based on live market data, identifies potential risks using predictive analysis and multi-step reasoning, and combines historical and live data for comprehensive strategies. In auto insurance, can automate claim processing by retrieving policy details and combining with accident data.

**Sources**:

- **20-Agentic_RAG_Survey (Chunk 3:74-98)**
  > These systems integrate live data streams, historical trends, and predictive modeling to generate actionable outputs

---

### 127. Adaptive Learning Pattern

An education application pattern where agentic RAG assists researchers by synthesizing key findings from multiple sources. Provides tailored learning paths adapted to individual student needs and performance levels, engaging interactions with interactive explanations and personalized feedback, and scalability supporting large-scale deployments for diverse educational environments.

**Sources**:

- **20-Agentic_RAG_Survey (Chunk 3:101-121)**
  > These systems enable adaptive learning by generating explanations, study materials, and feedback tailored to the learner's progress and preferences

---

### 128. Graph-Enhanced Multimodal Workflows

A pattern combining graph structures with retrieval for workflows requiring interconnected data sources. Enables synthesis of text, images, and videos for marketing campaigns. Features multi-modal capabilities integrating text, image, and video data; enhanced creativity generating innovative ideas and solutions; and dynamic adaptability to evolving market trends and customer needs.

**Sources**:

- **20-Agentic_RAG_Survey (Chunk 3:124-150)**
  > Graph-Enhanced Agentic RAG (GEAR) combines graph structures with retrieval mechanisms, making it particularly effective in multimodal workflows

---

### 129. LangGraph Workflow Orchestration

A framework providing modular components for building RAG pipelines with graph-based workflows. Enables sophisticated orchestration and self-correction mechanisms in agentic systems. Supports loops for iterative processing, state persistence for maintaining context across steps, and human-in-the-loop interactions for validation and oversight.

**Sources**:

- **20-Agentic_RAG_Survey (Chunk 3:164-167)**
  > LangGraph complements this by introducing graph-based workflows that support loops, state persistence, and human-in-the-loop interactions

---

### 130. Meta-Agent Document Architecture

LlamaIndex's Agentic Document Workflows (ADW) pattern enabling end-to-end automation of document processing, retrieval, and structured reasoning. Sub-agents manage smaller document sets and coordinate through a top-level agent for complex tasks like compliance analysis and contextual understanding.

**Sources**:

- **20-Agentic_RAG_Survey (Chunk 3:169-172)**
  > It introduces a meta-agent architecture where sub-agents manage smaller document sets, coordinating through a top-level agent for tasks such as compliance analysis

---

### 131. Adaptive Vector Search

A retrieval pattern where agents dynamically switch between sparse and dense vector methods to optimize performance. Combined with Hugging Face pre-trained models for embedding and generation tasks, enables flexible, context-aware retrieval optimization.

**Sources**:

- **20-Agentic_RAG_Survey (Chunk 3:174-176)**
  > Qdrant enhances retrieval workflows with adaptive vector search capabilities, allowing agents to optimize performance by dynamically switching between sparse and dense vector methods

---

### 132. Multi-Agent Orchestration Frameworks

Frameworks emphasizing multi-agent architectures. CrewAI supports hierarchical and sequential processes with robust memory systems and tool integrations. AG2 (formerly AutoGen) excels in multi-agent collaboration with advanced support for code generation, tool execution, and decision-making. OpenAI Swarm provides educational, lightweight multi-agent orchestration emphasizing agent autonomy and structured collaboration.

**Sources**:

- **20-Agentic_RAG_Survey (Chunk 3:182-189)**
  > CrewAI supports hierarchical and sequential processes, robust memory systems, and tool integrations. AG2 excels in multi-agent collaboration with advanced support for code generation, tool execution, and decision-making

---

### 133. Semantic Kernel Agentic Patterns

Microsoft's open-source SDK integrating LLMs into applications with support for agentic patterns. Enables creation of autonomous AI agents for natural language understanding, task automation, and decision-making. Used in scenarios like ServiceNow's P1 incident management to facilitate real-time collaboration, automate task execution, and retrieve contextual information seamlessly.

**Sources**:

- **20-Agentic_RAG_Survey (Chunk 3:198-203)**
  > Semantic Kernel is an open-source SDK by Microsoft that integrates large language models (LLMs) into applications. It supports agentic patterns, enabling the creation of autonomous AI agents

---

### 134. Zero-Shot Prompting

An LLM prompting pattern where models complete tasks based solely on instructions without prior examples. Demonstrates that LLMs can perform complex tasks beyond language understanding and generation, including analyzing and creating business process models and smart contracts, without task-specific training.

**Sources**:

- **21-LLM_Smart_Contracts_from_BPMN (Chunk 1:145-146)**
  > In zero-shot prompting, models complete tasks based solely on instructions without prior examples

---

### 135. Few-Shot Prompting

An LLM prompting pattern providing illustrative examples within the input. Augmenting the generation process by a formalized model improves results in smart contract generation. Studies show that moving from zero-shot to one-shot and two-shot prompts can improve performance, though not consistently.

**Sources**:

- **21-LLM_Smart_Contracts_from_BPMN (Chunk 1:146-147)**
  > few-shot prompting involves providing a handful of illustrative examples directly within the input

---

### 136. LLM-Driven Code Generation from Process Models

A pattern using LLMs for model-driven engineering where process descriptions are transformed into executable artifacts. LLM-based approaches outperform traditional rule-based approaches in code-to-code translation. Applied to blockchain-based business process execution where BPMN choreographies are transformed into smart contracts. Challenges include non-determinism, hallucination, security vulnerabilities, and biases.

**Sources**:

- **21-LLM_Smart_Contracts_from_BPMN (Chunk 1:54-61)**
  > LLMs are similarly prospected to have the potential to drive automation. This hope can draw on seminal results from the related field of code-to-code translation (transpilers)

---

### 137. LLM Temperature Control for Determinism

A configuration pattern controlling LLM output randomness. Lower temperatures select most probable tokens for predictable, focused outputs. Higher temperatures select less probable tokens for creative, varied responses. For smart contract generation requiring reliability, temperature is set to 0 for quasi-deterministic inference results, though tie-breaking and floating point variability may still cause stochasticity.

**Sources**:

- **21-LLM_Smart_Contracts_from_BPMN (Chunk 1:171-174)**
  > Temperature is a setting for LLMs that controls the randomness of generated text; lower temperatures make outputs more predictable and focused

---

### 138. Automated Evaluation Framework for LLM Code Generation

A pattern for systematically evaluating LLM-generated code through automated testing. Replays all possible conforming traces (which the smart contract must accept) and non-conforming traces (which it must reject). Framework components include test runner, simulator (generates conforming/non-conforming traces), LLM provider interface, log replayer, and blockchain environment. Enables repeatable benchmarks as LLM capabilities evolve rapidly.

**Sources**:

- **21-LLM_Smart_Contracts_from_BPMN (Chunk 1:229-241)**
  > To assess the capabilities of LLMs for smart contract generation, we designed a configurable benchmarking framework

---

### 139. LLM Integration with Verification Pipelines

A responsible integration pattern for high-security contexts like smart contracts. LLMs propose code snippets checked against formal specifications or verified using automated theorem provers. LLMs also generate test cases or identify potential vulnerabilities, augmenting existing verification processes. Combines reliability of traditional code generation tools with flexibility and natural language understanding of LLMs.

**Sources**:

- **21-LLM_Smart_Contracts_from_BPMN (Chunk 1:650-659)**
  > LLM integration must rely on extensive evaluation and robust verification of generated outcomes. This could involve using LLMs to propose code snippets or modifications, which are then rigorously checked

---

