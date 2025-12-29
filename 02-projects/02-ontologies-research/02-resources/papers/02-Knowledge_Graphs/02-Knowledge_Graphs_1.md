<!-- Source: 02-Knowledge_Graphs.pdf | Chunk 1/15 -->

### **Knowledge Graphs**

AIDAN HOGAN, IMFD, DCC, Universidad de Chile, Chile
EVA BLOMQVIST, Linköping University, Sweden
MICHAEL COCHEZ, Vrije Universiteit and Discovery Lab, Elsevier, The Netherlands
CLAUDIA D’AMATO, University of Bari, Italy
GERARD DE MELO, HPI, Germany and Rutgers University, USA
CLAUDIO GUTIERREZ, IMFD, DCC, Universidad de Chile, Chile
JOSÉ EMILIO LABRA GAYO, Universidad de Oviedo, Spain
SABRINA KIRRANE, SEBASTIAN NEUMAIER, and AXEL POLLERES, WU Vienna, Austria
ROBERTO NAVIGLI, Sapienza University of Rome, Italy
AXEL-CYRILLE NGONGA NGOMO, DICE, Universität Paderborn, Germany
SABBIR M. RASHID, Tetherless World Constellation, Rensselaer Polytechnic Institute, USA
ANISA RULA, University of Milano–Bicocca, Italy and University of Bonn, Germany
LUKAS SCHMELZEISEN, Universität Stuttgart, Germany
JUAN SEQUEDA, data.world, USA
STEFFEN STAAB, Universität Stuttgart, Germany and University of Southampton, UK
ANTOINE ZIMMERMANN, École des mines de Saint-Étienne, France


In this paper we provide a comprehensive introduction to knowledge graphs, which have recently garnered

significant attention from both industry and academia in scenarios that require exploiting diverse, dynamic,

large-scale collections of data. After some opening remarks, we motivate and contrast various graph-based data

models and query languages that are used for knowledge graphs. We discuss the roles of schema, identity, and

context in knowledge graphs. We explain how knowledge can be represented and extracted using a combination

of deductive and inductive techniques. We summarise methods for the creation, enrichment, quality assessment,

refinement, and publication of knowledge graphs. We provide an overview of prominent open knowledge

graphs and enterprise knowledge graphs, their applications, and how they use the aforementioned techniques.

We conclude with high-level future research directions for knowledge graphs.


CCS Concepts: • **Information systems** → **Graph-based database models** ; **Information integration** ;


Additional Key Words and Phrases: knowledge graph


**1** **INTRODUCTION**


Though the phrase “knowledge graph” has been used in the literature since at least 1972 [465], the

modern incarnation of the phrase stems from the 2012 announcement of the Google Knowledge

Graph [484], followed by further announcements of the development of knowledge graphs by

Airbnb [87], Amazon [298], eBay [417], Facebook [387], IBM [128], LinkedIn [224], Microsoft [482],

Uber [214], and more besides. The growing industrial uptake of the concept proved difficult for

academia to ignore: more and more scientific literature is being published on knowledge graphs,

which includes books (e.g. [425]), as well as papers outlining definitions (e.g., [141]), novel techniques

(e.g., [318, 424, 553]), and surveys of specific aspects of knowledge graphs (e.g., [400, 549]).

Underlying all such developments is the core idea of using graphs to represent data, often

enhanced with some way to explicitly represent knowledge [387]. The result is most often used in

application scenarios that involve integrating, managing and extracting value from diverse sources

of data at large scale [387]. Employing a graph-based abstraction of knowledge has numerous

benefits in such settings when compared with, for example, a relational model or NoSQL alternatives.

Graphs provide a concise and intuitive abstraction for a variety of domains, where edges capture the

(potentially cyclical) relations between the entities inherent in social data, biological interactions,


bibliographical citations and co-authorships, transport networks, and so forth [17]. Graphs allow

maintainers to postpone the definition of a schema, allowing the data – and its scope – to evolve in

a more flexible manner than typically possible in a relational setting, particularly for capturing

incomplete knowledge [3]. Unlike (other) NoSQL models, specialised graph query languages support

