<!-- Source: 02-Knowledge_Graphs.pdf | Chunk 13/15 -->



Moving to the 00’s, Jiang and Ma (2002) [273] introduce the notion of “plan knowledge graphs”

where nodes represent goals and edges dependencies between goals, further encoding supporting

degrees that can change upon further evidence. Search algorithms are then defined on the graph

to determine a plan for a particular goal. Helms and Buijsrogge (2005) [232] propose a knowl
edge graph to represent the flow of knowledge in an organisation, with nodes representing

knowledge actors (creators, sharers, users), edges representing knowledge flow from one actor

to another, and edge weights indicating the “velocity” (delay of flow) and “viscosity” (the depth

of knowledge transferred). Graph algorithms are then proposed to find bottlenecks in knowl
edge flow. Kasneci et al. (2008) [280] propose a search engine for knowledge graphs, defined to

be weighted directed edge-labelled graphs, where weights denote confidence scores based on the

centrality of source documents from which the edge/relation was extracted. From the same group,

Elbassuoni et al. (2009) [142] adopt a similar notion of a knowledge graph, adding edge attributes

to include keywords from the source, a count of supporting sources, etc., showing how the graph

can be queried. Coursey and Mihalcea (2009) [106] construct a knowledge graph from Wikipedia,

where nodes represent Wikipedia articles and categories, while edges represent the proximity of

nodes. Subsequently, given an input text, entity linking and centrality measures are applied over

the knowledge graph to determine relevant Wikipedia categories for the text.

Concluding with the 10’s (prior to 2012), Pechsiri and Piriyakul (2010) [403] use knowledge

graphs to capture “explanation knowledge” – the knowledge of why something is the way it is – by

representing events as nodes and causal relationships as edges, claiming that this graphical notation

offers intuitive explanations to users; their work focuses on extracting such knowledge graphs from

text. Corby and Faron-Zucker (2010) [101] use the phrase “knowledge graph” in a general way to

denote any graph encoding knowledge, proposing an abstract machine for querying such graphs.

Other phrases were used to represent similar notions by other authors, including “information

graphs” [303], “information networks” [510], “knowledge networks” [91], as well as “semantic

networks” [66, 373, 557] and “conceptual graphs” [490], as mentioned previously. Here we exclu
sively considered works that (happen to) use the phrase “knowledge graph” prior to Google’s

announcement of their knowledge graph in 2012, where we see that many works had independently

coined this phrase for different purposes. Similar to the current practice, all of the works of this

period consider a knowledge graph to be formed of a set of nodes denoting entities of interest and

a set of edges denoting relations between those entities, with different entities and relations being

considered in different works. Some works add extra elements to these knowledge graphs, such as

edge weights, edge labels, or other meta-data [142]. Other trends include knowledge acquisition

from experts [129, 331, 428] and knowledge extraction from text [27, 242, 266, 501], combinations

of symbolic and inductive methods [121, 331, 461, 480], as well as the use of rules [433], ontolo
gies [242], graph analytics [232, 280, 495], learning [121, 428, 461, 480], and so forth. Later papers

(2008–2010) by Kasneci et al. [280], Elbassuoni et al. [142], Coursey and Mihalcea [106] and Corby

and Faron-Zucker [101] introduce notions of knowledge graph similar to current practice.

However, some trends are not reflected in current practice. Of particular note, quite a lot of

the knowledge graphs defined in this period consider edges as denoting a form of dependence or

causality, where _[𝑥]_ _𝑦_ may denote that _𝑥_ is a prerequisite for _𝑦_ [273, 337, 465] or that _𝑥_ leads to

_𝑦_ [27, 273, 331, 428, 433, 480]. In some cases and–or graphs are used to denote conjunctions or

disjunctions of such relations [331], while in other cases edges are weighted to assign a belief to a

relation [273, 331, 428]. In addition, papers from 1970–2000 tend to have worked with small graphs,

which contrasts with modern practice where knowledge graphs can reach scales of millions or

billions of nodes [387]: during this period, computational resources were more limited [465], and

fewer sources of structured data were readily available meaning that the knowledge graphs were

often sourced solely from human experts [129, 331, 428] or from text [27, 242, 266, 501].


110


**A.3** **“Knowledge Graphs”: 2012 Onwards**


Google Knowledge Graph was announced in 2012 [484]. This initial announcement was targeted at

a broad audience, mainly motivating the knowledge graph and describing applications that it would

enable, where the knowledge graph itself is described as “ _[a graph] that understands real-world_

_entities and their relationships to one another_ ” [484]. Mentions of “knowledge graphs” quickly gained

momentum in the research literature from that point. As noted by Bergman [40], this announcement

by Google was a watershed moment in terms of adopting the phrase “knowledge graph”. However,

given the informal nature of the announcement, a technical definition was lacking [57, 141].

Given that knowledge graphs were gaining more and more attention in the academic literature,

formal definitions were becoming a necessity in order to precisely characterise what they were,

how they were structured, how they could be used, etc., and more generally to facilitate their study

in a precise manner. We can determine four general categories of definitions.


_Category I_ : The first category simply defines the knowledge graph as a graph where nodes represent

entities, and edges represent relationships between those entities. Often a directed edge
labelled graph is assumed (or analogously, a set of binary relations, or a set of triples). This

simple and direct definition was popularised by some of the seminal papers on knowledge

graph embeddings [318, 553] (2014–2015), being sufficient to represent the data structure

upon which these embeddings would operate. As reflected in the survey by Wang et al. [549],

the multitude of works that would follow on knowledge graph embeddings have continued

to use this definition. Though simple, the _Category I_ definition raises some doubts: How is a

knowledge graph different from a graph (database)? Where does knowledge come into play?

_Category II_ : A second common definition goes as follows: “ _a knowledge graph is a graph-structured_

_knowledge base_ ”, where, to the best of our knowledge, the earliest usages of this definition

in the academic literature were by Nickel et al. [384] (2016) and Seufert et al. (2016) [474]

(interestingly in the formal notation of these initial papers, a knowledge graph is defined

analogously to a directed edge-labelled graph). Such a definition raises the question: what,

then is a “knowledge base”? The phrase “knowledge base” was popularised in the 70’s

(possibly earlier) in the context of rule-based expert systems [72], and later were used in

the context of ontologies and other logical formalisms [68]. The follow-up question then is

whether or not one can have a knowledge base (graph-structured or not) without a logical

