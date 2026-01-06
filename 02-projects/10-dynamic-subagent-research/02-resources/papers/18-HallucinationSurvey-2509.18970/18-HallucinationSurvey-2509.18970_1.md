<!-- Source: 18-HallucinationSurvey-2509.18970.pdf | Chunk 1/8 -->

JOURNAL OF L [A] TEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021 1

## LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions


Xixun Lin, Yucheng Ning, Jingwen Zhang, Yan Dong, Yilong Liu, Yongxuan Wu, Xiaohua Qi, Nan Sun, Yanmin
Shang, Kun Wang, Pengfei Cao, Qingyue Wang, Lixin Zou, Xu Chen, Chuan Zhou, Jia Wu, Peng Zhang,
Qingsong Wen, Shirui Pan, Bin Wang, Yanan Cao, Kai Chen, Songlin Hu, Li Guo



_**Abstract**_ **—Driven by the rapid advancements of Large Lan-**
**guage Models (LLMs), LLM-based agents have emerged as**
**powerful intelligent systems capable of human-like cognition,**
**reasoning, and interaction. These agents are increasingly being**
**deployed across diverse real-world applications, including student**
**education, scientific research, and financial analysis. However,**
**despite their remarkable potential, LLM-based agents remain**
**vulnerable to hallucination issues, which can result in erroneous**
**task execution and undermine the reliability of the overall**
**system design. Addressing this critical challenge requires a**
**deep understanding and a systematic consolidation of recent**
**advances on LLM-based agents. To this end, we present the first**
**comprehensive survey of hallucinations in LLM-based agents. By**
**carefully analyzing the complete workflow of agents, we propose**
**a new taxonomy that identifies different types of agent hallucina-**
**tions occurring at different stages. Furthermore, we conduct an**
**in-depth examination of eighteen triggering causes underlying the**
**emergence of agent hallucinations. Through a detailed review of**
**a large number of existing studies, we summarize approaches for**
**hallucination mitigation and detection, and highlight promising**
**directions for future research. We hope this survey will inspire**
**further efforts toward addressing hallucinations in LLM-based**
**agents, ultimately contributing to the development of more robust**
**and reliable agent systems.**


_**Index Terms**_ **—LLM-based Agents, Hallucinations, Safety.**


I. INTRODUCTION

Language Models (LLMs) [1], [2], [3], [4], [5] have
recently showcased extraordinary capabilities across a
# **L**


X. Lin, Y. Ning, J. Zhang, Y. Dong, Y. Liu, Y. Wu, X. Qi, N. Sun,
Y. Shang, Y. Cao, K. Chen, S. Hu, and L. Guo are with Institute of
Information Engineering, Chinese Academy of Sciences, School of Cyber
Security, University of Chinese Academy of Sciences, Beijing, China.
K. Wang is with Nanyang Technological University, Singapore.
P. Cao is with Institute of Automation, Chinese Academy of Sciences,
Beijing, China.
Q. Wang is with Hong Kong University of Science and Technology, Hong
Kong, China.
L. Zou is with School of Cyber Science and Engineering, Wuhan University,
Wuhan, China.
X. Chen is with Gaoling School of Artificial Intelligence, Renmin University of China, Beijing, China.
C. Zhou is with Academy of Mathematics and Systems Science, Chinese
Academy of Sciences, Beijing, China.
J. Wu is with School of Computing, Faculty of Science and Engineering,
Macquarie University, Sydney, Australia.
P. Zhang is with the Cyberspace Institute of Advanced Technology,
Guangzhou University, Guangzhou, China.
Q. Wen is with Squirrel Ai Learning, Bellevue, USA.
S. Pan is with School of Information and Communication Technology,
Griffith University, Gold Coast, Australia.
B. Wang is with Xiaomi Company, Beijing, China.



broad spectrum of tasks, including language generation [6],
intent comprehension [7], and knowledge reasoning [8]. These
capabilities are largely attributed to the vast scale of training
data [9], model architecture innovations [10], and emergent
abilities [11] that arise during instruction tuning [12] and
in-context learning [13]. Building on these breakthroughs,
**LLM-based Agents** [14], [15], [16], [17], [18] are becoming
increasingly proficient in task automation across a wide range
of fields, marking a critical milestone on the path toward
Artificial General Intelligence (AGI) [19]. Moreover, these
agents can be orchestrated into a **LLM-based Multi-agent**
**System** (MAS) [20], [21], [22], [23], [24], where different
agents with distinct specializations collaborate and interact to
solve real-world and complex problems beyond the capacity
of any single agent through mutual cooperation, such as
knowledge sharing [25] and collaborative coordination [26].


