<!-- Source: 15-AgentSurvey-2503.21460.pdf | Chunk 6/10 -->

are also used to improve the generation pipeline of academic
works. AgentReview [268] proposes an LLM-agent-based


framework for simulating academic peer review processes,
offering valuable insights to improve the design of evaluation
protocols for academic papers.


_5.1.2_ _Agentic AI in Chemistry, Materials Science and As-_
_tronomy_


Due to the abundance of digital tools and data in these fields,
chemistry, materials science, and Astronomy have been early
adopters of LLM-based agentic AI. In the chemistry domain,
ChemCrow [269] exemplifies an LLM-driven chemistry agent
designed to foster scientific advancement by bridging the
gap between experimental and computational chemistry.
ChemCrow integrates an LLM with a suite of 18 expertdesigned chemistry tools, such as molecule property predictors, reaction planners and databases, enabling it to plan
and execute chemical syntheses autonomously. Materials
science problems, which often span multiple scales and
modalities (from atomic simulations to empirical data), also
benefit from multi-agent AI. AtomAgents [270] framework
is a physics-aware multi-agent system for automating alloy
design. In this system, a Planner agent (GPT-4) decomposes a
complex materials design challenge into a sequence of tasks,
which are then verified by a Critic agent and delegated to
specialist modules. Similar principles are being applied in
physics and astronomy. For example, an AI copilot agent
has been developed for the Cherenkov Telescope Array
in astronomy [271], using an instruction-tuned LLM to
autonomously manage telescope configuration databases and
even generate code for data analysis workflows. Although
still experimental, these efforts indicate that LLM-based
agents could soon be used in physics labs and astronomical
observatories. They could handle routine decision-making
and free human scientists to focus on high-level insights.


_5.1.3_ _Agentic AI in Biology_


The life sciences are likewise beginning to embrace LLMbased multi-agent systems for hypothesis generation and
data analysis [272]. One notable direction is using LLM
agents to propose biological experiments or interpret multiomics data. BioDiscoveryAgent [273] proposed an AI agent to
design genetic perturbation experiments in molecular biology.
By parsing literature and gene databases, an LLM agent can
suggest which gene knockouts or edits might elucidate a
certain biological pathway. Another system, GeneAgent [274],
uses a self-refinement loop to discover gene associations from
biomedical databases, improving the reliability of findings
by cross-checking against known gene sets. RiGPS [275]
developed a multi-agent system with an experiment-based
self-verified reinforcement learning framework, enhancing
the biomarker identification task in the single-cell dataset.
BioRAG [211] developed a multi-agent-based RAG system
to handle biology-related QA, where several agents are
designed to retrieve information using multiple tools, and
one agent is specifically used to self-evaluate the retrieval
results. These examples illustrate the methodology of selfquestioning or self-verification in multi-agent AI: one or more
agents propose a scientific insight, and another evaluates its
plausibility with known knowledge, thereby reducing errors.



16


_5.1.4_ _Agentic AI in Scientific Dataset Construction_


Multi-agent systems also accelerate the construction of
scientific datasets. For instance, PathGen-1.6M [276] generated a massive pathology image dataset via multi-agent
collaboration, where multiple AI models played different
roles: one vision model scanned whole-slide histology images
to select representative regions, another (an LLM or multimodal model) generated descriptive captions for each region,
and additional agents iteratively refined the captions for
accuracy. KALIN [277] developed a multi-agent collaborative
framework to generate a high-quality domain LLM training
corpus. Specifically, two distinct LLMs are trained to generate
scientific questions with input chunked research articles as
context. Then, KAILIN utilizes a knowledge hierarchy to
self-evaluate the alignment of generated questions with the
input context, then self-evolving to more in-depth questions.
GeneSUM [278] is designed to maintain the gene function
description knowledge dataset automatically. Specifically, a
single description agent serves as a reader for gene ontology,
a retrieval agent functions as a reader for related literature,
and a summarization agent acts as the generator. GeneSUM
thus can automatically read emerging gene-function-related
research articles and renew the database of gene function
descriptions. These approaches demonstrate a virtuous
cycle: AI systems can consume scientific data and create
it, improving the next generation of models.


_5.1.5_ _Agentic AI in Medical_


