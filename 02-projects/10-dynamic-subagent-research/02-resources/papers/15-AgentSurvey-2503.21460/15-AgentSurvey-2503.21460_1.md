<!-- Source: 15-AgentSurvey-2503.21460.pdf | Chunk 1/10 -->

1


## Large Language Model Agent: A Survey on Methodology, Applications and Challenges

Junyu Luo, Weizhi Zhang, Ye Yuan, Yusheng Zhao, Junwei Yang, Yiyang Gu, Bohan Wu, Binqi Chen,
Ziyue Qiao, Qingqing Long, Rongcheng Tu, Xiao Luo, Wei Ju, Zhiping Xiao, Yifan Wang, Meng Xiao,
Chenwu Liu, Jingyang Yuan, Shichang Zhang, Yiqiao Jin, Fan Zhang, Xian Wu, Hanqing Zhao,
Dacheng Tao, _Fellow, IEEE_, Philip S. Yu, _Fellow, IEEE_ and Ming Zhang


**Abstract** —The era of intelligent agents is upon us, driven by revolutionary advancements in large language models. Large Language
Model (LLM) agents, with goal-driven behaviors and dynamic adaptation capabilities, potentially represent a critical pathway toward
artificial general intelligence. This survey systematically deconstructs LLM agent systems through a methodology-centered taxonomy,
linking architectural foundations, collaboration mechanisms, and evolutionary pathways. We unify fragmented research threads by
revealing fundamental connections between agent design principles and their emergent behaviors in complex environments. Our work
provides a unified architectural perspective, examining how agents are constructed, how they collaborate, and how they evolve over time,
while also addressing evaluation methodologies, tool applications, practical challenges, and diverse application domains. By surveying
the latest developments in this rapidly evolving field, we offer researchers a structured taxonomy for understanding LLM agents and
[identify promising directions for future research. The collection is available at https://github.com/luo-junyu/Awesome-Agent-Papers.](https://github.com/luo-junyu/Awesome-Agent-Papers)


**Index Terms** —Large language model, LLM agent, AI agent, intelligent agent, multi-agent system, LLM, literature survey


✦



**1** **INTRODUCTION**

rtificial Intelligence is entering a pivotal era with the
emergence of LLM agents—intelligent entities powered
# A
by large language models (LLMs) capable of perceiving
environments, reasoning about goals, and executing actions [1]. Unlike traditional AI systems that merely respond
to user inputs, modern LLM agents actively engage with
their environments through continuous learning, reasoning, and adaptation. This shift represents a technological
advancement and a fundamental reimagining of humanmachine relationships. Commercial LLM agent systems
( _e.g_ ., DeepResearch, DeepSearch, and Manus) exemplify this
paradigm shift—autonomously executing complex tasks that


_•_ _Junyu Luo, Ye Yuan, Yusheng Zhao, Junwei Yang, Yiyang Gu, Bohan_
_Wu, Binqi Chen, Wei Ju, Chenwu Liu, Jingyang Yuan, and Ming Zhang_
_are with the School of Computer Science and PKU-Anker LLM Lab,_
_Peking University, Beijing, China. (e-mail: luojunyu@stu.pku.edu.cn,_
_mzhang cs@pku.edu.cn)_

_•_ _Weizhi Zhang and P.S. Yu are with the Department of Computer Science,_
_University of Illinois at Chicago, Chicago, USA._

_•_ _Ziyue Qiao is with the School of Computing and Information Technology,_
_Great Bay University, Guangdong, China._

_•_ _Qingqing Long and Meng Xiao are with the Computer Network Informa-_
_tion Center, Chinese Academy of Sciences, Beijing, China._

_•_ _Rongcheng Tu, Hanqing Zhao, and Dacheng Tao are with Nanyang_
_Technological University, Singapore._

_•_ _Xiao Luo is with the Department of Computer Science, University of_
_California, Los Angeles, USA._

_•_ _Zhiping Xiao is with Paul G. Allen School of Computer Science and_
_Engineering, University of Washington, Seattle, USA._

_•_ _Yifan Wang is with the School of Information Technology_ & _Management,_
_University of International Business and Economics, Beijing, China._

_•_ _Shichang Zhang is with Harvard University, Cambridge, USA._

_•_ _Yiqiao Jin is with Georgia Institute of Technology, Atlanta, USA._

_•_ _Fan Zhang and Xian Wu are with Jarvis Research Center, Tencent YouTu_
_Lab, Shenzhen, China._



once required human expertise, from in-depth research to
computer operation, while adapting to specific user needs.
Compared to traditional agent systems [2], LLM-based
agents have achieved generational across multiple dimensions, including knowledge sources [3], generalization capabilities [4], and interaction modalities [5]. Today’s agents
represent a qualitative leap driven by the convergence of
three key developments: ❶ unprecedented reasoning capabilities of LLMs [6], ❷ advancements in tool manipulation and
environmental interaction [7], and ❸ sophisticated memory
architectures that support longitudinal experience accumulation [8], [9]. This convergence has transformed theoretical
constructs into practical systems, increasingly blurring the
boundary between assistants and collaborators. This shift
fundamentally arises from LLMs’ role as _general-purpose task_
_processors_, unifying perception, decision-making, and action
within semantic space through generative architectures,
thereby forming human-like cognitive loops [10].
Our study presents a novel examination of agent systems
through a unified taxonomy that connects agent construction,
collaboration mechanisms, and evolutionary pathways. We
offer a comprehensive perspective tracing on how agents
are defined, how they function individually or collectively,
and how they evolve over time. Beyond clarifying the
current landscape, our work not only clarifies the current
landscape but identifies emerging patterns that signal future
developments. The rapid advancement of agent technologies
necessitates timely surveys to provide researchers with an
up-to-date taxonomy for understanding this dynamic field.
Figure 1 presents our organizational framework for
understanding the LLM agent ecosystem. At its core, our
methodology-centered approach examines the technical
foundations of agent systems through three interconnected
dimensions: construction (how agents are defined and built),


2









































Fig. 1: An overview of the LLM agent ecosystem organized into four interconnected dimensions: ❶ Agent Methodology,
covering the foundational aspects of construction, collaboration, and evolution; ❷ Evaluation and Tools, presenting
benchmarks, assessment frameworks, and development tools; ❸ Real-World Issues, addressing critical concerns around
security, privacy, and social impact; and ❹ Applications, highlighting diverse domains where LLM agents are being deployed.
We provide a structured framework for understanding the complete lifecycle of modern LLM-based agent systems.



collaboration (how they interact and work together), and
evolution (how they learn and improve over time). This
tripartite foundation is complemented by practical considerations, including evaluation methodologies, development
tools, real-world challenges related to security and ethics,
and diverse application domains. This framework shapes the
structure of our survey, enabling a systematic exploration of
each dimension while highlighting their interconnections.
_**Distinction from Previous Surveys.**_ Despite several surveys
exploring various aspects of AI agents in recent years,
our study makes a distinctive contribution through its
methodological focus and comprehensive analysis of LLM
agent architectures. Previous surveys have primarily focused
on specific applications ( _e.g_ ., gaming [11], [12]), deployment
environments [13], [14], multi-modality [15] or security [16],
while others have provided broad overviews without a detailed methodological taxonomy [1], [17]. Recent works also
have examined LLM-based agents compared to traditional AI
agents [9], multi-agent interaction [18], workflows [19], and
cooperative decision-making mechanisms [20]. In contrast to
these works, our survey stands out through:

1) **Methodology-centered taxonomy:** We propose a systematic taxonomy that deconstructs LLM agent systems
into their fundamental methodological components, including role definition, memory mechanisms, planning
capabilities, and action execution [21].
2) **Build-Collaborate-Evolve framework:** We analyze three
interconnected dimensions of LLM agents - construction,
collaboration, and evolution - offering a more holistic
understanding than previous approaches [22], [23].
This integrated architectural perspective highlights the
continuity between individual LLM agent design and



