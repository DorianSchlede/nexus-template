---
batch_id: 1
field: entity_types
papers_read: [02-Knowledge_Graphs, 04-PROV-O_to_BFO_Semantic_Mapping, 05-DOLCE_Descriptive_Ontology, 06-BFO_Function_Role_Disposition, 07-Classifying_Processes_Barry_Smith]
chunks_read: 10
patterns_found: 47
extracted_at: "2025-12-28T12:30:00Z"
---

# Batch Extraction: entity_types (Batch 1)

## Patterns Extracted

### Pattern: Knowledge Graph Core Types (Data Graph vs Knowledge Graph)

- **Source**: 02-Knowledge_Graphs (Chunk 2:78-86)
- **Description**: Distinguishes between data graphs (collections of data as nodes and edges) and knowledge graphs (data graphs enhanced with schema, identity, context, ontologies and/or rules). Knowledge graphs layer additional representations on top of basic data graphs.
- **Quote**: "We refer to a data graph as a collection of data represented as nodes and edges using one of the models discussed in Section 2. We refer to a knowledge graph as a data graph potentially enhanced with representations of schema, identity, context, ontologies and/or rules."
- **Context**: Section 3 discussing schema, identity, and context enhancements to data graphs.

---

### Pattern: Semantic Schema Classes and Properties

- **Source**: 02-Knowledge_Graphs (Chunk 2:101-127)
- **Description**: Semantic schema defines classes (groupings of nodes) and properties (edge labels). Classes form hierarchies through subclass relations, and properties form hierarchies through sub-property relations. Domain and range constraints specify which classes can be connected by which properties.
- **Quote**: "We may thus decide to define classes to denote these groupings, such as Event, City, etc. ... Aside from classes, we may also wish to define the semantics of edge labels, aka properties."
- **Context**: Section 3.1.1 on semantic schema explaining how to define meaning of vocabulary terms used in graphs.

---

### Pattern: Class Hierarchy with Subclass Relations

- **Source**: 02-Knowledge_Graphs (Chunk 2:113-118)
- **Description**: Classes can be organized in hierarchies where children are subclasses of parents. If a node is of type Food Festival, it can be inferred to also be of type Festival and Event.
- **Quote**: "In Figure 11, we present a class hierarchy for events where children are defined to be subclasses of their parents such that if we find an edge [EID15] type Food Festival in our graph, we may also infer that [EID15] type Festival and [EID15] type Event."
- **Context**: Example of class hierarchy for Event showing taxonomic structure.

---

### Pattern: RDFS Schema Features (Subclass, Subproperty, Domain, Range)

- **Source**: 02-Knowledge_Graphs (Chunk 2:155-166)
- **Description**: RDFS standard defines four core schema features: Subclass (x type c implies x type d), Subproperty (x p y implies x q y), Domain (x p y implies x type c), and Range (x p y implies y type c).
- **Quote**: "Subclass c subc. of d: x type c implies [x] type d ... Subproperty p subp. of q: x p y implies [x] q y ... Domain p domain c: x p y implies [x] type c ... Range p range c: x p y implies [y] type c"
- **Context**: Table 2 providing formal definitions for semantic schema features.

---

### Pattern: Shapes for Graph Validation (Shape, Target, Constraint)

- **Source**: 02-Knowledge_Graphs (Chunk 2:250-260)
- **Description**: Shapes define validation constraints on graph data. A shape targets a set of nodes and specifies constraints on those nodes. A shapes graph is formed from a set of interrelated shapes.
- **Quote**: "A shape targets a set of nodes in a data graph and specifies constraints on those nodes. The shape's target can be defined in many ways, such as targetting all instances of a class, the domain or range of a property, the result of a query..."
- **Context**: Section 3.1.2 on validating schema using shapes for ensuring data completeness.

---

### Pattern: Open vs Closed Shapes

- **Source**: 02-Knowledge_Graphs (Chunk 2:309-312)
- **Description**: An open shape allows nodes to have additional properties not specified by the shape, while a closed shape does not permit unspecified properties.
- **Quote**: "An open shape allows the node to have additional properties not specified by the shape, while a closed shape does not."
- **Context**: Discussion of shape definition flexibility in data modeling.