Despite the impressive performance achieved by LLMbased agents, their rapid advancement introduces a spectrum
of safety challenges [27], [28], [29]. Among these challenges,
**Agent Hallucinations** represents a particularly significant
threat [30], [31], [32]. Previous studies on hallucinations have
primarily focused on the field of natural language generation
(NLG) [13], where hallucinations refer to the phenomenon in
which NLG models generate unfaithful or nonsensical text.
Ji et al. review recent advances in addressing hallucinations
across various NLG tasks [33]. Meanwhile, Huang et al.
specifically focus on the causes of LLM hallucinations [34].
In this context, hallucinations in LLMs are categorized into
factuality and faithfulness hallucinations. Factuality hallucinations highlight discrepancies between the generated content
and verifiable real-world facts [35]; while faithfulness hallucinations refer to deviations from the user’s original input [36].
In addition, the authors discuss several effective methods for
detecting and mitigating hallucination issues [37].


Unlike the aforementioned settings, the LLM-based agent is
a more sophisticated intelligent system, equipped with goaldirected reasoning and action-taking capabilities. Such agents
typically comprise three core modules: brain, perception, and
action [38]. The brain module is primarily responsible for
storing memory and knowledge, supporting reasoning and
decision-making for executing tasks; the perception module
extends the agent’s perceptual space, enabling it to handle
multi-modal environmental inputs; and the action module expands the agent’s action space, allowing it not only to generate



0000–0000/00$00.00 © 2021 IEEE


|I’m planning a trip to Beijing next week. Could you suggest a detailed guide<br>and pack my luggage? I’m especially interested in ancient buildings.|Col2|Col3|
|---|---|---|
|I’m planning a trip to**Beijing next week**. Could you**suggest a detailed guide**<br>and**pack my luggage**? I’m especially interested in**ancient buildings**.|I’m planning a trip to**Beijing next week**. Could you**suggest a detailed guide**<br>and**pack my luggage**? I’m especially interested in**ancient buildings**.||
|I’m planning a trip to**Beijing next week**. Could you**suggest a detailed guide**<br>and**pack my luggage**? I’m especially interested in**ancient buildings**.|||























































task allocation within the LLM-based multi-agent system including broadcasting and structure evolution further enhances the fulfillment of user requirements.



textual outputs but also to invoke tools for completing more
complex tasks. Therefore, in LLM-based agents, hallucinations
are not ”linguistic errors”, but rather a broad category of fabricated or misjudged ”human-like behaviors” that may occur at
any stage of the agent’s pipeline. Accordingly, the manifestations and causes of agent hallucinations are considerably more
complex. This complexity is reflected in three key aspects:
**1) More Diverse Types** : Rather than the straightforward
response errors of a single model, agent hallucinations are
compound behaviors arising from interactions among multiple
modules, resulting in a broader and more varied range of
hallucination types. **2) Longer Propagation Chains** : The
aforementioned hallucinations are mostly localized and singlestep errors, whereas agent hallucinations often span multiple
steps and involve multi-state transitions. Such hallucinations
are not limited to the final output; they may also arise
during intermediate processes such as perception and reasoning, where they can propagate and accumulate over time. **3)**
**More Severe Consequences** : Agent hallucinations involve
”physically consequential” errors, where incorrect embodied
actions can directly affect task execution, system devices, and
user experiences in the real world. As a result, the cost and risk
associated with agent hallucinations are significantly higher.
However, existing reviews of LLM-based agents primarily
focus on architectural designs and practical applications, while
giving far insufficient attention to the importance and urgency
of agent hallucinations.


To this end, we provide an overview of agent hallucinations
to fill this important gap and promote the advancement of



agents. In this paper, the interaction dynamics of LLMbased agents are formulated as a partially observable Markov
decision process (POMDP) where the agent [1] interacts with
the learning environment, makes decisions, receives feedback,
and updates its state over multiple time steps. Based on this
general POMDP setting, we summarize the contributions of
our work below.

_•_ **First Survey.** To the best of our knowledge, this is the
first survey to review hallucination issues in LLM-based
agents. It encompasses recent research on both mitigation
and detection methods, offering a broad perspective on
the development of LLM-based agents.

_•_ **Innovative Taxonomy.** We introduce a novel decomposition of agent components into two parts: internal state
and external behaviors. The former is characterized by a
belief state maintained by the agent, which serves as the
most fundamental unit of the agent cognition policy. External behaviors refer to a series of proactive procedures
guided by the belief state. Through this internal–external
distinction, we can classify agent hallucinations based on
the specific stage at which they occur, covering five types
of agent hallucinations.

