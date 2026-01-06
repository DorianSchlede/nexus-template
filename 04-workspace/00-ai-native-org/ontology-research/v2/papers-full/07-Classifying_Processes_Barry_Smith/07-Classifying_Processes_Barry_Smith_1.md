<!-- Source: 07-Classifying_Processes_Barry_Smith.pdf | Chunk 1/2 -->

© 2012 Blackwell Publishing Ltd
_Ratio (new series)_ XXV 4 December 2012 0034–0006


CLASSIFYING PROCESSES: AN ESSAY IN
APPLIED ONTOLOGYrati_557 463..488


_Barry Smith_


_Abstract_
We begin by describing recent developments in the burgeoning
discipline of applied ontology, focusing especially on the ways
ontologies are providing a means for the consistent representation
of scientific data. We then introduce Basic Formal Ontology
(BFO), a top-level ontology that is serving as domain-neutral framework for the development of lower level ontologies in many specialist disciplines, above all in biology and medicine. BFO is a
bicategorial ontology, embracing both three-dimensionalist (continuant) and four-dimensionalist (occurrent) perspectives within
a single framework. We examine how BFO-conformant domain
ontologies can deal with the consistent representation of scientific
data deriving from the measurement of processes of different
types, and we outline on this basis the first steps of an approach to
the classification of such processes within the BFO framework. [1]


**1. The Background of Applied Ontology**


_1.1 Applied Ontologies in Biology_


In the wake of the successful sequencing of the human genome,
contemporary biology has been transformed into a discipline in
which computer processing of genomic data plays an essential
role. But genomic data processed by computers are useful to our
understanding of, say, animal behavior, or human health and
disease, only if some way can be found to link these data
to theoretical assertions using terms that are intelligible to biologists. Such links are created by means of what biologists call
‘ontologies’, which are classifications of biological and other phe

1 With acknowledgements to all of those who have worked on the development of Basic
Formal Ontology since its inception, and with special thanks to Thomas Bittner, Werner
Ceusters, Damiano Costa, Pierre Grenon, Ingvar Johansson, Kevin Mulligan, Chris
Mungall, Alan Ruttenberg, and Peter Simons. The work on this paper was partially supported by the National Institutes of Health through the NIH Roadmap for Medical
Research, Grant 1 U 54 HG004028 (National Center for Biomedical Ontology).


464 BARRY SMITH


nomena used to annotate (or ‘tag’) genomic and other experimental data in a systematic way that enables computers to gain
consistent access even to data that has been collected in highly
heterogeneous ways. [2]
When scientists are collecting data, this still frequently happens
in a poorly coordinated fashion, and this is so even where the
scientists in question are working in the same field. The data are
in consequence difficult to aggregate in ways that might be useful
in testing hypotheses or in drawing comparisons. In former times
the needed connections were drawn through manual intervention by human beings familiar with the subject-matter. The
indispensability of computers to the processing of data in
information-intensive areas of science, however, has brought the
recognition that ways need to be found to establish such connections computationally. The rise of science-based ontologies [3] is one
product of this recognition. [4]
We shall focus in what follows on those ontologies that are
being developed on the basis of the assumption that, to create an
ontology that brings benefits to scientists working with data in a
given domain, the ontology should employ classifications that are
based on the established scientific understanding of the entities
and relations in this domain. [5] An ontology of this sort comprises
theoretical terms used to represent the types or classes of entities
in some given domain together with relational expressions representing the relations between these entities. It thereby extends
into the terminology of scientific theories some of the advantages
brought by the International System of Units to the consistent
representation of experimental data expressed in quantitative
terms.
Each ontology can be conceived as a set of terms (nouns and
noun phrases) which form the nodes of a directed acyclical graph,
as in Figure 1. We can think of the nodes in such a graph as


2 David P. Hill, et al., ‘Gene Ontology Annotations: What They Mean and Where They
Come From’, _BMC Bioinformatics_, 9 (2008), S2.
3 On May 7, 2012 a google query for ‘ontology and database’ returned some 10 million
hits, almost twice as many as are returned for the query ‘ontology and philosophy’.
4 Judith Blake, ‘Bio-ontologies – fast and furious’, _Nature Biotechnology_ 22 (2004), 773–
774.
5 Some of the principles governing ontologies of this sort are set forth and defended in
Barry Smith and Werner Ceusters, ‘Ontological Realism as a Methodology for Coordinated
Evolution of Scientific Ontologies’, _Applied Ontology_, 5 (2010), 139–188.


© 2012 Blackwell Publishing Ltd


CLASSIFYING PROCESSES: AN ESSAY IN APPLIED ONTOLOGY 465


representing _types_ or _universals_, [6] which are the sorts of entities
represented by the general terms used in formulating scientific
theories such as ‘cell’ or ‘electron’ and which have _instances_
which are the sorts of entities that are observed in scientific
experiments. The nodes in the graph are joined by edges representing relations between the types, of which the most important
(illustrated in Figure 1) are _is_a_ (abbreviating ‘is a subtype of’)
and _part_of_ . [7]


