# Batch Extraction: framework_comparison (Batch 2 of 4)

**Field:** framework_comparison
**Description:** How this ontology compares to others (UFO, PROV-O, BBO, ArchiMate, TOGAF, OCEL)
**Extraction Date:** 2025-12-28

---

## Paper: 09-OCEL_20_Specification

### Pattern: OCEL 2.0 vs XES Comparison
- **Source:** 09-OCEL_20_Specification (Chunk 1:37-40)
- **Description:** OCEL 2.0 is compared to the IEEE XES standard, highlighting that OCEL 2.0 is more expressive, less complicated, and better readable than XES for object-centric event data.
- **Quote:** "Compared to XES, it is more expressive, less complicated, and better readable. OCEL 2.0 offers three exchange formats: a relational database (SQLite), XML, and JSON format."
- **Context:** The abstract section positions OCEL 2.0 as a successor to both OCEL 1.0 and as an alternative to XES for object-centric process mining.

### Pattern: OCEL 2.0 vs OCEL 1.0 Comparison
- **Source:** 09-OCEL_20_Specification (Chunk 1:33-40)
- **Description:** OCEL 2.0 extends OCEL 1.0 with new capabilities for depicting changes in objects, providing information on object relationships, and qualifying relationships to other objects or specific events.
- **Quote:** "In contrast to the first OCEL standard, it can depict changes in objects, provide information on object relationships, and qualify these relationships to other objects or specific events."
- **Context:** The abstract establishes the evolution from OCEL 1.0 to 2.0.

### Pattern: OCEL vs Traditional Process Modeling Notations
- **Source:** 09-OCEL_20_Specification (Chunk 1:117-127)
- **Description:** OCEL addresses limitations of traditional process mining approaches and notations like DFGs, BPMN, UML activity diagrams, workflow nets, and process trees that assume single-case events.
- **Quote:** "The same applies to mainstream process modeling notations like Directly-Follows-Graphs (DFGs), BPMN models, UML activity diagrams, workflow nets, and process trees. However, most real-life events involve multiple objects. Traditional process mining approaches require the flattening of event data in order to satisfy this assumption. This may lead to misleading analysis results."
- **Context:** Section 2 on Introduction to Object-Centric Process Mining explains why traditional approaches fall short.

### Pattern: XES Historical Context and OCEL Paradigm Shift
- **Source:** 09-OCEL_20_Specification (Chunk 1:237-243)
- **Description:** XES became an IEEE standard in 2016 and was revised in 2023, but there is consensus in the process mining community that a paradigm shift toward object-centric event data standards is needed.
- **Quote:** "The first comprehensive standard for storing event data was the IEEE Standard for eXtensible Event Stream (XES) [10]. XES became an official IEEE standard in 2016 [5]. The revised standard (IEEE 1849-2023) was published on 8 September 2023 and will be valid for another ten years [9]. XES has played a major role in the development of the field. However, within the process mining community, there seems to be a consensus that a paradigm shift is needed."
- **Context:** Section 3 on Metamodel of the OCEL 2.0 Standard provides historical perspective.

### Pattern: OCEL 1.0 Limitations and Extensions in OCEL 2.0
- **Source:** 09-OCEL_20_Specification (Chunk 1:198-203)
- **Description:** OCEL 1.0 did not include Object-to-Object (O2O) relationships, qualifiers for O2O and E2O relationships, or changing object attribute values. OCEL 2.0 addresses these limitations.
- **Quote:** "The first OCEL format (OCEL 1.0) provided an event log standard that could capture events related to multiple objects with attributes but did not include Object-to-Object (O2O) relationship, qualifiers for either O2O and E2O relationships, or changing object attribute values [7, 8]. OCEL 2.0 addresses these limitations by providing a new metamodel and three storage formats, including a relational implementation of the standard."
- **Context:** Section 2 detailing the limitations that motivated OCEL 2.0 development.

### Pattern: OCEL 2.0 vs OCEL 1.0 Feature Comparison
- **Source:** 09-OCEL_20_Specification (Chunk 1:251-260)
- **Description:** OCEL 1.0 could store various types of events and objects, link objects of different types to events, and add multiple attributes, but OCEL 2.0 extends this with O2O relationships, dynamic attributes, and relationship qualifiers.
- **Quote:** "The first version of the object-centric event log standard, OCEL 1.0, was a big step forward for object-centric process mining [7,8]. It can store various types of events and objects in one log and link objects of different types to each event, giving a more detailed picture. OCEL 1.0 also allowed for adding multiple attributes to each event and object, providing even more information."
- **Context:** Section 3 on the Metamodel comparing OCEL versions.

