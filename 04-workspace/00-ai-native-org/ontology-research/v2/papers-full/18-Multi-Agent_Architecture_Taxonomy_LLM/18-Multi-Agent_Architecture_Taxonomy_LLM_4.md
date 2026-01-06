<!-- Source: 18-Multi-Agent_Architecture_Taxonomy_LLM.pdf | Chunk 4/4 -->

Based on our taxonomic classification and the resulting system profiles as illustrated in Fig. 9, we can categorize
the selected 7 systems under analysis into three distinct system groups, which encompass general-purpose
systems, central-controller systems, and role-agent systems. It’s important to note that our categorization
into these three groups, based on the systems chosen for this exploration, doesn’t capture the entire spectrum
of autonomous LLM-powered multi-agent systems. For a comprehensive overview of existing systems and
system categories, we recommend referring to the recent surveys provided by [84, 95]. In the following, the
key characteristics as observed from the corresponding system profiles are discussed.


    - **General-Purpose Systems**     - representing multi-agent systems designed for and adaptable to a
broad spectrum of tasks and applications. Within the analyzed set of multi-agent systems, the
following fall into this group: AUTO-GPT [77], BABYAGI [51], SUPERAGI [79], and AGENTGPT

[71]. Goals are decomposed autonomously and represented as prioritized task lists (L2 `Decom` ).
They employ a multi-cycle process framework performed by dedicated task-management agents
represented by certain generic agent types, including a single task-execution agent (see Section 3.2).


30


Relations and communications between these agents are strictly predefined, and agent conversations
express as a monologue of the task-execution agent, resulting in low autonomy levels (L0) for
communication protocol ( `CommP` ), and network management ( `NetM` ). The task-related actions are
performed autonomously by the task-execution agent (mostly L2 autonomy `ActM` ). while resource
integration is based on provided mechanisms ( `Integ` ), the resources are selected and utilized by the
LLM-powered in a self-organizing manner (L2 autonomy for `Util` ), except for CAMEL; resulting
in similar autonomy profiles for the aforementioned aspects. Besides from these commonalities,
these systems distinguish in certain characteristics. Both AUTO-GPT and BABYAGI employ generic
task-execution agent, and provide no further alignment options at all. Moreover, these systems
employ a generic task-execution agent with predefined agent roles and relations, reulting in L0
autonomy for `AGen` and `NetM` . In contrast, SUPERAGI and AGENTGPT employ execution agents
with self-organizing agent roles (L2 autonomy for `RoleD` ), an adaptable orchestration process (L1 for
`Orch` ), and some alignment options, especially for agent-specific aspects. Moreover, these systems
employ execution agents, whose roles can be customized by the user (L1 alignment for `AGen` ).

    - **Central LLM Controller**     - marks a third group specialized in leveraging and combining contextual
resources for accomplishing the complex goals. HUGGINGGPT [70] serves as an archetype of such
systems, utilizing resources especially in terms of existing ML models integrated via HUGGING FACE.
As already detailed in Section 5.1, HUGGINGGPT is characterized by a single central LLM-powered
control agent with monologue-based reflection and planning. Language in terms of agent prompts
as generic interface to manage the interplay between multiple specialized foundation models. In
comparison to other systems or system groups, we see the highest levels of autonomy granted to
this central agent (mostly L2); also see Fig. 9 (d). Furthermore, we see a finite and artefact-oriented
process adaptable by the LLM-powered agent for orchestrating the different model-related tasks (L1
autonomy). As already stated above, beyond prompting the task, there are no further user-centric
alignment options (L0 alignment).

    - **Role-Agent Systems**     - employ an interplay or simulation between multiple dedicated roles agents.
This collaboration can serve different purposes, such as simulating a discussion or solving tasks that
demand for a multi-perspective collaboration. With defined roles in a certain environment (such as
in a software development project), their application is bound to this application domain or special
purpose. Among the analyzed systems, METAGPT [28] and CAMEL [41] represent such systems. In
contrast to the general-purpose systems, the execution agents play roles with dedicated responsibilities
in a certain application domain. Furthermore, these role agents actually collaborate directly with
each other. In case of the two exemplary systems, this collaboration is realized by communication
protocols employing a dynamic exchange between agents with instructor and executor roles. In
particular, CAMEL employs two such role agents based on predefined agent types, but adjustable by
the user. In ongoing strict dialogue cycles, the AI-user role agents instructs the AI-assistant role agent
to execute the tasks (L0 autonomy for `CommP` ). Similar to SUPERAGI, CAMEL requires the user to
specify the agents’ roles (L1 alignment). METAGPT, in contrast, internally assigns predefined roles
with responsibilities alongside a waterfall development process (L0 alignment); thus, also expressing
a finite and artefact-oriented process (L0 autonomy for `Orch` ), terminating with the produced and
tested software program. However, like in real-world software project, refinement iterations can
follow, optional feedback cycles make it adaptable for the agents (L1 autonomy for `CommP` ).


