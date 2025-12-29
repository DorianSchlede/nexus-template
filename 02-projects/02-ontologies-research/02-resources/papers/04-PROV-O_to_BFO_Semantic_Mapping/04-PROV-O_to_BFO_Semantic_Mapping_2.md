<!-- Source: 04-PROV-O_to_BFO_Semantic_Mapping.pdf | Chunk 2/2 -->

_qualifiedInfluence_ or PROV _influencer_, depending on whether they are the subject or object of the
influence relation, respectively. Additional properties can then be added to the PROV Influence,
such as when it occurred. For example, the RDF triple `:sortActivity prov:used :datasetA`
could be qualified as an instance of `prov:Usage` (see **Figure 6** ) and then annotated with

`prov:atTime` . Note that while we mapped terms involved with the Qualification Pattern, our
alignments are not intended to force users to adopt this pattern or reification more generally. For
representing _n_ -ary information, some alternative options are the description/situation strategy [47],
the strategy of non-rigid classification [48], and the strategy of temporally qualified continuants [49].


**Figure 6:** Illustration of a Qualified Pattern [8].

**PROV Influence**, as the superclass of 16 Qualified Influence classes, is mapped to a
subclass of the _disjoint union_ of **BFO process** and **BFO process boundary** . Some of its subclasses
such as **PROV Generation**, **PROV Start**, and **PROV End** are subsumed under **PROV**
**InstantaneousEvent**, which is equivalently mapped to **BFO process boundary** since instances of
PROV InstantaneousEvent are indivisible boundaries of some PROV Activity that is equivalent to a
BFO process. Other subclasses of PROV Influence, like **PROV Communication** and **PROV**
**Derivation**, are not subsumed under PROV InstantaneousEvent, and therefore are mapped as
subclasses of **BFO process** instead. Either way, however, no instance of a PROV Influence subclass
can be both a process and a process boundary because these classes are disjoint in BFO. See **Figure**
**2** for simplified illustrations of these mappings.


It is worth noting a radical divergence of our mapping of PROV Influence from its original
definition in PROV-O. According to its original definition,


“Influence is the capacity of an entity, activity, or agent to have an effect on the character,
development, or behavior of another by means of usage, start, end, generation, invalidation,
communication, derivation, attribution, association, or delegation.”


18


A semantic approach to mapping the Provenance Ontology to Basic Formal Ontology


In our view, PROV-O authors’ conception of influence as capacity is intended to emphasize
the dependent nature of PROV Influence. After all, a capacity, understood as a special kind of BFO
disposition, would be a BFO specifically dependent continuant since it specifically depends on some
independent continuant as its bearer. However, the dependent nature of PROV influences is better
explained by classifying these as BFO processes or process boundaries that depend on agents
through relations such as BFO _has participant_ . Given our alternative conception, a PROV Influence
may _realize_ a capacity as BFO disposition, but it is not thereby identical to that capacity, nor is
anything like this represented in any canonical PROV-O example.


