<!-- Source: 12-CollabSurvey-2501.06322.pdf | Chunk 3/7 -->

_4.2.3_ _Coopetition._ Coopetition, a strategic blend of cooperation and competition, enables agents
to collaborate on certain tasks to achieve shared objectives while simultaneously competing with
others. This concept, though relatively new, has been explored in recent studies. For instance, [2, 34]
simulate negotiation scenarios where agents with differing, and sometimes conflicting, interests
engage in trade-offs to reach mutually beneficial agreements. In these scenarios, agents assign
varying values to their interests, creating opportunities for compromise and collaboration.
The mixture-of-experts (MoE) framework also fits in the coopetition collaboration type [6, 15].
In MoE, multiple expert models compete to contribute to the final output, with a gating mechanism
selecting the most appropriate experts for each input. This competitive selection process ensures
that the combined expertise of the selected experts leads to a superior overall model performance.
The coopetitive interaction among experts occurs first during the model’s training phase, where
they are trained to specialize in different aspects of the data, thereby enhancing the model’s capacity
to handle diverse tasks effectively.


_4.2.4_ _Coordination of Different Collaboration Channel Types._ In LLM-based MASs, there is often
the need for complex interactions that transcend singular collaboration types like competition
or cooperation. Different agents may participate in different collaboration channels C, each with
distinct interaction types, coordinating together to achieve the overall system goal O _𝑐𝑜𝑙𝑙𝑎𝑏_ . This
hybrid collaboration model combines features of each collaboration type, such as competition
or cooperation, leveraging the strengths of each to enhance overall system performance and
adaptability.
Hybrid collaboration has been explored in various LLM-based MASs. For example, in LEGO [54],
in the first state of the framework, 3 agents cooperate to augment information about the current
task, and in the second state, a competitive channel is created between an Explainer LLM agent
and a Critic LLM agent to refine their outputs for the task.
Consider the scenario in [77] where two agents, _𝑎_ 1 and _𝑎_ 2 engage in a competitive debate to argue
opposing viewpoints on a topic, aiming to persuade a judge agent _𝑎_ 3. The competitive collaboration
channel between _𝑎_ 1 and _𝑎_ 2 can be denoted as _𝑐_ comp, characterized by the agents involved and the
competitive interaction type. Simultaneously, agent _𝑎_ 3 cooperates with both _𝑎_ 1 and _𝑎_ 2 to reach a
final decision, forming cooperative collaboration channels _𝑐_ coop with the group of debating agents.
Incorporating multiple collaboration channels with distinct interaction types in LLM-based MASs
enriches the interaction dynamics and enhances the system’s ability to achieve complex objectives.
This design reflects real-world scenarios where diverse interactions contribute to successful outcomes, and it opens avenues for developing more sophisticated and adaptable MASs. However,
coordinating multiple collaboration channels introduces complexity. To manage the complexity of
hybrid collaboration, coordination mechanisms such as role assignments, communication protocols,
and shared knowledge representations are essential.
Finally, we present a summary of the definitions, advantages, and disadvantages of each collaboration type in Table 2, accompanied by illustrative examples in Fig. 3.


**4.3** **Collaboration Strategies**

In general, there are three different kinds of MAS cooperation strategies: 1) Rule-based, 2) Rolebased, and 3) Model-based. Fig. 4 shows instances of three types of strategies. The research on
several cooperation protocols is summarized in Table 3.


_4.3.1_ _Rule-based Protocols._ Interactions among agents in C are strictly controlled by predefined
rules, ensuring that agents coordinate their actions according to system-wide constraints on
acceptable inputs _𝑥𝑐𝑜𝑙𝑙𝑎𝑏_ . These protocols enforce a structured collaboration channel setup, where
agents act on the basis of specific rule sets rather than probabilistic or role-specific inputs.


14 Tran et al.


Table 3. Collaboration strategies: definitions, advantages, disadvantages, and example scenarios.


**Protocol** **Definition** **Advantages** **Disadvantages** **Example Scenario** **Refs.**


Rule-based Agent interactions are strictly  - Efficient, high  - Low adaptablility Question answering [151]
controlled by predefined rules. predictability to uncertainty Concensus seeking [21, 151]

                          - Consistency and                          - Difficult to scale Navigation [162]
