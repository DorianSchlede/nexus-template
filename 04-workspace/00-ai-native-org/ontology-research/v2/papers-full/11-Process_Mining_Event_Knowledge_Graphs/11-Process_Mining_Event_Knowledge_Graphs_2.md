<!-- Source: 11-Process_Mining_Event_Knowledge_Graphs.pdf | Chunk 2/3 -->

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


starting event for _X_ 1 _, X_ 2 _, X_ 3 and _e_ 7 is the starting event for _Y_ 1 _, Y_ 2 while _e_ 27
is the ending event for _X_ 1 _, X_ 2 _, Y_ 1 and _e_ 31 is the ending event for _X_ 3 _, Y_ 2.
We call an event _intermediate_ in a df-path of an entity _n_ if it is not a starting or ending event in the df-path of _n_ . For example, _e_ 6 is an intermediate
event of _A_ .
In graph in Fig. 9 we see that the df-paths of entities of the same type are
rather similar to each other.


 - _O_ 1 and _O_ 2 both start with _Create Order_ and end with _Ship_ events with
_Create Invoice_ followed by _Pack Shipment_ in between.

 - _A_ and _B_ both start with _Place SO_ (eventually) followed by _Receive SO_,
ending with multiple _Unpack_ events. Specifically

 - Items _X_ 1 _, . . ., Y_ 2 start with _Receive SO_ followed by _Unpack_ and end with
_Pack Shipment_

 - _I_ 1 and _I_ 2 start with _Create Invoice_ and end with _Clear Invoice_


Note that the graph no longer shows any directly-follows relation from _Receive_
_SO_ to _Update SO_ that was falsely observed in Sect. 3. We can also analyze time


Event Knowledge Graphs 297


differences between events on the df-path. For example, in Sect. 1 we stated that
each Supplier Order is to be received within 3 days of placing the order.


 - On the df-path of _A_, event _e_ 6 ( _Receive SO_ for _A_, 4-5 10:15) is directly preceded
by _e_ 4 ( _Place SO_ for _A_, 1-5 11:25) which is within 3 days as required.

 - On the df-path of _B_, event _e_ 19 ( _Receive SO_ for _B_, 7-5 10:15) is directly
preceded by _e_ 7 ( _Update SO_ for _B_, 4-5 10:25) which is within 3 days, but 6
days since _e_ 4 ( _Place SO_ for _B_, 1-5 11:25). Thus, while the supplier delivered
within the required 3 days since _Update SO_, the update itself introduced a
3-day delay.


Thus, the graph now shows temporal information and delays for individual entities correctly, in contrast to the classical event log of Sect. 3.


**5.2** **How to Read Synchronization in a Graph**


Analyzing the df-paths for _O_ 1 and _O_ 2 also shows that none of the orders were
shipped within 6 days: _e_ 20 _.time−e_ 1 _.time >_ 7 _days_ and _e_ 32 _.time−e_ 2 _.time >_ 8 _days_ .
As completing the orders depends on other entities, i.e., the items, we now
analyze entity interactions through synchronization of df-paths.
A df-path **r** = _⟨e_ 0 _, . . ., ek⟩_ _goes through_ an event _e_ iff _e_ = _ei,_ 0 _≤_ _i ≤_ _k_ .
An event _e_ is _local_ to an entity _n_ if there is only one df-path of entity _n_ that
goes through _e_, e.g., _e_ 1 _, e_ 2 _, e_ 32. Two or more entities _n_ 1 _, . . ., nk synchronize_ in
a _shared_ event _e_ if two or more df-paths of _n_ 1 _, . . ., nk_ go through _e_, e.g., _e_ 7
synchronizes Supplier Order _B_ and Order _O_ 2 whereas _e_ 19 synchronizes Supplier
Order _B_ and Items _Y_ 1 and _Y_ 2.


**Reading Entity Creation and Updates.** We now discuss different interpretations of entities _n_ 1 _, . . ., nk synchronizing_ in a shared event.
Event _e intermediately synchronizes_ entities _n_ 1 _, . . ., nk_ when _e_ is an intermediate event for _n_ 1 _, . . ., nk_ . We can interpret an intermediate synchronization as
an update or state change of one or more entities that requires the involvement
of the other entities. For example, event _e_ 7 intermediately synchronizes Order
_O_ 2 and Supplier Order _B_ to update _B_ based on the information in _O_ 2; event _e_ 8
updates both Supplier Order _A_ and Item _X_ 3. Which entity changes state in _e_ 8
is not visible in the graph of Fig. 9.
An event _e_ that is intermediate for one entity _n_ but a starting event for entities _n_ 1 _, . . ., nk_ can be interpreted as _entity n “created” or “initiated” entities_
_n_ 1 _, . . ., nk_ . For example, Supplier Order _A_ created Items _X_ 1 _, X_ 2 _, X_ 3 in _e_ 6, and
Supplier Order _B_ created _I_ 2 in _e_ 5. Correspondingly, an event _e_ that is intermediate for entity _n_ and ending event for _n_ 1 _, . . ., nk_ is “closing” or “completing”
entities _n_ 1 _, . . ., nk_ . For example, Order _O_ 1 “completes” items _X_ 1 _, X_ 2 _, Y_ 1 in _e_ 27.
An event _e_ where multiple entities _n_ 1 _, . . ., nk_ of the same type synchronize is
a _batching_ event for _n_ 1 _, . . ., nk_ [36,42,55]. For example, _e_ 27 batches _X_ 1 _, X_ 2 _, Y_ 1,
_e_ 30 batches _I_ 1 _, I_ 2, and _e_ 31 batches _X_ 3 _, Y_ 2.


298 D. Fahland


However, we have to be careful with those interpretations as, both, the graph
and the data from which it was created may be incomplete. Entities that are “created” or “closed” may continue to exist both prior and after the data recorded,
e.g., all Items _X_ 1 _, . . ., Y_ 2 certainly exist prior to this process and after it, thus _e_ 6
and _e_ 27 only show when these items entered the visibility or scope of our observations. Likewise, a starting event _e_ for an entity _n_ that is _not_ an intermediate
event for another entity _n_ 2 does _not_ describe how _n_ was created. For example,
_e_ 1 _, . . ., e_ 4 do not explain how _O_ 1 _, O_ 2 _, A, B_ were created. This is because our
graph of Fig. 9 is incomplete as we did _not_ (a) infer the _Resource_ entity and
the corresponding _df_ -relationships from Table 1 and (b) we only recorded data
in a limited time window. A helpful principle to check for incompleteness in
distributed behavior is due to C.A. Petri [27]: most events happens due to a
synchronous interaction of two or more entities, and most physical entities are
never created from nothing and never disappear into nothing.


