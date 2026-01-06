<!-- Source: 05-DOLCE_Descriptive_Ontology.pdf | Chunk 2/2 -->

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


_SpeedUp_ ( _x_ ) _→_ ACC( _x_ ) (28)


The formulas above state that a person is an agentive physical object, speed is a quality of perdurants,
a space of speed measure is a physical region, walking and running are processes, speeding up is an
accomplishment. The elements and the temporal constraints:


_Person_ ( _p_ ) _∧_ PD( _e_ ) _∧_ _Walk_ ( _e_ 1) _∧_ _SpeedUp_ ( _e_ 2) _∧_ _Run_ ( _e_ 3) _∧_


_SpeedQuality_ ( _s_ ) _∧_ _SpeedQuality_ ( _s_ 1) _∧_ _SpeedQuality_ ( _s_ 2) _∧_ _SpeedQuality_ ( _s_ 3) _∧_


T( _te_ ) _∧_ T( _te_ 1) _∧_ T( _te_ 2) _∧_ T( _te_ 3) (29)


The formula says that _p_ is a person, that there is a perdurant _e_, a walking perdurant _e_ 1, a speeding-up
perdurant _e_ 2, a running perdurant _e_ 3, that _s_ and _si_ are speed qualities, and that _te_, _te_ 1, _te_ 2, _te_ 3 are times.


The following formula states that _p_ exists during the time _te_ :


PRE( _p_, _te_ ) (30)


Relational claims (note that DOLCE already ensures that the quale "l" is in the speed space):


P( _l_, _S peedS pace_ ) _∧_ P( _l_ 1, _S peedS pace_ ) _∧_


P( _l_ 2, _S peedS pace_ ) _∧_ P( _l_ 3, _S peedS pace_ ) _∧_


qt( _s_, _e_ ) _∧_ ql( _l_, _s_, _te_ ) _∧_ qt( _s_ 1, _e_ 1) _∧_ ql( _l_ 1, _s_ 1, _te_ 1) _∧_


qt( _s_ 2, _e_ 2) _∧_ ql( _l_ 2, _s_ 2, _te_ 2) _∧_ qt( _s_ 3, _e_ 3) _∧_ ql( _l_ 3, _s_ 3, _te_ 3) _∧_


_e_ = _e_ 1 + _e_ 2 + _e_ 3 _∧_ PCC( _p_, _e_ ) (31)


This formula says that _l_, _l_ 1, _l_ 2 and _l_ 3 are locations in _S peedS pace_ . It also states that _s_, _s_ 1, _s_ 2 and _s_ 3 are
qualities of the perdurants _e_, _e_ 1, _e_ 2 and _e_ 3, respectively, and have locations _l_, _l_ 1, _l_ 2 and _l_ 3. Finally, it states
that _p_ constantly participates in the perdurant _e_ which is the sum of the perdurants _e_ 1, _e_ 2, _e_ 3.


We can now characterize the core property of walking and of running: these are events across which
the speed of the participant is qualitatively stable. This is what formula (32) states by enforcing the speed
quality of a walking (or of a running) perdurant to remain in the same position during the perdurant, say


18 _S. Borgo et al. / DOLCE_


within the range for walking or for running. [14] A speeding up event is an event in which the frequency of
a process increases. In the specific case, the change leads to move from a walking to a running process.
To characterize events in which speed regularly changes, we introduce formula (33): this formula states
that there is at least one speed change during the event, and that any speed change during the event can
only increase the speed (here < _speed_ is the ordering in the speed quality space).


(qt( _s_, _x_ ) _∧_ ( _Walk_ ( _x_ ) _∨_ _Run_ ( _x_ ))) _→∀li_, _l j_, _ti_, _t_ _j_ (ql( _li_, _s_, _ti_ ) _∧_


ql( _l_ _j_, _s_, _t_ _j_ ) _∧_ P( _ti_, _tx_ ) _∧_ P( _t j_, _tx_ ) _→_ _li_ = _l j_ ) (32)


