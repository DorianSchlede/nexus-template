---
batch_id: 1
field: entity_relationships
papers_read: [02-Knowledge_Graphs, 04-PROV-O_to_BFO_Semantic_Mapping, 05-DOLCE_Descriptive_Ontology, 06-BFO_Function_Role_Disposition, 07-Classifying_Processes_Barry_Smith]
chunks_read: 6
patterns_found: 47
extracted_at: "2025-12-28T14:30:00Z"
---

# Batch Extraction: entity_relationships (Batch 1)

## Patterns Extracted

### Pattern: Disjointness Axiom Relationship

- **Source**: 02-Knowledge_Graphs (Chunk 6:19-31)
- **Description**: Disjointness axioms define that two classes cannot have overlapping instances - the intersection of the classes is equivalent to the empty class. This is a fundamental structural relationship that constrains entity classification.
- **Quote**: "the disjointness axiom DomesticAirport ⊓ InternationalAirport ≡⊥ states that the intersection of the two classes is equivalent to the empty class, or in simpler terms, no node can be simultaneously of type [Domestic Airport] and [International Airport]"
- **Context**: Discussion of axiom mining from knowledge graphs, specifically how disjointness axioms are extracted using negative association rule mining.

### Pattern: Class Learning Through Positive/Negative Examples

- **Source**: 02-Knowledge_Graphs (Chunk 6:59-75)
- **Description**: DL Learner performs class learning where given positive and negative node sets, it finds logical class descriptions that divide them. This defines relationships between entities based on their properties.
- **Quote**: "given a set of positive nodes and negative nodes, the goal is to find a logical class description that divides the positive and negative sets. For example, given { [Iquique], [Arica] } as the positive set and { [Santiago] } as the negative set, we may learn a (DL) class description ∃nearby.Airport ⊓¬(∃capital[−].⊤), denoting entities near to an airport that are not capitals"
- **Context**: Description of DL Learner system for mining axioms from knowledge graphs.

### Pattern: Entity Linking Association

- **Source**: 02-Knowledge_Graphs (Chunk 6:233-257)
- **Description**: Entity Linking (EL) associates mentions of entities in text with existing nodes of a target knowledge graph, handling multiple mentions of the same entity and disambiguation of identical mentions to different entities.
- **Quote**: "The EL task associates mentions of entities in a text with the existing nodes of a target knowledge graph... First, there may be multiple ways to mention the same entity, as in the case of [Rapa Nui] and [Easter Island]; if we created a node [Rapa Nui] to represent that mention, we would split the information available under both mentions across different nodes"
- **Context**: Discussion of text extraction techniques for building knowledge graphs.

### Pattern: Binary Relation Extraction

- **Source**: 02-Knowledge_Graphs (Chunk 6:274-296)
- **Description**: Relation Extraction (RE) extracts relations between entities in text, either in a closed setting with fixed relation types or open setting where relations are discovered from text.
- **Quote**: "The RE task extracts relations between entities in the text... The simplest case is that of extracting binary relations in a closed setting wherein a fixed set of relation types are considered... Binary RE can also be applied using unsupervised methods in an open setting – often referred to as Open Information Extraction (OIE) – whereby the set of target relations is not pre-defined but rather extracted from text"
- **Context**: Explanation of how relations are extracted from text for knowledge graph construction.

### Pattern: N-ary Relation with Frame Semantics

- **Source**: 02-Knowledge_Graphs (Chunk 6:298-316)
- **Description**: N-ary relations capture additional context for how entities are related, using frame semantics where for a given verb, it captures the entities involved and how they may be interrelated.
- **Quote**: "Various methods for n-ary RE are based on frame semantics, which, for a given verb (e.g., 'named'), captures the entities involved and how they may be interrelated. Resources such as FrameNet then define frames for words, such as to identify that the semantic frame for 'named' includes a speaker (the person naming something), an entity (the thing named) and a name"
- **Context**: Discussion of extracting complex relations that capture temporal and contextual information.

### Pattern: Discourse Representation Theory Relations

