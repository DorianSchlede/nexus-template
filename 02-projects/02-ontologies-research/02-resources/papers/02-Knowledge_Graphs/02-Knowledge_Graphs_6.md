<!-- Source: 02-Knowledge_Graphs.pdf | Chunk 6/15 -->

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

to count how many nodes have incoming flights from a domestic airport (there are 3), and how

many nodes have incoming flights from a domestic airport _and_ are international airports (there is

1), where the greater the difference between both counts, the weaker the evidence for the axiom.


**6** **CREATION AND ENRICHMENT**

In this section, we discuss the principal techniques by which knowledge graphs can be created

and subsequently enriched from diverse sources of legacy data that may range from plain text

to structured formats (and anything in between). The appropriate methodology to follow when

creating a knowledge graph depends on the actors involved, the domain, the envisaged applications,

the available data sources, etc. Generally speaking, however, the flexibility of knowledge graphs

lends itself to starting with an initial core that can be incrementally enriched from other sources

as required (typically following an Agile [256] or “pay-as-you-go” [473] methodology). For our

running example, we assume that the tourism board decides to build a knowledge graph from

scratch, aiming to initially describe the main tourist attractions – places, events, etc. – in Chile in

order to help visiting tourists identify those that most interest them. The board decides to postpone

adding further data, like transport routes, reports of crime, etc., for a later date.


**6.1** **Human Collaboration**


One approach for creating and enriching knowledge graphs is to solicit direct contributions from

human editors. Such editors may be found in-house (e.g., employees of the tourist board), using

crowd-sourcing platforms, through feedback mechanisms (e.g., tourists adding comments on

attractions), through collaborative-editing platforms (e.g., an attractions wiki open to public edits),

etc. Though human involvement incurs high costs [401], some prominent knowledge graphs have

been primarily based on direct contributions from human editors [224, 543]. Depending on how the

contributions are solicited, however, the approach has a number of key drawbacks, due primarily

to human error [407], disagreement [571], bias [270], vandalism [228], etc. Successful collaborative

creation further raises challenges concerning licensing, tooling, and culture [407]. Humans are

sometimes rather employed to verify and curate additions to a knowledge graph extracted by other

means [407] (through, e.g., video games with a purpose [275]), to define high-quality mappings

from other sources [118], to define appropriate high-level schema [284, 306], and so forth.


50


**6.2** **Text Sources**

Text corpora – such as sourced from newspapers, books, scientific articles, social media, emails,

web crawls, etc. – are an abundant source of rich information [231, 447]. However, extracting such

information with high precision and recall for the purposes of creating or enriching a knowledge

graph is a non-trivial challenge. To address this, techniques from Natural Language Processing

(NLP) [274, 343] and Information Extraction (IE) [199, 338, 554] can be applied. Though processes

vary considerably across text extraction frameworks, in Figure 31 we illustrate four core tasks for

text extraction on a sample sentence. We will discuss these tasks in turn.


_6.2.1_ _Pre-processing._ The pre-processing task may involve applying various techniques to the input

text, where Figure 31 illustrates _Tokenisation_, which parses the text into atomic terms and symbols.

Other pre-processing tasks applied to a text corpus may include: _Part-of-Speech_ ( _POS_ ) _tagging_ [274,

343] to identify terms representing verbs, nouns, adjectives, etc.; _Dependency Parsing_, which extracts

a grammatical tree structure for a sentence where leaf nodes indicate individual words that together

form phrases (e.g., noun phrases, verb phrases) and eventually clauses and sentences [274, 343];

and _Word Sense Disambiguation_ ( _WSD_ ) [372] to identify the meaning (aka _sense_ ) in which a word is

used, linking words with a lexicon of senses (e.g., WordNet [353] or BabelNet [373]), where, for

instance, the term [flights] may be linked with the WordNet sense “an instance of travelling by air”
rather than “a stairway between one floor and the next’. The appropriate type of pre-processing to

apply often depends on the requirements of later tasks in the pipeline.


_6.2.2_ _Named Entity Recognition (NER)._ The NER task identifies mentions of named entities in a

text [369, 434], typically targetting mentions of people, organisations, locations, and potentially

other types [320, 370, 573]. A variety of NER techniques exist, with many modern approaches

based on learning frameworks that leverage lexical features (e.g., POS tags, dependency parse trees,

etc.) and gazetteers (e.g., lists of common first names, last names, countries, prominent businesses,

etc.). Supervised methods [46, 160, 307] require manually labelling all entity mentions in a training