_qt_ ( _s_, _x_ ) _∧_ _SpeedUp_ ( _x_ ) _→_


_∃li_, _l j_, _ti_, _t_ _j_ (P( _ti_, _tx_ ) _∧_ P( _t_ _j_, _tx_ ) _∧_ ql( _li_, _s_, _ti_ ) _∧_ ql( _l_ _j_, _s_, _t_ _j_ ) _∧_ _li ̸_ = _l_ _j_ ) _∧_


_∀li_, _l_ _j_, _ti_, _t_ _j_ (P( _ti_, _tx_ ) _∧_ P( _t_ _j_, _tx_ ) _∧_ ql( _li_, _s_, _ti_ ) _∧_ ql( _l_ _j_, _s_, _t_ _j_ ) _→_ ( _li_ ⩽ _speed l_ _j ↔_ _ti_ < _t_ _j_ )) (33)


DOLCE and these formulas for the specific Case 3.2 suffice to model the example of this section. To
model continuity in speed change, one can use the approach exploited in formula (22).
As for the previous case, the model presented here shows the most natural modeling approach for this
kind of scenarios in DOLCE.


_3.4._ _Case 4: Event Change_


“A man is walking to the station, but before he gets there, he turns around and goes
home.”


Following the viewpoint of DOLCE, this case is composed of (sub)events that correspond to the execution of distinct plans: reaching the station and reaching home. The first event (a man walking to the
station) and the third (a man going home) are processes that are intended to be parts of a plan execution,
that is, parts of distinct accomplishments. The intermediate event is an accomplishment (turning towards
a direction) which is part of the second plan, namely, reaching home. To model this case, we need to
include in the formalization the purpose of the (sub) events.


The DOLCE categories that we need for modeling Case 4 are: physical object (POB), agentive physical
object (APO), concept (C), process (PRO), accomplishment (ACC), temporal quality (TQ), and time (T).
We will also use _DirectionQuality_ and _SpeedQuality_ as specialization of the quality category. In terms of
relations we use: _subsumption_ (IS_A), _constant participation_ (PCC), _being present_ (PRE), _mereological_
_sum_ (+), _parthood_ (P), _quale_ (ql), _inherence_ (qt), _classification_ (CF), _temporal order_ (<). In addition,
we introduce the new relationship _ExecutesPlan_ to connect a perdurant to a plan. This relation is used
to state that an event complies with the plan requirements. For instance, if a plan _p_ states that a person
must go first to point A and then to point B, then any event _e_ that takes that person to point A satisfies
_ExecutesPlan_ ( _e_, _p_ ) because it executes the plan even though it does not complete it. Figure 6 depicts
some relevant classes and relationships.


14
In DOLCE this can be done by measuring the quality in a qualitative speed space. For instance, take a space with two
values only, say, ‘regular speed’ and ‘varying speed’. When an event has only limited speed variations (e.g., according to the
granularity of that space), the associated speed quale is ‘regular speed’.


_S. Borgo et al. / DOLCE_ 19


Fig. 6. Fragment of the DOLCE taxonomy and relevant relationships for Case 4


Formally, Case 4 can be expressed as follows.


Taxonomic claims:


_Person_ ( _x_ ) _→_ APO( _x_ ) (34)


_DirectionQuality_ ( _x_ ) _→_ TQ( _x_ ) (35)


_SpeedQuality_ ( _x_ ) _→_ TQ( _x_ ) (36)


_Walk_ ( _x_ ) _→_ PRO( _x_ ) (37)


_Turn_ ( _x_ ) _→_ ACC( _x_ ) (38)


_Plan_ ( _x_ ) _→_ C( _x_ ) (39)


The previous formulas state that a person is an agentive physical object and that direction and speed
qualities are qualities of perdurants.
The elements we need to model this case are a person, a perdurant, two walking and a turning events,
two plans and three times:


_Person_ ( _a_ ) _∧_ PD( _e_ ) _∧_ _Walk_ ( _e_ 1) _∧_ _Turn_ ( _e_ 2) _∧_


