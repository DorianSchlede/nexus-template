<!-- Source: 15-AgentSurvey-2503.21460.pdf | Chunk 2/10 -->

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



help evaluate the agent’s performance and thus guide its
planning. For instance, the agent can use feedback to update
(regenerate) its plan, adjust its reasoning path, or even modify
its goal. This iterative process continues until a satisfactory
plan is achieved [64], [65].


_2.1.4_ _Action Execution_

With the planning capability, it is important for the LLMs
to have the ability to execute the planned actions in the real
world. Action execution is a critical aspect of LLM agents’
abilities, as good plans are useless if the agent cannot execute
them effectively. Action execution involves two aspects: tool
utilization [113], and physical interaction [114].
**Tool utilization** [113] is an important aspect of LLM
action execution, enabling a wide range of abilities such
as precise calculation of numbers, up-to-date information
understanding, and proficient code generation. The tool
use ability involves two aspects: tool use decision and tool
selection. The tool-use decision is the process of deciding
whether to use a tool to solve a problem. When the agent is
generating content with less confidence or facing problems
related to specific tool functions, the agent should decide to
use specific tools [66], [67]. Tool selection is another important
aspect of tool utilization, involving the understanding of
tools and the agent’s current situation [68], [69]. For example,
Yuan et al. [68] propose simplifying the tool documentation
to better understand the available tools, enabling a more
accurate selection of tools.
**Physical interaction** [114] is a fundamental aspect of
embodied LLM agents. Their ability to perform specific
actions in the real world and interpret environmental feedback is crucial. When deployed in real-world settings, LLM
agents must comprehend various factors to execute actions
accurately. These factors include robotic hardware [114],
social knowledge [70], and interactions with other LLM
agents [71], [72].


**2.2** **Agent Collaboration**


Collaboration among LLM agents plays a crucial role in
extending their problem-solving capabilities beyond individual reasoning. Effective collaboration enables agents to
leverage distributed intelligence, coordinate actions, and
refine decisions through multi-agent interactions [26], [121].
We categorize existing collaboration paradigms into three



TABLE 1: A summary of agent collaboration methods.


**Category** **Method** **Key Contribution**



**Centralized Control**


**Decentralized Collaboration**


**Hybrid Architecture**



Coscientist [73] Human-centralized experimental control
LLM-Blender [74] Cross-attention response fusion
MetaGPT [27] Role-specialized workflow management
AutoAct [75] Triple-agent task differentiation
Meta-Prompting [76] Meta-prompt task decomposition
WJudge [77] Weak-discriminator validation


MedAgents [78] Expert voting consensus
ReConcile [79] Multi-agent answer refinement
METAL [115] Domain-specific revision agents
DS-Agent [116] Database-driven revision
MAD [80] Structured anti-degeneration protocols
MADR [81] Verifiable fact-checking critiques
MDebate [82] Stubborn-collaborative consensus
AutoGen [26] Group-chat iterative debates


CAMEL [25] Grouped role-play coordination
AFlow [29] Three-tier hybrid planning
EoT [117] Multi-topology collaboration patterns
DiscoGraph [118] Pose-aware distillation
DyLAN [119] Importance-aware topology
MDAgents [120] Complexity-aware routing


fundamental architectures: _centralized control_, _decentralized_
_cooperation_, and _hybrid architectures_ . These paradigms differ
in their decision hierarchies, communication topologies, and
task allocation mechanisms, each offering distinct advantages
for specific application scenarios.