**Figure 1 Fragments of the Gene Ontology from http://www.ebi.ac.uk/**
**QuickGO/. Nodes in the graph represent types in reality; edges repre-**
**sent** _**is_a**_ **and** _**part_of**_ **relations**


6 We use these expressions synonymously in what follows. In the wider ontological
literature the term ‘class’ is often used for what we are here calling types or universals.
7 Barry Smith, et al., ‘Relations in Biomedical Ontologies’, _Genome Biology_ (2005), 6 (5),
R46.


© 2012 Blackwell Publishing Ltd


466 BARRY SMITH


When two nodes are joined together by the _is_a_ relation, as for
example in:


(1) _receptor activity is_a molecular function_


then this represents an assertion to the effect that all instances of
the first type are also instances of the second type.
When two nodes are joined together by the _part_of_ relation,
as in


(2) _viral receptor activity part_of response to virus_


then this represents an assertion to the effect that every instance
of the first type is a part of some instance of the second type.
(Here ‘part of’ in the unitalicized form represents the familiar
instance-level parthood relation holding between, for example,
your finger and your hand, or between the first half of a football
match and the whole match. [8] )


_1.2 The Common Logic Interchange Format and the Web_
_Ontology Language_


Ontological axioms such as (1) and (2), together with accompanying definitions of terms and relations, are formulated using
logical languages – typically fragments of first-order logic – developed to facilitate the representation and interchange of information and data among disparate computer systems. [9] Prominent
examples are the (CLIF) Common Logic Interchange Format [10]
and the (OWL) Web Ontology Language [11] . Common Logic is an
ISO Standard family of languages with an expressivity equivalent
to that of first-order logic. OWL-DL is a fragment of the language
of first order logic belonging to the family of what are called
Description Logics. While OWL-DL is marked by severe restrictions on its expressivity, the theories formulated in its terms have


8 See again ‘Relations in Biomedical Ontologies’.
9 http://metadata-stds.org/24707/index.html.
10 _Common Logic – A Framework for a Family of Logic-Based Languages_, ed. Harry Delugach.
ISO/IEC JTC 1/SC 32N1377, International Standards Organization Final Committee
Draft, 2005-12-13; http://cl.tamu.edu/docs/cl/32N1377T-FCD24707.pdf.
11 ‘OWL 2 Web Ontology Language’, http://www.w3.org/TR/owl2-overview.


© 2012 Blackwell Publishing Ltd


CLASSIFYING PROCESSES: AN ESSAY IN APPLIED ONTOLOGY 467


desirable computational properties. Because logical languages
such as CLIF or OWL are used in their formulation, ontologies
themselves can be viewed as simple first-order theories. Providing
care is taken to use terms, definitions and relational expressions
in consistent ways in different ontologies, such theories can be
merged at will to create larger ontologies and, at least in the case
of ontologies formulated using a language like OWL, the consistency of such mergers can be checked automatically using dedicated software applications called ‘reasoners’. [12]


_1.3 The Gene Ontology_


It is the Gene Ontology (GO), portions of which are illustrated in
Figure 1, which is the most successful ontology currently being
used by scientists in reasoning with experimental data. [13] The GO
consists of three sub-ontologies, together comprehending some
30,000 terms representing types and subtypes of _biological processes,_
_molecular functions_, and _cellular components_ . The GO is used by
researchers in biology and biomedicine as a controlled vocabulary
for describing in species-neutral fashion the attributes of genes
and gene products (for example proteins) identified both in
experiments on model organisms such as mouse or fly and in
clinical studies of human beings. The GO offers a set of terms, such
as ‘membrane’ or ‘viral receptor activity’ or ‘meiosis’, which are
defined in ways which reflect the usage of biologists. It thereby
provides a means of computationally associating humanly intelligible descriptions of biological phenomena with the massive quantities of sequence data being made available through genomic
experimentation. Because the GO is species neutral, it provides a
means of comparing data pertaining to different organisms in a
way which allows results gained through experimentation on nonhuman organisms to be exploited in studies of human health and
disease. [14]


12 http://www.w3.org/2007/OWL/wiki/Implementations.
13 The Gene Ontology Consortium, et al., ‘Gene Ontology: Tool for the Unification of
Biology’, _Nature Genetics_, 2000 May; 25(1): 25–29.
14 See for example A. Mohammadi et al., ‘Identification of Disease-Causing Genes Using
Microarray Data Mining and Gene Ontology,’ _BMC Medical Genomics_, 2011; 4: 12.


© 2012 Blackwell Publishing Ltd


468 BARRY SMITH


_1.4 The Gene Ontology and the Unification of Science_


