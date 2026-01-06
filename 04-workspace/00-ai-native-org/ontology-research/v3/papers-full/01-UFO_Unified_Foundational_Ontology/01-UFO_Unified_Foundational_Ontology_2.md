<!-- Source: 01-UFO_Unified_Foundational_Ontology.pdf | Chunk 2/4 -->

follows.


**a54** ifd( _x, x_ _[′]_ _, y, y_ _[′]_ ) _↔_ gfd( _x_ _[′]_ _, y_ _[′]_ ) _∧_ _x_ :: _x_ _[′]_ _∧_ _y_ :: _y_ _[′]_ _∧_ (F( _x, x_ _[′]_ ) _→_ F( _y, y_ _[′]_ ))


We can now introduce the notion of _component of_ that we are going to use in the subsequent example.


**a55** componentOf( _x, x_ _[′]_ _, y, y_ _[′]_ ) _↔_ _x_ PP _y ∧_ ifd( _x, x_ _[′]_ _, y, y_ _[′]_ ))


_2.7. Constitution_


We adopt here a very simple and preliminary view of constitution. First, it is a relation that holds
between things of the same ontological category (a56).


**a56** constitutedBy( _x, y_ ) _→_ ((Endurant( _x_ ) _↔_ Endurant( _y_ )) _∧_ (Perdurant( _x_ ) _↔_ Perdurant( _y_ )))


However, following Baker (2007), we have that constitution holds between things of different Kinds
(a57). From this, we have the non-reflexivity of constitution as a theorem (t27). Notice that by instantiating
different kinds, constituent and constituted obey different principles of identity, and have different modal
properties (including different essential parts). [7]


**a57** constitutedBy( _x, y_ ) _∧_ ( _x_ :: _x_ _[′]_ ) _∧_ ( _y_ :: _y_ _[′]_ ) _∧_ Kind( _x_ _[′]_ ) _∧_ Kind( _y_ _[′]_ ) _→_ _x_ _[′]_ _̸_ = _y_ _[′]_


**t27** _¬_ constitutedBy( _x, x_ )


7Thomson (1998) requires the following condition to hold in constitution: _“there must be at least one essential part of the_
_constituent, and no part of the constituent is essential to the constituted”_ .


12 _Giancarlo Guizzardi et al. / UFO: Unified Foundational Ontology_


Any complete theory of constitution should explain why material properties of the constituent are systematically related to those of the constituted. Typically, for physical endurants, the spatial location of the
former are inherited by the latter [8] ; for perdurants, the temporal properties of the former are constrained
by the latter [9] . However, these derived relations can apply to many other properties, e.g., the weight, volume, color, chemical structure of the statue are derived from the properties of the constituting clay (Baker,
2007). Now, it would be hard to defend that these derivation relations work the other way around as well
(e.g., that the weight, volume, color, chemical structure of the lump of clay are derived from the properties
of the constituted statue). In fact, although it is natural to conceptualize _The Beatles_ as being constituted
by collective of John, Paul, George, Ringo, it is utterly unnatural to conceptualize the collective as being
constituted by _The Beatles_ . Why is that? We believe that this is because constitution relies on a notion of
_grounding_ . This seems to also explain requirements such as the one proposed by Baker (2007) that _special_
_circumstances_ must hold for the constituent to constitute the constituted (e.g., for the clay to constitute the
statue, an intentional act of the sculptor is required), and that these circumstances are both necessary and
sufficient.
This asymmetry is also often framed in terms of asymmetric cases of dependence (again, strongly
connected to grounding). For example, every instance of statue of clay must be constituted by a particular
lump of clay, but not the other way around, i.e., lumps of clay can exist without constituting statues. In
other words, statues of clay are _generically dependent_ on the type Lump of Clay. This can be captured
with the notions of Generic Constitutional Dependence (GCD), between types _x_ _[′]_ and _y_ _[′]_, as well as the
type-level relation of Constitution (a59) between _x_ of type _x_ _[′]_, and _y_ of type _y_ _[′]_ .


**a58** GCD( _x_ _[′]_ _, y_ _[′]_ ) _↔∀x_ ( _x_ :: _x_ _[′]_ ) _→∃y_ ( _y_ :: _y_ _[′]_ ) _∧_ constitutedBy( _x, y_ )

**a59** Constitution( _x, x_ _[′]_ _, y, y_ _[′]_ ) _↔_ ( _x_ :: _x_ _[′]_ ) _∧_ ( _y_ :: _y_ _[′]_ ) _∧_ GCD( _x_ _[′]_ _, y_ _[′]_ ) _∧_ constitutedBy( _x, y_ )


Now, using another example, we can have a Boxing Match being constituted by one or more punches
(again, an asymmetric dependence). In this case, however, a specific Boxing Match is constituted by
specific punching events, i.e., a case of _specific dependence_ . This is because we are dealing here with a
constitution relation between events and, as previously discussed, events are modally fragile entities and,
hence, all their parts and constituents are necessary constituents (a60).


**a60** _∀x, y_ Perdurant( _x_ ) _∧_ constitutedBy( _x, y_ ) _→_ _2_ (ex( _x_ ) _→_ constitutedBy( _x, y_ ))


In light of these notions of dependence, constitution seems to be similar to the relation of functional
parthood ( _componentOf_ ). ComponentOf is a material relation (Guizzardi, 2009) that also requires “special
circumstances” in order to hold. Due to the different configurations involving different types of dependence relations holding between functional parts, functional parthood is not irrestrictively transitive. In
fact, transitivity only holds in certain scopes defined by these “special circumstances” (Guizzardi, 2009).
Maybe an analogous case can be made to explain why transitivity does not seem to hold for constitution
irrestrictively either. For example, the human tissue that constitutes Paul McCartney does not constitute
_The Beatles_ . Perhaps, like parthood (Guizzardi, 2005), constitution is not a single relation but a family of
relations, each requiring additional axioms extending a very minimal common core.
Again, we advocate that a complete theory of constitution requires a proper theory of grounding. For this
reason, we postpone proposing a complete theory for the former relation in UFO until we can fully advance
a complete theory of the latter relation. In any case, to honor this strong intuition based on grounding
(which is asymmetric) and asymmetric dependence, we assume here that constitution is an asymmetric
relation (a61).


