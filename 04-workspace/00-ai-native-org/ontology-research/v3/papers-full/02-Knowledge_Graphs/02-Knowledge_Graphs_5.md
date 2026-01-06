<!-- Source: 02-Knowledge_Graphs.pdf | Chunk 5/15 -->


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

rank decomposition of tensors; this method is called Canonical Polyadic (CP) decomposition [236].

For example, we might have a 3-order tensor C containing monthly temperatures for Chilean cities
_at four different times of day_, which could be approximated with x1 ⊗ y1 ⊗ z1 + _. . ._ x _𝑑_ ⊗ y _𝑑_ ⊗ z _𝑑_
(e.g., x1 might be a latitude factor, y1 a monthly variation factor, and z1 a daily variation factor,


24The outer product of two (column) vectors x of length _𝑎_ and y of length _𝑏_, denoted x ⊗ y, is defined as xyT, yielding an
( _𝑎,𝑏_ )-matrix M such that (M) _𝑖𝑗_ = (x) _𝑖_ - (y) _𝑗_ . Analogously, the outer product of _𝑘_ vectors is a _𝑘_ -order tensor.


40


y1 z1



y _𝑑_ z _𝑑_



A. C. L. S. T. V.



north of
west of



A.
C.
L.
S.
T.
V.




# ≈ ⊗ + . . . + ⊗



x1



x _𝑑_


|f<br>0 0 0 0 0 0<br>0 0 0 0 0 0<br>0 1 0 0 0 0<br>0 0 0 0 0 0<br>0 0 0 0 0 0<br>0 0 0 1 0 0|Col2|Col3|Col4|Col5|Col6|
|---|---|---|---|---|---|
|<br>0|0|0|0|0|0|
|0|0|0|0|0|0|
|0|1|0|0|0|0|
|0|0|0|0|0|0|
|0|0|0|0|0|0|
|0|0|0|1|0|0|



G ≈ x1 ⊕ y1 ⊕ z1 + _. . ._ + x _𝑑_ ⊕ y _𝑑_ ⊕ z _𝑑_


Fig. 28. Abstract illustration of a CP _𝑑_ -rank decomposition of a tensor representing the graph of Figure 27a


and so on). Various algorithms then exist to compute (approximate) CP decompositions, including

Alternating Least Squares, Jennrich’s Algorithm, and the Tensor Power method [427].

Returning to graphs, similar principles can be used to decompose a graph into vectors, thus

yielding embeddings. In particular, a graph can be encoded as a one-hot 3-order tensor G with
| _𝑉_ | × | _𝐿_ | × | _𝑉_ | elements, where the element (G) _𝑖𝑗𝑘_ is set to one if the _𝑖_ [th] node links to the _𝑘_ [th]


node with an edge having the _𝑗_ [th] label, or zero otherwise. As previously mentioned, such a tensor

will typically be very large and sparse, where rank decompositions are thus applicable. A CP

decomposition [236] would compute a sequence of vectors (x1 _,_ y1 _,_ z1 _, . . .,_ x _𝑑,_ y _𝑑,_ z _𝑑_ ) such that
x1 ⊗ y1 ⊗ z1 + _. . ._ + x _𝑑_ ⊗ y _𝑑_ ⊗ z _𝑑_ ≈G. We illustrate this scheme in Figure 28. Letting X _,_ Y _,_ **Z** denote
the matrices formed by �x1 · · · x _𝑑_ �, �y1 · · · y _𝑑_ �, �z1 · · · z _𝑑_ �, respectively, with each vector forming
a column of the corresponding matrix, we could then extract the _𝑖_ [th] row of Y as an embedding
for the _𝑖_ [th] relation, and the _𝑗_ [th] rows of X and Z as _two_ embeddings for the _𝑗_ [th] entity. However,

knowledge graph embeddings typically aim to assign _one_ vector to each entity.

DistMult [568] is a seminal method for computing knowledge graph embeddings based on rank

decompositions, where each entity and relation is associated with a vector of dimension _𝑑_, such
that for an edge [s] p -, a plausibility scoring function [�] _[𝑑]_ _𝑖_ =1 [(][e][s][)] _[𝑖]_ [(][r][p][)] _[𝑖]_ [(][e][o][)] _[𝑖]_ [is defined, where][ (][e][s][)] _[𝑖]_ [,]
(rp) _𝑖_ and (eo) _𝑖_ denote the _𝑖_ [th] elements of vectors es, rp, eo, respectively. The goal, then, is to learn

vectors for each node and edge label that maximise the plausibility of positive edges and minimise