fairness ensured for complex tasks Peer-review process [143]
Role-based Leverage distinct predefined  - Modularity and  - Rigid structure Decision making [24, 120]
roles or communication structure reusability         - Performance Software development [24, 56, 120]
Each agent operates on segmented         - Leverage agents’ relies on agents’ Robotics [83]
objective, support overall goal. own expertise connection level
Model-based Based on input (with uncertainty  - Adaptability to  - Complex to Game environments [75, 141]
in perception), environment and dynamic env. implement Decision making [90, 141]
shared goals, agents carry out         - Robust to         - Computationally Robotics [16]
probabilistic decision making. uncertainties expensive


An article applies rules-based social psychology-inspired protocols, where agents mimic human
collaborative dynamics such as debate and majority rule, achieving efficient collaboration without
deviating from predefined pathways [151]. Another recent paper highlights a dynamic rule-based
protocol that leverages predefined event-triggered conditions to optimize communication and coordination in LLM-powered systems. These protocols reduce unnecessary communication between
agents while maintaining effective collaboration through clearly defined rules of interaction [162].
A peer review-inspired collaboration mechanism uses predefined rules to allow agents to critique,
revise, and refine each other’s output, improving the precision of reasoning in complex tasks [143].
Finally, research on consensus seeking in MASs highlights how rule-based strategies enable agents
to negotiate and align their actions toward a shared goal, with applications in multi-robot aggregation tasks [21]. Through the experiment, four consensus strategies, the effects of agent personality
and network topology on the rule-following tendency, and the final results were discovered and
discussed, highlighting the considerate and cooperative nature of LLM-driven agents in consensus
seeking.
Rule-based strategies offer the advantage of efficiency and predictability in MASs. By employing
a set of predefined rules to govern agent interactions, these strategies ensure straightforward
implementation and facilitate debugging, as system behavior can be easily traced back to specific
rules. This approach is particularly efficient for tasks with well-defined procedures and limited
variability, such as consensus seeking and navigation. Moreover, the predetermined constraints help
to ensure the fairness of the system, since the limitation of power is imposed on each agent [151].
However, rule-based systems suffer from a lack of adaptability. When confronted with unexpected
situations or dynamic environments that fall outside the scope of the predefined rules, these systems
may fail to respond appropriately or may require significant manual intervention to adjust the rule
set. Furthermore, as the complexity of the task increases, the number of rules required can grow
exponentially, making the system difficult to scale and maintain.


_4.3.2_ _Role-based Protocols._ Role-based protocols in MASs leverage distinct predefined roles or
division of work, where each agent, _𝑎𝑖_ ∈A, operates on a segmented objective _𝑜𝑖_ ⊂ _𝑂𝑐𝑜𝑙𝑙𝑎𝑏_ usually based on their domain knowledge - that supports the system’s overarching goal. The
“AgentVerse” model demonstrates the efficacy of assigning specific responsibilities to each agent,
simulating human-like collaboration, and strengthening alignment through role adherence [24].
This strategy classifies the role of each agent in C, enabling them to work proactively and cohesively
to avoid overlaps. In another study, MetaGPT formalizes role-based protocols by encoding Standard
Operating Procedures (SOPs), where each agent’s role is defined by expert-level knowledge, allowing
agents to act as specialized operators who can verify each other’s results [56]. This protocol prevents


Multi-Agent Collaboration Mechanisms: A Survey of LLMs 15


Fig. 4. Different types of collaboration strategies, illustrated by multiple use cases. In the rule-based example,
agents debate and participate in majority voting. Software project is an instance of role-based protocol. In
games, agents communicate and perform probabilistic decision-making in uncertain environments.


error propagation by modularizing task distribution, yielding coherent outputs even in complex
projects. In other environments such as multi-robot, the RoCo framework assigns LLM agents to
dialogue roles [83]. These settings allow specialized agents to increase the effectiveness of physical
interactions by optimizing planning and trajectory tasks. As a final example, BabyAGI demonstrates
how distinct roles in task creation and prioritization enhance efficiency within the framework, as
agents autonomously manage their tasks in parallel using 3 different chains for Task creation, Task
prioritization, and Execution [120].
By giving each agent a specific function and set of tasks, role-based techniques improve the
efficiency and structure of MASs. Because agents are individually created, implemented, and
updated, this explicit division of labor encourages modularity and increases the reusability of
individual modules, enhancing the system performance as a whole [56]. Thus, this technique is
suitable for MAS that simulates a real-world environment with well-defined specialized jobs, such
as in business or technology. Despite these advantages, if roles are not properly specified, role-based
systems can show rigidity, which might result in disputes or functional deficiencies. Furthermore,
the interdependencies between agent jobs are intrinsically linked to the system’s performance.
The efficacy of the system as a whole can be severely impacted by ineffective communication or
blocking of interactions between agents in various roles.


