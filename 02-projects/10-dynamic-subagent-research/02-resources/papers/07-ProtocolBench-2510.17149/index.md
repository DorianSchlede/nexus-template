---
# REQUIRED METADATA
paper_id: "07-ProtocolBench-2510.17149"
title: "Which LLM MultiAgent Protocol to Choose? ProtocolBench"
authors:
  - "Hongyi Du"
  - "Jiaqi Su"
  - "Jisen Li"
  - "Lijie Ding"
  - "Yingxuan Yang"
  - "Peixuan Han"
  - "Xiangru Tang"
  - "Kunlun Zhu"
  - "Jiaxuan You"
year: 2025
chunks_expected: 8
chunks_read: 8
analysis_complete: true
schema_version: "2.3"
high_priority_fields_found: 6

# CHUNK-LEVEL FIELD ASSESSMENT
chunk_index:
  1:
    token_count: 5236
    fields_found:
      pattern_definition: true
      mechanism_type: partial
      failure_mode: false
      implementation_detail: partial
      integration_point: true
      quality_metric: true
      limitation: partial
      related_pattern: false
  2:
    token_count: 5185
    fields_found:
      pattern_definition: true
      mechanism_type: true
      failure_mode: partial
      implementation_detail: partial
      integration_point: true
      quality_metric: true
      limitation: true
      related_pattern: partial
  3:
    token_count: 5989
    fields_found:
      pattern_definition: partial
      mechanism_type: partial
      failure_mode: false
      implementation_detail: true
      integration_point: true
      quality_metric: true
      limitation: true
      related_pattern: false
  4:
    token_count: 4713
    fields_found:
      pattern_definition: partial
      mechanism_type: true
      failure_mode: true
      implementation_detail: true
      integration_point: true
      quality_metric: partial
      limitation: partial
      related_pattern: false
  5:
    token_count: 3667
    fields_found:
      pattern_definition: true
      mechanism_type: partial
      failure_mode: true
      implementation_detail: partial
      integration_point: partial
      quality_metric: false
      limitation: false
      related_pattern: false
  6:
    token_count: 3760
    fields_found:
      pattern_definition: true
      mechanism_type: true
      failure_mode: partial
      implementation_detail: true
      integration_point: true
      quality_metric: false
      limitation: true
      related_pattern: true
  7:
    token_count: 4505
    fields_found:
      pattern_definition: true
      mechanism_type: partial
      failure_mode: partial
      implementation_detail: true
      integration_point: partial
      quality_metric: false
      limitation: false
      related_pattern: true
  8:
    token_count: 2280
    fields_found:
      pattern_definition: partial
      mechanism_type: false
      failure_mode: false
      implementation_detail: partial
      integration_point: false
      quality_metric: true
      limitation: false
      related_pattern: false

# EXTRACTION FIELDS
pattern_definition:
  - name: "Protocol Adapter Pattern"
    purpose: "Normalize communication across different protocols"
    mechanism: "Encode/decode bridges with field mappings, retries, streaming semantics"
    chunk_ref: "1:110-116"
    quote: "Protocol Adapters that normalize envelopes, field mappings..."
    confidence: "high"

  - name: "Unified Transport Envelope (UTE)"
    purpose: "Enable cross-protocol interoperability with standard message format"
    mechanism: "Universal envelope with src, dst, content, context fields; ENCODE_TABLE/DECODE_TABLE transformation"
    chunk_ref: "6:51-59"
    quote: "Minimal required fields: src, dst, content, context..."
    confidence: "high"

  - name: "ProtocolRouter Dynamic Selection"
    purpose: "Select optimal protocol per-scenario or per-module"
    mechanism: "Learned selection based on requirements and runtime signals"
    chunk_ref: "1:113-116"
    quote: "learned protocol router that selects per-scenario protocols..."
    confidence: "high"

  - name: "Stateless Bridge Pattern"
    purpose: "Enable heterogeneous protocol links without state overhead"
    mechanism: "Syntactic envelope/field mapping translation only; no business content or security attribute changes"
    chunk_ref: "2:18-21"
    quote: "translation is purely syntactic (envelope/field mapping)..."
    confidence: "high"

  - name: "Hard Constraint Filtering"
    purpose: "Pre-filter incompatible protocols before selection"
    mechanism: "Priority-based filtering: identity/E2E -> operation semantics -> interaction preferences"
    chunk_ref: "5:80-85"
    quote: "Hard constraints first prune incompatible candidates..."
    confidence: "high"

  - name: "Scenario Harness Pattern"
    purpose: "Standardize protocol evaluation across test scenarios"
    mechanism: "Fixed topologies and workloads with unified logging/metrics"
    chunk_ref: "1:338-340"
    quote: "Scenario Harness that fixes topologies and workloads..."
    confidence: "high"

