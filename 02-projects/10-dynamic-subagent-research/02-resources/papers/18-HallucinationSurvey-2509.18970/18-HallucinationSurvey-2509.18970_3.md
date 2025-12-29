<!-- Source: 18-HallucinationSurvey-2509.18970.pdf | Chunk 3/8 -->

granularity or delayed index updates, can further exacerbate
this problem, potentially resulting in information loss and the
retrieval of outdated memory. Finally, insufficient understanding of **Query Semantics** is also an important problem. If the
agent misinterprets the query’s intent or overlooks specific task
requirements [121], [122], it may fail to capture contextual
cues necessary for accurate retrieval.
_3) Imperfect Priority Assignment._ This issue mainly manifests
in two aspects: **Forgetting Priority** and **Merging Priority** .
For memory forgetting, poorly assigned priorities can result
in the elimination of important information or the retention of
irrelevant content, ultimately compromising the accuracy of
subsequent decisions [112], [123]. Moreover, when the agent
merges multiple memory fragments, failure to correctly assess
their priorities [124], [125] may result in the merged memory
containing inherent conflicts [126], [127]. Some of these
conflicts are implicit [128]: Although memory fragments may
appear similar, they differ significantly in key semantic details,
thereby increasing the difficulty of priority determination.
_4) Inaccurate Information Writing._ When performing longterm tasks and engaging in multi-turn interactions, agents
must summarize, structure, and store relevant historical information to the memory module. However, this process is
susceptible to **Information Compression** issues, where the
generated summaries may be overly general, omit crucial
details [129], [130], [131], or introduce distortions due to
imperfect abstraction [132], [133], [111]. Additionally, nonstandardized **Memory Formats** with disorganized structures
can hinder writing efficiency [111], [134]. Memory **Capac-**
**ity Constraints** exacerbate these challenges, because limited
storage may necessitate the selective retention of information [112], [135], increasing the risk that salient but less
frequently accessed information is discarded.


_E. Communication Hallucinations_



Compared with the independent operations of a single agent,
LLM-based MAS emphasizes collaboration and coordination
to harness collective intelligence for solving more complex
and demanding tasks [136]. In such systems, effective interagent communication serves as an essential requirement [137],
facilitating the exchange of ideas and the coordination of plans
among agents [138].
The following sub-sections provide a detailed account of
triggering causes underlying communication hallucinations.
_1) Erroneous Message Propagation._ In LLM-based MAS,
agents fundamentally rely on LLMs [38], [139], [30] to generate messages for exchanging information with other agents.
However, since LLMs are prone to the well-known **Factuality**
**and Faithfulness Hallucinations** [34], some agents may produce messages containing inaccurate facts, misinterpretations
of shared knowledge, or misleading inferences [140], [141],

[142], thereby giving rise to communication hallucinations.
Beyond this, **Content Redundancy** is also an important cause,
where agents generate unnecessary or repetitive content that
obscures critical signals, increases cognitive load, and sometimes leads to redundant task execution steps that manifest as
logical errors [143], [144], [141]. **Information Asymmetry**
can further exacerbate this issue. Because agents own different
roles and positions within MAS, the information accessible to
them varies, and such asymmetric settings may yield vague or
incomplete instructions that hinder task comprehension [145]
and amplify the risk of biased decisions [146].
_2) Uncoordinated Communication Protocols._ Communication
protocols govern how agents exchange messages, directly
determining the efficiency, reliability, and coordination of
their interactions [147], [137], [148]. Without a unified and
effective protocol, agents may ”talk past each other”, leading to communication hallucinations. First, LLM-based MAS
usually follows a manner of **Asynchronous Scheduling** [22],
so when receiving and processing instructions, agents may
encounter issues of information loss and information overload.
Such temporal discrepancies can result in information errors,
thereby increasing the risk of hallucinatory outputs [149],

[150]. Second, communication protocols define the **Message**
**formats** . Current LLM-based agents predominantly rely on the
format of natural language [151] which often introduces instruction ambiguity. Adopting structured formats (e.g., JSON)
can improve clarity and rigor of expression, which mitigates
the risk of miscommunication [152], [153]. Finally, LLMbased MAS demands a robust **Fault-tolerant Design**, incorporating confirmation conditions and synchronization constraints
to avoid erroneous decisions caused by message loss or delays
in dynamic or noisy environments [154], [155].
_3) Ineffective Network Updates._ Network topology defines how
agents are interconnected, determining who communicates
with whom and how frequently [137], [20], [156]. As discussed in Appendix A, the network topology is continuously
evolving, and network updates reshape the propagation paths
of messages within MAS. When network updates are ineffective, they can induce communication hallucinations due to
inconsistent or outdated inter-agent connections [141], [142],

