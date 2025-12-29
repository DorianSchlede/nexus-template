<!-- Source: 10-TalkHier-2502.11098.pdf | Chunk 1/5 -->

## **Talk Structurally, Act Hierarchically:** **A Collaborative Framework for LLM Multi-Agent Systems**

Zhao Wang _[∗][,][†]_, Sota Moriyama _[∗]_, Wei-Yao Wang, Briti Gangopadhyay, Shingo Takamatsu


Sony Group Corporation, Japan





**Abstract**


Recent advancements in LLM-based multiagent (LLM-MA) systems have shown promise,
yet significant challenges remain in managing
communication and refinement when agents
collaborate on complex tasks. In this paper,
we propose _Talk Structurally, Act Hierarchi-_
_cally (TalkHier)_, a novel framework that introduces a structured communication protocol for context-rich exchanges and a hierarchical refinement system to address issues such
as incorrect outputs, falsehoods, and biases.
_TalkHier_ surpasses various types of SoTA, including inference scaling model (OpenAI-o1),
open-source multi-agent models (e.g., AgentVerse), and majority voting strategies on current LLM and single-agent baselines (e.g., ReAct, GPT4o), across diverse tasks, including open-domain question answering, domainspecific selective questioning, and practical
advertisement text generation. These results
highlight its potential to set a new standard for
LLM-MA systems, paving the way for more
effective, adaptable, and collaborative multiagent frameworks. The code is available at
[https://github.com/sony/talkhier.](https://github.com/sony/talkhier)


**1** **Introduction**


Large Language Model (LLM) Agents have broad
applications across domains such as robotics (Brohan et al., 2022), finance (Shah et al., 2023; Zhang
et al., 2024b), and coding (Chen et al., 2021; Hong
et al., 2023). By enhancing capabilities such as
autonomous reasoning (Wang et al., 2024b) and
decision-making (Eigner and Händler, 2024), LLM
agents bridge the gap between human intent and
machine execution, generating contextually relevant responses (Pezeshkpour et al., 2024).
Recent research has primarily focused on LLMbased Multi-Agent (LLM-MA) systems, which


*These authors contributed equally to this work
†Corresponding author: Zhao Wang (Email Address:
Zhao.Wang@sony.com)



Figure 2: Our _TalkHier_ built on GPT4o surpasses inference scaling models (OpenAI-o1), open-source multiagent models (AgentVerse and etc.), and models with
majority voting strategies (ReAct, GPT4o) on five subtasks of MMLU.


leverage collective intelligence and specialize each
agent with the corresponding subtasks, to solve
complicated and multi-step problems. For instance,
previous works on LLM-MA have explored approaches where instances of LLMs, referred to as
agents (Xi et al., 2023; Gao et al., 2023; Wang
et al., 2024a; Cheng et al., 2024; Ma et al., 2024),
collaborate synergistically by debate (Chen et al.,
2024), reflection (He et al., 2024), self-refinement
(Madaan et al., 2023), or multi-agent based feedback refinement (Yang et al., 2023). These systems
employ diverse communication topologies to enable efficient interactions between agents such as













Figure 1: Existing LLM-MA methods (left) face two major challenges: 1) disorganized, lengthy text-based communication protocols, and 2) sequential or overly similar flat multi-agent refinements. In contrast, _TalkHier_
(right) introduces a well-structured communication protocol and a hierarchical refinement approach.











1


Chain (Wei et al., 2022) and Tree (Yao et al., 2023)
structures, among others (Qian et al., 2024; Zhuge
et al., 2024; Zhang et al., 2024a).

Despite the promising advancements in LLMMA systems, several challenges in this field remain
unexplored (shown in Figure 1):

**1) Disorganized communication in text form.**
Agents often engage in debates (Zhao et al., 2024),
share insights (Chen et al., 2024), or perform refinement (Madaan et al., 2023; Yang et al., 2023) to effectively solve complex tasks, with their exchanges
primarily in text form (Guo et al., 2024). However, communication often becomes disorganized
because it requires explicitly describing agent tasks,
providing background context for the communication, and specifying the required output formats.
These factors together lead to lengthy and unstructured exchanges, making it difficult for agents to
manage subgoals, maintain output structures, and
retrieve independent memories from prior actions
and observations.

