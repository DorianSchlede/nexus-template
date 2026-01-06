<!-- Source: 02-Knowledge_Graphs.pdf | Chunk 4/15 -->


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


Figure 22 provides a more complete example of an ontology that is used to rewrite the query of

Figure 21; if evaluated over the graph of Figure 1, [Ñam] will be returned as a solution. However,

not all of the aforementioned features of OWL can be supported in this manner. The OWL 2 QL

profile [363] is a subset of OWL designed specifically for query rewriting of this form [21].

While rules can be used to (partially) capture ontological entailments, they can also be defined

independently of an ontology language, capturing entailments for a given domain. In fact, some

rules – such as the following – cannot be captured by the ontology features previously seen, as they

do not support ways to infer relations from cyclical graph patterns (for computability reasons):


Various languages allow for expressing rules over graphs – independently or alongside of an

ontology language – including: Notation3 (N3) [42], Rule Interchange Format (RIF) [288], Semantic

Web Rule Language (SWRL) [254], and SPARQL Inferencing Notation (SPIN) [295].


_4.3.2_ _Description Logics._ Description Logics (DLs) were initially introduced as a way to formalise

the meaning of _frames_ [355] and _semantic networks_ [426]. Considering that semantic networks

are an early version of knowledge graphs, and the fact that DLs have heavily influenced the Web

Ontology Language, DLs thus hold an important place in the logical formalisation of knowledge


31


graphs. DLs form a family of logics rather than a particular logic. Initially, DLs were restricted

fragments of First Order Logic (FOL) that permit decidable reasoning tasks, such as entailment

checking [23]. Different DLs strike different balances between expressive power and computational

complexity of reasoning. DLs would later be extended with features that go beyond FOL but are

useful in the context of modelling graph data, such as transitive closure, datatypes, etc.

Description Logics are based on three types of elements: _individuals_, such as Santiago; _classes_
(aka _concepts_ ) such as City; and _properties_ (aka _roles_ ) such as flight. DLs then allow for making

claims, known as _axioms_, about these elements. _Assertional axioms_ can be either unary class

relations on individuals, such as City(Santiago), or binary property relations on individuals,
such as flight(Santiago,Arica). Such axioms form the _Assertional Box_ ( _A-Box_ ). DLs further

introduce logical symbols to allow for defining _class axioms_ (forming the _Terminology Box_, or

_T-Box_ for short), and _property axioms_ (forming the _Role Box_, _R-Box_ ); for example, the class axiom

City ⊑ Place states that the former class is a subclass of the latter one, while the property axiom
flight ⊑ connectsTo states that the former property is a subproperty of the latter one. DLs may

then introduce a rich set of logical symbols, not only for defining class and property axioms, but

also defining new classes based on existing terms; as an example of the latter, we can define a

class ∃nearby _._ Airport as the class of individuals that have some airport nearby. Noting that the
symbol ⊤ is used in DLs to denote the class of all individuals, we can then add a class axiom
∃flight _._ ⊤⊑∃nearby _._ Airport to state that individuals with an outgoing flight must have some
airport nearby. Noting that the symbol ⊔ can be used in DL to define that a class is the union of
other classes, we can further define that Airport ⊑ DomesticAirport ⊔ InternationalAirport,

i.e., that an airport is either a domestic airport or an international airport (or both).

The similarities between these DL features and the OWL features previously outlined in Tables 3–

5 are not coincidental: the OWL standard was heavily influenced by DLs, where, for example, the

OWL 2 DL language is a fragment of OWL restricted so that entailment becomes decidable. As an

example of a restriction, with DomesticAirport ⊑ = 1 destination ◦ country _._ ⊤, we can define
in DL syntax that domestic airports have flights destined to precisely one country (where p ◦ q

denotes a chain of properties). However, counting chains is often disallowed in DLs to ensure

decidability. In Appendix B.5.3, we present formal definitions for DL syntax and semantics, as well