The GO is described by its originators as a ‘tool for the unification
of biology’, and we can see how it is being used, in conjunction
with other ontologies such as the Protein [15] and Cell Ontologies [16],
to realize at least a part of the old logical empiricist vision of a
logical unification of scientific knowledge. [17] One aspect of this
realization – not clearly anticipated by the logical empiricists – is
the degree to which not only do theoretical assertions need to be
unified through use of common logically structured ontologies,
but so also do experimental data (for example gene or protein
sequence data) compiled in databases processed by computers. In
addition, bioinformaticians have discovered that additional ontology resources are needed to unify both of these with assertions
about the experimental and computational procedures used to
generate the data. This aspect of the unification of science is
addressed by the Ontology for Biomedical Investigations (OBI), [18]
which comprehends a set of terms which can be used to describe
the attributes of experiments in biological and related domains.
The goal is a logically well-structured set of preferred terms and
logical definitions that can be used to support common access
to, and computational reasoning over, data about experiments in
order to address the problems which arise at the point where
experimental methods (or protocols or statistical algorithms or
sample processing techniques or software or equipment used)
have become so complex as to cause problems for the interpretation and comparison of the results achieved with their aid. The
underlying idea is that use of the OBI vocabulary to annotate
results obtained through experimentation would make these
results not only more easily interpretable by human beings but
also more reliably processable by computers.


15 Darren A. Natale, et al. ‘The Protein Ontology: A Structured Representation of
Protein Forms and Complexes’, _Nucleic Acids Research_, 39 (2011), D539–45.
16 Terrence F. Meehan, et al. ‘Logical Development of the Cell Ontology’, _BMC Bioin-_
_formatics_ 12 (2011), 6.
17 Rudolf Carnap, ‘Logical Foundations of the Unity of Science’, _International Encyclo-_
_paedia of Unified Science_, vol. I, Chicago: University of Chicago Press, 1938. Compare also
J. J. Woodger, _The Axiomatic Method in Biology_, Cambridge: Cambridge University Press,
1937, and the discussion in Smith and Ceusters, ‘Ontological Realism’.
18 Ryan R. Brinkman, et al., ‘Modeling Biomedical Experimental Processes with OBI’,
_Journal of Biomedical Semantics_, 2010, 1, Suppl. 1.


© 2012 Blackwell Publishing Ltd


CLASSIFYING PROCESSES: AN ESSAY IN APPLIED ONTOLOGY 469


**2. Basic Formal Ontology**


As will by now be clear, the principal concerns of applied ontologists are highly practical in nature. Just occasionally, however, they
still face problems of a recognizably philosophical sort, and one
such problem – relating to the treatment of process measurement
data – is the topic of this essay.
Basic Formal Ontology (BFO) is a domain-neutral resource
used by biologists and others to provide a top-level ontology that
can serve as a common starting point for the creation of domain
ontologies in different areas of science. [19] BFO provides a formalontological architecture and a set of very general terms and relations that are currently being used by more than 100 ontology
development groups in biology and other fields. [20]
BFO is, by the standards predominant in contemporary ontology, very small, consisting of just 34 terms (see Figure 2), including both familiar terms such as ‘process’, ‘object’, ‘function’,
‘role’ and ‘disposition’, and less familiar terms such as ‘generically
dependent continuant’ and ‘continuant fiat boundary’. Each of
these terms must either be declared primitive and elucidated by
examples and accompanying axioms, or it must be defined in a
logically coherent way in terms of these primitives.


_2.1 Continuants and Occurrents_


BFO takes as its starting point a familiar distinction between
two sets of views, which we can refer to as four-dimensionalist
and three-dimensionalist, respectively. Four-dimensionalists (in
simple terms) see reality as consisting exclusively of fourdimensional entities (variously referred to as processes, events,
occurrents, perdurants, spacetime-worms, and so forth). They
thereby regard all talk of entities of other sorts – for example, of
three-dimensional things such as you and me – as a mere locution,
to be eliminated in favour of some ultimate four-dimensionalist
translation. (A four-dimensionalist might hold, for example, that
only processes exist, and that talk of continuously existing things
pertains rather to special kinds of processual entities, for example


19 http://ontology.buffalo.edu/BFO/Reference.
20 http://www.ifomis.org/bfo/users.


© 2012 Blackwell Publishing Ltd


470 BARRY SMITH


© 2012 Blackwell Publishing Ltd


CLASSIFYING PROCESSES: AN ESSAY IN APPLIED ONTOLOGY 471


to continuous series of _processes of a bill-clintonizing sort_ . [22] ) The
three-dimensionalists who embrace positions at the opposite
extreme see reality as consisting exclusively of entities extended
along the three spatial dimensions, and they view all change in
terms of the different attributes truly predicable of such entities
at different times. Talk of processes, from this perspective, is a
mere locution to be eliminated in favour of some ultimate threedimensionalist translation.
Both families of views bring benefits of their own. In the field of
medical ontology, for example, four-dimensionalism provides
a natural framework for the ontological treatment of processes
of, say, drug interaction or immune response, while threedimensionalism provides a similarly natural framework for the
treatment of the chemical, histological and anatomical structures
which participate in such processes.
Unfortunately, the two sets of views are standardly formulated
in a way which forces a choice between one or the other. BFO, in
contrast, is founded on a bicategorial approach which seeks to
combine elements of both the three-dimensionalist and fourdimensionalist perspectives. [23] Thus it incorporates an ontology of
continuants and an ontology of occurrents within a single framework in a way that seeks to reconcile the contrasting logicoontological orders reigning in each.


