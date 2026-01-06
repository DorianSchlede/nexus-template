# Knowledge Graphs - V2 Discovery Analysis

## Source
- **Paper**: Knowledge Graphs
- **Authors**: Hogan et al. (2021)
- **Type**: Comprehensive Survey
- **Focus**: Graph-based knowledge representation, storage, querying, and reasoning

---

## V2 Extraction Fields

### ontological_primitives

```yaml
ontological_primitives:
  - term: "Node"
    definition: "A vertex in a graph representing an entity of interest"
    source: "Chunk 13-14 (Formal Definitions)"
    unique_aspects: "Can be IRIs, blank nodes, or literals; context-dependent identity"

  - term: "Edge"
    definition: "A directed, labelled connection between nodes representing a relation"
    source: "Chunk 13-14 (Formal Definitions)"
    unique_aspects: "Always labelled; edge labels from set L; direction matters"

  - term: "Directed Edge-Labelled Graph"
    definition: "G = (V, E, L) where V is vertices, E is edges, L is labels; edge e = (u, l, v)"
    source: "Chunk 14 (Definition B.1)"
    unique_aspects: "Core model - simplest KG representation"

  - term: "Heterogeneous Graph"
    definition: "G = (V, E, L, l) with node typing function l: V -> L"
    source: "Chunk 14 (Definition B.2)"
    unique_aspects: "Nodes have explicit types; supports classification"

  - term: "Property Graph"
    definition: "G = (V, E, L, P, U, e, l, p) with properties on nodes and edges"
    source: "Chunk 14 (Definition B.3)"
    unique_aspects: "Richer than RDF; attribute-value pairs on both nodes and edges"

  - term: "Graph Dataset"
    definition: "D = (G_d, N) where G_d is default graph and N maps names to graphs"
    source: "Chunk 14 (Definition B.4)"
    unique_aspects: "Named graphs for context; provenance tracking"

  - term: "IRI (Internationalized Resource Identifier)"
    definition: "Global, persistent identifier for resources following RFC 3987"
    source: "Chunk 8 (Section 9.1)"
    unique_aspects: "Enables Linked Data; HTTP dereferenceable"

  - term: "Blank Node"
    definition: "Anonymous node without global identifier; local scope only"
    source: "Chunk 13-14"
    unique_aspects: "Existential semantics; problematic for identity across graphs"
```

### structural_patterns

```yaml
structural_patterns:
  - pattern_name: "Subject-Predicate-Object Triple"
    structure: "(s, p, o) where s is subject, p is predicate/relation, o is object"
    instances:
      - "RDF triple model"
      - "Edge in directed edge-labelled graph"
      - "SPARQL basic graph pattern"
    source: "Chunk 13-14 (Core throughout)"

  - pattern_name: "Graph Pattern"
    structure: "Set of edge patterns with variables; evaluated via homomorphism"
    instances:
      - "Basic Graph Pattern (BGP)"
      - "Complex Graph Pattern (with union, optional, negation)"
      - "Navigational Graph Pattern (with path expressions)"
    source: "Chunk 14 (Definitions B.5-B.8)"

  - pattern_name: "Schema-Instance Duality"
    structure: "Classes/properties at schema level; instances/edges at data level"
    instances:
      - "RDFS: rdfs:Class, rdfs:subClassOf"
      - "OWL: owl:Class, owl:ObjectProperty"
      - "Validating schema: shapes constrain instances"
    source: "Chunk 14 (Section B.3)"

  - pattern_name: "Quotient Graph (Emergent Schema)"
    structure: "Graph summarization via equivalence relation on nodes"
    instances:
      - "Simulation-based quotient"
      - "Bisimulation-based quotient"
      - "Type-based partitioning"
    source: "Chunk 14 (Definitions B.11-B.14)"

  - pattern_name: "Reification Pattern"
    structure: "Edge-as-node to attach metadata (time, provenance, certainty)"
    instances:
      - "RDF reification vocabulary"
      - "Named graphs"
      - "RDF-star (edge as subject/object)"
    source: "Chunk 8 (Section 3)"

  - pattern_name: "Knowledge Graph Completion Triad"
    structure: "Predict (subject, relation, ?) or (?, relation, object) or (subject, ?, object)"
    instances:
      - "Link prediction"
      - "Type prediction"
      - "Identity prediction (entity matching)"
    source: "Chunk 7-8 (Section 8.1)"
```

