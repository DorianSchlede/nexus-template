---
title: "Balancing Autonomy and Alignment: A Multi-Dimensional Taxonomy for Autonomous LLM-Powered Multi-Agent Architectures"
authors: ["Thorsten Haendler"]
year: 2023
source: "Ferdinand Porsche Mobile University of Applied Sciences (FERNFH)"
paper_type: "Taxonomy/Classification Framework"
extraction_version: "v2"
extraction_date: "2025-12-31"

# V2 DISCOVERY EXTRACTION

ontological_primitives:
  - term: "Agent"
    definition: "An intelligent component endowed with a unique set of competencies including a clearly defined role, individual memory, and access to contextual resources, with reasoning capabilities rooted in LLMs"
    source: "Chunk 1:467-474"
    unique_aspects: "Agents are defined primarily by their COMPETENCIES (role, memory, context access) rather than by intentionality or autonomy alone. The LLM provides the 'backbone' of reasoning."

  - term: "Action"
    definition: "A unit of work performed by an Agent, with sub-types including DecomposeTask, CreateTask, DelegateTask, ExecuteTask, EvaluateResult, MergeResult"
    source: "Chunk 2:35-49"
    unique_aspects: "Actions are TYPED and compositional - each Action can be part of another Action. This is unusual - most frameworks treat actions as atomic."

  - term: "Goal"
    definition: "A user-prompted directive, problem, question, or mission that undergoes decomposition into Tasks"
    source: "Chunk 1:853-854"
    unique_aspects: "Goals are explicitly USER-PROMPTED, not agent-generated. The framework assumes external goal-setting."

  - term: "Task"
    definition: "A manageable unit of work derived from Goal decomposition, interconnectable in different ways (sequential tasks, graph tasks)"
    source: "Chunk 1:854-856"
    unique_aspects: "Tasks can form GRAPHS, not just sequences. This enables non-linear execution paths."

  - term: "Context"
    definition: "External resources available to agents, categorized as Tools, Data, and Foundation Models"
    source: "Chunk 2:99-101"
    unique_aspects: "Context is explicitly TRIADIC (Tools/Data/Models) rather than a single category. Each has distinct sub-types."

  - term: "Role"
    definition: "A distinct functional identity assigned to or assumed by an Agent within a task-management activity"
    source: "Chunk 1:876, Chunk 2:14-17"
    unique_aspects: "Roles can be domain-specific (project manager, developer) or generic (task-creation agent, task-execution agent)"

  - term: "Autonomy"
    definition: "The extent to which an AI system can make decisions and act independently of rules and mechanisms defined by humans"
    source: "Chunk 2:303-307"
    unique_aspects: "Autonomy is explicitly DISTINGUISHED from automation - automation is task execution without input, autonomy is DECISION-MAKING without intervention"

  - term: "Alignment"
    definition: "Techniques ensuring the system's actions are in sync with human intentions and values, implementable at multiple levels and timings"
    source: "Chunk 1:500-506, Chunk 2:362-367"
    unique_aspects: "Alignment is decomposed into ORIGIN (architect vs user) and TIMING (pre-deployment, post-deployment pre-runtime, runtime)"

  - term: "Interaction Layer"
    definition: "The architectural layer providing workspace for multiple collaborating agents, managing both external context interaction and internal agent collaboration"
    source: "Chunk 1:74-79"
    unique_aspects: "This is a software architecture concept mapped onto MAS - unusual to see explicit layer abstraction"

  - term: "Communication Protocol"
    definition: "A structured framework and methodology for agents' collaboration, establishing rules and mechanisms for message exchanges"
    source: "Chunk 2:75-80"
    unique_aspects: "Three types identified: strict finite processes, dialogue cycles, multi-cycle process frameworks"

