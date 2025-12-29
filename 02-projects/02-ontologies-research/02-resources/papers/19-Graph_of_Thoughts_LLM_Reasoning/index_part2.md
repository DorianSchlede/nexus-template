---
# PARTIAL INDEX HEADER
partial: true
part: 2
total_parts: 2
chunks_covered: [7]

# Paper metadata
paper_id: "19-Graph_of_Thoughts_LLM_Reasoning"
title: "Graph of Thoughts: Solving Elaborate Problems with Large Language Models"
chunks_expected: 7
chunks_read: 1
analysis_complete: false
high_priority_fields_found: 3

# Extraction fields (from Chunk 7 only)
entity_types:
  - "Thought"
  - "Operation"
  - "Graph"

entity_definitions:
  Operation: "A transformation applied to thoughts in the graph, including Generate, Score, KeepBestN, Aggregate, and GroundTruth (Chunk 7:640-651)"

entity_relationships:
  - from: "Generate"
    to: "Thought"
    relationship: "creates"
    source: "Chunk 7:640-643"
  - from: "Score"
    to: "Thought"
    relationship: "evaluates"
    source: "Chunk 7:644-645"
  - from: "KeepBestN"
    to: "Thought"
    relationship: "selects"
    source: "Chunk 7:645"
  - from: "Aggregate"
    to: "Thought"
    relationship: "merges"
    source: "Chunk 7:646-647"
  - from: "GroundTruth"
    to: "Thought"
    relationship: "validates"
    source: "Chunk 7:651"

abstraction_level: "application"

framework_comparison: []

ai_integration:
  - pattern: "Multi-step reasoning with scoring"
    description: "LLM generates multiple candidate solutions (k=5 or k=10), scores them locally, keeps best N"
    source: "Chunk 7:643-649"
  - pattern: "Divide-and-conquer decomposition"
    description: "Complex problems split into subproblems (e.g., 128 elements into 8 parts of 16)"
    source: "Chunk 7:685-687"
  - pattern: "Iterative refinement"
    description: "Generate operations try to improve solutions after aggregation"
    source: "Chunk 7:749-752"

agent_modeling: []

agentic_workflows:
  - pattern: "Hierarchical merge workflow"
    description: "Multi-level aggregation: split into 8 parts, merge pairwise in 3 levels"
    source: "Chunk 7:681-735"
  - pattern: "Score-and-select loop"
    description: "After each operation, score results locally and keep best N"
    source: "Chunk 7:644-648"

generative_ai_patterns:
  - pattern: "Graph-based prompting"
    description: "Prompts structured as operations in a directed graph (Generate, Score, Aggregate)"
    source: "Chunk 7:630-651"
  - pattern: "Multi-sample generation"
    description: "Generate(k=N) produces N candidate solutions for subsequent scoring"
    source: "Chunk 7:640-644"
  - pattern: "Harmonic mean scoring"
    description: "Final score computed as harmonic mean of redundancy and retained information"
    source: "Chunk 7:580-583"
  - pattern: "Tagged output extraction"
    description: "Outputs wrapped in XML-like tags for extraction (e.g., <Merged>, <Redundancy>, <Retained>)"
    source: "Chunk 7:29-31, 417-419"
  - pattern: "LLM-as-judge"
    description: "LLM scores merged documents on redundancy and retained information criteria"
    source: "Chunk 7:405-419"
  - pattern: "Iterative improvement prompting"
    description: "Prompt asks to improve merged result by adding information and removing redundancy"
    source: "Chunk 7:29-30"

agent_ontology_integration: []

entity_count:
  count: 5
  rationale: "Core operation types in GoT: Generate, Score, KeepBestN, Aggregate, GroundTruth"
  source: "Chunk 7:640-651"

methodology: "top-down"

empirical_evidence:
  - type: "Document merging task"
    description: "4 NDAs merged using GoT with multiple responses scored (10 responses, scores 5.33-7.78)"
    source: "Chunk 7:139-583"
  - type: "Set intersection benchmarks"
    description: "Configurations for 32, 64, and 128 element sets with hierarchical merge"
    source: "Chunk 7:636-735"
  - type: "Sorting benchmarks"
    description: "Configurations for sorting 32, 64, and 128 elements with divide-and-conquer"
    source: "Chunk 7:738-859"