the plausibility of negative edges. This approach equates to a CP decomposition of the graph tensor
G, but where entities have one vector that is used twice: x1 ⊗ y1 ⊗ x1 + _. . ._ + x _𝑑_ ⊗ y _𝑑_ ⊗ x _𝑑_ ≈G. A
weakness of this approach is that per the scoring function, the plausibility of [s] p - will always
be equal to that of [o] p s ; in other words, DistMult does not consider edge direction.

Rather than use a vector as a relation embedding, RESCAL [386] uses a matrix, which allows for

combining values from es and eo across all dimensions, and thus can capture (e.g.) edge direction.

However, RESCAL incurs a higher cost in terms of space and time than DistMult. HolE [385] uses

vectors for relation and entity embeddings, but proposes to use the _circular correlation operator_ 
which takes sums along the diagonals of the outer product of two vectors – to combine them. This

operator is not commutative, and can thus consider edge direction. ComplEx [526], on the other

hand, uses a complex vector (i.e., a vector containing complex numbers) as a relational embedding,

which similarly allows for breaking the aforementioned symmetry of DistMult’s scoring function

while keeping the number of parameters low. SimplE [283] rather proposes to compute a standard

CP decomposition computing two initial vectors for entities from X and Z and then averaging
terms across X, Y, Z to compute the final plausibility scores. TuckER [30] employs a different

type of decomposition – called a Tucker Decomposition [528], which computes a smaller “core”

tensor T and a sequence of three matrices A, B and C, such that G ≈T ⊗ A ⊗ B ⊗ C – where


41


entity embeddings are taken from A and C, while relation embeddings are taken from B. Of these

approaches, TuckER [30] currently provides state-of-the-art results on standard benchmarks.


_5.2.3_ _Neural models._ A limitation of the previously discussed approaches is that they assume

either linear (preserving addition and scalar multiplication) or bilinear (e.g., matrix multiplication)

operations over embeddings to compute plausibility scores. A number of approaches rather use

neural networks to learn embeddings with non-linear scoring functions for plausibility.

One of the earliest proposals of a neural model was Semantic Matching Energy (SME) [192],
which learns parameters (aka weights: w, w [′] ) for two functions – _𝑓_ w(es _,_ rp) and _𝑔_ w [′] (eo _,_ rp) – such
that the dot product of the result of both functions – _𝑓_ w(es _,_ rp) · _𝑔_ w [′] (eo _,_ rp) – gives the plausibility
score. Both linear and bilinear variants of _𝑓_ w and _𝑔_ w [′] are proposed. Another early proposal was
Neural Tensor Networks (NTN) [488], which rather proposes to maintain a tensor W of internal

weights, such that the plausibility score is computed by a complex function that combines the outer
product es ⊗W ⊗ eo with a standard neural layer over es and eo, which in turn is combined with
rp, to produce a plausibility score. The use of the tensor W results in a high number of parameters,
which limits scalability [549]. Multi Layer Perceptron (MLP) [131] is a simpler model, where es, rp
and eo are concatenated and fed into a hidden layer to compute the plausibility score.

A number of more recent approaches have proposed using convolutional kernels in their models.
ConvE [127] proposes to generate a matrix from es and rp by “wrapping” each vector over several

rows and concatenating both matrices. The concatenated matrix serves as the input for a set of

(2D) convolutional layers, which returns a feature map tensor. The feature map tensor is vectorised

and projected into _𝑑_ dimensions using a parametrised linear transformation. The plausibility score
is then computed based on the dot product of this vector and eo. A disadvantage of ConvE is

that by wrapping vectors into matrices, it imposes an artificial two-dimensional structure on the

embeddings. HypER [28] is a similar model using convolutions, but avoids the need to wrap vectors
into matrices. Instead, a fully connected layer (called the “hypernetwork”) is applied to rp and used

to generate a matrix of relation-specific convolutional filters. These filters are applied directly to

es to give a feature map, which is vectorised. The same process is then applied as in ConvE: the
resulting vector is projected into _𝑑_ dimensions, and a dot product applied with eo to produce the

plausibility score. The resulting model is shown to outperform ConvE on standard benchmarks [28].

The presented approaches strike different balances in terms of expressivity and the number of

parameters that need to be trained. While more expressive models, such as NTN, may better fit

more complex plausibility functions over lower dimensional embeddings by using more hidden

parameters, simpler models, such as that proposed by Dong et al. [131], and convolutional net
works [28, 127] that enable parameter sharing by applying the same (typically small) kernels over

different regions of a matrix, require handling fewer parameters overall and are more scalable.


_5.2.4_ _Language models._ Embedding techniques were first explored as a way to represent natural

language within machine learning frameworks, with word2vec [352] and GloVe [408] being two

seminal approaches. Both approaches compute embeddings for words based on large corpora of text