---

### Pattern: Quotient Graph Entity Types

- **Source**: 02-Knowledge_Graphs (Chunk 2:443-450)
- **Description**: Quotient graphs partition nodes based on equivalence relations into types such as event, name, venue, class, date-time, city. These partitions describe the structure of the graph.
- **Quote**: "In order to describe the structure of the graph, we could consider six partitions of nodes: event, name, venue, class, date-time, city."
- **Context**: Section 3.1.3 on emergent schema using quotient graphs for graph summarization.

---

### Pattern: Knowledge Graph Identity Types (Persistent Identifiers, IRIs)

- **Source**: 02-Knowledge_Graphs (Chunk 2:561-595)
- **Description**: Persistent Identifiers (PIDs) uniquely identify entities. RDF uses Internationalized Resource Identifiers (IRIs) for non-information resources. URLs identify information resources (webpages) while IRIs identify real-world entities.
- **Quote**: "RDF 1.1 proposes to use Internationalised Resource Identifiers (IRIs) to identify non-information resources such as cities or events."
- **Context**: Section 3.2.1 on persistent identifiers and distinguishing entities from resources describing them.

---

### Pattern: Datatype Nodes

- **Source**: 02-Knowledge_Graphs (Chunk 2:713-731)
- **Description**: Datatype values are nodes whose syntactic form conveys meaning (dates, numbers, etc.). RDF uses XML Schema Datatypes (XSD) where a datatype node is a pair of lexical string and datatype IRI (e.g., xsd:dateTime, xsd:string, xsd:integer).
- **Quote**: "RDF utilises XML Schema Datatypes (XSD), amongst others, where a datatype node is given as a pair (l,d) where l is a lexical string, such as '2020-03-29T20:00:00', and d is an IRI denoting the datatype, such as xsd:dateTime."
- **Context**: Section 3.2.3 on datatype handling in RDF graphs.

---

### Pattern: Existential Nodes (Blank Nodes)

- **Source**: 02-Knowledge_Graphs (Chunk 2:779-806)
- **Description**: Existential nodes represent entities known to exist but not identifiable. In RDF these are called blank nodes. They denote that a node exists with particular relationships without identifying it.
- **Quote**: "These edges denote that there exists a common venue for [chile:EID42] and [chile:EID42] without identifying it. Existential nodes are supported in RDF as blank nodes..."
- **Context**: Section 3.2.5 on modeling incomplete information using existential nodes.

---

### Pattern: Context Types (Temporal, Geographic, Provenance)

- **Source**: 02-Knowledge_Graphs (Chunk 2:816-827)
- **Description**: Facts in data graphs can be considered true with respect to different types of context: temporal (when something existed or occurred), geographic (where it applies), and provenance (source of the data).
- **Quote**: "With respect to temporal context, [Santiago] has only existed as a city since 1541... With respect to geographic context, the graph describes events in Chile. With respect to provenance, data relating to [EID15] were taken from..."
- **Context**: Section 3.3 on context as the scope of truth for graph data.

---

### Pattern: Reification Representations (RDF Reification, N-ary Relations, Singleton Properties)

- **Source**: 02-Knowledge_Graphs (Chunk 2:880-905)
- **Description**: Three forms of reification for making statements about statements: RDF reification (new node connected to source, target, and predicate), n-ary relations (source connected to edge node), and singleton properties (edge label connected to original label).
- **Quote**: "RDF reification defines a new node [e] to represent the edge and connects it to the source node (via subject), target node (via object), and edge label (via predicate) of the edge."
- **Context**: Section 3.3.2 on reification for defining context on edges.

---

### Pattern: Description Logics Core Elements (Individuals, Classes/Concepts, Properties/Roles)

- **Source**: 02-Knowledge_Graphs (Chunk 4:127-162)
- **Description**: Description Logics are based on three types of elements: individuals (e.g., Santiago), classes/concepts (e.g., City), and properties/roles (e.g., flight). DLs allow making claims (axioms) about these elements including assertional axioms (A-Box), class axioms (T-Box), and property axioms (R-Box).
- **Quote**: "Description Logics are based on three types of elements: individuals, such as Santiago; classes (aka concepts) such as City; and properties (aka roles) such as flight."
- **Context**: Section 4.3.2 on Description Logics as formalization framework for knowledge graphs.

