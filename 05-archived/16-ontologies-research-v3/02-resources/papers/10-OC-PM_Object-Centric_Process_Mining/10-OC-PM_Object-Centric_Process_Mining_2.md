<!-- Source: 10-OC-PM_Object-Centric_Process_Mining.pdf | Chunk 2/2 -->

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


The rule CC1 is useful to identify situations where an
excessive number of objects is worked by an activity. For
example, we can think of an activity “Approve Expense
Report” which usually involves a limited number of expense
reports. If an event with the activity “Approve Expense
Report” involves 50 different reports, CC1 is useful to identify the given event. The rule CC2 is helpful in identifying
objects with an extremely long lifecycle. As an example, if
a ticket is supposed to be approved in one week, while it is
still not closed after one month, CC2 is useful for identifying
the given ticket (object).
Figure 2 proposes a visualization of the rule CC1 and
Fig. 3 provides a visualization of the rule CC2. For both, we
assume that the event log is filtered on the different object
types, and the rules are applied to the filtered logs. For CC1,
we calculate for each activity the average _μ_ and the standard

## 123


A. Berti, W. M. P. van der Aalst



**Fig. 2** Conformance checking based on the number of related objects (in the web-based tool proposed in Sect. 4.1)


**Fig. 3** Conformance checking based on the objects lifecycle duration (in the web-based tool proposed in Sect. 4.1)



deviation _σ_ of the number of related objects for the events
of the given activity. Then, we assume that every event of
the given activity having a number of related objects that
is lower than _μ_ - _ζ_ ∗ _σ_ or higher than _μ_ + _ζ_ ∗ _σ_ (where
_ζ_ ∈ R [+] ∪{0} is a positive number) are anomalous [8] . For
CC2, we calculate for each object the average _μ_ and the
standard deviation _σ_ of the duration of the lifecycle of the
object. Then, we assume that every object having a duration
of the lifecycle that is lower than _μ_ - _ζ_ ∗ _σ_ or higher than
_μ_ + _ζ_ ∗ _σ_ (where _ζ_ ∈ R [+] ∪{0} is a positive number) are
anomalous [9] . For both rules, it is possible to filter the object

8 Choosing _ζ_ = 1 includes all the events for which the number of
related objects is more deviant than one standard deviation from the
average. Choosing _ζ_ = 6 includes all the events for which the number
of related objects is more deviant than six standard deviations from the
average.

9 Choosing _ζ_ = 1 includes all the objects for which the duration of
the lifecycle is more deviant than one standard deviation from the

## 123



centric event log, keeping respectively only the anomalous
events and the anomalous objects.


**4 Tool**