- **Source**: 02-Knowledge_Graphs (Chunk 6:316-328)
- **Description**: DRT considers a logical representation of text based on existential events, relating entities through patient and other semantic roles.
- **Quote**: "the naming of Easter Island as a World Heritage Site is considered to be an (existential) event where Easter Island is the patient (the entity affected), leading to the logical (neo-Davidsonian) formula: ∃e: naming(e), patient(e, [Easter Island]), name(e, [World Heritage Site])"
- **Context**: Explanation of how Discourse Representation Theory represents relations as reification.

### Pattern: Direct Mapping from Tables

- **Source**: 02-Knowledge_Graphs (Chunk 6:596-611)
- **Description**: Direct mapping automatically generates a graph from a table, creating edges for each cell where the row represents the subject, column name represents the predicate, and cell value represents the object.
- **Quote**: "A direct mapping automatically generates a graph from a table... which creates an edge [x] y z for each (non-header, non-empty, non-null) cell of the table, such that [x] represents the row of the cell, y the column name of the cell, and [z] the value of the cell"
- **Context**: Discussion of mapping structured sources to knowledge graphs.

### Pattern: Foreign Key Linking

- **Source**: 02-Knowledge_Graphs (Chunk 6:615-621)
- **Description**: Foreign key relationships in relational databases can be mapped to links between entity nodes in knowledge graphs.
- **Quote**: "In case of a foreign key between two tables – such as Report.claimant referencing Claimant.id - we can link, for example, to [Claimant-XY12SDA] rather than [XY12SDA], where the former node also has the name and country of the claimant"
- **Context**: Explanation of how database foreign keys translate to graph relationships.

### Pattern: Ontology Design Pattern Relationships

- **Source**: 02-Knowledge_Graphs (Chunk 6:827-846)
- **Description**: Ontology Design Patterns (ODPs) specify generalizable ontology modeling patterns that define relationships between entities in specific domains.
- **Quote**: "Ontology Design Patterns (ODPs) are another common feature of modern methodologies, specifying generalisable ontology modelling patterns that can be used as inspiration for modelling similar patterns, as modelling templates, or as directly reusable components"
- **Context**: Discussion of ontology engineering methodologies.

### Pattern: Accuracy as Entity-Reality Correspondence

- **Source**: 02-Knowledge_Graphs (Chunk 7:20-24)
- **Description**: Accuracy refers to the extent to which entities and relations encoded by nodes and edges correctly represent real-life phenomena.
- **Quote**: "Accuracy refers to the extent to which entities and relations – encoded by nodes and edges in the graph – correctly represent real-life phenomena. Accuracy can be further sub-divided into three dimensions: syntactic accuracy, semantic accuracy, and timeliness"
- **Context**: Quality assessment dimensions for knowledge graphs.

### Pattern: Linkability Completeness

- **Source**: 02-Knowledge_Graphs (Chunk 7:107-108)
- **Description**: Linkability completeness refers to the degree to which instances in the dataset are interlinked.
- **Quote**: "linkability completeness refers to the degree to which instances in the data set are interlinked"
- **Context**: Discussion of completeness as a quality dimension.

### Pattern: Consistency Through Logical Contradiction

- **Source**: 02-Knowledge_Graphs (Chunk 7:168-176)
- **Description**: Consistency means a knowledge graph is free of logical contradictions with respect to the particular logical entailment considered.
- **Quote**: "Consistency means that a knowledge graph is free of (logical/formal) contradictions with respect to the particular logical entailment considered... 'not' condition can give rise to inconsistencies if the negated condition is entailed"
- **Context**: Coherency quality dimension for knowledge graphs.

### Pattern: Validity Through Shape Constraints

- **Source**: 02-Knowledge_Graphs (Chunk 7:179-191)
- **Description**: Validity means the knowledge graph is free of constraint violations, such as cardinality restrictions captured by shape expressions.
- **Quote**: "Validity means that the knowledge graph is free of constraint violations, such as captured by shape expressions. We may, for example, specify a shape City whose target nodes have at most one country. Then, given the edges [Chile] country Santiago country Cuba, and assuming that [Santiago] becomes a target of City, we have a constraint violation"
- **Context**: Discussion of validity as a coherency sub-dimension.