[157]. Although recently proposed strategies improve the
flexibility and responsiveness of MAS, they often suffer from


JOURNAL OF L [A] TEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021 9



delayed updates and poor coordination [20], [158], [159]. If
the updated network fails to accurately reflect agents’ current
relevance or expertise, messages may be routed to inappropriate recipients, leading to misunderstandings or redundant
reasoning in LLM-based MAS.


IV. SYSTEMATIC METHODOLOGY


In this section, we provide a comprehensive review of recent
methods for mitigating and detecting hallucinations in agents.
For mitigation, we systematically group existing approaches
into three main categories in Section IV-A: **1) Knowledge**
**Utilization**, which leverages external and internal knowledge
to address hallucination issues; **2) Paradigm Improvement**,
which focuses on developing advanced learning paradigms
to prevent agent hallucinations during training and inference;
and **3) Post-hoc Verification**, which introduces verification
techniques to calibrate agent outputs and reduce the risk of
hallucinations. In Fig. 3, we provide a simple illustration
of each specific mitigation approach. For detection, existing
methods are fewer compared to mitigation, so we place
detection methods after mitigation methods. In Section IV-B,
we review the available detection approaches corresponding to
each type of agent hallucinations.


_A. Agent Hallucination Mitigation_


_1) Knowledge Utilization._ This category equips LLM-based
agents with accurate and reliable information support, enabling
multi-dimensional regulation of their reasoning, execution,
perception, and memorization behaviors. This, in turn, helps
reduce hallucinatory outputs stemming from knowledge gaps
and biases. Here we categorize knowledge utilization into
two types: **a) External Knowledge Guidance** : Agent hallucinations often arise from insufficient knowledge guidance.
Therefore, external knowledge serves as a critical resource for
mitigating hallucinations and enhancing output reliability. **b)**
**Internal Knowledge Enhancement** : This line of research focuses on activating or rectifying the agent’s internal knowledge
to better mitigate hallucinations.
_a) External Knowledge Guidance (EKG)_ [4] _._ We categorize the
existing approaches of external knowledge guidance into two
types: **Expert Knowledge** and **World Models** .
Expert knowledge refers to the domain-specific information
distilled from the behaviors and decision-making processes
of human experts or high-performing systems during task
execution. Owing to its high reliability and precision, expert
knowledge serves as a robust external reference, significantly
reducing the likelihood of hallucinations across various agentic
operations. In related literature, expert knowledge can be
manifested different forms, and we list several representative
forms: **i) Knowledge base methods** : Expert knowledge can
be stored as knowledge bases, such as introspective reasoning
knowledge bases [160], action knowledge bases [59], experiential knowledge bases [161], from which agents can retrieve
real cases and incorporate them into prompts to support
more accurate decision-making [61]. **ii) Rule-based methods** :


4The abbreviation is added here mainly to save space in Table I.