_4.3.3_ _Model-based Protocols._ Model-based protocols in MASs provide flexibility for decision making, especially in environments where uncertainties in input perception may impact agents’ actions.
Within this structure, the probabilistic nature of decision-making supports each agent _𝑎𝑖_ ∈A in
anticipating probable outcomes based on the analysis of input _𝑥𝑐𝑜𝑙𝑙𝑎𝑏_, current environmental data
E, and shared collaborative goals _𝑂𝑐𝑜𝑙𝑙𝑎𝑏_ .
An article explores how probabilistic models, specifically through Theory of Mind (ToM) inferences, allow agents to make decisions that account for the likely mental states of their peers,
improving task alignment even when agents face divergent objectives within _𝑂𝑐𝑜𝑙𝑙𝑎𝑏_ [75]. This
approach effectively distributes the focus of each agent based on ToM-based predictions, enhancing
coordination through probabilistic adjustments in C, the collaboration channels. Another paper
attempts to improve human-AI collaboration by integrating logical rules with ToM to infer human goals and guide agent actions [16]. The approach employs probabilistic logical reasoning,
treating logic rules as latent variables and utilizing a hierarchical reinforcement learning model
with ToM to enable agents to dynamically adapt their beliefs and actions based on observed behaviors. By combining rule-based probabilistic social perception with dynamic collaboration, the


16 Tran et al.


proposed framework effectively addresses uncertainties in input perception and facilitates robust
task performance, as demonstrated by significant improvements in benchmarks like Watch-andHelp and HandMeThat, showcasing the potential of this method in complex, partially observable
environments.
Furthermore, as explored in another article, the Probabilistic Graphical Modeling (PGM) framework enriches the performance of MASs in games like Chameleon, where agents infer the goals and
rationalities of each other within shared collaboration channels [141]. This PGM integration enables
agents to process ambiguous contextual data, enhancing performance across multi-objective tasks
in environments with unpredictable variables. Another study uses probabilistic timed automata to
model state transitions within intelligent environments, such as an adaptive parking system, where
the collaboration channel C adjusts in response to agent movements and time-sensitive variables,
optimizing interactions in real-time [90].
By allowing agents to make probabilistic decisions based on their perception of the environment,
common objectives, and inherent uncertainties, model-based methods give MAS a high degree of
flexibility and robustness. This method works especially effectively in dynamic contexts where
agents have to constantly modify their behavior to adapt to changing circumstances, such as
game and robotics environments. Because model-based systems can use probabilistic reasoning to
determine the most likely course of action, they are more resilient to noise and unforeseen events.
However, the greater complexity of model-based solutions is a trade-off for their flexibility. These
systems can be difficult to design and deploy because they need complex models of the environment
and agent interactions. Additionally, model-based systems’ probabilistic decision-making might
result in computationally costly procedures, which may restrict their use in real-time.


**4.4** **Communication Structures**

Overall, the communication structure of multi-agent collaboration can be categorized into four
main classes, referred to as 1) Centralized topology, 2) Decentralized and distributed topology,
and 3) Hierarchical topology (see Fig. 5). Table 4 demonstrates the summary of research studies
according to different communication structures.


Table 4. Definition of communication structures: advantages, disadvantages, and example scenarios


**Stuctures** **Definition** **Advantages** **Disadavantages** **Example Scenario** **Refs.**


Centralized Collaboration decision is  - Simple to design and implement.  - If the central node fails Question answering [64, 95, 106]
concentrated in a central          - Efficient resource allocation. the entire system might collapse. Decision making [97, 119]
agent.          - System is less resilient to

                                              - disruptions.