as notions of entailment. For further reading, we also refer to the textbook by Baader et al. [23].

Expressive DLs support complex entailments involving existentials, universals, counting, etc.

A common strategy for deciding such entailments is to reduce entailment to _satisfiability_, which

decides if an ontology is consistent or not [253]. [17] Thereafter methods such as _tableau_ can be used

to check satisfiability, cautiously constructing models by completing them along similar lines to

the materialisation strategy previously described, but additionally branching models in the case of

disjunction, introducing new elements to represent existentials, etc. If any model is successfully

“completed”, the process concludes that the original definitions are satisfiable (see, e.g., [364]). Due

to their prohibitive computational complexity [363] – where for example, disjunction may lead to an

exponential number of branching possibilities – such reasoning strategies are not typically applied

in the case of large-scale data, though they may be useful when modelling complex domains.


**5** **INDUCTIVE KNOWLEDGE**


While deductive knowledge is characterised by precise logical consequences, inductively acquiring

knowledge involves generalising patterns from a given set of input observations, which can then be

used to generate novel but potentially imprecise predictions. For example, from a large data graph

with geographical and flight information, we may observe the pattern that almost all capital cities


17 _𝐺_ entails _𝐺_ ′ if and only if _𝐺_ ∪ not( _𝐺_ ′) is not satisfiable.


32


Inductive Knowledge


Supervised



Symbolic


Self-supervised



Unsupervised


Graph Analytics



Numeric


Self-supervised


Embeddings



GNNs



Rule Mining Axiom Mining



Fig. 23. Conceptual overview of popular inductive techniques for knowledge graphs in terms of
type of representation generated (Numeric/Symbolic) and type of paradigm used (Unsupervised/Selfsupervised/Supervised).

















































Fig. 24. Data graph representing transport routes in Chile


of countries have international airports serving them, and hence predict that if Santiago is a capital

city, it _likely_ has an international airport serving it; however, the predictions drawn from this pattern

do not hold for certain, where (e.g.) Vaduz, the capital city of Liechtenstein, has no (international)

airport serving it. Hence predictions will often be associated with a level of confidence; for example,

we may say that a capital has an international airport in [187]

195 [of cases, offering a confidence of]

0 _._ 959 for predictions made with that pattern. We then refer to knowledge acquired inductively

as _inductive knowledge_, which includes both the models used to encode patterns, as well as the

predictions made by those models. Though fallible, inductive knowledge can be highly valuable.

In Figure 23 we provide an overview of the inductive techniques typically applied to knowledge

graphs. In the case of unsupervised methods, there is a rich body of work on _graph analytics_, which

uses well-known functions/algorithms to detect communities or clusters, find central nodes and

edges, etc., in a graph. Alternatively, _knowledge graph embeddings_ can use self-supervision to learn

a low-dimensional numeric model of a knowledge graph that (typically) maps input edges to an

output _plausibility score_ indicating the likelihood of the edge being true. The structure of graphs

can also be directly leveraged for supervised learning, as explored in the context of _graph neural_

_networks_ . Finally, while the aforementioned techniques learn numerical models, _symbolic learning_

can learn symbolic models – i.e., logical formulae in the form of rules or axioms – from a graph in

a self-supervised manner. We now discuss each of the aforementioned techniques in turn.


**5.1** **Graph Analytics**

Analytics is the process of discovering, interpreting, and communicating meaningful patterns

inherent to (typically large) data collections. Graph analytics is then the application of analytical

processes to (typically large) graph data. The nature of graphs naturally lends itself to certain

types of analytics that derive conclusions about nodes and edges based on the _topology_ of the

graph, i.e., how the nodes of the graph are connected. Graph analytics hence draws many of its

techniques from related areas such as graph theory and network analysis, which have been used to


33


study graphs that represent social networks, the Web, internet routing, transportation networks,

ecosystems, protein–protein interactions, linguistic cooccurrences, and more besides [147].

Returning to the domain of our running example, the tourism board could use graph analytics

