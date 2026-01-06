<!-- Source: 23-UFO_Story_Ontological_Foundations.pdf | Chunk 1/1 -->

Applied Ontology 10 (2015) 259–271 259
DOI 10.3233/AO-150157
IOS Press

## Position paper

# Towards ontological foundations for conceptual modeling: The unified foundational ontology (UFO) story


Giancarlo Guizzardi [a] _[,]_ [∗], Gerd Wagner [b],
João Paulo Andrade Almeida [a] and Renata S.S. Guizzardi [a]

a _Ontology and Conceptual Modeling Research Group (NEMO), Federal University of Espírito Santo,_
_Vitória, Brazil_
_[E-mails: gguizzardi@inf.ufes.br, jpalmeida@inf.ufes.br, rguizzardi@inf.ufes.br](mailto:gguizzardi@inf.ufes.br)_
b _Institute of Informatics, Brandenburg University of Technology, Germany_
_[E-mail: G.Wagner@tu-cottbus.de](mailto:G.Wagner@tu-cottbus.de)_


**Abstract.** This paper describes a long-term research program on developing ontological foundations for conceptual modeling.
This program, organized around the theoretical background of the foundational ontology _UFO_ ( _Unified Foundational Ontol-_
_ogy_ ), aims at developing theories, methodologies and engineering tools with the goal of advancing conceptual modeling as a
theoretically sound discipline but also one that has concrete and measurable practical implications. The paper describes the
historical context in which UFO was conceived, briefly discusses its stratified organization, and reports on a number of applications of this foundational ontology over more than a decade. In particular, it discusses the most successful application of UFO,
namely, the development of the conceptual modeling language _OntoUML_ . The paper also discusses a number of methodological
and computational tools, which have been developed over the years to support the OntoUML community. Examples of these
methodological tools include _ontological patterns_ and _anti-patterns_ ; examples of these computational tools include automated
support for pattern-based model construction, formal model verification, formal model validation via visual simulation, model
verbalization, code generation and anti-pattern detection and rectification. In addition, the paper reports on a variety of applications in which the language as well as its associated tools have been employed to engineer models in several institutional
contexts and domains. Finally, it reflects on some of these lessons learned by observing how OntoUML has been actually used
in practice by its community and on how these have influenced both the evolution of the language as well as the advancement
of some of the core ontological notions in UFO.


Keywords: Ontology, conceptual modeling, OntoUML, UFO, ontology-driven conceptual modeling

Accepted by: Nicola Guarino


**1. Introduction**


This paper describes a long-term research program on developing ontological foundations for conceptual modeling. This research program aims at developing theories, methodologies and engineering
tools (including modeling languages, patterns, anti-patterns as well as computational tools) with the


[*Corresponding author. E-mail: gguizzardi@inf.ufes.br.](mailto:gguizzardi@inf.ufes.br)


1570-5838/15/$35.00 © 2015 – IOS Press and the authors. All rights reserved


260 _G. Guizzardi et al. / Towards ontological foundations for conceptual modeling_


goal of advancing conceptual modeling as a theoretically sound discipline with concrete and measurable practical implications. For over a decade, our research program has been organized around the
theoretical background of a foundational ontology termed _UFO_ ( _Unified Foundational Ontology_ ) and,
frequently, materialized through the development of number of results associated with an ontologically
well-founded conceptual modeling version of UML termed _OntoUML_ .
In Section 2, we start by briefly describing the historical context in which UFO was conceived. This
has the purpose of highlighting the goals of the project and contextualizing the rationale behind fundamental ontological choices made in the design of UFO. In Section 3, we briefly discuss the layers
(or strata) comprising UFO and the ontological micro-theories comprising each of them. This section
also reports on a number of applications of this foundational ontology over more than a decade, chiefly,
related to the ontological analysis, (re)design and integration of different modeling languages, reference
models and standards. In Section 4, we discuss the most successful application of UFO, namely, the
development of the OntoUML language. The section briefly discusses the design of this language and
reports on a number of applications in which the language as well as its associated methodological and
computational tools have been employed to engineer models in a variety of institutional contexts and
domains. In addition, the section elaborates on the development of a model-based computational environment, which has been developed to support the OntoUML community in terms of pattern-based
model construction, code generation, formal verification, formal validation via visual simulation, model
verbalization and anti-pattern detection and rectification. Given the diffusion of the language, over the
years, we have managed to assemble a model repository containing OntoUML models in different domains. The observation of how the language was used in practice in the construction of these models
proved to be a fruitful source of empirical knowledge about the actual notions that needed to be accounted for in an ontology-driven structural conceptual modeling language. Section 5 concludes the
paper by reflecting on some of these lessons learned and how they have influenced both the evolution of
the language of some core ontological notions in UFO.


**2. A brief historical background**


In 2002, the first two authors have started a research program of conducting ontological analysis of
conceptual modeling languages and standards with the goal of developing sound ontological foundations
for conceptual modeling languages (Guizzardi et al., 2002a; 2002b). Our program was motivated by the
strong belief that any serious scientific discipline should have well-established and explicitly defined
metaphysical foundations (Bunge, 1977) or that, as nicely put by Collier (1994): “ _the opposite of on-_
_tology is not non-ontology, but bad ontology_ ”. In other words, any representation system that has some
real-world semantics (as opposed to mere formal semantics) makes an ontological commitment (Guizzardi & Halpin, 2008). This research program was motivated by the belief that controlling and defending
a particular ontological commitment is essential for the progress of a scientific discipline.
In the realm of conceptual modeling, the idea that “ _data are fragments of a theory of the real-world and_
_data processing is about manipulating models of such a theory_ ” was there since Mealy’s seminal paper
entitled ‘Another Look on Data’ (Mealy, 1967). In fact, Mealy’s paper seems to contain the first mention
of the term ‘ontology’ in the computer and information science literature. A number of fundamental
conceptual modeling issues of an ontological nature were also discussed in Bill Kent’s book ‘Data and
Reality’ (Kent, 1978). This book brought attention to issues like identity, unity and classification, and
started exposing the subtleties of fundamental conceptual modeling constructs such as _relationships_ .


_G. Guizzardi et al. / Towards ontological foundations for conceptual modeling_ 261