formalism while staying true to the original definitions. Looking in further detail, similar

ambiguities have also existed regarding the definition of a “knowledge base” (KB). Of note:

Brachman and Levesque (1986) [67] – reporting after a workshop on this issue – state that

“ _if we ask what the KB tells us about the world, we are asking about its Knowledge Level_ ”.

_Category III_ : The third category of definitions outline additional, technical characteristics that a

“knowledge graph” should comply with, where we list some prominent definitions.


**–** In an influential survey on knowledge graph refinement, Paulheim [400] lists four crite
ria that characterise the knowledge graphs considered for the paper. Specifically, that a

knowledge graph “ _mainly describes real world entities and their interrelations, organized in_

_a graph; defines possible classes and relations of entities in a schema; allows for potentially_

_interrelating arbitrary entities with each other; covers various topical domains_ ”; he thus rules

out ontologies without instances (e.g., DOLCE) and graphs of word senses (e.g., WordNet) as

not meeting the first two criteria, while relational databases do not meet the third criterion

(due to schema restrictions), and domain-specific graphs (e.g., Geonames) are considered

to not meet the fourth criterion; this leaves graphs such as DBpedia, YAGO, Freebase, etc.


111


**–** Ehrlinger and Wöß [141] also review definitions of “knowledge graph”, where they criticise

the _Category II_ definitions based on the argument that knowledge bases are often synony
mous with ontologies [38], while knowledge graphs are not; they further criticise Google

for calling its knowledge graph a “knowledge base”. After reviewing prior definitions of

terms such as “knowledge base”, “ontology”, and “knowledge graph”, they propose their

definition: “ _A knowledge graph acquires and integrates information into an ontology and_

_applies a reasoner to derive new knowledge_ ”. In the subsequent discussion, they remark that

a knowledge graph is distinguished from an ontology (considered synonymous with a

knowledge base) by the provision of reasoning capabilities.

**–** One of the most detailed technical definitions for a “knowledge graph” is provided by Bel
lomarini et al. [35], who state: “ _A knowledge graph is a semi-structured data model charac-_

_terized by three components: (i) a ground extensional component, that is, a set of relational_

_constructs for schema and data (which can be effectively modeled as graphs or generalizations_

_thereof); (ii) an intensional component, that is, a set of inference rules over the constructs of_

_the ground extensional component; (iii) a derived extensional component that can be produced_

_as the result of the application of the inference rules over the ground extensional component_

_(with the so-called “reasoning” process)._ ” They remark that ontologies and rules represent

analogous structures, and that a knowledge graph is then a knowledge base extended with

reasoning along similar lines to the definition provided by Ehrlinger and Wöß [141].

We refer to Bergman [40] for a list of further definitions that fit this category. While having

a specific, technical definition for knowledge graphs provides a more solid grounding for

their study, as Bergman [40] remarks, many of these definitions do not seem to fit the current

practice of knowledge graphs. For example, it is not clear which of these definitions the

Google Knowledge Graph itself – responsible for popularising the idea – would meet (if

any). Furthermore, many of the criteria proposed by such definitions are orthogonal to the

multitude of works in the area of knowledge graph embeddings [549].

_Category IV_ : While the previous three categories involve (sometimes conflicting) intensional defi
nitions, the fourth category adopts an extensional definition of knowledge graphs, defining

them by example. Knowledge graphs are then characterised by examples such as DBpedia,

Google’s Knowledge Graph, Freebase, YAGO, amongst others [57]. Arguably this category

sidesteps the issue of defining a knowledge graph, rather than providing such a definition.

These categories refer to definitions that have appeared in the academic literature. In terms of

enterprise knowledge graphs, an important reference is the paper of Noy et al. [387], which has

been co-authored by leaders of knowledge graph projects from eBay, Facebook, Google, IBM, and

Microsoft, and thus can be seen as representing a form of consensus amongst these companies on

what is a knowledge graph — a concept these companies have played a key role in popularising.

Specifically this paper states that “ _a knowledge graph describes objects of interest and connections_

_between them_ ”, and goes on to state that “ _many practical implementations impose constraints on the_

_links in knowledge graphs by defining a schema or ontology_ ”. They later add “ _Knowledge graphs and_

_similar structures usually provide a shared substrate of knowledge within an organization, allowing_

_different products and applications to use similar vocabulary and to reuse definitions and descriptions_

_that others create. Furthermore, they usually provide a compact formal representation that developers_

_can use to infer new facts and build up the knowledge_ ”. We interpret this definition as corresponding

to _Category I_, but further acknowledging that while not a necessary condition for a knowledge

graph, ontologies and formal representations _usually_ play a key role. The definition we provide at

the outset of the paper is largely compatible with that of Noy et al. [387].


38Prior definitions of an ontology – such as by Guarino et al. [204] – would seem to contradict this conclusion.


112


**B** **FORMAL DEFINITIONS**


In order to keep the discussion as accessible as possible, the body of the paper uses example-driven

explanations of the main concepts and techniques associated with knowledge graphs. In this section,

we complement the discussion of the paper with formal definitions.


**B.1** **Data Graph Models**


We define the graph data models in line with previous conventions (e.g., [16]). While different types

of constants may be used in different models (e.g., RDF allows IRIs and literals), these definitions

use a single (countably) infinite set of constants denoted Con. (We thus also abstract away from

issues that are not exigent for the current introductory discussion, such as the existential semantics

of blank nodes in RDF [247], _𝐷_ -entailment over literals [223], positional restrictions [111], etc.)


_B.1.1_ _Directed edge-labelled graph._ We first provide definitions for a directed edge-labelled graph.


_Definition B.1 (Directed edge-labelled graph)._ A _directed edge-labelled graph_ is a tuple _𝐺_  
( _𝑉, 𝐸, 𝐿_ ), where _𝑉_ ⊆ Con is a set of nodes, _𝐿_ ⊆ Con is a set of edge labels, and _𝐸_ ⊆ _𝑉_ × _𝐿_ × _𝑉_ is a

set of edges.


_Example B.2._ In reference to Figure 1, the set of nodes _𝑉_ has 15 elements, including Arica, EID16,
etc. The set of edges _𝐸_ has 23 triples, including (Arica,flight,Santiago). Bidirectional edges are
represented with two edges. The set of edge labels _𝐿_ has 8 elements, including start, flight, etc.


Definition B.1 does not state that _𝑉_ and _𝐿_ are disjoint: though not present in the example, a

