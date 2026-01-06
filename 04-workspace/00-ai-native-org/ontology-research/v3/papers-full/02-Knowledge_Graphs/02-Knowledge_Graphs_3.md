<!-- Source: 02-Knowledge_Graphs.pdf | Chunk 3/15 -->

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

directly in the graph, or using reification, writing a query to manually intersect the corresponding

temporal contexts will be tedious – or may not even be possible at all. Another alternative is

to consider _annotations_ that provide mathematical definitions of a contextual domain and key

operations possible within that domain that can then be applied automatically.

Some annotations model a particular contextual domain; for example, _Temporal RDF_ [210]

allows for annotating edges with time intervals, such as [Chile] [2006 _,_ 2010] M. Bachelet, while _Fuzzy_

_RDF_ [502] allows for annotating edges with a degree of truth such as [Santiago] 0 _._ 8 Semi-Arid,


indicating that it is more-or-less true – with a degree of 0.8 – that Santiago has a semi-arid climate.

Other forms of annotation are domain-independent; for example, _Annotated RDF_ [130, 530, 583]

allows for representing various forms of context modelled as _semi-rings_ : algebraic structures

consisting of domain values (e.g., temporal intervals, fuzzy values, etc.) and two main operators to

combine domain values: _meet_ and _join_ . [10] We provide an example in Figure 20, where _𝐺_ is annotated

with values from a simplified temporal domain consisting of sets of integers (1–365) representing

days of the year. For brevity we use an interval notation, where, for example, {[150 _,_ 152]} indicates
the set {150 _,_ 151 _,_ 152}. Query _𝑄_ then asks for flights from Santiago to cities with events; this query


10The _join_ operator for annotations is different from the join operator for relational algebra.


22


_𝑄_ : ?event


|?event|Col2|
|---|---|
|ci|ty|







_𝑄_ ( _𝐺_ ) :



**?city** **context**


Arica {[123 _,_ 125] _,_ [276 _,_ 279]}



Fig. 20. Example query on a temporally annotated graph


will check and return an annotation reflecting the temporal validity of each answer. To derive

these answers, we first require applying a conjunction of annotations on compatible flight and
city edges, applying the _meet operator_ to compute the annotation for which both edges hold. The

natural way to define meet in our scenario is as the intersection of sets of days, where, for example,

applying meet on the event annotation {[150 _,_ 152]} and the flight annotation {[1 _,_ 120] _,_ [220 _,_ 365]}
for [Punta Arenas] leads to the empty time interval {}, which may thus lead to the city being filtered

from the results (depending on the query evaluation semantics). However, for [Arica], we find two
different non-empty intersections: {[123 _,_ 125]} for [EID16] and {[276 _,_ 279]} for [EID17] . Given that we

are interested in the city (a projected variable), rather than the event, we can thus combine these

two annotations for [Arica] using the _join operator_, returning the annotation in which either result

holds true. In our scenario, the natural way to define join is as the union of the sets of days, giving

{[123 _,_ 125] _,_ [276 _,_ 279]}. We provide formal definitions in Appendix B.4.1 based on the general

framework proposed by Zimmermann et al. [583] for annotations on graphs.


_3.3.5_ _Other contextual frameworks._ Other frameworks have been proposed for modelling and rea
soning about context in graphs. A notable example is that of _contextual knowledge repositories_ [252],

which allow for assigning individual (sub-)graphs to their own context. Unlike in the case of named

graphs, context is explicitly modelled along one or more dimensions, where each (sub-)graph must

take a value for each dimension. Each dimension is further associated with a partial order over its

values – e.g., [2020-03-22] ⪯ [2020-03] ⪯ [2020] - allowing to select and combine sub-graphs that are valid

within contexts at different levels of granularity. Schuetz et al. [467] similarly propose a form of

contextual OnLine Analytic Processing (OLAP), based on a data cube formed by dimensions where

