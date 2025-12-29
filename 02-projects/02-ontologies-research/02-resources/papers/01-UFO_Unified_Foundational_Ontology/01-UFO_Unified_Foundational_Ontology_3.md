<!-- Source: 01-UFO_Unified_Foundational_Ontology.pdf | Chunk 3/4 -->



In Figure 8, we present an OntoUML model [17] representing this situation. In this model, a Rose is
modeled as a subkind of Flower. All flowers are bearers of a Color quality [18] . As for any quality, a
Flower Color [19] quality inheres in its bearer (the characterization relation). A perceivable quality takes
its value in a color domain (here modeled as a simple ordinal space of colors).


Figure 8. The Flower case in OntoUML.


In the sequel, we show a partial formalization of this case.


17In OntoUML, the simplest way to represent quality structures is as datatypes (Guizzardi, 2005). Classes stereotyped as
«enumeration» are particular types of datatypes. For a more sophisticated representation of these structures in the language, one
should refer to Albuquerque and Guizzardi (2013). We take here the simplest approach.
18To be precise, Color is a particular type of quality termed as Perceivable Quality by Albuquerque and Guizzardi (2013).
We omit this discussion here.
19Flower Color is a genuine subtype of Color given that it is associated with a particular subspace of possible values, which
is a proper part of the entire color spindle.


_Giancarlo Guizzardi et al. / UFO: Unified Foundational Ontology_ 25


ObjectKind(Flower)


SubKind(Rose)

Rose _⊑_ Flower


SubKind(Color)


SubKind(FlowerColor)

FlowerColor _⊑_ Color


QualityStructure(FlowerColorValues)


Now, the quality type Flower Color characterizes the object type Flower:


characterization(Flower _,_ FlowerColor)


Following (a81) and (a82), this implies:


_∀x._ ( _x_ :: Flower _→∃_ ! _y._ ( _y_ :: FlowerColor _∧_ inheresIn( _y, x_ )))

_∀z._ ( _z_ :: FlowerColor _→∃_ ! _w._ ( _w_ :: Flower _∧_ inheresIn( _z, w_ )))


Since Flower Color is a Quality Type, it is associated with a Quality Structure (a91):


associatedWith(FlowerColor _,_ FlowerColorValues)


As Quality Structures are non-empty sets of possible values that qualities can take (a86):


Red _∈_ FlowerColorValues _∧_ Yellow _∈_ FlowerColorValues _∧_
Brown _∈_ FlowerColorValues _∧_ White _∈_ FlowerColorValues


Given (a93) and (a94), each quality instance of Flower Color takes, in a given situation, a value in the
Flower Color Values Space:


_∀x._ ( _x_ :: FlowerColor _→∃_ ! _y._ ( _y ∈_ FlowerColorValues _∧_ hasValue( _x, y_ )))


Now, notice that inherence is an existential dependence relation and, hence, the connection between a
particular quality and its bearer is immutable. However, the relation of hasValue between a quality and
its value (qualia) in a quality structure is one of generic dependence. Therefore, the value of a given
Flower Color can change from situation to situation. In the sequel, we show examples (Figure 9) of the
visual models automatically generated for the OntoUML diagram of Figure 8.


Figure 9. In world _w_ 1, we have two roses Object0 (Object0 :: Rose, Object0 :: Flower) and Object1 (Object1 :: Rose,
Object1 :: Flower). These roses bear each a Flower Color quality (Property0 :: FlowerColor, inheresIn(Property0,
Object1), Property2 :: FlowerColor, inheresIn(Property2, Object0). In that situation, qualities Property0 and
Property2 have the color values Red and Brown, respectively. In world _w_ 2, Rose Object1 turns from Red to Brown (by having
its quality Property0 assuming the new value), and Rose Object0 turns from Brown to White (again, by having its quality
Property2 taking the new value).


_3.b) “A man is walking when suddenly he starts walking faster and then breaks into a run.”_


26 _Giancarlo Guizzardi et al. / UFO: Unified Foundational Ontology_


In Figure 10, we present an OntoUML model representing this case. In UFO, we follow a classical view
of events in which events are _modally fragile_ entities. So, events cannot bear modal properties, they cannot
genuinely change, and they cannot be different from what they are (Guizzardi et al., 2016). Events are also
polygenic manifestations of (possibly bundles of) dispositions (Guizzardi et al., 2013a). These (bundles
of) dispositions are said to be the focuses of these events, so that events are carved out of _scenes_ by having
those underlying endurants as their focus (Guarino and Guizzardi, 2016). For example, the marriage of
John and Mary as a perdurant is the manifestation of the marriage (as a relator) that binds John and Mary,
i.e., the sum of all manifestations of the moments inhering in John-qua-Husband-of-Mary and Mary-quaWife-of-John (Guizzardi et al., 2016; Guarino and Guizzardi, 2016; Guizzardi, 2006; Guizzardi et al.,
2013b). Following up on this example, there are two kinds of “changes” referring to “John and Mary’s
marriage”: (1) a _change in_ the marriage relator—for example, when we say that the marriage between
John and Mary (as a whole) changed from passionate in situation _s_ 1 to cold and distant in situation _s_ 2,
we are referring to this endurant (a bundle of moments), which can qualitatively change while remaining
numerically the same; (2) a _change of_ (or, more precisely, a variation of) temporal parts of a perdurant
that are qualitatively different. Figure 10 illustrates a case of the latter; Figure 12 illustrates a case of the
former.


Figure 10. The Changing Speed case in OntoUML.


In the sequel, we show a partial formalization of this case.


ObjectKind(Person)


Jogger is a role played by a Person when bearing a Jog mode (an endurant comprising an intention
as well as the capacities of the person as a Jogger).


Role(Jogger)

Jogger _⊑_ Person


_Giancarlo Guizzardi et al. / UFO: Unified Foundational Ontology_ 27


ModeKind(Jog)


characterization(Jogger _,_ Jog)

_∀x._ ( _x_ :: Jog _→∃_ ! _y._ ( _y_ :: JoggingTrack _∧_ externallyDependent( _x, y_ )))


As explained in details by Guizzardi et al. (2016), associated to a Jog (an endurant), we have Jogging
perdurants that are manifestations of that endurant. In particular, we have Jogging Events, which are direct manifestations of the dispositions constituting a Jog, and Jogging Processes, which are constituted
by Jogging Events.


EventType(JoggingProcess)


EventType(JoggingEvent)
_∀x._ ( _x_ :: JoggingEvent _→∃_ ! _y._ ( _y_ :: Jog _∧_ _2_ (ex( _x_ ) _→_ manifestedBy( _y, x_ ))))


At each situation, we have a particular type of maximal Jogging Process (termed the life of a Jog) that
is constituted by (exactly) the sum of Jogging Events that are manifestations of that Jog. Moreover, since
perdurants have all their parts, properties and constituents necessarily, every time a new Jogging Event
takes place, there is a new Jogging Process that arises as a cumulative aggregation of manifestations of
that Jog, i.e., a new life of that Jog.


