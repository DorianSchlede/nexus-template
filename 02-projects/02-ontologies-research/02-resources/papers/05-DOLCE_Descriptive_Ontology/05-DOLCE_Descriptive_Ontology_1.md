<!-- Source: 05-DOLCE_Descriptive_Ontology.pdf | Chunk 1/2 -->

Applied Ontology 0 (0) 1 1
IOS Press

# DOLCE: A Descriptive Ontology for Linguistic and Cognitive Engineering [1]


Stefano Borgo _[∗]_, Roberta Ferrario, Aldo Gangemi, Nicola Guarino, Claudio Masolo,
Daniele Porello, Emilio M. Sanfilippo and Laure Vieu


**Abstract.** DOLCE, the first top-level (foundational) ontology to be axiomatized, has remained stable for twenty years and today
is broadly used in a variety of domains. DOLCE is inspired by cognitive and linguistic considerations and aims to model a
commonsense view of reality, like the one human beings exploit in everyday life in areas as diverse as socio-technical systems,
manufacturing, financial transactions and cultural heritage. DOLCE clearly lists the ontological choices it is based upon, relies
on philosophical principles, is richly formalized, and is built according to well-established ontological methodologies, e.g.
OntoClean. Because of these features, it has inspired most of the existing top-level ontologies and has been used to develop or
improve standards and public domain resources (e.g. CIDOC CRM, DBpedia and WordNet). Being a foundational ontology,
DOLCE is not directly concerned with domain knowledge. Its purpose is to provide the general categories and relations needed
to give a coherent view of reality, to integrate domain knowledge, and to mediate across domains. In these 20 years DOLCE has
shown that applied ontologies can be stable and that interoperability across reference and domain ontologies is a reality. This
paper briefly introduces the ontology and shows how to use it on a few modeling cases.


Keywords: DOLCE, Foundational ontology, Ontological analysis, Formal ontology, Use cases


**Introduction**


As a foundational ontology, DOLCE [2] provides general categories and relations that can be reused in
different application scenarios by specializing them to the specific domains to be modeled.
In order to rely on well-established modeling principles and theoretical bases, it is a common practice
for the categories and relations of foundational ontologies to be philosophically grounded. This is one
of the reasons why the ontological analysis preceding modeling is of paramount importance. A careful choice and characterization of categories and relations produces indeed ontologies that have higher
chances of being interoperable, or at least of understanding potential obstacles to interoperability. In particular, when this strategy is applied to foundational ontologies, interoperability is possible also between
the domain ontologies aligned to them.
From a philosophical perspective, DOLCE adopts a descriptive (rather than referentialist) metaphysics,
as its main purpose is to make explicit already existing conceptualizations through the use of categories
whose structure is influenced by natural language, the makeup of human cognition, and social practices. As a consequence, such categories are mostly situated at a mesoscopic level, and may change
while scientific knowledge or social consensus evolve. Also, DOLCE’s domain of discourse is formed by
particulars, while properties and relations are taken to be universals.


1
This paper is a presentation of DOLCE based on (Masolo et al., 2003) and experience acquired with its application.
[*Corresponding author. E-mail: stefano.borgo@cnr.it.](mailto:stefano.borgo@cnr.it)
2http://www.loa.istc.cnr.it/index.php/dolce/


1570-5838/$35.00 © 0 – IOS Press and the authors. All rights reserved


2 _S. Borgo et al. / DOLCE_


Once the intended meaning of the terms denoting the relevant ontology categories has been analyzed,
it should be expressed in a way that is as semantically transparent as possible. To this aim, DOLCE is
equipped with a rich axiomatization in first-order modal logic. Such richness greatly enhances expressiveness but, on the other hand, it makes foundational ontologies non computable, due to the well-known
trade-off between formal expressiveness and computability. For this reason, approximated and partial
translations expressed in application-oriented languages are often provided, as is the case for DOLCE. [3]


_A bit of history of_ DOLCE


The first comprehensive presentation of DOLCE appeared in the deliverables of the WonderWeb project
in the early 2000s and in particular (Masolo et al., 2003). Following this work, several applicationoriented, “lite” versions were later published, including DOLCE-lite, DOLCE-ultralite, and DOLCE-zero
(Paulheim and Gangemi, 2015), see (Presutti and Gangemi, 2016) for a summary, and widely used (see
also Sect. 4). The present article is mainly based on the work of Masolo et al. (2003) with the addition
of concepts, e.g. roles, as introduced by Borgo and Masolo (2009).
The analysis underlying the formalization of DOLCE leverages the techniques of ontological engineering and the study of classes’ meta-properties of the OntoClean methodology, firstly developed in the
early 2000s by Guarino and Welty (2002) and later revised by Guarino and Welty (2009) and Guarino
(2009).
A later work presented by Masolo et al. (2004) introduced social roles and concepts within DOLCE
through a reification pattern, allowing in this way to introduce them as particulars into the domain of
discourse.
In 2009, DOLCE-CORE was introduced in Borgo and Masolo (2009). The main purpose behind this
work was that of simplifying the whole system, making it more usable in applications, and at the same
time acceptable under different philosophical stands. Such simplification was also intended to facilitate
the task of further extending the ontology. In particular, some of the changes introduced by DOLCE-CORE
are: the adoption of the notion of concept as an ontology category, a better explanation on how to distinguish and formalize properties, the formalization of the notion of resemblance to facilitate the use
of qualities, and the possibility of having more quality spaces associated to the same quality. Further
changes include the definition of different parthood relations depending on ontological categories, the
introduction of a notion of time regularity, and a simplification concerning the most basic categories,
which in DOLCE were called ‘endurant’ and ‘perdurant’ and which become ‘object’ and ‘event’ in
DOLCE-CORE and can be distinguished based on whether they have space or time as main dimension,
respectively.
Leaving aside these theoretical studies, DOLCE has remained fixed over the years fulfilling the purpose
of top-level ontologies to provide a solid and stable basis for modeling different domains, in this way
ensuring interoperability of reference and domain ontologies that use DOLCE. Through the years, DOLCE
has been enriched with modules to extend and specialize it. These modules facilitate the application and
coherent use of the ontology. Some extensions tackle knowledge representation’s specific issues, like the
modeling of roles by Masolo et al. (2004), of artifacts by Vieu et al. (2008) and by Borgo et al. (2014),
and of modules by Ferrario and Porello (2015). Others showed a possible integration with machine
learning and in particular computer vision (Conigliaro et al., 2017). Extensions to the modeling of social


