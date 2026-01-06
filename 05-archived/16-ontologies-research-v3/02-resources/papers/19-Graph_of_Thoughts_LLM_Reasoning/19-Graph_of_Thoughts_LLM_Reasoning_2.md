<!-- Source: 19-Graph_of_Thoughts_LLM_Reasoning.pdf | Chunk 2/7 -->


4.8
4.5
4.2
3.9
3.6
3.3
3.0
2.7
2.4
2.1
1.8
1.5
1.2
0.9
0.6
0.3
0.0















0
IO CoT ToT ToT2 **GoT**



1.6


1.4


1.2


1.0


0.8


0.6


0.4


0.2


0.0



Figure 5: Number of errors and cost in sorting tasks with ChatGPT-3.5. _L_ and _k_ indicate the structure of ToT (see Sections 3.2
and 6).



**Used LLMs** Due to budget restrictions, we focus on GPT3.5. We also experimented with Llama-2, but it was usually
worse than GPT-3.5 and also much slower to run, making it
infeasible to obtain enough samples.


**7.2** **Analysis of GoT’s Advantages**


The results of the analysis are in Figure 5 (sorting), 6 (set
intersection), 7 (keyword counting), and 8 (document merging); see Section 5 for the description of specific use cases.
_Overall, GoT improves the quality of outcomes over all the_
_considered baselines and it reduces inference costs com-_
_pared to ToT_ .
**GoT vs. ToT** GoT improves upon ToT and ToT2 by a
large margin over all the considered problem instances. ToT
usually comes with somewhat higher quality than ToT2, but
simultaneously much higher costs. GoT’s costs are always
lower than ToT, and comparable (in some cases lower, in
others higher) to ToT2. For example, it reduces median error by _≈_ 62%, thereby achieving a higher quality of sorting,
for _P_ = 128 in comparison to ToT while ensuring _>_ 31%
cost reductions. These advantages are due to GoT’s ability to
decompose complex tasks into simpler subtasks, solve these
subtasks independently, and then incrementally merge these
outcomes into the final result.
**GoT vs. IO and CoT** GoT consistently delivers much
higher quality of outcomes than IO/CoT. For example, for
sorting ( _P_ = 64), GoT’s median error is _≈_ 65% and _≈_ 83%
lower than, respectively, CoT and IO. Yet, the costs of GoT

- and ToT – are much higher than in IO and CoT. This is
mostly due to our configuration of CoT, where we do not artificially inflate the lengths of the chains of reasoning if this
does not improve the outcomes. The higher costs of GoT and
ToT are driven by _k_ new thoughts built for each Generate
operation; these multiple thoughts are one of the reasons for
GoT’s superiority in quality.
**Increasing Complexity of Tackled Problems** Most importantly, the advantages of GoT in the quality _increase for_
_all the baselines with the growing size of the problem P_ . For



example, in sorting, while for _P_ = 32 GoT only negligibly
improves upon ToT2, its median error count becomes lower
by _≈_ 61% for _P_ = 64 and _≈_ 69% for _P_ = 128. The quartiles also become respectively better. The results for other
schemes also follow the intuition; for example, IO becomes
consistently worse with the increasing _P_, which is expected
as a single thought is unlikely to solve a large problem instance. _Overall, this analysis illustrates that GoT is indeed_
_well-suited for elaborate problem cases_, as the execution
schedules usually become more complex with the growing
problem sizes.


**7.3** **Discussion on Task Decomposition**


When splitting a task into subtasks and then solving these
subtasks, the size of responses and the input (in tokens) are
reduced proportionally to the degree of the task decomposition. However, the “static” part of the prompt (i.e., few-shot
examples) may become a significant overhead (see GoT4 to
GoT8 in Figure 7). Here, we observe that these few-shot examples can usually also be reduced in size (e.g., the passages
used to demonstrate keyword counting can also be made
smaller and still be indicative of the actual input size), thus
actively working towards decreasing the cost (e.g., see the
difference between GoT8 and GoTx in Figure 7).
The overall goal when conducting graph decomposition is
to break down a task to the point, where the LLM can solve
it correctly for the majority of time using a single prompt
(or with a few additional improvement steps). This significantly lowers the number of improvement/refinement steps
needed during the later stages of the graph exploration. Furthermore, as indicated by our results, combining or concatenating subresults is usually an easier task than solving large
task instances from scratch. Hence, the LLM is often successful when aggregating the final solution.


