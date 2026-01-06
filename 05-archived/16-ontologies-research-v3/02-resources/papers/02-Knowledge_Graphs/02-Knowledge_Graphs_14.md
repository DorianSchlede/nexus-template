<!-- Source: 02-Knowledge_Graphs.pdf | Chunk 14/15 -->



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

simulates but is not bisimilar to the data graph. Figure 15 is bisimilar to the data graph. Often the

goal will be to compute the most concise quotient graph that satisfies a given condition; for example,

the nodes without outgoing edges in Figure 15 could be merged while preserving bisimilarity.


**B.4** **Context**


_B.4.1_ _Annotation domain._ We define an annotation domain per Zimmermann et al. [583].


_Definition B.34 (Annotation domain)._ Let _𝐴_ be a set of _annotation values_ . An _annotation domain_ is

defined as an idempotent, commutative semi-ring _𝐷_ = ⟨ _𝐴,_ ⊕ _,_ ⊗ _,_ ⊥ _,_ ⊤⟩.


This definition can be used to instantiate specific domains of context. Letting _𝐷_ be a semi-ring

imposes that, for any values _𝑎,𝑎_ 1 _,𝑎_ 2 _,𝑎_ 3 in _𝐴_, the following hold:


  - ( _𝑎_ 1 ⊕ _𝑎_ 2) ⊕ _𝑎_ 3 = _𝑎_ 1 ⊕( _𝑎_ 2 ⊕ _𝑎_ 3)

  - (⊥⊕ _𝑎_ ) = ( _𝑎_ ⊕⊥) = _𝑎_

  - ( _𝑎_ 1 ⊕ _𝑎_ 2) = ( _𝑎_ 2 ⊕ _𝑎_ 1)

  - ( _𝑎_ 1 ⊕ _𝑎_ 2) = ( _𝑎_ 2 ⊕ _𝑎_ 1)

  - ( _𝑎_ 1 ⊗ _𝑎_ 2) ⊗ _𝑎_ 3 = _𝑎_ 1 ⊗( _𝑎_ 2 ⊗ _𝑎_ 3)

  - (⊤⊗ _𝑎_ ) = ( _𝑎_ ⊗⊤) = _𝑎_

  - _𝑎_ 1 ⊗( _𝑎_ 2 ⊕ _𝑎_ 3) = ( _𝑎_ 1 ⊗ _𝑎_ 2) ⊕( _𝑎_ 1 ⊗ _𝑎_ 3)

  - ( _𝑎_ 1 ⊕ _𝑎_ 2) ⊗ _𝑎_ 3 = ( _𝑎_ 1 ⊗ _𝑎_ 3) ⊕( _𝑎_ 2 ⊗ _𝑎_ 3)

  - (⊥⊗ _𝑎_ ) = ( _𝑎_ ⊗⊥) = ⊥

The requirement that it be a commutative semi-ring imposes the following constraint:


  - ( _𝑎_ 1 ⊗ _𝑎_ 2) = ( _𝑎_ 2 ⊗ _𝑎_ 1)

Finally, the requirement that it be an idempotent semi-ring imposes the following constraint:


  - ( _𝑎_ ⊕ _𝑎_ ) = _𝑎_

Idempotence induces a partial order: _𝑎_ 1 ≤ _𝑎_ 2 if and only if _𝑎_ 1 ⊕ _𝑎_ 2 = _𝑎_ 2. Imposing these conditions

on the annotation domain allow for reasoning and querying to be conducted over the annotation

domain in a well-defined manner. Annotated graphs can then be defined in the natural way:


_Definition B.35 (Annotated directed-edge labelled graph)._ Letting _𝐷_ = ⟨ _𝐴,_ ⊕ _,_ ⊗ _,_ ⊥ _,_ ⊤⟩ denote an
idempotent, commutative semi-ring, we define an _annotated directed-edge labelled graph 𝐺_ ≔
( _𝑉, 𝐸𝐴, 𝐿_ ) where _𝑉_ ⊆ Con is a set of nodes, _𝐿_ ⊆ Con is a set of edge labels, and _𝐸𝐴_ ⊆ _𝑉_ × _𝐿_ × _𝑉_ × _𝐴_

is a set of edges annotated with values from _𝐴_ .


Figure 20 exemplifies query answering on a graph annotated with days of the year. Formally this

domain can be defined as follows: _𝐴_ ≔ 2 [N][[][1] _[,]_ [365][]], ⊕ ≔ ∪, ⊗ ≔ ∩, ⊤ ≔ N[1 _,_ 365], ⊥ ≔ ∅, where one
may verify that _𝐷_ = ⟨2 [N][[][1] _[,]_ [365][]] _,_ ∪ _,_ ∩ _,_ N[1 _,_ 365] _,_ ∅⟩ is indeed an idempotent, commutative semi-ring.


120


**B.5** **Deductive Knowledge**

We provide some formal definitions for concepts relating to deductive knowledge, starting with

the notion of an interpretation for a graph. We then describe some logical formalisms by which

reasoning can be conducted over graphs, describing rules and Description Logics.


_B.5.1_ _Graph interpretations._ A graph interpretation – or simply interpretation – captures the

assumptions under which the semantics of a graph can be defined. We define interpretations for

directed edge-labelled graphs, though the notion extends naturally to other graph models.


_Definition B.36 (Graph interpretation)._ A _(graph) interpretation 𝐼_ is defined as a pair _𝐼_ ≔ (Γ _,_  - _[𝐼]_ )
where Γ = ( _𝑉_ Γ _, 𝐸_ Γ _, 𝐿_ Γ) is a (directed edge-labelled) graph called the _domain graph_ and · _[𝐼]_ : Con →
_𝑉_ Γ ∪ _𝐿_ Γ is a partial mapping from constants to terms in the domain graph.


We denote the domain of the mapping · _[𝐼]_ by dom(· _[𝐼]_ ). For interpretations under the UNA, the
mapping · _[𝐼]_ is required to be injective, while with no UNA (NUNA), no such requirement is necessary.

Interpretations that _satisfy_ a graph are then said to be _models_ of that graph. We first define this

notion for a base case that ignores ontological features.


_Definition B.37 (Graph models)._ Let _𝐺_ ≔ ( _𝑉, 𝐸, 𝐿_ ) be a directed edge-labelled graph. An interpretation _𝐼_ ≔ (Γ _,_ - _[𝐼]_ ) _satisfies 𝐺_ if and only if the following hold:


  - _𝑉_ ∪ _𝐿_ ⊆ dom(· _[𝐼]_ );

  - for all _𝑣_ ∈ _𝑉_, it holds that _𝑣_ _[𝐼]_ ∈ _𝑉_ Γ;

  - for all _𝑙_ ∈ _𝐿_, it holds that _𝑙_ _[𝐼]_ ∈ _𝐿_ Γ; and

   - for all ( _𝑢,𝑙, 𝑣_ ) ∈ _𝐸_, it holds that ( _𝑢_ _[𝐼]_ _,𝑙_ _[𝐼]_ _, 𝑣_ _[𝐼]_ ) ∈ _𝐸_ Γ.

