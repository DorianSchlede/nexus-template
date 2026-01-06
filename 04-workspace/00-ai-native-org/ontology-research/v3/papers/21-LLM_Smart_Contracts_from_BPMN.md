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
schema_version: "2.3"

chunk_index:
  1:
    token_count: 11793
    fields_found:
      entity_types: partial
      entity_definitions: partial
      entity_relationships: partial
      entity_count: false
      abstraction_level: true
      framework_comparison: partial
      methodology: true
      ai_integration: true
      agent_modeling: partial
      agentic_workflows: false
      generative_ai_patterns: true
      agent_ontology_integration: partial
      empirical_evidence: true
      limitations: true
      tools_standards: true

entity_types:
  - item: "Choreography Task"
    chunk: 1
    lines: "413-416"
    quote: "Chorpiler supports all basic elements of BPMN Choreographies: Choreography tasks, start and end event, exclusive, event, and parallel gateways, sub choreographies, and loops in the model."
  - item: "Start Event"
    chunk: 1
    lines: "413-416"
    quote: "Chorpiler supports all basic elements of BPMN Choreographies: Choreography tasks, start and end event..."
  - item: "End Event"
    chunk: 1
    lines: "413-416"
    quote: "...start and end event, exclusive, event, and parallel gateways..."
  - item: "Exclusive Gateway (XOR)"
    chunk: 1
    lines: "355-359"
    quote: "As we also want to benchmark data-based exclusive gateways (XOR), we had to extend the playout functionality to generate appropriate data manipulation events."
  - item: "Parallel Gateway"
    chunk: 1
    lines: "413-416"
    quote: "...exclusive, event, and parallel gateways, sub choreographies, and loops..."
  - item: "Event-based Gateway"
    chunk: 1
    lines: "419-420"
    quote: "...one diverging exclusive gateway, 0.1 diverging event-based gateways, and 0.2 diverging parallel gateways..."
  - item: "Sub Choreography"
    chunk: 1
    lines: "413-416"
    quote: "...parallel gateways, sub choreographies, and loops in the model."
  - item: "Trace"
    chunk: 1
    lines: "247-250"
    quote: "A trace is the ordered sequence of events (activities) that occurred for a specific case. Each event represents a task (activity) in the model."
  - item: "Participant"
    chunk: 1
    lines: "313-314"
    quote: "The simulator also generates an encoding that maps the events and participants to how they should be represented in the smart contract (taskIDs and participantIDs, the latter associated with a blockchain address)."
  - item: "Smart Contract"
    chunk: 1
    lines: "16-17"
    quote: "...the use of LLMs for generating smart contract code from business process descriptions..."

entity_definitions:
  Trace: "The ordered sequence of events (activities) that occurred for a specific case. A trace can be said to be in conformance with a process model if it represents a valid execution path through that model. (Chunk 1:247-250)"
  ConformingTrace: "A trace that represents a valid execution path through a process model, which the smart contract must accept. (Chunk 1:239-240)"
  NonConformingTrace: "A manipulated trace that does not represent a valid execution path, which the smart contract must reject. (Chunk 1:239-240)"
  Token: "The units of input and output for LLMs. Tokens can be whole words, subwords, individual characters, punctuation, or special characters. (Chunk 1:148-149)"
  Temperature: "A setting for LLMs that controls the randomness of generated text; lower temperatures make outputs more predictable and focused, while higher temperatures encourage more creative and varied responses. (Chunk 1:171-174)"
  InteractionNet: "A special type of labelled Petri net suitable to represent choreographies, used as intermediate representation. (Chunk 1:349-351)"

entity_relationships:
  - relationship: "Trace conformsTo ProcessModel"
    chunk: 1
    lines: "249-250"
    quote: "A trace can be said to be in conformance with a process model if it represents a valid execution path through that model."
  - relationship: "Event partOf Trace"
    chunk: 1
    lines: "247-248"
    quote: "A trace is the ordered sequence of events (activities) that occurred for a specific case."
  - relationship: "Event represents Task"
    chunk: 1
    lines: "249-250"
    quote: "Each event represents a task (activity) in the model."
  - relationship: "Choreography transformedTo SmartContract"
    chunk: 1
    lines: "346-348"
    quote: "Chorpiler transforms BPMN Choreographies to smart contracts, generates non-conforming traces from conforming traces, and also generates machine-readable encodings on how to interact with a contract."
  - relationship: "Participant associatedWith BlockchainAddress"
    chunk: 1
    lines: "313-314"
    quote: "...participantIDs, the latter associated with a blockchain address."

