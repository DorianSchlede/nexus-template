---
paper_id: "18-HallucinationSurvey-2509.18970"
title: "LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions"
authors: ["Xixun Lin", "Yucheng Ning", "Jingwen Zhang", "et al."]
year: 2025
chunks_expected: 8
chunks_read: 8
analysis_complete: true
schema_version: "2.3"
high_priority_fields_found: 6

chunk_index:
  1:
    token_count: 4874
    hash: "chunk1_hash"
    fields_found:
      pattern_definition: true
      mechanism_type: true
      failure_mode: partial
      implementation_detail: false
      integration_point: true
      quality_metric: false
      limitation: true
      related_pattern: partial
  2:
    token_count: 6015
    hash: "chunk2_hash"
    fields_found:
      pattern_definition: true
      mechanism_type: true
      failure_mode: true
      implementation_detail: partial
      integration_point: true
      quality_metric: partial
      limitation: true
      related_pattern: true
  3:
    token_count: 5420
    hash: "chunk3_hash"
    fields_found:
      pattern_definition: true
      mechanism_type: true
      failure_mode: partial
      implementation_detail: partial
      integration_point: true
      quality_metric: partial
      limitation: true
      related_pattern: true
  4:
    token_count: 5878
    hash: "chunk4_hash"
    fields_found:
      pattern_definition: true
      mechanism_type: true
      failure_mode: partial
      implementation_detail: partial
      integration_point: true
      quality_metric: partial
      limitation: true
      related_pattern: partial
  5:
    token_count: 6270
    hash: "chunk5_references"
    fields_found:
      pattern_definition: false
      mechanism_type: false
      failure_mode: false
      implementation_detail: false
      integration_point: false
      quality_metric: false
      limitation: false
      related_pattern: false
  6:
    token_count: 6174
    hash: "chunk6_references"
    fields_found:
      pattern_definition: false
      mechanism_type: false
      failure_mode: false
      implementation_detail: false
      integration_point: false
      quality_metric: false
      limitation: false
      related_pattern: false
  7:
    token_count: 5722
    hash: "chunk7_references"
    fields_found:
      pattern_definition: false
      mechanism_type: false
      failure_mode: false
      implementation_detail: false
      integration_point: false
      quality_metric: false
      limitation: false
      related_pattern: false
  8:
    token_count: 2017
    hash: "chunk8_appendix"
    fields_found:
      pattern_definition: true
      mechanism_type: partial
      failure_mode: true
      implementation_detail: false
      integration_point: true
      quality_metric: false
      limitation: partial
      related_pattern: partial