collaborative systems, whereas prior studies have often
examined these aspects separately [22], [24].
3) **Frontier applications and real-world focus:** Beyond
addressing theoretical concepts, our work examines
cutting-edge tools, communication protocols, and diverse applications on LLM agents. We provide comprehensive analysis of pressing real-world challenges
including security, privacy, and ethics. This forwardlooking perspective is particularly valuable as agent
technologies transition from research to widespread
implementation.
Our survey provides researchers and practitioners with
a more structured taxonomy for understanding, comparing,
and advancing research of LLM agents from different perspectives. As LLM agent systems increasingly integrate into
various critical domains, understanding their architectural
foundations becomes essential not only for researchers but
also for policy scholars, industry practitioners, and society
at large. This survey aims to provide this foundation while
charting a path forward for this rapidly evolving field.


**2** **AGENT METHODOLOGY**


This section presents a comprehensive framework for understanding LLM-based agent systems through three interconnected dimensions: construction, collaboration, and
evolution. As illustrated in Figure 2, we first examine agent
construction (Section 2.1), which establishes the foundational components including profile definition, memory
mechanisms, planning capabilities, and action execution.
We then explore collaboration paradigms (Section 2.2) that
enable multiple agents to work together through centralized


3



























































Fig. 2: A taxonomy of large language model agent methodologies.