not only standard relational operators (joins, unions, projections, etc.), but also navigational

operators for recursively finding entities connected through arbitrary-length paths [16]. Standard

knowledge representation formalisms – such as ontologies [70, 239, 366] and rules [254, 288] –

can be employed to define and reason about the semantics of the terms used to label and describe

the nodes and edges in the graph. Scalable frameworks for graph analytics [335, 503, 563] can

be leveraged for computing centrality, clustering, summarisation, etc., in order to gain insights

about the domain being described. Various representations have also been developed that support

applying machine learning techniques directly over graphs [549, 559].

In summary, the decision to build and use a knowledge graph opens up a range of techniques that

can be brought to bear for integrating and extracting value from diverse sources of data. However,

we have yet to see a general unifying summary that describes how knowledge graphs are being

used, what techniques they employ, and how they relate to existing data management topics.

The goal of this tutorial paper is to motivate and give a comprehensive introduction to knowl
edge graphs: to describe their foundational data models and how they can be queried; to discuss

representations relating to schema, identity, and context; to discuss deductive and inductive ways

to make knowledge explicit; to present a variety of techniques that can be used for the creation

and enrichment of graph-structured data; to describe how the quality of knowledge graphs can be

discerned and how they can be refined; to discuss standards and best practices by which knowledge

graphs can be published; and to provide an overview of existing knowledge graphs found in practice.

Our intended audience includes researchers and practitioners who are new to knowledge graphs.

As such, we do not assume that readers have specific expertise on knowledge graphs.


_Knowledge graph._ The definition of a “ _knowledge graph_ ” remains contentious [40, 57, 141], where

a number of (sometimes conflicting) definitions have emerged, varying from specific technical

proposals to more inclusive general proposals; we address these prior definitions in Appendix A.

Herein we adopt an inclusive definition, where we view a knowledge graph as _a graph of data_

_intended to accumulate and convey knowledge of the real world, whose nodes represent entities of_

_interest and whose edges represent relations between these entities_ . The graph of data (aka _data graph_ )

conforms to a graph-based data model, which may be a _directed edge-labelled graph_, a _property_

_graph_, etc. (we discuss concrete alternatives in Section 2). By _knowledge_, we refer to something

that is _known_ [1] . Such knowledge may be accumulated from external sources, or extracted from the

knowledge graph itself. Knowledge may be composed of simple statements, such as “ _Santiago is_

_the capital of Chile_ ”, or quantified statements, such as “ _all capitals are cities_ ”. Simple statements

can be accumulated as edges in the data graph. If the knowledge graph intends to accumulate

quantified statements, a more expressive way to represent knowledge – such as _ontologies_ or _rules_

- is required. _Deductive methods_ can then be used to entail and accumulate further knowledge (e.g.,

“ _Santiago is a city_ ”). Additional knowledge – based on simple or quantified statements – can also be

extracted from and accumulated by the knowledge graph using _inductive methods_ .

Knowledge graphs are often assembled from numerous sources, and as a result, can be highly

diverse in terms of structure and granularity. To address this diversity, representations of _schema_,

_identity_, and _context_ often play a key role, where a _schema_ defines a high-level structure for the

knowledge graph, _identity_ denotes which nodes in the graph (or in external sources) refer to

the same real-world entity, while _context_ may indicate a specific setting in which some unit of


1A number of specific definitions for knowledge have been proposed in the literature on epistemology.


2


knowledge is held true. As aforementioned, effective methods for _extraction_, _enrichment_, _quality_

_assessment_, and _refinement_ are required for a knowledge graph to grow and improve over time.


_In practice._ Knowledge graphs aim to serve as an ever-evolving shared substrate of knowledge

within an organisation or community [387]. We distinguish two types of knowledge graphs in

practice: _open knowledge graphs_ and _enterprise knowledge graphs_ . Open knowledge graphs are

published online, making their content accessible for the public good. The most prominent exam
ples – DBpedia [311], Freebase [55], Wikidata [543], YAGO [243], etc. – cover many domains and

are either extracted from Wikipedia [243, 311], or built by communities of volunteers [55, 543].