corpus, whereas _bootstrapping_ -based approaches [98, 148, 209, 370] rather require a small set of

_seed examples_ of entity mentions from which patterns can be learnt and applied to unlabelled text.

_Distant supervision_ [320, 437, 573] uses known entities in a knowledge graph as seed examples

through which similar entities can be detected. Aside from learning-based frameworks, manually
crafted rules [88, 293] are still sometimes used due to their more controllable and predictable

behaviour [89]. The named entities identified by NER may be used to generate new candidate nodes

for the knowledge graph (known as _emerging entities_, shown dashed in Figure 31), or may be linked

to existing nodes per the Entity Linking task described in the following.


_6.2.3_ _Entity Linking (EL)._ The EL task associates mentions of entities in a text with the existing

nodes of a target knowledge graph, which may be the nucleus of a knowledge graph under creation,

or an external knowledge graph [558]. In Figure 31, we assume that the nodes [Santiago] and [Easter Island]

already exist in the knowledge graph (possibly extracted from other sources). EL may then link

the given mentions to these nodes. The EL task presents two main challenges. First, there may be

multiple ways to mention the same entity, as in the case of [Rapa Nui] and [Easter Island] ; if we created

a node [Rapa Nui] to represent that mention, we would split the information available under both

mentions across different nodes, where it is thus important for the target knowledge graph to capture

the various aliases and multilingual labels by which one can refer to an entity [362]. Secondly,

the same mention in different contexts can refer to distinct entities; for instance, [Santiago] can refer

to cities in Chile, Cuba, Spain, among others. The EL task thus considers a _disambiguation phase_

wherein mentions are associated to candidate nodes in the knowledge graph, the candidates are

ranked, and the most likely node being mentioned is chosen [558]. Context can be used in this phase;


51


for example, if [Easter Island] is a likely candidate for the corresponding mention alongside [Santiago],

we may boost the probability that this mention refers to the Chilean capital as both candidates

are located in Chile. Other heuristics for disambiguation consider a prior probability, where for

example, [Santiago] most often refers to the Chilean capital (being, e.g., the largest city with that

name); centrality measures on the knowledge graph can be used for such purposes [558].


_6.2.4_ _Relation Extraction (RE)._ The RE task extracts relations between entities in the text [24,

582]. The simplest case is that of extracting binary relations in a _closed setting_ wherein a fixed

set of relation types are considered. While traditional approaches often used manually-crafted

patterns [225], modern approaches rather tend to use learning-based frameworks [446], including

supervised methods over manually-labelled examples [77, 582]. Other learning-based approaches

again use bootstrapping [78, 148] and distant supervision [244, 356, 440, 487, 512, 566] to forgo

the need for manual labelling; the former requires a subset of manually-labelled seed examples,

while the latter finds sentences in a large corpus of text mentioning pairs of entities with a known

relation/edge, which are used to learn patterns for that relation. Binary RE can also be applied

using unsupervised methods in an open setting – often referred to as _Open Information Extraction_

( _OIE_ ) [31, 149, 150, 341, 342, 357] – whereby the set of target relations is not pre-defined but rather

extracted from text based on, for example, dependency parse trees from which relations are taken.

A variety of RE methods have been proposed to extract _𝑛_ -ary relations that capture further

context for how entities are related. In Figure 31, we see how an _𝑛_ -ary relation captures additional

temporal context, denoting when Rapa Nui was named a World Heritage site; in this case, an

anonymous node is created to represent the higher-arity relation in the directed-labelled graph.

Various methods for _𝑛_ -ary RE are based on _frame semantics_ [159], which, for a given verb (e.g.,

“ _named_ ”), captures the entities involved and how they may be interrelated. Resources such as

FrameNet [26] then define frames for words, such as to identify that the semantic frame for “ _named_ ”

includes a _speaker_ (the person naming something), an _entity_ (the thing named) and a _name_ . Optional

frame elements are an _explanation_, a _purpose_, a _place_, a _time_, etc., that may add context to the

relation. Other RE methods are rather based on _Discourse Representation Theory_ ( _DRT_ ) [278], which

considers a logical representation of text based on existential events. Under this theory, for example,

the naming of Easter Island as a World Heritage Site is considered to be an (existential) event where

Easter Island is the _patient_ (the entity affected), leading to the logical (neo-Davidsonian) formula:


∃ _𝑒_ : [�] naming( _𝑒_ ) _,_ patient( _𝑒,_ [Easter Island] ) _,_ name( _𝑒,_ [World Heritage Site] ) [�]


Such a formula is analogous to the idea of reification, as discussed previously in Section 3.3.

Finally, while relations extracted in a closed setting are typically mapped directly to a knowledge

graph, relations that are extracted in an open setting may need to be aligned with the knowledge

graph; for example, if an OIE process extracts a binary relation [Santiago] has flights to Easter Island,
it may be the case that the knowledge graph does not have other edges labelled has flights to,
where alignment may rather map such a relation to the edge [Santiago] flight Easter Island assuming
flight is used in the knowledge graph. A variety of methods have been applied for such purposes,

including mappings [102, 175] and rules [448] for aligning _𝑛_ -ary relations; distributional and

dependency-based similarities [361], association rule mining [135], Markov clustering [136] and

linguistic techniques [339] for aligning OIE relations; amongst others.


_6.2.5_ _Joint tasks._ Having presented the four main tasks for building knowledge graphs from text,

it is important to note that frameworks do not always follow this particular sequence of tasks.

A common trend, for example, is to combine interdependent tasks, jointly performing WSD and

EL [362], or NER and EL [330, 382], or NER and RE [438, 579], etc., in order to mutually improve


52


<html>

<head><title>UNESCO World Heritage Sites</title></head>
<body>

<h1>World Heritage Sites</h1>
<h2>Chile</h2>
<p>Chile has 6 UNESCO World Heritage Sites.</p>
<table border="1">

<tr><th>Place</th><th>Year</th><th>Criteria</th></tr>
<tr><td>Rapa Nui</td><td>1995</td>

<td rowspan="6">Cultural</td></tr>
<tr><td>Churches of Chiloé</td><td>2000</td></tr>
<tr><td>Historical Valparaíso</td><td>2003</td></tr>
<tr><td>Saltpeter Works</td><td>2005</td></tr>
<tr><td>Sewell Mining Town</td><td>2006</td></tr>
<tr><td>Qhapaq Ñan</td><td>2014</td></tr>
</table>
</body>
</html>




- UNESCO World Heritage Sites ×


**World Heritage Sites**
**Chile**

Chile has 6 UNESCO World Heritage Sites.






|Place|Year|Criteria|
|---|---|---|
|Rapa Nui|1995|Cultural|
|Churches of Chiloé|2000|2000|
|Historical Valparaíso|2003|2003|
|Saltpeter Works|2005|2005|
|Sewell Mining Town|2006|2006|
|Qhapaq Ñan|2014|2014|



Fig. 32. Example markup document (HTML) with source-code (left) and formatted document (right)


the performance of multiple tasks. For further details on extracting knowledge from text we refer

to the book by Maynard et al. [343] and the recent survey by Martínez-Rodríguez et al. [338].


**6.3** **Markup Sources**

The Web was founded on interlinking _markup documents_ wherein markers (aka _tags_ ) are used

to separate elements of the document (typically for formatting purposes). Most documents on

the Web use the HyperText Markup Language (HTML). Figure 32 presents an example HTML

webpage about World Heritage Sites in Chile. Other formats of markup include Wikitext used

by Wikipedia, TeX for typesetting, Markdown used by Content Management Systems, etc. One

approach for extracting information from markup documents – in order to create and/or enrich a

knowledge graph – is to strip the markers (e.g., HTML tags), leaving only plain text upon which the

techniques from the previous section can be applied. However, markup can be useful for extraction

purposes, where variations of the aforementioned tasks for text extraction have been adapted to

exploit such markup [324, 327, 338]. We can divide extraction techniques for markup documents

into three main categories: general approaches that work independently of the markup used in

a particular format, often based on _wrappers_ that map elements of the document to the output;

focussed approaches that target specific forms of markup in a document, most typically _web tables_

(but sometimes also lists, links, etc.); and form-based approaches that extract the data underlying a

webpage, per the notion of the _Deep Web_ . These approaches can often benefit from the regularities

shared by webpages of a given website, be it due to informal conventions on how information is

published across webpages, or due to the re-use of templates to automatically generate content

across webpages; for example, intuitively speaking, while the webpage of Figure 32 is about Chile,

we will likely find pages for other countries following the same structure on the same website.