individual cells contain knowledge graphs. Operations such as “ _slice-and-dice_ ” (selecting knowledge

according to given dimensions), as well as “ _roll-up_ ” (aggregating knowledge at a higher level) can

then be supported. We refer the reader to the respective papers for more details [252, 467].


**4** **DEDUCTIVE KNOWLEDGE**

As humans, we can _deduce_ more from the data graph of Figure 1 than what the edges explicitly

indicate. We may deduce, for example, that the Ñam festival ( [EID15] ) will be located in Santiago,
even though the graph does not contain an edge [EID15] location Santiago . We may further deduce

that the cities connected by flights must have some airport nearby, even though the graph does

not contain nodes referring to these airports. In these cases, given the data as premises, and some

general rules about the world that we may know _a priori_, we can use a deductive process to derive

new data, allowing us to know more than what is explicitly given by the data. These types of general

premises and rules, when shared by many people, form part of “ _commonsense knowledge_ ” [344];

conversely, when rather shared by a few experts in an area, they form part of “ _domain knowledge_ ”,


23


Fig. 21. Graph pattern querying for names of festivals in Santiago


where, for example, an expert in biology may know that _hemocyanin_ is a protein containing copper

that carries oxygen in the blood of some species of _Mollusca_ and _Arthropoda_ .

Machines, in contrast, do not have _a priori_ access to such deductive faculties; rather they need to

be given formal instructions, in terms of premises and _entailment regimes_, in order to make similar

deductions to what a human can make. These entailment regimes formalise the conclusions that

logically follow as a consequence of a given set of premises. Once instructed in this manner, machines

can (often) apply deductions with a precision, efficiency, and scale beyond human performance.

These deductions may serve a range of applications, such as improving query answering, (deductive)

classification, finding inconsistencies, etc. As a concrete example involving query answering, assume

we are interested in knowing _the festivals located in Santiago_ ; we may straightforwardly express

such a query as per the graph pattern shown in Figure 21. This query returns no results for the

graph in Figure 1: there is no node named [Festival], and nothing has (directly) the location [Santiago] .

However, an answer ( [Ñam] ) could be automatically entailed were we to state that _𝑥_ being a Food

Festival _entails_ that _𝑥_ is a Festival, or that _𝑥_ having venue _𝑦_ in city _𝑧_ _entails_ that _𝑥_ has location

_𝑧_ . How, then, should such entailments be captured? In Section 3.1.1 we already discussed how

the former entailment can be captured with sub-class relations in a semantic schema; the second

entailment, however, requires a more expressive entailment regime than seen thus far.

In this section, we discuss ways in which more complex entailments can be expressed and

automated. Though we could leverage a number of logical frameworks for these purposes – such as

First-Order Logic, Datalog, Prolog, Answer Set Programming, etc. – we focus on _ontologies_, which

constitute a formal representation of knowledge that, importantly for us, can be represented as a

graph. We then discuss how these ontologies can be formally defined, how they relate to existing

logical frameworks, and how reasoning can be conducted with respect to such ontologies.


**4.1** **Ontologies**


To enable entailment, we must be precise about what the terms we use mean. Returning to Figure 1,

for example, and examining the node [EID16] more closely, we may begin to question how it is

modelled, particularly in comparison with [EID15] . Both nodes – according to the class hierarchy

of Figure 11 – are considered to be events. But what if, for example, we wish to define two pairs

of start and end dates for [EID16] corresponding to the different venues? Should we rather consider

what takes place in each venue as a different event? What then if an event has various start and end

dates in a single venue: would these also be considered as one (recurring) event, or many events?

These questions are facets of a more general question: _what precisely do we mean by an “event”_ ?

Does it happen in one contiguous time interval or can it happen many times? Does it happen in

one place or can it happen in multiple? There are no “correct” answers to such questions – we may

understand the term “event” in a variety of ways, and thus the answers are a matter of _convention_ .

In the context of computing, an _ontology_ [11] is then a concrete, formal representation of what

