<!-- Source: 18-HallucinationSurvey-2509.18970.pdf | Chunk 4/8 -->




step, the agent assesses the validity, consistency, and factuality
of the intermediate decisions and actions generated in that specific step. This assessment helps prevent the accumulation and
propagation of hallucinations in long-horizon tasks. Existing
approaches can be broadly categorized into two types: **a) Self-**
**verification Mechanism**, in which the agent introspectively
reviews its own behaviors using an internal reasoning strategy
or prompt-based self-assessment. **b) Validator Assistance**,
which leverages another independent system to detect potential
flaws in the agent’s outputs.


_a) Self-verification Mechanism (SM)._ Self-verification is a
lightweight and model-internal approach wherein agents assess
the validity and reliability of their own outputs without relying
on external validators. It plays a crucial role in hallucination
mitigation [223], and several technical methods have been
explored to implement self-verification. Specifically, **Self-**
**reflection** enables agents to revisit and critique their own
outputs, often through prompting techniques that encourage
introspection and identification of reasoning flaws [89], [224],

[15], which can be further facilitated by estimating the
agent’s own confidence or uncertainty [225], [226], [50]. **Self-**
**consistency** leverages the generation of multiple candidate
outputs, such as diverse reasoning paths or answers, and
aggregates them using majority voting or confidence-weighted
schemes to select the most reliable results [177], [81], [78].
**Self-questioning** guides the agent to pose and answer critical
verification questions grounded in its own reasoning process,
enabling the detection of unsupported assertions [227], [228],

[74]. Collectively, these strategies establish a foundation for
autonomous error detection and correction, empowering agents
to self-regulate hallucination risks.


_b) Validator Assistance (VA)._ This approach leverages external
validators to verify the correctness of an agent’s outputs,
aiming to mitigate hallucinations [141], [142]. According to
the types of external validators, we divide existing methods
into the following five categories: **Language-based Valida-**
**tors** independently assess the truthfulness or coherence of
an agent’s outputs using techniques such as atomic fact


JOURNAL OF L [A] TEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021 12















































Fig. 4. A typology of methods of agent hallucination detection. We highlight the representative approaches for each type of agent hallucinations.



decomposition and entailment checking [229], [230], [231].
**Retrieval-based Validators** rely on some external sources
such as search engines to verify whether outputs aligns with
established facts [232]. **Execution-based Validators** evaluate
outputs by running generated codes or plans in external
execution environments, enabling direct assessment of correctness through functional outcomes [233]. **Simulation-based**
**Validators** validate agent behaviors through interaction with
sandboxed environments, allowing for realistic testing in tasks
involving embodiment, planning, or sequential control [234].
Building on these categories, an increasing number of studies have explored **Ensemble-based Validators** that integrate
multiple types of validators to improve robustness. By enabling
cross-verification among different approaches, these methods
help mitigate the limitations inherent in individual validation
strategies [78]. In the end, Table I summarizes which types
of agent hallucinations can be addressed by the ten listed
mitigation methods.


_B. Agent Hallucination Detection_


Based on the introduced taxonomy of agent hallucinations,
we summarize the existing detection methods in Fig. 4.
From it, we can observe that unlike the mitigation strategies
discussed above, research on agent hallucination detection
remains relatively limited. Among these detection methods,
those addressing perception hallucinations are relatively numerous, whereas methods on memorization hallucinations and



communication hallucinations are comparatively limited. We
believe this is because perception belongs to the shallow
layers of the agent, making hallucination detection and error
identification relatively straightforward, which explains the
larger amount of corresponding work. In contrast, memory
and communication are part of the deeper layers of the agent,
where the final outputs are coupled with computations from
numerous intermediate modules. This makes hallucination
detection and localization more challenging, and consequently,
there is comparatively less work in these areas.


V. FUTURE DIRECTIONS

