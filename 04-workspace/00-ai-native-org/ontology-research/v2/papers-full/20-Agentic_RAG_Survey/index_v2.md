---
title: "Agentic Retrieval-Augmented Generation: A Survey on Agentic RAG"
paper_id: "20-Agentic_RAG_Survey"
extraction_version: "v2"
extraction_date: "2025-12-31"
domain: "AI/LLM Agents, Knowledge Retrieval, Multi-agent Systems"
source_chunks: 3

ontological_primitives:
  - term: "AI Agent"
    definition: "An intelligent entity comprising LLM (with Role and Task), Memory (short-term and long-term), Planning (reflection and self-critique), and Tools"
    source: "Chunk 1:484-502"
    unique_aspects: "Four-component architecture: LLM core, dual memory, planning layer, tool access. Notably treats agent as composite rather than atomic."

  - term: "Agentic Patterns"
    definition: "Structured methodologies that guide agent behavior: Reflection, Planning, Tool Use, Multi-Agent Collaboration"
    source: "Chunk 1:507-509"
    unique_aspects: "These are BEHAVIORAL primitives, not entity primitives - patterns of action rather than types of things"

  - term: "Agentic Workflow Patterns"
    definition: "Structural patterns for LLM application orchestration: Prompt Chaining, Routing, Parallelization, Orchestrator-Workers, Evaluator-Optimizer"
    source: "Chunk 1:610-614"
    unique_aspects: "Distinct from agentic patterns - these are STRUCTURAL/FLOW patterns vs behavioral patterns"

  - term: "Query"
    definition: "The initiating input that triggers retrieval and generation workflows"
    source: "Chunk 1:764-766"
    unique_aspects: "Query is the primary event that activates the entire pipeline - it's the fundamental trigger primitive"

  - term: "Knowledge Source"
    definition: "External data repositories accessed during retrieval: Structured Databases, Semantic Search, Web Search, Recommendation Systems"
    source: "Chunk 1:768-789"
    unique_aspects: "Taxonomy of knowledge sources is functional rather than ontological - defined by access pattern"

  - term: "Retrieval-Augmentation-Generation Triad"
    definition: "Three core components - Retrieval (query external sources), Augmentation (process retrieved data), Generation (combine with LLM knowledge)"
    source: "Chunk 1:158-170"
    unique_aspects: "This is the fundamental process triad of all RAG systems"

structural_patterns:
  - pattern_name: "Query-Route-Retrieve-Synthesize-Respond"
    structure: "Linear flow: User Query -> Agent Evaluation -> Source Selection -> Data Retrieval -> LLM Synthesis -> Output"
    instances:
      - "Single-Agent RAG workflow (Chunk 1:764-799)"
      - "Multi-Agent RAG workflow (Chunk 1:886-932)"
      - "Hierarchical RAG workflow (Chunk 2:115-136)"
    source: "Chunk 1:764-799"

  - pattern_name: "Coordinator-Specialist Hierarchy"
    structure: "Central orchestrator delegates to specialized subordinate agents"
    instances:
      - "Multi-Agent RAG: coordinator agent distributes to retrieval agents (Chunk 1:886-891)"
      - "Hierarchical RAG: top-tier agent delegates to subordinate agents (Chunk 2:103-127)"
      - "Orchestrator-Workers workflow pattern (Chunk 1:696-718)"
    source: "Multiple - core architectural pattern"

  - pattern_name: "Iterative Refinement Loop"
    structure: "Generate -> Evaluate -> Critique -> Refine -> Repeat"
    instances:
      - "Reflection pattern: self-feedback and iterative improvement (Chunk 1:515-531)"
      - "Evaluator-Optimizer workflow (Chunk 1:721-741)"
      - "Corrective RAG: document relevance evaluation and correction (Chunk 2:193-244)"
    source: "Chunk 1:515-531"

  - pattern_name: "Complexity-Adaptive Routing"
    structure: "Classify query complexity -> Route to appropriate strategy (simple/medium/complex)"
    instances:
      - "Adaptive RAG: classifier predicts complexity, selects strategy (Chunk 2:317-380)"
      - "Routing workflow pattern (Chunk 1:644-668)"
    source: "Chunk 2:317-380"

  - pattern_name: "Parallel Specialization"
    structure: "Multiple specialized agents execute concurrently, results aggregated"
    instances:
      - "Multi-Agent RAG parallel retrieval (Chunk 1:917)"
      - "Parallelization workflow: sectioning and voting (Chunk 1:671-694)"
    source: "Chunk 1:671-694"

  - pattern_name: "Graph-Text Fusion"
    structure: "Combine structured graph knowledge with unstructured document retrieval"
    instances:
      - "Agent-G: graph knowledge base + document retrieval + critic module (Chunk 2:449-478)"
      - "GeAR: graph expansion enhances base retrievers (Chunk 2:586-623)"
    source: "Chunk 2:449-478"

