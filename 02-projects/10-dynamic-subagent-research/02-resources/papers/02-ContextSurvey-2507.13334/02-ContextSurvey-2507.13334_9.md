<!-- Source: 02-ContextSurvey-2507.13334.pdf | Chunk 9/26 -->

must be addressed while preserving interoperability and functionality. Research must develop defense
mechanisms and detection systems that address evolving threat landscapes across distributed agent networks

[250, 934].


Alignment and value specification challenges require investigation into methods for ensuring context
engineering systems behave according to intended objectives while avoiding specification gaming, reward
hacking, and goal misalignment. Context engineering systems present unique alignment challenges due to
their dynamic adaptation capabilities and complex interaction patterns across multiple components. The
substantial performance gaps revealed by evaluation frameworks underscore the importance of developing
robust alignment mechanisms that can maintain beneficial behaviors as systems evolve and adapt [778, 128].


_**7.4.3. Ethical Considerations and Responsible Development**_


Bias mitigation and fairness evaluation require comprehensive assessment frameworks that can identify and
address systematic biases across different demographic groups, application domains, and use cases while
maintaining system performance and utility. Research must investigate bias sources in training data, model
architectures, and deployment contexts while developing mitigation strategies that address root causes
rather than symptoms [1141, 841].


Privacy protection mechanisms must address challenges in handling sensitive information, preventing data
leakage, and maintaining user privacy while enabling beneficial system capabilities. Memory systems face
particular privacy challenges due to their persistent information storage and retrieval capabilities, requiring
advanced frameworks for secure memory management and selective forgetting mechanisms [1340, 463].


Transparency and accountability frameworks require development of explanation systems, audit mechanisms, and governance structures that enable responsible oversight of context engineering systems while
supporting innovation and beneficial applications. The substantial performance gaps revealed by evaluation frameworks like GAIA (human 92% vs AI 15%) highlight the importance of transparent capability
communication and appropriate expectation setting for deployed systems [778, 1098].


57


The future of Context Engineering will be shaped by our ability to address these interconnected challenges
through sustained, collaborative research efforts that bridge technical innovation with societal considerations.


Success will require continued investment in fundamental research, interdisciplinary collaboration,
and responsible development practices that ensure context engineering systems remain beneficial, reliable,
and aligned with human values as they become increasingly integrated into critical societal functions

[841, 1141, 314].

##### **8. Conclusion**


This survey has presented the first comprehensive examination of Context Engineering as a formal discipline
that systematically designs, optimizes, and manages information payloads for LLMs. Through our analysis of
over 1400 research papers, we have established Context Engineering as a critical foundation for developing
sophisticated AI systems that effectively integrate external knowledge, maintain persistent memory, and
interact dynamically with complex environments.


Our primary contribution lies in introducing a unified taxonomic framework that organizes context
engineering techniques into **Foundational Components** (Context Retrieval and Generation, Context Processing, and Context Management) and **System Implementations** (Retrieval-Augmented Generation, Memory
Systems, Tool-Integrated Reasoning, and Multi-Agent Systems). This framework demonstrates how core
technical capabilities integrate into sophisticated architectures addressing real-world requirements.


Through this systematic examination, we have identified several key insights. First, we observe a
fundamental asymmetry between LLMs’ remarkable capabilities in understanding complex contexts and
their limitations in generating equally sophisticated outputs. This comprehension-generation gap represents
one of the most critical challenges facing the field. Second, our analysis reveals increasingly sophisticated
integration patterns where multiple techniques combine synergistically, creating capabilities that exceed
their individual components. Third, we observe a clear trend toward modularity and compositionality,
enabling flexible architectures adaptable to diverse applications while maintaining system coherence. The
evaluation challenges we identified underscore the need for comprehensive assessment frameworks that
capture the complex, dynamic behaviors exhibited by context-engineered systems. Traditional evaluation
methodologies prove insufficient for systems that integrate multiple components, exhibit adaptive behaviors,
and operate across extended time horizons. Our examination of future research directions reveals significant
opportunities including developing next-generation architectures for efficient long context handling, creating
intelligent context assembly systems, and advancing multi-agent coordination mechanisms. Key challenges
span theoretical foundations, technical implementation, and practical deployment, including the lack of
unified theoretical frameworks, scaling limitations, and safety considerations.


