---
paper_id: "17-KG_Reasoning_Logics_Embeddings_Survey"
title: "Knowledge Graph Reasoning with Logics and Embeddings: Survey and Perspective"
authors:
  - "Wen Zhang"
  - "Jiaoyan Chen"
  - "Juan Li"
  - "Zezhong Xu"
  - "Jeff Z. Pan"
  - "Huajun Chen"
year: null
chunks_expected: 1
chunks_read: 1
analysis_complete: true
schema_version: "2.3"

chunk_index:
  1:
    token_count: 11706
    fields_found:
      entity_types: true
      entity_definitions: true
      entity_relationships: true
      entity_count: false
      abstraction_level: true
      framework_comparison: true
      methodology: true
      ai_integration: true
      agent_modeling: false
      agentic_workflows: false
      generative_ai_patterns: false
      agent_ontology_integration: true
      empirical_evidence: partial
      limitations: true
      tools_standards: true

entity_types:
  - item: "Entity"
    chunk: 1
    lines: "52-53"
    quote: "KG embedding (KGE)...aims to represent entities and relations by vectors with their semantics (e.g., relationships) preserved in the vector space"
  - item: "Relation"
    chunk: 1
    lines: "52-53"
    quote: "KG embedding (KGE)...aims to represent entities and relations by vectors with their semantics (e.g., relationships) preserved in the vector space"
  - item: "Triple"
    chunk: 1
    lines: "35-36"
    quote: "Knowledge graph (KG), representing facts in the form of triples, with vocabulary defined in a schema (also known as ontology)"
  - item: "Class"
    chunk: 1
    lines: "200-202"
    quote: "Class hierarchies classify entity types, denoting entities as instantiations of classes"
  - item: "Logic Rule"
    chunk: 1
    lines: "79-85"
    quote: "One rule, which can be simply represented as B1 B2 ... Bn, means that the head atom H can be inferred...the head atom H can be inferred by the body atoms B1, ..., Bn"
  - item: "Ontological Schema"
    chunk: 1
    lines: "195-198"
    quote: "Ontological schemas, which are often defined by languages such as OWL and RDF Schema, describe high-level semantics (meta information) of KGs"
  - item: "Path Rule"
    chunk: 1
    lines: "151-153"
    quote: "A typical kind of logic rule is path rule...where rule body is a path from a head variable to a tail variable in the rule head"
  - item: "Embedding"
    chunk: 1
    lines: "97-99"
    quote: "KG embedding (KGE), as a kind of representation learning technique, aims to represent entities and relations by vectors"
  - item: "Query"
    chunk: 1
    lines: "359-361"
    quote: "Query answering returns correct entities in a KG as answers of a given structured query, where reasoning is usually considered for hidden answers"
---

# Knowledge Graph Reasoning with Logics and Embeddings: Survey and Perspective

## Summary

This survey paper provides a comprehensive review of methods that integrate logic-based and embedding-based approaches for Knowledge Graph (KG) reasoning. The paper addresses the complementary strengths of these paradigms: logic-based reasoning is deterministic and explainable but struggles with incompleteness and noise, while embedding-based reasoning handles uncertainty well but lacks interpretability.

## Key Contributions

### 1. Categorization Framework

The paper organizes integration methods across two major directions:

**Direction 1: Logics for Embeddings (Section 3)**
- Injecting logic rules into KG embeddings
- Incorporating ontological schemas (class hierarchies, relation hierarchies, relation properties)

**Direction 2: Embeddings for Logics (Section 4)**
- Query answering with embeddings
- Theorem proving with differentiable methods
- Rule mining/learning with embedding guidance

### 2. Four-Perspective Analysis

Each integration approach is analyzed from:
1. **Logic Types**: Path rules, ontological schemas, query types
2. **Pre-defined Logics**: With explicit logics vs. learning implicit logics
3. **Integration Stages**: Pre-training, joint-training, post-training
4. **Mechanisms**: Data-based vs. model-based (for logics-to-embeddings); Hybrid vs. neural (for embeddings-to-logics)