**2) Refinement schemes.** While some studies
have shown that incorporating agent debates (Chen
et al., 2024) or evaluation-based multi-agent refinement (Wang et al., 2023; Yang et al., 2023)
can improve system accuracy, these approaches
also expose significant limitations. As the number of agents increases, LLM-MA systems face
challenges in effectively summarizing opinions or
feedback (Fang et al., 2024). They often fail to
balance these inputs, frequently overlooking some
or exhibiting biases based on the order in which
feedback is provided (Errica et al., 2024).

In this paper, we propose a novel collaborative LLM-MA framework called _Talk Structurally,_
_Act Hierarchically (TalkHier)_ -the first collaborative
LLM-MA framework to integrate a well-structured
communication protocol with hierarchical refinement. Our key contributions shown in Figure 1 and
2 are as follows:


1. **Well-Structured, Context-Rich Communica-**
**tion Protocol:** _TalkHier_ introduces a novel communication protocol that incorporates newly proposed elements: _messages_, _intermediate outputs_,
and relevant _background information_ . These
components form the foundation of a wellstructured protocol that organizes agent communication, ensuring clarity and precision. By
embedding these elements, _TalkHier_ significantly improves communication accuracy and
efficiency compared to traditional text-based



methods.


2. **Hierarchical Refinement in LLM-MA Sys-**
**tems:** _TalkHier_ enhances traditional multi-agent
evaluation systems with a hierarchical refinement framework, enabling agents to act hierarchically. This approach addresses such as the
difficulty in summarizing opinions or feedback
as the number of agents increases, balancing
diverse inputs, and mitigating biases caused by
the order of feedback processing, resulting in
more reliable and robust interactions.


3. **State-of-the-Art Results Across Benchmarks:**
Experimental results show that _TalkHier_
achieves state-of-the-art performance on diverse benchmarks, including selective problemsolving in complex sub-domains, open question
answering, and Japanese text generation tasks.
Ablation studies confirm the effectiveness of
each component, demonstrating their contributions to the framework’s overall success.


**2** **Related Work**


**Collaborative LLM-MA.** LLM-MA systems
enable agents to collaborate on complex tasks
through dynamic role allocation, communication,
and task execution (Guo et al., 2024; Han et al.,
2024). Recent advancements include agent profiling (Yang et al., 2024), hierarchical communication (Rasal, 2024), and integration of reasoning
and intentions (Qiu et al., 2024). However, challenges remain in ensuring robust communication,
avoiding redundancy, and refining evaluation processes (Talebirad and Nadiri, 2023). Standardized
benchmarks and frameworks are needed to drive
future progress (Li et al., 2024).


**Communication in LLM-MA.** Effective communication is crucial for collaborative intelligence (Guo et al., 2024). While many previous works, including chain (Wei et al., 2022),
tree (Yao et al., 2023), complete graph (Qian et al.,
2024), random graph (Qian et al., 2024), optimizable graph (Zhuge et al., 2024), and pruned
graph (Zhang et al., 2024a) methods have focused
on communication topologies, there has been limited discussion on the optimal form of communication. Most systems rely on text-based exchanges (Zhang et al., 2024a; Shen et al., 2024),
which is inefficient and prone to errors as agents
often lose track of subtasks or fail to recall prior
outputs as tasks grow in complexity. We argue



2


Figure 3: Comparisons between existing approaches (left) and ours (right). Our _TalkHier_ proposes a new communication protocol (first row) featuring context-rich and well-structured communication information, along with a
collaborative hierarchical refinement (second row) where evaluations provide summarized and coordinated feedback
within an LLM-MA framework.



for structured communication protocols that guide
subtasks with clear, context-specific instructions,
ensuring coherence across interactions.