### Pattern: Identity Link Prediction

- **Source**: 02-Knowledge_Graphs (Chunk 7:358-379)
- **Description**: Identity-link prediction searches for nodes that refer to the same entity, using value matchers and context matchers to determine similarity.
- **Quote**: "Predicting identity links involves searching for nodes that refer to the same entity... Such techniques are generally based on two types of matchers: value matchers determine how similar the values of two entities on a given property are... while context matchers consider the similarity of entities based on various nodes and edges"
- **Context**: Knowledge graph completion through identity linking.

### Pattern: Ontology Mapping Relationship

- **Source**: 04-PROV-O_to_BFO_Semantic_Mapping (Chunk 1:51-54)
- **Description**: An ontology mapping is a statement <s, p, o> where s is a subject term from one ontology, o is an object term from another ontology, and p specifies how they relate.
- **Quote**: "An ontology mapping, or correspondence, is a statement <s, p, o> such that 's' is a subject term representing a class or object property in a ontology, 'o' is an object term representing a class or object property in some other ontology, and 'p' is a predicate that specifies how s and o relate"
- **Context**: Introduction to ontology alignment methodology.

### Pattern: Equivalence Relation Mapping

- **Source**: 04-PROV-O_to_BFO_Semantic_Mapping (Chunk 1:146-156)
- **Description**: Equivalence relations using OWL equivalentClass/equivalentProperty give necessary and sufficient conditions for something to be an instance of classes in both ontologies.
- **Quote**: "Equivalence relations represented by OWL equivalentClass and OWL equivalentProperty give necessary and sufficient conditions for something to be an instance of a certain BFO class or relation and a certain PROV-O class or relation at the same time. Everything that satisfies these conditions will be an instance of both, and nothing else will be an instance of either"
- **Context**: Mapping relation types for ontology alignment.

### Pattern: Subsumption Relation Mapping

- **Source**: 04-PROV-O_to_BFO_Semantic_Mapping (Chunk 1:158-164)
- **Description**: Subsumption relations using RDFS subClassOf/subPropertyOf give sufficient conditions for an instance of one class to be an instance of another.
- **Quote**: "Subsumption relations represented by RDFS subClassOf or RDFS subPropertyOf give sufficient conditions for an instance of one class or relation to be an instance of another class or relation. If a certain PROV-O class is a subclass of a certain BFO class, then all the instances of the PROV-O class are also instances of the corresponding BFO class"
- **Context**: Mapping relation types for ontology alignment.

### Pattern: Coherent Alignment Satisfiability

- **Source**: 04-PROV-O_to_BFO_Semantic_Mapping (Chunk 1:213-221)
- **Description**: An ontology alignment is coherent if and only if all formulae in the aligned ontologies are satisfiable, meaning every formula can be true in some interpretation.
- **Quote**: "An ontology alignment is coherent if and only if all formulae in the aligned ontologies are satisfiable, i.e. it is possible for every formula to be true in some interpretation (a model). An incoherent alignment might contain classes that cannot have instances"
- **Context**: Criteria for evaluating ontology alignments.

### Pattern: Conservative Extension Preservation

- **Source**: 04-PROV-O_to_BFO_Semantic_Mapping (Chunk 1:241-267)
- **Description**: The conservativity principle states that an ontology alignment should not change the semantic relationships between terms within each ontology.
- **Quote**: "The conservativity principle states that an ontology alignment should not change the semantic relationships between terms within each ontology. This is based on the notion of a conservative extension of a logical theory, which does not introduce or eliminate entailments expressed in the signature of that theory"
- **Context**: Criterion for maintaining semantic integrity in alignments.

### Pattern: PROV Entity to BFO Continuant Mapping