node can also serve as an edge-label. The definition also permits that nodes and edge labels can be

present without any associated edge. Either restriction could be explicitly stated – if necessary – in

a particular application while still conforming to a directed edge-labelled graph.

In some of the definitions that follow, for ease of presentation, we may treat a set of (directed

labelled) edges _𝐸_ ⊆ _𝑉_ × _𝐿_ × _𝑉_ as a directed edge-labelled graph ( _𝑉, 𝐸, 𝐿_ ), in which case we refer to

the graph induced by _𝐸_ assuming that _𝑉_ and _𝐿_ contain all and only those nodes and edge labels,

respectively, used in _𝐸_ . We may similarly apply set operators on directed edge-labelled graphs,
which should be interpreted as applying to their sets of edges; for example, given _𝐺_ 1 = ( _𝑉_ 1 _, 𝐸_ 1 _, 𝐿_ 1)
and _𝐺_ 2 = ( _𝑉_ 2 _, 𝐸_ 2 _, 𝐿_ 2), by _𝐺_ 1 ∪ _𝐺_ 2 we refer to the directed edge-labelled graph induced by _𝐸_ 1 ∪ _𝐸_ 2.


_B.1.2_ _Heterogeneous graph._ We next define the notion of a heterogeneous graph.


_Definition B.3 (Heterogeneous graph)._ A _heterogeneous graph_ is a tuple _𝐺_  - ( _𝑉, 𝐸, 𝐿,𝑙_ ), where
_𝑉_ ⊆ Con is a set of nodes, _𝐿_ ⊆ Con is a set of edge and node labels, _𝐸_ ⊆ _𝑉_ × _𝐿_ × _𝑉_ is a set of edges,
and _𝑙_ : _𝑉_ → _𝐿_ maps each node to a label.


_Example B.4._ In reference to Figure 2b, the set of nodes _𝑉_ has three elements: Santiago, Chile,
and Perú. The set of edges _𝐸_ has 3 triples, including (Santiago,capital,Chile). The set of edge
labels _𝐿_ has 4 elements: capital, borders, City, Country. Finally, with respect to the node labels,
_𝑙_ (Santiago) = City, _𝑙_ (Chile) = Country, and _𝑙_ (Perú) = Country.


In heterogeneous graphs, edge and node labels are most commonly called _types_ . We remark that

by defining edges with labels per directed-edge labelled graphs – rather than labelling edges with _𝑙_

- we allow two nodes to be related by _𝑛_ edges with _𝑛_ different labels; e.g., we can represent both

(Santiago _,_ capital _,_ Chile) and (Santiago _,_ country _,_ Chile).


_B.1.3_ _Property graph._ Finally, we define a property graph.


_Definition B.5 (Property graph)._ A _property graph_ is a tuple _𝐺_  - ( _𝑉, 𝐸, 𝐿, 𝑃,𝑈,𝑒,𝑙, 𝑝_ ), where
_𝑉_ ⊆ Con is a set of node ids, _𝐸_ ⊆ Con is a set of edge ids, _𝐿_ ⊆ Con is a set of labels, _𝑃_ ⊆ Con is a


113


set of properties, _𝑈_ ⊆ Con is a set of values, _𝑒_ : _𝐸_ → _𝑉_ × _𝑉_ maps an edge id to a pair of node ids,
_𝑙_ : _𝑉_ ∪ _𝐸_ → 2 _[𝐿]_ maps a node or edge id to a set of labels, and _𝑝_ : _𝑉_ ∪ _𝐸_ → 2 _[𝑃]_ [×] _[𝑈]_ maps a node or

edge id to a set of property–value pairs.


_Example B.6._ Returning to Figure 4:


  - the set _𝑉_ contains Santiago and Arica;

  - the set _𝐸_ contains LA380 and LA381;

  - the set _𝐿_ contains Capital City, Port City, and flight;

  - the set _𝑃_ contains lat, long, and company;

  - the set _𝑈_ contains −33.45, −70.66, LATAM, −18.48, and −70.33;

  - the mapping _𝑒_ gives, for example, _𝑒_ (LA380) = (Santiago _,_ Arica);

  - the mapping _𝑙_ gives, for example, _𝑙_ (LA380) = {flight} and _𝑙_ (Santiago) = {Capital City};

  - the mapping _𝑝_ gives, for example, _𝑝_ (Santiago) = {(lat _,_ −33.45) _,_ (long _,_ −70.66)} and
_𝑝_ (LA380) = {(company _,_ LATAM)}.


Definition B.5 does not require that the sets _𝑉_, _𝐸_, _𝐿_, _𝑃_ or _𝑈_ to be (pairwise) disjoint: we allow, for

example, that values are also nodes. Unlike some previous definitions [16], here we allow a node or

edge to have several values for a given property. In practice, systems like Neo4j [354] may rather

support this by allowing an array of values. We view such variations as syntactic.


_B.1.4_ _Graph dataset._ Next we define a graph dataset, where one can consider directed-edge labelled

graph datasets, heterogeneous graph datasets, property graph datasets, etc.


_Definition B.7 (Graph dataset)._ A _named graph_ is a pair ( _𝑛,𝐺_ ) where _𝐺_ is a graph, and _𝑛_ ∈ Con is a
graph name. A _graph dataset_ is a pair _𝐷_ - ( _𝐺𝐷, 𝑁_ ) where _𝐺𝐷_ is a directed edge-labelled graph called
the _default graph_ and _𝑁_ is either the empty set, or a set of named graphs {( _𝑛_ 1 _,𝐺_ 1) _, . . ._ ( _𝑛𝑘,𝐺𝑘_ )}
( _𝑘_ _>_ 0) such that _𝑛𝑖_ = _𝑛_ _𝑗_ if and only if _𝑖_ = _𝑗_ (1 ≤ _𝑖_ ≤ _𝑘_, 1 ≤ _𝑗_ ≤ _𝑘_ ).


_Example B.8._ Figure 5 provides an example of a directed-edge labelled graph dataset _𝐷_ consisting

of two named graphs and a default graph. The default graph does not have a name associated with

it. The two graph names are Events and Routes; these are also used as nodes in the default graph.


An RDF dataset is a graph dataset model standardised by the W3C [111] where each graph is an

RDF graph, and graph names can be blank nodes or IRIs.


**B.2** **Querying**


Here we formalise foundational notions relating to queries over graphs, starting with graph patterns,

to which we later add relational-style operators and path expressions.


