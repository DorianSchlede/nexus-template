# Ontological foundations of digital work: What entities actually exist

**Digital work is structured around a remarkably consistent core triad—Agent, Activity, and Object—but the number of entities required to describe it is fundamentally abstraction-dependent, not fixed.** This research synthesizes empirical findings from Object-Centric Process Mining with theoretical frameworks spanning formal ontologies (UFO, PROV-O, BBO), workflow patterns research, Activity Theory, and enterprise architecture frameworks. The findings reveal both strong convergence on foundational primitives and irreducible disagreement about what lies beyond them. Most significantly, **4-8 object types emerge from real enterprise logs**, while theoretical frameworks propose **15-106 entity classes**—a gap explained not by error but by different levels of abstraction serving different purposes.

---

## The empirical reality: What process mining discovers

Object-Centric Process Mining (OCEL 2.0) provides the most grounded empirical evidence for digital work entities. Analysis of enterprise event logs across procurement, manufacturing, insurance, and service industries reveals a consistent pattern: **4-5 object types typically emerge per business process**, with complex end-to-end processes reaching 6-8 types.

The most frequently documented object types from real implementations include:

| Domain | Core Object Types |
|--------|-------------------|
| **Procurement (P2P)** | Purchase Requisition, Purchase Order, Goods Receipt, Invoice, Payment, Vendor |
| **Order-to-Cash** | Order, Order Item, Customer, Product, Invoice, Delivery |
| **Manufacturing** | Work Order, Material, Machine, Production Order, Batch |
| **Field Service** | Service Request, Schedule, Technician, Work Order |
| **Insurance** | Claim, Policy, Customer, Payment, Document |

These entities emerge through **hybrid discovery**—database schema extraction reveals structure (tables become object types, foreign keys become relationships), but meaningful interpretation requires domain expertise. The OCEL 2.0 specification provides formal criteria distinguishing objects from attributes: objects possess unique identifiers, participate in multiple events over time, and maintain relationships to other entities. Attributes, by contrast, exist as dependent properties without autonomous identity.

Critically, Wil van der Aalst's research group notes that while entities emerge from data structures, **the decision about which object types to include requires human judgment about what questions the analysis should answer**. This methodological finding undermines pure bottom-up approaches: entity discovery is semi-automated in extraction but fundamentally interpretive in selection.

---

## Theoretical convergence: The foundational triad

Across formal enterprise ontologies, one pattern appears universal: the **Agent-Activity-Entity triad**. Every major framework distinguishes between actors who perform work, actions that constitute work, and objects that work transforms.

**PROV-O** (W3C Provenance Ontology) formalizes this most parsimoniously with three core classes:
- **prov:Entity** — Physical, digital, or conceptual things with fixed aspects
- **prov:Activity** — Something occurring over time that acts upon entities
- **prov:Agent** — Something bearing responsibility for an activity

**UFO** (Unified Foundational Ontology) provides the deepest philosophical grounding, distinguishing:
- **Endurants** — Things wholly present at each moment (Substantials like objects, Moments like properties)
- **Perdurants** — Things that unfold in time accumulating temporal parts (Events, Processes)
- **Agents** — Intentional entities with beliefs, desires, and intentions (UFO-C layer)

**BBO** (BPMN 2.0 Based Ontology) operationalizes this for process modeling with **106 classes** organized around:
- **Process/Activity** — Work containers and units
- **Resource** — Material, data, software, and human resources
- **Agent** — Performers with roles and jobs
- **Flow** — Sequence and message connections

The workflow patterns research from van der Aalst's group identifies entities across four perspectives, each irreducible to the others:

- **Control Flow**: Task, Condition, Flow, Split/Join, Token (execution state)
- **Data**: Data Element, Data Binding, Data Store, Data Transformation
- **Resource**: Resource, Role, Work Item, Worklist, Capability, Authorization
- **Exception**: Trigger, Signal, Exception Handler

The minimum entity set sufficient to describe all documented workflow patterns comprises approximately **15-20 fundamental concepts**. More expressive notations like BPMN 2.0 expand this to **100+ specialized elements**, while formal systems like Petri nets reduce pure control flow to just **4 primitives**: Place, Transition, Arc, Token.

---

## The abstraction-dependency problem

Is there a "natural" entity count for digital work? The research strongly suggests **no**—entity count is a function of modeling purpose and abstraction level, not an intrinsic property of work itself.

Enterprise architecture frameworks illustrate this clearly:

