<!-- Source: 15-AgentSurvey-2503.21460.pdf | Chunk 7/10 -->

datasets and single-turn tasks, fail to capture the complexities
of LLM agents in dynamic, multi-turn, and multi-agent
environments [310]. Current benchmarks primarily assess
task execution such as code completion [321], [322] and
dialogue generation [57] in isolated settings, overlooking
emergent agent behaviors, long-term adaptation, and collaborative reasoning that unfold across multi-turn interactions.
Additionally, static benchmarks struggle to keep pace with
evolving LLM capabilities [323]. Concerns persist regarding
potential data contamination, where model performance


may stem from memorization rather than genuine reasoning. Future research should focus on dynamic evaluation
methodologies, integrating multi-agent interaction scenarios,
structured performance metrics, and adaptive sample generation algorithms [324] to create more robust and reliable
assessment frameworks.


**6.5** **Regulatory Measures for Safe Deployment**


As agentic AI systems gain autonomy, regulatory frameworks
must evolve to ensure accountability, transparency, and safety.
A key challenge is mitigating algorithmic bias–agents may
inadvertently discriminate based on gender, age, ethnicity,
or other sensitive attributes, often in ways imperceptible
to developers [248], [325]. Addressing this requires standardized auditing protocols to systematically identify and
correct biases, alongside traceability mechanisms that log
decision-making pathways and model confidence for posthoc accountability. Future work can explore multidisciplinary
approaches combining fairness-aware training pipelines
with legal and ethical safeguards. Collaboration between
policymakers, researchers, and industry stakeholders will
be critical to ensuring AI-driven systems operate safely and
equitably in alignment with societal values [326].


**6.6** **Role-playing Scenarios**


LLM agents can simulate roles such as researchers, debators,
and instructors [307], [327], but their effectiveness is constrained by training data limitations and an incomplete understanding of human cognition [326], [328]. Since LLMs are
predominantly trained on web-based corpora, they struggle
to emulate roles with insufficient representation online [329]
and often produce conversations lacking diversity [268].
Future research should focus on enhancing role-play fidelity
by improving multi-agent coordination, incorporating realworld reasoning frameworks, and refining dialogue diversity
to better support complex human-AI interactions.


**7** **CONCLUSION**


This survey has presented a systematic taxonomy of LLM
agents, deconstructing their methodological components
across construction, collaboration, and evolution dimensions.
We have advanced a unified architectural perspective that
bridges individual agent design principles with multi-agent
collaborative systems—an approach that distinguishes our
work from previous surveys. Despite remarkable progress,
significant challenges remain, including scalability limitations, memory constraints, reliability concerns, and inadequate evaluation frameworks. Looking forward, we anticipate transformative developments in coordination protocols,
hybrid architectures, self-supervised learning, and safety
mechanisms that will enhance agent capabilities across
diverse domains. By providing this foundational understanding and identifying promising research directions, we
hope to contribute to the responsible advancement of LLM
agent technologies that may fundamentally reshape humanmachine collaboration.



19


**REFERENCES**


[1] Z. Xi, W. Chen, X. Guo, W. He, Y. Ding, B. Hong, M. Zhang,
J. Wang, S. Jin, E. Zhou _et al._, “The rise and potential of large
language model based agents: A survey,” _Science China Information_
_Sciences_, vol. 68, no. 2, p. 121101, 2025.

[2] M. Wooldridge and N. R. Jennings, “Intelligent agents: Theory
and practice,” _The knowledge engineering review_, vol. 10, no. 2, pp.
115–152, 1995.

[3] D. Zheng, M. Lapata, and J. Z. Pan, “Large language models as
reliable knowledge bases?” _arXiv preprint arXiv:2407.13578_, 2024.

[4] S. Lotfi, M. Finzi, Y. Kuang, T. G. Rudner, M. Goldblum, and A. G.
Wilson, “Non-vacuous generalization bounds for large language
models,” _arXiv preprint arXiv:2312.17173_, 2023.

[5] H. Fei, Y. Yao, Z. Zhang, F. Liu, A. Zhang, and T.-S. Chua,
“From multimodal llm to human-level ai: Modality, instruction,
reasoning, efficiency and beyond,” in _COLING_, 2024, pp. 1–8.