_B.2.1_ _Graph patterns._ We formalise the notions of graph patterns first for directed edge-labelled

graphs, and subsequently for property graphs [16]. For these definitions, we introduce a countably

infinite set of _variables_ Var ranging over (but disjoint from: Con ∩ Var = ∅) the set of constants. We
refer generically to constants and variables as _terms_, denoted and defined as Term = Con ∪ Var.


_Definition B.9 (Directed edge-labelled graph pattern)._ We define a _directed edge-labelled graph_

_pattern_ as a tuple _𝑄_ = ( _𝑉, 𝐸, 𝐿_ ), where _𝑉_ ⊆ Term is a set of node terms, _𝐿_ ⊆ Term is a set of edge
terms, and _𝐸_ ⊆ _𝑉_ × _𝐿_ × _𝑉_ is a set of edges (triple patterns).


_Example B.10._ Returning to the graph pattern of Figure 6:


  - the set _𝑉_ contains the constant Food Festival and variables ?event, ?ven1 and ?ven2;

  - the set _𝐿_ contains the constants type and venue;

  - the set _𝐸_ contains four edges, including (?event _,_ type _,_ Food Festival), etc.


114


A property graph pattern is defined analogously, allowing variables in any position.


_Definition B.11 (Property graph pattern)._ We define a _property graph pattern_ as a tuple _𝑄_ =
( _𝑉, 𝐸, 𝐿, 𝑃,𝑈,𝑒,𝑙, 𝑝_ ), where _𝑉_ ⊆ Term is a set of node id terms, _𝐸_ ⊆ Term is a set of edge id terms,
_𝐿_ ⊆ Term is a set of label terms, _𝑃_ ⊆ Term is a set of property terms, _𝑈_ ⊆ Term is a set of value
terms, _𝑒_ : _𝐸_ → _𝑉_ × _𝑉_ maps an edge id term to a pair of node id terms, _𝑙_ : _𝑉_ ∪ _𝐸_ → 2 _[𝐿]_ maps a node
or edge id term to a set of label terms, and _𝑝_ : _𝑉_ ∪ _𝐸_ → 2 _[𝑃]_ [×] _[𝑈]_ maps a node or edge id term to a set

of pairs of property–value terms.


Towards defining the evaluation of a graph pattern, we first define a partial mapping _𝜇_ : Var →
Con from variables to constants, whose _domain_ (the set of variables for which it is defined) is
denoted by dom( _𝜇_ ). Given a graph pattern _𝑄_, let Var( _𝑄_ ) denote the set of all variables appearing
in (some recursively nested element of) _𝑄_ . Abusing notation, we denote by _𝜇_ ( _𝑄_ ) the image of _𝑄_
under _𝜇_, meaning that any variable _𝑣_ ∈ Var( _𝑄_ ) ∩ dom( _𝜇_ ) is replaced in _𝑄_ by _𝜇_ ( _𝑣_ ). Observe that
when Var( _𝑄_ ) ⊆ dom( _𝜇_ ), then _𝜇_ ( _𝑄_ ) is a data graph (in the corresponding model of _𝑄_ ).

Next, we define the notion of containment between data graphs. For two directed edge-labelled
graph pattern _𝐺_ 1 = ( _𝑉_ 1 _, 𝐸_ 1 _, 𝐿_ 1) and _𝐺_ 2 = ( _𝑉_ 2 _, 𝐸_ 2 _, 𝐿_ 2), we say that _𝐺_ 1 is a _sub-graph_ of _𝐺_ 2, denoted
_𝐺_ 1 ⊆ _𝐺_ 2, if and only if _𝑉_ 1 ⊆ _𝑉_ 2, _𝐸_ 1 ⊆ _𝐸_ 2, and _𝐿_ 1 ⊆ _𝐿_ 2. [39] Conversely, in property graphs, nodes
can often be defined without edges. For two property graphs _𝐺_ 1 = ( _𝑉_ 1 _, 𝐸_ 1 _, 𝐿_ 1 _, 𝑃_ 1 _,𝑈_ 1 _,𝑒_ 1 _,𝑙_ 1 _, 𝑝_ 1) and
_𝐺_ 2 = ( _𝑉_ 2 _, 𝐸_ 2 _, 𝐿_ 2 _, 𝑃_ 2 _,𝑈_ 2 _,𝑒_ 2 _,𝑙_ 2 _, 𝑝_ 2), we say that _𝐺_ 1 is a _sub-graph_ of _𝐺_ 2, denoted _𝐺_ 1 ⊆ _𝐺_ 2, if and only
if _𝑉_ 1 ⊆ _𝑉_ 2, _𝐸_ 1 ⊆ _𝐸_ 2, _𝐿_ 1 ⊆ _𝐿_ 2, _𝑃_ 1 ⊆ _𝑃_ 2, _𝑈_ 1 ⊆ _𝑈_ 2, for all _𝑥_ ∈ _𝐸_ 1 it holds that _𝑒_ 1( _𝑥_ ) = _𝑒_ 2( _𝑥_ ), and for all
_𝑦_ ∈ _𝐸_ 1 ∪ _𝑉_ 1 it holds that _𝑙_ 1( _𝑦_ ) ⊆ _𝑙_ 2( _𝑦_ ) and _𝑝_ 1( _𝑦_ ) ⊆ _𝑝_ 2( _𝑦_ ).

We are now ready to define the evaluation of a graph pattern.


_Definition B.12 (Evaluation of a graph pattern)._ Let _𝑄_ be a graph pattern and let _𝐺_ be a data graph.

We then define the _evaluation of graph pattern 𝑄_ _over the data graph 𝐺_, denoted _𝑄_ ( _𝐺_ ), to be the set
of mappings { _𝜇_ | _𝜇_ ( _𝑄_ ) ⊆ _𝐺_ and dom( _𝜇_ ) = Var( _𝑄_ )}.


_Example B.13._ Figure 6 enumerates all of the mappings given by the evaluation of the depicted

graph pattern over the data graph of Figure 1. Each non-header row indicates a mapping _𝜇_ .


The final results of evaluating a graph pattern may then vary depending on the choice of

semantics: the results under _homomorphism-based semantics_ are defined as _𝑄_ ( _𝐺_ ). Conversely,

under _isomorphism-based_ semantics, mappings that send two edge variables to the same constant

and/or mappings that send two node variables to the same constant may be excluded from the

results. Henceforth we assume the more general _homomorphism-based semantics_ .


