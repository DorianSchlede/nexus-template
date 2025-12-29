<!-- Source: 02-Knowledge_Graphs.pdf | Chunk 9/15 -->

embeddings) [548]; _shape induction_, in order to extract and formalise inherent patterns in the

knowledge graph as constraints [350]; and _contextual knowledge graph embeddings_ that provide

numeric representations of nodes and edges that vary with time, place, etc. [282]. Finally, in the

intersection of deductive and inductive knowledge, we mention the topics of _entailment-aware_

_knowledge graph embeddings_ [125, 207], that incorporate rules and/or ontologies when computing

plausibility; _expressive graph neural networks_ proven capable of complex classification analogous to

expressive ontology languages [32]; as well as further advances on _rule and axiom mining_, allowing

to extract symbolic, deductive representations from the knowledge graphs [73, 169].

Aside from specific topics, more general challenges for knowledge graphs include _scalability_,

particularly for deductive and inductive reasoning; _quality_, not only in terms of data, but also the

models induced from knowledge graphs; _diversity_, such as managing contextual or multi-modal

data; _dynamicity_, considering temporal or streaming data; and finally _usability_, which is key to

increasing adoption. Though techniques are continuously being proposed to address precisely these

challenges, they are unlikely to ever be completely “solved”; rather they serve as dimensions along

which knowledge graphs, and their techniques, tools, etc., will continue to mature.

Given the availability of open knowledge graphs whose quality continue to improve, as well

as the growing adoption of enterprise knowledge graphs in various industries, future research on

knowledge graphs has the potential to foster key advancements in broad aspects of society. Here

we have highlighted just some examples of future research directions of importance to this pursuit.


_Acknowledgements:_ We thank the attendees of the Dagstuhl Seminar on “Knowledge Graphs”

for discussions that inspired and influenced this paper, and all those that make such seminars

possible. We would also like to thank Matteo Palmonari for feedback on Figures 3 and 4, as well as

Stefan Decker and Carlos Bobed who provided suggestions for the paper. Hogan was supported by

Fondecyt Grant No. 1181896. Hogan and Gutierrez were funded by ANID – Millennium Science

Initiative Program – Code ICN17_002. Cochez did part of the work while employed at Fraunhofer

FIT, Germany and was later partially funded by Elsevier’s Discovery Lab. Kirrane, Ngonga Ngomo,

Polleres and Staab received funding through the project “KnowGraphs” from the European Union’s

Horizon programme under the Marie Skłodowska-Curie grant agreement No. 860801. Kirrane and

Polleres were supported by the European Union’s Horizon 2020 research and innovation programme

under grant 731601. Labra was supported by the Spanish Ministry of Economy and Competitiveness

(Society challenges: TIN2017-88877-R). Navigli was supported by the MOUSSE ERC Grant No.

726487 under the European Union’s Horizon 2020 research and innovation programme. Rashid was

supported by IBM Research AI through the AI Horizons Network. Schmelzeisen was supported by

the German Research Foundation (DFG) grant STA 572/18-1.


78


**REFERENCES**


[1] 2019. _7th International Conference on Learning Representations, ICLR 2019, New Orleans, LA, USA, May 6-9, 2019_ .