However, neither Mealy’s paper nor Kent’s book tried to actually develop comprehensive ontological
foundations for conceptual modeling. Perhaps the first corpus of work to attempt that goal was reported
in the series of publications initiated by Yair Wand, Ron Weber and colleagues (Wand & Weber, 1989;
1990; Weber, 1997) in the late 80’s. Instead of developing a new ontology themselves, Wand and Weber
proposed an adaptation of the ontological theory put forth by the Argentinean physicist and philosopher
of science Mario Bunge. The result of this effort came to be known as the BWW (Bunge–Wand–Weber)
ontology. The authors then employed this theory to evaluate a number of conceptual modeling languages
including NIAM (Weber & Zhang, 1991), ER (Wand et al., 1999), UML (Evermann & Weber, 2001)
and OWL (Bera & Wand, 2004).
Despite being inspired by the goals of the BWW approach, we did not share their research direction. Bunge’s objective was doing philosophy of science and, being a physicist, chiefly, philosophy of
the hard sciences. Conceptual Modeling, in contrast, is about “ _representing aspects of the physical and_
_social world for the purpose of understanding and communication_ [ _and, hence_ ] _the contribution of a_
_conceptual modeling notation rests in its ability to promote understanding about the depicted reality_
_among human users_ ” (Mylopoulos, 1992). As a result, any attempt to develop ontological foundations
for conceptual modeling should take both human cognition and human linguistic competence seriously;
it should be a project in descriptive metaphysics and not in revisionary ontology (Guarino & Guizzardi,
2006; Guizzardi, 2007b). This mismatch between the purposes for which Bunge’s ontology was developed and the requirements of ontological foundations for conceptual modeling became manifest in the
literature as the predictions made by the BWW approach found themselves in strong contrast with the
intuitions and practical knowledge of modelers and with some predictions unanimously shared by alternative approaches. For instance, around 2003, a number of authors showed that the BWW dictum that
“ _mutual properties_ ( _or relations_ ) _should never be modeled as classes as they should not be allowed to_
_have properties_ ” was in conflict with modeling predictions made by other foundational theories (e.g.,
Jackendoff’s Semantic Structures (Veres & Hitchman, 2002; Veres & Mansson, 2005)) and with the intuition of modelers. Regarding the latter, as shown by (Hitchman, 2003), in recorded modeling sessions
with practitioners, it became evident that reified relationships were frequently a part of these practitioners’ ontology.
It was clear to us from the outset that we needed an ontological theory that would countenance both
individuals and universals and one that would include not only substantial individuals and universals but
also accidents (particularized properties, moments, qualities, modes, tropes, abstract particulars, aspects,
ways) and accident universals. In other words, we needed a _Four-Category Ontology_ (Lowe, 2006). We
needed particularized properties not only because they were of great importance in making sense of
language and cognition (Davison, 2001; Parsons, 1990; Masolo et al., 2003) but because they would
repeatedly appear in the discourse of conceptual modelers. As previously mentioned, particularized relations (relationships) and particularized intrinsic properties (e.g., often represented by the so-called
weak entities) are frequently modeled as bearers of other particularized properties in the practice of
conceptual modeling. In fact, as demonstrated by (Guizzardi, 2005; Guizzardi et al., 2006; Guizzardi
& Wagner, 2008; Guarino & Guizzardi, 2015), there are many conceptual modeling problems that can
hardly be solved without considering particularized properties.
In initial papers for this project, we attempted to employ the GFO (General Formalized Ontology)/GOL (General Ontology Language) being developed in Leipzig, Germany, as our reference theory
(Heller & Herre, 2004; Heller et al., 2004). More or less at the same time, a strong cooperation was established with the Laboratory of Applied Ontology (LOA) (Trento, Italy), which was during that period
developing the Descriptive Ontology for Linguistic and Cognitive Engineering (DOLCE) (Masolo et al.,


262 _G. Guizzardi et al. / Towards ontological foundations for conceptual modeling_


2003). In this setting, our first attempt was to unify DOLCE and GFO to produce a reference foundational ontology for conceptual modeling (hence, the name _Unified_ Foundational Ontology) (Guizzardi
& Wagner, 2004). Both theories were philosophically sound and formally characterized. Moreover, they
were both based on the so-called Aristotelian Square, i.e., “Four-Category Ontologies”.
It became clear quite soon, however, that further investigation was needed, with a focus on the requirements of the conceptual modeling discipline. In particular, ontological foundations for conceptual
modeling would demand micro-theories to address conceptual modeling’s most fundamental constructs,
namely, _Entity Types_ and _Relationship Types_ (hence, the name of the so-called Entity-Relationship approach that gives the name to the most important conference in conceptual modeling!). So, any reference
theory for conceptual modeling would need a rich theory of entity (object) types and a rich theory of
domain (also called material) relations. In the case of the former, we needed something in the spirit of
the ontology of universals underlying the OntoClean methodology (Guarino & Welty, 2009) in order to
systematize a number of notions that were pervasive in the conceptual modeling literature (e.g., types,
roles, phases or states, mixins) but for which there were no precise definitions or consensus (Guizzardi
et al., 2004a). In that respect, GFO’s theory of universals still does not recognize these notions and
DOLCE does not include universal as a category (DOLCE was designed as an ontology of particulars).
Regarding the latter, DOLCE still does not include a theory of particularized relational properties (relational qualities) and the GFO theory of relations is subject to the so-called Bradley Regress (Bradley,
1893) and, hence, it can only be instantiated by infinite (logical) models. This feature makes it unsuitable for conceptual modeling applications. Finally, there were many additional specific aspects needed
for a general ontology for conceptual modeling that were not addressed by the existing approaches (e.g.,
attributes and datatypes, different types of specialization relations between relations, a rich theory of
cognitively/linguistically motivated part-whole relations). We needed to develop a full-blown foundational ontology specifically created to address these conceptual modeling requirements.


**3. The unified foundational ontology and its applications**


The UFO ontology was developed by consistently putting together a number of theories originating
from areas such as Formal Ontology in philosophy, cognitive science, linguistics and philosophical logics. It comprises a number of micro-theories addressing fundamental conceptual modeling notions. The
ontology is divided in three strata dealing with different aspects of reality, namely:


 - **UFO-A** : An Ontology of Endurants dealing with aspects of structural conceptual modeling. It is
organized as a Four-Category ontology comprising theories of Types and Taxonomic Structures
(Guizzardi et al., 2004a; Guizzardi, 2012) connected to a theory of object identifiers (including a
formal semantics in a Sortal Quantified Modal Logics (Guizzardi, 2015)), Part-Whole Relations
(Guizzardi, 2007a; 2009; 2010a; 2011), Particularized Intrinsic Properties, Attributes and Attribute
Value Spaces (Guizzardi et al., 2004b; 2006; Guizzardi & Zamborlini, 2014) (including a theory
of Datatypes as Measure Structures (Albuquerque & Guizzardi, 2013)), Particularized Relational
Properties and Relations (Guizzardi & Wagner, 2008; Costal et al., 2011; Guarino & Guizzardi,
2015) and Roles (Guizzardi, 2006; Masolo et al., 2005);

 - **UFO-B** : An Ontology of Perdurants (Events, Processes) dealing with aspects such as Perdurant Mereology, Temporal Ordering of Perdurants, Object Participation in Perdurants, Causation,
Change and the connection between Perdurans and Endurants via Dispositions (Guizzardi et al.,
2013a);


_G. Guizzardi et al. / Towards ontological foundations for conceptual modeling_ 263


 - **UFO-C** : An Ontology of Intentional and Social Entities, which is constructed on top of UFOA and UFO-B, and which addresses notions such as Beliefs, Desires, Intentions, Goals, Actions,
Commitments and Claims, Social Roles and Social Particularized Relational Complexes (Social
Relators), among others (Guizzardi et al., 2008; Guizzardi & Guizzardi, 2010).