Digitization of medical records [279], [280] brings great
potential in applying agentic AI in medical service. One
line of research has created simulated clinical environments
in which autonomous doctors and patient agents interact.
AgentHospital [281] is a virtual hospital populated by LLMdriven doctors, nurses, and patient agents, modeling the
full cycle of care from triage to diagnosis to treatment. In
this system, each patient agent presents symptoms, and
doctor agents must converse with the patient, order virtual
tests, make a diagnosis, and prescribe treatment. In parallel,
other work focuses on aligning multi-agent AI directly with
clinical decision support in real scenarios. ClinicalLab [282]introduced a comprehensive benchmark and an agent for
multi-department medical diagnostics, which involved 150
diseases across 24 medical specialties, reflecting the breadth
of knowledge required in hospital settings. Multi-agent
systems can also enhance conversational applications by
introducing roles and simulations. AIPatient [283] is a
system that creates realistic patient simulators powered
by LLMs. It leverages a structured knowledge graph of
medical information as a source of ground truth about a
patient’s conditions, and a Reasoning RAG workflow that
allows the patient agent to retrieve relevant details and
respond to a doctor’s questions in a convincing manner.
Medical imaging is another domain ripe for multi-agent AI
integration. For instance, CXR-Agent [284] uses a visionlanguage model together with an LLM to interpret chest
X-rays and generate radiology reports with uncertainty
estimates. MedRAX [285] integrates several specialized tools,
such as an optical character reader for reading prior reports,
a segmentation model for highlighting image regions, and
an LLM for clinical reasoning, to solve complex chest


TABLE 7: Overview of Applications in LLM Agents.


Method Domain Core Idea


**Scientific Discovery**


SciAgents [266] General Sciences Collaborative hypothesis generation
Curie [267] General Sciences Automated experimentation
ChemCrow [269] Chemistry Tool-augmented synthesis planning
AtomAgents [270] Materials Science Physics-aware alloy design
D. Kostunin el al [271] Astronomy Telescope configuration management
BioDiscoveryAgent [273] Biology Genetic perturbation design
GeneAgent [274] Biology Self-verifying gene association discovery
RiGPS [275] Biology Biomarker identification
BioRAG [211] Biology Biology-focused retrieval augmentation
PathGen-1.6M [276] Medical Dataset Pathology image dataset generation
KALIN [277] Biology Dataset Scientific question corpus generation
GeneSUM [278] Biology Dataset Gene function knowledge maintenance
AgentHospital [281] Medical Virtual hospital simulation
ClinicalLab [282] Medical Multi-department diagnostics
AIPatient [283] Medical Patient simulation
CXR-Agent [284] Medical Chest X-ray interpretation
MedRAX [285] Medical Multimodal medical reasoning


**Gaming**


ReAct [33] Game Playing Reasoning and acting in text environments
Voyager [35] Game Playing Lifelong learning in Minecraft
ChessGPT [287] Game Playing Chess gameplay evaluation
GLAM [288] Game Playing Reinforcement learning in text environments
CALYPSO [289] Game Generation Narrative generation for D&D
GameGPT [290] Game Generation Automated game development
Sun et al. [291] Game Generation Interactive storytelling experience


**Social Science**


Econagent [292] Economy Economic decision simulation
TradingGPT [293] Economy Financial trading simulation
CompeteAI [294] Economy Market competition modeling
Ma et al. [295] Psychology Mental health support analysis
Zhang et al. [296] Psychology Social behavior simulation
TE [297] Psychology Psychological experiment simulation
Generative agents [30] Social Simulation Human behavior emulation
Liu et al. [298] Social Simulation Learning from social interactions
S [3] [299] Social Simulation Social network behavior modeling


**Productivity Tools**


SDM [300] Software Development Self-collaboration for code generation
ChatDev [301] Software Development Chat-powered development framework
MetaGPT [27] Software Development Meta-programming for collaboration
Agent4Rec [302] Recommender Systems User behavior modeling
AgentCF [303] Recommender Systems User-item interaction modeling
MACRec [304] Recommender Systems Multi-agent recommendation
RecMind [305] Recommender Systems Knowledge-enhanced recommendation