mechanism_type:
  - type: "verification"
    context: "Protocol selection must satisfy hard requirements"
    chunk_ref: "2:36-44"
    quote: "router must choose the correct protocol for each module under explicit hard requirements"

  - type: "detection"
    context: "Failure detection via heartbeats/timeouts"
    chunk_ref: "4:214-218"
    quote: "Agents detect failures via timeouts or heartbeat checks..."

  - type: "enforcement"
    context: "Error normalization via PAL taxonomy"
    chunk_ref: "6:85-87"
    quote: "Adapter exceptions are normalized by PAL into: E_TIMEOUT, E_HTTP, E_CONN..."

failure_mode:
  - mode: "List-wise exclusion for malformed protocol selection"
    chunk_ref: "5:103-106"
    quote: "entire scenario is list-wise excluded and the exclusion is logged; no zero-filling"

  - mode: "Ring skip on agent failure with recovery measurement"
    chunk_ref: "4:184-187"
    quote: "Upon detecting a failed target agent, messages skip it and forward to the next in the ring"

implementation_detail:
  - type: "class"
    name: "BaseAgent"
    description: "Dual-role agent: server (receives) and multi-client (sends)"
    chunk_ref: "6:14-18"
    quote: "BaseAgent (dual role): Acts as a server and as a multiclient"

  - type: "class"
    name: "BaseProtocolAdapter"
    description: "Per-edge adapter for isolation and metering"
    chunk_ref: "6:21-24"
    quote: "One adapter instance per egress edge for isolation and precise metering"

  - type: "dataclass"
    name: "UTE"
    description: "Universal message envelope with src, dst, content, context"
    chunk_ref: "6:51-59"
    quote: "Minimal required fields: src, dst, content, context"

  - type: "function"
    name: "send_message"
    description: "Sends protocol payload via UTE encoding"
    chunk_ref: "6:35-36"
    quote: "Sends a protocol-specific payload and returns the protocol response"

  - type: "function"
    name: "priority_decide"
    description: "Fixed-priority protocol chooser"
    chunk_ref: "7:94-96"
    quote: "priority_decide(candidates, caps) -> str|List[str]"

integration_point:
  - point: "handover"
    context: "Protocol adapter at agent communication boundaries"
    chunk_ref: "2:18-21"
    quote: "adapters perform encode/decode translation between wire formats"

  - point: "execution"
    context: "Router protocol assignment during runtime"
    chunk_ref: "2:16-17"
    quote: "router emits a protocol assignment per module"

  - point: "verification"
    context: "Post-workflow LLM-based quality evaluation"
    chunk_ref: "3:397-400"
    quote: "LLM summarizer generates outcome; LLM judge evaluates result"

quality_metric:
  - metric: "Task Success Rate (GAIA)"
    values:
      A2A: 9.29
      ACP: 5.25
      ANP: 7.28
      Agora: 6.27
    chunk_ref: "2:161-164"
    quote: "A2A achieves highest success rate of 9.29"

  - metric: "Mean E2E Latency (Streaming Queue)"
    values:
      ACP: "9,663ms"
      A2A: "9,698ms"
      ANP: "11,364ms"
      Agora: "13,135ms"
    chunk_ref: "2:178-181"
    quote: "ACP achieves lowest mean response time of 9,663ms"

  - metric: "Post-Fault Retention (Fail-Storm)"
    values:
      A2A: "98.85%"
      ACP: "92.41%"
      ANP: "86.96%"
      Agora: "81.29%"
    chunk_ref: "2:194-198"
    quote: "A2A maintains 98.85% of pre-failure answer discovery"

  - metric: "Recovery Time Improvement"
    value: "-18.1% (Router: 6.55s vs A2A: 8.00s)"
    chunk_ref: "3:21"
    quote: "Recovery time (s) 6.55 vs 8.00"

  - metric: "Router Selection Accuracy"
    values:
      spec_only_scenario: "53.5%"
      spec_only_module: "71.2%"
      spec_perf_scenario: "63.3%"
      spec_perf_module: "81.7%"
    chunk_ref: "2:372-374"
    quote: "Adding performance priors lifts accuracy to 63.3%"

limitation:
  - text: "No single protocol dominates universally across all scenarios"
    chunk_ref: "3:84-88"
    quote: "no single protocol dominates universally"

  - text: "Router assumes stationary or slowly-changing workload distributions"
    chunk_ref: "3:302-304"
    quote: "assumes stationary or slowly-changing workload distributions"

  - text: "Multiple protocol state maintenance overhead at large scale"
    chunk_ref: "3:302-304"
    quote: "computational overhead could become prohibitive at very large scales"

  - text: "Security-performance tradeoff between protocols"
    chunk_ref: "2:319-321"
    quote: "ACP and A2A offer partial security capabilities"