If _𝐼_ _satisfies 𝐺_ we call _𝐼_ a _(graph) model_ of _𝐺_ .


Next we define models under semantics conditions (e.g., of ontology features).


_Definition B.38 (Semantic condition)._ Let 2 _[𝐺]_ denote the set of all (directed edge-labelled) graphs.
A _semantic condition_ is a mapping _𝜙_ : 2 _[𝐺]_ →{true _,_ false}. An interpretation _𝐼_ ≔ (Γ _,_ - _[𝐼]_ ) is a model
of _𝐺_ under _𝜙_ if and only if _𝐼_ is a model of _𝐺_ and _𝜙_ (Γ). Given a set of semantic conditions Φ, we say
that _𝐼_ is a model of _𝐺_ if and only if _𝐼_ is a model of _𝐺_ and for all _𝜙_ ∈ Φ, _𝜙_ (Γ) is true.


We do not restrict the language used to define semantic conditions, but, for example, we can

define the Has Value semantic condition of Table 5 in FOL as follows:

∀ _𝑐, 𝑝,𝑦_ ��Γ( _𝑐,_ prop _, 𝑝_ ) ∧ Γ( _𝑐,_ value _,𝑦_ )� ↔∀ _𝑥_ �Γ( _𝑥,_ type _,𝑐_ ) ↔ Γ( _𝑥, 𝑝,𝑦_ )��


Here we overload Γ as a ternary predicate to capture the edges of Γ. The above FOL formula defines

an if-and-only-if version of the semantic condition for Has Value. The other semantic conditions

enumerated in Tables 3–5 can be defined in a similar way [466]. [40]


Finally, we can define entailment considering such semantic conditions.


_Definition B.39 (Graph entailment)._ Letting _𝐺_ 1 and _𝐺_ 2 denote two (directed edge-labelled) graphs,
and Φ a set of semantic conditions, we say that _𝐺_ 1 _entails 𝐺_ 2 _under_ Φ – denoted _𝐺_ 1 |=Φ _𝐺_ 2 – if and
only if any model of _𝐺_ 1 under Φ is also a model of _𝐺_ 2 under Φ.


An example of entailment is discussed in Section 4.2. Note that in a slight abuse of notation, we
may simply write _𝐺_ |=Φ ( _𝑠, 𝑝,𝑜_ ) to denote that _𝐺_ entails the edge ( _𝑠, 𝑝,𝑜_ ) under Φ.


40Note that although these tables consider axioms originating in the data graph, it suffices to check their image in the

domain graph since _𝐼_ only satisfies _𝐺_ if the edges of _𝐺_ defining the axioms are reflected in _𝐼_ .


121


Under OWA, entailment is as defined as given in Definition B.39. Under CWA, we make the
additional assumption that if _𝐺_ ̸|=Φ _𝑒_, where _𝑒_ is an edge (strictly speaking, a _positive_ edge), then
_𝐺_ |=Φ ¬ _𝑒_ ; in other words, under CWA we assume that any (positive) edges that _𝐺_ does not entail
under Φ can be assumed false according to _𝐺_ and Φ. [41]


_B.5.2_ _Rules._ Given a graph pattern _𝑄_ - be it a directed edge-labelled graph pattern per Definition B.9 or a property graph pattern per Definition B.11 – recall that Var( _𝑄_ ) denotes the variables

appearing in _𝑄_ . We can now define the notion of a rule for graphs.


_Definition B.40 (Rule)._ A _rule_ is a pair _𝑅_  - ( _𝐵, 𝐻_ ) such that _𝐵_ and _𝐻_ are graph patterns and
Var( _𝐻_ ) ⊆ _𝐵_ . We call _𝐵_ the _body_ of the rule while we call _𝐻_ the _head_ of the rule.


This definition of a rule applies for directed edge-labelled graphs and property graphs by consid
ering the corresponding type of graph pattern. The head is considered to be a conjunction of edges.

Given a graph _𝐺_, a rule is _applied_ by computing the mappings from the body to the graph and then

using those mappings to substitute the variables in _𝐻_ . The restriction Var( _𝐻_ ) ⊆ _𝐵_ ensures that the

results of this substitution is a graph, with no variables in _𝐻_ left unsubstituted.


_Definition B.41 (Rule application)._ Given a rule _𝑅_ = ( _𝐵, 𝐻_ ) and a graph _𝐺_, we define the _application_
_of 𝑅_ _over 𝐺_ as the graph _𝑅_ ( _𝐺_ ) � [�] _𝜇_ ∈ _𝐵_ ( _𝐺_ ) _[𝜇]_ [(] _[𝐻]_ [)][.]


Given a set of rules R � { _𝑅_ 1 _, . . ., 𝑅𝑛_ } and a knowledge graph _𝐺_, towards defining the set of
inferences given by the rules over the graph, we denote by R( _𝐺_ ) � [�] _𝑅_ ∈R _[𝑅]_ [(] _[𝐺]_ [)][ the union of the]
application of all rules of R over _𝐺_, and we denote by R [+] ( _𝐺_ ) � R( _𝐺_ ) ∪ _𝐺_ the extension of _𝐺_ with
respect to the application of R. Finally, we denote by R _[𝑘]_ ( _𝐺_ ) (for _𝑘_ ∈ N [+] ) the recursive application
of R [+] ( _𝐺_ ), where R [1] ( _𝐺_ ) � R [+] ( _𝐺_ ), and R _[𝑖]_ [+][1] ( _𝐺_ ) � R [+] (R _[𝑖]_ ( _𝐺_ )). We are now ready to define the
_least model_, which captures the inferences possible for R over _𝐺_ .


_Definition B.42 (Least model)._ The _least model of_ R _over 𝐺_ is defined as R [∗] ( _𝐺_ ) ≔ [�] _𝑘_ ∈N [(] _[𝑅][𝑘]_ [(] _[𝐺]_ [))][.]


At some point _𝑅_ _[𝑘]_ [′] ( _𝐺_ ) = _𝑅_ _[𝑘]_ [′][+][1] ( _𝐺_ ): the rule applications reach a fixpoint and we have the least
model. Once the least model R [∗] ( _𝐺_ ) is computed, the entailed data can be treated as any other data.


