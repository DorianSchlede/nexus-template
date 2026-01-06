---
paper_id: "09-SEMAP-2510.12120"
title: "Towards Engineering Multi-Agent LLMs: A Protocol-Driven Approach"
authors:
  - "Zhenyu Mao"
  - "Jacky Keung"
  - "Fengji Zhang"
  - "Shuo Liu"
  - "Yifei Wang"
  - "Jialong Li"
year: 2025
chunks_expected: 2
chunks_read: 2
analysis_complete: true
high_priority_fields_found: 6
schema_version: "2.3"

chunk_index:
  1:
    token_count: 6048
    fields_found:
      pattern_definition: true
      mechanism_type: true
      failure_mode: true
      implementation_detail: true
      integration_point: true
      quality_metric: true
      limitation: partial
      related_pattern: true
  2:
    token_count: 1935
    fields_found:
      pattern_definition: partial
      mechanism_type: false
      failure_mode: false
      implementation_detail: false
      integration_point: false
      quality_metric: true
      limitation: true
      related_pattern: false

pattern_definition:
  - name: "Explicit Behavioral Contract Modeling"
    purpose: "Formalize agent responsibilities via pre/post-conditions to reduce under-specification"
    mechanism: "Contract tuple C = (name, IC, OC) specifying input/output artifacts"
    source: "Chunk 1:175-208"
    quote: "each agent is modeled through an explicit behavioral contract..."
    confidence: "high"
  - name: "Structured Messaging"
    purpose: "Standardize inter-agent communication to prevent coordination misalignment"
    mechanism: "Message tuple M = (sender, receiver, CM) with schema-designated payload"
    source: "Chunk 1:210-231"
    quote: "Each message M is formalized as: M = (sender, receiver, CM)..."
    confidence: "high"
  - name: "Lifecycle-Guided Execution with Verification"
    purpose: "Structure collaboration as FSM with verification gates to ensure output validity"
    mechanism: "FSM L = (S, Sigma, delta, s0, F) with verification-gated transitions"
    source: "Chunk 1:238-266"
    quote: "task lifecycle is modeled as a finite state machine (FSM)..."
    confidence: "high"

mechanism_type:
  - type: "verification"
    description: "Verification-driven state transitions ensure output correctness"
    source: "Chunk 1:168-172"
    quote: "ensures output correctness and guards against premature termination"
  - type: "enforcement"
    description: "Contracts enforce preconditions and postconditions on agent behavior"
    source: "Chunk 1:160-162"
    quote: "formalizes agent responsibilities through preconditions and post-conditions"
  - type: "detection"
    description: "FSM detects failures and triggers recovery or reassignment"
    source: "Chunk 1:246-247"
    quote: "failures can trigger appropriate recovery or reassignment actions"

failure_mode:
  - mode: "Under-specification"
    description: "Poorly defined agent responsibilities and role boundaries"
    source: "Chunk 1:69-73"
    quote: "inadequate component design, where agent responsibilities are poorly defined"
  - mode: "Coordination misalignment"
    description: "Inter-agent communication lacks semantic structure or typed formats"
    source: "Chunk 1:74-76"
    quote: "insufficient interface specification, where inter-agent communication lacks semantic structure"
  - mode: "Task verification failure"
    description: "System progresses without formal gating or validation"
    source: "Chunk 1:76-78"
    quote: "inappropriate transition logic, where the system progresses without formal gating"

implementation_detail:
  - type: "tuple"
    name: "Behavioral Contract C"
    description: "C = (name, IC, OC) where IC=input artifacts, OC=output artifacts"
    source: "Chunk 1:194-207"
  - type: "tuple"
    name: "Message M"
    description: "M = (sender, receiver, CM) with schema-designated payload objects"
    source: "Chunk 1:217-231"
  - type: "fsm"
    name: "Task Lifecycle L"
    description: "L = (S, Sigma, delta, s0, F) for verification-gated stage transitions"
    source: "Chunk 1:248-265"
  - type: "infrastructure"
    name: "A2A Protocol Base"
    description: "HTTP-based APIs with JSON-RPC 2.0, Agent Cards for capability discovery"
    source: "Chunk 1:137-146"

integration_point:
  - point: "prompt_generation"
    description: "Input contracts (IC) define minimal artifacts agent requires"
    source: "Chunk 1:184-191"
  - point: "execution"
    description: "FSM structures agent collaboration during task execution"
    source: "Chunk 1:245-246"
  - point: "verification"
    description: "Transitions gated by validation; failures trigger recovery"
    source: "Chunk 1:246-247"
  - point: "handover"
    description: "Structured messaging ensures semantic clarity in agent transfers"
    source: "Chunk 1:213-216"

quality_metric:
  - metric: "Total failure reduction (function-level)"
    value: "69.6%"
    baseline: "112 to 34 failures with DeepSeek"
    source: "Chunk 1:344-346"
  - metric: "Total failure reduction (deployment-level)"
    value: "56.7%"
    baseline: "67 to 29 failures with DeepSeek"
    source: "Chunk 1:348-351"
  - metric: "Under-specification reduction"
    value: "73.0%"
    baseline: "63 to 17 failures"
    source: "Chunk 1:346-348"
  - metric: "Inter-agent misalignment elimination"
    value: "100%"
    baseline: "8 to 0 failures in ProgramDev/DeepSeek"
    source: "Chunk 1:351"
  - metric: "Python vulnerability detection"
    value: "47.4% reduction"
    baseline: "38 to 20 failures"
    source: "Chunk 1:355-357"
  - metric: "C/C++ vulnerability detection"
    value: "28.2% reduction"
    baseline: "78 to 56 failures"
    source: "Chunk 1:353-355"

