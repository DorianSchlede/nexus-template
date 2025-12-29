<!-- Source: 02-Knowledge_Graphs.pdf | Chunk 7/15 -->


In the following we discuss _quality dimensions_ that capture aspects of multifaceted data quality

which evolves from the traditional domain of databases to the domain of knowledge graphs [33],

some of which are general, others of which are more particular to knowledge graphs [574]. While

quality dimensions aim to capture qualitative aspects of the data, we also discuss _quality metrics_

that provide ways to measure quantitative aspects of these dimensions. We discuss groupings of

dimensions and metrics as inspired by Batini and Scannapieco [34].


**7.1** **Accuracy**


Accuracy refers to the extent to which entities and relations – encoded by nodes and edges in the

graph – correctly represent real-life phenomena. Accuracy can be further sub-divided into three

dimensions: _syntactic accuracy_, _semantic accuracy_, and _timeliness_ .


_7.1.1_ _Syntactic accuracy_ is the degree to which the data are accurate with respect to the grammat
ical rules defined for the domain and/or data model. A prevalent example of syntactic inaccuracies

occurs with datatype nodes, which may be incompatible with a defined range or be malformed. For

example, assuming that a property start is defined with the range xsd:dateTime, taking a value


58


such as ["March 29, 2019, 20:00"^^xsd:string] would be incompatible with the defined range, while a value


"March 29, 2019, 20:00"^^xsd:dateTime would be malformed (a value such as "2019-03-29T20:00:00"^^xsd:dateTime is

rather expected). A corresponding metric for syntactic accuracy is the ratio between the number of

incorrect values of a given property and the total number of values for the same property [574].

Such forms of syntactic accuracy can typically be assessed using validation tools [167, 248].


_7.1.2_ _Semantic accuracy_ is the degree to which data values correctly represent real world phenom
ena, which may be affected by imprecise extraction results, imprecise entailments, vandalism, etc.

For instance, given that the National Congress of Chile is located in Valparaíso, this may give rise to

the edge [Chile] capital Valparaiso (through entailment, extraction, completion, etc.), which is in fact

semantically inaccurate: the Chilean capital is Santiago. Assessing the level of semantic inaccuracies

is challenging. While one option is to apply manual verification, an automatic option may be to

check the stated relation against several sources [146, 313]. Another option is to rather validate the

quality of individual processes used to generate the knowledge graph, based on measures such as

precision, possibly with the help of human experts or gold standards [338].


_7.1.3_ _Timeliness_ is the degree to which the knowledge graph is currently up-to-date with the

real world state [276]; in other words, a knowledge graph may be semantically accurate now, but

may quickly become inaccurate (outdated) if no procedures are in place to keep it up-to-date in

a timely manner. For example, consider a user checking the tourist knowledge graph for flights

from one city to another. Suppose that the flight timetable is updated every minute with current

flight statuses, but the knowledge graph is only updated every hour. In this case, we see that there

is a quality issue regarding timeliness in the knowledge graph. Timeliness can be assessed based

on how frequently the knowledge graph is updated with respect to underlying sources [276, 452],

which can be done using temporal annotations of changes in the knowledge graph [450, 451], as

well as contextual representations that capture the temporal validity of data (see Section 3.3).


**7.2** **Coverage**


Coverage refers to avoiding the omission of domain-relevant elements, which otherwise may yield

incomplete query results or entailments, biased models, etc.


_7.2.1_ _Completeness_ refers to the degree to which all required information is present in a particular

dataset. Completeness comprises the following aspects: (i) _schema completeness_ refers to the degree

to which the classes and properties of a schema are represented in the data graph, (ii) _property_

_completeness_ refers to the ratio of missing values for a specific property, (iii) _population completeness_

provides the percentage of all real-world entities of a particular type that are represented in

the datasets, and (iv) _linkability completeness_ refers to the degree to which instances in the data

set are interlinked. Measuring completeness directly is non-trivial as it requires knowledge of a

hypothetical _ideal knowledge graph_ [116] that contains all the elements that the knowledge graph

in question should “ _ideally_ ” represent. Concrete strategies involve comparison with gold standards

that provide samples of the ideal knowledge graph (possibly based on _completeness statements_ [116]),

or measuring the recall of extraction methods from complete sources [338], and so forth.


_7.2.2_ _Representativeness_ is a related dimension that, instead of focusing on the ratio of domain
relevant elements that are missing, rather focuses on assessing high-level _biases_ in what is includ
ed/excluded from the knowledge graph [25]. As such, this dimension assumes that the knowledge

graph is incomplete – i.e., that it is a sample of the ideal knowledge graph – and asks how biased