[6] J. Huang and K. C.-C. Chang, “Towards reasoning in large
language models: A survey,” _arXiv preprint arXiv:2212.10403_, 2022.

[7] C. Wang, W. Luo, Q. Chen, H. Mai, J. Guo, S. Dong, Z. Li, L. Ma,
S. Gao _et al._, “Tool-lmm: A large multi-modal model for tool agent
learning,” _arXiv e-prints_, pp. arXiv–2401, 2024.

[8] Z. Zhang, X. Bo, C. Ma, R. Li, X. Chen, Q. Dai, J. Zhu, Z. Dong,
and J.-R. Wen, “A survey on the memory mechanism of large
language model based agents,” _arXiv preprint arXiv:2404.13501_,
2024.

[9] P. Zhao, Z. Jin, and N. Cheng, “An in-depth survey of large
language model-based artificial intelligence agents,” _arXiv preprint_
_arXiv:2309.14365_, 2023.

[10] T. Sumers, S. Yao, K. Narasimhan, and T. Griffiths, “Cognitive
architectures for language agents,” _TMLR_, 2023.

[11] S. Hu, T. Huang, F. Ilhan, S. Tekin, G. Liu, R. Kompella, and L. Liu,
“A survey on large language model-based game agents,” _arXiv_
_preprint arXiv:2404.02039_, 2024.

[12] X. Xu, Y. Wang, C. Xu, Z. Ding, J. Jiang, Z. Ding, and B. F. Karlsson,
“A survey on game playing agents and large models: Methods,
applications, and challenges,” _arXiv preprint arXiv:2403.10249_,
2024.

[13] M. Xu, H. Du, D. Niyato, J. Kang, Z. Xiong, S. Mao, Z. Han,
A. Jamalipour, D. I. Kim, X. Shen _et al._, “Unleashing the power
of edge-cloud generative ai in mobile networks: A survey of aigc
services,” _IEEE Communications Surveys & Tutorials_, vol. 26, no. 2,
pp. 1127–1170, 2024.

[14] G. Qu, Q. Chen, W. Wei, Z. Lin, X. Chen, and K. Huang, “Mobile
edge intelligence for large language models: A contemporary
survey,” _IEEE Communications Surveys & Tutorials_, 2025.

[15] Z. Durante, Q. Huang, N. Wake, R. Gong, J. S. Park, B. Sarkar,
R. Taori, Y. Noda, D. Terzopoulos, Y. Choi _et al._, “Agent ai:
Surveying the horizons of multimodal interaction,” _arXiv preprint_
_arXiv:2401.03568_, 2024.

[16] Y. Wang, Y. Pan, Q. Zhao, Y. Deng, Z. Su, L. Du, and
T. H. Luan, “Large model agents: State-of-the-art, cooperation
paradigms, security and privacy, and future trends,” _arXiv preprint_
_arXiv:2409.14457_, 2024.

[17] L. Wang, C. Ma, X. Feng, Z. Zhang, H. Yang, J. Zhang, Z. Chen,
J. Tang, X. Chen, Y. Lin _et al._, “A survey on large language model
based autonomous agents,” _Frontiers of Computer Science_, vol. 18,
no. 6, p. 186345, 2024.

[18] X. Li, S. Wang, S. Zeng, Y. Wu, and Y. Yang, “A survey on llm-based
multi-agent systems: workflow, infrastructure, and challenges,”
_Vicinagearth_, vol. 1, no. 1, p. 9, 2024.

[19] X. Li, “A review of prominent paradigms for llm-based agents:
Tool use (including rag), planning, and feedback learning,” _arXiv_
_preprint arXiv:2406.05804_, 2024.

[20] W. Jin, H. Du, B. Zhao, X. Tian, B. Shi, and G. Yang, “A comprehensive survey on multi-agent cooperative decision-making:
Scenarios, approaches, challenges and perspectives,” _arXiv preprint_
_arXiv:2503.13415_, 2025.

[21] Y. Ma, Z. Song, Y. Zhuang, J. Hao, and I. King, “A survey on
vision-language-action models for embodied ai,” _arXiv preprint_
_arXiv:2405.14093_, 2024.

[22] T. Guo, X. Chen, Y. Wang, R. Chang, S. Pei, N. V. Chawla,
O. Wiest, and X. Zhang, “Large language model based multiagents: A survey of progress and challenges,” _arXiv preprint_
_arXiv:2402.01680_, 2024.