_∀x._ ( _x_ :: Jog _→∃_ ! _y._ ( _y_ :: JoggingProcess _∧_ lifeOf( _y, x_ ))

_∀x._ ( _x_ :: JoggingProcess _→∃y._ ( _y_ :: JoggingEvent _∧_ constitutedBy( _x, y_ ))

_∀x, y._ ( _x_ :: Jog _∧_ _y_ :: JoggingProcess _∧_ lifeOf( _y, x_ ) _→∀z._ ( _z_ :: JoggingEvent _→_
(constitutedBy( _y, z_ ) _↔_ manifestedBy( _x, z_ ))))


Since perdurants unfold in time accumulating parts, if we have two Jogging Processes that are manifestations of the same Jog and that immediately follow each other, _meeting_ in the Allen sense (Guizzardi
et al., 2013a), then we have that all constituents of the preceding process also constitute the succeeding
process [20] .


_∀x, y, z._ ( _x_ :: Jog _∧_ _y_ :: JoggingProcess _∧_ _z_ :: JoggingProcess _∧_ manifestedBy( _x, y_ ) _∧_
manifestedBy( _x, z_ ) _∧_ meet( _y, z_ ) _→∀w._ ( _w_ :: JoggingEvent _∧_ constitutedBy( _y, w_ ) _→_
constitutedBy( _z, w_ )))


Jogging Events can be stative/homeomerous and some are dynamic/sequences of changes. In the
former’s case, we have Jog State, while in the latter we have Jogging Locomotion. Moreover,
Jogging Locomotions can be such that they have the quality of being a Walk While Jogging event (an
event characterized by a “walking” moving speed), or they can be such that they have the quality of being a Run While Jogging (an event characterized by a “running” moving speed). Since events are immutable, they are characterized by tropes, in the classical sense, not qualities as _variable tropes_ (Guarino
and Guizzardi, 2015, 2016). Unlike qualities, tropes cannot change their values.


EventType(JogState)


EventType(JoggingLocomotion)


EventType(WalkWhileJogging)


EventType(RunWhileJogging)
_∀x._ ( _x_ :: JoggingLocomotion _→∃_ ! _y._ ( _y ∈_ JoggingSpeedValues _∧_ _2_ hasValue( _x, y_ )))


20We use the term _process_ here in this very specific sense to denote the current life of an endurant constituted by all and exactly
the manifestations of (the dispositions inhering in) that endurant (see section 2.13)(Guizzardi et al., 2016). These formulae here
capture the continuous changes _of_ life of an endurant as dispositions continue to manifest. Each current life of an endurant is
monotonically constituted by all constituents of its immediate preceding life.


28 _Giancarlo Guizzardi et al. / UFO: Unified Foundational Ontology_


In the specialization of Jogging Event into Jogging Locomotion and Jog State, and the specialization Jogging Locomotion into Walk While Jogging and Run While Jogging, partition the instances of
the specialized types, which can be represented with support of (a105)–(a107).


**a106** isCompletelyCoveredBy( _t, t_ _[′]_ _, t_ _[′′]_ ) _↔∀x_ ( _x_ :: _t →_ _x_ :: _t_ _[′]_ _∨_ _x_ :: _t_ _[′′]_ )

**a107** isPartitionedInto( _t, t_ _[′]_ _, t_ _[′′]_ ) _↔_ isCompletelyCoveredBy( _t, t_ _[′]_ _, t_ _[′′]_ ) _∧_ isDisjointWith( _t_ _[′]_ _, t_ _[′′]_ )


isPartitionedInto(JoggingEvent _,_ JogState _,_ JoggingLocomotion)


isPartitionedInto(JoggingLocomotion _,_ WalkWhileJogging _,_ RunWhileJogging)


Figure 11 depicts instances automatically generated for the OntoUML diagram of Figure 10.


_3.4. Event change_


_4) “A man is walking to the station, but before he gets there, he turns around and goes home.”_


Figure 11. From world _w_ 1 to _w_ 3, we have a jogger Object2 (Object2 :: Jogger) who is an increasing
speed jog (Property :: Jog, inheresIn(Property, Object2)). In _w_ 1, the jog is manifested by a walking
speed jog Object5 (Object5 :: WalkingWhileJogging), which is then manifested by a fast walking Object4
(Object4 :: WalkingWhileJogging) in _w_ 2, and finally, breaks into a run Object3 (Object3 :: RunningWhileJogging)
in _w_ 3. These events meet as they succeed one another being constituents of the same jogging process Object1
(Object1 :: JoggingProcess, meet(Object5, Object4), meet(Object4, Object3), constitutedBy(Object1, Object5),
constitutedBy(Object1, Object4), constitutedBy(Object1, Object3)).


_Giancarlo Guizzardi et al. / UFO: Unified Foundational Ontology_ 29


As discussed in the previous sections, in UFO, we take the classical approach towards events, thus,
treating them as modally fragile entities. For this reason, events cannot genuinely change, i.e., they cannot
qualitatively change as a whole while maintaining their numerical identity. Alleged events change are
either: (a) event variation — different temporal parts of the event in question have different properties as a
whole. An example of this is exercised in the previous section; (b) the subject of change is the focus of the
event, i.e., the underlying endurant of which the event is a manifestation. The case addressed in this section
is not really a case of the former but one of the latter. To put it baldly, what genuinely changes is this case
is the complex mode (including an intentional component) inhering in the Walker. Due to a change in the
intention of the walker, a different walking perdurant will be manifested. In other words, what genuinely
changes is a property of Walk (the complex mode). These changes make that Walk be manifested as a
(numerically) different walking perdurant. Given that the focus of change here is the endurant, we will
refrain from representing the perdurant part of this example, which would otherwise follow the design
pattern proposed by Guizzardi et al. (2016) and instantiated in the previous section.
In Figure 12, we present an OntoUML model representing this situation. [21] In this model, a Walk is
modeled as an externally dependent mode that inheres in the Walker and that is externally dependent on
Place (that plays the role of an originally intended destination).


Figure 12. The Redirected Walk case in OntoUML.


ObjectKind(Person)


Role(Walker)

Walker _⊑_ Person


ModeKind(Walk)


characterization(Walk _,_ Walker)

_∀x._ ( _x_ :: Walk _→∃_ ! _y._ ( _y_ :: OriginallyIntendedDestination _∧_ externalDependence( _x, y_ )))


21It would, of course, be trivial to model the class Man here as a subkind of Person and as a supertype of Walker. We omit it,
however, for the sake of simplicity and given that it does not have any impact on the focus of the analysis conducted here.


30 _Giancarlo Guizzardi et al. / UFO: Unified Foundational Ontology_


A (originally intended) destination is a role played by a Place when involved in a relationship with a
Walk (i.e., when it is the target of an intention present in a Walk).


ObjectKind(Place)


Role(Destination)


Role(OriginallyIntendedDestination)

Destination _⊑_ Place

OriginallyIntendedDestination _⊑_ Destination

_∀x._ ( _x_ :: OriginallyIntendedDestination _→∃y._ ( _y_ :: Walk _∧_ externalDependence( _y, x_ )))


As previously discussed, a Walk here is an endurant that is the _focus_ of a walking perdurant, in the
technical sense discussed by Guarino and Guizzardi (2016). In this sense, the Walk aggregates both the
intention of the walker and his capabilities qua-walker. As such, i.e., as an endurant, the Walk can change
in time undergoing the phases of Ongoing Walk and Finalized Walk (Guarino and Guizzardi, 2016).


isPartitionedInto(Walk _,_ OngoingWalk _,_ FinalizedWalk)
_∀x._ ( _x_ :: FinalizedWalk _→∃_ ! _y._ ( _y_ :: Destination _∧_ arrivedAt( _x, y_ ) [22] ))


A Finalized Walk is only contingently a Successful Walk (i.e., a walk that arrives at the originally intended destination) as well as it can be contingently (i.e., in a counterfactual situation) a
Redirected Walk.


isPartitionedInto(FinalizedWalk _,_ SucessfulWalk _,_ RedirectedWalk)

_∀x._ ( _x_ :: SuccessfulWalk _↔_ ( _x_ :: FinalizedWalk _∧_
_∀y, z._ (( _y_ :: OriginallyIntendedDestination _∧_ externallyDependent( _x, y_ ) _∧_
_z_ :: Destination _∧_ arrivedAt( _x, z_ )) _→_ ( _y_ = _z_ )))) [23]


In the case of a Redirected Walk, there is a new intention, which is aggregated to the original walk
and which is directed (again, externally dependent on) a new destination. Associated to the Walk (i.e., the
endurant), there are many possible unfoldings (in different histories of the world) representing how the
dispositions aggregated in the walk mode are manifested by different walking perdurants (Guizzardi et al.,
2016).


Role(RedirectedDestination)

RedirectedDestination _⊑_ Destination


ModeKind(RedirectedDestinationIntention)

_∀x._ ( _x_ :: RedirectedDestinationIntention _→∃_ ! _y._ ( _y_ :: RedirectedWalk _∧_ inheresIn( _x, y_ )))

_∀x._ ( _x_ :: RedirectedWalk _→∃_ ! _y._ ( _y_ :: RedirectedDestinationIntention _∧_ inheresIn( _y, x_ )))

_∀x._ ( _x_ :: RedirectedDestinationIntention _→∃_ ! _y._ ( _y_ :: RedirectedDestination _∧_
externallyDependent( _x, y_ )))

_∀x._ ( _x_ :: RedirectedDestination _→∃y._ ( _y_ :: RedirectedDestinationIntention _∧_
externallyDependent( _x, y_ ))

_∀x._ ( _x_ :: RedirectedWalk _→∀y, z._ (( _y_ :: OriginallyIntendedDestination _∧_
externallyDependent( _x, y_ ) _∧z_ :: RedirectedDestination _∧_ arrivedAt( _x, z_ )) _→_ ( _y ̸_ = _z_ ))) [24]


22The relation of “arrived at” is a material relation, which is a derived from the following rule: a walk _x_, qua-endurant, is
related via this relation to a place _y_ iff _y_ is the location of the Walker in the post-situation immediately brought about by the
occurrence of the walking process that is the manifestation of _x_ (Guizzardi et al., 2016).
23A successful walk must “arrive at” a place that is identical to the originally intended destination. This constraint is automatically generated by the OntoUML tool after an automated process of anti-pattern detection and rectification (Sales and Guizzardi,
2015).
24A redirected walk must “arrive at” a place that is different from the originally intended destination. Again, this constraint is
automatically generated by the OntoUML tool after an automated process of anti-pattern detection and rectification.


_Giancarlo Guizzardi et al. / UFO: Unified Foundational Ontology_ 31


_∀x, y, z._ (( _x_ :: RedirectedWalk _∧_ _y_ :: RedirectedDestinationIntention _∧_ inheresIn( _y, x_ ) _∧_
_z_ :: RedirectedDestination _∧_ externallyDependent( _y, z_ )) _→_ arrivedAt( _x, z_ ))


In the sequel, we show an example of visual model (Figure 13) automatically generated for the OntoUML diagram of Figure 12.


Figure 13. In this model, we have a Person Object1 that plays the role of a Walker by being the bearer of three
distinct Walk modes (Object1 :: Person, Object1 :: Walker, Property0 :: Walk, Property1 :: Walk, Property2 :: Walk,
inheresIn(Property0, Object1), inheresIn(Property1, Object1), inheresIn(Property3, Object1)). Property1 is
an ongoing walk that has Object0 as its originally intended destination (Property1 :: OngoingWalk, Object0 :: Place,
Object0 :: Destination, externallyDependent(Property1, Object0), Object0 :: OriginallyIntendedDestination);
Property0 is a finalized walk that also had Object1 as its originally dependent and also final destination
(externallyDependent(Property0, Object0), arrivedAt(Property0, Object0)); finally, Property3 is a finalized
walk that had Object0 as its originally dependent but it was redirected and arrived at a different destination
(externallyDependent(Property3, Object0), arrivedAt(Property3, Object2)).


_3.5. Concept evolution_


_5) “A marriage is a contract that is regulated by civil and social constraints. These constraints can_
_change but the meaning of marriage continues over time.”_


Figure 14. The Concept Evolution case in OntoUML.


In order to address matters of “concept evolution,” it is key to understand what the subject of “evolution”
is, and what aspects of this subject remain stable. According to the “marriage” concept evolution case, “a
marriage is a contract that is regulated by civil and social constraints”, and “these constraints can change


32 _Giancarlo Guizzardi et al. / UFO: Unified Foundational Ontology_


but the meaning of marriage continues over time.” We observe that what remains stable here is a general
kind of relator we call Conjugal Relationship between Spouses. Varying constraints established in
the social process in time lead to specific types of conjugal relationships, e.g., “monogamous marriage,”
“polygamous marriage,” “heterosexual marriage,” and “same-sex marriage.” What is invariant across all
foreseen types of conjugal relationships is that they specialize the more general Conjugal Relationship
relator kind. However, the number and sex of spouses may vary according to the specific type of conjugal
relationship.
UFO captures this scenario by accounting not only for the individuals in the domain of inquiry but
types as well. This leads to higher-order types, i.e., types whose instances are themselves types [25] . The
theory provides a formal characterization of the relations between higher-order types, first-order types,
and individuals, along with a characterization of the so-called powertype pattern in the conceptual modeling literature). In this case, we have that specializations of the more general (and stable) notion of
Conjugal Relationship are instances of a second-order type Conjugal Relationship Type. These
instances establish more specific constraints that are not required in every Conjugal Relationship.
The type Conjugal Relationship serves as the so-called base type in its relation with the higherorder type (Carvalho and Almeida, 2018). Identifying the second-order type allows us to specify invariants that apply to any first-order type instantiating the second-order type: First, all its instances specialize Conjugal Relationship (this is what remains the same or is said to continue over time). Further,
by identifying the second-order type, we can impose conditions on the first-order types that instantiate
it, such as, e.g., that any instance of Conjugal Relationship Type determines one or more specific
Spouse Types. For a Monogamous Heterosexual Marriage, for example, these are Husband and Wife.
The formal relation between these higher-order types and their base types is captured with (a108), as
defined by Carvalho and Almeida (2018) for MLT.