**a61** constitutedBy( _x, y_ ) _→¬_ constitutedBy( _y, x_ )


8We do admit, however, relations of constitution between non-physical endurants (Wang et al., 2014a).
9For the case of parthood between events (Benevides et al., 2019b), we have that the temporal interval framing the parts are
part of the one framing the whole. _Mutatis mutandis_, for the case of constitution between events, we assume the same here for
the relation between the temporal interval framing the constituent and the one framing the constituted.


_Giancarlo Guizzardi et al. / UFO: Unified Foundational Ontology_ 13


In summary, in this rather simplified form, the general relation of constitution is taken here as a nonreflexive and asymmetric relation. Moreover, it is a relation that holds between entities of the same ontological categories but between entities of different Kinds. Specific types of constituents and constituted
entities can extend this minimal axiomatization, for example, to constraint relations between properties of
physical endurants or events. A fuller theory of derivation of properties in this sense, however, waits for a
fuller theory of grounding.


_2.8. Existence and Existential Dependence_


UFO introduces an _existence predicate_ defined on any possible entity. In principle, we can view existence as related to time, ex( _x, t_ ), however, as we are proposing here a single time slice formalization of
UFO, we introduce in (a62) existence as a unary predicate ex( _x_ ). By means of the existence predicate, we
implicitly define in (a63) the relation of _existential dependence_ between two entities, ed( _x, y_ ). We also
implicitly define the notion of existential independence, ind( _x, y_ ), accordingly (a64).


**a62** ex( _x_ ) _→_ Thing( _x_ )

**a63** ed( _x, y_ ) _↔_ _2_ (ex( _x_ ) _→_ ex( _y_ ))


**a64** ind( _x, y_ ) _↔¬_ ed( _x, y_ ) _∧¬_ ed( _y, x_ )


_2.9. Moments and inherence_


We summarize a few points of the formalization of substantials and moments of the original UFO,
as they shall be required in the subsequent sections. Moments are known as _variable tropes_, abstract
particulars, or particular qualities in the philosophical literature (Guizzardi, 2005). In UFO, moments can
be viewed either as individualized properties, such as the color or the weight of an object, for the case of
intrinsic moments, or a marriage or an enrollment, for the case of relational moments (relators), cf. (a40),
(a41). The relation that connects moments to the object that they are about is the relation of _inherence_ .
Inherence is a type of existential dependence relation (a65) holding between a moment and an entity of
which it depends, called its _bearer_ (a66).


**a65** inheresIn( _x, y_ ) _→_ ed( _x, y_ ) (6.4)


**a66** inheresIn( _x, y_ ) _→_ Moment( _x_ ) _∧_ (Type( _y_ ) _∨_ ConcreteIndividual( _y_ ))
(6.10)


Moreover, a moment cannot inhere in two separate individuals (a67), this is the so-called _non-migration_
or _non-transferability_ principle (a67).


**a67** inheresIn( _x, y_ ) _∧_ inheresIn( _x, z_ ) _→_ _y_ = _z_ (6.9)


Moments can also be involved in chains of inherence relations (d2), which are ultimately grounded on
a unique entity that does not inhere in anything else. This entity that we will call here the _Ultimate Bearer_ .
(d3). Furthermore, the ultimate bearer of a moment is unique (a68).


_def_
**d2** momentOf( _m, x_ ) = inheresIn( _m, x_ ) _∨∃y_ (inheresIn( _m, y_ ) _∧_ momentOf( _y, x_ ))


_def_
**d3** ultimateBearerOf( _b, m_ ) = _¬_ Moment( _b_ ) _∧_ momentOf( _m, b_ )


**a68** Moment( _m_ ) _→∃_ ! _b_ ultimateBearerOf( _b, m_ )


Finally, in line with what was proposed originally in UFO (Guizzardi, 2005), we have the following
theorems (t28)–(t30), i.e., inherence is a non-reflexive, asymmetric and anti-transitive relation.


**t28** _¬_ inheresIn( _x, x_ ) (6.5)

**t29** inheresIn( _x, y_ ) _→¬_ inheresIn( _y, x_ ) (6.6)

**t30** inheresIn( _x, y_ ) _∧_ inheresIn( _y, z_ ) _→¬_ inheresIn( _x, z_ ) (6.7)


14 _Giancarlo Guizzardi et al. / UFO: Unified Foundational Ontology_


_2.10. Relators_


We summarize below the presentation of relators by Guizzardi (2005). Recent investigations on relators, relations, and their connections to perdurants (events) have been proposed by Guarino and Guizzardi (2015, 2016). We start by defining _externally dependent modes_ (a70): a mode _x_ that is existentially
dependent on an entity that is independent of the bearer of _x_ .


**a69** externallyDependent( _x, y_ ) _↔_ ed( _x, y_ ) _∧∀z_ (inheresIn( _x, z_ ) _→_ ind( _y, z_ ))


**a70** ExternallyDependentMode( _x_ ) _↔_ Mode( _x_ ) _∧∃y_ (externallyDependent( _x, y_ )) (6 _._ 42)


Externally dependent modes indeed capture truly relational qualities. For instance, by being married to
Mary, in virtue of this relation, John acquires a number of properties (i.e. _modes_ ) that depend on John’s
relationship with Mary; John’s commitment towards Mary is a mode that depends on an individual that is
existentially independent of the bearer of John’s commitment. The condition of existential independence
excludes that an externally dependent mode may depend on individuals that are ontologically too close
to the bearer of the mode. For instance, the courage of John is a mode that depends on John, who is not
existentially independent of himself; for this reason, the courage of John is a mode that is not externally
dependent.
Externally dependent modes (as well as relators, as we discuss later) are founded by means of a unique
event (a71), (a72). E.g., John’s conjugal commitments towards Mary are founded on the event of the
wedding between John and Mary. Since every externally dependent mode is founded by an unique event,
we can define foundationOf( _x_ ) by means of a definite description (d4).