**Strategy Assessment.** Beyond differences in the applied communication protocols, it is the flexibility of
agent roles (in relation to both autonomy and alignment) and further customization options for agent-specific
aspects that distinguishes the systems’ strategies (see above). However, when examining how the systems
deal with autonomy and alignment across further aspects, most systems and system groups show similar
strategies. The reasoning capabilities of LLM-powered agents are especially leveraged in areas demanding
high autonomy, such as the goal decomposition, the actual execution of task-related actions, and the utilization
of contextual resources. Interestingly, these high-autonomy aspects are mostly combined with low alignment
levels, resulting in _bounded autonomy_ aspects (refer to Table 1). A closer look at aspect interdependencies, as
depicted in Fig. 8, reveals that these internally _unbalanced_ aspects are accompanied by other low-autonomy
aspects equipped with limited flexibility, as follows:


   - Autonomous decomposition directly depends on the user-prompted goal.

   - Autonomous action management depends on strict or predefined communication protocol.

    - Autonomous resource utilization depends on strict or predefined resource integration.


In these cases, the predefined and rule-based mechanisms serve as integrated alignment guiding and controlling
the accurate operation of the dependent autonomous aspects.


31


Based on the findings of the taxonomic classification, in the next Section 6, we discuss challenges for current
systems and reflect on the taxonomy’s limitations and potentials.


**6** **Discussion**


This paper introduces and applies a novel comprehensive taxonomy, shedding light on the ways autonomous
LLM-powered multi-agent systems manage the dynamic interplay between autonomy and alignment within
their architectures. When interpreted through the lens of our taxonomy, we encounter challenges and development potentials for current LLM-powered multi-agent systems, which are discussed in Section 6.1. Moreover,
in Section 6.2, we reflect on limitations and further potentials of the taxonomy itself.


**6.1** **Challenges for Current Systems**


Our analysis of architectural dynamics inherent to current LLM-powered multi-agent systems, as detailed
in Section 5, reveals a number of challenges regarding the interplay between autonomy and alignment. In
accordance with [84], we recognize challenges related to the adaptability of agent collaboration. Moreover,
our exploration indicates potentials for user-centric alignment options and controlling high-autonomy aspects.


**Agent Collaboration.** Among the systems analyzed, we especially observe limitations regarding collaboration
modes and role-playing capabilities, as well as risks tied to prompt-driven collaboration techniques.


    - **Adaptability of Communication Protocols:** As discussed in Section 5.2, the collaboration between agents is mainly characterized by restricted communication protocols between predefined
task-execution agents, such as instructor-and-executor relationships, or sequential or multi-cycle
processes with predefined execution chains. Employing LLM-powered agents to manage and adapt
the constellation of the agent network as well as their collaboration modes could pave the way for
more creative problem-solving methods in task execution.


    - **Dynamic Role-Playing:** In particular, we also see development potentials via the flexible collaboration between self-organizing role agents, such as for simulating the complex interplay within a
certain application domain. As far as observable, the potential of engaging multiple perspectives
through different roles and standpoints has not yet been fully sounded.


    - **Robustness of Prompt-driven Collaboration:** Collaboration between LLM-powered agents basically relies on prompt-driven message exchange, such as by delegating tasks, asking questions,
or evaluating task results. This communication mechanism, founded on a sequence of prompts,
heavily relies on the quality of LLM responses, which are susceptible to errors in terms of incorrect
or hallucinated results [45, 30]. However, without the integration of comprehensive and robust
control mechanisms to check the quality of these responses, the system is vulnerable to inaccuracies,
misunderstandings, and inefficiencies [28].


**User-Centric Alignment.** Within the scope of analyzed systems, user-centric alignment options are very rare.
Alignment mechanisms are predominantly integrated into the system architecture (see Section 5.2). Drawing
from this limitation, we see potentials in certain user-guided and real-time responsive alignment options.


    - **User-Guided Alignment Options:** The options for users to access and influence the internal workings
of the system are very limited. The internal composition and collaboration of the agents are mostly
opaque to the user, which reduces transparency of the system operation. Exception to this represents
the runtime documentation of agents’ reflection and planning, provided by certain systems (see
Section 5.1). The customization of internal mechanisms is mostly not provided to users. Besides
agent generation and role definition (offered by a few systems), there is potential for user modifications
related to communication protocols, task orchestration, or result synthesis. Corresponding to the
aspect adaptability for LLM-powered agents (see above), modifying these internal mechanisms would
enable the user in exploring alternative problem-solving ways.


    - **Real-Time Responsiveness:** The obvious lack of real-time adjustment capabilities can be seen
founded in the nature of autonomous agent systems, which is accomplishing the user-prompted
goal without further human intervention. However, as elaborated on in Section 4, autonomy and
alignment can be understood as complementary aspects. The absence of user interaction and control
during runtime restricts the potential for dynamic alignment, thereby limiting the system’s flexibility
in response to changes in the operational context. As detailed in Section 4.1.2, the interaction


32


layer allows the integration of interceptor mechanisms. This not only allows real-time monitoring,
addressing key concerns of explainable AI [63, 96], but also to implement effective feedback and
intervention options [40, 27]. Collaborative environments fostering _hybrid teamwork_, comprising
autonomous agents (or agents systems) and human co-workers are essentially built upon such realtime responsiveness, ensuring dynamic realignment while working towards shared goals [34, 54, 89].


**Controlling High-Autonomy Aspects.** Besides prompting-related flaws such as inaccurate or hallucinated
responses (see above), our engagement with the analyzed multi-agent systems has revealed additional operational issues. Occasionally, we witness non-terminating activities, where the system falls into infinite loops.
For instance, this can manifest via solutions continually fine-tuned under the premise of improvement, or the
system operation is stuck in a never ending dialogue between two LLM-powered agents. Conversely, system
operations might terminate in a dead end when encountering a task that requires competencies or resources that
are either unavailable or inaccessible. Obviously, the corresponding control mechanisms ( _integrated alignment_ )
applied in such systems are ill-equipped to efficiently catch these kinds of exceptions. This insufficiency proves
particularly concerning, as it undermines the reliability and effectiveness of these systems. However, besides
this symptomatic treatment, the reasons for these problems can be seen founded in architectural complexities,
such as high-autonomy levels not adequately aligned or intertwined dependencies resulting from varying levels
of autonomy (refer to Section 4.2.2).


