---
paper_id: "20-Agentic_RAG_Survey"
title: "Agentic Retrieval-Augmented Generation: A Survey on Agentic RAG"
extraction_date: "2026-01-01"
extraction_type: "temporal_event_patterns"
schema_version: "1.0"

# HIGH PRIORITY FIELDS

event_types:
  - type: "Retrieval Event"
    description: "Query submission and document retrieval from external data sources (vector databases, knowledge bases, APIs)"
    source: "Chunk 1:161-163"
  - type: "Augmentation Event"
    description: "Processing retrieved data, extracting and summarizing relevant information to align with query context"
    source: "Chunk 1:165-166"
  - type: "Generation Event"
    description: "Combining retrieved information with LLM pre-trained knowledge to generate coherent responses"
    source: "Chunk 1:168-169"
  - type: "Reflection Event"
    description: "Iterative self-evaluation and refinement of outputs through self-feedback mechanisms"
    source: "Chunk 1:515-531"
  - type: "Planning Event"
    description: "Autonomous decomposition of complex tasks into smaller, manageable subtasks"
    source: "Chunk 1:540-549"
  - type: "Tool Invocation Event"
    description: "Agent interaction with external tools, APIs, or computational resources"
    source: "Chunk 1:555-569"
  - type: "Delegation Event"
    description: "Coordinator agent assigning tasks to specialized retrieval agents"
    source: "Chunk 1:886-904"
  - type: "Synthesis Event"
    description: "LLM integration of retrieved information into coherent response"
    source: "Chunk 2:28-30"
  - type: "Evaluation Event"
    description: "Relevance assessment of retrieved documents for quality control"
    source: "Chunk 2:232-233"
  - type: "Correction Event"
    description: "Query refinement and re-retrieval when initial results are insufficient"
    source: "Chunk 2:236-244"

event_definitions:
  Query_Submission:
    definition: "User initiates workflow by submitting a query to the system"
    temporal_properties:
      - "timestamp"
      - "triggers_evaluation"
    source: "Chunk 1:764-766"
  Knowledge_Source_Selection:
    definition: "Coordinating agent determines most suitable data sources based on query type"
    temporal_properties:
      - "follows_query_submission"
      - "precedes_retrieval"
    source: "Chunk 1:768-788"
  Data_Integration:
    definition: "Retrieved data from multiple sources passed to LLM for synthesis"
    temporal_properties:
      - "follows_retrieval"
      - "precedes_output"
    source: "Chunk 1:791-793"
  Output_Generation:
    definition: "System delivers comprehensive response addressing original query"
    temporal_properties:
      - "follows_synthesis"
      - "workflow_completion"
    source: "Chunk 1:796-798"
  Iterative_Refinement:
    definition: "Feedback loop to improve retrieval accuracy and response relevance"
    temporal_properties:
      - "cyclic"
      - "continues_until_threshold"
    source: "Chunk 1:361-362"

temporal_relations:
  - relation: "before"
    domain: "Query Submission"
    range: "Knowledge Source Selection"
    semantics: "Query must be received before source selection can begin"
    source: "Chunk 1:764-768"
  - relation: "before"
    domain: "Knowledge Source Selection"
    range: "Retrieval Event"
    semantics: "Source must be selected before retrieval can execute"
    source: "Chunk 1:768-788"
  - relation: "before"
    domain: "Retrieval Event"
    range: "Data Integration"
    semantics: "Data must be retrieved before synthesis can occur"
    source: "Chunk 1:791-793"
  - relation: "before"
    domain: "Data Integration"
    range: "Output Generation"
    semantics: "Synthesis must complete before response delivery"
    source: "Chunk 1:796-798"
  - relation: "triggers"
    domain: "Reflection Event"
    range: "Correction Event"
    semantics: "Self-evaluation may trigger corrective actions"
    source: "Chunk 1:523-525"
  - relation: "overlaps"
    domain: "Parallel Retrieval"
    range: "Parallel Retrieval"
    semantics: "Multiple retrieval agents execute simultaneously"
    source: "Chunk 2:19"
  - relation: "during"
    domain: "Tool Invocation"
    range: "Workflow Execution"
    semantics: "Tool calls occur within broader workflow context"
    source: "Chunk 1:555-569"
  - relation: "causes"
    domain: "Evaluation Event"
    range: "Correction Event"
    semantics: "Low relevance evaluation triggers query refinement"
    source: "Chunk 2:204-209"