**Feedback-Based Refinement.** Feedback mechanisms, such as Self-Refine (Madaan et al., 2023)
and generator-evaluator frameworks (Wang et al.,
2023), improve system accuracy through iterative
refinement. However, these methods face challenges in managing diverse feedback, which can
lead to bias or inefficiencies if inputs are not wellorganized (Xu et al., 2024). Scalable, unbiased
solutions are essential to enhance multi-agent evaluation processes.



_c_ [(] _ij_ _[t]_ [)] _∈Cp_ represents a communication between
agents _vi_ and _vj_ along an edge _eij ∈E_ at time step
_t_ . While the graph structure _G_ remains fixed, the
communication events _Cp_ are dynamic and adapt
to the specific task.


**3.1** **Agents with Independent Memory**


Each agent _vi ∈V_ in graph _G_ can be formally
represented as:



**3** **Methodology**


_TalkHier_ aims to design a LLM-MA system represented as a graph _G_ = ( _V, E_ ), where _V_ denotes
the set of agents (nodes) and _E_ represents the set
of communication pathways (edges). Given an input problem _p_, the system dynamically defines a
set of communication events _Cp_, where each event



_vi_ = (Role _i,_ Plugins _i,_ Memory _i,_ Type _i_ ) _._


Role _i_ : Assign roles such as generator, evaluator,
or revisor based on the task type. Plugins _i_ : External tools or plugins attached for domain-specific
operations. Memory _i_ : An agent-specific memory
that stores and retrieves information relevant to the
agent’s role and task. Type _i_ : Specifies whether
the agent is a Supervisor ( _S_ ) responsible for overseeing task success, or a Member ( _M_ ) focused on
problem-solving.
The first two components—Role _i_, and
Plugins _i_ —are standard in most related works,



3


Figure 4: Prompts for acquiring the contents of the context-rich, structured communication protocol in _TalkHier_ .



forming the foundation of agent functionality. Our
contributions lie in the last three components:
Memory _i_, which equips each agent with our refined
independent, agent-specific memory for reasoning,
Team _i_, which represents the team the agent is a
part of, and Type _i_, which explicitly categorizes
agents into Supervisor ( _S_ ) roles, responsible for
overseeing the multi-agent team and ensuring
task success, or Member ( _M_ ) roles, focused on
problem-solving and optionally utilizing plugins.
These additions enable hierarchical, structured
collaboration and role-specific operations within
the framework.


**Agent-Specific Memory.** To enhance efficiency
and scalability, each agent _vi_ maintains an independent memory, Memory _i_ . Unlike long-term memory,
which relies on a shared memory pool accessible
by all agents, or short-term memory, which is limited to a single session or conversational thread, our
proposed memory mechanism is agent-specific but
not limited to session or conversational thread.


_TalkHier_ allows each agent to independently retain and reason on its past interactions and knowledge, offering two key advantages: independence,
where each agent’s memory operates without interference from others, avoiding centralized dependencies; and persistence, enabling agents to maintain
historical data across sessions for consistent and
informed decision-making.



**3.2** **Context-Rich Communication Between**
**Agents**


Communication between agents is represented by
communication events _c_ [(] _ij_ _[t]_ [)] _[∈C][p]_ [, where each event]

_c_ [(] _ij_ _[t]_ [)] [encapsulates the interaction from agent] _[ v][i]_ [ to]
agent _vj_ along an edge _eij ∈E_ at time step _t_ .
Formally, a communication event _c_ [(] _ij_ _[t]_ [)] [is defined as:]


_c_ [(] _ij_ _[t]_ [)] [= (] **[M]** _ij_ [(] _[t]_ [)] _[,]_ **[ B]** [(] _ij_ _[t]_ [)] _[,]_ **[ I]** _ij_ [(] _[t]_ [)][)] _[,]_

