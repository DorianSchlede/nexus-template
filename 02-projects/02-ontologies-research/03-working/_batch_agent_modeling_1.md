---
batch_id: 1
field: agent_modeling
papers_read: [02-Knowledge_Graphs, 04-PROV-O_to_BFO_Semantic_Mapping, 05-DOLCE_Descriptive_Ontology, 15-SciAgents_Multi-Agent_Graph_Reasoning, 16-KG-Agent_Knowledge_Graph_Reasoning]
chunks_read: 9
patterns_found: 18
extracted_at: "2025-12-28T03:15:00Z"
---

# Batch Extraction: agent_modeling (Batch 1)

## Patterns Extracted

### Pattern: PROV Agent as Material Entity with Role and Participation

- **Source**: 04-PROV-O_to_BFO_Semantic_Mapping (Chunk 1:Line 654-662)
- **Description**: PROV Agent is modeled as a subclass of BFO material entities that both participate in some PROV Activity and bear some BFO role that is realized in a PROV Activity. This captures the ontological nature of agents as material entities with responsibilities realized through roles.
- **Quote**: "PROV Agent is mapped as a subclass of BFO material entities that both participate in some PROV Activity and bear some BFO role that is realized in a PROV Activity. The reason for this mapping is that a PROV Agent always has some matter as a part that persists in time."
- **Context**: This is part of the semantic mapping between PROV-O and BFO ontologies, establishing how agents are formally classified in foundational ontology terms.

### Pattern: Agent Responsibility Through Role Realization

- **Source**: 04-PROV-O_to_BFO_Semantic_Mapping (Chunk 1:Line 659-666)
- **Description**: Agents bear responsibility for activities through roles that are realized in those activities. This models the intentional/responsibility aspect of agents through BFO role theory.
- **Quote**: "The definition of PROV Agent also states that an agent 'bears some form of responsibility for an activity taking place, for the existence of an entity, or another agent's activity'. This is formalized in axioms which entail that every PROV Agent participates in, and bears some role that is realized in, some PROV Activity."
- **Context**: Explaining why PROV Agent requires both participation and role-bearing in the BFO mapping.

### Pattern: CCO Agent Equivalence with PROV Agent

- **Source**: 04-PROV-O_to_BFO_Semantic_Mapping (Chunk 1:Line 676-679)
- **Description**: A more specific equivalence mapping where PROV Agent is equivalent to the intersection of CCO agents that are a CCO agent in some PROV Activity.
- **Quote**: "A PROV Agent is equivalent to the intersection of CCO agents that are a CCO agent in some PROV Activity."
- **Context**: Providing a more specific CCO mapping for BFO users who also use CCO.

### Pattern: Software Agent as Material Realization

- **Source**: 04-PROV-O_to_BFO_Semantic_Mapping (Chunk 1:Line 657-659)
- **Description**: Even software agents are modeled as having material basis, since every particular instance of a PROV SoftwareAgent is a material realization of some software.
- **Quote**: "This is true even for instances of its subclass, PROV SoftwareAgent, which is defined as 'running software', because every particular instance of a PROV SoftwareAgent is a material realization of some software (which may itself be considered a generically dependent continuant)."
- **Context**: Clarifying how software agents fit within the material entity classification.

### Pattern: Agent vs Activity Disjointness

- **Source**: 04-PROV-O_to_BFO_Semantic_Mapping (Chunk 1:Line 694-721)
- **Description**: The mapping enforces that agents and activities are disjoint (agents are continuants, activities are occurrents), which contradicts PROV-O's allowance for agents to be activities but provides cleaner ontological foundations.
- **Quote**: "Mapping PROV Agent to BFO continuant and PROV Activity to BFO process implies that PROV Agent is disjoint with PROV Activity. While this contradicts Requirement V14, it does not contradict any specific example provided in the essay or W3C documentation of something that is both a PROV Agent and PROV Activity."
- **Context**: Discussing the design decision to enforce the continuant/occurrent distinction for agents.

### Pattern: Person and Organization as Agent Intersections