Open knowledge graphs have also been published within specific domains, such as media [431],

government [233, 475], geography [497], tourism [13, 279, 328, 577], life sciences [82], and more

besides. Enterprise knowledge graphs are typically internal to a company and applied for com
mercial use-cases [387]. Prominent industries using enterprise knowledge graphs include Web

search (e.g., Bing [482], Google [484]), commerce (e.g., Airbnb [87], Amazon [132, 298], eBay [417],

Uber [214]), social networks (e.g., Facebook [387], LinkedIn [224]), finance (e.g., Accenture [390],

Banca d’Italia [35], Bloomberg [347], Capital One [69], Wells Fargo [377]), among others. Ap
plications include search [482, 484], recommendations [87, 214, 224, 387], personal agents [417],

advertising [224], business analytics [224], risk assessment [112, 522], automation [234], and more

besides. We will provide more details on the use of knowledge graphs in practice in Section 10.


_Running example._ To keep the discussion accessible, throughout the paper, we present concrete

examples in the context of a hypothetical knowledge graph relating to tourism in Chile (loosely

inspired by, e.g., [279, 328]). The knowledge graph is managed by a tourism board that aims to

increase tourism in the country and promote new attractions in strategic areas. The knowledge

graph itself will eventually describe tourist attractions, cultural events, services, and businesses, as

well as cities and inter-city travel routes. Some applications the organisation envisages are to:


  - create a tourism portal that allows visitors to search for attractions, upcoming events, and

other related services (in multiple languages);

  - gain insights into tourism demographics in terms of season, nationalities, etc.;

  - analyse sentiment about various attractions and events, including positive reviews, summaries

of complaints about events and services, reports of crime, etc.;

  - understand tourism trajectories: the sequence of attractions, events, etc., that tourists visit;

  - cross-reference trajectories with available flights/buses to suggest new strategic routes;

  - offer personalised recommendations of places to visit;

  - and so forth.


_Related Literature._ A number of related surveys, books, etc., have been published relating to

knowledge graphs. In Table 1, we provide an overview of the tertiary literature – surveys, books,

tutorials, etc. – relating to knowledge graphs, comparing the topics covered to those covered herein.

We see that the existing literature tends to focus on specific aspects of knowledge graphs. Unlike

the various surveys that have been published, our goal as a tutorial paper is to provide a broad

and accessible introduction to knowledge graphs. Some of the surveys (in particular) provide more

in-depth technical details on their chosen topic than this paper; throughout the discussion, where

appropriate, we will refer to these surveys for further reading.


_Structure._ The remainder of the paper is structured as follows:


**Section 2** outlines graph data models and the languages that can be used to query them.
**Section 3** describes representations of schema, identity, and context in knowledge graphs.
**Section 4** presents deductive formalisms by which knowledge can be represented and entailed.


3


Table 1. Related tertiary literature on knowledge graphs; ✓ denotes in-depth discussion, denotes brief
discussion, * denotes informal publication (arXiv)


**Publication** **Year Type**


Pan et al. [392] 2017 Book ✓ ✓ ✓ ✓ ✓ ✓

Paulheim [400] 2017 Survey ✓

Wang et al. [549] 2017 Survey ✓

Yan et al. [567] 2018 Survey ✓ ✓ ✓ ✓ ✓

Gesese et al. [183] 2019 Survey ✓

Kazemi et al. [282] 2019 Survey* ✓ ✓ ✓

Kejriwal [286] 2019 Book ✓

Xiao et al. [562] 2019 Survey ✓

Wang and Yang [552] 2019 Survey ✓ ✓

Al-Moslmi et al. [8] 2020 Survey ✓

Fensel et al. [154] 2020 Book ✓ ✓

Heist et al. [229] 2020 Survey* ✓

Ji et al. [272] 2020 Survey* ✓ ✓ ✓ ✓


Hogan et al. 2020 Tutorial* ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓ ✓


