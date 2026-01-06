---
paper_id: "17"
title: "Knowledge Graph Reasoning with Logics and Embeddings: Survey and Perspective"
authors: ["Wen Zhang", "Jiaoyan Chen", "Juan Li", "Zezhong Xu", "Jeff Z. Pan", "Huajun Chen"]
institutions: ["Zhejiang University", "University of Oxford", "University of Edinburgh", "Alibaba-Zhejiang University Joint Research Institute"]
year: 2022
extraction_version: "v2_discovery"
extraction_date: "2025-12-31"

# V2 DISCOVERY EXTRACTION

ontological_primitives:
  - term: "Triple"
    definition: "Facts represented in the form (head, relation, tail) with vocabulary defined in a schema/ontology"
    source: "Chunk 1:35-37"
    unique_aspects: "The atomic unit of KG representation - irreducible below this level"

  - term: "Embedding"
    definition: "Vectors representing entities and relations with their semantics (relationships) preserved in vector space"
    source: "Chunk 1:98-99"
    unique_aspects: "Continuous representation enabling approximate/probabilistic reasoning"

  - term: "Score Function (phi)"
    definition: "Function computing truth value based on entity and relation embeddings"
    source: "Chunk 1:104-105"
    unique_aspects: "Core mechanism that defines how embeddings capture semantic relationships"

  - term: "Logic Rule"
    definition: "Form H <- B1 AND B2 AND ... AND Bn where head atom H can be inferred from body atoms"
    source: "Chunk 1:79-81"
    unique_aspects: "Symbolic, discrete primitive - contrasts with continuous embeddings"

  - term: "Path Rule"
    definition: "Logic rule where body is a path from head variable to tail variable: r(X,Y) <- r1(X,Z) AND r2(Z,Y)"
    source: "Chunk 1:151-153"
    unique_aspects: "Compositional structure - enables reasoning about multi-hop relations"

  - term: "Grounding"
    definition: "Replacing variables in rules with concrete entities, inferring implicit triples"
    source: "Chunk 1:169-171"
    unique_aspects: "Bridge between symbolic rules and data - materialization mechanism"

  - term: "Ontological Schema"
    definition: "High-level semantics (meta information) defined by OWL/RDFS describing class/relation structure"
    source: "Chunk 1:195-196"
    unique_aspects: "Declarative constraints on KG structure - not just data but data about data"

structural_patterns:
  - pattern_name: "Dual Reasoning Paradigm"
    structure: "Logic-based (symbolic, deductive, deterministic) <--> Embedding-based (neural, inductive, probabilistic)"
    instances:
      - "HermiT reasoner vs TransE embeddings"
      - "RDFox Datalog vs ComplEx/RotatE"
      - "Explicit triples vs predicted triples"
    source: "Chunk 1:19-27, 52-58"
    observation: "The entire paper is organized around this fundamental duality"

  - pattern_name: "Integration Stage Triad"
    structure: "Pre -> Joint -> Post injection of logics into embeddings"
    instances:
      - "Pre: Reasoning before embedding learning (impacts training samples)"
      - "Joint: Logic constraints during training (regularizers, loss extensions)"
      - "Post: Reasoning after embeddings learned (filter, combine predictions)"
    source: "Chunk 1:136-141"
    observation: "Temporal decomposition of integration - WHEN matters as much as WHAT"

  - pattern_name: "Data-based vs Model-based Mechanism"
    structure: "Adding new triples to training <--> Adding constraints on embeddings"
    instances:
      - "Grounding adds triples (data-based)"
      - "Regularization on relation embeddings (model-based)"
      - "Negative sampling from schema violations"
    source: "Chunk 1:143-147"
    observation: "Two fundamentally different ways to inject knowledge"

  - pattern_name: "Hierarchy Encoding Pattern"
    structure: "Type/Relation hierarchies encoded geometrically in embedding space"
    instances:
      - "Polar coordinates for entity hierarchies (HAKE)"
      - "Relation-specific spheres with nesting (TransRHS)"
      - "Cluster-relation-subrelation three-layer structure (HRS)"
    source: "Chunk 1:219-234"
    observation: "Geometric structure encodes ontological structure"

  - pattern_name: "Query Complexity Ladder"
    structure: "Path queries -> Conjunctive -> EPFO -> Full FOL (AND, OR, NOT, NEQ)"
    instances:
      - "Path queries (TransE-based traversal)"
      - "Conjunctive + AND (GQE)"
      - "+ Disjunction via DNF (Query2box)"
      - "+ Negation (BetaE, ConE)"
      - "+ Difference (NewLook)"
    source: "Chunk 1:394-410"
    observation: "Progressive extension of query expressiveness"

