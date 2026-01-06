<!-- Source: 10-OC-PM_Object-Centric_Process_Mining.pdf | Chunk 1/2 -->

International Journal on Software Tools for Technology Transfer
https://doi.org/10.1007/s10009-022-00668-w


~~**GENERAL**~~


**Regular**

# **OC-PM: analyzing object-centric event logs and process models**


**Alessandro Berti** **[1]** **· Wil M. P. van der Aalst** **[1]**


Accepted: 29 August 2022
© The Author(s) 2022


**Abstract**
Object-centric process mining is a novel branch of process mining that aims to analyze event data from mainstream information
systems (such as SAP) more naturally, without being forced to form mutually exclusive groups of events with the specification
of a case notion. The development of object-centric process mining is related to exploiting object-centric event logs, which
includes exploring and filtering the behavior contained in the logs and constructing process models which can encode the
behavior of different classes of objects and their interactions (which can be discovered from object-centric event logs). This
paper aims to provide a broad look at the exploration and processing of object-centric event logs to discover information related
to the lifecycle of the different objects composing the event log. Also, comprehensive tool support (OC-PM) implementing
the proposed techniques is described in the paper.


**Keywords** Object-centric process mining · Object-centric event logs · Object-centric process discovery · Object-centric
conformance checking



**1 Introduction**


Process mining [1] is a branch of data science providing techniques to exploit the event data that support the execution
of business processes. Different areas exist in process mining, such as process discovery (the discovery of a process
model from an event log), conformance checking (comparing the behavior described in the event log with a process
model), process enhancement (enriching models with information related to time and data), machine learning (such
as root cause analysis and the prediction of the next activity/remaining time).
Mainstream process mining techniques start from an _event_
_log_, i.e., a collection of events extracted from the databases
supporting the process execution. In such event logs, a _case_ is
acollectionofeventsrelatedtoaparticularprocessexecution.
For example, in a sales order management system, a case may
refer to all the events related to the creation and confirmation


B Alessandro Berti
a.berti@pads.rwth-aachen.de


Wil M. P. van der Aalst
wvdaalst@pads.rwth-aachen.de


1 Process and Data Science Group, RWTH Aachen University,
Ahornstrasse 55, 52074 Aachen, NRW, Germany



of the order, collecting and packing the different order items,
the delivery, and invoicing. For such a system, establishing
a case notion can lead to the known _convergence_ and _diver-_
_gence_ problems [2]. We have a convergence problem when
the same event is related to different cases. In event log formats such as XES [1], this leads to replicating the same event.
We have a divergence problem when a case contains different instances of the same activity. For example, a sales order
contains different instances of the collection and the packing
of the order items. Mainstream process mining techniques
(e.g., process discovery and conformance checking) use the
order of the events inside the log cases. However, the quality
of the output is affected by the convergence and divergence
problems.
_Object-centric event logs_ have been proposed to resolve
the convergence and divergence problems. Object-centric
event logs are a novel representation of the event data in the
information systems, where each event is related to different
objects of different types. An informal representation of an
object-centric event log is contained in Table 1. The event log
contains eight events. The first event, having activity “create order”, is related to an object of type order ( _o_ 1) and two
objects of type item ( _i_ 1 and _i_ 2). Moreover, some attributes at