**Section 5** describes inductive techniques by which additional knowledge can be extracted.
**Section 6** discusses the creation and enrichment of knowledge graphs from external sources.
**Section 7** enumerates quality dimensions by which a knowledge graph can be assessed.
**Section 8** discusses various techniques for knowledge graph refinement.
**Section 9** discusses principles and protocols for publishing knowledge graphs.
**Section 10** surveys some prominent knowledge graphs and their applications.
**Section 11** concludes with a summary and future research directions for knowledge graphs.
**Appendix A** provides historical background and previous definitions for knowledge graphs.
**Appendix B** enumerates formal definitions that will be referred to from the body of the paper.


**2** **DATA GRAPHS**


At the foundation of any knowledge graph is the principle of first applying a graph abstraction to

data, resulting in an initial data graph. We now discuss a selection of graph-structured data models

that are commonly used in practice to represent data graphs. We then discuss the primitives that

form the basis of graph query languages used to interrogate such data graphs.


**2.1** **Models**

Leaving aside graphs, let us assume that the tourism board from our running example has not

yet decided how to model relevant data about attractions, events, services, etc. The board first

considers using a tabular structure – in particular, relational databases – to represent the required

data, and though they do not know precisely what data they will need to capture, they start to

design an initial relational schema. They begin with an Event table with five columns:


Event(name _,_ venue _,_ type _,_ start _,_ end)


where name and start together form the primary key of the table in order to uniquely identify

recurring events. But as they start to populate the data, they encounter various issues: events may


4


have multiple names (e.g., in different languages), events may have multiple venues, they may

not yet know the start and end date-times for future events, events may have multiple types, and

so forth. Incrementally addressing these modelling issues as the data become more diverse, they

generate internal identifiers for events and adapt their relational schema until they have:


EventName(id _,_ name) _,_ EventStart(id _,_ start) _,_ EventEnd(id _,_ end) _,_ (1)


EventVenue(id _,_ venue) _,_ EventType(id _,_ type)


With the above schema, the organisation can now model events with 0– _𝑛_ names, venues, and types,

and 0–1 start dates and end dates (without needing relational nulls/blank cells in tables).

Along the way, the board has to incrementally change the schema several times in order to support

new sources of data. Each such change requires a costly remodelling, reloading, and reindexing of

data; here we only considered one table. The tourism board struggles with the relational model

because they do not know, _a priori_, what data will need to be modelled or what sources they will

use. But once they reach the latter relational schema, the board finds that they can integrate further

sources without more changes: with minimal assumptions on _multiplicities_ (1–1, 1– _𝑛_, etc.) this

schema offers a lot of flexibility for integrating incomplete and diverse data.

In fact, the refined, flexible schema that the board ends up with – shown in (1) – is modelling

a set of binary relations between entities, which indeed can be viewed as modelling a graph. By

instead adopting a graph data model from the outset, the board could forgo the need for an upfront

schema, and could define any (binary) relation between any pair of entities at any time.

We now introduce graph data models commonly used in practice [16].


_2.1.1_ _Directed edge-labelled graphs._ A directed edge-labelled graph (also known as a _multi-relational_
_graph_ [29, 63, 386]) is defined as a set of nodes – like [Santiago], [Arica], [EID16], [2018-03-22 12:00] - and a
set of directed labelled edges between those nodes, like [Santa Lucía] city Santiago . In the case of

knowledge graphs, nodes are used to represent entities and edges are used to represent (binary)

relations between those entities. Figure 1 provides an example of how the tourism board could

model some relevant event data as a directed edge-labelled graph (for a formal definition of a

directed edge-labelled graph see Definition B.1 in Appendix B). The graph includes data about

the names, types, start and end date-times, and venues for events. [2] Adding information to such

a graph typically involves adding new nodes and edges (with some exceptions discussed later).

Representing incomplete information requires simply omitting a particular edge; for example, the

graph does not yet define a start/end date-time for the Food Truck festival.

Modelling data as a graph in this way offers more flexibility for integrating new sources of data,

compared to the standard relational model, where a schema must be defined upfront and followed

at each step. While other structured data models such as trees (XML, JSON, etc.) would offer similar

