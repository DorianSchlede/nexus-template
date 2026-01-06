<!-- Source: 02-Knowledge_Graphs.pdf | Chunk 2/15 -->


(Arica _,_ bus* _,_ ?city) evaluated against the graph of Figure 1 may match the paths in Figure 9. In

fact, since a cycle is present, an infinite number of paths are potentially matched. For this reason,

restricted semantics are often applied, returning only the shortest paths, or paths without repeated

nodes or edges (as in the case of Cypher). [7] Rather than returning paths, another option is to instead

return the (finite) set of pairs of nodes connected by a matching path (as in the case of SPARQL 1.1).

Regular path queries can then be used in graph patterns to express _navigational graph pat-_

_terns_ [16], as shown in Figure 10, which illustrates a query searching for food festivals in cities

reachable (recursively) from Arica by bus or flight. Furthermore, when regular path queries and

graph patterns are combined with operators such as projection, selection, union, difference, and

optional, the result is known as _complex navigational graph patterns_ [16]. Appendix B.2.3 provides

definitions for (complex) navigational graph patterns and their evaluation.


6Some authors distinguish _2-way regular path queries_ from regular path queries, where only the former supports inverses.

7Mapping variables to paths requires special treatment [16]. Cypher [165] returns a string that encodes a path, upon which

certain functions such as length(·) can be applied. G-CORE [15], on the other hand, allows for returning paths, and

supports additional operators on them, including projecting them as graphs, applying cost functions, and more besides.


11


**?event** **?name** **?city**


EID15 Ñam Santiago

EID16 Food Truck Arica

EID16 Food Truck Viña del Mar







Fig. 10. Navigational graph pattern (left) with mappings generated over the graph of Figure 1 (right)


_2.2.4_ _Other features._ Thus far we have discussed features that form the practical and theoretical

foundation of any query language for graphs [16]. However, specific query languages for graphs

may support other practical features, such as aggregation (GROUP BY, COUNT, etc.), more complex

filters and datatype operators (e.g., range queries on years extracted from a date), federation for

querying remotely hosted graphs over the Web, languages for updating graphs, support for semantic

entailment regimes, etc. For more information, we refer to the documentation of the respective

query languages (e.g., [15, 217]) and to the survey by Angles et al. [16].


**3** **SCHEMA, IDENTITY, CONTEXT**

In this section we describe various enhancements and extensions of the data graph – relating to

schema, identity and context – that provide additional structures for accumulating knowledge.

Henceforth, we refer to a _data graph_ as a collection of data represented as nodes and edges using

one of the models discussed in Section 2. We refer to a _knowledge graph_ as a data graph potentially

enhanced with representations of schema, identity, context, ontologies and/or rules. These additional

representations may be embedded in the data graph, or layered above it. Representations for schema,

identity and context are discussed herein, while ontologies and rules will be discussed in Section 4.


**3.1** **Schema**


One of the benefits of modelling data as graphs – versus, for example, the relational model – is the

option to forgo or postpone the definition of a schema. However, when modelling data as graphs,

schemata _can_ be used to prescribe a high-level structure and/or semantics that the graph follows or

should follow. We discuss three types of graph schemata: _semantic_, _validating_, and _emergent_ .


_3.1.1_ _Semantic schema._ A semantic schema allows for defining the meaning of high-level terms

(aka _vocabulary_ or _terminology_ ) used in the graph, which facilitates reasoning over graphs using

those terms. Looking at Figure 1, for example, we may notice some natural groupings of nodes

based on the types of entities to which they refer. We may thus decide to define _classes_ to denote

these groupings, such as Event, City, etc. In fact, Figure 1 already illustrates three low-level classes

- Open Market, Food Market, Drinks Festival – grouping similar entities with an edge labelled

type. We may subsequently observe some natural relations between some of these classes that

we would like to capture. In Figure 11, we present a class hierarchy for events where children are

defined to be _subclasses_ of their parents such that if we find an edge [EID15] type Food Festival in
our graph, we may also _infer_ that [EID15] type Festival and [EID15] type Event .

Aside from classes, we may also wish to define the semantics of edge labels, aka _properties_ .

Returning to Figure 1, we may consider that the properties city and venue are _sub-properties_ of a
more general property location, such that given an edge [Santa Lucía] city Santiago, for example,
we may also infer that [Santa Lucía] location Santiago . We may also consider, for example, that bus and
flight are both sub-properties of a more general property connects to. As such, properties may

also form a hierarchy. We may further define the _domain_ of properties, indicating the class(es) of

entities for nodes from which edges with that property extend; for example, we may define that


12


Festival


Food Festival Drinks Festival Music Festival . . .



Event


Periodic Market . . .