- **Source**: 04-PROV-O_to_BFO_Semantic_Mapping (Chunk 1:633-645)
- **Description**: PROV Entity is mapped as a subclass of BFO continuant (excluding spatial regions), preserving the disjoint relationship with PROV Activity through the continuant/occurrent distinction.
- **Quote**: "PROV Entity is defined as 'a physical, digital, conceptual, or other kind of thing with some fixed aspects'. We therefore map PROV Entity as a subclass of BFO continuant with one exception... This axiom ensures that any other subclass of BFO continuant... is not automatically entailed to be a superclass of PROV Entity"
- **Context**: Specific mapping of PROV-O Starting Point classes.

### Pattern: PROV Agent Participation Relationship

- **Source**: 04-PROV-O_to_BFO_Semantic_Mapping (Chunk 1:654-668)
- **Description**: PROV Agent is mapped as a subclass of BFO material entities that both participate in some PROV Activity and bear some BFO role that is realized in a PROV Activity.
- **Quote**: "PROV Agent is mapped as a subclass of BFO material entities that both participate in some PROV Activity and bear some BFO role that is realized in a PROV Activity... The definition of PROV Agent also states that an agent 'bears some form of responsibility for an activity taking place, for the existence of an entity, or another agent's activity'"
- **Context**: Mapping of agent relationships between ontologies.

### Pattern: PROV Activity to BFO Process Equivalence

- **Source**: 04-PROV-O_to_BFO_Semantic_Mapping (Chunk 1:682-691)
- **Description**: PROV Activity is mapped as equivalent to BFO process, both representing something that occurs over a period of time.
- **Quote**: "PROV Activity is mapped as equivalent to the class BFO process. The definition of PROV Activity includes 'something that occurs over a period of time and acts upon or with entities'. Similarly, a BFO occurrent - the parent class of BFO process - is defined as 'an entity that unfolds itself in time'"
- **Context**: Core equivalence mapping between provenance and foundational ontology.

### Pattern: wasGeneratedBy Property Chain

- **Source**: 04-PROV-O_to_BFO_Semantic_Mapping (Chunk 1:735-744)
- **Description**: PROV wasGeneratedBy is mapped as a subproperty of BFO participates in, connecting entities that are outputs of processes.
- **Quote**: "Since the domain and range of PROV wasGeneratedBy are PROV Entity and PROV Activity, respectively, it is mapped as a subproperty of BFO participates in, whose domain and range are non-spatial region continuants and process, respectively"
- **Context**: Object property mappings for provenance relations.

### Pattern: PROV Influence as Process/Process Boundary

- **Source**: 04-PROV-O_to_BFO_Semantic_Mapping (Chunk 1:911-920)
- **Description**: PROV Influence is mapped to the disjoint union of BFO process and BFO process boundary, with subclasses mapped accordingly based on temporal characteristics.
- **Quote**: "PROV Influence, as the superclass of 16 Qualified Influence classes, is mapped to a subclass of the disjoint union of BFO process and BFO process boundary. Some of its subclasses such as PROV Generation, PROV Start, and PROV End are subsumed under PROV InstantaneousEvent, which is equivalently mapped to BFO process boundary"
- **Context**: Mapping of qualified influence patterns.

### Pattern: Endurant vs Perdurant Distinction

- **Source**: 05-DOLCE_Descriptive_Ontology (Chunk 1:128-137)
- **Description**: Endurants (continuants) are wholly present at any time they exist, while perdurants (occurrents) can be partially present with temporal parts. This is the fundamental distinction between entities in DOLCE.
- **Quote**: "while endurants may acquire and lose properties and parts through time, perdurants are fixed in time. Their fundamental difference concerns therefore their presence in time: endurants are wholly present (i.e., with all their parts) at any time in which they are present; differently, perdurants can be partially present, so that at any time in which they unfold only a part of them is present"
- **Context**: Principles and structure of DOLCE ontology.

### Pattern: Participation Relation