Looking toward the future, Context Engineering stands poised to play an increasingly central role in AI
development as the field moves toward complex, multi-component systems. The interdisciplinary nature of
Context Engineering necessitates collaborative research approaches spanning computer science, cognitive
science, linguistics, and domain-specific expertise.


As LLMs continue to evolve, the fundamental insight underlying Context Engineering—that AI system
performance is fundamentally determined by contextual information—will remain central to artificial
intelligence development. This survey provides both a comprehensive snapshot of the current state and a
roadmap for future research, establishing Context Engineering as a distinct discipline with its own principles,
methodologies, and challenges to foster innovation and support responsible development of context-aware
AI systems.


58


##### **Acknowledgments**

This survey represents an ongoing effort to comprehensively map the rapidly evolving landscape of Context
Engineering for Large Language Models. Given the dynamic nature of this field, with new developments
emerging continuously, we acknowledge that despite our best efforts, some recent works or emerging trends
may have been inadvertently overlooked or underrepresented. We welcome feedback from the research
community to help improve future iterations of this work. We are grateful to the broader research community
whose foundational contributions have made this survey possible. This work would not have been achievable
without the invaluable support of both the research community and the open-source community, whose
collaborative efforts in developing frameworks, tools, and resources have significantly advanced the field of
Context Engineering. We extend special gratitude to the teams behind the Long Chain-of-Thought [149] and
AI4Research [151] projects for their excellent template designs and visualizations, which have significantly
enhanced the presentation quality of this survey. Their thoughtful contributions to the research community
are deeply appreciated.

##### **References**