Decentralized Collaboration decision is  - System can continue functioning  - Inefficient resource allocation. Question answering [61, 77, 140, 146]
distributed among multiple even if some agents fail.         - High communication overheads Decision making [24, 151]
agents.          - High scalability. Reasoning [41, 152]
•Agents can operate autonomously Code Generation [20, 59]
and adapt to changes in the system. Storyboard generation [158]
Hierarchical Agents are arranged in •Low bottleneck as communication, •Edge devices become critical as Code Generation [74, 81, 105]
a layered system with tasks are distributed across levels. a failure in edge devices lead to Question answering [18]
distinct roles and levels •Efficient resource allocation. system failure. Reasoning [41]
of authority. •Tasks are offload among levels. •High complexity and latency. Storyboard generation [132]


_4.4.1_ _Centralized Structure._ The centralized structure (also known as a star structure) is an implementation where every agent is connected to a central agent. In a centralized structure, the
collaboration channels C = { _𝑐_ _𝑗_ } are set as the participating-serving nature in a centralized communication channel. The serving agent acts as a hub through which all other agents communicate and,
thus, has the objective of managing, controlling, and coordinating the interactions or collaborations
among participants within the system. One of the most well-known centralized structures in multiagent collaboration can be aligned with Federated Learning (FL). In general, FL is a MAS where _𝑛_


Multi-Agent Collaboration Mechanisms: A Survey of LLMs 17

































































































Fig. 5. Summary of communication structures of MAS. Figure (a) illustrates the centralized structure, which
can be categorized into two types. In the first type, the LLM resides on distributed agents, with FedIT serving
as an example. In the second type, the LLM is hosted on a central agent, as exemplified by AutoAct. Figure (b)
depicts the decentralized structure, with AgentCF as an example. Finally, Figure (c) represents the hierarchical
structure, with the CAMEL architecture.


agents collaborate toward learning an optimal aggregated model that achieves a collaborative goal
setting for all agents.
Recently, many works provide alternate collaboration paradigms besides average loss minimization, such as layer-wise aggregation [92] or on-serving side optimization for global learning rate
adaptation [62] and invariant gradient direction searching [8, 9]. With the advent of LLMs, LLMbased FL has become a highly efficient approach for training distributed clients. The integration of
LLMs and FL represents a compelling collaboration that leverages each other’s strengths to address
their respective limitations, embodying a complementary relationship [163]. From the perspective
of integrating FL into LLMs, FL enhances data accessibility for LLMs. Specifically, FL facilitates the
incorporation of personal and task-specific data, enabling LLMs to be effectively customized for
individual applications. For example, Google has utilized FL to train next-word prediction models
for LLMs using mobile keyboard input data, significantly improving user experience [13], [142].
Besides FL, some other researchers considered a central agent as a hub to coordinate the communication among multi-agents. To aggregate multiple LLM responses, LLM-Blender [64] calls
different LLMs in one round and uses pairwise ranking to combine the top responses. It has also
been shown effective in distributing workloads to LLMs and concatenating their answers, thus
producing better results [95, 106, 119]. AgentCoord [97] is an open-source, user-friendly tool that
helps users design effective coordination strategies for multiple LLMs. It provides a visual interface
and various interactive features to facilitate this process, as demonstrated through a formal user
study. [164, 166] introduce a method for extracting knowledge from multiple agents and synthesizing it into an aggregated graph. This approach leverages LLMs to iteratively perform querying,
searching, and answering processes until the construction of the graph is complete.


18 Tran et al.


_4.4.2_ _Decentralized and Distributed Structure._ Decentralized MAS differs from centralized systems
by distributing control and decision-making across agents. Each agent operates based on local information and possibly limited communication with other agents, requiring sophisticated algorithms
for interaction and decision-making. Decentralized MAS are prevalent in various fields, such as
robotics (e.g., swarm robotics), networked systems (e.g., sensor networks), and distributed AI.
Decentralized communication operates as channel set C = { _𝑐_ _𝑗_ } are assigned to peer-to-peer,
where agents directly communicate with each other, a structure commonly employed in world
simulation applications. Researchers have found taking multiple LLM instances to debate for a fixed
number of rounds can boost their factuality and reasoning capabilities [41, 77, 140]. On specific
reasoning tasks, adopting a dynamic directed acyclic graph structure for LLMs has been shown
effective [152]. Also, recent studies [24, 146, 151] have demonstrated that optimal communication
structures vary with tasks and compositions of agents.
Recent research has explored methods to coordinate agents with diverse expertise to enhance
outcomes across a wide range of tasks that benefit from varied knowledge domains. For instance,
MedAgent [122] integrates medical agents with different specialties to deliver comprehensive
analyses of patients’ conditions and treatment options. Similarly, MetaGPT [56] and ChatDev