3Given the emphasis on formal expressivity, recall that foundational ontologies are not directly used for applications; rather,
they provide _conceptual handles_ to solve cases of misunderstandings due to the limitations of expressiveness of the application
languages.


_S. Borgo et al. / DOLCE_ 3


(Bottazzi and Ferrario, 2009; Porello et al., 2013, 2014a) and cognitive aspects (Ferrario and Oltramari,
2004; Biccheri et al., 2020) have also been proposed. Today DOLCE is becoming part of the ISO 21838
standard, under development, and is available also in CLIF, a syntax of Common Logic ISO 24707
(2018). [4]


The remaining of the paper is organized as follows: section 1 introduces the most fundamental categories and relations of DOLCE, which are axiomatized in section 2. With the aim of enhancing understanding, section 3 shows the application of DOLCE’s axioms to five modeling examples. Before looking
at the structure of the ontology, we shall spend some words on its history.


**1. Principles and structure of DOLCE**


As depicted in the taxonomy in Figure 1, the basic categories of DOLCE are endurant (aka continuant),
perdurant (occurrent), quality, and abstract.


Fig. 1. The taxonomy of DOLCE extended with the subcategories _Concept_, _Role_, and _Artefact_ .


_I. Continuant vs. occurrent.._ The distinction between endurants and perdurants is inspired by the philosophical debate about change in time. In particular, while endurants may acquire and lose properties and
parts through time, perdurants are fixed in time. Their fundamental difference concerns therefore their
presence in time: endurants are wholly present (i.e., with all their parts) at any time in which they are
present; differently, perdurants can be partially present, so that at any time in which they unfold only a
part of them is present. Examples of endurants are a table, a person, a cat, or a planet, while examples of
perdurants are a tennis match, a conference talk or a manufacturing process producing a certain item.
The relation connecting endurants and perdurants is called _participation_ . An endurant can _be_ in time
by participating in a perdurant, and perdurants _happen_ in time by having endurants as participants. For
instance, a person is in time by participating to her own life, and a conference talk happens if at least
one presenter (or attendant) participates to it.