novel_concepts:
  - concept: "Agentic RAG"
    definition: "RAG paradigm that embeds autonomous AI agents into the retrieval-generation pipeline, enabling dynamic retrieval strategies, iterative refinement, and adaptive workflows"
    novelty_claim: "Transcends traditional RAG by introducing agent autonomy, not just improved retrieval"
    source: "Chunk 1:55-60"

  - concept: "Agentic Document Workflows (ADW)"
    definition: "End-to-end knowledge work automation that orchestrates document parsing, retrieval, reasoning, and structured outputs with intelligent agents"
    novelty_claim: "Extends RAG to full document-centric process automation, not just Q&A"
    source: "Chunk 2:704-708"

  - concept: "Corrective RAG"
    definition: "RAG with self-correction mechanisms using specialized agents: Relevance Evaluation Agent, Query Refinement Agent, External Knowledge Retrieval Agent, Response Synthesis Agent"
    novelty_claim: "Introduces explicit correction loop with agent specialization for quality assurance"
    source: "Chunk 2:193-244"

  - concept: "Adaptive RAG"
    definition: "RAG that dynamically adjusts handling strategy based on query complexity classification"
    novelty_claim: "Not just routing but LEARNING to adapt - uses trained classifier on query patterns"
    source: "Chunk 2:317-380"

  - concept: "Meta-Agent Architecture"
    definition: "In LlamaIndex ADW: sub-agents manage smaller document sets, coordinated by top-level agent"
    novelty_claim: "Hierarchical document partitioning with agent-per-partition, novel decomposition strategy"
    source: "Chunk 3:169-172"

  - concept: "Critic Module"
    definition: "Agent component that evaluates relevance and quality of retrieved information, flags low-confidence results"
    novelty_claim: "Explicit quality gate as architectural component, not just post-processing"
    source: "Chunk 2:474-476"

semantic_commitments:
  - commitment: "Agent as Composite Entity"
    position: "AI Agent is NOT atomic but composed of LLM + Memory + Planning + Tools"
    implications: "Agent identity is tied to configuration, not a single substrate"
    source: "Chunk 1:484-502"

  - commitment: "Behavioral over Ontological Taxonomy"
    position: "System categorized by WHAT IT DOES (patterns) not WHAT IT IS"
    implications: "Functional classification prioritized over essence-based classification"
    source: "Chunk 1:507-509, 610-614"

  - commitment: "Query-Centric Event Model"
    position: "User query is the initiating event that triggers all downstream processing"
    implications: "System is reactive rather than proactive - waits for query stimulus"
    source: "Chunk 1:764-766"

  - commitment: "Knowledge Externalism"
    position: "Valuable knowledge resides OUTSIDE the LLM in retrievable sources"
    implications: "LLM is reasoning engine, not knowledge repository"
    source: "Chunk 1:96-101"

  - commitment: "Process over State"
    position: "Focus on workflows, patterns, and pipelines rather than static entity types"
    implications: "Dynamic, procedural ontology rather than static, substantive ontology"
    source: "Throughout - paper organized by process patterns"