[105] facilitate collaboration among agents representing distinct roles, such as product managers,
designers, and programmers, to improve the quality of software development. MARG [32] provides
a framework that leverages the expertise of multiple specialized agents to review scientific papers.
Creative content generation tasks, including creative writing and storyboard design, have also
benefited from multi-agent collaboration, as demonstrated by AutoAgents [20] and OKR-Agent

[158]. SOA [59] propose a self-organized MAS that can automatically generate and modify largescale code. With the self-organization of agents, a single agent no longer needs to comprehend
the codebase, making it possible to scale up large-scale code simply by increasing the number
of agents. Authors in [150] propose the agent-based collaborative filtering approach, namely
AgentCF. Specifically, AgentCF considers not only users but also items as agents. Both kinds of
agents are equipped with memory modules, maintaining the simulated preferences and tastes of
potential adopters. At each step, user and item agents are prompted to autonomously interact,
thereby exploring whether these simulated agents can make consistent decisions with real-world
interaction records.
To implement the decentralized MAS without a large amount of communication, ProAgent

[149] utilizes LLMs as a comprehensive guideline for leveraging the powerful reasoning and
planning capabilities of LLMs in cooperative settings. From the given guideline, ProAgent can
interpretably analyze the current scene, explicitly infer teammates’ intentions, and dynamically
adapt its behavior accordingly. Authors in [99] build an agent society using LLMs augmented with
memories to simulate human behavior. To efficiently leverage the prior knowledge of agents in the
system for an efficient MAS collaboration, the generative agents have a mechanism for storing a
comprehensive record of each agent’s experiences, deepening its understanding of itself and the
environment through reflection, and retrieving a compact subset of that information to inform the
agent’s actions. OpenAgents, proposed by [139], aims to transition LLMs from theoretical tools
to interactive systems serving diverse users. They include three agents: the Data Agent for data
analysis using Python and SQL, the Plugins Agent for API-based tasks, and the WebAgent for
autonomous web browsing. Through a user-friendly interface, OpenAgents offers swift responses
and robustness for general users while providing developers and researchers with an efficient local
deployment platform for building and evaluating language agents in real-world settings.


_4.4.3_ _Hierarchical Structure._ Layered communication is structured hierarchically, with agents at
each level having distinct functions and primarily interacting within their layer or with adjacent


Multi-Agent Collaboration Mechanisms: A Survey of LLMs 19


Table 5. Comparisons of coordination and orchestration architectures: definition, advantages, disadvantages,
and implementations from previous works.


**Arch.** **Definition** **Advantages** **Disadvantages** **Mechanism** **Implementation** **Refs.**


Static Static list of  - Ensures consistent  - Relies on accurate Predefined Rules Sequential chaining [23, 135, 138]
collaboration channels, task execution. initial design and Domain Knowledge Code generation [60]
leveraging prior       - Utilize domain domain knowledge. Recommendation [131]
knowledge to optimize knowledge.       - Fixed channels may Literary translation [133]
the system’s deal with scalability
performance. and fexibility.l
Dynamic Adaptable to changing/ - Adaptable roles and - Higher resource Management Agent Based on DAG [61]
evolving environments channels based on usage due to real- Based on personas [132]
and task requirements. task needs. time adjustments. Based on inputs [33, 44]

                  - Handles complex                   - Potential failures in
and evolving tasks dynamic adjustments.
dynamically.