_2.2 Zemach’s ‘Four Ontologies’_


BFO’s treatment of the dichotomy between continuants and
occurrents is adapted in part from the strategy proposed by
Zemach in his ‘Four Ontologies’ [24] for distinguishing between continuant and non-continuant entities, which Zemach calls ‘things’
and ‘events’, respectively. The former, for Zemach, are defined by
the fact that they can be sliced (in actuality, or in imagination) to
yield parts only along the spatial dimension – for example those
parts of your table which we call its legs, top, nails, and so on. [25]


22 W. V. O. Quine, _Word and Object (_ Cambridge, MA: The MIT Press), 1960.
23 Pierre Grenon and Barry Smith, ‘SNAP and SPAN: Towards Dynamic Spatial Ontology’, _Spatial Cognition and Computation_, 4 (2004), 69–103.
24 Eddy Zemach, ‘Four Ontologies’, _Journal of Philosophy_ 23 (1970), 231–247.
25 ‘My desk stretches from the window to the door. It has spatial parts, and can be sliced
(in space) in two. With respect to time, however, a thing is a continuant.’ (‘Four Ontologies’, p. 240)


© 2012 Blackwell Publishing Ltd


472 BARRY SMITH


The latter, in contrast, can be sliced to yield parts along any spatial
and temporal dimensions. For example: the first year of the life of
your table; the entire life of your table top (as contrasted with the
life of your table legs); and so forth. As Zemach puts it:


An event is an entity that exists, in its entirety, in the area
defined by its spatiotemporal boundaries, and each part of this
area contains a _part_ of the whole event. There are obviously
indefinitely many ways to carve the world into events, some of
which are useful and interesting (e.g., for the physicist) and
some of which – the vast majority – seem to us to create hodgepodge collections of no interest whatsoever. (‘Four Ontologies’, pp. 233 f.)


Zemach notes that it is the ontology of continuants that comes
most naturally to normal persons:


We normally regard almost every object we come across as a

[continuant entity]: this chair, my pencil, my friend Richard
Roe, the tree around the corner, the fly that crawls on the page.

[The names we give to chairs and dogs] in our language, obey
a grammar which is fundamentally dissimilar to the grammar of
names of events. (‘Four Ontologies’, p. 240)


You, for example, are a continuant; your arms and legs are parts
of you; your childhood, however, is not a part of you; rather, it is
a part of your life. Continuants are entities which have no parts
along the time axis; that is, they may be extended along the three
spatial dimensions, not however along the temporal dimension.
It will be important for what follows that BFO generalizes Zemach’s idea of a continuant entity by allowing not only _things_ (such
as pencils and people) as continuants, but also entities that are
_dependent_ on things, such as qualities and dispositions such as
solubility and fragility. [26] The solubility of a given portion of salt
requires a dissolving process in order to be realized or manifested.
A quality, for BFO, is a dependent continuant that does not
require such a process of realization of this sort.


26 As we shall see below, processes, for BFO, are also dependent entities; they depend for
their existence on the independent continuant entities which are their participants or on
which their participants depend.


© 2012 Blackwell Publishing Ltd


CLASSIFYING PROCESSES: AN ESSAY IN APPLIED ONTOLOGY 473


BFO departs from Zemach also in its account of occurrent
entities. What Zemach refers to as ‘events’ are in every case the
whole content of a spatiotemporal region. As we shall see,
however, what BFO ‘processes’ are conceived in such a way that
multiple processes are able to occupy the same spatiotemporal
region, as for example when a process of your running down the
street is co-located with a process of your getting warmer.
The distinction between continuants and occurrents is for BFO
categorical. All the parts of continuants are continuants, and any
whole to which a continuant belongs is also a continuant. Similarly, all the parts of occurrents are occurrents, and any whole to
which an occurrent belongs is also an occurrent. This division
flows from two essentially different ways of existing in time. For
each continuant, there is some temporal interval during which it
_exists_ . For each occurrent there is some temporal interval during
which it _occurs_ . Certainly there are manifold connections between
continuants and occurrents, but they are secured in BFO not
through parthood relations, but rather through relations of
participation. [27]


_2.3 The Ontological Square_