abstraction_level: "Application-level. The paper focuses on practical transformation of BPMN choreography models into executable Solidity smart contracts for blockchain-based process execution. It operates at the intersection of business process modeling standards (BPMN 2.0) and blockchain implementation (EVM/Solidity). (Chunk 1:338-343)"

framework_comparison:
  - item: "BPMN 2.0 Choreographies as input standard"
    chunk: 1
    lines: "338-343"
    quote: "In the current instantiation of our framework, we support BPMN 2.0 Choreographies. This is a purely practical implementation choice, given that there is no consensus on the best fitting modelling paradigm for blockchain-based execution."
  - item: "Rule-based vs LLM-based transformation approaches"
    chunk: 1
    lines: "54-61"
    quote: "Blockchain-based business process execution relies on a model-driven paradigm, where process descriptions are transformed into executable artefacts based on rule-based transformation tools. These tools, however, exhibit various limitations... LLMs are similarly prospected to have the potential to drive automation."
  - item: "Chorpiler as baseline code generation tool"
    chunk: 1
    lines: "346-351"
    quote: "Chorpiler transforms BPMN Choreographies to smart contracts... Chorpiler parses a given Choreography into an interaction net, a special type of labelled Petri net."

methodology: "Empirical benchmarking study. The paper uses an automated evaluation framework to test LLM-generated smart contracts against ground truth process traces. The methodology involves: (1) Pre-processing 1,427 BPMN choreography models from SAP-SAM dataset, (2) Sampling 165 models for benchmark, (3) Generating conforming and non-conforming traces using Chorpiler/pm4py, (4) Testing 7 LLMs (4 open-source, 3 proprietary) with one-shot and two-shot prompts, (5) Evaluating via precision, recall, and F1 scores. (Chunk 1:230-242, 385-395, 455-479)"

ai_integration:
  - item: "LLM-based code generation from BPMN to Solidity"
    chunk: 1
    lines: "14-17"
    quote: "In this work, we present an exploratory study to investigate the use of LLMs for generating smart contract code from business process descriptions, an idea that has emerged in recent literature to overcome the limitations of traditional rule-based code generation approaches."
  - item: "Zero-shot and few-shot prompting strategies"
    chunk: 1
    lines: "145-147"
    quote: "In zero-shot prompting, models complete tasks based solely on instructions without prior examples, whereas few-shot prompting involves providing a handful of illustrative examples directly within the input."
  - item: "Temperature setting for deterministic output"
    chunk: 1
    lines: "477-479"
    quote: "...we benchmark a one-shot and two-shot variant of our prompt with temperature set to 0, [leading to quasi-deterministic inference results]"
  - item: "Proprietary vs open-source model comparison"
    chunk: 1
    lines: "164-170"
    quote: "LLMs are available in both proprietary and open-source forms. Proprietary models... are typically accessed via APIs hosted by third parties... open-source models enable self-hosting and on-premise deployment--an attractive option in blockchain contexts where data sovereignty, trust minimization, and operational independence are essential."
  - item: "LLM non-determinism as fundamental limitation"
    chunk: 1
    lines: "67-68"
    quote: "LLM outputs are inherently non-deterministic, making them unreliable for consistent behaviour."

agent_modeling:
  - item: "LLMs as transformation tools"
    chunk: 1
    lines: "15-17"
    quote: "...the use of LLMs for generating smart contract code from business process descriptions..."
  - item: "Non-deterministic behavior characteristic"
    chunk: 1
    lines: "67-68"
    quote: "LLM outputs are inherently non-deterministic, making them unreliable for consistent behaviour."

agentic_workflows: []

generative_ai_patterns:
  - item: "One-shot prompting for code generation"
    chunk: 1
    lines: "464-469"
    quote: "Through our initial tests, we arrived at a one-shot prompt. Specifically, in our prompt we ask for a Solidity implementation for the given process model, enforcing: (i) the control flow, i.e., the order of tasks, (ii) that only the respective initiator can execute a task, and (iii) the autonomous enforcement of gateways."
  - item: "Two-shot prompting for improved accuracy"
    chunk: 1
    lines: "469-470"
    quote: "To gauge the effect of prompt-based training, we test a one-shot and a two-shot variant."
  - item: "Prompt engineering and refinement"
    chunk: 1
    lines: "458-464"
    quote: "To reduce the likelihood of our results being tainted by a poorly performing prompt, we tested, compared, and refined multiple versions in pre-runs... our prompts moved from loosely defined (zero-shot) instructions, to (better performing) more specific instructions on how the process model should be interpreted."
  - item: "LLM output extraction and compilation"
    chunk: 1
    lines: "322-324"
    quote: "From the usage log output, the log replayer extracts the smart contract code, compiles and deploys it to an external blockchain environment, and uses the encodings and event logs to perform a benchmark on the deployed contract."
  - item: "Reasoning models"
    chunk: 1
    lines: "156-158"
    quote: "Models that perform complex reasoning (so called reasoning models) typically generate a plan to answer a query, execute the steps in the plan, and possibly check their work; hence they require many more tokens than regular LLMs."
  - item: "LLM judge evaluation"
    chunk: 1
    lines: "196-197"
    quote: "...a LLM judge evaluation approach, where LLMs assess the output of other LLMs."