[OpenReview.net. https://openreview.net/group?id=ICLR.cc/2019/conference](https://openreview.net/group?id=ICLR.cc/2019/conference)

[2] Karl Aberer, Key-Sun Choi, Natasha Fridman Noy, Dean Allemang, Kyung-Il Lee, Lyndon J. B. Nixon, Jennifer Golbeck,

Peter Mika, Diana Maynard, Riichiro Mizoguchi, Guus Schreiber, and Philippe Cudré-Mauroux (Eds.). 2007. _The_

_Semantic Web, 6th International Semantic Web Conference, 2nd Asian Semantic Web Conference, ISWC 2007 + ASWC_

_2007, Busan, Korea, November 11-15, 2007_ . Lecture Notes in Computer Science, Vol. 4825. Springer.

[3] Serge Abiteboul. 1997. Querying Semi-Structured Data. In _Database Theory - ICDT ’97, 6th International Conference,_

_Delphi, Greece, January 8-10, 1997, Proceedings (Lecture Notes in Computer Science)_, Foto N. Afrati and Phokion G.

[Kolaitis (Eds.), Vol. 1186. Springer, 1–18. https://doi.org/10.1007/3-540-62222-5_33](https://doi.org/10.1007/3-540-62222-5_33)

[4] Sushant Agarwal, Simon Steyskal, Franjo Antunovic, and Sabrina Kirrane. 2018. Legislative Compliance Assessment:

Framework, Model and GDPR Instantiation. In _Privacy Technologies and Policy - 6th Annual Privacy Forum, APF 2018,_

_Barcelona, Spain, June 13-14, 2018, Revised Selected Papers (Lecture Notes in Computer Science)_, Manel Medina, Andreas

Mitrakas, Kai Rannenberg, Erich Schweighofer, and Nikolaos Tsouroulas (Eds.), Vol. 11079. Springer, 131–149.

[5] Rakesh Agrawal, Tomasz Imieliński, and Arun Swami. 1993. Mining association rules between sets of items in large

databases. In _Proceedings of the 1993 ACM SIGMOD International Conference on Management of Data, Washington, DC,_

_USA, May 26-28, 1993_, Peter Buneman and Sushil Jajodia (Eds.). ACM Press, 207–216.

[6] Jinhyun Ahn, Dong-Hyuk Im, Jae-Hong Eom, Nansu Zong, and Hong-Gee Kim. 2015. G-Diff: A Grouping Algorithm

for RDF Change Detection on MapReduce. In _Semantic Technology - 4th Joint International Conference, JIST 2014,_

_Chiang Mai, Thailand, November 9-11, 2014. Revised Selected Papers (Lecture Notes in Computer Science)_, Thepchai

Supnithi, Takahira Yamaguchi, Jeff Z. Pan, Vilas Wuwongse, and Marut Buranarach (Eds.), Vol. 8943. Springer,

230–235.

[7] Adnan Akhter, Axel-Cyrille Ngonga Ngomo, and Muhammad Saleem. 2018. An Empirical Evaluation of RDF Graph

Partitioning Techniques. In _Knowledge Engineering and Knowledge Management - 21st International Conference, EKAW_

_2018, Nancy, France, November 12-16, 2018, Proceedings (Lecture Notes in Computer Science)_, Catherine Faron-Zucker,

Chiara Ghidini, Amedeo Napoli, and Yannick Toussaint (Eds.), Vol. 11313. Springer, 3–18.

[8] Tareq Al-Moslmi, Marc Gallofré Ocaña, Andreas L. Opdahl, and Csaba Veres. 2020. Named Entity Extraction for

Knowledge Graphs: A Literature Overview. _IEEE Access_ [8 (2020), 32862–32881. https://doi.org/10.1109/ACCESS.2020.](https://doi.org/10.1109/ACCESS.2020.2973928)

[2973928](https://doi.org/10.1109/ACCESS.2020.2973928)

[9] Harith Alani, Lalana Kagal, Achille Fokoue, Paul T. Groth,, Josian Xavier Parreira, Lora Aroyo, Natasha Fridman Noy,

Christopher A. Welty, and Krzysztof Janowicz (Eds.). 2013. _The Semantic Web - ISWC 2013 - 12th International Semantic_

_Web Conference, Sydney, NSW, Australia, October 21-25, 2013, Proceedings, Part II_ . Lecture Notes in Computer Science,

Vol. 8219. Springer.

[10] Harith Alani, Lalana Kagal, Achille Fokoue, Paul T. Groth,, Josian Xavier Parreira, Lora Aroyo, Natasha Fridman Noy,

Christopher A. Welty, and Krzysztof Janowicz (Eds.). 2013. _The Semantic Web - ISWC 2013 - 12th International Semantic_

_Web Conference, Sydney, NSW, Australia, October 21-25, 2013, Proceedings, Part I_ . Lecture Notes in Computer Science,

Vol. 8218. Springer.

[11] Keith Alexander, Richard Cyganiak, Michael Hausenblas, and Jun Zhao. 2009. Describing Linked Datasets. In

_Proceedings of the WWW2009 Workshop on Linked Data on the Web, LDOW 2009, Madrid, Spain, April 20, 2009 (CEUR_

_Workshop Proceedings)_, Christian Bizer, Tom Heath, Tim Berners-Lee, and Michael Hausenblas (Eds.), Vol. 538. Sun

[SITE Central Europe (CEUR), 10. http://ceur-ws.org/Vol-538/ldow2009_paper20.pdf](http://ceur-ws.org/Vol-538/ldow2009_paper20.pdf)

[12] Gustavo Alonso, José A. Blakeley, and Arbee L. P. Chen (Eds.). 2008. _Proceedings of the 24th International Conference_

_on Data Engineering, ICDE 2008, April 7-12, 2008, Cancún, Mexico_ . IEEE Computer Society.

[13] Ricardo Alonso Maturana, Elena Alvarado-Cortes, Susana López-Sola, María Ortega Martínez-Losa, and Pablo

Hermoso-González. 2018. La Rioja Turismo: The Construction and Exploitation of a Queryable Tourism Knowledge

Graph. In _Current Trends in Web Engineering - ICWE 2018 International Workshops, MATWEP, EnWot, KD-WEB, WEOD,_

_TourismKG, Cáceres, Spain, June 5, 2018, Revised Selected Papers (Lecture Notes in Computer Science)_, Cesare Pautasso,

Fernando Sánchez-Figueroa, Kari Systä, and Juan Manuel Murillo Rodriguez (Eds.), Vol. 11153. Springer, 213–220.

[14] Renzo Angles. 2018. The Property Graph Database Model. In _Proceedings of the 12th Alberto Mendelzon International_

_Workshop on Foundations of Data Management, Cali, Colombia, May 21–25, 2018 (CEUR Workshop Proceedings)_,

[Dan Olteanu and Barbara Poblete (Eds.), Vol. 2100. Sun SITE Central Europe (CEUR), 10. http://ceur-ws.org/Vol-](http://ceur-ws.org/Vol-2100/paper26.pdf)

[2100/paper26.pdf](http://ceur-ws.org/Vol-2100/paper26.pdf)

[15] Renzo Angles, Marcelo Arenas, Pablo Barceló, Peter A. Boncz, George H. L. Fletcher, Claudio Gutierrez, Tobias

Lindaaker, Marcus Paradies, Stefan Plantikow, Juan F. Sequeda, Oskar van Rest, and Hannes Voigt. 2018. G-CORE: A

Core for Future Graph Query Languages, See [117], 1421–1432.

[16] Renzo Angles, Marcelo Arenas, Pablo Barceló, Aidan Hogan, Juan L. Reutter, and Domagoj Vrgoc. 2017. Foundations

of Modern Query Languages for Graph Databases. _ACM Computing Surveys_ 50, 5 (2017), 68:1–68:40. [https:](https://doi.org/10.1145/3104031)


[79](https://doi.org/10.1145/3104031)


[//doi.org/10.1145/3104031](https://doi.org/10.1145/3104031)

[17] Renzo Angles and Claudio Gutiérrez. 2008. Survey of graph database models. _ACM Computing Surveys_ 40, 1 (2008),

[1:1–1:39. https://doi.org/10.1145/1322432.1322433](https://doi.org/10.1145/1322432.1322433)

[18] Renzo Angles, Harsh Thakkar, and Dominik Tomaszuk. 2019. RDF and Property Graphs Interoperability: Status and

[Issues, See [249], 11. http://ceur-ws.org/Vol-2369/paper01.pdf](http://ceur-ws.org/Vol-2369/paper01.pdf)

[19] Mikel Egaña Aranguren, Erick Antezana, Martin Kuiper, and Robert Stevens. 2008. Ontology Design Patterns for bio
ontologies: a case study on the Cell Cycle Ontology. _BMC Bioinformatics_ [9, 5 (2008), S1. https://doi.org/10.1186/1471-](https://doi.org/10.1186/1471-2105-9-S5-S1)

[2105-9-S5-S1](https://doi.org/10.1186/1471-2105-9-S5-S1)

[20] Marcelo Arenas, Alexandre Bertails, Eric Prud’hommeaux, and Juan Sequeda. 2012. _A Direct Mapping of Relational_

_Data to RDF, W3C Recommendation 27 September 2012_ . W3C Recommendation. World Wide Web Consortium.

[https://www.w3.org/TR/2012/REC-rdb-direct-mapping-20120927/](https://www.w3.org/TR/2012/REC-rdb-direct-mapping-20120927/)

[21] Alessandro Artale, Diego Calvanese, Roman Kontchakov, and Michael Zakharyaschev. 2009. The DL-Lite Family and

Relations. _Journal of Artificial Intelligence Research_ 36 (2009), 1–69.

[22] Sören Auer, Christian Bizer, Georgi Kobilarov, Jens Lehmann, Richard Cyganiak, and Zachary Ives. 2007. DBpedia: A

Nucleus for a Web of Open Data, See [2], 722–735.

[23] Franz Baader, Ian Horrocks, Carsten Lutz, and Ulrike Sattler. 2017. _An Introduction to Description Logic_ . Cambridge

University Press, Cambridge, United Kingdom.

[24] Nguyen Bach and Sameer Badaskar. 2007. _A Review of Relation Extraction_ . Technical Report. Carnegie Mellon

University.

[25] Ricardo Baeza-Yates. 2018. Bias on the Web. _Communications of the ACM_ [61, 6 (2018), 54–61. https://doi.org/10.1145/](https://doi.org/10.1145/3209581)

[3209581](https://doi.org/10.1145/3209581)

[26] Collin F. Baker, Charles J. Fillmore, and John B. Lowe. 1998. The Berkeley FrameNet Project. In _36th Annual Meeting of_

_the Association for Computational Linguistics and 17th International Conference on Computational Linguistics, COLING-_

_ACL’98, August 10-14, 1998, Université de Montréal, Montréal, Quebec, Canada. Proceedings of the Conference_, Christian

Boitet and Pete Whitelock (Eds.). Morgan Kaufmann, 86–90.

[27] René Ronald Bakker. 1987. _Knowledge Graphs: Representation and Structuring of Scientific Knowledge_ . Ph.D. Dissertation.

University of Twente.

[28] Ivana Balazevic, Carl Allen, and Timothy M. Hospedales. 2019. Hypernetwork Knowledge Graph Embeddings. In

_Artificial Neural Networks and Machine Learning - ICANN 2019 - 28th International Conference on Artificial Neural_

_Networks, Munich, Germany, September 17-19, 2019, Proceedings - Workshop and Special Sessions (Lecture Notes in_

_Computer Science)_, Igor V. Tetko, Vera Kurková, Pavel Karpov, and Fabian J. Theis (Eds.), Vol. 11731. Springer, 553–565.

[29] Ivana Balazevic, Carl Allen, and Timothy M. Hospedales. 2019. Multi-relational Poincaré Graph Embeddings, See

[[546], 4465–4475. http://papers.nips.cc/book/advances-in-neural-information-processing-systems-32-2019](http://papers.nips.cc/book/advances-in-neural-information-processing-systems-32-2019)

[30] Ivana Balazevic, Carl Allen, and Timothy M. Hospedales. 2019. TuckER: Tensor Factorization for Knowledge Graph

Completion. In _Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing and the 9th_

_International Joint Conference on Natural Language Processing, EMNLP-IJCNLP 2019, Hong Kong, China, November 3-7,_

_2019_, Kentaro Inui, Jing Jiang, Vincent Ng, and Xiaojun Wan (Eds.). The Association for Computational Linguistics,

[5184–5193. https://aclweb.org/anthology/volumes/D19-1/](https://aclweb.org/anthology/volumes/D19-1/)

[31] Michele Banko, Michael J. Cafarella, Stephen Soderland, Matthew Broadhead, and Oren Etzioni. 2007. Open Infor
mation Extraction from the Web. In _IJCAI 2007, Proceedings of the 20th International Joint Conference on Artificial_

_Intelligence, Hyderabad, India, January 6-12, 2007_, Manuela M. Veloso (Ed.). AAAI Press, 2670–2676.

[32] Pablo Barceló, Egor V. Kostylev, Mikael Monet, Jorge Peréz, Juan Reutter, and Juan Pablo Silva. 2020. The Logical

Expressiveness of Graph Neural Networks. In _8th International Conference on Learning Representations, ICLR 2020,_

_Addis Ababa, Ethiopia, April 26–30, 2020_ [. OpenReview.net, 20. https://openreview.net/forum?id=r1lZ7AEKvB](https://openreview.net/forum?id=r1lZ7AEKvB)

[33] Carlo Batini, Anisa Rula, Monica Scannapieco, and Gianluigi Viscusi. 2015. From Data Quality to Big Data Quality.

_Journal of Database Management_ [26, 1 (2015), 60–82. https://doi.org/10.4018/JDM.2015010103](https://doi.org/10.4018/JDM.2015010103)

[34] Carlo Batini and Monica Scannapieco. 2016. _Data and Information Quality - Dimensions, Principles and Techniques_ .

Springer.

[35] Luigi Bellomarini, Daniele Fakhoury, Georg Gottlob, and Emanuel Sallinger. 2019. Knowledge Graphs and Enterprise

AI: The Promise of an Enabling Technology, See [262], 26–37.

[36] Luigi Bellomarini, Emanuel Sallinger, and Georg Gottlob. 2018. The Vadalog System: Datalog-based Reasoning for

Knowledge Graphs. _Proceedings of the VLDB Endowment_ 11, 9 (2018), 975–987.

[37] Claus Bendtsen and Slavé Petrovski. 2019. How data and AI are helping unlock the secrets of disease. AstraZeneca

[Blog. https://www.astrazeneca.com/what-science-can-do/labtalk-blog/uncategorized/how-data-and-ai-are-helping-](https://www.astrazeneca.com/what-science-can-do/labtalk-blog/uncategorized/how-data-and-ai-are-helping-unlock-the-secrets-of-disease.html)

[unlock-the-secrets-of-disease.html.](https://www.astrazeneca.com/what-science-can-do/labtalk-blog/uncategorized/how-data-and-ai-are-helping-unlock-the-secrets-of-disease.html)

[38] Samy Bengio, Hanna M. Wallach, Hugo Larochelle, Kristen Grauman, Nicolò Cesa-Bianchi, and Roman Garnett (Eds.).

2018. _Advances in Neural Information Processing Systems 31: Annual Conference on Neural Information Processing_


80


_Systems 2018, NeurIPS 2018, 3-8 December 2018, Montréal, Canada_ [. http://papers.nips.cc/book/advances-in-neural-](http://papers.nips.cc/book/advances-in-neural-information-processing-systems-31-2018)

[information-processing-systems-31-2018](http://papers.nips.cc/book/advances-in-neural-information-processing-systems-31-2018)

[39] Yoshua Bengio and Yann LeCun (Eds.). 2013. _1st International Conference on Learning Representations, ICLR 2013,_

_Scottsdale, Arizona, USA, May 2-4, 2013, Workshop Track Proceedings_ [. OpenReview.net. https://openreview.net/group?](https://openreview.net/group?id=ICLR.cc/2013)

[id=ICLR.cc/2013](https://openreview.net/group?id=ICLR.cc/2013)

[40] Michael K. Bergman. 2019. A Common Sense View of Knowledge Graphs. Adaptive Information, Adaptive Innovation,

[Adaptive Infrastructure Blog. http://www.mkbergman.com/2244/a-common-sense-view-of-knowledge-graphs/.](http://www.mkbergman.com/2244/a-common-sense-view-of-knowledge-graphs/)

[[41] Tim Berners-Lee. 2006. Linked Data. W3C Design Issues. https://www.w3.org/DesignIssues/LinkedData.html.](https://www.w3.org/DesignIssues/LinkedData.html)

[42] Tim Berners-Lee and Dan Connolly. 2011. _Notation3 (N3): A readable RDF syntax, W3C Team Submission 28 March_

_2011_ [. W3C Team Submission. World Wide Web Consortium. https://www.w3.org/TeamSubmission/2011/SUBM-n3-](https://www.w3.org/TeamSubmission/2011/SUBM-n3-20110328/)

[20110328/](https://www.w3.org/TeamSubmission/2011/SUBM-n3-20110328/)

[43] Tim Berners-Lee, James Hendler, and Ora Lassila. 2001. The Semantic Web. _Scientific American_ 284, 5 (May 2001),

34–43.

[44] Abraham Bernstein, David R. Karger, Tom Heath, Lee Feigenbaum, Diana Maynard, Enrico Motta, and Krishnaprasad

Thirunarayan (Eds.). 2009. _The Semantic Web - ISWC 2009, 8th International Semantic Web Conference, ISWC 2009,_

_Chantilly, VA, USA, October 25-29, 2009. Proceedings_ . Lecture Notes in Computer Science, Vol. 5823. Springer.

[45] Anant P. Bhardwaj, Souvik Bhattacherjee, Amit Chavan, Amol Deshpande, Aaron J. Elmore, Samuel Madden, and

Aditya G. Parameswaran. 2015. DataHub: Collaborative Data Science & Dataset Version Management at Scale, See

[[92], 7. http://cidrdb.org/cidr2015/Papers/CIDR15_Paper18.pdf](http://cidrdb.org/cidr2015/Papers/CIDR15_Paper18.pdf)

[46] Daniel M. Bikel, Richard M. Schwartz, and Ralph M. Weischedel. 1999. An Algorithm that Learns What’s in a Name.

_Machine Learning_ 34, 1–3 (1999), 211–231.

[47] Stefan Bischof, Stefan Decker, Thomas Krennwallner, Nuno Lopes, and Axel Polleres. 2012. Mapping between RDF

and XML with XSPARQL. _Journal of Web Semantics_ 1, 3 (2012), 147–185.

[48] Christian Bizer, Jens Lehmann, Georgi Kobilarov, Sören Auer, Christian Becker, Richard Cyganiak, and Sebastian

Hellmann. 2009. DBpedia-A crystallization point for the Web of Data. _Journal of Web Semantics_ 7, 3 (2009), 154–165.

[49] Eva Blomqvist, Paolo Ciancarini, Francesco Poggi, and Fabio Vitali (Eds.). 2016. _Knowledge Engineering and Knowledge_

_Management - 20th International Conference, EKAW 2016, Bologna, Italy, November 19-23, 2016, Proceedings_ . Lecture

Notes in Computer Science, Vol. 10024. Springer.

[50] Eva Blomqvist, Karl Hammar, and Valentina Presutti. 2016. Engineering Ontologies with Patterns – The eXtreme

Design Methodology. In _Ontology Engineering with Ontology Design Patterns_, Pascal Hitzler, Aldo Gangemi, Krzysztof

Janowicz, Adila Krisnadhi, and Valentina Presutti (Eds.). Studies on the Semantic Web, Vol. 25. IOS Press.

[51] Eva Blomqvist, Diana Maynard, Aldo Gangemi, Rinke Hoekstra, Pascal Hitzler, and Olaf Hartig (Eds.). 2017. _The_

_Semantic Web - 14th International Conference, ESWC 2017, Portorož, Slovenia, May 28 - June 1, 2017, Proceedings, Part I_ .

Lecture Notes in Computer Science, Vol. 10249. Springer.

[52] Eva Blomqvist and Kurt Sandkuhl. 2005. Patterns in Ontology Engineering: Classification of Ontology Patterns. In

_ICEIS 2005, Proceedings of the Seventh International Conference on Enterprise Information Systems, Miami, USA, May_

_25-28, 2005_, Chin-Sheng Chen, Joaquim Filipe, Isabel Seruca, and José Cordeiro (Eds.), Vol. 3. 413–416.

[53] Eva Blomqvist, Azam Seil Sepour, and Valentina Presutti. 2012. Ontology Testing - Methodology and Tool. In

_Knowledge Engineering and Knowledge Management - 18th International Conference, EKAW 2012, Galway City, Ireland,_

_October 8-12, 2012. Proceedings (Lecture Notes in Computer Science)_, Annette ten Teije, Johanna Völker, Siegfried

Handschuh, Heiner Stuckenschmidt, Mathieu d’Aquin, Andriy Nikolov, Nathalie Aussenac-Gilles, and Nathalie

Hernandez (Eds.), Vol. 7603. Springer, 216–226.

[54] Kurt Bollacker, Robert Cook, and Patrick Tufts. 2007. Freebase: A Shared Database of Structured General Human

Knowledge. In _Proceedings of the Twenty-Second AAAI Conference on Artificial Intelligence, July 22-26, 2007, Vancouver,_

_British Columbia, Canada_ . AAAI Press, 1962–1963.

[55] Kurt Bollacker, Patrick Tufts, Tomi Pierce, and Robert Cook. 2007. A platform for scalable, collaborative, structured

information integration. In _Intl. Workshop on Information Integration on the Web (IIWeb’07)_, Ullas Nambiar and Zaiqing

Nie (Eds.). 6.

[56] Piero Bonatti, Sabrina Kirrane, Iliana Mineva Petrova, Luigi Sauro, and Eva Schlehahn. 2019. _The SPECIAL Usage Policy_

_Language, V1.0_ [. Draft. Vienna University of Economics and Business. https://ai.wu.ac.at/policies/policylanguage/](https://ai.wu.ac.at/policies/policylanguage/)

[57] Piero Andrea Bonatti, Stefan Decker, Axel Polleres, and Valentina Presutti. 2018. Knowledge Graphs: New Directions

for Knowledge Representation on the Semantic Web (Dagstuhl Seminar 18371). _Dagstuhl Reports_ 8, 9 (2018), 29–111.

[58] Piero A. Bonatti, Aidan Hogan, Axel Polleres, and Luigi Sauro. 2011. Robust and scalable Linked Data reasoning

incorporating provenance and trust annotations. _Journal of Web Semantics_ 9, 2 (2011), 165–201.

[59] Piero A. Bonatti and Sabrina Kirrane. 2019. Big Data and Analytics in the Age of the GDPR. In _2019 IEEE International_

_Congress on Big Data, BigData Congress 2019, Milan, Italy, July 8-13, 2019_, Elisa Bertino, Carl K. Chang, Peter Chen,

Ernesto Damiani, Michael Goul, and Katsunori Oyama (Eds.). IEEE Computer Society, 7–16.


81


[60] Iovka Boneva, Jérémie Dusart, Daniel Fernández-Álvarez, and José Emilio Labra Gayo. 2019. Shape Designer for

[ShEx and SHACL constraints, See [505], 269–272. http://ceur-ws.org/Vol-2456](http://ceur-ws.org/Vol-2456)

[61] Iovka Boneva, Jose Emilio Labra Gayo, and Eric G. Prud’hommeaux. 2017. Semantics and Validation of Shapes

Schemas for RDF, See [113], 104–120.

[62] Angela Bonifati, Wim Martens, and Thomas Timm. 2017. An Analytical Study of Large SPARQL Query Logs.

_Proceedings of the VLDB Endowment_ 11, 2 (2017), 149–161.

[63] Antoine Bordes, Nicolas Usunier, Alberto García-Durán, Jason Weston, and Oksana Yakhnenko. 2013. Translating

[Embeddings for Modeling Multi-relational Data, See [79], 2787–2795. http://papers.nips.cc/book/advances-in-neural-](http://papers.nips.cc/book/advances-in-neural-information-processing-systems-26-2013)

[information-processing-systems-26-2013](http://papers.nips.cc/book/advances-in-neural-information-processing-systems-26-2013)

[64] Gerlof Bouma. 2009. Normalized (Pointwise) Mutual Information in Collocation Extraction. In _Von der Form zur_

_Bedeutung: Texte automatisch verarbeiten - From Form to Meaning: Processing Texts Automatically, Proceedings of the_

_Biennial GSCL Conference 2009_, Christian Chiarcos, Richard Eckart de Castilho, and Manfred Stede (Eds.). Gunter

Narr Verlag, 31–40.

[65] Jacqueline Bourdeau, Jim Hendler, Roger Nkambou, Ian Horrocks, and Ben Y. Zhao (Eds.). 2016. _Proceedings of the_

_25th International Conference on World Wide Web, WWW 2016, Montreal, Canada, April 11-15, 2016, Companion Volume_ .

ACM Press.

[66] Ronald J. Brachman. 1977. _A structural paradigm for representing knowledge_ . Ph.D. Dissertation. Harvard University.

[67] Ronald J. Brachman and Hector J. Levesque. 1986. The Knowledge Level of a KBMS. In _On Knowledge Base Management_

_Systems: Integrating Artificial Intelligence and Database Technologies, Book resulting from the Islamorada Workshop 1985_

_(Islamorada, FL, USA) (Topics in Information Systems)_, Michael L. Brodie and John Mylopoulos (Eds.). Springer, 9–12.

[68] Ronald J. Brachman and James G. Schmolze. 1985. An Overview of the KL-ONE Knowledge Representation System.

_Cognitive Science_ 9, 2 (1985), 171–216.

[69] Patricia Branum and Bethany Sehon. 2019. Knowledge Graph Pilot Improves Data Quality While Providing a Customer

360 View. In _Knowledge Graph Conference_ . (Invited talk).

[70] Dan Brickley and R. V. Guha. 2014. _RDF Schema 1.1, W3C Recommendation 25 February 2014_ . W3C Recommendation.

[World Wide Web Consortium. https://www.w3.org/TR/2014/REC-rdf-schema-20140225/](https://www.w3.org/TR/2014/REC-rdf-schema-20140225/)

[71] Joan Bruna, Wojciech Zaremba, Arthur Szlam, and Yann LeCun. 2014. Spectral Networks and Locally Connected

Networks on Graphs. In _2nd International Conference on Learning Representations, ICLR 2014, Banff, AB, Canada,_

_April 14-16, 2014, Conference Track Proceedings_, Yoshua Bengio and Yann LeCun (Eds.). OpenReview.net. [https:](https://openreview.net/group?id=ICLR.cc/2014)

[//openreview.net/group?id=ICLR.cc/2014](https://openreview.net/group?id=ICLR.cc/2014)

[72] Bruce G. Buchanan and Edward A. Feigenbaum. 1978. Dendral and Meta-Dendral: Their Applications Dimension.

_Artificial Intelligence_ 11, 1–2 (1978), 5–24.

[73] Lorenz Bühmann, Jens Lehmann, and Patrick Westphal. 2016. DL-Learner – A framework for inductive learning on

the Semantic Web. _Journal of Web Semantics_ [39 (2016), 15–24. https://doi.org/10.1016/j.websem.2016.06.001](https://doi.org/10.1016/j.websem.2016.06.001)

[74] Carlos Buil Aranda, Marcelo Arenas, Óscar Corcho, and Axel Polleres. 2013. Federating queries in SPARQL 1.1:

Syntax, semantics and evaluation. _Journal of Web Semantics_ 18, 1 (2013), 1–17.

[75] Carlos Buil-Aranda, Aidan Hogan, Jürgen Umbrich, and Pierre-Yves Vandenbussche. 2013. SPARQL Web-Querying

Infrastructure: Ready for Action?, See [9], 277–293.

[76] Paul Buitelaar, Philipp Cimiano, and Bernardo Magnini (Eds.). 2005. _Ontology learning from text: methods, evaluation_

_and applications_ . Frontiers in Artificial Intelligence and Applications, Vol. 123. IOS Press.

[77] Razvan C. Bunescu and Raymond J. Mooney. 2005. Subsequence Kernels for Relation Extraction. In _Advances in Neural_

_Information Processing Systems 18 [Neural Information Processing Systems, NIPS 2005, December 5-8, 2005, Vancouver,_

_British Columbia, Canada]_, Christopher J. C. Burges, Léon Bottou, Zoubin Ghahramani, and Kilian Q. Weinberger

[(Eds.). 171–178. http://papers.nips.cc/book/advances-in-neural-information-processing-systems-18-2005](http://papers.nips.cc/book/advances-in-neural-information-processing-systems-18-2005)

[78] Razvan C. Bunescu and Raymond J. Mooney. 2007. Learning to Extract Relations from the Web using Minimal

Supervision. In _ACL 2007, Proceedings of the 45th Annual Meeting of the Association for Computational Linguistics, June_

_23-30, 2007, Prague, Czech Republic_, John A. Carroll, Antal van den Bosch, and Annie Zaenen (Eds.). The Association

for Computational Linguistics, 576–583.

[79] Christopher J. C. Burges, Léon Bottou, Zoubin Ghahramani, and Kilian Q. Weinberger (Eds.). 2013. _Advances in Neural_

_Information Processing Systems 26: 27th Annual Conference on Neural Information Processing Systems 2013. Proceedings_

_of a meeting held December 5-8, 2013, Lake Tahoe, Nevada, United States_ [. http://papers.nips.cc/book/advances-in-](http://papers.nips.cc/book/advances-in-neural-information-processing-systems-26-2013)

[neural-information-processing-systems-26-2013](http://papers.nips.cc/book/advances-in-neural-information-processing-systems-26-2013)

[80] Elena Cabrio, Alessio Palmero Aprosio, and Serena Villata. 2014. These Are Your Rights - A Natural Language

Processing Approach to Automated RDF Licenses Generation, See [421], 255–269.

[81] Michael J. Cafarella, Alon Y. Halevy, Daisy Zhe Wang, Eugene Wu, and Yang Zhang. 2008. WebTables: exploring the

power of tables on the web. _Proceedings of the VLDB Endowment_ 1, 1 (2008), 538–549.


82


[82] Alison Callahan, Jose Cruz-Toledo, Peter Ansell, and Michel Dumontier. 2013. Bio2RDF Release 2: Improved Coverage,

Interoperability and Provenance of Life Science Linked Data, See [94], 200–212.

[83] Nicholas J. Car, Paul J. Box, and Ashley Sommer. 2019. The Location Index: A Semantic Web Spatial Data Infrastructure,

See [237], 543–557.

[84] Šejla Čebirić, François Goasdoué, Haridimos Kondylakis, Dimitris Kotzinos, Ioana Manolescu, Georgia Troullinou,

and Mussab Zneika. 2019. Summarizing semantic graphs: a survey. _The Very Large Data Base Journal_ 28, 3 (2019),

295–327.

[85] Stefano Ceri, Georg Gottlob, and Letizia Tanca. 1989. What you Always Wanted to Know About Datalog (And Never

Dared to Ask). _IEEE Transactions on Knowledge and Data Engineering_ 1, 1 (1989), 146–166.

[86] Pierre-Antoine Champin, Fabien L. Gandon, Mounia Lalmas, and Panagiotis G. Ipeirotis (Eds.). 2018. _Proceedings of_

_the 2018 World Wide Web Conference on World Wide Web, WWW 2018, Lyon, France, April 23-27, 2018_ . ACM Press.

[[87] Spencer Chang. 2018. Scaling Knowledge Access and Retrieval at Airbnb. AirBnB Medium Blog. https://medium.](https://medium.com/airbnb-engineering/scaling-knowledge-access-and-retrieval-at-airbnb-665b6ba21e95)

[com/airbnb-engineering/scaling-knowledge-access-and-retrieval-at-airbnb-665b6ba21e95.](https://medium.com/airbnb-engineering/scaling-knowledge-access-and-retrieval-at-airbnb-665b6ba21e95)

[88] Laura Chiticariu, Marina Danilevsky, Yunyao Li, Frederick Reiss, and Huaiyu Zhu. 2018. SystemT: Declarative Text

Understanding for Enterprise. In _Proceedings of the 2018 Conference of the North American Chapter of the Association_

_for Computational Linguistics: Human Language Technologies, NAACL-HLT 2018, New Orleans, Louisiana, USA, June_

_1-6, 2018, Volume 3 (Industry Papers)_, Srinivas Bangalore, Jennifer Chu-Carroll, and Yunyao Li (Eds.). The Association

for Computational Linguistics, 76–83.

[89] Laura Chiticariu, Yunyao Li, and Frederick R. Reiss. 2013. Rule-Based Information Extraction is Dead! Long Live

Rule-Based Information Extraction Systems!. In _Proceedings of the 2013 Conference on Empirical Methods in Natural_

_Language Processing, EMNLP 2013, 18-21 October 2013, Grand Hyatt Seattle, Seattle, Washington, USA, A meeting_

_of SIGDAT, a Special Interest Group of the ACL_ . The Association for Computational Linguistics, 827–832. [https:](https://www.aclweb.org/anthology/volumes/D13-1/)

[//www.aclweb.org/anthology/volumes/D13-1/](https://www.aclweb.org/anthology/volumes/D13-1/)

[90] Chin-Wan Chung, Andrei Z. Broder, Kyuseok Shim, and Torsten Suel (Eds.). 2014. _23rd International World Wide Web_

_Conference, WWW ’14, Seoul, Republic of Korea, April 7-11, 2014_ . ACM Press.

[91] Giovanni Luca Ciampaglia, Prashant Shiralkar, Luis M Rocha, Johan Bollen, Filippo Menczer, and Alessandro Flammini.

2015. Computational fact checking from knowledge networks. _PLOS One_ 10, 6 (2015), e0128193.

[92] CIDR 2015. _CIDR 2015, Seventh Biennial Conference on Innovative Data Systems Research, Asilomar, CA, USA, January_

_4-7, 2015, Online Proceedings_ . www.cidrdb.org.

[93] Philipp Cimiano. 2006. Ontology Learning from Text. In _Ontology Learning and Population from Text: Algorithms,_

_Evaluation and Applications_ . Springer, Chapter 3, 19–34.

[94] Philipp Cimiano, Óscar Corcho, Valentina Presutti, Laura Hollink, and Sebastian Rudolph (Eds.). 2013. _The Semantic_

_Web: Semantics and Big Data, 10th International Conference, ESWC 2013, Montpellier, France, May 26-30, 2013. Proceedings_ .

Lecture Notes in Computer Science, Vol. 7882. Springer.

[95] Michael Cochez, Petar Ristoski, Simone Paolo Ponzetto, and Heiko Paulheim. 2017. Biased Graph Walks for RDF

Graph Embeddings. In _Proceedings of the 7th International Conference on Web Intelligence, Mining and Semantics, WIMS_

_2017, Amantea, Italy, June 19-22, 2017_, Rajendra Akerkar, Alfredo Cuzzocrea, Jannong Cao, and Mohand-Said Hacid

(Eds.). ACM Press, Article 21, 12 pages.

[96] Michael Cochez, Petar Ristoski, Simone Paolo Ponzetto, and Heiko Paulheim. 2017. Global RDF Vector Space

Embeddings, See [113], 190–207.

[97] Diego Collarana, Mikhail Galkin, Christoph Lange, Irlán Grangel-González, Maria-Esther Vidal, and Sören Auer. 2016.

FuhSen: A Federated Hybrid Search Engine for Building a Knowledge Graph On-Demand (Short Paper), See [123],

752–761.

[98] Michael Collins and Yoram Singer. 1999. Unsupervised Models for Named Entity Classification. In _Joint SIGDAT_

_Conference on Empirical Methods in Natural Language Processing and Very Large Corpora, EMNLP 1999, College Park, MD,_

_USA, June 21-22, 1999_ [. The Association for Computational Linguistics, 11. https://www.aclweb.org/anthology/W99-](https://www.aclweb.org/anthology/W99-0613/)

[0613/](https://www.aclweb.org/anthology/W99-0613/)

[99] Dan Connolly. 2007. _Gleaning Resource Descriptions from Dialects of Languages (GRDDL), W3C Recommendation 11_

_September 2007_ [. W3C Recommendation. World Wide Web Consortium. https://www.w3.org/TR/2007/REC-grddl-](https://www.w3.org/TR/2007/REC-grddl-20070911/)

[20070911/](https://www.w3.org/TR/2007/REC-grddl-20070911/)

[100] Mariano P. Consens and Alberto O. Mendelzon. 1990. GraphLog: a Visual Formalism for Real Life Recursion. In

_Proceedings of the Ninth ACM SIGACT-SIGMOD-SIGART Symposium on Principles of Database Systems, April 2-4, 1990,_

_Nashville, Tennessee, USA_, Daniel J. Rosenkrantz and Yehoshua Sagiv (Eds.). ACM Press, 404–416.

[101] Olivier Corby and Catherine Faron-Zucker. 2010. The KGRAM Abstract Machine for Knowledge Graph Querying. In

_2010 IEEE/WIC/ACM International Conference on Web Intelligence, WI 2010, Toronto, Canada, August 31 - September 3,_

_2010, Main Conference Proceedings_, Jimmy Xiangji Huang, Irwin King, Vijay V. Raghavan, and Stefan Rueger (Eds.).

IEEE Computer Society, 338–341.


83


[102] Francesco Corcoglioniti, Marco Rospocher, and Alessio Palmero Aprosio. 2016. Frame-Based Ontology Population

with PIKES. _IEEE Transactions on Knowledge and Data Engineering_ 28, 12 (2016), 3261–3275.

[103] Julien Corman, Fernando Florenzano, Juan L. Reutter, and Ognjen Savkovic. 2019. Validating SHACL Constraints

[over a SPARQL Endpoint, See [185], 145–163. https://doi.org/10.1007/978-3-030-30793-6_9](https://doi.org/10.1007/978-3-030-30793-6_9)

[104] Julien Corman, Juan L. Reutter, and Ognjen Savković. 2018. Semantics and Validation of Recursive SHACL, See [542],

318–336.

[105] Luca Costabello, Serena Villata, Nicolas Delaforge, and Fabien Gandon. 2012. Linked Data Access Goes Mobile:

Context-Aware Authorization for Graph Stores. In _WWW2012 Workshop on Linked Data on the Web, Lyon, France, 16_

_April, 2012 (CEUR Workshop Proceedings)_, Christian Bizer, Tom Heath, Tim Berners-Lee, and Michael Hausenblas

[(Eds.), Vol. 937. Sun SITE Central Europe (CEUR), 8. http://ceur-ws.org/Vol-937/ldow2012-paper-05.pdf](http://ceur-ws.org/Vol-937/ldow2012-paper-05.pdf)

[106] Kino Coursey and Rada Mihalcea. 2009. Topic Identification Using Wikipedia Graph Centrality. In _Human Language_

_Technologies: Conference of the North American Chapter of the Association of Computational Linguistics, Proceedings,_

_May 31 - June 5, 2009, Boulder, Colorado, USA, Short Papers_ . The Association for Computational Linguistics, 117–120.

[107] Simon Cox, Chris Little, Jerry R. Hobbs, and Feng Pan. 2017. _Time Ontology in OWL, W3C Recommendation 19 October_

_2017_ . W3C Recommendation / OGC 16-071r2. World Wide Web Consortium and Open Geospatial Consortium.

[https://www.w3.org/TR/2017/REC-owl-time-20171019/](https://www.w3.org/TR/2017/REC-owl-time-20171019/)

[108] Eric Crestan and Patrick Pantel. 2011. Web-scale table census and classification. In _Proceedings of the Forth International_

_Conference on Web Search and Web Data Mining, WSDM 2011, Hong Kong, China, February 9-12, 2011_, Irwin King,

Wolfgang Nejdl, and Hang Li (Eds.). ACM Press, 545–554.

[109] Philippe Cudré-Mauroux, Jeff Heflin, Evren Sirin, Tania Tudorache, Jérôme Euzenat, Manfred Hauswirth,

Josiane Xavier Parreira, Jim Hendler, Guus Schreiber, Abraham Bernstein, and Eva Blomqvist (Eds.). 2012. _The_

_Semantic Web - ISWC 2012 - 11th International Semantic Web Conference, Boston, MA, USA, November 11-15, 2012,_

_Proceedings, Part I_ . Lecture Notes in Computer Science, Vol. 7649. Springer.

[110] Alfredo Cuzzocrea, James Allan, Norman W. Paton, Divesh Srivastava, Rakesh Agrawal, Andrei Z. Broder, Mohammed J.

Zaki, K. Selçuk Candan, Alexandros Labrinidis, Assaf Schuster, and Haixun Wang (Eds.). 2018. _Proceedings of the 27th_

_ACM International Conference on Information and Knowledge Management, CIKM 2018, Torino, Italy, October 22-26,_

_2018_ . ACM Press.

[111] Richard Cyganiak, David Wood, and Markus Lanthaler. 2014. _RDF 1.1 Concepts and Abstract Syntax, W3C Recommen-_

_dation 25 February 2014_ [. W3C Recommendation. World Wide Web Consortium. https://www.w3.org/TR/2014/REC-](https://www.w3.org/TR/2014/REC-rdf11-concepts-20140225/)

[rdf11-concepts-20140225/](https://www.w3.org/TR/2014/REC-rdf11-concepts-20140225/)

[[112] Jeff Dalgliesh. 2016. How the Enterprise Knowledge Graph Connects Oil and Gas Data Silos. Maana Blog. https:](https://www.maana.io/blog/enterprise-knowledge-graph-connects-oil-gas-data-silos/)

[//www.maana.io/blog/enterprise-knowledge-graph-connects-oil-gas-data-silos/.](https://www.maana.io/blog/enterprise-knowledge-graph-connects-oil-gas-data-silos/)

[113] Claudia d’Amato, Miriam Fernández, Valentina A. M. Tamma, Freddy Lécué, Philippe Cudré-Mauroux, Juan F.

Sequeda, Christoph Lange, and Jeff Heflin (Eds.). 2017. _The Semantic Web - ISWC 2017 - 16th International Semantic_

_Web Conference, Vienna, Austria, October 21-25, 2017, Proceedings, Part I_ . Lecture Notes in Computer Science, Vol. 10587.

Springer.

[114] Claudia d’Amato, Steffen Staab, Andrea G. B. Tettamanzi, Duc Minh Tran, and Fabien L. Gandon. 2016. Ontology

enrichment by discovering multi-relational association rules from ontological knowledge bases. In _Proceedings of the_

_31st Annual ACM Symposium on Applied Computing, Pisa, Italy, April 4-8, 2016_, Sascha Ossowski (Ed.). ACM Press,

333–338.

[115] Claudia d’Amato, Andrea G. B. Tettamanzi, and Minh Duc Tran. 2016. Evolutionary Discovery of Multi-relational

Association Rules from Ontological Knowledge Bases, See [49], 113–128.

[116] Fariz Darari, Werner Nutt, Giuseppe Pirrò, and Simon Razniewski. 2018. Completeness Management for RDF Data

Sources. _ACM Transactions on the Web_ 12, 3 (2018), 18:1–18:53.

[117] Gautam Das, Christopher M. Jermaine, and Philip A. Bernstein (Eds.). 2018. _Proceedings of the 2018 International_

_Conference on Management of Data, SIGMOD Conference 2018, Houston, TX, USA, June 10-15, 2018_ . ACM Press.

[118] Souripriya Das, Seema Sundara, and Richard Cyganiak. 2012. _R2RML: RDB to RDF Mapping Language, W3C Recommen-_

_dation 27 September 2012_ [. W3C Recommendation. World Wide Web Consortium. https://www.w3.org/TR/2012/REC-](https://www.w3.org/TR/2012/REC-r2rml-20120927/)

[r2rml-20120927/](https://www.w3.org/TR/2012/REC-r2rml-20120927/)

[119] Ankur Dave, Alekh Jindal, Li Erran Li, Reynold Xin, Joseph Gonzalez, and Matei Zaharia. 2016. GraphFrames: an

integrated API for mixing graph and relational queries. In _Proceedings of the Fourth International Workshop on Graph_

_Data Management Experiences and Systems, Redwood Shores, CA, USA, June 24 - 24, 2016_, Peter A. Boncz and Josep-Lluís

Larriba-Pey (Eds.). ACM Press, 2.

[120] Gerard de Melo. 2015. Lexvo.org: Language-Related Information for the Linguistic Linked Data Cloud. _Semantic Web_

_Journal_ 6, 4 (7 Aug. 2015), 393–400.

[121] Luc De Raedt, Bart Vandersmissen, Marc Denecker, and Maurice Bruynooghe. 1990. A hybrid approach to learning

and its knowledge representation. In _Proceedings of the third COGNITIVA symposium on At the crossroads of artificial_


84


_intelligence, cognitive science, and neuroscience_ . Elsevier, 409–416.

[122] Marina De Vos, Sabrina Kirrane, Julian Padget, and Ken Satoh. 2019. ODRL policy modelling and compliance checking.

In _Rules and Reasoning - Third International Joint Conference, RuleML+RR 2019, Bolzano, Italy, September 16-19, 2019,_

_Proceedings (Lecture Notes in Computer Science)_, Paul Fodor, Marco Montali, Diego Calvanese, and Dumitru Roman

(Eds.), Vol. 11784. Springer, 36–51.

[123] Christophe Debruyne, Hervé Panetto, Robert Meersman, Tharam S. Dillon, eva Kühn, Declan O’Sullivan, and Clau
dio Agostino Ardagna (Eds.). 2016. _On the Move to Meaningful Internet Systems: OTM 2016 Conferences - Confederated_

_International Conferences: CoopIS, C&TC, and ODBASE 2016, Rhodes, Greece, October 24-28, 2016, Proceedings_ . Lecture

Notes in Computer Science, Vol. 10033. Springer.

[124] Remy Delanaux, Angela Bonifati, Marie-Christine Rousset, and Romuald Thion. 2018. Query-Based Linked Data

Anonymization, See [542], 530–546.

[125] Thomas Demeester, Tim Rocktäschel, and Sebastian Riedel. 2016. Lifted Rule Injection for Relation Embeddings, See

[504], 1389–1399.

[126] Dong Deng, Yu Jiang, Guoliang Li, Jian Li, and Cong Yu. 2013. Scalable Column Concept Determination for Web

Tables Using Large Knowledge Bases. _Proceedings of the VLDB Endowment_ 6, 13 (2013), 1606–1617.

[127] Tim Dettmers, Pasquale Minervini, Pontus Stenetorp, and Sebastian Riedel. 2018. Convolutional 2D Knowledge

Graph Embeddings, See [346], 1811–1818.

[[128] Deepika Devarajan. 2017. Happy Birthday Watson Discovery. IBM Cloud Blog. https://www.ibm.com/blogs/bluemix/](https://www.ibm.com/blogs/bluemix/2017/12/happy-birthday-watson-discovery/)

[2017/12/happy-birthday-watson-discovery/.](https://www.ibm.com/blogs/bluemix/2017/12/happy-birthday-watson-discovery/)

[129] Rose Dieng, Alain Giboin, Paul-André Tourtier, and Olivier Corby. 1992. Knowledge Acquisition for Explainable,

Multi-Expert, Knowledge-Based Design Systems. In _Current Developments in Knowledge Acquisition - EKAW’92, 6th_

_European Knowledge Acquisition Workshop, Heidelberg and Kaiserslautern, Germany, May 18-22, 1992 (Lecture Notes in_

_Computer Science)_, Thomas Wetter, Klaus-Dieter Althoff, John H. Boose, Brian R. Gaines, and Marc Linster (Eds.),

Vol. 599. Springer, 298–317.

[130] Renata Queiroz Dividino, Sergej Sizov, Steffen Staab, and Bernhard Schueler. 2009. Querying for provenance,

trust, uncertainty and other meta knowledge in RDF. _Journal of Web Semantics_ 7, 3 (2009), 204–219. [https:](https://doi.org/10.1016/j.websem.2009.07.004)

[//doi.org/10.1016/j.websem.2009.07.004](https://doi.org/10.1016/j.websem.2009.07.004)

[131] Xin Dong, Evgeniy Gabrilovich, Geremy Heitz, Wilko Horn, Ni Lao, Kevin Murphy, Thomas Strohmann, Shaohua

Sun, and Wei Zhang. 2014. Knowledge vault: a web-scale approach to probabilistic knowledge fusion. In _The 20th_

_ACM SIGKDD International Conference on Knowledge Discovery and Data Mining, KDD ’14, New York, NY, USA - August_

_24 - 27, 2014_, Sofus A. Macskassy, Claudia Perlich, Jure Leskovec, Wei Wang, and Rayid Ghani (Eds.). ACM Press,

601–610.

[132] Xin Luna Dong. 2019. Building a Broad Knowledge Graph for Products, See [262], 25–25.

[133] Uwe Draisbach and Felix Naumann. 2011. A generalization of blocking and windowing algorithms for duplicate

detection. In _2011 International Conference on Data and Knowledge Engineering, ICDKE 2011, Milano, Italy, September 6,_

_2011_, Ji Zhang and Giovanni Livraga (Eds.). IEEE Computer Society, 18–24.

[134] Martin Dürst and Michel Suignard. 2005. _Internationalized Resource Identifiers (IRIs)_ . RFC 3987. Internet Engineering

[Task Force. http://www.ietf.org/rfc/rfc3987.txt](http://www.ietf.org/rfc/rfc3987.txt)

[135] Arnab Dutta, Christian Meilicke, and Heiner Stuckenschmidt. 2014. Semantifying Triples from Open Information

Extraction Systems. In _STAIRS 2014 - Proceedings of the 7th European Starting AI Researcher Symposium, Prague, Czech_

_Republic, August 18-22, 2014 (Frontiers in Artificial Intelligence and Applications)_, Ulle Endriss and João Leite (Eds.),

Vol. 264. IOS Press, 111–120.

[136] Arnab Dutta, Christian Meilicke, and Heiner Stuckenschmidt. 2015. Enriching Structured Knowledge with Open

Information, See [174], 267–277.

[137] Cynthia Dwork. 2006. Differential Privacy. In _Automata, Languages and Programming, 33rd International Colloquium,_

_ICALP 2006, Venice, Italy, July 10-14, 2006, Proceedings, Part II (Lecture Notes in Computer Science)_, Michele Bugliesi,

Bart Preneel, Vladimiro Sassone, and Ingo Wegener (Eds.), Vol. 4052. Springer, 1–12.

[138] Eugene Dynkin. 1965. _Markov processes_ . Springer.

[139] Julian Eberius, Katrin Braunschweig, Markus Hentsch, Maik Thiele, Ahmad Ahmadov, and Wolfgang Lehner. 2015.

Building the Dresden Web Table Corpus: A Classification Approach. In _2nd IEEE/ACM International Symposium on Big_

_Data Computing, BDC 2015, Limassol, Cyprus, December 7-10, 2015_, Ioan Raicu, Omer F. Rana, and Rajkumar Buyya

(Eds.). IEEE Computer Society, 41–50.

[140] Mikel Egaña, Alan Rector, Robert Stevens, and Erick Antezana. 2008. Applying Ontology Design Patterns in Bio
ontologies. In _Knowledge Engineering: Practice and Patterns, 16th International Conference, EKAW 2008, Acitrezza, Italy,_

_September 29 - October 2, 2008. Proceedings (Lecture Notes in Computer Science)_, Aldo Gangemi and Jérôme Euzenat

(Eds.), Vol. 5268. Springer, 7–16.


85


[141] Lisa Ehrlinger and Wolfram Wöß. 2016. Towards a Definition of Knowledge Graphs. In _Joint Proceedings of the Posters_

_and Demos Track of the 12th International Conference on Semantic Systems - SEMANTiCS2016 and the 1st International_

_Workshop on Semantic Change & Evolving Semantics (SuCCESS’16) co-located with the 12th International Conference on_

_Semantic Systems (SEMANTiCS 2016), Leipzig, Germany, September 12-15, 2016 (CEUR Workshop Proceedings)_, Michael

[Martin, Martí Cuquet, and Erwin Folmer (Eds.), Vol. 1695. Sun SITE Central Europe (CEUR), 4. http://ceur-ws.org/Vol-](http://ceur-ws.org/Vol-1695/paper4.pdf)

[1695/paper4.pdf](http://ceur-ws.org/Vol-1695/paper4.pdf)

[142] Shady Elbassuoni, Maya Ramanath, Ralf Schenkel, Marcin Sydow, and Gerhard Weikum. 2009. Language-model
based ranking for queries on RDF-graphs. In _Proceedings of the 18th ACM Conference on Information and Knowledge_

_Management, CIKM 2009, Hong Kong, China, November 2-6, 2009_, David Wai-Lok Cheung, Il-Yeol Song, Wesley W.

Chu, Xiaohua Hu, and Jimmy J. Lin (Eds.). ACM Press, 977–986.

[143] Basil Ell, Andreas Harth, and Elena Simperl. 2014. SPARQL Query Verbalization for Explaining Semantic Search

Engine Queries, See [421], 426–441.

[144] Orri Erling. 2012. Virtuoso, a Hybrid RDBMS/Graph Column Store. _IEEE Data Engineering Bulletin_ 35, 1 (2012), 3–8.

[145] Ivan Ermilov and Axel-Cyrille Ngonga Ngomo. 2016. TAIPAN: Automatic Property Mapping for Tabular Data, See

[49], 163–179.

[146] Diego Esteves, Anisa Rula, Aniketh Janardhan Reddy, and Jens Lehmann. 2018. Toward Veracity Assessment in

RDF Knowledge Bases: An Exploratory Analysis. _Journal of Data and Information Quality_ 9, 3 (2018), 16:1–16:26.

[https://doi.org/10.1145/3177873](https://doi.org/10.1145/3177873)

[147] Ernesto Estrada. 2011. _The Structure of Complex Networks: Theory and Applications_ . Oxford University Press, Inc.

[148] Oren Etzioni, Michael J. Cafarella, Doug Downey, Stanley Kok, Ana-Maria Popescu, Tal Shaked, Stephen Soderland,

Daniel S. Weld, and Alexander Yates. 2004. Web-scale information extraction in knowitall: (preliminary results). In

_Proceedings of the 13th international conference on World Wide Web, WWW 2004, New York, NY, USA, May 17-20, 2004_,

Stuart I. Feldman, Mike Uretsky, Marc Najork, and Craig E. Wills (Eds.). ACM Press, 100–110.

[149] Oren Etzioni, Anthony Fader, Janara Christensen, Stephen Soderland, and Mausam. 2011. Open Information Extraction:

The Second Generation, See [547], 3–10.

[150] Anthony Fader, Stephen Soderland, and Oren Etzioni. 2011. Identifying Relations for Open Information Extraction.

In _Proceedings of the 2011 Conference on Empirical Methods in Natural Language Processing, EMNLP 2011, 27-31 July_

_2011, John McIntyre Conference Centre, Edinburgh, UK, A meeting of SIGDAT, a Special Interest Group of the ACL_ . The

[Association for Computational Linguistics, 1535–1545. https://www.aclweb.org/anthology/volumes/D11-1/](https://www.aclweb.org/anthology/volumes/D11-1/)

[151] Wenfei Fan, Xin Wang, and Yinghui Wu. 2013. Diversified Top- _𝑘_ Graph Pattern Matching. _Proceedings of the VLDB_

_Endowment_ 6, 13 (2013), 1510–1521.

[152] Michael Färber. 2019. The Microsoft Academic Knowledge Graph: A Linked Data Source with 8 Billion Triples of

Scholarly Data, See [186], 113–129.

[153] Michael Färber, Frederic Bartscherer, Carsten Menne, and Achim Rettinger. 2018. Linked data quality of DBpedia,

Freebase, OpenCyc, Wikidata, and YAGO. _Semantic Web Journal_ 9, 1 (2018), 77–129.

[154] Dieter Fensel, Umutcan Simsek, Kevin Angele, Elwin Huaman, Elias Kärle, Oleksandra Panasiuk, Ioan Toma, Jürgen

Umbrich, and Alexander Wahler. 2020. _Knowledge Graphs - Methodology, Tools and Selected Use Cases_ . Springer.

[https://doi.org/10.1007/978-3-030-37439-6](https://doi.org/10.1007/978-3-030-37439-6)

[155] Javier D. Fernández, Sabrina Kirrane, Axel Polleres, and Simon Steyskal. 2017. Self-Enforcing Access Control for

Encrypted RDF, See [51], 607–622.

[156] Javier D. Fernández, Miguel A. Martínez-Prieto, Claudio Gutiérrez, Axel Polleres, and Mario Arias. 2013. Binary RDF

representation for publication and exchange (HDT). _Journal of Web Semantics_ 19 (2013), 22–41.

[157] Mariano Fernández, Asuncón Gómez-Pérez, and Natalia Juristo. 1997. METHONTOLOGY: from Ontological Art

towards Ontological Engineering. In _Proceedings of the AAAI97 Spring Symposium Series on Ontological Engineering_ .

[158] Emilio Ferrara, Pasquale De Meo, Giacomo Fiumara, and Robert Baumgartner. 2014. Web data extraction, applications

and techniques: A survey. _Knowledge-based Systems_ 70 (2014), 301–323.

[159] Charles J. Fillmore. 1976. Frame semantics and the nature of language. _Annals of the New York Academy of Sciences_

280, 1 (1976), 20–32.

[160] Jenny Rose Finkel, Trond Grenager, and Christopher D. Manning. 2005. Incorporating Non-local Information into

Information Extraction Systems by Gibbs Sampling, See [294], 363–370.

[161] Sergio Flesca, Giuseppe Manco, Elio Masciari, Eugenio Rende, and Andrea Tagarelli. 2004. Web wrapper induction: a

brief survey. _AI Communications_ 17, 2 (2004), 57–61.

[162] Giorgos Flouris, Irini Fundulaki, Maria Michou, and Grigoris Antoniou. 2010. Controlling Access to RDF Graphs.

In _Future Internet - FIS 2010 - Third Future Internet Symposium, Berlin, Germany, September 20-22, 2010. Proceedings_