- **Source**: 05-DOLCE_Descriptive_Ontology (Chunk 1:134-137)
- **Description**: The participation relation connects endurants and perdurants - an endurant is in time by participating in a perdurant, and perdurants happen by having endurants as participants.
- **Quote**: "The relation connecting endurants and perdurants is called participation. An endurant can be in time by participating in a perdurant, and perdurants happen in time by having endurants as participants. For instance, a person is in time by participating to her own life, and a conference talk happens if at least one presenter (or attendant) participates to it"
- **Context**: Explanation of the core relation bridging continuants and occurrents.

### Pattern: Independent vs Dependent Entity

- **Source**: 05-DOLCE_Descriptive_Ontology (Chunk 1:148-154)
- **Description**: Features are endurants whose existence depends on some physical object (the feature bearer), while physical objects are independent entities. This dependence relationship structures the taxonomy.
- **Quote**: "features (e.g., edges, holes, bumps, etc.) are endurants whose existence depends on some physical object (the feature bearer), while physical objects are independent entities, i.e., their existence does not require other endurants to exist"
- **Context**: Discussion of independence vs dependence across DOLCE categories.

### Pattern: Quality Inherence Relation

- **Source**: 05-DOLCE_Descriptive_Ontology (Chunk 1:168-181)
- **Description**: Qualities are particulars that inhere in endurants or perdurants, specific to their bearers. The quale represents the position of a quality within a quality space, allowing comparison.
- **Quote**: "Qualities are, roughly speaking, what can be perceived and measured; they are particulars inhering in endurants or perdurants. For example, when we talk about the red of a rose, we are talking about a particular quality (that specific red) which inheres in a particular endurant (that specific rose)"
- **Context**: Explanation of how properties relate to entities in DOLCE.

### Pattern: Role Classification Relation

- **Source**: 05-DOLCE_Descriptive_Ontology (Chunk 1:184-189)
- **Description**: Roles are represented as social concepts connected to entities by the classification relation. Roles are anti-rigid (dynamic) and founded (relational in nature, depending on other roles and contexts).
- **Quote**: "Roles are represented as (social) concepts, which are connected to other entities (like endurants, perdurants, and abstracts) by the relation of classification. In particular, roles are concepts that are anti-rigid and founded, meaning that (i) they have dynamic properties and (ii) they have a relational nature, i.e. they depend on other roles and on contexts"
- **Context**: Description of role modeling in DOLCE.

### Pattern: Temporary Parthood Relation

- **Source**: 05-DOLCE_Descriptive_Ontology (Chunk 1:253-268)
- **Description**: DOLCE uses both atemporal parthood P(x,y) and time-dependent parthood P(x,y,t), with temporary parthood only holding between endurants at specific times when both are present.
- **Quote**: "DOLCE assumes two primitive parthood relations: atemporal (P(x, y) for 'x is part of y') and time-dependent (P(x, y, t) for 'x is part of y at time t') parthood... Axiom (a1) states that temporary parthood holds only between two endurants at some time, axiom (a2) states that to have a parthood relationship both the part and the whole must be present"
- **Context**: Formalization of mereology in DOLCE.

### Pattern: Constitution Relation

- **Source**: 05-DOLCE_Descriptive_Ontology (Chunk 1:208-214)
- **Description**: Constitution is a temporalized relation holding between entities that are spatio-temporally co-located but distinguishable for their histories, persistence conditions, or relational properties.
- **Quote**: "Constitution is another temporalized relation in DOLCE, holding between either endurants or perdurants. It is often used to single out entities that are spatio-temporally co-located but nonetheless distinguishable for their histories, persistence conditions, or relational properties. A typical example of constitution is the relation between a statue and the amount of matter it is built with"
- **Context**: Explanation of how constitution differs from composition.

### Pattern: Constant Participation

- **Source**: 05-DOLCE_Descriptive_Ontology (Chunk 1:369-380)
- **Description**: Constant participation (PCC) defines participation that holds throughout the whole perdurant - whenever the perdurant is present, the endurant participates in it.
- **Quote**: "PCC(x, y) = ∃t(PRE(y, t)) ∧ ∀t(PRE(y, t) → PC(x, y, t)) (Const. Participation, cf. Dd63)"
- **Context**: Formalization of participation relations.