### novel_concepts

```yaml
novel_concepts:
  - concept: "Knowledge Graph (as comprehensive definition)"
    definition: "A graph of data intended to accumulate and convey knowledge of the real world, whose nodes represent entities of interest and whose edges represent relations between these entities"
    novelty_claim: "Unifies prior notions of semantic networks, knowledge bases, ontologies under graph-centric view"
    source: "Chunk 8 (Section 11)"

  - concept: "Knowledge Graph Embeddings"
    definition: "Low-dimensional vector representations of entities and relations preserving graph structure"
    novelty_claim: "Enables ML on symbolic knowledge; bridges deductive and inductive paradigms"
    source: "Chunk 15 (Table 8, Definitions B.17-B.21)"

  - concept: "Graph Neural Networks for KGs"
    definition: "Neural architectures operating on graph structure via message passing"
    novelty_claim: "Learns node representations incorporating neighborhood; enables inductive transfer"
    source: "Chunk 15 (Definitions B.22-B.24)"

  - concept: "Shapes Validation"
    definition: "Declarative constraints on graph structure using SHACL or ShEx"
    novelty_claim: "Closed-world validation separate from open-world ontological reasoning"
    source: "Chunk 14 (Definition B.10)"

  - concept: "Linked Data Principles"
    definition: "Use HTTP IRIs, provide useful RDF when dereferenced, include links to other IRIs"
    novelty_claim: "Technical basis for Web of Data; enables graph traversal across organizations"
    source: "Chunk 8 (Section 9.1.2)"

  - concept: "FAIR Principles for Knowledge Graphs"
    definition: "Findable, Accessible, Interoperable, Reusable data principles"
    novelty_claim: "Bridges scientific data management with semantic web; emphasizes machine-readability"
    source: "Chunk 8 (Section 9.1.1)"

  - concept: "Hypothesis Mining"
    definition: "Extracting rules or axioms from graph data to explain patterns"
    novelty_claim: "Generates symbolic knowledge from subsymbolic patterns; interpretability"
    source: "Chunk 15 (Definitions B.25-B.26)"
```

### semantic_commitments

```yaml
semantic_commitments:
  - commitment: "Open World Assumption"
    position: "Absence of information does not imply negation"
    implications: "Cannot derive false from missing edges; constrasts with database CWA"
    source: "Chunk 14 (Section B.4)"

  - commitment: "No Unique Name Assumption (in ontologies)"
    position: "Different IRIs may denote same entity unless stated otherwise"
    implications: "Requires explicit identity statements (owl:sameAs); affects constraint checking"
    source: "Chunk 7 (Section 7.3)"

  - commitment: "Graph-Centric Worldview"
    position: "Knowledge is fundamentally relational and best represented as labeled graphs"
    implications: "Entities exist in relation to others; isolation is meaningless"
    source: "Implicit throughout"

  - commitment: "Entity Realism"
    position: "Nodes represent real-world entities; edges represent real relations"
    implications: "Not merely syntactic; ontological commitment to reference"
    source: "Chunk 8 (Section 11 definition)"

  - commitment: "Extensibility over Completeness"
    position: "Knowledge graphs should be open to extension rather than closed and complete"
    implications: "No complete schema; collaborative editing; continuous enrichment"
    source: "Chunk 8 (Section 10.1.4 - Wikidata)"
```

### boundary_definitions