**8** **Related Work**


We summarize relations between GoT and related work.



8


**128 elements**



Solved
correctly:


18


16


14


12


10


8


6


4


2



**32 elements**



32



12


8


4


0
IO CoT ToT ToT2 **GoT**



GoT: Appendix 1.8 GoT: Appendix GoT: Appendix



88


80


72


64


56


48


40


32


24


16



8


0
IO CoT ToT ToT2 **GoT**





28


24


20









L=3k=10 1.0 16 48 L=9k=10



16



4.8


4.2


3.6


3.0


2.4


1.8


1.2


0.6


0.0



11


10


9


8


7


6


5


4


3


2


1


0



0
IO CoT ToT ToT2 **GoT**



1.8


1.6


1.4


1.2


1.0


0.8


0.6


0.4


0.2


0.0



Figure 6: Number of errors and cost in set intersection tasks with ChatGPT-3.5. _L_ and _k_ indicate the structure of ToT (see
Sections 3.2 and 6).



Samples solved
correctly



15


12


9


6


3


0



35


30


25


20


15


10


5





0
IO CoT ToT **GoT** **GoT2**









8


7


6


5


4


3


2


1


0



8


6


4


2





0
IO CoT ToT ToT2 **GoT4 GoT8 GoTx**



Figure 7: Number of errors and cost in keyword counting
with ChatGPT-3.5. _L_ and _k_ indicate the structure of ToT (see
Sections 3.2 and 6).


**8.1** **Prompting Paradigms & Approaches**


We detail different prompting paradigms in Section 1 and
Table 1. There are numerous other works related to prompting. We now briefly summarize selected most related ones;
more extensive descriptions can be found in dedicated surveys [34, 40, 69, 70]. Wang et al. proposed Plan-andSolve, an approach to enhance CoT with an explicit planning stage [66]. Using complexity-based criteria to enhance
prompting within a CoT was designed by Fu et al. [29, 67].
The self-taught reasoner (STaR) [80] generates several chain
of thoughts, and selects the ones that are valid. Similarly, a
scheme by Shum et al. [61] generates a pool of CoT candidates, and selects the best candidate based on whether the
candidates match the ground truth and on a policy gradientbased method. Automatic prompt generation overcomes the



Figure 8: Score and cost in document merging with
ChatGPT-3.5. _L_ and _k_ indicate the structure of ToT (see Sections 3.2 and 6). Number of samples: 50; context size: 16k
tokens.


issues of scaling in CoT [41, 42, 59]. Zhou et al. propose to harness selecting the best prompt out of a candidate
set [84]. Skeleon-of-Thought [47] generates at first a number of skeleton answers (brief bullet points of 3 to 5 words)
and expands on these points in parallel in a second step.
Finally, in prompt chaining, one cascades different LLMs.
This enables prompting different LLMs via different contexts, enabling more powerful reasoning [21, 23, 48, 51, 72,
73, 73]. GoT is orthogonal to this class of schemes, as it
focuses on a single context capabilities.


**8.2** **Self-Reflection & Self-Evaluation**

Self-reflection and self-evaluation were introduced recently [45, 49, 60, 75, 85]. They are used to enhance different tasks, for example for code generation [17] or com


9


puter operation tasks [39]. In GoT, we partially rely on
self-evaluation when taking decisions on how to expand the
graph of thoughts within a prompt.


**8.3** **LLMs & Planning**


There are many works recently on how to plan complex
tasks with LLMs [36, 37, 68, 76, 78, 81]. GoT could be seen
as a generic framework that could potentially be used to enhance such schemes, by offering a paradigm for generating
complex graph-based plans.


**8.4** **Graphs and Graph Computing**


Graphs have become an immensely popular and important
part of the general computing landscape [31, 32, 44, 46, 56].
Recently, there has been a growing interest in domains
such as graph databases [2–4, 7, 55], graph pattern matching [8, 10, 11, 18, 25, 62], graph streaming [1, 22, 26],
and graph machine learning as well as graph neural networks [5, 6, 12, 16, 30, 33, 33, 57, 74, 82, 83]. The graph
abstraction has been fruitful for many modern research domains, such as social sciences (e.g., studying human interactions), bioinformatics (e.g., analyzing protein structures),
chemistry (e.g., designing chemical compounds), medicine
(e.g., drug discovery), cybersecurity (e.g., identifying intruder machines), healthcare (e.g., exposing groups of people who submit fraudulent claims), web graph analysis (e.g.,
providing accurate search services), entertainment services
(e.g., predicting movie popularity), linguistics (e.g., modeling relationships between words), transportation (e.g., finding efficient routes), physics (e.g., understanding phase transitions and critical phenomena), and many others [15, 20,
35, 38, 44]. In this work, we harness the graph abstraction
as a key mechanism that enhances prompting capabilities in
LLMs.


