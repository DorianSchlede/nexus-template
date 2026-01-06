<!-- Source: 11-Process_Mining_Event_Knowledge_Graphs.pdf | Chunk 3/3 -->

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


16. Denisov, V., Fahland, D., van der Aalst, W.M.P.: Unbiased, fine-grained description
of processes performance from event data. In: Weske, M., Montali, M., Weber, I.,
vom Brocke, J. (eds.) BPM 2018. LNCS, vol. 11080, pp. 139–157. Springer, Cham
[(2018). https://doi.org/10.1007/978-3-319-98648-7](https://doi.org/10.1007/978-3-319-98648-7_9) ~~9~~
17. Dumas, M., et al.: Augmented business process management systems: a research
manifesto. CoRR, abs/2201.12855 (2022)
18. Dumas, M., La Rosa, M., Mendling, J., Reijers, H.A.: Fundamentals of Business
[Process Management, 2nd edn. Springer, Heidelberg (2018). https://doi.org/10.](https://doi.org/10.1007/978-3-662-56509-4)
[1007/978-3-662-56509-4](https://doi.org/10.1007/978-3-662-56509-4)
[19. Esser, S., Fahland, D.: Event Graph of BPI Challenge 2014. Dataset. https://doi.](https://doi.org/10.4121/14169494)
[org/10.4121/14169494](https://doi.org/10.4121/14169494)
[20. Esser, S., Fahland, D.: Event Graph of BPI Challenge 2015. Dataset. https://doi.](https://doi.org/10.4121/14169569)
[org/10.4121/14169569](https://doi.org/10.4121/14169569)
[21. Esser, S., Fahland, D.: Event Graph of BPI Challenge 2016. Dataset. https://doi.](https://doi.org/10.4121/14164220)
[org/10.4121/14164220](https://doi.org/10.4121/14164220)
[22. Esser, S., Fahland, D.: Event Graph of BPI Challenge 2017. Dataset. https://doi.](https://doi.org/10.4121/14169584)
[org/10.4121/14169584](https://doi.org/10.4121/14169584)
[23. Esser, S., Fahland, D.: Event Graph of BPI Challenge 2019. Dataset. https://doi.](https://doi.org/10.4121/14169614)
[org/10.4121/14169614](https://doi.org/10.4121/14169614)
24. Esser, S., Fahland, D.: Event Data and Queries for Multi-Dimensional Event Data
[in the Neo4j Graph Database, April 2021. https://doi.org/10.5281/zenodo.4708117](https://doi.org/10.5281/zenodo.4708117)
25. Esser, S., Fahland, D.: Multi-dimensional event data in graph databases. J. Data
Semant. **10** [(1–2), 109–141 (2021). https://doi.org/10.1007/s13740-021-0122-1](https://doi.org/10.1007/s13740-021-0122-1)
26. Fahland, D.: Describing behavior of processes with many-to-many interactions. In:
Donatelli, S., Haar, S. (eds.) PETRI NETS 2019. LNCS, vol. 11522, pp. 3–24.
[Springer, Cham (2019). https://doi.org/10.1007/978-3-030-21571-2](https://doi.org/10.1007/978-3-030-21571-2_1) ~~1~~
27. Fahland, D.: Petri’s understanding of nets. In: Reisig, W., Rozenberg, G. (eds.)
Carl Adam Petri: Ideas, Personality, Impact, pp. 31–36. Springer, Cham (2019).
[https://doi.org/10.1007/978-3-319-96154-5](https://doi.org/10.1007/978-3-319-96154-5_5) ~~5~~
28. Fahland, D.: multi-dimensional-process-mining/eventgraph tutorial, April 2022
29. Fahland, D., de Leoni, M., van Dongen, B.F., van der Aalst, W.M.P.: Behavioral
conformance of artifact-centric process models. In: Abramowicz, W. (ed.) BIS 2011.
[LNBIP, vol. 87, pp. 37–49. Springer, Heidelberg (2011). https://doi.org/10.1007/](https://doi.org/10.1007/978-3-642-21863-7_4)
[978-3-642-21863-7](https://doi.org/10.1007/978-3-642-21863-7_4) ~~4~~
30. Fahland, D., Denisov, V., van der Aalst, W.M.P.: Inferring unobserved events in
systems with shared resources and queues. Fundam. Informaticae **183** (3–4), 203–
[242 (2021). https://doi.org/10.3233/FI-2021-2087](https://doi.org/10.3233/FI-2021-2087)
31. Fahland, D., Pr¨ufer, R.: Data and abstraction for scenario-based modeling with
petri nets. In: Haddad, S., Pomello, L. (eds.) PETRI NETS 2012. LNCS, vol.
[7347, pp. 168–187. Springer, Heidelberg (2012). https://doi.org/10.1007/978-3-](https://doi.org/10.1007/978-3-642-31131-4_10)
[642-31131-4](https://doi.org/10.1007/978-3-642-31131-4_10) ~~1~~ 0
32. Goh, K., Pentland, B.: From actions to paths to patterning: toward a dynamic
theory of patterning in routines. Acad. Manag. Ann. **62**, 1901–1929 (2019)
33. Hogan, A., et al.: Knowledge graphs. ACM Comput. Surv. **54** [(4) (2021). https://](https://doi.org/10.1145/3447772)
[doi.org/10.1145/3447772](https://doi.org/10.1145/3447772)
34. Jalali, A.: Graph-based process mining. In: Leemans, S., Leopold, H. (eds.) ICPM
[2020. LNBIP, vol. 406, pp. 273–285. Springer, Cham (2021). https://doi.org/10.](https://doi.org/10.1007/978-3-030-72693-5_21)
[1007/978-3-030-72693-5](https://doi.org/10.1007/978-3-030-72693-5_21) ~~2~~ 1
35. Jans, M., Soffer, P.: From relational database to event log: decisions with quality
impact. In: Teniente, E., Weidlich, M. (eds.) BPM 2017. LNBIP, vol. 308, pp.
[588–599. Springer, Cham (2018). https://doi.org/10.1007/978-3-319-74030-0](https://doi.org/10.1007/978-3-319-74030-0_46) ~~4~~ 6


318 D. Fahland


36. Klijn, E.L., Fahland, D.: Performance mining for batch processing using the performance spectrum. In: Di Francescomarino, C., Dijkman, R., Zdun, U. (eds.) BPM
[2019. LNBIP, vol. 362, pp. 172–185. Springer, Cham (2019). https://doi.org/10.](https://doi.org/10.1007/978-3-030-37453-2_15)
[1007/978-3-030-37453-2](https://doi.org/10.1007/978-3-030-37453-2_15) ~~1~~ 5
37. Klijn, E.L., Fahland, D.: Identifying and reducing errors in remaining time predic[tion due to inter-case dynamics. In: ICPM 2020, pp. 25–32. IEEE (2020). https://](https://doi.org/10.1109/ICPM49681.2020.00015)
[doi.org/10.1109/ICPM49681.2020.00015](https://doi.org/10.1109/ICPM49681.2020.00015)
38. Klijn, E.L., Mannhardt, F., Fahland, D.: Classifying and detecting task executions
and routines in processes using event graphs. In: Polyvyanyy, A., Wynn, M.T., Van
Looy, A., Reichert, M. (eds.) BPM 2021. LNBIP, vol. 427, pp. 212–229. Springer,
[Cham (2021). https://doi.org/10.1007/978-3-030-85440-9](https://doi.org/10.1007/978-3-030-85440-9_13) ~~1~~ 3
39. Li, G., de Carvalho, R.M., van der Aalst, W.M.P.: Automatic discovery of objectcentric behavioral constraint models. In: Abramowicz, W. (ed.) BIS 2017. LNBIP,
[vol. 288, pp. 43–58. Springer, Cham (2017). https://doi.org/10.1007/978-3-319-](https://doi.org/10.1007/978-3-319-59336-4_4)
[59336-4](https://doi.org/10.1007/978-3-319-59336-4_4) ~~4~~
40. Li, G., de Murillas, E.G.L., de Carvalho, R.M., van der Aalst, W.M.P.: Extracting
object-centric event logs to support process mining on databases. In: Mendling, J.,
Mouratidis, H. (eds.) CAiSE 2018. LNBIP, vol. 317, pp. 182–199. Springer, Cham
[(2018). https://doi.org/10.1007/978-3-319-92901-9](https://doi.org/10.1007/978-3-319-92901-9_16) ~~1~~ 6
41. Xixi, L., Nagelkerke, M., van de Wiel, D., Fahland, D.: Discovering interacting
artifacts from ERP systems. IEEE Trans. Serv. Comput. **8** (6), 861–873 (2015)
42. Martin, N., Pufahl, L., Mannhardt, F.: Detection of batch activities from event
logs. Inf. Syst. **95**, 101642 (2021)
43. Nooijen, E.H.J., van Dongen, B.F., Fahland, D.: Automatic discovery of datacentric and artifact-centric processes. In: La Rosa, M., Soffer, P. (eds.) BPM 2012.
[LNBIP, vol. 132, pp. 316–327. Springer, Heidelberg (2013). https://doi.org/10.](https://doi.org/10.1007/978-3-642-36285-9_36)
[1007/978-3-642-36285-9](https://doi.org/10.1007/978-3-642-36285-9_36) ~~3~~ 6
44. Pegoraro, M., Bakullari, B., Uysal, M.S., van der Aalst, W.M.P.: Probability estimation of uncertain process trace realizations. In: Munoz-Gama, J., Lu, X. (eds.)
[ICPM 2021. LNBIP, vol. 433, pp. 21–33. Springer, Cham (2021). https://doi.org/](https://doi.org/10.1007/978-3-030-98581-3_2)
[10.1007/978-3-030-98581-3](https://doi.org/10.1007/978-3-030-98581-3_2) ~~2~~
45. Piessens, D.A.M.: Event log extraction from SAP ECC 6.0. Master’s thesis, Eindhoven University of Technology (2011)
46. Popova, V., Fahland, D., Dumas, M.: Artifact lifecycle discovery. Int. J. Cooperative Inf. Syst. **24** [(1), 1550001:1–1550001:44 (2015). https://doi.org/10.1142/](https://doi.org/10.1142/S021884301550001X)
[S021884301550001X](https://doi.org/10.1142/S021884301550001X)
47. Pourmirza, S., Dijkman, R.M., Grefen, P.: Correlation miner: mining business process models and event correlations without case identifiers. Int. J. Cooperative Inf.
Syst. **26** (2):1742002:1–1742002:32 (2017)
48. Robinson, I., Webber, J., Eifrem, E.: Graph Databases. O’Reilly Media, Sebastopol
(2013)
49. Schruben, L.: Simulation modeling with event graphs. Commun. ACM **26** (11),
957–963 (1983)
50. Stoica, R., Fletcher, G.H.L., Sequeda, J.F.: On directly mapping relational
databases to property graphs. In: 13th Alberto Mendelzon International Workshop on Foundations of Data Management. CEUR Workshop Proceedings, vol.
2369. CEUR-WS.org (2019)
51. Toosinezhad, Z., Fahland, D., K¨oroglu, O., van der Aalst, W.M.P.: Detecting [¨]
system-level behavior leading to dynamic bottlenecks. In: ICPM 2020, pp. 17–24.
[IEEE (2020). https://doi.org/10.1109/ICPM49681.2020.00014](https://doi.org/10.1109/ICPM49681.2020.00014)


Event Knowledge Graphs 319


52. Aalst, W.M.P.: Object-centric process mining: dealing with divergence and convergence in event data. In: Olveczky, P.C., Sala¨un, G. (eds.) SEFM 2019. LNCS, [¨]
[vol. 11724, pp. 3–25. Springer, Cham (2019). https://doi.org/10.1007/978-3-030-](https://doi.org/10.1007/978-3-030-30446-1_1)
[30446-1](https://doi.org/10.1007/978-3-030-30446-1_1) ~~1~~
53. van der Wil, M.P.: Aalst and Alessandro Berti. Discovering object-centric petri
nets. Fundam. Informaticae **175** (1–4), 1–40 (2020)
54. van der Aalst, W.M.P., Tacke Genannt Unterberg, D., Denisov, V., Fahland, D.:
Visualizing token flows using interactive performance spectra. In: Janicki, R.,
Sidorova, N., Chatain, T. (eds.) PETRI NETS 2020. LNCS, vol. 12152, pp. 369–
[380. Springer, Cham (2020). https://doi.org/10.1007/978-3-030-51831-8](https://doi.org/10.1007/978-3-030-51831-8_18) ~~1~~ 8
55. Waibel, P., Novak, C., Bala, S., Revoredo, K., Mendling, J.: Analysis of business
process batching using causal event models. In: Leemans, S., Leopold, H. (eds.)
[ICPM 2020. LNBIP, vol. 406, pp. 17–29. Springer, Cham (2021). https://doi.org/](https://doi.org/10.1007/978-3-030-72693-5_2)
[10.1007/978-3-030-72693-5](https://doi.org/10.1007/978-3-030-72693-5_2) ~~2~~
56. Waibel, P., Pfahlsberger, L., Revoredo, K., Mendling, J.: Causal process min[ing from relational databases with domain knowledge (2022). https://doi.org/10.](https://doi.org/10.48550/ARXIV.2202.08314)
[48550/ARXIV.2202.08314](https://doi.org/10.48550/ARXIV.2202.08314)


**Open Access** This chapter is licensed under the terms of the Creative Commons
[Attribution 4.0 International License (http://creativecommons.org/licenses/by/4.0/),](http://creativecommons.org/licenses/by/4.0/)
which permits use, sharing, adaptation, distribution and reproduction in any medium
or format, as long as you give appropriate credit to the original author(s) and the
source, provide a link to the Creative Commons license and indicate if changes were
made.
The images or other third party material in this chapter are included in the
chapter’s Creative Commons license, unless indicated otherwise in a credit line to the
material. If material is not included in the chapter’s Creative Commons license and
your intended use is not permitted by statutory regulation or exceeds the permitted
use, you will need to obtain permission directly from the copyright holder.