_Walk_ ( _e_ 3) _∧_ _Plan_ ( _p_ 1) _∧_ _Plan_ ( _p_ 2) _∧_ T( _te_ 1) _∧_ T( _te_ 2) _∧_ T( _te_ 3) (40)


Stating the temporal constraints and the elements’ presence:


_te_ 1 < _te_ 2 < _te_ 3 _∧_ ql _T_ ( _te_ 1, _e_ 1) _∧_ ql _T_ ( _te_ 2, _e_ 2) _∧_ ql _T_ ( _te_ 3, _e_ 3) _∧_ PRE( _a_, _te_ ) _∧_ PRE( _p_ 1, _te_ 1) _∧_


PRE( _p_ 2, _te_ 2) _∧_ PRE( _p_ 2, _te_ 3) _∧¬_ PRE( _p_ 1, _te_ 2) _∧¬_ PRE( _p_ 1, _te_ 3) _∧¬_ PRE( _p_ 2, _te_ 1) (41)


20 _S. Borgo et al. / DOLCE_


Formula (41) states the ordering of the times, that _tei_ is the time of perdurant _ei_, that person _a_ is present
all the times, that plan _p_ 1 is present during _e_ 1 and plan _p_ 2 is during _e_ 2 and _e_ 3. It also says that plan _p_ 1 is
not present during _e_ 2 and _e_ 3 while plan _p_ 2 is not present during _e_ 1.
The following formula binds the use of the execution relation to pairs of one perdurant and one concept, we do not characterize it further:


_ExecutesPlan_ ( _x_, _y_ ) _→_ PD( _x_ ) _∧_ C( _y_ ) (42)


We now write _t_ 2 _i_ and _t_ 2 _f_ for the initial and final time of event _e_ 2:


_DirectionQuality_ ( _s_ ) _∧_ qt( _s_, _e_ ) _∧_ ql( _l_ 1, _s_, _te_ 1) _∧_ ql( _l_ 2, _s_, _te_ 2) _∧_ ql( _l_ 3, _s_, _te_ 3) _∧_


ql( _l_ 1, _s_, _t_ 2 _i_ ) _∧_ ql( _l_ 3, _s_, _t_ 2 _f_ ) _∧_ _l_ 1 _̸_ = _l_ 3 _∧_ _e_ = _e_ 1 + _e_ 2 + _e_ 3 _∧_ PCC( _a_, _e_ ) _∧_


_ExecutesPlan_ ( _e_ 1, _p_ 1) _∧_ _ExecutesPlan_ ( _e_ 2 + _e_ 3, _p_ 2) (43)


Formula (43) states that the direction quality _s_ of the event _e_ changes during the turning subevent _e_ 2,
and that event _e_ 1 executes plan _p_ 1 and event _e_ 2 + _e_ 3 executes plan _p_ 2. Finally, it states that _e_ 1, _e_ 2 and _e_ 3
span the whole event _e_ and that person _a_ participates to the whole event.
To state that an event _x_ is a walking event, we can use a formula similar to the one introduced in Case
3.2, reported below as (44). To characterize the core property of a turning event _y_, we use formula (45)
where _l_ 1 and _l_ 3 are as in formula (43) and write _ty_, _tyi_ and _ty f_ for the temporal interval of event _y_ and for
its initial and final instants, respectively. [15]


_SpeedQuality_ ( _s_ ) _∧_ qt( _s_, _x_ ) _∧_ _Walk_ ( _x_ ) _→_


_∀li_, _l_ _j_, _ti_, _t j_ (ql( _li_, _s_, _ti_ ) _∧_ ql( _l_ _j_, _s_, _t_ _j_ ) _∧_ P( _ti_, _tx_ ) _∧_ P( _t_ _j_, _tx_ ) _→_ _li_ = _l_ _j_ ) (44)


_DirectionQuality_ ( _s_ ) _∧_ qt( _s_, _y_ ) _∧_ _Turn_ ( _y_ ) _∧_ ql( _l_ 1, _s_, _tyi_ ) _∧_ ql( _l_ 3, _s_, _ty f_ ) _∧_ _ti_ < _t j ∧_


