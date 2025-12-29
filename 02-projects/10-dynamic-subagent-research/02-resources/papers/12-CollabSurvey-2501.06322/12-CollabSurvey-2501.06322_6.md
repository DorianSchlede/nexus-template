<!-- Source: 12-CollabSurvey-2501.06322.pdf | Chunk 6/7 -->

flows (Content Transformation, Seed Instruction Generation, and Instruction Refinement) and
decentralised structure of agents in each flow, it showed significant performance gains when used
to fine-tune a Mistral 7B model, achieving improvements of up to 54% across various benchmarks.
Orca-AgentInstruct project represents a significant step towards building a synthetic data factory
for model customization and continuous improvement.
In summary, the capabilities of QA/NLG in different tasks have been improved by integrating the
MAS mechanism into the process. Response evaluation in QA is now done with higher confidence,
since the MAS evaluation systems resemble the process of human evaluation and now includes
more dynamic evaluation with automated modified benchmarks. The NLG task of synthesizing
the data is also carried out with higher-quality training data generated from the collaboration
mechanism. Several notable frameworks recently introduced by big-tech companies also pave
the way for the easier creation of MASs, promoting the development of such systems in practical
applications. It is important to recognize that these early efforts are still in the process of being
adapted and that the efficacy of applying them in practice will take time to be assessed. In addition,
the integration of different types and strategies of collaboration, communication structures, and
orchestration architecture also need to be considered, since most existing frameworks or systems
are focusing primarily on role-based strategy and either centralized or decentralized structures.


**5.3** **Social and Cultural Domains**

Research on LLMs and MASs has showcased the capability and applicability of these systems to
simulate human behaviors, social dynamics, and cultural interactions, offering novel methodologies
for understanding complex societal phenomenons, as illustrated in Fig. 8. Studies such as [3, 11]
argue the potential of LLMs to enhance traditional social science methods, including survey research,
online experiments, automated content analyses, and agent-based modeling. However, these studies
also underscore critical limitations, such as biases in training data that lack global psychological
diversity, cautioning against treating stand-alone LLMs as universal solutions. The shift from
stand-alone LLMs to Multi-Agent Collaborative Systems can not only enable the analysis of LLMs
in replicating individual social behavior but also provide powerful tools for exploring complex
social dynamics, collaborative problem-solving, and emergent collective behaviors [46].
Several studies have focused on simulating social interactions through carefully designed environments, where agents are equipped with diverse prompts or LLMs tailored to specific roles. For
instance, [89] follows the definition of social interaction as a theatrical performance, with agents
assuming roles (e.g., office employees or family members) driven by LLMs like GPT-4, Qwen2.5-14b,