**9** **Conclusion**


Prompt engineering is one of the central new domains of
the large language model (LLM) research. It enables using
LLMs efficiently, without any model updates. However, designing effective prompts is a challenging task.
In this work, we propose Graph of Thoughts (GoT), a new
paradigm that enables the LLM to solve different tasks effectively without any model updates. The key idea is to model
the LLM reasoning as an arbitrary graph, where thoughts
are vertices and dependencies between thoughts are edges.
This enables novel transformations of thoughts, such as aggregation. Human’s task solving is often non-linear, and it
involves combining intermediate solutions into final ones,
or changing the flow of reasoning upon discovering new insights. GoT reflects this with its graph structure.
GoT outperforms other prompting schemes, for example
ensuring 62% increase in the quality of sorting over ToT,
while simultaneously reducing costs by _>_ 31%. We also propose a novel metric for a prompting scheme, the volume of
a thought, to indicate the scope of information that a given
LLM output could carry with it, where GoT also excels. This
provides a step towards more principled prompt engineering.



The graph abstraction has been the foundation of several
successful designs in computing and AI over last decades,
for example AlphaFold for protein predictions. Our work
harnesses it within the realm of prompt engineering.


**Acknowledgements**
We thank Hussein Harake, Colin McMurtrie, Mark Klein, Angelo Mangili, and the whole CSCS team granting access to the
Ault and Daint machines, and for their excellent technical support. We thank Timo Schneider for help with infrastructure at
SPCL. This project received funding from the European Research Council (Project PSAP, No. 101002047), and the European
High-Performance Computing Joint Undertaking (JU) under grant
agreement No. 955513 (MAELSTROM). This project was supported by the ETH Future Computing Laboratory (EFCL), financed
by a donation from Huawei Technologies. This project received
funding from the European Union’s HE research and innovation
programme under the grant agreement No. 101070141 (Project
GLACIATION).


**References**

[1] Besta, M.; Fischer, M.; Kalavri, V.; Kapralov, M.; and
Hoefler, T. 2023. Practice of Streaming Processing
of Dynamic Graphs: Concepts, Models, and Systems.
_IEEE Transactions on Parallel and Distributed Sys-_
_tems_, 34(6): 1860–1876.

[2] Besta, M.; Gerstenberger, R.; Blach, N.; Fischer, M.;
and Hoefler, T. 2023. GDI: A Graph Database Interface Standard. https://github.com/spcl/GDI-RMA. Accessed: 2023-09-05.

[3] Besta, M.; Gerstenberger, R.; Fischer, M.; Podstawski,
M.; Blach, N.; Egeli, B.; Mitenkov, G.; Chlapek, W.;
Michalewicz, M.; Niewiadomski, H.; M¨uller, J.; and
Hoefler, T. 2023. The Graph Database Interface: Scaling Online Transactional and Analytical Graph Workloads to Hundreds of Thousands of Cores. In _Proceed-_
_ings of the International Conference for High Perfor-_
_mance Computing, Networking, Storage and Analysis_,
SC ’23. ACM.

[4] Besta, M.; Gerstenberger, R.; Peter, E.; Fischer, M.;
Podstawski, M.; Barthels, C.; Alonso, G.; and Hoefler,
T. 2023. Demystifying Graph Databases: Analysis and
Taxonomy of Data Organization, System Designs, and
Graph Queries. _ACM Comput. Surv._, 56(2).

[5] Besta, M.; Grob, R.; Miglioli, C.; Bernold, N.;
Kwa´sniewski, G.; Gjini, G.; Kanakagiri, R.; Ashkboos,
S.; Gianinazzi, L.; Dryden, N.; and Hoefler, T. 2022.
Motif Prediction with Graph Neural Networks. In
_Proceedings of the 28th ACM SIGKDD Conference_
_on Knowledge Discovery and Data Mining_, KDD ’22,
35–45.

[6] Besta, M.; and Hoefler, T. 2022. Parallel and Distributed Graph Neural Networks: An In-Depth Concurrency Analysis. arXiv:2205.09702.