| Framework | Entity Count | Purpose |
|-----------|-------------|---------|
| ArchiMate 3.2 | ~57 elements | Visual architecture modeling |
| TOGAF Content Metamodel | ~33 entities | EA development lifecycle |
| BPMN 2.0 (via BBO) | ~106 classes | Detailed process specification |
| Petri nets | 4 primitives | Formal verification |
| OCEL empirical | 4-8 object types | Process mining analysis |

ArchiMate explicitly designs for **"80% of practical cases"**—intentionally simpler than UML (~150 elements) or full BPMN. This design choice reflects a judgment that enterprise communication requires less granularity than software engineering or process automation.

Real enterprise models scale accordingly:
- Small organizations: 100-500 entities
- Large enterprises: 2,000-10,000 entities
- Fortune 500: 10,000-100,000+ entities

The implication is profound: **entity count reflects analytical needs, not ontological reality**. A process miner needs 4-5 object types; an enterprise architect needs 50+; a formal verification system needs 4 primitives. All are correct for their purposes.

---

## Bottom-up meets top-down: Do paths converge?

The methodological question of whether entities emerge from data or from theory yields a nuanced answer: **both paths identify the same foundational triad but diverge beyond it**.

**Bottom-up (empirical) approaches** reliably discover:
- Business documents (orders, invoices, claims)
- Transaction records (payments, deliveries)
- Master data entities (customers, products, vendors)
- Resource assignments (technicians, schedules)

These correspond directly to database tables with primary keys—OCEL's extraction methodology leverages existing data architecture.

**Top-down (theoretical) approaches** additionally specify:
- Abstract behavioral concepts (events, gateways, conditions)
- Organizational structure (roles, communities, divisions)
- Intentional states (goals, beliefs, intentions—from UFO-C)
- Temporal relationships (precedence, simultaneity, duration)

The divergence occurs because empirical approaches discover **what is recorded**, while theoretical approaches specify **what is necessary for complete description**. Process logs capture events and object states; they rarely capture why someone made a decision or what organizational tensions shaped a process.

---

## Relationships between entities: Structure not hierarchy

Digital work ontologies consistently define relationships as **structural patterns** rather than strict hierarchies. The documented relationship types organize into three categories:

**Control relationships** govern execution:
- Precedes/follows (sequential ordering)
- Enables/triggers (causal initiation)
- Contains/decomposes (hierarchical nesting)
- Synchronizes (parallel coordination)

**Data relationships** govern information:
- Reads/writes (access patterns)
- Transforms (conversion operations)
- Passes (movement between components)
- Realizes (abstraction mapping)

**Resource relationships** govern responsibility:
- Performs/executes (work completion)
- Offers/allocates (assignment mechanisms)
- Delegates/escalates (transfer of responsibility)
- MemberOf/hasRole (organizational membership)

ArchiMate formalizes cross-layer integration through two primary relationship types: **serving** (support/enablement) and **realization** (abstraction-to-concrete mapping). These allow tracing from business processes through applications to infrastructure.

Notably, **no framework proposes strict entity hierarchy**. Even UFO's foundational/domain layering treats layers as analytical distinctions, not ontological rankings. Entities at different abstraction levels coexist as different views of the same underlying reality.

---

## What Activity Theory adds: The human-centric gap

Activity Theory introduces entities that **no process-centric ontology captures**. Rooted in Vygotsky's cultural-historical psychology, it identifies six fundamental elements forming an "activity system":

- **Subject** — Actor with motives, needs, and consciousness (not mere "resource")
- **Object** — Dynamically interpreted goal, not fixed input/output
- **Tools** — Mediating artifacts that shape cognition, not neutral instruments
- **Rules** — Implicit norms, not just explicit business rules
- **Community** — Group sharing the object, with collective purpose
- **Division of Labor** — Negotiated, evolving distribution of tasks

The critical additions include:

**Contradictions** — Developmental tensions driving change. BPM treats process deviations as errors; Activity Theory treats them as signals of underlying contradictions requiring resolution.

**Mediation** — Tools don't merely enable work; they fundamentally shape how work is conceived and performed. A spreadsheet structures thinking differently than a database.

**Historical development** — Current processes embed accumulated historical decisions. Process models capture current state; activity analysis traces genesis.

**Zone of Proximal Development** — Gap between current and potential capability, essential for understanding learning and expertise growth.

Knowledge-Intensive Business Process (KiBP) research extends BPM toward Activity Theory by adding entities for:
- Beliefs, Desires, Intentions (BDI agent model)
- Innovation and Impact agents (creative roles)
- Contingency and half-life (knowledge validity decay)
- Collaborative sessions and mental images

These additions acknowledge that knowledge work cannot be fully specified in advance—goals emerge, decisions depend on judgment, and outcomes reflect expertise not just procedure execution.