[23] T. Masterman, S. Besen, M. Sawtell, and A. Chao, “The landscape
of emerging ai agent architectures for reasoning, planning, and
tool calling: A survey,” _arXiv preprint arXiv:2404.11584_, 2024.


[24] Y. Cheng, C. Zhang, Z. Zhang, X. Meng, S. Hong, W. Li, Z. Wang,
Z. Wang, F. Yin, J. Zhao _et al._, “Exploring large language model
based intelligent agents: Definitions, methods, and prospects,”
_arXiv preprint arXiv:2401.03428_, 2024.

[25] G. Li, H. A. A. K. Hammoud, H. Itani, D. Khizbullin, and
B. Ghanem, “Camel: Communicative agents for ”mind” exploration of large language model society,” in _NeurIPS_, 2023.

[26] Q. Wu, G. Bansal, J. Zhang, Y. Wu, B. Li, E. Zhu, L. Jiang, X. Zhang,
S. Zhang, J. Liu, A. H. Awadallah, R. W. White, D. Burger, and
C. Wang, “Autogen: Enabling next-gen llm applications via multiagent conversation,” 2023.

[27] S. Hong, X. Zheng, J. Chen, Y. Cheng, J. Wang, C. Zhang, Z. Wang,
S. K. S. Yau, Z. Lin, L. Zhou _et al._, “Metagpt: Meta programming
for a multi-agent collaborative framework,” in _ICLR_, 2024.

[28] C. Qian, W. Liu, H. Liu, N. Chen, Y. Dang, J. Li, C. Yang, W. Chen,
Y. Su, X. Cong _et al._, “Chatdev: Communicative agents for software
development,” in _ACL_, 2024, pp. 15 174–15 186.

[29] J. Zhang, J. Xiang, Z. Yu, F. Teng, X.-H. Chen, J. Chen, M. Zhuge,
X. Cheng, S. Hong, J. Wang, B. Liu, Y. Luo, and C. Wu, “AFlow:
Automating agentic workflow generation,” in _ICLR_, 2025.

[30] J. S. Park, J. O’Brien, C. J. Cai, M. R. Morris, P. Liang, and M. S.
Bernstein, “Generative agents: Interactive simulacra of human
behavior,” in _UIST_, 2023, pp. 1–22.

[31] L. Wang, J. Zhang, H. Yang, Z.-Y. Chen, J. Tang, Z. Zhang, X. Chen,
Y. Lin, H. Sun, R. Song _et al._, “User behavior simulation with large
language model-based agents,” _ACM Transactions on Information_
_Systems_, vol. 43, no. 2, pp. 1–37, 2025.

[32] O. Khattab, A. Singhvi, P. Maheshwari, Z. Zhang, K. Santhanam,
S. Vardhamanan, S. Haq, A. Sharma, T. T. Joshi, H. Moazam,
H. Miller, M. Zaharia, and C. Potts, “Dspy: Compiling declarative
language model calls into self-improving pipelines,” in _ICLR_, 2024.

[33] S. Yao, J. Zhao, D. Yu, N. Du, I. Shafran, K. Narasimhan, and
Y. Cao, “React: Synergizing reasoning and acting in language
models,” in _ICLR_, 2023.

[34] M. Besta, N. Blach, A. Kubicek, R. Gerstenberger, M. Podstawski,
L. Gianinazzi, J. Gajda, T. Lehmann, H. Niewiadomski, P. Nyczyk
_et al._, “Graph of thoughts: Solving elaborate problems with large
language models,” in _AAAI_, vol. 38, no. 16, 2024, pp. 17 682–17 690.

[35] G. Wang, Y. Xie, Y. Jiang, A. Mandlekar, C. Xiao, Y. Zhu, L. Fan,
and A. Anandkumar, “Voyager: An open-ended embodied agent
with large language models,” _TMLR_, 2023.

[36] X. Zhu, Y. Chen, H. Tian, C. Tao, W. Su, C. Yang, G. Huang,
B. Li, L. Lu, X. Wang _et al._, “Ghost in the minecraft: Generally
capable agents for open-world environments via large language
models with text-based knowledge and memory,” _arXiv preprint_
_arXiv:2305.17144_, 2023.