_6.3.1_ _Wrapper-based extraction._ Many general approaches are based on _wrappers_ that locate and

extract the useful information directly from the markup document. While the traditional approach

was to define such wrappers manually – a task for which a variety of declarative languages and

tools have been defined – such approaches are brittle to changes in a website’s layout [158]. Hence

other approaches allow for (semi-)automatically _inducing_ wrappers [161]. A modern such approach

- used to enrich knowledge graphs in systems such as LODIE [180] – is to apply distant supervision,

whereby EL is used to identify and link entities in the webpage to nodes in the knowledge graph

such that paths in the markup that connect pairs of nodes for known edges can be extracted, ranked,


53


**Report**



**Claimant**


|id|name|country|
|---|---|---|
|XY12SDA<br>AB9123N<br>XI92HAS|John Smith<br>Joan Dubois<br>Jorge Hernández|U.S.<br>France<br>Chile|


|crime|claimant|station|date|
|---|---|---|---|
|Pickpocketing<br>Assault<br>Pickpocketing<br>Fraud|XY12SDA<br>AB9123N<br>XY12SDA<br>FI92HAS|Viña del Mar<br>Arica<br>Rapa Nui<br>Arica|2019-04-12<br>2019-04-12<br>2019-04-12<br>2019-04-13|



Fig. 33. Example relational database instance with two tables describing crime data


and applied to other examples. Taking Figure 32, for example, distant supervision may link [Rapa Nui]

and **[World Heritage Sites]** to the nodes [Easter Island] and [World Heritage Site] in the knowledge graph using
EL, and given the edge [Easter Island] named World Heritage Site in the knowledge graph (extracted per
Figure 31), identify the candidate path ( _𝑥,_ td[1] [−] - tr [−] - table [−] - h1 _,𝑦_ ) as reflecting edges of the form

_𝑥_ named _𝑦_, where _𝑡_ [ _𝑛_ ] indicates the _𝑛_ [th] child of tag _𝑡_, _𝑡_ [−] its inverse, and _𝑡_ 1 · _𝑡_ 2 concatenation.

Finally, paths with high confidence (e.g., ones “witnessed” by many known edges in the knowledge

graph) can then be used to extract novel edges, such as [Qhapaq Ñan] named World Heritage Site, both

on this page and on related pages of the website with similar structure (e.g., for other countries).


_6.3.2_ _Web table extraction._ Other approaches target specific types of markup, most commonly

_web tables_, i.e., tables embedded in HTML webpages. However, web tables are designed to enhance

human readability, which often conflicts with machine readability. Many web tables are used for lay
out and page structure (e.g., navigation bars), while those that do contain data may follow different

formats such as relational tables, listings, attribute-value tables, matrices, etc. [81, 108]. Hence a first

step is to classify tables to find ones appropriate for the given extraction mechanism(s) [108, 139].

Next, web tables may contain column spans, row spans, inner tables, or may be split vertically

to improve human aesthetics. Hence a table normalisation phase is required to identify headers,

merge split tables, un-nest tables, transpose tables, etc. [81, 108, 126, 145, 312, 418]. Subsequently,

approaches may need to identify the _protagonist_ [108, 367] – the main entity that the table describes

- which is rather found elsewhere in the webpages; for example, though [World Heritage Sites] is the pro
tagonist of the table of Figure 31, it is not mentioned by the table. Finally, extraction processes can

be applied, potentially associating cells with entities [317, 365], columns with types [126, 317, 365],

and column pairs with relations [317, 367]. For the purposes of enriching knowledge graphs, more

recent approaches again apply distant supervision, first linking table cells to knowledge graph nodes,

which are used to generate candidates for type and relation extraction [317, 365, 367]. Statistical

distributions can also aid in linking numerical columns [376]. Specialised extraction frameworks

have also been designed for tables on specific websites, where prominent knowledge graphs, such

as DBpedia [311] and YAGO [507] focus on extraction from info-box tables in Wikipedia.


_6.3.3_ _Deep Web crawling._ The _Deep Web_ presents a rich source of information accessible only

through searches on web forms, thus requiring _Deep Web crawling_ techniques to access [332].

Systems have been proposed to extract knowledge graphs from Deep Web sources [97, 178, 310].

Approaches typically attempt to generate sensible form inputs – which may be based on a user

query or generated from reference knowledge – and then extract data from the generated responses

(markup documents) using the aforementioned techniques [97, 178, 310].