### Pattern: OCED Working Group and Standards Discussion
- **Source:** 09-OCEL_20_Specification (Chunk 1:266-278)
- **Description:** The IEEE Task Force on Process Mining conducted a survey and formed the OCED Working Group, but discussions did not converge due to conflicting requirements between expressiveness vs simplicity and different implementation paradigms (relational vs graph-based).
- **Quote:** "In 2021, a survey was conducted by the IEEE Task Force on Process Mining [12]. The goal was to collect requirements for a new standard succeeding XES... Unfortunately, the discussions in the OCED Working Group did not converge after 1.5 years of discussion. This was due to conflicting requirements (expressiveness versus simplicity), different implementation paradigms (relational versus graph-based), and a lack of clarity on who would implement things."
- **Context:** Background on the development of OCEL 2.0 and standards landscape.

---

## Paper: 10-OC-PM_Object-Centric_Process_Mining

### Pattern: OCPM vs Artifact-Centric Approaches
- **Source:** 10-OC-PM_Object-Centric_Process_Mining (Chunk 2:315-352)
- **Description:** Artifact-centric process mining focuses on single artifacts and their interactions, with conformance checking and discovery from relational databases. The limitation is lack of comprehensive tool support and dependence on relational database schema.
- **Quote:** "Artifact-centric process mining is based on defining the properties of key business-relevant entities called business artifacts. In particular, the proposed techniques focus on the modeling of the single artifacts and their interactions... A limitation of these approaches is the lack of comprehensive tool support and the dependence on a relational database schema."
- **Context:** Section 5.1 on Related Work - Artifact-centric approaches.

### Pattern: OCPM vs Object-Centric Behavioral Constraint Models (OCBC)
- **Source:** 10-OC-PM_Object-Centric_Process_Mining (Chunk 2:356-365)
- **Description:** OCBC models are declarative models with rich semantics but have scalability issues due to storing the entire state of the object model for each event.
- **Quote:** "In [13], the object-centric behavioral constraint models (OCBC) are proposed as declarative models with rich semantics that can describe the interaction between the different entities of a database and the activities recorded in an object-centric event log... However, the discovery of the rich set of constraints and the proposed event log format (storing the entire state of the object model for each event) have scalability issues."
- **Context:** Section 5.2 on Related Work - Object-centric behavioral constraint models.

### Pattern: OCPM vs Colored Petri Nets
- **Source:** 10-OC-PM_Object-Centric_Process_Mining (Chunk 2:376-389)
- **Description:** Colored Petri nets allow token colors and expressions but proposing a process discovery algorithm for them is an enormous challenge due to their rich semantics.
- **Quote:** "Colored Petri nets [15] have been proposed in the '80 and have a wide range of applications. Colored Petri nets allow the storage of a data value for each token... Given their rich semantics, the proposal of a process discovery algorithm able to manage colors, color sets, expressions, and guards is an enormous challenge."
- **Context:** Section 5.3 on Related Work - Petri nets-based approaches.

### Pattern: OCPM vs Graph and Process Querying Approaches
- **Source:** 10-OC-PM_Object-Centric_Process_Mining (Chunk 2:400-418)
- **Description:** Graph databases (like Neo4j) are used for storing and querying object-centric event data, but scalability on process mining tasks is disappointing.
- **Quote:** "In [18,19], the usage of graph databases for the storage, querying, and aggregation of object-centric event data is proposed... However, the scalability of graph databases on process mining tasks still needs to be investigated thoroughly. In [20], the execution time of process mining tasks in a popular graph database (Neo4J) is shown to be disappointing."
- **Context:** Section 5.4 on Related Work - Graph and process querying.

### Pattern: OCPM vs Ontology-Based Event Data Extraction
- **Source:** 10-OC-PM_Object-Centric_Process_Mining (Chunk 2:417-418)
- **Description:** Ontology-based extraction of event data has been proposed as an alternative approach.
- **Quote:** "An approach for ontology-based extraction of event data has been proposed in [22]."
- **Context:** Section 5.4 mentions ontology-based approaches.

