<!-- Source: 02-Knowledge_Graphs.pdf | Chunk 8/15 -->


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

only solutions compatible with the solutions in the request [220] (e.g., sending a batch of solutions

for **[?ff]** type Food Festival to join with the solutions for the request **[?ff]** location Santiago ).


_9.2.4_ _(Complex) graph patterns._ Another alternative is to let client agents make requests based on

(complex) graph patterns (see Section 2.2), with the server returning (only) the final solutions. In our

running example, this involves the client issuing a request for [Food Festival] type **?ff** location Santiago

and directly receiving the relevant results. Compared with the previous protocols, this protocol is

much more efficient in terms of bandwidth: it allows clients to make more specific requests and the

server to return more specific responses. However, this reduction in bandwidth use comes at the

cost of the server having to evaluate much more complex requests, where, furthermore, the costs

of a single request are much more difficult to anticipate. While a variety of optimised engines exist

for evaluating (complex) graph patterns (e.g., [144, 354, 520] amongst many others), the problem of

evaluating such queries is known to be intractable [16]. Perhaps for this reason, public services

offering such a protocol (most often supporting SPARQL queries [217]) have been found to often

exhibit downtimes, timeouts, partial results, slow performance, etc. [75]. Even considering such

issues, however, popular services continue to receive – and successfully evaluate – millions of

requests/queries per day [336, 457], with difficult (worst-case) instances being rare in practice [62].


_9.2.5_ _Other protocols._ While Figure 37 makes explicit reference to some of the most commonly
encountered access protocols found for knowledge graphs in practice, one may of course imagine

other protocols lying almost anywhere on the spectrum from more simple to more complex inter
faces. To the right of (Complex) Graph Patterns, one could consider supporting even more complex


69


Fig. 38. Associating licenses with event data, along with permissions, actions, and obligations


requests, such as queries with entailments [191], queries that allow recursion [439], federated queries

that can join results from remote services [74], or even (hypothetically) supporting Turing-complete

requests that allow running arbitrary procedural code on a knowledge graph. As mentioned at the

outset, a server may also choose to support multiple, complementary protocols [536].


**9.3** **Usage Control**

Considering our hypothetical tourism knowledge graph, at first glance, one might assume that

the knowledge required to deliver the envisaged services is public and thus can be used both by

the tourism board and the tourists. On closer inspection, however, we may see the need for usage

control in various forms: (i) both the tourist board and its partners should associate an appropriate

license with knowledge that they contribute to the knowledge graph, such that the terms of use

are clear to all parties; (ii) a tourist might opt to install an app on their mobile phone that could be

used to recommend tourist attractions based on their location, bringing with it potential privacy

concerns; (iii) the tourist board may be required to report criminal activities to the police services

and thus may need to encrypt personal information; and (iv) the tourist board could potentially

share information relating to tourism demographics in an anonymous format to allow for improving

transport infrastructure on strategic routes. Thus in this section, we examine the state of the art in

terms of knowledge graph licensing, usage policies, encryption, and anonymisation.


_9.3.1_ _Licensing._ When it comes to associating machine readable licenses with knowledge graphs,

the W3C Open Digital Rights Language (ODRL) [261] provides an information model and related

vocabularies that can be used to specify permissions, duties, and prohibitions with respect to actions

relating to assets. ODRL supports fine-grained descriptions of digital rights that are represented as

- and thus can be embedded within – graphs. Figure 38 illustrates a license granting the assignee

the permission to [Modify], [Distribute], and [Derive] work from the [EventGraph] (e.g., Figure 1); however the

assignee is obliged to [Attribute] the copyright holder. From a modelling perspective, ODRL can be used

to model several well known license families, for instance Apache, Creative Commons (CC), and

Berkeley Software Distribution (BSD), to name but a few [80, 393]. Additionally, Cabrio et al. [80]

propose methods to automatically extract machine-readable licenses from unstructured text. From a

reasoning perspective, license compatibility validation and composition techniques [198, 360, 539]

can be used to combine knowledge graphs that are governed by different licenses. Such techniques

are employed by the the Data Licenses Clearance Center (DALICC), which includes a library of

standard machine readable licenses, and tools that enable users both to compose arbitrary custom

licenses and also to verify the compatibility of different licenses [405].