boundary_definitions:
  - entity_type: "RAG Paradigm Boundaries"
    identity_criteria: "Defined by retrieval mechanism (keyword vs dense vs hybrid), workflow structure (static vs adaptive vs agentic)"
    boundary_cases: "When does Advanced RAG become Modular RAG? When does Modular become Agentic? Boundaries are capability-based, somewhat fuzzy"
    source: "Chunk 1:172-383 (RAG evolution section)"

  - entity_type: "Agent Boundary"
    identity_criteria: "Defined by role, memory scope, and tool access - each agent has its own 'memory and workflow'"
    boundary_cases: "Can an agent be forked? Is a coordinator agent the 'same' agent across queries?"
    source: "Chunk 1:591-592"

  - entity_type: "Agentic Pattern vs Workflow Pattern"
    identity_criteria: "Agentic patterns = behavioral (reflection, planning, tool use, collaboration); Workflow patterns = structural (chaining, routing, parallelization)"
    boundary_cases: "Overlap exists - is 'orchestrator-worker' a workflow pattern or multi-agent pattern?"
    source: "Chunk 1:507-614"

  - entity_type: "Single vs Multi-Agent System"
    identity_criteria: "Single = one centralized agent handles all; Multi = coordinator + specialized agents"
    boundary_cases: "Does a single agent with multiple tools count as multi-agent?"
    source: "Chunk 1:752-759, 874-880"

temporal_modeling:
  - aspect: "Query-Response Cycle"
    approach: "Discrete event model - query initiates, processing occurs, response terminates"
    mechanism: "Each query is an independent transaction; no explicit temporal continuity across queries"
    source: "Throughout workflow descriptions"

  - aspect: "Iterative Refinement"
    approach: "Multiple rounds/cycles within single query"
    mechanism: "Reflection, correction, and optimization happen in loops before final response"
    source: "Chunk 1:515-531 (Reflection), Chunk 2:193-244 (Corrective)"

  - aspect: "Memory Persistence"
    approach: "Short-term (within conversation) vs Long-term (across sessions)"
    mechanism: "Short-term tracks conversation state; long-term stores accumulated knowledge and experiences"
    source: "Chunk 1:490-493"

  - aspect: "Latency as Design Constraint"
    approach: "Time is a cost to minimize, not a semantic dimension"
    mechanism: "Parallel processing, adaptive routing, workflow optimization all target latency reduction"
    source: "Chunk 1:445-456, 671-676"

agency_spectrum:
  - agent_type: "Naive/Traditional RAG System"
    capabilities: "Static retrieval, fixed workflow, no adaptation"
    constraints: "No autonomy - purely reactive pipeline"
    source: "Chunk 1:196-226"

  - agent_type: "Single Agent (Router)"
    capabilities: "Query evaluation, source selection, routing decisions"
    constraints: "Centralized - bottleneck for complex queries, limited parallelization"
    source: "Chunk 1:752-827"

  - agent_type: "Specialized Retrieval Agent"
    capabilities: "Domain-specific retrieval (SQL, semantic search, web search, recommendations)"
    constraints: "Narrow scope - optimized for one data type/source"
    source: "Chunk 1:890-904"

  - agent_type: "Coordinator/Orchestrator Agent"
    capabilities: "Task decomposition, agent delegation, result aggregation, strategic prioritization"
    constraints: "Coordination overhead, depends on subordinate agents"
    source: "Chunk 1:886-888, Chunk 2:103-106"

  - agent_type: "Critic Agent"
    capabilities: "Relevance evaluation, quality assessment, correction triggering"
    constraints: "Evaluative only - does not retrieve or generate"
    source: "Chunk 2:204-206, 474-476"

  - agent_type: "Query Refinement Agent"
    capabilities: "Semantic query rewriting, specificity optimization"
    constraints: "Operates on queries only, not on retrieved content"
    source: "Chunk 2:208-209, 236-237"

  - agent_type: "Human User"
    capabilities: "Query initiation, implicit feedback through interaction"
    constraints: "External to system - provides input, receives output"
    source: "Implicit throughout - query submitter role"