novel_concepts:
  - concept: "Differentiable Theorem Proving"
    definition: "Theorem proving that learns embeddings and compares symbols via embeddings rather than identical symbols"
    novelty_claim: "Enables Prolog-style reasoning to generalize to similar but not identical symbols"
    source: "Chunk 1:420-428"
    surprise: "Bridges discrete symbolic reasoning with continuous learned representations"

  - concept: "t-norm Fuzzy Logic Grounding"
    definition: "Using t-norm fuzzy logics to give truth scores to groundings based on truth values of all atoms"
    novelty_claim: "KALE trains groundings with negative sampling using fuzzy truth values"
    source: "Chunk 1:171-173"
    surprise: "Fuzzy logic as bridge between discrete rules and probabilistic embeddings"

  - concept: "TensorLog"
    definition: "Differentiable probabilistic logic establishing connection between first-order rule inference and sparse matrix multiplication"
    novelty_claim: "Compiles logical inference into differentiable numerical operations on matrices"
    source: "Chunk 1:470-473"
    surprise: "Logic as linear algebra - deep connection between symbolic and numeric"

  - concept: "Schema Correctness vs Silver Standard"
    definition: "Evaluation based on ontological schema consistency rather than held-out triples"
    novelty_claim: "SIC argues silver standard is 'highly questionable' - good benchmark results don't transfer"
    source: "Chunk 1:542-547"
    surprise: "Fundamental critique of how KG reasoning methods are evaluated"

  - concept: "Iterative Embedding-Rule Co-learning"
    definition: "Predicting labels for unlabeled triples dynamically based on current embeddings in each iteration"
    novelty_claim: "RUGE, IterE enable dynamic labeling rather than one-time grounding"
    source: "Chunk 1:175-180"
    surprise: "Emergent labels from embedding-rule interaction"

semantic_commitments:
  - commitment: "Open World Assumption"
    position: "KGs are incomplete - absence of triple doesn't mean falsity"
    implications: "Need prediction/inference for missing knowledge; cannot use closed-world negation"
    source: "Implicit throughout; explicit in handling 'noise and uncertainty' Chunk 1:56"

  - commitment: "Compositionality of Relations"
    position: "Complex relations can be composed from simpler ones (path rules)"
    implications: "r(X,Y) <- r1(X,Z) AND r2(Z,Y) - relations are compositional"
    source: "Chunk 1:151-153"

  - commitment: "Embedding Space Semantics"
    position: "Geometric relationships in vector space encode semantic relationships"
    implications: "Translation (TransE), rotation (RotatE), projection (Rot-Pro) all encode relation semantics"
    source: "Chunk 1:102-108, 244-250"

  - commitment: "Logic-Embedding Complementarity"
    position: "Neither alone is sufficient; integration preserves advantages of both"
    implications: "Logic = interpretable, transferable; Embeddings = uncertainty-tolerant, scalable"
    source: "Chunk 1:21-27, 55-58"