lifecycle_patterns:
  - entity: "Agent Workflow"
    states: ["query_received", "evaluating", "retrieving", "synthesizing", "refining", "completed"]
    transitions:
      - from: "query_received"
        to: "evaluating"
        trigger: "query_analysis_start"
      - from: "evaluating"
        to: "retrieving"
        trigger: "source_selection_complete"
      - from: "retrieving"
        to: "synthesizing"
        trigger: "retrieval_complete"
      - from: "synthesizing"
        to: "refining"
        trigger: "quality_check_failed"
      - from: "refining"
        to: "retrieving"
        trigger: "re-retrieval_needed"
      - from: "synthesizing"
        to: "completed"
        trigger: "quality_check_passed"
    source: "Chunk 2:226-244"
  - entity: "Memory"
    states: ["short_term_active", "long_term_stored"]
    transitions:
      - from: "short_term_active"
        to: "long_term_stored"
        trigger: "conversation_context_persisted"
    source: "Chunk 1:491-493"
  - entity: "Document Workflow"
    states: ["parsing", "structured", "retrieved", "validated", "output_generated"]
    transitions:
      - from: "parsing"
        to: "structured"
        trigger: "extraction_complete"
      - from: "structured"
        to: "retrieved"
        trigger: "knowledge_retrieval_complete"
      - from: "retrieved"
        to: "validated"
        trigger: "agentic_orchestration_complete"
      - from: "validated"
        to: "output_generated"
        trigger: "synthesis_complete"
    source: "Chunk 2:714-749"
  - entity: "Corrective RAG"
    states: ["context_retrieved", "relevance_evaluated", "query_refined", "external_fetched", "response_synthesized"]
    transitions:
      - from: "context_retrieved"
        to: "relevance_evaluated"
        trigger: "evaluation_agent_invoked"
      - from: "relevance_evaluated"
        to: "query_refined"
        trigger: "low_relevance_detected"
      - from: "query_refined"
        to: "external_fetched"
        trigger: "refinement_insufficient"
      - from: "relevance_evaluated"
        to: "response_synthesized"
        trigger: "high_relevance_confirmed"
      - from: "external_fetched"
        to: "response_synthesized"
        trigger: "external_data_integrated"
    source: "Chunk 2:226-244"

state_change_mechanisms:
  - mechanism: "Query Complexity Classification"
    description: "Adaptive RAG classifier determines retrieval strategy based on query complexity (straightforward, simple, complex)"
    source: "Chunk 2:317-344"
  - mechanism: "Relevance Threshold Evaluation"
    description: "Documents below relevance threshold trigger corrective steps including query refinement"
    source: "Chunk 2:204-209"
  - mechanism: "Memory State Transition"
    description: "Short-term memory tracks immediate conversation state; long-term memory stores accumulated knowledge and agent experiences"
    source: "Chunk 1:491-493"
  - mechanism: "Feedback Loop Refinement"
    description: "Critic module validates retrieved data and flags low-confidence results for re-retrieval"
    source: "Chunk 2:493-499"
  - mechanism: "Hierarchical Delegation"
    description: "Top-tier agent evaluates query complexity and delegates to subordinate agents"
    source: "Chunk 2:103-127"