terms mean within the scope in which they are used (e.g., a given domain). For example, one event

ontology may formally define that if an entity is an “event”, then it has precisely one venue and


11The term stems from the philosophical study of _ontology_, concerned with the different kinds of entities that exist, the

nature of their existence, what kinds of properties they have, and how they may be identified and categorised.


24


precisely one time instant in which it begins. Conversely, a different event ontology may define

that an “event” can have multiple venues and multiple start times, etc. Each such ontology formally

captures a particular perspective – a particular _convention_ . Under the first ontology, for example,

we could not call the Olympics an “event”, while under the second ontology we could. Likewise

ontologies can guide how graph data are modelled. Under the first ontology we may split [EID16] into

two events. Under the second, we may elect to keep [EID16] as one event with two venues. Ultimately,

given that ontologies are formal representations, they can be used to automate entailment.

Like all conventions, the usefulness of an ontology depends on the level of agreement on what

that ontology defines, how detailed it is, and how broadly and consistently it is adopted. Adoption

of an ontology by the parties involved in one knowledge graph may lead to a consistent use of

terms and consistent modelling in that knowledge graph. Agreement over multiple knowledge

graphs will, in turn, enhance the interoperability of those knowledge graphs.

Amongst the most popular ontology languages used in practice are the _Web Ontology Language_

( _OWL_ ) [239] [12], recommended by the W3C and compatible with RDF graphs; and the _Open Biomedical_

_Ontologies Format_ ( _OBOF_ ) [366], used mostly in the biomedical domain. Since OWL is the more

widely adopted, we focus on its features, though many similar features are found in both [366].

Before introducing such features, however, we must discuss how graphs are to be _interpreted_ .


_4.1.1_ _Interpretations._ We as humans may _interpret_ the node [Santiago] in the data graph of Figure 1

as referring to the real-world city that is the capital of Chile. We may further _interpret_ an edge

Arica flight Santiago as stating that there are flights from the city of Arica to this city. We thus

interpret the data graph as another graph – what we here call the _domain graph_ - composed of

real-world entities connected by real-world relations. The process of interpretation, here, involves

_mapping_ the nodes and edges in the data graph to nodes and edges of the domain graph.

Along these lines, we can abstractly define an _interpretation_ of a data graph as being composed

of two elements: a domain graph, and a mapping from the _terms_ (nodes and edge-labels) of the data

graph to those of the domain graph. The domain graph follows the same model as the data graph;

for example, if the data graph is a directed edge-labelled graph, then so too will be the domain

graph. For simplicity, we will speak of directed edge-labelled graphs and refer to the nodes of the

domain graph as _entities_, and the edges of the domain graph as _relations_ . Given a data graph and an

interpretation, while we denote nodes in the data graph by [Santiago], we will denote the entity it refers

to in the domain graph by [Santiago] (per the mapping of the given interpretation). Likewise, while
we denote an edge by [Arica] flight Santiago, we will denote the relation by [Arica] flight Santiago

(again, per the mapping of the given interpretation). In this abstract notion of an interpretation, we

do not require that [Santiago] nor [Arica] be the real-world cities, nor even that the domain graph contain

real-world entities and relations: an interpretation can have any domain graph and mapping.

Why is such an abstract notion of interpretation useful? The distinction between nodes/edges

and entities/relations becomes important when we define the meaning of ontology features and

entailment. To illustrate this distinction, if we ask whether there is an edge labelled flight between

Arica and Viña del Mar for the data graph in Figure 1, the answer is _no_ . However, if we ask if the
entities [Arica] and [Viña del Mar] are connected by the relation flight, then the answer depends on what

assumptions we make when interpreting the graph. Under the Closed World Assumption (CWA), if

we do not have additional knowledge, then the answer is a definite _no_ - since what is not known is

assumed to be false. Conversely, under the Open World Assumption (OWA), we cannot be certain

that this relation does not exist as this could be part of some knowledge not (yet) described by