pattern_definition:
  - name: "Multi-Agent Communication Loop"
    purpose: "Formal model for agent coordination with Broadcasting and Structure Evolution phases"
    mechanism: "POMDP-based loop: Reasoning-Execution-Broadcasting-Feedback-Perception-Memorization-Belief Update-Structure Evolution"
    chunk_ref: "1:419-428"
    quote: "Reasoning-Execution-Broadcasting-Feedback-Environment Transition..."
    confidence: "high"
  - name: "Belief State Maintenance"
    purpose: "Enable agents to maintain subjective understanding of partially observable environments"
    mechanism: "Continuous belief state updates based on observations and actions"
    chunk_ref: "1:290-294"
    quote: "agents must maintain a Belief State to represent its subjective understanding"
    confidence: "high"
  - name: "Structured Message Format"
    purpose: "Reduce miscommunication in agent-to-agent messaging"
    mechanism: "Use JSON or structured formats instead of natural language"
    chunk_ref: "2:468-471"
    quote: "Adopting structured formats (e.g., JSON) can improve clarity and rigor"
    confidence: "high"
  - name: "Fault-tolerant Design Pattern"
    purpose: "Prevent erroneous decisions from message loss or delays"
    mechanism: "Confirmation conditions and synchronization constraints"
    chunk_ref: "2:471-474"
    quote: "robust Fault-tolerant Design, incorporating confirmation conditions"
    confidence: "high"
  - name: "Self-verification Mechanism"
    purpose: "Lightweight internal output validation without external validators"
    mechanism: "Self-reflection, self-consistency, self-questioning"
    chunk_ref: "3:403-433"
    quote: "agents assess the validity and reliability of their own outputs"
    confidence: "high"
  - name: "External Validator Pattern"
    purpose: "Independent verification of agent outputs"
    mechanism: "Language-based, Retrieval-based, Execution-based, Simulation-based validators"
    chunk_ref: "3:436-443"
    quote: "leverages external validators to verify the correctness of agents outputs"
    confidence: "high"
  - name: "Chain-of-Thought (CoT)"
    purpose: "Improve reasoning accuracy through step-by-step decomposition"
    mechanism: "Step-by-step reasoning instructions in prompts"
    chunk_ref: "3:185-189"
    quote: "CoT guides the agent to break down complex problems"
    confidence: "high"
  - name: "Tree-of-Thought (ToT)"
    purpose: "Enhance reasoning robustness through parallel path exploration"
    mechanism: "Explore and evaluate multiple reasoning paths in parallel"
    chunk_ref: "3:189-194"
    quote: "ToT explores and evaluates multiple reasoning paths in parallel"
    confidence: "high"
  - name: "Lightweight Checkpoint Injection"
    purpose: "Enable early hallucination detection at each pipeline stage"
    mechanism: "Inject verification checkpoints between processing stages"
    chunk_ref: "4:186-189"
    quote: "lightweight checkpoints can be injected at each stage to verify"
    confidence: "high"
  - name: "Constrained Prompting"
    purpose: "Focus agent attention on task-relevant information"
    mechanism: "Semantic and spatial constraints in prompts"
    chunk_ref: "3:194-199"
    quote: "guides the agent to focus on task-relevant information"
    confidence: "high"

mechanism_type:
  - type: "verification"
    name: "Self-reflection"
    description: "Agents revisit and critique own outputs through introspection"
    chunk_ref: "4:22-25"
    confidence: "high"
  - type: "verification"
    name: "Self-consistency"
    description: "Multiple candidate outputs aggregated via majority voting"
    chunk_ref: "4:28-32"
    confidence: "high"
  - type: "detection"
    name: "Self-questioning"
    description: "Agent poses verification questions about its own reasoning"
    chunk_ref: "4:33-35"
    confidence: "high"
  - type: "verification"
    name: "Language-based Validation"
    description: "Assess truthfulness via atomic fact decomposition and entailment"
    chunk_ref: "4:46-48"
    confidence: "high"
  - type: "verification"
    name: "Retrieval-based Validation"
    description: "Verify against external sources like search engines"
    chunk_ref: "4:104-106"
    confidence: "high"
  - type: "verification"
    name: "Execution-based Validation"
    description: "Run generated code/plans to verify correctness"
    chunk_ref: "4:106-108"
    confidence: "high"
  - type: "verification"
    name: "Simulation-based Validation"
    description: "Test in sandboxed environments for embodied tasks"
    chunk_ref: "4:108-111"
    confidence: "high"
  - type: "verification"
    name: "Ensemble Validation"
    description: "Cross-verification using multiple validator types"
    chunk_ref: "4:112-116"
    confidence: "high"

failure_mode:
  - name: "Erroneous Message Propagation"
    description: "Agents produce messages with inaccurate facts or misleading inferences"
    chunk_ref: "2:441-448"
    quote: "messages containing inaccurate facts, misinterpretations..."
    confidence: "high"
  - name: "Hallucination Accumulation"
    description: "Minor hallucinations amplify over multi-step processes"
    chunk_ref: "4:153-160"
    quote: "hallucinations can accumulate and amplify over time"
    confidence: "high"
  - name: "Echo Chamber Effect"
    description: "Information progressively distorted through agent chain transmission"
    chunk_ref: "8:192-205"
    quote: "telephone game style accumulation of deviations"
    confidence: "high"
  - name: "Content Redundancy"
    description: "Unnecessary repetitive content obscures critical signals"
    chunk_ref: "2:448-451"
    quote: "generate unnecessary or repetitive content that obscures critical signals"
    confidence: "high"
  - name: "Information Asymmetry"
    description: "Different agent roles have varying information access causing bias"
    chunk_ref: "2:451-456"
    quote: "asymmetric settings may yield vague or incomplete instructions"
    confidence: "high"

