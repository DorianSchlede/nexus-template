---
paper_id: "17-KG_Reasoning_Logics_Embeddings_Survey"
title: "Knowledge Graph Reasoning with Logics and Embeddings: Survey and Perspective"
chunks_expected: 1
chunks_read: 1
analysis_complete: true
high_priority_fields_found: 8

# Extraction fields
entity_types:
  - "Entity (KG triple subject/object)"
  - "Relation (KG triple predicate)"
  - "Class (entity type)"
  - "Logic Rule"
  - "Ontological Schema"
  - "Embedding (vector representation)"

entity_definitions:
  KnowledgeGraph: "Representing facts in the form of triples, with vocabulary defined in a schema (also known as ontology) (Chunk 1:35-37)"
  KGEmbedding: "Representation learning technique that represents entities and relations by vectors with their semantics preserved in vector space (Chunk 1:97-99)"
  LogicRule: "Form H <- B1 ^ B2 ^ ... ^ Bn where head atom H is inferred from body atoms (Chunk 1:79-82)"
  ClassHierarchy: "Classifies entity types, denoting entities as instantiations of classes (Chunk 1:200-202)"
  RelationHierarchy: "Subsumption relationships between relations, e.g., hasFather is sub-relation of hasParents (Chunk 1:224)"

entity_relationships:
  - from: "Entity"
    to: "Entity"
    relationship: "connected via Relation in triple (h,r,t)"
    source: "Chunk 1:35-37"
  - from: "LogicRule"
    to: "Triple"
    relationship: "infers new triples through grounding"
    source: "Chunk 1:169-176"
  - from: "OntologicalSchema"
    to: "Embedding"
    relationship: "constrains/regularizes via axioms"
    source: "Chunk 1:194-198"
  - from: "Class"
    to: "Entity"
    relationship: "instantiation (type membership)"
    source: "Chunk 1:200-202"

abstraction_level: "core"

framework_comparison:
  - compared_to: "OWL 2 / Description Logics"
    relationship: "foundational"
    details: "OWL 2 based on SROIQ DL provides schema language for KGs with rich expressive power"
    source: "Chunk 1:86-92"
  - compared_to: "TransE"
    relationship: "embedding_method"
    details: "Translation-based embedding using ||h+r-t|| as score function"
    source: "Chunk 1:102-107"
  - compared_to: "ComplEx"
    relationship: "embedding_method"
    details: "Complex vector space for asymmetric relations"
    source: "Chunk 1:244-245"
  - compared_to: "RotatE"
    relationship: "embedding_method"
    details: "Rotation in complex space for compositional relations"
    source: "Chunk 1:245-246"
  - compared_to: "SPARQL"
    relationship: "query_language"
    details: "Structured query language for KG retrieval and manipulation"
    source: "Chunk 1:359-361"

ai_integration:
  - pattern: "Neural-Symbolic Integration"
    description: "Combining logic-based and embedding-based reasoning for robust KG inference"
    source: "Chunk 1:57-71"
  - pattern: "Embedding-based uncertainty handling"
    description: "Embeddings deal with data noise and predict plausible but non-determined knowledge"
    source: "Chunk 1:54-58"
  - pattern: "Differentiable theorem proving"
    description: "NTP enables Prolog to learn embeddings and compare symbols via vector similarity"
    source: "Chunk 1:418-430"
  - pattern: "Embedding-guided rule mining"
    description: "Use embeddings to guide/prune search during rule learning"
    source: "Chunk 1:463-468"

agent_modeling:
  - aspect: "N/A - Paper predates agent-focused research"
    description: "Paper focuses on KG reasoning methods rather than agent modeling patterns"
    source: "N/A"

agentic_workflows: "N/A - paper predates modern agentic AI discussion"

generative_ai_patterns: "N/A - paper predates LLM/generative AI era"