the graph. Likewise under the Unique Name Assumption (UNA), the data graph describes _at least_


12We could include RDF Schema (RDFS) in this list, but it is largely subsumed by OWL, which builds upon its core.


25


_two_ flights to [Santiago] (since [Viña del Mar] and [Arica] are assumed to be different entities and therefore,

Arica flight Santiago and [Viña del Mar] flight Santiago must be different edges). Conversely, under

No Unique Name Assumption (NUNA), we can only say that there is _at least one_ such flight since


Viña del Mar and Arica may be the same entity with two “names”.

These assumptions (or lack thereof) define which interpretations are valid, and which interpreta
tions _satisfy_ which data graphs. The UNA forbids interpretations that map two data terms to the

same domain term. The NUNA allows such interpretations. Under CWA, an interpretation that

contains an edge [x] p y in its domain graph can only satisfy a data graph from which we can
entail [x] p y . Under OWA, an interpretation containing the edge [x] p y can satisfy a data graph
not entailing [x] p y so long it does not contradict that edge. [13] In the case of OWL, the NUNA and

|Col1|m. The|
|---|---|
||x<br>p|
|. Un<br>x<br>p|. Un<br>x<br>p|



OWA are adopted, thus representing the most general case, whereby multiple nodes/edge-labels in

the graph may refer to the same entity/relation-type (NUNA), and where anything not entailed by

the data graph is _not_ assumed to be false as a consequence (OWA).

Beyond our base assumptions, we can associate certain patterns in the data graph with _semantic_

_conditions_ that define which interpretations satisfy it; for example, we can add a semantic condition

to enforce that if our data graph contains the edge [p] subp. of q, then any edge [x] p y in the
domain graph of the interpretation must also have a corresponding edge [x] q y to satisfy the data

graph. These semantic conditions then form the features of an ontology language. In what follows,

to aid readability, we will introduce the features of OWL using an abstract graphical notation

with abbreviated terms. For details of concrete syntaxes, we rather refer to the OWL and OBOF

standards [239, 366]. Likewise we present semantic conditions for interpretations associated with

each feature in the same graphical format; [14] further details of these conditions will be described

later in Section 4.2, with formal definitions rather provided in Appendix B.5.


_4.1.2_ _Individuals._ In Table 3, we list the main features supported by OWL for describing _indi-_
_viduals_ (e.g., Santiago, EID16), sometimes distinguished from classes and properties. First, we
can _assert_ (binary) relations between individuals using edges such as [Santa Lucía] city Santiago . In

the condition column, when we write _[𝑥]_ _𝑦_ _𝑧_, for example, we refer to the condition that the

given relation holds in the interpretation; if so, the interpretation _satisfies_ the axiom. OWL further

allows for defining relations to explicitly state that two terms refer to the _same_ entity, where, e.g.,

Región V same as Región de Valparaíso states that both refer to the same region (per Section 3.2); or that

two terms refer to _different_ entities, where, e.g., [Valparaíso] diff. from Región de Valparaíso distinguishes

the city from the region of the same name. We may also state that a relation does not hold using

_negation_, which can be serialised as a graph using a form of reification (see Figure 18a).


_4.1.3_ _Properties._ In Section 3.1.1, we already discussed how _subproperties_, _domains_ and _ranges_

may be defined for properties. OWL allows such definitions, and further includes other features,

as listed in Table 4. We may define a pair of properties to be _equivalent_, _inverses_, or _disjoint_ . We

can further define a particular property to denote a _transitive_, _symmetric_, _asymmetric_, _reflexive_, or

_irreflexive_ relation. We can also define the multiplicity of the relation denoted by properties, based

on being _functional_ (many-to-one) or _inverse-functional_ (one-to-many). We may further define a

_key_ for a class, denoting the set of properties whose values uniquely identify the entities of that

class. Without adopting a Unique Name Assumption (UNA), from these latter three features we

may conclude that two or more terms refer to the same entity. Finally, we can relate a property to