boundary_definitions:
  - entity_type: "Logic Types"
    identity_criteria: "Path rules vs Ontological schemas (can often be inter-converted)"
    boundary_cases: "Composition of relations - is it rule or schema? Paper notes they are 'not entirely distinct'"
    source: "Chunk 1:310-313"

  - entity_type: "Pre-defined vs Learned Logics"
    identity_criteria: "With: injecting predefined logics; Without: logics assumed existing but not explicitly given"
    boundary_cases: "Methods that learn hierarchies from embeddings (HAKE) - are these logics?"
    source: "Chunk 1:131-132"

  - entity_type: "Hybrid vs Neural Mechanism"
    identity_criteria: "Hybrid: inference still in symbolic space; Neural: all inference in vector space"
    boundary_cases: "NTP keeps variable binding symbolic but compares via embeddings - which is it?"
    source: "Chunk 1:350, 424-426"

temporal_modeling:
  - aspect: "Integration Stages as Temporal Phases"
    approach: "Pre/Joint/Post decomposition of when logic-embedding integration occurs"
    mechanism: "Pre affects training samples, Joint affects loss/constraints, Post affects inference"
    source: "Chunk 1:136-141"

  - aspect: "Iterative Learning"
    approach: "Multiple iterations of embedding-rule co-learning"
    mechanism: "Each iteration predicts new labels based on current embeddings"
    source: "Chunk 1:174-180"

  - aspect: "No Explicit Temporal Modeling"
    approach: "Paper focuses on static KG reasoning"
    mechanism: "No mention of temporal KGs, event sequences, or time-stamped facts"
    source: "Implicit - gap in coverage"

agency_spectrum:
  - agent_type: "No Explicit Agency Model"
    capabilities: "N/A"
    constraints: "Paper treats KG reasoning as system task, not agent task"
    source: "Implicit throughout"
    observation: "SURPRISE: Survey on KG reasoning has no agent ontology despite being central to AI systems"

knowledge_representation:
  - mechanism: "Triple-based KG"
    formalism: "RDF/OWL, with triples as atomic units"
    reasoning: "Deductive (logic-based) and inductive (embedding-based)"
    source: "Chunk 1:35-37"

  - mechanism: "Knowledge Graph Embeddings (KGE)"
    formalism: "Vectors in Euclidean/complex space"
    reasoning: "Score function evaluation, nearest-neighbor search, vector arithmetic"
    source: "Chunk 1:97-112"

  - mechanism: "Description Logics (OWL 2)"
    formalism: "SROIQ DL with class hierarchies, complex classes, relation properties"
    reasoning: "Consistency checking, materialization, query answering"
    source: "Chunk 1:86-94"

  - mechanism: "Logic Rules (Datalog-style)"
    formalism: "Horn clauses with head <- body structure"
    reasoning: "Forward chaining, backward chaining, rule mining"
    source: "Chunk 1:79-85"

  - mechanism: "Hybrid Query Representations"
    formalism: "Queries as embeddings (GQE), boxes (Query2box), Beta distributions (BetaE), cones (ConE)"
    reasoning: "Vector space operators for conjunction, disjunction, negation, projection"
    source: "Chunk 1:394-410"

emergence_indicators:
  - phenomenon: "Logic Pattern Discovery"
    mechanism: "Rule mining discovers implicit patterns from KG structure"
    evidence: "AMIE, AnyBURL, differentiable rule mining (NeuralLP, DRUM)"
    source: "Chunk 1:443-475"

  - phenomenon: "Hierarchy Emergence"
    mechanism: "Entity/relation hierarchies can be discovered from embeddings"
    evidence: "HAKE learns implicit hierarchies from polar coordinate structure"
    source: "Chunk 1:218-220"

  - phenomenon: "Iterative Refinement Convergence"
    mechanism: "Co-learning of embeddings and rules produces stable patterns"
    evidence: "IterE, RUGE show emergent labeling of unlabeled triples"
    source: "Chunk 1:175-180"