_l_ 1 < _l_ 3 _∧_ P( _ti_, _ty_ ) _∧_ P( _t_ _j_, _ty_ ) _∧_ ql( _li_, _s_, _ti_ ) _∧_ ql( _l j_, _s_, _t j_ ) _∧_ _li_ + _ri_ = _l_ _j_ + _r j_ = _l_ 3 _→_


0 ⩽ _r_ _j_ < _ri_ (45)


The modeling approach we followed here is the preferred one in DOLCE for this kind of scenarios.


_3.5._ _Case 5: Concept Evolution_


Background: marriage is a contract between two people that is present in most social
and cultural systems and it can change in major (e. g. gender constraints) and minor
(e.g. marriage breaking procedures) aspects. “Marriage is a contract that is regulated
by civil and social constraints. These constraints can change but the meaning of marriage continues over time.”


There is disagreement about the nature of concepts, including whether concepts can change in time
while preserving identity. Some argue that concepts have a stable nature (their characterizations cannot


15For completeness, one should add the symmetric condition for _li_  - _l_ _j_ .


_S. Borgo et al. / DOLCE_ 21


change in time), others argue the opposite (Masolo et al., 2019). Similarly to the case of artifacts presented in Sect. 3.1, DOLCE does not prescribe the adoption of one or the other view, allowing in this way
the knowledge engineer to select the approach that better fits with their modeling needs and world-view.
For instance, the example mentioned above assumes that concepts can persist through time while partially changing in their characterization. In particular, it points to a social scenario where the concepts
characterizing a socio-cultural system are associated with different rules across time because of the legal
and cultural evolution of the society. We shall therefore take this perspective for the sake of this case.


The DOLCE categories that we need for modeling Case 5 are: social object (SOB), concept (C), and
time (T). In terms of relations, we use: _subsumption_ (IS_A), _being present_ (PRE), and _classification_ (CF).
Figure 7 depicts the DOLCE classes and relationships used for Case 5.


Fig. 7. Fragment of the DOLCE taxonomy and relevant relationships for Case 5.


Formally, Case 5 can be expressed as follows.


Taxonomic claims (a social relationship, _SocRelationship_, holds for various types of unions between
people; the notions of social marriage and legal marriage are intended to be elements in the DOLCE
category of concepts):


_SocMarriage_ ( _x_ ) _→_ C( _x_ ) (46)


_LegMarriage_ ( _x_ ) _→_ C( _x_ ) (47)


_SocRelationship_ ( _x_ ) _→_ SOB( _x_ ) (48)


The elements and the temporal constraints that we need are: a social relationship _M_, a social concept
of marriage _sm_, two legal concepts of marriage and two times:


_SocRelationship_ ( _M_ ) _∧_ _SocMarriage_ ( _sm_ ) _∧_ _LegMarriage_ ( _lm_ ) _∧_ _LegMarriage_ ( _lm_ _[′]_ )


22 _S. Borgo et al. / DOLCE_


_∧_ T( _t_ ) _∧_ T( _t_ _[′]_ ) (49)


The social relationship holds in both times and so does the social marriage, one legal marriage concept
exists at _t_, the other at _t_ _[′]_ . Then, the elements’ presence is as follows:


PRE( _M_, _t_ ) _∧_ PRE( _M_, _t_ _[′]_ ) _∧_ PRE( _sm_, _t_ ) _∧_ PRE( _sm_, _t_ _[′]_ ) _∧_

PRE( _lm_, _t_ ) _∧¬_ PRE( _lm_, _t_ _[′]_ ) _∧¬_ PRE( _lm_ _[′]_, _t_ ) _∧_ PRE( _lm_ _[′]_, _t_ _[′]_ ) (50)


The relational claims are simple: first the two legal concepts are different; second if the social relationship is classified by the social marriage concept at a time, then it has to satisfy the legal concept existing
at that very time.


