<!-- Source: 17-KG_Reasoning_Logics_Embeddings_Survey.pdf | Chunk 1/1 -->

## Knowledge Graph Reasoning with Logics and Embeddings: Survey and Perspective

Wen Zhang [1][∗], Jiaoyan Chen [2], Juan Li [4], Zezhong Xu [4], Jeff Z. Pan [3] and Huajun Chen [4][,][5][,][6][∗]

1School of Software Technology, Zhejiang University
2Department of Computer Science, University of Oxford
3School of Informatics, The University of Edinburgh
4College of Computer Science and Technology, Zhejiang University
5Alibaba-Zhejiang University Joint Research Institute of Frontier Technologies
6Hangzhou Innovation Center, Zhejiang University



Abstract


Knowledge graph (KG) reasoning is becoming increasingly popular in both academia and industry. Conventional KG reasoning based on symbolic
logic is deterministic, with reasoning results being
explainable, while modern embedding-based reasoning can deal with uncertainty and predict plausible knowledge, often with high efficiency via vector computation. A promising direction is to integrate both logic-based and embedding-based methods, with the vision to have advantages of both. It
has attracted wide research attention with more and
more works published in recent years. In this paper,
we comprehensively survey these works, focusing
on how logics and embeddings are integrated. We
first briefly introduce preliminaries, then systematically categorize and discuss works of logic and
embedding-awareKG reasoning from different perspectives, and finally conclude and discuss the challenges and further directions.


1 Introduction


Knowledge representation and reasoning plays a critical
role in many domains, especially Artificial Intelligence(AI).
Knowledge graph (KG), representing facts in the form of
triples, with vocabulary defined in a schema (also known as
ontology), is a simple yet efficient and increasingly popular way of knowledge representation. Many general-purpose
and domain-specific KGs, such as Wikidata and SNOMED
Clinical Terms are under fast development and widely used.
Reasoning, which aims to discover implicit knowledge, can
significantly boost the usage of KGs in many applications
such as question answering and assist KG curation by e.g.,
link prediction. Conventional KG reasoning is often based
on symbolic logics and is deductive. For example, HermiT [Glimm et al., 2014] is a classic description logic reasoner for OWL [1] ontologies; RDFox [Nenov et al., 2015] is a
famous KG storage supporting Datalog rule reasoning. Re

∗Corresponding Authors.
[1Web Ontology Language. https://www.w3.org/OWL/](https://www.w3.org/OWL/)



cently, with the fast development of deep learning, KG embedding, which represents entities and relations as vectors
(embeddings) with their relationships reflected, shows great
success in KG reasoning, especially in inductive reasoning
without pre-defined logics. Logic-based reasoning is usually
interpretable and transferable, while embedding-based reasoning can deal with uncertainty and data noise, and is able to
predict non-determined but plausible knowledge. Thus flourishing research has been conducted to integrate logics and
embeddings for more robust KG reasoning.
There are several survey papers about both KG and neuralsymbolic integration. [Li et al., 2020] focuses on combing symbolic reasoning with statistical reasoning, while

[Zhang et al., 2021a] reviews papers on symbolic, neural, and
hybrid reasoning. Unlike these papers, our survey has a more
specific topic, focusing on logics and KG embeddings, and
has a more fine-grained categorization to these studies, from
two general perspectives: (i) injecting logics, such as logical rules and ontological schemas, into embedding learning,
and (ii) utilizing KG embeddings for logic reasoning-relevant
tasks, such as query answering, theorem proving and rule
mining. More importantly, we analyze and compare methods of each category from some more fine-grained perspectives, including logic types, the existence of pre-defined logics, integration stages, and integration mechanisms. The survey also introduces the challenges and discusses the potential
directions. All these are beneficial for future research on KG
reasoning as well as KG construction, KG application, and
neural-symbolic integration.
The remainder of the paper is organized as follows. Section 2 briefly introduces the background on logic-based and
embedding-based KG reasoning. Section 3 reviews methods
that utilize logics for augmenting embeddings. Section 4 reviews methods of using embeddings for supporting reasoning
tasks. Section 5 analyzes the challenges and discusses the future directions.

2 Background
Reasoning with Logics Given a KG G, logical reasoning can be used to infer new implicit knowledge or to detect inconsistencies. Many might be familiar with logical
rules. One rule, which can be simply represented asB1 B2 ... Bn, means that the head atom H can be inferred H ←
∧ ∧ ∧


by the body atoms B1, ..., Bn. For example, isfatherOf(X, Y)
← Male(X) ∧ isParentOf(X, Y) means that if X is a male, and
X is a parent of Y, then X is the father of Y . In addition to
rules, the Web Ontology Language OWL 2, which is based on
Description Logics (DLs), is a key standard schema language
of KGs. It is based on the SROIQ DL [Horrocks et al., ].
OWL 2 provides rich expressive power, including a
strong support for datatypes [Pan and Horrocks, 2006] and
rules [Kr¨otzsch et al., 2008]. OWL 2 schema can be used to
define class hierarchies, complex classes and relations, domain and range for relations, and more complex schema axioms. Logic languages allow deductive reasoning, such as
consistency checking, materialization, query answering, as
well as inductive and abductive reasoning.


Reasoning with Embeddings KG embedding (KGE), as
a kind of representation learning technique, aims to represent entities and relations by vectors with their semantics
(e.g., relationships) preserved in the vector space. With the
embeddings, implicit and new knowledge can be inferred,
often with approximation or prediction. Many successful
KGE methods, such as TransE [Bordes et al., 2013], ComplEx [Trouillon et al., 2016] and RotatE [Sun et al., 2019],
have been developed in the past decade. A KGE method is
usually composed of a score function φ() which defines how
to compute the truth value based on entity and relation embeddings, and a loss function that maximizes the truth value
of explicit positive triples and minimizes values of generated
negative triples. Take TransE [Bordes et al., 2013] as an example, it makesh, r, and t are vectors of ||h+r−t h, r|| as score function of triples, where, and t in the Euclidean space,
respectively. The embeddings are learned based on a margin
loss that tried to maximize the margin between truth value
of possitive and negative triples. Finally, KGEs can be used
to query triples, infer new triples and discover inconsistency
between triples.


3 Logics for Embeddings


Though KGE methods have achieved great success, they still
suffer from the following problems: 1) they could fail to embed complex semantics such as relationships by logical rules;
2) they usually ignore the ontological schema of a KG as inputs; 3) most of them build black-box models with a shortage of explanation. Integrating logics into embeddings is expected to solve these problems. Before analyzing concrete
methods of such KG embedding, we first introduce the perspectives that are considered in categorization and discussion:


Logic Types We consider two mainstream logic forms used
in KG reasoning: (1) logic rules and (2) Ontological schema,
such as those supported by OWL 2, which can internalize
most logic rules, with some exceptions, such as those with
loops in the body [Kr¨otzsch et al., 2008].


Pre-defined logics 1) With: injecting predefined logics or
their reasoning results into embeddings, and/or applying ontological axioms as constraints. 2) Without: injecting the concept of logics into embeddings, where logics are assumed existing in the KG while no specific data of logics are used.



Integration Stages Considering the time when logic is injected in learning embeddings, there are three stages: 1) Pre:
conducting symbolic reasoning before learning embeddings.
The reasoning often impacts training samples such as positive and negative triples. 2) Joint: injecting the logics during embedding learning. This often extends the loss function
with logic constraints, by e.g., adding an additional regularizer on some relation embeddings. 3) Post: conducting symbolic reasoning after embeddings are learned, by e.g., jointly
constructing a predictive model with both results from embeddings and logics as inputs, or logical constraints as filters.


Mechanisms 1) Data-based: replacing variables in logic
expressions with concrete entities and getting new triples,
then adding all or part of the new triples into training. 2)
Model-based: adding constraints on the embedding of entities and relations included in logic expressions into training.
No additional triples are used.


3.1 Logic Rules for Embeddings
Logic rules are of the formis the rule head andconjunction of atoms. A typical kind of logic rule is path rule B1 ∧ B2 H ∧ ←... ∧BB1n ∧ is the rule body with theB2 ∧ ... ∧ Bn where H
where rule body is a path from a head variable to a tail variable in the rule head; for example, r(X,Y)← r1(X,Z) ∧ r2(Z,Y)
is a path rule with a path from variable X to Y as body. Note
that the number of atoms in the body is also known as the
rule length. There are a few works that inject path rules into
embeddings. PTransE [Lin et al., 2015] is a typical explicit
and joint-training method, where path compositional representations calculated with relation embeddings in the path
are encouraged to near the relation embedding in rule head
in vector space. PTransE applies all high-quality paths during training. Alternatively, RPJE [Niu et al., 2020] selects the
path with the highest confidence to compose the path for each
triple and distinguishes paths with length 1 from other paths,
for which confidence of rules are not considered during training. Instead of compositional representation regularization,
ComplEx-NNE AER [Ding et al., 2018] infers constrains on
relation embeddings through making φ(h, r1, t) > φ(h, r2, t)
if r1(X,Y) ← r2(X,Y), and the larger φ(h, r, t) is, the more
possible (h, r, t) to be a positive one. Following ComplExNNE AER, SLRE [Guo et al., 2020] adapts relation embedding constrains to longer path rules.
Methods mentioned above inject pre-defined rules via
regularizing relation embeddings during training. They
are specific to KGE methods. One more general solution is using grounding, which replaces variables in each
rule with concrete entities, infers implicit triples, and generates additional triples for KGEs’ training. For example,
KALE [Guo et al., 2016] models groundings by t-norm fuzzy
logics which gives a truth score for each grounding based
on truth value of all atoms. It trains groundings with negative sampling together with existing triples. KALE conducts
grounding before training and injects them one time. Alternatively, multiple times or iterative injection ensures more
flexibility for a model. For example, in each training iteration, RUGE [Guo et al., 2018] and IterE [Zhang et al., 2019]
predicts labels of unlabeled triples in groundings based on tnorm fuzzy logics, and uses labeled triples and post-labeled


triples for training. The iterative manner enables the model to
predict labels for unlabeled triples dynamically based on embeddings. These data-based methods need to materialize each
rule, resulting in a massive number of groundings, thus they
do not scale well to large KGs. However, the KGE-free property makes them continuously benefit from the development
of KGEs. Post-training injection solutions are also KGEfree. For example, [Wang et al., 2015] proposes to frame an
Integer Linear Programming problem to combine rules and
KGEs, where rules are translated into conditional constraints
during training, and scores from well-trained KGEs are inputs.
Apart from the satisfaction of rules,
TARE [Wang et al., 2018b] emphasizes the properties
of transitivity and asymmetry of rules which makes the order
of relations in rules matter, and it models the order of relation
types in logic rules by the component-wise inequality.


3.2 Ontological Schemas for Embeddings
Ontological schemas, which are often defined by languages
such as OWL and RDF Schema, describe high-level semantics (meta information) of KGs. We next survey methods
that inject class hierarchies, relation hierarchies, and relation
properties.