[37] A. Zhao, D. Huang, Q. Xu, M. Lin, Y.-J. Liu, and G. Huang, “Expel:
Llm agents are experiential learners,” in _AAAI_, 2024, pp. 19 632–
19 642.

[38] N. Shinn, F. Cassano, A. Gopinath, K. Narasimhan, and S. Yao,
“Reflexion: Language agents with verbal reinforcement learning,”
_NeurIPS_, vol. 36, pp. 8634–8652, 2023.

[39] J. Ruan, Y. Chen, B. Zhang, Z. Xu, T. Bao, H. Mao, Z. Li, X. Zeng,
R. Zhao _et al._, “Tptu: Task planning and tool usage of large
language model-based ai agents,” in _NeurIPS_, 2023.

[40] T. Xie, F. Zhou, Z. Cheng, P. Shi, L. Weng, Y. Liu, T. J. Hua, J. Zhao,
Q. Liu, C. Liu _et al._, “Openagents: An open platform for language
agents in the wild,” _arXiv preprint arXiv:2310.10634_, 2023.

[41] H. Wang, H. Xin, C. Zheng, Z. Liu, Q. Cao, Y. Huang, J. Xiong,
H. Shi, E. Xie, J. Yin _et al._, “Lego-prover: Neural theorem proving
with growing libraries,” in _ICLR_, 2024.

[42] C. Packer, V. Fang, S. G. Patil, K. Lin, S. Wooders, and J. E.
Gonzalez, “Memgpt: Towards llms as operating systems,” _CoRR_,
2023.

[43] P. Lewis, E. Perez, A. Piktus, F. Petroni, V. Karpukhin, N. Goyal,
H. Kuttler, M. Lewis, W.-t. Yih, T. Rockt¨ aschel¨ _et al._, “Retrievalaugmented generation for knowledge-intensive nlp tasks,”
_NeurIPS_, vol. 33, pp. 9459–9474, 2020.

[44] D. Edge, H. Trinh, N. Cheng, J. Bradley, A. Chao, A. Mody, S. Truitt,
D. Metropolitansky, R. O. Ness, and J. Larson, “From local to
global: A graph rag approach to query-focused summarization,”
_arXiv preprint arXiv:2404.16130_, 2024.

[45] Y. Zhang, R. Sun, Y. Chen, T. Pfister, R. Zhang, and S. Arik, “Chain
of agents: Large language models collaborating on long-context
tasks,” _Advances in Neural Information Processing Systems_, vol. 37,
pp. 132 208–132 237, 2024.



20


[46] H. Trivedi, N. Balasubramanian, T. Khot, and A. Sabharwal, “Interleaving retrieval with chain-of-thought reasoning for knowledgeintensive multi-step questions,” _arXiv preprint arXiv:2212.10509_,
2022.

[47] X. Li, C. Zhu, L. Li, Z. Yin, T. Sun, and X. Qiu, “Llatrieval: Llmverified retrieval for verifiable generation,” in _NAACL_, 2024, pp.
5453–5471.

[48] W. Wu, Y. Jing, Y. Wang, W. Hu, and D. Tao, “Graph-augmented
reasoning: Evolving step-by-step knowledge graph retrieval for
llm reasoning,” 2025.

[49] X. Guan, J. Zeng, F. Meng, C. Xin, Y. Lu, H. Lin, X. Han, L. Sun,
and J. Zhou, “Deeprag: Thinking to retrieval step by step for large
language models,” _arXiv preprint arXiv:2502.01142_, 2025.

[50] L. Wang, W. Xu, Y. Lan, Z. Hu, Y. Lan, R. K.-W. Lee, and E.P. Lim, “Plan-and-solve prompting: Improving zero-shot chainof-thought reasoning by large language models,” _arXiv preprint_
_arXiv:2305.04091_, 2023.

[51] E. H. Durfee, “Distributed problem solving and planning,” in
_ECCAI Advanced Course on Artificial Intelligence_ . Springer, 2001,
pp. 118–149.

[52] M. Tao, D. Zhao, and Y. Feng, “Chain-of-discussion: A multimodel framework for complex evidence-based question answering,” _arXiv preprint arXiv:2402.16313_, 2024.