X-ray cases that require referring to patient history and
imaging simultaneously. Evaluations of these approaches
on standard chest X-ray benchmarks [286] showed that it
could achieve diagnostic accuracy on par with state-of-the-art
standalone models while also providing an uncertainty score
that correlates with its correctness. In summary, the multiagent paradigm in medicine holds promise for improving
AI reliability by introducing redundancy, specialization, and
oversight. However, it also complicates the system, requiring
rigorous validation.


**5.2** **Gaming**


The development of LLM agents offers an unprecedented opportunity in gaming, enabling agents to take on diverse roles
and exhibit human-like decision-making skills in intricate
game environments. Based on the different characteristics
of the games and roles of the agent, the applications can be
categorized into game playing and game generation.
_**Game Playing.**_ In role-playing games, LLM agents can
assume various character roles, both as player-controlled
characters and non-player characters (NPCs). ReAct [33]
prompts LLMs to integrate reasoning and reflection into
action generation, enhancing decision-making in the embodied environment. Voyager [35] introduces an LLM-powered
lifelong learning agent in Minecraft that persistently explores
the game world. ChessGPT [287] presents an autonomous
agent on mixed game-language data to facilitate board state



17


evaluation and chess gameplay. GLAM [288] builds an agent
in the BabyAI-text environment, where a policy is used to
select the next action, with training conducted through online
reinforcement learning.
_**Game Generation.**_ In game generation, LLMs are used to
create dynamic and interactive game content. CALYPSO [289]
creates LLM agents as the assistants to help build a compelling narrative to present in the context of playing Dungeons & Dragons. GameGPT [290] leverages dual-agent
collaboration and a hierarchical approach, using multiple
internal dictionaries to automate and enhance the game
development process. Sun et al. [291] create an interactive
storytelling game experience in 1001 Nights, where instructive language models and image generation are combined to
shape the narrative and world.


**5.3** **Social Science**


The application of LLM agents in social science has seen
significant advancements, providing new opportunities for
understanding and simulating complex human behaviors
and interactions. These models facilitate insights into various domains, including economics, psychology and social
simulation. Below, we explore how LLM agents are being
applied across these three critical areas.
_**Economy.**_ In economics, LLM agents are utilized to analyze financial data and simulate financial activities. Econagent [292] employs prompt engineering to create agents that
mimic human-like decisions or macroeconomic simulations.
TradingGPT [293] presents a multi-agent framework for
financial trading, which simulates human decision processes by incorporating hierarchical memory structures and
debate mechanisms with individualized trading profiles.
CompeteAI [294] leverages LLM agents to model a virtual
town where restaurants and customers interact, providing
insights consistent with sociological and economic theories.
_**Psychology.**_ In psychological research, LLM agents are
utilized to model human behavior with diverse traits and
cognitive processes. Ma et al. [295] investigate the psychological effects and potential benefits of using LLM-based
conversational agents for mental health support. Zhang
et al. [296] examine how LLM agents with unique traits
and thought processes replicate human-like social behaviors, including conformity and majority influence. TE [297]
uses LLM agents to simulate psychological experiments,
potentially revealing consistent distortions in how language
models replicate specific human behaviors.
_**Social Simulation.**_ In societal simulation, LLM agents are
employed to model complex societal behaviors. These simulations help in understanding real-world phenomena, such
as social influence, information diffusion, and collective
decision-making. Generative agents [30] introduce a multiagent interaction model within an interactive sandbox environment, leveraging LLM agents to simulate realistic human
behavior in a variety of contexts. Building on this, Liu et
al. [298] introduce a training paradigm that enables LLMs
to learn from these simulated social interactions involving
multiple LLM agents. S [3] [299] develops an LLM-based multiagent system to ensure the agents’ behaviors closely mimic
those of real humans within social networks.


**5.4** **Productivity Tools**


LLM agents are increasingly leveraged to boost productivity
by automating diverse tasks, facilitating collaboration in
solving complex problems, and optimizing efficiency across
multiple domains. Below, we highlight their applications in
software development and recommender systems.