_•_ **Comprehensive Review.** For each type of agent hallucinations, we offer a formal definition, illustrative examples, and an in-depth discussion of representative studies.
Based on this, we identify eighteen triggering causes
of agent hallucinations. Furthermore, we summarize ten


1Throughout this paper, we use the term ”agent” to denote the LLM-based
agent, unless otherwise specified.


JOURNAL OF L [A] TEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021 3



general approaches for hallucination mitigation, along
with corresponding detection methods, to provide readers
with a clear and up-to-date overview of the current
research landscape on agent hallucinations.

_•_ **Future Outlook.** By reviewing and summarizing existing
solutions to hallucination problems and their possible
limitations, we outline several promising directions for
future exploration that will need to be fully investigated
to advance both academic research and real-world deployment of LLM-based agents.

_•_ **Open Resource.** We provide a well-curated collection
of resources, encompassing over 200+ related papers,
which we make publicly available on GitHub [2] to foster
community engagement and collaboration.

**Paper Organization.** The remainder of this paper is structured as follows. Section II introduces the formal definition of LLM-based agents. Based on this definition, Section III presents a new taxonomy of agent hallucinations. Section IV reviews existing solutions, with particular emphasis on
methodologies for hallucination mitigation. Section V outlines
future research directions. Section VI concludes the survey.


II. FORMAL DEFINITION OF LLM-BASED AGENTS


Fig. 1 provides an overview of agent goal completion. The
formal definition of LLM-based agents including interaction
dynamics and LLM-based agent loop is given here.


_A. Interaction Dynamics_


The interaction dynamics between the agent and the learning
environment is usually formulated as a Partially Observable
Markov Decision Process (POMDP) [39] which is defined as a
8-tuple: _E_ = ( _S, A, T, G, O, Z, R, γ_ ). The description of each
element in _E_ is given here:

_• S_ is the state space where _s ∈S_ represents a true environment state. A POMDP explicitly models an agent decision
process in which the agent cannot directly observe the
underlying state. Instead, the agents must maintain a
**Belief State** to represent its subjective understanding of
the learning environment.

_• A_ is the action space. An action _a ∈A_ involves content
generation or the use of external tools, such as scheduling
events via calendar APIs and issuing smart home control
commands.

_• T_ : _S × A →_ _P_ ( _S_ ) is the state transition probability
function. For each state-action pair ( _s, a_ ), it specifies a
probability distribution over possible subsequent states.
For example, executing a “turn off lights” action may
result in reaching the desired state with 90% probability,
while network latency or system errors could cause the
state to remain unchanged with 10% probability.

_• G_ is the goal space. Each goal _g ∈G_ specifies a particular
objective of users.

_• O_ is the observation space. Each observation _o ∈O_
represents a partial view of _s_, which can be manifested
through different modalities. Partial observability may


2https://github.com/ASCII-LAB/Awesome-Agent-Hallucinations.



stem from multiple factors, such as the complexity of the
learning environment and the limitations of the agent’s
perceptual capabilities.

_• Z_ : _S × A →O_ is the observation function. For each
state-action pair ( _s, a_ ), it provides a possible observation

_o_ for the agent.

_• R_ : _S × A →R_ is the reward function, where _R_ is the
reward space. For each state-action pair ( _s, a_ ), it provides
a feedback _r ∈R_, and _r_ is usually expressed in numerical
form.

_• γ ∈_ [0 _,_ 1) is the discount factor. It serves to balance
the importance between immediate and future rewards.
Since events that occur farther in the future are harder to
predict accurately, it is generally desirable to reduce the
significance of long-term rewards.


_B. LLM-based Agent Loop_


Given a specific goal _g_, accomplishing it typically requires
multiple execution loops. Furthermore, since the true environment state cannot be directly observed, an LLM-based agent
needs to maintain a belief state _bt_ that represents its internal
and subjective understanding of the learning environment. In
the multi-loop process, the agent continuously updates _bt_,
allowing _bt_ to be dynamically refined across diverse contexts
and over extended time spans. _bt_ is the most fundamental unit
in the agent’s loop process, forming the basis of all agentic
operations. Based on _bt_, we further introduce the agent’s
external behaviors including reasoning, execution, perception,
and memorization. The concrete calculation in each loop can
be given here:

_•_ **Reasoning** : The agent first generates a plan _pt_ for the
next action conditioned on _bt_ and _g_ :


_pt_ = Φ( _bt, g_ ) _._ (1)


