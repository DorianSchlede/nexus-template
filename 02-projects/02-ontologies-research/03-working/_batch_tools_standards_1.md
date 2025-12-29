# Batch Extraction: tools_standards (Batch 1 of 2)

**Field:** tools_standards
**Description:** Technical implementations (OWL, RDF, BPMN, CMMN, DMN, OCEL 2.0)

---

## Paper: 02-Knowledge_Graphs (Chunk 1)

### Pattern: RDF as Standardized Data Model for Directed Edge-Labelled Graphs

**Source:** 02-Knowledge_Graphs (Chunk 1:435-446)

**Description:** The Resource Description Framework (RDF) is a W3C-recommended standardized data model for representing directed edge-labelled graphs. RDF defines specific node types including Internationalized Resource Identifiers (IRIs) for global identification of entities on the Web, literals for representing strings and datatype values (integers, dates, etc.), and blank nodes for anonymous nodes without identifiers.

**Quote:** "A standardised data model based on directed edge-labelled graphs is the Resource Description Framework (RDF) [111], which has been recommended by the W3C. The RDF model defines different types of nodes, including Internationalized Resource Identifiers (IRIs) [134] which allow for global identification of entities on the Web; literals, which allow for representing strings (with or without language tags) and other datatype values (integers, dates, etc.); and blank nodes, which are anonymous nodes that are not assigned an identifier"

**Context:** Discussion of graph data models used for knowledge graphs, comparing RDF with property graphs and other representations.

---

### Pattern: Property Graph Model and Neo4j Implementation

**Source:** 02-Knowledge_Graphs (Chunk 1:548-572)

**Description:** Property graphs allow property-value pairs and labels to be associated with both nodes and edges, providing additional modeling flexibility. This model is most prominently used in graph databases like Neo4j. Property graphs can be translated to/from directed edge-labelled graphs without loss of information.

**Quote:** "The property graph model was thus proposed to offer additional flexibility when modelling data as a graph [16, 354]. A property graph allows a set of property-value pairs and a label to be associated with both nodes and edges... Property graphs are most prominently used in popular graph databases, such as Neo4j [16, 354]. In choosing between graph models, it is important to note that property graphs can be translated to/from directed edge-labelled graphs without loss of information [18, 235]"

**Context:** Explaining how property graphs provide more flexibility than directed edge-labelled graphs for modeling complex relations with attributes.

---

### Pattern: SPARQL Query Language for RDF Graphs

**Source:** 02-Knowledge_Graphs (Chunk 1:663-708)

**Description:** SPARQL is the query language for RDF graphs, supporting graph patterns, relational operators, and path expressions. It adopts homomorphism-based semantics for evaluating graph patterns, meaning multiple variables can be mapped to the same term.

**Quote:** "A number of practical languages have been proposed for querying graphs [16], including the SPARQL query language for RDF graphs [217]; and Cypher [165], Gremlin [445], and G-CORE [15] for querying property graphs... different practical languages adopt different semantics for evaluating graph patterns where, for example, SPARQL adopts a homomorphism-based semantics, while Cypher adopts an isomorphism-based semantics on edges."

**Context:** Comparison of query languages for different graph data models.

---

### Pattern: Graph Storage Techniques for Directed Edge-Labelled Graphs

**Source:** 02-Knowledge_Graphs (Chunk 1:642-658)

**Description:** Multiple storage techniques exist for directed edge-labelled graphs in relational databases: triple tables (single relation of arity three), vertical partitioning (binary relation for each property), and property tables (n-ary relations for entities of a given type). Custom storage techniques provide efficient access for finding nodes, edges and their adjacent elements.

**Quote:** "Directed-edge labelled graphs can be stored in relational databases either as a single relation of arity three (triple table), as a binary relation for each property (vertical partitioning), or as n-ary relations for entities of a given type (property tables) [560]. Custom storage techniques have also been developed for a variety of graph models, providing efficient access for finding nodes, edges and their adjacent elements [17, 354, 560]."

**Context:** Technical discussion of graph storage implementation options.

---

### Pattern: Linked Data and Named Graphs for Web Data Provenance

**Source:** 02-Knowledge_Graphs (Chunk 1:612-619)

**Description:** Graph datasets support managing Linked Data composed of interlinked documents of RDF graphs spanning the Web. Named graphs enable tracking the source of data, which is critical when dealing with Web data.

**Quote:** "A prominent use-case for graph datasets is to manage and query Linked Data composed of interlinked documents of RDF graphs spanning the Web. When dealing with Web data, tracking the source of data becomes of key importance [58, 130, 583]."

**Context:** Discussion of graph datasets as a way to manage multiple graphs with provenance tracking.

---

## Paper: 04-PROV-O_to_BFO_Semantic_Mapping (Chunk 1)

### Pattern: OWL and RDF for Ontology Construction

**Source:** 04-PROV-O_to_BFO_Semantic_Mapping (Chunk 1:39-43)

**Description:** OWL (Web Ontology Language) and RDF (Resource Description Framework) are W3C standards used for constructing ontologies and achieving semantic interoperability. Data sets become more semantically interoperable when interpreted by the same OWL ontology into a knowledge graph.