_2.2.1_ _Centralized Control_
Centralized control architectures employ a hierarchical coordination mechanism where a central controller organizes
agent activities through task allocation and decision integration, while other sub-agents can only communicate with
the controller. This paradigm features two implementation
strategies: _explicit controller_ systems utilize dedicated coordination modules (often implemented as separate LLM
agents) to decompose tasks and assign subgoals, while
_differentiation-based_ systems achieve centralized control by
using prompts to guide the meta agent in assuming distinct
sub-roles. The centralized approach excels in mission-critical
scenarios requiring strict coordination, such as industrial
automation [122] and scientific research [73].
_**Explicit Controller Systems.**_ Multiple related works have
been developed to explicitly implenment centralized architectures. The Coscientist [73] exemplifies the explicit controller
paradigm, where a human operator serves as the central
controller. It establishes standardized scientific experimental
workflows, allocates specialized agents and tools to distinct
experimental phases, and maintains direct control over the
final execution plan. LLM-Blender [74] explicitly creates
a controller that employs a cross-attention encoder for
pairwise comparison to identify the best responses, and then
fuses the top-ranked responses, enhancing their strengths
while mitigating weaknesses. MetaGPT [27] simulates realworld software development workflows, direclty assigning
specialized managers to control distinct functional roles and
phases.
_**Differentiation-based Systems.**_ AutoAct [75] exemplifies
the differentiation-based paradigm, which implicitly differentiates the meta-agent into three sub-agents—plan-agent,
tool-agent, and reflect-agent—to break down the complex
ScienceQA task. Meta-Prompting [76] decomposes complex tasks into domain-specific subtasks through carefully
crafted meta-prompts. A single model acts as a coordinator,
dynamically assigning subtasks to specialized sub-agents
guided by task-oriented prompts. The centrol manager then
integrates all intermediate outputs to produce the final
solution. These works predominantly employ highly capable
agents as central controllers to optimize task allocation and
decision aggregation. However, WJudge [77] demonstrates
that even controllers with limited discriminative power can
also significantly enhance the overall performance of agent
systems.


_2.2.2_ _Decentralized Collaboration_
In contrast to centralized architectures where a single control node often becomes a bottleneck due to handling all
inter-agent communication, task scheduling, and contention
resolution, decentralized collaboration enables direct nodeto-node interaction through self-organizing protocols. This
paradigm can be further categorized into two distinct
approaches: _revision-based systems_ and _communication-based_
_systems_ .



6


_**Revision-based Systems.**_ In this paradigm, agents only
observe finalized decisions generated by peers and iteratively
refine a shared output through structured editing protocols.
This approach typically produces more standardized and deterministic outcomes. For instance, MedAgents [78] employs
predefined domain-specific expert agents that sequentially
propose and modify decisions independently, with consensus
achieved through final voting. ReConcile [79] coordinates
agents to iteratively refine answers through mutual response
analysis, confidence evaluation, and human-curated exemplars. METAL [115] introduces specialized text and visual
revision agents for chart generation tasks, demonstrating
how domain-specific refinement improves output quality.
Notably, revision signals may originate not only from agent
interactions but also from external knowledge bases [116],

[123], enabling hybrid refinement strategies.
_**Communication-based Systems.**_ Compared to revision-based
approaches, communication-based methods feature more
flexible organizational structures, allowing agents to directly
engage in dialogues and observe peers’ reasoning processes.
This makes them particularly suitable for modeling dynamic scenarios such as human social interactions [30]. Key
implementations include: MAD [80] employs structured
communication protocols to address the ”degeneration-ofthought” problem, where agents overly fixate on initial
solutions. MADR [81] enhances this by enabling agents to
critique implausible claims, refine arguments, and generate verifiable explanations for fact-checking. MDebate [82]
optimizes consensus-building through strategic alternation
between stubborn adherence to valid points and collaborative
refinement. AutoGen [26] implements a group-chat framework that supports multi-agent participation in iterative
debates for decision refinement.


_2.2.3_ _Hybrid Architecture_


Hybrid architectures strategically combine centralized coordination and decentralized collaboration to balance controllability with flexibility, optimize resource utilization, and
adapt to heterogeneous task requirements. This approach
introduces two implementation patterns: _static systems_ with
predefined coordination rules and _dynamic systems_ featuring
self-optimizing topologies.
_**Static Systems.**_ Static systems predefine fixed patterns for
combining different collaboration modalities. Representative
implementations include: CAMEL [25] partitions agents into
intra-group decentralized teams for role-playing simulations,
while maintaining inter-group coordination through centralized governance. AFlow [29] employs a three-tier hierarchy
consisting of centralized strategic planning, decentralized
tactical negotiation, and market-driven operational resource
allocation. EoT [117] formalizes four collaboration patterns
(BUS, STAR, TREE, RING) to align network topologies with
specific task characteristics.
_**Dynamic Systems.**_ Recent innovations introduce neural topology optimizers that dynamically reconfigure collaboration
structures based on real-time performance feedback, enabling
automatic adaptation to changing conditions. Key implementations demonstrate this paradigm: DiscoGraph [118] introduces trainable pose-aware collaboration through a teacherstudent framework. The teacher model with holistic-view