[53] M. Hu, Y. Mu, X. Yu, M. Ding, S. Wu, W. Shao, Q. Chen,
B. Wang, Y. Qiao, and P. Luo, “Tree-planner: Efficient closeloop task planning with large language models,” _arXiv preprint_
_arXiv:2310.08582_, 2023.

[54] J.-W. Choi, H. Kim, H. Ong, Y. Yoon, M. Jang, J. Kim _et al._,
“Reactree: Hierarchical task planning with dynamic tree expansion
using llm agent nodes,” 2025.

[55] J. Long, “Large language model guided tree-of-thought,” _arXiv_
_preprint arXiv:2305.08291_, 2023.

[56] D. Zhang, S. Zhoubian, Z. Hu, Y. Yue, Y. Dong, and J. Tang, “Restmcts*: Llm self-training via process reward guided tree search,”
_NeurIPS_, vol. 37, pp. 64 735–64 772, 2024.

[57] A. Lykov, M. Dronova, N. Naglov, M. Litvinov, S. Satsevich,
A. Bazhenov, V. Berman, A. Shcherbak, and D. Tsetserukou, “Llmmars: Large language model for behavior tree generation and nlpenhanced dialogue in multi-agent robot systems,” _arXiv preprint_
_arXiv:2312.09348_, 2023.

[58] J. Ao, F. Wu, Y. Wu, A. Swikir, and S. Haddadin, “Llm as btplanner: Leveraging llms for behavior tree generation in robot
task planning,” _arXiv preprint arXiv:2409.10444_, 2024.

[59] C. Rivera, G. Byrd, W. Paul, T. Feldman, M. Booker, E. Holmes,
D. Handelman, B. Kemp, A. Badger, A. Schmidt _et al._, “Conceptagent: Llm-driven precondition grounding and tree search for robust task planning and execution,” _arXiv preprint arXiv:2410.06108_,
2024.

[60] V. Bhat, A. U. Kaypak, P. Krishnamurthy, R. Karri, and F. Khorrami,
“Grounding llms for robot task planning using closed-loop state
feedback,” _arXiv preprint arXiv:2402.08546_, 2024.

[61] H. Li, H. Jiang, T. Zhang, Z. Yu, A. Yin, H. Cheng, S. Fu, Y. Zhang,
and W. He, “Traineragent: Customizable and efficient model
training through llm-powered multi-agent system,” _arXiv preprint_
_arXiv:2311.06622_, 2023.

[62] G. Wan, Y. Wu, J. Chen, and S. Li, “Dynamic self-consistency:
Leveraging reasoning paths for efficient llm sampling,” _arXiv_
_preprint arXiv:2408.17017_, 2024.

[63] S. Seo, J. Lee, S. Noh, and H. Kang, “Llm-based cooperative agents
using information relevance and plan validation,” _arXiv preprint_
_arXiv:2405.16751_, 2024.

[64] H. Sun, Y. Zhuang, L. Kong, B. Dai, and C. Zhang, “Adaplanner: Adaptive planning from feedback with language models,”
_NeurIPS_, vol. 36, pp. 58 202–58 245, 2023.

[65] M. Jafaripour, S. Golestan, S. Miwa, Y. Mitsuka, and O. Zaiane,
“Adaptive iterative feedback prompting for obstacle-aware path
planning via llms,” in _AAAI Workshop_, 2025.

[66] S. Qiao, H. Gui, C. Lv, Q. Jia, H. Chen, and N. Zhang, “Making
language models better tool learners with execution feedback,”
_arXiv preprint arXiv:2305.13068_, 2023.

[67] R. Yang, L. Song, Y. Li, S. Zhao, Y. Ge, X. Li, and Y. Shan,
“Gpt4tools: Teaching large language model to use tools via selfinstruction,” _NeurIPS_, vol. 36, pp. 71 995–72 007, 2023.

[68] S. Yuan, K. Song, J. Chen, X. Tan, Y. Shen, R. Kan, D. Li, and
D. Yang, “Easytool: Enhancing llm-based agents with concise tool
instruction,” _arXiv preprint arXiv:2401.06201_, 2024.


[69] S. Wu, S. Zhao, Q. Huang, K. Huang, M. Yasunaga, K. Cao,
V. Ioannidis, K. Subbian, J. Leskovec, and J. Y. Zou, “Avatar:
Optimizing llm agents for tool usage via contrastive reasoning,”
_NeurIPS_, vol. 37, pp. 25 981–26 010, 2025.