agent_ontology_integration:
  - mechanism: "Ontological reasoning for KG completion"
    description: "SIC uses ontological reasoning within iterative KG completion to infer triples and filter schema-incorrect ones"
    source: "Chunk 1:258-259, 294-298"
  - mechanism: "Schema-aware negative sampling"
    description: "ReasonKGE uses schema-incorrect triples for negative sampling"
    source: "Chunk 1:296-298"
  - mechanism: "Embedding-based query answering"
    description: "GQE embeds entities as vectors, relations as projection operators, queries as vectors"
    source: "Chunk 1:396-398"
  - mechanism: "Complex query support"
    description: "Query2box, BetaE, ConE support conjunction, disjunction, negation via geometric embeddings"
    source: "Chunk 1:400-410"

entity_count:
  count: "N/A"
  rationale: "Survey paper does not define a fixed entity count - reviews multiple methods"
  source: "N/A"

methodology: "hybrid"

empirical_evidence:
  - type: "Benchmark evaluation"
    description: "Methods evaluated on WN18RR, FB15k-237, NELL datasets for link prediction and query answering"
    source: "Chunk 1:532-541"
  - type: "Survey analysis"
    description: "Systematic review of methods categorized by logic type, integration stage, and mechanism"
    source: "Chunk 1:263-290 (Table 1), 371-387 (Table 2)"

limitations:
  - "Logic diversity: Methods typically only support specific logic types, not general schemas (Chunk 1:497-504)"
  - "Explainability: Embedding methods remain black-box; vector intermediate results hard to interpret (Chunk 1:514-520)"
  - "Benchmark shortage: Datasets lack diverse pre-defined logic patterns for evaluation (Chunk 1:532-541)"
  - "Schema correctness: Silver standard results may not transfer to other KGs (Chunk 1:542-547)"

tools_standards:
  - "OWL 2"
  - "RDF Schema"
  - "SPARQL"
  - "Datalog"
  - "HermiT (DL reasoner)"
  - "RDFox (Datalog reasoner)"
  - "Prolog"
  - "TensorLog"
---

# Knowledge Graph Reasoning with Logics and Embeddings: Survey and Perspective - Analysis Index

## Paper Overview

- **Source**: 17-KG_Reasoning_Logics_Embeddings_Survey.pdf
- **Chunks**: 1 chunk, ~12166 estimated tokens
- **Analyzed**: 2025-12-28T13:30:00
- **Authors**: Wen Zhang, Jiaoyan Chen, Juan Li, Zezhong Xu, Jeff Z. Pan, Huajun Chen
- **Institutions**: Zhejiang University, University of Oxford, University of Edinburgh

## Key Extractions

This survey paper comprehensively reviews methods that integrate symbolic logic-based reasoning with embedding-based (neural) reasoning for knowledge graphs. The paper identifies two primary integration directions and systematically categorizes methods along multiple dimensions.

### Integration Directions (Chunk 1:65-67)

| Direction | Description | Quote |
|-----------|-------------|-------|
| Logics for Embeddings | Inject rules/schemas into embedding learning | "injecting logics, such as logical rules and ontological schemas, into embedding learning" |
| Embeddings for Logics | Use embeddings for reasoning tasks | "utilizing KG embeddings for logic reasoning-relevant tasks, such as query answering, theorem proving and rule mining" |

### Classification Dimensions (Chunk 1:124-148)

| Dimension | Options | Description |
|-----------|---------|-------------|
| Logic Types | Rules, Ontological schemas | What kind of logic is integrated |
| Pre-defined Logics | With/Without | Whether explicit logic data is used |
| Integration Stage | Pre/Joint/Post | When logic is injected in learning |
| Mechanism | Data-based/Model-based | How integration occurs |

### Ontological Schema Integration Patterns (Chunk 1:194-260)

| Schema Type | Methods | Integration Approach |
|-------------|---------|---------------------|
| Class Hierarchies | TKRL, HAKE | Type embeddings, polar coordinates |
| Relation Hierarchies | HRS, TransRHS | Cluster embeddings, relation spheres |
| Domain/Range | TRESCAL, TypeDM | Triple filtering, constraint embedding |
| Inverse/Equivalent | Minervini et al. | Axiom-based regularization |
| Transitive/Symmetric | RotatE, Rot-Pro, dORC | Complex space rotation, projection |