**Reading Entity Interactions.** Events and df-paths describe different modes
of interaction. An event _e_ where the df-paths of _n_ 1 and _n_ 2 synchronize is a
_synchronous interaction_ . A df-path for entity _n_ describes an _asynchronous inter-_
_action_ between _n_ 1 and _n_ 2 if _n_ synchronizes both with _n_ 1 and _n_ 2 in different
events. If the df-path for _n_ has only 2 events _⟨e_ 1 _, e_ 2 _⟩_ then we can interpret entity
_n_ as _message_ from _n_ 1 to _n_ 2. We can interpret an event _e_ that is the ending event
of entity _n_ 1 and the starting event of entity _n_ 2 as a _handover_ from _n_ 1 to _n_ 2. In
Fig. 9, _e_ 7 is a synchronous interaction of _O_ 2 and _B_, the df-path of _Y_ 1 describes
an asynchronous interaction from _B_ to _O_ 2, and _e_ 28 is a handover from _O_ 1 to
( _O_ 1 _, P_ 1).
If two entities _n_ 1 and _n_ 2 never synchronize in a shared event but there is at
least one asynchronous interaction between _n_ 1 and _n_ 2, then _n_ 1 and _n_ 2 _interact_
_asynchronously_ . If all asynchronous interactions, i.e., df-paths, only go from _n_ 1
to _n_ 2, then the interaction is _one-directional_, and it is _bi-directional_ otherwise.
In Fig. 9, _A_ and _O_ 1 interact asynchronously and one-directional (from _A_ to _O_ 1
via _X_ 1), _O_ 2 and _P_ 1 interact asynchronously and bi-directional (via ( _O_ 2 _, P_ 1)).
_n_ 1 and _n_ 2 _interact indirectly_ if for any two events _e_ 1 of _n_ 1 and _e_ 2 of _n_ 2
the shortest df-path from _e_ 1 to _e_ 2 involves df-relationships from multiple other
entities. For example, _O_ 1 interacts indirectly with _O_ 2 via ( _O_ 1 _, P_ 1) and ( _O_ 2 _, P_ 2)
(df-path _⟨e_ 28 _, e_ 29 _, e_ 30 _, e_ 31 _⟩_ ).
Finally, _n_ 1 and _n_ 2 _do not interact_ if there is no df-path from _n_ 1 to _n_ 2, or
vice versa. For example, _A_ and _B_ do not interact. Note, however, that (indirect)
interactions via other entities as well as non-interaction are subject to which
entities have been included in the construction of the graph and which relations
have been reified into derived entities.


**Reading Event Dependencies and Delays.** We observed in Sect. 5.1 that
neither _O_ 1 nor _O_ 2 was shipped within 6 days as required in Sect. 1. We now
want to analyze which entities, that synchronized with _O_ 1 and _O_ 2, delayed
either order to be shipped on time.


Event Knowledge Graphs 299


Consider an event _e_ that synchronizes the df-paths of multiple entities
_n_ 1 _, . . ., nk_ . Event _e directly depends on_ any event _ei_ that directly precedes _e_
via an incoming df-relationship ( _ei, e_ ) _∈_ _Rn_ _[df]_ _i_ _[,]_ [ 1] _[ ≤]_ _[i][ ≤]_ _[k]_ [ along entity] _[ n][i]_ [. We call]
_e.time −_ _ei.time_ the _delay_ between _ei_ and _e_ .
Suppose _e_ 1 _, . . ., ek_ are sorted on their delay to _e_ . Event _e_ 1 was the first event
that directly preceded _e_, i.e., _e_ could not have occurred earlier than _e_ 1. The
entity _n_ 1, for which ( _e_ 1 _, e_ ) _∈_ _Rn_ _[df]_ 1 [was observed, was the first entity ready to]
synchronize in _e_ . We can interpret that each later event _ei, i >_ 1 _delayed_ the
synchronization in _e_ as entity _ni_ became ready to synchronize later than _n_ 1 did,
with _ek_ and _nk_ delaying _e_ the most.
For example in Fig, 9, _e_ 31 ( _Pack Shipment_ for _O_ 2) depends on _e_ 7 _, e_ 8 _, e_ 21 _, e_ 30
along entities _O_ 2, _X_ 3, _Y_ 2, and ( _O_ 2 _, P_ 1) with delays of 3 days, 3 days, 2 days,
and 3 h, respectively. While _O_ 2 was first ready to synchronize in _e_ 31 after _e_ 7
( _Update Order_ ); _e_ 31 was delayed most by _e_ 30 ( _Clear Invoice_ for _I_ 1 _, I_ 2) along
( _O_ 2 _, P_ 1).
For a given event _e_, we can build the set _delay_ _[∗]_ ( _e_ ) of transitive predecessors
that delayed _e_ the most, by first adding event _e_ _[′]_ that delayed _e_ most, then
adding event _e_ _[′′]_ that delayed _e_ _[′]_ most, etc. For example in Fig. 9, _delay_ _[∗]_ ( _e_ 32) =
_{e_ 31 _, e_ 30 _, e_ 29 _, e_ 28 _, e_ 27 _, e_ 20 _, e_ 19 _, e_ 7 _, e_ 5 _, e_ 2 _}_ .
Comprehending such subsets of events (and the dynamics they describe) is
rather difficult. We use graph querying to reduce a graph to a subgraph of
interesting events.


**5.3** **Basic Querying Operations**


Similarly to classical event logs, we can also subset (or filter) event knowledge
graphs for a more focused analysis. Recall that we have two basic operations to
sub-setting classical event logs: selection (include only a subset of the cases with
specific properties but keep all events in a case) and projection (keep all cases
but keep only a subset of events with specific properties). The same operations
can be applied on event knowledge graphs.
We _select_ a subset of entities, but keep all event nodes correlated to the
entities and all directly-follows relations between the events of these entities.
Formally, given a graph _G_, we select entity nodes _Nsel_ _[Entity]_ _⊆_ _N_ _[Entity]_ from _G_ by
(1) removing all entity nodes _N_ _[Entity]_ _\Nsel_ _[Entity]_ and all adjacent _corr_ relationships,
then (2) removing all event nodes _e ∈_ _N_ _[Event]_ which no longer have any _corr_
relationships (because none of their entities was selected) and the adjacent _df_
relationships.
We _project_ on a subset of events by keeping all entity nodes but only the
selected event nodes; as this may interrupt df-paths (if an intermediate event
gets removed) we have to recompute all df-relationships. Formally, given a graph
_G_, we project onto event nodes _Nproj_ _[Event]_ _⊆_ _N_ _[Event]_ from _G_ by (1) removing all
_df_ -relationships from _G_, (2) removing all event nodes _N_ _[Event]_ _\_ _Nproj_ _[Event]_ [, and then]
(3) doing df-inference on the resulting graph (Definition 12).
The criteria by which we select events and entities can consider properties of
events and entities but also relations to other event and entity nodes, and even