implementation_detail:
  - item: "NOT_FOUND"
    chunk: null
    lines: null
    quote: null
    reason: "Paper is a survey without concrete code implementations"

integration_point:
  - type: "handover"
    name: "Broadcasting Phase"
    description: "Agent broadcasts messages to neighbors according to plan"
    chunk_ref: "1:422-426"
    confidence: "high"
  - type: "verification"
    name: "Post-hoc Verification"
    description: "Output monitoring and evaluation after task execution"
    chunk_ref: "3:395-402"
    confidence: "high"
  - type: "execution"
    name: "Decoding Optimization"
    description: "Test-time probability adjustment during generation"
    chunk_ref: "3:375-381"
    confidence: "high"
  - type: "handover"
    name: "Structure Evolution"
    description: "Dynamic update of communication topology between agents"
    chunk_ref: "1:426-427"
    confidence: "high"

quality_metric:
  - metric: "Hallucination Type Coverage"
    description: "Five distinct hallucination types identified across agent pipeline"
    chunk_ref: "1:28-37"
    confidence: "high"
  - metric: "Mitigation Method Mapping"
    description: "Ten mitigation methods mapped to hallucination types in Table I"
    chunk_ref: "4:116-118"
    confidence: "medium"

limitation:
  - description: "Agent hallucinations span multiple steps with multi-state transitions"
    chunk_ref: "1:196-200"
    quote: "hallucinations often span multiple steps and involve multi-state transitions"
    confidence: "high"
  - description: "Detection harder for deep layers (memory, communication) vs shallow (perception)"
    chunk_ref: "4:134-142"
    quote: "memory and communication are part of the deeper layers...more challenging"
    confidence: "high"
  - description: "Asynchronous scheduling causes information loss and overload issues"
    chunk_ref: "2:462-466"
    quote: "agents may encounter issues of information loss and information overload"
    confidence: "high"
  - description: "Network topology updates often suffer from delays and poor coordination"
    chunk_ref: "2:490-493"
    quote: "recently proposed strategies...often suffer from delayed updates"
    confidence: "high"

related_pattern:
  - name: "CoT to ToT"
    relationship: "extension"
    note: "ToT builds on CoT with parallel path exploration"
    chunk_ref: "3:189-191"
  - name: "Self-verification vs Validator Assistance"
    relationship: "alternative"
    note: "Internal vs external validation approaches"
    chunk_ref: "4:9-14"
  - name: "Knowledge Editing vs Unlearning"
    relationship: "alternative"
    note: "Edit vs remove erroneous internal knowledge"
    chunk_ref: "3:201-285"
---

# LLM-based Agents Suffer from Hallucinations: A Survey - Analysis Index

## Paper Overview

- **Source**: 18-HallucinationSurvey-2509.18970.pdf
- **Chunks**: 8 chunks, ~42,373 estimated tokens
- **Analyzed**: 2025-12-28
- **Relevance**: HIGH - Comprehensive survey on agent hallucinations directly addressing multi-agent communication, verification patterns, and quality mechanisms

## Key Extractions

This survey paper is highly relevant to the dynamic subagent research question. It provides a formal taxonomy of hallucinations in LLM-based agents and multi-agent systems, along with mitigation and detection strategies that directly inform handover protocol design.

### Pattern Definitions