expert knowledge can be leveraged to establish rules such
as mathematical rules [77], linguistic rules [71], procedural
rules [162] or MAS communication protocols [155]. These
rules can explicitly constrain the agent’s external behaviors,
mitigating agent hallucination risks [163]. **iii) Data construc-**
**tion methods** : By leveraging expert annotations and prompting techniques, synthetic datasets can include diverse and
targeted instruction–response pairs [164], Q&A pairs [165] or
preference pairs [166]. These curated datasets can enhance the
agent’s capability to handle complex scenarios, including finegrained reasoning, tool usage, and multi-modal perception.
World models refer to systems that construct useful representations of the world, equipping agents with foundational
world knowledge [167]. This enables them to handle realworld problems and reject outputs that contradict established
facts, thereby effectively mitigating the occurrence of agent
hallucinations [168]. In POMDP setting, world models are particularly important for constructing more accurate estimations
of partially observable environments [169], [170]. The scope
of world knowledge encompasses a wide range of domains,
from fundamental **Physical Principles** [171] such as Newton’s
laws of motion and the conservation of mass to complex
**Social Systems and Structures** [57], [172]. For example,
NavMorph [173] leverages the world model to provide knowledge of the physical environment, avoiding navigation biases
caused by environmental unfamiliarity, while WKM [174]
supplies common-sense knowledge—such as the need to clean
ingredients before cooking—to achieve behaviors aligned with
human expectations.
_b) Internal Knowledge Enhancement (IKE)._ Current enhancement strategies can be broadly classified into two types:
**Internal Knowledge Activation** and **Internal Knowledge**
**Rectification** . The former aims to leverage **Prompt Engi-**
**neering** to carefully stimulate and utilize the agent’s internal knowledge, guiding it to fully exploit its capabilities.
Here we highlight several representative prompting techniques:
**i) Chain-of-Thought (CoT)** : By incorporating step-by-step
reasoning instructions [175], [176] into the prompt, CoT
guides the agent to break down complex problems and output
intermediate steps in a logical sequence, thereby enhancing the
accuracy and reliability of handling multi-step tasks. **ii) Tree-**
**of-Thought (ToT)** : Building upon CoT, ToT explores and
evaluates multiple reasoning paths in parallel [177], [58], fully
utilizing the diversified information within the agent’s internal
knowledge to strengthen the completeness and robustness
of its reasoning process. **iii) Constrained Prompting** : By
incorporating various forms of constraints [178], [179] such
as semantic [180] and spatial constraints [181] into prompts,
this approach guides the agent to focus on task-relevant
information, effectively reducing the generation of irrelevant
content.
Internal knowledge rectification generally involves two
representative paradigms. The first is **Knowledge Editing**
which replaces inaccurate or outdated knowledge with correct
knowledge while minimizing disruptions to other internal
knowledge [114]. It is typically divided into two main approaches [182]: the locate-and-edit approach [183], which
identifies and modifies specific knowledge components; the


JOURNAL OF L [A] TEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021 10































































Fig. 3. A simple illustration of approaches to agent hallucination mitigation. It encompasses three branches, knowledge utilization, paradigm improvement,
and post-hoc certification, comprising a total of ten representative methods.



meta-learning approach [184], which aims to to learn how to
update the model’s parameters for adjusting knowledge for
new information. The second is **Knowledge Unlearning** . In
contrast to knowledge editing, it focuses on removing erroneous knowledge to improve the agent’s reliability. It includes
two main approaches [185]: parameter optimization [186],
which fine-tunes model parameters under certain conditions
(e.g., parameter update scopes[187]) to forget some targeted
knowledge; parameter merging [188], which performs offline
operations on model parameters without further training.
_2) Paradigm Improvement._ This section focuses on enhancing
the agent’s capabilities through general learning paradigms
to mitigate hallucinations. We summarize six representative
paradigms as follows.
_a) Contrastive Learning (CoL)_ is a well-established selfsupervised learning paradigm whose core idea is to learn
more discriminative representations by comparing similarities
and differences between samples [189], [190], [191]. By
incorporating contrastive learning, the agent can better identify
relevant and accurate patterns, reducing errors when handling
unfamiliar or incomplete task inputs and effectively mitigating
hallucination issues [192], [193], [194].
_b) Curriculum Learning (CuL)_ is a learning paradigm inspired
by the way humans learn. Its core idea is to start training
the model with ”easy” examples and gradually move to
”harder” ones, improving learning efficiency and generalization ability [189]. By leveraging curriculum learning, agents
rapidly accumulate successful experiences by starting with
simpler tasks and gradually transferring this knowledge to



more complex scenarios. This progressive learning paradigm
enhances their fundamental capabilities, effectively mitigating
agent hallucinations [195], [196], [94].
_c) Reinforcement Learning (RL)_ serves as a fundamental
learning paradigm, emulating the biological learning process
of ”trial, feedback, and adjustment”. This approach enables
agents to interact with their environment and learn to maximize
cumulative rewards through iterative trial and error [197].
Through the reinforcement learning paradigm, the agent can
adjust its policy based on rewards, thereby optimizing future
decision-making, learning to achieve goals in complex environments, and significantly mitigating potential hallucination
issues in multi-turn interactions [198], [199], [200], [201],