---

## The boundary question: What cannot be formalized

Several aspects of digital work **resist entity formalization**:

| Aspect | Why It Resists Formalization |
|--------|------------------------------|
| **Tacit knowledge** | "We can know more than we can tell" (Polanyi)—embodied know-how escapes articulation |
| **Articulation work** | Invisible coordination that makes visible work possible, rarely logged |
| **Awareness** | Dynamic, implicit mutual knowledge of others' activities—continuously negotiated |
| **Social capital** | Trust and relationships enabling collaboration—cannot be encoded as workflow |
| **Sense-making** | Retrospective interpretation creating meaning—subjective and contextual |
| **Improvisation** | Spontaneous adaptation to contingencies—by definition unscripted |
| **Emotion and motivation** | Passion, frustration, engagement—outside formal process scope |

Process mining researchers acknowledge: "Tacit knowledge often evades codification and is not available for process mining. Because knowledge-intensive processes often lack extensive digital event logs, many common process mining techniques cannot be applied without adaptation."

This suggests **"digital work" may not be a fully coherent concept** with shared ontological basis. What can be digitally recorded (events, objects, timestamps) differs fundamentally from what constitutes meaningful human work (purpose, understanding, collaboration). Entity-based ontologies capture the recordable substrate; they systematically miss the human dimension that makes work meaningful.

---

## Cross-domain vs. domain-specific entities

Certain entities appear **universally across industries**:

**Cross-domain entities (appear everywhere):**
- Document/artifact objects (orders, invoices, reports)
- Transaction events (create, approve, complete)
- Person/organization agents
- Temporal references (deadlines, durations)
- Status/state attributes

**Domain-specific entities (appear in specific contexts):**
- Healthcare: Patient, Diagnosis, Treatment Plan, Clinical Pathway
- Manufacturing: Work Order, Bill of Materials, Quality Control Record
- Finance: Account, Transaction, Portfolio, Risk Assessment
- Logistics: Shipment, Container, Route, Carrier

Enterprise ontologies like ArchiMate handle this through **layered abstraction**—generic elements (Business Process, Application Component) instantiate differently per domain while maintaining structural consistency.

---

## Consensus and open questions

**Points of strong consensus:**
1. Agent-Activity-Entity triad is foundational
2. Activities have temporal bounds (start, end, duration)
3. Objects serve as inputs/outputs of activities
4. Roles mediate agent participation in activities
5. Events trigger state changes and process flow

**Points of persistent disagreement:**
1. Whether entities are discovered or constructed
2. Appropriate granularity for different purposes
3. Status of intentional/mental entities (beliefs, goals)
4. Whether tacit knowledge can ever be captured
5. Relationship between specification (model) and execution (instance)

**Open research questions:**
- How can automated systems determine appropriate object granularity?
- Can the entity/attribute boundary be formalized without domain knowledge?
- What methodology bridges Activity Theory's human-centric view with process mining's data-centric view?
- Is there a universal minimal ontology for digital work, or is domain-specificity irreducible?

---

## Synthesis: A proposed entity framework

Based on this research, digital work ontologies organize around **four irreducible perspectives**, each with characteristic entity types:

```
STRUCTURAL PERSPECTIVE
├── Agent (Subject, Actor, Resource, Role)
├── Object (Entity, Business Object, Data Object, Artifact)
└── Tool (Application, Technology, Mediating Artifact)

BEHAVIORAL PERSPECTIVE
├── Activity (Process, Task, Function, Action, Event)
├── Flow (Sequence, Control, Data, Message)
└── State (Condition, Marking, Situation)

ORGANIZATIONAL PERSPECTIVE
├── Community (Organization Unit, Pool, Group)
├── Rule (Constraint, Business Rule, Norm)
└── Division (Role Assignment, Authorization, Capability)

INTENTIONAL PERSPECTIVE (often implicit/missing)
├── Goal (Objective, Outcome, Motive)
├── Knowledge (Belief, Expertise, Tacit Know-how)
└── Meaning (Value, Purpose, Interpretation)
```

The first three perspectives achieve reasonable formalization across existing frameworks. The fourth—the intentional perspective—remains under-specified, capturing what Activity Theory and KiBP research identify as the distinctively human elements of work.

**The fundamental finding:** There is no single correct entity count for digital work. **4 primitives suffice for formal verification; 5-8 object types emerge from logs; 15-20 concepts describe workflow patterns; 50-100 elements support enterprise architecture.** These are not competing answers but different tools for different purposes. The ontological question "what entities exist?" must always be qualified by the pragmatic question "exist for what purpose?"