a _chain_ (a path expression only allowing concatenation of properties) such that pairs of entities


13Variations of the CWA can provide a middle ground between a completely open world that makes no assumption about

completeness, falsehood of unknown statements, or unicity of names. One example of such variation is Local Closed World

Assumption, already mentioned in Section 3.1.1.

14We use “iff” as an abbreviation for “if and only if” whereby “ _𝜙_ iff _𝜓_ ” can be read as “if _𝜙_ then _𝜓_ ” and “if _𝜓_ then _𝜙_ ”.


26


Table 3. Ontology features for individuals


**Feature** **Axiom** **Condition** **Example**

Assertion _𝑥_ _𝑦_ _𝑧_ _𝑥_ _𝑦_ _𝑧_ Chile capital Santiago
























|Col1|Neg|
|---|---|
|_𝑛_<br>sub<br>pre<br>obj<br>type|_𝑛_<br>sub<br>pre<br>obj<br>type|







Same As _𝑥_ 1 same as _𝑥_ 2 _𝑥_ 1 = _𝑥_ 2 Región V same as Región de Valparaíso

Different From _𝑥_ 1 diff. from _𝑥_ 2 _𝑥_ 1 ≠ _𝑥_ 2 Valparaíso diff. from Región de Valparaíso


Table 4. Ontology features for property axioms


**Feature** **Axiom** **Condition** (for all _𝑥_ ∗, _𝑦_ ∗, _𝑧_ ∗) **Example**

Subproperty _𝑝_ subp. of _𝑞_ _𝑥_ _𝑝_ _𝑦_ implies _[𝑥]_ _𝑞_ _𝑦_ venue subp. of location

Domain _𝑝_ domain _𝑐_ _𝑥_ _𝑝_ _𝑦_ implies _[𝑥]_ type _𝑐_ venue domain Event

Range _𝑝_ range _𝑐_ _𝑥_ _𝑝_ _𝑦_ implies _[𝑦]_ type _𝑐_ venue range Venue

Eqivalence _𝑝_ equiv. p. _𝑞_ _𝑥_ _𝑝_ _𝑦_ iff _[𝑥]_ _𝑞_ _𝑦_ start equiv. p. begins

Inverse _𝑝_ inv. of _𝑞_ _𝑥_ _𝑝_ _𝑦_ iff _[𝑦]_ _𝑞_ _𝑥_ venue inv. of hosts

Disjoint _𝑝_ disj. p. _𝑞_ not _[𝑥]_ _𝑝_ _𝑦_ venue disj. p. hosts

Transitive _𝑝_ type Transitive _𝑥_ _𝑝_ _𝑦_ _𝑝_ _𝑧_ implies _[𝑥]_ _𝑝_ _𝑧_ part of type Transitive

|𝑝|𝑧|
|---|---|
|||



Symmetric _𝑝_ type Symmetric _𝑥_ _𝑝_ _𝑦_ iff _[𝑦]_ _𝑝_ _𝑥_ nearby type Symmetric

Asymmetric _𝑝_ type Asymmetric not _[𝑥]_ _𝑝_ _𝑦_ capital type Asymmetric

Reflexive _𝑝_ type Reflexive _𝑥_ _𝑝_ part of type Reflexive

Irreflexive _𝑝_ type Irreflexive not _[𝑥]_ _𝑝_ flight type Irreflexive

Functional _𝑝_ type Functional _𝑦_ 1 _𝑝_ _𝑥_ _𝑝_ _𝑦_ 2 implies _[𝑦]_ 1 = _[𝑦]_ 2 population type Functional

Inv. Functional _𝑝_ type Inv. Functional _𝑥_ 1 _𝑝_ _𝑦_ _𝑝_ _𝑥_ 2 implies _[𝑥]_ 1 = _[𝑥]_ 2 capital type Inv. Functional



























related by the chain are also related by the given property. Note that for the latter two features in



Table 4 we require representing a list, denoted with a vertical notation