- **Source**: 04-PROV-O_to_BFO_Semantic_Mapping (Chunk 1:Line 773-788)
- **Description**: PROV Person and PROV Organization are modeled as intersections of their CCO counterparts with PROV Agent, rather than simple equivalences, because CCO Person/Organization are not subclasses of CCO Agent.
- **Quote**: "We map PROV Person as equivalent to the intersection of CCO Person and PROV Agent. This entails that every PROV Person is both a CCO Person and PROV Agent. Conversely, anyone who is both a CCO Person and a PROV Agent is therefore a PROV Person."
- **Context**: Addressing lexical homonymy between PROV-O and CCO terms.

### Pattern: Agentive Physical Object (APO) in DOLCE

- **Source**: 05-DOLCE_Descriptive_Ontology (Chunk 2:Line 88, 106, 203, 233, 251)
- **Description**: DOLCE models agents as Agentive Physical Objects (APO), a category that represents physical objects with agency/intentionality. Persons are modeled as APO.
- **Quote**: "Person(x) -> APO(x)" and "The formulas above state that a person is an agentive physical object"
- **Context**: DOLCE taxonomy formalization for modeling events involving agents like walking or turning.

### Pattern: Agent Constant Participation in Events

- **Source**: 05-DOLCE_Descriptive_Ontology (Chunk 2:Line 145-150)
- **Description**: Agents are modeled with constant participation (PCC) in perdurants/events, indicating that the agent is present throughout the entire event.
- **Quote**: "e = e1 + e2 + e3 ^ PCC(p, e)" meaning "it states that p constantly participates in the perdurant e which is the sum of the perdurants e1, e2, e3"
- **Context**: Formalizing how agents relate to composite events in DOLCE.

### Pattern: Multi-Agent System with Specialized Roles

- **Source**: 15-SciAgents_Multi-Agent_Graph_Reasoning (Chunk 1:Line 117-130)
- **Description**: Agents are modeled with distinct specialized roles within a collaborative system. Each agent is assigned a specific function optimized through complex prompting strategies.
- **Quote**: "Each agent in the system is assigned a distinct role, optimized through complex prompting strategies to ensure that every subtask is tackled with targeted expertise and precision. This strategic division of labor allows the AI system to proficiently manage the complexities of scientific research, fostering effective collaboration among agents."
- **Context**: Describing the SciAgents multi-agent framework architecture.

### Pattern: Agent Roles in SciAgents Framework

- **Source**: 15-SciAgents_Multi-Agent_Graph_Reasoning (Chunk 1:Line 225-229)
- **Description**: Specific agent roles are defined including Ontologist, Scientist 1, Scientist 2, and Critic, each with specialized functions in the research hypothesis generation process.
- **Quote**: "Each agent plays a specialized role: The Ontologist defines key concepts and relationships, Scientist 1 crafts a detailed research proposal, Scientist 2 expands and refines the proposal, and the Critic agent conducts a thorough review and suggests improvements."
- **Context**: Describing the role-based agent architecture in the multi-agent system.

### Pattern: Autonomous Agent Decision Making

- **Source**: 15-SciAgents_Multi-Agent_Graph_Reasoning (Chunk 1:Line 186-191)
- **Description**: Agents can operate with pre-programmed interaction sequences OR as fully autonomous agents that self-organize without predetermined order.
- **Quote**: "In the first approach (Figure 1b), the interactions between agents are pre-programmed and follow a predefined sequence of tasks that ensure consistency and reliability in hypothesis generation. In contrast, the second approach features fully automated agent interactions without any predetermined order of how interactions between agents unfold, providing a more flexible and adaptive framework."
- **Context**: Comparing two different agent interaction paradigms.

### Pattern: Human-in-the-Loop Agent Interaction

- **Source**: 15-SciAgents_Multi-Agent_Graph_Reasoning (Chunk 1:Line 191-194)
- **Description**: The autonomous agent approach incorporates human-in-the-loop interactions, enabling human intervention at various stages.
- **Quote**: "This second strategy (Figure 1c) also incorporates human-in-the-loop interactions, enabling human intervention at various stages of research development. Such interventions allow for expert feedback, refinement of hypotheses, or strategic guidance."
- **Context**: Describing hybrid human-agent interaction models.