such that words used in similar contexts (e.g., “frog”, “toad”) have similar vectors. Word2vec uses

neural networks trained either to predict the current word from surrounding words ( _continuous_

_bag of words_ ), or to predict the surrounding words given the current word ( _continuous skip-gram_ ).

GloVe rather applies a regression model over a matrix of co-occurrence probabilities of word pairs.

Embeddings generated by both approaches are widely used in natural language processing tasks.

Another approach for graph embeddings is thus to leverage proven approaches for language

embeddings. However, while a graph consists of an unordered set of sequences of three terms

(i.e., a set of edges), text in natural language consists of arbitrary-length sequences of terms (i.e.,

sentences of words). Along these lines, RDF2Vec [441] performs (biased [95]) random walks on


42


the graph and records the paths (the sequence of nodes and edge labels traversed) as “sentences”,

which are then fed as input into the word2vec [352] model. An example of such a path extracted

from Figure 24 might be, for example, [San Pedro] bus Calama flight Iquique flight Santiago, where

the paper experiments with 500 paths of length 8 per entity. RDF2Vec also proposes a second mode

where sequences are generated for nodes from canonically-labelled sub-trees of which they are a

root node, where the paper experiments with sub-trees of depth 1 and 2. Conversely, KGloVe [96]

is based on the GloVe model. Much like how the original GloVe model [408] considers words that

co-occur frequently in windows of text to be more related, KGloVe uses personalised PageRank [25] to

determine the most related nodes to a given node, whose results are then fed into the GloVe model.


_5.2.5_ _Entailment-aware models._ The embeddings thus far consider the data graph alone. But what

if an ontology or set of rules is provided? Such deductive knowledge could be used to improve the

embeddings. One approach is to use constraint rules to refine the predictions made by embeddings;

for example, Wang et al. [550] use functional and inverse-functional definitions as constraints

(under UNA) such that, for example, if we define that an event can have at most one value for

venue, this is used to lower the plausibility of edges that would assign multiple venues to an event.

More recent approaches rather propose joint embeddings that consider both the data graph and

rules when computing embeddings. KALE [207] computes entity and relation embeddings using a

translational model (specifically TransE) that is adapted to further consider rules using _t-norm fuzzy_

_logics_ . With reference to Figure 24, consider a simple rule [?x] bus ?y ⇒ [?x] connects to ?y . We can
use embeddings to assign plausibility scores to new edges, such as _𝑒_ 1: [Piedras Rojas] bus Moon Valley .
We can further apply the previous rule to generate a new edge _𝑒_ 2: [Piedras Rojas] connects to Moon Valley

from the predicted edge _𝑒_ 1. But what plausibility should we assign to this second edge? Letting _𝑝_ 1

and _𝑝_ 2 be the current plausibility scores of _𝑒_ 1 and _𝑒_ 2 (initialised using the standard embedding), then
t-norm fuzzy logics suggests that the plausibility be updated as _𝑝_ 1 _𝑝_ 2 − _𝑝_ 1 + 1. Embeddings are then

trained to jointly assign larger plausibility scores to positive examples versus negative examples

of both edges and _ground rules_ . An example of a positive ground rule based on Figure 24 would

be [Arica] bus San Pedro ⇒ [Arica] connects to San Pedro . Negative ground rules randomly replace the
relation in the head of the rule; for example, [Arica] bus San Pedro ⇏ [Arica] flight San Pedro . Guo

et al. [208] later propose RUGE, which uses a joint model over ground rules (possibly soft rules

with confidence scores) and plausibility scores to align both forms of scoring for unseen edges.

Generating ground rules can be costly. An alternative approach, called FSL [125], observes that

in the case of a simple rule, such as [?x] bus ?y ⇒ [?x] connects to ?y, the relation embedding
bus should always return a lower plausibility than connects to. Thus, for all such rules, FSL

proposes to train relation embeddings while avoiding violations of such inequalities. While relatively

straightforward, FSL only supports simple rules, while KALE also supports more complex rules.

These works are interesting examples of how deductive and inductive forms of knowledge – in

this case rules and embeddings – can interplay and complement each other.


**5.3** **Graph Neural Networks**


While embeddings aim to provide a dense numerical representation of graphs suitable for use within

existing machine learning models, another approach is to build custom machine learning models

adapted for graph-structured data. Most custom learning models for graphs are based on (artificial)

neural networks [559], exploiting a natural correspondence between both: a neural network already

corresponds to a weighted, directed graph, where nodes serve as artificial neurons, and edges serve


25Intuitively speaking, personalised PageRank starts at a given node and then determines the probability of a random walk