limitations:
  - "Requires problem decomposition strategy to be specified upfront (Chunk 7:630-651)"
  - "Scoring relies on LLM self-evaluation which may have biases (Chunk 7:514-577)"

tools_standards:
  - "Custom GoT configuration DSL"
  - "XML-like tagging for structured extraction"
---

# Graph of Thoughts: Solving Elaborate Problems with Large Language Models - Partial Index (Part 2 of 2)

## Chunks Covered: 7

This partial analysis covers the appendix sections of the paper containing detailed examples and configurations.

## Paper Overview

- **Source**: 19-Graph_of_Thoughts_LLM_Reasoning.pdf
- **Chunks Covered**: 7 (of 7 total)
- **Analysis Type**: PARTIAL (Part 2 of 2)
- **Focus**: Appendix material with document merging examples and GoT configurations

## Key Extractions

### Generative AI Patterns

This chunk provides detailed examples of GoT's prompting and reasoning patterns:

| Pattern | Source | Description |
|---------|--------|-------------|
| Graph-based prompting | Chunk 7:630-651 | Operations structured as directed graph |
| Multi-sample generation | Chunk 7:640-644 | Generate(k=N) produces N candidates |
| LLM-as-judge | Chunk 7:405-419 | LLM scores outputs on quality criteria |
| Tagged output extraction | Chunk 7:29-31 | XML-like tags for structured extraction |
| Harmonic mean scoring | Chunk 7:580-583 | Combines redundancy and retention scores |
| Iterative improvement | Chunk 7:29-30 | Prompts to improve and reduce redundancy |

### AI Integration Patterns

| Pattern | Source | Description |
|---------|--------|-------------|
| Multi-step scoring | Chunk 7:643-649 | Generate k solutions, score, keep best |
| Divide-and-conquer | Chunk 7:685-687 | Split into 16-element chunks |
| Iterative refinement | Chunk 7:749-752 | Improve solutions after aggregation |

### Agentic Workflows

| Pattern | Source | Description |
|---------|--------|-------------|
| Hierarchical merge | Chunk 7:681-735 | Multi-level pairwise aggregation |
| Score-and-select | Chunk 7:644-648 | Loop of scoring and selection |

### GoT Operation Types (Entity Types)

The chunk defines 5 core operations that compose the GoT graph:

1. **Generate(k)** - Create k candidate thoughts/solutions (Chunk 7:640-643)
2. **Score(k)** - Evaluate quality of k thoughts (Chunk 7:644)
3. **KeepBestN(n)** - Select top n scoring thoughts (Chunk 7:645)
4. **Aggregate(n)** - Merge n thoughts into one (Chunk 7:646-647)
5. **GroundTruth()** - Validate against known answer (Chunk 7:651)

## Chunk Navigation

### Chunk 7: Appendix - Document Merging Examples and GoT Configurations

- **Summary**: Contains detailed appendix material showing (1) complete NDA document merging example with prompts, 10 scored responses, and final merged output, (2) LLM scoring rubrics for redundancy and retained information, and (3) GoT configuration pseudocode for set intersection and sorting tasks at 32/64/128 element scales.

- **Key concepts**: [Document merging, Multi-sample generation, LLM-as-judge scoring, Hierarchical aggregation, Divide-and-conquer strategy, GoT configuration DSL]

- **Key quotes**:
  - Line 29-30: "Please improve the merged NDA by adding more information and removing redundancy"
  - Line 405-409: "Please score the merged NDA in terms of how much redundant information is contained...as well as how much information is retained"
  - Line 580-583: "Final Overall Score (Harmonic Mean of Averages): 7.78"
  - Line 640: "Generate(k=1) # Split second set into two halves of 16 elements"
  - Line 643-644: "Generate(k=5) # Determine intersected subset... Score(k=1) # Score locally"

- **Load when**: "User asks about GoT configuration syntax", "Query mentions document merging with LLMs", "Question about LLM scoring/evaluation patterns", "How does GoT handle set intersection or sorting", "Multi-sample generation examples"

## Evidence for Chunk 7

```yaml
chunk_evidence:
  7:
    start: "_<_ Merged _>_ NON-DISCLOSURE AGREEMENT (NDA) 1. Agreement between [Your Compan"
    mid: "1 Generate(k=1) # Split second set into four parts of 16 elements 2 foreach subs"
    end: "54 KeepBestN (1) # Keep the best result 55 GroundTruth () # Compare to precomputed result"
```