limitation:
  - "Needs scaling to larger datasets, agent populations, and longer workflows (Chunk 2:15-17)"
  - "Resource overhead not measured (Chunk 2:19)"
  - "Missing formal protocol correctness verification (Chunk 2:19-20)"
  - "Ablation studies needed to isolate component impacts (Chunk 2:17-18)"

related_pattern:
  - name: "A2A (Agent-to-Agent) Protocol"
    relationship: "foundation"
    note: "SEMAP built as middleware atop Google A2A (Chunk 1:89-90)"
  - name: "Design by Contract (DbC)"
    relationship: "inspiration"
    note: "Behavioral contracts inspired by DbC principle (Chunk 1:160-162)"
  - name: "Finite State Machine (FSM)"
    relationship: "implementation_basis"
    note: "Task lifecycle modeled as FSM (Chunk 1:248)"
  - name: "MetaGPT Framework"
    relationship: "baseline_comparison"
    note: "Baseline system uses MetaGPT (Chunk 1:315-317)"
---

# Towards Engineering Multi-Agent LLMs: A Protocol-Driven Approach - Analysis Index

## Paper Overview

- **Source**: 09-SEMAP-2510.12120.pdf
- **Chunks**: 2 chunks, ~7983 estimated tokens
- **Analyzed**: 2025-12-28
- **Authors**: Mao, Keung, Zhang, Liu, Wang, Li (City University of Hong Kong, Waseda University)

## Key Extractions

This paper introduces SEMAP (Software Engineering Multi-Agent Protocol), a protocol-layer methodology that addresses three core deficiencies in multi-agent LLM systems: under-specification, coordination misalignment, and inappropriate verification. SEMAP instantiates SE-inspired principles through behavioral contracts, structured messaging, and lifecycle-guided execution with verification gates.

The paper is highly relevant to handover patterns research as it provides formal definitions for agent-to-agent communication structures and demonstrates quantified improvements in failure reduction. SEMAP achieves up to 69.6% failure reduction in function-level development and 100% elimination of inter-agent misalignment in some configurations.

### Pattern Definitions

| Pattern | Purpose | Mechanism | Source |
|---------|---------|-----------|--------|
| Behavioral Contract Modeling | Reduce under-specification | C = (name, IC, OC) tuple | Chunk 1:175-208 |
| Structured Messaging | Prevent coordination misalignment | M = (sender, receiver, CM) tuple | Chunk 1:210-231 |
| Lifecycle-Guided Execution | Ensure output validity | FSM with verification gates | Chunk 1:238-266 |

### Quality Metrics

| Metric | Improvement | Context | Source |
|--------|-------------|---------|--------|
| Function-level development failures | -69.6% | DeepSeek, HumanEval | Chunk 1:344-346 |
| Deployment-level failures | -56.7% | DeepSeek, ProgramDev | Chunk 1:348-351 |
| Under-specification failures | -73.0% | DeepSeek | Chunk 1:346-348 |
| Inter-agent misalignment | -100% | DeepSeek, ProgramDev | Chunk 1:351 |
| Python vulnerability detection | -47.4% | ChatGPT, vudenc100 | Chunk 1:355-357 |

### Key Findings (with evidence)

- **Behavioral contracts reduce under-specification** (Chunk 1:160-165): "Explicit behavioral contract modeling, inspired by DbC, formalizes agent responsibilities through preconditions and post-conditions. This reduces ambiguity..."
- **Structured messaging prevents misalignment** (Chunk 1:166-168): "Structured messaging enforces semantically typed inter-agent messaging to ensure clarity, completeness, and coordination alignment"
- **FSM-based verification enables recovery** (Chunk 1:246-247): "task progression is gated by validation and failures can trigger appropriate recovery or reassignment actions"

## Chunk Navigation

### Chunk 1: Core Methodology and Evaluation Results

- **Summary**: Contains the complete SEMAP methodology including the three core principles (behavioral contracts, structured messaging, lifecycle-guided execution), formal definitions (C, M, L tuples), experimental setup, and quantitative results showing 69.6% failure reduction.
- **Key concepts**: [SEMAP, behavioral contract, structured messaging, FSM lifecycle, A2A protocol, verification gates, under-specification, coordination misalignment]
- **Key quotes**:
  - Line 22-23: "SEMAP instantiates three core SE design principles for multi-agent LLMs"
  - Line 160-162: "Explicit behavioral contract modeling, inspired by the principle of Design by Contract (DbC), formalizes agent responsibilities"
  - Line 194: "C = (name, IC, OC)"
  - Line 220: "M = (sender, receiver, CM)"
  - Line 251: "L = (S, Sigma, delta, s0, F)"
- **Load when**: "User asks about SEMAP protocol", "Query about behavioral contracts in multi-agent systems", "Looking for structured messaging patterns", "FSM-based agent coordination", "Multi-agent failure taxonomy"

### Chunk 2: Conclusion, References, and Results Tables

- **Summary**: Contains the conclusion summary, future work directions (ablation studies, resource overhead measurement, formal verification), complete reference list, and the results tables (Table I for development tasks, Table II for vulnerability detection).
- **Key concepts**: [limitations, future work, ablation studies, resource overhead, formal verification, MetaGPT baseline, HumanEval, ProgramDev, vulnerability detection]
- **Key quotes**:
  - Line 3-4: "SEMAP, a protocol-layer methodology for addressing common failures in multi-agent LLMs"
  - Line 17-18: "Ablation studies will isolate the impact of contracts, messaging, and lifecycle control"
  - Line 19: "Future work also includes measuring resource overhead"
- **Load when**: "User asks about SEMAP limitations", "Query about evaluation metrics", "Looking for failure reduction percentages", "Multi-agent LLM benchmarks"