**a71** foundedBy( _x, y_ ) _→_ (ExternallyDependentMode( _x_ ) _∨_ Relator( _x_ )) _∧_ Perdurant( _y_ )


**a72** ExternallyDependentMode( _x_ ) _→∃_ ! _y_ (foundedBy( _x, y_ ))


**d4** foundationOf( _x_ ) = _y ↔_ foundedBy( _x, y_ )


We can now explain what it means for an individual _x_ to be a _qua individual of_ another individual _y_ : the
relation quaIndividualOf holds between _x_ and _y_ iff _x_ is the sum of all externally dependent modes of _y_ that
share the same foundational event (a73). Moreover, an entity is a _qua individual_ iff it is a quaIndividualOf
another entity (a74). For instance, in virtue of the marriage with Mary, John is the bearer of a number of
externally dependent modes related to conjugal commitments that constitute John-qua-husband-of-Mary.
For this reason, we view a qua individual as a complex externally dependent mode (a75), and so it has
a unique foundation, which is the same as the foundation of its parts (a31). Finally, qua individuals are
genuine individuals in the sense that they cannot be attached to two distinct particulars (a76). E.g., John
qua student is the qua individual of John, not of any other person.


**a73** quaIndividualOf( _x, y_ ) _↔∀z_ (O( _z, x_ ) _↔_ (ExternallyDependentMode( _z_ ) _∧_ inheresIn( _z, y_ ) _∧_
foundationOf( _z_ ) = foundationOf( _x_ )))

**t31** quaIndividualOf( _x, y_ ) _∧_ _x_ _[′]_ P _x →_ foundationOf( _x_ ) = foundationOf( _x_ _[′]_ )


**a74** QuaIndividual( _x_ ) _↔∃y_ quaIndividualOf( _x, y_ )


**a75** QuaIndividual( _x_ ) _→_ ExternallyDependentMode( _x_ )

**a76** quaIndividualOf( _x, y_ ) _∧_ quaIndividualOf( _x, y_ _[′]_ ) _→_ _y_ = _y_ _[′]_


We assume that every relator is founded on a unique event (a77), which is also the foundation of the
parts of the relator. Relators are then implicitly defined by (a79): they are sums of qua individuals that
share the same foundation and are existentially dependent on each other.


**a77** Relator( _x_ ) _→∃_ ! _y_ (foundedBy( _x, y_ ))


**a78** Relator( _x_ ) _∧_ _y_ P _x →_ foundationOf( _x_ ) = foundationOf( _y_ )


_Giancarlo Guizzardi et al. / UFO: Unified Foundational Ontology_ 15


**a79** Relator( _x_ ) _↔∃y_ (PP( _y, x_ )) _∧∀y, z_ ((PP( _y, x_ ) _∧_ PP( _z, x_ )) _→_ (QuaIndividual( _y_ ) _∧_
QuaIndividual( _z_ ) _∧_ (foundationOf( _y_ ) = foundationOf( _z_ )) _∧_ ed( _y, z_ ) _∧_ ed( _z, y_ ))) _∧_
_∀y, z_ ((PP( _y, x_ ) _∧_ QuaIndividual( _z_ ) _∧_ (foundationOf( _y_ ) = foundationOf( _z_ )) _∧_ ed( _y, z_ ) _∧_
ed( _z, y_ )) _→_ PP( _z, x_ ))


For example, John and Mary’s wedding is the foundation of a number of externally dependent modes
of John that depend on Mary and of Mary that depend on John, the sum of which constitutes the marriage
relator.
According to this view, relators bring about qua individuals. By (a79), there must exist at least two qua
individuals, _x_ _[′]_ and _x_ _[′′]_, that are part of the relator, given by the existence of a proper part in (a79) and by
strong supplementation (a51). By (t32), those qua individuals are qua individuals of some other individual,
_y_ _[′]_ and _y_ _[′′]_ . Thus, we establish (t32).


**t32** Relator( _x_ ) _→∃x_ _[′]_ _, x_ _[′′]_ _, y_ _[′]_ _, y_ _[′′]_ (quaIndividualOf( _x_ _[′]_ _, y_ _[′]_ ) _∧_ quaIndividualOf( _x_ _[′′]_ _, y_ _[′′]_ ))


We introduce the relation of _mediation_, mediates( _x, y_ ), between a relator _x_ and an individual _y_ that the
relator connects in a relational statement (a80).


**a80** mediates( _x, y_ ) _↔_ Relator( _x_ ) _∧_ Endurant( _y_ ) _∧∃z._ (quaIndividualOf( _z, y_ ) _∧_ P _zx_ )


**t33** Relator( _x_ ) _→∃y, z_ ( _y ̸_ = _z ∧_ mediates( _x, y_ ) _∧_ mediates( _x, z_ ))


By axiom (a79), any relator has at least two distinct qua individuals as parts. Those qua individuals are
associated to distinct individuals by (a74) and (a76), which are mediated by the relator by (a80). Thus, we
infer (t33). [10]

Since a relator is a particular type of moment, it has to have a unique bearer, we define the bearer of the
relator as the mereological sum of the individuals that the relator mediates. Moreover, a relator type is a
type that applies to relators. For instance, _marriage_ is a relator type of which the marriage between John
and Mary is an instance. Relator types are defined according to schema (a44).


_2.11. Characterization_


Guizzardi (2005) states that a type is _characterized_ by moment types that inhere in its instances.