4
[DOLCE in CLIF, OWL etc. can be found at http://www.loa.istc.cnr.it/index.php/dolce/ together with additional papers and](http://www.loa.istc.cnr.it/index.php/dolce/)
materials.


4 _S. Borgo et al. / DOLCE_


_II. Independent vs. dependent entity.._ This distinction is found across the entire taxonomy of DOLCE.
For instance, features (e.g., edges, holes, bumps, etc.) are endurants whose existence depends on some
physical object (the feature bearer), while physical objects are independent entities, i.e., their existence
does not require other endurants to exist. Note that if we take a notion of cross-categorical dependence,
only abstract entities turn out to be independent in DOLCE. For instance, since a physical object necessarily participates in an event (namely, its life), every physical object requires the existence of at least
one event (and vice versa).


_III. Processes vs. events.._ In DOLCE processes and events are special types of perdurants. As it can
be seen from Figure 1, DOLCE covers various classes of perdurant following taxonomic distinctions
found in both philosophy and linguistics. In particular, a perdurant(-type) is stative or eventive according to whether it holds of the mereological sum of two of its instances, i.e. if it is cumulative or not.
Common examples of stative perdurants are states; e.g., a sitting state is stative because the sum of
two sittings is still a sitting. Among stative perdurants, processes are cumulative but not homeomeric,
namely, they have parts of different types; e.g., there are (even very short) temporal parts of a running
that are not themselves runnings. Finally, eventive occurrences (events) are not cumulative, and they are
called achievements if they are atomic, otherwise they are accomplishments. [5]


_IV. Properties, qualities, quantities.._ DOLCE covers these entities through the general notion of quality. [6]

Qualities are, roughly speaking, what can be perceived and measured; they are particulars inhering in
endurants or perdurants. For example, when we talk about the red of a rose, we are talking about a
particular quality (that specific red) which inheres in a particular endurant (that specific rose). See also
Section 3.3.1. Qualities are therefore specific to their bearers (this is why they are called _individual_
_qualities_ in DOLCE), and they are present at each time in which their bearers are present. Depending on
the entities in which they inhere (qualities are dependent entities indeed), DOLCE identifies qualities of
different types, namely, physical, temporal or abstract qualities. Moreover, since complex qualities can
have qualities themselves, DOLCE includes a notion of direct quality to distinguish qualities of endurants,
perdurants and abstracts, from qualities of qualities.
To compare qualities of the same kind, e.g., the color of a rose and the color of a book cover, the
category of _quale_ is introduced. A quale is the position occupied by an individual quality within a quality
space. [7] In our example, if the rose and the book cover exhibit the same shade of red, their individual
colors occupy the same position (quale) in the color space. Hence, the two qualities are distinct but they
have the same quale (within the same color space).


_V. Function and Role.._ DOLCE does not formalize functions and roles, although these have been widely
investigated and represented in DOLCE-driven approaches (Borgo et al., 2010; Masolo et al., 2004). Roles
are represented as (social) concepts, which are connected to other entities (like endurants, perdurants,
and abstracts) by the relation of _classification_ . In particular, roles are concepts that are anti-rigid and
founded, meaning that (i) they have dynamic properties [8] and (ii) they have a relational nature, i.e. they
depend on other roles and on contexts.


5
As said in the Introduction, endurants are called ‘objects’, and perdurants ‘events’ in DOLCE-CORE. This terminological
difference is due to changes in the formalization of the ontology even though the two systems largely overlap.
6Recall that ‘property’ is generally used in analytic metaphysics as something which can be instantiated. We treat property
here in a more restricted sense; informally, as synonym of ‘characteristic’ or ‘attribute’.
7
Quality spaces in DOLCE are based on Gärdenfors’ conceptual spaces (Gärdenfors, 2000).
8For instance, each role can be played by different entities at the same or at different times, the same entity can play a role at
different times or discontinuously, or it can play different roles at the same or at different times.


_S. Borgo et al. / DOLCE_ 5


_VI. Relations.._ An important relation in DOLCE is _parthood_, which is time-indexed when connecting
endurants and a-temporal when holding between perdurants or abstracts, i.e. between entities that do
not change in time. _Constitution_ is another temporalized relation in DOLCE, holding between either
endurants or perdurants. It is often used to single out entities that are spatio-temporally co-located but
nonetheless distinguishable for their histories, persistence conditions, or relational properties. A typical
example of constitution is the relation between a statue and the amount of matter it is built with. The
former started to exist at a later moment with respect to the latter; the latter can survive the destruction
of the former and only for the former the existence of a sculptor is a necessary condition of existence.


The last basic category of the ontology is that of abstracts. These are entities that have neither spatial
nor temporal qualities and are not qualities themselves. We will not deal with them in the current paper,
so it should suffice to give a few examples: quality regions (and therefore also quality spaces), sets, and
facts. Also, although DOLCE has other important categories and relations, in the present paper we will
focus especially on those just presented, as they will be discussed in the following in the light of their
axiomatization and used for the formalization of the cases in Section 3.


**2. The formalization of DOLCE in First-Order Logic**


The formal theory of DOLCE is written in the first-order quantified modal logic QS5, including the
Barcan and the converse Barcan formula, cf. (Fitting and Mendelsohn, 2012). These assumptions entail
a _possibilistic_ view of the entities: the domain of quantification contains all possible entities, regardless
of their actual existence.
Here we present an excerpt of the axiomatization, focusing on the axioms required for the subsequent
examples, that provides a general view of the DOLCE approach. An exhaustive presentation of DOLCE
was given by Masolo et al. (2003) and a proof of consistency was provided by Kutz and Mossakowski
(2011). In the following paragraphs, next to each axiom and definition we report the label of that formula
in the primary presentation, cf. (Masolo et al., 2003). DOLCE is here extended to include the category
of Concepts (C) and Roles (RL) and the relation of classification (CF), as we shall see below; their
formalization is taken from (Masolo et al., 2004). [9]


_2.1. Taxonomy_


As said, the taxonomy of DOLCE is shown in Figure 1. We omit in the following the taxonomic axioms
which can be found in (Masolo et al., 2003). With respect to the original version, we include in this paper
the categories _Concept_ and _Role_ as specializations of Non-Agentive Social Object, and the category
_Artefact_ as specialization of Non-Agentive Physical Object. These will be used in the formalization of
the examples.


_2.2. Mereology_


DOLCE assumes two primitive parthood relations: atemporal (P( _x_, _y_ ) for ‘ _x_ is part of _y_ ’) and timedependent (P( _x_, _y_, _t_ ) for ‘ _x_ is part of _y_ at time _t_ ’) parthood. The same predicate symbol P is used for


9A CLIF version of DOLCE plus the theory of concepts and roles from (Masolo et al., 2004) is formalized and proved
[consistent by means of Mace4. The theory the proof of consistency and further material can be downloaded at http://www.loa.](http://www.loa.istc.cnr.it/index.php/dolce/)
[istc.cnr.it/index.php/dolce/](http://www.loa.istc.cnr.it/index.php/dolce/)


6 _S. Borgo et al. / DOLCE_


both relations. The first follows the principles of the General Extensional Mereology (GEM), whereas
temporary parthood drops the antisymmetry axioms, cf. (Masolo et al., 2003, p.33).
Here we give some axioms and definitions relative to temporary parthood, which we will use in Section
3.1 (in the rest of this section Dd _n_ and Ad _n_ are the labels of definitions and axioms, respectively, used
in (Masolo et al., 2003)). In the formulas, PRE( _x_, _t_ ) reads ‘ _x_ is present at time _t_ ’; PP( _x_, _y_, _t_ ) reads ‘ _x_ is
a proper part of _y_ at _t_ ’ and O( _x_, _y_, _t_ ) reads ‘ _x_ and _y_ overlap at time _t_ ’. The expression _x_ + _te y_ reads ‘the
temporary sum of _x_ and _y_ ’, and σ _tex_ ϕ( _x_ ) reads ‘the termporary fusion of each _x_ that satisfies ϕ’. After
the formulas we give a description in natural language.


**a1** P( _x_, _y_, _t_ ) _→_ ED( _x_ ) _∧_ ED( _y_ ) _∧_ T( _t_ ) ( _Temporary part typing_, cf. Ad10)
**a2** P( _x_, _y_, _t_ ) _→_ PRE( _x_, _t_ ) _∧_ PRE( _y_, _t_ ) (cf. Ad17)

_de f_
**d1** PP( _x_, _y_, _t_ ) = P( _x_, _y_, _t_ ) _∧¬_ P( _y_, _x_, _t_ ) ( _Temporary proper part_, cf. Dd20)

_de f_
**d2** O( _x_, _y_, _t_ ) = _∃z_ (P( _z_, _x_, _t_ ) _∧_ P( _z_, _y_, _t_ )) ( _Temporary Overlap_, cf. Dd21)

_de f_
**d3** _x_ + _te y_ = ι _z∀w_, _t_ (O( _w_, _z_, _t_ ) _↔_ (O( _w_, _x_, _t_ ) _∨_ O( _w_, _y_, _t_ ))) ( _Temporary binary sum_, cf. Dd26)

_de f_
**d4** σ _tex_ ϕ( _x_ ) = ι _z∀y_, _t_ (O( _y_, _z_, _t_ ) _↔∃w_ (ϕ( _w_ ) _∧_ O( _y_, _w_, _t_ ))) ( _Temporary sum_, cf. Dd27)


Axiom (a1) states that temporary parthood holds only between two endurants at some time, axiom (a2)
states that to have a parthood relationship both the part and the whole must be present, while (d1) states
that a proper part is any part which does not contain the whole itself. (d2) defines overlap as a relation
that holds on a pair of entities at the time when they have a common part. Using overlap, one can define
binary and unrestricted sums, see cf. (d3) and (d4). These definitions characterize new entities: the sum
of two entities and the fusion (sum of possibly infinite entities) of all the entities that satisfy a given
formula ϕ, where ϕ does not contain time variables. Finally, note that in DOLCE sum (fusion) is defined
also on events and on abstracts, thus including the sum (fusion) of times. We do not report these latter
definitions since they are standard (cf. Dd18 and Dd19). We use the same notation (+ and σ) for sum
and fusion with or without the temporal parameter depending on the entities to which it applies.


_2.3. Quality and quale_


The relation _being a quality of_ (qt) is primitive in DOLCE. Its full characterization is in (Masolo et al.,
2003, p.35). To be able to say that ‘ _x_ is a quality of _y_ of type ϕ’ we extend it relatively to a type as
follows:


_de f_
**d5** qt(ϕ, _x_, _y_ ) = qt( _x_, _y_ ) _∧_ ϕ( _x_ ) _∧_ SBL _X_ ( _Q_, ϕ) ( _Quality of type_ ϕ, cf. Dd29)


where SBL _X_ ( _Q_, ϕ) is an abbreviation for the statement that ϕ is a leaf in the DOLCE hierarchy of qualities
(i.e. it is a minimal category in the quality branch of Fig.1, cf. (Masolo et al., 2003, p.27)).
Then, DOLCE defines the temporal _quale_ (relation ql), i.e., the position occupied by an individual
quality within a quality space, as follows (recall that TL is the temporal location category, see Fig.1):


_de f_
**d6** ql _T_, _PD_ ( _t_, _x_ ) = PD( _x_ ) _∧∃z_ (qt(TL, _z_, _x_ ) _∧_ ql( _t_, _z_ )) ( _Temporal quale of perdurants_, cf. Dd30)

_de f_
**d7** ql _T_, _ED_ ( _t_, _x_ ) = ED( _x_ ) _∧_ _t_ = σ _t_ _[′]_ ( _∃y_ (PC( _x_, _y_, _t_ _[′]_ )) ( _Temporal quale of endurants_, cf. Dd31)

_de f_
**d8** ql _T_ ( _t_, _x_ ) = ql _T_, _ED_ ( _t_, _x_ ) _∨_ ql _T_, _PD_ ( _t_, _x_ ) _∨_ ql _T_, _Q_ ( _t_, _x_ ) ( _Temporal Quale_, cf. Dd35)


From (d6) the temporal quale of a perdurant is the quale associated to the time location quality (TL) of
the perdurant, and from (d7) the temporal quale of an endurant is the sum of all the times during which


_S. Borgo et al. / DOLCE_ 7


the endurant participates (PC) to some perdurant. (The _participation_ relation is formally introduced
below.) The temporal quale of a quality (ql _T_, _Q_ ) is defined in a similar way (Masolo et al., 2003, p.28).
Finally, the temporal quale of an entity is given by the collection of all the previous definitions, (d8).
Qualities are classified in DOLCE as physical, temporal, and abstract qualities as stated below where
the formulas add that a quality inheres in one and only one entity (qt( _x_, _y_ ) reads ‘ _x_ is a quality of _y_ ’):


**a3** PQ( _x_ ) _→∃_ ! _y_ (qt( _x_, _y_ ) _∧_ PED( _x_ )) ( _Physical quality_, cf. Ad47)
**a4** TQ( _x_ ) _→∃_ ! _y_ (qt( _x_, _y_ ) _∧_ PD( _x_ )) ( _Temporal quality_, cf. Ad46)
**a5** AQ( _x_ ) _→∃_ ! _y_ (qt( _x_, _y_ ) _∧_ NPED( _x_ )) ( _Abstract quality_, cf. Ad48)


_2.4. Time and existence_


Actual existence in DOLCE is represented by means of the _being present at_ (PRE) relation. The assumption here is that things exist if they have a temporal quale.


_de f_
**d9** PRE( _x_, _t_ ) = _∃t_ _[′]_ (ql _T_ ( _t_ _[′]_, _x_ ) _∧_ P( _t_, _t_ _[′]_ )) ( _Being Present at t_, cf. Dd40)


Further properties of PRE are described in (Masolo et al., 2003), Section 4.3.8.


_2.5. Participation_


The participation (PC) relation connects endurants, perdurants, and times, i.e. endurants _participate_
in perdurants at a certain time (a6). Here we write PC( _x_, _y_, _t_ ) for ‘ _x_ participates in _y_ at time _t_ ’. (a7)
states that a perdurant has at least one participant and (a8) that an endurant participates in at least one
perdurant. Axiom (a9) says that for an endurant to participate in a perdurant they must be present at the
same time. We also introduce the relation of constant participation (PCC), cf. (d10), i.e., participation
during the whole perdurant, which we will use in sections 3.4 and 3.5.


**a6** PC( _x_, _y_, _t_ ) _→_ ED( _x_ ) _∧_ PD( _y_ ) _∧_ T( _t_ ) ( _Participation typing_, cf. Ad33)
**a7** PD( _x_ ) _∧_ PRE( _x_, _t_ ) _→∃y_ (PC( _y_, _x_, _t_ )) (cf. Ad34)
**a8** ED( _x_ ) _→∃y_, _t_ (PC( _x_, _y_, _t_ )) (cf. Ad35)
**a9** PC( _x_, _y_, _t_ ) _→_ PRE( _x_, _t_ ) _∧_ PRE( _y_, _t_ ) (cf. Ad36)


_de f_
**a10** PCC( _x_, _y_ ) = _∃t_ (PRE( _y_, _t_ )) _∧∀t_ (PRE( _y_, _t_ ) _→_ PC( _x_, _y_, _t_ )) ( _Const. Participation_, cf. Dd63)


_2.6. Constitution_


The constitution relation K is mainly used here to model the scenario in Section 3.1. We report only a
few axioms required to model the scenario (K( _x_, _y_, _t_ ) reads ‘ _x_ constitutes _y_ at time _t_ ’).


**a11** K( _x_, _y_, _t_ ) _→_ ((ED( _x_ ) _∨_ PD( _x_ )) _∧_ (ED( _y_ ) _∨_ PD( _y_ )) _∧_ T( _t_ )) ( _Constitution typing_, cf. Ad20)
**a12** K( _x_, _y_, _t_ ) _→_ (PED( _x_ ) _↔_ PED( _y_ )) (cf. Ad21)
**a13** K( _x_, _y_, _t_ ) _→¬_ K( _y_, _x_, _t_ ) (cf. Ad24)


(a11) states that K applies to pairs of endurants or of perdurants and a time. (a12) states that only
physical endurants can constitute another physical endurant. (a13) states that constitution is asymmetric.


8 _S. Borgo et al. / DOLCE_


_2.7. Concepts, roles, and classification_


As anticipated, the relation of classification (CF) is not in (Masolo et al., 2003) as it applies to the
category _Concept_ (C), and to its subcategories including _Role_ (RL), which informally collects particulars
that classify, as introduced in (Masolo et al., 2004). We thus take the following axioms from the latter
work (CF( _x_, _y_, _t_ ) stands for ‘at the time _t_, _x_ is classified by the concept _y_ ’):


**a14** CF( _x_, _y_, _t_ ) _→_ ED( _x_ ) _∧_ C( _y_ ) _∧_ T( _t_ ) (cf. A11 in (Masolo et al., 2004) [10] )
**a15** CF( _x_, _y_, _t_ ) _→_ PRE( _x_, _t_ ) (cf. A12 in (Masolo et al., 2004))
**a16** CF( _x_, _y_, _t_ ) _→¬_ CF( _y_, _x_, _t_ ) (cf. A14 in (Masolo et al., 2004))
**a17** CF( _x_, _y_, _t_ ) _∧_ CF( _y_, _z_, _t_ ) _→¬_ CF( _x_, _z_, _t_ ) (cf. A15 in (Masolo et al., 2004))


_de f_
**d10** AR( _x_ ) = _∀y_, _t_ (CF( _x_, _y_, _t_ ) _→∃t_ _[′]_ (PRE( _x_, _t_ _[′]_ ) _∧¬_ CF( _x_, _y_, _t_ _[′]_ )) (cf. D1 in (Masolo et al., 2004))


_de f_
**d11** RL( _x_ ) = AR( _x_ ) _∧_ FD( _x_ ) (cf. D3 in (Masolo et al., 2004))


The classification relationship CF applies to an endurant, a concept and a time (a14), requires the
endurant to be present when it is classified (a15), and is not symmetrical (a16). A concept can classify
other concepts but not what the latter classify, this is stated to avoid circularity (a17). Roles (RL) are
defined as concepts that are _anti-rigid_ (d10) and _founded_ (d11). Informally, the foundation property
(FD) holds for a concept that is defined by means of another concept such that the instances of the latter
are all external to (not part of) the instances of the former (Masolo et al., 2004).


**3. Analysis and formalization in DOLCE: examples**


We present in the following sections how to formalize the five given cases according to DOLCE. Since to
model some cases it is helpful to use a temporal ordering relation and since DOLCE does not formalize
any, we introduce one here as follows: ‘<’ is an ordering relation over atomic and convex regions of time
(usually, these are understood as time instants and time intervals) such that if _t_ 1 < _t_ 2 holds, then _t_ 1 and
_t_ 2 are ordered and non overlapping, i.e., _¬_ O( _t_ 1, _t_ 2). We write _t_ 1 ⩽ _t_ 2 to mean that _t_ 1 and _t_ 2 are ordered,
may properly overlap (i.e., they overlap but none is completely included in the other), and, given _t_ their
overlapping region, then _t_ 1 _−_ _t_ < _t_ 2 _−_ _t_ holds.


_3.1._ _Case 1: Composition/Constitution_


“There is a four-legged table made of wood. Some time later, a leg of the table is
replaced. Even later, the table is demolished so it ceases to exist although the wood
is still there after the demolition.”


DOLCE provides two ways to model this and similar examples. The first option, which we call _artifact-_
_based_ and we follow here, considers entities like tables and legs as ontological entities on their own
because of their artifactual status, namely, the fact that tables and the legs are intentionally produced
products. The second option, called _role-based_, considers table and leg as roles of objects. In this view,
indeed, some objects play the role of table and leg in a given context but not necessarily. We do not


10Note that Masolo et al. (2004) apply classification only to endurants, though the possibility of applying it also to perdurants
and abstracts was mentioned. Here we allow concepts to classify also perdurants as done in Section 3.4


_S. Borgo et al. / DOLCE_ 9


use this second modeling approach for Case 1 and exemplify it for Case 2 (see next section) where the
adoption of the role perspective is more natural. Note that DOLCE is neutral with respect to the choice
between these two modeling approaches: it entirely depends on what one takes as essential properties of
an entity, that is, how one answers the question: is ‘being a table’ an essential property for that object
or is it only an accidental condition? In this way, by using DOLCE, the knowledge engineer is free to
choose the option that best matches their modeling purposes and application concerns.


Tables and legs are objects whose kinds provide criteria for their persistence in time. We shall assume
that a table remains the same object whenever it has a suitable shape and the right functionalities, even
though some of its legs may be substituted. For simplicity, let us assume that a table is identified by a
tabletop, i.e., no matter what happens, a table remains the same entity provided that its tabletop is not
substituted or destroyed. Clearly, when a leg is substituted, the quantity of wood that constitutes the
table changes. It follows that the existence of the table does not imply that it is made of the same matter
throughout its whole life. Allowing the possibility that some entities keep existing while some of their
parts change (or even cease to exist) is a design characteristic of DOLCE. More precisely, the ontology
allows distinguishing between quantities of matter (e.g., the wood of which a table is made), the object
constituted by the matter (that object made of that wood), and the artifact (the table, i.e., the functional
object (Mizoguchi et al., 2016)).
The constitution and composition relations in DOLCE capture distinct forms of dependence: the former
is the dependence holding between entities with different essential properties (intercategorical) like the
dependence of a table from the matter it is made of; the latter holds between entities with the same
essential properties (intracategorical) like the dependence of a table from the tabletop and the legs.
It follows that constitution connects elements belonging to distinct categories and that are related by
an existential co-temporal dependence. Here, it holds between elements of the category Matter (the
considered amount of wood) and elements of the category Physical Object (the object made of that
wood), since a material object exists at time _t_ only if there exists at _t_ a quantity of matter that constitutes
it. The composition relation (expressed in DOLCE by parthood restricted to the category at stake) holds
instead among elements of the same category which are bound to form a more complex element. These
are generally called composing parts or _components_ . In this case, composition implies that the existence
of the composed object requires the co-temporal existence of its composing objects.


The DOLCE categories that we use for the artifact-based modeling of this case are: matter (M), physical
object (POB), and Time (T). We will also use the Artefact category, as introduced by Borgo and Vieu
(2009) and two new subclasses of it introduced specifically for this scenario, i.e., Table and TableLeg. [11]

In terms of relations we use: _being subclass_ (IS_A), _parthood_ (P), _constitution_ (K) and _being present_
(PRE). We also use the _sum_ operator (+), and the order relation (<) for time.
Figure 2 depicts the portion of the DOLCE taxonomy and relationships considered in this case. For the
sake of simplicity, relationships like parthood (P) and constitution (K) are restricted in the figure to the
classes relevant for the representation of the example. Also, in all figures, ternary relations are shown in
a simplified manner (e.g., K at _t_ ).


Formally, Case 1 can be expressed as follows.


11One could avoid the use of the Artefact category and treat table and leg as mere objects. However, the introduction of
domain-driven categories at intermediate layers, e.g. Artefact, is considered good practice in applications.


10 _S. Borgo et al. / DOLCE_


Fig. 2. Fragment of the DOLCE taxonomy and relevant relationships for Case 1.


Taxonomic claims:


_Artefact_ ( _x_ ) _→_ POB( _x_ ) (1)


_Table_ ( _x_ ) _→_ _Artefact_ ( _x_ ) (2)


_Tabletop_ ( _x_ ) _→_ _Artefact_ ( _x_ ) (3)


_Leg_ ( _x_ ) _→_ _Artefact_ ( _x_ ) (4)


_Wood_ ( _x_ ) _→_ M( _x_ ) (5)


The previous formulas state that an artifact is a physical object, that table, tabletop and the legs are
artifacts, and that wood is matter. Formula (6) represents the elements and the temporal constraints ( _L_ 1 _′_
and _W_ 1 _′_ are the elements which are substituted for the original table parts).




      _Table_ ( _T_ ) _∧_ _Tabletop_ ( _T p_ ) _∧_




- 
_Leg_ ( _Li_ ) _∧_ _Leg_ ( _L_ 4 _′_ ) _∧_ _Wood_ ( _Wtop_ ) _∧_

1⩽ _i_ ⩽4 1⩽ _i_



_Wood_ ( _Wi_ ) _∧_

1⩽ _i_ ⩽4



_Wood_ ( _W_ 4 _′_ ) _∧_ T( _t_ ) _∧_ T( _t_ _[′]_ ) _∧_ T( _t_ _[′′]_ ) _∧_ _t_ < _t_ _[′]_ _∧_ _t_ _[′]_ < _t_ _[′′]_ (6)


The formula above states that _T_ is a table; _Li_ are legs and so is _L_ 1 _′_ ; _Wtop_ is an amount of wood and so
are _Wi_ and _W_ 1 _′_ (informally, these are the amounts of wood of which the tabletop, the legs, and the new
leg are made of, respectively); _t_, _t_ _[′]_, and _t_ _[′′]_ are temporal instants or intervals such that _t_ is earlier than _t_ _[′]_

and _t_ _[′]_ is earlier than _t_ _[′′]_ .


_S. Borgo et al. / DOLCE_ 11



Stating the elements’ presence:




          PRE( _T_, _t_ ) _∧_ PRE( _T_, _t_ _[′]_ ) _∧_ PRE( _T p_, _t_ ) _∧_ PRE( _T p_, _t_ _[′]_ ) _∧_





PRE( _Li_, _t_ _[′]_ ) _∧_

1⩽ _i_ ⩽3




- 
PRE( _Li_, _t_ ) _∧_

1⩽ _i_ ⩽4 1⩽ _i_




   PRE( _L_ 4 _′_, _t_ _[′]_ ) _∧_




- 
PRE( _Wi_, _t_ _[′]_ ) _∧_ PRE( _W_ 4 _′_, _t_ _[′]_ ) _∧_

1⩽ _i_ ⩽3 1⩽ _i_




 - 
PRE( _Wi_, _t_ ) _∧_

1⩽ _i_ ⩽4 1⩽ _i_





PRE( _Wi_, _t_ _[′′]_ )

1⩽ _i_ ⩽3




      _∧_ PRE( _W_ 4 _′_, _t_ _[′′]_ ) _∧¬_ PRE( _T_, _t_ _[′′]_ ) _∧_ _¬_ PRE( _Li_, _t_ _[′′]_ ) _∧¬_ PRE( _L_ 4 _′_, _t_ _[′′]_ ) (7)


1⩽ _i_ ⩽3



Formula (7) states that the table _T_ is present at _t_ and _t_ _[′]_ ; the legs _Li_ are present at _t_ and _t_ _[′]_ except for _L_ 4
which is not present at _t_ _[′]_ ; _L_ 4 _′_ is present at _t_ _[′]_ ; _Wtop_ and _Wi_ are present at _t_, _t_ _[′]_ and _t_ _[′′]_ except _W_ 4 for which
nothing is said about _t_ _[′]_ and _t_ _[′′]_ ; _W_ 4 _′_ is present at _t_ _[′]_ and _t_ _[′′]_ .


Relational claims:




    P( _T p_, _T_, _t_ + _t_ _[′]_ ) _∧_




- 
P( _Li_, _T_, _t_ ) _∧_

1⩽ _i_ ⩽4 1⩽ _i_





P( _Li_, _T_, _t_ _[′]_ ) _∧_ P( _L_ 4 _′_, _T_, _t_ _[′]_ ) _∧¬_ P( _L_ 4, _T_, _t_ _[′]_ ) _∧_

1⩽ _i_ ⩽3




- 
K( _Wi_, _Li_, _t_ ) _∧_

1⩽ _i_ ⩽4 1⩽ _i_




    K( _Wtop_, _T p_, _t_ + _t_ _[′]_ ) _∧_





K( _Wi_, _Li_, _t_ _[′]_ ) _∧_ K( _W_ 4 _′_, _L_ 4 _′_, _t_ _[′]_ ) (8)

1⩽ _i_ ⩽3



Formula (8) states that the tabletop _T p_ is component of the table _T_ at _t_ and _t_ _[′]_ ; the legs _Li_ are components of _T_ at _t_ ; the legs _L_ 1, _L_ 2, _L_ 3 and _L_ 4 _′_ are components of _T_ at _t_ _[′]_ ; _Wtop_ and _W_ 1, _W_ 2, _W_ 3 are constituents
of the tabletop and legs (respectively) at _t_ and _t_ _[′]_ ; _W_ 4 is a constituent of _L_ 4 at _t_ ; _W_ 4 _′_ is a constituent of _L_ 4 _′_
at _t_ _[′]_ .
Since constitution is transitive and distributes over parthood, it follows that the table _T_ is constituted
by the sum of _Wtop_, _W_ 1, _W_ 2, _W_ 3 and _W_ 4 at _t_, and by that of _Wtop_, _W_ 1, _W_ 2, _W_ 3 and _W_ 4 _′_ at _t_ _[′]_ .


The modeling presented above is mainly focused on objects: the table as a whole and the legs and
tabletop as its components. In this view, the perdurants during which the table changes are not modeled. In DOLCE one can explicitly introduce such perdurants, like the replacement and the demolition
accomplishments. This second approach would make explicit the modeling of how and why the changes
happen. The two views can be integrated in a single model since the essential relationships between the
whole, its components and the material they are made of remain unchanged. Other modeling views, like
the functional or the role-based modelings, are also possible in DOLCE.


_3.2._ _Case 2: Roles_


“Mr. Potter is the teacher of class 2C at Shapism School and resigns at the beginning
of the spring break. After the spring break, Mrs. Bumblebee replaces Mr. Potter as
the teacher of 2C. Also, student Mary left the class at the beginning of the break and
a new student, John, joins in when the break ends.”


This case requires to model social roles, thus we follow the _role-based_ modeling approach briefly
mentioned in discussing Case 1. Roles are properties that an entity can have temporarily (roles can be
acquired and lost at will), and they depend on an external entity, often indicated as the context, which


12 _S. Borgo et al. / DOLCE_


(perhaps implicitly) defines them. In this example, the role of student and teacher are defined within a
school system, which we shall assume to stand for the context of the example.
To model Case 2, we need four instances of Person, namely Mr. Potter, Mrs. Bumblebee, Mary, and
John, as well as two instances of Object, namely, class 2C and Shapism School. [12]

At first, say at time _t_ 1, we have that Mr. Potter has the role of _teacher_ (at the Shapism School’s class
2C), technically writing that such role property holds for Mr. Potter at _t_ 1. At the same time, _t_ 1, the
property does not hold for Mrs. Bumblebee. During the spring break period, say at _t_ 2, the property holds
for neither, even though the role property continues to exist, since the entities that define it (the Shapism
School and the Shapism School’s class 2C) continue to exist during the break. After the spring break, at
_t_ 3, Mrs. Bumblebee has the (Shapism School’s class 2C) teacher role and Mr. Potter has not. The role
teacher is played by a person at _t_ 1, by nobody at _t_ 2, and by another person at _t_ 3. The Shapism School’s
class 2C teacher role exists and does not change during the whole period. Since the teacher role can be
played by one person at a time, usually one says that Mrs. Bumblebee replaced Mr Potter in that teacher
role.
Similarly, at first Mary has the _student_ role (at the Shapism School’s class 2C) and John has not. Only
the persons who are students before the break and do not leave the class have the student role during
the break. Those people, now including John, have the Shapism School’s class 2C student role after the
break. In this case, however, one cannot say that John substituted Mary since, differently from teacher
roles, which are characterized by individual rights and duties (an English teacher and a math teacher
must satisfy different requirements and have duties tailored to the discipline they are hired for), the class
2C student role does not differentiate among players.


The DOLCE categories that we need for modeling this case are: agentive physical object (APO), nonagentive social object (NASO), and Time (T). We will also use the Teacher and Student roles as specializations of the Role category (RL, a subcategory of NASO) from (Masolo et al., 2004). In terms of
relations we use: _being subclass_ (IS_A), _being present_ (PRE), _time order_ (<), _mereological sum_ (+), and
the _classify_ relation (CF) also introduced in (Masolo et al., 2004). Figure 3 depicts some relevant classes
and relationships for this case.
Formally, Case 2 can be expressed as follows.


Taxonomic claims:


_Person_ ( _x_ ) _→_ APO( _x_ ) (9)


_Funct_ RL( _x_ ) _→_ RL( _x_ ) (10)


RL( _x_ ) _→_ NASO( _x_ ) (11)


The previous formulas state that a person is an agentive physical object, a functional role is a role and
a role is a non-agentive social object.


Functional role characterization:


_Funct_ RL( _y_ ) _∧_ CF( _x_, _y_, _t_ ) _∧_ CF( _x_ _[′]_, _y_, _t_ ) _→_ _x_ = _x_ _[′]_ (12)


12For the sake of simplicity, we ignore that a school and a class are complex objects, namely, an organization and a group.
These specializations of the category Object can be modeled in DOLCE by introducing the subcategories Organization and
Group following the work of Porello et al. (2014b). Also, we do not model the ‘spring break’ in detail and limit ourselves to
see it as a generic, yet finite and temporally located, interval of time.


_S. Borgo et al. / DOLCE_ 13


Fig. 3. Fragment of the DOLCE taxonomy and relevant relationships for Case 2.


Formula (12) states that a functional role ( _y_ ) can classify only one entity at each time.


The elements and the temporal constraints:


_Person_ ( _Potter_ ) _∧_ _Person_ ( _Bumblebee_ ) _∧_ _Person_ ( _Mary_ ) _∧_ _Person_ ( _John_ ) _∧_


RL(2 _CS tudent_ ) _∧_ _Funct_ RL(2 _CTeacher_ ) _∧¬Funct_ RL(2 _CS tudent_ ) _∧_


T( _t_ 1) _∧_ T( _t_ 2) _∧_ T( _t_ 3) _∧_ _t_ 1 < _t_ 2 < _t_ 3 (13)


Formula (13) states that Potter, Bumblebee, Mary, and John are persons; that 2CTeacher and 2CStudent are roles and that the first of these is a functional role. Finally, the formula says that _ti_ are times and
indicates their ordering.


Stating the elements’ presence:


PRE( _Potter_, _t_ 1) _∧_ PRE( _Bumblebee_, _t_ 2 + _t_ 3)


PRE( _Mary_, _t_ 1) _∧_ PRE( _John_, _t_ 3) (14)


Formula (14) states that Potter, Bumblebee, Mary, and John exist at least at the listed times.


14 _S. Borgo et al. / DOLCE_


Relational claims:


_∀x ¬_ CF( _x_, 2 _CTeacher_, _t_ 2) _∧_


CF( _Potter_, 2 _CTeacher_, _t_ 1) _∧_ CF( _Bumblebee_, 2 _CTeacher_, _t_ 3) _∧_


CF( _Mary_, 2 _CS tudent_, _t_ 1) _∧¬_ CF( _John_, 2 _CS tudent_, _t_ 1) _∧_


_¬_ CF( _Mary_, 2 _CS tudent_, _t_ 2) _∧¬_ CF( _John_, 2 _CS tudent_, _t_ 2) _∧_


_¬_ CF( _Mary_, 2 _CS tudent_, _t_ 3) _∧_ CF( _John_, 2 _CS tudent_, _t_ 3) (15)


Formula (15) states that: 2CTeacher holds for nobody at _t_ 2; Potter satisfies 2CTeacher at _t_ 1 only;
Bumblebee satisfies 2CTeacher at _t_ 3 only; Mary satisfies 2CStudent at _t_ 1 only; John satisfies 2CStudent
at _t_ 3 only; neither Mary nor John satisfies 2CStudent at _t_ 2.
The model presented here is the most natural approach for this kind of scenarios in DOLCE.


_3.3. Property change_


_3.3.1._ _Case 3.1: color change_

“A flower is red in the summer. As time passes, the color changes. In autumn the
flower is brown.”


We have seen how to understand and model essential properties in Case 1 and roles (dynamic, contextual properties) in Case 2. To model Case 3.1, we use individual qualities, that is, properties as manifested
by an object. These are properties that an object must have, they are necessary for its existence. For instance, in the case of material objects, these include mass, color, and speed. Having qualities is necessary
for objects, although the value they take may change in time.


The DOLCE categories needed to model Case 3.1 are: physical object (POB), physical quality (PQ),
physical (quality) space (PR), and time (T). We will also use Flower as specialization of the POB category,
_ColorQuality_ as specialization of the PQ category, and _ColorSpace_ as specialization of the PR category.
For relations we use: _being subclass_ (IS_A), _inherence_ (qt), _being present_ (PRE), _parthood_ (P), _time_
_order_ (<), and (the relation) _quale_ (ql). Figure 4 depicts some relevant classes and relations used for
representing Case 3.1.
Formally, Case 3.1 can be expressed as follows.


Taxonomic claims:


_Flower_ ( _x_ ) _→_ POB( _x_ ) (16)


_ColorQuality_ ( _x_ ) _→_ PQ( _x_ ) (17)


_ColorSpace_ ( _x_ ) _→_ PR( _x_ ) (18)


The previous formulas state that a flower is a physical object, a color quality is a quality of physical
endurants and a color space is one of the spaces in the physical region.


The elements we need to model this case are:


_Flower_ ( _F_ ) _∧_ _ColorQuality_ ( _q_ ) _∧_ T( _S ummer_ ) _∧_ T( _Autumn_ ) _∧_ T( _t_ 0) _∧_ T( _t_ 1) (19)


_S. Borgo et al. / DOLCE_ 15


Fig. 4. Fragment of the DOLCE taxonomy and relevant relationships for Case 3.1.


Formula (19) states that _F_ is a flower, _q_ is a color quality, Summer and Autumn are times (thus, these
are not modeled as seasons in this example) and so are _t_ 0 and _t_ 1. The following formula states that the
flower _F_ is present during the Summer and the Autumn.


Stating the elements’ presence:


PRE( _F_, _S ummer_ ) _∧_ PRE( _F_, _Autumn_ ) (20)


Relational claims:


qt( _q_, _F_ ) _∧_ ql( _l_, _q_, _t_ 0) _∧_ P( _t_ 0, _S ummer_ ) _∧_ ql( _l_ _[′]_, _q_, _t_ 1) _∧_ P( _t_ 1, _Autumn_ ) _∧_

P( _l_, _RedRegion_ ) _∧_ P( _l_ _[′]_, _BrownRegion_ ) _∧_


P( _RedRegion_, _ColorS pace_ ) _∧_ P( _BrownRegion_, _ColorS pace_ ) _∧_


_S ummer_ < _Autumn_ (21)


Formula (21) states that: _q_ is the color quality of flower _F_ ; _q_ has value _l_ at time _t_ 0 in the summer and
has value _l_ _[′]_ at time _t_ 1 in the autumn where _l_ is located in the red region and _l_ _[′]_ in the brown region (both
regions in the color space). Finally, it states that Summer is before Autumn.
One can model that the flower takes all the shades from red to brown by adding the following formula (here _SC_ stands for the property of self-connected region, a property which is defined from the
connection relation _C_ in the standard way, cf. (Casati and Varzi, 1996):


_∃p_ ( _SC_ ( _p_ ) _∧_ P( _p_, _ColorS pace_ ) _∧_ P( _l_, _p_ ) _∧_ P( _l_ _[′]_, _p_ ) _∧_


_∀l_ _[∗]_ (P( _l_ _[∗]_, _p_ ) _→∃t_ (P( _t_, _S ummer_ + _Autumn_ ) _∧_ ql( _l_ _[∗]_, _q_, _t_ )))) (22)


16 _S. Borgo et al. / DOLCE_


Formula (22), combined with the earlier formulas, states that there exists a path ( _p_ ) in the space of
colors which has the given red and brown colors of the flower as endpoints, and such that the flower
takes all the colors in the path during the Summer and Autumn. In a similar way, one can also model
that the change of color has no jumps. For instance, preventing the flower from suddenly jumping from
red to light brown, then back to scarlet etc.
The model presented here follows the approach that best exploits DOLCE’s treatment of qualities.


_3.3.2._ _Case 3.2: speed change_

“A man is walking when suddenly he starts walking faster and then breaks into a
run.”
This example focuses on a change that occurs during an event. The event is divided in three parts,
in the first part the man is walking, that is, there is a movement based on a repeated regular movement
which is a process in DOLCE. In the second part, there is again a movement which is repeated at an
increasing frequency until the desired speed is reached. [13] For this reason, we model the second part
of the event as an accomplishment whose completion point is the achievement of the desired speed.
Finally, the third part is a movement based on a repeated regular movement (running) which is similar to
the first movement but with different characteristics. From this analysis, we model Case 3.2 as an event
composed of three ordered subevents.


The DOLCE categories that we need for modeling Case 3.2 are: agentive physical object (APO), process (PRO), time quality (TQ), accomplishment (ACC), quale (ql), and time (T). In terms of relations
we use: _being subclass_ (IS_A), _constant participation_ (PCC), _parthood_ (P), _quality of_ (qt), _being present_
(PRE), _time order_ (<), _mereological_ sum (+), and (the relation) _quale_ (ql). Figure 5 depicts (some of)
the classes and relationships relevant for representing Case 3.2.


Fig. 5. Fragment of the DOLCE taxonomy and relevant relationships for Case 3.2.


Formally, Case 3.2 can be expressed as follows.


13One can argue that the quality that distinguishes walking from running is not speed but how the feet touches the ground
or a combination of this and the speed quality. In these cases, the modeling approach is analogous to the one we provide here,
what changes is only the quality one considers.


_S. Borgo et al. / DOLCE_ 17


Taxonomic claims:


_Person_ ( _x_ ) _→_ APO( _x_ ) (23)


_SpeedQuality_ ( _x_ ) _→_ TQ( _x_ ) (24)


_SpeedSpace_ ( _x_ ) _→_ TR( _x_ ) (25)


_Walk_ ( _x_ ) _→_ PRO( _x_ ) (26)


_Run_ ( _x_ ) _→_ PRO( _x_ ) (27)