structural_patterns:
  - pattern_name: "Triadic Decision-Making Tension"
    structure: "Human Users <-> Rules/Mechanisms <-> LLM-Powered Agents"
    instances:
      - "The primary decision-making entities form a triangle of dynamic tensions (Fig. 3)"
      - "Alignment pulls toward Human/Rules, Autonomy pulls toward Agents"
      - "System Operation mediates between Rules and Agents"
    source: "Chunk 1:497-503, Chunk 1:529"
    significance: "This is the CORE structural insight - every design choice can be mapped to this triad"

  - pattern_name: "Three-Level Hierarchy (L0/L1/L2)"
    structure: "Static/Rule-Driven -> Adaptive/Predefined-Flexible -> Self-Organizing/Dynamic"
    instances:
      - "Autonomy Levels: L0 Static, L1 Adaptive, L2 Self-Organizing"
      - "Alignment Levels: L0 Integrated, L1 User-Guided, L2 Real-Time Responsive"
      - "Combined into 9-cell matrix (Table 1)"
    source: "Chunk 2:326-352, Chunk 2:409-432"
    significance: "Universal 3-level scale applied across all dimensions"

  - pattern_name: "Four Architectural Viewpoints (adapted from Kruchten 4+1)"
    structure: "Functional / Development / Process / Physical mapped to MAS concerns"
    instances:
      - "Functional -> Goal-driven Task Management"
      - "Development -> Agent Composition"
      - "Process -> Multi-Agent Collaboration"
      - "Physical -> Context Interaction"
    source: "Chunk 2:641-676"
    significance: "Software architecture viewpoints applied to MAS - unusual bridging"

  - pattern_name: "Task-Management Activity Triad"
    structure: "Decomposition -> Orchestration -> Synthesis"
    instances:
      - "Decomposition: Breaking down Goals into Tasks"
      - "Orchestration: Distributing Tasks among Agents"
      - "Synthesis: Combining Task Results into Total Result"
    source: "Chunk 1:860-868"
    significance: "This pattern recurs as the core 'function' of the system"

  - pattern_name: "Agent Type Triad"
    structure: "Task-Management Agents / Domain Role Agents / Technical Agents"
    instances:
      - "Task-Management: Task-Creation, Task-Prioritization, Task-Execution"
      - "Domain Role: Project Manager, Developer, QA Engineer"
      - "Technical: SQL Agent, Python Agent"
    source: "Chunk 1:902-921, Chunk 2:6-21"
    significance: "Three categories of agent function - generic vs domain vs technical"

  - pattern_name: "Availability-driven vs Requirements-driven Dependencies"
    structure: "Low-autonomy systems have capabilities determining needs; High-autonomy systems have needs determining capabilities"
    instances:
      - "Low-autonomy: Goal-driven TM 'relies on capabilities of' other viewpoints"
      - "High-autonomy: Goal-driven TM 'adapts capabilities to' other viewpoints"
    source: "Chunk 2:697-801"
    significance: "INVERSION of dependency direction based on autonomy level - crucial architectural insight"

novel_concepts:
  - concept: "Cross-Cutting Concerns of Autonomy and Alignment"
    definition: "Autonomy and alignment are not localized features but traverse components and mechanisms across the entirety of the system's architecture"
    novelty_claim: "Treating autonomy/alignment as cross-cutting concerns (borrowing from aspect-oriented programming) rather than single dimensions"
    source: "Chunk 1:533-537, Chunk 2:185-186"

  - concept: "Autonomy-Alignment Matrix"
    definition: "A 3x3 matrix combining levels of autonomy (Static/Adaptive/Self-Organizing) with levels of alignment (Integrated/User-Guided/Real-Time) yielding 9 configuration types"
    novelty_claim: "Treating autonomy and alignment as INDEPENDENT dimensions that combine multiplicatively, not as a single spectrum"
    source: "Chunk 2:270-297"

  - concept: "108 Single Configuration Options / 282 Billion Combinations"
    definition: "12 aspects x 9 autonomy-alignment combinations = 108 single options; 9^12 = ~282 billion total combined configurations"
    novelty_claim: "Explicit quantification of architectural design space complexity"
    source: "Chunk 3:101-111"

  - concept: "Intertwined Dependencies"
    definition: "Mixed autonomy levels across viewpoints/aspects create complex webs where some aspects are availability-driven and others requirements-driven"
    novelty_claim: "Explicit recognition that heterogeneous autonomy levels create emergent complexity"
    source: "Chunk 2:803-817"

  - concept: "Bounded Autonomy"
    definition: "High autonomy (L2) combined with low alignment (L0) - system can self-organize but within architect-defined constraints"
    novelty_claim: "A specific configuration option recognizing autonomous operation within fixed guardrails"
    source: "Chunk 2:580-584"

  - concept: "User-Responsive Autonomy"
    definition: "The highest level combination (L2/L2) where agents self-organize AND respond to real-time user adjustments"
    novelty_claim: "Defines the theoretical maximum of the framework"
    source: "Chunk 2:593-597"

  - concept: "Prompt Augmentation"
    definition: "The process of integrating additional specifics (role, memory, context information, templates) into agent prompts before LLM processing"
    novelty_claim: "Formalizes the engineering practice of prompt construction as an architectural concern"
    source: "Chunk 2:59-68"

  - concept: "Society of Mind as Architectural Metaphor"
    definition: "Minsky's theory applied to explain cognitive synergy of multiple 'mindless' agents solving complex tasks"
    novelty_claim: "Explicit invocation of Minsky's framework as theoretical foundation for LLM-MAS"
    source: "Chunk 1:69-71, Chunk 1:483-484"