1 [https://xes-standard.org/](https://xes-standard.org/)

## 123


A. Berti, W. M. P. van der Aalst


the event level are described (for example, _prepaid-amount_
having a value 200.0 for the first event). Object-centric event
logs describe the lifecycle of different objects without leading to the convergence problem since an event can be related
to different objects. Also, the divergence problem is avoided
since we avoid specifying a single case notion.
In an object-centric event log, it is also possible to specify
the values for some attributes of the objects. This is represented in Table 2: object _o_ 1, having type order, is sold to the
customerAppleatthecostof3500.Toexploittheinformation
contained in object-centric event logs, new process mining
techniques are required. This leads to the development of
_object-centric process mining_ techniques. These exploit the
lifecycle of the objects and the relationships between the
objects to provide insights on the execution of a business
process and check the actual execution logs.
However, the discipline is still in an early development stage. While some approaches have been proposed for
process discovery and conformance checking in an objectcentric setting (see Sect. 5), some important aspects, such
as the exploration (being able to visualize the event log and
focus on some dimensions) and filtering (restrict the behavior of the log to a subset of events/objects) of object-centric
event logs have been marginally explored. Moreover, a comprehensive description of the annotations for the elements
of object-centric process models (such as the frequency of
nodes and edges) is missing. The paper aims to propose a
set of object-centric process mining techniques to bridge the
gap between traditional and object-centric process mining,
including:


 - The exploration of object-centric event logs: its events
and the _lifecycle_ of its objects.

 - The filtering possibilities on object-centric event logs.

 - Provide the automatic discovery of object-centric process
models with different complexity (less/more activities,
less/more edges).

 - Describe meaningful annotations (number of events/
objects) at the activity and the edge level.

 - Provide some conformance metrics on object-centric
event logs.


Also, the paper describes the OC-PM tool(s) for objectcentric process mining, providing the proposed techniques
as a web-based interface and as a plugin of the ProM frame[work. These are available at the address https://ocpm.info.](https://ocpm.info)
Tool support in object-centric process mining is currently
limited to a set of library and ad-hoc tools (for example, [3]
for the discovery of variants), hence the importance of comprehensive tool support covering a good part of the lifecycle
of an object-centric process mining analysis.
The rest of the paper is organized as follows. Section 2
describes the information on event logs and directly-follows


## 123


OC-PM: analyzing object...


**Table 2** Informal representation
of the objects of an
object-centric event log. Each
row (except the header)
represents an object



Id Type Customer Costs Color Size Ensured Priority


_o_ 1 _Order_ _Apple_ _3500.0_


_i_ 1 _Item_ _Orange_ _Big_


_i_ 2 _Item_ _Green_ _Small_


_p_ 1 _Package_ _Yes_


_p_ 2 _Package_ _No_


_d_ 1 _Delivery_ _High_



graphs needed to understand the paper. Section 3 presents
some operations on object-centric event logs (flattening,
lifecycle, filtering), the discovery of object-centric directlyfollows multigraphs, and several annotations at the activity
and the edge level. Section 4 presents the tools supporting the
paper. Section 5 presents the related work on object-centric
process mining. Finally, Sect. 6 concludes the paper.


**2 Background**


This section introduces the basic knowledge (event logs,
directly-follows graph) needed to understand the rest of the
paper.


**2.1 Traditional event log**


“Traditional” event logs, used by mainstream process mining
techniques, are a collection of events and cases. A case is
a collection of events of the same process execution. For
example, in a ticket management system, a case contains
events for the creation, the resolution, and the closure of the
ticket. To introduce a definition of traditional event logs, we
introduce some universes (event identifiers, case identifiers,
activities) in Def. 1 and then the definition of traditional event
log in Def. 2.


**Definition 1** (Generic Universes) Below are the universes
used in the definition of traditional (and object-centric) event
logs:


 - _Ue_ is the universe of event identifiers. _Example: Ue_ =
{ _e_ 1 _, e_ 2 _, e_ 3 _, . . ._ }

 - _Uc_ is the universe of case identifiers. _Example: Uc_ =
{ _c_ 1 _, c_ 2 _, . . ._ }

 - _Uact_ is the universe of activities. _Example: Uact_ = {
_place order_, _check availability_, …}

 - _Utimest_ istheuniverseoftimestamps. _Example:Utimest_ =
{ _2020-07-09T08:21:01.527+01:00_, …} We assume
_Utimest_ to be totally ordered. Moreover, a difference −
operation is defined for timestamps as the number of seconds separating the subtrahend from the minuend.



**Definition 2** (Traditional Event Log) A _traditional_ event log
is a tuple _T L_ = _(E, πact_ _, πtime, πcase,_ ≤ _)_ where:


 - _E_ ⊆ _Ue_ is a set of events.

 - _πact_ : _E_ → _Uact_ associates an activity to each event.

 - _πtime_ : _E_ → _Utimest_ associates a timestamp to each
event.

 - _πcase_ : _E_ → _P(Uc)_ \ {∅} associates a non-empty set of
cases to each event.

 - ≤ ⊆ _E_ × _E_ is a total order on _E_ .


An important consideration is that, in Def. 2, each event
can be associated with several cases. In traditional event log
formats such as XES [2], cases are primary-level objects, so if
an event belongs to different cases, it is going to be replicated
in the serialization.
The operations introduced in Def. 3 can be defined on an
event log.


**Definition 3** (Operations on an Event Log) Given a traditional event log _T L_ = _(E, πact_ _, πtime, πcase,_ ≤ _)_, we define
the following operations:


 - _πact_ _(T L)_ = { _πact_ _(e)_ | _e_ ∈ _E_ }

 - _πcase(T L)_ = ∪ _e_ ∈ _E πcase(e)_

 - For _c_ ∈ _πcase(T L)_, _caseT L_ _(c)_ = ⟨ _e_ 1 _, . . ., en_ ⟩ where:


  - { _e_ 1 _, . . ., en_ } = { _e_ ∈ _E_ | _c_ ∈ _πcase(e)_ }

  - ∀1≤ _i<n ei < ei_ +1


 - Given _c_ ∈ _πcase(T L)_ and _caseT L_ _(c)_ = ⟨ _e_ 1 _, . . ., en_ ⟩:


   - trace _T L_ _(c)_ = ⟨ _πact_ _(e_ 1 _), . . ., πact_ _(en)_ ⟩

   - start _T L_ _(c)_ = _πact_ _(e_ 1 _)_ .

  - end _T L_ _(c)_ = _πact_ _(en)_ .


 - _πstart_ _(T L)_ = {start _T L_ _(c)_ | _c_ ∈ _πcase(T L)_ } is the set of
start activities.

 - _πend_ _(T L)_ = {end _T L_ _(c)_ | _c_ ∈ _πcase(T L)_ } is the set of
end activities.


2 [http://www.processmining.org/logs/xes](http://www.processmining.org/logs/xes)

## 123


**2.2 Directly-follows graphs**


A _directly-follows graph_ (DFG) is a simple process model
describing the directly-follows relationship between the different activities of a process. In Def. 4, we introduce a formal
definition of DFG. The definition comes with a frequency
measure on the nodes and a frequency measure on the edges
of the DFG. This identifies the most and the least used paths
in the process model.


**Definition 4** (Directly-Follows Graph) A _directly-follows_
_graph_ is a tuple _(A, F, π f reqn, π f reqe)_ where:


 - _A_ ⊆ _Uact_ is a set of activities.

 - ▷ is the start node of the graph, □ is the end node of the
graph.

 - _F_ ⊆ _(_ {▷} ∪ _A)_ × _(A_ ∪{□} _)_ is the set of edges.

 - _π f reqn_ : _A_ ↛N is a frequency measure on the nodes.

 - _π f reqe_ : _F_ ↛N is a frequency measure on the edges.


In the previous definition, we use ↛ as a symbol telling
thatasubsetofelementsofthedomain( _A_ and _F_ respectively)
is mapped to an element of the image (N). We can discover
a directly-follows graph from a traditional event log. This is
introduced in Def. 5.


**Definition 5** (Discovery of a Directly-Follows Graph) Let
_T L_ = _(E, πact_ _, πtime, πcase,_ ≤ _)_ be a traditional event log.
We define the following discovery operation:


_DFG(T L)_ = _(A, F, π f reqn, π f reqe)_


where:


 - _A_ = _πact_ _(T L)_ and


_F_ = { _(_  - _,_ start _T L_ _(c)), (_ end _T L_ _(c),_  - _)_ | _c_ ∈ _πcase(T L)_ }∪

∪ _c_ ∈ _πcase(T L),_ trace _T L_ _(c)_ =⟨ _a_ 1 _,...,an_ ⟩{ _(ai_ _, ai_ +1 _)_ | 1 ≤ _i < n_ }


 - For _a_ ∈ _A_, _π f reqn(a)_ = |{ _e_ ∈ _E_ | _πact_ _(e)_ = _a_ }|

 - For _(_ - _, a)_ ∈ _F_, _π f reqe(_ - _, a)_ = |{ _c_ ∈ _πcase(T L)_ | start _T L_
_(c)_ = _a_ }|

 - For _(a,_ - _)_ ∈ _F_, _π f reqe(a,_ - _)_ = |{ _c_ ∈ _πcase(T L)_ | end _T L_
_(c)_ = _a_ }|

 - For _(a, b)_ ∈ _F_ ∩ _(A_ × _A)_,

    _π f reqe(a, b)_ =

_c_ ∈ _πcase(T L),_
trace _T L_ _(c)_ =⟨ _a_ 1 _,...,an_ ⟩
|{ _i_ ∈ N | 1 ≤ _i < n_ ∧ _ai_ = _a_ ∧ _ai_ +1 = _b_ }|


Given Def. 5, we can define two operators: the _projection_
_on the set of activities_ ( _πA((A, F, π f reqn, π f reqe))_ = _A_ )
and the _set of edges_ ( _πF_ _((A, F, π f reqn, π f reqe))_ = _F_ ).

## 123



A. Berti, W. M. P. van der Aalst


The directly-follows graphs are the building blocks for
some object-centric process models introduced in Sect. 3.3.
As seen in Def. 5, they can be straightforwardly discovered
from event logs, and they can be easily filtered based on a
threshold on the frequency of activities and edges.


**3 Approach**


The approach section is composed of different subsections,
analyzing different techniques to exploit object-centric event
logs. We start with the definition of object-centric event logs
and the proposition of the OCEL format for the storage of
object-centric event logs. The flattening operation (which
projects the object-centric event log to a traditional event
log with the choice of a case notion) is introduced, as it is
essential for process discovery purposes. Then, some filtering operations (activities, paths, endpoints, timeframe, object
types) are proposed on top of object-centric event logs.
In Sect. 3.3, an object-centric process model (the objectcentric directly-follows multigraph) is defined that can be
discoveredstraightforwardlyfromanobject-centriceventlog
using the aforementioned flattening operation. Then, some
generic metrics on object-centric event logs are introduced,
whichcanbeusedtoannotatetheobject-centricprocessmodels.
Finally, some model-independent conformance checking
techniques are introduced, which can be applied to objectcentric event logs.


**3.1 Object-centric event log and flattening**


The starting point of an object-centric process mining analysis lies in an object-centric event log. In object-centric event
logs, we assume that each event is related to different objects
of different types. Moreover, some other attributes are associated with the events and the objects of the log. Def. 6
introduces some universes that are necessary for the formal
definition of object-centric event log. The definition has also
been introduced in [4].


**Definition 6** (Universes(forOCEL))Belowaretheuniverses
used in the formal definition of object-centric event logs:


 - _Uatt_ is the universe of attribute names. _Example: Uatt_ =
{ _resource_, _weight_, …}

 - _Uval_ is the universe of attribute values. _Example: Uval_ =
{ _500_, _1000_, _Mike_, …}

 - _Utyp_ is the universe of attribute types. _Example: Utyp_ =
{ _string_, _integer_, _float_, …}

 - _Uo_ is the universe of object identifiers. _Example: Uo_ =
{ _o_ 1 _, i_ 1 _, . . ._ }


OC-PM: analyzing object...


 - _Uot_ is the universe of objects types. _Example: Uot_ = {
_order_, _item_, …}


Def 7 introduces the formal definition of object-centric
event log.


**Definition 7** (Object-Centric Event Log) An object-centric
event log is a tuple
_L_ = _(E, AN_ _, AV, AT, OT, O, πtyp, πact_ _, πtime,_
_πvmap, πomap, πotyp, πovmap,_ ≤ _)_ such that:


 - _E_ ⊆ _Ue_ is the set of event identifiers. _Example:_ the first
event shown in Table 1 is related to the event identifier
_e_ 1.

 - _AN_ ⊆ _Uatt_ is the set of attributes names. _Example:_
in Table 1 _resource_, _prepaid-amount_, _weight_, and _total-_
_weight_ are attribute names and, in Table 2, _costs_, _color_,
and _size_ are attribute names.

 - _AV_ ⊆ _Uval_ is the set of attribute values (with the requirement that AN ∩ AV = ∅). _Example:_ in Table 1 _200.0_,
_Anahita_, and _10.0_ are attribute values, and in Table 2,
_Apple_, _green_, and _3500.0_ are attribute values.

 - _AT_ ⊆ _Utyp_ is the set of attribute types. _Example:_ the
type of the attribute _resource_ in Table 1 is _string_ .

 - _OT_ ⊆ _Uot_ is the set of object types. _Example:_ in Table 2,
for the first object, the type is _order_ .

 - _O_ ⊆ _Uo_ is the set of object identifiers. _Example:_ the first
object in Table 2 is related to the object identifier _o_ 1.

 - _πtyp_ : _AN_ ∪ _AV_ → _AT_ is the function associating an
attribute name or value to its corresponding type. _Exam-_
_ple:_ for the attributes in Table 1,
_πtyp(prepaid-amount)_ = _float_, _πtyp(200.0)_ = _float_ .

 - _πact_ : _E_ → _Uact_ is the function associating an event
(identifier) to its activity. _Example:_ for the first event
shown in Table 1, the activity is _place order_ .

 - _πtime_ : _E_ → _Utimest_ is the function associating an
event (identifier) to a timestamp. _Example:_ for the first
event shown in Table 1, the timestamp is _2020-07-_
_09T08:21:01.527+01:00_ .

 - _πvmap_ : _E_ → _(AN_ ↛ _AV )_ such that


_πtyp(n)_ = _πtyp(πvmap(e)(n))_

∀ _e_ ∈ _E_ ∀ _n_ ∈ dom _(πvmap(e))_


is the function associating an event (identifier) to its
attribute value assignments. _Example:_ for the first event
in Table 1 _, πvmap(e_ 1 _)(prepaid-amount)_ = _200.0_

 - _πomap_ : _E_ → _P(O)_ is the function associating an event
(identifier) to a set of related object identifiers. _Exam-_
_ple:_ the first event in Table 1 is related to three objects
_πomap(e_ 1 _)_ = { _o_ 1 _, i_ 1 _, i_ 2}.




 - _πotyp_ ∈ _O_ → _OT_ assigns precisely one object type
to each object identifier. _Example:_ for the first object in
Table 2, _πotyp(o_ 1 _)_ = _order_ .

 - _πovmap_ : _O_ → _(AN_ ↛ _AV )_ such that


_πtyp(n)_ = _πtyp(πovmap(o)(n))_

∀ _n_ ∈ dom _(πovmap(o))_ ∀ _o_ ∈ _O_


is the function associating an object to its attribute value
assignments. _Example:_ for the second object in Table 2,
_πovmap(i_ 2 _)(color)_ = _green_ .

 - ≤ is a total order (i.e., it respects the antisymmetry, transitivity, and connexity properties).


Recently, the OCEL format has been proposed for objectcentric event logs [3] . Two implementations of the format
exist (JSON-OCEL, supported by JSON; XML-OCEL, supported by XML; MongoDB [5]), with tool support available for some popular languages (Java/ProM framework [4],
Javascript [5], Python [6] ). On the page _Event Logs_, some event
logs (in the JSON-OCEL and XML-OCEL formats) are
available, which can be ingested by the tool support.
In Def. 8, some general statistics on object-centric event
logs are introduced. While the number of events and (unique)
objects derives directly from the log elements, the number of
total objects is an interesting aggregation that considers how
many events are related to the given object. So, considering
the ratio between the number of total objects and unique
objects, the higher the ratio, the higher the average length of
the lifecycle of the objects of the object-centric event log.


**Definition 8** (General Statistics on an Object-Centric Event
Log) Let _L_ be an object-centric event log as in Def. 7. We
define the following general statistics on the object-centric
event log:


GS1 _Number of Events_ E _(L)_ = | _E_ |.
GS2 _Number of Unique Objects_ UO _(L)_ = | _O_ |.
GS3 _Number of Total Objects_ TO _(L)_ = [�] _e_ ∈ _E_ [|] _[π][omap][(][e][)]_ [|][.]


An operation defined on object-centric event logs is _flat-_
_tening_ . A flattening operation transforms the object-centric
event log into a traditional event log given the choice of
an object type. This is useful because many process mining approaches are only available for traditional event logs.
Moreover, some object-centric process discovery algorithms
(suchasMVP[6,7]andobject-centricPetrinets[8])performs
flattening to apply classic process discovery techniques and


3 [http://www.ocel-standard.org/](http://www.ocel-standard.org/)

[4 https://svn.win.tue.nl/repos/prom/Packages/OCELStandard/Trunk/](https://svn.win.tue.nl/repos/prom/Packages/OCELStandard/Trunk/)

[5 https://github.com/Javert899/pm4js-sandbox](https://github.com/Javert899/pm4js-sandbox)

[6 https://github.com/OCEL-standard/ocel-support](https://github.com/OCEL-standard/ocel-support)

## 123


then unite the results for the different object types in a single
model. Def. 9 proposes a formal definition of flattening. This
is based on the definition of _restriction_ for a function. Given
a function _f_ : _X_ → _Y_, and _X_ [′] ⊆ _X_, _f_ | _X_ ′ is a function with
dom _( f_ | _X_ ′ _)_ = _X_ [′] and for all _x_ ∈ _X_ [′], _f (x)_ = _f_ | _X_ ′ _(x)_ .


**Definition 9** (Flattening with an Object Type) Let _L_ be an
object-centriceventlogasinDef. 7,andot ∈ _OT_ beanobject
type. We define the flattening of _L_ using ot as _FL(L,_ ot _)_ =
_(E_ _[ot]_ _, πact_ _[ot]_ _[, π]_ _time_ _[ot]_ _[, π]_ _case_ _[ot]_ _[,]_ [ ≤] _[ot]_ _[)]_ [ where:]


 - _E_ _[ot]_ = { _e_ ∈ _E_ | ∃ _o_ ∈ _O πotyp(o)_ = ot ∧ _o_ ∈ _πomap(e)_ }

 - _πact_ _[ot]_ [=] _[ π][act]_ [|] _E_ _[ot]_

 - _πtime_ _[ot]_ [=] _[ π][time]_ [|] _[E]_ _[ot]_

 - For _e_ ∈ _E_ _[ot]_, _πcase_ _[ot]_ _[(][e][)]_ [ = {] _[o]_ [ ∈] _[π][omap][(][e][)]_ [ |] _[ π][otyp][(][o][)]_ [ =] _[ ot]_ [}]

 - ≤ _[ot]_ = { _(e_ 1 _, e_ 2 _)_ ∈≤ | ∃ _o_ ∈ _O πotyp(o)_ = ot ∧ _o_ ∈
_πomap(e_ 1 _)_ ∩ _πomap(e_ 2 _)_ }


Given the definition of flattening, we can introduce the
notion of _lifecycle_ in Def. 10. The lifecycle of an object is
the corresponding case in the flattened log [7] .


**Definition 10** (Lifecycle, Start and End Event for an Object)
Let _L_ be an object-centric event log as in Def. 7. We define:


 - The _lifecycle_ of an object _o_ ∈ _O_ as the sequence
of events to which the object is related: lif _(o)_ =
case _FL(L,πotyp(o))(o)_

 - The _trace_ of an object _o_ ∈ _O_ as the sequence of activities of the events belonging to its lifecycle: trace _(o)_ =
trace _FL(L,πotyp(o))(o)_

 - The start activity of an object _o_ ∈ _O_ as the first activity
of its trace: start _(o)_ = start _FL(L,πotyp(o))(o)_

 - The end activity of an object _o_ ∈ _O_ as the last activity of
its trace: end _(o)_ = end _FL(L,πotyp(o))(o)_


In Def. 10, we introduce the additional concepts of _trace_
for an object (the activities of the events of its lifecycle). The
start and end activities are of particular importance, as they
are the start/end of the process execution and can be used to
identify incomplete/improperly terminated objects.


**3.2 Filtering**


Filtering is an operation of high importance because it
restricts the behavior contained in the log to the desired one.
Many filters have been defined for traditional event logs (filteringthecasescontaininganactivity,filtersthecasesstarting
or ending with an activity, timeframe filter). In this section,
we want to introduce some filtering operations on objectcentric event logs. In Def. 11, given a subset of events of the


7 So, is the sequence of events that are related to the object.

## 123



A. Berti, W. M. P. van der Aalst


log, we define filtering operations restricting the event log to
these events.


**Definition 11** (Filtering on a Set of Events) Let _L_ be an
object-centric event log as in Def. 7, and _E_ [′] ⊆ _E_ a
set of events. We define the filtered event log _L E_ = _E_ ′ =
_(E_ [′] _, AN_ _, AV, AT, OT, O, πtyp, πact_ | _E_ ′ _, πtime_ | _E_ ′ _, πvmap_ | _E_ ′ _,_
_πomap_ | _E_ ′ _, πotyp, πovmap,_ ≤ _)_


Some filters based on Def. 11 are presented in Def. 12.
These include a filter on a subset of activities (useful to
remove some undesired activities from the analysis) and a
filter on timeframe (useful to restrict the analysis to a given
period of time).


**Definition 12** (Filtering on a Set of Events - Approaches)
Let _L_ be an object-centric event log as in Def. 7. Let _A_ =
{ _πact_ _(e)_ | _e_ ∈ _E_ } be the set of activities of _L_ . We present
some possibilities for the filtering of a set of objects:


F1 _Filtering on a Subset of Activities_ Given a set of activities
_A_ [′] ⊆ _A_, filter on the events having an activity in _A_ [′] :
_E_ [′] = { _e_ ∈ _E_ | _πact_ _(e)_ ∈ _A_ [′] }
F2 _Filtering on Timeframe_ Given some lower and upper
bounds lb _,_ ub ∈ _Utimest_, filter on the events falling in
the range [lb _,_ ub]: _E_ [′] = { _e_ ∈ _E_ | lb ≤ _πtime(e)_ ≤ ub}


The filtered log is defined starting from _E_ [′] as in Def. 11.


It is also possible to define a filtering operation starting
from a subset of objects. In Def. 13, the event log is filtered
to the set of events that are related to one of these objects.


**Definition 13** (Filtering on a Set of Objects) Let _L_ be an
object-centric event log as in Def. 7, and _O_ [′] ⊆ _O_ a set of
objects. Let _E_ _O_ ′ = { _e_ ∈ _E_ | _πomap(e)_ ∩ _O_ [′] ̸= ∅} be the
subset of events in _E_ related to at least one object in _O_ [′] . We
define the filtered event log
_L E_ = _E_ _O_ ′ _,O_ = _O_ ′ = _(E_ _O_ ′ _, AN_ _, AV, AT, OT, O_ [′] _, πtyp,_
_πact_ | _E_ _O_ ′ _, πtime_ | _E_ _O_ ′ _, πvmap_ | _E_ _O_ ′ _, πomap_ | _E_ _O_ ′ _, πotyp_ | _O_ ′ _,_
_πovmap_ | _O_ ′ _,_ ≤ _)_


Some filters based on Def. 13 are presented in Def. 14.
These exploit the operations on object-centric event logs
introduced in Def. 10.


**Definition 14** (Filtering on a Set of Objects - Approaches)
Let _L_ be an object-centric event log as in Def. 7. Let _A_ =
{ _πact_ _(e)_ | _e_ ∈ _E_ } be the set of activities of _L_ . We present
some possibilities for the filtering of a set of objects:


F3 _Filtering on the Objects related to an Activity_ Given a set
of activities _A_ [′] ⊆ _A_, filter on the objects related to one
of these activities: _O_ [′] = { _o_ ∈ _O_ | trace _(o)_ ∩ _A_ [′] ̸= ∅}


OC-PM: analyzing object...


F4 _Filtering on Start Activities_ Given a set of activities _A_ [′] ⊆
_A_, filter ontheobjects startingwithoneof theseactivities:
_O_ [′] = { _o_ ∈ _O_ | start _(o)_ ∈ _A_ [′] }
F5 _Filtering on End Activities_ Given a set of activities _A_ [′] ⊆
_A_, filter on the objects ending with one of these activities:
_O_ [′] = { _o_ ∈ _O_ | end _(o)_ ∈ _A_ [′] }
F6 _Filter on a Path_ Given a couple of activities _(a_ 1 _, a_ 2 _)_ ∈
_A_ × _A_, filter on the objects containing _(a_ 1 _, a_ 2 _)_ in their
trace: _O_ [′] = { _o_ ∈ _O_ | _(a_ 1 _, a_ 2 _)_ ∈ trace _(o)_ }
F7 _Filter on Object Types_ Given a set of object types SOT ⊆
OT, filter on the objects having one of these types: _O_ [′] =
{ _o_ ∈ _O_ | _πotyp(o)_ ∈ SOT}


The filtered log is defined starting from _O_ [′] as in Def. 13.


With the approaches presented in Def. 12 and Def. 14,
many filters available in the classic setting (endpoints, timeframe, attributes) are also made available in the object-centric
setting.


**3.3 Process discovery - OC-DFG**


Some of the proposed approaches for object-centric process discovery on object-centric event logs follow a common
schema: the object-centric event log is flattened on the available object types, a process model is discovered for the
flattened logs, and then the results are collated together.
In this section, we formalize one object-centric process
model, the _object-centric directly-follows multigraph_ (OCDFG), and how to discover an object-centric directly-follows
multigraph starting from an object-centric event log. We
choose to present object-centric directly-follows multigraphs
in the context of the current section because:


 - They can be straightforwardly discovered from objectcentric event logs (flattening - discovery of DFG collating).

 - They can be easily annotated, given that no replay operation is necessary.


The formal definition of OC-DFG is presented in Def.
15. We see that an OC-DFG is a collection of nodes (the
activities, plus one start and end node for each object type)
and typed edges between the activities.


**Definition 15** (Object-CentricDirectly-FollowsMultigraph)
An object-centric directly-follows multigraph (OC-DFG) is
a tuple _(A, OT, N_ _, F, π f reqn, π f reqe)_ where:


 - _A_ is a set of activities.

 - _OT_ is a set of object types.

 - _N_ = _A_ ∪{ _n_ _S,_ ot | _ot_ ∈ _OT_ }∪{ _n_ _E,_ ot | _ot_ ∈ _OT_ } is the set
of nodes of the graph, which includes the set of activities



and a start/end node for each object type ( _n_ _S,_ ot and _n_ _E,_ ot
respectively).

 - _F_ ⊆ _N_ × _OT_ × _N_ is a set of typed arcs.

 - _π f reqn_ : _A_ ↛N assigns a frequency to the activities.

 - _π f reqe_ : _F_ ↛R [+] ∪{0} assigns a frequency to the arcs.


Def. 16 introduces the discovery of OC-DFG from objectcentric event logs. Essentially, the event log is flattened for
each object type, the operation of discovery of an objectcentric directly-follows multigraph is performed for each
flattened log and the results are collated together to obtain
the OC-DFG.


**Definition 16** (Discovery of an Object-Centric DirectlyFollows Multigraph) Let _L_ be an object-centric event log as
in Def. 7. We define _O DFG(L)_ = _(A, OT, N_ _, F, π f reqn,_
_π f reqe)_ where _A_ and _OT_ are the set of activities and object
types of the log, respectively, _N_ is obtained as in Def. 15,
and given _n_ 1 _, n_ 2 ∈ _N_ we have _(n_ 1 _, ot, n_ 2 _)_ ∈ _F_ ⇐⇒
_(n_ 1 _, n_ 2 _)_ ∈ _πF_ _(DFG(FL(L,_ ot _)))_, and dom _(π f reqn)_ =
dom _(π f reqe)_ = ∅ (no frequency is described in this definition).


Figure 1 shows an example object-centric directly-follows
multigraph. The example contains different object types and
tells some information about the lifecycles of the different
object types, including:


 - The lifecycle of the objects with type _DOCTYPE_Inquiry_
starts and ends with the activity “Create Quotation”.

 - The lifecycle of the objects with type _DOCTYPE_
__Quotation_ starts with a “Create Quotation” activity,
which can end the lifecycle of the quotation or lead to
the “Create Order” activity.

 - The lifecycle of the objects with type _DOCTYPE_Order_
allows for a “Create Order” activity, which can end the
lifecycle of the order or lead to the “Create Goods Movement” activity.


Def. 17 defines a frequency-based filtering on objectcentric event logs. This is useful to simplify the model after
the discovery, for example, by focusing on the mainstream
behavior (most frequent activities and edges).


**Definition 17** (Frequency-Based Filtering) Let _(A, OT, N_ _,_
_F, π f reqn, π f reqe)_ beanobject-centricdirectly-followsmultigraph. Given _mn_ and _me_, which are thresholds for the
frequencies of the activities and edges respectively, we
define the filtered object-centric directly-follows multigraph _(A_ [′] _, OT, N_ [′] _, F_ [′] _, π_ [′] _f reqn_ _[, π]_ [′] _f reqe_ _[)]_ [, where] _[ A]_ [′][ = {] _[a]_ [ ∈]
_A_ | _π f reqn(a)_ ≥ _mn_ }, _N_ [′] = _A_ [′] ∪{ _n_ _S,_ ot | _ot_ ∈ _OT_ } ∪
{ _n_ _E,_ ot | _ot_ ∈ _OT_ }, _F_ [′] = { _f_ ∈ _F_ | _π f reqe( f )_ ≥ _me_ }∩ _(N_ [′] ×
_OT_ × _N_ [′] _)_, _π_ [′] _f reqn_ [=] _[ π][ f reqn]_ [|] _A_ [′][,] _[ π]_ [′] _f reqe_ [=] _[ π][ f reqe]_ [|] _F_ [′][.]

## 123


**Fig. 1** An example
object-centric directly-follows
multigraph (complete view).
The arc with number 1
highlights the activity “Create
Order”, which shows all the
statistics for all the object types
of the event log. The arc with
number 2 highlights the arc
going from “Create WMS
transfer order” to “Create Goods
movement”, which shows the
statistics for the three
annotations (E/O/EC)


We see that in Def. 16 we do not introduce any frequency
measure on the nodes/edges of the OC-DFG. In Def. 18 and
Def. 19, some frequency metrics are introduced for activities
and paths, respectively, and the discovery of OC-DFGs can
be modified with the inclusion of these measures. It should
be noted that the type of models presented in [7] is equivalent
to OC-DFGs with the choice of AF1 as frequency metric for
the activities and PF2 as frequency metric for the paths.

## 123



A. Berti, W. M. P. van der Aalst


**3.4 Activity/Path metrics**


This section proposes some frequency metrics for activities
and paths that can be computed starting from an objectcentric event log. The measures are independent from the
type of model but can be used to annotate the model (for
example, the OC-DFGs introduced in Def. 15).


OC-PM: analyzing object...


Def. 18 proposes some metrics at the activity level (number of events, number of unique objects, number of total
objects).


**Definition 18** (Activity Frequency Metrics) Let _L_ be an
object-centric event log as in Def. 7. Let _A_ = { _πact_ _(e)_ | _e_ ∈
_E_ } be the set of activities of _L_, and for _a_ ∈ _A_, the set
_Ea_ = { _e_ ∈ _E_ | _πact_ _(e)_ = _a_ } of all the events having _a_
as activity. We define the following metrics on an activity
_a_ ∈ _A_ :


AF1 _Counting the Number of Events having a given Activity_
E _(a)_ = | _Ea_ |.
AF2 _Counting the Number of Unique Objects related to Events_
_having a given Activity_ UO _(a)_ = |{ _o_ ∈ _O_ | ∃ _e_ ∈ _Ea, o_ ∈
_πomap(e)_ }|
AF3 _Counting the Number of Total Objects related to Events_
_having a given Activity_ TO _(a)_ = |{ _(e, o)_ ∈ _O_ | _e_ ∈
_Ea_ ∧ _o_ ∈ _πomap(e)_ }|


The metrics proposed in Def. 18 can be applied either on
the overall log, or on the log filtered on a specific object type
(see filter 7 of Def. 14). Figure 1(1) shows the annotations
(extracted using the tool proposed in Sect. 4) on the activity
“Create Order”. In the same box, we have different lines:


  - The name of the activity.

  - The three frequency annotations (E, UO, TO) on the
overall log.

  - The three frequency annotations on the log filtered on the
_DOCTYPE_Order_ object type (which is colored blue).

  - The three frequency annotations on the log filtered on
the _DOCTYPE_Quotation_ object type (which is colored
red).


Def. 19 defines some metrics on the paths based on the
lifecycle of the objects.


**Definition 19** (Paths Frequency Metrics) Let _L_ be an objectcentric event log as in Def. 7. Let _A_ = { _πact_ _(e)_ | _e_ ∈ _E_ } be
the set of activities of _L_, and for _a_ ∈ _A_, the set _Ea_ = { _e_ ∈
_E_ | _πact_ _(e)_ = _a_ } of all the events having _a_ as activity. Let
ot ∈ _OT_ be an object type, and _Oot_ = { _o_ ∈ _O_ | _πotyp(o)_ =
_ot_ } be the set of all the objects having object type ot. We
define the following metrics, depending on ot, provided two
activities _a_ 1 _, a_ 2 ∈ _A_ :


PF1 _Counting the Number of Event Couples which real-_
_ize the Path_ EC _(a_ 1 _,_ ot _, a_ 2 _)_ = |{ _(e_ 1 _, e_ 2 _)_ ∈ _Ea_ 1 ×
_Ea_ 2 | ∃ _o_ ∈ _Oot_ _, (e_ 1 _, e_ 2 _)_ ∈ lif _(o)_ }|.
PF2 _Counting the Number of Objects having the Path in_
_theirLifecycle_ UO _(a_ 1 _,_ ot _, a_ 2 _)_ = |{ _o_ ∈ _Oot_ | _(a_ 1 _, a_ 2 _)_ ∈
trace _(o)_ }|.



PF3 _Counting the Number of Total Objects having the Path_
_in their Lifecycle_ TO _(a_ 1 _,_ ot _, a_ 2 _)_ = |{ _(e_ 1 _, o, e_ 2 _)_ ∈
_Ea_ 1 × _O_ ot × _Ea_ 2 | _(e_ 1 _, e_ 2 _)_ ∈ lif _(o)_ }|.


Figure 1(2) shows the annotations (extracted using the tool
proposed in Sect. 4) on the path of type _DOCTYPE_Delivery_
between the activities “Create WMS transfer order” and
“Create Goods movement”. We see that the three proposed
measures (EC, UO, TO) are all reported.
As the last technique, we describe some approaches for
conformance checking which are independent of a process
model and depend solely on the verification of properties on
the event log. Def. 20 presents formally the rules.


**Definition 20** (Conformance Checking - Model Independent
Approaches) Let _L_ be an object-centric event log as in Def.
7. Let _A_ = { _πact_ _(e)_ | _e_ ∈ _E_ } be the set of activities of _L_, and
_Ea_ = { _e_ ∈ _E, πact_ _(e)_ = _a_ }. We present some possibilities
for conformance checking on top of object-centric event logs:


CC1 _Number of Objects related to an Activity_ for _a_ ∈ _A_,
we define for lb _,_ ub ∈ N (lower and upper bound for
the number of related objects)


confnum_obj _(a,_ lb _,_ ub _)_ = { _e_ ∈ _Ea_ | | _πomap(e)_ |

_<_ lb ∨| _πomap(e)_ | _>_ ub}


as the set of events violating the rule.
CC2 _Duration of the Lifecycle_ given lb _,_ ub ∈ R [+] ∪{0}, we
define:


confdur_lif _(_ lb _,_ ub _)_ = { _o_ ∈ _O_ |

_πtime(_ lif _(o)(_ |lif _(o)_ | _))_   - _πtime(_ lif _(o)(_ 1 _)) <_ lb ∨

_πtime(_ lif _(o)(_ |lif _(o)_ | _))_   - _πtime(_ lif _(o)(_ 1 _)) >_ ub}


as the set of objects violating the rule.