Class Hierarchies Class hierarchies classify entity types,
denoting entities as instantiations of classes. There are two
tasks for injecting class hierarchies, encoding the types of entities and encoding hierarchies of entity types.
To encode entity types, with entity types given, one
kind of method learns an embedding for each type, and
adds regularization one these embeddings. For example,
TAGAT [Wang et al., 2021] regularizes entity embeddings to
be close to their corresponding type embeddings, and also
closes the embeddings of entities that belong to the same
type. RETA-Grader [Rosso et al., 2021] uses type embeddings in entity-typed triples (h typei, r, t typej) for each
triple (h, r, t), and concatenate embeddings in these two
types of triples as inputs for triple scoring. Without entity types given, a common way is to assume a type for
each entity and learn an embedding for it. For example,
TypeDM [Jain et al., 2018] uses the assumed type embedding of an entity and domain(range) embeddings of a relation to calculate the satisfactory of domain(range) of a relation. Another way is to infer candidate types of each entity based on ontological information. For example, IterefinE [Arora et al., 2020] applies the inferred types to refine
the KG data and regularize the learning of embeddings.
In order to inject entity type hierarchies into embeddings, there are methods with and without pre-defined hierarchies. With class hierarchies given, one kind of method
combines the type hierarchy of each entity to its embedding. For example, TKRL [Xie et al., 2016] encodes type
hierarchies into projection matrix, and injects type hierarchies into entity embeddings via projecting them with
projection matrices. Without pre-defined class hierarchies,
HAKE [Zhang et al., 2020b] proposes to map entities into
polar coordinate system, where concentric circles can naturally reflect hierarchies. After training, implicit entity hierarchies could be decoded from entity embeddings.



Relation Hierarchies Relation hierarchies contain subsumption relationships between relations; for example, hasFather is a sub-relation of hasParents. Without pre-defined
relation hierarchies, HRS [Zhang et al., 2018] assumes a
three-layer hierarchical relation structure for each relation,
including relation clusters, relations and sub-relations, discovered by the K-means algorithm on relation embeddings
from KGE. To encode relation hierarchies, it learns an embedding for each relation cluster and represents relations
as the sum of their cluster embedding, relation embedding, and sub-relations’ embedding. Another method TransRHS [Zhang et al., 2020a] which does not explicitly assume
a multi-layer relation hierarchy, proposes to model each relation as a vector together with a relation-specific sphere. It
assumes lower-level relations are with smaller spheres. If a
predicted entity lies in the spheres of a lower level relation
such as hasFather, then the model will ensure it also lies in
the sphere of its parent relations such as hasParent. This embodies the inherent generalization relationships among relations.


Relation Properties Ontological schemas often define
quite a few relation properties (and constraints).
First, we introduce properties constraining only one relation that have been considered. For domain and range
of relations, TRESCAL [Chang et al., 2014] leverages them
by filtering triples in KGs where entities are not compatible
with the domain or range of relations. If not pre-defined,
TypeDM [Jain et al., 2018] learns an assumed domain and
range embedding for each relation and uses them for constraining entity type embeddings. To model Ansymmetric relations, ComplEx [Trouillon et al., 2016] proposes to embed
KGs in complex vector space, where the commutative property for multiplication is not satisfied. To further model Composition [2] between relations, RotatE [Sun et al., 2019] proposes to define each relation as a rotation from the head
entity to the tail entity in complex vector space. Furthermore, Rot-Pro [Song et al., 2021] proposes to model Transitive relations by defining relations as projection and rotation.
dORC [Zhang, 2017] enables modeling Reflexive, Symmetric
and Transitive relations by disentangling the embedding of
each entity as head and tail entities. [Wang et al., 2015] propose a post-training injection for Cardinality of relations, by
framing a Liner programming problem.
Second, we introduce relation properties constraining
multiple relations that have been considered, including
Equivalent and Inverse. Given these two pre-defined relation properties, [Minervini et al., 2017] injects them via
a single constraint on the embedding of the two relations in schemas, based on the vector space assumption in KGEs. Besides applying axiom-based regularization, TransOWL [d’Amato et al., 2021] also proposes to
add new triples inferred by these schemas into training,
which could also be applied to entity type constraints
such as equivalentClass and subClassOf. More generally,
SIC [Wiharja et al., 2020] proposes to use ontological reasoning within their iterative KG completion approach to in

2Composition of relations includes multiple relations, we introduce it in this paragraph because RotatE is based on ComplEx.


Pre-defined Logics Integration Stage Mechanism
Logic Types Methods
With Without Pre Joint Post Data-based Model-based


[Lin et al., 2015; Wu et al., 2015; Niu et al., 2020]
path rule √      -      - √      -      - √ [Niu et al., 2020; Ding et al., 2018]

[Guo et al., 2020; Wang et al., 2018b]
path rule √      - √      -      - √      - [Guo et al., 2016; Guo et al., 2018]
path, cardinality √     -     -     - √     - √ [Wang et al., 2015]
class hierarchy √     -     - √     -     - √ [Xie et al., 2016]
class hierarchy     - √     - √     -     - √ [Zhang et al., 2020b]
entity type √      -      - √      -      - √ [Wang et al., 2021; Jain et al., 2018]
entity type √      -      - √      - √ √ [Rosso et al., 2021]
entity type      - √ √ √      - √ √ [Arora et al., 2020]
relation hierarchy    - √    - √    -    - √ [Zhang et al., 2018; Zhang et al., 2020b]
domain, range √     - √     -     - √     - [Chang et al., 2014]
domain, range     - √     - √     -     - √ [Jain et al., 2018]
equivalent, inverse √    -    - √    -    - √ [Minervini et al., 2017]
ansymmetric     - √     - √     -     - √ [Trouillon et al., 2016]
composition     - √     - √     -     - √ [Sun et al., 2019]
transitive       - √       - √       -       - √ [Song et al., 2021]
reflexive, symmetric, transitive - √ - √ - - √ [Zhang, 2017]
ontological schema √   - √   - √ √   - [Wiharja et al., 2020]