semantic_commitments:
  - commitment: "User-Prompted Goal Origin"
    position: "Goals originate from human users, not from agents themselves"
    implications: "Framework cannot model proactive/self-motivated agents; assumes human-in-the-loop for goal-setting"
    source: "Chunk 1:853-854"

  - commitment: "Autonomy is Decision-Making Independence"
    position: "Autonomy refers to decisions about tasks, not task execution itself (which is automation)"
    implications: "Clear separation between DOING (automation) and DECIDING (autonomy)"
    source: "Chunk 2:313-316"

  - commitment: "Alignment as Complementary, Not Counter to Autonomy"
    position: "Alignment acts to complement and refine autonomy, applicable across various levels"
    implications: "Rejects the autonomy-vs-alignment tradeoff framing"
    source: "Chunk 2:368-370"

  - commitment: "Software Architecture as Primary Lens"
    position: "Multi-agent systems should be analyzed through software architecture frameworks (viewpoints, concerns, dependencies)"
    implications: "Bridges AI/MAS research with software engineering; may miss some AI-specific aspects"
    source: "Chunk 2:608-616"

  - commitment: "Pragmatic/Technical Perspective on AI Safety"
    position: "Alignment is operationalized as calibration of conditions tied to user-specified objectives, not philosophical value alignment"
    implications: "Sidesteps deep AI safety questions; focuses on practical user-goal alignment"
    source: "Chunk 2:364-367"

boundary_definitions:
  - entity_type: "Agent vs Component"
    identity_criteria: "An agent has: (1) LLM-powered reasoning, (2) defined role, (3) individual memory, (4) context access"
    boundary_cases: "Is a prompt template an agent? No - lacks reasoning. Is Wolfram Alpha an agent? No - it's a Tool."
    source: "Chunk 1:467-474"

  - entity_type: "Task vs Sub-Task"
    identity_criteria: "A Task is 'manageable' - can be assigned to an agent for execution. Sub-Tasks arise from Decomposition."
    boundary_cases: "When is a Task small enough? Paper leaves this to implementation."
    source: "Chunk 1:854-861"

  - entity_type: "Autonomy Level Boundaries"
    identity_criteria: "L0: predefined rules only; L1: predefined but adaptable framework; L2: self-organizing, no predefined constraints"
    boundary_cases: "A 'highly generic infrastructure modifiable by agents' is L2, not L1"
    source: "Chunk 2:346-351"

  - entity_type: "Action vs Activity"
    identity_criteria: "Actions are agent-level operations; Task-Management Activity is the system-level lifecycle containing actions"
    boundary_cases: "Multiple Actions can occur within one Activity; Activities contain the full Goal->Result cycle"
    source: "Chunk 1:857-868"