this sample is. Biases may occur in the data, in the schema, or during reasoning [270]. Examples

of data biases include geographic biases that under-represent entities/relations from certain parts

of the world [270], linguistic biases that under-represent multilingual resources (e.g., labels and


59


descriptions) for certain languages [277], social biases that under-represent people of particular

genders or races [545], and so forth. In contrast, schema biases may result from high-level defini
tions extracted from biased data [270], semantic definitions that do not cover uncommon cases,

etc. Unrecognised biases may lead to adverse effects; for example, if our tourism knowledge graph

has a geographic bias towards events and attractions close to Santiago city – due perhaps to the

sources used for creation, the employment of curators from the city, etc. – then this may lead to

tourism in and around Santiago being disproportionally promoted (potentially compounding future

biases). Measures of representativeness involve comparison of known statistical distributions with

those of the knowledge graph, for example, comparing geolocated entities with known population

densities [270], linguistic distributions with known distributions of speakers [277], etc. Another

option is to compare the knowledge graph with general statistical laws, where Soulet et al. [489]

use (non-)conformance with Benford’s law [29] to measure representativeness in knowledge graphs.


**7.3** **Coherency**


Coherency refers to how well the knowledge graph conforms to – or is coherent with – the formal

semantics and constraints defined at the schema-level.


_7.3.1_ _Consistency_ means that a knowledge graph is free of (logical/formal) contradictions with re
spect to the particular logical entailment considered. For example, in the ontology of our knowledge


“not” condition can give rise to inconsistencies if the negated condition is entailed. A measure of

consistency can be the number of inconsistencies found in a knowledge graph, possibly sub-divided

into the number of such inconsistencies identified by each semantic feature [58].


_7.3.2_ _Validity_ means that the knowledge graph is free of constraint violations, such as captured by

shape expressions [521] (see Section 3.1.2). We may, for example, specify a shape City whose target

nodes have at most one country. Then, given the edges [Chile] country Santiago country Cuba, and

assuming that [Santiago] becomes a target of City, we have a constraint violation. Conversely, even if

we defined analogous cardinality restrictions in an ontology, this would not necessarily cause an

inconsistency since, without UNA, we would first infer that [Chile] and [Cuba] refer to the same entity.

A straightforward measure of validity is to count the number of violations per constraint.


**7.4** **Succinctness**


Succinctness refers to the inclusion only of relevant content (avoiding “information overload”) that

is represented in a concise and intelligible manner.


_7.4.1_ _Conciseness_ refers to avoiding the inclusion of schema and data elements that are irrelevant

to the domain. Mendes et al. [349] distinguish _intensional conciseness_ (schema level), which refers

to the case when the data does not contain redundant schema elements (properties, classes, shapes,

etc.), and _extensional conciseness_ (data level), when the data does not contain redundant entities

and relations. For example, including events in [Santiago de Cuba] in our knowledge graph dedicated

to tourism in Chile may affect the extensional conciseness of the knowledge graph, potentially

returning irrelevant results for the given domain. In general, conciseness can be measured in terms

of the ratio of properties, classes, shapes, entities, relations, etc., of relevance to the domain, which

may in turn require a gold standard, or techniques to assess domain-relevance.


29Benford’s law states that the leading significant digit in many collections of numbers is more likely to be small.


60


_7.4.2_ _Representational-conciseness_ refers to the extent to which content is compactly represented

in the knowledge graph, which may again be intensional or extensional [574]. For example, having

two properties flight and flies to serving the same purpose would negatively affect the intensional
form of representational conciseness, while having two nodes [Santiago] and [Santiago de Chile] repre
senting the capital of Chile (with neither linked to the other) would affect the extensional form

of representational conciseness. Another example of representational conciseness is the unneces
sary use of complex modelling constructs, such as using reification unnecessarily, or using linked

lists when the order of elements is not important [250]. Though representational conciseness is

challenging to assess, measures such as the number of redundant nodes can be used [167].


_7.4.3_ _Understandability_ refers to the ease with which data can be interpreted without ambiguity by

human users, which involves – at least – the provision of human-readable labels and descriptions

(preferably in different languages [277]) that allow them to understand what is being spoken

about [250]. Referring back to Figure 1, though the nodes [EID15] and [EID16] are used to ensure unique

identifiers for events, they should also be associated with labels such as [Ñam] and [Food Truck] . Ideally

the human readable information is sufficient to disambiguate a particular node, such as associating

a description ["Santiago, the capital of Chile"@en] with [Santiago] to disambiguate the city from synonymous

ones. Measures of understandability may include the ratio of nodes with human-readable labels