| Pattern | Source | Quote |
|---------|--------|-------|
| Multi-Agent Communication Loop | Chunk 1:419-428 | "Reasoning-Execution-Broadcasting-Feedback-Environment Transition..." |
| Structured Message Format | Chunk 2:468-471 | "Adopting structured formats (e.g., JSON) can improve clarity..." |
| Fault-tolerant Design | Chunk 2:471-474 | "robust Fault-tolerant Design, incorporating confirmation conditions" |
| Self-verification Mechanism | Chunk 3:403-433 | "agents assess the validity and reliability of their own outputs" |
| External Validator Pattern | Chunk 3:436-443 | "leverages external validators to verify correctness" |
| Lightweight Checkpoint Injection | Chunk 4:186-189 | "checkpoints can be injected at each stage to verify" |

### Verification Mechanisms

| Mechanism | Type | Source | Description |
|-----------|------|--------|-------------|
| Self-reflection | verification | Chunk 4:22-25 | Agents revisit and critique outputs through introspection |
| Self-consistency | verification | Chunk 4:28-32 | Multiple outputs aggregated via majority voting |
| Self-questioning | detection | Chunk 4:33-35 | Agent poses verification questions about reasoning |
| Language-based Validators | verification | Chunk 4:46-48 | Atomic fact decomposition and entailment checking |
| Retrieval-based Validators | verification | Chunk 4:104-106 | Verify against external sources |
| Execution-based Validators | verification | Chunk 4:106-108 | Run code/plans to verify correctness |
| Simulation-based Validators | verification | Chunk 4:108-111 | Test in sandboxed environments |
| Ensemble Validators | verification | Chunk 4:112-116 | Cross-verification with multiple validators |

### Failure Modes

| Failure Mode | Source | Description |
|--------------|--------|-------------|
| Erroneous Message Propagation | Chunk 2:441-448 | Inaccurate facts or misleading inferences in messages |
| Hallucination Accumulation | Chunk 4:153-160 | Minor issues amplify over multi-step processes |
| Echo Chamber Effect | Chunk 8:192-205 | Telephone game style distortion in message chains |
| Content Redundancy | Chunk 2:448-451 | Repetitive content obscures critical signals |
| Information Asymmetry | Chunk 2:451-456 | Different information access causes bias |

### Key Findings (with evidence)

- **POMDP Framework for Agents** (Chunk 1:285-340): "The interaction dynamics between the agent and the learning environment is usually formulated as a Partially Observable Markov Decision Process (POMDP)"
- **Structured Formats Reduce Errors** (Chunk 2:468-471): "Adopting structured formats (e.g., JSON) can improve clarity and rigor of expression, which mitigates the risk of miscommunication"
- **Three Mitigation Categories** (Chunk 3:106-112): "Knowledge Utilization, Paradigm Improvement, and Post-hoc Verification"
- **Checkpoint Pattern for Detection** (Chunk 4:186-189): "lightweight checkpoints can be injected at each stage to verify whether hallucinations have occurred"

## Chunk Navigation

### Chunk 1: Introduction and Agent Formalization
- **Summary**: Introduces the paper's scope, defines LLM-based agents using POMDP framework, describes the agent loop (Reasoning-Execution-Feedback-Perception-Memorization-Belief Update), and introduces MAS extensions (Broadcasting, Structure Evolution).
- **Key concepts**: [Agent Hallucinations, POMDP, Belief State, Multi-Agent System, Broadcasting, Structure Evolution]
- **Key quotes**:
  - Line 81-90: "LLM-based Agents are becoming increasingly proficient in task automation"
  - Line 192-205: "agent hallucinations...More Diverse Types, Longer Propagation Chains, More Severe Consequences"
  - Line 419-428: "Reasoning-Execution-Broadcasting-Feedback-Environment Transition-Perception-Memorization-Belief Update-Structure Evolution"
- **Load when**: User asks about agent architecture, multi-agent loops, belief states, or formal agent definitions

