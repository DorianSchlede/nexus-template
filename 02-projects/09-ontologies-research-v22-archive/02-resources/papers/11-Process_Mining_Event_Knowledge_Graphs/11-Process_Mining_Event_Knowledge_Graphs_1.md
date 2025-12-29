<!-- Source: 11-Process_Mining_Event_Knowledge_Graphs.pdf | Chunk 1/3 -->

# **Process Mining over Multiple Behavioral** **Dimensions with Event Knowledge Graphs**

Dirk Fahland [(][B][)]


Eindhoven University of Technology, Eindhoven, The Netherlands

d.fahland@tue.nl


**Abstract.** Classical process mining relies on the notion of a unique
case identifier, which is used to partition event data into independent
sequences of events. In this chapter, we study the shortcomings of this
approach for event data over _multiple entities_ . We introduce _event knowl-_
_edge graphs_ as data structure that allows to naturally model behavior
over multiple entities as a network of events. We explore how to construct, query, and aggregate event knowledge graphs to get insights into
complex behaviors. We will ultimately show that event knowledge graphs
are a very versatile tool that opens the door to process mining analyses
in multiple behavioral dimensions at once.


**Keywords:** Event knowledge graph _·_ Process mining


**1** **Introduction—A Second Look at Processes**


Process mining aims at analyzing processes from recorded event data. Thereby,
the actual processes are rather complex and emerge from the interplay of multiple
inter-related _entities_ : the various _objects_ handled by the process as well as the
_organizational entities_ that execute the process. We best explain this kind of
interplay by an example.


1. Consider a retailer who took two _Orders_ for multiple _Items_ from the same
customer: the customer first places Order _O_ 1 for 2 items _X_ and 1 item _Y_,
and shortly afterwards Order _O_ 2 for 1 item _X_ and 1 item _Y_ . The retailer
promises to ship every order within 6 days.


The retailer handles both orders as explained next and illustrated in Fig. 1.


2. Items _X_ are provided by supplier _A_ while items _Y_ are provided by supplier
_B_ . To save costs, _workers_ of the retailer bundle the orders for the items and
place two _Supplier Orders_, one at _A_ for 3 items _X_ and one at _B_ for 1 item _Y_ .
Suppliers ensure to deliver their products within 3 days of placing the order.
3. Invoice _I_ 2 for Order _O_ 2 is created right after placing the supplier order at _B_ .
4. When the retailer receives the Supplier Order from _A_, workers unpack three
Items _X_ one by one and store them in an _automated warehouse_ until needed
for shipment. At this point, workers also create _Invoice I_ 1 for _O_ 1.


_⃝_ c The Author(s) 2022