flexibility, graphs do not require organising the data hierarchically (should venue be a parent, child,
or sibling of type for example?). They also allow cycles to be represented and queried (e.g., note

the directed cycle in the routes between Santiago, Arica, and Viña del Mar).

A standardised data model based on directed edge-labelled graphs is the Resource Description

Framework (RDF) [111], which has been recommended by the W3C. The RDF model defines

different types of nodes, including _Internationalized Resource Identifiers_ (IRIs) [134] which allow for

global identification of entities on the Web; _literals_, which allow for representing strings (with or

2We represent bidirectional edges as Viña del Mar bus Arica, which more concisely depicts two directed edges:
Viña del Mar bus Arica and [Viña del Mar] bus Arica . Also while some naming conventions recommend more
complete edge labels that include a verb, such as has venue or is valid from, in this paper, for presentation purposes, we will
omit the “has” and “is” verbs from such labels, using simply venue or valid from.


5


Fig. 1. Directed edge-labelled graph describing events and their venues.











(a) Del graph



(b) Heterogeneous graph


Fig. 2. Data about capitals and countries in a directed edge-labelled graph and a heterogeneous graph


without language tags) and other datatype values (integers, dates, etc.); and _blank nodes_, which

are anonymous nodes that are not assigned an identifier (for example, rather than create internal

identifiers like EID15, EID16, in RDF, we have the option to use blank nodes). We will discuss these

different types of nodes further in Section 3.2 when we speak about issues relating to identity.


_2.1.2_ _Heterogeneous graphs._ A heterogeneous graph [257, 551, 570] (or _heterogeneous information_

_network_ [509, 510]) is a graph where each node and edge is assigned one type. Heterogeneous

graphs are thus akin to del graphs – with edge labels corresponding to edge types – but where the

type of node forms part of the graph model itself, rather than being expressed as a special relation,

as illustrated in Figure 2. An edge is called _homogeneous_ if it is between two nodes of the same type

(e.g., borders); otherwise it is called _heterogeneous_ (e.g., capital). A benefit of heterogeneous graphs

is that they allow for partitioning nodes according to their type, for example, for the purposes

of machine learning tasks [257, 551, 570]. Conversely, they typically only support a one-to-one

relation between nodes and types, which is not the case for del graphs (see, for example, the node


Santiago with zero types and EID15 with multiple types in Figure 1).


_2.1.3_ _Property graphs._ Property graphs were introduced to provide additional flexibility when

modelling more complex relations. Consider integrating incoming data that provides information

on which companies offer fares on which flights, allowing the board to better understand available


6


Fig. 3. Directed edge-labelled graph with companies offering flights between Santiago and Arica















Fig. 4. Property graph with companies offering flights between Santiago and Arica


routes between cities (for example, on national airlines). In the case of directed-edge labelled graphs,

we cannot directly annotate an edge like [Santiago] flight Arica with the company (or companies)

offering that route. But we could add a new node denoting a flight, connect it with the source,

destination, companies, and mode, as shown in Figure 3. Applying this modelling to all routes in

Figure 1 would, however, involve a significant change to the graph. Another option might be to put

the flights of different companies in different named graphs, but if named graphs are already being

used to track the source of graphs (for example), this could become cumbersome.

The property graph model was thus proposed to offer additional flexibility when modelling

data as a graph [16, 354]. A property graph allows a set of _property–value_ pairs and a _label_ to be

associated with both nodes and edges. Figure 4 shows a concise example of a property graph with

data analogous to Figure 3 (for a formal definition of a property graph, we refer to Definition B.5 in

Appendix B). This time we use property–value pairs on edges to model the companies [3] . The type

of relation is captured by the label flight. We further use node labels to indicate the types of the

two nodes, and use property–value pairs to indicate their latitude and longitude.

Property graphs are most prominently used in popular graph databases, such as Neo4j [16, 354].

In choosing between graph models, it is important to note that property graphs can be translated

to/from directed edge-labelled graphs without loss of information [18, 235] (per, e.g., Figure 4). In

summary, directed-edge labelled graphs offer a more minimal model, while property graphs offer a

more flexible one. Often the choice of model will be secondary to other practical factors, such as