to extract knowledge about, for instance: key transport hubs that serve many tourist attractions

(centrality); groupings of attractions visited by the same tourists (community detection); attractions

that may become unreachable in the event of strikes or other route failures (connectivity), or

pairs of attractions that are similar to each other (node similarity). Given that such analytics will

require a complex, large-scale graph, for the purposes of illustration, in Figure 24 we present a more

concise example of some transportation connections in Chile directed towards popular touristic

destinations. We first introduce a selection of key techniques that can be applied for graph analytics.

We then discuss frameworks and languages that can be used to compute such analytics in practice.

Given that many traditional graph algorithms are defined for unlabelled graphs, we then describe

ways in which analytics can be applied over directed edge-labelled graphs. Finally we discuss the

potential connections between graph analytics and querying and reasoning.


_5.1.1_ _Techniques._ A wide variety of techniques can be applied for graph analytics. In the following

we will enumerate some of the main techniques – as recognised, for example, by the survey of Iosup

et al. [264] – that can be invoked in this setting.


  - _Centrality:_ aims to identify the most important (aka _central_ ) nodes or edges of a graph. Specific

node centrality measures include _degree_, _betweenness_, _closeness_, _Eigenvector_, _PageRank_, _HITS_,

_Katz_, among others. Betweenness centrality can also be applied to edges. A node centrality

measure would allow, e.g., to predict the transport hubs in Figure 24, while edge centrality

would allow us to find the edges on which many shortest routes depend for predicting traffic.

  - _Community detection:_ aims to identify _communities_ in a graph, i.e., sub-graphs that are

more densely connected internally than to the rest of the graph. Community detection

algorithms, such as _minimum-cut algorithms_, _label propagation_, _Louvain modularity_, etc.

enable discovering such communities. Community detection applied to Figure 24 may, for

example, detect a community to the left (referring to the north of Chile), to the right (referring

to the south of Chile), and perhaps also the centre (referring to cities with airports).

  - _Connectivity:_ aims to estimate how well-connected the graph is, revealing, for instance, the

resilience and (un)reachability of elements of the graph. Specific techniques include measuring

_graph density_ or _𝑘-connectivity_, detecting _strongly connected components_ and _weakly connected_

_components_, computing _spanning trees_ or _minimum cuts_, etc. In the context of Figure 24,

such analysis may tell us that routes to [Grey Glacier], [Osorno Volcano] and [Piedras Rojas] are the most
“brittle”, becoming disconnected if one of two bus routes fail.

  - _Node similarity:_ aims to find nodes that are similar to other nodes by virtue of how they

are connected within their neighbourhood. Node similarity metrics may be computed us
ing _structural equivalence_, _random walks_, _diffusion kernels_, etc. These methods provide an

understanding of what connects nodes, and, thereafter, in what ways they are similar. In the

context of Figure 24, such analysis may tell us that [Calama] and [Arica] are similar nodes based

on both having return flights to [Santiago] and return buses to [San Pedro] .


While the previous techniques accept a graph alone as input, [18] other forms of graph analytics may

further accept a node, a pair of nodes, etc., along with the graph.


18Node similarity can be run over an entire graph to find the _𝑘_ most similar nodes for each node, or can also be run

for a specific node to find its most similar nodes. There are also measures for graph similarity (based on, e.g., frequent

itemsets [334]) that accept multiple graphs as input.


34


  - _Path finding:_ aims to find paths in a graph, typically between pairs of nodes given as input.

Various technical definitions exist that restrict the set of valid paths between such nodes,

including simple paths that do not visit the same node twice, shortest paths that visit the

fewest number of edges, or – as previously discussed in Section 2.2 – regular path queries that

restrict the labels of edges that can be traversed by the path [16]. We could use such algorithms

to find, for example, the shortest path(s) in Figure 24 from [Torres del Paine] to [Moon Valley] .


Most such techniques have been proposed and studied for simple graphs or directed graphs without

edge labels. We will discuss their application to more complex graph models – and how they can