---

### Pattern: DL Axiom Types (A-Box, T-Box, R-Box)

- **Source**: 02-Knowledge_Graphs (Chunk 4:151-162)
- **Description**: Assertional axioms (A-Box) are unary class relations or binary property relations on individuals. Terminology Box (T-Box) contains class axioms. Role Box (R-Box) contains property axioms.
- **Quote**: "Assertional axioms can be either unary class relations on individuals, such as City(Santiago), or binary property relations on individuals, such as flight(Santiago,Arica). Such axioms form the Assertional Box (A-Box). DLs further introduce logical symbols to allow for defining class axioms (forming the Terminology Box, or T-Box for short), and property axioms (forming the Role Box, R-Box)..."
- **Context**: Description of DL axiom organization into three boxes.

---

### Pattern: PROV-O Core Entity Types (Entity, Activity, Agent)

- **Source**: 04-PROV-O_to_BFO_Semantic_Mapping (Chunk 1:75-77)
- **Description**: PROV-O defines three core types for provenance: Entity (physical, digital, conceptual things), Activity (occurrences over time), and Agent (entities with responsibility for activities).
- **Quote**: "The Provenance Ontology (PROV-O) is a W3C recommended ontology used to structure data about provenance: 'information about entities, activities, and people involved in producing a piece of data or thing...'"
- **Context**: Abstract section introducing PROV-O as W3C standard for provenance.

---

### Pattern: BFO Top-Level Ontology Structure (Continuant, Occurrent, Spatial Region, Temporal Region)

- **Source**: 04-PROV-O_to_BFO_Semantic_Mapping (Chunk 1:78-79)
- **Description**: Basic Formal Ontology (BFO) is an ISO standard top-level ontology providing foundational classes for structuring domain ontologies and enabling semantic interoperability.
- **Quote**: "Basic Formal Ontology (BFO) is a top-level ontology ISO standard used to provide foundational classes to structure different domain ontologies and to allow for semantic interoperability between them."
- **Context**: Introduction describing BFO as foundational ontology framework.

---

### Pattern: PROV Entity Mapped to BFO Continuant

- **Source**: 04-PROV-O_to_BFO_Semantic_Mapping (Chunk 1:633-645)
- **Description**: PROV Entity is defined as "a physical, digital, conceptual, or other kind of thing with some fixed aspects" and is mapped as a subclass of BFO continuant (excluding spatial regions). PROV Entity can persist through time with all spatial parts.
- **Quote**: "PROV Entity is defined as 'a physical, digital, conceptual, or other kind of thing with some fixed aspects; entities may be real or imaginary'. Our interpretation of this is that a PROV Entity can exist entirely at different times and persist its identity over time with all spatial parts and no temporal parts. We therefore map PROV Entity as a subclass of BFO continuant..."
- **Context**: Results section explaining PROV Entity to BFO continuant mapping.

---

### Pattern: PROV Agent as Material Entity with Role

- **Source**: 04-PROV-O_to_BFO_Semantic_Mapping (Chunk 1:654-668)
- **Description**: PROV Agent is mapped as a subclass of BFO material entities that participate in some PROV Activity and bear some BFO role realized in a PROV Activity. Agents always have matter and bear responsibility for activities.
- **Quote**: "PROV Agent is mapped as a subclass of BFO material entities that both participates in some PROV Activity and bears some BFO role that is realized in a PROV Activity... The reason for this mapping is that a PROV Agent always has some matter as a part that persists in time."
- **Context**: Detailed mapping of PROV Agent showing complex relationship to BFO.

---

### Pattern: PROV Activity Equivalent to BFO Process