[8https://www.microsoft.com/en-us/research/blog/orca-agentinstruct-agentic-flows-can-be-effective-synthetic-data-](https://www.microsoft.com/en-us/research/blog/orca-agentinstruct-agentic-flows-can-be-effective-synthetic-data-generators/)
[generators/](https://www.microsoft.com/en-us/research/blog/orca-agentinstruct-agentic-flows-can-be-effective-synthetic-data-generators/)


Multi-Agent Collaboration Mechanisms: A Survey of LLMs 27















Fig. 8. LLM-based multi-agent collaborative system in social & cultural applications.


or Llama-3-8b. These roles include specific goals, such as providing and receiving feedback during
office discussions. Research has shown that collaboration among LLM-based agents can elicit
human-like capabilities, including conversational skills, theory of mind (reasoning about others’
mental states) [2, 75], Hobbesian social contract theory (submit to authority to avoid chaos) [31],
and non-verbal action inference [79, 147].
**Social Applications.** Authors in [5, 36] suggest that LLM-based agents can replace human
participants in specific social science experiments, while [88] demonstrates their use in generating
diverse natural language data with iterative cross-agent refinement. Moreover, multimodal AI
systems such as those described in [144] integrate verbal, non-verbal, and social cues as input
to multi-tier collaborative agents to generate in-situ suggestions via augmented reality glasses.
Integrating LLM-based agents into traditional agent-based modeling [48] can enhance the realism
of simulations, offering controlled environments to test social theories, including the effects of
policy interventions [10, 148] and norm violation detection [53].
**Cultural Applications.** LLM-based MASs can represent diverse cultural perspectives, advancing
cross-cultural understanding and reducing bias. For example, the CulturePark framework [73]
simulates cross-cultural interactions, with each agent embodying distinct cultural viewpoints.
Similarly, Mango [94] iteratively extracts high-quality cultural knowledge from LLM-based agents,
providing a rich dataset for fine-tuning models to improve their ability to align with diverse cultural
contexts. Another emerging area involves simulating cultural evolution within LLM populations.
By modeling how cultural information is transmitted and transformed among agents, researchers
gain insights into both human cultural dynamics and their influence on LLM behavior [103, 126].
Another area of application involves simulating cultural evolution within LLM populations. By
modeling how cultural information is transmitted and transformed among agents, researchers gain
insights into both human cultural dynamics and their influence on LLM behavior [103].
Despite their promise, LLMs are not perfect replicas of humans and cannot fully replicate the
complexities of human social and cultural behavior. For instance, [36] highlights the limitations
of using LLMs as human replacements in social science experiments, particularly in scenarios
involving information asymmetry (unequal access to private mental states or goals) [161], and in
tasks requiring competition and conflict resolution [89]. To address these challenges, consistent and
standardized benchmarking approaches are necessary to evaluate the cultural and social awareness
of LLM-based agents [109].


28 Tran et al.


**6** **Open Problems & Discussion**


**6.1** **The Road to Artificial Collective Intelligence**

Collective intelligence is the ability of a group to perform complex tasks and solve problems
collectively, often overcoming the sum of individual contributions [71]. With increasingly complex
capabilities that mimic characteristics of living organisms, LLMs are being treated as “digital
species”. Enabling collective intelligence through collaborations among multiple LLM-based agents
offers the potential for AI systems that are adaptive, efficient, and capable of addressing real-world
problems. However, several open challenges must be addressed to realize this potential fully.
**Unified Governance.** Unified governance is fundamental in enabling collective intelligence
among group of LLM-based agents, including the design of coordination and planning mechanisms.
Deciding which steps to take, which agents to involve, and how tasks should be distributed among
them requires advanced mechanisms. Assigning specific roles or specializations to individual agents
can enhance the system’s overall effectiveness. Determining optimal role assignments and ensuring
agents can adapt to dynamic task requirements are ongoing research areas. Moreover, governance
must account for potential failures, such as miscommunication or task disruptions. Designing
robust mechanisms to detect and recover from such failures is vital for ensuring the reliability and
resilience of MASs. For example, introducing redundancy or fallback agents may help maintain
system functionality even in adversarial scenarios.
**Shared Decision Making.** Beyond governance, MASs must achieve coherent and accurate
collective decision-making. Current LLM-based MASs commonly utilize limited decision-making
methods, such as dictatorial or popular voting, which may not capture different aspects of agent preferences, or aggregating overconfidence of LLMs. Research into novel decision making approaches
can enhance the diversity and fairness of collective decisions.
**Agent as Digital Species.** LLMs are increasingly being viewed as digital species; however, they
were not originally designed for agentic applications involving collaboration and multi-participant
interactions. They suffer from known limitations such as hallucinations and are susceptible to
adversarial attacks. A single agent’s hallucination can be spread and reinforced by other agents,
leading to minor inaccuracies into critical and cascading effects. Addressing these issues requires
techniques to not only detect and correct individual errors but also to control the collaboration
channels between agents. Designing LLMs specifically for collaborative environments, such as
Gemini 2.0 [9], represents a step toward refining these “digital species” for agentic systems.
**Scalability and Resource Maintainance.** Increasing agent population poses a significant
challenge in MASs. Managing resources (memory, processing time), coordination and collaboration
channels among a growing number of agents introduces additional complexities, such as maintaining efficiency in agent interactions and preventing bottlenecks. Understanding the scaling laws of
the behavior and performance of MASs is critical for designing architectures capable of handling
large-scale collaboration.
**Discovering/Exploring Unexpected Generalization.** Complex, emergent behaviors of collective intelligence, such as coordinated problem-solving or innovation, can arise under the right
conditions, especially in generalizing to unseen domains. However, identifying and fostering these
conditions is an ongoing challenge. Understanding how these generalizations emerge from the
interactions of agents is key to acquiring collective intelligence.


**6.2** **Comprehensive Evaluation and Benchmarking**


Evaluation of MASs presents challenges beyond the evaluation of individual LLMs. While there has
been active research in exploring various aspects of LLMs [19], including their decision making


[9https://blog.google/products/gemini/google-gemini-ai-collection-2024/](https://blog.google/products/gemini/google-gemini-ai-collection-2024/)


Multi-Agent Collaboration Mechanisms: A Survey of LLMs 29


capabilities and tool usage in agentic applications [100, 102], relatively few effort has been dedicated
to systematically assessing the performance and behavior of LLM-based MASs [80].
The collaborative nature of these systems introduces complexities that require a broader set of
evaluation criteria. These criteria include assessing the overall system performance [155], such
as reasoning capabilities, task completion rates, as well as specific system characteristics like
coordination efficiency and contextual appropriateness [17]. Fine-grained evaluation at the agent
and collaboration levels enable root cause analysis [63], offering insights into individual agent
behaviors, the effectiveness of collaboration channels, and the system’s overall dynamics.
Furthermore, evaluations of MASs are often conducted in narrow scenarios with different configurations, leading to inconsistent and incomparable results [18, 22, 34]. The absence of standardized
evaluation protocols prevents the ability to objectively compare different systems and track progress
across the field. Establishing unified, broad, and comprehensive benchmarking frameworks is vital
to ensure reproducibility and consistency in evaluating MASs. Moreover, static evaluation benchmarks risk becoming lack of relevance to current real-world scenarios, leading to data leakage and
overfitting [102]. Therfore, there is a need for implementing dynamic benchmarking systems that
evolve alongside technological and informational advancements.


**6.3** **Ethical Risk and Safety**

Intrinsicly, LLMs can be harmful with hallucinated information. When deployed in MASs, these
issues can propagate and amplify through agent interactions. There are two key factors behind
this amplification: LLM overconfidence problem, where LLMs persistently assert the correctness
of their outputs despite inaccuracies [151], and misunderstandings that arise between LLM-based
agents during collaboration. Additionally, LLMs are vulnerable to adversarial attacks, which make
MASs particularly attractive targets for exploitation [115]. Compromised agents in such systems
can be manipulated to execute harmful or malicious behaviors. As the number of agents in LLMbased MAS increases, these risks scale proportionally, compromising the safety and reliability of
communication and information exchange.
Recent studies have also highlighted the potential for AI systems to deceive humans, raising
significant concerns in the context of LLM-based multi-agent collaborative systems [7, 35, 84].
These systems, capable of simulating human societies and exhibiting human-like psychological
traits, can blur the line between artificial and human behavior. Attributing human-like qualities
to these systems risks fostering over-reliance, where users place trust in their capabilities. This
perception can increase susceptibility to manipulation and obscure the inherent limitations of LLMbased agents [161]. Overlooking these limitations not only undermines informed decision-making
but also introduces broader ethical concerns [10] regarding the responsible deployment and use of
LLM-based MASs.


**7** **Conclusion**

Through our extensive review of the collaborative aspect of LLM-based MASs, we introduce a
structured and extensible framework as an important lens to guide future research. Our framework
characterizes collaboration along five key dimensions: actors, types, structures, strategies, and
coordination mechanisms, providing a systematic approach to analyze and design collaborative
interactions within MASs empowered by LLMs. We believe this work will inspire future research
and serve as a foundational step in advancing MASs toward more intelligent and collaborative
solutions.


[10https://artificialintelligenceact.eu/](https://artificialintelligenceact.eu/)


30 Tran et al.


**Acknowledgments**

This research work has emanated from research conducted with financial support from Science
Foundation Ireland under Grant 12/RC/2289-P2 and 18/CRT/6223.


**References**


[1] Azad Abad, Moin Nabi, and Alessandro Moschitti. 2017. Autonomous crowdsourcing through human-machine
collaborative learning. In _Proceedings of the 40th International ACM SIGIR Conference on Research and Development in_
_Information Retrieval_ . 873–876.

[2] Sahar Abdelnabi et al. 2024. Cooperation, Competition, and Maliciousness: LLM-Stakeholders Interactive Negotiation.
In _The Thirty-eight Conference on Neural Information Processing Systems Datasets and Benchmarks Track_ .

[3] Suhaib Abdurahman et al. 2024. Perils and opportunities in using large language models in psychological research.
_PNAS Nexus_ (Jul. 2024).

[4] Josh Achiam et al. 2023. Gpt-4 technical report. _arXiv preprint arXiv:2303.08774_ (2023).

[5] Gati Aher et al. 2023. Using large language models to simulate multiple humans and replicate human subject studies.
In _Proceedings of the International Conference on Machine Learning_ .

[6] Junhyeok Ahn and Luis Sentis. 2021. Nested mixture of experts: Cooperative and competitive learning of hybrid
dynamical system. In _Learning for Dynamics and Control_ . PMLR, 779–790.

[7] Canfer Akbulut et al. 2024. All Too Human? Mapping and Mitigating the Risk from Anthropomorphic AI. _Proceedings_
_of the AAAI/ACM Conference on AI, Ethics, and Society_ 7 (Oct. 2024), 13–26.

[8] Anonymous. 2024. DOMAIN GENERALIZATION VIA PARETO OPTIMAL GRADIENT MATCHING. In _Submitted to_
_The Thirteenth International Conference on Learning Representations_ . under review.

[9] Anonymous. 2024. Federated Domain Generalization with Data-free On-server Gradient Matching. In _Submitted to_
_The Thirteenth International Conference on Learning Representations_ . under review.

[10] Gabriele Ansaldo. 2023. _AgentSpeak: A Framework for Agent-Based Modeling with Integrated Large Language Models;_
_Case Study: Analyzing Policy Interventions in Electric Vehicle Adoption_ . Master’s thesis. Northeastern University.

[11] Christopher A. Bail. 2024. Can Generative AI improve social science? _Proceedings of the National Academy of Sciences_
121, 21 (2024), e2314021121.

[12] Rafael Barbarroxa et al. 2024. Benchmarking AutoGen with different large language models. In _2024 IEEE Conference_
_on Artificial Intelligence (CAI)_ . IEEE, 263–264.

[13] Kallista Bonawitz et al. 2021. Federated Learning and Privacy: Building privacy-preserving systems for machine
learning and data science on decentralized data. _Queue_ (Nov. 2021).

[14] Michele Braccini et al. 2024. Swarm Intelligence: A Novel and Unconventional Approach to Dance Choreography
Creation.

[[15] Weilin Cai et al. 2024. A Survey on Mixture of Experts. arXiv:2407.06204 [cs.LG]](https://arxiv.org/abs/2407.06204)

[16] Chengzhi Cao et al. 2024. Enhancing Human-AI Collaboration Through Logic-Guided Reasoning. In _The Twelfth_
_International Conference on Learning Representations_ .

[17] Alan Chan et al. 2023. Harms from Increasingly Agentic Algorithmic Systems. In _Proceedings of the 2023 ACM_
_Conference on Fairness, Accountability, and Transparency_ (Chicago, IL, USA) _(FAccT ’23)_ . Association for Computing
Machinery, New York, NY, USA, 651–666.

[18] Chi-Min Chan et al. 2024. ChatEval: Towards Better LLM-based Evaluators through Multi-Agent Debate. In _The_
_Twelfth International Conference on Learning Representations_ .

[19] Yupeng Chang et al. 2024. A survey on evaluation of large language models. _ACM Transactions on Intelligent Systems_
_and Technology_ 15, 3 (2024), 1–45.

[20] Guangyao Chen et al. 2024. AutoAgents: A Framework for Automatic Agent Generation. In _Proceedings of the_
_Thirty-Third International Joint Conference on Artificial Intelligence, IJCAI-24_, Kate Larson (Ed.). International Joint
Conferences on Artificial Intelligence Organization, 22–30. Main Track.

[21] Huaben Chen, Wenkang Ji, Lufeng Xu, and Shiyu Zhao. 2023. Multi-Agent Consensus Seeking via Large Language
Models. _ArXiv_ abs/2310.20151 (2023).

[22] Junzhe Chen et al. 2024. LLMArena: Assessing Capabilities of Large Language Models in Dynamic Multi-Agent
Environments. In _Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1:_
_Long Papers)_ . Association for Computational Linguistics, Bangkok, Thailand, 13055–13077.

[23] Pei Chen, Shuai Zhang, and Boran Han. 2024. CoMM: Collaborative Multi-Agent, Multi-Reasoning-Path Prompting
for Complex Problem Solving. In _Findings of the Association for Computational Linguistics: NAACL 2024_, Kevin Duh,
Helena Gomez, and Steven Bethard (Eds.). ACL, Mexico City, Mexico, 1720–1738.

[24] Weize Chen et al. 2024. AgentVerse: Facilitating Multi-Agent Collaboration and Exploring Emergent Behaviors. In
_The Twelfth International Conference on Learning Representations_ .


Multi-Agent Collaboration Mechanisms: A Survey of LLMs 31


[25] Wei-Lin Chiang et al. 2024. Chatbot arena: An open platform for evaluating llms by human preference. _arXiv preprint_
_arXiv:2403.04132_ (2024).

[26] Vincent Conitzer and Caspar Oesterheld. 2024. Foundations of Cooperative AI. _Proceedings of the AAAI Conference_
_on Artificial Intelligence_ 37, 13 (Jul. 2024), 15359–15367.

[27] James L. Crowley et al. 2023. A Hierarchical Framework for Collaborative Artificial Intelligence. _IEEE Pervasive_
_Computing_ [22, 1 (2023), 9–18. https://doi.org/10.1109/MPRV.2022.3208321](https://doi.org/10.1109/MPRV.2022.3208321)

[28] Florin Cuconasu et al. 2024. The power of noise: Redefining retrieval for rag systems. In _Proceedings of the 47th_
_International ACM SIGIR Conference on Research and Development in Information Retrieval_ . 719–729.

[[29] Allan Dafoe et al. 2020. Open Problems in Cooperative AI. arXiv:2012.08630 [cs.AI]](https://arxiv.org/abs/2012.08630)

[30] Allan Dafoe et al. 2021. Cooperative AI: machines must learn to find common ground. _Nature_ 593, 7857 (May 2021),
33–36.

[31] Gordon Dai et al. 2024. Artificial Leviathan: Exploring Social Evolution of LLM Agents Through the Lens of Hobbesian
[Social Contract Theory. arXiv:2406.14373 [cs.AI]](https://arxiv.org/abs/2406.14373)

[[32] Mike D’Arcy et al. 2024. MARG: Multi-Agent Review Generation for Scientific Papers. arXiv:2401.04259 [cs.CL]](https://arxiv.org/abs/2401.04259)

[33] Ayushman Das et al. 2023. Enabling Synergistic Knowledge Sharing and Reasoning in Large Language Models with
Collaborative Multi-Agents. In _IEEE International Conference on Collaboration and Internet Computing_ .

[34] Tim Ruben Davidson et al. 2024. Evaluating Language Model Agency Through Negotiations. In _The Twelfth_
_International Conference on Learning Representations_ .

[[35] Ameet Deshpande et al. 2023. Anthropomorphization of AI: Opportunities and Risks. arXiv:2305.14784 [cs.AI]](https://arxiv.org/abs/2305.14784)

[36] Danica Dillion et al. 2023. Can AI language models replace human participants? _Trends in Cognitive Sciences_ 27, 7
(2023), 597–600.

[37] Mohammad Divband Soorati et al. 2022. From intelligent agents to trustworthy human-centred multiagent systems.
_AI Communications_ 35, 4 (2022), 443–457.

[38] Manqing Dong, Hao Huang, and Longbing Cao. 2024. Can LLMs Serve As Time Series Anomaly Detectors? _arXiv_
_preprint arXiv:2408.03475_ (2024).

[39] Yubo Dong et al. 2024. VillagerAgent: A Graph-Based Multi-Agent Framework for Coordinating Complex Task
Dependencies in Minecraft. In _Findings of the Association for Computational Linguistics: ACL 2024_, Lun-Wei Ku, Andre
Martins, and Vivek Srikumar (Eds.). Association for Computational Linguistics, Bangkok, Thailand, 16290–16314.

[40] Ali Dorri, Salil S. Kanhere, and Raja Jurdak. 2018. Multi-Agent Systems: A Survey. _IEEE Access_ 6 (2018), 28573–28593.

[41] Yilun Du et al. 2023. Improving Factuality and Reasoning in Language Models through Multiagent Debate.
[arXiv:2305.14325 [cs.CL]](https://arxiv.org/abs/2305.14325)

[42] Lizhou Fan et al. 2024. A bibliometric review of large language models research from 2017 to 2023. _ACM Transactions_
_on Intelligent Systems and Technology_ 15, 5 (2024), 1–25.

[43] Joel E Fischer et al. 2021. In-the-loop or on-the-loop? Interactional arrangements to support team coordination with
a planning agent. _Concurrency and Computation: Practice and Experience_ 33, 8 (2021), e4082.

[44] Adam Fourney et al. 2024. _Magentic-One: A Generalist Multi-Agent System for Solving Complex Tasks_ . Technical
Report MSR-TR-2024-47. Microsoft.

[45] Chris Frith and Uta Frith. 2005. Theory of mind. _Current biology_ 15, 17 (2005), R644–R645.

[46] Chen Gao et al. 2024. Large language models empowered agent-based modeling and simulation: a survey and
perspectives. _Humanities and Social Sciences Communications_ 11, 1 (Sept. 2024).

[47] Taicheng Guo et al. 2024. Large Language Model Based Multi-agents: A Survey of Progress and Challenges. In
_Proceedings of the Thirty-Third International Joint Conference on Artificial Intelligence, IJCAI-24_, Kate Larson (Ed.).
International Joint Conferences on Artificial Intelligence Organization, 8048–8057. Survey Track.

[48] Onder Gurcan. 2024. LLM-Augmented Agent-Based Modelling for Social Simulations: Challenges and Opportunities.
[arXiv:2405.06700 [physics.soc-ph]](https://arxiv.org/abs/2405.06700)

[49] Thilo Hagendorff, Sarah Fabi, and Michal Kosinski. 2023. Human-like intuitive behavior and reasoning biases emerged
in large language models but disappeared in ChatGPT. _Nature Computational Science_ 3, 10 (2023), 833–838.

[[50] Shanshan Han et al. 2024. LLM Multi-Agent Systems: Challenges and Open Problems. arXiv:2402.03578 [cs.MA]](https://arxiv.org/abs/2402.03578)

[51] Kostas Hatalis et al. 2023. Memory Matters: The Need to Improve Long-Term Memory in LLM-Agents. In _Proceedings_
_of the AAAI Symposium Series_, Vol. 2. 277–280.

[52] Junda He, Christoph Treude, and David Lo. 2024. LLM-Based Multi-Agent Systems for Software Engineering: Vision
and the Road Ahead. _arXiv preprint arXiv:2404.04834_ (2024).

[53] Shawn He et al. 2024. Norm Violation Detection in Multi-Agent Systems using Large Language Models: A Pilot
[Study. arXiv:2403.16517 [cs.MA]](https://arxiv.org/abs/2403.16517)

[54] Zhitao He et al. 2023. LEGO: A Multi-agent Collaborative Framework with Role-playing and Iterative Feedback for
Causality Explanation Generation. In _Findings of the Association for Computational Linguistics: EMNLP 2023_, Houda
Bouamor, Juan Pino, and Kalika Bali (Eds.). Association for Computational Linguistics, Singapore, 9142–9163.


32 Tran et al.


[55] Jordan Hoffmann et al. 2024. Training compute-optimal large language models. In _Proceedings of the 36th International_
_Conference on Neural Information Processing Systems_ (New Orleans, LA, USA) _(NIPS ’22)_ . Curran Associates Inc., Red
Hook, NY, USA, Article 2176, 15 pages.

[56] Sirui Hong et al. 2024. MetaGPT: Meta Programming for A Multi-Agent Collaborative Framework. In _The Twelfth_
_International Conference on Learning Representations_ .

[57] Lei Huang et al. 2023. A survey on hallucination in large language models: Principles, taxonomy, challenges, and
open questions. _arXiv preprint arXiv:2311.05232_ (2023).

[58] Xu Huang et al. 2024. Understanding the planning of LLM agents: A survey. _arXiv preprint arXiv:2402.02716_ (2024).

[59] Yoichi Ishibashi and Yoshimasa Nishimura. 2024. Self-Organized Agents: A LLM Multi-Agent Framework toward
[Ultra Large-Scale Code Generation and Optimization. arXiv:2404.02183 [cs.SE]](https://arxiv.org/abs/2404.02183)

[60] Md. Ashraful Islam, Mohammed Eunus Ali, and Md Rizwan Parvez. 2024. MapCoder: Multi-Agent Code Generation
for Competitive Problem Solving. In _Proceedings of the Annual Meeting of the Association for Computational Linguistics_ .

[61] Shankar Kumar Jeyakumar, Alaa Alameer Ahmad, and Adrian Garret Gabriel. 2024. Advancing Agentic Systems:
Dynamic Task Decomposition, Tool Integration and Evaluation using Novel Metrics and Dataset. In _NeurIPS 2024_
_Workshop on Open-World Agents_ .

[62] Divyansh Jhunjhunwala, Shiqiang Wang, and Gauri Joshi. 2023. FedExP: Speeding Up Federated Averaging via
Extrapolation. In _The Eleventh International Conference on Learning Representations_ .

[63] Zhenlan Ji et al. 2024. Testing and Understanding Erroneous Planning in LLM Agents through Synthesized User
[Inputs. arXiv:2404.17833 [cs.AI]](https://arxiv.org/abs/2404.17833)

[64] Dongfu Jiang, Xiang Ren, and Bill Yuchen Lin. 2023. LLM-Blender: Ensembling Large Language Models with Pairwise
Ranking and Generative Fusion. In _Proceedings of the Annual Meeting of the Association for Computational Linguistics_ .

[65] Feibo Jiang et al. 2024. Large AI Model Empowered Multimodal Semantic Communications. _IEEE Communications_
_Magazine_ (2024), 1–7.

[66] Feibo Jiang et al. 2024. Large Language Model Enhanced Multi-Agent Systems for 6G Communications. _IEEE Wireless_
_Communications_ (2024), 1–8.

[67] Xue Jiang et al. 2024. Self-Planning Code Generation with Large Language Models. _ACM Trans. Softw. Eng. Methodol._
33, 7, Article 182 (Sept. 2024), 30 pages.

[68] Yogeswaranathan Kalyani and Rem Collier. 2024. The Role of Multi-Agents in Digital Twin Implementation: Short
Survey. _ACM Comput. Surv._ 57, 3, Article 72 (Nov. 2024), 15 pages.

[69] Jared Kaplan et al. 2020. Scaling laws for neural language models. _arXiv preprint arXiv:2001.08361_ (2020).

[70] Stefano Lambiase et al. 2024. Motivations, Challenges, Best Practices, and Benefits for Bots and Conversational
Agents in Software Engineering: A Multivocal Literature Review. _ACM Comput. Surv._ 57, 4, Article 93 (Dec. 2024),
37 pages.

[71] Jan Marco Leimeister. 2010. Collective Intelligence. _Business and Information Systems Engineering_ 2, 4 (June 2010),
245–248.

[72] Yaniv Leviathan, Matan Kalman, and Yossi Matias. 2023. Fast inference from transformers via speculative decoding.
In _International Conference on Machine Learning_ . PMLR, 19274–19286.

[73] Cheng Li et al. 2024. CulturePark: Boosting Cross-cultural Understanding in Large Language Models.
[arXiv:2405.15145 [cs.AI]](https://arxiv.org/abs/2405.15145)

[74] Guohao Li et al. 2023. CAMEL: Communicative Agents for ”Mind” Exploration of Large Language Model Society. In
_Thirty-seventh Conference on Neural Information Processing Systems_ .

[75] Huao Li et al. 2023. Theory of Mind for Multi-Agent Collaboration via Large Language Models. In _Proceedings of the_
_2023 Conference on Empirical Methods in Natural Language Processing_, Houda Bouamor, Juan Pino, and Kalika Bali
(Eds.). Association for Computational Linguistics, Singapore, 180–192.

[76] Junyi Li et al. 2024. Pre-Trained Language Models for Text Generation: A Survey. _ACM Comput. Surv._ 56, 9, Article
230 (April 2024), 39 pages.

[77] Tian Liang et al. 2024. Encouraging Divergent Thinking in Large Language Models through Multi-Agent Debate. In
_Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing_, Yaser Al-Onaizan, Mohit
Bansal, and Yun-Nung Chen (Eds.). Association for Computational Linguistics, Miami, Florida, USA, 17889–17904.

[78] Qiang Liu et al. 2024. LLM Enhanced Reconfigurable Intelligent Surface for Energy-Efficient and Reliable 6G IoV.
_IEEE Transactions on Vehicular Technology_ (2024), 1–9.

[79] Ryan Liu et al. 2024. Large Language Models Assume People are More Rational than We Really are.
[arXiv:2406.17055 [cs.CL]](https://arxiv.org/abs/2406.17055)

[80] Xiao Liu et al. 2024. AgentBench: Evaluating LLMs as Agents. In _The Twelfth International Conference on Learning_
_Representations_ .

[81] Zijun Liu et al. 2024. A Dynamic LLM-Powered Agent Network for Task-Oriented Agent Collaboration. In _First_
_Conference on Language Modeling_ .


Multi-Agent Collaboration Mechanisms: A Survey of LLMs 33


[82] Jinliang Lu et al. 2024. Merge, Ensemble, and Cooperate! A Survey on Collaborative Strategies in the Era of Large
[Language Models. arXiv:2407.06089 [cs.CL]](https://arxiv.org/abs/2407.06089)

[83] Zhao Mandi, Shreeya Jain, and Shuran Song. 2024. Roco: Dialectic multi-robot collaboration with large language
models. In _2024 IEEE International Conference on Robotics and Automation (ICRA)_ . IEEE, 286–299.

[[84] Alexander Meinke et al. 2024. Frontier Models are Capable of In-context Scheming. arXiv:2412.04984 [cs.AI]](https://arxiv.org/abs/2412.04984)

[85] Andres F. Mena-Guacas et al. 2023. Collaborative learning and skill development for educational growth of artificial
intelligence: A systematic review. _Contemporary Educational Technology_ 15, 3 (July 2023), ep428.

[86] Bonan Min et al. 2023. Recent Advances in Natural Language Processing via Large Pre-trained Language Models: A
Survey. _ACM Comput. Surv._ 56, 2, Article 30 (Sept. 2023), 40 pages.

[87] Marvin Minsky. 1988. _Society of mind_ . Simon and Schuster.

[88] Arindam Mitra et al. 2024. Agentinstruct: Toward generative teaching with agentic flows. _arXiv preprint_
_arXiv:2407.03502_ (2024).

[89] Xinyi Mou, Jingcong Liang, Jiayu Lin, Xinnong Zhang, Xiawei Liu, Shiyue Yang, Rong Ye, Lei Chen, Haoyu Kuang,
Xuanjing Huang, and Zhongyu Wei. 2024. AgentSense: Benchmarking Social Intelligence of Language Agents
[through Interactive Scenarios. arXiv:2410.19346 [cs.CL]](https://arxiv.org/abs/2410.19346)

[90] Yongan Mu et al. 2023. Runtime verification of self-adaptive multi-agent system using probabilistic timed automata.
_Journal of Intelligent & Fuzzy Systems_ 45, 6 (2023), 10305–10322.