be combined with other techniques such as reasoning and querying – later in Section 5.1.3.


_5.1.2_ _Frameworks._ Various frameworks have been proposed for large-scale graph analytics, often

in a distributed (cluster) setting. Amongst these we can mention Apache Spark (GraphX) [119, 563],

GraphLab [326], Pregel [335], Signal–Collect [503], Shark [564], etc. These _graph parallel frameworks_

apply a _systolic abstraction_ [304] based on a directed graph, where nodes are processors that can

send messages to other nodes along edges. Computation is then iterative, where in each iteration,

each node reads messages received through inward edges (and possibly its own previous state),

performs a computation, and then sends messages through outward edges based on the result.

These frameworks then define the systolic computational abstraction on top of the data graph

being processed: nodes and edges in the data graph become nodes and edges in the systolic graph.

We refer to Appendix B.6.1 for more formal details on graph parallel frameworks.

To take an example, assume we wish to compute the places that are most (or least) easily reached

by the routes shown in the graph of Figure 24. A good way to measure this is using centrality,

where we choose PageRank [391], which computes the probability of a tourist randomly following

the routes shown in the graph being at a particular place after a given number of “hops”. We can

implement PageRank on large graphs using a graph parallel framework. In Figure 25, we provide

an example of an iteration of PageRank for an illustrative sub-graph of Figure 24. The nodes are

initialised with a score of 1 [1]
| _𝑉_ | [=] 6 [, where we assume the tourist to have an equal chance of starting]



at any point. In the _message phase_ (Msg), each node _𝑣_ passes a score of _[𝑑]_ | _𝐸_ [R] _[𝑖]_ ( _𝑣_ [(] _[𝑣]_ ) | [)] [on each of its outgoing]


edges, where we denote by _𝑑_ a constant damping factor used to ensure convergence (typically

_𝑑_ = 0 _._ 85, indicating the probability that a tourist randomly “jumps” to any place), by R _𝑖_ ( _𝑣_ ) the score
of node _𝑣_ in iteration _𝑖_ (the probability of the tourist being at node _𝑣_ after _𝑖_ hops), and by | _𝐸_ ( _𝑣_ )|

the number of outgoing edges of _𝑣_ . The aggregation phase (Agg) for _𝑣_ then sums all incoming
messages received along with its constant share of the damping factor ( [1] | _𝑉_ [−] _[𝑑]_ | [) to compute][ R] _[𝑖]_ [+][1][(] _[𝑣]_ [)][.]


We then proceed to the message phase of the next iteration, continuing until some termination

criterion is reached (e.g., iteration count or residual threshold, etc.) and final scores are output.

While the given example is for PageRank, the systolic abstraction is general enough to support

a wide variety of graph analytics, including those previously mentioned. An algorithm in this

framework consists of the functions to compute message values in the _message phase_ (Msg), and

to accumulate the messages in the aggregation phase (Agg). The framework will take care of

distribution, message passing, fault tolerance, etc. However, such frameworks – based on message

passing between neighbours – have limitations: not all types of analytics can be expressed in such

frameworks [565]. [19] Hence frameworks may allow additional features, such as a _global step_ that

performs a global computation on all nodes, making the result available to each node [335]; or a

_mutation step_ that allows for adding or removing nodes and edges during processing [335].


19Formally Xu et al. [565] have shown that such frameworks are as powerful as the (incomplete) Weisfeiler–Lehman (WL)

graph isomorphism test – based on recursively hashing neighbouring hashes – for distinguishing graph structures.


35


Fig. 25. Example of a systolic iteration of PageRank for a sample sub-graph of Figure 24


_5.1.3_ _Analytics on data graphs._ As aforementioned, most analytics presented thus far are, in their

“native” form, applicable for undirected or directed graphs without the _edge meta-data_ - i.e., edge

labels or property–value pairs – typical of graph data models. [20] A number of strategies can be