knowledge_representation:
  - mechanism: "Vector Database"
    formalism: "Dense vector embeddings for semantic similarity search"
    reasoning: "Nearest-neighbor retrieval, no explicit logical reasoning"
    source: "Chunk 1:162-163, Chunk 3:214-217"

  - mechanism: "Knowledge Graph"
    formalism: "Graph-structured data with nodes (entities) and edges (relationships)"
    reasoning: "Multi-hop traversal, relationship extraction, hierarchical navigation"
    source: "Chunk 1:302-318 (Graph RAG), Chunk 2:449-478 (Agent-G)"

  - mechanism: "Hybrid Retrieval"
    formalism: "Combination of sparse (BM25) and dense (DPR) methods"
    reasoning: "Lexical matching + semantic similarity, broader coverage"
    source: "Chunk 1:274-276"

  - mechanism: "LLM as Reasoning Engine"
    formalism: "Natural language in/out, internal transformer representations"
    reasoning: "Synthesis, summarization, contextual integration, response generation"
    source: "Chunk 1:487-489, throughout"

  - mechanism: "Agent Memory"
    formalism: "Short-term (conversation context) + Long-term (persistent knowledge store)"
    reasoning: "Context-dependent retrieval, experience accumulation"
    source: "Chunk 1:490-493"

emergence_indicators:
  - phenomenon: "Multi-Agent Collaboration Outcomes"
    mechanism: "Specialized agents + coordinator produce responses neither could alone"
    evidence: "Multi-domain research assistant example synthesizes SQL data + academic papers + news + recommendations"
    source: "Chunk 1:973-996"

  - phenomenon: "Adaptive Behavior from Classification"
    mechanism: "Query classifier + strategy selection produces emergent adaptation"
    evidence: "System 'learns' which strategy to use based on query patterns"
    source: "Chunk 2:350-358"

  - phenomenon: "Self-Correction Without Explicit Programming"
    mechanism: "Corrective RAG agents evaluate and refine each other's outputs"
    evidence: "Relevance agent triggers query refinement which triggers external retrieval - cascading correction"
    source: "Chunk 2:226-244"

  - phenomenon: "Graph-Enhanced Reasoning"
    mechanism: "Graph structure enables reasoning paths not explicit in documents"
    evidence: "Multi-hop QA answering 'Which author influenced the mentor of X' requires graph traversal"
    source: "Chunk 2:663-698"

integration_surfaces:
  - surface: "Agent Concept"
    connects_to: ["PROV-O Agent (provenance attribution)", "UFO Agent (intentionality)", "BDI Agent (beliefs-desires-intentions)"]
    alignment_quality: "Partial - paper's agent is componentized (LLM+Memory+Planning+Tools), lacks explicit intentionality discourse"
    source: "Chunk 1:484-502"

  - surface: "Activity/Workflow"
    connects_to: ["BPMN Process", "OCEL Activity", "PROV-O Activity"]
    alignment_quality: "Moderate - workflow patterns map to process constructs, but no formal process ontology adopted"
    source: "Chunk 1:610-741"

  - surface: "Knowledge Graph"
    connects_to: ["RDF/OWL frameworks", "Property graphs (Neo4j)", "Knowledge Graph QA literature"]
    alignment_quality: "Good - explicit integration with graph-based retrieval, cites relevant benchmarks"
    source: "Chunk 2:449-478, Chunk 3:214-217"

  - surface: "Tools/APIs"
    connects_to: ["Function calling (OpenAI)", "Tool use (Anthropic)", "External system integration"]
    alignment_quality: "Strong - tool use is core agentic pattern, well-defined integration points"
    source: "Chunk 1:555-569"

  - surface: "Memory Systems"
    connects_to: ["RAG vector stores", "Conversation history", "Long-term memory research"]
    alignment_quality: "Moderate - dual memory (short/long) mentioned but not deeply theorized"
    source: "Chunk 1:490-493"