_9.3.2_ _Usage policies._ Access control policies based on edge patterns can be used to restrict access
to parts of a knowledge graph [162, 290, 435]. WebAccessControl (WAC) [31] is an access control


[31WAC, http://www.w3.org/wiki/WebAccessControl](http://www.w3.org/wiki/WebAccessControl)


70


Fig. 39. A policy for the usage of a sub-graph of location data in the knowledge graph















Fig. 40. Directed edge-labelled graph with the name of the claimant encrypted; plaintext elements are dashed
and may be omitted from published data (possibly along with encryption details)


framework for graphs that uses WebID for authentication and provides a vocabulary for specifying

access control policies. Extensions of this WAC vocabulary have been proposed to capture privacy

preferences [453] and to cater for contextual constraints [105, 538]. Although ODRL is primarily

used to specify licenses, profiles to specify access policies [498] and regulatory obligations [4, 122]

have also been proposed in recent years, as discussed in the survey by Kirrane et al. [291].

As a generalisation of access policies, usage policies specify how data can be used: what kinds of

processing can be applied, by whom, for what purpose, etc. The example usage policy presented

in Figure 39 states that the process [Analyse] of [LocationGraph] can be performed on [InternalServers] by

members of [CompanyStaff] in order to provide [EventRecommendations] . Vocabularies for usage policies have

been proposed by the SPECIAL H2020 project [56] and the W3C Data Privacy Vocabularies and

Controls Community Group (DPVCG) [59, 394]. Once specified, usage policies can then be used to

verify that data processing conforms to legal norms and the consent provided by subjects [59, 124].


_9.3.3_ _Encryption._ Rather than internally controlling usage, the tourist board could use encryption

mechanisms on parts of the published knowledge graph, for example relating to reports of crimes,

and provide keys to partners who should have access to the plaintext. While a straightforward

approach is to encrypt the entire graph (or sub-graphs) with one key, more fine-grained encryption

can be performed for individual nodes or edge-labels in a graph, potentially providing different

clients access to different information through different keys [187]. The CryptOntology [182] can

further be used to embed details about the encryption mechanism used within the knowledge

graph. Figure 40 illustrates how this could be used to encrypt the names of claimants from Figure 34,

storing the ciphertext [zhk...kjg], as well as the key-length and encryption algorithm used. In order

to grant access to the plaintext, one approach is to encrypt individual edges with symmetric keys

so as to allow specific types of edge patterns to only be executed by clients with the appropriate

key [281]. This approach can be used, for example, to allow clients who know a claimant ID (e.g.,


Claimant-XY12SDA ) and have the appropriate key to find (only) the name of the claimant through

an edge pattern [Claimant-XY12SDA] Claimant-name **?name** . A key limitation of this approach, however,

is that it requires attempting to decrypt all edges to find all possible solutions. A more efficient

alternative is to combine functional encryption and specialised indexing to retrieve solutions from

the encrypted graph without attempting to decrypt all edges [155].


71


Fig. 41. Anonymised sample of a directed edge-labelled graph describing a passenger (dashed) of a flight


_9.3.4_ _Anonymisation._ Consider that the tourist board acquires information on transport taken

by individuals within the country, which can be used to understand trajectories taken by tourists.

However, from a data-protection perspective, it would be advisable to remove any personal data

from the knowledge graph to avoid leaks of information about each individual’s travel.

A first approach to anonymisation is to suppress and generalise knowledge in a graph such that

individuals cannot be identified, based on _𝑘_ -anonymity [459] [32], _𝑙_ -diversity [316] [33], etc. Approaches

to apply _𝑘_ -anonymity on graphs identify and suppress “quasi-identifiers” that would allow a

given individual to be distinguished from fewer than _𝑘_ - 1 other individuals [230, 429]. Figure 41

illustrates a possible result of _𝑘_ -anonymisation for a sub-graph describing a flight passenger, where

quasi-identifiers (passport, plane ticket) have been converted into blank nodes, ensuring that the

passenger (the dashed blank node) cannot be distinguished from _𝑘_ - 1 other individuals. In the

context of a graph, however, _neighbourhood attacks_ [581] – using information about neighbours –

can also break _𝑘_ -anonymity, where we also suppress the day and time of the flight, which, though

not sensitive information per se, could otherwise break _𝑘_ -anonymity for passengers (if, for example,

a particular flight had fewer than _𝑘_ males from the U.S. onboard).

More complex neighbourhood attacks may rely on more abstract graph patterns, observing that

individuals can be deanonymised purely from knowledge of the graph structure, even if all nodes

and edge labels are left blank; for example, if we know that a team of _𝑘_ - 1 players take flights

together for a particular number of away games, we could use this information for a neighbourhood

attack that reveals the set of players in the graph. Hence a number of guarantees specific to graphs

have been proposed, including _𝑘_ -degree anonymity [321], which ensures that individuals cannot be

deanonymised by attackers with knowledge of the degree of particular individuals. The approach is

based on minimally modifying the graph to ensure that each node has at least _𝑘_ - 1 other nodes with

the same degree. A stronger guarantee, called _𝑘_ -isomorphic neighbour anonymity [580], avoids

neighbourhood attacks where an attacker knows how an individual is connected to nodes in their

neighbourhood; this is done by modifying the graph to ensure that for each node, there exist at

least _𝑘_ - 1 nodes with isomorphic (i.e., identically structured) neighbourhoods elsewhere in the

graph. Both approaches only protect against attackers with knowledge of bounded neighbourhoods.

An even stronger notion is that of _𝑘_ -automorphism [584], which ensures that for every node, it is

structurally indistinguishable from _𝑘_ - 1 other nodes, thus avoiding any attack based on structural

information (as a trivial example, a _𝑘_ -clique or a _𝑘_ -cycle satisfy _𝑘_ -automorphism). Many of these

techniques for anonymisation of graph data were originally motivated by social networks [371],

though they can also be applied to knowledge graphs, per the work of Lin and Tripunitara [319],

who adapt _𝑘_ -automorphism for directed edge-labelled graphs (specifically RDF graphs).

While the aforementioned approaches anonymise data, a second approach is to apply anonymi
sation when answering queries, such as adding noise to the solutions in a way that preserves


32 _𝑘_ -anonymity guarantees that the data of an individual is indistinguishable from at least _𝑘_ - 1 other individuals.
33 _𝑙_ -diversity guarantees that sensitive data fields have at least _𝑙_ diverse values within each group of individuals; this avoids

leaks such as that all tourists from Austria (a group of individuals) in the data have been pick-pocketed (a sensitive attribute).


72


privacy. One approach is to apply _𝜀_ -differential privacy [137] [34] for querying graphs [483]. Such

mechanisms are typically used for aggregate (e.g., count) queries, where noise is added to avoid

leaks about individuals. To illustrate, differential privacy may allow for counting the number of

passengers of specified nationalities taking specified flights, adding (just enough) random noise to

the count to ensure that we cannot tell, within a certain probability (controlled by _𝜀_ ), whether or

not a particular individual took a flight, where we would require (proportionally) less noise for

common nationalities, but more noise to “hide” individuals from more uncommon nationalities.

These approaches require information loss for stronger guarantees of privacy; which to choose

is thus heavily application dependent. If the anonymised data are to be published in their entirety

as a “dump”, then an approach based on _𝑘_ -anonymity can be used to protect individuals, while

_𝑙_ -diversity can be used to protect groups. On the other hand, if the data are to be made available, in

part, through a query interface, then _𝜀_ -differential privacy is a more suitable framework.


**10** **KNOWLEDGE GRAPHS IN PRACTICE**

In this section, we discuss some of the most prominent knowledge graphs that have emerged in

the past years. We begin by discussing open knowledge graphs, which have been published on the

Web per the guidelines and protocols described in Section 9. We later discuss enterprise knowledge

graphs that have been created by companies for a diverse range of applications.


**10.1** **Open Knowledge Graphs**

By _open knowledge graphs_, we specifically refer to knowledge graphs published under the Open

Data philosophy, namely that “ _open means anyone can freely access, use, modify, and share for any_

_purpose (subject, at most, to requirements that preserve provenance and openness)_ ”. [35] Many open

knowledge graphs have been published in the form of _Linked Open Datasets_ [226], which are

(RDF) graphs published under the Linked Data principles (see Section 9.1.2) following the Open

Data philosophy. Many of the most prominent open knowledge graphs – including DBpedia [311],

YAGO [506], Freebase [54], and Wikidata [543] – cover multiple domains, representing a broad

diversity of entities and relationships; we first discuss these in turn. Later we discuss some of the

other (specific) domains for which open knowledge graphs are currently available. Most of the

open knowledge graphs we discuss in this section are modelled in RDF, published following Linked

Data principles, and offer access to their data through dumps (RDF), node lookups (Linked Data),

graph patterns (SPARQL) and, in some cases, edge patterns (Triple Pattern Fragments).


_10.1.1_ _DBpedia._ The DBpedia project was developed to extract a graph-structured representation

of the semi-structured data embedded in Wikipedia articles [22], enabling the integration, pro
cessing, and querying of these data in a unified manner. The resulting knowledge graph is further

enriched by linking to external open resources, including images, webpages, and external datasets

such as DailyMed, DrugBank, GeoNames, MusicBrainz, New York Times, and WordNet [311]. The

DBpedia extraction framework consists of several components, corresponding to abstractions of

Wikipedia article sources, graph storage and serialisation destinations, wiki-markup extractors,

parsers, and extraction managers [48]. Specific extractors are designed to process labels, abstracts,

interlanguage links, images, redirects, disambiguation pages, external links, internal pagelinks,

homepages, categories, and geocoordinates. The content in the DBpedia knowledge graph is not

only multidomain, but also multilingual: as of 2012, DBpedia contained labels and abstracts in up to

97 different languages [348]. Entities within DBpedia are classified using four different schemata in


34 _𝜀_ -differential privacy ensures that the probability of achieving a given result from some process (e.g., query) applied to

data, to which random noise is added, differs no more than _𝑒_ _[𝜀]_ when the data includes or excludes any individual.

[35See http://opendefinition.org/](http://opendefinition.org/)


73


order to address varying application requirements [48]. These schemata include a Simple Knowledge

Organization System (SKOS) representation of Wikipedia categories, a Yet Another Great Ontology

(YAGO) classification schema (discussed in the following), an Upper Mapping and Binding Exchange

Layer (UMBEL) ontology categorisation schema, and a custom schema called the DBpedia ontology

with classes such as Person, Place, Organisation, and Work [311]. DBpedia also supports live

synchronisation in order to remain consistent with dynamic Wikipedia articles [311].


_10.1.2_ _Yet Another Great Ontology._ YAGO likewise extracts graph-structured data from Wikipedia,

which are then unified with the hierarchical structure of WordNet to create a “ _light-weight and_

_extensible ontology with high quality and coverage_ ” [506]. This knowledge graph aims to be applied

for various information technology tasks, such as machine translation, word sense disambiguation,

query expansion, document classification, data cleaning, information integration, etc. While earlier

approaches automatically extracted structured knowledge from text using pattern matching, natural

language processing (NLP), and statistical learning, the resulting content tended to lack in quality

when compared with what was possible through manual construction [506]. However, manual

construction is costly, making it challenging to achieve broad coverage and keep the data up-to-date.

In order to extract data with high coverage and quality, YAGO (like DBpedia) mostly extracts data

from Wikipedia infoboxes and category pages, which contain basic entity information and lists of

articles for a specific category, respectively; these, in turn, are unified with hierarchical concepts

from WordNet [507]. A schema – called the YAGO model – provides a vocabulary defined in RDFS;

this model allows for representing words as entities, capturing synonymy and ambiguity [506]. The

model further supports reification, _𝑛_ -ary relations, and data types [507]. Refinement mechanisms

employed within YAGO include canonicalisation, where each edge and node is mapped to a unique

identifier and duplicate elements are removed, and type checking, where nodes that cannot be

assigned to a class by deductive or inductive methods are eliminated [507]. YAGO would be extended

in later years to support spatio-temporal context [243] and multilingual Wikipedias [333].


_10.1.3_ _Freebase._ Freebase was a general collection of human knowledge that aimed to address

some of the large scale information integration problems associated with the decentralised nature

of the Semantic Web, such as uneven adoption, implementation challenges, and distributed query

performance limitations [55]. Unlike DBpedia and YAGO – which are mostly extracted from

Wikipedia/WordNet – Freebase solicited contributions directly from human editors. Included in

the Freebase platform were a scalable data store with versioning mechanisms; a large data object

store (LOB) for the storage of text, image, and media files; an API that could be queried using

the Metaweb Query Language (MQL); a Web user interface; and a lightweight typing system [55].

The latter typing system was designed to support collaborative processes. Rather than forcing

ontological correctness or logical consistency, the system was implemented as a loose collection of

structuring mechanisms – based on datatypes, semantic classes, properties, schema definitions,

etc. – that allowed for incompatible types and properties to coexist simultaneously [55]. Content

could be added to Freebase interactively through the Web user interface or in an automated way

by leveraging the API’s write functionality. Freebase had been acquired by Google in 2010, where

the content of Freebase formed an important part of the Google Knowledge Graph announced in

2012 [484]. When Freebase became read-only as of March 2015, the knowledge graph contained

over three billion edges. Much of this content was subsequently migrated to Wikidata [407].


_10.1.4_ _Wikidata._ As exploited by DBpedia and YAGO, Wikipedia contains a wealth of semi
structured data embedded in info-boxes, lists, tables, etc. However, these data have traditionally been

curated and updated manually across different articles and languages; for example, a goal scored by

a Chilean football player may require manual updates in the player’s article, the tournament article,


74


the team article, lists of top scorers, and so forth, across hundreds of language versions. Manual

curation has led to a variety of data quality issues, including contradictory data in different articles,

languages, etc. The Wikimedia Foundation thus uses Wikidata as a centralised, collaboratively
edited knowledge graph to supply Wikipedia – and arbitrary other clients – with data. Under

this vision, a fact could be added to Wikidata once, triggering the automatic update of potentially

multitudinous articles in Wikipedia across different languages [543]. Like Wikipedia, Wikidata is

also considered a secondary source containing _claims_ that should reference primary sources, though

claims can also be initially added without reference [415]. Wikidata further allows for different

viewpoints in terms of potentially contradictory (referenced) claims [543]. Wikidata is multilingual,

where nodes and edges are assigned language-agnostic Qxx and Pxx codes (see Figure 36) and are

subsequently associated with labels, aliases, and descriptions in various languages [277], allowing

claims to be surfaced in these languages. Collaborative editing is not only permitted on the data level,

but also on the schema level, allowing users to add or modify lightweight semantic axioms [416] –

including sub-classes, sub-properties, inverse properties, etc. – as well as shapes [60]. Wikidata

offers various access protocols [336] and has received broad adoption, being used by Wikipedia to

generate infoboxes in certain domains [456], being supported by Google [407], and having been

used as a data source for prominent applications such as Apple’s Siri, amongst others [336].


_10.1.5_ _Other open cross-domain knowledge graphs._ A number of other cross-domain knowledge

graphs have been developed down through the years. BabelNet [373] – in a similar fashion to

YAGO – is based on unifying WordNet and Wikipedia, but with the integration of additional

knowledge graphs such as Wikidata, and a focus on creating a knowledge graph of multilingual

lexical forms (organised into multilingual synsets) by transforming lexicographic resources such

as Wiktionary and OmegaWiki into knowledge graphs. Compared to other knowledge graphs,

lexicalised knowledge graphs such as BabelNet bring together the encyclopedic information found

in Wikipedia with the lexicographic information usually found in monolingual and bilingual

dictionaries. The Cyc project [314] aims to encode common-sense knowledge in a machine-readable

way, where over 900 person-years of effort [340] have, since 1986, gone into the creation of 2.2

million facts and rules. Though Cyc is proprietary, an open subset called OpenCyc has been

published, where we refer to the comparison by Färber et al. [153] of DBpedia, Freebase, OpenCyc,

and YAGO for further details. The Never Ending Language Learning (NELL) project [357] has, since

2010, extracted a graph of 120 million edges from the text of web pages using OIE methods (see

Section 6). Each such open knowledge graph applies different combinations of the languages and

techniques discussed in this paper over different sources with differing results.


_10.1.6_ _Domain-specific open knowledge graphs._ Open knowledge graphs have been published in a

variety of specific domains. Schmachtenberg et al. [463] identify the most prominent domains in

the context of Linked Data as follows: _media_, relating to news, television, radio, etc. (e.g., the BBC

World Service Archive [431]); _government_, relating to the publication of data for transparency and

development (e.g., by the U.S. [233] and U.K. [475] governments); _publications_, relating to academic

literature in various disciplines (e.g., OpenCitations [410], SciGraph [260], Microsoft Academic

Knowledge Graph [152]); _geographic_, relating to places and regions of interest (e.g., LinkedGeo
Data [497]); _life sciences_, relating to proteins, genes, drugs, diseases, etc. (e.g., Bio2RDF [82]); and

_user-generated content_, relating to reviews, open source projects, etc. (e.g., Revyu [227]). Open

knowledge graphs have also been published in other domains, including _cultural heritage_ [259], _mu-_

_sic_ [432], _law_ [359], _theology_ [476], and even _tourism_ [13, 279, 328, 577]. The envisaged applications

for such knowledge graphs are as varied as the domains from which they emanate, but often relate

to integration [82, 432], recommendation [328, 432], transparency [233, 475], archiving [259, 431],

decentralisation [227], multilingual support [476], regulatory compliance [359], etc.


75


**10.2** **Enterprise Knowledge Graphs**


A variety of companies have announced the creation of proprietary “enterprise knowledge graphs”

with a variety of goals in mind, which include: improving search capabilities [87, 214, 298, 482, 484],

providing user recommendations [87, 214], implementing conversational/personal agents [417],

enhancing targetted advertising [224], empowering business analytics [224], connecting users [224,

387], extending multilingual support [224], facilitating research and discovery [37], assessing and

mitigating risk [112, 522], tracking news events [347], and increasing transport automation [234],

amongst (many) others. Though highly diverse, these enterprise knowledge graphs do follow some

high-level trends, as reflected in the discussion by Noy et al. [387]: (1) data are typically integrated

into the knowledge graph from a variety of both external and internal sources (often involving

text); (2) the enterprise knowledge graph is often very large, with millions or even billions of nodes

and edges, posing challenges in terms of scalability; (3) refinement of the initial knowledge graph

- adding new links, consolidating duplicate entities, etc. – is important to improve quality; (4)

techniques to keep the knowledge graph up-to-date with the domain are often crucial; (5) a mix of

ontological and machine learning representations are often combined or used in different situations

in order to draw conclusions from the enterprise knowledge graph; (6) the ontologies used tend to

be lightweight, often simple taxonomies representing a hierarchy of classes or concepts.

We now discuss the main industries in which enterprise knowledge graphs have been deployed.


_10.2.1_ _Web search._ Web search engines have traditionally focused on matching a query string

with sub-strings in web documents. The Google Knowledge Graph [387, 484] rather promoted a

paradigm of “ _things not strings_ ” – analogous to semantic search [206] – where the search engine

would now try to identify the entities that a particular search may be expressing interest in. The

knowledge graph itself describes these entities and how they interrelate. One of the main user
facing applications of the Google Knowledge Graph is the “Knowledge Panel”, which presents a

pane on the right-hand side of (some) search results describing the principal entity that the search

appears to be seeking, including some images, attribute–value pairs, and a list of related entities

that users also search for. The Google Knowledge Graph was key to popularising the modern usage

of the phrase “knowledge graph” (see Appendix A). Other major search engines, such as Microsoft

Bing [36] [482], would later announce knowledge graphs along similar lines.


_10.2.2_ _Commerce._ Enterprise knowledge graphs have also been announced by companies that are

principally concerned with selling or renting goods and services. A prominent example of such

a knowledge graph is that used by Amazon [132, 298], which describes the products on sale in

their online marketplace. One of the main stated goals of this knowledge graph is to enable more

advanced (semantic) search features for products, as well as to improve product recommendations

to users of its online marketplace. Another knowledge graph for commerce was announced by

eBay [417], which encodes product descriptions and shopping behaviour patterns, and is used to

power conversational agents that aid users to find relevant products through a natural language

interface. Airbnb [87] have also described a knowledge graph that encodes accommodation for rent,

places, events, experiences, neighbourhoods, users, tags, etc., on top of which a taxonomic schema

is defined. This knowledge graph is used to offer potential clients recommendations of attractions,

events, and activities available in the neighbourhood of a particular home for rent. Uber [214]

have similarly announced a knowledge graph focused on food and restaurants for their “Uber Eats”

delivery service. The goals are again to offer semantic search features and recommendations to

users who are uncertain precisely what kind of food they are looking for.


36Microsoft’s Knowledge Graph was previously called “Satori” (meaning _understanding_ in Japanese).


76


_10.2.3_ _Social networks._ Enterprise knowledge graphs have also emerged in the context of social

networking services. Facebook [387] have gathered together a knowledge graph describing not

only social data about users, but also the entities they are interested in, including celebrities,

places, movies, music, etc., in order to connect people, understand their interests, and provide

recommendations. LinkedIn [224] announced a knowledge graph containing users, jobs, skills,

companies, places, schools, etc., on top of which a taxonomic schema is defined. The knowledge

graph is used to provide multilingual translations of important concepts, to improve targetted

advertising, to provide advanced features for job search and people search, and likewise to provide

recommendations matching jobs to people (and vice versa). Another knowledge graph has been

created by Pinterest [195], describing users and their interests, the latter being organised into a

taxonomy. The main use-cases for the knowledge graph are to aid users to more easily find content

of interest to them, as well as to enhance revenue through targetted advertisements.


_10.2.4_ _Finance._ The financial sector has also seen deployment of enterprise knowledge graphs.

Amongst these, Bloomberg [347] has proposed a knowledge graph that powers financial data

analytics, including sentiment analysis for companies based on current news reports and tweets,

a question answering service, as well as detecting emerging events that may affect stock values.

Thompson Reuters (Refinitiv) [522] have likewise announced a knowledge graph encoding “the

financial ecosystem” of people, organisations, equity instruments, industry classifications, joint

ventures and alliances, supply chains, etc., using a taxonomic schema to organise these entities.

Some of the applications they mention for the knowledge graph include supply chain monitoring,

risk assessment, and investment research. Knowledge graphs have also been used for deductive

reasoning, with Banca d’Italia [35] using rule-based reasoning to determine, for example, the

percentage of ownership of a company by various stakeholders. Other companies exploring financial

knowledge graphs include Accenture [390], Capital One [69], Wells Fargo [377], amongst others.


_10.2.5_ _Other industries._ Enterprises have also been actively developing knowledge graphs to

enable novel applications in a variety of other industries, including: _health-care_, where IBM are

exploring use-cases for drug discovery [387] and information extraction from package inserts [179],

while AstraZeneca [37] are using a knowledge graph to advance genomics research and disease

understanding; _transport_, where Bosch are exploring a knowledge graph of scenes and locations

for driving automation [234]; _oil & gas_, where Maana [112] are using knowledge graphs to perform

data integration for risk mitigation regarding oil wells and drilling; and more besides.


**11** **SUMMARY AND CONCLUSION**


We have provided a comprehensive introduction to knowledge graphs, which have been receiving

more and more attention in recent years. Under the definition of a knowledge graph as _a graph of_

_data intended to accumulate and convey knowledge of the real world, whose nodes represent entities_

_of interest and whose edges represent relations between these entities_, we have discussed models by

which data can be structured as graphs; representations of schema, identity and context; techniques

for leveraging deductive and inductive knowledge; methods for the creation, enrichment, quality

assessment and refinement of knowledge graphs; principles and standards for publishing knowledge

graphs; and finally, the adoption of knowledge graphs in the real world.


_Future directions._ Research on knowledge graphs can become a confluence of techniques arising

from different areas with the common objective of maximising the knowledge – and thus value –

that can be distilled from diverse sources at large scale using a graph-based data abstraction [246].

Pursuing this objective will benefit from expertise on graph databases, knowledge representation,


77


logic, machine learning, graph algorithms and theory, ontology engineering, data quality, natural

language processing, information extraction, privacy and security, and more besides.

While advances in these individual disciplines are sure to continue and to generate further impact,

particularly interesting topics arise also from their intersections. In the intersection of data graphs

and deductive knowledge, we emphasise emerging topics such as _formal semantics for property_

_graphs_, with languages that can take into account the meaning of labels and property–value pairs

on nodes and edges [302]; and _reasoning and querying over contextual data_, in order to derive

conclusions and results valid in a particular setting [252, 467, 583]. In the intersection of data

graphs and inductive knowledge, we highlight topics such as _similarity-based query relaxation_,

allowing to find approximate answers to exact queries based on numerical representations (e.g.,

embeddings) [548]; _shape induction_, in order to extract and formalise inherent patterns in the

knowledge graph as constraints [350]; and _contextual knowledge graph embeddings_ that provide

numeric representations of nodes and edges that vary with time, place, etc. [282]. Finally, in the

intersection of deductive and inductive knowledge, we mention the topics of _entailment-aware_

_knowledge graph embeddings_ [125, 207], that incorporate rules and/or ontologies when computing

plausibility; _expressive graph neural networks_ proven capable of complex classification analogous to

expressive ontology languages [32]; as well as further advances on _rule and axiom mining_, allowing

to extract symbolic, deductive representations from the knowledge graphs [73, 169].

Aside from specific topics, more general challenges for knowledge graphs include _scalability_,

particularly for deductive and inductive reasoning; _quality_, not only in terms of data, but also the

models induced from knowledge graphs; _diversity_, such as managing contextual or multi-modal

data; _dynamicity_, considering temporal or streaming data; and finally _usability_, which is key to

increasing adoption. Though techniques are continuously being proposed to address precisely these

challenges, they are unlikely to ever be completely “solved”; rather they serve as dimensions along

which knowledge graphs, and their techniques, tools, etc., will continue to mature.

Given the availability of open knowledge graphs whose quality continue to improve, as well

as the growing adoption of enterprise knowledge graphs in various industries, future research on

knowledge graphs has the potential to foster key advancements in broad aspects of society. Here

we have highlighted just some examples of future research directions of importance to this pursuit.


_Acknowledgements:_ We thank the attendees of the Dagstuhl Seminar on “Knowledge Graphs”

for discussions that inspired and influenced this paper, and all those that make such seminars

possible. We would also like to thank Matteo Palmonari for feedback on Figures 3 and 4, as well as

Stefan Decker and Carlos Bobed who provided suggestions for the paper. Hogan was supported by

Fondecyt Grant No. 1181896. Hogan and Gutierrez were funded by ANID – Millennium Science

Initiative Program – Code ICN17_002. Cochez did part of the work while employed at Fraunhofer

FIT, Germany and was later partially funded by Elsevier’s Discovery Lab. Kirrane, Ngonga Ngomo,

Polleres and Staab received funding through the project “KnowGraphs” from the European Union’s

Horizon programme under the Marie Skłodowska-Curie grant agreement No. 860801. Kirrane and

Polleres were supported by the European Union’s Horizon 2020 research and innovation programme

under grant 731601. Labra was supported by the Spanish Ministry of Economy and Competitiveness

(Society challenges: TIN2017-88877-R). Navigli was supported by the MOUSSE ERC Grant No.

726487 under the European Union’s Horizon 2020 research and innovation programme. Rashid was

supported by IBM Research AI through the AI Horizons Network. Schmelzeisen was supported by

the German Research Foundation (DFG) grant STA 572/18-1.


78


**REFERENCES**


[1] 2019. _7th International Conference on Learning Representations, ICLR 2019, New Orleans, LA, USA, May 6-9, 2019_ .

[OpenReview.net. https://openreview.net/group?id=ICLR.cc/2019/conference](https://openreview.net/group?id=ICLR.cc/2019/conference)

[2] Karl Aberer, Key-Sun Choi, Natasha Fridman Noy, Dean Allemang, Kyung-Il Lee, Lyndon J. B. Nixon, Jennifer Golbeck,

Peter Mika, Diana Maynard, Riichiro Mizoguchi, Guus Schreiber, and Philippe Cudré-Mauroux (Eds.). 2007. _The_

_Semantic Web, 6th International Semantic Web Conference, 2nd Asian Semantic Web Conference, ISWC 2007 + ASWC_

_2007, Busan, Korea, November 11-15, 2007_ . Lecture Notes in Computer Science, Vol. 4825. Springer.

[3] Serge Abiteboul. 1997. Querying Semi-Structured Data. In _Database Theory - ICDT ’97, 6th International Conference,_

_Delphi, Greece, January 8-10, 1997, Proceedings (Lecture Notes in Computer Science)_, Foto N. Afrati and Phokion G.

[Kolaitis (Eds.), Vol. 1186. Springer, 1–18. https://doi.org/10.1007/3-540-62222-5_33](https://doi.org/10.1007/3-540-62222-5_33)

[4] Sushant Agarwal, Simon Steyskal, Franjo Antunovic, and Sabrina Kirrane. 2018. Legislative Compliance Assessment:

Framework, Model and GDPR Instantiation. In _Privacy Technologies and Policy - 6th Annual Privacy Forum, APF 2018,_

_Barcelona, Spain, June 13-14, 2018, Revised Selected Papers (Lecture Notes in Computer Science)_, Manel Medina, Andreas