**Quote:** "A popular way to construct ontologies, and the way relevant to this paper, is by leveraging the W3C standards Web Ontology Language (OWL) [3] and Resource Description Framework (RDF) [4]. Data sets become more semantically interoperable when interpreted by the same OWL ontology into a knowledge graph [5]."

**Context:** Introduction to using OWL and RDF for ontology mapping between PROV-O and BFO.

---

### Pattern: OWL equivalentClass and equivalentProperty for Mapping Relations

**Source:** 04-PROV-O_to_BFO_Semantic_Mapping (Chunk 1:146-156)

**Description:** OWL equivalentClass and equivalentProperty are used for equivalence relation mappings that give necessary and sufficient conditions for something to be an instance of both a BFO class/relation and a PROV-O class/relation. This provides a two-way bridge for interoperability between knowledge graphs.

**Quote:** "Equivalence relations represented by OWL equivalentClass and OWL equivalentProperty give necessary and sufficient conditions for something to be an instance of a certain BFO class or relation and a certain PROV-O class or relation at the same time. Everything that satisfies these conditions will be an instance of both, and nothing else will be an instance of either. An equivalence mapping provides a two-way bridge which allows for interoperability between two knowledge graphs."

**Context:** Explanation of the first criterion for mapping PROV-O to BFO using equivalence relations.

---

### Pattern: RDFS subClassOf and subPropertyOf for Subsumption Relations

**Source:** 04-PROV-O_to_BFO_Semantic_Mapping (Chunk 1:158-164)

**Description:** RDFS subClassOf and subPropertyOf represent subsumption relations that provide sufficient conditions for an instance of one class or relation to be an instance of another. This creates a one-way bridge from one term to another and allows for non-injective alignments.

**Quote:** "Subsumption relations represented by RDFS subClassOf or RDFS subPropertyOf give sufficient conditions for an instance of one class or relation to be an instance of another class or relation [20]. If a certain PROV-O class is a subclass of a certain BFO class, then all the instances of the PROV-O class are also instances of the corresponding BFO class. The result of a subsumption relation mapping is then a one-way bridge from one term to another."

**Context:** Explanation of subsumption relations for ontology mapping.

---

### Pattern: OWL unionOf, intersectionOf, and Property Restrictions for Complex Mappings

**Source:** 04-PROV-O_to_BFO_Semantic_Mapping (Chunk 1:167-183)

**Description:** Complex equivalence and subsumption relations can be represented using OWL unionOf, OWL intersectionOf, and OWL property restrictions. SWRL rules are useful for restricting domain or range of OWL object properties and are implemented by semantic reasoners such as HermiT. SPARQL queries can encode mappings equivalent to some SWRL rules. OWL property chain axioms can axiomatize complex subsumption relations between object properties.

**Quote:** "Complex equivalence and subsumption relations between combinations of terms may be represented with OWL unionOf, OWL intersectionOf, and OWL property restrictions. SWRL rules [21] are especially useful for restricting the domain or range of an OWL object property in order to use it in a valid mapping. An advantage of SWRL is that it is implemented by semantic reasoners such as HermiT [22, 23]. SPARQL [24] queries can also encode mappings that are equivalent to some SWRL rules. If a set of relations in one ontology should imply a relation in another ontology, OWL property chain axioms can be used to axiomatize this complex subsumption relation between object properties."

**Context:** Description of advanced OWL constructs for complex ontology mappings.

---

### Pattern: SKOS Vocabulary for Informal Mapping Relations

**Source:** 04-PROV-O_to_BFO_Semantic_Mapping (Chunk 1:186-195)

**Description:** SKOS (Simple Knowledge Organization System) vocabulary represents informal relations between terms that may be intuitively similar. SKOS is commonly used with SSSOM (Simple Standard for Sharing Ontology Mappings) vocabulary. SKOS predicates have weaker inferential semantics than RDFS/OWL subsumption and equivalence.

**Quote:** "Mapping predicates from the SKOS vocabulary [25] represent informal relations between terms which may be interpreted by users to be intuitively similar. SKOS is commonly used for ontology mappings, especially in conjunction with annotations from the Simple Standard for Sharing Ontology Mappings (SSSOM) vocabulary [7]. However, SKOS predicates have weaker inferential semantics than those of subsumption and equivalence in RDFS and OWL."

**Context:** Discussion of SKOS as an alternative to formal OWL mappings.

---

### Pattern: OWL 2 DL and Description Logic Profiles

**Source:** 04-PROV-O_to_BFO_Semantic_Mapping (Chunk 1:201-207)

**Description:** BFO, RO, and CCO conform to OWL 2 DL profile corresponding to description logic SROIQ. PROV-O and its extensions conform to OWL 2 RL corresponding to description logic DLP. These profiles balance expressivity and computational efficiency for automated reasoning tasks.

**Quote:** "The OWL implementations of BFO and PROV-O are based on first-order logic fragments which balance expressivity and computational efficiency for automated reasoning tasks such as classification or checking satisfiability. BFO, RO, and CCO conform to the OWL 2 DL profile, corresponding to the description logic SROIQ [3]. PROV-O and its extensions conform to OWL 2 RL, corresponding to the description logic DLP, with the exception of some axioms that conform to OWL 2 DL [8]."

**Context:** Technical discussion of OWL profiles used by different ontologies.