Open Market Closed Market



Fig. 11. Example class hierarchy for Event


Table 2. Definitions for sub-class, sub-property, domain and range features in semantic schemata


**Feature** **Definition** **Condition** **Example**

Subclass _𝑐_ subc. of _𝑑_ _𝑥_ type _𝑐_ implies _[𝑥]_ type _𝑑_ City subc. of Place

Subproperty _𝑝_ subp. of _𝑞_ _𝑥_ _𝑝_ _𝑦_ implies _[𝑥]_ _𝑞_ _𝑦_ venue subp. of location

Domain _𝑝_ domain _𝑐_ _𝑥_ _𝑝_ _𝑦_ implies _[𝑥]_ type _𝑐_ venue domain Event

Range _𝑝_ range _𝑐_ _𝑥_ _𝑝_ _𝑦_ implies _[𝑦]_ type _𝑐_ venue range Venue


the domain of connects to is a class Place, such that given the previous sub-property relations,
we could conclude that [Arica] type Place . Conversely, we may define the _range_ of properties,

indicating the class(es) of entities for nodes to which edges with that property extend; for example,

we may define that the range of city is a class City, inferring that [Arica] type City .

A prominent standard for defining a semantic schema for (RDF) graphs is the _RDF Schema_ ( _RDFS_ )

standard [70], which allows for defining subclasses, subproperties, domains, and ranges amongst

the classes and properties used in an RDF graph, where such definitions can be serialised as a

graph. We illustrate the semantics of these features in Table 2 and provide a concrete example of

definitions in Figure 12 for a sample of terms used in the running example. These definitions can

then be embedded into a data graph. More generally, the semantics of terms used in a graph can be

defined in much more depth than seen here, as is supported by the _Web Ontology Language_ ( _OWL_ )

standard [239] for RDF graphs. We will return to such semantics later in Section 4.

Semantic schema are typically defined for incomplete graph data, where the absence of an edge

between two nodes, such as [Viña del Mar] flight Arica, does not mean that the relation does not

hold in the real world. Therefore, from the graph of Figure 1, we cannot assume that there is no

flight between Viña del Mar and Arica. In contrast, if the _Closed World Assumption_ ( _CWA_ ) were

adopted – as is the case in many classical database systems – it would be assumed that the data

graph is a complete description of the world, thus allowing to assert with certainty that no flight

exists between the two cities. Systems that do not adopt the CWA are said to adopt the _Open World_

_Assumption_ ( _OWA_ ). A consequence of CWA is that the addition of an edge to the data graph may

contradict what was previously assumed to be false (due to missing information), whereas with

OWA, a statement that is proven false continues to be false with the addition of more edges.

Considering our running example, it would be unreasonable to assume that the tourism organi
sation has complete knowledge of everything describable in its knowledge graph. However, it is

inconvenient if a system is unable to definitely answer “ _yes_ ” or “ _no_ ” to questions such as “ _is there_

_a flight between Arica and Viña del Mar?_ ”, especially when the organisation is certain that it has

complete knowledge of the flights. A compromise between OWA and CWA is the _Local Closed_

_World Assumption_ ( _LCWA_ ), where portions of the data graph are assumed to be complete.


13


Fig. 12. Example schema graph describing sub-classes, sub-properties, domains, and ranges


_3.1.2_ _Validating schema._ When graphs are used to represent diverse, incomplete data at large-scale,

the OWA is the most appropriate choice for a _default_ semantics. But in some scenarios, we may

wish to guarantee that our data graph – or specific parts thereof – are in some sense “complete”.

Returning to Figure 1, for example, we may wish to ensure that all events have at least a name, a

venue, a start date, and an end date, such that applications using the data – e.g., one that sends event

notifications to users – can ensure that they have the minimal information required. Furthermore,

we may wish to ensure that the city of an event is _stated to be_ a city (rather than _inferring_ that it is

a city). We can define such constraints in a validating schema and validate the data graph with

respect to the resulting schema, listing constraint violations (if any). Thus while semantic schemata

allow for inferring new graph data, validating schemata allow for validating existing graph data.

A standard way to define a validating schema for graphs is using _shapes_ [296, 306, 423]. A shape

_targets_ a set of nodes in a data graph and specifies _constraints_ on those nodes. The shape’s target

can be defined in many ways, such as targetting all instances of a class, the domain or range of a

property, the result of a query, nodes connected to the target of another shape by a given property,

etc. Constraints can then be defined on the targetted nodes, such as to restrict the number or types

of values taken on a given property. A _shapes graph_ is formed from a set of interrelated shapes.

Shapes graphs can be depicted as UML-like class diagrams, where Figure 13 illustrates an example