applied to make data graphs subject to analytics of this form:


  - _Projection_ involves simply “projecting” an undirected or directed graph by optionally selecting

a sub-graph from the data graph from which all edge meta-data are dropped; for example,

Figure 25 may be the result of extracting the sub-graph induced by the edge labels bus and
flight from a larger data graph, where the labels are then dropped to create a directed graph.

  - _Weighting_ involves converting edge meta-data into numerical values according to some

function. Many of the aforementioned techniques are easily adapted to the case of weighted

(directed) graphs; for example, we could consider weights on the graph of Figure 25 denoting

trip duration (or price, traffic, etc.), and then compute the shortest paths adding the duration

of each leg. [21] In the absence of external weights, we may rather map edge labels to weights,

assigning the same weight to all flight edges, to all bus edges, etc., based on some criteria.

  - _Transformation_ involves transforming the graph to a lower arity model. A transformation may

be _lossy_, meaning that the original graph cannot be recovered; or _lossless_, meaning that the

original graph can be recovered. Figure 26 provides an example of a lossy and lossless trans
formation from a directed edge-labelled graph to directed graphs. In the lossy transformation,

we cannot tell, for example, if the original graph contained the edge [Iquique] flight Santiago or
Iquique flight Arica, etc. The lossless transformation must introduce new nodes (similar to

reification) to maintain information about directed labelled edges. Both transformed graphs

further attempt to preserve the directionality of the original graph.

  - _Customisation_ involves changing the analytical procedure to incorporate edge meta-data,

such as was the case for path finding based on path expressions. Other examples might

include structural measures for node similarity that not only consider common neighbours,

but also common neighbours connected by edges with the same label, or aggregate centrality

measures that capture the importance of edges grouped by label, etc.

The results of an analytical process may change drastically depending on which of the previous

strategies are chosen to prepare the data for analysis. This choice may be a non-trivial one to make


20We remark that in the case of property graphs, property–value pairs on nodes can be converted by mapping values to

nodes and properties to edges with the corresponding label.

21Other forms of analytics are possible if we assume the graph is weighted; for example, if we annotated the graph of

Figure 25 with probabilities of tourists moving from one place to the next, we could leverage _Markov processes_ to understand

features such as reducibility, periodicity, transience, recurrence, ergodicity, steady-states, etc., of the routes [138].


36


(a) Original graph



(b) Lossy transformation











(c) Lossless transformation



Fig. 26. Transformations from a directed edge-labelled graph to a directed graph


_a priori_ and may require empirical validation. More study is required to more generally understand

the effects of such strategies on the results of different analytical techniques.


_5.1.4_ _Analytics with queries._ As discussed in Section 2.2, various languages for querying graphs

have been proposed [16]. One may consider a variety of ways in which query languages and

analytics can complement each other. First, we may consider using query languages to project or

transform a graph suitable for a particular analytical task, such as to extract the graph of Figure 24

from a larger data graph. Query languages such as SPARQL [217], Cypher [165], and G-CORE [15]

allow for outputting graphs, where such queries can be used to select sub-graphs for analysis. These

languages can also express some limited (non-recursive) analytics, where aggregations can be used

to compute degree centrality, for example; they may also have some built-in analytical support,

where, for example, Cypher [165] allows for finding shortest paths. In the other direction, analytics

can contribute to the querying process in terms of _optimisations_, where, for example, analysis of

connectivity may suggest how to better distribute a large data graph over multiple machines for

querying using, e.g., _minimum cuts_ [7, 268]. Analytics have also been used to _rank_ query results

over large graphs [151, 544], selecting the most important results for presentation to the user.

In some use-cases we may further wish to interleave querying and analytical processes. For

example, from the full data graph collected by the tourist board, consider an upcoming airline strike

where the board wishes to find _the events during the strike with venues in cities unreachable from_

_Santiago by public transport due to the strike_ . Hypothetically, we could use a query to extract the

transport network excluding the airline’s routes (assuming, per Figure 3 that the airline information

is available), use analytics to extract the strongly connected component containing Santiago, and