In allowing not only things but also entities that are dependent on
things as continuants, BFO draws on Aristotle’s ideas concerning
the division of substances and accidents, which reappears in BFO
as the division between independent and dependent continuants.
Given that BFO accepts also the distinction between universals
and particulars, it thus recapitulates Aristotle’s ontological
square, [28] as represented in Table 1.


_2.4 Determinable and Determinate Quality Universals_


Qualities are first-class entities in the BFO ontology (of the sort
referred to elsewhere in the literature as ‘tropes’, or ‘individual


27 Barry Smith and Pierre Grenon, ‘The Cornucopia of Formal-Ontological Relations’,
_Dialectica_ 58: 3 (2004), 279–296.
28 See Barry Smith, ‘Against Fantology’, in J. C. Marek and M. E. Reicher (eds.),
_Experience and Analysis_, Vienna: HPT&ÖBV, 2005, 153–170. Compare also E. J. Lowe, _The_
_Four-Category Ontology_ . _A Metaphysical Foundation for Natural Science_, Oxford University Press:
Oxford 2006, and Luc Schneider, ‘Revisiting the Ontological Square’, in A. Galton and R.
Mizoguchi (eds.), _Formal Ontology in Information Systems, Proceedings of the Sixth International_
_Conference_, Amsterdam: IOS Press, 2010, 73–86.


© 2012 Blackwell Publishing Ltd


474 BARRY SMITH


**Table 1:** Aristotle’s Ontological Square in BFO form










|Col1|Independent Continuant|Col3|Col4|Dependent Continuant|
|---|---|---|---|---|
|Type|_planet_<br>_organism_<br>_cell_<br>exemplifies<br>iates|_planet_<br>_organism_<br>_cell_<br>exemplifies<br>iates|_planet_<br>_organism_<br>_cell_<br>exemplifies<br>iates|_temperature_<br>_30° Celsius temperature_<br>_sickle shape_<br>iates|
|Type|||||
|Instance|_this planet_<br>_this organism_<br>_this cell_<br>depends<br><br>instant|instant|instant|_this temperature_<br>_this 30° Celsius_<br>_temperature_<br>_this sickle shape_<br> on<br>instant|
|Instance|_this planet_<br>_this organism_<br>_this cell_<br>depends<br><br>instant|instant|instant|on|
|Instance|_this planet_<br>_this organism_<br>_this cell_<br>depends<br><br>instant|instant|||



accidents’). They are entities which are dependent on the independent continuant entities (such as molecules, organisms,
planets) which are their bearers. Qualities instantiate quality universals, which are divided into _determinable_ (such as _temperature_,
_length_ and _mass_ ) and _determinate_ (such as _37.0°C temperature_, _1.6_
_meter length_, and _4 kg mass_ ). [29]
Determinable quality universals are _rigid_ in the sense that, if a
determinable quality universal is exemplified by a particular
bearer at any time during which this bearer exists, then it is
exemplified at every such time. [30] John’s temperature (a certain
quality instance inhering in John from the beginning to the end
of his existence) instantiates the same determinable universal
_temperature_ throughout John’s life, even while instantiating different determinate temperature universals from one moment to the
next, as illustrated in Figure 3.
We note in passing that the determinate temperature universals
are independent of whatever system of units is used to describe
them. The universals here referred to in terms of degrees Celsius
would be instantiated even in a world in which the Celsius or any
other system of units had never been proposed. We note also
that for certain families of determinate qualities we can draw a


29 Ingvar Johansson, ‘Determinables are Universals,’ _The Monist_, 83 (2000), 101–121.
30 To say that a quality universal is exemplified by an independent continuant is to say
that some instance of this universal is dependent upon (inheres in) this independent
continuant as its bearer.


© 2012 Blackwell Publishing Ltd


CLASSIFYING PROCESSES: AN ESSAY IN APPLIED ONTOLOGY 475


**Figure 3 John’s temperature and some of the determinable and deter-**
**minate universals it instantiates at different times**


distinction between what we can think of as absolute and relative
values, respectively. The Kelvin scale is a scale of absolute temperature values in this sense.
We can acknowledge also a second sense of ‘relative’ for determinate qualities that is involved for example when clinicians speak
of temperatures as falling within some ‘normal’ range. A single
person has a normal temperature in this sense only relative to (the
temperature qualities of) persons in one or other larger population (for example healthy persons at rest in an indoor environment, persons recovering from pneumonia, persons sharing a
certain genetic mutation in common, and so on).


**3. Processes in BFO**


Our primary concern in the remainder of this essay is with BFO’s
treatment of occurrents, which include processes, process boundaries (for example beginnings and endings), spatiotemporal
regions, and temporal intervals and temporal instants. BFO uses
‘occupies’ to refer to the relation that holds between an occurrent
and the spatiotemporal region which it exactly fills. Processes and
process boundaries _occupy_ spatiotemporal regions and they _span_