**6.2** **Limitations and Potentials of the Taxonomy**


For engineering the taxonomic system, we chose a pragmatic and technical perspective (see Section 4) and
explored its utility by the exemplary classification of seven selected LLM-powered multi-agent systems (see
Section 5). However, departing from this exploration, certain limitations and further potentials become evident.


**Taxonomic System.** Our taxonomy conceptualizes autonomy and alignment not as binary extremes in a
one-dimensional continuum, but as interacting and synergistic aspects. This distinctions allows forming a
two-dimensional matrix (see Section 4) combining hierarchic levels of autonomy (from automated mechanisms
to self-organizing agents) and alignment (from system-integrated to real-time responsive). This structure
reflects the aforementioned triadic relationship between the key decision-making entities in the system (i.e.,
human users, rules and mechanisms, as well as LLM-powered agents) and their dynamic interplay (i.e.,
alignment, system operation, and collaboration), as illustrated in Fig. 3. Augmenting this, we map this matrix
onto different characteristic aspects derived from four applied architectural viewpoints (see Section 4.2).


    - **Autonomy Scope:** Within this, we reference high autonomy to the agents’ self-organization capabilities for decision-making and further operational impact (see Section 4.1.1). However, it’s essential to
consider that autonomy can span beyond this definition, encompassing facets like an agent’s ability
for self-enhancement and proactive agency.


    - **Alignment Scope:** In turn, the alignment dimension employed by the taxonomy reflects two key
aspects, i.e., the _origin_ of the alignment, and the _moment_ of its communication to the system (see
Section 4.1.2). In combination with the architectural dimension, we also reflect the _architectural or_
_functional scope_ of the alignment technique in terms of the viewpoint-specific aspects. However, one
must note that this dimension does not reflect the quality, efficacy, or depth of the applied techniques.


    - **Scope of Architectural Aspects:** As detailed in Section 4.3, the taxonomy adopts 12 architectural
aspects inherent to the four architectural viewpoints characteristic for LLM-powered multi-agent
systems. The viewpoints are oriented to Kruchten’s viewpoint model for software architecture [38], a
recognized standard in this field. However, as there exist more viewpoint models reflecting further
concerns and perspectives on software systems, there might also be further architectural aspects
possibly relevant to autonomous LLM-powered multi-agent systems. Considering the ongoing
evolution in the field, these adaptions become crucial.


**Expressiveness of Taxonomic Classification.** The scope of the taxonomic structure forms the foundation for
the taxonomy’s analytical power enabling conclusions about the classified systems under analysis.


    - **Levels as Strengths and Weaknesses:** It is important to understand that higher levels in autonomy
and alignment, termed as _user-responsive autonomy_ (see Table 1), might not always be the optimal
system configuration for every scenario. Indeed, high autonomy can deviate from the intended goal
and therefore needs to be aligned accordingly. In certain situations, a system with modest autonomy
could be considered the best choice. Given the intention to automate a repetitive set of routine tasks


33


with predictable variables and contextual requirements, a static autonomy with predefined rules and
mechanisms would not be just sufficient, but also provide a higher reliability. If there is no need to
include user-specific information, a combination with an integrated alignment can be seen as best
choice ( _rule-driven automation_ ).

    - **System Efficiency and Accuracy:** As previously elaborated, our taxonomy focuses on the architectural complexities driven by the dynamics between autonomy and alignment, rather than evaluating
functional performance metrics like operational efficiency or accuracy. Neither recent surveys in
the field [84, 30] do measure the systems’ performance, such as in terms of efficiency, accuracy, or
scalability. However, while engaging with the analyzed systems, we observed substantial differences
among them, reflecting the exploratory state and the ongoing rapid evolution of the domain. For
measuring their functional performance, benchmarks and methods could be adopted similar to those
presented in [13].

    - **Balancing Techniques:** As reported in Section 5.2, we have identified different balancing strategies
across the system architectures. In this context, it is important to notice that aspects marked as
_unbalanced_ (for example, combining high-autonomy and low-alignment levels) might be actually
controlled or balanced via automated mechanisms applied by another aspect (static autonomy and
integrated alignment). Within the analyzed systems, user-centric alignment options are barely applied
to curb the wildness of high-autonomy aspects. It would be interesting, to investigate and compare in
detail, how integrated alignment techniques are employed to deal with the challenges and complexities
of agent-driven autonomy.


**Practical Implications.** Drawing from the information value provided by the classification results, we can
distinguish considerations regarding the practical utility and relevance of the taxonomy.


    - **Analysis Purposes:** The analysis and understanding of these dynamic architectural complexities can
serve different purposes, such as:

**–** Comparing, selecting, and applying available multi-agent systems in the context of given
scenarios with certain requirements for autonomy and alignment.

**–** Reasoning about architectural design options for the development of novel multi-agent systems.

**–** Scrutinizing and rethinking strategies for balancing levels of autonomy and alignment.