finally use a query to find events in cities not in the Santiago component on the given dates. [22] While

one could solve this task using an imperative language such as Gremlin [445], GraphX [563], or

R [518], more declarative languages are also being explored to more easily express such tasks, with

proposals including the extension of graph query languages with recursive capabilities [47, 439], [23]


combining linear algebra with relational (query) algebra [258], and so forth.


_5.1.5_ _Analytics with entailment._ Knowledge graphs are often associated with a semantic schema

or ontology that defines the semantics of domain terms, giving rise to entailments (per Section 4).

Applying analytics with or without such entailments – e.g., before or after materialisation – may

yield radically different results. For example, observe that an edge [Santa Lucía] hosts EID15 is semantically equivalent to an edge [EID15] venue Santa Lucía once the inverse axiom [hosts] inv. of venue is


22Such a task could not be solved in a single query using regular path queries as such expressions would not be capable of

filtering edges representing flights of a particular airline.

23Recursive query languages become Turing complete assuming one can also express operations on binary arrays.


37


invoked; however, these edges are far from equivalent from the perspective of analytical techniques

that consider edge direction, for which including one type of edge, or the other, or both, may have

a major bearing on the final results. To the best of our knowledge, the combination of analytics

and entailment has not been well-explored, leaving open interesting research questions. Along

these lines, it may be of interest to explore _semantically-invariant analytics_ that yield the same

results over semantically-equivalent graphs (i.e., graphs that entail one another), thus analysing

the semantic content of the knowledge graph rather than simply the topological features of the

data graph; for example, semantically-invariant analytics would yield the same results over a graph

containing the inverse axiom [hosts] inv. of venue and a number of hosts edges, the same graph but
where every hosts edge is replaced by an inverse venue edge, and the union of both graphs.


**5.2** **Knowledge Graph Embeddings**

Methods for machine learning have gained significant attention in recent years. In the context

of knowledge graphs, machine learning can either be used for directly _refining_ a knowledge

graph [400] (discussed further in Section 8); or for _downstream tasks_ using the knowledge graph,

such as recommendation [575], information extraction [533], question answering [255], query

relaxation [548], query approximation [215], etc. (discussed further in Section 10). However, many

traditional machine learning techniques assume dense numeric input representations in the form

of vectors, which is quite distinct from how graphs are usually expressed. So how can graphs – or

nodes, edges, etc., thereof – be encoded as numeric vectors?

A first attempt to represent a graph using vectors would be to use a _one-hot encoding_, generating

a vector for each node of length | _𝐿_ | · | _𝑉_ | – with | _𝑉_ | the number of nodes in the input graph and | _𝐿_ |

the number of edge labels – placing a one at the corresponding index to indicate the existence of

the respective edge in the graph, or zero otherwise. Such a representation will, however, typically

result in large and sparse vectors, which will be detrimental for most machine learning models.

The main goal of knowledge graph embedding techniques is to create a dense representation of

the graph (i.e., _embed_ the graph) in a continuous, low-dimensional vector space that can then be

used for machine learning tasks. The dimensionality _𝑑_ of the embedding is fixed and typically low

(often, e.g., 50 ≥ _𝑑_ ≥ 1000). Typically the graph embedding is composed of an _entity embedding_
for each node: a vector with _𝑑_ dimensions that we denote by e; and a _relation embedding_ for each
edge label: (typically) a vector with _𝑑_ dimensions that we denote by r. The overall goal of these

vectors is to abstract and preserve latent structures in the graph. There are many ways in which

this notion of an embedding can be instantiated. Most commonly, given an edge [s] p -, a specific
embedding approach defines a _scoring function_ that accepts es (the entity embedding of node [s] ), rp
(the entity embedding of edge label p) and eo (the entity embedding of node [o] ) and computes the

_plausibility_ of the edge: how likely it is to be true. Given a data graph, the goal is then to compute