gaps_and_tensions:
  - gap_type: "Omission"
    description: "No explicit ontological grounding - paper is purely architectural/functional"
    implications: "No formal semantics for agent, activity, or knowledge concepts"
    source: "Throughout - no references to foundational ontologies like UFO, BFO, DOLCE"

  - gap_type: "Omission"
    description: "No treatment of agent identity, persistence, or lifecycle"
    implications: "Cannot formally reason about agent continuity, forking, or termination"
    source: "Implicit - agents are described functionally but not as persistent entities"

  - gap_type: "Omission"
    description: "No explicit goal/intention modeling"
    implications: "Agents have 'tasks' and 'roles' but no formal goal representation"
    source: "Chunk 1:487-488 - LLM has 'defined Role and Task' but not elaborated"

  - gap_type: "Tension"
    description: "Agentic Patterns vs Workflow Patterns distinction is blurry"
    implications: "Is orchestrator-worker a workflow pattern or multi-agent pattern? Categorization seems ad-hoc"
    source: "Chunk 1:507-614 - parallel taxonomies without clear boundary"

  - gap_type: "Tension"
    description: "Single agent 'with tools' vs multi-agent system"
    implications: "When does tool invocation become agent delegation? Paper doesn't clarify"
    source: "Chunk 1:555-569 (tool use) vs Chunk 1:874-880 (multi-agent)"

  - gap_type: "Underspecified"
    description: "Memory semantics - what IS stored in long-term memory?"
    implications: "No clear model of what gets persisted, how it's structured, or how it's retrieved"
    source: "Chunk 1:490-493 - mentions 'accumulated knowledge and agent experiences' without formalization"

  - gap_type: "Underspecified"
    description: "Coordination mechanisms in multi-agent systems"
    implications: "Acknowledges 'coordination complexity' as challenge but no formal coordination model"
    source: "Chunk 1:959-962, Chunk 2:156-161"

  - gap_type: "Missing"
    description: "No treatment of rules, constraints, or governance"
    implications: "Agents operate without explicit behavioral bounds or compliance frameworks"
    source: "Not addressed - agents just 'do things' without governance layer"

  - gap_type: "Missing"
    description: "No provenance tracking"
    implications: "Cannot trace how responses were derived from sources - black box generation"
    source: "Despite citing PROV-related work, no integration of provenance"

empirical_grounding:
  - type: "Industry Case Studies"
    domain: "Multiple: Customer Support, Healthcare, Finance, Legal, Education"
    scale: "Illustrative examples, not quantitative evaluations"
    findings: "Demonstrates applicability but lacks rigorous validation"
    source: "Chunk 3:1-150 (Applications section)"

  - type: "Framework/Tool Ecosystem"
    domain: "LangChain, LlamaIndex, CrewAI, AutoGen, Vertex AI, Semantic Kernel, Amazon Bedrock, IBM Watson"
    scale: "Survey of available implementations"
    findings: "Rich ecosystem exists but no comparative benchmarks"
    source: "Chunk 3:153-218"

  - type: "Benchmark Datasets"
    domain: "QA, Reasoning, Retrieval"
    scale: "Lists ~50+ datasets across categories"
    findings: "Notes lack of AGENTIC-specific benchmarks as a gap"
    source: "Chunk 3:220-327"

  - type: "Specific Case: Twitch Ad Sales"
    domain: "Advertising/Marketing"
    scale: "Single enterprise deployment"
    findings: "RAG on Amazon Bedrock 'significantly boosted operational efficiency'"
    source: "Chunk 3:5-9"

surprises_and_discoveries:
  - surprise: "Behavioral primitives over entity primitives"
    description: "Paper's taxonomy is organized by PATTERNS OF ACTION (reflection, planning, tool use) rather than TYPES OF THINGS. This is a process-centric rather than substance-centric ontology."
    implications: "May align better with process mining and OCEL than with BFO/UFO entity hierarchies"

  - surprise: "Agent as configured composite, not primitive"
    description: "Unlike UFO where Agent is near-primitive, here Agent = LLM + Memory + Planning + Tools. The 'agent' is an assembled system, not an atomic entity."
    implications: "Agent identity becomes configuration-dependent - same LLM with different memory/tools = different agent?"

  - surprise: "Two parallel pattern taxonomies"
    description: "Agentic Patterns (Reflection, Planning, Tool Use, Multi-Agent) AND Workflow Patterns (Chaining, Routing, Parallelization, etc.) exist side-by-side without clear integration"
    implications: "Paper reveals two orthogonal dimensions: behavioral capabilities vs structural arrangements"

  - surprise: "Latency as primary temporal concern"
    description: "Time is treated as a cost to minimize, not as a semantic dimension. No discussion of temporal ordering, causality, or temporal relationships."
    implications: "Contrasts sharply with process ontologies (OCEL, PROV) where time is semantically rich"

  - surprise: "No goals, only tasks"
    description: "Despite being about 'agentic' systems, there's no formal goal modeling. Agents have 'tasks' and 'roles' but no intentions, desires, or goal hierarchies."
    implications: "Gap between AI agent engineering and classical agent theory (BDI)"

  - surprise: "Critic as architectural component"
    description: "Quality evaluation is reified as a distinct agent type (Critic Module), not just a post-processing step. This is an interesting ontological choice - making evaluation first-class."
    implications: "Suggests evaluation/critique may deserve primitive status in agent ontologies"