**–** Building a foundational framework for additional analysis techniques or complementing them,
such as measuring the functional system capabilities (see above).

    - **Ongoing Evolution:** As underscored by recent surveys [84, 95], the field of autonomous LLMpowered multi-agent systems is characterized by an ongoing rapid evolution showcasing a dynamically
growing number of approaches featuring diverse architectures and a wide spectrum of system-maturity
levels. While designed to abstract from concrete system specifics, the taxonomic system might need
periodic updates to accommodate this dynamically evolving landscape.

    - **Broader Applicability.** Tailored to address the characteristics of autonomous LLM-powered multiagent architectures (refer to Section 3), the foundational principles of our taxonomy, however, seem
to be transferable to other AI systems. Certain segments of the taxonomic structure can be seen
as universally applicable across AI architectures. Conversely, facets specifically tailored to multiagent systems, such as the aspects inherent to the agent composition and multi-agent collaboration
viewpoints, would require corresponding adjustments.


**7** **Conclusion**


In this paper, we have introduced a comprehensive multi-dimensional taxonomy engineered to analyze how autonomous LLM-powered multi-agent systems balance the dynamic interplay between autonomy and alignment
across their system architectures. For this purpose, the taxonomy employs a matrix that combines hierarchical
levels of autonomy and alignment. This matrix is then mapped onto various architectural aspects organized
by four architectural viewpoints reflecting different complementary concerns and perspectives. The resulting
taxonomic system enables the assessment of interdependent aspect configurations in a wide spectrum, ranging
from simple configurations, such as predefined mechanisms combined with system-integrated alignment
techniques ( _rule-driven automation_ ), to sophisticated configurations, such as self-organizing agency responsive
to user feedback and evolving conditions ( _user-responsive autonomy_ ). Applied to 12 distinct architectural
aspects inherent to viewpoints, such as goal-driven task management, multi-agent collaboration, agent composition, and context interaction, this taxonomy allows for a nuanced analysis and understanding of architectural
complexities within autonomous LLM-powered multi-agent systems.


34


Through our taxonomy’s application to seven selected LLM-powered multi-agent systems, its practical
relevance and utility has been illustrated. In particular, it has been shown that a combined assessment
of autonomy and alignment levels across the architectural aspects of each multi-agent system allows for
identifying system profiles that can indicate certain strategies for balancing the dynamic interplay between
autonomy and alignment. This exploration of exemplary current systems also revealed several challenges.
Most prominently, we observed a lack of user-centric alignment options across all systems, with little userguided alignment, but no real-time responsive alignment at all. Moreover, the systems exhibit high autonomy
levels mostly for certain aspects, such as the goal decomposition, the action management, or the utilization of
contextual resources. In contrast, other key aspects of the system operation show limited autonomy; aspects
such as managing the communication protocol, memory usage, or agent network are largely static, leaning
heavily on predefined mechanisms.


Based on these and further findings, we especially see two promising avenues for the evolution of autonomous
LLM-powered multi-agent systems. Firstly, by employing adaptable and self-organizing communication
protocols and agent networks, the systems’ role-playing capabilities could be enhances, which enables them to
better simulate complex multi-perspective environments. By reflecting and weighing up diverse standpoints
and strategies, this could also pave the way for more in-depth inter-agent discussions and creativity in problem
solving. Secondly, the exploration of real-time responsive systems, which can adapt to evolving conditions as
well as to user feedback during runtime, would foster dynamic collaboration and hybrid teamwork between
LLM-powered agents and human users.


Departing from an exploratory stage, the field of autonomous LLM-powered multi-agent systems is rapidly
evolving, resulting in a growing number of promising approaches and innovative architectures. With their
current capabilities and inherent potentials, such as multi-perspective domain simulations or collaborative
environments of autonomous agents and human coworkers, these systems could significantly contribute to
the progression towards advanced stages of artificial intelligence, such as AGI or ASI. From a pragmatic
perspective, there are numerous opportunities for combining LLMs as general purpose technology with
the specifics of various application domains. LLM-based multi-agent systems can serve as foundation for
developing corresponding domain-specific application layers. The architectural complexities resulting from the
dynamic interplay between autonomy and alignment can be seen as one of the key challenges in such systems.
By providing a systematic framework for analyzing these complexities, our taxonomy aims to contribute to
these ongoing efforts.


For our subsequent endeavors, we aim at developing a comprehensive overview and comparison of existing
autonomous LLM-powered multi-agent systems, complementing existing literature reviews in the field [84, 95].
To this end, we intend to analyze and classify available systems using our taxonomy. The identified system
profiles and balancing strategies resulting from this analysis will then be combined with further investigations
of functional system capabilities. In addition, driven by the potentials identified during the taxonomic
classification of selected systems, we currently explore the development of an LLM-powered multi-agent
system that aims at combining high levels of agency with real-time user-centric control mechanisms.


Building on the foundation of our taxonomy, future initiatives could venture into the following areas: A
dedicated exploration, assessment, and systematization of alignment techniques, particularly tailored for
LLM-based interaction and application layers, could serve as reference for future systems. Moreover, the
conception of a methodological framework with instruments and benchmarks for measuring the functional
capabilities of LLM-powered multi-agent systems could provide a structured template to evaluate key metrics
like efficiency, accuracy, and scalability of these systems.


**Acknowledgements**


The author gratefully acknowledges the support from the "Gesellschaft für Forschungsförderung (GFF)" of
Lower Austria, as this research was conducted at Ferdinand Porsche Mobile University of Applied Sciences
(FERNFH) as part of the "Digital Transformation Hub" project funded by the GFF.