control, decentralized cooperation, or hybrid architectures.
Finally, we investigate evolution mechanisms (Section 2.3)
that allow agents to improve over time through autonomous
optimization, multi-agent co-evolution, and external resource
integration. This three-dimensional framework provides a
systematic approach to analyzing the full lifecycle of LLM
agent systems.


**2.1** **Agent Construction**


Agent construction serves as the foundational phase in
developing LLM-based autonomous systems, encompassing
the systematic design of core components that enable goaldirected behaviors. This process prioritizes four interdependent pillars: profile definition (2.1.1), memory mechanism
(2.1.2), planning capability (2.1.3), and action execution (2.1.4).
These components collectively form a recursive optimization
loop, where memory informs planning, execution outcomes
update memory, and contextual feedback refines agent



profiles. The construction paradigm emphasizes modular
interoperability while preserving system-wide coherence, enabling subsequent collaboration and evolutionary adaptation
mechanisms, which will be discussed in later sections.


_2.1.1_ _Profile Definition_

Profile definition establishes an agent’s operational identity by configuring its intrinsic attributes and behavioral
patterns [25], [26]. Current methodologies encompass two
approaches: _human-curated static profiles_ ensure domainspecific consistency through manual specification, while
_batch-generated dynamic profiles_ adaptively modulate operational parameters to stochastically yield a batch of agent
initializations. These mechanisms collectively govern an
agent’s decision boundaries and interaction protocols while
maintaining alignment with predefined objectives.
_**Human-Curated Static Profiles.**_ This approach establishes
fixed agent profiles through manual specification by domain


experts, embedding explicit rules and domain-specific knowledge. It ensures strict adherence to predefined behavioral
guidelines and task requirements enabling standardized
communication protocols among agents. This is particularly
effective in scenarios demanding high interpretability and
regulatory compliance. Such frameworks typically employ
coordinated interactions between predefined agent components to achieve complex functionalities through structured
communication patterns. Representative implementations
demonstrate two key paradigms: systems like Camel [25],
AutoGen [26], and OpenAgents [40] orchestrate humanagent collaboration through predefined conversational roles
(e.g., user proxy and assistant), enabling task execution
through structured dialogues. Meanwhile, frameworks such
as MetaGPT [27], ChatDev [28], and AFlow [29] showcase
role-based coordination patterns. ChatDev specializes in
code development by coordinating static technical roles (e.g.,
product managers and programmers) with deterministic
interaction protocols, while MetaGPT and AFlow extend this
paradigm to general task solving through structured role
orchestration.