of a shapes graph based on Figure 1, defining constraints on four interrelated shapes. Each shape –

denoted with a box like Place, Event, etc. – is associated with a set of constraints. Nodes conform

to a shape if and only if they satisfy all constraints defined on the shape. Inside each shape box

are placed constraints on the number (e.g., [1..*] denotes one-to-many, [1..1] denotes precisely
one, etc.) and types (e.g., string, dateTime, etc.) of nodes that conforming nodes can relate to with
a property (e.g., name, start, etc.). Another option is to place constraints on the number of nodes

conforming to a particular shape that the conforming node can relate to with a property (thus

generating edges between shapes); for example, Event 1..* Venue denotes that conforming

|Col1|venue|
|---|---|
|Event|venue|
|Event||


nodes for Event must relate to at least one node with the property venue that conforms to the

Venue shape. Shapes can inherit the constraints of parent shapes – denoted with an △ connector –

as in the case of City and Venue, whose conforming nodes must also conform to the Place shape.

Given a shape and a targetted node, it is possible to check if the node conforms to that shape

or not, which may require checking conformance of other nodes; for example, the node [EID15]

conforms to the Event shape not only based on its local properties, but also based on conformance

of [Santa Lucía] to Venue and [Santiago] to City . Conformance dependencies may also be recursive,

where the conformance of [Santiago] to City requires that it conforms to Place, which requires that


Viña del Mar and Arica conform to Place, and so on. Conversely, EID16 does not conform to Event, as

|Col1|City|
|---|---|
|Place|Place|

it does not have the start and end properties required by the example shapes graph.

When declaring shapes, the data modeller may not know in advance the entire set of prop
erties that some nodes can have. An _open shape_ allows the node to have additional proper
ties not specified by the shape, while a _closed shape_ does not. For example, if we add the edge


14


|Place<br>flight 0..* lat: float[0..1] 0..* bus<br>long: float[0..1]<br>Event<br>name: string[1..∗] venue Venue city City<br>start: dateTime[1..1]<br>1..* indoor: boolean[0..1] 0..1 population: int ∧ >5000 [0..1]<br>end: dateTime[1..1]<br>type: any[1..∗]|Col2|Col3|
|---|---|---|
|Event|Event|Event|
|name: string[1_.._∗]<br>start: dateTime[1_.._1]<br>end:<br>dateTime[1_.._1]<br>type: any[1_.._∗]|name: string[1_.._∗]<br>start: dateTime[1_.._1]<br>end:<br>dateTime[1_.._1]<br>type: any[1_.._∗]|City|
|name: string[1_.._∗]<br>start: dateTime[1_.._1]<br>end:<br>dateTime[1_.._1]<br>type: any[1_.._∗]|1..*<br>0..1<br>indoor: boolean[0_.._1]<br>population: int ∧>5000 [0_.._1]|population: int ∧>5000 [0_.._1]|



Fig. 13. Example shapes graph depicted as a UML-like diagram

Santiago founder Pedro de Valdivia to the graph represented in Figure 1, then [Santiago] only conforms to
the City shape if that shape is defined as open (since the shape does not mention founder).

Practical languages for shapes often support additional boolean features, such as conjunction

( _and_ ), disjunction ( _or_ ), and negation ( _not_ ) of shapes; for example, we may say that all the values

of venue should conform to the shape Venue _and_ ( _not_ City), making explicit that venues in the data

graph should not be directly given as cities. However, shapes languages that freely combine recur
sion and negation may lead to semantic problems, depending on how their semantics are defined.

To illustrate, consider the following case inspired by the barber paradox [306], involving a shape


Barber whose conforming nodes shave at least one node conforming to Person _and_ ( _not_ Barber) .
Now, given (only) [Bob] shave Bob with [Bob] conforming to Person, does [Bob] conform to Barber ? If

|to Person and (not Barber)<br>Bob conform to Barber ? If|Person and (not Barber)|Col3|Col4|
|---|---|---|---|
|to Person_ and_ (_not_ Barber) <br> Bob conform to Barber ? If|Person_ and_ (_not_ Barber)|Barber|? If|



_yes_ - if [Bob] conforms to Barber – then [Bob] violates the constraint by not shaving at least one node

conforming to Person _and_ ( _not_ Barber) . If _no_ - if [Bob] does not conform to Barber – then [Bob] satisfies

the Barber constraint by shaving such a node. Semantics to avoid such paradoxical situations have

been proposed based on stratification [61], partial assignments [104], and stable models [177].

Although validating schemata and semantic schemata serve different purposes, they can comple
ment each other. In particular, a validating schema can take into consideration a semantic schema,

such that, for example, validation is applied on the data graph including inferences. Taking the class

