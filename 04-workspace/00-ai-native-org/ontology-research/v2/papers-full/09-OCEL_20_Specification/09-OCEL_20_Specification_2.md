<!-- Source: 09-OCEL_20_Specification.pdf | Chunk 2/4 -->



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


e3 2022-01-10 09:15 Mike
e10 2022-02-02 17:00 Mario


3Which can be the identity function.


17


Table 11: [Proposed relational implementation] Event type table:
**event** ~~**C**~~ **hangePOQuantity**


**ocel** ~~**i**~~ **d [PK] [FK]** **ocel** ~~**t**~~ **ime** **po** ~~**e**~~ **ditor**


e4 2022-01-13 12:00 Mike


Table 12: [Proposed relational implementation] Event type table: **event** ~~**I**~~ **nsertInvoice**


**ocel** ~~**i**~~ **d [PK] [FK]** **ocel** ~~**t**~~ **ime** **invoice** ~~**i**~~ **nserter**


e5 2022-01-14 12:00 Luke
e6 2022-01-16 11:00 Luke
e9 2022-02-02 09:00 Mario


Table 13: [Proposed relational implementation] Event type table:
**event** ~~**S**~~ **etPaymentBlock**


**ocel** ~~**i**~~ **d [PK] [FK]** **ocel** ~~**t**~~ **ime** **invoice** ~~**b**~~ **locker**


e11 2022-02-03 07:30 Sam


Table 14: [Proposed relational implementation] Event type table:
**event** ~~**R**~~ **emovePaymentBlock**


**ocel** ~~**i**~~ **d [PK] [FK]** **ocel** ~~**t**~~ **ime** **invoice** ~~**b**~~ **lock** ~~**r**~~ **em**


e12 2022-02-03 23:30 Mario


Table 15: [Proposed relational implementation] Event type table:
**event** ~~**I**~~ **nsertPayment**


**ocel** ~~**i**~~ **d [PK] [FK]** **ocel** ~~**t**~~ **ime** **payment** ~~**i**~~ **nserter**


e7 2022-01-30 23:00 Robot
e8 2022-01-31 22:00 Robot
e13 2022-02-28 23:00 Robot


18


#### **6.4 Object Type Tables**

Having defined the table **object** as the general table for the objects (having the identifier
of the object as the primary key), we want to define object-type-specific tables for equivalent reasons to the ones explained in Subsection 6.3. Therefore, if _ot ∈_ _OT_ ( _L_ ) is the
object type, we have a table called **object** ~~_⊕_~~ _mapOT_ **(ot)**, where _mapOT_ : _OT_ ( _L_ ) _→_ U _Σ_ is
an injective function [4] mapping the object types to unique identifiers, containing the objects of the given object type along with the history of their attributes. In particular, all
the attributes associated with the given object type (oatype in Definition 2) are columns
of the table, and the values for each object are populated accordingly. The timestamp
column here highlights the history of the values of the different attributes. We made the
following design choices:


  - In accordance with the definition of OCEL 2.0, rows possessing the smallest feasible
timestamp, specifically _1970-01-01 00:00 UTC_    - which equates to 0 in Definition 2

   - correspond to the initial values of all the attributes for a given object. This uniform timestamp selection, symbolic of the starting point or ”epoch”, facilitates a
consistent reference frame across all objects, aligning seamlessly with the structure
proposed by OCEL 2.0. The deliberate choice of this fixed date for the timestamp of 0 is not arbitrary; instead, it serves a clear purpose by fostering improved
compatibility and coherence with the OCEL 2.0 definition.


  - The rows having a different timestamp have a value in the column
_ocel_ ~~_c_~~ _hanged_ ~~_f_~~ _ield_, which highlights which other column has been changed.


This allows (according to _oaval_ in Definition 2) to reconstruct the value of a given attribute at a specified point in time. For example, given the purchase order **PO1**, the
quantity of the order at **2022-01-11 10:00** is 500 cows, but it becomes 600 cows at
**2022-01-13 13:00** . Also, consider the invoice _R_ 3, which was blocked and then released.
The object identifier column is pointing (as a foreign key) to the object identifier
column of the **object** table.
Examples follow (Table 16, Table 17, Table 18, Table 19) for all the object types of
the running example log.


Table 16: [Proposed relational implementation] Object type table: **ob-**
**ject** ~~**P**~~ **urchaseRequisition**