temporal_modeling:
  - aspect: "Activity Lifecycle Phases"
    approach: "Three-phase sequential process: Decomposition -> Orchestration -> Synthesis"
    mechanism: "Phases follow sequentially within a Task-Management Activity"
    source: "Chunk 1:857-868"

  - aspect: "Alignment Timing"
    approach: "Three temporal windows: pre-deployment, post-deployment pre-runtime, runtime"
    mechanism: "Alignment can be specified at different points relative to system execution"
    source: "Chunk 2:395-396"

  - aspect: "Iterative Refinement"
    approach: "Communication protocols may include feedback loops and multi-cycle processes"
    mechanism: "Dialogue cycles between agents; optional re-prioritization after task completion"
    source: "Chunk 2:82-92, Chunk 3:648-654"

  - aspect: "Memory Types"
    approach: "Short-term memory (context window) vs Long-term memory (vector databases)"
    mechanism: "Different temporal persistence; short-term for immediate context, long-term for accumulated experience"
    source: "Chunk 1:894-896"

  - aspect: "Real-Time Responsiveness"
    approach: "L2 alignment enables runtime adjustment via interceptors and monitoring"
    mechanism: "System can solicit user feedback at critical junctures during execution"
    source: "Chunk 2:427-432"

agency_spectrum:
  - agent_type: "Human User"
    capabilities: "Goal specification, preference setting, runtime feedback, goal adjustment"
    constraints: "Not part of the automated system; external to the interaction layer"
    source: "Chunk 1:848-853"

  - agent_type: "Task-Management Agent"
    capabilities: "Task creation, task prioritization, task execution orchestration"
    constraints: "Generic roles; may lack domain expertise"
    source: "Chunk 1:902-912"

  - agent_type: "Domain Role Agent"
    capabilities: "Domain-specific expertise; specialized collaboration with peer role agents"
    constraints: "Bound to specific application domain"
    source: "Chunk 1:914-917, Chunk 2:14-17"

  - agent_type: "Technical Agent"
    capabilities: "Interfacing with technical platforms, development tools, databases"
    constraints: "Limited to technical operations"
    source: "Chunk 1:919-921, Chunk 2:19-21"

  - agent_type: "Central LLM Controller"
    capabilities: "Autonomous model selection, task planning, resource coordination (as in HuggingGPT)"
    constraints: "Single agent architecture; no multi-agent collaboration"
    source: "Chunk 3:699-717, Chunk 4:39-49"

  - agent_type: "System Architect"
    capabilities: "Defines interaction layer, integrates alignment techniques, specifies rules and mechanisms"
    constraints: "Pre-deployment influence only; cannot adjust at runtime"
    source: "Chunk 2:187-188"

knowledge_representation:
  - mechanism: "Domain Ontology Model"
    formalism: "UML 2 Class Diagram representing conceptual model"
    reasoning: "No formal reasoning; serves human understanding of domain concepts"
    source: "Chunk 1:795-819"

  - mechanism: "Agent Memory"
    formalism: "Multiple formats: textual records, structured databases, vector embeddings"
    reasoning: "Supports reflection, planning, experience retrieval"
    source: "Chunk 1:893-896"

  - mechanism: "Activity Log"
    formalism: "Record of all Actions performed during activity"
    reasoning: "Transparency and traceability; no automated reasoning specified"
    source: "Chunk 1:871-873"

  - mechanism: "Library"
    formalism: "Repository of best practices, lessons learned, prompt templates, API credentials"
    reasoning: "Reusable knowledge accessible to agents"
    source: "Chunk 1:874-875"

  - mechanism: "Feature Diagram"
    formalism: "Software engineering notation for organizing taxonomic structure"
    reasoning: "Hierarchical feature models with dependencies"
    source: "Chunk 2:953-955, Chunk 3:53-55"

  - mechanism: "Prompt Templates"
    formalism: "Predefined and adaptable text patterns for LLM interaction"
    reasoning: "Pattern-based prompt engineering; reusable across scenarios"
    source: "Chunk 1:875, Chunk 2:66-67"