TABLE 2: A summary of agent evolution methods.


**Category** **Method** **Key Contribution**


SE [86] Adaptive token masking for pretraining
**Self-Supervised Learning** Evolutionary Optimization [87] Efficient model merging and adaptation
DiverseEvol [88] Improved instruction tuning via diverse data



**Self-Reflection & Self-Correction**



SELF-REFINE [89] Iterative self-feedback for refinement
STaR [90] Bootstrapping reasoning with few rationales
V-STaR [91] Training a verifier using DPO
Self-Verification [92] Backward verification for correction



Self-Rewarding [93] LLM-as-a-Judge for self-rewarding
**Self-Rewarding & RL** RLCD [94] Contrastive distillation for alignment
RLC [95] Evaluation-generation gap for optimization


ProAgent [96] Intent inference for teamwork
**Cooperative Co-Evolution** CORY [97] Multi-agent RL fine-tuning
CAMEL [25] Role-playing framework for cooperation


Red-Team LLMs [98] Adversarial robustness training
**Competitive Co-Evolution** Multi-Agent Debate [82] Iterative critique for refinement
MAD [99] Debate-driven divergent thinking

**Knowledge-Enhanced Evolution** KnowAgent [WKM [84] 83] Action knowledge for planningSynthesizing prior and dynamic knowledge


CRITIC [100] Tool-assisted self-correction
**Feedback-Driven Evolution** STE [101] Simulated trial-and-error for tool learning
SelfEvolve [102] Automated debugging and refinement


inputs guides the student model via feature map distillation,
while matrix-valued edge weights enable adaptive spatial
attention across agents. DyLAN [119] first utilizes the Agent
Importance Score to identify the most contributory agents
and then dynamically adjusts the collaboration structure
to optimize task completion. MDAgents [120] dynamically
assigns collaboration structures based on the task at hand.
It first performs a complexity check to classify tasks as low,
moderate, or high complexity. Simple tasks are handled by
a single agent, while more complex tasks are addressed
through hierarchical collaboration.


**2.3** **Agent Evolution**


LLM Agents are evolving through various mechanisms that
enable autonomous improvement, multi-agent interaction,
and external resource integration. This section explores three
key dimensions of agent evolution: autonomous optimization
and self-learning, multi-agent co-evolution, and evolution via
external resources. These mechanisms collectively enhance
model adaptability, reasoning, and performance in complex
environments. We summarize the methods in Table 2.


_2.3.1_ _Autonomous Optimization and Self-Learning_


Autonomous optimization and self-learning allow LLMs
to improve their capabilities without extensive supervision.
This includes self-supervised learning, self-reflection, selfcorrection, and self-rewarding mechanisms that enable models to explore, adapt, and refine their outputs dynamically.


_**Self-Supervised Learning and Adaptive Adjustment.**_ Selfsupervised learning enables LLMs to improve using unlabeled or internally generated data, reducing reliance on
human annotations. For example, self-evolution learning
(SE) [86] enhances pretraining by dynamically adjusting token masking and learning strategies. Evolutionary optimization techniques facilitate efficient model merging and adaptation, improving performance without extensive additional
resources [87]. DiverseEvol [88] refines instruction tuning
by improving data diversity and selection efficiency. These
advancements contribute to the autonomous adaptability of
LLMs, enabling more efficient learning and generalization
across tasks.


_**Self-Reflection and Self-Correction.**_ Self-reflection and selfcorrection enable LLMs to iteratively refine their outputs



7


by identifying and addressing errors. For instance, SELFREFINE [89] applies iterative self-feedback to improve generated responses without external supervision. In reasoning
tasks, STaR [90] and V-STaR [91] train models to verify and
refine their own problem-solving processes, reducing reliance
on labeled data. Additionally, self-verification techniques
enable models to retrospectively assess and correct their
outputs, leading to more reliable decision-making [92].
These approaches collectively enhance LLM agents’ ability
to self-reflect and self-correct, reducing hallucinations and
improving reasoning quality.
_**Self-Rewarding and Reinforcement Learning.**_ Self-rewarding
and reinforcement learning approaches enable LLMs to
enhance performance by generating internal reward signals.
Self-generated rewards help models refine decision-making,
with techniques ensuring stable and consistent learning
improvements [93]. Contrastive distillation further enables
models to align themselves through self-rewarding mechanisms [94]. Additionally, RLC [95] leverages the evaluationgeneration gap via reinforcement learning strategies, facilitating self-improvement. These methods enhance LLM
adaptability by integrating self-rewarding strategies and
reinforcement learning paradigms.