the implementations available for different models, etc.


_2.1.4_ _Graph dataset._ Although multiple directed edge-labelled graphs can be merged by taking

their union, it is often desirable to manage several graphs rather than one monolithic graph; for

example, it may be beneficial to manage multiple graphs from different sources, making it possible to

update or refine data from one source, to distinguish untrustworthy sources from more trustworthy

ones, and so forth. A graph dataset then consists of a set of _named graphs_ and a _default graph_ . Each


3In practical implementations of property graphs, properties with multiple values may be expressed, for example, as a single

array value. Such issues do not, however, affect expressivity, nor our discussion.


7


Fig. 5. Graph dataset with two named graphs and a default graph describing events and routes


named graph is a pair of a graph ID and a graph. The default graph is a graph without an ID, and is

referenced “by default” if a graph ID is not specified. Figure 5 provides an example where events

and routes are stored in two named graphs, and the default graph manages meta-data about the

named graphs (for a formal definition of a graph dataset, see Definition B.7 in Appendix B). Graph

names can also be used as nodes in a graph. Furthermore, nodes and edges can be repeated across

graphs, where the same node in different graphs will typically refer to the same entity, allowing

data on that entity to be integrated when merging graphs. Though the example illustrates a dataset

of directed edge-labelled graphs, the concept generalises straightforwardly to other types of graphs.

A prominent use-case for graph datasets is to manage and query _Linked Data_ composed of

interlinked documents of RDF graphs spanning the Web. When dealing with Web data, tracking

the source of data becomes of key importance [58, 130, 583]. We will discuss Linked Data later in

Section 3.2 and further discuss provenance in Section 3.3.


_2.1.5_ _Other graph data models._ The previous models are popular examples of graph representations.

Other graph data models exist with _complex nodes_ that may contain individual edges [17, 222] or

nested graphs [17, 42] (sometimes called _hypernodes_ [315]). Likewise the mathematical notion of

a _hypergraph_ defines _complex edges_ that connect sets rather than pairs of nodes. In our view, a

knowledge graph can adopt any such graph data model based on nodes and edges: often data can be

converted from one model to another (see Figure 3 vs. Figure 4). In the rest of the paper, we prefer

discussing directed-edge labelled graphs given their relative succinctness, but most discussion

extends naturally to other models.


8


_2.1.6_ _Graph stores._ A variety of techniques have been proposed for storing and indexing graphs,

facilitating the efficient evaluation of queries (as discussed next). Directed-edge labelled graphs can

be stored in relational databases either as a single relation of arity three ( _triple table_ ), as a binary

relation for each property ( _vertical partitioning_ ), or as _𝑛_ -ary relations for entities of a given type

( _property tables_ ) [560]. Custom storage techniques have also been developed for a variety of graph

models, providing efficient access for finding nodes, edges and their adjacent elements [17, 354, 560].

A number of systems further allow for distributing graphs over multiple machines based on popular

NoSQL stores or custom partitioning schemes [267, 560]. For further details we refer to the book

chapter by Janke and Staab [267] and the survey by Wylot et al. [560] dedicated to this topic.


**2.2** **Querying**

A number of practical languages have been proposed for querying graphs [16], including the

SPARQL query language for RDF graphs [217]; and Cypher [165], Gremlin [445], and G-CORE [15]

for querying property graphs. [4] Underlying these query languages are some common primitives,

including (basic) graph patterns, relational operators, path expressions, and more besides [16]. We

now describe these core features for querying graphs in turn, starting with graph patterns.


_2.2.1_ _Graph patterns._ At the core of every structured query language for graphs are ( _basic_ ) _graph_

_patterns_ [16, 100], which follow the same model as the data graph being queried (see Section 2.1),

additionally allowing variables as terms. [5] Terms in graph patterns are thus divided into constants,

such as [Arica] or venue, and variables, which we prefix with question marks, such as [?event] or ?rel. A

graph pattern is then evaluated against the data graph by generating mappings from the variables

of the graph pattern to constants in the data graph such that the image of the graph pattern under

the mapping (replacing variables with the assigned constants) is contained within the data graph.