[1] Anp-agent communication meta-protocol specification(draft). [https://](https://agent-network-protocol.com/specs/communication.html)
[agent-network-protocol.com/specs/communication.html.](https://agent-network-protocol.com/specs/communication.html) [Online; accessed 17July-2025].


[2] S. A. Automating human evaluation of dialogue systems. _North American Chapter of the Association_
_for Computational Linguistics_, 2022.


[3] Samir Abdaljalil, Hasan Kurban, Khalid A. Qaraqe, and E. Serpedin. Theorem-of-thought: A multiagent framework for abductive, deductive, and inductive reasoning in language models. arXiv
preprint, 2025.


[4] Abdelrahman Abdallah, Bhawna Piryani, Jamshid Mozafari, Mohammed Ali, and Adam Jatowt.
Rankify: A comprehensive python toolkit for retrieval, re-ranking, and retrieval-augmented genera[tion, arXiv preprint arXiv:2502.02464, 2025. URL https://arxiv.org/abs/2502.02464v3.](https://arxiv.org/abs/2502.02464v3)


[5] Ibrahim Abdelaziz, Kinjal Basu, Mayank Agarwal, Sadhana Kumaravel, Matt Stallone, Rameswar
Panda, Yara Rizk, G. Bhargav, M. Crouse, Chulaka Gunasekara, S. Ikbal, Sachin Joshi, Hima P.
Karanam, Vineet Kumar, Asim Munawar, S. Neelam, Dinesh Raghu, Udit Sharma, Adriana Meza
Soria, Dheeraj Sreedhar, P. Venkateswaran, Merve Unuvar, David Cox, S. Roukos, Luis A. Lastras, and
P. Kapanipathi. Granite-function calling model: Introducing function calling abilities via multi-task
learning of granular tasks. _Conference on Empirical Methods in Natural Language Processing_, 2024.


[6] D. Acharya, Karthigeyan Kuppan, and Divya Bhaskaracharya. Agentic ai: Autonomous intelligence
for complex goals—a comprehensive survey. _IEEE Access_, 2025.


[7] Manoj Acharya, Kushal Kafle, and Christopher Kanan. Tallyqa: Answering complex counting
questions. _AAAI Conference on Artificial Intelligence_, 2018.


[8] Shantanu Acharya, Fei Jia, and Boris Ginsburg. Star attention: Efficient llm inference over
[long sequences, arXiv preprint arXiv:2411.17116, 2024. URL https://arxiv.org/abs/2411.](https://arxiv.org/abs/2411.17116v3)
[17116v3.](https://arxiv.org/abs/2411.17116v3)


59


[9] Emre Can Acikgoz, Jeremy Greer, Akul Datta, Ze Yang, William Zeng, Oussama Elachqar, Emmanouil
Koukoumidis, Dilek Hakkani-Tur, and Gokhan Tur. Can a single model master both multi-turn
conversations and tool use? coalm: A unified conversational agentic language model, arXiv preprint
[arXiv:2502.08820, 2025. URL https://arxiv.org/abs/2502.08820v3.](https://arxiv.org/abs/2502.08820v3)


[10] Emre Can Acikgoz, Cheng Qian, Hongru Wang, Vardhan Dongre, Xiusi Chen, Heng Ji, Dilek HakkaniTur, and Gokhan Tur. A desideratum for conversational agents: Capabilities, challenges, and
[future directions, arXiv preprint arXiv:2504.16939, 2025. URL https://arxiv.org/abs/2504.](https://arxiv.org/abs/2504.16939v1)
[16939v1.](https://arxiv.org/abs/2504.16939v1)


[11] Anum Afzal, Juraj Vladika, Gentrit Fazlija, Andrei Staradubets, and Florian Matthes. Towards optimizing a retrieval augmented generation using large language model on academic data. _International_
_Conference on Natural Language Processing and Information Retrieval_, 2024.


[12] Ankush Agarwal, Sakharam Gawade, A. Azad, and P. Bhattacharyya. Kitlm: Domain-specific
knowledge integration into language models for question answering. _ICON_, 2023.


[13] Oshin Agarwal, Heming Ge, Siamak Shakeri, and Rami Al-Rfou. Large scale knowledge graph based
synthetic corpus generation for knowledge-enhanced language model pre-training. arXiv preprint,
2020.


[14] Monica Agrawal, S. Hegselmann, Hunter Lang, Yoon Kim, and D. Sontag. Large language models
are few-shot clinical information extractors. _Conference on Empirical Methods in Natural Language_
_Processing_, 2022.


[15] Arash Ahmadi, S. Sharif, and Yaser Mohammadi Banadaki. Mcp bridge: A lightweight, llm-agnostic
restful proxy for model context protocol servers, arXiv preprint arXiv:2504.08999, 2025. URL
[https://arxiv.org/abs/2504.08999v1.](https://arxiv.org/abs/2504.08999v1)


[16] J. Ainslie, J. Lee-Thorp, Michiel de Jong, Yury Zemlyanskiy, Federico Lebr’on, and Sumit K. Sanghai.
Gqa: Training generalized multi-query transformer models from multi-head checkpoints. _Conference_
_on Empirical Methods in Natural Language Processing_, 2023.


[17] Adel Al-Jumaily. Multi-agent system concepts theory and application phases. arXiv preprint, 2006.


[18] Faisal Al-Khateeb, Nolan Dey, Daria Soboleva, and Joel Hestness. Position interpolation improves
alibi extrapolation. arXiv preprint, 2023.


[19] Jean-Baptiste Alayrac, Jeff Donahue, Pauline Luc, Antoine Miech, Iain Barr, Yana Hasson, Karel Lenc,
A. Mensch, Katie Millican, Malcolm Reynolds, Roman Ring, Eliza Rutherford, Serkan Cabi, Tengda
Han, Zhitao Gong, Sina Samangooei, Marianne Monteiro, Jacob Menick, Sebastian Borgeaud, Andy
Brock, Aida Nematzadeh, Sahand Sharifzadeh, Mikolaj Binkowski, Ricardo Barreira, O. Vinyals,
Andrew Zisserman, and K. Simonyan. Flamingo: a visual language model for few-shot learning.
_Neural Information Processing Systems_, 2022.


[20] Stefano V. Albrecht and P. Stone. Autonomous agents modelling other agents: A comprehensive
survey and open problems. _Artificial Intelligence_, 2017.


[21] Buthayna AlMulla, Maram Assi, and Safwat Hassan. Understanding the challenges and promises of
developing generative ai apps: An empirical study, arXiv preprint arXiv:2506.16453, 2025. URL
[https://arxiv.org/abs/2506.16453v2.](https://arxiv.org/abs/2506.16453v2)


60


[22] Reem S. Alsuhaibani, Christian D. Newman, M. J. Decker, Michael L. Collard, and Jonathan I. Maletic.
On the naming of methods: A survey of professional developers. _International Conference on Software_
_Engineering_, 2021.


[23] Francesco Alzetta, P. Giorgini, A. Najjar, M. Schumacher, and Davide Calvaresi. In-time explainability
in multi-agent systems: Challenges, opportunities, and roadmap. _EXTRAAMAS@AAMAS_, 2020.


[24] Kenza Amara, Lukas Klein, Carsten T. Lüth, Paul F. Jäger, Hendrik Strobelt, and Mennatallah ElAssady. Why context matters in vqa and reasoning: Semantic interventions for vlm input modalities,
[arXiv preprint arXiv:2410.01690v1, 2024. URL https://arxiv.org/abs/2410.01690v1.](https://arxiv.org/abs/2410.01690v1)


[25] Xavier Amatriain. Prompt design and engineering: Introduction and advanced methods, arXiv
[preprint arXiv:2401.14423, 2024. URL https://arxiv.org/abs/2401.14423v4.](https://arxiv.org/abs/2401.14423v4)


[26] Zahra Aminiranjbar, Jianan Tang, Qiudan Wang, Shubha Pant, and Mahesh Viswanathan. Dawn:
Designing distributed agents in a worldwide network, arXiv preprint arXiv:2410.22339, 2024. URL
[https://arxiv.org/abs/2410.22339v3.](https://arxiv.org/abs/2410.22339v3)


[27] Chenxin An, Jun Zhang, Ming Zhong, Lei Li, Shansan Gong, Yao Luo, Jingjing Xu, and Lingpeng
Kong. Why does the effective context length of llms fall short? _International Conference on Learning_
_Representations_, 2024.


[28] Kaikai An, Fangkai Yang, Liqun Li, Junting Lu, Sitao Cheng, Shuzheng Si, Lu Wang, Pu Zhao, Lele
Cao, Qingwei Lin, et al. Thread: A logic-based data organization paradigm for how-to question
answering with retrieval augmented generation. _arXiv preprint arXiv:2406.13372_, 2024.


[29] Kaikai An, Fangkai Yang, Junting Lu, Liqun Li, Zhixing Ren, Hao Huang, Lu Wang, Pu Zhao, Yu Kang,
Hua Ding, et al. Nissist: An incident mitigation copilot based on troubleshooting guides. In
_Proceedings of the 27th European Conference on Artificial Intelligence (ECAI 2024)_, pages 4471–4474,
2024.


[30] Kaikai An, Li Sheng, Ganqu Cui, Shuzheng Si, Ning Ding, Yu Cheng, and Baobao Chang. Ultraif:
Advancing instruction following from the wild. pages 7930–7957, 2025.


[31] Sumin An, Junyoung Sung, Wonpyo Park, Chanjun Park, and Paul Hongsuck Seo. Lcirc: A recurrent
compression approach for efficient long-form context and query dependent modeling in llms. _North_
_American Chapter of the Association for Computational Linguistics_, 2025.


[32] Sotiris Anagnostidis, Dario Pavllo, Luca Biggio, Lorenzo Noci, Aurélien Lucchi, and Thomas Hofmann. Dynamic context pruning for efficient and interpretable autoregressive transformers. _Neural_
_Information Processing Systems_, 2023.


[33] John R. Anderson, M. Matessa, and C. Lebiere. Act-r: A theory of higher level cognition and its
relation to visual attention. _Hum. Comput. Interact._, 1997.


[34] Jacob Andreas. Language models as agent models. _Conference on Empirical Methods in Natural_
_Language Processing_, 2022.


[35] Leonardo Aniello, R. Baldoni, and Leonardo Querzoni. Adaptive online scheduling in storm. _Dis-_
_tributed Event-Based Systems_, 2013.


61


[36] Petr Anokhin, Nikita Semenov, Artyom Sorokin, Dmitry Evseev, M. Burtsev, and Evgeny Burnaev.
Arigraph: Learning knowledge graph world models with episodic memory for llm agents, arXiv
[preprint arXiv:2407.04363, 2024. URL https://arxiv.org/abs/2407.04363v3.](https://arxiv.org/abs/2407.04363v3)


[37] Anthropic. Introducing the model context protocol, November 2024. [URL https://www.](https://www.anthropic.com/news/model-context-protocol)
[anthropic.com/news/model-context-protocol. [Online; accessed 17-July-2025].](https://www.anthropic.com/news/model-context-protocol)


[38] RM Aratchige and Dr. Wmks Ilmini. Llms working in harmony: A survey on the technological aspects
of building effective llm-based multi agent systems, arXiv preprint arXiv:2504.01963, 2025. URL
[https://arxiv.org/abs/2504.01963v1.](https://arxiv.org/abs/2504.01963v1)


[39] Leo Ardon, Daniel Furelos-Blanco, and A. Russo. Learning reward machines in cooperative multiagent tasks. _AAMAS Workshops_, 2023.


[40] K. Armeni, C. Honey, and Tal Linzen. Characterizing verbatim short-term memory in neural language
models. _Conference on Computational Natural Language Learning_, 2022.


[41] Akari Asai, Zeqiu Wu, Yizhong Wang, Avirup Sil, and Hannaneh Hajishirzi. Self-rag: Learning
to retrieve, generate, and critique through self-reflection. _International Conference on Learning_
_Representations_, 2023.


[42] Hikaru Asano, Tadashi Kozuno, and Yukino Baba. Self iterative label refinement via robust unla[beled learning, arXiv preprint arXiv:2502.12565, 2025. URL https://arxiv.org/abs/2502.](https://arxiv.org/abs/2502.12565v1)
[12565v1.](https://arxiv.org/abs/2502.12565v1)


[43] Ben Athiwaratkun, Sujan Kumar Gonugondla, Sanjay Krishna Gouda, Haifeng Qian, Hantian Ding,
Qing Sun, Jun Wang, Jiacheng Guo, Liangfu Chen, Parminder Bhatia, Ramesh Nallapati, Sudipta
Sengupta, and Bing Xiang. Bifurcated attention: Accelerating massively parallel decoding with
[shared prefixes in llms, arXiv preprint arXiv:2403.08845, 2024. URL https://arxiv.org/abs/](https://arxiv.org/abs/2403.08845v2)
[2403.08845v2.](https://arxiv.org/abs/2403.08845v2)


[44] Avinash Ayalasomayajula, Rui Guo, Jingbo Zhou, Sujan Kumar Saha, and Farimah Farahmandi. Lasp:
Llm assisted security property generation for soc verification. _Workshop on Machine Learning for_
_CAD_, 2024.


[45] Simon A. Aytes, Jinheon Baek, and Sung Ju Hwang. Sketch-of-thought: Efficient llm reasoning with
adaptive cognitive-inspired sketching. arXiv preprint, 2025.


[46] Bobby Azad, Reza Azad, Sania Eskandari, Afshin Bozorgpour, A. Kazerouni, I. Rekik, and D. Merhof.
Foundational models in medical imaging: A comprehensive survey and future vision, arXiv preprint
[arXiv:2310.18689, 2023. URL https://arxiv.org/abs/2310.18689v1.](https://arxiv.org/abs/2310.18689v1)


[47] Gilbert Badaro, Mohammed Saeed, and Paolo Papotti. Transformers for tabular data representation:
A survey of models and applications. _Transactions of the Association for Computational Linguistics_,
2023.


[48] Jinheon Baek, N. Chandrasekaran, Silviu Cucerzan, Allen Herring, and S. Jauhar. Knowledgeaugmented large language models for personalized contextual query suggestion. _The Web Conference_,
2023.


62


[49] Tianyi Bai, Hao Liang, Binwang Wan, Ling Yang, Bozhou Li, Yifan Wang, Bin Cui, Conghui He,
Binhang Yuan, and Wentao Zhang. A survey of multimodal large language model from a data-centric
[perspective, arXiv preprint arXiv:2405.16640v2, 2024. URL https://arxiv.org/abs/2405.](https://arxiv.org/abs/2405.16640v2)
[16640v2.](https://arxiv.org/abs/2405.16640v2)


[50] Yu Bai, Xiyuan Zou, Heyan Huang, Sanxing Chen, Marc-Antoine Rondeau, Yang Gao, and Jackie
Chi Kit Cheung. Citrus: Chunked instruction-aware state eviction for long sequence modeling.
_Conference on Empirical Methods in Natural Language Processing_, 2024.


[51] Yuntao Bai, Saurav Kadavath, Sandipan Kundu, Amanda Askell, Jackson Kernion, Andy Jones,
Anna Chen, Anna Goldie, Azalia Mirhoseini, Cameron McKinnon, Carol Chen, Catherine Olsson,
Christopher Olah, Danny Hernandez, Dawn Drain, Deep Ganguli, Dustin Li, Eli Tran-Johnson,
Ethan Perez, Jamie Kerr, Jared Mueller, Jeffrey Ladish, Joshua Landau, Kamal Ndousse, Kamile
Lukosuite, Liane Lovitt, Michael Sellitto, Nelson Elhage, Nicholas Schiefer, Noemi Mercado, Nova
DasSarma, Robert Lasenby, Robin Larson, Sam Ringer, Scott Johnston, Shauna Kravec, Sheer El
Showk, Stanislav Fort, Tamera Lanham, Timothy Telleen-Lawton, Tom Conerly, Tom Henighan,
Tristan Hume, Samuel R. Bowman, Zac Hatfield-Dodds, Ben Mann, Dario Amodei, Nicholas Joseph,
Sam McCandlish, Tom Brown, and Jared Kaplan. Constitutional ai: Harmlessness from ai feedback,
[arXiv preprint arXiv:2212.08073, 2022. URL https://arxiv.org/abs/2212.08073.](https://arxiv.org/abs/2212.08073)


[52] Souhail Bakkali, Sanket Biswas, Zuheng Ming, Mickaël Coustaty, Marccal Rusinol, O. R. Terrades,
and Josep Llad’os. Globaldoc: A cross-modal vision-language framework for real-world document
image retrieval and classification. _IEEE Workshop/Winter Conference on Applications of Computer_
_Vision_, 2023.


[53] Jayachandu Bandlamudi, K. Mukherjee, Prerna Agarwal, Sampath Dechu, Siyu Huo, Vatche Isahagian,
Vinod Muthusamy, N. Purushothaman, and Renuka Sindhgatta. Towards hybrid automation by
bootstrapping conversational interfaces for it operation tasks. _AAAI Conference on Artificial Intelligence_,
2023.


[54] Jayachandu Bandlamudi, Kushal Mukherjee, Prerna Agarwal, Ritwik Chaudhuri, R. Pimplikar,
Sampath Dechu, Alex Straley, Anbumunee Ponniah, and Renuka Sindhgatta. Building conversational
artifacts to enable digital assistant for apis and rpas. _AAAI Conference on Artificial Intelligence_, 2024.


[55] Keqin Bao, Jizhi Zhang, Xinyu Lin, Yang Zhang, Wenjie Wang, and Fuli Feng. Large language models
for recommendation: Past, present, and future. _Annual International ACM SIGIR Conference on_
_Research and Development in Information Retrieval_, 2024.


[56] Sara Di Bartolomeo, Giorgio Severi, V. Schetinger, and Cody Dunne. Ask and you shall receive
(a graph drawing): Testing chatgpt’s potential to apply graph layout algorithms. _Eurographics_
_Conference on Visualization_, 2023.


[57] Saikat Barua. Exploring autonomous agents through the lens of large language models: A review,
[arXiv preprint arXiv:2404.04442, 2024. URL https://arxiv.org/abs/2404.04442v1.](https://arxiv.org/abs/2404.04442v1)


[58] Kinjal Basu, Ibrahim Abdelaziz, Kelsey Bradford, M. Crouse, Kiran Kate, Sadhana Kumaravel, Saurabh
Goyal, Asim Munawar, Yara Rizk, Xin Wang, Luis A. Lastras, and P. Kapanipathi. Nestful: A benchmark
for evaluating llms on nested sequences of api calls, arXiv preprint arXiv:2409.03797, 2024. URL
[https://arxiv.org/abs/2409.03797v3.](https://arxiv.org/abs/2409.03797v3)


63


[59] Amin Beheshti. Natural language-oriented programming (nlop): Towards democratizing software
creation. _2024 IEEE International Conference on Software Services Engineering (SSE)_, 2024.


[60] Azadeh Beiranvand and S. M. Vahidipour. Integrating structural and semantic signals in text[attributed graphs with bigtex, arXiv preprint arXiv:2504.12474, 2025. URL https://arxiv.org/](https://arxiv.org/abs/2504.12474v2)
[abs/2504.12474v2.](https://arxiv.org/abs/2504.12474v2)


[61] Assaf Ben-Kish, Itamar Zimerman, Shady Abu-Hussein, Nadav Cohen, Amir Globerson, Lior Wolf,
and Raja Giryes. Decimamba: Exploring the length extrapolation potential of mamba. _International_
_Conference on Learning Representations_, 2024.


[62] Assaf Ben-Kish, Itamar Zimerman, M. J. Mirza, James R. Glass, Leonid Karlinsky, and Raja Giryes.
Overflow prevention enhances long-context recurrent llms. arXiv preprint, 2025.


[63] M. Benna and Stefano Fusi. Complex synapses as efficient memory systems. _BMC Neuroscience_,
2015.


[64] M. Benna and Stefano Fusi. Computational principles of biological memory, arXiv preprint
[arXiv:1507.07580, 2015. URL https://arxiv.org/abs/1507.07580v1.](https://arxiv.org/abs/1507.07580v1)


[65] Shelly Bensal, Umar Jamil, Christopher Bryant, M. Russak, Kiran Kamble, Dmytro Mozolevskyi,
Muayad Ali, and Waseem Alshikh. Reflect, retry, reward: Self-improving llms via reinforcement learn[ing, arXiv preprint arXiv:2505.24726, 2025. URL https://arxiv.org/abs/2505.24726v1.](https://arxiv.org/abs/2505.24726v1)


[66] Idoia Berges, J. Bermúdez, A. Goñi, and A. Illarramendi. Semantic web technology for agent
communication protocols. _Extended Semantic Web Conference_, 2008.


[67] Gaurav Beri and Vaishnavi Srivastava. Advanced techniques in prompt engineering for large language
models: A comprehensive study. _2024 IEEE 4th International Conference on ICT in Business Industry_
_& Government (ICTBIG)_, 2024.


[68] Amanda Bertsch, Uri Alon, Graham Neubig, and Matthew R. Gormley. Unlimiformer: Long-range
transformers with unlimited length input. _Neural Information Processing Systems_, 2023.


[69] Maciej Besta, Nils Blach, Aleš Kubíček, Robert Gerstenberger, Lukas Gianinazzi, Joanna Gajda,
Tomasz Lehmann, Michal Podstawski, H. Niewiadomski, P. Nyczyk, and Torsten Hoefler. Graph of
thoughts: Solving elaborate problems with large language models. _AAAI Conference on Artificial_
_Intelligence_, 2023.


[70] Gregor Betz and Kyle Richardson. Judgment aggregation, discursive dilemma and reflective equilibrium: Neural language models as self-improving doxastic agents. _Frontiers in Artificial Intelligence_,
2022.


[71] L. Bezalel, Eyal Orgad, and Amir Globerson. Teaching models to improve on tape. _AAAI Conference_
_on Artificial Intelligence_, 2024.


[72] Umang Bhatt, Sanyam Kapoor, Mihir Upadhyay, Ilia Sucholutsky, Francesco Quinzan, Katherine M.
Collins, Adrian Weller, Andrew Gordon Wilson, and Muhammad Bilal Zafar. When should we
[orchestrate multiple agents?, arXiv preprint arXiv:2503.13577, 2025. URL https://arxiv.org/](https://arxiv.org/abs/2503.13577v1)
[abs/2503.13577v1.](https://arxiv.org/abs/2503.13577v1)


64


[73] Baolong Bi, Shaohan Huang, Yiwei Wang, Tianchi Yang, Zihan Zhang, Haizhen Huang, Lingrui
Mei, Junfeng Fang, Zehao Li, Furu Wei, et al. Context-dpo: Aligning language models for contextfaithfulness. _ACL 2025_, 2024.


[74] Baolong Bi, Shenghua Liu, Lingrui Mei, Yiwei Wang, Pengliang Ji, and Xueqi Cheng. Decoding by
contrasting knowledge: Enhancing llms’ confidence on edited facts. _ACL 2025_, 2024.


[75] Baolong Bi, Shenghua Liu, Yiwei Wang, Lingrui Mei, and Xueqi Cheng. Lpnl: Scalable link prediction
with large language models. _ACL 2024_, 2024.


[76] Baolong Bi, Shenghua Liu, Yiwei Wang, Lingrui Mei, Hongcheng Gao, Junfeng Fang, and Xueqi
Cheng. Struedit: Structured outputs enable the fast and accurate knowledge editing for large
language models. 2024.


[77] Baolong Bi, Shenghua Liu, Yiwei Wang, Lingrui Mei, Hongcheng Gao, Yilong Xu, and Xueqi Cheng.
Adaptive token biaser: Knowledge editing via biasing key entities. _EMNLP 2024_, 2024.