© 2012 Blackwell Publishing Ltd


476 BARRY SMITH


temporal intervals and temporal instants, respectively. Processes
are thus distinguished from process boundaries in that the
former, but not the latter, are temporally extended.
The assertion that one entity is an occurrent part of a second
entity means simply that both are occurrents and that the first is a
part – for example a sub-process – of the second. The sum of all
processes taking place in your upper body during the course of
your life is a proper occurrent part of the sum of processes taking
place in your whole body during the same period. There is
however a narrower relation which holds between occurrents _a_
and _b_ in the case where _a_ is exactly the restriction of _b_ to a
temporal region that is a proper part of the temporal region
spanned by _b_ . When this relation holds, we shall say that _a_ and _b_
stand in the relation of _temporal parthood_, defined as follows: [31]


_a_ temporal_part_of _b_ =Def.
_a_ occurrent_part_of _b_
& for some temporal region _r_ ( _a_ spans _r_
& for all occurrents _c_, _r�_
if ( _c_ spans _r�_ & _r�_ occurrent_part_of _r_ )
then ( _c_ occurrent_part_of _a_ iff _c_ occurrent_part_of _b_ )))


The first quarter of a game of football is a temporal part of the
whole game. The process of your heart beating from 4pm to 5pm
today is a temporal part of the entire process of your heart beating
throughout your life. The 4th year of your life is a temporal part
of your life, as is the process boundary which separates the 3rd and
4th years of your life. The process of a footballer’s heart beating
once is an occurrent part, but not a temporal part, of the whole
game (because when this heart beat occurs many other things are
occurring which are also occurrent parts of the whole game).


_3.1 BFO’s Treatment of Quality Measurement Data_


When BFO is used to annotate the results of measurements of
qualities, then in a typical case, for example in the case where
your height is being measured, the following elements can be
distinguished:


31 Compare Peter M. Simons, _Parts. A Study in Ontology_, Oxford: Clarendon Press, 1987,
p. 132.


© 2012 Blackwell Publishing Ltd


CLASSIFYING PROCESSES: AN ESSAY IN APPLIED ONTOLOGY 477


(1) the BFO:object that is you,
(2) the BFO:quality that is your height,
(3) the BFO:one-dimensional spatial region, stretching at some
time _t_ between the top of your head and the base of your
feet, that is measured when we measure your height at _t_ .


The result of this measurement is expressed by means of


(4) the BFO:generically dependent continuant expression:
‘1.7 m tall’.


Each item on this list is unproblematically identifiable as instantiating a BFO category. (4) is an information artifact. [32] It can be
stored, for instance, as a record in some file on your laptop. The
record is said to be _generically dependent_ upon its bearer since it can
be transferred to another laptop through a process of exact
copying. The temperature of your laptop, in contrast, is _specifically_
_dependent_ on the laptop, since a temperature (a specific instance
of the universal _temperature_ ) cannot migrate from one body to
another.


_3.2 Ontological Treatment of Process Measurements_


What happens, now, when we attempt to develop a corresponding
analysis in BFO terms of the data resulting from measurements
of processes? In the case of a body moving with constant speed,
for example, we can here distinguish at least the following
elements:


(1) the BFO:object that is moving (changing its spatial
location),
(2) the BFO:process of moving (change of spatial location),
(3) the BFO:spatiotemporal region occupied by this process
(the path of the motion),
(4) the BFO:temporal region spanned by this process (the
temporal projection of (3)),
(5) the speed of the process (rate of change of the spatial
location of (1)),


32 http://code.google.com/p/information-artifact-ontology/.


© 2012 Blackwell Publishing Ltd


478 BARRY SMITH


where (5) is represented by means of


(6) the BFO:generically dependent continuant expression:
‘3.12 meters per second’.


Each of the items (1)–(4) and (6) instantiates a readily identifiable BFO category. For item (5), on the other hand, there is no
candidate category in the BFO ontology, since there is no counterpart on the occurrent side for BFO’s qualities of independent
continuants. [33]


_3.3 Why Processes Do Not Change_


To see why not, we need to understand the reason why qualities
of independent continuants are accepted by BFO as first class
entities. This turns on the fact that _independent continuants can_
_change_ from one time to the next by gaining and losing qualities.
No counterpart of such change can be accepted by BFO on the
occurrent side, since it follows trivially from BFO’s fourdimensionalist account of occurrents that _occurrents cannot_
_change_ .
Processes, in particular, cannot change on the fourdimensionalist view, because processes _are_ changes (they are
changes in those independent continuant entities which are their
participants). [34] Certainly we have ways of speaking whose surface
grammar suggests that processes can change. But when we say, for
example, _let’s speed up this process_, then what we mean (in fourdimensionalist terms) is: let’s ensure that some on-going process
is one which will be quicker than the process that would have
occurred had we not made some specific extra effort.