agent_ontology_integration:
  - item: "Process model as structured input for LLM"
    chunk: 1
    lines: "135-136"
    quote: "...training ingests very large textual corpora, comprising not only natural language, but also programming code (such as Solidity for blockchain smart contracts), and formal representations (such as BPMN for modeling business processes)."
  - item: "Encoding mapping for contract interaction"
    chunk: 1
    lines: "313-315"
    quote: "The simulator also generates an encoding that maps the events and participants to how they should be represented in the smart contract (taskIDs and participantIDs, the latter associated with a blockchain address). This encoding is embedded into the prompt, along with the model data."

entity_count: null

empirical_evidence:
  - item: "SAP-SAM dataset: 4,096 BPMN choreographies, 1,427 filtered, 165 sampled"
    chunk: 1
    lines: "386-394"
    quote: "Our process model data is based on the SAP Signavio Academic Models Dataset (SAP-SAM)... The collection includes 4,096 BPMN 2.0 choreography models... After the filtering steps, 1,427 choreography models remain. We use a sample of 165 models for our benchmark runs."
  - item: "Model complexity metrics"
    chunk: 1
    lines: "417-421"
    quote: "In our sample, on average, each process contains 13 participants, six tasks, one diverging exclusive gateway, 0.1 diverging event-based gateways, and 0.2 diverging parallel gateways... The largest model in the dataset contains 24 tasks and ten gateways."
  - item: "LLM performance results (F1 scores)"
    chunk: 1
    lines: "575-613"
    quote: "grok-3-beta [one-shot] F1 0.918... claude-sonnet-4 [one-shot] F1 0.862... gpt-4.1 [one-shot] F1 0.797"
  - item: "Compilability rates"
    chunk: 1
    lines: "610-613"
    quote: "Compilability (Comp.) reports on the percentage of syntactically correct generated contracts. [100% for grok-3-beta and claude-sonnet-4]"
  - item: "Cost per process translation"
    chunk: 1
    lines: "618-622"
    quote: "The cost for translating a process model was on the orders of 0.1 cents to a few cents."

limitations:
  - item: "LLM non-determinism prevents perfect reliability"
    chunk: 1
    lines: "109-116"
    quote: "Due to the stochastic nature of LLMs, output remains imperfect and unreliable. While such performance may be acceptable in other contexts, blockchain is an unforgiving environment... we believe this is a fundamental issue of the chosen approach to have LLMs generate smart contract code, which cannot be overcome by LLMs based on the current architectures."
  - item: "F1 scores below 100% unacceptable for smart contracts"
    chunk: 1
    lines: "638-648"
    quote: "F1 scores that do not reliably achieve 100% would not be suitable for this context. Say, the approaches would be improved to achieving an average F1 score of 98%; while this would be impressive in many domains, it falls short of the perfect reliability required for blockchain-based smart contracts."
  - item: "Security vulnerabilities in LLM-generated code"
    chunk: 1
    lines: "66-67"
    quote: "GitHub Copilot can introduce numerous security vulnerabilities into generated code."
  - item: "Prompt optimization not guaranteed"
    chunk: 1
    lines: "677-679"
    quote: "We experimented with different prompts, but cannot guarantee that the selected query was optimal; furthermore, we used the same prompt across all LLMs, which may be suboptimal."
  - item: "Proprietary model confidentiality concerns"
    chunk: 1
    lines: "71-75"
    quote: "Proprietary models raise concerns about confidentiality, privacy, and autonomy... Relying on central deployments may not be a good fit for blockchain-based processes, where decentralisation is a goal."