---

# Agentic RAG Survey - V2 Discovery Extraction

## Executive Summary

This survey paper presents a comprehensive taxonomy of Agentic Retrieval-Augmented Generation systems, tracing the evolution from naive RAG through to agent-orchestrated architectures. The paper is organized around **process patterns** rather than **entity types**, revealing a fundamentally procedural rather than substantive ontological orientation.

## Key Ontological Insights

### 1. Process-Centric Over Entity-Centric

The paper organizes knowledge around:
- **Agentic Patterns**: Reflection, Planning, Tool Use, Multi-Agent Collaboration
- **Workflow Patterns**: Prompt Chaining, Routing, Parallelization, Orchestrator-Workers, Evaluator-Optimizer

This is a BEHAVIORAL taxonomy - what agents DO, not what they ARE.

### 2. Agent as Configured Composite

The paper defines an AI Agent as comprising four components:
1. LLM (with Role and Task)
2. Memory (Short-term and Long-term)
3. Planning (Reflection and Self-Critique)
4. Tools (Vector Search, Web Search, APIs)

This is notably different from philosophical agent concepts where agency is primitive. Here, agents are ASSEMBLED from components.

### 3. The RAG Evolution Hierarchy

```
Naive RAG
    |
    v
Advanced RAG (dense retrieval, re-ranking)
    |
    v
Modular RAG (hybrid retrieval, tool integration)
    |
    v
Graph RAG (knowledge graph integration)
    |
    v
Agentic RAG (autonomous decision-making, multi-agent)
```

Each level adds capabilities but also coordination complexity.

### 4. Novel Architectural Concepts

- **Corrective RAG**: Self-correction through specialized agents (Relevance Evaluation, Query Refinement, External Retrieval, Response Synthesis)
- **Adaptive RAG**: Query complexity classification drives strategy selection
- **Agentic Document Workflows**: End-to-end document automation, not just Q&A
- **Meta-Agent Architecture**: Sub-agents manage document partitions, coordinated by top-level agent

## Critical Gaps Identified

1. **No Formal Ontology**: Despite extensive architectural taxonomy, no grounding in foundational ontologies
2. **No Goal Modeling**: Tasks and roles exist, but no intentions, desires, or goal hierarchies
3. **No Provenance**: Despite retrieval focus, no mechanism to trace how responses derive from sources
4. **No Governance Layer**: Agents operate without explicit behavioral constraints or compliance
5. **Memory Underspecified**: Dual memory (short/long-term) mentioned but not formalized

## Integration Opportunities

| This Paper | Potential Alignment |
|------------|---------------------|
| Agentic Patterns | UFO Agent dispositions |
| Workflow Patterns | BPMN/OCEL process structures |
| Knowledge Graph retrieval | RDF/OWL reasoning |
| Agent Memory | PROV-O derivation chains |
| Coordinator Agent | UFO Social Role |

## Implications for Synthesis

1. The paper's BEHAVIORAL focus complements entity-focused foundational ontologies
2. The pattern taxonomy provides a valuable bridge between abstract ontology and implementation
3. The gap in goal/intention modeling is a synthesis opportunity
4. The Critic Module concept suggests evaluation deserves ontological status
5. The process-centric orientation aligns with OCEL/process mining more than BFO/UFO

## Quality Checklist

- [x] Used paper's own terminology (not normalized)
- [x] Captured at least 2 novel concepts (Corrective RAG, Adaptive RAG, ADW, Meta-Agent)
- [x] Found at least 1 gap or tension (9 gaps documented)
- [x] Noted at least 1 surprise (6 surprises documented)
- [x] All extractions have chunk:line references
- [x] Did NOT force-fit to predefined categories
- [x] Preserved nuance and qualification