---

### Pattern: SPARQL Queries for Alignment Verification

**Source:** 04-PROV-O_to_BFO_Semantic_Mapping (Chunk 1:398-421)

**Description:** SPARQL queries are used to automatically verify the totality of ontology alignments. The query finds any PROV-O class or object property term not transitively related via equivalence or subsumption to some BFO/RO/CCO term. SPARQL property path expressions exclude transitively entailed mappings. HermiT reasoner materializes entailed mappings before running the query.

**Quote:** "A SPARQL query was developed for automatically verifying the Totality of the combined alignments as described in Criterion 4. The query finds any PROV-O class or object property term such that it, or its inverse, is not transitively related via equivalence or subsumption, or related via a property chain axiom or SWRL rule, to some BFO, RO, or CCO class or object property term. This query was added to the continuous development pipeline, and generated a list of unmapped terms when triggered."

**Context:** Technical implementation of automated alignment verification.

---

### Pattern: RDF Turtle Serialization for Alignment Files

**Source:** 04-PROV-O_to_BFO_Semantic_Mapping (Chunk 1:424-436)

**Description:** RDF Turtle (TTL - Terse Triple Language) is used to serialize example instances and alignment files. The HermiT reasoner tests consistency of example instances. 312 instances were encoded including named individuals and anonymous individuals represented with blank nodes.

**Quote:** "To test the Coherence and Consistency of each alignment, as in Criterion 2, every canonical example instance from the W3C documentation for PROV-O and its extensions was copied into RDF files serialized in the Terse Triple Language (TTL or 'RDF Turtle') [35] and imported into the editor's module. 312 instances were counted, including either named or anonymous individuals represented with blank nodes. The HermiT reasoner tested the consistency of these example instances with PROV, BFO, RO, CCO, and the alignments between them."

**Context:** Technical implementation details for testing alignment consistency.

---

### Pattern: ROBOT Command-Line Tool and GNU Make for Ontology Engineering

**Source:** 04-PROV-O_to_BFO_Semantic_Mapping (Chunk 1:461-474)

**Description:** ROBOT is a command-line tool used for running SPARQL queries and the HermiT reasoner. GNU Make composes ROBOT commands into Makefile tasks. GitHub Actions runs these Makefile tasks as part of a continuous development pipeline for automatic testing of alignment changes.

**Quote:** "Automated tests for the techniques described above were implemented as part of an ontology engineering pipeline using ROBOT and GNU Make (https://www.gnu.org/software/make/). ROBOT commands used for running SPARQL queries and the HermiT reasoner were composed into Makefile tasks. These Makefile tasks are run within a continuous development pipeline using GitHub Actions. The result is that changes to the alignments can be automatically, rigorously tested when committed to the Git repository hosted in GitHub."

**Context:** Description of CI/CD pipeline for ontology engineering.

---

### Pattern: OWL annotatedSource, annotatedProperty, annotatedTarget for Reified Axioms

**Source:** 04-PROV-O_to_BFO_Semantic_Mapping (Chunk 1:511-528)

**Description:** OWL annotatedSource, annotatedProperty, and annotatedTarget properties serialize reified OWL axioms in RDF Turtle. These correspond to subject, predicate, and object of a mapping. SSSOM annotation properties (subject label, object label) provide human-friendly references for terms with opaque IRIs.

**Quote:** "Provenance metadata for the alignments are encoded as annotations on each OWL axiom that represents a mapping relation. In RDF Turtle, the mapping relations themselves are serialized with OWL annotatedSource, OWL annotatedProperty, and OWL annotatedTarget properties of reified OWL axioms [39], which correspond to the subject, predicate, and object of a mapping, respectively."

**Context:** Technical details of how mapping axioms are serialized with provenance metadata.

---

### Pattern: SWRL Rules for Object Property Mapping with Domain/Range Restrictions

**Source:** 04-PROV-O_to_BFO_Semantic_Mapping (Chunk 1:837-880)

**Description:** SWRL rules are used to map object properties when the source and target properties have different domains or ranges. The rules restrict the domain and range of particular instances to enable valid mappings. A semantic reasoner can then automatically infer which instances are related by both properties.

**Quote:** "PROV atLocation is mapped using SWRL rules... In order to map PROV atLocation to both of these object properties, SWRL rules were used to restrict the domain and range of particular instances of them. Here are the SWRL rule mappings between PROV atLocation and BFO occurs in (obo:BFO_0000066):
'If a PROV Activity is at some location, then it occurs in that location'
prov:atLocation(?x,?y) ^ prov:Activity(?x) -> obo:BFO_0000066(?x,?y)"

**Context:** Concrete example of using SWRL rules for complex property mappings.

---

### Pattern: OWL Qualification Pattern for N-ary Information

**Source:** 04-PROV-O_to_BFO_Semantic_Mapping (Chunk 1:892-906)

**Description:** The Qualification Pattern is a form of reification recommended for representing n-ary information in description logic. It reifies binary relations as instances of a class (e.g., PROV Influence) so additional properties can be added. Alternative options include description/situation strategy, non-rigid classification, and temporally qualified continuants.