the embeddings of dimension _𝑑_ that maximise the plausibility of positive edges (typically edges in

the graph) and minimise the plausibility of negative examples (typically edges in the graph with a

node or edge label changed such that they are no longer in the graph) according to the given scoring

function. The resulting embeddings can then be seen as models learnt through self-supervision

that encode (latent) features of the graph, mapping input edges to output plausibility scores.

Embeddings can then be used for a number of low-level tasks involving the nodes and edge-labels

of the graph from which they were computed. First, we can use the plausibility scoring function to

assign a confidence to edges that may, for example, have been extracted from an external source

(discussed later in Section 6). Second, the plausibility scoring function can be used to complete edges

with missing nodes/edge labels for the purposes of link prediction (discussed later in Section 8);

for example, in Figure 24, we might ask which nodes in the graph are likely to complete the edge


38


|Antofagasta|Col2|
|---|---|
|nort|h of|














|Santiago|Col2|
|---|---|
|nort|h of|





(c) Entity embeddings



(a) Original graph



(b) Relation embeddings



Fig. 27. Toy example of two-dimensional relation and entity embeddings learnt by TransE; the entity embeddings use abbreviations and include an example of vector addition to predict what is west of Antofagasta

Grey Glacier bus ?, where – aside from [Punta Arenas], which is already given – we might intuitively

expect [Torres del Paine] to be a plausible candidate. Third, embedding models will typically assign

similar vectors to similar nodes and similar edge-labels, and thus they can be used as the basis of

similarity measures, which may be useful for finding duplicate nodes that refer to the same entity,

or for the purposes of providing recommendations (discussed later in Section 10).

A wide range of knowledge graph embedding techniques have been proposed [549]. Our goal here

is to provide a high-level introduction to some of the most popular techniques proposed thus far. First

we discuss _translational models_ that adopt a geometric perspective whereby relation embeddings

translate subject entities to object entities in the low-dimensional space. We then describe _tensor_

_decomposition models_ that extract latent factors approximating the graph’s structure. Thereafter

we discuss _neural models_ that use neural networks to train embeddings that provide accurate

plausibility scores. Finally, we discuss _language models_ that leverage existing word embedding

techniques, proposing ways of generating graph-like analogues for their expected (textual) inputs.

A more formal treatment of these models is provided in Appendix B.6.2.


_5.2.1_ _Translational models. Translational models_ interpret edge labels as transformations from

subject nodes (aka the _source_ or _head_ ) to object nodes (aka the _target_ or _tail_ ); for example, in the

edge [San Pedro] bus Moon Valley, the edge label bus is seen as transforming [San Pedro] to [Moon Valley],
and likewise for other bus edges. The most elementary approach in this family is TransE [63].
Over all positive edges [s] p -, TransE learns vectors es, rp, and eo aiming to make es + rp as
close as possible to eo. Conversely, if the edge is a negative example, TransE attempts to learn a
representation that keeps es + rp away from eo. To illustrate, Figure 27 provides a toy example
of two-dimensional ( _𝑑_ = 2) entity and relation embeddings computed by TransE. We keep the
orientation of the vectors similar to the original graph for clarity. For any edge [s] p - in the
original graph, adding the vectors es + rp should approximate eo. In this toy example, the vectors
correspond precisely where, for instance, adding the vectors for [Licantén] (eL.) and west of (rwo.)
gives a vector corresponding to [Curico] (eC.). We can use these embeddings to predict edges (among
other tasks); for example, in order to predict which node in the graph is most likely to be west of

Antofagasta (A.), by computing eA. + rwo. we find that the resulting vector (dotted in Figure 27c) is
closest to eT., thus predicting [Toconao] (T.) to be the most _plausible_ such node.
Aside from this toy example, TransE can be too simplistic; for example, in Figure 24, bus not
only transforms [San Pedro] to [Moon Valley], but also to [Arica], [Calama], and so forth. TransE will, in this

case, aim to give similar vectors to all such target locations, which may not be feasible given other


39