being at a particular node after a given number of steps. A higher number of steps converges towards standard PageRank

emphasising global node centrality, while a lower number emphasises proximity/relatedness to the starting node.


43


as weighted connections (axons). However, the typical topology of a traditional neural network –

more specifically, a fully-connected feed-forward neural network – is quite homogeneous, being

defined in terms of sequential layers of nodes where each node in one layer is connected to all

nodes in the next layer. Conversely, the topology of a data graph is quite heterogeneous, being

determined by the relations between entities that its edges represent.

A _graph neural network_ (GNN) [462] builds a neural network based on the topology of the data

graph; i.e., nodes are connected to their neighbours per the data graph. Typically a model is then

learnt to map input features for nodes to output features in a supervised manner; output features

for example nodes may be manually labelled, or may be taken from the knowledge graph. Unlike

knowledge graphs embeddings, GNNs support end-to-end supervised learning for specific tasks:

given a set of labelled examples, GNNs can be used to classify elements of the graph or the graph

itself. GNNs have been used to perform classification over graphs encoding compounds, objects in

images, documents, etc.; as well as to predict traffic, build recommender systems, verify software,

etc. [559]. Given labelled examples, GNNs can even replace graph algorithms; for example, GNNs

have been used to find central nodes in knowledge graphs in a supervised manner [396, 397, 462].

We now discuss the ideas underlying two flavours of GNN – _recursive GNNs_ and _convolutional_

_GNNs_ - where we refer to Appendix B.6.3 for more formal definitions relating to GNNs.


_5.3.1_ _Recursive graph neural networks._ Recursive graph neural networks (RecGNNs) are the seminal

approach to graph neural networks [462, 493]. The approach is conceptually similar to the systolic

abstraction illustrated in Figure 25, where messages are passed between neighbours towards

recursively computing some result. However, rather than define the functions used to decide the

messages to pass, we rather label the output of a training set of nodes and let the framework learn

the functions that generate the expected output, thereafter applying them to label other examples.

In a seminal paper, Scarselli et al. [462] proposed what they generically call a graph neural

network (GNN), which takes as input a directed graph where nodes and edges are associated with

_feature vectors_ that can capture node and edge labels, weights, etc. These feature vectors remain

fixed throughout the process. Each node in the graph is also associated with a _state vector_, which is

recursively updated based on information from the node’s neighbours – i.e., the feature and state

vectors of the neighbouring nodes and the feature vectors of the edges extending to/from them –

using a parametric function, called the _transition function_ . A second parametric function, called the

_output function_, is used to compute the final output for a node based on its own feature and state

vector. These functions are applied recursively up to a fixpoint. Both parametric functions can be

implemented using neural networks where, given a partial set of _supervised nodes_ in the graph – i.e.,

nodes labelled with their desired output – parameters for the transition and output functions can

be learnt that best approximate the supervised outputs. The result can thus be seen as a recursive

neural network architecture. [26] To ensure convergence up to a fixpoint, certain restrictions are

applied, namely that the transition function be a _contractor_, meaning that upon each application of

the function, points in the numeric space are brought closer together (intuitively, in this case, the

numeric space “shrinks” upon each application, ensuring a unique fixpoint).

To illustrate, consider, for example, that we wish to find priority locations for creating new tourist

information offices. A good strategy would be to install them in hubs from which many tourists visit

popular destinations. Along these lines, in Figure 29 we illustrate the GNN architecture proposed

by Scarselli et al. [462] for a sub-graph of Figure 24, where we highlight the neighbourhood of


Punta Arenas . In this graph, nodes are annotated with feature vectors (n _𝑥_ ) and hidden states at step
_𝑡_ (h _𝑥_ [(] _[𝑡]_ [)] [), while edges are annotated with feature vectors (][a] _𝑥𝑦_ [). Feature vectors for nodes may, for]


26Some authors refer to such architectures as _recurrent graph neural networks_, observing that the internal state maintained

for nodes can be viewed as a form of recurrence over a sequence of transitions.


44


n1 _,_ h1 [(] _[𝑡]_ [)]









h _𝑥_ [(] _[𝑡]_ [)] ≔ [�] _𝑦_ ∈N( _𝑥_ ) _[𝑓]_ w [(][n] _𝑥_ _[,]_ [ n] _𝑦_ _[,]_ [ a] _𝑦𝑥_ _[,]_ [ h] _𝑦_ [(] _[𝑡]_ [−][1][)] )

- _𝑥_ [(] _[𝑡]_ [)] ≔ _𝑔_ w [′] (h _𝑥_ [(] _[𝑡]_ [)] _[,]_ [ n] _𝑥_ [)]