**Quote:** "The Qualification Pattern employed in PROV-O is a form of reification, which is generally recommended as a standard methodology for alleviating the representational limits of description logic [45] and representing n-ary information among the OWL community [46]. To associate further information to a binary unqualified relation of 'influence' between entities, activities or agents, the Qualification Pattern reifies this relation as an instance of the class PROV Influence."

**Context:** Discussion of reification patterns for complex relationships in OWL.

---

## Paper: 09-OCEL_20_Specification (Chunk 1)

### Pattern: OCEL 2.0 Standard with XML, JSON, and Relational Formats

**Source:** 09-OCEL_20_Specification (Chunk 1:17-28)

**Description:** OCEL 2.0 provides three exchange formats for object-centric event logs: relational database (SQLite), XML, and JSON. Validation schemes are provided for each format with official URLs for schemas.

**Quote:** "Version: 2.0
Date: October 16, 2023
Standard Document URL: https://www.ocel-standard.org/2.0/ocel20_specification.pdf
Validation Schemes:
- XML: https://www.ocel-standard.org/2.0/ocel20-schema-xml.xsd
- JSON: https://www.ocel-standard.org/2.0/ocel20-schema-json.json
- Relational: https://www.ocel-standard.org/2.0/ocel20-schema-relational.pdf"

**Context:** Introduction to the OCEL 2.0 standard specification document.

---

### Pattern: OCEL 2.0 Metamodel with Typed Events and Objects

**Source:** 09-OCEL_20_Specification (Chunk 1:149-175)

**Description:** OCEL 2.0 defines events as discrete, atomic actions with timestamps and attributes. Events are typed into event types (activities). Objects represent entities involved in events with changeable attribute values. Objects are also typed into object types.

**Quote:** "Events: Object-centric process mining works on discrete events. They represent the various actions or activities that occur within a system or process... Events are atomic (i.e., do not take time), have a timestamp, and may have additional attributes. Events are typed.
Event Types: Events are categorized into different types based on their nature or function... Each event is of exactly one type.
Objects: In object-centric process mining, objects represent the entities that are involved in events... Objects have attributes with values, e.g., prices. These values may change over time.
Object Types: Each object is of one type."

**Context:** Core concepts definition for the OCEL 2.0 metamodel.

---

### Pattern: Event-to-Object (E2O) and Object-to-Object (O2O) Relationships with Qualifiers

**Source:** 09-OCEL_20_Specification (Chunk 1:177-194)

**Description:** OCEL 2.0 supports Event-to-Object (E2O) relationships where events can relate to multiple objects. Relationships can be qualified to describe the role an object plays. Object-to-Object (O2O) relationships allow objects to relate outside event context, also with qualifiers (e.g., part-of, reports-to, belongs-to).

**Quote:** "Event-to-Object (E2O) Relationships: Events are associated with objects. This relationship describes that an object affects an event or that an event affects an object. In contrast to traditional event logs, events can be related to multiple objects. Furthermore, these relationships can be qualified differently, describing the role an object plays in the occurrence of this specific event.
Object-to-Object (O2O) Relationships: Objects can also be related to other objects outside the context of an event... In addition to the mere existence of a relation, this relationship can also be qualified (e.g., part-of, reports-to, or belongs-to)."

**Context:** Description of relationship types in OCEL 2.0.

---

### Pattern: IEEE XES Standard for Event Streams

**Source:** 09-OCEL_20_Specification (Chunk 1:237-250)

**Description:** IEEE XES (eXtensible Event Stream) is the first comprehensive IEEE standard for storing event data, established in 2016 and revised in 2023 (IEEE 1849-2023). However, the process mining community recognizes the need for a paradigm shift toward object-centric event data.

**Quote:** "The first comprehensive standard for storing event data was the IEEE Standard for eXtensible Event Stream (XES) [10]. XES became an official IEEE standard in 2016 [5]. The revised standard (IEEE 1849-2023) was published on 8 September 2023 and will be valid for another ten years [9]. XES has played a major role in the development of the field. However, within the process mining community, there seems to be a consensus that a paradigm shift is needed."

**Context:** Historical context of event log standards leading to OCEL 2.0.

---

### Pattern: OCEL 2.0 Formal Definition Using Set Theory

**Source:** 09-OCEL_20_Specification (Chunk 1:346-440)

**Description:** OCEL 2.0 provides formal mathematical definitions using set theory. It defines pairwise disjoint universes for events, event types, objects, object types, attribute names, attribute values, timestamps, and qualifiers. The formal OCEL tuple includes functions for type assignment, timestamps, attribute values, and qualified relationships.

**Quote:** "Definition 1 (Universes). Let UΣ be the universe of strings. We define the following pairwise disjoint universes:
- Uev ⊆ UΣ is the universe of events.
- Uetype ⊆ UΣ is the universe of event types (i.e., activities).
- Uobj ⊆ UΣ is the universe of objects.
- Uotype ⊆ UΣ is the universe of object types.
- Uattr ⊆ UΣ is the universe of attribute names.
- Uval is the universe of attribute values.
- Utime is the universe of timestamps
- Uqual ⊆ UΣ is the universe of qualifiers."

**Context:** Formal mathematical foundation of the OCEL 2.0 standard.

---

### Pattern: OCEL 2.0 Relational SQLite Implementation