- **Source**: 04-PROV-O_to_BFO_Semantic_Mapping (Chunk 1:682-691)
- **Description**: PROV Activity is mapped as equivalent to BFO process. Activities include things that occur over time and act upon entities. BFO process was selected over BFO occurrent because Activities don't include temporal regions.
- **Quote**: "PROV Activity is mapped as equivalent to the class BFO process. The definition of PROV Activity includes 'something that occurs over a period of time and acts upon or with entities'. Similarly, a BFO occurrent - the parent class of BFO process - is defined as 'an entity that unfolds itself in time...'"
- **Context**: Equivalence mapping between PROV Activity and BFO process.

---

### Pattern: PROV Influence as Process or Process Boundary

- **Source**: 04-PROV-O_to_BFO_Semantic_Mapping (Chunk 1:911-920)
- **Description**: PROV Influence (superclass of 16 Qualified Influence classes) is mapped to disjoint union of BFO process and BFO process boundary. Subclasses like PROV Generation, Start, End are process boundaries (instantaneous events), while Communication and Derivation are processes.
- **Quote**: "PROV Influence, as the superclass of 16 Qualified Influence classes, is mapped to a subclass of the disjoint union of BFO process and BFO process boundary. Some of its subclasses such as PROV Generation, PROV Start, and PROV End are subsumed under PROV InstantaneousEvent, which is equivalently mapped to BFO process boundary..."
- **Context**: Complex mapping of PROV Influence to BFO occurrent types.

---

### Pattern: PROV InstantaneousEvent Equivalent to BFO Process Boundary

- **Source**: 04-PROV-O_to_BFO_Semantic_Mapping (Chunk 1:913-915)
- **Description**: PROV InstantaneousEvent is equivalently mapped to BFO process boundary since instances are indivisible boundaries of PROV Activities.
- **Quote**: "PROV InstantaneousEvent, which is equivalently mapped to BFO process boundary since instances of PROV InstantaneousEvent are indivisible boundaries of some PROV Activity that is equivalent to a BFO process."
- **Context**: Mapping of instantaneous events to process boundaries.

---

### Pattern: PROV Location Equivalent to BFO Site

- **Source**: 04-PROV-O_to_BFO_Semantic_Mapping (Chunk 1:808-816)
- **Description**: PROV Location is mapped as equivalent to BFO site, defined as a three-dimensional immaterial entity whose boundaries coincide with material entities or have locations determined by them.
- **Quote**: "PROV Location is mapped as equivalent to BFO site, which is defined as 'a three-dimensional immaterial entity whose boundaries either (partially or wholly) coincide with the boundaries of one or more material entities or have locations determined in relation to some material entity'."
- **Context**: Mapping of location concept between PROV-O and BFO.

---

### Pattern: PROV Role as Subclass of BFO Role

- **Source**: 04-PROV-O_to_BFO_Semantic_Mapping (Chunk 2:103-113)
- **Description**: PROV Role is mapped as subclass of BFO role because it is externally determined by context. BFO distinguishes roles (externally determined, can be gained/lost) from functions (internally determined by physical makeup).
- **Quote**: "PROV Role is defined as 'the function of an entity or agent with respect to an activity, in the context of a usage, generation, invalidation, association, start, and end'. Although the word 'function' is used here, BFO distinguishes between roles and functions... we map PROV Role directly as a subclass of BFO role on the grounds that a PROV Role is externally determined by the context in which the bearer plays the role."
- **Context**: Mapping of PROV Role with discussion of BFO function/role distinction.

---

### Pattern: PROV Plan as Information Content Entity

- **Source**: 04-PROV-O_to_BFO_Semantic_Mapping (Chunk 2:116-143)
- **Description**: PROV Plan is mapped to subclass of CCO Information Content Entity, which is a BFO generically dependent continuant. Plans are about some entity and may have multiple copies (generically dependent).
- **Quote**: "The case of PROV Plan is more complicated. It is mapped to a subclass of CCO Information Content Entity. According to CCO, an Information Content Entity is a BFO generically dependent continuant (GDC) that generically depends on some CCO Information Bearing Entity and stands in relation of aboutness to some entity."
- **Context**: Complex mapping of PROV Plan showing layered ontology integration.

---

### Pattern: DOLCE Fundamental Categories (Endurant, Perdurant, Quality, Abstract)