W. M. P. van der Aalst and J. Carmona (Eds.): Process Mining Handbook, LNBIP 448, pp. 274–319, 2022.
[https://doi.org/10.1007/978-3-031-08848-3_9](https://doi.org/10.1007/978-3-031-08848-3_9)


Event Knowledge Graphs 275


**Fig. 1.** Illustration of a multi-entity process: a retailer handles two orders for multiple
items by placing and receiving supplier orders for specific items.


5. Around the time of receiving the supplier order from _A_, a _worker_ notices
they made a mistake: they ordered only one item _Y_ from _B_ while _O_ 1 and
_O_ 2 both require one item _Y each_ . The worker updates the Supplier Order _O_ 2
and invoice _I_ 2 accordingly.
6. When finally the supplier order from _B_ is received, the items _Y_ are unpacked.
One item _Y_ is stored in the warehouse while the other item _Y_ is packed
together with two items _X_ taken from the _warehouse_ into the shipment for
_O_ 1. Packed shipments are picked up for delivery every day at 15:00.
7. The retailer has the policy that they only ship to a customer if there is at
most one unpaid invoice. Thus, packing and shipment of _O_ 2 (another item
_X_ and the second _Y_ ) are delayed until _Payment P_ 1 is received which covers
the amount for both invoices _I_ 1 and _I_ 2.


This process relies on 7 different types of entities. _Actors_ (human workers) and
_machines_ (an automated warehouse) together handle 5 types of objects: _Orders_,
_Supplier Orders_, _Items_, _Invoices_, _Payments_ .


**Challenges Due to Event Data over Multiple Entities.** A process mining
analysis of the above process execution relies on recorded event data. Each event
has to record in its attributes at least (1) which _action_ (or activity) has been
executed (2) at which _time_ . To construct an event log, classical process mining
also expects each event to record (3) in which process execution, typically called


276 D. Fahland



**Table 1.** Event table of events underlying the event log of Table 2.



_case_, the event occurred (see [13], Sect. 2). Table 1 shows the events related to
the above example.


1. create _Orders_ in _e_ 1 _, e_ 2;
2. create _Supplier Orders_ in _e_ 3 _, e_ 4;
3. create _Invoice I_ 2 in _e_ 5;
4. receive _Supplier Order_ from _A_ in _e_ 6 and unpack _Items X_ in _e_ 8 _, e_ 10 _, e_ 11, and
create _Invoice I_ 1 in _e_ 18;
5. update _Supplier Order_ for _B_ in _e_ 7 and _Invoice I_ 2 in _e_ 9;
6. receive _Supplier Order_ for _B_ in _e_ 19 and unpack _Items Y_ in _e_ 20 _, e_ 21, and pack
and ship _Order O_ 1 in _e_ 27 _, e_ 28;
7. receive _Payment P_ 1 and clear _Invoices I_ 1 _, I_ 2 in _e_ 29 _, e_ 30 and finally pack and
ship _Order O_ 2 in _e_ 33 _, e_ 34.


In contrast to classical event logs, Table 1 contains no typical case identifier
attribute by which each event is related to one specific process execution.
Instead, we see multiple sparsely filled attributes identifying _multiple entities_ of


Event Knowledge Graphs 277


various types: _Order_ ( _O_ 1 _, O_ 2), _Supplier Order_ ( _A, B_ ), _Item_ ( _X_ 1 _, X_ 2 _, X_ 3 _,_
_Y_ 1 _, Y_ 2), _Invoice_ ( _I_ 1 _, I_ 2), and _Payment_ ( _P_ 1).
This makes it difficult to construct an _event log_ which is the basis for process
mining analysis. Recall that to obtain a classical event log we select one _case_
_identifier_ attribute. Then all events referring to the same case id and ordered by
time form the _trace_ of this case, that is, one process execution. In this way, classical event logs partition the recorded behavior into multiple process executions.
Process mining techniques then identify frequent patterns shared by all process
executions, or identify outliers and deviations of specific process executions.
However, what exactly _is_ a process execution in our example? It is not just all
events related the one particular entity. For instance, if we chose _Order_ as case
identifier, we would obtain traces _⟨e_ 1 _, e_ 18 _, e_ 27 _, e_ 29 _⟩_ for _O_ 1 and _⟨e_ 2 _, e_ 5 _, e_ 7 _, e_ 33 _, e_ 34 _⟩_
for _O_ 2. These traces do reveal that both orders were not shipped within 6 days
as intended by the supplier. However, they do not allow us to understand the
cause for this as they clearly do not describe the entire behavior shown in Fig. 1.
We could try to group all events into traces using _multiple related case identi-_
_fiers_ . However, we will see in Sect. 3 that doing so introduces false behavioral
information called _convergence_ and _divergence_ [41,45] in the resulting event log
leading to false analysis results (see [1], Sect. 3)
False behavioral information arises when flatting Table 1 into sequential
traces because we _cannot_ partition the entities _O_ 1 _, O_ 2 _, A, B, X, Y, I_ 1 _, I_ 2 _, P_ 1 into
disjoint sets, each belonging to one process execution that is independent of all
others. Rather, the behavior itself is a larger “fabric” of multiple entities that
are inter-related and inter-twined over time as shown in Fig. 1. This “fabric” is
even more complex as individual _Actors_ ( _R_ 1 _, . . ., R_ 5) are specialized in specific
activities across multiple different entities, e.g., _R_ 2 specializes receiving, updating, and unpacking _Supplier Orders_ and handling _Items_ . In the following, we
explain how to analyze this very “fabric” of multiple inter-related entities as a
whole from a simple event table over multiple entity identifiers such as Table 1.


**A Graph-Based Approach.** Our trick will be to slightly adapt the existing
definitions for obtaining an event log from an event table: instead of constructing
entire traces related to a single case identifier, we discuss in Sect. 3 a _local directly-_
_follows_ relation for each _individual_ entity in the data. Each event can be part of
multiple such directly-follows relations, depending on to how many entities it is
correlated. We then use the model of _labeled property graphs_ in Sect. 4 to create
an _event knowledge graph_ having events as nodes and the local directly-follows
relations as edges between events. We obtain a graph similar to what is shown
in Fig. 1, but with precise semantics for events and behavioral information.
A path of directly-follows edges over events related to the same entity is similar to a classical trace. However in an event knowledge graph, such paths meet
whenever an event is related to more than one entity, where in an event log each
trace is disjoint from all others. We explain in Sect. 5 how to interpret and analyze behavioral information in event knowledge graphs. We show how basic _query-_
_ing_ on event knowledge graphs gives insights into complex behavioral properties.


278 D. Fahland


We show how _aggregation_ on event knowledge graphs allows to construct multientity process models that better describe such processes.
We finally explore the versatility of event knowledge graphs beyond the
control-flow perspective in Sect. 6. We show how event knowledge graphs naturally integrate the control-flow perspective and the _actor perspective_ . Querying
for specific structures in the event knowledge graph reveals complex patterns of
_task instances_ not visible in either perspective alone. Further, we show how event
knowledge graphs allow us to take a _system-perspective_ (or queueing perspective) to analyze emergent behavior and performance problems across multiple
entities. We conclude in Sect. 7 with an outlook on the various applications areas
of event knowledge graphs in process mining, and on open research challenges.
All concepts for constructing and analyzing event knowledge graphs presented in this chapter are implemented as Cypher queries on the graph database
system Neo4j [1] [at https://github.com/multi-dimensional-process-mining/event](https://github.com/multi-dimensional-process-mining/eventgraph_tutorial)
graph [tutorial [28].](https://github.com/multi-dimensional-process-mining/eventgraph_tutorial)


**2** **Multi-entity Event Data**


Before we discuss problems and solutions for analyzing event data over multiple
entities, we first define what “event data over multiple entities” actually is.


**2.1** **Events**


We assume all data to be given in a single event table. Data is recorded from a
universe of values _Val_ ; timestamps _Val_ _time ⊆_ _Val_ are totally ordered by _≤_ .


**Definition 1 (Event Table).** _An_ event table _T_ = ( _E, Attr_ _,_ #) _is a set E of_
_events, a set Attr of_ attribute names _with act, time ∈_ _Attr. Partial function_
# : _E × Attr_ ↛ _Val assigns an event e ∈_ _E and an attribute name a ∈_ _Attr to_
_a value_ # _a_ ( _e_ ) = _v;_ # _a_ ( _e_ ) = _⊥_ _if a is undefined for e._
_Each event e ∈_ _E records an activity and a timestamp, i.e.,_ # _act_ ( _e_ ) _̸_ = _⊥_ _and_
# _time_ ( _e_ ) _∈_ _Val_ _time._


We write _e.a_ = _v_ for # _a_ ( _e_ ) = _v_ as a shorthand. An event table specifically
allows multi-valued attributes, e.g., sets of values # _a_ ( _e_ ) = _{v_ 1 _, v_ 2 _, v_ 3 _}_ or a list of
values # _a_ ( _e_ ) = _⟨v_ 1 _, v_ 2 _, v_ 3 _, v_ 1 _⟩_ . [2] Simplifying notation, we also may write _v ∈_ _e.a_
if _e.a_ = _v_ or if _e.a_ = _⟨. . ., v, . . .⟩_ .
An event table only defines _e.activity_ and _e.time_ attributes for each event.
The special characteristic of event data over multiple entities is that it does not
record a unique case identifier attribute, but identifiers of _multiple entity types_ .


**Definition 2 (Event table with entity types).** _An_ event table with entities
types _T_ = ( _E, Attr_ _,_ # _, ENT_ ) _additionally designates one or more attributes ∅̸_ =
_ENT ⊆_ _Attr as names of_ entity types _._


1 [neo4j.com.](http://neo4j.com/)
2 We assume the values in an event table to be consistent with some data model that
is specified elsewhere. Our subsequent discussion does not rely on it.


Event Knowledge Graphs 279


A classical event log corresponds to an event table with a single entity type
_ENT_ = _{case}_ . We can consider Table 1 is an event table with entity types
_ENT_ = _{Resource, Order, Supplier Order, Item, Invoice, Payment}_ .
Event tables (Definition 1) are also called raw event logs and are – besides
relational data – the most common form of input to process mining. The entity
types of Definition 2 can be retrieved from an event table through schema recovery techniques [46]. Note that Definition 2 formalizes the object-centric event
logs (OCEL) described in Sect. 3.4 of [1]; we here use the more general term
“entity” instead of “object” as we will later study behavior over entities which
are not tangible objects.
Event tables do not model the ordering of events with respect to a case or
an entity which is needed for process mining. Before we study the ordering of
events, we explain how events relate to entities.


**2.2** **Entities and Correlated Events**


Each entity type _ent ∈_ _ENT_ is a column in the event table _T_ . Each value in
that column refers to a specific entity.


**Definition 3 (Entities).** _Let T_ = ( _E, Attr_ _,_ # _, ENT_ ) _be an event table with_
_entities. Let ent ∈_ _ENT be an entity type. The_ set of entities _in T of type ent_
_is Entities_ ( _ent, T_ ) = _{n | ∃e ∈_ _E_ : _n ∈_ _e.ent}._


From Table 1 we identify 6 entity types with corresponding entities: (1) Order:
_{O_ 1 _, O_ 2 _}_ = _Entities_ ( _Order_ _, T_ ), (2) Supplier Order: _A, B_, (3) Item: _X_ 1 _, X_ 2 _, X_ 3
and _Y_ 1 _, Y_ 2, (4) Invoice: _I_ 1 _, I_ 2, (5) Payment: _P_ 1, (6) Resource: _R_ 1 _−_ _R_ 5 (see
Definition 3).
An event _e ∈_ _E_ which has a value _n_ = _e.ent_ or _n ∈_ _e.ent_ is _correlated_ to
entity _n_ .


**Definition 4 (Correlation).** _Let T_ = ( _E, Attr_ _,_ # _, ENT_ ) _be an event table_
_with entities. Let n ∈_ _Entities_ ( _ent, T_ ) _be an entity of type ent ∈_ _ENT._
_Event e is_ correlated to _entity n, written_ ( _e, n_ ) _∈_ _corr ent,T iff n_ = _e.ent ∨n ∈_
_e.ent. We write corr_ ( _n, ent, T_ ) = _{e ∈_ _E |_ ( _e, n_ ) _∈_ _corr ent,T } for the set of_
_events correlated to entity n ∈_ _Entities_ ( _ent, T_ ) _._


For example, for Table 1, event _e_ 30 is correlated to _I_ 1, _I_ 2, and _P_ 1, i.e.,
( _e_ 30 _, I_ 1) _,_ ( _e_ 30 _, I_ 2) _∈_ _corr Invoice,T_ and ( _e_ 30 _, P_ 1) _∈_ _corr Payment,T_ . The events correlated to _I_ 2 are _corr_ ( _I_ 2 _, Invoice, T_ ) = _{e_ 5 _, e_ 9 _, e_ 30 _}_ . In case the entity identifiers
used by different entity types are disjoint, e.g., there are not an Order _O_ 3 and an
Item _O_ 3, we can omit entity types and just write ( _e_ 30 _, I_ 1) _,_ ( _e_ 30 _, I_ 2) _,_ ( _e_ 30 _, P_ 1) _∈_
_corr T_ and _corr_ ( _I_ 2 _, T_ ) = _{e_ 5 _, e_ 9 _, e_ 30 _}_ .
Correlation lifts to a _set_ _N_ of entities by union: _corr_ ( _N, T_ ) =

_n∈N_ _[corr]_ [(] _[n, T]_ [). We will later use this to collect events of (transitively) related]
entities, which we discuss next.


280 D. Fahland


**Fig. 2.** Relations between entities derived from Table 1


**2.3** **Relations Between Entities**


We now make a first important observation. Although our data only defines
entity types explicitly, it _implicity_ defines _relations between entity types_ . A
record _e_ in Table 1 containing two identifiers _n_ 1 _, n_ 2 of two different types implicitly relates _n_ 1 and _n_ 2. For example, event _e_ 5 defines that _e_ 5 _.Order_ = _O_ 2
is related to _e_ 5 _.Invoice_ = _I_ 2 and event _e_ 18 defines that _e_ 18 _.Order_ = _O_ 1 is
related to _e_ 18 _.Invoice_ = _I_ 1. We can write this as a relation _R_ ( _Invoice,Order_ ) =
_{_ ( _O_ 1 _, I_ 1) _,_ ( _O_ 2 _, I_ 2) _}_ .


**Definition 5 (Relation).** _Let T_ = ( _E, Attr_ _,_ # _, ENT_ ) _be an event table with_
_entities. Let ent_ 1 _, ent_ 2 _∈_ _ENT be two entity types. The_ relation between _ent_ 1
and _ent_ 2 in _T is R_ ( _ent_ 1 _,ent_ 2) = _{_ ( _e.ent_ 1 _, ent_ 2) _| e.ent_ 1 _̸_ = _⊥, e.ent_ 2 _̸_ = _⊥}._


Note that Definition 5 does not impose the direction of a relation. Figure 2
visualizes the relations we can derive from Table 1.
Recall that in relational data modeling, each relation _R_ ( _ent_ 1 _,ent_ 2) has a _car-_
_dinality_ describing how many entities of type _ent_ 1 are related to each entity
of type _ent_ 2, and vice versa. We can infer this cardinality from the tuples in
_R_ ( _ent_ 1 _,ent_ 2) if we assume that the data in the input event table is sufficiently
complete. For example, for the relations in Fig. 2,


 - _R_ ( _Invoice,Order_ ) is a 1-to-1 relation as each invoice is related to one order, and
vice versa;

 - _R_ ( _Invoice,Payment_ ) is an n-to-1 relation as both _I_ 1 and _I_ 2 are related to _P_ 1;

 - _R_ ( _Item,Order_ ) is an n-to-1 relation as each order has multiple items but each
item relates to exactly one order;

 - _R_ ( _Item,Supplier Order_ ) is an n-to-1 relation.


Entities are also transitively related by concatenating or joining the relations on a shared entity typed (and then omitting this shared entity type).
For example, _R_ ( _Order,Payment_ ) = _R_ ( _Invoice,Order_ ) _▷◁_ _R_ ( _Invoice,Payment_ ) =
_{_ ( _O_ 1 _, P_ 1) _,_ ( _O_ 2 _, P_ 1) _}_ is an n-to-1 relation, and _R_ ( _Order,Supplier Order_ ) =
_R_ ( _Item,Order_ ) _▷◁R_ ( _Item,Supplier Order_ ) = _{_ ( _O_ 1 _, A_ ) _,_ ( _O_ 1 _, B_ ) _,_ ( _O_ 2 _, A_ ) _,_ ( _O_ 2 _, B_ ) _}_ is an
n-to-m relation.
Entities, relations, and correlation of events can be automatically retrieved
from event tables [46] and relational databases [41,43] through schema recovery
techniques. However, we have to be aware that relations and their cardinalities


Event Knowledge Graphs 281


recovered according to Definition 5 are a _static_ view of the relations obtained by
aggregating all observations over time while _a process updates relations dynam-_
_ically_ . For instance, _Order O_ 1 was not related to any _Item_ until event _e_ 27.
Modeling such dynamics requires additional concepts as defined in XOC event
logs [39,40]. We have to ignore this aspect in the remainder.


**3** **Shortcomings of Event Logs over Multi-entity Event**
**Data**


Having defined event data over multiple entities, we can now discuss ways of
ordering events correlated to a case or an entity, which is the basis for process
mining analysis. We first explain how transforming multi-entity data into a classical event log with a single case identifier (Sect. 3.1) introduces false behavioral
information leading to false analysis results (Sect. 3.2). We then propose a different approach to ordering events with respect to individual entities (Sect. 3.3).


**3.1** **Classical Event Log Extraction**


We cannot directly turn the event data in Table 1 into a classical event log,
because we lack a clear case identifier column that is defined for all events. While
_Actor_ is an entity identifier defined for all events, it does not group events into
the process executions described in Sect. 1. The standard procedure to extract
a classical event log from such data is the following (see also Def. 5 of [1] and

[13]).
**Step 1. Determine relevant entities in the data.** An event table with
entity identifiers already defines the set of entities in the process (see Definition 3).
For extracting an event log for a process execution, we only consider entities that
are also handled “along” or “within” a process execution. Thus, we now focus on
_Order_, _Supplier Order_, _Item_, _Invoice_, and _Payment_ and exclude _Actor_ . [3]

**Step 2. Pick one entity as case identifier.** As the process goal is to complete an order, entity _Order_ is our best candidate for a case identifier. This identifier defines two cases: _O_ 1 and _O_ 2. However, as most events in Table 1 are not
directly correlated to an _Order_, we cannot simply group events by attribute _Order_ .
**Step 3. Define the set of all entities related to a case.** The classical
idea is to “enlarge” the scope of the case. We include all entities which are
(transitively) related to the case entities _O_ 1 and _O_ 2 via the relations we can
identify in the event table (see Definition 5 and Fig. 2).


 - Order _O_ 1 is related to Invoice _I_ 1, Payment _P_ 1, Items _X_ 1 _, X_ 2 _, Y_ 1, and Supplier Orders _A, B_, i.e., _caseEntities_ ( _O_ 1) = _{O_ 1 _, I_ 1 _, P_ 1 _, X_ 1 _, X_ 2 _, Y_ 1 _, A, B}_ .

 - Order _O_ 2 is related to Invoice _I_ 2, Payment _P_ 1, Items _X_ 3 _, Y_ 2, Supplier Orders
_A, B_, i.e., _caseEntities_ ( _O_ 2) = _{O_ 2 _, I_ 2 _, P_ 1 _, X_ 3 _, Y_ 2 _, A, B}_ .


3 In later sections we will not have to make such a distinction and can consider behavior
along any kind of entity.


282 D. Fahland


**Step 4. Construct a trace from events of all entities in a case.** Each
event _e_ correlated to an entity _n ∈_ _caseEntities_ ( _O_ 1) is now also considered as
correlated to case _O_ 1: _corr_ _[∗]_ ( _O_ 1 _, T_ ) = _corr_ ( _caseEntities_ ( _O_ 1) _, T_ ). For example,
for _O_ 1 we extract from Table 1:


 - _corr_ ( _O_ 1 _, T_ ) = _{e_ 1 _, e_ 2 _, e_ 18 _}_

 - _corr_ ( _I_ 1 _, T_ ) = _{e_ 18 _, e_ 30 _}_

 - _corr_ ( _P_ 1 _, T_ ) = _{e_ 29 _, e_ 30 _}_

 - _corr_ ( _X_ 1 _, T_ ) = _{e_ 6 _, e_ 10 _, e_ 27 _}_

 - _corr_ ( _X_ 2 _, T_ ) = _{e_ 6 _, e_ 11 _, e_ 27 _}_

 - _corr_ ( _Y_ 1 _, T_ ) = _{e_ 19 _, e_ 20 _, e_ 27 _}_

 - _corr_ ( _A, T_ ) = _{e_ 3 _, e_ 6 _, e_ 8 _, e_ 10 _, e_ 11 _}_

 - _corr_ ( _B, T_ ) = _{e_ 4 _, e_ 7 _, e_ 19 _, e_ 20 _, e_ 21 _}_


Taking their union yields _corr_ _[∗]_ ( _O_ 1 _, T_ ) = _{e_ 1 _, e_ 3 _, e_ 4 _, e_ 6 _, e_ 10 _, e_ 11 _, e_ 18 _, e_ 19 _, e_ 20 _, e_ 27 _,_
_e_ 28 _, e_ 29 _, e_ 30 _}_ . We store all events extracted for _O_ 1 in a new event table where
we explicitly set the attribute _Case_ to _O_ 1. In this way, we materialize that each
_ei ∈_ _corr_ _[∗]_ ( _O_ 1 _, T_ ) is correlated to _O_ 1. We repeat this procedure for each case.
Table 2 shows the extracted events for _O_ 1 and _O_ 2.
Note that this extraction approach can extract the same event _multiple times_
for different cases but with a different value for the newly set _Case_ attribute.
For instance, _e_ 3 and _e_ 30 are extracted both for _O_ 1 and for _O_ 2. This is due to
the n-to-m relation between _Order_ and _Supplier Order_ and the n-to-1 relation
between _Payment_ and _Order_ .
Ordering the extracted events by time in each case results in the _traces_ from
the viewpoint of _O_ 1 and from the viewpoint of _O_ 2 respectively as shown in Tab 2.
Event logs can be automatically extracted in this way from event tables with
multiple entity identifiers [46]. Extraction from relational databases succeeds
through SQL queries that extract and group events from different tables into
traces [35]. These queries can be generated automatically using a variety of
techniques [6,7,12,29,35,41]; see [2,13] for a detailed discussion.


**3.2** **False Behavioral Information in Classical Event Logs**


Note that the event log in Table 2 contains numerous _false_ behavioral
information. Some events were duplicated and occur in both traces, e.g.,
_e_ 3 _, e_ 4 _, e_ 6 _, e_ 19 _, e_ 29, suggesting that in total four _Supplier Orders_ were placed and
received (while there were only two) and that two _Payments_ were received (while
there was only one). This is also known as _divergence_ [41,41,45,52].
Further, the order of events in both traces gives false behavior information.
For instance, in the trace for O2, _Update SO_ ( _e_ 7) occurs after _Receive SO_ ( _e_ 6)
suggesting a supplier order was updated after it had been received (while this
never happened for any Supplier Order). This is also known as _convergence_ [41,
45,52].
Where divergence falsifies frequencies of events, convergence falsifies the
behavioral information in the directly-follows relation, which is the basis for


Event Knowledge Graphs 283


**Table 2.** Classical event log of order process with events extracted for case identifier
_Order_ .


most process discovery techniques. As a result, also discovered process models are wrong. Figure 3 (left) shows the directly-follows graph (DFG) of the log
in Table 2 and the corresponding process model discovered with the Inductive
Miner (IM) annotated with the mean waiting times. Both models show false
information suggesting that


 - a _Supplier Order_ was _Updated_ after it was _Received_ while this never happened;

 - _rework_ happened around receiving a _Supplier Order_ and unpacking _Items_
while each Supplier Order and each Item was touched only once;

 - an _Invoice_ can be _created_ and _updated_ in an arbitrary order while only one
order was observed;


284 D. Fahland


**Fig. 3.** Directly-follows graph of event log of Table 2 (left) and Inductive Miner model
(right) show false dependencies.


The performance information in the IM model suggests that


 - the mean time for receiving a _Supplier Order_ after placement is 2.2d while _A_
was received within 3d after placement ( _e_ 3- _e_ 6) and _B_ was received within 5d
after placement ( _e_ 4- _e_ 19) and within 3d after the last update ( _e_ 7- _e_ 19).


This false behavioral information makes it impossible to properly locate deviating behaviors and causes for delays, e.g., the reasons why both orders were not
shipped within 6 days.


**3.3** **Correct Behavioral Information: Local Directly-Follows**


The reason why the event log in Table 2 contains false behavioral information is
the following:


Event Knowledge Graphs 285


 - Events that are (transitively) correlated to the global case identifier _Order_
via a 1-to-m relationship are visible to multiple cases, and thus extracted
multiple times, e.g. _e_ 3.

 - Extracting events from multiple different entities and ordering them by time
from the perspective of the global case identifier _Order_ constructs a temporal
order between events that are actually unrelated, e.g., _e_ 6 and _e_ 7.


We can avoid both problems by simply _not_ extracting all events towards a single case identifier, but keeping all events local to the entities they are _directly_
correlated to. To analyze behavior, we only construct a temporal order between
events that are related, e.g., correlated to the same entity.
In other words, instead of defining one global directly-follows relation for all
events based on a global case identifier, we define a local directly-follows relation
_per_ entity [30, Def. 4.6].


**Definition 6 (Directly-Follows (per Entity)).** _Let T_ = ( _E, Attr_ _,_ # _, ENT_ )
_be an event table with entities. Let n ∈_ _Entities_ ( _ent, T_ ) _be an entity of type_
_ent ∈_ _ENT._
_Let e_ 1 _, e_ 2 _∈_ _E be two events; e_ 2 directly follows _e_ 1 from the perspective of
_n, written e_ 1 ⋖ _n,T e_ 2 _iff_


_1._ ( _e_ 1 _, n_ ) _,_ ( _e_ 2 _, n_ ) _∈_ _corr ent,T (both are correlated to n),_
_2. e_ 1 _.time < e_ 2 _.time (e_ 1 _occurred before e_ 2 _),_
_3. and there is no other event_ ( _e_ _[′]_ _, n_ ) _∈_ _corr ent,T with e_ 1 _.time < e_ _[′]_ _.time <_
_e_ 2 _.time_


For example, while _e_ 7 directly follows _e_ 6 globally for _O_ 2, they do not follow each
other locally from the perspective of _O_ 2. Instead, from the perspective of _O_ 2, _e_ 7
directly follows _e_ 4, i.e., _e_ 4 ⋖ _B,T e_ 7. Interestingly, also _e_ 2 ⋖ _O_ 2 _,T e_ 7 and _e_ 6 ⋖ _R_ 2 _,T e_ 7
hold. That means _e_ 7 directly follows _three_ different events as seen from three
different perspectives: the Supplier Order _B_, the Order _O_ 2 and resource _R_ 2.
We cannot represent this information in a single table or a sequential event
log. Extracting a _collection_ of related sequential event logs from event tables [46]
and relational databases [41] results in collection of directly-follows relations per
entity-type. However, the behavioral information remains separated per entity
type, hindering reasoning about the process as a whole [25]. We therefore turn
to a graph-based data model.


**4** **Event Knowledge Graphs**


Our primary aim is to model multiple local directly-follows relations (see Definition 6) over events correlated to multiple entities. To construct these relations,
we also have to model entities, relations between entities, and correlations of
entities to events (see Sect. 2). A _typed_ graph data model such as _labeled prop-_
_erty graphs_ [48] allows to distinguish different types of nodes (events, entities)
and relationships (directly-follows, correlated-to). We adopt labeled property


286 D. Fahland


graphs to construct a _knowledge graph_ [33] of a process from event data, to augment this graph with further knowledge, and to even perform process mining
analysis within a graph. Section 4.1 defines the generic data model of labeled
property graphs which we use in Sect. 4.2 to define _event knowledge graphs_ and
“directly-follows” paths in an event knowledge graph. In Sect. 4.3 we discuss how
to algorithmically construct an event knowledge graph from an event table.


**4.1** **Labeled Property Graphs**


A labeled property graph is a graph where each node and each directed edge
(called relationship) has a type, called _label_ . Further, each node and each relationship can carry attribute-value pairs as properties. For the remainder, we fix
a set _λN_ of node labels, a set _λR_ of relationship labels, and a set _Attr_ of property
names over a value domain _Val_ .


**Definition 7 (Labeled Property Graph).** _A_ labeled property graph _(LPG)_
_G_ = ( _N, R, λ,_ #) _is a graph with_ nodes _N_ _, and_ relationships _R with the following_
_properties:_


_1. Each node n ∈_ _N carries a_ label _λ_ ( _n_ ) _∈_ Λ _N_ _._
_2. Each relationship r ∈_ _R carries a label λ_ ( _r_ ) _∈_ Λ _R and defines a directed_ edge
_−→r_ = ( _nsource, ntarget_ ) _∈_ _N × N between two nodes._
_3. Any node n and relationship r can carry_ properties _as attribute-value pairs_
_via function_ # : ( _N ∪_ _R_ ) _× Attr_ ↛ _Val_


We write _x.a_ = _v_ for #( _x, a_ ) = _v_ and _x.a_ = _⊥_ if _a_ is undefined for _x_ . We
write _N_ _[ℓ]_ = _{n ∈_ _N | λ_ ( _n_ ) = _ℓ}_ and _R_ _[ℓ]_ = _{r ∈_ _R | λ_ ( _r_ ) = _ℓ}_ for the nodes
and relationships with label _ℓ_, respectively. We also write ( _n_ 1 _, n_ 2) _∈_ _R_ _[ℓ]_ if there
exists _r ∈_ _R_ _[ℓ]_ with _[−→]_ _r_ = ( _n_ 1 _, n_ 2).
Figure 4 shows an example of a labeled property graph, defining 5 nodes
with label _Event_, 3 nodes with label _Entity_, 7 relationships with label _corr_, and
4 relationships with label _df_ .
We here also provide some notation for standard operations on LPGs. Let
_G_ 1 = ( _N_ 1 _, R_ 1 _, λ_ 1 _,_ # [1] ) and _G_ 2 = ( _N_ 2 _, R_ 2 _, λ_ 2 _,_ # [2] ) be two LPGs.
_G_ 2 is a _sub-graph_ of _G_ 1, written _G_ 2 _⊆_ _G_ 1, iff _N_ 2 _⊆_ _N_ 1 _, R_ 2 _⊆_ _R_ 1 _, λ_ 2 =
_λ_ 1 _|N_ 2 _∪R_ 2 _,_ #2 = #1 _|N_ 2 _∪R_ 2. The _union_ of _G_ 1 and _G_ 2 is _G_ 1 _∪_ _G_ 2 = ( _N_ 1 _∪_ _N_ 2 _, R_ 1 _∪_
_R_ 2 _, λ_ 1 _∪_ _λ_ 2 _,_ # [1] _∪_ # [2] ) under the assumption that _λ_ 1( _x_ ) = _λ_ 2( _x_ ) and # [1] _a_ [(] _[x]_ [) =]
# [2] _a_ [(] _[x]_ [) for all] _[ a][ ∈]_ _[Attr]_ [ for any] _[ x][ ∈]_ [(] _[N]_ [1] _[∪]_ _[R]_ [1][)] _[ ∩]_ [(] _[N]_ [2] _[∪]_ _[R]_ [2][). For a set] **[ G]** [ =]
_{G_ 1 _, . . ., Gn}_ of graphs, we write [�] _G∈_ **G** _[G]_ [ =] _[ G]_ [1] _[ ∪]_ _[. . .][ ∪]_ _[G][n]_ [.]

Labeled property graphs are a native data structure for knowledge graphs [33]
and for a variety of _graph database systems_ [48] that provide data management
and query languages for reading and manipulating graphs [5].


**4.2** **Formal Definition of an Event Knowledge Graph**


To precisely model event data in an LPG, we have to restrict ourselves to specific
node labels for events and entities, and to specific relationship labels for correlation and directly-follows. Thereby, directly-follows relationships can only be


Event Knowledge Graphs 287


**Fig. 4.** Event knowledge graph of events _e_ 5 _, e_ 9 _, e_ 18 _, e_ 29 _, e_ 30 of Table 2.


defined between events that are correlated to the same entity and directly follow
each other from the viewpoint of that entity (Definition 6). This is formalized
in the model proposed by Esser [25] which we here call _event knowledge graph_ [4]


**Definition 8 (Event Knowledge Graph).** _An_ event knowledge graph _(or_
_just_ graph _) is an LPG G_ = ( _N, R, λ,_ #) _with node labels {Event, Entity} ⊆_
Λ _N and relationship labels {df, corr_ _} ⊆_ Λ _R indicating “directly-follows” and_
_“correlation” with the following properties._


_1. Every event node e ∈_ _N_ _[Event]_ _records an activity name e.act ̸_ = _⊥_ _and a times-_
_tamp e.time ̸_ = _⊥._
_2. Every entity node n ∈_ _N_ _[Entity]_ _has an entity type n.type ̸_ = _⊥._
_3. Every correlation relationship r ∈_ _R_ _[corr]_ _,_ _[−→]_ _r_ = ( _e, n_ ) _is defined from an event_
_node to an entity node, e ∈_ _N_ _[Event]_ _, n ∈_ _N_ _[Entity]_ _; we write n ∈_ _corr_ ( _e_ ) _and_
_e ∈_ _corr_ ( _n_ ) _as shorthand._
_4. Any directly-follows relationship df ∈_ _R_ _[df]_ _,_ _[−→]_ _df_ = ( _e_ 1 _, e_ 2) _is defined between_
_event nodes e_ 1 _, e_ 2 _∈_ _N_ _[Event]_ _and refers to a specific entity df .ent_ = _n ∈_
_N_ _[Entity]_ _such that_
_(a) e_ 1 _and e_ 2 _are correlated to entity n:_ ( _e_ 1 _, n_ ) _,_ ( _e_ 2 _, n_ ) _∈_ _R_ _[corr]_ _;_
_(b) e_ 1 _occurs before e_ 2 _: e_ 1 _.time < e_ 2 _.time; and_
_(c) there is no other event e_ _[′]_ _∈_ _N_ _[Event]_ _correlated to n,_ ( _e_ _[′]_ _, n_ ) _∈_ _R_ _[corr]_ _that_
_occurs in between e_ 1 _.time < e_ _[′]_ _.time < e_ 2 _.time_


4 The initially chosen term “event graph” [25, 38] which seems natural and shorter has
previously been coined for a model for discrete event simulation [49]. At the same
time, we will see that the proposed event _knowledge_ graph model allows to capture
more than just events.


288 D. Fahland


_We write df .type_ = _df .ent.type and_ ( _e_ 1 _, e_ 2) _∈_ _Rn_ _[df]_ _[.]_


Figure 4 shows an event knowledge graph for entities _I_ 1 _, I_ 2 _, P_ 1 of Table 2 and
their correlated events. Each _df_ relationship is defined between any two subsequent events correlated to the same entity. In the following, we omit the labels
and use dashed edges for _corr_ relationships, square nodes for _Event_ nodes, and
ellipses for _Entity_ nodes.
A path along _df_ -relationships corresponds to a trace in a classical event log. A
_path_ in a graph _G_ is a sequence **r** = _⟨r_ 1 _, . . ., rk⟩∈_ _R_ _[∗]_ of consecutive relationships,
i.e., the target node of _[−→]_ _ri_ = ( _ni−_ 1 _, ni_ ) is the start node of _r_ _[−−→]_ _i_ +1 = ( _ni, ni_ +1),
1 _≤_ _i < k_ .


**Definition 9 (df-path).** _Let G_ = ( _N, R, λ,_ #) _be an graph._
_A path_ **r** = _⟨r_ 1 _, . . ., rk⟩∈_ ( _R_ _[df]_ ) _[∗]_ _of df-relationships is a_ directly-follows
path (df-path) _iff all relationships are defined for the same entity, i.e., for all_
1 _≤_ _i < k, ri.ent_ = _ri_ +1 _.ent_ = _n; we also say_ **r** _is a df-path for entity n._
**r** _is_ maximal _iff there is no other df-relationship r ∈_ _R_ _[df]_ _so that ⟨r, r_ 1 _, . . ., rk⟩_
_or ⟨r_ 1 _, . . ., rk, r⟩_ _is also a df-path._

For a path **r** = _⟨r_ 1 _, . . ., rk⟩∈_ ( _R_ _[df]_ ) _[∗]_ _,_ _[−→]_ _ri_ = ( _ei−_ 1 _, ei_ ) we write just the sequence
of its nodes _⟨e_ 0 _, . . ., ek⟩_ in case the correlated entity is clear. The graph in
Fig. 4 defines three DF-paths: for _I_ 1: _⟨e_ 18 _, e_ 30 _⟩_, for _I_ 2: _⟨e_ 5 _, e_ 9 _, e_ 30 _⟩_, and for _P_ 1:
_⟨e_ 29 _, e_ 30 _⟩_ .
Event knowledge graphs can be efficiently stored and queried using graph
database systems [25]. This enables retrieving df-paths from graph databases
using query languages, such as Cypher [25,33]. While the nodes and relationships
of Definition 8 can also be encoded in RDF [11], the df-paths rely on attributes
of relationships (Definition 9) which are not supported by RDF but by LPGs.
Alternative formalizations of Definition 8 define just a partial order over
events [4,30,55,56] describing the local directly-follows relation wrt. various entities 6. Such a partial order view is equivalent to a family of df-paths [30, Cor. 4.9].
This equivalence allows to switch perspectives depending on the analysis task at
hand.


**4.3** **Obtaining an Event Knowledge Graph from an Event Table**


Event data is (currently) not recorded in the form of a graph, but for example
in the form of an event table _T_ with multiple entities (Definition 2). We obtain
an event knowledge graph from an event table _T_ in three steps.


1. Create an event node _e ∈_ _N_ _[Event]_ for each event record in the event table _T_ .
2. _Infer entities and correlation relationships_ from the event attributes: For each
unique entity identifier found at some event _e_, create an entity node _n_ and a
_corr_ relationship from _e_ to _n_ .
3. _Infer directly-follows relationships_ between all events _e_ 1 _, . . ., ek_ with a _corr_
relationship to the same entity node _n_ .


Event Knowledge Graphs 289


We now explain and define each step along the running example of Table 1. We
assume as input an event table _T_ = ( _E, Attr_ _,_ # _[T]_ _, ENT_ ) with multiple entities
as stated in Definition 2. The central requirement is that each unique entity type
_ent ∈_ _ENT ⊆_ _Attr_ is explicitly recorded as a dedicated attribute (column) of
_T_, and that each value in column _ent_ is an entity identifier.


**Step 1: Create Event Nodes.** We start by translating each event record in
event table _T_ into an event node in graph _G_ .


**Definition 10 (Event nodes from an event table).** _Let T_ = ( _E, Attr_ _,_
# _[T]_ _, ENT_ ) _be an event table with entities. The_ event nodes of _T are the graph_
_G_ _[Event]_ _T_ = ( _N_ _[Event]_ _, ∅, λ,_ # _[G]_ ) _with_


_1. N_ _[Event]_ = _E, i.e., each event of T becomes an event node, and_
_2._ # _[G]_ _a_ [(] _[e]_ [) = #] _a_ _[T]_ [(] _[e]_ [)] _[ for all][ a][ ∈]_ _[Attr, i.e., each event keeps all attributes from][ T]_
_as properties in G._


The resulting graph _G_ is a set of disconnected _Event_ nodes only.


**Step 2: Create Entity Nodes and Correlation Relationships.** Each
attribute of an event _e_ in _T_ that refers to an entity, e.g., _e.ent_ = _{n}_, is now a
property of the event node _e_ in _G_ . The basic idea is to “push out” this property:
we make each unique value _n_ an _Entity_ node _n_ and link _e_ to _n_ by a _corr_ relationship. The following definition constructs a small graph _G_ _[corr]_ ( _n_ ) that does
exactly this. We then use graph union _G ∪_ [�] _n_ _[G][corr]_ [(] _[n]_ [) to add them to] _[ G]_ [. The]

reason for doing so is that we can later calculate with various subgraphs.


**Definition 11 (Entity and correlation inference).** _Let G_ = ( _N, R, λ,_ # _[G]_ )
_be a graph and ENT be known entity types._
_Given a property name ent ∈_ _ENT, each property value e.ent we find on an_
_event node e ∈_ _N_ _[Event]_ _is an_ entity identifier of _ent_ in _G: Entities_ ( _ent, G_ ) = _{n |_
_∃e ∈_ _N_ _[Event]_ : _n ∈_ _e.ent}, see Definition 3._
_Let n ∈_ _Entities_ ( _ent, G_ ) _be an identifier of type ent ∈_ _ENT. The_ entity and
correlation inferred for _n_ in _G is the graph G_ _[corr]_ ( _n_ ) = ( _N_ _[′]_ _, R_ _[′]_ _, λ_ _[′]_ # _[′]_ ) _with:_


_1. entity node N_ _[′][Entity]_ = _{n} with_ # _[′]_ _type_ [(] _[n]_ [) =] _[ ent;]_
_2. event nodes N_ _[′][Event]_ = _{e ∈_ _N_ _[Event]_ _| n ∈_ _e.ent} with_ # _[′]_ ( _e_ ) = #( _e_ ) _for each_
_e ∈_ _N_ _[′][Event]_ _, i.e., each e is correlated to n, see Definition 4; and_
_3. correlation relationships re,n ∈_ _R_ _[′][corr]_ _,_ _[−→]_ _r e,n_ = ( _e, n_ ) _iff n ∈_ _e.ent._


We can infer entities and correlation on _any_ event knowledge graph, not just
the graph produced by Definition 10. This allows us to apply Definition 11
multiple times in any order. We can infer entities and correlation for an entity
type _ent_ by _G_ _[corr]_ ( _ent_ ) = [�] _n∈Entities_ ( _ent,G_ ) _[G][corr]_ [(] _[n]_ [). We can add the inferred]
entities and correlation to graph _G_ for all entity types _ENT_ by graph union
_G_ _∪_ [�] _ent∈ENT_ _[G][corr]_ [(] _[ent]_ [). In the result, each value] _[ n][ ∈]_ _[Entities]_ [(] _[ent][, T]_ [) becomes]

a new node _n_ with _n.type_ = _ent_ . Correspondingly, each pair ( _e, n_ ) _∈_ _corr ent,T_
becomes a new relationship of type _corr_ from _e_ to _n_ .


290 D. Fahland


**Fig. 5.** Event graph of events of Table 2 without directly-follows relationships.


For example, applying Definition 10 on the event table of Table 2 results
in the event nodes _e_ 1 _, . . ., e_ 11 _, e_ 18 _, . . ., e_ 21 _, e_ 27 _, . . ., e_ 32 shown in Fig. 5. Inferring
entities and correlation for entity types _Order_, _Supplier Order_, _Item_, _Invoice_,
and _Payment_ adds the entity nodes and correlation edges shown in Fig. 5. In
this graph we see that events _e_ 1 _, e_ 18 _, e_ 27 _, e_ 28 are the events correlated to entity
_O_ 1 of type _Order_ . Moreover, event _e_ 18 is correlated to two entities _Order O_ 1
and _Invoice I_ 1; event _e_ 27 is correlated to four entities _Order O_ 1, _Item X_ 1, _Item_
_X_ 2, and _Item Y_ 1.


**Step 3: Infer Local Directly-Follows Relations.** We now can infer the
local directly-follows relation (Definition 6) and materialize it as _df_ -relationships
between event nodes. Again, the basic idea is simple: for each entity node _n_
we retrieve all events _e_ 1 _, . . ., en_ with a _corr_ -relationship from _ei_ to _n_ . We order


Event Knowledge Graphs 291


_e_ 1 _, . . ., en_ by time and define a new _df_ -relationship _r_ from _ei_ to _ei_ +1; to remember
for which entity _r_ holds, we set _r.ent_ = _n_ .
As before, we do not add the _df_ -relationships directly to _G_ but construct a
separate graph _G_ _[df]_ ( _n_ ). We then add to _G_ by graph union _G ∪_ [�] _n_ _[G][df]_ [ (] _[n]_ [) which]

later allows us to calculate with graphs.


**Definition 12 (df inference).** _Let G_ = ( _N, R, λ,_ #) _be a graph. Let n ∈_
_N_ _[Entity]_ _. Let ⟨e_ 0 _, . . ., ek⟩_ _be the sequence of events {e_ 0 _, . . ., ek}_ = _corr_ ( _n_ ) _corre-_
_lated to n and sorted by time: ei−_ 1 _.time < ei.time,_ 1 _≤_ _i ≤_ _k._
_The_ df-relationships inferred for _n_ in _G_ _is_ _the_ _graph_ _G_ _[df]_ ( _n_ ) =
( _N_ _[′][Event]_ _, R_ _[′][df]_ _, λ_ _[′]_ _,_ # _[′]_ ) _with_


_1. event nodes N_ _[′][Event]_ = _{e_ 0 _, . . ., ek}, and_
_2. for each_ 1 _≤_ _i_ _≤_ _k one_ df _-relationship ri_ _∈_ _R_ _[′][df]_ _with_ _[−→]_ _ri_ =
( _ei−_ 1 _, ei_ ) _,_ # _[′]_ _ent_ [(] _[r][i]_ [) =] _[ n,]_ [ #] _[′]_ _type_ [(] _[r][i]_ [) = #] _[type]_ [(] _[n]_ [)] _[.]_


We can only infer a df-relationship for entity _n_ if _|corr_ ( _n_ ) _| >_ 1. Thus, for dfinference to have any effect, we have to have inferred the entity _n_ and correlation
using Definition 11 and there are at least two events correlated to _n_ . As for entity
and correlation inference, we can add the inferred df-relationships to _G_ by graph
union _G ∪_ [�] _n∈N_ _[Entity][ G][df]_ [ (] _[n]_ [).]

For example, if we infer the df-relationships for each entity in the graph of
Fig. 5 and add them to that graph, we obtain the graph shown in Fig. 6. Note
that we only show the _corr_ relationships to the first event of each entity for
readability. This graph explicitly models the events, entities, correlation, and
local directly-follows relations of all events in Table 2.


**Complete Procedure.** The following definition summarizes how to apply the
above three definitions to obtain an event knowledge graph of an event table _T_ .


**Definition 13 (Event knowledge graph of an event table).** _Let T_ =
( _E, Attr_ _,_ # _[T]_ _, ENT_ ) _be an event table with entities. The event table T defines_
_the_ graph _G_ = ( _N, R, λ,_ # _[G]_ ) of _T as follows:_


_1. Obtain the graph of event nodes G_ _[Event]_ _of T (Definition 10)._
_2. Infer the entities and correlation for each entity type ent ∈_ _ENT from G_ _[Event]_

_(Definition 11), i.e., G_ _[corr]_ = [�] _ent∈ENT_ _[G][corr]_ [(] _[ent]_ [)] _[ which results in the inter-]_
_mediate graph G_ _[Event]_ _∪_ _G_ _[corr]_ = ( _N_ _[Event]_ _∪_ _N_ _[Entity]_ _, R_ _[corr]_ _, λ,_ # _[G]_ ) _._
_3. Infer the df-relationships G_ _[df]_ = [�] _n∈N_ _[Entity][ G][df]_ [(] _[n]_ [)] _[ from][ G][Event][ ∪]_ _[G][corr][ (Def-]_

_inition 12) and return G_ = _G_ _[Event]_ _∪_ _G_ _[corr]_ _∪_ _G_ _[df]_ _._


From Definition 10–13 follows that the df-relationships in graph _G_ materialize
the local directly-follows relation of event table _T_ (Definition 6).


**Lemma 1.** _Let G_ = ( _N, R, λ,_ # _[G]_ ) _be the event knowledge graph of event table_
_T_ = ( _E, Attr_ _,_ # _[T]_ _, ENT_ ) _with entities. For any entity n ∈_ _Entities_ ( _ent, T_ ) _, ent ∈_
_ENT holds e_ 1 ⋖ _n,T e_ 2 _(e_ 2 _directly follows e_ 1 _from the perspective of n) iff_
( _e_ 1 _, e_ 2) _∈_ _Rn_ _[df]_ _[.]_


292 D. Fahland


**Fig. 6.** Event graph of events of Table 2 after inferring directly-follows relationships.


**4.4** **Inferring Entity Interactions**


The procedure of Definition 13 infers the local directly-follows relation for each
entity in the graph. However, there are also important behavioral dependencies
in the process _between_ related entities, such as _Orders_ and _Payments_, that are
not visible in the graph of Fig. 6.
We know from Fig. 1 that shipping _O_ 2 has to wait until the invoice of _O_ 1
has been cleared by the related payment _P_ 1, but the graph of Fig. 6 suggests
that _e_ 31 of _O_ 2 does not depend on _e_ 30 of _P_ 1 or any event of _O_ 1. This is because
there is no entity correlated to both _e_ 31 and _e_ 30 or any event of _O_ 1.
Our analysis in Sect. 2.3 found that _Orders_ are related to _Payments_ . We
can materialize this information in an event knowledge graph. We apply Definition 5 on all _Event_ nodes to obtain relation _R_ ( _ent_ 1 _,ent_ 2) between any two
(interesting) entity types _ent_ 1 _, ent_ 2. For each pair, ( _n_ 1 _, n_ 2) _∈_ _R_ ( _ent_ 1 _,ent_ 2)
we add a new relationship with label _related_ from entity node _n_ 1 to entity
node _n_ 2. Figure 7 illustrates the result of this step for ( _Order, Invoice_ ) and
( _Invoice, Payment_ ). We can infer transitive relationships by materializing paths
of _related_ -relationships (ignoring their directions) as new _related_ -relationships.


Event Knowledge Graphs 293


**Fig. 7.** Inferring relations between _Orders_, _Invoices_, and _Payments_ .


For example, we materialize _⟨O_ 1 _, I_ 1 _, P_ 1 _⟩∈_ ( _R_ _[related]_ ) _[∗]_ and _⟨O_ 2 _, I_ 2 _, P_ 1 _⟩∈_
( _R_ _[related]_ ) _[∗]_ as ( _O_ 1 _, P_ 1) _,_ ( _O_ 2 _, P_ 1) _∈_ _R_ _[related]_ in Fig. 7. These steps obviously
require domain knowledge to decide which potential relations to materialize,
esp. when considering paths over n-to-1 and 1-to-n relationships [41].
We then can infer the behavior between two related entities by adapting
entity and correlation inference (Definition 11) as follows [25]:


1. We _reify_ the relation between two entity types _ent_ 1 and _ent_ 2 into a new
_derived_ entity type ( _ent_ 1 _, ent_ 2). That is, we make each pair ( _n_ 1 _, n_ 2) _∈_ _R_ _[related]_

an entity node ( _n_ 1 _, n_ 2) _∈_ _N_ _[Entity]_ with ( _n_ 1 _, n_ 2) _.type_ = ( _ent_ 1 _, ent_ 2). For example, we create two entity nodes ( _O1_ _, P1_ ) _,_ ( _O2_ _, P1_ ) of type _(Order,Payment)_ .
For traceability, we add a new relationship _d ∈_ _R_ _[derived]_ with label _derived_
from entity ( _n_ 1 _, n_ 2) to _n_ 1 and to _n_ 2.
2. An event _e_ is then correlated to a derived entity ( _n_ 1 _, n_ 2) iff _e_ is correlated to
_n_ 1 or _n_ 2 (or both). Formally, we add a new correlation relationship from _e_
to ( _n_ 1 _, n_ 2) iff there is a correlation relationship _r ∈_ _R_ _[corr]_ from _e_ to _n_ 1 or _n_ 2,
i.e., _[−→]_ _r_ = ( _e, n_ 1) or _[−→]_ _r_ = ( _e, n_ 2).
3. Then we can treat any derived entity ( _n_ 1 _, n_ 2) just like any other entity and
infer the df-relationships for ( _n_ 1 _, n_ 2), which results in a new path describing
the interactions between _n_ 1 and _n_ 2.


Figure 8 shows the result of reifying the relation between _Order_ and _Pay-_
_ment_ entities of Fig. 7 into derived entities ( _O_ 1 _, P_ 1) and ( _O_ 2 _, P_ 1) of type
( _Order_ _, Payment_ ) and inferring the df-relationships for this entity type. We now
inferred df-paths from _Create Invoice_ in _O_ 1 ( _e_ 18) via _Clear Invoice_ in _P_ 1 ( _e_ 30)
to _Pack Shipment_ in _O_ 2 ( _e_ 31). [5]

Not all df-relationships for ( _O_ 1 _, P_ 1) and for ( _O_ 2 _, P_ 2) provide new information. For example in Fig. 8, ( _e_ 2 _, e_ 5) _∈_ _RO2_ _[df]_ [and (] _[e]_ [2] _[, e]_ [5][)] _[ ∈]_ _[R]_ ( _[df]_ _O2_ _,P1_ ) [run in]
parallel.
We say that a df-relationship ( _e_ 1 _, e_ 2) _∈_ _R_ ( _[df]_ _n_ 1 _,n_ 2) [of a derived entity (] _[n]_ [1] _[, n]_ [2][)]
_provides new information_ if there is not already an existing df-relationship


5 Our example here exploits that both orders of the same customer have invoices
cleared by the same payment. For the more general case, we would have to include
the customer in the data and infer the dependency via the customer entity.


294 D. Fahland


**Fig. 8.** Result of reifying the relation between _Order_ and _Invoice_ entities of Fig. 6 into a
derived entity of type ( _Order_ _, Invoice_ ) and inferring the df-relationships for this entity
type.


( _e_ 1 _, e_ 2) _∈_ _Rn_ _[df]_ 1 [or (] _[e]_ [1] _[, e]_ [2][)] _[ ∈]_ _[R]_ _n_ _[df]_ 2 [for one of the original entities] _[ n]_ [1] [or] _[ n]_ [2][. Thus, a]
df-relationship ( _e_ 1 _, e_ 2) provides new information if it actually describes an interaction from _n_ 1 to _n_ 2 or vice versa. In Fig. 8, ( _e_ 7 _, e_ 29), ( _e_ 28 _, e_ 29), and ( _e_ 30 _, e_ 31)
provide new information.
In principle we should keep only those _df_ -relationships of a derived entity
( _n_ 1 _, n_ 2) that provide new information. However, we can best study the interaction between _n_ 1 and _n_ 2 when all _df_ -relationships between _n_ 1 and _n_ 2 are part
of a path related to ( _n_ 1 _, n_ 2). We therefore keep all _df_ -relationships of ( _n_ 1 _, n_ 2)
that either provide new information or are between two _df_ -relationships of the
_df_ -path for ( _n_ 1 _, n_ 2) that do provide new information. In Fig. 8, for ( _O2_ _, P1_ ),
we keep ( _e_ 7 _, e_ 29) and ( _e_ 30 _, e_ 31) (provide new information) and also ( _e_ 29 _, e_ 30)
(between df-relationships that provide new information); for ( _O1_ _, P1_ ), we only
keep ( _e_ 28 _, e_ 29).
The complete graph for Table 1 after inferring the _df_ -relationships between
_Order_ and _Payment_ entities is shown in Fig. 9.


Event Knowledge Graphs 295


**4.5** **Creating Event Knowledge Graphs from Real-Life Data**


This method for constructing event knowledge graphs uses basic principles of
information inference: (1) construct entities and correlation based on the presence of an entity identifier or a relation; and (2) derive a local directly-follows
relation from the viewpoint of _each_ entity. Our definitions assume the data to
be accurate wrt. the real process, for instance, that entity identifiers and time
stamps are recorded correctly and precise; otherwise further preprocessing is
required [30,44,47].
All steps of the method can be implemented as a series of Cypher queries [6]

to construct event knowledge graphs in a graph database for our running example [28] as well as for various real-life datasets comprising single and multiple
event tables [24]; several event knowledge graphs of real-life processes are available [19–24]. A variant of event knowledge graphs, called _causal event graph_
that only models events but not the entities, can be extracted automatically
from relational databases [56].
In the following, we exploit the flexibility of LPGs that underly event
knowledge graphs to infer and materialize further behavioral information, going
beyond what event tables or event logs can describe.


**5** **Understanding Behavior over Multiple Entities**


The event knowledge graph of Fig. 9 we obtain with the method of Sect. 4 explicitly models what we observed earlier in Sect. 1: the behavior of the different entities forms a complex _network_ of synchronizing _df_ -paths. This section first discusses how to interpret df-paths (Sect. 5.1) and how they synchronize (Sect. 5.2).
We then discuss querying graphs through selection of entities and projection onto
events in Sect. 5.3; we apply these operations to understand why the retailer of
our example in Sect. 1 could not ship orders within the promised 6 days. We
finally introduce aggregation in Sect. 5.4 which we use to discover basic process
models directly within event knowledge graphs in Sect. 5.5.


**5.1** **How to Read Df-Paths in an Event Knowledge Graph**


We discuss how to read _df_ -paths over events based on running example of Fig. 6.
In a classical event log, each trace has a unique initial event and a unique
final event indicating the start and completion of a process execution. A graph
has multiple initial and final events – one per entity. Event _e_ is _starting_ or _ending_
event if it has no incoming or outgoing _df_ -relationship at all, e.g., _e_ 1 _, . . ., e_ 4, and
_e_ 32. Event _e_ is _starting_ or _ending_ event for entity _n_ if it has no incoming or
outgoing _df_ -relationship for _n_ . For example, _e_ 11 is the ending event of the _df_ path for _A_ but it still has an outgoing _df_ -relationship for _X_ 2. Some events are
starting/ending events for _multiple df_ -paths or entities. For example, _e_ 6 is the


6 [https://github.com/multi-dimensional-process-mining/eventgraph](https://github.com/multi-dimensional-process-mining/eventgraph_tutorial) ~~t~~ utorial.


296 D. Fahland


**Fig. 9.** Complete event knowledge graph of event table Table 1.