**6.4** **Structured Sources**

Much of the legacy data available within organisations and on the Web is represented in struc
tured formats, primarily tables – in the form of relational databases, CSV files, etc. – but also

tree-structured formats such as JSON, XML etc. Unlike text and markup documents, structured


54


Fig. 34. Possible result of applying a direct mapping to the first rows of both tables in Figure 33


sources can often be _mapped_ to knowledge graphs whereby the structure is (precisely) transformed

according to a mapping rather than (imprecisely) extracted. The mapping process involves two

steps: 1) create a mapping from the source to a graph, and 2) use the mapping in order to materialise

the source data as a graph or to virtualise the source (creating a graph view over the legacy data).


_6.4.1_ _Mapping from tables._ Tabular sources of data are prevalent, where, for example, the structured

content underlying many organisations, websites, etc., are housed in relational databases. In

Figure 33 we present an example of a relational database instance that we would like to integrate

into our knowledge graph under construction. There are then two approaches for mapping content

from tables to knowledge graphs: a _direct mapping_, and a _custom mapping_ .

A direct mapping automatically generates a graph from a table. We present in Figure 34 the result

of a standard direct mapping [20], which creates an edge [x] y z for each (non-header, non-empty,
non-null) cell of the table, such that [x] represents the row of the cell, y the column name of the cell,

and [z] the value of the cell. In particular, [x] typically encodes the values of the primary key for a row
(e.g., **Claimant** . **id** ); otherwise, if no primary key is defined (e.g., per the **Report** table), [x] can be an
anonymous node or a node based on the row number. The node [x] and edge label y further encode

the name of the table to avoid clashes across tables that have the same column names used with

different meanings. For each row [x], we may add a type edge based on the name of its table. The

value [z] may be mapped to datatype values in the corresponding graph model based on the source
domain (e.g., a value in an SQL column of type Date can be mapped to xsd:date in the RDF data
model). If the value is null (or empty), typically the corresponding edge will be omitted. [28] With

respect to Figure 34, we highlight the difference between the nodes [Claimant-XY12SDA] and [XY12SDA],

where the former denotes the row (or entity) identified by the latter primary key value. In case of a

foreign key between two tables – such as **Report.claimant** referencing **Claimant.id** - we can

link, for example, to [Claimant-XY12SDA] rather than [XY12SDA], where the former node also has the name

and country of the claimant. A direct mapping along these lines has been standardised for mapping

relational databases to RDF [20], where Stoica et al. [500] have recently proposed an analogous

direct mapping for property graphs. Another direct mapping has been defined for CSV and other

tabular data [516] that further allows for specifying column names, primary/foreign keys, and data

types – which are often missing in such data formats – as part of the mapping itself.

Although a direct mapping can be applied automatically on tabular sources of data and preserve

the information of the original source – i.e., allowing a deterministic inverse mapping that recon
structs the tabular source from the output graph [471] – in many cases it is desirable to customise

a mapping, such as to align edge labels or nodes with a knowledge graph under enrichment, etc.

Along these lines, declarative mapping languages allow for manually defining custom mappings


28One might consider representing nulls with anonymous nodes. However, nulls in SQL can be used to mean that there is

no such value, which conflicts with the existential semantics of anonymous nodes in models such as RDF (i.e., blank nodes).


55


from tabular sources to graphs. A standard language along these lines is the RDB2RDF Mapping

Language (R2RML) [118], which allows for mapping from individual rows of a table to one or

more custom edges, with nodes and edges defined either as constants, as individual cell values, or

using templates that concatenate multiple cell values from a row and static substrings into a single

term; for example, a template {id}-{country} may produce nodes such as [XY12SDA-U.S.] from the
**Claimant** table. In case that the desired output edges cannot be defined from a single row, R2RML

allows for (SQL) queries to generate tables from which edges can be extracted where, for example,

edges such as [U.S.] crimes 2 can be generated by defining the mapping with respect to a query
that joins the **Report** and **Claimant** tables on **claimant** = **id**, grouping by **country**, and applying

a count. A mapping can then be defined on the results table such that the source node denotes

the value of **country**, the edge label is the constant crimes, and the target node is the count value.

An analogous standard also exists for mapping CSV and other tabular data to RDF graphs, again

allowing keys, column names, and datatypes to be chosen as part of the mapping [517].

Once the mappings have been defined, one option is to use them to _materialise_ graph data