[7] Besta, M.; Iff, P.; Scheidl, F.; Osawa, K.; Dryden, N.;
Podstawski, M.; Chen, T.; and Hoefler, T. 2022. Neural
Graph Databases. In _Proceedings of the First Learning_
_on Graphs Conference_, volume 198 of _Proceedings of_
_Machine Learning Research_, 31:1–31:38. PMLR.



10


[8] Besta, M.; Kanakagiri, R.; Kwa´sniewski, G.;
Ausavarungnirun, R.; Ber´anek, J.; Kanellopoulos,
K.; Janda, K.; Vonarburg-Shmaria, Z.; Gianinazzi,
L.; Stefan, I.; Luna, J. G.; Golinowski, J.; Copik,
M.; Kapp-Schwoerer, L.; Di Girolamo, S.; Blach,
N.; Konieczny, M.; Mutlu, O.; and Hoefler, T. 2021.
SISA: Set-Centric Instruction Set Architecture for
Graph Mining on Processing-in-Memory Systems. In
_Proceedings of the 54th Annual IEEE/ACM Interna-_
_tional Symposium on Microarchitecture_, MICRO ’21,
282–297.

[9] Besta, M.; Kanakagiri, R.; Mustafa, H.; Karasikov,
M.; R¨atsch, G.; Hoefler, T.; and Solomonik, E. 2020.
Communication-Efficient Jaccard Similarity for HighPerformance Distributed Genome Comparisons. In
_Proceedings of the IEEE International Parallel and_
_Distributed Processing Symposium_, IPDPS ’20, 1122–
1132.

[10] Besta, M.; Miglioli, C.; Labini, P. S.; Tˇetek, J.; Iff, P.;
Kanakagiri, R.; Ashkboos, S.; Janda, K.; Podstawski,
M.; Kwa´sniewski, G.; Gleinig, N.; Vella, F.; Mutlu, O.;
and Hoefler, T. 2022. ProbGraph: High-Performance
and High-Accuracy Graph Mining with Probabilistic
Set Representations. In _Proceedings of the Interna-_
_tional Conference on High Performance Computing,_
_Networking, Storage and Analysis_, SC ’22. IEEE.

[11] Besta, M.; Vonarburg-Shmaria, Z.; Schaffner, Y.;
Schwarz, L.; Kwa´sniewski, G.; Gianinazzi, L.; Beranek, J.; Janda, K.; Holenstein, T.; Leisinger, S.;
Tatkowski, P.; Ozdemir, E.; Balla, A.; Copik, M.; Lindenberger, P.; Konieczny, M.; Mutlu, O.; and Hoefler, T. 2021. GraphMineSuite: Enabling HighPerformance and Programmable Graph Mining Algorithms with Set Algebra. _Proc. VLDB Endow._, 14(11):
1922–1935.

[12] Bronstein, M. M.; Bruna, J.; LeCun, Y.; Szlam, A.; and
Vandergheynst, P. 2017. Geometric Deep Learning:
Going beyond Euclidean data. _IEEE Signal Process-_
_ing Magazine_, 34(4): 18–42.

[13] Brown, T.; Mann, B.; Ryder, N.; Subbiah, M.; Kaplan, J. D.; Dhariwal, P.; Neelakantan, A.; Shyam,
P.; Sastry, G.; Askell, A.; Agarwal, S.; Herbert-Voss,
A.; Krueger, G.; Henighan, T.; Child, R.; Ramesh, A.;
Ziegler, D.; Wu, J.; Winter, C.; Hesse, C.; Chen, M.;
Sigler, E.; Litwin, M.; Gray, S.; Chess, B.; Clark, J.;
Berner, C.; McCandlish, S.; Radford, A.; Sutskever, I.;
and Amodei, D. 2020. Language Models are Few-Shot
Learners. In _Advances in Neural Information Process-_
_ing Systems (NeurIPS ’20)_, volume 33, 1877–1901.
Curran Associates.

[14] Bubeck, S.; Chandrasekaran, V.; Eldan, R.; Gehrke,
J.; Horvitz, E.; Kamar, E.; Lee, P.; Lee, Y. T.; Li,
Y.; Lundberg, S.; Nori, H.; Palangi, H.; Ribeiro,
M. T.; and Zhang, Y. 2023. Sparks of Artificial
General Intelligence: Early experiments with GPT-4.
arXiv:2303.12712.

[15] Chakrabarti, D.; and Faloutsos, C. 2006. Graph Min