**Source:** 09-OCEL_20_Specification (Chunk 1:801-846)

**Description:** OCEL 2.0 proposes a relational SQLite implementation with specific tables: event_map_type and object_map_type for type definitions, event and object tables with type assignments, event-type-specific tables (event_⊕mapET(et)) with timestamps and attributes, object-type-specific tables for attribute histories, event_object for E2O relationships, and object_object for O2O relationships.

**Quote:** "We propose a relational implementation of the standard, which adheres to Definition 2. In this implementation, starting from an object-centric event log L, we have:
- We have a table, event_map_type, reporting the distinct event types (ET(L)); and a table, object_map_type, reporting the distinct object types (OT(L)).
- We have a table, event, reporting the event type (evtype in Definition 2) for each event, and a table, object, reporting the object type (objtype in Definition 2) for each object.
- For every event type in ET(L), we have a different table... containing the events of the given event type along with their timestamp and attributes."

**Context:** Technical specification of relational database implementation for OCEL 2.0.

---

### Pattern: OCEL 2.0 Dense Tables for Efficient Storage

**Source:** 09-OCEL_20_Specification (Chunk 1:316-321)

**Description:** OCEL 2.0 uses dense tables where each table corresponds to a unique event or object type, storing only relevant attributes. This approach provides efficient storage, reduced data redundancy, scalability, and improved accessibility for analysis.

**Quote:** "Relational Specification based on Dense Tables: One major feature of OCEL 2.0 is its data structure using dense tables. Each table corresponds to a unique event or object type, storing only relevant attributes. This results in efficient use of storage space and less data redundancy. It also scales well, allowing for easy addition of new event or object types. The separate tables make the data more accessible and easy to understand, improving both efficiency and analysis in process mining."

**Context:** Key architectural feature of OCEL 2.0 relational implementation.

---

### Pattern: ISO 8601 Time Format for Timestamps

**Source:** 09-OCEL_20_Specification (Chunk 1:382-388)

**Description:** While the formalization maps time to non-negative reals, concrete implementations use ISO 8601 time format. Reference timestamps 0 (earliest) and infinity (latest) are used for convenience in the formalization.

**Quote:** "We would like to emphasize that these two reference timestamps (i.e., 0 and ∞) are chosen for convenience. In the formalization, time is mapped on the non-negative reals, but concrete implementations will use, for example, the ISO 8601 time format."

**Context:** Implementation guidance for timestamp handling.

---

## Paper: 12-Foundations_of_Process_Event_Data (Chunk 1)

### Pattern: IEEE XES Standard for Event Log Storage

**Source:** 12-Foundations_of_Process_Event_Data (Chunk 1:159-175)

**Description:** IEEE XES (eXtensible Event Stream) is an IEEE Standards Association-approved language for transporting, storing, and exchanging event data. It uses W3C XML Schema definition language for interoperability. XES defines log, trace, event, and attribute components. Classifiers assign identity to traces and events. Extensions define attribute sets for specific domains.

**Quote:** "This observation drove the development of the eXtensible Event Stream (XES) standard [1], an IEEE Standards Association-approved language to transport, store, and exchange event data. Its metadata structure is represented in Fig. 2. XES uses the W3C XML Schema definition language, guaranteeing interoperability between various systems. An IEEE XES instance corresponds to a file-based event log or formatted event stream that can be used to transfer event data in a unified manner. In IEEE XES, events are considered as an observed atomic granule of activity. Next to events, IEEE XES specifies the concept of a log, a trace, and an attribute component. Event and/or trace classifiers are used to assign an identity to traces and events."

**Context:** Description of XES standard for event log representation.

---

### Pattern: BPMN 2.0 Activity Lifecycle Model

**Source:** 12-Foundations_of_Process_Event_Data (Chunk 1:181-192)

**Description:** BPMN 2.0 provides a transactional lifecycle model describing states and state transitions that activities undergo during execution. IEEE XES also has an approved lifecycle extension specifying a default activity lifecycle state machine.

**Quote:** "When sourcing events from many process-aware information systems, events oftentimes relate to the transactional lifecycle that activities undergo. One example of such a transactional lifecycle model is shown in Fig. 3a. This is the transition lifecycle model of the BPMN 2.0 standard [2]. Such a transactional lifecycle model describes the states and state transitions which an activity might take in its execution. Also in IEEE XES, a lifecycle extension has been approved, which specifies a default activity lifecycle [3]. This state machine is shown in Fig. 3b."

**Context:** Discussion of event types and lifecycle transitions for activities.

---

### Pattern: JSON for Web-Based Platform Data

**Source:** 12-Foundations_of_Process_Event_Data (Chunk 1:302-315)

**Description:** JSON (JavaScript Object Notation) is a default standard for web-based platforms to store data. This includes data from online shopping, gaming, investing, trading, media consumption, social interaction platforms, and learning environments like MOOCs.

**Quote:** "Website and apps data are another unmistakably important source of event data. From online shopping, gaming, investing, trading, media consumption, to social interaction, online platforms are the main driver of modern B2C business models... Please note that, in many cases, including for instance learning environments such as MOOCs, a default standard for web-based platforms to store data is JSON (JavaScript Object Notation)."

**Context:** Discussion of event data sources and storage formats.

---