_B.2.2_ _Complex graph patterns._ We now define complex graph patterns.


_Definition B.14 (Complex graph pattern). Complex graph patterns_ are defined recursively:


  - If _𝑄_ is a graph pattern, then _𝑄_ is a _complex graph pattern_ .

  - If _𝑄_ is a complex graph pattern, and V ⊆ Var( _𝑄_ ), then _𝜋_ V ( _𝑄_ ) is a _complex graph pattern_ .

  - If _𝑄_ is a complex graph pattern, and _𝑅_ is a selection condition with boolean and equality
connectives (∧, ∨, ¬, =), then _𝜎𝑅_ ( _𝑄_ ) is a _complex graph pattern_ .

  - If _𝑄_ 1 and _𝑄_ 2 are complex graph patterns, then _𝑄_ 1 � _𝑄_ 2, _𝑄_ 1 ∪ _𝑄_ 2, _𝑄_ 1 − _𝑄_ 2 and and _𝑄_ 1 ▷ _𝑄_ 2

are also _complex graph patterns_ .


39Given, for example, _𝐺_ 1 = ({ _𝑎_ } _,_ {( _𝑎,𝑏,𝑎_ ) } _,_ { _𝑏,𝑐_ }) and _𝐺_ 2 = ({ _𝑎,𝑐_ } _,_ {( _𝑎,𝑏,𝑎_ ) } _,_ { _𝑏_ }), we remark that _𝐺_ 1 ⊈ _𝐺_ 2 and

_𝐺_ 2 ⊈ _𝐺_ 1: the former has a label not used on an edge while the latter has a node without an incident edge. In concrete data
models like RDF where such cases of nodes or labels without edges cannot occur, the sub-graph relation _𝐺_ 1 ⊆ _𝐺_ 2 holds if
and only if _𝐸_ 1 ⊆ _𝐸_ 2 holds.


115


Next we define the evaluation of complex graph patterns. First, given a mapping _𝜇_, for a set of
variables V ⊆ Var let _𝜇_ [V] denote the mapping _𝜇_ [′] such that dom( _𝜇_ [′] ) = dom( _𝜇_ ) ∩V and _𝜇_ ( _𝑣_ ) =
_𝜇_ [′] ( _𝑣_ ) for all _𝑣_ ∈ dom( _𝜇_ [′] ) (in other words, _𝜇_ [V] projects the variables V from _𝜇_ ). Furthermore,
letting _𝑅_ denote a boolean selection condition and _𝜇_ a mapping, by _𝜇_ |= _𝑅_ we denote that _𝜇_ satisfies
the boolean condition. Finally, we define two mappings _𝜇_ 1 and _𝜇_ 2 to be _compatible_, denoted _𝜇_ 1 ∼ _𝜇_ 2,
if and only if _𝜇_ 1( _𝑣_ ) = _𝜇_ 2( _𝑣_ ) for all _𝑣_ ∈ dom( _𝜇_ 1) ∩ dom( _𝜇_ 2) (in other words, they map all common

variables to the same constant). We are now ready to provide the definition.


_Definition B.15 (Complex graph pattern evaluation)._ Given a complex graph pattern _𝑄_, if _𝑄_ is a

graph pattern, then _𝑄_ ( _𝐺_ ) is defined per Definition B.12. Otherwise:


_𝜋_ V ( _𝑄_ )( _𝐺_ ) � { _𝜇_ [V] | _𝜇_ ∈ _𝑄_ ( _𝐺_ )}


_𝜎𝑅_ ( _𝑄_ )( _𝐺_ ) � { _𝜇_ | _𝜇_ ∈ _𝑄_ ( _𝐺_ ) and _𝜇_ |= _𝑅_ }


_𝑄_ 1 � _𝑄_ 2( _𝐺_ ) � { _𝜇_ 1 ∪ _𝜇_ 2 | _𝜇_ 1 ∈ _𝑄_ 2( _𝐺_ ) and _𝜇_ 2 ∈ _𝑄_ 1( _𝐺_ ) and _𝜇_ 1 ∼ _𝜇_ 2}


_𝑄_ 1 ∪ _𝑄_ 2( _𝐺_ ) � { _𝜇_ | _𝜇_ ∈ _𝑄_ 1( _𝐺_ ) or _𝜇_ ∈ _𝑄_ 2( _𝐺_ )}


_𝑄_ 1 − _𝑄_ 2( _𝐺_ ) � { _𝜇_ | _𝜇_ ∈ _𝑄_ 1( _𝐺_ ) and _𝜇_ ∉ _𝑄_ 2( _𝐺_ )}


_𝑄_ 1 ▷ _𝑄_ 2( _𝐺_ ) = { _𝜇_ | _𝜇_ ∈ _𝑄_ 1( _𝐺_ ) and � _𝜇_ 2 ∈ _𝑄_ 2( _𝐺_ ) such that _𝜇_ ∼ _𝜇_ 2}


Based on these query operators, we can also define some additional syntactic operators, such as

the _left-join_ ( ~~�~~, aka _optional_ ):


_𝑄_ 1 ~~�~~ _𝑄_ 2( _𝐺_ ) � ( _𝑄_ 1( _𝐺_ ) � _𝑄_ 2( _𝐺_ )) ∪( _𝑄_ 1( _𝐺_ ) ▷ _𝑄_ 2( _𝐺_ ))


We call such operators _syntactic_ as they do not add expressivity to the query language.


_Example B.16._ Figure 8 illustrates a complex graph pattern and its evaluation.


_B.2.3_ _Navigational graph patterns._ We first define path expressions and regular path queries.


_Definition B.17 (Path expression)._ A constant (edge label) _𝑐_ is a _path expression_ . Furthermore:


  - If _𝑟_ is a path expression, then _𝑟_ [−] ( _inverse_ ) and _𝑟_ [∗] ( _Kleene star_ ) are _path expressions_ .

  - If _𝑟_ 1 and _𝑟_ 2 are path expressions, then _𝑟_ 1 · _𝑟_ 2 ( _concatenation_ ) and _𝑟_ 1 | _𝑟_ 2 ( _disjunction_ ) are _path_

_expressions_ .


We now define the evaluation of a path expression under the SPARQL 1.1-style semantics whereby

the endpoints (pairs of start and end nodes) of the path are returned [217].