related_pattern:
  - pattern_1: "Protocol Adapter Pattern"
    pattern_2: "Unified Transport Envelope"
    relationship: "dependency"
    note: "Adapters require UTE for encoding/decoding"
    chunk_ref: "6:35-36"

  - pattern_1: "ProtocolRouter"
    pattern_2: "Hard Constraint Filtering"
    relationship: "dependency"
    note: "Router uses constraint filtering as first selection stage"
    chunk_ref: "5:80-85"
---

# ProtocolBench: Which LLM MultiAgent Protocol to Choose? - Analysis Index

## Paper Overview

- **Source**: 07-ProtocolBench-2510.17149.pdf
- **Chunks**: 8 chunks, ~35,339 estimated tokens
- **Analyzed**: 2025-12-28
- **Category**: Multi-Agent Protocols
- **Institutions**: UIUC, Shanghai Jiao Tong University, Oak Ridge National Lab, Yale

## Key Extractions

This paper introduces **ProtocolBench**, the first systematic benchmark for evaluating LLM multi-agent communication protocols, and **ProtocolRouter**, a dynamic protocol selector. The work directly addresses how protocol choice affects task success, latency, throughput, and fault tolerance in multi-agent systems.

### Pattern Definitions

| Pattern | Purpose | Source |
|---------|---------|--------|
| Protocol Adapter | Normalize envelopes, field mappings, retries across protocols | Chunk 1:110-116 |
| Unified Transport Envelope (UTE) | Standard message format with src, dst, content, context | Chunk 6:51-59 |
| ProtocolRouter | Learned per-module protocol selection | Chunk 1:113-116 |
| Stateless Bridge | Cross-protocol translation without state | Chunk 2:18-21 |
| Hard Constraint Filtering | Pre-filter protocols violating requirements | Chunk 5:80-85 |

### Quality Metrics

| Scenario | Best Protocol | Key Metric |
|----------|---------------|------------|
| GAIA (Task Success) | A2A | 9.29 success avg (27.6% better than next) |
| Streaming Queue (Latency) | ACP | 9,663ms mean (36% faster than Agora) |
| Fail-Storm (Resilience) | A2A | 98.85% retention (vs 81.29% Agora) |
| Safety Tech (Security) | ANP/Agora | Full security matrix coverage |

### Key Findings

- **Finding 1** (Chunk 3:84-88): "No single protocol dominates universally" - protocol selection must be scenario-dependent
- **Finding 2** (Chunk 1:127-131): ProtocolRouter reduces Fail-Storm recovery time by 18.1% vs best single-protocol baseline
- **Finding 3** (Chunk 2:372-374): Adding performance priors to router improves selection accuracy from 53.5% to 63.3%

## Chunk Navigation

### Chunk 1: Introduction and ProtocolBench Design
- **Summary**: Introduces the research problem of protocol selection in multi-agent systems. Presents ProtocolBench covering four evaluation dimensions and four protocols (A2A, ACP, ANP, Agora). Describes the four benchmark scenarios: GAIA, Safety Tech, Streaming Queue, Fail-Storm Recovery.
- **Key concepts**: [ProtocolBench, protocol comparison, A2A, ACP, ANP, Agora, multi-agent communication]
- **Key quotes**:
  - Line 22-26: "ProtocolBench, a benchmark that systematically compares agent protocols along four measurable axes: task success, end-to-end latency, message or byte overhead, and robustness under failures"
  - Line 110-116: "Protocol Adapters that normalize envelopes, field mappings, retries, and streaming semantics"
- **Load when**: "User asks about multi-agent protocol benchmarks" / "Query about A2A vs ACP vs ANP vs Agora comparison"

### Chunk 2: ProtocolRouter Design and Experimental Results
- **Summary**: Details ProtocolRouter's design goals (correct-by-constraints, deterministic, interoperable). Presents experimental results showing A2A excels in task utility, ACP in latency, A2A in fault tolerance, ANP/Agora in security. Introduces ProtocolRouterBench for evaluating router selection quality.
- **Key concepts**: [ProtocolRouter, protocol selection, latency metrics, failure recovery, security capabilities]
- **Key quotes**:
  - Line 36-44: "router must choose the correct protocol for each independent module under explicit hard requirements"
  - Line 161-164: "A2A emerges as the superior protocol for overall task utility"
- **Load when**: "User asks about protocol selection algorithms" / "Query about latency performance across protocols"

### Chunk 3: Router Performance Validation and Conclusion
- **Summary**: Validates router performance against single-protocol baselines. Shows router achieves 6.55s recovery time (vs 8.00s A2A), 9.90 success rate (vs 9.29 A2A). Discusses limitations and future work including edge cases, byzantine failures, scale overhead.
- **Key concepts**: [router validation, recovery time, per-module selection, limitations]
- **Key quotes**:
  - Line 21: "Recovery time (s) 6.55 8.00 (A2A)" - 18.1% improvement
  - Line 84-88: "no single protocol dominates universally"