### 3. Key Methods Surveyed

**Logic Rules for Embeddings:**
- PTransE: Path compositional representations
- KALE: T-norm fuzzy logics for grounding
- RUGE/IterE: Iterative injection with dynamic labeling

**Ontological Schemas for Embeddings:**
- TKRL: Type hierarchy projection matrices
- HAKE: Polar coordinate hierarchies
- TransRHS: Relation hierarchy spheres

**Embeddings for Query Answering:**
- GQE: Entity and relation embeddings with operators
- Query2box: Box embeddings supporting disjunction
- BetaE/ConE: Support full first-order logic operations

**Embeddings for Theorem Proving:**
- NTP: Differentiable proving with learned similarities
- GNTP/CTP: Efficiency improvements via embedding-based selection

**Embeddings for Rule Learning:**
- RuLES: Confidence extension via embeddings
- NeuralLP/DRUM: Differentiable end-to-end rule mining

## Extracted Fields

### entity_definitions

| Entity | Definition | Source |
|--------|------------|--------|
| Knowledge Graph | Representing facts in the form of triples, with vocabulary defined in a schema (also known as ontology) - a simple yet efficient and increasingly popular way of knowledge representation | Chunk 1:35-37 |
| KG Embedding | A representation learning technique that aims to represent entities and relations by vectors with their semantics preserved in the vector space | Chunk 1:97-99 |
| Logic Rule | An expression of form H <- B1 ^ B2 ^ ... ^ Bn where H is the rule head and B1...Bn is the rule body; if body atoms are satisfied, head atom can be inferred | Chunk 1:79-85 |
| Path Rule | A logic rule where rule body is a path from a head variable to a tail variable in the rule head; e.g., r(X,Y) <- r1(X,Z) ^ r2(Z,Y) | Chunk 1:151-153 |
| Class Hierarchy | Classification of entity types, denoting entities as instantiations of classes | Chunk 1:200-202 |
| Relation Hierarchy | Subsumption relationships between relations; e.g., hasFather is a sub-relation of hasParents | Chunk 1:224 |
| Ontological Schema | High-level semantics defined by languages such as OWL and RDF Schema, describing meta information of KGs | Chunk 1:195-198 |
| Score Function | Defines how to compute the truth value based on entity and relation embeddings; e.g., TransE uses ||h+r-t|| | Chunk 1:104-107 |
| Grounding | Replacing variables in each rule with concrete entities, inferring implicit triples, and generating additional triples for training | Chunk 1:169-171 |

### entity_relationships

| Relationship | Source | Quote |
|--------------|--------|-------|
| Entity instantiates Class | Chunk 1:200-202 | "Class hierarchies classify entity types, denoting entities as instantiations of classes" |
| Relation has subRelation | Chunk 1:224 | "Relation hierarchies contain subsumption relationships between relations; for example, hasFather is a sub-relation of hasParents" |
| Triple composed of (Entity, Relation, Entity) | Chunk 1:35-36 | "Knowledge graph (KG), representing facts in the form of triples" |
| Embedding represents Entity | Chunk 1:97-99 | "KG embedding...aims to represent entities and relations by vectors" |
| Logic Rule derives Triple | Chunk 1:79-81 | "the head atom H can be inferred by the body atoms B1, ..., Bn" |
| Ontological Schema constrains Relation | Chunk 1:237-238 | "Ontological schemas often define quite a few relation properties (and constraints)" |

### abstraction_level

Domain-specific survey paper focused on Knowledge Graph reasoning methods. Operates at the intersection of symbolic logic and machine learning, categorizing integration approaches from foundational logic types to specific implementation mechanisms. Bridges theoretical logic formalisms (DL, OWL) with practical embedding methods (TransE, ComplEx, RotatE). (Chunk 1:19-27)

### framework_comparison