[70] Y. Huang, J. Sansom, Z. Ma, F. Gervits, and J. Chai, “Drivlme:
Enhancing llm-based autonomous driving agents with embodied
and social experiences,” in _IROS_ . IEEE, 2024, pp. 3153–3160.

[71] Y. Zhang, S. Yang, C. Bai, F. Wu, X. Li, Z. Wang, and X. Li,
“Towards efficient llm grounding for embodied multi-agent collaboration,” _arXiv preprint arXiv:2405.14314_, 2024.

[72] B. Colle, “Improving embodied llm agents capabilities through
collaboration,” 2024.

[73] D. A. Boiko, R. MacKnight, B. Kline, and G. Gomes, “Autonomous
chemical research with large language models,” _Nature_, vol. 624,
no. 7992, pp. 570–578, 2023.

[74] H. Jiang, Q. Wu, C.-Y. Lin, Y. Yang, and L. Qiu, “Llmlingua:
Compressing prompts for accelerated inference of large language
models,” in _EMNLP_, 2023, pp. 13 358–13 376.

[75] S. Qiao, N. Zhang, R. Fang, Y. Luo, W. Zhou, Y. E. Jiang, C. Lv,
and H. Chen, “Autoact: Automatic agent learning from scratch
for qa via self-planning,” _arXiv preprint arXiv:2401.05268_, 2024.

[76] M. Suzgun and A. T. Kalai, “Meta-prompting: Enhancing language models with task-agnostic scaffolding,” _arXiv preprint_
_arXiv:2401.12954_, 2024.

[77] A. Khan, J. Hughes, D. Valentine, L. Ruis, K. Sachan, A. Radhakrishnan, E. Grefenstette, S. R. Bowman, T. Rocktaschel, and¨
E. Perez, “Debating with more persuasive llms leads to more
truthful answers,” _arXiv preprint arXiv:2402.06782_, 2024.

[78] X. Tang, A. Zou, Z. Zhang, Z. Li, Y. Zhao, X. Zhang, A. Cohan, and
M. Gerstein, “Medagents: Large language models as collaborators
for zero-shot medical reasoning,” _arXiv preprint arXiv:2311.10537_,
2023.

[79] J. C.-Y. Chen, S. Saha, and M. Bansal, “Reconcile: Round-table
conference improves reasoning via consensus among diverse llms,”
_arXiv preprint arXiv:2309.13007_, 2023.

[80] T. Liang, Z. He, W. Jiao, X. Wang, Y. Wang, R. Wang, Y. Yang,
S. Shi, and Z. Tu, “Encouraging divergent thinking in large
language models through multi-agent debate,” _arXiv preprint_
_arXiv:2305.19118_, 2023.

[81] K. Kim, S. Lee, K.-H. Huang, H. P. Chan, M. Li, and H. Ji, “Can
llms produce faithful explanations for fact-checking? towards
faithful explainable fact-checking via multi-agent debate,” _arXiv_
_preprint arXiv:2402.07401_, 2024.

[82] Y. Du, S. Li, A. Torralba, J. B. Tenenbaum, and I. Mordatch,
“Improving factuality and reasoning in language models through
multiagent debate,” in _ICML_, 2023.

[83] Y. Zhu, S. Qiao, Y. Ou, S. Deng, N. Zhang, S. Lyu, Y. Shen,
L. Liang, J. Gu, and H. Chen, “Knowagent: Knowledge-augmented
planning for llm-based agents,” _arXiv preprint arXiv:2403.03101_,
2024.

[84] S. Qiao, R. Fang, N. Zhang, Y. Zhu, X. Chen, S. Deng, Y. Jiang,
P. Xie, F. Huang, and H. Chen, “Agent planning with world
knowledge model,” _NeurIPS_, vol. 37, pp. 114 843–114 871, 2024.

[85] R. Fang, S. Qiao, and Z. Xi, “Refining guideline knowledge for
agent planning using textgrad,” in _ICKG_ . IEEE, 2024, pp. 102–103.

[86] Q. Zhong, L. Ding, J. Liu, B. Du, and D. Tao, “Self-evolution
learning for discriminative language model pretraining,” in _ACL_
_Findings_, 2023, pp. 4130–4145.