_..._ ; while such a list may be



serialised as a graph in a number of concrete ways, OWL uses RDF lists (see Figure 17).


27


_4.1.4_ _Classes._ In Section 3.1.1, we discussed how class hierarchies can be modelled using a _sub-class_

relation. OWL supports sub-classes, and many additional features, for defining and making claims

about classes; these additional features are summarised in Table 5. Given a pair of classes, OWL

allows for defining that they are _equivalent_, or _disjoint_ . Thereafter, OWL provides a variety of

features for defining novel classes by applying set operators on other classes, or based on conditions

that the properties of its instances satisfy. First, using set operators, one can define a novel class

as the _complement_ of another class, the _union_ or _intersection_ of a list (of arbitrary length) of other

classes, or as an _enumeration_ of all of its instances. Second, by placing restrictions on a particular

property _𝑝_, one can define classes whose instances are all of the entities that have: _some value_ from

a given class on _𝑝_ ; _all values_ from a given class on _𝑝_ ; [15] have a specific individual as a value on _𝑝_ ( _has_

_value_ ); have themselves as a reflexive value on _𝑝_ ( _has self_ ); have at least, at most or exactly some

number of values on _𝑝_ ( _cardinality_ ); and have at least, at most or exactly some number of values on

_𝑝_ from a given class ( _qualified cardinality_ ). For the latter two cases, in Table 5, we use the notation

“#{ [a] | _𝜙_ }” to count distinct entities satisfying _𝜙_ in the interpretation. These features can then be

combined to create more complex classes, where combining the examples for Intersection and

Has Self in Table 5 gives the definition: _self-driving taxis are taxis having themselves as a driver_ .


_4.1.5_ _Other features._ OWL supports other language features not previously discussed, including:

_annotation properties_, which provide metadata about ontologies, such as versioning info; _datatype_

_vs. object properties_, which distinguish properties that take datatype values from those that do not;

and _datatype facets_, which allow for defining new datatypes by applying restrictions to existing

datatypes, such as to define that places in Chile must have a _float between -66.0 and -110.0_ as their

value for the (datatype) property latitude. For more details we refer to the OWL 2 standard [239].

We will further discuss methodologies for the creation of ontologies in Section 6.5.


**4.2** **Semantics and Entailment**


The conditions listed in the previous tables indicate how each feature should be interpreted. These

conditions give rise to _entailments_, where, for example, in reference to the Symmetric feature

of Table 4, the definition [nearby] type Symmetric and edge [Santiago] nearby Santiago Airport entail
the edge [Santiago Airport] nearby Santiago according to the condition given for that feature. We now

describe how these conditions lead to entailments.


_4.2.1_ _Model-theoretic semantics._ Each axiom described by the previous tables, when added to a

graph, enforces some condition(s) on the interpretations that _satisfy_ the graph. The interpretations

that satisfy a graph are called _models_ of the graph. Were we to consider only the base condition of the

Assertion feature in Table 3, for example, then the models of a graph would be any interpretation

such that for every edge [x] y z in the graph, there exists a relation [x] y z in the model. Given

that there may be other relations in the model (under the OWA), the number of models of any such

graph is infinite. Furthermore, given that we can map multiple nodes in the graph to one entity

in the model (under the NUNA), any interpretation with (for example) the relation [a] a a is
a model of any graph so long as for every edge [x] y z in the graph, it holds that [x] = [y] = [z]

= [a] in the interpretation (in other words, the interpretation maps everything to [a] ). As we add

axioms with their associated conditions to the graph, we restrict models for the graph; for example,

considering a graph with two edges – [x] y z and [y] type Irreflexive - the interpretation with

a a a, [x] = [y] = ... = [a] is no longer a model as it breaks the condition for the irreflexive axiom.

15While something like flight ~~prop~~ DomesticAirport all NationalFlight might appear to be a more natural example for

All Values, this would be a modelling mistake, as the corresponding _for all_ condition is satisfied when no such node exists.