- **Source**: 05-DOLCE_Descriptive_Ontology (Chunk 1:121-122)
- **Description**: DOLCE's basic categories are endurant (continuant), perdurant (occurrent), quality, and abstract. This forms the top-level taxonomy of the ontology.
- **Quote**: "As depicted in the taxonomy in Figure 1, the basic categories of DOLCE are endurant (aka continuant), perdurant (occurrent), quality, and abstract."
- **Context**: Section 1 introducing DOLCE's structure and fundamental categories.

---

### Pattern: Endurant vs Perdurant Distinction

- **Source**: 05-DOLCE_Descriptive_Ontology (Chunk 1:128-137)
- **Description**: Endurants may acquire and lose properties through time but are wholly present at any time. Perdurants are fixed in time and can only be partially present (unfolding over time). Examples: table, person (endurants) vs tennis match, conference talk (perdurants).
- **Quote**: "While endurants may acquire and lose properties and parts through time, perdurants are fixed in time. Their fundamental difference concerns therefore their presence in time: endurants are wholly present (i.e., with all their parts) at any time in which they are present; differently, perdurants can be partially present, so that at any time in which they unfold only a part of them is present."
- **Context**: Core distinction between continuants and occurrents in DOLCE.

---

### Pattern: Independent vs Dependent Entity

- **Source**: 05-DOLCE_Descriptive_Ontology (Chunk 1:148-153)
- **Description**: This distinction crosses the entire DOLCE taxonomy. Features (edges, holes, bumps) are dependent endurants requiring a bearer. Physical objects are independent entities. Only abstract entities are truly independent across categories.
- **Quote**: "Features (e.g., edges, holes, bumps, etc.) are endurants whose existence depends on some physical object (the feature bearer), while physical objects are independent entities, i.e., their existence does not require other endurants to exist."
- **Context**: Explanation of dependence relations across ontology categories.

---

### Pattern: DOLCE Process Types (Stative, Eventive, Achievement, Accomplishment)

- **Source**: 05-DOLCE_Descriptive_Ontology (Chunk 1:156-163)
- **Description**: Perdurants are classified as stative or eventive based on cumulativity. Stative perdurants (states) are cumulative. Among stative, processes are cumulative but not homeomeric. Eventive occurrences (events) are not cumulative and are either achievements (atomic) or accomplishments.
- **Quote**: "In particular, a perdurant(-type) is stative or eventive according to whether it holds of the mereological sum of two of its instances, i.e. if it is cumulative or not. Common examples of stative perdurants are states... Among stative perdurants, processes are cumulative but not homeomeric... Finally, eventive occurrences (events) are not cumulative, and they are called achievements if they are atomic, otherwise they are accomplishments."
- **Context**: Detailed taxonomy of perdurants following linguistic and philosophical distinctions.

---

### Pattern: DOLCE Quality Types (Physical, Temporal, Abstract)

- **Source**: 05-DOLCE_Descriptive_Ontology (Chunk 1:166-182)
- **Description**: Qualities are particulars that inhere in endurants or perdurants and can be perceived/measured. Qualities are classified as physical, temporal, or abstract based on their bearers. Individual qualities have a position (quale) within a quality space.
- **Quote**: "Qualities are, roughly speaking, what can be perceived and measured; they are particulars inhering in endurants or perdurants... Depending on the entities in which they inhere (qualities are dependent entities indeed), DOLCE identifies qualities of different types, namely, physical, temporal or abstract qualities."
- **Context**: Section on properties, qualities, and quantities in DOLCE.

---

### Pattern: DOLCE Quale (Quality Position in Quality Space)

- **Source**: 05-DOLCE_Descriptive_Ontology (Chunk 1:177-181)
- **Description**: A quale is the position occupied by an individual quality within a quality space. Two qualities are distinct but have the same quale if they occupy the same position (e.g., two objects with same shade of red).
- **Quote**: "A quale is the position occupied by an individual quality within a quality space. In our example, if the rose and the book cover exhibit the same shade of red, their individual colors occupy the same position (quale) in the color space. Hence, the two qualities are distinct but they have the same quale (within the same color space)."
- **Context**: Explanation of how qualities are compared using qualia.