Rules can be used to support graph entailments of the form _𝐺_ 1 |=Φ _𝐺_ 2. We say that a set of rules
R is _correct_ for Φ if, for any graph _𝐺_, _𝐺_ |=Φ R [∗] ( _𝐺_ ). We say that R is _complete_ for Φ if, for any graph
_𝐺_, there does not exist an edge _𝑒_ such that _𝐺_ |=Φ _𝑒_ and _𝑒_ ∉ R [∗] ( _𝐺_ ). Table 6 exemplifies a correct

(but incomplete) set of rules for the semantic conditions laid out by the RDFS standard [70].

Alternatively, rules can be directly specified in a rule language such as Notation3 (N3) [42],

Rule Interchange Format (RIF) [288], Semantic Web Rule Language (SWRL) [254], or SPARQL

Inferencing Notation (SPIN) [295]. Languages such as SPIN represent rules as graphs, allowing the

rules of a knowledge graph to be embedded in the data graph. Taking advantage of this fact, we can
then consider a form of graph entailment _𝐺_ 1 ∪ _𝛾_ (R) |=Φ _𝐺_ 2, where by _𝛾_ (R) we denote the graph
representation of rules R. If the set of rules R is correct and complete for Φ, we may simply write
_𝐺_ 1 ∪ _𝛾_ (R) |= _𝐺_ 2, indicating that Φ captures the same semantics for _𝛾_ (R) as applying the rules in R;
formally, _𝐺_ 1 ∪ _𝛾_ (R) |= R( _𝐺_ 1 ∪ _𝛾_ (R)) and there does not exist an edge _𝑒_ such that _𝐺_ 1 ∪ _𝛾_ (R) |= _𝑒_
but _𝑒_ ∉ R [∗] ( _𝐺_ 1 ∪ _𝛾_ (R)). This allows us to view rules as another form of graph entailment.


41In FOL, the CWA only applies to positive _facts_, whereas edges in a graph can be used to represent other FOL formulae. If

one wished to maintain FOL-compatibility under CWA, additional restrictions on the types of edge _𝑒_ may be needed.


122


_B.5.3_ _Description Logics._ Table 7 provides definitions for all of the constructs typically found

in Description Logics. The syntax column denotes how the construct is expressed in DL. A DL

knowledge base then consists of an A-Box, a T-Box, and an R-Box.


_Definition B.43 (DL knowledge base)._ A _DL knowledge base_ K is defined as a tuple (A _,_ T _,_ R), where
A is the _A-Box_ : a set of assertional axioms; T is the _T-Box_ : a set of class (aka concept/terminological)
axioms; and R is the _R-Box_ : a set of relation (aka property/role) axioms.


The semantics column defines the meaning of axioms using _interpretations_ . These interpretations

are typically defined in a slightly different way to those previously defined for graphs, though the

idea is roughly the same.


_Definition B.44 (DL interpretation)._ A _DL interpretation 𝐼_ is defined as a pair (Δ _[𝐼]_ _,_  - _[𝐼]_ ), where Δ _[𝐼]_ is
the _interpretation domain_, and · _[𝐼]_ is the _interpretation function_ . The interpretation domain is a set of

individuals. The interpretation function accepts a definition of either an individual _𝑎_, a class _𝐶_, or
a relation _𝑅_, mapping them, respectively, to an element of the domain ( _𝑎_ _[𝐼]_ ∈ Δ _[𝐼]_ ), a subset of the
domain ( _𝐶_ _[𝐼]_ ⊆ Δ _[𝐼]_ ), or a set of pairs from the domain ( _𝑅_ _[𝐼]_ ⊆ Δ _[𝐼]_ × Δ _[𝐼]_ ).


An interpretation _𝐼_ _satisfies_ a knowledge-base K if and only if, for all of the syntactic axioms in
K, the corresponding semantic conditions in Table 7 hold for _𝐼_ . In this case, we call _𝐼_ a _model_ of K.


As an example, for K ≔ (A _,_ T _,_ R), let:

  - A ≔ {City(Arica) _,_ City(Santiago) _,_ flight(Arica,Santiago)};

  - T ≔ {City ⊑ Place _,_ ∃flight _._ ⊤⊑∃nearby _._ Airport};

  - R ≔ {flight ⊑ connectsTo}.
For _𝐼_ = (Δ _[𝐼]_ _,_ - _[𝐼]_ ), let:

  - Δ _[𝐼]_ ≔ {� _,_ _,_ �};

  - Arica _[𝐼]_ ≔ �, Santiago _[𝐼]_ ≔, AricaAirport _[𝐼]_ ≔ �;

  - City _[𝐼]_ ≔ {� _,_ }, Airport _[𝐼]_ ≔ {�};

  - flight _[𝐼]_ ≔ {(� _,_ )}, connectsTo _[𝐼]_ ≔ {(� _,_ )}, sells _[𝐼]_ ≔ {(� _,_ �)}.
The interpretation _𝐼_ is not a model of K since it does not have that � is nearby some Airport, nor
that � and are in the class Place. However, if we _extend 𝐼_ with the following:

  - Place _[𝐼]_ ≔ {� _,_ };

  - nearby _[𝐼]_ ≔ {(� _,_ �)}.

Now _𝐼_ is a model of K. Note that although K does not imply that sells(Arica,coffee) while _𝐼_
indicates that � sells �, _𝐼_ is still a model of K since K is not assumed to be a complete description

of the world, as per the Open World Assumption.

Finally, the notion of a model gives rise to the key notion of entailment.


_Definition B.45._ Given two DL knowledge bases K1 and K2, we define that K1 entails K2, denoted
K1 |= K2, if and only if any model of K1 is a model of K2.


The entailment relation tells us which knowledge bases hold as a logical consequence of which

others: if all models of K1 are also models of K2 then, intuitively speaking, K2 says nothing new over
K1. For example, let K1 denote the knowledge base K from the previous example, and define a second
knowledge base with one assertion: K2 ≔ ({connectsTo(Arica _,_ Santiago)} _,_ {} _,_ {}). Though K1
does not assert this axiom, it does entail K2: to be a model of K2, an interpretation must have that
(Arica _[𝐼]_ _,_ Santiago _[𝐼]_ ) ∈ connectsTo _[𝐼]_, but this must also be the case for any interpretation that
satisfies K1 since it must have that (Arica _[𝐼]_ _,_ Santiago _[𝐼]_ ) ∈ flight _[𝐼]_ and flight _[𝐼]_ ⊆ connectsTo _[𝐼]_ .

Unfortunately, the problem of deciding entailment for knowledge bases expressed in the DL

composed of the unrestricted use of all of the axioms of Table 7 combined is undecidable. We could,