_Definition B.18 (Path expression evaluation (directed edge-labelled graph))._ Given a directed edge
labelled graph _𝐺_ = ( _𝑉, 𝐸, 𝐿_ ) and a path expression _𝑟_, we define the _evaluation of 𝑟_ _over 𝐺_, denoted
_𝑟_ [ _𝐺_ ], as follows:


_𝑟_ [ _𝐺_ ] � {( _𝑢, 𝑣_ ) | ( _𝑢,𝑟, 𝑣_ ) ∈ _𝐸_ } (for _𝑟_ ∈ Con)

_𝑟_ [−] [ _𝐺_ ] � {( _𝑢, 𝑣_ ) | ( _𝑣,𝑢_ ) ∈ _𝑟_ [ _𝐺_ ]}


_𝑟_ 1 | _𝑟_ 2 [ _𝐺_ ] � _𝑟_ 1 [ _𝐺_ ] ∪ _𝑟_ 2 [ _𝐺_ ]


_𝑟_ 1 · _𝑟_ 2 [ _𝐺_ ] � {( _𝑢, 𝑣_ ) | ∃ _𝑤_ ∈ _𝑉_ : ( _𝑢,𝑤_ ) ∈ _𝑟_ 1 [ _𝐺_ ] and ( _𝑤, 𝑣_ ) ∈ _𝑟_ 2 [ _𝐺_ ]}


      _𝑟_ [∗] [ _𝐺_ ] � _𝑉_ ∪ _𝑟_ _[𝑛]_ [ _𝐺_ ]


_𝑛_ ∈N [+]


where by _𝑟_ _[𝑛]_ we denote the _𝑛_ [th] -concatenation of _𝑟_ (e.g., _𝑟_ [3] = _𝑟_ - _𝑟_ - _𝑟_ ).


116


The evaluation of a path expression on a property graph _𝐺_ = ( _𝑉, 𝐸, 𝐿, 𝑃,𝑈,𝑒,𝑙, 𝑝_ ) can be defined
analogously by adapting the first definition (in the case that _𝑟_ ∈ Con) as follows:


_𝑟_ [ _𝐺_ ] � {( _𝑢, 𝑣_ ) | ∃ _𝑥_ ∈ _𝐸_ : _𝑒_ ( _𝑥_ ) = ( _𝑢, 𝑣_ ) and _𝑙_ ( _𝑒_ ) = _𝑟_ } _._


The rest of the definitions then remain unchanged.
Query languages may support additional operators, some of which are syntactic (e.g., _𝑟_ [+] is
sometimes used for one-or-more, but can be rewritten as _𝑟_ - _𝑟_ [∗] ), while others may add expressivity

such as the case of SPARQL [217], which allows a limited form of negation in expressions (e.g., ! _𝑟_,

with _𝑟_ being a constant or the inverse of a constant, matching any path not labelled _𝑟_ ).

Next we define a regular path query and its evaluation.


_Definition B.19 (Regular path query)._ A _regular path query_ is a triple ( _𝑥,𝑟,𝑦_ ) where _𝑥,𝑦_ ∈
Con ∪ Var and _𝑟_ is a path expression.


_Definition B.20 (Regular path query evaluation)._ Let _𝐺_ denote a directed edge-labelled graph, _𝑐_,
_𝑐_ 1, _𝑐_ 2 ∈ Con denote constants and _𝑧_, _𝑧_ 1, _𝑧_ 2 ∈ Var denote variables. Then the _evaluation of a regular_

_path query_ is defined as follows:


( _𝑐_ 1 _,𝑟,𝑐_ 2)( _𝐺_ ) �{ _𝜇_ ∅ | ( _𝑐_ 1 _,𝑐_ 2) ∈ _𝑟_ [ _𝐺_ ]}


( _𝑐,𝑟,𝑧_ )( _𝐺_ ) �{ _𝜇_ | dom( _𝜇_ ) = { _𝑧_ } and ( _𝑐, 𝜇_ ( _𝑧_ )) ∈ _𝑟_ [ _𝐺_ ]}


( _𝑧,𝑟,𝑐_ )( _𝐺_ ) �{ _𝜇_ | dom( _𝜇_ ) = { _𝑧_ } and ( _𝜇_ ( _𝑧_ ) _,𝑐_ ) ∈ _𝑟_ [ _𝐺_ ]}


( _𝑧_ 1 _,𝑟,𝑧_ 2)( _𝐺_ ) �{ _𝜇_ | dom( _𝜇_ ) = { _𝑧_ 1 _,𝑧_ 2} and ( _𝜇_ ( _𝑧_ 1) _, 𝜇_ ( _𝑧_ 2)) ∈ _𝑟_ [ _𝐺_ ]}


where _𝜇_ ∅ denotes the empty mapping such that dom( _𝜇_ ) = ∅ (the join identity).


_Definition B.21 (Navigational graph pattern)._ If _𝑄_ is a graph pattern, then _𝑄_ is a _navigational_

_graph pattern_ . Furthermore, if _𝑄_ is a navigational graph pattern and ( _𝑥,𝑟,𝑦_ ) is a regular path query,
then _𝑄_ - ( _𝑥,𝑟,𝑦_ ) is a _navigational graph pattern_ .


The definition of the evaluation of a navigational graph pattern then follows from the previous

definition of a join and the corresponding definition of the evaluation of a regular path query (for

a directed edge-labelled graph or a property graph, respectively). Likewise, _complex navigational_

_graph patterns_ - and their evaluation – are defined by extending this definition in the natural way

with the same operators from Definition B.14 following the same semantics seen in Definition B.15.


**B.3** **Schema**

Here we formalise notions relating to schemata for graphs. Though we present definitions for

directed edge-labelled graphs – which allows for more succinct presentation – the same concepts

can be applied to property graphs and other graph models.


_B.3.1_ _Semantic schema._ We provide definitions that generalise semantic schemata in Appendix B.5.


_B.3.2_ _Validating schema._ We define shapes following conventions used by Labra Gayo et al. [305].


_Definition B.22 (Shape)._ A _shape 𝜙_ is defined as:


117


_𝜙_ ::= ⊤ true
| Δ _𝑁_ node belongs to the set of nodes _𝑁_
| Ψcond node satisfies the boolean condition cond
| _𝜙_ 1 ∧ _𝜙_ 2 conjunction of shape _𝜙_ 1 and shape _𝜙_ 2
| ¬ _𝜙_ negation of shape _𝜙_
| @ _𝑠_ reference to shape with label _𝑠_


