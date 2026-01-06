# UFO: Unified Foundational Ontology - Complete Documentation

**Source**: Guizzardi et al. (2021), "UFO: Unified Foundational Ontology", Applied Ontology

**Authors**: Giancarlo Guizzardi, Alessander Botti Benevides, Claudenir M. Fonseca, Daniele Porello, João Paulo A. Almeida, Tiago Prince Sales

**Status**: Definitive reference for UFO (consolidates 20 years of development)

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Foundations & Philosophy](#foundations--philosophy)
3. [Core Taxonomies](#core-taxonomies)
4. [Type Theory](#type-theory)
5. [Relations & Dependencies](#relations--dependencies)
6. [Change & Events](#change--events)
7. [Quality Structures](#quality-structures)
8. [Constitution & Grounding](#constitution--grounding)
9. [Formal Axiomatization](#formal-axiomatization)
10. [OntoUML Modeling Language](#ontouml-modeling-language)
11. [Applications & Impact](#applications--impact)
12. [Comparison with Other Ontologies](#comparison-with-other-ontologies)
13. [Advanced Topics](#advanced-topics)

---

## Executive Summary

### What is UFO?

**UFO (Unified Foundational Ontology)** is a philosophically and logically rigorous framework for conceptual modeling, developed over 20+ years to provide foundational categories and principles for representing reality at the mesoscopic level.

### Key Innovations

1. **Relators as First-Class Entities**: Relationships are reified as dependent entities (relators), solving classical problems like Bradley's Regress
2. **Fine-Grained Type Theory**: 14 meta-types (Kind, Role, Phase, etc.) based on rigidity and sortality
3. **3D Ontology**: Clear distinction between endurants (persist) and perdurants (unfold)
4. **Trope-Based**: Particularized properties (moments) are fundamental
5. **Multi-Level Modeling**: Types can be instances of higher-order types

### Why It Matters

- **Precision**: Eliminates ambiguities in conceptual models
- **Validation**: Automated anti-pattern detection
- **Interoperability**: Common semantic foundation across domains
- **Proven**: 50+ domains, empirically validated

---

## Foundations & Philosophy

### 1.1 Philosophical Stance

#### Descriptive vs Revisionary

UFO is **descriptive** (Strawson 1959):
- Reflects actual cognitive/linguistic reality
- Not prescriptive about "ideal" categorization
- Takes seriously how humans naturally conceptualize domains

**Quote from paper**:
> "UFO aims at providing instruments for describing what is real, at the mesoscopic level, and as accounted for by human cognition. For this reason, not only rocks and animals are real, but so are enrollments, employments, presidential mandates, symptoms, covalent bonds, birthday parties and football matches, colors and electrical charges, organizations and constitutions, software systems and derivative contracts."

#### Realism

UFO is **stubbornly realist** (Smith 2019):
- Tables, marriages, colors exist in the world
- Not merely epistemic constructs
- But world can be "taken in many ways" (pluralism)

**Key tension**:
- Multiple ontologically viable worldviews exist (pluralism)
- Not all worldviews are equally valid ("carve reality at its joints")
- Goal: **Intra-worldview consistency** + **Inter-worldview interoperability**

#### Four-Category Ontology (Aristotelian Square)

UFO countenances:
1. **Types** (universals, patterns)
2. **Individuals** (particulars)
3. **Substantials** (independent individuals)
4. **Moments** (dependent individuals - tropes/aspects)

Why needed:
- Conceptual modeling requires both types AND individuals
- Must represent both objects AND their properties
- Properties appear as "bearers of properties" (weak entities, relationships with attributes)

### 1.2 Historical Development

#### Origins

**1989-2004**: Bunge-Wand-Weber (BWW) approach
- Used Mario Bunge's ontology for evaluating modeling languages
- Problems: Mismatch between Bunge's physics-oriented ontology and modeling needs
- BWW disavowed reified relationships (conflicted with practice)

**2004**: Attempted unification
- DOLCE (Descriptive Ontology for Linguistic and Cognitive Engineering)
- GFO (General Formal Ontology)
- Result: "Unified Foundational Ontology"

**2004-2021**: UFO evolution
- Driven by conceptual modeling requirements
- Informed by OntoUML applications in diverse domains
- Expanded from substantials-only to all endurants

#### Key Influences

- **Philosophy**: Lowe, Fine, Baker, Guarino
- **Cognitive Science**: Jackendoff, Gärdenfors (conceptual spaces)
- **Linguistics**: Davidson, Parsons (event semantics)
- **Logic**: Modal logic, mereology

### 1.3 Structure of UFO

**UFO-A**: Ontology of endurants (focus of this paper)

**UFO-B**: Ontology of perdurants/events
- Event mereology
- Temporal ordering
- Participation
- Causation
- Manifestation of dispositions

**UFO-C**: Ontology of social/intentional entities
- Built on UFO-A and UFO-B
- Commitments, claims, goals, beliefs

---

## Core Taxonomies

### 2.1 Fundamental Dichotomy: Endurant vs Perdurant

#### Endurant

**Definition**: Individuals that exist in time **with all their parts**

**Characteristics**:
- Have essential and accidental properties
- Can qualitatively change while maintaining numerical identity
- Persist through time

**Examples**:
- Mick Jagger
- The Moon
- John's headache
- Mary's marriage to Paul

**Identity**: Defined by unique Kind instantiated

#### Perdurant

**Definition**: Individuals that unfold in time **accumulating temporal parts**

**Characteristics**:
- Manifestations of dispositions
- Only exist in the past
- **Modally fragile**: No cross-world identity (cannot be different than what they are)
- Cannot genuinely change

**Examples**:
- 2020 U.S. Presidential Election
- World War II
- UEFA Euro 2021 Final

**Key insight**:
> "Perdurants are modally fragile, i.e., there is no cross-world identity between them and, hence, they cannot be in any way different than what they are. Changes are perdurants but perdurants cannot be the subject of change."

**Contrast with 4D ontologies**: 4D treats everything as perdurant. UFO is 3D.

### 2.2 Endurant Taxonomy

```
Endurant
├── Substantial (independent)
│   ├── Object (functional complex)
│   ├── Collective (homogeneous parts)
│   └── Quantity (maximally-connected matter)
└── Moment (dependent)
    ├── Intrinsic Moment
    │   ├── Quality (projectable to value space)
    │   └── Mode (cannot project, bears moments)
    │       └── Disposition (function, capability, capacity)
    └── Relator (multi-sided dependent)
        └── Qua Individual (bearer-specific perspective)
```

#### 2.2.1 Substantial

**Definition**: Independent entities

**Axiom**: `Substantial(x) → ¬∃y(Moment(y) ∧ ed(x,y) ∧ ¬ed(y,x))`

**Examples**:
- Mick Jagger
- Free University of Bozen-Bolzano

**Unity Categories** (how parts relate):

**Object (Functional Complex)**
- Parts play **differentiated functional roles**
- Examples: human body (heart ≠ lungs ≠ brain), organization, computer, car
- Mereologically complex with functional organization

**Collective**
- Parts play the **same role** with respect to whole
- Examples: Black Forest (tree = tree = tree), deck of cards, Dutch-speaking group
- Uniform role distribution

**Quantity**
- **Maximally-topologically-self-connected** homeomerous amounts of matter
- Examples: puddle of water, pile of sand
- Continuous stuff of same material

#### 2.2.2 Moment

**Definition**: Existentially dependent entities (tropes, aspects, abstract particulars)

**Key principle**: Moments are **parasitic** - can only exist by **inhering in** other entities

**Axiom**: `Moment(x) → ∃y(inheresIn(x,y))`

##### Intrinsic Moments

**Quality**

**Definition**: Reifications of categorical properties that can be directly projected into value spaces

**Characteristics**:
- Associated with **Quality Structure** (abstract value space)
- Can change value via `hasValue` relation
- Inherence is immutable, but value is mutable

**Examples**:
- Color (projects to color spindle)
- Height (projects to positive reals)
- Weight (projects to mass scale)
- Electrical charge

**Key relations**:
```
Quality --inheresIn--> Endurant (immutable)
Quality --hasValue--> Quale (mutable)
Quale --memberOf--> QualityStructure
QualityType --associatedWith--> QualityStructure
```

**Mode**

**Definition**: Intrinsic moments that bear their own moments

**Characteristics**:
- Cannot be directly projected to value space
- Can have qualities that vary independently
- More complex than qualities

**Includes**:
- **Dispositions**: functions, capabilities, capacities, vulnerabilities
- **Externally dependent modes**: e.g., love of John for Mary

**Examples**:
- Paul's Dengue Fever (mode with intensity quality)
- Matteo's capacity for programming in Scratch
- John's love for Mary (externally dependent on Mary)

##### Externally Dependent Modes

**Definition**: Modes that inhere in entity `x` while being existentially dependent on entity `y` mereologically disjoint from `x`

**Axiom**: `externallyDependent(x,y) ↔ ed(x,y) ∧ ∀z(inheresIn(x,z) → ind(y,z))`

**Example**: John's commitment toward Mary
- Inheres in John
- Externally dependent on Mary
- Mary is existentially independent of John

##### Qua Individual

**Definition**: Complex mode composed of externally dependent modes sharing:
1. Same bearer
2. Same source of external dependence
3. Same foundational event

**Example**: John-qua-husband-of-Mary
- Sum of all commitments and claims of John toward Mary
- All inhere in John
- All externally dependent on Mary
- All founded in wedding event

**Formal**:
```
quaIndividualOf(x,y) ↔
  ∀z(O(z,x) ↔ (ExternallyDependentMode(z) ∧
               inheresIn(z,y) ∧
               foundationOf(z) = foundationOf(x)))
```

##### Relator

**Definition**: Moment that is an aggregation of qua individuals

**Characteristics**:
- Existentially dependent on **multiple** individuals
- Founded by unique event
- Serves as **truthmaker** for material relations

**Structure**:
```
Relator = QuaIndividual₁ + QuaIndividual₂ + ... + QuaIndividualₙ
where all share same foundational event
```

**Example**: John and Mary's Marriage
- Composed of:
  - John-qua-husband-of-Mary
  - Mary-qua-wife-of-John
- Founded by wedding event
- Existentially dependent on both John and Mary

**Why revolutionary**:
- Most ontologies: relationships as predicates or universals
- UFO: relationships as **reified dependent entities**
- Solves Bradley's Regress
- Allows relationships to have properties

**Axiom**:
```
Relator(x) ↔ ∃y(PP(y,x)) ∧
  ∀y,z((PP(y,x) ∧ PP(z,x)) →
    (QuaIndividual(y) ∧ QuaIndividual(z) ∧
     foundationOf(y) = foundationOf(z) ∧
     ed(y,z) ∧ ed(z,y)))
```

**Examples from paper**:
- Marriage
- Enrollment
- Employment
- Contract
- Presidential mandate

### 2.3 Abstract Individuals

**Set**: Abstract collections

**Quale**: Abstract value in quality structure
- Example: The color value "Red" in ColorSpace
- Not the quality instance, but the abstract point

**Quality Structure**: Non-empty set of qualia
- **Quality Dimension**: 1D (e.g., height scale ≅ ℝ⁺)
- **Quality Domain**: Multi-dimensional (e.g., color spindle, taste tetrahedron)

---

## Type Theory

### 3.1 Types vs Individuals

**Fundamental partition**:

**Type**: `Type(x) ↔ ◇(∃y(y::x))`
- Something that is possibly instantiated
- Can be first-order or second-order

**Individual**: `Individual(x) ↔ □(¬∃y(y::x))`
- Necessarily not instantiated
- Concrete or abstract

**Instantiation** (`::`)
- Domain: Type ∪ Individual
- Codomain: Type
- At most second-order: `¬∃x,y,z(Type(x) ∧ x::y ∧ y::z)`

### 3.2 Specialization

**Definition** (extensional inclusion):
```
x ⊑ y ↔ Type(x) ∧ Type(y) ∧ □(∀z(z::x → z::y))
```

**Properties**:
- Quasi-reflexive: `x ⊑ y → (x ⊑ x ∧ y ⊑ y)`
- Transitive: `x ⊑ y ∧ y ⊑ z → x ⊑ z`

**Common supertype axiom**: Types with common instance share supertype or subtype

### 3.3 Rigidity (Modal Instantiation)

#### Rigid Type

**Definition**: If instance possibly instantiates type, then necessarily instantiates it

```
Rigid(t) ↔ EndurantType(t) ∧ ∀x(◇(x::t) → □(x::t))
```

**Examples**:
- Person (if you're possibly a person, you're necessarily a person)
- Dog
- Computer
- Marriage (the relator kind)

**Implication**: Essential classification

#### Anti-Rigid Type

**Definition**: If instance possibly instantiates type, then possibly doesn't

```
AntiRigid(t) ↔ EndurantType(t) ∧ ∀x(◇(x::t) → ◇(¬x::t))
```

**Examples**:
- Student (can exist without being student)
- Employee
- Teenager
- Red Flower

**Implication**: Contingent classification

#### Semi-Rigid Type

**Definition**: Neither rigid nor anti-rigid

```
SemiRigid(t) ↔ EndurantType(t) ∧ ¬Rigid(t) ∧ ¬AntiRigid(t)
```

**Examples**:
- Music Artist (essential to bands, accidental to people)

**Key constraint**: Rigid/Semi-rigid cannot specialize Anti-rigid
- `¬∃x,y(Rigid(x) ∧ AntiRigid(y) ∧ x ⊑ y)`

### 3.4 Sortality (Identity Provision)

#### Kind

**Definition**: Provides uniform principles of individuation, identity, and persistence

**Characteristics**:
- Rigid
- Every endurant instantiates exactly one kind: `Endurant(x) → ∃!k(Kind(k) ∧ □(x::k))`
- Kinds are necessarily disjoint: `Kind(x) ∧ Kind(y) ∧ x≠y → □(¬∃z(z::x ∧ z::y))`

**Examples**:
- Person
- Dog
- Computer
- Car
- Headache
- Organization
- Marriage

**Axiom**: `Kind(k) → Rigid(k)`

**Sub-categorization**:
- ObjectKind (instances are Objects)
- CollectiveKind
- QuantityKind
- RelatorKind
- ModeKind
- QualityKind

#### Sortal

**Definition**: Type whose instances necessarily instantiate same kind

```
Sortal(t) ↔ EndurantType(t) ∧ ∃k(Kind(k) ∧ □(∀x(x::t → x::k)))
```

**Properties**:
- Every sortal specializes exactly one kind
- Sortals cannot specialize different kinds

**Categories**:

**SubKind**
- Rigid sortal that is not a kind
- Example: Man (subkind of Person), Hatchback Car (subkind of Car)

**Phase**
- Anti-rigid sortal with **intrinsic** contingent conditions
- Examples:
  - Teenager (phase of Person - intrinsic age)
  - Hemorrhagic Dengue Fever (phase of Dengue Fever)
  - Tenured Employment (phase of Employment)

**Role**
- Anti-rigid sortal with **relational** contingent conditions
- Examples:
  - Employee (role of Person in scope of Employment relator)
  - Husband (role of Person in scope of Marriage relator)
  - Customer

**SemiRigidSortal**
- Semi-rigid and sortal

#### Non-Sortal

**Definition**: `NonSortal(t) ↔ EndurantType(t) ∧ ¬Sortal(t)`

**Key property**: Instances can instantiate different kinds

**Constraint**: Non-sortal cannot specialize sortal

**Categories**:

**Category**
- Rigid non-sortal
- Defines essential properties for instances of multiple kinds
- Example: Physical Object (has mass + spatial extension - common to Person, Car, Bridge)

**Mixin**
- Semi-rigid non-sortal
- Example: Music Artist (essential to Band kind, accidental to Person kind)

**Phase Mixin**
- Anti-rigid non-sortal with intrinsic conditions
- Examples:
  - Living Animal (applies to Person, Dog, Horse)
  - Functional Device (applies to Computer, Watch, Espresso Machine)

**Role Mixin**
- Anti-rigid non-sortal with relational conditions
- Examples:
  - Customer (applies to Person and Organization)
  - Insured Legal Relator (applies to Employment and Enrollment)

### 3.5 Complete Type Taxonomy

**14 Leaf Categories** (LET):

| Type | Rigidity | Sortality | Identity | Examples |
|------|----------|-----------|----------|----------|
| **ObjectKind** | Rigid | Sortal | Provides | Person, Car |
| **CollectiveKind** | Rigid | Sortal | Provides | Forest, Team |
| **QuantityKind** | Rigid | Sortal | Provides | Water Portion |
| **RelatorKind** | Rigid | Sortal | Provides | Marriage |
| **ModeKind** | Rigid | Sortal | Provides | Headache |
| **QualityKind** | Rigid | Sortal | Provides | Color |
| **SubKind** | Rigid | Sortal | Inherits | Man, Woman |
| **Phase** | Anti-Rigid | Sortal | Inherits | Teenager, Child |
| **Role** | Anti-Rigid | Sortal | Inherits | Student, Employee |
| **SemiRigidSortal** | Semi-Rigid | Sortal | Inherits | - |
| **Category** | Rigid | Non-Sortal | None | Physical Object |
| **Mixin** | Semi-Rigid | Non-Sortal | None | Music Artist |
| **PhaseMixin** | Anti-Rigid | Non-Sortal | None | Living Thing |
| **RoleMixin** | Anti-Rigid | Non-Sortal | None | Customer |

**Theorem**: These 14 categories are:
- Pairwise disjoint
- Complete (every EndurantType is exactly one)

### 3.6 Higher-Order Types (Multi-Level Modeling)

**Second-Order Type**: Type whose instances are types

**Categorizes relation**:
```
categorizes(t₁,t₂) ↔ Type(t₁) ∧ ∀t₃(t₃::t₁ → t₃ < t₂)
```

**Powertype Pattern**:
- Second-order type (e.g., ConjugalRelationshipType)
- Base type (e.g., ConjugalRelationship)
- First-order types as instances (MonogamousMarriage, PolygamousMarriage)

**Example from paper**: Marriage concept evolution
- Base: ConjugalRelationship (what remains constant)
- Second-order: ConjugalRelationshipType
- Instances:
  - MonogamousHeterosexualMarriage
  - MonogamousSamesexMarriage
  - (future types can be added without changing base)

**Use case**: **Anticipated evolution**
- Foresee that types will change
- Introduce invariant structures to accommodate

---

## Relations & Dependencies

### 4.1 Fundamental Relations

#### Instantiation (`::`)

**Signature**: `Individual × Type → Boolean`

**Properties**:
- Connects individuals to types
- At most second-order
- Basis for classification

#### Specialization (`⊑`)

**Definition**: Necessary extensional inclusion

**Properties**:
- Quasi-reflexive
- Transitive
- Not antisymmetric (can have equivalent types)

#### Inherence

**Definition**: Existential dependence of moment to bearer

**Signature**: `Moment × (Type ∪ ConcreteIndividual) → Boolean`

**Properties**:
- Non-reflexive: `¬inheresIn(x,x)`
- Asymmetric: `inheresIn(x,y) → ¬inheresIn(y,x)`
- Anti-transitive: `inheresIn(x,y) ∧ inheresIn(y,z) → ¬inheresIn(x,z)`

**Non-migration principle**: `inheresIn(x,y) ∧ inheresIn(x,z) → y=z`

**Ultimate bearer**: Unique non-moment at end of inherence chain

#### Mediation

**Definition**: Connection between relator and entities it binds

```
mediates(x,y) ↔ Relator(x) ∧ Endurant(y) ∧ ∃z(quaIndividualOf(z,y) ∧ P(z,x))
```

**Theorem**: Every relator mediates at least two distinct individuals

**Examples**:
- Marriage mediates John and Mary
- Employment mediates Employee and Company
- Enrollment mediates Student and School

### 4.2 Mereology (Part-Whole)

**Axiomatization**: General Extensional Mereology

**Proper Part** (`PP`):
```
PP(x,y) ↔ P(x,y) ∧ ¬P(y,x)
```

**Overlap** (`O`):
```
O(x,y) ↔ ∃z(P(z,x) ∧ P(z,y))
```

**Properties**:
- Reflexive: `P(x,x)`
- Antisymmetric: `P(x,y) ∧ P(y,x) → x=y`
- Transitive: `P(x,y) ∧ P(y,z) → P(x,z)`
- Strong supplementation: `¬P(y,x) → ∃z(P(z,y) ∧ ¬O(z,x))`

**Functional Parthood** (`componentOf`):

**Definition**: Part + functional dependence

```
componentOf(x,x',y,y') ↔ x PP y ∧ ifd(x,x',y,y')
```

**Where**:
- `x` is individual part
- `x'` is type of part
- `y` is individual whole
- `y'` is type of whole
- `ifd` is individual functional dependence

**Key property**: **Not irrestrictively transitive**
- Transitivity holds only in specific scopes
- Defined by "special circumstances"

**Example**: Wooden Table
- Has componentOf relations to:
  - Right Front Leg (playing RightFrontLeg role)
  - Right Rear Leg
  - Left Front Leg
  - Left Rear Leg
  - Top Component

### 4.3 Existential Dependence

**General existential dependence**:
```
ed(x,y) ↔ □(ex(x) → ex(y))
```

**Existential independence**:
```
ind(x,y) ↔ ¬ed(x,y) ∧ ¬ed(y,x)
```

**Types**:

**Inherence** (moment to bearer):
- Special case of existential dependence
- Additional constraints (non-migration, anti-transitivity)

**External dependence** (to mereologically disjoint entity):
```
externallyDependent(x,y) ↔ ed(x,y) ∧ ∀z(inheresIn(x,z) → ind(y,z))
```

**Generic dependence** (to type, not specific individual):
- Example: Statue of clay generically depends on "Lump of Clay" type
- Not dependent on specific lump (can be replaced)

**Specific dependence** (to specific individual):
- Example: Boxing match specifically depends on specific punches
- Cannot be different punches

### 4.4 Characterization

**Definition**: Type is characterized by moment types that inhere in instances

```
characterization(t,m) → EndurantType(t) ∧ MomentType(m) ∧
  ∀x(x::t → ∃y(y::m ∧ inheresIn(y,x))) ∧
  ∀z(z::m → ∃!w(w::t ∧ inheresIn(z,w)))
```

**Example**: Flower characterized by FlowerColor
- Every flower has exactly one flower color quality
- Every flower color quality inheres in exactly one flower

### 4.5 Foundation

**Definition**: Externally dependent modes and relators are founded by unique events

```
foundedBy(x,y) → (ExternallyDependentMode(x) ∨ Relator(x)) ∧ Perdurant(y)
ExternallyDependentMode(x) → ∃!y(foundedBy(x,y))
```

**Example**: John-qua-husband founded by wedding event

**Definite description**: `foundationOf(x) = y ↔ foundedBy(x,y)`

---

## Change & Events

### 5.1 Who Can Change?

**Endurants**: YES
- Can qualitatively change while maintaining numerical identity
- Change constrained by Kind (identity principle)

**Perdurants**: NO
- Modally fragile
- No cross-world identity
- Cannot be different than what they are

### 5.2 Types of "Change"

#### Change IN (endurant qualitative change)

**Definition**: Same individual, different properties in different situations

**Example**: Flower color change
- Same flower individual
- Color quality inheres in flower (immutable)
- But hasValue relation to quale changes (Red → Brown)

**Mechanism**:
- Inherence is immutable (existential dependence)
- hasValue is generic dependence (mutable)

**Formal**:
```
World w₁: flower₁ --inheresIn-- colorQuality₁ --hasValue--> Red
World w₂: flower₁ --inheresIn-- colorQuality₁ --hasValue--> Brown
          (same flower, same quality, different value)
```

#### Change OF (perdurant variation)

**Definition**: Different temporal parts of event have different properties

**Example**: Man walking then running
- Not event changing
- Different temporal parts (WalkingEvent, RunningEvent)
- Each part is immutable
- Variation, not change

**Mechanism**:
- Jog mode (endurant) manifests as different events
- Each event is modally fragile snapshot
- Cumulative aggregation creates "life" of mode

#### Change of FOCUS (underlying endurant changes)

**Definition**: Endurant that event manifests changes

**Example**: Walker redirects destination
- Walk mode changes (new destination intention)
- Different walking perdurant manifested
- Subject of change is Walk (endurant), not walking event

### 5.3 Manifestation Theory

**Core principle**: Events are manifestations of dispositions

**Manifestation relation**:
```
manifests(x,y) → Endurant(x) ∧ Perdurant(y)
```

**Life of endurant**:
```
lifeOf(x,y) ↔ Perdurant(x) ∧ Endurant(y) ∧
  ∀z(O(z,x) ↔ (Perdurant(z) ∧ manifests(z,y)))
```

**Definition**: Mereological sum of all events that manifest the endurant

**Key insight**: Life is a **process** (special perdurant)
- Current life at each point in time
- Each manifestation creates new cumulative life
- Change *of* life, not change *in* life

**Example**: Jogging
- Jog (mode/endurant): intention + capabilities
- JoggingEvent (perdurant): direct manifestation
- JoggingProcess (perdurant): cumulative life of Jog
- Each new event creates new process (monotonic accumulation)

**Meeting relation** (temporal succession):
```
meet(x,y) → Perdurant(x) ∧ Perdurant(y)
```

If processes meet:
```
∀x,y,z(x::Jog ∧ y::JoggingProcess ∧ z::JoggingProcess ∧
       manifestedBy(x,y) ∧ manifestedBy(x,z) ∧ meet(y,z) →
  ∀w(w::JoggingEvent ∧ constitutedBy(y,w) → constitutedBy(z,w)))
```

All constituents of preceding process also constitute succeeding process.

### 5.4 Focus

**Definition**: Underlying endurant of which event is manifestation

**Example**: Walk mode is focus of walking perdurant

**Carving from scene**: Events carved out by having endurant as focus

**Key distinction**:
- Change in focus → different perdurant manifested
- Not event changing, but focus changing

### 5.5 Event Types

**From paper example**:

**JoggingEvent** (direct manifestation)
- Partitioned into:
  - JogState (homeomerous/stative)
  - JoggingLocomotion (dynamic/sequence)

**JoggingLocomotion** further partitioned:
- WalkWhileJogging (characterized by walking speed)
- RunWhileJogging (characterized by running speed)

**Key**: Events characterized by tropes (immutable properties), not qualities (variable tropes)

---

## Quality Structures

### 6.1 Quality Hierarchy

```
IntrinsicMoment
└── Quality (can project to value space)
    ├── SimpleQuality (bears nothing)
    └── ComplexQuality (bears simple qualities)
```

### 6.2 Quality Structures

**Definition**: Non-empty set associated with unique quality type

```
QualityStructure(x) ↔ ∃!t(QualityType(t) ∧ associatedWith(x,t))
QualityStructure(x) → Set(x) ∧ x ≠ ∅
```

**Types**:

**Quality Dimension** (1D):
- Associated with SimpleQualityType
- Examples: height scale (≅ ℝ⁺), weight scale, temperature scale

**Quality Domain** (multi-dimensional):
- Associated with ComplexQualityType
- Cartesian product of quality dimensions
- Examples: color spindle (hue × saturation × brightness), taste tetrahedron

**Formal**:
```
QualityDomain(x) ∧ associatedWith(x,t) →
  ∃y₁,...,yₙ,z₁,...,zₙ(
    (x ⊆ y₁ × ... × yₙ) ∧
    ⋀ᵢ₌₁ⁿ(associatedWith(yᵢ,zᵢ) ∧ characterization(t,zᵢ)) ∧
    ∀w(characterization(t,w) → ⋁ᵢ₌₁ⁿ(w = zᵢ))
  )
```

Domain is subset of Cartesian product of dimensions corresponding to characterizing quality types.

### 6.3 Quale

**Definition**: Member of quality structure

```
Quale(x) ↔ ∃!y(QualityStructure(y) ∧ x ∈ y)
```

**Examples**:
- Red (quale in ColorSpace)
- 1.8m (quale in HeightDimension)
- 70kg (quale in WeightDimension)

**Key**: Quale is abstract individual, not quality instance

### 6.4 hasValue Relation

**Signature**: `Quality × Quale → Boolean`

**Properties**:
- Functional: `Quality(x) → ∃!y(hasValue(x,y))`
- Constraint: `hasValue(x,y) → ∃t,s(x::t ∧ associatedWith(s,t) ∧ y ∈ s)`

**Mutability**: Generic dependence (can change across worlds)

**Example**:
```
World w₁: flowerColor₁ --hasValue--> Red
World w₂: flowerColor₁ --hasValue--> Brown
```

### 6.5 Simple vs Complex Qualities

**Simple Quality**: Bears nothing
```
SimpleQuality(x) ≝ Quality(x) ∧ ¬∃y(inheresIn(y,x))
```

**Complex Quality**: Bears simple qualities
```
ComplexQuality(x) ≝ Quality(x) ∧ ¬SimpleQuality(x)
ComplexQuality(x) → ∀y(inheresIn(y,x) → SimpleQuality(y))
```

**Example**: Color (complex)
- Hue (simple quality inhering in color)
- Saturation (simple quality)
- Brightness (simple quality)

**No duplicate types**:
```
ComplexQuality(x) ∧ y::Y ∧ z::Z ∧ inheresIn(y,x) ∧ inheresIn(z,x) ∧ Y=Z → y=z
```

Complex quality cannot have two qualities of same type.

### 6.6 Metric Spaces

**Distance function** (ternary relation):
```
d(x,y,r) → Quale(x) ∧ Quale(y) ∧ ∃z(memberOf(x,z) ∧ memberOf(y,z))
Quale(x) ∧ Quale(y) → ∃!r(d(x,y,r))
```

**Properties**:
- Identity: `x=y ∧ d(x,y,r) → r=0`
- Symmetry: `d(x,y,r) → d(y,x,r)`
- Triangle inequality: `d(x,y,r₀) ∧ d(y,z,r₁) ∧ d(x,z,r₂) ∧ r₀+r₁=s → s≥r₂`

**Quality Region**: Convex subset of quality domain
- All points between two points in region are also in region

### 6.7 Subtype Constraints on Quality Structures

**Specialization constraint**:
```
associatedWith(s,t) ∧ associatedWith(s',t') ∧ t' < t → s' ⊂ s
```

If quality type specializes another, its structure is proper subset.

**Example**:
- Color associated with ColorSpace
- SkinColor < Color
- SkinColor associated with SkinColorSpace ⊂ ColorSpace

---

## Constitution & Grounding

### 7.1 Constitution vs Identity

**Critical distinction**: Constitution ≠ Identity

**Constitution**: Relation between things of:
- Same ontological category (both endurants or both perdurants)
- Different Kinds
- Asymmetric relationship

**Example**: Statue constituted by clay
- Both are endurants
- Statue (kind: Sculpture) ≠ Clay (kind: Lump)
- Different identity principles
- Different essential properties
- Different modal properties

### 7.2 Constitution Axioms

**Same category**:
```
constitutedBy(x,y) → ((Endurant(x) ↔ Endurant(y)) ∧
                      (Perdurant(x) ↔ Perdurant(y)))
```

**Different kinds**:
```
constitutedBy(x,y) ∧ x::x' ∧ y::y' ∧ Kind(x') ∧ Kind(y') → x' ≠ y'
```

**Non-reflexive**: `¬constitutedBy(x,x)`

**Asymmetric**: `constitutedBy(x,y) → ¬constitutedBy(y,x)`

**For events** (specific dependence):
```
∀x,y(Perdurant(x) ∧ constitutedBy(x,y) → □(ex(x) → constitutedBy(x,y)))
```

All constituents of perdurant are necessary constituents.

### 7.3 Generic Constitutional Dependence (GCD)

**Definition**: Type generically depends on constituent type

```
GCD(x',y') ↔ ∀x(x::x' → ∃y(y::y' ∧ constitutedBy(x,y)))
```

**Example**: Statue of Clay
- Every statue of clay must be constituted by some lump of clay
- But not necessarily the same lump across worlds

**Type-level constitution**:
```
Constitution(x,x',y,y') ↔ x::x' ∧ y::y' ∧ GCD(x',y') ∧ constitutedBy(x,y)
```

### 7.4 Grounding

**Key insight**: Constitution relies on **grounding**

**Grounding characteristics**:
- Asymmetric
- Grounds explanation of property derivation
- Constituent grounds constituted

**Property derivation**:
- Spatial location of statue derived from clay
- Weight, volume, color, chemical structure derived
- **NOT** vice versa

**Special circumstances** (Baker 2007):
- Necessary and sufficient conditions for constitution
- Example: For clay to constitute statue, intentional act of sculptor required

**Why The Beatles grounded in John/Paul/George/Ringo**:
- Not the reverse
- Collective derives properties from members

### 7.5 Constitution and Functional Parthood

**Similarity**: Both require "special circumstances"

**ComponentOf** (functional parthood):
- Part + functional dependence
- Special circumstances define functional role
- Not irrestrictively transitive (only in scopes)

**Constitution**:
- Constituent + grounding
- Special circumstances enable constitution
- Not irrestrictively transitive

**Example of non-transitivity**:
- Tissue constitutes Paul McCartney
- Paul McCartney participates in The Beatles
- Tissue does NOT constitute The Beatles

**Hypothesis**: Like parthood, constitution is family of relations
- Each with additional axioms
- Extending minimal common core

### 7.6 Dependence Asymmetry

**Generic dependence**:
- Wooden Table generically depends on Wooden Table Components
- Table can exist with different components

**Specific dependence**:
- This Boxing Match specifically depends on these punches
- Perdurants have necessary constituents

**From constituent perspective**:
- Wood Portion can exist without constituting table
- Contingent constitution

**From constituted perspective**:
- Wooden Table Component must be constituted by some wood portion
- Generic constitutional dependence

### 7.7 Incomplete Theory

**Acknowledgment**: Full theory of constitution awaits full theory of grounding

**Current status**: Minimal axiomatization
- Same category
- Different kinds
- Asymmetric
- Non-reflexive

**Future work**:
- Complete grounding theory
- Property derivation rules
- Transitivity scopes
- Family of constitution relations

---

## Formal Axiomatization

### 8.1 Logical Framework

**Logic**: First-Order Modal Logic **QS5**
- Quantified modal logic
- S5 modal system (accessibility relation is equivalence)
- Barcan formula and converse

**Modalities**:
- Necessity: `□φ` (phi is true in all accessible worlds)
- Possibility: `◇φ` (phi is true in some accessible world)

**Domain**: Fixed across possible worlds
- Possibilistic view
- Domain includes all possibilia

**Conventions**:
- Universal quantifier and necessity dropped when scope is full formula
- Definitions marked with `≝`
- Axioms: `(aₙ)`
- Theorems: `(tₙ)`
- Definitions: `(dₙ)`

### 8.2 Core Axioms

#### Types and Individuals

```
a1: Type(x) ↔ ◇(∃y(y::x))
a2: Individual(x) ↔ □(¬∃y(y::x))
a3: x::y → (Type(x) ∨ Individual(x))
a4: ¬∃x,y,z(Type(x) ∧ x::y ∧ y::z)

t1: Individual(x) ∨ Type(x)
t2: ¬∃x(Individual(x) ∧ Type(x))
```

#### Specialization

```
a5: x ⊑ y ↔ Type(x) ∧ Type(y) ∧ □(∀z(z::x → z::y))

d1: x < y ≝ x ⊑ y ∧ ¬(y ⊑ x)

t3: x ⊑ y → (x ⊑ x ∧ y ⊑ y)
t4: x ⊑ y ∧ y ⊑ z → x ⊑ z

a6: ∀t₁,t₂,x((x::t₁ ∧ x::t₂ ∧ ¬(t₁ ⊑ t₂) ∧ ¬(t₂ ⊑ t₁)) →
    (∃t₃(t₁ ⊑ t₃ ∧ t₂ ⊑ t₃ ∧ x::t₃) ∨
     ∃t₃(t₃ ⊑ t₁ ∧ t₃ ⊑ t₂ ∧ x::t₃)))
```

#### Concrete and Abstract

```
a7: ConcreteIndividual(x) → Individual(x)
a8: AbstractIndividual(x) → Individual(x)
a9: ConcreteIndividual(x) → ¬AbstractIndividual(x)
a10: Individual(x) ↔ ConcreteIndividual(x) ∨ AbstractIndividual(x)

a11: Endurant(x) → ConcreteIndividual(x)
a12: Perdurant(x) → ConcreteIndividual(x)
a13: Endurant(x) → ¬Perdurant(x)
a14: ConcreteIndividual(x) ↔ Endurant(x) ∨ Perdurant(x)
```

### 8.3 Rigidity Axioms

```
a18: Rigid(t) ↔ EndurantType(t) ∧ ∀x(◇(x::t) → □(x::t))

a19: AntiRigid(t) ↔ EndurantType(t) ∧ ∀x(◇(x::t) → ◇(¬x::t))

a20: SemiRigid(t) ↔ EndurantType(t) ∧ ¬Rigid(t) ∧ ¬AntiRigid(t)

t5: EndurantType(t) ↔ Rigid(t) ∨ AntiRigid(t) ∨ SemiRigid(t)

t6: ¬∃x((Rigid(x) ∧ AntiRigid(x)) ∨
         (Rigid(x) ∧ SemiRigid(x)) ∨
         (SemiRigid(x) ∧ AntiRigid(x)))

t7: ¬∃x,y(Rigid(x) ∧ AntiRigid(y) ∧ x ⊑ y)
t8: ¬∃x,y(SemiRigid(x) ∧ AntiRigid(y) ∧ x ⊑ y)
```

### 8.4 Sortality Axioms

```
a21: Endurant(x) → ∃k(Kind(k) ∧ □(x::k))

a22: Kind(k) ∧ x::k → ¬◇(∃z(Kind(z) ∧ x::z ∧ z≠k))

a23: Sortal(t) ↔ EndurantType(t) ∧ ∃k(Kind(k) ∧ □(∀x(x::t → x::k)))

a24: NonSortal(t) ↔ EndurantType(t) ∧ ¬Sortal(t)

t9: Kind(k) → Rigid(k)
t10: Kind(x) ∧ Kind(y) ∧ x≠y → □(¬∃z(z::x ∧ z::y))
t11: Kind(x) ∧ Kind(y) ∧ x≠y → (¬(x ⊑ y) ∧ ¬(y ⊑ x))
t12: Kind(t) → Sortal(t)
t13: Sortal(x) → ∃k(Kind(k) ∧ x ⊑ k)
t14: ¬∃x,y,z(Kind(y) ∧ Kind(z) ∧ y≠z ∧ x ⊑ y ∧ x ⊑ z)
t15: ¬∃x,y(NonSortal(x) ∧ Sortal(y) ∧ x ⊑ y)
```

### 8.5 Endurant Taxonomy Axioms

```
a34: Substantial(x) ∨ Moment(x) ↔ Endurant(x)
a35: ¬∃x(Substantial(x) ∧ Moment(x))

a36: Object(x) ∨ Collective(x) ∨ Quantity(x) ↔ Substantial(x)
a37: ¬∃x(Object(x) ∧ Collective(x))
a38: ¬∃x(Object(x) ∧ Quantity(x))
a39: ¬∃x(Collective(x) ∧ Quantity(x))

a40: Relator(x) ∨ IntrinsicMoment(x) ↔ Moment(x)
a41: ¬∃x(Relator(x) ∧ IntrinsicMoment(x))

a42: Mode(x) ∨ Quality(x) ↔ IntrinsicMoment(x)
a43: ¬∃x(Mode(x) ∧ Quality(x))
```

### 8.6 Mereology Axioms

```
a47: P(x,x)                                    [reflexivity]
a48: P(x,y) ∧ P(y,x) → x=y                    [anti-symmetry]
a49: P(x,y) ∧ P(y,z) → P(x,z)                 [transitivity]
a50: O(x,y) ↔ ∃z(P(z,x) ∧ P(z,y))            [overlap]
a51: ¬P(y,x) → ∃z(P(z,y) ∧ ¬O(z,x))          [strong supplementation]
a52: PP(x,y) ↔ P(x,y) ∧ ¬P(y,x)              [proper part]
```

### 8.7 Inherence Axioms

```
a65: inheresIn(x,y) → ed(x,y)

a66: inheresIn(x,y) → Moment(x) ∧ (Type(y) ∨ ConcreteIndividual(y))

a67: inheresIn(x,y) ∧ inheresIn(x,z) → y=z   [non-migration]

d2: momentOf(m,x) ≝ inheresIn(m,x) ∨ ∃y(inheresIn(m,y) ∧ momentOf(y,x))

d3: ultimateBearerOf(b,m) ≝ ¬Moment(b) ∧ momentOf(m,b)

a68: Moment(m) → ∃!b(ultimateBearerOf(b,m))

t28: ¬inheresIn(x,x)                          [non-reflexive]
t29: inheresIn(x,y) → ¬inheresIn(y,x)        [asymmetric]
t30: inheresIn(x,y) ∧ inheresIn(y,z) → ¬inheresIn(x,z)  [anti-transitive]
```

### 8.8 Relator Axioms

```
a69: externallyDependent(x,y) ↔ ed(x,y) ∧ ∀z(inheresIn(x,z) → ind(y,z))

a70: ExternallyDependentMode(x) ↔ Mode(x) ∧ ∃y(externallyDependent(x,y))

a71: foundedBy(x,y) → (ExternallyDependentMode(x) ∨ Relator(x)) ∧ Perdurant(y)

a72: ExternallyDependentMode(x) → ∃!y(foundedBy(x,y))

a73: quaIndividualOf(x,y) ↔ ∀z(O(z,x) ↔
     (ExternallyDependentMode(z) ∧ inheresIn(z,y) ∧
      foundationOf(z) = foundationOf(x)))

a74: QuaIndividual(x) ↔ ∃y(quaIndividualOf(x,y))

a75: QuaIndividual(x) → ExternallyDependentMode(x)

a76: quaIndividualOf(x,y) ∧ quaIndividualOf(x,y') → y=y'

a77: Relator(x) → ∃!y(foundedBy(x,y))

a79: Relator(x) ↔ ∃y(PP(y,x)) ∧
     ∀y,z((PP(y,x) ∧ PP(z,x)) →
       (QuaIndividual(y) ∧ QuaIndividual(z) ∧
        foundationOf(y) = foundationOf(z) ∧
        ed(y,z) ∧ ed(z,y))) ∧
     ∀y,z((PP(y,x) ∧ QuaIndividual(z) ∧
           foundationOf(y) = foundationOf(z) ∧
           ed(y,z) ∧ ed(z,y)) → PP(z,x))

a80: mediates(x,y) ↔ Relator(x) ∧ Endurant(y) ∧ ∃z(quaIndividualOf(z,y) ∧ P(z,x))

t32: Relator(x) → ∃x',x'',y',y''(quaIndividualOf(x',y') ∧
                                  quaIndividualOf(x'',y''))

t33: Relator(x) → ∃y,z(y≠z ∧ mediates(x,y) ∧ mediates(x,z))
```

### 8.9 Quality Axioms

```
a83: Quale(x) → AbstractIndividual(x)
a84: Set(x) → AbstractIndividual(x)
a85: ¬∃x(Quale(x) ∧ Set(x))

d5: QualityStructure(x) ≝ ∃!t(QualityType(t) ∧ associatedWith(x,t))

a86: QualityStructure(x) → Set(x) ∧ x≠∅

a87: Quale(x) ↔ ∃!y(QualityStructure(y) ∧ x ∈ y)

a88: QualityStructure(x) ↔ QualityDomain(x) ∨ QualityDimension(x)

a89: QualityDomain(x) → ¬QualityDimension(x)

a90: associatedWith(s,t) ∧ associatedWith(s',t') ∧ t' < t → s' ⊂ s

a91: QualityType(t) ↔ IntrinsicMomentType(t) ∧
                      ∃!x(QualityStructure(x) ∧ associatedWith(x,t))

a92: hasValue(x,y) → Quality(x) ∧ Quale(y)

a93: Quality(x) → ∃!y(hasValue(x,y))

a94: hasValue(x,y) → ∃t,s(x::t ∧ associatedWith(s,t) ∧ y ∈ s)

a95: associatedWith(x,y) → (QualityDimension(x) ↔ SimpleQualityType(y))

a96: associatedWith(x,y) → (QualityDomain(x) ↔ ComplexQualityType(y))

a97: ComplexQuality(x) ∧ y::Y ∧ z::Z ∧
     inheresIn(y,x) ∧ inheresIn(z,x) ∧ Y=Z → y=z

a98: ComplexQuality(x) → ∀y(inheresIn(y,x) → SimpleQuality(y))

a99: QualityDomain(x) ∧ associatedWith(x,t) →
     ∃y₁,...,yₙ,z₁,...,zₙ((x ⊆ y₁×...×yₙ) ∧
       ⋀ᵢ₌₁ⁿ(associatedWith(yᵢ,zᵢ) ∧ characterization(t,zᵢ)) ∧
       ∀w(characterization(t,w) → ⋁ᵢ₌₁ⁿ(w = zᵢ)))
```

### 8.10 Constitution Axioms

```
a56: constitutedBy(x,y) → ((Endurant(x) ↔ Endurant(y)) ∧
                           (Perdurant(x) ↔ Perdurant(y)))

a57: constitutedBy(x,y) ∧ x::x' ∧ y::y' ∧ Kind(x') ∧ Kind(y') → x'≠y'

t27: ¬constitutedBy(x,x)

a58: GCD(x',y') ↔ ∀x(x::x' → ∃y(y::y' ∧ constitutedBy(x,y)))

a59: Constitution(x,x',y,y') ↔ x::x' ∧ y::y' ∧ GCD(x',y') ∧ constitutedBy(x,y)

a60: ∀x,y(Perdurant(x) ∧ constitutedBy(x,y) → □(ex(x) → constitutedBy(x,y)))

a61: constitutedBy(x,y) → ¬constitutedBy(y,x)
```

### 8.11 Event Axioms

```
a102: manifests(x,y) → Endurant(x) ∧ Perdurant(y)

a103: lifeOf(x,y) ↔ Perdurant(x) ∧ Endurant(y) ∧
                    ∀z(O(z,x) ↔ (Perdurant(z) ∧ manifests(z,y)))

a104: meet(x,y) → Perdurant(x) ∧ Perdurant(y)
```

---

## OntoUML Modeling Language

### 9.1 Overview

**OntoUML**: Ontology-driven conceptual modeling language that reflects UFO micro-theories

**Purpose**:
- Makes UFO categories explicit in models
- Enables automated validation
- Supports semantic interoperability

**Philosophy**: Language as theory reflection
- Stereotypes correspond to UFO meta-types
- Constraints embedded in language
- Anti-patterns automatically detected

### 9.2 Stereotypes

#### Endurant Types

| Stereotype | UFO Category | Rigidity | Sortality |
|------------|--------------|----------|-----------|
| `«kind»` | Kind | Rigid | Sortal |
| `«subkind»` | SubKind | Rigid | Sortal |
| `«phase»` | Phase | Anti-Rigid | Sortal |
| `«role»` | Role | Anti-Rigid | Sortal |
| `«category»` | Category | Rigid | Non-Sortal |
| `«mixin»` | Mixin | Semi-Rigid | Non-Sortal |
| `«phaseMixin»` | PhaseMixin | Anti-Rigid | Non-Sortal |
| `«roleMixin»` | RoleMixin | Anti-Rigid | Non-Sortal |

#### Moment Types

| Stereotype | UFO Category |
|------------|--------------|
| `«quality»` | QualityKind |
| `«mode»` | ModeKind |
| `«relator»` | RelatorKind |

#### Substantial Types

| Stereotype | UFO Category |
|------------|--------------|
| `«quantity»` | QuantityKind |
| `«collective»` | CollectiveKind |

#### Event Types

| Stereotype | UFO-B Category |
|------------|----------------|
| `«event»` | EventType |

#### Relations

| Stereotype | UFO Relation |
|------------|--------------|
| `«material»` | Material relation (derived from relator) |
| `«mediation»` | Mediation (relator to relata) |
| `«characterization»` | Characterization (type to moment type) |
| `«componentOf»` | Functional parthood |
| `«instantiation»` | Higher-order instantiation |

### 9.3 Modeling Patterns

#### Relator Pattern

**Purpose**: Reify relationships

**Structure**:
```
PersonKind ---[mediation]---> MarriageRelator <---[mediation]--- PersonKind
     ↑                                                                 ↑
     |                                                                 |
 HusbandRole                                                       WifeRole
```

**Example from paper**: Marriage
- Marriage is `«relator»`
- Mediates Person instances
- Husband and Wife are `«role»`s of Person

#### Material Relation Pattern

**Purpose**: Derived relation from relator

**Rule**: Material relation is shorthand for:
1. Relator existence
2. Mediation to both relata

**Example**: "is married to"
```
married_to(x,y) ≝ ∃r(Marriage(r) ∧ mediates(r,x) ∧ mediates(r,y))
```

#### Phase Partition Pattern

**Purpose**: Mutually exclusive life stages

**Structure**:
```
PersonKind
    ↑
    |------ ChildPhase
    |------ TeenagerPhase
    |------ AdultPhase
```

**Constraints**:
- Disjoint phases
- Complete coverage (every instance in some phase)

#### Role Pattern

**Purpose**: Contextual classification

**Structure**:
```
PersonKind ---[mediation]---> EnrollmentRelator <---[mediation]--- SchoolKind
     ↑
     |
 StudentRole
```

**Constraint**: Role instantiation → relator exists

#### Powertype Pattern

**Purpose**: Multi-level modeling

**Structure**:
```
ConjugalRelationshipType «type»
        |
        |«instantiation»
        ↓
MonogamousMarriage «subkind» ⊑ ConjugalRelationship «kind»
```

**Constraints**:
- All instances of second-order type specialize base type
- Compatible spouse types specified

### 9.4 Visual Notation

**Class boxes**:
```
┌─────────────────────┐
│ «kind»              │
│ Person              │
└─────────────────────┘
```

**Generalization** (hollow triangle):
```
PersonKind ◁───── ManSubKind
```

**Association**:
```
PersonKind ────────── OrganizationKind
```

**Mediation** (filled circle):
```
PersonKind ●──────── EmploymentRelator
```

**Parthood** (filled diamond):
```
TableKind ♦──────── LegComponent
```

**Exclusive parthood** (black diamond):
```
TableKind ♦──────── LegComponent
          (each leg part of exactly one table)
```

### 9.5 Tooling Infrastructure

#### OntoUML as a Service (OaaS)

**Architecture**:
- Microservice-based
- HTTP + JSON communication
- Decoupled services and tools

**Components**:

1. **ontouml-schema**: JSON Schema specification
2. **ontouml-js**: TypeScript manipulation library
3. **ontouml-server**: HTTP server with model intelligence services
4. **ontouml-vp-plugin**: Visual Paradigm integration

**Model Intelligence Services**:
- Validation
- Anti-pattern detection
- Instance generation (consistency checking)
- Verbalization (natural language)
- Transformation to other languages

#### Anti-Pattern Detection

**Common anti-patterns**:

**Role/Phase confusion**:
- Bad: Student as `«phase»`
- Good: Student as `«role»` (relational condition: enrollment)

**Identity/Constitution conflation**:
- Bad: Statue and Clay as same entity
- Good: Statue constituted by Clay (different kinds)

**Missing relator**:
- Bad: Direct material relation for employment
- Good: Employment relator mediating Employee and Organization

**Rigid/Anti-rigid violation**:
- Bad: `«kind»` specializing `«role»`
- Good: Respect specialization constraints

#### Instance Generation

**Purpose**: Check model consistency

**Method**: Automated theorem proving
- Generate models satisfying axioms
- Visualize instances across possible worlds
- Detect unsatisfiable constraints

**Example output** (from paper):
```
World w₁:
  Object0::WoodPortion

World w₂:
  Object0::WoodPortion, Object0::WoodenComponentConstituent
  Object1::WoodenTableComponent, Object1::TableTopComponent
  constitutedBy(Object1, Object0)
```

Shows wood portion existing unconstituted in w₁, then constituting table component in w₂.

### 9.6 OntoUML Examples from Paper

All examples in Section 3 use OntoUML diagrams:

1. **Wooden Table** (composition/constitution)
2. **School** (roles and relators)
3. **Flower** (property change via qualities)
4. **Jogging** (event change and manifestation)
5. **Redirected Walk** (focus change)
6. **Marriage** (concept evolution with powertypes)

Each includes:
- Visual OntoUML diagram
- Formal axiomatization
- Generated instances across worlds

---

## Applications & Impact

### 10.1 Domain Applications (50+ domains)

#### Business & Enterprise

**Business Process Modeling**:
- BPMN ontological analysis
- Discrete event simulation
- Process mining integration

**Enterprise Architecture**:
- ArchiMate reengineering
- TOGAF alignment
- DEMO integration

**Accounting**:
- REA ontology formalization
- Financial reporting standards
- Budgetary processes

**Services**:
- Service contracts
- Value propositions
- Service offerings

#### Science & Engineering

**Geology**: Geomodeling, weathering processes

**Biodiversity**: Species classification, ecological relationships

**Bioinformatics**: ECG data, urinary profiles

**Agriculture**: Grain production decision support

**Engineering**: Railway systems, telecommunication networks

#### Legal & Government

**Law**:
- Fundamental rights
- Criminal liability
- Contract specification (Symboleo language)

**E-Government**:
- Public expenditure
- Normative acts
- Transparency ontology

#### Healthcare

**Treatment**: Clinical processes

**Emergency Management**: Disaster response

**Mulsemedia**: Multi-sensory systems

#### Technology & Software

**Software Engineering**:
- Requirements engineering
- Software anomalies and risks
- Quality management
- Programming language ontologies

**Security**:
- Information security incidents
- Safety in aviation
- Risk modeling

**Smart Contracts**: Blockchain applications

#### Social & Economic

**Trust**: Multi-dimensional trust modeling

**Money**: Currency and virtual currencies

**Value**: Economic exchanges, competition

**Game Theory**: Strategic interaction

**Tourism**: Alpine regions (AlpineBits)

### 10.2 Language Analysis

UFO used to analyze/reengineer:

- **UML**: Ontological profile
- **BPMN**: Process modeling semantics
- **ArchiMate**: Enterprise architecture
- **ARIS**: Business process modeling
- **Tropos / i***: Goal-oriented requirements
- **RM-ODP**: Reference model
- **ISO/IEC 24744**: Software engineering standards
- **ITU-T G.805**: Telecommunication networks

### 10.3 Empirical Validation

**Verdonck & Gailly (2016)** survey:
- UFO is **second-most used** foundational ontology
- **Fastest adoption rate** among foundational ontologies
- OntoUML among most used languages (with UML, ER, OWL, BPMN)

**Verdonck et al. (2019)** experiment:
- 100 participants
- Two countries
- **OntoUML significantly improves model quality vs EER**
- **No additional modeling effort required**

**Model repository**:
- Dozens of OntoUML models publicly available
- http://purl.org/krdb-core/model-repository/

### 10.4 Community Impact

**Publications**: 300+ papers using UFO/OntoUML

**Tool adoption**: Visual Paradigm plugin, web-based editors

**Education**: Taught in universities worldwide

**Industry**: Used in banking, government, healthcare, telecommunications

**Standards influence**: Informing ISO, W3C, OMG standards

---

## Comparison with Other Ontologies

### 11.1 UFO vs BWW (Bunge-Wand-Weber)

**BWW Origins**: Based on Mario Bunge's physics-oriented ontology

**Key Differences**:

| Aspect | BWW | UFO |
|--------|-----|-----|
| **Properties** | Only substantials have properties | Moments are first-class entities |
| **Relationships** | Disavows reified relationships | Relators as truthmakers |
| **Purpose** | Physics/general science | Conceptual modeling |
| **Predictions** | Conflicts with modeler intuitions | Aligns with practice |

**Why UFO emerged**: BWW predictions conflicted with:
- Jackendoff's semantic structures
- Practitioner evidence (Hitchman 2003)
- Need for weak entities, relationship attributes

### 11.2 UFO vs DOLCE

**DOLCE**: Descriptive Ontology for Linguistic and Cognitive Engineering

**Similarities**:
- Both descriptive (not revisionary)
- Cognitive/linguistic motivation
- 3D ontology (endurants vs perdurants)
- Trope-based

**Differences**:

| Aspect | DOLCE | UFO |
|--------|-------|-----|
| **Scope** | Ontology of particulars only | Includes universals/types |
| **Type theory** | No systematic type theory | Fine-grained (14 meta-types) |
| **Roles** | Limited role theory | Comprehensive role theory |
| **Relators** | No relational qualities | Relators + qua individuals |
| **Evolution** | Static | Actively developed |

**Historical**: UFO initially attempted to unify DOLCE and GFO

### 11.3 UFO vs GFO (General Formal Ontology)

**GFO**: Developed in Leipzig

**Similarities**:
- Four-category ontology
- Philosophical rigor
- German philosophical tradition

**Differences**:

| Aspect | GFO | UFO |
|--------|-----|-----|
| **Type distinctions** | No Kind/Role/Phase distinctions | Fine-grained type taxonomy |
| **Relations** | Subject to Bradley's Regress | Relators avoid regress |
| **Models** | Requires infinite models | Finite models possible |
| **Applications** | Medical domain focused | Multi-domain |

**Why UFO diverged**: GFO's relation theory incompatible with conceptual modeling needs

### 11.4 UFO vs BFO (Basic Formal Ontology)

**BFO**: Widely used in biomedicine

**Similarities**:
- Endurant/Perdurant distinction (Continuant/Occurrent in BFO)
- Realist stance
- Formal rigor

**Differences**:

| Aspect | BFO | UFO |
|--------|-----|-----|
| **Domain** | Natural science (biology focus) | Conceptual modeling (all domains) |
| **Social entities** | Limited | UFO-C comprehensive |
| **Type theory** | Basic | Sophisticated (rigidity, sortality) |
| **Relators** | No reified relationships | Central feature |
| **Qualities** | Quality/Realizable distinction | Quality/Mode/Disposition hierarchy |

### 11.5 UFO vs OntoClean

**OntoClean**: Methodology using meta-properties (Guarino & Welty)

**Relationship**: UFO incorporates and extends OntoClean

**UFO additions**:
- Comprehensive axiomatization
- Additional meta-properties (sortality)
- Complete type taxonomy (14 vs 4)
- Relator theory
- Event theory integration

**OntoClean meta-properties in UFO**:
- Rigidity → UFO Rigid/Anti-Rigid/Semi-Rigid
- Identity → UFO Kind/Sortal distinction
- Unity → UFO Object/Collective/Quantity
- Dependence → UFO Substantial/Moment

### 11.6 Unique UFO Contributions

1. **Relators**: Reified relationships as dependent entities
2. **Fine-grained type theory**: 14 meta-types vs 3-4 in others
3. **Qua individuals**: Solve participation problem
4. **Multi-level modeling**: Formal powertype theory
5. **Practical validation**: Empirically tested in modeling experiments
6. **Tooling**: OntoUML + OaaS infrastructure
7. **Breadth**: 50+ domains vs domain-specific ontologies

---

## Advanced Topics

### 12.1 Bradley's Regress and Relators

**Bradley's Regress**: Classic problem in metaphysics

**Problem**:
1. If relationship R holds between a and b
2. What connects a to R?
3. Need meta-relationship R' connecting a to R
4. What connects a to R'?
5. Infinite regress...

**UFO Solution via Relators**:

**Step 1**: Relationship grounded in relator (moment)
```
John ←[inheres]─ John-qua-husband ─[part-of]→ Marriage ←[part-of]─ Mary-qua-wife ─[inheres]→ Mary
```

**Step 2**: Inherence is primitive (no further grounding needed)
- Inherence is existential dependence (fundamental)
- Non-migratory, anti-transitive
- Terminates regress

**Key insight**: Material relation is **derived**, not primitive
```
married_to(John, Mary) ≝ ∃m(Marriage(m) ∧ mediates(m,John) ∧ mediates(m,Mary))
```

### 12.2 Modal Fragility of Events

**Thesis**: Events cannot be different than what they are

**Formal**: No cross-world identity for perdurants

**Implications**:

1. **No counterfactuals**: "If WWII had lasted longer" doesn't reference same event
2. **All parts necessary**: Boxing match necessarily has those exact punches
3. **No property change**: Can't have "same event with different properties"

**Contrast with endurants**:
- Person can be different (different hair, job, location)
- Maintains identity across worlds
- Essential vs accidental properties

**Why modally fragile**:
- Events are **manifestations** of dispositions
- Disposition is endurant (can have modal properties)
- But event is "snapshot" of manifestation
- Different manifestation = different event

### 12.3 Grounding Theory (Incomplete)

**Current status**: UFO acknowledges need for grounding theory but doesn't fully formalize

**Why needed**:

1. **Constitution asymmetry**: Why clay grounds statue, not vice versa
2. **Property derivation**: Which properties flow from constituent to constituted
3. **Special circumstances**: What enables constitution relation

**Partial account**:

**Generic Constitutional Dependence (GCD)**:
- Captures that statues depend on material
- But material doesn't depend on statues

**Asymmetry axiom**:
```
constitutedBy(x,y) → ¬constitutedBy(y,x)
```

**Property derivation examples** (informal):
- Physical endurants: spatial location, mass, volume inherited
- Events: temporal properties constrained
- But: requires systematic theory

**Future work**: Full grounding theory to complete constitution theory

### 12.4 Weak Truthmaking

**Problem**: How do relators serve as truthmakers for material relations?

**Guarino et al. (2019)**: Weak Truthmaking proposal

**Idea**:
- Strong truthmaking: truth supervenes on being
- Weak truthmaking: grounding relation between facts

**Application to relators**:
```
Fact: married_to(John, Mary)
Truthmaker: Marriage relator m
Grounding: Fact grounded in existence and mediation of m
```

**Advantages**:
- Explains derived nature of material relations
- Connects to broader metaphysics
- Allows relationship properties (moments of relators)

### 12.5 Conceptual Spaces Integration

**Gärdenfors (2004)**: Conceptual Spaces theory

**UFO connection**: Quality structures as conceptual spaces

**Integral dimensions**:
- Cannot vary independently
- Example: Hue-Saturation-Brightness in color

**UFO formalization**:
```
QualityDomain(ColorSpace) ↔
  ColorSpace ⊆ HueDimension × SaturationDimension × BrightnessDimension
```

**Distance metric**:
- Conceptual distance = metric on quality structure
- Triangle inequality
- Similarity judgments

**Regions**:
- Convex regions = natural categories
- Example: "Red" region in color spindle

### 12.6 Multi-Level Theory (MLT)

**Carvalho & Almeida (2018)**: Multi-Level Theory integrated with UFO

**Key concepts**:

**Categorization**:
```
categorizes(t₁,t₂) ↔ Type(t₁) ∧ ∀t₃(t₃::t₁ → t₃ < t₂)
```

**Powertype**:
```
powertypeOf(p,b,c) ↔ categorizes(p,b) ∧ characterizes(p,c)
```

**Regularity**:
- Constraints spanning multiple levels
- Example: "All spouse types compatible with conjugal relationship types"

**Applications**:
- Biological taxonomy (species, genus, family...)
- Product types
- Document classification

### 12.7 OntoUML Formal Semantics

**Benevides et al. (2010)**: Semantics via world structures

**Approach**:
- OntoUML diagram → First-order modal theory
- Theory → Set of models
- Models → Visual world structures

**Validation**:
- If model exists, diagram is consistent
- If no model, axioms are contradictory

**Tools**:
- Alloy (bounded model finding)
- SMT solvers
- Custom constraint satisfaction

**Example output**: Figures 3-5, 7, 9, 11, 13, 15 in paper

### 12.8 Event Mereotopology

**UFO-B** (Benevides et al. 2019b): Complete event ontology

**Temporal ordering**:
- Allen's interval algebra
- Before, after, during, overlaps, meets, etc.

**Event mereology**:
- Parts of events
- Constitution of events

**Participation**:
```
participates(x,e) ↔ Endurant(x) ∧ Perdurant(e) ∧
  ∃p(P(p,e) ∧ ∃d(manifestation(p,d) ∧ inheresIn(d,x)))
```

Endurant participates in event if event has part that is manifestation of disposition inhering in endurant.

**Causation**: Based on disposition manifestation

### 12.9 UFO-C: Social Ontology

**Scope**: Intentional and social entities

**Key categories**:

**Intention**: Mode directed at goal

**Commitment**: Externally dependent mode toward agent

**Claim**: Right to demand action

**Social Object**: Constituted by agentive designation

**Example**: Money
- Physical: Paper with ink
- Constituted as: $20 bill
- Constitution based on: Collective intentionality + institutional facts

**Applications**:
- Goal modeling
- Organizational structures
- Social networks
- Institutional ontology

### 12.10 Ontology Patterns

**Guizzardi (2014)**: Pattern language for conceptual modeling

**Pattern categories**:

**Relator patterns**:
- Basic relator
- Multi-relator
- Relator with roles
- Historical relator

**Parthood patterns**:
- Functional parthood
- Memberof (collective)
- Subcollection-of
- Subquantity-of

**Role patterns**:
- Role with single relator type
- Role with multiple relator types
- Role mixin

**Phase patterns**:
- Phase partition
- Phase with history

**Anti-patterns** (what to avoid):
- Relator as relationship
- Role as kind
- Part-whole cycle
- Homonym/synonym types

---

## Conclusion

### Summary of UFO's Contribution

**Theoretical**:
1. Comprehensive four-category ontology
2. Fine-grained type theory (14 meta-types)
3. Relator-based theory of relationships
4. Integration of endurants and events
5. Multi-level modeling framework

**Practical**:
1. OntoUML modeling language
2. Automated validation tools
3. Anti-pattern detection
4. 50+ domain applications
5. Empirically validated effectiveness

**Philosophical**:
1. Descriptive realism
2. Cognitive/linguistic grounding
3. Pluralistic but principled
4. Connects metaphysics to modeling

### Current Status (2021)

- **Most comprehensive** foundational ontology for conceptual modeling
- **Second-most used** foundational ontology overall
- **Fastest growing** adoption rate
- **Active development** continues

### Future Directions

1. **Complete grounding theory**
2. **Extend UFO-C** (social/institutional ontology)
3. **AI integration** (knowledge graphs, LLMs)
4. **Process mining** alignment (OCEL integration)
5. **Standard development** (ISO, W3C, OMG)

---

## References

**Primary Source**:
Guizzardi, G., Benevides, A. B., Fonseca, C. M., Porello, D., Almeida, J. P. A., & Sales, T. P. (2021). UFO: Unified Foundational Ontology. _Applied Ontology_, 16(1), 1-44.

**Complete TPTP formalization**: https://purl.org/ufo-formalization

**OntoUML repository**: http://purl.org/krdb-core/model-repository/

**OaaS infrastructure**:
- Schema: https://purl.org/krdb-core/ontouml-schema
- JavaScript library: https://purl.org/krdb-core/ontouml-js
- Server: https://purl.org/krdb-core/ontouml-server
- Visual Paradigm plugin: https://purl.org/krdb-core/ontouml-plugin

---

**Document Status**: Complete documentation of UFO paper (Guizzardi et al. 2021)

**Last Updated**: 2026-01-01

**Author**: Extracted from full paper analysis