and descriptions, the uniqueness of such labels and descriptions, the languages supported, etc.


**7.5** **Other Quality Dimensions**


We have discussed some key quality dimensions that have been discussed for – and apply generally

to – knowledge graphs. Further dimensions may be pertinent in the context of specific domains,

specific applications, or specific graph data models. For further details, we refer to the survey

by Zaveri et al. [574] and to the book by Batini and Scannapieco [34].


**8** **REFINEMENT**


Beyond assessing the quality of a knowledge graph, there exist techniques to refine the knowledge

graph, in particular to (semi-)automatically complete and correct the knowledge graph [400], aka

_knowledge graph completion_ and _knowledge graph correction_, respectively. As distinguished from the

creation and enrichment tasks outlined in Section 6, refinement typically does not involve applying

extraction or mapping techniques over external sources in order to ingest their content into the

local knowledge graph. Instead, refinement typically targets improvement of the local knowledge

graph as given (but potentially using external sources to verify local content [400]).


**8.1** **Completion**


Knowledge graphs are characterised by incompleteness [555]. As such, knowledge graph completion

aims at filling in the _missing edges_ (aka _missing links_ ) of a knowledge graph, i.e., edges that are

deemed correct but are neither given nor entailed by the knowledge graph. This task is often

addressed with _link prediction_ techniques proposed in the area of _Statistical Relational Learning_ [184],

which predict the existence – or sometimes more generally, predict the probability of correctness

- of missing edges. For instance, one might predict that the edge [Moon Valley] bus San Pedro is a

probable missing edge for the graph of Figure 24, given that most bus routes observed are return

services (i.e., bus is typically symmetric). Link prediction may target three settings: _general links_
involving edges with arbitrary labels, e.g., bus, flight, type, etc.; _type links_ involving edges with
label type, indicating the type of an entity; and _identity links_ involving edges with label same as,

indicating that two nodes refer to the same entity (cf. Section 3.2.2). While type and identity links

can be addressed using general link prediction techniques, the particular semantics of type and


61


identity links can be addressed with custom techniques. (The related task of generating links across

knowledge graphs – referred to as _link discovery_ [374] – will be discussed later in Section 9.1.)


_8.1.1_ _General link prediction._ Link prediction, in the general case, is often addressed with inductive

techniques as discussed in Section 5, and in particular, knowledge graph embeddings and rule/axiom

mining. For example, given Figure 24, using knowledge graph embeddings, we may detect that

given an edge of the form _[𝑥]_ bus _𝑦_, a (missing) edge _[𝑦]_ bus _𝑥_ has high plausibility, while
using symbol-based approaches, we may learn the high-level rule [?x] bus ?y ⇒ [?y] bus ?x .
Either such approach would help us to predict the missing link [Moon Valley] bus San Pedro .


_8.1.2_ _Type-link prediction._ Type links are of particular importance to a knowledge graph, where

dedicated techniques can be leveraged taking into account the specific semantics of such links.

In the case of type prediction, there is only one edge label (type) and typically fewer distinct

values (classes) than in other cases, such that the task can be reduced to a traditional classification

task [400], training models to identify each semantic class based on features such as outgoing

and/or incoming edge labels on their instances in the knowledge graph [402, 486]. For example,

assume that in Figure 24 we also know that [Arica], [Calama], [Puerto Montt], [Punta Arenas] and [Santiago] are
of type [City] . We may then predict that [Iquique] and [Easter Island] are also of type [City] based on the
presence of edges labelled flight to/from these nodes, which (we assume) are learnt to be a good

feature for prediction of that class (the former prediction is correct, while the latter is incorrect).

Graph neural networks (see Section 5.3) can also be used for node classification/type prediction.


_8.1.3_ _Identity-link prediction._ Predicting identity links involves searching for nodes that refer to

the same entity; this is analogous to the task of _entity matching_ (aka record linkage, deduplication,

etc.) considered in more general data integration settings [297]. Such techniques are generally

based on two types of _matchers_ : _value matchers_ determine how similar the values of two entities on

a given property are, which may involve similarity metrics on strings, numbers, dates, etc.; while

_context matchers_ consider the similarity of entities based on various nodes and edges [297]. An

illustrative example is given in Figure 35, where value matchers will compute similarity between

values such as [7400] and [7500], while context matchers will compute similarity between [Easter Island] and


Rapa Nui based on their surrounding information, such as their having similar latitudes, longitudes,

populations, and the same seat (by way of comparison, a value matcher on this pair of nodes would

measure string similarity between “Easter Island” and “Rapa Nui”).
A major challenge in this setting is efficiency, where a pairwise matching would require _𝑂_ ( _𝑛_ [2] )