### Pattern: OCEL Standard for Object-Centric Event Data

**Source:** 12-Foundations_of_Process_Event_Data (Chunk 1:431-433)

**Description:** The OCEL standard provides a general standard to interchange object-centric event data with multiple case notions, addressing the need for artifact/object centricity in event log extraction.

**Quote:** "Finally, the recently introduced OCEL standard [4] is another relevant piece of work, putting forward a general standard to interchange object-centric event data with multiple case notions."

**Context:** Mention of OCEL in context of event log preparation techniques.

---

### Pattern: ETL Processing for Event Data Correlation

**Source:** 12-Foundations_of_Process_Event_Data (Chunk 1:463-470)

**Description:** Extract-Transform-Load (ETL) processing is a default technology for correlating event data from multiple non-integrated sources. ETL tools can derive and deploy matching schemes to integrate data. Data virtualization/federation provides an alternative to data consolidation.

**Quote:** "As such, an integration of these different sources should be achieved. Hereto, especially when an organizational data warehousing architecture is present, Extract-Transform-Load (ETL) processing would be a default technology to resort to. ETL tools are perfectly equipped to derive and deploy matching schemes to integrate data from non-integrated data sources."

**Context:** Discussion of techniques for event data correlation from multiple sources.

---

### Pattern: Ontology-Based Data Access (ODBA) for Event Log Extraction

**Source:** 12-Foundations_of_Process_Event_Data (Chunk 1:428-431)

**Description:** Ontology-based data access (ODBA) uses an ontological view of the domain linked to a database schema for event log extraction. This approach is implemented in the Onprom tool.

**Quote:** "One noteworthy scientific initiative in this context is ontology-based data access (ODBA) for event log extraction [13, 14]. The approach is based on an ontological view of the domain of interest and linking it as such to a database schema and has been implemented in the Onprom tool."

**Context:** Description of semantic approach to event log extraction.

---

## Paper: 21-LLM_Smart_Contracts_from_BPMN (Chunk 1)

### Pattern: BPMN 2.0 Choreographies for Process Modeling

**Source:** 21-LLM_Smart_Contracts_from_BPMN (Chunk 1:338-343)

**Description:** BPMN 2.0 Choreographies are used for process modeling in blockchain-based execution. This is a practical implementation choice given lack of consensus on the best fitting modeling paradigm for blockchain-based execution. Chorpiler tool transforms BPMN Choreographies to smart contracts.

**Quote:** "In the current instantiation of our framework, we support BPMN 2.0 Choreographies. This is a purely practical implementation choice, given that there is no consensus on the best fitting modelling paradigm for blockchain-based execution (c.f. [39]) and given our familiarity with a suitable tool. We instantiate our framework for an Ethereum virtual machine (EVM) blockchain environment, the most widely employed environment [39]."

**Context:** Explanation of process modeling choice for LLM-based smart contract generation.

---

### Pattern: Chorpiler Tool for BPMN to Smart Contract Transformation

**Source:** 21-LLM_Smart_Contracts_from_BPMN (Chunk 1:346-354)

**Description:** Chorpiler is an open source tool that transforms BPMN Choreographies to smart contracts, generates non-conforming traces, and creates machine-readable encodings for contract interaction. It parses choreographies into interaction nets (special type of labelled Petri net).

**Quote:** "We extend the open source tool Chorpiler, first introduced in [40] with simulation capabilities. Chorpiler transforms BPMN Choreographies to smart contracts, generates non-conforming traces from conforming traces, and also generates machine-readable encodings on how to interact with a contract. Chorpiler parses a given Choreography into an interaction net, a special type of labelled Petri net (see [13]), suitable to represent choreographies."

**Context:** Technical description of the Chorpiler tool for process-to-contract transformation.

---

### Pattern: Hardhat for Ethereum Smart Contract Testing

**Source:** 21-LLM_Smart_Contracts_from_BPMN (Chunk 1:362-367)

**Description:** Hardhat is a popular Ethereum development framework for testing, deployment, and debugging of smart contracts in a locally simulated EVM environment. Used in benchmarking framework for LLM-generated smart contracts.

**Quote:** "To provide the replayer with a blockchain environment, we use hardhat, a popular Ethereum development framework that allows testing, deployment, and debugging of smart contracts in a locally simulated EVM environment."

**Context:** Implementation details of smart contract testing infrastructure.

---

### Pattern: pm4py Library for Petri Net Trace Generation

**Source:** 21-LLM_Smart_Contracts_from_BPMN (Chunk 1:351-354)

**Description:** pm4py is a popular Python library for process mining that includes playout functionality to generate event log traces from Petri nets. Used to generate conforming traces for smart contract benchmarking.

**Quote:** "We make use of this intermediate presentation to generate conforming traces. Here, we adopt the implementation of pm4py [6], a popular Python library for process mining, which includes a playout functionality to generate event log traces from Petri nets."

**Context:** Technical tool used for trace generation in benchmarking framework.

---

### Pattern: Solidity Smart Contracts for Ethereum

**Source:** 21-LLM_Smart_Contracts_from_BPMN (Chunk 1:134-136)

**Description:** Solidity is the programming language for Ethereum smart contracts. LLMs are trained on code including Solidity for blockchain smart contracts, enabling them to analyze and create smart contracts.