35


**References**


[1] D. Amodei, C. Olah, J. Steinhardt, P. Christiano, J. Schulman, and D. Mané. Concrete problems in AI
safety. _arXiv preprint arXiv:1606.06565_, 2016.


[2] A. B. Arrieta, N. Díaz-Rodríguez, J. Del Ser, A. Bennetot, S. Tabik, A. Barbado, S. García, S. GilLópez, D. Molina, R. Benjamins, et al. Explainable artificial intelligence (XAI): Concepts, taxonomies,
opportunities and challenges toward responsible AI. _Information fusion_, 58:82–115, 2020.


[3] A. Askell, Y. Bai, A. Chen, D. Drain, D. Ganguli, T. Henighan, A. Jones, N. Joseph, B. Mann,
N. DasSarma, et al. A general language assistant as a laboratory for alignment. _arXiv preprint_
_arXiv:2112.00861_, 2021.


[4] L. Bass, P. Clements, and R. Kazman. _Software architecture in practice_ . Addison-Wesley Professional,
2003.


[5] D. Batory. Feature models, grammars, and propositional formulas. In _9th International Software_
_Product Line Conference_, pages 7–20, 2005.


[6] J. M. Beer, A. D. Fisk, and W. A. Rogers. Toward a framework for levels of robot autonomy in
human-robot interaction. _Journal of human-robot interaction_, 3(2):74, 2014.


[7] S. D. Bird. Toward a taxonomy of multi-agent systems. _International Journal of Man-Machine Studies_,
39(4):689–704, 1993.


[8] B. W. Boehm and P. N. Papaccio. Understanding and controlling software costs. _IEEE transactions on_
_software engineering_, 14(10):1462–1477, 1988.


[9] R. Bommasani, D. A. Hudson, E. Adeli, R. Altman, S. Arora, S. von Arx, M. S. Bernstein, J. Bohg,
A. Bosselut, E. Brunskill, et al. On the opportunities and risks of foundation models. _arXiv preprint_
_arXiv:2108.07258_, 2021.


[10] N. Bostrom. _Superintelligence_ . Dunod, 2017.


[11] T. Brown, B. Mann, N. Ryder, M. Subbiah, J. D. Kaplan, P. Dhariwal, A. Neelakantan, P. Shyam,
G. Sastry, A. Askell, et al. Language models are few-shot learners. _Advances in neural information_
_processing systems_, 33:1877–1901, 2020.


[12] J. C. Brustoloni. _Autonomous agents: Characterization and requirements_ . Carnegie Mellon University,
1991.


[13] S. Bubeck, V. Chandrasekaran, R. Eldan, J. Gehrke, E. Horvitz, E. Kamar, P. Lee, Y. T. Lee, Y. Li,
S. Lundberg, et al. Sparks of artificial general intelligence: Early experiments with GPT-4. _arXiv_
_preprint arXiv:2303.12712_, 2023.


[14] H. Chase. LangChain. `[https://github.com/langchain-ai/langchain](https://github.com/langchain-ai/langchain)`, 2022.


[15] A. Chowdhery, S. Narang, J. Devlin, M. Bosma, G. Mishra, A. Roberts, P. Barham, H. W. Chung,
C. Sutton, S. Gehrmann, et al. Palm: Scaling language modeling with pathways. _arXiv preprint_
_arXiv:2204.02311_, 2022.


[16] P. Clements, D. Garlan, R. Little, R. Nord, and J. Stafford. Documenting software architectures: views
and beyond. In _25th International Conference on Software Engineering, 2003. Proceedings._, pages
740–741. IEEE, 2003.


[17] L. M. Csepregi. The effect of context-aware LLM-based NPC conversations on player engagement in
role-playing video games. 2023.


[18] Y. Du, S. Li, A. Torralba, J. B. Tenenbaum, and I. Mordatch. Improving factuality and reasoning in
language models through multiagent debate. _arXiv preprint arXiv:2305.14325_, 2023.


[19] G. Dudek, M. R. Jenkin, E. Milios, and D. Wilkes. A taxonomy for multi-agent robotics. _Autonomous_
_Robots_, 3:375–397, 1996.


[20] F. Fabiano, V. Pallagani, M. B. Ganapini, L. Horesh, A. Loreggia, K. Murugesan, F. Rossi, and
B. Srivastava. Fast and slow planning. _arXiv preprint arXiv:2303.04283_, 2023.


[21] S. Franklin and A. Graesser. Is it an agent, or just a program?: A taxonomy for autonomous agents. In
_International workshop on agent theories, architectures, and languages_, pages 21–35. Springer, 1996.

[22] C. Gao, X. Lan, Z. Lu, J. Mao, J. Piao, H. Wang, D. Jin, and Y. Li. S [3] : Social-network simulation
system with large language model-empowered agents. _arXiv preprint arXiv:2307.14984_, 2023.


36


[23] T. R. Gruber. Toward principles for the design of ontologies used for knowledge sharing? _International_
_journal of human-computer studies_, 43(5-6):907–928, 1995.

[24] G. Guizzardi, H. Herre, and G. Wagner. On the general ontological foundations of conceptual modeling.
In _Conceptual Modeling—ER 2002: 21st International Conference on Conceptual Modeling Tampere,_
_Finland, October 7–11, 2002 Proceedings 21_, pages 65–78. Springer, 2002.