comparisons for _𝑛_ the number of nodes. To address this issue, _blocking_ can be used to group similar

entities into (possibly overlapping, possibly disjoint) “blocks” based on similarity-preserving keys,

with matching performed within each block [133, 265, 297]; for example, if matching places based

on latitude/longitude, blocks may represent geographic regions. An alternative to discrete blocking

is to use _windowing_ over entities in a similarity-preserving ordering [133], or to consider searching

for similar entities within _multi-dimensional spaces_ (e.g., spacetime [460], spaces with Minkowski

distances [379], orthodromic spaces [380], etc. [477]). The results can either be pairs of nodes with a

computed confidence of them referring to the same entity, or crisp identity links extracted based on

a fixed threshold, binary classification, etc. [297]. For confident identity links, the nodes’ edges may

then be _consolidated_ [251]; for example, we may select [Easter Island] as the canonical node and merge

the edges of [Rapa Nui] onto it, enabling us to find, e.g., _World Heritage Sites in the Pacific Ocean_ from
Figure 35 based on the (consolidated) sub-graph [World Heritage Site] named Easter Island ocean Pacific .


62


Fig. 35. Identity linking example, where Rapa Nui and Easter Island refer to the same island


**8.2** **Correction**


As opposed to completion – which finds new edges in a knowledge graph – correction identifies and

removes existing incorrect edges in the knowledge graph. We here divide the principal approaches

for knowledge graph correction into two main lines: _fact validation_, which assigns a plausibility

score to a given edge, typically in reference to external sources; and _inconsistency repairs_, which

aim to resolve inconsistencies found in the knowledge graph through ontological axioms.


_8.2.1_ _Fact validation._ The task of _fact validation_ (aka _fact checking_ ) [63, 146, 181, 478, 481, 488, 513,

514, 572] involves assigning plausibility or _veracity_ scores to facts/edges, typically between 0 and 1.

An ideal fact-checking function assumes a hypothetical reference universe (an ideal knowledge

graph) and would return 1 for the fact [Santa Lucía] city Santiago (being true) while returning 0 for
Sotomayor city Santiago (being false). There is a clear relation between fact validation and link

prediction – with both relying on assessing the plausibility of edges/facts/links – and indeed the

same numeric- and symbol-based techniques can be applied for both cases. However, fact validation

often considers online assessment of edges given as input, whereas link prediction is often an offline

task that generates novel candidate edges to be assessed from the knowledge graph. Furthermore,

works on fact validation are characterised by their consideration of external reference sources,

which may be _unstructured sources_ [181, 458, 513, 572] or _structured sources_ [63, 478, 481, 488, 514].

Approaches based on unstructured sources assume that they are given a _verbalisation function_

- using, for example, rule-based approaches [143, 381], encoder–decoder architectures [176], etc.

- that is able to translate edges into natural language. Thereafter, approaches for computing the

plausibility of facts in natural language – called _fact finders_ [398, 399] – can be directly employed.

Many fact finding algorithms construct an _𝑛_ -partite (often bipartite) graph whose nodes are facts

and sources, where a source is connected to a fact if the source “evidences” the fact, i.e., if it contains

a text snippet that matches – with sufficient confidence – the verbalisation of the input edge. Two

mutually-dependent scores, namely the trustworthiness of sources and the plausibility of facts,

are then calculated based on this graph, where fact finders differ on how they compute these

scores [399]. Here we mention three scores proposed by Pasternack and Roth [398]:


  - _Sums_ [398] adapts the HITS algorithm [292] by defining sources as hubs (with 0 authority

score) and facts as authorities (with 0 hub score).

  - _Average Log_ [398] extends HITS with a normalisation factor that prevents a single source

from receiving a high trustworthiness score by evidencing many facts (that may be false).

  - _Investment_ [398] lets the scores of facts grow with a non-linear function based on “investments”

coming from the connected sources. The score a source receives from a fact is based on the

individual facts in this particular source compared to the other connected sources.


Pasternack and Roth [399] then show that these three algorithms can be generalised into a single

multi-layered graph-based framework within which (1) a source can support a fact with a weight

expressing uncertainty, (2) similar facts can support each other, and (3) sources can be grouped

together leading to an implicit support between sources of the same group. Other approaches for


63


fact checking of knowledge graphs later extended this framework [171, 458]. Alternative approaches

based on classifiers have also emerged, where commonly-used features include trust scores for

information sources, co-occurrences of facts in sources, and so forth [181, 513].