---

### Pattern: DOLCE Roles and Concepts

- **Source**: 05-DOLCE_Descriptive_Ontology (Chunk 1:184-200)
- **Description**: Roles are represented as social concepts connected to entities by classification relation. Roles are anti-rigid (dynamic properties, can be gained/lost) and founded (relational nature, depend on other roles and contexts).
- **Quote**: "Roles are represented as (social) concepts, which are connected to other entities (like endurants, perdurants, and abstracts) by the relation of classification. In particular, roles are concepts that are anti-rigid and founded, meaning that (i) they have dynamic properties and (ii) they have a relational nature, i.e. they depend on other roles and on contexts."
- **Context**: Section V on Function and Role in DOLCE.

---

### Pattern: DOLCE Parthood (Temporal vs Atemporal)

- **Source**: 05-DOLCE_Descriptive_Ontology (Chunk 1:206-214)
- **Description**: Parthood in DOLCE is time-indexed for endurants and a-temporal for perdurants and abstracts. Constitution is a temporalized relation holding between entities with different essential properties.
- **Quote**: "An important relation in DOLCE is parthood, which is time-indexed when connecting endurants and a-temporal when holding between perdurants or abstracts, i.e. between entities that do not change in time. Constitution is another temporalized relation in DOLCE, holding between either endurants or perdurants."
- **Context**: Section VI on Relations in DOLCE.

---

### Pattern: DOLCE Abstract Category

- **Source**: 05-DOLCE_Descriptive_Ontology (Chunk 1:216-219)
- **Description**: Abstracts are entities that have neither spatial nor temporal qualities and are not qualities themselves. Examples include quality regions, quality spaces, sets, and facts.
- **Quote**: "The last basic category of the ontology is that of abstracts. These are entities that have neither spatial nor temporal qualities and are not qualities themselves. We will not deal with them in the current paper, so it should suffice to give a few examples: quality regions (and therefore also quality spaces), sets, and facts."
- **Context**: Brief description of the abstract category in DOLCE.

---

### Pattern: DOLCE Physical Object and Matter

- **Source**: 05-DOLCE_Descriptive_Ontology (Chunk 1:480-498)
- **Description**: DOLCE distinguishes between quantities of matter (wood), objects constituted by matter (object made of wood), and artifacts (functional objects like tables). Constitution connects elements of different categories while composition connects elements of same category.
- **Quote**: "The ontology allows distinguishing between quantities of matter (e.g., the wood of which a table is made), the object constituted by the matter (that object made of that wood), and the artifact (the table, i.e., the functional object)."
- **Context**: Case 1 example on composition and constitution.

---

### Pattern: BFO Continuant Hierarchy

- **Source**: 06-BFO_Function_Role_Disposition (Chunk 1:66-88)
- **Description**: BFO continuants include: independent continuant (material entity: object, fiat object part, object aggregate; object boundary; site), dependent continuant (generically dependent continuant, specifically dependent continuant: quality, realizable entity: role, disposition, capability, function), and spatial region (zero/one/two/three-dimensional).
- **Quote**: "continuant > independent continuant > material entity > object, fiat object part, object aggregate... dependent continuant > generically dependent continuant, specifically dependent continuant > quality, realizable entity > role, disposition, capability, function..."
- **Context**: Figure 1 showing complete BFO 1.1 continuant taxonomy.

---

### Pattern: BFO Occurrent Hierarchy

- **Source**: 06-BFO_Function_Role_Disposition (Chunk 1:92-108)
- **Description**: BFO occurrents include: processual entity (process, process boundary, process aggregate, fiat process part, processual context-deprecated), spatiotemporal region (scattered/connected, instant/interval), and temporal region (scattered/connected, instant/interval).
- **Quote**: "occurrent > processual entity > process, process boundary, process aggregate, fiat process part, processual context... spatiotemporal region > scattered spatiotemporal region, connected spatiotemporal region > spatiotemporal instant, spatiotemporal interval... temporal region..."
- **Context**: Figure 2 showing complete BFO 1.1 occurrent taxonomy.