[25] T. Haendler and G. Neumann. Ontology-based analysis and design of educational games for software refactoring. In _Computer Supported Education: 11th International Conference, CSEDU 2019,_
_Heraklion, Crete, Greece, May 2-4, 2019, Revised Selected Papers_, pages 602–628. Springer, 2020.

[26] R. Hao, L. Hu, W. Qi, Q. Wu, Y. Zhang, and L. Nie. ChatLLM network: More brains, more intelligence.
_arXiv preprint arXiv:2304.12998_, 2023.

[27] J. L. Hellerstein, Y. Diao, S. Parekh, and D. M. Tilbury. _Feedback control of computing systems_ . John
Wiley & Sons, 2004.

[28] S. Hong, X. Zheng, J. Chen, Y. Cheng, C. Zhang, Z. Wang, S. K. S. Yau, Z. Lin, L. Zhou, C. Ran,
et al. MetaGPT: Meta programming for multi-agent collaborative framework. _arXiv preprint_
_arXiv:2308.00352_, 2023.

[29] S. International. Taxonomy and definitions for terms related to driving automation systems for on-road
motor vehicles, 2016.

[30] Z. Ji, N. Lee, R. Frieske, T. Yu, D. Su, Y. Xu, E. Ishii, Y. J. Bang, A. Madotto, and P. Fung. Survey of
hallucination in natural language generation. _ACM Computing Surveys_, 55(12):1–38, 2023.

[31] J. Johnson, M. Douze, and H. Jégou. Billion-scale similarity search with GPUs. _IEEE Transactions on_
_Big Data_, 7(3):535–547, 2019.

[32] J. Kaddour, J. Harris, M. Mozes, H. Bradley, R. Raileanu, and R. McHardy. Challenges and applications
of large language models. _arXiv preprint arXiv:2307.10169_, 2023.

[33] D. Kahneman. _Thinking, fast and slow_ . Macmillan, 2011.

[34] R. Khosla. _Engineering intelligent hybrid multi-agent systems_ . Springer Science & Business Media,
1997.

[35] G. Kiczales, J. Lamping, A. Mendhekar, C. Maeda, C. Lopes, J.-M. Loingtier, and J. Irwin. Aspectoriented programming. In _ECOOP’97—Object-Oriented Programming: 11th European Conference_
_Jyväskylä, Finland, June 9–13, 1997 Proceedings 11_, pages 220–242. Springer, 1997.

[36] B. A. Kitchenham, G. H. Travassos, A. Von Mayrhauser, F. Niessink, N. F. Schneidewind, J. Singer,
S. Takada, R. Vehvilainen, and H. Yang. Towards an ontology of software maintenance. _Journal of_
_Software Maintenance: Research and Practice_, 11(6):365–389, 1999.

[37] T. Kojima, S. S. Gu, M. Reid, Y. Matsuo, and Y. Iwasawa. Large language models are zero-shot
reasoners. _Advances in neural information processing systems_, 35:22199–22213, 2022.

[38] P. B. Kruchten. Architectural blueprints — the “4+1” view model of software architecture. _IEEE_
_software_, 12(6):42–50, 1995.

[39] Y. Labrou and T. Finin. Semantics and conversations for an agent communication language. _arXiv_
_preprint cs/9809034_, 1998.

[40] P. A. Laplante et al. _Real-time systems design and analysis_ . Wiley New York, 2004.

[41] G. Li, H. A. A. K. Hammoud, H. Itani, D. Khizbullin, and B. Ghanem. CAMEL: Communicative agents
for "mind" exploration of large scale language model society. _arXiv preprint arXiv:2303.17760_, 2023.

[42] T. Liang, Z. He, W. Jiao, X. Wang, Y. Wang, R. Wang, Y. Yang, Z. Tu, and S. Shi. Encouraging divergent
thinking in large language models through multi-agent debate. _arXiv preprint arXiv:2305.19118_, 2023.

[43] B. Y. Lin, Y. Fu, K. Yang, P. Ammanabrolu, F. Brahman, S. Huang, C. Bhagavatula, Y. Choi, and
X. Ren. SwiftSage: A generative agent with fast and slow thinking for complex interactive tasks. _arXiv_
_preprint arXiv:2305.17390_, 2023.

[44] P. Maes. Artificial life meets entertainment: lifelike autonomous agents. _Communications of the ACM_,
38(11):108–114, 1995.

[45] J. Maynez, S. Narayan, B. Bohnet, and R. McDonald. On faithfulness and factuality in abstractive
summarization. _arXiv preprint arXiv:2005.00661_, 2020.

[46] B. Meyer. Applying’design by contract’. _Computer_, 25(10):40–51, 1992.


37


[47] T. Mikolov, K. Chen, G. Corrado, and J. Dean. Efficient estimation of word representations in vector
space. _arXiv preprint arXiv:1301.3781_, 2013.


[48] M. Minsky. _The Society of mind_ . Simon and Schuster, 1988.


[49] H. Mintzberg. _The structuring of organizations_ . Springer, 1989.


[50] L. J. Moya and A. Tolk. Towards a taxonomy of agents and multi-agent systems. In _SpringSim (2)_,
pages 11–18, 2007.


[51] Y. Nakajima. BabyAGI. `[https://github.com/yoheinakajima/babyagi](https://github.com/yoheinakajima/babyagi)`, 2023.