ing: Laws, Generators, and Algorithms. _ACM Comput._
_Surv._, 38(1).

[16] Chami, I.; Abu-El-Haija, S.; Perozzi, B.; R´e, C.;
and Murphy, K. 2020. Machine Learning on
Graphs: A Model and Comprehensive Taxonomy.
arXiv:2005.03675.

[17] Chen, X.; Lin, M.; Sch¨arli, N.; and Zhou, D. 2023.
Teaching Large Language Models to Self-Debug.
arXiv:2304.05128.

[18] Cheng, J.; Yu, J. X.; Ding, B.; Philip, S. Y.; and Wang,
H. 2008. Fast Graph Pattern Matching. In _Proceedings_
_of the IEEE 24th International Conference on Data En-_
_gineering_, ICDE ’08, 913–922.

[19] Chowdhery, A.; Narang, S.; Devlin, J.; Bosma,
M.; Mishra, G.; Roberts, A.; Barham, P.; Chung,
H. W.; Sutton, C.; Gehrmann, S.; Schuh, P.; Shi, K.;
Tsvyashchenko, S.; Maynez, J.; Rao, A.; Barnes, P.;
Tay, Y.; Shazeer, N.; Prabhakaran, V.; Reif, E.; Du,
N.; Hutchinson, B.; Pope, R.; Bradbury, J.; Austin, J.;
Isard, M.; Gur-Ari, G.; Yin, P.; Duke, T.; Levskaya,
A.; Ghemawat, S.; Dev, S.; Michalewski, H.; Garcia,
X.; Misra, V.; Robinson, K.; Fedus, L.; Zhou, D.; Ippolito, D.; Luan, D.; Lim, H.; Zoph, B.; Spiridonov,
A.; Sepassi, R.; Dohan, D.; Agrawal, S.; Omernick,
M.; Dai, A. M.; Pillai, T. S.; Pellat, M.; Lewkowycz,
A.; Moreira, E.; Child, R.; Polozov, O.; Lee, K.; Zhou,
Z.; Wang, X.; Saeta, B.; Diaz, M.; Firat, O.; Catasta,
M.; Wei, J.; Meier-Hellstern, K.; Eck, D.; Dean, J.;
Petrov, S.; and Fiedel, N. 2022. PaLM: Scaling Language Modeling with Pathways. arXiv:2204.02311.

[20] Cook, D. J.; and Holder, L. B., eds. 2006. _Mining_
_Graph Data_ . John Wiley & Sons.

[21] Creswell, A.; Shanahan, M.; and Higgins, I. 2022.
Selection-Inference: Exploiting Large Language
Models for Interpretable Logical Reasoning.
arXiv:2205.09712.

[22] Dhulipala, L.; Blelloch, G. E.; and Shun, J. 2019. LowLatency Graph Streaming Using Compressed PurelyFunctional Trees. In _Proceedings of the 40th ACM_
_SIGPLAN Conference on Programming Language De-_
_sign and Implementation_, PLDI ’19, 918–934.

[23] Dohan, D.; Xu, W.; Lewkowycz, A.; Austin, J.; Bieber,
D.; Lopes, R. G.; Wu, Y.; Michalewski, H.; Saurous,
R. A.; Sohl-Dickstein, J.; Murphy, K.; and Sutton, C.
2022. Language Model Cascades. In _Beyond Bayes:_
_Paths Towards Universal Reasoning Systems_, Workshop at ICML ’22.

[24] Drori, I.; Zhang, S.; Shuttleworth, R.; Tang, L.; Lu, A.;
Ke, E.; Liu, K.; Chen, L.; Tran, S.; Cheng, N.; Wang,
R.; Singh, N.; Patti, T. L.; Lynch, J.; Shporer, A.;
Verma, N.; Wu, E.; and Strang, G. 2022. A neural network solves, explains, and generates university math
problems by program synthesis and few-shot learning
at human level. _Proceedings of the National Academy_
_of Sciences_, 119(32): e2123433119.

[25] Fan, W.; Li, J.; Ma, S.; Tang, N.; Wu, Y.; and Wu,
Y. 2010. Graph Pattern Matching: From Intractable



11


to Polynomial Time. _Proc. VLDB Endow._, 3(1–2):
264–275.

[26] Feng, G.; Meng, X.; and Ammar, K. 2015. DISTINGER: A distributed graph data structure for massive dynamic graph processing. In _Proccedings of the_
_IEEE International Conference on Big Data_, Big Data
’15, 1814–1822.