In Figure 6, we provide an example of a graph pattern looking for the venues of Food Festivals,

along with the possible mappings generated by the graph pattern against the data graph of Figure 1.

In some of the presented mappings (the last two listed), multiple variables are mapped to the

same term, which may or may not be desirable depending on the application. Hence a number

of semantics have been proposed for evaluating graph patterns [16], amongst which the most

important are: _homomorphism-based semantics_, which allows multiple variables to be mapped to the

same term such that all mappings shown in Figure 6 would be considered results; and _isomorphism-_

_based semantics_, which requires variables on nodes and/or edges to be mapped to unique terms,

thus excluding the latter three mappings of Figure 6 from the results. Different practical languages

adopt different semantics for evaluating graph patterns where, for example, SPARQL adopts a

homomorphism-based semantics, while Cypher adopts an isomorphism-based semantics on edges.

As we will see in later examples (particularly Figure 8), graph patterns may also form cycles

(be they directed or undirected), and may replace edge labels with variables. Graph patterns in

the context of other models – such as property graphs – can be defined analogously by allowing

variables to replace terms in any position of the model. We provide a formalisation of graph patterns

and their evaluation for both directed edge-labelled graphs and property graphs in Appendix B.2.1.


_2.2.2_ _Complex graph patterns._ A graph pattern transforms an input graph into a table of results (as

shown in Figure 6). We may then consider using the relational algebra to combine and/or transform

such tables, thus forming more complex queries from one or more graph patterns. Recall that the

relational algebra consists of unary operators that accept one input table, and binary operators


4The popularity of these languages is investigated by Seifer et al. [470].

5The terms of a directed edge-labelled graph are its nodes and edge-labels. The terms of a property graph are its ids, labels,

properties, and values (as used on either edges or nodes).


9


**?ev** **?vn1** **?vn2**


EID16 Piscina Olímpica Sotomayor

EID16 Sotomayor Piscina Olímpica

EID16 Piscina Olímpica Piscina Olímpica

EID16 Sotomayor Sotomayor

EID15 Santa Lucía Santa Lucía



Fig. 6. Graph pattern (left) with mappings generated over the graph of Figure 1 (right)


that accept two input tables. Unary operators include projection ( _𝜋_ ) to output a subset of columns,

selection ( _𝜎_ ) to output a subset of rows matching a given condition, and renaming of columns ( _𝜌_ ).

Binary operators include union (∪) to merge the rows of two tables into one table, difference (−)

to remove the rows from the first table present in the second table, and joins (�) to extend the

rows of one table with rows from the other table that satisfy a join condition. Selection and join

conditions typically include equalities (=), inequalities (≤), negation (¬), disjunction (∨), etc. From
these operators, we can further define other (syntactic) operators, such as intersection (∩) to output

rows in both tables, anti-join (▷, aka _not exists_ ) to output rows from the first table for which there

are no join-compatible rows in the second table, left-join ( ~~�~~, aka _optional_ ) to perform a join but

keeping rows from the first table without a compatible row in the second table, etc.

Graph patterns can then be expressed in a subset of relational algebra (namely _𝜋_, _𝜎_, _𝜌_, �).

Assuming, for example, a single ternary relation _𝐺_ ( _𝑠, 𝑝,𝑜_ ) representing a graph – i.e., a table _𝐺_

with three columns _𝑠_, _𝑝_, _𝑜_ - the query of Figure 6 can be expressed in relational algebra as:


_𝜋𝑒𝑣,𝑣𝑛_ 1 _,𝑣𝑛_ 2( _𝜎𝑝_ =type∧ _𝑜_ =Food Festival∧ _𝑝_ 1= _𝑝_ 2=venue( _𝜌𝑠_ / _𝑒𝑣_ ( _𝐺_ _⊲⊳_ _𝜌𝑝_ / _𝑝_ 1 _,𝑜_ / _𝑣𝑛_ 1( _𝐺_ ) _⊲⊳_ _𝜌𝑝_ / _𝑝_ 2 _,𝑜_ / _𝑣𝑛_ 2( _𝐺_ ))))