edges. TransE will also tend to assign cyclical relations a zero vector, as the directional components

will tend to cancel each other out. To resolve such issues, many variants of TransE have been

investigated. Amongst these, for example, TransH [553] represents different relations using distinct

hyperplanes, where for the edge [s] p -, [s] is first projected onto the hyperplane of p before the

translation to [o] is learnt (uninfluenced by edges with other labels for [s] and for [o] ). TransR [318]
generalises this approach by projecting [s] and [o] into a vector space specific to p, which involves
multiplying the entity embeddings for [s] and [o] by a projection matrix specific to p. TransD [271]

simplifies TransR by associating entities and relations with a second vector, where these secondary

vectors are used to project the entity into a relation-specific vector space. Recently, RotatE [511]

proposes translational embeddings in complex space, which allows to capture more characteristics

of relations, such as direction, symmetry, inversion, antisymmetry, and composition. Embeddings

have also been proposed in non-Euclidean space, e.g., MuRP [29] uses relation embeddings that

transform entity embeddings in the hyperbolic space of the Poincaré ball mode, whose curvature

provides more “space” to separate entities with respect to the dimensionality. For discussion of

other translational models, we refer to the survey by Wang et al. [549].


_5.2.2_ _Tensor decomposition models._ A second approach to derive graph embeddings is to apply

methods based on _tensor decomposition_ . A _tensor_ is a multidimensional numeric field that generalises

scalars (0-order tensors), vectors (1-order tensors) and matrices (2-order tensors) towards arbitrary

dimension/order. Tensors have become a widely used abstraction for machine learning [427].

Tensor decomposition involves decomposing a tensor into more “elemental” tensors (e.g., of lower

order) from which the original tensor can be recomposed (or approximated) by a fixed sequence of

basic operations. These elemental tensors can be viewed as capturing _latent factors_ underlying the

information contained in the original tensor. There are many approaches to tensor decomposition,

where we will now briefly introduce the main ideas behind _rank decompositions_ [427].

Leaving aside graphs momentarily, consider an ( _𝑎,𝑏_ )-matrix (i.e., a 2-order tensor) C, where _𝑎_ is
the number of cities in Chile, _𝑏_ is the number of months in a year, and each element (C) _𝑖𝑗_ denotes
the average temperature of the _𝑖_ [th] city in the _𝑗_ [th] month. Noting that Chile is a long, thin country

- ranging from subpolar climates in the south, to a desert climate in the north – we may find a

decomposition of C into two vectors representing latent factors – specifically x (with _𝑎_ elements)
giving lower values for cities with lower latitude, and y (with _𝑏_ elements), giving lower values for
months with lower temperatures – such that computing the outer product [24] of the two vectors

approximates C reasonably well: x ⊗ y ≈ C. In the (unlikely) case that there exist vectors x and y
such that C is precisely the outer product of two vectors (x ⊗ y = C) we call C a rank-1 matrix;
we can then precisely encode C using _𝑎_ + _𝑏_ values rather than _𝑎_ × _𝑏_ values. Most times, however,
to get precisely C, we will need to sum multiple rank-1 matrices, where the rank _𝑟_ of C is the
minimum number of rank-1 matrices that need to be summed to derive precisely C, such that
x1 ⊗ y1 + _. . ._ x _𝑟_ ⊗ y _𝑟_ = C. In the temperature example, x2 ⊗ y2 might correspond to a correction for
altitude, x3 ⊗ y3 for higher temperature variance further south, etc. A (low) rank decomposition
of a matrix then sets a limit _𝑑_ on the rank and computes the vectors (x1 _,_ y1 _, . . .,_ x _𝑑,_ y _𝑑_ ) such that
x1 ⊗ y1 + _. . ._ + x _𝑑_ ⊗ y _𝑑_ gives the best _𝑑_ -rank approximation of C. Noting that to generate _𝑛_ -order

tensors we need to compute the outer product of _𝑛_ vectors, we can generalise this idea towards low