Table 1: Summary of methods injecting logics into KG embeddings.



ject inferred triples to enrich the input KG for embedding,
and to filter out schema-incorrect triples via consistency and
constraint checking. ReasonKGE [Jain et al., 2021] follows
SIC [Wiharja et al., 2020] by using schema-incorrect triples
for negative sampling.


3.3 Summary
We summarize methods injecting logics into embedding
methods introduced before in Table 1. If logics are predefined, there are diverse methods with different integration
stages and mechanisms. Moreover, in the scenario without
pre-defined logics, model-based and post-training injection
methods are used. For pre-training injection methods, databased models are more common, while model-based models
are more common for joint-training injection. We separately
discussed injecting logical rules and ontology schemas for
embeddings in this section, considering they are two types of
logic languages. However, they are not entirely distinct, and
each ontological schema could be rephrased into a logic rule.
For example composition of relations could be represented as
a path rule.


4 Embeddings for Logics
Pure symbolic reasoning with different kinds of logics have
been investigated for years and widely applied, but it still suffers from the following problems: 1) the logics must be given
as a priori, but constructing logics often relies on domain experts, costing a lot of time and labor, and the logics in most
applications are underspecified, limiting the knowledge that
can be inferred; 2) it often cannot cope with noise and uncertainty inherent to real-world data; 3) logic reasoning often cannot scale up since some (complex) logics may lead to
high time or space complexity. In contrast, embedding-based
reasoning is good at inductive reasoning without pre-defined
logics, can well address uncertainty, and can scale up by approximation. Thus utilizing embeddings for augmenting KG
reasoning tasks attracts wide research attention. We mainly
review two kinds of KG reasoning tasks: deductive logic reasoning, which further includes query answering and theorem



proving, and inductive logic learning. Before discussing the
methods, as in Section 3, we first introduce the perspectives
for analyzing and categorization:


Logic Types Many logics are considered in each work,
such as path rules, numerical rules, path queries, and logic
queries constructed by ∧, ∨, ¬, and ̸=. We present logic types
following the expression in logical forms they originated.


Pre-defined Logics Embeddings could be combined to logics 1)With and 2)Without pre-defined logics.


Combination Stage Considering the time when embeddings are combined to logics, there are two stages: 1) Pre:
applying embeddings before logic reasoning or learning, such
as for candidate selection. 2) Joint: applying embeddings
during logic reasoning or learning.


Mechanism 1) Hybrid: after applying embeddings, methods still infer in a symbolic space. 2) Neural: using embeddings following the process of logic reasoning, and all inferences are conducted in vector space.


4.1 Embeddings for Logic Reasoning
Query answering and theorem proving are two popular logic
reasoning tasks where embeddings could be utilized. They
are originally implemented by pure deductive symbolic reasoning with pre-defined logics. With the embeddings, additional knowledge can be predicted for more robust results.


Query Answering Query answering returns correct entities
in a KG as answers of a given structured query, where reasoning is usually considered for hidden answers. Conventional
query answering is conducted based on structure query languages such as SPARQL [3] to retrieve and manipulate knowledge in a KG.
Quite a few studies use embeddings to KG incomplete
and noise in query answering. In the beginning, simple
queries are considered, for example, path queries proposed
in [Guu et al., 2015]. It interprets TransE as implementing a