300 D. Fahland


**Fig. 10.** Projection of Fig. 9 onto events that delayed most _e_ 28 and _e_ 32 and are not
_Unpack_ events. Bold df-relationships indicate which preceding event delayed an event
the most.


more complex paths or sub-graphs. For example, to understand what caused
delays in shipping order _O_ 1 ( _e_ 28) and _O_ 2 ( _e_ 32) while also removing unnecessary
events, we can project the graph of Fig. 9 onto the events the (1) delayed either
shipment the most (2) but without _Unpack_ events. Formally, we project onto
( _delay_ _[∗]_ ( _e_ 32) _∪_ _delay_ _[∗]_ ( _e_ 28)) _\ {e ∈_ _N_ _[Event]_ _| e.act_ = _Unpack}_ . Figure 10 shows the
resulting graph. Note the new df-relationships ( _e_ 5 _, e_ 30) _∈_ _RI_ _[df]_ 2 [, (] _[e]_ [19] _[, e]_ [27][)] _[ ∈]_ _[R]_ _Y_ _[df]_ 1 [,]
( _e_ 19 _, e_ 31) _∈_ _RY_ _[df]_ 2 [, obtained after doing df-inference over the remaining events.]
In Fig. 10, we observe the following: _Pack Shipment_ for _O_ 1 ( _e_ 27) was delayed
by Item _Y_ 1 which was only ready for _e_ 27 after _Receive SO_ ( _e_ 19). In turn, _e_ 19 was
delayed by Supplier Order _B_ with _Update SO_ ( _e_ 7), which we already identified
as cause for not receiving all items within 3 days in Sect. 5.1. _Pack Shipment_ for
_O_ 2 ( _e_ 31) was delayed by entity ( _O_ 2 _, P_ 1), that means, by _Clear Invoice_ ( _e_ 30) for
the Payment _P_ 1 related to _O_ 2. _Receive Payment_ for _P_ 1 ( _e_ 29) was delayed by
( _O_ 1 _, P_ 1), that means, by _Ship_ ( _e_ 28) for the related order _O_ 1.
Altogether, this allows us to pinpoint the bottlenecks in the process: _Update_
_SO_ delayed delivery of items _Y_ 1 _, Y_ 2 needed for both _O_ 1 and _O_ 2, causing a
delay in shipment for _O_ 1. The fact that the customer only paid and cleared
both invoice _I_ 1 _, I_ 2 after _O_ 1 was shipped delayed shipping _O_ 2 together with the
retailer’s policies.


Event Knowledge Graphs 301


**5.4** **Aggregating Events and Df-Relationships**


Selection and projection allow to subset the data. Aggregation allows to materialize new nodes and relationships in the data. While the aggregation principle
we explain here can be applied for many purposes, we specifically discuss it for


 - aggregating sets of events into activities (or event classes), and

 - aggregating df-relationships between events into corresponding relationships
between activities.


The basic aggregation principle from sets of events to activities is formally identical to creating entity nodes from event properties as given in Definition 11.


 - We select one event property that identifies a unique concept shared by many
events, in this case the property _Activity_ .

 - For each value _c ∈{e.Activity | e ∈_ _N_ _[Event]_ _}_ of the _Activity_ property that we
find among the events in the graph, we create a new node _c_ with label _Class_
(representing the class of events with the same _Activity_ property).

 - We add an _observes_ relationship from each event _e_ to the _Class_ node _c ∈_
_N_ _[Class]_ if _e.Activity_ = _c_ .

 - We can also materialize how many events observe class _c ∈_ _N_ _[Class]_ in property
_c.count_ .


The yellow rounded rectangles in Fig. 11 represent the _Class_ nodes of the
events for Orders _O_ 1, _O_ 2 and Supplier Orders _A_, _B_ . The dashed edges represent
the _observes_ relationship, e.g., _e_ 2 and _e_ 1 both observe _Create Order_ .
We then can aggregate the df-relationships in a straight-forward way: for any
two class nodes _c_ 1 and _c_ 2 we add a _df_ relationship of type _ent_ from _c_ 1 to _c_ 2 if
there are corresponding events _e_ 1 and _e_ 2 that directly follow each other for _ent_,
i.e., if ( _e_ 1 _, c_ 1) _,_ ( _e_ 2 _, c_ 2) _∈_ _R_ _[observes]_ and ( _e_ 1 _, e_ 2) _∈_ _Rn_ _[df][, n.][type]_ [ =] _[ ent]_ [. We can also]
count how many df-relationships occur between events of _c_ 1 and _c_ 2 and add this
as property to this relationship.
For example, in Fig. 11, we observe two df-relationships from _Create Order_ to
_Create Invoice_ ( _e_ 1 _, e_ 18) and ( _e_ 2 _, e_ 5). Note, that this definition also creates selfloops around event classes, e.g., we observe three df-relationships from _Unpack_
to _Unpack_ . Also note that, as for events nodes, a class node can be part of _df_ relationships for multiple different entity types, e.g., _Update SO_ is an activity
that occurs for _Order_ and _Supplier Order_ .


**5.5** **Discovering Multi-entity Process Models**


The aggregation operation of Sect. 5.4 essentially constructs a directly-follows
graph. The key difference to the directly-follows graph of classical event logs is
that each df-relationship between _Class_ nodes is specific to one entity type. Thus,
it respects the idea of the local directly-follows relation laid out in Definition 6.
The resulting graph is a _multi-entity directly-follows graph_, also called _multi-_
_viewpoint DFG_ [4] or _artifact-centric model_ [41].


302 D. Fahland


**Fig. 11.** Aggregating events to event classes and lifting the directly-follows relationships


Applying the event and df-aggregation of Sect. 5.4 to the graph of Fig. 9
results in the multi-entity DFG shown in Fig. 12. While the graph as a whole is
rather complex, each edge is grounded in temporal relations of a specific entity
type. Moreover, we can see that the behavior for each entity type is rather simple.
Event and df-aggregation can be implemented as simple, scalable queries [7]