**a81** characterization( _t, m_ ) _→_ EndurantType( _t_ ) _∧_ MomentType( _m_ ) _∧_
_∀x._ ( _x_ :: _t →∃y._ ( _y_ :: _m ∧_ inheresIn( _y, x_ ))) _∧∀z._ ( _z_ :: _m →∃_ ! _w._ ( _w_ :: _t ∧_ inheresIn( _z, w_ )))


In particular, for quality kinds, we have that:


**a82** characterization( _t, q_ ) _∧_ QualityType( _q_ ) _→_ ( _∀x_ :: _q →∃_ ! _y_ :: _t ∧_ inheresIn( _x, y_ ))


_2.12. Qualities and quality structures_


In the following axioms, we use the standard notation from set-theory and arithmetic, i.e., membership
_∈_, set inclusion _⊆_, proper set inclusion _⊂_, Cartesian product _×_, the empty set _∅_, addition +, the greater
or equal relation _≥_, and the natural number zero 0, by appealing to their intuitive meaning. However, we
will not commit to a specific theory. [11]

UFO grounds _quality structures_ in its taxonomy of abstract individuals, which in classified into sets and
quales (a83)–(a85).


10Our theorem (t33) corresponds to axiom (6.45) in Guizzardi’s book (Guizzardi, 2005, §6.45). It is now a theorem, since we
introduced a stronger definition of relators.
11A suitable set theory should be enough for expressing these notions. For instance, New Foundations with Urelements (NFU)
+ Infinity + Choice can represent first-order Peano arithmetic (PA) and Cartesian product. One problem here is that theories of
arithmetic, like Robinson arithmetic (Q) and PA, have no finite models.


16 _Giancarlo Guizzardi et al. / UFO: Unified Foundational Ontology_



**a83** Quale( _x_ ) _→_ AbstractIndividual( _x_ )


**a84** Set( _x_ ) _→_ AbstractIndividual( _x_ )



**a85** _¬∃x_ (Quale( _x_ ) _∧_ Set( _x_ ))



A _quality structure_ is defined as an entity associated with a unique _quality type_ (d5). Moreover, quality
structures are non-empty sets (a86). The members of quality structures are _quale_ s, where an entity is a
quale iff it is a member of a unique quality structure (a87). A quality structure is partitioned into _quality_
_dimension_ and _quality domain_ (a88), (a89). Finally, given two quality types such that one properly specializes the other, the sub-quality-type imposes constraints on the quality structure associated with the superquality-type. Since quality structures are sets, the quality structure associated with the sub-quality-type
must be a proper subset of the quality structure associated with the super-quality-type. For instance, given
that Color is associated with ColorSpace, then SkinColor (a subkind of Color) is associated with a proper
subset of ColorSpace. More formally, for any quality structures _s_ and _s_ _[′]_ and quality types _t_ and _t_ _[′]_ such
that _s_ is associated with _t_, _s_ _[′]_ is associated with _t_ _[′]_, and _t_ _[′]_ is a proper specialization of _t_, then _s_ _[′]_ is a proper
subset of _s_ (a90).


_def_
**d5** QualityStructure( _x_ ) = _∃_ ! _t_ (QualityType( _t_ ) _∧_ associatedWith( _x, t_ )) (6.26)

**a86** QualityStructure( _x_ ) _→_ Set( _x_ ) _∧_ _x ̸_ = _∅_ (6.27)

**a87** Quale( _x_ ) _↔∃_ ! _y_ (QualityStructure( _y_ ) _∧_ _x ∈_ _y_ ) (6.40)

**a88** QualityStructure( _x_ ) _↔_ QualityDomain( _x_ ) _∨_ QualityDimension( _x_ ) (6.23)


**a89** QualityDomain( _x_ ) _→¬_ QualityDimension( _x_ )

**a90** associatedWith( _s, t_ ) _∧_ associatedWith( _s_ _[′]_ _, t_ _[′]_ ) _∧_ _t_ _[′]_ _< t →_ _s_ _[′]_ _⊂_ _s_


An intrinsic moment type is a quality type iff it is associated with a unique quality structure (a91). A
_quality_ is defined as an entity that instantiates a unique _quality kind_ (d6).


**a91** QualityType( _t_ ) _↔_ IntrinsicMomentType( _t_ ) _∧∃_ ! _x_ (QualityStructure( _x_ ) _∧_ associatedWith( _x, t_ )) (6.24)


_def_
**d6** Quality( _x_ ) = _∃_ ! _t_ (QualityKind( _t_ ) _∧_ _x_ :: _t_ ) (6.25)


The hasValue relation holds from qualities to quales (a92), where hasValue is functional (a93). From
(d6), we have that a _quality_ instantiates a unique _quality kind_, which from (a91) is associated to at least
one quality structure. The axiom (a94) enforces each _quale_ of a _quality_ to be member of such _quality_
_structure_ s.


**a92** hasValue( _x, y_ ) _→_ Quality( _x_ ) _∧_ Quale( _y_ ) (6.37)

**a93** Quality( _x_ ) _→∃_ ! _y_ (hasValue( _x, y_ )) (6.39)

**a94** hasValue( _x, y_ ) _→∃t, s_ ( _x_ :: _t ∧_ associatedWith( _s, t_ ) _∧_ _y ∈_ _s_ ) (6.38)


UFO-A also defines what is for a quality (type) to be _simple_ or _complex_ . A _simple quality_ is a quality
that bears nothing (d7). A _complex quality_ is a quality but not a simple quality (d8). A _simple quality_
_type_ is a quality type that have only simple qualities as instances (d9). Similarly, a _complex quality type_
is a quality type that have only complex qualities as instances (d10). Moreover, quality dimensions can
only be associatedWith simple quality types, and vice versa (a95), while quality domains can only be
associatedWith complex quality types, and vice versa (a96).


_def_
**d7** SimpleQuality( _x_ ) = Quality( _x_ ) _∧¬∃y_ (inheresIn( _y, x_ )) (6.28)