[52] K. S. Narendra and A. M. Annaswamy. _Stable adaptive systems_ . Courier Corporation, 2012.


[53] H. Naveed, A. U. Khan, S. Qiu, M. Saqib, S. Anwar, M. Usman, N. Barnes, and A. Mian. A
comprehensive overview of large language models. _arXiv preprint arXiv:2307.06435_, 2023.


[54] M. Neef. A taxonomy of human-agent team collaborations. In _Proceedings of the 18th BeNeLux_
_Conference on Artificial Intelligence (BNAIC 2006)_, pages 245–250, 2006.


[55] Object Management Group. Unified Modeling Language – version 2.5.1. `[https://www.omg.org/](https://www.omg.org/spec/UML/2.5.1)`
`[spec/UML/2.5.1](https://www.omg.org/spec/UML/2.5.1)`, Dec. 2017.


[56] L. Ouyang, J. Wu, X. Jiang, D. Almeida, C. Wainwright, P. Mishkin, C. Zhang, S. Agarwal, K. Slama,
A. Ray, et al. Training language models to follow instructions with human feedback. _Advances in_
_Neural Information Processing Systems_, 35:27730–27744, 2022.


[57] C. A. O’reilly Iii and M. L. Tushman. Ambidexterity as a dynamic capability: Resolving the innovator’s
dilemma. _Research in organizational behavior_, 28:185–206, 2008.


[58] R. Parasuraman, T. B. Sheridan, and C. D. Wickens. A model for types and levels of human interaction
with automation. _IEEE Transactions on systems, man, and cybernetics-Part A: Systems and Humans_,
30(3):286–297, 2000.


[59] J. S. Park, J. C. O’Brien, C. J. Cai, M. R. Morris, P. Liang, and M. S. Bernstein. Generative agents:
Interactive simulacra of human behavior. _arXiv preprint arXiv:2304.03442_, 2023.


[60] S. G. Patil, T. Zhang, X. Wang, and J. E. Gonzalez. Gorilla: Large language model connected with
massive APIs. _arXiv preprint arXiv:2305.15334_, 2023.


[61] C. Qian, X. Cong, C. Yang, W. Chen, Y. Su, J. Xu, Z. Liu, and M. Sun. Communicative agents for
software development. _arXiv preprint arXiv:2307.07924_, 2023.


[62] A. Rahmati, E. Fernandes, J. Jung, and A. Prakash. IFTTT vs. Zapier: A comparative study of
trigger-action programming frameworks. _arXiv preprint arXiv:1709.02788_, 2017.


[63] M. T. Ribeiro, S. Singh, and C. Guestrin. "why should i trust you?" explaining the predictions of any
classifier. In _Proceedings of the 22nd ACM SIGKDD international conference on knowledge discovery_
_and data mining_, pages 1135–1144, 2016.


[64] N. Rozanski and E. Woods. _Software systems architecture: working with stakeholders using viewpoints_
_and perspectives_ . Addison-Wesley, 2012.


[65] S. Russell. _Human compatible: Artificial intelligence and the problem of control_ . Penguin, 2019.


[66] S. Russell. Artificial intelligence and the problem of control. _Perspectives on Digital Humanism_,
page 19, 2022.


[67] S. Russell, D. Dewey, and M. Tegmark. Research priorities for robust and beneficial artificial intelligence.
_AI magazine_, 36(4):105–114, 2015.


[68] S. K. K. Santu and D. Feng. TELeR: A general taxonomy of LLM prompts for benchmarking complex
tasks. _arXiv preprint arXiv:2305.11430_, 2023.


[69] P.-Y. Schobbens, P. Heymans, J.-C. Trigaux, and Y. Bontemps. Generic semantics of feature diagrams.
_Computer networks_, 51(2):456–479, 2007.


[70] Y. Shen, K. Song, X. Tan, D. Li, W. Lu, and Y. Zhuang. HuggingGPT: Solving AI tasks with ChatGPT
and its friends in Hugging Face. _arXiv preprint arXiv:2303.17580_, 2023.


[71] A. Shrestha, S. Subedi, and A. Watkins. AgentGPT. `[https://github.com/reworkd/AgentGPT](https://github.com/reworkd/AgentGPT)`,
2023.


[72] K. Shum, S. Diao, and T. Zhang. Automatic prompt augmentation and selection with chain-of-thought
from labeled data. _arXiv preprint arXiv:2302.12822_, 2023.


38


[73] M. P. Singh. Agent communication languages: Rethinking the principles. _Computer_, 31(12):40–47,
1998.


[74] S. A. Sloman. The empirical case for two systems of reasoning. _Psychological bulletin_, 119(1):3, 1996.


[75] J. F. Sowa. Top-level ontological categories. _International journal of human-computer studies_, 43(56):669–685, 1995.


[76] R. Thoppilan, D. De Freitas, J. Hall, N. Shazeer, A. Kulshreshtha, H.-T. Cheng, A. Jin, T. Bos, L. Baker,
Y. Du, et al. Lamda: Language models for dialog applications. _arXiv preprint arXiv:2201.08239_, 2022.


[77] Torantulino et al. Auto-GPT. `[https://github.com/Significant-Gravitas/Auto-GPT](https://github.com/Significant-Gravitas/Auto-GPT)`, 2023.


[78] P. T. Tosic and G. A. Agha. Towards a hierarchical taxonomy of autonomous agents. In _2004 IEEE_
_International Conference on Systems, Man and Cybernetics (IEEE Cat. No. 04CH37583)_, volume 4,
pages 3421–3426. IEEE, 2004.