[27] Friggeri, A.; Chelius, G.; and Fleury, E. 2011. Triangles to Capture Social Cohesion. In _Proceedings of_
_the IEEE Third International Conference on Privacy,_
_Security, Risk and Trust and IEEE Third International_
_Conference on Social Computing_, PASSAT/SocialCom
’11, 258–265.

[28] Friston, K. 2008. Hierarchical Models in the Brain.
_PLOS Computational Biology_, 4(11): 1–24.

[29] Fu, Y.; Peng, H.; Sabharwal, A.; Clark, P.; and Khot,
T. 2022. Complexity-Based Prompting for Multi-Step
Reasoning. arXiv:2210.00720.

[30] Gianinazzi, L.; Fries, M.; Dryden, N.; Ben-Nun, T.;
Besta, M.; and Hoefler, T. 2021. Learning Combinatorial Node Labeling Algorithms. arXiv:2106.03594.

[31] Gregor, D.; and Lumsdaine, A. 2005. Lifting Sequential Graph Algorithms for Distributed-Memory Parallel
Computation. _SIGPLAN Not._, 40(10): 423–437.

[32] Gregor, D.; and Lumsdaine, A. 2005. The Parallel
BGL: A generic library for distributed graph computations. _Parallel Object-Oriented Scientific Computing_
_(POOSC)_ .

[33] Hamilton, W. L.; Ying, R.; and Leskovec, J. 2017. Representation Learning on Graphs: Methods and Applications. _Bulletin of the Technical Committee on Data_
_Engineering_, 40(3): 52–74.

[34] Hartmann, M.; and Sonntag, D. 2022. A survey on
improving NLP models with human explanations. In
_Proceedings of the First Workshop on Learning with_
_Natural Language Supervision_, 40–47. Association for
Computational Linguistics.

[35] Horv´ath, T.; G¨artner, T.; and Wrobel, S. 2004. Cyclic
Pattern Kernels for Predictive Graph Mining. In _Pro-_
_ceedings of the Tenth ACM SIGKDD International_
_Conference on Knowledge Discovery and Data Min-_
_ing_, KDD ’04, 158–167.

[36] Huang, W.; Abbeel, P.; Pathak, D.; and Mordatch, I.
2022. Language Models as Zero-Shot Planners: Extracting Actionable Knowledge for Embodied Agents.
In _Proceedings of the 39th International Conference_
_on Machine Learning_, volume 162 of _Proceedings of_
_Machine Learning Research_, 9118–9147. PMLR.

[37] Huang, W.; Xia, F.; Xiao, T.; Chan, H.; Liang, J.; Florence, P.; Zeng, A.; Tompson, J.; Mordatch, I.; Chebotar, Y.; Sermanet, P.; Brown, N.; Jackson, T.; Luu,
L.; Levine, S.; Hausman, K.; and Ichter, B. 2022. Inner Monologue: Embodied Reasoning through Planning with Language Models. arXiv:2207.05608.

[38] Jiang, C.; Coenen, F.; and Zito, M. 2013. A survey of
frequent subgraph mining algorithms. _The Knowledge_
_Engineering Review_, 28(1): 75–105.




[39] Kim, G.; Baldi, P.; and McAleer, S. 2023. Language
Models can Solve Computer Tasks. arXiv:2303.17491.

[40] Lertvittayakumjorn, P.; and Toni, F. 2021.
Explanation-Based Human Debugging of NLP
Models: A Survey. _Transactions of the Association for_
_Computational Linguistics_, 9: 1508–1528.

[41] Lester, B.; Al-Rfou, R.; and Constant, N. 2021. The
Power of Scale for Parameter-Efficient Prompt Tuning. In _Proceedings of the Conference on Empiri-_
_cal Methods in Natural Language Processing_, EMNLP
’21, 3045–3059. Association for Computational Linguistics.

[42] Li, X. L.; and Liang, P. 2021. Prefix-Tuning:
Optimizing Continuous Prompts for Generation.
arXiv:2101.00190.

[43] Long, J. 2023. Large Language Model Guided Treeof-Thought. arXiv:2305.08291.

[44] Lumsdaine, A.; Gregor, D.; Hendrickson, B.; and
Berry, J. 2007. Challenges in Parallel Graph Processing. _Parallel Processing Letters_, 17(1): 5–20.