**ocel** ~~**i**~~ **d [FK]** **ocel** ~~**t**~~ **ime** **pr** ~~**p**~~ **roduct** **pr** ~~**q**~~ **uantity** **ocel** ~~**c**~~ **hanged** ~~**f**~~ **ield**


PR1 1970-01-01 00:00 UTC Cows 500


4Which can be the identity function.


19


Table 17: [Proposed relational implementation] Object type table: **ob-**
**ject** ~~**P**~~ **urchaseOrder**


**ocel** ~~**i**~~ **d [FK]** **ocel** ~~**t**~~ **ime** **po** ~~**p**~~ **roduct** **po** ~~**q**~~ **uantity** **ocel** ~~**c**~~ **hanged** ~~**f**~~ **ield**


PO1 1970-01-01 00:00 UTC Cows 500


PO1 2022-01-13 12:00 UTC 600 po ~~q~~ uantity


PO2 1970-01-01 01:00 UTC Notebooks 1


Table 18: [Proposed relational implementation] Object type table: **object** ~~**I**~~ **nvoice**


**ocel** ~~**i**~~ **d [FK]** **ocel** **time** **is** ~~**b**~~ **locked** **ocel** ~~**c**~~ **hanged** ~~**f**~~ **ield**


R1 1970-01-01 00:00 UTC No


R2 1970-01-01 00:00 UTC No


R3 1970-01-01 00:00 UTC No


R3 2022-02-03 07:30 UTC Yes is ~~b~~ locked


R3 2022-02-03 23:30 UTC No is ~~b~~ locked


Table 19: [Proposed relational implementation] Object type table: **object** ~~**P**~~ **ayment**


**ocel** ~~**i**~~ **d [FK]** **ocel** ~~**t**~~ **ime** **ocel** ~~**c**~~ **hanged** ~~**f**~~ **ield**


P1 1970-01-01 00:00 UTC


P2 1970-01-01 00:00 UTC


P3 1970-01-01 00:00 UTC


20


#### **6.5 Event-to-Object (E2O) Relationships**

The **event** ~~**o**~~ **bject** table contains the event-to-object relationships (E2O in Definition 2).
Therefore, it contains the correlated event identifier and object identifier (foreign key to
**event.ocel** ~~**i**~~ **d** and **object.ocel** ~~**i**~~ **d** respectively) with a qualifier explaining the nature
of the relationship. A primary key is set on **event** ~~**o**~~ **bject** containing all the columns,
therefore “realizing” the set proposed in Definition 2. The **event** ~~**o**~~ **bject** table of the
running example is proposed in Table 20. Note that we can have an event related with
different qualifiers to the same object.


Table 20: [Proposed relational implementation] Table containing the event-to-object
( **event** **object** ) relationships


**ocel** **event** ~~**i**~~ **d [PK] [FK]** **ocel** ~~**o**~~ **bject** **id [PK] [FK]** **ocel** **qualifier [PK]**


e1 PR1 Regular placement of PR
e2 PR1 Regular approval of PR
e3 PR1 Created order from PR
e3 PO1 Created order with identifier
e4 PO1 Change of quantity
e5 PO1 Invoice created starting from the PO
e5 R1 Invoice created with identifier
e5 PO1 Invoice created starting from the PO
e6 R2 Invoice created with identifier
e6 PO1 Invoice created starting from the PO
e7 R1 Payment for the invoice
e7 P1 Payment inserted with identifier
e8 R2 Payment for the invoice
e8 P2 Payment inserted with identifier
e9 R3 Invoice created with identifier
e10 R3 Purchase order created with maverick buying from
e10 PO2 Purchase order created with identifier
e11 R3 Payment block due to unethical maverick buying
e12 R3 Payment block removed . . .
e13 R3 Payment for the invoice
e13 P3 Payment inserted with identifier


21


#### **6.6 Object-to-Object (O2O) Relationships**

The **object** ~~**o**~~ **bject** table contains the object-to-object relationships (O2O in Definition 2). Therefore, it contains the correlated object identifiers (source and target; both
are foreign keys to **object.ocel** ~~**i**~~ **d** ) with a qualifier explaining the nature of the relationship. A primary key is set on **object** ~~**o**~~ **bject** containing all the columns, therefore
“realizing” the set proposed in Definition 2. The **object** ~~**o**~~ **bject** table of the running
example is proposed in Table 21. Note that we can have the same couple of objects
related through different qualifiers.