[202]. In addition, there are also studies that aim to improve
the reliability of reward signals in order to enhance the overall
model effectiveness [203].
_d) Causal Learning (CaL)_ refers to the process in statistical
machine learning that goes beyond capturing mere correlations
and instead aims to model, discover, and leverage causal
relationships between variables, thereby enhancing the model’s
interpretability and generalization ability [204], [205]. In the
context of LLM-based agents, identifying and leveraging potential causal relationships within task inputs and decisionmaking processes enables more accurate understanding of how
different factors influence task outcomes. This helps reduce
representational errors and logical inconsistencies for mitigating perception [206], [207] and reasoning hallucinations [208],

[209].
_e) Graph Learning (GL)_ is a class of machine learning


JOURNAL OF L [A] TEX CLASS FILES, VOL. 14, NO. 8, AUGUST 2021 11


TABLE I
AN OVERVIEW OF MITIGATION METHODS. TO SAVE SPACE, WE USE THE ABBREVIATIONS OF HALLUCINATION TYPES AND MITIGATION METHODS
MENTIONED EARLIER. “✔” INDICATES THAT RELATED WORKS ALREADY EXIST; “–” INDICATES THAT IT HAS NOT YET BEEN EXPLORED.


Knowledge Post-hoc
Branch Paradigm Improvement
Utilization Verification
Type

EKG IKE CoL CuL RL CaL GL DO SM VA


|Reasoning<br>Hallucinations|GUHs<br>IDHs<br>PGHs|✔<br>✔<br>✔|✔<br>✔<br>✔|✔<br>–<br>✔|–<br>–<br>✔|✔<br>–<br>✔|–<br>–<br>✔|–<br>✔<br>✔|–<br>✔<br>✔|✔<br>✔<br>✔|✔<br>✔<br>✔|
|---|---|---|---|---|---|---|---|---|---|---|---|
|Execution<br>Hallucinations|TSHs<br>TCHs|✔<br>✔|✔<br>✔|✔<br>✔|✔<br>✔|✔<br>✔|–<br>–|✔<br>–|–<br>–|✔<br>✔|✔<br>✔|
|Perception<br>Hallucinations|Perception<br>Hallucinations|✔|✔|✔|–|✔|✔|–|✔|–|✔|
|Memorization<br>Hallucinations|MRHs<br>MUHs|✔<br>✔|–<br>✔|–<br>✔|–<br>–|–<br>–|–<br>–|✔<br>✔|–<br>–|–<br>–|✔<br>✔|
|Communication<br>Hallucinations|Communication<br>Hallucinations|✔|–|–|–|✔|–|✔|–|✔|✔|



paradigms specifically designed to handle graph-structured
data, which has been widely applied in various domains such
as social networks, bioinformatics, and recommendation systems [210], [211], [212]. It enhances the agent’s capability to
organize and manage tasks in a structured and systematic manner, particularly for tool usage and memory updates, thereby
reducing the risk of agent hallucinations [213], [17], [214]. For
example, ControlLLM [215] builds a tool graph comprising
resource and tool nodes, and employs a parallel graph search
algorithm to efficiently find appropriate tool paths for mitigating execution hallucinations. More importantly, recent studies
leverage graph learning to optimize communication topology
in LLM-based MAS [157], [216], [217]. By dynamically
learning which agents should communicate, when, and through
what channels, the system can suppress noisy message passing
while promoting informative interactions.


Unlike the aforementioned training-phase learning
paradigms, _f) Decoding Optimization (DO)_ is a test-time
learning paradigm. This paradigm can improve output quality
by adjusting probability distributions or attention patterns in
decoding processes, ensuring better alignment with inputs and
factual knowledge,thereby reducing hallucinations stemming
from reasoning errors [54], [218], [219]. Common decoding
strategies include contrastive decoding, self-calibrated
attention decoding [220] and fusion decoding [218].
Contrastive decoding [221] selects more reliable and contextconsistent outputs by comparing multiple decoding candidates.
Self-calibrated attention decoding [220] aims to dynamically
adjust the attention weights to capture more informative cues.
Fusion decoding incorporates the multi-source information
to reduce dependence on single-modal priors for mitigating
hallucinations. CGD [222] is one of representative works,
which integrates semantic similarity scores between textual
and visual content with final-layer token likelihoods to reduce
reliance on language priors.


_3) Post-hoc Verification._ This paradigm focuses on monitoring and evaluating outputs after task execution. It generally
follows a multi-step process in which, immediately after each



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