33 Note that we could view speed in BFO terms as a (non-rigid) quality of the moving
object, a view conformant with our way of speaking when we talk, for example, of the speed
of light, or the speed of the earth, or the speed of a billiard ball. We believe that a view
along these lines for process measurement data in general can and should be developed,
since processes of each different type can occur only if there are corresponding types of
qualities and dispositions on the side of the continuants which are their participants. Thus
we see a view of this sort as a supplement to an account along the lines presented in the
text.
34 Antony Galton and Riichiro Mizoguchi, ‘The Water Falls but the Waterfall Does Not
Fall: New Perspectives on Objects, Processes and Events’, _Applied Ontology_, 4 (2009),
71–107.


© 2012 Blackwell Publishing Ltd


CLASSIFYING PROCESSES: AN ESSAY IN APPLIED ONTOLOGY 479


Continuants may change not only through change in qualities
but also in other ways. For example they may gain and lose parts
over time, as for example when you gain and lose cells from
your body. To address such changes, BFO’s instance-level continuant parthood relation is indexed by time. The counterpart
relation on the side of occurrents, in contrast, holds always
in a non-indexed way. [35] If a process _p_ 1 occupying temporal
interval _t_ 1 is a part of a second process _p2_ occupying temporal
interval _t_ 2, then _p_ 1 is timelessly a part of _p_ 2 just as _t_ 1 is timelessly
a part of _t_ 2.
A second way in which continuants, but not occurrents, may
change is by instantiating non-rigid universals. We saw examples
of this in our discussion of dependent continuant universals
such as temperature above. But examples can be found also
among independent continuant universals such as _larva_ or _fetus_ .
If some organism _a_ instantiates the universal _larva_ at _t_, for
example, then it does not follow that _a_ instantiates _larva_ at all
times at which _a_ exists. Universals on the side of occurrents, in
contrast, are always rigid, so that if an occurrent instantiates a
universal at some time, then it instantiates this universal at all
times. [36]
An apparent analogue of the phenomenon of non-rigidity in
the realm of occurrents is illustrated by a case such as the following. Suppose John, half way through some 20 minute running
process _p_, increases his running speed from 6 to 7 mph. Could we
not then say that the process _p_ instantiates the determinate universal _6 mph running process_ in the first 10 minute interval and the
determinate universal _7 mph running process_ in the second? On the
four-dimensionalist view, the answer to this question is ‘no’: _p_
never instantiates the universal _6 mph running process_, any more
than the front half of my rabbit instantiates the universal _rabbit_ .
What we can more properly assert is that _p_, timelessly, has a
sub-process _p_ 1 (a temporal part of _p_ ), which instantiates the universal _6 mph running process_, and a subsequent sub-process _p_ 2 (a
second temporal part of _p_ ) which instantiates the universal _7 mph_
_running process_ .


35 See again Smith, et al., ‘Relations in Biomedical Ontologies’.
36 See again ‘Relations in Biomedical Ontologies’.


© 2012 Blackwell Publishing Ltd


480 BARRY SMITH


_3.4 First Approximation to a Solution of the Problem of Process_
_Measurement Data_


How, then, do we respond to the need on the part of the users of
BFO to annotate data deriving from measurements which have
processes as their targets?
Our response is, in first approximation, very simple: when we
predicate, for instance, ‘has speed 3.12 m/s’, of a certain process
of motion, then we are asserting, not that that the process in
question _has some special quality_ which the same process, in another
scenario, might conceivably have lacked. Rather, we are asserting
that this process _is of a certain special type_ . Thus an assertion to the
effect that


(1) motion _p_ has speed _v_


is analogous, not to:


(2) rabbit _r_ has weight _w_,


but rather to:


(3) rabbit _r_ instance_of universal _rabbit_ .


(1), in other words, should be interpreted as being of the form:


(4) motion _p_ instance_of universal _motion with speed v_ .


where the universal _motion with speed v_ is a specification of the
universal _motion_ . [37]
This treatment of attribution in terms of instantiation reflects
what is standard policy in other parts of BFO in accordance with
its goal of remaining ontologically simple. There are no qualities
of occurrents, in BFO, just as there are no qualities of qualities,
and also no qualities of spatial or temporal regions. Leaving aside
the single case of qualities of independent continuants, attributions in BFO are quite generally treated in terms of the relation of
instantiation, as in Table 2:


37 See Ingvar Johansson, ‘Four Kinds of Is_a Relation’, in Katherine Munn and Barry
Smith (eds.), _Applied Ontology_, Frankfurt/Lancaster: ontos, 2008, 269–293.


© 2012 Blackwell Publishing Ltd


CLASSIFYING PROCESSES: AN ESSAY IN APPLIED ONTOLOGY 481


**Table 2:** Examples of attributions in BFO