over standard graph databases, enabling efficient in-database process discovery [25,34]; the queries can be extended to filter based on frequencies or properties of the event knowledge graph [28].
An alternative representation of the multi-entity DFG is the proclet
model [26] shown in Fig. 13. It is constructed by not creating a global _Class_
node per unique _e.Activity_ value in the data, but by creating a _Class_ node per
unique pair of activity name and entity type ( _e.Activity, ent_ ). As a result, we
see for example two _Create Invoice_ nodes, one for _Order_ and one for _Invoice_ .
Two class nodes of the same name are linked by a _cardinality_ relationship that
indicates how many entities are involved in an event of this class. For example,
in every _Create Invoice_ events, one _Order_ and one _Invoice_ is involved, while in
every _Receive SO_ event one _Supplier Order_ and 2-3 _Items_ are involved.


7 [https://github.com/multi-dimensional-process-mining/eventgraph](https://github.com/multi-dimensional-process-mining/eventgraph_tutorial) ~~t~~ utorial.


Event Knowledge Graphs 303


**Fig. 12.** Multi-Entity Directly-Follows-Graph of the running example obtained by
aggregating the graph of Fig. 9


**Fig. 13.** Synchronous proclet model of the running example obtained by aggregating
the graph of Fig. 9


304 D. Fahland


**6** **Beyond Control-Flow: Multi-dimensional Process**
**Analysis**


So far, we analyzed the entities that are created and updated by the process based
on the event data in Table 1. We now turn our attention to the _organizational_
_entities_ that actually make the process happen: the workers and supporting
systems often called _resources_, and the work itself that is being carried out. Along
the way, we showcase how flexible event knowledge graphs are. We integrate new
events from a different data source in Sect. 6.1. We then enrich event knowledge
graphs with df-paths over _activities_ Sect. 6.2, which reveals _queues_ . Enriching
event knowledge graphs with df-paths over _workers_ in Sect. 6.3 reveals patterns
of how individual workers perform larger scale _tasks_ . Finally, we show how to
infer new information from (enriched) event knowledge graphs in Sect. 6.4.


**6.1** **Extending Event Knowledge Graphs with New Events**



The process is supported by an automated
warehouse (see Fig. 1). Figure 14 shows
events of how the _Items_ were handled by the
warehouse. To analyze how the warehouse
influenced the process, we have to combine
these events with the events from Table 1.
Luckily, we can avoid combining both tables
into one joint event table and repeating the
entire procedure of Sect. 4.3. We can simply
_locally update_ an existing graph with new
events as follows. We choose to start from
the graph of Fig. 6.





1. Import Fig. 14 into new event nodes
(Definition 10). This results in new
event nodes _e_ 12 _, . . ., e_ 17 _, e_ 22 _, . . ., e_ 26 _,_ e32 Retrieve 09-05 09:45 Y2
_e_ 31 _, e_ 32.
2. Infer entities and correlation from the

**Fig. 14.** Warehouse events

new event nodes (Definition 11). This
results in the already existing entity
nodes _X_ 1 _, . . ., Y_ 2.
3. For each entity node _n_ inferred in step 2, remove every df-relationship
_r ∈_ _R_ _[df]_ _, r.ent_ = _n_, and then infer the df-relationships for _n_ (Definition 12)
now including the new imported events.


The resulting graph is shown in Fig. 15. Note that we can obtained the original Fig. 6 again by selection of the original entities and projection onto the
original events (see Sect. 5.3).



**Fig. 14.** Warehouse events


Event Knowledge Graphs 305


**Fig. 15.** Event graph after extending Fig. 6 with Fig. 14 (new events highlighted).


**6.2** **Adding Activities as Entities Reveals Queues**


We defined entity inference in Definition 10 for the entity type attributes of the
source event table. However, Definition 10 can be applied on _any_ property of an
event node.
For example, if we pick the _Activity_ property as “entity identifier”, we infer
entities such as _Receive SO_, _Unpack_, _Scan_, _Store_, _Retrieve_, _Pack Shipment_ . These
are not entities handled by the process. No, these entities are the actual building
blocks of the process. For example, each _Item_ handled has to “pass through” each
of these entities to be completely processed. We can visualize how other entities
“pass through” activities by inferring in the graph of Fig. 15 the entity nodes for
_Activity_ and their df-paths [8] . Figure 16 shows the resulting graph (limited to a
subset of events for readability).
We can see that the (red) _Activity_ df-paths “go across” all the existing dfpaths while the (green) _Item_ df-paths traverse the different _Activity_ df-paths
largely “in parallel”. Whenever an _Item_ df-path synchronizes with an _Activity_


8 Note that the _Entity_ nodes identified by the activity property are _semantically dif-_
_ferent_ from the _Class_ nodes identified by the activity property that we obtained
in Sect. 5.4. The _Class_ nodes semantically aggregate the existing _df_ relationships
between events observed for other entities to _df_ relationships between _Class_ nodes.
_Entity_ nodes of the entity type _Activity_ instead derive new df relationships in addition to existing df relationships for other entities.


306 D. Fahland


**Fig. 16.** Inferring _Activity_ as entities in the graph of Fig. 15 reveals _Queues_ . (Color
figure online)


df-path in an event, the item is being worked on. Thus, we can interpret each
_Activity_ entity _A_ as an abstract “work station” and its events as the work that
is being performed there.
The space between two work stations _A_ and _B_ is a _queue A_ : _B_, i.e., the space
where _Items_ after being worked on at _A_ wait until being worked on at _B_ . We can see
in the graph in Fig. 16 that the _Items_ do not always leave a queue in the same order
they entered it: _X_ 1 entered _Unpack:Scan_ after _X_ 3 ( _e_ 10 follows _e_ 8 in the df-path
for _Unpack_ ) but leaves before _X_ 3 ( _e_ 12 precedes _e_ 16 in the df-path for _Scan_ ).
We can better understand this behavior by changing the layout of the graph
in Fig. 16. We select from Fig. 16 only _Item_ and _Activity_ entities. Setting the
x-coordinate of each event by its time property and the y-coordinate by its
_Activity_ entity results in the graph in Fig. 17, which is called the _Performance_
_Spectrum_ [16].
The Performance Spectrum shows us that batching happens at _Receive SO_
and _Pack Shipment_ (diverging/converging _Item_ df-paths), that _Scan:Store_ and
_Store:Retrieve_ are being FIFO queues, that _Unpack:Scan_ is _not_ a FIFO queue,
e.g., _X_ 3 is overtaken by _X_ 1 _, X_ 2 and _Y_ 1 is overtaken by _Y_ 2.
We already identified in Sect. 5 reasons why Order _O_ 2 was not shipped within
the 6 days promised by the retailed (see Sect. 1). We now can also clarify the
reasons for _O_ 1. Figure 17 shows that although the second supplier order _B_ with
the required item _Y_ 1 was received on _7-5_ (the 6th day of _O_ 1), order _O_ 1 was only
packed _after_ the _15:00_ pick-up time. The non-FIFO handling in _Unpack:Scan_
seems to be at fault. We observe


Event Knowledge Graphs 307



Receive SO


Unpack


Scan


Store


Retrieve


Pack Shipment




|Col1|Col2|Col3|Col4|Col5|Col6|Col7|Col8|Col9|Col10|Col11|Col12|Col13|Col14|Col15|Col16|Col17|Col18|Col19|Col20|Col21|Col22|Col23|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
||||||||||||||||||||||||
||||||||||||||||||||||||
||||||||||||||||||||||||
||_1hr_||||||||||||||||||||||
||||||||||||||||||||||||



_4-5 10:00_ _4-5 15:00_ _7-5 10:00_ _7-5_ _15:00_ _9-5 10:00_



_9-5_ _15:00_



**Fig. 17.** Sub-graph of Fig. 16 for _Activity_ entities and _Item_ entities, with event coordinates defined by _Activity_ (y-axis) and _time_ (x-axis), results in the _Performance Spectrum_ .


1. a consistent _2-h minimum waiting time_ between two subsequent _Scan_ activities (along its _Activity_ df-path) causing _Y_ 1 to finish _Scan_ after _Y_ 2 at _7-5_
_15:00_, and
2. a consistent _2-h minimum soujourn time_ for the last _Item_ reaching _Pack_
_Shipment_, i.e., Pack Shipment for _X_ 1 _, X_ 2 _, Y_ 1 completes at _7-5 17:00_ .


Thus, if _Unpack:Scan_ had followed a strict FIFO policy, _Y_ 1 could have completed its _Scan_ activity at _7-5 12:45_ ; the subsequent _Pack Shipment_ event over
_X_ 1 _, X_ 2 _, Y_ 1 could have completed at _7-5 14:45_ just before the scheduled pick-up
at _7-5 15:00_ .
The Performance Spectrum reveals further, far more involved patterns of
process performance over time than just batching and FIFO [16]. It is also implemented as a visual analytics tool over event data [15] and in combination with
process models [54]. Mining performance patterns from it [36] allows to engineer so called inter-case features for improving the accuracy of remaining time
prediction [37].


**6.3** **Adding Actors as Entities Reveals Complex Tasks**


We found in Sect. 6.2 that _Activity_ entities describe the abstract “work stations”
where other entities are being worked on. Workers are performing this actual
work. Often called “resources” in process management literature [18], we prefer
the term _Actor_ used in organizations research [32], as each actor follows its own
behavior. To study actor behavior in the graph of Fig. 6, we only have to (1)
infer the _Actor_ entities from the event nodes (see Table 1), and (2) infer each
actor’s df-path. Figure 18 shows the resulting graph.
We can see actors _R_ 1 _, R_ 2 _, R_ 3 working “intertwined” in the same part of the
process. In contrast, _R_ 4 and _R_ 5 work more separated from the other actors.
Also, the actor df-paths actors show very different characteristics. The df-path
_⟨e_ 1 _, e_ 2 _, e_ 3 _, e_ 7 _⟩_ of _R_ 1 synchronizes with any other entity only in one event, and


308 D. Fahland


**Fig. 18.** Adding actors ( _Resource_ ) entities to the event knowledge graph reveals task
execution patterns


then moves on to the next entity _O_ 1, _O_ 2, _A_, _B_, always performing just a single
activity on each. In contrast, the df-path of _R_ 4 synchronizes over multiple subsequent events with the same entity, i.e., _e_ 27 _, e_ 28 in _O_ 1 and _e_ 31 _, e_ 32 in _O_ 2, meaning
_R_ 4 always performs a “unit of work” that consists of two subsequent activities.
Such a larger unit of work of multiple related activities is called a _task_ [32,38].
A _task instance_ of an actor _R_ working on an entity _X_ materializes in an event
knowledge graph as a specific subgraph over event nodes _e_ 1 _, . . ., ek_ : (1) the dfpaths of _R_ and _X_ both meet in _e_ 1, (2) diverge in _ek_, (3) synchronize in each
event node _e_ 1 _, . . ., ek_, and (4) at least one of their df-paths has no other event in
between _e_ 1 _, . . ., ek_ [38]. The grey rectangles highlighted in Fig. 18 shows several
task instance. The task instances themselves and the way they are ordered in
the graph reveal unique characteristics of performing work.


Event Knowledge Graphs 309


 - Actor _R_ 1 only performs a series of singleton tasks _ti_ 1 _, ti_ 2 _, ti_ 3 _, ti_ 4. The df-path
of _R_ 1 describes that _Supplier Order A_ has been placed only after both _Orders_
_O_ 1 and _O_ 2 were created.

 - Actor _R_ 4 performs two instances _ti_ 27 and _ti_ 31 of the same task (first _Pack_
_Shipment_ then _Ship_ ) directly after each other on two different _Orders_ .

 - Actor _R_ 2 also performs two instances _ti_ 6 and _ti_ 19 of the same task (first
_Receive_ then repeatedly _Unpack_ ) directly after each other; however _R_ 2 interrupts _ti_ 6 on _A_ to perform _ti_ 9 ( _Update Invoice_ ) on _I_ 2.


Further, more complex types of task instances can be identified in event knowledge graphs [38]. The df-relationships between task instances also reveal patterns
of how work is handed over between actors. For example _R_ 1 hands work over to
_R_ 2 in all _Supplier Orders_, to _R_ 3 in all _Orders_, and to _R_ 4 in _O_ 2; _R_ 2 hands work
over to _R_ 4 in all _Items_ and to _R_ 5 in _I_ 2. Such patterns are studied in the area
of routines research [32].
We clearly can see some undesirable behavior in how actors collaborate over
the different entities.


 - _R_ 1 created both _Orders O_ 1 and _O_ 2 but only placed _Supplier Order A_ .
Instead, _R_ 3 placed _B_ and we cannot observe a handover from _R_ 1 to _R_ 3; this
lack of collaboration may have led to _R_ 3 placing a wrongly _Supplier Order_
_B_ (with only one item _Y_ ). The _Update SO_ by _R_ 1 remedies the problem but
caused to the delay in delivering _Y_ 1 we identified in Sect. 5. The problem may
have been avoided by _R_ 1 completing the “larger task” _⟨e_ 1 _, . . ., e_ 4 _⟩_ alone.

 - _R_ 2 is _interrupting_ their work on unpacking _Supplier Order A_ after _X_ 3 ( _e_ 8)
to _Update Invoice I_ 2 before continuing on unpacking _X_ 1 ( _e_ 10). This “context
switch” between handling _Items_ and _Invoice_ results in a longer delay between
two subsequent _Unpack_ events (30mins) than usual (15mins), which we can
directly see in the Performance Spectrum in Fig. 17. The longer delay is a
risk to packing shipments on time as we analyzed in Sect. 6.2. The risk could
be reduced by ensuring that _R_ 2 is not interrupting their task; _R_ 3 could have
updated the invoice instead.


The process model shown in Fig. 21, and further explained in Sect. 7, describes
for each actor behavioral routines that could avoid undesirable behavior.


**6.4** **Inference in Event Knowledge Graphs with Multiple Layers**


Our discussions so far focused on constructing, understanding, and finding patterns in graphs over _Entity_ and _Event_ nodes and the _df_ and _corr_ relationships.
As the model of event knowledge graphs (Definition 8) is based on labeled property graphs (Definition 7), we can extend an event knowledge graph with further
node and relationship types, to describe more knowledge about the process. We
already did that in Sect. 5.4 when aggregating multiple _Event_ nodes of the same
activity to a new node with label _Class_ . In the following we expand on this idea
by an example. We do so in the style of a process mining analyst applying all


310 D. Fahland


the concepts of the previous sections as data processing operations. In fact all
steps shown here can be realized through Cypher queries over a graph database.
Suppose we want to create a concise summary of how actors organize the
work of handling _Supplier Orders_, based on the graph with actor df-paths shown
in Fig. 18. The actors correlated to _Supplier Order_ events are _R_ 1 _, R_ 2 _, R_ 3. We
select entities _A_ and _B_ and _R_ 1 _, R_ 2 _, R_ 3 and then project onto events of a _Supplier_
_Order_ or between two _Supplier Order_ events (to keep _e_ 9). The resulting graph
is shown in Fig. 19 as “Event Entity Layer”.


**Fig. 19.** An event knowledge graph extended with additional layers into a “process
knowledge graph”.


Next, we aggregate the event layer into a new “Task Instance Layer”.


1. For each task instances, i.e., each subgraph of an _Actor_ df-path and an _Sup-_
_plier Order_ df-path synchronizing on consecutive events as defined in Sect. 6.3,


Event Knowledge Graphs 311


we extend the graph with a new node with label _TaskInstance_, resulting in the
nodes _ti_ 3 _, ti_ 4 _, ti_ 6 _, ti_ 7 _, ti_ 9 _, ti_ 21 shown in the “Task Instance Layer” of Fig. 19.
2. We add a new _contains_ relationship ( _ti, e_ ) _∈_ _R_ _[contains]_ from each _TaskIn-_
_stance_ node _ti_ to each _Event_ node _e_ that is part of the task instance, e.g.,
( _ti_ 9 _, e_ 19) _,_ ( _ti_ 9 _, e_ 20) _,_ ( _ti_ 9 _, e_ 21) _∈_ _R_ _[contains]_ in Fig. 19. This connects the nodes in
both layers.
3. Each _ti ∈_ _N_ _[TaskInstance]_ gets the property _ti.Task_ by concatenating the _Activ-_
_ity_ values of the event nodes it contains along their df-path (abstracting
repetitions with a Kleene star), e.g., _ti_ 6 _.Task_ = _⟨Receive SO, Unpack_ _[∗]_ _⟩_ .
4. We then lift the df-relationships from _Event_ nodes to _TaskInstance_ nodes.
For each df-relationship ( _e, e_ _[′]_ ) _∈_ _R_ _[df]_ between events _e, e_ _[′]_ contained in different task instances _ti ̸_ = _ti_ _[′]_ _,_ ( _ti, e_ ) _,_ ( _ti_ _[′]_ _, e_ _[′]_ ) _∈_ _R_ _[contains]_, we create a new dfrelationship ( _ti, ti_ _[′]_ ) _∈_ _R_ _[df]_ between task instance nodes _ti_ and _ti_ _[′]_ (and copy
the properties of the df relationship).


The resulting “Task Instance Layer” in Fig. 19 represents the “Event Entity
Layer” at the aggregation level of task executions instead of activity executions.


5. To understand which tasks are performed and how often, we aggregate _Task-_
_Instance_ nodes into _Task_ nodes by their _Task_ property (see Sect. 5.4).


The resulting “Task Layer” in Fig. 19 shows four tasks _Place SO_ (performed
twice in _ti_ 3 _, ti_ 4), _Update SO_ (performed once in _ti_ 7), _Update Invoice_ (performed
once in _ti_ 9), and _⟨Receive SO, Unpack_ _[∗]_ _⟩_ (performed twice in _ti_ 6 _, ti_ 21).
We now want to visualize the behavior all actors regarding the _frequent tasks_
in handling _Supplier Orders_, e.g., tasks performed at least twice. The visualization shall be on the abstraction level of the activities performed by actors, i.e., a
multi-entity DFG. To achieve this, we aggregate the “Event Entity Layer” into
a “Class Layer” using the “Task Layer” as context.


1. Select from the “Event Entity Layer” only the _Actor_ entities; this removes
all df-relationships for _A_ and _B_ .
2. Project onto all event nodes _e ∈_ _N_ _[Event]_ having a path _⟨e, ti, t⟩_ to a task node
_t ∈_ _N_ _[Task]_ with _t.count ≥_ 2, i.e., only events that are contained in a task
instance _ti_ of a frequently occurring task. This removes _e_ 7 and _e_ 9 from the
graph in Fig. 19 and introduces ( _e_ 8 _, e_ 10) _∈_ _RR_ _[df]_ 2 [.]
3. Aggregate the _Event_ nodes to _Class_ nodes by their _Activity_ property and lift
df-relationships from _Event_ nodes to _Class_ nodes (see Sect. 5.4).


The resulting multi-entity DFG forms a new “Class Layer” in the graph, that
is connected to the “Event Entity Layer” by _observes_ relationships, as shown in
Fig. 19. The multi-entity DFG shows that _R_ 1 and _R_ 2 work on disjoint sets of
activities, and that _R_ 2 indeed follows a cyclic, structured behavior. The paths
from _Class_ nodes _Receive SO_ and _Unpack_ to the _Task_ nodes show that all
activities belong to the same task, i.e., one cycle is one “unit of work”.
The multi-entity DFG is a filtered DFG: it lacks df-relationships for _Supplier_
_Orders_ and it omits _Update SO_ . Thus, the multi-entity DFG _does not fit_ or _deviates_
from the “Event Entity Layer”. We can identify the deviations in multi-layered


312 D. Fahland


process knowledge graph in Fig. 19 similar to alignments [9]; see [8]. For instance,
for df-relationship ( _Unpack, Unpack_ ) _∈_ _R_ _[df]_ in the “Class Layer”, we see


 - two corresponding “synchronous” df-relationship ( _e_ 10 _, e_ 11) _,_ ( _e_ 20 _, e_ 21) _∈_ _RR_ _[df]_ 2
with ( _ei, Unpack_ ) _∈_ _R_ _[observes]_ ; and

 - one corresponding “log-move” df-path _⟨e_ 8 _, e_ 9 _, e_ 10 _⟩_ _∈_ ( _RR_ _[df]_ 2 [)] _[∗]_ with
( _e_ 8 _, Unpackt_ ) _,_ ( _e_ 9 _, Update Invoice_ ) _,_ ( _e_ 10 _, Unpack_ ) _∈_ _R_ _[observes]_, i.e., _e_ 9 occurs
in between _Unpack_ and _Unpack_ .


**7** **Conclusion and Outlook**


The preceding sections studied different forms of process mining over multiple
behavioral dimensions that are summarized in Fig. 20. We showed in Sect. 3 how
classical process mining techniques fail when the assumption of a single entity
handled by a single execution (bottom left quadrant in Fig. 20) is violated.


**analysis over…**



**mul�ple** dynamics:
all execu�ons
and actors


one dynamic:
one execu�on






|Call Centers<br>Queuing Networks<br>Healthcare|Logiscs<br>Warehouses<br>Producon Systems|
|---|---|
|classical<br>process<br>mining|ERP Systems<br>Document-driven<br>processes|



one en�ty **mul�ple** en��es **…in process behavior**


**Fig. 20.** Quadrants of process analysis over multiple behavioral dimensions


To overcome these assumptions, we introduced process mining with event
knowledge graphs, that rests on three simple, but fundamental principles:


1. Explicitly represent every entity that an event is correlated to as a node. An
entity thereby can be anything: a specific object, a person or actor, or even
an abstract concept such as an activity.
2. Infer directly-follows relations over events per entity. This results in directlyfollows paths forming complex, but meaningful structures that can be filtered
for.
3. Aggregate any structure of interest formed by directly-follows paths into new
nodes describing process-related concepts, explicitly linked to the structures
that generate them. This allows to infer interactions between related entities
(see Sect. 4.4), multi-entity process models (see Sect. 5.5), and task instances
(see Sect. 6.3).


Event Knowledge Graphs 313


Applying these principles, we constructed event knowledge graphs from standard
event data through simple concepts in Sect. 4.3. We showed in Sect. 5 how to
analyze processes where each execution involves _multiple related entities_, such as
ERP systems and document-driven processes (bottom right quadrant in Fig. 20).
We showed in Sect. 6 how event knowledge graphs also allow to analyze _multiple_
_dynamics_ together. We added actor and queue behavior to study how entities
pass through queues or actors perform tasks across multiple entities, which are
dynamics studied in call centers or in healthcare (top left quadrant in Fig. 20).
Note that, in Sect. 6 we always focused on a single entity processed in a queue
or in a task. How to analyze the combination of _multiple dynamics_ over _multiple_
_entities_ (top right quadrant in Fig. 20) is an open question.
Event knowledge graphs give rise to a number of novel research questions.
We have shown how to construct event knowledge graphs from event tables,
even automatically [24,25]. We also need techniques to construct event knowledge graphs from relational database while preserving the existing entities and
relations. Existing automated conversion techniques from relational to graph
databases [50] only convert records into entity nodes, while event knowledge
graphs require to construct event nodes.
The quality of a process mining analysis on event knowledge graphs relies on
having identified the relevant structural relations (between entities) and behavioral or cause-effect relations (between events) (see Sect. 4.4). We need automated techniques to infer relevant relations that take the temporal semantics
of the df-relationship into account. Promising first steps are techniques that
explicitly allow to incorporate domain knowledge when inferring causal relationships from relational data [56], or use ontologies [6,7] for extraction. Specifically,
dynamically changing relationships and changes of object properties [39,40] still
need to be considered.
We have sketched the possibility of structuring a complex process mining
analysis by adding analysis layers to the graph, but limited ourselves to simple
selection, projection, and aggregation queries. Adequate query languages that
also can handle process-relevant phenomena such as frequency, noise, performance in relation to multiple entities need to be considered. Also, more complex
behavioral dynamics can be discovered. For example, enriching the event knowledge graph with the activity dimension to derive the performance spectrum (see
Sect. 6.2) allows detecting subgraphs that indicate high workload (many events
in a short interval) or a dynamic bottleneck (a short-term increase in waiting
time) [51]. Aggregating these to “high-level events” and mining for cause-effect
relations among them reveals how performance anomalies cascade through a
process [51].
Finally, while we did discuss how to discover multi-entity directly-follows
graphs through aggregation, true process discovery of models with precise semantics from event knowledge graphs still has to be addressed. In principle, such
models can be discovered through principles of artifact-centric process mining [41,46]: First obtain a classical event log per entity type, e.g., by extracting
the df-paths per entity type from the graph, and discover a classical process


314 D. Fahland


**Fig. 21.** Synchronous proclet model for the graph of Fig. 9 extended with proclets
describing the _intended_ (not the observed) behavior for all actors.


model per entity type. Then compose the models of the different entity types to
express their synchronization.
Figure 21 shows a possible process model that could be obtained in this way
for our example, using a multi-entity extension for Petri nets, called _synchronous_
_proclets_ [26]. Each proclet is a Petri net that describes the behavior of one
entity type; bold-bordered initial transitions describe the creation of a new entity.
The dashed _synchronization edges_ describe which transitions occur together; the
multiplicity annotations indicate how many entities of each type have to be
involved. Note that the proclet model in Fig. 21 is a hybrid between discovered
and manually created model. The proclets for _Order_, _Supplier Order_, _Invoice_,


Event Knowledge Graphs 315


_Item_, _Payment_, and _(Order,Payment)_ are each discovered from the entity type’s
df-paths of the graph in Fig. 9. The proclets for the _Actors_ however are created
manually [9], describing the intended routine for each actor based on the insights in
Sect. 6.3. Bold-bordered initial transitions describe the creation of a new entity;
note that the proclets for actors do not have an initial transition but an initial
marking as actors are not created in the process. Dashed _synchronization edges_
between transitions describe that the transitions have to occur together; the
multiplicity annotations indicate how many entities of each type have to be
involved. For instance, _R_ 1 creates 1 new _Order_ in each occurrence of _Create_
_Order_, but _R_ 4 always packs 2–3 _Items_ into 1 _Shipment_ in each occurrence of
_Pack Shipment_ .
An alternative formalization of this concept are _object-centric Petri nets_ [53].
Object-centric Petri nets also first discover one Petri net per entity type, then
annotate the places and arcs with entity identifiers, and then compose all entity
nets along transitions for the same activity, resulting in a coloured Petri net
model that is accessible for analysis [53] and measuring model quality [3]. However, synchronization by composition prevents explicitly modeling (and thus
discovering) interactions between entities such as the relation from _Order_ to
_Payment_ described by proclet _(Order,Payment)_ in Fig. 21.

Though, while proclets can
describe entity interactions, the
behavior of entity interactions
tends to be rather unstructured
resulting in overly complex models [41]. Extensions of declarative
models (see [10]) such as modular DCR graphs [14], that apply
similar principles as synchronous
proclets, could be more suitable.
Alternatively, scenario-based models [31] that specify conditional partial orders of events over multiple entities could be applied. For
instance, the conditional scenario **Fig. 22.** Conditional scenario describing an
in Fig. 22 specifies the interac- interaction of 2 _Orders_ and 1 _Payment_ .
tion between _Orders_ and _Payments_
observed in the graph of Fig. 9.
Altogether, event knowledge graphs give rise to entirely novel forms of process
mining that support novel forms of process management [17].


9 We created one proclet per actor as introducing a proclet for all actors would result
in a very complex proclet as different actors follow very different behavior. Further,
the manually created model conveniently avoids the issue of having to layout how
_R_ 2 synchronizes both with _Supplier Order_ and with _Invoice_ .


316 D. Fahland


**References**


1. van der Aalst, W.M.P.: Process mining: a 360 degrees overview. In: van der Aalst,
W.M.P., Carmona, J. (eds.) Process Mining Handbook. LNBIP, vol. 448, pp. 3–34.
Springer, Cham (2022)
2. Accorsi, R., Lebherz, J.: A practitioner’s view on process mining adoption, event
log engineering and data challenges. In: van der Aalst, W.M.P., Carmona, J. (eds.)
Process Mining Handbook. LNBIP, vol. 448, pp. 212–240. Springer, Cham (2022)
3. Adams, J.N., van der Aalst, W.M.P.: Precision and fitness in object-centric process
mining. In: ICPM 2021, pp. 128–135. IEEE (2021)
4. Berti, A., van der Aalst, W.: Extracting multiple viewpoint models from relational
databases. In: Ceravolo, P., van Keulen, M., G´omez-L´opez, M.T. (eds.) SIMPDA
[2018-2019. LNBIP, vol. 379, pp. 24–51. Springer, Cham (2020). https://doi.org/](https://doi.org/10.1007/978-3-030-46633-6_2)
[10.1007/978-3-030-46633-6](https://doi.org/10.1007/978-3-030-46633-6_2) ~~2~~
5. Bonifati, A., Fletcher, G.H.L., Voigt, H., Yakovets, N.: Querying Graphs. Synthesis
Lectures on Data Management. Morgan & Claypool Publishers, San Rafael (2018)
6. Calvanese, D., Kalayci, T.E., Montali, M., Santoso, A.: OBDA for log extraction
in process mining. In: Ianni, G., et al. (eds.) Reasoning Web 2017. LNCS, vol.
[10370, pp. 292–345. Springer, Cham (2017). https://doi.org/10.1007/978-3-319-](https://doi.org/10.1007/978-3-319-61033-7_9)
[61033-7](https://doi.org/10.1007/978-3-319-61033-7_9) ~~9~~
7. Calvanese, D., Kalayci, T.E., Montali, M., Tinella, S.: Ontology-based data access
for extracting event logs from legacy data: the onprom tool and methodology. In:
Abramowicz, W. (ed.) BIS 2017. LNBIP, vol. 288, pp. 220–236. Springer, Cham
[(2017). https://doi.org/10.1007/978-3-319-59336-4](https://doi.org/10.1007/978-3-319-59336-4_16) ~~1~~ 6
8. Carmona, J., van Dongen, B., Weidlich, M.: Conformance checking: foundations,
milestones and challenges. In: van der Aalst, W.M.P., Carmona, J. (eds.) Process
Mining Handbook. LNBIP, vol. 448, pp. 155–190. Springer, Cham (2022)
9. Carmona, J., van Dongen, B.F., Solti, A., Weidlich, M.: Conformance Checking [Relating Processes and Models. Springer, Cham (2018). https://doi.org/10.1007/](https://doi.org/10.1007/978-3-319-99414-7)
[978-3-319-99414-7](https://doi.org/10.1007/978-3-319-99414-7)
10. Di Ciccio, C., Montali, M.: Declarative process specifications: reasoning, discovery, monitoring. In: van der Aalst, W.M.P., Carmona, J. (eds.) Process Mining
Handbook. LNBIP, vol. 448, pp. 108–152. Springer, Cham (2022)
11. Cyganiak, R., Hyland-Wood, D., Lanthaler, M.: RDF 1.1 concepts and abstract
syntax. W3C Proposed Recommendation (2014)
12. de Murillas, E.G.L., Reijers, H.A., van der Aalst, W.M.P.: Case notion discovery
and recommendation: automated event log building on databases. Knowl. Inf. Syst.
**62** [(7), 2539–2575 (2019). https://doi.org/10.1007/s10115-019-01430-6](https://doi.org/10.1007/s10115-019-01430-6)
13. De Weerdt, J., Wynn, M.T.: Foundations of process event data. In: van der Aalst,
W.M.P., Carmona, J. (eds.) Process Mining Handbook. LNBIP, vol. 448, pp. 193–
211. Springer, Cham (2022)
14. Debois, S., L´opez, H.A., Slaats, T., Andaloussi, A.A., Hildebrandt, T.T.: Chain of
events: modular process models for the law. In: Dongol, B., Troubitsyna, E. (eds.)
[IFM 2020. LNCS, vol. 12546, pp. 368–386. Springer, Cham (2020). https://doi.](https://doi.org/10.1007/978-3-030-63461-2_20)
[org/10.1007/978-3-030-63461-2](https://doi.org/10.1007/978-3-030-63461-2_20) ~~2~~ 0
15. Denisov, V., Belkina, E., Fahland, D., van der Aalst, W.M.P.: The performance
spectrum miner: visual analytics for fine-grained performance analysis of processes.
In: BPM 2018 Demos. CEUR Workshop Proceedings, vol. 2196, pp. 96–100. CEURWS.org (2018)


Event Knowledge Graphs 317