In other words, with this example definition, we could infer anything known not to have any flights to be a domestic airport.

(We could, however, define the intersection of this class and airport as being a domestic airport.)


28


Table 5. Ontology features for class axioms and definitions


**Feature** **Axiom** **Condition** (for all _𝑥_ ∗, _𝑦_ ∗, _𝑧_ ∗) **Example**

Subclass _𝑐_ subc. of _𝑑_ _𝑥_ type _𝑐_ implies _[𝑥]_ type _𝑑_ City subc. of Place

Eqivalence _𝑐_ equiv. c. _𝑑_ _𝑥_ type _𝑐_ iff _[𝑥]_ type _𝑑_ Human equiv. c. Person

Disjoint _𝑐_ disj. c. _𝑑_ not _[𝑐]_ type _𝑥_ type _𝑑_ City disj. c. Region

Complement _𝑐_ comp. _𝑑_ _𝑥_ type _𝑐_ iff not _[𝑥]_ type _𝑑_ Dead comp. Alive










|Col1|Col2|Col3|Col4|Col5|Col6|Col7|prop|Col9|
|---|---|---|---|---|---|---|---|---|
||||||||EUCitizen<br><br>prop|EUCitizen<br><br>prop|
|some|_𝑑_|_𝑥_<br>_𝑝_|_𝑎_<br>t|ype|_𝑑_|some|some|EUState|


|𝑝|Col2|Col3|Col4|
|---|---|---|---|
|_𝑑_<br>_𝑥_<br>_𝑐_<br>type<br>if<br>it holds that _𝑎_|type||_𝑑_|















nationality























Cardinality

_★_ ∈{= _,_ ≤ _,_ ≥}


|𝑝|Col2|Col3|Col4|Col5|Col6|Col7|
|---|---|---|---|---|---|---|
|_𝑛_<br>|.<br>#{ _𝑎_|||_𝑥_<br>_𝑝_||_𝑎_<br>}|_ ★𝑛_<br>Polyglot<br>≥<br>|





fluent














|Col1|body|
|---|---|
|BinaryStarSystem<br>class<br>=<br>prop|BinaryStarSystem<br>class<br>=<br>prop|



_4.2.2_ _Entailment._ We say that one graph _entails_ another if and only if any model of the former

graph is also a model of the latter graph. Intuitively this means that the latter graph says nothing

new over the former graph and thus holds as a logical consequence of the former graph. For example,

consider the graph [Santiago] type City subc. of Place and the graph [Santiago] type Place . All models
of the latter must have that [Santiago] type Place, but so must all models of the former, which must
have [Santiago] type City subc. of Place and further must satisfy the condition for Subclass, which
requires that [Santiago] type Place also hold. Hence we conclude that any model of the former graph

must be a model of the latter graph, or, in other words, the former graph entails the latter graph.

_4.2.3_ _If–then vs. if-and-only-if semantics._ Consider the graph [nearby] type Symmetric and the graph

nearby inv. of nearby . They result in the same semantic conditions being applied in the domain

graph, but does one entail the other? The answer depends on the semantics applied. Considering


29


the axioms and conditions of Tables 3, we can consider two semantics. Under if–then semantics –

if **Axiom** matches data graph then **Condition** holds in domain graph – the graphs do not entail

each other: though both graphs give rise to the same condition, this condition is not translated back

into the axioms that describe it. [16] Conversely, under if-and-only-if semantics – **Axiom** matches
data graph if-and-only-if **Condition** holds in domain graph – the graphs entail each other: both

graphs give rise to the same condition, which is translated back into all possible axioms that describe

it. Hence if-and-only-if semantics allows for entailing more axioms in the ontology language than

if–then semantics. OWL generally applies an if-and-only-if semantics [239].


**4.3** **Reasoning**


Unfortunately, given two graphs, deciding if the first entails the second – per the notion of entailment

we have defined and for all of the ontological features listed in Tables 3–5 – is _undecidable_ : no