### Pattern: OCPM vs Flattening-Based Process Discovery
- **Source:** 10-OC-PM_Object-Centric_Process_Mining (Chunk 2:421-451)
- **Description:** Flattening-based discovery projects object-centric event logs into different object types and applies traditional process discovery methods. Object-centric DFGs and Object-centric Petri nets are building blocks for this approach.
- **Quote:** "A discovery operation can be defined by flattening (see Def. 11) the object-centric event log into the different object types, discovering traditional process models (as an example, a DFG or a Petri net) on top of the flattened logs and then collating the results together."
- **Context:** Section 5.5 on Related Work - Flattening-based process discovery.

### Pattern: OCEL Format Tool Support
- **Source:** 10-OC-PM_Object-Centric_Process_Mining (Chunk 2:199-203)
- **Description:** The web-based OC-PM tool enables upload of object-centric event logs in JSON-OCEL or XML-OCEL formats.
- **Quote:** "The first page of the tool enables the upload of an object-centric event log in the JSON-OCEL or XML-OCEL formats [10]. Some of these logs are available at the address http://www.ocel-standard.org/"
- **Context:** Section 4.1 on the OC-PM web-based tool.

### Pattern: Flattening to XES Format
- **Source:** 10-OC-PM_Object-Centric_Process_Mining (Chunk 2:283-285)
- **Description:** The tool supports flattening object-centric event logs to traditional event logs saved in XES format.
- **Quote:** "the download of the filtered event log in the JSON-OCEL or XML-OCEL is available, and the possibility to flatten the object-centric event log to a traditional event log saved in the XES format is offered"
- **Context:** Section 4.1 on additional features of the OC-PM tool.

---

## Paper: 11-Process_Mining_Event_Knowledge_Graphs

### Pattern: Event Knowledge Graphs vs Classical Event Logs
- **Source:** 11-Process_Mining_Event_Knowledge_Graphs (Chunk 1:13-21)
- **Description:** Classical process mining relies on unique case identifiers that partition event data into independent sequences. Event knowledge graphs model behavior over multiple entities as a network of events instead.
- **Quote:** "Classical process mining relies on the notion of a unique case identifier, which is used to partition event data into independent sequences of events. In this chapter, we study the shortcomings of this approach for event data over multiple entities. We introduce event knowledge graphs as data structure that allows to naturally model behavior over multiple entities as a network of events."
- **Context:** Abstract introducing the event knowledge graph approach.

### Pattern: Event Knowledge Graphs vs OCEL
- **Source:** 11-Process_Mining_Event_Knowledge_Graphs (Chunk 1:236-239)
- **Description:** Event tables with entity types formalize object-centric event logs (OCEL) using the more general term "entity" instead of "object" to study behavior over entities that are not tangible objects.
- **Quote:** "Note that Definition 2 formalizes the object-centric event logs (OCEL) described in Sect. 3.4 of [1]; we here use the more general term 'entity' instead of 'object' as we will later study behavior over entities which are not tangible objects."
- **Context:** Section 2.1 on Events, connecting to OCEL standard.

### Pattern: Event Knowledge Graphs vs Traditional Traces
- **Source:** 11-Process_Mining_Event_Knowledge_Graphs (Chunk 1:161-168)
- **Description:** Instead of extracting all events toward a single case identifier, the approach keeps events local to correlated entities and constructs temporal order only between related events.
- **Quote:** "instead of defining one global directly-follows relation for all events based on a global case identifier, we define a local directly-follows relation per entity [30, Def. 4.6]."
- **Context:** Section 3.3 on Correct Behavioral Information using local directly-follows.

### Pattern: Problems of Convergence and Divergence in Classical Event Logs
- **Source:** 11-Process_Mining_Event_Knowledge_Graphs (Chunk 1:434-449)
- **Description:** Classical event log extraction introduces false behavioral information through divergence (duplicated events) and convergence (false temporal ordering between unrelated events).
- **Quote:** "Note that the event log in Table 2 contains numerous false behavioral information. Some events were duplicated and occur in both traces, e.g., e3, e4, e6, e19, e29, suggesting that in total four Supplier Orders were placed and received (while there were only two)... This is also known as divergence. Further, the order of events in both traces gives false behavior information... This is also known as convergence."
- **Context:** Section 3.2 on False Behavioral Information in Classical Event Logs.

### Pattern: Labeled Property Graphs vs RDF
- **Source:** 11-Process_Mining_Event_Knowledge_Graphs (Chunk 1:681-682)
- **Description:** While event knowledge graph nodes and relationships can be encoded in RDF, the df-paths rely on attributes of relationships which are not supported by RDF but are supported by labeled property graphs.
- **Quote:** "While the nodes and relationships of Definition 8 can also be encoded in RDF [11], the df-paths rely on attributes of relationships (Definition 9) which are not supported by RDF but by LPGs."
- **Context:** Section 4.2 on Formal Definition of an Event Knowledge Graph.