Approaches for fact validation based on structured data typically assume external knowledge

graphs as reference sources and are based on finding paths that evidence the input edge being

validated. Unsupervised approaches search for undirected [91, 481] or directed [514] paths up to

a given threshold length that evidence the input edge. The relatedness between input edges and

paths is computed using a mutual information function, such as normalized pointwise mutual

information [64]. Supervised approaches rather extract features for input edges from external

knowledge graphs [309, 510, 578] and use these features to train a classification model to label

the edges as true or false. An important set of features are _metapaths_, which encode sequences of

predicates that correlate positively with the edge label of the input edge. Amongst such works,

PredPath [478] automatically extracts metapaths based on type information. Several approaches

rather encode the reference nodes and edges using graph embeddings (see Section 5.2), which are

then used to estimate the plausibility of the input edge being validated.


_8.2.2_ _Inconsistency repairs._ Ontologies can contain axioms – such as disjointness – that lead to

inconsistencies. While such axioms can be provided by experts, they can also be derived through

symbolic learning, as discussed in Section 5.4. Such axioms can then be used to detect inconsistencies.

With respect to correcting a knowledge graph, however, detecting inconsistencies is not enough:

techniques are also required to _repair_ such inconsistencies, which itself is not a trivial task. In

the simplest case, we may have an instance of two disjoint classes, such as that [Santiago] is of type


City and Airport, which are stated or found to be disjoint. To repair the inconsistency, it would be

preferable to remove only the “incorrect” class, but which should we remove? This is not a trivial

question, particularly if we consider that one edge can be involved in many inconsistencies, and one

inconsistency can involve many edges. The issue of computing repairs becomes more complex when

entailment is considered, where we not only need to remove the stated type, but also all of the ways

in which it might be entailed; for example, removing the edge [Santiago] type Airport is insufficient if
we further have an edge [Arica] flight Santiago combined with an axiom [flight] range Airport . Töpper

et al. [524] suggest potential repairs for such violations – remove a domain/range constraint, remove

a disjointness constraint, remove a type edge, remove an edge with a domain/range constraint –

where one is chosen manually. In contrast, Bonatti et al. [58] propose an automated method to

repair inconsistencies based on _minimal hitting sets_ [436], where each set is a minimal explanation

for an inconsistency. The edges to remove are chosen based on scores of the trustworthiness of

their sources and how many minimal hitting sets they are either elements of or help to entail an

element of, where the knowledge graph is revised to avoid re-entailment of the removed edges.

Rather than repairing the data, another option is to evaluate queries under inconsistency-aware

semantics, such as returning _consistent answers_ valid under every possible repair [329].


**8.3** **Other refinement tasks**


In comparison to the quality clusters discussed in Section 7, the refinement methods discussed here

address particular aspects of the accuracy, coverage, and coherency dimensions. Beyond these, one

could conceive of further refinement methods to address further quality issues of knowledge graphs,

such as succinctness. In general, however, the refinement tasks of _knowledge graph completion_ and

_knowledge graph correction_ have received the majority of attention until now. For further details on

knowledge graph refinement, we refer to the survey by Paulheim [400].


64


**9** **PUBLICATION**

While it may not be desirable to publish, for example, enterprise knowledge graphs that offer a

competitive advantage to a company [387], it may be desirable – or even required – to publish

other knowledge graphs, such as those produced by volunteers [311, 333, 543], by publicly-funded

research [82, 200, 519], by governmental organisations [233, 475], etc. Publishing refers to making

the knowledge graph (or part thereof) accessible to the public, often over the Web. Knowledge

graphs published as open data are then called open knowledge graphs (discussed in Section 10.1).

In the following, we first discuss two sets of principles that have been proposed to guide the

publication of data on the Web. We next discuss access protocols that constitute the interfaces

by which the public can interact with the content of a knowledge graph. Finally, we consider

techniques to restrict the access or usage of (parts of) a knowledge graph, as appropriate.


**9.1** **Best Practices**


We now discuss two key sets of principles for publishing data, namely the FAIR Principles proposed

by Wilkinson et al. [556], and the Linked Data Principles proposed by Berners-Lee [41].


_9.1.1_ _FAIR Principles._ The FAIR Principles were originally proposed in the context of publishing

scientific data [556] – particularly motivated by maximising the impact of publicly-funded research

- but the principles generally apply to other situations where data are to be published in a manner

that facilitates their re-use by external agents, with particular emphasis on machine-readability.

FAIR itself is an acronym for four foundational principles, each with particular goals [556], that

may apply to _data_, _metadata_, or both – the latter being denoted _(meta)data_ . [30] We now describe the