emergence_indicators:
  - phenomenon: "Cognitive Synergy"
    mechanism: "Collaboration of specialized agents produces capabilities beyond individual agents"
    evidence: "Paper's core premise; Minsky's 'society of mind' invoked"
    source: "Chunk 1:65, Chunk 1:481-484"

  - phenomenon: "System Profiles"
    mechanism: "Characteristic patterns emerge when mapping autonomy-alignment levels across aspects"
    evidence: "Three system groups identified (general-purpose, central-controller, role-agent) from classification"
    source: "Chunk 4:3-9, Chunk 3:902-907"

  - phenomenon: "Intertwined Dependency Complexity"
    mechanism: "Mixed autonomy levels across viewpoints create emergent operational challenges"
    evidence: "Example given of L2 decomposition + L0 context interaction causing dead-ends"
    source: "Chunk 2:820-849"

  - phenomenon: "Bounded Autonomy Pattern"
    mechanism: "High-autonomy aspects combined with low-alignment produce characteristic operational dynamics"
    evidence: "Most systems show this pattern for decomposition, action management, resource utilization"
    source: "Chunk 3:832-838, Chunk 3:975-989"

integration_surfaces:
  - surface: "Software Architecture Viewpoints"
    connects_to: ["Kruchten 4+1 Model", "Software Engineering taxonomies", "UML conceptual modeling"]
    alignment_quality: "Strong - explicit adaptation of established framework"
    source: "Chunk 2:641-643"

  - surface: "LangChain Framework"
    connects_to: ["Agent definitions", "Chain of tasks", "Vector databases", "Prompt templates"]
    alignment_quality: "Strong - several analyzed systems built on LangChain"
    source: "Chunk 1:348-352"

  - surface: "AI Safety/Alignment Research"
    connects_to: ["Control problem", "Value alignment", "AI safety discourse"]
    alignment_quality: "Acknowledged but not deeply integrated; pragmatic stance"
    source: "Chunk 2:362-364"

  - surface: "Multi-Agent Systems Literature"
    connects_to: ["Bird taxonomy", "Dudek taxonomy", "Wooldridge/Jennings taxonomy"]
    alignment_quality: "Builds upon but claims to supersede (pre-LLM frameworks)"
    source: "Chunk 1:269-291"

  - surface: "Foundation Model Research"
    connects_to: ["Hugging Face models", "NLP/Vision/Audio modalities"]
    alignment_quality: "Context resources map to foundation model categories"
    source: "Chunk 2:150-171"

gaps_and_tensions:
  - gap_type: "Omission"
    description: "No formal treatment of agent identity/persistence across sessions"
    implications: "Cannot model long-running agents, agent cloning, or agent identity problems"
    source: "Implicit - not discussed"

  - gap_type: "Omission"
    description: "No explicit error handling or failure mode ontology"
    implications: "Hallucination and dead-ends mentioned as problems but not formalized"
    source: "Chunk 4:175-185"

  - gap_type: "Tension"
    description: "Autonomy-alignment as complementary vs as tradeoff"
    implications: "Paper claims complementarity but empirical findings show bounded autonomy (high A, low L) dominates"
    source: "Chunk 2:368-370 vs Chunk 3:975-976"

  - gap_type: "Underspecified"
    description: "No formal semantics for the domain ontology"
    implications: "UML diagram is conceptual model only; no OWL or formal logic"
    source: "Chunk 1:812-813"

  - gap_type: "Tension"
    description: "User-centric alignment desired but rarely implemented"
    implications: "Real-time responsive alignment (L2) not found in ANY analyzed system"
    source: "Chunk 3:814-820, Chunk 4:315-316"

  - gap_type: "Omission"
    description: "No treatment of multi-tenancy or multi-user scenarios"
    implications: "Framework assumes single user prompting single goal"
    source: "Implicit - all examples are single-user"

  - gap_type: "Tension"
    description: "Generic vs domain-specific systems"
    implications: "Taxonomy applies to both but doesn't capture domain-specificity as a dimension"
    source: "Chunk 3:911-967"

  - gap_type: "Underspecified"
    description: "How agents acquire/update roles at L2 autonomy"
    implications: "Self-organizing role definition mentioned but mechanism not detailed"
    source: "Chunk 3:226-230"