### Pattern: Event Knowledge Graphs vs XOC Event Logs
- **Source:** 11-Process_Mining_Event_Knowledge_Graphs (Chunk 1:339-342)
- **Description:** Relations and cardinalities recovered from event tables are static views, while processes update relations dynamically. Modeling such dynamics requires additional concepts as defined in XOC event logs.
- **Quote:** "Note that Definition 5 does not impose the direction of a relation... relations and their cardinalities recovered according to Definition 5 are a static view of the relations obtained by aggregating all observations over time while a process updates relations dynamically. For instance, Order O1 was not related to any Item until event e27. Modeling such dynamics requires additional concepts as defined in XOC event logs [39,40]."
- **Context:** Section 2.3 on Relations Between Entities.

### Pattern: Event Knowledge Graph Construction from Relational Databases
- **Source:** 11-Process_Mining_Event_Knowledge_Graphs (Chunk 1:959-965)
- **Description:** Event knowledge graphs can be extracted from event tables and relational databases, with a variant called "causal event graph" that only models events without entities.
- **Quote:** "All steps of the method can be implemented as a series of Cypher queries to construct event knowledge graphs in a graph database for our running example as well as for various real-life datasets comprising single and multiple event tables; several event knowledge graphs of real-life processes are available. A variant of event knowledge graphs, called causal event graph that only models events but not the entities, can be extracted automatically from relational databases [56]."
- **Context:** Section 4.5 on Creating Event Knowledge Graphs from Real-Life Data.

### Pattern: Event Knowledge Graphs vs Event Logs for Multi-Entity Analysis
- **Source:** 11-Process_Mining_Event_Knowledge_Graphs (Chunk 1:536-542)
- **Description:** Extracting a collection of related sequential event logs separates behavioral information per entity-type, hindering reasoning about the process as a whole. Event knowledge graphs address this limitation.
- **Quote:** "We cannot represent this information in a single table or a sequential event log. Extracting a collection of related sequential event logs from event tables [46] and relational databases [41] results in collection of directly-follows relations per entity-type. However, the behavioral information remains separated per entity type, hindering reasoning about the process as a whole [25]. We therefore turn to a graph-based data model."
- **Context:** Section 3.3 on moving from event logs to graph-based models.

---

## Paper: 12-Foundations_of_Process_Event_Data

### Pattern: XES Standard for Event Data Storage
- **Source:** 12-Foundations_of_Process_Event_Data (Chunk 1:162-175)
- **Description:** The XES (eXtensible Event Stream) standard is an IEEE-approved language for transporting, storing, and exchanging event data, using XML Schema and allowing extensions for domain-specific attributes.
- **Quote:** "This observation drove the development of the eXtensible Event Stream (XES) standard [1], an IEEE Standards Association-approved language to transport, store, and exchange event data. Its metadata structure is represented in Fig. 2. XES uses the W3C XML Schema definition language, guaranteeing interoperability between various systems."
- **Context:** Section 2.3 on Storing Event Data.

### Pattern: XES vs BPMN Lifecycle Models
- **Source:** 12-Foundations_of_Process_Event_Data (Chunk 1:183-186)
- **Description:** Both BPMN 2.0 and XES have activity lifecycle models for event types. BPMN 2.0 has a transition lifecycle model, while XES has an approved lifecycle extension with a default activity lifecycle.
- **Quote:** "One example of such a transactional lifecycle model is shown in Fig. 3a. This is the transition lifecycle model of the BPMN 2.0 standard. Such a transactional lifecycle model describes the states and state transitions which an activity might take in its execution. Also in IEEE XES, a lifecycle extension has been approved, which specifies a default activity lifecycle."
- **Context:** Section 2.4 on Event Types.

### Pattern: OCEL Standard for Object-Centric Event Data
- **Source:** 12-Foundations_of_Process_Event_Data (Chunk 1:431-433)
- **Description:** The OCEL standard is a general standard to interchange object-centric event data with multiple case notions.
- **Quote:** "Finally, the recently introduced OCEL standard is another relevant piece of work, putting forward a general standard to interchange object-centric event data with multiple case notions."
- **Context:** Section 4.1 on Extraction of Event Data.