h1 [(] _[𝑡]_ [)] ≔ _𝑓_ w (n1 _,_ n3 _,_ a31 _,_ h3 [(] _[𝑡]_ [−][1][)] )
+ _𝑓_ w (n1 _,_ n4 _,_ a41 _,_ h4 [(] _[𝑡]_ [−][1][)] )
o1 [(] _[𝑡]_ [)] ≔ _𝑔_ w [′] (h1 [(] _[𝑡]_ [)] _[,]_ [ n][1][)]


...





n4 _,_ h4 [(] _[𝑡]_ [)]



n5 _,_ h5 [(] _[𝑡]_ [)]







Fig. 29. On the left a sub-graph of Figure 24 highlighting the neighbourhood of Punta Arenas, where nodes
are annotated with feature vectors (n _𝑥_ ) and hidden states at step _𝑡_ (h _𝑥_ [(] _[𝑡]_ [)] [), and edges are annotated with]
feature vectors (a _𝑥𝑦_ ); on the right, the GNN transition and output functions proposed by Scarselli et al. [462]
and an example for Punta Arenas ( _𝑥_ = 1), where N( _𝑥_ ) denotes the neighbouring nodes of _𝑥_, _𝑓_ w (·) denotes
the transition function with parameters w and _𝑔_ w [′] (·) denotes the output function with parameters w [′]


example, one-hot encode the type of node ( _City_, _Attraction_, etc.), directly encode statistics such as

the number of tourists visiting per year, etc. Feature vectors for edges may, for example, one-hot

encode the edge label (the type of transport), directly encode statistics such as the distance or

number of tickets sold per year, etc. Hidden states can be randomly initialised. The right-hand

side of Figure 29 provides the GNN transition and output functions, where N( _𝑥_ ) denotes the
neighbouring nodes of _𝑥_, _𝑓_ w (·) denotes the transition function with parameters w, and _𝑔_ w [′] (·)
denotes the output function with parameters w [′] . An example is also provided for Punta Arenas
( _𝑥_ = 1). These functions will be recursively applied until a fixpoint is reached. To train the network,

we can label examples of places that already have (or should have) tourist offices and places that do

(or should) not have tourist offices. These labels may be taken from the knowledge graph, or may
be added manually. The GNN can then learn parameters w and w [′] that give the expected output

for the labelled examples, which can subsequently be used to label other nodes.

This GNN model is flexible and can be adapted in various ways [462]: we may define neighbouring

nodes differently, for example to include nodes for outgoing edges, or nodes one or two hops away;

we may allow pairs of nodes to be connected by multiple edges with different vectors; we may

consider transition and output functions with distinct parameters for each node; we may add states

and outputs for edges; we may change the sum to another aggregation function; etc.


_5.3.2_ _Convolutional graph neural networks._ Convolutional neural networks (CNNs) have gained a

lot of attention, in particular, for machine learning tasks involving images [301]. The core idea in

the image setting is to apply small kernels (aka filters) over localised regions of an image using a

convolution operator to extract features from that local region. When applied to all local regions,

the convolution outputs a feature map of the image. Typically multiple kernels are applied, forming

multiple convolutional layers. These kernels can be learnt, given sufficient labelled examples.

One may note an analogy between GNNs as previously discussed, and CNNs as applied to images:

in both cases, operators are applied over local regions of the input data. In the case of GNNs, the

transition function is applied over a node and its neighbours in the graph. In the case of CNNs, the

convolution is applied on a pixel and its neighbours in the image. Following this intuition, a number

of _convolutional graph neural networks_ ( _ConvGNNs_ ) [71, 289, 559] have been proposed, where the

transition function is implemented by means of convolutions. A key consideration for ConvGNNs

is how regions of a graph are defined. Unlike the pixels of an image, nodes in a graph may have

varying numbers of neighbours. This creates a challenge: a benefit of CNNs is that the same kernel


45


can be applied over all the regions of an image, but this requires more careful consideration in the

case of ConvGNNs since neighbourhoods of different nodes can be diverse. Approaches to address

these challenges involve working with spectral (e.g. [71, 289]) or spatial (e.g., [358]) representations

of graphs that induce a more regular structure from the graph. An alternative is to use an attention

mechanism [535] to _learn_ the nodes whose features are most important to the current node.

Aside from architectural considerations, there are two main differences between RecGNNs and

ConvGNNs. First, RecGNNs aggregate information from neighbours recursively up to a fixpoint,

whereas ConvGNNs typically apply a fixed number of convolutional layers. Second, RecGNNs

typically use the same function/parameters in uniform steps, while different convolutional layers

of a ConvGNN can apply different kernels/weights at each distinct step.


**5.4** **Symbolic Learning**