**Quote:** "In the case of LLMs, training ingests very large textual corpora, comprising not only natural language, but also programming code (such as Solidity for blockchain smart contracts), and formal representations (such as BPMN for modeling business processes)."

**Context:** Discussion of LLM training data including smart contract languages.

---

### Pattern: BPMN XML with Boolean Conditions for XOR Gateways

**Source:** 21-LLM_Smart_Contracts_from_BPMN (Chunk 1:400-411)

**Description:** Pre-processing BPMN models requires adding execution-relevant information for exclusive gateways. Boolean conditions are inserted for outgoing flows other than default flows. BPMN 2.0 Diagram Interchange is removed to reduce input size. Start and end events are merged to single events.

**Quote:** "When no default flow was marked, we set the first outgoing flow to the default flow. Then, for all other outgoing flows, we inserted a boolean condition. Furthermore, we removed any Signavio extension elements. To reduce the size of LLM input, we also removed the BPMN 2.0 Diagram Interchange, as it only contains additional information required to visualise the model. Finally, we merged all start and end events, so each model contains only one, to adhere to the implementation limitation of Chorpiler."

**Context:** Pre-processing requirements for BPMN models in smart contract generation.

---

## Paper: 31-BBO_BPMN_Ontology (Chunk 1)

### Pattern: BPMN 2.0 Meta-Model for Business Process Representation

**Source:** 31-BBO_BPMN_Ontology (Chunk 1:79-88)

**Description:** BPMN (Business Process Model and Notation) is the most adopted meta-model for representing business processes, maintained by OMG (Object Management Group). BPMN provides finer-grained representation than EPC (Event Process driven Chain) with defined execution logic for its elements.

**Quote:** "In the literature, Business Process Model and Notation (BPMN) is the most adopted meta-model for representing BPs (OMG., 2011). Indeed, it is a standard for BPM maintained by the Object Management Group (OMG). In spite of its industrial maturity, BPMN does not support the representation of some process specifications such as the material resources required to carry out a given task, or the workstation where a given task should be performed."

**Context:** Introduction of BPMN 2.0 as basis for BBO ontology.

---

### Pattern: OWL 2 DL Implementation with Protege

**Source:** 31-BBO_BPMN_Ontology (Chunk 1:359-363)

**Description:** BBO ontology is formalized and implemented in OWL 2 DL using Protege. Conversion rules automatically generate OWL representation from UML diagrams. Natural language specifications from BPMN document are manually formalized in OWL.

**Quote:** "We have formalized and implemented the conceptual model of BBO in OWL 2 DL using Protege. First, we designed and applied a set of conversion rules that automatically generated an OWL representation from the UML diagrams of BBO. Second, we manually turned various natural language specifications in the BPMN document into a formal OWL representation."

**Context:** Implementation approach for BBO ontology.

---

### Pattern: UML to OWL Conversion Algorithm

**Source:** 31-BBO_BPMN_Ontology (Chunk 1:368-386)

**Description:** Systematic algorithm for converting UML class diagrams to OWL: UML classes become OWL classes, relations become OWL ObjectProperties, class attributes become ObjectProperties (if type is UML class) or DataProperties (otherwise), cardinalities transform to qualified cardinality restrictions using subClassOf with exactly, min, or max constraints.

**Quote:** "Generating an OWL representation from the UML diagrams results in the following algorithm:
- For each UML class, create an owl class
- For each relation between UML classes create an OWL ObjectProperty
- For each class attribute: If the type is an UML class, create an OWL ObjectProperty. Otherwise, create an OWL DataProperty
- Cardinalities have been transformed into qualified cardinality restrictions."

**Context:** Technical specification of UML-to-OWL conversion rules.

---

### Pattern: OWL Cardinality Restrictions from UML Multiplicities

**Source:** 31-BBO_BPMN_Ontology (Chunk 1:377-386)

**Description:** UML cardinalities are transformed to OWL qualified cardinality restrictions: [x..x] becomes exactly x, [x..n] becomes min x, [0..x] becomes max x, all using subClassOf axioms.

**Quote:** "UClass1 UProperty [x..x] UClass2 => OClass1 subClassOf OProperty exactly x OClass2
UClass1 UProperty [x..n] UClass2 => OClass1 subClassOf OProperty min x OClass2
UClass1 UProperty [0..x] UClass2 => OClass1 subClassOf OProperty max x OClass2"

**Context:** Detailed cardinality conversion rules from UML to OWL.

---

### Pattern: Natural Language to OWL Specification Conversion

**Source:** 31-BBO_BPMN_Ontology (Chunk 1:409-445)

**Description:** BPMN natural language specifications are manually converted to OWL restrictions. Two categories: (i) constraints on existing properties using subClassOf with some/not restrictions, (ii) new class definitions using equivalentTo with intersection and cardinality restrictions.

**Quote:** "Specification in natural language: A Start Event MUST be a source for a Sequence Flow.
Formalized Specification: StartEvent subClassOf has_outgoing some SequenceFlow

Specification in natural language: A Gateway with a gatewayDirection of converging MUST have multiple incoming Sequence Flows, but MUST NOT have multiple outgoing Sequence Flows.
Formalized Specification: ConvergingGateway equivalentTo (Gateway and (has_incoming min 2 SequenceFlow) and (has_outgoing exactly 1 SequenceFlow))"