Thissectionpresentstwotoolsupportsfortheprocessdiscovery techniques proposed in this paper: a web-based tool and
an implementation on top of the ProM process mining frame[work. These are available and described at https://ocpm.info.](https://ocpm.info)
Along with process discovery, both tools support flattening
and filtering. In particular, the web-based tool also supports
conformance checking and statistics on object-centric event
logs.


Footnote 9 continued
average. Choosing _ζ_ = 6 includes all the objects for which the duration
of the lifecycle is more deviant than six standard deviations from the
average (six sigma principle).


OC-PM: analyzing object...


**Fig. 4** Overall view over the
process model page of the
proposed web-based tool


**4.1 OC-PM (Web-based tool)**


We present a novel tool for object-centric process mining,
OC-PM, which enables the object-centric process mining
analyses presented in this paper. The tool is available at the
[address https://ocpm.info and consists of HTML/Javascript](https://ocpm.info)



content that can be downloaded and promptly run in the
browser without any backend. The first page of the tool
enables the upload of an object-centric event log in the JSONOCEL or XML-OCEL formats [10] .


10 [Some of these logs are available at the address http://www.ocel-](http://www.ocel-standard.org/)
[standard.org/](http://www.ocel-standard.org/)

## 123


The tool consists of different pages, including the _Process_
_Schema_ (which visualizes a process model with the possibility to interact with it), the _Events_ page (which visualizes
the list of events contained in the object-centric event log,
with the possibility to focus on the events belonging to the
lifecycle of an object), the _Objects_ page (the list of objects of
the log having a given object type is shown, along with their
lifecycle, the duration of the lifecycle, and other statistics),
the _Statistics_ page (showing some generic graphs including
the number of related objects per object type, the number of
events per activity, the number of related objects per event,
the distribution of the length of the lifecycle of objects, the
distribution of the events during the time, the dotted chart),
the _Conformance_ page (providing some conformance checking functionalities).
Figure 4 shows the process model page of the proposed
tool. The page is organized as follows:


 - The top menu presents the different pages/features of the
application.

 - The second menu presents some options, shown in Fig.

4(1), including the type of the process model:


   - Object-centricdirectly-followsmultigraphs(described
in Sect. 3.3).

   - Object-centric Petri nets [8]. In particular, the decorations are obtained using the token-based replay
technique described in [9].


and the type of annotation:


   - With the _E/EC_ option, the process model is annotated
using the measure E for the activities and the measure
EC for the edges.

  - With the _UO_ option, the process model is annotated
using the measure UO for the activities and the edges.

  - With the _TO_ option, the process model is annotated
using the measure TO for the activities and the edges.


Moreover, the filtering on object types, along with a filters
chain functionality (which shows the active filters, with
the possibility to remove them), is implemented in this
menu (see Fig. 4(2-3)).

 - The left panel shows the number of events, unique
objects, and total objects of the overall log (see Def. 8).
Moreover, a _sliding_ functionality is offered, keeping only
the most frequent activities/edges (this is done for OCDFGs using the approach described in Def. 17).

 - The right panel shows the process model.


The process model page permits interaction with the activities and the edges. The filtering approaches F1-7 presented
in Def. 14 are all implemented in the tool. Figure 4(4-5)
shows the interaction menus when an activity and an edge
are clicked, respectively. It is possible to apply the filtering,

## 123



A. Berti, W. M. P. van der Aalst


or to observe the list of objects related to the activity and
edge.
Figure 5 and 6 show some of the statistics that can be
computed on object-centric event logs. Among the additional
features, the download of the filtered event log in the JSONOCEL or XML-OCEL is available, and the possibility to
flatten the object-centric event log to a traditional event log
saved in the XES format is offered (Fig. 7).


**4.2 OC-PM (ProM framework)**


We present another implementation of the process discovery techniques proposed in this paper, on top of the popular
process mining framework ProM 6.x [11] . The implementation is proposed in the package OCELStandard [12], which
can be downloaded using the package manager of ProM.
An object-centric event log, in the JSON-OCEL or XMLOCEL formats, can be imported in ProM using the import
button on the top right. After importing, some object-centric
process mining features are available on top of the objectcentric event log: flattening to an object type and process
discovery (object-centric directly-follows multigraphs and
object-centric Petri nets [13] ). Opening the process discovery
plugin, a visualization of an object-centric directly-follows
multigraph with a default choice for the activity/path sliders
is proposed. The notation is analogous to the one of the webbased tool presented in the previous subsection. The user can
interact with the diagram by clicking on the nodes (activities)
and edges of the directly-follows multigraph. The values for
the activity/path sliders can be changed on the top panel. The
user can also apply some filters on the object-centric event
log starting from the top panel.


**5 Related work**


This section presents the related work on object-centric process mining.


**5.1 Artifact-centric approaches**


Artifact-centric process mining is based on defining the
properties of key business-relevant entities called business
artifacts. In particular, the proposed techniques focus on the
modeling of the single artifacts and their interactions. In [10],
two-phases conformance checking approach is proposed, in
which the conformance is checked both in the single artifacts


11 [https://www.promtools.org/doku.php?id=prom611](https://www.promtools.org/doku.php?id=prom611)

[12 https://svn.win.tue.nl/repos/prom/Packages/OCELStandard/](https://svn.win.tue.nl/repos/prom/Packages/OCELStandard/Trunk/)
[Trunk/](https://svn.win.tue.nl/repos/prom/Packages/OCELStandard/Trunk/)

13 The decorations are obtained using the token-based replay technique
described in [9].


OC-PM: analyzing object...


**Fig. 5** Statistic proposed in the
web-based tool: number of
objects per type


**Fig. 6** Statistic proposed in the web-based tool: length of the lifecycle


both in the interactions between them. In [11], an approach
to discover the artifacts and their lifecycle from a relational
database is proposed. This is done by identifying the artifacts and extracting event logs for each artifact. In [12], the
discovery of artifact-centric models on top of the SAP ERP
system is discussed. A limitation of these approaches is the
lack of comprehensive tool support and the dependence on a
relational database schema.



**5.2 Object-centric behavioral constraint models**


In [13], the _object-centric behavioral constraint models_
(OCBC) are proposed as declarative models with rich semantics that can describe the interaction between the different
entities of a database and the activities recorded in an objectcentriceventlogwiththefeaturesdescribedin[14].However,
the discovery of the rich set of constraints and the proposed
event log format (storing the entire state of the object model
for each event) have scalability issues.

## 123


A. Berti, W. M. P. van der Aalst


**Fig. 7** Implementation of the object-centric process discovery techniques as plug-in of the ProM process mining framework



**5.3 Petri nets-based approaches**


Colored Petri nets [15] have been proposed in the ’80 and
have a wide range of applications. Colored Petri nets allow
the storage of a data value for each token. The data value
is called the token color. Every place contains tokens of
one type, which is referred to as the color set of the place.
Moreover, expressions are defined at the arc level for consumption/production purposes, and some guards can control
the execution of the transitions. Given their rich semantics,
the proposal of a process discovery algorithm able to manage colors, color sets, expressions, and guards is an enormous
challenge. In [16], colored Petri nets are extended (with the
name catalog-nets) to accommodate processes with several
cases that need to co-evolve flexibly.
In [17], three concepts are provided to describe the behavior of processes with many-to-many interactions:


 - Unbounded dynamic synchronization of transitions.

 - Cardinality constraints limit the size of the synchronization.

 - Correlation of the token identities based on history.


**5.4 Graph and process querying**


In [18,19], the usage of graph databases for the storage,
querying, and aggregation of object-centric event data is proposed. An object-centric event log is inserted in the graph by

## 123



creating nodes for the events, objects, object types, attributes
of the event log, and connections are created based on the
content of the log. In [20], an algorithm for the discovery
of directly-follows graphs on top of graph databases is proposed. However, the scalability of graph databases on process
mining tasks still needs to be investigated thoroughly. In [20],
the execution time of process mining tasks in a popular graph
database (Neo4J) is shown to be disappointing.
In [21], a query language to analyze the execution of business processes is proposed. An approach for ontology-based
extraction of event data has been proposed in [22].


**5.5 Flattening-based process discovery**


A discovery operation can be defined by flattening (see Def.
11) the object-centric event log into the different object types,
discovering traditional process models (as an example, a
DFG or a Petri net) on top of the flattened logs and then
collating the results together. Different process models can
serve as building blocks and have been proposed in the literature:


 - _Object-centric directly-follows graphs_ : in [7], the usage
of object-centric directly-follows multigraphs is proposed to describe the activities of an object-centric event
log, and the interactions between them.

 - _Object-centric Petri nets_ : in [8], object-centric Petri nets
have been proposed to support a subset of the semantics


OC-PM: analyzing object...


of colored Petri nets. A discovery approach is proposed
starting from object-centric event logs, in which a flattened log is obtained for each object type, a mainstream
process discovery algorithm (such as the alpha miner or
the inductive miner) is applied on top of the flattened
log, and the Petri nets are then collated together into an
object-centric Petri net. In the model, every place and arc
is associated with a unique object type, and an arc can be
allowed to consume/produce a single or multiple tokens.


**5.6 Other approaches**


Some object-centric process models have been proposed in

[23,24], however the tool support/assessment is lacking.
The relationship between interconnected processes has
been investigated. In [25], a token-based interaction monitoring framework is proposed. In [26], instance-spanning
constraints are discovered from event logs, which regulate
the start of the process instances. In [27], object-state transitions are proposed to improve business process intelligence.
Although all these approaches are useful for conformance
checking, they do not result in a comprehensive process
model. In [28], multi-instance mining has been proposed,
along with an implementation in the ProM framework that
can show the interaction between the states visually.


**6 Conclusion**


The current paper describes a set of object-centric process
mining techniques which can be used to analyze objectcentric event logs extracted from mainstream information
systems (such as SAP ERP). The definition of object-centric
event logs, and the introduction of the OCEL format, permit the introduction of some operations both at the formal
level both in tools/libraries supporting OCEL. The operations of flattening (projecting the object-centric event log to
a traditional event log after the choice of an object type)
and filtering (activities, paths, endpoints, timeframe, object
types) are important for the development of more advanced
object-centric process mining techniques. In particular, the
flattening operation is an essential operation for process discovery.
The paper also proposes an object-centric process model
(the object-centric directly-follows multigraph, OC-DFG),
which can be straightforwardly discovered from objectcentric event logs, and easily annotated with frequency
measures. Moreover, several frequency measures for the
activities and the paths of the event log are introduced,
which can be used as annotations for OC-DFGs and other
types of object-centric process models. Eventually, some
conformance checking approaches for object-centric event



logs are introduced, which verify some properties of the
events/objects of the log.
Comprehensive tool support, which is available as a web
interface and as plugin in the ProM framework, is offered for
the ingestion, exploration, and discovery of OC-DFGs and of
object-centric Petri nets [8], statistical analysis, and conformance checking. To the best of the authors’ knowledge, this
is the first attempt to provide comprehensive tool support in
the object-centric setting.
There are several points of interest in object-centric process mining not discussed in the current paper, including
a more precise visualization of the interactions between
different objects and model-based conformance checking.
Moreover, an assessment of the proposed techniques on reallife event logs is missing from the current paper. As the
discipline is still young, these points can be developed in
future work.


**Funding** Open Access funding enabled and organized by Projekt
DEAL.


**Open Access** This article is licensed under a Creative Commons
Attribution 4.0 International License, which permits use, sharing, adaptation, distribution and reproduction in any medium or format, as
long as you give appropriate credit to the original author(s) and the
source, provide a link to the Creative Commons licence, and indicate if changes were made. The images or other third party material
in this article are included in the article’s Creative Commons licence,
unless indicated otherwise in a credit line to the material. If material
is not included in the article’s Creative Commons licence and your
intended use is not permitted by statutory regulation or exceeds the
permitteduse,youwillneedtoobtainpermissiondirectlyfromthecopy[right holder. To view a copy of this licence, visit http://creativecomm](http://creativecommons.org/licenses/by/4.0/)
[ons.org/licenses/by/4.0/.](http://creativecommons.org/licenses/by/4.0/)


**References**


1. van der Aalst, W.M.P.: Process mining - data science in action,
[second Edition. Springer, New York City (2016). https://doi.org/](https://doi.org/10.1007/978-3-662-49851-4)
[10.1007/978-3-662-49851-4](https://doi.org/10.1007/978-3-662-49851-4)
2. van der Aalst, W.M.P.: Object-Centric Process Mining: Dealing
with Divergence and Convergence in Event Data. In: Ölveczky,
P.C., Salaün, G. (eds.) Software Engineering and Formal Methods - 17th International Conference, SEFM 2019, Oslo, Norway,
September 18-20, 2019, Proceedings. Lecture Notes in Computer
Science, vol. 11724, pp. 3–25. Springer, New York City (2019).
[https://doi.org/10.1007/978-3-030-30446-1_1](https://doi.org/10.1007/978-3-030-30446-1_1)
3. Adams, J.N., van der Aalst, W.M.P.: Oc _π_ : Object-centric process
insights. In: Bernardinello, L., Petrucci, L. (eds.) Application and
Theory of Petri Nets and Concurrency - 43rd International Conference, PETRI NETS 2022, Bergen, Norway, June 19-24, 2022,
Proceedings. Lecture Notes in Computer Science, vol. 13288, pp.
139–150.Springer,NewYork(2022). [https://doi.org/10.1007/978-](https://doi.org/10.1007/978-3-031-06653-5_8)
[3-031-06653-5_8](https://doi.org/10.1007/978-3-031-06653-5_8)
4. Ghahfarokhi, A.F., Park, G., Berti, A., van der Aalst, W.M.P.:
OCEL: A standard for object-centric event logs. In: Bellatreche,
L., Dumas, M., Karras, P., Matulevicius, R., Awad, A., Weidlich, M., Ivanovic, M., Hartig, O. (eds.) New Trends in Database
and Information Systems - ADBIS 2021 Short Papers, Doc
## 123


toral Consortium and Workshops: DOING, SIMPDA, MADEISD,
MegaData, CAoNS, Tartu, Estonia, August 24-26, 2021, Proceedings. Communications in Computer and Information Science, vol.
[1450, pp. 169–175. Springer, New York City (2021). https://doi.](https://doi.org/10.1007/978-3-030-85082-1_16)
[org/10.1007/978-3-030-85082-1_16](https://doi.org/10.1007/978-3-030-85082-1_16)
5. Berti, A., Farhang, A., Park, G., van der Aalst, W.M.P.: A scalable
database for the storage of object-centric event logs. In: ICPM 2021
DoctoralConsortiumandDemoTrack2021.CEURWorkshopProceedings, vol. 3098, pp. 19–20. CEUR-WS.org, Sun SITE Central
[Europe (2021). http://ceur-ws.org/Vol-3098/demo_137.pdf](http://ceur-ws.org/Vol-3098/demo_137.pdf)
6. Berti, A., van der Aalst, W.M.P.: Starstar models: Using events at
database level for process analysis. In: Ceravolo, P., López, M.T.G.,
van Keulen, M. (eds.) Proceedings of the 8th International Symposium on Data-driven Process Discovery and Analysis (SIMPDA
2018), Seville, Spain, December 13-14, 2018. CEUR Workshop
Proceedings, vol. 2270, pp. 60–64. CEUR-WS.org, Sun SITE Cen[tral Europe (2018). http://ceur-ws.org/Vol-2270/short3.pdf](http://ceur-ws.org/Vol-2270/short3.pdf)
7. Berti, A., van der Aalst, W.M.P.: Extracting Multiple Viewpoint
Models from Relational Databases. In: Ceravolo, P., van Keulen,
M., López, M.T.G. (eds.) Data-Driven Process Discovery and
Analysis - 8th IFIP WG 2.6 International Symposium, SIMPDA
2018, Seville, Spain, December 13-14, 2018, and 9th International
Symposium, SIMPDA 2019, Bled, Slovenia, September 8, 2019,
Revised Selected Papers. Lecture Notes in Business Information
Processing, vol. 379, pp. 24–51. Springer, New York City (2019).
[https://doi.org/10.1007/978-3-030-46633-6_2](https://doi.org/10.1007/978-3-030-46633-6_2)
8. van der Aalst, W.M.P., Berti, A.: Discovering object-centric petri
nets. Fundam. Informaticae **175** [(1–4), 1–40 (2020). https://doi.org/](https://doi.org/10.3233/FI-2020-1946)
[10.3233/FI-2020-1946](https://doi.org/10.3233/FI-2020-1946)
9. Berti, A., van der Aalst, W.M.P.: A novel token-based replay technique to speed up conformance checking and process enhancement.
Trans. Petri Nets Other Model. Concurr. **15** [, 1–26 (2021). https://](https://doi.org/10.1007/978-3-662-63079-2_1)
[doi.org/10.1007/978-3-662-63079-2_1](https://doi.org/10.1007/978-3-662-63079-2_1)
10. Fahland, D., de Leoni, M., van Dongen, B.F., van der Aalst, W.M.P.:
Behavioral Conformance of Artifact-Centric Process Models. In:
Abramowicz, W. (ed.) Business Information Systems - 14th International Conference, BIS 2011, Poznan, Poland, June 15-17, 2011.
Proceedings. Lecture Notes in Business Information Processing,
[vol. 87, pp. 37–49. Springer, New York City (2011). https://doi.](https://doi.org/10.1007/978-3-642-21863-7_4)
[org/10.1007/978-3-642-21863-7_4](https://doi.org/10.1007/978-3-642-21863-7_4)
11. Nooijen, E.H.J., van Dongen, B.F., Fahland, D.: Automatic Discovery of Data-Centric and Artifact-Centric Processes. In: Rosa,
M.L., Soffer, P. (eds.) Business Process Management Workshops BPM2012InternationalWorkshops,Tallinn,Estonia,September3,
2012. Revised Papers. Lecture Notes in Business Information Processing, vol. 132, pp. 316–327. Springer, New York City (2012).
[https://doi.org/10.1007/978-3-642-36285-9_36](https://doi.org/10.1007/978-3-642-36285-9_36)
12. Lu, X., Nagelkerke, M., van de Wiel, D., Fahland, D.: Discovering
interacting artifacts from ERP systems. IEEE Trans. Serv. Comput.
**8** [(6), 861–873 (2015). https://doi.org/10.1109/TSC.2015.2474358](https://doi.org/10.1109/TSC.2015.2474358)
13. Li, G., de Carvalho, R.M., van der Aalst, W.M.P.: Object-centric
behavioral constraint models: a hybrid model for behavioral and
data perspectives. In: Hung, C., Papadopoulos, G.A. (eds.) Proceedings of the 34th ACM/SIGAPP Symposium on Applied
Computing, SAC 2019, Limassol, Cyprus, April 8-12, 2019, pp.
[48–56. ACM, New York (2019). https://doi.org/10.1145/3297280.](https://doi.org/10.1145/3297280.3297287)
[3297287](https://doi.org/10.1145/3297280.3297287)
14. Li, G., de Murillas, E.G.L., de Carvalho, R.M., van der Aalst,
W.M.P.: Extracting Object-Centric Event Logs to Support Process
Mining on Databases. In: Mendling, J., Mouratidis, H. (eds.) Information Systems in the Big Data Era - CAiSE Forum 2018, Tallinn,
Estonia, June 11-15, 2018, Proceedings. Lecture Notes in Business
Information Processing, vol. 317, pp. 182–199. Springer, New York
[City (2018). https://doi.org/10.1007/978-3-319-92901-9_16](https://doi.org/10.1007/978-3-319-92901-9_16)

## 123



A. Berti, W. M. P. van der Aalst


15. Peterson, J.L.: A Note on Colored Petri Nets. Inf. Process. Lett. **11** [(1), 40–43 (1980). https://doi.org/10.1016/0020-](https://doi.org/10.1016/0020-0190(80)90032-0)
[0190(80)90032-0](https://doi.org/10.1016/0020-0190(80)90032-0)
16. Ghilardi, S., Gianola, A., Montali, M., Rivkin, A.: Petri Nets with
Parameterised Data - Modelling and Verification. In: Fahland, D.,
Ghidini,C.,Becker,J.,Dumas,M.(eds.)BusinessProcessManagement - 18th International Conference, BPM 2020, Seville, Spain,
September 13-18, 2020, Proceedings. Lecture Notes in Computer
Science, vol. 12168, pp. 55–74. Springer, New York City (2020).
[https://doi.org/10.1007/978-3-030-58666-9_4](https://doi.org/10.1007/978-3-030-58666-9_4)
17. Fahland, D.: Describing Behavior of Processes with Many-toMany Interactions. In: Donatelli, S., Haar, S. (eds.) Application and
Theory of Petri Nets and Concurrency - 40th International Conference, PETRI NETS 2019, Aachen, Germany, June 23-28, 2019,
Proceedings. Lecture Notes in Computer Science, vol. 11522, pp.
[3–24. Springer, New York City (2019). https://doi.org/10.1007/](https://doi.org/10.1007/978-3-030-21571-2_1)
[978-3-030-21571-2_1](https://doi.org/10.1007/978-3-030-21571-2_1)
18. Esser, S., Fahland, D.: Storing and Querying Multi-dimensional
Process Event Logs Using Graph Databases. In: Francescomarino,
C.D., Dijkman, R.M., Zdun, U. (eds.) Business Process Management Workshops - BPM 2019 International Workshops, Vienna,
Austria, September 1-6, 2019, Revised Selected Papers. Lecture
Notes in Business Information Processing, vol. 362, pp. 632–644.
[Springer, New York City (2019). https://doi.org/10.1007/978-3-](https://doi.org/10.1007/978-3-030-37453-2_51)
[030-37453-2_51](https://doi.org/10.1007/978-3-030-37453-2_51)
19. Esser, S., Fahland, D.: Multi-Dimensional Event Data in Graph
Databases. J. Data Semant. **10** [(1), 109–141 (2021). https://doi.org/](https://doi.org/10.1007/s13740-021-00122-1)
[10.1007/s13740-021-00122-1](https://doi.org/10.1007/s13740-021-00122-1)
20. Jalali, A.: Graph-Based Process Mining. In: Leemans, S.J.J.,
Leopold, H. (eds.) Process Mining Workshops - ICPM 2020 International Workshops, Padua, Italy, October 5-8, 2020, Revised
Selected Papers. Lecture Notes in Business Information Process[ing, vol. 406, pp. 273–285. Springer, New York City (2020). https://](https://doi.org/10.1007/978-3-030-72693-5_21)
[doi.org/10.1007/978-3-030-72693-5_21](https://doi.org/10.1007/978-3-030-72693-5_21)
21. Beheshti, S., Benatallah, B., Nezhad, H.R.M., Sakr, S.: A
Query Language for Analyzing Business Processes Execution. In:
Rinderle-Ma, S., Toumani, F., Wolf, K. (eds.) Business Process
Management-9thInternationalConference,BPM2011,ClermontFerrand, France, August 30 - September 2, 2011. Proceedings.
Lecture Notes in Computer Science, vol. 6896, pp. 281–297.
[Springer, New York City (2011). https://doi.org/10.1007/978-3-](https://doi.org/10.1007/978-3-642-23059-2_22)
[642-23059-2_22](https://doi.org/10.1007/978-3-642-23059-2_22)
22. Calvanese, D., Montali, M., Syamsiyah, A., van der Aalst,
W.M.P.: Ontology-Driven Extraction of Event Logs from Relational Databases. In: Reichert, M., Reijers, H.A. (eds.) Business
Process Management Workshops - BPM 2015, 13th International
Workshops, Innsbruck, Austria, August 31 - September 3, 2015,
Revised Papers. Lecture Notes in Business Information Processing,
[vol. 256, pp. 140–153. Springer, New York City (2015). https://doi.](https://doi.org/10.1007/978-3-319-42887-1_12)
[org/10.1007/978-3-319-42887-1_12](https://doi.org/10.1007/978-3-319-42887-1_12)
23. Steinau, S., Künzle, V., Andrews, K., Reichert, M.: Coordinating
Business Processes Using Semantic Relationships. In: Loucopoulos, P., Manolopoulos, Y., Pastor, O., Theodoulidis, B., Zdravkovic,
J. (eds.) 19th IEEE Conference on Business Informatics, CBI 2017,
Thessaloniki, Greece, July 24-27, 2017, Volume 1: Conference
Papers, pp. 33–42. IEEE Computer Society, New York City (2017).
[https://doi.org/10.1109/CBI.2017.53](https://doi.org/10.1109/CBI.2017.53)
24. Steinau, S., Andrews, K., Reichert, M.: The Relational Process
Structure. In: Krogstie, J., Reijers, H.A. (eds.) Advanced Information Systems Engineering - 30th International Conference, CAiSE
2018, Tallinn, Estonia, June 11-15, 2018, Proceedings. Lecture
Notes in Computer Science, vol. 10816, pp. 53–67. Springer, New
[York City (2018). https://doi.org/10.1007/978-3-319-91563-0_4](https://doi.org/10.1007/978-3-319-91563-0_4)
25. Li, C., Ge, J., Li, Z., Huang, L., Yang, H., Luo, B.: Monitoring
interactionsacrossmultibusinessprocesseswithtokencarrieddata.


OC-PM: analyzing object...


IEEE Trans. Serv. Comput. **12** [(6), 941–954 (2019). https://doi.org/](https://doi.org/10.1109/TSC.2016.2645690)
[10.1109/TSC.2016.2645690](https://doi.org/10.1109/TSC.2016.2645690)
26. Winter, K., Stertz, F., Rinderle-Ma, S.: Discovering instance and
process spanning constraints from process execution logs. Inf. Syst.
**89** [, 101484 (2020). https://doi.org/10.1016/j.is.2019.101484](https://doi.org/10.1016/j.is.2019.101484)
27. Herzberg, N., Meyer, A., Weske, M.: Improving business process
intelligence by observing object state transitions. Data Knowl. Eng.
**98** [, 144–164 (2015). https://doi.org/10.1016/j.datak.2015.07.008](https://doi.org/10.1016/j.datak.2015.07.008)
28. van Eck, M.L., Sidorova, N., van der Aalst, W.M.P.: Multiinstance Mining: Discovering Synchronisation in Artifact-Centric
Processes. In: Daniel, F., Sheng, Q.Z., Motahari, H. (eds.) Business
Process Management Workshops - BPM 2018 International Workshops, Sydney, NSW, Australia, September 9-14, 2018, Revised
Papers. Lecture Notes in Business Information Processing, vol.
[342, pp. 18–30. Springer, New York City (2018). https://doi.org/](https://doi.org/10.1007/978-3-030-11641-5_2)
[10.1007/978-3-030-11641-5_2](https://doi.org/10.1007/978-3-030-11641-5_2)



**Publisher’s Note** Springer Nature remains neutral with regard to jurisdictional claims in published maps and institutional affiliations.

## 123