[79] TransformerOptimus et al. SuperAGI. `[https://github.com/TransformerOptimus/SuperAGI](https://github.com/TransformerOptimus/SuperAGI)`,
2023.


[80] E. R. Tufte. _The visual display of quantitative information_, volume 2. Graphics press Cheshire, CT,
2001.


[81] M. Usman, R. Britto, J. Börstler, and E. Mendes. Taxonomies in software engineering: A systematic
mapping study and a revised taxonomy development method. _Information and Software Technology_,
85:43–59, 2017.


[82] H. Van Dyke Parunak, S. Brueckner, M. Fleischer, and J. Odell. A design taxonomy of multi-agent
interactions. In _Agent-Oriented Software Engineering IV: 4th InternationalWorkshop, AOSE 2003,_
_Melbourne, Australia, July 15, 2003. Revised Papers 4_, pages 123–137. Springer, 2004.


[83] G. Wang, Y. Xie, Y. Jiang, A. Mandlekar, C. Xiao, Y. Zhu, L. Fan, and A. Anandkumar. Voyager: An
open-ended embodied agent with large language models. _arXiv preprint arXiv:2305.16291_, 2023.


[84] L. Wang, C. Ma, X. Feng, Z. Zhang, H. Yang, J. Zhang, Z. Chen, J. Tang, X. Chen, Y. Lin, et al. A
survey on large language model based autonomous agents. _arXiv preprint arXiv:2308.11432_, 2023.


[85] L. Wang, W. Xu, Y. Lan, Z. Hu, Y. Lan, R. K.-W. Lee, and E.-P. Lim. Plan-and-solve prompting: Improving zero-shot chain-of-thought reasoning by large language models. _arXiv preprint arXiv:2305.04091_,
2023.


[86] Q. Wang, L. Ding, Y. Cao, Z. Tian, S. Wang, D. Tao, and L. Guo. Recursively summarizing enables
long-term dialogue memory in large language models. _arXiv preprint arXiv:2308.15022_, 2023.


[87] W. Wang, L. Dong, H. Cheng, X. Liu, X. Yan, J. Gao, and F. Wei. Augmenting language models with
long-term memory. _arXiv preprint arXiv:2306.07174_, 2023.


[88] Z. Wang, S. Mao, W. Wu, T. Ge, F. Wei, and H. Ji. Unleashing cognitive synergy in large language models: A task-solving agent through multi-persona self-collaboration. _arXiv preprint arXiv:2307.05300_,
2023.


[89] J. Wei, K. Shuster, A. Szlam, J. Weston, J. Urbanek, and M. Komeili. Multi-party chat: Conversational
agents in group settings with humans and models. _arXiv preprint arXiv:2304.13835_, 2023.


[90] J. Wei, X. Wang, D. Schuurmans, M. Bosma, F. Xia, E. Chi, Q. V. Le, D. Zhou, et al. Chain-of-thought
prompting elicits reasoning in large language models. _Advances in Neural Information Processing_
_Systems_, 35:24824–24837, 2022.


[91] J. White, Q. Fu, S. Hays, M. Sandborn, C. Olea, H. Gilbert, A. Elnashar, J. Spencer-Smith, and D. C.
Schmidt. A prompt pattern catalog to enhance prompt engineering with ChatGPT. _arXiv preprint_
_arXiv:2302.11382_, 2023.


[92] Y. Wolf, N. Wies, Y. Levine, and A. Shashua. Fundamental limitations of alignment in large language
models. _arXiv preprint arXiv:2304.11082_, 2023.


[93] M. Wooldridge. _An introduction to multiagent systems_ . John wiley & sons, 2009.


[94] M. Wooldridge and N. R. Jennings. Intelligent agents: Theory and practice. _The knowledge engineering_
_review_, 10(2):115–152, 1995.


[95] Z. Xi, W. Chen, X. Guo, W. He, Y. Ding, B. Hong, M. Zhang, J. Wang, S. Jin, E. Zhou, et al. The rise
and potential of large language model based agents: A survey. _arXiv preprint arXiv:2309.07864_, 2023.


39


[96] F. Xu, H. Uszkoreit, Y. Du, W. Fan, D. Zhao, and J. Zhu. Explainable AI: A brief survey on history,
research areas, approaches and challenges. In _Natural Language Processing and Chinese Computing:_
_8th CCF International Conference, NLPCC 2019, Dunhuang, China, October 9–14, 2019, Proceedings,_
_Part II 8_, pages 563–574. Springer, 2019.

[97] E. Yudkowsky. The AI alignment problem: why it is hard, and where to start. _Symbolic Systems_
_Distinguished Speaker_, 4, 2016.

[98] S. Zhang, S. Roller, N. Goyal, M. Artetxe, M. Chen, S. Chen, C. Dewan, M. Diab, X. Li, X. V. Lin,
et al. OPT: Open pre-trained transformer language models. _arXiv preprint arXiv:2205.01068_, 2022.

[99] J. Zhao. Using dependence analysis to support software architecture understanding. _arXiv preprint_
_cs/0105009_, 2001.

[100] W. X. Zhao, K. Zhou, J. Li, T. Tang, X. Wang, Y. Hou, Y. Min, B. Zhang, J. Zhang, Z. Dong, et al. A
survey of large language models. _arXiv preprint arXiv:2303.18223_, 2023.


40