**a108** categorizes( _t_ 1 _, t_ 2) _↔_ Type( _t_ 1) _∧∀t_ 3( _t_ 3 :: _t_ 1 _→_ _t_ 3 _< t_ 2) [26]


In the sequel, we show a partial formalization of this case. We start with the structure that is invariant
with respect to the possible types of conjugal relationships:


categorizes(ConjugalRelationshipType _,_ ConjugalRelationship)


RelatorKind(ConjugalRelationship)


categorizes(SpouseType _,_ Spouse)


ObjectKind(Person)


Role(Spouse)
Spouse _<_ Person

_∀x_ ( _x_ :: Spouse _→∃y_ ( _y_ :: ConjugalRelationship _∧_ mediates( _y, x_ ))

_∀x_ ( _x_ :: ConjugalRelationship _→∃y, z_ ( _y_ :: Spouse _∧_ _z_ :: Spouse _∧_ _y ̸_ = _z ∧_ mediates( _x, y_ ) _∧_
mediates( _x, z_ )))


We also need to ensure that Conjugal Relationships (at the individual level) respect the invariants specified for Conjugal Relationship Types and Spouse Types. Thus, we add a constraint that
all Conjugal Relationships (instances of instances of Conjugal Relationship Type) mediate relata
that instantiate Spouse Type that are compatible with their specific Conjugal Relationship Types: [27]


_∀x, y_ (( _x_ :: _y ∧_ _y_ :: ConjugalRelationshipType) _→∀z_ (mediates( _y, z_ ) _→∃t_ ( _t_ :: SpouseType _∧_
compatibleWith( _t, y_ ) _∧_ _z_ :: _t_ )))


25We refer the reader to Carvalho et al. (2017) which shows the combination of UFO with the Multi-Level Theory (MLT,
Carvalho and Almeida, 2018).
26In OntoUML, the «instantiation» stereotype represents both MLT relations of _categorizes_ and _powertypeOf_, the later being
outside the scope of this example.
27This constraint spans more than two levels of classification and corresponds to what can be obtained with a “regularity
attribute” of types (Carvalho and Almeida, 2018; Guizzardi et al., 2015a).


_Giancarlo Guizzardi et al. / UFO: Unified Foundational Ontology_ 33


And then introduce two types of Conjugal Relationships, in conformance with the formalization so
far. First, we introduce Monogamous Heterosexual Marriage:


MonogamousHeterosexualMarriage :: ConjugalRelationshipType


SubKind(MonogamousHeterosexualMarriage)
MonogamousHeterosexualMarriage _<_ ConjugalRelationship

Husband :: SpouseType


Role(Husband)
Husband _<_ Spouse

_∀x_ ( _x_ :: Husband _→∃_ ! _y_ ( _y_ :: MonogamousHeterosexualMarriage _∧_ mediates( _y, x_ ))

Wife :: SpouseType


Role(Wife)
Wife _<_ Spouse

_∀x_ ( _x_ :: Wife _→∃_ ! _y_ ( _y_ :: MonogamousHeterosexualMarriage _∧_ mediates( _y, x_ ))

_∀x_ ( _x_ :: MonogamousHeterosexualMarriage _→∃_ ! _y,_ ! _z_ ( _y_ :: Husband _∧z_ :: Wife _∧_ mediates( _x, y_ ) _∧_
mediates( _x, z_ )))


And, second, MonogamousSamesexMarriage:


MonogamousSamesexMarriage :: ConjugalRelationshipType


SubKind(MonogamousSamesexMarriage)
MonogamousSamesexMarriage _<_ ConjugalRelationship

Partner :: SpouseType


Role(Partner)
Partner _<_ Spouse

_∀x_ ( _x_ :: Partner _→∃_ ! _y_ ( _y_ :: MonogamousSamesexMarriage _∧_ mediates( _y, x_ ))

_∀x_ ( _x_ :: MonogamousSamesexMarriage _→∃_ ! _y,_ ! _z_ ( _y_ :: Partner _∧_ _z_ :: Partner _∧_ _y ̸_ = _z ∧_
mediates( _x, y_ ) _∧_ mediates( _x, z_ ) _∧_ (( _y_ :: Man _∧_ _z_ :: Man) _∨_ ( _y_ :: Woman _∧_ _z_ :: Woman))))


In the sequence, we present a simulation of such a scenario where in the past world the only instance of Conjugal Relationship Type present is the Monogamic Heterosexual Marriage, which
is also foreseen in the model. In the subsequent world another Conjugal Relationship Type is also
present, one that has only one compatible Spouse Type (which can be interpreted as a sort of Partner
type), and whose instances relate two instances of Spouse of the same sex. This simulation shows that
Monogamic Samesex Marriage is also a possible instance for the model in Figure 15.
We should observe that we are dealing here with a case of _anticipated evolution_ (Bennett and Rajlich,
2000), i.e., when it is possible at specification time to foresee that types are likely to change and hence
introduce invariant structures that can accommodate the envisioned space of change. _Unanticipated evo-_
_lution_ would effectively require changing the model, which could be obtained by application of model
refactoring operations (Sunyé et al., 2001). For example, in the case of the “marriage” scenario, if we had
an initial model consisting of a “marriage” relator between a “man” and a “woman,” we could rename it to
“heterosexual marriage”, add “same-sex marriage” and introduce “conjugal relationship” as a super type
of both of them along with declaring “monogamous heterosexual marriage” and “monogamous same-sex
marriage” as instances of “conjugal relationship type” (to foresee other possible changes).


34 _Giancarlo Guizzardi et al. / UFO: Unified Foundational Ontology_


Figure 15. Simulation of evolving notion of Conjugal Relationship. In _w_ 1, the only Conjugal Relationship Type
present is the one whose instances include Monogamic Heterosexual Marriage, e.g., Property0
(Object5 :: ConjugalRelationshipType, Property0 :: _Monogamic_ HeterosexualMarriage, instantiation(Property0,
Object5). In a subsequent world, it is present a different instance of Conjugal Relationship Type — Object8 —
whose instances include same sex conjugal relationships, such as Property1 (Object8 :: ConjugalRelationshipType,
Property1 :: ConjugalRelationship, instantiation(Property1, Object8). The compatible Spouse Type to Object8

- Object0 — is also different from the ones classifying instances of Husband and xObject0 — Object2 and Object1
—, what shows that the model also accommodates types such as Partner as instances (Object0 :: SpouseType,
Object1 :: SpouseType, Object2 :: SpouseType, Object7 :: Spouse, Object3 :: Spouse, Object4 :: Husband,
Object6 :: Wife, instantiation(Object7, Object0), instantiation(Object3, Object0), instantiation(Object4, Object2),
instantiation(Object6, Object1).


**4. Ontology usage and community impact**


Over the years, UFO has been used for the development of core and domain ontologies on a wide range
of domains, both in academic and industrial contexts. For instance, it has been used to provide conceptual
clarification in domains such as:


**–** agriculture (Neves and Cruvinel, 2021; Niederkofler et al., 2019)

**–** accounting (Blums and Weigand, 2021; Fischer-Pauzenberger and Schwaiger, 2017; Fraller, 2019;
Laurier et al., 2018)

**–** business processes (Guizzardi and Wagner, 2011a; Guizzardi et al., 2016; Santos Júnior et al., 2010;
van Wingerde and Weigand, 2020)

**–** biodiversity (Albuquerque et al., 2015)

**–** bioinformatics (Gonçalves et al., 2011; Rodrigues et al., 2017)

**–** branding (Elikan, 2019)

**–** communities (Almeida and Guizzardi, 2013)

**–** capabilities (Azevedo et al., 2015)

**–** competition (Sales et al., 2018c)

**–** data processing (Moura et al., 2021)

**–** decision making (Guizzardi et al., 2020; Richetti et al., 2019)

**–** design science research (Weigand et al., 2021)

**–** digital platforms (Derave et al., 2021)

**–** discrete event simulation (Guizzardi and Wagner, 2010, 2011b, 2012, 2013)

**–** economic exchanges (Porello et al., 2020)

**–** emergency and disaster management (Ferreira et al., 2015; Khantong and Ahmad, 2019; Moreira
et al., 2015)

**–** engineering (Pereira et al., 2019)

**–** e-government (Barcelos et al., 2013; Detoni et al., 2018; Kˇremen and Neˇcaský, 2019; Pereira et al.,
2020)

**–** game theory (Amaral et al., 2020c)

**–** game design (Franco et al., 2018; Kritz, 2020)

**–** goals and motivation (Azevedo et al., 2011; Guizzardi et al., 2012, 2013b)

**–** geology (Abel et al., 2015; Rodrigues et al., 2019; Vieira et al., 2020)


_Giancarlo Guizzardi et al. / UFO: Unified Foundational Ontology_ 35


**–** legal issues (El Ghosh and Abdulrab, 2020, 2021; Griffo et al., 2015; Mário de Oliveira Rodrigues
et al., 2020; Santos et al., 2018)

**–** money (Amaral et al., 2020b)

**–** mulsemedia (Saleme et al., 2019)

**–** organizational structures (Santos Júnior et al., 2013)

**–** programming languages (Aguiar et al., 2019)

**–** security and safety (Debbech et al., 2020; Faria et al., 2019; Kostov et al., 2017; Sales et al., 2018b;
Zhou et al., 2017)

**–** services (Nardi et al., 2015)

**–** simulation for land covering and use (Grueau, 2013)

**–** smart contracts (Sharifi et al., 2020)

**–** software engineering (Duarte et al., 2018; Henderson-Sellers, 2012; Henderson-Sellers et al., 2014;
Kirk and MacDonell, 2016; Maretto and Barcellos, 2014; Morales-Ramirez et al., 2015; Ruy et al.,
2016; Shekhovtsov and Mayr, 2014; Sydorov et al., 2019; Wang et al., 2014b)

**–** software requirements (Bernabé et al., 2019; Duarte et al., 2018, 2021; Guizzardi et al., 2014; Li
et al., 2015; Negri et al., 2017)

**–** telecommunication networks (Barcelos et al., 2009; Rita de Cássia et al., 2012)

**–** treatment (Johannesson and Perjons, 2020)

**–** tourism (AlpineBits Alliance, 2021)

**–** trust (Amaral et al., 2019)

**–** value (Gailly et al., 2016; Guarino et al., 2016; Sales et al., 2017)

**–** waste management (Ahmad et al., 2018)


Moreover, UFO and ontologies built with it have been used to analyze, reengineer, or integrate many
modeling languages and standards in different domains:


**–** ArchiMate (Almeida et al., 2009; Amaral et al., 2020a; Azevedo et al., 2011, 2015; Griffo et al.,
2017; Sales et al., 2018a, 2019)

**–** ARIS (Santos Júnior et al., 2010, 2013)

**–** DEMO (Poletaeva et al., 2017)

**–** ISO/IEC 24744 (Ruy et al., 2014)

**–** ITU-T G.805 (Barcelos et al., 2011)

**–** BPMN (Guizzardi and Wagner, 2011a)

**–** RM-ODP (Almeida and Guizzardi, 2013)

**–** TOGAF (Almeida et al., 2009)

**–** Tropos and i [*] (Guizzardi et al., 2013b,c; Franch et al., 2011)

**–** UML (Costal et al., 2011; Guizzardi, 2005)


A recent study shows that UFO is the second-most used foundational ontology in conceptual modeling
and the one with the fastest adoption rate (Verdonck and Gailly, 2016). That study also shows that OntoUML is among the most used languages in ontology-driven conceptual modeling (together with UML,
(E)ER, OWL, and BPMN). Moreover, empirical evidence shows that OntoUML significantly contributes
to improving the quality of conceptual models without requiring an additional effort to producing them.
For instance, Verdonck et al. (2019) report on a modeling experiment conducted with 100 participants
in two countries showing the advantages (in these respects) of OntoUML when compared to a classical
conceptual modeling language (EER – Extended ER).
Currently, the development of UFO-based models through OntoUML is supported by a microservicebased infrastructure. The _OntoUML as a Service_ infrastructure (Fonseca et al., 2021b), or OaaS, is designed to decouple model services developed by OntoUML researchers (e.g., transformations, verifications, simulations, verbalizations) and the modeling tools they support. As a result, these _model intelli-_
_gence services_ can be developed independently, making use of programming languages and libraries that
best fit the researcher’s needs and preferences, and later integrated into modeling tools, such as UML


36 _Giancarlo Guizzardi et al. / UFO: Unified Foundational Ontology_


CASE tools. This is enabled by OaaS’s low requirements on services and tool developers that consists
of support to HTTP and JSON used for service request and model serialization respectively. The current implementation of OaaS consists of a JSON Schema specification to govern the JSON serialization
of OntoUML models [28], a TypeScript library to support the manipulation and serialization of OntoUML
models [29], an HTTP server that provides multiple model intelligence services [30], and a plugin for the UML
CASE Visual Paradigm [31] that extends it with OntoUML modeling capabilities [32] .


**Acknowledgments**


We are grateful to Gerd Wagner, Nicola Guarino, and the members of the Ontology & Conceptual
Modeling Research Group (NEMO)—especially, Renata Guizzardi and Ricardo Falbo ( _in memoriam_ )—
for all the years of collaboration in the scope of UFO.
Claudenir M. Fonseca and Giancarlo Guizzardi are supported by the NeXON Project (Free University
of Bozen-Bolzano). João Paulo A. Almeida is funded by the Brazilian Research Funding Agencies CNPq
(grants number 313687/2020-0 and 407235/2017-5), CAPES (23038.028816/2016-41) Finance Code 001
and FAPES (281/2021).


**References**


Abel, M., Perrin, M., and Carbonera, J. L. (2015). Ontological analysis for information integration in geomodeling. _Earth_
_Science Informatics_, 8(1):21–36.
Aguiar, C. Z., Almeida Falbo, R., and Souza, V. E. S. (2019). OOC-O: A reference ontology on object-oriented code. In Laender,
A. H. F., Pernici, B., Lim, E.-P., and de Oliveira, J. P. M., editors, _Conceptual Modeling_, pages 13–27, Cham. Springer.
Ahmad, M. N., Badr, K. B. A., Salwana, E., Zakaria, N. H., Tahar, Z., and Sattar, A. (2018). An ontology for the waste management domain. In _Pacific Asia Conference on Information Systems (PACIS)_, page 12.
Albuquerque, A. and Guizzardi, G. (2013). An ontological foundation for conceptual modeling datatypes based on semantic
reference spaces. In _IEEE 7th International Conference on Research Challenges in Information Science (RCIS)_, pages 1–12.
Albuquerque, A. C., dos Santos, J. L. C., and de Castro, A. N. (2015). OntoBio: A biodiversity domain ontology for Amazonian
biological collected objects. In _2015 48th Hawaii International Conference on System Sciences_, pages 3770–3779. IEEE.
Almeida, J. P. A., Falbo, R. A., and Guizzardi, G. (2019). Events as entities in ontology-driven conceptual modeling. In
_International Conference on Conceptual Modeling_, pages 469–483. Springer.
Almeida, J. P. A. and Guizzardi, G. (2013). An ontological analysis of the notion of community in the RM-ODP enterprise
language. _Computer Standards & Interfaces_, 35(3):257–268.
Almeida, J. P. A., Guizzardi, G., and Santos Júnior, P. S. (2009). Applying and extending a semantic foundation for role-related
concepts in enterprise modelling. _Enterprise Information Systems_, 3(3):253–277.
AlpineBits Alliance (2021). AlpineBits DestinationData 2021-04.
Amaral, G., Sales, T. P., Guizzardi, G., Almeida, J. P. A., and Porello, D. (2020a). Modeling trust in enterprise architecture:
A pattern language for ArchiMate. In Grabis, J. and Bork, D., editors, _The Practice of Enterprise Modeling. PoEM 2020_,
volume 400 of _Lecture Notes in Business Information Processing_, pages 73–89, Cham. Springer International Publishing.
Amaral, G., Sales, T. P., Guizzardi, G., and Porello, D. (2019). Towards a reference ontology of trust. In Panetto, H. et al., editors,
_27th International Conference on Cooperative Information Systems (CoopIS)_, volume 11877 of _Lecture Notes in Computer_
_Science_, pages 3–21, Cham. Springer.
Amaral, G., Sales, T. P., Guizzardi, G., and Porello, D. (2020b). A reference ontology of money and virtual currencies. In _IFIP_
_Working Conference on The Practice of Enterprise Modeling_, pages 228–243. Springer.
Amaral, G. C., Porello, D., Sales, T. P., and Guizzardi, G. (2020c). Modeling the emergence of value and risk in game theoretical
approaches. In _EEWC_, pages 70–91.
Azevedo, C. L. B., Almeida, J. P. A., van Sinderen, M., Quartel, D. A. C., and Guizzardi, G. (2011). An ontology-based semantics
for the motivation extension to ArchiMate. In _IEEE 15th International Enterprise Distributed Object Computing Conference_
_(EDOC)_, pages 25–34. IEEE.
Azevedo, C. L. B., Iacob, M., Almeida, J. P. A., van Sinderen, M., Pires, L. F., and Guizzardi, G. (2015). Modeling resources
and capabilities in enterprise architecture: A well-founded ontology-based proposal for ArchiMate. _Information Systems_,
54:235–262.


[28The ontouml-schema project is available at https://purl.org/krdb-core/ontouml-schema.](https://purl.org/krdb-core/ontouml-schema)
[29The ontouml-js project is available at https://purl.org/krdb-core/ontouml-js.](https://purl.org/krdb-core/ontouml-js)
[30The ontouml-server is available at https://purl.org/krdb-core/ontouml-server.](https://purl.org/krdb-core/ontouml-server)
[31https://www.visual-paradigm.com/](https://www.visual-paradigm.com/)
[32The ontouml-vp-plugin is available at https://purl.org/krdb-core/ontouml-plugin.](https://purl.org/krdb-core/ontouml-plugin)


_Giancarlo Guizzardi et al. / UFO: Unified Foundational Ontology_ 37


Baker, L. R. (2007). _The metaphysics of everyday life_ . Cambridge: Cambridge University Press.
Barcelos, P. P., Monteiro, M. E., Simões, R. d. M., Garcia, A. S., and Segatto, M. E. (2009). OOTN – an ontology proposal for
optical transport networks. In _2009 International Conference on Ultra Modern Telecommunications & Workshops_, pages
1–7. IEEE.
Barcelos, P. P. F., Guizzardi, G., Garcia, A. S., and Monteiro, M. E. (2011). Ontological evaluation of the ITU-T recommendation
G. 805. In _2011 18th International Conference on Telecommunications_, pages 232–237. IEEE.
Barcelos, P. P. F., Guizzardi, R. S., and Garcia, A. S. (2013). An ontology reference model for normative acts. In Bax, M. P.,
Almeida, M. B., and Wassermann, R., editors, _13th Seminar on Ontology Research in Brazil (ONTOBRAS)_, volume 1041.
Benevides, A. B., Almeida, J. P. A., and Guizzardi, G. (2019a). Towards a unified theory of endurants and perdurants: UFO-AB.
In _JOWO_ .
Benevides, A. B., Bourguet, J.-R., Guizzardi, G., Penaloza, R., and Almeida, J. P. A. (2019b). Representing a reference foundational ontology of events in SROIQ. _Applied Ontology_, 14(3):293–334.
Benevides, A. B., Guizzardi, G., Braga, B. F. B., and Almeida, J. P. A. (2010). Validating modal aspects of OntoUML conceptual
models using automatically generated visual world structures. _Journal of Universal Computer Science_, 16(20):2904–2933.
Bennett, K. H. and Rajlich, V. T. (2000). Software maintenance and evolution: A roadmap. In _Proceedings of the Conference on_
_The Future of Software Engineering_, ICSE ’00, pages 73–87. ACM.
Bera, P. and Wand, Y. (2004). Analyzing OWL using a philosophy-based ontology. In Varzi, A. and Vieu, L., editors, _3rd_
_International Conference on Formal Ontology in Information Systems (FOIS)_, pages 353–62. IOS Press.
Bernabé, C. H., Silva Souza, V. E., Almeida Falbo, R. d., Guizzardi, R. S. S., and Silva, C. (2019). GORO 2.0: Evolving an
ontology for goal-oriented requirements engineering. In Guizzardi, G., Gailly, F., and Suzana Pitangueira Maciel, R., editors,
_Advances in Conceptual Modeling. ER 2019_, volume 11787 of _Lecture Notes in Computer Science_, pages 169–179. Springer.
Blums, I. and Weigand, H. (2017). Financial reporting by a shared ledger. In _8th International Workshop on Formal Ontologies_
_Meet Industry (FOMI)_ .
Blums, I. and Weigand, H. (2021). Conceptualizing social relators and economic exchange contracts for reporting purposes. In
_International Workshop on Value Modelling and Business Ontologies (VMBO_, volume 2835.
Bradley, F. (1893). _Appearance and reality: a metaphysical essay._ Swan Sonnenschein & Co.
Bunge, M. (1977). _Treatise on Basic Philosophy. Ontology I: The Furniture of the World._, volume 3. Reidel Publishing Company.
Carmo, A. P., Zamperini, T., Mello, M. R. S., Leal, A. L. C., and Garcia, A. S. (2017). Ontologia das coisas para espaços
inteligentes baseados em visão computacional. In _9th Seminar of Ontology Research in Brazil (ONTOBRAS)_ .
Carvalho, V. A. and Almeida, J. P. A. (2018). Toward a well-founded theory for multi-level conceptual modeling. _Software &_
_Systems Modeling_, 17(1):205–231.
Carvalho, V. A., Almeida, J. P. A., Fonseca, C. M., and Guizzardi, G. (2017). Multi-level ontology-based conceptual modeling.
_Data & Knowledge Engineering_, 109:3–24.
Carvalho, V. A., Almeida, J. P. A., and Guizzardi, G. (2016). Using a well-founded multi-level theory to support the analysis
and representation of the powertype pattern in conceptual modeling. In _Advanced Information Systems Engineering. CAiSE_
_2016_, pages 309–324. Springer.
Costal, D., Gómez, C., and Guizzardi, G. (2011). Formal semantics and ontological analysis for understanding subsetting,
specialization and redefinition of associations in UML. In _Conceptual Modeling. ER 2011_, pages 189–203.
Davidson, D. (2001). _Essays on actions and events: Philosophical essays_, volume 1. Oxford University Press on Demand.
de Oliveira Bringuente, A. C., de Almeida Falbo, R., and Guizzardi, G. (2011). Using a foundational ontology for reengineering
a software process ontology. _Journal of Information and Data Management_, 2(3):511–511.
Debbech, S., Dutilleul, S. C., and Bon, P. (2020). An ontological approach to support dysfunctional analysis for railway systems
design. _Journal of Universal Computer Science_, 26(5):549–582.
Derave, T., Sales, T. P., Gailly, F., and Poels, G. (2021). Comparing digital platform types in the platform economy. In La Rosa,
M., Sadiq, S., and Teniente, E., editors, _Advanced Information Systems Engineering. CAiSE 2021_, volume 12751 of _Lecture_
_Notes in Computer Science_, pages 417–431, Cham. Springer.
Detoni, A. A., Fonseca, L. B. R., Almeida, J. P. A., and Falbo, R. A. (2018). A reference ontology for budgetary authorization and
execution of public expenditure (uma ontologia de referência para autorização orçamentária e execução da despesa pública).
_iSys: Brazilian Journal of Information Systems_, 11(3):4–53.
Duarte, B. B., de Almeida Falbo, R., Guizzardi, G., Guizzardi, R., and Souza, V. E. S. (2021). An ontological analysis of software
system anomalies and their associated risks. _Data & Knowledge Engineering_, 134:101892.
Duarte, B. B., Leal, A. L. C., Falbo, R. A., Guizzardi, G., Guizzardi, R. S. S., and Souza, V. E. S. (2018). Ontological foundations
for software requirements with a focus on requirements at runtime. _Applied Ontology_, 13(2):73–105.
El Ghosh, M. and Abdulrab, H. (2020). Ontology-based liability decision support in the international maritime law. In _Legal_
_Knowledge and Information Systems_, pages 273–276. IOS Press.
El Ghosh, M. and Abdulrab, H. (2021). Cargo-s: A pattern-based well-founded legal domain ontology for the traceability of
goods in logistic sea corridors. _Applied Ontology_, pages 1–40.
Elikan, D. (2019). _Designing a Visual Inquiry Tool for Identity Communication_ . PhD thesis, Université de Lausanne, Faculté des
hautes études commerciales.
Evermann, J. and Wand, Y. (2001). Towards ontologically based semantics for UML constructs. In Kunii, H. S., Jajodia, S., and
Sølvberg, A., editors, _Conceptual Modeling. ER 2001_, volume 2224 of _Lecture Notes in Computer Science_, pages 354–367.
Springer.
Falbo, R. A., Quirino, G. K., Nardi, J. C., Barcellos, M. P., Guizzardi, G., Guarino, N., Longo, A., and Livieri, B. (2016). An
ontology pattern language for service modeling. In _31st Annual ACM Symposium on Applied Computing (SAC)_, pages
321–326. ACM.
Faria, M. R., de Figueiredo, G. B., de Faria Cordeiro, K., Cavalcanti, M. C., and Campos, M. L. M. (2019). Applying multi-level
theory to an information security incident domain ontology. In Almeida, J. P. A. et al., editors, _12th Seminar on Ontology_
_Research in Brazil (ONTOBRAS)_ .


38 _Giancarlo Guizzardi et al. / UFO: Unified Foundational Ontology_


Ferreira, M. I., Moreira, J. L. R., Campos, M. L. M., Braga, B., Sales, T. P., de Faria Cordeiro, K., and Borges, M. (2015).
OntoEmergePlan: Variability of emergency plans supported by a domain ontology. In _12th International Conference on_
_Information Systems for Crisis Response & Management (ISCRAM)_ .
Fischer-Pauzenberger, C. and Schwaiger, W. S. (2017). The ontorea accounting model: Ontology-based modeling of the accounting domain. _Complex Systems Informatics and Modeling Quarterly_, 11:20–37.
Fitting, M. and Mendelsohn, R. L. (2012). _First-order modal logic_, volume 277. Springer Science & Business Media.
Fonseca, C. M., Almeida, J. P. A., Guizzardi, G., and Carvalho, V. A. (2021a). Multi-level conceptual modeling: Theory, language
and application. _Data & Knowledge Engineering_, 134:101894.
Fonseca, C. M., Porello, D., Guizzardi, G., Almeida, J. P. A., and Guarino, N. (2019). Relations in ontology-driven conceptual
modeling. In _International Conference on Conceptual Modeling_, pages 28–42. Springer.
Fonseca, C. M., Sales, T. P., Viola, V., Fonseca, L. B. R., Guizzardi, G., and Almeida, J. P. A. (2021b). Ontology-driven conceptual
modeling as a service. In _11_ _[th]_ _International Workshop on Formal Ontologies meet Industry (FOMI 2021)_ .
Fraller, C. (2019). _Flexible budgeting in an activity-based costing framework: from conceptual modeling to prototypical imple-_
_mentation_ . PhD thesis, Wien.
Franch, X., Guizzardi, R. S. S., Guizzardi, G., and López, L. (2011). Ontological analysis of means-end links. In _5th International_
i _* Workshop_, pages 37–42.
Franco, A. O., Rolim, T. V., Santos, A. M., Silva, J. W., Vidal, V. M., Gomes, F. A., Castro, M. F., and Maia, J. G. (2018). An
ontology for role playing games. _Proceedings of SBGames_, pages 615–618.
Gailly, F., Roelens, B., and Guizzardi, G. (2016). The design of a core value ontology using ontology patterns. In _Advances in_
_Conceptual Modeling. ER 2016_, volume 9975 of _Lecture Notes in Computer Science_, pages 183–193. Springer.
Gärdenfors, P. (2004). _Conceptual spaces: The geometry of thought_ . MIT press.
Gonçalves, B., Guizzardi, G., and Filho, J. G. P. (2011). Using an ECG reference ontology for semantic interoperability of ECG
data. _Journal of Biomedical Informatics_, 44(1):126–136.
Griffo, C., Almeida, J. P. A., and Guizzardi, G. (2015). Towards a legal core ontology based on Alexy’s theory of fundamental
rights. In _Multilingual Workshop on Artificial Intelligence and Law_ .
Griffo, C., Almeida, J. P. A., Guizzardi, G., and Nardi, J. C. (2017). From an ontology of service contracts to contract modeling
in enterprise architecture. In _IEEE 21st International Enterprise Distributed Object Computing Conference (EDOC)_, pages
40–49. IEEE.
Grueau, C. (2013). Towards a domain specific modeling language for agent-based modeling of land use/cover change. In
_Advances in Conceptual Modeling. ER 2013_, volume 8697 of _Lecture Notes in Computer Science_, pages 267–276. Springer.
Guarino, N., Andersson, B., Johannesson, P., and Livieri, B. (2016). Towards an ontology of value ascription. In _9th International_
_Conference on Formal Ontology in Information Systems (FOIS)_, volume 283, page 331. IOS Press.
Guarino, N. and Guizzardi, G. (2015). "We need to discuss the relationship": Revisiting relationships as modeling constructs.
In _Advanced Information Systems Engineering. CAiSE 2015_, volume 9097 of _Lecture Notes in Computer Science_, pages
279–294.
Guarino, N. and Guizzardi, G. (2016). Relationships and events: Towards a general theory of reification and truthmaking. In
Adorni, G., Cagnoni, S., Gori, M., and Maratea, M., editors, _Advances in Artificial Intelligence. AI*IA 2016_, volume 10037
of _Lecture Notes in Computer Science_, pages 237–249.
Guarino, N., Guizzardi, G., and Mylopoulos, J. (2020). On the philosophical foundations of conceptual models. _Information_
_Modelling and Knowledge Bases_, 31(321):1.
Guarino, N., Porello, D., and Guizzardi, G. (2019). On weak truthmaking. In Barton, A., Seppälä, S., and Porello, D., editors,
_Proceedings of the Joint Ontology Workshops 2019 Episode V: The Styrian Autumn of Ontology, Graz, Austria, September_
_23-25, 2019_, volume 2518 of _CEUR Workshop Proceedings_ . CEUR-WS.org.
Guarino, N. and Welty, C. A. (2009). An overview of OntoClean. In _Handbook on Ontologies_, International Handbooks on
Information Systems, pages 201–220. Springer.
Guerson, J., Sales, T. P., Guizzardi, G., and Almeida, J. P. A. (2015). OntoUML Lightweight Editor: a model-based environment
to build, evaluate and implement reference ontologies. In _19th IEEE International Enterprise Distributed Object Computing_
_Workshops_, pages 144–147. IEEE.
Guizzardi, G. (2005). _Ontological foundations for structural conceptual models_ . CTIT, Centre for Telematics and Information
Technology, Enschede.
Guizzardi, G. (2006). Agent roles, qua individuals and _the Counting Problem_ . In Garcia, A., Choren, R., Lucena, C., Giorgini,
P., Holvoet, T., and Romanovsky, A., editors, _Software Engineering for Multi-Agent Systems IV_, pages 143–160, Berlin,
Heidelberg. Springer Berlin Heidelberg.
Guizzardi, G. (2007). Modal aspects of object types and part-whole relations and the _de re/de dicto_ distinction. In _dvanced_
_Information Systems Engineering. CAiSE 2007_, volume 4495, pages 5–20.
Guizzardi, G. (2009). The problem of transitivity of part-whole relations in conceptual modeling revisited. In van Eck, P.,
Gordijn, J., and Wieringa, R., editors, _Advanced Information Systems Engineering. CAiSE 2009_, volume 5565 of _Lecture_
_Notes in Computer Science_, pages 94–109.
Guizzardi, G. (2010). On the representation of quantities and their parts in conceptual modeling. In _6th International Conference_
_on Formal Ontology in Information Systems (FOIS)_, pages 103–116.
Guizzardi, G. (2011). Ontological foundations for conceptual part-whole relations: The case of collectives and their parts. In
_Advanced Information Systems Engineering. CAiSE 2011_, volume 6741 of _Lecture Notes in Computer Science_, pages 138–
153. Springer.
Guizzardi, G. (2014). Ontological patterns, anti-patterns and pattern languages for next-generation conceptual modeling. In
_International Conference on Conceptual Modeling_, pages 13–27. Springer.
Guizzardi, G. (2015). Logical, ontological and cognitive aspects of object types and cross-world identity with applications to the
theory of conceptual spaces. In _Applications of Conceptual Spaces_, pages 165–186. Springer.


_Giancarlo Guizzardi et al. / UFO: Unified Foundational Ontology_ 39


Guizzardi, G. (2020). Ontology, ontologies and the “I” of FAIR. _Data Intelligence_, 2(1-2):181–191.
Guizzardi, G., Almeida, J. P. A., Guarino, N., and Carvalho, V. A. (2015a). Towards an ontological analysis of powertypes. In
Papini, O. et al., editors, _Joint Ontology Workshops (JOWO)_, volume 1517. CEUR-WS.org.
Guizzardi, G., de Almeida Falbo, R., and Guizzardi, R. S. (2008). Grounding software domain ontologies in the Unified Foundational Ontology (UFO): The case of the ODE Software Process Ontology. In _CIbSE_, pages 127–140. Citeseer.
Guizzardi, G. et al. (2007). On ontology, ontologies, conceptualizations, modeling languages, and (meta) models. _Frontiers in_
_artificial intelligence and applications_, 155:18.
Guizzardi, G., Fonseca, C. M., Almeida, J. P. A., Sales, T. P., Benevides, A. B., and Porello, D. (2021). Types and taxonomic
structures in conceptual modeling: A novel ontological theory and engineering support. _Data & Knowledge Engineering_,
134.
Guizzardi, G., Guarino, N., and Almeida, J. P. A. (2016). Ontological considerations about the representation of events and
endurants in business models. In Rosa, M. L., Loos, P., and Pastor, O., editors, _Business Process Management. BPM 2016_,
volume 9850 of _Lecture Notes in Computer Science_, pages 20–36. Springer.
Guizzardi, G., Masolo, C., and Borgo, S. (2006). In defense of a trope-based ontology for conceptual modeling: An example
with the foundations of attributes, weak entities and datatypes. In Persson, A. and Stirna, J., editors, _Conceptual Modeling._
_ER 2006_, volume 3084 of _Lecture Notes in Computer Science_, pages 112–125. Springer.
Guizzardi, G. and Wagner, G. (2004a). On the ontological foundations of agent concepts. In _Agent-Oriented Information Systems_
_II. AOIS 2004_, volume 3508 of _Lecture Notes in Computer Science_, pages 265–279.
Guizzardi, G. and Wagner, G. (2004b). A Unified Foundational Ontology and some applications of it in business modeling.
In Missikoff, M., editor, _Enterprise Modelling and Ontologies for Interoperability. EMOI - INTEROP 2004_, volume 125.
CEUR-WS.org.
Guizzardi, G. and Wagner, G. (2008). What’s in a relationship: An ontological analysis. In Li, Q. et al., editors, _Conceptual_
_Modeling. ER 2008_, volume 5231 of _Lecture Notes in Computer Science_, pages 83–97. Springer.
Guizzardi, G. and Wagner, G. (2010). Towards an ontological foundation of discrete event simulation. In _Winter Simulation_
_Conference (WSC)_, pages 652–664.
Guizzardi, G. and Wagner, G. (2011a). Can BPMN be used for making simulation models? In Barjis, J., Eldabi, T., and Gupta,
A., editors, _Enterprise and Organizational Modeling and Simulation. EOMAS 2011_, volume 88, pages 100–115. Springer.
Guizzardi, G. and Wagner, G. (2011b). Towards an ontological foundation of agent-based simulation. In _Winter Simulation_
_Conference (WSC)_, pages 284–295.
Guizzardi, G. and Wagner, G. (2012). Conceptual simulation modeling with OntoUML. In _Winter Simulation Conference (WSC)_,
pages 1–15.
Guizzardi, G. and Wagner, G. (2013). Dispositions and causal laws as the ontological foundation of transition rules in simulation
models. In _Winter Simulations Conference (WSC)_, pages 1335–1346.
Guizzardi, G., Wagner, G., Almeida, J. P. A., and Guizzardi, R. S. S. (2015b). Towards ontological foundations for conceptual
modeling: The Unified Foundational Ontology (UFO) story. _Applied Ontology_, 10(3-4):259–271.
Guizzardi, G., Wagner, G., Falbo, R. A., Guizzardi, R. S. S., and Almeida, J. P. A. (2013a). Towards ontological foundations
for the conceptual modeling of events. In Ng, W., Storey, V. C., and Trujillo, J. C., editors, _Conceptual Modeling. ER 2013_,
volume 8217 of _Lecture Notes in Computer Science_, pages 327–341. Springer.
Guizzardi, G., Wagner, G., Guarino, N., and van Sinderen, M. (2004). An ontologically well-founded profile for UML conceptual
models. In _Advanced Information Systems Engineering. CAiSE 2004_, volume 3084 of _Lecture Notes in Computer Science_,
pages 112–126.
Guizzardi, G. and Zamborlini, V. (2014). Using a trope-based foundational ontology for bridging different areas of concern in
ontology-driven conceptual modeling. _Science of Computer Programming_, 96:417–443.
Guizzardi, R. S., Carneiro, B. G., Porello, D., and Guizzardi, G. (2020). A core ontology on decision making. In Lemos, D. L.
d. S. et al., editors, _13th Seminar on Ontology Research in Brazil (ONTOBRAS)_, volume 2728, pages 9–21.
Guizzardi, R. S. and Guizzardi, G. (2011). Ontology-based transformation framework from Tropos to AORML. In Yu, E.,
Giorgini, P., Maiden, N., Mylopoulos, J., and Fickas, S., editors, _Social Modeling for Requirements Engineering_, pages
547–570. MIT Press.
Guizzardi, R. S. S., Franch, X., and Guizzardi, G. (2012). Applying a foundational ontology to analyze means-end links in the
i _[∗]_ framework. In Rolland, C., Castro, J., and Pastor, O., editors, _6th International Conference on Research Challenges in_
_Information Science (RCIS)_, pages 1–11.
Guizzardi, R. S. S., Franch, X., Guizzardi, G., and Wieringa, R. (2013b). Ontological distinctions between means-end and
contribution links in the i _[∗]_ framework. In Ng, W., Storey, V. C., and Trujillo, J. C., editors, _Conceptual Modeling. ER 2013_,
volume 8217 of _Lecture Notes in Computer Science_, pages 463–470. Springer.
Guizzardi, R. S. S., Franch, X., Guizzardi, G., and Wieringa, R. (2013c). Using a foundational ontology to investigate the
semantics behind the concepts of the i* language. In _6th International_ i* _Workshop_, pages 13–18.
Guizzardi, R. S. S., Li, F., Borgida, A., Guizzardi, G., Horkoff, J., and Mylopoulos, J. (2014). An ontological interpretation of
non-functional requirements. In _8th International Conference on Formal Ontology in Information Systems (FOIS)_, pages
344–357.
Heller, B. and Herre, H. (2004). Ontological categories in gol. _Axiomathes_, 14(1):57–76.
Henderson-Sellers, B. (2012). _On the Mathematics of Modelling, Metamodelling, Ontologies and Modelling Languages_ . Springer
Briefs in Computer Science. Springer.
Henderson-Sellers, B., Gonzalez-Perez, C., McBride, T., and Low, G. (2014). An ontology for ISO software engineering standards: 1) creating the infrastructure. _Computer Standards & Interfaces_, 36(3):563–576.
Herre, H., Heller, B., Burek, P., Loebe, F., and Michalek, H. (2004). General ontological language: A formal framework for
building and representing ontologies (version 1.0). Onto-Med Report 7, Reseach Group Ontologies in Medicine, University
of Leipzig.


40 _Giancarlo Guizzardi et al. / UFO: Unified Foundational Ontology_