following an _Extract-Transform-Load_ ( _ETL_ ) approach, whereby the tabular data are transformed

and explicitly serialised as graph data using the mapping. A second option is to use _virtualisation_

through a _Query Rewriting_ ( _QR_ ) approach, whereby queries on the graph (using, e.g., SPARQL,

Cypher, etc.) are translated to queries over the tabular data (typically using SQL). Comparing these

two options, ETL allows the graph data to be used as if they were any other data in the knowledge

graph. However, ETL requires updates to the underlying tabular data to be explicitly propagated

to the knowledge graph, whereas a QR approach only maintains one copy of data to be updated.

The area of _Ontology-Based Data Access_ ( _OBDA_ ) [561] is then concerned with QR approaches

that support ontological entailments as discussed in Section 4. Although most QR approaches

only support non-recursive entailments expressible as a single (non-recursive) query, some QR

approaches support recursive entailments through rewritings to recursive queries [472].


_6.4.2_ _Mapping from trees._ A number of popular data formats are based on trees, including XML

and JSON. While one could imagine – leaving aside issues such as the ordering of children in a tree

- a trivial direct mapping from trees to graphs by simply creating edges of the form _[𝑥]_ child _𝑦_

for each node _𝑦_ that is a child of _𝑥_ in the source tree, such an approach is not typically used,

as it represents the literal structure of the source data. Instead, the content of tree-structured

data can be more naturally represented as a graph using a custom mapping. Along these lines,

the GRDLL standard [99] allows for mapping from XML to (RDF) graphs, while the JSON-LD

standard [494] allows for mapping from JSON to (RDF) graphs. In contrast, hybrid query languages

such as XSPARQL [47] allow for querying XML and RDF in an integrated fashion, thus supporting

both materialisation and virtualisation of graphs over tree-structured sources of legacy data.


_6.4.3_ _Mapping from other knowledge graphs._ Another route to construct or enrich knowledge

graphs is to leverage existing knowledge graphs as a source. In our scenario, for instance, a large

number of points of interest for the Chilean tourist board may be available in existing knowledge

graphs such as DBpedia [311], LinkedGeoData [497], Wikidata [543], YAGO [243], BabelNet [373],

etc. However, depending on the knowledge graph under construction, not all entities and/or

relations may be of interest. A standard option to extract a relevant sub-graph of data is to use

SPARQL construct-queries that generate graphs as output [375]. Entity and schema alignment

between the knowledge graphs may be further necessary to better integrate (parts of) external

knowledge graphs; this may be done using linking tools for graphs [378, 541], based on the use of

external identifiers [407], or indeed may be done manually [407]. For instance, Wikidata [543] uses

Freebase [54, 407] as a source; Gottschalk and Demidova [197] extract an event-centric knowledge


56


graph from Wikidata, DBpedia and YAGO; while Neumaier and Polleres [375] construct a spatio
temporal knowledge graph from Geonames, Wikidata, and PeriodO [193] (as well as tabular data).


**6.5** **Schema/Ontology Creation**


The discussion thus far has focussed on extracting _data_ from external sources in order to create and

enrich a knowledge graph. In this section, we discuss some of the principal methods for generating a

schema based on external sources of data, including human knowledge. For discussion on extracting

a schema from the knowledge graph itself, we refer back to Section 3.1.3. In general, much of the

work in this area has focussed on the creation of ontologies using either ontology engineering

methodologies, and/or ontology learning. We discuss these two approaches in turn.


_6.5.1_ _Ontology engineering._ Ontology engineering refers to the development and application of

methodologies for building ontologies, proposing principled processes by which better quality

ontologies can be constructed and maintained with less effort. Early methodologies [157, 202, 388]

were often based on a waterfall-like process, where requirements and conceptualisation were fixed

before starting to implement the ontology in a logical language, using, for example, an ontology

engineering tool [194, 284, 287]. However, for situations involving large or ever-evolving ontologies,

more iterative and agile ways of building and maintaining ontologies have been proposed.

DILIGENT [414] was an early example of an agile methodology, proposing a complete process

for ontology life-cycle management and knowledge evolution, as well as separating local changes

(local views on knowledge) from global updates of the core part of the ontology, using a review

process to authorise the propagation of changes from the local to the global level. This methodology

is similar to how, for instance, the large clinical reference terminology SNOMED CT [263] (also

available as an ontology) is maintained and evolved, where the (international) core terminology