FAIR principles (slightly rephrasing the original wording in some cases for brevity [556]).


  - _Findability_ refers to the ease with which external agents who might benefit from the dataset

can initially locate the dataset. Four sub-goals should be met:

**–** F1: (meta)data are assigned a globally unique and persistent identifier.

**–** F2: data are described with rich metadata (see R1).

**–** F3: metadata clearly and explicitly include the identifier of the data they describe.

**–** F4: (meta)data are registered or indexed in a searchable resource.

  - _Accessibility_ refers to the ease with which external agents (once they have located the dataset)

can access the dataset. Two goals are defined, the first with two sub-goals:

**–** A1: (meta)data are retrievable by their identifier using a standard protocol.

    - A1.1: the protocol is open, free, and universally implementable.

    - A1.2: the protocol allows for authentication and authorisation, where necessary.

**–** A2. metadata are accessible, even when the data are no longer available.

  - _Interoperability_ refers to the ease with which the dataset can be exploited (in conjunction

with other datasets) using standard tools. Three goals are defined:

**–** I1: (meta)data use an accessible, shared, and general knowledge representation formalism.

**–** I2: (meta)data use vocabularies that follow FAIR principles.

**–** I3: (meta)data include qualified references to other (meta)data.

  - _Reusability_ refers to the ease with which the dataset can be re-used in conjunction with other

datasets. One goal is defined (with three sub-goals):

**–** R1: meta(data) are richly described with a plurality of accurate and relevant attributes.

    - R1.1. (meta)data are released with a clear and accessible data usage license.

    - R1.2. (meta)data are associated with detailed provenance.


30Metadata are data about data. The distinction is often important in observational sciences, where in astronomy, for

example, data may include raw image data, while metadata may include the celestial coordinates and time of the image.


65


Fig. 36. Two example Linked Data documents from two websites, each containing an RDF graph, where
wd:Q142701 refers to Pearl Jam in Wikidata while wdd:Q142701 refers to the RDF graph about Pearl Jam, and
where wd:Q221535 refers to Eddie Vedder while wdd:Q221535 refers to the RDF graph about Eddie Vedder;
the edge-label wdt:571 refers to “inception” in Wikidata, while wdt:527 refers to “has part”


    - R1.3. (meta)data meet domain-relevant community standards.

In the context of knowledge graphs, a variety of vocabularies, tools, and services have been

proposed that both directly and indirectly help to satisfy the FAIR principles. In terms of _Findability_,

as discussed in Section 2, IRIs are built into the RDF model, providing a general schema for global

identifiers. In addition, resources such as the Vocabulary of Interlinked Datasets (VoID) [11] allow

for representing meta-data about graphs, while services such as DataHub [45] provide a central

repository of such dataset descriptions. Access protocols that enable _Accessibility_ will be discussed

in Section 9.2, while mechanisms for authorisation will be discussed in Section 9.3. With respect to

_Interoperability_, as discussed in Section 4, ontologies serve as a general knowledge representation

formalism, and can in turn be used to describe vocabularies that follow FAIR principles. Finally,

regarding _Reusability_, licensing will be discussed in Section 9.3, while the _PROV Data Model_ [188]

discussed in Section 3 allows for capturing detailed provenance.

A number of knowledge graphs have been published using FAIR principles, where Wilkinson

et al. [556] explicitly mention Open PHACTS [200], a data integration platform for drug discovery,

and UniProt [519], a large collection of protein sequence and annotation data, as conforming to

FAIR principles. Both datasets offer graph views of their content through the RDF data model.


_9.1.2_ _Linked Data Principles._ Wilkinson et al. [556] state that FAIR Principles “precede implemen
tation choices”, meaning that the principles do not cover _how_ they can or should be achieved.

Preceding the FAIR Principles by almost a decade are the Linked Data Principles, proposed by

Berners-Lee [41], which provide a technical basis for one possible way in which these FAIR Princi
ples can be achieved. Specifically the Linked Data Principles are as follows:


(1) Use IRIs as names for things.

(2) Use HTTP IRIs so those names can be looked up.

(3) When a HTTP IRI is looked up, provide useful content about the entity that the IRI names

using standard data formats.

(4) Include links to the IRIs of related entities in the content returned.

These principles were proposed in a Semantic Web setting, where for principle (3), the standards

based on RDF (including RDFS, OWL, etc.) are currently recommended for use, particularly because

they allow for naming entities using HTTP IRIs, which further paves the way for satisfying all four

principles. As such, these principles outline a way in which (RDF) graph-structured data can be

published on the Web such that these graphs are interlinked to form what Berners-Lee [41] calls a