### Chunk 2: Taxonomy of Agent Hallucinations
- **Summary**: Presents the five-type hallucination taxonomy (Reasoning, Execution, Perception, Memorization, Communication). Details causes including problematic objective expression, tool documentation limitations, communication protocol issues.
- **Key concepts**: [Reasoning Hallucinations, Execution Hallucinations, Perception Hallucinations, Memorization Hallucinations, Communication Hallucinations, Tool Selection, Message Formats]
- **Key quotes**:
  - Line 457-474: "Communication protocols govern how agents exchange messages"
  - Line 468-471: "Adopting structured formats (e.g., JSON) can improve clarity"
  - Line 471-474: "Fault-tolerant Design, incorporating confirmation conditions"
- **Load when**: User asks about hallucination types, communication protocols, message formats, or tool-related errors

### Chunk 3: Mitigation Methods
- **Summary**: Reviews hallucination mitigation approaches: Knowledge Utilization (External Knowledge Guidance, Internal Knowledge Enhancement), Paradigm Improvement (Contrastive Learning, Curriculum Learning, RL, Causal Learning, Graph Learning, Decoding Optimization), Post-hoc Verification.
- **Key concepts**: [Knowledge Utilization, Paradigm Improvement, Post-hoc Verification, Chain-of-Thought, Tree-of-Thought, Contrastive Learning, Self-verification, Validator Assistance]
- **Key quotes**:
  - Line 185-189: "Chain-of-Thought guides the agent to break down complex problems"
  - Line 189-194: "Tree-of-Thought explores and evaluates multiple reasoning paths in parallel"
  - Line 395-402: "Post-hoc Verification focuses on monitoring and evaluating outputs after task execution"
- **Load when**: User asks about hallucination mitigation, prompt engineering techniques, verification strategies, or learning paradigms

### Chunk 4: Detection Methods and Future Directions
- **Summary**: Covers hallucination detection approaches, self-verification mechanisms (self-reflection, self-consistency, self-questioning), external validators, and future research directions including hallucinatory accumulation investigation and checkpoint injection.
- **Key concepts**: [Hallucination Detection, Self-verification, Self-reflection, Self-consistency, Self-questioning, Language-based Validators, Retrieval-based Validators, Execution-based Validators, Checkpoint Injection]
- **Key quotes**:
  - Line 17-39: "Self-verification is a lightweight and model-internal approach"
  - Line 153-160: "hallucinations can accumulate and amplify over time"
  - Line 186-189: "lightweight checkpoints can be injected at each stage"
- **Load when**: User asks about detection methods, self-verification, checkpoint patterns, or future research directions

### Chunk 5: References (Part 1)
- **Summary**: Bibliography entries 27-134, covering safety benchmarks, hallucination surveys, tool learning, and memory management.
- **Key concepts**: [References, Citations]
- **Load when**: User needs specific citation details from references 27-134

### Chunk 6: References (Part 2)
- **Summary**: Bibliography entries 113-220, covering memory systems, multi-agent collaboration, communication protocols, and world models.
- **Key concepts**: [References, Citations]
- **Load when**: User needs specific citation details from references 113-220

### Chunk 7: References (Part 3)
- **Summary**: Bibliography entries 199-279, covering reinforcement learning, graph learning, hallucination detection, and architectural improvements.
- **Key concepts**: [References, Citations]
- **Load when**: User needs specific citation details from references 199-279

### Chunk 8: Appendix - MAS Loop and Hallucination Examples
- **Summary**: Appendix A: Formal definition of LLM-based MAS loop with equations. Appendix B: Concrete examples of each hallucination type with explanations.
- **Key concepts**: [MAS Loop Formalization, Broadcasting, Structure Evolution, Hallucination Examples, Echo Chamber Effect]
- **Key quotes**:
  - Line 7-14: "each LLM-based agent in the MAS must communicate with other agents"
  - Line 30-37: "Broadcasting: The agent broadcasts its message to its neighbors"
  - Line 192-205: "echo chamber effect...telephone game style accumulation of deviations"
- **Load when**: User asks about MAS formalization, broadcast mechanics, or concrete hallucination examples