_def_
**d8** ComplexQuality( _x_ ) = Quality( _x_ ) _∧¬_ SimpleQuality( _x_ ) (6.29)


_def_
**d9** SimpleQualityType( _t_ ) = QualityType( _t_ ) _∧∀x_ ( _x_ :: _t →_ SimpleQuality( _x_ )) (6.30)


_def_
**d10** ComplexQualityType( _t_ ) = QualityType( _t_ ) _∧∀x_ ( _x_ :: _t →_ ComplexQuality( _x_ )) (6.31)

**a95** associatedWith( _x, y_ ) _→_ (QualityDimension( _x_ ) _↔_ SimpleQualityType( _y_ )) (6.34)

**a96** associatedWith( _x, y_ ) _→_ (QualityDomain( _x_ ) _↔_ ComplexQualityType( _y_ )) (6.35)


_Giancarlo Guizzardi et al. / UFO: Unified Foundational Ontology_ 17


Since the qualities of a complex quality _x_ :: _X_ correspond to the quality dimensions of the quality
domain associated with _X_, then no two distinct qualities inhering a complex quality can be of the same
type (a97). Moreover, since quality dimensions are unidimensional, and quality domains can only be
defined by quality dimensions, then complex qualities can only bear simple qualities (a98).


**a97** ComplexQuality( _x_ ) _∧_ _y_ :: _Y ∧_ _z_ :: _Z ∧_ inheresIn( _y, x_ ) _∧_ inheresIn( _z, x_ ) _∧_ _Y_ = _Z →_ _y_ = _z_ (6.32)


**a98** ComplexQuality( _x_ ) _→∀y_ (inheresIn( _y, x_ ) _→_ SimpleQuality( _y_ )) (6.33)


Concerning quality domains, each quality domain _d_ associatedWith a complex quality type _t_ can be
defined in terms of the Cartesian product of the quality dimensions associatedWith the quality types
characterizing _t_ (a99).



**a99** QualityDomain( _x_ ) _∧_ associatedWith( _x, t_ ) _→∃y_ 1 _, . . ., yn, z_ 1 _, . . ., zn_ (( _x ⊆_ _y_ 1 _× . . . × yn_ ) _∧_
_n_

   



- (associatedWith( _yi, zi_ ) _∧_ characterization( _t, zi_ )) _∧∀w_ (characterization( _t, w_ ) _→_

_i_ =1



_n_





- ( _w_ = _zi_ ))) (6.36)

_i_ =1



A metric space _s_ is obtained from a quality domain _s_ by associating a distance function _d_ (called the
metric of _s_ ) such that for every two quality values _x_, _y_ in _s_, _d_ ( _x, y_ ) represents the distance between _x_ and
_y_ in _s_ (see Guizzardi, 2005, §6.11). Here, we define _d_ as a left-total functional ternary relation _d_ ( _x, y, r_ )
such that _r_ is the distance between the quales _x_ and _y_, see (a100), (a101).


**a100** _d_ ( _x, y, r_ ) _→_ (Quale( _x_ ) _∧_ Quale( _y_ ) _∧∃z_ (memberOf( _x, z_ ) _∧_ memberOf( _y, z_ )))


**a101** (Quale( _x_ ) _∧_ Quale( _y_ )) _→∃_ ! _r_ ( _d_ ( _x, y, r_ ))


Moreover, the distance relation _d_ must also obey the following constraints:


a) _x_ = _y ∧_ _d_ ( _x, y, r_ ) _→_ ( _r_ = 0);
b) _d_ ( _x, y, r_ ) _→_ _d_ ( _y, x, r_ );

c) _d_ ( _x, y, r_ 0) _∧_ _d_ ( _y, z, r_ 1) _∧_ _d_ ( _x, z, r_ 2) _∧_ +( _r_ 0 _, r_ 1 _, s_ ) _→_ _s ≥_ _r_ 2 (triangle inequality) [12]


The notion of _region_ is also informally defined by Guizzardi (2005, §6.2.6). A region is a kind of
division of a quality structure with respect to a specific quale and according to the structure of the quality
structure. Definition 6.12 (see quality region, Guizzardi, 2005, p.228) states that a _quality region_ is a
convex region _c_ of a quality domain; while _c_ is convex iff for all two points _x_, _y_ in _c_, all points between _x_
and _y_ are also in _c_ . We think that a suitable set theory would be able to represent the required topological
notions.


_2.13. Endurants and perdurants_


Any endurant is connected to a perdurant by the _manifestation_ relation (a102). The _life of_ an endurant
is then specified by a functional relation that associates the endurant with the mereological sum of all the
events that manifest it (a103). The life of an endurant is unique due to the unicity of mereological sums.
Moreover, the case where two perdurants are consecutive in time is here abstractly modeled by means of
the _meet_ relation (a104). We refer to Guizzardi et al. (2016) for the detailed presentation of this approach,
and to Benevides et al. (2019b) for a complete formalization of the UFO-B ontology.


**a102** manifests( _x, y_ ) _→_ Endurant( _x_ ) _∧_ Perdurant( _y_ )


**a103** lifeOf( _x, y_ ) _↔_ Perdurant( _x_ ) _∧_ Endurant( _y_ ) _∧∀z_ (O( _z, x_ ) _↔_ Perdurant( _z_ ) _∧_ manifests( _z, y_ ))


**a104** meet( _x, y_ ) _→_ Perdurant( _x_ ) _∧_ Perdurant( _y_ )


12+( _r_ 0 _, r_ 1 _, s_ ) denotes the relationship that holds when the arithmetic equation _s_ = _r_ 0 + _r_ 1 is true.


18 _Giancarlo Guizzardi et al. / UFO: Unified Foundational Ontology_