### Pattern: Ontology-Based Data Access (ODBA) for Event Log Extraction
- **Source:** 12-Foundations_of_Process_Event_Data (Chunk 1:428-430)
- **Description:** The Onprom tool implements ontology-based data access for event log extraction, based on an ontological view of the domain linked to database schema.
- **Quote:** "One noteworthy scientific initiative in this context is ontology-based data access (ODBA) for event log extraction [13, 14]. The approach is based on an ontological view of the domain of interest and linking it as such to a database schema and has been implemented in the Onprom tool."
- **Context:** Section 4.1 on Extraction of Event Data.

### Pattern: PM2 Methodology vs CRISP-DM
- **Source:** 12-Foundations_of_Process_Event_Data (Chunk 1:370-375)
- **Description:** The PM2 process mining methodology defines four event data preprocessing tasks (creating views, filtering logs, enriching logs, aggregating events) that are tailored to process mining and have no immediate corresponding task in CRISP-DM.
- **Quote:** "When making an assessment of one of the most recently introduced process mining methodologies, i.e. PM2 [56], four event data preprocessing tasks are defined: (1) creating views, (2) filtering logs, (3) enriching logs, and (4) aggregating events. All these tasks are tailored to the process mining context, and have no immediate corresponding task in a classical data analytics pipeline."
- **Context:** Section 3.2 on Comparison with Classical Analytics Data Preprocessing.

### Pattern: XES Survey and Standards Evolution
- **Source:** 12-Foundations_of_Process_Event_Data (Chunk 1:434-436)
- **Description:** The IEEE Task Force is working on reinventing the IEEE XES standard to address data-related challenges, particularly to capture semantics of event data and support complex data structures.
- **Quote:** "There is also ongoing work by the IEEE Task force on reinventing the IEEE XES standard to address several identified data related challenges in the XES survey [57], in particular, to capture the semantics of event data and to support complex data structures."
- **Context:** Section 4.1 discussing evolution of standards.

---

## Paper: 23-UFO_Story_Ontological_Foundations

### Pattern: UFO vs BWW (Bunge-Wand-Weber) Ontology
- **Source:** 23-UFO_Story_Ontological_Foundations (Chunk 1:103-125)
- **Description:** UFO was developed as an alternative to BWW because Bunge's philosophy of science was designed for hard sciences, not for conceptual modeling which requires consideration of human cognition and linguistic competence. BWW predictions conflicted with modelers' intuitions.
- **Quote:** "Despite being inspired by the goals of the BWW approach, we did not share their research direction. Bunge's objective was doing philosophy of science and, being a physicist, chiefly, philosophy of the hard sciences. Conceptual Modeling, in contrast, is about 'representing aspects of the physical and social world for the purpose of understanding and communication'... any attempt to develop ontological foundations for conceptual modeling should take both human cognition and human linguistic competence seriously; it should be a project in descriptive metaphysics and not in revisionary ontology."
- **Context:** Section 2 on A brief historical background.

### Pattern: UFO vs DOLCE and GFO
- **Source:** 23-UFO_Story_Ontological_Foundations (Chunk 1:137-162)
- **Description:** UFO was initially an attempt to unify DOLCE and GFO (General Formalized Ontology), but these existing ontologies lacked sufficient theories for entity types and domain relations needed for conceptual modeling.
- **Quote:** "In this setting, our first attempt was to unify DOLCE and GFO to produce a reference foundational ontology for conceptual modeling (hence, the name Unified Foundational Ontology)... It became clear quite soon, however, that further investigation was needed, with a focus on the requirements of the conceptual modeling discipline. In particular, ontological foundations for conceptual modeling would demand micro-theories to address conceptual modeling's most fundamental constructs, namely, Entity Types and Relationship Types."
- **Context:** Section 2 on historical development of UFO.

### Pattern: UFO vs GFO Theory of Relations
- **Source:** 23-UFO_Story_Ontological_Foundations (Chunk 1:158-162)
- **Description:** The GFO theory of relations is subject to Bradley Regress and can only be instantiated by infinite logical models, making it unsuitable for conceptual modeling applications.
- **Quote:** "Regarding the latter, DOLCE still does not include a theory of particularized relational properties (relational qualities) and the GFO theory of relations is subject to the so-called Bradley Regress (Bradley, 1893) and, hence, it can only be instantiated by infinite (logical) models. This feature makes it unsuitable for conceptual modeling applications."
- **Context:** Section 2 explaining why existing ontologies were insufficient.