Over the years, UFO has been employed as a basis for analyzing, reengineering and integrating many
modeling languages and standards in different domains (e.g., UML, TOGAF, ArchiMate, RM-ODP,
TROPOS/i [∗], AORML, ARIS, BPMN) as well as for the development of Core and Domain Ontologies
in different areas. For instance, it has been successfully used to provide conceptual clarification in complex domains such as Services (Nardi et al., 2015), Capabilities (Azevedo et al., 2015), Organizational
Structures (Santos Junior et al., 2013), Communities (Almeida & Guizzardi, 2013), Goals and Motivations (Guizzardi et al., 2012; 2013b; Azevedo et al., 2011), Constitutional Law (Griffo et al., 2015),
Business Processes (Guizzardi & Wagner, 2011b; Santos Junior et al., 2010), Discrete Event Simulation (Guizzardi & Wagner, 2010; 2011a; 2012; 2013), Simulation for Land Covering and Use (Grueau,
2014), Software Quality (Shekhovtsov & Mayr, 2014), Software Measurement (Moretto & Barcellos,
2014), Foundations of Software Engineering (Henderson-Sellers, 2012; Henderson-Sellers et al., 2014),
Software Requirements (Guizzardi et al., 2014), among many others. Of all applications of UFO, one
deserves special attention, namely, the use of UFO-A in the design of an ontology-driven conceptual
modeling language, which later came to be known as OntoUML. This language is discussed in the next
section.


**4. OntoUML: Language, engineering support and its applications**


OntoUML (Guizzardi, 2005) was conceived as an ontologically well-founded version of the UML 2.0
fragment of class diagrams. The idea was to employ the ontology-based language engineering method
proposed by (Guizzardi et al., 2005) (and later refined by (Guizzardi, 2013)) to design a _language for_
_structural conceptual modeling_ (i.e., for modeling aspects related to endurants) that would have two
main characteristics. Firstly, the worldview embedded in the language through its conceptual primitives
(what some authors would call the _ontology behind the language_ (Guizzardi, 2007b)) should be isomorphic to the ontological distinctions put forth by UFO-A. Secondly, the language metamodel should
incorporate formal syntactical constraints that would delimit the set of grammatically valid models of
the language to those that represented intended state of affairs admitted by the underlying ontology.
By doing this, we have managed to build a modeling language with explicitly defined formal and realworld semantics. This language serves as an engineering tool for enabling the use of formal ontological
theories in the construction of conceptual models and domain ontologies.
Over the years, OntoUML has been adopted by many research, industrial and government institutions
worldwide. In particular, it has been considered as a candidate for addressing the OMG SIMF (Semantic Information Model Federation) Request for Proposal, [1] after a report of its successful use over the
years by a branch of the U.S. Department of Defense (2011). In addition, some of the foundational theories underlying OntoUML have also been adopted by other conceptual modeling languages, e.g., ORM
2.0 (Halpin & Morgan, 2008; Halpin, 2010). It has been employed in a number of projects in different
countries, in academic, government and industrial institutions, in domains such as Geology (Carbonera
et al., 2015; Abel et al., 2015), Biodiversity Management (Albuquerque et al., 2015), Organ Donation