_𝑝_
| −→ _𝜙_ { _𝑚𝑖𝑛,𝑚𝑎𝑥_ } between _𝑚𝑖𝑛_ and _𝑚𝑎𝑥_ outward edges (inclusive)

with label _𝑝_ to nodes satisfying shape _𝜙_


where _𝑚𝑖𝑛_ ∈ N(0), _𝑚𝑎𝑥_ ∈ N(0) ∪{∗}, with “∗” indicating unbounded.


_Definition B.23 (Shapes schema)._ A _shapes schema_ is defined as a tuple Σ ≔ (Φ _,𝑆, 𝜆_ ) where Φ is a
set of shapes, _𝑆_ is a set of shape labels, and _𝜆_ : _𝑆_ → Φ is a total function from labels to shapes.


_Example B.24._ The shapes schema from Figure 13 can be expressed as:



start
−−−→ ΔdateTime{1 _,_ 1}∧



end
−−→ ΔdateTime{1 _,_ 1}



Event ↦→



name
−−−−→ Δstring{1 _,_ ∗}∧



venue
−−−−→ @ Venue {1 _,_ ∗}



∧



type
−−−→⊤{1 _,_ ∗}∧



city
−−→ @ City {0 _,_ 1}



Venue ↦→ @ Place ∧


City ↦→ @ Place ∧



indoor
−−−−→ Δboolean{0 _,_ 1}∧



population
−−−−−−−−→(Δint ∧ Ψ _>_ 5000){0 _,_ 1}



long
−−−→ Δfloat{0 _,_ 1}



Place ↦→



lat
−−→ Δfloat{0 _,_ 1}∧



bus
−−→ @ Place {0 _,_ ∗}



∧



flight
−−−−→ @ Place {0 _,_ ∗}∧



In a shapes schema, shapes may refer to other shapes, giving rise to a graph that is sometimes

known as the _shapes graph_ [296]. Figure 13 illustrates a shapes graph of this form.


The semantics of a shape _𝜙_ is defined in terms of the evaluation of _𝜙_ over the nodes of a graph

_𝐺_ = ( _𝑉, 𝐸, 𝐿_ ) with respect to a shapes map _𝜎_ associating nodes and shape labels that apply to them.


_Definition B.25 (Shapes map)._ Given a graph _𝐺_ = ( _𝑉, 𝐸, 𝐿_ ) and a schema Σ = (Φ _,𝑆, 𝜆_ ), a _shapes_
_map_ is a (partial) mapping _𝜎_ : _𝑉_ × _𝑆_ →{0 _,_ 1}.


The precise semantics of a shape then depends on whether or not _𝜎_ is a total or partial mapping:

whether or not it is defined for every value in _𝑉_ × _𝑆_ . In this paper, we present the semantics for the

more straightforward case where _𝜎_ is assumed to be a total shapes map.


_Definition B.26 (Shape evaluation)._ Given a shapes schema Σ ≔ (Φ _,𝑆, 𝜆_ ), the semantics of a shape
_𝜙_ ∈ Φ is defined in terms of a _shape evaluation function_ [ _𝜙_ ] _[𝐺,𝑣,𝜎]_ ∈{0 _,_ 1}, for a graph _𝐺_ = ( _𝑉, 𝐸, 𝐿_ ),
a node _𝑣_ ∈ _𝑉_ and a total shapes map _𝜎_, such that:

[⊤] _[𝐺,𝑣,𝜎]_ = 1

[Δ _𝑁_ ] _[𝐺,𝑣,𝜎]_ = 1 iff _𝑣_ ∈ _𝑁_

[Ψcond] _[𝐺,𝑣,𝜎]_ = 1 iff cond( _𝑣_ ) is true

[ _𝜙_ 1 ∧ _𝜙_ 2] _[𝐺,𝑣,𝜎]_ = min{[ _𝜙_ 1] _[𝐺,𝑣,𝜎]_ _,_ [ _𝜙_ 2] _[𝐺,𝑣,𝜎]_ }

[¬ _𝜙_ ] _[𝐺,𝑣,𝜎]_ = 1 −[ _𝜙_ ] _[𝐺,𝑣,𝜎]_

[@ _𝑠_ ] _[𝐺,𝑣,𝜎]_ = 1 iff _𝜎_ ( _𝑣,𝑠_ ) = 1


_𝑝_

[−→ _𝜙_ { _𝑚𝑖𝑛,𝑚𝑎𝑥_ }] _𝐺,𝑣,𝜎_ = 1 iff _𝑚𝑖𝑛_ ≤|{( _𝑣, 𝑝,𝑢_ ) ∈ _𝐸_ | [ _𝜙_ ] _[𝐺,𝑢,𝜎]_ = 1}| ≤ _𝑚𝑎𝑥_


If [ _𝜙_ ] _[𝐺,𝑣,𝜎]_ = 1, then _𝑣_ is said to _satisfy 𝜙_ in _𝐺_ under _𝜎_ .


Typically for the purposes of validating a graph with respect to a shapes schema, a _target_ is

defined that requires certain nodes to satisfy certain shapes.


118


_Definition B.27 (Shapes target)._ Given a directed edge-labelled graph _𝐺_ = ( _𝑉, 𝐸, 𝐿_ ) and a shapes
schema Σ = (Φ _,𝑆, 𝜆_ ), a _shapes target 𝑇_ is a set of pairs of nodes and shape labels: _𝑇_ ⊆ _𝑉_ × _𝑆_ .


The nodes that a shape targets can be selected manually, based on the type(s) of the nodes, based

on the results of a graph query, etc. [104, 305].


Lastly, we can define the notion of a valid graph under a given shapes schema and target.


_Definition B.28 (Valid graph)._ Given a shapes schema Σ = (Φ _,𝑆, 𝜆_ ), a graph _𝐺_ = ( _𝑉, 𝐸, 𝐿_ ), and a
shapes target _𝑇_, we say that _𝐺_ _is valid under_ Σ _and 𝑇_ if and only if there exists a shapes map _𝜎_ such
that, for all _𝑠_ ∈ _𝑆_ and _𝑣_ ∈ _𝑉_ it holds that _𝜎_ ( _𝑣,𝑠_ ) = [ _𝜆_ ( _𝑠_ )] _[𝐺,𝑣,𝜎]_, and ( _𝑣,𝑠_ ) ∈ _𝑇_ implies _𝜎_ ( _𝑣,𝑠_ ) = 1.