The supervised techniques discussed thus far – namely knowledge graph embeddings and graph

neural networks – learn numerical models over graphs. However, such models are often difficult to

explain or understand. For example, taking the graph of Figure 30, knowledge graph embeddings

might predict the edge [SCL] flight ARI as being highly plausible, but they will not provide an

interpretable model to help understand why this is the case: the reason for the result may lie in a

matrix of parameters learnt to fit a plausibility score on training data. Such approaches also suffer

from the _out-of-vocabulary_ problem, where they are unable to provide results for edges involving

previously unseen nodes or edges; for example, if we add an edge [SCL] flight CDG, where [CDG] is

new to the graph, a knowledge graph embedding will not have the entity embedding for [CDG] and
would need to be retrained in order to estimate the plausibility of an edge [CDG] flight SCL .

An alternative (sometimes complementary) approach is to adopt _symbolic learning_ in order to

learn _hypotheses_ in a symbolic (logical) language that “explain” a given set of positive and negative

edges. These edges are typically generated from the knowledge graph in an automatic manner

(similar to the case of knowledge graph embeddings). The hypotheses then serve as interpretable

models that can be used for further deductive reasoning. Given the graph of Figure 30, we may,

for example, learn the rule [?x] flight ?y ⇒ [?y] flight ?x from observing that flight routes tend

to be return routes. Alternatively, we might learn a DL axiom stating that airports are either

domestic, international, or both: Airport ⊑ DomesticAirport ⊔ InternationalAirport. Such

rules and axioms can then be used for deductive reasoning, and offer an interpretable model for new

knowledge that is entailed/predicted; for example, from the aforementioned rule for return flights,

one can interpret why a novel edge [SCL] flight ARI is predicted. This further offers domain experts

the opportunity to verify the models – e.g., the rules and axioms – derived by such processes.

Finally, rules/axioms are quantified ( _all_ flights have a return flight, _all_ airports are domestic or

international, etc.), so they can be applied to unseen examples (e.g., with the aforementioned rule,

we can derive [CDG] flight SCL from a new edge [SCL] flight CDG with the unseen node [CDG] ).

In this section, we discuss two forms of symbolic learning: _rule mining_, which learns rules from

a knowledge graph, and _axiom mining_, which learns other forms of logical axioms. We refer to

Appendix B.6.4 for a more formal treatment of these two tasks.


_5.4.1_ _Rule mining._ Rule mining, in the general sense, refers to discovering meaningful patterns in

the form of rules from large collections of background knowledge. In the context of knowledge

graphs, we assume a set of positive and negative edges as given. Typically positive edges are

observed edges (i.e., those given or entailed by a knowledge graph) while negative edges are defined

according to a given assumption of completeness (discussed later). The goal of rule mining is to

identify new rules that entail a high ratio of positive edges from other positive edges, but entail a low

ratio of negative edges from positive edges. The types of rules considered may vary from more simple


46


Fig. 30. An incomplete directed edge-labelled graph describing flights between airports

cases, such as [?x] flight ?y ⇒ [?y] flight ?x mentioned previously, to more complex rules, such as
?x capital ?y nearby ?z type Airport ⇒ [?z] type International Airport, indicating that airports near
capitals tend to be international airports; or [?x] flight ?y country ?z ⇒ [?x] domestic flight ?y,


indicating that flights within the same country denote domestic flights (as seen in Section 4.3.1).

Per the international airport example, rules are not assumed to hold in all cases, but rather are

associated with measures of how well they conform to the positive and negative edges. In more

detail, we call the edges entailed by a rule and the set of positive edges (not including the entailed

edge itself), the _positive entailments_ of that rule. The number of entailments that are positive is called

the _support_ for the rule, while the ratio of a rule’s entailments that are positive is called the _confidence_

for the rule [508]. As such, support and confidence indicate, respectively, the number and ratio of

entailments “confirmed” to be true for the rule, where the goal is to identify rules that have both high

support and high confidence. In fact, techniques for rule mining in relational settings have long been

explored in the context of _Inductive Logic Programming_ ( _ILP_ ) [430]. However, knowledge graphs

present novel challenges due to the scale of the data and the frequent assumption of incomplete

data (OWA), where dedicated techniques have been proposed to address these issues [170].

When dealing with an incomplete knowledge graph, it is not immediately clear how to define

negative edges. A common heuristic – also used for knowledge graph embeddings – is to adopt

a Partial Completeness Assumption (PCA) [170], which considers the set of positive edges to be

those contained in the data graph, and the set of negative examples to be the set of all edges

_𝑥_ _𝑝_ _𝑦_ [′] not in the graph but where there exists a node _[𝑦]_ such that _[𝑥]_ _𝑝_ _𝑦_ is in the graph. Taking