123


for example, reduce instances of the Halting Problem to such entailment. Hence DLs in practice

restrict use of the features listed in Table 7. Different DLs then apply different restrictions, implying

different trade-offs for expressivity and the complexity of the entailment problem. Most DLs are

founded on one of the following base DLs (we use indentation to denote derivation):

ALC (A _ttributive_ L _anguage with_ C _omplement_ [464]), supports atomic classes, the top and bottom

classes, class intersection, class union, class negation, universal restrictions and existential

restrictions. Relation and class assertions are also supported.

S extends ALC with transitive closure.

These base languages can be extended as follows:


H adds relation inclusion.

R adds (limited) complex relation inclusion, as well as relation reflexivity, relation irreflexivity,

relation disjointness and the universal relation.

O adds (limited) nomimals.
I adds inverse relations.
F adds (limited) functional properties.

N adds (limited) number restrictions (subsuming F given ⊤).

Q adds (limited) qualified number restrictions (subsuming N given ⊤).

We use “(limited)” to indicate that such features are often only allowed under certain restrictions

to ensure decidability; for example, complex relations (chains) typically cannot be combined with

cardinality restrictions. DLs are then typically named per the following scheme, where [ _𝑎_ | _𝑏_ ] denotes
an alternative between _𝑎_ and _𝑏_ and [ _𝑐_ ][ _𝑑_ ] denotes a concatenation _𝑐𝑑_ :


[ALC|S][H|R][O][I][F |N|Q]


Examples include ALCO, ALCHI, SHIF, SROIQ, etc. These languages often apply addi
tional restrictions on class and property axioms to ensure decidability, which we do not discuss

here. For further details on Description Logics, we refer to the recent book by Baader et al. [23].

As mentioned in the body of the survey, DLs have been very influential in the definition

of OWL, where the OWL 2 DL fragment (roughly) corresponds to the DL SROIQ. For example, the axiom [venue] domain Event in OWL can be translated to ∃venue _._ ⊤⊑ Event, meaning that the class of individuals with some value for venue (in any class) is a sub-class of the
class Event. We leave other translations from the OWL axioms of Tables 3–5 to DL as an ex
expressed in DL: “subTaxonOf ⊑⊑” is not syntactically valid. Hence only a subset of graphs can

be translated into well-formed DL ontologies; we refer to the OWL standard for details [239].


**B.6** **Inductive Knowledge**


We provide further discussion and formal definitions relating to graph parallel frameworks, knowl
edge graph embeddings, and graph neural networks, as discussed in Section 5.


_B.6.1_ _Graph parallel frameworks._ Before defining a graph parallel framework, in the interest of

generality, we first define a directed graph labelled with feature vectors, which captures the type of

input that such a framework can accept, with vectors assigned to both nodes and edges.


_Definition B.46 (Directed vector-labelled graph)._ We define a _directed vector-labelled graph 𝐺_ =
( _𝑉, 𝐸, 𝐹, 𝜆_ ), where _𝑉_ is a set of nodes, _𝐸_ ⊆ _𝑉_ × _𝑉_ is a set of edges, _𝐹_ is a set of feature vectors, and
_𝜆_ : _𝑉_ ∪ _𝐸_ → _𝐹_ labels each node and edge with a feature vector.


42Though not previously mentioned, OWL defines classes Thing and Nothing that correspond to ⊤ and ⊥, respectively.


124


Table 7. Description Logic semantics (such that _𝑥,𝑦,𝑧,𝑎_ _[𝐼]_ _,𝑎_ _[𝐼]_ 1 _[, . . . 𝑎][𝐼𝑛][,𝑏][𝐼]_ [are in][ Δ] _[𝐼]_ [)]


**Name** **Syntax** **Semantics** (· _[𝐼]_ )


Class Definitions


Atomic Class _𝐴_ _𝐴_ _[𝐼]_ (a subset of Δ _[𝐼]_ )
Top Class ⊤ Δ _[𝐼]_

Bottom Class ⊥ ∅
Class Negation ¬ _𝐶_ Δ _[𝐼]_ \ _𝐶_ _[𝐼]_

Class Intersection _𝐶_ ⊓ _𝐷_ _𝐶_ _[𝐼]_ ∩ _𝐷_ _[𝐼]_

Class Union _𝐶_ ⊔ _𝐷_ _𝐶_ _[𝐼]_ ∪ _𝐷_ _[𝐼]_