```yaml
boundary_definitions:
  - entity_type: "Entity (Node)"
    identity_criteria: "IRI provides global identity; blank nodes have local/existential identity"
    boundary_cases: "Same entity with different IRIs (owl:sameAs needed); blank node merging"
    source: "Chunk 14 (Definitions B.1-B.4)"

  - entity_type: "Knowledge Graph vs Database"
    identity_criteria: "KG: open-world, schema-flexible, identity-rich; DB: closed-world, fixed schema, primary keys"
    boundary_cases: "Property graphs blur boundary; graph databases increasingly KG-like"
    source: "Chunk 13 (Category definitions)"

  - entity_type: "Knowledge Graph vs Ontology"
    identity_criteria: "KG: primarily extensional (instance data); Ontology: primarily intensional (class definitions)"
    boundary_cases: "KGs include schema; distinction is emphasis not kind"
    source: "Chunk 13 (Historical discussion)"

  - entity_type: "Fact vs Claim"
    identity_criteria: "Fact: asserted as true; Claim: may be qualified with uncertainty, provenance, viewpoint"
    boundary_cases: "Wikidata 'claims' with references; contextualized assertions"
    source: "Chunk 8 (Section 10.1.4)"
```

### temporal_modeling

```yaml
temporal_modeling:
  - aspect: "Temporal Validity"
    approach: "Contextual annotations on edges with valid-time intervals"
    mechanism: "Reification, named graphs, or property graphs for temporal metadata"
    source: "Chunk 7 (Section 7.1.3 - Timeliness)"

  - aspect: "Knowledge Graph Evolution"
    approach: "Diff-based updates; change detection between versions"
    mechanism: "Version identifiers; temporal annotations; streaming updates"
    source: "Chunk 8 (Section 9.2.1 - Dumps)"

  - aspect: "Temporal Queries"
    approach: "Point-in-time or interval-based graph pattern matching"
    mechanism: "W3C Time Ontology; temporal RDF extensions"
    source: "Chunk 9 (References [107, 210])"

  - aspect: "Dynamic Knowledge Graph Embeddings"
    approach: "Embeddings that vary with time"
    mechanism: "Temporal plausibility functions; contextual embeddings"
    source: "Chunk 9 (Future directions)"
```

### agency_spectrum

```yaml
agency_spectrum:
  - agent_type: "Human Curator"
    capabilities: "Full editorial control; semantic judgment; quality assessment"
    constraints: "Scalability; consistency; coverage limitations"
    source: "Chunk 8 (Section 10.1.3 - Freebase, 10.1.4 - Wikidata)"

  - agent_type: "Extraction System"
    capabilities: "Scale; pattern recognition; multi-source integration"
    constraints: "Error propagation; semantic accuracy; schema alignment"
    source: "Chunk 7 (Section 7.1.2 - Semantic accuracy)"

  - agent_type: "Reasoning Engine"
    capabilities: "Deductive inference; consistency checking; entailment"
    constraints: "Scalability; expressivity/tractability tradeoff; open-world limits"
    source: "Chunk 14 (Section B.4)"

  - agent_type: "ML Model (Embeddings/GNN)"
    capabilities: "Pattern recognition; link prediction; soft inference"
    constraints: "Interpretability; symbolic grounding; training data bias"
    source: "Chunk 15 (Section B.5)"

# Note: Paper does not directly discuss AI agents or agentic systems - this is a GAP
```

### knowledge_representation

```yaml
knowledge_representation:
  - mechanism: "RDF (Resource Description Framework)"
    formalism: "Directed edge-labelled graphs with IRIs, blank nodes, literals"
    reasoning: "RDFS entailment; OWL reasoning; SPARQL querying"
    source: "Chunk 13-14 (Throughout)"

  - mechanism: "Property Graphs"
    formalism: "Nodes and edges with key-value properties"
    reasoning: "Cypher/Gremlin queries; no standard entailment"
    source: "Chunk 14 (Definition B.3)"

  - mechanism: "Description Logics"
    formalism: "ALC family (S, H, R, O, I, F, N, Q extensions)"
    reasoning: "TBox classification; ABox consistency; concept satisfiability"
    source: "Chunk 14 (Definition B.16)"

  - mechanism: "Rules (Datalog-style)"
    formalism: "If-then rules with variables; body-head structure"
    reasoning: "Forward chaining (materialization); backward chaining (query rewriting)"
    source: "Chunk 14 (Definition B.15)"

  - mechanism: "Knowledge Graph Embeddings"
    formalism: "Vectors/tensors for entities and relations"
    reasoning: "Plausibility scoring; nearest neighbor; vector arithmetic"
    source: "Chunk 15 (Table 8)"

  - mechanism: "Graph Neural Networks"
    formalism: "Message passing on graph structure"
    reasoning: "Node classification; link prediction; graph classification"
    source: "Chunk 15 (Definitions B.22-B.24)"
```