### Pattern: Classification Relation Properties

- **Source**: 05-DOLCE_Descriptive_Ontology (Chunk 1:405-430)
- **Description**: The classification relation CF(x,y,t) applies to an endurant, concept, and time. It is asymmetrical, requires presence, and avoids circularity through transitivity restrictions.
- **Quote**: "The classification relationship CF applies to an endurant, a concept and a time (a14), requires the endurant to be present when it is classified (a15), and is not symmetrical (a16). A concept can classify other concepts but not what the latter classify, this is stated to avoid circularity (a17)"
- **Context**: Formalization of concepts, roles, and classification.

### Pattern: Composition vs Constitution in Artifacts

- **Source**: 05-DOLCE_Descriptive_Ontology (Chunk 1:486-497)
- **Description**: Constitution connects elements with different essential properties (intercategorical), while composition holds between elements with same essential properties (intracategorical).
- **Quote**: "The constitution and composition relations in DOLCE capture distinct forms of dependence: the former is the dependence holding between entities with different essential properties (intercategorical) like the dependence of a table from the matter it is made of; the latter holds between entities with the same essential properties (intracategorical) like the dependence of a table from the tabletop and the legs"
- **Context**: Case study analysis of table composition.

### Pattern: Inherence as One-Sided Existential Dependence

- **Source**: 06-BFO_Function_Role_Disposition (Chunk 1:186-191)
- **Description**: Dependent continuants are related to their bearers by inherence, a one-sided existential dependence relation where the dependent entity cannot exist without its specific bearer.
- **Quote**: "Dependent continuants are related to their bearers by inherence. Inherence is defined as a one-sided, existential dependence relation. This means that, in order for a dependent continuant to exist, some other independent continuant must exist to serve as its bearer"
- **Context**: BFO's treatment of dependent entities.

### Pattern: Specific vs Generic Dependence

- **Source**: 06-BFO_Function_Role_Disposition (Chunk 1:189-211)
- **Description**: Specifically dependent continuants (like qualities, functions, roles) cannot migrate between bearers, while generically dependent continuants (like pdf files) can exist in multiple bearers through copying.
- **Quote**: "Specifically dependent continuants, such as headaches or talents, cannot migrate from one bearer to another, as contrasted with generically dependent continuants, such as the pdf file on your laptop, which can exist in a multiplicity of bearers"
- **Context**: Classification of dependence types in BFO.

### Pattern: Realizable Entity Realization

- **Source**: 06-BFO_Function_Role_Disposition (Chunk 1:221-243)
- **Description**: Functions, roles, dispositions and capabilities are realizable entities whose instances can be realized (manifested, actualized, executed) in associated processes in which the bearer participates.
- **Quote**: "A realizable entity is defined as a specifically dependent continuant that has an independent continuant entity as its bearer, and whose instances can be realized (manifested, actualized, executed) in associated processes in which the bearer participates"
- **Context**: Definition of realizable entities and their process connections.

### Pattern: Role as Externally-Grounded Realizable

- **Source**: 06-BFO_Function_Role_Disposition (Chunk 1:268-286)
- **Description**: A role exists because the bearer is in some special circumstances (physical, social, or institutional) that the bearer does not have to be in, and losing the role does not change the bearer's physical make-up.
- **Quote**: "A role is a realizable entity which exists because the bearer is in some special physical, social, or institutional set of circumstances in which the bearer does not have to be, and is not such that, if it ceases to exist, then the physical make-up of the bearer is thereby changed"
- **Context**: Definition distinguishing roles from dispositions.

### Pattern: Disposition as Internally-Grounded Realizable

- **Source**: 06-BFO_Function_Role_Disposition (Chunk 1:333-340)
- **Description**: A disposition is a realizable entity where if it ceases to exist, its bearer is physically changed, and its realization occurs in virtue of the bearer's physical make-up when in special circumstances.
- **Quote**: "A disposition is a realizable entity which is such that, if it ceases to exist, then its bearer is physically changed, and whose realization occurs in virtue of the bearer's physical make-up when this bearer is in some special physical circumstances"
- **Context**: Definition of disposition in contrast to role.