hierarchy of Figure 11 and the shapes graph of Figure 13, for example, we may define the target of

the Event shape as the nodes that are of type Event (the class). If we first apply inferencing with

respect to the class hierarchy of the semantic schema, the Event shape would now target [EID15] and


EID16 . The presence of a semantic schema may, however, require adapting the validating schema.

Taking into account, for example, the aforementioned class hierarchy would require defining a

relaxed cardinality on the type property. Open shapes may also be preferred in such cases rather

than enumerating constraints on all possible properties that may be inferred on a node.

We provide high-level definitions for shapes and related concepts in Appendix B.3.2. Two shapes

languages have recently emerged for RDF graphs: _Shape Expressions_ ( _ShEx_ ), published as a W3C

Community Group Report [423]; and _SHACL_ ( _Shapes Constraint Language_ ), published as a W3C

Recommendation [296]. These languages support the discussed features (and more) and have been

adopted for validating graphs in a number of domains relating to health-care [521], scientific

literature [216], spatial data [83], amongst others. More details about ShEx and SHACL can be

found in the book by Labra Gayo et al. [306]. A recently proposed language that can be used as a

common basis for both ShEx and SHACL reveals their similarities and differences [305]. A similar

notion of schema has been proposed by Angles [14] for property graphs.


15


Fig. 14. Example quotient graph simulating the data graph in Figure 1





























Fig. 15. Example quotient graph bisimilar with the data graph in Figure 1


_3.1.3_ _Emergent schema._ Both semantic and validating schemata require a domain expert to explic
itly specify definitions and constraints. However, a data graph will often exhibit latent structures

that can be automatically extracted as an _emergent schema_ [413] (aka _graph summary_ [84, 322, 492]).

A framework often used for defining emergent schema is that of _quotient graphs_, which partition

groups of nodes in the data graph according to some equivalence relation while preserving some

structural properties of the graph. Taking Figure 1, we can intuitively distinguish different _types_

of nodes based on their context, such as event nodes, which link to venue nodes, which in turn

link to city nodes, and so forth. In order to describe the structure of the graph, we could consider

six partitions of nodes: _event_, _name_, _venue_, _class_, _date-time_, _city_ . In practice, these partitions may

be computed based on the class or shape of the node. Merging the nodes of each partition into

one node while preserving edges leads to the quotient graph shown in Figure 14: the nodes of this

quotient graph are the partitions of nodes from the data graph and the edge _[𝑋]_ _𝑦_ _𝑍_ is in the

quotient graph if and only if there exists _𝑥_ ∈ _𝑋_ and _𝑧_ ∈ _𝑍_ such that _[𝑥]_ _𝑦_ _𝑧_ is in the data graph.

There are many ways in which quotient graphs may be defined, depending not only on how nodes

are partitioned, but also how the edges are defined. Different quotient graphs may provide different

guarantees with respect to the structure they preserve. Formally, we can say that every quotient

graph _simulates_ its input graph (based on the _simulation relation_ of set membership between data

nodes and quotient nodes), meaning that for all _𝑥_ ∈ _𝑋_ with _𝑥_ an input node and _𝑋_ a quotient node,

if _[𝑥]_ _𝑦_ _𝑧_ is an edge in the data graph, then there must exist an edge _[𝑋]_ _𝑦_ _𝑍_ in the quotient

graph such that _𝑧_ ∈ _𝑍_ ; for example, the quotient graph of Figure 14 simulates the data graph of

Figure 1. However, this quotient graph seems to suggest (for instance) that [EID16] would have a

start and end date in the data graph when this is not the case. A stronger notion of structural

preservation is given by _bisimilarity_, which in this case would further require that if _[𝑋]_ _𝑦_ _𝑍_ is

an edge in the quotient graph, then for all _𝑥_ ∈ _𝑋_, there must exist a _𝑧_ ∈ _𝑍_ such that _[𝑥]_ _𝑦_ _𝑧_ is in

the data graph; this is not satisfied by [EID16] in the quotient graph of Figure 14, which does not have


16


an outgoing edge labelled start or end in the original data graph. Figure 15 illustrates a bisimilar

version of the quotient graph, splitting the _event_ partition into two nodes reflecting their different

outgoing edges. An interesting property of bisimilarity is that it preserves forward-directed paths:

given a path expression _𝑟_ without inverses and two bisimilar graphs, _𝑟_ will match a path in one

graph if and only if it matches a corresponding path in the other bisimilar graph. One can verify,

for example, that a path matches _[𝑥]_ city·(flight|bus)* _𝑧_ in Figure 1 if and only if there is a path
matching _[𝑋]_ city·(flight|bus)* _𝑍_ in Figure 15 such that _𝑥_ ∈ _𝑋_ and _𝑧_ ∈ _𝑍_ .