is maintained based on global requirements, while national or local extensions to SNOMED CT

are maintained based on local requirements. A group of authors then decides which national or

local extensions to propagate to the core terminology. More modern agile methodologies include

eXtreme Design (XD) [50, 420], Modular Ontology Modelling (MOM) [238, 300], Simplified Agile

Methodology for Ontology Development (SAMOD) [409], etc. Such methodologies typically include

two key elements: _ontology requirements_ and (more recently) _ontology design patterns_ .

Ontology requirements specify the intended task of the resulting ontology – or indeed the

knowledge graph itself – based on the ontology as its schema. A common way to express ontology

requirements is through Competency Questions (CQ) [203], which are natural language questions

illustrating the typical knowledge that one would require the ontology (or the knowledge graph)

to provide. Such CQs can then be complemented with additional restrictions, and reasoning

requirements, in case that the ontology should also contain restrictions and general axioms for

inferring new knowledge or checking data consistency. A common way of testing ontologies (or

knowledge graphs based on them) is then to formalise the CQs as queries over some test set of

data, and make sure the expected results are entailed [53, 285]. We may, for example, consider the

CQ “ _What are all the events happening in Santiago?_ ”, which can be represented as a graph query

Event type **?event** location Santiago . Taking the data graph of Figure 1 and the axioms of Figure 12,

we can check to see if the expected result [EID15] is entailed by the ontology and the data, and since
it is not, we may consider expanding the axioms to assert that [location] type Transitive .

Ontology Design Patterns (ODPs) are another common feature of modern methodologies [52, 173],

specifying generalisable ontology modelling patterns that can be used as inspiration for modelling

similar patterns, as modelling templates [140, 485], or as directly reusable components [163, 479].

Several pattern libraries have been made available online, ranging from carefully curated ones [19,

479] to open and community moderated ones [163]. As an example, in modelling an ontology for


57


our scenario, we may decide to follow the Core Event ontology pattern proposed by Krisnadhi and

Hitzler [299], which specifies a spatio-temporal extent, sub-events, and participants of an event,

further suggesting competency questions, formal definitions, etc., to support this pattern.


_6.5.2_ _Ontology learning._ The previous methodologies outline methods by which ontologies can be

built and maintained manually. Ontology learning, in contrast, can be used to (semi-)automatically

extract information from text that is useful for the ontology engineering process [76, 93]. Early

methods focussed on extracting terminology from text that may represent the relevant domain’s

classes; for example, from a collection of text documents about tourism, a terminology extrac
tion tool – using measures of _unithood_ that determine how cohesive an _𝑛_ -gram is as a unitary

phrase, and _termhood_ that determine how relevant the phrase is to a domain [339] – may iden
tify _𝑛_ -grams such as “visitor visa”, “World Heritage Site”, “off-peak rate”, etc., as terminology of

particular importance to the tourist domain, and that thus may merit inclusion in such an ontol
ogy. Axioms may also be extracted from text, where subclass axioms are commonly targetted,

based on modifying nouns and adjectives that incrementally specialise concepts (e.g., extracting

f



Visitor Visa subc. of Visa from the noun phrase “visitor visa” and isolated appearances of “visa” else
f

where), or using Hearst patterns [225] (e.g., extracting [Off-Peak Rate] subc. of Discount from “many
discounts, such as off-peak rates, are available” based on the pattern “X, such as Y”). Textual defi
nitions can also be harvested from large texts to extract hypernym relations and induce a taxonomy

from scratch [534]. More recent works aim to extract more expressive axioms from text, including

disjointness axioms [540]; and axioms involving the union and intersection of classes, along with

existential, universal, and qualified-cardinality restrictions [412]. The results of an ontology learn
ing process can then serve as input to a more general ontology engineering methodology, allowing

us to validate the terminological coverage of an ontology, to identify new classes and axioms, etc.


**7** **QUALITY ASSESSMENT**


Independently of the (kinds of) source(s) from which a knowledge graph is created, data extracted

for the initial knowledge graph will usually be incomplete, and will contain duplicate, contradictory

or even incorrect statements – especially when taken from multiple sources. After the initial

creation and enrichment of a knowledge graph from external sources, a crucial step is thus to assess

the _quality_ of the resulting knowledge graph. By quality, we here refer to _fitness for purpose_ . Quality

assessment then helps to ascertain for which purposes a knowledge graph can be reliability used.

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