“Web of Data”, whose goal is to increase automation on the Web by making content available not


66


only in (HTML) documents intended for human consumption, but also as (RDF) structured data

that machines can locate, retrieve, combine, validate, reason over, query over, etc., towards solving

tasks automatically. Conceptually, the Web of Data is then composed of graphs of data published

on individual web-pages, where one can click on a node or edge-label – or more precisely perform

a HTTP lookup on an IRI of the graph – to be transported to another graph elsewhere on the Web

with relevant content on that node or edge-label, and so on recursively.

In Figure 36, we show a simple example with two Linked Data documents published on the

Web, with each containing an RDF graph. As discussed in Section 3.2, terms such as clv:Concert,
wd:Q142701, rdfs:label, etc., are abbreviations for IRIs, where, for example, wd:Q142701 expands
[to http://www.wikidata.org/entity/Q142701. Prefixes beginning with cl are fictitious prefixes we](http://www.wikidata.org/entity/Q142701)
assume to have been created by the Chilean tourist board. The IRIs prefixed with _↩_ →� indicate the

document returned if the node is looked up. The leftmost document is published by the tourist board

and describes Lollapalooza 2018 (identified by the node [cle:LP2018] ), which links to the headlining act

Pearl Jam ( [wd:Q142701] ) described by an external knowledge graph, namely Wikidata. By looking up

the node [wd:Q142701] in the leftmost graph, the IRI _dereferences_ (i.e., returns via HTTP) the document

with the RDF graph on the right describing that entity in more detail. From the rightmost document,

the node [wd:Q221535] can be looked up, in turn, to find a graph about Eddie Vedder (not shown in the

example). The IRIs for entities and documents are distinguished to ensure that we do not confuse

data about the entity and the document; for example, while wd:Q221535 refers to Eddie Vedder, the
IRI wd **d** :Q221535 refers to the document about Eddie Vedder; if we were to assign a last-modified

date to the document, we should use [wd] **[d]** [:Q221535] not [wd:Q221535] . In Figure 36, we can further observe

that edge labels (which are also IRIs) and nodes representing classes (e.g., [clv:Concert] ) can also be

dereferenced, typically returning semantic definitions of the respective terms.

A key challenge is posed by the fourth principle – include links to related entities – as illustrated

in Figure 36, where [wd:Q221535] in the leftmost graph constitutes a link to related content about Pearl

Jam in an external knowledge graph. Specifically, the _link discovery_ task considers adding such

links from one knowledge graph to another, which may involve inclusion of IRIs that dereference to

external graphs (per Figure 36), or links with special semantics such as identity links. In comparison

with the link prediction task discussed in Section 8.1, which is used to complete links within a

knowledge graph, link discovery aims to discover links across knowledge graphs, which involves

unique aspects: first, link discovery typically considers disjoint sets of source (local) nodes and

target (remote) nodes; second, the knowledge graphs may often use different vocabularies; third,

while in link prediction there already exist local examples of the links to predict, in link discovery,

there are often no existing links between knowledge graphs to learn from. A common technique is

to define manually-crafted linkage rules (aka link specifications) that apply heuristics for defining

links that potentially incorporate similarity measures [378, 541]. Link discovery is greatly expedited

by the provision of standard identifier schemes within knowledge graphs, such as ISBNs for books,

alpha-2 and alpha-3 codes for countries (e.g., cl, clp), or even links to common knowledge graphs

such as DBpedia [311] or Wikidata [543] (that themselves include standard identifiers). We refer to

the survey on link discovery by Nentwig et al. [374] for more details.

Further guidelines have been proposed that provide finer-grained recommendations for pub
lishing Linked Data, relating to how best implement dereferencing, what kinds of links to include,

how to publish and interlink vocabularies, amongst other considerations [226, 269]. We refer to the

book by Heath and Bizer [226] for more discussion on how to publish Linked Data on the Web.


67


Dumps Node Lookups Edge Patterns (Complex) Graph Patterns



_More bandwidth_


_Less server CPU_



_Less bandwidth_

_More server CPU_



Fig. 37. Access protocols for knowledge graphs, from simple protocols (left) to more complex protocols (right)


**9.2** **Access Protocols**

Publishing involves allowing the public to interact with the knowledge graph, which implies the

provision of _access protocols_ that define the requests that agents can make and the response that they

can expect as a result. Per the _Accessibility_ principle of FAIR (specifically A1.1), this protocol should

be open, free, and universally implementable. In the context of knowledge graphs, as shown in

Figure 37, there are a number of access protocols to choose from, varying from simple protocols that

allow users to simply download all content, towards protocols that accept and evaluate increasingly

complex requests. While simpler protocols require less computation on the server that publishes the

data, more complex protocols allow agents to request more specific data, thus reducing bandwidth.

A knowledge graph may also offer a variety of access protocols catering to different agents with

different requirements [536]. We now discuss such access protocols.


_9.2.1_ _Dumps._ A dump is a file or collection of files containing the content of the knowledge graph

available for download. The request in this case is for the file(s) and the response is the content of

the file(s). In order to publish dumps, first of all, concrete – and ideally standard – syntaxes are

required to serialise the graph. While for RDF graphs there are various standard syntaxes available

based on XML [172], JSON [494], custom syntaxes [422], and more besides, currently there are

only non-standard syntaxes available for property graphs [523]. Second, to reduce bandwidth,

compression methods can be applied. While standard compression such as GZIP or BZip2 can

be straightforwardly applied on any file, custom compression methods have been proposed for

graphs that not only offer better compression ratios than these standard methods, but also offer

additional functionalities, such as compact indexes for performing efficient lookups once the file is

downloaded [156]. Finally, to further reduce bandwidth, when the knowledge graph is updated,

“diffs” can be computed and published to obviate the need for agents to download all data from

scratch (see [6, 395, 529]). Still, however, dumps are only suited to certain use-cases, in particular

for agents that wish to maintain a full local copy of a knowledge graph. If an agent were rather

only interested in, for example, all food festivals in Santiago, downloading the entire dump would

require transferring and processing a lot of irrelevant data.


_9.2.2_ _Node lookups._ Protocols for performing node lookups accept a node (id) request (e.g., [cle:LP2018]
in Figure 36) and return a (sub-)graph describing that node (e.g., the document cld:LP2018). Such

a protocol is the basis for the Linked Data principles outlined previously, where node lookups

are implemented through HTTP dereferencing, which further allows nodes in remote graphs

to be referenced from across the Web. Although there are varying definitions on what content

should be returned for a node [499], a common convention is to return a sub-graph containing

either all outgoing edges for that node or all incident edges (both outgoing and incoming) for that

node [250]. Though simple, mechanisms for answering graph patterns can be implemented on

top of a node lookup interface by traversing from node to node according to the particular graph

pattern [219]; for example, to find all food festivals in Santiago – represented by the graph pattern

Food Festival type **?ff** location Santiago - we may perform a node lookup for [Santiago], subsequently
performing a node lookup for each node connected by a location edge to [Santiago], returning those


68


nodes declared to be of type [Food Festival] . However, such an approach may not be feasible if no

starting node is declared (e.g., if all nodes are variables), if the node lookup service does not return

incoming edges, etc. Furthermore, the client agent may need to request more data than necessary,

where the document returned for [Santiago] may return a lot of irrelevant data, and where nodes
with a location in [Santiago] that do not represent instances of [Food Festival] still need to be looked up to

check their type. On the plus side, node lookups are relatively inexpensive for servers to support.


_9.2.3_ _Edge patterns._ Edge patterns – also known as _triple patterns_ in the case of directed, edge
labelled graphs – are singleton graph patterns, i.e., graph patterns with a single edge. Examples

of edge patterns are **[?ff]** type Food Festival or **[?ff]** location Santiago, etc., where any term can be a

variable or a constant. A protocol for edge patterns accepts such a pattern and returns all solutions

for the pattern. Edge patterns provide more flexibility than node lookups, where graph patterns are

more readily decomposed into edge patterns than node lookups. With respect to the agent interested

in food festivals in Santiago, they can first, for example, request solutions for the edge pattern

**?ff** location Santiago and locally join/intersect these solutions with those of **[?ff]** type Food Festival .
Given that some edge patterns (e.g., **[?x]** **?y** **?z** ) can return many solutions, protocols for edge

patterns may offer additional practical features such as iteration or pagination over results [537].

Much like node lookups, the server cost of responding to a request is relatively low and easy

to predict. However, the server may often need to transfer irrelevant intermediate results to the

client, which in the previous example may involve returning nodes located in Santiago that are

not food festivals. This issue is further aggravated if the client does not have access to statistics

about the knowledge graph in order to plan how to best perform the join; for example, if there

are relatively few food festivals but many things located in Santiago, rather than intersecting the

solutions of the two aforementioned edge patterns, it should be more efficient to send a request for

each food festival to see if it is in Santiago, but deciding this requires statistics about the knowledge

graph. Extensions to the edge-pattern protocol have thus been proposed to allow for more efficient

joins [221], such as allowing batches of solutions to be sent alongside the edge pattern, returning