There are many ways in which quotient graphs may be defined, depending on the equivalence

relation that partitions nodes. Furthermore, there are many ways in which other similar or bisimilar

graphs can be defined, depending on the (bi)simulation relation that preserves the data graph’s

structure [84]. We provide formal definitions for the notions of _quotient graphs_, _simulation_ and

_bisimulation_ in Appendix B.3.3. Such techniques aim to _summarise_ the data graph into a higher-level

topology. In order to reduce the memory overhead of the quotient graph, in practice, nodes may

rather be labelled with the cardinality of the partition and/or a high-level label (e.g., _event_, _city_ ) for

the partition rather than storing the labels of all nodes in the partition.

Various other forms of emergent schema not based on a quotient graph framework have also been

proposed; examples include emergent schemata based on relational tables [413], formal concept

analysis [196], and so forth. Emergent schemata may be used to provide a human-understandable

overview of the data graph, to aid with the definition of a semantic or validating schema, to optimise

the indexing and querying of the graph, to guide the integration of data graphs, and so forth. We

refer to the survey by Čebirić et al. [84] for further details.


**3.2** **Identity**


In Figure 1, we use nodes like [Santiago], but to which Santiago does this node refer? Do we refer to

Santiago de Chile, Santiago de Cuba, Santiago de Compostela, or do we perhaps refer to the indie

rock band Santiago? Based on edges such as [Santa Lucía] city Santiago, we may deduce that it is

one of the three cities mentioned (not the rock band), and based on the fact that the graph describes

tourist attractions in Chile, we may further deduce that it refers to Santiago de Chile. Without

further details, however, _disambiguating_ nodes of this form may rely on heuristics prone to error

in more difficult cases. To help avoid such ambiguity, first we may use globally-unique identifiers

to avoid naming clashes when the knowledge graph is extended with external data, and second we

may add external identity links to disambiguate a node with respect to an external source.


_3.2.1_ _Persistent identifiers._ Assume we wished to compare tourism in Chile and Cuba, and we have

acquired an appropriate knowledge graph for Cuba. Part of the benefit of using graphs to model

data is that we can merge two graphs by taking their union. However, as shown in Figure 16, using

an ambiguous node like [Santiago] may result in a _naming clash_ : the node is referring to two different

real-world cities in both graphs, where the merged graph indicates that Santiago is a city in both

Chile and Cuba (rather than two different cities). [8] To avoid such clashes, long-lasting _persistent_

_identifiers_ ( _PIDs_ ) [213] can be created in order to uniquely identify an entity. Prominent examples of

PID schemes include _Digital Object Identifiers_ ( _DOIs_ ) for papers, _ORCID iDs_ for authors, _International_

_Standard Book Numbers_ ( _ISBNs_ ) for books, _Alpha-2 codes_ for counties, and more besides.

In the context of the Semantic Web, the RDF data model goes one step further and recommends

that global Web identifiers be used for nodes and edge labels. However, rather than adopt the

_Uniform Resource Locators (URLs)_ used to identify the location of _information resources_ such as


8Such a naming clash is not unique to graphs, but could also occur if merging tables, trees, etc.


17


Fig. 16. Result of merging two graphs with ambiguous local identifiers


webpages, RDF 1.1 proposes to use _Internationalised Resource Identifiers (IRIs)_ to identify _non-_

_information resources_ such as cities or events. [9] Hence, for example, in the RDF representation of the

Wikidata [543] – a knowledge graph proposed to complement Wikipedia, discussed in more detail in