empirical_grounding:
  - type: "System Analysis"
    domain: "LLM-powered Multi-Agent Systems"
    scale: "7 systems analyzed: AutoGPT, BabyAGI, SuperAGI, HuggingGPT, MetaGPT, CAMEL, AgentGPT"
    findings: "Autonomy concentrated in decomposition, action management, resource utilization; Alignment mostly L0"
    source: "Chunk 3:283-286, Chunk 3:799-821"

  - type: "Comparative Classification"
    domain: "Workflow automation"
    scale: "1 comparison system: Zapier"
    findings: "Zapier contrasts as User-Guided Automation (L0/L1) vs MAS bounded autonomy patterns"
    source: "Chunk 3:312-313, Chunk 3:762-786"

  - type: "Code/Documentation Review"
    domain: "Open-source MAS implementations"
    scale: "AutoGPT, SuperAGI, MetaGPT, Generative Agents, LangChain"
    findings: "Domain ontology derived from iterative analysis of these codebases"
    source: "Chunk 1:833-840"

  - type: "Interactive Testing"
    domain: "System engagement"
    scale: "All 7 analyzed systems"
    findings: "Operational issues observed: infinite loops, dead-ends, non-terminating activities"
    source: "Chunk 4:175-185"

---

# Multi-Agent Architecture Taxonomy for LLM-Powered Systems

## Summary

This paper introduces a comprehensive multi-dimensional taxonomy for analyzing autonomous LLM-powered multi-agent systems. The core contribution is treating **autonomy** and **alignment** as independent, cross-cutting concerns that can be configured at multiple levels across four architectural viewpoints.

## Key Discoveries

### SURPRISE: Autonomy and Alignment are Orthogonal Dimensions

The paper explicitly rejects treating autonomy and alignment as a tradeoff or spectrum. Instead, they form a 3x3 matrix where each combination represents a valid system configuration. "Bounded Autonomy" (high autonomy, low alignment) is just as valid as "User-Responsive Autonomy" (high both).

### SURPRISE: Software Architecture Frameworks Apply to MAS

The adaptation of Kruchten's 4+1 viewpoint model to multi-agent systems is novel. The paper demonstrates that traditional software architecture analysis tools (viewpoints, concerns, dependencies) can systematically analyze LLM-MAS architectures.

### SURPRISE: Real-Time Alignment is Absent

Despite defining L2 alignment (real-time responsive), NO analyzed system implements it. This represents a significant gap in current implementations - all systems either have integrated (L0) or user-guided pre-runtime (L1) alignment only.

### SURPRISE: Intertwined Dependencies Create Emergent Complexity

When different aspects have different autonomy levels, the interaction between availability-driven and requirements-driven dependencies creates complex, sometimes problematic system behaviors (infinite loops, dead-ends).

## Critical Concepts for Synthesis

### The Triadic Tension Model

The paper's Figure 3 (Human Users <-> Rules/Mechanisms <-> LLM-Agents) provides a powerful lens for analyzing ANY multi-agent system design choice. Every configuration option maps to this triangle.

### Cross-Cutting Concerns

Treating autonomy/alignment as cross-cutting concerns (from aspect-oriented programming) rather than localized features is methodologically significant. This allows systematic analysis across viewpoints rather than ad-hoc assessment.

### Configuration Space Quantification

The explicit calculation of 108 single options and 282 billion combined configurations demonstrates the SCALE of the design space for LLM-MAS. This argues for systematic taxonomy over intuitive design.

## Gaps for Further Research

1. **Formal semantics** - The domain ontology lacks formal OWL/logic representation
2. **Error handling** - No ontology of failure modes despite observing failures empirically
3. **Identity persistence** - Agent identity across sessions not addressed
4. **Multi-user scenarios** - Framework assumes single user/goal
5. **Real-time alignment** - Theoretical construct not yet implemented in practice

## Connections to Other Papers

- **PROV-O**: The Agent/Activity/Entity triad partially maps to this framework's Agent/Action/Task but with different emphasis
- **UFO**: The Role concept connects to UFO's anti-rigid types but without the formal modal logic
- **BFO**: The Occurrent/Continuant distinction is implicit in Action (occurrent) vs Agent (continuant) but not formalized
- **Process Mining**: The Task-Management Activity with phases maps loosely to process models but at a more abstract level