[45] Madaan, A.; Tandon, N.; Gupta, P.; Hallinan, S.; Gao,
L.; Wiegreffe, S.; Alon, U.; Dziri, N.; Prabhumoye, S.;
Yang, Y.; Gupta, S.; Majumder, B. P.; Hermann, K.;
Welleck, S.; Yazdanbakhsh, A.; and Clark, P. 2023.
Self-Refine: Iterative Refinement with Self-Feedback.
arXiv:2303.17651.

[46] Malewicz, G.; Austern, M. H.; Bik, A. J.; Dehnert,
J. C.; Horn, I.; Leiser, N.; and Czajkowski, G. 2010.
Pregel: A System for Large-Scale Graph Processing. In
_Proceedings of the International Conference on Man-_
_agement of Data_, SIGMOD ’10, 135–146. ACM.

[47] Ning, X.; Lin, Z.; Zhou, Z.; Wang, Z.; Yang, H.; and
Wang, Y. 2023. Skeleton-of-Thought: Large Language
Models Can Do Parallel Decoding. arXiv:2307.15337.

[48] Nye, M.; Andreassen, A. J.; Gur-Ari, G.; Michalewski,
H.; Austin, J.; Bieber, D.; Dohan, D.; Lewkowycz, A.;
Bosma, M.; Luan, D.; Sutton, C.; and Odena, A. 2021.
Show Your Work: Scratchpads for Intermediate Computation with Language Models. arXiv:2112.00114.

[49] Paul, D.; Ismayilzada, M.; Peyrard, M.; Borges, B.;
Bosselut, A.; West, R.; and Faltings, B. 2023. REFINER: Reasoning Feedback on Intermediate Representations. arXiv:2304.01904.

[50] Prat-P´erez, A.; Dominguez-Sal, D.; Brunat, J. M.; and
Larriba-Pey, J.-L. 2012. Shaping Communities out
of Triangles. In _Proceedings of the 21st ACM Inter-_
_national Conference on Information and Knowledge_
_Management_, CIKM ’12, 1677–1681.

[51] Qiao, S.; Ou, Y.; Zhang, N.; Chen, X.; Yao, Y.; Deng,
S.; Tan, C.; Huang, F.; and Chen, H. 2023. Reasoning
with Language Model Prompting: A Survey. In _Pro-_
_ceedings of the 61st Annual Meeting of the Association_
_for Computational Linguistics_, ACL ’23, 5368–5393.
Association for Computational Linguistics.

[52] qrdlgit. 2023. graph-of-thoughts Repository. https:
//github.com/qrdlgit/graph-of-thoughts. Accessed:
2023-10-11.



12


[53] Radford, A.; Narasimhan, K.; Salimans, T.; and
Sutskever, I. 2018. Improving Language Understanding by Generative Pre-Training. https://openai.com/
research/language-unsupervised. Accessed: 2023-0906.

[54] Radford, A.; Wu, J.; Child, R.; Luan, D.; Amodei, D.;
and Sutskever, I. 2019. Language Models are Unsupervised Multitask Learners. https://openai.com/research/
better-language-models. Accessed: 2023-09-06.

[55] Robinson, I.; Webber, J.; and Eifrem, E. 2015. _Graph_
_Databases: New Opportunities for Connected Data_ .
O’Reilly Media, 2nd edition.

[56] Sakr, S.; Bonifati, A.; Voigt, H.; Iosup, A.; Ammar, K.;
Angles, R.; Aref, W.; Arenas, M.; Besta, M.; Boncz,
P. A.; Daudjee, K.; Valle, E. D.; Dumbrava, S.; Hartig, O.; Haslhofer, B.; Hegeman, T.; Hidders, J.; Hose,
K.; Iamnitchi, A.; Kalavri, V.; Kapp, H.; Martens, W.;
¨Ozsu, M. T.; Peukert, E.; Plantikow, S.; Ragab, M.; Ripeanu, M. R.; Salihoglu, S.; Schulz, C.; Selmer, P.; Sequeda, J. F.; Shinavier, J.; Sz´arnyas, G.; Tommasini,
R.; Tumeo, A.; Uta, A.; Varbanescu, A. L.; Wu, H.Y.; Yakovets, N.; Yan, D.; and Yoneki, E. 2021. The
Future is Big Graphs: A Community View on Graph
Processing Systems. _Commun. ACM_, 64(9): 62–71.