_2.3.2_ _Multi-Agent Co-Evolution_


Multi-agent co-evolution enables LLMs to improve through
interactions with other agents. This involves cooperative
learning, where agents share information and coordinate
actions, as well as competitive co-evolution, where agents
engage in adversarial interactions to refine strategies and
enhance performance.
_**Cooperative and Collaborative Learning.**_ Multi-agent collaboration enhances LLMs by enabling knowledge sharing,
joint decision-making, and coordinated problem-solving.
For instance, ProAgent [96] enables LLM-based agents
to adapt dynamically in cooperative tasks by inferring
teammates’ intentions and updating beliefs, enhancing zeroshot coordination. CORY [97] extends RL fine-tuning into a
cooperative multi-agent framework, where LLMs iteratively
improve through role-exchange mechanisms, enhancing
policy optimality and stability. CAMEL [25] develops a roleplaying framework where communicative agents collaborate
autonomously using inception prompting, improving coordination and task-solving efficiency in multi-agent settings.
These approaches contribute to more efficient, adaptable, and
intelligent multi-agent LLM systems.
_**Competitive and Adversarial Co-Evolution.**_ Competitive coevolution strengthens LLMs through adversarial interactions,
debate, and strategic competition. For example, Red-team
LLMs [98] dynamically evolve in adversarial interactions,
continuously challenging LLMs to uncover vulnerabilities
and mitigate mode collapse, leading to more robust safety
alignment. Du et al. propose a multi-agent debate framework [82] to enhance reasoning by having multiple LLMs
critique and refine each other’s arguments over multiple
rounds, improving factuality and reducing hallucinations.
Furthermore, the MAD framework [99] structures debates
among agents in a tit-for-tat manner, encouraging divergent
thinking and refining logical reasoning in complex tasks.
These competitive co-evolution strategies drive LLMs to


Fig. 3: An overview of evaluation benchmarks and tools
for LLM agents. The left side shows various evaluation
frameworks categorized by general assessment, domainspecific evaluation, and collaboration evaluation. The right
side illustrates tools used by LLM agents, tools created by
agents, and tools for deploying agents.


develop stronger reasoning, resilience, and strategic adaptability in a multi-agent adversarial manner.


_2.3.3_ _Evolution via External Resources_
External resources enhance the evolution of agents by
providing structured information and feedback. Knowledgeenhanced evolution integrates structured knowledge to
improve reasoning and decision-making, while external
feedback-driven evolution leverages real-time feedback from
tools and environments to refine model performance.
_**Knowledge-Enhanced Evolution.**_ LLMs can evolve by integrating structured external knowledge, improving reasoning,
decision-making, and task execution. For example, KnowAgent [83] improves LLM-based planning by integrating action
knowledge, constraining decision paths, and mitigating hallucinations, leading to more reliable task execution. The world
knowledge model (WKM) [84] enhances agent planning
by synthesizing expert and empirical knowledge, providing
global priors and dynamic local knowledge to guide decisionmaking. These approaches collectively improve the evolution
of LLM by incorporating diverse and structured external
information.
_**External Feedback-Driven Evolution.**_ LLMs can refine their
behavior by leveraging external feedback from tools, evaluators, and humans to improve performance iteratively.
For example, CRITIC [100] allows LLMs to validate and
revise their outputs through tool-based feedback, improving
accuracy and reducing inconsistencies. STE [101] enhances
tool learning by simulating trial-and-error, imagination, and
memory, enabling more effective tool use and long-term
adaptation. SelfEvolve [102] adopts a two-step framework
where LLMs generate and debug code using feedback from
execution results, enhancing performance without human
intervention. These approaches enable LLMs to evolve
iteratively by integrating structured feedback, improving
adaptability and robustness.


**3** **EVALUATION AND TOOLS**