agent_participation:
  - participation_type: "initiates"
    description: "User submits query to start workflow"
    source: "Chunk 1:764"
  - participation_type: "performs"
    description: "Coordinating agent receives query and analyzes to determine suitable sources"
    source: "Chunk 1:764-766"
  - participation_type: "performs"
    description: "Specialized retrieval agents execute domain-specific retrieval tasks"
    source: "Chunk 1:890-904"
  - participation_type: "performs"
    description: "LLM synthesizes retrieved information into coherent response"
    source: "Chunk 1:791-793"
  - participation_type: "observes"
    description: "Critic module evaluates relevance and quality of retrieved information"
    source: "Chunk 2:493-499"
  - participation_type: "initiates"
    description: "Relevance Evaluation Agent flags documents for corrective actions"
    source: "Chunk 2:232-233"
  - participation_type: "performs"
    description: "Query Refinement Agent rewrites queries to improve retrieval"
    source: "Chunk 2:236-237"
  - participation_type: "performs"
    description: "Response Synthesis Agent integrates validated information"
    source: "Chunk 2:244"
  - participation_type: "oversees"
    description: "Top-tier agent in hierarchical system oversees and directs lower-level agents"
    source: "Chunk 2:103-106"

event_correlation:
  - pattern: "Query-to-Agent"
    description: "User query correlated to coordinating agent that manages workflow"
    source: "Chunk 1:764-766"
  - pattern: "Query-to-Source"
    description: "Query type determines appropriate knowledge source (SQL, semantic, web, recommendation)"
    source: "Chunk 1:768-788"
  - pattern: "Agent-to-Tool"
    description: "Each specialized agent correlated to specific retrieval tools and data sources"
    source: "Chunk 1:905-916"
  - pattern: "Workflow-to-Response"
    description: "Complete workflow correlated to final synthesized response"
    source: "Chunk 1:796-798"

# MEDIUM PRIORITY FIELDS

ordering_mechanisms:
  - mechanism: "Sequential Prompt Chaining"
    description: "Complex task decomposed into multiple steps where each step builds upon previous one"
    source: "Chunk 1:620-632"
  - mechanism: "Routing Classification"
    description: "Input classified and directed to appropriate specialized prompt or process"
    source: "Chunk 1:644-668"
  - mechanism: "Parallel Sectioning"
    description: "Task divided into independent processes that run simultaneously"
    source: "Chunk 1:671-693"
  - mechanism: "Orchestrator-Worker Delegation"
    description: "Central orchestrator dynamically breaks tasks into subtasks and assigns to workers"
    source: "Chunk 1:696-719"
  - mechanism: "Evaluator-Optimizer Iteration"
    description: "Initial output generated then iteratively refined based on evaluation feedback"
    source: "Chunk 1:721-740"
  - mechanism: "Hierarchical Tier Ordering"
    description: "Top-tier agents delegate to subordinate agents in multi-level decision-making structure"
    source: "Chunk 2:103-127"

causation_patterns:
  - pattern: "Query triggers Evaluation"
    description: "User query submission triggers coordinating agent evaluation"
    source: "Chunk 1:764-766"
  - pattern: "Evaluation triggers Retrieval"
    description: "Source selection causes retrieval process to begin"
    source: "Chunk 1:768-788"
  - pattern: "Low Relevance triggers Correction"
    description: "Documents flagged as irrelevant trigger query refinement"
    source: "Chunk 2:204-209"
  - pattern: "Complexity triggers Strategy"
    description: "Query complexity classification triggers appropriate retrieval strategy selection"
    source: "Chunk 2:317-328"
  - pattern: "Feedback triggers Refinement"
    description: "Critic module evaluation causes re-retrieval or response refinement"
    source: "Chunk 2:493-499"
  - pattern: "Reflection triggers Iteration"
    description: "Self-critique identifies errors causing iterative improvement cycle"
    source: "Chunk 1:515-531"

temporal_standards:
  - standard: "Workflow State Machine"
    description: "Implicit FSM governing state transitions in agentic workflows"
    source: "Chunk 2:226-244"
  - standard: "Sequential Processing"
    description: "Prompt chaining ensures ordered execution of dependent steps"
    source: "Chunk 1:620-632"
  - standard: "Parallel Execution"
    description: "Independent retrieval tasks may execute concurrently"
    source: "Chunk 2:19"