spatial region _r_ has _r_ instance_of universal _region with_
volume _w_ _volume w_
height quality _q_ has value _q_ projects onto a one-dimensional
2 meters at _t_ spatial region _r_ at _t_ and _r_
instance of universal _2 meter long_
_one-dimensional spatial region_
temporal region _t_ has _t_ instance_of universal _temporal_
duration _d_ _region with duration d_
temperature quality _q_ has _q_ instance_of universal _63° Celsius_
value 63° Celsius _temperature quality_
process _p_ has duration _d_ process _p_ spans temporal region _t_
and _t_ instance_of universal
_temporal region with duration d_
motion _p_ of object _o_ has the sequence of locations occupied
trajectory with shape _s_ by object _o_ at successive instants
of time forms a spatiotemporal
region _t_ and _t_ instance_of
universal _spatiotemporal region with_
_shape s_


_3.5 Processes as Dependent Entities_


Processes themselves stand to the independent continuants which
are their participants in a relation that is analogous to that in
which qualities stand to the independent continuants which are
their bearers. In both cases we have to deal with the relation of
what BFO calls _specific dependence_ . [38] This means that we can extend
the ontological square in Table 1 with a representation of the
relation between instances and universals on the side of occurrents to create an ontological sextet, as in Table 3. [39]
Our strategy, now, is to use the instantiation relation captured
in the rightmost column of Table 3 as basis for an account of the
truthmakers of process attributions. But to make an approach
along these lines work, certain problems still need to be
addressed.


38 See again Smith and Grenon, ‘Cornucopia’.
39 See again Smith, ‘Against Fantology’.


© 2012 Blackwell Publishing Ltd


482 BARRY SMITH


**Table 3:** The Ontological Sextet











|Col1|Independent<br>Continuant|Dependent<br>Continuant|Col4|Col5|Occurrent|
|---|---|---|---|---|---|
|Type|_Planet_<br>_organism_<br>_cell_<br>iates<br>|_temperature_<br>_30° Celsius temperature_<br>_sickle shape_<br>es<br>iates|_temperature_<br>_30° Celsius temperature_<br>_sickle shape_<br>es<br>iates|_temperature_<br>_30° Celsius temperature_<br>_sickle shape_<br>es<br>iates|_course of temperature_<br>_changes_<br>_life of organism_<br>_life of cell_<br>tes|
|Type|_Planet_<br>_organism_<br>_cell_<br>iates<br>|_temperature_<br>_30° Celsius temperature_<br>_sickle shape_<br>es<br>iates|_temperature_<br>_30° Celsius temperature_<br>_sickle shape_<br>es<br>iates|||
|Instance|_this planet_<br>_this organism_<br>_this cell_<br>instant<br>dep<br>exe|_John’s temperature_<br>_this 30° Celsius_<br>_temperature in this_<br>_organism now_<br>_this sickle shape_<br>ends on<br>mplifi<br>instant|instant|instant|_the course of_<br>_temperature changes in_<br>_John during his lifetime_<br>_John’s life_<br>_the life of this cell_<br>instantia|
|Instance|_this planet_<br>_this organism_<br>_this cell_<br>instant<br>dep<br>exe|depends on|depends on|depends on||
|Instance|_this planet_<br>_this organism_<br>_this cell_<br>instant<br>dep<br>exe|||||


**4. Process Profiles**


We note, first, that a single running process _p_ might be an instance
of multiple determinable universals such as:


_running process_
_constant speed running process_
_cardiovascular exercise process_
_air-displacement process_
_compression sock testing process_


as well as of multiple determinate universals such as


_running process of 30 minute duration_
_3.12 m/s motion process_
_9.2 calories per minute energy burning process_
_30.12 liters per kilometer oxygen utilizing process_


and so on.
How, given the complexity of this list and of the many similar
lists which could be created for many other types of process, are
we to create classifications of the process universals instantiated
in different domains in the sort of principled way that will be


© 2012 Blackwell Publishing Ltd


CLASSIFYING PROCESSES: AN ESSAY IN APPLIED ONTOLOGY 483


necessary to ensure consistency and interoperability when classifications are needed for the annotation of data in domains such as
physiology or pathology?
To see the lines of our answer to this question, consider Figure 4,
which illustrates the cardiac events occurring in the left ventricle of
a human heart. This figure tells us that each successive beating of
the heart is such as to involve multiple different sorts of physiological processes, corresponding to measurements along the six distinct dimensions of _aortic pressure_, _atrial pressure_, _ventricular pressure_,
_ventricular volume_, _electrical activity_, and _voltage_ [40], respectively. [41]


**Figure 4 A Wiggers diagram, showing the cardiac processes occurring in**
**the left ventricle** [42]



120


100


80


60


40


20


0


130


90


50











Aortic pressure


Atrial pressure


Ventricular pressure


Ventricular volume


Electrocardiogram



Phonocardiogram