So, there is a special perdurant (which we may call a process, in a very particular sense) that is the
life of an endurant, i.e., the sum of everything that is a manifestation of the dispositions inhering in) that
perdurant (Guizzardi et al., 2016). As previously discussed, perdurants have all their parts and constituents
necessarily. So, every single manifestation of that endurant literally changes its life (a change _of_ life, not
a change _in_ the life!). In other words, this particular perdurant represents the _current life of an endurant_ at
each point in time (Guizzardi et al., 2016).


**3. Analysis and formalization in UFO: examples**


This section presents an analysis and formalization of various cases that originate from the First FOUST
Workshop – the Foundational Stance, an international forum dedicated to Foundational Ontology research.
They cover a number of topics (composition/constitution, roles, property change, event change, and conceptual evolution) and are also addressed by other papers in this special issue to facilitate the comparison
of the various approaches. Each of the following sub-sections begins with a quote of the text supplied as
the case description, which is followed by our analysis. We employ OntoUML diagrams and provide some
formalization to accompany them.


_3.1. Composition/constitution_


_1) “There is a four-legged table made of wood. Some time later, a leg of the table is replaced. Even later,_
_the table is demolished so it ceases to exist although the wood is still there after the demolition.”_


Figure 2. The Wooden Table case in OntoUML.


Figure 2 depicts an OntoUML model [13] representing this situation. In this model, a Wood Portion is
a quantity (in the technical sense discussed by Guizzardi (2010), i.e., a maximally topologically selfconnected portion of matter). It is _contingent_ for a Wood Portion to constitute a Wooden Table Component.
In this model, Wooden Table Components are artifacts that are manufactured to necessarily serve the role
of Wooden Table Component (i.e., Wooden Table Component is a nominal kind/artifact kind). Two par

13In OntoUML, the stereotypes «kind» and «quantity» stand for ObjectKind and QuantityKind, respectively.


_Giancarlo Guizzardi et al. / UFO: Unified Foundational Ontology_ 19


ticular subkinds considered are a Table Leg Component (e.g., that has necessarily a shape and necessarily a certain structure capable of supporting a certain weight range, etc.) and a Table Top Component. A
Wooden Table is structured in a number of functional roles associated via componentOf relations, i.e.,
parthood relations in which the parts play a functional role with respect to the whole (see Guizzardi, 2009),
that can _contingently_ be played by Wooden Table Components. Since the relation between the table and
its parts is one of _generic dependence_, parts can be replaced without any impact on the identity of the
table. Moreover, since the relation between a Wood Portion and each Wooden Table Component (that it
contingently constitutes) is one of constitution and not one of identity, the lifecycles of the former and the
latter are completely independent. Therefore, a Wood Portion can survive the destruction of these wood
components and the destruction of the table as a functional complex. Finally, as represented by the black
diamond in the figure (exclusive parthood), each Table Leg Component can only be part of one single
Wooden Table at a certain point in time.
In the sequel, we show a partial formalization of this case.


QuantityKind(WoodPortion)


Being a Wooden Component Constituent is a role played by a Wood Portion in the scope of a (contingent) constitution relation with a Wooden Table Component:


Role(WoodenComponentConstituent)

WoodenComponentConstituent _⊑_ WoodPortion

_∀x._ ( _x_ :: WoodenComponentConstituent _→∃_ ! _y._ ( _y_ :: WoodenTableComponent _∧_
constitutedBy( _y, x_ )))


This constitution relation is also contingent from the point of view of the Wooden Table Component,
i.e., the Wooden Table Component can be constituted by different Wood Portions in different situations
(worlds): [14]


_∀x._ ( _x_ :: WoodenTableComponent _→∃_ ! _y._ ( _y_ :: WoodenComponentConstituent _∧_
constitutedBy( _x, y_ )))


ObjectKind(WoodenTable)


ObjectKind(WoodenTableComponent)


SubKind(TableLegComponent)


SubKind(TableTopComponent)

TableTopComponent _⊑_ WoodenTableComponent

TableLegComponent _⊑_ WoodenTableComponent


To allow the representation of Table Leg Component and Table Top Component as disjoint types, we
introduce (a105):


**a105** isDisjointWith( _t, t_ _[′]_ ) _↔_ Type( _t_ ) _∧_ Type( _t_ _[′]_ ) _∧¬∃x_ ( _x_ :: _t_ 1 _∧_ _x_ :: _t_ 2)

isDisjointWith(TableLegComponent _,_ TableTopComponent)


Right Rear Leg, Right Front Leg, Left Front Leg, Left Rear Leg and Top Component are roles
played by a Table Leg Component (the first four) and Table Top Component (the latter) in the scope of
a _component of_ relation with a Table:


14One should notice that these formulae here are a special case of (a58) in which there is a single constituent involved. In
other words, a case of what is called _wholly constituting_ . Moreover, since WoodenTableComponent is a kind, its instances are
always generically dependent on WoodenComponentConstituent. In contrast, since WoodenComponentConstituent is a role,
WoodPortion is only dependent on WoodenTableComponent insofar as it instantiates the WoodenComponentConstituent
role.


20 _Giancarlo Guizzardi et al. / UFO: Unified Foundational Ontology_


Role(RightRearLeg)


Role(RightFrontLeg)


Role(LeftRearLeg)


Role(LeftFrontLeg)


Role(TopComponent)

RightRearLeg _⊑_ TableLegComponent

RightFrontLeg _⊑_ TableLegComponent

LeftRearLeg _⊑_ TableLegComponent

LeftFrontLeg _⊑_ TableLegComponent

TopComponent _⊑_ TableTopComponent


For example, Right Front Leg is a role played by a Table Leg Component when being a functional
part of a Wooden Table. Guizzardi (2009) defines the relation of _component of_ between a functional part
and a functional complex, and it conflates a mereological relation plus a relation of functional dependence.
Here, in order for a Table Component to function as a Table Component, it must be part of a Table
functioning as a Table ( _Mutatis mutandis_, the same for the roles of Right Rear Leg, Left Front Leg,
Left Rear Leg and Top Component):


