---
paper_id: "21-LLM_Smart_Contracts_from_BPMN"
title: "On LLM-Assisted Generation of Smart Contracts from Business Processes"
authors:
  - "Fabian Stiehle"
  - "Hans Weytjens"
  - "Ingo Weber"
year: 2025
chunks_expected: 1
chunks_read: 1
analysis_complete: true
high_priority_fields_found: 6

# Extraction fields
entity_types: "N/A - Paper focuses on LLM code generation evaluation, not ontology design"
entity_definitions: "N/A - No formal entity definitions provided"
entity_relationships: "N/A - Paper evaluates code generation, not ontological relationships"
abstraction_level: "N/A - Not an ontology paper"

framework_comparison:
  - compared_to: "Traditional rule-based code generation"
    relationship: "evaluates_alternative"
    details: "LLMs outperform traditional rule-based approaches in code-to-code translation but lack reliability for smart contracts"
    source: "Chunk 1:54-61"
  - compared_to: "Proprietary vs Open-source LLMs"
    relationship: "compares"
    details: "Proprietary models (GPT-4.1, Claude Sonnet 4, Grok 3) generally outperform open-source (Llama, DeepSeek, Qwen) but introduce data sovereignty risks"
    source: "Chunk 1:164-170"

ai_integration:
  - pattern: "BPMN-to-Solidity code generation"
    description: "LLMs transform BPMN 2.0 choreography models into executable Solidity smart contracts for EVM blockchain"
    source: "Chunk 1:92-100"
  - pattern: "Automated evaluation framework"
    description: "Framework generates conforming/non-conforming traces to benchmark LLM-generated smart contract correctness"
    source: "Chunk 1:230-241"
  - pattern: "LLM integration in BPM lifecycle"
    description: "LLMs evaluated across modeling, prediction, automation phases of business process management"
    source: "Chunk 1:180-186"

agent_modeling:
  - aspect: "Participant-to-address mapping"
    description: "Participants in choreography mapped to blockchain addresses (participantIDs) for resource allocation enforcement"
    source: "Chunk 1:313-314"
  - aspect: "Task initiator enforcement"
    description: "Smart contracts enforce that only designated participants can execute specific tasks"
    source: "Chunk 1:467-468"

agentic_workflows: "N/A - Paper focuses on single-LLM code generation, not multi-agent orchestration"

generative_ai_patterns:
  - pattern: "Zero-shot prompting"
    description: "Models complete tasks based solely on instructions without prior examples"
    source: "Chunk 1:145-147"
  - pattern: "Few-shot prompting (one-shot, two-shot)"
    description: "Providing illustrative examples within input; tested one-shot and two-shot variants"
    source: "Chunk 1:145-147, 464-470"
  - pattern: "Temperature control"
    description: "Set to 0 for quasi-deterministic outputs; lower values produce more predictable results"
    source: "Chunk 1:171-174, 478"
  - pattern: "Token-based processing"
    description: "Input/output as tokens influences computational load; model size (parameters) affects performance"
    source: "Chunk 1:148-163"

agent_ontology_integration: "N/A - Paper does not address ontology-guided LLM reasoning"

entity_count: null
methodology: "empirical"

empirical_evidence:
  - type: "Large-scale benchmark"
    description: "165 BPMN choreography models from SAP-SAM dataset (filtered from 4,096 models)"
    source: "Chunk 1:386-394, 417-421"
  - type: "Multi-model comparison"
    description: "7 LLMs tested (GPT-4.1, Claude Sonnet 4, Grok 3, Llama-3.1-405b, Llama-3.3-70b, DeepSeek-V3, Qwen3-235b)"
    source: "Chunk 1:437-452"
  - type: "Trace replay validation"
    description: "2,500 conforming traces + 50 non-conforming traces per model for F1 score calculation"
    source: "Chunk 1:529-530"
  - type: "Reproducible benchmark"
    description: "Open-source framework with archived data (GitHub + Zenodo DOI)"
    source: "Chunk 1:245-246"

limitations:
  - "LLM outputs inherently non-deterministic - unreliable for consistent behavior (Chunk 1:67-69)"
  - "F1 scores of 0.8-0.9 insufficient for production blockchain where 100% reliability required (Chunk 1:638-649)"
  - "Even 2% error rate unacceptable for financial risks and immutable transactions (Chunk 1:646-648)"
  - "Security vulnerabilities can be introduced by LLM-generated code (Chunk 1:66-67)"
  - "Proprietary models raise confidentiality, privacy, autonomy concerns (Chunk 1:71-75)"
  - "Current LLM architectures cannot resolve fundamental reliability issue (Chunk 1:648-649)"
  - "Prompt may not be optimal; same prompt used across all LLMs (Chunk 1:677-679)"

tools_standards:
  - "BPMN 2.0 Choreographies"
  - "Solidity (smart contract language)"
  - "EVM (Ethereum Virtual Machine)"
  - "Chorpiler (BPMN-to-smart-contract transformer)"
  - "pm4py (Python process mining library)"
  - "Hardhat (Ethereum development framework)"
  - "OpenRouter (unified LLM API)"
  - "Mocha (JavaScript test framework)"
  - "Petri nets (interaction net representation)"
---

# On LLM-Assisted Generation of Smart Contracts from Business Processes - Analysis Index

## Paper Overview