_lm ̸_ = _lm_ _[′]_ _∧_ CF( _sm_, _M_, _t_ ) _→_ CF( _lm_, _M_, _t_ ) _∧_ CF( _sm_, _M_, _t_ _[′]_ ) _→_ CF( _lm_ _[′]_, _M_, _t_ _[′]_ ) (51)


The same concept of social marriage ( _sm_ ) persists through time, from _t_ to _t_ _[′]_ while changing its legal
characterization (from _lm_ to _lm_ _[′]_ ). For _sm_ to classify a marriage relationship _M_ at _t_, it is necessary that
_M_ is also classified as a legal marriage _lm_ (so satisfying concept _lm_ is necessary at _t_ for _sm_ ), while at _t_ _[′]_

it is necessary that _M_ is classified by _sm_ which now depends on _lm_ _[′]_ .
The model presented here is quite natural in DOLCE for this kind of scenarios. By changing the assumptions we made in the initial discussion of this case, other approaches can be put forward like, e.g.,
the use of role theory applied to concepts. Note also that these modeling approaches are not limited to
purely social concepts. They apply to technology-dependent concepts like, e.g., that of road which has
different qualifications across history (e.g. in ancient Rome, during the 19th century or today).


**4. Ontology usage and community impact**


Foundational ontologies enjoy a double-edged reputation in several communities, spanning across
conceptual modeling, semantic web, natural language processing, etc. They are intuitively needed by
most data-intensive applications, but their precise utility at different steps of design methodologies is
not widely agreed, and certainly not for the same reasons. As a consequence, the wide application of
DOLCE ranges from the simple reuse of a few categories, to delving into full-fledged axiomatic versions.
We provide here a quick description of the OWL version of DOLCE, a list of application areas and
specific reuse cases, with a few comments on the current opportunity for foundational approaches to
ontology design. (For the new CLIF and OWL versions of DOLCE produced for the ISO 21838 standard
[under development, see http://www.loa.istc.cnr.it/index.php/dolce/).](http://www.loa.istc.cnr.it/index.php/dolce/)
DOLCE “lite” versions take into account the requirements from semantic web modeling practices, and
the need for simplified semantics as in natural language processing lexicons. They also address the need
for some extensions of DOLCE categories, by reusing the D&S (Description and Situations) ontology
pattern framework, which was early designed to overcome the expressivity limits of OWL, later much
facilitated by _punning_ in OWL2 W3C OWL Working Group (2012) (i.e. the ability to use a constant as
the name for a class, an individual, or a binary relation).
In particular, the DOLCE+D&S Ultralite [16] (DUL) OWL ontology was intended to popularize DOLCE to
the Semantic Web community. DUL uses DOLCE, D&S, and a few more ontology design patterns (Plan [17],


[16http://www.ontologydesignpatterns.org/ont/DUL/dul.owl](http://www.ontologydesignpatterns.org/ont/DUL/dul.owl)
[17http://www.ontologydesignpatterns.org/cp/owl/basicplan.owl](http://www.ontologydesignpatterns.org/cp/owl/basicplan.owl)


_S. Borgo et al. / DOLCE_ 23


Information Object [18], and Collection, that extend DOLCE. Presutti and Gangemi (2016) give an account
of DUL as an architecture of ontology design patterns inspired by those integrated theories, and Gangemi
(2008) offers an integrated axiomatization of plans, information objects and collections in D&S. DUL is
the result of various refinements and integrations of the OWL versions of those theories. The main
motivations why DUL was conceived include: (i) intuitive terminology (e.g. substituting Endurant and
Perdurant with Object and Event), (ii) lighter axiomatization (e.g. giving up some predicate indexing),
(iii) integration of other theories, (iv) semantic-web-oriented OWL2 modeling styles.
As reported in (Presutti and Gangemi, 2016), even a non-exhaustive search makes one stumble upon
the great variety of DUL reuse, citing 25 large ontology projects for: e-learning systems, water quality systems; in multimedia: annotation facets, content annotation, audiovisual formal descriptions; in
medicine: for modelling intracranial aneurysms, annotating medical images and neuroimages, and for
modelling biomedical research; law; events; geo-spatial data; robotics and automation; industry and
smart products, textile manufacturing; cybersecurity; enterprise integration; process mining; disaster
management; semantic sensor networks; customer relationship management.
In addition, DUL has been applied as a _tool_ to improve existing semantic resources. This has happened
for example in identifying and fixing millions of inconsistencies in DBpedia, on-the-go discovering modelling anti-patterns that were completely opaque to the axioms of the DBpedia ontology (Paulheim and
Gangemi, 2015). Another example is the DUL application to improve the quality of lexical resources,
from the very inception of DOLCE, used to reorganize the WordNet top level and causing Princeton
WordNet developers to include the individual/class distinction in their lexicon (Gangemi et al., 2003),
to the recent massive Framester knowledge graph (Gangemi et al., 2016), which unifies many different
linguistic databases under a frame semantics, and maps them to widely used ontologies under a common DUL hat. Several other standard or _de facto_ standard are based on or compatible with DUL, e.g.,
CIDOC CRM (CIDOC Conceptual Reference Model) [19], SSN (Semantic Sensor Network Ontology) [20]

and SAREF (Smart REFerence Ontology) [21] .


An important lesson learnt is that DOLCE can be used to foster different design approaches:


(1) as an _upper ontology_, in order to support a minimal agreement about a few distinctions;
(2) as an _expressive axiomatic theory_, in order to associate one’s ontological commitment to welldefined criteria, and to perform (detailed) meaning negotiation;
(3) as a coherence/consistency _stabilizer_, able to reveal problems in a conceptualization against both
its domain schema, and the data. This approach could also be used to reveal _unwanted_ inferences,
even when no inconsistency emerges;
(4) as a source of _patterns_ that improve the quality of ontologies by applying the good practices encoded in DOLCE, and eventually ameliorating semantic interoperability.


Especially (3) and (4) are central to the current needs of the huge knowledge graphs maintained by
the Web stakeholders, but also (2) is finally emerging as a potential tool to help clarifying the underlying
semantics in domains that have been less prone to formalization in the past (e.g. sociology).


[18http://www.ontologydesignpatterns.org/cp/owl/informationrealization.owl](http://www.ontologydesignpatterns.org/cp/owl/informationrealization.owl)
[19http://www.cidoc-crm.org/](http://www.cidoc-crm.org/)
[20https://w3c.github.io/sdw/ssn](https://w3c.github.io/sdw/ssn)
[21https://saref.etsi.org](https://saref.etsi.org)


24 _S. Borgo et al. / DOLCE_


**Acknowledgements**


Over the years many people have contributed to the application of DOLCE, to the discussion of the best
modeling approaches, and to the development of DOLCE’s modular extensions. We take the opportunity
to thank in particular Emanuele Bottazzi, Francesco Compagno and Alessandro Oltramari. DOLCE was
conceptualized and developed as part of the European project WonderWeb (IST-2001-33052) and many
public and industrial projects reused it since then. Among these, the authors thank the European project
OntoCommons (GA 958371) for co-funding the writing of this paper.


**References**


Biccheri, L., Ferrario, R. & Porello, D. (2020). Needs and Intentionality. In B. Brodaric and F. Neuhaus (Eds.), _Formal Ontology_
_in Information Systems - Proceedings of the 11th International Conference, FOIS 2020_ . Frontiers in Artificial Intelligence
and Applications (Vol. 330, pp. 125–139). Amsterdam, The Netherlands: IOS Press.
Borgo, S. & Masolo, C. (2009). Foundational Choices in DOLCE. In S. Staab and R. Studer (Eds.), _Handbook on Ontologies_
(2nd ed.). Springer.
Borgo, S. & Vieu, L. (2009). Artifacts in Formal Ontology. In A. Meijers (Ed.), _Handbook of the Philosophy of the Technolog-_
_ical Sciences. Technology and Engineering Sciences_ (Vol. 9, pp. 273–307). Elsevier.
Borgo, S., Carrara, M., Garbacz, P. & Vermaas, P.E. (2010). Formalizations of functions within the DOLCE ontology. In
_Proceedings of the Eighth International Symposium on Tools and Methods of Competitive Engineering TMCE_ (Vol. 1, pp.
113–126). Citeseer.
Borgo, S., Franssen, M., Garbacz, P., Kitamura, Y., Mizoguchi, R. & Vermaas, P.E. (2014). Technical artifacts: An integrated
perspective. _Appl. Ontology_, _9_ (3-4), 217–235.
Bottazzi, E. & Ferrario, R. (2009). Preliminaries to a DOLCE Ontology of Organizations. _International Journal of Business_
_Process Integration and Management, Special Issue on Vocabularies, Ontologies and Business Rules for Enterprise Model-_
_ing_, _4_ (4), 225–238.
Casati, R. & Varzi, A.C. (Eds.) (1996). _Events_ . Aldershot: Dartmund.
Conigliaro, D., Ferrario, R., Hudelot, C. & Porello, D. (2017). Integrating Computer Vision Algorithms and Ontologies for
Spectator Crowd Behavior Analysis. In V. Murino, M. Cristani, S. Shah and S. Savarese (Eds.), _Group and Crowd Behavior_
_for Computer Vision, 1st Edition_ (pp. 297–319). Academic Press. doi:10.1016/B978-0-12-809276-7.00016-3.
Ferrario, R. & Oltramari, A. (2004). Towards a Computational Ontology of Mind. In A.C. Varzi and L. Vieu (Eds.), _Formal_
_Ontology in Information Systems, Proceedigs of the Intl. Conf. FOIS 2004_ (pp. 287–297). IOS Press.
Ferrario, R. & Porello, D. (2015). Towards a Conceptualization of Sociomaterial Entanglement. In H. Christiansen, I. Stojanovic and G.A. Papadopoulos (Eds.), _Modeling and Using Context - 9th International and Interdisciplinary Conference,_
_CONTEXT 2015, Lanarca, Cyprus, November 2-6, 2015. Proceedings_ . Lecture Notes in Computer Science (Vol. 9405, pp.
32–46). Springer. doi:10.1007/978-3-319-25591-0_3.
Fitting, M. & Mendelsohn, R.L. (2012). _First-order modal logic_ (Vol. 277). Springer Science & Business Media.
Gangemi, A. (2008). Norms and plans as unification criteria for social collectives. _Autonomous Agents and Multi-Agent Systems_,
_17_ (1), 70–112. doi:10.1007/s10458-008-9038-9.
Gangemi, A., Guarino, N., Masolo, C. & Oltramari, A. (2003). Sweetening WORDNET with DOLCE. _AI Mag._, _24_ (3), 13–24.
doi:10.1609/aimag.v24i3.1715.
Gangemi, A., Alam, M., Asprino, L., Presutti, V. & Recupero, D.R. (2016). Framester: A Wide Coverage Linguistic Linked
Data Hub. In _EKAW_ .
Gärdenfors, P. (2000). _Conceptual Spaces: the Geometry of Thought_ . Cambridge, Massachussetts: MIT Press.
Guarino, N. (2009). The Ontological Level: Revisiting 30 Years of Knowledge Representation. In A. Borgida, V.K. Chaudhri, P.
Giorgini and E.S.K. Yu (Eds.), _Conceptual Modeling: Foundations and Applications - Essays in Honor of John Mylopoulos_ .
Lecture Notes in Computer Science (Vol. 5600, pp. 52–67). Springer. doi:10.1007/978-3-642-02463-4_4.
Guarino, N. & Welty, C.A. (2002). Evaluating ontological decisions with OntoClean. _Commun. ACM_, _45_ (2), 61–65.
doi:10.1145/503124.503150.
Guarino, N. & Welty, C. (2009). An Overview of OntoClean. In S. Staab and R. Studer (Eds.), _Handbook on Ontologies_ . International Handbooks on Information Systems (pp. 201–220). Springer Berlin Heidelberg. doi:10.1007/978-3-540-92673-3_9.
ISO 24707 (2018). _ISO/IEC-24707:2018 - Information technology — Common Logic (CL): a framework for a family of logic-_
_based languages_ . International Organization for Standardization.


_S. Borgo et al. / DOLCE_ 25


Kutz, O. & Mossakowski, T. (2011). A Modular Consistency Proof for DOLCE. In W. Burgard and D. Roth (Eds.), _Proceedings_
_of the Twenty-Fifth AAAI Conference on Artificial Intelligence, AAAI 2011, San Francisco, California, USA, August 7-11,_
_2011_ [. AAAI Press. http://www.aaai.org/ocs/index.php/AAAI/AAAI11/paper/view/3754.](http://www.aaai.org/ocs/index.php/AAAI/AAAI11/paper/view/3754)
Masolo, C., Borgo, S., Gangemi, A., Guarino, N. & Oltramari, A. (2003). WonderWeb Deliverable D18. Technical report,
CNR.
Masolo, C., Vieu, L., Bottazzi, E., Catenacci, C., Ferrario, R., Gangemi, A. & Guarino, N. (2004). Social Roles and their
Descriptions. In _Proceedings of the 9th International Conference on the Principles of Knowledge Representation and Rea-_
_soning (KR-2004)_ (pp. 267–277).
Masolo, C., Sanfilippo, E., Lamé, M. & Pittet, P. (2019). Modeling Concept Drift for Historical Research in the Digital Humanities. In _1st International Workshop on Ontologies for Digital Humanities and their Social Analysis (WODHSA)_ .
Mizoguchi, R., Kitamura, Y. & Borgo, S. (2016). A unifying definition for artifact and biological functions. _Appl. Ontology_,
_11_ (2), 129–154.
Paulheim, H. & Gangemi, A. (2015). Serving DBpedia with DOLCE - More than Just Adding a Cherry on Top. In _The Semantic_
_Web - ISWC 2015. ISWC 2015, Part I_ (pp. 180–196). Springer, Cham. doi:10.1007/978-3-319-25007-6_11.
Porello, D., Bottazzi, E. & Ferrario, R. (2014a). The Ontology of Group Agency. In P. Garbacz and O. Kutz (Eds.), _Formal_
_Ontology in Information Systems, Proceedigs of the Intl. Conf. FOIS 2014_ . Frontiers in Artificial Intelligence and its Applications (Vol. 267, pp. 183–196). IOS Press.
Porello, D., Bottazzi, E. & Ferrario, R. (2014b). The Ontology of Group Agency. In _FOIS_ (pp. 183–196).
Porello, D., Setti, F., Ferrario, R. & Cristani, M. (2013). Multiagent Socio-technical Systems. An Ontological Approach. In T.
Balke, F. Dignum, M.B. Riemsdijk and A.K. Chopra (Eds.), _Coordination, Organisations, Institutions and Norms in Agent_
_Systems IX (COIN 2013)_ . LNAI (Vol. 8368, pp. 42–63). Springer Verlag.
Presutti, V. & Gangemi, A. (2016). Dolce+D&S Ultralite and its main Ontology Design Patterns. _Ontology Engineering with_
_Ontology Design Patterns_, _25_, 81–103.
Vieu, L., Borgo, S. & Masolo, C. (2008). Artefacts and Roles: Modelling Strategies in a Multiplicative Ontology. In C. Eschenbach and M. Grüninger (Eds.), _Formal Ontology in Information Systems, Proceedings of the Fifth International Conference,_
_FOIS 2008, Saarbrücken, Germany, October 31st - November 3rd, 2008_ . Frontiers in Artificial Intelligence and Applications
(Vol. 183, pp. 121–134). IOS Press. doi:10.3233/978-1-58603-923-3-121.
W3C OWL Working Group (2012). _OWL 2 Web Ontology Language Document Overview (Second Edition) - W3C Recommen-_
_dation 11 December 2012_ [. World Wide Web Consortium (W3C). http://www.w3.org/TR/owl2-overview/.](http://www.w3.org/TR/owl2-overview/)