Table 21: [Proposed relational implementation] Table containing the object-to-object
( **object** ~~**o**~~ **bject** ) relationships


**ocel** ~~**s**~~ **ource** **id [PK] [FK]** **ocel** ~~**t**~~ **arget** ~~**i**~~ **d [PK] [FK]** **ocel** ~~**q**~~ **ualifier [PK]**


PR1 PO1 PO from PR
PO1 R1 Invoice from PO
PO1 R2 Invoice from PO
R1 P1 Payment from invoice
R2 P2 Payment from invoice
PO2 R3 Maverick buying
R3 P3 Payment from invoice


22


#### **6.7 Constraints on the Relational Implementation**

Clearly, all the elements introduced using the metamodel can be mapped onto the table
structures proposed. However, we need to ensure consistency. Therefore, the following
constraints are implemented on the proposed relational implementation:


  - The uniqueness of the event/object types in the tables **event** ~~**m**~~ **ap** ~~**t**~~ **ype** and
**object** ~~**m**~~ **ap** ~~**t**~~ **ype** is ensured by setting the type as the primary key.


  - The uniqueness of the events/objects in the overall **event** and **object** tables is
ensured by setting the identifier as the primary key.


  - The uniqueness of the event identifiers in the specific event type tables is ensured
by setting the identifier as the primary key. Since the same objects can appear (by
design choice) several times in the specific object type tables, we cannot set the
identifier as the primary key in the given setting.


  - There is a foreign key between the specific event type tables and the generic **event**
table. This ensures that every identifier appearing in the specific event type tables
has been added to the **event** table.


  - There is a foreign key between the specific object type table and the generic **object**
table. This ensures that every identifier appearing in the specific object type tables
has been added to the **object** table.


  - There is a foreign key between the generic **event** table and **event** ~~**m**~~ **ap** ~~**t**~~ **ype**,
ensuring that every event can be mapped to a specific event type table.


  - There is a foreign key between the generic **object** table and **object** ~~**m**~~ **ap** ~~**t**~~ **ype**,
ensuring that every object is mapped to a specific object type table.


  - The **event** ~~**o**~~ **bject** table has two foreign keys, directed towards **event.ocel** ~~**i**~~ **d** and
**object.ocel** ~~**i**~~ **d** respectively. This ensures that every identifier appearing in the
**event** ~~**o**~~ **bject** table is effectively an event or an object. Moreover, the three columns
together form the primary key, ensuring that no duplicate rows are contained in
the table.


  - The **object** ~~**o**~~ **bject** table has two foreign keys, both directed towards **object.ocel** ~~**i**~~ **d** .
This ensures that every identifier appearing in the **object** ~~**o**~~ **bject** table is effectively
an object. Moreover, the three columns together form the primary key, ensuring
that no duplicate rows are contained in the table.