tools_standards:
  - item: "BPMN 2.0 Choreographies"
    chunk: 1
    lines: "338"
    quote: "In the current instantiation of our framework, we support BPMN 2.0 Choreographies."
  - item: "Solidity (Ethereum smart contract language)"
    chunk: 1
    lines: "135"
    quote: "...programming code (such as Solidity for blockchain smart contracts)..."
  - item: "Ethereum Virtual Machine (EVM)"
    chunk: 1
    lines: "341-342"
    quote: "We instantiate our framework for an Ethereum virtual machine (EVM) blockchain environment, the most widely employed environment."
  - item: "Chorpiler (BPMN-to-contract transformation tool)"
    chunk: 1
    lines: "346-348"
    quote: "We extend the open source tool Chorpiler, first introduced in [40] with simulation capabilities. Chorpiler transforms BPMN Choreographies to smart contracts."
  - item: "pm4py (Python process mining library)"
    chunk: 1
    lines: "351-354"
    quote: "We make use of this intermediate presentation to generate conforming traces. Here, we adopt the implementation of pm4py, a popular Python library for process mining, which includes a playout functionality to generate event log traces from Petri nets."
  - item: "Hardhat (Ethereum development framework)"
    chunk: 1
    lines: "362-365"
    quote: "To provide the replayer with a blockchain environment, we use hardhat, a popular Ethereum development framework that allows testing, deployment, and debugging of smart contracts in a locally simulated EVM environment."
  - item: "OpenRouter (unified LLM API platform)"
    chunk: 1
    lines: "365-367"
    quote: "As LLM provider, we use OpenRouter, a platform that provides a unified API across multiple language model providers."
  - item: "Petri nets (interaction nets as intermediate representation)"
    chunk: 1
    lines: "349-351"
    quote: "Chorpiler parses a given Choreography into an interaction net, a special type of labelled Petri net, suitable to represent choreographies."
---

# On LLM-Assisted Generation of Smart Contracts from Business Processes

## Summary

This paper presents an exploratory study investigating the use of Large Language Models (LLMs) for generating smart contract code from business process descriptions (BPMN 2.0 Choreographies). The authors introduce an automated benchmarking framework to evaluate LLM-generated Solidity smart contracts against ground truth process execution traces.

## Key Contributions

1. **Open Benchmarking Framework**: First open-source framework for automated assessment of code generation from process models to smart contracts, using trace replay for verification.

2. **Large-Scale Empirical Study**: Evaluation of 7 LLMs (4 open-source, 3 proprietary) on 165 BPMN choreography models from the SAP-SAM dataset.

3. **Performance Results**: Top models (Grok-3-beta, Claude Sonnet 4) achieved F1 scores of 0.8+, but the authors argue this is insufficient for smart contract deployment where 100% reliability is required.

4. **Fundamental Limitation Identified**: The inherent non-determinism of LLMs makes them unsuitable for direct smart contract generation in blockchain contexts where any error could lead to financial loss.

## Research Context

The paper bridges three domains:
- **Business Process Management (BPM)**: Using BPMN choreographies as input specifications
- **Large Language Models**: Evaluating code generation capabilities
- **Blockchain**: Smart contract execution on Ethereum Virtual Machine

## Methodology

1. Pre-process BPMN 2.0 choreography models from SAP-SAM dataset (1,427 valid models)
2. Sample 165 models for benchmark
3. Generate conforming and non-conforming traces using Chorpiler + pm4py
4. Test LLMs with one-shot and two-shot prompts (temperature=0)
5. Compile and deploy generated Solidity contracts to Hardhat EVM
6. Evaluate via precision, recall, and F1 scores based on trace acceptance/rejection

## Results Summary

| Model | Shot | F1 (Macro) | Compilability |
|-------|------|------------|---------------|
| grok-3-beta | One | 0.918 | 100% |
| claude-sonnet-4 | One | 0.862 | 100% |
| gpt-4.1 | One | 0.797 | 99.4% |
| deepseek-v3 | One | 0.580 | 99.4% |
| llama-3.3-70b | One | 0.399 | 90.4% |

## Relevance to Ontologies Research

**Moderate relevance** - The paper focuses on LLM code generation rather than ontological foundations, but provides:
- Entity types from BPMN Choreographies (tasks, events, gateways, participants)
- Process-to-code transformation patterns
- Empirical data on LLM capabilities for structured model interpretation
- Insights on AI integration limitations for safety-critical applications

## Future Directions Proposed

1. LLMs for verification rather than direct generation
2. LLM-assisted extension of rule-based code generation tools
3. LLM-generated test cases and vulnerability detection
4. Hybrid approaches combining rule-based reliability with LLM flexibility