event_log_formats:
  - format: "N/A"
    description: "Paper does not specify explicit event log formats; focuses on workflow patterns rather than event storage"
    source: "N/A"
---

# Temporal Event Patterns: Agentic RAG Survey

## Executive Summary

This paper provides rich temporal/event patterns for agentic workflows, particularly relevant to:
- **Workflow orchestration patterns** (5 distinct patterns)
- **Agent lifecycle management** (memory, planning, reflection cycles)
- **Multi-agent coordination timing** (hierarchical, parallel, sequential)

## Key Temporal Contributions

### 1. Five Agentic Workflow Patterns with Temporal Semantics

| Pattern | Temporal Characteristic | Ordering |
|---------|------------------------|----------|
| Prompt Chaining | Sequential, dependent | Strict ordering |
| Routing | Classification-based branching | Conditional |
| Parallelization | Concurrent execution | Partial order |
| Orchestrator-Workers | Dynamic delegation | Hierarchical |
| Evaluator-Optimizer | Iterative cycles | Loop until satisfied |

**Source**: Chunk 1:620-740

### 2. Four Agentic Design Patterns

| Pattern | Temporal Behavior | Event Types |
|---------|-------------------|-------------|
| Reflection | Iterative self-evaluation loops | Evaluate, Refine |
| Planning | Task decomposition into subtasks | Decompose, Schedule |
| Tool Use | External invocation during workflow | Invoke, Wait, Receive |
| Multi-Agent | Parallel/coordinated agent actions | Delegate, Execute, Aggregate |

**Source**: Chunk 1:512-597

### 3. Memory State Model

```
Short-Term Memory <-> Long-Term Memory
     |                      |
[immediate state]    [accumulated knowledge]
[conversation]       [agent experiences]
```

**Source**: Chunk 1:491-493

### 4. Corrective RAG Lifecycle

```
Context Retrieved -> Relevance Evaluated -> Query Refined -> External Fetched -> Response Synthesized
                           |                                        ^
                           +-------- (if low relevance) ------------+
```

**Source**: Chunk 2:226-244

## Relevance to UDWO Metamodel

### Event Entity Definition
The paper suggests canonical event types for agentic systems:
- **Query Event**: Initiates workflow
- **Retrieval Event**: Data acquisition
- **Synthesis Event**: LLM integration
- **Evaluation Event**: Quality assessment
- **Correction Event**: Iterative refinement

### Temporal Operators
- **Sequential**: Prompt chaining enforces strict ordering
- **Parallel**: Sectioning allows concurrent execution
- **Conditional**: Routing enables branching based on classification
- **Iterative**: Evaluator-Optimizer cycles until quality threshold met

### Agent Participation Types
- **Coordinator**: Central orchestration role
- **Specialist**: Domain-specific retrieval
- **Evaluator**: Quality assessment
- **Synthesizer**: Response generation

### Causation Patterns
- Query -> Evaluation -> Retrieval -> Synthesis -> Output
- Low Relevance -> Correction -> Re-retrieval
- Complexity Classification -> Strategy Selection

## Quality Checklist

- [x] event_types: 10 types extracted
- [x] event_definitions: 5 definitions with temporal properties
- [x] temporal_relations: 8 relations extracted
- [x] lifecycle_patterns: 4 entities with state machines
- [x] state_change_mechanisms: 5 mechanisms extracted
- [x] agent_participation: 9 participation types extracted
- [x] event_correlation: 4 patterns extracted
- [x] ordering_mechanisms: 6 mechanisms extracted
- [x] causation_patterns: 6 patterns extracted
- [x] temporal_standards: 3 standards noted
- [ ] event_log_formats: N/A - not specified in paper

---

**Extraction completed**: 2026-01-01
**Extracted by**: Claude Opus 4.5