_•_ **Execution** : The agent then translates _pt_ into an executable action _at_ :


_at_ = _E_ ( _bt, pt_ ) _._ (2)


_at_ typically involves the invocation of relevant external
tools.

_•_ **Feedback** : The learning environment would objectively
provide a reward _rt_ based on _st_ and _at_ :


_rt_ = _R_ ( _st, at_ ) _._ (3)


_•_ **Environment** **Transition** : The learning environment
transitions to the next state _st_ +1 _∈S_ according to the
following generated probability distribution:


Pr( _st_ +1 _|st, at_ ) = _T_ ( _st, at_ ) _._ (4)


_•_ **Perception** : The agent would then perceive _st_ +1 and
generate the observation _ot_ +1 _∈O_ :


_ot_ +1 = _Z_ ( _st_ +1 _, bt, at_ ) _._ (5)


_•_ **Memorization** : Both _at_ and _ot_ +1 are used for updating
its external memory module:


_mt_ +1 = _LM_ ( _mt, at, ot_ +1) _._ (6)


JOURNAL OF L [A] TEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021 4




_•_ **Belief Update** : Based on the above decision-making
process and feedback, the agent refines _bt_ as follows,


_bt_ +1 = _LB_ ( _bt, mt_ +1 _, at, rt, ot_ +1) _._ (7)


The agent ultimately receives a cumulative discounted reward
(i.e., [�] _t_ _[∞]_ =0 _[γ][t][r][t]_ [) as a measure of goal achievement.]
Different from the single-agent setting, in the LLM-based
MAS, each agent must communicate with other agents to
accomplish goals. To model these processes, a communication structure _Gt_ is introduced among _N_ agents. Furthermore, _Gt_ would evolve with time to align with the dynamic
adjustments of MAS. Therefore, compared with the above
loop, the loop of LLM-based MAS is given as “Reasoning–
Execution– **Broadcasting** –Feedback–Environment Transition–
Perception–Memorization–Belief Update– **Structure Evolu-**
**tion** ”. This loop includes two additional procedures: Broadcasting and Structure Evolution. Broadcasting means that the
agent broadcasts its message to neighboring nodes according
to its plan, while structure evolution indicates that the communication structure _Gt_ can be updated in each iteration. The
complete description of the loop of MAS is given in Appendix
A.



_A. Reasoning Hallucinations_


Reasoning serves as the cornerstone of an agent’s functionality, influencing behavior analysis and decision-making [40],

[41], [42]. Upon receiving a specific goal _g_, the agent first
leverages its own reasoning capabilities to perform goal understanding for inferring the user’s true intention:


_•_ **Goal Understanding** : This phase occurs before the agent
executes multiple loops:


_I_ = Understand( _b_ 0 _, g_ ) _,_ (8)


where _I_ denotes the inferred intention, and _b_ 0 represents
the initial belief state. When _I_ is complex and relatively
difficult to execute, the agent would perform the intention
decomposition to decompose _I_ into a series of manageable sub-intentions _{It}_ _[n]_ _t_ =0 [.]

_•_ **Intention Decomposition** : Typically, there are two decomposition methods: pre-defined decomposition and
dynamic decomposition. In the first one, these subintentions are specified in advance:


_{It}_ _[n]_ _t_ =0 [=][ Pre-decompose][(] _[b]_ [0] _[,][ I]_ [)] _[.]_ (9)


In the second one, the sub-intention for each loop is
generated by


_It_ = Dyn-decompose( _bt, I_ ) _._ (10)


The decomposition results are dynamically optimized
based on the current belief state _bt_, enabling timely and
continuous refinement for the subsequent workflow [43].

_•_ **Planning Generation** : Each sub-intention _It_ is then
mapped to a concrete plan _pt_ for the current loop:


_pt_ = Plan( _bt, It_ ) _._ (11)



III. TAXONOMY OF AGENT HALLUCINATIONS


We first provide a formal definition of agent hallucinations.
Based on this definition, we then introduce the new taxonomy
that includes the following five types of agent hallucinations:
Reasoning Hallucinations, Execution Hallucinations, Perception hallucinations, Memorization Hallucinations, and Communication Hallucinations, as illustrated in Fig. 2. Detailed
descriptions of each type of agent hallucinations are provided
in the following sub-sections. Representative hallucination
examples are presented in Appendix B.



The subsequent sub-sections detail the triggering causes that
give rise to these three types of reasoning hallucinations.
_1) Problematic Objective Expression._ Understanding the user’s
true intention from _g_ is the first and essential step for effective




JOURNAL OF L [A] TEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021 5