- **Source**: 21-LLM_Smart_Contracts_from_BPMN.pdf
- **Chunks**: 1 chunk, ~12,232 estimated tokens
- **Analyzed**: 2025-12-28
- **Authors**: Fabian Stiehle, Hans Weytjens, Ingo Weber (TU Munich, Fraunhofer)
- **Keywords**: Blockchain, Process Execution, Workflow, Large language models, Generative AI

## Key Extractions

This paper presents an empirical study benchmarking LLM capabilities for generating smart contract code from BPMN choreography models. The research addresses a gap in LLM evaluation for blockchain-based process execution, where prior work relied on small samples and manual inspection.

### AI Integration Patterns

| Pattern | Source | Quote |
|---------|--------|-------|
| BPMN-to-Solidity generation | Chunk 1:92-100 | "We introduce an automated evaluation framework for generating smart contract code from process models" |
| Trace-based validation | Chunk 1:238-241 | "From a given process model, it generates conforming traces...and non-conforming traces" |
| BPM lifecycle integration | Chunk 1:180-186 | "Vidgof et al. outline opportunities and challenges of integrating LLM-based tools within the BPM lifecycle" |

### Generative AI Patterns

| Pattern | Source | Quote |
|---------|--------|-------|
| Zero-shot prompting | Chunk 1:145-147 | "models complete tasks based solely on instructions without prior examples" |
| Few-shot prompting | Chunk 1:145-147, 464-470 | "providing illustrative examples directly within the input" |
| Temperature=0 for determinism | Chunk 1:171-174, 478 | "lower temperatures make outputs more predictable and focused" |

### Framework Comparison

| Compared To | Relationship | Details | Source |
|-------------|--------------|---------|--------|
| Rule-based code generation | evaluates_alternative | LLMs more flexible but less reliable | Chunk 1:54-61 |
| Proprietary vs Open-source | compares | Trade-off between performance and data sovereignty | Chunk 1:164-170 |

### Empirical Results (Key Findings)

| Model | F1 Score | Compilability | Cost/Process |
|-------|----------|---------------|--------------|
| Grok 3 (one-shot) | 0.918 | 100% | $0.044 |
| Claude Sonnet 4 (one-shot) | 0.862 | 100% | $0.046 |
| GPT-4.1 (one-shot) | 0.797 | 99.4% | $0.028 |
| Llama-3.3-70b (one-shot) | 0.399 | 90.4% | $0.001 |

Source: Chunk 1:575-608 (Table 2)

### Limitations (Critical for Smart Contracts)

- **Non-determinism**: LLM outputs inherently stochastic (Chunk 1:67-69)
- **Reliability gap**: Even 98% F1 = 2% error rate unacceptable for immutable blockchain transactions (Chunk 1:638-649)
- **Fundamental issue**: "We do not see a way in which this fundamental issue could be resolved with current LLM architectures" (Chunk 1:648-649)
- **Security**: LLM-generated code can introduce vulnerabilities (Chunk 1:66-67)

## Chunk Navigation

### Chunk 1: Complete Paper (Lines 1-838)

- **Summary**: Full paper covering LLM-based smart contract generation from BPMN choreographies. Introduces benchmarking framework, tests 7 LLMs on 165 process models, reports F1 scores and costs. Concludes that current LLMs lack the perfect reliability required for blockchain deployment.

- **Key concepts**: [BPMN choreography, Solidity smart contracts, LLM benchmarking, F1 score evaluation, zero-shot/few-shot prompting, EVM blockchain, SAP-SAM dataset, Chorpiler, process trace replay]

- **Key quotes**:
  - Line 12-14: "Large language models (LLMs) have changed the reality of how software is produced..."
  - Line 109-115: "our results indicate good performance of some models, with those achieving F1 scores of 0.8 or more. Due to the stochastic nature of LLMs, output remains imperfect and unreliable"
  - Line 648-649: "We do not see a way in which this fundamental issue could be resolved with current LLM architectures"
  - Line 701-704: "we propose future work to explore responsible LLM integrations in existing tools for code generation, focusing on using LLMs for verification and enhancing current code generation tools rather than replacing them entirely"

- **Load when**:
  - "User asks about LLM code generation from BPMN"
  - "Query about smart contract generation reliability"
  - "Comparing LLM performance on code generation tasks"
  - "Blockchain process execution with AI"
  - "LLM benchmarking methodology"
  - "Generative AI for software engineering"
  - "BPMN-to-Solidity transformation"

## Synthesis Notes

### For Ontology Research Questions

This paper is **tangentially relevant** to the ontology research questions:

1. **Entity types/definitions**: Not applicable - paper does not propose ontological structures
2. **Framework comparison**: Useful for understanding LLM vs rule-based code generation trade-offs
3. **AI integration**: High relevance - demonstrates concrete LLM integration pattern for process execution
4. **Generative AI patterns**: High relevance - detailed coverage of prompting strategies and temperature control
5. **Limitations**: Critical insight - LLM non-determinism fundamentally incompatible with blockchain's reliability requirements

### Key Insight for Multi-Agent Systems

The paper recommends LLMs be integrated as **assistive tools within existing systems** rather than autonomous generators:
- Generate code snippets for human/tool verification
- Generate test cases and vulnerability checks
- Extend rule-based tools with learned heuristics
- This pattern parallels "human-in-the-loop" agentic workflow design

### Cross-Paper Connections

- Relates to papers on process mining (OCEL, pm4py usage)
- Connects to BPM lifecycle integration literature (Vidgof et al.)
- Relevant to smart contract ontology design (participant-task-gateway structures)