where � denotes a _natural join_, meaning that equality is checked across pairs of columns with the

same name in both tables (here, the join is thus performed on the subject column _𝑠_ ). The result of

this query is a table with a column for each variable: _𝑒𝑣, 𝑣𝑛_ 1 _, 𝑣𝑛_ 2. However, not all queries using _𝜋_,

_𝜎_, _𝜌_ and � on _𝐺_ can be expressed as graph patterns; for example, we cannot choose which variables

to project in a graph pattern, but rather must project all variables not fixed to a constant.

Graph query languages such as SPARQL [217] and Cypher [165] allow the full use of relational

operators over the results of graph patterns, giving rise to _complex graph patterns_ [16]. Figure 7

presents an example of a complex graph pattern with projected variables in bold, choosing particular

variables to appear in the final results. In terms of expressivity, graph patterns with (unrestricted)

projection of this form equate to _conjunctive queries_ on graphs. In Figure 8, we give another example

of a complex graph pattern looking for food festivals or drinks festivals not held in Santiago,

optionally returning their start date and name (where available). Such queries – allowing the full

use of relational operators on top of graph patterns – equate to _first-order queries_ on graphs. In

Appendix B.2.2, we formalise complex graph patterns and their evaluation over data graphs.

Complex graph patterns can give rise to duplicate results; for example, the first result in Figure 7

appears twice since ?city1 matches Arica and ?city2 matches Viña del Mar in one result,

and vice-versa in the other. Query languages then offer two semantics: _bag semantics_ preserves

duplicates according to the multiplicity of the underlying mappings, while _set semantics_ (typically

invoked with a DISTINCT keyword) removes duplicates from the results.


_2.2.3_ _Navigational graph patterns._ A key feature that distinguishes graph query languages is the

ability to include _path expressions_ in queries. A path expression _𝑟_ is a regular expression that

allows matching arbitrary-length paths between two nodes, which is expressed as a _regular path_

_query_ ( _𝑥,𝑟,𝑦_ ), where _𝑥_ and _𝑦_ can be variables or constants (or even the same term). The base path


10


**?name1** **?con** **?name2**


Food Truck bus Food Truck

Food Truck bus Food Truck

Food Truck bus Ñam

Food Truck flight Ñam

Food Truck flight Ñam

Ñam bus Food Truck

Ñam flight Food Truck

Ñam flight Food Truck













Fig. 7. Conjunctive query (left) with mappings generated over the graph of Figure 1 (right)

_𝑄_ 1: **?event** type Food Festival _𝑄_ 2: **?event** type Drinks Festival

_𝑄_ 3: **?event** venue ?ven city Santiago _𝑄_ 4: **?event** start **?start** _𝑄_ 5: **?event** name **?name**



_𝑄_ := (((( _𝑄_ 1 ∪ _𝑄_ 2) ▷ _𝑄_ 3) ~~�~~ _𝑄_ 4) ~~�~~ _𝑄_ 5) _,_ _𝑄_ ( _𝐺_ ) =



**?event** **?start** **?name**


EID16 Food Truck



Fig. 8. Complex graph pattern ( _𝑄_ ) with mappings generated ( _𝑄_ ( _𝐺_ )) over the graph of Figure 1 ( _𝐺_ )

1 Arica 2 Arica bus Viña del Mar 3 Arica bus Viña del Mar bus Arica


Fig. 9. Some possible paths matching (Arica _,_ bus* _,_ ?city) over the graph of Figure 1


expression is where _𝑟_ is a constant (an edge label). Furthermore if _𝑟_ is a path expression, then _𝑟_ [−]

( _inverse_ ) [6] and _𝑟_ [∗] ( _Kleene star_ : zero-or-more) are also path expressions. Finally, if _𝑟_ 1 and _𝑟_ 2 are path
expressions, then _𝑟_ 1 | _𝑟_ 2 ( _disjunction_ ) and _𝑟_ 1 · _𝑟_ 2 ( _concatenation_ ) are also path expressions.

Regular path queries can then be evaluated under a number of different semantics. For example,

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