We can ensure that every event/object is added to the correct event type/object type
table by a trigger that checks during the insertion time the
**event** ~~**m**~~ **ap** ~~**t**~~ **ype** / **object** ~~**m**~~ **ap** ~~**t**~~ **ype** tables to compare the name of the current table
with the expected table into which the event/object should be assigned.
We also provide some offline validation constraints as SQL queries. These are available
[at https://www.ocel-standard.org/2.0/ocel20-schema-relational.pdf.](https://www.ocel-standard.org/2.0/ocel20-schema-relational.pdf)


23


### **7 XML Format**

We propose an XML implementation following Definition 2. The timestamps are assumed
to follow the ISO format specification `[https://en.wikipedia.org/wiki/ISO_8601](https://en.wikipedia.org/wiki/ISO_8601)` .
The XML schema is organized as follows. There is a root element with the tag **log** .
The log element has the following children:


  - An element with tag **object-types**, containing as many **object-type** elements as
types in _OT_ ( _L_ ). Each **object-type** has a **name** property (which is the object
type) and a single child with tag **attributes** :


**–** For every attribute in oatype( _ot_ ), the element **attributes** has a child with tag
**attribute** and properties **name** (which is the attribute) and **type** (the type
of the attribute, which should be considered during the parsing of the values).


  - An element with tag **event-types**, containing as many **event-type** elements as
types in _OT_ ( _L_ ). Each **event-type** has a **name** property (which is the event type)
and a single child with tag **attributes** :


**–** For every attribute in eatype( _et_ ), the element **attributes** has a child with tag
**attribute** and properties **name** (which is the attribute) and **type** (the type
of the attribute, which should be considered during the parsing of the values).


  - An element with tag **events**, containing as many **event** elements as many events
are in _E_ . An **event** is characterized by:


**–** Its properties **id** (the identifier of the event), **type** (the event type of the event,
given by evtype in Definition 2) and **time** (the timestamp of the event, given
by time in Definition 2).


**–** A child with tag **objects**, containing the related objects to the event (E2O in
Definition 2; we define the function:


relobj( _e_ ) = _{_ ( _o, q_ ) _|_ ( _e_ _[′]_ _, q, o_ ) _∈_ E2O _∧_ _e_ _[′]_ = _e}_


which associates to every event a set of objects along with the qualifier of
the relationship). In particular, for every event-to-object relationship an entry
**relobj** is created, having as properties the **object-id** (related object identifier)
and **qualifier** (the qualifier of the event-to-object relationship).


**–** A child with tag **attributes**, having as many children **attribute** as many
attributes are related to the event (the domain of eaval _ea_ in Definition 2):

∗ Each **attribute** is characterized by a **name** property and the corresponding value is reported as text of the (XML) element.


  - An element with tag **objects**, containing as many **object** elements as many objects
are in _O_ . An **object** is characterized by:


**–** Its properties **id** (the identifier of the object) and **type** (the object type of the
object, given by objtype in Definition 2).


**–** An element with tag **attributes**, containing the different **attribute** of the
object.


24


**–** Each **attribute** is characterized by a **time** property (the timestamp in which
the value for the given attribute was recorded), a **name** property, and the
corresponding value is reported as the text of the (XML) element. An attribute
is valid from the specified **time** (until an attribute with the same name and
greater timestamp is recorded).


**–** A child with tag **objects**, containing the related objects to the given object
(O2O in Definition 2; we define the function:


relobj( _o_ ) = _{_ ( _o_ _[′′]_ _, q_ ) _|_ ( _o_ _[′]_ _, q, o_ _[′′]_ ) _∈_ O2O _∧_ _o_ _[′]_ = _o}_


which associates to every object a set of objects along with the qualifier of the
relationship). In particular, for every object-to-object relationship an entry
**relobj** is created, having as properties the **object-id** (related object identifier)
and **qualifier** (the qualifier of the object-to-object relationship).


In the remainder of this section, we show an example file and the XSD (XML Schema
Definition) that can be used to check consistency.

#### **7.1 XML Example**


An example (on the running example log) follows.


1 `<?xml version=’1.0’ encoding=’UTF-8’?>`

2 `<log>`

3 `<object-types>`

4 `<object-type name="Invoice">`

5 `<attributes>`

6 `<attribute name="is_blocked" type="string"/>`

7 `</attributes>`

8 `</object-type>`

9 `<object-type name="Payment">`

10 `<attributes/>`

11 `</object-type>`

12 `<object-type name="Purchase Order">`

13 `<attributes>`

14 `<attribute name="po_product" type="string"/>`

15 `<attribute name="po_quantity" type="string"/>`

16 `</attributes>`

17 `</object-type>`

18 `<object-type name="Purchase Requisition">`

19 `<attributes>`

20 `<attribute name="pr_product" type="string"/>`

21 `<attribute name="pr_quantity" type="string"/>`

22 `</attributes>`

23 `</object-type>`

24 `</object-types>`

25 `<event-types>`

26 `<event-type name="Approve Purchase Requisition">`

27 `<attributes>`

28 `<attribute name="pr_approver" type="string"/>`

29 `</attributes>`

30 `</event-type>`

31 `<event-type name="Change PO Quantity">`

32 `<attributes>`

33 `<attribute name="po_editor" type="string"/>`


25


34 `</attributes>`

35 `</event-type>`

36 `<event-type name="Create Purchase Order">`

37 `<attributes>`

38 `<attribute name="po_creator" type="string"/>`

39 `</attributes>`

40 `</event-type>`

41 `<event-type name="Create Purchase Requisition">`

42 `<attributes>`

43 `<attribute name="pr_creator" type="string"/>`

44 `</attributes>`

45 `</event-type>`

46 `<event-type name="Insert Invoice">`

47 `<attributes>`

48 `<attribute name="invoice_inserter" type="string"/>`

49 `</attributes>`

50 `</event-type>`

51 `<event-type name="Insert Payment">`

52 `<attributes>`

53 `<attribute name="payment_inserter" type="string"/>`

54 `</attributes>`

55 `</event-type>`

56 `<event-type name="Remove Payment Block">`

57 `<attributes>`

58 `<attribute name="invoice_block_rem" type="string"/>`

59 `</attributes>`

60 `</event-type>`

61 `<event-type name="Set Payment Block">`

62 `<attributes>`

63 `<attribute name="invoice_blocker" type="string"/>`

64 `</attributes>`

65 `</event-type>`

66 `</event-types>`

67 `<objects>`

68 `<object id="R1" type="Invoice">`

69 `<attributes>`

70 `<attribute name="is_blocked" time="1970-01-01T00:00:00Z">No</attribute>`

71 `</attributes>`

72 `<objects>`

73 `<relationship object-id="P1" qualifier="Payment from invoice"/>`

74 `</objects>`

75 `</object>`

76 `<object id="R2" type="Invoice">`

77 `<attributes>`

78 `<attribute name="is_blocked" time="1970-01-01T00:00:00Z">No</attribute>`

79 `</attributes>`

80 `<objects>`

81 `<relationship object-id="P2" qualifier="Payment from invoice"/>`

82 `</objects>`

83 `</object>`

84 `<object id="R3" type="Invoice">`

85 `<attributes>`

86 `<attribute name="is_blocked" time="1970-01-01T00:00:00Z">No</attribute>`

87 `<attribute name="is_blocked" time="2022-02-03T07:30:00Z">Yes</attribute>`

88 `<attribute name="is_blocked" time="2022-02-03T23:30:00Z">No</attribute>`

89 `</attributes>`

90 `<objects>`

91 `<relationship object-id="P3" qualifier="Payment from invoice"/>`


26


92 `</objects>`

93 `</object>`

94 `<object id="P1" type="Payment">`

95 `<attributes/>`

96 `</object>`

97 `<object id="P2" type="Payment">`

98 `<attributes/>`

99 `</object>`

100 `<object id="P3" type="Payment">`

101 `<attributes/>`

102 `</object>`

103 `<object id="PO1" type="Purchase Order">`

104 `<attributes>`

105 `<attribute name="po_product" time="1970-01-01T00:00:00Z">Cows</attribute>`

106 `<attribute name="po_quantity" time="1970-01-01T00:00:00Z">500</attribute>`

107 `<attribute name="po_quantity" time="2022-01-13T12:00:00Z">600</attribute>`

108 `</attributes>`

109 `<objects>`

110 `<relationship object-id="R1" qualifier="Invoice from PO"/>`

111 `<relationship object-id="R2" qualifier="Invoice from PO"/>`

112 `</objects>`

113 `</object>`

114 `<object id="PO2" type="Purchase Order">`

115 `<attributes>`

116 `<attribute name="po_product" time="1970-01-01T00:00:00Z">Notebooks</attribute>`

117 `<attribute name="po_quantity" time="1970-01-01T00:00:00Z">1</attribute>`

118 `</attributes>`

119 `<objects>`

120 `<relationship object-id="R3" qualifier="Maverick buying"/>`

121 `</objects>`

122 `</object>`

123 `<object id="PR1" type="Purchase Requisition">`

124 `<attributes>`

125 `<attribute name="pr_product" time="1970-01-01T00:00:00Z">Cows</attribute>`

126 `<attribute name="pr_quantity" time="1970-01-01T00:00:00Z">500</attribute>`

127 `</attributes>`

128 `<objects>`

129 `<relationship object-id="PO1" qualifier="PO from PR"/>`

130 `</objects>`

131 `</object>`

132 `</objects>`

133 `<events>`

134 `<event id="e1" type="Create Purchase Requisition" time="2022-01-09T15:00:00Z">`

135 `<attributes>`

136 `<attribute name="pr_creator">Mike</attribute>`

137 `</attributes>`

138 `<objects>`

139 `<relationship object-id="PR1" qualifier="Regular placement of PR"/>`

140 `</objects>`

141 `</event>`

142 `<event id="e2" type="Approve Purchase Requisition" time="2022-01-09T16:30:00Z">`

143 `<attributes>`

144 `<attribute name="pr_approver">Tania</attribute>`

145 `</attributes>`

146 `<objects>`

147 `<relationship object-id="PR1" qualifier="Regular approval of PR"/>`

148 `</objects>`

149 `</event>`


27


150 `<event id="e3" type="Create Purchase Order" time="2022-01-10T09:15:00Z">`

151 `<attributes>`

152 `<attribute name="po_creator">Mike</attribute>`

153 `</attributes>`

154 `<objects>`

155 `<relationship object-id="PR1" qualifier="Created order from PR"/>`

156 `<relationship object-id="PO1" qualifier="Created order with identifier"/>`

157 `</objects>`

158 `</event>`

159 `<event id="e4" type="Change PO Quantity" time="2022-01-13T12:00:00Z">`

160 `<attributes>`

161 `<attribute name="po_editor">Mike</attribute>`

162 `</attributes>`

163 `<objects>`

164 `<relationship object-id="PO1" qualifier="Change of quantity"/>`

165 `</objects>`

166 `</event>`

167 `<event id="e5" type="Insert Invoice" time="2022-01-14T12:00:00Z">`

168 `<attributes>`

169 `<attribute name="invoice_inserter">Luke</attribute>`

170 `</attributes>`

171 `<objects>`

172 `<relationship object-id="PO1" qualifier="Invoice created starting from the PO"/>`

173 `<relationship object-id="R1" qualifier="Invoice created with identifier"/>`

174 `</objects>`

175 `</event>`

176 `<event id="e6" type="Insert Invoice" time="2022-01-16T11:00:00Z">`

177 `<attributes>`

178 `<attribute name="invoice_inserter">Luke</attribute>`

179 `</attributes>`

180 `<objects>`

181 `<relationship object-id="PO1" qualifier="Invoice created starting from the PO"/>`

182 `<relationship object-id="R2" qualifier="Invoice created with identifier"/>`

183 `</objects>`

184 `</event>`

185 `<event id="e7" type="Insert Payment" time="2022-01-30T23:00:00Z">`

186 `<attributes>`

187 `<attribute name="payment_inserter">Robot</attribute>`

188 `</attributes>`

189 `<objects>`

190 `<relationship object-id="R1" qualifier="Payment for the invoice"/>`

191 `<relationship object-id="P1" qualifier="Payment inserted with identifier"/>`

192 `</objects>`

193 `</event>`

194 `<event id="e8" type="Insert Payment" time="2022-01-31T22:00:00Z">`

195 `<attributes>`

196 `<attribute name="payment_inserter">Robot</attribute>`

197 `</attributes>`

198 `<objects>`

199 `<relationship object-id="R2" qualifier="Payment for the invoice"/>`

200 `<relationship object-id="P2" qualifier="Payment created with identifier"/>`

201 `</objects>`

202 `</event>`

203 `<event id="e9" type="Insert Invoice" time="2022-02-02T09:00:00Z">`

204 `<attributes>`

205 `<attribute name="invoice_inserter">Mario</attribute>`

206 `</attributes>`

207 `<objects>`


28


208 `<relationship object-id="R3" qualifier="Invoice created with identifier"/>`

209 `</objects>`

210 `</event>`

211 `<event id="e10" type="Create Purchase Order" time="2022-02-02T17:00:00Z">`

212 `<attributes>`

213 `<attribute name="po_creator">Mario</attribute>`

214 `</attributes>`

215 `<objects>`

216 `<relationship object-id="R3" qualifier="Purchase order created with maverick buying from"/>`

217 `<relationship object-id="PO2" qualifier="Purchase order created with identifier"/>`

218 `</objects>`

219 `</event>`

220 `<event id="e11" type="Set Payment Block" time="2022-02-03T07:30:00Z">`

221 `<attributes>`

222 `<attribute name="invoice_blocker">Mario</attribute>`

223 `</attributes>`

224 `<objects>`

225 `<relationship object-id="R3" qualifier="Payment block due to unethical maverick buying"/>`

226 `</objects>`

227 `</event>`

228 `<event id="e12" type="Remove Payment Block" time="2022-02-03T23:30:00Z">`

229 `<attributes>`

230 `<attribute name="invoice_block_rem">Mario</attribute>`

231 `</attributes>`

232 `<objects>`

233 `<relationship object-id="R3" qualifier="Payment block removed ..."/>`

234 `</objects>`

235 `</event>`

236 `<event id="e13" type="Insert Payment" time="2022-02-28T23:00:00Z">`

237 `<attributes>`

238 `<attribute name="payment_inserter">Robot</attribute>`