Take an example from the W3C documentation, where the illustration and derivation of a
bar chart are both classified as examples of PROV Influence
[(https://www.w3.org/TR/prov-o/#hadGeneration) (see](https://www.w3.org/TR/prov-o/#hadGeneration) **Figure 7** ). Here an act of illustrating a bar
chart, when considered as a type of influence on the bar chart, clearly depends on the existence of
an illustrator. The bar chart could also be derived from some data set, and this derivation clearly
would depend on the data set. However, in both cases, it seems more appropriate to consider these
influences as _events_ occurring in time and not _capacities_ of the illustrator or data set, respectively.


**Figure 7:** Example instances of PROV Influence represented in RDF Turtle from the W3C documentation [8]. These

do not represent “capacities” of an agent but instead a specific events in time – the derivation of a bar chart and the

generation of that bar chart during an illustrating activity – which an agent may have nevertheless been causally

responsible for.

Moreover, this example provides a further reason why not all influences are capacities. Note
that some PROV influences, like the generation of a bar chart, only exist at an instant of time.
Assuming that no capacity only exists at an instant of time, then our mapping of PROV
InstantaneousEvent to BFO process boundary entails that some instances of PROV influences, such
as PROV generations, cannot be classified as capacities as BFO dispositions. This is because process
boundaries and dispositions are disjoint in BFO: the former are occurrents while the latter are
continuants.


19


A semantic approach to mapping the Provenance Ontology to Basic Formal Ontology


PROV-O further divides PROV Influence into 3 direct subclasses – **PROV**
**EntityInfluence**, **PROV ActivityInfluence**, **PROV AgentInfluence** - according to a trisection of
influencers. Since an influencer is an entity, activity, or agent, the influence it exerts is, accordingly, an
entity influence, activity influence, or agent influence. These 3 influence classes lack equivalent
mappings in BFO, but they are automatically mapped into a subclass of the disjoint union of BFO
process and BFO process boundary since they are subclasses of PROV Influence.


CCO is used to provide two additional cases of equivalent mappings. **PROV Start** is
equivalently mapped to **CCO process beginning**, while **PROV End** is equivalently mapped to
**CCO process ending** . PROV-O treats PROV Start and End as instantaneous events connected to
particular activities via the Qualification Properties PROV _qualifiedStart_ and _qualifiedEnd_, subject to
further restrictions by particular triggering entities, locations, time data, and so on. So, PROV Start
and PROV End can be mapped to CCO process beginning and CCO process ending. A process
beginning/ending is a process boundary occurring on the starting/ending instant of the temporal
period, which is occupied by a process that is equivalent to a PROV Activity.


**PROV Role** is defined as “the function of an entity or agent with respect to an activity, in
the context of a usage, generation, invalidation, association, start, and end”. Although the word
“function” is used here, BFO distinguishes between roles and functions. While a BFO function must
be partially internally determined by the physical make-up of its bearer, a BFO role could be
completely externally determined and can be gained or lost by its bearer. For example, a hammer's
function to drive nails is based on its shape, but a hammer can also play the role of a paper weight
when necessary. In light of the BFO function/role distinction, we map PROV Role directly as a
subclass of **BFO role** on the grounds that a PROV Role is externally determined by the context in
which the bearer plays the role. However, PROV Role is not equivalent to BFO role because it is
defined as existing specifically in a “context of a usage, generation, invalidation, association, start,
and end”.


The case of **PROV Plan** is more complicated. It is mapped to a subclass of **CCO**
**Information Content Entity** . According to CCO, an Information Content Entity is a BFO
generically dependent continuant (GDC) that generically depends on some CCO Information
Bearing Entity and stands in relation of aboutness to some entity [17]. It is clear that a PROV Plan is
a GDC because it may have multiple copies and thus does not have to depend on any specific
bearer. And a PROV Plan is clearly _about_ some entity in the BFO or CCO sense since it “represents a
set of actions or steps intended by one or more agents to achieve some goals” [8]. Also, given that
CCO Information Content Entity is a subclass of BFO generically dependent continuant, our CCO
mapping result implies that PROV Plan is mapped to a subclass of GDC in BFO.


However, it is worth noting that PROV Plan is not mapped to **CCO Plan**, though they are
similar to some degree. A CCO Plan is a Directive Information Content Entity that prescribes some
set of intended CCO Intentional Acts through which some Agent expects to achieve some CCO
Objective. Here CCO Plan is constrained to the prescription of intentional acts, but PROV Plan is
allowed to prescribe activities or processes that are broader than intentional acts. As its definition
reveals, “[t]here exist no prescriptive requirement on the nature of plans, their representation, the


20


A semantic approach to mapping the Provenance Ontology to Basic Formal Ontology


actions or steps they consist of, or their intended goals” [8]. Therefore, there is no reason for
limiting PROV Plan only to Directive Information Content Entity, and thus there is no equivalent
mapping between PROV Plan and CCO Plan.​


**Qualified object properties**


PROV-O contains 14 Qualification Properties, 4 Influencer Properties, and 6 additional
object properties. **PROV** _**qualifiedInfluence**_ and **PROV** _**influencer**_ are the superproperties of
Qualification properties and Influencer properties, respectively. Given their maximal causal
generality, a plausible proposal is to appeal to RO by mapping them both as subproperties of **RO**
_**causally related to**_ . The same is for **PROV** _**wasInfluencedBy**_, the most general one among the 6
additional qualified properties.


We highlight mappings of PROV-O qualified properties whose domain or range is mapped
to a subclass of BFO process boundary. Few object properties in BFO, RO, and CCO directly
involve process boundary. This fact also indirectly shows why there exists no equivalent mapping for
some qualified properties. For example, **PROV** _**qualifiedStart**_, _**qualifiedEnd**_, and _**qualifiedUsage**_
take PROV Activity as their shared domain, and their respective ranges are PROV Start, PROV End,
and PROV Usage, which are all mapped as subclasses of BFO process boundary. We thus find it
tractable to map their domains and ranges to the parent class of BFO process boundary: occurrent.
In light of this, the most appropriate way is to map them as subproperties of **BFO** _**has temporal**_
_**part**_, because it takes occurrents including process boundaries as their domain and range. Informally,
the start and end of an activity, and an activity's usage of an entity, are simply temporal parts of an
activity.


A more difficult type of cases concerns how to map **PROV** _**qualifiedGeneration**_ and **PROV**
_**qualifiedInvalidation**_ . As their respective range, PROV Generation and PROV Invalidation are also
mapped as subclasses of BFO process boundary. Given that their shared domain is PROV Entity,
however, they cannot be mapped as subproperties of **BFO** _**has temporal part**_ . On the other hand,
the meanings of PROV _qualifiedGeneration_ and PROV _qualifiedInvalidation_ are somewhat similar to
those of **CCO** _**is output of**_ and **CCO** _**is affected by**_, respectively. But it is still inconsistent to directly
map the former to the latter by the subsumption relation because the latter take process as their
shared range but process is disjoint with process boundary (as the former’s range). Therefore, we
have to appeal to SKOS _relatedMatch_ as a last resort here. Nevertheless, all of these qualified
properties are still transitively subsumed by our mapping of PROV _qualifiedInfluence_ to RO _causally_
_related to_ .


Up to now we have reviewed all important mapping cases of qualified classes and object
properties. The remaining qualified properties, though not discussed here, are encoded in the
alignment files [18].


**Data properties**


While we considered complex mappings for PROV-O data properties, we were unable to encode


21


A semantic approach to mapping the Provenance Ontology to Basic Formal Ontology


these in a computable format due to representational limits of OWL, RDF, and SWRL. For example,
the data properties **PROV** _**startedAtTime**_ and _**endedAtTime**_ relate a PROV Activity to a

`xsd:dateTime` value. In BFO, the relationship between these entities is encoded in a more
fine-grained way to make clear the distinctions between a process, the time when it occurred, and
the different names for that time. **Figure 8** shows how a PROV Activity, as a process, _occupies_ a
temporal region with a _first instant_ . That instant can be _designated_ with an identifier, a **CCO** **Time of**
**Day Identifier**, which is a BFO generically dependent continuant. In turn, that identifier may be
encoded in different ways, such as with a **CCO Document Field**, a BFO independent continuant,
that is related to the `xsd:dateTime` value with **CCO** _**has date time value**_ . PROV-O’s remaining data
properties could be similarly translated with even more complex relationships represented in BFO
and CCO. It may be possible to represent these complex mappings with SPARQL CONSTRUCT
queries.


**Figure 8:** Conceptual mapping of PROV _startedAtTime_ and _atTime_ to several BFO and CCO properties. Data properties

are shown in green. Note that PROV-O can similarly encode more information using its reified PROV Start class.


22


A semantic approach to mapping the Provenance Ontology to Basic Formal Ontology


**Inconsistencies**


All alignments were tested by importing them, along with BFO, RO, CCO, and all example instances
(312 individuals) from the W3C documentation into a temporary OWL ontology that is verified for
satisfiability and consistency using the HermiT reasoner. Two examples from the W3C PROV-O
documentation were discovered to be inconsistent with PROV-O itself, independently of our
alignments. First, _Example 4_ [(https://www.w3.org/TR/prov-o/#narrative-example-expanded-3)](https://www.w3.org/TR/prov-o/#narrative-example-expanded-3)
relates an instance of publication activity to a post editor via the PROV _wasAttributedTo_ relation,
whose domain is PROV Entity. This entails that the publication activity is both a PROV Activity and
a PROV Entity, but these classes are disjoint in PROV-O, so this results in a contradiction. Second,
the example for PROV Revision relates an instance of PROV Entity to someone via the PROV
_wasAssociatedWith_ relation, whose domain is PROV Activity. This results in a contradiction because
PROV Entity and PROV Activity are disjoint.


Two example instances were found to be inconsistent with our PROV-BFO alignment. One
is an instance of PROV Entity, a digested protein sample that is related to a different, (non-digested)


**Figure 9** : A PROV-O example instance that contradicts our PROV-BFO alignment [8]. The digested protein sample, a

BFO continuant, is inferred to also be an instance of PROV EntityInfluence, a BFO occurrent.

The above example assertions entail that the digested protein sample is also an instance of
PROV EntityInfluence. However, PROV Entity is a continuant while PROV EntityInfluence is an
occurrent, and these classes are disjoint. Therefore, the disjointness of continuants and occurrents is
inconsistent with the digested protein sample being both a PROV Entity and a PROV
EntityInfluence. To explain this inconsistency with our alignment, note that the subject of the
PROV _entity_ relation should have been the PROV Derivation, not the digested protein sample, as
shown in **Figure 10** and similarly in a previous example shown in **Figure 7** . This demonstrates how
our alignments can be used to find mistakes that are otherwise consistent with PROV-O.


23


A semantic approach to mapping the Provenance Ontology to Basic Formal Ontology


**Figure 10** : Simplified visual model of the digested protein example from Figure 7. Instances are shown as diamonds
with purple lines indicating relations between them. The anonymous PROV Derivation instance is named “(digestion)”.
The left side shows the original example, while the right side shows our suggested correction with the modified relation

in green.

Another case of inconsistency concerns an instance of PROV Activity, `:sortActivity`, that
is tagged with PROV _atTime_ [(https://www.w3.org/TR/prov-o/#used) (see](https://www.w3.org/TR/prov-o/#used) **Figure 11** ). PROV
_atTime_ is defined as "the time at which an InstantaneousEvent occurred, in the form of

`xsd:dateTime` ”, having domain PROV InstantaneousEvent, which is equivalently mapped to BFO
process boundary. But in our alignment, PROV Activity is mapped to BFO process, which is disjoint
with process boundary. So this case is inconsistent with our alignment again. Again, to explain this
inconsistency with our mapping, note that this same instance is related in other examples via the
PROV _startedAtTime_ data property, whose domain is PROV Activity
[(https://www.w3.org/TR/prov-o/#Usage) (see](https://www.w3.org/TR/prov-o/#Usage) **Figure 12** ). This suggests that this one example


24


**Figure 11** : An instance of PROV-O that is inconsistent with our PROV-BFO alignment [8]. We believe PROV
_startedAtTime_, whose domain is PROV Activity, should have been used here instead of PROV _atTime_, whose domain is

PROV InstantaneousEvent.


**Figure 12** : Another example of the same PROV-O instance that uses a different object property, PROV _startedAtTime_,

consistent with our PROV-BFO alignment [8].

## **Discussion**


A total alignment was achieved such that every class and object property from PROV-O and its
extensions is mapped to some class or object property from BFO or its extensions, RO and CCO.
Complex data property mappings may be possible in future versions. The mapping predicates used
represent simple or complex equivalence and subsumption relations, implemented with OWL
_equivalentClass_, OWL _equivalentProperty_, RDFS _subClassOf_, RDFS _subPropertyOf_, OWL
_propertyChainAxiom_, and SWRL rules. OWL axiom annotations encode provenance metadata for each
mapping. Coherence, consistency, and conservativity of our alignments was verified with a variety of
ontology engineering techniques. The alignments serve as a test for these techniques, which may be
reused in future projects. SPARQL queries, SWRL rules, OWL axiom annotations, and SKOS
metadata are all W3C-affiliated options for ontology mapping in support of FAIR principles.


The current alignments are practically useful for a number of reasons. They allow for
integration of PROV-O data in projects using BFO, RO, or CCO, and vice versa. For example, our
PROV-BFO alignment entails a SOSA-BFO alignment when combined with PROV-SOSA
alignment [36]. Most significantly, the alignments demonstrate how BFO and related ontologies can
be used to find inconsistencies in data by enriching it with additional logical axioms. In this case,
potential mistakes in example data were found that were consistent with PROV-O alone. The initial
set of BFO class mappings was used to narrow down possible object property mappings, which
demonstrates a benefit of aligning to upper-level ontologies. Finally, the alignments may serve as a
reference alignment for evaluating and improving automated ontology matching systems [6].


25


A semantic approach to mapping the Provenance Ontology to Basic Formal Ontology


​ Our methodology described stages of alignment to maximize semantic interoperability in
terms of the types and number of mapping relations between ontologies. An alignment which
provides a full interpretation of PROV-O into BFO-based ontologies using only equivalence
relations may be achievable in future work. However, we do not recommend adding terms to either
sets of ontologies for the sole purpose of creating equivalence mappings between individual terms.
Instead, existing terms should be reused. For example, we did not find an equivalence mapping for
PROV _wasAttributedTo_ . Users of BFO-based ontologies should use this term with our current
alignments instead of creating an equivalent term. An exception to this would be to add terms that
are not individually equivalent to an existing term, but may be used for other independent reasons.
Reusing existing terms helps ensure that ontologies do not overlap in scope. When an existing term
is reused, a mapping is unnecessary and therefore semantic interoperability is already achieved.

## **Data availability**


The alignment files [18] for each ontology and all related project resources are archived at
[https://doi.org/10.5281/zenodo.14692262 for use according to the Creative Commons Zero v1.0](https://doi.org/10.5281/zenodo.14692262)
Universal license.

## **Code availability**


The mapping project is maintained in a Git repository hosted in GitHub at
[https://github.com/BFO-Mappings/PROV-to-BFO. This repository contains the RDF Turtle files,](https://github.com/BFO-Mappings/PROV-to-BFO)
SPARQL query files, GNU Makefile, and Protege catalog file used for representing and verifying the
alignments. The project dependencies and their versions are listed in the repository, which include
the tools ROBOT, HermiT, GNU Make, and specific versions of RDF, RDFS, OWL, SPARQL, and
SWRL.

## **References**

[1]​ Smith, B. Ontology (Science). _Nature Proceedings_, 2008, 3-4.

[https://doi.org/10.1038/npre.2008.2027.1](https://doi.org/10.1038/npre.2008.2027.1) (2008).

[2]​ Beverley, J. et al. Coordinating virus research: The Virus Infectious Disease Ontology. _PloS_

_One_ **19** [(1), e0285093. https://doi.org/10.1371/journal.pone.0285093](https://doi.org/10.1371/journal.pone.0285093) (2024).

[3]​ W3C OWL Working Group. OWL 2 Web Ontology Language Document Overview (Second

Edition). W3C Recommendation 11 December 2012.
[https://www.w3.org/TR/2012/REC-owl2-overview-20121211/](https://www.w3.org/TR/2012/REC-owl2-overview-20121211/) (2012).

[4]​ Schreiber, G., & Raimond, Y. RDF 1.1 Primer. W3C Working Group Note 24 June 2014.

[https://www.w3.org/TR/2014/NOTE-rdf11-primer-20140624/ (2014).](https://www.w3.org/TR/2014/NOTE-rdf11-primer-20140624/)

[5]​ Callahan, T.J., Tripodi, I.J., Stefanski, A.L. et al. An open source knowledge graph ecosystem

for the life sciences. _Scientific Data_ **11**, 363. [https://doi.org/10.1038/s41597-024-03171-w](https://doi.org/10.1038/s41597-024-03171-w)


26


A semantic approach to mapping the Provenance Ontology to Basic Formal Ontology


(2024).

[6]​ Euzenat, J., & Shvaiko, P. _Ontology Matching_, 2nd edition. Heidelberg: Springer. 43-51 & 300.

[https://doi.org/10.1007/978-3-642-38721-0 (2013).](https://doi.org/10.1007/978-3-642-38721-0)

[7]​ Matentzoglu, N. et al. A simple standard for sharing ontological mappings (SSSOM). _Database_

**2022** [. https://doi.org/10.1093/database/baac035](https://doi.org/10.1093/database/baac035) (2022).

[8]​ Lebo, T. et al. PROV-O: The PROV Ontology. W3C Recommendation April 30 2013.

[https://www.w3.org/TR/2013/REC-prov-o-20130430/ (2013).](https://www.w3.org/TR/2013/REC-prov-o-20130430/)

[9]​ Groth, P. & Moreau, L. PROV-Overview. W3C Working Group Note, 30 April 2013.

[https://www.w3.org/TR/2013/NOTE-prov-overview-20130430/ (2013).](https://www.w3.org/TR/2013/NOTE-prov-overview-20130430/)

[10]​ International Organization for Standardization. Information technology — Top-level

ontologies (TLO) — Part 2: Basic Formal Ontology (BFO) (ISO Standard No.
21838-2:2020). [https://www.iso.org/standard/74572.html](https://www.iso.org/standard/74572.html) (2016).

[11]​ Arp, R., Smith, B. & Spear, A.D. _Building Ontologies with Basic Formal Ontology_ . Cambridge, MA:

[MIT Press. https://doi.org/10.7551/mitpress/9780262527811.001.0001](https://doi.org/10.7551/mitpress/9780262527811.001.0001) (2015).

[12]​ BFO 2020. Version 2024-01-29.

[https://github.com/BFO-ontology/BFO-2020/releases/tag/release-2024-01-29](https://github.com/BFO-ontology/BFO-2020/releases/tag/release-2024-01-29) (2024).

[13]​ Jackson, R. C. et al. OBO Foundry in 2021: operationalizing open data principles to evaluate

ontologies. _Database_ **2021,** baab069. [https://doi.org/10.1093/database/baab069 (2021).](https://doi.org/10.1093/database/baab069)

[14]​ Smith B. et al. Relations in biomedical ontologies. _Genome Biol._ **6** (5), R46. doi:

10.1186/gb-2005-6-5-r46. Epub 2005 Apr 28. PMID: 15892874; PMCID: PMC1175958.
[https://doi.org/10.1186/gb-2005-6-5-r46](https://doi.org/10.1186/gb-2005-6-5-r46) (2005).

[15]​ Mungall, C. et al. OBO Relations Ontology. Version 2024-04-24.

[https://github.com/oborel/obo-relations/releases/tag/v2024-04-24](https://github.com/oborel/obo-relations/releases/tag/v2024-04-24) (2024).

[16]​ Jensen, M., et al. The Common Core Ontologies. arXiv preprint arXiv:2404.17758.

[https://doi.org/10.48550/arXiv.2404.17758](https://doi.org/10.48550/arXiv.2404.17758) (2024).

[17]​ CUBRC. The Common Core Ontologies (CCO). Version v2.0. 2024-11-06.

[https://github.com/CommonCoreOntology/CommonCoreOntologies/releases/tag/v2.0-20](https://github.com/CommonCoreOntology/CommonCoreOntologies/releases/tag/v2.0-2024-11-06)
[24-11-06](https://github.com/CommonCoreOntology/CommonCoreOntologies/releases/tag/v2.0-2024-11-06) (2024).

[18]​ Prudhomme, T., De Colle, G., Liebers, A., Sculley, A., Xie, P., Cohen, S., & Beverley, J.

PROV-to-BFO: v2025-01-19 (v2025-01-19). Zenodo.
[https://doi.org/10.5281/zenodo.14692262](https://doi.org/10.5281/zenodo.14692262) (2025).

[19]​ Wilkinson, M. D. et al. The FAIR Guiding Principles for scientific data management and

stewardship. _Scientific Data_ **3** [, 160018. https://doi.org/10.1038/sdata.2016.18](https://doi.org/10.1038/sdata.2016.18) (2016).

[20]​ Brickley, D. & Guha, R. Resource Description Framework (RDF) Schema Specification 1.0.

RDF Schema 1.1. W3C Recommendation 25 February 2014.
[https://www.w3.org/TR/2014/REC-rdf-schema-20140225/](https://www.w3.org/TR/2014/REC-rdf-schema-20140225/) (2014).


27


A semantic approach to mapping the Provenance Ontology to Basic Formal Ontology


[21]​ Horrocks, I. SWRL: A Semantic Web Rule Language Combining OWL and RuleML. W3C

Member Submission 21 May 2004.
[https://www.w3.org/submissions/2004/SUBM-SWRL-20040521/](https://www.w3.org/submissions/2004/SUBM-SWRL-20040521/) (2004).

[22]​ Shearer R., Motik B. & Horrocks I. HermiT: A Highly-Efficient OWL Reasoner. _OWLED_

**432** [. https://ceur-ws.org/Vol-432/owled2008eu_submission_12.pdf](https://ceur-ws.org/Vol-432/owled2008eu_submission_12.pdf) (2008).

[23]​ Glimm, B., Horrocks, I., Motik, B., Stoilos, G. & Wang, Z. HermiT: an OWL 2 reasoner.

_Journal of Automated Reasoning_ **53,** 245-269. [https://doi.org/10.1007/s10817-014-9305-1](https://doi.org/10.1007/s10817-014-9305-1)
(2014).

[24]​ Harris, S., Seaborne, A., & Prud’hommeaux, E. SPARQL 1.1 query language. W3C

Recommendation 21 March 2013.
[https://www.w3.org/TR/2013/REC-sparql11-query-20130321/](https://www.w3.org/TR/2013/REC-sparql11-query-20130321/) (2013).

[25]​ Miles, A. & Bechhofer, Sean. SKOS simple knowledge organization system reference. W3C

Recommendation 18 August 2009.
[https://www.w3.org/TR/2009/REC-skos-reference-20090818/](https://www.w3.org/TR/2009/REC-skos-reference-20090818/) (2009).

[26]​ Grüninger, M. Model-theoretic Approaches to Semantic Integration (Extended Abstract).

Semantic Interoperability and Integration. Dagstuhl Seminar Proceedings **4391**, 1-9, Schloss
Dagstuhl – Leibniz-Zentrum für Informatik. [https://doi.org/10.4230/DagSemProc.04391.11](https://doi.org/10.4230/DagSemProc.04391.11)
(2005).

[27]​ Jiménez-Ruiz, E., Cuenca Grau, B., Horrocks, I. & Berlanga, R.: Logic-based Assessment of

the Compatibility of UMLS Ontology Sources. _J. Biomed. Semant_ . **2** (Suppl 1), S2.
[https://doi.org/10.1186/2041-1480-2-S1-S2 (2011).](https://doi.org/10.1186/2041-1480-2-S1-S2)

[28]​ Lutz, C., Walther, D. & Wolter, F. Conservative Extensions in Expressive Description Logics.

_IJCAI_ **7**, 453-458. [https://www.ijcai.org/Proceedings/07/Papers/071.pdf](https://www.ijcai.org/Proceedings/07/Papers/071.pdf) (2007).

[29]​ Motik, B., Patel-Schneider, P.F. & Grau, B.C. OWL 2 Web Ontology Language Direct

Semantics (Second Edition). W3C Recommendation 11 December 2012.
[https://w3.org/TR/2012/REC-owl2-direct-semantics-20121211/](https://w3.org/TR/2012/REC-owl2-direct-semantics-20121211/) (2012).

[30]​ Solimando, A., Jimenez-Ruiz, E. & Guerrini, G. Minimizing conservativity violations in

ontology alignments: Algorithms and evaluation. _Knowledge and Information Systems_ **51,** 775-819.
[https://doi.org/10.1007/s10115-016-0983-3](https://doi.org/10.1007/s10115-016-0983-3) (2017).

[31]​ Grüninger, M., Hahmann, T., Hashemi, A., Ong, D. & Ozgovde, A. Modular first-order

ontologies via repositories. _Applied Ontology_, **7** (2), 169-209.
[https://doi.org/10.3233/AO-2012-0106](https://doi.org/10.3233/AO-2012-0106) (2012).

[32]​ Grüninger, M., Chui, C.S., & Katsumi, M. Upper Ontologies in COLORE. _Proceedings of the_

_Joint Ontology Workshops (JOWO)_ [, 3. https://ceur-ws.org/Vol-2050/FOUST_paper_2.pdf](https://ceur-ws.org/Vol-2050/FOUST_paper_2.pdf)
(2017).

[33]​ Schorlemmer, M., & Kalfoglou, Y. Institutionalising ontology-based semantic integration.

_Applied Ontology,_ **3** [(3), 131-150. https://doi.org/10.3233/AO-2008-0041 (2008).](https://doi.org/10.3233/AO-2008-0041)


28


A semantic approach to mapping the Provenance Ontology to Basic Formal Ontology


[34]​ Jackson, R. C. et al. ROBOT: a tool for automating ontology workflows. _BMC bioinformatics_,

**20,** 1-10. [https://doi.org/10.1186/s12859-019-3002-3 (2019).](https://doi.org/10.1186/s12859-019-3002-3)

[35]​ Gavin, C. & Prud’hommeaux, E. RDF 1.1 Turtle — Terse RDF Triple Language. W3C

Recommendation 25 February 2014. [https://www.w3.org/TR/2014/REC-turtle-20140225/](https://www.w3.org/TR/2014/REC-turtle-20140225/)
(2014).

[36]​ Janowicz, K. et al. SOSA: A Lightweight Ontology for Sensors, Observations, Samples, and

Actuators. _Journal of Web Semantics_ **56,** [1-10. https://doi.org/10.1016/j.websem.2018.06.003](https://doi.org/10.1016/j.websem.2018.06.003)
(2018).

[37]​ Haller, A. et al. Semantic Sensor Network Ontology. W3C Recommendation 19 October

[2017. https://www.w3.org/TR/2017/REC-vocab-ssn-20171019/](https://www.w3.org/TR/2017/REC-vocab-ssn-20171019/) (2009).

[38]​ Garijo, D. & Echkert, K. Dublin Core to PROV Mapping. W3C Working Group Note 30

April 2013. [https://www.w3.org/TR/2013/NOTE-prov-dc-20130430/](https://www.w3.org/TR/2013/NOTE-prov-dc-20130430/) (2013).

[39]​ Patel-Schneider, P. F. et al. OWL 2 Web Ontology Language Mapping to RDF Graphs. W3C

Recommendation 11 December 2012.
[https://www.w3.org/TR/2012/REC-owl2-mapping-to-rdf-20121211/#Translation_of_Axio](https://www.w3.org/TR/2012/REC-owl2-mapping-to-rdf-20121211/#Translation_of_Axioms_with_Annotations)
[ms_with_Annotations (2012).](https://www.w3.org/TR/2012/REC-owl2-mapping-to-rdf-20121211/#Translation_of_Axioms_with_Annotations)

[40]​ Matentzoglu, N. et al. A Simple Standard for Ontological Mappings 2022: Updates of data

model and outlook. _OM@ ISWC_, pp. 61-66. 2022. [http://doi.org/10.5281/zenodo.7672104](http://doi.org/10.5281/zenodo.7672104)
(2022).

[41]​ Musen, M. A. The protégé project: a look back and a look forward. _AI matters_ **1.4**, 4-12.

[https://pmc.ncbi.nlm.nih.gov/articles/PMC4883684/](https://pmc.ncbi.nlm.nih.gov/articles/PMC4883684/) (2015).

[42]​ Motik, B. et al. OWL 2 Web Ontology Language Structural Specification and Functional-Style

Syntax (Second Edition). W3C Recommendation 11 December 2012.
[https://www.w3.org/TR/2012/REC-owl2-syntax-20121211/ (2012).](https://www.w3.org/TR/2012/REC-owl2-syntax-20121211/)

[43]​ Moreau, L., Groth, P., Cheney, J., Lebo, T. & Miles, S. The rationale of PROV. _Journal of Web_

_Semantics_ **35** [, 235-257. https://doi.org/10.1016/j.websem.2015.04.001 (2015).](https://doi.org/10.1016/j.websem.2015.04.001)

[44]​ De Nies, T. et al. PROV-Dictionary: Modeling Provenance for Dictionary Data Structures.

W3C Working Group Note 30 April 2013.
[https://www.w3.org/TR/2013/NOTE-prov-dictionary-20130430/ (2013).](https://www.w3.org/TR/2013/NOTE-prov-dictionary-20130430/)

[45]​ Baader, F., Horrocks, I., Lutz, C. & Sattler, U. _Introduction to Description Logic_ . Cambridge

University Press. [https://doi.org/10.1017/9781139025355 (2017).](https://doi.org/10.1017/9781139025355)

[46]​ Noy, N. & Rector, A. Defining N-ary Relations on the Semantic Web. W3C Working Group

Note 12 April 2006. [https://www.w3.org/TR/2006/NOTE-swbp-n-aryRelations-20060412/](https://www.w3.org/TR/2006/NOTE-swbp-n-aryRelations-20060412/)
(2006).

[47]​ Gangemi, A. & Mika, P. Understanding the Semantic Web through Descriptions and

Situations. In Meersman, R., Tari, Z., Schmidt, D. C. (eds.), _On the Move to Meaningful Internet_
_Systems 2003: CoopIS, DOA, and ODBASE_ . OTM Confederated International Conferences,


29


A semantic approach to mapping the Provenance Ontology to Basic Formal Ontology


Catania, Sicily, Italy, November 3-7, 2003, **2888** . Lecture Notes in Computer Science.
Springer, 689-706. [https://doi.org/10.1007/978-3-540-39964-3_44 (2003).](https://doi.org/10.1007/978-3-540-39964-3_44)

[48]​ Guarino, N. & Welty, C. An Introduction to Ontoclean (revised version). In Staab, S., and

Studer, R. (eds.), _Handbook on Ontologies_ (second edition). Springer: 201-221.
[https://doi.org/10.1007/978-3-540-24750-0_8](https://doi.org/10.1007/978-3-540-24750-0_8) (2009).

[49]​ Grewe, N. et al. Expressing Time-dependent Relations through Temporal Qualifications.

[https://studylib.net/doc/6849748/1---basic-formal-ontology--bfo (2016).](https://studylib.net/doc/6849748/1---basic-formal-ontology--bfo-)

## **Acknowledgements**


The authors would like to thank Timothy Lebo for guidance and context about PROV-O. Jonathan
Vajda and Ali Hasanzadeh also provided feedback about BFO.

## **Author information** Authors and Affiliations


**National Center for Ontological Research, University at Buffalo, Buffalo, NY, USA**


Tim Prudhomme, Giacomo De Colle, Austin Liebers, Alec Sculley, Peihong “Karl” Xie, Sydney
Cohen, & John Beverley


**Department of Philosophy, University at Buffalo, Buffalo, NY, USA**


Giacomo De Colle, Austin Liebers, & John Beverley


**Conceptual Systems, Chapel Hill, NC, USA**


Tim Prudhomme


**Summit Knowledge Solutions, Arlington, VA, USA**


Alec Sculley


**Department of Philosophy, University of Vienna, Vienna, Austria**


Peihong “Karl” Xie


**Institute for Artificial Intelligence and Data Science, Buffalo, NY, USA**

John Beverley​

## Contributions


G.D.C., A.L., A.S., P.X., T.P. and S.C. engineered the mappings by analyzing the ontologies in the
context of their associated literature and documentation. T.P. formulated the methodology in terms
of theoretical alignment criteria and practical engineering techniques for verifying the alignment. T.P.
developed and documented the technical artifacts used to encode and test the alignments, in


30


A semantic approach to mapping the Provenance Ontology to Basic Formal Ontology


addition to the automated ontology engineering pipeline.


T.P. was the primary author and editor of the manuscript and illustrator of figures while P.X., G.D.C.,
A.L., A.S. wrote and reviewed significant sections. G.D.C., A.L., and A.S. presented the project for
feedback to separate groups within the ontology community. T.P. and S.C. managed the project by
scheduling meetings, assigning tasks, and documenting progress. J.B. served as the primary
supervisor and senior researcher responsible for conceiving this project.

## Corresponding Author


[Correspondence to Tim Prudhomme.](mailto:tmprdh@gmail.com)

## **Ethics declarations** Competing Interests


None


31