[57] Scarselli, F.; Gori, M.; Tsoi, A. C.; Hagenbuchner, M.;
and Monfardini, G. 2008. The Graph Neural Network
Model. _IEEE Transactions on Neural Networks_, 20(1):
61–80.

[58] Schaeffer, S. E. 2007. Graph clustering. _Computer_
_Science Review_, 1(1): 27–64.

[59] Shin, T.; Razeghi, Y.; Logan IV, R. L.; Wallace, E.;
and Singh, S. 2020. AutoPrompt: Eliciting Knowledge
from Language Models with Automatically Generated
Prompts. arXiv:2010.15980.

[60] Shinn, N.; Labash, B.; and Gopinath, A. 2023. Reflexion: Language Agents with Verbal Reinforcement
Learning. arXiv:2303.11366.

[61] Shum, K.; Diao, S.; and Zhang, T. 2023. Automatic
Prompt Augmentation and Selection with Chain-ofThought from Labeled Data. arXiv:2302.12822.

[62] Teixeira, C. H. C.; Fonseca, A. J.; Serafini, M.;
Siganos, G.; Zaki, M. J.; and Aboulnaga, A. 2015.
Arabesque: A System for Distributed Graph Mining.
In _Proceedings of the 25th Symposium on Operating_
_Systems Principles_, SOSP ’15, 425–440. ACM.

[63] Touvron, H.; Lavril, T.; Izacard, G.; Martinet, X.;
Lachaux, M.-A.; Lacroix, T.; Rozi`ere, B.; Goyal,
N.; Hambro, E.; Azhar, F.; Rodriguez, A.; Joulin,
A.; Grave, E.; and Lample, G. 2023. LLaMA:
Open and Efficient Foundation Language Models.
arXiv:2302.13971.

[64] Touvron, H.; Martin, L.; Stone, K.; Albert, P.; Almahairi, A.; Babaei, Y.; Bashlykov, N.; Batra, S.; Bhargava, P.; Bhosale, S.; Bikel, D.; Blecher, L.; Ferrer,
C. C.; Chen, M.; Cucurull, G.; Esiobu, D.; Fernandes,
J.; Fu, J.; Fu, W.; Fuller, B.; Gao, C.; Goswami, V.;
Goyal, N.; Hartshorn, A.; Hosseini, S.; Hou, R.; Inan,



H.; Kardas, M.; Kerkez, V.; Khabsa, M.; Kloumann,
I.; Korenev, A.; Koura, P. S.; Lachaux, M.-A.; Lavril,
T.; Lee, J.; Liskovich, D.; Lu, Y.; Mao, Y.; Martinet,
X.; Mihaylov, T.; Mishra, P.; Molybog, I.; Nie, Y.;
Poulton, A.; Reizenstein, J.; Rungta, R.; Saladi, K.;
Schelten, A.; Silva, R.; Smith, E. M.; Subramanian,
R.; Tan, X. E.; Tang, B.; Taylor, R.; Williams, A.;
Kuan, J. X.; Xu, P.; Yan, Z.; Zarov, I.; Zhang, Y.; Fan,
A.; Kambadur, M.; Narang, S.; Rodriguez, A.; Stojnic, R.; Edunov, S.; and Scialom, T. 2023. Llama
2: Open Foundation and Fine-Tuned Chat Models.
arXiv:2307.09288.

[65] Vaswani, A.; Shazeer, N.; Parmar, N.; Uszkoreit, J.;
Jones, L.; Gomez, A. N.; Kaiser, Ł.; and Polosukhin, I.
2017. Attention is All you Need. In _Advances in Neu-_
_ral Information Processing Systems (NIPS ’17)_, volume 30. Curran Associates.

[66] Wang, L.; Xu, W.; Lan, Y.; Hu, Z.; Lan, Y.; Lee, R.
K.-W.; and Lim, E.-P. 2023. Plan-and-Solve Prompting: Improving Zero-Shot Chain-of-Thought Reasoning by Large Language Models. In _Proceedings of the_
_61st Annual Meeting of the Association for Computa-_
_tional Linguistics_, ACL ’23, 2609–2634. Association
for Computational Linguistics.

[67] Wang, X.; Wei, J.; Schuurmans, D.; Le, Q. V.; Chi,
E. H.; Narang, S.; Chowdhery, A.; and Zhou, D. 2023.
Self-Consistency Improves Chain of Thought Reasoning in Language Models. In _Proceedings of the_
_Eleventh International Conference on Learning Rep-_
_resentations_, ICLR ’23.