where **M** [(] _ij_ _[t]_ [)] [indicates the] _[ message]_ [ content sent]
from _vi_ to _vj_, containing instructions or clarifications, **B** [(] _ij_ _[t]_ [)] [denotes] _[ background]_ [ information to en-]
sure coherence and task progression, including the
problem’s core details and intermediate decisions,
and **I** [(] _ij_ _[t]_ [)] [refers to the] _[ intermediate output]_ [ generated]
by _vi_, shared with _vj_ to support task progression
and traceability, all at time step _t_ . These structures
ensure that agents of _TalkHier_ accomplish efficient
communication and task coordination.


**Communication Event Sequence.** At each time
step _t_, the current agent _vi_ communicates with a
connected node _vj_, with one being selected by the
LLM if more than one exists. The elements of
each edge **M** [(] _ij_ _[t]_ [)] _[,]_ **[ B]** _ij_ [(] _[t]_ [)] [and] **[ I]** _ij_ [(] _[t]_ [)] [are then generated]
by invoking an independent LLM. To ensure consistency, clarity, and efficiency in extracting these
elements, the system employs specialized prompts
tailored to the roles of Supervisors and Members,
as illustrated in Figure 4. Most notably, background
information **B** [(] _ij_ _[t]_ [)] [is not present for connections]



4


**Algorithm 1:** Hierarchical Refinement

**Input:** Initial output **A** 0 generated by the Generator node _v_ main [Gen] [, quality threshold] _[ M]_ [threshold][, maximum iterations] _[ T]_ [max]
**Output:** Final output **A** final

**1** Initialize iteration counter _t ←_ 0

**2 repeat**

**3** _t ←_ _t_ + 1 // Step 1: Task Assignment from _vmain_ _[s]_ [to] _[ v]_ _eval_ _[s]_

**4** **T** [(] assign _[t]_ [)] [=] _[ {]_ [(][Role] _v_ eval _[S]_ _[,]_ [ Criteria] _[v]_ eval _[S]_ [)] _[}]_ // Step 2: Task Distribution by _veval_ _[s]_

**5** **T** [(] distribute _[t]_ [)] [=] _[ {]_ [(][Criterion] _v_ eval _[Ei]_ [)] _[}]_ _i_ _[k]_ =1 // Step 3: Evaluation

**6** **F** _v_ [(] _[t]_ eval _[Ei]_ [)] = _f_ evaluate( **A** _t−_ 1 _,_ Criterion _v_ eval _Ei_ [)] _[,]_ _∀v_ eval _[E][i]_ _[∈V]_ [eval]



i


**7** **F** eval [(] _[t]_ [)] [=] _[ {]_ **[F]** [(] _[t][E]_ [)]



i


[(] _[t]_ [)] _}_ // Step 4: Feedback Aggregation by _veval_ _[s]_

_v_ eval _[Ek]_



i


[(] _[t]_ [)] _, . . .,_ **F** [(] _[t]_ [)]

_v_ eval _[E]_ [1] _v_



i


**8** **F** [eval] summary [=] _[ f]_ summarize [(] **[F]** [(] eval _[t]_ [)] [)] // Step 5: Summarizing results

**9** **if** _M_ ( **F** _[eval]_ _summary_ [)] _[ ≥M]_ _threshold_ **[then]**

**10** **return A** final = **A** _t−_ 1 // Step 6: Return the current text if above threshold

**11** **A** _t_ = _f_ revise( **A** _t−_ 1 _,_ **F** [eval] summary [)] // Step 7: Revision of the text

**12 until** _t ≥_ _Tmax_
**13 return A** final = **A** _t_


operations and assign tasks to each member, the
Generator ( _v_ main [Gen] [) gives solutions for a given prob-]
lem, and the Revisor ( _v_ main [Rev] [) refines outputs based]
on given feedback. Furthermore, the evaluation
team is composed of _k_ independent evaluators _v_ eval _[E][k]_ [,]
each of which outputs evaluation results for a given
problem based on their specified metric. The overall structure is shown in Figure 5.

Figure 5: Illustrated hierarchy of _TalkHier_ .



i



i