### Pattern: Function as Designed/Evolved Disposition

- **Source**: 06-BFO_Function_Role_Disposition (Chunk 1:385-408)
- **Description**: A function is a disposition that exists in virtue of the bearer's physical make-up, which the bearer possesses because it came into being through evolution (biological) or intentional design (artifacts) to realize processes of a certain sort.
- **Quote**: "A function is a disposition that exists in virtue of the bearer's physical make-up, and this physical make-up is something the bearer possesses because it came into being, either through evolution (in the case of natural biological entities) or through intentional design (in the case of artifacts), in order to realize processes of a certain sort"
- **Context**: Definition distinguishing function from general disposition.

### Pattern: is_a Relation Between Types

- **Source**: 07-Classifying_Processes_Barry_Smith (Chunk 1:104-106)
- **Description**: The is_a relation joins nodes representing an assertion that all instances of the first type are also instances of the second type.
- **Quote**: "The nodes in the graph are joined by edges representing relations between the types, of which the most important (illustrated in Figure 1) are is_a (abbreviating 'is a subtype of') and part_of"
- **Context**: Introduction to ontology graph structure.

### Pattern: Type-Level part_of Relation

- **Source**: 07-Classifying_Processes_Barry_Smith (Chunk 1:135-147)
- **Description**: When two nodes are joined by part_of, this represents an assertion that every instance of the first type is a part of some instance of the second type.
- **Quote**: "When two nodes are joined together by the part_of relation, as in viral receptor activity part_of response to virus then this represents an assertion to the effect that every instance of the first type is a part of some instance of the second type"
- **Context**: Explanation of part_of relation semantics.

### Pattern: Continuant vs Occurrent Categorical Distinction

- **Source**: 07-Classifying_Processes_Barry_Smith (Chunk 1:430-440)
- **Description**: The distinction between continuants and occurrents is categorical - all parts of continuants are continuants, all parts of occurrents are occurrents. This flows from two different ways of existing in time.
- **Quote**: "The distinction between continuants and occurrents is for BFO categorical. All the parts of continuants are continuants, and any whole to which a continuant belongs is also a continuant. Similarly, all the parts of occurrents are occurrents... This division flows from two essentially different ways of existing in time"
- **Context**: BFO's bicategorial approach to ontology.

### Pattern: Participation Connects Continuants and Occurrents

- **Source**: 07-Classifying_Processes_Barry_Smith (Chunk 1:437-440)
- **Description**: Connections between continuants and occurrents are secured not through parthood relations but through relations of participation.
- **Quote**: "Certainly there are manifold connections between continuants and occurrents, but they are secured in BFO not through parthood relations, but rather through relations of participation"
- **Context**: How the two BFO categories interact.

### Pattern: Temporal Parthood for Occurrents

- **Source**: 07-Classifying_Processes_Barry_Smith (Chunk 1:574-593)
- **Description**: Temporal parthood is defined for occurrents where a is a temporal part of b if a is the exact restriction of b to a temporal region that is a proper part of the temporal region spanned by b.
- **Quote**: "a temporal_part_of b =Def. a occurrent_part_of b & for some temporal region r (a spans r & for all occurrents c, r' if (c spans r' & r' occurrent_part_of r) then (c occurrent_part_of a iff c occurrent_part_of b)))"
- **Context**: Formal definition of temporal parthood.

### Pattern: Process Specific Dependence on Participants

- **Source**: 07-Classifying_Processes_Barry_Smith (Chunk 1:848-852)
- **Description**: Processes stand to independent continuants (their participants) in a relation analogous to how qualities stand to their bearers - both are cases of specific dependence.
- **Quote**: "Processes themselves stand to the independent continuants which are their participants in a relation that is analogous to that in which qualities stand to the independent continuants which are their bearers. In both cases we have to deal with the relation of what BFO calls specific dependence"
- **Context**: Discussion of process dependence relations.
