<!-- Source: 09-OCEL_20_Specification.pdf | Chunk 4/4 -->

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


431 `"value": "Mario"`
432 `}`
433 `],`
434 `"relationships": [`
435 `{`
436 `"objectId": "R3",`
437 `"qualifier": "Invoice created with identifier"`
438 `}`
439 `]`
440 `},`
441 `{`
442 `"id": "e10",`
443 `"type": "Create Purchase Order",`
444 `"time": "2022-02-02T17:00:00Z",`
445 `"attributes": [`
446 `{`
447 `"name": "po_creator",`
448 `"value": "Mario"`
449 `}`
450 `],`
451 `"relationships": [`
452 `{`
453 `"objectId": "R3",`
454 `"qualifier": "Purchase order created with maverick buying from"`
455 `},`
456 `{`
457 `"objectId": "PO2",`
458 `"qualifier": "Purchase order created with identifier"`
459 `}`
460 `]`
461 `},`
462 `{`
463 `"id": "e11",`
464 `"type": "Set Payment Block",`
465 `"time": "2022-02-03T07:30:00Z",`
466 `"attributes": [`
467 `{`
468 `"name": "invoice_blocker",`
469 `"value": "Mario"`
470 `}`
471 `],`
472 `"relationships": [`
473 `{`
474 `"objectId": "R3",`
475 `"qualifier": "Payment block due to unethical maverick buying"`
476 `}`
477 `]`
478 `},`
479 `{`
480 `"id": "e12",`
481 `"type": "Remove Payment Block",`
482 `"time": "2022-02-03T23:30:00Z",`
483 `"attributes": [`
484 `{`
485 `"name": "invoice_block_rem",`
486 `"value": "Mario"`
487 `}`
488 `],`


41


489 `"relationships": [`
490 `{`
491 `"objectId": "R3",`
492 `"qualifier": "Payment block removed ..."`
493 `}`
494 `]`
495 `},`
496 `{`
497 `"id": "e13",`
498 `"type": "Insert Payment",`
499 `"time": "2022-02-28T23:00:00Z",`
500 `"attributes": [`
501 `{`
502 `"name": "payment_inserter",`
503 `"value": "Robot"`
504 `}`
505 `],`
506 `"relationships": [`
507 `{`
508 `"objectId": "R3",`
509 `"qualifier": "Payment for the invoice"`
510 `},`
511 `{`
512 `"objectId": "P3",`
513 `"qualifier": "Payment inserted with identifier"`
514 `}`
515 `]`
516 `}`
517 `]`
518 `}`

#### **8.2 JSON Schema Definition**