Section 10 – while the URL [[https://www.wikidata.org/wiki/Q2887]](https://www.wikidata.org/wiki/Q2887) refers to a webpage that can be loaded in a

browser providing human-readable meta-data about Santiago, the IRI [[http://www.wikidata.org/entity/Q2887]](http://www.wikidata.org/entity/Q2887)

refers to the city itself. Distinguishing the identifiers for both resources (the webpage and the city

itself) avoids naming clashes; for example, if we use the URL to identify both the webpage and the

city, we may end up with an edge in our graph, such as (with readable labels below the edge):


[http://www.wikidata.org/wiki/Q2887](http://www.wikidata.org/wiki/Q2887) [http://www.wikidata.org/wiki/Property:P112](http://www.wikidata.org/wiki/Property:P112) [https://www.wikidata.org/wiki/Q203534](https://www.wikidata.org/wiki/Q203534)


[Santiago (URL)] [founded by (URL)] [Pedro de Valdivia (URL)]


Such an edge leaves ambiguity: was Pedro de Valdivia the founder of the webpage, or the city?

Using IRIs for entities distinct from the URLs for the webpages that describe them avoids such

ambiguous cases, where Wikidata thus rather defines the previous edge as follows:


[http://www.wikidata.org/entity/Q2887](http://www.wikidata.org/entity/Q2887) [http://www.wikidata.org/prop/direct/P112](http://www.wikidata.org/prop/direct/P112) [http://www.wikidata.org/entity/Q203534](http://www.wikidata.org/entity/Q203534)


[Santiago (IRI)] [founded by (IRI)] [Pedro de Valdivia (IRI)]


using IRIs for the city, person, and founder of, distinct from the webpages describing them. These

[Wikidata identifiers use the prefix http://www.wikidata.org/entity/ for entities and the prefix](http://www.wikidata.org/entity/)

[http://www.wikidata.org/prop/direct/ for relations. Such prefixes are known as](http://www.wikidata.org/prop/direct/) _namespaces_, and

are often abbreviated with prefix strings, such as wd: or wdt:, where the latter triple can then be
written more concisely using such abbreviations as [wd:Q2887] wdt:P112 wd:Q203534 .

If HTTP IRIs are used to identify the graph’s entities, when the IRI is looked up (via HTTP),

the web-server can return (or redirect to) a description of that entity in formats such as RDF. This

further enables RDF graphs to link to related entities described in external RDF graphs over the Web,

giving rise to _Linked Data_ [41, 226] (discussed in Section 9). Though HTTP IRIs offer a flexible and

powerful mechanism for issuing global identifiers on the Web, they are not necessarily persistent:

websites may go offline, the resources described at a given location may change, etc. In order to

enhance the persistence of such identifiers, _Persistent URL_ ( _PURL_ ) services offer redirects from

a central server to a particular location, where the PURL can be redirected to a new location if

necessary, changing the address of a document without changing its identifier. The persistence of

HTTP IRIs can then be improved by using namespaces defined through PURL services.


9Uniform Resource Identifiers (URIs) can be Uniform Resource Locators (URLs), used to locate information resources, and

Uniform Resource Names (URNs), used to name non-information resources. Internationalised Resource Identifiers (IRIs) are

URIs that allow Unicode. For example, http://example.com/Ñam is an IRI, but not a URI, due to the use of “Ñ”. Percentage

encoding – http://example.com/%C3%91am – can encode an IRI as a URI (but reduces readability).


18


_3.2.2_ _External identity links._ Assume that the tourist board opts to define the chile: namespace
with an IRI such as http://turismo.cl/entity/ on a web-server that they control, allowing

nodes such as [chile:Santiago] - a shortcut for the IRI [http://turismo.cl/entity/Santiago] - to be looked up over

the Web. While using such a naming scheme helps to avoid naming clashes, the use of IRIs does not

necessarily help ground the identity of a resource. For example, an external geographic knowledge

graph may assign the same city the IRI [geo:SantiagoDeChile] in their own namespace, where we have no

direct way of knowing that the two identifiers refer to the same city. If we merge the two knowledge

graphs, we will end up with two distinct nodes for the same city.

There are a number of ways to ground the identity of an entity. The first is to associate the entity

with uniquely-identifying information in the graph, such as its geo-coordinates, its postal code, the

year it was founded, etc. Each additional piece of information removes ambiguity as to which city

is being referred, providing (for example) more options for matching the city with its analogue in

external sources. A second option is to use _identity links_ to state that a local entity has the same

identity as another _coreferent_ entity found in an external source; an instantiation of this concept

can be found in the OWL standard, which defines the owl:sameAs property relating coreferent
entities. Using this property, we could state the edge [chile:Santiago] owl:sameAs geo:SantiagoDeChile in

our RDF graph, thus establishing an identity link between the corresponding nodes in both graphs.

The semantics of owl:sameAs defined by the OWL standard then allow us to combine the data for

both nodes. Such semantics will be discussed later in Section 4. Ways in which identity links can

be computed will also be discussed later in Section 8.


_3.2.3_ _Datatypes._ Consider the two date-times on the left of Figure 1: how should we assign these

nodes persistent/global identifiers? Intuitively it would not make sense, for example, to assign IRIs

to these nodes since their syntactic form tells us what they refer to: specific dates and times in

March 2020. This syntactic form is further recognisable by machine, meaning that with appropriate

software, we could order such values in ascending or descending order, extract the year, etc.

Most practical data models for graphs allow for defining nodes that are datatype values. RDF

utilises _XML Schema Datatypes_ ( _XSD_ ) [411], amongst others, where a datatype node is given as a

pair ( _𝑙,𝑑_ ) where _𝑙_ is a lexical string, such as "2020-03-29T20:00:00", and _𝑑_ is an IRI denoting the
datatype, such as xsd:dateTime. The node is then denoted ["][2020-03-29T20:00:00]["^^xsd:dateTime] . Datatype

nodes in RDF are called _literals_ and are not allowed to have outgoing edges. Other datatypes

commonly used in RDF data include xsd:string, xsd:integer, xsd:decimal, xsd:boolean, etc.
In case that the datatype is omitted, the value is assumed to be of type xsd:string. Applications

built on top of RDF can then recognise these datatypes, parse them into datatype objects, and apply

equality checks, normalisation, ordering, transformations, casting, according to their standard

definition. In the context of property graphs, Neo4j [354] also defines a set of internal datatypes on

property values that includes numbers, strings, booleans, spatial points, and temporal values.


_3.2.4_ _Lexicalisation._ Global identifiers for entities will sometimes have a human-interpretable
form, such as [chile:Santiago], but the identifier strings themselves do not carry any formal semantic

significance. In other cases, the identifiers used may not be human-interpretable by design. In

Wikidata, for instance, Santiago de Chile is identified as [wd:Q2887], where such a scheme has the

advantage of providing better persistence and of not being biased to a particular human language.

For example, the Wikidata identifier for Eswatini ( [wd:Q1050] ) was not affected when the country

changed its name from Swaziland, and does not necessitate choosing between languages for creating

(more readable) IRIs such as [wd:Eswatini] (English), [wd:eSwatini] (Swazi), [wd:Esuatini] (Spanish), etc.

Since identifiers can be arbitrary, it is common to add edges that provide a human-interpretable

label for nodes, such as [wd:Q2887] rdfs:label “Santiago”, indicating how people may refer to the subject

node linguistically. Linguistic information of this form plays an important role in grounding


19


Fig. 17. RDF list representing the three largest peaks of Chile, in order


knowledge such that users can more clearly identify which real-world entity a particular node in a

knowledge graph actually references [120]; it further permits cross-referencing entity labels with

text corpora to find, for example, documents that potentially speak of a given entity [338]. Labels


specific graph model, such literal nodes may also be defined as a pair ( _𝑠,𝑙_ ), where _𝑠_ denotes
the string and _𝑙_ a language code; in RDF, for example we may state [chile:City] rdfs:label "City"@en,

chile:City rdfs:label "Ciudad"@es, etc., indicating labels for the node in different languages. In other

models, the pertinent language can rather be specified, e.g., via metadata on the edge. Knowl
edge graphs with human-interpretable labels, aliases, comments, etc., (in various languages) are

sometimes called ( _multilingual_ ) _lexicalised knowledge graphs_ [57].


_3.2.5_ _Existential nodes._ When modelling incomplete information, we may in some cases know

that there must exist a particular node in the graph with particular relationships to other nodes,

but without being able to identify the node in question. For example, we may have two co-located

events [chile:EID42] and [chile:EID43] whose venue has yet to be announced. One option is to simply omit

the venue edges, in which case we lose the information that these events have a venue and that

both events have the same venue. Another option might be to create a fresh IRI representing the

venue, but semantically this becomes indistinguishable from there being a known venue. Hence

some graph models permit the use of existential nodes, represented here as a blank circle:


These edges denote that there exists a common venue for [chile:EID42] and [chile:EID42] without identifying

it. Existential nodes are supported in RDF as blank nodes [111], which are also commonly used to

support modelling complex elements in graphs, such as _RDF lists_ [111, 247]. Figure 17 exemplifies

an RDF list, which uses blank nodes in a linked-list structure to encode order. Though existential

nodes can be convenient, their presence can complicate operations on graphs, such as deciding

if two data graphs have the same structure modulo existential nodes [111, 245]. Hence methods

for _skolemising_ existential nodes in graphs – replacing them with canonical labels – have been

proposed [245, 325]. Other authors rather call to minimise the use of such nodes in graph data [226].


**3.3** **Context**

Many (arguably _all_ ) facts presented in the data graph of Figure 1 can be considered true with

respect to a certain _context_ . With respect to _temporal context_, [Santiago] has only existed as a city

since 1541, flights from [Arica] to [Santiago] began in 1956, etc. With respect to _geographic context_, the

graph describes events in Chile. With respect to _provenance_, data relating to [EID15] were taken from

- and are thus said to be true with respect to – the Ñam webpage on January 4 [th], 2020. Other forms

of context may also be used. We may further combine contexts, such as to indicate that [Arica] is a

Chilean city ( _geographic_ ) since 1883 ( _temporal_ ) according to the Treaty of Ancón ( _provenance_ ).


20


By context we herein refer to the _scope of truth_, and thus talk about the context in which some

data are held to be true [205, 345]. The graph of Figure 1 leaves much of its context implicit. However,

making context explicit can allow for interpreting the data from different perspectives, such as

to understand what held true in 2016, what holds true excluding webpages later found to have

spurious data, etc. As seen in the previous examples, context for graph data may be considered

at different levels: on individual nodes, individual edges, or sets of edges (sub-graphs). We now

discuss various representations by which context can be made explicit at different levels.


_3.3.1_ _Direct representation._ The first way to represent context is to consider it as data no different from other data. For example, the dates for the event [EID15] in Figure 1 can be seen as

representing a form of temporal context, indicating the temporal scope within which edges such as

EID15 venue Santa Lucía are held true. Another option is to change a relation represented as an edge,

such as [Santiago] flight Arica, into a node, such as seen in Figure 3, allowing to assign additional

context to the relation. While in these examples context is represented in an ad hoc manner, a

number of specifications have been proposed to represent context as data in a more standard way.

One example is the _Time Ontology_ [107], which specifies how temporal entities, intervals, time

instants, etc. – and relations between them such as before, overlaps, etc. – can be described in RDF

graphs in an interoperable manner. Another example is the _PROV Data Model_ [188], which specifies

how provenance can be described in RDF graphs, where entities (e.g., graphs, nodes, physical

document) are derived from other entities, are generated and/or used by activities (e.g., extraction,

authorship), and are attributed to agents (e.g., people, software, organisations).


_3.3.2_ _Reification._ Often we may wish to directly define the context of edges themselves; for
example, we may wish to state that the edge [Santiago] flight Arica is valid from 1956. While we

could use the pattern of turning the edge into a node – as illustrated in Figure 3 – to directly

represent such context, another option is to use _reification_, which allows for making statements

about statements in a generic manner (or in the case of a graph, for defining edges about edges). In

Figure 18 we present three forms of reification that can be used for modelling temporal context on

the aforementioned edge within a directed edge-labelled graph [235]. We use _𝑒_ to denote an arbitrary

identifier representing the edge itself to which the contextual information can be associated. Unlike

in a direct representation, _𝑒_ represents an edge, not a flight. RDF reification [111] (Figure 18a) defines

a new node _[𝑒]_ to represent the edge and connects it to the source node (via subject), target node
(via object), and edge label (via predicate) of the edge. In contrast, _𝑛_ -ary relations [111] (Figure 18b)

connect the source node of the edge directly to the edge node _[𝑒]_ with the label of the edge; the

target node of the edge is then connected to _[𝑒]_ (via value). Finally, singleton properties [383]

(Figure 18c) rather use _𝑒_ as an edge label, connecting it to a node indicating the original edge

label (via singleton). Other forms of reification have been proposed in the literature, including, for

example, NdFluents [190]. In general, a reified edge does not assert the edge it reifies; for example,

we may reify an edge to state that it is no longer valid. We refer to the work of Hernández et al. [235]

for further comparison of reification alternatives and their relative strengths and weaknesses.


_3.3.3_ _Higher-arity representation._ As an alternative to reification, we can rather use higher-arity
representations for modelling context. Taking again the edge Santiago flight Arica, Figure 19

illustrates three higher-arity representations of temporal context. First, we can use a named graph

(Figure 19a) to contain the edge and then define the temporal context on the graph name. Second, we

can use a property graph (Figure 19b) where the temporal context is defined as an attribute on the

edge. Third, we can use _RDF*_ [218] (Figure 19c): an extension of RDF that allows edges to be defined

as nodes. Amongst these options, the most flexible is the named graph representation, where we

can assign context to multiple edges at once by placing them in one named graph; for example, we


21


(b) _𝑛_ -ary Relations









(a) RDF Reification



(c) Singleton properties



Fig. 18. Three representations of temporal context on an edge in a directed-edge labelled graph





















(a) Named graph



(b) Property graph



(c) RDF*



Fig. 19. Three higher-arity representations of temporal context on an edge


can add more edges to the named graph of Figure 19a that are also valid from 1956. The least flexible

option is RDF*, which, in the absence of an edge id, does not permit different groups of contextual

values to be assigned to an edge; for example, considering the edge [Chile] president M. Bachelet, if

we add four contextual values to this edge to state that it was valid from 2006 until 2010 and valid

from 2014 until 2018, we cannot pair the values, but may rather have to create a node to represent

different presidencies (in the other models, we could have used two named graphs or edge ids).


_3.3.4_ _Annotations._ Thus far we have discussed representing context in a graph, but we have not

spoken about automated mechanisms for reasoning about context; for example, if there are only

seasonal summer flights from [Santiago] to [Arica], we may wish to find other routes from Santiago

for winter events taking place in [Arica] . While the dates for buses, flights, etc., can be represented