---

### Pattern: BFO Realizable Entity Definition

- **Source**: 06-BFO_Function_Role_Disposition (Chunk 1:241-243)
- **Description**: A realizable entity is a specifically dependent continuant that has an independent continuant as its bearer, whose instances can be realized (manifested, actualized, executed) in associated processes in which the bearer participates.
- **Quote**: "A realizable entity is defined as a specifically dependent continuant that has an independent continuant entity as its bearer, and whose instances can be realized (manifested, actualized, executed) in associated processes in which the bearer participates."
- **Context**: Section 4 defining realizable entities as basis for function, role, disposition.

---

### Pattern: BFO Role (Externally-Grounded Realizable Entity)

- **Source**: 06-BFO_Function_Role_Disposition (Chunk 1:268-286)
- **Description**: A role exists because the bearer is in special physical, social, or institutional circumstances. Roles are extrinsic/externally-grounded and optional - a bearer can lose a role without physical change. Examples: analyte role, drug role, infection role, boundary marker role.
- **Quote**: "A role is a realizable entity which exists because the bearer is in some special physical, social, or institutional set of circumstances in which the bearer does not have to be, and is not such that, if it ceases to exist, then the physical make-up of the bearer is thereby changed."
- **Context**: Section 5 defining role as externally-grounded realizable entity.

---

### Pattern: BFO Disposition (Internally-Grounded Realizable Entity)

- **Source**: 06-BFO_Function_Role_Disposition (Chunk 1:333-339)
- **Description**: A disposition is a realizable entity where if it ceases to exist, its bearer is physically changed. Dispositions are internally-grounded, reflecting the in-built or acquired physical make-up of the bearer. Dispositions exist along a strength continuum (weaker to sure-fire).
- **Quote**: "A disposition is a realizable entity which is such that, if it ceases to exist, then its bearer is physically changed, and whose realization occurs in virtue of the bearer's physical make-up when this bearer is in some special physical circumstances."
- **Context**: Section 6 defining disposition as internally-grounded realizable entity.

---

### Pattern: BFO Function (Designed/Evolved Disposition)

- **Source**: 06-BFO_Function_Role_Disposition (Chunk 1:385-401)
- **Description**: A function is a disposition that exists in virtue of the bearer's physical make-up, which came into being through evolution (biological) or intentional design (artifacts). Functions are realized in processes called functionings.
- **Quote**: "A function is a disposition that exists in virtue of the bearer's physical make-up, and this physical make-up is something the bearer possesses because it came into being, either through evolution (in the case of natural biological entities) or through intentional design (in the case of artifacts), in order to realize processes of a certain sort."
- **Context**: Section 7 defining function as special type of disposition.

---

### Pattern: BFO Artifactual vs Biological Function

- **Source**: 06-BFO_Function_Role_Disposition (Chunk 1:433-466)
- **Description**: Artifactual function: bearer designed and made intentionally to function in a certain way. Biological function: bearer is part of an organism that evolved to contribute to organism's life plan. Biological functions are attributed to parts of organisms, not whole organisms.
- **Quote**: "An artifactual function is a function whose bearer's physical make-up has been designed and made intentionally... A biological function is a function whose bearer is part of an organism, and exists and has the physical make-up it has because it has evolved that way and contributes to the organism's realization of a life plan appropriate to an organism of its type."
- **Context**: Sections 8.1 and 8.2 distinguishing two types of functions.

---

### Pattern: BFO Continuant vs Occurrent Distinction

- **Source**: 07-Classifying_Processes_Barry_Smith (Chunk 1:296-311)
- **Description**: Four-dimensionalists see reality as four-dimensional processes/events/occurrents. Three-dimensionalists see reality as three-dimensional things. BFO adopts a bicategorial approach combining both perspectives within a single framework.
- **Quote**: "Four-dimensionalists (in simple terms) see reality as consisting exclusively of four-dimensional entities (variously referred to as processes, events, occurrents, perdurants, spacetime-worms, and so forth)... BFO, in contrast, is founded on a bicategorial approach which seeks to combine elements of both the three-dimensionalist and four-dimensionalist perspectives."
- **Context**: Section 2.1 on BFO's treatment of the continuant/occurrent dichotomy.