- **Load when**: "User asks about protocol router performance" / "Query about limitations of protocol selection"

### Chunk 4: GAIA and Safety Tech Implementation Details
- **Summary**: Details GAIA implementation (planner module, agent lifecycle, step-based memory, LLM judging). Describes Safety Tech security testing including TLS attacks, E2E encryption probes, session hijacking, metadata leakage detection.
- **Key concepts**: [GAIA benchmark, planner module, security probing, TLS testing, session protection]
- **Key quotes**:
  - Line 17-19: "LLM judge assesses outcomes using structured prompts and rubric criteria"
  - Line 55-61: "Conducts 3 rounds of TLS downgrade attacks using weak cipher suites"
- **Load when**: "User asks about GAIA document QA implementation" / "Query about security testing in multi-agent systems"

### Chunk 5: Streaming Queue, Fail-Storm, and RouterBench Implementation
- **Summary**: Details Streaming Queue (coordinator-worker load balancing), Fail-Storm (ring topology fault injection), and ProtocolRouterBench (60 scenarios, 180 modules, L1-L5 difficulty). Describes feature facets and evidence mapping for protocol selection.
- **Key concepts**: [streaming queue, fault injection, ring topology, RouterBench, hard constraints]
- **Key quotes**:
  - Line 80-85: "Hard constraints first prune incompatible candidates... identity/E2E -> operation semantics -> interaction"
  - Line 103-106: "If a module record is malformed, the entire scenario is list-wise excluded"
- **Load when**: "User asks about fault tolerance testing" / "Query about protocol selection rules"

### Chunk 6: Protocol Adapter Layer (PAL) Technical Specification
- **Summary**: Specifies PAL architecture with BaseAgent (dual-role), BaseProtocolAdapter (per-edge isolation), UTE (universal envelope), unified API lifecycle (send_message, streaming, initialize, cleanup). Defines error taxonomy and reliability guarantees.
- **Key concepts**: [BaseAgent, BaseProtocolAdapter, UTE, PAL, error taxonomy, idempotency]
- **Key quotes**:
  - Line 51-59: "Minimal required fields: src, dst, content, context. UTE.new(...) produces the envelope"
  - Line 85-87: "exceptions are normalized by PAL into: E_TIMEOUT, E_HTTP, E_CONN, E_PROTOCOL"
- **Load when**: "User asks about protocol adapter implementation" / "Query about universal message envelope design"

### Chunk 7: Router Layer Technical Details
- **Summary**: Complete router specification sitting above PAL. Details deterministic protocol selection with temperature=0, helper interfaces (extract_evidence_spans, priority_decide, pick_by_narrative), cross-protocol bridging, resilience primitives, security posture preservation.
- **Key concepts**: [router layer, deterministic selection, bridging policy, resilience primitives, security]
- **Key quotes**:
  - Line 44-50: "router deterministically selects exactly one protocol per module from {A2A, ACP, ANP, AGORA}"
  - Line 103-106: "enforce 'change transport, not semantics or security'"
- **Load when**: "User asks about deterministic protocol routing" / "Query about cross-protocol bridging"

### Chunk 8: Router Prompts and Performance Data
- **Summary**: Contains full router prompts for Streaming Queue, Fail-Storm, and ProtocolRouterBench scenarios. Includes detailed performance data JSON with metrics for each protocol across GAIA, Streaming Queue, Fail-Storm, and Doctor scenarios.
- **Key concepts**: [router prompts, performance JSON, scenario descriptions, protocol comparison data]
- **Key quotes**:
  - Line 132-135: "quality_avg: {acp: 2.27, a2a: 2.51, anp: 2.14, agora: 2.33}"
  - Line 176-178: "ACP: {total:1000, duration_s:2417, avg_ms:9663, std_ms:1077}"
- **Load when**: "User asks about protocol performance data" / "Query about router prompt design"

## Relevance to Research Question

**High Relevance**: This paper directly addresses multi-agent communication protocols and provides:

1. **Quantified Protocol Trade-offs**: Clear metrics showing when to use each protocol
2. **Adapter Pattern for Handover**: Protocol adapters normalize communication similar to ULTRASEARCH handover patterns
3. **Universal Envelope (UTE)**: Standardized message format analogous to ticket-based handover
4. **Dynamic Selection**: ProtocolRouter demonstrates scenario-aware protocol selection
5. **Failure Recovery Patterns**: Fail-Storm scenario tests fault tolerance mechanisms

**Gap Analysis**: Paper focuses on protocol selection rather than data quality verification within protocols. ULTRASEARCH patterns (3-Point Evidence, Hash Verification) operate at a different abstraction level than ProtocolBench's protocol-level patterns.