Figure 30, an example of a negative edge under PCA would be [SCL] flight ARI (given the presence
of [SCL] flight LIM ); conversely, [SCL] domestic flight ARI is neither positive nor negative. The PCA

confidence measure is then the ratio of the support to all entailments in the positive or nega
confidence is [2] 2 [=][ 1 (noting that][ SCL] domestic flight ARI, though entailed, is neither positive nor

negative, and is thus ignored by the measure). The support for the rule [?x] flight ?y ⇒ [?y] flight ?x
is analogously 4, while the confidence is 5 [4] [=][ 0] _[.]_ [8 (noting that][ SCL] flight ARI is negative).

The goal then, is to find rules satisfying given support and confidence thresholds. An influential

rule-mining system for graphs is AMIE [169, 170], which adopts the PCA measure of confidence,


47


and builds rules in a top-down fashion [508] starting with rule heads like ⇒ [?x] country ?y . For

each rule head of this form (one for each edge label), three types of _refinements_ are considered,

each of which adds a new edge to the body of the rule. This new edge takes an edge label from the

graph and may otherwise use _fresh variables_ not appearing previously in the rule, _existing variables_

that already appear in the rule, or nodes from the graph. The three refinements may then:


(1) add an edge with one existing variable and one fresh variable; for example, refining the

aforementioned rule head might give: [?z] flight ?x ⇒ [?x] country ?y ;

(2) add an edge with an existing variable and a node from the graph; for example, refining the

above rule might give: Domestic Airport ~~type~~ ?z flight ?x ⇒ [?x] country ?y ;

(3) add an edge with two existing variables; for example, refining the above rule might give:







These refinements can be combined arbitrarily, which gives rise to a potentially exponential search

space, where rules meeting given thresholds for support and confidence are maintained. To improve

efficiency, the search space can be pruned; for example, these three refinements always decrease

support, so if a rule does not meet the support threshold, there is no need to explore its refinements.

Further restrictions are imposed on the types of rules generated. First, only rules up to a certain

fixed size are considered. Second, a rule must be _closed_, meaning that each variable appears in at

least two edges of the rule, which ensures that rules are _safe_, meaning that each variable in the head

appears in the body; for example, the rules produced previously by the first and second refinements

are neither closed (variable [y] appears once) nor safe (variable [y] appears only in the head). [27] To

ensure closed rules, the third refinement is applied until a rule is closed. For further discussion of

possible optimisations based on pruning and indexing, we refer to the paper on AMIE+ [169].

Later works have built on these techniques for mining rules from knowledge graphs. Gad-Elrab

et al. [168] propose a method to learn non-monotonic rules – rules with negated edges in the

body – in order to capture exceptions to base rules; for example, the approach may learn a rule





⇒ [?x] country ?y, indicating that flights are within



the same country _except_ when the (departure) airport is international, where the exception is shown

dotted and we use ¬ to negate an edge. The RuLES system [241] – which is also capable of learning

non-monotonic rules – proposes to mitigate the limitations of the PCA heuristic by extending the

confidence measure to consider the plausibility scores of knowledge graph embeddings for entailed

edges not appearing in the graph. Where available, explicit statements about the completeness of

the knowledge graph (such as expressed in shapes; see Section 3.1.2) can be used in lieu of PCA

for identifying negative edges. Along these lines, CARL [406] exploits additional knowledge about

the cardinalities of relations to refine the set of negative examples and the confidence measure

for candidate rules. Alternatively, where available, ontologies can be used to derive logically
certain negative edges under OWA through, for example, disjointness axioms. The system proposed

by d’Amato et al. [114, 115] leverages ontologically-entailed negative edges for determining the

confidence of rules generated through an evolutionary algorithm.

While the previous works involve discrete expansions of candidate rules for which a fixed

confidence scoring function is applied, another line of research is on a technique called _differentiable_

_rule mining_ [444, 455, 569], which allows end-to-end learning of rules. The core idea is that the

joins in rule bodies can be represented as matrix multiplication. More specifically, we can represent

the relations of an edge label _𝑝_ by the adjacency matrix A _𝑝_ (of size | _𝑉_ | × | _𝑉_ |) such that the value

on the _𝑖_ [th] row of the _𝑗_ [th] column is 1 if there is an edge labelled _𝑝_ from the _𝑖_ [th] entity to the _𝑗_ [th]

27Safe rules like ?x capital ?y nearby ?z type Airport ⇒ [?z] type International Airport are not closed as [?x]

appears only in one edge. Hence the condition that rules are closed is strictly stronger than the condition that they are safe.


48


