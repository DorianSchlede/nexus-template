<!-- Source: 09-OCEL_20_Specification.pdf | Chunk 1/4 -->

### **OCEL (Object-Centric Event Log) 2.0 Specification**

Alessandro Berti, Istv´an Koren, Jan Niklas Adams,
Gyunam Park, Benedikt Knopp, Nina Graves, Majid Rafiei, Lukas Liß,
Leah Tacke Genannt Unterberg, Yisong Zhang, Christopher Schwanen, Marco Pegoraro,
Wil M.P. van der Aalst


Chair of Process and Data Science, RWTH Aachen University


[ocel@pads.rwth-aachen.de](mailto:ocel@pads.rwth-aachen.de)


**Version:** 2.0
**Date:** October 16, 2023
**Standard Document URL:**
[https://www.ocel-standard.org/2.0/ocel20](https://www.ocel-standard.org/2.0/ocel20_specification.pdf) ~~s~~ pecification.pdf
**Validation Schemes:**

[• XML: https://www.ocel-standard.org/2.0/ocel20-schema-xml.xsd](https://www.ocel-standard.org/2.0/ocel20-schema-xml.xsd)

[• JSON: https://www.ocel-standard.org/2.0/ocel20-schema-json.json](https://www.ocel-standard.org/2.0/ocel20-schema-json.json)

[• Relational: https://www.ocel-standard.org/2.0/ocel20-schema-relational.pdf](https://www.ocel-standard.org/2.0/ocel20-schema-relational.pdf)


**Abstract**


Object-Centric Event Logs (OCELs) form the basis for Object-Centric Process
Mining (OCPM). OCEL 1.0 was first released in 2020 and triggered the development of a range of OCPM techniques. OCEL 2.0 forms the new, more expressive
standard, allowing for more extensive process analyses while remaining in an easily
exchangeable format. In contrast to the first OCEL standard, it can depict changes
in objects, provide information on object relationships, and qualify these relationships to other objects or specific events. Compared to XES, it is more expressive,
less complicated, and better readable. OCEL 2.0 offers three exchange formats: a
relational database (SQLite), XML, and JSON format. This OCEL 2.0 specification document provides an introduction to the standard, its metamodel, and its
exchange formats, aimed at practitioners and researchers alike.


### **Contents**

**1** **Scope and Structure of this Document** **2**


**2** **Introduction to Object-Centric Process Mining** **2**


**3** **Metamodel of the OCEL 2.0 Standard** **4**


**4** **Formal Definitions** **7**


**5** **Running Example** **10**


**6** **Relational SQLite Format** **13**
6.1 Tables for the Distinct Event/Object Types . . . . . . . . . . . . . . . . 15
6.2 Events and Objects Tables . . . . . . . . . . . . . . . . . . . . . . . . . . 16
6.3 Event Type Tables . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 17
6.4 Object Type Tables . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 19
6.5 Event-to-Object (E2O) Relationships . . . . . . . . . . . . . . . . . . . . 21
6.6 Object-to-Object (O2O) Relationships . . . . . . . . . . . . . . . . . . . 22
6.7 Constraints on the Relational Implementation . . . . . . . . . . . . . . . 23


**7** **XML Format** **24**
7.1 XML Example . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 25
7.2 XML Schema Definition . . . . . . . . . . . . . . . . . . . . . . . . . . . 29


**8** **JSON Format** **33**
8.1 JSON Example . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 33
8.2 JSON Schema Definition . . . . . . . . . . . . . . . . . . . . . . . . . . . 42


**9** **Conclusion** **45**


1


### **1 Scope and Structure of this Document**

This document introduces the OCEL 2.0 standard to record and exchange object-centric
event logs. The purpose of the standard is to guide the implementation of conformant
process mining tools, and to provide the basis for the development of training material
and other resources for users.
OCEL 2.0 and its metamodel are designed from the ground up to facilitate the exchange of event logs coming from a wide variety of information systems. Unlike traditional exchange formats, events may refer to any number of objects of different types. It
is intended to be interoperable with data extracted from a wide variety of databases, systems, or applications. Likewise, the format aims to be equally compatible with existing
and emerging Object-Centric Process Mining (OCPM) techniques. It is anticipated that
OCEL 2.0 will become the default exchange format for OCPM tools, whether these are
research prototypes or commercial tools.
This document is structured as follows. Section 2 explains object-centric process
mining and discusses the limitations of current standards for recording object-centric
event logs. Section 3 introduces the OCEL 2.0 standard and discusses its advantages over
past object-centric standardization attempts. Section 4 contains the formal definitions
of the standard. Section 5 illustrates OCEL 2.0 using a running example. Sections 6, 7
and 8 describe the practical implementation of the standard, using relational, XML, and
JSON formats, respectively. Finally, Section 9 concludes this document.

### **2 Introduction to Object-Centric Process Mining**


The first process mining algorithms were developed in the late 1990-ties [1,4]. Initially,
adoption was limited, with just a handful of researchers working on the topic. However,
over time, the field matured. Currently, there are over 40 vendors offering process mining software (cf. `www.processmining.org` ) and advisory firms such as Gartner consider
these to form a new and substantial category of tools [11]. Many of the world’s largest
companies already use process mining to improve their operational processes (across all
economic sectors), and adoption is expected to increase in the coming years. The increasing maturity of the process-mining discipline is also reflected by the success of the
International Conference on Process Mining (ICPM) and the large number of processmining papers in other conferences (e.g., BPM and CAiSE) and journals.
However, traditional process mining considers processes involving single cases, their
events, and event attributes. The approach falls short when dealing with complex, multidimensional processes, where events possibly relate to a variety of entities or _objects_ that
interact and evolve over time [2]. Traditional event data are based on the assumption that
each event refers to precisely one case. The same applies to mainstream process modeling
notations like Directly-Follows-Graphs (DFGs), BPMN models, UML activity diagrams,
workflow nets, and process trees. However, most real-life events involve multiple objects.
Traditional process mining approaches require the _flattening_ of event data in order to
satisfy this assumption. This may lead to misleading analysis results. Process mining
results also tend to become more complex because different objects get intertwined while
trying to straitjacket the processes. Changing the viewpoint (e.g., looking at the process
from a different angle) also implies changing the case notion and going back to the
source systems to extract other event data. This leads to redundancies in event data and
unnecessary repetitions. Moreover, many compliance and performance problems arise at


2


the intersection points of processes, systems, and organizations.
_Object-Centric Process Mining_ (OCPM) represents a paradigm shift, intended to
address and overcome the inherent limitations of traditional case-centric process mining methods [2]. OCPM starts from the actual events and objects that leave traces in
ERP (Enterprise Resource Planning), CRM (Customer Relationship Management), MES
(Manufacturing Execution System), and other IT systems. In the databases of such systems, one-to-one relationships are the exception. Most relationships are one-to-many or
many-to-many. As a result, data need to be transformed to be able to assign events to a
single case, leading to all the problems mentioned before. Therefore, there is consensus
among experienced process miners that _Object-Centric Event Data_ (OCED) provide a
much better abstraction of reality than the classical case-based event logs. OCEL 1.0,
released in 2020 [7], was the first standard for storing OCED and triggered the development of OCPM techniques (e.g., discovering object-centric process models). OCEL 2.0
extends OCEL 1.0, leveraging experiences gathered while developing and applying these
OCPM techniques.
Before discussing in what way OCEL 2.0 extends OCEL 1.0, we first need to introduce
some terminology and basic concepts.


  - _Events_ : Object-centric process mining works on discrete events. They represent
the various actions or activities that occur within a system or process, such as
approving an order, shipping an item, or making a payment. Every event is unique
and corresponds to a specific action or observation at a specific point in time. Events
are atomic (i.e., do not take time), have a timestamp, and may have additional
attributes. Events are typed.


  - _Event Types_ : Events are categorized into different types based on their nature or
function. For example, a procurement process might have event types such as Order
Created, Order Approved, or Invoice Sent. Each type of event represents a specific
kind of action that can take place in the process. Each event is of exactly one type.
Sometimes, we use the term _activity_ to refer to an event type.


  - _Objects_ : In object-centric process mining, objects represent the entities that are
involved in events. These might be physical items like products in a supply chain,
machines, workers, or abstract/information entities like orders, invoices, or contracts in a procurement process. Objects have attributes with values, e.g., prices.
These values may change over time.


  - _Object Types_ : Each object is of one type. The object is an instantiation of its type.
Object types might include categories like Product, Order, Invoice, or Supplier.


Events and objects may be related. In particular, OCPM techniques exploit the
following two relationships.


  - _Event-to-Object (E2O) Relationships_ : Events are associated with objects. This
relationship describes that an object affects an event or that an event affects an
object. In contrast to traditional event logs, events can be related to multiple
objects. Furthermore, these relationships can be qualified differently, describing
the role an object plays in the occurrence of this specific event. Consider, for
example, a meeting event involving multiple participant objects. Using a qualifier,
it is possible to distinguish between regular participants and the organizer of the
meeting.


3


  - _Object-to-Object (O2O) Relationships_ : Objects can also be related to other objects
outside the context of an event. For example, an employee may be part of an
organizational unit. In addition to the mere existence of a relation, this relationship
can also be qualified (e.g., part-of, reports-to, or belongs-to).


Recent standardization attempts have addressed some but not all of these requirements.
The first OCEL format (OCEL 1.0) provided an event log standard that could capture
events related to multiple objects with attributes but did not include Object-to-Object
(O2O) relationship, qualifiers for either O2O and E2O relationships, or changing object
attribute values [7, 8]. OCEL 2.0 addresses these limitations by providing a new metamodel and three storage formats, including a relational implementation of the standard.
We will address OCEL 1.0, its limitations, and how OCEL 2.0 enriches the metamodel
of OCEL 1.0 in more detail in the following section.

### **3 Metamodel of the OCEL 2.0 Standard**


Standards for storing object-centric event data serve as a crucial backbone in managing
and analyzing complex process data. They provide a coherent, uniform, and structured
approach to representing, storing, and exchanging event data across multiple systems,
platforms, and applications. The adoption of a standard has several significant benefits:


  - _Interoperability_ : a standard promotes seamless data interchange between diverse
systems. It eliminates data silos by ensuring that event logs are represented in a
universally understandable format.


  - _Scalability_ : a well-structured standard allows efficient handling of data, enabling it
to scale with increasing complexity and volume. It ensures that the data remains
manageable, reducing the overhead of dealing with unstructured or inconsistently
structured logs.


  - _Data Integrity and Consistency_ : the standardization of event logs upholds the consistency and integrity of data across different sources. It provides a uniform structure to data, making it less prone to inconsistencies and errors, thereby improving
the overall data quality.


  - _Simplifies Analysis_ : by adhering to a standard, the interpretation and analysis of
event logs are significantly simplified. It enables the use of standard analysis tools
and methods, fostering easy comparability and benchmarking of results.


  - _Future-Proofing_ : standards also future-proof data, ensuring that it remains accessible, reusable, and comprehensible even as technologies evolve.


The first comprehensive standard for storing event data was the IEEE Standard for
eXtensible Event Stream (XES) [10]. XES became an official IEEE standard in 2016 [5].
The revised standard (IEEE 1849-2023) was published on 8 September 2023 and will be
valid for another ten years [9]. XES has played a major role in the development of the
field. However, within the process mining community, there seems to be a consensus
that a paradigm shift is needed. The development and adoption of a standard for storing
object-centric event data are vital for realizing the full potential of process mining and


4


other data-driven analytics methods. It paves the way for more effective, efficient, and
reliable data management and analysis strategies.
The first version of the object-centric event log standard, OCEL 1.0, was a big step
forward for object-centric process mining [7,8]. It can store various types of events and
objects in one log and link objects of different types to each event, giving a more detailed
picture. OCEL 1.0 also allowed for adding multiple attributes to each event and object,
providing even more information. This made data analysis deeper and more insightful.
We provided OCEL 1.0 specifications in both JSON and XML formats. Several OCEL
1.0 data sets were provided and the availability of the standard fueled the development
of a range of OCPM techniques, e.g., discovering object-centric Petri nets, discovering
object-centric DFGs, checking conformance on object-centric process models, clustering
object-centric event data, object-centric predictive methods, etc. [2,3,6].
Although OCEL 1.0 can be considered a success, the time has come to extend the
standard. OCEL 1.0 has a few deliberate limitations. In 2020, there were hardly any
OCPM techniques, and the goal was to keep the standard as simple and lean as possible.
However, with the rapid development of the field, the first OCEL standard can now
be perceived as an incomplete solution for object-centric process mining. In 2021, a
survey was conducted by the IEEE Task Force on Process Mining [12]. The goal was
to collect requirements for a new standard succeeding XES. The online survey with 289
participants, spanning the roles of practitioners, researchers, software vendors and endusers, showed the need for supporting object-centricity. This resulted in the so-called
“OCED Working Group” of the IEEE Task Force on Process Mining. Input for the
discussion was an early version of the OCEL 2.0 metamodel (similar to the model in

[2]). Unfortunately, the discussions in the OCED Working Group did not converge after
1.5 years of discussion. This was due to conflicting requirements (expressiveness versus
simplicity), different implementation paradigms (relational versus graph-based), and a
lack of clarity on who would implement things. Therefore, after a delay of two years,
the OCEL team decided to release OCEL 2.0, including example event logs, reference
implementations, libraries, and documentation. OCEL 2.0 aims to strike a middle ground
between simplicity and expressiveness.
Figure 1 shows the meta model using a simplified UML-like notation (just using
classes, associations, and multiplicities). Compared to OCEL 1.0 there are several commonalities. There are objects and events, and these are typed. Events have a timestamp
and any number of additional attributes. Also, objects can have attributes. There is a
many-to-many relationship between events and objects. There are also several differences.
OCEL 2.0 was extended to address the limitations discussed before.


  - _Object-to-Object (O2O) Relationships_ : OCEL 2.0 allows a deeper understanding of
how objects interact within a business process. It shows that objects are part of
a complex network of relationships and actions. Capturing these relationships can
reveal insights about process performance and inefficiencies and allows for advanced
analytics techniques like network analysis and predictive modeling.


  - _Dynamic Object Attribute Values_ : OCEL 2.0 adopts a dynamic approach where
attribute values can change over time. Instead of having a single, fixed value, an
object attribute may have a value that changes during the process. This gives a
more realistic view of process instances by recognizing that object attributes change
over time due to events and progression.


5


Figure 1: OCEL 2.0 metamodel


  - _Relationship Qualifiers_ : OCEL 2.0 offers capabilities to express qualifiers for relationships, both for Object-to-Object (O2O) and Event-to-Object (E2O) relationships. E2O relationship qualifiers describe in which role an object takes part in
an event, while O2O relationship qualifiers can further characterize the association
between two objects.


Apart from these conceptual extensions, the specifications have been enhanced. This
makes the standard more scalable and easier to use in practical situations (e.g., in the
context of a relational database). Notable differences are:


  - _Relational Specification based on Dense Tables_ : One major feature of OCEL 2.0 is
its data structure using dense tables. Each table corresponds to a unique event or
object type, storing only relevant attributes. This results in efficient use of storage
space and less data redundancy. It also scales well, allowing for easy addition of
new event or object types. The separate tables make the data more accessible and
easy to understand, improving both efficiency and analysis in process mining.


  - _Improved XML Specification_ : The XML specification in OCEL 2.0 has been significantly upgraded to handle complex data better. Essential information for events
and objects is now directly within the corresponding tags, making the data more
readable. It also includes the ability to show object-to-object relationships and
track attribute changes over time, providing a better view of how objects evolve.


6


### **4 Formal Definitions**

The metamodel Figure 1 is supported by a formalization that adds more details. The
theoretical foundation is crucial for understanding and using OCEL 2.0. These definitions
form the basis for concrete exchange formats discussed later. The connection between
theory and practice ensures that both the relational model and XML schema respect the
standard’s principles, enhancing its usefulness for object-centric event logging. Readers
will see how these concepts turn into practical solutions, improving their understanding
and use of OCEL 2.0 in process mining. We also encourage authors writing scientific
papers using OCEL 2.0 to adopt these formal definitions and thus improve reliability.
First, Definition 1 introduces some concepts (universes) needed in the remainder.


**Definition 1** (Universes) **.** _Let_ U _Σ be the universe of strings. We define the following_
_pairwise disjoint universes:_


  - U _ev ⊆_ U _Σ is the universe of events._


  - U _etype ⊆_ U _Σ is the universe of event types (i.e., activities)._


  - U _obj ⊆_ U _Σ is the universe of objects._


  - U _otype ⊆_ U _Σ is the universe of object types._


  - U _attr ⊆_ U _Σ is the universe of attribute names._


  - U _val is the universe of attribute values._


  - U _time is the universe of timestamps (with_ 0 _∈_ U _time as the smallest element and_
_∞∈_ U _time as the largest element)_


  - U _qual ⊆_ U _Σ is the universe of qualifiers._


Note that the universes are assumed to be pairwise disjoint, i.e., objects cannot be
used as events, etc. _e ∈_ U _ev_ will be used to denote an event, _et ∈_ U _etype_ will be used to
denote an event type, _o ∈_ U _obj_ will be used to denote an object, _ot ∈_ U _otype_ will be used
to denote an object type, _ea ∈_ U _attr_ will be used to denote an event attribute, _oa ∈_ U _attr_
will be used to denote an object attribute, _v ∈_ U _val_ will be used to denote an attribute
value, _t ∈_ U _time_ will be used to denote a timestamp, and _q ∈_ U _qual_ will be used to denote
a qualifier.
We assume a total ordering on timestamps, with 0 _∈_ U _time_ as the earliest timestamp
and _∞∈_ U _time_ as the latest timestamp (i.e., for any _t ∈_ U _time_ : 0 _≤_ _t ≤∞_ ). These
are added for notational convenience, e.g., we can use 0 for missing timestamps and the
start of the process, and _∞_ as the end time. We would like to emphasize that these two
reference timestamps (i.e., 0 and _∞_ ) are chosen for convenience. In the formalization,
time is mapped on the non-negative reals, but concrete implementations will use, for
example, the ISO 8601 time format.
Definition 2 provides the formal definition for object-centric event logs, describing all
the basic concepts introduced in Section 2 (events, objects, event types, object types,
and event-to-object relationships), and introducing object-to-object relationships and
dynamic object attribute values.


**Definition 2** (OCEL) **.** _An Object-Centric Event Log (OCEL) is a tuple L_ = ( _E, O, EA,_
_OA, evtype, time, objtype, eatype, oatype, eaval, oaval, E2O, O2O_ ) _with_


7


  - _E ⊆_ U _ev is the set of events._


  - _O ⊆_ U _obj is the set of objects._


  - _evtype_ : _E →_ U _etype assigns types to events._


  - _time_ : _E →_ U _time assigns timestamps to events._


  - _EA ⊆_ U _attr is the set of event attributes._


  - _eatype_ : _EA →_ U _etype assigns event types to event attributes._


  - _eaval_ : ( _E × EA_ ) _̸→_ U _val assigns values to event attributes (not all the attributes_
_are mapped for each event)._


  - _objtype_ : _O →_ U _otype assigns types to objects._


  - _OA ⊆_ U _attr is the set of object attributes._


  - _oatype_ : _OA →_ U _otype assigns object types to object attributes._


  - _oaval_ : ( _O × OA ×_ U _time_ ) _̸→_ U _val assigns values to object attributes._


  - _E_ 2 _O ⊆_ _E ×_ U _qual × O are the qualified event-to-object relations._


  - _O_ 2 _O ⊆_ _O ×_ U _qual × O are the qualified object-to-object relations._


_such that_


  - _dom_ ( _eaval_ ) _⊆{_ ( _e, ea_ ) _∈_ _E × EA | evtype_ ( _e_ ) = _eatype_ ( _ea_ ) _} to ensure that only_
_existing event attributes can have values._


  - _dom_ ( _oaval_ ) _⊆{_ ( _o, oa, t_ ) _∈_ _O ×_ _OA_ _×_ U _time | objtype_ ( _o_ ) = _oatype_ ( _oa_ ) _} to ensure that_
_only existing object attributes can have values._


The stipulations embedded in the final two criteria of the definition ensure that each
event and object is limited to possessing attribute values pertinent to its respective event
or object type. Additionally, these guidelines also mandate that the set of attributes is
distinct and non-overlapping for each individual event and object type, guaranteeing a
disjoint attribute set across all types.
In order to facilitate the following examples and explanations, we introduce the following notations given an OCEL _L_ :


  - _ET_ ( _L_ ) = _{_ evtype( _e_ ) _| e ∈_ _E}_ is the set of event types.


  - _OT_ ( _L_ ) = _{_ objtype( _o_ ) _| o ∈_ _O}_ is the set of object types.


  - For any event _e ∈_ _E_ and event attribute ea _∈_ U _attr_ :


**–** eaval _ea_ ( _e_ ) = eaval( _e, ea_ ) if ( _e, ea_ ) _∈_ dom(eaval).


**–** eaval _ea_ ( _e_ ) = _⊥_ if ( _e, ea_ ) _̸∈_ dom(eaval).


  - For any object _o ∈_ _O_, object attribute oa _∈_ U _attr_ and time _t ∈_ U _time_ :


8


**–** oaval _[t]_ _oa_ [(] _[o]_ [) = oaval(] _[o, oa, t][′]_ [) if there exists a] _[ t][′][ ∈]_ [U] _[time]_ [such that] _[ t][′][ ≤]_ _[t]_ [ and]
( _o, oa, t_ _[′]_ ) _∈_ dom(oaval) such that there is no _t_ _[′′]_ _∈_ U _time_ such that _t_ _[′]_ _< t_ _[′′]_ _≤_ _t_
and ( _o, oa, t_ _[′′]_ ) _∈_ dom(oaval).

**–** If no such _t_ _[′]_ exists, then oaval _[t]_ _oa_ [(] _[o]_ [) =] _[ ⊥]_ [.]


Hence, oaval _[t]_ _oa_ [provides us with the latest object attribute value at time] _[ t]_ [.]


  - oaval _oa_ ( _o_ ) = oaval _[∞]_ _oa_ [(] _[o]_ [) is the final value for the object attribute in the event log.]


Note that oaval describes object attribute updates at particular points in time. Function oaval _[t]_ _oa_ [(] _[o]_ [) allows us to determine the value of object attributes at any point in time,]
thus clarifying the semantics. A missing timestamp for a value assignment can be interpreted as time 0. If this is the only value assignment for an object-attribute combination,
then the value for an object attribute is always the same. This way, we can handle static
object-attribute values.



|Col1|Col2|
|---|---|
|object<br>attribute|object<br>attribute|


1




## 1 * event object 1 *




|event type<br>(activity)|1 *|Col3|event<br>attribute|Col5|
|---|---|---|---|---|
|event type<br>(activity)|1<br>*||||



1







has attrib. has attrib.





has type has name has type has name




## * * *
## 1 * attribute object 1 *













for event







for event for object




|Col1|Col2|
|---|---|
|||
||event|


|Col1|* has name|Col3|
|---|---|---|
||<br>||
||event<br>attribute<br>value<br>|event<br>attribute<br>value<br>|


|Col1|object|Col3|
|---|---|---|
||||
||||


|Col1|* has name|Col3|
|---|---|---|
||<br>||
||object<br>attribute<br>value<br><br>|object<br>attribute<br>value<br><br>|





















Figure 2: Linking the OCEL 2.0 metamodel to the formalization in Definition 2.


Object attribute values are deliberately _not_ connected to events. The definition allows
for events without objects or objects without events. Events should correspond to relevant activities, and therefore, there should not be the need to promote individual object
attribute changes to events. Also, the object-to-object relations may exist independent of
events. The only explicit connections between events and objects are the event-to-object
relations (i.e., _E2O_ ). However, for an event _e_ happening at time _t_ involving object _o_
with attribute oa we can look up the corresponding value at the time of the event via
oaval _[t]_ _oa_ [(] _[o]_ [). Hence, there is no limitation.]
Figure 2 links the OCEL metamodel in Figure 1 to the formalization just provided.
Sections 6, 7, and 8 map the formalization onto concrete relational, XML, and JSON
formats.


9


### **5 Running Example**

In order to visualize the concepts of Definition 2 and propose some implementations
of OCEL 2.0, we describe an example object-centric setting supporting the following
situations:


1. A purchase requisition ( **PR1** ) is created and approved, requesting 500 cows, and a
purchase order ( **PO1** ) is created on top of the purchase requisition. The quantity
of the purchase order **PO1** is then changed to 600 cows. Two invoices **R1** and **R2**
are received (for the first 500 cows and for the additional 100 cows), which are paid
separately by the payments **P1** and **P2** .


2. Mario is an unethical employee who places purchase orders of notebooks without
getting proper approval. An invoice **R3** is received before an order **PO2** is formally
inserted in the system. Therefore, Sam, who is a financial controller, blocks the
payment of the invoice. However, Mario manages to override Sam and puts himself
as an approver of the invoice; therefore, the invoice is paid in the **P4** payment.


In this example, the attributes at the object level evolve, highlighting one of the main
features of OCEL 2.0. Also, we provide qualified event-to-object and object-to-object
relationships, specifically in Table 20 and Table 21, highlighting the other main novelties.
For this example:


  - We identify the following sets (in relation to Definition 2):


**–** (sets of objects) _O_ = _{_ **PR1** _,_ **PO1** _,_ **R1** _,_ **R2** _,_ **P1** _,_ **P2** _,_ **R3** _,_ **PO2** _,_ **R3** _,_ **P3** _}_ .


**–** (sets of events) _E_ = _{e_ 1 _, e_ 2 _, e_ 3 _, e_ 4 _, e_ 5 _, e_ 6 _, e_ 7 _, e_ 8 _, e_ 9 _, e_ 10 _, e_ 11 _, e_ 12 _, e_ 13 _}_ .


**–** (sets of attributes at the event level) _EA_ = _{_ pr ~~c~~ reator _,_
pr ~~a~~ pprover _,_ po ~~c~~ reator _,_ po ~~e~~ ditor _,_ invoice ~~i~~ nserter _,_ invoice ~~b~~ locker _,_
invoice ~~b~~ lock ~~r~~ em _,_ payment ~~i~~ nserter _}_ where:


∗ **pr** ~~**c**~~ **reator** is the resource that created the purchase requisition in the
system.
∗ **pr** ~~**a**~~ **pprover** is the resource that approved the purchase requisition in the
system.
∗ **po** ~~**c**~~ **reator** is the resource that created the purchase order in the system.
∗ **po** ~~**e**~~ **ditor** is the resource that changed some parameters of the purchase
order.
∗ **invoice** ~~**i**~~ **nserter** is the resource that inserted the invoice in the system.
∗ **invoice** ~~**b**~~ **locker** is the resource that blocked the payment of a given invoice.
∗ **invoice** ~~**b**~~ **lock** ~~**r**~~ **em** is the resource that removed the payment block.
∗ **payment** ~~**i**~~ **nserter** is the resource that performed the payment.


**–** (sets of attributes at the object level)
_OA_ = _{_ pr ~~p~~ roduct _,_ pr ~~q~~ uantity _,_ po ~~p~~ roduct _,_ po quantity _,_ is ~~b~~ locked _}_ where:


∗ **pr** ~~**p**~~ **roduct** is the product requested in the purchase requisition.
∗ **pr** ~~**q**~~ **uantity** is the quantity requested in the purchase requisition.
∗ **po** ~~**p**~~ **roduct** is the product bought in the purchase order.


10


∗ **po** ~~**q**~~ **uantity** is the quantity bought in the purchase order.
∗ **is** ~~**b**~~ **locked** relates to a payment block on the invoice.


  - The object types corresponding to the given objects (objtype in Definition 2) are
described in Table 1. Moreover, the attributes defined for the object types (oatype
in Definition 2) are also described in Table 1.


  - The event types are described in Table 2, along with the corresponding attributes
(eatype in Definition 2) and event identifiers.


  - A high-level tabular view is provided in Table 3. In particular, the event type
(evtype in Definition 2) and timestamp (time in Definition 2) of each event is
defined.


Table 1: High-level view on the object types of the object-centric event log (running
example).


**Object Type** **Attributes** **Object IDs**


Purchase Requisition pr ~~p~~ roduct, pr ~~q~~ uantity **PR1**
Purchase Order po ~~p~~ roduct, po ~~q~~ uantity **PO1, PO2**
Invoice is ~~b~~ locked **R1, R2, R3**
Payment _∅_ **P1, P2**


Table 2: High-level view on the event types of the object-centric event log (running
example).


**Event Type** **Attributes** **Event IDs**


Create Purchase Requisition pr ~~c~~ reator e1
Approve Purchase Requisition pr ~~a~~ pprover e2
Create Purchase Order po creator e3, e10
Change PO Quantity po editor e4
Insert Invoice invoice ~~i~~ nserter e5, e6, e9
Set Payment Block invoice ~~b~~ locker e11
Remove Payment Block invoice ~~b~~ lock ~~r~~ em e12
Insert Payment payment ~~i~~ nserter e7, e8, e13


11


Table 3: High-level tabular view on the object-centric event log (running example), showing the list of events along with the related objects. In this view, no event/object attribute
is reported, no qualifier is reported (see Table 20 for the event-to-object relationships qualifiers), and no object-to-object relationship is described.


**Event ID** **Event Type** **Timestamp** **Related Objects**


e1 Create Purchase Requisition 2022-01-09 15:00 **PR1**
e2 Approve Purchase Requisition 2022-01-09 16:30 **PR1**
e3 Create Purchase Order 2022-01-10 09:15 **PR1, PO1**
e4 Change PO Quantity 2022-01-13 12:00 **PO1**
e5 Insert Invoice 2022-01-14 12:00 **PO1, R1**
e6 Insert Invoice 2022-01-16 11:00 **PO1, R2**
e7 Insert Payment 2022-01-30 23:00 **R1, P1**
e8 Insert Payment 2022-01-31 22:00 **R2, P2**
e9 Insert Invoice 2022-02-02 09:00 **R3**
e10 Create Purchase Order 2022-02-02 17:00 **R3, PO2**
e11 Set Payment Block 2022-02-03 07:30 **R3**
e12 Remove Payment Block 2022-02-03 23:30 **R3**
e13 Insert Payment 2022-02-28 23:00 **R3, P3**



























Figure 3: General relational schema of the proposed relational implementation.


12


### **6 Relational SQLite Format**

We propose a relational implementation of the standard, which adheres to Definition 2.
In this implementation, starting from an object-centric event log _L_, we have:


  - We have a table, **event** ~~**m**~~ **ap** ~~**t**~~ **ype**, reporting the distinct event types ( _ET_ ( _L_ ));
and a table, **object** ~~**m**~~ **ap** ~~**t**~~ **ype**, reporting the distinct object types ( _OT_ ( _L_ )).


  - We have a table, **event**, reporting the event type (evtype in Definition 2) for each
event, and a table, **object**, reporting the object type (objtype in Definition 2) for
each object. This is described in Subsection 6.2.


  - For every event type in _ET_ ( _L_ ), we have a different table. More specifically, if
et _∈_ _ET_ ( _L_ ) is the event type, we have a table called **event** ~~_⊕_~~ _mapET_ **(et)**, where
_mapET_ : _ET_ ( _L_ ) _→_ U _Σ_ is an injective function [1] mapping the event types to unique
identifiers, containing the events of the given event type along with their timestamp
and attributes. This is described in Subsection 6.3.


  - For every object type in _OT_ ( _L_ ), we have a different table. More specifically, if
_ot ∈_ _OT_ ( _L_ ) is the object type, we have a table called **object** ~~_⊕_~~ _mapOT_ **(ot)**, where
_mapOT_ : _OT_ ( _L_ ) _→_ U _Σ_ is an injective function [2] mapping the object types to unique
identifiers, containing the objects of the given object type along with the history of
their attributes. This is described in Subsection 6.4.


  - We have a table, **event** ~~**o**~~ **bject**, containing the event-to-object relationships (E2O
in Definition 2). This is described in Subsection 6.5.


  - We have a table, **object** ~~**o**~~ **bject**, containing the object-to-object relationships (O2O
in Definition 2). This is described in Subsection 6.6.


A general representation of the relational schema of OCEL 2.0 is portrayed in Figure 3.
The overall relational schema of the running example OCEL 2.0 log is shown in Figure 4.


1Which can be the identity function.
2Which can be the identity function.


13


|event_RemovePaymentBlock event_CreatePurchaseOrder event_CreatePurchaseRequisition<br>ocel_id (PK) ocel_id (PK) ocel_id (PK)<br>ocel_time ocel_time ocel_time<br>invoice_block_rem po_creator pr_creator<br>ocel_id ocel_id<br>ocel_id<br>event_map_type event event_object<br>ocel_type (PK) ocel_id (PK) ocel_event_id (PK)<br>ocel_type_map ocel_type ocel_type ocel_event_id ocel_object_id (PK)<br>ocel_qualifier (PK)<br>ocel_id<br>ocel_id ocel_id<br>ocel_id ocel_id<br>event_ApprovePurchaseRequisition<br>ocel_id (PK)<br>ocel_time<br>pr_approver<br>event_ChangePOQuantity event_InsertInvoice event_SetPaymentBlock event_InsertPayment<br>ocel_id (PK) ocel_id (PK) ocel_id (PK) ocel_id (PK)<br>ocel_time ocel_time ocel_time ocel_time<br>po_editor invoice_inserter invoice_blocker payment_inserter<br>Event Tables|Col2|
|---|---|
|ocel_objec|t_id|
|**object**<br>ocel_id (PK)<br>ocel_type<br>**object_Payment**<br>ocel_id (PK)<br>ocel_time<br>**object_object**<br>ocel_source_id (PK)<br>ocel_target_id (PK)<br>ocel_qualifier (PK)<br>**object_PurchaseRequisition**<br>ocel_id<br>pr_product<br>pr_quantity<br>ocel_time<br>ocel_changed_field<br>**object_PurchaseOrder**<br>ocel_id<br>po_product<br>po_quantity<br>ocel_time<br>ocel_changed_field<br>**object_map_type**<br>ocel_type (PK)<br>ocel_type_map<br>**object_Invoice**<br>ocel_id<br>is_blocked<br>ocel_time<br>ocel_changed_field<br>ocel_type<br>ocel_source_id<br>ocel_target_id<br>ocel_id<br>ocel_id<br>ocel_id<br>ocel_id<br>Object Tables|**object**<br>ocel_id (PK)<br>ocel_type<br>**object_Payment**<br>ocel_id (PK)<br>ocel_time<br>**object_object**<br>ocel_source_id (PK)<br>ocel_target_id (PK)<br>ocel_qualifier (PK)<br>**object_PurchaseRequisition**<br>ocel_id<br>pr_product<br>pr_quantity<br>ocel_time<br>ocel_changed_field<br>**object_PurchaseOrder**<br>ocel_id<br>po_product<br>po_quantity<br>ocel_time<br>ocel_changed_field<br>**object_map_type**<br>ocel_type (PK)<br>ocel_type_map<br>**object_Invoice**<br>ocel_id<br>is_blocked<br>ocel_time<br>ocel_changed_field<br>ocel_type<br>ocel_source_id<br>ocel_target_id<br>ocel_id<br>ocel_id<br>ocel_id<br>ocel_id<br>Object Tables|


Figure 4: Relational schema of the running example OCEL 2.0 log.


14


#### **6.1 Tables for the Distinct Event/Object Types**

In our implementation, we define the table **event** ~~**m**~~ **ap** ~~**t**~~ **ype** (Table 4) defining the
event types along with their unique identifier obtained by applying the injective function
_mapET_ : _ET_ ( _L_ ) _→_ U _Σ_ . This unique identifier is used to link the event type to a table
containing the attributes of the events of the given event type (see Subsection 6.3). The
event type should be set as the primary key to avoid duplication.


Table 4: [Proposed relational implementation] Distinct event types: **event** ~~**m**~~ **ap** ~~**t**~~ **ype**


**ocel** ~~**t**~~ **ype [PK]** **ocel** ~~**t**~~ **ype** ~~**m**~~ **ap**


Approve Purchase Requisition ApprovePurchaseRequisition
Change PO Quantity ChangePOQuantity
Create Purchase Order CreatePurchaseOrder
Create Purchase Requisition CreatePurchaseRequisition
Insert Invoice InsertInvoice
Insert Payment InsertPayment
Remove Payment Block RemovePaymentBlock
Set Payment Block SetPaymentBlock


Also, the table **object** ~~**m**~~ **ap** ~~**t**~~ **ype** (Table 5) defines the object types along with their
unique identifier obtained applying the injective function _mapOT_ : _OT_ ( _L_ ) _→_ U _Σ_ . This
unique identifier is used to link the object type to a table containing the attributes of the
objects of the given object type (see Subsection 6.4). The object type should be set as
the primary key to avoid duplication.


Table 5: Proposed relational implementation: Distinct object types


**ocel** ~~**t**~~ **ype [PK]** **ocel** ~~**t**~~ **ype** ~~**m**~~ **ap**


Invoice Invoice
Payment Payment
Purchase Order PurchaseOrder
Purchase Requisition PurchaseRequisition


15


#### **6.2 Events and Objects Tables**

In the proposed implementation, we use several tables to store information related to
an event/object type. However, we also create two additional tables, hosting the event/object identifiers. This is done to map the event/object to a specific event/object
type table, and to allow for the definition of E2O/O2O tables with proper foreign keys
(directed towards the events and the objects tables).
This is done in Table 6 (having the event identifier, _ocel_ ~~_i_~~ _d_, as primary key) and
Table 7 (having the object identifier, _ocel_ ~~_i_~~ _d_, as primary key).


Table 6: [Proposed Relational Implementation] General Events Table
**event**


**ocel** ~~**i**~~ **d [PK]** **ocel** ~~**t**~~ **ype FK**


e1 Create Purchase Requisition
e2 Approve Purchase Requisition
e3 Create Purchase Order
e4 Change PO Quantity
e5 Insert Invoice
e6 Insert Invoice
e7 Insert Payment
e8 Insert Payment
e9 Insert Invoice
e10 Create Purchase Order
e11 Set Payment Block
e12 Remove Payment Block
e13 Insert Payment


Table 7: [Proposed Relational Implementation] General Objects Table
**object**


**ocel** ~~**i**~~ **d [PK]** **ocel** ~~**t**~~ **ype FK**


PR1 Purchase Requisition
PO1 Purchase Order
PO2 Purchase Order
R1 Invoice
R2 Invoice
R3 Invoice
P1 Payment
P2 Payment


16


#### **6.3 Event Type Tables**

Having defined the table **event** as the general table for the events (having the identifier
of the event as the primary key), we define event-type-specific tables. These allow for the
storage of event-type-specific attributes without having a gigantic “sparse table” hosting
all the events with all the different attributes (with an empty value for most of them).
Therefore, if _et ∈_ _ET_ ( _L_ ) is the event type, we have a table called **event** ~~_⊕_~~ _mapET_ **(et)**,
where _mapET_ : _ET_ ( _L_ ) _→_ U _Σ_ is an injective function [3] mapping the event types to unique
identifiers, containing the events of the given event type along with their timestamp and
attributes. In particular, all the attributes associated with the given event type (eatype
in Definition 2) are columns of the table, and the values for each event are populated
accordingly (eaval in Definition 2). Moreover, the timestamp is a column of the eventtype-specific tables. The event identifier column is pointing (as a foreign key) to the
event identifier column of the **event** table. Examples follow (Table 8, Table 9, Table 10,
Table 11, Table 12, Table 13, Table 14, Table 15) for all the event types of the running
example log.


Table 8: [Proposed relational implementation] Event Type Table:
**event** ~~**C**~~ **reatePurchaseRequisition**


**ocel** ~~**i**~~ **d [PK] [FK]** **ocel** ~~**t**~~ **ime** **pr** ~~**c**~~ **reator**


e1 2022-01-09 15:00 Mike


Table 9: [Proposed relational implementation] Event type table:
**event** ~~**A**~~ **pprovePurchaseRequisition**


**ocel** ~~**i**~~ **d [PK] [FK]** **ocel** ~~**t**~~ **ime** **pr** ~~**a**~~ **pprover**


e2 2022-01-09 16:30 Tania


Table 10: [Proposed relational implementation] Event type table:
**event** ~~**C**~~ **reatePurchaseOrder**


**ocel** ~~**i**~~ **d [PK] [FK]** **ocel** ~~**t**~~ **ime** **po** ~~**c**~~ **reator**