_**Batch-Generated Dynamic Profiles.**_ This paradigm employs
parameterized initialization to systematically generate diverse agent profiles that emulate human societal behaviors.
By injecting controlled variations into personality traits,
knowledge backgrounds, or value systems during agent
creation (e.g., through template-based prompting or latent
space sampling), the framework produces heterogeneous
populations capable of exhibiting complex social dynamics.
Such parameter-driven diversity is essential for simulating
realistic human-agent interactions in applications ranging
from social behavior studies to emergent group intelligence simulations. This is demonstrated in systems for
human behavior simulation [30] and simulated user data
collection [31] where different profile configurations directly
shape collective interaction patterns. Moreover, DSPy [32]
can further optimize the parameters of the agent profile
initialization.


_2.1.2_ _Memory Mechanism_


Memory mechanisms equip agents with the ability to store,
organize, and retrieve information across temporal dimensions. Short-term memory maintains transient contextual
data for immediate task execution, while long-term memory preserves structured experiential knowledge for persistent reference. Integrating knowledge retrieval mechanisms
further optimizes information accessibility with RetrievalAugmented Generation (RAG) techniques [43].
_**Short-Term Memory.**_ Short-term memory retains agentinternal dialog histories and environmental feedback to
support context-sensitive task execution. This mechanism
is widely implemented in frameworks such as ReAct [33]
for thinking with reflection, ChatDev [28] for software
development, Graph of Thoughts [34] for solving elaborate problems, and AFlow [29] for workflow automation,
demonstrating its versatility across domains. While this
mechanism enables detailed reasoning through interactive
exchanges, its transient nature limits knowledge retention
beyond immediate contexts—intermediate reasoning traces
often dissipate after task completion and cannot be directly



4


transferred to new scenarios. Furthermore, due to LLMs’
context window limitations, practical implementations require active information compression (e.g., summarization or
selective retention) and impose many constraints on multiturn interaction depth to prevent performance degradation.
_**Long-Term Memory.**_ Long-term memory systematically
archives agents’ intermediate reasoning trajectories and
synthesizes them into reusable tools for future invocation. This process transforms ephemeral cognitive efforts
into persistent operational assets through three dominant
paradigms: ❶ skill libraries that codify procedural knowledge
(e.g., Voyager’s automated skill discovery in Minecraft [35]
and GITM’s text-based knowledge base [36]), ❷ experience repositories that store success/failure patterns (e.g.,
ExpeL’s distilled experience pool [37] and Reflexion’s trialoptimized memory [38]), and ❸ tool synthesis frameworks
that evolve capabilities through combinatorial adaptation
(e.g., TPTU’s adaptive tool composition [39] and OpenAgents’
self-expanding toolkit [40]). Cross-domain implementations,
such as Lego-Prover’s theorem bank [41] and MemGPT’s
tiered memory architecture [42], further demonstrate how
structured long-term storage enhances reasoning efficiency
through strategic knowledge reuse.
_**Knowledge**_ _**Retrieval**_ _**as**_ _**Memory.**_ This paradigm diverges from agent-internal memory generation by integrating external knowledge repositories into generation processes, effectively expanding agents’ accessible information
boundaries. Current implementations exhibit three dominant approaches: ❶ Static knowledge grounding through
text corpora (RAG [43]) or structured knowledge graphs
(GraphRAG [44]), ❷ Interactive retrieval that integrates
agent dialogues with external queries, as demonstrated in
Chain of Agents [45] where short-term inter-agent communications trigger contextualized knowledge fetching, and ❸
Reasoning-integrated retrieval, exemplified by IRCoT [46]
and Llatrieval [47], which interleave step-by-step reasoning
with dynamic knowledge acquisition. Advanced variants
like KG-RAR [48] further construct task-specific subgraphs
during reasoning, while DeepRAG [49] introduces fine-tuned
retrieval decision modules to balance parametric knowledge
and external evidence. These hybrid architectures enable
agents to transcend training data limitations while maintaining contextual relevance, establishing knowledge retrieval as
critical infrastructure for scalable memory systems.


