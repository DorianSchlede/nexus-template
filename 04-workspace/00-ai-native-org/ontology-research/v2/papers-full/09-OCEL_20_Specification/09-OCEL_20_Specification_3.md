<!-- Source: 09-OCEL_20_Specification.pdf | Chunk 3/4 -->

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

239 `</attributes>`

240 `<objects>`

241 `<relationship object-id="R3" qualifier="Payment for the invoice"/>`

242 `<relationship object-id="P3" qualifier="Payment inserted with identifier"/>`

243 `</objects>`

244 `</event>`

245 `</events>`

246 `</log>`

#### **7.2 XML Schema Definition**


A machine-readable XML Schema Definition (XSD) file is provided to check whether an
[example XML OCEL 2.0 is valid, see https://www.ocel-standard.org/2.0/ocel20-schema-](https://www.ocel-standard.org/2.0/ocel20-schema-xml.xsd)
[xml.xsd Numerous tools are available to validate an XML file against an XSD file.](https://www.ocel-standard.org/2.0/ocel20-schema-xml.xsd)


1 `<xs:schema attributeFormDefault="unqualified" elementFormDefault="qualified"`

2 `xmlns:xs="http://www.w3.org/2001/XMLSchema">`

3 `<xs:element name="attribute">`

4 `<xs:complexType>`

5 `<xs:simpleContent>`

6 `<xs:extension base="xs:string">`

7 `<xs:attribute type="xs:string" name="name" use="required"/>`

8 `<xs:attribute name="type" use="optional">`

9 `<xs:simpleType>`

10 `<xs:restriction base="xs:string">`

11 `<xs:enumeration value="string"/>`


29


12 `<xs:enumeration value="time"/>`

13 `<xs:enumeration value="integer"/>`

14 `<xs:enumeration value="float"/>`

15 `<xs:enumeration value="boolean"/>`

16 `</xs:restriction>`

17 `</xs:simpleType>`

18 `</xs:attribute>`

19 `<xs:attribute type="xs:dateTime" name="time" use="optional"/>`

20 `</xs:extension>`

21 `</xs:simpleContent>`

22 `</xs:complexType>`

23 `</xs:element>`

24 `<xs:element name="attributes">`

25 `<xs:complexType mixed="true">`

26 `<xs:sequence>`

27 `<xs:element ref="attribute" maxOccurs="unbounded" minOccurs="0"/>`

28 `</xs:sequence>`

29 `</xs:complexType>`

30 `</xs:element>`

31 `<xs:element name="object-type">`

32 `<xs:complexType>`

33 `<xs:sequence>`

34 `<xs:element ref="attributes"/>`

35 `</xs:sequence>`

36 `<xs:attribute type="xs:string" name="name" use="required"/>`

37 `</xs:complexType>`

38 `<xs:key name="objectTypeAttributeKey">`

39 `<xs:selector xpath="attributes/attribute"/>`

40 `<xs:field xpath="@name"/>`

41 `</xs:key>`

42 `</xs:element>`

43 `<xs:element name="event-type">`

44 `<xs:complexType>`

45 `<xs:sequence>`

46 `<xs:element ref="attributes"/>`

47 `</xs:sequence>`

48 `<xs:attribute type="xs:string" name="name" use="required"/>`

49 `</xs:complexType>`

50 `<xs:key name="eventTypeAttributeKey">`

51 `<xs:selector xpath="attributes/attribute"/>`

52 `<xs:field xpath="@name"/>`

53 `</xs:key>`

54 `</xs:element>`

55 `<xs:element name="object">`

56 `<xs:complexType mixed="true">`

57 `<xs:sequence>`

58 `<xs:element ref="attributes" minOccurs="0"/>`

59 `<xs:element ref="objects" minOccurs="0"/>`

60 `</xs:sequence>`

61 `<xs:attribute type="xs:string" name="object-id" use="optional"/>`

62 `<xs:attribute type="xs:string" name="qualifier" use="optional"/>`

63 `<xs:attribute type="xs:string" name="id" use="optional"/>`

64 `<xs:attribute type="xs:string" name="type" use="required"/>`

65 `</xs:complexType>`

66 `</xs:element>`

67 `<xs:element name="objects">`

68 `<xs:complexType>`

69 `<xs:sequence>`


30


70 `<xs:element ref="object" maxOccurs="unbounded" minOccurs="0"/>`

71 `</xs:sequence>`

72 `</xs:complexType>`

73 `</xs:element>`

74 `<xs:element name="event">`

75 `<xs:complexType>`

76 `<xs:sequence>`

77 `<xs:element ref="attributes"/>`

78 `<xs:element ref="objects"/>`

79 `</xs:sequence>`

80 `<xs:attribute type="xs:string" name="id" use="required"/>`

81 `<xs:attribute type="xs:string" name="type" use="required"/>`

82 `<xs:attribute type="xs:dateTime" name="time" use="required"/>`

83 `</xs:complexType>`

84 `</xs:element>`

85 `<xs:element name="object-types">`

86 `<xs:complexType>`

87 `<xs:sequence>`

88 `<xs:element ref="object-type" maxOccurs="unbounded" minOccurs="0"/>`

89 `</xs:sequence>`

90 `</xs:complexType>`

91 `</xs:element>`

92 `<xs:element name="event-types">`

93 `<xs:complexType>`

94 `<xs:sequence>`

95 `<xs:element ref="event-type" maxOccurs="unbounded" minOccurs="0"/>`

96 `</xs:sequence>`

97 `</xs:complexType>`

98 `</xs:element>`

99 `<xs:element name="events">`

100 `<xs:complexType>`

101 `<xs:sequence>`

102 `<xs:element ref="event" maxOccurs="unbounded" minOccurs="0"/>`

103 `</xs:sequence>`

104 `</xs:complexType>`

105 `</xs:element>`

106 `<xs:element name="log">`

107 `<xs:complexType>`

108 `<xs:sequence>`

109 `<xs:element ref="object-types"/>`

110 `<xs:element ref="event-types"/>`

111 `<xs:element ref="objects"/>`

112 `<xs:element ref="events"/>`

113 `</xs:sequence>`

114 `</xs:complexType>`

115 `<xs:key name="objectTypeKey">`

116 `<xs:selector xpath="object-types/object-type"/>`

117 `<xs:field xpath="@name"/>`

118 `</xs:key>`

119 `<xs:key name="objectKey">`

120 `<xs:selector xpath="objects/object"/>`

121 `<xs:field xpath="@id"/>`

122 `</xs:key>`

123 `<xs:key name="eventTypeKey">`

124 `<xs:selector xpath="event-types/event-type"/>`

125 `<xs:field xpath="@name"/>`

126 `</xs:key>`

127 `<xs:key name="eventKey">`


31


128 `<xs:selector xpath="events/event"/>`

129 `<xs:field xpath="@id"/>`

130 `</xs:key>`

131 `<xs:keyref name="objectTypeRef" refer="objectTypeKey">`

132 `<xs:selector xpath="objects/object"/>`

133 `<xs:field xpath="@type"/>`

134 `</xs:keyref>`

135 `<xs:keyref name="eventTypeRef" refer="eventTypeKey">`

136 `<xs:selector xpath="events/event"/>`

137 `<xs:field xpath="@type"/>`

138 `</xs:keyref>`

139 `<xs:keyref name="objectObjectRef" refer="objectKey">`

140 `<xs:selector xpath="objects/object/objects/object"/>`

141 `<xs:field xpath="@object-id"/>`

142 `</xs:keyref>`

143 `<xs:keyref name="eventObjectRef" refer="objectKey">`

144 `<xs:selector xpath="events/event/objects/object"/>`

145 `<xs:field xpath="@object-id"/>`

146 `</xs:keyref>`

147 `<xs:keyref name="objectAttributeRef" refer="objectTypeAttributeKey">`

148 `<xs:selector xpath="objects/object/attributes/attribute"/>`

149 `<xs:field xpath="@name"/>`

150 `</xs:keyref>`

151 `<xs:keyref name="eventAttributeRef" refer="eventTypeAttributeKey">`

152 `<xs:selector xpath="events/event/attributes/attribute"/>`

153 `<xs:field xpath="@name"/>`

154 `</xs:keyref>`

155 `</xs:element>`

156 `</xs:schema>`


32


### **8 JSON Format**

The JSON format provides a lightweight structure for web-native process mining applications. It is conceptually similar to the XML format with its top-level arrays `events`,
`eventTypes`, `objects`, and `objectTypes` .
In the following, we describe these four top-level properties in detail.


    - The top-level `event` array contains event objects with the properties `id`, `type` (referencing the name of an event type), and `time` (ISO format). An event’s `attributes`
are structured into an array of attribute objects with `name` and `value` properties.
The event’s event-to-object relationships are listed in the _relationships_ array with
`objectId` and `qualifier` .


    - The top-level `eventTypes` array contains event type objects with a `name` and a
list of attributes with `name` and `value` properties. Valid types are **string**, **time**,
**integer**, **float**, and **boolean** .


    - The top-level `object` array contains a list of objects as JSON object, with properties
`id` and `type` (referencing the name of an object type). The attributes property
contains an array of attributes with the properties `name`, `time` (ISO format), and
`value` .


    - Finally, the top-level objectTypes array contains object type description objects
with a `name` and a list of attributes with `name` and `value` properties. Valid types
are **string**, **time**, **integer**, **float**, and **boolean** .

#### **8.1 JSON Example**


As an example, we show the running example formatted as a JSON document.


1 `{`
2 `"objectTypes": [`
3 `{`
4 `"name": "Invoice",`
5 `"attributes": [`
6 `{`
7 `"name": "is_blocked",`
8 `"type": "string"`
9 `}`
10 `]`
11 `},`
12 `{`
13 `"name": "Payment",`
14 `"attributes": []`
15 `},`
16 `{`
17 `"name": "Purchase Order",`
18 `"attributes": [`
19 `{`
20 `"name": "po_product",`
21 `"type": "string"`
22 `},`
23 `{`
24 `"name": "po_quantity",`


33


25 `"type": "string"`
26 `}`
27 `]`
28 `},`
29 `{`
30 `"name": "Purchase Requisition",`
31 `"attributes": [`
32 `{`
33 `"name": "pr_product",`
34 `"type": "string"`
35 `},`
36 `{`
37 `"name": "pr_quantity",`
38 `"type": "string"`
39 `}`
40 `]`
41 `}`
42 `],`
43 `"eventTypes": [`
44 `{`
45 `"name": "Approve Purchase Requisition",`
46 `"attributes": [`
47 `{`
48 `"name": "pr_approver",`
49 `"type": "string"`
50 `}`
51 `]`
52 `},`
53 `{`
54 `"name": "Change PO Quantity",`
55 `"attributes": [`
56 `{`
57 `"name": "po_editor",`
58 `"type": "string"`
59 `}`
60 `]`
61 `},`
62 `{`
63 `"name": "Create Purchase Order",`
64 `"attributes": [`
65 `{`
66 `"name": "po_creator",`
67 `"type": "string"`
68 `}`
69 `]`
70 `},`
71 `{`
72 `"name": "Create Purchase Requisition",`
73 `"attributes": [`
74 `{`
75 `"name": "pr_creator",`
76 `"type": "string"`
77 `}`
78 `]`
79 `},`
80 `{`
81 `"name": "Insert Invoice",`
82 `"attributes": [`


34


83 `{`
84 `"name": "invoice_inserter",`
85 `"type": "string"`
86 `}`
87 `]`
88 `},`
89 `{`
90 `"name": "Insert Payment",`
91 `"attributes": [`
92 `{`
93 `"name": "payment_inserter",`
94 `"type": "string"`
95 `}`
96 `]`
97 `},`
98 `{`
99 `"name": "Remove Payment Block",`
100 `"attributes": [`
101 `{`
102 `"name": "invoice_block_rem",`
103 `"type": "string"`
104 `}`
105 `]`
106 `},`
107 `{`
108 `"name": "Set Payment Block",`
109 `"attributes": [`
110 `{`
111 `"name": "invoice_blocker",`
112 `"type": "string"`
113 `}`
114 `]`
115 `}`
116 `],`
117 `"objects": [`
118 `{`
119 `"id": "R1",`
120 `"type": "Invoice",`
121 `"attributes": [`
122 `{`
123 `"name": "is_blocked",`
124 `"time": "1970-01-01T00:00:00Z",`
125 `"value": "No"`
126 `}`
127 `],`
128 `"relationships": [`
129 `{`
130 `"objectId": "P1",`
131 `"qualifier": "Payment from invoice"`
132 `}`
133 `]`
134 `},`
135 `{`
136 `"id": "R2",`
137 `"type": "Invoice",`
138 `"attributes": [`
139 `{`
140 `"name": "is_blocked",`


35


141 `"time": "1970-01-01T00:00:00Z",`
142 `"value": "No"`
143 `}`
144 `],`
145 `"relationships": [`
146 `{`
147 `"objectId": "P2",`
148 `"qualifier": "Payment from invoice"`
149 `}`
150 `]`
151 `},`
152 `{`
153 `"id": "R3",`
154 `"type": "Invoice",`
155 `"attributes": [`
156 `{`
157 `"name": "is_blocked",`
158 `"time": "1970-01-01T00:00:00Z",`
159 `"value": "No"`
160 `},`
161 `{`
162 `"name": "is_blocked",`
163 `"time": "2022-02-03T07:30:00Z",`
164 `"value": "Yes"`
165 `},`
166 `{`
167 `"name": "is_blocked",`
168 `"time": "2022-02-03T23:30:00Z",`
169 `"value": "No"`
170 `}`
171 `],`
172 `"relationships": [`
173 `{`
174 `"objectId": "P3",`
175 `"qualifier": "Payment from invoice"`
176 `}`
177 `]`
178 `},`
179 `{`
180 `"id": "P1",`
181 `"type": "Payment"`
182 `},`
183 `{`
184 `"id": "P2",`
185 `"type": "Payment"`
186 `},`
187 `{`
188 `"id": "P3",`
189 `"type": "Payment"`
190 `},`
191 `{`
192 `"id": "PO1",`
193 `"type": "Purchase Order",`
194 `"attributes": [`
195 `{`
196 `"name": "po_product",`
197 `"time": "1970-01-01T00:00:00Z",`
198 `"value": "Cows"`


36


199 `},`
200 `{`
201 `"name": "po_quantity",`
202 `"time": "1970-01-01T00:00:00Z",`
203 `"value": "500"`
204 `},`
205 `{`
206 `"name": "po_quantity",`
207 `"time": "2022-01-13T12:00:00Z",`
208 `"value": "600"`
209 `}`
210 `],`
211 `"relationships": [`
212 `{`
213 `"objectId": "R1",`
214 `"qualifier": "Invoice from PO"`
215 `},`
216 `{`
217 `"objectId": "R2",`
218 `"qualifier": "Invoice from PO"`
219 `}`
220 `]`
221 `},`
222 `{`
223 `"id": "PO2",`
224 `"type": "Purchase Order",`
225 `"attributes": [`
226 `{`
227 `"name": "po_product",`
228 `"time": "1970-01-01T00:00:00Z",`
229 `"value": "Notebooks"`
230 `},`
231 `{`
232 `"name": "po_quantity",`
233 `"time": "1970-01-01T00:00:00Z",`
234 `"value": "1"`
235 `}`
236 `],`
237 `"relationships": [`
238 `{`
239 `"objectId": "R3",`
240 `"qualifier": "Maverick buying"`
241 `}`
242 `]`
243 `},`
244 `{`
245 `"id": "PR1",`
246 `"type": "Purchase Requisition",`
247 `"attributes": [`
248 `{`
249 `"name": "pr_product",`
250 `"time": "1970-01-01T00:00:00Z",`
251 `"value": "Cows"`
252 `},`
253 `{`
254 `"name": "pr_quantity",`
255 `"time": "1970-01-01T00:00:00Z",`
256 `"value": "500"`



37


257 `}`
258 `],`
259 `"relationships": [`
260 `{`
261 `"objectId": "PO1",`
262 `"qualifier": "PO from PR"`
263 `}`
264 `]`
265 `}`
266 `],`
267 `"events": [`
268 `{`
269 `"id": "e1",`
270 `"type": "Create Purchase Requisition",`
271 `"time": "2022-01-09T15:00:00Z",`
272 `"attributes": [`
273 `{`
274 `"name": "pr_creator",`
275 `"value": "Mike"`
276 `}`
277 `],`
278 `"relationships": [`
279 `{`
280 `"objectId": "PR1",`
281 `"qualifier": "Regular placement of PR"`
282 `}`
283 `]`
284 `},`
285 `{`
286 `"id": "e2",`
287 `"type": "Approve Purchase Requisition",`
288 `"time": "2022-01-09T16:30:00Z",`
289 `"attributes": [`
290 `{`
291 `"name": "pr_approver",`
292 `"value": "Tania"`
293 `}`
294 `],`
295 `"relationships": [`
296 `{`
297 `"objectId": "PR1",`
298 `"qualifier": "Regular approval of PR"`
299 `}`
300 `]`
301 `},`
302 `{`
303 `"id": "e3",`
304 `"type": "Create Purchase Order",`
305 `"time": "2022-01-10T09:15:00Z",`
306 `"attributes": [`
307 `{`
308 `"name": "po_creator",`
309 `"value": "Mike"`
310 `}`
311 `],`
312 `"relationships": [`
313 `{`
314 `"objectId": "PR1",`


38


315 `"qualifier": "Created order from PR"`
316 `},`
317 `{`
318 `"objectId": "PO1",`
319 `"qualifier": "Created order with identifier"`
320 `}`
321 `]`
322 `},`
323 `{`
324 `"id": "e4",`
325 `"type": "Change PO Quantity",`
326 `"time": "2022-01-13T12:00:00Z",`
327 `"attributes": [`
328 `{`
329 `"name": "po_editor",`
330 `"value": "Mike"`
331 `}`
332 `],`
333 `"relationships": [`
334 `{`
335 `"objectId": "PO1",`
336 `"qualifier": "Change of quantity"`
337 `}`
338 `]`
339 `},`
340 `{`
341 `"id": "e5",`
342 `"type": "Insert Invoice",`
343 `"time": "2022-01-14T12:00:00Z",`
344 `"attributes": [`
345 `{`
346 `"name": "invoice_inserter",`
347 `"value": "Luke"`
348 `}`
349 `],`
350 `"relationships": [`
351 `{`
352 `"objectId": "PO1",`
353 `"qualifier": "Invoice created starting from the PO"`
354 `},`
355 `{`
356 `"objectId": "R1",`
357 `"qualifier": "Invoice created with identifier"`
358 `}`
359 `]`
360 `},`
361 `{`
362 `"id": "e6",`
363 `"type": "Insert Invoice",`
364 `"time": "2022-01-16T11:00:00Z",`
365 `"attributes": [`
366 `{`
367 `"name": "invoice_inserter",`
368 `"value": "Luke"`
369 `}`
370 `],`
371 `"relationships": [`
372 `{`


39


373 `"objectId": "PO1",`
374 `"qualifier": "Invoice created starting from the PO"`
375 `},`
376 `{`
377 `"objectId": "R2",`
378 `"qualifier": "Invoice created with identifier"`
379 `}`
380 `]`
381 `},`
382 `{`
383 `"id": "e7",`
384 `"type": "Insert Payment",`
385 `"time": "2022-01-30T23:00:00Z",`
386 `"attributes": [`
387 `{`
388 `"name": "payment_inserter",`
389 `"value": "Robot"`
390 `}`
391 `],`
392 `"relationships": [`
393 `{`
394 `"objectId": "R1",`
395 `"qualifier": "Payment for the invoice"`
396 `},`
397 `{`
398 `"objectId": "P1",`
399 `"qualifier": "Payment inserted with identifier"`
400 `}`
401 `]`
402 `},`
403 `{`
404 `"id": "e8",`
405 `"type": "Insert Payment",`
406 `"time": "2022-01-31T22:00:00Z",`
407 `"attributes": [`
408 `{`
409 `"name": "payment_inserter",`
410 `"value": "Robot"`
411 `}`
412 `],`
413 `"relationships": [`
414 `{`
415 `"objectId": "R2",`
416 `"qualifier": "Payment for the invoice"`
417 `},`
418 `{`
419 `"objectId": "P2",`
420 `"qualifier": "Payment created with identifier"`
421 `}`
422 `]`
423 `},`
424 `{`
425 `"id": "e9",`
426 `"type": "Insert Invoice",`
427 `"time": "2022-02-02T09:00:00Z",`
428 `"attributes": [`
429 `{`
430 `"name": "invoice_inserter",`


40