entity; otherwise the value is 0. Now we can represent a join in a rule body as matrix multiplication;

for example, given [?x] domestic flight ?y country ?z ⇒ [?x] country ?z, we can denote the body by
the matrix multiplication Adf.Ac., which gives an adjacency matrix representing entailed country
edges, where we should expect the 1’s in Adf.Ac. to be covered by the head’s adjacency matrix Ac..

Since we are given adjacency matrices for all edge labels, we are left to learn confidence scores

for individual rules, and to learn rules (of varying length) with a threshold confidence. Along

these lines, NeuralLP [569] uses an _attention mechanism_ to select a variable-length sequence of

edge labels for path-like rules of the form [?x] p1 ?y1 p2 ... p _𝑛_ ?y _𝑛_ p _𝑛_ +1 ?z ⇒ [?x] p ?z,

for which confidences are likewise learnt. DRUM [455] also learns path-like rules, where, observing

that some edge labels are more/less likely to follow others in the rules – for example, flight will
not be followed by capital in the graph of Figure 24 as the join will be empty – the system uses

bidirectional recurrent neural networks (a popular technique for learning over sequential data)

to learn sequences of relations for rules, and their confidences. These differentiable rule mining

techniques are, however, currently limited to learning path-like rules.


_5.4.2_ _Axiom mining._ Aside from rules, more general forms of axioms – expressed in logical

languages such as DLs (see Section 4.3.2) – can be mined from a knowledge graph. We can divide

these approaches into two categories: those mining specific axioms and more general axioms.

Among systems mining specific types of axioms, disjointness axioms are a popular target; for

example, the disjointness axiom DomesticAirport ⊓ InternationalAirport ≡⊥ states that the

intersection of the two classes is equivalent to the empty class, or in simpler terms, no node can be

simultaneously of type [Domestic Airport] and [International Airport] . The system proposed by Völker et al.

[540] extracts disjointness axioms based on (negative) _association rule mining_ [5], which finds pairs

of classes where each has many instances in the knowledge graph but there are relatively few (or

no) instances of both classes. Töpper et al. [524] rather extract disjointness for pairs of classes that

have a cosine similarity below a fixed threshold. For computing this cosine similarity, class vectors

are computed using a TF–IDF analogy, where the “document” of each class is constructed from all

of its instances, and the “terms” of this document are the properties used on the class’ instances

(preserving multiplicities). While the previous two approaches find disjointness constraints between

named classes (e.g., _city_ is disjoint with _airport_ ), Rizzo et al. [443] propose an approach that can

capture disjointness constraints between class descriptions (e.g., _city without an airport nearby_ is

disjoint with _city that is the capital of a country_ ). The approach first clusters similar nodes of the

knowledge base. Next, a _terminological cluster tree_ is extracted, where each leaf node indicates

a cluster extracted previously, and each internal (non-leaf) node is a class definition (e.g., _cities_ )

where the left child is either a cluster having all nodes in that class or a sub-class description (e.g.,

_cities without airports_ ) and the right child is either a cluster having no nodes in that class or a

disjoint-class description (e.g., _non-cities with events_ ). Finally, candidate disjointness axioms are

proposed for pairs of class descriptions in the tree that are not entailed to have a subclass relation.

Other systems propose methods to learn more general axioms. A prominent such system is DL
Learner [73], which is based on algorithms for _class learning_ (aka _concept learning_ ), whereby given

a set of positive nodes and negative nodes, the goal is to find a logical class description that divides

the positive and negative sets. For example, given { [Iquique] _,_ [Arica] } as the positive set and { [Santiago] }
as the negative set, we may learn a (DL) class description ∃nearby _._ Airport ⊓¬(∃capital [−] _._ ⊤),

denoting entities near to an airport that are not capitals, of which all positive nodes are instances

and no negative nodes are instances. Such class descriptions are learnt in an analogous manner to

how aforementioned systems like AMIE learn rules, with a refinement operator used to move from

more general classes to more specific classes (and vice-versa), a confidence scoring function, and

a search strategy. The system further supports learning more general axioms through a scoring


49


Pre-Processing: Santiago has flights to Rapa Nui, which was named a World Heritage Site in 1995 .


Named Entity
Santiago Rapa Nui World Heritage Site 1995
Recognition:


Entity Linking: Santiago Easter Island World Heritage Site 1995


Relation Extraction


Fig. 31. Text extraction example; nodes new to the knowledge graph are shown dashed


function that uses count queries to determine what ratio of expected edges – edges that would

be entailed were the axiom true – are indeed found in the graph; for example, to score the axiom
∃flight [−] _._ DomesticAirport ⊑ InternationalAirport over Figure 30, we can use a graph query