(finite) algorithm for such entailment can exist that halts on all inputs with the correct true/false

answer [240]. However, we can provide practical reasoning algorithms for ontologies that (1) halt

on any input ontology but may miss entailments, returning false instead of true, (2) always halt

with the correct answer but only accept input ontologies with restricted features, or (3) only return

correct answers for any input ontology but may never halt on certain inputs. Though option (3) has

been explored using, e.g., theorem provers for First Order Logic [466], options (1) and (2) are more

commonly pursued using rules and/or Description Logics. Option (1) generally allows for more

efficient and scalable reasoning algorithms and is useful where data are incomplete and having

some entailments is valuable. Option (2) may be a better choice in domains – such as medical

ontologies – where missing entailments may have undesirable outcomes.


_4.3.1_ _Rules._ One of the most straightforward ways to provide automated access to deductive

knowledge is through _inference rules_ (or simply _rules_ ) encoding if–then-style consequences. A rule

is composed of a _body_ (if) and a _head_ (then). Both the body and head are given as graph patterns.

A rule indicates that if we can replace the variables of the body with terms from the data graph and

form a subgraph of a given data graph, then using the same replacement of variables in the head

will yield a valid entailment. The head must typically use a subset of the variables appearing in the

body to ensure that the conclusion leaves no variables unreplaced. Rules of this form correspond to

(positive) Datalog [85] in databases, Horn clauses [323] in logic programming, etc.

Rules can be used to capture entailments under ontological conditions. In Table 6, we list

some example rules for sub-class, sub-property, domain and range features [368]; these rules

may be considered incomplete, not capturing, for example, that every class is a sub-class of itself,

that every property is a sub-property of itself, etc. A more comprehensive set of rules for the

OWL features of Tables 3–5 have been defined as OWL 2 RL/RDF [363]; these rules are likewise

incomplete as such rules cannot fully capture negation (e.g., Complement), existentials (e.g., Some

Values), universals (e.g., All Values), or counting (e.g., Cardinality and Qualified Cardinality).

Other rule languages have, however, been proposed to support additional such features, including
existentials (see, e.g., Datalog [±] [36]), disjunction (see, e.g., Disjunctive Datalog [449]), etc.

Rules can be leveraged for reasoning in a number of ways. _Materialisation_ refers to the idea of

applying rules recursively to a graph, adding the conclusions generated back to the graph until a

fixpoint is reached and nothing more can be added. The materialised graph can then be treated as

any other graph. Although the efficiency and scalability of materialisation can be enhanced through

optimisations like Rete networks [164], or using distributed frameworks like MapReduce [531],

depending on the rules and the data, the materialised graph may become unfeasibly large to manage.

16Observe that nearby type Symmetric is a model of the first graph but not the second, while [nearby] inv. of nearby

is a model of the second graph but not the first. Hence neither graph entails the other.


30


_𝑂_ ( _𝑄_ ) : ( [?festival] type Festival ∪ [?festival] type Food Festival ∪ [?festival] type Drinks Festival )


Fig. 22. Query rewriting example for the query _𝑄_ of Figure 21


Table 6. Example rules for sub-class, sub-property, domain, and range features


**Feature** **Body** ⇒ **Head**

Subclass (I) ?x type ?c subc. of ?d ⇒ ?x type ?d

Subclass (II) ?c subc. of ?d subc. of ?e ⇒ ?c subc. of ?e

Subproperty (II) ?p subp. of ?q subp. of ?r ⇒ ?p subp. of ?r


Another strategy is to use rules for _query rewriting_, which given a query, will automatically extend

the query in order to find solutions entailed by a set of rules; for example, taking the schema graph

in Figure 12 and the rules in Table 6, the (sub-)pattern [?x] type Event in a given input query would

be rewritten to the following disjunctive pattern evaluated on the original graph:

?x type Event ∪ [?x] type Festival ∪ [?x] type Periodic Market ∪ [?x] venue ?y