LLM-based agent hallucinations represent an emerging research frontier that has attracted increasing attention from both
academia and industry. As discussed above, a substantial body
of work has focused on the mitigation and detection of agent
hallucinations. Building upon our established taxonomy and
existing literature, this survey introduces several promising
directions for future study.
_1) Hallucinatory Accumulation Investigation._ Most existing
studies investigate hallucination instances and their underlying
causes within a single agent loop. However, as we emphasize,
agent decision-making is inherently a multi-step and sequential
process, in which hallucinations can accumulate and amplify
over time. In such cases, hallucinations may initially appear
as minor issues, but their iterative accumulation can ultimately
lead to severe consequences. Compared to single-step scenarios, hallucination accumulation presents a significantly more


JOURNAL OF L [A] TEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021 13



complex challenge. Addressing it requires a comprehensive
analysis of the agent’s entire decision-making process, thereby
facilitating early hallucination detection and mitigation.
_2) Accurate Hallucinatory Location._ As previously mentioned,
in contrast to hallucinations in traditional language models
that are typically manifested in textual generation errors,
agent hallucinations are far more complex, involving full-chain
error propagation across multiple interdependent components.
While hallucination taxonomy and attribution we presented
in Section III have mapped these issues to specific modules
within the agent, promptly and accurately locate the source of
agent hallucinations in the final outputs remains a significant
challenge. This difficulty stems from the fact that agent
hallucinations may arise at any stage of the decision-making
pipeline and often exhibit complex characteristics such as
hallucinatory accumulation and inter-module dependency. In
fact, the limited amount of research on agent hallucination
detection in Section IV-B and the difficulty of conducting
such works are also related to this issue. Therefore, future
study should focus on designing agent systems capable of
modeling and tracing their entire execution trajectories [142].
For example, lightweight checkpoints can be injected at each
stage to verify whether hallucinations have occurred.
_3) Hallucination Mechanistic Interpretability._ Mechanistic interpretability (MI) seeks to uncover how hidden representations and internal components of neural networks give rise
to specific behaviors [270]. Therefore, MI provides a natural
pathway for diagnosing and mitigating hallucinations at the
root cause. Recent studies demonstrate that MI techniques,
such as feature analysis [271] and causal pathway tracing [272]
can reveal the internal sources of hallucinations in LLMs and
provide insights for mitigation. However, extending MI to
LLM-based agents introduces new challenges. Unlike LLMs,
where interpretability analysis is typically performed under
single-step prediction with controlled prompt–response settings, agent hallucinations emerge through multi-step sequential interactions involving reasoning, tool use, memorization,
and MAS communication. This dynamic process substantially
complicates the controlled interventions required for mechanistic analysis. Future research should therefore adapt MI
techniques to account for these dynamic and interconnected
processes, enabling more precise diagnosis and systematic
mitigation of agent hallucinations.
_4) Unified Benchmark Construction._ Existing benchmarks for
agent hallucinations are often limited to a specific hallucination type. For example, Guan et al. propose HALLUSIONBENCH to evaluate hallucination issues in visual-language
reasoning [273]; Hu et al. propose MemoryAgentBench to
evaluate hallucination issues in agents during memory retrieval
and update [274]; Zhang et al. introduce ToolBH to evaluate
execution hallucinations in tool use across different scenarios
from both depth and breadth perspectives [31]. Therefore,
there is a lack of a unified benchmark of hallucination
evaluation that can define diverse hallucination scenarios and
adopt various evaluation metrics to comprehensively assess
the extent of hallucinations in agents’ reasoning, execution,
perception, memory, and communication.
_5) Continual Self-evolution Capacity._ The analysis of agent



hallucinations is typically conducted under the assumption of
fixed user goals and static environments. However, in practice,
both user demands and environmental configurations evolve
continuously over time. To remain effective, agents must
possess continual self-evolution capabilities that allow them to
dynamically adapt to shifting goals and changing conditions.
Throughout this process, agents can consistently refine their
cognition to mitigate agent hallucinations stemming from outdated knowledge or delayed updates. Based on this important
need, integrating the lifelong learning paradigm [275] with
agents to endow them with more effective dynamic adaptation
capabilities represents a promising solution.
_6) Foundation Architecture Upgrade._ Current LLM-based
agents primarily rely on the Transformer architecture. However, this architecture faces challenges in handling longcontext information and suffers from high computational complexity, which have gradually revealed performance bottlenecks and contributed to the emergence of hallucination issues.
Recent works have explored more effective architectural upgrades, such as introducing linear-complexity modules [276]
as Transformer components, integrating neural-symbolic systems [277] to enhance model interpretability through symbolic
reasoning, and leveraging automated machine learning [278] to
design and compose optimal model architectures. In addition,
agents typically require a predefined workflow to organize the
execution of their various components. While this fixed pattern
enhances systematization and controllability, it also reduces
flexibility, resulting in limited adaptability and poor scalability.
Designing a dynamic self-scheduling agentic system [279]
that can autonomously organize task execution and coordinate
multi-agent collaboration is a critical direction for future
research.