### Pattern: UFO Applications to Modeling Languages and Standards
- **Source:** 23-UFO_Story_Ontological_Foundations (Chunk 1:196-198)
- **Description:** UFO has been used to analyze, reengineer, and integrate modeling languages and standards including UML, TOGAF, ArchiMate, RM-ODP, TROPOS/i*, AORML, ARIS, and BPMN.
- **Quote:** "Over the years, UFO has been employed as a basis for analyzing, reengineering and integrating many modeling languages and standards in different domains (e.g., UML, TOGAF, ArchiMate, RM-ODP, TROPOS/i*, AORML, ARIS, BPMN) as well as for the development of Core and Domain Ontologies in different areas."
- **Context:** Section 3 on The unified foundational ontology and its applications.

### Pattern: OntoUML vs UML 2.0
- **Source:** 23-UFO_Story_Ontological_Foundations (Chunk 1:213-222)
- **Description:** OntoUML was conceived as an ontologically well-founded version of UML 2.0 class diagrams, with a worldview isomorphic to UFO-A distinctions and formal syntactical constraints that delimit valid models.
- **Quote:** "OntoUML (Guizzardi, 2005) was conceived as an ontologically well-founded version of the UML 2.0 fragment of class diagrams. The idea was to employ the ontology-based language engineering method... to design a language for structural conceptual modeling... that would have two main characteristics. Firstly, the worldview embedded in the language through its conceptual primitives... should be isomorphic to the ontological distinctions put forth by UFO-A. Secondly, the language metamodel should incorporate formal syntactical constraints."
- **Context:** Section 4 on OntoUML: Language, engineering support and its applications.

### Pattern: OntoUML Adopted by ORM 2.0
- **Source:** 23-UFO_Story_Ontological_Foundations (Chunk 1:225-226)
- **Description:** Some foundational theories underlying OntoUML have been adopted by other conceptual modeling languages, including ORM 2.0.
- **Quote:** "In addition, some of the foundational theories underlying OntoUML have also been adopted by other conceptual modeling languages, e.g., ORM 2.0 (Halpin & Morgan, 2008; Halpin, 2010)."
- **Context:** Section 4 on OntoUML adoption.

### Pattern: OntoUML Code Generation to Multiple Languages
- **Source:** 23-UFO_Story_Ontological_Foundations (Chunk 1:302-317)
- **Description:** OntoUML conceptual models can be mapped to different codification languages (OWL DL, RDFS, F-Logic, Haskell, Relational Database languages, CASL, XML, Smalltalk, Modal Prolog) with different mappings for different non-functional requirements.
- **Quote:** "given a conceptual model representing a domain ontology in OntoUML, we can have different mappings to different codification languages (e.g., OWL DL, RDFS, F-Logic, Haskell, Relational Database languages, CASL, among many others). The choice of each of these languages should be made to favor a specific set of non-functional requirements."
- **Context:** Section 4 part (v) on Ontology Codification.

### Pattern: UFO Four-Category Ontology vs Other Approaches
- **Source:** 23-UFO_Story_Ontological_Foundations (Chunk 1:126-136)
- **Description:** UFO is based on a Four-Category Ontology (individuals, universals, substantial individuals/universals, accidents) which was needed to make sense of language, cognition, and conceptual modeling practices like reified relationships and weak entities.
- **Quote:** "It was clear to us from the outset that we needed an ontological theory that would countenance both individuals and universals and one that would include not only substantial individuals and universals but also accidents (particularized properties, moments, qualities, modes, tropes, abstract particulars, aspects, ways) and accident universals. In other words, we needed a Four-Category Ontology (Lowe, 2006)."
- **Context:** Section 2 on the theoretical foundations of UFO.

### Pattern: UFO-A, UFO-B, UFO-C Layer Structure
- **Source:** 23-UFO_Story_Ontological_Foundations (Chunk 1:173-193)
- **Description:** UFO is organized in three strata: UFO-A (Ontology of Endurants for structural modeling), UFO-B (Ontology of Perdurants for events/processes), and UFO-C (Ontology of Intentional and Social Entities built on UFO-A and UFO-B).
- **Quote:** "UFO-A: An Ontology of Endurants dealing with aspects of structural conceptual modeling... UFO-B: An Ontology of Perdurants (Events, Processes) dealing with aspects such as Perdurant Mereology, Temporal Ordering of Perdurants, Object Participation in Perdurants, Causation, Change... UFO-C: An Ontology of Intentional and Social Entities, which is constructed on top of UFO-A and UFO-B."
- **Context:** Section 3 on The unified foundational ontology and its applications.