layers. AgentVerse [24] presents a use case where agents with diverse backgrounds collaborate
to develop solutions for hydrogen storage station siting. Authors in [81] introduce a framework
called Dynamic LLM-Agent Network (DyLAN), which organizes agents in a multi-layered feedforward network. DyLAN functions in two stages to incorporate task-oriented agent collaborations.
The first stage is termed Team Optimization, where DyLAN selects top contributory agents unsupervisedly among the initial team of candidates according to the task query, based on their
individual contributions. The most contributory agents from a smaller team collaborate at the
second stage, Task Solving, thereby minimizing the impact of less effective agents from the final
answer. Specifically, the collaboration begins with a team of agents, and an LLM-powered ranker in
the middle dynamically deactivates low-performing agents, thus, integrating dynamic communication structures into DyLAN. This setup facilitates dynamic interactions, incorporating features like
inference-time agent selection and an early-stopping mechanism, which collectively enhance the
efficiency of cooperation among agents. [74] have conceptualized assemblies of agents as a group
and focused on exploring the potential of their cooperation [18, 41, 105, 132] found social behaviors
autonomously emerge within a group of agents. Inspired by network topology and intelligent agent
communication, authors in [146] proposed four communication paradigms (i.e., memory, report,
relay, and debate) to determine the counterparts for model communication (i.e., bus, star, ring, tree).


**4.5** **Coordination and Orchestration**

Coordination and orchestration in LLM-based multi-agent collaborative systems extend beyond
the functionality of individual collaboration channels, focusing instead on the relationships and
interactions among multiple channels. These mechanisms define how collaboration channels are
created, ordered, and characterized, forming the backbone of multi-agent interactions. Depending
on their design, coordination, and orchestration can be categorized as either static or dynamic,
each offering distinct advantages. A summary is provided in Table 5.


_4.5.1_ _Static Architecture._ Static architectures rely on domain knowledge and predefined rules to
establish collaboration channels. These approaches ensure that interactions align with specific
domain requirements, leveraging prior knowledge to optimize the system’s performance. For
instance, sequential chaining of channels is a commonly used strategy in static coordination.
In [23], three LLM agents are connected sequentially, where the output of one agent feeds into
the next alongside the initial human input, _𝑦𝑖_ +1 = _𝑦𝑖_ || _𝑥𝑖_ || _𝑥𝑐𝑜𝑙𝑙𝑎𝑏_ with _𝑥𝑐𝑜𝑙𝑙𝑎𝑏_ as initial human
input, and || as the concatenation operation. The first two agents specialize as domain experts,
offering complementary viewpoints, while the third agent acts as a summarizer. This setup proved
highly effective for solving complex tasks such as college-level science multiple-choice questions,


20 Tran et al.


outperforming single-agent methods like chain-of-thought reasoning. Similarly, sequential channel
aggregation is explored in other works [135, 138], where collaboration channels are connected in a
sequence to amplify the benefits of individual channels.
Domain-specific knowledge plays a critical role in static coordination architectures. In the
MapCoder framework [60], for example, collaboration channels are explicitly designed to emulate
the program synthesis process, involving agents tasked with recall, planning, code generation,
and debugging. The agents communicate through predefined collaboration channels, ensuring a
structured workflow where the planning agent directly exchanges information with the coding
agent. Similarly, the MACRec framework [131] applies static coordination to recommendation tasks,
where specialized agents such as the Manager, User/Item Analyst, and Reflector operate through
explicitly defined channels. These workflows leverage domain expertise to optimize interactions,
such as enabling the User/Item Analyst to access detailed data about users and items. A similar
approach is implemented in literary translation [133], where collaboration channels mirror the
traditional workflow of translation publication.


_4.5.2_ _Dynamic Architecture._ Dynamic coordination and orchestration architectures, on the other
hand, are designed to adapt to changing/evolving environments and task requirements. These
architectures rely on management agents or adaptive mechanisms to assign roles and define collaboration channels in real-time. For instance, the Solo Performance Prompting (SPP) approach [132]
dynamically identifies relevant personas based on the input. A management agent generates LLM
agents with tailored system prompts corresponding to these personas, allowing them to brainstorm
and refine solutions collaboratively. This adaptability enables systems to handle diverse tasks
effectively, as demonstrated in the ability of GPT-4 to identify accurate and meaningful personas
across a wide range of scenarios.
In another example [61], a graph-based orchestration mechanism employs an LLM-based Orchestrator agent to dynamically construct a Directed Acyclic Graph (DAG) from user input. Nodes
in the graph represent tasks, while edges define dependencies and collaboration channels between
agents. This architecture allows agents to execute tasks in parallel or sequence as dictated by the
DAG structure. A Delegator agent consolidates the results from all completed tasks to form the final
response, significantly enhancing system responsiveness and scalability, particularly for multi-step,
complex queries.


**4.6** **Summary and Lessons Learned**