from Member nodes to Supervisor nodes. These information are then established as a communication
event _c_ [(] _ij_ _[t]_ [)] _[∈C][p]_ [.]


**3.3** **Collaborative Hierarchy Agent Team**


The entire graph _G_ consists of multiple teams, each
represented as a subset _V_ team _⊆V_ . Each team includes a dedicated supervisor agent _v_ team _[S]_ [and one]
or more member agents _v_ team _[M]_ [. A key feature of the]
hierarchical structure in _TalkHier_ is that a member agent in one team can also act as a supervisor
for another team, creating a nested hierarchy of
agent teams. As shown in the second row of Figure 3, this structure enables the entire graph _G_ to
represent a hierarchical node system, where teams
are recursively linked through supervisor-member
relationships.
Formally, the hierarchical structure of agents
with two teams is defined as:


_V_ main = _{v_ main _[S]_ _[, v]_ main [Gen] _[, v]_ eval _[S]_ _[, v]_ main [Rev] _[}][,]_

_V_ eval = _{v_ eval _[S]_ _[, v]_ eval _[E]_ [1] _[, v]_ eval _[E]_ [2] _[, . . ., v]_ eval _[E][k]_ _[}][,]_

where the Main Supervisor ( _v_ main _[S]_ [) and Evaluation]
Supervisor ( _v_ eval _[S]_ [) oversee their respective team’s]



i


**Algorithm.** Algorithm 1 illustrates the operation
of our hierarchical refinement process within the
collaborative agent framework. The process begins with the main Supervisor ( _v_ main _[S]_ [) assigning]
tasks to the evaluation Supervisor ( _v_ eval _[S]_ [), who then]
distributes evaluation criteria to individual evaluators ( _v_ eval _[E][i]_ [). Each evaluator assesses the gener-]
ated output ( **A** _t−_ 1) based on their assigned criteria,
producing detailed feedback. The evaluation Supervisor aggregates and summarizes this feedback
( **F** [eval] summary [) before passing it to the main Supervi-]
sor. The main Supervisor evaluates whether the
summarized feedback meets the quality threshold
( _M_ threshold). If the threshold is satisfied, the output
is finalized; otherwise, the Revisor ( _v_ main [Rev] [) refines]
the output for further iterations. This iterative refinement ensures accurate and unbiased collaboration across the agent hierarchy.


The main Supervisor evaluates whether the
summarized feedback meets the quality threshold
( _M_ threshold), defined vaguely as “ensuring correctness” or “achieving high relevance.” If satisfied, the
output is finalized; otherwise, the Revisor ( _v_ main [Rev] [)]
refines it. Details of our settings are in Appendix B,
Appendix C, and Appendix D.



i


5


**4** **Experiments**


In this section, we aim to answer the following
research questions across various domains:
**RQ1:** Does _TalkHier_ outperform existing multiagent, single-agent, and proprietary approaches on
general benchmarks?
**RQ2:** How does _TalkHier_ perform on open-domain
question-answering tasks?
**RQ3:** What is the contribution of each component
of _TalkHier_ to its overall performance?
**RQ4:** How well does _TalkHier_ generalize to more
practical but complex generation task?


**4.1** **Experimental Setup**


**Datasets.** We evaluated _TalkHier_ on a diverse collection of datasets to assess its performance across
various tasks. The Massive Multitask Language
Understanding (MMLU) Benchmark (Hendrycks
et al., 2021) tests domain-specific reasoning problems including Moral Scenario, College Physics,
Machine Learning, Formal Logic and US Foreign
Policy. WikiQA (Yang et al., 2017) evaluates opendomain question-answering using real-world questions from Wikipedia. The Camera Dataset (Mita
et al., 2024) focuses on advertisement headline generation, assessing the ability to create high-quality
advertising text.


**Baselines.** To evaluate _TalkHier_, we compared it
against a comprehensive set of baselines including:

  - **GPT-4o** (OpenAI, 2024a), based on OpenAI’s
GPT-4 model with both single-run and ensemble majority voting (3, 5, or 7 runs).