We defined a validation schema for the OCEL 2.0 JSON specification. The schema
[is reported in the following snippet and can be downloaded from https://www.ocel-](https://www.ocel-standard.org/2.0/ocel20-schema-json.json)
[standard.org/2.0/ocel20-schema-json.json.](https://www.ocel-standard.org/2.0/ocel20-schema-json.json)


1 `{`
2 `"$schema": "http://json-schema.org/draft-07/schema#",`
3 `"type": "object",`
4 `"properties": {`
5 `"eventTypes": {`
6 `"type": "array",`
7 `"items": {`
8 `"type": "object",`
9 `"properties": {`
10 `"name": { "type": "string" },`
11 `"attributes": {`
12 `"type": "array",`
13 `"items": {`
14 `"type": "object",`
15 `"properties": {`
16 `"name": { "type": "string" },`
17 `"type": { "type": "string" }`
18 `},`
19 `"required": ["name", "type"]`
20 `}`


42


21 `}`
22 `},`
23 `"required": ["name", "attributes"]`
24 `}`
25 `},`
26 `"objectTypes": {`
27 `"type": "array",`
28 `"items": {`
29 `"type": "object",`
30 `"properties": {`
31 `"name": { "type": "string" },`
32 `"attributes": {`
33 `"type": "array",`
34 `"items": {`
35 `"type": "object",`
36 `"properties": {`
37 `"name": { "type": "string" },`
38 `"type": { "type": "string" }`
39 `},`
40 `"required": ["name", "type"]`
41 `}`
42 `}`
43 `},`
44 `"required": ["name", "attributes"]`
45 `}`
46 `},`
47 `"events": {`
48 `"type": "array",`
49 `"items": {`
50 `"type": "object",`
51 `"properties": {`
52 `"id": { "type": "string" },`
53 `"type": { "type": "string" },`
54 `"time": { "type": "string", "format": "date-time" },`
55 `"attributes": {`
56 `"type": "array",`
57 `"items": {`
58 `"type": "object",`
59 `"properties": {`
60 `"name": { "type": "string" },`
61 `"value": { "type": "string" }`
62 `},`
63 `"required": ["name", "value"]`
64 `}`
65 `},`
66 `"relationships": {`
67 `"type": "array",`
68 `"items": {`
69 `"type": "object",`
70 `"properties": {`
71 `"objectId": { "type": "string" },`
72 `"qualifier": { "type": "string" }`
73 `},`
74 `"required": ["objectId", "qualifier"]`
75 `}`
76 `}`
77 `},`
78 `"required": ["id", "type", "time"]`


43


79 `}`
80 `},`
81 `"objects": {`
82 `"type": "array",`
83 `"items": {`
84 `"type": "object",`
85 `"properties": {`
86 `"id": { "type": "string" },`
87 `"type": { "type": "string" },`
88 `"relationships": {`
89 `"type": "array",`
90 `"items": {`
91 `"type": "object",`
92 `"properties": {`
93 `"objectId": { "type": "string" },`
94 `"qualifier": { "type": "string" }`
95 `},`
96 `"required": ["objectId", "qualifier"]`
97 `}`
98 `},`
99 `"attributes": {`
100 `"type": "array",`
101 `"items": {`
102 `"type": "object",`
103 `"properties": {`
104 `"name": { "type": "string" },`
105 `"value": { "type": "string" },`
106 `"time": { "type": "string", "format": "date-time" }`
107 `},`
108 `"required": ["name", "value", "time"]`
109 `}`
110 `}`
111 `},`
112 `"required": ["id", "type"]`
113 `}`
114 `}`
115 `},`
116 `"required": ["eventTypes", "objectTypes", "events", "objects"]`
117 `}`


44


### **9 Conclusion**

This document provides a comprehensive introduction to the OCEL 2.0 standard. Given
the increasing importance of Object-Centric Process Mining (OCPM), it is important to
be able to standardize Object-Centric Event Data (OCED). OCEL 2.0 aims to provide
a middle ground between simplicity and expressiveness, building upon experiences with
OCEL 1.0 over the past three years. We first provided a contextual understanding of
the object-centric process mining landscape and then discussed the motivation and the
necessities that led to the creation of the OCEL 2.0 standard.
Why is this relevant?


  - Using OCEL 2.0, it is possible to create a system-agnostic, single source of truth.
Event data should capture real business-relevant events without being limited by a
single-case notion.


  - We no longer need to create a new event log for each process (or view on a selected
process). Using traditional event logs, there may be overlapping logs that refer to
products, suppliers, etc. This leads to duplication and inconsistencies. Using OCEL
2.0, views can be created on demand without going back to the source systems.


  - OCEL 2.0 and the OCPM techniques that build upon it allow us to stay closer to
reality, also allowing organizations to uncover problems that live at the intersection
points of processes and organizational units.


Through a detailed presentation of formal definitions, we built the mathematical foundation that equips readers to effectively utilize and understand the OCEL 2.0 standard
in a scientific context. Our illustrative running example served to bridge the gap between abstract theory and practical application, enabling readers to fully grasp how the
principles of OCEL 2.0 come into play.
The detailed overview of the relational SQLite, XML, and JSON implementations
demonstrated the versatility and compatibility of the standard across multiple technological contexts. Together, these make OCEL 2.0 an accessible and practical choice for
both academics and industry practitioners.
Compared to OCEL 1.0, OCEL 2.0 allows for changes in objects, is able to relate
objects directly, and can qualify relationships between objects and events. We hope
that this will fuel new OCPM techniques using these extensions. The relational SQLite
implementation also shows that this standard goes beyond file formats like XML, JSON,
and Excel. Because the reference storage format for the XES standard was XML, people
often misunderstood the XES standard. The XES metamodel can be implemented in
many different ways. However, some vendors used the bulkiness XML as an excuse
not to support XES, thus blocking any form of standardization. However, the critical
point is the standardization and unification of concepts (not the serialization of data
using a specific syntax). Therefore, we encourage researchers and software companies to
come up with new storage formats implementing the OCEL 2.0 metamodel and provide
conversations. The SQLite, XML, and JSON formats are just examples, and we provide
tools to convert any one of them into the two other formats. However, we encourage
developers to create novel, highly scalable formats. This is one of the reasons why we
kept OCEL 2.0 as simple and as concrete as possible.
We also hope that OCEL 2.0 will also be the basis for creating _standard object and_
_event types_ for different application domains. Organizations struggle to use ontologies


45


and related technologies because the added value of extensively modeling data is not
so clear. OCPM can address this problem. Event data in OCEL 2.0 format enables
process discovery, conformance checking, performance analysis, and operational support
without the need to process the data further. However, any organization has standard
processes like Order-to-Cash (O2C) and Procure-to-Pay (P2P) that talk about suppliers,
customers, orders, items, shipments, etc. There is no need to reinvent the wheel. Also,
one would like to keep these things system-agnostic. Definitions of object types and event
types and their attributes need to be standardized. It is possible to define taxonomies
of object types and event types using inheritance notions [2]. This creates possibilities
for both generative and discriminative Artificial Intelligence (AI). Therefore, researchers
and solution providers should focus on creating standard object and event types and the
corresponding normative object-centric process models. This will prevent organizations
from starting from scratch when applying process mining and AI for the first time.
Lastly, it is essential to note that the rapidly evolving field of object-centric process
mining continues to present new challenges and opportunities. As such, the OCEL 2.0
standard, despite its substantial contribution, should be seen as a stepping stone in this
exciting journey rather than a final destination. Furthermore, this standard is intended
to help pave the path for the development of process mining techniques supporting the
journey to more sustainable operational practices. We encourage further research and
development efforts to build on this foundation, with the aim of continuously advancing
the field to new heights of innovation and practical value.
You can find further details of OCEL 2.0, example event logs, and tool support, on
our homepage:

#### `https://www.ocel-standard.org`


46


### **Acknowledgments**

Funded by the Deutsche Forschungsgemeinschaft (DFG, German Research Foundation)
under Germany’s Excellence Strategy - EXC-2023 Internet of Production - 390621612.
We also thank the Alexander von Humboldt (AvH) Stiftung for supporting our research.


47


### **References**


[1] W.M.P. van der Aalst. _Process Mining: Data Science in Action_ . Springer-Verlag,
Berlin, 2016.


[2] W.M.P van der Aalst. Object-Centric Process Mining: Unraveling the Fabric of Real
Processes. _Mathematics_, 11(12):2691, 2023.


[3] W.M.P. van der Aalst and A. Berti. Discovering Object-Centric Petri Nets. _Funda-_
_menta Informaticae_, 175(1-4):1–40, 2020.


[4] W.M.P. van der Aalst and J. Carmona, editors. _Process Mining Handbook_, volume
448 of _Lecture Notes in Business Information Processing_ . Springer-Verlag, Berlin,
2022.


[5] G. Acampora, A. Vitiello, B. Di Stefano, W. van der Aalst, C. G¨unther, and E. Verbeek. IEEE 1849: The XES Standard - The Second IEEE Standard Sponsored by
IEEE Computational Intelligence Society. _IEEE Computational Intelligence Maga-_
_zine_, 12(2):4–8, 2017.


[6] J.N. Adams, G. Park, S. Levich, D. Schuster, and W.M.P. van der Aalst. A Framework for Extracting and Encoding Features from Object-Centric Event Data. In
J. Troya, B.Medjahed, M.Piattini, L. Yao, P. Fern´andez, and A. Ruiz-Cort´es, editors, _International Conference on Service-Oriented Computing (ICSOC 2022)_, volume 13740 of _Lecture Notes in Computer Science_, pages 36–53. Springer-Verlag,
Berlin, 2022.


[7] A.F. Ghahfarokhi, G. Park, A. Berti, and W.M.P. van der Aalst. OCEL Standard.
www.ocel-standard.org, 2020.


[8] A.F. Ghahfarokhi, G. Park, A. Berti, and W.M.P. van der Aalst. OCEL: A Standard
for Object-Centric Event Logs. In L. Bellatreche, M. Dumas, and P. Karras, editors,
_New Trends in Database and Information Systems (Short Papers ADBIS 2021)_,
volume 1450 of _Communications in Computer and Information Science_, pages 169–
175. Springer-Verlag, Berlin, 2021.


[9] IEEE. IEEE Standard for eXtensible Event Stream (XES) for Achieving Interoperability in Event Logs and Event Streams. _IEEE Std 1849-2023 (Revision of IEEE_
_Std 1849-2016)_, pages 1–55, 2023. 10.1109/IEEESTD.2023.10267858.


[10] IEEE Task Force on Process Mining. XES Standard Definition. www.xesstandard.org, 2010.


[11] M. Kerremans, K. Iijima, A. Sachelarescu, N. Duffy, and D. Sugden. Magic Quadrant
for Process Mining Tools, Gartner Research Note GG00774746. www.gartner.com,
2023.


[12] M.T. Wynn, J. Lebherz, W.M.P. van der Aalst, R. Accorsi, C. Di Ciccio, L. Jayarathna, and H.M.W. Verbeek. Rethinking the Input for Process Mining: Insights
from the XES Survey and Workshop. In J. Munoz-Gama and X. Lu, editors, _Pro-_
_cess Mining Workshops of the International Conference on Process Mining (Revised_
_Selected Papers)_, volume 433 of _Lecture Notes in Business Information Processing_,
pages 3–16. Springer-Verlag, Berlin, 2021.


48