| Comparison | Source | Quote |
|------------|--------|-------|
| Logic-based vs Embedding-based reasoning | Chunk 1:55-58 | "Logic-based reasoning is usually interpretable and transferable, while embedding-based reasoning can deal with uncertainty and data noise, and is able to predict non-determined but plausible knowledge" |
| HermiT vs RDFox | Chunk 1:44-46 | "HermiT is a classic description logic reasoner for OWL ontologies; RDFox is a famous KG storage supporting Datalog rule reasoning" |
| TransE vs ComplEx vs RotatE | Chunk 1:102-103 | "Many successful KGE methods, such as TransE, ComplEx and RotatE, have been developed" |
| Pre vs Joint vs Post integration stages | Chunk 1:136-140 | "Pre: conducting symbolic reasoning before learning embeddings...Joint: injecting the logics during embedding learning...Post: conducting symbolic reasoning after embeddings are learned" |
| Data-based vs Model-based mechanisms | Chunk 1:143-147 | "Data-based: replacing variables in logic expressions with concrete entities and getting new triples...Model-based: adding constraints on the embedding of entities and relations" |
| Hybrid vs Neural mechanisms | Chunk 1:350 | "Hybrid: after applying embeddings, methods still infer in a symbolic space. Neural: using embeddings following the process of logic reasoning, and all inferences are conducted in vector space" |

### methodology

Survey paper synthesizing logic-based and embedding-based KG reasoning approaches. Uses systematic categorization from four perspectives: (1) Logic Types - rules vs ontological schemas; (2) Pre-defined Logics - with vs without; (3) Integration Stages - pre/joint/post; (4) Mechanisms - data-based vs model-based for logics-to-embeddings, hybrid vs neural for embeddings-to-logics. (Chunk 1:64-71, 121-147)

### ai_integration

| Pattern | Source | Description |
|---------|--------|-------------|
| Knowledge Graph Embedding for reasoning | Chunk 1:52-58 | "KG embedding, which represents entities and relations as vectors (embeddings) with their relationships reflected, shows great success in KG reasoning, especially in inductive reasoning without pre-defined logics" |
| Differentiable Theorem Proving | Chunk 1:418-428 | "Differentiable theorem proving using embeddings overcome the limits of symbolic provers on generalizing to queries with similar but not identical symbols" |
| Neural Query Answering | Chunk 1:393-410 | "GQE embeds entities as a vector, relations as projection operators on entity embeddings, and makes conjunction in conjunctive logical queries as intersection operators" |
| Differentiable Rule Mining | Chunk 1:470-475 | "Differentiable rule mining, learning rules in an end-to-end differentiable manner in vector space...inspired by TensorLog, a differentiable probabilistic logic" |

### agent_ontology_integration

| Pattern | Source | Description |
|---------|--------|-------------|
| Ontology-guided embedding constraints | Chunk 1:131-132 | "injecting predefined logics or their reasoning results into embeddings, and/or applying ontological axioms as constraints" |
| Schema-aware KG completion | Chunk 1:258-259 | "SIC proposes to use ontological reasoning within their iterative KG completion approach to inject inferred triples to enrich the input KG for embedding" |
| Type-aware graph attention | Chunk 1:206-208 | "TAGAT regularizes entity embeddings to be close to their corresponding type embeddings, and also closes the embeddings of entities that belong to the same type" |

### empirical_evidence

| Evidence | Source | Quote |
|----------|--------|-------|
| Benchmark datasets mentioned | Chunk 1:534-536 | "Commonly used benchmarks for KGEs' evaluation, such as WN18RR, FB15k-237 and NELL, are subsets sampled from one or multiple domain in large KGs" |
| Real-world KG examples | Chunk 1:38-39 | "Many general-purpose and domain-specific KGs, such as Wikidata and SNOMED Clinical Terms are under fast development and widely used" |

### limitations