[3https://www.w3.org/TR/rdf-sparql-query/](https://www.w3.org/TR/rdf-sparql-query/)


Pre-defined Logics Integration Stage Mechanism
Tasks Logic Types Methods
With Without Pre Joint Hybrid Neural

Query Answering path query √ - - √ - √ [Guu et al., 2015]
Query Answering path query √ - √ - √ - [Wei et al., 2015]
Query Answering √ - - √ - √ [Hamilton et al., 2018; Kotnis et al., 2021]
Query Answering ∧, √ - - √ - √ [Ren et al., 2020; Arakelyan et al., 2021]
Query Answering ∧, ∨, √ - - √ - √ [Ren and Leskovec, 2020; Zhang et al., 2021c]
Query AnsweringTheorem proving ∧path rule∧, ∨ ∨, ¬ ¬, ̸= √√ √- -- √√ √- √- [Rockt¨aschel and Riedel, 2017][Liu et al., 2021]
Theorem proving path rule √ √ - √ √ - [Minervini et al., 2020a; Minervini et al., 2020b]
Rule Mining path rule  - √ √ √ √  - [Ho et al., 2018; Omran et al., 2018; Wang and Cohen, 2016]
Rule Mining path rule  - √  - √  - √ [Yang et al., 2017; Sadeghian et al., 2019]
Rule Mining numerical rule  - √  - √  - √ [Wang et al., 2020]


Table 2: Summary of methods integrating embeddings for symbolic logic reasoning and learning.


̸



soft edge traversal operator and recursively applies it to predict compositional path queries and is trained on path samples from random walks and explicit triples. Apart from simple path queries, more complex queries, such as conjunctive
logical queries and Existential Positive First-Order (EPFO),
involving multiple unobserved edges, nodes, and even variables are also widely researched with the help of embeddings. GQE embeds entities as a vector, relations as projection operators on entity embeddings, and makes ∧ in conjunctive logical queries as intersection operators. Through these
embeddings and operators, it encodes each query into a vector and gives answers based on the similarity between query
and candidate entity embeddings. BiQE [Kotnis et al., 2021]
translates conjunctive queries into a sequence and encodes
them by Transformer Encoder. Query2box [Ren et al., 2020]
can further support disjunctions (∨) in queries via transforming them into Disjunctive Normal Form (DNF), and it defines vector space operators for each type of quantifications.
Alternatively, CQD [Arakelyan et al., 2021] only defines
projection operators using ComplEx [Trouillon et al., 2016]
while applying other quantifications according to tnorms. To support a complete set of first-order logical operations, including conjunction(∧), disjunction(∨)
and negation(¬), BetaE [Ren and Leskovec, 2020] and
ConE [Zhang et al., 2021c] propose to embed entities and
queries as Beta distributions and sector-cones respectively,
on which projection, intersection and negation operator are
defined. NewLook [Liu et al., 2021] further supports queries
including Difference(≠ ) by logical operations as flexible neural networks.
Some studies use embeddings to improve the efficiency of
query answering, especially for those queries with complex
logics. For example, INS-ES [Wei et al., 2015], running the
data-driven inference algorithm INS on Markov Logic Network (MLN) for symbolic reasoning, uses embeddings from
TransE to generate a much smaller candidate set for subsequent fact inference in INS.


Theorem Proving Another task of logic reasoning is theorem proving, automatically inferring triples given a set of
facts and predefined logic rules. Conventional theorem proving methods are based on different logic languages, such as
Prolog, Datalog, and OWL, which are vulnerable to incomplete and noise KGs. Differentiable theorem proving using embeddings overcome the limits of symbolic provers on
generalizing to queries with similar but not identical sym


bols. With NTP [Rockt¨aschel and Riedel, 2017] as an example, it enables Prolog to learn embeddings and similarities between entities and relations in a KG. It keeps the
variable binding symbolic following the inference process of
Prolog but compares symbols using their embeddings rather
than identical symbols. It could learn without predefined
domain-specific rules and seamlessly reason with them. The
core process of NTP follows steps of symbolic logic reasoning that requires enumerating and scoring all bounded-depth
proof paths for a given goal, thus NTP is inefficient on large
KGs. Thus in some works, embeddings are also used to improve the efficiency of the differentiable prover. For example,
GNTP [Minervini et al., 2020a] use fact embeddings to select
the top nearest neighbor facts for proving sub-goals, and also
use relation embeddings to select top rules to be expanded.
Another method CTP [Minervini et al., 2020b] uses a keyvalue memory network, conditioned on the goal to prove and
embeddings of relations and constants, to dynamically generate a minimal set of rules to consider at each reasoning step.


4.2 Embeddings for Logic Learning


Logic learning is to learn patterns from KGs and
discover potential (and probabilistic) logics such
as schemas and logic rules. Conventional methods like AMIE [Gal´arraga et al., 2015] and AnyBURL [Meilicke et al., 2019] are symbolic-based. They
determine structures of rules via random walking and adding
atoms based on KGs, and measure the quality of rules by

̸ statistical matrices such as Confidence and Head Coverage.

While statistical matrices might be misleading due to the
incompleteness of and noise in KGs, thus it is difficult
to learn high-quality rules from the explicit triples alone.
Embeddings are widely used in logic learning to overcome
incompleteness and noise issues. RuLES [Ho et al., 2018]
adds confidential triples using embedding models for quality
extension of KGs. It iteratively extends rules induced
from a KG through feedback from embedding models and
evaluates the quality of rules on the origin KG and extended
KG. ProPPR+MF [Wang and Cohen, 2016] reconstructs
the transition of proofs in ProPPR [Wang et al., 2013], a
stochastic extension of Prolog, based on embeddings of
first-order logics through matrix factorization.
Embeddings have also been utilized to improve the efficiency of rule learning. RLvLR [Omran et al., 2018] uses
embeddings to guide and prune the search during rule mining,


where embeddings are learned on the subgraph sampled for
target predicates with RESCAL [Nickel et al., 2011]. While
DistMult [Yang et al., 2015] and IterE [Zhang et al., 2019]
alternatively use relation embeddings to calculate the confidence of rules. Another type of method is differentiable rule mining, learning rules in an end-to-end differentiable manner in vector space. They are inspired by
TensorLog [Cohen et al., 2020], a differentiable probabilistic logic. Tensorlog establishes a connection between inference using first-order rules and sparse matrix multiplication, and enables certain types of logical inference tasks
to be compiled into a sequence of differentiable numerical
operations on matrices. Differentiable rule mining methods use a module containing relation embeddings to learn
the weights for each operation of a rule used in TensorLog, for example, NeuralLP [Yang et al., 2017] uses an
attention-based neural controller system for weight generation, and DRUM [Sadeghian et al., 2019] applies a lowrank approximation. Besides path rules, Neural-NumLP [Wang et al., 2020] further enable mining rules with numerical features in a differentiable framework.

4.3 Summary
We summarize methods applying embeddings for logic reasoning and learning introduced before in Table 2. Embeddings could be combined with pre-defined logics either before(Pre) or during(Joint) the process of logic reasoning and
learning. And without pre-defined logics, embeddings usually are applied jointly. If the integration stage of embeddings
is Joint, there are both hybrid and neural methods, and only
hybrid methods for Pre. Methods that combining embeddings
in a Post manner haven’t been proposed yet.


5 Conclusion and Discussion

This paper presents a literature review for KG reasoning with
logics and embeddings. We divided the integrated methods
into integrating logics(logic rules and ontological schemas)
to embeddings and integrating embeddings to logic-based
reasoning tasks(query answering, theorem proving, and rule
mining). Moreover, we analyzed those methods from four
perspectives: logic types, the existence of pre-defined logics,
integration stages, and integration mechanisms.
Next, we discuss challenges on this topic from four perspectives: logic diversity, explainability, benchmark, and application.

Logic diversity One critical challenge of logic and embedding integration lies in the diversity of logics. The majority of current methods only consider specific kinds of logics,
such as path rules, entity types (classes), class hierarchies,
relation hierarchies, and relation properties (see Section 3),
or specific logic quantifications such as conjunction, disjunction, and negation (see Section 4). Only a few methods, like
SIC, ReasonKGE, and TransOWL, support general ontological schemas. Since a KG is often equipped with different
kinds of logics, e.g., rules or ontological schemas, it becomes
a significant challenge to support and integrate all or most of
them simultaneously.
To this end, we think there are two promising directions.
One is to explore more logic forms, such as rules with con


stants, universal quantification (∀), disjointness, and more.
Another is to research general frameworks that can simultaneously support different kinds of logics and is independent
of KG embedding methods.


Explainability Another critical challenge is making integrated methods more explainable. Most methods in Section 3 focus on improving the model’s expressiveness, which
does not change the black-box nature of embedding methods. Methods in Section 4 enabling logic reasoning in vector
space decrease the transparency of logic-based methods because the intermediate results are represented as embeddings
that is understandable by human if and only if the meaning
of these embeddings are properly interpreted, which is difficult in most cases. While for further AI applications, systems
with higher safety, trustness, and fairness are expected. Improving the transparency of integrated methods could ensure
them broader applications in the further.
In order to achieve this, potential directions may lie in the
following three directions. First, for black-box models such
as KGEs, inject not only semantics of logics but also reasoning steps into models, which extends them from one-step
to multi-step reasoning models with interpretable intermediate results. Second, for multi-step models with embeddings
as intermediate results, improve the interpretability of intermediate embeddings, especially generate a set of symbolic
representations that is easy for humans to understand, instead
of similarity intuitions between embeddings. Third, integrate
logics and embeddings through explainable machine learning methods to help preserve the transparency of logic-based
methods and the robustness of embedding-based methods.


Benchmark There is a shortage of resources for evaluating
KG reasoning with both logics and embeddings. Commonly
used benchmarks for KGEs’ evaluation, such as WN18RR,
FB15k-237 and NELL, are subsets sampled from one or multiple domain in large KGs. When creating these datasets, the
primary goal is making them suitable for supervised learning setting, which do not ensure and explore diverse logic
patterns contained in the dataset. While many works injecting logics in embeddings or combining embeddings for
logic reasoning are evaluated on these datasets, which could
not reflect the capability of methods once the logic patterns
they concerned are missing in the dataset. Therefore, benchmarks containing diverse pre-defined logics or logic patterns
in triples deserved to be proposed.
Also, SIC [Wiharja et al., 2020] argues that experimental
results show that the existing correctness notion based on the
silver standard is highly questionable. Good results from the
silver standard often cannot be transferred to other knowledge graphs beyond the benchmark KGs reported in papers.
Instead, in the absence of large scale human evaluations,
schema correctness [Wiharja et al., 2020] is more promising.


Application Apart from KG reasoning tasks, there are
many KG applications, which have been proved could
benefit from logics(embeddings) in KGs, for example, information extraction [Wang et al., 2018a], recommender system [Wong et al., 2021], and image classification [Geng et al., 2021], especially low-resource learning [Chen et al., 2021]. However, these tasks have been


rarely explored with both logics and embeddings. Recently,
inspired by the concept of pre-training and fine-tuning of language models, which is powerful in many downstream natural language processing tasks, KGEs are also extended to pretrained KG models [Zhang et al., 2021b] to be used in many
KG applications. Thus in the future, applying both logics and
embeddings into more KG applications and pre-trained KG
models deserves attention.


References


[Arakelyan et al., 2021] Erik Arakelyan, Daniel Daza,
Pasquale Minervini, and Michael Cochez. Complex query
answering with neural link predictors. In ICLR, 2021.


[Arora et al., 2020] S. Arora, S. Bedathur, M. Ramanath, and
D. Sharma. Iterefine: Iterative KG refinement embeddings
using symbolic knowledge. In AKBC, 2020.


[Bordes et al., 2013] Antoine Bordes, Nicolas Usunier,
Alberto Garcia-Duran, Jason Weston, and Oksana
Yakhnenko. Translating embeddings for modeling
multi-relational data. In NIPS, 2013.


[Chang et al., 2014] K. Chang, W. Yih, B. Yang, and
C. Meek. Typed tensor decomposition of knowledge bases
for relation extraction. In EMNLP, 2014.


[Chen et al., 2021] Jiaoyan Chen, Yuxia Geng, Zhuo Chen,
Jeff Z Pan, Yuan He, Wen Zhang, and so on. Low-resource
learning with knowledge graphs: A comprehensive survey.
arXiv preprint arXiv:2112.10006, 2021.


[Cohen et al., 2020] W. W. Cohen, F. Yang, and K. Mazaitis.
Tensorlog: A probabilistic database implemented using
deep-learning infrastructure. J. Artif. Intell. Res., 2020.


[d’Amato et al., 2021] Claudia d’Amato, Nicola Flavio Quatraro, and Nicola Fanizzi. Injecting background knowledge into embedding models for predictive tasks on
knowledge graphs. In ESWC, 2021.


[Ding et al., 2018] Boyang Ding, Quan Wang, Bin Wang,
and Li Guo. Improving knowledge graph embedding using
simple constraints. In ACL, 2018.


[Gal´arraga et al., 2015] L. Gal´arraga, C. Teflioudi, K. Hose,
and F. M. Suchanek. Fast rule mining in ontological
knowledge bases with AMIE+. VLDB J., 2015.


[Geng et al., 2021] Yuxia Geng, Jiaoyan Chen, Zhuo Chen,
Jeff Z. Pan, Zhiquan Ye, Zonggang Yuan, Yantao Jia,
and Huajun Chen. Ontozsl: Ontology-enhanced zero-shot
learning. In WWW, 2021.


[Glimm et al., 2014] Birte Glimm, Ian Horrocks, Boris
Motik, Giorgos Stoilos, and Zhe Wang. Hermit: An OWL
2 reasoner. J. Autom. Reason., 2014.


[Guo et al., 2016] Shu Guo, Quan Wang, Lihong Wang, Bin
Wang, and Li Guo. Jointly embedding knowledge graphs
and logical rules. In EMNLP, 2016.


[Guo et al., 2018] Shu Guo, Quan Wang, Lihong Wang, Bin
Wang, and Li Guo. Knowledge graph embedding with
iterative guidance from soft rules. In AAAI, 2018.




[Guo et al., 2020] Shu Guo, Lin Li, Zhen Hui, Lingshuai
Meng, Bingnan Ma, Wei Liu, Lihong Wang, Haibin Zhai,
and Hong Zhang. Knowledge graph embedding preserving
soft logical regularity. In CIKM, 2020.

[Guu et al., 2015] K. Guu, J. Miller, and P. Liang. Traversing
knowledge graphs in vector space. In EMNLP, 2015.

[Hamilton et al., 2018] W. L. Hamilton, P. Bajaj, M. Zitnik,
D. Jurafsky, and JJ.ure Leskovec. Embedding logical
queries on knowledge graphs. In NeurIPS, 2018.

[Ho et al., 2018] Vinh Thinh Ho, Daria Stepanova, Mohamed H. Gad-Elrab, Evgeny Kharlamov, and Gerhard
Weikum. Rule learning from knowledge graphs guided
by embedding models. In ISWC, 2018.

[Horrocks et al., ] Ian Horrocks, Oliver Kutz, and Ulrike Sattler. The even more irresistible sroiq. In KR2006.

[Jain et al., 2018] Prachi Jain, Pankaj Kumar, Mausam, and
Soumen Chakrabarti. Type-sensitive knowledge base inference without explicit type supervision. In ACL, 2018.

[Jain et al., 2021] N. Jain, T. Tran, M. H. Gad-Elrab, and
D. Stepanova. Improving knowledge graph embeddings
with ontological reasoning. In ISWC, 2021.

[Kotnis et al., 2021] B. Kotnis, C. Lawrence, and
M. Niepert. Ans. complex queries in KGs with bidirectional sequence encoders. In AAAI, 2021.

[Kr¨otzsch et al., 2008] Markus Kr¨otzsch, S. Rudolph, and
P. Hitzler. Description logic rules. 2008.

[Li et al., 2020] Weizhuo Li, Guilin Qi, and Qiu Ji. Hybrid
reasoning in knowledge graphs: Combing symbolic reasoning and statistical reasoning. Semantic Web, 2020.

[Lin et al., 2015] Y. Lin, Z. Liu, H. Luan, M. Sun, S. Rao,
and S. Liu. Modeling relation paths for representation
learning of knowledge bases. In EMNLP, 2015.

[Liu et al., 2021] Lihui Liu, Boxin Du, Heng Ji, ChengXiang Zhai, and Hanghang Tong. Neural-answering logical
queries on knowledge graphs. In KDD, 2021.

[Meilicke et al., 2019] C. Meilicke, M. Chekol,
D. Ruffinelli, and H. Stuckenschmidt. Anytime bottom-up
rule learning for knowledge graph completion. In IJCAI,
2019.

[Minervini et al., 2017] P. Minervini, L. Costabello, E., V.,
and P. Vandenbussche. Regularizing knowledge graph
embeddings via equivalence and inversion axioms. In
ECML/PKDD, 2017.

[Minervini et al., 2020a] Pasquale Minervini, Matko Bosnjak, Tim Rockt¨aschel, Sebastian Riedel, and Edward
Grefenstette. Differentiable reasoning on large knowledge
bases and natural language. In AAAI, 2020.

[Minervini et al., 2020b] Pasquale Minervini, Sebastian
Riedel, Pontus Stenetorp, Edward Grefenstette, and Tim
Rockt¨aschel. Learning reasoning strategies in end-to-end
differentiable proving. In ICML, 2020.

[Nenov et al., 2015] Yavor Nenov, Robert Piro, Boris Motik,
Ian Horrocks, Zhe Wu, and Jay Banerjee. Rdfox: A
highly-scalable RDF store. In ISWC, 2015.


[Nickel et al., 2011] Maximilian Nickel, Volker Tresp, and
Hans-Peter Kriegel. A three-way model for collective
learning on multi-relational data. In ICML, 2011.


[Niu et al., 2020] Guanglin Niu, Yongfei Zhang, Bo Li, Peng
Cui, Si Liu, Jingyang Li, and Xiaowei Zhang. Ruleguided compositional representation learning on knowledge graphs. In AAAI, 2020.


[Omran et al., 2018] Pouya Ghiasnezhad Omran, Kewen
Wang, and Zhe Wang. Scalable rule learning via learning
representation. In IJCAI, 2018.


[Pan and Horrocks, 2006] Jeff Z. Pan and Ian Horrocks.
OWL-Eu: Adding Customised Datatypes into OWL. Journal of Web Semantics, 2006.


[Ren and Leskovec, 2020] Hongyu Ren and Jure Leskovec.
Beta embeddings for multi-hop logical reasoning in
knowledge graphs. In NeurIPS, 2020.


[Ren et al., 2020] Hongyu Ren, Weihua Hu, and Jure
Leskovec. Query2box: Reasoning over knowledge graphs
in vector space using box embeddings. In ICLR, 2020.


[Rockt¨aschel and Riedel, 2017] T. Rockt¨aschel and
S. Riedel. End-to-end differentiable proving. In
NIPS, 2017.


[Rosso et al., 2021] Paolo Rosso, Dingqi Yang, Natalia
Ostapuk, and Philippe Cudr´e-Mauroux. RETA: A schemaaware, end-to-end solution for instance completion in
knowledge graphs. In WWW, 2021.


[Sadeghian et al., 2019] A. Sadeghian, M. Armandpour,
P. Ding, and D. Wang. DRUM: end-to-end differentiable
rule mining on knowledge graphs. In NeurIPS, 2019.


[Song et al., 2021] Tengwei Song, Jie Luo, and Lei Huang.
Rot-pro: Modeling transitivity by projection in knowledge
graph embedding. NeurIPS, 2021.


[Sun et al., 2019] Zhiqing Sun, Zhi-Hong Deng, Jian-Yun
Nie, and Jian Tang. Rotate: Knowledge graph embedding
by relational rotation in complex space. In ICLR, 2019.


[Trouillon et al., 2016] T. Trouillon, J. Welbl, S. Riedel, E.,
and G. Bouchard. Complex embeddings for simple link
prediction. In ICML, 2016.


[Wang and Cohen, 2016] William Y. Wang and William W.
Cohen. Learning first-order logic embeddings via matrix
factorization. In IJCAI, 2016.


[Wang et al., 2013] William Yang Wang, Kathryn Mazaitis,
and William W. Cohen. Programming with personalized
pagerank: a locally groundable first-order probabilistic
logic. In CIKM, 2013.


[Wang et al., 2015] Q. Wang, B. Wang, and L. Guo. Knowledge base completion using embeddings and rules. In IJCAI, 2015.


[Wang et al., 2018a] G. Wang, W. Zhang, R. Wang, Y. Zhou,
X. Chen, W. Zhang, H. Zhu, and H. Chen. Label-free
distant supervision for relation extraction via knowledge
graph embedding. In EMNLP, 2018.




[Wang et al., 2018b] M. Wang, E. Rong, H. Zhuo, and
H. Zhu. Embedding knowledge graphs based on transitivity and asymmetry of rules. In PAKDD, 2018.

[Wang et al., 2020] Po-Wei Wang, Daria Stepanova, Csaba
Domokos, and J. Zico Kolter. Differentiable learning of
numerical rules in knowledge graphs. In ICLR, 2020.

[Wang et al., 2021] Yuzhuo Wang, Hongzhi Wang, Junwei
He, Wenbo Lu, and Shuolin Gao. TAGAT: type-aware
graph attention networks for reasoning over knowledge
graphs. Knowl. Based Syst., 233:107500, 2021.

[Wei et al., 2015] Zhuoyu Wei, Jun Zhao, Kang Liu, Zhenyu
Qi, Zhengya Sun, and Guanhua Tian. Large-scale knowledge base completion: Inferring via grounding network
sampling over selected instances. In CIKM, 2015.

[Wiharja et al., 2020] Kemas Wiharja, Jeff Z. Pan, Martin J.
Kollingbaum, and Yu Deng. Schema Aware Iterative
Knowledge Graph Completion. JoWS, 2020.

[Wong et al., 2021] C. Wong, F. Feng, W. Zhang, C. Vong,
H. Chen, Y. Zhang, P. He, H. Chen, K. Zhao, and H. Chen.
Improving conversational recommender system by pretraining billion-scale knowledge graph. In ICDE, 2021.

[Wu et al., 2015] Fei Wu, Jun Song, Yi Yang, Xi Li,
Zhongfei (Mark) Zhang, and Yueting Zhuang. Structured
embedding via pairwise relations and long-range interactions in knowledge base. In AAAI, 2015.

[Xie et al., 2016] Ruobing Xie, Zhiyuan Liu, and Maosong
Sun. Representation learning of knowledge graphs with
hierarchical types. In IJCAI, 2016.

[Yang et al., 2015] B. Yang, W. Yih, X. He, J. Gao, and
L. Deng. Embedding entities and relations for learning
and inference in knowledge bases. In ICLR, 2015.

[Yang et al., 2017] Fan Yang, Zhilin Yang, and William W.
Cohen. Differentiable learning of logical rules for knowledge base reasoning. In NIPS, 2017.

[Zhang et al., 2018] Zhao Zhang, Fuzhen Zhuang, Meng Qu,
Fen Lin, and Qing He. Knowledge graph embedding with
hierarchical relation structure. In EMNLP, 2018.

[Zhang et al., 2019] W. Zhang, B. Paudel, L. Wang, J. Chen,
H. Zhu, W. Zhang, A. Bernstein, and H. Chen. Iteratively
learning embeddings and rules for knowledge graph reasoning. In WWW, 2019.

[Zhang et al., 2020a] Fuxiang Zhang, Xin Wang, Zhao Li,
and Jianxin Li. Transrhs: A representation learning
method for knowledge graphs with relation hierarchical
structure. In IJCAI, 2020.

[Zhang et al., 2020b] Zhanqiu Zhang, Jianyu Cai, Yongdong
Zhang, and Jie Wang. Learning hierarchy-aware knowledge graph embeddings for link prediction. In AAAI, 2020.

[Zhang et al., 2021a] Jing Zhang, Bo Chen, Lingxi Zhang,
Xirui Ke, and Haipeng Ding. Neural, symbolic and neuralsymbolic reasoning on knowledge graphs. AI Open, 2021.

[Zhang et al., 2021b] W. Zhang, C. Man Wong, G. Ye,
B. Wen, W. Zhang, and H. Chen. Billion-scale pre-trained


e-commerce product knowledge graph model. In ICDE,
2021.

[Zhang et al., 2021c] Z. Zhang, J. Wang, J. Chen, S. Ji, and
F. Wu. Cone: Cone embeddings for multi-hop reasoning
over knowledge graphs. In NeurIPS, 2021.

[Zhang, 2017] Wen Zhang. Knowledge graph embedding
with diversity of structures. In WWW, 2017.