_**Software Development.**_ Since software development involves
multiple roles, such as product managers, developers, and
testers, all working together to deliver high-quality products, LLM agents are increasingly being used to streamline
various aspects of the process. SDM [300] introduces a
self-collaboration framework that guides multiple LLM
agents to work together on code generation tasks, enhancing their ability to tackle complex software development
challenges collaboratively. ChatDev [301] proposes a chatpowered software development framework, where agents
are guided on both what to communicate and how to
communicate effectively. MetaGPT [27] further incorporates
human workflows (i.e., Standardized Operating Procedures)
into LLM-powered multi-agent collaboration through a
meta-programming approach to enhance coordination and
streamline the collaborative process.


_**Recommender Systems.**_ In the realm of recommender systems, LLM agents are increasingly utilized to simulate user
behaviors. Agent4Rec [302] employs LLM agents with integrated user profiling, memory, and action modules to model
user behavior in recommender systems. AgentCF [303]
treats both users and items as LLM agents, introducing
a collaborative learning framework to model user-item
interactions in recommender systems. MACRec [304] directly
develops multiple agents to tackle the recommendation task.
RecMind [305] employs LLM agents to incorporate external
knowledge and carefully plans the utilization of tools for
zero-shot personalized recommendations.


**6** **CHALLENGES AND FUTURE TRENDS**


Advancements in LLM-based multi-agent systems bring
significant opportunities but also present pressing challenges
in scalability, memory, reliability, and evaluation. This section
outlines key obstacles and emerging trends shaping the
future of agentic AI.


**6.1** **Scalability and Coordination**


Scaling LLM-based multi-agent systems remains challenging due to high computational demands, inefficiencies in
coordination, and resource utilization [306], [307]. Existing
multi-agent frameworks, designed for lightweight agents
like function calls and rule-based systems [308], [309], lack
system-level optimization for LLM agents with billionscale parameters [26]. Future directions include _hierarchical_
_structuring_, where high-level LLM agents delegate subtasks
to specialized lower-level agents, and _decentralized planning_,
which enables agents to plan concurrently and synchronize
periodically to mitigate bottlenecks. Advancements in robust
communication protocols and efficient scheduling mechanisms are needed to enhance coordination, real-time decisionmaking, and system robustness [306], [307].



18


**6.2** **Memory Constraints and Long-Term Adaptation.**


Maintaining coherence across multi-turn dialogues and the
longitudinal accumulation of knowledge requires effective
memory mechanisms [310]. However, as LLMs possess very
limited effective context [74], [311], integrating sufficient
historical information into prompts becomes challenging.
This hinders the models’ contextual awareness over extended
interactions. Ensuring interaction continuity requires efficient
memory scalability and relevance management [312] beyond
current practice such as vector databases, memory caches,
context window management, and retrieval-augmented
generation (RAG) [43]. Future directions include _hierarchical_
_memory architectures_ that combine _episodic memory_ for shortterm planning with _semantic memory_ for long-term retention,
as well as autonomous knowledge compression [313] to
refine memory dynamically and enhance reasoning over
extended interactions.


**6.3** **Reliability and Scientific Rigor**


LLMs, while knowledge-rich, are neither comprehensive nor
up-to-date, thus potentially unsuitable as standalone replacements for structured databases. Their stochastic nature makes
outputs highly sensitive to minor variations in prompts [314],
causing hallucinations [315] and compounding uncertainty
in multi-agent systems, such as agentic frameworks for
medical applications and autonomous scientific discovery [316], where unreliable outputs can mislead high-stake
decision-making. Addressing these challenges necessitates
the development of rigorous validation mechanisms and
structured verification pipelines, including _knowledge-graph-_
_based verification_, where outputs are cross-checked against
structured databases [317], and _cross-referencing via retrieval_,
which grounds responses in cited source like web pages
as in WebGPT [318]. Along this direction, future work can
explore LLMs capable of direct citation generation, as well
as up-to-date and comprehensive knowledge sources readily
available for LLM applications. Meanwhile, in high-stakes
domains like healthcare, law, or scientific research, pure
automation remains risky. _AI-human verification loops_ are becoming standard for ensuring safety, reliability, and accountability [315]. Future works can enhance cross-referencing
mechanisms [319], self-consistency [320], and standardized
AI auditing frameworks, such as fact-checking logs, to
improve accountability. For example, one critical challenge is
determining optimal intervention points amid the vast scale
of LLM-generated content.


**6.4** **Multi-turn, Multi-agent Dynamic Evaluation**


Traditional AI evaluation frameworks, designed for static
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