### emergence_indicators

```yaml
emergence_indicators:
  - phenomenon: "Web of Data"
    mechanism: "Individual knowledge graphs linked via IRIs create emergent global graph"
    evidence: "Linked Open Data cloud; federated queries across datasets"
    source: "Chunk 8 (Section 9.1.2)"

  - phenomenon: "Collective Knowledge Construction"
    mechanism: "Collaborative editing produces knowledge no individual contributor created"
    evidence: "Wikidata: multilingual, multi-viewpoint claims from distributed editors"
    source: "Chunk 8 (Section 10.1.4)"

  - phenomenon: "Emergent Schema"
    mechanism: "Quotient graphs reveal structure not explicitly designed"
    evidence: "Type distributions; path patterns; clustering from data"
    source: "Chunk 14 (Definitions B.11-B.14)"

  - phenomenon: "Enterprise Knowledge Integration"
    mechanism: "Multiple data sources unified reveal cross-domain patterns"
    evidence: "Google Knowledge Graph connecting search, advertising, services"
    source: "Chunk 8 (Section 10.2)"
```

### integration_surfaces

```yaml
integration_surfaces:
  - surface: "RDF/Property Graph"
    connects_to: ["RDF directed edge-labelled graph", "Property graph model", "GQL upcoming standard"]
    alignment_quality: "Active standardization effort; property graphs more expressive locally, RDF more expressive globally"
    source: "Chunk 13-14 (Definitions B.1-B.3)"

  - surface: "Ontology/Schema Layer"
    connects_to: ["RDFS", "OWL", "SHACL/ShEx", "Schema.org"]
    alignment_quality: "RDFS/OWL for inference; SHACL/ShEx for validation; complementary"
    source: "Chunk 14 (Section B.3)"

  - surface: "External Knowledge Bases"
    connects_to: ["DBpedia", "Wikidata", "YAGO", "Freebase (legacy)"]
    alignment_quality: "owl:sameAs linking; entity alignment; varying quality"
    source: "Chunk 8 (Section 10.1)"

  - surface: "Machine Learning"
    connects_to: ["Knowledge graph embeddings", "GNNs", "Neuro-symbolic approaches"]
    alignment_quality: "Active research area; entailment-aware embeddings; rule mining"
    source: "Chunk 9 (Future directions)"

  - surface: "Natural Language"
    connects_to: ["NER", "Relation extraction", "Question answering", "Text generation"]
    alignment_quality: "Bidirectional: NLP populates KGs; KGs ground NLP"
    source: "Chunk 7-8 (Sections 6, 8.2.1)"
```

### gaps_and_tensions

```yaml
gaps_and_tensions:
  - gap_type: "Omission"
    description: "No treatment of AI agents or autonomous systems using KGs"
    implications: "Cannot directly apply to agentic AI architectures"
    source: "Implicit - published 2021 before LLM agent explosion"

  - gap_type: "Omission"
    description: "Limited discussion of real-time/streaming knowledge graphs"
    implications: "Event-driven architectures underspecified"
    source: "Chunk 9 (Mentioned as future direction)"

  - gap_type: "Tension"
    description: "Open-world semantics vs. validation constraints"
    implications: "SHACL validates but doesn't entail; OWL entails but can't validate"
    source: "Chunk 14 (Section B.3.2 vs B.4)"

  - gap_type: "Tension"
    description: "Scalability vs. Expressivity in reasoning"
    implications: "Full OWL 2 DL intractable; practical systems use fragments"
    source: "Chunk 14 (Section B.4.3)"

  - gap_type: "Tension"
    description: "Symbolic deduction vs. Statistical induction"
    implications: "Embeddings lose interpretability; rules lose soft patterns"
    source: "Chunk 9 (Future directions - neuro-symbolic)"

  - gap_type: "Underspecified"
    description: "Process/workflow representation in knowledge graphs"
    implications: "KGs model static relations well; dynamic processes less clear"
    source: "Implicit - no dedicated section"

  - gap_type: "Underspecified"
    description: "Multi-modal knowledge graphs (images, audio, video)"
    implications: "Mentioned as future challenge; no concrete approach"
    source: "Chunk 9 (Future directions - diversity)"
```