_Example B.29._ Taking the graph _𝐺_ from Figure 1 and the shapes schema Σ from Figure 13,
first assume an empty shapes target _𝑇_ = {}. If we consider a shapes map where (for example) _𝜎_ ( [EID15] _,_ Event ) = 1, _𝜎_ ( [Santa Lucía] _,_ Venue ) = 1, _𝜎_ ( [Santa Lucía] _,_ Place ) = 1, etc., but where
_𝜎_ ( [EID16] _,_ Event ) = 0 (as it does not have the required values for start and end), etc., then we see that

|e) 𝜎( EID15, Event<br>EID16, Event ) = 0|Col2|Event|Col4|
|---|---|---|---|
|e)_ 𝜎_( EID15 _,_ Event <br> EID16 _,_ Event ) = 0|Event|Event|) = 0|

_𝐺_ is valid under Σ and _𝑇_ . However, if we were to define a shapes target _𝑇_ to ensure that the Event
shape targets [EID15] and [EID16] - i.e., to define _𝑇_ such that {( [EID15] _,_ Event ) _,_ ( [EID16] _,_ Event )} ⊆ _𝑇_ then the graph would no longer be valid under Σ and _𝑇_ since [EID16] does not satisfy Event .

|Event|Col2|)|
|---|---|---|
|y|Event|Event|



The semantics we present here assumes that each node in the graph either satisfies or does

not satisfy each shape labelled by the schema. More complex semantics – for example, based on

Kleene’s three-valued logic [104, 305] – have been proposed that support partial shapes maps,

where the satisfaction of some nodes for some shapes can be left undefined. Shapes languages

in practice may support other forms of constraints, such as counting on paths [296]. In terms of

implementing validation with respect to shapes, work has been done on translating constraints

into sets of graph queries, whose results are input to a SAT solver for recursive cases [103].


_B.3.3_ _Emergent schema._ Emergent schemata are often based on the notion of a quotient graph.


_Definition B.30 (Quotient graph)._ Given a directed-edge labelled graph _𝐺_ = ( _𝑉, 𝐸, 𝐿_ ), a graph
G = (V _,_ E _, 𝐿_ ) is a _quotient graph_ of _𝐺_ if and only if:

  - V is a partition of _𝑉_ without the empty set, i.e., V ⊆(2 _[𝑉]_ −∅), _𝑉_ = [�] _𝑈_ ∈V _[𝑈]_ [, and for all]
_𝑈_ ∈V, _𝑊_ ∈V, it holds that _𝑈_ = _𝑊_ or _𝑈_ ∩ _𝑊_ = ∅; _and_

  - E = {( _𝑈,𝑙,𝑊_ ) | _𝑈_ ∈V _,𝑊_ ∈V and there exist _𝑢_ ∈ _𝑈,𝑤_ ∈ _𝑊_ such that ( _𝑢,𝑙,𝑤_ ) ∈ _𝐸_ }.


Intuitively speaking, a quotient graph can merge multiple nodes into one node, where the merged

node preserves the edges of its constituent nodes. For an input graph _𝐺_ = ( _𝑉, 𝐸, 𝐿_ ), there is an

exponential number of potential quotient graphs: as many as there are partitions of the input

graphs’ nodes. On one extreme, the input graph is a quotient graph of itself (turning nodes like


u into singleton nodes like {u} ). On the other extreme, a single node _𝑉_, with all input nodes,
and loops ( _𝑉,𝑙,𝑉_ ) for each edge-label _𝑙_ used in _𝐸_, the set of input edges, is also a quotient graph.
Practical quotient graphs typically fall somewhere in between, where the partition V of _𝑉_ is often
defined in terms of an _equivalence relation_ ∼ on the set _𝑉_ such that V � ∼/ _𝑉_ ; i.e., V is defined as
the _quotient set_ of _𝑉_ with respect to ∼; for example, we might define an equivalence relation on
nodes such that _𝑢_ ∼ _𝑣_ if and only if they have the same set of defined types, where ∼/ _𝑉_ is then a

partition whose parts contain all nodes with the same types. Another way to induce a quotient

graph is to define the partition in a way that preserves some of the topology of the input graph.

One way to formally define this idea is through _simulation_ and _bisimulation_ .


_Definition B.31 (Simulation)._ Given two directed-edge labelled graph _𝐺_  - ( _𝑉, 𝐸, 𝐿_ ) and _𝐺_ [′]  ( _𝑉_ [′] _, 𝐸_ [′] _, 𝐿_ [′] ), let _𝑅_ ⊆ _𝑉_ × _𝑉_ [′] be a relation between the nodes of _𝐺_ and _𝐺_ [′], respectively. We call _𝑅_ a
_simulation_ on _𝐺_ and _𝐺_ [′] if, for all ( _𝑣, 𝑣_ [′] ) ∈ _𝑅_, the following holds:


119


  - if ( _𝑣, 𝑝,𝑤_ ) ∈ _𝐸_ then there exists _𝑤_ [′] such that ( _𝑣_ [′] _, 𝑝,𝑤_ [′] ) ∈ _𝐸_ [′] and ( _𝑤,𝑤_ [′] ) ∈ _𝑅_ .
If a simulation exists on _𝐺_ and _𝐺_ [′], we say that _𝐺_ [′] _simulates 𝐺_, denoted _𝐺_ ⇝ _𝐺_ [′] .


_Definition B.32 (Bisimulation)._ If _𝑅_ is a simulation on _𝐺_ and _𝐺_ [′], we call it a _bisimulation_ if, for all
( _𝑣, 𝑣_ [′] ) ∈ _𝑅_, the following condition holds:

  - if ( _𝑣_ [′] _𝑝,𝑤_ [′] ) ∈ _𝐸_ [′] then there exists _𝑤_ such that ( _𝑣, 𝑝,𝑤_ ) ∈ _𝐸_ and ( _𝑤,𝑤_ [′] ) ∈ _𝑅_ .
If a bisimulation exists on _𝐺_ and _𝐺_ [′], we say that they are _bisimilar_, denoted _𝐺_ ≈ _𝐺_ [′] .


Bisimulation (≈) is then an equivalence relation on graphs. By defining the (bi)simulation
relation _𝑅_ in terms of set membership ∈, every quotient graph simulates its input graph, but does

not necessarily bisimulate its input graph. This gives rise to the notion of _bisimilar quotient graphs_ .


_Example B.33._ Figures 14 and 15 exemplify quotient graphs for the graph of Figure 1. Figure 14