Nominal { _𝑎_ 1 _, ...,𝑎𝑛_ } { _𝑎_ _[𝐼]_ 1 _[, ...,𝑎]_ _𝑛_ _[𝐼]_ [}]
Existential Restriction ∃ _𝑅.𝐶_ { _𝑥_ | ∃ _𝑦_ : ( _𝑥,𝑦_ ) ∈ _𝑅_ _[𝐼]_ and _𝑦_ ∈ _𝐶_ _[𝐼]_ }
Universal Restriction ∀ _𝑅.𝐶_ { _𝑥_ | ∀ _𝑦_ : ( _𝑥,𝑦_ ) ∈ _𝑅_ _[𝐼]_ implies _𝑦_ ∈ _𝐶_ _[𝐼]_ }
Self Restriction ∃ _𝑅._ Self { _𝑥_ | ( _𝑥,𝑥_ ) ∈ _𝑅_ _[𝐼]_ }
Number Restriction _★𝑛𝑅_ (where _★_ ∈{≥ _,_ ≤ _,_ =}) { _𝑥_ | #{ _𝑦_ : ( _𝑥,𝑦_ ) ∈ _𝑅_ _[𝐼]_ } _★_ _𝑛_ }
Qualified Number Restriction _★𝑛𝑅.𝐶_ (where _★_ ∈{≥ _,_ ≤ _,_ =}) { _𝑥_ | #{ _𝑦_ : ( _𝑥,𝑦_ ) ∈ _𝑅_ _[𝐼]_ and _𝑦_ ∈ _𝐶_ _[𝐼]_ } _★_ _𝑛_ }


Class Axioms (T-Box)


Class Inclusion _𝐶_ ⊑ _𝐷_ _𝐶_ _[𝐼]_ ⊆ _𝐷_ _[𝐼]_


Relation Definitions


Relation _𝑅_ _𝑅_ _[𝐼]_ (a subset of Δ _[𝐼]_ × Δ _[𝐼]_ )
Inverse Relation _𝑅_ [−] {( _𝑦,𝑥_ ) | ( _𝑥,𝑦_ ) ∈ _𝑅_ _[𝐼]_ }
Universal Relation U Δ _[𝐼]_ × Δ _[𝐼]_


Relation Axioms (R-Box)


Relation Inclusion _𝑅_ ⊑ _𝑆_ _𝑅_ _[𝐼]_ ⊆ _𝑆_ _[𝐼]_

Complex Relation Inclusion _𝑅_ 1 ◦ _..._  - _𝑅𝑛_ ⊑ _𝑆_ _𝑅_ 1 _[𝐼]_ [◦] _[...]_ [ ◦] _[𝑅]_ _𝑛_ _[𝐼]_ [⊆] _[𝑆][𝐼]_

Transitive Relations Trans( _𝑅_ ) _𝑅_ _[𝐼]_  - _𝑅_ _[𝐼]_ ⊆ _𝑅_ _[𝐼]_

Functional Relations Func( _𝑅_ ) {( _𝑥,𝑦_ ) _,_ ( _𝑥,𝑧_ )} ⊆ _𝑅_ _[𝐼]_ implies _𝑦_ = _𝑧_
Reflexive Relations Ref( _𝑅_ ) for all _𝑥_ : ( _𝑥,𝑥_ ) ∈ _𝑅_ _[𝐼]_

Irreflexive Relations Irref( _𝑅_ ) for all _𝑥_ : ( _𝑥,𝑥_ ) ∉ _𝑅_ _[𝐼]_

Symmetric Relations Sym( _𝑅_ ) _𝑅_ _[𝐼]_ = ( _𝑅_ [−] ) _[𝐼]_

Asymmetric Relations Asym( _𝑅_ ) _𝑅_ _[𝐼]_ ∩( _𝑅_ [−] ) _[𝐼]_ = ∅
Disjoint Relations Disj( _𝑅,𝑆_ ) _𝑅_ _[𝐼]_ ∩ _𝑆_ _[𝐼]_ = ∅


Assertional Definitions


Individual _𝑎_ _𝑎_ _[𝐼]_


Assertional Axioms (A-Box)


Relation Assertion _𝑅_ ( _𝑎,𝑏_ ) ( _𝑎_ _[𝐼]_ _,𝑏_ _[𝐼]_ ) ∈ _𝑅_ _[𝐼]_

Negative Relation Assertion ¬ _𝑅_ ( _𝑎,𝑏_ ) ( _𝑎_ _[𝐼]_ _,𝑏_ _[𝐼]_ ) ∉ _𝑅_ _[𝐼]_

Class Assertion _𝐶_ ( _𝑎_ ) _𝑎_ _[𝐼]_ ∈ _𝐶_ _[𝐼]_

Equality _𝑎_ = _𝑏_ _𝑎_ _[𝐼]_ = _𝑏_ _[𝐼]_

Inequality _𝑎_ ≠ _𝑏_ _𝑎_ _[𝐼]_ ≠ _𝑏_ _[𝐼]_


A directed-edge labelled graph or a property graph may be encoded as a directed vector-labelled

graph in a number of ways, depending on the application. The type of node and/or a selection of its

attributes may be encoded in the node feature vectors, while the label of an edge and/or a selection

of its attributes may be encoded in the edge feature vector (including, for example, weights applied

to edges). Typically node feature vectors will all have the same dimensionality, as will edge feature


125


vectors. The directed vector-labelled graph can thus be seen as defining the initial state and features

that will be used as input for the graph parallel framework.


_Example B.47._ We define a directed vector-labelled graph in preparation for later computing

PageRank using a graph parallel framework. Let _𝐺_ = ( _𝑉, 𝐸, 𝐿_ ) denote a directed edge-labelled
graph. Let | _𝐸_ ( _𝑢_ )| denote the outdegree of node _𝑢_ ∈ _𝑉_ . We then initialise a directed vector-labelled
graph _𝐺_ [′] = ( _𝑉, 𝐸_ [′] _, 𝐹, 𝜆_ ) such that _𝐸_ [′] = {( _𝑥,𝑧_ ) | ∃ _𝑦_ : ( _𝑥,𝑦,𝑧_ ) ∈ _𝐸_ }, and for all _𝑢_ ∈ _𝑉_, we define







_𝜆_ ( _𝑢_ ) ≔




1
| _𝑉_ |
| _𝐸_ [′] ( _𝑢_ )|
| _𝑉_ |



, and _𝜆_ ( _𝑢, 𝑣_ ) ≔ ��, with _𝐹_ ≔ { _𝜆_ ( _𝑢_ ) | _𝑢_ ∈ _𝑉_ } ∪{ _𝜆_ ( _𝑢, 𝑣_ ) | ( _𝑢, 𝑣_ ) ∈ _𝐸_ ′}, assigning



each node a vector containing its initial PageRank score, the outdegree of the node, and the number

of nodes in the graph. Conversely, edge-vectors are not used in this case.



We are now ready to define a graph parallel framework operating over a directed vector-labelled

graph. In the following we use {{·}} to denote a multiset (an unordered set preserving duplicates),
2 _[𝑆]_ [→][N] to denote the set of all multisets containing (only) elements from the set _𝑆_, and R _[𝑎]_ to denote

the set of all vectors of dimension _𝑎_ (i.e., the set of all vectors containing _𝑎_ real-valued elements).


_Definition B.48 (Graph parallel framework)._ A _graph parallel framework_ ( _GPF_ ) is a triple of

functions 𝔊≔ (Msg _,_ Agg _,_ End) such that (with _𝑎,𝑏,𝑐_ ∈ N):




- Msg : R _[𝑎]_ × R _[𝑏]_ → R _[𝑐]_




- Agg : R _[𝑎]_ × 2 [R] _[𝑐]_ [→][N] → R _[𝑎]_




- End : 2 [R] _[𝑎]_ [→][N] →{true _,_ false}



The function Msg defines what message (i.e., vector) must be passed from a node to a neighbour
ing node along a particular edge, given the current feature vectors of the node and the edge; the

function Agg is used to compute a new feature vector for a node, given its previous feature vector

and incoming messages; the function End defines a condition for termination of vector computation.

The integers _𝑎_, _𝑏_ and _𝑐_ denote the dimensions of node feature vectors, edge feature vectors, and

message vectors, respectively; we assume that _𝑎_ and _𝑏_ correspond with the dimensions of input

feature vectors for nodes and edges. Given a GPF 𝔊= (Msg _,_ Agg _,_ End), a directed vector-labelled
graph _𝐺_ = ( _𝑉, 𝐸, 𝐹, 𝜆_ ), and a node _𝑢_ ∈ _𝑉_, we define the output vector assigned to node _𝑢_ in _𝐺_ by 𝔊
(written 𝔊( _𝐺,𝑢_ )) as follows. First let n _𝑢_ [(][0][)] ≔ _𝜆_ ( _𝑢_ ). For all _𝑖_ ≥ 1, let:


��                          - ��
_𝑀𝑢_ [(] _[𝑖]_ [)] ≔ Msg n _𝑣_ [(] _[𝑖]_ [−][1][)] _, 𝜆_ ( _𝑣,𝑢_ )��� ( _𝑣,𝑢_ ) ∈ _𝐸_


                       -                        n _𝑢_ [(] _[𝑖]_ [)] ≔ Agg n _𝑢_ [(] _[𝑖]_ [−][1][)] _, 𝑀𝑢_ [(] _[𝑖]_ [)]


If _𝑗_ is the smallest integer for which End({{n _𝑢_ [(] _[𝑗]_ [)] | _𝑢_ ∈ _𝑉_ }}) is true, then 𝔊( _𝐺,𝑢_ ) ≔ n _𝑢_ [(] _[𝑗]_ [)] [.]

This particular definition assumes that vectors are dynamically computed for nodes, and that

messages are passed only to outgoing neighbours, but the definitions can be readily adapted to

consider dynamic vectors for edges, or messages being passed to incoming neighbours, etc. We

now provide an example instantiating a GPF to compute PageRank over a directed graph.


_Example B.49._ We take as input the directed vector labelled graph _𝐺_ [′] = ( _𝑉, 𝐸, 𝐹, 𝜆_ ) from Exam
ple B.47 for a PageRank GPF. First we define the messages passed from _𝑢_ to _𝑣_ :




            - _𝑑_ (n _𝑣_ )1
Msg (n _𝑣, 𝜆_ ( _𝑣,𝑢_ )) ≔ (n _𝑣_ )2







where _𝑑_ denotes PageRank’s constant dampening factor (typically _𝑑_ ≔ 0 _._ 85) and (n _𝑣_ ) _𝑘_ denotes the
_𝑘_ [th] element of the n _𝑣_ vector. In other words, _𝑣_ will pass to _𝑢_ its PageRank score multiplied by the


126


dampening factor and divided by its degree (we do not require _𝜆_ ( _𝑣,𝑢_ ) in this particular example).

Next we define the function for _𝑢_ to aggregate the messages it receives from other nodes:



(n _𝑢_ )3 m∈ _𝑀𝑢_ 1

Agg (n _𝑢, 𝑀𝑢_ ) ≔ (n _𝑢_ )2

(n _𝑢_ )3

 


Here, we sum the scores received from other nodes along with its share of rank from the dampening

factor, copying over the node’s degree and the total number of nodes for future use. Finally, there

are a number of ways that we could define the termination condition; here we simply define:


End({{n _𝑢_ [(] _[𝑖]_ [)] | _𝑢_ ∈ _𝑉_ }}) ≔ ( _𝑖_ ≥ z)


where z is a fixed number of iterations, at which point the process stops.


We may note in this example that the total number of nodes is duplicated in the vector for each

node of the graph. Part of the benefit of GPFs is that only local information in the neighbourhood of

the node is required for each computation step. In practice, such frameworks may allow additional

features, such as global computation steps whose results are made available to all nodes [335],

operations that dynamically modify the graph [335], etc.


_B.6.2_ _Knowledge graph embeddings._ As discussed in Section 5.2, knowledge graph embeddings
represent graphs in a low-dimensional numeric space. [43] Before defining the key notions, we

introduce mathematical objects related to tensor calculus, on which embeddings heavily rely.


_Definition B.50 (Vector, matrix, tensor, order, mode)._ For any positive integer _𝑎_, a _vector_ of dimen
sion _𝑎_ is a family of real numbers indexed by integers in {1 _, . . .,𝑎_ }. For _𝑎_ and _𝑏_ positive integers, an
( _𝑎,𝑏_ )-matrix is a family of real numbers indexed by pairs of integers in {1 _, . . .,𝑎_ }×{1 _, . . .,𝑏_ }. A ten
sor is a family of real numbers indexed by a finite sequence of integers such that there exist positive

numbers _𝑎_ 1 _, . . .,𝑎𝑛_ such that the indices are all the tuples of numbers in {1 _, . . .,𝑎_ 1}× _. . ._ ×{1 _, . . .,𝑎𝑛_ }.
The number _𝑛_ is called the _order_ of the tensor, the subindices _𝑖_ ∈{1 _, . . .,𝑛_ } indicate the _mode_ of a
tensor, and each _𝑎𝑖_ defines the dimension of the _𝑖_ [th] mode. A 1-order tensor is a vector and a 2-order

tensor is a matrix. We denote the set of all tensors as T.


For specific dimensions _𝑎_ 1 _, . . .,𝑎𝑛_ of modes, a tensor is an element of (· · · (R _[𝑎]_ [1] ) _[...]_ ) _[𝑎][𝑛]_ but we write
R _[𝑎]_ [1] _[,...,𝑎][𝑛]_ to simplify the notation. We use lower-case bold font to denote vectors (x ∈ R _[𝑎]_ ), upper-case
bold font to denote matrices (X ∈ R _[𝑎,𝑏]_ ) and calligraphic font to denote tensors (X ∈ R _[𝑎]_ [1] _[,...,𝑎][𝑛]_ ).


Now we are ready to abstractly define knowledge graph embeddings.


_Definition B.51 (Knowledge graph embedding)._ Given a directed edge-labelled graph _𝐺_ = ( _𝑉, 𝐸, 𝐿_ ),
a _knowledge graph embedding of 𝐺_ is a pair of mappings ( _𝜀, 𝜌_ ) such that _𝜀_ : _𝑉_ → T and _𝜌_ : _𝐿_ → T.


In the most typical case, _𝜀_ and _𝜌_ map nodes and edge-labels, respectively, to vectors of fixed

dimension. In some cases, however, they may map to matrices. Given this abstract notion of a

knowledge graph embedding, we can then define a plausibility score.


_Definition B.52 (Plausibility)._ A _plausibility scoring function_ is a partial function _𝜙_ : T×T×T → R.
Given a directed edge-labelled graph _𝐺_ = ( _𝑉, 𝐸, 𝐿_ ), an edge ( _𝑠, 𝑝,𝑜_ ) ∈ _𝑉_ × _𝐿_ × _𝑉_, and a knowledge
graph embedding ( _𝜀, 𝜌_ ) of _𝐺_, the plausibility of ( _𝑠, 𝑝,𝑜_ ) is given as _𝜙_ ( _𝜀_ ( _𝑠_ ) _, 𝜌_ ( _𝑝_ ) _,𝜀_ ( _𝑜_ )).


43To the best of our knowledge, the term “ _knowledge graph embedding_ ” was coined by Wang et al. [553] in order to distinguish

the case from a “graph embedding” that considers a single relation (i.e., an undirected or directed graph). Earlier papers

rather used the phrase “ _multi-relational data_ ” [63, 192, 386].


127



Agg (n _𝑢, 𝑀𝑢_ ) ≔




1− _𝑑_
(n _𝑢_ )3 [+][ �] m∈ _𝑀𝑢_ [(][m][)] 1
(n _𝑢_ )2
(n _𝑢_ )3


Edges with higher scores are considered to be more plausible. Given a graph _𝐺_ = ( _𝑉, 𝐸, 𝐿_ ), we
assume a set of positive edges _𝐸_ [+] and a set of negative edges _𝐸_ [−] . Positive edges are often simply
the edges in the graph: _𝐸_ [+] ≔ _𝐸_ . Negative edges use the vocabulary of _𝐺_ (i.e., _𝐸_ [−] ⊆ _𝑉_ × _𝐿_ × _𝑉_ ) and
typically are defined by taking edges ( _𝑠, 𝑝,𝑜_ ) from _𝐸_ and changing one of the terms of each edge –

most often, but not always, one of the nodes – such that the edge is no longer in _𝐸_ . Given sets of

positive and negative edges, and a plausibility scoring function, the objective is then to find the
embedding that maximises the plausibility of edges in _𝐸_ [+] while minimising the plausibility of edges
in _𝐸_ [−] . Specific knowledge graph embeddings then instantiate the type of embedding considered

and the plausibility scoring function in (a wide variety of) different ways.

In Table 8, we define the plausibility scoring function used by different models for knowledge

graph embeddings, and further provide details of the types of embeddings considered. To simplify

the definitions of embeddings given in Table 8, we will use e _𝑥_ to denote _𝜀_ ( _𝑥_ ) when it is a vector,
and we will use r _𝑦_ to denote _𝜌_ ( _𝑦_ ) when it is a vector and R _𝑦_ to denote _𝜌_ ( _𝑦_ ) when it is a matrix.

Some models use additional parameters (aka weights) that – although they do not form part of the

entity/relation embeddings – are learnt to compute the plausibility score from the embeddings. We

denote these as v, V, V, w, W W (for vectors, matrices or tensors). We use _𝑑𝑒_ and _𝑑𝑟_ to denote

the dimensionality chosen for entity embeddings and relation embeddings, respectively. Often it

is assumed that _𝑑𝑒_ = _𝑑𝑟_, in which case we will write _𝑑_ . Sometimes weights may have their own

dimensionality, which we denote _𝑤_ . The embeddings in Table 8 use a variety of operators on

vectors, matrices and tensors. In the interest of keeping the discussion self-contained, we refer to

the latter part of this section for definitions of these operators and other conventions used.

The embeddings listed in Table 8 vary in complexity, ranging from simple models such as

TransE [63] and DistMult [568], to more complex ones, such as SME Bilinear [192] and ConvE [127].

A trade-off underlies these proposals in terms of the number of parameters used, where more

parameters increases computational costs, but increases the expressiveness of the model in terms of

the model’s capability to capture latent features of the graph. To increase expressivity, many of the

models in Table 8 use additional parameters beyond the embeddings themselves. A possible formal
guarantee of such models is _full expressiveness_, which, given any disjoint sets of positive edges _𝐸_ [+]

and negative edges _𝐸_ [−], asserts that the model can always correctly partition those edges. On the

one hand, for example, DistMult [568] cannot distinguish an edge [s] p - from its inverse [o] p s,
so by adding an inverse of an edge in _𝐸_ [+] to _𝐸_ [−], we can show that it is _not_ fully expressive. On the

other hand, models such as ComplEx [526], SimplE [283], and TuckER [30] have been proven to be

fully expressive given sufficient dimensionality; for example, TuckER [30] with dimensions _𝑑𝑟_ = | _𝐿_ |
and _𝑑𝑒_ = | _𝑉_ | trivially satisfies full expressivity since its core tensor W then has sufficient capacity

to store the full one-hot encoding of any graph. This formal property is useful to show that the

model does not have built-in limitations for numerically representing a graph, though of course in

practice the dimensions needed to reach full expressivity are often impractical/undesirable.

Here we have not discussed language models for embedding [96, 441], which are based on a

distinct set of principles, or entailment-aware models [125, 207, 550], which add additional scoring

constraints on top of the types of models listed in Table 8. For further information on such works,

we refer to the survey by Wang et al. [549] and/or the corresponding papers.


We continue by defining in detail the operators and conventions used in Table 8. We start with

the conventions used, thereafter defining the pertinent operators.


  - We use indexed parentheses – such as (x) _𝑖_, (X) _𝑖𝑗_, or (X) _𝑖_ 1 _...𝑖𝑛_   - to denote elements of vectors,
matrices, and tensors, respectively. If a vector x ∈ R _[𝑎]_ is used in a context that requires a
matrix, the vector is interpreted as an ( _𝑎,_ 1)-matrix (i.e., a column vector) and can be turned
into a row vector (i.e., a (1 _,𝑎_ )-matrix) using the transpose operation x _[𝑇]_ . We use x [D] ∈ R _[𝑎,𝑎]_ to


128


Table 8. Details for selected knowledge graph embeddings, including the plausibility scoring function
_𝜙_ ( _𝜀_ ( _𝑠_ ) _, 𝜌_ ( _𝑝_ ) _,𝜀_ ( _𝑜_ )) for edge _[𝑠]_ _𝑝_ _𝑜_, and other conditions applied


**Model** _𝜙_ ( _𝜀_ ( _𝑠_ ) _, 𝜌_ ( _𝑝_ ) _,𝜀_ ( _𝑜_ )) **Conditions** (for all _𝑥_ ∈ _𝑉_, _𝑦_ ∈ _𝐿_ )


TransE [63] −∥e _𝑠_ + r _𝑝_ - e _𝑜_ ∥ _𝑞_ e _𝑥_ ∈ R _[𝑑]_, r _𝑦_ ∈ R _[𝑑]_, _𝑞_ ∈{1 _,_ 2}, ∥e _𝑥_ ∥2 = 1


e _𝑥_ ∈ R _[𝑑]_, r _𝑦_ ∈ R _[𝑑]_, w _𝑦_ ∈ R _[𝑑]_,
TransH [553] −∥(e _𝑠_ −(e _𝑠_ [T] w _𝑝_ )w _𝑝_ ) + r _𝑝_ −(e _𝑜_ −(e _𝑜_ [T] w _𝑝_ )w _𝑝_ ) ∥ [2] 2 ∥w _𝑦_ ∥2 = 1, w∥r [T] _𝑦𝑦_ r∥ _𝑦_ 2 [≈] [0,][ ∥][e] _[𝑥]_ [∥][2][ ≤] [1]


e _𝑥_ ∈ R _[𝑑][𝑒]_, r _𝑦_ ∈ R _[𝑑][𝑟]_, W _𝑦_ ∈ R _[𝑑][𝑟]_ _[,𝑑][𝑒]_,
TransR [271] −∥W _𝑝_ e _𝑠_ + r _𝑝_ - W _𝑝_ e _𝑜_ ∥ [2] 2 ∥e _𝑥_ ∥2 ≤ 1, ∥r _𝑦_ ∥2 ≤ 1, ∥W _𝑦_ e _𝑥_ ∥2 ≤ 1


e _𝑥_ ∈ R _[𝑑][𝑒]_, r _𝑦_ ∈ R _[𝑑][𝑟]_, w _𝑥_ ∈ R _[𝑑][𝑒]_, w _𝑦_ ∈ R _[𝑑][𝑟]_,
TransD [271] −∥(w _𝑝_ ⊗ w _𝑠_ + I)e _𝑠_ + r _𝑝_ −(w _𝑝_ ⊗ w _𝑜_ + I)e _𝑜_ ∥ [2] 2 ∥e _𝑥_ ∥2 ≤ 1, ∥r _𝑦_ ∥2 ≤ 1, ∥(w _𝑦_ ⊗ w _𝑥_ + I)e _𝑥_ ∥2 ≤ 1


RotatE [511] −∥e _𝑠_ ⊙ r _𝑝_ - e _𝑜_ ∥2 e _𝑥_ ∈ C _[𝑑]_, r _𝑦_ ∈ C _[𝑑]_, ∥r _𝑦_ ∥2 = 1


RESCAL [386] e _𝑠_ [T] R _𝑝_ e _𝑜_ e _𝑥_ ∈ R _[𝑑]_, R _𝑦_ ∈ R _[𝑑,𝑑]_, ∥e _𝑥_ ∥2 ≤ 1, ∥R _𝑦_ ∥2 _,_ 2 ≤ 1


DistMult [568] e _𝑠_ [T] r _𝑝_ [D] e _𝑜_ e _𝑥_ ∈ R _[𝑑]_, r _𝑦_ ∈ R _[𝑑]_, ∥e _𝑥_ ∥2 = 1, ∥r _𝑦_ ∥2 ≤ 1


HolE [385] r _𝑝_ [T] (e _𝑠_ _★_ e _𝑜_ ) e _𝑥_ ∈ R _[𝑑]_, r _𝑦_ ∈ R _[𝑑]_, ∥e _𝑥_ ∥2 ≤ 1, ∥r _𝑦_ ∥2 ≤ 1


ComplEx [526] Re(e _𝑠_ [T] r _𝑝_ [D] ~~e~~ _𝑜_ ) e _𝑥_ ∈ C _[𝑑]_, r _𝑦_ ∈ C _[𝑑]_, ∥e _𝑥_ ∥2 ≤ 1, ∥r _𝑦_ ∥2 ≤ 1


SimplE [283] e _𝑠_ [T] r _𝑝_ [D] w _𝑜_ +e _𝑜_ [T] w _𝑝_ [D] w _𝑠_ e _𝑥_ ∈ R _[𝑑]_, r _𝑦_ ∈ R _[𝑑]_, w _𝑥_ ∈ R _[𝑑]_, w _𝑦_ ∈ R _[𝑑]_,

2 ∥e _𝑥_ ∥2 ≤ 1, ∥w _𝑥_ ∥2 ≤ 1, ∥r _𝑦_ ∥2 ≤ 1 _,_ ∥w _𝑦_ ∥2 ≤ 1


TuckER [30] W ⊗1 e _𝑠_ [T] ⊗2 r _𝑝_ [T] ⊗3 e _𝑜_ [T] e _𝑥_ ∈ R _[𝑑][𝑒]_, r _𝑦_ ∈ R _[𝑑][𝑟]_, W ∈ R _[𝑑][𝑒]_ _[,𝑑][𝑟]_ _[,𝑑][𝑒]_


SME Linear [192] (Ve _𝑠_ + V [′] r _𝑝_ + v) [T] (We _𝑜_ + W [′] r _𝑝_ + w) e _𝑥_ ∈ R _[𝑑]_, r _𝑦_ ∈ R _[𝑑]_, v ∈ R _[𝑤]_, w ∈ R _[𝑤]_, ∥e _𝑥_ ∥2 = 1,
V ∈ R _[𝑤,𝑑]_ _,_ V [′] ∈ R _[𝑤,𝑑]_ _,_ W ∈ R _[𝑤,𝑑]_ _,_ W [′] ∈ R _[𝑤,𝑑]_

SME Bilinear [192] ((V ⊗3 r _𝑝_ [T] )e _𝑠_ + v) [T] ((W ⊗3 r _𝑝_ [T] )e _𝑜_ + w) eV ∈ _𝑥_ ∈ RR _[𝑑][𝑤,𝑑,𝑑]_, r _𝑦_, W ∈∈ R _[𝑑]_, vR ∈ _[𝑤,𝑑,𝑑]_ R _[𝑤]_, w ∈ R _[𝑤]_, ∥e _𝑥_ ∥2 = 1,




               - �e _𝑠_
NTN [488] r _𝑝_ [T] _𝜓_ e _𝑠_ [T] We _𝑜_ + W
e _𝑜_




- - e _𝑥_ ∈ R _[𝑑]_, r _𝑦_ ∈ R _[𝑑]_, w ∈ R _[𝑤]_, W ∈ R _[𝑤,]_ [2] _[𝑑]_,
+ w W ∈ R _[𝑑,𝑤,𝑑]_, ∥e _𝑥_ ∥2 ≤ 1, ∥r _𝑦_ ∥2 ≤ 1,
∥w ∥2 ≤ 1, ∥W ∥2 _,_ 2 ≤ 1, ∥W1 [[·] ≤ [:] _𝑖_ _[𝑖]_ [:] ≤ [·]] _𝑤_ [∥][2] _[,]_ [2][ ≤] [1]


e _𝑥_ ∈ R _[𝑑]_, r _𝑦_ ∈ R _[𝑑]_, v ∈ R _[𝑤]_, w ∈ R _[𝑤]_, W ∈ R _[𝑤,]_ [3] _[𝑑]_

∥e _𝑥_ ∥2 ≤ 1 ∥r _𝑦_ ∥2 ≤ 1



e _𝑠_

MLP [131] v [T] _𝜓_ [�] W r _𝑝_

            -  

e _𝑜_

            -  



+ w [�]

  
  



 