### empirical_grounding

```yaml
empirical_grounding:
  - type: "Production Deployment"
    domain: "Web Search"
    scale: "Billions of edges (Google, Bing Knowledge Graphs)"
    findings: "Powers knowledge panels; entity-centric search"
    source: "Chunk 8 (Section 10.2.1)"

  - type: "Open Knowledge Graph"
    domain: "General/Cross-domain"
    scale: "Wikidata: 100M+ items; DBpedia: billions of triples"
    findings: "Collaborative construction viable; multilingual coverage"
    source: "Chunk 8 (Section 10.1)"

  - type: "Enterprise Deployment"
    domain: "E-commerce, Social Networks, Finance"
    scale: "Amazon, LinkedIn, Bloomberg - billions of edges"
    findings: "ROI in search, recommendations, analytics"
    source: "Chunk 8 (Sections 10.2.2-10.2.4)"

  - type: "Query Workload Analysis"
    domain: "Public SPARQL Endpoints"
    scale: "Millions of queries analyzed"
    findings: "Most queries tractable; worst-case rare in practice"
    source: "Chunk 8 (Section 9.2.4, Reference [62])"

  - type: "Domain-specific KGs"
    domain: "Life Sciences, Publications, Government"
    scale: "Bio2RDF, OpenCitations, data.gov"
    findings: "Integration use case dominant; quality varies"
    source: "Chunk 8 (Section 10.1.6)"
```

---

## Chunk Index

| Chunk | V2 Fields Found |
|-------|-----------------|
| 1 | Introduction, basic definitions (ontological_primitives) |
| 2 | Graph models, RDF basics (structural_patterns, knowledge_representation) |
| 3 | Schema, context, identity (boundary_definitions, semantic_commitments) |
| 4 | Ontologies, OWL (knowledge_representation, semantic_commitments) |
| 5 | Deductive reasoning, rules (knowledge_representation) |
| 6 | Inductive reasoning, embeddings (novel_concepts, knowledge_representation) |
| 7 | Quality dimensions (gaps_and_tensions, temporal_modeling) |
| 8 | Refinement, publication, practice (empirical_grounding, integration_surfaces, novel_concepts) |
| 9 | References, future directions (gaps_and_tensions, emergence_indicators) |
| 10 | References continued |
| 11 | References continued |
| 12 | References continued |
| 13 | Historical context, definition categories (boundary_definitions, semantic_commitments) |
| 14 | Formal definitions: graphs, patterns, schema, reasoning (ontological_primitives, structural_patterns, knowledge_representation) |
| 15 | Embeddings, GNNs, hypothesis mining (novel_concepts, knowledge_representation) |

---

## Discovery Notes

### Surprises
1. **Four distinct definition categories** for "knowledge graph" - from simple graph to extensional/philosophical
2. **Quotient graphs as emergent schema** - structure discovered rather than designed
3. **Strong emphasis on publication/access protocols** - significant infrastructure concern
4. **Hypothesis mining** as formal counterpart to KG embeddings - symbolic extraction from patterns

### Key Terminology (Paper's Own)
- "Knowledge graph" (intentionally loose definition)
- "Directed edge-labelled graph" (preferred over "RDF graph")
- "Validating schema" vs "semantic schema" (key distinction)
- "Emergent schema" (quotient-based)
- "Plausibility" (for embedding-based scoring)
- "Fact validation" vs "link prediction" (external vs internal)

### Notable Absences
- No discussion of agents/agency in the AI sense
- No treatment of causal reasoning
- No discussion of temporal logic/event calculus
- Limited process/workflow modeling
- No mention of LLMs (published 2021)

---

## Metadata

```yaml
extraction_version: "V2 Discovery"
extraction_date: "2025-12-31"
extractor: "Claude Opus 4.5"
paper_chunks: 15
total_characters: ~650,000
primary_contribution: "Comprehensive survey unifying KG concepts across communities"
relevance_to_project: "HIGH - foundational for understanding KG primitives, but gaps for agentic systems"
```