integration_surfaces:
  - surface: "OWL 2 Schema Language"
    connects_to: ["Description Logics (SROIQ)", "RDF", "SPARQL", "Datalog rules"]
    alignment_quality: "Strong - OWL 2 designed to support these integrations"
    source: "Chunk 1:86-94"

  - surface: "Score Functions"
    connects_to: ["TransE (translation)", "ComplEx (complex space)", "RotatE (rotation)", "Rot-Pro (projection+rotation)"]
    alignment_quality: "Good - all share triple-scoring interface"
    source: "Chunk 1:102-112"

  - surface: "Rule Grounding"
    connects_to: ["Symbolic rules", "Training triples", "Negative sampling"]
    alignment_quality: "Moderate - scalability issues with large KGs"
    source: "Chunk 1:169-182"

  - surface: "Pre-trained KG Models"
    connects_to: ["NLP pre-training paradigm", "Downstream KG applications"]
    alignment_quality: "Emerging - mentioned as future direction"
    source: "Chunk 1:556-559"

gaps_and_tensions:
  - gap_type: "Logic Diversity Challenge"
    description: "Most methods only support specific logic types; few support general ontological schemas"
    implications: "Real KGs have diverse logic types that need simultaneous support"
    source: "Chunk 1:496-504"

  - gap_type: "Explainability-Power Tradeoff"
    description: "Logic injection improves expressiveness but doesn't remove black-box nature; neural reasoning decreases transparency"
    implications: "Integrated methods may lose advantages of both approaches"
    source: "Chunk 1:514-529"

  - gap_type: "Benchmark Inadequacy"
    description: "Common benchmarks (WN18RR, FB15k-237, NELL) don't ensure diverse logic patterns"
    implications: "Methods may be evaluated on data that doesn't test their claimed capabilities"
    source: "Chunk 1:532-541"

  - gap_type: "Silver Standard Unreliability"
    description: "SIC argues benchmark results don't transfer to other KGs"
    implications: "Need schema correctness evaluation instead of held-out triple accuracy"
    source: "Chunk 1:542-547"

  - gap_type: "Scalability of Grounding"
    description: "Data-based methods that materialize rules don't scale to large KGs"
    implications: "Tension between completeness (ground all rules) and efficiency"
    source: "Chunk 1:180-182"

  - gap_type: "No Agent Model"
    description: "Survey on AI/KG reasoning has no ontology of agents, goals, or intentions"
    implications: "Gap between KG reasoning methods and agent architectures"
    source: "Implicit - not discussed"

  - gap_type: "No Temporal KGs"
    description: "No coverage of temporal knowledge graphs or event-based reasoning"
    implications: "Static KG assumption limits applicability to dynamic domains"
    source: "Implicit - not discussed"

  - gap_type: "Tension: Interpretability vs Generalization"
    description: "Differentiable proving (NTP) loses symbolic interpretability of variable bindings"
    implications: "Trade-off between symbolic clarity and neural generalization"
    source: "Chunk 1:424-430"

empirical_grounding:
  - type: "Benchmark datasets mentioned"
    domain: "General purpose KGs"
    scale: "WN18RR, FB15k-237, NELL - not specified in this survey"
    findings: "Used throughout cited papers but survey critiques their adequacy"
    source: "Chunk 1:534-535"

  - type: "Referenced applications"
    domain: "Multiple"
    scale: "Various"
    findings: "Information extraction, recommender systems, image classification, low-resource learning all mentioned as benefiting from KG+logic"
    source: "Chunk 1:550-553"

# SYNTHESIS NOTES

key_contributions:
  - "Comprehensive taxonomy of logic-embedding integration: Pre/Joint/Post stages, Data-based/Model-based mechanisms"
  - "Dual perspective organization: Logics-for-Embeddings AND Embeddings-for-Logics"
  - "Identification of four challenges: Logic diversity, Explainability, Benchmark adequacy, Application breadth"
  - "Query complexity ladder from path queries to full FOL"

surprising_findings:
  - "No agent ontology in an AI survey - KG reasoning treated as system property not agent capability"
  - "Silver standard evaluation is 'highly questionable' per SIC - fundamental methodology critique"
  - "TensorLog: logic inference as matrix multiplication - deep symbolic-numeric connection"
  - "Iterative co-learning produces emergent labels from embedding-rule interaction"

tensions_for_synthesis:
  - "Logic diversity vs unified framework - can one approach handle all logic types?"
  - "Interpretability vs power - integration seems to compromise both"
  - "Scalability vs completeness in grounding"
  - "Static KGs vs dynamic/temporal knowledge"