---

## Paper: 31-BBO_BPMN_Ontology

### Pattern: BBO vs BPMN 2.0 Meta-model
- **Source:** 31-BBO_BPMN_Ontology (Chunk 1:89-91)
- **Description:** BBO is based on a fragment extracted from the BPMN 2.0 meta-model, exploiting its process-execution specifications but extending it with additional taxonomies, concepts, relations and attributes.
- **Quote:** "The core of BBO is an ontological representation of a fragment extracted from the BPMN 2.0 meta-model. Hence, we exploited the process-execution specifications of BPMN 2.0. In addition, we have extended the core of BBO with taxonomies, concepts, relations and attributes to meet the specifications presented in Section 3."
- **Context:** Section 1 Introduction.

### Pattern: BBO vs EPC (Event Process Driven Chain)
- **Source:** 31-BBO_BPMN_Ontology (Chunk 1:113-114)
- **Description:** BPMN offers a finer-grained representation than EPC and includes execution logic for its elements.
- **Quote:** "Event Process driven Chain (EPC) (Scheer et al., 2005) and BPMN are the most known BP meta-models (and graphical languages). However, BPMN offers a finer grained representation than EPC and an execution logic for its elements."
- **Context:** Section 2 Related work.

### Pattern: BBO vs General vs Domain-Specific BP Ontologies
- **Source:** 31-BBO_BPMN_Ontology (Chunk 1:115-121)
- **Description:** Existing BP ontologies are either too general or domain-specific (software project management, software processes, industrial maintenance, manufacturing). BBO aims to be generic yet fine-grained.
- **Quote:** "BP ontologies have often overlapping fragments and are either very general (Uschold et al., 1998; Van Grondelle and Gulpers, 2011; Abdalla et al., 2014), or specific to a given type of processes: (Ruiz et al., 2004) propose an ontology for software project management; (Falbo and Bertollo, 2009) also present a software process ontology; (Karray, Chebel-Morello and Zerhouni, 2012) describe an ontology for industrial maintenance processes; (Chungoora et al., 2013) report an ontology for the manufacturing process."
- **Context:** Section 2 Related work.

### Pattern: BBO vs Previous BPMN Ontology Attempts
- **Source:** 31-BBO_BPMN_Ontology (Chunk 1:122-134)
- **Description:** Previous attempts to convert BPMN to ontology include BPMN 1.0 transformation by Rospocher et al., BPMN 2.0 ontology by Natschlager (not available), and BPMN-onto (automatically extracted, no documentation). BBO differs by extracting only process description fragments and extending them.
- **Quote:** "The idea of converting BPMN into an ontological model has been investigated in two previous works. In (Rospocher, Ghidini and Serafini, 2014), BPMN 1.0 is transformed into an ontology that has been manually revised and enriched with annotations and axioms... Natschlager (2011) has proposed an ontological version of BPMN 2.0. However, to the best of our knowledge, this ontology is not available for the community. Another ontology (BPMN-onto, 2019) has been automatically extracted from BPMN 2.0, but we were not able to find any documentation about how it was generated."
- **Context:** Section 2 Related work.

### Pattern: BPMN Limitations for Resource Representation
- **Source:** 31-BBO_BPMN_Ontology (Chunk 1:83-88)
- **Description:** Despite industrial maturity, BPMN does not support representation of some process specifications like material resources required for tasks or workstation locations. BBO addresses these limitations.
- **Quote:** "In spite of its industrial maturity, BPMN does not support the representation of some process specifications such as the material resources required to carry out a given task, or the workstation where a given task should be performed. These specifications are essential for a complete description of BPs."
- **Context:** Section 1 Introduction.

### Pattern: BBO Resource Taxonomy vs BPMN Resource Concept
- **Source:** 31-BBO_BPMN_Ontology (Chunk 1:291-303)
- **Description:** The BPMN Resource concept has ambiguous semantics, sometimes meaning all resource types and sometimes limited to agents. BBO adopts the broader definition and creates a resource taxonomy inspired by Falbo/Bertollo and Karray et al.
- **Quote:** "The Resource concept exists in the BPMN meta-model. However, its semantics and definition are ambiguous. Indeed, on p. 95 of BPMN specification, the Resource class is supposed to cover all resource types. However, the definition of the relation that assigns resources to a process (p. 148) or an activity (p.152), limits the set of resources to the agents responsible for performing the work... In BBO, like in (Karray et al., 2012), we adopt the first definition of Resource, that englobes all resource types."
- **Context:** Section 4.2 on Input/output specifications.