[1http://www.omgwiki.org/architecture-ecosystem/.](http://www.omgwiki.org/architecture-ecosystem/)


264 _G. Guizzardi et al. / Towards ontological foundations for conceptual modeling_


(Pereira et al., 2015), Petroleum Reservoir Modeling (Werlang, 2015), Disaster Management (Moreira
et al., 2015), Context Modeling (Brandt et al., 2014), Datawarehousing (Moreira et al., 2014), University
Campus Management (Carolla & Spitta, 2014), Enterprise Architecture (Buckl et al., 2011), Metamodeling (Nijenhuis, 2011), Data Provenance (Serra et al., 2012), Measurement (Nunes et al., 2015), Logistics
(Andreeva et al., 2015), Integration of Analytical Tools (Blackburn & Denno, 2015), Complex Media
Management (Carolo & Burlamaqui, 2011), Telecommunications (Barcelos et al., 2011), Petroleum and
Gas (Guizzardi et al., 2010), heart electrophysiology (Gonçalves et al., 2011), among many others.
The decision to build the language as a version of UML (technically, as a UML profile) was mainly
motivated by the fact that UML (unlike many other conceptual modeling languages) has a standardized
and explicitly defined metamodel and a significant set of metamodeling tools that can be used to manipulate and extend this metamodel. As a result, we managed to actually propose a concrete modeling
language that could be used to create ontology-driven conceptual models and domain ontology in a variety of existing UML tools. For instance, as reported by (Guerson et al., 2015), an OntoUML plug-in
has been implemented for the professional tool Enterprise Architect. [2] Moreover, as UML is a de facto
modeling standard, we also managed to leverage existing knowledge and acceptance of the language (at
least among computer scientists).
The first version of this adapted UML metamodel was proposed by (Guizzardi, 2005), fully implemented as a concrete UML profile by (Carraretto, 2010) and implemented as a model-based tool by
(Benevides & Guizzardi, 2009). In that original OntoUML editor, we had support for model construction
and formal verification (against formal metamodel constraints reflecting part of the UFO-A axiomatization). Over the years, a number of contributions have been aggregated in the proposal of a new editor
that, besides supporting model construction and formal verification, incorporates support for a number
of additional methodological features (Guerson et al., 2015):


(i) **A Pattern-Based approach for Model Construction** : As demonstrated by (Guizzardi et al.,

2011; Guizzardi, 2014), OntoUML is actually a Pattern-Based Language in the sense that its
modeling primitives are _patterns_, i.e., higher-granularity clusters of modeling elements that can
appear in a model only in particular fixed configurations. Moreover, these patterns are of an
ontological nature, as they directly reflect the ontological micro-theories underlying the language.
Examples include the _role with disjoint allowed types_ modeling pattern proposed by (Guizzardi
et al., 2004a), the relator-material relation pattern (Guizzardi & Wagner, 2008), the _qualities with_
_alternative quality spaces_ pattern (Guizzardi et al., 2006), among many others. Furthermore, the
editor also implements a number of topological patterns that allows for isolating the scope of
transitivity of part-whole relations (Guizzardi, 2009). Finally, the editor allows for the extraction
of _Domain-Related Patterns_ from Core Ontologies (e.g., the _Employment_, _Organization Structure_
and _Project Involvement_ patterns exemplified by (Ruy et al., 2015)) such that these patterns can
be reused for the construction of Domain Ontologies;
(ii) **Model Verbalization** : Model verbalization stands for the activity of generating a rendering of
the model in (controlled) natural language. This process is very useful, for example, to allow
domain experts that are not well-versed in the modeling language’s notation, to access a partial
view of what is represented in a conceptual model. The editor incorporates a functionality for
automatically generating model verbalization in structured English following a slightly modified
version of the _SBVR_ ( _Semantics for Business Vocabularies and Rules_ ) OMG proposal; [3]


[2http://www.sparxsystems.com.au/.](http://www.sparxsystems.com.au/)
[3http://www.omg.org/spec/SBVR/1.2/.](http://www.omg.org/spec/SBVR/1.2/)


_G. Guizzardi et al. / Towards ontological foundations for conceptual modeling_ 265


(iii) **Support for the Representation of Domain-Specific Formal Constraints** : In order to cover
domain constraints that cannot be represented using the language’s diagrammatic notation, the
current editor supports the specification of OCL (Guerson et al., 2014) and temporal OCL formal
constraints (Guerson & Almeida, 2015). The editor provides support for syntax highlighting,
code-completion and syntax verification (parsing) for textual constraints;
(iv) **Model Validation:** This approach addresses conceptual model validation by using _visual sim-_
_ulation_ . In particular, in the strategy proposed by (Benevides et al., 2010; Braga et al., 2010)
and implemented in this later version of the editor, we have the automatic generation of visual
instances (exemplars) of a given conceptual model such that the modeler can be confronted with
what her model is actually representing. In other words, the strategy is to systematically contrast
the set of formally-valid instances of a given conceptual model (automatically generated by the
visual simulator) with the set of _intended_ instances of that model (i.e., instances that represent
admissible state of affairs in reality), which exists only in the modeler’s mind. Once the modeler
detects a deviation between valid and intended instances (either due to _overconstraining_ or _un-_
_derconstraining_ of the model), she rectifies the model, for instance, by the inclusion of formal
domain-specific constraints;
(v) **Ontology Codification** : In the ontology engineering process defended by (Guizzardi, 2007b;
Guizzardi & Halpin, 2008; Guizzardi, 2010b), we have advocated a separation between the modeling approaches that should be used for the conceptual modeling phase of ontology engineering
and the representation approaches that could be used to realize alternative implementations of
a given ontology (as a conceptual model). For instance, given a conceptual model representing
a domain ontology in OntoUML, we can have different mappings to different codification languages (e.g., OWL DL, RDFS, F-Logic, Haskell, Relational Database languages, CASL, among
many others). The choice of each of these languages should be made to favor a specific set of
non-functional requirements. Moreover, within the solution space defined by these codification
languages, we have a multitude of choices regarding, for instance, decidability, completeness,
computational complexity, reasoning paradigm (e.g., closed versus open world, adoption of a
unique name assumption or not), expressivity (e.g., regarding the need for representing modal
constraints, higher-order types, relations of a higher arity), verification of finite satisfiability,
among many others. In the current version of the editor, we have implemented six different automatic mappings from OntoUML to OWL contemplating different transformation styles that were
designed to address different sets of non-functional requirements (Guizzardi & Zamborlini, 2014,
Zamborlini & Guizzardi, 2010). It is important to highlight that other authors have implemented
alternative mappings from OntoUML to languages such as XML (Baumann, 2009), Smalltalk
(Pergl et al., 2013), OWL (Barcelos et al., 2013) and a version of a Modal Prolog (Araujo, 2015);
(vi) **Anti-Pattern Detection and Rectification** : Given the diffusion of the language, we have managed to assemble a model repository containing OntoUML models in different domains (e.g.,
telecommunications, government, biodiversity, bioinformatics), different sizes (e.g., ranging
from dozens of concepts to thousand of concepts), and produced in different types of contexts
(e.g., ranging from academic exercises of novices to models produced by teams of practitioners
in industrial or government settings) (Sales & Guizzardi, 2015). By using this model repository
as a benchmark, in three different empirical studies, Guizzardi & Sales (2014), Sales & Guizzardi (2015) managed to show that this approach for model validation via visual simulation is
not only able to detect deviations between formally valid model instances and intended model
instances, but is also able to detect recurrent structures that tend to cause these deviations, i.e.,


266 _G. Guizzardi et al. / Towards ontological foundations for conceptual modeling_


_ontological anti-patterns_ . Once these anti-patterns are catalogued, they were able to devise solution patterns, i.e., solution proposals that eliminate the deviation between valid instances and
intended instances (Guizzardi & Sales, 2014; Sales & Guizzardi, 2015). The current version of
the editor implements both a mechanism for anti-pattern detection and an implementation of
these proposed rectification solutions. Sales and Guizzardi (2015) have presented a validation
study developed with a large industrial model and managed to empirically demonstrate, for the
vast majority of the identified anti-patterns, a very high correlation between the presence of these
anti-patterns and the adoption of our proposed solutions for ontology-based model enhancement.


**5. Learning from “** _**Systematic Language Subversions**_ **” to evolve UFO and OntoUML**


The observation of the application of OntoUML over the years conducted by a variety of groups in a
variety of domains also amounted to a very fruitful empirical source of knowledge for us regarding the
language and its foundations. In particular, we have managed to observe a number of different ways in
which people would slightly _subvert_ the syntax of the language, ultimately creating what we could call
“ _systematic subversions_ ” of the language. These “subversions” would (purposefully) produce models
that were grammatically incorrect, but which were needed to express the intended characterization of
their underlying conceptualizations that could not be expressed otherwise. Loosely speaking, following
the semiotic engineering principle of seeing representations as dialogues between designer and user
(de Souza, 2005), we had the feeling that the users of the language were “speaking to us” via these
“systematic subversions”.
One example is the representation of events in OntoUML models. As previously mentioned, the language was created to represent structural conceptual models expressing endurantistic aspects of reality.
However, systematically, a number of authors, in different institutions and in different domains (e.g.,
Moretto & Barcellos, 2014; U.S. Department of Defense, 2011) started to produce OntoUML models in
which perdurants (and perdurant relations) would appear as modeling primitives. These examples were
concrete cases of the need to also represent perdurants in structural conceptual models (Olivé, 2007). In
order to respond to these modeling requirements, we intend to, once more, employ the aforementioned
ontology-based language engineering process, extending the metamodel the language to incorporate the
ontological distinctions and axiomatization prescribed by UFO-B (Guizzardi et al., 2013a). Doing that,
however, requires that a number of new research problems be addressed. To cite one of these challenges,
given that the introduction of this new perspective substantially increases the complexity of the resulting
diagrams, new complexity management theories and tools for OntoUML diagrams need to be developed
(e.g., dealing with model filtering, modularization, viewpoint selection).
A second case systematic “language subversions” led us to reconsider some of the theoretical foundations underlying the language, i.e., it led us to rethink and evolve a core theory in UFO. As previously
mentioned, in the original version of UFO (and, hence, also in OntoUML), we had a number of ontological distinctions representing different sorts of universals. These include distinctions between substance
sortals (kinds), phased-sortals (roles and phases) and non-sortals (categories, mixins and role mixins).
These distinctions, however, were considered to be distinctions among _object universals_ . However, consciously ignoring this rule, users of the language started to systematically employ these distinctions
also when characterizing universals whose instances are _existentially dependent endurants_ (i.e., moments/aspects/particularized properties such as modes and relators). These “subversions” called our attention to the fact that, like full-fledged endurants, modes and relators also have their identity supplied


_G. Guizzardi et al. / Towards ontological foundations for conceptual modeling_ 267


by substance sortals (i.e., mode kinds and relator kinds) and are also subject of both essential and accidental properties. If these endurants can be subjects of modal properties, then they can also contingently
instantiate anti-rigid types. In other words, phases, roles, roleMixins, mixins, categories, etc., (as sorts
of types characterized by formal ontological meta-properties) could also be used to characterize mode
and relator universals. This realization triggered a process that led to a much richer theory of material
relations and particularized relational properties in UFO, which in turn triggered an evolution of the
OntoUML model, with direct interesting consequences to the practice of conceptual modeling (Guarino
& Guizzardi, 2015). In fact, in an upcoming version of UFO, these different sorts of universals will
be applicable to all categories of endurant universals, including the so-called _powertypes_ . Powertypes
can be loosely defined as “types whose instances are other types” (e.g., the type _Organization Position_,
which can be instantiated by the types _Director_, _Manager_ and _Secretary_, or the type _Bird Species_, which
can be instantiated by the types _Golden Eagle_ and _Emperor Penguin_ ). Guizzardi et al. (2015) defend that
powertypes should not be interpreted as higher-order universals but as concrete _resemblance structures_
(Armstrong, 1990) that are themselves _endurants_ .
With the increasing popularization of OntoUML and its associated tools, this dialogue with language
users will continue, with more implications to be drawn to OntoUML and UFO from their practical applications in various domains. In this way, the evolution of the language and its conceptual foundations
can remain anchored in the conceptual modeling discipline, not only taking the real-world semantics
of conceptual modeling primitives seriously, but also addressing recurrent conceptual modeling problems against the solid background of formal ontology. We believe this combined use of insights from
theory and practice is key to applied ontology in general, but is essential to ontology-driven conceptual
modeling.


**Acknowledgements**


The authors are grateful to Ricardo Falbo, Monalessa Barcellos, Nicola Guarino, John Mylopoulos,
Heinrich Herre and the members of NEMO for many years of fruitful collaboration. Finally, we would
like to express our gratitude to Terry Hapin, Alex Borgida and Yair Wand for their valuable comments
to a previous version of this paper.


**References**


Abel, M., Perrin, M. & Carbonera, J.L. (2015). Ontological analysis for information integration in geomodeling. _Earth Science_
_Informatics_, _8_ (1), 21–36.
Albuquerque, A. & Guizzardi, G. (2013). An ontological foundation for conceptual modeling datatypes based on semantic
reference spaces. In _7th IEEE International Conference on Research, Challenges in Information Science (RCIS 2013)_, Paris
(pp. 1–12). ISBN 978-1-4673-2912-5.
Albuquerque, A.C.F., Campos dos Santos, J.L., De Castro, A.N. & OntoBio (2015). A biodiversity domain ontology for Amazonian biological collected objects. In _48th Hawaii International Conference on System Sciences (HICSS)_ .
Almeida, J.P.A. & Guizzardi, G. (2013). An ontological analysis of the notion of community in the RM-ODP enterprise language. _Computer Standards & Interfaces_, _35_ [(3), 257–268. doi:10.1016/j.csi.2012.01.007.](http://dx.doi.org/10.1016/j.csi.2012.01.007)
Andreeva, E., et al. (2015). One solution for semantic data integration in logistics. In _Enterprise and Organizational Modeling_
_and Simulation_ . Lecture Notes in Business Information Processing (Vol. 231, pp. 75–86).
Araujo, L.C. (2015). _An ontology-based language to formalize discourses_ . PhD Thesis, University of Brasilia, Brazil.
Armstrong, D.M. (1990). _A Theory of Universals, Vol. 2: Universals and Scientific Realism_ . Cambridge University Press.
Azevedo, C., Almeida, J.P.A., van Sinderen, M.J., Quartel, D. & Guizzardi, G. (2011). An ontology-based semantics for the motivation extension to archimate. In _15th IEEE International Conference on Enterprise Computing (EDOC 2011)_, Helsinki,
Finland.


268 _G. Guizzardi et al. / Towards ontological foundations for conceptual modeling_


Azevedo, C., Iacob, M.E., Almeida, J.P., Pires, L.F. & Guizzardi, G. (2015). _Modeling Resources and Capabilities in Enterprise_
_Architecture: A Well-Founded Ontology-Based Proposal for ArchiMate, Information Systems_ . Oxford University Press.
Barcelos, P.P.F., dos Santos, V.A., Silva, F.B., Monteiro, M.E. & Garcia, A.S. (2013). An automated transformation from
OntoUML to OWL and SWRL. In _Ontobras_ (pp. 130–141).
Barcelos, P.P.F., Guizzardi, G., Garcia, A.S. & Monteiro, M.E. (2011). Ontological evaluation of the ITU-T recommendation
G.805. In _18th International Conference on Telecommunications (ICT 2011)_ . Cyprus: IEEE Press.
Bauman, B.T. (2009). Prying apart semantics and implementation: Generating XML schemata directly from ontologically sound
conceptual models. In _Balisage Markup Conference_ .
Benevides, A.B., et al. (2010). Validating modal aspects of OntoUML conceptual models using automatically generated visual
world structures. _Journal of Universal Computer Science_, _16_, 2904–2933.
Benevides, A.B. & Guizzardi, G. (2009). A model-based tool for conceptual modeling and domain ontology engineering in
OntoUML. In _11th International Conf. on Enterprise Information Systems (ICEIS)_, Milan.
Bera, P. & Wand, Y. (2004). Analyzing OWL using a philosophy-based ontology. In _Formal Ontology in Information Systems_,
Amsterdam: IOS Press.
Blackburn, M.A. & Denno, P.O. (2015). Using semantic web technologies for integrating domain specific modeling and analytical tools. In _Complex Adaptive Systems_, San Jose, CA, November 2–4. Elsevier.
Bradley, F.H. (1893). _Appereance and Reality_ . London: George Allen & Unwin Ltd.
Braga, B., Almeida, J.P.A., Guizzardi, G. & Benevides, A.B. (2010). Transforming OntoUML into alloy: Towards conceptual
model validation using a lightweight formal method, innovations. In _System and Software Engineering (ISSE)_ . Springer.
Brandt, P., Basten, T. & Stuijk, S. (2014). In _ContoExam: An Ontology on Context-Aware Examinations, 8th International_
_Conference on Formal Ontology in Information Systems (FOIS 2014)_, Rio de Janeiro, Brazil.
Buckl, S., Matthes, F. & Schweda, C.M. (2011). A method to develop EA modeling languages using practice-proven solutions.
In _Advances in Enterprise Engineering V_ . Lecture Notes in Business Information Processing (Vol. 79).
Bunge, M. (1977). _Treatise on Basic Philosophy. Vol. 3. Ontology I. The Furniture of the World_ . New York: D. Reidel Publishing.
Carbonera, J., Abel, M. & Scherer, C.M.S. (2015). Visual interpretation of events in petroleum exploration: An approach
supported by well-founded ontologies. _Expert Systems with Applications_, _42_ (5), 2749–2763.
Carolla, M. & Spitta, T. (2014). _Methodological aspects of a data reference model for campus management systems_ . Technical
Report, Fakultät für Wirtschaftswissenschaften, University of Bielefeld.
Carolo, F. & Burlamaqui, L. (2011). Improving web content management with semantic technologies. In _Semantic Technology_
_Conference (SemTech)_, San Francisco.
Carraretto, R. (2010). _A modeling infrastructure for OntoUML_ . Technical Report, Ontology and Conceptual Modeling Research, Group (NEMO), Federal University of Espírito, Santo, Brazil.
Collier, A. (1994). _Critical Realism: An Introduction to Roy Bhaskar’s Philosophy_ . London, England: Verso.
Costal, D., Goméz, C. & Guizzardi, G. (2011). Formal semantics and ontological analysis for understanding subsetting, specialization and redefinition of associations in UML. In _30th International Conference on Conceptual Modeling (ER 2011)_,
Brussels, Belgium.
Davidson, D. (2001). The logical form of action sentences. In _Essays on Actions and Events_ . Oxford University Press. ISBN
9780199246274.
De Souza, C.S. (2005). _The Semiotic Engineering of Human-Computer Interaction_ . MIT Press.
Evermann, J. & Wand, Y. (2001). Towards ontologically based semantics for UML constructs. In H. Kunii, S. Jajodia and A.
Solvberg (Eds.), _Proceedings of the 20th International Conference on Conceptual Modeling (ER)_, Japan.
Gonçalves, B.N., Guizzardi, G. & Pereira Filho, J.G. (2011). Using an ECG reference ontology for semantic interoperability
of ECG data. In B. Smith, W. Ceusters and R.H. Scheuermann (Eds.), _Journal of Biomedical Informatics_ . Elsevier. Special
Issue on Ontologies for Clinical and Translational Research.
Griffo, C., Almeida, J.P.A. & Guizzardi, G. (2015). Towards a legal core ontology based on Alexy’s theory of fundamental
rights. In _(MWAIL 2015) ICAIL Multi-Lingual Workshop on AI & Law, 15th International Conference on Artificial Intelli-_
_gence and Law (ICAIL 2015)_, San Diego.
Grueau Grueau, C. (2014). Towards a domain specific modeling language for agent-based modeling of land use/cover change.
In _Advances in Conceptual Modeling_ . Lecture Notes in Computer Science (Vol. 8697, pp. 267–276).
Guarino, N. & Guizzardi, G. (2006). In the defense of ontological foundations for conceptual modeling. _Scandinavian Journal_
_of Information Systems_, _18_ (1). ISSN 0905-0167.
Guarino, N. & Guizzardi, G. (2015). “We need to discuss the relationship”: Revisiting relationships as modeling constructs. In
_27th International Conference on Advanced Information Systems Engineering (CAISE 2015)_, Stockholm.
Guarino, N. & Welty, C. (2009). An overview of OntoClean. In S. Staab and R. Studer (Eds.), _Handbook on Ontologies_ (2nd
edn., pp. 201–220). Springer.
Guerson, J. & Almeida, J.P.A. (2015). Representing dynamic invariants in ontologically well-founded conceptual models. In
_20th International Conference, EMMSAD_ .


_G. Guizzardi et al. / Towards ontological foundations for conceptual modeling_ 269


Guerson, J., Almeida, J.P.A. & Guizzardi, G. (2014). Support for domain constraints in ontologically well-founded conceptual
models. In _19th International Conference on Exploring Modeling Methods for Systems Analysis and Design (EMMSAD_
_2014)_, Thessaloniki, Greece.
Guerson, J., Sales, T.P., Guizzardi, G. & Almeida, J.P.A. (2015). A model-based environment to build, evaluate and implement
reference ontologies. In O. Lightweight (Ed.), _19th IEEE Enterprise Computing Conference (EDOC 2015), Demo Track_,
Adelaide, Australia.
Guizzardi, G. (2005). Ontological foundations for structural conceptual models. In _Telematics Instituut Fundamental Research_
_Series_ (Vol. 015). The Netherlands. ISSN 1388-1795.
Guizzardi, G. (2006). Agent roles, qua individuals and the counting problem. In P. Giorgini, A. Garcia, C. Lucena and R.
Choren (Eds.), _Software Engineering of Multi-Agent Systems, Vol. IV_ . Springer.
Guizzardi, G. (2007a). Modal aspects of object types and part–whole relations and the de re/de dicto distinction. In _19th Inter-_
_national Conference on Advanced Information Systems Engineering (CAISE’07), Trondheim_ . Lecture Notes in Computer
Science (Vol. 4495). Springer.
Guizzardi, G. (2007b). On ontology, ontologies, conceptualizations, modeling languages, and (meta)models. In _Frontiers in_
_Artificial Intelligence and Applications, Databases and Information Systems IV_ . Amsterdam: IOS Press.
Guizzardi, G. (2009). The problem of transitivity of part-whole relations in conceptual modeling revisited. In _21st Intl. Conf._
_on Advanced Information Systems Engineering (CAISE’09)_ . The Netherlands.
Guizzardi, G. (2010a). On the representation of quantities and their parts in conceptual modeling. In _6th International Conf. on_
_Formal Ontology and Information Systems (FOIS’10)_, Toronto, Canada.
Guizzardi, G. (2010b). Theoretical foundations and engineering tools for building ontologies as reference conceptual models.
_Semantic Web Journal_ . Editors-in-Chief: Pascal Hitzler and Krzysztof Janowicz. Amsterdam: IOS Press.
Guizzardi, G. (2011). Ontological foundations for conceptual part-whole relations: The case of collectives and their parts. In
_23rd International Conference on Advanced Information System Engineering (CAiSE’11)_, London, UK.
Guizzardi, G. (2012). Ontological meta-properties of derived object types. In _24th International Conference on Advanced_
_Information System Engineering (CAiSE’12)_, Gdansk, Poland.
Guizzardi, G. (2013). Ontology-based evaluation and design of visual conceptual modeling languages. In I. Reinhartz-Berger,
A. Sturm, T. Clark, S. Cohen and J. Bettin (Eds.), _Domain Engineering. Product Lines, Languages and Conceptual Models_
(p. 345). New York: Springer.
Guizzardi, G. (2014). In _Ontological Patterns, Anti-Patterns and Pattern Languages for Next-Generation Conceptual Modeling,_
_Conceptual Modeling (ER 2014)_, Atlanta, USA.
Guizzardi, G. (2015). Logical, ontological and cognitive aspects of objects types and cross-world identity with applications to
the theory of conceptual spaces. In P. Gardenfors and F. Zenker (Eds.), _Applications of Conceptual Space: The Case for_
_Geometric Knowledge Representation_ . Synthese Library. Dordrecht: Springer.
Guizzardi, G., et al. (2006). In the defense of a trope-based ontology for conceptual modeling: An example with the foundations
of attributes, weak entities and datatypes. In _25th International Conference on Conceptual Modeling (ER’2006)_, Tucson.
Guizzardi, G., et al. (2011). Design patterns and inductive modeling rules to support the construction of ontologically wellfounded conceptual models in OntoUML. In _3rd International Workshop on Ontology-Driven Information Systems (ODISE_
_2011)_, London, UK.
Guizzardi, G., et al. (2013a). Towards ontological foundations for the conceptual modeling of events. In _32nd International_
_Conf. on Conceptual Modeling (ER 2013)_, Hong Kong.
Guizzardi, G., Almeida, J.P.A., Guarino, N. & Carvalho, V.A. (2015). Towards an ontological analysis of powertypes, international workshop on formal ontologies for artificial intelligence (FOFAI 2015). In _24th International Joint Conference on_
_Artificial Intelligence (IJCAI 2015)_, Buenos Aires.
Guizzardi, G., Falbo, R.A. & Guizzardi, R.S.S. (2008). Grounding software domain ontologies in the unified foundational ontology (UFO): The case of the ODE software process ontology. In _11th Iberoamerican Conference on Software Engineering_
_(CIbSE 2008)_, Recife.
Guizzardi, G., Ferreira Pires, L. & van Sinderen, M. (2005). An ontology-based approach for evaluating the domain appropriateness and comprehensibility appropriateness of modeling languages. In _ACM/IEEE 8th International Conference on_
_Model Driven Engineering Languages and Systems_, Montego Bay, Jamaica. Lecture Notes in Computer Science (Vol. 3713).
Springer.
Guizzardi, G. & Halpin, T. (2008). Ontological foundations for conceptual modeling. _Applied Ontology_, _3_, 91–110.
Guizzardi, G., Herre, H. & Wagner, G. (2002a). On the general ontological foundations of conceptual modeling. In _21st Inter-_
_national Conf. on Conceptual Modeling (ER 2002)_, Tampere.
Guizzardi, G., Herre, H. & Wagner, G. (2002b). Towards ontological foundations for UML conceptual models. In _1st Interna-_
_tional Conference on Ontologies Databases and Applications of Semantics (ODBASE)_, USA.
Guizzardi, G., Lopes, M., Baião, F. & Falbo, R. (2010). The role of foundational ontologies for domain ontology engineering:
An industrial case study in the domain of oil and gas exploration and production. _International Journal of Information_
_Systems Modeling and Design_, _1_ (2), 1–22.


270 _G. Guizzardi et al. / Towards ontological foundations for conceptual modeling_


Guizzardi, G. & Sales, T.P. (2014). Detection, simulation and elimination of semantic anti-patterns in ontology-driven conceptual models. In _Proc. of 33rd International Conf. on Conceptual Modeling (ER 2014)_, Atlanta.
Guizzardi, G. & Wagner, G. (2004). On a unified foundational ontology and some applications of it in business modeling. In
_Open INTEROP workshop on enterprise modelling and ontologies for interoperability, 16th International Conference on_
_Advances in Information Systems Engineering (CAiSE)_, Latvia.
Guizzardi, G. & Wagner, G. (2008). What’s in a relationship: An ontological analysis. In _Conceptual Modeling (ER 2008)_ .
Lecture Notes in Computer Science (Vol. 5231, pp. 83–97). Barcelona, Spain. 2008.
Guizzardi, G. & Wagner, G. (2010). Towards and ontological foundation of discrete event simulation. In _16th International_
_Winter Simulation Conference_ .
Guizzardi, G. & Wagner, G. (2011a). Towards and ontological foundation of agent-based simulation. In _17th International_
_Winter Simulation Conference (WSC 2011)_, Phoenix, USA.
Guizzardi, G. & Wagner, G. (2011b). Can BPMN be used for simulation models? In _7th International Workshop on Enterprise_
_& Organizational Modeling and Simulation (EOMAS 2011), Together with the 23rd International Conference on Advanced_
_Information System Engineering (CAiSE’11)_, London, UK.
Guizzardi, G. & Wagner, G. (2012). Conceptual simulation modeling with OntoUML. In _Proceedings of the 2012 Winter_
_Simulation Conference_, Berlin, Germany.
Guizzardi, G. & Wagner, G. (2013). Disposition and causal laws as the ontological foundation of transition rules in simulation
models. In _Proceedings of the 2013 Winter Simulation Conference_, Washington DC, USA.
Guizzardi, G., Wagner, G., Guarino, N. & van Sinderen, M. (2004a). An ontologically well-founded profile for UML conceptual
models. In _16th International Conference on Advanced Information Systems Engineering (CAiSE)_, Latvia.
Guizzardi, G., Wagner, G. & Herre, H. (2004b). On the foundations of UML as an ontology representation language. In _Pro-_
_ceedings of 14th International Conference on Knowledge Engineering and Knowledge Management (EKAW)_ . Lecture Notes
in Computer Science. Berlin: Springer.
Guizzardi, G. & Zamborlini, V. (2014). Using a trope-based foundational ontology for bridging different areas of concern in
ontology-driven conceptual modeling. _Science of Computer Programming_, _96_, 417–443.
Guizzardi, R., Li, F.-L., Borgida, A., Guizzardi, G., Horkoff, J. & Mylopoulos, J. (2014). An ontological interpretation of nonfunctional requirements. In _8th International Conference on Formal Ontology in Information Systems (FOIS 2014)_, Rio de
Janeiro, Brazil.
Guizzardi, R.S.S., Franch, X. & Guizzardi, G. (2012). Applying a foundational ontology to analyze the i [∗] framework. In _6th_
_International Conference on Research Challenges in Information Systems (RCIS 2012)_, Valencia, Spain.
Guizzardi, R.S.S., Franch, X., Guizzardi, G. & Wieringa, R. (2013b). Ontological distinctions between means-end and contribution links in the i [∗] framework. In _32nd International Conference on Conceptual Modeling (ER 2013)_, Hong Kong.
Guizzardi, R.S.S. & Guizzardi, G. (2010). Ontology-based transformation framework from tropos to AORML. In _Social Mod-_
_eling for Requirements Engineering_ . Cooperative Information Systems Series. Boston: MIT Press.
Halpin, T. (2010). Object-role modeling: Principles and benefits. _International Journal of Information Systems Modeling and_
_Design_, _1_, 32–54. IGI Global.
Halpin, T. & Morgan, T. (2008). _Information Modeling and Relational Databases_ (2nd edn.). Morgan Kaufmann.
Heller, B. & Herre, H. (2004). Ontological categories in GOL. In _Axiomathes_ (Vol. 14, pp. 71–90). Kluwer Academic Publishers.
Heller, B., Herre, H., Burek, P., Loebe, F. & Michalek, H. (2004). General ontology language (GOL) – A formal framework
for building and representing ontologies, Onto-Med Report, Nr. 7. Research Group Ontologies in Medicine, University of
Leipzig.
Henderson-Sellers, B. (2012). _On the Mathematics of Modelling, Metamodelling, Ontologies and Modelling Languages_ .
Springer Briefs in Computer Science. Heidelberg: Springer. 106 pp.
Henderson-Sellers, B., et al. (2014). An ontology for ISO software engineering standards: 1 creating the infrastructure. _Com-_
_puter Standards & Interfaces_, _36_ (3), 563–576.
Hitchman, S. (2003). An interpretive study of how practitioners use entity-relationship modeling in a ternary relationship
situation. _Comm. Assoc. for Inf. Systems_, _11_, 451–485.
Kent, W. (1978). _Data and Reality_ . Elsevier Science.
Lowe, E.J. (2006). _The Four Category Ontology_ . Oxford University Press.
Masolo, C., Borgo, S., Gangemi, A., Guarino, N. & Oltramari, A. (2003). Ontology library. WonderWeb Deliverable D18.
Masolo, C., Guizzardi, G., Vieu, L., Bottazzi, E. & Ferrario, R. (2005). Relational roles and qua individuals. In _AAAI Fall_
_Symposium on Roles, an Interdisciplinary Perspective_, Virginia, USA.
Mealy, G.H. (1967). Another look at data. In _AFIPS Conference Proceedings_ (Vol. 31, pp. 525–534). Washington, DC: Thompson Books, London: Academic Press.
Moreira, et al. (2014). OntoWarehousing – Multidimensional design supported by a foundational ontology: A temporal perspective. In _Data Warehousing and Knowledge Discovery_ . Lecture Notes in Computer Science (Vol. 8646, pp. 35–44).
Springer.


_G. Guizzardi et al. / Towards ontological foundations for conceptual modeling_ 271


Moreira, J., et al. (2015). Developing situation-aware applications for disaster management with a distributed rule-based platform. In _Proceedings of the RuleML 2015 Doctoral Consortium 9th International Web Rule Symposium (RuleML 2015)_,
Berlin.
Moretto, C. & Barcellos, M.P. (2014). A levels-based approach for defining software measurement architectures. _CLEI Eletronic_
_Journal_, _17_ (3), Montevideo.
Mylopoulos, J. (1992). Conceptual modeling and Telos. In P. Loucopoulos and R. Zicari (Eds.), _Conceptual Modeling,_
_Databases, and CASE_ (Chapter 2; pp. 49–68). Wiley.
Nardi, J.C., de Almeida Falbo, R., Almeida, J.P.A., Guizzardi, G., Pires, L.F., van Sinderen, M.J., Guarino, N. & Fonseca, C.M.
(2015). _A Commitment-Based Reference Ontology for Services, Information Systems_ . Elsevier.
Nijenhuis, C.F. (2011). Automatic generation of graphical domain ontology editors. University of Twente.
Nunes, R.P., et al. (2015). Measurement ontology pattern language applied to network performance measurement. In _Brazilian_
_Seminar on Ontological Research (Ontobras 2015)_, São Paulo, Brazil.
Olivé, A. (2007). _Conceptual Modeling of Information Systems_ . Springer.
Parsons, T. (1990). _Events in the Semantics of English: A Study in Subatomic Semantics_ . Cambridge, MA: MIT Press.
Pereira, L.D., Calhau, R.F., Santos Junior, P.S. & Costa, M.B. (2015). Ontologia de domínio de doação de órgãos e tecidos para
apoio a integração semântica de sistemas (A domain ontology for organ and tissue donation and its support for semantic
system integration). In _18th Ibero-American Conference on Software Engineering (CIbSE 2015)_ .
Pergl, R., Sales, T.P. & Rybola, Z. (2013). Towards OntoUML for software engineering: From domain ontology to implementation model. In _Model and Data Engineering_ . Lecture Notes in Computer Science (Vol. 8216, pp. 249–263). Springer.
Ruy, F.B., Reginato, C.C., Santos, V.A., Falbo, R.A. & Guizzardi, G. (2015). Ontology engineering by combining ontology
patterns. In _34th International Conference on Conceptual Modeling (ER’2015)_, Stockholm, Sweden.
Salles, T.P. & Guizzardi, G. (2015). Ontological anti-patterns: Empirically uncovered error-prone structures in ontology-driven
conceptual models. _Data & Knowledge Engineering_, _99_, 72–104.
Santos, P.S. Jr., Almeida, J.P.A. & Guizzardi, G. (2010). An ontology-based semantic foundation for ARIS EPCs. In _25th ACM_
_Symposium on Applied Computing (ACM SAC 2010)_, Sierre, Switerland.
Santos, P.S. Jr., Almeida, J.P.A. & Guizzardi, G. (2013). _An Ontology-Based Analysis and Semantics for Organizational Struc-_
_ture Modeling in the ARIS Method_ . Oxford: Information Systems.
Serra, S.M.S.C., et al. (2012). A foundational ontology to support scientific experiments. In _Proceedings of Joint V Seminar on_
_Ontology Research in Brazil and VII International Workshop on Metamodels, Ontologies and Semantic Technologies_ .
Shekhovtsov, V.A. & Mayr, H.C. (2014). Managing quality related information in software development processes. In _Pro-_
_ceedings of the CAiSE 2014 Forum, 26th International Conference on Advanced Information Systems Engineering (CAiSE_
_2014)_, Thessaloniki, Greece (pp. 18–20).
U.S. Department of Defense (2011). Data modeling guide (DMG) for an enterprise logical data model (ELDM). available
[online, http://www.omgwiki.org/architecture-ecosystem/lib/exe/fetch.php?media=dmg_for_enterprise_ldm_v2_3.pdf.](http://www.omgwiki.org/architecture-ecosystem/lib/exe/fetch.php?media=dmg_for_enterprise_ldm_v2_3.pdf)
Veres, C. & Hitchman, S. (2002). Using psychology to understand conceptual modeling. In _10th European Conference on_
_Information Systems (ECIS 2002)_, Poland.
Veres, C. & Mansson, G. (2005). Cognition and modeling: Foundations for research and practice’. _Journal of Information_
_Technology Theory and Application_, _7_ (1), 93–104.
Wand, Y., Storey, V.C. & Weber, R. (1999). An ontological analysis of the relationship construct in conceptual modeling. _ACM_
_Trans. on Database Systems_, _24_ (4), 494–528.
Wand, Y. & Weber, R. (1989). An ontological evaluation of systems analysis and design methods. In E.D. Falkenberg and P.
Lindgreen (Eds.), _Information System Concepts: An in-Depth Analysis_ . North-Holland.
Wand, Y. & Weber, R. (1990). An ontological model of an information system. _IEEE Trans. Software Eng._, _16_ (11), 1282–1292.
Weber, R. (1997). _Ontological Foundations of Information Systems_ . Melbourne: Coopers & Lybrand.
Weber, R. & Zhang, Y. (1991). An ontological evaluation of NIAM’s grammar for conceptual schema diagrams. In _ICIS 1991_
_Proceedings_ (Paper 48).
Werlang, R. (2015). _Ontology-based approach for standard formats integration in reservoir modeling_ . M.Sc. Thesis, Federal
University of Rio Grande do Sul.
Zamborlini, V. & Guizzardi, G. (2010). On the representation of temporally changing information in OWL. In _15th IEEE_
_International Enterprise Computing Conference (EDOC 2010) Workshop Proceedings_, Vitória, Brazil.