---

### Pattern: Zemach's Things vs Events

- **Source**: 07-Classifying_Processes_Barry_Smith (Chunk 1:349-381)
- **Description**: Continuants (things) can be sliced only along spatial dimension. Occurrents (events) can be sliced along any spatial and temporal dimension. Things are wholly present at any time; events exist as the whole content of spatiotemporal regions.
- **Quote**: "The former, for Zemach, are defined by the fact that they can be sliced (in actuality, or in imagination) to yield parts only along the spatial dimension... The latter, in contrast, can be sliced to yield parts along any spatial and temporal dimensions."
- **Context**: Section 2.2 discussing Zemach's 'Four Ontologies' influence on BFO.

---

### Pattern: Aristotle's Ontological Square (Types/Instances x Independent/Dependent)

- **Source**: 07-Classifying_Processes_Barry_Smith (Chunk 1:446-452)
- **Description**: BFO recapitulates Aristotle's ontological square with four categories: Independent Continuant Types (planet, organism, cell), Independent Continuant Instances, Dependent Continuant Types (temperature, sickle shape), Dependent Continuant Instances.
- **Quote**: "In allowing not only things but also entities that are dependent on things as continuants, BFO draws on Aristotle's ideas concerning the division of substances and accidents, which reappears in BFO as the division between independent and dependent continuants. Given that BFO accepts also the distinction between universals and particulars, it thus recapitulates Aristotle's ontological square..."
- **Context**: Section 2.3 showing how BFO relates to classical ontological categories.

---

### Pattern: Quality Universals (Determinable vs Determinate)

- **Source**: 07-Classifying_Processes_Barry_Smith (Chunk 1:458-510)
- **Description**: Qualities instantiate determinable universals (temperature, length, mass) and determinate universals (37.0C temperature, 1.6 meter length). Determinable universals are rigid (exemplified at all times of bearer's existence). Determinate universals change over time.
- **Quote**: "Qualities instantiate quality universals, which are divided into determinable (such as temperature, length and mass) and determinate (such as 37.0C temperature, 1.6 meter length, and 4 kg mass)... Determinable quality universals are rigid in the sense that, if a determinable quality universal is exemplified by a particular bearer at any time during which this bearer exists, then it is exemplified at every such time."
- **Context**: Section 2.4 on determinable and determinate quality universals.

---

### Pattern: BFO Process Types (Process, Process Boundary, Spatiotemporal Region, Temporal Region)

- **Source**: 07-Classifying_Processes_Barry_Smith (Chunk 1:547-563)
- **Description**: BFO occurrents include processes, process boundaries (beginnings/endings), spatiotemporal regions, temporal intervals and instants. Processes occupy spatiotemporal regions and span temporal intervals. Process boundaries span temporal instants.
- **Quote**: "BFO's treatment of occurrents, which include processes, process boundaries (for example beginnings and endings), spatiotemporal regions, and temporal intervals and temporal instants. BFO uses 'occupies' to refer to the relation that holds between an occurrent and the spatiotemporal region which it exactly fills."
- **Context**: Section 3 on processes in BFO.

---

### Pattern: Process Profile Types (Quality, Rate, Cyclical)

- **Source**: 07-Classifying_Processes_Barry_Smith (Chunk 2:149-256)
- **Description**: Process profiles are parts of processes serving as targets of selective abstraction. Types include: Quality process profiles (sequence of determinate qualities over time), Rate process profiles (ratios of magnitudes to elapsed time like speed, acceleration), and Cyclical process profiles (cycles per unit time).
- **Quote**: "The simplest example of a process profile is that part of a process which serves as the target of selective abstraction focused on a sequence of instances of determinate qualities such as temperature or height... Rate process profiles... are the targets of selective abstraction focused not on determinate quality magnitudes plotted over successive instants of time, but rather on certain ratios between these magnitudes and associated intervals of elapsed time..."
- **Context**: Section 4 on process profiles for classifying processes.