### Pattern: BBO Manufacturing Facility Taxonomy Reuse
- **Source:** 31-BBO_BPMN_Ontology (Chunk 1:309-313)
- **Description:** BBO reuses manufacturing facility taxonomies from Chungoora et al. and Fraga et al. for representing where tasks should be performed (Station, Cell, Shop, Factory).
- **Quote:** "To specify where the task should be performed, we reused the taxonomies introduced in (Chungoora et al., 2013) and (Fraga, Vegetti and Leone, 2018) and obtained the part of the ontology shown in Figure 5. A workstation, Station, is where a particular job is performed. Cell is the place that groups a set of related operations in the production flow, while Shop is the area where production is carried out, and Factory is the place where those production areas are located."
- **Context:** Section 4.3 on Manufacturing facility.

### Pattern: BBO Agent Sub-Ontology Reuse
- **Source:** 31-BBO_BPMN_Ontology (Chunk 1:340-341)
- **Description:** BBO reuses the Agent sub-ontology from Ruiz et al. 2004 for representing human and software resources with job and role distinctions.
- **Quote:** "We reused the Agent sub-ontology proposed in (Ruiz et al., 2004), and presented in Figure 7."
- **Context:** Section 4.5 on Agent.

### Pattern: BBO UO Ontology Reuse for Units of Measure
- **Source:** 31-BBO_BPMN_Ontology (Chunk 1:288-289)
- **Description:** BBO uses the Unit and Prefix concepts from the UO (Unit of Measure) ontology for specifying parameter values.
- **Quote:** "The UnitOfMeasure class is specified using the two concepts Unit and Prefix of the unit measures ontology UO (UO-onto, 2019)."
- **Context:** Section 4.2 on Input/output specifications.

### Pattern: BBO vs BPMN Natural Language Specifications
- **Source:** 31-BBO_BPMN_Ontology (Chunk 1:398-403)
- **Description:** BPMN 2.0 UML diagrams and XML schema do not reflect the whole specification. BBO manually conceptualizes natural language specifications and formalizes them in OWL.
- **Quote:** "BPMN 2.0 specification provides a meta-model for BPMN elements as a UML class diagram and in the form of an XML schema. However, the diagrams and XML schema do not reflect the whole specification and miss a part of its semantics (Dijkman, Dumas and Ouyang, 2008; Wong and Gibbons, 2008). Consequently, even a formal translation of the UML and XML specifications would not enable checking the consistency of represented processes, because a large part of the specifications is in natural language."
- **Context:** Section 5.2 on Formalizing BPMN natural language specifications in OWL.

### Pattern: BBO Implementation in OWL 2 DL
- **Source:** 31-BBO_BPMN_Ontology (Chunk 1:359-363)
- **Description:** BBO is formalized and implemented in OWL 2 DL using Protege, with conversion rules to generate OWL from UML diagrams.
- **Quote:** "We have formalized and implemented the conceptual model of BBO in OWL 2 DL using Protege. First, we designed and applied a set of conversion rules that automatically generated an OWL representation from the UML diagrams of BBO. Second, we manually turned various natural language specifications in the BPMN document into a formal OWL representation."
- **Context:** Section 5 on Formalization and Implementation.

---

## Summary of Framework Comparisons

| Paper | Main Comparisons |
|-------|------------------|
| 09-OCEL_20_Specification | OCEL 2.0 vs XES, OCEL 1.0, traditional process notations (BPMN, DFG, UML) |
| 10-OC-PM_Object-Centric_Process_Mining | OCPM vs artifact-centric, OCBC, colored Petri nets, graph databases, ontology-based extraction |
| 11-Process_Mining_Event_Knowledge_Graphs | Event knowledge graphs vs classical event logs, OCEL, XOC, RDF, labeled property graphs |
| 12-Foundations_of_Process_Event_Data | XES vs BPMN lifecycle, OCEL, ODBA/Onprom, PM2 vs CRISP-DM |
| 23-UFO_Story_Ontological_Foundations | UFO vs BWW, DOLCE, GFO; OntoUML vs UML 2.0, ORM 2.0; UFO applications to TOGAF, ArchiMate, BPMN |
| 31-BBO_BPMN_Ontology | BBO vs BPMN 2.0, EPC, general/domain-specific BP ontologies, previous BPMN ontology attempts |