### Pattern: Swarm Intelligence Agent Model

- **Source**: 15-SciAgents_Multi-Agent_Graph_Reasoning (Chunk 1:Line 40-43)
- **Description**: Multi-agent systems are modeled as harnessing a "swarm of intelligence" similar to biological systems.
- **Quote**: "Our case studies demonstrate scalable capabilities to combine generative AI, ontological representations, and multi-agent modeling, harnessing a 'swarm of intelligence' similar to biological systems."
- **Context**: Describing the bio-inspired approach to multi-agent system design.

### Pattern: Agent Team Composition with Manager

- **Source**: 15-SciAgents_Multi-Agent_Graph_Reasoning (Chunk 4:Line 79-84, Chunk 7:Line 474-486)
- **Description**: Agents are organized into teams with specialized roles including a Group Chat Manager that coordinates by selecting speakers based on context and agent profiles.
- **Quote**: "ontologist: An ontologist who defines each of the terms and discusses the relationships in the path. scientist: A scientist who can craft the research proposal... critic_agent: Summarizes, critiques, and suggests improvements after all seven aspects of the proposal have been expanded by the agents."
- **Context**: Describing the full team composition in the autonomous multi-agent system.

### Pattern: KG-Agent as Autonomous LLM-Based Agent

- **Source**: 16-KG-Agent_Knowledge_Graph_Reasoning (Chunk 1:Line 23-29)
- **Description**: KG-Agent models an autonomous LLM-based agent that can actively make decisions during the reasoning process over knowledge graphs, integrating LLM, toolbox, executor, and memory.
- **Quote**: "we propose an autonomous LLM-based agent framework, called KG-Agent, which enables a small LLM to actively make decisions until finishing the reasoning process over KGs. In KG-Agent, we integrate the LLM, multifunctional toolbox, KG-based executor, and knowledge memory, and develop an iteration mechanism that autonomously selects the tool then updates the memory for reasoning over KG."
- **Context**: Introducing the KG-Agent framework architecture.

### Pattern: Agent Autonomy Without Human Assistance

- **Source**: 16-KG-Agent_Knowledge_Graph_Reasoning (Chunk 1:Line 85-89)
- **Description**: Agents are designed with true autonomy - able to make decisions during reasoning without human assistance, and can work with relatively small models.
- **Quote**: "The motivations are twofold: (1) designing autonomous reasoning approaches that can actively make decisions during reasoning, without human assistance; (2) enabling relatively small models (e.g., 7B LLM) to effectively perform complex reasoning, without reliance on close-sourced LLM APIs."
- **Context**: Stating the design goals for autonomous agent behavior.

### Pattern: Agent Planner with Tool Selection

- **Source**: 16-KG-Agent_Knowledge_Graph_Reasoning (Chunk 1:Line 537-565)
- **Description**: The agent contains a Planner component (the LLM) that selects tools from a toolbox to interact with the knowledge graph at each step. The planner addresses task requirements through tool invocation.
- **Quote**: "Based on the current knowledge memory, the LLM-based planner selects a tool to interact with KG at each step... Generally, the planner needs to invoke tools from the pre-defined toolbox to address four types of task requirements, i.e., linking the mentioned entity to KG, accessing the KG information, processing the intermediate results, or returning the final answer to end the reasoning process."
- **Context**: Describing the internal agent architecture with planner and tool selection.

### Pattern: Agent Memory for Context Maintenance

- **Source**: 16-KG-Agent_Knowledge_Graph_Reasoning (Chunk 1:Line 546-551)
- **Description**: Agents maintain a knowledge memory that preserves currently useful information including question, toolbox definition, current KG information, and history reasoning program.
- **Quote**: "The knowledge memory preserves the currently useful information to support the LLM-based planner for making decisions. It mainly contains four parts of information, i.e., natural language question, toolbox definition, current KG information, and history reasoning program."
- **Context**: Describing the agent's memory architecture for context maintenance during reasoning.