[87] T. Akiba, M. Shing, Y. Tang, Q. Sun, and D. Ha, “Evolutionary optimization of model merging recipes,” _Nature Machine Intelligence_,
pp. 1–10, 2025.

[88] S. Wu, K. Lu, B. Xu, J. Lin, Q. Su, and C. Zhou, “Self-evolved
diverse data sampling for efficient instruction tuning,” _arXiv_
_preprint arXiv:2311.08182_, 2023.

[89] A. Madaan, N. Tandon, P. Gupta, S. Hallinan, L. Gao, S. Wiegreffe,
U. Alon, N. Dziri, S. Prabhumoye, Y. Yang _et al._, “Self-refine:
Iterative refinement with self-feedback,” _NeurIPS_, vol. 36, pp.
46 534–46 594, 2023.

[90] E. Zelikman, Y. Wu, J. Mu, and N. D. Goodman, “Star: Self-taught
reasoner bootstrapping reasoning with reasoning,” in _NeurIPS_,
vol. 1126, 2024.

[91] A. Hosseini, X. Yuan, N. Malkin, A. Courville, A. Sordoni, and
R. Agarwal, “V-star: Training verifiers for self-taught reasoners,”
in _COLM_, 2024.

[92] Y. Weng, M. Zhu, F. Xia, B. Li, S. He, S. Liu, B. Sun, K. Liu,
and J. Zhao, “Large language models are better reasoners with
self-verification,” in _EMNLP Findings_, 2023, pp. 2550–2575.



21


[93] W. Yuan, R. Y. Pang, K. Cho, X. Li, S. Sukhbaatar, J. Xu, and
J. Weston, “Self-rewarding language models,” 2024.

[94] K. Yang, D. Klein, A. Celikyilmaz, N. Peng, and Y. Tian, “Rlcd:
Reinforcement learning from contrastive distillation for lm alignment,” in _ICLR_, 2024.

[95] J.-C. Pang, P. Wang, K. Li, X.-H. Chen, J. Xu, Z. Zhang, and Y. Yu,
“Language model self-improvement by reinforcement learning
contemplation,” in _ICLR_, 2024.

[96] C. Zhang, K. Yang, S. Hu, Z. Wang, G. Li, Y. Sun, C. Zhang,
Z. Zhang, A. Liu, S.-C. Zhu _et al._, “Proagent: building proactive
cooperative agents with large language models,” in _AAAI_, vol. 38,
no. 16, 2024, pp. 17 591–17 599.

[97] H. Ma, T. Hu, Z. Pu, L. Boyin, X. Ai, Y. Liang, and M. Chen,
“Coevolving with the other you: Fine-tuning llm with sequential
cooperative multi-agent reinforcement learning,” _NeurIPS_, vol. 37,
pp. 15 497–15 525, 2024.

[98] C. Ma, Z. Yang, H. Ci, J. Gao, M. Gao, X. Pan, and Y. Yang,
“Evolving diverse red-team language models in multi-round multiagent games,” _arXiv preprint arXiv:2310.00322_, 2023.

[99] T. Liang, Z. He, W. Jiao, X. Wang, Y. Wang, R. Wang, Y. Yang, S. Shi,
and Z. Tu, “Encouraging divergent thinking in large language
models through multi-agent debate,” in _EMNLP_, 2024, pp. 17 889–
17 904.

[100] Z. Gou, Z. Shao, Y. Gong, Y. Yang, N. Duan, W. Chen _et al._, “Critic:
Large language models can self-correct with tool-interactive
critiquing,” in _ICLR_, 2024.

[101] Y. Song, D. Yin, X. Yue, J. Huang, S. Li, and B. Y. Lin, “Trial and
error: Exploration-based trajectory optimization of llm agents,” in
_ACL_, 2024, pp. 7584–7600.

[102] S. Jiang, Y. Wang, and Y. Wang, “Selfevolve: A code evolution framework via large language models,” _arXiv preprint_
_arXiv:2306.02907_, 2023.

[103] X. Huang, W. Liu, X. Chen, X. Wang, H. Wang, D. Lian, Y. Wang,
R. Tang, and E. Chen, “Understanding the planning of llm agents:
A survey,” _arXiv preprint arXiv:2402.02716_, 2024.