_2.1.3_ _Planning Capability_


Planning capabilities are a critical aspect of LLM agents’ abilities, enabling them to navigate through complex tasks and
problem-solving scenarios with high accuracy [103]. Effective
planning is essential for deploying LLM agents in real-world
applications, where they must handle a diverse range of
complex tasks and scenarios. The planning capability of
an LLM agent can be viewed from two perspectives: task
decomposition and feedback-driven iteration.
_**Task Decomposition Strategies.**_ Task decomposition represents a basic approach to enhancing LLM planning capabilities by breaking down complex problems into more
manageable subtasks. Although solving an entire problem
may be challenging for LLM agents, they can more easily
handle subtasks and then integrate the results to address


5



the full problem. Task decomposition strategies fall into two
main categories: single-path chaining and multi-path tree
expansion.
Single-path chaining is a simple method with the simplist
version as zero-shot chain-of-thought [104], [105]. It first asks
the agent to devise a plan, which consists of a sequence of
subtasks that are built upon one another. Subsequently, the
agent is asked to solve the subtasks in the order they are
presented [50], [105]. This plan-and-solve paradigm [51] is
straightforward and easy to implement. However, it may
suffer from a lack of flexibility and error accumulation
during chaining, as the agent is required to follow the predefined plan without any deviation during the problemsolving procedure. Therefore, one line of work proposes to
adopt dynamic planning that only generates the next subtask
based on the current situation of the agent [33], [105]. This
enables the agent to receive environmental feedback and
adjust its plan accordingly, enhancing its robustness and
adaptability. Moreover, another line of work proposes to
use multiple chain-of-thoughts to improve the robustness of
the planning process. This is similar to ensemble methods,
involving self-consistency [62], [106], majority voting [107],
and agent discussion [52] to combine multiple chains. By
combining the wisdom of multiple chains, the agent can
make more accurate decisions and reduce the risk of error
accumulation.
A more complicated method is to use trees instead
of chains as the planning data structure, where multiple
possible reasoning paths exist when the agent is planning,
and the agent is allowed to backtrack with information
from feedback [53], [54]. Long et al. [55] propose a treeof-thought (ToT) method that explores the solution space
through a tree-like thought process. This allows the LLMs
to backtrack to previous states, which makes it possible
for the model to correct its previous mistakes, enabling
applications to various complicated tasks that involve the
”trial-error-correct” process. In more realistic scenarios, the
agent can gather feedback from the environment or humans
and dynamically adjust its reasoning path, potentially incorporating reinforcement learning [56], [108]. This enables
the agent to make more informed decisions in real-world
applications using advanced algorithms such as Monte Carlo
Tree Search [109], facilitating use cases in robotics [57]–[59]
and game-playing [110], [111].


_**Feedback-Driven Iteration.**_ Feedback-driven iteration is a crucial aspect of LLM planning capabilities, enabling the agent
to learn from the feedback and enhance its performance over
time. Feedback can originate from various sources, such as
environmental input, human guidance, model introspection,
and multi-agent collaboration.
Environmental feedback is one of the most common types
of feedback in robotics [60], generated by the environment
in which the embodied agent operates. Human feedback,
another crucial type, comes from user interactions or manually labeled data prepared in advance [61], [112]. Model
introspection provides an additional source of feedback,
which is generated by the agent itself [62]. Multi-agent
collaboration also serves as a feedback mechanism, where
multiple agents work together to solve a problem and
exchange insights [63], [112]. These sources of feedback