| Limitation | Source | Quote |
|------------|--------|-------|
| Logic diversity challenge | Chunk 1:497-504 | "The majority of current methods only consider specific kinds of logics...Since a KG is often equipped with different kinds of logics...it becomes a significant challenge to support and integrate all or most of them simultaneously" |
| Explainability challenge | Chunk 1:514-520 | "Most methods...focus on improving the model's expressiveness, which does not change the black-box nature of embedding methods...Methods enabling logic reasoning in vector space decrease the transparency of logic-based methods" |
| Benchmark limitations | Chunk 1:532-541 | "There is a shortage of resources for evaluating KG reasoning with both logics and embeddings...do not ensure and explore diverse logic patterns contained in the dataset" |
| Scalability of grounding | Chunk 1:180-182 | "These data-based methods need to materialize each rule, resulting in a massive number of groundings, thus they do not scale well to large KGs" |

### tools_standards

| Tool/Standard | Source | Description |
|---------------|--------|-------------|
| OWL 2 (Web Ontology Language) | Chunk 1:86-92 | "OWL 2, which is based on Description Logics (DLs), is a key standard schema language of KGs. It is based on the SROIQ DL...OWL 2 provides rich expressive power" |
| RDF Schema | Chunk 1:195-196 | "Ontological schemas, which are often defined by languages such as OWL and RDF Schema" |
| SPARQL | Chunk 1:361 | "Conventional query answering is conducted based on structure query languages such as SPARQL to retrieve and manipulate knowledge in a KG" |
| HermiT | Chunk 1:44 | "HermiT is a classic description logic reasoner for OWL ontologies" |
| RDFox | Chunk 1:45 | "RDFox is a famous KG storage supporting Datalog rule reasoning" |
| Datalog | Chunk 1:45 | "RDFox is a famous KG storage supporting Datalog rule reasoning" |
| Prolog | Chunk 1:419 | "Conventional theorem proving methods are based on different logic languages, such as Prolog, Datalog, and OWL" |
| TransE | Chunk 1:102-108 | "TransE...makes h+r approximately equal to t as score function of triples, where h, r, and t are vectors of h, r, and t in the Euclidean space" |
| ComplEx | Chunk 1:102, 244 | "ComplEx proposes to embed KGs in complex vector space, where the commutative property for multiplication is not satisfied" |
| RotatE | Chunk 1:102, 245-246 | "RotatE proposes to define each relation as a rotation from the head entity to the tail entity in complex vector space" |
| TensorLog | Chunk 1:471-472 | "TensorLog, a differentiable probabilistic logic. Tensorlog establishes a connection between inference using first-order rules and sparse matrix multiplication" |

## Relevance to Research Questions

### Foundational Ontology Grounding
**Relevance**: LOW-MEDIUM
- Paper focuses on KG reasoning methods, not foundational ontology theory
- Does reference OWL 2 and Description Logics as schema standards
- Discusses class hierarchies and relation properties but as constraints for embeddings, not as foundational concepts

### AI Agent Integration
**Relevance**: MEDIUM-HIGH
- Extensive coverage of neural-symbolic integration for reasoning
- Methods for injecting ontological schemas into AI systems (embeddings)
- Query answering and theorem proving patterns applicable to agent reasoning
- Does NOT cover: LLM agents, ReAct, Chain-of-Thought, function calling (pre-LLM paper)

### Knowledge Graph as Reasoning Substrate
**Relevance**: HIGH
- Core topic of the paper
- Comprehensive taxonomy of KG reasoning approaches
- Integration patterns between symbolic logic and embeddings
- Applicable to agent memory and knowledge management systems

## Key Insights for Research

1. **Integration Stages**: Pre/Joint/Post training injection patterns could inform how AI agents interact with ontological knowledge at different phases.

2. **Logic Types**: The taxonomy of logic types (path rules, class hierarchies, relation properties) provides vocabulary for ontology-guided agent reasoning.

3. **Explainability Challenge**: The paper identifies explainability as key limitation - relevant to designing interpretable agentic workflows.

4. **Schema Correctness**: SIC's approach of using ontological reasoning for consistency checking is directly applicable to agent guardrails.

5. **Benchmark Gaps**: Warning about silver standard benchmarks not transferring to real KGs - important for validating agent-ontology integration.