VI. CONCLUSION


This paper presents a comprehensive survey of hallucination
issues in LLM-based agents, with the goal of consolidating past progress, clarifying current challenges, and outlining future opportunities. We begin by distinguishing agent
components into internal states and external behaviors, and,
from this perspective, propose a taxonomy of hallucination
types occurring at different stages. We then provide an indepth overview of each type and identify seventeen underlying
causes. Furthermore, we summarize ten general approaches for
hallucination mitigation, together with corresponding detection
methods. Finally, we discuss promising research directions
to guide future exploration in this rapidly evolving domain.
We believe this survey can serve as a valuable resource for
researchers and practitioners, inspiring and facilitating further
progress in the development of LLM-based agents.


REFERENCES


[1] Josh Achiam, Steven Adler, Sandhini Agarwal, Lama Ahmad, Ilge
Akkaya, Florencia Leoni Aleman, Diogo Almeida, Janko Altenschmidt,
Sam Altman, Shyamal Anadkat, et al. Gpt-4 technical report. _arXiv_
_preprint arXiv:2303.08774_, 2023.

[2] Hugo Touvron, Thibaut Lavril, Gautier Izacard, Xavier Martinet,
Marie-Anne Lachaux, Timoth´ee Lacroix, Baptiste Rozi`ere, Naman
Goyal, Eric Hambro, Faisal Azhar, et al. Llama: Open and efficient
foundation language models. _arXiv preprint arXiv:2302.13971_, 2023.


JOURNAL OF L [A] TEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021 14




[3] Hugo Touvron, Louis Martin, Kevin Stone, Peter Albert, Amjad Almahairi, Yasmine Babaei, Nikolay Bashlykov, Soumya Batra, Prajjwal
Bhargava, Shruti Bhosale, et al. Llama 2: Open foundation and finetuned chat models. _arXiv preprint arXiv:2307.09288_, 2023.

[4] Aaron Grattafiori, Abhimanyu Dubey, Abhinav Jauhri, Abhinav Pandey,
Abhishek Kadian, Ahmad Al-Dahle, Aiesha Letman, Akhil Mathur,
Alan Schelten, Alex Vaughan, et al. The llama 3 herd of models.
_arXiv preprint arXiv:2407.21783_, 2024.

[5] Daya Guo, Dejian Yang, Haowei Zhang, Junxiao Song, Ruoyu Zhang,
Runxin Xu, Qihao Zhu, Shirong Ma, Peiyi Wang, Xiao Bi, et al.
Deepseek-r1: Incentivizing reasoning capability in llms via reinforcement learning. _arXiv preprint arXiv:2501.12948_, 2025.

[6] Bailin Wang, Zi Wang, Xuezhi Wang, Yuan Cao, Rif A Saurous, and
Yoon Kim. Grammar prompting for domain-specific language generation with large language models. _Advances in Neural Information_
_Processing Systems_, 36:65030–65055, 2023.

[7] Mingyang Geng, Shangwen Wang, Dezun Dong, Haotian Wang, Ge Li,
Zhi Jin, Xiaoguang Mao, and Xiangke Liao. Large language models
are few-shot summarizers: Multi-intent comment generation via incontext learning. In _Proceedings of the 46th IEEE/ACM International_
_Conference on Software Engineering_, pages 1–13, 2024.

[8] Linhao Luo, Yuan-Fang Li, Gholamreza Haffari, and Shirui Pan.
Reasoning on graphs: Faithful and interpretable large language model
reasoning. _arXiv preprint arXiv:2310.01061_, 2023.

[9] Yue Yu, Yuchen Zhuang, Jieyu Zhang, Yu Meng, Alexander J Ratner,
Ranjay Krishna, Jiaming Shen, and Chao Zhang. Large language
model as attributed training data generator: A tale of diversity and bias.
_Advances in Neural Information Processing Systems_, 36:55734–55784,
2023.

[10] Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion
Jones, Aidan N Gomez, Łukasz Kaiser, and Illia Polosukhin. Attention
is all you need. _Advances in neural information processing systems_,
30, 2017.

[11] Jason Wei, Yi Tay, Rishi Bommasani, Colin Raffel, Barret Zoph,
Sebastian Borgeaud, Dani Yogatama, Maarten Bosma, Denny Zhou,
Donald Metzler, et al. Emergent abilities of large language models.
_arXiv preprint arXiv:2206.07682_, 2022.

[12] Shayne Longpre, Le Hou, Tu Vu, Albert Webson, Hyung Won Chung,
Yi Tay, Denny Zhou, Quoc V Le, Barret Zoph, Jason Wei, et al. The
flan collection: Designing data and methods for effective instruction
tuning. In _International Conference on Machine Learning_, pages
22631–22648. PMLR, 2023.

[13] Qingxiu Dong, Lei Li, Damai Dai, Ce Zheng, Jingyuan Ma, Rui Li,
Heming Xia, Jingjing Xu, Zhiyong Wu, Tianyu Liu, et al. A survey
on in-context learning. _arXiv preprint arXiv:2301.00234_, 2022.

[14] Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik
Narasimhan, and Yuan Cao. React: Synergizing reasoning and acting
in language models. In _International Conference on Learning Repre-_
_sentations (ICLR)_, 2023.

[15] Noah Shinn, Federico Cassano, Ashwin Gopinath, Karthik Narasimhan,
and Shunyu Yao. Reflexion: Language agents with verbal reinforcement learning. _Advances in Neural Information Processing Systems_,
36:8634–8652, 2023.

[16] Zehui Chen, Kuikun Liu, Qiuchen Wang, Wenwei Zhang, Jiangning
Liu, Dahua Lin, Kai Chen, and Feng Zhao. Agent-flan: Designing
data and methods of effective agent tuning for large language models.
_arXiv preprint arXiv:2403.12881_, 2024.

[17] Xixi Wu, Yifei Shen, Caihua Shan, Kaitao Song, Siwei Wang, Bohang
Zhang, Jiarui Feng, Hong Cheng, Wei Chen, Yun Xiong, and Dongsheng Li. Can graph learning improve planning in llm-based agents?
In _Proceedings of Neural Information Processing Systems_, 2024.

[18] Lei Wang, Chen Ma, Xueyang Feng, Zeyu Zhang, Hao Yang, Jingsen
Zhang, Zhiyuan Chen, Jiakai Tang, Xu Chen, Yankai Lin, et al. A
survey on large language model based autonomous agents. _Frontiers_
_of Computer Science_, 18(6):186345, 2024.

[19] Ben Goertzel. Artificial general intelligence: concept, state of the art,
and future prospects. _Journal of Artificial General Intelligence_, 5(1):1,
2014.

[20] Joon Sung Park, Joseph O’Brien, Carrie Jun Cai, Meredith Ringel
Morris, Percy Liang, and Michael S Bernstein. Generative agents:
Interactive simulacra of human behavior. In _Proceedings of the 36th_
_annual acm symposium on user interface software and technology_,
pages 1–22, 2023.

[21] Guohao Li, Hasan Hammoud, Hani Itani, Dmitrii Khizbullin, and
Bernard Ghanem. Camel: Communicative agents for” mind” exploration of large language model society. _Advances in Neural Information_
_Processing Systems_, 36:51991–52008, 2023.




[22] Sirui Hong, Mingchen Zhuge, Jonathan Chen, Xiawu Zheng, Yuheng
Cheng, Jinlin Wang, Ceyao Zhang, Zili Wang, Steven Ka Shing Yau,
Zijuan Lin, Liyang Zhou, Chenyu Ran, Lingfeng Xiao, Chenglin
Wu, and J¨urgen Schmidhuber. MetaGPT: Meta programming for a
multi-agent collaborative framework. In _The Twelfth International_
_Conference on Learning Representations_, 2024.

[23] Chi-Min Chan, Weize Chen, Yusheng Su, Jianxuan Yu, Wei Xue,
Shanghang Zhang, Jie Fu, and Zhiyuan Liu. Chateval: Towards
better llm-based evaluators through multi-agent debate. _arXiv preprint_
_arXiv:2308.07201_, 2023.

[24] Taicheng Guo, Xiuying Chen, Yaqi Wang, Ruidi Chang, Shichao Pei,
Nitesh V Chawla, Olaf Wiest, and Xiangliang Zhang. Large language
model based multi-agents: A survey of progress and challenges. _arXiv_
_preprint arXiv:2402.01680_, 2024.

[25] Yanwen Ba, Xuan Liu, Xinning Chen, Hao Wang, Yang Xu, Kenli
Li, and Shigeng Zhang. Cautiously-optimistic knowledge sharing for
cooperative multi-agent reinforcement learning. In _Proceedings of the_
_AAAI Conference on Artificial Intelligence_, volume 38, pages 17299–
17307, 2024.

[26] Kunlun Zhu, Hongyi Du, Zhaochen Hong, Xiaocheng Yang, Shuyi
Guo, Zhe Wang, Zhenhailong Wang, Cheng Qian, Xiangru Tang, Heng
Ji, et al. Multiagentbench: Evaluating the collaboration and competition
of llm agents. _arXiv preprint arXiv:2503.01935_, 2025.

[27] Zhexin Zhang, Shiyao Cui, Yida Lu, Jingzhuo Zhou, Junxiao Yang,
Hongning Wang, and Minlie Huang. Agent-safetybench: Evaluating
the safety of llm agents. _arXiv preprint arXiv:2412.14470_, 2024.

[28] Tongxin Yuan, Zhiwei He, Lingzhong Dong, Yiming Wang, Ruijie
Zhao, Tian Xia, Lizhen Xu, Binglin Zhou, Fangqi Li, Zhuosheng
Zhang, et al. R-judge: Benchmarking safety risk awareness for llm
agents. _arXiv preprint arXiv:2401.10019_, 2024.

[29] Yu Tian, Xiao Yang, Jingyuan Zhang, Yinpeng Dong, and Hang Su.
Evil geniuses: Delving into the safety of llm-based agents. _arXiv_
_preprint arXiv:2311.11855_, 2023.

[30] Bang Liu, Xinfeng Li, Jiayi Zhang, Jinlin Wang, Tanjin He, Sirui
Hong, Hongzhang Liu, Shaokun Zhang, Kaitao Song, Kunlun Zhu,
et al. Advances and challenges in foundation agents: From braininspired intelligence to evolutionary, collaborative, and safe systems.
_arXiv preprint arXiv:2504.01990_, 2025.

[31] Yuxiang Zhang, Jing Chen, Junjie Wang, Yaxin Liu, Cheng Yang,
Chufan Shi, Xinyu Zhu, Zihao Lin, Hanwen Wan, Yujiu Yang, Tetsuya
Sakai, Tian Feng, and Hayato Yamana. Toolbehonest: A multi-level
hallucination diagnostic benchmark for tool-augmented large language
models. In _Proceedings of the 2024 Conference on Empirical Methods_
_in Natural Language Processing, EMNLP 2024, Miami, FL, USA,_
_November 12-16, 2024_, pages 11388–11422, 2024.

[32] Zehang Deng, Yongjian Guo, Changzhou Han, Wanlun Ma, Junwu
Xiong, Sheng Wen, and Yang Xiang. Ai agents under threat: A survey
of key security challenges and future pathways. _ACM Computing_
_Surveys_, 57(7):1–36, 2025.

[33] Ziwei Ji, Nayeon Lee, Rita Frieske, Tiezheng Yu, Dan Su, Yan Xu,
Etsuko Ishii, Ye Jin Bang, Andrea Madotto, and Pascale Fung. Survey
of hallucination in natural language generation. _ACM computing_
_surveys_, 55(12):1–38, 2023.

[34] Lei Huang, Weijiang Yu, Weitao Ma, Weihong Zhong, Zhangyin Feng,
Haotian Wang, Qianglong Chen, Weihua Peng, Xiaocheng Feng, Bing
Qin, et al. A survey on hallucination in large language models: Principles, taxonomy, challenges, and open questions. _ACM Transactions_
_on Information Systems_, 43(2):1–55, 2025.

[35] Sewon Min, Kalpesh Krishna, Xinxi Lyu, Mike Lewis, Wen-tau Yih,
Pang Wei Koh, Mohit Iyyer, Luke Zettlemoyer, and Hannaneh Hajishirzi. Factscore: Fine-grained atomic evaluation of factual precision
in long form text generation. _arXiv preprint arXiv:2305.14251_, 2023.

[36] Alexander R Fabbri, Chien-Sheng Wu, Wenhao Liu, and Caiming
Xiong. Qafacteval: Improved qa-based factual consistency evaluation
for summarization. _arXiv preprint arXiv:2112.08542_, 2021.

[37] Sheng Liu, Haotian Ye, and James Zou. Reducing hallucinations in
large vision-language models via latent space steering. In _The Thir-_
_teenth International Conference on Learning Representations_, 2025.

[38] Zhiheng Xi, Wenxiang Chen, Xin Guo, Wei He, Yiwen Ding, Boyang
Hong, Ming Zhang, Junzhe Wang, Senjie Jin, Enyu Zhou, et al. The
rise and potential of large language model based agents: A survey.
_Science China Information Sciences_, 68(2):121101, 2025.

[39] Karl Johan ˚Astr¨om. Optimal control of markov processes with
incomplete state information i. _Journal of mathematical analysis and_
_applications_, 10:174–205, 1965.

[40] Pengfei Cao, Tianyi Men, Wencan Liu, Jingwen Zhang, Xuzhao Li,
Xixun Lin, Dianbo Sui, Yanan Cao, Kang Liu, and Jun Zhao. Large


JOURNAL OF L [A] TEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021 15



language models for planning: A comprehensive and systematic survey.
_arXiv preprint arXiv:2505.19683_, 2025.

[41] Gaole He, Gianluca Demartini, and Ujwal Gadiraju. Plan-then-execute:
An empirical study of user trust and team performance when using llm
agents as a daily assistant. In _Proceedings of the 2025 CHI Conference_
_on Human Factors in Computing Systems_, pages 1–22, 2025.

[42] Zhuosheng Zhang, Yao Yao, Aston Zhang, Xiangru Tang, Xinbei Ma,
Zhiwei He, Yiming Wang, Mark Gerstein, Rui Wang, Gongshen Liu,
et al. Igniting language intelligence: The hitchhiker’s guide from chainof-thought reasoning to language agents. _ACM Computing Surveys_,
57(8):1–39, 2025.

[43] Ranjan Sapkota, Konstantinos I Roumeliotis, and Manoj Karkee. Ai
agents vs. agentic ai: A conceptual taxonomy, applications and challenge. _arXiv preprint arXiv:2505.10468_, 2025.

[44] Xuanming Zhang, Yuxuan Chen, Min-Hsuan Yeh, and Yixuan Li.
Metamind: Modeling human social thoughts with metacognitive multiagent systems. _arXiv preprint arXiv:2505.18943_, 2025.

[45] Shen Zheng, Jie Huang, and Kevin Chen-Chuan Chang. Why does
chatgpt fall short in providing truthful answers? _arXiv preprint_
_arXiv:2304.10513_, 2023.

[46] Sergey Linok, Tatiana Zemskova, Svetlana Ladanova, Roman Titkov,
Dmitry Yudin, Maxim Monastyrny, and Aleksei Valenkov. Beyond bare
queries: Open-vocabulary object grounding with 3d scene graph. _arXiv_
_preprint arXiv:2406.07113_, 2024.