### Embedding-Based Reasoning Tasks (Chunk 1:316-476)

| Task | Methods | Capability |
|------|---------|------------|
| Path Query Answering | TransE, PTransE | Simple compositional queries |
| Conjunctive Queries | GQE, BiQE | AND operations via intersection |
| EPFO Queries | Query2box, CQD | Disjunction via DNF transformation |
| Full FOL | BetaE, ConE, NewLook | Negation, difference operations |
| Theorem Proving | NTP, GNTP, CTP | Differentiable proof with embeddings |
| Rule Mining | AMIE, NeuralLP, DRUM | Differentiable rule learning |

### Key Findings (with evidence)

- **Neural-symbolic integration advantage** (Chunk 1:21-27): "A promising direction is to integrate both logic-based and embedding-based methods, with the vision to have advantages of both."
- **Embedding handles uncertainty** (Chunk 1:54-58): "embedding-based reasoning can deal with uncertainty and data noise, and is able to predict non-determined but plausible knowledge"
- **Schema injection methods** (Chunk 1:294-298): "inject inferred triples to enrich the input KG for embedding, and to filter out schema-incorrect triples via consistency and constraint checking"
- **Explainability challenge** (Chunk 1:516-518): "intermediate results are represented as embeddings that is understandable by human if and only if the meaning of these embeddings are properly interpreted"

## Chunk Navigation

### Chunk 1: Complete Paper (Lines 1-850)

- **Summary**: Comprehensive survey covering KG reasoning with integrated logic and embedding approaches. Introduces background on symbolic vs embedding reasoning, reviews methods for injecting logics into embeddings (Section 3) and using embeddings for logic tasks (Section 4), and concludes with challenges in logic diversity, explainability, benchmarks, and applications.

- **Key concepts**: [Knowledge Graph Embedding, Neural-Symbolic Integration, Ontological Schema, Logic Rules, Query Answering, Theorem Proving, Rule Mining, Description Logics, OWL 2]

- **Key quotes**:
  - Line 19-22: "Conventional KG reasoning based on symbolic logic is deterministic, with reasoning results being explainable, while modern embedding-based reasoning can deal with uncertainty and predict plausible knowledge"
  - Line 86-88: "Web Ontology Language OWL 2, which is based on Description Logics (DLs), is a key standard schema language of KGs"
  - Line 97-99: "KG embedding (KGE), as a kind of representation learning technique, aims to represent entities and relations by vectors"
  - Line 418-421: "Differentiable theorem proving using embeddings overcome the limits of symbolic provers on generalizing to queries with similar but not identical symbols"
  - Line 497-500: "The majority of current methods only consider specific kinds of logics, such as path rules, entity types (classes), class hierarchies, relation hierarchies, and relation properties"

- **Load when**: "User asks about neural-symbolic integration in knowledge graphs" / "Query mentions embedding methods for ontological reasoning" / "Question about combining logic rules with neural embeddings" / "Research on KG query answering with embeddings" / "OWL/Description Logic integration with machine learning"

## Relevance to Research Questions

### Foundational Ontologies
This paper extensively discusses how ontological schemas (OWL 2, Description Logics) integrate with embedding methods. It provides a taxonomy of ontological constructs (class hierarchies, relation hierarchies, relation properties) and how each can be embedded.

### AI Agent Integration
While the paper predates modern LLM agents, it provides foundational patterns for:
- Using ontological knowledge to constrain/improve neural reasoning
- Performing complex query answering via embeddings
- Differentiable reasoning that could support agent planning
- Rule learning from knowledge graphs

### Agent-Ontology Interaction
The paper's patterns for ontology-guided embedding are directly applicable to how AI agents could:
- Query knowledge graphs with incomplete/noisy data
- Learn rules from ontological structures
- Reason with uncertainty while respecting logical constraints