**Context:** Examples of converting BPMN textual specifications to formal OWL axioms.

---

### Pattern: BPMN Flow Elements: SequenceFlow, FlowNode, Activity, Event, Gateway

**Source:** 31-BBO_BPMN_Ontology (Chunk 1:220-242)

**Description:** BPMN Process is a subclass of FlowElementsContainer composed of FlowElements. FlowElements includes SequenceFlow (transitions with optional condition Expression) and FlowNode (activities: Task, Sub-Process, CallActivity; Events; and Gateways). Activities relate to LoopCharacteristics for iteration.

**Quote:** "Process is a sub-class of FlowElementsContainer. Describing a process consists in defining the FlowElements that compose it. FlowElements class has two sub-classes: SequenceFlow and FlowNode. SequenceFlow represents transitions that ensure the move from the source FlowNode to the target one. A SequenceFlow may depend on a given condition, which is represented as an instance of Expression class. FlowNode class groups the activities that compose a process:
- Activity is the work to be performed. Activity class has three sub-classes: Task (atomic), Sub-Process (complex with several Tasks), CallActivity (calls a CallableElement)
- Event is something that 'happens' during the course of a process
- Gateway is used to control how SequenceFlows interact"

**Context:** Core BPMN concepts reused in BBO ontology.

---

### Pattern: SPARQL Queries for Competency Question Validation

**Source:** 31-BBO_BPMN_Ontology (Chunk 1:485-533)

**Description:** SPARQL queries are designed to validate that the ontology can answer competency questions. Queries select resources, places, next tasks, and resource types from the instantiated knowledge base. HermiT, Fact, and Pellet reasoners verify ontology consistency.

**Quote:** "SELECT ?resource WHERE
{ BBO:T1 BBO:has_ioSpecification ?io.
  ?io BBO:has_resourceInputs ?resource.}
Result: R2

SELECT ?nextTask WHERE
{ BBO:T1 BBO:has_outgoing ?SequenceFlow.
  ?SequenceFlow BBO:has_targetRef ?nextTask.
  ?nextTask a BBO:Task}
Result: T2"

**Context:** Validation of BBO ontology using SPARQL queries against populated knowledge base.

---

### Pattern: rdfs:comment for BPMN Element Descriptions

**Source:** 31-BBO_BPMN_Ontology (Chunk 1:424-428)

**Description:** For each BPMN element, the description from BPMN 2.0 specification is added using rdfs:comment property. Reasoners (HermiT, Fact, Pellet) verify ontology consistency before and after population with business process assertions.

**Quote:** "As a first stage, for each BPMN element, we added its description as mentioned in BPMN 2.0 specification (OMG., 2011) using the rdfs:comment property. Class definitions in Table 4 are particularly interesting for the automatic classification of instances. According to the various reasoners in Protege (i.e., Hermit, Fact and Pellet), the ontology is consistent and remains consistent, even after its population with assertions describing several BP models."

**Context:** Documentation approach and consistency verification for BBO ontology.

---

### Pattern: Unit Ontology (UO) for Parameter Units of Measure

**Source:** 31-BBO_BPMN_Ontology (Chunk 1:288-289)

**Description:** The UnitOfMeasure class in BBO is specified using Unit and Prefix concepts from the UO (Unit Ontology). This allows standardized representation of parameter values with their units.

**Quote:** "The UnitOfMeasure class is specified using the two concepts Unit and Prefix of the unit measures ontology UO (UO-onto, 2019)."

**Context:** Reuse of external ontology for unit specifications in BBO.

---

### Pattern: Camunda for BPMN Graphical Representation

**Source:** 31-BBO_BPMN_Ontology (Chunk 1:481-484)

**Description:** Camunda is an open source software used to represent business processes with BPMN graphical elements. This visualization step aids communication with experts and validation of process representations before ontology population.

**Quote:** "For each BP description, (1) we represent this BP with BPMN graphical elements using an open source software, Camunda (https://camunda.com/): this step is not mandatory to instantiate BBO, however it is more convenient to communicate with experts and to validate BP representations"

**Context:** Tooling used for BPMN visualization in BBO ontology workflow.

---

### Pattern: Schema Metrics for Ontology Evaluation (RD and SD)

**Source:** 31-BBO_BPMN_Ontology (Chunk 1:454-466)

**Description:** Two schema metrics evaluate BBO: Relationship Diversity (RD = NR/(NR+NH)) indicates richness beyond taxonomy with diverse relationships (>50%); Schema Deepness (SD = NH/NC) indicates detailed domain coverage (low value = deep/vertical ontology).

**Quote:** "RD = NR / (NR+ NH), which exceeds for us 50%. This ratio indicates that BBO is not just a hierarchy of subclasses, but it is also rich with relationships that describe the knowledge domain.
SD = NH/NC. This measure describes the distribution of classes across different levels of the ontology class hierarchy. The SD value of BBO is low (less than one hypernymy link per class): it means that the ontology is deep (or vertical): it covers a knowledge domain (i.e., BPs) in a detailed manner."

**Context:** Quantitative evaluation approach for ontology quality.

---