connections_to_other_papers:
  - "PROV-O: Could integrate provenance triples as special case of KG reasoning"
  - "Agent papers: Gap - no connection to agent goals/intentions despite being AI paper"
  - "Process mining (OCEL): Temporal events missing from KG reasoning taxonomy"
  - "UFO/BFO: Foundational ontologies not mentioned - KG schemas are shallower"

novel_synthesis_opportunities:
  - "Agent-aware KG reasoning: Add goal/intention predicates to knowledge graphs"
  - "Temporal KG embeddings: Extend score functions to handle time-stamped triples"
  - "Process-KG integration: Event sequences as special KG structures"
  - "Schema-grounded evaluation: Move beyond silver standard to ontological consistency"
---

# Knowledge Graph Reasoning with Logics and Embeddings: Survey and Perspective

## Paper Overview

This survey provides a comprehensive review of methods integrating symbolic logic-based reasoning with neural embedding-based reasoning for knowledge graphs. The authors organize the field around a fundamental duality: (1) injecting logics into embeddings and (2) utilizing embeddings for logic reasoning tasks.

## Core Contribution

The paper's primary contribution is a fine-grained categorization framework analyzing integration from multiple perspectives:

1. **Logic Types**: Path rules vs ontological schemas
2. **Pre-defined Logics**: With explicit logics vs learning implicit patterns
3. **Integration Stages**: Pre-training, Joint-training, Post-training
4. **Mechanisms**: Data-based (adding triples) vs Model-based (adding constraints)

## Key Technical Content

### Logics for Embeddings (Section 3)

Methods that inject logical constraints to improve embedding quality:

- **Path Rules**: PTransE, RPJE, ComplEx-NNE AER regularize relation embeddings
- **Grounding-based**: KALE, RUGE, IterE use t-norm fuzzy logic for truth scores
- **Class Hierarchies**: TKRL, HAKE encode type structures geometrically
- **Relation Properties**: ComplEx (asymmetric), RotatE (composition), Rot-Pro (transitive)

### Embeddings for Logics (Section 4)

Methods that use embeddings to enhance symbolic reasoning:

- **Query Answering**: Progressive expressiveness ladder
  - Path queries (TransE traversal)
  - Conjunctive (GQE)
  - EPFO with disjunction (Query2box)
  - Full FOL including negation (BetaE, ConE)

- **Theorem Proving**: NTP enables differentiable proving by comparing symbols via embeddings

- **Rule Mining**: NeuralLP, DRUM enable end-to-end differentiable rule learning

## Critical Gaps Identified

The paper explicitly identifies four challenges:

1. **Logic Diversity**: Most methods support only specific logic types
2. **Explainability**: Integration doesn't resolve black-box nature
3. **Benchmark Inadequacy**: Common datasets don't test diverse logic patterns
4. **Application Scope**: Few applications use both logics and embeddings

## Surprising Omissions

From a discovery perspective, notable gaps:

- **No Agent Ontology**: Despite being an AI survey, no treatment of agents, goals, or intentions
- **No Temporal Dimension**: Static KG assumption throughout
- **No Connection to Foundational Ontology**: UFO/BFO not mentioned - shallow schemas only
- **Benchmark Critique**: SIC's argument that silver standard is "highly questionable" is significant

## Relevance to Agent/Process Domains

This survey reveals a significant gap between KG reasoning research and agent architectures. The methods reviewed could theoretically support:

- Agent belief states as KG embeddings
- Goal inference as query answering
- Action effects as rule application

But these connections are not made explicit. The absence of temporal modeling also limits applicability to process/workflow domains.

## Quality Assessment

**Strengths**:
- Comprehensive coverage of integration approaches
- Clear categorization framework
- Honest acknowledgment of limitations
- Forward-looking challenge identification

**Limitations**:
- No empirical comparison of methods
- No coverage of temporal or dynamic KGs
- No connection to agent/multi-agent systems
- Benchmark critique not followed by alternatives