_∀x._ ( _x_ :: RightFrontLeg _→∃_ ! _y._ ( _y_ :: WoodenTable _∧_
componentOf( _x,_ RightFrontLeg _, y,_ WoodenTable))


In the converse direction, in order for a Wooden Table to function as such it must be composed
of four distinct Table Leg Components and a Top Component (which here are all assumed to be
Wooden Table Components), each of these functioning in a particular role:


_∀x._ ( _x_ :: WoodenTable _→∃y_ 1 _, y_ 2 _, y_ 3 _, y_ 4 _, y_ 5 _._ ( _y_ 1 :: RightRearLeg _∧_ _y_ 2 :: RightFrontLeg _∧_
_y_ 3 :: LeftFrontLeg _∧_ _y_ 4 :: LeftRearLeg _∧_ _y_ 5 :: TopComponent _∧_
componentOf( _y_ 1 _,_ RightRearLeg _, x,_ WoodenTable) _∧_
componentOf( _y_ 2 _,_ RightFrontLeg _, x,_ WoodenTable) _∧_
componentOf( _y_ 3 _,_ LeftFrontLeg _, x,_ WoodenTable) _∧_
componentOf( _y_ 4 _,_ LeftRearLeg _, x,_ WoodenTable) _∧_
componentOf( _y_ 5 _,_ TopComponent _, x,_ WoodenTable) _∧_
( _y_ 1 _̸_ = _y_ 2) _∧_ ( _y_ 1 _̸_ = _y_ 3) _∧_ ( _y_ 1 _̸_ = _y_ 4) _∧_ ( _y_ 2 _̸_ = _y_ 3) _∧_ ( _y_ 2 _̸_ = _y_ 4) _∧_ ( _y_ 3 _̸_ = _y_ 4))


The relation of _component of_ is a relation of generic dependence from the whole to the part and from the
part to the whole. So, not only the Wooden Table can have different Wooden Table Components playing
these functional part roles in different situations, but these components can play these roles in different
tables in different situations.
From an OntoUML model and using its supporting tools, we can automatically generate models that
satisfy the logical theory corresponding to the OntoUML model (Benevides et al., 2010). In conceptual
modeling terms, this means that we can generate instances that are admissible by an OntoUML model. In
the sequel, we show a number of examples (Figures 3 to 5) of these visual models automatically generated
for the OntoUML diagram of Figure 2.


_Giancarlo Guizzardi et al. / UFO: Unified Foundational Ontology_ 21


Figure 3. A Wood Portion exists in world _w_ 1 without constituting any object (Object0 :: WoodPortion) and in _w_ 2 it
goes on to constitute a Wooden Table Component, namely, a Table Top Component (Object1 :: WoodenTableComponent,
Object1 :: TableTopComponent).


Figure 4. A Table Leg Component (Object3 :: TableLegComponent, Object3 :: WoodenTableComponent) exists in _w_ 1 being
constituted by a Wood Portion (Object7 :: WoodPortion) and, in _w_ 2, it still exists but now constituted by a different Wood
Portion (Object4 :: WoodPortion).


Figure 5. A Wooden Table (Object10 :: WoodenTable) exists in world _w_ 1 being composed by a Table Leg Component
that plays in it a functional role of Right Rear Leg (Object5 :: WoodenTableComponent _,_ Object5 :: TableLegComponent,
Object5 :: RightRearLeg, componentOf(Object5, RightRearLeg, Object10 _,_ WoodenTable)) and which, in that world,
is constituted by a particular Wood Portion (Object1 :: WoodPortion, Object1 :: WoodenComponentConstituent,
constitutedBy(Object5, Object1)). In a different world _w_ 2, the table still exists but now having that same
Table Leg Component Object5 playing a different role, namely, that of a Left Front Leg (Object5 :: LeftFrontLeg,
componentOf(Object5, LeftFrontLeg, Object10 _,_ WoodenTable)). In that world, this Table Leg Component is also constituted by a different Wood Portion (constitutedBy(Object5, Object0)).


_3.2. Roles_


_2) “Mr. Potter is the teacher of class 2C at Shapism School and resigns at the beginning of the spring_
_break. After the spring break, Mrs. Bumblebee replaces Mr. Potter as the teacher of 2C. Also, student_
_Mary left the class at the beginning of the break and a new student, John, joins in when the break_
_ends.”_


In this example, captured in the OntoUML of Figure 6, Teacher is a role played by a person when
mediated by an Employment relator (Guizzardi and Wagner, 2008; Guarino and Guizzardi, 2015) connecting her to a School. Analogously, Student is a role played by a Person when connected via a
School Enrollment relator to a School. A School makes Course Offerings (a relator) to a given


22 _Giancarlo Guizzardi et al. / UFO: Unified Foundational Ontology_


Class (a collective forming the target community to which that course is addressed). Students can enroll
to a Course Offering via a Course Enrollment relator, connecting the former to a particular enrollment
of a Student in that School. In other words, the enrollment of a Student to a Course Offering _existen-_
_tially depends_ both on the offering and on a particular School Enrollment of that Student. Notice that
the relation from Course Enrollment to Course Offering is one of existential dependence (mediation,
Guizzardi and Wagner, 2008; Guarino and Guizzardi, 2015) and, hence, immutable. However, the relation
from Course Offering to Course Enrollment is an optional relation of generic dependence and, thus,
contingent, mutable. For this reason, the set of students actually enrolled in a given Course Offering
can change from situation to situation. Analogously, a Teacher is assigned to a Course Offering by
having a Course Teacher Assignment relator that connects a Course Offering to an Employment of
a Teacher . In other words, a teacher’s assignment to a course offering existentially depends on both on
the Course Offering and on the Employment of a Teacher in that School. Again, since the relation
from Course Offering to Teacher Assignment is one of generic dependence, different teachers can be
assigned to a course offering in different points in time.


Figure 6. The School case in OntoUML.


In the sequel, we show a partial formalization of this case.


ObjectKind(School)


ObjectKind(Course)


ObjectKind(Person)


CollectiveKind(Class)


Teacher is a role (contingently) played by a Person in the scope of an Employment relation to a
School.


Role(Teacher)

Teacher _⊑_ Person


RelatorKind(Employment)

_∀x_ ( _x_ :: Teacher _→∃y_ ( _y_ :: Employment _∧_ mediates( _y, x_ ))


_Giancarlo Guizzardi et al. / UFO: Unified Foundational Ontology_ 23


_∀x_ ( _x_ :: Employment _→∃_ ! _y,_ ! _z_ ( _y_ :: Teacher _∧_ _z_ :: School _∧_ mediates( _x, y_ ) _∧_ mediates( _x, z_ )))


Student is a role (contingently) played by a Person in the scope of an Enrollment relation to a
School.


Role(Student)

Student _⊑_ Person


RelatorKind(SchoolEnrollment)

_∀x_ ( _x_ :: Student _→∃y_ ( _y_ :: SchoolEnrollment _∧_ mediates( _y, x_ ))

_∀x_ ( _x_ :: SchoolEnrollment _→∃_ ! _y,_ ! _z_ ( _y_ :: Student _∧_ _z_ :: School _∧_ mediates( _x, y_ ) _∧_
mediates( _x, z_ )))


A School can make several Course Offerings to Classes. Students can be members of Classes.
A Class must have at least two Students as members. Notice that a Course Offering in this model
is a particular instantiation of the UFO-S Service Offering pattern (Falbo et al., 2016), having the
Classhere as the Target Community.


RelatorKind(CourseOffering)

_∀x_ ( _x_ :: CourseOffering _→∃_ ! _y,_ ! _z, w_ ( _y_ :: School _∧_ _z_ :: Course _∧_ _w_ :: Class _∧_ mediates( _x, y_ ) _∧_
mediates( _x, z_ ) _∧_ mediates( _x, w_ )))

_∀x_ ( _x_ :: Student _→∃y_ ( _y_ :: Class _∧_ memberOf( _x, y_ ))

_∀x_ ( _x_ :: Class _→∃y, z_ ( _y_ :: Student _∧z_ :: Student _∧_ ( _y ̸_ = _z_ ) _∧_ memberOf( _y, x_ ) _∧_ memberOf( _z, x_ )))


Students that are enrolled in a School can enroll in Course Offerings of that School. Notice that a
Course Enrollment here is an instantiation of the UFO-S pattern of Service Agreements (Falbo et al.,
2016). [15]


RelatorKind(CourseEnrollment)

_∀x_ ( _x_ :: CourseEnrollment _→∃_ ! _y,_ ! _z_ ( _y_ :: SchoolEnrollment _∧_ _z_ :: CourseOffering _∧_
mediates( _x, y_ ) _∧_ mediates( _x, z_ )))


Teachers can be assigned to Course Offerings. There is exactly one Teacher assigned to a
Course Offering in a given situation. However, since the relation between Course Offering and
Course Teacher Assignment is one of generic dependence, different Teachers can be assigned to the
same Course Offering in different situations. [16]


RelatorKind(CourseTeacherAssignment)

_∀x_ ( _x_ :: CourseTeacherAssignment _→∃_ ! _y,_ ! _z_ ( _y_ :: Employment _∧_ _z_ :: CourseOffering _∧_
mediates( _x, y_ ) _∧_ mediates( _x, z_ )))

_∀x, y, z_ ( _x_ :: CourseOffering _∧_ _y_ :: CourseTeacherAssignment _∧_
_z_ :: CourseTeacherAssignment _∧_ mediates( _y, x_ ) _∧_ mediates( _z, x_ ) _→_ ( _y_ = _z_ ))


Figure 7 shows visual models automatically generated for the OntoUML diagram of Figure 6 illustrating
the dynamics of change in this domain.


15The complete specification of this case includes a constraint that guarantees that a Student can only enroll in
Course Offerings of the Schools in which he has a School Enrollment. This constraint is automatically detected and included in the specification by the anti-pattern detection and rectification support of the OntoUML tool (Guerson et al., 2015). We
omit it here, nonetheless, for the sake of brevity.
16The complete specification of this case includes a constraint that guarantees that a Teacher can only be assigned to
Course Offerings of the Schools in which she has an Employment relationship. Once more, this constraint is automatically
detected and included in the specification by the anti-pattern detection and rectification support of the OntoUML tool. Once
more, we omit it here, nonetheless, for the sake of brevity.


24 _Giancarlo Guizzardi et al. / UFO: Unified Foundational Ontology_


Figure 7. In world _w_ 1, we have a School Object0 (Object0 :: School) and a student Object3 (Object3 :: Student)
enrolled in that School (by Property3 (Property3 :: SchoolEnrollment)) and who is part of Class Object4
(Object4 :: Class). Moreover, we have a Teacher Object1 (Object1 :: Teacher) that works for that School (by
Employment Property0 (Property0 :: Employment)). There is also a Course Offering (Property2 :: CourseOffering)
of Course Object5 (Object5 :: Course, e.g., CS 101,) made by that School to Class Object4. Finally, Student
Object3 enrolls in Course Offering Property2 (by Course Enrollment Property6 (Property6 :: CourseEnrollment))
and Teacher Object1 is assigned to teach that Course Offering (by Course Teacher Assignment Property1
(Property1 :: CourseTeacherAssignment)). In world _w_ 2, a different Teacher Object2 (Object2 :: School), who is
also employed in that same school (by Employment Property4 (Property4 :: Employment)), is now assigned to that
Course Offering Property2.


_3.3. Property change_


_3.a) “A flower is red in the summer. As time passes, the color changes. In autumn the flower is brown.”_


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

